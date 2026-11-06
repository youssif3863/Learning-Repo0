# -*- coding: utf-8 -*-
"""Stamps the original YMnotes header (vector logo) and footer onto generated pages."""
import os, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "assets", "header_footer_template.pdf")
TEMPLATE_LOGO = os.path.join(ROOT, "assets", "header_logo_template.pdf")
F_REG = os.path.join(ROOT, "assets", "fonts", "inter-400.ttf")
F_SEMI = os.path.join(ROOT, "assets", "fonts", "inter-600.ttf")
GREEN = (0.10196, 0.35686, 0.19216)
GREY = (0.4, 0.4588, 0.4235)       # #66756C
RULE = (0.8314, 0.8667, 0.8431)    # #D4DDD7
R = 552.8


def _w(fontfile, text, size):
    return pymupdf.Font(fontfile=fontfile).text_length(text, fontsize=size)


def stamp(doc, page_numbers, right_label=None, first=0, count=None):
    """page_numbers: dict page_index -> label (str) or None. right_label: None = keep original header text."""
    tpl = pymupdf.open(TEMPLATE)
    tpl_logo = pymupdf.open(TEMPLATE_LOGO)
    n = len(doc) if count is None else count
    for i in range(first, first + n):
        pg = doc[i]
        if right_label is None:
            pg.show_pdf_page(pymupdf.Rect(0, 0, 595.2756, 58), tpl, 0, clip=pymupdf.Rect(0, 0, 595.2756, 58))
        else:
            pg.show_pdf_page(pymupdf.Rect(50, 24, 200, 52), tpl_logo, 0, clip=pymupdf.Rect(50, 24, 200, 52))
            pg.draw_line((56.7, 53.9), (R, 53.9), color=RULE, width=0.3)
            wlab = _w(F_REG, right_label, 7.8)
            pg.insert_text((R - wlab, 41.06), right_label, fontfile=F_REG, fontname="InterR", fontsize=7.8, color=GREY)
        pg.show_pdf_page(pymupdf.Rect(50, 800, 330, 832), tpl, 0, clip=pymupdf.Rect(50, 800, 330, 832))
        lab = page_numbers.get(i)
        if lab:
            w = _w(F_SEMI, lab, 9.6)
            pg.insert_text((R - w, 819.9), lab, fontfile=F_SEMI, fontname="InterS", fontsize=9.6, color=GREEN)
