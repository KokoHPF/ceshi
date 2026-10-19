#!/usr/bin/env python3
"""Jahan 2025 器械辅助软组织松动 vs 干拔罐治疗颈痛（印度社区医学杂志短篇）：首图中文标题卡；图 3 CONSORT 流程中文重绘；
两组方案卡；图 1、图 2 照片（模糊器械/拔罐杯上的品牌字样）；图表 1～8 合并重绘为疼痛图与“8 张图里的数字”核对图。
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
LT = (225, 240, 243); OR = (252, 240, 230); GY = (242, 242, 242)
CA, CB = '#00788c', '#e9a07a'
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


def bx(dr, x0, y0, x1, y1, lines, fill, fs=30, col=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill, outline=(120, 150, 170), width=2)
    yy = (y0 + y1 - len(lines) * (fs + 10)) / 2 + 2
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs), col); yy += fs + 10


def down(dr, x, y0, y1):
    dr.line([x, y0, x, y1 - 14], fill=TEAL, width=4); dr.polygon([(x - 12, y1 - 16), (x + 12, y1 - 16), (x, y1)], fill=TEAL)


def blur(im, b, r=8):
    im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r)), b[:2])


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '短篇报告 · 《印度社区医学杂志》2025', font=font(32), fill=TEAL)
for i, t in enumerate(['颈痛：刮痧板式器械松动', 'vs 干拔罐，谁更好？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '30 名患者 · 4 周 · 两组都加上斜方肌牵伸', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Jahan A. Indian J Community Med 2025;50:506-11', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 3 流程 ----------
W, H = 1300, 1000; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
bx(dr, 350, 20, 950, 100, ['评估是否符合条件 58 人'], LT, 32)
dr.line([650, 100, 650, 300], fill=TEAL, width=4); dr.line([650, 160, 840, 160], fill=TEAL, width=4)
bx(dr, 840, 115, 1280, 260, ['排除 28 人', '不符合纳入标准 27 人', '拒绝参加 1 人'], GY, 26)
down(dr, 650, 280, 330)
bx(dr, 350, 330, 950, 410, ['随机分组（抽签）30 人'], LT, 32)
dr.line([650, 410, 650, 450], fill=TEAL, width=4); dr.line([330, 450, 970, 450], fill=TEAL, width=4)
down(dr, 330, 450, 510); down(dr, 970, 450, 510)
for cx, t, c in [(330, ['A 组 器械辅助软组织松动', '15 人接受分配的治疗'], LT), (970, ['B 组 干拔罐', '15 人接受分配的治疗'], OR)]:
    bx(dr, cx - 300, 510, cx + 300, 630, t, c, 28)
    down(dr, cx, 630, 690)
    bx(dr, cx - 300, 690, cx + 300, 800, ['失访 0 人', '中断治疗 0 人'], 'white', 28)
    down(dr, cx, 800, 860)
    bx(dr, cx - 300, 860, cx + 300, 940, ['纳入分析 15 人'], 'white', 30)
dr.text((40, 960), '原文为 CONSORT 模板，“其他原因”“未接受分配”等空格未填', font=font(22), fill=(150, 150, 150))
save(titled(im, '原文图 3　研究流程（中文重绘）'), 2)

# ---------- 方案卡 ----------
W, H = 1400, 1080; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 470], 16, fill=LT)
dr.text((50, 40), 'A 组　器械辅助软组织松动（IASTM）', font=font(38), fill=TEAL)
for i, t in enumerate(['舒适的含胸坐姿，颈部涂凡士林', '先用不锈钢刮板沿上斜方肌探查“受限”区域',
                       '刮板约 45°，从肌肉起点到止点轻柔地顺肌纤维刮', '每次约 3 分钟，全程不引起不适或疼痛',
                       '每周 2 次 × 4 周；治疗后如有灼热感可冰敷']):
    dr.text((60, 110 + i * 70), '· ' + t, font=font(30), fill=INK)
dr.rounded_rectangle([20, 490, W - 20, 790], 16, fill=OR)
dr.text((50, 510), 'B 组　干拔罐', font=font(38), fill=(190, 100, 40))
for i, t in enumerate(['同样含胸坐姿，涂润滑剂', '硅胶罐 + 抽气泵抽出空气，形成负压吸附在皮肤上',
                       '原文没写：放在哪、负压多大、留罐多久、每周几次']):
    dr.text((60, 580 + i * 70), '· ' + t, font=font(30), fill=RED if i == 2 else INK)
dr.rounded_rectangle([20, 810, W - 20, H - 20], 16, fill=GY)
dr.text((50, 830), '两组都加：上斜方肌被动牵伸', font=font(36), fill=INK)
dr.text((60, 900), '· 头向侧屈，保持 30 秒 × 3 次；可加一点低头加大牵拉', font=font(30), fill=INK)
dr.text((60, 970), '· 另外布置居家自我牵伸，每周 5 次', font=font(30), fill=INK)
save(titled(im, '两组怎么治（编者根据原文整理）'), 3)

# ---------- 照片 ----------
f1 = xim(26); blur(f1, (540, 400, 640, 470), 10)
save(titled(f1, '原文图 1　干拔罐（硅胶罐 + 抽气，杯上字样已模糊）', 1200), 4)
f2 = xim(28); blur(f2, (70, 120, 200, 240), 9)
save(titled(f2, '原文图 2　不锈钢软组织松动刮板（品牌字样已模糊）', 1200), 5)

# ---------- 疼痛 ----------
fig, ax = plt.subplots(figsize=(9, 5)); x = np.arange(2)
ax.bar(x - 0.2, [7.25, 5.65], 0.38, yerr=[1.07, 0.91], capsize=5, color=CA, label='A 组 器械松动')
ax.bar(x + 0.2, [7.25, 3.65], 0.38, yerr=[1.07, 0.93], capsize=5, color=CB, label='B 组 干拔罐')
for i, (a, b) in enumerate([(7.25, 7.25), (5.65, 3.65)]):
    ax.text(i - 0.2, a + 1.25, f'{a}', ha='center'); ax.text(i + 0.2, b + 1.25, f'{b}', ha='center')
ax.set_xticks(x); ax.set_xticklabels(['治疗前', '4 周后']); ax.set_ylim(0, 10); ax.set_ylabel('视觉模拟评分（0～10）')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(frameon=False)
fig.text(0.01, -0.04, '均值 ± 标准差（原文表 1、图表 1～2）。两组治疗前数值完全相同（7.25 ± 1.07）；组间疼痛比较没有给 P 值', fontsize=11, color='#777')
save(titled(fig2img(), '原文图表 1、2　疼痛（中文重绘）', 1300), 6)

# ---------- 8 张图核对 ----------
fig, ax = plt.subplots(figsize=(11, 5.6))
labels = ['正常人\n颈椎前屈', '正常人\n颈椎侧屈', 'A 组前屈\n治疗前', 'A 组前屈\n4 周后', 'B 组前屈\n治疗前', 'B 组前屈\n4 周后']
vals = [50, 45, 151.2, 152.67, 149.47, 176.93]
cols = ['#9fc5cf', '#9fc5cf', CA, CA, CB, CB]
ax.bar(range(6), vals, color=cols, width=0.6)
for i, v in enumerate(vals): ax.text(i, v + 3, f'{v:g}°' if i > 1 else f'约 {v}°', ha='center', fontsize=12)
ax.axhline(90, color='#be2832', ls='--', lw=1.2); ax.text(5.45, 93, '90°', color='#be2832', ha='right', fontsize=11)
ax.set_xticks(range(6)); ax.set_xticklabels(labels, fontsize=12); ax.set_ylabel('活动度（°）'); ax.set_ylim(0, 200)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.01, -0.07, '正常值为常用参考（量角器测量约 45°～50°）。原文图表 5、8 标为“侧屈”的数值（152.67、176.93）与前屈完全相同；\n图表 6 标为“B 组前屈”的数值（151.2→152.67）其实是 A 组的；图表 7 用 B 组治疗前的 149.47 当作“A 组治疗后”', fontsize=11, color='#777')
save(titled(fig2img(), '核对：报告的颈椎活动度约是正常值的 3 倍', 1300), 7)

# ---------- 封面 ----------
c = xim(26); s = 900 / c.width; c = c.resize((900, round(c.height * s)), Image.LANCZOS); blur(c, (480, 356, 570, 420), 8)
top = 150; c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
