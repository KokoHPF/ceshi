#!/usr/bin/env python3
"""Lupowitz 2023：照片背景海报上的英文模糊处理；图 1、图 2 等高并排；图 4 “核心四层金字塔”中文重绘；封面取自图 3。
用法：python3 make_figs.py <素材目录（x01..x04.png、title.png）> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def blur(im, boxes):
    for b in boxes:
        reg = im.crop(b).filter(ImageFilter.GaussianBlur(14))
        im.paste(reg, b[:2])
    return im


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 22))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def pair(a, b, ta, tb, H=1100, gap=14):
    a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS)
    b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
    badge(a, ta); badge(b, tb)
    im = Image.new('RGB', (a.width + b.width + gap, H), 'white')
    im.paste(a, (0, 0)); im.paste(b, (a.width + gap, 0))
    return im


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')
f1 = blur(X(1), [(0, 130, 130, 230)])
f2 = blur(X(2), [(460, 110, 720, 215), (1290, 125, 1560, 230), (460, 1225, 720, 1335), (1135, 1238, 1410, 1296)])
f3 = blur(X(3), [(540, 230, 826, 345)])
save(pair(f1, f2, '图1', '图2'), 'img02.jpg')
save(badge(f3.copy(), '图3'), 'img03.jpg', W=700)

# ---------- 图 4：核心四层金字塔 ----------
W, H = 1080, 640
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
d.polygon([(W // 2, 20), (60, H - 30), (W - 60, H - 30)], fill=(68, 114, 196))
layers = [('激活', '减痛 · 呼吸 · 姿势 · 收紧核心', 560, 470, 590, 58),
          ('稳定', '抗运动 · 耐力 · 髋力量比', 440, 355, 455, 48),
          ('整合', '负重功能动作模式', 330, 245, 345, 42),
          ('扰动', '反应 · 双任务', 190, 150, 240, 34)]
for name, sub, w, y0, y1_, fs in layers:
    h = 100 if fs > 40 else 80
    y0 = {'激活': 470, '稳定': 355, '整合': 250, '扰动': 160}[name]
    d.rounded_rectangle([W // 2 - w // 2, y0, W // 2 + w // 2, y0 + h], 14, fill=(234, 239, 248))
    f = font(fs); tw = d.textlength(name, font=f)
    d.text((W // 2 - tw / 2, y0 + 8), name, font=f, fill=(20, 20, 20), stroke_width=1, stroke_fill=(20, 20, 20))
    f2_ = font(22 if fs > 40 else 18); tw = d.textlength(sub, font=f2_)
    d.text((W // 2 - tw / 2, y0 + h - (30 if fs > 40 else 26)), sub, font=f2_, fill=(80, 80, 80))
im.save(f'{OUT}/img04.jpg', quality=92)

c = f3; w, h = c.size; ch = round(w * 383 / 900); y = 300
c.crop((0, y, w, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('done')
