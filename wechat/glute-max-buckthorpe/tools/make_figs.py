#!/usr/bin/env python3
"""Buckthorpe 2019：图 4 英文标注改中文；图 6 背景横幅英文抹去；图 9 流程中文重绘；其余照片加图号；封面取自图 5。
用法：python3 make_figs.py <素材目录（x01..x08.png、title.png）> <输出目录>"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 28))
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
save(badge(X(1), '图1'), 'img02.jpg')
save(badge(X(2), '图2'), 'img03.jpg')
save(badge(X(3), '图3'), 'img04.jpg')

# ---------- 图 4：英文改中文 ----------
im = X(4); d = ImageDraw.Draw(im)
for box, col in [((10, 10, 748, 84), im.getpixel((30, 30))), ((770, 10, 1496, 84), im.getpixel((790, 30)))]:
    d.rectangle(box, fill=col)
for x0, y0, x1, y1 in [(484, 425, 588, 538), (484, 425, 650, 499), (118, 700, 280, 778),
                       (1122, 426, 1262, 538), (788, 692, 946, 770)]:
    d.rectangle([x0, y0, x1, y1], fill='white')


def ctext(t, cx, cy, fs, col, bold=False):
    f = font(fs); w = d.textlength(t, font=f)
    d.text((cx - w / 2, cy - fs / 2 - 2), t, font=f, fill=col, **(dict(stroke_width=1, stroke_fill=col) if bold else {}))


ctext('股四头肌（膝）主导策略', 379, 46, 38, 'white', True)
ctext('双屈曲（膝 + 髋/躯干）策略', 1133, 46, 38, 'white', True)
K = (30, 30, 30)
for x, y, t in [(488, 440, '髋/躯干\n屈曲不足'), (124, 708, '膝屈曲\n适当'), (1128, 440, '髋/躯干\n屈曲适当'), (796, 700, '膝屈曲\n适当')]:
    for i, ln in enumerate(t.split('\n')):
        d.text((x, y + i * 40), ln, font=font(32), fill=K)
save(badge(im, '图4'), 'img05.jpg')

save(badge(X(5), '图5'), 'img06.jpg', W=900)

# ---------- 图 6：背景横幅上的英文字母抹去 ----------
a = cv2.cvtColor(np.array(X(6)), cv2.COLOR_RGB2BGR)
hsv = cv2.cvtColor(a, cv2.COLOR_BGR2HSV); mask = np.zeros(a.shape[:2], np.uint8)
y0, y1, x0, x1 = 365, 432, 985, 1495
sub = hsv[y0:y1, x0:x1]
mask[y0:y1, x0:x1] = ((sub[..., 2] > 150) & (sub[..., 1] < 90)) * 255
mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
a = cv2.inpaint(a, mask, 9, cv2.INPAINT_TELEA)
save(badge(Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB)), '图6'), 'img07.jpg')

save(badge(X(7), '图7'), 'img08.jpg')
save(badge(X(8), '图8'), 'img09.jpg', W=780)

# ---------- 图 9：四步流程中文重绘 ----------
im = Image.new('RGB', (1080, 250), 'white'); d = ImageDraw.Draw(im)
NAV = (31, 56, 100); AR = (198, 217, 241)
steps = [('评估', '全面评估'), ('纠正', '针对性纠正'), ('再整合', '融入基础动作'), ('优化', '专项任务优化')]
bw, gap = 210, 80
for i, (a_, s_) in enumerate(steps):
    x = 20 + i * (bw + gap)
    d.rounded_rectangle([x, 40, x + bw, 150], 14, fill=NAV)
    f = font(40); w = d.textlength(a_, font=f)
    d.text((x + bw / 2 - w / 2, 70), a_, font=f, fill='white', stroke_width=1, stroke_fill='white')
    f2 = font(26); w2 = d.textlength(s_, font=f2)
    d.text((x + bw / 2 - w2 / 2, 175), s_, font=f2, fill=(70, 70, 70))
    if i < 3:
        ax = x + bw + 14
        d.rectangle([ax, 85, ax + 26, 105], fill=AR)
        d.polygon([(ax + 26, 70), (ax + 52, 95), (ax + 26, 120)], fill=AR)
im.save(f'{OUT}/img10.jpg', quality=92)

# ---------- 封面：图 5 裁成 900×383 ----------
c = X(5); w, h = c.size; ch = round(w * 383 / 900); y = (h - ch) // 2 + 40
c.crop((0, y, w, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('done')
