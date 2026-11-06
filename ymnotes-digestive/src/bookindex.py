"""Search helper over the book PDF text (kept outside the repo)."""
import os, pymupdf, re, json, math, pickle, os, sys
W = os.environ.get("YM_WORK", "/tmp/ymnotes_work")   # folder that holds book.pdf
CACHE = W + "/bookidx.pkl"
STOP = set("the of a an and or to in is are was were be been for with by on at as from that this these those it its which what who whom how when where why not no all any following most more less than than other only also may can could should would will into has have had does do did such about according book gi".split())
def toks(s):
    out = []
    for w in re.findall(r"[a-z0-9]+", s.lower()):
        if w in STOP or len(w) < 2: continue
        if len(w) > 4 and w.endswith("s") and not w.endswith("ss"): w = w[:-1]
        out.append(w)
    return out
def build():
    doc = pymupdf.open(W + "/book.pdf")
    pages = []
    for p in doc:
        t = p.get_text("text")
        pages.append(t)
    pm = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "page_map.json")))
    df = {}
    ptoks = []
    for t in pages:
        tk = toks(t); ptoks.append(tk)
        for w in set(tk): df[w] = df.get(w, 0) + 1
    N = len(pages)
    idf = {w: math.log(1 + (N - d + .5) / (d + .5)) for w, d in df.items()}
    pickle.dump(dict(pages=pages, ptoks=ptoks, idf=idf), open(CACHE, "wb"))
def load():
    if not os.path.exists(CACHE): build()
    return pickle.load(open(CACHE, "rb"))
def printed(pm, i):  # i = 1-based pdf page; interpolate missing
    v = pm.get(str(i))
    if v: return v
    j = i - 1
    while j > 0 and not pm.get(str(j)): j -= 1
    b = pm.get(str(j))
    return (str(int(b) + (i - j)) + "~") if b and b.isdigit() else "?"
def search(q, k=2, extra=None, win=4, width=260):
    D = load(); idf = D["idf"]; pages = D["pages"]; ptoks = D["ptoks"]
    qt = toks(q); qs = set(qt)
    pm = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "page_map.json")))
    avg = sum(len(t) for t in ptoks) / len(ptoks)
    res = []
    for i, tk in enumerate(ptoks):
        if not tk: continue
        tf = {}
        for w in tk: tf[w] = tf.get(w, 0) + 1
        sc = 0
        for w in qs:
            f = tf.get(w, 0)
            if f: sc += idf[w] * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * len(tk) / avg))
        res.append((sc, i))
    res.sort(reverse=True)
    out = []
    for sc, i in res[:k]:
        lines = [l.strip() for l in pages[i].split("\n") if l.strip()]
        best = (0, 0)
        for a in range(max(1, len(lines) - win + 1)):
            seg = " ".join(lines[a:a + win])
            s = sum(idf.get(w, 0) for w in set(toks(seg)) & qs)
            if s > best[0]: best = (s, a)
        seg = " ".join(lines[best[1]:best[1] + win])
        out.append((round(sc, 1), i + 1, printed(pm, i + 1), seg[:width]))
    return out
if __name__ == "__main__":
    for r in search(" ".join(sys.argv[1:]), k=3): print(r)
