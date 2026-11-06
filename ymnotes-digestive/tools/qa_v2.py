import sys, collections, pymupdf
sys.path.insert(0, "src")
import model, build_v2 as B
groups = model.load(); items = {it["id"]: it for g in groups for it in g["items"]}
d = pymupdf.open(B.OUT)
bs = 135
print("pages", len(d), "toc", len(d.get_toc()))
kinds = collections.Counter(); to_book = []; internal = []
for p in range(bs):
    for lk in d[p].get_links():
        kinds[lk["kind"]] += 1
        if lk["kind"] == pymupdf.LINK_GOTO:
            (to_book if lk["page"] >= bs else internal).append((p, lk))
print("answer-page link kinds:", dict(kinds), "| to book:", len(to_book), "| internal:", len(internal))
# 1. internal links: target page + y inside the page and near a card/group top (text there)
bad = 0
for p, lk in internal:
    H = d[lk["page"]].rect.height
    if not (0 <= lk["to"].y <= H): bad += 1
print("internal links with out-of-page y:", bad)
# 2. every question's answer-row link: find by rect containing 'Book p.' chip text... use expected multiset
exp = collections.Counter(bs + B.INV[it["pg"]] - 1 for it in items.values() if it["pg"])
got = collections.Counter(lk["page"] for p, lk in to_book if lk["from"].width > 60 and p != 0)
print("answer->book targets match expectations:", exp == got, "(", sum(got.values()), "links )")
# 3. cover button
cov = [lk for lk in d[0].get_links() if lk["kind"] == pymupdf.LINK_GOTO and lk["page"] == bs]
print("cover 'Open the book' links:", len(cov))
# 4. back-links on book pages: should land on a page < bs, y within page, and the text at/under the target contains the group chip
ok = 0; bad = []
for p in range(bs, len(d)):
    for lk in d[p].get_links():
        if lk["kind"] == pymupdf.LINK_GOTO and lk["page"] < bs:
            tp = lk["page"]; y = lk["to"].y
            # text slice right below the landing point
            r = pymupdf.Rect(0, y, 595, min(y + 40, d[tp].rect.height))
            t = d[tp].get_text("text", clip=r)
            lab = d[p].get_text("text", clip=lk["from"]).strip()   # e.g. 'A·1'
            if lab and lab.replace("\n", "") in t.replace("\n", ""): ok += 1
            else: bad.append((p, lab, tp, round(y)))
print("back-links verified (card with that A·1 tag is right below the landing point):", ok, "| mismatches:", len(bad), bad[:6])
# 5. forward links: landing area on the book page contains the highlighted anchor?
miss = []; n = 0
for p, lk in to_book:
    if lk["from"].width <= 60 or p == 0: continue
    tp = lk["page"]; y = lk["to"].y
    r = pymupdf.Rect(0, y, 595, min(y + 300, d[tp].rect.height))
    hl = [a for a in d[tp].annots(types=[pymupdf.PDF_ANNOT_HIGHLIGHT]) if a.rect.intersects(r)]
    n += 1
    if not hl: miss.append((p, tp - bs, round(y)))
print("forward links checked:", n, "| landing window without a highlight (nearest-page items expected):", len(miss))
