"""Saved-file checks: contents links land on their chapter, folios match page labels,
bookmarks land, fonts are embedded outlines (no Type3), text stays inside the page."""
import json, pathlib, pymupdf
R = pathlib.Path(__file__).resolve().parent.parent
d = pymupdf.open(R / "output/YMnotes Digestive System - After Mid-Module Hepatology Extras.pdf")
content = json.loads((R / "src/content.json").read_text()); ok = True
links = sorted((l for l in d[1].get_links() if l["kind"] == pymupdf.LINK_GOTO), key=lambda l: l["from"].y0)
print("contents GOTO links:", len(links), "chapters:", len(content["chapters"])); ok &= len(links) == len(content["chapters"])
for l, c in zip(links, content["chapters"]):
    tgt = l["page"]; row = d[1].get_textbox(l["from"]).replace("\n", " | ")
    good = f"CHAPTER{c['no']}" in d[tgt].get_text().replace(" ", "") and c["title"] in d[tgt].get_text() \
        and c["subjects"] in row and row.strip().endswith(d[tgt].get_label())
    ok &= good; print("PASS" if good else "FAIL", c["no"], "-> page label", d[tgt].get_label())
for lvl, t, p in d.get_toc():
    if t.startswith("Chapter"):
        good = f"CHAPTER{t.split()[1]}" in d[p - 1].get_text().replace(" ", ""); ok &= good
print("bookmarks:", len(d.get_toc()))
types = {fo[2] for p in d for fo in p.get_fonts()}; print("font types:", types); ok &= "Type3" not in types
for i, p in enumerate(d):
    if i in (0, d.page_count - 1): continue
    for b in p.get_text("blocks"):
        r = pymupdf.Rect(b[:4])
        if r.x0 < 14 or r.x1 > p.rect.width - 14 or r.y1 > p.rect.height - 10: ok = False; print("OUT OF BOUNDS", i + 1, r)
print("pages", d.page_count, "labels", [d[i].get_label() for i in range(d.page_count)])
print("OVERALL", "PASS" if ok else "FAIL")
