#!/usr/bin/env python3
"""Caratun 等 2018 大负荷力量训练治疗足底筋膜炎：首图中文标题卡；原文图 1、2 英文标注改为中文，图 3 患者指导按原文译为中文卡片，
图 4 照片重排为三栏；原方案与简化方案对比卡为编者根据原文及 Rathleff 2015 整理。
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

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '临床实践技巧 · 《加拿大家庭医生》2018', font=font(32), fill=TEAL)
dr.text((70, 130), '顽固性足跟痛：', font=font(56), fill=INK)
dr.text((70, 215), '用大负荷力量训练治疗足底筋膜炎', font=font(56), fill=INK)
dr.line([70, 340, W - 70, 340], fill=(200, 205, 210), width=2)
dr.text((70, 375), 'Caratun R, Rutkowski NA, Finestone HM. Can Fam Physician 2018;64(1):44-46', font=font(28), fill=GREY)
dr.text((70, 430), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1
f1 = relabel(up(raw(150)), [((100, 165, 195, 210), '跟腱', 24, 'l'), ((222, 312, 272, 346), '距骨', 22),
                            ((128, 428, 178, 458), '跟骨', 22), ((596, 426, 646, 456), '跖骨', 22),
                            ((818, 416, 878, 441), '趾骨', 22), ((395, 470, 500, 498), '足底筋膜', 22),
                            ((178, 486, 352, 508), '常见损伤部位', 20, 'l')])
save(capbox(f1, '原文图 1：跟骨附着点是足底筋膜炎最常见的损伤部位（英文缩写已改为中文）'), 2)

# 原文图 2
f2 = up(raw(35)); d = ImageDraw.Draw(f2)
d.rectangle([150, 235, 182, 280], fill=(128, 128, 128))
f2 = relabel(f2, [((200, 225, 330, 285), '跟腱', 34, 'l'), ((158, 515, 222, 556), '跟骨', 28),
                  ((340, 526, 400, 566), '距骨', 28), ((322, 758, 450, 800), '足底筋膜', 28, 'l'),
                  ((545, 866, 612, 906), '跖骨', 28), ((740, 896, 800, 930), '趾骨', 26)])
pad = Image.new('RGB', (1500, f2.height), 'white'); pad.paste(f2, (250, 0))
save(capbox(pad, '原文图 2：提踵时给跟腱加负荷，同时让足趾背伸（绞盘机制），两者叠加，对足底筋膜产生大的张力负荷'), 3)

# 原文图 3：患者指导
blocks = [('准备工作', '① 把一件纯棉 T 恤卷成直径约 2 cm 的圆柱（让足趾能包住它，粗细按脚的大小调整）。\n'
           '② 把 T 恤卷放在台阶边缘往里约 5 cm 处，患脚的足趾踩上去包住它（见图 4）。\n'
           '③ 让台阶边缘正好位于脚长的一半（最好有扶手可扶，防止摔倒）。', LT, TEAL),
          ('动作要求*', '① 提踵：向上至少 5 秒（向心），顶端停 3 秒（等长），再用 5 秒慢慢放下（离心）。\n'
           '② 尽量单腿做，另一条腿离地；做不到或两只脚都有问题，可以双脚一起做。', OR, (200, 110, 30)),
          ('训练安排†', '第 1～4 周：自身体重，每天 1 组 10 次。刚开始可能做不满 10 次，能做几次做几次。\n'
           '第 5～12 周：用最大重复重量，每天 1 组 10 次。最大重复重量指保持动作标准下能举起的最大重量：往背包里装书，'
           '让你刚好在力竭前能完成 10 次。', GR, (40, 130, 60)),
          ('注　释', '* 做练习时会痛。“好的痛”是练的时候痛，但第二天不比之前更痛；“坏的痛”是练完第二天更痛了。'
           '出现“坏的痛”就要减少次数或减轻重量。\n† 用进度表记录每天的提踵练习。', PK, RED)]
save(card(1200, '原文图 3：足底筋膜炎肌力训练方案（患者指导）', blocks), 4)

# 原文图 4：重排为三栏
s = raw(55); cells = []
for i, (y0, y1) in enumerate([(1, 187), (189, 376), (378, 566)]):
    cells.append(s.crop((1, y0, 252, y1)))
cw = 390
tiles = [up(c, cw) for c in cells]
row = Image.new('RGB', (cw * 3 + 30, tiles[0].height + 70), 'white'); dr = ImageDraw.Draw(row)
labs = ['A　足跟最低位', 'B　中立位', 'C　足跟最高位']
for i, t in enumerate(tiles):
    row.paste(t, (i * (cw + 15), 0)); ctext(dr, i * (cw + 15) + cw / 2, t.height + 16, labs[i], font(30))
save(capbox(row, '原文图 4：踩着卷起的 T 恤做单腿提踵（每格左为侧面、右为后面）'), 5)

# 原方案与简化方案对比
W = 1200; im = Image.new('RGB', (W, 1000), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '原始方案与本文简化方案对比（编者整理）', font=font(36), fill='white')
cols = [(30, 260, ''), (270, 600, '原始试验方案（2015）'), (610, 1170, '本文简化方案')]
rows = [('足趾垫', '毛巾卷', 'T 恤卷（直径约 2 cm，更好抓握）'),
        ('节奏', '上 3 秒 · 停 2 秒 · 下 3 秒', '上 5 秒 · 停 3 秒 · 下 5 秒'),
        ('频率', '隔天 1 次', '每天 1 次'),
        ('负荷', '12 次力竭重量×3 组\n→ 10 次×4 组 → 8 次×5 组', '第 1～4 周自身体重\n第 5～12 周 10 次力竭重量'),
        ('每次组数', '3～5 组', '1 组 10 次'),
        ('周期', '3 个月', '至少 3 个月或到不痛为止'),
        ('证据', '随机对照试验，48 人', '作者临床经验，无对照数据')]
y = 100
for x0, x1, t in cols[1:]:
    dr.rounded_rectangle([x0, y, x1, y + 60], 8, fill=TEAL if x0 > 600 else GREY); ctext(dr, (x0 + x1) / 2, y + 14, t, font(30), 'white')
y += 76
for i, (a, b_, c) in enumerate(rows):
    h = 56 + 38 * max(b_.count('\n'), c.count('\n'))
    if i % 2 == 0: dr.rectangle([20, y, W - 20, y + h], fill=(246, 248, 250))
    dr.text((40, y + h / 2 - 16), a, font=font(30), fill=TEAL)
    for (x0, x1, _), t in zip(cols[1:], (b_, c)):
        for j, l in enumerate(t.split('\n')):
            ctext(dr, (x0 + x1) / 2, y + h / 2 - 19 * (t.count('\n') + 1) + 38 * j + 3, l, font(28))
    y += h + 6
dr.text((30, y + 14), '原始方案引自本文参考文献 9 的随机对照试验（2015）；“12 次力竭重量”指刚好能做 12 次的负重', font=font(22), fill=GREY)
save(im.crop((0, 0, W, y + 56)), 6)

c = up(f1, 900); y0 = c.height - 383 - 20
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
