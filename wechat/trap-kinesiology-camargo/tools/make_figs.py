#!/usr/bin/env python3
"""Camargo、Neumann 2019 斜方肌运动学（第 2 部分）：首图中文标题卡；原文图 1、2 的英文标注（PDF 叠加文字层）按原位置改为中文，
图 3～13 照片直接使用并加中文图注。
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
dr.text((70, 50), '大师课 · 《巴西物理治疗杂志》2019', font=font(32), fill=TEAL)
dr.text((70, 130), '针对性激活肩胸肌群的运动学考量', font=font(54), fill=INK)
dr.text((70, 215), '第 2 部分：斜方肌', font=font(54), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 365), 'Camargo PR, Neumann DA. Braz J Phys Ther 2019;23(6):467-475', font=font(28), fill=GREY)
dr.text((70, 420), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1：右侧加留白放标签
f = raw(19); bb = (340, 56, 521, 414); s = f.width / (bb[2] - bb[0])
c = Image.new('RGB', (f.width + 120, f.height), 'white'); c.paste(f, (0, 0))
c = lab(c, (bb[0], bb[1], bb[0] + c.width / s, bb[1] + c.height / s),
        [(352, 126, '上斜方肌'), (470, 252, '下斜方肌'), (372, 222, '三角肌后束'), (440, 181, '中斜方肌')], fs=44)
save(capbox(up(c, 900), '原文图 1：斜方肌的三个部分（另画出三角肌后束），红色箭头为上斜方肌的作用线'), 2)

# 图 2
f = lab(raw(28), (83, 56, 504, 569), [
    (176, 492, '前锯肌', RED), (469, 226, '前锯肌', RED), (353, 507, '下斜方', RED), (343, 240, '下斜方', RED), (410, 499, '前锯肌', RED),
    (244, 421, '下 / 中斜方', RED), (258, 283, '上斜方', RED), (221, 132, '上斜方', RED),
    (84, 426, '肩胛骨\n外旋'), (237, 436, '肩胛骨\n外旋'), (172, 276, '锁骨\n后缩'), (169, 110, '锁骨\n上提'),
    (84, 399, 'C 上面观'), (84, 229, 'B 上面观'), (86, 64, 'A 前面观'), (378, 464, '肩胛骨\n后倾'), (330, 402, '肩胛骨\n后倾'),
    (406, 199, '肩胛骨\n上回旋'), (398, 63, 'D 后面观'), (317, 345, 'E 侧面观')], fs=34, pad=5)
save(capbox(f, '原文图 2：肩前屈时部分肩胸肌群的作用线（红色粗箭头）。A 锁骨上提；B 锁骨后缩；C 肩胛外旋；D 肩胛上回旋；E 肩胛后倾。'
               '实线为内力臂，虚线表示作用线与力臂成直角；两个旋转轴：胸锁关节轴（胸骨柄附近）和肩锁关节轴（肩峰附近）'), 3)

caps = [(51, '原文图 3：斜方肌徒手肌力测试。A 上斜方肌；B 中斜方肌；C 下斜方肌'),
        (70, '原文图 4：耸肩加后缩。双臂垂于体侧、肩后缩起始（A），耸肩（B）后还原'),
        (71, '原文图 5：过头耸肩。站立，双臂举过头贴墙（A），耸肩（B）后还原'),
        (97, '原文图 6：俯卧水平外展。俯卧，肩外展 90° 并外旋，做水平外展'),
        (98, '原文图 7：过头后缩。站立，双臂举过头贴墙（A），双臂抬离墙面（黑箭头）同时肩胛后缩（蓝箭头）（B），然后还原'),
        (110, '原文图 8：俯卧肩胛定位。俯卧，手臂过头放在床上（A）；把肩胛放在相对后缩、下沉的位置（黑箭头），保持住再把手臂稍抬离床面（B）；避免耸肩和上斜方肌用力'),
        (111, '原文图 9：外旋位上举。站立，屈肘 90°，双手拉弹力带外旋 30° 使其绷紧（A）；保持张力，在肩胛面把双臂上举到 90°（B）'),
        (112, '原文图 10：俯卧后伸。俯卧，手臂前屈 90°（A），在中立旋转位后伸到中立位（B）'),
        (113, '原文图 11：侧卧外旋。侧卧，肩中立、屈肘 90°（A），肘与躯干间夹毛巾做肩外旋（B）；避免代偿'),
        (121, '原文图 12：侧卧前屈。侧卧，手臂贴体侧（A），做前屈（B）'),
        (122, '原文图 13：俯卧 I、T、Y。俯卧，手臂垂于床边（A），肩胛后缩下沉，治疗师可用手给反馈；保持此位置，'
              '手臂沿躯干后伸（I，B）、水平外展（T，C）或上举约 120°（Y，D）；避免上斜方肌用力，黑箭头提示全程保持肩胛后缩和下沉')]
for n, (x, t) in enumerate(caps, start=4):
    im = raw(x); im = up(im, 1200) if im.width < 1200 or x != 97 else im
    if x == 97: im = up(raw(97), 800); p = Image.new('RGB', (1200, im.height), 'white'); p.paste(im, (200, 0)); im = p
    save(capbox(im, t), n)

c = up(raw(122), 900); c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
