#!/usr/bin/env python3
"""Olds & Uhl 2024 肩关节不稳的非手术治疗：首图中文标题卡；原文图 1、2、3、6（矢量英文流程图）按原图版式用中文重绘（坐标取自 110 dpi 页面渲染）；
原文图 4、5 和附录图 1、2 的插图直接使用，加中文图注；评分卡为编者根据原文整理。
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

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '当前临床概念 · 《运动防护杂志》2024', font=font(32), fill=TEAL)
dr.text((70, 135), '当前临床概念：', font=font(56), fill=INK)
dr.text((70, 215), '肩关节不稳的非手术治疗', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Olds M, Uhl TL.', font=font(28), fill=GREY)
dr.text((70, 405), 'J Athl Train. 2024;59(3):243-254', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


class Chart:
    """按页面渲染坐标（110 dpi）重绘流程图；x0..x1 为裁切范围，输出宽 Wout"""
    def __init__(s, x0, y0, x1, y1, Wout=1200):
        s.x0, s.y0, s.k = x0, y0, Wout / (x1 - x0)
        s.im = Image.new('RGB', (Wout, round((y1 - y0) * s.k)), 'white'); s.dr = ImageDraw.Draw(s.im)

    def p(s, x, y): return (round((x - s.x0) * s.k), round((y - s.y0) * s.k))

    def text(s, b, t, fmax=24, fill=INK, al='c'):
        (a, c), (e, f) = s.p(b[0], b[1]), s.p(b[2], b[3]); w, h = e - a - 10, f - c - 6
        for fs in range(fmax, 9, -1):
            ft = font(fs); lines = []
            for para_ in t.split('\n'):
                cur = ''
                for ch in para_:
                    if s.dr.textlength(cur + ch, font=ft) > w and cur: lines.append(cur); cur = ch
                    else: cur += ch
                lines.append(cur)
            if len(lines) * fs * 1.25 <= h: break
        y = (c + f) / 2 - len(lines) * fs * 1.25 / 2
        for l in lines:
            tw = s.dr.textlength(l, font=ft); x = (a + e) / 2 - tw / 2 if al == 'c' else a + 6
            s.dr.text((x, y), l, font=ft, fill=fill); y += fs * 1.25

    def box(s, b, t, kind='solid', bg='white', fmax=22, al='c'):
        a, c = s.p(b[0], b[1]); e, f = s.p(b[2], b[3])
        if kind == 'dash':
            for x in range(a, e, 12): s.dr.line([x, c, min(x + 7, e), c], fill=INK, width=2); s.dr.line([x, f, min(x + 7, e), f], fill=INK, width=2)
            for y in range(c, f, 12): s.dr.line([a, y, a, min(y + 7, f)], fill=INK, width=2); s.dr.line([e, y, e, min(y + 7, f)], fill=INK, width=2)
        else:
            s.dr.rectangle([a, c, e, f], fill=bg, outline=INK, width=2)
        s.text(b, t, fmax, al=al)

    def label(s, b, t): s.box(b, t, bg=(200, 200, 200), fmax=22)

    def band(s, b, col=(214, 236, 248)): s.dr.rectangle([*s.p(b[0], b[1]), *s.p(b[2], b[3])], fill=col)

    def hdash(s, xa, xb, y):
        a, c = s.p(xa, y); e, _ = s.p(xb, y)
        for x in range(a, e, 16): s.dr.line([x, c, min(x + 9, e), c], fill=INK, width=2)

    def line(s, *pts, arrow=True, dash=False):
        q = [s.p(pts[i], pts[i + 1]) for i in range(0, len(pts), 2)]
        for (xa, ya), (xb, yb) in zip(q, q[1:]):
            if dash:
                L = max(abs(xb - xa), abs(yb - ya)); n = max(1, L // 12)
                for i in range(0, n, 2):
                    s.dr.line([xa + (xb - xa) * i / n, ya + (yb - ya) * i / n, xa + (xb - xa) * (i + 1) / n, ya + (yb - ya) * (i + 1) / n], fill=INK, width=2)
            else: s.dr.line([xa, ya, xb, yb], fill=INK, width=2)
        if arrow:
            (xa, ya), (xb, yb) = q[-2], q[-1]; a = 12
            if xa == xb: d = 1 if yb > ya else -1; tri = [(xb, yb), (xb - a / 2, yb - d * a), (xb + a / 2, yb - d * a)]
            else: d = 1 if xb > xa else -1; tri = [(xb, yb), (xb - d * a, yb - a / 2), (xb - d * a, yb + a / 2)]
            s.dr.polygon(tri, fill=INK)


# 原文图 1
c = Chart(82, 60, 830, 665)
c.line(170, 75, 808, 75, arrow=False); c.line(808, 75, 815, 75); c.line(170, 75, 163, 75)
c.label((90, 93, 157, 127), '谱系'); c.label((90, 173, 157, 207), '症状'); c.label((90, 305, 160, 340), '体征')
for b, t in [((172, 93, 285, 125), '微不稳'), ((340, 93, 452, 125), '半脱位'), ((506, 93, 618, 125), '脱位'), ((657, 90, 810, 140), '多次不稳发作\n（脱位和半脱位）')]: c.box(b, t)
for b, t in [((172, 173, 285, 205), '间歇性疼痛'), ((320, 173, 470, 230), '间歇性疼痛 ± 滑动感；可有“死臂”或感觉丧失'),
             ((520, 173, 605, 230), '疼痛 ± “死臂”或感觉丧失'), ((657, 173, 808, 230), '反复不稳发作，诱发所需的外力可越来越小')]: c.box(b, t, 'dash', fmax=20)
c.box((555, 250, 700, 282), '制动时间不一', 'dash', fmax=20)
for x in (228, 396, 562, 733): c.line(x, 125 if x != 733 else 140, x, 173)
c.line(562, 230, 562, 250); c.line(678, 230, 678, 250); c.hdash(90, 818, 293)
c.box((237, 312, 742, 332), '患者自述有不稳病史，或在急性脱位制动期结束后就诊', fmax=20)
c.line(488, 332, 488, 428); c.line(488, 380, 398, 380)
c.box((248, 350, 397, 408), '筛查并排除颈椎功能障碍、牵涉痛和神经症状', fmax=19)
c.box((418, 428, 562, 448), '评估', fmax=20); c.line(490, 448, 490, 465, arrow=False); c.line(238, 465, 740, 465, arrow=False)
for x, b, t in [(238, (163, 485, 312, 505), '评估活动度'), (405, (330, 485, 480, 505), '评估肩袖力量'),
                (572, (497, 485, 647, 517), '评估特殊试验和症状调整'), (740, (665, 485, 812, 517), '评估肩胛控制和力量')]:
    c.line(x, 465, x, 485); c.box(b, t, fmax=19)
c.hdash(90, 818, 528); c.band((82, 585, 818, 657)); c.label((90, 594, 155, 628), '方向')
c.box((163, 540, 648, 572), '结合临床病史和不稳试验，诊断为 ≥1 个方向的肩关节不稳', fmax=20)
c.line(405, 572, 405, 586, arrow=False); c.line(238, 586, 572, 586, arrow=False)
for x in (238, 405, 572): c.line(x, 586, x, 602)
c.box((163, 602, 312, 620), '前向', fmax=20); c.box((331, 602, 481, 633), '前、后和下向（多向）', fmax=19); c.box((497, 602, 647, 620), '后向', fmax=20)
c.box((657, 602, 808, 650), '± 调整肩胛位置可明显改变症状', fmax=19); c.line(740, 517, 740, 602)
save(capbox(c.im, '原文图 1（编者中文重绘）  肩关节不稳的谱系、症状和评估'), 2)

# 原文图 2
c = Chart(115, 55, 828, 305)
c.label((122, 64, 232, 97), '不稳发作次数'); c.label((122, 178, 232, 200), '决策'); c.label((122, 265, 232, 298), '处理选择')
c.box((266, 64, 386, 97), '首次肩关节脱位'); c.box((483, 64, 603, 97), '第二次脱位'); c.box((697, 64, 820, 97), '≥3 次脱位或睡眠中脱位', fmax=20)
c.box((284, 115, 370, 155), 'PRIS / NISIS 工具', fmax=20); c.line(326, 97, 326, 115)
c.line(326, 155, 326, 165, arrow=False); c.line(295, 165, 360, 165, arrow=False); c.line(295, 165, 295, 178); c.line(360, 165, 360, 178)
c.box((266, 178, 323, 200), '低风险'); c.box((332, 178, 388, 200), '高风险')
c.line(543, 97, 543, 165, arrow=False); c.line(497, 165, 590, 165, arrow=False); c.line(497, 165, 497, 178); c.line(590, 165, 590, 178)
c.box((458, 178, 536, 225), '之前康复不足', fmax=20); c.box((545, 178, 636, 225), '之前康复充分 / 良好', fmax=20)
c.box((646, 228, 710, 262), '很少采用', 'dash', fmax=19)
c.box((266, 265, 350, 298), '保守治疗', fmax=20); c.box((453, 265, 632, 298), '共同决策：手术还是不手术', fmax=20); c.box((728, 265, 795, 298), '手术', fmax=20)
c.line(295, 200, 295, 265); c.line(497, 225, 497, 240, 322, 240, 322, 265)
c.line(360, 200, 360, 232, 513, 232, 513, 265); c.line(590, 225, 590, 245, 560, 245, 560, 265)
c.line(765, 97, 765, 265); c.line(750, 97, 750, 245, 710, 245, dash=True); c.line(646, 245, 610, 245, 610, 265, dash=True)
c.line(453, 282, 350, 282); c.line(632, 282, 728, 282)
save(capbox(c.im, '原文图 2（编者中文重绘）  肩关节脱位后手术与非手术治疗的决策。PRIS：肩关节复发性不稳预测；NISIS：非手术不稳严重度指数评分'), 3)

# 原文图 3
c = Chart(80, 585, 858, 1085)
c.band((82, 590, 852, 652)); c.label((88, 600, 150, 628), '方向'); c.label((88, 760, 150, 786), '治疗')
c.box((262, 600, 382, 630), '前向'); c.box((418, 598, 534, 632), '前、后和下向', fmax=20); c.box((572, 600, 688, 630), '后向')
c.box((712, 598, 852, 648), '± 调整肩胛位置可明显改变症状', fmax=18)
c.line(322, 630, 322, 650, arrow=False); c.line(285, 650, 357, 650, arrow=False); c.line(285, 650, 285, 672); c.line(357, 650, 357, 672)
c.box((252, 672, 318, 727), '前向，伴后方紧张', fmax=18); c.box((325, 672, 391, 727), '前向，无后方紧张', fmax=18)
c.line(782, 648, 782, 660, arrow=False); c.line(749, 660, 821, 660, arrow=False); c.line(749, 660, 749, 672); c.line(821, 660, 821, 672)
c.box((716, 672, 782, 727), '评估下斜方肌力量', fmax=18); c.box((788, 672, 854, 727), '评估前锯肌力量', fmax=18)
c.hdash(88, 852, 745)
c.box((409, 763, 541, 782), '协同收缩方案', fmax=18); c.box((409, 800, 541, 818), '协同收缩第 1 期', fmax=18); c.box((409, 836, 541, 854), '协同收缩第 2 期', fmax=18)
c.line(475, 630, 475, 763); c.line(475, 782, 475, 800); c.line(475, 818, 475, 836)
c.box((252, 836, 391, 854), '前方肩袖方案', fmax=18); c.box((560, 836, 699, 854), '后方肩袖方案', fmax=18)
c.line(409, 845, 391, 845); c.line(541, 845, 560, 845)
c.line(285, 727, 285, 836); c.line(357, 727, 357, 836); c.line(630, 630, 630, 836)
c.line(252, 700, 200, 700, 200, 872)
c.box((158, 872, 243, 1032), '处理后方紧张', fmax=18); c.line(200, 1032, 200, 1048); c.box((158, 1048, 243, 1078), '监测后方紧张', fmax=17)
for xa, name in [(252, '前方肩袖'), (560, '后方肩袖')]:
    xm, xs = xa + 33, xa + 105
    c.line(xm, 854, xm, 872); c.line(xs, 854, xs, 872)
    c.box((xa, 872, xa + 66, 925), f'{name}运动控制第 1 期', fmax=16); c.box((xa + 73, 872, xa + 139, 925), f'{name}力量第 1 期', fmax=16)
    c.line(xm, 925, xm, 942); c.line(xs, 925, xs, 942)
    c.box((xa, 942, xa + 66, 995), f'{name}运动控制第 2 期', fmax=16); c.box((xa + 73, 942, xa + 139, 995), f'{name}力量第 2 期', fmax=16)
    c.line(xm, 995, xm, 1013); c.line(xs, 995, xs, 1013)
    c.box((xa, 1013, xa + 139, 1031), f'{name}第 3 期', fmax=17); c.line(xa + 70, 1031, xa + 70, 1048); c.box((xa, 1048, xa + 139, 1066), f'{name}第 4 期', fmax=17)
c.line(391, 1022, 548, 1022, 548, 845, 560, 845)
c.line(749, 727, 749, 836); c.line(821, 727, 821, 836)
c.box((716, 836, 782, 890), '下斜方肌强化方案', fmax=17); c.box((788, 836, 854, 890), '前锯肌强化方案', fmax=17)
save(capbox(c.im, '原文图 3（编者中文重绘）  从亚急性期到末期的进阶康复：按不稳方向、活动受限和常见肌肉缺陷选择方案'), 4)

blocks = [('PRIS（Olds 等）：6 个预测复发的因素', '① 骨性 Bankart 损伤  ② 年龄 16～25 岁  ③ 优势侧受累\n④ 恐动症量表（TSK）得分高  ⑤ 肩痛与功能障碍指数（SPADI）得分高  ⑥ 未制动\n可在作者网站的免费在线计算器输入数据得到复发风险', LT, TEAL),
          ('NISIS（Tokish 等）：6 项加权评分，满分 10 分', '冲撞类运动 3 分　　年龄 >15 岁 2 分　　X 线可见骨缺损 2 分\n脱位（而非半脱位）1 分　　优势侧 1 分　　男性 1 分\n<7 分为低风险：最初研究中 97% 非手术治疗成功；>7 分为高风险', OR, (200, 110, 30))]
save(card(1200, '首次前脱位后的复发风险工具（编者根据原文整理）', blocks), 5)

save(capbox(raw(51), '原文图 4  外旋等长强化：A 肩前屈 90°、B 肩前屈 135°（侧卧，用对侧手托住上臂，保持肩胛不代偿）'), 6)
save(capbox(raw(69), '原文图 5  多向不稳患者的侧卧支撑进阶，目标是让肱骨头始终居中于关节盂。A：侧卧，上肢约 90° 举起、无负重，保持中立位；'
                     'B：手持 3 kg、再到 5 kg 做轴向负荷；C：手和髋支撑上半身体重'), 7)

c = Chart(212 - 8, 66, 692 + 8, 282, 1200)
c.box((212, 73, 390, 93), '投掷和过头运动员', fmax=22); c.box((478, 73, 614, 93), '冲撞类运动员', fmax=22)
c.box((405, 120, 550, 140), '前向不稳', fmax=22); c.box((553, 120, 690, 140), '后向不稳', fmax=22)
c.line(300, 93, 300, 165); c.line(546, 93, 546, 106, arrow=False); c.line(478, 106, 622, 106, arrow=False); c.line(478, 106, 478, 120); c.line(622, 106, 622, 120)
c.line(478, 140, 478, 165); c.line(622, 140, 622, 165)
c.box((212, 165, 390, 275), '自我评估角\n侧撑旋转\nBABER（外展外旋位抛球）\n上肢 Y 平衡\n肩耐力测试\n后肩耐力测试\n单臂坐位推铅球', fmax=19, al='l')
c.box((405, 165, 550, 225), '侧撑旋转\nASH 测试\n仰卧动态恐惧试验', fmax=19, al='l')
c.box((553, 165, 690, 275), '侧撑旋转\n线跳\n击掌俯卧撑\n俯卧撑\nCKUEST\n上肢 Y 平衡\n单臂跳\n上肢旋转测试', fmax=19, al='l')
save(capbox(c.im, '原文图 6（编者中文重绘）  按运动类型和不稳方向选择的回归运动测试。ASH：运动员肩部测试；BABER：外展外旋位抛球；CKUEST：闭链上肢稳定性测试'), 8)

def tagged(x, t):
    im = raw(x); dr = ImageDraw.Draw(im); f = font(max(20, im.width // 16)); w = dr.textlength(t, font=f)
    dr.rounded_rectangle([8, 8, 26 + w, 20 + f.size], 8, fill=(255, 255, 255), outline=(200, 200, 200)); dr.text((17, 12), t, font=f, fill=INK); return im


save(capbox(stack([row([tagged(199, 'A'), tagged(200, 'B')]), row([tagged(197, 'C'), tagged(198, 'D')])]),
            '原文附录图 1  下斜方肌训练进阶（A～D）：俯卧位，保持肩胛后倾。双手掌心向上放在床上等长收缩 → 双臂伸直外展 45°、掌心向下等长收缩 → '
            '从“W”位（外展外旋 90°、屈肘）到“Y”位（伸肘外展 135°）'), 9)
save(capbox(stack([row([tagged(217, 'A 仰卧出拳'), tagged(216, 'B 侧卧出拳'), tagged(215, 'C 四点跪')]),
                   row([tagged(219, 'D 平板（脚撑）'), tagged(212, 'E 平板抬腿'), tagged(218, 'F 侧坐支撑')]),
                   row([tagged(214, 'G 跪姿侧桥'), tagged(213, 'H 侧桥'), Image.new('RGB', raw(213).size, 'white')])]),
            '原文附录图 2  前锯肌渐进负荷：A～E 为冠状面方向，F～H 为矢状面方向（原文如此）'), 10)

c = raw(69).crop((0, 0, 834, 355)).resize((900, 383), Image.LANCZOS)
c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
