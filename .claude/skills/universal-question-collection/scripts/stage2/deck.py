# -*- coding: utf-8 -*-
"""Stage 2 · deck configuration, answer files (load + validate) and the grouped model used by both PDFs."""
import glob, json, os, re, sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))
ASSETS = os.path.join(SKILL, "assets")
BRAND = os.path.join(ASSETS, "brand")
AR = re.compile(r"[؀-ۿ]")


# ------------------------------------------------------------------ config
def load_deck(path=None):
    deck = json.load(open(os.path.join(ASSETS, "deck.json"), encoding="utf-8"))
    if path and os.path.isfile(path):
        user = json.load(open(path, encoding="utf-8"))
        for k, v in user.items():
            if k in ("tags",) and isinstance(v, dict):
                deck["tags"].update(v)
            else:
                deck[k] = v
    used = {t for p in deck["parts"] for t in p["tags"]}
    missing = set(deck["tags"]) - used
    if missing:
        raise ValueError(f"deck.json: tags not placed in any part: {sorted(missing)}")
    return deck


def letters(n):  # 1 -> A … 26 -> Z, 27 -> AA …
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


# ------------------------------------------------------------------ answers
def load_answers(work):
    files = sorted(glob.glob(os.path.join(work, "answers", "*.json")))
    out = {}
    for f in files:
        data = json.load(open(f, encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"{f}: expected a JSON array of answer objects")
        for a in data:
            if a["id"] in out:
                raise ValueError(f"duplicate answer for {a['id']} (also in {f})")
            out[a["id"]] = a
    return out


def correct_letters(a):
    return [x.strip().upper() for x in re.split(r"[,;&\s]+", a["answer"]) if x.strip()]


def validate(work, strict=False, verbose=True):
    """Hard errors stop the build. Warnings are for the author to review."""
    from book import Book
    qd = json.load(open(os.path.join(work, "questions.json"), encoding="utf-8"))["questions"]
    deck = load_deck(os.path.join(work, "deck.json"))
    ans = load_answers(work)
    bk = Book(work)
    doc = pymupdf.open(bk.meta["book"])
    errs, warns = [], []
    qids = {q["id"] for q in qd}
    for extra in sorted(set(ans) - qids):
        errs.append(f"{extra}: answer for an unknown question id")
    for q in qd:
        a = ans.get(q["id"])
        if not a:
            errs.append(f'{q["id"]}: no answer entry')
            continue
        labels = [o["label"] for o in q["options"]]
        corr = correct_letters(a)
        if not corr or any(c not in labels for c in corr):
            errs.append(f'{q["id"]}: answer {a["answer"]!r} not among {labels}')
            continue
        if set(a.get("wrong", {})) != set(labels) - set(corr):
            errs.append(f'{q["id"]}: wrong-option keys {sorted(a.get("wrong", {}))} != {sorted(set(labels) - set(corr))}')
        if a.get("tag") not in deck["tags"]:
            errs.append(f'{q["id"]}: tag {a.get("tag")!r} not in deck tags {sorted(deck["tags"])}')
        for fld in ("why",):
            v = a.get(fld) or {}
            if not v.get("en") or not v.get("ar") or not AR.search(v["ar"]):
                errs.append(f'{q["id"]}: {fld} needs English and Arabic text')
        for L, v in (a.get("wrong") or {}).items():
            if not v.get("en") or not v.get("ar"):
                errs.append(f'{q["id"]}: wrong[{L}] needs English and Arabic text')
            elif not AR.search(v["ar"]) and len(v["en"].split()) > 4:
                warns.append(f'{q["id"]}: wrong[{L}] Arabic has no Arabic letters (only a Latin term is acceptable for very short reasons)')
        for fld in ("pearl", "note"):
            v = a.get(fld)
            if v and (not v.get("en") or not v.get("ar") or not AR.search(v["ar"])):
                errs.append(f'{q["id"]}: {fld} needs English and Arabic text')
        if len(a["why"]["en"]) > 320: warns.append(f'{q["id"]}: why.en is long ({len(a["why"]["en"])} chars); keep it brief')
        if q["source_answer"] and q["source_answer"].replace(" ", "") != "".join(corr) and q["source_answer"].replace(" ", "") != ",".join(corr) and not a.get("note"):
            errs.append(f'{q["id"]}: differs from the SOURCE answer ({q["source_answer"]}); keep the source answer or add a note explaining the conflict')
        pg = a.get("page")
        if pg:
            pdf = bk.pdf_of(pg)
            if pdf is None:
                errs.append(f'{q["id"]}: printed page {pg!r} not found in the main sequence of the book')
            elif a.get("anchor"):
                if not doc[pdf - 1].search_for(a["anchor"]):
                    errs.append(f'{q["id"]}: anchor not found on book p.{pg}: {a["anchor"]!r}')
            elif a.get("exact", True):
                errs.append(f'{q["id"]}: exact=true needs an anchor phrase (or set exact=false for nearest page)')
            if a.get("exact", True) and not a.get("anchor"):
                pass
        elif a.get("exact"):
            errs.append(f'{q["id"]}: exact=true without a page')
        if not a.get("pearl"): warns.append(f'{q["id"]}: no teaching pearl (fine for trivial questions)')
    n_near = sum(1 for a in ans.values() if a.get("page") and not a.get("exact", True))
    n_nobook = sum(1 for a in ans.values() if not a.get("page"))
    summary = f"{len(ans)}/{len(qd)} answers · {len(errs)} errors · {len([w for w in warns if 'pearl' not in w])} warnings · {n_near} nearest-page · {n_nobook} not in book"
    if verbose:
        for e in errs: print("ERROR  ", e)
        for w in warns:
            if "no teaching pearl" in w and not strict:
                continue
            print("WARNING", w)
        print(summary)
    return errs, warns


# ------------------------------------------------------------------ model
def assemble(work, deck=None):
    from book import Book, chapter_label
    deck = deck or load_deck(os.path.join(work, "deck.json"))
    qd = json.load(open(os.path.join(work, "questions.json"), encoding="utf-8"))
    base = qd.get("base_dir", ".")
    ans = load_answers(work)
    bk = Book(work)
    items = []
    for q in qd["questions"]:
        a = ans[q["id"]]
        tag = a["tag"]
        pdf = bk.pdf_of(a["page"]) if a.get("page") else None
        chap = a.get("chapter") or (chapter_label(bk.chapter_of(pdf)) if pdf else None)
        bt = deck.get("book_title") or ""
        chapter_line = (f"{bt} — {chap}" if bt and chap else (chap or bt)) if pdf else "Not covered in the supplied book"
        exam = q["id"].split("-")[0]
        items.append(dict(
            id=q["id"], q=q["stem"], passage=q["passage"], group_src=(exam + ":" + q["group"]) if q["group"] else None,
            labels=[o["label"] for o in q["options"]], opts=[o["text"] for o in q["options"]],
            images=[os.path.join(base, p) for p in q["images"]],
            ans=correct_letters(a), tag=tag, tagname=deck["tags"][tag]["en"], tagname_ar=deck["tags"][tag]["ar"],
            pg=a.get("page"), anchor=a.get("anchor"), exact=bool(a.get("page")) and a.get("exact", True),
            why=(a["why"]["en"], a["why"]["ar"]),
            wrong={L: (v["en"], v["ar"]) for L, v in (a.get("wrong") or {}).items()},
            pearl=(a["pearl"]["en"], a["pearl"]["ar"]) if a.get("pearl") else None,
            note=(a["note"]["en"], a["note"]["ar"]) if a.get("note") else None,
            chapter_line=chapter_line, pdf_page=pdf, source_answer=q["source_answer"]))
    groups, gno = [], 0
    cycle = deck.get("group_cycle", [3, 4, 5])
    for pi, part in enumerate(deck["parts"]):
        its = [it for it in items if it["tag"] in part["tags"]]
        i = c = 0
        while i < len(its):
            size = cycle[c % len(cycle)]
            c += 1
            j = min(len(its), i + size)
            while j < len(its) and its[j]["group_src"] and its[j]["group_src"] == its[j - 1]["group_src"]:
                j += 1                                  # never split a passage group
            gno += 1
            g = dict(letter=letters(gno), part=part["id"], part_index=pi, part_title=part["title"],
                     part_title_ar=part.get("title_ar", ""), first_in_part=(c == 1), items=its[i:j])
            for pos, it in enumerate(g["items"], 1):
                it["group"], it["pos"], it["part"] = g["letter"], pos, part["id"]
            groups.append(g)
            i = j
    return deck, groups
