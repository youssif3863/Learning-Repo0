# -*- coding: utf-8 -*-
"""Stage 2 · Version 2 — the teacher's phone PDF: answers + EN/AR explanations + hyperlinked, highlighted book."""
import html, json, os, re, subprocess
import pymupdf
import stamp
from book import compress, chapter_label
from deck import BRAND

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = "file://" + os.path.join(BRAND, "fonts") + "/"
URI = "https://uqc.invalid/"
TOP_MARGIN = 66.0   # must equal the @page top margin below: Chromium anchor positions exclude it
esc = html.escape

ICON_CHECK = '<svg viewBox="0 0 12 12" width="10" height="10"><path d="M2 6.5l2.6 2.6L10 3" fill="none" stroke="#1A9A4A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_X = '<svg viewBox="0 0 12 12" width="8" height="8"><path d="M3 3l6 6M9 3l-6 6" fill="none" stroke="#B3483C" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_OPEN = '<svg viewBox="0 0 12 12" width="8" height="8"><path d="M3 9l6-6M4 3h5v5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_STAR = '<svg viewBox="0 0 12 12" width="9" height="9"><path d="M6 .8l1.6 3.4 3.7.4-2.8 2.5.8 3.7L6 8.9 2.7 10.8l.8-3.7L.7 4.6l3.7-.4z" fill="#E3A400"/></svg>'

CSS = """
@font-face{font-family:'Inter';font-weight:400;src:url(%(f)sinter-latin-400-normal.woff2)}
@font-face{font-family:'Inter';font-weight:500;src:url(%(f)sinter-latin-500-normal.woff2)}
@font-face{font-family:'Inter';font-weight:600;src:url(%(f)sinter-latin-600-normal.woff2)}
@font-face{font-family:'Inter';font-weight:700;src:url(%(f)sinter-latin-700-normal.woff2)}
@font-face{font-family:'Archivo';font-weight:600;src:url(%(f)sarchivo-latin-600-normal.woff2)}
@font-face{font-family:'Archivo';font-weight:700;src:url(%(f)sarchivo-latin-700-normal.woff2)}
@font-face{font-family:'Source Serif 4';font-weight:400;src:url(%(f)ssource-serif-4-latin-400-normal.woff2)}
@font-face{font-family:'Source Serif 4';font-weight:600;src:url(%(f)ssource-serif-4-latin-600-normal.woff2)}
@font-face{font-family:'Noto Sans Arabic';font-weight:400;src:url(%(f)snoto-sans-arabic-arabic-400-normal.woff2)}
@font-face{font-family:'Noto Sans Arabic';font-weight:600;src:url(%(f)snoto-sans-arabic-arabic-600-normal.woff2)}
@font-face{font-family:'Noto Sans Arabic';font-weight:700;src:url(%(f)snoto-sans-arabic-arabic-700-normal.woff2)}
@page{size:595.28pt 841.89pt;margin:66pt 32pt 50pt 32pt}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
body{font:400 9.6pt/1.45 'Inter','Noto Sans Arabic',sans-serif;color:#15201A}
a{color:inherit;text-decoration:none}
.ar{direction:rtl;text-align:right;font-family:'Noto Sans Arabic','Inter',sans-serif;unicode-bidi:isolate}
.gh{display:flex;align-items:center;height:24pt;margin:2pt 0 9pt;break-after:avoid}
.gh .t{font:600 15.6pt/1 'Archivo','Inter',sans-serif;color:#1A5B31;margin-right:12pt;white-space:nowrap}
.gh .rule{flex:1;border-top:.6pt solid #7FAE92}
.part{break-before:page;margin:0 0 12pt;padding:12pt 14pt;border-radius:9pt;background:#1A5B31;color:#fff;break-after:avoid}
.part .a{font:700 8pt 'Inter';letter-spacing:.12em;text-transform:uppercase;opacity:.8}
.part .b{font:600 18pt/1.15 'Archivo';margin-top:3pt}
.part .c{font:600 13pt/1.4 'Noto Sans Arabic';direction:rtl;text-align:right;margin-top:-18pt}
.card{margin:0 0 11pt;padding:9pt 11pt 8pt;border:.6pt solid #D4DDD7;border-radius:8pt;break-inside:avoid;background:#fff}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:5pt 7pt;margin-bottom:6pt}
.pos{font:700 8.4pt/1 'Inter';color:#1A5B31;background:#E8F1EB;border-radius:4pt;padding:3pt 6pt}
.tag{font:600 7.2pt/1 'Inter';letter-spacing:.05em;text-transform:uppercase;border-radius:10pt;padding:3.4pt 8pt}
.tag i{font:600 8pt/1 'Noto Sans Arabic';font-style:normal;letter-spacing:0;text-transform:none;margin-left:5pt}
.chap{font:400 7.8pt/1.3 'Inter';color:#66756C}
.pass{margin:0 0 6pt;padding:5pt 9pt;background:#F6F9F7;border-left:2pt solid #7FAE92;font:400 9.4pt/1.4 'Source Serif 4','DejaVu Serif',serif;color:#22302A;white-space:pre-wrap}
.passref{font:500 8pt 'Inter';color:#66756C;margin:0 0 5pt}
.qtext{font:400 11.5pt/1.38 'Source Serif 4','DejaVu Serif',serif;color:#15201A;margin:2pt 0 6pt;padding-left:9pt;position:relative;white-space:pre-wrap}
.qtext::before{content:"";position:absolute;left:0;top:1pt;bottom:1pt;width:1.7pt;background:#DCEAE0}
.fig{margin:0 0 6pt 9pt}.fig img{max-width:100%;max-height:150pt}
.wo{margin:0 0 1pt}
.o{display:grid;grid-template-columns:19pt 1fr;align-items:baseline;padding:1.6pt 4pt 0 0}
.o .l{font:500 9.6pt/1.4 'Inter';color:#34423A}
.o .x{font:400 10.6pt/1.35 'Source Serif 4','DejaVu Serif',serif;color:#2A3731;white-space:pre-wrap}
.rw{display:flex;justify-content:space-between;gap:10pt;margin:1pt 0 3.5pt 19pt;font:400 8.5pt/1.35 'Inter';color:#55615A}
.rw .en{flex:1 1 48%;padding-left:12pt;position:relative}
.rw .en svg{position:absolute;left:1pt;top:2.2pt}
.rw .ar{flex:1 1 48%;font-size:9pt;line-height:1.55}
a.o.right{display:grid;grid-template-columns:19pt 1fr auto;align-items:center;background:#E3F4E9;border-left:3pt solid #1A9A4A;border-radius:5pt;padding:5.5pt 8pt 5.5pt 6pt;margin:3pt 0 4pt}
a.o.right .l{color:#1A5B31;font-weight:700}
a.o.right .x{font-weight:600;color:#0E3B20}
.bk{display:inline-flex;align-items:center;gap:3pt;font:600 7.8pt/1 'Inter';color:#fff;background:#1A5B31;border-radius:10pt;padding:3.6pt 8pt;margin-left:8pt;white-space:nowrap}
.bk.near{background:#4C7A5E}
.bk.none{background:#EEF1EF;color:#66756C;font-weight:500}
.why{margin:5pt 0 0;padding:6pt 9pt;background:#F6F9F7;border-radius:6pt}
.why .en{font:400 9.4pt/1.45 'Inter';color:#22302A}
.why .ar{font-size:10pt;line-height:1.65;color:#22302A;margin-top:3pt}
.why b{font-weight:700;color:#1A5B31}
.pearl{margin:5pt 0 0;padding:6pt 9pt;background:#FFF6DC;border-left:3pt solid #E3A400;border-radius:5pt}
.pearl .en{font:400 9.1pt/1.42 'Inter';color:#4A3A07}
.pearl .ar{font-size:9.6pt;line-height:1.6;color:#4A3A07;margin-top:2pt}
.pearl b{font-weight:700}
.note{margin:5pt 0 0;padding:5pt 9pt;background:#FDECEA;border-left:3pt solid #D9534F;border-radius:5pt}
.note .en{font:500 8.8pt/1.4 'Inter';color:#7A2A24}
.note .ar{font-size:9.3pt;line-height:1.55;color:#7A2A24;margin-top:2pt}
.cover h1{font:700 27pt/1.08 'Archivo','Inter',sans-serif;color:#1A5B31;margin:4pt 0 4pt}
.cover .sub{font:500 11pt/1.4 'Inter';color:#34423A}
.cover .sub-ar{font:600 14pt/1.5 'Noto Sans Arabic';direction:rtl;text-align:right;color:#1A5B31;margin-top:2pt}
.cover h2{font:600 11pt/1 'Archivo';color:#1A5B31;margin:15pt 0 6pt;padding-bottom:4pt;border-bottom:.6pt solid #7FAE92}
.how{display:grid;grid-template-columns:1fr 1fr;gap:10pt}
.how ul{margin:0;padding-left:12pt;font:400 8.9pt/1.45 'Inter'}.how li{margin:0 0 3pt}
.how .ar ul{padding-left:0;padding-right:12pt;font:400 9.4pt/1.6 'Noto Sans Arabic'}
.legend{display:flex;flex-wrap:wrap;gap:6pt;margin-top:4pt}
.idx{display:flex;flex-wrap:wrap;gap:4pt}
.idx a{font:600 8.6pt/1 'Inter';color:#1A5B31;background:#E8F1EB;border-radius:4pt;padding:4.5pt 7pt;min-width:25pt;text-align:center}
.idxh{font:600 8.2pt/1.2 'Inter';color:#34423A;margin:7pt 0 3pt}
.btn{display:inline-block;font:600 9pt/1 'Inter';color:#fff;background:#1A5B31;border-radius:6pt;padding:7pt 11pt;margin:6pt 6pt 0 0}
.notes h3{font:600 11pt/1.2 'Archivo';color:#1A5B31;margin:12pt 0 5pt}
.nl{margin:0 0 5pt;padding:5pt 8pt;border:.6pt solid #E1E7E3;border-radius:5pt;break-inside:avoid;font:400 8.7pt/1.4 'Inter'}
.nl b{font-weight:700;color:#1A5B31}
.nl .ar{font-size:9.2pt;line-height:1.55;margin-top:1pt}
.nl .q{color:#55615A}
"""


def tag_css(deck):
    return "".join(f".t-{k}{{color:{v['fg']};background:{v['bg']}}}" for k, v in deck["tags"].items())


def book_chip(it, with_book):
    if with_book and it["pg"]:
        cls = "bk" if it["exact"] else "bk near"
        lab = f'Book p. {esc(it["pg"])}' if it["exact"] else f'Nearest: p. {esc(it["pg"])}'
        return f'<span class="{cls}">{lab} {ICON_OPEN}</span>'
    return '<span class="bk none">Not in the supplied book</span>'


def card_html(it, with_book, prev):
    qid = it["id"]
    h = [f'<article class="card" id="q-{qid}"><div class="meta"><a class="pos" href="#q-{qid}">{it["group"]}·{it["pos"]}</a>',
         f'<span class="tag t-{it["tag"]}">{esc(it["tagname"])}<i>{it["tagname_ar"]}</i></span>',
         f'<span class="chap">{esc(it["chapter_line"])}</span></div>']
    if it["passage"]:
        if prev and prev["group_src"] == it["group_src"] and prev["passage"]:
            h.append('<div class="passref">Same passage as the previous question.</div>')
        else:
            h.append(f'<div class="pass">{esc(it["passage"])}</div>')
    h.append(f'<div class="qtext">{esc(it["q"])}</div>')
    for im in it["images"]:
        h.append(f'<div class="fig"><img src="file://{esc(im)}"></div>' if os.path.isfile(im) else '<div class="fig">[figure missing]</div>')
    for k, o in zip(it["labels"], it["opts"]):
        if k in it["ans"]:
            h.append(f'<a class="o right" href="{URI}q{qid}"><span class="l">{k}.</span><span class="x">{esc(o)}</span>'
                     f'<span>{ICON_CHECK} {book_chip(it, with_book)}</span></a>')
        else:
            en, ar = it["wrong"][k]
            h.append(f'<div class="wo"><div class="o"><span class="l">{k}.</span><span class="x">{esc(o)}</span></div>'
                     f'<div class="rw"><span class="en">{ICON_X}{esc(en)}</span><span class="ar" dir="rtl">{esc(ar)}</span></div></div>')
    en, ar = it["why"]
    h.append(f'<div class="why"><div class="en"><b>Why:</b> {esc(en)}</div><div class="ar" dir="rtl"><b>لماذا:</b> {esc(ar)}</div></div>')
    if it["pearl"]:
        h.append(f'<div class="pearl"><div class="en">{ICON_STAR} <b>Tell the students:</b> {esc(it["pearl"][0])}</div>'
                 f'<div class="ar" dir="rtl"><b>قل للطلاب:</b> {esc(it["pearl"][1])}</div></div>')
    if it["note"]:
        h.append(f'<div class="note"><div class="en"><b>Question note:</b> {esc(it["note"][0])}</div>'
                 f'<div class="ar" dir="rtl"><b>ملاحظة على السؤال:</b> {esc(it["note"][1])}</div></div>')
    h.append('</article>')
    return "".join(h)


def cover_html(groups, deck, with_book):
    parts = {}
    for g in groups:
        parts.setdefault(g["part_index"], []).append(g)
    c = [f'<section class="cover"><div style="font:700 8pt Inter;letter-spacing:.14em;color:#66756C">{esc(deck["brand"].upper())} · {esc(deck["module_label"])}</div>',
         f'<h1>{esc(deck["cover_title"]).replace(" &amp; ", "<br>&amp; ", 1)}</h1>',
         '<div class="sub">Version 2 · for the teacher' + (' · every answer links to its line in the book' if with_book else '') + '</div>',
         '<div class="sub-ar">مفتاح الإجابات ودليل المذاكرة — النسخة الثانية للمدرّس</div>',
         '<h2>How to use · طريقة الاستخدام</h2><div class="how"><div><ul>']
    if with_book:
        c += ['<li><b>Green row = correct answer.</b> Tap it: the book opens at the exact line, highlighted in green.</li>',
              '<li>At the bottom of that book page tap the green <b>&lt; A·1</b> chip to return to the question.</li>']
    else:
        c += ['<li><b>Green row = correct answer.</b></li>']
    c += ['<li>Each card: why it is right, why each other option is wrong, and a one-line <b>Tell the students</b> pearl.</li>',
          '<li>Every card shows its subject tag and the book chapter.</li></ul></div><div class="ar" dir="rtl"><ul>']
    if with_book:
        c += ['<li><b>الصف الأخضر = الإجابة الصحيحة.</b> اضغط عليه فيفتح الكتاب عند السطر نفسه مظللاً بالأخضر.</li>',
              '<li>أسفل صفحة الكتاب اضغط الشريحة الخضراء <b>A·1 &gt;</b> للرجوع إلى السؤال.</li>']
    else:
        c += ['<li><b>الصف الأخضر = الإجابة الصحيحة.</b></li>']
    c += ['<li>في كل سؤال: لماذا صحيحة، ولماذا باقي الاختيارات خطأ، ونقطة <b>قل للطلاب</b>.</li>',
          '<li>كل سؤال عليه التخصص وفصل الكتاب.</li></ul></div></div><div class="legend">']
    for k, v in deck["tags"].items():
        c.append(f'<span class="tag t-{k}">{esc(v["en"])}<i>{v["ar"]}</i></span>')
    c.append('</div><h2>Group index · فهرس المجموعات</h2>')
    for pi, part in enumerate(deck["parts"]):
        if pi not in parts:
            continue
        c.append(f'<div class="idxh">Part {pi + 1} — {esc(part["title"])} · {part.get("title_ar", "")}</div><div class="idx">')
        c += [f'<a href="#g-{g["letter"]}">{g["letter"]}</a>' for g in parts[pi]]
        c.append('</div>')
    c.append('<div>' + (f'<a class="btn" href="{URI}book">Open the book ↗</a>' if with_book else '') + '<a class="btn" href="#notes" style="background:#8A3B12">Teacher notes ↗</a></div></section>')
    return "".join(c)


def notes_html(groups, deck, with_book, compressed):
    items = [it for g in groups for it in g["items"]]
    flagged = [it for it in items if it["note"]]
    nobook = [it for it in items if not it["pg"] and not it["note"]]
    near = [it for it in items if it["pg"] and not it["exact"]]

    def line(it, extra=""):
        q = it["q"] if len(it["q"]) < 90 else it["q"][:87] + "…"
        return f'<div class="nl"><a href="#q-{it["id"]}"><b>{it["group"]}·{it["pos"]}</b> <span class="q">{esc(q)}</span></a>{extra}</div>'
    h = ['<section class="notes" id="notes" style="break-before:page"><div class="gh"><span class="t">Teacher notes</span><span class="rule"></span></div>',
         '<h3>Questions to double-check · أسئلة تحتاج مراجعتك</h3>']
    h += [line(it, f'<div>{esc(it["note"][0])}</div><div class="ar" dir="rtl">{esc(it["note"][1])}</div>') for it in flagged] or ['<div class="nl">None flagged.</div>']
    if with_book:
        h.append('<h3>Not in the supplied book · غير موجودة في الكتاب</h3><div class="nl" style="border:none;padding:0 0 4pt">'
                 'These were answered from standard references because the supplied book does not cover them, so they have no link. '
                 '· أُجيبت من المراجع القياسية لأن الكتاب المرفق لا يغطيها، فلا رابط لها.</div>')
        h += [line(it) for it in nobook] or ['<div class="nl">None.</div>']
        h.append('<h3>Nearest page only · أقرب صفحة فقط</h3><div class="nl" style="border:none;padding:0 0 4pt">'
                 'The exact sentence is not printed in the book (or sits inside a figure), so the link opens the closest topic page without a highlight. '
                 '· الجملة نفسها غير مكتوبة بالكتاب فالرابط يفتح أقرب صفحة بدون تظليل.</div>')
        h += [line(it) for it in near] or ['<div class="nl">None.</div>']
    h.append('<h3>How this file was organised · طريقة التنظيم</h3>')
    parts = "; ".join(f'Part {i + 1} {esc(p["title"])}' for i, p in enumerate(deck["parts"]))
    h.append(f'<div class="nl">Questions keep the shuffled order of the Stage 1 file and are grouped 3-4-5 inside each part ({parts}).'
             + (' Book images were compressed to about 150 dpi to keep the file phone-friendly; text stays sharp.' if compressed else '')
             + '<div class="ar" dir="rtl">تحتفظ الأسئلة بترتيب ملف المرحلة الأولى وتُجمّع 3-4-5 داخل كل جزء.</div></div></section>')
    return "".join(h)


def answers_html(groups, deck, with_book, compressed):
    body = [cover_html(groups, deck, with_book)]
    cur, prev = None, None
    for g in groups:
        if g["part_index"] != cur:
            cur = g["part_index"]
            body.append(f'<div class="part"><div class="a">Part {cur + 1}</div><div class="b">{esc(g["part_title"])}</div><div class="c">{g["part_title_ar"]}</div></div>')
        body.append(f'<div class="gh" id="g-{g["letter"]}"><span class="t">Group {g["letter"]}</span><span class="rule"></span></div>')
        for it in g["items"]:
            body.append(card_html(it, with_book, prev))
            prev = it
    body.append(notes_html(groups, deck, with_book, compressed))
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{esc(deck["module_label"])} answer key</title>'
            f'<style>{CSS.replace("%(f)s", FONTS)}{tag_css(deck)}</style></head><body>{"".join(body)}</body></html>')


# ------------------------------------------------------------------ post-processing
def locate(bdoc, bk, it):
    """-> (page_index0, quads, y_top) or None."""
    if not it["pg"]:
        return None
    pdf = bk.pdf_of(it["pg"])
    if not pdf:
        return None
    quads = []
    if it["anchor"]:
        hits = bdoc[pdf - 1].search_for(it["anchor"], quads=True)
        if hits:
            quads = hits if len(hits) <= 3 else hits[:1]
    return pdf - 1, quads, (min(q.rect.y0 for q in quads) if quads else None)


def build(groups, deck, work, out_pdf, bk, with_book=True):
    os.makedirs(work, exist_ok=True)
    book_path = bk.meta["book"]
    compressed = False
    if with_book:
        mode = deck.get("compress_book", "auto")
        if mode is True or (mode == "auto" and bk.meta["size_mb"] > 60):
            small = os.path.join(work, "book_small.pdf")
            if not os.path.exists(small):
                compress(book_path, small)
            book_path, compressed = small, True
    hp = os.path.join(work, "v2.html")
    open(hp, "w", encoding="utf-8").write(answers_html(groups, deck, with_book, compressed))
    raw = os.path.join(work, "v2_raw.pdf")
    r = subprocess.run(["node", os.path.join(HERE, "render.js"), hp, raw], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("render failed: " + r.stderr[-600:])
    final = pymupdf.open(raw)
    n_ans = len(final)
    names = final.resolve_names()

    def dest(name):
        d = names[name]
        H = final[d["page"]].rect.height
        y_up = d["to"][1] if isinstance(d["to"], (tuple, list)) else d["to"].y
        return d["page"], max(0.0, H - y_up + TOP_MARGIN)
    items = [it for g in groups for it in g["items"]]
    card_dest = {it["id"]: dest(f'q-{it["id"]}') for it in items}
    group_dest = {g["letter"]: dest(f'g-{g["letter"]}') for g in groups}
    notes_dest = dest("notes")
    stamp.stamp(final, {i: str(i + 1) for i in range(1, n_ans)}, right_label=f'{deck["module_label"]}  ·  ANSWER KEY', first=0, count=n_ans)

    report = {"answer_pages": n_ans, "compressed_book": compressed, "with_book": with_book}
    loc, bdoc = {}, None
    if with_book:
        bdoc = pymupdf.open(book_path)
        loc = {it["id"]: locate(bdoc, bk, it) for it in items}
        final.insert_pdf(bdoc, links=True, annots=True)
    report["book_start"] = n_ans
    # 1) answer rows -> book (explicit GoTo, y measured from the top of the target page)
    n_goto = n_none = 0
    for pno in range(n_ans):
        pg = final[pno]
        for lk in pg.get_links():
            u = lk.get("uri", "") or ""
            if not u.startswith(URI):
                continue
            rect = lk["from"]; tail = u[len(URI):]
            pg.delete_link(lk)
            if tail == "book":
                pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": rect, "page": n_ans, "to": pymupdf.Point(0, 0), "zoom": 0}); continue
            L = loc.get(tail[1:])
            if L:
                pno_b, quads, y = L
                pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": rect, "page": n_ans + pno_b, "to": pymupdf.Point(0, max(0, (y or 0) - 70)), "zoom": 0}); n_goto += 1
            else:
                n_none += 1
    # 2) in-document links: Chromium named destinations -> explicit page destinations (every viewer)
    n_named = 0
    for pno in range(n_ans):
        pg = final[pno]
        for lk in pg.get_links():
            if lk["kind"] == pymupdf.LINK_NAMED and lk.get("nameddest") in names:
                tp = lk["page"]; H = final[tp].rect.height
                rect = lk["from"]
                pg.delete_link(lk)
                pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": rect, "page": tp, "to": pymupdf.Point(0, max(0.0, H - lk["to"].y + TOP_MARGIN - 8)), "zoom": 0}); n_named += 1
    # 3) highlights + back chips on the book pages
    n_hl = n_pages = 0
    if with_book:
        by_page = {}
        for it in items:
            if loc[it["id"]]:
                by_page.setdefault(loc[it["id"]][0], []).append(it)
        font = pymupdf.Font(fontfile=stamp.F_SEMI)
        for pno_b, lst in sorted(by_page.items()):
            pg = final[n_ans + pno_b]; n_pages += 1
            x, y0 = 36.0, 818.5
            for it in lst:
                _, quads, _y = loc[it["id"]]
                if it["exact"] and quads:
                    an = pg.add_highlight_annot(quads)
                    an.set_colors(stroke=(0.25, 0.95, 0.45)); an.set_opacity(0.55); an.update(); n_hl += 1
                lab = f'{it["group"]}·{it["pos"]}'
                w = font.text_length(lab, fontsize=7.4) + 16
                if x + w > 520:
                    x, y0 = 36.0, y0 - 14.5
                rect = pymupdf.Rect(x, y0, x + w, y0 + 12.5)
                pg.draw_rect(rect, color=None, fill=stamp.GREEN, radius=0.3)
                pg.draw_polyline([(x + 6.6, y0 + 3.4), (x + 6.6, y0 + 9.1), (x + 3.2, y0 + 6.25)], color=None, fill=(1, 1, 1), closePath=True)
                pg.insert_text((x + 9.6, y0 + 9.1), lab, fontfile=stamp.F_SEMI, fontname="InterS", fontsize=7.4, color=(1, 1, 1))
                cp, cy = card_dest[it["id"]]
                pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": rect, "page": cp, "to": pymupdf.Point(0, max(0.0, cy - 10)), "zoom": 0})
                x += w + 3
    # 4) bookmarks
    toc = [[1, "Cover & group index", 1]]
    for pi, part in enumerate(deck["parts"]):
        gs = [g for g in groups if g["part_index"] == pi]
        if not gs:
            continue
        toc.append([1, f'Part {pi + 1} — {part["title"]}', group_dest[gs[0]["letter"]][0] + 1])
        toc += [[2, f'Group {g["letter"]}', group_dest[g["letter"]][0] + 1] for g in gs]
    toc.append([1, "Teacher notes", notes_dest[0] + 1])
    if with_book:
        toc.append([1, f'BOOK — {deck.get("book_title") or "reference"} (hyperlinked)', n_ans + 1])
        toc += [[2, chapter_label(c) or c["title"], n_ans + c["pdf_page"]] for c in bk.chapters]
    final.set_toc(toc)
    final.set_metadata({"title": f'{deck["brand"]} — {deck["module_label"]} answer key' + (" + book (Version 2)" if with_book else " (Version 2)"), "author": deck["brand"]})
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    final.save(out_pdf, garbage=4, deflate=True, clean=True, use_objstms=True)
    report.update({"pages": len(final), "links_to_book": n_goto, "answers_without_book": n_none, "named_links_converted": n_named,
                   "highlights": n_hl, "book_pages_referenced": n_pages, "size_mb": round(os.path.getsize(out_pdf) / 1048576, 1)})
    return report
