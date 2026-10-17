#!/usr/bin/env python3
"""李明珠等 2025 ACL 重建术后 PRP + Mulligan 动态关节松动术 3 例：首页中文标题与作者区截图；
图 1～5 操作照片，去除中华医学会水印中的英文字样（按局部色差检测水印笔画后修补）；封面为文字设计图。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import cv2
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); RED = (171, 25, 66); TEAL = (20, 120, 110)
d = pymupdf.open(PDF)


def clip(pg, r, dpi=200):
    pix = d[pg].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*r))
    return np.array(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))[..., ::-1].copy()


def dewm(im, boxes, bright=None):
    """去掉水印英文：青色笔画比局部中值更偏蓝绿；蓝色铺巾上的笔画比局部中值更亮。"""
    x = im.astype(np.int16)
    dd = (x[..., 0] - x[..., 2]).astype(np.float32); g = (x[..., 1] - x[..., 2]).astype(np.float32)
    dm = cv2.medianBlur(np.clip(dd + 128, 0, 255).astype(np.uint8), 41).astype(np.float32) - 128
    m = ((dd - dm) > 7) & (g > dm - 20)
    if bright:
        L = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
        Lm = cv2.medianBlur(L.astype(np.uint8), 41).astype(np.float32)
        b2 = np.zeros(m.shape, bool); x0, y0, x1, y1 = bright; b2[y0:y1, x0:x1] = True
        m |= ((L - Lm) > 4) & b2
    box = np.zeros(m.shape, bool)
    for x0, y0, x1, y1 in boxes: box[y0:y1, x0:x1] = True
    m = cv2.dilate(((m & box) * 255).astype(np.uint8), np.ones((5, 5), np.uint8))
    return cv2.inpaint(im, m, 5, cv2.INPAINT_TELEA)


save = lambda a, n: Image.fromarray(a[..., ::-1]).save(f'{OUT}/img{n:02d}.jpg', quality=88)

# 首页：中文标题 + 作者单位（跳过英文标题和数据库 logo）
a = clip(0, (85, 85, 510, 158)); b = clip(0, (85, 205, 510, 293))
save(np.vstack([a, np.full((20, a.shape[1], 3), 255, np.uint8), b]), 1)

f1 = clip(5, (110, 86, 475, 480))[:-8]
save(dewm(f1, [(240, 820, 830, 1096), (600, 930, 780, 1096)], bright=(420, 930, 780, 1096)), 2)
save(clip(5, (111, 515, 528, 754)), 3)
save(dewm(clip(6, (110, 293, 525, 523)), [(200, 0, 548, 640), (588, 0, 830, 640)]), 4)
save(clip(7, (110, 83, 525, 343)), 5)
save(dewm(clip(7, (110, 373, 525, 646)), [(230, 0, 563, 360), (588, 0, 800, 330)]), 6)

cv = Image.new('RGB', (900, 383), (234, 245, 243)); dr = ImageDraw.Draw(cv)
dr.rectangle([0, 0, 900, 70], fill=TEAL)
dr.text((40, 14), '中华医学会 · 病例报告精读', font=font(34), fill='white')
dr.text((40, 100), 'ACL 重建术后', font=font(66), fill=INK)
dr.text((40, 195), 'PRP + Mulligan 动态松动', font=font(56), fill=RED)
x = 40
for tg in ['3 例病例', '胫骨旋转', '动态松动', '证据点评']:
    w = dr.textlength(tg, font=font(28)) + 28
    dr.rounded_rectangle([x, 305, x + w, 353], 22, fill='white', outline=TEAL, width=2)
    dr.text((x + 14, 313), tg, font=font(28), fill=TEAL); x += w + 14
cv.save(f'{OUT}/cover.jpg', quality=92)
