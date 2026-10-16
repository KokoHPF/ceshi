#!/usr/bin/env python3
"""Manske 2026 半月板超声：图 2B、3B 解剖标注改为中文，图 4A、5A 超声机英文注记抹除；
图 1～5 加图号；封面取自图 3。
用法：python3 make_figs.py <素材目录（x01～x05.png、title.png）> <输出目录>"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def badge(im, t, left=True):
    d = ImageDraw.Draw(im); f = font(max(26, im.width // 40))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = 10 if left else im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=90)
    return im


def inpaint(im, boxes, thr=None):
    a = np.array(im); g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY); m = np.zeros(a.shape[:2], np.uint8)
    for b in boxes:
        x0, y0, x1, y1 = b[:4]
        if thr is not None and len(b) == 4:  # 白字：只抹亮像素
            mm = cv2.dilate(((g[y0:y1, x0:x1] > thr) * 255).astype(np.uint8), np.ones((5, 5), np.uint8), 3)
            m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], mm)
        elif len(b) == 5:  # 黑字：只抹暗像素
            mm = cv2.dilate(((g[y0:y1, x0:x1] < 90) * 255).astype(np.uint8), np.ones((5, 5), np.uint8), 2)
            m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], mm)
        else:
            m[y0:y1, x0:x1] = 255
    return Image.fromarray(cv2.inpaint(a, m, 7, cv2.INPAINT_TELEA))


def labels(im, items, fs):
    d = ImageDraw.Draw(im)
    for (cx, cy), t in items:
        f = font(fs); w = d.textlength(t, font=f)
        d.text((cx - w / 2, cy - fs / 2 - 2), t, font=f, fill='white', stroke_width=3, stroke_fill=(30, 30, 30))
    return im


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

# 图 1：体位与探头放置（仅 1A～1D 编号）
save(badge(X(1), '图1', left=False), 'img02.jpg')

# 图 2：外侧半月板长轴切面，2B 标注改中文（放大 2 倍处理，文字更清晰）
im = X(2); im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
B = [(222, 500, 464, 534), (444, 552, 582, 588), (2, 595, 352, 630), (336, 629, 724, 664, 'dark'), (834, 656, 942, 732),
     (188, 746, 292, 770), (463, 788, 537, 822), (33, 818, 130, 854)]
im = inpaint(im, [tuple(v * 2 for v in b[:4]) + b[4:] for b in B], thr=150)
im = labels(im, [((343 * 2, 516 * 2), '皮下组织'), ((513 * 2, 570 * 2), '脂肪'), ((110 * 2, 612 * 2), '股二头肌腱'),
                 ((530 * 2, 646 * 2), '外侧副韧带'), ((888 * 2, 694 * 2), '腓骨头'), ((240 * 2, 758 * 2), '半月板'),
                 ((500 * 2, 805 * 2), '胫骨'), ((82 * 2, 836 * 2), '股骨')], 50)
save(badge(im, '图2'), 'img03.jpg')

# 图 3：内侧半月板长轴切面，3B 标注改中文
im = X(3); im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
im = inpaint(im, [tuple(v * 2 for v in b[:4]) + b[4:] for b in [(606, 48, 686, 82, 'dark'), (590, 180, 724, 258), (862, 188, 948, 220)]], thr=150)
im = labels(im, [((646 * 2, 66 * 2), '内侧副韧带'), ((657 * 2, 218 * 2), '股骨髁'), ((905 * 2, 204 * 2), '胫骨')], 50)
save(badge(im, '图3'), 'img04.jpg')
w, h = im.size; ch = round(w * 383 / 900); y0 = (h - ch) // 2
im.crop((0, y0, w, y0 + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)

# 图 4、5：撕裂与囊肿，抹去超声机英文注记（RE MED、RE）
save(badge(inpaint(X(4), [(82, 238, 190, 266)]), '图4'), 'img05.jpg')
save(badge(inpaint(X(5), [(0, 26, 48, 62)]), '图5'), 'img06.jpg')
