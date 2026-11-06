# -*- coding: utf-8 -*-
"""Stage 2 · end-to-end self-test on synthetic data (no website, no real book, no network).
Runs Stage 1 export -> parse -> book index -> answer validation -> Version 1 + Version 2 -> QA."""
import base64, json, os, shutil, subprocess, sys, tempfile
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
AR = "نص عربي تجريبي قصير."


def synthetic_book(path, n_facts):
    doc = pymupdf.open()
    doc.new_page(width=595.28, height=841.89).insert_text((60, 120), "Synthetic Book - cover", fontsize=18)
    pages = 8
    for p in range(1, pages + 1):
        pg = doc.new_page(width=595.28, height=841.89)
        y = 100
        if p in (1, 5):
            pg.insert_text((60, y), "C H A P T E R 0 %d" % (1 if p == 1 else 2), fontsize=20)
            pg.insert_text((60, y + 34), "Synthetic Chapter %s" % ("One" if p == 1 else "Two"), fontsize=16)
            y += 90
        for i in range(1, n_facts + 1):
            if (i % pages) + 1 == p or (i % pages == 0 and p == 1):
                pg.insert_text((60, y), f"Fact {i}: the unique token zebra{i} is the answer for topic {i}.", fontsize=11); y += 26
        pg.insert_text((528, 812), str(p), fontsize=10)
    doc.save(path)
    return pages


def page_of(i, pages=8):                      # printed page that holds fact i
    p = (i % pages) + 1
    return p


def run():
    tmp = tempfile.mkdtemp(prefix="uqc_selftest_")
    work, outS1, out = os.path.join(tmp, "work"), os.path.join(tmp, "stage1"), os.path.join(tmp, "out")
    os.makedirs(os.path.join(tmp, "assets")); open(os.path.join(tmp, "assets", "fig1.png"), "wb").write(PNG)
    n = 14
    # ------------------------------------------------ Stage 1 (synthetic journal -> shuffled Markdown)
    recs = []
    for i in range(1, n + 1):
        ch = [{"label": L, "text": f"Option {L} for question {i}"} for L in "ABCD"]
        r = {"exam": "Synthetic exam %d" % (1 if i <= 8 else 2), "position": i if i <= 8 else i - 8, "stem": f"Which statement matches topic {i}?",
             "choices": ch, "answer": None, "answerExplicit": False, "explanation": None, "source": "synthetic", "group": None, "images": [], "issues": []}
        if i % 3 == 0: r.update(answer="B", answerExplicit=True)
        if i == 4: r["choices"][3]["text"] = "All of the above"
        if i in (5, 6, 7): r.update(group="pass1", passage="Shared synthetic passage for questions 5-7.")
        if i == 2: r["images"] = ["assets/fig1.png"]
        recs.append(r)
    journal = os.path.join(tmp, "journal.jsonl")
    open(journal, "w").write("\n".join(json.dumps(r) for r in recs) + "\n")
    cfg = os.path.join(tmp, "config.json"); json.dump({"expected": {}, "date": "2026-01-01", "sourceLocation": "synthetic", "shuffle": True, "shuffleOptions": True, "seed": 7}, open(cfg, "w"))
    r = subprocess.run(["node", os.path.join(SKILL, "scripts", "bank.cjs"), "export", journal, outS1, cfg], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    md = os.path.join(outS1, "questions_shuffled.md")
    assert os.path.exists(md) and os.path.exists(os.path.join(outS1, "assets", "fig1.png"))
    # ------------------------------------------------ Stage 2 parse + book
    sys.path.insert(0, HERE)
    import md_parse, book, deck as D, stage2
    qs = md_parse.run(md, os.path.join(work, "questions.json"))
    assert len(qs) == n
    by_topic = {int(q["stem"].split("topic ")[1].rstrip("?")): q for q in qs}
    assert [o["label"] for o in by_topic[4]["options"]] == list("ABCD") and by_topic[4]["options"][3]["text"] == "All of the above"   # kept in order
    bpath = os.path.join(tmp, "book.pdf"); synthetic_book(bpath, n)
    meta = book.prepare(bpath, work)
    assert meta["number_zone"] == "right" and meta["chapters"] == 2, meta
    bk = book.Book(work)
    assert bk.pdf_of("1") == 2 and book.chapter_label(bk.chapter_of(6)) == "Chapter 02: Synthetic Chapter Two", book.chapter_label(bk.chapter_of(6))
    # ------------------------------------------------ synthetic answer file
    tags = ["S", "M", "MI", "PA", "PH"]
    answers = []
    for k, q in enumerate(qs):
        t = int(q["stem"].split("topic ")[1].rstrip("?"))
        correct = (q["source_answer"] or "A")
        wrong = {o["label"]: {"en": f"Not this one ({o['label']}).", "ar": AR} for o in q["options"] if o["label"] != correct}
        a = {"id": q["id"], "answer": correct, "tag": tags[t % 5], "page": str(page_of(t)), "exact": True, "anchor": f"zebra{t}",
             "why": {"en": f"Fact {t} says so.", "ar": AR}, "wrong": wrong, "pearl": {"en": "Remember topic %d." % t, "ar": AR}, "note": None}
        if t == 9: a.update(exact=False, anchor=None)                       # nearest page only
        if t == 10: a.update(page=None, anchor=None, exact=False)           # not in the book
        if t == 11: a["note"] = {"en": "Synthetic wording issue.", "ar": AR}
        answers.append(a)
    os.makedirs(os.path.join(work, "answers"), exist_ok=True)
    json.dump(answers, open(os.path.join(work, "answers", "ans_001_014.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(dict(D.load_deck(None), module_label="SYNTHETIC / TEST", file_prefix="Selftest", compress_book=False), open(os.path.join(work, "deck.json"), "w", encoding="utf-8"), ensure_ascii=False)
    errs, _ = D.validate(work, verbose=False)
    assert not errs, errs
    # validation must catch mistakes
    bad = json.loads(json.dumps(answers)); keyed = next(a for a, q in zip(bad, qs) if q["source_answer"])
    q_ = next(q for q in qs if q["id"] == keyed["id"]); keyed["answer"] = "A" if q_["source_answer"] != "A" else "B"
    keyed["wrong"] = {o["label"]: {"en": "x", "ar": AR} for o in q_["options"] if o["label"] != keyed["answer"]}
    json.dump(bad, open(os.path.join(work, "answers", "ans_001_014.json"), "w", encoding="utf-8"), ensure_ascii=False)
    errs, _ = D.validate(work, verbose=False); assert any("SOURCE answer" in e for e in errs), errs
    json.dump(answers, open(os.path.join(work, "answers", "ans_001_014.json"), "w", encoding="utf-8"), ensure_ascii=False)
    # ------------------------------------------------ build + QA
    assert stage2.cmd_build(work, out) == 0
    import qa
    rep = json.load(open(os.path.join(out, "stage2_report.json")))
    problems = qa.run(work, out, rep["v1_path"], rep["v2_path"])
    assert not problems, problems
    v1 = pymupdf.open(rep["v1_path"]); v2 = pymupdf.open(rep["v2_path"])
    t1 = " ".join(p.get_text() for p in v1)
    assert "Shared synthetic passage" in t1 and "SYNTHETIC / TEST" in t1 and len(v2) == rep["answer_pages"] + 9
    assert rep["flags"]["not_in_book"] and rep["flags"]["nearest_page"] and rep["flags"]["notes"]
    print(f"\nPASS (Stage 2 self-test): shuffled Markdown -> parse -> index -> validate -> V1 ({len(v1)} pages) + V2 ({len(v2)} pages) -> QA clean. Workspace: {tmp}")
    return 0
