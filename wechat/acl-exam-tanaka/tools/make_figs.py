#!/usr/bin/env python3
"""Tanaka 2022：图 2（文献筛选流程）、图 3（偏倚风险）、图 4/5（森林图）、图 6（SROC 曲线）按原图数据中文重绘；
图 1 照片加图号；封面取自图 1。
用法：python3 make_figs.py <素材目录（x01.png、title.png）> <输出目录>"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
RED = (171, 25, 66); INK = (25, 25, 25)
font = lambda s: ImageFont.truetype(F, s)

# ---------- 数据（读自原文图 4～6） ----------
ST = {
    '拉赫曼试验': ['Jarbo 2017', 'Lee 1988', 'Massey 2017', 'Gürpınar 2019', 'Kıyak 2018', 'Mulligan 2015', 'Mulligan 2017', 'Kostov 2014'],
    '前抽屉试验': ['Jarbo 2017', 'Lee 1988', 'Massey 2017', 'Gürpınar 2019', 'Kıyak 2018', 'Kostov 2014'],
    '轴移试验': ['Jarbo 2017', 'Massey 2017', 'Gürpınar 2019', 'Kıyak 2018', 'Kostov 2014'],
    '杠杆征试验': ['Jarbo 2017', 'Massey 2017', 'Gürpınar 2019', 'Mulligan 2017'],
}
SENS = {
    '拉赫曼试验': ([(.91, .78, .97), (.91, .72, .99), (.89, .79, .95), (.81, .69, .90), (.37, .22, .54), (.81, .54, .96), (.38, .19, .59), (.92, .83, .97)], (.79, .74, .83), 90.2),
    '前抽屉试验': ([(.89, .75, .96), (.78, .56, .93), (.82, .71, .90), (.77, .65, .87), (.26, .13, .43), (.95, .87, .98)], (.78, .73, .82), 92.3),
    '轴移试验': ([(.59, .43, .74), (.66, .53, .77), (.52, .39, .65), (.21, .10, .37), (.62, .50, .73)], (.55, .49, .60), 82.9),
    '杠杆征试验': ([(.64, .48, .78), (.83, .72, .91), (.92, .82, .97), (.83, .63, .95)], (.82, .76, .87), 77.6),
}
SPEC = {
    '拉赫曼试验': ([(.97, .88, 1), (1, .94, 1), (.85, .62, .97), (.63, .35, .85), (.83, .63, .95), (1, .88, 1), (.72, .55, .86), (1, .88, 1)], (.91, .87, .94), 85.0),
    '前抽屉试验': ([(.95, .86, .99), (1, .94, 1), (.80, .56, .94), (.69, .41, .89), (.75, .53, .90), (1, .88, 1)], (.91, .86, .95), 84.0),
    '轴移试验': ([(.98, .91, 1), (.94, .70, 1), (.94, .70, 1), (.92, .73, .99), (.97, .83, 1)], (.96, .91, .98), 0.0),
    '杠杆征试验': ([(.90, .79, .96), (.80, .56, .94), (.94, .70, 1), (.89, .74, .97)], (.88, .82, .93), 0.0),
}
LRP = {
    '拉赫曼试验': ([(26.36, 6.73, 103.23), (102.13, 6.44, 1618.41), (5.92, 2.08, 16.85), (2.15, 1.13, 4.10), (2.21, .82, 5.93), (47.65, 3.02, 752.26), (1.35, .65, 2.82), (56.55, 3.61, 884.90)], (7.63, 2.52, 23.11), 85.1, '随机'),
    '前抽屉试验': ([(17.14, 5.66, 51.84), (87.87, 5.52, 1399.90), (4.08, 1.69, 9.88), (2.48, 1.18, 5.19), (1.05, .44, 2.52), (58.23, 3.72, 910.85)], (6.70, 1.96, 22.86), 85.0, '随机'),
    '轴移试验': ([(34.27, 4.83, 242.95), (10.51, 1.56, 70.65), (8.26, 1.22, 55.93), (2.53, .59, 10.91), (18.49, 2.67, 128.11)], (11.60, 5.31, 25.33), 29.8, '固定'),
    '杠杆征试验': ([(6.15, 2.79, 13.55), (4.15, 1.72, 10.05), (14.71, 2.20, 98.27), (7.50, 2.93, 19.22)], (6.49, 3.92, 10.73), 0.0, '固定'),
}
LRN = {
    '拉赫曼试验': ([(.09, .04, .24), (.11, .03, .34), (.13, .07, .26), (.31, .16, .58), (.76, .56, 1.02), (.21, .08, .53), (.87, .60, 1.25), (.09, .04, .19)], (.23, .10, .52), 93.5, '随机'),
    '前抽屉试验': ([(.12, .05, .27), (.23, .11, .48), (.23, .13, .39), (.33, .19, .58), (.98, .73, 1.32), (.06, .03, .15)], (.23, .09, .63), 94.4, '随机'),
    '轴移试验': ([(.42, .29, .59), (.37, .26, .52), (.52, .39, .69), (.86, .70, 1.06), (.40, .29, .53)], (.49, .33, .72), 88.5, '随机'),
    '杠杆征试验': ([(.41, .27, .61), (.21, .12, .37), (.09, .04, .20), (.19, .08, .46)], (.21, .11, .40), 75.7, '随机'),
}
AUC = {'拉赫曼试验': .9270, '前抽屉试验': .9193, '轴移试验': .8910, '杠杆征试验': .9038}
TESTS = list(ST)


def forest(ax, names, rows, pooled, i2, xlabel, log=False, model=None, fmt='{:.2f}'):
    n = len(names)
    for k, (v, lo, hi) in enumerate(rows):
        y = n - k
        ax.plot([lo, hi], [y, y], color='#5b7bd5', lw=1.4)
        ax.plot(v, y, 'o', color='#c62828', ms=7)
        ax.text(1.02, y, f'{fmt.format(v)}（{fmt.format(lo)}–{fmt.format(hi)}）', transform=ax.get_yaxis_transform(), va='center', fontsize=10)
    v, lo, hi = pooled
    ax.fill([lo, v, hi, v], [-.3, -.6, -.3, 0], color='#c62828')
    ax.axvline(v, color='#c62828', ls='--', lw=.8)
    if log:
        ax.set_xscale('log'); top = 100 if max(r[2] for r in rows) < 100 else 2000
        ax.set_xlim(.01, top)
        tk = [.01, .1, 1, 10, 100] + ([1000] if top > 100 else [])
        ax.set_xticks(tk); ax.set_xticklabels([f'{t:g}' for t in tk]); ax.minorticks_off()
        ax.axvline(1, color='k', lw=.8)
    else:
        ax.set_xlim(0, 1)
    ax.set_ylim(-1, n + .8)
    ax.set_yticks(range(n, 0, -1)); ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=11)
    t = f'合并 {fmt.format(v)}（{fmt.format(lo)}–{fmt.format(hi)}），I²={i2:.1f}%'
    if model:
        t = f'{model}效应模型：' + t
    ax.set_title(t, fontsize=10.5, loc='left')
    ax.grid(axis='x', ls=':', alpha=.5)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def forest_fig(A, B, la, lb, name, title, log=False):
    fig = plt.figure(figsize=(10.8, 17.5), dpi=100)
    gs = fig.add_gridspec(4, 2, hspace=.62, wspace=.95, left=.13, right=.86, top=.915, bottom=.04)
    for r, t in enumerate(TESTS):
        for c, (D, lab) in enumerate(((A, la), (B, lb))):
            ax = fig.add_subplot(gs[r, c])
            d = D[t]
            forest(ax, ST[t], d[0], d[1], d[2], lab, log=log, model=d[3] if log else None)
            if c == 0:
                ax.text(-.32, 1.32, t, transform=ax.transAxes, fontsize=15, fontweight='bold')
    fig.suptitle(title, fontsize=17, fontweight='bold', y=.99)
    fig.savefig(f'{OUT}/{name}', dpi=100); plt.close(fig)


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 22))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

# 图 1：照片
p = Image.open(f'{SRC}/x01.png').convert('RGB')
p = p.resize((1080, round(p.height * 1080 / p.width)), Image.LANCZOS)
d = ImageDraw.Draw(p)
for (x, y), t in zip([(287, 327), (821, 327), (287, 660), (821, 660)], ['a 拉赫曼试验', 'b 前抽屉试验', 'c 轴移试验', 'd 杠杆征试验']):
    d.rectangle([x - 150, y - 26, x + 150, y + 22], fill='white')
    f = font(28); w = d.textlength(t, font=f); d.text((x - w / 2, y - 18), t, font=f, fill=INK)
badge(p, '图1').save(f'{OUT}/img02.jpg', quality=88)

# 图 2：文献筛选流程
W = 1080; im = Image.new('RGB', (W, 1180), 'white'); d = ImageDraw.Draw(im)


def box(x0, y0, x1, y1, lines, fill='white', fs=28):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=(90, 90, 90), width=3)
    f = font(fs); lh = fs + 10; y = (y0 + y1) / 2 - lh * len(lines) / 2 + 2
    for i, t in enumerate(lines):
        w = d.textlength(t, font=f)
        d.text(((x0 + x1) / 2 - w / 2, y + i * lh), t, font=f, fill=INK, **({'stroke_width': 1, 'stroke_fill': INK} if i == 0 else {}))


def arr(x, y0, y1):
    d.line([x, y0, x, y1 - 16], fill=(90, 90, 90), width=4)
    d.polygon([(x - 12, y1 - 18), (x + 12, y1 - 18), (x, y1)], fill=(90, 90, 90))


def harr(x0, x1, y):
    d.line([x0, y, x1 - 16, y], fill=(90, 90, 90), width=4)
    d.polygon([(x1 - 18, y - 12), (x1 - 18, y + 12), (x1, y)], fill=(90, 90, 90))


f = font(36); t = '图2　文献筛选流程'; d.text((W / 2 - d.textlength(t, font=f) / 2, 18), t, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
for k, (n, c) in enumerate([('PubMed', '1,002'), ('MEDLINE', '980'), ('CINAHL', '485'), ('Web of Science', '952'), ('医中志 Ichushi', '417')]):
    x0 = 20 + k * 210; box(x0, 90, x0 + 195, 210, [n, f'{c} 篇'], fill=(214, 228, 243), fs=24)
d.text((20, 222), '检索', font=font(26), fill=(120, 120, 120))
d.line([117, 210, 117, 240], fill=(90, 90, 90), width=3); d.line([117, 240, 957, 240], fill=(90, 90, 90), width=3)
for k in range(5):
    d.line([117 + k * 210, 210, 117 + k * 210, 240], fill=(90, 90, 90), width=3)
arr(400, 240, 290)
box(150, 290, 650, 390, ['检索到的记录总数', '3,836 篇'])
arr(400, 390, 450); d.text((20, 470), '筛选', font=font(26), fill=(120, 120, 120))
box(150, 450, 650, 550, ['去重后记录', '1,536 篇'])
harr(650, 720, 500); box(720, 450, 1060, 550, ['按题目和摘要排除', '1,450 篇'], fill=(235, 235, 235), fs=26)
arr(400, 550, 610); d.text((20, 630), '合格性', font=font(26), fill=(120, 120, 120))
box(150, 610, 650, 710, ['全文评估合格性', '86 篇'])
harr(650, 720, 660); box(720, 600, 1060, 960, ['阅读全文后排除 78 篇', '研究设计不符 40', '未报告检验准确性 14', '综述 10', '未用体格检查 8', '不含急性期 6'], fill=(235, 235, 235), fs=26)
arr(400, 710, 770); d.text((20, 790), '纳入', font=font(26), fill=(120, 120, 120))
box(150, 770, 650, 870, ['纳入定量合成（荟萃分析）', '8 篇'], fill=(190, 235, 180))
im.crop((0, 0, W, 980)).save(f'{OUT}/img03.jpg', quality=92)

# 图 3：偏倚风险
studies = ['Gürpınar 2019', 'Jarbo 2017', 'Kıyak 2018', 'Kostov 2014', 'Lee 1988', 'Massey 2017', 'Mulligan 2015', 'Mulligan 2017']
R = ['L?? ?', 'LLL H', 'L?? ?', '?H? L', 'LLL ?', 'LLL L', 'LLL H', 'LLL H']
cols = ['病例选择', '待评价试验', '参考标准', '流程与时间', '病例选择', '待评价试验', '参考标准']
W, H = 1080, 1060; im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
f = font(36); t = '图3　纳入研究的偏倚风险（QUADAS-2）'; d.text((W / 2 - d.textlength(t, font=f) / 2, 18), t, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
x0, y0, cw, rh = 300, 270, 100, 82
for g, (a, b, t) in enumerate([(0, 4, '偏倚风险'), (4, 7, '适用性')]):
    xa = x0 + a * cw + g * 30; xb = x0 + b * cw + g * 30
    f = font(30); w = d.textlength(t, font=f); d.text(((xa + xb) / 2 - w / 2, 80), t, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
    d.line([xa + 8, 122, xb - 8, 122], fill=INK, width=3)
for j, c in enumerate(cols):
    x = x0 + j * cw + (30 if j >= 4 else 0) + cw / 2
    for i, ch in enumerate(c):
        d.text((x - 12, 135 + i * 26), ch, font=font(24), fill=INK)
COL = {'L': ((46, 160, 67), '＋'), 'H': ((200, 40, 40), '－'), '?': ((235, 200, 40), '？')}
for i, s in enumerate(studies):
    y = y0 + i * rh
    f = font(28); w = d.textlength(s, font=f); d.text((x0 - 20 - w, y + rh / 2 - 16), s, font=f, fill=INK)
    codes = R[i].replace(' ', '') + 'LLL'
    for j, cd in enumerate(codes):
        x = x0 + j * cw + (30 if j >= 4 else 0)
        d.rectangle([x, y, x + cw, y + rh], outline=INK, width=2)
        colr, sym = COL[cd]; cx, cy = x + cw / 2, y + rh / 2
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=colr)
        f2 = font(30); w = d.textlength(sym, font=f2); d.text((cx - w / 2, cy - 18), sym, font=f2, fill=INK)
y = y0 + 8 * rh + 40
for k, cd in enumerate('HL?'.replace('L?', '?L')):
    colr, sym = COL[cd]; x = 260 + k * 230
    d.ellipse([x, y, x + 44, y + 44], fill=colr)
    d.text((x + 56, y + 6), {'H': '高', '?': '不清楚', 'L': '低'}[cd], font=font(30), fill=INK)
im.crop((0, 0, W, y + 70)).save(f'{OUT}/img04.jpg', quality=92)

# 图 4、5：森林图
forest_fig(SENS, SPEC, '敏感度', '特异度', 'img05.png', '图4　敏感度和特异度森林图')
forest_fig(LRP, LRN, '阳性似然比（对数刻度）', '阴性似然比（对数刻度）', 'img06.png', '图5　阳性/阴性似然比森林图', log=True)
for n in ('img05', 'img06'):
    Image.open(f'{OUT}/{n}.png').convert('RGB').save(f'{OUT}/{n}.jpg', quality=90)
    import os; os.remove(f'{OUT}/{n}.png')

# 图 6：SROC（对称 SROC：logit(TPR) = D + logit(FPR)，D 由原文 AUC 反推）
from scipy.optimize import brentq
lg = lambda p: np.log(p / (1 - p)); il = lambda x: 1 / (1 + np.exp(-x))
fpr = np.linspace(1e-4, 1 - 1e-4, 2000)
fig, axs = plt.subplots(2, 2, figsize=(10.8, 10.8), dpi=100)
for ax, t in zip(axs.flat, TESTS):
    Dv = brentq(lambda D: np.trapezoid(il(D + lg(fpr)), fpr) - AUC[t], 0.1, 15)
    ax.plot(fpr, il(Dv + lg(fpr)), color='#3b5bdb', lw=2)
    se = [r[0] for r in SENS[t][0]]; sp = [r[0] for r in SPEC[t][0]]
    ax.scatter([1 - s for s in sp], se, color='#c62828', s=60, zorder=3)
    ax.plot([0, 1], [0, 1], ls=':', color='gray', lw=.8)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.02); ax.grid(ls=':', alpha=.5)
    ax.set_xlabel('1－特异度'); ax.set_ylabel('敏感度')
    ax.set_title(t, fontsize=15, fontweight='bold', loc='left')
    ax.text(.45, .25, f'对称 SROC\nAUC = {AUC[t]:.4f}', fontsize=13)
fig.suptitle('图6　汇总受试者工作特征（SROC）曲线', fontsize=17, fontweight='bold')
fig.tight_layout(rect=(0, 0, 1, .96)); fig.savefig(f'{OUT}/img07.png', dpi=100); plt.close(fig)
Image.open(f'{OUT}/img07.png').convert('RGB').save(f'{OUT}/img07.jpg', quality=90); import os; os.remove(f'{OUT}/img07.png')

# 封面：图 1 上排
c = Image.open(f'{SRC}/x01.png').convert('RGB'); w, h = c.size; ch = round(w * 383 / 900)
c.crop((0, 40, w, 40 + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
