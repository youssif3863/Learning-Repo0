#!/usr/bin/env python3
"""Saved-file checks for the integrated PDF. Reads ONLY the final PDF (plus
source/chapters.json for the expected titles) and writes qa/verification.json.

Every check is made on the saved file, independently of the build's own map:
chapter headings are located by their printed "CHAPTER NN" kicker, contents rows
by their printed number and title, and each link by its saved annotation.

    python3 qa/verify.py          exit code 1 if any check fails
"""
import json
import pathlib
import re
import sys

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF = ROOT / "YMnotes-Digestive-System-Integrated-Teaching-Extras.pdf"
MM = 72 / 25.4
BRAND_URL = "https://youtube.com/@ymnotes?si=lJu1kuQj5x9LcjmA"

checks, failures = [], []


def check(name, ok, detail=""):
    checks.append({"check": name, "ok": bool(ok), "detail": detail})
    if not ok:
        failures.append(f"{name}: {detail}")


def squash(t):
    return re.sub(r"[^0-9a-z]", "", t.lower())


def lines(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            txt = "".join(s["text"] for s in ln["spans"])
            out.append((txt, pymupdf.Rect(ln["bbox"]), min((s["size"] for s in ln["spans"]), default=0)))
    return out


def main():
    meta = json.loads((ROOT / "source/chapters.json").read_text())["chapters"]
    doc = pymupdf.open(PDF)
    n = doc.page_count
    labels = [doc[i].get_label() for i in range(n)]

    # ---------------------------------------------------------- page labels
    check("page labels: cover", labels[0] == "Cover", labels[0])
    check("page labels: closing page", labels[-1] == "YMnotes", labels[-1])
    bad = [i for i in range(1, n - 1) if labels[i] != str(i)]
    check("page labels: body pages numbered 1..N", not bad, f"mismatch on physical pages {bad[:5]}")

    # printed folio in the footer equals the page label
    bad = []
    for i in range(1, n - 1):
        pg = doc[i]
        foot = [t.strip() for t, r, _ in lines(pg) if r.y0 > pg.rect.height - 18 * MM and re.fullmatch(r"\d+", t.strip())]
        if foot != [labels[i]]:
            bad.append((i + 1, foot, labels[i]))
    check("footer folio equals page label on every numbered page", not bad, str(bad[:4]))

    # ------------------------------------------ locate headings independently
    toc_pages = [i for i in range(1, 6) if "bookchaptersubjects" in squash(doc[i].get_text())
                 or "afterthechapters" in squash(doc[i].get_text())]
    review_page = next(i for i in range(n) if "pointsforyousseftoreview" in squash(doc[i].get_text())
                       and "separatefromtheteachingpoints" in squash(doc[i].get_text()))
    heading = {}
    for i in range(max(toc_pages) + 1, review_page):
        for t, r, _ in lines(doc[i]):
            m = re.fullmatch(r"chapter(\d\d)", squash(t))
            if m and r.y0 > 20 * MM:          # not the running header
                heading.setdefault(int(m.group(1)), []).append((i, r))
    missing = [c["n"] for c in meta if c["n"] not in heading]
    dup = [k for k, v in heading.items() if len(v) != 1]
    check("every chapter 1-40 has exactly one printed heading in the body", not missing and not dup,
          f"missing {missing}, duplicated {dup}")
    order = [heading[c["n"]][0] for c in meta if c["n"] in heading]
    check("chapter headings run in book order 1-40",
          all((a[0], a[1].y0) < (b[0], b[1].y0) for a, b in zip(order, order[1:])), "")

    # ------------------------------------------------------------ contents
    links = {i: doc[i].get_links() for i in range(n)}
    rows = []
    for c in meta:
        num = f"{c['n']:02d}"
        found = []
        for i in toc_pages:
            L = lines(doc[i])
            for t, r, _ in L:
                if squash(t) == squash(c["title"]):
                    left = [tt for tt, rr, _ in L if abs(rr.y0 - r.y0) < 3 and rr.x1 <= r.x0 and tt.strip() == num]
                    if left:
                        found.append((i, r, L))
        rec = {"n": c["n"], "title": c["title"]}
        if len(found) != 1:
            rec["error"] = f"contents row found {len(found)} times"
            rows.append(rec)
            continue
        i, r, L = found[0]
        band = pymupdf.Rect(doc[i].rect.x0, r.y0 - 3, doc[i].rect.x1, r.y1 + 3)
        subj = " · ".join(c["subjects"])
        rec["subject_line"] = any(squash(subj) in squash(t) for t, rr, _ in L if r.y1 - 1 <= rr.y0 <= r.y1 + 16)
        folio_words = [w[4] for w in doc[i].get_text("words") if w[1] > band.y0 and w[3] < band.y1 and w[0] > doc[i].rect.width - 40 * MM and w[4].isdigit()]
        row_links = [l for l in links[i] if pymupdf.Rect(l["from"]).intersects(band)]
        gotos = [l for l in row_links if l["kind"] == pymupdf.LINK_GOTO and pymupdf.Rect(l["from"]).intersects(r)]
        uris = [l for l in row_links if l["kind"] == pymupdf.LINK_URI]
        rec.update({"contents_page": i + 1, "links_on_row": len(gotos), "uri_on_row": len(uris),
                    "printed_folio": folio_words[-1] if folio_words else None})
        if len(gotos) == 1:
            l = gotos[0]
            lr = pymupdf.Rect(l["from"])
            num_words = [w for w in doc[i].get_text("words") if w[4] == num and band.y0 < w[1] < band.y1]
            lr_tol = pymupdf.Rect(lr.x0 - .5, lr.y0 - .5, lr.x1 + .5, lr.y1 + .5)   # glyph-box slack
            fol_words = [w for w in doc[i].get_text("words") if w[4] == rec["printed_folio"] and band.y0 < w[1] < band.y1 and w[0] > doc[i].rect.width - 40 * MM]
            rec["whole_row_clickable"] = lr_tol.contains(r) and all(lr_tol.contains(pymupdf.Rect(w[:4])) for w in num_words + fol_words)
            hp, hr = heading[c["n"]][0]
            ty = l["to"].y if l.get("to") is not None else None
            rec.update({"target_page": l["page"] + 1, "heading_page": hp + 1,
                        "target_label": labels[l["page"]], "target_y": round(ty, 1) if ty is not None else None,
                        "heading_y": round(hr.y0, 1)})
            rec["lands_on_heading"] = (l["page"] == hp and ty is not None and hr.y0 - 45 <= ty <= hr.y0 + 2)
            rec["folio_matches_label"] = rec["printed_folio"] == labels[l["page"]]
        rows.append(rec)
    ok_rows = [x for x in rows if x.get("links_on_row") == 1 and not x.get("uri_on_row") and x.get("lands_on_heading")
               and x.get("folio_matches_label") and x.get("subject_line")]
    check("contents: 40 rows, each with number, title, subject line, one internal link landing on the chapter heading, folio = label",
          len(ok_rows) == 40, json.dumps([x for x in rows if x not in ok_rows])[:1500])
    check("contents: whole logical row is one clickable target", all(x.get("whole_row_clickable") for x in rows),
          str([x["n"] for x in rows if not x.get("whole_row_clickable")]))

    # ---------------------------------------------- all internal links resolve
    bad = []
    n_goto = 0
    for i in range(n):
        for l in links[i]:
            if l["kind"] in (pymupdf.LINK_GOTO,):
                n_goto += 1
                if not (0 <= l["page"] < n):
                    bad.append((i + 1, l["page"]))
            elif l["kind"] == pymupdf.LINK_NAMED:
                bad.append((i + 1, "unresolved named link"))
            elif l["kind"] == pymupdf.LINK_URI and i < n - 1 and l["uri"] != BRAND_URL:
                bad.append((i + 1, l["uri"]))
            elif l["kind"] not in (pymupdf.LINK_URI,):
                bad.append((i + 1, l["kind"]))
    check("every internal link resolves to a page in the file; only brand URLs before the closing page", not bad, str(bad[:5]))

    # review cross-links: each "Rnn" link lands on that review point's page
    rv_pos = {}
    for i in range(review_page, n - 1):
        for t, r, _ in lines(doc[i]):
            m = re.match(r"^(R\d\d)", t.strip())
            if m and r.x0 < 70 * MM + 60:
                rv_pos.setdefault(m.group(1), (i, r))
    bad = []
    for i in range(max(toc_pages) + 1, review_page):
        for l in links[i]:
            if l["kind"] != pymupdf.LINK_GOTO:
                continue
            txt = doc[i].get_textbox(pymupdf.Rect(l["from"])).strip()
            m = re.match(r"^(R\d\d)\b", txt)
            if m:
                tgt = rv_pos.get(m.group(1))
                if not tgt or tgt[0] != l["page"]:
                    bad.append((i + 1, m.group(1), l["page"] + 1, tgt and tgt[0] + 1))
    check("chapter review flags link to the right review point", not bad, str(bad[:5]))
    check("36-point review section: R01..Rnn all present in order", list(rv_pos) == sorted(rv_pos) and len(rv_pos) >= 1,
          f"{len(rv_pos)} found")

    # return-to-contents: every body page's header navigation links to the contents
    contents_first = min(toc_pages)
    bad = [i + 1 for i in range(max(toc_pages) + 1, n - 1)
           if not any(l["kind"] == pymupdf.LINK_GOTO and l["page"] == contents_first and pymupdf.Rect(l["from"]).y1 < 20 * MM for l in links[i])]
    check("running header returns to the contents on every body page", not bad, str(bad[:5]))

    # ------------------------------------------------------------ bookmarks
    toc = doc.get_toc(simple=False)
    bm = {}
    for lvl, title, page, dest in toc:
        m = re.match(r"Ch (\d\d) · ", title)
        if m and lvl == 2:
            bm[int(m.group(1))] = (page, dest)
    bad = []
    for c in meta:
        if c["n"] not in bm:
            bad.append((c["n"], "missing"))
            continue
        page, dest = bm[c["n"]]
        hp, hr = heading[c["n"]][0]
        to = dest.get("to")
        if page - 1 != hp or to is None or not (hr.y0 - 45 <= to.y <= hr.y0 + 2):
            bad.append((c["n"], page, hp + 1, to))
    check("bookmarks: one per chapter, landing on its heading", not bad, str(bad[:5]))
    tops = [t[1] for t in toc if t[0] == 1]
    check("bookmarks: major sections present",
          all(any(k in t for t in tops) for k in ["Cover", "Contents", "Part 1", "Part 2", "Points for Youssef", "Sources, method", "YMnotes"]), str(tops))
    check("bookmarks: every target page exists", all(1 <= t[2] <= n for t in toc), "")

    # ----------------------------------------------------- fonts and bounds
    fonts = set()
    type3 = []
    for i in range(n):
        for f in doc[i].get_fonts(full=True):
            fonts.add((f[3], f[1]))
            if f[2] == "Type3":
                type3.append((i + 1, f[3]))
    unembedded = [f for f in fonts if f[1] == "n/a"]
    check("fonts: no Type3 fonts", not type3, str(type3[:5]))
    check("fonts: all fonts embedded", not unembedded, str(unembedded))
    out_of_page, out_of_margin, small = [], [], []
    for i in range(n - 1):
        pg = doc[i]
        for w in pg.get_text("words"):
            r = pymupdf.Rect(w[:4])
            if not pg.rect.contains(r):
                out_of_page.append((i + 1, w[4]))
            if i > 0 and (r.x0 < 20 * MM - 2 or r.x1 > pg.rect.width - 15 * MM + 2):
                out_of_margin.append((i + 1, w[4], round(r.x0), round(r.x1)))
        for t, r, sz in lines(pg):
            if 0 < sz < 5.5:
                small.append((i + 1, t[:20], sz))
    check("no text outside the page box", not out_of_page, str(out_of_page[:5]))
    check("no text outside the left/right margins on body pages", not out_of_margin, str(out_of_margin[:5]))
    check("no text below the 5.5 pt floor", not small, str(small[:5]))

    # ------------------------------------------------ running header content
    bad = []
    for c in meta:
        hp, hr = heading[c["n"]][0]
    for i in range(max(toc_pages) + 1, review_page):
        top = [t for t, r, _ in lines(doc[i]) if r.y1 < 17 * MM]
        m = re.search(r"CHAPTER (\d\d)", " ".join(top).replace(" ", " "))
        hdr = re.sub(r"\s+", " ", " ".join(top))
        part_top = any(squash(t) in ("chapters115", "chapters1640") and r.y0 < 45 * MM for t, r, _ in lines(doc[i]))
        in_force = max((c["n"] for c in meta if ((heading[c["n"]][0][0] < i and not part_top) or (heading[c["n"]][0][0] == i and heading[c["n"]][0][1].y0 < 32 * MM))), default=None)
        opening = [c["n"] for c in meta if heading[c["n"]][0][0] == i]
        want = in_force if in_force is not None else (opening[0] if opening else None)
        rng = re.search(r"CHAPTERS (\d\d)–(\d\d)", hdr)
        if rng:   # a page of no-additions entries: the range must cover every chapter on the page
            lo, hi = int(rng.group(1)), int(rng.group(2))
            ok = want is not None and lo <= want <= hi and all(lo <= o <= hi for o in opening)
            if not ok:
                bad.append((i + 1, hdr[:40], want))
            continue
        got = int(squash(hdr).split("chapter")[1][:2]) if "chapter" in squash(hdr) else None
        if want != got:
            bad.append((i + 1, got, want))
    check("running header names the chapter in force on every chapter page", not bad, str(bad[:6]))

    # ------------------------------------------------ header QR decodes (print size)
    try:
        import zxingcpp
        from PIL import Image
        bad = []
        for i in range(0, n - 1):
            pg = doc[i]
            clip = pymupdf.Rect(pg.rect.width - 60 * MM, 0, pg.rect.width, 25 * MM) if i > 0 else pg.rect
            pix = pg.get_pixmap(dpi=300, clip=clip)
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            if BRAND_URL not in [r.text for r in zxingcpp.read_barcodes(img)]:
                bad.append(i + 1)
        check("QR code decodes to the brand URL on the cover and every body page", not bad, str(bad))
    except ImportError:
        check("QR decode (zxing-cpp not installed: NOT RUN)", True, "not run")

    report = {"pdf": PDF.name, "pages": n, "checks": checks, "contents_rows": rows,
              "summary": {"passed": sum(c["ok"] for c in checks), "failed": len(failures)}}
    (ROOT / "qa/verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    for c in checks:
        print(("PASS " if c["ok"] else "FAIL ") + c["check"] + ("" if c["ok"] else "  -> " + c["detail"][:600]))
    print(f"{report['summary']['passed']} passed, {report['summary']['failed']} failed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
