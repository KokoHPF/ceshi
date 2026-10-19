#!/usr/bin/env python3
"""Uttamchandani 2024 PowerBall vs Mulligan 动态关节松动治疗网球肘（Cureus 随机对照试验）：首图中文标题卡；
图 1 流程中文重绘；图 2～6 照片加中文标注（握力计表盘文字模糊）；两组方案卡、结果图（按表 4～6）、
“均值差核对”图为编者中文绘制。
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
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); GY = (242, 242, 242)
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


def xim(x, w=None):
    im = Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')
    if w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    return im


def fig2img():
    b = BytesIO(); plt.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close()
    return Image.open(b).convert('RGB')


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def tag(dr, x, y, t, fs=34):
    w = dr.textlength(t, font=font(fs))
    dr.rounded_rectangle([x, y, x + w + 28, y + fs + 22], 10, fill=(255, 255, 255))
    dr.text((x + 14, y + 9), t, font=font(fs), fill=TEAL)


def bx(dr, x0, y0, x1, y1, lines, fill, fs=30, col=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill, outline=(120, 150, 170), width=2)
    yy = (y0 + y1 - len(lines) * (fs + 10)) / 2 + 2
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs), col); yy += fs + 10


def down(dr, x, y0, y1):
    dr.line([x, y0, x, y1 - 14], fill=TEAL, width=4); dr.polygon([(x - 12, y1 - 16), (x + 12, y1 - 16), (x, y1)], fill=TEAL)


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '随机对照试验 · 《Cureus》2024', font=font(32), fill=TEAL)
for i, t in enumerate(['网球肘：陀螺腕力球', 'vs Mulligan 动态松动']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '50 名患者 · 3 周 · 每周 5 次 · 都加超声和常规练习', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Uttamchandani SR, Phansopkar P. Cureus 2024;16(3):e56444', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1 流程 ----------
W, H = 1300, 1060; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
bx(dr, 350, 20, 950, 100, ['肱骨外上髁炎患者 88 人评估'], LT, 32)
down(dr, 650, 100, 160)
bx(dr, 350, 160, 950, 290, ['排除 38 人：拒绝 14 人、', '不符合纳入标准 19 人、其他 5 人'], GY, 28)
down(dr, 650, 290, 350)
bx(dr, 350, 350, 950, 430, ['随机分组（序号不透明信封）50 人'], LT, 30)
dr.line([650, 430, 650, 470], fill=TEAL, width=4); dr.line([330, 470, 970, 470], fill=TEAL, width=4)
down(dr, 330, 470, 530); down(dr, 970, 470, 530)
for cx, g, t, c in [(330, 'A 组 25 人（试验组）', ['陀螺腕力球训练', '+ 超声 + 常规练习'], LT), (970, 'B 组 25 人（“常规组”）', ['Mulligan 动态关节松动', '+ 超声 + 常规练习'], OR)]:
    bx(dr, cx - 300, 530, cx + 300, 610, ['治疗前测评'], 'white', 30)
    down(dr, cx, 610, 670)
    bx(dr, cx - 300, 670, cx + 300, 830, [g, '3 周，每周 5 次'] + t, c, 28)
    down(dr, cx, 830, 890)
    bx(dr, cx - 300, 890, cx + 300, 970, ['第 3 周末测评'], 'white', 30)
dr.text((40, 1000), '原图仅有方框流程，人数为编者按正文补充；原图“治疗后测评”与“第 3 周测评”重复列出，此处合并', font=font(22), fill=(150, 150, 150))
save(titled(im, '原文图 1　研究流程（中文重绘）'), 2)

# ---------- 图 2 Mill 试验 ----------
save(titled(xim(72, 1300), '原文图 2　Mill 试验：被动屈腕 + 前臂旋前 + 伸肘，外上髁痛为阳性'), 3)

# ---------- 共同方案卡 ----------
W, H = 1400, 760; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 230], 16, fill=LT)
dr.text((50, 40), '① 治疗性超声', font=font(36), fill=TEAL)
dr.text((50, 100), '坐位，肩中立、肘屈 90° 完全支撑', font=font(30), fill=INK)
dr.text((50, 150), '压痛点 · 脉冲模式 · 1 W/cm² · 10 分钟', font=font(30), fill=RED)
dr.rounded_rectangle([20, 250, W - 20, H - 20], 16, fill=GR)
dr.text((50, 270), '② 常规练习（每个动作 3 组 × 10 次）', font=font(36), fill=(40, 120, 60))
for i, t in enumerate(['用力握拳（捏软球）', '腕屈肌、腕伸肌抗阻训练（按 DeLorme 渐进抗阻原则加量）',
                       '前臂旋前、旋后练习（拧弹力带）', '腕部牵伸，每次至少 30 秒（含合掌牵伸）']):
    dr.text((70, 340 + i * 80), '· ' + t, font=font(30), fill=INK)
dr.text((50, 680), '两组每次都先做超声和常规练习，再各自做腕力球或 Mulligan 松动', font=font(26), fill=GREY)
save(titled(im, '两组共同的基础治疗（每周 5 次 × 3 周）'), 4)

# ---------- 图 3、4 照片 ----------
f3 = xim(90, 1000); dr = ImageDraw.Draw(f3); h = f3.height
for y, t in [(0.03, '捏球握拳'), (0.355, '双手拧弹力带（前臂旋转）'), (0.68, '超声治疗')]:
    tag(dr, 40, int(h * y) + 10, t)
f4 = xim(101, 1000); dr = ImageDraw.Draw(f4); h = f4.height
for x, y, t in [(40, 0.03, '合掌牵伸'), (40, 0.515, '哑铃腕部力量'), (530, 0.515, '前臂牵伸'), (40, 0.76, '哑铃腕部力量'), (530, 0.76, '前臂牵伸')]:
    tag(dr, x, int(h * y) + 10, t, 30)
both = Image.new('RGB', (2020, max(f3.height, f4.height)), 'white'); both.paste(f3, (0, 0)); both.paste(f4, (1020, 0))
save(titled(both, '原文图 3、4　常规练习与超声'), 5)

# ---------- 腕力球方案（表 1） ----------
W, H = 1400, 1020; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.text((30, 20), '4 个动作：手握腕力球转动，分别做', font=font(30), fill=INK)
moves = ['屈腕', '伸腕', '屈肘', '伸肘']; pose = ['坐位 前臂搭桌', '坐位 前臂搭桌', '站立', '站立 躯干前倾']
for i in range(4):
    x0 = 30 + i * 340
    dr.rounded_rectangle([x0, 75, x0 + 320, 185], 12, fill=LT)
    ctext(dr, x0 + 160, 85, moves[i], font(40), TEAL); ctext(dr, x0 + 160, 140, pose[i], font(24), GREY)
wk = [('第 1 周', '轻', '3 组 × 30 秒', '组间 1 分钟', '动作间 2 分钟', '约 20 分钟', GR),
      ('第 2 周', '中', '4 组 × 45 秒', '组间 1.5 分钟', '动作间 3 分钟', '约 39 分钟', OR),
      ('第 3 周', '重', '5 组 × 60 秒', '组间 2 分钟', '动作间 4 分钟', '约 64 分钟', (250, 225, 225))]
for i, (w, lv, s, r1, r2, tt, bg) in enumerate(wk):
    y0 = 215 + i * 200
    dr.rounded_rectangle([30, y0, W - 30, y0 + 180], 14, fill=bg)
    dr.text((60, y0 + 20), w, font=font(40), fill=INK); dr.text((60, y0 + 90), '强度：' + lv, font=font(30), fill=GREY)
    dr.text((320, y0 + 30), s, font=font(48), fill=RED)
    dr.text((320, y0 + 110), r1 + '　' + r2, font=font(28), fill=INK)
    dr.text((1060, y0 + 60), tt, font=font(38), fill=TEAL)
dr.text((30, 830), '· 转速按个人能力从约 2000 逐步提高到 10,000 转/分（原文误写为“加仑/分”）', font=font(26), fill=INK)
dr.text((30, 880), '· 允许轻微症状下继续；疼痛加重或影响功能就停', font=font(26), fill=INK)
dr.text((30, 930), '· 做起来已无不适时，可加手持重物增加阻力', font=font(26), fill=INK)
dr.text((30, 980), '原文表 1，编者中文重排', font=font(22), fill=(150, 150, 150))
save(titled(im, 'A 组：陀螺腕力球 3 周进阶方案'), 6)

# ---------- 图 5 ----------
f5 = xim(120); w, h = f5.size
dial = (int(w * 0.06), int(h * 0.03), int(w * 0.28), int(h * 0.32))
f5.paste(f5.crop(dial).filter(ImageFilter.GaussianBlur(18)), dial[:2])
f5 = f5.resize((1300, round(h * 1300 / w)), Image.LANCZOS); dr = ImageDraw.Draw(f5)
tag(dr, 20, f5.height - 80, '握力计测无痛握力'); tag(dr, 600, f5.height - 80, '手握陀螺腕力球')
save(titled(f5, '原文图 5　握力测试与腕力球（表盘文字已模糊）'), 7)
c = f5.crop((565, 400, 1300, 400 + 313)).resize((900, 383), Image.LANCZOS)
c.save(f'{OUT}/cover.jpg', quality=90)

# ---------- MMWM ----------
W, H = 1400, 760; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 330], 16, fill=OR)
dr.text((50, 40), '做法', font=font(36), fill=(190, 100, 40))
for i, t in enumerate(['患者仰卧，肘伸直、前臂旋前', '治疗带绕过治疗师身体和患者前臂近端（肘上方），持续向外侧滑动',
                       '滑动的同时让患者握拳（或握握力计）、伸腕，全程无痛', '每次 30 次，每 10 次休息 1 分钟']):
    dr.text((60, 100 + i * 55), '· ' + t, font=font(28), fill=INK)
for i, (w, s, t) in enumerate([('第 1 周', '3 × 10', '约 32 分钟'), ('第 2 周', '3 × 15', '约 47 分钟'), ('第 3 周', '3 × 20', '约 62 分钟')]):
    x0 = 20 + i * 460
    dr.rounded_rectangle([x0, 360, x0 + 440, 600], 14, fill=LT)
    ctext(dr, x0 + 220, 380, w, font(36), TEAL); ctext(dr, x0 + 220, 440, s, font(56), RED); ctext(dr, x0 + 220, 530, '组间 1 分钟 · ' + t, font(26), GREY)
dr.text((30, 630), '原文表 2 写“坐在治疗床上”，正文写“仰卧”；正文“每次 30 次”与表 2 第 2、3 周的', font=font(24), fill=(150, 150, 150))
dr.text((30, 670), '45 次、60 次不一致；30～60 次松动耗时 32～62 分钟也明显偏长。编者照录', font=font(24), fill=(150, 150, 150))
save(titled(im, 'B 组：Mulligan 动态关节松动（外侧滑动 + 握拳）'), 8)
save(titled(xim(134, 1000), '原文图 6　Mulligan 动态关节松动：治疗带外侧滑动 + 主动握拳'), 9)

# ---------- 主要结果 ----------
fig, axs = plt.subplots(1, 4, figsize=(15, 4.8))
data = [('静息痛（视觉模拟评分）', [6.56, 2.60], [6.20, 1.96], (0, 9)), ('活动痛（视觉模拟评分）', [7.56, 4.32], [7.28, 3.80], (0, 9)),
        ('网球肘患者自评（PRTEE）', [52.68, 31.28], [56.72, 30.64], (0, 70)), ('握力（kg）', [18.4, 23.0], [19.2, 22.3], (0, 28))]
for ax, (t, a, b, yl) in zip(axs, data):
    x = np.arange(2)
    ax.bar(x - 0.2, a, 0.38, color=CA, label='A 组 腕力球'); ax.bar(x + 0.2, b, 0.38, color=CB, label='B 组 Mulligan')
    for i in range(2):
        ax.text(i - 0.2, a[i] + yl[1] * 0.015, f'{a[i]:g}', ha='center', fontsize=11); ax.text(i + 0.2, b[i] + yl[1] * 0.015, f'{b[i]:g}', ha='center', fontsize=11)
    ax.set_xticks(x); ax.set_xticklabels(['治疗前', '治疗后']); ax.set_title(t, fontsize=14); ax.set_ylim(*yl)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
axs[0].legend(frameon=False, loc='upper right', fontsize=11)
fig.text(0.01, -0.04, '均值，按原文表 4 重绘（原图 7～9）。注意：治疗后疼痛和 PRTEE 其实是 B 组更低', fontsize=11, color='#777')
plt.tight_layout()
save(titled(fig2img(), '原文图 7～9　疼痛、功能、握力（中文重绘）', 1300), 10)

# ---------- 均值差核对 ----------
items = ['静息痛', '活动痛', 'PRTEE', '握力']
rep_a = [4.6, 3.5, 26.08, 4.62]; rep_b = [4.0, 3.2, 21.40, 3.11]
cal_a = [3.96, 3.24, 21.40, 4.6]; cal_b = [4.24, 3.48, 26.08, 3.1]
fig, axs = plt.subplots(1, 4, figsize=(13, 4.6))
for i, ax in enumerate(axs):
    x = np.arange(2)
    ax.bar(x - 0.2, [rep_a[i], rep_b[i]], 0.38, color='#bbbbbb', label='原文表 4 写的改善量')
    ax.bar(x + 0.2, [cal_a[i], cal_b[i]], 0.38, color=[CA, CB], label='按前后均值算出的改善量')
    for j, v in enumerate([rep_a[i], rep_b[i]]): ax.text(j - 0.2, v * 1.02, f'{v:g}', ha='center', fontsize=11)
    for j, v in enumerate([cal_a[i], cal_b[i]]): ax.text(j + 0.2, v * 1.02, f'{v:g}', ha='center', fontsize=11, color='#be2832' if i < 3 else '#333')
    ax.set_xticks(x); ax.set_xticklabels(['A 组', 'B 组']); ax.set_title(items[i], fontsize=15)
    ax.set_ylim(0, max(rep_a[i], rep_b[i], cal_a[i], cal_b[i]) * 1.25)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color='#bbbbbb', label='原文表 4 写的改善量'), Patch(color=CA, label='按前后均值算：A 组'), Patch(color=CB, label='按前后均值算：B 组')], loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.08), fontsize=12)
fig.text(0.01, -0.13, 'PRTEE 两组的改善量正好对调：按原文自己的前后均值，B 组改善 26.08 分、A 组 21.40 分；疼痛也是 B 组改善更多', fontsize=11, color='#777')
plt.tight_layout()
save(titled(fig2img(), '核对：原文的“组间差异”和它自己的数据对不上', 1300), 11)

# ---------- 活动度 ----------
rom = [('伸腕', 55.0, 67.4, 55.5, 66.6), ('屈腕', 59.8, 75.9, 58.8, 73.0), ('桡偏', 12.4, 17.8, 13.0, 17.4), ('尺偏', 25.3, 33.6, 25.7, 32.0),
       ('旋后', 75.0, 82.2, 75.4, 80.9), ('旋前', 67.8, 77.0, 76.3, 83.7), ('屈肘', 110.0, 135.0, 109.7, 131.6)]
fig, ax = plt.subplots(figsize=(12, 4.8)); x = np.arange(len(rom))
ax.bar(x - 0.2, [r[2] - r[1] for r in rom], 0.38, color=CA, label='A 组 改善量')
ax.bar(x + 0.2, [r[4] - r[3] for r in rom], 0.38, color=CB, label='B 组 改善量')
for i, r in enumerate(rom):
    ax.text(i - 0.2, r[2] - r[1] + 0.4, f'{r[2]-r[1]:.1f}', ha='center', fontsize=10); ax.text(i + 0.2, r[4] - r[3] + 0.4, f'{r[4]-r[3]:.1f}', ha='center', fontsize=10)
ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rom]); ax.set_ylabel('活动度改善（°）')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(frameon=False)
fig.text(0.01, -0.06, '按原文表 5、6 前后均值计算（原图 10、11）。表 5“伸肘”数值与屈肘几乎相同（110°→135°），明显是复制错误，未画；\n旋前基线 A 组 67.8° vs B 组 76.3°，两组起点就差了 8.5°', fontsize=11, color='#777')
save(titled(fig2img(), '原文图 10、11　活动度改善（中文重绘）', 1300), 12)
print('ok')
