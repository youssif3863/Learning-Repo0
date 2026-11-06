# -*- coding: utf-8 -*-
"""Stage 2 · stamps the vector YMnotes logo, a module label, the footer and page numbers onto rendered pages."""
import os
import pymupdf
from deck import BRAND

TEMPLATE = os.path.join(BRAND, "brand_template.pdf")          # vector logo + footer bar/url cut from the original YMnotes PDF
F_REG = os.path.join(BRAND, "fonts", "inter-400.ttf")
F_SEMI = os.path.join(BRAND, "fonts", "inter-600.ttf")
GREEN = (0.10196, 0.35686, 0.19216)
GREY = (0.4, 0.4588, 0.4235)       # #66756C
RULE = (0.8314, 0.8667, 0.8431)    # #D4DDD7
R = 552.8


def text_width(fontfile, text, size):
    return pymupdf.Font(fontfile=fontfile).text_length(text, fontsize=size)


def stamp(doc, labels, right_label, first=0, count=None):
    """labels: {page_index: 'n'}; right_label: header text at the top right."""
    tpl = pymupdf.open(TEMPLATE)
    n = len(doc) - first if count is None else count
    for i in range(first, first + n):
        pg = doc[i]
        pg.show_pdf_page(pymupdf.Rect(50, 24, 200, 52), tpl, 0, clip=pymupdf.Rect(50, 24, 200, 52))
        pg.draw_line((56.7, 53.9), (R, 53.9), color=RULE, width=0.3)
        w = text_width(F_REG, right_label, 7.8)
        pg.insert_text((R - w, 41.06), right_label, fontfile=F_REG, fontname="InterR", fontsize=7.8, color=GREY)
        pg.show_pdf_page(pymupdf.Rect(50, 800, 330, 832), tpl, 0, clip=pymupdf.Rect(50, 800, 330, 832))
        lab = labels.get(i)
        if lab:
            pg.insert_text((R - text_width(F_SEMI, lab, 9.6), 819.9), lab, fontfile=F_SEMI, fontname="InterS", fontsize=9.6, color=GREEN)
