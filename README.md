# 永錫 Agent Skill 庫

這個資料夾整理四個已成熟、可分享、可放進 GitHub，也適合在新書中連結引用的 Codex Skills。

## Four Core Skills

| Skill | 用途 | 入口 |
|---|---|---|
| JSON 到 EPUB | 把結構化專案筆記 JSON 轉成可驗證的 EPUB | [`skills/project-note-json-to-epub/`](skills/project-note-json-to-epub/) |
| Graph view | 從 JSON、索引、TOC、卡片資料產生 Obsidian 風格關係圖 | [`skills/obsidian-graph-view/`](skills/obsidian-graph-view/) |
| 九宮格 / iMandalArt | 產生九宮格、曼陀羅卡、Hermes/Discord 文字卡 | [`skills/imandalart/`](skills/imandalart/) |
| FIRE 原則 | 以 Fact、Index、Relation、Encyclopedia 分析中文文章 | [`skills/fire-analysis-card/`](skills/fire-analysis-card/) |

## Repo Layout

```text
skills/      四個正式 Skills
docs/        GitHub、安裝、書籍連結說明
examples/    未來放每個 Skill 的輸入與輸出範例
archive/     舊版或暫不公開的 Skill 草稿
```

## Install Locally

把需要的 Skill 複製到 Codex skills 目錄：

```bash
cp -R skills/project-note-json-to-epub ~/.codex/skills/
cp -R skills/obsidian-graph-view ~/.codex/skills/
cp -R skills/imandalart ~/.codex/skills/
cp -R skills/fire-analysis-card ~/.codex/skills/
```

更多說明見 [`docs/install.md`](docs/install.md)。

## For VS Code Editing

用 VS Code 開啟這個資料夾：

```bash
code "/Users/twhsi/+++ 000 AI向量庫/01 Agent Skill庫"
```

建議每次修改後驗證 Skill：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/imandalart
```

## Book Links

未來新書可以把每個章節連到固定 GitHub URL。先用 [`docs/book-links.md`](docs/book-links.md) 管理草稿連結，等 GitHub repo 建好後再替換成正式網址。
