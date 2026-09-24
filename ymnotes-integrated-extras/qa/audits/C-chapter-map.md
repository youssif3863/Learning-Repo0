# C — Authoritative 40-chapter map: YMnotes Digestive System, Version 3

Audit script: `audits/C_chapter_audit.py` (read-only on the repo; writes `C_chapter_map.json` and `C_audit_raw.json`). Renders: `audits/renders/` (contents pages, p. 197 from both files, final page of the second file).

## 0. Book files and page arithmetic (verified)

| File | PDF pages | Content | Printed folio |
|---|---|---|---|
| `4_5875397832227168769.PDF` ("first") | 200 | PDF 1 cover, PDF 2–3 Interactive Contents (unnumbered), PDF 4–200 = printed pp. 1–197 | printed = PDF − 3 (checked on all 197 body pages: 0 mismatches) |
| `4_5875397832227168769(1).PDF` ("second") | 238 | PDF 1–237 = printed pp. 197–433; PDF 238 = unnumbered back-cover advert (YMnotes video-lecture poster) | printed = PDF + 196 (checked on all 237 body pages: 0 mismatches) |

- The true final printed page is **433** (end of Ch 40, Splenic Trauma). Nothing after it except the unnumbered advert page.
- Viewer page labels: both files carry the same label table (cover '', i–ii, then 1, 2, 3 …), inherited from the single-volume book. In the first file labels equal printed folios; in the second they restart (PDF 1 = '', PDF 2 = 'i', PDF 4 = '1', PDF 14 = '11' while its folio is 210). **Never use viewer labels for the second file.**
- Navigation defects inherited from the split: in the first file the contents links for Ch 16–40 point to PDF page 1 (cover), and its outline bookmarks for Ch 16–40 point to page 1; in the second file the bookmarks for Ch 1–15 point to page 1. Bookmarks for the chapters actually present are correct.
- Mid-module boundary: **the book does not label one anywhere.** A full-text search of both files for "mid", "module", "midterm", "final exam" finds nothing relevant; the PDF metadata, outline and contents only say "Digestive System — Version 3" and split the contents 01–20 / 21–40 (a page-layout split, not a module split). The "before / after mid-module" wording comes only from the inputs: IM cover "Part 1 · Before the Mid-Module Exam · Chapters 1–15" and HEP title "After Mid-Module Hepatology Extras" (scope Ch 16–40). The only physical marker is the file split inside Ch 15 at p. 197. Adopted convention: Ch 1–14 before, Ch 15 spans (pp. 195–197 in first file, pp. 197–209 in second), Ch 16–40 after.

## 1. Chapter map (book contents vs chapter openers)

Contents = PDF pp. 2–3 of the first file ("Interactive Contents", Chapters 01–20 / 21–40). Opener = the `C H A P T E R NN` page; its printed folio equals the contents start page for all 40 chapters.

| Ch | Title (contents) | Title on opener | Subjects (contents) | Printed pp. | Pages | File | Opener PDF p. | Module |
|---|---|---|---|---|---|---|---|---|
| 01 | GI Symptoms and Investigations | Introduction | Internal Medicine · Radiology / Investigation | 1–9 | 9 | first | 4 (first) | before |
| 02 | The Esophagus | THE ESOPHAGUS | Internal Medicine · Surgery | 10–32 | 23 | first | 13 (first) | before |
| 03 | The Stomach and Duodenum | THE STOMACH AND DUODENUM | Internal Medicine · Pharmacology · Surgery | 33–69 | 37 | first | 36 (first) | before |
| 04 | Pathology of GIT Tumours | Pathology of GIT tumours | Pathology · Surgery | 70–75 | 6 | first | 73 (first) | before |
| 05 | Diarrhea and Malabsorption | DIARRHEA AND MALABSORPTION | Internal Medicine | 76–94 | 19 | first | 79 (first) | before |
| 06 | Constipation | Constipation | Internal Medicine | 95–105 | 11 | first | 98 (first) | before |
| 07 | Foodborn Infection | Foodborn Infection | Microbiology · Internal Medicine | 106–114 | 9 | first | 109 (first) | before |
| 08 | Inflammatory Bowel Disease | INFLAMMATORY BOWEL DISEASE (IBD) | Internal Medicine · Pharmacology | 115–121 | 7 | first | 118 (first) | before |
| 09 | Parasitic GI Diseases | Parasitic GI diseases | Parasitology | 122–139 | 18 | first | 125 (first) | before |
| 10 | Small Intestine and Colon Surgery | Surgery of the Small Intestine and Colon | Surgery | 140–144 | 5 | first | 143 (first) | before |
| 11 | Diverticulosis of the Colon | Diverticulosis of the colon | Surgery · Internal Medicine | 145–150 | 6 | first | 148 (first) | before |
| 12 | Appendix | Appendix | Surgery | 151–161 | 11 | first | 154 (first) | before |
| 13 | Intestinal Obstruction | Intestinal obstruction | Surgery · Emergency / Acute Care | 162–188 | 27 | first | 165 (first) | before |
| 14 | Polyposis of Colon | Polyposis of Colon | Surgery · Pathology | 189–194 | 6 | first | 192 (first) | before |
| 15 | Colorectal Cancer | Colorectal Cancer | Surgery · Pathology | 195–209 | 15 | both | 198 (first); cont. first PDF 199–200, second PDF 1–13 | spans |
| 16 | Anorectal Diseases | Anorectal diseases | Surgery | 210–230 | 21 | second | 14 (second) | after |
| 17 | Hepatology and Hepatic Surgery | Hepatology and Hepatic Surgery | Surgery | 231–235 | 5 | second | 35 (second) | after |
| 18 | Liver Disease Assessment | SYMPTOMATOLOGY AND INVESTIGATIONS OF LIVER DISEASES | Radiology / Investigation · Internal Medicine | 236–250 | 15 | second | 40 (second) | after |
| 19 | Acute Hepatitis | ACUTE HEPATITIS | Internal Medicine | 251–263 | 13 | second | 55 (second) | after |
| 20 | Chronic Hepatitis B | CHRONIC HEPATITIS B | Internal Medicine · Pharmacology | 264–273 | 10 | second | 68 (second) | after |
| 21 | Autoimmune Hepatitis | Autoimmune hepatitis | Internal Medicine | 274–279 | 6 | second | 78 (second) | after |
| 22 | Liver Cirrhosis | LIVER CIRRHOSIS | Internal Medicine · Pathology | 280–307 | 28 | second | 84 (second) | after |
| 23 | Portal Hypertension | PORTAL HYPERTENSION | Internal Medicine · Surgery | 308–317 | 10 | second | 112 (second) | after |
| 24 | Hydatid Cyst | Hydatid cyst | Parasitology · Surgery | 318–323 | 6 | second | 122 (second) | after |
| 25 | Pyogenic Liver Abscess | Pyogenic liver abscess | Surgery · Internal Medicine · Parasitology | 324–331 | 8 | second | 128 (second) | after |
| 26 | Hepatocellular Carcinoma | Hepato-cellular carcinoma (HCC) | Surgery · Pathology | 332–336 | 5 | second | 136 (second) | after |
| 27 | Ascites | ASCITES | Internal Medicine | 337–344 | 8 | second | 141 (second) | after |
| 28 | Renal Impairment in Cirrhosis | Renal impairment in liver cirrhosis | Internal Medicine | 345–348 | 4 | second | 149 (second) | after |
| 29 | Jaundice | JAUNDICE | Internal Medicine | 349–354 | 6 | second | 153 (second) | after |
| 30 | Hepatic Encephalopathy | HEPATIC ENCEPHALOPATHY | Internal Medicine | 355–360 | 6 | second | 159 (second) | after |
| 31 | Acute Hepatic Failure | Acute Hepatic Failure | Internal Medicine · Emergency / Acute Care | 361–366 | 6 | second | 165 (second) | after |
| 32 | Biliary System Anatomy | Anatomy of the biliary system | Surgery | 367–372 | 6 | second | 171 (second) | after |
| 33 | Gallbladder Diseases | Diseases of the gall bladder | Surgery | 373–375 | 3 | second | 177 (second) | after |
| 34 | Gallstones and Cholecystitis | Gall stones and chronic cholecystitis | Surgery | 376–388 | 13 | second | 180 (second) | after |
| 35 | Obstructive Jaundice | Obstructive Jaundice | Surgery · Radiology / Investigation | 389–398 | 10 | second | 193 (second) | after |
| 36 | Acute Pancreatitis | Acute pancreatitis | Surgery · Emergency / Acute Care | 399–406 | 8 | second | 203 (second) | after |
| 37 | Cancer Pancreas | Cancer pancreas | Surgery · Pathology | 407–412 | 6 | second | 211 (second) | after |
| 38 | Acute Abdomen | Acute Abdomen | Emergency / Acute Care · Surgery | 413–417 | 5 | second | 217 (second) | after |
| 39 | Abdominal Trauma | Abdominal trauma | Surgery · Emergency / Acute Care | 418–424 | 7 | second | 222 (second) | after |
| 40 | Splenic Trauma | Splenic trauma | Surgery · Emergency / Acute Care | 425–433 | 9 | second | 229 (second) | after |
### Title differences between contents and opener

Case-only differences (e.g. "THE ESOPHAGUS", "Parasitic GI diseases", "Hydatid cyst") are typography. Substantive wording differences:

| Ch | Contents title | Opener title | Running head |
|---|---|---|---|
| 01 | GI Symptoms and Investigations | **Introduction** | GI SYMPTOMS AND INVESTIGATIONS |
| 08 | Inflammatory Bowel Disease | Inflammatory Bowel Disease **(IBD)** | INFLAMMATORY BOWEL DISEASE |
| 10 | Small Intestine and Colon Surgery | **Surgery of the Small Intestine and Colon** | SMALL INTESTINE AND COLON SURGERY |
| 18 | Liver Disease Assessment | **Symptomatology and Investigations of Liver Diseases** | LIVER DISEASE ASSESSMENT |
| 26 | Hepatocellular Carcinoma | Hepato-cellular carcinoma **(HCC)** | HEPATOCELLULAR CARCINOMA |
| 28 | Renal Impairment in Cirrhosis | Renal impairment in **liver** cirrhosis | RENAL IMPAIRMENT IN CIRRHOSIS |
| 32 | Biliary System Anatomy | **Anatomy of the biliary system** | BILIARY SYSTEM ANATOMY |
| 33 | Gallbladder Diseases | **Diseases of the gall bladder** | GALLBLADDER DISEASES |
| 34 | Gallstones and Cholecystitis | Gall stones and **chronic** cholecystitis | GALLSTONES AND CHOLECYSTITIS |

Running heads (the footer line above each folio) match the contents titles in every chapter, so the contents title is the book's canonical short title; all three inputs use it.

## 2. Page 197 (the join) and pp. 198–209

- Printed p. 197 = first file PDF 200 = second file PDF 1. The two pages are **identical**: same extracted text (921 characters, byte-identical), same two embedded images, and pixel-identical renders at 100 dpi.
- Duplicated content (Ch 15 Colorectal Cancer): Figure 15.1 "Macroscopic appearances of colorectal cancer"; Figure 15.2 "Distribution of colorectal cancer" (rectosigmoid commonest; multicentricity common; incidence in different parts); "Spread": A- Direct (mucosa → serosa → organs; internal fistulae; rectum → bladder, vagina, sacrum, prostate, seminal vesicles, peritoneum; right/transverse/left colon local relations) and the start of B- Lymphatic spread (1- epicolic, 2- paracolic nodes). The text continues on p. 198 (3- mesocolic, 4- mesenteric nodes, Fig 15.3, blood spread, staging).
- Pp. 198–209 (rest of Ch 15) exist **only in the second file** (PDF 2–13). The first file stops at p. 197; p. 196 (PDF 199) is its last page not duplicated.
- Consequence: an integrated index must cite Ch 15 as pp. 195–209 and count p. 197 once.

## 3. Cross-check of the three inputs against the book

Inputs: IM = `inputs/im/companion/source/handout.md` (Ch 1–15 headings); OS = `inputs/os/ymnotes-other-subjects-capsule/source/content.json` (6 chapters with items + 6 "checked" rows); HEP = `inputs/hep/ymnotes-hepatology-extras/src/content.py` (12 chapters) and `qa/chapter-map.json`.

**Titles:** all 15 IM headings, all 6 OS chapters, all 6 OS "checked" rows and all 12 HEP chapters use the contents titles exactly. No disagreement among the inputs or with the book. (HEP adds a nav label "Chronic Hepatitis B (and C)" for Ch 20 — a navigation label only; the chapter title is exact.) HEP REPORT explicitly notes the Ch 18 opener title and chooses the contents title, as do the others.

**Subject labels:** all IM, OS-chapter and HEP subject strings match the contents labels exactly (including order and separators). One apparent mismatch is not a real one: the OS "checked" table's 4th column is the *GIT Others* discipline that was checked, not the chapter label (Ch 19 "Microbiology", Ch 22 "Parasitology", Ch 23 "Parasitology · Pharmacology", Ch 35 "Parasitology" do not appear in the book labels for those chapters; Ch 9 and 24 happen to coincide). Do not import that column as chapter subjects.

**Page ranges:** every OS `book_pages`, OS "checked" range and HEP `pages` equals start → next start − 1 from the contents (e.g. Ch 15 pp. 195–209, Ch 25 pp. 324–331, Ch 31 pp. 361–366). IM headings give only `main=` start pages, all equal to the contents. IM section headings (`## … | Main pp. …`) all fall inside their chapter. IM explicitly restricts Ch 15 to pp. 195–197 ("the supplied book file ends at p. 197") — its Ch 15 review did not cover pp. 198–209.

**File/PDF metadata:** every OS item's `book_pdf` equals printed + 3 (1st half) or printed − 196 (2nd half), and every `also` PDF citation is also correct. OS Ch 15 note ("195–197 first file PDF 198–200; 197–209 second file PDF 1–13") is correct.

**HEP `qa/chapter-map.json`:** maps ch17…ch31 to pages *inside the HEP handout* (page_index = printed_folio 2–13), not to book pages; it is internally consistent with the 12 chapters in content.py and carries no book-page claims. HEP `src/content.json` is in sync with `content.py`.

**Chapters with no additions, as stated by each input:**
- IM: explicit "No substantive additions identified" for Ch 4, 7, 9, 10, 11, 12, 13, 14, 15 (15 limited to pp. 195–197). IM does not cover Ch 16–40.
- OS: chapters with items 3, 4, 7, 14, 15, 25; "checked, nothing to add" with a note: 9, 19, 22, 23, 24, 35; "no matching material in GIT Others": 1, 2, 5, 6, 8, 10, 11, 12, 13, 16, 17, 18, 20, 21, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40 (28 chapters; 6 + 28 = the "other 34").
- HEP: items for 17–23, 27–31; "nothing new" for 24–26, 32–40 (handout) and also 16 (REPORT); Ch 1–15 out of scope.

## 4. Do cited book pages fall inside the chapter each entry is filed under?

Checked: IM 61 `:::` blocks (40 addition, 12 pearl, 9 discrepancy) + 17 section headings; OS 25 items (`book_page`) + 4 `also` references (cross-chapter `also` refs checked against the chapter they name); HEP 91 `it()` items + 30 topic `book` ranges. Every page in a range or list was checked (both ends of ranges).

**Out-of-range references: 1**

| Input | Entry | Filed under | Cited | Page actually in |
|---|---|---|---|---|
| HEP | ledger B1-18, fact "Hepatitis G is spread by contaminated blood or blood products; prevalence in blood donors is about 1%." (topic "Virology and transmission", pp. 254–256) | Ch 19 Acute Hepatitis (251–263) | p. 249 | **Ch 18 Liver Disease Assessment** (236–250) |

The page citation itself is right: the book's only Hepatitis G paragraph is on p. 249 (Ch 18, viral-hepatitis markers section: "Hepatitis G: single stranded RNA virus… parenteral…"); Ch 19 has no Hepatitis G text. Fix for the integrated PDF: move B1-18 to Ch 18 under "Viral hepatitis markers" (pp. 247–250), or keep it in Ch 19 but relabel as "Book p. 249 (Ch 18)". After the move, counts become Ch 18 = 27, Ch 19 = 7.

No other IM, OS or HEP reference falls outside its chapter; no OS PDF-page or file-half mismatch.

## 5. Proposed 40-row index for the integrated PDF

Counts are entries as they stand in each input (before the B1-18 move). IM "add/pearl/disc" = block kinds; OS "disc" = CHECK/discrepancy entries; HEP counts are printed points. Totals: IM 61, OS 25 (19 additions + 6 discrepancies), HEP 91. 23 chapters have at least one entry; 17 have none (9, 10, 11, 12, 13, 16, 24, 26, 32–40).

| Ch | Title | Subjects | Printed pp. | Half-file | Module | IM (Part 1) | OS capsule | HEP extras | Any additions |
|---|---|---|---|---|---|---|---|---|---|
| 01 | GI Symptoms and Investigations | Internal Medicine · Radiology / Investigation | 1–9 | first | before | 10 (7 add, 3 pearl) | 0 (no material) | — (out of scope) | yes |
| 02 | The Esophagus | Internal Medicine · Surgery | 10–32 | first | before | 1 (1 add) | 0 (no material) | — (out of scope) | yes |
| 03 | The Stomach and Duodenum | Internal Medicine · Pharmacology · Surgery | 33–69 | first | before | 18 (11 add, 5 pearl, 2 disc) | 4 (1 add, 3 disc) | — (out of scope) | yes |
| 04 | Pathology of GIT Tumours | Pathology · Surgery | 70–75 | first | before | 0 (none stated) | 8 (8 add, 0 disc) | — (out of scope) | yes |
| 05 | Diarrhea and Malabsorption | Internal Medicine | 76–94 | first | before | 17 (14 add, 1 pearl, 2 disc) | 0 (no material) | — (out of scope) | yes |
| 06 | Constipation | Internal Medicine | 95–105 | first | before | 7 (2 add, 2 pearl, 3 disc) | 0 (no material) | — (out of scope) | yes |
| 07 | Foodborn Infection | Microbiology · Internal Medicine | 106–114 | first | before | 0 (none stated) | 7 (6 add, 1 disc) | — (out of scope) | yes |
| 08 | Inflammatory Bowel Disease | Internal Medicine · Pharmacology | 115–121 | first | before | 8 (5 add, 1 pearl, 2 disc) | 0 (no material) | — (out of scope) | yes |
| 09 | Parasitic GI Diseases | Parasitology | 122–139 | first | before | 0 (none stated) | 0 (checked, covered) | — (out of scope) | no |
| 10 | Small Intestine and Colon Surgery | Surgery | 140–144 | first | before | 0 (none stated) | 0 (no material) | — (out of scope) | no |
| 11 | Diverticulosis of the Colon | Surgery · Internal Medicine | 145–150 | first | before | 0 (none stated) | 0 (no material) | — (out of scope) | no |
| 12 | Appendix | Surgery | 151–161 | first | before | 0 (none stated) | 0 (no material) | — (out of scope) | no |
| 13 | Intestinal Obstruction | Surgery · Emergency / Acute Care | 162–188 | first | before | 0 (none stated) | 0 (no material) | — (out of scope) | no |
| 14 | Polyposis of Colon | Surgery · Pathology | 189–194 | first | before | 0 (none stated) | 1 (1 add, 0 disc) | — (out of scope) | yes |
| 15 | Colorectal Cancer | Surgery · Pathology | 195–209 | first + second (p.197 in both) | spans | 0 (none stated) | 4 (3 add, 1 disc) | — (out of scope) | yes |
| 16 | Anorectal Diseases | Surgery | 210–230 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 17 | Hepatology and Hepatic Surgery | Surgery | 231–235 | second | after | — (out of scope) | 0 (no material) | 2 | yes |
| 18 | Liver Disease Assessment | Radiology / Investigation · Internal Medicine | 236–250 | second | after | — (out of scope) | 0 (no material) | 26 | yes |
| 19 | Acute Hepatitis | Internal Medicine | 251–263 | second | after | — (out of scope) | 0 (checked, covered) | 8 | yes |
| 20 | Chronic Hepatitis B | Internal Medicine · Pharmacology | 264–273 | second | after | — (out of scope) | 0 (no material) | 9 | yes |
| 21 | Autoimmune Hepatitis | Internal Medicine | 274–279 | second | after | — (out of scope) | 0 (no material) | 2 | yes |
| 22 | Liver Cirrhosis | Internal Medicine · Pathology | 280–307 | second | after | — (out of scope) | 0 (checked, covered) | 11 | yes |
| 23 | Portal Hypertension | Internal Medicine · Surgery | 308–317 | second | after | — (out of scope) | 0 (checked, covered) | 7 | yes |
| 24 | Hydatid Cyst | Parasitology · Surgery | 318–323 | second | after | — (out of scope) | 0 (checked, covered) | 0 | no |
| 25 | Pyogenic Liver Abscess | Surgery · Internal Medicine · Parasitology | 324–331 | second | after | — (out of scope) | 1 (0 add, 1 disc) | 0 | discrepancy only |
| 26 | Hepatocellular Carcinoma | Surgery · Pathology | 332–336 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 27 | Ascites | Internal Medicine | 337–344 | second | after | — (out of scope) | 0 (no material) | 13 | yes |
| 28 | Renal Impairment in Cirrhosis | Internal Medicine | 345–348 | second | after | — (out of scope) | 0 (no material) | 4 | yes |
| 29 | Jaundice | Internal Medicine | 349–354 | second | after | — (out of scope) | 0 (no material) | 4 | yes |
| 30 | Hepatic Encephalopathy | Internal Medicine | 355–360 | second | after | — (out of scope) | 0 (no material) | 4 | yes |
| 31 | Acute Hepatic Failure | Internal Medicine · Emergency / Acute Care | 361–366 | second | after | — (out of scope) | 0 (no material) | 1 | yes |
| 32 | Biliary System Anatomy | Surgery | 367–372 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 33 | Gallbladder Diseases | Surgery | 373–375 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 34 | Gallstones and Cholecystitis | Surgery | 376–388 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 35 | Obstructive Jaundice | Surgery · Radiology / Investigation | 389–398 | second | after | — (out of scope) | 0 (checked, covered) | 0 | no |
| 36 | Acute Pancreatitis | Surgery · Emergency / Acute Care | 399–406 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 37 | Cancer Pancreas | Surgery · Pathology | 407–412 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 38 | Acute Abdomen | Emergency / Acute Care · Surgery | 413–417 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 39 | Abdominal Trauma | Surgery · Emergency / Acute Care | 418–424 | second | after | — (out of scope) | 0 (no material) | 0 | no |
| 40 | Splenic Trauma | Surgery · Emergency / Acute Care | 425–433 | second | after | — (out of scope) | 0 (no material) | 0 | no |