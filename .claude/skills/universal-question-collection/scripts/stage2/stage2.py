#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage 2 command line. Usage: python3 stage2.py <command> …   (run with no arguments for the list)

  doctor                               check python / PyMuPDF / node / playwright / chromium / fonts
  init   WORK [--label L] [--book-title T]   create the work folder with deck.json and answers/
  parse  QUESTIONS.md WORK/questions.json     read the Stage 1 Markdown
  index  BOOK.pdf WORK                  printed page numbers, chapters, search index
  show   WORK A B                       print questions A..B (1-based) in full
  retrieve WORK A B [-k 2]              questions A..B with the best book pages for each
  search WORK "query" [-k 3]            search the book text
  grep   WORK REGEX…                    find a regular expression in the book (printed page + context)
  page   WORK N… [--png FILE]           text (or an image) of PDF page(s) N
  validate WORK [--strict]              check answer files against the questions and the book
  build  WORK OUTDIR [--no-book] [--only v1|v2]   build Version 1 and Version 2
  qa     WORK OUTDIR                    verify counts, links, highlights
  selftest                              build everything from synthetic data
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def need(argv, n, usage):
    if len(argv) < n:
        raise SystemExit("usage: stage2.py " + usage)


def doctor():
    ok = True
    print(f"python {sys.version.split()[0]}")
    try:
        import pymupdf
        print("PyMuPDF", pymupdf.__doc__.split(":")[0].replace("PyMuPDF ", ""))
    except Exception as e:
        ok = False; print("MISSING PyMuPDF -> pip install pymupdf")
    for tool in ("node",):
        p = shutil.which(tool)
        print(tool, p or "MISSING"); ok &= bool(p)
    r = subprocess.run(["node", "-e", "require('playwright'); console.log('playwright module ok')"], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip()[:120]); ok &= r.returncode == 0
    if r.returncode == 0:
        r = subprocess.run(["node", "-e", "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();await b.close();console.log('chromium launches')})().catch(e=>{console.log('chromium FAILED: '+e.message.split('\\n')[0]);process.exit(1)})"], capture_output=True, text=True)
        print(r.stdout.strip()); ok &= r.returncode == 0
    from deck import BRAND
    for f in ("brand_template.pdf", "fonts/inter-latin-400-normal.woff2", "fonts/noto-sans-arabic-arabic-400-normal.woff2", "fonts/inter-600.ttf"):
        e = os.path.exists(os.path.join(BRAND, f)); ok &= e
        if not e: print("MISSING brand asset", f)
    print("READY" if ok else "NOT READY — fix the items above (pip install pymupdf; npm i -g playwright && npx playwright install chromium)")
    return 0 if ok else 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); return 0
    cmd, a = argv[0], argv[1:]
    flag = lambda name, default=None: (a[a.index(name) + 1] if name in a else default)
    if cmd == "doctor":
        return doctor()
    if cmd == "init":
        need(a, 1, "init WORK [--label L] [--book-title T]")
        from deck import ASSETS
        os.makedirs(os.path.join(a[0], "answers"), exist_ok=True)
        deck = json.load(open(os.path.join(ASSETS, "deck.json"), encoding="utf-8"))
        if flag("--label"): deck["module_label"] = flag("--label")
        if flag("--book-title"): deck["book_title"] = flag("--book-title")
        if flag("--prefix"): deck["file_prefix"] = flag("--prefix")
        json.dump(deck, open(os.path.join(a[0], "deck.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("created", os.path.join(a[0], "deck.json"), "and answers/"); return 0
    if cmd == "parse":
        need(a, 2, "parse QUESTIONS.md WORK/questions.json")
        import md_parse; md_parse.run(a[0], a[1]); return 0
    if cmd == "index":
        need(a, 2, "index BOOK.pdf WORK")
        import book; book.prepare(a[0], a[1]); return 0
    if cmd == "show":
        need(a, 3, "show WORK A B")
        qd = json.load(open(os.path.join(a[0], "questions.json"), encoding="utf-8"))["questions"]
        for n, q in enumerate(qd[int(a[1]) - 1:int(a[2])], int(a[1])):
            print(f'#{n} [{q["id"]}]' + (f' (passage) {q["passage"][:300]}' if q["passage"] else "") + f'\n{q["stem"]}')
            for o in q["options"]: print(f'  {o["label"]}. {o["text"]}')
            if q["source_answer"]: print("  SOURCE ANSWER:", q["source_answer"], "|", (q["source_explanation"] or "")[:200])
            print()
        return 0
    if cmd == "retrieve":
        need(a, 3, "retrieve WORK A B [-k 2]")
        import book; book.cmd_retrieve(a[0], int(a[1]), int(a[2]), int(flag("-k", 2))); return 0
    if cmd == "search":
        need(a, 2, 'search WORK "query" [-k 3]')
        import book
        for r in book.Book(a[0]).search(a[1], k=int(flag("-k", 3))): print(r)
        return 0
    if cmd == "grep":
        need(a, 2, "grep WORK REGEX…")
        import book
        bk = book.Book(a[0])
        for pat in a[1:]:
            print(f"--- /{pat}/")
            for pr, pdf, ctx in bk.grep(pat): print(f"  p.{pr} (pdf {pdf}): …{ctx}…")
        return 0
    if cmd == "page":
        need(a, 2, "page WORK N… [--png FILE]")
        import book
        pages = [int(x) for x in a[1:] if x.isdigit()]
        book.cmd_page(a[0], pages, flag("--png")); return 0
    if cmd == "validate":
        need(a, 1, "validate WORK [--strict]")
        import deck
        errs, _ = deck.validate(a[0], strict="--strict" in a); return 1 if errs else 0
    if cmd == "build":
        need(a, 2, "build WORK OUTDIR [--no-book] [--only v1|v2]")
        return cmd_build(a[0], a[1], with_book="--no-book" not in a, only=flag("--only"))
    if cmd == "qa":
        need(a, 2, "qa WORK OUTDIR")
        import qa
        rep = json.load(open(os.path.join(a[1], "stage2_report.json")))
        return 1 if qa.run(a[0], a[1], rep["v1_path"], rep["v2_path"]) else 0
    if cmd == "selftest":
        import selftest; return selftest.run()
    print("unknown command:", cmd); print(__doc__); return 2


def cmd_build(work, out, with_book=True, only=None):
    import deck as D, v1, v2, book
    deck_cfg = D.load_deck(os.path.join(work, "deck.json"))
    errs, warns = D.validate(work, verbose=True)
    if errs:
        print(f"\n{len(errs)} answer error(s): fix them first (nothing was built)."); return 1
    deck_cfg, groups = D.assemble(work, deck_cfg)
    bk = book.Book(work)
    os.makedirs(out, exist_ok=True)
    prefix = deck_cfg["file_prefix"]
    rep = {"groups": len(groups), "questions": sum(len(g["items"]) for g in groups)}
    p1 = os.path.join(out, f"{prefix}_V1_Students.pdf")
    p2 = os.path.join(out, f"{prefix}_V2_Answers_with_Book.pdf" if with_book else f"{prefix}_V2_Answer_Key.pdf")
    rep["v1_path"], rep["v2_path"] = p1, p2
    if only in (None, "v1"):
        rep["v1"] = v1.build(groups, deck_cfg, p1, work); print("Version 1:", rep["v1"], "->", p1)
    if only in (None, "v2"):
        rep["v2"] = v2.build(groups, deck_cfg, work, p2, bk, with_book=with_book)
        rep["answer_pages"], rep["with_book"], rep["book_start"] = rep["v2"]["answer_pages"], with_book, rep["v2"]["book_start"]
        print("Version 2:", rep["v2"], "->", p2)
    items = [it for g in groups for it in g["items"]]
    rep["flags"] = {"notes": [it["id"] for it in items if it["note"]], "not_in_book": [it["id"] for it in items if not it["pg"]],
                    "nearest_page": [it["id"] for it in items if it["pg"] and not it["exact"]]}
    json.dump(rep, open(os.path.join(out, "stage2_report.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
