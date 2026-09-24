# YMnotes Digestive System — After Mid-Module Hepatology Extras · Report

## Deliverables (paths relative to repo root)
| File | What it is |
|---|---|
| `ymnotes-hepatology-extras/output/YMnotes Digestive System - After Mid-Module Hepatology Extras.pdf` | Finished handout (A4, 15 pp.: cover, interactive contents, 12 chapter sections, YMnotes closing page) |
| `ymnotes-hepatology-extras/src/content.py` → `content.json` | Editable content (every point carries its ledger IDs) |
| `ymnotes-hepatology-extras/src/build.py`, `handout.css`, `render.cjs`, `assets/` | Build (YMnotes v3 tokens, fonts, brand) — `python3 src/content.py && python3 src/build.py` |
| `ymnotes-hepatology-extras/ledger/comparison-ledger.{md,csv,json}` | Comparison ledger (249 rows) + `agent-parts/` raw per-range rows + `make_ledger.py` |
| `ymnotes-hepatology-extras/qa/verify.py`, `verification.txt`, `render/` | Saved-file checks and the page renders used for visual review |

## Sources and boundaries
- **Source "hapatology"**: actual file is `Hepatology .pdf` (capital H, trailing space before `.pdf`), 96 pp., native text + many image tables/figures. Source page = PDF page = its printed number.
- **Book split (printed folios, not viewer numbers)**: `4_5875397832227168769.PDF` = cover + contents + printed pp. 1–197 (Ch 01–15, ending mid-Colorectal Cancer). `4_5875397832227168769(1).PDF` = printed pp. 197–433 (p. 197 repeated), i.e. tail of Ch 15 and Ch 16–40. After-mid-module scope: Ch 16–40; liver chapters 17–31.
- Chapter titles/subject labels are taken from the book's own Interactive Contents. Ch 18's opener prints "Symptomatology and Investigations of Liver Diseases" while the contents calls it "Liver Disease Assessment"; the handout uses the contents title.

## Method
Seven parallel comparisons (source pp. 1–13, 14–33, 34–42, 43–56, 57–65, 66–80, 81–96), each searching the whole of both books with multiple keywords and viewing every source page with images. Central review then: re-checked absences by keyword sweep across both books; re-read the image tables at high resolution (HBV marker tables p. 17, AIH subtypes p. 22, portal-hypertension sites p. 57, zonation p. 64, SAAG p. 71, diuretic box p. 72, HRS table p. 80, cholestasis levels p. 85, jaundice tables p. 87, indirect-bilirubin algorithm p. 10); removed duplicates across ranges (ligandin, 5′-nucleotidase, CSPH >25 kPa, ammonia); dropped low-value/outdated rows. Main finding: the book already reproduces most of this source nearly verbatim, so additions are mostly omitted sentences, numbers and image-only tables.

## Additions per chapter (91 points)
| Ch | Book chapter | Book pp. | Points | Topics |
|---|---|---|---|---|
| 17 | Hepatology and Hepatic Surgery | 231–235 | 2 | Liver functions; metabolic zonation |
| 18 | Liver Disease Assessment | 236–250 | 26 | Signs & hyperdynamic circulation; LFTs; bilirubin/bile-acid metabolism; jaundice-type table; HBV/HCV serology tables; chronic-hepatitis comparison |
| 19 | Acute Hepatitis | 251–263 | 8 | Course/prognosis (PT); HBV/HCV/HDV/HEV/HGV facts; rosettes |
| 20 | Chronic Hepatitis B | 264–273 | 9 | HBV natural history, reactivation prophylaxis, IFN/entecavir/tenofovir/YMDD; DAA mechanism, sofosbuvir & ribavirin |
| 21 | Autoimmune Hepatitis | 274–279 | 2 | AIH type 1/2 table; MASLD weight-loss cap |
| 22 | Liver Cirrhosis | 280–307 | 11 | Cryptogenic; two routes of harm; clinical/lab extras; elastography cut-offs; PBC, haemochromatosis, Wilson, A1AT extras |
| 23 | Portal Hypertension | 308–317 | 7 | Extra causes by site; β-blocker mechanism/propranolol; bleeding-management numbers; TIPS window; shunt types |
| 27 | Ascites | 337–344 | 13 | PHT-based causes; RAAS; paracentesis/fluid tests/SAAG; diuretic regimen; refractory ascites; SBP |
| 28 | Renal Impairment in Cirrhosis | 345–348 | 4 | HRS mechanism, classic criteria & differential, prevention, doses |
| 29 | Jaundice | 349–354 | 4 | Indirect-bilirubin algorithm; halothane; obstruction-vs-liver table; cholestasis levels |
| 30 | Hepatic Encephalopathy | 355–360 | 4 | Ammonia, amino-acid, GABA mechanisms; treatment framework |
| 31 | Acute Hepatic Failure | 361–366 | 1 | Cerebral blood flow and oedema |

No additions for Ch 16, 24–26, 32–40 (the source does not cover them). **Earlier chapters:** only Ch 02 (no varices section — varices belong to Ch 23) and Ch 03 (NPO in upper GI bleeding already at printed p. 50) were touched; nothing important enough for an appendix, so none is included.

## Unresolved discrepancies (not printed in the handout; both sides cited)
| Ledger | Source p. | Book p. | Point |
|---|---|---|---|
| A-34 | 11 | 239 | PBC in immunoglobulin list: source "raised AMA", book "raised IgM" |
| B1-24 | 22 | 275 | AIH type 1 frequency: 95% vs 80–90% |
| B1-35 | 31 | 259 | Acute hepatitis: bed rest mandatory until bilirubin <1.5 vs normal activity as tolerated |
| B2-03 | 35 | 265 | HBV prevalence in Egypt 5% vs <2% |
| B2-04 | 35 | 265 (248) | Chronicity: children <5 y 20–50%, adults <10% vs 20–30%, <5% |
| B2-10 | 35 | 266–267 | Inactive-carrier HBV DNA <400 IU/L vs <2,000 IU/mL |
| B2-12 | 35 | 267 | Spontaneous HBsAg clearance 1–2%/yr vs ~1%/yr |
| B2-30 | 39 | 273 | Egypt HCV screening >49 million (2018–19, prevalence 4.4%) vs ~60 million |
| C-02 | 44 | 279 | Metformin for NAFLD listed vs not recommended for MASH |
| C-08 | 46 | 283 | Fetor hepaticus: faecal (mercaptans) vs sweet, musty |
| C-13 | 48 | 286 | Protein in HE: restrict 30–40 g/day vs 1.2–1.5 g/kg/day |
| C-15 | 51 | 288 | PBC criteria: all "mandatory" vs two of three |
| C-16 | 51 | 288 | UDCA: no effect on disease process vs slows fibrosis/improves survival |
| C-26 | 55 (44) | 281 | Alcohol ≥30 g/day vs >30 ml/day |
| D-24 | 61 | 315 | Transfusion target Hct ≈30 vs Hb 7–8 g/dL |
| D-25 | 61 | 315 | Ryle's tube routine vs selective |
| D-26 | 61 | 285, 313 | Endoscopy for every cirrhotic vs Baveno VII selection |
| E-37 | 80 (image) | 347 | Terlipressin escalation at day 3 to 2 mg q4h & albumin 20–60 g vs after 2 days (max 12 mg/day) & 20–40 g |
| F-04 | 82 | 245 | Reabsorbed 10–20% urobilinogen: mostly re-excreted by liver vs excreted in urine |
| F-05 | 83–84 | 245 (vs 350) | Gilbert's: decreased conjugation vs listed under "decrease uptake" on p. 245 |

Also noted (within one document, not source-vs-book): source garbles "terlipressin should be given to patients with ischaemic heart disease" (p. 62) and "rifaximin … with any systemic side effects" (p. 91, copied on book p. 359); Child-Pugh C ">10" (source p. 49); book p. 250 "≥250" vs p. 297 ">250" µg/g Wilson liver copper; book HCV chronicity 55–85% vs 80% (p. 271); book p. 354 direct >15% vs p. 246 conjugated >50%. **Book PDF split:** `(1).PDF` restarts viewer page labels (i, ii, 1…) and its bookmarks for Ch 01–15 all point to page 1; printed folios were used throughout.

## Duplicate check
No "Other Subjects Capsule" exists in the repository. The one other completed extras handout — branch `claude/ymnotes-digestive-extras-pdf-fs83fc`, `ymnotes-after-mid-extras/` (source: "GIT others") — covers Colorectal Cancer, Pyogenic Liver Abscess and earlier-chapter pharmacology/tumour/infection/parasite points. None of those chapters receive additions here, so there is no duplicated addition. This handout is a separate publication.

## QA
`qa/verify.py` on the saved PDF: 12/12 contents rows (number, title, subject line, book pages, folio) are single internal links landing on their chapter; folios equal page labels; 15 bookmarks land; all fonts embedded Type0 (no Type3); no text outside the page box; header mark and QR link to the brand URL; closing page appended by the skill's `append_final_page.py` (22 links, readback PASS). Visual review: all 15 pages rendered and inspected; fixed header navigation on pages where a chapter opens mid-page and orphaned words before the page references. Known cosmetic limit: the last content page (Ch 31) is mostly white because Ch 31 has a single point.
