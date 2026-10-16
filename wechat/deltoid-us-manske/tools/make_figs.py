#!/usr/bin/env python3
"""Manske 2025 三角韧带超声：图 2D、3D、4D、7A 解剖标注改为中文（抹去英文后按原方向写中文）；
其余图仅有编号、箭头和数字标记；封面取自图 1。
用法：python3 make_figs.py <素材目录（x01～x07.png、title.png）> <输出目录>"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.width // 34))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    im.resize((W, round(im.height * W / im.width)), Image.LANCZOS).save(f'{OUT}/{name}', quality=90)


def relabel(im, items):
    """items: (box, 模式, 中文, 字号, 颜色, 角度)。模式 light/dark/lightred 决定抹去哪些像素"""
    a = np.array(im); g = a.mean(2); m = np.zeros(g.shape, np.uint8)
    for (x0, y0, x1, y1), mode, *_ in items:
        sg, sa = g[y0:y1, x0:x1], a[y0:y1, x0:x1].astype(int)
        if mode == 'light':
            mk = sg > 170
        elif mode == 'light2':  # 暗背景上的白字，连抗锯齿边一起抹
            mk = sg > 105
        elif mode == 'dark':
            mk = sg < 95
        else:  # 白字 + 红色波浪下划线
            mk = (sg > 170) | ((sa[..., 0] > 140) & (sa[..., 1] < 90))
        m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], mk * 255)
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), 2)
    im = Image.fromarray(cv2.inpaint(a, m, 5, cv2.INPAINT_TELEA))
    for (x0, y0, x1, y1), mode, t, fs, col, ang in items:
        f = font(fs); d0 = ImageDraw.Draw(im); w = int(d0.textlength(t, font=f)) + 12
        lay = Image.new('RGBA', (w, fs + 14), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        stroke = (0, 0, 0) if col == 'white' else (255, 255, 255)
        dl.text((6, 4), t, font=f, fill=col, stroke_width=2, stroke_fill=stroke)
        lay = lay.rotate(ang, expand=True, resample=Image.BICUBIC)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        im.paste(lay, (cx - lay.width // 2, cy - lay.height // 2), lay)
    return im


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

# 图 1：体位与骨性标志（仅数字标记）
x1 = X(1); save(badge(x1.copy(), '图1'), 'img02.jpg')
w, h = x1.size; cw = round(h * 900 / 383); x0 = (w - cw) // 2
x1.crop((x0, 0, x0 + cw, h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)

# 图 2：胫舟韧带
save(badge(relabel(X(2), [
    ((1132, 722, 1342, 808), 'dark', '胫舟韧带', 32, 'black', 15),
    ((868, 888, 948, 928), 'light', '胫骨', 36, 'white', 0),
    ((1262, 870, 1325, 900), 'light', '距骨', 28, 'white', 0),
    ((1450, 870, 1550, 900), 'light', '舟骨', 28, 'white', 0)]), '图2'), 'img03.jpg')

# 图 3：胫跟韧带与胫距后深韧带前部
save(badge(relabel(X(3), [
    ((1138, 783, 1348, 852), 'dark', '胫跟韧带', 34, 'black', 9),
    ((1195, 848, 1292, 897), 'dark', '胫距后深韧带前部', 24, 'black', 12),
    ((1496, 886, 1700, 926), 'light2', '载距突', 30, 'white', 0),
    ((915, 922, 1012, 968), 'light', '胫骨', 40, 'white', 0),
    ((1412, 972, 1628, 1032), 'light2', '跟骨', 40, 'white', 0)]), '图3'), 'img04.jpg')

# 图 4：胫距后浅韧带与胫距后深韧带后部
save(badge(relabel(X(4), [
    ((652, 460, 768, 497), 'light', '胫后肌腱', 20, 'white', 0),
    ((806, 486, 858, 517), 'light', '趾长屈肌腱', 13, 'white', 0),
    ((656, 497, 707, 524), 'dark', '胫距后浅韧带', 15, 'black', -10),
    ((688, 553, 762, 588), 'dark', '胫距后深韧带后部', 17, 'black', -4),
    ((550, 592, 615, 623), 'light', '胫骨', 26, 'white', 0),
    ((882, 598, 953, 630), 'light', '距骨', 26, 'white', 0)]), '图4'), 'img05.jpg')

# 图 5、6：撕裂（仅箭头）
save(badge(X(5), '图5'), 'img06.jpg')
save(badge(X(6), '图6'), 'img07.jpg')

# 图 7：胫距后浅韧带增厚、胫距后深韧带后部部分撕裂
save(badge(relabel(X(7), [
    ((348, 150, 438, 222), 'light', '胫距后浅韧带', 24, 'white', -28),
    ((232, 230, 358, 274), 'lightred', '胫距后深韧带后部', 24, 'white', 0)]), '图7'), 'img08.jpg')
