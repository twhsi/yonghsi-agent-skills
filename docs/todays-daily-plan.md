# 今日的日計畫教學

`今日的日計畫` 是一個把口語內容寫進 Obsidian Mandala Grid 日計劃的 Skill。它的核心關鍵字是：青蛙、日計劃、日計畫、九宮、時段、日記。

## 它解決什麼

你每天只要用嘴巴說：

```text
今日的日計畫，上午羽球，下午三點林君，日記 Miru 來訪，狀況不是很好，加油。
```

Codex 會把內容分配到今天的九宮時段：

- `09-12`: 羽球
- `15-18`: 林君
- `日記`: 下一個編號日記項目

## Obsidian 檔案格式

目標檔案需要是 Mandala Grid 的日計畫格式：

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

每天是一個 `<!--section: N-->`，當天八格是 `N.1` 到 `N.8`。Skill 不會重排整份日計劃，只會補齊今天需要的八格並追加內容。

## 口語範例

```text
今日的日計畫，早上日文課，中午領午餐，晚上合唱團。
```

```text
🐸 晚上耿彬 Hermes＋Codex 活動。
```

```text
補今天日記：Esor 討論到建立 Desktop 案例放入書中，還有 Prompt 的重要。
```

```text
今天 18:30 管委會，放到 18-19。
```

## 完整台詞範例

```text
[$todays-daily-plan](/Users/twhsi/.codex/skills/todays-daily-plan/SKILL.md)
請做 2026-06-19 五 的日計畫：
09-12 準備晚上直播投影片。
13-15 14:00 小睦到達。
18-19 晚上和小睦一起吃披薩。
19-21 20:00 騰訊直播，主題：Hermes、Skill Loops、GitHub。
```

寫入後會落在同一天的這些 Mandala Grid section：

```md
<!--section: 170.2-->
### 09-12
準備晚上直播投影片

<!--section: 170.4-->
### 13-15
14:00 小睦到達

<!--section: 170.6-->
### 18-19
晚上和小睦一起吃披薩

<!--section: 170.7-->
### 19-21
20:00 騰訊直播，主題：Hermes、Skill Loops、GitHub
```

如果一次只寫了一部分，再說「繼續」時，Skill 會先檢查當天 section，已存在的文字不重複追加，只補尚未寫入的時段。

## 手動測試腳本

從 Skill 目錄執行：

```bash
python3 scripts/update_today_plan.py \
  --file "/Users/twhsi/+ 02 Area_Mandlal Diary 曼陀羅手帳/00 Daily/1.a 2026 日計劃.md" \
  --date 2026-06-18 \
  --slot "09-12" \
  --text "羽球"
```

不加 `--apply` 只會預覽 JSON 摘要。要真正寫入：

```bash
python3 scripts/update_today_plan.py \
  --file "/Users/twhsi/+ 02 Area_Mandlal Diary 曼陀羅手帳/00 Daily/1.a 2026 日計劃.md" \
  --date 2026-06-18 \
  --slot "日記" \
  --text "今天完成了今日的日計畫 Skill，正式進入 GitHub 技能庫。" \
  --kind diary \
  --apply
```

如果同一格同一句已存在，腳本會回報：

```json
{
  "duplicate_skipped": true,
  "changed": false,
  "applied": true
}
```

## 安裝

```bash
cp -R skills/todays-daily-plan ~/.codex/skills/
```

下次對 Codex 說：

```text
Use $todays-daily-plan 今日的日計畫，幫我把剛剛口述的事情放進今天九宮時段和日記。
```
