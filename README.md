# 永錫 Agent Skill 庫

用 Desktop 概念幫助知識工作者：**Agent 高效率，人腦慢生活**。

## 指揮官入口

先看這裡：**[`Hermes.md`](Hermes.md)**

`Hermes.md` 是這個 repo 的指揮官，負責統一調度時間管理、卡片筆記、Agent Skill 與 Desktop 工作桌。

這個 repo 收納可安裝、可分享、可放進新書連結的 Codex Skills。它不是單純工具箱，而是一套 Hermes HyperCard Loop：把時間管理、卡片筆記、Agent Skill、Desktop 工作桌連成一個知識工作系統。

## Hermes HyperCard Loop

### 指揮官：[`Hermes.md`](Hermes.md)

核心循環：

```text
人腦慢想
  -> 卡片整理
  -> Agent 執行
  -> Skill 沉澱
  -> GitHub 分享
  -> 書籍連結
  -> 回到 Desktop 日常
```

四軸總控台：**[`Hermes.md`](Hermes.md)**

## 四軸首頁

### 1. 時間管理軸

把「今天、本週、長期訓練、新書進度」整理成可執行節奏。

- [`skills/imandalart/`](skills/imandalart/)：每日重心、章節重心、手機九宮卡。
- [`skills/personal-athlete-81-grid/`](skills/personal-athlete-81-grid/)：長期目標與 8+64 行動展開。

### 2. 卡片筆記軸

把文章、筆記、索引、章節拆成可連結、可出版的知識卡片。

- [`skills/fire-analysis-card/`](skills/fire-analysis-card/)：用 FIRE 分析中文文章。
- [`skills/imandalart/`](skills/imandalart/)：把概念壓成 3x3 方形索引卡。
- [`skills/markdown-nine-grid-clipboard/`](skills/markdown-nine-grid-clipboard/)：輸出 Obsidian、AIDA、GitHub 可讀的 Markdown 九宮格。
- [`skills/obsidian-graph-view/`](skills/obsidian-graph-view/)：把關鍵字、章節、卡片做成 Obsidian 風格 graph。

### 3. Agent 軸向

把反覆發生的工作沉澱成 Codex Skill，讓 Agent 記得流程、格式、驗證方式。

- [`skills/project-note-json-to-epub/`](skills/project-note-json-to-epub/)：把 project-note JSON 變成可驗證 EPUB。
- [`skills/fire-card-to-epub/`](skills/fire-card-to-epub/)：把 FIRE 分析卡或 project-note JSON 變成可驗證 EPUB。
- [`skills/epub-hypercard-obsidian/`](skills/epub-hypercard-obsidian/)：把 EPUB 卡片書轉成 Obsidian HyperCard 資料夾。
- [`docs/skill-index.md`](docs/skill-index.md)：Skill 索引。

### 4. Desktop 軸向

把 Agent 之外的工作桌納入系統：ChatGPT、Codex、Obsidian、AIDA、Bike、Finder、VS Code、紙本、手機、桌面硬體。

Desktop 軸的重點不是更多工具，而是降低切換成本：

- 快速轉換交給 Agent。
- 深層判斷留給人腦。
- 長期記憶交給卡片系統。
- 公開分享交給 GitHub。
- 慢想、重讀、畫線、沉澱交給紙本與桌面環境。

## Core Skills

### 個人運動員81宮格

參考大谷翔平 81 宮格，產生可編輯 JSON 與大谷風格 SVG/PNG 的個人訓練圖。

入口：[`skills/personal-athlete-81-grid/`](skills/personal-athlete-81-grid/)

### FIRE 原則分析卡

以 Fact、Index、Relation、Encyclopedia 分析中文文章，適合書稿、筆記、研究材料。

入口：[`skills/fire-analysis-card/`](skills/fire-analysis-card/)

### FIRE 卡到 EPUB

把 FIRE 分析卡或專案筆記 JSON 轉成可驗證 EPUB，支援目錄卡、章節卡、關鍵詞索引卡與回鏈驗證。

入口：[`skills/fire-card-to-epub/`](skills/fire-card-to-epub/)

### iMandalArt 九宮卡

產生手機可讀的 3x3 方形索引卡，用於 Hermes、Discord、章節卡、每日重心。

入口：[`skills/imandalart/`](skills/imandalart/)

### Markdown / Obsidian 九宮格

把素材、iMandalArt 或八領域草稿轉成 Markdown 3x3 表格，可貼到 Obsidian、AIDA、GitHub。

入口：[`skills/markdown-nine-grid-clipboard/`](skills/markdown-nine-grid-clipboard/)

### Obsidian Graph View

從 JSON、索引、TOC、卡片資料產生 Obsidian 風格關係圖。

入口：[`skills/obsidian-graph-view/`](skills/obsidian-graph-view/)

### Project Note JSON 到 EPUB

把結構化專案筆記 JSON 轉成可驗證 EPUB，支援章節目錄、索引卡、雙向連結。

入口：[`skills/project-note-json-to-epub/`](skills/project-note-json-to-epub/)

### EPUB 到 HyperCard / Obsidian

把 EPUB 卡片書轉成可跳轉的 Obsidian HyperCard Markdown folder 與 zip。

入口：[`skills/epub-hypercard-obsidian/`](skills/epub-hypercard-obsidian/)

## Install Locally

從 repo 根目錄把需要的 Skill 複製到 Codex skills 目錄：

```bash
cp -R skills/personal-athlete-81-grid ~/.codex/skills/
cp -R skills/fire-analysis-card ~/.codex/skills/
cp -R skills/imandalart ~/.codex/skills/
cp -R skills/markdown-nine-grid-clipboard ~/.codex/skills/
cp -R skills/obsidian-graph-view ~/.codex/skills/
cp -R skills/project-note-json-to-epub ~/.codex/skills/
cp -R skills/fire-card-to-epub ~/.codex/skills/
cp -R skills/epub-hypercard-obsidian ~/.codex/skills/
```

更多說明：[`docs/install.md`](docs/install.md)

## Book Links

新書可連到固定 GitHub URL：

```text
https://github.com/twhsi/skills
```

每章延伸工具整理在：[`docs/book-links.md`](docs/book-links.md)

書中可用句型：

```markdown
本章延伸 Skill: https://github.com/twhsi/skills/tree/main/skills/imandalart
```

## Repo Layout

```text
skills/      正式、可安裝、可分享的 Skills
docs/        安裝說明、書籍連結、索引與操作文件
examples/    每個 Skill 的輸入、輸出、測試樣本
archive/     舊版、草稿、暫不公開或已退役的 Skill
Hermes.md    四軸管理總控台
README.md    GitHub 首頁與讀者入口
```

## Maintain

建議每次修改 Skill 後驗證：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/fire-card-to-epub
```

每週用 [`Hermes.md`](Hermes.md) 裡的 Weekly Hermes Sync 檢查：哪些 Skill 要升級、補範例、移到 archive，或變成新書章節連結。
