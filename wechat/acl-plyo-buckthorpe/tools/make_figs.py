#!/usr/bin/env python3
"""Buckthorpe 2021（ACL 术后增强式训练）：图 2 英文标注改中文；图 3 表面名称改中文；
蓝色横幅上的英文字母（ISOKINETIC 等）自动抹去；各图加图号；封面取自图 9。
用法：python3 make_figs.py <素材目录（x01..x15.png、title.png）> <输出目录>"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def erase_on_blue(im, y_from=0.0):
    """抹去蓝色横幅上的白色字母（只处理被大面积蓝色包围的白色像素）。"""
    a = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR); hsv = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    blue = ((h > 100) & (h < 130) & (s > 120) & (v > 60)).astype(np.float32)
    white = (v > 170) & (s < 70)
    near = cv2.blur(blue, (45, 45)) > 0.45
    m = (white & near).astype(np.uint8) * 255
    m[: int(im.height * y_from)] = 0
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    return Image.fromarray(cv2.cvtColor(cv2.inpaint(a, m, 7, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 18))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


def pair(a, b, H=800, gap=14):
    a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS)
    b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
    im = Image.new('RGB', (a.width + b.width + gap, H), 'white')
    im.paste(a, (0, 0)); im.paste(b, (a.width + gap, 0))
    return im


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')

# 图 1（四类增强式）
save(badge(X(1), '图1'), 'img02.jpg', W=760)

# 图 2：英文标注改中文
im = X(2); d = ImageDraw.Draw(im)
for box, t in [((222, 181, 290, 205), '理想 <5°'), ((390, 246, 458, 270), '理想 <5°'),
               ((16, 368, 274, 392), '无动态膝外翻表现'), ((746, 221, 814, 245), '理想 90°'),
               ((640, 380, 702, 404), '理想 90°')]:
    d.rectangle(box, fill='white')
    f = font(19); w = d.textlength(t, font=f)
    d.text(((box[0] + box[2]) / 2 - w / 2, box[1] + 2), t, font=f, fill=(20, 20, 20))
save(badge(im, '图2'), 'img03.jpg')

# 图 3：表面进阶
im = erase_on_blue(X(3), 0.3); d = ImageDraw.Draw(im)
for (x0, x1), t in zip([(8, 412), (548, 922), (1060, 1450), (1590, 2026)], ['水/泳池', '蹦床', '沙地', '草地/硬地']):
    d.rectangle([x0, 8, x1, 132], fill='white')
    f = font(48); w = d.textlength(t, font=f)
    d.text(((x0 + x1) / 2 - w / 2, 42), t, font=f, fill=(20, 20, 20))
save(badge(im, '图3'), 'img04.jpg')

save(badge(pair(X(4), X(5)), '图4、5'), 'img05.jpg')
save(badge(X(6), '图6'), 'img06.jpg', W=620)
save(badge(X(7), '图7'), 'img07.jpg')
save(badge(X(8), '图8'), 'img08.jpg')
save(badge(erase_on_blue(X(9), 0.7), '图9'), 'img09.jpg')
save(badge(X(10), '图10'), 'img10.jpg')
save(badge(X(11), '图11'), 'img11.jpg', W=700)
save(badge(X(12), '图12'), 'img12.jpg')
save(badge(X(13), '图13'), 'img13.jpg')
x14 = erase_on_blue(X(14), 0.3)
save(badge(x14.copy(), '图14'), 'img14.jpg')
save(badge(X(15), '图15'), 'img15.jpg')

c = erase_on_blue(X(9), 0.7); w, h = c.size; ch = round(w * 383 / 900)
c.crop((0, 20, w, 20 + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
