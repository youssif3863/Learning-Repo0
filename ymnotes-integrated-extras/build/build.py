#!/usr/bin/env python3
"""Build "YMnotes Digestive System — Integrated Teaching Extras".

    source/chapters.json     the 40-chapter map of the main book (titles, subject
                             labels, printed page ranges, book file, module part)
    source/part1-before-mid-module.md   retained additions, Chapters 1-15
    source/part2-after-mid-module.md    retained additions, Chapters 16-40
    source/review-points.md             the consolidated review points
          |
          v  parse (grammar below)            -> build/out/content.json
          v  HTML + style.css                  -> build/out/integrated.html
          v  Chromium print, pass 1            -> chapter positions (named dests)
          v  Chromium print, pass 2 (folios)   -> same pagination, real folios
          v  furniture post-pass               -> running header (mark, nav, QR),
                                                  footer, folio, return-to-contents
          v  skill append_final_page.py        -> permanent YMnotes closing page
          v  outline, page labels, metadata    -> ../<FINAL_NAME>

Run from anywhere:  python3 build/build.py      (then python3 qa/verify.py)

Source grammar (the three source/*.md files, read in that order)
-------------------------------------
    # 03                                   chapter (title etc. come from chapters.json)
    > text                                 chapter note (shown on a no-additions entry)
    ## Topic title | Book pp. 34–36        topic band inside a chapter
    ::: E03.01 | IM | Title | book=35 | src=GIT IM pp. 21–22 | from=IM:C3-02, IM:C3-03
    body: paragraphs, "- " bullets (2-space nesting), **bold**, *italic*,
    "Table: caption" followed by | pipe | rows | (first row = header)
    :::
    Subject codes: IM PHARM PATH MICRO PARA HEP; join several with "+".

    # REVIEW                               start of the review section
    ::: review R01 | ch=3 | Title | subj=PHARM | from=OS:C3-D1 (PH-15)
    A | Book p. 37 | position text
    B | Book p. 48 · GIT Others p. 4 | position text
    note | neutral note (never a verdict)
    :::
"""
import html
import json
import os
import pathlib
import re
import subprocess
import sys

import pymupdf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUTDIR = HERE / "out"
SKILL = pathlib.Path(os.environ.get(
    "YMNOTES_SKILL",
    "/root/.claude/skills/synced/9e64779b-7e56-405a-bea8-e1a695a63aec_b53328e2-3aba-468f-bac9-89c120548dbd/ymnotes-medical-book-redesign"))
FINAL_NAME = "YMnotes-Digestive-System-Integrated-Teaching-Extras.pdf"
TITLE = "YMnotes Digestive System — Integrated Teaching Extras"
FOOTER_ID = "YMNOTES MEDICAL · DIGESTIVE SYSTEM · INTEGRATED TEACHING EXTRAS"
BRAND = json.loads((HERE / "assets/brand/brand.json").read_text())
HOME_URL = BRAND["brand_home_url"] or next(
    d["url"] for d in BRAND["destinations"].values() if d["role"] == "primary")

SUBJECTS = {  # code: (css class, visible label)
    "IM": ("im", "INTERNAL MEDICINE"),
    "PHARM": ("pharm", "PHARMACOLOGY"),
    "PATH": ("path", "PATHOLOGY"),
    "MICRO": ("micro", "MICROBIOLOGY"),
    "PARA": ("para", "PARASITOLOGY"),
    "HEP": ("hep", "HEPATOLOGY"),
}
SOURCE_OF = {"IM": "GIT Internal Med", "PHARM": "GIT Others", "PATH": "GIT Others",
             "MICRO": "GIT Others", "PARA": "GIT Others", "HEP": "Hepatology"}

MM = 72 / 25.4
M_TOP = 22 * MM   # --m-top in design-tokens.css


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


PART_COL = {"a": rgb("1A5B31"), "b": rgb("2F3F86")}
PART_DEEP = {"a": rgb("0F3C21"), "b": rgb("1F2A5E")}
REVIEW_COL = rgb("7A5714")
MUTED = rgb("66756C")
RULE = rgb("D4DDD7")
SOFT = rgb("7FAE92")


# ---------------------------------------------------------------- parsing
def parse_fields(head):
    parts = [p.strip() for p in head.split(" | ")]
    pos, kv = [], {}
    for p in parts:
        m = re.match(r"^([a-z]+)=(.*)$", p)
        if m:
            kv[m.group(1)] = m.group(2).strip()
        else:
            pos.append(p)
    return pos, kv


SOURCE_FILES = ["part1-before-mid-module.md", "part2-after-mid-module.md", "review-points.md"]


def parse_source(paths):
    chapters, reviews = {}, []
    cur_ch = cur_topic = None
    in_review = False
    lines = []
    for path in paths:
        lines += [ln for ln in path.read_text(encoding="utf-8").splitlines() if not ln.startswith("<!--")] + [""]
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# "):
            tag = ln[2:].strip()
            if tag == "REVIEW":
                in_review, cur_ch = True, None
            else:
                n = int(tag)
                if n in chapters:
                    raise SystemExit(f"chapter {n} declared twice in the source")
                cur_ch = chapters[n] = {"n": n, "note": "", "topics": []}
                cur_topic = None
        elif ln.startswith("> ") and cur_ch is not None:
            cur_ch["note"] = (cur_ch["note"] + " " + ln[2:].strip()).strip()
        elif ln.startswith("## ") and cur_ch is not None:
            pos, _ = parse_fields(ln[3:])
            cur_topic = {"title": pos[0], "book": pos[1] if len(pos) > 1 else "", "entries": []}
            cur_ch["topics"].append(cur_topic)
        elif ln.startswith("::: "):
            head = ln[4:]
            body = []
            i += 1
            while lines[i].strip() != ":::":
                body.append(lines[i])
                i += 1
            if head.startswith("review "):
                pos, kv = parse_fields(head[len("review "):])
                rv = {"id": pos[0], "title": pos[1], "ch": int(kv["ch"]),
                      "subj": kv.get("subj", ""), "from": kv.get("from", ""),
                      "positions": [], "note": ""}
                for b in body:
                    if not b.strip():
                        continue
                    k, _, rest = b.partition(" | ")
                    k = k.strip()
                    if k == "note":
                        rv["note"] = rest.strip()
                    else:
                        label, _, text = rest.partition(" | ")
                        rv["positions"].append({"key": k, "label": label.strip(), "text": text.strip()})
                reviews.append(rv)
            else:
                if cur_topic is None:
                    raise SystemExit(f"entry outside a topic: {head}")
                pos, kv = parse_fields(head)
                subj = pos[1].split("+")
                for s in subj:
                    if s not in SUBJECTS:
                        raise SystemExit(f"unknown subject {s!r} in {pos[0]}")
                cur_topic["entries"].append({
                    "id": pos[0], "subjects": subj, "title": pos[2],
                    "book": kv.get("book", ""), "src": kv.get("src", ""),
                    "from": [x.strip() for x in kv.get("from", "").split(",") if x.strip()],
                    "body": "\n".join(body).strip()})
        i += 1
    return chapters, reviews


# ------------------------------------------------------------ inline markup
def inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    return s


def md_block(text):
    """Paragraphs, nested "- " lists and pipe tables. Authored text, trusted."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("Table:") or ln.startswith("|"):
            cap = ""
            if ln.startswith("Table:"):
                cap = ln[len("Table:"):].strip()
                i += 1
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], rows[1:]
            t = ['<table class="t">']
            if cap:
                t.append(f"<caption>{inline(cap)}</caption>")
            t.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>")
            t += ["<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body]
            t.append("</tbody></table>")
            out.append("".join(t))
            continue
        if re.match(r"^\s*- ", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*- ", lines[i]):
                depth = (len(lines[i]) - len(lines[i].lstrip(" "))) // 2
                items.append((depth, lines[i].strip()[2:]))
                i += 1
            html_, stack = [], []
            for depth, txt in items:
                while len(stack) > depth + 1:
                    html_.append("</li></ul>")
                    stack.pop()
                if len(stack) == depth + 1:
                    html_.append("</li>")
                while len(stack) < depth + 1:
                    html_.append("<ul>")
                    stack.append(depth)
                html_.append(f"<li>{inline(txt)}")
            while stack:
                html_.append("</li></ul>")
                stack.pop()
            out.append("".join(html_))
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^\s*- ", lines[i]) \
                and not lines[i].startswith(("Table:", "|")):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "".join(out)


def e(s):
    return html.escape(s, quote=False)


def chips(codes):
    return "".join(f'<span class="chip {SUBJECTS[c][0]}">{SUBJECTS[c][1]}</span>' for c in codes)


def svg(name):
    return re.sub(r"<\?xml.*?\?>", "", (HERE / "assets/brand" / name).read_text())


# ------------------------------------------------------------------- HTML
def pages_text(meta):
    return f'pp. {meta["start"]}–{meta["end"]}'


def file_text(meta):
    if meta["file"] == "both":
        return "book file 1 (pp. 195–197) and file 2 (pp. 197–209)"
    return "book file 1" if meta["file"] == "first" else "book file 2"


def entry_html(en):
    cls = "entry s-" + SUBJECTS[en["subjects"][0]][0]
    if len(en["body"]) > 1400:
        cls += " long"
    refs = [f'<span class="eid">{en["id"]}</span>']
    if en["book"]:
        refs.append(f'<b>Book {e(en["book"])}</b>')
    if en["src"]:
        refs.append(e(en["src"]))
    ref = '<span class="sep">·</span>'.join(r.replace(" ", " ", 1) for r in refs)
    return (f'<div class="{cls}" id="{en["id"]}"><div class="e-head"><span class="e-title">{inline(e(en["title"]))}</span>'
            f'<span class="e-chips">{chips(en["subjects"])}</span></div>'
            f'<div class="e-body">{md_block(en["body"])}</div><div class="e-ref">{ref}</div></div>')


def count_entries(ch):
    return sum(len(t["entries"]) for t in ch["topics"])


def chapter_html(meta, ch, reviews, folios, first):
    part = "b" if meta["module"] == "after" else "a"
    kick = f'CHAPTER {meta["n"]:02d}'
    part_name = "AFTER MID-MODULE" if part == "b" else "BEFORE MID-MODULE"
    if meta["n"] == 15:
        part_name += " · SPANS BOTH BOOK FILES"
    rv = [r for r in reviews if r["ch"] == meta["n"]]
    out = [f'<section class="chapter {part}{" first" if first else ""}" id="ch{meta["n"]:02d}">',
           '<div class="ch-head"><div class="ch-top"><span>'
           f'<span class="ch-kicker">{kick}</span><span class="ch-part">{part_name}</span></span>'
           '<a class="ch-back" href="#contents">↑ CONTENTS</a></div>',
           f'<h2 class="ch-title">{e(meta["title"])}</h2>',
           f'<div class="ch-sub"><b>Adds to book {pages_text(meta)}</b> · {file_text(meta)} · '
           f'book subjects: {e(" · ".join(meta["subjects"]))}</div><div class="ch-rule"></div>']
    if len(ch["topics"]) > 1:
        out.append('<div class="ch-toc"><span class="lab">IN THIS CHAPTER</span>' + '<span class="sep"> · </span>'.join(
            f'<a href="#ch{meta["n"]:02d}-t{ti + 1}">{e(t["title"])}</a>' for ti, t in enumerate(ch["topics"])) + '</div>')
    out.append('</div>')
    for ti, t in enumerate(ch["topics"]):
        bref = f'<span class="bref">BOOK {e(t["book"].replace("Book ", "").upper())}</span>' if t["book"] else ""
        out.append(f'<div class="topic" id="ch{meta["n"]:02d}-t{ti + 1}"><h3>{e(t["title"])}{bref}</h3>')
        out += [entry_html(en) for en in t["entries"]]
        out.append("</div>")
    if rv:
        links = " · ".join(
            f'<a href="#rv-{r["id"]}">{r["id"]} {e(r["title"])} <span class="pg">(p. {folios.get("rv-" + r["id"], "00")})</span></a>'
            for r in rv)
        out.append(f'<div class="flagline"><span class="fl">FOR REVIEW</span>Source disagreements for this chapter '
                   f'are kept out of the teaching points above: {links}</div>')
    out.append("</section>")
    return "\n".join(out)


def stub_html(meta, ch, reviews, folios):
    part = "b" if meta["module"] == "after" else "a"
    rv = [r for r in reviews if r["ch"] == meta["n"]]
    note = inline(re.sub(r"^No additions\.\s*", "", ch["note"])) if ch and ch.get("note") else ""
    rvl = ""
    if rv:
        rvl = " Review point: " + " · ".join(
            f'<a href="#rv-{r["id"]}"><b>{r["id"]}</b> {e(r["title"])} (p. {folios.get("rv-" + r["id"], "00")})</a>' for r in rv) + "."
    return (f'<div class="stub {part}" id="ch{meta["n"]:02d}"><div class="sk">CHAPTER {meta["n"]:02d}</div>'
            f'<div><div class="st">{e(meta["title"])}<span class="none">NO ADDITIONS</span></div>'
            f'<div class="ss"><b>Book {pages_text(meta)}</b> · {file_text(meta)} · {e(" · ".join(meta["subjects"]))}</div>'
            f'<span class="sb">{note}{rvl}</span></div></div>')


def review_html(meta_by_n, reviews, folios):
    out = ['<section class="review" id="review">',
           '<p class="kicker">SEPARATE FROM THE TEACHING POINTS</p>',
           '<h2 class="front-title">Points for Youssef to Review</h2>',
           '<div class="intro"><p>These are disagreements found while comparing the three source handouts with the main book. '
           'Each point shows both (or all) positions with their page references. <b>None of them has been resolved here</b>, and '
           'none of the disputed values is used as a teaching point in the chapters.</p>'
           '<p>Duplicate flags raised by more than one handout are merged. The ID in brackets under each point '
           'traces it to the original handout and ledger row.</p></div>']
    last = None
    for r in sorted(reviews, key=lambda r: (r["ch"], r["id"])):
        m = meta_by_n[r["ch"]]
        if r["ch"] != last:
            part = "b" if m["module"] == "after" else "a"
            out.append(f'<div class="rv-ch {part}"><a href="#ch{m["n"]:02d}"><span class="rk">CHAPTER {m["n"]:02d}</span>'
                       f'{e(m["title"])} <span style="font:400 7.4pt var(--font-ui);color:var(--c-muted)">· p. {folios.get(f"ch{m[chr(110)]:02d}", "00")}</span></a></div>')
            last = r["ch"]
        grid = "rv-grid three" if len(r["positions"]) == 3 else "rv-grid"
        pos = "".join(f'<div class="rv-pos"><span class="pl">{inline(p["label"])}</span>{inline(p["text"])}</div>' for p in r["positions"])
        chip = chips(r["subj"].split("+")) if r["subj"] else ""
        note = f'<div class="rv-note">{inline(r["note"])}</div>' if r["note"] else ""
        out.append(f'<div class="rv" id="rv-{r["id"]}"><div class="rv-head"><span class="rv-title"><span class="rid">{r["id"]}</span>{inline(e(r["title"]))}</span>'
                   f'<span class="e-chips">{chip}</span></div><div class="{grid}">{pos}</div>{note}'
                   f'<div class="rv-src">Raised by: {e(r["from"])}</div></div>')
    notes = ROOT / "source/wording-notes.html"
    if notes.exists():
        out.append(notes.read_text(encoding="utf-8"))
    out.append("</section>")
    return "\n".join(out)


def fill(text, stats):
    for k, v in stats.items():
        text = text.replace("{{" + k + "}}", str(v))
    if re.search(r"\{\{[A-Z_]+\}\}", text):
        raise SystemExit("unfilled placeholder in method page: " + re.search(r"\{\{[A-Z_]+\}\}", text).group(0))
    return text


def build_html(chap_meta, chapters, reviews, method_html, folios, stats):
    meta_by_n = {m["n"]: m for m in chap_meta}
    # ---- cover
    cover = f'''
<section class="cover">
  <div class="band"></div><div class="band2"></div>
  <div class="emblem">{svg("ymnotes-symbol.svg")}</div>
  <div class="inner">
    <div class="logo">{svg("ymnotes-mark-h.svg")}</div>
    <div class="eyebrow">TEACHING COMPANION · VERSION 3 · CHAPTERS 1–40</div>
    <h1>YMnotes Digestive System<span class="sub">Integrated Teaching Extras</span></h1>
    <div class="rule"></div>
    <p class="lede">Everything the three extras handouts add to the main book, merged into one book and filed under the chapter it belongs to.
    Teach a chapter from the book, then turn to the same chapter here.</p>
    <div class="parts">
      <div class="part"><b>Part 1 · Before mid-module</b>Chapters 1–15 · book file 1, pp. 1–197<br>Chapter 15 continues to p. 209 in file 2</div>
      <div class="part b"><b>Part 2 · After mid-module</b>Chapters 16–40 · book file 2, pp. 197–433</div>
    </div>
    <div class="subjects">{chips(["IM", "PHARM", "PATH", "MICRO", "PARA", "HEP"])}</div>
  </div>
  <div class="meta">
    <div><b>{stats["entries"]} teaching additions · {stats["reviews"]} points for review</b><br>
    From GIT Internal Med, GIT Others and the Hepatology source<br>Keyed to the printed page numbers of the main book</div>
    <a class="qr" href="{html.escape(HOME_URL)}">{svg("qr-youtube.svg")}YMNOTES</a>
  </div>
</section>'''
    # ---- contents
    rows = []

    def row(meta, part):
        n = meta["n"]
        ch = chapters.get(n)
        k = count_entries(ch) if ch else 0
        nrv = sum(1 for r in reviews if r["ch"] == n)
        if k:
            info = f'{k} addition{"s" if k != 1 else ""}' + (f' · {nrv} review' if nrv else "")
        else:
            info = "No additions" + (f' · {nrv} review' if nrv else "")
        cls = [part] + ([] if k else ["empty"])
        return (f'<li class="{" ".join(cls)}"><a href="#ch{n:02d}"><span class="no">{n:02d}</span>'
                f'<span class="t">{e(meta["title"])}<span class="subj">{e(" · ".join(meta["subjects"]))}</span></span>'
                f'<span class="bk">Book {pages_text(meta)}</span><span class="n">{info}</span>'
                f'<span class="pg">{folios.get(f"ch{n:02d}", "00")}</span></a></li>')

    cols = '<div class="toc-cols"><span>CH</span><span>BOOK CHAPTER · SUBJECTS</span><span>BOOK PAGES</span><span>IN THIS HANDOUT</span><span>PAGE</span></div>'
    rows.append('<a class="toc-part" href="#part-a"><span class="pn">PART 1 · BEFORE MID-MODULE</span>'
                '<span class="pd">Chapters 1–15 · book file 1 (printed pp. 1–197); Chapter 15 runs on to p. 209 in file 2</span></a>' + cols + '<ul class="toc">')
    rows += [row(m, "a") for m in chap_meta if m["module"] != "after"]
    rows.append('</ul><a class="toc-part b" href="#part-b"><span class="pn">PART 2 · AFTER MID-MODULE</span>'
                '<span class="pd">Chapters 16–40 · book file 2 (printed pp. 197–433)</span></a>' + cols + '<ul class="toc">')
    rows += [row(m, "b") for m in chap_meta if m["module"] == "after"]
    rows.append('</ul><div class="toc-part x"><span class="pn">AFTER THE CHAPTERS</span><span class="pd">Kept apart from the teaching points</span></div><ul class="toc">')
    rows.append(f'<li class="x"><a href="#review"><span class="no">R</span><span class="t">Points for Youssef to Review'
                f'<span class="subj">{stats["reviews"]} source disagreements · both positions, with page references · not resolved</span></span>'
                f'<span class="bk"></span><span class="n"></span><span class="pg">{folios.get("review", "00")}</span></a></li>')
    rows.append(f'<li class="x"><a href="#method"><span class="no">M</span><span class="t">Sources, method and traceability'
                f'<span class="subj">The three handouts, page conventions, what was merged or left out</span></span>'
                f'<span class="bk"></span><span class="n"></span><span class="pg">{folios.get("method", "00")}</span></a></li></ul>')
    legend = "".join([chips([c]) for c in SUBJECTS])
    front = f'''
<section class="front" id="contents">
  <p class="kicker">INTERACTIVE CONTENTS · ALL 40 CHAPTERS</p>
  <h2 class="front-title">Chapter by chapter</h2>
  <div class="howto">
    <p><b>How to use it.</b> Teach a chapter from the main book, then open the same chapter here: every point adds something that is <b>not</b> on those book pages.
    Each point ends with its ID, <b>Book p.</b> (the printed page it extends) and its source page. Click a chapter to jump to it; <b>↑ Contents</b> and the running header bring you back.
    Source disagreements are not taught as facts; they are in <b>Points for Youssef to Review</b>.</p>
    <div class="legend"><span class="lab">SUBJECT LABELS</span>{legend}</div>
  </div>
  {"".join(rows)}
</section>'''
    # ---- body
    body = []
    first_after = True
    body.append('<div class="part-open" id="part-a"><div class="pk">PART 1 · BEFORE MID-MODULE</div>'
                '<h2>Chapters 1–15</h2><p>Book file 1, printed pp. 1–197. Chapter 15 (Colorectal Cancer) starts on p. 195 and runs on into book file 2 '
                'to p. 209; printed p. 197 appears in both files. It is treated here as one chapter.</p></div>')
    stub_run = []

    def flush(part):
        if stub_run:
            body.append(f'<div class="stubs {part}">' + "".join(stub_run) + "</div>")
            stub_run.clear()

    first = True
    for m in chap_meta:
        part = "b" if m["module"] == "after" else "a"
        if part == "b" and first_after:
            flush("a")
            body.append('<div class="part-open b" id="part-b"><div class="pk">PART 2 · AFTER MID-MODULE</div>'
                        '<h2>Chapters 16–40</h2><p>Book file 2, printed pp. 197–433 (Chapter 16 starts on p. 210). '
                        'Most additions here come from the Hepatology source.</p></div>')
            first_after, first = False, True
        ch = chapters.get(m["n"])
        if ch and count_entries(ch):
            flush(part)
            body.append(chapter_html(m, ch, reviews, folios, first))
        else:
            stub_run.append(stub_html(m, ch, reviews, folios))
        first = False
    flush("b")
    body.append(review_html(meta_by_n, reviews, folios))
    body.append(method_html)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(TITLE)}</title>'
            f'<link rel="stylesheet" href="../style.css"></head><body>{cover}{front}{"".join(body)}</body></html>')


# ----------------------------------------------------------------- render
def render(html_text, pdf_path):
    OUTDIR.mkdir(exist_ok=True)
    src = OUTDIR / "integrated.html"
    src.write_text(html_text, encoding="utf-8")
    subprocess.run(["node", str(HERE / "render.cjs"), str(src), str(pdf_path)], check=True)


def named_positions(pdf_path):
    """Named destinations -> (0-based page, y from the TOP of the page, in points).

    Chromium writes each /XYZ destination bottom-up and relative to the page
    AREA (inside the @page margins), not the sheet: measured on the saved file,
    every target sat exactly one top margin above its element. Convert to a
    top-down y on the sheet."""
    doc = pymupdf.open(pdf_path)
    names = doc.resolve_names()
    out = {}
    for k, v in names.items():
        h = doc[v["page"]].rect.height
        out[k] = (v["page"], max(0.0, h - v["to"][1]) + M_TOP)
    return out, doc.page_count


def explicit_links(doc, pos):
    """Replace Chromium's named GoTo links with explicit ones at the true
    element position (a little air above it), so every target is exact and no
    later tool has to resolve a name."""
    n = 0
    for page in doc:
        for l in page.get_links():
            if l["kind"] == pymupdf.LINK_NAMED:
                name = l.get("nameddest") or l.get("name")
                if name not in pos:
                    raise SystemExit(f"link to unknown destination {name!r} on page {page.number + 1}")
                p, y = pos[name]
                page.delete_link(l)
                page.insert_link({"kind": pymupdf.LINK_GOTO, "from": l["from"], "page": p,
                                  "to": pymupdf.Point(0, max(0, y - 6)), "zoom": 0})
                n += 1
    return n


# -------------------------------------------------------------- furniture
class Fonts:
    def __init__(self):
        f = HERE / "assets/fonts"
        self.disp = pymupdf.Font(fontfile=str(f / "Archivo-Semibold.ttf"))
        self.disp_b = pymupdf.Font(fontfile=str(f / "Archivo-Bold.ttf"))
        self.ui = pymupdf.Font(fontfile=str(f / "Inter-Medium.ttf"))


def svg_pdf(name, hexcolor):
    s = (HERE / "assets/brand" / name).read_text().replace("currentColor", hexcolor)
    d = pymupdf.open(stream=s.encode(), filetype="svg")
    return pymupdf.open("pdf", d.convert_to_pdf())


TOP_ZONE = 32 * MM   # a heading this close to the top of the sheet "opens" the page


def page_nav(pos, chap_meta, n_pages, special, empty):
    """Header navigation per page: the chapter in force at the top of the page;
    if none, the first chapter opening on it; a page holding only no-additions
    entries gets a range label."""
    starts = sorted((pos[f"ch{m['n']:02d}"][0], pos[f"ch{m['n']:02d}"][1], m) for m in chap_meta)
    nav = {}
    part_top = {pos[k][0] for k in ("part-a", "part-b") if pos[k][1] < TOP_ZONE}
    for i in range(1, n_pages):
        cur = None
        for pi, y, m in starts:
            if (pi < i and i not in part_top) or (pi == i and y < TOP_ZONE):
                cur = m
        opening = [m for pi, y, m in starts if pi == i]
        if cur is None and opening:
            cur = opening[0]
        on_page = ([cur] if cur and cur not in opening else []) + opening
        if len(on_page) > 1 and all(m["n"] in empty for m in on_page):
            nav[i] = ("range", (on_page[0], on_page[-1]))
        else:
            nav[i] = ("chapter", cur)
    for key, label in special:
        p0, y0 = pos[key]
        for i in range(p0 if y0 < TOP_ZONE else p0 + 1, n_pages):
            nav[i] = ("label", label)
    for i in range(pos["contents"][0], pos["part-a"][0]):
        nav[i] = ("label", "CONTENTS")
    if pos["contents"][0] != 1:
        raise SystemExit("contents does not start on physical page 2")
    return nav


def furniture(pdf_in, pdf_out, chap_meta, pos, contents_pages, empty):
    doc = pymupdf.open(pdf_in)
    explicit_links(doc, pos)
    F = Fonts()
    mark = svg_pdf("ymnotes-mark-h.svg", "#1A5B31")
    qr = svg_pdf("qr-youtube-compact.svg", "#0F3C21")
    n = doc.page_count
    special = [("review", "POINTS FOR YOUSSEF TO REVIEW"), ("method", "SOURCES, METHOD AND TRACEABILITY")]
    nav = page_nav(pos, chap_meta, n, special, empty)
    W, H = doc[0].rect.width, doc[0].rect.height
    left, right = 20 * MM, W - 15 * MM
    contents_page = pos["contents"][0]
    report = {}
    for i, page in enumerate(doc):
        if i == 0:
            continue
        kind, val = nav[i]
        part = "a"
        if kind == "range":
            a, b = val
            part = "b" if a["module"] == "after" else "a"
            nav_a, nav_b = f'CHAPTERS {a["n"]:02d}–{b["n"]:02d}', "No additions"
        elif kind == "chapter" and val is not None:
            part = "b" if val["module"] == "after" else "a"
            nav_a, nav_b = f'CHAPTER {val["n"]:02d}', val.get("nav") or val["title"]
        elif kind == "chapter":
            nav_a, nav_b = "PART 1 · BEFORE MID-MODULE", ""
        else:
            nav_a, nav_b = val, ""
        col = REVIEW_COL if nav_a.startswith("POINTS") else PART_COL[part]
        # mark (link) and QR (link)
        mh = 5.8 * MM
        mw = mh * mark[0].rect.width / mark[0].rect.height
        mr = pymupdf.Rect(left, 9.2 * MM, left + mw, 9.2 * MM + mh)
        page.show_pdf_page(mr, mark, 0)
        page.insert_link({"kind": pymupdf.LINK_URI, "from": mr, "uri": HOME_URL})
        qs = 11.4 * MM
        qrr = pymupdf.Rect(right - qs, 5.4 * MM, right, 5.4 * MM + qs)
        page.show_pdf_page(qrr, qr, 0)
        page.insert_link({"kind": pymupdf.LINK_URI, "from": qrr, "uri": HOME_URL})
        # navigation: tracked capitals + title, centred in the free zone
        size = 7.8
        track = size * 0.085
        sep = "  ·  " if nav_b else ""
        zone_l, zone_r = mr.x1 + 6 * MM, qrr.x0 - 6 * MM

        def width(a, b):
            return sum(F.disp_b.text_length(c, size) + track for c in a) + F.disp.text_length(b, size)

        if width(nav_a, sep + nav_b) > zone_r - zone_l:
            short = (val.get("nav_short") if kind == "chapter" and val else None)
            if short and width(nav_a, sep + short) <= zone_r - zone_l:
                nav_b = short
            else:
                nav_b, sep = "", ""
        if width(nav_a, sep + nav_b) > zone_r - zone_l:
            raise SystemExit(f"header navigation does not fit on page {i + 1}: {nav_a}")
        wtot = width(nav_a, sep + nav_b)
        x = (zone_l + zone_r) / 2 - wtot / 2
        y = 13.3 * MM
        tw = pymupdf.TextWriter(page.rect)
        xx = x
        for c in nav_a:
            tw.append((xx, y), c, font=F.disp_b, fontsize=size)
            xx += F.disp_b.text_length(c, size) + track
        tw.write_text(page, color=col)
        if nav_b:
            tw2 = pymupdf.TextWriter(page.rect)
            tw2.append((xx, y), sep + nav_b, font=F.disp, fontsize=size)
            tw2.write_text(page, color=MUTED)
        # the navigation line returns to the contents (not on the contents itself)
        if i not in contents_pages:
            nr = pymupdf.Rect(x - 1, y - size, x + wtot + 1, y + 2.4)
            page.insert_link({"kind": pymupdf.LINK_GOTO, "from": nr, "page": contents_page,
                              "to": pymupdf.Point(0, 0), "zoom": 0})
        page.draw_line((left, 17.6 * MM), (right, 17.6 * MM), color=RULE, width=0.4)
        # footer: identity rule, identity line, folio tab in the part colour
        fy = H - 11.2 * MM
        page.draw_line((left, fy - 3.4 * MM), (left + 9 * MM, fy - 3.4 * MM), color=SOFT, width=0.9)
        tw3 = pymupdf.TextWriter(page.rect)
        xx = left
        for c in FOOTER_ID:
            tw3.append((xx, fy), c, font=F.ui, fontsize=6.6)
            xx += F.ui.text_length(c, 6.6) + 6.6 * 0.14
        tw3.write_text(page, color=MUTED)
        folio = str(i)
        bw, bh = 9.5 * MM, 5.2 * MM
        box = pymupdf.Rect(right - bw, fy - 4.0 * MM, right, fy - 4.0 * MM + bh)
        page.draw_rect(box, color=col, width=0.9)
        fw = F.disp_b.text_length(folio, 8.4)
        tw4 = pymupdf.TextWriter(page.rect)
        tw4.append((box.x0 + (bw - fw) / 2, box.y1 - 1.55 * MM), folio, font=F.disp_b, fontsize=8.4)
        tw4.write_text(page, color=PART_DEEP[part] if col != REVIEW_COL else REVIEW_COL)
        report[i + 1] = f"{nav_a} {nav_b}".strip()
    doc.save(pdf_out, garbage=3, deflate=True)
    return report


def finish(pdf_in, pdf_out, chap_meta, chapters, reviews, pos):
    doc = pymupdf.open(pdf_in)

    def dest(key):
        p, y = pos[key]
        return {"kind": pymupdf.LINK_GOTO, "page": p, "to": pymupdf.Point(0, max(0, y - 6)), "zoom": 0}

    toc = [[1, "Cover", 1], [1, "Contents (all 40 chapters)", pos["contents"][0] + 1, dest("contents")]]
    toc.append([1, "Part 1 · Before mid-module (Chapters 1–15)", pos["part-a"][0] + 1, dest("part-a")])
    for m in chap_meta:
        if m["module"] == "after" and m["n"] == 16:
            toc.append([1, "Part 2 · After mid-module (Chapters 16–40)", pos["part-b"][0] + 1, dest("part-b")])
        key = f'ch{m["n"]:02d}'
        ch = chapters.get(m["n"])
        k = count_entries(ch) if ch else 0
        label = f'Ch {m["n"]:02d} · {m["title"]}' + ("" if k else " (no additions)")
        toc.append([2, label, pos[key][0] + 1, dest(key)])
        if k:
            for ti, t in enumerate(ch["topics"]):
                tk = f"{key}-t{ti + 1}"
                if tk in pos:
                    toc.append([3, t["title"], pos[tk][0] + 1, dest(tk)])
    toc.append([1, "Points for Youssef to Review", pos["review"][0] + 1, dest("review")])
    for r in sorted(reviews, key=lambda r: (r["ch"], r["id"])):
        toc.append([2, f'{r["id"]} · Ch {r["ch"]:02d} · {r["title"]}', pos["rv-" + r["id"]][0] + 1, dest("rv-" + r["id"])])
    toc.append([1, "Sources, method and traceability", pos["method"][0] + 1, dest("method")])
    toc.append([1, "YMnotes", doc.page_count])
    doc.set_toc(toc)
    n = doc.page_count
    doc.set_page_labels([
        {"startpage": 0, "prefix": "Cover", "style": "", "firstpagenum": 1},
        {"startpage": 1, "prefix": "", "style": "D", "firstpagenum": 1},
        {"startpage": n - 1, "prefix": "YMnotes", "style": "", "firstpagenum": 1},
    ])
    doc.set_metadata({"title": TITLE, "author": "YMnotes", "subject": "Digestive System — integrated teaching extras (Chapters 1–40)",
                      "keywords": "YMnotes Medical; digestive system; internal medicine; pharmacology; pathology; microbiology; parasitology; hepatology",
                      "creator": "YMnotes Medical", "producer": "YMnotes Medical"})
    doc.save(pdf_out, garbage=3, deflate=True)
    return toc


# ------------------------------------------------------------------- main
def main():
    chap_meta = json.loads((ROOT / "source/chapters.json").read_text(encoding="utf-8"))["chapters"]
    if [m["n"] for m in chap_meta] != list(range(1, 41)):
        raise SystemExit("chapters.json must list chapters 1-40 in order")
    chapters, reviews = parse_source([ROOT / "source" / f for f in SOURCE_FILES])
    stats = {"entries": sum(count_entries(c) for c in chapters.values()), "reviews": len(reviews)}
    all_entries = [en for c in chapters.values() for t in c["topics"] for en in t["entries"]]
    for code in SUBJECTS:
        stats["N_" + code] = sum(1 for en in all_entries if code in en["subjects"])
    stats["N_ENTRIES"] = stats["entries"]
    stats["N_REVIEWS"] = stats["reviews"]
    stats["N_CH_WITH"] = sum(1 for c in chapters.values() if count_entries(c))
    stats["N_CH_EMPTY"] = 40 - stats["N_CH_WITH"]
    stats["N_ROWS"] = len({x for en in all_entries for x in en["from"]})
    method_html = fill((ROOT / "source/method.html").read_text(encoding="utf-8"), stats)
    ids = [en["id"] for c in chapters.values() for t in c["topics"] for en in t["entries"]] + [r["id"] for r in reviews]
    dup = {x for x in ids if ids.count(x) > 1}
    if dup:
        raise SystemExit(f"duplicate ids: {sorted(dup)}")
    for r in reviews:
        if r["ch"] not in range(1, 41):
            raise SystemExit(f"review {r['id']} has no valid chapter")
    OUTDIR.mkdir(exist_ok=True)
    (OUTDIR / "content.json").write_text(json.dumps(
        {"chapters": [chapters[k] for k in sorted(chapters)], "reviews": reviews, "stats": stats},
        ensure_ascii=False, indent=1), encoding="utf-8")

    p1 = OUTDIR / "pass1.pdf"
    render(build_html(chap_meta, chapters, reviews, method_html, {}, stats), p1)
    pos1, _ = named_positions(p1)
    folios = {k: str(v[0]) for k, v in pos1.items()}
    p2 = OUTDIR / "pass2.pdf"
    render(build_html(chap_meta, chapters, reviews, method_html, folios, stats), p2)
    pos, npages = named_positions(p2)
    moved = [k for k in folios if str(pos.get(k, (None,))[0]) != folios[k]]
    if moved:
        raise SystemExit(f"pagination moved between passes: {moved[:8]}")
    contents_pages = set(range(pos["contents"][0], pos["part-a"][0]))
    p3 = OUTDIR / "furnished.pdf"
    empty = {m["n"] for m in chap_meta if not (chapters.get(m["n"]) and count_entries(chapters[m["n"]]))}
    nav_report = furniture(p2, p3, chap_meta, pos, contents_pages, empty)
    p4 = OUTDIR / "with-closing.pdf"
    if p4.exists():
        p4.unlink()
    subprocess.run([sys.executable, str(SKILL / "scripts/append_final_page.py"), str(p3),
                    str(HERE / "assets/brand/ymnotes-closing-page.pdf"), str(p4)],
                   check=True, cwd=str(SKILL / "scripts"))
    final = ROOT / FINAL_NAME
    toc = finish(p4, final, chap_meta, chapters, reviews, pos)
    build_map = {
        "final_pdf": FINAL_NAME,
        "page_count": pymupdf.open(final).page_count,
        "contents_pages_physical": sorted(p + 1 for p in contents_pages),
        "destinations": {k: {"physical_page": v[0] + 1, "folio": str(v[0]), "y": round(v[1], 2)} for k, v in sorted(pos.items())},
        "header_navigation": nav_report,
        "outline": [[t[0], t[1], t[2]] for t in toc],
        "stats": stats,
    }
    (OUTDIR / "build-map.json").write_text(json.dumps(build_map, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {final.name}: {build_map['page_count']} pages, {stats['entries']} additions, {stats['reviews']} review points")


if __name__ == "__main__":
    main()
