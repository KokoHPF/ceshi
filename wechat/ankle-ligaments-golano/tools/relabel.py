#!/usr/bin/env python3
"""把原图中的英文方位罗盘（DORSAL/PLANTAR/ANTERIOR…）和图 9 的 “Level” 标注替换成中文。

用法：python3 relabel.py <原图目录> <输出目录>
原图目录内为 f1.png … f21.png（300 dpi 截取的原文 Figure 1–21）。
"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'

D, P, A, PO, M, L, PR, DI = '背侧', '跖侧', '前方', '后方', '内侧', '外侧', '近端', '远端'
# 图号: (罗盘左上角 x, y, 边长, 上, 左, 右, 下, 深色罗盘?)
COMPASS = {
    2: (808, 47, 98, D, PO, A, P), 3: (753, 69, 147, D, PO, A, P), 4: (830, 44, 98, D, PO, A, P),
    6: (828, 47, 98, PR, M, L, DI), 7: (809, 47, 98, D, PO, A, P), 8: (33, 47, 98, D, M, L, P),
    9: (51, 52, 98, D, M, L, P), 10: (51, 70, 147, D, PO, A, P), 12: (828, 47, 98, D, A, PO, P),
    13: (40, 55, 118, D, A, PO, P), 14: (76, 74, 152, D, A, PO, P), 15: (18, 57, 118, D, A, PO, P),
    16: (24, 21, 157, D, L, M, P), 18: (47, 47, 98, D, L, M, P), 19: (824, 47, 98, D, PO, A, P),
    20: (16, 51, 108, D, M, L, P), 21: (773, 72, 142, D, PO, A, P, 'dark'),
}


def relabel_compass(bgr, spec):
    x, y, w, top, left, right, bot = spec[:7]
    dark = len(spec) > 7
    cx, cy = x + w / 2, y + w / 2
    H, W = bgr.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.hypot(xx - cx, yy - cy)
    ring = (r > 0.53 * w) & (r < 0.9 * w)
    b, g, rr = [bgr[..., i].astype(int) for i in range(3)]
    gray = (b + g + rr) / 3
    sat = np.max(bgr, 2).astype(int) - np.min(bgr, 2).astype(int)
    if dark:
        txt = ring & (gray < 150) & (sat < 35)
    else:
        # 只处理黑色背景上的字：周围 21px 平均亮度要低，避免把组织涂黑
        local = cv2.blur(gray.astype(np.float32), (21, 21))
        txt = ring & (gray > 95) & (sat < 45) & (local < 90)
    mask = cv2.dilate(txt.astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
    if dark:
        # 图 21 下方的字压在深红色带上，直接整块修补
        mask[int(cy + 0.5 * w):int(cy + 0.95 * w), int(cx - 0.6 * w):int(cx + 0.6 * w)] = 255
    out = cv2.inpaint(bgr, mask, 7, cv2.INPAINT_TELEA)
    im = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(im)
    fs = max(16, int(w * 0.24))
    f = ImageFont.truetype(FONT, fs)
    col = (50, 50, 50) if dark else (255, 255, 255)
    stroke = dict(stroke_width=3, stroke_fill=(255, 255, 255)) if dark else {}
    R = 0.74 * w

    def hcenter(t, py):
        d.text((cx - d.textlength(t, font=f) / 2, py - fs / 2), t, font=f, fill=col, **stroke)

    def vcenter(t, px):
        n = len(t)
        for i, ch in enumerate(t):
            d.text((px - fs / 2, cy - n * fs / 2 + i * fs), ch, font=f, fill=col, **stroke)

    hcenter(top, max(cy - R, fs / 2 + 2))
    hcenter(bot, cy + R)
    vcenter(left, max(cx - R, fs / 2 + 2))
    vcenter(right, min(cx + R, W - fs / 2 - 2))
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


def relabel_levels(bgr):
    """图 9：a 图竖线旁的 Level 1–4，b 图 MRI 四格右上角的 Level 1–4。"""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(gray.shape, np.uint8)
    lines = {663: '1', 577: '2', 497: '3', 421: '4'}
    for lx in lines:
        box = (slice(58, 205), slice(lx + 3, lx + 40))
        mask[box] = (gray[box] > 150) * 255
    mri = [(1440, 2, 1531, 38, '1'), (1940, 2, 2031, 38, '2'), (1440, 337, 1531, 373, '3'), (1940, 337, 2031, 373, '4')]
    for x0, y0, x1, y1, _ in mri:
        mask[y0:y1, x0:x1] = (gray[y0:y1, x0:x1] > 60) * 255
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
    out = cv2.inpaint(bgr, mask, 7, cv2.INPAINT_TELEA)
    for x0, y0, x1, y1, _ in mri:
        out[y0:y1, x0:x1] = 0
    im = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 28)
    for lx, n in lines.items():  # 竖排“层面N”，放在竖线右侧
        for i, ch in enumerate('层面' + n):
            d.text((lx + 6, 64 + i * 32), ch, font=f, fill='white')
    for x0, y0, x1, y1, n in mri:
        t = '层面 ' + n
        d.text((x1 - 6 - d.textlength(t, font=f), y0 + 3), t, font=f, fill='white')
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


for k in range(1, 22):
    img = cv2.imread(f'{SRC}/f{k}.png')
    if k in COMPASS:
        img = relabel_compass(img, COMPASS[k])
    if k == 9:
        img = relabel_levels(img)
    cv2.imwrite(f'{OUT}/g{k}.png', img)
print('done')
