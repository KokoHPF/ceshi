#!/usr/bin/env python3
"""Prince 2021 腘绳肌孤立力量动作的冲刺特异性（Frontiers 简报）：首图中文标题卡；表 1 六项测试照片拼图加中文名；
图 1 电极位置原图换中文标注；冲刺力-速度关系示意、相关系数图（按表 3）、肌电图（按表 2 均值±标准差重绘）、
六个动作与冲刺阶段对应示意均为编者中文绘制。
用法：python3 make_figs.py <原文 PDF> <补充材料解压目录> <输出目录>"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, SUP, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 14
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(38), fill='white')
    out.paste(im, (0, 90)); return out


def fig2img():
    b = BytesIO(); plt.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close()
    return Image.open(b).convert('RGB')


def photo(i):
    return Image.open(f'{SUP}/fspor-02-609636-i000{i}.jpg').convert('RGB')


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '横断面研究 · 《运动与积极生活前沿》2021', font=font(32), fill=TEAL)
for i, t in enumerate(['腘绳肌力量练习', '离“冲刺”有多远？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '14 名短跑运动员 · 6 个腘绳肌动作 · 水平发力 + 肌电双重比较', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Prince C 等，Front Sports Act Living 2021;2:609636', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 表 1 照片：六项测试 ----------
names = ['① 50 m 冲刺（雷达测速）', '② 北欧挺（髋 0°）', '③ 北欧挺（髋屈 90°）',
         '④ 站立伸髋（向心/等长）', '⑤ 站立踢腿', '⑥ 仰卧滑腿桥']
TW, TH = 680, 470
im = Image.new('RGB', (TW * 2 + 30, (TH + 70) * 3 + 10), 'white'); dr = ImageDraw.Draw(im)
for k in range(6):
    p = photo(k + 1); p.thumbnail((TW, TH), Image.LANCZOS)
    if p.width < TW and p.height < TH:
        s = min(TW / p.width, TH / p.height); p = p.resize((round(p.width * s), round(p.height * s)), Image.LANCZOS)
    x0 = 10 + (k % 2) * (TW + 10); y0 = 10 + (k // 2) * (TH + 70)
    dr.rounded_rectangle([x0, y0, x0 + TW, y0 + 56], 8, fill=(225, 240, 243))
    dr.text((x0 + 16, y0 + 10), names[k], font=font(32), fill=TEAL)
    im.paste(p, (x0 + (TW - p.width) // 2, y0 + 62 + (TH - p.height) // 2))
save(titled(im, '原文表 1 照片　六项测试的姿势与器材'), 2)

# ---------- 图 1 电极位置 ----------
x = [i for i in d[6].get_images() if i[2] == 2008][0][0]
f1 = Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB'); dr = ImageDraw.Draw(f1)
w, h = f1.size
for r, t in ((int(w * 0.452), 'a 半腱肌'), (int(w * 0.99), 'b 股二头肌长头')):
    tw = dr.textlength(t, font=font(64))
    dr.rounded_rectangle([r - tw - 40, int(h * 0.72), r, h - 14], 14, fill='white')
    dr.text((r - tw - 20, int(h * 0.72) + (h - 14 - int(h * 0.72) - 70) // 2), t, font=font(64), fill=INK)
im = titled(f1, '原文图 1　表面肌电电极位置（黑点为电极，× 为肌腹）', 1400)
save(im, 3)

# ---------- 冲刺力-速度关系示意 ----------
fig, ax = plt.subplots(figsize=(8.5, 5.2))
F0, V0 = 7.1, 8.6
ax.plot([0, V0], [F0, 0], color='#00788c', lw=3)
ax.scatter([0, V0], [F0, 0], s=80, color='#be2832', zorder=5, clip_on=False)
ax.annotate('F0：速度为 0 时的理论最大水平力\n（≈ 起跑、加速早期的推地能力）\n本研究均值 7.1 N/kg', (0, F0), (0.8, 7.9), va='top',
            fontsize=13, arrowprops=dict(arrowstyle='->', color='#555'))
ax.annotate('V0：还能产生水平力的理论最高速度\n（≈ 接近最高速时还能不能往后推地）\n本研究均值 8.6 m/s', (V0, 0), (0.5, 2.9), va='top',
            fontsize=13, arrowprops=dict(arrowstyle='->', color='#555'))
ax.set_xlim(0, 9.6); ax.set_ylim(0, 8.2)
ax.set_xlabel('跑速（m/s）'); ax.set_ylabel('水平推地力（N/kg）')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.text(0.99, 0.99, '用雷达测速 + 简单模型\n从一次 50 m 冲刺算出\n直线为示意，数值为本研究均值', transform=ax.transAxes,
        ha='right', va='top', fontsize=11, color='#777')
save(titled(fig2img(), '冲刺“力-速度”关系里的 F0 和 V0（编者示意）', 1300), 4)

# ---------- 相关系数（表 3） ----------
ex = ['北欧挺 0°', '北欧挺 90°', '站立伸髋 等长', '站立伸髋 向心', '站立踢腿', '仰卧滑腿桥']
rv = [0.66, 0.73, 0.56, 0.35, -0.29, 0.29]; pv = ['*', '**', '*', '', '', '']
rf = [0.59, 0.43, 0.60, 0.26, 0.04, 0.09]; pf = ['*', '', '*', '', '', '']
fig, ax = plt.subplots(figsize=(9.5, 6))
y = np.arange(len(ex))
ax.barh(y - 0.2, rf, 0.38, color='#e9a07a', label='与 F0（低速推地）')
ax.barh(y + 0.2, rv, 0.38, color='#4f9fb0', label='与 V0（高速推地）')
for i in range(len(ex)):
    for r, s, dy in ((rf[i], pf[i], -0.2), (rv[i], pv[i], 0.2)):
        ax.text(r + (0.02 if r >= 0 else -0.02), i + dy, f'{r:.2f}{s}', va='center',
                ha='left' if r >= 0 else 'right', fontsize=12)
ax.axvline(0, color='#444', lw=1); ax.axvline(0.5, color='#bbb', ls='--', lw=1)
ax.text(0.505, -0.62, '≥0.5 为“大”相关', fontsize=11, color='#888')
ax.set_yticks(y); ax.set_yticklabels(ex); ax.invert_yaxis()
ax.set_xlim(-0.45, 0.95); ax.set_xlabel('斯皮尔曼相关系数')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(loc='lower left', frameon=False)
ax.text(0.0, -0.13, '* P<0.05，** P<0.01；未做多重比较校正。北欧挺看“断点角”，站立伸髋等长看最大力，其余看峰值速度；\n仰卧滑腿桥速度越慢代表离心能力越好，所以它的正相关方向其实是“反的”',
        transform=ax.transAxes, fontsize=10.5, color='#777', va='top')
save(titled(fig2img(), '原文表 3　动作成绩与冲刺水平发力的相关（编者绘图）', 1300), 5)

# ---------- 肌电（表 2） ----------
bf = [(46.1, 20.3), (29.7, 9.4), (54.0, 27.0), (48.4, 22.9), (27.4, 19.4), (34.3, 16.7)]
st = [(57.8, 18.3), (40.8, 7.9), (53.7, 20.7), (55.2, 22.3), (29.5, 16.0), (39.3, 13.4)]
fig, ax = plt.subplots(figsize=(10, 5.6)); x = np.arange(6)
ax.bar(x - 0.2, [m for m, s in bf], 0.38, yerr=[s for m, s in bf], capsize=4, color='#4f9fb0', label='股二头肌长头')
ax.bar(x + 0.2, [m for m, s in st], 0.38, yerr=[s for m, s in st], capsize=4, color='#e9a07a', label='半腱肌')
ax.axhline(100, color='#be2832', ls='--', lw=1.6); ax.text(5.6, 102, '冲刺最大肌电 = 100%', ha='right', color='#be2832', fontsize=12)
for i in range(6):
    ax.text(i - 0.2, bf[i][0] + bf[i][1] + 2, f'{bf[i][0]:.0f}', ha='center', fontsize=11)
    ax.text(i + 0.2, st[i][0] + st[i][1] + 2, f'{st[i][0]:.0f}', ha='center', fontsize=11)
ax.set_xticks(x); ax.set_xticklabels(['北欧挺 0°', '北欧挺 90°', '站立伸髋\n等长', '站立伸髋\n向心', '站立踢腿', '仰卧滑腿桥'])
ax.set_ylim(0, 112); ax.set_ylabel('峰值肌电（% 冲刺最大值）')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(loc='upper left', frameon=False, ncol=2)
ax.text(0.0, -0.17, '柱为均值，误差线为标准差（按原文表 2 重绘；原图为个体分布小提琴图）。所有动作均显著低于冲刺（P<0.008）',
        transform=ax.transAxes, fontsize=10.5, color='#777', va='top')
save(titled(fig2img(), '原文图 2　六个动作的腘绳肌肌电只有冲刺的三到六成', 1300), 6)

# ---------- 六个动作与冲刺阶段对应 ----------
W, H = 1400, 900; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
ph = [('摆动中期', 60), ('摆动末期', 400), ('触地早期', 740), ('支撑期', 1080)]
for i, (t, x0) in enumerate(ph):
    dr.rounded_rectangle([x0, 30, x0 + 300, 110], 14, fill=(0, 110, 130) if i in (1, 2) else (150, 190, 200))
    dr.text((x0 + 150 - dr.textlength(t, font=font(36)) / 2, 50), t, font=font(36), fill='white')
dr.text((400, 125), '腘绳肌被拉得最长、受力最大、最容易拉伤', font=font(26), fill=RED)
rows = [('站立踢腿', '高速离心（间接）', '髋屈 90° 快速伸膝', 1, (240, 248, 250)),
        ('北欧挺 90°', '慢速离心 · 肌肉较长', '髋屈 90° 前倒', 1, (240, 248, 250)),
        ('站立伸髋 等长', '等长 · 最大力', '单腿站，后脚跟顶墙', 2, (252, 244, 238)),
        ('站立伸髋 向心', '向心 · 快速', '直腿快速后伸', 3, (252, 244, 238)),
        ('北欧挺 0°', '慢速离心 · 肌肉较短', '髋伸直前倒', 0, (245, 245, 245)),
        ('仰卧滑腿桥', '慢速离心 · 肌肉较短', '单腿桥，脚慢慢往远滑', 0, (245, 245, 245))]
for k, (n, m, how, col, fill) in enumerate(rows):
    y0 = 190 + k * 112
    x0 = min(ph[col][1], 1000)
    dr.rounded_rectangle([40, y0, W - 40, y0 + 96], 12, fill=fill, outline=(215, 220, 225))
    dr.text((x0 + 10, y0 + 10), n, font=font(34), fill=INK)
    dr.text((x0 + 10, y0 + 54), m + ' ｜ ' + how, font=font(24), fill=GREY)
dr.text((40, H - 46), '编者按原文和补充材料对各动作“对应阶段”的描述整理；北欧挺 0° 和滑腿桥原文未对应具体阶段，放在最左只表示肌肉较短',
        font=font(20), fill=(150, 150, 150))
save(titled(im, '六个动作分别在模仿冲刺的哪一段（编者整理）'), 7)

# ---------- 封面 ----------
c = photo(2); s = 900 / c.width; c = c.resize((900, round(c.height * s)), Image.LANCZOS)
top = c.height - 383 - 10; c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
