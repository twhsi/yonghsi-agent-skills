# iMandalArt Style Notes

## Core Correction

iMandalArt is a square index card. In Discord, render it as PE2-like fixed-width text, not HTML and not Markdown 九宮格.

The target analogy is:

- HyperCard card: one self-contained square card, index-like, navigable.
- Old iMandalArt mobile UI: phone screen, 3x3 square, visible cell borders, center emphasis.
- Paper Mandal-Art: hand-drawn planning grid, compact labels, physical card feeling.
- BPDA/Palm era: small screen, dense but calm, minimal decoration.
- PE2 text UI: lines and spaces create a table that displays directly in chat.

## Visual Priorities

1. Square canvas first.
2. Nine visible cells second.
3. Center cell as hub third.
4. Text readable at phone size fourth.
5. Styling restrained: no marketing hero, no decorative gradient blobs, no card-inside-card.

For Discord, "canvas" means a monospaced code block made from borders and spaces.

## Modes

### classic

Use for old iMandalArt/iPhone references:

- White or light gray app background.
- Thin black or gray grid lines.
- Center cell slightly rounded or outlined.
- Simple title above grid.
- Optional tiny status/navigation marks outside the square.

### hypercard

Use for Hermes, card-box, index card, HyperCard, or software-thinking references:

- Off-white card surface.
- Thick black outer border.
- Pixel/Chicago-like or system sans typography if available.
- Header strip with title.
- Strong center cell border or inverted header.
- Feels like a clickable card in a stack.

### pe2

Use for Discord and other chat surfaces that cannot open HTML:

- Render a `text` code block.
- Use ASCII borders: `+`, `-`, `|`.
- Keep all nine cells exactly the same column width and row height.
- Render nine separated mini-cards, not one continuous table.
- Leave one-column gutters between cards to imitate paper/iMandalArt spacing.
- Use left/top text alignment by default; this feels more like a handwritten card.
- Highlight the center card with heavier borders.
- Use pure text hierarchy; do not rely on Discord ANSI color.
- Use a separate title band above the grid; do not let the title consume grid space.
- Default to Discord phone width: `8 columns x 3 rows` per cell, total grid width `32 columns`.
- Calculate cell capacity before writing:
  - 4 CJK characters per line.
  - 8 ASCII characters per line.
  - 12 CJK characters per cell.
  - 24 ASCII characters per cell.
- Use `mobile-air`: `10 columns x 4 rows` only for screenshots or wide chat surfaces after confirming it will not wrap.
- After rendering, immediately run the square check. Do not deliver a card whose main 3x3 body is not visually square.
- Count mixed-width display columns:
  - CJK full-width characters = 2 columns.
  - English letters, numbers, ASCII punctuation = 1 column.
  - Pad with spaces after measuring display width.
- Do not split a long English token letter-by-letter; abbreviate it with `..`.
- Prefer left/top text for Palm launcher labels; use centered text only when the user asks for a poster-like look.
- Use larger cell dimensions for dense specs.

## Plain Text Hierarchy

Use plain `text` code blocks to separate three levels:

- Title line: `[ 標題 ]` above the grid by default.
- Surrounding cards: title-like Chinese headings, left/top aligned.
- Center card: heavier `=` borders plus leading `⭕`.

Avoid ANSI escape sequences. Discord mobile color support is inconsistent and makes the output harder to control.

## Chinese Title Rules

- Prefer Chinese headings.
- Do not insert spaces between Chinese characters.
- Default mobile line width is 4 Chinese characters.
- If a Chinese heading is longer than 4 characters, wrap into the next line instead of inserting spaces.
- Surrounding cells should look like titles, not paragraphs.
- Prefer 2-4 Chinese characters when the cell is a category label, so the remaining blank area becomes visible card space.
- Translate English app names into compact Chinese labels for the mobile render when the meaning remains clear.

## Alignment Rules

- All `+` and `|` characters must be produced by the renderer, not hand-spaced.
- All content lines must be padded to exact display width after CJK/ASCII measurement.
- Spaces are visual language: they create right-side padding, card breathing room, and the Palm OS launcher feel.
- Spaces are not inserted between Chinese characters; they appear only after measured content and between mini-cards.
- Padding formula: `trailing_spaces = cell_width - display_width(label)`.
- In the default 8-column cell, `觸發語` gets 2 trailing spaces, while `水墨輸出` gets 0.
- If a pasted card is visually broken, regenerate from JSON or cell text instead of manually editing the table.

## Palm Card Aesthetic

When the user asks for Rob Haitani, Palm, PE2, Diddlebug, or old iMandalArt:

- Make the card feel like a 160x160-era handheld screen: compact, scannable, and touchable.
- A cell is a tappable label. It should leave interior white space instead of filling every line.
- Phone fit beats air: if visible breathing room causes Discord mobile wrapping, compress the card back to 32 columns.
- Center should read like a Home icon plus a short name, e.g. `⭕塗鴉匣`.
- Do not output `⭕` alone unless the user explicitly asks for an empty center. The symbol marks the center; it does not replace the center label.
- The surrounding eight cells should be short Chinese launcher labels, e.g. `觸發語`, `輸入源`, `水墨輸出`.
- The 3x3 body must read as one big square first, then nine small cards second.

## Square Body Check

The title band is not part of the square body. The square body starts at the first border using `-`.

Pass conditions:

- Main grid width is constant on every line.
- Main grid has 17 text rows with the default mobile preset, including two gutter rows.
- Main grid is at most 32 display columns for Discord phone delivery.
- Each individual cell is also visually close to square: `cell_width / (cell_height * 2)` should be close to `1.0`.
- Estimated visual ratio is close to 1.0.
- No Discord line is wide enough to force horizontal scrolling on a phone.

### paper

Use for paper, notebook, doodle, Diddlebug, handwritten planning references:

- Warm paper background.
- Slightly uneven line color.
- Larger margins.
- Handwritten-like sans fallback.
- Optional faint dot/grid texture from CSS only.

## Difference From Nearby Hermes Skills

| Format | Primary artifact | Text density | Best for |
|---|---|---:|---|
| Markdown 九宮格 | Markdown table | very short | copy/paste labels |
| 向量九宮圖 | icon visual | minimal | concept icons |
| 81 宮 Mandala | large image/HTML | medium | full expansion systems |
| iMandalArt | one square index card / PE2 code block | medium/high | Discord display, phone screenshot, card stack, specs, planning |

## Writing Cells

Each cell is a tiny index-card field:

- Use a compact heading-like phrase.
- Add a short qualifier only when it helps recognition.
- Avoid prose paragraphs.
- Keep the center as the card's hub, not a copied title.
- Keep each default mobile cell within about 12 CJK characters total or 24 ASCII columns total.

Good cell examples:

- `觸發語`
- `輸入來源`
- `構圖辨識`
- `塗鴉匣`
- `13 吋高階`
- `保存筆記`
- `下一技能`

Bad patterns:

- A Markdown table as the final answer.
- Explaining the card instead of rendering it.
- A long essay squeezed into each cell.
- 81 cells or multiple 3x3 grids.
- Icon-only visual output.

## Discord Behavior

When used from Discord, prefer PE2 text output directly in the message. HTML is only a secondary artifact when the user explicitly wants a local visual preview.
