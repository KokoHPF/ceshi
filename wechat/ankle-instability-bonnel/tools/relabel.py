#!/usr/bin/env python3
"""把原文图片中的英文（及图 9 的法文和患者姓名）替换为中文。

用法：python3 relabel.py <原图目录> <输出目录>   （原图为 f1.png … f9.png，300 dpi）
坐标按 900 px 宽缩略图量取，脚本内按比例换算。
"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'


def load(k):
    im = cv2.imread(f'{SRC}/f{k}.png')
    s = im.shape[1] / 900 if im.shape[1] > 900 or im.shape[0] > 900 else 1
    s = max(im.shape[1], im.shape[0]) / 900 if max(im.shape[:2]) > 900 else 1
    return im, s


def R(s, box):
    return [int(round(v * s)) for v in box]


def inpaint(im, boxes, bright=True, thr=170):
    """仅修补框内的文字像素（亮字或暗字）"""
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(g.shape, np.uint8)
    for x0, y0, x1, y1 in boxes:
        sub = g[y0:y1, x0:x1]
        mask[y0:y1, x0:x1] = ((sub > thr) if bright else (sub < thr)) * 255
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
    return cv2.inpaint(im, mask, 9, cv2.INPAINT_TELEA)


def wipe(im, boxes, color=(255, 255, 255)):
    for x0, y0, x1, y1 in boxes:
        im[y0:y1, x0:x1] = color
    return im


def text(im, items):
    """items: (x, y, 文本, 字号, 颜色, 描边色或None)"""
    p = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(p)
    for x, y, t, fs, col, stroke in items:
        f = ImageFont.truetype(FONT, fs)
        kw = dict(stroke_width=max(2, fs // 14), stroke_fill=stroke) if stroke else {}
        d.text((x, y), t, font=f, fill=col, **kw)
    return cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR)


out = {}
for k in range(1, 10):
    out[k] = cv2.imread(f'{SRC}/f{k}.png')

# 图 2：Lateral / Medial 字样 + 下方曲率半径说明框
im, s = load(2)
im = inpaint(im, [R(s, (115, 110, 285, 160)), R(s, (625, 110, 785, 160))], bright=False, thr=90)
im = wipe(im, [R(s, (0, 345, 900, 512))])
B = (20, 20, 20)
im = text(im, [
    (*R(s, (150, 112)), '外侧', int(40 * s), B, None), (*R(s, (660, 112)), '内侧', int(40 * s), B, None),
    (*R(s, (230, 360)), 'RC：曲率半径', int(30 * s), B, None),
    (*R(s, (230, 402)), '1 型（66%）外侧 RC ＞ 内侧 RC', int(30 * s), B, None),
    (*R(s, (230, 440)), '2 型（19%）外侧 RC ＝ 内侧 RC', int(30 * s), B, None),
    (*R(s, (230, 478)), '3 型（15%）外侧 RC ＜ 内侧 RC', int(30 * s), B, None),
])
out[2] = im

# 图 3：两行 Type 说明（白底）
im, s = load(3)
im = wipe(im, [R(s, (140, 368, 670, 402)), R(s, (140, 795, 670, 828))])
im = cv2.copyMakeBorder(im, 0, int(28 * s), 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
im = text(im, [(*R(s, (250, 362)), '1 型 = 距腓前韧带紧张', int(32 * s), B, None),
               (*R(s, (235, 790)), '3 型 = 距腓前韧带受保护', int(32 * s), B, None)])
out[3] = im

# 图 4：跟腓韧带标注（白字压在骨面上）
im, s = load(4)
im = inpaint(im, [R(s, (20, 540, 540, 585))], bright=True, thr=215)
im = text(im, [(*R(s, (40, 535)), '跟腓韧带（CFL）', int(36 * s), (255, 255, 255), (40, 40, 40))])
out[4] = im

# 图 6：颈韧带说明 + 跗骨窦
im, s = load(6)
im = inpaint(im, [R(s, (425, 12, 875, 148)), R(s, (310, 550, 520, 600))], bright=True, thr=200)
W = (255, 255, 255)
im = text(im, [(*R(s, (590, 18)), '颈韧带', int(26 * s), W, (30, 30, 30)),
               (*R(s, (520, 58)), '或距跟外侧韧带', int(26 * s), W, (30, 30, 30)),
               (*R(s, (590, 98)), '常为多束', int(26 * s), W, (30, 30, 30)),
               (*R(s, (335, 552)), '跗骨窦', int(32 * s), W, (30, 30, 30))])
out[6] = im

# 图 7：下方三段说明（白底）
im, s = load(7)
im = wipe(im, [R(s, (0, 322, 322, 414)), R(s, (318, 350, 900, 414))])
im = text(im, [
    (*R(s, (8, 326)), '1 距腓前韧带', int(15 * s), B, None), (*R(s, (8, 348)), '2 跟腓韧带', int(15 * s), B, None),
    (*R(s, (8, 370)), '3 颈韧带', int(15 * s), B, None), (*R(s, (8, 392)), '4 距跟骨间韧带', int(15 * s), B, None),
    (*R(s, (362, 356)), '跟腓韧带扭伤', int(16 * s), B, None), (*R(s, (362, 380)), '＝距跟单元仍完整', int(16 * s), B, None),
    (*R(s, (668, 356)), '颈韧带扭伤', int(16 * s), B, None), (*R(s, (668, 380)), '＝距下关节松弛', int(16 * s), B, None),
])
out[7] = im

# 图 9：法文 Droit / VARUS → 右侧 / 内翻；左下角患者姓名抹除
im, s = load(9)
im = inpaint(im, [R(s, (118, 448, 195, 480)), R(s, (128, 502, 222, 535)), R(s, (0, 605, 150, 650))], bright=True, thr=150)
im = text(im, [(*R(s, (125, 448)), '右侧', int(24 * s), W, None), (*R(s, (135, 503)), '内翻', int(24 * s), W, None)])
out[9] = im

for k, im in out.items():
    cv2.imwrite(f'{OUT}/g{k}.png', im)
print('done')
