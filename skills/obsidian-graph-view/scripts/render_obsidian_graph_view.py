#!/usr/bin/env python3
"""Render an Obsidian-style spherical weighted graph from project-note JSON.

This script is intentionally dependency-light. It writes SVG and HTML using the
standard library. Use headless Chrome to capture the HTML as PNG when needed.
"""
import argparse
import json
import math
import re
from pathlib import Path


def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def short_label(text, limit=12):
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def build_from_project_note_json(data, top_n):
    nodes = {}
    edges = []
    link_weight_by_code = {chunk["code"]: 0 for chunk in data.get("chunks", [])}
    for entry in data.get("index", []):
        for link in entry.get("links", []):
            link_weight_by_code[link["chunk_code"]] = link_weight_by_code.get(link["chunk_code"], 0) + link.get("weight", 1)

    for item in data.get("toc", []):
        code = item["code"]
        linked_weight = link_weight_by_code.get(code, 0)
        weight = max(item.get("cjk_count", 0), linked_weight // 3, 50)
        nodes[f"toc:{code}"] = {
            "id": f"toc:{code}",
            "kind": "toc",
            "code": code,
            "title": item["title"],
            "weight": weight,
        }

    for entry in data.get("index", []):
        kid = entry["id"]
        nodes[f"kw:{kid}"] = {
            "id": f"kw:{kid}",
            "kind": "keyword",
            "code": kid,
            "title": entry["keyword"],
            "weight": entry.get("weight", 50),
        }
        for link in entry.get("links", []):
            target = f"toc:{link['chunk_code']}"
            if target in nodes:
                edges.append({"source": f"kw:{kid}", "target": target, "weight": link.get("weight", 1)})

    top_ids = [
        node["id"]
        for node in sorted(nodes.values(), key=lambda n: (-n["weight"], n["kind"], n["title"]))[:top_n]
    ]
    top = {node_id: nodes[node_id] for node_id in top_ids}
    return top, [edge for edge in edges if edge["source"] in top and edge["target"] in top]


def layout(nodes, edges, width, height):
    ranked = sorted(nodes.values(), key=lambda n: (-n["weight"], n["kind"], n["title"]))
    positions = {}
    cx, cy = width / 2, height / 2 + 70
    rings = [(0, 1, 0, 0), (1, 7, 300, 210), (7, len(ranked), 600, 420)]
    for start, end, rx, ry in rings:
        group = ranked[start:end]
        for i, node in enumerate(group):
            if rx == 0:
                positions[node["id"]] = [cx, cy]
                continue
            angle = -math.pi / 2 + 2 * math.pi * i / len(group)
            perspective = 0.90 + 0.16 * max(0, math.sin(angle))
            positions[node["id"]] = [cx + math.cos(angle) * rx * perspective, cy + math.sin(angle) * ry]

    center_id = ranked[0]["id"] if ranked else None
    for _ in range(45):
        forces = {node_id: [0.0, 0.0] for node_id in nodes}
        ids = list(nodes)
        for i, a in enumerate(ids):
            ax, ay = positions[a]
            for b in ids[i + 1 :]:
                bx, by = positions[b]
                dx, dy = ax - bx, ay - by
                dist2 = max(dx * dx + dy * dy, 400)
                force = 4300 / dist2
                forces[a][0] += dx * force
                forces[a][1] += dy * force
                forces[b][0] -= dx * force
                forces[b][1] -= dy * force
        for edge in edges:
            a, b = edge["source"], edge["target"]
            ax, ay = positions[a]
            bx, by = positions[b]
            dx, dy = bx - ax, by - ay
            dist = max(math.sqrt(dx * dx + dy * dy), 1)
            force = (dist - 270) * 0.003
            forces[a][0] += dx / dist * force
            forces[a][1] += dy / dist * force
            forces[b][0] -= dx / dist * force
            forces[b][1] -= dy / dist * force
        for node_id in ids:
            if node_id == center_id:
                positions[node_id] = [cx, cy]
                continue
            x, y = positions[node_id]
            fx, fy = forces[node_id]
            positions[node_id] = [min(width - 210, max(210, x + fx)), min(height - 200, max(250, y + fy))]
    return positions


def render_svg(data, nodes, edges, positions, width, height, top_n):
    weights = [node["weight"] for node in nodes.values()]
    min_w, max_w = min(weights), max(weights)

    def radius_for(weight):
        norm = (weight - min_w) / max(1, max_w - min_w)
        return math.sqrt(((1500 + norm * 6200) * 2) / math.pi)

    edge_weight_max = max([e["weight"] for e in edges] or [1])
    title = data.get("title", "Obsidian Graph View")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<radialGradient id="tocBall" cx="35%" cy="28%" r="70%"><stop offset="0%" stop-color="#e0f2fe"/><stop offset="22%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#0369a1"/></radialGradient>',
        '<radialGradient id="kwBall" cx="35%" cy="28%" r="70%"><stop offset="0%" stop-color="#dcfce7"/><stop offset="22%" stop-color="#6ee7b7"/><stop offset="100%" stop-color="#059669"/></radialGradient>',
        '<radialGradient id="bgGlow" cx="50%" cy="50%" r="62%"><stop offset="0%" stop-color="#132033"/><stop offset="58%" stop-color="#080b0f"/><stop offset="100%" stop-color="#05070a"/></radialGradient>',
        '<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="10" result="blur"/><feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.33 0 0 0 0 0.72 0 0 0 0 1 0 0 0 .62 0"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        "</defs>",
        '<rect width="100%" height="100%" fill="url(#bgGlow)"/>',
        f'<text x="70" y="78" fill="#f8fafc" font-family="PingFang TC, Heiti TC, Arial" font-size="44" font-weight="800">{esc(title)} Graph View</text>',
        f'<text x="72" y="122" fill="#cbd5e1" font-family="PingFang TC, Heiti TC, Arial" font-size="23">前 {top_n} 節點；權重越高越靠中心，球型節點面積依權重放大兩倍。</text>',
    ]
    for edge in sorted(edges, key=lambda e: e["weight"]):
        sx, sy = positions[edge["source"]]
        tx, ty = positions[edge["target"]]
        line_w = 1.1 + 4.2 * edge["weight"] / edge_weight_max
        parts.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="#94a3b8" stroke-width="{line_w:.2f}" stroke-opacity=".34"/>')
    for node in sorted(nodes.values(), key=lambda n: n["weight"]):
        x, y = positions[node["id"]]
        r = radius_for(node["weight"])
        fill = "url(#tocBall)" if node["kind"] == "toc" else "url(#kwBall)"
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="#e2e8f0" stroke-width="2.3" filter="url(#glow)"/>')
        label = short_label(node["title"], 13)
        label_y = y + r + 22 if y + r + 82 < height - 70 else y - r - 52
        parts.append(f'<rect x="{x-145:.1f}" y="{label_y-22:.1f}" width="290" height="58" rx="14" fill="#020617" fill-opacity=".82" stroke="#475569"/>')
        parts.append(f'<text x="{x:.1f}" y="{label_y:.1f}" text-anchor="middle" fill="#f8fafc" font-family="PingFang TC, Heiti TC, Arial" font-size="22" font-weight="850">{esc(label)}</text>')
        parts.append(f'<text x="{x:.1f}" y="{label_y+24:.1f}" text-anchor="middle" fill="#cbd5e1" font-family="Menlo, PingFang TC, Arial" font-size="16" font-weight="700">{esc(node["code"])} · W{node["weight"]}</text>')
    parts.append(f'<text x="70" y="{height-28}" fill="#64748b" font-family="Menlo, Arial" font-size="18">nodes {len(nodes)} / edges {len(edges)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path")
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--prefix", default="obsidian-graph-view")
    parser.add_argument("--top-n", type=int, default=15)
    parser.add_argument("--width", type=int, default=1800)
    parser.add_argument("--height", type=int, default=1300)
    args = parser.parse_args()
    json_path = Path(args.json_path)
    out_dir = Path(args.out_dir) if args.out_dir else json_path.parent
    data = json.loads(json_path.read_text(encoding="utf-8"))
    nodes, edges = build_from_project_note_json(data, args.top_n)
    positions = layout(nodes, edges, args.width, args.height)
    svg = render_svg(data, nodes, edges, positions, args.width, args.height, args.top_n)
    svg_path = out_dir / f"{args.prefix}.svg"
    html_path = out_dir / f"{args.prefix}.html"
    svg_path.write_text(svg, encoding="utf-8")
    html_path.write_text(f'<!doctype html><meta charset="utf-8"><style>body{{margin:0;background:#080b0f}}</style>{svg}', encoding="utf-8")
    print(json.dumps({"svg": str(svg_path), "html": str(html_path), "nodes": len(nodes), "edges": len(edges)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
