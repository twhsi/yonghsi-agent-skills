---
name: imandalart
description: Design and render iMandalArt-style square 3x3 index cards for Discord/Hermes. Version 1.0 defaults to five-character no-frame text cards with ◎ center, title/content/breath rows, and deliberate full-width/half-width spacing. Also supports legacy PE2-like fixed-width bordered text boxes and optional HTML visual cards. Use when the user asks for iMandalArt, iMandalart, I MandalArt, 手機方形曼陀羅, 正方形九宮索引卡, 五字定格, 無框九宮, ◎中心, HyperCard-like Mandala cards, PE2-style text UI, paper/doodle nine-grid references, or a square 3x3 card that handles Chinese/Japanese/English mixed text but is not Markdown 九宮格 or an 81-cell Mandala.
---

# iMandalArt

## Purpose

Use this skill to create a square 3x3 index card for Discord/Hermes, not a Markdown table.

iMandalArt 1.0 default: five-character no-frame cards. The grid is formed by measured text, spacing, and center breathing room rather than visible borders.

iMandalArt is the user's third Mandala format:

- Not `markdown-nine-grid-clipboard`: that skill makes copyable short Markdown tables.
- Not `vector-nine-grid`: that skill makes icon-first concept diagrams.
- Not `mandala-81-grid-image`: that skill expands one center into 81 cells.
- iMandalArt is one square card: HyperCard-like, paper-index-card-like, and old mobile-app-like.

The default deliverable should be an iMandalArt 1.0 no-frame fixed-width text card when the user asks for a new card, a 1.0 card, a clean mobile card, or mentions five-character rows, ◎ center, or spacing aesthetics. Use legacy PE2 bordered rendering only when the user asks for PE2, borders, old mobile UI, deterministic script output, or Discord-safe framed text. HTML is optional when the user can open local files.

## Default Deliverable

For iMandalArt 1.0, default to no-frame text art:

1. Create 9 structured cells.
2. Give each cell three rows: title, content, breath.
3. Keep each visible row exactly 5 counted characters.
4. Use `◎` in the center cell and give the center more whitespace than outer cells.
5. Return the code block directly after manually checking that every 1.0 row is five counted characters.

For legacy PE2/Discord-safe framed text:

1. Create 9 structured cells.
2. Render a PE2-like square text card with `scripts/imandalart_card.py discord`.
3. Immediately run the square check with `scripts/imandalart_card.py check-square`.
4. Return the code block directly in Discord/Hermes only after the check passes.

Use HTML only when the user asks for a local visual artifact or screenshot source.

## iMandalArt 1.0 Five-Character No-Frame Mode

Use this 1.0 mode when the user asks for iMandalArt 1.0, no `|`, no borders, five-character fixed rows, title/content separation, full-width and half-width spacing, or the Zhongchi / Zhuge Bagua Village style.

Core rule: the square is not drawn by borders. It emerges from fixed five-character rows, measured spacing, and center breathing room.

- Do not use `|`, `+`, `-`, box drawing, Markdown tables, or visible cell borders.
- Keep every visible row in a cell exactly 5 characters. Count CJK, full-width spaces, half-width spaces, punctuation, numbers, and symbols as one character each for this mode.
- A cell normally has three rows: `TITLE(5)`, `CONTENT(5)`, `BREATH(5)`.
- The title row must have rhythm and spacing, not just packed text.
- The content row should be semantically clear, usually a five-character phrase.
- The breath row is usually five spaces or a sparse two-to-three character line.
- The center cell keeps `◎` as the center mark, but uses more blank space than the outer cells.
- Aim for a near-square visual body by balancing row count, inter-cell gaps, and center whitespace.

Title rhythm patterns:

```text
字 空 字 空 字
二字 全形空 二字
三字 半形空 一字
一字 全形空 二字 半形空
留白 字詞 留白
```

Five-character examples:

```text
諸 葛 村
鐘 池 心
八 卦 局
諸葛　村 
鐘池　心 
　鐘池　 
　 ◎ 　
 鐘　池 
 水　心 
```

Center pattern:

```text
　 ◎ 　
 鐘　池 
 水　心 
```

For Zhongchi / Zhuge Bagua Village cards, treat `◎` as the quiet water-center, `鐘池` as the name, `水心` as the symbol, and the surrounding eight cells as the village's spatial ring.

Example 1.0 card:

```text
浙 江 蘭　　諸 葛 脈　　九 宮 局
蘭溪諸葛鎮　　後裔聚居地　　八卦村落形
地理入村線　　史脈入村中　　格局先行法

太 極 水　　 ◎ 　　八 巷 出
鐘池如太極　　 鐘　池 　　小巷向外放
水面作中心　　 水　心 　　路徑成放射

外 山 環　　考 據 線　　語 法 一
八山成外卦　　傳說分層記　　五字定格法
村外成邊界　　不混作事實　　正式版語法
```

1.0 grammar sketch for future jison work:

```text
TITLE   = FIVE_CHAR_RHYTHM
BODY    = FIVE_CHAR_PHRASE
BREATH  = FIVE_CHAR_SPACE
CELL    = TITLE BODY BREATH
CENTER  = CENTER_BREATH CENTER_MARK CENTER_NAME
GRID    = ROW ROW ROW
ROW     = CELL GAP CELL GAP CELL
```

Design gate for 1.0:

- No visible borders.
- Each cell row is exactly five counted characters.
- Outer titles show spacing rhythm.
- Center contains `◎`.
- Center has more whitespace than the outer cells.
- The whole card feels close to square and visually calm.

## Card Modes

Choose the visual mood from the user context:

| Mode | Visual analogy | Use when |
|---|---|---|
| `classic` | old iMandalArt/iPhone square app | mobile UI, specs, concise notes |
| `hypercard` | HyperCard/BPDA index card | Hermes, card-box, retro software, linked notes |
| `paper` | printed/drawn Mandal-Art sheet | paper reference, handwritten planning, doodle inbox |
| `pe2` | fixed-width text UI | Discord, no-HTML environments, terminal-style cards |

If unspecified, use `pe2` for Discord/Hermes and `hypercard` for local HTML previews.

## Workflow

1. Identify the card title: one short phrase above the square.
2. Identify the center cell: the whole card's concept, conclusion, or controlling question.
3. Compress the center into a Palm-style launcher label when possible, usually `⭕` plus 3 Chinese characters.
4. Extract eight surrounding cells as index-card fragments, not table labels.
5. Keep each cell visually scannable: one title-like line plus optional supporting words.
6. Arrange cells in a square 3x3 layout.
7. Render the card as a fixed-width PE2 text block. Use HTML only as an optional secondary artifact.
8. Return the code block first.

## PE2 Text Grid Rules

The PE2 renderer builds one big square from nine small card-like cells.

- Use monospaced code blocks in Discord.
- Count display width, not character count.
- CJK full-width characters count as 2 columns.
- English letters, digits, and ASCII punctuation count as 1 column.
- Wrap English words as units when possible; wrap CJK by character.
- If one English token exceeds the cell width, abbreviate it with `..` instead of splitting letters across lines.
- Pad each line with spaces until it reaches the exact cell width.
- Treat spaces as visual language: they are the Palm card's breathing room and right-side padding, not accidental leftover text.
- Give every cell the same width and height.
- Render each cell as its own mini-card with one-column gutters between cells.
- Default to left/top text alignment for handwritten card feeling.
- Highlight the center card with heavier `=` borders and a leading `⭕`.
- Do not use Discord ANSI color; use pure text only.
- Surrounding cells should read like titles: compact Chinese headings first, details only if there is room.
- In compact mobile output, do not insert spaces between Chinese characters.
- In `mobile-human` output, deliberate visual spaces between CJK characters are allowed when they improve phone reading rhythm.
- In the default mobile preset, one Chinese line is fixed at 4 characters (`8 display columns`).
- Default mobile preset: `8 columns x 3 rows` per cell.
- Default human-eye mobile preset: `mobile-human`, `8 columns x 3 rows` per cell, two visible lines plus one blank breathing row.
- Default total grid width: `32 columns`, designed to survive Discord phone message bubbles without wrapping.
- The title is rendered as a separate title line above the square content grid, defaulting to `[ 標題 ]`.
- The content grid itself is approximately square on mobile monospace fonts: `32 columns x 17 text rows`.
- After rendering, immediately check that the 3x3 content grid is visually square.
- Use `--cell-width` and `--cell-height` when text is too dense.

## Cell Capacity

Before writing cell text, calculate capacity:

- One CJK character occupies 2 display columns.
- One ASCII character occupies 1 display column.
- `cjk_per_line = cell_width // 2`
- `ascii_per_line = cell_width`
- `cell_height = round(cell_width / 2)` unless explicitly set.
- `cjk_total = cjk_per_line * cell_height`
- `ascii_total = ascii_per_line * cell_height`

Default `mobile` preset:

```text
cell_width=8
cell_height=3
cjk_per_line=4
ascii_per_line=8
cjk_total=12
ascii_total=24
```

If text is shorter than the cell capacity, pad with spaces until each rendered line reaches exactly `cell_width` display columns. Do not rely on Markdown table alignment.

Use `mobile-air` only for screenshots or wider surfaces after checking that Discord phone wrapping will not occur:

```text
cell_width=10
cell_height=4
cjk_per_line=5
ascii_per_line=10
```

Use `mobile-human` as the preferred Discord phone preset when the goal is a screenshot-like, collectible learning card:

```text
cell_width=8
cell_height=3
style=human-eye
preferred_line_width=4-6 display columns
preferred_trailing_padding=2-4 spaces
```

For `mobile-human`, each outer cell should normally use exactly two visible lines:

- First line: 2-3 CJK title characters, with right-side padding visible, e.g. `句型熱  `.
- Second line: 2-3 CJK context characters, with right-side padding visible, e.g. `抓骨架  `.
- Third line: blank breathing row.
- Center line: keep to `⭕` plus 3-4 compact CJK characters where possible; do not let the emoji consume the whole cell.
- Avoid 4 CJK characters in an 8-column mobile cell unless the meaning would break; it leaves no right-side breathing room.
- Avoid CJK internal spaces in `mobile-human` when they consume the right-side padding, e.g. prefer `句型熱  ` over `句 型 熱`.
- Move explanations longer than 5 visible characters per line to a short table or notes below the grid.

## Plain Text Hierarchy

Do not use Discord color control. Use pure text hierarchy:

- Title line: `[ 標題 ]` above the nine-grid. Use `--title-style box` only when the user wants a stronger PE2 frame.
- Center card: heavier `=` border plus leading `⭕`.
- Surrounding cards: compact title-like Chinese headings, left/top aligned.
- Avoid decorative color or ANSI escapes because Discord mobile rendering is inconsistent.
- Prefer Chinese titles over English when meaning is equivalent.
- In compact mode, keep Chinese continuous: write `今日工作` not `今日 工作`.
- In `mobile-human`, prioritize right-side breathing room. Deliberate CJK internal spacing is allowed only when it does not remove the right-side padding.

## Alignment Rules

Spaces are part of the design. Every visible row must be assembled from measured cells, not typed by hand:

- Every `+` and `|` column must line up with the matching card edge above and below.
- Every cell content line must be padded with spaces to exactly `cell_width` display columns.
- Gutter spaces between cards must be fixed-width and identical on every row.
- The title line must have the same display width as the nine-card body.
- Never manually add random extra spaces after Chinese text; let the renderer add padding after measuring display width.
- Use short labels so the generated padding becomes visible margin. Example: `輸入源` is better than `輸入來源` in the default 4-Chinese-character cell.
- For `mobile-human`, spaces may be intentional content inside a label, but right-side padding is preferred over internal CJK spacing. Spaces must still be measured by display width and generated by the renderer, not hand-patched after rendering.
- Padding formula: `trailing_spaces = cell_width - display_width(label)`.
- In default mobile mode, `觸發語` is 6 display columns, so it receives 2 trailing spaces inside an 8-column cell: `|觸發語  |`.
- In default mobile mode, `水墨輸出` is 8 display columns, so it receives 0 trailing spaces inside an 8-column cell: `|水墨輸出|`.
- If a hand-edited card breaks alignment, re-render it instead of patching individual spaces.

## Palm / Rob Haitani Rules

Think like a Palm OS launcher designer:

- A cell is a tappable card label, not a paragraph.
- Prefer one glanceable Chinese label per cell.
- Phone fit beats air. Use the empty area inside each cell as affordance only after the whole 3x3 body fits the phone width.
- The center is the Home button of the card. Default center shape is `⭕塗鴉匣`, `⭕主題核`, or another `⭕` plus 3-character Chinese label.
- Never render the center as `⭕` alone when a center label is known. `⭕` is a prefix, not a replacement for the center text.
- Avoid English in the default mobile render when a compact Chinese equivalent exists.
- The 3x3 body must feel like one square object made from nine smaller square cards.

## PALM Design Gate

Before delivering a Discord/Hermes card, check it against PALM:

- `P` Phone first: the 3x3 body must be at most `32 display columns`; if it wraps in Discord mobile, it fails.
- `A` At-a-glance: each cell starts with a short label, ideally 2-4 Chinese characters.
- `L` Locked layout: all `+` and `|` edges align because the renderer, not hand spacing, builds them.
- `M` Measured margin: spaces are calculated by `cell_width - display_width(label)` and appear only after content or between mini-cards.

## Human-Eye Mobile Gate

Use this gate for `mobile-human` and for learning cards meant to be screenshotted on Discord mobile:

- Every cell must have at least one visible non-empty line.
- Outer cells should have two visible lines: title first, context second.
- A default `8 x 3` cell should keep at least one blank breathing row.
- First and second line should not be visually lopsided; avoid pairing a full-width line with a tiny fragment.
- Outer cell lines should usually occupy 4-6 display columns, leaving 2-4 trailing spaces in an 8-column cell.
- Warn or rewrite when an outer line occupies all 8 display columns; it has no right-side breathing room.
- The center cell should usually be 3-4 CJK characters after `⭕`; if longer, shorten the label and move detail below.
- Deliberate spaces count as visible design, but internal CJK spaces should not steal the right-side breathing room.
- If a concept needs more than two 5-character visual lines, keep the grid terse and place detail below the nine-grid.

## Square Check

After every PE2 render, run the square check before replying.

The checker verifies:

- The main 3x3 grid has exactly 6 card border rows.
- Every rendered line has the same display width.
- The row count matches `3 * (cell_height + 2) + 2 * gutter_rows`.
- The content row count matches `3 * cell_height`.
- The center cell includes both `⭕` and the center label, such as `⭕塗鴉匣`.
- The estimated mobile monospace visual ratio is `0.85-1.15`.

Default mobile preset:

```text
cell_width=8
cell_height=3
display_columns=32
text_rows=17
body_ratio≈0.94
cell_ratio=1.0
```

## Text Density

Use these defaults unless the user specifies another density:

| Density | Center | Surrounding cells | Visual target |
|---|---:|---:|---|
| `label` | 3-18 CJK chars | 2-16 CJK chars | paper/HyperCard index labels |
| `micro` | 6-16 CJK chars | 8-24 CJK chars | old phone screenshot |
| `standard` | 8-28 CJK chars | 16-44 CJK chars | Hermes/Discord card |
| `dense` | 12-44 CJK chars | 28-72 CJK chars | specs, comparisons, lecture notes |

Rules:

- A cell may contain more text than a Markdown 九宮格, but it must still look like a cell on a square card.
- Prefer line breaks and compact clauses over long prose.
- Keep center visually distinct, often shorter and bolder.
- For paper mode, tolerate slightly rougher, handwritten-style phrasing.
- For HyperCard mode, write like clickable card fields: direct, noun-first, navigable.

## Layout Semantics

Use this 3x3 order:

```text
------------+------------+------------+
| trigger   | input      | recognition|
+------------+------------+------------+
| output    | center     | workflow   |
+------------+------------+------------+
| save      | avoid      | next skill |
+------------+------------+------------+
```

That example matches the user's paper reference:

```text
八大面向
| 觸發語 | 輸入源 | 構圖辨識 |
| 水墨輸出 | 塗鴉匣 | 工作流程 |
| 保存筆記 | 不要做 | 下一技能 |
```

For other topics, keep the same logic:

- Top row: entry points, source material, recognition.
- Middle-left: output or visible result.
- Center: the index card's hub.
- Middle-right: workflow or method.
- Bottom row: storage, constraints, next step.

## Renderer

Use `scripts/imandalart_card.py` for deterministic visual output.

Input JSON:

```json
{
  "title": "八大面向",
  "top_left": "觸發語",
  "top_center": "輸入源",
  "top_right": "構圖辨識",
  "middle_left": "水墨輸出",
  "center": "塗鴉匣",
  "middle_right": "工作流程",
  "bottom_left": "保存筆記",
  "bottom_center": "不要做",
  "bottom_right": "下一技能"
}
```

Commands:

```bash
python3 scripts/imandalart_card.py html cells.json --mode hypercard --out card.html
python3 scripts/imandalart_card.py html cells.json --mode paper --out card.html
python3 scripts/imandalart_card.py discord cells.json
python3 scripts/imandalart_card.py discord cells.json --preset mobile-human
python3 scripts/imandalart_card.py check-square cells.json
python3 scripts/imandalart_card.py check-human-eye cells.json --preset mobile-human
python3 scripts/imandalart_card.py pe2 cells.json --preset mobile-air --max-columns 999
python3 scripts/imandalart_card.py discord cells.json --cell-width 8
python3 scripts/imandalart_card.py text cells.json
python3 scripts/imandalart_card.py validate cells.json --density label
```

## Response Pattern

For Discord/Hermes creation:

```text
```text
[ 八大面向 ]

+--------+ +--------+ +--------+
|觸發語  | |輸入源  | |構圖辨識|
...
+--------+ +--------+ +--------+
```
```

Do not lead with a Markdown table. In Discord, the PE2 text block is the primary artifact.

Before returning the block, verify that `check-square` prints `OK: square`. If it fails, reduce cell text, adjust `cell_width/cell_height`, or compress labels and render again. The final Discord block should show three levels: title band, ordinary surrounding title cards, and `⭕` center card.

## Reference

Read `references/imandalart-style.md` when the user mentions HyperCard, paper Mandal-Art, Diddlebug, BPDA/Palm, old iMandalArt screenshots, or asks why this differs from Markdown 九宮格.
