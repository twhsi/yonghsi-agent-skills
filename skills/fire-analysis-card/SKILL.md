---
name: fire-analysis-card
description: "Analyze Chinese articles around 1000 characters with the FIRE principle: Fact, Index, Relation, and Encyclopedia. Use when Codex needs to turn an essay, reflection, transcript excerpt, research note, product note, or Obsidian/LLM knowledge material into a compact Chinese FIRE analysis card, encyclopedia-style note, or fixed-width text diagram inspired by PDCA card formatting."
---

# FIRE Analysis Card

Transform a short Chinese article, usually around 1000 characters, into a stable knowledge-analysis card using FIRE:

- `F = Fact`: extract atomic facts from the source.
- `I = Index`: create re-entry points, keywords, titles, and navigation hooks.
- `R = Relation`: identify how facts connect, support, challenge, revise, or extend each other.
- `E = Encyclopedia`: synthesize the facts and relations into a readable encyclopedia-style explanation.

The output should feel useful for Obsidian, LLM project files, and personal knowledge systems. Prefer compact Chinese phrases and stable concepts over promotional or interpretive prose.

## Core Rules

- Always render the main FIRE card in a fenced `text` code block.
- Use full-width spaces `　` for visual alignment.
- Use half-width spaces only inside English labels such as `Fact 事實`.
- Keep the center phrase at 8 Chinese characters or fewer, prefixed with `◎`.
- Prefer Chinese phrases of 4 to 8 characters in the card.
- Analyze the article rather than merely summarize it.
- Preserve the author's main claim, but rewrite it into encyclopedia-stable language.
- When source evidence is weak, mark it as `待證`, `推論`, or `需補例`.
- Render only one main card unless the user asks for explanation, debug spacing, or multiple versions.

## FIRE Meaning

- `Ⓕ Fact 事實`: atomic claims, observations, definitions, examples, data points, and explicit statements from the article.
- `Ⓘ Index 索引`: topic title, keywords, entry points, tags, one-line retrieval cues, and questions that help a reader return to the material.
- `Ⓡ Relation 關係`: causal links, contrast, support, tension, sequence, hierarchy, analogy, and missing bridges among facts.
- `Ⓔ Encyclopedia 百科`: a concise, coherent, reusable explanation that integrates the important facts and relations.

Use the flow:

`Raw Article -> Fact -> Index -> Relation -> Encyclopedia -> Human Judgment`

## Fixed Template

Copy this template first, then replace the phrases.

```text
　　　　　　　　　　【Ⓕ Fact 事實】
　　　　　　　　　　定義：＿＿＿＿
　　　　　　　　　　主張：＿＿＿＿
　　　　　　　　　　證據：＿＿＿＿


　　　　　↗　　　　　　　　　　　　　　　↘
　　【Ⓘ Index】　　　中【◎核心】　　　【Ⓡ Relation】
　　　重新入口　　　　◎＿＿＿＿　　　　關係網絡
　　　────────　────────　────────
　　　＿＿＿＿　　　　＿＿＿＿　　　　　＿＿＿＿
　　　＿＿＿＿　　　　＿＿＿＿　　　　　＿＿＿＿
　　　＿＿＿＿　　　　＿＿＿＿　　　　　＿＿＿＿


　　　　　↖　　　　　　　　　　　　　　　↙
　　　　　　　　　　【Ⓔ Encyclopedia】
　　　　　　　　　　概念：＿＿＿＿
　　　　　　　　　　用途：＿＿＿＿
　　　　　　　　　　判斷：＿＿＿＿
```

## Compass Mapping

- Top `Ⓕ Fact`: what the article explicitly provides as material.
- Left `Ⓘ Index`: how future readers or LLMs can find and re-enter this material.
- Right `Ⓡ Relation`: how facts interact and what relationship lines matter.
- Bottom `Ⓔ Encyclopedia`: the reusable knowledge page distilled from the source.
- Center `◎核心`: the article's knowledge object, not its mood or slogan.

Arrow meanings:

- `↘` means Fact -> Relation: facts become relationship material.
- `↙` means Relation -> Encyclopedia: relations become readable explanation.
- `↖` means Encyclopedia -> Index: finished notes create better entry points.
- `↗` means Index -> Fact: entry points guide future fact collection.

## Construction Workflow

1. Read the article once for topic and stance.
2. Extract the center `◎核心詞` in 8 Chinese characters or fewer.
3. Fill `Ⓕ Fact` with definition, main claim, and strongest evidence.
4. Fill `Ⓘ Index` with retrieval handles: title, tags, questions, or adjacent concepts.
5. Fill `Ⓡ Relation` with three relationship lines such as `因果`, `對比`, `支撐`, `修正`, `延伸`, or `缺口`.
6. Fill `Ⓔ Encyclopedia` with concept, use case, and human judgment.
7. Compress long phrases before widening the layout.
8. If the user asks for a full analysis, add a short prose section after the card with `Fact / Index / Relation / Encyclopedia` bullets.

## 1000-Character Article Handling

For an article around 1000 Chinese characters:

- Extract 3 to 7 atomic facts, but put only the best 3 into the card.
- Create 3 index handles: one title-like entry, one tag-like entry, and one question-like entry.
- Create 3 relation lines: one internal relation, one external relation, and one missing or risky relation.
- Write encyclopedia language as if it were an Obsidian concept page: neutral, reusable, and revisable.
- Do not quote long passages. Convert source wording into compact knowledge units.

## Phrase Compression

Prefer concise compounds:

- `從原始資料中抽取可以獨立存在的最小知識單位` -> `原子事實`
- `讓使用者重新找到資料的入口` -> `重返入口`
- `事實與事實之間互相支持或修正` -> `事實連線`
- `把事實與關係寫成可閱讀頁面` -> `百科成頁`
- `最後仍然需要人的判斷` -> `人定判斷`

## Full Analysis Add-On

If the user asks for more than a card, append this compact structure after the `text` card:

```markdown
**F｜Fact**
- ...

**I｜Index**
- ...

**R｜Relation**
- ...

**E｜Encyclopedia**
...

**人工判斷**
- ...
```

Keep this add-on short unless the user asks for a long encyclopedia entry.

## Visible Spacing Debug

If the user asks for a visible spacing version, show a second debug block where:

- `□` means one full-width space `　`.
- `·` means one half-width space.

Visible debug example:

```text
□□□□□□□□□□【Ⓕ·Fact·事實】
□□□□□□↗□□□□□□□□□□□□□□□□□↘
□□【Ⓘ·Index】□□□中【◎核心】□□□【Ⓡ·Relation】
□□□重新入口□□□□◎知識成頁□□□□關係網絡
```

## Example

```text
　　　　　　　　　　【Ⓕ Fact 事實】
　　　　　　　　　　定義：四層流程
　　　　　　　　　　主張：知識生產
　　　　　　　　　　證據：事實關係


　　　　　↗　　　　　　　　　　　　　　　↘
　　【Ⓘ Index】　　　中【◎核心】　　　【Ⓡ Relation】
　　　重新入口　　　　◎知識成頁　　　　關係網絡
　　　────────　────────　────────
　　　FIRE原則　　　　火種成頁　　　　　事實供料
　　　知識管理　　　　入口可返　　　　　關係綜合
　　　LLM Wiki　　　　人定判斷　　　　　百科修正


　　　　　↖　　　　　　　　　　　　　　　↙
　　　　　　　　　　【Ⓔ Encyclopedia】
　　　　　　　　　　概念：知識流程
　　　　　　　　　　用途：Obsidian
　　　　　　　　　　判斷：人機分工
```
