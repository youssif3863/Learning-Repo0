# -*- coding: utf-8 -*-
"""Shared registry for the per-question answer content."""
ANS = {}


def a(qid, correct, tag, pg, anchor, why, wrong, pearl=None, note=None):
    """Register the answer for one question.
    tag: 'M' internal medicine, 'S' surgery.
    pg : printed book page as str; '~N' = nearest page (no exact line); None = not in the supplied book.
    """
    exact = True
    if pg and pg.startswith("~"):
        pg = pg[1:]
        exact = False
    ANS[qid] = dict(id=qid, ans=correct, tag=tag, pg=pg, anchor=anchor, exact=exact,
                    why=why, wrong=wrong, pearl=pearl, note=note)
