# 永錫 Agent Skill 庫

這個資料夾整理已成熟、可分享、可放進 GitHub，也適合在新書中連結引用的 Codex Skills。

## Featured Skill：今日的日計畫

[`今日的日計畫`](skills/todays-daily-plan/) 是這個 repo 目前主打的正式 Skill。它專門服務 Obsidian 的 Mandala Grid 日計畫檔：當你用口語說「上午羽球」「下午三點林君」「晚上合唱」「補今天日記」時，Codex 會把內容分配到今天的九宮時段，並安全追加到正確的 `<!--section: N.x-->` 區塊。

這個 Skill 的關鍵字是：`青蛙`、`日計劃`、`日計畫`、`九宮`、`時段`、`日記`、`Mandala Grid`。它特別適合每天早上或晚上用嘴巴整理一天，不需要手動在 Markdown 裡找今天的 section。

它會做三件事：

- 找到今天在年度日計畫中的 section，例如 `2026-06-18` 是 `169`。
- 補齊今天的 8 個九宮格時段：`陽光起床運動`、`09-12`、`12-13`、`13-15`、`15-18`、`18-19`、`19-21`、`日記`。
- 只追加到目標時段或日記，不重排全年檔案，不破壞 Mandala Grid 的 section marker。

快速說法：

```text
Use $todays-daily-plan 今日的日計畫，上午羽球，下午三點林君，日記 Miru 來訪，狀況不是很好，加油。
```

正式 Skill：[`skills/todays-daily-plan/`](skills/todays-daily-plan/)  
完整教學：[`docs/todays-daily-plan.md`](docs/todays-daily-plan.md)

## Hermes HyperCard Loop

![Hermes HyperCard Loop](assets/hermes-four-axis-nonoverlap.svg)

這張圖說明目前核心技能在 Hermes Loop 中的位置：時間管理、卡片盒、Skill tree 與 Agent 四條軸如何交會。

## Core Skills

| Skill | 用途 | 入口 |
|---|---|---|
| 今日的日計畫 | 用青蛙口語把今天的日計劃寫入 Obsidian Mandala Grid 九宮時段與日記 | [`skills/todays-daily-plan/`](skills/todays-daily-plan/) |
| 個人運動員81宮格 | 參考大谷翔平 81 宮格，產生可編輯 JSON 與大谷風格 SVG 的個人運動員訓練圖 | [`skills/personal-athlete-81-grid/`](skills/personal-athlete-81-grid/) |
| 自動魯曼編號機 | 為書稿與卡片盒分配魯曼式編號，清理公開案例 catalog，並附 EPUB 使用手冊 | [`skills/auto-luhmann-numberer/`](skills/auto-luhmann-numberer/) |
| JSON 到 EPUB | 把結構化專案筆記 JSON 轉成可驗證的 EPUB | [`skills/project-note-json-to-epub/`](skills/project-note-json-to-epub/) |
| Graph view | 從 JSON、索引、TOC、卡片資料產生 Obsidian 風格關係圖 | [`skills/obsidian-graph-view/`](skills/obsidian-graph-view/) |
| 九宮格 / iMandalArt | 產生九宮格、曼陀羅卡、Hermes/Discord 文字卡 | [`skills/imandalart/`](skills/imandalart/) |
| Markdown / Obsidian 九宮格 | 把素材、iMandalArt 或八領域草稿轉成可在 Obsidian、AIDA、GitHub 渲染的 Markdown 九宮表格 | [`skills/markdown-nine-grid-clipboard/`](skills/markdown-nine-grid-clipboard/) |
| FIRE 原則 | 以 Fact、Index、Relation、Encyclopedia 分析中文文章 | [`skills/fire-analysis-card/`](skills/fire-analysis-card/) |
| PDCA / CAPD 方位卡 | 把問題、事件、決策取捨轉成中文方位羅盤式 PDCA/CAPD 文字圖卡 | [`skills/pdca/`](skills/pdca/) |

## Repo Layout

```text
skills/      正式 Skills
docs/        GitHub、安裝、書籍連結說明
examples/    未來放每個 Skill 的輸入與輸出範例
archive/     舊版或暫不公開的 Skill 草稿
```

## Install Locally

把需要的 Skill 複製到 Codex skills 目錄：

```bash
cp -R skills/todays-daily-plan ~/.codex/skills/
cp -R skills/personal-athlete-81-grid ~/.codex/skills/
cp -R skills/auto-luhmann-numberer ~/.codex/skills/
cp -R skills/project-note-json-to-epub ~/.codex/skills/
cp -R skills/obsidian-graph-view ~/.codex/skills/
cp -R skills/imandalart ~/.codex/skills/
cp -R skills/markdown-nine-grid-clipboard ~/.codex/skills/
cp -R skills/fire-analysis-card ~/.codex/skills/
cp -R skills/pdca ~/.codex/skills/
```

更多說明見 [`docs/install.md`](docs/install.md)。

## For VS Code Editing

用 VS Code 開啟這個資料夾：

```bash
code .
```

建議每次修改後驗證 Skill：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/markdown-nine-grid-clipboard
```

## Book Links

未來新書可以把每個章節連到固定 GitHub URL。正式 repo：

https://github.com/twhsi/skills

書籍用連結整理在 [`docs/book-links.md`](docs/book-links.md)。
