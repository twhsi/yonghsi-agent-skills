#!/usr/bin/env python3
import html
import json
import posixpath
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WORK = ROOT / "assets" / "_epub_work"
EPUB_NAME = "自動魯曼編號機_使用手冊_公開版_2026-06-17_03.epub"
EPUB_PATH = ASSETS / EPUB_NAME
DOWNLOAD = ASSETS / "download.epub"
TITLE = "自動魯曼編號機 使用手冊 公開版 2026-06-17 03"
AUTHOR = "永錫與 Codex"


CHAPTERS = [
    {
        "code": "0.1",
        "title": "FIRE 知識卡：為什麼需要自動魯曼編號機",
        "body": "自動魯曼編號機的任務，是讓書稿地址、魯曼分支、Mandala section 與 EPUB 索引各守其位。公開版用 FAST 日計劃作為小案例，示範如何保留舊碼、補上新卡，並在發布前清理私人 catalog。",
        "fire": {
            "Fact 事實": ["定義：穩定卡號", "主張：章節生長", "證據：缺號錯碼"],
            "Index 索引": ["重新入口", "魯曼編號", "EPUB 目錄"],
            "Relation 關係": ["關係網絡", "章節定址", "錯碼校正"],
            "Encyclopedia 百科": ["概念：書稿地址", "用途：卡片入書", "判斷：保留舊碼"]
        },
        "center": "◎ 編號機：書稿成骨，卡片補枝，索引分離"
    },
    {
        "code": "1.1",
        "title": "核心規則",
        "body": "自動魯曼編號機把書稿章節當成主題地址。純數字最多五級，分別是部、章、節、項、目。英文字母代表魯曼分支或 Mandala container。K001 這類代碼只屬於關鍵字索引，不放進章節層級。這樣一來，書稿可以進 EPUB，卡片仍能保留插入與旁枝能力。"
    },
    {
        "code": "1.2",
        "title": "掃描資料夾",
        "body": "使用時可以說：用 auto-luhmann-numberer 掃描這個 folder，列出所有部、章、節、項、目，並標出缺號與待校正碼。Skill 會建立 catalog，列出正式碼與 off-prefix 碼。off-prefix 不是立刻錯誤，而是待判斷的跨章引用或需要校正的卡號。"
    },
    {
        "code": "1.3",
        "title": "幫新卡片取號",
        "body": "給一張新卡片時，先找最接近的章節 anchor。例如 FAST 日計劃的核心卡可以進入 1.1，補充、旁枝或插入卡可以成為 1.1.a、1.1.b 或 1.1.E。若要插入既有兩張卡中間，不重編舊卡，而是用字母或英數 suffix。"
    },
    {
        "code": "1.4",
        "title": "Mandala Section",
        "body": "若 Markdown 檔案有 mandala: true 或 <!--section: 1.7--> 這種標記，section 只在該檔內有效。顯示時可寫成 1.1.E｜1.7，意思是 1.1.E 這個分支檔案中的第 1.7 格。不要把它誤認為全書的 1.7 章。"
    },
    {
        "code": "1.5",
        "title": "轉成 EPUB 前的檢查",
        "body": "EPUB 需要穩定 toc、chunks、anchors 與 keyword index。輸出前要檢查 duplicate code、缺號、off-prefix、五級深度上限與 K### 索引分離。公開發布前還要檢查 catalog 是否含完整書稿結構、絕對路徑或私人章節標題。"
    },
    {
        "code": "1.6",
        "title": "常用指令",
        "body": "常用 prompt：用 auto-luhmann-numberer 掃描這個資料夾，列出所有卡片編號，分成部、章、節、項、目，並標出缺號和待校正碼。另一個 prompt：用 auto-luhmann-numberer 幫這張卡片找位置，依照目前書稿章節和魯曼分支規則給它一個編號。"
    },
    {
        "code": "1.7",
        "title": "公開案例：FAST 日計劃",
        "body": "公開版只保留 1.1 FAST 日計劃作為示例：1 是部，1.1 是章，1.1.1 到 1.1.4 是節，1.1.E 是魯曼分支，1.1.E｜1.7 是 Mandala container 的局部 section。完整書稿 catalog 不放入公開 repo。"
    },
    {
        "code": "1.8",
        "title": "GitHub Skill 包",
        "body": "公開 Skill repo 應包含 SKILL.md、agents/openai.yaml、references、scripts 與 assets。電子書可放在 assets 內，作為教學附件。公開前要用搜尋檢查私人路徑、完整 catalog 與舊 EPUB 是否殘留。"
    },
]


def cjk_count(text: str) -> int:
    return len(re.findall(r"[\u3400-\u9fff]", text))


def chapter_plain_text(chapter):
    parts = [chapter.get("body", ""), chapter.get("center", "")]
    for values in chapter.get("fire", {}).values():
        parts.extend(values)
    return "\n".join(parts)


def render_body(chapter):
    paras = "".join(f"<p>{html.escape(p)}</p>" for p in chapter["body"].split("\n\n") if p.strip())
    if "fire" not in chapter:
        return paras
    fire_items = []
    for heading, values in chapter["fire"].items():
        lis = "".join(f"<li>{html.escape(value)}</li>" for value in values)
        fire_items.append(
            f'<section class="fire-section"><h2>{html.escape(heading)}</h2><ul>{lis}</ul></section>'
        )
    return (
        f'{paras}<p class="fire-center">{html.escape(chapter["center"])}</p>'
        f'<section class="fire-card">{"".join(fire_items)}</section>'
    )


def xhtml_page(chapter, index, total):
    prev_link = f"part{index - 1:03d}.xhtml" if index > 1 else "toc.xhtml"
    next_link = f"part{index + 1:03d}.xhtml" if index < total else "index.xhtml"
    body = render_body(chapter)
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-Hant">
<head><title>{html.escape(chapter["code"])} {html.escape(chapter["title"])}</title><link rel="stylesheet" href="../Styles/style.css" type="text/css"/></head>
<body>
<section id="p{index:03d}">
<p class="code">{html.escape(chapter["code"])}</p>
<h1>{html.escape(chapter["title"])}</h1>
{body}
<nav class="pager"><a href="{prev_link}">上一頁</a><a href="toc.xhtml">目錄</a><a href="{next_link}">下一頁</a></nav>
</section>
</body>
</html>'''


def write_epub():
    if WORK.exists():
        shutil.rmtree(WORK)
    (WORK / "META-INF").mkdir(parents=True)
    (WORK / "OEBPS" / "Text").mkdir(parents=True)
    (WORK / "OEBPS" / "Styles").mkdir(parents=True)

    (WORK / "mimetype").write_text("application/epub+zip", encoding="utf-8")
    (WORK / "META-INF" / "container.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>""", encoding="utf-8")
    (WORK / "OEBPS" / "Styles" / "style.css").write_text("""
body { font-family: serif; line-height: 1.75; margin: 1.5em; color: #1f2933; }
h1 { font-size: 1.4em; border-bottom: 1px solid #c9d2dc; padding-bottom: .25em; }
h2 { font-size: 1.05em; margin: 0 0 .35em; }
.code { color: #586474; font-family: monospace; }
.pager { display: flex; gap: 1em; margin-top: 2em; border-top: 1px solid #d7dee7; padding-top: 1em; }
.fire-center { font-weight: 700; border-left: .25em solid #8091a5; padding-left: .75em; }
.fire-card { margin: 1em 0; }
.fire-section { border-top: 1px solid #d7dee7; padding: .75em 0; page-break-inside: avoid; }
.fire-section ul { margin: 0; padding-left: 1.2em; }
""", encoding="utf-8")

    toc_items = []
    nav_items = []
    spine_items = []
    manifest_items = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="toc" href="Text/toc.xhtml" media-type="application/xhtml+xml"/>',
        '<item id="idx" href="Text/index.xhtml" media-type="application/xhtml+xml"/>',
        '<item id="css" href="Styles/style.css" media-type="text/css"/>',
    ]
    spine_items.append('<itemref idref="toc"/>')

    for i, chapter in enumerate(CHAPTERS, start=1):
        filename = f"part{i:03d}.xhtml"
        (WORK / "OEBPS" / "Text" / filename).write_text(xhtml_page(chapter, i, len(CHAPTERS)), encoding="utf-8")
        manifest_items.append(f'<item id="p{i:03d}" href="Text/{filename}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="p{i:03d}"/>')
        toc_items.append(f'<li><a href="{filename}#p{i:03d}">{html.escape(chapter["code"])} {html.escape(chapter["title"])}</a></li>')
        nav_items.append(f'<li><a href="Text/{filename}#p{i:03d}">{html.escape(chapter["code"])} {html.escape(chapter["title"])}</a></li>')

    index_links = [
        ("K001", "魯曼編號", "part002.xhtml#p002"),
        ("K002", "Mandala Section", "part004.xhtml#p004"),
        ("K003", "EPUB 檢查", "part005.xhtml#p005"),
        ("K004", "GitHub Skill", "part008.xhtml#p008"),
    ]
    index_rows = "".join(
        f'<tr id="idx-{kid.lower()}"><td>{kid}</td><td>{html.escape(keyword)}</td><td><a href="{href}">前往</a></td></tr>'
        for kid, keyword, href in index_links
    )
    (WORK / "OEBPS" / "Text" / "index.xhtml").write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-Hant">
<head><title>關鍵字索引</title><link rel="stylesheet" href="../Styles/style.css" type="text/css"/></head>
<body><section id="index"><h1>關鍵字索引</h1><table><tbody>{index_rows}</tbody></table><p><a href="toc.xhtml">回目錄</a></p></section></body></html>''', encoding="utf-8")
    spine_items.append('<itemref idref="idx"/>')

    toc_html = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-Hant">
<head><title>{html.escape(TITLE)}</title><link rel="stylesheet" href="../Styles/style.css" type="text/css"/></head>
<body><nav id="toc"><h1>{html.escape(TITLE)}</h1><ol>{''.join(toc_items)}<li><a href="index.xhtml#index">關鍵字索引</a></li></ol></nav></body></html>'''
    (WORK / "OEBPS" / "Text" / "toc.xhtml").write_text(toc_html, encoding="utf-8")
    nav_html = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-Hant">
<head><title>{html.escape(TITLE)}</title></head>
<body><nav epub:type="toc" xmlns:epub="http://www.idpf.org/2007/ops"><h1>目錄</h1><ol>{''.join(nav_items)}<li><a href="Text/index.xhtml#index">關鍵字索引</a></li></ol></nav></body></html>'''
    (WORK / "OEBPS" / "nav.xhtml").write_text(nav_html, encoding="utf-8")

    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">urn:auto-luhmann-numberer-guide-2026-06-17-03</dc:identifier>
<dc:title>{html.escape(TITLE)}</dc:title>
<dc:language>zh-Hant</dc:language>
<dc:creator>{html.escape(AUTHOR)}</dc:creator>
</metadata>
<manifest>{''.join(manifest_items)}</manifest>
<spine>{''.join(spine_items)}</spine>
</package>'''
    (WORK / "OEBPS" / "content.opf").write_text(opf, encoding="utf-8")

    if EPUB_PATH.exists():
        EPUB_PATH.unlink()
    with zipfile.ZipFile(EPUB_PATH, "w") as zf:
        zf.write(WORK / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for file in sorted(WORK.rglob("*")):
            if file.is_file() and file.name != "mimetype":
                zf.write(file, file.relative_to(WORK), compress_type=zipfile.ZIP_DEFLATED)
    shutil.copyfile(EPUB_PATH, DOWNLOAD)


def validate_epub():
    errors = []
    hrefs = []
    ids_by_file = {}
    files = set()
    with zipfile.ZipFile(EPUB_PATH) as zf:
        names = zf.namelist()
        if names[0] != "mimetype":
            errors.append("mimetype is not first")
        files = set(names)
        for name in names:
            if name.endswith(".xhtml"):
                root = ET.fromstring(zf.read(name))
                ids_by_file[name] = {el.attrib["id"] for el in root.iter() if "id" in el.attrib}
                for el in root.iter():
                    href = el.attrib.get("href")
                    if href and not href.startswith("http"):
                        hrefs.append((name, href))
    for src, href in hrefs:
        base = Path(src).parent
        target, _, anchor = href.partition("#")
        target_path = str((base / target).as_posix()) if target else src
        normalized = posixpath.normpath(target_path)
        if normalized not in files:
            errors.append(f"missing file: {src} -> {href}")
            continue
        if anchor and anchor not in ids_by_file.get(normalized, set()):
            errors.append(f"missing anchor: {src} -> {href}")
    true_body_cjk_count = sum(cjk_count(chapter_plain_text(ch)) for ch in CHAPTERS)
    report = {
        "errors": errors,
        "title": TITLE,
        "all_href_count": len(hrefs),
        "index_forward_links_tested": 4,
        "body_return_links_tested": len(CHAPTERS),
        "index_entries": 4,
        "true_body_cjk_count": true_body_cjk_count,
        "file_type": "EPUB document",
        "epub": str(EPUB_PATH.relative_to(ROOT)),
        "download": str(DOWNLOAD.relative_to(ROOT)),
    }
    (ASSETS / "epub-validation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    write_epub()
    report = validate_epub()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not report["errors"] else 1)
