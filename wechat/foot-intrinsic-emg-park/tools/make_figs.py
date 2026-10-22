#!/usr/bin/env python3
"""Park & Hwang 2020 治疗性与三维足踝运动中足内在肌肌电比较：首图中文标题卡；原文图 1 流程图中文重绘；图 2 英文标注按 OCR 定位改为中文；
图 3～6 照片直接使用（只有 A、B 字母）；图 7、8 柱状图按原文表 2 数据和原图显著性标记用中文重绘。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys, os
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


def card(W, title, blocks, bg=(246, 248, 250)):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


up = lambda im, w=1000: im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def lab(im, page_bbox, items, fs=30, pad=6):
    """items: (页面 x, 页面 y, 中文, 颜色)；按 PDF 坐标映射到图像，白底写字"""
    x0, y0, x1, y1 = page_bbox; s = im.width / (x1 - x0); dr = ImageDraw.Draw(im)
    for x, y, t, *c in items:
        X, Y = (x - x0) * s, (y - y0) * s; f = font(fs)
        lines = t.split('\n'); w = max(dr.textlength(l, font=f) for l in lines); h = fs * 1.2 * len(lines)
        dr.rounded_rectangle([X - pad, Y - pad, X + w + pad, Y + h + pad], 6, fill=(255, 255, 255))
        for i, l in enumerate(lines): dr.text((X, Y + i * fs * 1.2), l, font=f, fill=c[0] if c else INK)
    return im


def row(ims, W=1200, gap=12):
    h = min(i.height for i in ims); ims = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in ims]
    tw = sum(i.width for i in ims) + gap * (len(ims) - 1); s = W / tw
    ims = [i.resize((round(i.width * s), round(h * s)), Image.LANCZOS) for i in ims]
    out = Image.new('RGB', (W, ims[0].height), 'white'); x = 0
    for i in ims: out.paste(i, (x, 0)); x += i.width + round(gap * s)
    return out


def stack(ims, gap=14):
    W = max(i.width for i in ims); out = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: out.paste(i, (0, y)); y += i.height + gap
    return out


import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0, HERE)
SRC = _os.path.join(HERE, '..', 'src')
import zh

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 45), '解释性研究 · 《国际环境研究与公共卫生杂志》2020', font=font(32), fill=TEAL)
dr.text((70, 115), '健康成人治疗性足踝运动与三维足踝运动中', font=font(50), fill=INK)
dr.text((70, 185), '足内在肌活动的比较：一项解释性研究', font=font(50), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Park DJ, Hwang YI.', font=font(28), fill=GREY)
dr.text((70, 375), 'Int J Environ Res Public Health. 2020;17(19):7189', font=font(28), fill=GREY)
dr.text((70, 440), '编者中文重排，仅作学术交流（原文 CC BY 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1 流程图（中文重绘）
im = Image.new('RGB', (1200, 640), 'white'); dr = ImageDraw.Draw(im)


def bx(b, lines, fs=26):
    dr.rectangle(b, outline=INK, width=2); y = (b[1] + b[3]) / 2 - len(lines) * fs * 1.35 / 2
    for k, l in enumerate(lines):
        f = font(fs if k == 0 else fs - 4); dr.text(((b[0] + b[2]) / 2 - dr.textlength(l, font=f) / 2, y), l, font=f, fill=INK); y += fs * 1.35


def ar(x0, y0, x1, y1):
    dr.line([x0, y0, x1, y1], fill=INK, width=2)
    if x0 == x1: dr.polygon([(x1, y1), (x1 - 7, y1 - 13), (x1 + 7, y1 - 13)], fill=INK)
    else: dr.polygon([(x1, y1), (x1 - 13, y1 - 7), (x1 - 13, y1 + 7)], fill=INK)


bx((40, 20, 520, 90), ['评估是否符合条件（n=19）'])
bx((640, 100, 1160, 210), ['排除（n=2）', '足部畸形（n=1）', '足踝活动度受限（n=1）'])
ar(280, 90, 280, 250); ar(280, 155, 640, 155)
bx((40, 250, 520, 340), ['随机分配（n=17）', '测试足内在肌最大自主等长收缩'])
ar(280, 340, 280, 430); ar(280, 385, 640, 385)
bx((640, 345, 1160, 425), ['退出（n=1）', '肌肉疲劳和痉挛（n=1）'])
bx((40, 430, 820, 520), ['随机分配（n=16）', '采集短足、脚趾张开、三维足踝运动中的肌电数据'])
ar(280, 520, 280, 550); bx((40, 550, 520, 630), ['数据分析', '单因素重复测量方差分析'])
save(capbox(im, '原文图 1（编者中文重绘）  研究流程'), 2)

f2, _ = zh.apply(raw(131), f'{SRC}/o131.json', [('abductorhallucis', '拇展肌', {'al': 'l', 'fg': INK}), ('flexor hallucis brevis', '拇短屈肌', {'al': 'l', 'fg': INK}),
                                                ('EMGcable', '肌电导线', {'fg': (200, 30, 30)})], W=1200)
save(capbox(f2, '原文图 2  自制肌电足板：(A) 俯视，(B) 仰视。板条可移动，在足底电极处留出空位，减少足底与支撑面接触造成的肌电干扰。B 图标注的是拇展肌和拇短屈肌'), 3)
save(capbox(raw(181), '原文图 3  短足运动：(A) 开始，(B) 结束。足底垫毛巾提供感觉反馈'), 4)
save(capbox(raw(182), '原文图 4  脚趾张开运动：(A) 开始，(B) 结束'), 5)
save(capbox(raw(237), '原文图 5  D1 模式：(A) 跖屈—旋前—外翻加屈趾，(B) 背伸—旋后—内翻加伸趾'), 6)
save(capbox(raw(236), '原文图 6  D2 模式：(A) 跖屈—旋后—内翻加屈趾，(B) 背伸—旋前—外翻加伸趾'), 7)

EX = ['SF', 'TSO', 'D1F', 'D1E', 'D2F', 'D2E']
COL = ['#d9d9d9', '#c4b97a', '#f4a6a6', '#f7c08a', '#f2f2a6', '#9be79b']
D = {'拇展肌': ([65.06, 80.84, 61.41, 76.48, 51.00, 78.97], [28.01, 26.33, 21.33, 30.40, 17.20, 22.00], [(1, 4), (3, 4), (4, 5)]),
     '拇长伸肌': ([49.16, 52.92, 68.14, 53.75, 73.19, 49.35], [16.44, 19.37, 19.37, 14.22, 22.83, 11.56], [(1, 2), (2, 3), (2, 5), (0, 4), (1, 4), (3, 4), (4, 5)]),
     '拇短屈肌': ([95.96, 90.09, 84.58, 105.14, 72.28, 97.23], [19.54, 19.40, 31.35, 35.15, 19.35, 27.97], [(0, 4), (3, 4), (4, 5)]),
     '拇展肌 / 拇收肌比值': ([0.70, 0.92, 0.71, 0.81, 0.58, 0.85], [0.28, 0.29, 0.23, 0.29, 0.22, 0.22], [(1, 4), (4, 5)])}


def chart(names, n):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5.2), dpi=100)
    for a, nm in zip(axs, names):
        m, sd, sig = D[nm]; x = np.arange(6)
        a.bar(x, m, 0.65, color=COL, edgecolor='#333', yerr=[[0] * 6, sd], capsize=4, error_kw={'elinewidth': 1})
        a.set_xticks(x); a.set_xticklabels(EX, fontsize=12); a.set_title(nm, fontsize=15)
        a.set_ylabel('比值' if '比值' in nm else '%MVIC', fontsize=12); a.spines[['top', 'right']].set_visible(False)
        top = max(mm + ss for mm, ss in zip(m, sd)); step = top * 0.07; y = top + step * 0.6
        for i, j in sorted(sig, key=lambda p: p[1] - p[0]):
            a.plot([i, i, j, j], [y - step * 0.25, y, y, y - step * 0.25], color='#333', lw=1); a.text((i + j) / 2, y, '*', ha='center', va='bottom', fontsize=13); y += step
        a.set_ylim(0, y + step * 0.5)
    fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
    return Image.open(buf).convert('RGB')


save(capbox(chart(['拇展肌', '拇长伸肌'], 7), '原文图 7（编者中文重绘）  各运动中拇展肌和拇长伸肌的激活。柱为均值，误差线为标准差，* P &lt; 0.05'.replace('&lt;', '<')), 8)
save(capbox(chart(['拇短屈肌', '拇展肌 / 拇收肌比值'], 8), '原文图 8（编者中文重绘）  各运动中拇短屈肌激活和拇展肌 / 拇收肌比值，* P < 0.05。SF：短足；TSO：脚趾张开；D1F / D1E：D1 屈曲 / 伸展；D2F / D2E：D2 屈曲 / 伸展'), 9)

c = raw(182); k = 900 / c.width; c = c.resize((900, round(c.height * k)), Image.LANCZOS)
y0 = round(c.height * 0.45); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
