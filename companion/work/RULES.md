# Comparison rules (shared by every comparison agent)

## Goal
Build a companion supplement: ONLY useful information in "GIT Internal Med.pdf" (IM) that is ABSENT
from the corresponding part of the teacher's main book (MAIN, "4_5875397832227168769.PDF").
Not a summary, not a rewrite, not whole topics.

## Files (all under /home/user/Learning-Repo0/companion/work)
- main.txt : full text of MAIN with markers `=== PDF pN | printed X | images K ===`.
  MAIN printed page = PDF page - 3 (PDF p4 = printed 1). File ends at printed 197.
- im.txt : full text of IM; IM printed page == PDF page (1..82).
- renders/main_pdfNNN_printedXXX.png, renders/im_pNN.png : 80-dpi page images.
  For higher resolution: `python3 -c "import pymupdf as f;d=f.open('<pdf>');d[<index0>].get_pixmap(dpi=150).save('<scratch>.png')"`
  then view it with the Read tool. You MUST view the rendered image of every page flagged
  `images K>0` with little text, and any page where a table/diagram/figure caption may carry content
  that the text layer misses. Do not infer content from titles.

## Test for every candidate
"Would a student already learn this fact, distinction, explanation, clinical implication,
investigation detail, or management point from the corresponding MAIN pages?"
- Yes (incl. paraphrase, or covered in another MAIN chapter within printed 1-197) -> duplicate/exclude.
- Partly -> include ONLY the incremental clause.
- Topic belongs to a MAIN chapter outside printed 1-197 (e.g. portal hypertension/varices,
  liver, biliary, pancreas, anorectal, acute abdomen) -> out of scope.
- IM and MAIN disagree (number, drug, duration, classification, cut-off) -> discrepancy/needs review,
  cite both pages; never blend or pick a winner.
Prioritise mechanisms, distinctions, diagnostic clues, investigation interpretation, management
indications, complications, concise pearls. Exclude filler, trivia, generic statements, and
anything unsupported. Do NOT add any medical content from your own knowledge: every included
statement must be traceable to the cited IM page text/figure. Rephrase for clarity only; keep
numbers, doses, negations, qualifiers exactly as IM states them. Don't pad.
Search main.txt with grep for key terms across the WHOLE of printed 1-197 before deciding
something is absent (the MAIN book may cover it in another chapter).

## Output
Write a JSON file to the path given in your task: a list of objects:
{
 "id": "C<chapter>-<nn>",            // e.g. C2-07
 "chapter": <int 1-15>,
 "main_section": "<MAIN heading where it should be taught>",
 "main_pages_printed": "e.g. 14-15",   // MAIN printed pages checked/where to teach
 "im_pages": "e.g. 12",                // IM pages (printed == PDF)
 "topic": "<short topic>",
 "candidate": "<what IM says, near-verbatim summary>",
 "main_coverage": "<what MAIN says on this, with quote/paraphrase, or 'absent after search for: ...'>",
 "decision": "include" | "duplicate/exclude" | "out of scope" | "discrepancy/needs review",
 "reason": "<why>",
 "handout_kind": "addition" | "pearl" | "discrepancy" | null,   // for include/discrepancy
 "handout_heading": "<short heading>",
 "handout_text": "<student-facing clear English, 1-4 sentences or bullet lines separated by \\n; only incremental info>",
 "handout_table": null | {"caption": "...", "header": [...], "rows": [[...],...]}  // only if a table genuinely helps
}
Log excluded candidates too (reasonably: every substantive IM point you examined should have a row;
group trivial duplicates by subsection). Aim for quality, not quantity.
Finish with a one-paragraph summary in your final reply: counts per decision, pages you could not read.
