#!/usr/bin/env python3
"""Buckthorpe 2020（ACL 十项任务）：图 1 英文标注改中文；图 2 十个任务拆分重排、背景横幅英文抹去；图 3 横幅英文抹去；封面取自图 3。
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


def erase_white(im, boxes):
    a = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR); hsv = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)
    m = np.zeros(a.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes:
        sub = hsv[y0:y1, x0:x1]
        m[y0:y1, x0:x1] = ((sub[..., 2] > 150) & (sub[..., 1] < 80)) * 255
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    return Image.fromarray(cv2.cvtColor(cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 22))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def panels(im, min_area=60000):
    g = np.array(im.convert('L'))
    m = (g < 238).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(m)
    rs = [tuple(st[i, :4]) for i in range(1, n) if st[i, 4] > min_area]
    rs.sort(key=lambda r: (r[1] + r[3] // 2) // (im.height // 5) * 10000 + r[0])
    return [im.crop((x, y, x + w, y + h)) for x, y, w, h in rs]


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


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')

# ---------- 图 1：英文标注改中文 ----------
im = X(1); d = ImageDraw.Draw(im)
labels = [((462, 331, 618, 356), (466, 333), '理想 <5°，躯干不倾斜'),
          ((464, 401, 672, 426), (468, 402), '理想 <5°，骨盆不下沉/不上提'),
          ((438, 524, 644, 549), (442, 526), '无动态膝外翻负荷'),
          ((1302, 398, 1366, 424), (1306, 400), '理想 90°'),
          ((1232, 573, 1302, 599), (1236, 575), '理想 90°')]
for box, (x, y), t in labels:
    d.rectangle(box, fill=(255, 255, 255))
for box, (x, y), t in labels:
    f = font(24); w = d.textlength(t, font=f)
    d.rectangle([x - 4, y - 3, x + w + 6, y + 29], fill='white', outline=(60, 60, 60), width=1)
    d.text((x + 1, y), t, font=f, fill=(20, 20, 20))
d.text((14, 14), '1a', font=font(40), fill='white', stroke_width=2, stroke_fill=(0, 0, 0))
d.text((866, 14), '1b', font=font(40), fill='white', stroke_width=2, stroke_fill=(0, 0, 0))
save(badge(im, '图1'), 'img02.jpg')

# ---------- 图 2：十项任务 ----------
x2 = erase_white(X(2), [(845, 2310, 905, 2395), (990, 2310, 1305, 2395)])
p = panels(x2)
print('panels', len(p))
save(badge(stack([row(p[:4]), row(p[4:7]), row(p[7:10])]), '图2'), 'img03.jpg')

# ---------- 图 3：横幅英文抹去 ----------
x3 = erase_white(X(3), [(770, 680, 1067, 760)])
save(badge(x3.copy(), '图3'), 'img04.jpg', W=720)

c = x3; w, h = c.size; ch = round(w * 383 / 900); y = 300
c.crop((0, y, w, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
