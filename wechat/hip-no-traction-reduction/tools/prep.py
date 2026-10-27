#!/usr/bin/env python3
"""把整页渲染的原文图 1～4 切成单幅（去掉图内“Figure:N”字样），X 线上的“RIGHT”改成“右”。
先渲染：E=../../skills/paper-to-xhs-cards/scripts/extract_figures.py
  python3 $E src/paper.pdf work --clip 1 47 46 302 325 f1；--clip 1 312 275 568 587 f2；--clip 2 49 47 302 374 f3；--clip 2 314 364 568 684 f4
用法：python3 prep.py <work 目录> <粗体>"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
W, FB = sys.argv[1:3]
f = {k: Image.open(f'{W}/{k}.jpg').convert('RGB') for k in ('f1', 'f2', 'f3', 'f4')}
P = {'1a': ('f1', (24, 22, 533, 567)), '1b': ('f1', (536, 22, 1038, 567)), '1c': ('f1', (24, 576, 533, 1056)), '1d': ('f1', (536, 576, 1038, 1056)),
     '2a': ('f2', (18, 18, 529, 422)), '2b': ('f2', (535, 18, 1041, 422)), '2c': ('f2', (18, 434, 529, 859)), '2d': ('f2', (535, 434, 1041, 859)),
     '2e': ('f2', (18, 869, 529, 1225)), '2f': ('f2', (535, 869, 1041, 1225)),
     '3a': ('f3', (16, 23, 1038, 679)), '3b': ('f3', (16, 695, 1038, 1265)), '4a': ('f4', (10, 24, 1035, 668)), '4b': ('f4', (10, 681, 1035, 1245))}
RIGHT = {'3a': (5, 8, 108, 47), '3b': (44, 306, 142, 343)}  # OCR 定位
for k, (src, box) in P.items():
    im = f[src].crop(box)
    if k in RIGHT:
        x0, y0, x1, y1 = RIGHT[k]; a = np.asarray(im).copy(); m = np.zeros(a.shape[:2], np.uint8)
        g = a[y0:y1, x0:x1].mean(2); m[y0:y1, x0:x1] = (g > np.percentile(g, 55)).astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((5, 5), np.uint8)); im = Image.fromarray(cv2.inpaint(a, m, 7, cv2.INPAINT_TELEA))
        d = ImageDraw.Draw(im)
        d.text((x0 + 4, y0 - 2), '右', font=ImageFont.truetype(FB, 34), fill=(235, 235, 235))
    im.save(f'{W}/p{k}.jpg', quality=93)
print('ok', len(P))
