# -*- coding: utf-8 -*-
"""Stage 2 · QA of the two finished PDFs. Prints PASS/FAIL lines and returns the list of problems."""
import collections, json, os, re
import pymupdf
from deck import assemble
from book import Book

norm = lambda s: re.sub(r"-\s+", "-", re.sub(r"\s+", " ", s)).strip()


def run(work, out_dir, v1_path, v2_path):
    deck, groups = assemble(work)
    items = [it for g in groups for it in g["items"]]
    rep = json.load(open(os.path.join(out_dir, "stage2_report.json")))
    bk = Book(work)
    problems = []

    def check(ok, msg):
        print(("PASS " if ok else "FAIL ") + msg)
        if not ok:
            problems.append(msg)

    # ---------------------------------------------------------------- Version 1
    v1 = pymupdf.open(v1_path)
    t1 = norm(" ".join(p.get_text("text") for p in v1))
    missing = [it["id"] for it in items if norm(it["q"]) not in t1 or any(norm(o) not in t1 for o in it["opts"])]
    check(not missing, f"V1 contains every question and option ({len(items)} questions)" + (f"; missing {missing[:5]}" if missing else ""))
    check(not re.search(r"Chapter \d+:|Why:|Tell the students", t1), "V1 has no chapter titles or answer text")
    check(len(v1) >= len(groups), f"V1 pages {len(v1)} ≥ groups {len(groups)}")
    heads = len(re.findall(r"Group [A-Z]{1,2}(?=\s)", t1))
    check(heads >= len(groups), f"V1 shows {heads} group headings for {len(groups)} groups")

    # ---------------------------------------------------------------- Version 2
    v2 = pymupdf.open(v2_path)
    n_ans, with_book = rep["answer_pages"], rep["with_book"]
    t2 = norm(" ".join(v2[i].get_text("text") for i in range(n_ans)))
    miss2 = [it["id"] for it in items if norm(it["q"]) not in t2]
    check(not miss2, f"V2 answer section contains every question" + (f"; missing {miss2[:5]}" if miss2 else ""))
    bad_pos = []
    for p in range(n_ans):
        for lk in v2[p].get_links():
            if lk["kind"] == pymupdf.LINK_GOTO and not (0 <= lk["to"].y <= v2[lk["page"]].rect.height):
                bad_pos.append((p, lk["page"]))
    check(not bad_pos, "all in-document link destinations lie inside their pages")
    check(not any(lk["kind"] == pymupdf.LINK_NAMED for p in range(n_ans) for lk in v2[p].get_links()), "no named-destination links remain (explicit page destinations only)")
    if with_book:
        bs = rep["book_start"]
        exp = collections.Counter(bs + bk.pdf_of(it["pg"]) - 1 for it in items if it["pg"] for _ in it["ans"])
        got = collections.Counter(lk["page"] for p in range(1, n_ans) for lk in v2[p].get_links()
                                  if lk["kind"] == pymupdf.LINK_GOTO and lk["page"] >= bs and lk["from"].width > 60)
        check(exp == got, f"every correct answer links to its own book page ({sum(got.values())} links)")
        back, bad = 0, []
        for p in range(bs, len(v2)):
            for lk in v2[p].get_links():
                if lk["kind"] == pymupdf.LINK_GOTO and lk["page"] < bs:
                    back += 1
                    y = lk["to"].y
                    t = v2[lk["page"]].get_text("text", clip=pymupdf.Rect(0, y, 595, min(y + 45, v2[lk["page"]].rect.height)))
                    lab = v2[p].get_text("text", clip=lk["from"]).strip().replace("\n", "")
                    if not lab or lab not in t.replace("\n", ""):
                        bad.append((p - bs + 1, lab))
        check(back == len({it["id"] for it in items if it["pg"]}) and not bad, f"every back-chip lands on its question card ({back} chips)" + (f"; mismatches {bad[:4]}" if bad else ""))
        nohl = []
        for it in items:
            if it["pg"] and it["exact"] and it["anchor"]:
                pg = v2[bs + bk.pdf_of(it["pg"]) - 1]
                if not list(pg.annots(types=[pymupdf.PDF_ANNOT_HIGHLIGHT])):
                    nohl.append(it["id"])
        check(not nohl, "every exact answer has a highlight on its book page" + (f"; missing {nohl[:5]}" if nohl else ""))
        check(len(v2) == bs + bk.meta["pages"], f"V2 = {bs} answer pages + {bk.meta['pages']} book pages")
    return problems
