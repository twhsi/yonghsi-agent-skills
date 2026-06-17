# Hermes.md

永錫 Agent Skill 庫的管理總控台。

中心思想：

> 用 Desktop 概念幫助知識工作者讓 Agent 高效率運轉，讓人腦回到慢生活。

Hermes 不是另一個工具清單，而是一個「桌面作業系統」：把時間、卡片、Agent、桌面環境放在同一張工作地圖上。GitHub repo 是公開倉庫；Hermes.md 是這個倉庫的操作面板。

## 0. North Star

知識工作者不是要把自己變成更快的機器，而是要把「快」交給 Agent，把「慢」留給人。

Hermes 的任務：

- 讓 Skill 變成可安裝、可分享、可驗證的工作模組。
- 讓卡片筆記變成可搜尋、可連結、可出版的知識結構。
- 讓時間管理從待辦清單升級為節奏管理。
- 讓 Desktop 重新成為人腦、紙本、App、硬體與 Agent 協作的工作桌。

## 1. Four Axes

### 1.1 時間管理軸

時間管理軸處理「今天、這週、這本書、這個人生階段」。

核心問題：

- 現在該收斂還是展開？
- 哪些任務應該交給 Agent？
- 哪些事情應該留給紙本、散步、睡眠、慢想？
- 哪些輸出需要成為下一個 Skill？

目前 repo 對應：

| 用途 | Skill / 文件 | 角色 |
|---|---|---|
| 每日/每週聚焦 | [`skills/imandalart/`](skills/imandalart/) | 用九宮卡壓縮當下重點 |
| 長期訓練圖 | [`skills/personal-athlete-81-grid/`](skills/personal-athlete-81-grid/) | 把目標拆成 8+64 行動 |
| 閱讀/寫作節奏 | [`docs/book-links.md`](docs/book-links.md) | 讓章節和 Skill 有固定入口 |

時間管理軸的原則：

- 用九宮格做「今日重心」，不用長清單耗損注意力。
- 用 81 宮做「長期訓練」，不用單日情緒決定人生方向。
- 用 GitHub link 做「書籍節奏」，讓每一章有可回訪的工具入口。

### 1.2 卡片筆記軸

卡片筆記軸處理「知識如何被拆小、命名、連結、再出版」。

核心問題：

- 這段內容的最小知識單位是什麼？
- 它應該成為 FIRE 卡、九宮卡、Obsidian graph，還是 EPUB/HyperCard？
- 它如何回到書、repo、桌面 App 和 Agent 工作流？

目前 repo 對應：

| 卡片層級 | Skill | 角色 |
|---|---|---|
| 單篇文章分析 | [`skills/fire-analysis-card/`](skills/fire-analysis-card/) | Fact / Index / Relation / Encyclopedia |
| 九宮索引卡 | [`skills/imandalart/`](skills/imandalart/) | 手機可讀的 3x3 思考物件 |
| Markdown 九宮 | [`skills/markdown-nine-grid-clipboard/`](skills/markdown-nine-grid-clipboard/) | Obsidian、AIDA、GitHub 可渲染表格 |
| 關係圖 | [`skills/obsidian-graph-view/`](skills/obsidian-graph-view/) | 把關鍵字、章節、卡片變成 graph |
| 書籍輸出 | [`skills/project-note-json-to-epub/`](skills/project-note-json-to-epub/) | 把 project-note JSON 變 EPUB |
| HyperCard 回流 | [`skills/epub-hypercard-obsidian/`](skills/epub-hypercard-obsidian/) | EPUB 轉 Obsidian Markdown 卡片堆疊 |

卡片筆記軸的流動：

```text
原始材料
  -> FIRE 分析
  -> 九宮索引
  -> Obsidian / AIDA / GitHub Markdown
  -> Graph view
  -> EPUB
  -> HyperCard / Obsidian 回流
```

### 1.3 Agent 軸向

Agent 軸向處理「哪些工作應該變成可重複的 Skill」。

核心問題：

- 這是一次性請求，還是應該沉澱成 Skill？
- 這個 Skill 的觸發句是否清楚？
- 它是否有可驗證的輸出？
- 它應該放在 `skills/`、`examples/`、`docs/`，還是 `archive/`？

Skill 生命週期：

```text
recipe -> prompt -> json -> codex -> hermes
```

| 階段 | 意義 | repo 位置 |
|---|---|---|
| recipe | 想法仍是自然語言配方 | `docs/` 或 issue 草稿 |
| prompt | 已可重複使用的提示詞 | `examples/` |
| json | 有固定輸入/輸出 schema | `examples/` 或 Skill assets |
| codex | 已成為 Codex Skill | `skills/` |
| hermes | 穩定、可路由、可放進總控台 | `Hermes.md` + README |

Agent 軸的原則：

- 每個 Skill 只做一件最小有用的事。
- `description` 要寫觸發場景，因為它是 Codex 是否載入 Skill 的入口。
- 每次修改後要跑 `quick_validate.py`。
- 重複使用三次以上，才考慮升級到 Hermes 核心視圖。

### 1.4 Desktop 軸向

Desktop 軸向處理「Agent 之外的整個工作桌」。

它包含：

- ChatGPT：對話、發想、草稿、問答。
- Codex Agent：讀檔、改檔、生成 Skill、驗證 repo。
- 紙本：慢想、畫圖、手寫索引、離線整理。
- App：Obsidian、AIDA、Bike、Finder、VS Code、瀏覽器。
- 桌面硬體：Mac、螢幕、鍵盤、滑鼠、掃描、列印、手機、平板。

Desktop 軸的中心不是硬體，而是「切換成本」。

高效率不是所有事都丟給 Agent，而是知道：

- 快速變形交給 Agent。
- 深層判斷交給人腦。
- 長期記憶交給卡片系統。
- 可公開分享的流程交給 GitHub。
- 需要身體節奏的事情交給紙本與桌面環境。

## 2. 8+1 Hermes Launcher

中心格是 Desktop Hermes OS，外圍八格代表目前 repo 的管理視圖。

| 時間聚焦 | FIRE 分析 | Graph 視圖 |
|---|---|---|
| 九宮卡片 | ◎ Desktop Hermes OS | Agent Skill |
| EPUB 出版 | HyperCard 回流 | 書籍連結 |

### Launcher Meaning

| 格位 | 管理問題 | 對應 |
|---|---|---|
| 時間聚焦 | 今天和本週最重要的是什麼？ | iMandalArt、81 宮 |
| FIRE 分析 | 這段材料的知識核心是什麼？ | FIRE Analysis Card |
| Graph 視圖 | 哪些概念正在連成網？ | Obsidian Graph View |
| 九宮卡片 | 如何把想法壓成可讀卡片？ | iMandalArt、Markdown 九宮 |
| Desktop Hermes OS | 人腦、Agent、App、紙本如何分工？ | 本文件 |
| Agent Skill | 哪些流程要變成可重複工具？ | `skills/` |
| EPUB 出版 | 哪些卡片可以成書？ | Project Note JSON to EPUB |
| HyperCard 回流 | 書如何回到卡片堆疊？ | EPUB HyperCard Obsidian |
| 書籍連結 | 哪些工具要讓讀者掃碼進入？ | `docs/book-links.md` |

## 3. Repo Operating Model

```text
skills/      正式、可安裝、可分享的 Skills
docs/        安裝說明、書籍連結、索引與操作文件
examples/    每個 Skill 的輸入、輸出、測試樣本
archive/     舊版、草稿、暫不公開或已退役的 Skill
Hermes.md    四軸管理總控台
README.md    GitHub 首頁與讀者入口
```

管理規則：

- 新 Skill 先進 `archive/` 或獨立草稿，穩定後再進 `skills/`。
- `skills/` 裡每個 Skill 都要有 `SKILL.md`。
- 能被新書引用的內容，要能從 `docs/book-links.md` 找到固定 URL。
- README 面向第一次來 GitHub 的讀者；Hermes.md 面向長期維護者與高階使用者。

## 4. Current Skill Map

| Skill | 主軸 | 副軸 | 狀態 | 下一步 |
|---|---|---|---|---|
| [`personal-athlete-81-grid`](skills/personal-athlete-81-grid/) | 時間管理 | Desktop / 卡片 | active | 可作為長期目標管理範例 |
| [`fire-analysis-card`](skills/fire-analysis-card/) | 卡片筆記 | Agent | active | 補 examples，展示中文文章分析 |
| [`imandalart`](skills/imandalart/) | 卡片筆記 | 時間管理 | active | 作為每日/章節九宮卡核心 |
| [`markdown-nine-grid-clipboard`](skills/markdown-nine-grid-clipboard/) | 卡片筆記 | Desktop | active | 強化 Obsidian/AIDA/GitHub 三用路徑 |
| [`obsidian-graph-view`](skills/obsidian-graph-view/) | 卡片筆記 | Desktop | active | 補 graph input/output example |
| [`project-note-json-to-epub`](skills/project-note-json-to-epub/) | 卡片筆記 | 出版/Desktop | active | 對接新書章節輸出 |
| [`epub-hypercard-obsidian`](skills/epub-hypercard-obsidian/) | 卡片筆記 | Desktop | lab | 補安裝與範例後升 active |

## 5. Book Link Strategy

這個 repo 不是只給工程師看，也要能放進新書。

書中連結分三層：

1. Repo 總入口：`https://github.com/twhsi/skills`
2. 章節工具入口：`https://github.com/twhsi/skills/tree/main/skills/<skill-name>`
3. 章節 companion 說明：`docs/book-links.md` 中的固定章節連結

書中句型：

```markdown
本章延伸 Skill: https://github.com/twhsi/skills/tree/main/skills/imandalart
```

或：

```markdown
下載永錫 Agent Skill 庫: https://github.com/twhsi/skills
```

## 6. Weekly Hermes Sync

每週用這份清單檢查 repo：

- 本週哪個 Skill 被使用三次以上？
- 哪個 Skill 的觸發語還不清楚？
- 哪個 Skill 應該補 example？
- 哪個 Skill 應該從 lab 升 active？
- 哪個 Skill 已被其他 Skill 取代，應移到 `archive/`？
- 哪個輸出適合放進新書章節？
- 哪個流程仍然太靠記憶，應該寫進 `SKILL.md`？

決策格式：

```markdown
## Weekly Hermes Sync - YYYY-MM-DD

Promote:
- 

Improve:
- 

Archive:
- 

Book Links:
- 

Next smallest change:
- 
```

## 7. Design Principles

### Agent 高效率

- 讓 Agent 做重複、轉換、驗證、輸出。
- 讓 Skill 承載流程記憶。
- 讓 GitHub 保存可分享版本。

### 人腦慢生活

- 人只保留方向、判斷、品味、關係與節奏。
- 紙本不是落後工具，而是減速器。
- Desktop 不是雜亂桌面，而是人和 Agent 的共同工作檯。

### 卡片作為中介

卡片是人腦慢想與 Agent 快速輸出之間的橋。

- 太長的文章先變 FIRE。
- 太散的念頭先變九宮。
- 太多的卡片變 graph。
- 成熟的卡片變 EPUB。
- 出版後再回流到 HyperCard / Obsidian。

## 8. Definition Of Done

一個 Skill 可以進入 Hermes 視圖，必須符合：

- 有清楚 `SKILL.md`。
- 有明確 trigger。
- 有至少一個可理解的使用情境。
- 能被 README 或 `docs/skill-index.md` 索引到。
- 能被 `docs/book-links.md` 或 GitHub URL 穩定引用。
- 修改後可通過基本驗證。

Hermes 的最終目標不是管理更多檔案，而是讓每一個檔案都知道自己在知識工作桌上的位置。
