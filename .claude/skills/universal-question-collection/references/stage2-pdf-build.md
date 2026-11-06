# Stage 2 · the two PDFs

`stage2.py build WORK OUT` writes `<prefix>_V1_Students.pdf`, `<prefix>_V2_Answers_with_Book.pdf` and `stage2_report.json`; `qa` re-opens the files and verifies them. Layout: A4, YMnotes header/footer (vector logo from `assets/brand/brand_template.pdf`), fonts Inter / Archivo / Source Serif 4 / Noto Sans Arabic bundled in `assets/brand/fonts` (all OFL).

## Version 1 — students (tablet)
Questions and options only. Header `module_label`, group title (“Group A” + rule), a thin green bar beside each question, options A–E in Source Serif, separators between questions, page number bottom right. **No chapter titles, no answers, no question numbers.** Groups hold 3, 4, 5, 3, 4, 5… questions (`group_cycle`), restarting in every part; a passage group is never split. Parts after the first carry their title under the group heading. Positions match the original YMnotes design within about 1 pt. Passages print once above their first question; figures print under the stem.

## Version 2 — teacher (phone)
Cover with usage notes and a clickable group index → Parts (banner pages) → question cards → Teacher notes → the book.
- Card: group·position chip (e.g. `B·3`), subject tag, book chapter; question; options with a green correct row (check mark, **“Book p. N”** chip) and a one-line English/Arabic reason under every wrong option; “Why”; “Tell the students”; “Question note” when flagged.
- Tapping the green row opens the book at the highlighted line (the printed page number is what the chip says). Green chips at the bottom of that book page (`A·1`) return to the question. Bookmarks: parts, groups, book chapters.
- Teacher notes lists: flagged questions, questions not in the book, nearest-page-only links, how the file was organised.
- Large books are compressed to ~150 dpi when > 60 MB (`compress_book`: `"auto"`, `true`, `false`) — roughly 120 MB → 45 MB; text stays vector. Check a few image-heavy pages if quality matters.

## Book indexing (`index`)
- Printed numbers: read from the bottom band; the corner (right/centre/left) with the most consistent sequence wins. Numbering that restarts later (appendix, duplicated back matter) ends the “main sequence”; later pages are neither searched nor cited. No numbering at all → chips use PDF page numbers (tell the user).
- Chapters: openers such as `CHAPTER 03` (letter-spaced display type is handled) with the next line as the title; ALL-CAPS titles are converted to Title Case; falls back to the PDF outline. Custom books: set `chapter_regex` (named groups `num`, `title`) in `deck.json`.
- Pages without a text layer (scans, handwriting) cannot be searched; view them with `page --png`.

## Mechanics that bite (already handled; keep when editing)
- Chromium anchors (`#id`) are positioned **without** the page's top margin: add `TOP_MARGIN` (= `@page` margin-top, 66 pt) before using them.
- `Page.insert_link` measures `y` from the page top; `get_links`/`resolve_names` for Chromium destinations are raw PDF coordinates (y up). Convert.
- Chromium links become named destinations; they are rewritten as explicit page destinations so every phone viewer follows them.
- CSS contains `%`; never `%`-format it (use `.replace`).
- Printed→PDF page mapping must use only the main sequence, first occurrence of each number.
- File size: GitHub rejects files > 100 MB; WhatsApp documents ≤ 100 MB.

## Troubleshooting
`doctor` fails on Chromium → `npx playwright install chromium` (or point Playwright at an installed Chromium). Arabic shows as boxes → fonts missing from `assets/brand/fonts`. Link lands off target → compare `TOP_MARGIN` with the CSS `@page` margin; run `qa`. A cited anchor disappears after the user swaps the book edition → re-run `validate`.
