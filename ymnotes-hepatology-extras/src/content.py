"""Authoring source for content.json (editable). Each item carries ledger ids.
Run: python3 content.py  -> writes content.json"""
import json, pathlib
C = []
def ch(no, title, pages, subjects, nav=None):
    c = {"id": f"ch{no}", "no": no, "title": title, "book_pages": f"Book pp. {pages}", "subjects": subjects,
         "subline": f"<b>Adds to book pp. {pages}</b> · {subjects}", "topics": []}
    if nav: c["nav"] = nav
    C.append(c); return c
def tp(c, title, book=None):
    t = {"title": title, "items": []}
    if book: t["book"] = book
    c["topics"].append(t); return t
def it(t, kind, text, book, src, ids, **kw):
    d = {"kind": kind, "text": text, "book": book, "src": src, "ledger": ids}; d.update(kw); t["items"].append(d)

# ---------------- 17
c = ch("17", "Hepatology and Hepatic Surgery", "231–235", "Surgery", nav="Hepatology and Hepatic Surgery")
t = tp(c, "Liver functions and lobular zonation", "pp. 233–235")
it(t, "fact", "Principal liver functions: bile formation and secretion; metabolism of carbohydrates, amino acids, lipids and water- and fat-soluble vitamins; inactivation of ammonia (urea cycle), toxins, steroids and other hormones; synthesis of acute-phase proteins, albumin, clotting factors and steroid/hormone-binding proteins; immune function (Kupffer cells).", "p. 233", "p. 64", ["D-19"])
it(t, "mechanism", "Metabolic zonation: the <b>periportal</b> zone carries out gluconeogenesis and cholesterol and urea synthesis; the <b>pericentral</b> zone carries out glycolysis and glutamine and bile-acid synthesis.", "p. 235", "p. 64 (figure)", ["D-20"])

# ---------------- 18
c = ch("18", "Liver Disease Assessment", "236–250", "Radiology / Investigation · Internal Medicine")
t = tp(c, "Symptoms and signs of chronic liver disease", "pp. 237–238")
it(t, "fact", "Palmar erythema is persistent redness of the palms; spider naevi are small red skin marks caused by dilated capillaries near the skin surface.", "p. 238", "p. 1", ["A-02"])
it(t, "mechanism", "The bleeding tendency reflects failed hepatic synthesis of fibrinogen and factors II, V, VII, IX, XI, XII and XIII.", "p. 238", "p. 1", ["A-03"])
it(t, "mechanism", "Hyperdynamic circulation: flushed extremities, bounding pulses and capillary pulsations, with increased portal blood flow, low blood pressure and reduced systemic vascular resistance.", "p. 237", "p. 2", ["A-04"])
it(t, "mechanism", "The vasodilators are probably multiple: formed by the sick hepatocyte, not inactivated by it, or bypassing it through intra- or extra-hepatic portosystemic shunts. They activate the sympathetic and renin–angiotensin systems, promoting sodium and water retention and ascites.", "p. 237", "p. 2", ["A-05"])
it(t, "mechanism", "<b>Nitric oxide</b> (endothelium-derived, potent vasodilator) is implicated in the hyperdynamic circulation and is important in ascites, hepatorenal syndrome and portal hypertension. Prostanoids released into the portal vein and endocannabinoids are also shown as splanchnic vasodilators; cardiac output rises.", "p. 237", "p. 2 (text + figure)", ["A-06", "A-07"])
it(t, "fact", "Hepatocellular failure complicates almost all liver diseases but <b>not portal venous occlusion alone</b>; it may be the terminal event in chronic cholestasis such as primary biliary cirrhosis. Its picture and treatment are similar whatever the cause.", "pp. 237–238", "p. 64", ["D-18"])
t = tp(c, "Liver function tests", "pp. 238, 244–246")
it(t, "fact", "The liver synthesises albumin, <b>all clotting factors except factor VIII</b>, carrier proteins (ceruloplasmin, transferrin), cholesterol, bile salts and urea.", "p. 244", "p. 5", ["A-11"])
it(t, "investigation", "Tests grouped by what they reflect: excretory/detoxification (serum and urine bilirubin, serum ammonia); liver-cell injury (AST, ALT); cholestasis (ALP, GGT, 5′-nucleotidase); synthetic function (albumin, coagulation factors). 5′-nucleotidase is more specific for cholestasis than ALP but is not widely used.", "p. 245", "pp. 6, 87 (table)", ["F-08", "A-16"])
it(t, "investigation", "A falling serum albumin is an excellent indicator of severity and prognosis in chronic liver disease. PT depends on factors I, II, V, VII and X; because these have a shorter half-life than albumin, PT is an <b>earlier</b> indicator of severe liver injury.", "pp. 244, 246", "pp. 5, 10", ["A-12", "A-30", "A-31"])
it(t, "distinction", "ALP and GGT are markedly raised (&gt;3-fold) not only in cholestasis but also with <b>space-occupying lesions</b> such as cancer; non-hepatic ALP rises occur in bone disease (rickets, osteomalacia).", "p. 245", "p. 6", ["A-14", "A-15"])
it(t, "investigation", "Causes of an <b>isolated</b> ALP rise: primary or metastatic hepatic tumours, granulomatous liver disease, primary biliary cirrhosis, non-Hodgkin lymphoma, hyperthyroidism, bone disease with rapid turnover, sclerosing cholangitis.", "p. 245", "p. 87 (table)", ["F-07"])
it(t, "distinction", "<b>Hepatic infiltration</b> (tumours, cysts, lymph nodes): ALP and GGT markedly raised while bilirubin may be normal — partial obstruction lets bilirubin pass yet stimulates ALP/GGT synthesis; AST/ALT normal or slightly raised (AST &gt; ALT); AFP rises in HCC and CEA with GIT-cancer secondaries.", "p. 245", "p. 20", ["B1-19"])
t = tp(c, "Bilirubin and bile-acid metabolism", "p. 245")
it(t, "fact", "About 250–300 mg of bilirubin is produced daily; 70–80% comes from haemoglobin of senescent red cells, the rest from prematurely destroyed erythroid cells in the marrow and turnover of haemoproteins such as myoglobin. It is formed in reticuloendothelial cells, mainly in the spleen and liver.", "p. 245", "p. 81", ["F-01"])
it(t, "mechanism", "Hepatocyte handling has four steps — uptake, cytosolic binding, conjugation, secretion: albumin-bound bilirubin is taken up (albumin is not), binds <b>ligandin (Z protein)</b>, is conjugated to glucuronic acid by UDP-glucuronosyl transferase in the endoplasmic reticulum, and mono- and diglucuronides are actively transported into bile.", "p. 245", "pp. 7, 81–82", ["F-02", "A-19", "A-17"])
it(t, "mechanism", "Conjugated bilirubin is not absorbed by the intestinal mucosa; only in the distal ileum and colon is it hydrolysed (bacterial β-glucuronidases) to unconjugated bilirubin, then reduced to colourless urobilinogens.", "p. 245", "pp. 7, 82", ["F-03", "A-17"])
it(t, "fact", "The primary bile acids, cholic and chenodeoxycholic acid, are made from cholesterol, secreted in bile, and mostly reabsorbed in the ileum for re-secretion (enterohepatic circulation).", "p. 245", "p. 7", ["A-18"])
t = tp(c, "Types of jaundice", "pp. 245–246")
it(t, "distinction", "Side-by-side comparison of the three types:", "pp. 245–246", "pp. 9–10 (table)", ["A-29"],
   table={"head": ["", "Haemolytic", "Obstructive", "Hepatic"], "rows": [
     ["Serum bilirubin", "Indirect ↑", "Direct ↑", "Both ↑"],
     ["Urine urobilinogen", "↑", "↓", "↑ early, then ↓"],
     ["Urine bilirubin / bile salts", "Absent", "Present", "Present"],
     ["Urine colour", "Normal", "Dark", "Dark"],
     ["Stool colour", "Dark", "Clay", "Clay"]]})
it(t, "investigation", "In haemolytic jaundice, evidence of haemolysis includes raised reticulocytes <b>and raised LDH</b>. Obstructive jaundice raises serum cholesterol and <b>β-lipoproteins</b>.", "p. 246", "p. 9", ["A-26", "A-28"])
it(t, "distinction", "Crigler-Najjar <b>type II</b> = partial UGT deficiency, bilirubin &lt;20 mg/dL (type I: complete absence, &gt;20 mg/dL). Dubin-Johnson (defect of bilirubin secretion) has a <b>darkly pigmented</b> liver; Rotor syndrome is usually asymptomatic with a non-pigmented liver.", "p. 245–246", "p. 8", ["A-21", "A-22"])
t = tp(c, "Viral hepatitis markers", "pp. 247–250")
it(t, "investigation", "HBV serology panels:", "p. 248", "p. 17 (tables)", ["B1-08", "B1-09"],
   table={"head": ["HBsAg", "Anti-HBc", "IgM anti-HBc", "Anti-HBs", "Interpretation"], "rows": [
     ["−", "−", "", "−", "Susceptible"],
     ["+", "+", "+", "−", "Acutely infected"],
     ["+", "+", "−", "−", "Chronically infected"],
     ["−", "+", "", "+", "Immune — natural infection"],
     ["−", "−", "", "+", "Immune — vaccination"]]})
it(t, "distinction", "Acute vs chronic vs past HBV: HBeAg and HBV DNA are + early then − in acute infection, ± in chronic, − in past; anti-HBe is − early then + (acute), ± (chronic), + (past); ALT is markedly raised (acute), mildly–moderately raised (chronic), normal (past).", "p. 248", "p. 17 (table)", ["B1-09"])
it(t, "investigation", "An isolated anti-HBc in the window period usually means a resolving acute infection that is <b>not yet completely resolved</b>, because anti-HBs has not yet appeared.", "p. 248", "p. 17", ["B1-07"])
it(t, "caution", "In hepatitis B and C, normal ALT/AST does not prove recovery — replication may persist, so clearance must be shown serologically.", "p. 247", "p. 14", ["B1-03"])
it(t, "investigation", "HAV can be detected by <b>PCR on faeces</b>, earlier than serology, but this is very rarely performed.", "p. 247", "p. 15", ["B1-04"])
it(t, "caution", "Anti-HCV: a positive result may be false (cross-reactivity with another infection) and must be confirmed by PCR; a negative result does not exclude HCV (immunodeficiency; very early infection before seroconversion — do PCR). <b>Anti-HCV IgM is not a marker of acute infection</b>.", "pp. 248–249", "p. 18", ["B1-12", "B1-13"])
it(t, "distinction", "Chronic hepatitis at a glance:", "p. 250", "p. 21 (table)", ["B1-22"],
   table={"head": ["", "Autoimmune", "HBV", "HCV"], "rows": [
     ["Sex", "Female", "Male", "Equal"],
     ["Age", "15–25 y", "Older", "All ages"],
     ["Associated autoimmune disease", "Frequent", "Rare", "Occasional"],
     ["Autoantibodies", "High titre (ANA, ASMA, LKM)", "Low / absent", "Low / absent"],
     ["Cancer risk", "Low", "High", "High"]]})

# ---------------- 19
c = ch("19", "Acute Hepatitis", "251–263", "Internal Medicine")
t = tp(c, "Course and prognosis", "pp. 252, 257")
it(t, "fact", "Acute viral hepatitis usually resolves 4–8 weeks after symptom onset.", "p. 257", "p. 14", ["B1-01"])
it(t, "investigation", "Severity is judged by impaired synthetic function rather than ALT/AST levels: <b>PT</b> is the key prognostic indicator, and a PT more than 3 seconds above normal carries a poor prognosis.", "p. 252", "p. 14", ["B1-02"])
t = tp(c, "Virology and transmission", "pp. 254–256")
it(t, "fact", "HBV is present in all body fluids <b>except stool</b>, so spread is by blood or body-fluid contact.", "p. 255", "p. 16", ["B1-06"])
it(t, "fact", "HCV (enveloped ssRNA flavivirus) is the most common cause of transfusion-associated hepatitis; sexual transmission is low.", "p. 256", "p. 18", ["B1-11"])
it(t, "mechanism", "HDV causes infection only when it is <b>encapsulated with HBsAg</b> — the basis of its dependence on HBV.", "p. 255", "p. 19", ["B1-14"])
it(t, "fact", "HEV: genotypes 1 and 2 cause waterborne outbreaks; genotypes 3 and 4 cause sporadic cases, including via undercooked meat such as pork. It affects mainly adults and is rare in children. Chronic (genotype 3) hepatitis E occurs only in the immunocompromised — organ-transplant recipients, cancer chemotherapy, HIV.", "pp. 254, 258", "p. 19", ["B1-15", "B1-16", "B1-17"])
it(t, "fact", "Hepatitis G is spread by contaminated blood or blood products; prevalence in blood donors is about 1%.", "p. 249", "p. 20", ["B1-18"])
t = tp(c, "Chronic hepatitis", "p. 263")
it(t, "fact", "In severe chronic hepatitis, fibrous septa extend into the lobule, producing <b>rosette formation</b> as well as bridging fibrosis.", "p. 263", "p. 34", ["B2-01"])

# ---------------- 20
c = ch("20", "Chronic Hepatitis B", "264–273", "Internal Medicine · Pharmacology", nav="Chronic Hepatitis B (and C)")
t = tp(c, "Natural history of HBV", "pp. 265–267")
it(t, "fact", "Chronic HBV is more common in males. About 50% of HBsAg carriers have evidence of replication (HBeAg / HBV DNA positive), and about 20% of carriers develop cirrhosis within 5 years of disease onset.", "p. 265", "p. 35", ["B2-05", "B2-06", "B2-07"])
it(t, "fact", "Immune-tolerant patients (mostly infected perinatally) often lose tolerance in the 3rd–5th decade, when acute hepatitis develops and chronic hepatitis may follow.", "p. 266", "p. 35", ["B2-08"])
it(t, "management", "Inactive carriers are usually discovered on screening before blood donation. Reactivation can occur with cancer chemotherapy or bone-marrow transplantation, so <b>antiviral prophylaxis is indicated</b> in these settings.", "p. 267", "p. 35", ["B2-09", "B2-11"])
t = tp(c, "Treatment of HBV", "pp. 269–271")
it(t, "fact", "When HBeAg disappears, remission is usually sustained for many years.", "p. 269", "p. 36", ["B2-14"])
it(t, "management", "Pegylated interferon α-2a for 48 weeks gives response rates of about 25–45%; response is best in younger patients with ALT about 3× the upper limit of normal.", "pp. 270–271", "p. 36", ["B2-15", "B2-16"])
it(t, "management", "Entecavir: HBV DNA becomes negative by 48 weeks in 67% (HBeAg-positive) and 90% (HBeAg-negative). Tenofovir can be used for lamivudine mutations but not alone for adefovir mutations. Lamivudine (100 mg/day) is well tolerated but limited by resistance from the <b>YMDD mutant</b>.", "p. 270", "p. 37", ["B2-17", "B2-18", "B2-19"])
t = tp(c, "Hepatitis C (within this chapter)", "pp. 271–273")
it(t, "mechanism", "DAAs target specific HCV <b>non-structural (NS) proteins</b> vital for viral replication, disrupting replication and infection.", "p. 272", "p. 38", ["B2-23"])
it(t, "management", "Sofosbuvir: 400 mg once daily with or without food; adverse effects (~10%) fatigue, headache, anorexia, insomnia. Ribavirin (adjuvant): 600–1200 mg/day by weight; adverse effects haemolytic anaemia, teratogenicity, sperm abnormalities.", "pp. 272–273", "p. 38", ["B2-24", "B2-26"])
it(t, "fact", "Egypt's HCV burden also reflects nosocomial spread through inadequately disinfected equipment (e.g. circumcision, dental practice), besides the antischistosomal injection campaigns.", "p. 273", "p. 39", ["B2-28"])

# ---------------- 21
c = ch("21", "Autoimmune Hepatitis", "274–279", "Internal Medicine")
t = tp(c, "AIH subtypes", "p. 275")
it(t, "distinction", "Autoantibody pattern and outcome by type:", "p. 275", "p. 22 (table)", ["B1-23"],
   table={"head": ["", "Type 1", "Type 2"], "rows": [
     ["Autoantibodies", "ANA alone 10% · ASMA alone 35% · both 50% · neither 5%", "LKM-1, LC-1"],
     ["Serum IgG", "+++", "+"],
     ["Usual age", "10 years to elderly", "2–18 years"],
     ["Progression to cirrhosis", "≈45%", "≈80%"]]})
t = tp(c, "Fatty liver (MASLD) management", "p. 279")
it(t, "management", "Weight loss should be gradual — <b>not more than 1.6 kg per week</b> — because rapid weight loss increases fibrosis.", "p. 279", "p. 44", ["C-01"])

# ---------------- 22
c = ch("22", "Liver Cirrhosis", "280–307", "Internal Medicine · Pathology")
t = tp(c, "Aetiology and consequences", "pp. 281–282")
it(t, "fact", "Some cirrhosis is <b>cryptogenic</b> (no identifiable cause).", "p. 281", "p. 65", ["D-21"])
it(t, "mechanism", "Cirrhosis causes disease by two routes: <b>altered hepatic blood flow</b> (portal hypertension → variceal bleeding, ascites, encephalopathy; ascites → SBP, HRS) and <b>reduced functional cell mass</b> (less detoxification of bilirubin, ammonia and drugs; less albumin and clotting-protein synthesis).", "p. 282", "p. 65 (figure)", ["D-22"])
t = tp(c, "Clinical picture and investigations", "pp. 282–284")
it(t, "fact", "Recurrent pancreatitis (especially in alcoholics) is among the associated conditions. Fever may be due to portal bacteraemia or liver-cell necrosis, not only infection. Feminization in males is seen in long-standing cases and usually indicates <b>decompensation</b>.", "p. 282", "p. 45", ["C-05", "C-06", "C-07"])
it(t, "investigation", "Urine urobilinogen is increased in cirrhosis.", "p. 284", "p. 47", ["C-10"])
t = tp(c, "Varices screening without endoscopy", "p. 285")
it(t, "investigation", "Liver stiffness <b>≤20 kPa with platelets &gt;150 × 10⁹/L</b>: screening endoscopy not needed (large varices &lt;5%). Liver stiffness <b>&gt;25 kPa</b> is sufficient to diagnose CSPH — no endoscopy needed; treat with carvedilol to reduce the risk of decompensation.", "p. 285", "pp. 48, 60", ["C-11", "C-12", "D-06"])
t = tp(c, "Cholestatic and metabolic cirrhosis", "pp. 287–300")
it(t, "management", "PBC: supplement fat-soluble vitamins and calcium. Biopsy shows loss of small bile ducts with <b>ductular proliferation</b>.", "pp. 287–288", "p. 51", ["C-17", "C-18"])
it(t, "fact", "Haemochromatosis: bronze skin is due to <b>melanin</b> deposition; about 30% may develop HCC as a complication of cirrhosis.", "p. 292", "p. 53", ["C-21", "C-23"])
it(t, "distinction", "MRI showing iron in the <b>pancreas</b> distinguishes hereditary haemochromatosis from secondary iron overload (haemosiderosis), where only the liver is affected.", "p. 293", "p. 53", ["C-22"])
it(t, "fact", "Wilson disease: ceruloplasmin is an α2-globulin carrying six copper atoms (loaded by ATP7B); 50–75% of intestinal copper is absorbed; normal serum ceruloplasmin is 20–35 mg/dL. Haemolysis is due to the toxic effect of copper on red cells; psychiatric disease can extend to psychosis (schizophrenia-like or manic-depressive).", "pp. 294–296", "pp. 12–13", ["A-36", "A-37", "A-39", "A-42", "A-43"])
it(t, "investigation", "Kayser-Fleischer rings are gold or greenish-gold rings at the corneoscleral junction; in a few people they are the <b>first sign</b> of Wilson disease.", "p. 295", "p. 13", ["A-41"])
it(t, "investigation", "α1-antitrypsin deficiency: gene analysis identifies M, Z and S phenotypes.", "p. 300", "p. 56", ["C-28"])

# ---------------- 23
c = ch("23", "Portal Hypertension", "308–317", "Internal Medicine · Surgery")
t = tp(c, "Causes the book does not list", "pp. 309–310")
it(t, "fact", "Additional causes by site:", "pp. 309–310", "p. 57 (figure)", ["D-01", "D-02", "D-03", "D-04"],
   table={"head": ["Site", "Additional causes in the source"], "rows": [
     ["Increased flow", "Idiopathic tropical splenomegaly; arteriovenous fistula"],
     ["Prehepatic", "Splenic-vein thrombosis; invasion or compression of portal/splenic vein by tumour"],
     ["Presinusoidal", "Early PBC; chronic active hepatitis; vinyl chloride, copper; idiopathic portal hypertension"],
     ["Sinusoidal (non-cirrhotic)", "Cytotoxic drugs; vitamin A intoxication"],
     ["Post-sinusoidal", "Alcoholic central hyaline sclerosis"],
     ["Posthepatic", "IVC webs, tumour invasion or thrombosis"]]})
it(t, "mechanism", "Splenomegaly results from congestion <b>and</b> reticulo-endothelial hyperplasia.", "p. 311", "p. 59", ["D-05"])
t = tp(c, "Primary prophylaxis", "p. 313")
it(t, "fact", "Variceal haemorrhage accounts for about <b>one-third</b> of deaths in cirrhosis with portal hypertension.", "p. 313", "p. 60", ["D-07"])
it(t, "mechanism", "Non-selective β-blockers reduce portal inflow by lowering cardiac output (β1) and blocking β2 vasodilator receptors on splanchnic arteries; they are <b>as effective as banding</b>. Propranolol alternative: 80–160 mg/day, titrated to cut resting pulse by 25%, for life.", "p. 313", "p. 61", ["D-08", "D-09", "D-10"])
t = tp(c, "Acute variceal bleeding", "pp. 314–317")
it(t, "management", "Resuscitate to a systolic BP of about 100 mmHg. Terlipressin: 2 mg IV every 6 h, then 1 mg every 4 h, for 2–5 days.", "p. 315", "pp. 61–62", ["D-11", "D-13"])
it(t, "management", "Histoacryl (tissue adhesive) is used for gastric varices <b>and big oesophageal varices</b>. Balloon tamponade still has a place when endoscopic or vasoconstrictor therapy has failed or is unavailable.", "pp. 315–316", "p. 62", ["D-12", "D-15"])
it(t, "management", "TIPS is indicated when bleeding cannot be stopped or rebleeding occurs <b>within 5 days</b> of endoscopic therapy. Surgical shunts are usually end-to-side portocaval or Warren (splenorenal).", "pp. 316–317", "pp. 62–63", ["D-16", "D-17"])

# ---------------- 27
c = ch("27", "Ascites", "337–344", "Internal Medicine")
t = tp(c, "Causes and mechanism", "pp. 338–339")
it(t, "fact", "After cirrhosis, malignancy is the next commonest cause; cardiac failure and tuberculous peritonitis are less frequent.", "p. 338", "p. 66", ["E-01"])
it(t, "distinction", "Causes grouped by portal hypertension:", "p. 338", "p. 66", ["E-02"],
   table={"head": ["", "Causes"], "rows": [
     ["With PHT — intrahepatic", "Cirrhosis, alcoholic hepatitis, active chronic hepatitis, liver failure, veno-occlusive disease, liver tumour, schistosomiasis, sarcoidosis, Budd-Chiari, focal nodular hyperplasia"],
     ["With PHT — extrahepatic", "Heart failure, pericarditis, portal-vein thrombosis"],
     ["No PHT — peritoneal", "Carcinomatosis, mesothelioma, pseudomyxoma, infection"],
     ["No PHT — hypoalbuminaemia", "Nephrotic syndrome, malnutrition, bowel disease"],
     ["No PHT — mixed", "Myxoedema, pancreatic/biliary ascites, amyloidosis, familial Mediterranean fever, granulomatous disease"]]})
it(t, "mechanism", "Renin (juxtaglomerular cells) converts liver-made angiotensinogen to angiotensin I; ACE (mainly pulmonary endothelium) forms angiotensin II, a pressor that also releases aldosterone. Release is driven by renal perfusion (JG cells), distal Na/Cl load (macula densa) and sympathetic β-receptors. The same RAAS activation causes <b>renal sodium avidity (ascites)</b> and <b>renal vasoconstriction (HRS)</b>.", "p. 339", "pp. 67–68", ["E-04", "E-05"])
t = tp(c, "Investigations", "p. 340")
it(t, "investigation", "Ultrasound detects as little as 30 mL (right lateral decubitus). Diagnostic paracentesis is indicated for new-onset ascites or suspected complication (sterile, 20–23-gauge angiocatheter).", "p. 340", "p. 70", ["E-08", "E-09"])
it(t, "investigation", "Extra fluid tests: Gram stain, triglycerides (chylous), bilirubin (bowel perforation), glucose, amylase, LDH, cytology. Pair ascitic with same-day serum albumin for SAAG.", "p. 340", "p. 70", ["E-10"])
it(t, "investigation", "SAAG correlates directly with portal pressure; ≥1.1 g/dL (11 g/L) vs &lt;1.1 separates portal-hypertensive ascites with &gt;97% accuracy. Extra high-gradient causes: fatty liver of pregnancy, massive metastases, mixed ascites, myxoedema, portal-vein thrombosis, sinusoidal obstruction syndrome. Extra low-gradient causes: bowel obstruction/infarction, postoperative lymphatic leak, serositis in connective-tissue disease.", "p. 340", "p. 71 (text + table)", ["E-11", "E-12"])
t = tp(c, "Management", "pp. 341–342")
it(t, "management", "Stepwise regimen: bed rest, 70–90 mmol sodium diet, daily weight; spironolactone 100–200 mg daily; after 4 days consider furosemide 40 mg daily. <b>Stop diuretics</b> if pre-coma (flap), hypokalaemia, azotaemia or alkalosis.", "p. 341", "p. 72 (box)", ["E-14"])
it(t, "distinction", "Refractory ascites (10–20% of patients) = diuretic-<b>resistant</b> (no response to maximal doses) or diuretic-<b>intractable</b> (complications prevent an effective dose). Look for contributors: worsening liver disease, portal/hepatic-vein thrombosis, GI bleeding, infection/SBP, malnutrition, HCC, cardiac or renal disease, hepatotoxic or nephrotoxic substances.", "p. 342", "p. 74", ["E-16", "E-17"])
it(t, "management", "Large-volume paracentesis: 4–6 L daily until the abdomen is emptied, repeat every 2–4 weeks; continue diuretics and sodium restriction afterwards. TIPS lowers diuretic needs, renin and aldosterone but may precipitate encephalopathy or liver failure. Peritoneovenous shunting is another option.", "p. 342", "p. 74", ["E-18", "E-19", "E-20"])
t = tp(c, "Spontaneous bacterial peritonitis", "pp. 343–344")
it(t, "fact", "SBP develops in about 8% of cirrhotics with ascites, especially when severely decompensated; 90% monomicrobial. More than one organism suggests paracentesis-related infection; anaerobes are rare. Variceal bleeding and previous SBP carry particular risk.", "p. 343", "pp. 75–76", ["E-21", "E-22", "E-24"])
it(t, "mechanism", "Gut bacteria translocate (overgrowth, dysmotility) to mesenteric nodes or bypass liver RES via portosystemic shunts → bacteraemia → <b>bacterascites</b>, which resolves if ascitic opsonic activity is good and becomes SBP if it is poor.", "p. 343", "p. 76 (figure)", ["E-23"])
it(t, "caution", "Classic features (fever, pain, leucocytosis) may be absent — tap any cirrhotic who deteriorates, e.g. with encephalopathy.", "p. 343", "p. 76", ["E-24"])
it(t, "management", "Treat ≥5 days; amoxicillin-clavulanate is as effective as third-generation cephalosporins. After upper GI haemorrhage (or sclerotherapy) give norfloxacin 400 mg 12-hourly for <b>at least 7 days</b>.", "pp. 343–344", "pp. 76–77", ["E-25", "E-26"])

# ---------------- 28
c = ch("28", "Renal Impairment in Cirrhosis", "345–348", "Internal Medicine")
t = tp(c, "Hepatorenal syndrome", "pp. 346–347")
it(t, "mechanism", "HRS is progressive; the kidneys are histologically normal and <b>capable of normal function</b> — the defect is renal blood flow. Three components: splanchnic/systemic vasodilatation, renal vasoconstriction and <b>cardiac dysfunction</b>, with raised sympathetic tone; most patients have tense ascites.", "p. 346", "p. 78 (text + figure)", ["E-28", "E-29"])
it(t, "investigation", "Classic criteria used serum creatinine ≥1.5 mg/dL (133 µmol/L) persisting 48 h after diuretic withdrawal and albumin expansion. Exclude toxins (paracetamol, NSAIDs, carbon tetrachloride), infection, ATN (hypotension, aminoglycosides, contrast) and obstructive uropathy.", "pp. 346–347", "p. 79", ["E-32", "E-33"])
it(t, "management", "Prevent HRS: avoid volume depletion (diuretics, lactulose, GI bleeding, LVP without albumin); use ACEI/ARB/NSAIDs/antibiotics judiciously; treat infection early and give SBP prophylaxis; pentoxifylline in severe alcoholic hepatitis; prevent variceal bleeding.", "p. 347", "p. 80 (table)", ["E-35"])
it(t, "management", "Albumin loading 1 g/kg/day (max 100 g) to a CVP of 10–15 cmH₂O. Alternatives to terlipressin: midodrine 2.5–5 mg tds (to 15 mg tds) + octreotide 100 µg SC tds (to 200 µg), or noradrenaline 0.1–0.7 µg/kg/min, titrated to MAP. Vasopressors generally for up to 2 weeks; evaluate for transplantation.", "p. 347", "p. 80 (table)", ["E-36"])

# ---------------- 29
c = ch("29", "Jaundice", "349–354", "Internal Medicine")
t = tp(c, "Approach", "pp. 351–354")
it(t, "investigation", "Isolated indirect hyperbilirubinaemia: first exclude recent trauma, haematoma or transfusion; then LDH, haptoglobin and reticulocyte count — abnormal → haemolysis/dyserythropoiesis; normal → Gilbert or Crigler-Najjar I/II.", "p. 354", "p. 10 (algorithm)", ["A-27"])
it(t, "fact", "Halothane (like paracetamol) causes toxic hepatitis with mixed (hepatic) hyperbilirubinaemia.", "p. 351", "p. 9", ["A-25"])
it(t, "distinction", "Biliary obstruction vs liver disease:", "pp. 353–354", "p. 87 (table)", ["F-06"],
   table={"head": ["", "Favours biliary obstruction", "Favours liver disease"], "rows": [
     ["History", "Abdominal pain, fever/rigors, prior biliary surgery, older age", "Viral prodrome, known viral exposure, blood products or IV drug use, hepatotoxin, family history"],
     ["Examination", "Fever, tenderness, palpable mass, surgical scar", "Spider telangiectasias, stigmata of portal hypertension, asterixis"],
     ["Laboratory", "ALP ↑ out of proportion; PT normal or corrects with vitamin K; leucocytosis; amylase/lipase ↑", "Aminotransferases ↑ out of proportion; PT does not correct with vitamin K; thrombocytopenia; positive serology"]]})
it(t, "fact", "Intrahepatic cholestasis by level: hepatocyte (viral, drug, alcoholic hepatitis; post-necrotic cirrhosis; endotoxin); canaliculus (benign recurrent cholestasis; hormones, pregnancy, drugs); ductules (PBC, allograft rejection, <b>graft-versus-host</b>, biliary atresia, idiopathic adult ductopenia); larger ducts (primary/secondary sclerosing cholangitis).", "p. 352", "p. 85 (figure)", ["F-10"])

# ---------------- 30
c = ch("30", "Hepatic Encephalopathy", "355–360", "Internal Medicine")
t = tp(c, "Pathogenesis", "p. 358")
it(t, "mechanism", "About half of gut ammonia is made by bacteria, the rest from dietary protein and glutamine; it is cleared as urea and glutamine. Blood ammonia is raised in <b>90%</b> of HE; ammonia damages the blood–brain barrier and astrocytes and shifts neural activity toward inhibition. Reduced muscle metabolism also raises it.", "p. 358", "p. 90 (text + figure)", ["F-12", "F-15"])
it(t, "mechanism", "Aromatic amino acids rise (failed hepatic deamination) while branched-chain amino acids fall (muscle/renal uptake driven by <b>hyperinsulinaemia</b>); more aromatic amino acids enter the brain, phenylalanine inhibits dopa synthesis → false neurotransmitters.", "pp. 358, 360", "p. 90", ["F-13"])
it(t, "mechanism", "GABA is made by gut bacteria and normally cleared by the liver; in liver failure or shunting it reaches the systemic circulation.", "p. 358", "p. 90", ["F-14"])
t = tp(c, "Treatment framework", "p. 359")
it(t, "management", "Three strategies: treat the <b>precipitating cause</b>; reduce production and absorption of gut-derived ammonia and toxins; modify neurotransmitter balance.", "p. 359", "p. 91", ["F-16"])

# ---------------- 31
c = ch("31", "Acute Hepatic Failure", "361–366", "Internal Medicine · Emergency / Acute Care")
t = tp(c, "Cerebral oedema", "p. 363")
it(t, "mechanism", "Cerebral blood flow is generally increased: persistent vasodilatation and loss of autoregulation cause hyperaemia, and the rise in cerebral blood volume can worsen brain oedema.", "p. 363", "p. 94", ["F-18"])

content = {
  "cover_lede": "Only what the Hepatology source adds to your book: missing mechanisms, investigation details, distinctions and management points, keyed to the book page they extend. Nothing here repeats the book.",
  "how_to_use": "<p>Read this alongside the book. Each point sits under the book chapter and topic it extends; <b>Book p.</b> is the printed page it adds to and <b>Src p.</b> is the page in the Hepatology source. Chapters with nothing new (24–26, 32–40) are omitted.</p><p>Where the source and the book disagree, the point is not printed here; it is flagged for review in the comparison ledger.</p>",
  "chapters": C, "appendices": []}
pathlib.Path(__file__).with_name("content.json").write_text(json.dumps(content, ensure_ascii=False, indent=1))
print(sum(len(t["items"]) for c in C for t in c["topics"]), "items in", len(C), "chapters")
