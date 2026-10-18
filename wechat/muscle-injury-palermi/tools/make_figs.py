#!/usr/bin/env python3
"""Palermi 2021 下肢间接结构性肌肉损伤康复：首图为原文标题区；三期康复总览自绘；表 2～5 动作照片（去掉表格文字）
按肌群拼图并加中文动作名；地垫等英文商标模糊。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); RED = (190, 40, 50); TEAL = (0, 110, 130)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


pix = d[0].get_pixmap(dpi=200, clip=pymupdf.Rect(160, 70, 560, 158))
save(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), 1)

# ---------- 三期总览（自绘） ----------
W, H = 1600, 1250; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
ctext(dr, W / 2, 24, '下肢肌肉拉伤：三期康复', font(48))
ctext(dr, W / 2, 92, '进阶看临床、功能和影像标准，不按固定天数', font(30), GREY)
P = [('0 期', '伤后 0～72 小时', (120, 120, 120), ['伤后 36～48 小时做超声', 'PRICE / POLICE 原则', '冷敷加压：15～20 分钟，', '间隔 30～60 分钟，共 6 h', '加压 40～50 mmHg', '短暂制动 3～5 天', '72 小时内避免热疗']),
     ('一期', '破坏期', (40, 90, 160), [mkb := '★ 等长收缩', '30～50 次 × 10～20 秒', '不痛，从小力矩角度开始', '无痛的延展性训练', '不做深层按摩', '健肢、上肢有氧训练', '电刺激、激光可用']),
     ('二期', '修复 / 再生期', (0, 130, 110), ['★ 向心收缩', '慢速控制，≤ 60% 1RM', '离心部分尽量减到最小', '本体感觉、核心稳定', '有氧：单车 → 椭圆机 →', '减重跑 → 跑步机', '可以开始按摩']),
     ('三期', '重塑期（可 ＞60 天）', (190, 60, 40), ['★ 离心收缩', '逐步加量，可用弹力带', '等速、惯性训练', '拉伸 10～15 秒 → 1 分钟', '肌力 ≥ 对侧 70% 才加跑', '专项训练放在最后', 'GPS 监控跑量'])]
for i, (t, s, col, items) in enumerate(P):
    x0 = 30 + i * 392; y0 = 160
    dr.rounded_rectangle([x0, y0, x0 + 370, y0 + 130], 18, fill=col)
    ctext(dr, x0 + 185, y0 + 16, t, font(46), 'white'); ctext(dr, x0 + 185, y0 + 80, s, font(28), 'white')
    dr.rounded_rectangle([x0, y0 + 140, x0 + 370, y0 + 650], 18, outline=col, width=4)
    for k, it in enumerate(items):
        f = font(34 if it.startswith('★') else 27)
        ctext(dr, x0 + 185, y0 + 170 + k * 66, it, f, col if it.startswith('★') else INK)
G = [('一期 → 二期', '最大等长收缩不痛；主动和被动牵伸到末端不痛；关节活动度完整；超声上裂隙消失'),
     ('二期 → 三期', '逐渐加量的抗阻向心收缩不痛；次最大离心收缩不痛；超声上裂隙基本消失'),
     ('回到训练', '一周至少 4 次正常训练不痛、不怕；GPS、心率数据与伤前差距 ≤ 10%；最大摄氧量 ≥ 伤前的 90%')]
y = 840
for t, s in G:
    dr.rounded_rectangle([30, y, W - 30, y + 120], 16, fill=(244, 244, 244))
    dr.text((60, y + 20), t, font=font(34), fill=RED)
    words = s; lines = []; cur = ''
    for ch in words:
        if dr.textlength(cur + ch, font=font(28)) > W - 430: lines.append(cur); cur = ''
        cur += ch
    lines.append(cur)
    for k, l in enumerate(lines): dr.text((330, y + 24 + k * 44), l, font=font(28), fill=INK)
    y += 135
save(im, 2)

# ---------- 动作照片 ----------
for pg in range(6, 15):
    p = d[pg]
    for w in p.get_text('words'): p.add_redact_annot(pymupdf.Rect(w[:4]))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)


def grab(pg, y0, y1):
    pix = d[pg].get_pixmap(dpi=220, clip=pymupdf.Rect(150, y0, 540, y1)); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    a = np.array(im); nw = a.min(2) < 235
    for y in range(a.shape[0]):
        if nw[y].mean() > .5 and a[y][nw[y]].std() < 30: a[y] = 255
    im = Image.fromarray(a); bb = ImageOps.invert(im.convert('L')).point(lambda v: 255 if v > 25 else 0).getbbox()
    return im.crop(bb)


def blur(im, boxes):
    for bx in boxes:
        b = tuple(int(v * s) for v, s in zip(bx, (im.width, im.height, im.width, im.height)))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2])
    return im


EX = {
    'H': [('等长：近端损伤', [(6, 385, 526)]), ('等长：中段或远端损伤', [(6, 531, 681)]), ('不同角度等长', [(6, 688, 758)]),
          ('伸展者', [(7, 147, 270)]), ('滑行者（单腿后滑）', [(7, 278, 443)]), ('北欧挺', [(7, 450, 560), (7, 565, 675)]),
          ('钟摆', [(8, 146, 263)]), ('直腿抬高拉伸', [(8, 270, 441)]), ('离心屈膝拉伸（预防）', [(8, 459, 588), (8, 593, 724)]),
          ('离心伸髋拉伸（预防）', [(9, 146, 270)])],
    'Q': [('等长：近端损伤', [(9, 362, 488)]), ('等长：中段或远端损伤', [(9, 495, 627)]), ('动态：近端损伤', [(9, 643, 758)]),
          ('动态：中段或远端损伤', [(10, 146, 247)]), ('跪姿离心屈髋伸膝拉伸（预防）', [(10, 264, 403)])],
    'A': [('夹球等长', [(10, 491, 653), (10, 657, 746)]), ('徒手抗阻内收', [(11, 146, 280), (11, 282, 411)]),
          ('弹力带内收', [(11, 417, 740)]), ('半球上本体感觉训练', [(12, 146, 319)]),
          ('离心侧弓步拉伸（预防）', [(12, 337, 466), (12, 471, 609)]), ('哥本哈根内收肌训练（预防）', [(13, 147, 272), (13, 274, 404)])],
    'C': [('徒手抗阻等长', [(13, 496, 608), (13, 612, 758)]), ('徒手抗阻向心/离心', [(14, 147, 318)]),
          ('向心/离心提踵', [(14, 326, 498)]), ('本体感觉训练', [(14, 516, 643)])],
}
BLUR = {('H', 8, 0): [(0, .8, .8, 1), (0, 0, .45, .14)], ('H', 8, 1): [(0, .78, .9, 1), (0, 0, .45, .12)],
        ('Q', 0, 0): [(0, 0, .13, .25)], ('Q', 2, 0): [(0, 0, .19, .16)], ('Q', 1, 0): [(.24, .86, .4, .96)],
        ('C', 3, 0): [(.06, .3, .27, .42)], ('H', 1, 0): [(0, 0, .22, .18)], ('H', 4, 0): [(0, .9, .62, 1), (.74, .2, 1, .45)],
        ('A', 4, 0): [(0, .82, .45, 1)], ('A', 4, 1): [(0, .88, .5, 1)],
        ('A', 5, 0): [(.12, .66, .9, .86)], ('A', 5, 1): [(.12, .78, .9, .95)]}
TRIM = {('A', 3, 0): .05}


def board(title, items, key, start, n, color=TEAL, CW=640, CH=420):
    rows = (len(items) + 1) // 2
    c = Image.new('RGB', (2 * CW + 60, 100 + rows * (CH + 80)), 'white'); dr = ImageDraw.Draw(c)
    dr.rectangle([0, 0, c.width, 76], fill=color); dr.text((30, 16), title, font=font(42), fill='white')
    for i, (name, parts) in enumerate(items):
        gx, gy = 30 + (i % 2) * CW, 100 + (i // 2) * (CH + 80)
        dr.text((gx, gy), f'{start + i}. {name}', font=font(32), fill=INK)
        ims = []
        for j, pp in enumerate(parts):
            m = grab(*pp); k = (key, start + i - 1, j)
            if k in TRIM: m = m.crop((0, int(m.height * TRIM[k]), m.width, m.height))
            ims.append(blur(m, BLUR.get(k, [])))
        if len(ims) == 1:
            m = ims[0]
        else:
            w = max(x.width for x in ims); ims = [x.resize((w, round(x.height * w / x.width))) for x in ims]
            m = Image.new('RGB', (w, sum(x.height for x in ims) + 10), 'white'); yy = 0
            for x in ims: m.paste(x, (0, yy)); yy += x.height + 10
        s = min((CW - 40) / m.width, (CH - 10) / m.height); m = m.resize((round(m.width * s), round(m.height * s)), Image.LANCZOS)
        c.paste(m, (gx + (CW - 20 - m.width) // 2, gy + 52))
    save(c, n)


board('腘绳肌（一）：等长与动态', EX['H'][:6], 'H', 1, 3)
board('腘绳肌（二）：本体感觉、拉伸与预防', EX['H'][6:], 'H', 7, 4)
board('股直肌（股四头肌）', EX['Q'], 'Q', 1, 5, (40, 90, 160))
board('内收肌', EX['A'], 'A', 1, 6, (0, 130, 110))
board('小腿三头肌（比目鱼肌、腓肠肌）', EX['C'], 'C', 1, 7, (190, 60, 40))

cv = Image.new('RGB', (900, 383), 'white'); dr = ImageDraw.Draw(cv)
m = blur(grab(7, 278, 443), BLUR[('H', 4, 0)]); m = m.resize((round(m.width * 383 / m.height), 383), Image.LANCZOS); cv.paste(m, (900 - m.width, 0))
dr.text((30, 40), '肌肉拉伤', font=font(76), fill=INK)
dr.text((30, 150), '分三期怎么练？', font=font(50), fill=TEAL)
dr.text((30, 230), '等长 → 向心 → 离心', font=font(34), fill=RED)
dr.text((30, 320), 'JFMK 2021 · 综述精读', font=font(22), fill=GREY)
cv.save(f'{OUT}/cover.jpg', quality=92)
