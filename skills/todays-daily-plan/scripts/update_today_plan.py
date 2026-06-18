#!/usr/bin/env python3
"""Safely append entries to an Obsidian Mandala Grid day-plan Markdown file."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_SLOTS = {
    "1": "陽光起床運動",
    "2": "09-12",
    "3": "12-13",
    "4": "13-15",
    "5": "15-18",
    "6": "18-19",
    "7": "19-21",
    "8": "日記",
}

SECTION_RE = re.compile(r"^\s*<!--\s*section:\s*([0-9]+(?:\.[0-9]+)*)\s*-->\s*$")
H2_DATE_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})(?:\s+.*)?$")
NUMBERED_RE = re.compile(r"^\s*(\d+)\.\s+")


def split_frontmatter(markdown: str) -> Tuple[str, str]:
    if not markdown.startswith("---\n"):
        return "", markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Frontmatter start marker found, but closing marker is missing.")
    frontmatter = markdown[: end + len("\n---\n")]
    body = markdown[end + len("\n---\n") :]
    return frontmatter, body


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(frontmatter: str) -> Dict[str, object]:
    body = frontmatter
    if body.startswith("---\n"):
        body = body[4:]
    if body.endswith("\n---\n"):
        body = body[:-5]
    elif body.endswith("\n---"):
        body = body[:-4]

    mandala = False
    in_plan = False
    in_slots = False
    enabled = False
    year: Optional[int] = None
    slots: Dict[str, str] = {}

    for raw_line in body.splitlines():
        line = raw_line.replace("\t", "    ")
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if indent == 0 and stripped.startswith("mandala:"):
            mandala = strip_quotes(stripped.split(":", 1)[1]).lower() == "true"
            in_plan = False
            in_slots = False
            continue

        if indent == 0 and stripped == "mandala_plan:":
            in_plan = True
            in_slots = False
            continue

        if indent == 0 and stripped and in_plan:
            in_plan = False
            in_slots = False

        if not in_plan:
            continue

        if stripped.lower() == "enabled: true":
            enabled = True
            continue

        if stripped.startswith("year:"):
            value = strip_quotes(stripped.split(":", 1)[1])
            if value.isdigit():
                year = int(value)
            continue

        if stripped == "slots:":
            in_slots = True
            continue

        if in_slots:
            if indent < 4 and stripped:
                in_slots = False
                continue
            match = re.match(r'^"?([1-8])"?\s*:\s*(.*)$', stripped)
            if match:
                slots[match.group(1)] = strip_quotes(match.group(2))

    return {
        "mandala": mandala,
        "enabled": enabled,
        "year": year,
        "slots": {**DEFAULT_SLOTS, **slots},
    }


def parse_iso_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Invalid ISO date: {value}") from exc


def day_section(plan_year: int, date_value: dt.date) -> str:
    if date_value.year != plan_year:
        raise ValueError(f"Date {date_value.isoformat()} is not in plan year {plan_year}.")
    return str((date_value - dt.date(plan_year, 1, 1)).days + 1)


def marker_section(line: str) -> Optional[str]:
    match = SECTION_RE.match(line)
    return match.group(1) if match else None


def find_section_index(lines: List[str], section: str) -> int:
    for index, line in enumerate(lines):
        if marker_section(line) == section:
            return index
    return -1


def find_next_marker_index(lines: List[str], start: int) -> int:
    for index in range(start, len(lines)):
        if marker_section(lines[index]):
            return index
    return len(lines)


def find_day_by_heading(lines: List[str], date_value: dt.date) -> Optional[str]:
    target = date_value.isoformat()
    current_section: Optional[str] = None
    for line in lines:
        section = marker_section(line)
        if section and "." not in section:
            current_section = section
            continue
        if current_section and H2_DATE_RE.match(line.strip()):
            if H2_DATE_RE.match(line.strip()).group(1) == target:
                return current_section
    return None


def ensure_children(lines: List[str], section: str, count: int = 8) -> List[str]:
    lines = list(lines)
    start = find_section_index(lines, section)
    if start == -1:
        raise ValueError(f'Missing parent section "{section}".')

    end = len(lines)
    for index in range(start + 1, len(lines)):
        parsed = marker_section(lines[index])
        if not parsed:
            continue
        if not parsed.startswith(f"{section}."):
            end = index
            break

    existing: Dict[int, int] = {}
    for index in range(start + 1, end):
        parsed = marker_section(lines[index])
        if not parsed or not parsed.startswith(f"{section}."):
            continue
        suffix = parsed[len(section) + 1 :]
        if "." in suffix:
            continue
        if suffix.isdigit():
            existing[int(suffix)] = index

    insertions: Dict[int, List[str]] = {}
    for slot in range(1, count + 1):
        if slot in existing:
            continue
        insert_at = end
        for next_slot in range(slot + 1, count + 1):
            if next_slot in existing:
                insert_at = existing[next_slot]
                break
        insertions.setdefault(insert_at, []).extend([f"<!--section: {section}.{slot}-->", ""])

    for insert_at in sorted(insertions.keys(), reverse=True):
        lines[insert_at:insert_at] = insertions[insert_at]

    return lines


def get_section_bounds(lines: List[str], section: str) -> Tuple[int, int, int]:
    marker = find_section_index(lines, section)
    if marker == -1:
        raise ValueError(f'Missing section "{section}".')
    end = find_next_marker_index(lines, marker + 1)
    return marker, marker + 1, end


def first_non_empty_index(lines: List[str], start: int, end: int) -> int:
    for index in range(start, end):
        if lines[index].strip():
            return index
    return -1


def ensure_slot_heading(lines: List[str], section: str, title: str) -> List[str]:
    lines = list(lines)
    _marker, start, end = get_section_bounds(lines, section)
    heading = f"### {title.strip()}"
    first = first_non_empty_index(lines, start, end)
    if first == -1:
        lines[start:end] = [heading]
        return lines
    if lines[first].strip().startswith("### "):
        lines[first] = heading
        return lines
    lines[start:start] = [heading]
    return lines


def resolve_slot(slot: str, slots: Dict[str, str], text: str) -> str:
    slot = slot.strip()
    if slot in slots:
        return slot
    normalized = slot.replace("：", ":")
    for key, title in slots.items():
        if normalized == title or normalized == title.replace("：", ":"):
            return key

    haystack = f"{slot} {text}"
    rules = [
        ("1", ["起床", "陽光", "太阳", "太陽", "跑步", "運動", "运动", "早餐", "靜坐"]),
        ("2", ["09", "9點", "九點", "10點", "十點", "11點", "十一點", "上午", "早上"]),
        ("3", ["12", "中午", "午餐", "午睡", "領午餐"]),
        ("4", ["13", "14", "一點", "兩點", "两点", "下午一", "下午二"]),
        ("5", ["15", "16", "17", "三點", "四點", "五點", "下午三", "下午四", "下午五"]),
        ("6", ["18", "六點", "六点", "晚餐", "傍晚"]),
        ("7", ["19", "20", "晚上", "晚間", "合唱", "管委會", "會議", "会议"]),
        ("8", ["日記", "日记", "心得", "感謝", "感谢", "反省", "回顧", "回顾"]),
    ]
    for key, keywords in rules:
        if any(keyword in haystack for keyword in keywords):
            return key

    raise ValueError(f"Cannot resolve slot from {slot!r}; pass 1..8 or a configured slot title.")


def next_diary_number(section_lines: List[str]) -> int:
    highest = 0
    for line in section_lines:
        match = NUMBERED_RE.match(line)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def format_entry(text: str, kind: str, section_lines: List[str], slot_key: str) -> str:
    text = text.strip("\n")
    if not text.strip():
        raise ValueError("Entry text is empty.")
    if kind == "auto":
        kind = "diary" if slot_key == "8" else "plain"
    if kind == "plain":
        return text
    if kind == "task":
        if re.match(r"^\s*-\s+\[[ xX]\]\s+", text):
            return text
        return f"- [ ] {text}"
    if kind == "done":
        if re.match(r"^\s*-\s+\[[xX]\]\s+", text):
            return text
        return f"- [x] {text}"
    if kind == "diary":
        if NUMBERED_RE.match(text):
            return text
        return f"{next_diary_number(section_lines)}. {text}"
    raise ValueError(f"Unsupported kind: {kind}")


def append_entry(lines: List[str], section: str, entry: str) -> List[str]:
    lines = list(lines)
    _marker, start, end = get_section_bounds(lines, section)
    while end > start and lines[end - 1].strip() == "":
        end -= 1
    insertion = entry.split("\n")
    if end > start:
        lines[end:end] = insertion
    else:
        lines[start:start] = insertion
    return lines


def section_has_entry(section_lines: List[str], entry: str) -> bool:
    needle = [line.rstrip() for line in entry.split("\n")]
    haystack = [line.rstrip() for line in section_lines]
    if not needle:
        return False
    for index in range(0, len(haystack) - len(needle) + 1):
        if haystack[index : index + len(needle)] == needle:
            return True
    return False


def update_markdown(markdown: str, date_text: str, slot: str, text: str, kind: str) -> Tuple[str, Dict[str, object]]:
    normalized = markdown.replace("\r\n", "\n")
    frontmatter, body = split_frontmatter(normalized)
    config = parse_frontmatter(frontmatter)
    if not config["mandala"] or not config["enabled"]:
        raise ValueError("Target file is not an active Mandala Grid day-plan Markdown file.")
    plan_year = config["year"]
    if not isinstance(plan_year, int):
        raise ValueError("mandala_plan.year is missing or invalid.")

    target_date = parse_iso_date(date_text)
    root = day_section(plan_year, target_date)
    lines = body.split("\n")

    if find_section_index(lines, root) == -1:
        heading_root = find_day_by_heading(lines, target_date)
        if heading_root:
            root = heading_root
        else:
            raise ValueError(f"Cannot find root section for {target_date.isoformat()} ({root}).")

    lines = ensure_children(lines, root, 8)
    slots = config["slots"]
    assert isinstance(slots, dict)
    for key in range(1, 9):
        child = f"{root}.{key}"
        lines = ensure_slot_heading(lines, child, str(slots[str(key)]))

    slot_key = resolve_slot(slot, slots, text)
    child = f"{root}.{slot_key}"
    _marker, start, end = get_section_bounds(lines, child)
    entry = format_entry(text, kind, lines[start:end], slot_key)
    duplicate_skipped = section_has_entry(lines[start:end], entry)
    if not duplicate_skipped:
        lines = append_entry(lines, child, entry)

    return frontmatter + "\n".join(lines), {
        "date": target_date.isoformat(),
        "root_section": root,
        "slot": slot_key,
        "slot_title": slots[slot_key],
        "section": child,
        "entry": entry,
        "duplicate_skipped": duplicate_skipped,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, help="Path to the day-plan Markdown file.")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Target date, YYYY-MM-DD.")
    parser.add_argument("--slot", required=True, help="Slot number, slot title, or a time phrase.")
    parser.add_argument("--text", required=True, help="Entry text to append.")
    parser.add_argument(
        "--kind",
        choices=["auto", "plain", "task", "done", "diary"],
        default="auto",
        help="Entry formatting. auto uses diary for slot 8 and plain text otherwise.",
    )
    parser.add_argument("--apply", action="store_true", help="Write the change to the file.")
    args = parser.parse_args()

    path = Path(args.file).expanduser()
    original = path.read_text(encoding="utf-8")
    updated, summary = update_markdown(original, args.date, args.slot, args.text, args.kind)
    summary["changed"] = updated != original.replace("\r\n", "\n")
    summary["applied"] = bool(args.apply)

    if args.apply and summary["changed"]:
        path.write_text(updated, encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
