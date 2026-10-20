#!/usr/bin/env python3
"""van den Tillaar 等 2017 冲刺跑与 7 种腘绳肌训练的肌电比较：首图中文标题卡；原文图 1（负片存储，先反相）按动作分组拼板、
字母改为中文；图 2 按原图估读数值中文重绘；图 3 顶部英文动作名改为中文。
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


from PIL import ImageOps

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '原始研究 · 《国际运动物理治疗杂志》2017', font=font(32), fill=TEAL)
dr.text((70, 150), '高速跑与多种腘绳肌强化训练中', font=font(58), fill=INK)
dr.text((70, 232), '腘绳肌激活的比较', font=font(58), fill=INK)
dr.text((70, 330), '12 名男性：冲刺跑 vs 7 个腘绳肌动作，表面肌电 + 三维动作捕捉', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'van den Tillaar R, Solheim JAB, Bencke J. IJSPT 2017;12(5):718-727', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1：反相后按行切分，去掉字母，按动作分组
f1 = ImageOps.invert(raw(10))
ROWS = [(0, 314), (330, 631), (646, 962), (974, 1290), (1305, 1626), (1639, 1953), (1967, 2282)]
NAME = ['① 仰卧踢腿', '② 站立踢腿', '③ 北欧挺', '④ 北欧挺 + 回起', '⑤ 北欧挺 + 推拉', '⑥ 鹤式', '⑦ 鹤式 + 回起']
DESC = ['仰卧，双肩、臀部和右脚跟着地；左腿猛地向上踢，带动右脚离地，再落回地面',
        '左腿单腿站立，右膝抬起后，右脚快速向前踢出',
        '双脚被绑带固定，髋和背挺直向前倒，撑不住时松开，用双手做离心俯卧撑缓冲',
        '同北欧挺，向前倒到撑不住之前，再用腘绳肌把身体拉回直立',
        '向前倒到能控制的极限，在该位置把 5 kg 重物尽快向前推出、再拉回',
        '先屈髋到 90°，躯干保持水平，再伸膝向前倒，撑不住时用双手离心缓冲',
        '同鹤式，伸膝向前倒到撑不住之前，再拉回起始位置']


def strip(i, W=1200):
    r = f1.crop((0, ROWS[i][0], f1.width, ROWS[i][1]))
    r.paste(r.crop((0, 0, 60, 60)).filter(ImageFilter.GaussianBlur(12)), (0, 0))
    r = r.resize((W, round(r.height * W / r.width)), Image.LANCZOS)
    tmp = ImageDraw.Draw(Image.new('RGB', (1, 1))); lines = 1; line = ''
    for ch in DESC[i]:
        if tmp.textlength(line + ch, font=font(26)) > W - 40: lines += 1; line = ch
        else: line += ch
    th = 60 + 36 * lines
    out = Image.new('RGB', (W, r.height + th), 'white'); d = ImageDraw.Draw(out)
    d.text((10, 8), NAME[i], font=font(32), fill=RED); para(d, 10, 52, DESC[i], 26, W - 40, fill=GREY)
    out.paste(r, (0, th)); return out


save(board([strip(0), strip(1)], '原文图 1：踢腿类（箭头为发力方向）'), 2)
save(board([strip(2), strip(3), strip(4)], '原文图 1：北欧挺及其变式'), 3)
save(board([strip(5), strip(6)], '原文图 1：鹤式及其变式'), 4)

# 图 2：按原图估读重绘
EX = ['冲刺跑', '仰卧踢腿', '站立踢腿', '北欧挺', '北欧挺\n+回起', '北欧挺\n+推拉', '鹤式', '鹤式\n+回起']
DATA = [('半腱肌', [100, 56, 51, 66, 64, 56, 45, 48], [0, 27, 24, 28, 30, 28, 24, 27], '#4c8fbf'),
        ('股二头肌', [100, 35, 19, 36, 38, 37, 21, 19], [0, 21, 10, 26, 26, 28, 19, 17], '#f39a2b'),
        ('半膜肌', [100, 77, 41, 66, 70, 63, 47, 43], [0, 40, 18, 30, 35, 26, 18, 20], '#6aa96a')]
fig, ax = plt.subplots(figsize=(13, 6.4), dpi=110)
x = np.arange(8); w = 0.27
for j, (k, m, s, c) in enumerate(DATA):
    ax.bar(x + (j - 1) * w, m, w, yerr=s, color=c, edgecolor='#333', capsize=3, label=k, error_kw={'lw': 1})
    for xi, mi in zip(x + (j - 1) * w, m):
        if mi < 100: ax.text(xi, 3, str(mi), ha='center', fontsize=10.5, color='white', fontweight='bold')
ax.axhline(70, color='#c0392b', ls='--', lw=1.4); ax.text(7.55, 72, '70%', color='#c0392b', fontsize=13, ha='right')
ax.set_xticks(x); ax.set_xticklabels(EX, fontsize=14); ax.set_ylabel('肌电峰值（冲刺跑 = 100%）', fontsize=15)
ax.set_ylim(0, 125); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=13)
ax.legend(fontsize=14, frameon=False, ncol=3, loc='upper right')
fig.text(0.5, 0.01, '柱高为均值，误差线为标准差；数值为编者按原文柱状图估读，非原文精确值。红色虚线：常用的“力量训练刺激”参考线', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.04, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '原文图 2 重绘：各动作的腘绳肌激活（相对冲刺跑）', 1320), 5)

# 图 3：顶部英文动作名改为中文
f3 = raw(26); ImageDraw.Draw(f3).rectangle([0, 0, f3.width, 40], fill='white')
g = Image.new('RGB', (f3.width, f3.height + 30), 'white'); g.paste(f3, (0, 30)); f3 = g
CX = [95, 273, 461, 700, 907, 1093, 1253, 1455]
LB = ['鹤式+回起', '鹤式', '仰卧踢腿', '北欧挺+推拉', '北欧挺+回起', '北欧挺', '冲刺跑', '站立踢腿']
d3 = ImageDraw.Draw(f3)
for cx, t in zip(CX, LB):
    ctext(d3, max(cx, 80), 10, t, font(32))
save(titled(f3, '原文图 3：肌电峰值出现时的髋、膝角度（三块肌肉平均）', 1200), 6)

# 封面 900×383：北欧挺 + 回起的中间三帧
h = ROWS[3][1] - ROWS[3][0]; w = round(h * 900 / 383); c = f1.crop((350, ROWS[3][0], 350 + w, ROWS[3][1]))
c.resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
