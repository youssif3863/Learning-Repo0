import os, sys, re, pymupdf
W = os.environ.get("YM_WORK", "/tmp/ymnotes_work")   # folder that holds book.pdf
doc = pymupdf.open(W + "/book.pdf")
for a in sys.argv[1:]:
    p = int(a)
    t = doc[p - 1].get_text("text")
    t = re.sub(r"\s*\n\s*", " | ", t.strip())
    print(f"=== pdf {p} ===\n{t}\n")
