#!/usr/bin/env python3
"""O'Sullivan 2022 女性运动员腘绳肌损伤：图 1～5 训练动作照片加图号，图 5 背景健身房标语模糊；封面取自图 2。
用法：python3 make_figs.py <素材目录（x01～x05.png、title.png）> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.width // 30))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    im.resize((W, round(im.height * W / im.width)), Image.LANCZOS).save(f'{OUT}/{name}', quality=88)


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)
for i in range(1, 5):
    save(badge(X(i), f'图{i}'), f'img{i + 1:02d}.jpg')
x5 = X(5)
for b in [(195, 28, 435, 74), (905, 38, 1015, 84), (1190, 22, 1440, 68), (0, 38, 35, 74)]:
    x5.paste(x5.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2])
save(badge(x5, '图5'), 'img06.jpg')
x2 = X(2); w, h = x2.size; cw = round(h * 900 / 383)
x2.crop((w - cw, 0, w, h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
