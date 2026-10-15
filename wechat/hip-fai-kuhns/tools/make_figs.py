#!/usr/bin/env python3
"""Kuhns 2017：图 1 四阶段流程中文重绘；图 2C 入路标注改中文；其余照片按等高并排拼图并标图号；封面取自正文图片。
用法：python3 make_figs.py <素材目录（x01..x10.png、title.png）> <输出目录>"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def badge(im, t, corner='br'):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 30))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10 if corner == 'br' else 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def pair(a, b, ta, tb, H=1100, gap=14):
    a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS)
    b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
    badge(a, ta); badge(b, tb)
    im = Image.new('RGB', (a.width + b.width + gap, H), 'white')
    im.paste(a, (0, 0)); im.paste(b, (a.width + gap, 0))
    return im


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


# ---------- 原文首页标题 ----------
save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')

# ---------- 图 1：四阶段流程（中文重绘） ----------
BL = (79, 129, 189); AR = (198, 217, 241)
im = Image.new('RGB', (1080, 900), 'white'); d = ImageDraw.Draw(im)
steps = [('第一阶段：术后 1～6 周', '目标：保护关节，避免刺激'),
         ('第二阶段：术后 3～10 周', '目标：恢复无代偿步态'),
         ('第三阶段：术后 8～16 周', '目标：恢复伤前功能'),
         ('第四阶段：术后 16～32 周', '目标：恢复跑步和运动')]
bw, bh, dx, dy = 600, 150, 150, 225
for i, (a, g) in enumerate(steps):
    x0, y0 = 20 + i * dx, 20 + i * dy
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 14, fill=BL)
    d.text((x0 + 28, y0 + 26), a, font=font(40), fill='white', stroke_width=1, stroke_fill='white')
    d.text((x0 + 28, y0 + 88), g, font=font(34), fill='white')
    if i < 3:
        cx = x0 + bw - 70; ya = y0 + bh + 4; yb = y0 + dy - 6
        d.rectangle([cx - 22, ya, cx + 22, yb - 34], fill=AR)
        d.polygon([(cx - 48, yb - 36), (cx + 48, yb - 36), (cx, yb)], fill=AR)
save(im.crop((0, 0, 1080, 20 + 3 * dy + bh + 20)), 'img02.jpg')

# ---------- 图 2：C 图入路标注改中文 ----------
im = cv2.imread(f'{SRC}/x02.png'); Y0 = 432
labels = [((100, 4, 145, 26), '髂前上棘', (96, 2), 22),
          ((286, 36, 356, 56), '前方入路', (290, 34), 22),
          ((396, 146, 456, 166), 'DALA 入路', (392, 144), 20),
          ((132, 171, 220, 191), '前外侧入路', (126, 169), 21),
          ((240, 220, 350, 244), '大转子', (262, 220), 24)]
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); mask = np.zeros(g.shape, np.uint8)
for (x0, y0, x1, y1), *_ in labels:
    sub = g[Y0 + y0:Y0 + y1, x0:x1]
    mask[Y0 + y0:Y0 + y1, x0:x1] = (sub < 110) * 255
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
im = cv2.inpaint(im, mask, 5, cv2.INPAINT_TELEA)
p = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(p)
for _, t, (x, y), fs in labels:
    d.text((x, Y0 + y), t, font=font(fs), fill=(25, 25, 25), stroke_width=2, stroke_fill=(250, 235, 220))
p.save(f'{OUT}/fig2_cn.png')
save(badge(p.copy(), '图2'), 'img03.jpg')

# ---------- 拼图 ----------
save(pair(X(3), X(4), '图3', '图4'), 'img04.jpg')
save(pair(X(5), X(6), '图5', '图6'), 'img05.jpg')
save(badge(X(7), '图7'), 'img06.jpg', W=720)
save(badge(X(8), '图8'), 'img07.jpg')
# 图 10：跑步机上的品牌英文（侧柱竖排商标、扶手贴纸）抹去
im = cv2.imread(f'{SRC}/x10.png'); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); mask = np.zeros(g.shape, np.uint8)
mask[300:545, 0:40] = (g[300:545, 0:40] > 170) * 255
mask[565:605, 560:725] = (g[565:605, 560:725] < 120) * 255
mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
x10 = Image.fromarray(cv2.cvtColor(cv2.inpaint(im, mask, 7, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))
save(pair(X(9), x10, '图9', '图10'), 'img08.jpg')

# ---------- 封面：图 8 下排（F 撑杖行走）裁成 900×383 ----------
c = X(8); w, h = c.size
c = c.crop((w - 893, h - 380, w, h))
c.resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('done')
