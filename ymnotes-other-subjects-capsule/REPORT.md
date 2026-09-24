# Report: YMnotes Digestive System — Other Subjects Capsule

## Files

| Deliverable | Path |
|---|---|
| Finished PDF (A4, 10 pages, clickable contents, 12 bookmarks) | `ymnotes-other-subjects-capsule/YMnotes-Digestive-Other-Subjects-Capsule.pdf` |
| Editable source | `source/content.json` (all entries and page references), `source/capsule.css`, `source/build.py` (run `python3 source/build.py`), `source/capsule.html` (generated) |
| Comparison ledger | `ledger/comparison-ledger.csv`, `.md` and `.json`, built by `ledger/make_ledger.py` from the per-agent ledgers in `ledger/agent-ledgers/` |
| QA | `qa/verification.json`, `qa/layout-guard.json`, `qa/verify_capsule.py` |

This capsule is a separate publication from the Internal Medicine companion. It replaces this session's earlier half-book draft (`ymnotes-after-mid-extras/`), which is kept for reference only.

## Page numbers and where the two files join

- **Source:** `GIT others.pdf`, 47 pages. Its printed page number equals its PDF page number.
- **First-half file:** `4_5875397832227168769.PDF`. Printed page = PDF page − 3, covering pp. 1–197.
- **Second-half file:** `4_5875397832227168769(1).PDF`. Printed page = PDF page + 196, covering pp. 197–433.
  - PDF p. 238 is the unnumbered closing page.
  - Its viewer page labels do not match the printed page numbers.
- **The join:** the files join inside **Chapter 15, Colorectal Cancer** (pp. 195–209), and p. 197 is in both files. The capsule treats Chapter 15 as one chapter and marks the join.

## Result

133 candidates were compared against all 40 chapters: 20 were included, 6 were flagged as disagreements, and 107 were excluded. They appear in the capsule as 19 addition entries (two Salmonella lab facts are merged) and 6 CHECK entries.

| Ch | Chapter | Subject | Additions | To check |
|---|---|---|---|---|
| 3 | The Stomach and Duodenum | Pharmacology, Pathology | 1 (osteoporosis with long-term PPI use) | 3 |
| 4 | Pathology of GIT Tumours | Pathology | 8 | 0 |
| 7 | Foodborn Infection | Microbiology | 6 | 1 |
| 14 | Polyposis of Colon | Pathology | 1 | 0 |
| 15 | Colorectal Cancer (spans both files) | Pathology | 3 | 1 |
| 25 | Pyogenic Liver Abscess | Parasitology | 0 | 1 |

**Parasitology:** no additions. GIT Others pp. 35–47 repeat Chapter 9 (pp. 122–139) word for word, with the same doses and time periods. The one parasitology finding is a disagreement over the blood count in amoebic abscess (Ch 25).

**Pharmacology:** GIT Others pp. 1–6 repeat book pp. 44–50. That leaves one addition and two places where your book contradicts itself: misoprostol PGE1 vs PGE₂ (pp. 37 and 48), and the levofloxacin dose (pp. 41 and 48).

**The other chapters:** the remaining 34 chapters were checked and have nothing to add. The capsule lists them.

## Points flagged for review (neither version chosen)

- **Misoprostol:** your book calls it a PGE₂ analogue on p. 37 and a PGE1 analogue on p. 48.
- **Levofloxacin dose:** your book gives 500 mg once daily on p. 41, but 250 or 500 mg twice daily on p. 48.
- **Gastric cancer site:** your p. 62 gives the antrum/pylorus as 60%; GIT Others p. 15 gives the pylorus as 50%.
- **Widal test, H-antigen reading:** your p. 109 and GIT Others p. 24 disagree. The GIT Others passage there is garbled.
- **Colorectal cancer age:** GIT Others gives 50–70 on p. 19 but 60–79 on p. 20. Your Ch 4 p. 74 says 60–79, and Ch 15 p. 196 says "old age".
- **Amoebic liver abscess blood count:** your Ch 25 p. 331 says leukocytosis and eosinophilia. GIT Others p. 47 and your Ch 9 p. 138 say polymorphonuclear leucocytosis.

## Duplicate check and limitation

- **No "Before Mid-Module Extras" handout was found** in the repository or on the connected Google Drive. The closest match is another session's **Internal Medicine companion** (branch `claude/credits-expiring-soon-7nbhf4`, from `GIT Internal Med.pdf`, covering the first half only). I read it for duplicates without changing it. It led to two changes:
  - **Poultry as the Salmonella reservoir (FI-02)** was excluded. That companion already teaches it (its entry C5-15).
  - **The H. pylori sequence (TU-12)** was trimmed to the dysplasia step and the "precancerous lesion" label. That companion already supplies the atrophic gastritis → intestinal metaplasia step (its entry C3-14).
- **Method:** four subagents compared four topic groups under one written standard. My own central review then:
  - re-checked every included and flagged row against both PDFs;
  - rejected the colorectal cancer site percentages, because your Figure 15.2 on p. 197 already shows them (I checked the figure on the rendered page);
  - trimmed two other entries;
  - checked the page mapping for all 133 rows by script.
- **Unreadable pages:** none. All PDFs have native text.
  - The MCQs on GIT Others pp. 33–34 have no answer key, so no facts were taken from them.

## Skill and QA

- **Skill:** the YMnotes medical-book redesign skill was used for:
  - its frozen design tokens and fonts;
  - the brand header with the QR code linked;
  - the adaptive watermark;
  - the permanent closing page, with its links read back from the saved file;
  - `layout_guard.py` (PASS);
  - page renders and a contact sheet.
- **Subject colours:** each subject uses one colour already in the design system — Pharmacology blue, Pathology brick, Microbiology amber, Parasitology green. Every entry also names its subject in text, so nothing depends on colour alone.
- **Visual review:** all 10 pages were inspected. The fixes made were:
  - the running header on the first chapter page;
  - a near-empty overflow page;
  - the column widths in the points-to-check table;
  - the end-note spacing;
  - the size of the contents-page subject chips.
- **Checks on the saved file, all PASS:**
  - Each of the 6 contents rows shows the chapter number, title, subject line and page number, and links to that chapter.
  - The 14 internal links resolve.
  - The 6 links in the points-to-check table land on their entries.
  - The header QR code decodes on every body page.
  - All fonts are embedded (no Type3).
  - The smallest text is 6.9 pt.
  - No text falls outside the page.
