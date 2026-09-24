"""Merge the per-range comparison rows with the central review into ledger.json/.csv/.md."""
import csv, json, pathlib
H = pathlib.Path(__file__).resolve().parent
content = json.loads((H.parent / "src/content.json").read_text())
used = {}
for c in content["chapters"]:
    for t in c["topics"]:
        for it in t["items"]:
            for lid in it["ledger"]:
                used.setdefault(lid, f'Ch {c["no"]} · {t["title"]}')
CENTRAL = {  # id: (final decision, central-review reason)
 "B2-25": ("exclude", "Central review: doses of older DAA combinations the book says are largely replaced; low value."),
 "B2-29": ("exclude", "Central review: programme history (2007 committee, NNTC); not student-useful."),
 "B2-31": ("exclude", "Central review: campaign detail (NCD screening); not student-useful."),
 "B2-32": ("exclude", "Central review: superseded Egyptian national regimen (sofosbuvir+daclatasvir); book states regimens replaced."),
 "B1-05": ("exclude", "Central review: low yield (vaccine-derived IgG immunity implied by book p259)."),
 "D-06": ("merged", "Duplicate of C-12 (same >25 kPa CSPH statement, HAP 60 vs 48); printed once under Ch 22."),
 "D-14": ("exclude", "Central review: NPO already in first-half book Ch 03 upper GI bleeding (printed p50)."),
 "D-23": ("exclude", "Central review: source gives only the heading 'changes in nitrogen metabolism' with no content."),
 "F-15": ("merged", "Merged with F-12 (same ammonia mechanism)."),
 "E-36": ("include (partial)", "Terlipressin escalation and albumin 20–60 g/day maintenance omitted because of unresolved discrepancy E-37."),
}
rows = []
for f in sorted((H / "agent-parts").glob("*.json")):
    for r in json.loads(f.read_text()):
        final, why = r["decision"], ""
        if r["id"] in CENTRAL: final, why = CENTRAL[r["id"]]
        elif r["decision"] == "include" and r["id"] not in used: final, why = "exclude", "Central review: not carried into handout."
        rows.append({"id": r["id"], "source_pages_hapatology": ", ".join(map(str, r["hap_pages"])),
            "source_excerpt": r["source_excerpt"], "topic": r.get("topic", ""), "book_chapter": r["book_chapter"],
            "book_printed_pages": ", ".join(map(str, r["book_pages"])), "book_has": r["book_has"],
            "new_contribution": r["new_contribution"], "evidence_type": r.get("evidence_type", ""),
            "agent_decision": r["decision"], "final_decision": final,
            "reason": (r.get("reason", "") + (" | " + why if why else "")).strip(" |"),
            "handout_location": used.get(r["id"], "")})
missing = set(used) - {r["id"] for r in rows}
assert not missing, missing
(H / "comparison-ledger.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
with open(H / "comparison-ledger.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def cell(s): return str(s).replace("|", "\\|").replace("\n", " ")
md = ["# Comparison ledger — Hepatology source vs YMnotes Digestive System (after mid-module)", "",
      "Source: `Hepatology .pdf` (96 pp.; HAP page = PDF page = printed page). Book: printed folios from "
      "`4_5875397832227168769(1).PDF` (printed 197–433) and `4_5875397832227168769.PDF` (printed 1–197).", ""]
from collections import Counter
cnt = Counter(r["final_decision"] for r in rows)
md.append("Totals: " + ", ".join(f"{k}: {v}" for k, v in sorted(cnt.items())) + f" (rows: {len(rows)})\n")
for dec in ["include", "include (partial)", "discrepancy", "merged", "exclude"]:
    sel = [r for r in rows if r["final_decision"] == dec]
    if not sel: continue
    md += [f"## {dec.title()} ({len(sel)})", "", "| ID | Src p. | Book chapter | Book p. | New contribution / finding | Book already has | Reason | Handout |", "|---|---|---|---|---|---|---|---|"]
    md += [f'| {r["id"]} | {r["source_pages_hapatology"]} | {cell(r["book_chapter"])} | {r["book_printed_pages"]} | {cell(r["new_contribution"])} | {cell(r["book_has"])} | {cell(r["reason"])} | {cell(r["handout_location"])} |' for r in sel]
    md.append("")
(H / "comparison-ledger.md").write_text("\n".join(md))
print(cnt, len(rows))
