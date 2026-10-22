#!/usr/bin/env python3
"""Zou 等 2024 PSSE 联合手法治疗青少年特发性脊柱侧弯：首图中文标题卡；原文图 1 运动照片直接使用（图中只有 a～l 字母），加中文图注；
干预方案卡为编者根据原文整理；主要结果图为编者根据原文表 3 数据用中文绘制。
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
dr.text((70, 50), '非随机对照研究 · 《BMC 肌肉骨骼疾病》2024', font=font(32), fill=TEAL)
dr.text((70, 130), '脊柱侧弯特定运动疗法联合手法治疗', font=font(54), fill=INK)
dr.text((70, 210), '青少年特发性脊柱侧弯的疗效', font=font(54), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Zou W, Li Y, Zhang Z, Jia G, Huang H, Zhang G, Wang C, Lo WLA, Liu P.', font=font(28), fill=GREY)
dr.text((70, 405), 'BMC Musculoskelet Disord. 2024;25:874', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文解读，仅作学术交流（原文 CC BY-NC-ND 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(raw(75), '原文图 1  PSSE 动作示例。a～f：以核心稳定为主的肌力训练体位；g、h：站立位双肩外展外旋；'
                     'i、j：通过牵伸侧弯弧度的强化矫正练习；k：呼吸训练（包括卧位和坐位）。原文图注没有说明 l'), 3)

blocks = [('分组（非随机，由患者和家长自选）', '干预组 17 人：门诊有治疗师监督的 PSSE 50 分钟 + 手法 10 分钟\n对照组 14 人：治疗师教会后，在家由家长录像监督做 PSSE 50 分钟\n两组都是每周 3 次、共 4 周，都接受常规健康教育', LT, TEAL),
          ('PSSE（基于 Schroth 和 SEAS 原则）', '脊柱稳定 / 核心训练 + 呼吸训练（吸气进凹侧、从凸侧呼气）+ 姿势矫正 + 三维自我矫正；用瑜伽球调整骨盆位置；难度按个人情况调整', GR, (40, 130, 60)),
          ('手法（每次 PSSE 之前）', '先做 3 分钟脊柱旁肌筋膜和肌肉按摩放松 → 再用高速低幅（HVLA）推扳手法，以顶椎为中心向两端，作用于对线异常的节段', OR, (200, 110, 30)),
          ('评估（干预前后，评估者设盲）', '主要：Cobb 角（全脊柱正位 X 线）\n次要：倾角计测脊柱活动度；DIERS 表面形貌测躯干形态；FMS；SRS-22 生活质量', PK, RED)]
save(card(1200, '研究设计和干预方案（编者根据原文整理）', blocks), 2)

fig, ax = plt.subplots(1, 3, figsize=(12, 4.6), dpi=100)
data = [('Cobb 角（°）', (21.58, 18.58), (18.00, 19.14), '越低越好'),
        ('FMS 总分', (13.52, 15.11), (14.78, 14.78), '越高越好'),
        ('SRS-22 总分', (85.82, 89.82), (87.42, 86.57), '越高越好')]
for a, (t, iv, cv, note) in zip(ax, data):
    a.plot([0, 1], iv, '-o', color='#00788c', lw=2.5, label='干预组（PSSE + 手法，17 人）')
    a.plot([0, 1], cv, '--s', color='#c8641e', lw=2.5, label='对照组（居家 PSSE，14 人）')
    for x in (0, 1):
        up_i = iv[x] >= cv[x]
        a.annotate(f'{iv[x]:.2f}', (x, iv[x]), textcoords='offset points', xytext=(0, 9 if up_i else -18), ha='center', color='#00788c', fontsize=11)
        a.annotate(f'{cv[x]:.2f}', (x, cv[x]), textcoords='offset points', xytext=(0, -18 if up_i else 9), ha='center', color='#c8641e', fontsize=11)
    a.set_xticks([0, 1]); a.set_xticklabels(['干预前', '4 周后'], fontsize=12); a.set_xlim(-0.3, 1.3)
    lo, hi = min(iv + cv), max(iv + cv); pad = (hi - lo) * 0.45 + 0.5; a.set_ylim(lo - pad, hi + pad)
    a.set_title(f'{t}（{note}）', fontsize=13); a.spines[['top', 'right']].set_visible(False); a.grid(axis='y', alpha=0.3)
h, l = ax[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', ncol=2, fontsize=12, frameon=False)
fig.tight_layout(rect=(0, 0.08, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '主要结果（编者根据原文表 3 均值绘制）。组别×时间交互作用：Cobb 角 P=0.001，FMS P=0.004，SRS-22 P=0.001；'
                                              '但 Cobb 角的时间主效应不显著（P=0.114），干预组 3° 的下降也没有达到 5° 的最小临床重要差异'), 4)

c = raw(75).crop((1040, 352, 1891, 714)).resize((900, 383), Image.LANCZOS)
c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
