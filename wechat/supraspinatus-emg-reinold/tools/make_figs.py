#!/usr/bin/env python3
"""Reinold 等 2007 冈上肌与三角肌肌电分析：首图中文标题卡；原文图 1～3 三个练习照片（模糊背景球衣名字和衣服品牌）；
原文图 4～5 力向量示意图（原图为负片，反相后字母标注改为中文）；结果柱状图按原文表格数值重绘；练习方法卡为编者绘制。
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
dr.text((70, 60), '肌电研究 · 《运动防护杂志》2007', font=font(32), fill=TEAL)
for i, t in enumerate(['练冈上肌：满罐、空罐、', '俯卧满罐，哪个最合适？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '22 名健康人，针电极同时记录冈上肌、三角肌中束和后束', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Reinold MM, et al. J Athl Train 2007;42(4):464-469', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1、2：满罐 vs 空罐并排；模糊背景球衣名字和衣服品牌
f1 = blur(raw(7), [(50, 120, 390, 410), (590, 145, 890, 410), (370, 355, 530, 430)], 12)
f2 = blur(raw(8), [(75, 85, 440, 380), (620, 125, 925, 395), (410, 335, 580, 405)], 12)


def pair(a, b, la, lb, W=1200, gap=12):
    w = (W - gap) // 2; a = a.resize((w, round(a.height * w / a.width)), Image.LANCZOS); b = b.resize((w, round(b.height * w / b.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, a.height + 60), 'white'); d = ImageDraw.Draw(out)
    out.paste(a, (0, 0)); out.paste(b, (w + gap, 0))
    ctext(d, w / 2, a.height + 12, la, font(30)); ctext(d, w + gap + w / 2, a.height + 12, lb, font(30))
    return out


save(titled(pair(f1, f2, '图 1　满罐：拇指朝上（外旋）', '图 2　空罐：拇指朝下（内旋）'), '满罐 vs 空罐：肩胛平面上举到 90°'), 2)

# 图 3：俯卧满罐，裁成横幅
f3 = blur(raw(12), [(0, 0, 480, 85), (700, 0, 1000, 85)], 12)
f3 = f3.crop((0, 180, f3.width, 180 + round(f3.width * .75)))
save(titled(f3, '图 3　俯卧满罐：俯卧位，约 100° 外展 + 外旋', 1200), 3)

# 练习方法卡
W = 1200; im = Image.new('RGB', (W, 920), 'white'); dr = ImageDraw.Draw(im)
cards = [('满罐', '站立；手臂在肩胛平面（额状面前方 30°）从体侧上举到 90°；肩外旋、拇指朝上', OR, RED),
         ('空罐', '站立；同样在肩胛平面从体侧上举到 90°；肩内旋、拇指朝下（像把罐子倒空）', LT, TEAL),
         ('俯卧满罐', '俯卧在治疗床边，手臂垂下；在约 100° 外展位做水平外展，肩外旋、拇指朝上，举到末端、出现代偿就停', GR, (40, 120, 60))]
y = 10
for h, t, bg, col in cards:
    dr.rounded_rectangle([20, y, W - 20, y + 190], 14, fill=bg)
    dr.text((50, y + 22), h, font=font(36), fill=col); para(dr, 70, y + 84, t, 28, W - 120, gap=14); y += 205
dr.rounded_rectangle([20, y, W - 20, y + 290], 14, fill=(244, 244, 244))
dr.text((50, y + 22), '三个练习统一的做法', font=font(36), fill=INK); yy = y + 84
for t in ['哑铃：每人每个练习用 10RM 重量（平均约 1.5～1.9 kg）',
          '节拍器每分钟 60 拍：上举 1 拍、放下 1 拍',
          '每个练习做 5 次，取第 2～4 次分析；练习顺序随机，间隔休息 3～5 分钟']:
    yy = para(dr, 70, yy, '· ' + t, 30, W - 140, gap=16) + 6
save(titled(im, '三个练习怎么做（编者根据原文整理）'), 4)

# 结果柱状图（原文表格数值）
fig, ax = plt.subplots(figsize=(12, 6), dpi=110)
mus = ['冈上肌', '三角肌中束', '三角肌后束']
data = {'满罐': ([62, 52, 38], [40, 27, 32], '#f39a2b'), '空罐': ([63, 77, 54], [45, 44, 28], '#4c8fbf'), '俯卧满罐': ([67, 63, 87], [50, 31, 53], '#6aa96a')}
x = np.arange(3); w = 0.26
for j, (k, (m, s, c)) in enumerate(data.items()):
    xx = x + (j - 1) * w
    ax.bar(xx, m, w, yerr=s, color=c, edgecolor='#333', capsize=4, label=k, error_kw={'lw': 1.1})
    for xi, mi in zip(xx, m): ax.text(xi, 4, str(mi), ha='center', fontsize=13, color='white', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(['冈上肌\n（P = 0.807，无差别）', '三角肌中束\n（P = 0.029）', '三角肌后束\n（P = 0.001）'], fontsize=14)
ax.set_ylabel('肌电活动（% MVIC）', fontsize=15); ax.set_ylim(0, 150); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=13)
ax.legend(fontsize=14, frameon=False, ncol=3, loc='upper left')
fig.text(0.5, 0.01, '柱高为均值，误差线为标准差，数值取自原文表格。MVIC：最大自主等长收缩', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.04, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '主要结果：冈上肌三个练习差不多，三角肌差别大', 1320), 5)

# 图 4、5：力向量示意图（原图为负片，先反相），字母改为中文
from PIL import ImageOps


def rel_px(im, items):
    s = 1000 / im.width
    return relabel(im, [((x0 * s, y0 * s, x1 * s, y1 * s), t, fs * s) for (x0, y0, x1, y1), t, fs in items])


f4 = ImageOps.invert(raw(16))
f4 = rel_px(f4, [((218, 196, 264, 232), '内', 24), ((238, 236, 264, 266), '外', 24), ((176, 248, 204, 278), '中', 24),
                 ((552, 0, 606, 34), '内', 24), ((548, 76, 576, 106), '中', 24), ((588, 138, 616, 168), '外', 24),
                 ((966, 22, 994, 52), '内', 24), ((944, 94, 972, 124), '中', 24), ((990, 138, 1018, 168), '外', 24),
                 ((312, 510, 340, 540), '中', 24), ((272, 552, 300, 582), '外', 24), ((346, 548, 404, 590), '内', 24),
                 ((626, 560, 654, 590), '中', 24), ((600, 586, 636, 644), '外', 24), ((880, 570, 908, 600), '中', 24),
                 ((960, 670, 1000, 710), '', 20)])
save(titled(f4, '图 4　不同旋转位上举时盂肱关节的合力方向', 1200), 6)
f5 = ImageOps.invert(raw(17))
f5 = rel_px(f5, [((20, 298, 200, 363), 'A 三角肌', 28), ((405, 298, 585, 363), 'B 冈上肌', 28), ((778, 298, 1000, 363), 'C 两者合力', 28)])
save(titled(f5, '图 5　三角肌、冈上肌及两者合力的方向', 1200), 7)

# 封面 900×383：取俯卧满罐
c = blur(raw(12), [(0, 0, 480, 85), (700, 0, 1000, 85)], 12)
c = c.crop((0, 230, c.width, 230 + round(c.width * 383 / 900)))
c.resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
