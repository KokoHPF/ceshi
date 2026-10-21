#!/usr/bin/env python3
"""Wilk 等 2011 进阶投掷十项：首图中文标题卡；原文图 1～6 照片直接使用并加中文标签和图注；
“三段式序列”示意卡为编者根据原文整理。
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


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '临床专题 · 《医师与运动医学》2011', font=font(32), fill=TEAL)
dr.text((70, 125), '进阶投掷十项训练方案：', font=font(54), fill=INK)
dr.text((70, 205), '增强过头投掷运动员肩关节', font=font(54), fill=INK)
dr.text((70, 285), '动态控制的新训练系列', font=font(54), fill=INK)
dr.line([70, 385, W - 70, 385], fill=(200, 205, 210), width=2)
dr.text((70, 415), 'Wilk KE, Yenchak AJ, Arrigo CA, Andrews JR. Phys Sportsmed 2011;39(4):90-97', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


def tagged(x, t):
    im = raw(x); dr = ImageDraw.Draw(im); f = font(max(26, im.height // 20)); w = dr.textlength(t, font=f)
    dr.rounded_rectangle([12, 12, 36 + w, 26 + f.size], 10, fill=(255, 255, 255)); dr.text((24, 16), t, font=f, fill=INK); return im


blocks = [('第 1 段：双侧同时做', '两臂一起完成 10 次', LT, TEAL),
          ('第 2 段：一侧动、对侧保持', '患侧做 10 次等张动作，健侧手臂在抬高位持续等长保持（原文图注写法是两侧轮流各做一次）', OR, (200, 110, 30)),
          ('第 3 段：两臂交替', '一侧保持、另一侧动，交替进行共 10 次', GR, (40, 130, 60)),
          ('剂量', '三段连续做、中间不休息（约 30 次），整个序列做 2 遍；保持用的重量以全程无痛、不掉位为准；全程坐在瑜伽球上，坐骨着球、双脚与肩同宽、收腹，肩胛保持后倾、外旋、后缩', PK, RED)]
save(card(1200, '“三段式”序列怎么做（编者根据原文整理）', blocks), 2)
save(capbox(row([tagged(76, '图 1 球上弹力带外旋 + 徒手抗阻'), tagged(75, '图 2 球上满罐')]),
            '原文图 1（左）：坐在瑜伽球上用弹力带做外旋，治疗师叠加徒手阻力；患侧腋下夹毛巾卷，提示后缩、下沉肩胛。'
            '原文图 2（右）：球上满罐，躯干直立、肩胛后缩下沉，在肩胛面抬臂到 90°，按三段式序列完成'), 3)
save(capbox(row([tagged(83, '图 3 侧平板外旋')]), '原文图 3：侧平板位外旋。健侧前臂撑床、屈肘 90°，抬起骨盆、收紧腰盆部肌肉保持脊柱中立，'
                                                   '外旋 10 次或保持 10 秒；治疗师密切观察脊柱角度，留意疲劳'), 4)
save(capbox(row([tagged(81, '图 4 俯卧球上 T 字'), tagged(82, '图 5 俯卧球上 Y 字')]),
            '原文图 4（左）：俯卧球上水平外展（T 字），腹部压在球上、躯干与地面平行；原文图 5（右）：俯卧球上在肩胛面外展 105° 并充分外旋（Y 字）。都按三段式序列，共 30 次再做一遍'), 5)
save(capbox(row([tagged(89, '图 6 球上 W 字外旋')]), '原文图 6：瑜伽球上 W 字外旋。坐直，手臂外展 30°、屈肘、前臂中立；先双侧后缩下沉肩胛，再伸展并外旋手臂，向心末端成“W”字，共 30 次'), 6)

c = up(raw(75), 900); y0 = (c.height - 383) // 3; c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
