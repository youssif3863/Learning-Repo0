> **Superseded.** The user widened the scope to the whole book. The current deliverable is `ymnotes-other-subjects-capsule/` (Other Subjects Capsule). This half-book draft is kept for reference only.

# Completion report: YMnotes Digestive System — After Mid-Module Extras

## Outputs

| Deliverable | Path |
|---|---|
| Finished PDF (A4, 11 pp., clickable contents, 14 bookmarks) | `ymnotes-after-mid-extras/YMnotes-Digestive-After-Mid-Module-Extras.pdf` |
| Editable source | `source/content.json` (all text and page references), `source/handout.css`, `source/build.py` (run `python3 source/build.py`), `source/handout.html` (generated) |
| Comparison ledger | `ledger/comparison-ledger.csv` (spreadsheet), `.md` (readable), `.json`. The shared standard is in `ledger/INCLUSION-STANDARD.md` and the raw per-agent ledgers are in `ledger/agent-ledgers/` |
| QA evidence | `qa/verification.json`, `qa/layout-guard.json`, `qa/verify_handout.py` |

## Scope established from the PDFs

- **"GIT others"** is `GIT others.pdf`: 47 pages, native text, A4. Its PDF page number is also its printed page number.
- **First half** is `4_5875397832227168769.PDF`: 200 PDF pages covering printed pp. 1–197. Printed page = PDF page − 3.
  - PDF pp. 1–3 are the cover and two contents pages.
  - Its embedded bookmarks for Ch 16–40 all point to page 1, so they are broken.
- **Second half** is `4_5875397832227168769(1).PDF`: 238 PDF pages covering printed pp. 197–433. Printed page = PDF page + 196.
  - PDF p. 238 is the unnumbered closing page.
  - Its viewer page labels (i, ii, 1…) do **not** match the printed folios.
- **Where the split falls:** inside **Ch 15, Colorectal Cancer**, which runs pp. 195–209.
  - Printed p. 197 appears in both files.
  - The after-mid-module material is therefore Ch 15 (continued) through Ch 40.

## Chapters covered and accepted additions

**Part A: after the mid-module (Ch 15–40)**

| Ch | Title | Additions | Discrepancies |
|---|---|---|---|
| 15 | Colorectal Cancer | 3: adenocarcinoma is 98% of large-bowel cancers; signet ring vs mucinous adenocarcinoma; irradiation as a predisposing factor | 1: age range |
| 25 | Pyogenic Liver Abscess (amoebic section) | 0 | 1: CBC in amoebic abscess |
| 16–24, 26–40 | 24 chapters | 0 | 0 |

For Ch 16–24 and 26–40, each chapter was checked. Where GIT Others touches the topic (Ch 19, 22, 23, 24, 35), your book already covers it.

**Part B: Earlier-Chapter Additions Found in GIT Others** (kept separate, ordered by your chapter numbers)

| Ch | Title | Additions | Discrepancies |
|---|---|---|---|
| 3 | The Stomach and Duodenum | 1 (osteoporosis with long-term PPI use) | 3 |
| 4 | Pathology of GIT Tumours | 8 | 0 |
| 7 | Foodborn Infection | 7 entries (8 ledger rows; two Salmonella lab facts are merged into one entry) | 1 |
| 9 | Parasitic GI Diseases | 0: GIT Others pp. 35–47 are already in your book pp. 123–138, word for word | 0 |
| 14 | Polyposis of Colon | 1 | 0 |

**Why Part A is short:** most of GIT Others copies first-half chapters almost word for word:
- pp. 1–6 match book pp. 44–50
- pp. 13–21 match book pp. 71–75
- pp. 22–33 match book pp. 107–114
- pp. 35–47 match book pp. 123–138

Only 3 genuine additions fall in the after-mid-module chapters. No outside facts were added to fill space.

**Ledger totals:** 133 candidates: 21 included, 6 discrepancies, 106 excluded.

## Discrepancies (both versions quoted in the handout; neither chosen)

1. **A15-D1:** colorectal cancer age.
   - GIT Others p. 19 says 50–70 years.
   - GIT Others p. 20 and book Ch 4 p. 74 say 60–79.
   - Book Ch 15 p. 196 says "old age".
2. **A25-D1:** CBC in amoebic liver abscess.
   - Book Ch 25 p. 331 (2nd-half PDF p. 135) says leukocytosis **and eosinophilia**.
   - GIT Others p. 47 and book Ch 9 p. 138 say polymorphonuclear leucocytosis only.
3. **B3-D1:** misoprostol.
   - Book p. 37 calls it a PGE₂ analogue.
   - Book p. 48 and GIT Others p. 4 call it a PGE1 analogue.
   - The book contradicts itself here.
4. **B3-D2:** levofloxacin in the rescue regimen.
   - Book p. 41 says 500 mg once daily.
   - Book p. 48 and GIT Others p. 5 say 250 or 500 mg twice daily for 10 days.
   - The book contradicts itself here.
5. **B3-D3:** site of gastric cancer.
   - Book p. 62 gives antrum/pylorus 60%, body 15%, fundus 25%.
   - GIT Others p. 15 gives pylorus 50%, lesser curvature 25%.
6. **B7-D1:** Widal test H-antigen interpretation.
   - Book p. 109 and GIT Others p. 24 differ.
   - The GIT Others list is garbled at this point: its items 1–2 are truncated.

## Central review (after the four parallel comparison agents)

- The same written standard was applied to all four groups: pharmacology, tumours, foodborne infection and parasitology.
- Every included row and every discrepancy was re-checked against both PDFs.
- Page mapping was checked by script for all 133 rows.
- Changes made at the central review:
  - **TU-34 rejected.** The site percentages for colorectal cancer duplicate book **Figure 15.2** (p. 197). The figure's values are in the image, not the text layer; I checked them on the rendered page.
  - **TU-23 trimmed** to the familial-predisposition point.
  - **FI-23 trimmed**: the Gram-smear point was already in the book.
  - **TU-31 moved** to Ch 15.
- 17 rows carry a summary quote rather than a verbatim one. They are marked in `others_quote_check`.
  - 16 are excluded rows, mostly batches of MCQs.
  - The 17th is TU-25, an included row whose quote comes from a table split across lines. I checked it against GIT Others p. 18 by eye.
- No duplicates remain between handout entries.

## Unreadable pages

None. All three PDFs have native text and no page failed to extract.
- Second-half PDF p. 238 has no text; it is the closing artwork.
- Book figures are images. Figures were checked visually where a candidate depended on them (Figure 15.2).
- The GIT Others MCQ pages have a key only for pp. 7–12. The MCQs on pp. 33–34 have no key, so their facts were not inferred.

## Before Mid-Module Extras handout

**Not available.** I searched the repository (all branches) and the connected Google Drive and did not find it. So I could not check this handout against it. Every Part B entry was checked against the first-half book itself. If that handout exists, check Part B against it for overlap.

## Skill use and QA

The **ymnotes-medical-book-redesign** skill was found and its instructions were read and applied:
- Source audit: native text, geometry and outline.
- Frozen design tokens and fonts, and the brand configuration.
- Header with the YMnotes mark and a live QR link.
- The skill's adaptive watermark (`apply_watermark.py`).
- The permanent closing page, with link readback checked (`append_final_page.py`).
- `layout_guard.py`: PASS.
- `render_pages.py` and `make_contact_sheet.py`.

The skill's extract → master pipeline was **not** used, because it rebuilds an existing source book and this is a newly written companion handout.

Page size is A4, the skill's frozen geometry. Your main book is US Letter. The first draft used Letter, but the skill's layout guard rejects it.

Visual review covered **all 11 pages**, at page size and on a contact sheet.

Saved-file checks, all PASS:
- Each of the 6 contents rows shows the chapter number, title, subject line and folio, and links internally to that chapter's page.
- 14 internal links resolve.
- The links in the "points to check" table land on their entries.
- The header QR decodes on every body page.
- All fonts are embedded; there are no Type3 fonts.
- No text falls outside the page.
