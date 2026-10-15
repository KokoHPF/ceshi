#!/usr/bin/env python3
"""Hugenberg 2023：图 1、图 2 拆出分图重新等高排版（图 2 抹去测力仪上的英文商标）；图 3 单腿跳示意图英文改中文；封面取自图 1。
用法：python3 make_figs.py <素材目录（x01..x03.png、title.png）> <输出目录>"""
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

L = 'ABCDE'
p1 = [label(p, L[k]) for k, p in enumerate(panels(X(1)))]
save(badge(stack([row(p1[:2]), row(p1[2:])]), '图1'), 'img02.jpg')

# 图 2：B、C 测力仪底板上的 “BIODEX” 字样抹去
a = cv2.cvtColor(np.array(X(2)), cv2.COLOR_RGB2BGR); g = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
mask = np.zeros(g.shape, np.uint8)
for x0, y0, x1, y1 in [(325, 1480, 410, 1610), (730, 1430, 845, 1530)]:
    mask[y0:y1, x0:x1] = (g[y0:y1, x0:x1] > 150) * 255
mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
x2 = Image.fromarray(cv2.cvtColor(cv2.inpaint(a, mask, 9, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))
p2 = [label(p, L[k]) for k, p in enumerate(panels(x2))]
save(badge(row(p2), '图2'), 'img03.jpg')

# 图 3：英文标题与标注改中文
im = X(3); d = ImageDraw.Draw(im)
d.rectangle([0, 0, im.width, 138], fill='white')
for x0, x1 in [(170, 270), (840, 940), (1565, 1670)]:
    d.rectangle([x0, 139, x1, 190], fill='white')
for x0 in (20, 688, 1413):
    d.rectangle([x0, 640, x0 + 186, 770], fill='white')
K = (20, 20, 20)
for cx, t in [(252, '单腿三级跳远'), (942, '外侧单腿三级跳远'), (1665, '内侧单腿三级跳远')]:
    f = font(60); w = d.textlength(t, font=f)
    d.text((cx - w / 2, 40), t, font=f, fill=K, stroke_width=1, stroke_fill=K)
for x0 in (178, 846, 1570):
    d.text((x0, 140), '6 米', font=font(46), fill=K)
for x0 in (30, 698, 1423):
    d.text((x0, 660), '总距离', font=font(50), fill=K)
save(badge(im, '图3'), 'img04.jpg')

# 封面：图 1A（前平板支撑测试）裁成 900×383
c = panels(X(1))[0]; w, h = c.size; ch = round(w * 383 / 900); y = max(0, (h - ch) // 2 + 20)
c.crop((0, y, w, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('panels', len(p1), len(p2))
