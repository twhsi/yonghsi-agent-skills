#!/usr/bin/env python3
"""Convert an EPUB card book into an Obsidian HyperCard Markdown folder."""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


XHTML_NS = "{http://www.w3.org/1999/xhtml}"
CONTAINER_NS = "{urn:oasis:names:tc:opendocument:xmlns:container}"
OPF_NS = "{http://www.idpf.org/2007/opf}"


@dataclass
class Card:
    code: str
    title: str
    body: list[str]
    keywords: list[str]
    source: str
    char_count: str = ""
    filename: str = ""


@dataclass
class Keyword:
    kid: str
    keyword: str
    weight: str
    targets: list[str] = field(default_factory=list)
    filename: str = ""


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def class_tokens(el: ET.Element) -> set[str]:
    return set((el.attrib.get("class") or "").split())


def text_content(el: ET.Element) -> str:
    text = "".join(el.itertext())
    return re.sub(r"\s+", " ", text).strip()


def visible_text_content(el: ET.Element, skip_classes: set[str] | None = None) -> str:
    skip_classes = skip_classes or {"keyword-backlink", "page", "count"}
    pieces: list[str] = []

    def walk(node: ET.Element) -> None:
        if class_tokens(node) & skip_classes:
            if node.tail:
                pieces.append(node.tail)
            return
        if node.text:
            pieces.append(node.text)
        for child in list(node):
            walk(child)
        if node.tail:
            pieces.append(node.tail)

    walk(el)
    return re.sub(r"\s+", " ", "".join(pieces)).strip()


def markdown_escape_cell(text: str) -> str:
    return escape_pipes(text).strip()


def escape_pipes(text: str) -> str:
    return text.replace("|", r"\|")


def markdown_link(label: str, target: str) -> str:
    return f"[{markdown_escape_cell(label)}]({target})"


def chunked(items: list[str], size: int) -> Iterable[list[str]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]


def table_row(cells: list[str], width: int) -> str:
    padded = cells[:width] + [""] * max(0, width - len(cells))
    return "| " + " | ".join(padded) + " |"


def safe_ascii_code(code: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9]+", "-", code.strip()).strip("-").lower()
    return clean or "card"


def safe_utf8_name(text: str) -> str:
    clean = re.sub(r"[\\/:*?\"<>|#]+", "", text.strip())
    clean = re.sub(r"\s+", "", clean)
    return clean or "card"


def parse_epub(epub_path: Path) -> tuple[str, list[Card], list[Keyword], dict[str, str]]:
    with zipfile.ZipFile(epub_path) as zf:
        container = ET.fromstring(zf.read("META-INF/container.xml"))
        rootfile = container.find(f".//{CONTAINER_NS}rootfile")
        if rootfile is None:
            raise ValueError("EPUB missing rootfile in META-INF/container.xml")
        opf_path = rootfile.attrib["full-path"]
        opf_dir = posixpath.dirname(opf_path)
        opf_root = ET.fromstring(zf.read(opf_path))
        title_el = opf_root.find(".//{http://purl.org/dc/elements/1.1/}title")
        book_title = text_content(title_el) if title_el is not None else epub_path.stem

        manifest = {}
        for item in opf_root.findall(f".//{OPF_NS}manifest/{OPF_NS}item"):
            manifest[item.attrib["id"]] = item.attrib["href"]

        spine_paths = []
        for itemref in opf_root.findall(f".//{OPF_NS}spine/{OPF_NS}itemref"):
            href = manifest.get(itemref.attrib["idref"])
            if href:
                spine_paths.append(posixpath.normpath(posixpath.join(opf_dir, href)))

        cards: list[Card] = []
        keywords: list[Keyword] = []
        directory_meta: dict[str, str] = {}

        for path in spine_paths:
            try:
                root = ET.fromstring(zf.read(path))
            except KeyError:
                continue

            if is_index_page(root):
                keywords = parse_keywords(root)
                continue

            card_containers = find_card_containers(root)
            if card_containers:
                for card_container in card_containers:
                    cards.append(parse_card(card_container, path))
                continue

            page_meta = parse_directory_meta(root)
            if page_meta and (not directory_meta or is_directory_page(root)):
                directory_meta = page_meta

        return book_title, cards, keywords, directory_meta


def find_first(root: ET.Element, name: str) -> ET.Element | None:
    for el in root.iter():
        if local_name(el.tag) == name:
            return el
    return None


def children_named(el: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in list(el) if local_name(child.tag) == name]


def find_card_containers(root: ET.Element) -> list[ET.Element]:
    articles = [el for el in root.iter() if local_name(el.tag) == "article"]
    if articles:
        return articles
    return [
        el
        for el in root.iter()
        if local_name(el.tag) == "section" and {"chunk", "card"} & class_tokens(el)
    ]


def is_index_page(root: ET.Element) -> bool:
    for el in root.iter():
        if {"index-card", "index-list"} & class_tokens(el):
            return True
    h1 = find_first(root, "h1")
    return h1 is not None and "索引" in text_content(h1)


def is_directory_page(root: ET.Element) -> bool:
    for el in root.iter():
        if "directory-card" in class_tokens(el):
            return True
    return False


def parse_card(article: ET.Element, source: str) -> Card:
    heading = find_first(article, "h1")
    if heading is None:
        heading = find_first(article, "h2")
    heading_text = visible_text_content(heading) if heading is not None else Path(source).stem
    title = heading_text

    code = ""
    char_count = ""
    body: list[str] = []
    keywords: list[str] = []

    if heading is not None:
        for child in heading.iter():
            if local_name(child.tag) == "span" and "count" in class_tokens(child):
                count_match = re.search(r"(\d+)", text_content(child))
                if count_match:
                    char_count = count_match.group(1)
        title = re.sub(r"\s*P\d+\s*$", "", title)
        title = re.sub(r"\s*中文字數\s*\d+\s*$", "", title)
        title_match = re.match(r"(\d+(?:\.\d+)*)\s+(.+)$", title)
        if title_match:
            code, title = title_match.groups()
            title = title.strip()

    for child in article.iter():
        if local_name(child.tag) == "p" and "code" in class_tokens(child):
            code_text = text_content(child)
            match = re.match(r"(.+?)(?:[｜|](.+))?$", code_text)
            if match:
                code = match.group(1).strip()
                char_count = (match.group(2) or "").replace("字", "").strip()
        elif local_name(child.tag) == "span" and {"keyword-marker", "indexed-keyword"} & class_tokens(child):
            keyword = visible_text_content(child).strip()
            if keyword and keyword not in keywords:
                keywords.append(keyword)

    for child in children_named(article, "p"):
        if not ({"code", "backlink-strip"} & class_tokens(child)):
            text = visible_text_content(child)
            if text:
                body.append(text)

    if not code:
        code = title

    return Card(code=code, title=title, body=body, keywords=keywords, source=source, char_count=char_count)


def parse_keywords(root: ET.Element) -> list[Keyword]:
    keywords: list[Keyword] = []
    for section in root.iter():
        if local_name(section.tag) != "section" or "index-card" not in class_tokens(section):
            continue
        h2 = find_first(section, "h2")
        heading = text_content(h2) if h2 is not None else ""
        match = re.match(r"(K\d+)\s+(.+?)(?:\s+權重\s+(\d+))?$", heading)
        if not match:
            continue
        kid, keyword, weight = match.groups()
        targets = []
        for link in section.iter():
            if local_name(link.tag) == "a":
                label = text_content(link)
                if label:
                    targets.append(label)
        keywords.append(Keyword(kid=kid, keyword=keyword.strip(), weight=weight or "", targets=targets))
    if keywords:
        return keywords

    for dl in root.iter():
        if local_name(dl.tag) != "dl" or "index-list" not in class_tokens(dl):
            continue
        current: Keyword | None = None
        for child in list(dl):
            if local_name(child.tag) == "dt":
                heading = text_content(child)
                match = re.match(r"(K\d+)\s+(.+?)(?:\s+權重\s+(\d+))?$", heading)
                if not match:
                    current = None
                    continue
                kid, keyword, weight = match.groups()
                current = Keyword(kid=kid, keyword=keyword.strip(), weight=weight or "")
                keywords.append(current)
            elif local_name(child.tag) == "dd" and current is not None:
                for link in child.iter():
                    if local_name(link.tag) == "a":
                        label = text_content(link)
                        if label:
                            current.targets.append(label)
    return keywords


def parse_directory_meta(root: ET.Element) -> dict[str, str]:
    meta: dict[str, str] = {}
    paragraph = find_first(root, "p")
    if paragraph is not None:
        meta["summary"] = text_content(paragraph)
    dts: list[str] = []
    dds: list[str] = []
    for el in root.iter():
        if local_name(el.tag) == "dt":
            dts.append(text_content(el))
        elif local_name(el.tag) == "dd":
            dds.append(text_content(el))
    for key, value in zip(dts, dds):
        meta[key] = value
    return meta


def assign_filenames(cards: list[Card], keywords: list[Keyword], portable: bool) -> None:
    used: set[str] = set()
    for card in cards:
        if portable:
            base = f"card-{safe_ascii_code(card.code)}"
        else:
            base = f"{safe_utf8_name(card.code)}-{safe_utf8_name(card.title)}"
        card.filename = unique_name(base, used)

    for keyword in keywords:
        if portable:
            base = f"key-{keyword.kid.lower()}"
        else:
            base = f"{keyword.kid}-{safe_utf8_name(keyword.keyword)}"
        keyword.filename = unique_name(base, used)


def unique_name(base: str, used: set[str]) -> str:
    candidate = f"{base}.md"
    index = 2
    while candidate in used:
        candidate = f"{base}-{index}.md"
        index += 1
    used.add(candidate)
    return candidate


def build_card_lookup(cards: list[Card]) -> dict[str, Card]:
    lookup: dict[str, Card] = {}
    for card in cards:
        lookup[card.code] = card
        lookup[card.title] = card
        lookup[f"{card.code} {card.title}"] = card
    return lookup


def find_card_for_target(target: str, cards: list[Card]) -> Card | None:
    for card in cards:
        if card.code in target or card.title in target:
            return card
    return None


def link_body(text: str, keyword_map: dict[str, Keyword]) -> str:
    pieces: list[str] = []
    keywords = [keyword for keyword in sorted(keyword_map, key=len, reverse=True) if keyword]
    index = 0
    while index < len(text):
        matched = None
        for keyword in keywords:
            if text.startswith(keyword, index):
                matched = keyword
                break
        if matched:
            pieces.append(markdown_link(matched, keyword_map[matched].filename))
            index += len(matched)
        else:
            pieces.append(escape_pipes(text[index]))
            index += 1
    return "".join(pieces)


def write_outputs(book_title: str, cards: list[Card], keywords: list[Keyword], directory_meta: dict[str, str], out_dir: Path) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    keyword_map = {keyword.keyword: keyword for keyword in keywords}

    for index, card in enumerate(cards, start=1):
        previous_card = cards[index - 2] if index > 1 else None
        next_card = cards[index] if index < len(cards) else None
        (out_dir / card.filename).write_text(
            render_card(card, index, len(cards), previous_card, next_card, keyword_map),
            encoding="utf-8",
        )

    for index, keyword in enumerate(keywords, start=1):
        previous_keyword = keywords[index - 2] if index > 1 else None
        next_keyword = keywords[index] if index < len(keywords) else None
        (out_dir / keyword.filename).write_text(
            render_keyword(keyword, index, len(keywords), previous_keyword, next_keyword, cards),
            encoding="utf-8",
        )

    (out_dir / "index.md").write_text(render_index(book_title, cards, keywords, directory_meta), encoding="utf-8")
    (out_dir / "keyword-index.md").write_text(render_keyword_index(keywords), encoding="utf-8")


def render_card(card: Card, index: int, total: int, previous_card: Card | None, next_card: Card | None, keyword_map: dict[str, Keyword]) -> str:
    body = "<br><br>".join(link_body(paragraph, keyword_map) for paragraph in card.body)
    keyword_links = [markdown_link(keyword, keyword_map[keyword].filename) for keyword in card.keywords if keyword in keyword_map]
    if not keyword_links:
        keyword_links = [markdown_link("目錄", "index.md")]

    keyword_rows = ["| 索引 |  |  |  |", "|---|---|---|---|"]
    for row in chunked(keyword_links, 4):
        keyword_rows.append(table_row(row, 4))

    previous_link = markdown_link(previous_card.title, previous_card.filename) if previous_card else markdown_link("目錄", "index.md")
    next_link = markdown_link(next_card.title, next_card.filename) if next_card else markdown_link("關鍵字索引卡", "keyword-index.md")

    return "\n".join(
        [
            f"# {card.code} {card.title}",
            "",
            "| 魯曼編號 | 卡片標題 |",
            "|---|---|",
            f"| `{markdown_escape_cell(card.code)}` | **{markdown_escape_cell(card.title)}** |",
            "",
            "| 內容 |",
            "|---|",
            f"| {body} |",
            "",
            *keyword_rows,
            "",
            f"| ← 上一張 | Card {index} / {total} | 下一張 → |",
            "|---|---|---|",
            f"| {previous_link} | [Home](index.md) | {next_link} |",
            "",
        ]
    )


def render_keyword(keyword: Keyword, index: int, total: int, previous_keyword: Keyword | None, next_keyword: Keyword | None, cards: list[Card]) -> str:
    target_links = []
    for target in keyword.targets:
        card = find_card_for_target(target, cards)
        if card is not None:
            target_links.append(markdown_link(f"{card.code} {card.title}", card.filename))

    rows = ["| 連到卡片 |  |  |  |", "|---|---|---|---|"]
    for row in chunked(target_links, 4):
        rows.append(table_row(row, 4))

    previous_link = markdown_link(previous_keyword.keyword, previous_keyword.filename) if previous_keyword else markdown_link("關鍵字索引", "keyword-index.md")
    next_link = markdown_link(next_keyword.keyword, next_keyword.filename) if next_keyword else markdown_link("關鍵字索引", "keyword-index.md")

    return "\n".join(
        [
            f"# {keyword.kid} {keyword.keyword}",
            "",
            "| 關鍵字 | 權重 |",
            "|---|---|",
            f"| {markdown_escape_cell(keyword.keyword)} | {markdown_escape_cell(keyword.weight)} |",
            "",
            *rows,
            "",
            f"| ← 上一張 | Keyword {index} / {total} | 下一張 → |",
            "|---|---|---|",
            f"| {previous_link} | [Home](index.md) | {next_link} |",
            "",
        ]
    )


def render_index(book_title: str, cards: list[Card], keywords: list[Keyword], directory_meta: dict[str, str]) -> str:
    rows = [
        "# " + markdown_escape_cell(book_title),
        "",
        "| Stack | 說明 |",
        "|---|---|",
        f"| 主題 | {markdown_escape_cell(book_title)} |",
        "| 格式 | 一張卡一個 Markdown 檔 |",
        "| 連結 | Markdown 相對檔案連結 |",
        f"| 正文卡 | {len(cards)} 張 |",
        f"| 關鍵字卡 | {len(keywords)} 張 |",
        "",
        "## 章節目錄",
        "",
        "| Card | 魯曼編號 | 卡片標題 | 字數 |",
        "|---|---|---|---|",
    ]
    for index, card in enumerate(cards, start=1):
        rows.append(
            f"| {markdown_link(f'Card {index}', card.filename)} | `{markdown_escape_cell(card.code)}` | {markdown_escape_cell(card.title)} | {markdown_escape_cell(card.char_count)} |"
        )

    rows.extend(
        [
            f"| {markdown_link('Index', 'keyword-index.md')} | `INDEX` | 關鍵字索引卡 | {len(keywords)} keywords |",
            "",
        ]
    )

    if directory_meta:
        if "summary" in directory_meta:
            rows.extend(["## 摘要", "", "| 中心句 |", "|---|", f"| {markdown_escape_cell(directory_meta['summary'])} |", ""])
        axes = [(key, value) for key, value in directory_meta.items() if key != "summary"]
        if axes:
            rows.extend(["## 正交檢查", "", "| 軸線 | 關鍵詞 |", "|---|---|"])
            for key, value in axes:
                rows.append(f"| {markdown_escape_cell(key)} | {markdown_escape_cell(value)} |")
            rows.append("")

    first_card = markdown_link(cards[0].title, cards[0].filename) if cards else ""
    rows.extend(
        [
            "## 導航",
            "",
            "| 開始閱讀 | 關鍵字索引 |",
            "|---|---|",
            f"| {first_card} | {markdown_link('關鍵字索引卡', 'keyword-index.md')} |",
            "",
        ]
    )
    return "\n".join(rows)


def render_keyword_index(keywords: list[Keyword]) -> str:
    rows = ["# 關鍵字索引卡", "", "| Key | 關鍵字 | 權重 | 關鍵字卡 |", "|---|---|---|---|"]
    for keyword in keywords:
        rows.append(
            f"| {markdown_escape_cell(keyword.kid)} | {markdown_escape_cell(keyword.keyword)} | {markdown_escape_cell(keyword.weight)} | {markdown_link(keyword.kid + ' ' + keyword.keyword, keyword.filename)} |"
        )
    rows.extend(["", "| 返回 |", "|---|", "| [HyperCard 目錄](index.md) |", ""])
    return "\n".join(rows)


def verify_links(out_dir: Path) -> list[str]:
    missing: list[str] = []
    for file_path in out_dir.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if re.match(r"^[a-z]+:", target):
                continue
            if "#" in target:
                target = target.split("#", 1)[0]
            if target and not (out_dir / html.unescape(target)).exists():
                missing.append(f"{file_path.name} -> {target}")
    return missing


def write_zip(out_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(out_dir.rglob("*")):
            zf.write(path, path.relative_to(out_dir.parent))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("epub", type=Path)
    parser.add_argument("--out", type=Path, help="Output folder. Defaults to EPUB stem + '-hypercard-obsidian'.")
    parser.add_argument("--zip", action="store_true", help="Also create OUTPUT_DIR.zip.")
    parser.add_argument("--portable", action="store_true", help="Use ASCII filenames for better zip/GitHub/AI upload portability.")
    args = parser.parse_args()

    if not args.epub.exists():
        print(f"error: EPUB not found: {args.epub}", file=sys.stderr)
        return 2

    out_dir = args.out or Path(f"{args.epub.stem}-hypercard-obsidian")
    book_title, cards, keywords, directory_meta = parse_epub(args.epub)
    if not cards:
        print("error: no <article> cards found in EPUB spine", file=sys.stderr)
        return 1

    assign_filenames(cards, keywords, args.portable)
    write_outputs(book_title, cards, keywords, directory_meta, out_dir)
    missing = verify_links(out_dir)

    zip_path = None
    if args.zip:
        zip_path = Path(f"{out_dir}.zip")
        write_zip(out_dir, zip_path)

    print(f"title: {book_title}")
    print(f"cards: {len(cards)}")
    print(f"keywords: {len(keywords)}")
    print(f"missing_links: {len(missing)}")
    for item in missing:
        print(f"missing: {item}")
    print(f"out_dir: {out_dir}")
    if zip_path:
        print(f"zip: {zip_path}")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
