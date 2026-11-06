---
name: universal-question-collection
description: Two-stage question-bank workflow. Stage 1 collects permitted quiz questions from a website through the user's own authorized browser into audited, shuffled, unnumbered Markdown (never AI-generated questions). Stage 2 turns that Markdown into two PDFs - Version 1 for students and Version 2 for the teacher (answers, English/Arabic explanations, subject tags, chapter titles, merged with the user's book and hyperlinked to the exact line). Use for question-bank extraction and for building the study and answer-key PDFs; not for answering or submitting live exams.
---

# Universal Question Collection — two stages

**Stage 1 · Collect** (website → audited Markdown) → **Stage 2 · Study PDFs** (Markdown + book → Version 1 + Version 2).
Keep the stages separate: Stage 1 output is frozen source material; Stage 2 never edits it. **Never add AI-generated or invented questions.** Deliver real files and report completion honestly.

## 0 · Start every use with this reminder
Before touching anything, tell the user in a few lines what this skill needs, and ask only for what is still missing:
1. **The website** to extract the questions from: URL(s) or the already-open signed-in tab, and which exams/sections. (Not needed if the user hands you a Stage 1 Markdown.)
2. **The book** (PDF file or download link) that Version 2 will be merged with and hyperlinked to.

Say what they will get: Stage 1 → shuffled, unnumbered Markdown + audit; Stage 2 → Version 1 (students) and Version 2 (teacher, with the book). Do not start until both are known; if the user says there is no book, build Version 2 without it (`--no-book`) and say so. Fetch a book link into a fresh folder and check its page count.

## Stage 1 — Collect (Part One)
1. Discover the current browser tool and read its documentation. Match the requested open tab and existing signed-in session; do not change accounts or browser environments. Use [platform notes](references/platforms.md) only for the selected host. Access to a page is not proof of export permission; respect the user's scope and the site's restrictions.
2. Read the current audit and saved records before navigating. Verify live section titles and counts once. Resume the last confirmed position; never recollect completed exams. Prefer review, solutions or read-only practice. Pause before an unclear graded or limited-attempt action.
3. Collect one exam and one rendered question at a time. Default two seconds between clicks, never below one; observe after each action; wait longer for loading. Save each question before navigating; checkpoint at least every ten entries, at exam boundaries and before interruption. See [browser and recovery](references/browser-recovery.md).
4. Preserve the full stem, passage, tables, original option labels/order, source-provided answers/explanations and images. A selected response is not an answer key. Unavailable fields read “Not displayed by the source.” Never solve missing answers into source files.
5. Store and export with the offline utility `scripts/bank.cjs` ([record and output contract](references/data-output.md)). `export` writes: one immutable source file per exam (original order and labels), **`questions_shuffled.md`** (questions shuffled with passage groups kept together, options shuffled inside each question and relabelled A, B, C…, **no numbering**, source answers remapped; options such as “all of the above” or “A and C” stay in their original order), and `collection_audit.md`. It never controls a browser and cannot judge permission, truth, visual completeness or semantic duplicates.
6. Validate counts, provenance uniqueness, ordered choices and image files. Report listed vs captured counts per exam and every defect. Deliver the Markdown files.

**Stop** site interactions on CAPTCHA, explicit automation restrictions, access denial or rate limiting. Save progress and request the specific intervention; resume only after a meaningful state change. Do not refresh to evade restrictions, inspect hidden application state, replay requests, preload exams or promise invisibility.

## Stage gate
Read `collection_audit.md`. If it shows missing positions, count mismatches or missing images, show them and ask whether to continue with the partial set. If clean, continue straight into Stage 2.

## Stage 2 — Study PDFs (Part Two)
All commands: `python3 scripts/stage2/stage2.py <command>` (run with no arguments for the list). Details: [answering](references/stage2-answering.md), [PDF build](references/stage2-pdf-build.md).
1. `doctor` — needs Python 3.9+, PyMuPDF, Node 18+ with Playwright/Chromium. Install what is missing; do not continue unready.
2. `init WORK --label "<MODULE LABEL>" --book-title "<Book>"`, then `parse questions_shuffled.md WORK/questions.json` and `index BOOK.pdf WORK`. Read the index report: printed page numbering, chapters, pages without a text layer.
3. **Answer in chunks of ≤ 45** with `retrieve` / `page` / `grep`, writing `WORK/answers/ans_NNN_MMM.json` and running `validate` after each chunk. For every question: the correct option, a subject tag, the printed book page + an exact phrase to highlight, a brief English and Arabic reason it is right, why each other option is wrong, a one-line “tell the students” pearl, and a note when the question is flawed. A source-provided answer is the key; verify answers against the book, never invent pages. Follow [answering rules](references/stage2-answering.md).
4. Adjust `WORK/deck.json` if needed (module label, subject tags, which tags form which part). Default: Internal Medicine + Surgery first, then Microbiology, Parasitology, Pharmacology.
5. `build WORK OUT`, then `qa WORK OUT` — QA must be clean. Version 1 and Version 2 share the same groups (3-4-5 questions each, lettered A, B, C… without question numbers).
   - **Version 1 (students):** the YMnotes design, questions and options only — no answers, no chapter titles.
   - **Version 2 (teacher):** green correct answer, why right / why others are wrong (English + Arabic), pearl, subject tag, book chapter; the book is merged after the questions; tapping the answer opens the book at the highlighted line with its printed page number; chips return to the question; bookmarks and a Teacher-notes page.
6. Deliver both PDFs with a short summary: counts, questions flagged, questions not in the book, nearest-page links, compression. Verify the files exist. Install or store (e.g. GitHub, zip) only as the user asks, and verify installation separately from archive creation.

## Always
- Collect only user-authorized material; do not transmit it to unrelated services or publish it; never package real questions into this skill. See [privacy](references/privacy.md).
- Report source and study completion separately; missing entries are reported, never invented. Run `node scripts/test.cjs` (Stage 1) and `python3 scripts/stage2/stage2.py selftest` (Stage 2) before adapting the utilities; passing tests do not prove a website permits export.
