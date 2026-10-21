#!/usr/bin/env python3
"""Askling 等 2013 腘绳肌急性损伤两种康复方案：首图中文标题卡；原文图 1～6 动作照片直接使用并加中文标签和图注；
图 7～10 箱线图的英文标注按 OCR 定位（src/o<xref>.json）改为中文；方案对比卡为编者根据原文整理。
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


import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0, HERE)
import zh
SRC = _os.path.join(HERE, '..', 'src')

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '随机对照试验 · 《英国运动医学杂志》2013', font=font(32), fill=TEAL)
dr.text((70, 125), '瑞典精英足球中的急性腘绳肌损伤：', font=font(52), fill=INK)
dr.text((70, 200), '比较两种康复方案的前瞻性', font=font(52), fill=INK)
dr.text((70, 275), '随机对照临床试验', font=font(52), fill=INK)
dr.line([70, 375, W - 70, 375], fill=(200, 205, 210), width=2)
dr.text((70, 405), 'Askling CM, Tengvar M, Thorstensson A. Br J Sports Med 2013;47:953-959', font=font(28), fill=GREY)
dr.text((70, 460), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


def tagged(x, t):
    im = raw(x); dr = ImageDraw.Draw(im); f = font(max(24, im.height // 12)); w = dr.textlength(t, font=f)
    dr.rounded_rectangle([10, 10, 30 + w, 22 + f.size], 8, fill=(255, 255, 255)); dr.text((20, 14), t, font=f, fill=INK); return im


save(capbox(row([tagged(5, 'L-1 伸膝器'), tagged(16, 'L-2 潜水者'), tagged(18, 'L-3 滑行者')]),
            'L 方案（拉长型）三个动作。原文图 1：L-1 “伸膝器”；原文图 2：L-2 “潜水者”；原文图 3：L-3 “滑行者”'), 2)
save(capbox(row([tagged(15, 'C-1 收缩-放松牵伸'), tagged(17, 'C-2 拉力器摆腿'), tagged(23, 'C-3 臀桥')]),
            'C 方案（常规型）三个动作。原文图 4：C-1 收缩-放松牵伸；原文图 5：C-2 拉力器摆腿；原文图 6：C-3 臀桥'), 3)

COMMON = [('Max', '最大值'), ('Min', '最小值'), ('L-protocol', 'L 方案'), ('C-protocol', 'C 方案')]


def relab(x, spec, extra=()):
    im, _ = zh.apply(raw(x), f'{SRC}/o{x}.json', spec, W=1200, extra=extra); return im


f7 = relab(27, COMMON + [(['Time to return (', '(days)'], '恢复时间（天）', {'rot': True})], extra=[((0, 240, 40, 300), '', {})])
f8 = relab(28, COMMON + [('Time to return (days)', '恢复时间（天）'), ('Sprinting-type', '冲刺型'), ('Stretching-type', '牵拉型')])
f9 = relab(29, COMMON + [('Time to return (days)', '恢复时间（天）'), ('PT not involved', '未累及近端游离腱'), ('PT involved', '累及近端游离腱')])
f10 = relab(33, [(['L-protocol', 'sprinting-type'], 'L 方案\n冲刺型'), (['Time to return (', '(days)'], '恢复时间（天）', {'rot': True}),
                ('MRl-negative', '磁共振阴性')] + COMMON, extra=[((0, 240, 40, 300), '', {})])
save(capbox(row([f7, f8]), '原文图 7（左）：两种方案的恢复时间（L 方案 37 人，C 方案 38 人）；原文图 8（右）：按损伤类型分组（冲刺型 / 牵拉型）。'
                            '箱体为四分位距，横线为中位数，黑方块为均值，须线为均值 ± 1 个标准差；*** p<0.001'), 4)
save(capbox(row([f9, f10]), '原文图 9（左）：按是否累及近端游离腱分组；原文图 10（右）：磁共振阴性者（11 人）与 L 方案冲刺型损伤者（27 人）比较。** p<0.01，*** p<0.001'), 5)

blocks = [('共同点', '伤后第 5 天开始；动作都在矢状面，在哪都能做，不需要复杂器械；每周至少一次有人监督；逐步增加速度和负荷；全程不允许诱发疼痛', LT, TEAL),
          ('L 方案：在长肌肉长度下加载', 'L-1 伸膝器：每天 2 次，3 组 × 12 次\nL-2 潜水者：隔天 1 次，3 组 × 6 次\nL-3 滑行者：每 3 天 1 次，3 组 × 4 次', GR, (40, 130, 60)),
          ('C 方案：常规动作', 'C-1 收缩-放松牵伸：每天 2 次，3 组 × 4 次\nC-2 拉力器摆腿：隔天 1 次，3 组 × 6 次\nC-3 臀桥：每 3 天 1 次，3 组 × 8 次', OR, (200, 110, 30)),
          ('回归标准', '每周临床检查，确认无残留体征（由另一名同事确认）→ Askling H 测试：没有任何不安全感才允许回到全队训练和比赛；否则延长康复，每 3～5 天复测', PK, RED)]
save(card(1200, '两种康复方案对比（编者根据原文整理）', blocks), 6)

c = row([raw(16), raw(18)], 900); y0 = max(0, (c.height - 383) // 2); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
