#!/usr/bin/env python3
"""Kaur 等 2020 下肢和躯干动力链募集对前锯肌激活的影响：首图中文标题卡；原文图 1～6 动作照片直接使用（稳定 / 不稳定平面各一排），加中文图注；
肌电结果图为编者根据原文表 2～7 数据用中文绘制；动作对比卡为编者根据原文整理。
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
SRC = _os.path.join(HERE, '..', 'src')

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 45), '原创研究 · 《国际运动物理治疗杂志》2020', font=font(32), fill=TEAL)
dr.text((70, 115), '下肢和躯干动力链募集对稳定与不稳定平面上', font=font(48), fill=INK)
dr.text((70, 185), '前出拳加强动作中前锯肌激活的影响', font=font(48), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Kaur N, Bhanot K, Ferreira G.', font=font(28), fill=GREY)
dr.text((70, 375), 'Int J Sports Phys Ther. 2020;15(1):126-138', font=font(28), fill=GREY)
dr.text((70, 440), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

blocks = [('动作 1 / 4：前出拳加强（FPP）', '双脚平行站立，优势侧屈肘 90°、前臂中立放在体侧 → 肩前屈到 90°、伸直肘、肱骨内旋 45°，并前伸肩胛（“出拳到底再往前送”）→ 原路收回', LT, TEAL),
          ('动作 2 / 5：闭链“塞拉佩”FPP（CS）', '出拳的同时躯干转向对侧，对侧腿屈髋内收、向前迈一步并越过身体中线落地（步长 = 腿长的 75%，地面贴胶带标记）', GR, (40, 130, 60)),
          ('动作 3 / 6：开链“塞拉佩”FPP（OS）', '出拳的同时躯干转向对侧，对侧腿屈髋内收、向前摆过身体中线但不落地，靠单腿保持平衡', OR, (200, 110, 30)),
          ('统一要求', '尽全力出拳，拳头碰到最大够距处的标记；节拍器 50 次 / 分钟，出拳和收回各 1 拍；每个动作 3 次，次间至少休息 5 秒，动作间至少休息 2 分钟\n动作 1～3 在地面（稳定），4～6 在 BOSU 球上（不稳定），顺序随机', PK, RED)]
save(card(1200, '六个动作（编者根据原文整理）', blocks), 2)

save(capbox(row([raw(17), raw(18), raw(19)]), '原文图 1～3：稳定平面。左：前出拳加强（FPP）；中：闭链塞拉佩（CS），对侧腿向前迈步越过中线；右：开链塞拉佩（OS），对侧腿向前摆、不落地'), 3)
save(capbox(row([raw(20), raw(24), raw(25)]), '原文图 4～6：不稳定平面（BOSU 球）。左：FPP；中：CS（图中迈步脚落在第二个 BOSU 上）；右：OS'), 4)

M = [('前锯肌', [85.50, 132.54, 160.65], [84.98, 138.40, 157.39], [(65.85, 105.15), (92.95, 172.13), (114.70, 206.60)], [(67.82, 102.14), (95.46, 181.33), (107.21, 207.57)]),
     ('腹外斜肌', [52.08, 78.75, 92.68], [53.83, 85.87, 87.79], [(42.15, 62.01), (63.90, 93.59), (77.18, 108.17)], [(42.05, 65.60), (70.40, 101.34), (70.52, 105.06)]),
     ('大腿内收肌', [14.87, 67.34, 111.52], [33.92, 73.00, 110.82], [(8.90, 20.83), (36.82, 97.87), (65.21, 157.81)], [(9.99, 57.85), (32.60, 113.41), (46.78, 174.86)]),
     ('对侧臀大肌', [12.27, 16.27, 13.41], [10.12, 14.07, 12.53], [(6.39, 18.16), (10.18, 22.36), (8.82, 17.99)], [(7.49, 12.75), (9.97, 18.18), (9.19, 15.87)]),
     ('同侧臀大肌', [15.91, 25.16, 33.20], [16.70, 22.46, 31.18], [(12.72, 19.09), (19.41, 30.91), (24.23, 42.16)], [(13.30, 20.10), (18.05, 26.87), (21.85, 40.51)]),
     ('背阔肌', [41.63, 43.80, 57.27], [37.03, 39.79, 54.32], [(27.69, 55.57), (29.24, 58.39), (36.24, 78.29)], [(28.05, 46.02), (29.53, 50.05), (33.15, 75.79)])]
fig, axs = plt.subplots(2, 3, figsize=(13, 8), dpi=100)
for a, (name, st, un, cs, cu) in zip(axs.flat, M):
    x = np.arange(3); w = 0.36
    for off, vals, ci, col, lab in [(-w / 2, st, cs, '#7fb3bf', '稳定平面'), (w / 2, un, cu, '#00788c', '不稳定平面（BOSU）')]:
        err = np.array([[v - c[0] for v, c in zip(vals, ci)], [c[1] - v for v, c in zip(vals, ci)]])
        a.bar(x + off, vals, w, color=col, label=lab, yerr=err, capsize=3, error_kw={'elinewidth': 1, 'ecolor': '#555'})
    a.set_xticks(x); a.set_xticklabels(['FPP', 'CS', 'OS'], fontsize=11); a.set_title(name + '（%MVIC）', fontsize=13)
    a.spines[['top', 'right']].set_visible(False); a.grid(axis='y', alpha=0.3)
    if name == '前锯肌': a.axhline(100, color='#be2832', lw=1, ls='--')
h, l = axs[0, 0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', ncol=2, fontsize=12, frameon=False)
fig.tight_layout(rect=(0, 0.05, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '六块肌肉在三个动作、两种平面上的平均肌电（%MVIC），误差线为 95% 置信区间（编者根据原文表 2～7 绘制）。'
                                              '前锯肌图中虚线为 100% MVIC。FPP：前出拳加强；CS：闭链塞拉佩；OS：开链塞拉佩'), 5)

c = row([raw(18), raw(19)]); k = 900 / c.width; c = c.resize((900, round(c.height * k)), Image.LANCZOS)
y0 = max(0, round(c.height * 0.12)); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
