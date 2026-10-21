#!/usr/bin/env python3
"""Maciejasz 等 2014 上肢康复机器人综述：首图中文标题卡；原文图 1 照片直接使用并加中文图注，图 2 加中文图例，
图 3 按原图柱高重绘为中文；分类总览卡为编者根据原文表 2～6 整理。
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

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '综述 · 《神经工程与康复杂志》2014', font=font(32), fill=TEAL)
dr.text((70, 140), '上肢康复机器人设备综述', font=font(64), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 335), 'Maciejasz P, Eschweiler J, Gerlach-Hahn K, Jansen-Troy A, Leonhardt S.', font=font(28), fill=GREY)
dr.text((70, 380), 'J Neuroeng Rehabil 2014;11:3', font=font(28), fill=GREY)
dr.text((70, 445), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1
f1 = raw(243)
save(capbox(f1, '原文图 1：上肢康复机器人的机械结构举例。A ARM Guide：用直线导轨调整方向的简单系统；B InMotion ARM：末端执行器式商用系统；'
                'C NeReBot：绳驱机器人；D ArmeoPower：外骨骼式商用系统'), 2)

# 原文图 2 + 图例
f2 = up(raw(293), 640); leg = Image.new('RGB', (560, f2.height), 'white'); dr = ImageDraw.Draw(leg)
items = [('1', '上臂（肩）屈伸', (20, 30, 130)), ('2', '上臂（肩）内收 / 外展', (40, 140, 40)), ('3', '上臂（肩）内旋 / 外旋', (140, 20, 20)),
         ('4', '肘屈伸', (20, 30, 130)), ('5', '前臂旋前 / 旋后', (140, 20, 20)), ('6', '腕屈伸', (40, 140, 40)),
         ('7', '腕内收（尺偏）/ 外展（桡偏）', (20, 30, 130)), ('8', '手抓握 / 松开', (20, 20, 20))]
y0 = (f2.height - 8 * 92) // 2
for i, (n, t, c) in enumerate(items):
    y = y0 + i * 92; dr.ellipse([20, y, 76, y + 56], fill=c); ctext(dr, 48, y + 8, n, font(36), 'white')
    para(dr, 96, y + 10, t, 32, 450)
row = Image.new('RGB', (1200, f2.height), 'white'); row.paste(f2, (0, 0)); row.paste(leg, (640, 0))
save(capbox(row, '原文图 2：上肢的主要运动（自由度），编号对应原图'), 3)

# 原文图 3：按原图柱高重绘
yrs = ['2005 年前', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2012 年后']
dev = [92, 250, 106, 134, 173, 95, 265, 300, 180, 81]; tot = [365, 351, 131, 173, 275, 169, 340, 869, 411, 679]
nd = [2, 4, 3, 1, 4, 2, 5, 2, 4, 4]; nt = [3, 2, 1, 1, 2, 1, 2, 7, 3, 5]
th = [t - d for t, d in zip(tot, dev)]
fig, ax = plt.subplots(figsize=(12, 7.2), dpi=100)
x = np.arange(10)
ax.bar(x, dev, 0.62, color='#1f4e8c', label='验证设备安全性 / 有效性')
ax.bar(x, th, 0.62, bottom=dev, color='#f05a28', label='改进治疗方法')
for i in range(10):
    ax.text(i, dev[i] / 2, str(nd[i]), ha='center', va='center', color='white', fontsize=17)
    if th[i] > 60: ax.text(i, dev[i] + th[i] / 2, str(nt[i]), ha='center', va='center', color='white', fontsize=17)
    else: ax.text(i, tot[i] + 12, str(nt[i]), ha='center', va='bottom', color='black', fontsize=17)
ax.set_xticks(x); ax.set_xticklabels(yrs, fontsize=15); ax.set_ylim(0, 1000); ax.tick_params(axis='y', labelsize=14)
ax.set_xlabel('研究开始年份', fontsize=17); ax.set_ylabel('入组受试者总数', fontsize=17)
ax.grid(axis='y', color='#ccc'); ax.set_axisbelow(True)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(title='研究目的', fontsize=15, title_fontsize=15, loc='upper left', frameon=False)
fig.tight_layout(); fig.savefig(f'{OUT}/_f3.png'); plt.close(fig)
f3 = Image.open(f'{OUT}/_f3.png').convert('RGB'); os.remove(f'{OUT}/_f3.png')
save(capbox(f3, '原文图 3：按研究目的和开始年份统计的临床研究数和入组人数（检索 clinicaltrials.gov，2013 年 10 月）。柱上数字为当年开始的研究数（编者按原图重绘）'), 4)

# 编者卡：分类总览
blocks = [('辅助类型', '主动：有驱动器，能带动肢体，适合完全不能动的人。被动：只有制动器，只能提供阻力，适合能自己动的人，更轻更便宜。'
           '触觉：通过触觉交互，多配虚拟现实。指导：不施力，只记录动作并反馈。', LT, TEAL),
          ('机械结构', '末端执行器式：只在手或前臂远端接触，结构和控制简单，但难以单独控制某个关节。'
           '外骨骼式：结构贴合上肢骨骼，能独立控制多个关节，但每个人都要调节杆长，上机耗时。还有平面机器人、绳驱、双机器人组合等。', OR, (200, 110, 30)),
          ('驱动方式', '电机最常用；气动轻、阻抗低但要气源，气动人工肌肉响应慢；液压很少用；'
           '串联弹性驱动器让力控更稳更安全；磁流变 / 电流变液制动器用于可调阻力；功能性电刺激直接让肌肉收缩。', GR, (40, 130, 60)),
          ('控制信号与策略', '输入：运动学信号（位置、角度）、动力学信号（力、力矩）、表面肌电、开关触发。'
           '高层策略：辅助型、挑战型（阻抗、放大误差、约束诱导）、触觉刺激、指导。底层：阻抗控制、导纳控制。', PK, RED)]
save(card(1200, '上肢康复机器人怎么分类（编者根据原文整理）', blocks), 5)

c = raw(243).crop((540, 0, 1181, 480)); c = up(c, 900); y0 = (c.height - 383) // 2
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
