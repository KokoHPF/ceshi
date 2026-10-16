#!/usr/bin/env python3
"""Marrone 2024 跟腱修复术后康复：图 4 跖屈肌进阶流程中文重绘；照片中背景横幅、器械品牌、显示屏文字模糊；封面取自图 1。
原文图号重复（两个图 5、图 6，缺图 8），本文按出现顺序重新编号为图 1～10；同页两图等高并排。
用法：python3 make_figs.py <素材目录（x01～x10.png、title.png）> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def blur(im, boxes, r=12):
    for b in boxes:
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r)), b[:2])
    return im


def badge(im, t, x=None):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 24))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10 if x is None else x; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')


def pair(a, b, ta, tb, H=1100, gap=14):
    a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS)
    b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
    c = Image.new('RGB', (a.width + b.width + gap, H), 'white'); c.paste(a, (0, 0)); c.paste(b, (a.width + gap, 0))
    badge(c, ta, a.width - (ImageDraw.Draw(c).textlength(ta, font=font(H // 24)) + 34)); badge(c, tb)
    return c


def save(im, name, W=1080):
    im.resize((W, round(im.height * W / im.width)), Image.LANCZOS).save(f'{OUT}/{name}', quality=88)


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

# 图 1、2：俯卧屈膝静息踝角度；缩短位跖屈等长 + 测力反馈（模糊背景横幅、器械字样和平板屏幕）
x2 = blur(X(2), [(650, 150, 810, 215), (725, 290, 810, 330), (465, 315, 605, 425)])
save(pair(X(1), x2, '图1', '图2'), 'img02.jpg')

# 图 3、4：坐位跖屈等张；跖屈肌力进阶（中文重绘）
fl = Image.new('RGB', (605, 1095), 'white'); d = ImageDraw.Draw(fl)
steps = ['缩短位次最大强度\n踝跖屈等长', '坐位踝跖屈\n等张训练', '腿举机上踝跖屈', '双腿提踵', '单腿辅助提踵', '单腿提踵', '单腿台阶边缘提踵\n（加大活动范围）']
bh, gap, y = 100, 44, 30
for i, t in enumerate(steps):
    d.rounded_rectangle([60, y, 545, y + bh], 10, fill=(68, 114, 196))
    f = font(36); ls = t.split('\n'); ty = y + bh / 2 - (len(ls) * 44 - 8) / 2
    for l in ls:
        d.text((302 - d.textlength(l, font=f) / 2, ty), l, font=f, fill='white'); ty += 44
    if i < len(steps) - 1:
        cx, ay = 302, y + bh + 6
        d.rectangle([cx - 12, ay, cx + 12, ay + 18], fill=(180, 190, 210))
        d.polygon([(cx - 26, ay + 18), (cx + 26, ay + 18), (cx, ay + 38)], fill=(180, 190, 210))
    y += bh + gap
save(pair(X(3), fl, '图3', '图4'), 'img03.jpg')

# 图 5、6：双腿提踵（经第一跖趾关节）；测力台双腿提踵等长（模糊器械字样和腰带标志）
x6 = blur(X(6), [(605, 580, 712, 615), (420, 355, 475, 390), (755, 370, 795, 405)])
save(pair(X(5), x6, '图5', '图6'), 'img04.jpg')

# 图 7、8：弹力带辅助单腿弹跳；三重伸展扶墙练习（模糊架上品牌和天花板标签）
x8 = blur(X(8), [(460, 36, 522, 66), (228, 4, 292, 36), (78, 205, 116, 226)])
save(pair(X(7), x8, '图7', '图8'), 'img05.jpg')

# 图 9、10：等速测试；站立提踵测试（模糊显示器品牌、屏幕和出口标志）
x9 = blur(X(9), [(112, 40, 370, 240), (138, 0, 182, 44)], r=16)
save(pair(x9, X(10), '图9', '图10'), 'img06.jpg')
x1 = X(1); w = x1.width; ch = round(w * 383 / 900)
x1.crop((0, 200, w, 200 + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
