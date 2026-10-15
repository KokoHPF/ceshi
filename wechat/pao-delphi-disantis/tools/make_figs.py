#!/usr/bin/env python3
"""Disantis 2022：原图各分图之间留白很多，拆出每张照片重新等高排版并重标 a～e；加图号；封面取自图 4。
用法：python3 make_figs.py <素材目录（x01..x04.png、title.png）> <输出目录>"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def panels(im, min_area=40000, by_col=False):
    """找出图中的各张照片（去掉字母标签），按行再按列排序。"""
    g = np.array(im.convert('L'))
    m = (g < 238).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(m)
    rs = [tuple(st[i, :4]) for i in range(1, n) if st[i, 4] > min_area]
    if by_col:
        rs.sort(key=lambda r: (r[0] + r[2] // 2) // (im.width // 2) * 10000 + r[1])
    else:
        rs.sort(key=lambda r: (r[1] + r[3] // 2) // (im.height // 4) * 10000 + r[0])
    return [im.crop((x, y, x + w, y + h)) for x, y, w, h in rs]


def label(im, t):
    d = ImageDraw.Draw(im); f = font(48)
    w = d.textlength(t, font=f) + 18; h = f.size + 12
    d.rectangle([0, im.height - h, w, im.height], fill='white')
    d.text((9, im.height - h + 5), t, font=f, fill=(20, 20, 20))
    return im


def row(ims, W=1080, gap=10):
    H = (W - gap * (len(ims) - 1)) / sum(i.width / i.height for i in ims)
    ims = [i.resize((max(1, round(i.width * H / i.height)), round(H)), Image.LANCZOS) for i in ims]
    out = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), round(H)), 'white'); x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width + gap
    return out


def stack(rows, gap=10):
    W = min(r.width for r in rows)
    rows = [r.resize((W, round(r.height * W / r.width))) for r in rows]
    out = Image.new('RGB', (W, sum(r.height for r in rows) + gap * (len(rows) - 1)), 'white'); y = 0
    for r in rows:
        out.paste(r, (0, y)); y += r.height + gap
    return out


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 22))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')

L = 'abcde'
p1 = [label(p, L[k] + ')') for k, p in enumerate(panels(X(1), by_col=True))]
# 图 1：a、b 上下叠放，c 在右侧等高
ab = stack([p1[0], p1[1]])
save(badge(row([ab, p1[2]]), '图1'), 'img02.jpg')

p2 = [label(p, L[k] + ')') for k, p in enumerate(panels(X(2)))]
save(badge(stack([row(p2[:2]), row(p2[2:])]), '图2'), 'img03.jpg')

p3 = [label(p, L[k] + ')') for k, p in enumerate(panels(X(3)))]
save(badge(stack([row(p3[:2]), row(p3[2:])]), '图3'), 'img04.jpg')

p4 = [label(p, L[k] + ')') for k, p in enumerate(panels(X(4)))]
save(badge(row(p4), '图4'), 'img05.jpg')

# 封面：图 4 四张照片并排后居中裁成 900×383
c = row(panels(X(4)), W=1500); w, h = c.size; cw = round(h * 900 / 383); x = (w - cw) // 2
c.crop((x, 0, x + cw, h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('panels', len(p1), len(p2), len(p3), len(p4))
