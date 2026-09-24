# Completion report: YMnotes Digestive System, Additional Teaching Points, Part 1

## Output paths (repository `youssif3863/Learning-Repo0`, branch `claude/credits-expiring-soon-7nbhf4`)

| Deliverable | Path |
|---|---|
| Finished PDF (30 pages, A4) | `companion/YMnotes-Digestive-System-Additional-Teaching-Points-Part-1.pdf` |
| Editable handout source | `companion/source/handout.md` (the grammar is described at the top of `companion/build/build.py`) |
| Build scripts | `companion/build/` (`build.py` turns the Markdown into HTML, `render.cjs` renders it with Chromium, `finish.py` assembles and verifies) |
| Comparison ledger | `companion/ledger/comparison-ledger.md` (readable), plus `.json` and `.csv` copies |
| Automated verification | `companion/build/out/verification.json`: 111 checks, 0 failures |
| Page-text extractions used for the comparison | `companion/work/main.txt`, `companion/work/im.txt` |

**To rebuild:** edit `source/handout.md`, then run `python finish.py` in `companion/build`. It needs `pymupdf`, `pypdf`, `cryptography`, Node, and Playwright's Chromium.

## Sources and page mapping

- **Main book:** `4_5875397832227168769.PDF`, YMnotes Digestive System Version 3.
  - Printed page = PDF page − 3.
  - All 15 chapter openers were checked against the embedded page labels and the printed folios.
  - **The supplied file ends at printed p. 197 (PDF p. 200).** Printed pp. 198–200 are not in the repository, so Chapter 15 could only be compared for pp. 195–197.
- **Comparison source:** `GIT Internal Med.pdf` (IM), 82 pages. Printed page = PDF page.
  - Its content maps to main-book Chapters 1, 2, 3 (including GI bleeding), 5, 6 and 8.
  - It has no sections corresponding to Chapters 4, 7 and 9–15. Each of those was keyword-checked, and IM's incidental mentions were placed in the chapter where the main book teaches them.
- **Both PDFs have native text,** so no OCR was needed.
  - Every image-bearing page that could carry tables, figure labels or captions was viewed as a rendered image.
  - Several additions come from IM tables that exist only as images (IM pp. 50, 55, 59, 62, 66, 69–70, 76, 78–82).
  - **No page was unreadable.** One exception: the percentages in IM's protein-digestion figure (p. 50) could not be read reliably, so they were not used.

## Accepted handout entries per chapter

Some entries group several ledger rows that belong to the same main-book section. The entry IDs (e.g. `C1-23/24/25/26`) list the rows each one contains.

| Ch. | Main-book chapter | Handout entries | Ledger rows accepted | Discrepancies |
|---|---|---|---|---|
| 1 | GI Symptoms and Investigations | 10 (7 additions, 3 pearls) | 23 | 0 |
| 2 | The Esophagus | 1 | 1 | 0 |
| 3 | The Stomach and Duodenum, incl. GI bleeding (pp. 50–53) | 18 (11 additions, 5 pearls, 2 discrepancies) | 36 | 2 |
| 4 | Pathology of GIT Tumours | none | 0 | 0 |
| 5 | Diarrhea and Malabsorption | 17 (14 additions, 1 pearl, 2 discrepancies) | 18 | 2 |
| 6 | Constipation | 7 (2 additions, 2 pearls, 3 discrepancies) | 8 | 3 |
| 7 | Foodborn Infection | none (IM's infective-diarrhoea items are taught in ch. 5) | 0 | 0 |
| 8 | Inflammatory Bowel Disease | 8 (5 additions, 1 pearl, 2 discrepancies) | 10 | 2 |
| 9–15 | Parasitic GI Diseases → Colorectal Cancer | none | 0 | 0 |
| | **Total** | **61 entries** (40 additions, 12 pearls, 9 discrepancies) | **96** | **9** |

The ledger has 203 candidate rows and 9 chapter-level rows. Central review changed the per-chapter results in these ways:
- **Excluded C1-17** as low value.
- **Excluded GB-02** because it duplicates C1-19.
- **Trimmed GB-05** (the generic resuscitation examples) and **GB-15** (the device-settings table).
- **Removed a clause** already in the main book (intrinsic factor, C3-03).
- **Removed two sentences of my own inference** that went beyond the source text. Every handout statement is now traceable to the cited IM page.

**Out of scope:** variceal bleeding (IM pp. 42–44). It belongs to the main book's Portal Hypertension chapter, beyond p. 197.

## Unresolved discrepancies (flagged in the handout; not resolved)

1. **C3-13:** is autoimmune gastritis "pangastritis"? Main pp. 38, 42 vs IM p. 26.
2. **C3-17:** triple-therapy duration and first-line status. Main p. 41 says 14 days and no longer first-line; main p. 48 says 10–14 days. IM p. 31 says 14 days, "commonly used".
3. **C5-08:** duration that defines acute diarrhoea. Main p. 77: under 2–3 weeks. IM p. 51: under 4 weeks.
4. **C5-38:** stool-fat diet, collection period and lactose breath-test dose. Main p. 93 matches IM's text (p. 68); IM's tables (pp. 69–70) differ.
5. **C6-16:** IBS criteria. Main p. 102 uses Rome V (≥ 3 days/month); IM p. 75 uses Rome IV (≥ 1 day/week).
6. **C6-17:** low-FODMAP example foods. Main p. 104: onions, garlic, wheat, rye, legumes. IM p. 75: potatoes, brown rice, oats, almonds.
7. **C6-20:** second IBS-C drug. Main p. 105: prucalopride. IM p. 75: linaclotide.
8. **C8-03:** granulomas in UC. Main Fig 8.1, p. 117: "should not be present". IM p. 76 table: "occasional". IM's own p. 77 table agrees with the main book.
9. **C8-17:** systemic steroid doses. Main pp. 119–120 and IM's p. 80 text agree; the IM p. 80 drug table differs.

**Source wording noted, not treated as discrepancies:**
- IM p. 39 prints the transfusion threshold unit as "Hb < 10 mg/dl". It is reproduced with that caveat.
- IM p. 37 says "right colon (the ligament of Teriz)". This is garbled and was not used.
- IM p. 18 says "mesenteric" where the main book says "myenteric" plexus.

## Production workflow and deviations

- **Skill used:** the `ymnotes-medical-book-redesign` skill (installed copy, 1.6.0-astra.1 candidate) was read and applied.
  - **From the skill:** its frozen design tokens (identity green, semantic info/warn roles, type scale, bullet grammar, "colour never alone" rule), its static fonts (Source Serif 4, Archivo, Inter) and its brand logo.
  - **Closing page:** its permanent closing page was appended with the skill's own `append_final_page.py`. Its link readback passed: 22 links.
  - **Contents contract:** chapter number, title, subject label and folio sit in one internal link per row. The subject labels come from your book's own contents page.
- **Deviations:**
  - **Different renderer:** the skill's pipeline (pandoc + Vivliostyle, `ymnotes_book.py` stages) is built to rebuild a single source book, and pandoc/Vivliostyle are not installed in this environment. This handout was rendered with the pre-installed Chromium through Playwright instead.
  - **Own checks:** the contents contract, folio and page-label agreement, the outline, margin bounds and font embedding were checked by `finish.py`, not by the skill's `contents_contract.py`/`run_qa.py`, which expect a skill project layout.
  - **No watermark pass.**
  - **Running header is static:** it does not show the current chapter.
- **Visual review:** all 30 pages were inspected on contact sheets. The following were inspected at full resolution:
  - cover, contents and the first chapter
  - discrepancy and dense-table pages: pp. 11, 15, 25
  - last chapter page (28)
  - closing page

  Fixes made:
  - The cover had received a running header; it is now rendered without one.
  - An empty chapter heading split across a page break; empty chapters are now kept together.
  - Bookmarks pointed to the wrong pages.
  - The fallback font is gone: header/footer and superscripts now use the YMnotes fonts.
  - Named links were lost during merging; they are now re-created as explicit links.
- **Navigation:** the PDF has a clickable contents page (15 internal links, each verified to land on that chapter's opener, with the folio equal to the page label), 36 bookmarks, and page labels (Cover, 1–28, YMnotes).
