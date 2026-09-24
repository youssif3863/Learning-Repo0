#!/usr/bin/env python3
"""Two-pass render, assembly and verification of the companion PDF.

1. build.py -> html; render body; locate each chapter's page; write folios; re-render.
2. cover + body + permanent YMnotes closing page (skill's append_final_page.py).
3. Bookmarks (outline), page labels, metadata.
4. Verify: contents links land on each chapter's opening page, folio == page label,
   every item id present, no text outside the page box, fonts embedded.
"""
import json, pathlib, re, subprocess, sys
import pymupdf

B = pathlib.Path(__file__).resolve().parent
OUT = B / "out"
SKILL = pathlib.Path("/root/.claude/skills/synced/9e64779b-7e56-405a-bea8-e1a695a63aec_b53328e2-3aba-468f-bac9-89c120548dbd/ymnotes-medical-book-redesign")
FINAL = B.parent / "YMnotes-Digestive-System-Additional-Teaching-Points-Part-1.pdf"
TITLE = "YMnotes Digestive System — Additional Teaching Points, Part 1 (Before Mid-Module Exam)"


def run(*a):
    subprocess.run(a, check=True, cwd=B)


def chapter_pages(pdf, structure):
    # the contents rows are internal links to #chNN; their resolved targets are the openers
    d = pymupdf.open(pdf)
    cp = next(i for i, p in enumerate(d) if "MAIN-BOOK CHAPTER" in p.get_text())
    links = sorted((l for l in d[cp].get_links() if l["kind"] in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED)), key=lambda l: l["from"].y0)
    assert len(links) == len(structure), len(links)
    pages = {}
    for c, l in zip(structure, links):
        assert c["title"] in d[l["page"]].get_text().replace("\n", " "), (c["title"], l["page"])
        pages[f"ch{c['num']:02d}"] = l["page"] + 1   # body folio (1-based)
    return pages


def install_fonts():
    # Chromium header/footer templates cannot use the page's @font-face, so the
    # YMnotes static fonts are made available to fontconfig instead.
    dest = pathlib.Path.home() / ".fonts" / "ymnotes"
    dest.mkdir(parents=True, exist_ok=True)
    for ttf in (B / "fonts").glob("*.ttf"):
        (dest / ttf.name).write_bytes(ttf.read_bytes())
    subprocess.run(["fc-cache", "-f", str(dest)], check=False)


def main():
    install_fonts()
    (OUT / "folios.json").unlink(missing_ok=True)
    run(sys.executable, "build.py")
    run("node", "render.cjs", str(OUT / "body.pdf"), "handout")
    structure = json.loads((OUT / "structure.json").read_text())
    folios = chapter_pages(OUT / "body.pdf", structure)
    (OUT / "folios.json").write_text(json.dumps(folios))
    run(sys.executable, "build.py")
    run("node", "render.cjs", str(OUT / "body.pdf"), "handout")
    run("node", "render.cjs", str(OUT / "cover.pdf"), "cover")
    assert chapter_pages(OUT / "body.pdf", structure) == folios, "pagination moved between passes"

    doc = pymupdf.open(OUT / "cover.pdf")
    assert doc.page_count == 1, doc.page_count
    body = pymupdf.open(OUT / "body.pdf")
    names = body.resolve_names()
    doc.insert_pdf(body)
    # insert_pdf drops named-destination links: re-create every body link as an explicit GoTo
    for i, bp in enumerate(body):
        for l in bp.get_links():
            if l["kind"] in (pymupdf.LINK_NAMED, pymupdf.LINK_GOTO):
                nd = names[l["nameddest"]] if l.get("nameddest") else {"page": l["page"], "to": (0, 841.92)}
                h = body[nd["page"]].rect.height
                y = max(0.0, h - nd["to"][1] - 6)   # PDF user space (bottom-up) -> top-down
                doc[i + 1].insert_link({"kind": pymupdf.LINK_GOTO, "from": l["from"], "page": nd["page"] + 1,
                                        "to": pymupdf.Point(0, y), "zoom": 0})
            elif l["kind"] == pymupdf.LINK_URI:
                doc[i + 1].insert_link({"kind": pymupdf.LINK_URI, "from": l["from"], "uri": l["uri"]})
    doc.save(OUT / "merged.pdf")
    run(sys.executable, str(SKILL / "scripts" / "append_final_page.py"), str(OUT / "merged.pdf"),
        str(SKILL / "assets" / "brand" / "ymnotes-closing-page.pdf"), str(OUT / "withclose.pdf"))

    doc = pymupdf.open(OUT / "withclose.pdf")
    n = doc.page_count
    body_n = n - 2
    # bookmarks: front matter, chapters, topics (level 2), items are not bookmarked
    toc = [[1, "Cover", 1]]
    def find(text, start):
        for i in range(start, n - 1):
            if text in doc[i].get_text().replace("\n", " "):
                return i + 1
        raise SystemExit(f"not found: {text}")
    toc.append([1, "How to use this companion", find("How to use this companion", 1)])
    toc.append([1, "Contents", find("MAIN-BOOK CHAPTER", 1)])
    for c in structure:
        p = folios[f"ch{c['num']:02d}"] + 1
        toc.append([1, f"{c['num']:02d}  {c['title']}", p])
        last = p
        for t in c["topics"]:
            q = find(t, last - 1)
            toc.append([2, t.split(" Main p")[0], q]); last = q
    toc.append([1, "YMnotes Medical", n])
    doc.set_toc(toc)
    doc.set_page_labels([{"startpage": 0, "prefix": "Cover", "style": ""},
                         {"startpage": 1, "prefix": "", "style": "D", "firstpagenum": 1},
                         {"startpage": n - 1, "prefix": "YMnotes", "style": ""}])
    doc.set_metadata({"title": TITLE, "author": "YMnotes Medical", "subject": "Digestive System companion: additions from GIT Internal Med, chapters 1–15",
                      "keywords": "YMnotes; digestive system; GIT; internal medicine; companion"})
    doc.save(FINAL, garbage=3, deflate=True)
    verify(structure, folios)


def verify(structure, folios):
    d = pymupdf.open(FINAL)
    report = {"pages": d.page_count, "checks": []}
    ok = True
    def check(name, cond, detail=""):
        nonlocal ok
        ok &= bool(cond)
        report["checks"].append({"check": name, "pass": bool(cond), "detail": detail})
    # contents contract: one internal link per chapter row, landing on that chapter's opener, folio == label
    contents_page = next(i for i, p in enumerate(d) if "MAIN-BOOK CHAPTER" in p.get_text())
    links = [l for l in d[contents_page].get_links() if l["kind"] == pymupdf.LINK_GOTO]
    uris = [l for l in d[contents_page].get_links() if l["kind"] == pymupdf.LINK_URI]
    check("contents has no external links", not uris)
    check("contents has one internal link per chapter", len(links) == 15, f"{len(links)} links")
    links.sort(key=lambda l: l["from"].y0)
    for c, lk in zip(structure, links):
        k = f"ch{c['num']:02d}"
        target = folios[k]  # physical index = folio (cover is index 0)
        row = [lk] if lk["page"] == target else []
        opener_text = d[target].get_text().replace("\n", " ")
        check(f"{k} link lands on opener", row and c["title"] in opener_text and c["item_ids_first"] in opener_text, f"target idx {target}")
        check(f"{k} folio equals page label", d[target].get_label() == str(folios[k]), d[target].get_label())
        rects = [l["from"] for l in row]
        vis = d[contents_page].get_textbox(rects[0]) if rects else ""
        check(f"{k} row shows number/title/subject/folio", rects and c["title"] in vis.replace("\n", " ") and str(folios[k]) in vis and c["subjects"].split(" · ")[0] in vis, vis.replace("\n", " | ")[:140])
    # every item id present in text
    txt = "\n".join(p.get_text() for p in d)
    for c in structure:
        for it in c["items"]:
            check(f"item {it['id']} rendered", it["id"] in txt)
    # geometry: no text outside page box / into header-footer bands (body pages)
    bad = []
    for i, p in enumerate(d):
        if i in (0, d.page_count - 1):
            continue
        for b in p.get_text("blocks"):
            x0, y0, x1, y1 = b[:4]
            if x0 < 20 or x1 > p.rect.width - 20:
                bad.append((i + 1, round(x0), round(x1), b[4][:30]))
    check("no text outside horizontal margins", not bad, str(bad[:5]))
    fonts = {f[3] for p in d for f in p.get_fonts()}
    check("fonts embedded (no Type3)", all("Type3" not in str(f) for p in d for f in p.get_fonts()), ", ".join(sorted(fonts))[:300])
    check("outline present", len(d.get_toc()) >= 17, f"{len(d.get_toc())} entries")
    (OUT / "verification.json").write_text(json.dumps(report, indent=1))
    fails = [c for c in report["checks"] if not c["pass"]]
    print(f"pages={d.page_count} checks={len(report['checks'])} failures={len(fails)}")
    for f in fails: print("FAIL", f)
    if not ok: sys.exit(1)


if __name__ == "__main__":
    main()
