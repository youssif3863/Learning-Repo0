# Stage 2 · answering and annotating

Goal: for every question a **correct answer checked against the user's book**, brief English + Arabic reasoning, a subject tag, a printed book page and an exact line to highlight. Work in chunks of ≤ 45 questions; keep text compact (cost matters).

## Loop (per chunk)
1. `stage2.py retrieve WORK A B` — questions A..B with the best book pages and a snippet each. Decide the answer from your own knowledge first, then confirm with the snippet.
2. Read the page (`stage2.py page WORK <pdf page>`) whenever there is doubt: “according to the book”, NOT/EXCEPT, numbers and cut-offs, classifications, regimens, anything that two options could both satisfy. Use `grep` for terms. Pages with no text layer (handwriting, figures) are listed by `index`; look at them with `page WORK N --png file.png` before deciding something is “not in the book”.
3. Write `WORK/answers/ans_NNN_MMM.json` (schema below) and run `stage2.py validate WORK`. Fix every error; read the warnings. Continue only when the chunk is clean.

## Rules of truth
- **A source answer is the key.** If the Markdown has `Source answer`, use it. If the book or standard references disagree, keep the source answer and add a `note` saying so (validate rejects a differing answer without a note).
- Without a source answer: the **book wins** for anything the book states; otherwise use standard references and say “not in the book” (`page: null`). Never invent a page or an anchor; validate checks both.
- **Never edit the question.** If the wording is broken (the correct option is missing, an option contradicts itself, the stem lacks the case it needs) choose the best available option and add a `note`. When exam-key teaching differs from modern practice, follow the key/book and say so in the note.
- NOT/EXCEPT questions: the reasons for options that are true statements begin with “True:”.
- Similar or duplicate questions get the same answer; keep them consistent.

## Pages and anchors
- `page`: the **printed** page number (bottom corner of the page), as a string — not the PDF index.
- `anchor`: a short distinctive phrase (≤ 8 words) that really exists on that page, plain ASCII punctuation (no curly quotes). It is highlighted green in Version 2 and the link lands on it. `exact: true`.
- Fact printed nowhere but the topic page exists (inside a figure, handwriting, implied): `exact: false`, anchor optional — Version 2 links to the nearest page without a highlight and lists it in Teacher notes.
- Not covered by the book: `page: null` (Version 2 shows “Not in the supplied book”).

## Style (both languages)
- `why`: ≤ ~25 words. `wrong[X]`: ≤ ~8 words each. `pearl`: one line — an exam tip, a related variant of the question, or the one fact worth saying aloud. Skip the pearl only for trivial questions.
- Arabic: concise Modern Standard Arabic; keep medical terms and drug names in Latin letters; avoid ending a sentence on a Latin word where possible; no decorative symbols.
- No numbering of questions anywhere.

## Subject tags and parts
One tag per question; the tags come from `deck.json` (`tags`) and `parts` decides the order. Defaults: `S` surgery, `M` internal medicine, `MI` microbiology, `PA` parasitology, `PH` pharmacology; part 1 = S + M, then MI, PA, PH collected at the end.
- **PH** only when the tested fact is a drug's mechanism, kinetics, adverse effect, class or regimen.
- **MI / PA** when the tested fact is about the organism (culture, virulence, life cycle, diagnostic stage, vector, treatment of an infection by name).
- Otherwise **S** when the point is operative, emergency, complication-management or surgical anatomy; **M** for diagnosis, medical therapy, investigations and physiology.
Tell the user in the summary which questions you moved to the end parts so they can overrule.

## Answer JSON (array; ids come from `questions.json`)
```json
{"id": "e1-p7", "answer": "C", "tag": "M",
 "page": "46", "exact": true, "anchor": "Competitive reversible PP inhibition",
 "why":   {"en": "…", "ar": "…"},
 "wrong": {"A": {"en": "…", "ar": "…"}, "B": {"en": "…", "ar": "…"}, "D": {"en": "…", "ar": "…"}},
 "pearl": {"en": "…", "ar": "…"},
 "note":  null,
 "chapter": null}
```
`answer` uses the labels in the Markdown (after Stage 1's shuffle); several correct options: `"A, C"`. `wrong` must list exactly the other options. `chapter` overrides the chapter shown on the card (default: the book chapter containing `page`). See `assets/answer_example.json`.
