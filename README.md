# 永錫 Agent Skill 庫

> 知識工作者的第二大腦系統：Agent 高效率，人腦慢生活。

[![Hermes All Skills Map](assets/hermes-all-skills-map.png)](assets/hermes-all-skills-map.png)

## 指揮官入口

先看這裡：**[`Hermes.md`](Hermes.md)**

`Hermes.md` 是這個 repo 的指揮官，負責統一調度時間聚焦、卡片筆記、Agent Skill、Desktop 工作桌與新書連結。這裡不是單純工具箱，而是一套 Hermes HyperCard Loop：把「收集 → 結構化 → 連結 → 輸出 → 迭代」變成可重複的知識工作流程。

## FIRE 總整理

```text
　　　　　　　　　　【Ⓕ Fact 事實】
　　　　　　　　　　定義：技能總圖
　　　　　　　　　　主張：人機分工
　　　　　　　　　　證據：八類入口


　　　　　↗　　　　　　　　　　　　　　　↘
　　【Ⓘ Index】　　　中【◎核心】　　　【Ⓡ Relation】
　　　重新入口　　　　◎技能中樞　　　　關係網絡
　　　────────　────────　────────
　　　Hermes.md　　　All Skills　　　　時間聚焦
　　　四軸首頁　　　　知識工作　　　　　卡片成書
　　　書籍連結　　　　慢快分工　　　　　Agent沉澱


　　　　　↖　　　　　　　　　　　　　　　↙
　　　　　　　　　　【Ⓔ Encyclopedia】
　　　　　　　　　　概念：技能作業系統
　　　　　　　　　　用途：書稿到桌面
　　　　　　　　　　判斷：人留慢想
```

**F｜Fact**

- 這個 repo 管理多個可安裝 Codex Skills，核心是 `Hermes.md`。
- 圖中把技能分成時間聚焦、FIRE 分析、Graph 視圖、九宮卡片、Agent Skill、EPUB 出版、HyperCard 回流、書籍連結。
- 北極星是「快交給 Agent，慢留給人」。

**I｜Index**

- 入口頁：[`Hermes.md`](Hermes.md)
- 書籍連結：[`docs/book-links.md`](docs/book-links.md)
- Skill 索引：[`docs/skill-index.md`](docs/skill-index.md)

**R｜Relation**

- 時間管理產生每日焦點，九宮卡把焦點壓成可讀卡片。
- FIRE 抽取知識骨架，Graph view 建立章節與關鍵字關係。
- JSON、EPUB、HyperCard、Obsidian 形成「出版 → 回流 → 再整理」循環。

**E｜Encyclopedia**

Hermes All Skills 是一個知識工作者的技能作業系統。它把人的慢思考、桌面工作流、Codex Agent、自動化腳本、GitHub 分享與書籍連結放在同一張圖裡，讓每個 Skill 都不是孤立工具，而是能回到日常、書稿與知識庫的循環節點。

## 八個入口

| # | 入口 | 作用 | Skill |
|---|---|---|---|
| 1 | 時間聚焦 | 今日、本週、長期訓練與章節重心 | [`imandalart`](skills/imandalart/), [`personal-athlete-81-grid`](skills/personal-athlete-81-grid/) |
| 2 | FIRE 分析 | Fact / Index / Relation / Encyclopedia | [`fire-analysis-card`](skills/fire-analysis-card/) |
| 3 | Graph 視圖 | 關鍵字、章節、卡片關係圖 | [`obsidian-graph-view`](skills/obsidian-graph-view/) |
| 4 | 九宮卡片 | 邏輯想法、手機可讀、Markdown 九宮 | [`imandalart`](skills/imandalart/), [`markdown-nine-grid-clipboard`](skills/markdown-nine-grid-clipboard/) |
| 5 | Agent Skill | Prompt → JSON → Codex → Hermes | [`docs/skill-index.md`](docs/skill-index.md) |
| 6 | EPUB 出版 | 卡片成書、Project Note、JSON → EPUB | [`project-note-json-to-epub`](skills/project-note-json-to-epub/) |
| 7 | HyperCard 回流 | EPUB → 卡片盒 → Obsidian → 知識循環 | [`epub-hypercard-obsidian`](skills/epub-hypercard-obsidian/) |
| 8 | 書籍連結 | 書中 QR、章節工具入口、Companion Docs | [`docs/book-links.md`](docs/book-links.md) |

## 四軸首頁

### 1. 時間管理軸

把「今天、本週、長期訓練、新書進度」整理成可執行節奏。

- [`skills/imandalart/`](skills/imandalart/)：每日重心、章節重心、手機九宮卡。
- [`skills/personal-athlete-81-grid/`](skills/personal-athlete-81-grid/)：長期目標與 8+64 行動展開。
- [`skills/fantastical-calendar/`](skills/fantastical-calendar/)：把 Codex 的會議、時段與提醒送進 Fantastical。

### 2. 卡片筆記軸

把文章、筆記、索引、章節拆成可連結、可出版的知識卡片。

- [`skills/fire-analysis-card/`](skills/fire-analysis-card/)：用 FIRE 分析中文文章。
- [`skills/imandalart/`](skills/imandalart/)：把概念壓成 3x3 方形索引卡。
- [`skills/markdown-nine-grid-clipboard/`](skills/markdown-nine-grid-clipboard/)：輸出 Obsidian、AIDA、GitHub 可讀的 Markdown 九宮格。
- [`skills/obsidian-graph-view/`](skills/obsidian-graph-view/)：把關鍵字、章節、卡片做成 Obsidian 風格 graph。

### 3. Agent 軸向

把反覆發生的工作沉澱成 Codex Skill，讓 Agent 記得流程、格式、驗證方式。

- [`skills/project-note-json-to-epub/`](skills/project-note-json-to-epub/)：把 project-note JSON 變成可驗證 EPUB。
- [`skills/epub-hypercard-obsidian/`](skills/epub-hypercard-obsidian/)：把 EPUB 卡片書轉成 Obsidian HyperCard 資料夾。
- [`docs/skill-index.md`](docs/skill-index.md)：Skill 索引。

### 4. Desktop 軸向

把 Agent 之外的工作桌納入系統：ChatGPT、Codex、Obsidian、AIDA、Bike、Finder、VS Code、紙本、手機、桌面硬體。

- 快速轉換交給 Agent。
- 深層判斷留給人腦。
- 長期記憶交給卡片系統。
- 公開分享交給 GitHub。
- 慢想、重讀、畫線、沉澱交給紙本與桌面環境。

## Install Locally

從 repo 根目錄把需要的 Skill 複製到 Codex skills 目錄：

```bash
cp -R skills/fire-analysis-card ~/.codex/skills/
cp -R skills/imandalart ~/.codex/skills/
cp -R skills/markdown-nine-grid-clipboard ~/.codex/skills/
cp -R skills/obsidian-graph-view ~/.codex/skills/
cp -R skills/personal-athlete-81-grid ~/.codex/skills/
cp -R skills/project-note-json-to-epub ~/.codex/skills/
cp -R skills/epub-hypercard-obsidian ~/.codex/skills/
cp -R skills/fantastical-calendar ~/.codex/skills/
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

## Website

這個 repo 也可以部署成免費的 Agent-first website：

- Source：`site/`
- Build：`npm run build`
- Output：`dist/`
- Agent endpoints：`/agent.json`、`/skills.json`、`/llms.txt`
- Free deploy：GitHub repo -> Vercel build -> Cloudflare DNS

Vercel 設定已放在 [`vercel.json`](vercel.json)：build command 使用 `npm run build`，output directory 使用 `dist`。

## Repo Layout

```text
assets/      首頁圖像與公開展示素材
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
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/imandalart
```

每週用 [`Hermes.md`](Hermes.md) 裡的 Weekly Hermes Sync 檢查：哪些 Skill 要升級、補範例、移到 archive，或變成新書章節連結。
