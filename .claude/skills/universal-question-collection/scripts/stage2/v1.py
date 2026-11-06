# -*- coding: utf-8 -*-
"""Stage 2 · Version 1 — the student/tablet PDF: clean question groups, no answers, no chapter titles, no numbering."""
import html, json, os, re, subprocess
import pymupdf
import stamp
from deck import BRAND

FONTS = "file://" + os.path.join(BRAND, "fonts") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))
esc = html.escape

CSS = """
@font-face{font-family:'Inter';font-weight:400;src:url(%(f)sinter-latin-400-normal.woff2)}
@font-face{font-family:'Inter';font-weight:600;src:url(%(f)sinter-latin-600-normal.woff2)}
@font-face{font-family:'Archivo';font-weight:600;src:url(%(f)sarchivo-latin-600-normal.woff2)}
@font-face{font-family:'Source Serif 4';font-weight:400;src:url(%(f)ssource-serif-4-latin-400-normal.woff2)}
@font-face{font-family:'Source Serif 4';font-weight:600;src:url(%(f)ssource-serif-4-latin-600-normal.woff2)}
@page{size:595.28pt 841.89pt;margin:62pt 42.5pt 54pt 56.7pt}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
.group{break-before:page}.group:first-child{break-before:auto}
.gh{display:flex;align-items:center;height:24pt;margin-top:.6pt;break-after:avoid}
.gh .t{font:600 15.6pt/1 'Archivo','Inter',sans-serif;color:#1A5B31;margin-right:13pt;white-space:nowrap}
.gh .rule{flex:1;border-top:.6pt solid #7FAE92}
.sec{margin:12pt 0 0 12pt;font:600 9.2pt/1 'Inter',sans-serif;color:#1A5B31;padding-bottom:5pt;border-bottom:.3pt solid #D4DDD7;break-after:avoid}
.qs{margin-top:6.9pt}
.q{margin-left:12pt;position:relative;padding-bottom:13pt;break-inside:avoid}
.q + .q{border-top:.3pt solid #D4DDD7;padding-top:9pt}
.pass{margin:0 0 7pt;padding:6pt 9pt;background:#F6F9F7;border-left:2pt solid #7FAE92;font:400 10pt/1.45 'Source Serif 4','DejaVu Serif',serif;color:#15201A;white-space:pre-wrap}
.qt{font:400 11.3pt/17pt 'Source Serif 4','DejaVu Serif',serif;color:#15201A;position:relative;white-space:pre-wrap}
.qt::before{content:"";position:absolute;left:-11pt;top:.4pt;bottom:0;width:1.7pt;background:#DCEAE0}
.fig{margin:6pt 0 0}.fig img{max-width:100%;max-height:170pt}
.opts{margin-top:7.1pt}
.o{display:grid;grid-template-columns:22pt 1fr;align-items:baseline;min-height:17.5pt}
.o .l{font:400 9.6pt/17.5pt 'Inter',sans-serif;color:#34423A}
.o .x{font:400 10.9pt/16.5pt 'Source Serif 4','DejaVu Serif',serif;color:#15201A;position:relative;top:-1.8pt;white-space:pre-wrap}
"""


def group_html(g, show_part):
    h = [f'<section class="group"><div class="gh"><span class="t">Group {g["letter"]}</span><span class="rule"></span></div>']
    if show_part:
        h.append(f'<div class="sec">{esc(g["part_title"])}</div>')
    h.append('<div class="qs">')
    last_pass = None
    for it in g["items"]:
        h.append('<div class="q">')
        if it["passage"] and it["group_src"] != last_pass:
            h.append(f'<div class="pass">{esc(it["passage"])}</div>')
        last_pass = it["group_src"] if it["passage"] else None
        h.append(f'<div class="qt">{esc(it["q"])}</div>')
        for im in it["images"]:
            h.append(f'<div class="fig"><img src="file://{esc(im)}"></div>' if os.path.isfile(im) else '<div class="fig">[figure missing]</div>')
        h.append('<div class="opts">')
        for k, o in zip(it["labels"], it["opts"]):
            h.append(f'<div class="o"><span class="l">{k}.</span><span class="x">{esc(o)}</span></div>')
        h.append('</div></div>')
    h.append('</div></section>')
    return "".join(h)


def build(groups, deck, out_pdf, workdir):
    os.makedirs(workdir, exist_ok=True)
    body = "".join(group_html(g, show_part=g["part_index"] > 0) for g in groups)
    doc_html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{esc(deck["module_label"])}</title>'
                f'<style>{CSS.replace("%(f)s", FONTS)}</style></head><body>{body}</body></html>')
    hp = os.path.join(workdir, "v1.html")
    open(hp, "w", encoding="utf-8").write(doc_html)
    raw = os.path.join(workdir, "v1_raw.pdf")
    r = subprocess.run(["node", os.path.join(HERE, "render.js"), hp, raw], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("render failed: " + r.stderr[-600:])
    doc = pymupdf.open(raw)
    stamp.stamp(doc, {i: str(i + 1) for i in range(len(doc))}, right_label=deck["module_label"])
    # bookmarks: the page that starts each group
    starts, seen = [], set()
    for i, pg in enumerate(doc):
        ws = [w[4] for w in pg.get_text("words", clip=pymupdf.Rect(40, 58, 300, 90))]
        if len(ws) >= 2 and ws[0] == "Group" and ws[1] not in seen:
            seen.add(ws[1]); starts.append((ws[1], i + 1))
    parts = {g["letter"]: g for g in groups}
    doc.set_toc([[1, f"Group {L}" + ("" if parts[L]["part_index"] == 0 else f" · {parts[L]['part_title']}"), p] for L, p in starts if L in parts])
    doc.set_metadata({"title": f'{deck["brand"]} — {deck["module_label"]} questions (Version 1, students)', "author": deck["brand"]})
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    doc.save(out_pdf, garbage=4, deflate=True)
    return {"pages": len(doc), "groups": len(groups), "questions": sum(len(g["items"]) for g in groups)}
