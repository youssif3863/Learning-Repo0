# -*- coding: utf-8 -*-
"""Stage 2 · the user's book: printed page numbers, chapters, search, page text, compression."""
import json, math, os, pickle, re, sys
import pymupdf

STOP = set("the of a an and or to in is are was were be been for with by on at as from that this these those it its which what who whom how when "
           "where why not no all any following most more less than other only also may can could should would will into has have had does do did "
           "such about according book".split())


def toks(s):
    out = []
    for w in re.findall(r"[a-z0-9]+", s.lower()):
        if w in STOP or len(w) < 2:
            continue
        if len(w) > 4 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.append(w)
    return out


# ------------------------------------------------------------------ printed page numbers
def _zone_numbers(doc, x0, x1):
    nums = []
    for p in doc:
        r = p.rect
        ws = p.get_text("words", clip=pymupdf.Rect(r.width * x0, r.height * 0.92, r.width * x1, r.height))
        t = [w[4] for w in ws if re.fullmatch(r"\d{1,4}", w[4])]
        nums.append(int(t[-1]) if t else None)
    return nums


def _score(nums):
    prev, good = None, 0
    for n in nums:
        if n is None:
            continue
        if prev is not None and 0 < n - prev <= 4:
            good += 1
        prev = n
    return good


def detect_page_numbers(doc):
    zones = {"right": (0.74, 1.0), "center": (0.38, 0.62), "left": (0.0, 0.26)}
    res = {z: _zone_numbers(doc, *rng) for z, rng in zones.items()}
    best = max(res, key=lambda z: (_score(res[z]), z == "right"))
    nums = res[best]
    coverage = sum(1 for n in nums if n is not None) / max(1, len(nums))
    if _score(nums) < 0.3 * len(nums):
        return None, best, coverage            # no usable printed numbering
    return nums, best, coverage


def main_range(nums, n_pages):
    """First page where numbering restarts (appendix / duplicated back matter)."""
    high = 0
    for i, n in enumerate(nums):
        if n is None:
            continue
        if high >= 20 and n < high - 5:
            return i
        high = max(high, n)
    return n_pages


# ------------------------------------------------------------------ chapters
CH_LINE = re.compile(r"^(?:CHAPTER|Chapter|UNIT|Unit|MODULE|Module)\s*(?P<num>\d{1,3}|[IVXLC]+)\b\s*[:.\-–—]?\s*(?P<title>.*)$")
_SPACED = re.compile(r"\b(?:\w ){2,}\w\b")


def _despace(line):
    """'C H A P T E R 0 1' -> 'CHAPTER01' (letter-spaced display type)."""
    return _SPACED.sub(lambda m: m.group(0).replace(" ", ""), line.strip())


_SMALL = {"and", "of", "the", "in", "to", "for", "on", "a", "an", "or", "with"}


def _nice(title):
    """ALL-CAPS display titles -> Title Case (small words stay lower-case)."""
    t = re.sub(r"\s+", " ", title).strip()
    if t.isupper():
        w = t.lower().split(" ")
        t = " ".join(x if (k and x in _SMALL) else x.capitalize() for k, x in enumerate(w))
    return t


def detect_chapters(doc, main_end, regex=None):
    rx = re.compile(regex) if regex else CH_LINE          # custom regex needs named groups: num, title
    out = []
    for i in range(min(main_end, len(doc))):
        lines = [_despace(l) for l in doc[i].get_text("text")[:500].split("\n") if l.strip()][:6]
        for j, l in enumerate(lines):
            m = rx.match(l)
            if not m:
                continue
            parts = [(m.group("title") or "").strip()]
            for nxt in lines[j + 1:j + 4]:                 # titles often wrap over two or three lines
                if re.fullmatch(r"[\d\W]*", nxt) or "·" in nxt or len(nxt) > 60 or nxt.rstrip().endswith("."):
                    break
                parts.append(nxt.strip())
            title = _nice(" ".join(p for p in parts if p))
            out.append({"num": m.group("num"), "title": title, "pdf_page": i + 1})
            break
    if len(out) >= 2:
        return out
    toc = [t for t in doc.get_toc(simple=True) if t[0] == 1 and t[2] <= main_end]
    return [{"num": None, "title": t[1], "pdf_page": t[2]} for t in toc]


def chapter_label(ch):
    if not ch:
        return None
    n = ch["num"]
    num = f"Chapter {int(n):02d}" if n and str(n).isdigit() else (f"Chapter {n}" if n else None)
    return f"{num}: {ch['title']}" if num and ch["title"] else (num or ch["title"])


# ------------------------------------------------------------------ index build / load
def prepare(book_path, work):
    doc = pymupdf.open(book_path)
    n = len(doc)
    nums, zone, coverage = detect_page_numbers(doc)
    main_end = main_range(nums, n) if nums else n
    pmap = {}
    for i in range(n):
        pmap[str(i + 1)] = str(nums[i]) if nums and nums[i] is not None else None
    chapters = detect_chapters(doc, main_end)
    pages = [p.get_text("text") for p in doc]
    df, ptoks = {}, []
    for i, t in enumerate(pages):
        tk = toks(t) if i < main_end else []
        ptoks.append(tk)
        for w in set(tk):
            df[w] = df.get(w, 0) + 1
    N = max(1, main_end)
    idf = {w: math.log(1 + (N - d + .5) / (d + .5)) for w, d in df.items()}
    no_text = [i + 1 for i, t in enumerate(pages) if not t.strip()]
    os.makedirs(work, exist_ok=True)
    json.dump(pmap, open(os.path.join(work, "page_map.json"), "w"))
    json.dump(chapters, open(os.path.join(work, "chapters.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    meta = {"book": os.path.abspath(book_path), "pages": n, "main_end": main_end, "number_zone": zone if nums else None,
            "numbered_pages": sum(1 for v in pmap.values() if v), "chapters": len(chapters), "no_text_pages": len(no_text),
            "size_mb": round(os.path.getsize(book_path) / 1048576, 1)}
    json.dump(meta, open(os.path.join(work, "book_meta.json"), "w"), indent=1)
    pickle.dump({"pages": pages, "ptoks": ptoks, "idf": idf}, open(os.path.join(work, "book_index.pkl"), "wb"))
    print(json.dumps(meta, indent=1))
    if not nums:
        print("WARNING: no printed page numbers detected. Chips and links will use PDF page numbers; tell the user.")
    if main_end < n:
        print(f"NOTE: numbering restarts at PDF page {main_end + 1}; later pages are treated as back matter (not searched, not cited).")
    if no_text:
        print(f"NOTE: {len(no_text)} page(s) have no text layer (figures/handwriting/scans), e.g. PDF pages {no_text[:8]}. Their content is invisible to search; view them with `page --png` when needed.")
    if not chapters:
        print("WARNING: no chapters detected; chapter lines will show only the book title. Set chapter_regex in deck.json if the book has chapter openers.")
    return meta


class Book:
    def __init__(self, work):
        self.work = work
        self.pmap = json.load(open(os.path.join(work, "page_map.json")))
        self.meta = json.load(open(os.path.join(work, "book_meta.json")))
        self.chapters = json.load(open(os.path.join(work, "chapters.json"), encoding="utf-8"))
        self._idx = None
        self.main_end = self.meta["main_end"]
        self.inv = {}
        for k, v in sorted(self.pmap.items(), key=lambda kv: int(kv[0])):
            if v and int(k) <= self.main_end and v not in self.inv:
                self.inv[v] = int(k)
        self.numbered = self.meta["numbered_pages"] > 0

    @property
    def idx(self):
        if self._idx is None:
            self._idx = pickle.load(open(os.path.join(self.work, "book_index.pkl"), "rb"))
        return self._idx

    def pdf_of(self, printed):
        """printed page label (str) -> 1-based PDF page, or None. Without numbering the label IS the PDF page."""
        if self.numbered:
            return self.inv.get(str(printed))
        return int(printed) if str(printed).isdigit() and 1 <= int(printed) <= self.meta["pages"] else None

    def printed(self, pdf_page):
        v = self.pmap.get(str(pdf_page))
        if v:
            return v
        j = pdf_page - 1
        while j > 0 and not self.pmap.get(str(j)):
            j -= 1
        b = self.pmap.get(str(j))
        return (str(int(b) + (pdf_page - j)) + "~") if b and b.isdigit() else str(pdf_page)

    def chapter_of(self, pdf_page):
        cur = None
        for ch in self.chapters:
            if ch["pdf_page"] <= pdf_page:
                cur = ch
            else:
                break
        return cur

    def search(self, query, k=2, win=4, width=230, extra_pages=False):
        D = self.idx
        qs = set(toks(query))
        avg = sum(len(t) for t in D["ptoks"]) / max(1, len(D["ptoks"]))
        res = []
        for i, tk in enumerate(D["ptoks"]):
            if not tk:
                continue
            tf = {}
            for w in tk:
                tf[w] = tf.get(w, 0) + 1
            sc = sum(D["idf"][w] * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * len(tk) / avg)) for w in qs if (f := tf.get(w, 0)))
            res.append((sc, i))
        res.sort(reverse=True)
        out = []
        for sc, i in res[:k]:
            lines = [l.strip() for l in D["pages"][i].split("\n") if l.strip()]
            best = (0, 0)
            for a in range(max(1, len(lines) - win + 1)):
                s = sum(D["idf"].get(w, 0) for w in set(toks(" ".join(lines[a:a + win]))) & qs)
                if s > best[0]:
                    best = (s, a)
            out.append((round(sc, 1), i + 1, self.printed(i + 1), " ".join(lines[best[1]:best[1] + win])[:width]))
        return out

    def grep(self, pattern, limit=5):
        rx = re.compile(pattern, re.I)
        out = []
        for i, t in enumerate(self.idx["pages"][:self.main_end]):
            flat = re.sub(r"\s+", " ", t)
            m = rx.search(flat)
            if m:
                out.append((self.printed(i + 1), i + 1, flat[max(0, m.start() - 110):m.end() + 150]))
                if len(out) >= limit:
                    break
        return out


# ------------------------------------------------------------------ cli helpers
def cmd_retrieve(work, a, b, k=2, width=230):
    qd = json.load(open(os.path.join(work, "questions.json"), encoding="utf-8"))["questions"]
    bk = Book(work)
    for n, q in enumerate(qd[a - 1:b], a):
        opts = " | ".join(f'{o["label"]}. {o["text"]}' for o in q["options"])
        print(f'#{n} [{q["id"]}] {q["stem"][:240]}\n   OPTIONS: {opts[:420]}' + (f'\n   SOURCE ANSWER: {q["source_answer"]}' if q["source_answer"] else ""))
        for sc, pdf, pr, seg in bk.search(q["stem"] + " " + " ".join(o["text"] for o in q["options"]), k=k, width=width):
            print(f"   p.{pr} (pdf {pdf}, {sc}): {seg}")


def cmd_page(work, pages, png=None):
    meta = json.load(open(os.path.join(work, "book_meta.json")))
    doc = pymupdf.open(meta["book"])
    for p in pages:
        if png:
            doc[p - 1].get_pixmap(dpi=70).save(png if len(pages) == 1 else png.replace(".png", f"_{p}.png"))
            print("saved image for pdf page", p)
        else:
            print(f"=== pdf {p} ===\n" + re.sub(r"\s*\n\s*", " | ", doc[p - 1].get_text("text").strip()) + "\n")


def compress(src, dst, dpi=150, quality=72):
    d = pymupdf.open(src)
    d.rewrite_images(dpi_threshold=dpi + 30, dpi_target=dpi, quality=quality, lossy=True, lossless=True, bitonal=True, color=True, gray=True)
    d.save(dst, garbage=4, deflate=True, clean=True, use_objstms=True)
    return os.path.getsize(dst)
