#!/usr/bin/env python3
"""Build "YMnotes Digestive System — Other Subjects Capsule".

    python3 build.py      # -> ../YMnotes-Digestive-Other-Subjects-Capsule.pdf

content.json + capsule.css + design-tokens.css -> capsule.html -> Vivliostyle
(pass 1 placeholders; contents folios read back from the rendered link targets;
pass 2 re-verified) -> adaptive watermark and permanent closing page (YMnotes
medical-book redesign skill scripts) -> PDF outline.
Set YMNOTES_SKILL to override the installed skill path.
"""
import html, json, os, pathlib, re, shutil, subprocess, sys
import pymupdf

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent
BUILD = PROJECT / "build"
OUT_PDF = PROJECT / "YMnotes-Digestive-Other-Subjects-Capsule.pdf"
SKILL = pathlib.Path(os.environ.get(
    "YMNOTES_SKILL",
    "/root/.claude/skills/synced/9e64779b-7e56-405a-bea8-e1a695a63aec_"
    "b53328e2-3aba-468f-bac9-89c120548dbd/ymnotes-medical-book-redesign"))
BRAND = json.loads((SKILL / "assets/brand/brand.json").read_text(encoding="utf-8"))
PRIMARY_URL = BRAND["destinations"]["youtube"]["url"]
HOME_URL = BRAND.get("brand_home_url") or PRIMARY_URL
C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
esc = html.escape
SUBJECTS = ["Pharmacology", "Pathology", "Microbiology", "Parasitology"]


def svg(name):
    return re.sub(r"<\?xml[^>]*>", "", (HERE / "assets/brand" / name).read_text(encoding="utf-8"))


def chip(s):
    return f'<span class="subj-chip s-{s.lower()}">{s.upper()}</span>'


def items_all():
    return [(c, i) for c in C["chapters"] for i in c["items"]]


def furniture():
    return f"""
<div class="hdr-left"><a href="{esc(HOME_URL)}">{svg('ymnotes-mark-h.svg')}</a></div>
<div class="hdr-right"><a href="{esc(PRIMARY_URL)}">{svg('qr-youtube-compact.svg')}</a></div>
<div class="ftr-left">YMNOTES MEDICAL · OTHER SUBJECTS CAPSULE</div>
<div class="ftr-right"><span class="folio"></span></div>"""


def cover():
    adds = sum(1 for _, i in items_all() if i["kind"] != "discrepancy")
    disc = sum(1 for _, i in items_all() if i["kind"] == "discrepancy")
    return f"""
<section class="cover" id="cover">
  <div class="cover__band"></div>
  <div class="cover__mark">{svg('ymnotes-mark-h.svg')}</div>
  <div class="cover__ghost">{svg('ymnotes-symbol.svg')}</div>
  <div class="cover__series">YMNOTES MEDICAL · COMPANION CAPSULE</div>
  <h1 class="cover__title">YMnotes Digestive System<span>Other Subjects Capsule</span></h1>
  <div class="cover__rule"></div>
  <div class="cover__sub">Pharmacology, pathology, microbiology and parasitology points from <b>GIT Others</b> that your book does not already contain. They are arranged by your chapters, across both halves of the book.</div>
  <div class="cover__stats">
    <div><b>{adds}</b>additions</div>
    <div><b>{len(C['chapters'])}</b>chapters with entries</div>
    <div><b>{disc}</b>points to check</div>
  </div>
</section>"""


def about():
    legend = " ".join(chip(s) for s in SUBJECTS)
    return f"""
<section class="front-page" id="about">
  <div class="front-kicker">HOW TO USE</div>
  <h1 class="front-title">About this capsule</h1>
  <p class="lede">A short teaching supplement to <b>{esc(C['companion_to'])}</b>. When you finish a chapter, open that chapter here. Each entry adds only what <b>GIT Others</b> contributes beyond your book: a fact, a distinction, a drug or laboratory detail, or a short mechanism. Points your book already makes, even in other words, are left out.</p>
  <div class="keygrid">
    <div class="keycell">
      <h3>Page references</h3>
      <p><b style="color:var(--c-identity)">Book p. 196</b> is the <b>printed page number</b> at the foot of your book’s page.</p>
      <p><b>1st-half PDF p. 199</b> or <b>2nd-half PDF p. 135</b> is the page number your PDF viewer shows in that file. It is a different number, given only to help you find the page.</p>
      <p><b>GIT Others p. 20</b> is the page in <span class="small">GIT others.pdf</span>. Its PDF page number and printed page number are the same.</p>
    </div>
    <div class="keycell">
      <h3>Subjects and checks</h3>
      <p>Each entry is labelled with the subject it comes from:</p>
      <p>{legend}</p>
      <p><span class="check" style="margin:0">CHECK</span> with a dashed border marks a place where the sources disagree, or where your book disagrees with itself. Both versions are quoted and neither is chosen for you.</p>
    </div>
  </div>
  <h2 class="h2">Your book’s two files and where they join</h2>
  <table class="map">
    <thead><tr><th>File</th><th>Printed pages</th><th>Converting a viewer page</th><th>Chapters</th></tr></thead>
    <tbody>
      <tr><td>1st half · 4_5875397832227168769.PDF (200 PDF pages)</td><td class="num">1–197</td><td>printed = PDF page − 3</td><td>1–14, and the start of 15</td></tr>
      <tr><td>2nd half · 4_5875397832227168769(1).PDF (238 PDF pages)</td><td class="num">197–433</td><td>printed = PDF page + 196<br><span class="muted">(PDF p. 238 is the closing page, with no number)</span></td><td>the rest of 15, then 16–40</td></tr>
    </tbody>
  </table>
  <p class="small">The files join <b>inside Chapter 15, Colorectal Cancer</b> (pp. 195–209). Printed page 197 is in both files. Chapter 15 is treated as one chapter here.</p>
  <p class="end-note">All 47 pages of GIT Others were compared with both files of YMnotes Digestive System, Version 3 (printed pp. 1–433). Every entry, and every point left out, is recorded in the comparison ledger that comes with this capsule.</p>
</section>"""


def toc(pages):
    def row(anchor, num, title, sub, meta, subjects=()):
        chips = f'<span class="toc-subjchips">{"".join(chip(s) for s in subjects)}</span>' if subjects else ""
        return (f'<div class="toc-row"><a href="#{anchor}"><span class="toc-num">{num}</span>'
                f'<span class="toc-text"><span class="toc-title">{esc(title)}</span>'
                f'<span class="toc-subject">{esc(sub)}</span>{chips}</span>'
                f'<span class="toc-meta">{esc(meta)}</span>'
                f'<span class="toc-page-no">{pages.get(anchor, "")}</span></a></div>')
    rows = []
    for c in C["chapters"]:
        subj = [s for s in SUBJECTS if any(i["subject"] == s for i in c["items"])]
        n = len(c["items"])
        if c["n"] == 15:
            rows.append('<div class="toc-row" style="border-bottom:none"><span class="toc-meta" style="color:var(--c-identity)">— the two book files join inside Chapter 15 (printed p. 197) —</span></div>')
        rows.append(row(f"ch-{c['n']}", f"{c['n']:02d}", c["title"], c["subjects"],
                        f"Book {c['book_pages']} · {c['half']} · {n} entr{'y' if n == 1 else 'ies'}", subj))
    rows.append(row("checked", "—", "The other 34 chapters: checked, nothing to add",
                    "Includes Ch 9 Parasitic GI Diseases, which GIT Others repeats word for word", "Book pp. 1–433"))
    rows.append(row("disc-index", "!", "Points to check", "Every CHECK entry in one list", ""))
    return f"""
<section class="toc-page" id="contents">
  <div class="front-kicker">CONTENTS</div>
  <h1 class="front-title">Contents</h1>
  <p class="lede" style="margin-bottom:var(--sp-3)">In your book’s chapter order. Tap a row to go to it. The number on the right is the page in this capsule. The book pages are printed page numbers.</p>
  <div class="toc-part">CHAPTERS WITH ADDITIONS</div>
  <div class="toc-list">{''.join(rows)}</div>
</section>"""


def item_html(it):
    disc = it["kind"] == "discrepancy"
    where = (f'<b>Fits after:</b> {esc(it["fits"])} · <b>Book p. {it["book_page"]}</b> '
             f'<span>({it["book_file"]} PDF p. {it["book_pdf"]})</span>')
    if it.get("also"):
        where += f' · also {esc(it["also"])}'
    body = f'<p class="item__where">{where}</p><p class="item__head">{esc(it["head"])}</p>'
    for t in it.get("text", []):
        body += f'<p class="item__text">{t}</p>'
    if it.get("list"):
        body += "<ul>" + "".join(f"<li>{t}</li>" for t in it["list"]) + "</ul>"
    if it.get("table"):
        t = it["table"]
        body += ('<table class="map" style="margin:1.4mm 0 0.6mm"><thead><tr>'
                 + "".join(f"<th>{h}</th>" for h in t["head"]) + "</tr></thead><tbody>"
                 + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in t["rows"])
                 + "</tbody></table>")
    if it.get("after"):
        body += f'<p class="item__text small muted">{it["after"]}</p>'
    s = it["subject"]
    src = (f'<span class="tag">{s.upper()}</span>'
           + ('<span class="check">CHECK</span>' if disc else '')
           + f'<span class="ref">GIT Others p. {esc(it["others_pages"])}</span>'
           f'<span class="id"><b>{esc(it["id"])}</b></span>'
           f'<span class="id">ledger {", ".join(it["ledger"])}</span>')
    return (f'<div class="item s-{s.lower()}{" k-discrepancy" if disc else ""}" id="{it["id"]}">'
            f'<div class="item__body">{body}</div><div class="item__src">{src}</div></div>')


def chapter_html(ch, first=False):
    nav = f"CHAPTER {ch['n']} · {ch['title'].upper()}"
    join = ('<div class="join-marker">THE TWO BOOK FILES JOIN INSIDE CHAPTER 15 (PRINTED P. 197)</div>'
            if ch["n"] == 15 else "")
    items = "".join(item_html(i) for i in ch["items"])
    return f"""{join}
<section class="chapter" id="ch-{ch['n']}" style="{'break-before:page; ' if first else ''}string-set: chapter-label '{esc(nav)}'">
  <div class="ch-head">
    <div class="ch-num">{ch['n']:02d}</div>
    <div class="ch-titles">
      <h2 class="ch-title">{esc(ch['title'])}</h2>
      <div class="ch-sub"><b>{esc(ch['subjects'])}</b> · Main book {esc(ch['book_pages'])}<span class="ch-half">{esc(ch['half'])}</span></div>
    </div>
  </div>
  <p class="teach-note">{esc(ch['files_note'])}</p>
  {items}
</section>"""


def body():
    chs = "".join(chapter_html(c, i == 0) for i, c in enumerate(C["chapters"]))
    rows = "".join(f"<tr><td class='num'><b>{n:02d}</b></td><td>{esc(t)}</td><td class='num'>{esc(p)}</td><td>{chip(s.split(' · ')[0])}</td><td>{esc(note)}</td></tr>"
                   for n, t, p, s, note in C["checked"])
    shown = {c["n"] for c in C["chapters"]} | {r[0] for r in C["checked"]}
    rest = ", ".join(str(n) for n in range(1, 41) if n not in shown)
    return f"""
{chs}
<section id="checked" style="break-before:page; string-set: chapter-label 'CHAPTERS CHECKED'">
  <h2 class="h2">The other 34 chapters: checked, nothing to add</h2>
  <p class="small">Every topic in GIT Others was matched to your book’s chapters in both files. In these chapters GIT Others covers the topic, but your book already says it:</p>
  <table class="map">
    <thead><tr><th>Ch</th><th>Chapter</th><th>Book pages</th><th>Subject</th><th>Where your book already has it</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="small"><b>No matching material in GIT Others:</b> chapters {rest}.</p>
</section>"""


def disc_index():
    rows = "".join(
        f"<tr><td class='num'><a href='#{i['id']}'><b>{i['id']}</b></a></td><td class='num'>{c['n']}</td>"
        f"<td>{chip(i['subject'])}</td><td>{esc(i['head'])}</td>"
        f"<td class='num'>Book p. {i['book_page']} ({i['book_file']} PDF p. {i['book_pdf']}){('<br>also ' + esc(i['also'])) if i.get('also') else ''}</td>"
        f"<td class='num'>GIT Others p. {esc(i['others_pages'])}</td></tr>"
        for c, i in items_all() if i["kind"] == "discrepancy")
    return f"""
<section id="disc-index" style="string-set: chapter-label 'POINTS TO CHECK'">
  <h2 class="h2">Points to check</h2>
  <p class="small">In these places your book and GIT Others disagree, or your book disagrees with itself. Each entry quotes both versions and chooses neither. Tap an ID to open the entry.</p>
  <table class="map" style="table-layout:fixed"><colgroup><col style="width:15mm"><col style="width:8mm"><col style="width:30mm"><col style="width:43mm"><col style="width:51mm"><col style="width:28mm"></colgroup>
  <thead><tr><th>Entry</th><th>Ch</th><th>Subject</th><th>Topic</th><th>Main book</th><th>Source</th></tr></thead>
  <tbody>{rows}</tbody></table>
</section>"""


def document(pages):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{esc(C['title'])}</title>
<meta name="author" content="YMnotes">
<link rel="stylesheet" href="capsule.css">
</head><body>
{furniture()}{cover()}{about()}{toc(pages)}{body()}{disc_index()}
</body></html>"""


def render(pages, out):
    stage = BUILD / "html"
    stage.mkdir(parents=True, exist_ok=True)
    for f in ("capsule.css", "design-tokens.css"):
        shutil.copy2(HERE / f, stage / f)
    if (stage / "assets").exists():
        shutil.rmtree(stage / "assets")
    shutil.copytree(HERE / "assets", stage / "assets")
    (stage / "capsule.html").write_text(document(pages), encoding="utf-8")
    shutil.copy2(stage / "capsule.html", HERE / "capsule.html")
    r = subprocess.run(["npx", "--yes", "--quiet", "@vivliostyle/cli", "build",
                        str(stage / "capsule.html"), "-o", str(out)], capture_output=True, text=True, cwd=stage)
    if r.returncode or not out.exists():
        sys.exit("vivliostyle failed:\n" + r.stdout + r.stderr)


def anchor_pages(pdf):
    d = pymupdf.open(pdf); found = {}
    for pno in range(d.page_count):
        for l in d[pno].get_links():
            m = re.search(r"0023([A-Za-z0-9:\-]+)$", l.get("nameddest") or "")
            if m and l.get("page") is not None and l["page"] >= 0:
                found.setdefault(m.group(1).replace(":002d", "-"), l["page"] + 1)
    return found


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    raw1, raw2 = BUILD / "pass1.pdf", BUILD / "pass2.pdf"
    render({}, raw1); pages = anchor_pages(raw1)
    render(pages, raw2); pages2 = anchor_pages(raw2)
    wanted = [f"ch-{c['n']}" for c in C["chapters"]] + ["checked", "disc-index"]
    if [a for a in wanted if a not in pages2] or any(pages.get(a) != pages2.get(a) for a in wanted):
        sys.exit(f"contents folios unresolved or moved: {pages} vs {pages2}")
    wm = BUILD / "wm.pdf"
    r = subprocess.run([sys.executable, str(SKILL / "scripts/apply_watermark.py"), str(raw2), str(wm),
                        str(SKILL / "assets/brand" / BRAND["assets"]["watermark_wordmark"]),
                        "--openers", "0", "--suppress", "1,3", "--report"], capture_output=True, text=True)
    src = wm if (r.returncode == 0 and wm.exists()) else raw2
    closed = BUILD / "closed.pdf"
    r = subprocess.run([sys.executable, str(SKILL / "scripts/append_final_page.py"), str(src),
                        str(SKILL / "assets/brand" / BRAND["assets"]["final_page"]), str(closed)],
                       capture_output=True, text=True)
    print(r.stdout.strip()[-300:])
    if r.returncode:
        sys.exit("closing page failed: " + r.stderr)
    d = pymupdf.open(closed)
    toc = [[1, "Cover", 1], [1, "About this capsule", 2], [1, "Contents", 3]]
    for c in C["chapters"]:
        toc.append([1, f"Ch {c['n']} · {c['title']}", pages2[f"ch-{c['n']}"]])
    toc += [[1, "Other chapters checked (nothing to add)", pages2["checked"]],
            [1, "Points to check", pages2["disc-index"]], [1, "Stay with YMnotes", d.page_count]]
    d.set_toc(toc)
    d.set_metadata({"title": C["title"], "author": "YMnotes",
                    "subject": "Companion capsule to YMnotes Digestive System, Version 3: additions from GIT Others",
                    "keywords": "YMnotes; digestive system; pharmacology; pathology; microbiology; parasitology"})
    d.save(OUT_PDF, garbage=3, deflate=True)
    (BUILD / "anchor-pages.json").write_text(json.dumps(pages2, indent=1), encoding="utf-8")
    print("wrote", OUT_PDF, d.page_count, "pages")


if __name__ == "__main__":
    main()
