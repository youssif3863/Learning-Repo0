# Validation record and limits

**Stage 1 (`node scripts/test.cjs`)** — offline, synthetic data only: idempotent replay, conflicting keys, torn-tail recovery to a new journal, source ordering, option attachment, exact duplicates at distinct positions, missing positions, protected output directories, relative asset paths, copied assets, deterministic shuffling, passage groups kept intact, option relabelling, answer remapping (single, multiple, text answers), position-dependent options kept in order, unnumbered output, and refusal of any supplement/AI configuration.

**Stage 2 (`python3 scripts/stage2/stage2.py selftest`)** — builds a synthetic journal, exports it, parses the Markdown, indexes a synthetic book (printed numbers, chapters), validates synthetic answers (and proves that a mistaken answer is rejected), builds Version 1 and Version 2 and runs QA: every question present, no chapter titles in Version 1, every answer linked to its book page, every back-chip landing on its card, every exact answer highlighted, no named destinations left, page counts.

The same pipeline reproduced a delivered 257-question, 475-page-book result exactly (243 links, 221 highlights, 65 groups, identical Version 1 text).

Test success is not evidence that a specific website supports exporting, that images are visually complete, that a book's printed page numbers were detected correctly (read the `index` report), or that the host has browser capabilities. Browser adapters are instruction-level capability mappings, not tested integrations for every host.
