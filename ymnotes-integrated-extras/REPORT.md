# Completion report: YMnotes Digestive System — Integrated Teaching Extras

## Deliverables (branch `claude/ymnotes-digestive-integrated-pdf-ixo39c`, folder `ymnotes-integrated-extras/`)

| Deliverable | Path |
|---|---|
| Finished PDF: A4, 49 pages, 40 linked chapter entries, 130 bookmarks | `YMnotes-Digestive-System-Integrated-Teaching-Extras.pdf` (SHA-256 `37856007…ca17a68`) |
| Editable source | `source/` (content in three Markdown files; chapter map; method page) |
| Build instructions | `README.md` |
| Build scripts | `build/` |
| Merged traceability ledger | `ledger/integrated-ledger.md` (readable), plus `.csv` and `.json`, built by `ledger/make_ledger.py` |
| QA results | `qa/verification.json` (22/22 PASS), `qa/layout-guard.json` (PASS), `qa/contents-entry-map.json`, `qa/contact-sheets/`, `qa/run_checks.sh` |
| Subagent audits | `qa/audits/` (A: inputs and build systems; B: overlap and discrepancies; C: chapter map) |
| Frozen inputs | `inputs/`, with `MANIFEST.json` giving the branch, commit and SHA-256 of each file |

**Inputs.** All three were read from the exact commits named in the brief using `git archive`. None of their branches was modified.
- Internal Medicine companion: `4d39d63`.
- Other Subjects capsule: `6e39c13`.
- Hepatology extras: `8afdb3d`.

The older `ymnotes-after-mid-extras/` draft was not used.

## Result in numbers

- **149 teaching additions in 22 chapters.** By subject:
  - Internal Medicine 52
  - Pharmacology 1
  - Pathology 12
  - Microbiology 6
  - Hepatology 78
- **Original ledger rows carried:** 254, as follows:
  - Internal Medicine companion: 96 of its 96 included rows. Four of them (GB-08, GB-09, GB-25, C8-02) also feed a review point.
  - Other Subjects capsule: 20 of its 20 included rows.
  - Hepatology extras: 138 of its 139 included rows. HEP C-28 was excluded in integration because the book already covers it on p. 300.
- **36 points for review.** No position was chosen in any of them.
  - 15 were printed in the Internal Medicine and Other Subjects handouts.
  - 20 were recorded only in the Hepatology ledger.
  - 1 was raised during integration.
  - Five wording and consistency notes (N1–N5) are listed with them.
- **All 40 chapters are in the contents and linked.** The 18 chapters with no additions appear as short entries grouped on shared pages:
  - Ch 9–13, 16, 24–26 and 32–40;
  - Ch 25 shows a review point only.
- **Ledger coverage:** all 594 original ledger rows (IM 212, OS 133, HEP 249) have exactly one integrated disposition. No included row is unaccounted for.

## How the work was split and reconciled

Three subagents audited in parallel. Their reports are in `qa/audits/`.
- **A: inputs and build systems.** Every count, ledger ID and source-to-PDF match checked out. It found:
  - Hepatitis G (HEP B1-18, book p. 249) was filed in Ch 19; I moved it to Ch 18.
  - The Internal Medicine handout compared only pp. 195–197 of Ch 15, and never compared its variceal-bleeding pages with Ch 23.
- **B: overlap and discrepancies.** It found no true duplicates across the three handouts, 12 partial overlaps, and seven kept points that printed a disputed value as settled.
- **C: chapter map.** It confirmed all 40 openers, the page arithmetic of both book files and the p. 197 join. It also found that the book itself never marks a mid-module boundary.

**My editorial decisions on B's findings:**
- **Moved out of the teaching points into review:**
  - GIT Internal Med's transfusion threshold "Hb < 10" (unit printed as mg/dl) → R05.
  - "Rectum always involved in UC" → R13, together with the granuloma row from the same p. 76 table.
- **Kept, with the book's own statement printed beside them:**
  - GIT Internal Med's nasogastric tube and lavage, cross-referenced to R33, which now carries all three positions.
  - TIPS within 5 days. The source itself gives "rebleed within 10 days → repeat endoscopy" with it, as does book p. 316.
  - Large-volume paracentesis, with albumin 8 g per litre removed (book p. 342).
  - The terlipressin dose, labelled "Hepatology source only; the book gives no dose". The garbled ischaemic-heart-disease sentence on that page became note N4.
  - Balloon tamponade, with the source's own "rarely used now" restored.
- **Checked and not a disagreement:** SBP 8% vs 10%. Hepatology p. 75 gives both figures: 10% for all cirrhotics, 8% for the spontaneous type in cirrhotics with ascites. The entry now states both denominators.
- **Merged:**
  - H2-blocker points: IM C3-11 with C3-23.
  - Antiplatelet points: GB-11 with GB-22.
  - ALP/GGT with infiltrative lesions: HEP A-14/15 with B1-19.
  - Clotting-factor lists: A-11, A-03 and A-30, so that no list reads as exhaustive.
  - A few other same-page groups; every one is listed in the ledger.
- **Kept separately:** the H. pylori → cancer steps (IM C3-14 in Ch 3; OS C4-3 in Ch 4) stay as two entries that refer to each other, because each carries distinct facts.
- **Trimmed:** sentences that B found already on the cited book pages, for example:
  - the NSAID burden sentence (p. 36);
  - "Hb falls late" (p. 51);
  - the C. difficile relapse sentence (p. 83);
  - the adenoma "number" row (p. 73);
  - most of the jaundice-type table (pp. 245–246);
  - the diuretic basics (pp. 341–342);
  - the HRS histology (p. 346).
- **Review points extended or corrected:**
  - R28 gained a third position: book p. 359 says 20 g/day in the acute attack.
  - R32 and R34 now also cite GIT Internal Med p. 43, whose text I checked is identical.
  - R21's page reference was corrected to p. 247.
- **Stale notes rewritten:** the original "no additions" notes that became false once the three handouts were merged were rewritten for the merged book.

No clinical or dosing disagreement was resolved. Every retained point carries its book page, its source page and an ID that traces it to the original handout and ledger rows.

## Structure and design

**Front matter:**
- Cover.
- Two-page interactive contents. Each row shows the number, the source-faithful title, the book's subject line, the book page range, an additions/review count and the folio. The whole row is one internal link.
- A Part 1 · Before mid-module band (Chapters 1–15; file 1, pp. 1–197; Ch 15 runs on to p. 209 in file 2) and a Part 2 · After mid-module band (Chapters 16–40).
- The review section and method page.

**Chapters:**
- Each chapter gives its book pages and file, an "In this chapter" topic line, topic bands with book page ranges, and entries with a subject label (colour plus a printed name).
- A "For review" line links to that chapter's review points, with page numbers.
- The running header names the chapter in force and links back to the contents. Pages holding only no-additions entries say "CHAPTERS 32–40 · No additions".

**Design:**
- Frozen YMnotes v3 tokens and static fonts.
- Brand header with a linked QR code, and the permanent closing page appended by the skill's `append_final_page.py` (22 links, readback PASS).
- Part colour: green for before, indigo for after.
- Subject chips: Internal Medicine blue, Pharmacology purple, Pathology brick, Microbiology amber, Parasitology olive, Hepatology teal. Every colour also prints its name.

**Bookmarks:** Cover, Contents, Part 1, the 40 chapters with their topics, Part 2, Points for Youssef to Review with R01–R36, Sources and method, YMnotes.

**Page labels:** Cover, then 1–47, then YMnotes. The printed folio equals the viewer label on every page.

## QA (all on the saved PDF)

- **`qa/verify.py`, 22/22 PASS:**
  - All 40 contents rows show number, title and subject line.
  - Each row has exactly one internal link covering the whole row, with no web link on the row.
  - Each link lands on its chapter's printed heading: same page, within the heading's top band.
  - Each row's folio equals the destination's page label.
  - Every internal link resolves; the only web links are the brand URL.
  - Every chapter "For review" link lands on its review point.
  - Every body page's header links to the contents.
  - One bookmark per chapter lands on its heading, and all major sections have bookmarks.
  - Fonts: no Type3, all embedded.
  - No text is outside the page or the margins, and none is below 5.5 pt.
  - The footer folio equals the page label.
  - The running header matches the chapter on every page.
  - The header QR code decodes to the brand URL on the cover and on every body page.
- **Skill `layout_guard.py`:** PASS.
- **Skill `contents_contract.py`:**
  - Declare: PASS.
  - Navigation integrity: 383 links preserved through outline building.
  - Verify: 33 of 40 chapters PASS, whole-row clickable True.
  - The 7 FAILs are all "N contents links point at chapter N". That gate identifies a chapter by its opening page. Where several targets open on one page it counts their rows as duplicates:
    - Ch 14's page also holds 9–13.
    - Ch 18's page also holds 16, 17 and the Part 2 header.
    - Ch 22's page also holds 21.
    - Ch 26's page also holds 24–25.
    - Ch 31's page also holds 30.
    - Ch 40's page also holds 32–39.
    - Ch 1's page also holds the Part 1 header.
  - For every one of the 40 entries the gate itself reports these as passing: visible number, title, subject line and folio; an internal GoTo link over the title; landing on the declared page; folio equal to the label.
  - `verify.py` checks each landing by exact heading position.
  - This is a structural consequence of the brief's "keep empty entries compact".
- **Visual review:** every page was rendered and inspected at reading size, twice (after the first build and after the fixes). The contents pages were also checked at higher resolution. Fixes made:
  - The running header named the wrong chapter on pages where a chapter opened near the top. Chromium reports destinations from the bottom of the page area, and the build now converts them.
  - Link and bookmark targets sat one top margin too high (same cause).
  - The contents spilled onto a third page; the contents rows were tightened, the body was not touched.
  - Contents pages 2–3 had the wrong header.
  - A literal `&gt;` printed in a review label.
  - "No additions" was printed twice on each empty-chapter entry.
  - A nearly empty page before the method section.
  - A Type3 fallback glyph (⚑).
  - A 0.14 pt folio overhang outside the link rectangle.
  - The header of the page where Part 2 opens.

## Limitations and open items

- **Contents gate:** the skill's `contents_contract.py` reports FAIL (7) for the shared-page reason above. If you want that gate to pass as-is, every chapter would need its own opening page, which would add about 15 near-empty pages.
- **Scope of comparison:** this integration adds only what the three handouts found; it does not re-compare the source PDFs with the book from scratch. Two gaps in the original comparisons remain:
  - The Internal Medicine handout checked only pp. 195–197 of Ch 15, though GIT Internal Med has no colorectal section.
  - GIT Internal Med's variceal pages (42–44) were never compared as a separate source. The Hepatology source has the same text and was compared with Ch 23.
- **Unverified page:** book p. 354 ("direct > 15%") is image-only and was not verified, so it is not printed. It is recorded in the ledger.
- **Chapter 15 layout:** Ch 15 sits alone on its page, because Part 2 starts on a new page.
- **Not a clinical update:** this is not a clinical update. Doses and regimens are reproduced as the sources print them. The 36 review points need your decision before any of them is taught as fact.
