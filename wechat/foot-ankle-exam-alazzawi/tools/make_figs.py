#!/usr/bin/env python3
"""Alazzawi 等 2017 足踝病史与临床检查：首图中文标题卡；原文图 1～10 检查照片直接使用（多张拼图按等高排列），加中文图注；
检查流程卡为编者根据原文整理。
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
dr.text((70, 50), '小型综述 · 《世界骨科杂志》2017', font=font(32), fill=TEAL)
dr.text((70, 140), '足踝病史与临床检查：', font=font(56), fill=INK)
dr.text((70, 225), '日常实践指南', font=font(56), fill=INK)
dr.line([70, 345, W - 70, 345], fill=(200, 205, 210), width=2)
dr.text((70, 375), 'Alazzawi S, Sukeik M, King D, Vemulapalli K.', font=font(28), fill=GREY)
dr.text((70, 420), 'World J Orthop. 2017;8(1):21-29', font=font(28), fill=GREY)
dr.text((70, 480), '编者中文重排，仅作学术交流（原文 CC BY-NC 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(row([raw(16), raw(18)]), '原文图 1（左）胫骨前肌检查：踝最大背伸加内翻，检查者向跖屈方向推，患者对抗，另一手触摸肌腱收缩；'
                                     '原文图 2（右）胫骨后肌检查：完全跖屈位内翻，检查者在足内侧缘向外推（试图外翻），另一手触摸肌腱'), 2)
save(capbox(row([raw(30), raw(32)]), '原文图 3  腓骨长、短肌检查：完全跖屈位外翻，检查者在足外侧缘向内推（试图内翻）'), 3)
save(capbox(row([raw(34), raw(36)]), '原文图 4（左）𧿹长伸肌检查：踝中立位，患者伸大脚趾，检查者向跖屈方向压；'
                                     '原文图 5（右）趾长伸肌检查：患者伸外侧四趾，检查者向跖屈方向压'), 4)
save(capbox(row([raw(38), raw(40)]), '原文图 6（左）前抽屉试验：小腿自然下垂，一手固定踝上方，一手保持踝跖屈并把足向前拉，观察距骨前外侧皮肤有无凹陷（沟征）；'
                                     '原文图 7（右）内翻应力试验：屈膝 90°，一手从内侧固定小腿，一手把跟骨和距骨推向内翻，过度内翻和 / 或疼痛为阳性'), 5)
save(capbox(row([raw(53), raw(55)]), '原文图 8  Coleman 木块试验：木块垫在足外侧缘下，让前足内侧悬空、第 1 跖骨下垂，消除第 1 跖列的影响。'
                                     '后足变为外翻或中立 → 后足柔软（前足驱动的后足内翻）；仍内翻 → 后足僵硬（后足驱动）'), 6)
save(capbox(row([raw(57), raw(59)]), '原文图 9  Semmes-Weinstein 单丝试验：用 10 g 单丝按压评估感觉缺失程度，尤其适用于糖尿病 Charcot 足'), 7)
save(capbox(row([raw(61), raw(63)]), '原文图 10  Silfverskiold 试验：屈膝位和伸膝位分别最大背伸踝关节；屈膝时背伸明显更多，提示腓肠肌紧张'), 8)

blocks = [('1 问病史', '疼痛（部位、性质、负重相关、放射、程度、夜间痛、加重和缓解因素）→ 畸形 → 肿胀 → 不稳 → 外伤史 → 伴随症状（红旗征）→ 一般病史', LT, TEAL),
          ('2 看鞋、鞋垫和助行器', '鞋跟外侧早磨损 → 旋后畸形；内侧缘磨损 → 旋前畸形', OR, (200, 110, 30)),
          ('3 站立位', '下肢力线、脊柱、骨盆、肌萎缩 → 足弓、足趾畸形 → 从前看“躲猫猫征” → 从后看后跟力线和“多趾征” → 踮脚尖看后跟是否内翻、足弓是否出现', GR, (40, 130, 60)),
          ('4 步态', '正常步行 → 脚尖走 → 脚跟走 → 足内侧缘走 → 足外侧缘走；别漏掉足下垂', PK, RED),
          ('5 坐位：看、摸、动', '看：足底到全足的皮肤、瘢痕、溃疡、毛发、趾甲、胼胝、鸡眼\n摸：先问哪里不能碰 → 皮温对比 → 按固定顺序找压痛\n动：主动 → 被动（背伸做 Silfverskiold）→ 距下 → 中足 → 第 1 跗跖关节 → 前足逐个关节', LT, TEAL),
          ('6 肌力和特殊试验', '按 MRC 0～5 级评肌力；按怀疑的诊断选特殊试验', OR, (200, 110, 30)),
          ('7 别忘了', '神经血管检查、脊柱（侧弯、腰骶部毛发丛）、双下肢长度、髋和膝；运动员加做单腿蹲、深蹲跳等功能测试', GR, (40, 130, 60))]
save(card(1200, '足踝检查流程（编者根据原文整理）', blocks), 9)

c = raw(53); k = 900 / c.width; c = c.resize((900, round(c.height * k)), Image.LANCZOS)
y0 = (c.height - 383) // 2 + 60; c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
