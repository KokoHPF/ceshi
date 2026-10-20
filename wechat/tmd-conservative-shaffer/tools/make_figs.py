#!/usr/bin/env python3
"""Shaffer 等 2014 颞下颌关节紊乱（第二部分）：保守治疗：首图中文标题卡；原文图 1～12 手法照片按类别拼板、中文标注（原图直接使用）。
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
dr.text((70, 60), '综述 · 《手法与整骨治疗杂志》2014', font=font(32), fill=TEAL)
dr.text((70, 160), '颞下颌关节紊乱（第二部分）：', font=font(60), fill=INK)
dr.text((70, 246), '保守治疗', font=font(60), fill=INK)
dr.line([70, 380, W - 70, 380], fill=(200, 205, 210), width=2)
dr.text((70, 410), 'Shaffer SM, Brismée JM, Sizer PS, Courtney CA. J Man Manip Ther 2014;22(1):13-23', font=font(28), fill=GREY)
dr.text((70, 465), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

XR = {1: 4, 2: 5, 3: 6, 4: 11, 5: 10, 6: 15, 7: 16, 8: 23, 9: 20, 10: 21, 11: 22, 12: 27}
LAB = {1: '图 1　分离（牵引）', 2: '图 2　前向滑动', 3: '图 3　张口位前向滑动', 4: '图 4　内/外侧滑动',
       5: '图 5　下-前-内复合滑动', 6: '图 6　张口位复合滑动', 7: '图 7　自我松动（闭口）', 8: '图 8　自我松动（张口）',
       9: '图 9　单指松解颞肌', 10: '图 10　双侧加强指松解颞肌', 11: '图 11　三指松解颞肌', 12: '图 12　口内松解翼内肌'}
PH = {n: raw(x) for n, x in XR.items()}


def row(nums, W=1200, gap=10):
    ims = [PH[n] for n in nums]; hh = 600
    ims = [m.resize((round(m.width * hh / m.height), hh), Image.LANCZOS) for m in ims]
    s = (W - gap * (len(ims) - 1)) / sum(m.width for m in ims)
    ims = [m.resize((round(m.width * s), round(hh * s)), Image.LANCZOS) for m in ims]
    h = ims[0].height; out = Image.new('RGB', (W, h + 52), 'white'); d = ImageDraw.Draw(out); x = 0
    for n, m in zip(nums, ims):
        out.paste(m, (x, 0)); f = font(26)
        while d.textlength(LAB[n], font=f) > m.width - 6: f = font(f.size - 1)
        ctext(d, x + m.width / 2, h + 10, LAB[n], f); x += m.width + gap
    return out


save(board([row([1, 2, 3])], '仰卧位关节松动：分离与前向滑动'), 2)
save(board([row([4, 5, 6])], '仰卧位关节松动：内侧滑动与复合滑动'), 3)
save(board([row([7, 8])], '居家自我松动'), 4)
save(board([row([9, 10]), row([11, 12])], '咀嚼肌软组织松解'), 5)

# 封面 900×383：图 2
c = PH[2]; h = round(c.width * 383 / 900); y0 = 60
c.crop((0, y0, c.width, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
