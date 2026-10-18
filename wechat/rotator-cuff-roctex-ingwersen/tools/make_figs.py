#!/usr/bin/env python3
"""Ingwersen 2017 RoCTEx（肩袖肌腱病 渐进大负荷 vs 传统小负荷）：首图中文标题卡；图 1 流程中文重绘；
附录 A/B 六个动作照片加中文标题与负荷说明；两组负荷进阶示意图；图 2 按原图读取的近似值中文重绘。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
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
plt.rcParams['font.size'] = 12
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); RED = (190, 40, 50); TEAL = (0, 110, 130); NAVY = (40, 70, 120)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def raw(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


# ---------- 首图：中文标题卡 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '原创研究 · 随机对照试验（RoCTEx 试验）', font=font(32), fill=TEAL)
for i, t in enumerate(['肩袖肌腱病：3 个月渐进大负荷训练', 'vs 传统小负荷训练']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '丹麦 3 家中心 · 100 例 · 12 周 · 主要结局为 DASH 评分', font=font(32), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Ingwersen KG 等，《骨科运动医学杂志》（OJSM）2017 年第 5 卷第 8 期', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，原文版权归作者与期刊', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1 流程 ----------
W, H = 1400, 1180; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def bx(x0, y0, x1, y1, lines, fill, fs=26, col=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 10, fill=fill)
    yy = (y0 + y1 - len(lines) * (fs + 10)) / 2 + 3
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs), col); yy += fs + 10


def ar(x, a, b, c=(120, 170, 200)):
    dr.line([x, a, x, b], fill=c, width=6); dr.polygon([(x, b + 6), (x - 13, b - 12), (x + 13, b - 12)], fill=c)


for y0, y1, t in [(20, 330, '入组'), (350, 560, '分配'), (580, 700, '随访'), (720, 1160, '分析')]:
    dr.rounded_rectangle([20, y0, 130, y1], 10, fill=(230, 236, 242)); ctext(dr, 75, (y0 + y1) / 2 - 16, t, font(30), NAVY)
bx(480, 30, 1020, 130, ['评估是否符合纳入标准（150 例）', '医院转诊 103 例 · 外部招募 47 例'], (225, 232, 245))
ar(750, 130, 160)
bx(1060, 50, 1380, 130, ['排除 50 例', '（不符合纳入标准）'], (245, 230, 230), 24)
bx(480, 165, 1020, 225, ['随机分组 100 例'], (200, 230, 210), 30)
bx(480, 240, 1020, 320, ['中心 1：68 例 · 中心 2：19 例', '中心 3：13 例'], (240, 244, 240), 24)
ar(470, 320, 360); ar(1030, 320, 360)
L, R = (160, 760), (790, 1390)
for (x0, x1), rows in [(L, [['渐进大负荷组（PHLE）49 例', '接受干预 48 例；未接受 1 例', '（放弃参加训练）'],
                             ['失访 4 例（无法联系）'],
                             ['意向性分析：49 例（排除 0 例）', '实际观察分析：44 例（排除 5 例）', '符合方案分析：28 例（排除 21 例）']]),
                       (R, [['传统小负荷组（LLE）51 例', '接受干预 50 例；未接受 1 例', '（合并其他损伤）'],
                            ['失访 1 例（无法联系）'],
                            ['意向性分析：51 例（排除 0 例）', '实际观察分析：49 例（排除 2 例）', '符合方案分析：31 例（排除 20 例）']])]:
    bx(x0, 370, x1, 550, rows[0], (250, 238, 210), 26)
    ar((x0 + x1) // 2, 550, 600)
    bx(x0, 605, x1, 690, rows[1], (240, 240, 240), 26)
    ar((x0 + x1) // 2, 690, 740)
    bx(x0, 745, x1, 960, rows[2], (225, 232, 245), 26)
ctext(dr, 775, 1000, '注：失访者按"基线值结转"补全，意向性分析人群共 100 例；', font(24), GREY)
ctext(dr, 775, 1040, '符合方案 = 至少到治疗师处随访 4/6 次且居家完成 > 80% 训练。', font(24), GREY)
save(im, 2)

# ---------- 六个动作 ----------
EX = [
    (37, '动作 1  挺胸收肩胛（姿势训练）', '两组相同：保持 5 次深呼吸（约 15 秒）× 3 次，间歇 30 秒', None),
    (46, '动作 2  靠墙水平内收牵伸（后关节囊）', '两组相同：保持约 15 秒 × 3 次，间歇 30 秒', None),
    (44, '动作 3  肩胛面哑铃上举（约 45°）', '★ PHLE：15RM→6RM，4 组，上下各 3～4 秒；LLE：20～25 次 × 3 组', RED),
    (40, '动作 4  侧卧哑铃外旋', '★ PHLE：15RM→6RM，4 组，上下各 3～4 秒；LLE：20～25 次 × 3 组', RED),
    (49, '动作 5  仰卧哑铃前伸（推肩胛）', '两组相同：20 次 × 3 组，上下各约 2 秒；下排为肩胛局部特写', None),
    (52, '动作 6  弹力带直臂后拉', '两组相同：20 次 × 3 组，上下各约 2 秒，靠握点远近调阻力', None),
]
for k, (x, name, rx, col) in enumerate(EX):
    ph = raw(x); w = 1200; ph = ph.resize((w, round(ph.height * w / ph.width)), Image.LANCZOS)
    im = Image.new('RGB', (w + 80, ph.height + 210), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, w + 80, 80], fill=TEAL if col is None else (170, 50, 55))
    dr.text((40, 18), name, font=font(40), fill='white')
    im.paste(ph, (40, 100))
    y = 100 + ph.height
    for t, cx in [('起始', 40 + w * 0.12), ('结束', 40 + w * 0.88)]:
        ctext(dr, cx, y + 12, t, font(28), GREY)
    ctext(dr, (w + 80) / 2, y + 60, rx, font(30), INK if col is None else RED)
    save(im, 3 + k)

# ---------- 负荷进阶示意 ----------
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=150)
wk = list(range(1, 13)); ph = [15, 12, 12, 10, 10, 8, 8, 8, 6, 6, 6, 6]
ax.step(wk, ph, where='mid', color='#b03038', lw=3, label='渐进大负荷组 PHLE（每组 RM 次数，4 组）')
ax.fill_between(wk, 20, 25, step='mid', color='#3a7fa0', alpha=.25)
ax.step(wk, [22.5] * 12, where='mid', color='#3a7fa0', lw=3, label='传统小负荷组 LLE（20～25 次，3 组）')
for a, b_, t in [(1, 15, '15RM'), (2.5, 12, '12RM'), (4.5, 10, '10RM'), (7, 8, '8RM'), (10.5, 6, '6RM')]:
    ax.text(a, b_ + .6, t, ha='center', color='#b03038', fontsize=12)
for v in [1, 2, 3, 4, 6, 9]: ax.axvline(v, color='#ccc', lw=1, ls=':', zorder=0)
ax.text(5.6, 2.4, '虚线 = 有治疗师监督的那一周（第 1、2、3、4、6、9 周）', fontsize=11, color='#666', ha='center')
ax.set_xticks(wk); ax.set_xlabel('周'); ax.set_ylabel('每组重复次数（负荷越大次数越少）')
ax.set_ylim(0, 28); ax.set_xlim(.5, 12.5); ax.legend(loc='upper right', fontsize=11, frameon=False)
ax.set_title('只有动作 3、4（肩袖）的负荷不同：两组 12 周进阶对比', fontsize=14)
for s in ['top', 'right']: ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(f'{OUT}/_p.png'); plt.close(fig)
save(Image.open(f'{OUT}/_p.png'), 9)

# ---------- 图 2（近似值） ----------
fig, axs = plt.subplots(1, 2, figsize=(11, 5), dpi=150, gridspec_kw={'width_ratios': [1, 1.6]})
ax = axs[0]
ax.bar([0, 1], [20.6, 19.1], yerr=[2.3, 2.3], color=['#222', 'white'], edgecolor='#222', capsize=5, width=.6)
ax.set_xticks([0, 1]); ax.set_xticklabels(['渐进大负荷\nPHLE', '传统小负荷\nLLE']); ax.set_ylim(0, 30)
ax.set_title('主要目的：两组总体比较', fontsize=13); ax.set_ylabel('12 周时校正后 DASH 评分（越低越好）')
ax = axs[1]; x = [0, 1, 2.6, 3.6]
ax.bar(x, [14.4, 21.3, 19.1, 13.5], yerr=[3.3, 3.3, 3.3, 3.3], color=['#222', 'white', '#222', 'white'], edgecolor='#222', capsize=5, width=.8)
ax.set_xticks([.5, 3.1]); ax.set_xticklabels(['同时打了激素（CS+）', '没打激素（CS-）']); ax.set_ylim(0, 30)
ax.set_title('次要目的：按是否合并激素注射分层', fontsize=13)
ax.bar([0], [0], color='#222', label='PHLE'); ax.bar([0], [0], color='white', edgecolor='#222', label='LLE')
ax.legend(frameon=False, loc='upper right')
for a in axs:
    for s in ['top', 'right']: a.spines[s].set_visible(False)
fig.text(.5, .01, '柱高 = 均值 ± 标准误（读图近似值，非原文数值表）', ha='center', fontsize=10, color='#666')
fig.tight_layout(rect=(0, .04, 1, 1)); fig.savefig(f'{OUT}/_p.png'); plt.close(fig)
save(Image.open(f'{OUT}/_p.png'), 10)

# ---------- 封面 900×383 ----------
c = raw(44); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = (c.height - 383) // 2; c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
import os; os.remove(f'{OUT}/_p.png')
