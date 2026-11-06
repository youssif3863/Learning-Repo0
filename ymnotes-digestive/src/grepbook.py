import sys, re, json, pymupdf
sys.path.insert(0, "src")
import bookindex as B
D = B.load(); pm = json.load(open("data/page_map.json"))
for pat in sys.argv[1:]:
    print(f"--- /{pat}/")
    n = 0
    for i, t in enumerate(D["pages"]):
        if i + 1 >= 447: continue          # skip back-matter duplicate section
        flat = re.sub(r"\s+", " ", t)
        for m in re.finditer(pat, flat, re.I):
            s = max(0, m.start() - 110); e = min(len(flat), m.end() + 150)
            print(f"  p.{B.printed(pm, i+1)} (pdf {i+1}): …{flat[s:e]}…"); n += 1
            break
        if n >= 5: break
