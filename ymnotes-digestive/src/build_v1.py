# -*- coding: utf-8 -*-
"""Version 1 — the student/tablet version: same design as the original, without chapter titles."""
import os, sys, html, subprocess, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model, stamp
import pymupdf

ROOT = model.ROOT
WORK = os.environ.get("YM_WORK", "/tmp/ymnotes_work")
os.makedirs(WORK, exist_ok=True)
FONTS = "file://" + os.path.join(ROOT, "assets", "fonts") + "/"
OUT = os.path.join(ROOT, "output", "YMnotes_Digestive_Mid_Module_Questions_V1_Students.pdf")

CSS = """
@font-face{font-family:'Inter';font-weight:400;src:url(%(f)sinter-latin-400-normal.woff2)}
@font-face{font-family:'Inter';font-weight:600;src:url(%(f)sinter-latin-600-normal.woff2)}
@font-face{font-family:'Archivo';font-weight:600;src:url(%(f)sarchivo-latin-600-normal.woff2)}
@font-face{font-family:'Source Serif 4';font-weight:400;src:url(%(f)ssource-serif-4-latin-400-normal.woff2)}
@font-face{font-family:'Source Serif 4';font-weight:600;src:url(%(f)ssource-serif-4-latin-600-normal.woff2)}
@page{size:595.28pt 841.89pt;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
.page{width:595.28pt;height:841.89pt;position:relative;overflow:hidden;break-after:page;page-break-after:always}
.content{position:absolute;left:56.7pt;width:496.1pt;top:62pt}
.gh{display:flex;align-items:center;height:24pt;margin-top:.6pt}
.gh .t{font:600 15.6pt/1 'Archivo','Inter',sans-serif;color:#1A5B31;margin-right:13pt;white-space:nowrap}
.gh .rule{flex:1;border-top:.6pt solid #7FAE92}
.sec{margin:12pt 0 0 12pt;font:600 9.2pt/1 'Inter',sans-serif;color:#1A5B31;padding-bottom:5pt;border-bottom:.3pt solid #D4DDD7}
.qs{margin-top:6.9pt}
.q{margin-left:12pt;position:relative;padding-bottom:13pt}
.q + .q{border-top:.3pt solid #D4DDD7;padding-top:9pt}
.qt{font:400 11.3pt/17pt 'Source Serif 4','DejaVu Serif',serif;color:#15201A;position:relative}
.qt::before{content:"";position:absolute;left:-11pt;top:.4pt;bottom:0;width:1.7pt;background:#DCEAE0}
.opts{margin-top:7.1pt}
.o{display:grid;grid-template-columns:22pt 1fr;align-items:baseline;min-height:17.5pt}
.o .l{font:400 9.6pt/17.5pt 'Inter',sans-serif;color:#34423A}
.o .x{font:400 10.9pt/16.5pt 'Source Serif 4','DejaVu Serif',serif;color:#15201A;position:relative;top:-1.8pt}
"""


def page_html(g):
    h = [f'<section class="page"><div class="content"><div class="gh"><span class="t">Group {g["letter"]}</span><span class="rule"></span></div>']
    if g["part"] != "medsurg":
        h.append(f'<div class="sec">{html.escape(g["part_name"])}</div>')
    h.append('<div class="qs">')
    for it in g["items"]:
        h.append('<div class="q"><div class="qt">%s</div><div class="opts">' % html.escape(it["q"]))
        for k, o in zip("ABCDE", it["opts"]):
            h.append(f'<div class="o"><span class="l">{k}.</span><span class="x">{html.escape(o)}</span></div>')
        h.append('</div></div>')
    h.append('</div></div></section>')
    return "".join(h)


def build():
    groups = model.load()
    body = "".join(page_html(g) for g in groups)
    doc_html = f'<!doctype html><html><head><meta charset="utf-8"><title>YMnotes Digestive Mid-Module Questions</title><style>{CSS % {"f": FONTS}}</style></head><body>{body}</body></html>'
    hp = os.path.join(WORK, "v1.html"); open(hp, "w", encoding="utf-8").write(doc_html)
    raw = os.path.join(WORK, "v1_raw.pdf")
    r = subprocess.run(["node", os.path.join(ROOT, "tools", "render.js"), hp, raw], capture_output=True, text=True)
    if r.returncode: print(r.stderr); raise SystemExit(1)
    bottoms = json.loads(r.stdout.split("PAGE_BOTTOMS ")[1])
    over = [(groups[i]["letter"], b) for i, b in enumerate(bottoms) if b > 790]
    print("pages:", len(bottoms), "max content bottom:", max(bottoms), "overflow:", over)
    doc = pymupdf.open(raw)
    assert len(doc) == len(groups), (len(doc), len(groups))
    stamp.stamp(doc, {i: str(i + 1) for i in range(len(doc))}, right_label=None)
    doc.set_metadata({"title": "YMnotes — Digestive Mid-Module Questions (Version 1, students)", "author": "YMnotes",
                      "subject": "Digestive system mid-module question groups", "keywords": "YMnotes, digestive, MCQ"})
    # bookmarks per group / part
    toc = []
    for i, g in enumerate(groups):
        toc.append([1, f"Group {g['letter']}" + ("" if g["part"] == "medsurg" else f"  ·  {g['part_name']}"), i + 1])
    doc.set_toc(toc)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc.save(OUT, garbage=4, deflate=True)
    print("saved", OUT, os.path.getsize(OUT) // 1024, "KB")


if __name__ == "__main__":
    build()
