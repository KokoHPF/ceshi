#!/usr/bin/env python3
"""Sezerel & Yüksel 2024 颈椎病：肌肉能量技术 vs 颈椎关节松动：首图中文标题卡；三组方案卡、肌肉能量技术步骤卡、
结果图为编者绘制；原文图 1、2 按页面渲染并加中文标注。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
CLIP = {1: (2, (51, 91, 516, 537)), 2: (3, (51, 92, 516, 704))}


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def fig(n, W):
    pg, r = CLIP[n]
    pix = doc[pg].get_pixmap(dpi=300, clip=pymupdf.Rect(*r))
    im = Image.open(BytesIO(pix.tobytes('png'))).convert('RGB')
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200, maxh=1500):
    im = fig(n, W)
    if im.height > maxh: im = im.resize((round(im.width * maxh / im.height), maxh), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in f'图 {n}　{cap}':
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, ((W - im.width) // 2, hh + 8)); return t


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '随机对照试验 · 《医学科学监测》2024', font=font(32), fill=TEAL)
for i, t in enumerate(['颈椎病颈痛：肌肉能量技术', '还是关节松动？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '止痛差不多，位置觉肌肉能量技术更好 · 76 人 4 周', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Sezerel B, Yüksel İ. Med Sci Monit 2024;30:e945149', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 三组 ----------
W = 1400; im = Image.new('RGB', (W, 660), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 220], 16, fill=(240, 240, 240))
dr.text((50, 36), '三组都做：理疗（每周 3 次 × 4 周，共 12 次）', font=font(34), fill=GREY)
for i, t in enumerate(['热敷斜方肌和枕下肌群 20 分钟', '调制经皮神经电刺激 20 分钟（80 赫兹）', '连续超声 10 分钟（1 兆赫，1.5 瓦/平方厘米）']):
    dr.text((60, 96 + i * 40), '· ' + t, font=font(28), fill=INK)
for k, (t, c, tc, items) in enumerate([('理疗组', (245, 245, 245), GREY, ['只做理疗', '（对照）']),
                                       ('理疗 + 肌肉能量技术', OR, RED, ['上斜方肌、胸锁乳突肌、', '斜角肌（前中后）、肩胛提肌', '双侧，各 3 次']),
                                       ('理疗 + 关节松动', LT, TEAL, ['先深部横向摩擦 3～4 分钟', '再做 5 种仰卧位被动松动', '（Cyriax 法）'])]):
    x = 20 + k * 460
    dr.rounded_rectangle([x, 250, x + 440, 640], 16, fill=c)
    ctext(dr, x + 220, 270, t, font(32), tc)
    for i, it in enumerate(items): ctext(dr, x + 220, 360 + i * 56, it, font(28), INK)
save(titled(im, '三组怎么分'), 2)

# ---------- 肌肉能量技术步骤 ----------
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
steps = [('定力度', '先用压力生物反馈仪测这块肌肉的最大等长力量，算出 20%；反馈仪充气到 20 毫米汞柱，垫在头部对应方向'),
         ('找位置', '按 Lewit 推荐的体位，把肌肉带到刚感到受限的位置'),
         ('吸气发力', '病人深吸一口气后屏住，向治疗师的阻力方向等长用力 7 秒，力度约最大的 20%（看反馈仪压力），同时睁眼看用力方向'),
         ('呼气放松', '放松、闭眼、呼气；治疗师顺势把头颈被动带到新的受限点'),
         ('重复', '在新位置重复，每块肌肉 3 次，两侧都做')]
for i, (a, t) in enumerate(steps):
    y = 30 + i * 180
    dr.rounded_rectangle([30, y, W - 30, y + 160], 14, fill=OR if i % 2 == 0 else LT)
    dr.ellipse([50, y + 40, 130, y + 120], fill=RED); ctext(dr, 90, y + 56, str(i + 1), font(40), 'white')
    dr.text((160, y + 18), a, font=font(34), fill=TEAL); para(dr, 160, y + 66, t, 28, 1180, INK, 8)
save(titled(im, '肌肉能量技术（Lewit 等长收缩后放松）怎么做'), 3)

save(titled(tile(1, '肌肉能量技术：A 上斜方肌（左）；B 胸锁乳突肌（右）；C 肩胛提肌（左）；D 前斜角肌（左）；E 中斜角肌（左）；F 后斜角肌（左）。头下垫的是压力生物反馈仪'), '肌肉能量技术的 6 个部位'), 4)
save(titled(tile(2, '颈椎关节松动：A 徒手牵引；B1、B2 “架桥”；C 侧向滑动；D1、D2 牵引下旋转；E1、E2 牵引下前后滑动'), '颈椎关节松动的 5 种手法'), 5)

# ---------- 结果 ----------
fig_, axs = plt.subplots(1, 3, figsize=(13, 4.6), dpi=110)
cols = ['#888888', '#c0504d', '#2f8fa0']; names = ['理疗', '理疗+肌肉能量', '理疗+关节松动']
data = [('活动时疼痛（0～10 厘米）', [(6.26, 3.10), (6.84, 3.74), (6.74, 4.31)], '组间 P=0.176'),
        ('哥本哈根颈部功能障碍（0～30）', [(12.92, 6.80), (14.44, 7.08), (14.50, 8.62)], '组间 P=0.441'),
        ('后伸位置误差（°）', [(2.99, 3.14), (2.64, 1.42), (2.88, 2.15)], '组间 P<0.001')]
for ax, (t, ds, note) in zip(axs, data):
    for (a, b), c, nm in zip(ds, cols, names): ax.plot([0, 1], [a, b], '-o', color=c, lw=3, ms=8, label=nm)
    ax.set_xticks([0, 1]); ax.set_xticklabels(['治疗前', '4 周后'], fontsize=13); ax.set_title(t, fontsize=14); ax.set_xlim(-0.3, 1.3)
    ax.text(0.5, 0.92, note, transform=ax.transAxes, ha='center', fontsize=13, color='#c0504d' if '<' in note else '#555555')
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
axs[0].legend(fontsize=11, frameon=False, loc='lower left')
plt.tight_layout(); buf = BytesIO(); fig_.savefig(buf, format='png'); plt.close(fig_)
save(titled(Image.open(buf), '主要结果：疼痛和功能三组一样，后伸位置觉肌肉能量组更好', 1320), 6)

# ---------- 效应量 ----------
fig_, ax = plt.subplots(figsize=(12, 5), dpi=110)
dirs = ['右-中立', '左-中立', '前屈', '后伸', '右旋', '左旋', '右侧屈', '左侧屈']
d = {'理疗': [0.03, 0.14, 0.31, 0.08, 0.20, 0.20, 0.30, 0.25], '理疗+肌肉能量': [0.41, 0.55, 0.81, 0.89, 0.53, 1.02, 0.62, 0.75], '理疗+关节松动': [0.22, 0.21, 0.28, 0.43, 0.16, 0.06, 0.14, 0.40]}
import numpy as np
x = np.arange(len(dirs)); w = 0.26
for k, (nm, c) in enumerate(zip(d, cols)): ax.bar(x + (k - 1) * w, d[nm], w, color=c, label=nm)
ax.axhline(0.8, ls='--', color='#999999', lw=1); ax.text(7.45, 0.82, '大效应 0.8', fontsize=11, color='#777777', ha='right')
ax.axhline(0.5, ls=':', color='#bbbbbb', lw=1); ax.text(7.45, 0.52, '中效应 0.5', fontsize=11, color='#999999', ha='right')
ax.set_xticks(x); ax.set_xticklabels(dirs, fontsize=13); ax.set_ylabel('组内效应量（科恩 d）', fontsize=13)
for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
ax.legend(fontsize=12, frameon=False, loc='upper left')
plt.tight_layout(); buf = BytesIO(); fig_.savefig(buf, format='png'); plt.close(fig_)
save(titled(Image.open(buf), '颈部位置误差：各方向组内改善幅度', 1320), 7)

c = fig(1, 900); c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
