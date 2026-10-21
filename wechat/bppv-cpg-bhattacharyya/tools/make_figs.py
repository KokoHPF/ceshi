#!/usr/bin/env python3
"""BPPV 临床实践指南（2017 更新版）：首图中文标题卡；原文图 1 英文标注按 OCR 定位（src/o<xref>.json）改为中文；
图 2～7 手法示意图直接使用，标题改为中文；图 8 流程图按原图版式用中文重绘；关键行动建议总览卡为编者根据原文表 5 整理。
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
import zh
SRC = _os.path.join(HERE, '..', 'src')

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '临床实践指南 · 《耳鼻咽喉头颈外科》2017 增刊', font=font(32), fill=TEAL)
dr.text((70, 140), '临床实践指南：', font=font(56), fill=INK)
dr.text((70, 225), '良性阵发性位置性眩晕（更新版）', font=font(56), fill=INK)
dr.line([70, 345, W - 70, 345], fill=(200, 205, 210), width=2)
dr.text((70, 375), 'Bhattacharyya N, Gubbels SP, Schwartz SR, et al.', font=font(28), fill=GREY)
dr.text((70, 420), 'Otolaryngol Head Neck Surg. 2017;156(3S):S1-S47', font=font(28), fill=GREY)
dr.text((70, 480), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


def relab(x, spec, extra=()):
    im, _ = zh.apply(raw(x), f'{SRC}/o{x}.json', spec, W=1200, extra=extra); return im


def retitle(x, t):
    """把左上角英文标题盖白，写中文标题（框取自 OCR）"""
    im = raw(x); k = 1200 / im.width; im = im.resize((1200, round(im.height * k)), Image.LANCZOS)
    import json
    b = [v * 1.2 for v in json.load(open(f'{SRC}/o{x}.json'))[0][:4]]
    dr = ImageDraw.Draw(im); dr.rectangle([b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4], fill='white')
    f = font((b[3] - b[1]) * 0.95); dr.text((b[0], b[1] - 2), t, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
    return im


f1 = relab(91, [(['Vantage@720,245', 'point@720,265'], '观察点'), (['Vantage@610,967', 'point@610,987'], '观察点'),
                (['Superior@340,273', 'canal@344,295'], '上半规管'), (['Superior@50,852', 'canal@52,873'], '上半规管'),
                (['Posterior@60,335', 'canal@60,356'], '后半规管'), (['Posterior@375,975', 'canal@375,996'], '后半规管'),
                (['Posterior-canal@334,477', 'ampulla@333,499'], '后半规管壶腹'), (['Posterior-canal@342,804', 'ampulla@341,825'], '后半规管壶腹'),
                ('Gravity', '重力'), ('Utriculus', '椭圆囊'), ('Particles', '耳石颗粒'), ('Sagittal body plane', '')],
           extra=[((408, 20, 760, 119), '', {'bg': (255, 255, 255)})])
# 矢状面箭头和 45° 被标签框盖掉，按原位置补画
dr = ImageDraw.Draw(f1); q = lambda *v: [int(a * 1.2) for a in v]
dr.line(q(494, 121, 700, 73), fill=(40, 40, 40), width=3); dr.polygon(q(714, 70, 697, 68, 701, 80), fill=(40, 40, 40))
dr.line(q(494, 121, 660, 121), fill=(40, 40, 40), width=2)
dr.text(q(540, 30), '身体矢状面', font=font(32), fill=INK); dr.text(q(640, 92), '45°', font=font(22), fill=INK)
save(capbox(f1, '原文图 1  Dix-Hallpike 试验（以右耳为例）。A：检查者站在患者右侧，把头向右转 45°，使右侧后半规管与身体矢状面对齐；'
                'B：保持转头，较快地把患者从坐位放倒成右耳朝下的仰卧位，再让颈部后伸约 20°（下巴略上抬，头悬于床沿外）。'
                '记录眼震的潜伏期、持续时间和方向，以及眩晕的潜伏期和持续时间。小图箭头示典型后半规管 BPPV 的眼震方向，并示意游离耳石颗粒的推测位置。'
                '来源：Furman & Cass, N Engl J Med 1999（© 马萨诸塞医学会，经许可改编转载）'), 2)
save(capbox(raw(95), '原文图 2  仰卧滚转试验。（1）仰卧、头居中；（2）把头快速向右转 90°，观察有无特征性眼震；回到面朝上（1），等眼震全部消失后，'
                     '（3）再把头快速向左转 90°，再次观察。来源：Fife 等 2008（© Barrow 神经研究所，经许可改编转载）'), 3)
save(capbox(raw(105), '原文图 3  耳石复位手法（Epley 手法），用于右耳后半规管 BPPV。具体步骤见文中表 10。来源：Fife 等 2008（© Barrow 神经研究所）'), 4)
save(capbox(retitle(107, 'Semont 手法（解脱法）'), '原文图 4  Semont 解脱法，用于右耳后半规管 BPPV。具体步骤见文中表 11。来源：Fife 等 2008（© Barrow 神经研究所）'), 5)
save(capbox(retitle(112, 'Lempert 滚转法'), '原文图 5  Lempert 360° 滚转法（“烤肉串”滚转法），用于右侧水平半规管 BPPV（向地性）。具体步骤见文中表 13。来源：Fife 等 2008（© Barrow 神经研究所）'), 6)
save(capbox(row([retitle(110, 'Gufoni 法：向地性'), retitle(111, 'Gufoni 法：背地性')]),
            '原文图 6（左）Gufoni 法，用于右侧水平半规管 BPPV 向地性；原文图 7（右）Gufoni 法，用于右侧水平半规管 BPPV 背地性（图中为变式 1）。'
            '具体步骤见文中表 14、表 15。来源：Fife 等 2008（© Barrow 神经研究所）'), 7)

# 原文图 8 流程图：按原图坐标（875×1169）放大重绘
S = 1.6; GRAYB = (125, 128, 130); ORG = (236, 160, 60); TL = (40, 160, 180)
im = Image.new('RGB', (int(875 * S), int(1180 * S)), 'white'); dr = ImageDraw.Draw(im)
z = lambda *v: [int(a * S) for a in v]


def mtext(cx, cy, t, fs=15, fill='white'):
    f = font(fs * S); ls = t.split('\n'); lh = f.size * 1.25; y = cy - lh * len(ls) / 2
    for l in ls:
        dr.text((cx * S - dr.textlength(l, font=f) / 2, y * S / S), l, font=f, fill=fill); y += lh


def rect(x0, y0, x1, y1, t, kas=None):
    dr.rectangle(z(x0, y0, x1, y1), fill=GRAYB); mtext((x0 + x1) / 2, (y0 + y1) / 2 * S / S, t) if False else None
    f = font(15 * S); ls = t.split('\n'); lh = f.size * 1.25; y = (y0 + y1) / 2 * S - lh * len(ls) / 2
    for l in ls:
        dr.text(((x0 + x1) / 2 * S - dr.textlength(l, font=f) / 2, y), l, font=f, fill='white'); y += lh
    if kas: dr.text(z(x0, y0 - 24), kas, font=font(13 * S), fill=INK)


def dia(cx, cy, w, h, t, kas=None):
    dr.polygon(z(cx - w / 2, cy, cx, cy - h / 2, cx + w / 2, cy, cx, cy + h / 2), fill=ORG)
    f = font(14 * S); ls = t.split('\n'); lh = f.size * 1.25; y = cy * S - lh * len(ls) / 2
    for l in ls:
        dr.text((cx * S - dr.textlength(l, font=f) / 2, y), l, font=f, fill='white'); y += lh
    if kas: dr.text(z(*kas[1]), kas[0], font=font(13 * S), fill=INK)


def oval(x0, y0, x1, y1, t):
    dr.rounded_rectangle(z(x0, y0, x1, y1), int((y1 - y0) / 2 * S), fill=TL)
    f = font(15 * S); ls = t.split('\n'); lh = f.size * 1.25; y = (y0 + y1) / 2 * S - lh * len(ls) / 2
    for l in ls:
        dr.text(((x0 + x1) / 2 * S - dr.textlength(l, font=f) / 2, y), l, font=f, fill='white'); y += lh


def arr(*pts, lab=None, lp=None):
    p = z(*pts); dr.line(p, fill=(70, 70, 70), width=int(2 * S), joint='curve')
    (x0, y0), (x1, y1) = (p[-4], p[-3]), (p[-2], p[-1]); a = 9 * S
    if x0 == x1: d = 1 if y1 > y0 else -1; tri = [(x1, y1), (x1 - a / 2, y1 - d * a), (x1 + a / 2, y1 - d * a)]
    else: d = 1 if x1 > x0 else -1; tri = [(x1, y1), (x1 - d * a, y1 - a / 2), (x1 - d * a, y1 + a / 2)]
    dr.polygon(tri, fill=(70, 70, 70))
    if lab: dr.text(z(*lp), lab, font=font(15 * S), fill=INK, stroke_width=1, stroke_fill=INK)


# 图例
dr.rectangle(z(30, 15, 200, 88), outline=(180, 180, 180), width=2)
dr.polygon(z(40, 30, 52, 23, 64, 30, 52, 37), fill=ORG); dr.text(z(72, 21), '作出判断', font=font(12 * S), fill=INK)
dr.rounded_rectangle(z(40, 46, 64, 58), int(6 * S), fill=TL); dr.text(z(72, 43), '开始或结束', font=font(12 * S), fill=INK)
dr.rectangle(z(40, 67, 64, 79), fill=GRAYB); dr.text(z(72, 64), '采取行动', font=font(12 * S), fill=INK)

oval(355, 10, 635, 62, '病史 / 症状与 BPPV\n相符的患者')
arr(495, 62, 495, 103)
dia(495, 155, 240, 104, '鉴别 BPPV 与\n其他眩晕病因', ('KAS 2A', (392, 104)))
arr(375, 155, 234, 155, lab='仍符合 BPPV', lp=(255, 122)); arr(615, 155, 758, 155, lab='不符合 BPPV', lp=(630, 122))
oval(760, 128, 866, 184, '退出\n本指南')
rect(12, 125, 232, 205, '做 Dix-Hallpike 试验\n（查后半规管 BPPV）', 'KAS 1A')
arr(122, 205, 122, 243)
dia(122, 295, 228, 100, '扭转性\n上跳型眼震？')
arr(236, 295, 303, 295, lab='否', lp=(258, 265))
rect(305, 255, 528, 335, '做仰卧滚转试验\n（查水平半规管 BPPV）', 'KAS 1B')
arr(122, 345, 122, 396, lab='是', lp=(132, 362))
rect(12, 398, 232, 478, '不做\n影像学检查', 'KAS 3A')
arr(418, 335, 418, 393)
dia(418, 440, 228, 94, '典型的\n方向改变性眼震？')
arr(304, 440, 234, 440, lab='是', lp=(258, 405)); arr(532, 440, 601, 440, lab='否', lp=(555, 405))
oval(603, 412, 718, 468, '退出\n本指南')
arr(122, 478, 122, 518)
rect(12, 520, 232, 600, '不做\n前庭功能检查', 'KAS 3B')
arr(122, 600, 122, 643)
rect(12, 645, 232, 725, '不常规开药', 'KAS 6')
arr(232, 685, 305, 685)
rect(307, 645, 527, 725, '就安全、复发和随访\n对患者进行教育', 'KAS 8')
arr(527, 685, 598, 685)
rect(600, 645, 820, 725, '评估影响处理的因素', 'KAS 2B')
arr(710, 725, 710, 773)
dia(712, 826, 228, 104, '有复位禁忌\n或患者拒绝？')
arr(598, 826, 529, 826, lab='否', lp=(555, 793))
rect(307, 790, 527, 868, '按 BPPV 类型\n做耳石复位（CRP）', 'KAS 4A')
arr(307, 829, 234, 829)
rect(12, 790, 232, 868, '复位后\n不加体位限制', 'KAS 4B')
arr(712, 878, 712, 928, lab='是', lp=(722, 893))
rect(600, 930, 820, 1010, '观察\n或前庭康复', 'KAS 4C 或 5')
arr(122, 868, 122, 967, 305, 967)
rect(307, 930, 527, 1010, '1 个月时\n复评治疗反应', 'KAS 7A')
arr(600, 970, 529, 970)
arr(417, 1010, 417, 1060)
dia(418, 1112, 228, 100, '1 个月时\n仍有症状？')
arr(304, 1112, 234, 1112, lab='是', lp=(258, 1078)); arr(532, 1112, 601, 1112, lab='否', lp=(555, 1078))
rect(12, 1072, 232, 1152, '重新评估或转诊：\n未缓解的 BPPV\n或其他病因', 'KAS 7B')
oval(603, 1085, 718, 1141, '退出\n本指南')
save(capbox(im, '原文图 8（编者中文重绘）  各条关键行动建议（KAS）之间的关系流程。BPPV：良性阵发性位置性眩晕；CRP：耳石复位手法'), 8)

blocks = [('诊断', '1a 用 Dix-Hallpike 试验确诊后半规管 BPPV【强推荐】\n1b Dix-Hallpike 阴性或出现水平眼震 → 做仰卧滚转试验查水平半规管【推荐】\n2a 与其他头晕/眩晕病因鉴别【推荐】\n2b 评估活动受限、平衡障碍、中枢疾病、无人照护、跌倒风险【推荐】', LT, TEAL),
          ('不要做', '3a 符合诊断标准且无其他可疑体征时，不做影像学【反对】\n3b 同上，不做前庭功能检查【反对】\n4b 复位后不加体位限制【强烈反对】\n6 不常规使用前庭抑制药（抗组胺药、苯二氮䓬类）【反对】', PK, RED),
          ('治疗', '4a 后半规管 BPPV 用耳石复位手法治疗，或转诊给会做的人【强推荐】\n4c 可选择观察加随访【可选】\n5 可提供前庭康复【可选】', GR, (40, 130, 60)),
          ('随访与教育', '7a 1 个月内复评，记录症状是否缓解【推荐】\n7b 症状持续者评估未缓解的 BPPV 和其他外周/中枢疾病【推荐】\n8 告知跌倒风险、复发可能和随访的重要性【推荐】', OR, (200, 110, 30))]
save(card(1200, '14 条关键行动建议一览（编者根据原文表 5 整理）', blocks), 9)

c = raw(107); k = 900 / c.width; c = c.resize((900, round(c.height * k)), Image.LANCZOS)
y0 = max(0, c.height - 383 - 10); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
