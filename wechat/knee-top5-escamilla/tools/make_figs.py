#!/usr/bin/env python3
"""Escamilla 2023 交叉韧带与髌股关节康复选动作的五个概念：首图中文标题卡；图 1、图 8 弓步照片去英文表头和字母后
重排成中文 2×2 图；正文峰值负荷数据做成范围条形图；图 2～7、9、10 曲线按读图近似值中文重绘（两两合并）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import numpy as np
import cv2
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


def inpaint(im, boxes):
    a = np.array(im); m = np.zeros(a.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes: m[y0:y1, x0:x1] = 255
    return Image.fromarray(cv2.inpaint(a, m, 5, cv2.INPAINT_TELEA))


def grid(title, cells, cols, rows, ch=480):
    cells = [c.resize((round(c.width * ch / c.height), ch), Image.LANCZOS) for c in cells]
    cw = max(c.width for c in cells); lw = 150; gap = 12
    W = lw + 2 * cw + 3 * gap; H = 90 + 60 + 2 * ch + 3 * gap
    out = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(out)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(40), fill='white')
    f = font(34)
    for j, t in enumerate(cols):
        cx = lw + gap + j * (cw + gap) + cw / 2; dr.text((cx - dr.textlength(t, font=f) / 2, 96), t, font=f, fill=INK)
    for i, t in enumerate(rows):
        y = 150 + gap + i * (ch + gap)
        for k, line in enumerate(t.split('\n')):
            dr.text((lw / 2 - dr.textlength(line, font=f) / 2, y + ch / 2 - 40 + k * 44), line, font=f, fill=INK)
        for j in range(2):
            c = cells[i * 2 + j]; out.paste(c, (int(lw + gap + j * (cw + gap) + (cw - c.width) / 2), y))
    return out


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床观点 · 《国际运动物理治疗杂志》（IJSPT）2023', font=font(32), fill=TEAL)
for i, t in enumerate(['交叉韧带、髌股关节康复', '怎么选下肢动作？五个概念']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '负重 vs 非负重 · 技术细节 · 动作之间 · 膝角度 · 膝过脚尖', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Escamilla RF. IJSPT 2023;18(1):14-25', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，原文以 CC BY-NC 4.0 开放获取', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1：前弓步步长 × 台阶 ----------
p = raw(71)
p = inpaint(p, [(30, 350, 62, 380), (262, 350, 294, 380), (30, 725, 66, 780), (262, 725, 298, 780)])
cells = [p.crop(b) for b in [(32, 24, 246, 374), (266, 24, 598, 374), (32, 392, 246, 776), (266, 392, 598, 776)]]
save(grid('原文图 1　前弓步：步长与台阶的四种组合', cells, ['短步（膝过脚尖）', '长步（膝在踝上方）'], ['地面', '上 10 cm\n台阶']), 2)

# ---------- 图 8：前弓步 vs 侧弓步 ----------
p = raw(108)
p = inpaint(p, [(64, 44, 96, 74), (406, 44, 438, 74), (64, 420, 96, 450), (406, 420, 438, 450)])
cells = [p.crop(b) for b in [(50, 37, 396, 372), (404, 37, 727, 372), (50, 412, 396, 750), (404, 412, 727, 750)]]
save(grid('原文图 8　前弓步与侧弓步：地面 vs 10 cm 台阶', cells, ['前弓步', '侧弓步'], ['地面', '上 10 cm\n台阶']), 3)

# ---------- 概念 1：峰值交叉韧带负荷（正文数据） ----------
ACL = [('坐姿伸膝（12RM 等张，15°）', 158, 158), ('坐姿伸膝（等长/等速，35～40°）', 254, 396), ('自重深蹲 / 12RM 杠铃深蹲（25°）', 0, 28),
       ('12RM 腿举', 0, 0), ('自重 / 12RM 哑铃单腿蹲（30°）', 59, 142), ('60 cm 双脚落地（33～48°）', 253, 253), ('平地走路（参照，15～20°）', 303, 303)]
PCL = [('坐姿屈膝（等长/等速，90°）', 2701, 3330), ('坐姿伸膝（12RM，79°）', 959, 959), ('12RM 杠铃深蹲（63～77°）', 1868, 2212),
       ('12RM 腿举（88～95°）', 1726, 1866), ('12RM 靠墙蹲（80～90°）', 757, 786), ('12RM 前/侧弓步（60～90°）', 612, 765),
       ('12RM 哑铃单腿蹲（90°）', 414, 414), ('自重前/侧弓步（60～80°）', 317, 334), ('平地走路（参照，15～20°）', 160, 160)]
fig, axs = plt.subplots(2, 1, figsize=(10, 10), dpi=150, gridspec_kw={'height_ratios': [7, 9]})
for ax, data, ttl, col in [(axs[0], ACL, '前交叉韧带（ACL）峰值负荷（N）', '#b5532c'), (axs[1], PCL, '后交叉韧带（PCL）峰值负荷（N）', '#1f5f8b')]:
    for i, (lab, lo, hi) in enumerate(data[::-1]):
        c = '#999' if '参照' in lab else ('#d98c6a' if '坐姿' in lab and col == '#b5532c' else col)
        ax.barh(i, max(hi - lo, (hi or 1) * 0.02 + 8), left=lo, color=c, height=0.55)
        ax.text(hi + (8 if col == '#b5532c' else 60), i, f'{lo}' if lo == hi else f'{lo}～{hi}', va='center', fontsize=11)
    ax.set_yticks(range(len(data))); ax.set_yticklabels([x[0] for x in data[::-1]], fontsize=12)
    ax.set_title(ttl, fontsize=14)
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
axs[0].set_xlim(0, 460); axs[1].set_xlim(0, 3800)
fig.text(.5, .005, '数据来自原文概念 1 正文；括号内为出现峰值的膝屈曲角度', ha='center', fontsize=10, color='#666')
fig.tight_layout(rect=(0, .02, 1, 1)); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 4)

# ---------- 曲线（读图近似值） ----------
D9 = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90]; D10 = D9 + [100]


def X(desc, asc):
    return [a for a in desc] + [210 - a for a in asc]


def panel(ax, desc, asc, series, ylab, ttl, top=None):
    for lab, v, sty in series:
        n = len(desc); mfc = 'white' if '--' in sty else '#222'
        ax.plot(desc, v[:n], sty, lw=2, ms=6, label=lab, color='#222', mfc=mfc)
        ax.plot([210 - a for a in asc], v[n:], sty, lw=2, ms=6, color='#222', mfc=mfc)
    ax.axvline(105, color='#ccc', lw=1)
    ticks = [0, 20, 40, 60, 80, 100]; ax.set_xticks(ticks + [210 - t for t in ticks[::-1]])
    ax.set_xticklabels([str(t) for t in ticks] + [str(t) for t in ticks[::-1]], fontsize=10)
    ax.set_xlim(-2, 212); ax.set_ylabel(ylab); ax.set_title(ttl, fontsize=13)
    if top: ax.set_ylim(top[0], top[1])
    ax.text(.24, -.13, '下蹲（屈膝）', ha='center', fontsize=12, transform=ax.transAxes)
    ax.text(.76, -.13, '起身（伸膝）', ha='center', fontsize=12, transform=ax.transAxes)
    ax.legend(frameon=False, fontsize=10, loc='upper left')
    for s in ['top', 'right']: ax.spines[s].set_visible(False)


L_long = [265, 310, 330, 350, 375, 445, 485, 510, 535, 540, 620, 715, 780, 785, 755, 705, 685, 530, 390, 380]
L_short = [-45, -10, 65, 105, 140, 185, 255, 335, 425, 515, 595, 615, 585, 555, 540, 415, 350, 300, 235, 170]
SIDE_P = [160, 225, 290, 315, 310, 245, 320, 355, 435, 480, 540, 545, 595, 655, 645, 570, 505, 385, 310, 330]
A9 = D9[::-1]; A10 = D10[::-1]
fig, axs = plt.subplots(2, 1, figsize=(10, 10), dpi=150)
panel(axs[0], D9, A9, [('长步前弓步', L_long, 'o-'), ('短步前弓步', L_short, 'o--')], '负值＝ACL、正值＝PCL（N）', '原文图 2　12RM 前弓步：长步 vs 短步的交叉韧带负荷', (-200, 1000))
axs[0].axhline(0, color='#888', lw=.8)
panel(axs[1], D9, A9, [('前弓步', L_long, 'o-'), ('侧弓步', SIDE_P, 'o--')], 'PCL 张力（N）', '原文图 7　12RM 前弓步 vs 侧弓步的 PCL 负荷', (0, 1000))
fig.text(.5, .005, '曲线为读图近似值（原文未给数值表）；横轴为膝屈曲角度（°）', ha='center', fontsize=10, color='#666')
fig.tight_layout(rect=(0, .02, 1, 1), h_pad=3); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 5)

BW_long = [25, 70, 115, 150, 170, 205, 300, 395, 525, 620, 615, 760, 760, 765, 625, 495, 370, 280, 205, 110, 70, 25]
BW_short = [25, 45, 80, 110, 140, 265, 470, 660, 775, 825, 840, 1090, 1300, 1280, 1070, 825, 435, 180, 110, 85, 45, 25]
RM_long = [100, 220, 310, 450, 780, 1230, 1620, 1980, 2130, 2140, 2190, 2150, 2100, 1790, 1380, 930, 620, 420, 250, 120]
RM_short = [80, 200, 290, 420, 600, 1000, 1620, 2250, 2750, 3000, 2850, 2700, 2330, 1880, 1410, 900, 580, 370, 200, 90]
fig, axs = plt.subplots(2, 1, figsize=(10, 10), dpi=150)
panel(axs[0], D10, A10, [('长步', BW_long, 'o-'), ('短步', BW_short, 'o--')], '髌股关节压力（N）', '原文图 3　自重前弓步：长步 vs 短步', (0, 2000))
panel(axs[1], D9, A9, [('长步', RM_long, 'o-'), ('短步', RM_short, 'o--')], '髌股关节压力（N）', '原文图 4　12RM 前弓步：长步 vs 短步', (0, 4000))
fig.text(.5, .005, '曲线为读图近似值（原文未给数值表）；横轴为膝屈曲角度（°）', ha='center', fontsize=10, color='#666')
fig.tight_layout(rect=(0, .02, 1, 1), h_pad=3); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 6)

GR = [25, 55, 100, 125, 165, 270, 420, 580, 720, 795, 815, 925, 1025, 1050, 930, 765, 490, 265, 155, 95, 55, 25]
PF10 = [25, 50, 100, 130, 140, 190, 340, 470, 560, 635, 645, 950, 1045, 985, 750, 530, 300, 190, 160, 105, 50, 25]
WS = [80, 230, 300, 460, 760, 1230, 1640, 1980, 2130, 2140, 2190, 2150, 2110, 1790, 1380, 940, 630, 420, 250, 100]
WOS = [80, 110, 150, 270, 520, 920, 1430, 1980, 2200, 2230, 2190, 2060, 1810, 1370, 990, 640, 390, 220, 120, 70]
fig, axs = plt.subplots(2, 1, figsize=(10, 10), dpi=150)
panel(axs[0], D10, A10, [('地面', GR, 'o-'), ('上 10 cm 台阶', PF10, 'o--')], '髌股关节压力（N）', '原文图 5　自重前弓步：地面 vs 10 cm 台阶', (0, 2000))
panel(axs[1], D9, A9, [('迈步（向前迈出再推回）', WS, 'o-'), ('原地（双脚不动上下蹲）', WOS, 'o--')], '髌股关节压力（N）', '原文图 6　前弓步：迈步 vs 原地', (0, 4000))
fig.text(.5, .005, '曲线为读图近似值（原文未给数值表）；横轴为膝屈曲角度（°）', ha='center', fontsize=10, color='#666')
fig.tight_layout(rect=(0, .02, 1, 1), h_pad=3); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 7)

SIDE_BW = [25, 40, 105, 160, 255, 375, 580, 730, 960, 1055, 975, 1045, 1220, 1305, 1205, 880, 575, 230, 125, 95, 30, 15]
SIDE_RM = [80, 220, 300, 470, 700, 1080, 1750, 2150, 2580, 2710, 2460, 2150, 1650, 1300, 1020, 710, 500, 310, 200, 80]
fig, axs = plt.subplots(2, 1, figsize=(10, 10), dpi=150)
panel(axs[0], D10, A10, [('前弓步', BW_long, 'o-'), ('侧弓步', SIDE_BW, 'o--')], '髌股关节压力（N）', '原文图 9　自重：前弓步 vs 侧弓步', (0, 2000))
panel(axs[1], D9, A9, [('前弓步', WS, 'o-'), ('侧弓步', SIDE_RM, 'o--')], '髌股关节压力（N）', '原文图 10　12RM：前弓步 vs 侧弓步', (0, 4000))
fig.text(.5, .005, '曲线为读图近似值（原文未给数值表）；横轴为膝屈曲角度（°）', ha='center', fontsize=10, color='#666')
fig.tight_layout(rect=(0, .02, 1, 1), h_pad=3); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 8)
import os; os.remove(f'{OUT}/_p.png')

# ---------- 封面 900×383 ----------
c = raw(108).crop((404, 37, 727, 372)); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = int(c.height * 0.25); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
