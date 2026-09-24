# YMnotes Digestive System — Integrated Teaching Extras

One chapter-ordered teaching companion to the main book (*YMnotes Digestive System, Version 3*, Chapters 1–40). It merges three finished handouts, rebuilt from their editable sources and ledgers:

- **Before Mid-Module Internal Medicine Extras**, compared with GIT Internal Med;
- **Other Subjects Capsule**, compared with GIT Others;
- **After Mid-Module Hepatology Extras**, compared with the Hepatology source.

**Finished PDF:** [`YMnotes-Digestive-System-Integrated-Teaching-Extras.pdf`](YMnotes-Digestive-System-Integrated-Teaching-Extras.pdf) (A4, 49 pages).

## Folder layout

| Path | What it is |
|---|---|
| `source/chapters.json` | The 40-chapter map of the main book: titles, subject labels, printed page ranges, book file, Part 1 / Part 2. |
| `source/chapter-subjects.json` | The same labels in the skill's contents-contract format. |
| `source/part1-before-mid-module.md` | **Editable content**, Chapters 1–15. |
| `source/part2-after-mid-module.md` | **Editable content**, Chapters 16–40. |
| `source/review-points.md` | **Editable** "Points for Youssef to Review". |
| `source/wording-notes.html` | Notes N1–N5, printed at the end of the review section. |
| `source/method.html` | The closing "Sources, method and traceability" page. Counts are filled in by the build. |
| `build/build.py` | The build: parse → HTML → Chromium (two passes) → page furniture → closing page → bookmarks and page labels. |
| `build/style.css`, `build/render.cjs` | The stylesheet and the Chromium renderer. |
| `build/assets/` | Fonts, brand SVGs, the closing page and the frozen design tokens, all copied from the skill. |
| `build/out/content.json`, `build/out/build-map.json` | Parsed content, destinations, header text per page and the outline. `build.py` rewrites both on every run. |
| `ledger/make_ledger.py` | Builds `ledger/integrated-ledger.{md,csv,json}`. |
| `qa/verify.py` | Checks run on the saved PDF. |
| `qa/run_checks.sh` | Runs `verify.py` and the skill's layout and contents gates. |
| `qa/*.json` | Their results. |
| `qa/contact-sheets/` | Renders of every page. |
| `inputs/` | Frozen copies of the three inputs' editable sources and ledgers, with commit hashes and SHA-256 in `MANIFEST.json`. |
| `REPORT.md` | The completion report. |

## Rebuild

You need:
- Python 3.10+ with `pymupdf`, `pypdf`, `pillow` and `zxing-cpp` (the last one is only for the QR check).
- Node with Playwright and Chromium.
- The **YMnotes medical-book redesign** skill. It supplies `append_final_page.py`, `layout_guard.py` and `contents_contract.py`. If it is not in the default location, set `YMNOTES_SKILL` to its folder.

```bash
cd ymnotes-integrated-extras
python3 build/build.py          # writes the PDF and build/out/*
python3 ledger/make_ledger.py   # regenerates the merged ledger (fails if an included row is unaccounted for)
bash qa/run_checks.sh           # saved-file checks + skill gates
```

The build renders twice. The second pass prints the real folios in the contents and in the review cross-links, and the build stops if pagination moved between the two passes.

## Source grammar

The full grammar is in the docstring at the top of `build/build.py`. In brief:

```
# 03                                        chapter (title etc. from chapters.json)
> note                                      shown on a "no additions" chapter entry
## Topic title | Book pp. 34–36             topic band
::: E03.01 | IM | Title | book=p. 35 | src=GIT Internal Med pp. 21–22 | from=IM:C3-02, IM:C3-03
- bullets, **bold**, *italic*, "Table: caption" + | pipe | rows |
:::
```

- **Subject codes:** `IM` (Internal Medicine), `PHARM`, `PATH`, `MICRO`, `PARA`, `HEP`. Join several with `+`.
- **`from=`:** keeps each entry traceable to the original handout and its ledger rows.
- **Review points:** `::: review Rnn | ch=N | Title | subj=… | from=…`, followed by `A | label | text`, `B | …`, an optional `C | …` and an optional `note | …`.
