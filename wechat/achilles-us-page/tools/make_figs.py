#!/usr/bin/env python3
"""Page 2025 跟腱超声：图 2B、3B、4B 解剖标注改为中文（抹去英文后按原方向写中文）；其余图仅有编号和箭头；
原文图注把腱周炎写成“图 8”，与撕裂图重号，图片本身标为 9A/9B，本文按图片编号用图 9；封面取自图 1。
用法：python3 make_figs.py <素材目录（x01～x09.png、title.png）> <输出目录>"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.width // 34))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    im.resize((W, round(im.height * W / im.width)), Image.LANCZOS).save(f'{OUT}/{name}', quality=90)


def relabel(im, items):
    """items: (box, 阈值, 中文, 字号, 颜色, 角度)。阈值 >0 抹去亮于它的像素（白字），<0 抹去暗于 |阈值| 的像素（黑字），'sN' 抹去饱和度低于 N 的像素"""
    a = np.array(im); g = a.mean(2); m = np.zeros(g.shape, np.uint8)
    for (x0, y0, x1, y1), thr, *_ in items:
        sg = g[y0:y1, x0:x1]
        if isinstance(thr, str):  # 's60'：彩色底上的白/灰字，按低饱和度抹
            sa = a[y0:y1, x0:x1].astype(int); mk = (sa.max(2) - sa.min(2)) < int(thr[1:])
        else:
            mk = sg > thr if thr > 0 else sg < -thr
        m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], mk * 255)
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), 3)
    im = Image.fromarray(cv2.inpaint(a, m, 5, cv2.INPAINT_TELEA))
    for (x0, y0, x1, y1), thr, t, fs, col, ang in items:
        f = font(fs); w = int(ImageDraw.Draw(im).textlength(t, font=f)) + 12
        lay = Image.new('RGBA', (w, fs + 14), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        stroke = (0, 0, 0) if col == 'white' else (255, 255, 255)
        dl.text((6, 4), t, font=f, fill=col, stroke_width=2, stroke_fill=stroke)
        lay = lay.rotate(ang, expand=True, resample=Image.BICUBIC)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        im.paste(lay, (cx - lay.width // 2, cy - lay.height // 2), lay)
    return im


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

x1 = X(1); save(badge(x1.copy(), '图1'), 'img02.jpg')
w, h = x1.size; cw = round(h * 900 / 383); x0 = (w - cw) // 2
x1.crop((x0, 0, x0 + cw, h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)

# 图 2：止点长轴
save(badge(relabel(X(2), [
    ((1305, 58, 1565, 99), -150, '皮下组织', 34, 'black', 0),
    ((1165, 126, 1525, 176), -150, '跟腱', 44, 'black', 0),
    ((1266, 206, 1360, 272), 70, '滑囊', 26, 'white', 40),
    ((1010, 400, 1200, 460), -140, '脂肪垫', 44, 'black', 0),
    ((1462, 372, 1768, 438), 's999', '跟骨', 50, 'white', 0)]), '图2'), 'img03.jpg')

# 图 3：中段长轴
save(badge(relabel(X(3), [
    ((1260, 48, 1550, 89), -150, '皮下组织', 32, 'black', 0),
    ((1206, 122, 1614, 184), 's45', '跟腱', 46, 'white', 0),
    ((1308, 238, 1492, 296), 's70', '比目鱼肌', 42, 'white', 0),
    ((1244, 453, 1586, 512), 's999', '拇长屈肌', 42, 'white', 0),
    ((1310, 634, 1410, 676), -140, '胫骨', 30, 'black', 0)]), '图3'), 'img04.jpg')

# 图 4：止点短轴
save(badge(relabel(X(4), [
    ((1040, 136, 1215, 249), -140, '耦合剂伪影', 30, 'black', 0),
    ((1332, 60, 1570, 165), -150, '皮下组织', 30, 'black', 20),
    ((1482, 110, 1840, 200), -150, '跟腱', 42, 'black', 5),
    ((1504, 312, 1742, 373), 35, '跟骨', 44, 'white', 0)]), '图4'), 'img05.jpg')

for i in range(5, 10):
    save(badge(X(i), f'图{i}'), f'img{i + 1:02d}.jpg')
