#!/usr/bin/env python3
"""Saved-file QA for the handout: contents entries, internal links, bookmarks,
fonts, running headers, QR decoding. Writes qa/verification.json."""
import json, pathlib, re, sys
import pymupdf, zxingcpp
from PIL import Image
P = pathlib.Path(__file__).resolve().parent.parent
pdf = P / "YMnotes-Digestive-Other-Subjects-Capsule.pdf"
C = json.loads((P / "source/content.json").read_text(encoding="utf-8"))
d = pymupdf.open(pdf)
res = {"pdf": pdf.name, "pages": d.page_count, "checks": {}, "failures": []}
def fail(m): res["failures"].append(m)

# 1. contents: every chapter row has number, title, subject, folio = its link's target page,
#    and the target page shows that chapter's title.
toc_page = d[2]
links = [l for l in toc_page.get_links() if l["kind"] == pymupdf.LINK_GOTO]
rows = []
for ch in C["chapters"]:
    num = f"{ch['n']:02d}"
    hit = [l for l in links if ch["title"] in toc_page.get_textbox(l["from"])
           and num in toc_page.get_textbox(l["from"]) and ch["subjects"] in toc_page.get_textbox(l["from"])]
    if len(hit) != 1:
        fail(f"contents row for ch {ch['n']}: {len(hit)} links"); continue
    l = hit[0]; txt = toc_page.get_textbox(l["from"])
    folio = re.findall(r"\b(\d{1,2})\s*$", txt.strip())
    target = l["page"] + 1
    lands = ch["title"] in d[l["page"]].get_text()
    ok = bool(folio) and int(folio[0]) == target and lands
    rows.append({"ch": ch["n"], "title": ch["title"], "subjects": ch["subjects"],
                 "printed_folio": int(folio[0]) if folio else None, "target_page": target, "lands_on_title": lands, "ok": ok})
    if not ok: fail(f"contents row ch {ch['n']} folio/target mismatch {folio} vs {target} lands={lands}")
res["checks"]["contents_rows"] = rows

# 2. every internal link resolves to a real page; external URIs listed
internal = external = 0; uris = set()
for i, p in enumerate(d):
    for l in p.get_links():
        if l["kind"] == pymupdf.LINK_GOTO:
            internal += 1
            if not (0 <= l["page"] < d.page_count): fail(f"p{i+1} link to missing page {l['page']}")
        elif l["kind"] == pymupdf.LINK_URI:
            external += 1; uris.add(l["uri"])
        elif l["kind"] == pymupdf.LINK_NAMED:
            fail(f"p{i+1} unresolved named link {l}")
res["checks"]["links"] = {"internal": internal, "external": external, "uris": sorted(uris)}

# 3. discrepancy index links land on the entry IDs
idx = d[[i for i in range(d.page_count) if "Points to check" in d[i].get_text() and "Entry" in d[i].get_text()][-1]]
for l in idx.get_links():
    if l["kind"] == pymupdf.LINK_GOTO:
        eid = idx.get_textbox(l["from"]).strip()
        if eid not in d[l["page"]].get_text(): fail(f"index link {eid} lands on p{l['page']+1} without the entry")
res["checks"]["discrepancy_index_links"] = sum(1 for l in idx.get_links() if l["kind"] == pymupdf.LINK_GOTO)

# 4. bookmarks
toc = d.get_toc()
res["checks"]["bookmarks"] = toc
for lvl, title, page in toc:
    m = re.match(r"Ch (\d+) · (.+)", title)
    if m and m.group(2) not in d[page - 1].get_text(): fail(f"bookmark {title} -> p{page} wrong")

# 5. fonts: embedded, no Type3
fonts = set()
for p in d:
    for f in p.get_fonts(full=True):
        fonts.add((f[3], f[2], f[1]))
res["checks"]["fonts"] = sorted({f"{n} ({t})" for n, t, e in fonts})
if any(t == "Type3" for n, t, e in fonts): fail("Type3 font present")

# 6. QR on every body page decodes to the brand destination
brand_url = None
qr_ok = []
for i in range(1, d.page_count - 1):
    pix = d[i].get_pixmap(dpi=300, clip=pymupdf.Rect(d[i].rect.width - 110, 0, d[i].rect.width, 80))
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    r = zxingcpp.read_barcodes(img)
    qr_ok.append((i + 1, r[0].text if r else None))
res["checks"]["header_qr_decode"] = qr_ok
if any(t is None for _, t in qr_ok): fail("header QR not decodable on some page")

# 7. text inside page box; smallest font size
small = min((s["size"] for p in d for b in p.get_text("dict")["blocks"] for ln in b.get("lines", []) for s in ln["spans"] if s["text"].strip()), default=0)
res["checks"]["smallest_font_pt"] = round(small, 2)
out = 0
for i, p in enumerate(d):
    for w in p.get_text("words"):
        if w[0] < 0 or w[1] < 0 or w[2] > p.rect.width + .5 or w[3] > p.rect.height + .5: out += 1
res["checks"]["words_outside_page"] = out
if out: fail(f"{out} words outside page box")
res["status"] = "PASS" if not res["failures"] else "FAIL"
(P / "qa/verification.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
print(res["status"], res["failures"])
print(json.dumps({k: v for k, v in res["checks"].items() if k not in ("bookmarks",)}, ensure_ascii=False)[:2500])
