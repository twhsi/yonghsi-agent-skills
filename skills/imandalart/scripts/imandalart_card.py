#!/usr/bin/env python3
"""Render iMandalArt square 3x3 index cards from JSON."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import textwrap
import unicodedata
from pathlib import Path

POSITIONS = [
    "top_left",
    "top_center",
    "top_right",
    "middle_left",
    "center",
    "middle_right",
    "bottom_left",
    "bottom_center",
    "bottom_right",
]

ROWS = [
    ("top_left", "top_center", "top_right"),
    ("middle_left", "center", "middle_right"),
    ("bottom_left", "bottom_center", "bottom_right"),
]

LIMITS = {
    "label": (3, 18, 2, 16),
    "micro": (6, 16, 8, 24),
    "standard": (8, 28, 16, 44),
    "dense": (12, 44, 28, 72),
}

THEMES = {
    "classic": {
        "body": "#ececec",
        "card": "#f8f8f8",
        "grid": "#1f1f1f",
        "cell": "#ffffff",
        "center": "#f7f7f7",
        "accent": "#606060",
        "text": "#111111",
        "shadow": "0 18px 34px rgba(0,0,0,.28)",
        "font": "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif",
        "radius": "4px",
    },
    "hypercard": {
        "body": "#d9d5c8",
        "card": "#f3f0e6",
        "grid": "#111111",
        "cell": "#fbfaf3",
        "center": "#fffdf6",
        "accent": "#111111",
        "text": "#111111",
        "shadow": "10px 10px 0 rgba(0,0,0,.22)",
        "font": "Chicago, Geneva, 'Helvetica Neue', Arial, sans-serif",
        "radius": "0",
    },
    "paper": {
        "body": "#c9c0ad",
        "card": "#f7f0dd",
        "grid": "#3c352b",
        "cell": "rgba(255,252,239,.72)",
        "center": "rgba(255,248,221,.95)",
        "accent": "#5c4c36",
        "text": "#211b14",
        "shadow": "0 20px 38px rgba(44,34,20,.26)",
        "font": "'Marker Felt', 'Hiragino Maru Gothic ProN', 'Helvetica Neue', Arial, sans-serif",
        "radius": "3px",
    },
}

PRESETS = {
    "mobile": {"cell_width": 8},
    "mobile-human": {"cell_width": 8, "cell_height": 3, "style": "human-eye"},
    "mobile-air": {"cell_width": 10},
    "mobile-compact": {"cell_width": 8},
    "mobile-loose": {"cell_width": 10},
    "desktop": {"cell_width": 16},
}

CARD_GAP = 1
DISCORD_MOBILE_MAX_COLUMNS = 32
CJK_RE = r"\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\uff00-\uffef"


def display_width(text: str) -> int:
    width = 0
    for char in text:
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width


def pad_display(text: str, width: int) -> str:
    return text + " " * max(0, width - display_width(text))


def fit_display(text: str, width: int) -> str:
    out = ""
    for char in text:
        next_text = out + char
        if display_width(next_text) > width:
            break
        out = next_text
    return out


def abbreviate_display(text: str, width: int) -> str:
    if display_width(text) <= width:
        return text
    marker = ".." if width >= 4 else "."
    base_width = max(1, width - display_width(marker))
    return fit_display(text, base_width) + marker


def align_display(text: str, width: int, align: str) -> str:
    used = display_width(text)
    if used >= width:
        return fit_display(text, width)
    if align == "center":
        left = (width - used) // 2
        right = width - used - left
        return " " * left + text + " " * right
    return pad_display(text, width)


def center_line(text: str, width: int) -> str:
    return align_display(text, width, "center")


def cjk_len(text: str) -> int:
    total = 0
    for char in text:
        if char.isspace():
            continue
        total += 1 if unicodedata.east_asian_width(char) in {"F", "W"} else 0.5
    return int(round(total))


def normalize_cell_text(text: str, preserve_visual_spaces: bool = False) -> str:
    if preserve_visual_spaces:
        lines = []
        for line in str(text).splitlines() or [str(text)]:
            line = re.sub(r"[ \t]+", " ", line.strip())
            lines.append(line)
        return "\n".join(lines).strip()

    text = " ".join(str(text).split())
    # Chinese/Japanese full-width text should stay compact: no spaces between CJK chars.
    text = re.sub(fr"([{CJK_RE}])\s+([{CJK_RE}])", r"\1\2", text)
    return text


def prepare_cell_text(key: str, text: str, style: str = "compact") -> str:
    text = normalize_cell_text(text, preserve_visual_spaces=style == "human-eye")
    if key == "center" and not text.startswith("⭕"):
        text = "⭕" + text
    return text


def text_units(text: str) -> list[str]:
    units = []
    for part in re.findall(r"[A-Za-z0-9][A-Za-z0-9._/-]*|\s+|.", text):
        if part.isspace():
            units.append(" ")
        else:
            units.append(part)
    return units


def wrap_cell(text: str, width: int, style: str = "compact") -> list[str]:
    text = normalize_cell_text(text, preserve_visual_spaces=style == "human-eye")
    if not text:
        return [""]

    if "\n" in text:
        wrapped_lines: list[str] = []
        for line in text.splitlines():
            wrapped_lines.extend(wrap_cell(line, width, style))
        return wrapped_lines or [""]

    lines: list[str] = []
    current = ""
    for unit in text_units(text):
        if display_width(unit) > width:
            unit = abbreviate_display(unit, width)
        if unit == " " and not current:
            continue
        next_text = current + unit
        if current and display_width(next_text) > width:
            lines.append(current)
            current = "" if unit == " " else unit
        else:
            current = next_text
    if current:
        lines.append(current)

    wrapped: list[str] = []
    for line in lines:
        if display_width(line) <= width:
            wrapped.append(line)
        else:
            wrapped.extend(textwrap.wrap(line, width=max(1, width)))
    return wrapped or [""]


def truncate_lines(lines: list[str], width: int, height: int) -> list[str]:
    clipped = lines[:height]
    if len(lines) > height and clipped:
        marker = "..."
        base_width = max(0, width - display_width(marker))
        clipped[-1] = fit_display(clipped[-1], base_width) + marker
    return clipped


def render_title_band(title: str, total_width: int, title_style: str = "bracket") -> list[str]:
    if title_style == "bracket":
        title_text = f"[ {normalize_cell_text(title)} ]"
        return [center_line(abbreviate_display(title_text, total_width), total_width)]

    inner_width = total_width - 2
    title_lines = truncate_lines(wrap_cell(title, inner_width), inner_width, 2)
    border = "+" + "=" * inner_width + "+"
    out = [border]
    for line in title_lines:
        out.append("|" + align_display(line, inner_width, "center") + "|")
    out.append(border)
    return out


def auto_cell_height(cell_width: int, gap: int = CARD_GAP) -> int:
    # Each cell is a mini card: content width plus two borders. Discord mobile
    # monospace characters are roughly half as wide as they are tall.
    card_width = cell_width + 2
    return max(2, round(card_width / 2) - 2)


def resolve_dimensions(preset: str, cell_width: int | None, cell_height: int | None) -> tuple[int, int]:
    if cell_width is None:
        cell_width = PRESETS[preset]["cell_width"]
    if cell_height is None:
        cell_height = PRESETS[preset].get("cell_height", auto_cell_height(cell_width))
    return cell_width, cell_height


def resolve_style(preset: str, style: str | None) -> str:
    if style:
        return style
    return PRESETS[preset].get("style", "compact")


def cell_capacity(cell_width: int, cell_height: int) -> dict[str, int]:
    return {
        "cell_width": cell_width,
        "cell_height": cell_height,
        "cjk_per_line": cell_width // 2,
        "ascii_per_line": cell_width,
        "cjk_total": (cell_width // 2) * cell_height,
        "ascii_total": cell_width * cell_height,
        "display_columns_total": cell_width * cell_height,
    }


def load_cells(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = [key for key in POSITIONS if key not in data]
    extra = [key for key in data if key not in POSITIONS and key != "title"]
    if missing or extra:
        problems = []
        if missing:
            problems.append(f"missing: {', '.join(missing)}")
        if extra:
            problems.append(f"extra: {', '.join(extra)}")
        raise SystemExit("; ".join(problems))
    cells = {key: str(data[key]).strip() for key in POSITIONS}
    cells["title"] = str(data.get("title", "iMandalArt")).strip() or "iMandalArt"
    return cells


def render_text(cells: dict[str, str], width: int) -> str:
    border = "+" + "+".join("-" * (width + 2) for _ in range(3)) + "+"
    out = [f"iMandalArt: {cells['title']}", "", border]
    for row in ROWS:
        wrapped = [wrap_cell(cells[key], width) for key in row]
        height = max(len(lines) for lines in wrapped)
        for line_index in range(height):
            parts = []
            for lines in wrapped:
                value = lines[line_index] if line_index < len(lines) else ""
                parts.append(f" {pad_display(value, width)} ")
            out.append("|" + "|".join(parts) + "|")
        out.append(border)
    return "\n".join(out)


def render_pe2(
    cells: dict[str, str],
    cell_width: int,
    cell_height: int,
    align: str,
    title_style: str,
    style: str = "compact",
) -> str:
    total_width = 3 * (cell_width + 2) + 2 * CARD_GAP
    out = render_title_band(cells["title"], total_width, title_style)
    out.append("")
    for row in ROWS:
        top_parts = []
        content_by_cell = []
        bottom_parts = []
        for key in row:
            is_center = key == "center"
            horizontal_char = "=" if is_center else "-"
            top = "+" + horizontal_char * cell_width + "+"
            bottom = "+" + horizontal_char * cell_width + "+"
            top_parts.append(top)
            bottom_parts.append(bottom)
            lines = wrap_cell(prepare_cell_text(key, cells[key], style), cell_width, style)
            lines = truncate_lines(lines, cell_width, cell_height)
            content_by_cell.append((key, lines))
        out.append((" " * CARD_GAP).join(top_parts))
        for line_index in range(cell_height):
            parts = []
            for key, lines in content_by_cell:
                value = lines[line_index] if line_index < len(lines) else ""
                cell_line = "|" + align_display(value, cell_width, align) + "|"
                parts.append(cell_line)
            out.append((" " * CARD_GAP).join(parts))
        out.append((" " * CARD_GAP).join(bottom_parts))
        if row != ROWS[-1]:
            out.extend([" " * total_width for _ in range(CARD_GAP)])
    return "\n".join(out)


def grid_metrics(cell_width: int, cell_height: int) -> dict[str, float | int]:
    display_columns = 3 * (cell_width + 2) + 2 * CARD_GAP
    text_rows = 3 * (cell_height + 2) + 2 * CARD_GAP
    # Discord mobile monospace characters are roughly half as wide as they are tall.
    visual_ratio = display_columns / (text_rows * 2)
    cell_visual_ratio = (cell_width + 2) / ((cell_height + 2) * 2)
    return {
        "display_columns": display_columns,
        "text_rows": text_rows,
        "visual_ratio": round(visual_ratio, 3),
        "cell_visual_ratio": round(cell_visual_ratio, 3),
    }


def extract_grid_lines(rendered: str) -> list[str]:
    lines = rendered.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("+") and "-" in line:
            return lines[index:]
        if line.startswith("+") and "=" in line:
            # Skip the title band; the square body starts after the blank line.
            continue
    return []


def check_square(
    rendered: str,
    cell_width: int,
    cell_height: int,
    max_columns: int | None = DISCORD_MOBILE_MAX_COLUMNS,
) -> list[str]:
    grid = extract_grid_lines(rendered)
    metrics = grid_metrics(cell_width, cell_height)
    expected_columns = int(metrics["display_columns"])
    expected_rows = int(metrics["text_rows"])
    errors = []

    if len(grid) != expected_rows:
        errors.append(f"grid rows {len(grid)}, expected {expected_rows}")

    if max_columns is not None and expected_columns > max_columns:
        errors.append(
            f"PALM phone-first width {expected_columns}, expected <= {max_columns}; "
            "use the mobile preset or shorter labels"
        )

    for index, line in enumerate(grid):
        width = display_width(line)
        if width != expected_columns:
            errors.append(f"line {index + 1} width {width}, expected {expected_columns}")

    borders = [line for line in grid if line.startswith("+")]
    if len(borders) != 6:
        errors.append(f"card border rows {len(borders)}, expected 6")

    content_rows = [line for line in grid if line.startswith("|")]
    if len(content_rows) != 3 * cell_height:
        errors.append(f"content rows {len(content_rows)}, expected {3 * cell_height}")

    ratio = float(metrics["visual_ratio"])
    if ratio < 0.85 or ratio > 1.15:
        errors.append(f"visual ratio {ratio}, expected 0.85-1.15")

    cell_ratio = float(metrics["cell_visual_ratio"])
    if cell_ratio < 0.85 or cell_ratio > 1.15:
        errors.append(f"cell visual ratio {cell_ratio}, expected 0.85-1.15")

    return errors


def check_human_eye(
    cells: dict[str, str],
    cell_width: int,
    cell_height: int,
    style: str = "compact",
) -> list[str]:
    errors = []
    for key in POSITIONS:
        prepared = prepare_cell_text(key, cells[key], style)
        lines = truncate_lines(wrap_cell(prepared, cell_width, style), cell_width, cell_height)
        nonempty = [line for line in lines if line.strip()]

        if not nonempty:
            errors.append(f"{key} has no visible text")

        blank_count = cell_height - len(nonempty)
        if blank_count > 1:
            errors.append(f"{key} has {blank_count} blank rows, expected <= 1")

        if key == "center":
            if not prepared.startswith("⭕"):
                errors.append("center is missing leading ⭕")
            center_label = prepared.removeprefix("⭕").strip()
            if not center_label:
                errors.append("center has ⭕ but no label")
            first_raw_line = prepared.splitlines()[0] if prepared.splitlines() else prepared
            if display_width(first_raw_line) > cell_width:
                errors.append(f"center first line is squeezed by emoji, expected <= {cell_width} columns")

        if len(nonempty) >= 2:
            first_width = display_width(nonempty[0])
            second_width = display_width(nonempty[1])
            if abs(first_width - second_width) > max(4, cell_width // 2):
                errors.append(
                    f"{key} line balance {first_width}/{second_width}, expected closer visual widths"
                )

        if style == "human-eye" and key != "center":
            for line in nonempty[:2]:
                width = display_width(line)
                trailing_padding = cell_width - width
                if width > cell_width:
                    errors.append(f"{key} human-eye line exceeds {cell_width} columns")
                if width < 4:
                    errors.append(f"{key} human-eye line {line!r} is too sparse, expected >= 4 columns")
                if width > 6:
                    errors.append(
                        f"{key} human-eye line {line!r} leaves {trailing_padding} trailing spaces, expected >= 2"
                    )
                if re.search(fr"[{CJK_RE}] [{CJK_RE}]", line) and trailing_padding < 2:
                    errors.append(
                        f"{key} human-eye line {line!r} uses internal CJK spacing without right-side breathing room"
                    )
    return errors


def print_square_report(
    cell_width: int,
    cell_height: int,
    max_columns: int | None = DISCORD_MOBILE_MAX_COLUMNS,
) -> None:
    metrics = grid_metrics(cell_width, cell_height)
    capacity = cell_capacity(cell_width, cell_height)
    print(
        "OK: square PALM "
        f"{metrics['display_columns']} columns x {metrics['text_rows']} rows "
        f"(body_ratio={metrics['visual_ratio']}, cell_ratio={metrics['cell_visual_ratio']}); "
        f"cell={capacity['cell_width']} cols x {capacity['cell_height']} rows, "
        f"{capacity['cjk_per_line']} CJK/line, {capacity['ascii_per_line']} ASCII/line, "
        f"{capacity['cjk_total']} CJK total or {capacity['ascii_total']} ASCII total; "
        f"phone_width<={max_columns if max_columns is not None else 'off'}"
    )


def font_size_class(value: str) -> str:
    length = display_width(value)
    if length <= 12:
        return "xl"
    if length <= 24:
        return "lg"
    if length <= 38:
        return "md"
    return "sm"


def cell_html(cells: dict[str, str], key: str) -> str:
    value = html.escape(cells[key]).replace("\n", "<br>")
    classes = ["cell", font_size_class(cells[key])]
    if key == "center":
        classes.append("center")
    return f'<section class="{" ".join(classes)}"><div>{value}</div></section>'


def render_html(cells: dict[str, str], mode: str) -> str:
    theme = THEMES[mode]
    cells_markup = "\n".join(cell_html(cells, key) for row in ROWS for key in row)
    paper_texture = ""
    if mode == "paper":
        paper_texture = """
  background-image:
    linear-gradient(rgba(60,53,43,.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(60,53,43,.06) 1px, transparent 1px);
  background-size: 22px 22px;
"""
    header = "Mandal-Art" if mode == "classic" else cells["title"]
    escaped_title = html.escape(cells["title"])
    escaped_header = html.escape(header)
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escaped_title} - iMandalArt</title>
<style>
:root {{
  color-scheme: light;
  --body: {theme["body"]};
  --card: {theme["card"]};
  --grid: {theme["grid"]};
  --cell: {theme["cell"]};
  --center: {theme["center"]};
  --accent: {theme["accent"]};
  --text: {theme["text"]};
  --radius: {theme["radius"]};
  --shadow: {theme["shadow"]};
  --font: {theme["font"]};
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: var(--body);
  color: var(--text);
  font-family: var(--font);
}}
.stage {{
  width: min(92vmin, 760px);
  aspect-ratio: 1 / 1;
  padding: 4.8%;
  background: var(--card);
  border: 3px solid var(--grid);
  box-shadow: var(--shadow);
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 3.4%;
{paper_texture}}}
.topbar {{
  min-height: 7%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  font-weight: 800;
  letter-spacing: 0;
  font-size: clamp(18px, 3.2vmin, 30px);
  line-height: 1;
}}
.topbar small {{
  font-size: clamp(12px, 1.7vmin, 16px);
  font-weight: 700;
  color: var(--accent);
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  border: 2px solid var(--grid);
  background: var(--grid);
  gap: 2px;
  min-height: 0;
}}
.cell {{
  min-width: 0;
  min-height: 0;
  background: var(--cell);
  border-radius: var(--radius);
  padding: 8%;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  overflow: hidden;
  line-height: 1.22;
  font-weight: 760;
  word-break: break-word;
  overflow-wrap: break-word;
}}
.cell > div {{
  max-width: 100%;
}}
.cell.xl {{ font-size: clamp(25px, 4.4vmin, 48px); }}
.cell.lg {{ font-size: clamp(21px, 3.5vmin, 38px); }}
.cell.md {{ font-size: clamp(17px, 2.8vmin, 30px); }}
.cell.sm {{ font-size: clamp(14px, 2.15vmin, 23px); }}
.center {{
  background: var(--center);
  outline: 4px solid var(--accent);
  outline-offset: -8px;
  border-radius: 16px;
  align-items: flex-start;
}}
.center > div {{
  font-weight: 900;
}}
.footer {{
  min-height: 5%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--accent);
  font-size: clamp(12px, 1.8vmin, 16px);
  font-weight: 700;
}}
.navdot {{
  width: .55rem;
  height: .55rem;
  border-radius: 999px;
  background: var(--accent);
  display: inline-block;
}}
@media (max-width: 520px) {{
  .stage {{ width: 96vmin; padding: 4%; }}
  .cell {{ padding: 7%; }}
}}
</style>
</head>
<body>
  <main class="stage" aria-label="iMandalArt square index card">
    <header class="topbar"><span>{escaped_header}</span><small>3x3</small></header>
    <div class="grid">
      {cells_markup}
    </div>
    <footer class="footer"><span>‹</span><span class="navdot"></span><span>⌂</span></footer>
  </main>
</body>
</html>
"""


def validate(cells: dict[str, str], density: str) -> list[str]:
    center_min, center_max, outer_min, outer_max = LIMITS[density]
    warnings = []
    for key, value in cells.items():
        if key == "title":
            continue
        length = cjk_len(value)
        if key == "center":
            if length < center_min or length > center_max:
                warnings.append(f"center length {length}, expected {center_min}-{center_max}")
        elif length < outer_min or length > outer_max:
            warnings.append(f"{key} length {length}, expected {outer_min}-{outer_max}")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Render iMandalArt square 3x3 index cards.")
    parser.add_argument("command", choices=["pe2", "discord", "html", "text", "json", "validate", "check-square", "check-human-eye"])
    parser.add_argument("cells", type=Path)
    parser.add_argument("--width", type=int, default=16)
    parser.add_argument("--preset", choices=sorted(PRESETS), default="mobile")
    parser.add_argument("--cell-width", type=int)
    parser.add_argument("--cell-height", type=int)
    parser.add_argument("--align", choices=["left", "center"], default="left")
    parser.add_argument("--mode", choices=sorted(THEMES), default="hypercard")
    parser.add_argument("--title-style", choices=["bracket", "box"], default="bracket")
    parser.add_argument("--style", choices=["compact", "human-eye"])
    parser.add_argument("--density", choices=sorted(LIMITS), default="standard")
    parser.add_argument("--max-columns", type=int, default=DISCORD_MOBILE_MAX_COLUMNS)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--skip-square-check", action="store_true")
    parser.add_argument("--report-square", action="store_true")
    args = parser.parse_args()

    cells = load_cells(args.cells)
    cell_width, cell_height = resolve_dimensions(args.preset, args.cell_width, args.cell_height)
    style = resolve_style(args.preset, args.style)

    if args.command in {"pe2", "discord"}:
        pe2_output = render_pe2(cells, cell_width, cell_height, args.align, args.title_style, style)
        if not args.skip_square_check:
            errors = check_square(pe2_output, cell_width, cell_height, args.max_columns)
            if style == "human-eye":
                errors.extend(check_human_eye(cells, cell_width, cell_height, style))
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
        output = pe2_output
        if args.command == "discord":
            output = "```text\n" + output + "\n```"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
            print(args.out)
        else:
            print(output)
        if args.report_square:
            print_square_report(cell_width, cell_height, args.max_columns)
    elif args.command == "html":
        output = render_html(cells, args.mode)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
            print(args.out)
        else:
            print(output)
    elif args.command == "text":
        print(render_text(cells, args.width))
    elif args.command == "json":
        print(json.dumps(cells, ensure_ascii=False, indent=2))
    elif args.command == "validate":
        warnings = validate(cells, args.density)
        if warnings:
            print("\n".join(warnings), file=sys.stderr)
            return 1
        print(f"OK: {args.density}")
    elif args.command == "check-square":
        output = render_pe2(cells, cell_width, cell_height, args.align, args.title_style, style)
        errors = check_square(output, cell_width, cell_height, args.max_columns)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print_square_report(cell_width, cell_height, args.max_columns)
    elif args.command == "check-human-eye":
        errors = check_human_eye(cells, cell_width, cell_height, style)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print(f"OK: human-eye {cell_width} cols x {cell_height} rows, style={style}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
