---
name: project-note-json-to-epub
description: Convert structured project-note JSON manuscripts into validated EPUB files. Use when the user asks to turn project notes, book-system JSON, FIRE-indexed notes, Luhmann/Zettelkasten numbered chunks, table-of-contents cards, index cards, cross-linked project notes, or manuscript JSON into an EPUB with chapter directories, keyword index cards, weighted links, bidirectional backlinks, versioned filenames, chapter-splitting plans, and full link testing.
---

# 專案筆記Json變成Epub

Use this skill when a project-note JSON or folder-derived JSON manuscript needs to become an EPUB, especially when the user wants chapter directories, index cards, cross-links, keyword numbering, versioned check editions, Chinese character counts, chapter-splitting plans, or full EPUB link verification.

Chinese trigger phrases include:

- `專案筆記Json變成Epub`
- `目錄索引卡交叉連結`
- `把這章做成EPUB`
- `章節拆書`
- `關鍵字索引卡`
- `雙向連結EPUB`

## Core Workflow

1. Inspect the JSON schema before generating anything.
   - Identify `title`, `sources`, `toc`, `chunks`, `index`, and validation fields if present.
   - Confirm each chunk has a stable code, title, body or source text, EPUB page/anchor, and Chinese character count.
   - If the JSON is missing fields, derive them deterministically and write the enriched JSON first.

2. Normalize the book identity.
   - Use the user-provided book name exactly.
   - For check editions, name versions as: `{書名} 檢查版 YYYY-MM-DD NN`.
   - Use an ASCII-safe or underscore filename when needed: `{書名}_檢查版_YYYY-MM-DD_NN.epub`.
   - Keep a simple `download.epub` copy for mobile sharing if the user needs an easy download link.

3. Build the table of contents from project-note numbers.
   - Preserve Luhmann/Zettelkasten-style codes such as `1.1`, `3.3.c3b`, and `3.3.d.1`.
   - Split into no more than five display levels: 部、章、節、項、目.
   - Prefer original titles; generate compact titles only for unnamed chunks.
   - Mark Chinese character counts at each level where possible.
   - Treat the TOC as a directory card: every entry should preserve code, title, depth, page anchor, and future split-book key.

4. Build the keyword index before EPUB rendering.
   - Each keyword must have a stable id: `K001`, `K002`, ...
   - Sort by descending weight, then keyword for deterministic order.
   - Remove keywords below the requested threshold. If unspecified, ask or use the current project threshold.
   - Each keyword may link to at most 5 target pages/chunks.
   - Each index link needs display text, target, anchor, chunk code, title, and weight.
   - Treat every keyword entry as an index card with id, keyword, weight, chapter attributes, selected page links, and cross-link metadata.

5. Add bidirectional link data.
   - Forward link: index keyword page number ->正文 chunk anchor.
   - Backlink:正文 keyword marker -> index keyword anchor.
   - Use the keyword id as backlink display text, such as `K001`.
   - Store backlinks in JSON on the chunk, for example `keyword_backlinks`.
   - Preserve cross-link attributes on each link: chapter key, section key, item key, selected page order, base weight, remote bonus, adjusted weight, and selection rank.

6. Prepare chapter splitting data.
   - Add a `book_split_plan` to JSON when the project is likely to become multiple chapter books.
   - Each split entry should include split key, title, first/last code, first/last page, chunk count, CJK count, and output filename hint.
   - Keep this data orthogonal to the EPUB render so chapters can later be exported independently.

7. Render EPUB paths relative to the XHTML file that contains the link.
   - From `Text/index.xhtml` to正文 parts, use `part2.xhtml#p099`, not `Text/part2.xhtml#p099`.
   - From `Text/part*.xhtml` back to the index, use `index.xhtml#idx-k001`, not `../Text/index.xhtml#idx-k001`.
   - Keep canonical JSON targets if useful, but convert hrefs correctly during XHTML rendering.
   - Put the keyword index card at the end of the book spine as book back matter: directory/intro first,正文 chunks next, `index.xhtml` last. This matches normal human book structure where an index appears after the main text.

8. Validate before delivery.
   - Open the EPUB zip and parse every XHTML file as XML.
   - Collect all `id` anchors and all `href` links.
   - Resolve every href relative to its source XHTML path.
   - Fail the build if any target file or anchor is missing.
   - Count expected forward links from `index[].links`.
   - Count expected backlinks from `chunks[].keyword_backlinks`.
   - Confirm actual EPUB forward/backlink counts match expected counts.
   - Recalculate `true_body_cjk_count` from正文 body/chunk text only, excluding TOC, index cards, navigation files, metadata, CSS, generated link labels, and markup.
   - Report the true body count separately from total EPUB or generated XHTML text counts.
   - Confirm `orthogonal_check.ok` is true when the JSON includes directory/index/cross-link fields.

## EPUB Requirements

- EPUB mimetype must be the first zip entry and stored uncompressed.
- `META-INF/container.xml`, `OEBPS/content.opf`, `OEBPS/nav.xhtml`, and XHTML text files must exist.
- `dc:title` in `content.opf` must match the requested book/version title.
- The書末索引 must show keyword id, keyword, weight, and clickable page links.
- The OPF spine must place the keyword index page after all正文 pages unless the user explicitly requests a front-loaded index for review.
-正文 keyword markers should show the keyword plus a small clickable `Kxxx` backlink.
- Preserve readable styling; backlinks should not disrupt paragraph flow.

## Validation Checklist

Before telling the user it is finished, report:

```text
errors: 0
title: ...
all_href_count: ...
index_forward_links_tested: ...
body_return_links_tested: ...
index_entries: ...
true_body_cjk_count: ...
file type: EPUB document
```

If any count fails, fix the generator and rebuild rather than editing EPUB output by hand.

## Delivery

Return two links when possible:

- A simple mobile-safe link: `download.epub`
- The formal versioned EPUB filename

Mention the version title and the link-test summary briefly.
