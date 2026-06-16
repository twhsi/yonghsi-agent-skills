# Install

## Local Codex Install

從 repo 根目錄執行：

```bash
cp -R skills/personal-athlete-81-grid ~/.codex/skills/
cp -R skills/project-note-json-to-epub ~/.codex/skills/
cp -R skills/obsidian-graph-view ~/.codex/skills/
cp -R skills/imandalart ~/.codex/skills/
cp -R skills/fire-analysis-card ~/.codex/skills/
```

如果已經安裝過同名 Skill，先在 VS Code 比對差異，再決定是否覆蓋。

## Validate

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/personal-athlete-81-grid
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/project-note-json-to-epub
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/obsidian-graph-view
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/imandalart
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/fire-analysis-card
```

## Trigger Examples

```text
Use $personal-athlete-81-grid to create an Ohtani-style 81 grid for my sport goal.
Use $project-note-json-to-epub to convert this project-note JSON into an EPUB.
Use $obsidian-graph-view to render a weighted graph view from this keyword index.
Use $imandalart to turn this theme into a nine-grid card.
Use $fire-analysis-card to analyze this Chinese article with FIRE.
```
