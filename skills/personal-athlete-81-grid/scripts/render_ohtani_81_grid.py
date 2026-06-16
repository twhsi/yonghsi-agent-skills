#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape


W = H = 2400
CELL = W / 9
COLORS = {
    "thin": "#b9b9b9",
    "black": "#050505",
    "pink": "#fb8aa0",
    "red": "#ff260f",
    "cyan": "#65eadb",
    "white": "#ffffff",
    "text": "#050505",
}
DOMAIN_POSITIONS = [0, 1, 2, 3, 5, 6, 7, 8]
MENTAL_TYPES = {"recovery", "mental", "social", "longevity"}


def split_label(text):
    if "\n" in text:
        return text.splitlines()
    if len(text) <= 5:
        return [text]
    if len(text) <= 8:
        return [text[:4], text[4:]]
    return [text[:5], text[5:10]]


def text_svg(x, y, text, size=39, fill=None, weight=850):
    fill = fill or COLORS["text"]
    lines = split_label(str(text))
    line_h = size * 1.05
    start = y - (len(lines) - 1) * line_h / 2
    parts = [
        f'<text x="{x:.1f}" y="{start:.1f}" text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">'
    ]
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_h
        parts.append(f'<tspan x="{x:.1f}" dy="{dy:.1f}">{escape(line)}</tspan>')
    parts.append("</text>")
    return "\n".join(parts)


def group_cells(domain):
    items = list(domain["items"])
    if len(items) != 8:
        raise ValueError(f"{domain['name']} must have exactly 8 items")
    return items[:4] + [domain["name"]] + items[4:]


def validate(data):
    domains = data.get("domains", [])
    if len(domains) != 8:
        raise ValueError("JSON must contain exactly 8 domains")
    for domain in domains:
        if "name" not in domain or "items" not in domain:
            raise ValueError("Each domain must include name and items")
        if len(domain["items"]) != 8:
            raise ValueError(f"{domain['name']} must have exactly 8 items")


def render(data):
    validate(data)
    groups = []
    for domain in data["domains"][:4]:
        groups.append({"kind": "domain", "domain": domain})
    center_cells = [d["name"] for d in data["domains"][:4]]
    center_cells += [data.get("center", data.get("title", "個人運動員\n81宮格"))]
    center_cells += [d["name"] for d in data["domains"][4:]]
    groups.append({"kind": "center", "cells": center_cells})
    for domain in data["domains"][4:]:
        groups.append({"kind": "domain", "domain": domain})

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        "<style>text{font-family:'PingFang TC','Noto Sans CJK TC','Heiti TC','Arial Unicode MS',sans-serif;letter-spacing:0}</style>",
        f'<rect width="{W}" height="{H}" fill="{COLORS["white"]}"/>',
    ]

    for group_index, group in enumerate(groups):
        group_col = group_index % 3
        group_row = group_index // 3
        if group["kind"] == "center":
            cells = group["cells"]
            group_fill = COLORS["pink"]
        else:
            domain = group["domain"]
            cells = group_cells(domain)
            group_fill = COLORS["cyan"] if domain.get("type") in MENTAL_TYPES else COLORS["white"]

        for sub_index, label in enumerate(cells):
            col = group_col * 3 + sub_index % 3
            row = group_row * 3 + sub_index // 3
            is_global_center = group["kind"] == "center" and sub_index == 4
            is_domain_center = group["kind"] == "domain" and sub_index == 4
            fill = group_fill
            if is_global_center:
                fill = COLORS["red"]
            elif group["kind"] == "center" or is_domain_center:
                fill = COLORS["pink"]
            svg.append(
                f'<rect x="{col * CELL:.1f}" y="{row * CELL:.1f}" width="{CELL:.1f}" height="{CELL:.1f}" '
                f'fill="{fill}" stroke="{COLORS["thin"]}" stroke-width="1.2"/>'
            )
            size = 36 if is_global_center else 39
            if len(str(label)) >= 8 and not is_global_center:
                size = 34
            elif len(str(label)) <= 4 and not is_global_center:
                size = 42
            text_fill = "#ffffff" if is_global_center else COLORS["text"]
            svg.append(text_svg((col + 0.5) * CELL, (row + 0.5) * CELL, label, size=size, fill=text_fill))

    for i in range(10):
        width = 7 if i % 3 == 0 else 1.4
        color = COLORS["black"] if i % 3 == 0 else COLORS["thin"]
        p = i * CELL
        svg.append(f'<line x1="{p:.1f}" y1="0" x2="{p:.1f}" y2="{H}" stroke="{color}" stroke-width="{width}"/>')
        svg.append(f'<line x1="0" y1="{p:.1f}" x2="{W}" y2="{p:.1f}" stroke="{color}" stroke-width="{width}"/>')

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: render_ohtani_81_grid.py input.json output.svg")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    Path(sys.argv[2]).write_text(render(data), encoding="utf-8")


if __name__ == "__main__":
    main()
