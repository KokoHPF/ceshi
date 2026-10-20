#!/usr/bin/env python3
"""Buckthorpe 等 2019 ACL 重建术后恢复伸膝力量：首图中文标题卡；原文图 1 周期化曲线按原图估读中文重绘；
六阶段方案卡、髌股关节安全角度示意、术后早期“去抑制”工具箱为编者根据原文绘制。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
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


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床述评 · 《国际运动物理治疗杂志》2019', font=font(32), fill=TEAL)
for i, t in enumerate(['ACL 重建术后，', '怎么把股四头肌力量练回来？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '先“去抑制”，再周期化力量训练：术前 + 术后 5 个阶段', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Buckthorpe M, La Rosa G, Della Villa F. IJSPT 2019;14(1):159-172', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1：周期化曲线重绘（按原图估读）
wk = np.arange(1, 25)
vol = np.interp(wk, [1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                [10, 20, 28, 45, 65, 80, 87, 94, 96, 93, 90, 86, 83, 78, 70, 65, 62, 58, 54, 50, 48, 46])
inten = np.interp(wk, [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24],
                  [10, 20, 25, 35, 40, 46, 52, 60, 68, 72, 75, 80, 85, 86, 87, 88, 89, 91, 92, 93, 93])
from scipy.interpolate import make_interp_spline
xs = np.linspace(1, 24, 300)
fig, ax = plt.subplots(figsize=(12, 7), dpi=110)
ax.plot(xs, make_interp_spline(wk, vol, k=2)(xs), color='#9aa0a6', lw=5, label='训练量')
ax.plot(xs, make_interp_spline(wk, inten, k=2)(xs), color='#c0392b', lw=3.5, ls='--', label='训练强度')
cols = ['#eef3f7', '#fdf2e6', '#eaf4ea', '#fbeaea', '#eeeaf6']
for (a, b2, t), c in zip([(1, 4, '术后恢复'), (4, 8, '肌耐力'), (8, 12, '增肌'), (12, 18, '最大力量'), (18, 24, '爆发力')], cols):
    ax.axvspan(a, b2, color=c, zorder=0); ax.text((a + b2) / 2, 103, t, ha='center', fontsize=16, fontweight='bold')
ax.set_xlim(1, 24); ax.set_ylim(0, 110); ax.set_xticks(range(1, 25, 2))
ax.set_xlabel('术后周数', fontsize=16); ax.set_ylabel('相对百分比（%）', fontsize=16); ax.tick_params(labelsize=13)
ax.spines[['top', 'right']].set_visible(False); ax.legend(fontsize=15, frameon=False, loc='lower right')
fig.text(0.5, 0.01, '以术后约 6 个月重返运动为例；曲线为编者按原图估读重绘', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.03, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '图 1　术后周期化力量训练：量先升后降，强度一路上升', 1320), 2)

# 六阶段方案卡
W = 1200
st = [('0', '术前约 6 周', '把力量练到健侧 90% 以内', '孤立 + 功能性抗阻，低强度加血流限制；伸膝、腿举、深蹲、硬拉', (240, 240, 240)),
      ('1', '术后 0～4 周', '消痛消肿、解除抑制、少掉肌肉', '患侧：等长收缩 + 电刺激；健侧：照常大重量练', LT),
      ('2', '5～8 周', '肌耐力（兼顾增肌）', '低至中负荷孤立训练 12～20RM；开链 + 闭链；练好髌骨轨迹和股内斜肌', OR),
      ('3', '9～12 周', '增肌，伸膝力量差距缩到 20% 以内', '中高训练量 6～10 组 × 8～12RM；如伸膝 3 组 + 腿举 6 组，配血流限制或电刺激', GR),
      ('4', '13～18 周', '力量差距缩到 10% 以内', '孤立 5～10RM + 功能性 6～12RM；深蹲、硬拉、单腿；开始跑步、落地减速', PK),
      ('5', '19～24 周+', '爆发力和快速发力', '大负荷功能性 3～8RM、增强式、负重跳、奥举、场上训练', (234, 230, 246))]
im = Image.new('RGB', (W, 6 * 205 + 10), 'white'); dr = ImageDraw.Draw(im); y = 10
for n, wks, goal, how, bg in st:
    dr.rounded_rectangle([20, y, W - 20, y + 190], 14, fill=bg)
    dr.ellipse([40, y + 22, 110, y + 92], fill=TEAL); ctext(dr, 75, y + 36, n, font(40), 'white')
    dr.text((135, y + 20), wks, font=font(34), fill=TEAL); dr.text((135, y + 68), goal, font=font(30), fill=INK)
    para(dr, 135, y + 114, how, 26, W - 190, fill=GREY, gap=10); y += 205
save(titled(im, '一术前 + 五阶段：伸膝力量训练怎么排（编者根据原文表 1 整理）'), 3)

# 髌股关节安全角度示意
W = 1200; im = Image.new('RGB', (W, 760), 'white'); dr = ImageDraw.Draw(im)
X0, X1 = 120, 1100; px = lambda d: X0 + (X1 - X0) * d / 120
rows = [('开链：坐姿伸膝等', 40, 90, (76, 143, 191), '越接近伸直，髌股压力越大 → 先只在屈膝 90°～40° 之间做'),
        ('闭链：腿举、弓步等', 0, 80, (243, 154, 43), '越接近深屈，髌股压力越大 → 先只在屈膝 0°～80° 之间做')]
y = 40
for t, lo, hi, c, note in rows:
    dr.text((X0, y), t, font=font(36), fill=INK)
    dr.rounded_rectangle([X0, y + 70, X1, y + 130], 10, fill=(235, 235, 235))
    dr.rounded_rectangle([px(lo), y + 70, px(hi), y + 130], 10, fill=c)
    ctext(dr, (px(lo) + px(hi)) / 2, y + 84, f'{lo}°～{hi}°', font(30), 'white')
    for d in range(0, 121, 20):
        dr.line([px(d), y + 132, px(d), y + 146], fill=GREY, width=2); ctext(dr, px(d), y + 150, f'{d}°', font(24), GREY)
    para(dr, X0, y + 196, note, 28, X1 - X0, fill=GREY); y += 300
dr.text((X0, y - 10), '0° = 膝伸直。两段合起来覆盖全范围，髌股压力更小；', font=font(26), fill=GREY)
dr.text((X0, y + 30), '一般术后约 4 周开始，先求控制、再加负荷。', font=font(26), fill=GREY)
save(titled(im, '开链、闭链先练哪段角度（编者根据原文绘制）'), 4)

# 去抑制、助激活工具箱
W = 1200; tools = [('冰敷', '降低关节源性肌肉抑制，效果在撤冰后还能维持一段时间，适合练前做'),
                   ('经皮神经电刺激', '减少突触前抑制；30 分钟可逆转关节积液造成的抑制，但关机后就回落，最好边刺激边练'),
                   ('神经肌肉电刺激', '直接激活被抑制的运动单位；在常规康复之外加用，术后早期股四头肌力量和功能更好'),
                   ('血流限制训练', '低负荷也能长力量、长肌肉；适合负荷受限、做伸膝会痛的人，可在周期中穿插使用'),
                   ('局部麻醉', '通过止痛减轻抑制；但抑制在不痛时也会存在，不能只盯着止痛'),
                   ('监测痛和肿', '每次记录疼痛评分；每天在髌骨处量膝围，变化超过 1 cm 有临床意义')]
im = Image.new('RGB', (W, len(tools) * 150 + 10), 'white'); dr = ImageDraw.Draw(im); y = 10
for i, (h, t) in enumerate(tools):
    dr.rounded_rectangle([20, y, W - 20, y + 138], 12, fill=[LT, OR, GR, PK, (240, 240, 240), (234, 230, 246)][i])
    dr.text((44, y + 16), h, font=font(32), fill=TEAL); para(dr, 44, y + 64, t, 27, W - 110, fill=INK, gap=10); y += 150
save(titled(im, '术后早期：先“去抑制”，再谈练力量（编者根据原文整理）'), 5)

# 封面 900×383：标题卡式
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), 'ACL 重建术后', font=font(40), fill=TEAL)
dr.text((50, 130), '股四头肌力量', font=font(64), fill=INK)
dr.text((50, 220), '怎么练回来？', font=font(64), fill=INK)
dr.text((50, 318), '去抑制 + 周期化 · 一术前五阶段', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
