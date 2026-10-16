#!/usr/bin/env python3
"""Wohl 2021：图 1 去右侧留白并加图号（图中仅有 A～F 字母）；封面取自图 1 上排。
用法：python3 make_figs.py <素材目录（x01.png、title.png）> <输出目录>"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)

Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)
im = Image.open(f'{SRC}/x01.png').convert('RGB')
g = np.array(im.convert('L')); cols = np.where((g < 235).mean(0) > 0.05)[0]; rows = np.where((g < 235).mean(1) > 0.05)[0]
im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
top = im.crop((0, 0, im.width, im.height // 2))
d = ImageDraw.Draw(im); f = ImageFont.truetype(F, 46); t = '图1'
w = d.textlength(t, font=f) + 24; h = f.size + 16; x = im.width - w - 10; y = im.height - h - 10
d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED); d.text((x + 12, y + 7), t, font=f, fill='white')
im.resize((1080, round(im.height * 1080 / im.width)), Image.LANCZOS).save(f'{OUT}/img02.jpg', quality=88)
w, h = top.size; ch = round(w * 383 / 900); y0 = max(0, (h - ch) // 2)
top.crop((0, y0, w, y0 + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
