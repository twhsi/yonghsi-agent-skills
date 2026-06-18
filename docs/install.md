# Install

## Local Codex Install

從 repo 根目錄執行：

```bash
cp -R skills/todays-daily-plan ~/.codex/skills/
cp -R skills/personal-athlete-81-grid ~/.codex/skills/
cp -R skills/auto-luhmann-numberer ~/.codex/skills/
cp -R skills/project-note-json-to-epub ~/.codex/skills/
cp -R skills/epub-hypercard-obsidian ~/.codex/skills/
cp -R skills/obsidian-graph-view ~/.codex/skills/
cp -R skills/imandalart ~/.codex/skills/
cp -R skills/markdown-nine-grid-clipboard ~/.codex/skills/
cp -R skills/fire-analysis-card ~/.codex/skills/
cp -R skills/fire-card-to-epub ~/.codex/skills/
cp -R skills/pdca ~/.codex/skills/
```

如果已經安裝過同名 Skill，先在 VS Code 比對差異，再決定是否覆蓋。

## Validate

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/todays-daily-plan
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/personal-athlete-81-grid
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/auto-luhmann-numberer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/project-note-json-to-epub
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/epub-hypercard-obsidian
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/obsidian-graph-view
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/imandalart
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/markdown-nine-grid-clipboard
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/fire-analysis-card
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/fire-card-to-epub
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/pdca
```

## Trigger Examples

```text
Use $todays-daily-plan 今日的日計畫，上午羽球，下午三點林君，日記今天完成正式 Skill。
Use $personal-athlete-81-grid to create an Ohtani-style 81 grid for my sport goal.
Use $auto-luhmann-numberer to scan this folder and assign Luhmann-style book/card numbers.
Use $project-note-json-to-epub to convert this project-note JSON into an EPUB.
Use $epub-hypercard-obsidian to convert this EPUB into an Obsidian HyperCard folder with verified links and a portable zip.
Use $obsidian-graph-view to render a weighted graph view from this keyword index.
Use $imandalart to turn this theme into a nine-grid card.
Use $markdown-nine-grid-clipboard to turn this iMandalArt into an Obsidian Markdown nine-grid table.
Use $fire-analysis-card to analyze this Chinese article with FIRE.
Use $fire-card-to-epub to turn FIRE cards into a validated EPUB with keyword index links.
Use $pdca to turn this problem into a Chinese compass-style PDCA/CAPD card.
```
