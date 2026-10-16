#!/usr/bin/env python3
"""Manske 2025 跖筋膜超声：图 2B、3B 解剖标注改为中文，图 2A 比例尺英文单位抹除；其余图仅有编号和箭头；封面取自图 1。
用法：python3 make_figs.py <素材目录（x01～x06.png、title.png）> <输出目录>"""
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
        elif mode == 'light3':  # 红底白字
            mk = sg > 125
        elif mode == 'dark2':  # 白色条带上的灰字
            mk = sg < 175
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

x1 = X(1); save(badge(x1.copy(), '图1'), 'img02.jpg')
w, h = x1.size; cw = round(h * 900 / 383); x0 = (w - cw) // 2
x1.crop((x0, 0, x0 + cw, h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)

im = relabel(X(2), [
    ((1024, 12, 1284, 60), 'dark', '皮下组织', 36, 'black', 0),
    ((1386, 122, 1452, 172), 'dark', '脂肪', 36, 'black', 0),
    ((1417, 238, 1676, 290), 'dark2', '跖筋膜', 36, 'black', 0),
    ((1125, 322, 1331, 376), 'light2', '跟骨', 38, 'white', 0),
    ((1588, 333, 2026, 388), 'light3', '足底内在肌', 38, 'white', 0)])
im = relabel(im, [((826, 530, 926, 566), 'light2', '', 10, 'white', 0)])  # 抹去“2,9 cm”
save(badge(im, '图2'), 'img03.jpg')

save(badge(relabel(X(3), [
    ((1390, 44, 1634, 88), 'dark', '皮下组织', 36, 'black', 0),
    ((1448, 149, 1592, 192), 'dark', '脂肪垫', 36, 'black', 0),
    ((1413, 245, 1672, 291), 'dark2', '跖筋膜', 36, 'black', 0),
    ((1409, 365, 1617, 419), 'light2', '跟骨', 38, 'white', 0)]), '图3'), 'img04.jpg')

save(badge(X(4), '图4'), 'img05.jpg')
save(badge(X(5), '图5'), 'img06.jpg')
save(badge(X(6), '图6'), 'img07.jpg')
