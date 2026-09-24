#!/usr/bin/env python3
"""Merge the four comparison ledgers, apply the central review, and export
ledger/comparison-ledger.{json,csv,md}. The handout entry IDs come from
source/content.json so the ledger and the PDF cannot drift apart."""
import csv, glob, json, pathlib, re
import pymupdf
L = pathlib.Path(__file__).resolve().parent
P = L.parent
rows = []
for f in sorted(glob.glob(str(L / "agent-ledgers/ledger_*.json"))):
    rows += json.load(open(f, encoding="utf-8"))
by = {r["id"]: r for r in rows}

CENTRAL = {
 "TU-34": dict(decision="exclude", reason="Central review: Figure 15.2 on book p.197 already gives the per-segment distribution (rectum 27%, sigmoid 20%, caecum 14%, ascending colon 8% ...). The GIT Others values group segments differently and teach nothing new.",
               book_evidence="Figure 15.2 'Distribution of colorectal cancer' (figure labels, checked on the rendered page): rectum 27%, sigmoid colon 20%, caecum 14%, ascending colon 8%, rectosigmoid junction 7%, transverse 5%, hepatic flexure 3%, descending 3%, splenic flexure 2%, anus 2%, appendix 1%."),
 "TU-23": dict(new_contribution="Colonic adenomas show a well-defined familial predisposition (and predispose to colorectal carcinoma).",
               reason="Central review: include the familial predisposition only. The GIT Others 'Age > 60' is left out because the book already gives adenoma prevalence (20-30% over age 50), and adding it would confuse rather than add."),
 "FI-23": dict(new_contribution="Campylobacter: a rectal swab is an acceptable specimen; darting motility is seen in wet mount under dark-field illumination; isolated colonies are identified by biotyping, serotyping and phage typing.",
               reason="Central review: the Gram-smear 'curved/S-shaped bacilli' point was dropped because book p.110 morphology already states it."),
 "TU-31": dict(book_chapter=15, book_chapter_title="Colorectal Cancer", book_printed_page=196, book_pdf_file="first-half", book_pdf_page=199,
               reason="Central review: placed in Ch 15 (the colorectal teaching chapter, which has an 'Age' heading on p.196). Also cites Ch 4 p.74 (60-79). GIT Others p.19 (50-70) contradicts its own p.20 (60-79)."),
 "TU-25": dict(book_printed_page=73, book_pdf_file="first-half", book_pdf_page=76),
}
for k, v in CENTRAL.items():
    by[k].update(v); by[k]["central_review"] = "changed"

# handout entry map from content.json
C = json.loads((P / "source/content.json").read_text(encoding="utf-8"))
entry = {}
for part, sec in (("part_a", "A · after mid-module"), ("part_b", "B · earlier-chapter additions")):
    for ch in C[part]["chapters"]:
        for it in ch["items"]:
            for lid in it["ledger"]:
                entry[lid] = (it["id"], sec)
for r in rows:
    r.setdefault("central_review", "confirmed")
    e = entry.get(r["id"])
    r["handout_entry"] = e[0] if e else ""
    r["handout_section"] = e[1] if e else ""
    if r["decision"] != "exclude" and not e:
        raise SystemExit(f"{r['id']} is {r['decision']} but not in the handout")
    if r["decision"] == "exclude" and e:
        raise SystemExit(f"{r['id']} excluded but in handout")

# quote verification against the GIT Others page
O = pymupdf.open(P.parent / "GIT others.pdf")
norm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())
for r in rows:
    t = norm(O[r["others_page"] - 1].get_text())
    pieces = [p for p in re.split(r"\.\.\.|…|\[.*?\]", r["others_quote"]) if len(norm(p)) > 12]
    r["others_quote_check"] = "verbatim on page" if pieces and all(norm(p)[:40] in t for p in pieces) else "summary (not verbatim)"
    r["others_printed_page"] = r["others_page"]   # GIT Others: printed page = PDF page

cols = ["id", "decision", "handout_entry", "handout_section", "others_page", "others_quote", "others_quote_check",
        "topic", "book_chapter", "book_chapter_title", "book_printed_page", "book_pdf_file", "book_pdf_page",
        "fits_after", "book_evidence", "new_contribution", "reason", "central_review"]
order = {"PH": 0, "TU": 1, "FI": 2, "PA": 3}
rows.sort(key=lambda r: (order[r["id"][:2]], int(r["id"][3:])))
(L / "comparison-ledger.json").write_text(json.dumps([{c: r.get(c) for c in cols} for r in rows], indent=1, ensure_ascii=False), encoding="utf-8")
with open(L / "comparison-ledger.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

n = lambda d: sum(1 for r in rows if r["decision"] == d)
md = ["# Comparison ledger: GIT Others vs YMnotes Digestive System (Version 3)", "",
      "**Page conventions.** *Book p.* = printed folio. *PDF* = viewer page index in the named file: first half `4_5875397832227168769.PDF` (printed = PDF − 3, pp. 1–197); second half `4_5875397832227168769(1).PDF` (printed = PDF + 196, pp. 197–433). *GIT Others p.* = its PDF page, which is also its printed number.", "",
      f"**Totals:** {len(rows)} candidates · {n('include')} include · {n('discrepancy')} discrepancy · {n('exclude')} exclude. The standard is in `INCLUSION-STANDARD.md`. `central_review` marks rows changed at the final central review.", "",
      "| ID | Decision | Handout | GIT Others p. | Book ch · printed p. (PDF) | Topic | New contribution / reason |",
      "|---|---|---|---|---|---|---|"]
esc = lambda s: str(s or "").replace("|", "\\|").replace("\n", " ")
for r in rows:
    bp = f"Ch {r['book_chapter']} · p. {r['book_printed_page']} ({r['book_pdf_file']} PDF {r['book_pdf_page']})" if r.get("book_printed_page") else f"Ch {r['book_chapter']}"
    txt = r["new_contribution"] if r["decision"] != "exclude" else r["reason"]
    flag = " ⟲" if r["central_review"] == "changed" else ""
    md.append(f"| {r['id']}{flag} | **{r['decision']}** | {r['handout_entry']} | {r['others_page']} | {esc(bp)} | {esc(r['topic'])} | {esc(txt)} |")
md += ["", "⟲ = changed at central review (see `reason`). The full book evidence and source quotes are in the CSV and JSON."]
(L / "comparison-ledger.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(len(rows), n("include"), n("discrepancy"), n("exclude"))
