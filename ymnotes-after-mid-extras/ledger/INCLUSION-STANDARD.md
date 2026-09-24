# Inclusion standard (identical for every comparison agent)

Goal: a companion handout listing ONLY useful facts from "GIT others.pdf" that are genuinely
ABSENT from the teacher's main book (YMnotes Digestive System, Version 3).

## Page conventions (must be exact)
- "GIT others" page = PDF page index (the file has no separate folio scheme; its printed
  page number equals its PDF page index — verify from the top-of-page number in the text).
- Main book: always cite the PRINTED page (book folio). Files:
  - first half `4_5875397832227168769.PDF`: printed = PDF page − 3 (printed 1–197)
  - second half `4_5875397832227168769(1).PDF`: printed = PDF page + 196 (printed 197–433)
  - Printed p.197 is in both files. The chapter text files in this folder already carry
    `==== PRINTED PAGE n (file ..., PDF page m) ====` markers — use them.
- Chapters in the after-split section: Ch 15 (continues across the split; pp.195–209) to Ch 40.
  Chapters 1–14 are EARLIER chapters.

## Unit of comparison
A candidate = one discrete teachable fact/distinction/mechanism/number/clinical detail in
GIT others (a sentence, table row, or bullet). Compare against the ACTUAL text, tables and
figure captions of the corresponding main-book chapter(s). Search the whole book text
(`grep -i` across ch*.txt) before declaring anything absent — the fact may sit in another chapter.

## Decision rules
INCLUDE only if all hold:
1. The specific fact is absent from the main book (not present in any wording, table, list or caption).
2. It is teachable and consequential (mechanism, distinguishing feature, number that matters
   clinically, drug of choice, complication, diagnostic test, management point).
3. It sits within a topic the book already covers (an addition, not a new topic / whole section).
4. It is verifiable from GIT others text itself (not garbled/unreadable).
EXCLUDE when: already in book (even reworded) → "duplicate"; trivial/filler → "low value";
a whole topic the book does not cover → "new topic, out of scope"; MCQ stems/options whose
fact is already covered → "MCQ duplicate"; unreadable → "unverifiable".
MCQs: only include a fact if the MCQ's keyed answer is explicitly stated in GIT others AND the
fact is absent; otherwise exclude. Do not infer answers from your own knowledge.
PARTIAL: if the book covers the topic but lacks one detail, include ONLY the incremental detail.
DISCREPANCY: if GIT others and the book state different values/claims about the same thing,
record decision "discrepancy" with both page references and both wordings verbatim — do not pick one.
Never add outside medical facts. Never correct either source from memory.

## Output
Write a JSON array to the path given in your task. One object per candidate:
{
 "id": "<group>-<nn>",
 "others_page": <int>,
 "others_quote": "<short verbatim excerpt from GIT others>",
 "topic": "<short topic>",
 "book_chapter": <int>,               // chapter where it fits
 "book_chapter_title": "<title>",
 "book_printed_page": <int or null>,   // printed page where it fits / where the related text is
 "book_pdf_file": "first-half" | "second-half",
 "book_pdf_page": <int or null>,
 "book_evidence": "<verbatim excerpt of the related book text, or 'no mention found (grep: terms)'>",
 "new_contribution": "<the precise incremental fact, student-facing, concise English>",
 "decision": "include" | "exclude" | "discrepancy",
 "reason": "<one line>",
 "fits_after": "<the book heading/subheading it sits under>"
}
Log excluded candidates too (aim to cover every substantive fact block in your page range,
grouping obvious duplicates into one row where sensible). Be strict: a differently worded
duplicate is an EXCLUDE.
