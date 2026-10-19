#!/usr/bin/env python3
"""Boren 2011 臀中肌、臀大肌康复动作肌电（IJSPT）：首图中文标题卡；表 4、5 排名中文重绘为条形图与双肌对照图；
原文图 1～18 照片按动作类型拼板，每格加中文名与两块肌肉的 %MVIC（训练平台标识已模糊）；动作进阶阶梯卡。
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
plt.rcParams['font.size'] = 13
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233)
doc = pymupdf.open(PDF)

# 名称: (臀中肌, 臀大肌)
D = {'侧桥外展（优势腿在下）': (103.11, 70.96), '侧桥外展（优势腿在上）': (88.82, 72.87), '单腿蹲': (82.26, 70.74),
     '蚌式 4': (76.88, 26.22), '平板支撑 + 伸髋': (75.13, 106.22), '蚌式 3': (67.63, 26.63), '侧卧外展': (62.91, 51.13),
     '蚌式 2': (62.45, 12.36), '侧向上台阶': (59.87, 63.83), '滑冰者蹲': (59.84, 66.18), '骨盆下降': (58.43, 25.10),
     '画圈（稳定面）': (57.39, 37.85), '动态摆腿': (57.30, 33.65), '单腿硬拉': (56.08, 58.84), '单腿桥（稳定面）': (54.99, 54.24),
     '向前上台阶': (54.62, 54.67), '单腿桥（不稳定面）': (47.29, 49.35), '蚌式 1': (47.23, 53.10), '四点跪伸髋（优势腿动）': (46.67, 59.70),
     '臀肌夹紧': (43.72, 80.72), '画圈（不稳定面）': (37.88, 28.87), '四点跪伸髋（非优势腿动）': (22.03, 21.04)}


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def xim(x):
    return Image.open(BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def blur(im, box, r=10):
    im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(r)), box[:2])


def fig2img():
    b = BytesIO(); plt.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close()
    return Image.open(b).convert('RGB')


def photo(x, W=900, blurs=()):
    im = xim(x); s = W / im.width; im = im.resize((W, round(im.height * s)), Image.LANCZOS)
    for b in blurs: blur(im, b, 8)
    return im


def tile(im, name, sub, W=1200):
    s = min(W / im.width, 760 / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    t = Image.new('RGB', (W, im.height + 120), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 6, W, 104], 8, fill=LT)
    dr.text((16, 14), name, font=font(32), fill=TEAL)
    if name in D:
        m, x = D[name]
        for k, (lab, v) in enumerate([('臀中肌', m), ('臀大肌', x)]):
            c = RED if v >= 70 else INK
            dr.text((16 + k * 270, 60), f'{lab} {v:.0f}%', font=font(28), fill=c)
    if sub: dr.text((560, 62), sub, font=font(24), fill=GREY)
    t.paste(im, ((W - im.width) // 2, 112)); return t


def board(items, title):
    tiles = [tile(*it) for it in items]
    H = sum(t.height for t in tiles) + 16 * len(tiles)
    out = Image.new('RGB', (1200, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 16
    return titled(out, title)


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '肌电研究 · 《国际运动物理治疗杂志》（IJSPT）2011', font=font(32), fill=TEAL)
for i, t in enumerate(['练臀中肌、臀大肌，', '18 个动作谁最“出力”？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '24 名健康人 · 表面肌电 · 22 种动作条件排名', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Boren K 等，Int J Sports Phys Ther 2011;6(3):206-223', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 排名图 ----------
def rank(idx, title, col):
    items = sorted(D.items(), key=lambda kv: kv[1][idx])
    fig, ax = plt.subplots(figsize=(10, 9))
    v = [x[1][idx] for x in items]
    ax.barh(range(len(items)), v, color=[col if a >= 70 else '#c9d6da' for a in v])
    for i, a in enumerate(v): ax.text(a + 1, i, f'{a:.0f}', va='center', fontsize=12)
    ax.set_yticks(range(len(items))); ax.set_yticklabels([x[0] for x in items], fontsize=13)
    ax.axvline(70, color='#be2832', ls='--', lw=1.4); ax.text(71, -0.9, '70%：作者认定的“够力量训练”门槛', color='#be2832', fontsize=11)
    ax.set_xlim(0, 118); ax.set_xlabel('峰值肌电（% 最大自主等长收缩）')
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    return titled(fig2img(), title, 1300)


save(rank(0, '原文表 4　臀中肌：22 种动作排名', '#00788c'), 2)
save(rank(1, '原文表 5　臀大肌：22 种动作排名', '#c8643c'), 3)

# 双肌散点
fig, ax = plt.subplots(figsize=(9, 8.5))
order = sorted(D.items(), key=lambda kv: -kv[1][0])
for i, (k, (m, x)) in enumerate(order):
    both = m >= 70 and x >= 70
    ax.scatter(m, x, s=260, color='#be2832' if both else '#00788c', zorder=3)
    ax.text(m, x, str(i + 1), color='white', ha='center', va='center', fontsize=10, zorder=4, fontweight='bold')
lines = [f'{i + 1}  {k}（{m:.0f} / {x:.0f}）' for i, (k, (m, x)) in enumerate(order)]
fig.text(0.93, 0.5, '\n'.join(lines), fontsize=11.5, va='center', linespacing=1.55)
ax.axvline(70, color='#999', ls='--', lw=1); ax.axhline(70, color='#999', ls='--', lw=1)
ax.fill_between([70, 112], 70, 112, color='#fde3e3', zorder=0)
ax.text(108, 108, '两块肌肉都 ≥70%', ha='right', va='top', color='#be2832', fontsize=13)
ax.set_xlim(15, 112); ax.set_ylim(8, 112)
ax.set_xlabel('臀中肌（%MVIC）'); ax.set_ylabel('臀大肌（%MVIC）'); fig.text(0.93, 0.9, '编号按臀中肌排名（臀中 / 臀大）', fontsize=11, color='#777')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
save(titled(fig2img(), '原文表 6　同时练到臀中肌和臀大肌的动作（编者绘图）', 1300), 4)

# ---------- 进阶阶梯 ----------
W, H = 1400, 1060; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
lv = [('入门：卧位、支撑多', '蚌式 1（臀中 47 / 臀大 53）、四点跪伸髋（47 / 60）、单腿桥（55 / 54）、侧卧外展（63 / 51）', LT),
      ('进阶：负重单腿', '骨盆下降（58 / 25）、向前上台阶（55 / 55）、侧向上台阶（60 / 64）、单腿硬拉（56 / 59）、滑冰者蹲（60 / 66）', GR),
      ('专练臀中肌', '蚌式 2～4：伸髋位做髋内旋，臀中肌 62～77%，臀大肌只有 12～27%', OR),
      ('高阶：两块都 ≥70%', '侧桥外展（89～103 / 71～73）、单腿蹲到 47 cm 椅子（82 / 71）、平板支撑 + 伸髋（75 / 106）', (250, 225, 225)),
      ('专练臀大肌的简单办法', '站立“臀肌夹紧”：口令要求全力收紧，臀大肌 81%', LT)]
for i, (t, s, bg) in enumerate(lv):
    y = 20 + i * 205
    dr.rounded_rectangle([20, y, W - 20, y + 185], 14, fill=bg)
    dr.text((50, y + 22), t, font=font(38), fill=TEAL if i != 3 else RED)
    line, yy = '', y + 88
    for ch in s:
        if dr.textlength(line + ch, font=font(29)) > 1290: dr.text((50, yy), line, font=font(29), fill=INK); yy += 42; line = ch
        else: line += ch
    dr.text((50, yy), line, font=font(29), fill=INK)
save(titled(im, '按难度排一排：从易到难的臀肌训练（编者根据结果整理，数字为 %MVIC）'), 5)

# ---------- 照片 ----------
f26 = photo(26)
f27 = photo(27, 500); blur(f27, (170, 580, 300, 650), 10)
s1 = Image.new('RGB', (1200, max(f26.height, f27.height)), 'white'); s1.paste(f26, (0, 0)); s1.paste(f27, (900 + (300 - min(300, f27.width)) // 2, 0))
f27s = f27.resize((300, round(f27.height * 300 / f27.width)), Image.LANCZOS)
s1 = Image.new('RGB', (1200, max(f26.height, f27s.height)), 'white'); s1.paste(f26, (0, 0)); s1.paste(f27s, (900, 0))
dr = ImageDraw.Draw(s1)
dr.text((10, s1.height - 46), '最大等长收缩测试（绑带固定）', font=font(28), fill='white', stroke_width=3, stroke_fill=(0, 0, 0))
save(titled(s1, '原文图 1、2　最大等长收缩测试（左）与不稳定平台（右）'), 6)

clam = photo(60, 1200); dr = ImageDraw.Draw(clam); w, h = clam.size
for (x, y), t in [((10, 10), '蚌式 1'), ((w // 2 + 10, 10), '蚌式 2'), ((10, h // 2 + 10), '蚌式 3'), ((w // 2 + 10, h // 2 + 10), '蚌式 4')]:
    tw = dr.textlength(t, font=font(36)); dr.rounded_rectangle([x, y, x + tw + 24, y + 54], 8, fill='white'); dr.text((x + 12, y + 7), t, font=font(36), fill=TEAL)
B = 'brand'
COREX = [(165, 525, 290, 580), (750, 525, 875, 580)]
items1 = [(clam, '蚌式 4', '图 3：蚌式 1～4 进阶（数值为蚌式 4）')]
save(board([(clam, '蚌式 4', '图 3：蚌式 1→4 进阶，数值为第 4 级'), (photo(64, 1200), '侧卧外展', '图 5'),
            (photo(66, 1200), '骨盆下降', '图 4：站 5 cm 台边')], '侧卧与站立的臀中肌练习'), 7)
save(board([(photo(65, 1200), '侧桥外展（优势腿在上）', '图 6：在下一侧数值更高'), (photo(71, 1200), '平板支撑 + 伸髋', '图 7')],
           '高阶：侧桥外展与平板支撑伸髋'), 8)
save(board([(photo(70, 1200), '单腿桥（稳定面）', '图 8'), (photo(76, 1200, [(25, 255, 190, 320), (625, 285, 800, 350)]), '单腿桥（不稳定面）', '图 9'),
            (photo(93, 1200), '四点跪伸髋（优势腿动）', '图 17')], '桥与四点跪'), 9)
save(board([(photo(80, 700), '单腿蹲', '图 12：坐到 47 cm 椅子'), (photo(81, 700), '单腿硬拉', '图 13'), (photo(91, 700), '滑冰者蹲', '图 18')],
           '单腿负重：单腿蹲、单腿硬拉、滑冰者蹲'), 10)
save(board([(photo(87, 700), '向前上台阶', '图 15：20 cm 台阶'), (photo(92, 700), '侧向上台阶', '图 16：15 cm 台阶'),
            (photo(86, 1200), '动态摆腿', '图 14')], '上台阶与摆腿'), 11)
save(board([(photo(75, 1200), '画圈（稳定面）', '图 10：单腿蹲同时脚尖画弧'), (photo(82, 1200, COREX), '画圈（不稳定面）', '图 11')],
           '单腿蹲 + 对侧脚画圈'), 12)

# 封面
c = photo(65, 900); top = max(0, (c.height - 383) // 2); c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
