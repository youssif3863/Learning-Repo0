# Records, files and utility (Stage 1)

Keep a task-private JSONL journal. Each line is one occurrence:

`exam`, `position` (positive integer in source order), `stem`, `choices` (ordered objects with `label` and `text`), `answer` and `explanation` (string or null), `answerExplicit` (boolean), `source` (non-sensitive locator), `group` (optional shared passage ID), `passage` (optional), `images` (relative paths), `issues` (strings).

Do not include account IDs, tokens, cookies or sensitive URL parameters in `source`. A stable path-free page description is sufficient. Number labels belong in `position`, not `stem`; remove only an actual leading question label during capture. Do not apply broad number-removal regexes to medical content. Preserve tables and meaningful whitespace in text fields. Mark a failed image as an issue containing `Required source image not captured` rather than inserting a remote authenticated URL.

Commands (paths are examples, not fixed output destinations):

```
node scripts/bank.cjs ingest journal.jsonl captured-record.json
node scripts/bank.cjs export journal.jsonl output-directory assets/config.json
node scripts/bank.cjs recover journal.jsonl
node scripts/test.cjs
```

Ingest validates and appends before reporting success; retries do not append duplicates. A torn final JSON line is ignored for recovery and reported. Ingest refuses to append until that torn journal is repaired from its valid prefix into a NEW file. A malformed nonfinal line or changed occurrence is an error.

Export refuses to reuse an existing output directory. It writes:
- `exam_N.md` — one immutable source file per exam: original order, original option labels, unnumbered headings, null fields shown as “Not displayed by the source.”
- `questions_shuffled.md` — **the Stage 1 deliverable and Stage 2 input**: whole groups shuffled (passage groups stay together), options shuffled inside each question and relabelled A, B, C…, no question numbers, the source answer remapped to the new labels. A question keeps its source option order (and is listed in the audit with the reason) when its options are position-dependent (“all of the above”, “A and C”), its stem or explanation refers to option letters, or its source answer cannot be mapped to a label.
- `collection_audit.md` — counts per exam, missing positions, issues, exact duplicates (never removed; similar questions need manual semantic review), answer/explanation gaps, and the per-question option order.

Config (`assets/config.json`): `expected` maps exact titles to counts; `date` and `sourceLocation` describe the capture; `shuffle` (default true), `shuffleOptions` (default true) and `seed` govern `questions_shuffled.md`. There is deliberately no option for AI-generated or supplementary questions; a config that names `supplements` is rejected.

## `questions_shuffled.md` format (parsed by Stage 2)

```
# Shuffled question set
Captured: … · Source: … · Questions: N
Exam index: e1 = <exam title>; e2 = …
---
## Question
<!-- id: e1-p7; group: passage1 -->
> **Passage** — optional shared passage (blockquote)
Stem text (may span lines or contain a table)
A. option text␠␠
B. option text
![Source figure](assets/fig.png)
**Source answer:** C        (remapped to the new labels, or “Not displayed by the source.”)
**Source explanation:** …
---
```
`id` = exam index + original position (provenance without visible numbering). Image paths resolve beneath the Markdown file's folder. Output paths are relative to each Markdown file. Missing images and counts remain visible in the audit; an export existing is not proof of source completion. Keep source exports immutable when building Stage 2 files.
