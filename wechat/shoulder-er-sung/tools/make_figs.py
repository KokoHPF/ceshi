#!/usr/bin/env python3
"""Sung 2023 不同体位与外展角度下肩外旋训练的肌电（Healthcare）：首图中文标题卡；图 1 线稿抹去英文换中文；
图 2 六种测试姿势照片加中文名；图 3 热身照片模糊海报与品牌字样；图 4 流程、图 5/6 折线（读图近似值）、
肌电比值柱图（按表 3）、选择建议卡为编者中文重绘。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 14
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(38), fill='white')
    out.paste(im, (0, 90)); return out


def xim(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


def fig2img():
    b = BytesIO(); plt.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close()
    return Image.open(b).convert('RGB')


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '实验研究 · 《医疗保健》（Healthcare）2023', font=font(32), fill=TEAL)
for i, t in enumerate(['肩外旋训练：', '坐着、躺着、趴着练，差在哪？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '23 名健康男性 · 3 种体位 × 2 种外展角度 · 7 块肩部肌肉肌电', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Sung J-H 等，Healthcare 2023;11(14):1977', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1 ----------
f1 = xim(84); dr = ImageDraw.Draw(f1)
for b in [(45, 355, 222, 395), (470, 355, 635, 395), (750, 85, 910, 125), (980, 85, 1150, 125), (300, 720, 380, 780), (830, 720, 910, 780)]:
    dr.rectangle(b, fill='white')
dr.text((40, 352), '外旋', font=font(40), fill=INK); dr.text((495, 352), '内旋', font=font(40), fill=INK)
dr.text((790, 80), '内旋', font=font(40), fill=INK); dr.text((1030, 80), '外旋', font=font(40), fill=INK)
ctext(dr, 340, 715, 'A　外展 90° 位旋转', font(42)); ctext(dr, 900, 715, 'B　外展 0° 位旋转', font(42))
save(titled(f1, '原文图 1　不同外展角度下的肩内外旋', 1300), 2)

# ---------- 图 2 六种姿势 ----------
f2 = xim(104)
cols = [(0, 212), (220, 446), (453, 692)]; rows = [(0, 283), (310, 597)]
names = [['坐位 外展 45°', '仰卧 外展 45°', '俯卧 外展 45°'], ['坐位 外展 90°', '仰卧 外展 90°', '俯卧 外展 90°']]
TW, TH = 440, 560
im = Image.new('RGB', (3 * (TW + 10) + 10, 2 * (TH + 70) + 10), 'white'); dr = ImageDraw.Draw(im)
for r, (y0, y1) in enumerate(rows):
    for c, (x0, x1) in enumerate(cols):
        p = f2.crop((x0, y0, x1, y1)); s = min(TW / p.width, TH / p.height)
        p = p.resize((round(p.width * s), round(p.height * s)), Image.LANCZOS)
        X = 10 + c * (TW + 10); Y = 10 + r * (TH + 70)
        dr.rounded_rectangle([X, Y, X + TW, Y + 56], 8, fill=LT if r == 0 else OR)
        ctext(dr, X + TW / 2, Y + 10, names[r][c], font(32), TEAL if r == 0 else (190, 100, 40))
        im.paste(p, (X + (TW - p.width) // 2, Y + 62))
board2 = titled(im, '原文图 2　六种测试条件（等速测力仪，60°/秒）')
save(board2, 3)

# ---------- 图 4 流程 + 图 3 照片 ----------
W, H = 1400, 520; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
heads = [('热身', 20, 300), ('熟悉练习', 330, 700), ('正式测试：5 次全力（随机顺序）', 730, 1380)]
for t, x0, x1 in heads:
    dr.polygon([(x0, 20), (x1 - 30, 20), (x1, 60), (x1 - 30, 100), (x0, 100)], fill=LT, outline=(150, 180, 190))
    ctext(dr, (x0 + x1) / 2 - 10, 42, t, font(30))
dr.rounded_rectangle([20, 130, 300, 300], 18, outline=TEAL, width=3)
for i, t in enumerate(['上肢功率车', '60 转/分']): ctext(dr, 160, 175 + i * 50, t, font(30))
for i, t in enumerate(['外展 45°', '外展 90°']):
    dr.rounded_rectangle([340, 130 + i * 95, 680, 205 + i * 95], 12, outline=TEAL, width=3); ctext(dr, 510, 148 + i * 95, t, font(30))
ctext(dr, 705, 190, '×', font(40))
for i, t in enumerate(['坐位', '仰卧', '俯卧']):
    dr.rounded_rectangle([740, 125 + i * 65, 1340, 182 + i * 65], 10, outline=TEAL, width=3); ctext(dr, 1040, 136 + i * 65, t, font(30))
dr.line([20, 380, 1360, 380], fill=INK, width=5); dr.polygon([(1360, 368), (1385, 380), (1360, 392)], fill=INK)
for x in (300, 700): dr.line([x, 365, x, 395], fill=(40, 110, 220), width=5)
for t, x, y in [('5 分钟', 130, 405), ('休息 3 分钟', 250, 445), ('10 分钟', 470, 405), ('休息 5 分钟', 650, 445), ('20 分钟', 950, 405), ('共 40～45 分钟', 1150, 445)]:
    dr.text((x, y), t, font=font(28), fill=INK)
flow = titled(im, '原文图 4　测试流程')
save(flow, 4)
f3 = xim(158); f3b = f3.copy()
for b in [(20, 50, 120, 135), (120, 0, 240, 100), (735, 520, 781, 610), (330, 190, 420, 245)]:
    f3b.paste(f3.crop(b).filter(ImageFilter.GaussianBlur(9)), b[:2])
save(titled(f3b, '原文图 3　上肢功率车热身', 900), 5)

# ---------- 图 5 折线 ----------
pos = ['坐位', '仰卧', '俯卧']
f5 = {'后三角肌': ([44, 46, 60], [55, 49, 49]), '冈下肌': ([47, 37, 51], [47, 36, 44]),
      '上斜方肌': ([35, 29, 53], [44, 57, 75]), '下斜方肌': ([43, 21, 58], [42, 25, 52])}
fig, axs = plt.subplots(2, 2, figsize=(11, 8))
for ax, (k, (a, b)) in zip(axs.flat, f5.items()):
    ax.plot(pos, a, '-o', color='#9aa3a8', lw=3, ms=9, label='外展 45°')
    ax.plot(pos, b, '-D', color='#1f2a30', lw=3, ms=8, label='外展 90°')
    ax.set_title(k, fontsize=17); ax.set_ylim(0, 100); ax.set_ylabel('平均幅值（%）')
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
axs[0, 1].legend(frameon=False, loc='upper right')
fig.text(0.01, -0.01, '读图近似值（误差线略）。幅值按“坐位 45°”条件的峰值标准化。原图标注的组间差异见正文', fontsize=11, color='#777')
plt.tight_layout()
save(titled(fig2img(), '原文图 5　四块肌肉在六种条件下的肌电（中文重绘）', 1300), 6)

# ---------- 图 6 折线 ----------
f6 = {'下斜方肌/上斜方肌 协同收缩': ([23, 13, 28], [24, 17, 26]), '前锯肌/上斜方肌 协同收缩': ([23, 17, 20], [28, 32, 27]),
      '冈下肌/后三角肌 协同收缩': ([31, 26, 35], [34, 25, 30])}
fig, axs = plt.subplots(1, 3, figsize=(14, 4.8))
for ax, (k, (a, b)) in zip(axs, f6.items()):
    ax.plot(pos, a, '-o', color='#9aa3a8', lw=3, ms=9, label='外展 45°')
    ax.plot(pos, b, '-D', color='#1f2a30', lw=3, ms=8, label='外展 90°')
    ax.set_title(k, fontsize=15); ax.set_ylim(0, 45); ax.set_ylabel('协同收缩指数（×100）')
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
axs[0].legend(frameon=False, loc='lower left')
fig.text(0.01, -0.03, '读图近似值。原图纵轴写“平均幅值（%）”，与表 3 的 0.15～0.33 相差 100 倍，此处按表 3 换算标注', fontsize=11, color='#777')
plt.tight_layout()
save(titled(fig2img(), '原文图 6　三组肌肉的协同收缩指数（中文重绘）', 1300), 7)

# ---------- 比值（表 3） ----------
fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
for ax, (k, v, sig) in zip(axs, [('下斜方肌 / 上斜方肌', [1.27, 0.67, 0.79], ['', 'a', 'a']), ('前锯肌 / 上斜方肌', [1.44, 1.40, 0.57], ['', '', 'a,b'])]):
    bars = ax.bar(pos, v, color=['#00788c', '#9fc5cf', '#9fc5cf'] if k.startswith('下') else ['#00788c', '#00788c', '#e9a07a'], width=0.6)
    for i, x in enumerate(v): ax.text(i, x + 0.03, f'{x:.2f} {sig[i]}', ha='center', fontsize=13)
    ax.axhline(1, color='#999', ls='--', lw=1); ax.set_title(k, fontsize=16); ax.set_ylim(0, 1.7)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.01, -0.04, '均值（原文表 3，两种外展角度合并）。a 与坐位比 P<0.05，b 与仰卧比 P<0.05；虚线 = 1。\n另：下斜方肌/上斜方肌比值 外展 45° 1.03，高于 90° 的 0.79', fontsize=11, color='#777')
plt.tight_layout()
save(titled(fig2img(), '原文表 3　肌电比值：坐位最“偏下斜方、偏前锯”', 1300), 8)

# ---------- 选择建议 ----------
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
rows = [('想多练下斜方肌、少用上斜方肌', '坐位 外展 45°', '下斜方/上斜方比值最高；45° 比 90° 上斜方肌更安静', GR),
        ('想练冈下肌、少用后三角肌', '坐位 45° 或 俯卧 45°', '仰卧时冈下肌最低；坐位 90° 后三角肌会变多', GR),
        ('想练前锯肌（肩胛稳定）', '坐位或仰卧', '俯卧时前锯肌最低、前锯/上斜方比值只有 0.57', GR),
        ('上斜方肌已经过度活跃（如撞击）', '避免 俯卧 90°', '上斜方肌最高（约 75%），三角肌前、中束也更活跃', OR),
        ('健康运动员、追求肩胛协同', '可用 外展 90°', '前锯/上斜方协同收缩更高，更接近投掷位', LT)]
for i, (a, b2, c, bg) in enumerate(rows):
    y0 = 20 + i * 190
    dr.rounded_rectangle([20, y0, W - 20, y0 + 170], 14, fill=bg)
    dr.text((46, y0 + 22), a, font=font(32), fill=INK)
    dr.text((46, y0 + 78), '→ ' + b2, font=font(40), fill=RED if bg == OR else TEAL)
    dr.text((560, y0 + 92), c, font=font(24), fill=GREY)
save(titled(im, '想练哪块肌肉，选哪种外旋姿势（编者根据原文整理）'), 9)

# ---------- 封面 ----------
c = board2.crop((0, 90, board2.width, 90 + 640)); s = 900 / c.width; c = c.resize((900, round(c.height * s)), Image.LANCZOS)
c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
