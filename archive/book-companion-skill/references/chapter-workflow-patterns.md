# Chapter Workflow Patterns

Use these patterns to turn book material into companion prompts, Skill drafts, and GitHub link targets.

## Stable Slugs

Use lowercase English slugs for filenames and anchors when possible:

- `chapter-01-thinking-with-skills.md`
- `exercise-03-nine-grid-review.md`
- `skill-card-book-companion.md`

Keep the reader-facing title in Chinese or bilingual text when that matches the book.

## Reader Prompt Checklist

Every reader prompt should answer:

- What should the reader paste into Codex?
- What material should the reader provide?
- What should Codex produce?
- Should Codex ask questions or proceed directly?
- What constraints from the book matter for the result?

## GitHub Companion README Pattern

Use this sequence for a book companion repo:

1. State what the repo is for.
2. Link to the Skill folder.
3. Show the fastest install/use path.
4. List chapter companion prompts.
5. Add a note about versioning and reader feedback.

## Book Link Pattern

For printed books and e-books, prefer one stable URL per chapter or companion page. Avoid linking directly to local files, branch-only files that may move, or raw generated assets without context.

Recommended link text:

```markdown
Companion Skill: <GitHub repo URL>
Chapter prompt: <GitHub repo URL>#chapter-x
```

## Exercise Upgrade Pattern

When rewriting a chapter exercise for Codex, preserve the learning objective and make the execution explicit:

```markdown
Use this exercise to help me <goal>. I will provide <input>. Produce <output>. Keep the result suitable for <audience/context>. Ask at most two clarifying questions only if the task cannot proceed.
```
