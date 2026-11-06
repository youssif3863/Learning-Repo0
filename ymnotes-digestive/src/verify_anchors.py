import os, sys, json, glob, importlib, pymupdf
sys.path.insert(0, "data"); sys.path.insert(0, "src")
W = os.environ.get("YM_WORK", "/tmp/ymnotes_work")   # folder that holds book.pdf
pm = json.load(open("data/page_map.json"))
inv = {}
for k, v in pm.items():
    if v and v.isdigit() and int(k) < 447: inv[v] = int(k)
import ans_core
for f in sorted(glob.glob("data/ans_[0-9]*.py")):
    importlib.import_module(f.split("/")[-1][:-3])
qs = {q["id"]: q for q in json.load(open("data/questions_raw.json"))}
doc = pymupdf.open(W + "/book.pdf")
bad = 0
for i, e in sorted(ans_core.ANS.items()):
    q = qs[i]
    if e["ans"] not in "ABCDE"[:len(q["opts"])]: print(f"#{i}: bad letter {e['ans']}"); bad += 1
    wrong = set("ABCDE"[:len(q["opts"])]) - {e["ans"]}
    if set(e["wrong"]) != wrong: print(f"#{i}: wrong-option keys {sorted(e['wrong'])} != {sorted(wrong)}"); bad += 1
    if e["pg"]:
        if e["pg"] not in inv: print(f"#{i}: page {e['pg']} not found"); bad += 1; continue
        if e["anchor"]:
            hits = doc[inv[e["pg"]] - 1].search_for(e["anchor"])
            if not hits: print(f"#{i}: anchor not found on p.{e['pg']}: {e['anchor']!r}"); bad += 1
print("entries:", len(ans_core.ANS), "problems:", bad)
