#!/usr/bin/env python3
"""Jayaseelan 2020：图 1 器械商标模糊，图 1、2 等高并排，图 3～5 通栏并加图号（图中仅有 a/b 字母）；封面取自图 1。
用法：python3 make_figs.py <素材目录（x01..x05.png、title.png）> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)


def X(i):
    im = Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')
    if i == 1:  # 器械上的英文商标
        b = (530, 390, 600, 420); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(8)), b[:2])
    return im


def badge(im, t, top=False):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(F, max(26, im.height // 20))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = 10 if top else im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')
a, b = badge(X(1), '图1'), badge(X(2), '图2')
im = Image.new('RGB', (a.width + b.width + 14, a.height), 'white'); im.paste(a, (0, 0)); im.paste(b, (a.width + 14, 0))
save(im, 'img02.jpg')
for k, n in enumerate((3, 4, 5)):
    save(badge(X(n), f'图{n}', top=True), f'img{k + 3:02d}.jpg')
c = X(1); w, h = c.size; ch = round(w * 383 / 900)
c.crop((0, 330, w, 330 + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
