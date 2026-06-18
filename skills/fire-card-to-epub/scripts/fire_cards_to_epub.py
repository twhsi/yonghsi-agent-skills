#!/usr/bin/env python3
"""Build a validated EPUB from FIRE-card project-note JSON."""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


XHTML_NS = "http://www.w3.org/1999/xhtml"
EPUB_NS = "http://www.idpf.org/2007/ops"
OPF_NS = "http://www.idpf.org/2007/opf"


@dataclass
class Chunk:
    code: str
    title: str
    body: str
    keywords: list[str]
    fire_card: str = ""
    filename: str = ""
    anchor: str = ""


@dataclass
class IndexEntry:
    kid: str
    keyword: str
    weight: int
    links: list[dict[str, Any]] = field(default_factory=list)
    anchor: str = ""


def esc(text: Any) -> str:
    return html.escape(str(text), quote=True)


def cjk_count(text: str) -> int:
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


def slug_code(code: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", code).strip("-").lower()
    return slug or "card"


def normalize_chunks(data: dict[str, Any]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for idx, item in enumerate(data.get("chunks", []), start=1):
        code = str(item.get("code") or f"{idx}")
        title = str(item.get("title") or f"Card {idx}")
        body = str(item.get("body") or item.get("text") or "")
        keywords = [str(k) for k in item.get("keywords", []) if str(k).strip()]
        chunk = Chunk(
            code=code,
            title=title,
            body=body,
            keywords=keywords,
            fire_card=str(item.get("fire_card") or ""),
            filename=f"part{idx:03d}.xhtml",
            anchor=f"p{idx:03d}",
        )
        chunks.append(chunk)
    if not chunks:
        raise ValueError("JSON must contain at least one chunk")
    return chunks


def normalize_index(data: dict[str, Any], chunks: list[Chunk]) -> list[IndexEntry]:
    by_keyword: dict[str, IndexEntry] = {}
    for idx, item in enumerate(data.get("index", []), start=1):
        keyword = str(item.get("keyword") or "").strip()
        if not keyword:
            continue
        kid = str(item.get("id") or f"K{idx:03d}")
        by_keyword[keyword] = IndexEntry(kid=kid, keyword=keyword, weight=int(item.get("weight", 100 - idx)), anchor=f"idx-{kid.lower()}")

    for chunk in chunks:
        for keyword in chunk.keywords:
            if keyword not in by_keyword:
                kid = f"K{len(by_keyword) + 1:03d}"
                by_keyword[keyword] = IndexEntry(kid=kid, keyword=keyword, weight=max(10, 100 - len(by_keyword) * 4), anchor=f"idx-{kid.lower()}")
            entry = by_keyword[keyword]
            entry.links.append({"code": chunk.code, "title": chunk.title, "href": f"{chunk.filename}#{chunk.anchor}", "weight": entry.weight})

    entries = sorted(by_keyword.values(), key=lambda x: (x.kid, x.keyword))
    for idx, entry in enumerate(entries, start=1):
        if not entry.kid:
            entry.kid = f"K{idx:03d}"
        entry.anchor = f"idx-{entry.kid.lower()}"
        deduped = []
        seen = set()
        for link in entry.links:
            key = link["href"]
            if key not in seen:
                deduped.append(link)
                seen.add(key)
        entry.links = deduped[:5]
    return entries


def keyword_map(entries: list[IndexEntry]) -> dict[str, IndexEntry]:
    return {entry.keyword: entry for entry in entries}


def link_keywords(text: str, entries: list[IndexEntry]) -> str:
    result: list[str] = []
    mapping = keyword_map(entries)
    keywords = sorted(mapping.keys(), key=len, reverse=True)
    idx = 0
    while idx < len(text):
        matched = None
        for keyword in keywords:
            if keyword and text.startswith(keyword, idx):
                matched = keyword
                break
        if matched:
            entry = mapping[matched]
            result.append(f'<a href="index.xhtml#{entry.anchor}">{esc(matched)}<sup>{esc(entry.kid)}</sup></a>')
            idx += len(matched)
        else:
            result.append(esc(text[idx]))
            idx += 1
    return "".join(result)


def xhtml_page(title: str, body: str) -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="{XHTML_NS}" lang="zh-Hant" xml:lang="zh-Hant">
<head>
  <meta charset="utf-8"/>
  <title>{esc(title)}</title>
  <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
</head>
<body>
{body}
</body>
</html>
'''


def render_toc(data: dict[str, Any], chunks: list[Chunk]) -> str:
    items = []
    for chunk in chunks:
        count = cjk_count(chunk.body)
        items.append(f'<li><a href="{chunk.filename}#{chunk.anchor}">{esc(chunk.code)} {esc(chunk.title)}</a><span>{count}字</span></li>')

    axes = data.get("orthogonal_check", {}).get("axes", {})
    axes_html = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in axes.items())
    sources_html = "".join(f"<li>{esc(s.get('skill', 'source'))}：{esc(s.get('role', ''))}</li>" for s in data.get("sources", []))

    body = f'''<section id="directory-card">
<h1>目錄卡</h1>
<p>{esc(data.get("subtitle", "FIRE 卡片整理成 EPUB 電子書。"))}</p>
<ol class="toc-list">
{''.join(items)}
</ol>
<h2>來源 Skill</h2>
<ul>{sources_html}</ul>
<h2>正交檢查</h2>
<dl>{axes_html}</dl>
</section>'''
    return xhtml_page("目錄卡", body)


def render_chunk(chunk: Chunk, entries: list[IndexEntry], previous_chunk: Chunk | None, next_chunk: Chunk | None) -> str:
    backlink_spans = []
    mapping = keyword_map(entries)
    for keyword in chunk.keywords:
        entry = mapping.get(keyword)
        if entry:
            backlink_spans.append(f'<span class="keyword-marker">{esc(keyword)} <a href="index.xhtml#{entry.anchor}">{esc(entry.kid)}</a></span>')
    backlinks = f'<div class="backlinks"><h2>索引回鏈</h2>{"".join(backlink_spans)}</div>' if backlink_spans else ""
    paragraphs = "".join(f"<p>{link_keywords(part.strip(), entries)}</p>" for part in re.split(r"\n\s*\n", chunk.body) if part.strip())
    fire = f"<h2>FIRE 卡</h2><pre>{esc(chunk.fire_card)}</pre>" if chunk.fire_card else ""
    links = []
    if previous_chunk:
        links.append(f'<li><a href="{previous_chunk.filename}#{previous_chunk.anchor}">上一卡：{esc(previous_chunk.code)}</a></li>')
    if next_chunk:
        links.append(f'<li><a href="{next_chunk.filename}#{next_chunk.anchor}">下一卡：{esc(next_chunk.code)}</a></li>')
    cross = f'<aside class="cross-links"><h2>交叉連結</h2><ul>{"".join(links)}</ul></aside>'
    body = f'''<article id="{chunk.anchor}">
<p class="code">{esc(chunk.code)}｜{cjk_count(chunk.body)}字</p>
<h1>{esc(chunk.title)}</h1>
{backlinks}
{paragraphs}
{fire}
{cross}
</article>'''
    return xhtml_page(f"{chunk.code} {chunk.title}", body)


def render_index(entries: list[IndexEntry]) -> str:
    sections = []
    for entry in entries:
        links = "".join(
            f'<li><a href="{esc(link["href"])}">{esc(link["code"])} {esc(link["title"])}</a><span>權重 {esc(link.get("weight", entry.weight))}</span></li>'
            for link in entry.links
        )
        sections.append(f'''<section class="index-card" id="{entry.anchor}">
<h2>{esc(entry.kid)} {esc(entry.keyword)} <span>權重 {esc(entry.weight)}</span></h2>
<ol>{links}</ol>
</section>''')
    return xhtml_page("關鍵字索引卡", "<h1>關鍵字索引卡</h1>" + "".join(sections))


def render_nav(data: dict[str, Any], chunks: list[Chunk]) -> str:
    items = ['<li><a href="Text/toc.xhtml">目錄卡</a></li>']
    for chunk in chunks:
        items.append(f'<li><a href="Text/{chunk.filename}#{chunk.anchor}">{esc(chunk.code)} {esc(chunk.title)}</a></li>')
    items.append('<li><a href="Text/index.xhtml">關鍵字索引卡</a></li>')
    title = data.get("title", "FIRE 卡片變成電子書")
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="{XHTML_NS}" xmlns:epub="{EPUB_NS}" lang="zh-Hant" xml:lang="zh-Hant">
<head><meta charset="utf-8"/><title>{esc(title)}</title><link rel="stylesheet" type="text/css" href="Styles/style.css"/></head>
<body><nav epub:type="toc" id="toc"><h1>{esc(title)}</h1><ol>{''.join(items)}</ol></nav></body>
</html>
'''


def render_opf(data: dict[str, Any], chunks: list[Chunk]) -> str:
    title = data.get("title", "FIRE 卡片變成電子書")
    creator = data.get("creator", "Codex")
    language = data.get("language", "zh-Hant")
    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="style" href="Styles/style.css" media-type="text/css"/>',
        '<item id="toc-card" href="Text/toc.xhtml" media-type="application/xhtml+xml"/>',
    ]
    spine = ['<itemref idref="toc-card"/>']
    for idx, chunk in enumerate(chunks, start=1):
        manifest.append(f'<item id="p{idx:03d}" href="Text/{chunk.filename}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="p{idx:03d}"/>')
    manifest.append('<item id="index-card" href="Text/index.xhtml" media-type="application/xhtml+xml"/>')
    spine.append('<itemref idref="index-card"/>')
    return f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="{OPF_NS}" unique-identifier="bookid" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">urn:fire-card-to-epub:{esc(slug_code(title))}</dc:identifier>
    <dc:title>{esc(title)}</dc:title>
    <dc:language>{esc(language)}</dc:language>
    <dc:creator>{esc(creator)}</dc:creator>
    <meta property="dcterms:modified">2026-06-17T00:00:00Z</meta>
  </metadata>
  <manifest>{''.join(manifest)}</manifest>
  <spine>{''.join(spine)}</spine>
</package>
'''


def write_epub_tree(data: dict[str, Any], out_dir: Path) -> tuple[list[Chunk], list[IndexEntry]]:
    chunks = normalize_chunks(data)
    entries = normalize_index(data, chunks)
    (out_dir / "META-INF").mkdir(parents=True, exist_ok=True)
    (out_dir / "OEBPS" / "Text").mkdir(parents=True, exist_ok=True)
    (out_dir / "OEBPS" / "Styles").mkdir(parents=True, exist_ok=True)

    (out_dir / "mimetype").write_text("application/epub+zip", encoding="utf-8")
    (out_dir / "META-INF" / "container.xml").write_text(
        '''<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
''',
        encoding="utf-8",
    )
    (out_dir / "OEBPS" / "Styles" / "style.css").write_text(STYLE, encoding="utf-8")
    (out_dir / "OEBPS" / "Text" / "toc.xhtml").write_text(render_toc(data, chunks), encoding="utf-8")
    for idx, chunk in enumerate(chunks):
        previous_chunk = chunks[idx - 1] if idx > 0 else None
        next_chunk = chunks[idx + 1] if idx + 1 < len(chunks) else None
        (out_dir / "OEBPS" / "Text" / chunk.filename).write_text(render_chunk(chunk, entries, previous_chunk, next_chunk), encoding="utf-8")
    (out_dir / "OEBPS" / "Text" / "index.xhtml").write_text(render_index(entries), encoding="utf-8")
    (out_dir / "OEBPS" / "nav.xhtml").write_text(render_nav(data, chunks), encoding="utf-8")
    (out_dir / "OEBPS" / "content.opf").write_text(render_opf(data, chunks), encoding="utf-8")
    return chunks, entries


def collect_ids(root: Path) -> dict[str, set[str]]:
    ids: dict[str, set[str]] = {}
    for file_path in root.rglob("*.xhtml"):
        rel = file_path.relative_to(root).as_posix()
        tree = ET.parse(file_path)
        file_ids = set()
        for el in tree.iter():
            value = el.attrib.get("id")
            if value:
                file_ids.add(value)
        ids[rel] = file_ids
    return ids


def validate_tree(root: Path, chunks: list[Chunk], entries: list[IndexEntry]) -> dict[str, Any]:
    errors: list[str] = []
    ids = collect_ids(root)
    href_count = 0
    for file_path in root.rglob("*.xhtml"):
        rel = file_path.relative_to(root).as_posix()
        base = posixpath.dirname(rel)
        tree = ET.parse(file_path)
        for el in tree.iter():
            href = el.attrib.get("href")
            if not href or href.startswith(("http:", "https:", "mailto:")):
                continue
            href_count += 1
            target_file, _, anchor = href.partition("#")
            target_rel = posixpath.normpath(posixpath.join(base, target_file)) if target_file else rel
            if not (root / target_rel).exists():
                errors.append(f"missing file: {rel} -> {href}")
            elif anchor and anchor not in ids.get(target_rel, set()):
                errors.append(f"missing anchor: {rel} -> {href}")

    return {
        "errors": errors,
        "all_href_count": href_count,
        "index_forward_links_tested": sum(len(entry.links) for entry in entries),
        "body_return_links_tested": sum(len(chunk.keywords) for chunk in chunks),
        "index_entries": len(entries),
        "true_body_cjk_count": sum(cjk_count(chunk.body) for chunk in chunks),
    }


def zip_epub(tree_dir: Path, out_path: Path) -> None:
    if out_path.exists():
        out_path.unlink()
    with zipfile.ZipFile(out_path, "w") as zf:
        zf.write(tree_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(tree_dir.rglob("*")):
            if path.is_file() and path.name != "mimetype":
                zf.write(path, path.relative_to(tree_dir).as_posix(), compress_type=zipfile.ZIP_DEFLATED)


def build_epub(json_path: Path, out_path: Path, download_copy: Path | None = None) -> dict[str, Any]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="fire-epub-") as temp_name:
        tree_dir = Path(temp_name) / "epub"
        chunks, entries = write_epub_tree(data, tree_dir)
        report = validate_tree(tree_dir, chunks, entries)
        if report["errors"]:
            return {"title": data.get("title", ""), "out": str(out_path), **report}
        zip_epub(tree_dir, out_path)
        if download_copy:
            shutil.copyfile(out_path, download_copy)
        report["file_type"] = "EPUB document"
        report["title"] = data.get("title", "")
        report["out"] = str(out_path)
        return report


STYLE = """
body {
  font-family: -apple-system, BlinkMacSystemFont, "Noto Sans CJK TC", "PingFang TC", sans-serif;
  line-height: 1.75;
  color: #202124;
  margin: 1.2em;
}
h1 { font-size: 1.5em; border-bottom: 2px solid #333; padding-bottom: .25em; }
h2 { font-size: 1.1em; margin-top: 1.4em; }
.code { font-family: ui-monospace, Menlo, monospace; color: #555; }
.toc-list li { margin: .45em 0; }
.toc-list span, .index-card span { color: #666; margin-left: .5em; font-size: .9em; }
.keyword-marker { display: inline-block; border: 1px solid #999; padding: .1em .35em; margin: .15em; border-radius: .25em; }
.cross-links { border-top: 1px solid #ccc; margin-top: 1.5em; }
pre {
  white-space: pre-wrap;
  font-family: ui-monospace, "SFMono-Regular", Menlo, monospace;
  background: #f7f7f7;
  border: 1px solid #ddd;
  padding: .8em;
}
a { color: #0645ad; }
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--download-copy", type=Path)
    args = parser.parse_args()

    report = build_epub(args.json_path, args.out, args.download_copy)
    print(f"errors: {len(report['errors'])}")
    print(f"title: {report.get('title', '')}")
    print(f"all_href_count: {report['all_href_count']}")
    print(f"index_forward_links_tested: {report['index_forward_links_tested']}")
    print(f"body_return_links_tested: {report['body_return_links_tested']}")
    print(f"index_entries: {report['index_entries']}")
    print(f"true_body_cjk_count: {report['true_body_cjk_count']}")
    print(f"file type: {report.get('file_type', 'not built')}")
    print(f"out: {report.get('out', '')}")
    for error in report["errors"]:
        print(f"error: {error}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
