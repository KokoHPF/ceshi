#!/usr/bin/env python3
"""图 1 三个阶段标题、图 3 “After taping” 改为中文。用法：python3 relabel.py <原图目录> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'


def fill(d, box, im, ref):
    # 用 ref 点（面板背景）的颜色填充
    d.rectangle(box, fill=im.getpixel(ref))


im = Image.open(f'{SRC}/f1.png').convert('RGB')
s = im.width / 520
S = lambda *v: tuple(round(x * s) for x in v)
d = ImageDraw.Draw(im)
fill(d, S(28, 10, 505, 98), im, S(500, 95))
fill(d, S(28, 175, 480, 208), im, S(30, 212))
fill(d, S(28, 565, 480, 600), im, S(30, 603))
f1 = ImageFont.truetype(F, round(19 * s)); f2 = ImageFont.truetype(F, round(14.5 * s))
W = (255, 255, 255)
d.text(S(32, 14), '第一阶段', font=f1, fill=W, stroke_width=1, stroke_fill=W)
d.text(S(32, 46), '肩胛骨上回旋引导练习 + 肩袖肌群等长练习', font=f2, fill=W)
d.text(S(32, 175), '第二阶段　佩戴 8 字贴扎进行练习', font=f1, fill=W, stroke_width=1, stroke_fill=W)
d.text(S(32, 565), '第三阶段　不贴扎的练习', font=f1, fill=W, stroke_width=1, stroke_fill=W)
im.save(f'{OUT}/g1.png')

im = Image.open(f'{SRC}/f3.png').convert('RGB')
s = im.width / 900
S = lambda *v: tuple(round(x * s) for x in v)
d = ImageDraw.Draw(im)
d.rounded_rectangle(S(392, 235, 522, 268), radius=round(4 * s), fill=(196, 75, 30))
f = ImageFont.truetype(F, round(19 * s))
t = '贴扎后'
d.text((S(457, 0)[0] - d.textlength(t, font=f) / 2, S(0, 241)[1]), t, font=f, fill=W)
im.save(f'{OUT}/g3.png')
print('done')
