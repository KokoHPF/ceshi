#!/usr/bin/env python3
"""Sohrabi 2024 踝背屈受限女运动员综合纠正训练 RCT：首图中文标题卡；图 1 流程中文重绘；图 2～6 测量照片去英文字母
（KG/HW、A～D）换中文、模糊量角器英文字样；训练流程卡；肌电结果按原文表 4 数值作图。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import numpy as np
import cv2

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def raw(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


def titled(ph, title, w=1300):
    ph = ph.resize((w, round(ph.height * w / ph.width)), Image.LANCZOS)
    out = Image.new('RGB', (w, ph.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, w, 76], fill=TEAL); od.text((28, 16), title, font=font(40), fill='white')
    out.paste(ph, (0, 90)); return out


def blur(im, box, r=18):
    im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(r)), box[:2])


def inpaint(im, box, thr=90):
    """把框内的深色字母用 OpenCV 修补掉（不留色块）"""
    a = np.array(im); x0, y0, x1, y1 = [int(v) for v in box]
    m = np.zeros(a.shape[:2], np.uint8)
    sub = a[y0:y1, x0:x1].min(axis=2) < thr
    m[y0:y1, x0:x1][sub] = 255
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    out = cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA)
    im.paste(Image.fromarray(out))


def tag(dr, x, y, t, fs=44, anchor='l'):
    f = font(fs); w = dr.textlength(t, font=f)
    x0 = x if anchor == 'l' else x - w - 24
    dr.rounded_rectangle([x0, y, x0 + w + 24, y + fs + 20], 10, fill=(255, 255, 255))
    dr.text((x0 + 12, y + 8), t, font=f, fill=INK)


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '随机对照试验 · 《公共科学图书馆·综合》（PLOS ONE）2024', font=font(32), fill=TEAL)
for i, t in enumerate(['踝背屈受限的女运动员：', '8 周综合纠正训练的效果']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '30 名 15～25 岁女运动员 · 软组织松解 + 关节松动 + 牵伸 + 力量', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Sohrabi T 等，PLoS ONE 2024;19(10):e0312152', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，原文以 CC0 公有领域协议发布', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1 流程 ----------
W, H = 1300, 1060; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def bx(x0, y0, x1, y1, lines, fill, fs=28):
    dr.rounded_rectangle([x0, y0, x1, y1], 10, fill=fill)
    yy = (y0 + y1 - len(lines) * (fs + 10)) / 2 + 3
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs)); yy += fs + 10


def ar(x, a, b, c=(120, 170, 200)):
    dr.line([x, a, x, b], fill=c, width=6); dr.polygon([(x, b + 6), (x - 13, b - 12), (x + 13, b - 12)], fill=c)


bx(330, 20, 770, 90, ['评估是否符合条件（57 人）'], (225, 232, 245))
dr.line([770, 55, 830, 55], fill=(120, 170, 200), width=6)
bx(830, 15, 1280, 200, ['排除 27 人：', '不符合纳入标准 11 人', '拒绝参加 8 人', '其他原因 8 人'], (245, 230, 230), 26)
ar(550, 90, 140)
bx(380, 145, 720, 210, ['随机分组（30 人）'], (200, 230, 210), 30)
ar(550, 210, 250); dr.line([300, 250, 1000, 250], fill=(120, 170, 200), width=6); ar(300, 250, 290); ar(1000, 250, 290)
for cx, t in [(300, ['训练组 15 人', '完成干预前评估 15 人', '接受 8 周训练 15 人']), (1000, ['对照组 15 人', '完成干预前评估 15 人', '不做干预 15 人'])]:
    bx(cx - 280, 295, cx + 280, 450, t, (250, 238, 210), 28)
    ar(cx, 450, 510)
bx(380, 510, 920, 575, ['8 周后'], (225, 232, 245), 30)
for cx, t in [(300, ['训练组 15 人', '完成干预后评估 15 人']), (1000, ['对照组 15 人', '完成干预后评估 15 人'])]:
    ar(cx, 575, 630); bx(cx - 280, 635, cx + 280, 750, t, (240, 240, 240), 28); ar(cx, 750, 810)
    bx(cx - 280, 815, cx + 280, 900, ['纳入分析 15 人'], (225, 232, 245), 30)
ctext(dr, 650, 960, '注：对照组在研究结束后也接受了同样的训练。', font(26), GREY)
save(im, 2)

# ---------- 图 2 背屈测量 ----------
ph = raw(66); dr = ImageDraw.Draw(ph); k = ph.width / 600
for b in [(508, 346, 550, 380), (414, 454, 458, 486)]:
    inpaint(ph, [v * k for v in b])
dr = ImageDraw.Draw(ph); fig2 = ph.copy()
tag(dr, 505 * k, 300 * k, '膝—地高度', 50, 'r')
tag(dr, 330 * k, 440 * k, '足跟—墙距离', 50, 'r')
save(titled(ph, '原文图 2　负重弓步背屈角度测量（三角函数法）'), 3)

# ---------- 图 3 本体感觉（模糊量角器英文字样） ----------
ph = raw(80); k = ph.width / 600
for b in [(140, 435, 250, 475), (385, 180, 450, 290)]:
    blur(ph, tuple(int(v * k) for v in b), 14)
save(titled(ph, '原文图 3　踝关节位置觉测量（被动—主动复位法）', 1000), 4)

# ---------- 图 4 Y 平衡（去掉 A/B/C，换中文） ----------
ph = raw(96); ph = ph.crop((0, 0, ph.width, ph.height - 75)); dr = ImageDraw.Draw(ph); w3 = ph.width / 3
for i, t in enumerate(['前向', '后外侧', '后内侧']):
    tag(dr, i * w3 + 20, ph.height - 90, t, 50)
save(titled(ph, '原文图 4　Y 平衡测试的三个方向'), 5)

# ---------- 图 5 过顶深蹲 ----------
save(titled(raw(95), '原文图 5　过顶深蹲（同步记录肌电）'), 6)

# ---------- 图 6 电极位置（去掉 A～D，换中文） ----------
ph = raw(112); k = ph.width / 600; dr = ImageDraw.Draw(ph)
for b in [(258, 320, 294, 360), (561, 320, 596, 360), (258, 617, 294, 660), (561, 617, 596, 660)]:
    inpaint(ph, [v * k for v in b])
dr = ImageDraw.Draw(ph)
for (x, y), t in zip([(290, 300), (592, 300), (290, 598), (592, 598)], ['胫骨前肌', '腓骨长肌', '腓肠肌内侧头', '比目鱼肌']):
    tag(dr, x * k, y * k, t, 50, 'r')
save(titled(ph, '原文图 6　肌电电极位置', 1000), 7)

# ---------- 训练流程卡 ----------
W, H = 1300, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, W, 90], fill=TEAL); dr.text((36, 20), '综合纠正训练：每次课的 5 个步骤（每周 3 次 × 8 周）', font=font(42), fill='white')
STEPS = [
    ('① 热身', '固定自行车 15 分钟', (225, 232, 245)),
    ('② 软组织松解', '器械松解（Graston）小腿三头肌、跟腱、足底筋膜 5 分钟：\n先扫 1 分钟找粘连，再针对处理 4 分钟；\n第 13 次课起改为泡沫轴自我放松（每处停 30 秒）', (250, 238, 210)),
    ('③ 关节松动', '站立位绑带距小腿关节松动 + 小腿牵伸：\n5 次 × 每次保持 30 秒，膝向前推、足跟不离地、无痛', (232, 245, 225)),
    ('④ 牵伸', '斜板小腿牵伸，伸膝、屈膝各做：\n3 次 × 每次保持 30 秒', (240, 232, 248)),
    ('⑤ 力量', '提踵 → 屈膝提踵 → 台阶上单腿离心提踵：各 1 组 × 15 次；\n双腿→单腿、直膝→屈膝、地面→台阶逐步进阶', (250, 228, 228)),
]
y = 115
for name, body, col in STEPS:
    lines = body.split('\n'); h = 60 + 44 * len(lines)
    dr.rounded_rectangle([40, y, W - 40, y + h], 14, fill=col)
    dr.text((70, y + 22), name, font=font(38), fill=INK)
    for j, l in enumerate(lines):
        dr.text((390, y + 26 + j * 44), l, font=font(28), fill=INK)
    y += h + 18
save(im.crop((0, 0, W, y + 10)), 8)

# ---------- 肌电结果图（原文表 4，训练组前后与对照组前后） ----------
M = [('胫骨前肌', (51.98, 37.39, 49.36, 52.92), (30.74, 22.10, 29.34, 32.23)),
     ('腓骨长肌', (46.09, 42.59, 47.98, 49.90), (32.16, 31.44, 34.34, 27.78)),
     ('腓肠肌内侧头', (17.67, 14.87, 16.49, 18.64), (13.87, 12.14, 14.34, 15.91)),
     ('比目鱼肌', (32.27, 20.34, 28.90, 29.52), (36.88, 22.69, 37.73, 38.06))]
fig, axs = plt.subplots(1, 2, figsize=(12, 5.2), dpi=150, sharey=True)
cols = ['#9bbbd4', '#1f5f8b', '#e3b9a4', '#b5532c']
labs = ['训练组 前', '训练组 后', '对照组 前', '对照组 后']
for a, (ph_i, ttl) in zip(axs, [(1, '下蹲阶段'), (2, '起身阶段')]):
    for j in range(4):
        a.bar([i + (j - 1.5) * 0.2 for i in range(4)], [m[ph_i][j] for m in M], 0.2, color=cols[j], label=labs[j])
    a.set_xticks(range(4)); a.set_xticklabels([m[0] for m in M]); a.set_title(ttl, fontsize=14)
    for s in ['top', 'right']: a.spines[s].set_visible(False)
axs[0].set_ylabel('肌肉激活（%最大自主收缩）'); axs[1].legend(frameon=False, fontsize=11)
fig.suptitle('过顶深蹲时的小腿肌肉激活（原文表 4 均值）', fontsize=15)
fig.tight_layout(); fig.savefig(f'{OUT}/_p.png'); plt.close(fig)
save(Image.open(f'{OUT}/_p.png'), 9)
import os; os.remove(f'{OUT}/_p.png')

# ---------- 封面 900×383 ----------
c = fig2; c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = int(c.height * 0.42); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
