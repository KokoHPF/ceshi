#!/usr/bin/env python3
"""Tsuruike & Ellenbecker 2023 侧卧外展时肩胛后缩对下斜方肌等肌电的影响：首图中文标题卡；图 1 四种体位照片切分后
加中文标签；图 2 侧卧外旋照片；按原文表 1 均值与 95% CI 重绘六块肌肉柱状图；图 7 上/下斜方肌比值按正文与读图重绘。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 13
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def raw(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


def runs(mask, minlen):
    out, s = [], None
    for i, v in enumerate(list(mask) + [False]):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= minlen: out.append((s, i))
            s = None
    return out


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '对照实验室研究 · 《国际运动物理治疗杂志》（IJSPT）2023', font=font(32), fill=TEAL)
for i, t in enumerate(['侧卧外展练下斜方肌：', '肩胛先“收”一下，差别有多大？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '20 名大学棒球运动员 · 6 块肌肉表面肌电 · 4 种姿势 × 2 种负荷', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Tsuruike M, Ellenbecker TS. IJSPT 2023;18(3):715-725', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，原文以 CC BY-NC 4.0 开放获取', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1：四种体位 ----------
g = raw(80); a = np.array(g.convert('L')) < 235
cols = runs(a.sum(0) > a.shape[0] * 0.3, 60); rows = runs(a.sum(1) > a.shape[1] * 0.3, 60)
cells = [g.crop((c0, r0, c1, r1)) for (r0, r1) in rows for (c0, c1) in cols]
LAB = ['① 中立位 + 前伸', '② 水平内收 15° + 前伸', '③ 中立位 + 后缩', '④ 水平内收 15° + 后缩']
cw = 520; cells = [c.resize((cw, round(c.height * cw / c.width)), Image.LANCZOS) for c in cells]
ch = max(c.height for c in cells); gap = 20
W = 2 * cw + 3 * gap; H = 96 + 2 * (ch + 70) + gap
out = Image.new('RGB', (W, H), 'white'); od = ImageDraw.Draw(out)
od.rectangle([0, 0, W, 80], fill=TEAL); od.text((24, 16), '原文图 1　侧卧 90° 外展的四种姿势', font=font(42), fill='white')
for k, c in enumerate(cells):
    x = gap + (k % 2) * (cw + gap); y = 96 + (k // 2) * (ch + 70)
    out.paste(c, (x, y)); f = font(32); t = LAB[k]
    od.text((x + cw / 2 - od.textlength(t, font=f) / 2, y + ch + 14), t, font=f, fill=INK)
save(out, 2)

# ---------- 图 2：侧卧外旋 ----------
ph = raw(92); w = 800; ph = ph.resize((w, round(ph.height * w / ph.width)), Image.LANCZOS)
out = Image.new('RGB', (w, ph.height + 90), 'white'); od = ImageDraw.Draw(out)
od.rectangle([0, 0, w, 76], fill=TEAL); od.text((24, 16), '原文图 2　侧卧等长外旋（腋下垫毛巾）', font=font(38), fill='white')
out.paste(ph, (0, 90)); save(out, 3)

# ---------- 表 1 重绘：六块肌肉 ----------
CON = ['9.1 kg\n前伸', '9.1 kg\n后缩', '40% 徒手\n前伸', '40% 徒手\n后缩']
T1 = {  # 肌肉: [(NEUT 均值, lo, hi), (HADD 均值, lo, hi)] × 4 条件
    '下斜方肌': [((5, 3, 7), (21, 15, 27)), ((24, 20, 29), (55, 49, 62)), ((16, 11, 21), (18, 13, 24)), ((38, 30, 45), (45, 37, 52))],
    '冈下肌': [((16, 12, 19), (33, 26, 40)), ((13, 11, 15), (41, 33, 48)), ((20, 16, 24), (23, 18, 27)), ((17, 13, 21), (22, 17, 26))],
    '三角肌后束': [((17, 14, 20), (50, 42, 58)), ((8, 6, 11), (28, 23, 33)), ((38, 32, 43), (44, 38, 50)), ((20, 16, 24), (21, 17, 24))],
    '三角肌中束': [((26, 21, 31), (49, 42, 56)), ((14, 11, 17), (27, 22, 32)), ((42, 36, 47), (46, 39, 52)), ((24, 19, 28), (22, 17, 26))],
    '上斜方肌': [((3, 2, 4), (6, 3, 8)), ((11, 5, 16), (12, 9, 16)), ((6, 4, 8), (5, 4, 7)), ((15, 12, 17), (15, 11, 18))],
    '前锯肌': [((10, 6, 14), (7, 5, 9)), ((9, 7, 11), (5, 4, 6)), ((4, 3, 5), (4, 3, 6)), ((4, 3, 5), (4, 3, 6))],
}
fig, axs = plt.subplots(3, 2, figsize=(11, 12), dpi=140, sharey=True)
x = np.arange(4)
for ax, (m, v) in zip(axs.flat, T1.items()):
    for j, (lab, col) in enumerate([('中立位', '#9bbbd4'), ('水平内收 15°', '#1f5f8b')]):
        mu = [c[j][0] for c in v]; lo = [c[j][0] - c[j][1] for c in v]; hi = [c[j][2] - c[j][0] for c in v]
        ax.bar(x + (j - .5) * .38, mu, .38, color=col, yerr=[lo, hi], capsize=3, label=lab)
        for xi, mi, h in zip(x, mu, hi):
            ax.text(xi + (j - .5) * .38, mi + h + 1.5, str(mi), ha='center', fontsize=10)
    ax.axvspan(.5, 1.5, color='#fff3a3', alpha=.35, zorder=0); ax.axvspan(2.5, 3.5, color='#fff3a3', alpha=.35, zorder=0)
    ax.set_title(m, fontsize=15); ax.set_xticks(x); ax.set_xticklabels(CON, fontsize=11); ax.set_ylim(0, 70)
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
axs[0, 0].legend(frameon=False, loc='upper left', fontsize=11)
for a in axs[:, 0]: a.set_ylabel('% 最大自主等长收缩')
fig.suptitle('侧卧 90° 外展等长收缩时各肌肉激活（黄底＝肩胛后缩；误差线为 95% CI）', fontsize=15)
fig.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 4)

# ---------- 图 7：上/下斜方肌比值 ----------
R = {'中立位': [1.01, 0.50, 0.50, 0.45], '水平内收 15°': [0.32, 0.23, 0.44, 0.37]}
fig, ax = plt.subplots(figsize=(9, 4.8), dpi=150)
for j, (lab, col) in enumerate(zip(R, ['#9bbbd4', '#1f5f8b'])):
    ax.bar(x + (j - .5) * .38, R[lab], .38, color=col, label=lab)
    for xi, v in zip(x, R[lab]): ax.text(xi + (j - .5) * .38, v + .02, f'{v:.2f}', ha='center', fontsize=11)
ax.set_xticks(x); ax.set_xticklabels([c.replace('\n', ' ') for c in CON]); ax.set_ylim(0, 1.2)
ax.set_ylabel('上斜方肌 / 下斜方肌'); ax.legend(frameon=False)
for s in ['top', 'right']: ax.spines[s].set_visible(False)
ax.set_title('上/下斜方肌激活比值（越低越好）', fontsize=14)
fig.text(.5, .01, '9.1 kg 四个数值取自原文正文；40% 徒手两组为读图近似值', ha='center', fontsize=10, color='#666')
fig.tight_layout(rect=(0, .04, 1, 1)); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 5)
import os; os.remove(f'{OUT}/_p.png')

# ---------- 封面 900×383 ----------
c = raw(92); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = int(c.height * 0.12); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
