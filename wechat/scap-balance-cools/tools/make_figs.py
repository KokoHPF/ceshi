#!/usr/bin/env python3
"""Cools 等 2007 肩胛肌平衡训练：首图中文标题卡；原文图 1～4 照片直接使用并加中文图注；
分级标准与推荐动作卡为编者根据原文整理。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys, os
import numpy as np
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
raw = lambda x: Image.open(BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def relabel(im, items, bg='white'):
    """items: (box@1000宽, 文字, 字号@1000宽, 对齐)"""
    s = im.width / 1000; d = ImageDraw.Draw(im)
    for box, t, fs, *al in items:
        b = [int(v * s) for v in box]
        d.rectangle(b, fill=bg)
        f = font(fs * s); lines = t.split('\n'); lh = fs * s * 1.25
        y0 = (b[1] + b[3]) / 2 - lh * len(lines) / 2
        for i, l in enumerate(lines):
            w = d.textlength(l, font=f)
            x = b[0] + 2 if al and al[0] == 'l' else (b[0] + b[2]) / 2 - w / 2
            d.text((x, y0 + i * lh), l, font=f, fill='black')
    return im


def blur(im, boxes, r=10):
    s = im.width / 1000
    for b0 in boxes:
        b = tuple(int(v * s) for v in b0); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * s)), b[:2])
    return im
def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def card(W, title, blocks, bg=(246, 248, 250)):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


up = lambda im, w=1000: im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def lab(im, page_bbox, items, fs=30, pad=6):
    """items: (页面 x, 页面 y, 中文, 颜色)；按 PDF 坐标映射到图像，白底写字"""
    x0, y0, x1, y1 = page_bbox; s = im.width / (x1 - x0); dr = ImageDraw.Draw(im)
    for x, y, t, *c in items:
        X, Y = (x - x0) * s, (y - y0) * s; f = font(fs)
        lines = t.split('\n'); w = max(dr.textlength(l, font=f) for l in lines); h = fs * 1.2 * len(lines)
        dr.rounded_rectangle([X - pad, Y - pad, X + w + pad, Y + h + pad], 6, fill=(255, 255, 255))
        for i, l in enumerate(lines): dr.text((X, Y + i * fs * 1.2), l, font=f, fill=c[0] if c else INK)
    return im


def row(ims, W=1200, gap=12):
    h = min(i.height for i in ims); ims = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in ims]
    tw = sum(i.width for i in ims) + gap * (len(ims) - 1); s = W / tw
    ims = [i.resize((round(i.width * s), round(h * s)), Image.LANCZOS) for i in ims]
    out = Image.new('RGB', (W, ims[0].height), 'white'); x = 0
    for i in ims: out.paste(i, (x, 0)); x += i.width + round(gap * s)
    return out


def stack(ims, gap=14):
    W = max(i.width for i in ims); out = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: out.paste(i, (0, y)); y += i.height + gap
    return out


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '对照实验室研究 · 《美国运动医学杂志》2007', font=font(32), fill=TEAL)
dr.text((70, 130), '肩胛肌平衡的康复：', font=font(56), fill=INK)
dr.text((70, 215), '该开哪些训练动作？', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 365), 'Cools AM, Dewitte V, Lanszweert F, et al. Am J Sports Med 2007;35(10):1744-1751', font=font(28), fill=GREY)
dr.text((70, 420), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(up(raw(13), 1200), '原文图 1：恢复斜方肌内部平衡的动作。A 侧卧前屈；B 侧卧外旋；C 俯卧水平外展加外旋；D 俯卧后伸。'
                                 'A、B、C 最适合纠正上斜方 / 下斜方失衡，A、B、D 最适合纠正上斜方 / 中斜方失衡'), 2)
save(capbox(row([raw(14), raw(15), raw(19)]), '原文图 2～4（从左到右）：高位划船；站立前屈；外旋位肩胛面上举。'
                                               '这三个是上斜方 / 前锯肌比值最低的前三名，但都没达到“优秀”标准'), 3)

blocks = [('比值怎么算', '用表面肌电测上、中、下斜方肌和前锯肌的激活（占最大自主收缩的百分比），算出 上斜方/下斜方、上斜方/中斜方、上斜方/前锯肌 三个比值，乘以 100。'
           '低于 100% 说明目标肌比上斜方肌更活跃，越低越好。', LT, TEAL),
          ('分级标准', '每个动作分向心、等长、离心三个阶段：\n优秀：三个阶段都 <60%\n良好：都 <80%，至少一个阶段在 60%～80%\n中等：显著低于 100%\n不合格：至少一个阶段显著高于 100%', OR, (200, 110, 30)),
          ('上斜方 / 下斜方最低', '侧卧前屈、侧卧外旋、俯卧水平外展加外旋', GR, (40, 130, 60)),
          ('上斜方 / 中斜方最低', '侧卧前屈、侧卧外旋、俯卧后伸', GR, (40, 130, 60)),
          ('上斜方 / 前锯肌', '没有一个动作达到优秀；最好的是高位划船（良好），其次站立前屈、外旋位肩胛面上举（中等）。练前锯肌要另选俯卧撑加强等动作', PK, RED)]
save(card(1200, '比值、分级和推荐动作（编者根据原文整理）', blocks), 4)

c = up(raw(13), 900); c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
