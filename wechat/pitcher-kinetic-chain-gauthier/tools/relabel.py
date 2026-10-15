#!/usr/bin/env python3
"""图 1：英文标注改中文；图 2：去掉全部英文标注，改为红色编号 + 正文中文对照。

用法：python3 relabel.py <原图目录> <输出目录>   （f1.png、f2.png 为 300 dpi 截图）
"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)


def draw(im, items):
    p = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(p)
    for it in items:
        x, y, t, fs, col = it[:5]
        bold = len(it) > 5 and it[5]
        f = ImageFont.truetype(FONT, fs)
        kw = dict(stroke_width=1, stroke_fill=col) if bold else {}
        if x == 'c':  # 以 y=(cx, cy) 居中
            cx, cy = y
            for i, ln in enumerate(t.split('\n')):
                w = d.textlength(ln, font=f)
                d.text((cx - w / 2, cy + i * fs * 1.25), ln, font=f, fill=col, **kw)
        else:
            for i, ln in enumerate(t.split('\n')):
                d.text((x, y + i * fs * 1.25), ln, font=f, fill=col, **kw)
    return cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR)


# ---------- 图 1 ----------
im = cv2.imread(f'{SRC}/f1.png')
s = im.shape[1] / 900
S = lambda v: int(round(v * s))
# 白底上的字直接涂白；压在插画上的字用 inpaint 修补
white = [(25, 50, 300, 74), (56, 78, 128, 98), (166, 78, 240, 98), (410, 86, 560, 109), (635, 86, 785, 109),
         (90, 458, 275, 495), (360, 458, 545, 516), (620, 458, 800, 516)]
for x0, y0, x1, y1 in white:
    im[S(y0):S(y1), S(x0):S(x1)] = 255
boxes = [(264, 269, 342, 292), (205, 341, 292, 378), (520, 186, 624, 221), (520, 229, 600, 264),
         (774, 186, 878, 221), (711, 294, 782, 329)]
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
mask = np.zeros(g.shape, np.uint8)
for x0, y0, x1, y1 in boxes:
    sub = g[S(y0):S(y1), S(x0):S(x1)]
    mask[S(y0):S(y1), S(x0):S(x1)] = (sub < 185) * 255
mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
im = cv2.inpaint(im, mask, 7, cv2.INPAINT_TELEA)
K = (40, 40, 40)
im = draw(im, [
    (S(30), S(55), '箭头表示关节运动方向', S(14), K),
    (S(58), S(80), '离心', S(14), K), (S(168), S(80), '向心', S(14), K),
    ('c', (S(483), S(90)), '关键时刻 1', S(15), K, True), ('c', (S(708), S(90)), '关键时刻 2', S(15), K, True),
    (S(275), S(273), '屈膝', S(14), K),
    ('c', (S(246), S(344)), '股四头肌\n离心收缩', S(13), K),
    ('c', (S(571), S(189)), '肩外旋', S(14), K),
    ('c', (S(552), S(232)), '躯干\n旋转', S(13), K),
    ('c', (S(823), S(194)), '肩内旋', S(14), K),
    ('c', (S(742), S(302)), '髋内旋', S(14), K),
    ('c', (S(180), S(462)), '前脚着地', S(24), (20, 20, 20)),
    ('c', (S(450), S(458)), '加速期', S(24), (20, 20, 20)), ('c', (S(450), S(492)), '肩最大外旋', S(15), (20, 20, 20)),
    ('c', (S(708), S(458)), '减速期', S(24), (20, 20, 20)), ('c', (S(708), S(492)), '出手', S(15), (20, 20, 20)),
])
cv2.imwrite(f'{OUT}/g1.png', im)

# ---------- 图 2 ----------
im = cv2.imread(f'{SRC}/f2.png')
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
nonwhite = (g < 235).astype(np.uint8)
fig = cv2.morphologyEx(nonwhite, cv2.MORPH_OPEN, np.ones((11, 11), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(fig)
big = np.zeros_like(fig)
for i in range(1, n):
    if st[i, 4] > 20000:
        big[lab == i] = 1
big = cv2.morphologyEx(big, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
# 填补人体内部的高光“洞”
ff = big.copy() * 255
h, w = ff.shape
m = np.zeros((h + 2, w + 2), np.uint8)
cv2.floodFill(ff, m, (0, 0), 128)
big = ((ff != 128)).astype(np.uint8)
big = cv2.dilate(big, np.ones((3, 3), np.uint8))
out = np.full_like(im, 255)
out[big > 0] = im[big > 0]
for x0, y0, x1, y1 in [(1265, 160, 1305, 195), (1585, 122, 1648, 172), (1812, 330, 1872, 412)]:
    out[y0:y1, x0:x1] = 255
# 去掉黑色引线残段（细线），保留人体
gg = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
sat = out.max(2).astype(int) - out.min(2).astype(int)
blk = ((gg < 60) & (sat < 30)).astype(np.uint8)
thin = blk & (1 - cv2.morphologyEx(blk, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)))
thin = cv2.dilate(thin, np.ones((3, 3), np.uint8))
out = cv2.inpaint(out, thin * 255, 5, cv2.INPAINT_TELEA)
A = [(1, 345, 160), (2, 500, 240), (3, 618, 228), (4, 380, 300), (5, 470, 352), (6, 860, 385),
     (7, 450, 478), (8, 640, 520), (9, 350, 668), (10, 310, 925), (11, 812, 885)]
B = [(1, 1415, 240), (2, 1605, 240), (3, 1790, 330), (4, 1415, 390), (5, 1400, 480), (6, 1300, 663)]
p = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
d = ImageDraw.Draw(p)
f = ImageFont.truetype(FONT, 30)
for num, x, y in A + B:
    r = 24
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline='white', width=3)
    t = str(num)
    d.text((x - d.textlength(t, font=f) / 2, y - 17), t, font=f, fill='white')
F = ImageFont.truetype(FONT, 56)
d.text((20, 960), 'a', font=F, fill=(20, 20, 20))
d.text((1030, 960), 'b', font=F, fill=(20, 20, 20))
cv2.imwrite(f'{OUT}/g2.png', cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR))
print('done')
