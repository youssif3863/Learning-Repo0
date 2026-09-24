# Audit B: Cross-handout overlap and medical discrepancies

**Inputs audited:** read only; nothing in the inputs or the git repository was changed.

| Handout | Short name | Source file | Scope | Content read |
|---|---|---|---|---|
| Internal Medicine companion | **IM** | "GIT Internal Med.pdf" | Ch 1–15 | `inputs/im/companion/source/handout.md` (entries C1-…, C3-…, GB-…, C5-…, C6-…, C8-…) and the ledger, 212 rows |
| Other Subjects Capsule | **OS** | "GIT others.pdf" | all chapters | `inputs/os/.../source/content.json` (entries C3-1 … C25-D1) and the ledger, 133 rows |
| Hepatology Extras | **HEP** | "Hepatology .pdf" | Ch 16–40 | `inputs/hep/.../src/content.py`, identical to `content.json` (checked by script; 91 points under ledger IDs A-, B1-, B2-, C-, D-, E-, F-) and the ledger, 249 rows, including the 20 unresolved discrepancies |

**Main book.** Checked on printed pages.
- First file: printed page = PDF page − 3.
- Second file: printed page = PDF page + 196.
- The mapping was confirmed from the running folios on pp. 37, 41, 48, 62, 74, 109, 138, 197, 198, 245, 315, 331 and 347.

**Method.**
1. PyMuPDF text extraction of both book files and all three source PDFs.
2. Regex searches of the cited pages and the pages around them.
3. For pages whose content is only an image, the page was rendered and inspected: IM pp. 69, 70, 76 and 80; Hepatology pp. 22 and 80; book p. 117 (Fig 8.1).

**Verification codes used below:**

| Code | Meaning |
|---|---|
| **V** | Verified by text extraction. |
| **V-img** | Verified by viewing the rendered page. |
| **U** | Not verified. |

---

## Executive summary

1. **No true duplicates across the three handouts.**
   - The OS capsule had already removed its two overlaps with IM: poultry → Salmonella (FI-02), and part of TU-12.
   - HEP has no chapter in common with IM or OS where both print additions. The only shared chapter is Ch 25, where OS has only a flag.
   - There are **12 partial overlaps**: 1 across handouts (X1) and 11 within a handout (W1–W11). A further 14 pairs are only related, with no shared fact. Merged wordings are proposed in §1.2.
2. **Seven retained entries carry a number or instruction that another source disputes but are printed as settled teaching (safety-critical).** Details in §3.
   - **IM GB-07/08/09/11:** transfuse at **Hb < 10**, and routine NG tube.
   - **IM GB-25/26/27:** NG lavage in unstable lower GI bleeding.
   - **HEP E-21:** SBP **8 %**, against the book's **10 %**.
   - **HEP D-16:** TIPS for rebleeding **within 5 days**, against the book's "rebleed within 10 days → repeat endoscopy".
   - **IM C8-02/08:** rectum "**always**" involved in UC, against the book's "typically involved". It comes from the same IM table row set that IM itself flags (C8-03).
   - **HEP E-18:** large-volume paracentesis described without the book's albumin statement.
   - **HEP D-13:** a single-source terlipressin dose, taken from a source page with a known garble.
3. **The consolidated discrepancy list has 46 rows.** Details in §4.
   - 35 flags already raised by the inputs: IM 9, OS 6, HEP 20.
   - 5 new tensions found in this audit (N1–N5).
   - 6 items that are internal to one source.
   - Two groups merge an IM retained entry with a HEP flag that is only in the ledger: transfusion target and NG tube.
   - One HEP flag (C-13, protein in HE) has a **third position inside the book itself**: p. 359 says 20 g/day in the acute attack.
   - All page references were verified except: book p. 354 ("direct > 15 %", image) and IM p. 77.
   - One page correction: HEP B2-04's "5–10 %" is on **p. 247**, not p. 248.
4. **Already in the book.** More than 100 retained entries were spot-checked (IM 40, all 18 OS additions, HEP about 70); details in §5.
   - **9 are largely already in the book:** IM C3-21/27 (3rd bullet), IM GB-07/08/09/11 (Hb and antiplatelet sentences), IM C5-19 (relapse sentence), OS C4-8 ("Number" row), HEP A-29 (jaundice-type table), HEP E-14 (diuretic regimen), HEP E-24 caution, HEP E-28/29, HEP C-28.
   - About 40 more are partly present; the new part of each is listed in §5.2.
5. **Merge blocker.** Several chapter-level "no additions" notes become false once the three handouts share one chapter-ordered PDF. For example, IM says "No substantive additions" for Ch 4, 7, 14 and 15, and the OS capsule's "remaining 34 chapters have nothing to add". Details in §6.

---

## 1. Overlaps among retained entries (Task 1)

### 1.1 Classification table

**Key to the Class column:**
- **TD:** true duplicate.
- **PO:** partial overlap.
- **REL:** related, with no overlapping fact.

**Across handouts**

| # | Entries | Topic | Book ch / pp | Class | Action |
|---|---|---|---|---|---|
| X1 | IM **C3-14** + OS **C4-3** | Atrophic gastritis → intestinal metaplasia → (dysplasia → cancer) | Ch 3 pp. 38, 42; Ch 4 p. 72 | **PO** | OS already dropped the step IM covers, but OS C4-3 still restates the whole chain. Merge into one entry at Ch 4 p. 72 and leave a pointer in Ch 3 (wording M1). |
| X2 | IM **GB-07/08/09/11** (shock: systolic BP < 100 mmHg; transfusion triggers) + HEP **D-11/13** (resuscitate to systolic BP ≈ 100 mmHg) | Resuscitation in upper GI bleeding | Ch 3 p. 50 / Ch 23 p. 315 | **REL** | The numbers agree. Keep both (non-variceal vs variceal) and add a cross-reference. Note that GB-07's Hb trigger conflicts with the book and a HEP flag (§3, S1). |
| X3 | IM **C5-15** (poultry, seafood → Salmonella; pets → Campylobacter) + OS **C7-1 / C7-4 / C7-5** | Salmonella and Campylobacter | Ch 5 pp. 81–82 / Ch 7 pp. 107–111 | **REL** | Distinct facts. OS FI-02 (poultry) was already excluded. Keep both and add a cross-reference (§2, P1). |
| X4 | IM **C3-17** (flag) + OS **C3-D2** (flag) | H. pylori regimens: book p. 41 vs p. 48 | Ch 3 | **REL** (two different disagreements) | Keep both flags, but present them together in one "book p. 41 vs p. 48" CHECK box. |
| X5 | IM **C3-21/27** (NSAIDs, pp. 36–37) + OS **C3-D1** (misoprostol, p. 37) | NSAID injury and prophylaxis | Ch 3 p. 37 | **REL** | Keep both. They sit next to each other. |
| X6 | IM **C3-23** (sucralfate, p. 48) + OS **C3-1** (PPI and osteoporosis, p. 45) | Gastritis pharmacology table | Ch 3 pp. 45–48 | **REL** | Keep both. |
| X7 | IM **GB-19/20/21/22** (bleeding gastric cancer) + OS **C4-2** (malignant oesophageal ulcer → fatal haemorrhage) + OS **C3-D3** (gastric cancer site) | Bleeding from GI cancers | Ch 3 p. 50 / Ch 4 p. 71 / Ch 3 p. 62 | **REL** | Keep all three. |
| X8 | IM **GB-28/29** ("varices rarely present as chronic blood loss"; "a colonic polyp should not be assumed to be the cause") + HEP Ch 23 + OS **C4-7/C4-8/C14-1** | Varices, polyps | Ch 3 p. 53 / Ch 23 / Ch 4, 14 | **REL** | Keep. |
| X9 | IM **C3-05/06** (gastropathy from chronic congestion in portal hypertension) + HEP Ch 23 | Portal hypertensive gastropathy | Ch 3 p. 35 / Ch 23 p. 313 | **REL** | Keep. HEP has no portal-hypertensive-gastropathy entry. |
| X10 | IM **C8-11** (bacterial colitis includes Shigella and invasive E. coli; Yersinia, TB, schistosomiasis mimic IBD) + OS Ch 7 entries | Infective mimics of IBD | Ch 8 p. 119 / Ch 7 | **REL** | Keep. |
| X11 | IM **C5-23** (travellers: amoebiasis) + OS **C25-D1** (amoebic abscess blood count) | Amoebiasis | Ch 5 / Ch 25 | **REL** | Keep. |
| X12 | HEP **E-25/26** (norfloxacin after upper GI haemorrhage) + IM **GB** block | Antibiotics in cirrhotic GI bleeding | Ch 27 p. 344 / Ch 3 | **REL** | Keep. IM has nothing on antibiotics. |

**Within a handout**

| # | Entries | Topic | Book pp | Class | Action |
|---|---|---|---|---|---|
| W1 | IM **C3-08/09/11** (treatment bullet: "H2 blocker (e.g. famotidine) may be used along with the PPI") + IM **C3-23** (H2 blockers, PPIs, sucralfate) | Drugs for acute / erosive gastritis | Ch 3 pp. 36, 48 | **PO** | Merge the H2-blocker point into one entry (M2). |
| W2 | IM **GB-07/08/09/11** (last bullet: "Clopidogrel and warfarin are also stopped… urgent discussion with a cardiologist") + IM **GB-19/20/21/22** ("After PCI… stopping antiplatelets carries a high risk") | Stopping antiplatelets during a GI bleed | Ch 3 p. 50 | **PO** | Merge (M3). Book p. 50 already says that interrupting antiplatelets needs specialist assessment (§5). |
| W3 | IM **C3-18/19** ("All patients with duodenal or gastric ulcer who have H. pylori should receive eradication") + IM **GB-19/20/21/22** ("always confirm H. pylori eradication" after a bleeding ulcer) | H. pylori and ulcer | Ch 3 pp. 40–41, 52 | **PO** | Keep both (different sections) and add a cross-reference. No merge needed. |
| W4 | IM **C1-19/20** (blood per rectum from a massive upper GI bleed) + IM **GB-25/26/27** (NG aspirate separates upper from lower source) | Upper vs lower source of rectal blood | Ch 1 p. 4 / Ch 3 p. 52 | **PO** | Keep both. IM's central review already folded the duplicate GB row into C1-19. |
| W5 | IM **C5-34/36** (lactose H₂ breath test: late peak) + IM **C5-35** ("contrast this with the late peak of lactose malabsorption") | H₂ breath tests | Ch 5 p. 93 | **PO** (deliberate cross-reference) | Keep. Both take numbers from the IM p. 69–70 tables that C5-38 flags (§3, S9). |
| W6 | HEP **A-14/15** (ALP/GGT > 3-fold with space-occupying lesions) + HEP **B1-19** (hepatic infiltration: ALP/GGT up, bilirubin may be normal) + HEP **F-07** (isolated ALP rise: tumours, granulomas …) | ALP/GGT with space-occupying or infiltrative lesions | Ch 18 p. 245 | **PO** (three entries on one page and one point) | Merge A-14/15 with B1-19 (M4). Keep F-07 as the list of causes. |
| W7 | HEP **A-03** (bleeding tendency: fibrinogen and factors II, V, VII, IX, XI, XII, XIII) + HEP **A-11** (all clotting factors except VIII) + HEP **A-30** (PT depends on I, II, V, VII, X) | Hepatic synthesis of clotting factors | Ch 18 pp. 238, 244, 246 | **PO** | The three lists disagree in coverage: A-03 omits factor X, which A-30 includes. Merge so that no list reads as exhaustive (M5). |
| W8 | HEP **A-12/30/31** (PT is an earlier indicator than albumin) + HEP **B1-02** (PT is the key prognostic indicator in acute viral hepatitis; PT > 3 s poor) | PT as a severity marker | Ch 18 p. 246 / Ch 19 p. 252 | **PO** | Keep both, one in each chapter, with a cross-reference. |
| W9 | HEP **A-26/28** (haemolysis: reticulocytes and **LDH**) + HEP **A-27** (algorithm: LDH, haptoglobin, reticulocytes) | Tests for haemolysis | Ch 18 p. 246 / Ch 29 p. 354 | **PO** | Keep both. Optionally drop "and raised LDH" from A-26 and add "see Ch 29". |
| W10 | HEP **A-05/06** (vasodilators → sympathetic and RAAS activation → Na/water retention, ascites; NO in ascites, HRS, portal hypertension) + HEP **E-04/05** (RAAS → renal sodium avidity (ascites) and renal vasoconstriction (HRS)) + HEP **E-28/29** (HRS: splanchnic vasodilatation, renal vasoconstriction, raised sympathetic tone) | Vasodilatation → RAAS → ascites and HRS | Ch 18 p. 237 / Ch 27 p. 339 / Ch 28 p. 346 | **PO** | Keep all three (each extends its own page). Trim the last sentence of E-04/05 to a cross-reference. The E-28/29 core is already on book p. 346 (§5). |
| W11 | HEP **E-21/22/24** fact ("variceal bleeding and previous SBP carry particular risk") + HEP **E-25/26** ("after upper GI haemorrhage … give norfloxacin 400 mg 12-hourly for at least 7 days") | GI bleeding and SBP risk | Ch 27 pp. 343–344 | **PO** | Keep both. They should sit next to each other. |
| W12 | HEP **C-11/12** (liver stiffness > 25 kPa → CSPH → carvedilol) + HEP **D-08/09/10** (non-selective β-blocker mechanism; propranolol alternative) | Non-selective β-blockers in portal hypertension | Ch 22 p. 285 / Ch 23 p. 313 | **REL** | Keep. Cross-reference Ch 22 ↔ Ch 23. |
| W13 | HEP **D-19** (liver inactivates ammonia via the urea cycle) + **D-22** (less detoxification of ammonia) + **F-12/15** (ammonia cleared as urea and glutamine; raised in 90 % of HE) | Ammonia | Ch 17, 22, 30 | **REL** | Keep. |
| W14 | HEP **A-29** (jaundice-type table) + **F-06** (obstruction vs liver-disease table) + **A-25** (halothane → mixed hyperbilirubinaemia) + **C-10** (urine urobilinogen raised in cirrhosis) | Jaundice classification | Ch 18 pp. 245–246 / Ch 29 / Ch 22 | **REL** | Keep. A-29 is largely already in the book (§5). |

**True duplicates (TD):** none found between retained entries, within or across handouts. The earlier duplicates were already removed by OS (IM C5-15 / FI-02, IM C3-14 / TU-12) and by HEP's central review (D-06 merged into C-12; A-16 merged into F-08).

### 1.2 Proposed merged wordings (no new medicine; every fact and page reference kept)

**M1: X1 (IM C3-14 + OS C4-3).** Place at Ch 4, book p. 72, next to "On top of intestinal metaplasia". Leave a one-line pointer at Ch 3, pp. 38/42.
> **From H. pylori gastritis to intestinal-type cancer.** Gastric metaplasia, usually of the **intestinal type**, occurs almost always in the setting of **atrophic gastritis** (IM p. 26). The sequence continues past metaplasia: H. pylori gastritis → atrophic gastritis → intestinal metaplasia → **dysplasia → cancer**. GIT Others lists intestinal metaplasia as a **precancerous (dysplastic) lesion** of the stomach (GIT Others p. 15). *Main pp. 38, 42, 72 · IM p. 26 · GIT Others p. 15 · IM C3-14, OS C4-3 (TU-12)*

**M2: W1 (IM C3-08/09/11 treatment bullet + IM C3-23).** Keep C3-08/09 (stress gastritis in MI and stroke; progression to chronic gastritis) at p. 36. Replace C3-11's treatment bullet and C3-23 with:
> **Drug options for acute erosive/haemorrhagic gastritis.** IM lists **H2 blockers** (e.g. famotidine, which may be used along with the PPI), **proton pump inhibitors** and **sucralfate**. Remove risk factors: stop NSAIDs, reduce caffeine, stop alcohol and smoking. In the main book, sucralfate appears only in the pharmacology table (mainly stress-ulcer prophylaxis). *Main pp. 36, 48 · IM pp. 25, 32 · IM C3-11, C3-23*

**M3: W2 (antiplatelets; IM GB-11 bullet + GB-22 bullet).**
> **Antithrombotics during a GI bleed.** Clopidogrel and warfarin are also stopped, but stopping antiplatelets needs urgent discussion with a **cardiologist**. **After PCI**, heparins and clopidogrel increase GI bleeding: give an IV PPI bolus followed by an infusion; platelet infusion can counter clopidogrel. Stopping antiplatelets carries a high risk. *Main p. 50 · IM pp. 40, 45 · IM GB-11, GB-22*
>
> *Note:* book p. 50 already says "interruption of antiplatelet therapy requires specialist assessment because of thrombosis risk", so the new content here is the PCI setting, the PPI bolus/infusion and platelet infusion.

**M4: W6 (HEP A-14/15 + B1-19).** Ch 18 p. 245.
> **ALP/GGT with space-occupying or infiltrative lesions.** ALP and GGT are markedly raised (> 3-fold) not only in cholestasis but also with **space-occupying lesions / hepatic infiltration** (tumours such as cancer, cysts, lymph nodes). In infiltration, bilirubin may be **normal**, because partial obstruction lets bilirubin pass yet stimulates ALP/GGT synthesis. AST/ALT are normal or slightly raised (AST > ALT). AFP rises in HCC, and CEA with secondaries from GIT cancer. Non-hepatic ALP rises occur in bone disease (rickets, osteomalacia). *Book p. 245 · Src pp. 6, 20 · A-14, A-15, B1-19*

**M5: W7 (HEP A-11 + A-03 + A-30).** Ch 18, pp. 238/244/246.
> **What the liver makes and what PT measures.** The liver synthesises albumin, **all clotting factors except factor VIII**, carrier proteins (ceruloplasmin, transferrin), cholesterol, bile salts and urea (src p. 5). The source's bleeding-tendency list names fibrinogen and factors II, V, VII, IX, XI, XII and XIII (src p. 1). PT depends on factors I, II, V, VII and X (src p. 10). *Book pp. 238, 244, 246 · A-11, A-03, A-30*
>
> Keep A-12/A-31 (albumin as a prognostic marker; PT an earlier indicator) as the next sentence.

---

## 2. Chapter placement conflicts (Task 2)

| # | Topic | Placements | Where the book teaches it | Recommendation |
|---|---|---|---|---|
| P1 | Infective diarrhoea / Salmonella | IM puts the exposure–pathogen table (C5-15) and C. difficile (C5-19) in **Ch 5**; its Ch 7 note says "no additions, see Ch 5". OS puts the Salmonella, Campylobacter and Brucella lab items (C7-1…C7-6, C7-D1) in **Ch 7**. | Acute infectious diarrhoea, pathogens and C. difficile: Ch 5 pp. 81–83. Salmonella and Campylobacter microbiology: Ch 7 pp. 107–111. | **Keep IM C5-15 and C5-19 in Ch 5**; they extend pp. 81–83. **Keep the OS items in Ch 7.** Add a Ch 5 → Ch 7 p. 110 pointer. **Rewrite IM's Ch 7 note** so it no longer says "No substantive additions" (§6). |
| P2 | Intestinal metaplasia sequence | IM C3-14 in **Ch 3** (main pp. 38, 42, 72); OS C4-3 in **Ch 4** (p. 72) | The sequence and "on top of intestinal metaplasia" are on Ch 4 p. 72; atrophic gastritis is on Ch 3 pp. 38/42 | **One merged entry in Ch 4, p. 72** (M1), with a pointer in Ch 3. |
| P3 | Blood per rectum from an upper GI bleed | IM C1-19/20 in **Ch 1** (p. 4); IM GB-25/26/27 in **Ch 3** (p. 52) | Ch 1 p. 4 ("Massive upper GI bleed: fresh blood per rectum + shock") and Ch 3 p. 50 | Keep C1-19/20 in **Ch 1, p. 4**, where the book states the rule. Keep the GB items in Ch 3. |
| P4 | Upper GI bleeding, non-variceal vs variceal | IM GB block in **Ch 3** (pp. 50–53); HEP D-07…D-17 in **Ch 23** (pp. 313–317) | Non-variceal: Ch 3 pp. 50–52. Variceal: Ch 23 pp. 314–317. Book p. 51 also has a one-line "Variceal bleeding → band ligation". | Keep the split. **Qualify IM's transfusion and NG-tube bullets** as they apply to non-variceal bleeding (§3, S1–S2). Cross-reference Ch 3 ↔ Ch 23. |
| P5 | Varices screening and CSPH → carvedilol | HEP C-11/12 in **Ch 22** (p. 285); HEP D-08/09/10 in **Ch 23** (p. 313) | Baveno VII / elastography / carvedilol: Ch 22 p. 285. Primary prophylaxis: Ch 23 p. 313. | Keep as placed, with a cross-reference. |
| P6 | Norfloxacin after upper GI haemorrhage or sclerotherapy | HEP E-25/26 in **Ch 27** (p. 344) | Ch 27 p. 344 (its norfloxacin sentence is truncated: "400mg/12 hours days") and Ch 23 p. 316 ("Prophylactic antibiotics: oral or IV") | Keep in **Ch 27, p. 344**, which completes the truncated book sentence. Add a pointer at Ch 23, p. 316. |
| P7 | Jaundice mechanisms and tests | HEP A-21/22/26/28/29 in **Ch 18** (pp. 245–246); HEP A-25/A-27/F-06/F-10 in **Ch 29** (pp. 351–354) | Both chapters. Ch 18 pp. 245–246 has the classification; Ch 29 pp. 350–354 has the approach. | Keep as placed. Add cross-references for A-26 ↔ A-27 (LDH). |
| P8 | Amoebic liver abscess blood count | OS C25-D1 in **Ch 25** (p. 331); the conflicting statement is also on Ch 9 p. 138 | Ch 25 p. 331 carries the disputed "eosinophilia" | Keep in Ch 25, with a pointer at Ch 9 p. 138. |
| P9 | Colorectal cancer age | OS C15-D1 in **Ch 15** (p. 196); also cites Ch 4 p. 74 | Both | Keep in Ch 15, with a pointer at Ch 4 p. 74. |
| P10 | Colonic adenomas | OS C4-7/C4-8 in **Ch 4** (p. 73); OS C14-1 in **Ch 14** (p. 190) | Both | Keep as placed. |

---

## 3. Retained additions that conflict with a flag, another handout, or the book (Task 3; safety-critical)

The disputed number or instruction is currently printed as settled teaching in every row below. The Recommendation column gives presentation options only; none of them resolves the clinical question.

| # | Retained entry (handout) | What it prints | Conflicting position | Severity | Recommendation |
|---|---|---|---|---|---|
| **S1** | **IM GB-07/08/09/11** (Ch 3, main pp. 50–51, IM p. 39) | "Transfuse if: shock … **or Hb < 10** (IM prints the unit as 'mg/dl') with recent or active bleeding" | <ul><li>Book p. 51: "Hemoglobin levels are generally a poor indicator of the need to transfuse" (V).</li><li>Book p. 315: "restrictive, with a target hemoglobin generally around **7–8 g/dL**" (V; variceal).</li><li>HEP ledger **D-24** (not printed): Hepatology p. 61 "hematocrit value around 30" vs book 7–8 g/dL (V).</li></ul>So IM's Hb < 10 trigger agrees in magnitude with the Hepatology source's Hct ≈ 30, and both disagree with the book's only numeric target. | **High** (transfusion threshold) | Do not print Hb < 10 as settled. Move the numeric trigger into a **CHECK** entry grouped with D-24 (see §4, G1). Alternatively print it as "IM states …" with the book's restrictive target beside it. Keep the other bullets (shock criteria, pulse and venous pressure as guides, CVP). |
| **S2** | **IM GB-07/08/09/11** (IM p. 40) and **IM GB-25/26/27** (IM p. 46) | "A **nasogastric tube** allows gastric wash and monitoring of ongoing bleeding"; "Unstable patient: perform **nasogastric lavage**" | <ul><li>Book p. 315: "A nasogastric tube may be considered **selectively** … but it is **not routinely required**" (V; variceal).</li><li>HEP ledger **D-25** (not printed): Hepatology p. 61 "Ryle's tube insertion for aspiration and lavage" vs book p. 315 (V).</li><li>Book pp. 50–52 (non-variceal upper and lower GI bleeding): silent (V).</li></ul> | **Medium** | Group with D-25 as one CHECK (§4, G2). If kept as an addition, qualify it as IM's advice for non-variceal / lower GI bleeding and cite book p. 315 for variceal bleeding. |
| **S3** | **HEP E-21/22/24** (Ch 27, book p. 343, src p. 75) | "SBP develops in about **8 %** of cirrhotics with ascites" | Book p. 343: "it affects **10 %** of cirrhotic patients" (V). HEP's ledger calls this "absent detail" and did not flag it. The denominators differ (with ascites vs all cirrhotics). | **Medium** (epidemiological figure) | Print both figures with their sources, or move to CHECK (§4, N1). |
| **S4** | **HEP D-16/17** (Ch 23, book pp. 316–317, src p. 62) | "TIPS is indicated when bleeding cannot be stopped or rebleeding occurs **within 5 days** of endoscopic therapy" | Book p. 316: "Patients may rebleed **within 10 days** and in this case **endoscopic therapy is repeated**" (V). Taken together, the two could imply different first actions for early rebleeding. | **Medium** | Flag as a possible tension (§4, N2); do not reconcile. At minimum, print the book sentence next to the HEP point. |
| **S5** | **IM C8-02/08** (Ch 8, book p. 117, IM p. 76 table) | "In IM's comparison table the **rectum is always involved in UC**" | Book Fig 8.1 p. 117: UC rectum "**Typically involved** with variable proximal distribution" (V-img). The **same IM p. 76 table** gives the granuloma row that IM flags as unreliable (C8-03). | **Low–Medium** | Soften to "IM's table: always; book: typically involved", or merge into the C8-03 CHECK as "IM p. 76 table vs book Fig 8.1" (§4, N3). |
| **S6** | **HEP E-18/19/20** (Ch 27, book p. 342, src p. 74) | "Large-volume paracentesis: **4–6 L daily** until the abdomen is emptied, repeat every 2–4 weeks …" (no albumin mentioned) | Book p. 342: removal of > 5 L "with administration of IV albumin (**8 gm/L removed**)"; < 5 L needs no volume expanders (V). This is an omission, not a contradiction; HEP's ledger calls the two "compatible". | **Medium** (could be read as large-volume paracentesis without albumin) | Merged wording should restate the book's albumin sentence next to the 4–6 L schedule (a book fact, so no new medicine). |
| **S7** | **HEP D-11/13** (Ch 23, book p. 315, src p. 62) | "Terlipressin: **2 mg IV every 6 h, then 1 mg every 4 h**, for 2–5 days" | <ul><li>The book gives no variceal dose, only "2–5 days" (V).</li><li>Single source: Hepatology p. 62, the same passage whose next sentence is garbled ("It should be given to patients with ischemic heart disease"; book p. 315 says "caution"; HEP REPORT "also noted").</li><li>A different terlipressin schedule for HRS (1 mg q4–6h; escalation disputed, E-37) is printed in Ch 28.</li></ul> | **Medium** (single-source dose) | Keep it only with a "source dose; not in book" label and a teacher check. Do not merge it with the HRS dosing. |
| S8 | **IM GB-03** (Ch 3, book p. 50, IM p. 37) | "Corticosteroids in usual therapeutic doses have **no influence on GI haemorrhage** on their own" | Book p. 50: "Avoid combination with corticosteroids except in selected cases" (V). IM's entry already says this in parentheses. | Low | Present it as a discrepancy/CHECK entry rather than an addition, or keep the parenthetical (§4, N4). |
| S9 | **IM C5-34/36, C5-35, C5-37** (Ch 5, book pp. 93–94) | Cut-offs from the IM p. 69–70 test tables (lactose late peak 3–6 h > 20 ppm; SeHCAT < 10 %; D-xylose > 4 g/5 h) | IM **C5-38** flags that the **same tables** disagree with IM's text and the book on protocol numbers (100 g vs 70–100 g fat; 3 vs 2–3 days; lactose 1 g/kg vs 25 g) (V, V-img). The printed cut-offs themselves are not contradicted anywhere. | Low | No change needed. Optionally note "IM p. 69–70 table" as the source of these cut-offs. |
| S10 | **IM C8-14/15, C8-20/21** (Ch 8, book pp. 119–120, IM p. 80 drug table) | 5-ASA, budesonide, immunomodulator and biologic doses | IM **C8-17** flags the **same p. 80 table's** steroid rows as contradicting IM's own p. 80 text and book pp. 119–120 (V, V-img). The other rows are not contradicted (the book gives no doses). | Low | Keep, attributed to the "IM p. 80 drug table". |
| S11 | **OS C4-8** (Ch 4, book p. 73, GIT Others p. 18) | Table: villous adenoma dysplasia/cancer "High (**about 40 %**)" | GIT Others p. 18 table ties the 40 % to adenomas **> 4 cm**; its text ties it to villous adenomas in general (V). OS prints this under the table. | Low | Keep the footnote directly under the table cell. |
| S12 | **HEP D-12/15** (Ch 23, book pp. 315–316) | "Balloon tamponade still has a place when endoscopic or vasoconstrictor therapy has failed or is unavailable" | Book p. 316: "now **rarely used** because of serious complications" (V). Hepatology p. 62 itself says "rarely used now … but can be used if …" (V). HEP dropped that qualifier. | Low | Restore "rarely used now" to the HEP wording (it is in both sources). |
| S13 | **HEP E-36** (Ch 28, book p. 347, src p. 80 image) | Albumin 1 g/kg/day (max 100 g); midodrine, octreotide and noradrenaline doses | These come from the **same image table** as flagged **E-37** (albumin maintenance 20–60 vs book 20–40 g/day; escalation day 3 vs 2 days) (V-img). HEP correctly left out the 20–60 g figure. The printed rows are not contradicted (book p. 346 "albumin 1 g per kg" agrees). | Low | Keep. The E-37 flag stays in the ledger or CHECK list. |

**No conflicts found for:** OS C3-1, C4-1…C4-7, C7-1…C7-6, C14-1, C15-1 (98 % is compatible with the book's "> 90 %"), C15-2, C15-3; HEP C-11/12 (consistent with book p. 285; the contrary Hepatology p. 61 statement is flag D-26); HEP B1-02, C-01, C-21/23, E-26.

---

## 4. Consolidated, deduplicated discrepancy list (Task 4)

**Key to the Verif column:**
- **V:** both sides verified by text extraction.
- **V-img:** at least one side verified by viewing the rendered page.
- **U:** not verified.

**Notes on the list:**
- **Pages:** "Book" means main-book printed pages.
- **Where the flags came from:**
  - IM flags are printed in the IM handout.
  - OS flags are printed in the OS capsule.
  - HEP flags are **only in the ledger**; they are not printed in the handout.
  - N-rows are new in this audit.
- **Groups G1–G2:** two groups merge flags that describe the same disagreement.

### 4.1 Flags already raised by the inputs (grouped and deduplicated)

| # | Topic | Position A (source, page) | Position B (source, page) | Raised by (IDs) | Book ch | Verif |
|---|---|---|---|---|---|---|
| 1 | Autoimmune gastritis called "pangastritis"? | Book p. 38 "body and fundus"; p. 42 "spares the gastric antrum"; "pangastritis" is used only for H. pylori gastritis | IM p. 26: autoimmune gastritis "(pangastritis)" | IM **C3-13** | 3 | V |
| 2 | H. pylori triple therapy: duration and first-line status | Book p. 41: 14 days, "no longer recommended as an empirical first-line choice"; book p. 48: 10–14 days | IM p. 31: 14 days, "one of the most commonly used" | IM **C3-17** | 3 | V |
| 3 | Levofloxacin rescue dose | Book p. 41: 500 mg once daily (+ PPI + amoxicillin) | Book p. 48 and GIT Others p. 5: 250 or 500 mg twice daily for 10 days | OS **C3-D2** (PH-16) | 3 | V |
| 4 | Misoprostol: PGE₁ or PGE₂ analogue | Book p. 37: "synthetic prostaglandin E₂ analogue" | Book p. 48 and GIT Others p. 4: "Synthetic PGE1 analog" | OS **C3-D1** (PH-15) | 3 | V |
| 5 | Commonest site of gastric cancer (%) | Book p. 62: antrum/pylorus 60 %, body 15 %, fundus 25 % | GIT Others p. 15: pyloric 50 %, lesser curvature 25 % | OS **C3-D3** (TU-13) | 3 (and 4) | V |
| 6 | Definition of "acute" diarrhoea | Book p. 77: < 2–3 weeks (rarely 6–8) | IM p. 51: < 4 weeks | IM **C5-08** | 5 | V |
| 7 | Stool fat and lactose breath test protocol | Book p. 93 and IM text p. 68: 70–100 g fat, 2–3 days, lactose 25 g | IM tables pp. 69–70: 100 g, 3 days, lactose 1 g/kg | IM **C5-38** | 5 | V (p. 68), V-img (pp. 69–70) |
| 8 | IBS criteria: frequency threshold | Book p. 102 (Rome V): ≥ 3 days/month for 3 months | IM p. 75 (Rome IV): ≥ 1 day/week for 3 months | IM **C6-16** | 6 | V |
| 9 | Low-FODMAP example foods | Book p. 104: onions, garlic, wheat, rye, legumes | IM p. 75: potatoes, brown rice, oats, almonds | IM **C6-17** | 6 | V |
| 10 | IBS-C second drug option | Book p. 105: prucalopride (linaclotide only in the p. 99 table) | IM p. 75: linaclotide | IM **C6-20** | 6 | V |
| 11 | Granulomas in UC | Book Fig 8.1 p. 117: "should not be present" | IM p. 76 table: "Occasional" (IM p. 77 agrees with the book) | IM **C8-03** | 8 | V-img (p. 117, IM p. 76); IM p. 77 **U** |
| 12 | Systemic steroid doses in IBD | Book pp. 119–120 and IM p. 80 text: methylprednisolone 10–30 mg IV q6–8h; prednisone 40–60 mg/day | IM p. 80 drug table: methylprednisolone 40–60 mg IV daily; prednisone 0.25–0.75 mg/kg/day | IM **C8-17** | 8 | V (text), V-img (table) |
| 13 | Widal: reading of a high H titre | Book p. 109: high titre to **one** H antigen → recent infection; O + > 1 H → immunization | GIT Others p. 24: "**More than one** H antigen … recent infection … and recent immunization" (garbled) | OS **C7-D1** (FI-13) | 7 | V |
| 14 | Colorectal cancer age | GIT Others p. 19: 50–70 y; book Ch 15 p. 196: "old age" | GIT Others p. 20 and book Ch 4 p. 74: 60–79 y | OS **C15-D1** (TU-31) | 15 (and 4) | V |
| 15 | Blood count in amoebic liver abscess | Book Ch 25 p. 331: "Leukocytosis and esinophilia" [sic] | Book Ch 9 p. 138 and GIT Others p. 47: polymorphonuclear leucocytosis | OS **C25-D1** (PA-29) | 25 (and 9) | V |
| 16 | PBC in the serum immunoglobulin list | Book p. 239: "raised IgM" | Hepatology p. 11: "raised AMA" | HEP **A-34** | 18 | V |
| 17 | AIH type 1 frequency | Book p. 275: 80–90 % | Hepatology p. 22 table: 95 % | HEP **B1-24** | 21 | V / V-img |
| 18 | Rest in acute viral hepatitis | Book p. 259: normal activity as tolerated; p. 253 (HAV): rest "unhelpful" | Hepatology p. 31: bed rest mandatory until bilirubin < 1.5 mg/dL | HEP **B1-35** | 19 | V |
| 19 | HBV prevalence in Egypt | Book p. 265: below 2 % | Hepatology p. 35: 5 % | HEP **B2-03** | 20 | V |
| 20 | HBV chronicity by age | Book p. 265: children < 5 y 20–30 %, adults < 5 %; **book p. 247** (not p. 248 as the ledger says): chronic hepatitis in 5–10 % | Hepatology p. 35: children 20–50 %, adults < 10 % | HEP **B2-04** | 20 (and 18) | V (page corrected) |
| 21 | HBV DNA in inactive carriers | Book pp. 266–267: < 2,000 IU/mL | Hepatology p. 35: < 400 IU/L | HEP **B2-10** | 20 | V |
| 22 | Spontaneous HBsAg clearance | Book p. 267: ≈ 1 %/yr | Hepatology p. 35: 1–2 %/yr | HEP **B2-12** | 20 | V |
| 23 | Egyptian HCV screening | Book p. 273: ≈ 60 million screened | Hepatology p. 39: > 49 million, prevalence 4.4 % | HEP **B2-30** | 20 | V |
| 24 | Metformin in NAFLD/MASH | Book p. 279: not recommended specifically for MASH | Hepatology p. 44: listed as an insulin sensitiser to use | HEP **C-02** | 21 | V |
| 25 | Fetor hepaticus | Book p. 283: sweet, musty (volatile sulphur compounds) | Hepatology p. 46: faecal smell (mercaptans from the colon) | HEP **C-08** | 22 | V |
| 26 | **Protein intake in HE** (three positions) | Book p. 286: no restriction, 1.2–1.5 g/kg/day even in HE; temporary reduction only in severe overt HE. **Book p. 359 (new in this audit): "In the acute attack dietary protein is reduced to 20 g/day"**, then normal intake (1.2 g/kg/day) | Hepatology p. 48: restrict to 30–40 g/day in encephalopathy | HEP **C-13** (+ this audit) | 22 and 30 | V |
| 27 | PBC diagnostic criteria | Book p. 288: two of three | Hepatology p. 51: all three "mandatory" | HEP **C-15** | 22 | V |
| 28 | UDCA effect in PBC | Book p. 288: slows fibrosis, improves survival | Hepatology p. 51: "no effect on the disease process" | HEP **C-16** | 22 | V |
| 29 | Alcohol threshold for cirrhosis | Book p. 281: > 30 **ml**/day for > 10 y | Hepatology pp. 55 (44): ≥ 30 **g**/day for > 10 y | HEP **C-26** | 22 | V |
| **G1** | **Transfusion target / trigger in acute upper GI (variceal) bleeding** | Book p. 315: restrictive, Hb ≈ 7–8 g/dL. Book p. 51: Hb a poor guide to transfusion | Hepatology p. 61: Hct ≈ 30 (HEP **D-24**). **IM p. 39: transfuse if Hb < 10 "mg/dl" with recent or active bleeding (IM GB-07/08, retained and printed)** | HEP **D-24** (ledger) + IM **GB-07/08/09/11** (retained) | 23 and 3 | V |
| **G2** | **Nasogastric tube / lavage in GI bleeding** | Book p. 315: selective, "not routinely required" | Hepatology p. 61: Ryle's tube routine (HEP **D-25**). **IM p. 40: NG tube for gastric wash; IM p. 46: NG lavage in unstable lower GI bleeding (retained)** | HEP **D-25** (ledger) + IM **GB-09**, **GB-25** (retained) | 23 and 3 | V |
| 30 | Screening endoscopy in cirrhosis | Book p. 285 (Baveno VII, some patients avoid endoscopy) and p. 313; Hepatology p. 48 (≤ 20 kPa and platelets > 150 → no endoscopy; HEP C-11 retained) | Hepatology p. 61: "Every patient … should have an upper GI endoscopy" | HEP **D-26** | 22 and 23 | V |
| 31 | HRS: terlipressin escalation and albumin dose | Book p. 347 and Hepatology p. 80 text: escalate "after 2 days" to max 12 mg/day; albumin 20–40 g/day | Hepatology p. 80 image table: escalate to 2 mg q4h if creatinine not improved by 25 % "at day 3"; albumin 20–60 g/day | HEP **E-37** | 28 | V / V-img |
| 32 | Fate of the reabsorbed 10–20 % of urobilinogen | Book p. 245: escapes the enterohepatic circulation and is excreted in urine | Hepatology p. 82: re-excreted by the liver | HEP **F-04** | 18 | V |
| 33 | Mechanism category for Gilbert's | Book p. 245: under "Decrease uptake" ("uptake and/or conjugation") | Book p. 350 and Hepatology pp. 83–84: decreased conjugation | HEP **F-05** | 18 and 29 | V |

This accounts for all 35 input flags (IM 9, OS 6, HEP 20): rows 1–33 plus G1 and G2.

### 4.2 New tensions found in this audit (not flagged by any input)

| # | Topic | Position A | Position B | Retained entry affected | Book ch | Verif |
|---|---|---|---|---|---|---|
| N1 | Frequency of SBP | Book p. 343: 10 % of cirrhotic patients | Hepatology p. 75: ≈ 8 % of cirrhotics **with ascites** | HEP **E-21** (printed) | 27 | V |
| N2 | Early rebleeding after endoscopic therapy | Book p. 316: rebleeding within 10 days → repeat endoscopic therapy | Hepatology p. 62: TIPS if rebleeding within 5 days of endoscopic therapy | HEP **D-16** (printed) | 23 | V |
| N3 | Rectal involvement in UC | Book Fig 8.1 p. 117: "Typically involved" | IM p. 76 table: "Always" (same table as flag 11) | IM **C8-02** (printed) | 8 | V-img |
| N4 | Corticosteroids and GI bleeding | Book p. 50: avoid NSAID + corticosteroid combinations except in selected cases | IM p. 37: corticosteroids in usual doses have no influence on GI haemorrhage | IM **GB-03** (printed; the parenthetical notes it) | 3 | V |
| N5 | Stopping antithrombotics | Book p. 50: interrupting antiplatelets requires specialist assessment (thrombosis risk) | IM p. 40: "Clopidogrel and warfarin are also stopped" (with a cardiologist-discussion qualifier) | IM **GB-11** (printed) | 3 | V |

N4 and N5 are soft; the IM entries already carry the qualifier. N1–N3 need either a CHECK entry or side-by-side wording.

### 4.3 Internal to one source (context; no action unless the text is printed)

| # | Item | Where | Raised by | Verif |
|---|---|---|---|---|
| I1 | "Terlipressin … **should** be given to patients with ischaemic heart disease" (garble; book says "caution") | Hepatology p. 62 vs book p. 315 | HEP REPORT "also noted" | V |
| I2 | Rifaximin "alters the intestinal flora **with** any systemic side effects" (garble, copied into the book) | Hepatology p. 91; **book p. 359** | HEP REPORT | V |
| I3 | Child-Pugh C "> 10" (B is 7–9) | Hepatology p. 49 | HEP REPORT | V |
| I4 | Hepatic copper in Wilson disease: "≥ 250" vs "> 250" µg/g | Book p. 250 vs p. 297 | HEP REPORT | V |
| I5 | HCV chronicity: "55–85 %" and "80 %" on the **same** page | Book p. 271 | HEP REPORT | V |
| I6 | Conjugated fraction: "direct > 15 %" vs "> 50 %" | Book p. 354 vs p. 246 | HEP REPORT | p. 246 V; **p. 354 U** (not in extractable text; probably an image) |

Also internal to one source, and already covered above: IM p. 68 text vs pp. 69–70 tables (row 7); IM p. 80 text vs table (row 12); GIT Others p. 19 vs p. 20 (row 14); GIT Others p. 18 table vs text on the 40 % figure (§3, S11); book p. 37 vs p. 48 (rows 3–4) and p. 41 vs p. 48 (row 2).

---

## 5. Retained additions already present in the main book (Task 5)

More than 100 retained entries were spot-checked: IM 40, all 18 OS additions, and about 70 HEP points. For each, key phrases or numbers were searched on the cited page and nearby pages (regexes in `auditB/spot.py` and `spot2.py`).

**Key to the Status column:**
- **LARGELY PRESENT:** most of the entry's teaching is already on the book page, so the entry should be trimmed.
- **PARTLY:** the book has part of it; what is new is named.
- **NEW:** not found in the book.

### 5.1 Largely already in the book (trim before merging)

| Entry | Text already in the book | Book page | What is actually new |
|---|---|---|---|
| IM **C3-21/27**, 3rd bullet, 2nd sentence | "Because of the large number of patients on NSAIDs including low-dose aspirin for vascular prophylaxis, this is a significant problem, particularly in the elderly." | **p. 36** | The 5 % and 1–2 % figures; PGF2α; chronic and asymptomatic erosive gastritis |
| IM **GB-07/08/09/11**, "Hb falls late because haemodilution has not yet occurred" | "Hemoglobin levels are generally a poor indicator of the need to transfuse because anemia does not develop immediately." | **p. 51** | Pulse and venous pressure as guides; CVP; 2 units; shock criteria |
| IM **GB-07/08/09/11**, antiplatelet bullet; IM **GB-22** "stopping antiplatelets carries a high risk" | "interruption of antiplatelet therapy requires specialist assessment because of thrombosis risk"; also "Monitor pulse and BP frequently", group & cross-match, "keep NPO" | **p. 50** | Cardiologist and high-dependency beds; PCI setting |
| IM **C5-19**, last sentence | "Clostridium difficile infection is often difficult to clear, and five or more relapses have been observed" | **p. 83** | Pathogenesis, diagnosis and treatment |
| OS **C4-8**, "Number" row (tubular multiple / villous solitary) and villous "sessile" | Tubular adenomas "commonly multiple, with 10–20 lesions"; villous "a single large, sessile lesion" | **p. 73** | Size (< 1 cm vs > 2 cm) and dysplasia/cancer risk |
| HEP **A-29** (jaundice-type table) | Haemolytic: indirect ↑, urine urobilinogen ↑, urine normal colour, stool dark. Obstructive: direct ↑, urine dark, urobilinogen ↓ or absent, stool clay. Hepatic: both ↑, urine dark, urobilinogen ↑ early then ↓. | **pp. 245–246** | Only the hepatic "stool clay" cell and "bile salts" in urine |
| HEP **E-14** (diuretic regimen) | "Bed rest is advised"; daily body weight; "Spironolactone alone … 100–200 mg daily"; combination spironolactone 100 mg + furosemide 40 mg. Diuretic-limiting complications are listed on p. 342. | **pp. 341–342** | 70–90 mmol sodium diet; "after 4 days"; stop criteria (flap, alkalosis, azotaemia) |
| HEP **E-24** caution ("tap any cirrhotic who deteriorates, e.g. with encephalopathy") | "should be suspected in any cirrhotic patient with ascites who clinically deteriorates. The patient becomes drowsy and confused" | **p. 343** | "Classic features may be absent" |
| HEP **E-28/29** (HRS mechanism) | "the histology of the kidney is normal … hallmark of HRS is renal vasoconstriction … Peripheral and splanchnic vasodilation … Activation of RAAS, ADH, sympathetic" | **p. 346** | Cardiac dysfunction; "capable of normal function"; tense ascites |
| HEP **C-28** (A1AT gene analysis) | "Phenotyping or genotyping of the SERPINA1 gene (the PiZZ genotype …)" | **p. 300** | Only the naming of the M and S phenotypes |

### 5.2 Partly present (keep, but consider cutting the part the book already has)

| Entry | Already in the book (page) | New part |
|---|---|---|
| IM C1-19/20 | p. 4: "Massive upper GI bleed: fresh blood per rectum + shock. Hematochezia … usually lower GI source"; p. 50 same | "Without shock always lower GI"; ligament of Treitz; rapid transit |
| IM C1-23/24/25/26 | p. 6: colonoscopy "stricture dilatation and stenting"; sigmoidoscopy rigid/flexible; p. 7: balloon enteroscopy, capsule endoscopy | Benign → dilate / malignant → stent; 20–25 cm; splenic flexure; avoid capsule if a stricture is suspected |
| IM C3-05/06 | p. 35: definition of gastropathy | Causes of gastropathy; classification of gastritis |
| IM C3-08/09/11 | p. 36: surgery, trauma, burns, CNS injury; self-resolving; alcohol, caffeine, smoke; p. 42: "self-limiting within days to weeks" | MI and stroke; H2 blocker |
| IM C3-18/19 | p. 41: clarithromycin resistance; "metronidazole resistance is high (> 50 %)" | "No single drug is effective"; who to treat |
| IM GB-19/20/21/22 | p. 52: "Eradicate H. pylori when present. Continue PPI therapy"; Mallory–Weiss "usually follows retching … most bleeding stops spontaneously" | PPI for 4 weeks; confirm eradication; retching may be absent; bleeding gastric cancer |
| IM GB-28/29 | p. 53: "hookworm is an important worldwide cause"; "investigate both upper and lower GI tract"; capsule preferred | "Most common" cause (hookworm); occult blood unhelpful; same-session endoscopy; 60–85 % yield |
| IM C5-02/03 | p. 77: "about 9 L of fluid is delivered to the small intestine" | Breakdown table; passive water movement |
| IM C5-35 | p. 93: quantitative culture of aspirate; 50 g glucose breath test, 90 % for 10⁵ bacteria | Early vs late peak; ¹⁴C-xylose test |
| IM C5-37 | p. 93: SeHCAT method; small-bowel biopsy heading | < 10 % cut-off; biopsy diagnostic list; Schilling no longer used |
| IM C6-08 | p. 98: anorectal manometry, balloon expulsion, defecography "measure pressures inside the rectum and anus" | Resting and squeeze pressures; MRI defecography |
| OS C4-3 | p. 72: pernicious anaemia (atrophic gastritis type A), H. pylori chronic gastritis, "On top of intestinal metaplasia" | Dysplasia step; "precancerous" label |
| OS C4-5 | p. 72: "Malignant ulcer with raised, everted edges" | > 5 cm; necrotic floor; firm base |
| OS C7-1 | p. 107: "non-lactose fermenter on MacConkey"; "partial sugar fermentation" | Facultative anaerobe; 37 °C, 24 h; acid + gas vs S. typhi acid only |
| OS C7-4 | p. 110: S. typhimurium "last for 2–5 days" | Spontaneous cure |
| OS C7-5 | p. 111: "Care to avoid oxygen exposure"; "darting motility in wet mount" | Rectal swab; dark-field illumination; biotyping, serotyping, phage typing |
| OS C7-6 | p. 111: "Aerobic, require enriched media containing serum" | 10 % CO₂ |
| HEP A-12/30/31 | p. 238 and p. 244: albumin half-life 21 days, not a good indicator of acute injury; p. 246: PT depends on coagulation factors (II, VII, IX, X) | Albumin as a prognostic marker; PT earlier than albumin; factor list |
| HEP A-14/15 | p. 245: > 3-fold rise in cholestasis; ALP in bone disease | Space-occupying lesions |
| HEP A-21/22 | p. 245: Crigler–Najjar severe form, complete absence of UDGT, > 20 mg/dL; p. 246: Dubin–Johnson secretion defect | Type II < 20; pigmented liver; Rotor |
| HEP A-26/28 | p. 246: ↑ reticulocytes; ↑ cholesterol | LDH; β-lipoproteins |
| HEP F-02 / F-03 | p. 245: uptake → conjugation to glucuronic acid → excretion; "gut bacteria deconjugate most bilirubin to colourless urobilinogen" | Ligandin; cytosolic binding; β-glucuronidase; site |
| HEP B1-07 / B1-08 | p. 248: anti-HBc "only positive marker in window period"; natural immunity = HBsAb + HBcAb, vaccination = HBsAb only; IgM anti-HBc = recent infection | Tabular panel; "not yet completely resolved" |
| HEP B1-02 | p. 252: "PT is prolonged in severe cases" | PT as the prognostic indicator; > 3 s |
| HEP B1-15/16/17 | p. 254: chronic HEV "in some immunosuppressed patients in solid-organ transplant recipients" | Genotypes; pork; chemotherapy and HIV |
| HEP B1-18 | p. 249: HGV "Mode of transmission is parenteral" | ≈ 1 % of donors |
| HEP B2-09/11 | p. 267 and p. 268: reactivation during chemotherapy or immunosuppression | Prophylaxis indicated; found at donation screening |
| HEP B2-15/16 | p. 270: PEG-IFN 180 µg weekly, **48 weeks** | 25–45 % response; 3× ULN |
| HEP B1-23 | p. 275: type 1 ANA/ASMA; type 2 LKM-1/LC-1 | Antibody percentages; IgG; age; cirrhosis 45/80 % |
| HEP C-17 / C-21/23 / C-22 / A-41 | p. 287: fat-soluble vitamin malabsorption; p. 292: bronze pigmentation, HCC risk; p. 293: MRI for hepatic iron; p. 295: KF rings (Descemet, slit lamp) | Supplements and ductular proliferation; melanin; 30 % HCC; pancreatic iron; gold colour and "first sign" |
| HEP E-01, E-11/12, E-16/17, E-18/19/20, E-21/22, E-23, E-25/26, E-32/33, E-36 | p. 338: cirrhosis 80 %, TB, malignancy; p. 340: SAAG ≥ 1.1; p. 342: "resistant" definition; LVP > 5 L with albumin; TIPS → HE; p. 343: monomicrobial, translocation, ↓ opsonins, 3rd-generation cephalosporins; p. 344: norfloxacin 400 mg/12 h with sclerotherapy (truncated); p. 346: 2 days of diuretic withdrawal + albumin 1 g/kg, nephrotoxins (NSAIDs, aminoglycosides, contrast); p. 347: noradrenaline and midodrine + octreotide as alternatives | See each HEP entry: percentages, schedules, doses, extra causes |
| HEP D-07 / D-11/13 / D-12/15 | p. 313: "significant proportion of deaths"; p. 315: terlipressin 2–5 days, Histoacryl for large gastric varices; p. 316: balloon tamponade "rarely used" | One-third; systolic BP target; dose; large oesophageal varices; indication for tamponade |
| HEP F-13 | p. 360: BCAAs low, aromatic amino acids high | Hyperinsulinaemia mechanism; false neurotransmitters |

### 5.3 Checked and found new (no book text found on or near the cited pages)

- **IM:** C1-02 (20 % of cancers), C1-05/06/08 (CTZ, retching), C1-09 (flatulence), C1-12 (porphyria), C1-32 (CO₂ insufflation), C2-14 (large hernia and complications as indications; book p. 20 has only "all symptomatic" and "failure of medical treatment"), C3-02/03 (mucins; acid not essential), C3-14 (metaplasia / atrophic gastritis in Ch 3), GB-03 (75 mg aspirin), GB-04/31 (85 %; 5–12 %), C5-17 (Na–glucose coupled uptake), C5-26 (absorption sites), C5-31 (IgA deficiency, Down syndrome, microscopic colitis), C5-34/36 (steatocrit, D-xylose numbers), C6-03/04 (obstipation), C6-10/11/13/15 (fibromyalgia, TSH), C8-11 (Behçet's, radiation colitis, Yersinia), C8-13/23 and C8-14/15 (5-ASA, budesonide: 0 hits in pp. 115–121), C8-20/21 (6-MP, adalimumab, natalizumab).
- **OS:** C3-1 (osteoporosis; book p. 45 lists B12 deficiency only), C4-1, C4-2, C4-4, C4-6, C4-7, C7-2, C7-3, C14-1, C15-1, C15-2, C15-3.
- **HEP:** A-02, A-03, A-06, D-18, D-19, D-20, A-11, A-18, F-01, F-07, D-21, C-01, C-05/06/07, C-10, C-11/12 (numbers), D-01…04, D-05, D-08/09/10, D-16/17, E-04/05, E-08/09, A-25, A-27, F-06, F-10, F-12/15, F-14, F-16, F-18, B2-01, B2-05/06/07, B2-08, B2-14, B2-23.

---

## 6. Merge-level notes (affect the integrated PDF)

1. **Chapter-level "no additions" notes become false once the handouts are merged.** Each must be relabelled as source-specific ("GIT Internal Med adds nothing here") or deleted:
   - **IM Ch 4:** "No substantive additions identified". OS has 8 additions in Ch 4.
   - **IM Ch 7:** "No substantive additions identified". OS has 6 additions and 1 flag.
   - **IM Ch 14:** OS adds C14-1.
   - **IM Ch 15:** "No substantive additions … pp. 195–197". OS adds C15-1, C15-2 and C15-3, all at p. 196.
   - **IM Ch 9:** fine. OS also has no Ch 9 additions, but OS C25-D1 cites p. 138.
   - **OS "checked" list:** "the remaining 34 chapters were checked and have nothing to add" (REPORT and capsule end list). IM and HEP add to many of those chapters. The Ch 19, 22 and 23 rows of that list would sit beside HEP additions.
   - **HEP how-to note:** "Chapters with nothing new (24–26, 32–40) are omitted". Ch 25 now has an OS CHECK entry.
2. **IM's Ch 7 note and Ch 13 note** point to "Chapter 5" and "Chapter 1 of this companion". In the merged PDF these internal references need to become chapter numbers or links.
3. **Discrepancy presentation differs by handout.**
   - IM and OS print their discrepancies as CHECK/discrepancy boxes.
   - HEP prints none; its 20 are in the ledger only.
   - A merged PDF should adopt one policy. Otherwise the G1 and G2 groups end up with the IM side printed as settled teaching and the HEP side hidden.
4. **Terminology and units to align.**
   - Hb "mg/dl" as IM prints it (IM GB-07) against the book's g/dL.
   - "Ryle's tube" vs "nasogastric tube".
   - PGE₁ vs PGE₂ (row 4).
