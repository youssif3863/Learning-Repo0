# YMnotes — Digestive mid-module questions (V1 students / V2 answer key + book)

Source of the two PDFs delivered to the teacher.

| Output | What it is |
|---|---|
| `output/YMnotes_Digestive_Mid_Module_Questions_V1_Students.pdf` | Same design as the original, **no chapter titles**; 65 groups (A–BM, 3-4-5 cycle); pharma questions collected at the end. |
| `YMnotes_Digestive_Mid_Module_V2_Answers_with_Book.pdf` (not committed, ~48 MB) | Answer key with EN/AR explanations, subject tags, chapter titles; the 475-page book is merged at the end and every correct answer links to a highlighted line in it. Rebuild with the commands below. |

## Layout of the repo folder
- `data/questions_raw.json` – the 257 questions parsed from the original PDF.
- `data/ans_*.py` – the answer content for every question (correct option, why right / why others wrong in EN+AR, teaching pearl, book page + highlight phrase).
- `data/page_map.json` – book PDF page → printed (bottom-right) page number.
- `src/model.py` – regrouping: Part 1 Medicine & Surgery, Part 2 Microbiology, Part 3 Parasitology, Part 4 Pharmacology (3-4-5 cycle restarts per part).
- `src/build_v1.py`, `src/build_v2.py`, `src/stamp.py` – HTML → PDF with Chromium (Playwright), then PyMuPDF for header/footer, links, highlights, back-chips, bookmarks.
- `src/verify_anchors.py`, `tools/qa_v2.py` – checks that every cited page/phrase exists and that all links land correctly.
- `assets/` – Inter, Archivo, Source Serif 4, Noto Sans Arabic (OFL) and the vector YMnotes header/footer cut from the original PDF.

## Rebuild
```bash
pip install pymupdf fonttools brotli          # plus Node + playwright (chromium)
python3 src/parse_questions.py <pdftotext -raw of the original>.txt data/questions_raw.json   # only if re-parsing
python3 src/build_v1.py
python3 tools/compress_book.py <book.pdf> /tmp/ymnotes_work/book_small.pdf 150 72           # optional: ~120 MB -> ~44 MB
YM_WORK=/tmp/ymnotes_work YM_BOOK=/tmp/ymnotes_work/book_small.pdf python3 src/build_v2.py
python3 tools/qa_v2.py
```

## Judgement calls (see the Teacher notes page inside V2)
- "Pharmacology" = questions whose tested fact is a drug's mechanism, kinetics, adverse effect, class or regimen (27 questions).
- Hernia questions come from a separate *Hernia book* that was not supplied, so they have no book link.
- Questions with weak wording or answers that depend on the exam key carry a "Question note".
