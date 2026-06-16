---
name: imandalart
description: Design iMandalArt and iMandala 3x3 square index cards. Default output is iMandala 1.0: no visible borders, no vertical dividers, no Markdown table, exactly five counted characters per visible cell row, and an ◎ center. Use when the user asks for iMandalArt, iMandala, I MandalArt, 五字定格, 無框九宮, ◎中心, 手機方形曼陀羅, 正方形九宮索引卡, or a square 3x3 card that is not an 81-cell Mandala.
---

# iMandalArt

## Hard Default

When the user asks for iMandalArt or iMandala, always default to iMandala 1.0:

- No visible borders.
- No vertical divider characters.
- No Markdown table.
- Exactly five counted characters per visible cell row.
- A quiet ◎ in the center cell.
- A square 3x3 body formed by spacing and rhythm, not by frames.

This default overrides older PE2, terminal, boxed, Discord-safe, and Markdown-table habits.

Use framed PE2-style output only when the user explicitly asks for borders, PE2, terminal frame, boxed text, or renderer debugging.

## Purpose

Use this skill to create one square 3x3 index card for Discord, Hermes, Codex, notes, or phone reading.

iMandalArt is:

- One center idea.
- Eight surrounding vectors.
- A phone-readable square card.
- A compact thinking object, not a spreadsheet.

It is not:

- A Markdown table.
- An 81-cell Mandala.
- A long article.
- A bordered terminal UI unless explicitly requested.

## Five-Character Counting

Each visible cell row must contain exactly five counted characters.

For this mode, count each CJK character, kana, English letter, digit, punctuation mark, symbol, full-width space, and half-width space as one character.

Good five-character rows:

```text
觸 發 源
輸入材料 
　 ◎ 　
下一技能 
```

Bad rows:

```text
觸發
輸入材料來源
◎
```

Fix short rows with deliberate spacing. Fix long rows by compressing the wording.

## Default Structure

Use this spatial meaning unless the user gives a different map:

```text
觸 發 源　　輸 入 物　　辨 識 法
輸 出 形　　 ◎ 　　流 程 線
保 存 處　　避 免 事　　下 一 步
```

Position logic:

- Top left: trigger, origin, or entry point.
- Top center: input, source, or material.
- Top right: recognition, pattern, or diagnosis.
- Middle left: output, result, or expression.
- Center: core concept, goal, or question.
- Middle right: process, method, or workflow.
- Bottom left: storage, memory, or evidence.
- Bottom center: constraint, risk, or what to avoid.
- Bottom right: next action, next skill, or future path.

## Default Output

Return the no-frame card first in a fenced text block.

Use this pattern:

```text
[ 標題 ]

觸 發 源　　輸 入 物　　辨 識 法
從何開始　　材料入口　　看見模式
　　　　　素材入場　　判斷線索

輸 出 形　　 ◎ 　　流 程 線
成品樣貌　　 中　心 　　步驟節奏
看得見物　　 主　題 　　先後次序

保 存 處　　避 免 事　　下 一 步
留下證據　　不要混雜　　立刻行動
回到卡盒　　界線清楚　　接上技能
```

Each of the nine cells normally has three rows:

- Title row.
- Content row.
- Breath row.

The center cell may use more whitespace, but it must still contain ◎.

Do not include a Markdown table as the default answer.

## Writing Style

- Use compact Chinese labels when the user writes in Chinese.
- Write like Palm launcher labels or index-card labels.
- Avoid explanations inside cells.
- Put any explanation below the card.
- Keep the center specific.
- Do not output Markdown table structure unless the user explicitly asks for Markdown.
- Do not output framed text unless the user explicitly asks for a frame.

## Quality Gate

Before replying, check:

- There are exactly nine cells.
- The center includes ◎.
- Every visible cell row is five counted characters.
- The card contains no visible frame.
- The card contains no Markdown table.
- The card fits phone reading.
- The final answer starts with the card, not with explanation.

## If The User Says You Forgot

Immediately correct the output into iMandala 1.0:

- Remove all frames.
- Remove all Markdown table structure.
- Recompress every cell row to five counted characters.
- Keep ◎ in the center.
- Return only the corrected card unless a brief apology is necessary.

