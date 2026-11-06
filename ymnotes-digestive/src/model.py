# -*- coding: utf-8 -*-
"""Builds the ordered, regrouped question model shared by Version 1 and Version 2.

Order: Part 1 Digestive (Internal Medicine + Surgery), Part 2 Microbiology,
Part 3 Parasitology, Part 4 Pharmacology.  Original relative order is kept inside each part,
and the user's 3-4-5 group-size cycle is restarted at every part.
"""
import json, glob, importlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "data"))
import ans_core

MICRO = set(range(170, 181)) | {256}
PARA = {181} | set(range(182, 191)) | {257}
PHARMA = {9, 10, 17, 23, 38, 43, 47, 48, 86, 92, 95, 101, 109, 213, 245} | set(range(135, 147)) | {92, 95, 101}
CYCLE = [3, 4, 5]

PARTS = [
    ("medsurg", "Part 1", "Digestive System — Internal Medicine & Surgery", "الجهاز الهضمي — باطنة وجراحة"),
    ("micro", "Part 2", "Microbiology", "ميكروبيولوجي"),
    ("para", "Part 3", "Parasitology", "باراسيتولوجي"),
    ("pharma", "Part 4", "Pharmacology", "فارماكولوجي"),
]
TAGS = {"S": ("Surgery", "جراحة"), "M": ("Internal Medicine", "باطنة"),
        "micro": ("Microbiology", "ميكروبيولوجي"), "para": ("Parasitology", "باراسيتولوجي"),
        "pharma": ("Pharmacology", "فارماكولوجي")}
TAGCLASS = {"S": "t-s", "M": "t-m", "micro": "t-mi", "para": "t-pa", "pharma": "t-ph"}


def section_of(qid):
    if qid in PHARMA: return "pharma"
    if qid in MICRO: return "micro"
    if qid in PARA: return "para"
    return "medsurg"


def letters(n):  # 1->A ... 26->Z, 27->AA ...
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def short_src(line):
    if line.startswith("General oncology"): return "General oncology — not covered in the Digestive book"
    if line.startswith("Diaphragm anatomy"): return "Diaphragm anatomy — not covered in the Digestive book"
    return line


def load():
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "ans_[0-9]*.py"))):
        importlib.import_module(os.path.basename(f)[:-3])
    qs = json.load(open(os.path.join(ROOT, "data", "questions_raw.json"), encoding="utf-8"))
    assert len(qs) == 257 and len(ans_core.ANS) == 257
    by_part = {k: [] for k, *_ in PARTS}
    for q in qs:
        e = ans_core.ANS[q["id"]]
        sec = section_of(q["id"])
        tagkey = sec if sec != "medsurg" else e["tag"]
        item = dict(q); item.update(e)
        item["section"] = sec
        item["tagkey"] = tagkey
        item["tag"] = TAGS[tagkey][0]; item["tag_ar"] = TAGS[tagkey][1]; item["tagclass"] = TAGCLASS[tagkey]
        item["src_clean"] = [short_src(s) for s in q["src"]]
        item["orig_group"] = q["group"]
        by_part[sec].append(item)
    groups = []; gno = 0; page_of_group = {}
    for key, pname, en, ar in PARTS:
        items = by_part[key]; i = 0; c = 0
        while i < len(items):
            size = CYCLE[c % 3]; c += 1
            chunk = items[i:i + size]; i += size
            gno += 1
            g = dict(letter=letters(gno), part=key, part_name=en, part_name_ar=ar, part_label=pname,
                     first_in_part=(c == 1), items=chunk, no=gno)
            for pos, it in enumerate(chunk, 1):
                it["group"] = g["letter"]; it["pos"] = pos
            groups.append(g)
    return groups


if __name__ == "__main__":
    gs = load()
    from collections import Counter
    print(len(gs), "groups;", sum(len(g["items"]) for g in gs), "questions")
    print(Counter(g["part"] for g in gs))
    print([ (g["letter"], len(g["items"])) for g in gs][:8], "...", [(g["letter"], len(g["items"]), g["part"]) for g in gs][-12:])
    print("pharma:", sorted(PHARMA), len(PHARMA)); print("micro", len(MICRO), "para", len(PARA))
