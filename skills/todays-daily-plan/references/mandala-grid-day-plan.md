# Mandala Grid Day-Plan Contract

Use this reference before manually editing an Obsidian Mandala Grid day-plan Markdown file.

## Source Plugin

Plugin: Mandala Grid  
Repository: https://github.com/panAtGitHub/obsidian-mandala-grid  
Obsidian community page: https://community.obsidian.md/plugins/mandala-grid

## Required Frontmatter

A day-plan file must contain:

```yaml
mandala: true
mandala_plan:
  enabled: true
  year: 2026
  slots:
    "1": "陽光起床運動"
    "2": "09-12"
    "3": "12-13"
    "4": "13-15"
    "5": "15-18"
    "6": "18-19"
    "7": "19-21"
    "8": "日記"
```

`daily_only_3x3: true` may appear in older files. Preserve it when present; do not add or remove it unless the user asks.

## Section Markers

Mandala Grid parses section markers with this shape:

```markdown
<!--section: 169-->
## 2026-06-18 四
<!--section: 169.1-->
### 陽光起床運動
<!--section: 169.2-->
### 09-12
```

Rules:

- Root sections are day-of-year numbers and must be continuous from `1` to the year's final day.
- Child slot IDs must be `N.1` through `N.8`.
- Never create `N.9`.
- Never create a child section if the parent root section is missing.
- Do not reorder existing root sections.
- Do not change existing section IDs to match headings.

## Date To Section Mapping

Compute the root section as day-of-year in `mandala_plan.year`.

Examples for 2026:

- `2026-01-01` -> `1`
- `2026-03-31` -> `90`
- `2026-06-18` -> `169`
- `2026-12-31` -> `365`

## Safe Update Pattern

1. Split frontmatter and body.
2. Find the target root marker.
3. If the root exists but children are missing, insert missing child markers in order before the next root marker.
4. Ensure the first non-empty line of each child section is `### {slot title}`.
5. Append user content inside the target child section, before the next section marker.
6. If continuing after an interrupted run, compare the requested entry against the target child section and skip exact duplicates.
7. Preserve all unrelated text, tables, images, links, and code blocks.

Prefer `scripts/update_today_plan.py` for this pattern.
