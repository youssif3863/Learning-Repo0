import json, sys
sys.path.insert(0, "src")
import bookindex as B
qs = json.load(open("data/questions_raw.json"))
a, b = int(sys.argv[1]), int(sys.argv[2]); k = int(sys.argv[3]) if len(sys.argv) > 3 else 2
for q in qs[a-1:b]:
    query = q["q"] + " " + " ".join(q["opts"])
    print(f"#{q['id']} [{q['group']}] {q['q'][:95]}")
    for sc, pdf, pr, seg in B.search(query, k=k, width=210):
        print(f"   p.{pr} (pdf {pdf}, {sc}): {seg}")
