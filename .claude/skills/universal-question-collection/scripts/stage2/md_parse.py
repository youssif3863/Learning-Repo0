# -*- coding: utf-8 -*-
"""Stage 2 · read the Stage-1 Markdown (questions_shuffled.md) into questions.json."""
import json, os, re, sys

UNAVAILABLE = "Not displayed by the source."
OPT = re.compile(r"^([A-Z])\. ?(.*)$")


def _clean(v):
    v = (v or "").strip()
    return None if not v or v == UNAVAILABLE else v


def parse_block(block):
    m = re.search(r"<!--\s*id:\s*([^;>\s]+)\s*(?:;\s*group:\s*([^;>]*?))?\s*(?:;[^>]*)?-->", block)
    if not m:
        raise ValueError("Question block without an <!-- id: ... --> comment")
    qid, group = m.group(1), (m.group(2) or "").strip() or None
    lines = block.split("\n")
    start = next(i for i, l in enumerate(lines) if l.strip() == "## Question") + 1
    body = [l for l in lines[start:] if not l.strip().startswith("<!--")]
    while body and not body[0].strip():
        body.pop(0)
    # passage = leading blockquote
    passage = []
    while body and body[0].startswith(">"):
        passage.append(re.sub(r"^>\s?", "", body.pop(0)))
    passage_text = "\n".join(passage).replace("**Passage** — ", "", 1).strip() or None
    while body and not body[0].strip():
        body.pop(0)
    # options start where A. is followed by B.
    oi = next((i for i in range(len(body) - 1) if OPT.match(body[i]) and body[i].startswith("A.") and body[i + 1].startswith("B.")), None)
    if oi is None:
        raise ValueError(f"{qid}: could not find the option list")
    stem = "\n".join(body[:oi]).strip()
    options, i = [], oi
    while i < len(body) and body[i].strip():
        mm = OPT.match(body[i])
        if mm and not body[i].startswith("   "):
            options.append({"label": mm.group(1), "text": mm.group(2).rstrip()})
        elif options:
            options[-1]["text"] += "\n" + body[i].strip()
        i += 1
    rest = "\n".join(body[i:])
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", rest)
    ans = re.search(r"\*\*Source answer:\*\*\s*(.*)", rest)
    expl = re.search(r"\*\*Source explanation:\*\*\s*(.*)", rest, re.S)
    labels = [o["label"] for o in options]
    if len(options) < 2 or labels != [chr(65 + k) for k in range(len(options))]:
        raise ValueError(f"{qid}: option labels are not A, B, C… in order: {labels}")
    return {"id": qid, "group": group, "passage": passage_text, "stem": stem, "options": options,
            "source_answer": _clean(ans.group(1)) if ans else None,
            "source_explanation": _clean(expl.group(1)) if expl else None, "images": images}


def parse_markdown(text):
    qs = []
    for block in re.split(r"^---\s*$", text, flags=re.M):
        if "## Question" in block:
            qs.append(parse_block(block))
    ids = [q["id"] for q in qs]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate question ids in the Markdown")
    m = re.search(r"Questions:\s*(\d+)", text)
    return qs, (int(m.group(1)) if m else None)


def run(md_path, out_json):
    text = open(md_path, encoding="utf-8").read()
    qs, declared = parse_markdown(text)
    base = os.path.dirname(os.path.abspath(md_path))
    missing = [im for q in qs for im in q["images"] if not os.path.isfile(os.path.join(base, im))]
    os.makedirs(os.path.dirname(os.path.abspath(out_json)), exist_ok=True)
    json.dump({"base_dir": base, "questions": qs}, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"parsed {len(qs)} questions" + (f" (header says {declared})" if declared is not None else ""))
    if declared is not None and declared != len(qs):
        print(f"WARNING: header declares {declared} questions but {len(qs)} were parsed")
    if missing:
        print(f"WARNING: {len(missing)} referenced image file(s) are missing, e.g. {missing[0]}")
    nokey = sum(1 for q in qs if q["source_answer"] is None)
    print(f"source answers present: {len(qs) - nokey}; absent: {nokey} (Stage 2 must determine those from the book)")
    return qs


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
