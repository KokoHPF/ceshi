#!/usr/bin/env python3
"""Selman 2022 产后重返运动：图 1 上下两幅改为左右并排；图 2、3 裁掉四周大片留白；图中只有 A～E 字母，未改动；封面取自图 2。
用法：python3 make_figs.py <素材目录（x01～x03.png、title.png）> <输出目录>"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def trim(im, thr=245, pad=4):
    g = np.array(im.convert('L')); ys, xs = np.where(g < thr)
    return im.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + pad), min(im.height, ys.max() + pad)))


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.width // 30))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080, tag=None):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    if tag:
        badge(im, tag)
    im.save(f'{OUT}/{name}', quality=88)


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

# 图 1：A、B 上下排列 → 左右并排
x1 = trim(X(1)); g = np.array(x1.convert('L')); rows = np.where((g < 240).mean(1) < 0.05)[0]
mid = rows[np.argmin(abs(rows - x1.height / 2))]
a = trim(x1.crop((0, 0, x1.width, mid))); b = trim(x1.crop((0, mid, x1.width, x1.height)))
b = b.resize((round(b.width * a.height / b.height), a.height))
c = Image.new('RGB', (a.width + b.width + 14, a.height + 70), 'white'); c.paste(a, (0, 0)); c.paste(b, (a.width + 14, 0))
save(c, 'img02.jpg', tag='图1')

x2 = trim(X(2)); c = Image.new('RGB', (x2.width, x2.height + 70), 'white'); c.paste(x2, (0, 0))
save(c, 'img03.jpg', tag='图2')
w, h = x2.size; pw = w // 2 - 8; rh = h // 2 - 8; ch = round(pw * 383 / 900)  # 只取 A 格，裁下半部（人物）
x2.crop((0, rh - ch, pw, rh)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)

x3 = trim(X(3)); c = Image.new('RGB', (x3.width, x3.height + 70), 'white'); c.paste(x3, (0, 0))
save(c, 'img04.jpg', W=820, tag='图3')
