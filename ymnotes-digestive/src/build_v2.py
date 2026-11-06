# -*- coding: utf-8 -*-
"""Version 2 — the teacher's phone version: answers + EN/AR explanations + hyperlinked book."""
import os, sys, html, subprocess, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model, stamp
import pymupdf

ROOT = model.ROOT
WORK = os.environ.get("YM_WORK", "/tmp/ymnotes_work")
BOOK = os.environ.get("YM_BOOK", os.path.join(WORK, "book_small.pdf"))
OUT = os.path.join(ROOT, "output", "YMnotes_Digestive_Mid_Module_V2_Answers_with_Book.pdf")
OUT_NOBOOK = os.path.join(ROOT, "output", "YMnotes_Digestive_Mid_Module_V2_Answer_Key_only.pdf")
FONTS = "file://" + os.path.join(ROOT, "assets", "fonts") + "/"
URI = "https://ymnotes.invalid/"
TOP_MARGIN = 66.0   # must equal the @page top margin: Chromium anchors exclude it
os.makedirs(WORK, exist_ok=True)
esc = html.escape

# ---------------------------------------------------------------- book page map
PM = json.load(open(os.path.join(ROOT, "data", "page_map.json")))
INV = {v: int(k) for k, v in PM.items() if v and v.isdigit() and int(k) < 447}

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
.gh .pt{font:600 7.6pt/1 'Inter';letter-spacing:.05em;text-transform:uppercase;color:#1A5B31;margin-left:10pt;white-space:nowrap}
.part{break-before:page;margin:0 0 12pt;padding:12pt 14pt;border-radius:9pt;background:#1A5B31;color:#fff;break-after:avoid}
.part .a{font:700 8pt 'Inter';letter-spacing:.12em;text-transform:uppercase;opacity:.8}
.part .b{font:600 18pt/1.15 'Archivo';margin-top:3pt}
.part .c{font:600 13pt/1.4 'Noto Sans Arabic';direction:rtl;text-align:right;margin-top:-18pt}
.card{margin:0 0 11pt;padding:9pt 11pt 8pt;border:.6pt solid #D4DDD7;border-radius:8pt;break-inside:avoid;background:#fff}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:5pt 7pt;margin-bottom:6pt}
.pos{font:700 8.4pt/1 'Inter';color:#1A5B31;background:#E8F1EB;border-radius:4pt;padding:3pt 6pt}
.tag{font:600 7.2pt/1 'Inter';letter-spacing:.05em;text-transform:uppercase;border-radius:10pt;padding:3.4pt 8pt}
.tag i{font:600 8pt/1 'Noto Sans Arabic';font-style:normal;letter-spacing:0;text-transform:none;margin-left:5pt}
.t-s{color:#8A3B12;background:#FCE9DA}.t-m{color:#1D4F91;background:#E3ECFA}.t-mi{color:#6B2A8F;background:#F0E5F8}
.t-pa{color:#7A5B00;background:#FBF0CC}.t-ph{color:#0B6B6B;background:#D9F1F0}
.chap{font:400 7.8pt/1.3 'Inter';color:#66756C}
.qtext{font:400 11.5pt/1.38 'Source Serif 4','DejaVu Serif',serif;color:#15201A;margin:2pt 0 6pt;padding-left:9pt;position:relative}
.qtext::before{content:"";position:absolute;left:0;top:1pt;bottom:1pt;width:1.7pt;background:#DCEAE0}
.wo{margin:0 0 1pt}
.o{display:grid;grid-template-columns:19pt 1fr;align-items:baseline;padding:1.6pt 4pt 0 0}
.o .l{font:500 9.6pt/1.4 'Inter';color:#34423A}
.o .x{font:400 10.6pt/1.35 'Source Serif 4','DejaVu Serif',serif;color:#2A3731}
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


def book_chip(it):
    if it["pg"]:
        cls = "bk" if it["exact"] else "bk near"
        lab = f'Book p. {esc(it["pg"])}' if it["exact"] else f'Nearest: p. {esc(it["pg"])}'
        return f'<span class="{cls}">{lab} {ICON_OPEN}</span>'
    if it["src"][0].startswith("Hernia book"):
        return '<span class="bk none">Hernia book — not in this file</span>'
    return '<span class="bk none">Not in the book</span>'


def card_html(it):
    qid = it["id"]
    pos = f'{it["group"]}·{it["pos"]}'
    h = [f'<article class="card" id="q-{qid}"><div class="meta"><a class="pos" href="#q-{qid}">{pos}</a>']
    h.append(f'<span class="tag {it["tagclass"]}">{esc(it["tag"])}<i>{it["tag_ar"]}</i></span>')
    h.append(f'<span class="chap">{" · ".join(esc(s) for s in it["src_clean"])}</span></div>')
    h.append(f'<div class="qtext">{esc(it["q"])}</div>')
    for k, o in zip("ABCDE", it["opts"]):
        if k == it["ans"]:
            inner = f'<span class="l">{k}.</span><span class="x">{esc(o)}</span><span>{ICON_CHECK} {book_chip(it)}</span>'
            if it["pg"] or True:
                h.append(f'<a class="o right" href="{URI}q{qid}">{inner}</a>')
        else:
            en, ar = it["wrong"][k]
            h.append(f'<div class="wo"><div class="o"><span class="l">{k}.</span><span class="x">{esc(o)}</span></div>'
                     f'<div class="rw"><span class="en">{ICON_X}{esc(en)}</span><span class="ar" dir="rtl">{esc(ar)}</span></div></div>')
    en, ar = it["why"]
    h.append(f'<div class="why"><div class="en"><b>Why:</b> {esc(en)}</div><div class="ar" dir="rtl"><b>لماذا:</b> {esc(ar)}</div></div>')
    if it.get("pearl"):
        pe, pa = it["pearl"]
        h.append(f'<div class="pearl"><div class="en">{ICON_STAR} <b>Tell the students:</b> {esc(pe)}</div>'
                 f'<div class="ar" dir="rtl"><b>قل للطلاب:</b> {esc(pa)}</div></div>')
    if it.get("note"):
        ne, na = it["note"]
        h.append(f'<div class="note"><div class="en"><b>Question note:</b> {esc(ne)}</div><div class="ar" dir="rtl"><b>ملاحظة على السؤال:</b> {esc(na)}</div></div>')
    h.append('</article>')
    return "".join(h)


def cover_html(groups):
    parts = {}
    for g in groups: parts.setdefault(g["part"], []).append(g)
    c = ['<section class="cover"><div style="font:700 8pt Inter;letter-spacing:.14em;color:#66756C">YMNOTES · DIGESTIVE · MID-MODULE</div>',
         '<h1>Questions — Answer Key<br>&amp; Study Guide</h1><div class="sub">Version 2 · for the teacher · every answer links to its line in the book</div>',
         '<div class="sub-ar">مفتاح الإجابات ودليل المذاكرة — النسخة الثانية للمدرّس</div>',
         '<h2>How to use · طريقة الاستخدام</h2><div class="how"><div><ul>',
         '<li><b>Green row = correct answer.</b> Tap it: the book opens at the exact line, highlighted in green.</li>',
         '<li>At the bottom of that book page tap the green <b>&lt; A·1</b> chip to return to the question.</li>',
         '<li>Each card: why it is right, why each other option is wrong, and a one-line <b>Tell the students</b> pearl.</li>',
         '<li>Every card shows its subject tag and the original chapter title.</li></ul></div>',
         '<div class="ar" dir="rtl"><ul>',
         '<li><b>الصف الأخضر = الإجابة الصحيحة.</b> اضغط عليه فيفتح الكتاب عند السطر نفسه مظللاً بالأخضر.</li>',
         '<li>أسفل صفحة الكتاب اضغط الشريحة الخضراء <b>A·1 &gt;</b> للرجوع إلى السؤال.</li>',
         '<li>في كل سؤال: لماذا صحيحة، ولماذا باقي الاختيارات خطأ، ونقطة <b>قل للطلاب</b>.</li>',
         '<li>كل سؤال عليه التخصص وعنوان الفصل الأصلي.</li></ul></div></div>',
         '<div class="legend">']
    for key in ("S", "M", "micro", "para", "pharma"):
        n, a = model.TAGS[key]
        c.append(f'<span class="tag {model.TAGCLASS[key]}">{n}<i>{a}</i></span>')
    c.append('</div><h2>Group index · فهرس المجموعات</h2>')
    for key, pname, en, ar in model.PARTS:
        c.append(f'<div class="idxh">{pname} — {esc(en)} · {ar}</div><div class="idx">')
        for g in parts[key]:
            c.append(f'<a href="#g-{g["letter"]}">{g["letter"]}</a>')
        c.append('</div>')
    c.append(f'<div><a class="btn" href="{URI}book">Open the book ↗</a><a class="btn" href="#notes" style="background:#8A3B12">Teacher notes ↗</a></div></section>')
    return "".join(c)


def notes_html(groups):
    items = [it for g in groups for it in g["items"]]
    flagged = [it for it in items if it.get("note")]
    nobook = [it for it in items if not it["pg"] and not it.get("note")]
    near = [it for it in items if it["pg"] and not it["exact"]]

    def line(it, extra=""):
        q = it["q"] if len(it["q"]) < 90 else it["q"][:87] + "…"
        return (f'<div class="nl"><a href="#q-{it["id"]}"><b>{it["group"]}·{it["pos"]}</b> <span class="q">{esc(q)}</span></a>{extra}</div>')

    h = ['<section class="notes" id="notes" style="break-before:page"><div class="gh"><span class="t">Teacher notes</span><span class="rule"></span></div>']
    h.append('<h3>Questions to double-check · أسئلة تحتاج مراجعتك</h3>')
    for it in flagged:
        ne, na = it["note"]
        h.append(line(it, f'<div>{esc(ne)}</div><div class="ar" dir="rtl">{esc(na)}</div>'))
    h.append('<h3>Not in the supplied book · غير موجودة في الكتاب</h3><div class="nl" style="border:none;padding:0 0 4pt">'
             'Hernia questions come from the separate <b>Hernia book</b> (not supplied); a few others are general anatomy/oncology. '
             'They are answered from standard references. · أسئلة الفتق من كتاب الفتق المنفصل (غير مرفق) وبعضها تشريح/أورام عامة.</div>')
    for it in nobook: h.append(line(it))
    h.append('<h3>Nearest page only · أقرب صفحة فقط</h3><div class="nl" style="border:none;padding:0 0 4pt">'
             'The exact sentence is not printed in the book (or sits inside a figure), so the link opens the closest topic page without a highlight. '
             '· الجملة نفسها غير مكتوبة بالكتاب فالرابط يفتح أقرب صفحة بدون تظليل.</div>')
    for it in near: h.append(line(it))
    h.append('<h3>What was changed versus the original file · ما تغيّر عن الملف الأصلي</h3>')
    ph = [it for it in items if it["section"] == "pharma"]
    h.append(f'<div class="nl">Questions are regrouped (3-4-5 cycle) into 4 parts: Internal Medicine &amp; Surgery, Microbiology, Parasitology, Pharmacology. '
             f'{len(ph)} drug-focused questions were collected into the Pharmacology part (the Giardia question moved to Parasitology). '
             f'Book images were compressed to ~150 dpi to keep the file phone-friendly; text stays sharp.'
             f'<div class="ar" dir="rtl">أعدنا تجميع الأسئلة (دورة 3-4-5) في 4 أجزاء. نُقل {len(ph)} سؤالاً دوائياً إلى جزء الفارماكولوجي، ونُقل سؤال Giardia إلى الباراسيتولوجي. '
             f'ضُغطت صور الكتاب إلى ~150 dpi لتخفيف الحجم والنص يبقى واضحاً.</div></div>')
    h.append('</section>')
    return "".join(h)


def answers_html(groups):
    body = [cover_html(groups)]
    cur_part = None
    for g in groups:
        if g["part"] != cur_part:
            cur_part = g["part"]
            body.append(f'<div class="part" id="part-{cur_part}"><div class="a">{g["part_label"]}</div><div class="b">{esc(g["part_name"])}</div><div class="c">{g["part_name_ar"]}</div></div>')
        body.append(f'<div class="gh" id="g-{g["letter"]}"><span class="t">Group {g["letter"]}</span><span class="rule"></span></div>')
        for it in g["items"]: body.append(card_html(it))
    body.append(notes_html(groups))
    return f'<!doctype html><html><head><meta charset="utf-8"><title>YMnotes Digestive V2</title><style>{CSS.replace("%(f)s", FONTS)}</style></head><body>{"".join(body)}</body></html>'


# ---------------------------------------------------------------- post-processing
def locate(book, it):
    """-> (pdf_page_index0, [quads] or [], dest_y)"""
    if not it["pg"] or it["pg"] not in INV: return None
    pno = INV[it["pg"]] - 1
    page = book[pno]
    quads = []
    if it["anchor"]:
        hits = page.search_for(it["anchor"], quads=True)
        if hits:
            quads = hits if len(hits) <= 3 else hits[:1]
    y = min(q.rect.y0 for q in quads) if quads else None
    return pno, quads, y


def find_chapters(book):
    out = []
    for i in range(0, min(len(book), 447)):
        t = book[i].get_text("text")
        m = re.match(r"\s*CHAPTER\s+(\d{2})\s+(.+?)\n", t)
        if m: out.append((int(m.group(1)), m.group(2).strip(), i))
    return out


def build(with_book=True):
    groups = model.load()
    items = [it for g in groups for it in g["items"]]
    hp = os.path.join(WORK, "v2.html"); open(hp, "w", encoding="utf-8").write(answers_html(groups))
    raw = os.path.join(WORK, "v2_raw.pdf")
    r = subprocess.run(["node", os.path.join(ROOT, "tools", "render.js"), hp, raw], capture_output=True, text=True)
    if r.returncode: print(r.stderr); raise SystemExit(1)
    ans = pymupdf.open(raw)
    n_ans = len(ans)
    names = ans.resolve_names()

    def dest(name):
        """-> (page, y measured from the TOP of the page). Named dests from Chromium are raw PDF coords (y up)."""
        d = names[name]
        H = ans[d["page"]].rect.height
        y_up = d["to"][1] if isinstance(d["to"], (tuple, list)) else d["to"].y
        return d["page"], max(0.0, H - y_up + TOP_MARGIN)
    card_dest = {it["id"]: dest(f"q-{it['id']}") for it in items}
    group_dest = {g["letter"]: dest(f"g-{g['letter']}") for g in groups}
    part_dest = {k: group_dest[[g["letter"] for g in groups if g["part"] == k][0]] for k, *_ in model.PARTS}
    notes_dest = dest("notes")

    # header/footer + numbers on the answer pages
    stamp.stamp(ans, {i: str(i + 1) for i in range(1, n_ans)}, right_label="DIGESTIVE / MID-MODULE  ·  ANSWER KEY")

    book = pymupdf.open(BOOK) if with_book else None
    final = ans
    book_start = n_ans
    loc = {}
    if with_book:
        for it in items:
            loc[it["id"]] = locate(book, it)
        final.insert_pdf(book, links=True, annots=True)
        # ---- link rewrite on answer pages
        n_goto = n_none = 0
        for pno in range(n_ans):
            pg = final[pno]
            for lk in pg.get_links():
                u = lk.get("uri", "") or ""
                if not u.startswith(URI): continue
                rect = lk["from"]
                pg.delete_link(lk)
                tail = u[len(URI):]
                if tail == "book":
                    pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": rect, "page": book_start, "to": pymupdf.Point(0, 0), "zoom": 0}); continue
                qid = int(tail[1:]); L = loc.get(qid)
                if L:
                    pno_b, quads, y = L
                    ty = max(0, (y if y is not None else 0) - 70)
                    pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": rect, "page": book_start + pno_b, "to": pymupdf.Point(0, ty), "zoom": 0})
                    n_goto += 1
                else:
                    n_none += 1
        print("answer links ->book:", n_goto, "| rows without book page:", n_none)
    # ---- turn Chromium's named-destination links into explicit page destinations (works in every viewer)
    n_named = 0
    for pno in range(n_ans):
        pg = final[pno]
        for lk in pg.get_links():
            if lk["kind"] == pymupdf.LINK_NAMED and lk.get("nameddest") in names:
                tp = lk["page"]; H = final[tp].rect.height
                ty = max(0.0, H - lk["to"].y + TOP_MARGIN - 8)
                rect = lk["from"]
                pg.delete_link(lk)
                pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": rect, "page": tp, "to": pymupdf.Point(0, ty), "zoom": 0})
                n_named += 1
    print("named links converted:", n_named)
    if with_book:
        # ---- highlights + back chips on the book pages
        by_page = {}
        for it in items:
            L = loc[it["id"]]
            if L: by_page.setdefault(L[0], []).append((it, L))
        F = stamp.F_SEMI
        font = pymupdf.Font(fontfile=F)
        n_hl = 0
        for pno_b, lst in sorted(by_page.items()):
            pg = final[book_start + pno_b]
            x = 36.0; y0 = 818.5
            for it, (_, quads, y) in lst:
                if it["exact"] and quads:
                    an = pg.add_highlight_annot(quads)
                    an.set_colors(stroke=(0.25, 0.95, 0.45)); an.set_opacity(0.55); an.update(); n_hl += 1
                lab = f'{it["group"]}·{it["pos"]}'
                w = font.text_length(lab, fontsize=7.4) + 16
                if x + w > 520: x = 36.0; y0 -= 14.5
                rect = pymupdf.Rect(x, y0, x + w, y0 + 12.5)
                pg.draw_rect(rect, color=None, fill=stamp.GREEN, radius=0.3)
                tri = [(x + 6.6, y0 + 3.4), (x + 6.6, y0 + 9.1), (x + 3.2, y0 + 6.25)]
                pg.draw_polyline(tri, color=None, fill=(1, 1, 1), closePath=True)
                pg.insert_text((x + 9.6, y0 + 9.1), lab, fontfile=F, fontname="InterS", fontsize=7.4, color=(1, 1, 1))
                cp, cy = card_dest[it["id"]]
                pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": rect, "page": cp, "to": pymupdf.Point(0, max(0.0, cy - 10)), "zoom": 0})
                x += w + 3
        print("book pages referenced:", len(by_page), "| highlights:", n_hl)

    # ---- outline
    toc = [[1, "Cover & group index", 1]]
    for key, pname, en, ar in model.PARTS:
        toc.append([1, f"{pname} — {en}", part_dest[key][0] + 1])
        for g in groups:
            if g["part"] == key: toc.append([2, f"Group {g['letter']}", group_dest[g["letter"]][0] + 1])
    toc.append([1, "Teacher notes", notes_dest[0] + 1])
    if with_book:
        toc.append([1, "BOOK — Digestive System (hyperlinked)", book_start + 1])
        for num, title, i in find_chapters(book):
            toc.append([2, f"Chapter {num:02d} — {title}", book_start + i + 1])
    final.set_toc(toc)
    final.set_metadata({"title": "YMnotes — Digestive Mid-Module Answer Key + Book (Version 2)", "author": "YMnotes",
                        "subject": "Answer key with Arabic/English explanations, hyperlinked to the book",
                        "keywords": "YMnotes, digestive, answers, hyperlinked"})
    out = OUT if with_book else OUT_NOBOOK
    os.makedirs(os.path.dirname(out), exist_ok=True)
    final.save(out, garbage=4, deflate=True, clean=True, use_objstms=True)
    print("saved", out, round(os.path.getsize(out) / 1024 / 1024, 1), "MB;", len(final), "pages (answers:", n_ans, ")")
    return out


if __name__ == "__main__":
    build(with_book=("--nobook" not in sys.argv))
