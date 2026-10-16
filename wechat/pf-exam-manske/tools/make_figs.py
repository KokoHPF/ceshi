#!/usr/bin/env python3
"""Manske & Davies 2016：照片中 T 恤上的英文字（FAST AS）和袜子商标模糊处理；24 张图按比例等高拼排并标图号；封面取自图 19。
用法：python3 make_figs.py <素材目录（x01..x24.png、title.png）> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)

# 需模糊的区域（各图原始像素坐标）
BLUR = {5: [(540, 0, 720, 155)], 7: [(700, 600, 1060, 795)], 9: [(775, 495, 850, 540)],
        10: [(300, 260, 540, 500)], 11: [(265, 300, 510, 610)], 12: [(235, 290, 505, 610)],
        13: [(245, 290, 525, 610)], 14: [(240, 320, 490, 610)], 16: [(340, 290, 525, 530)],
        17: [(0, 830, 120, 960)]}


def X(i):
    im = Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')
    for b in BLUR.get(i, []):
        b = (max(0, b[0]), max(0, b[1]), min(im.width, b[2]), min(im.height, b[3]))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(16)), b[:2])
    return im


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(28, im.height // 16))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def row(nums, gap=12, H=800):
    ims = []
    for n in nums:
        im = X(n)
        im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
        ims.append(badge(im, f'图{n}'))
    out = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), H), 'white'); x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width + gap
    return out


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=86)


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')
save(row([1]), 'img02.jpg', W=760)
save(row([2, 3, 4]), 'img03.jpg')
save(row([5, 6]), 'img04.jpg')
save(row([7, 8]), 'img05.jpg')
save(row([9, 10]), 'img06.jpg')
save(row([11, 12, 13, 14]), 'img07.jpg')
save(row([15, 16]), 'img08.jpg')
save(row([17, 18]), 'img09.jpg')
save(row([19, 20]), 'img10.jpg')
save(row([21, 22]), 'img11.jpg')
save(row([23, 24]), 'img12.jpg')

c = X(19); w, h = c.size; ch = round(w * 383 / 900); y = 200
c.crop((0, y, w, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('done')
