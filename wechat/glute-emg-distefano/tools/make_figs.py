#!/usr/bin/env python3
"""Distefano 等 2009 臀肌肌电：首图中文标题卡；原文图 1～9 动作照片直接使用并加中文标签和图注；
臀中肌、臀大肌激活柱状图按原文表 2、表 3 数值绘制。
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
dr.text((70, 50), '实验室研究 · 《骨科与运动物理治疗杂志》2009', font=font(32), fill=TEAL)
dr.text((70, 130), '常用治疗性训练中的臀肌激活', font=font(60), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 335), 'Distefano LJ, Blackburn JT, Marshall SW, Padua DA.', font=font(28), fill=GREY)
dr.text((70, 380), 'J Orthop Sports Phys Ther 2009;39(7):532-540', font=font(28), fill=GREY)
dr.text((70, 445), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


def tagged(x, t):
    im = raw(x); dr = ImageDraw.Draw(im); f = font(max(18, im.height // 14)); w = dr.textlength(t, font=f)
    dr.rounded_rectangle([8, im.height - f.size - 26, 24 + w, im.height - 8], 8, fill=(255, 255, 255))
    dr.text((16, im.height - f.size - 20), t, font=f, fill=INK); return im


save(capbox(row([tagged(160, '蚌式（屈髋 60°）'), tagged(164, '侧卧髋外展')]),
            '原文图 1（左）：屈髋 60° 蚌式，A 起止位、B 中间位；原文图 2（右）：侧卧髋外展的中间位（外展到 30°）'), 2)
save(capbox(row([tagged(165, '单腿深蹲'), tagged(163, '单腿硬拉'), tagged(162, '弹力带侧向走')]),
            '原文图 3～5（从左到右）：单腿深蹲；单腿硬拉；弹力带侧向走'), 3)
save(capbox(row([tagged(175, '前弓步'), tagged(174, '侧弓步'), tagged(176, '旋转弓步'), tagged(177, '单腿跳落地')]),
            '原文图 6～9（从左到右）：前弓步；侧弓步；旋转弓步（转体 135°）；多方向单腿跳的落地姿势'), 4)

gm = [('侧卧髋外展', 81), ('单腿深蹲', 64), ('弹力带侧向走', 61), ('单腿硬拉', 58), ('侧向单腿跳', 57), ('旋转单腿跳', 48), ('旋转弓步', 48),
      ('向前单腿跳', 45), ('前弓步', 42), ('蚌式（屈髋 30°）', 40), ('侧弓步', 39), ('蚌式（屈髋 60°）', 38)]
gx = [('单腿深蹲', 59), ('单腿硬拉', 59), ('旋转弓步', 49), ('前弓步', 44), ('侧弓步', 41), ('侧卧髋外展', 39), ('侧向单腿跳', 30),
      ('蚌式（屈髋 60°）', 39), ('旋转单腿跳', 35), ('向前单腿跳', 35), ('蚌式（屈髋 30°）', 34), ('弹力带侧向走', 27)]
fig, axs = plt.subplots(1, 2, figsize=(13, 7.2), dpi=100)
for ax, data, t, c in ((axs[0], gm, '臀中肌', '#2e7d9a'), (axs[1], gx, '臀大肌', '#c0504d')):
    names = [d[0] for d in data][::-1]; v = [d[1] for d in data][::-1]
    ax.barh(names, v, color=c); ax.axvspan(50, 60, color='#f5c242', alpha=0.25, lw=0)
    for i, val in enumerate(v): ax.text(val + 1, i, str(val), va='center', fontsize=12)
    ax.set_xlim(0, 95); ax.set_title(t + '（%MVIC，按原文排序）', fontsize=15); ax.tick_params(labelsize=12)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.5, 0.01, '黄色带：50%～60% MVIC，常被认为是有助于增强肌力的激活门槛', ha='center', fontsize=12, color='#8a6d00')
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(f'{OUT}/_c.png'); plt.close(fig)
ch = Image.open(f'{OUT}/_c.png').convert('RGB'); os.remove(f'{OUT}/_c.png')
save(capbox(ch, '12 个动作的臀中肌、臀大肌平均激活（编者按原文表 2、表 3 数值绘制；臀大肌表中“侧向单腿跳”原文均值 30 与其置信区间不符，见正文）'), 5)

c = row([raw(165), raw(163), raw(162)], 900); y0 = max(0, (c.height - 383) // 2); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
