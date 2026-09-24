#!/usr/bin/env python3
"""Build "YMnotes Digestive System — After Mid-Module Extras".

    python3 build.py            # full build -> ../YMnotes-Digestive-After-Mid-Module-Extras.pdf

Pipeline (YMnotes medical-book redesign skill conventions):
  content.json + handout.css + design-tokens.css
    -> handout.html
    -> Vivliostyle (pass 1: placeholders; contents folios read back from the
       rendered link targets; pass 2: real folios, re-verified)
    -> adaptive watermark      (skill: scripts/apply_watermark.py)
    -> permanent closing page  (skill: scripts/append_final_page.py)
    -> PDF outline/bookmarks   (built here, verified on the saved file)

Paths to the skill come from YMNOTES_SKILL or the installed default below.
"""
import html, json, os, pathlib, re, shutil, subprocess, sys

import pymupdf

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent
BUILD = PROJECT / "build"
OUT_PDF = PROJECT / "YMnotes-Digestive-After-Mid-Module-Extras.pdf"
SKILL = pathlib.Path(os.environ.get(
    "YMNOTES_SKILL",
    "/root/.claude/skills/synced/9e64779b-7e56-405a-bea8-e1a695a63aec_"
    "b53328e2-3aba-468f-bac9-89c120548dbd/ymnotes-medical-book-redesign"))
BRAND = json.loads((SKILL / "assets/brand/brand.json").read_text(encoding="utf-8"))
PRIMARY_URL = BRAND["destinations"]["youtube"]["url"]
HOME_URL = BRAND.get("brand_home_url") or PRIMARY_URL

C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
esc = html.escape


def svg(name):
    s = (HERE / "assets/brand" / name).read_text(encoding="utf-8")
    return re.sub(r"<\?xml[^>]*>", "", s)


# ------------------------------------------------------------------ pieces
def furniture():
    return f"""
<div class="hdr-left"><a href="{esc(HOME_URL)}">{svg('ymnotes-mark-h.svg')}</a></div>
<div class="hdr-right"><a href="{esc(PRIMARY_URL)}">{svg('qr-youtube-compact.svg')}</a></div>
<div class="ftr-left">YMNOTES MEDICAL · AFTER MID-MODULE EXTRAS</div>
<div class="ftr-right"><span class="folio"></span></div>"""


def count_items(part, kind=None):
    n = 0
    for ch in C[part]["chapters"]:
        for it in ch["items"]:
            if kind is None or (kind == "disc") == (it["kind"] == "discrepancy"):
                n += 1
    return n


def cover():
    a_add = count_items("part_a", "add"); a_dis = count_items("part_a", "disc")
    b_add = count_items("part_b", "add"); b_dis = count_items("part_b", "disc")
    return f"""
<section class="cover" id="cover">
  <div class="cover__band"></div>
  <div class="cover__mark">{svg('ymnotes-mark-h.svg')}</div>
  <div class="cover__ghost">{svg('ymnotes-symbol.svg')}</div>
  <div class="cover__series">YMNOTES MEDICAL · COMPANION HANDOUT</div>
  <h1 class="cover__title">YMnotes Digestive System<span>After Mid-Module Extras</span></h1>
  <div class="cover__rule"></div>
  <div class="cover__sub">Points found in <b>GIT Others</b> that are missing from your main book, placed where they fit in your chapters. Use this after you finish each chapter.</div>
  <div class="cover__stats">
    <div><b>{a_add}</b>additions · chapters 15–40</div>
    <div><b>{b_add}</b>earlier-chapter additions</div>
    <div><b>{a_dis + b_dis}</b>points to check</div>
  </div>
</section>"""


def about():
    return f"""
<section class="front-page" id="about">
  <div class="front-kicker">HOW TO USE</div>
  <h1 class="front-title">About this handout</h1>
  <p class="lede">This handout goes with <b>{esc(C['companion_to'])}</b>. It contains only what <b>GIT Others</b> adds to your book: a missing fact, distinction, mechanism or clinical detail within a topic your book already covers. Anything already in your book, even in different words, has been left out.</p>

  <div class="keygrid">
    <div class="keycell">
      <h3>Reading a reference</h3>
      <p><b style="color:var(--c-identity)">Book p. 196</b> is the <b>printed page number</b> at the foot of your book’s page.</p>
      <p><b>1st-half PDF p. 199</b> is the page number your PDF viewer shows in <span class="small">4_5875397832227168769.PDF</span>. <b>2nd-half PDF</b> means <span class="small">4_5875397832227168769(1).PDF</span>.</p>
      <p><b>GIT Others p. 20</b> is the page in that source. Its PDF page and printed page are the same.</p>
    </div>
    <div class="keycell">
      <h3>Reading an entry</h3>
      <p><b>Fits after</b> names the heading in your book where the point belongs.</p>
      <p>Each entry has a label in the margin: <span class="pill" style="background:var(--c-identity-tint);color:var(--c-identity)">KEY FACT</span> <span class="pill" style="background:var(--c-info-tint);color:var(--c-info)">MECHANISM</span> <span class="pill" style="background:var(--c-seq-tint);color:var(--c-seq)">DISTINCTION</span> <span class="pill" style="background:var(--c-warn-tint);color:var(--c-warn)">CLINICAL</span>.</p>
      <p><span class="pill" style="background:var(--c-corr-tint);color:var(--c-corr-ink);border:0.3pt solid var(--c-corr-rule)">CHECK</span> entries with a dashed border mark places where the sources disagree. Both versions are quoted and neither is chosen for you.</p>
    </div>
  </div>

  <h2 class="h2">Where the mid-module split falls</h2>
  <table class="map">
    <thead><tr><th>File</th><th>Printed pages</th><th>How to convert</th><th>Chapters</th></tr></thead>
    <tbody>
      <tr><td>1st half · 4_5875397832227168769.PDF (200 PDF pages)</td><td class="num">1–197</td><td>printed = PDF page − 3</td><td>1–14, and the start of 15</td></tr>
      <tr><td>2nd half · 4_5875397832227168769(1).PDF (238 PDF pages)</td><td class="num">197–433</td><td>printed = PDF page + 196<br><span class="muted">(PDF p. 238 is the closing page, with no number)</span></td><td>the rest of 15, then 16–40</td></tr>
    </tbody>
  </table>
  <p class="small">The split falls <b>inside Chapter 15, Colorectal Cancer</b>, which starts on p. 195. Printed page 197 appears in both files. The page numbers your PDF viewer shows are not the book’s printed page numbers, so always use the printed number in this handout.</p>
  <p class="small"><b>Part A</b> covers Chapters 15–40, the material after the mid-module. <b>Part B</b> holds the additions for earlier chapters, because GIT Others covers mainly first-half topics (drug treatment of peptic ulcer, GIT tumour pathology, foodborne infection and parasitology).</p>
</section>"""


def toc(pages):
    def row(anchor, num, title, subjects, meta):
        p = pages.get(anchor, "")
        return (f'<div class="toc-row"><a href="#{anchor}"><span class="toc-num">{num}</span>'
                f'<span class="toc-text"><span class="toc-title">{esc(title)}</span>'
                f'<span class="toc-subject">{esc(subjects)}</span></span>'
                f'<span class="toc-meta">{esc(meta)}</span>'
                f'<span class="toc-page-no">{p}</span></a></div>')
    rows_a = "".join(row(f"ch-{c['n']}", f"{c['n']:02d}", c["title"], c["subjects"],
                         f"Book {c['book_pages']} · {len(c['items'])} entr{'y' if len(c['items'])==1 else 'ies'}")
                     for c in C["part_a"]["chapters"])
    rows_a += row("checked-none", "—", "Chapters 16–24, 26–40: checked, nothing to add",
                  "Every after-mid chapter compared against GIT Others", "Book pp. 210–433")
    rows_b = "".join(row(f"ch-{c['n']}", f"{c['n']:02d}", c["title"], c["subjects"],
                         f"Book {c['book_pages']} · {len(c['items'])} entr{'y' if len(c['items'])==1 else 'ies'}")
                     for c in C["part_b"]["chapters"])
    rows_c = row("disc-index", "!", "Points to check: sources disagree",
                 "All CHECK entries in one list", "")
    return f"""
<section class="toc-page" id="contents">
  <div class="front-kicker">CONTENTS</div>
  <h1 class="front-title">Contents</h1>
  <p class="lede" style="margin-bottom:var(--sp-3)">Tap an entry to go to it. The page numbers on the right are this handout’s own pages. The book page ranges are printed pages in your main book.</p>
  <div class="toc-part">PART A · AFTER MID-MODULE CHAPTERS</div>
  <div class="toc-list">{rows_a}</div>
  <div class="toc-part toc-part--earlier">PART B · EARLIER-CHAPTER ADDITIONS FOUND IN GIT OTHERS</div>
  <div class="toc-list">{rows_b}</div>
  <div class="toc-part">REVIEW</div>
  <div class="toc-list">{rows_c}</div>
</section>"""


def item_html(it):
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
    tag, _, sub = it["tag"].partition(" · ")
    src = (f'<span class="tag">{esc(tag)}</span>'
           + (f'<span class="sub">{esc(sub.capitalize())}</span>' if sub else '')
           + f'<span class="ref">GIT Others p. {esc(it["others_pages"])}</span>'
           f'<span class="id"><b>{esc(it["id"])}</b></span>'
           f'<span class="id">ledger {", ".join(it["ledger"])}</span>')
    return (f'<div class="item k-{it["kind"]}" id="{it["id"]}">'
            f'<div class="item__body">{body}</div><div class="item__src">{src}</div></div>')


def chapter_html(ch, earlier, first):
    nav = (f"EARLIER CHAPTER {ch['n']} · " if earlier else f"CHAPTER {ch['n']} · ") + ch["title"].upper()
    items = "".join(item_html(i) for i in ch["items"])
    brk = ' style="break-before:page"' if first else ""
    return f"""
<section class="chapter{' earlier' if earlier else ''}" id="ch-{ch['n']}" style="string-set: chapter-label '{esc(nav)}'">
  <div class="ch-head">
    <div class="ch-num">{ch['n']:02d}</div>
    <div class="ch-titles">
      <h2 class="ch-title">{esc(ch['title'])}</h2>
      <div class="ch-sub"><b>{esc(ch['subjects'])}</b> · Main book {esc(ch['book_pages'])}</div>
    </div>
  </div>
  <p class="teach-note">{esc(ch['files_note'])} Teach after finishing this chapter.</p>
  {items}
</section>"""


def part_a():
    P = C["part_a"]
    chs = "".join(chapter_html(c, False, False) for c in P["chapters"])
    noted = [r for r in P["checked_none"] if not r[3].startswith("No matching material")]
    plain = [r for r in P["checked_none"] if r[3].startswith("No matching material")]
    rows = "".join(f"<tr><td class='num'><b>{n:02d}</b></td><td>{esc(t)}</td><td class='num'>{esc(p)}</td><td>{esc(note)}</td></tr>"
                   for n, t, p, note in noted)
    nomatch = "".join(f"<div><b>{n:02d}</b><span>{esc(t)}</span><span class='pp'>{esc(p)}</span></div>"
                      for n, t, p, note in plain)
    return f"""
<section class="part-divider" id="part-a" style="string-set: chapter-label 'PART A · AFTER MID-MODULE'">
  <div class="part-head">
    <div class="part-kicker">{P['kicker']}</div>
    <h1>{esc(P['title'])}</h1>
    <p>{esc(P['intro'])}</p>
  </div>
  {chs}
  <section id="checked-none" style="string-set: chapter-label 'PART A · CHAPTERS CHECKED'">
    <h2 class="h2">Chapters 16–40 with nothing to add</h2>
    <p class="small">Each of these chapters was compared with GIT Others. None has a missing point that belongs in it.</p>
    <p class="small" style="margin-bottom:1mm"><b>GIT Others touches the topic, but your book already covers it:</b></p>
    <table class="map">
      <thead><tr><th>Ch</th><th>Chapter</th><th>Book pages</th><th>Where your book already has it</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p class="small" style="margin-bottom:0"><b>No matching material in GIT Others:</b></p>
    <div class="nomatch">{nomatch}</div>
  </section>
</section>"""


def part_b():
    P = C["part_b"]
    chs = "".join(chapter_html(c, True, False) for c in P["chapters"])
    return f"""
<section class="part-divider" id="part-b" style="string-set: chapter-label 'PART B · EARLIER-CHAPTER ADDITIONS'">
  <div class="part-head part-head--earlier">
    <div class="part-kicker">{P['kicker']} · NOT PART OF THE AFTER-MID-MODULE CHAPTERS</div>
    <h1>{esc(P['title'])}</h1>
    <p>{esc(P['intro'])}</p>
  </div>
  {chs}
  <p class="teach-note">{esc(P['checked_none_note'])}</p>
</section>"""


def disc_index():
    rows = []
    for part, label in (("part_a", "A"), ("part_b", "B")):
        for ch in C[part]["chapters"]:
            for it in ch["items"]:
                if it["kind"] == "discrepancy":
                    rows.append(f"<tr><td class='num'><a href='#{it['id']}'><b>{it['id']}</b></a></td>"
                                f"<td>Part {label} · Ch {ch['n']}</td><td>{esc(it['head'])}</td>"
                                f"<td class='num'>Book p. {it['book_page']} ({it['book_file']} PDF p. {it['book_pdf']}){('<br>also ' + esc(it['also'])) if it.get('also') else ''}</td>"
                                f"<td class='num'>GIT Others p. {esc(it['others_pages'])}</td></tr>")
    return f"""
<section class="front-page" id="disc-index" style="break-before:page; string-set: chapter-label 'POINTS TO CHECK'">
  <div class="front-kicker">REVIEW</div>
  <h1 class="front-title">Points to check</h1>
  <p class="lede">In these places your book and GIT Others disagree, or your book disagrees with itself. Both versions are quoted in the entry and neither is chosen for you. Tap an ID to go to the entry.</p>
  <table class="map"><thead><tr><th>Entry</th><th>Where</th><th>Topic</th><th>Main book</th><th>Source</th></tr></thead>
  <tbody>{''.join(rows)}</tbody></table>
  <p class="end-note">Compiled from GIT Others (47 pages) against both files of YMnotes Digestive System, Version 3 (printed pp. 1–433). Every entry is in the comparison ledger that comes with this handout.</p>
</section>"""


def document(pages):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{esc(C['title'])}</title>
<meta name="author" content="YMnotes">
<meta name="subject" content="Companion handout to YMnotes Digestive System, Version 3">
<link rel="stylesheet" href="handout.css">
</head><body>
{furniture()}
{cover()}
{about()}
{toc(pages)}
{part_a()}
{part_b()}
{disc_index()}
</body></html>"""


# ------------------------------------------------------------------ render
def render(pages, out):
    stage = BUILD / "html"
    stage.mkdir(parents=True, exist_ok=True)
    for f in ("handout.css", "design-tokens.css"):
        shutil.copy2(HERE / f, stage / f)
    if (stage / "assets").exists():
        shutil.rmtree(stage / "assets")
    shutil.copytree(HERE / "assets", stage / "assets")
    (stage / "handout.html").write_text(document(pages), encoding="utf-8")
    shutil.copy2(stage / "handout.html", HERE / "handout.html")   # editable/inspectable copy
    r = subprocess.run(["npx", "--yes", "--quiet", "@vivliostyle/cli", "build",
                        str(stage / "handout.html"), "-o", str(out)],
                       capture_output=True, text=True, cwd=stage)
    log = r.stdout + r.stderr
    if r.returncode or not out.exists():
        sys.exit("vivliostyle failed:\n" + log)
    errs = [l for l in log.splitlines() if "ERROR" in l or "WARN" in l]
    return errs


def anchor_pages(pdf):
    """Read the contents links back from the rendered file: anchor -> page."""
    d = pymupdf.open(pdf)
    found = {}
    for pno in range(d.page_count):
        for l in d[pno].get_links():
            nd = l.get("nameddest") or ""
            m = re.search(r"0023([A-Za-z0-9\-]+)$", nd)
            if m and l.get("page") is not None and l["page"] >= 0:
                key = m.group(1).replace(":002d", "-")
                found.setdefault(key, l["page"] + 1)
    d.close()
    return found


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    raw1, raw2 = BUILD / "pass1.pdf", BUILD / "pass2.pdf"
    errs = render({}, raw1)
    pages = anchor_pages(raw1)
    errs = render(pages, raw2)
    pages2 = anchor_pages(raw2)
    wanted = [f"ch-{c['n']}" for p in ("part_a", "part_b") for c in C[p]["chapters"]] + ["checked-none", "disc-index"]
    missing = [a for a in wanted if a not in pages2]
    if missing:
        sys.exit(f"contents anchors not resolved: {missing}")
    if any(pages[a] != pages2[a] for a in wanted):
        sys.exit(f"contents folios moved between passes: {pages} vs {pages2}")
    print("renderer messages:", errs or "none")

    # adaptive watermark (skill). Cover and contents stay clean.
    wm = BUILD / "wm.pdf"
    r = subprocess.run([sys.executable, str(SKILL / "scripts/apply_watermark.py"), str(raw2), str(wm),
                        str(SKILL / "assets/brand" / BRAND["assets"]["watermark_wordmark"]),
                        "--openers", "0", "--suppress", "1,3", "--report"],
                       capture_output=True, text=True)
    print(r.stdout[-800:], r.stderr[-800:])
    src = wm if (r.returncode == 0 and wm.exists()) else raw2

    # permanent closing page (skill)
    closed = BUILD / "closed.pdf"
    r = subprocess.run([sys.executable, str(SKILL / "scripts/append_final_page.py"), str(src),
                        str(SKILL / "assets/brand" / BRAND["assets"]["final_page"]), str(closed)],
                       capture_output=True, text=True)
    print(r.stdout[-600:], r.stderr[-600:])
    if r.returncode:
        sys.exit("closing page failed")

    # outline
    d = pymupdf.open(closed)
    toc = [[1, "Cover", 1], [1, "About this handout", pages2.get("about", 2) if "about" in pages2 else 2],
           [1, "Contents", 3],
           [1, "Part A · After Mid-Module Chapters", pages2["ch-15"]]]
    for c in C["part_a"]["chapters"]:
        toc.append([2, f"Ch {c['n']} · {c['title']}", pages2[f"ch-{c['n']}"]])
    toc.append([2, "Chapters 16–40 checked (no additions)", pages2["checked-none"]])
    toc.append([1, "Part B · Earlier-Chapter Additions Found in GIT Others", pages2[f"ch-{C['part_b']['chapters'][0]['n']}"]])
    for c in C["part_b"]["chapters"]:
        toc.append([2, f"Ch {c['n']} · {c['title']}", pages2[f"ch-{c['n']}"]])
    toc.append([1, "Points to check", pages2["disc-index"]])
    toc.append([1, "Stay with YMnotes", d.page_count])
    d.set_toc(toc)
    d.set_metadata({"title": C["title"], "author": "YMnotes",
                    "subject": "Companion handout to YMnotes Digestive System, Version 3",
                    "keywords": "YMnotes; digestive system; GIT; companion; after mid-module"})
    d.save(OUT_PDF, garbage=3, deflate=True)
    d.close()
    (BUILD / "anchor-pages.json").write_text(json.dumps(pages2, indent=1), encoding="utf-8")
    print("wrote", OUT_PDF)


if __name__ == "__main__":
    main()
