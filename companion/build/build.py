#!/usr/bin/env python3
"""Build the YMnotes companion handout.

source/handout.md  ->  build/out/handout.html  ->  (render.cjs, Chromium)  ->  PDF
then: outline/bookmarks, page labels, closing page, verification.

Source grammar (plain text, editable by hand):
  # NN | Chapter title | main=<printed first page> | subjects=A · B
  > note paragraph shown under the chapter header (optional; used for "no additions")
  ## Topic heading | Main p. X
  ::: kind ID | Item title | main=<printed pages> | im=<IM pages> | section=<main section>
  paragraph lines; "- " bullet; "  - " second-level bullet
  | a | b |   table rows (first row = header); "Table: caption" line before it
  Main book: ...      (discrepancy only: a "Main book:" line and an "IM:" line become a comparison grid)
  :::
kind = addition | pearl | discrepancy
"""
import html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
COMP = ROOT.parent
SRC = COMP / "source" / "handout.md"
OUT = ROOT / "out"
TITLE = "YMnotes Digestive System — Additional Teaching Points, Part 1 (Before Mid-Module Exam)"
LABEL = {"addition": "ADDITION", "pearl": "CLINICAL PEARL", "discrepancy": "DISCREPANCY · REVIEW"}


def inline(s):
    s = html.escape(s, quote=False)
    s = s.replace("⁺", "<sup>+</sup>").replace("⁻", "<sup>−</sup>")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def parse(text):
    chapters, ch, item, topic = [], None, None, None
    for raw in text.splitlines():
        line = raw.rstrip()
        if item is not None:
            if line.strip() == ":::":
                ch["blocks"].append(item); item = None
            else:
                item["lines"].append(line)
            continue
        if line.startswith("# "):
            parts = [p.strip() for p in line[2:].split("|")]
            kv = dict(p.split("=", 1) for p in parts[2:])
            ch = {"num": int(parts[0]), "title": parts[1], "main": kv["main"],
                  "subjects": kv.get("subjects", ""), "notes": [], "blocks": []}
            chapters.append(ch)
        elif line.startswith("## "):
            parts = [p.strip() for p in line[3:].split("|")]
            ch["blocks"].append({"type": "topic", "title": parts[0], "where": parts[1] if len(parts) > 1 else ""})
        elif line.startswith("> "):
            ch["notes"].append(line[2:])
        elif line.startswith("::: "):
            parts = [p.strip() for p in line[4:].split("|")]
            kind, iid = parts[0].split()
            kv = dict(p.split("=", 1) for p in parts[2:])
            assert kind in LABEL, kind
            item = {"type": "item", "kind": kind, "id": iid, "title": parts[1], "lines": [], **kv}
        elif line.strip():
            raise SystemExit(f"unparsed line outside block: {line!r}")
    return chapters


def body(lines, kind):
    out, para, ul, table, caption = [], [], [], [], None
    cmp_rows = []

    def flush():
        nonlocal para, ul, table, caption
        if para: out.append(f"<p>{inline(' '.join(para))}</p>"); para = []
        if ul: out.append("<ul>" + "".join(ul) + "</ul>"); ul = []
        if table:
            head, rows = table[0], table[1:]
            t = ['<table class="dt">']
            if caption: t.append(f"<caption>{inline(caption)}</caption>")
            t.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>")
            for r in rows: t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>"); out.append("".join(t)); table = []; caption = None

    for l in lines:
        s = l.strip()
        if not s: flush(); continue
        if kind == "discrepancy" and re.match(r"^(Main book|IM|Teaching note):", s):
            flush(); k, v = s.split(":", 1); cmp_rows.append((k, v.strip())); continue
        if s.startswith("Table:"): flush(); caption = s[6:].strip(); continue
        if s.startswith("|"):
            if para or ul:
                p2, u2 = para, ul; para, ul = [], []
                if p2: out.append(f"<p>{inline(' '.join(p2))}</p>")
                if u2: out.append("<ul>" + "".join(u2) + "</ul>")
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells): continue
            table.append(cells); continue
        if table: flush()
        if l.startswith("  - "): ul.append(f'<li class="l2">{inline(s[2:])}</li>'); continue
        if s.startswith("- "):
            if para: out.append(f"<p>{inline(' '.join(para))}</p>"); para = []
            ul.append(f"<li>{inline(s[2:])}</li>"); continue
        if ul: out.append("<ul>" + "".join(ul) + "</ul>"); ul = []
        para.append(s)
    flush()
    if cmp_rows:
        names = {"Main book": "Main book", "IM": "GIT Internal Med", "Teaching note": "For review"}
        out.append('<table class="cmp">' + "".join(f"<tr><th>{names[k]}</th><td>{inline(v)}</td></tr>" for k, v in cmp_rows) + "</table>")
    return "\n".join(out)


def im_ref(p):
    return ("IM p. " if re.fullmatch(r"\d+", p) else "IM pp. ") + p


def main_ref(p):
    return ("Main p. " if re.fullmatch(r"\d+", p) else "Main pp. ") + p


def render_html(chapters):
    counts = {c["num"]: sum(1 for b in c["blocks"] if b["type"] == "item") for c in chapters}
    kinds = {}
    for c in chapters:
        for b in c["blocks"]:
            if b["type"] == "item": kinds[b["kind"]] = kinds.get(b["kind"], 0) + 1
    h = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(TITLE)}</title>',
         '<link rel="stylesheet" href="../style.css"></head><body>']
    logo = (ROOT / "brand" / "ymnotes-logo.svg").read_text()
    cover = [h[0], h[1]]
    cover.append(f'''<section class="cover" id="cover"><div class="cover__rule"></div>
<div class="cover__logo">{logo}</div>
<div class="cover__eyebrow">YMNOTES MEDICAL · DIGESTIVE SYSTEM</div>
<div class="cover__title">Additional Teaching Points</div>
<div class="cover__sub">A chapter-by-chapter companion to the Digestive System study edition</div>
<div class="cover__part">Part 1 · Before the Mid-Module Exam · Chapters 1–15</div>
<div class="cover__bar"></div>
<div class="cover__meta">Contains only the points in <b>GIT Internal Med</b> that are not already taught in the corresponding
pages of the <b>YMnotes Digestive System</b> study edition (Version 3), book pages 1–197. Teach each chapter from the main book first, then use this companion for its additions.</div>
<div class="cover__foot">YMNOTES MEDICAL · DIGESTIVE SYSTEM · VERSION 3 COMPANION</div></section></body></html>''')

    # how to use
    h.append(f'''<section class="front howto" id="how-to-use"><div class="eyebrow">BEFORE YOU START</div>
<h1 class="front__title">How to use this companion</h1><div class="front__rule"></div>
<p class="lead">This is not a summary. Every entry is a point that the GIT Internal Med notes add to what the main book already teaches.
Points that repeat or reword the main book have been left out on purpose.</p>
<h2>Three kinds of entry</h2>
<div class="legend">
<div class="item"><div class="item__label">ADDITION</div><div class="item__body">A fact, mechanism, investigation detail or management point missing from the main book. Green rail, diamond marker.</div></div>
<div class="item pearl"><div class="item__label">CLINICAL PEARL</div><div class="item__body">A short, high-yield clinical clue or distinction. Blue double rail, round marker.</div></div>
<div class="item discrepancy"><div class="item__label">DISCREPANCY · REVIEW</div><div class="item__body">The two sources disagree. Both versions are shown with their page numbers, and neither is presented as correct. Check these before teaching. Red heavy rail, triangle marker.</div></div>
</div>
<h2>Reading the page references</h2>
<table class="reftable"><tr><th>Reference</th><th>Means</th><th>PDF viewer page</th></tr>
<tr><td><b>Main p. 14</b></td><td>The page number printed on the YMnotes Digestive System book. Teach the entry at this point.</td><td>Printed page + 3 (p. 14 → PDF page 17)</td></tr>
<tr><td><b>IM p. 12</b></td><td>The page number printed on GIT Internal Med, where the point comes from.</td><td>The same as the printed page</td></tr></table>
<h2>Scope</h2>
<ul><li>Chapters 1–15 of the main book, in its own order, up to printed page 197 (the last page of the supplied file). Chapter 15 therefore covers pages 195–197 only.</li>
<li>Items are grouped under the main-book section where they should be taught, not in the order of the Internal Medicine notes.</li>
<li>Chapters for which the Internal Medicine notes add nothing worthwhile still appear, with a short note, so the sequence matches the main book.</li></ul>
</section>''')

    # contents
    h.append('<section class="front" id="contents"><div class="eyebrow">CONTENTS</div><h1 class="front__title">Chapters</h1><div class="front__rule"></div>')
    h.append('<div class="toc__head"><span>NO.</span><span>MAIN-BOOK CHAPTER · SUBJECTS</span><span>ENTRIES</span><span>PAGE</span></div><ul class="toc">')
    for c in chapters:
        n = counts[c["num"]]
        cls = "" if n else ' class="is-empty"'
        cnt = f"<b>{n}</b> {'entry' if n == 1 else 'entries'}" if n else "none"
        h.append(f'<li{cls}><a href="#ch{c["num"]:02d}"><span class="toc__num">{c["num"]:02d}</span>'
                 f'<span><span class="toc__title">{html.escape(c["title"])}</span><span class="toc__subject">{html.escape(c["subjects"])} · main book from p. {c["main"]}</span></span>'
                 f'<span class="toc__count">{cnt}</span><span class="toc__folio" data-folio="ch{c["num"]:02d}">00</span></a></li>')
    total = sum(counts.values())
    h.append(f'</ul><p class="toc-note">{total} entries in total: {kinds.get("addition",0)} additions, {kinds.get("pearl",0)} clinical pearls, {kinds.get("discrepancy",0)} discrepancies for review. Tap a chapter to jump to it.</p></section>')

    for c in chapters:
        n = counts[c["num"]]
        cls = "chapter" + ("" if n else " is-empty")
        h.append(f'<section class="{cls}" id="ch{c["num"]:02d}"><div class="chapter__head"><div class="chapter__chip">{c["num"]:02d}</div>'
                 f'<div><div class="chapter__eyebrow">CHAPTER {c["num"]:02d} · TEACH AFTER MAIN BOOK FROM P. {c["main"]}</div>'
                 f'<h2 class="chapter__title">{html.escape(c["title"])}</h2></div></div><div class="chapter__rule"></div>'
                 f'<div class="chapter__meta"><span>{html.escape(c["subjects"])}</span><span><b>{n}</b> {"entry" if n == 1 else "entries"}</span></div>')
        for note in c["notes"]:
            h.append(f'<div class="none">{inline(note)}</div>')
        for b in c["blocks"]:
            if b["type"] == "topic":
                where = f'<small>{html.escape(b["where"])}</small>' if b["where"] else ""
                h.append(f'<h3 class="topic">{html.escape(b["title"])}{where}</h3>')
                continue
            text = body(b["lines"], b["kind"])
            long = " is-long" if len(text) > 1800 or "<table" in text and len(text) > 1300 else ""
            sec = f' · {html.escape(b["section"])}' if b.get("section") else ""
            h.append(f'<article class="item {b["kind"]}{long}" id="{b["id"]}"><div class="item__label">{LABEL[b["kind"]]}</div>'
                     f'<h4 class="item__title">{inline(b["title"])}</h4><div class="item__body">{text}</div>'
                     f'<div class="item__refs"><span>Teach with <b>{main_ref(b["main"])}</b>{sec}</span>'
                     f'<span>Source <b>{im_ref(b["im"])}</b></span><span class="item__id">{b["id"]}</span></div></article>')
        h.append("</section>")
    h.append('<p class="endnote">Source for every entry: GIT Internal Med (page shown on each entry). Compared against the YMnotes Digestive System study edition, Version 3, printed pages 1–197. '
             'Entries marked Discrepancy · Review are shown for the teacher to decide and are not resolved here.</p>')
    h.append("</body></html>")
    return "\n".join(h), "\n".join(cover)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    chapters = parse(SRC.read_text())
    assert [c["num"] for c in chapters] == list(range(1, 16)), [c["num"] for c in chapters]
    body_html, cover_html = render_html(chapters)
    folios = json.loads((OUT / "folios.json").read_text()) if (OUT / "folios.json").exists() else {}
    for k, v in folios.items():
        body_html = body_html.replace(f'data-folio="{k}">00<', f'data-folio="{k}">{v}<')
    (OUT / "handout.html").write_text(body_html)
    (OUT / "cover.html").write_text(cover_html)
    json.dump([{"num": c["num"], "title": c["title"], "main": c["main"], "subjects": c["subjects"],
                "items": [{"id": b["id"], "kind": b["kind"], "title": b["title"], "main": b["main"], "im": b["im"]}
                          for b in c["blocks"] if b["type"] == "item"],
                "topics": [b["title"] + (" " + b["where"] if b["where"] else "") for b in c["blocks"] if b["type"] == "topic"],
                "item_ids_first": next((b["id"] for b in c["blocks"] if b["type"] == "item"), c["title"])} for c in chapters],
              open(OUT / "structure.json", "w"), indent=1)
    print("html written", sum(len(c["blocks"]) for c in chapters), "blocks")
