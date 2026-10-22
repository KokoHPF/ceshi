#!/usr/bin/env python3
"""Boob 等 2024 足底筋膜炎物理治疗病例报告：首图中文标题卡；原文图 1、3～7 直接使用（只有 A、B 字母），加中文图注；
原文图 2 时间轴用中文重绘；结局对比图为编者根据原文表 2 绘制。
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
dr.text((70, 50), '病例报告 · 《Cureus》2024', font=font(32), fill=TEAL)
dr.text((70, 135), '一名 45 岁女性足底筋膜炎的', font=font(56), fill=INK)
dr.text((70, 215), '综合物理治疗康复方案：病例报告', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Boob MA, Phansopkar P, Somaiya KJ.', font=font(28), fill=GREY)
dr.text((70, 405), 'Cureus. 2024;16(1):e51585', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文重排，仅作学术交流（原文 CC BY 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 2 时间轴（中文重绘）
im = Image.new('RGB', (1200, 360), 'white'); dr = ImageDraw.Draw(im)
cols = [((70, 115, 195), '2023-09-02', '患者因足跟痛\n到物理治疗科就诊'), ((112, 173, 71), '2023-09-03', '进行影像学检查'),
        ((237, 125, 49), '2023-09-04', '开始物理治疗康复'), ((150, 150, 150), '2023-10-18', '物理治疗结束，\n给予家庭训练建议')]
x0 = 40; w = 270; gap = botw = 12
for k, (c, d, t) in enumerate(cols):
    x = x0 + k * (w + 13)
    dr.rectangle([x, 30, x + w + 13, 50], fill=c)
    dr.line([x + w / 2, 50, x + w / 2, 110], fill=c, width=4)
    dr.rectangle([x, 110, x + w, 320], outline=c, width=4); dr.rectangle([x, 110, x + w, 170], fill=c)
    f = font(34); dr.text((x + w / 2 - dr.textlength(d, font=f) / 2, 120), d, font=f, fill='white')
    y = 200
    for l in t.split('\n'):
        f = font(30); dr.text((x + 20, y), l, font=f, fill=INK); y += 46
save(capbox(im, '原文图 2（编者中文重绘）  事件时间轴'), 3)

save(capbox(raw(36), '原文图 1  右踝侧位 X 线片，红圈处可见跟骨骨刺'), 2)
save(capbox(raw(64), '原文图 3  超声治疗足底筋膜炎疼痛：作用于跟骨内侧结节，频率 1 MHz，强度 1.8 W/cm²，8 分钟'), 4)
save(capbox(raw(73), '原文图 4  足底筋膜炎的肌内效贴扎'), 5)
save(capbox(raw(82), '原文图 5  足内在肌强化。A：踩球滚动；B：毛巾抓卷'), 6)
save(capbox(raw(91), '原文图 6  踝关节本体感觉神经肌肉促进（PNF），用于改善平衡。A：跖屈加内翻；B：背伸加外翻'), 7)
save(capbox(raw(100), '原文图 7  本体感觉训练。A：站平衡板；B：双侧提踵'), 8)

fig, ax = plt.subplots(1, 4, figsize=(13, 4.2), dpi=100)
data = [('疼痛 NPRS（分）', 7, 3), ('足功能指数 FFI（%）', 60, 20), ('背伸活动度（°）', 8, 20), ('背伸肌力（MMT 级）', 3, 5)]
for a, (t, pre, post) in zip(ax, data):
    bars = a.bar([0, 1], [pre, post], 0.55, color=['#9fb7bd', '#00788c'])
    for r, v in zip(bars, [pre, post]): a.text(r.get_x() + r.get_width() / 2, v, f'{v}', ha='center', va='bottom', fontsize=12)
    a.set_xticks([0, 1]); a.set_xticklabels(['治疗前', '治疗后'], fontsize=12); a.set_ylim(0, max(pre, post) * 1.25)
    a.set_title(t, fontsize=13); a.spines[['top', 'right']].set_visible(False); a.grid(axis='y', alpha=0.3)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '治疗前后结局（编者根据原文表 2 绘制）。疼痛和足功能指数越低越好；跖屈活动度（50°）和跖屈肌力（5 级）前后不变'), 9)

c = raw(82); k = 900 / c.width; c = c.resize((900, round(c.height * k)), Image.LANCZOS)
y0 = (c.height - 383) // 2; c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
