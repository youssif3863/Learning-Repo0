#!/usr/bin/env python3
"""Build the YMnotes hepatology extras handout.

content.json  -> handout.html -> Chromium print (render.cjs) -> furniture post-pass
(header mark, navigation, QR, footer, folio) -> page labels, bookmarks, contents
folios -> closing page (skill's append_final_page.py) -> ../output/*.pdf

Two render passes: the first finds each chapter's physical page so the contents
can print real folios; the second prints them. Run from anywhere:
    python3 build.py
"""
import html, json, os, pathlib, re, subprocess, sys
import pymupdf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "output"
QA = ROOT / "qa"
SKILL = pathlib.Path(os.environ.get("YMNOTES_SKILL", "/root/.claude/skills/synced/9e64779b-7e56-405a-bea8-e1a695a63aec_b53328e2-3aba-468f-bac9-89c120548dbd/ymnotes-medical-book-redesign"))
FINAL_NAME = "YMnotes Digestive System - After Mid-Module Hepatology Extras.pdf"
TITLE = "YMnotes Digestive System — After Mid-Module Hepatology Extras"
BRAND = json.loads((HERE / "assets/brand/brand.json").read_text())
HOME_URL = BRAND["brand_home_url"] or next(d["url"] for d in BRAND["destinations"].values() if d["role"] == "primary")
FOOTER_ID = "YMNOTES MEDICAL · DIGESTIVE SYSTEM · HEPATOLOGY EXTRAS"

KINDS = {  # class, visible label (colour never works alone: the label carries it)
    "mechanism": ("k-mech", "MECHANISM"),
    "investigation": ("k-inv", "INVESTIGATION"),
    "distinction": ("k-dist", "DISTINCTION"),
    "management": ("k-mgmt", "MANAGEMENT"),
    "caution": ("k-warn", "CAUTION"),
    "fact": ("k-fact", "KEY FACT"),
}

GREEN = (0x1A / 255, 0x5B / 255, 0x31 / 255)
DEEP = (0x0F / 255, 0x3C / 255, 0x21 / 255)
MUTED = (0x66 / 255, 0x75 / 255, 0x6C / 255)
RULE = (0xD4 / 255, 0xDD / 255, 0xD7 / 255)
SOFT = (0x7F / 255, 0xAE / 255, 0x92 / 255)
MM = 72 / 25.4


def svg_inline(name, color=None):
    s = (HERE / "assets/brand" / name).read_text()
    s = re.sub(r"<\?xml.*?\?>", "", s)
    return s


def e(s):
    return html.escape(s, quote=False)


def page_ref(item):
    parts = []
    if item.get("book"):
        parts.append("Book " + item["book"])
    if item.get("src"):
        parts.append("Src " + item["src"])
    parts = [x.replace(" ", "\u00a0") for x in parts]  # each reference stays whole; the pair may wrap
    return f'<span class="ref">{" · ".join(parts)}</span>' if parts else ""


def render_item(item):
    cls, lab = KINDS[item["kind"]]
    body = item["text"]  # trusted authored HTML (handout editor), not source text
    sub = ""
    if item.get("points"):
        sub = "<ul>" + "".join(f"<li>{p}</li>" for p in item["points"]) + "</ul>"
    table = ""
    if item.get("table"):
        t = item["table"]
        table = '<table class="t"><thead><tr>' + "".join(f"<th>{h}</th>" for h in t["head"]) + "</tr></thead><tbody>"
        table += "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in t["rows"]) + "</tbody></table>"
    return f'<li><span class="k {cls}">{lab}</span>{body}{page_ref(item)}{sub}{table}</li>'


def render_chapter(ch, first=False):
    appx = ch.get("appendix", False)
    kicker = f'APPENDIX {ch["no"]}' if appx else f'CHAPTER {ch["no"]}'
    classes = ["chapter"] + (["appx"] if appx else []) + (["first"] if first else []) + (["newpage"] if ch.get("newpage") else [])
    out = [f'<section class="{" ".join(classes)}" id="{ch["id"]}">',
           '<div class="ch-head">',
           f'<span class="ch-kicker">{kicker}</span>',
           f'<h2 class="ch-title">{e(ch["title"])}</h2>',
           f'<div class="ch-sub">{ch["subline"]}</div>',
           '<div class="ch-rule"></div></div>']
    if ch.get("note"):
        out.append(f'<div class="appendix-note">{ch["note"]}</div>')
    for tp in ch["topics"]:
        bref = f'<span class="bref">BOOK {e(tp["book"])}</span>' if tp.get("book") else ""
        out.append(f'<div class="topic"><h3>{e(tp["title"])}{bref}</h3><ul class="adds">')
        out += [render_item(it) for it in tp["items"]]
        out.append("</ul></div>")
    out.append("</section>")
    return "\n".join(out)


def build_html(content, folios):
    chapters = content["chapters"]
    appendices = content.get("appendices", [])
    toc = ['<div class="toc-head"><span>CH</span><span>BOOK CHAPTER</span><span>BOOK PAGES</span><span>PAGE</span></div><ul class="toc">']
    for ch in chapters + appendices:
        appx = ch.get("appendix", False)
        no = f'APP. {ch["no"]}' if appx else ch["no"]
        pg = folios.get(ch["id"], "00")
        toc.append(f'<li class="{"appx" if appx else ""}"><a href="#{ch["id"]}"><span class="no">{no}</span>'
                   f'<span class="t">{e(ch["title"])}<span class="subj">{e(ch["subjects"])}</span></span>'
                   f'<span class="bk">{e(ch["book_pages"])}</span><span class="pg">{pg}</span></a></li>')
    toc.append("</ul>")
    legend = "".join(f'<span><span class="k {c}">{l}</span></span>' for c, l in KINDS.values())
    body = [render_chapter(ch, first=(i == 0)) for i, ch in enumerate(chapters)]
    body += [render_chapter(ch) for ch in appendices]
    cover = f'''
<section class="cover">
  <div class="band"></div>
  <div class="emblem">{svg_inline("ymnotes-symbol.svg")}</div>
  <div class="inner">
    <div class="logo">{svg_inline("ymnotes-mark-h.svg")}</div>
    <div class="eyebrow">COMPANION EXTRAS · VERSION 3</div>
    <h1>YMnotes Digestive System<span class="sub">After Mid-Module<br>Hepatology Extras</span></h1>
    <div class="rule"></div>
    <p class="lede">{content["cover_lede"]}</p>
    <div class="meta">
      <div><b>Hepatology &amp; liver chapters · Book chapters 17–31</b><br>Keyed to the Digestive System book, printed pages 231–366<br>Hepatogastroenterology</div>
      <a class="qr" href="{html.escape(HOME_URL)}">{svg_inline("qr-youtube.svg")}YMNOTES</a>
    </div>
  </div>
</section>'''
    front = f'''
<section class="front" id="contents">
  <p class="front-kicker">INTERACTIVE CONTENTS</p>
  <h2 class="front-title">What this handout adds</h2>
  <div class="how">{content["how_to_use"]}<div class="legend">{legend}</div></div>
  {"".join(toc)}
</section>
<div style="break-after: page"></div>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(TITLE)}</title>
<link rel="stylesheet" href="handout.css"></head><body>{cover}{front}
{"".join(body)}
</body></html>'''


def render(html_text, pdf_path):
    src = HERE / "handout.html"
    src.write_text(html_text)
    subprocess.run(["node", str(HERE / "render.cjs"), str(src), str(pdf_path)], check=True)


def chapter_pages(pdf_path, content):
    doc = pymupdf.open(pdf_path)
    found = {}
    all_ch = content["chapters"] + content.get("appendices", [])
    for ch in all_ch:
        kicker = f'APPENDIX {ch["no"]}' if ch.get("appendix") else f'CHAPTER {ch["no"]}'
        hits = []
        for i, p in enumerate(doc):
            if i < 2:
                continue
            for b in p.get_text("dict")["blocks"]:
                for ln in b.get("lines", []):
                    txt = "".join(s["text"] for s in ln["spans"]).strip()
                    if txt.replace(" ", "") == kicker.replace(" ", ""):
                        hits.append((i, ln["bbox"][1]))
        if len(hits) != 1:
            raise SystemExit(f"chapter kicker {kicker!r} found {len(hits)} times")
        found[ch["id"]] = hits[0]
    return found


class Fonts:
    def __init__(self):
        f = HERE / "assets/fonts"
        self.disp = str(f / "Archivo-Semibold.ttf")
        self.disp_b = str(f / "Archivo-Bold.ttf")
        self.ui = str(f / "Inter-Medium.ttf")


def colored_svg_pdf(name, hexcolor):
    s = (HERE / "assets/brand" / name).read_text().replace("currentColor", hexcolor)
    d = pymupdf.open(stream=s.encode(), filetype="svg")
    return pymupdf.open("pdf", d.convert_to_pdf())


def furniture(pdf_in, pdf_out, content, where):
    doc = pymupdf.open(pdf_in)
    F = Fonts()
    mark = colored_svg_pdf("ymnotes-mark-h.svg", "#1A5B31")
    qr = colored_svg_pdf("qr-youtube-compact.svg", "#0F3C21")
    all_ch = content["chapters"] + content.get("appendices", [])
    starts = sorted((where[c["id"]][0], where[c["id"]][1], c) for c in all_ch)
    W, H = doc[0].rect.width, doc[0].rect.height
    li, lo = 20 * MM, 15 * MM
    page_chapter = {}
    for i, page in enumerate(doc):
        if i == 0:
            continue
        # navigation: chapter in force at the top of the page, unless a chapter opens in its top 40%
        cur = None
        for (pi, y, c) in starts:
            if pi < i or (pi == i and y < 32 * MM):  # opens at the top of this page
                cur = c
        page_chapter[i] = cur
        left, right = li, W - lo  # CSS margins are fixed inner/outer (no mirroring)
        # header: mark (link), navigation, QR (link), hairline
        mh = 5.8 * MM
        mw = mh * mark[0].rect.width / mark[0].rect.height
        mr = pymupdf.Rect(left, 9.2 * MM, left + mw, 9.2 * MM + mh)
        page.show_pdf_page(mr, mark, 0)
        page.insert_link({"kind": pymupdf.LINK_URI, "from": mr, "uri": HOME_URL})
        qs = 11.4 * MM
        qrr = pymupdf.Rect(right - qs, 5.4 * MM, right, 5.4 * MM + qs)
        page.show_pdf_page(qrr, qr, 0)
        page.insert_link({"kind": pymupdf.LINK_URI, "from": qrr, "uri": HOME_URL})
        if i == 1:
            nav_a, nav_b = "CONTENTS", ""
        elif cur is None:
            nav_a, nav_b = "", ""
        else:
            nav_a = (f'APPENDIX {cur["no"]}' if cur.get("appendix") else f'CHAPTER {cur["no"]}')
            nav_b = cur.get("nav", cur["title"])
        size = 7.8
        fa = pymupdf.Font(fontfile=F.disp_b)
        fb = pymupdf.Font(fontfile=F.disp)
        sep = "  ·  " if nav_b else ""
        wa = fa.text_length(nav_a, size) + len(nav_a) * size * 0.085
        wb = fb.text_length(sep + nav_b, size)
        zone_l, zone_r = mr.x1 + 6 * MM, qrr.x0 - 6 * MM
        if wa + wb > zone_r - zone_l:
            raise SystemExit(f"header navigation does not fit on page {i+1}: {nav_a} {nav_b}")
        x = (zone_l + zone_r) / 2 - (wa + wb) / 2
        y = 13.3 * MM
        tw = pymupdf.TextWriter(page.rect)
        xx = x
        for ch_ in nav_a:  # tracked capitals, drawn glyph by glyph
            tw.append((xx, y), ch_, font=fa, fontsize=size)
            xx += fa.text_length(ch_, size) + size * 0.085
        tw.write_text(page, color=GREEN)
        if nav_b:
            tw2 = pymupdf.TextWriter(page.rect)
            tw2.append((xx, y), sep + nav_b, font=fb, fontsize=size)
            tw2.write_text(page, color=MUTED)
        page.draw_line((left, 17.6 * MM), (right, 17.6 * MM), color=RULE, width=0.4)
        # footer: short identity rule, identity line, folio tab on the outer edge
        fy = H - 11.2 * MM
        page.draw_line((left, fy - 3.4 * MM), (left + 9 * MM, fy - 3.4 * MM), color=SOFT, width=0.9)
        fu = pymupdf.Font(fontfile=F.ui)
        tw3 = pymupdf.TextWriter(page.rect)
        xx = left
        for ch_ in FOOTER_ID:
            tw3.append((xx, fy), ch_, font=fu, fontsize=6.6)
            xx += fu.text_length(ch_, 6.6) + 6.6 * 0.14
        tw3.write_text(page, color=MUTED)
        folio = str(i)
        bw, bh = 9.5 * MM, 5.2 * MM
        bx = right - bw  # folio tab at the right edge; the identity line sits left
        box = pymupdf.Rect(bx, fy - 4.0 * MM, bx + bw, fy - 4.0 * MM + bh)
        page.draw_rect(box, color=GREEN, width=0.9)
        fbld = pymupdf.Font(fontfile=F.disp_b)
        fw = fbld.text_length(folio, 8.4)
        tw4 = pymupdf.TextWriter(page.rect)
        tw4.append((box.x0 + (bw - fw) / 2, box.y1 - 1.55 * MM), folio, font=fbld, fontsize=8.4)
        tw4.write_text(page, color=DEEP)
    doc.save(pdf_out, garbage=3, deflate=True)
    return page_chapter


def finish(pdf_in, pdf_out, content, where):
    doc = pymupdf.open(pdf_in)
    toc = [[1, "Cover", 1], [1, "Contents", 2]]
    for c in content["chapters"]:
        toc.append([1, f'Chapter {c["no"]} — {c["title"]}', where[c["id"]][0] + 1])
        for tp in c["topics"]:
            pass
    for c in content.get("appendices", []):
        toc.append([1, f'Appendix {c["no"]} — {c["title"]}', where[c["id"]][0] + 1])
    toc.append([1, "YMnotes", doc.page_count])
    doc.set_toc(toc)
    n = doc.page_count
    doc.set_page_labels([
        {"startpage": 0, "prefix": "Cover", "style": "", "firstpagenum": 1},
        {"startpage": 1, "prefix": "", "style": "D", "firstpagenum": 1},
        {"startpage": n - 1, "prefix": "YMnotes", "style": "", "firstpagenum": 1},
    ])
    doc.set_metadata({"title": TITLE, "author": "YMnotes", "subject": "Digestive System — hepatology companion extras",
                      "keywords": "YMnotes Medical; hepatology; medical education", "creator": "YMnotes Medical", "producer": "YMnotes Medical"})
    doc.save(pdf_out, garbage=3, deflate=True)


def main():
    content = json.loads((HERE / "content.json").read_text())
    work = QA / "work"
    work.mkdir(parents=True, exist_ok=True)
    p1 = work / "pass1.pdf"
    render(build_html(content, {}), p1)
    where = chapter_pages(p1, content)
    folios = {k: str(v[0]) for k, v in where.items()}  # printed folio = physical index (cover unnumbered)
    p2 = work / "pass2.pdf"
    render(build_html(content, folios), p2)
    where2 = chapter_pages(p2, content)
    if {k: v[0] for k, v in where2.items()} != {k: v[0] for k, v in where.items()}:
        raise SystemExit("pagination moved between passes")
    p3 = work / "furnished.pdf"
    furniture(p2, p3, content, where2)
    p4 = work / "with-closing.pdf"
    if p4.exists():
        p4.unlink()
    subprocess.run([sys.executable, str(SKILL / "scripts/append_final_page.py"), str(p3),
                    str(HERE / "assets/brand/ymnotes-closing-page.pdf"), str(p4)], check=True, cwd=str(SKILL / "scripts"))
    OUT.mkdir(exist_ok=True)
    final = OUT / FINAL_NAME
    finish(p4, final, content, where2)
    (QA / "chapter-map.json").write_text(json.dumps({c: {"page_index": v[0], "printed_folio": v[0]} for c, v in where2.items()}, indent=1))
    print("wrote", final, pymupdf.open(final).page_count, "pages")


if __name__ == "__main__":
    main()
