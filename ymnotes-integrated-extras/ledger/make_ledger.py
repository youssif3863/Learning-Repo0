#!/usr/bin/env python3
"""Merged traceability ledger for the integrated PDF.

Inputs:  build/out/content.json (written by build/build.py from source/*.md)
         inputs/*-comparison-ledger.json, inputs/im-handout.md, inputs/os-content.json
Outputs: ledger/integrated-ledger.json, .csv (one row per ORIGINAL ledger row, all
         three handouts) and ledger/integrated-ledger.md (readable: entries, review
         points, integration edits and exclusions).

Every original row gets exactly one integrated disposition:
  retained  -> the integrated entry ID (E..) that carries it
  review    -> the review point (R..) that carries it
  excluded  -> by the original handout (its own reason), or by this integration (reason given)
  note      -> chapter-level "no additions" rows of the original handout
The script fails if an originally included row is not accounted for.

    python3 ledger/make_ledger.py
"""
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
IN = ROOT / "inputs"
OUT = ROOT / "ledger"

# Editorial actions taken during integration, per integrated entry / review point.
EDITS = {
    "E01.04": "Merged IM C1-12 (addition: porphyria) with IM pearl C1-13/14/15: same book page and section (abdominal pain).",
    "E03.03": "IM C3-11's treatment bullet moved into E03.07 (overlap with C3-23; audit B W1).",
    "E03.06": "Trimmed the sentence on NSAID burden in the elderly: already on book p. 36 (audit B §5.1).",
    "E03.07": "Merged IM C3-11 treatment bullet with IM C3-23 (both: drug options for acute/erosive gastritis; audit B M2).",
    "E03.12": "Hb < 10 'mg/dl' transfusion threshold moved to review point R05 (conflicts with book pp. 51, 315). "
              "Sentence 'Hb falls late…' trimmed (book p. 51 has it). NG-tube bullet kept as GIT Internal Med's practice for "
              "non-variceal bleeding with cross-reference to R33. Antiplatelet bullet moved to E03.16.",
    "E03.15": "IM GB-22's PCI bullet moved to E03.16.",
    "E03.16": "New merged entry: IM GB-11 antiplatelet bullet + IM GB-22 PCI bullet (audit B M3); 'stopping antiplatelets "
              "carries a high risk' trimmed because book p. 50 already states the thrombosis risk.",
    "E03.17": "IM GB-25 nasogastric lavage attributed to GIT Internal Med with cross-reference to R33.",
    "E04.03": "OS C4-3 kept separate from IM C3-14 (E03.04): partial overlap, distinct facts; both carry a cross-reference.",
    "E04.08": "Table row 'Number (multiple vs solitary)' removed: already on book p. 73 (audit B §5.1).",
    "E05.06": "Pointer to Chapter 7 (Salmonella/Campylobacter laboratory points) added.",
    "E05.07": "Relapse sentence ('five or more relapses') removed: already on book p. 83 (audit B §5.1).",
    "E08.01": "'Rectum always involved in UC' (IM p. 76 table) moved to review point R13: book Fig 8.1 says 'typically involved'.",
    "E08.04": "Note that the steroid rows of the same table are kept for review (R14).",
    "E18.02": "Merged Hepatology points A-04, A-05 and A-06/A-07 (hyperdynamic circulation).",
    "E18.04": "Merged Hepatology A-11, A-03 and A-12/A-30/A-31 so that no clotting-factor list reads as exhaustive (audit B M5).",
    "E18.06": "Merged Hepatology A-14/A-15 with B1-19 (ALP/GGT with space-occupying or infiltrative lesions; audit B M4).",
    "E18.07": "Hepatology F-07 (isolated ALP causes) kept as its own entry.",
    "E18.10": "Merged Hepatology F-03/A-17 with A-18 (bilirubin and bile acids in the gut).",
    "E18.11": "Hepatology A-29 jaundice table reduced to the details the book lacks (most of it is on book pp. 245–246; "
              "audit B §5.1); merged with A-26/A-28 (LDH, β-lipoproteins).",
    "E18.13": "Merged Hepatology B1-08/B1-09 tables, B1-09 comparison and B1-07 window-period point.",
    "E18.17": "Hepatology B1-18 (Hepatitis G, book p. 249) moved from Chapter 19 to Chapter 18, where p. 249 belongs (audit C).",
    "E21.01": "Type frequencies left out (disputed; review point R25).",
    "E22.07": "Merged Hepatology C-21/C-23 with C-22 (haemochromatosis).",
    "E22.08": "Merged Hepatology A-36/37/39/42/43 with A-41 (Wilson disease).",
    "E23.05": "Terlipressin dose labelled as Hepatology-source only (book gives duration, no dose); garbled IHD sentence "
              "pointed to note N4 (audit B S7).",
    "E23.06": "Restored the source's own qualifier 'rarely used now' for balloon tamponade (book p. 316 and Hepatology p. 62; audit B S12).",
    "E23.07": "Added the source's own 'rebleed within 10 days → repeat endoscopy' sentence (also book p. 316) beside the TIPS "
              "5-day window, so the two are read together (audit B S4).",
    "E27.04": "Merged Hepatology E-08/E-09 with E-10 (detecting and tapping ascites).",
    "E27.06": "Diuretic regimen reduced to what the book lacks (sodium intake, 4-day step, stop criteria); book pp. 341–342 "
              "already give bed rest, weight and spironolactone dose (audit B §5.1).",
    "E27.08": "Added the book's albumin statement (8 g per litre removed, p. 342; also Hepatology p. 74) beside the "
              "large-volume paracentesis schedule (audit B S6).",
    "E27.09": "SBP 8% reworded with its exact denominator (spontaneous type, cirrhotics with ascites) and the 10% overall "
              "figure that book p. 343 and Hepatology p. 75 both give; checked: not a disagreement (audit B S3/N1).",
    "E27.11": "Reduced to 'classic features may be absent': the rest is already on book p. 343.",
    "E28.01": "Reduced to what the book lacks (normal renal function, cardiac dysfunction, tense ascites); the rest is on book p. 346.",
    "E28.04": "Note that the terlipressin escalation and maintenance albumin rows are kept for review (R36).",
    "R05": "New review point raised in integration: GIT Internal Med's Hb < 10 threshold vs book pp. 50–51 (and p. 315).",
    "R13": "Extended with the rectum row of the same GIT Internal Med p. 76 table (moved out of E08.01).",
    "R21": "Book page corrected from p. 248 to p. 247 for the 5–10% figure (audit B).",
    "R28": "Third position added: book p. 359 (20 g/day in the acute attack), found by audit B.",
    "R32": "The same Hct ≈ 30 text is in GIT Internal Med p. 43 (verified); both sources cited.",
    "R33": "Extended with GIT Internal Med's nasogastric uses (pp. 40, 46) as context; kept in Chapter 3 with cross-references.",
    "R34": "The same sentence is in GIT Internal Med p. 43 (verified); both sources cited.",
}

# Rows excluded by this integration (not by the original handout).
INTEGRATION_EXCLUDED = {
    ("HEP", "C-28"): "Excluded in integration: largely already in the book (book p. 300 gives phenotyping/genotyping of SERPINA1, PiZZ); "
                     "only the naming of M and S phenotypes was new, judged low value (audit B §5.1).",
}

HANDOUT_NAME = {"IM": "Before Mid-Module Internal Medicine Extras (GIT Internal Med)",
                "OS": "Other Subjects Capsule (GIT Others)",
                "HEP": "After Mid-Module Hepatology Extras (Hepatology)"}


def main():
    content = json.loads((ROOT / "build/out/content.json").read_text(encoding="utf-8"))
    entries = [(c["n"], t["title"], en) for c in content["chapters"] for t in c["topics"] for en in t["entries"]]
    reviews = content["reviews"]

    # original entry IDs
    im_entry = {}
    for m in re.finditer(r"^::: (\w+) ([A-Z0-9/-]+) \|", (IN / "im-handout.md").read_text(encoding="utf-8"), re.M):
        kind, eid = m.groups()
        parts = eid.split("/")
        pref = parts[0].rsplit("-", 1)[0]
        for x in [parts[0]] + [pref + "-" + p for p in parts[1:]]:
            im_entry[x] = (eid, kind)
    os_entry = {}
    for c in json.loads((IN / "os-content.json").read_text(encoding="utf-8"))["chapters"]:
        for it in c["items"]:
            for x in it["ledger"]:
                os_entry[x] = (it["id"], it["kind"])

    ledgers = {"IM": json.loads((IN / "im-comparison-ledger.json").read_text(encoding="utf-8")),
               "OS": json.loads((IN / "os-comparison-ledger.json").read_text(encoding="utf-8")),
               "HEP": json.loads((IN / "hep-comparison-ledger.json").read_text(encoding="utf-8"))}

    # where each original row went
    where = {}
    for ch, topic, en in entries:
        for f in en["from"]:
            h, rid = f.split(":", 1)
            h = "OS" if h in ("PHARM", "PATH", "MICRO", "PARA") else h
            where.setdefault((h, rid), []).append(en["id"])
    for r in reviews:
        for rid in re.findall(r"\b([A-Z]{1,2}\d?-[A-Z]?\d+)\b", r["from"]):
            h = "HEP" if "Hepatology" in r["from"] and re.match(r"^(A|B1|B2|C|D|E|F)-\d+$", rid) else None
            if "GIT Internal Med companion" in r["from"] and re.match(r"^(C\d|GB)-", rid):
                h = h or "IM"
            if "GIT Others" in r["from"] and re.match(r"^(PH|TU|FI|PA)-", rid):
                h = "OS"
            if h:
                where.setdefault((h, rid), []).append(r["id"])
    # IM discrepancy entries are cited by entry ID (e.g. C3-13) in review "from"
    for r in reviews:
        for m in re.finditer(r"companion (C\d-\d+|C\d+-\d+)", r["from"]):
            where.setdefault(("IM", m.group(1)), []).append(r["id"])
        for m in re.finditer(r"capsule (C\d+-D\d)", r["from"]):
            for x, (eid, _) in os_entry.items():
                if eid == m.group(1):
                    where.setdefault(("OS", x), []).append(r["id"])

    rows, problems = [], []
    for h, L in ledgers.items():
        for r in L:
            rid = r["id"]
            if h == "IM":
                dec, reason = r["final_decision"], r.get("reason", "")
                orig_entry = im_entry.get(rid, ("", ""))[0]
                ch = r.get("chapter")
                topic = r.get("topic", "")
                book = r.get("main_pages_printed", "")
                srcp = f'GIT Internal Med p. {r.get("im_pages", "")}'
            elif h == "OS":
                dec, reason = r["decision"], r.get("reason", "")
                orig_entry = os_entry.get(rid, ("", ""))[0]
                ch = r.get("book_chapter")
                topic = r.get("topic", "")
                book = r.get("book_printed_page", "")
                srcp = f'GIT Others p. {r.get("others_page", "")}'
            else:
                dec, reason = r["final_decision"], r.get("reason", "")
                orig_entry = ""
                ch = (r.get("book_chapter") or "").split(" ")[0]
                topic = r.get("topic", "")
                book = r.get("book_printed_pages", "")
                srcp = f'Hepatology p. {r.get("source_pages_hapatology", "")}'
            targets = sorted(set(where.get((h, rid), [])))
            included = dec.startswith("include") or dec == "merged" or dec.startswith("discrepancy")
            if (h, rid) in INTEGRATION_EXCLUDED:
                disp, detail = "excluded in integration", INTEGRATION_EXCLUDED[(h, rid)]
            elif targets:
                kinds = {t[0] for t in targets}
                disp = "retained" if kinds == {"E"} else ("review point" if kinds == {"R"} else "retained + review point")
                detail = "; ".join(f"{t}: {EDITS[t]}" for t in targets if t in EDITS)
            elif dec in ("no additions", "no substantive additions"):
                disp, detail = "chapter note (original)", "Chapter-level 'no additions' row of the original handout; the integrated chapter entry is rewritten for the merged book."
            elif included:
                disp, detail = "UNACCOUNTED", ""
                problems.append(f"{h} {rid} ({dec}) is included in its original handout but not placed")
            else:
                disp = "excluded by original handout"
                detail = reason
                if h == "IM" and rid == "GB-18":
                    detail += " Its variceal-bleeding text (GIT Internal Med p. 43) is cited in review points R32 and R34."
            rows.append({"handout": h, "handout_name": HANDOUT_NAME[h], "row_id": rid,
                         "original_entry": orig_entry, "original_decision": dec, "chapter": ch,
                         "topic": topic, "book_printed_pages": book, "source_pages": srcp,
                         "integrated_disposition": disp, "integrated_ids": ", ".join(targets),
                         "detail": detail})

    OUT.mkdir(exist_ok=True)
    (OUT / "integrated-ledger.json").write_text(json.dumps({"rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(OUT / "integrated-ledger.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # ---------------------------------------------------------------- markdown
    from collections import Counter
    cnt = Counter((r["handout"], r["integrated_disposition"]) for r in rows)
    md = ["# Integrated traceability ledger",
          "",
          "Generated by `ledger/make_ledger.py` from `build/out/content.json` and the three frozen input ledgers in `inputs/`.",
          "The CSV/JSON copies hold one row per original ledger row (all three handouts) with its integrated disposition.",
          "",
          "## Disposition of every original ledger row",
          "",
          "| Handout | Rows | Retained | Review point | Retained + review | Excluded by original | Excluded in integration | Chapter notes |",
          "|---|---|---|---|---|---|---|---|"]
    for h in ("IM", "OS", "HEP"):
        n = sum(1 for r in rows if r["handout"] == h)
        md.append(f"| {HANDOUT_NAME[h]} | {n} | {cnt[(h, 'retained')]} | {cnt[(h, 'review point')]} | "
                  f"{cnt[(h, 'retained + review point')]} | {cnt[(h, 'excluded by original handout')]} | "
                  f"{cnt[(h, 'excluded in integration')]} | {cnt[(h, 'chapter note (original)')]} |")
    md += ["", f"Unaccounted included rows: **{sum(1 for r in rows if r['integrated_disposition'] == 'UNACCOUNTED')}**.", ""]

    md += ["## Integrated entries", "",
           "| ID | Ch | Topic | Title | Subject | Book | Source | Original handout and rows | Integration edit |",
           "|---|---|---|---|---|---|---|---|---|"]
    for ch, topic, en in entries:
        frm = ", ".join(en["from"])
        md.append(f'| {en["id"]} | {ch} | {topic} | {en["title"]} | {"+".join(en["subjects"])} | {en["book"]} | {en["src"]} | '
                  f'{frm} | {EDITS.get(en["id"], "retained as in the source handout (wording lightly tightened where needed)")} |')
    md += ["", "## Review points", "", "| ID | Ch | Topic | Raised by | Integration edit |", "|---|---|---|---|---|"]
    for r in reviews:
        md.append(f'| {r["id"]} | {r["ch"]} | {r["title"]} | {r["from"]} | {EDITS.get(r["id"], "consolidated as raised")} |')
    md += ["", "## Excluded in integration", ""]
    for (h, rid), why in INTEGRATION_EXCLUDED.items():
        md.append(f"- **{h} {rid}**: {why}")
    md += ["", "## Merged duplicates and overlaps", "",
           "No true duplicate existed between the three handouts: the Other Subjects capsule had already dropped its overlaps "
           "with the Internal Medicine companion (FI-02 poultry → Salmonella; part of TU-12). The merges made here join "
           "points from the same handout that sit on the same book page and topic; see the entries marked 'Merged' above. "
           "Partial cross-handout overlap: IM C3-14 (E03.04) and OS C4-3 (E04.03) are kept as two entries with cross-references.",
           "", "## Wording notes (printed in the review section)", "",
           "N1–N5 are printed at the end of the review section. Not printed (source wording only, not used): GIT Internal Med p. 37 "
           "'right colon (the ligament of Teriz)'; GIT Internal Med p. 18 'mesenteric' for myenteric plexus; book p. 354 'direct > 15%' "
           "vs p. 246 '> 50%' (p. 354 is image-only and could not be verified)."]
    (OUT / "integrated-ledger.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(rows)} original rows; " + ", ".join(f"{k[0]} {k[1]}: {v}" for k, v in sorted(cnt.items())))
    if problems:
        print("\n".join(problems))
        sys.exit(1)


if __name__ == "__main__":
    main()
