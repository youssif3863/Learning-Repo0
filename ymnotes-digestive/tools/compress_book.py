import pymupdf, sys, time, os
src, dst = sys.argv[1], sys.argv[2]
dpi_t = int(sys.argv[3]) if len(sys.argv) > 3 else 150
q = int(sys.argv[4]) if len(sys.argv) > 4 else 75
t = time.time()
d = pymupdf.open(src)
print("opened", len(d), "pages", flush=True)
d.rewrite_images(dpi_threshold=dpi_t + 30, dpi_target=dpi_t, quality=q, lossy=True, lossless=True, bitonal=True, color=True, gray=True)
d.save(dst, garbage=4, deflate=True, clean=True, use_objstms=True)
print("saved", dst, os.path.getsize(dst) // 1024 // 1024, "MB in", round(time.time() - t), "s", flush=True)
