#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter
from pathlib import Path


TOPIC_RE = re.compile(r"^[0-9]+(?:\.[0-9]+){0,4}$")
NUMERIC_RE = re.compile(r"^[0-9]+(?:\.[0-9]+)*$")
KEY_RE = re.compile(r"^K[0-9]{3}$")
MANDALA_RE = re.compile(r"^1(?:\.[1-8]){0,2}$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_codes(payload):
    for chapter in payload.get("chapters", []):
        for entry in chapter.get("observed_codes", []):
            yield entry.get("code"), chapter.get("code"), entry


def main():
    parser = argparse.ArgumentParser(description="Validate auto-luhmann-numberer catalog JSON.")
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()

    payload = load(args.catalog)
    errors = []
    warnings = []
    codes = [code for code, _, _ in flatten_codes(payload) if code]
    source_paths = [
        chapter.get("source_path", "")
        for chapter in payload.get("chapters", [])
        if chapter.get("source_path")
    ]

    duplicates = sorted(code for code, count in Counter(codes).items() if count > 1)
    if duplicates:
        errors.append({"type": "duplicate_code", "codes": duplicates})

    absolute_paths = [path for path in source_paths if path.startswith("/")]
    if absolute_paths:
        errors.append({"type": "absolute_source_path", "paths": absolute_paths[:10]})

    for code, chapter_code, entry in flatten_codes(payload):
        if not code or KEY_RE.match(code):
            continue
        if NUMERIC_RE.match(code) and len(code.split(".")) > 5:
            errors.append({"type": "too_deep", "code": code, "chapter": chapter_code})
        if entry.get("prefix_status") == "off_prefix":
            warnings.append({"type": "off_prefix", "code": code, "chapter": chapter_code})
        for section in entry.get("mandala_sections", []):
            if not MANDALA_RE.match(section):
                errors.append({
                    "type": "invalid_mandala_section",
                    "code": code,
                    "section": section
                })
    for chapter in payload.get("chapters", []):
        for section in chapter.get("mandala_sections", []):
            if not MANDALA_RE.match(section):
                errors.append({
                    "type": "invalid_mandala_section",
                    "code": chapter.get("code"),
                    "section": section
                })

    missing = payload.get("summary", {}).get("missing", [])
    for code in missing:
        warnings.append({"type": "missing_expected_chapter", "code": code})

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "code_count": len(codes),
        "chapter_count": len(payload.get("chapters", [])),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
