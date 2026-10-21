#!/usr/bin/env python3
"""Selkowitz 等 2013 JOSPT 哪些训练能靶向臀肌、同时尽量少激活阔筋膜张肌（细丝电极肌电）：首图为原题直译标题卡；
原文图 1～11 直接用原图照片（照片内无英文，图 9 的步序箭头和数字保留），英文图注译成中文放在照片下方；
肌电对比图和选动作卡为编者根据原文表 1、表 2 整理。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
Z = 4
K, G, R = (0, 0, 0), (94, 94, 94), (255, 38, 0)
doc = pymupdf.open(PDF)
PUNC = '，。；、：）”'


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=90)


def titled(im, t, W=1200):
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30 and ch not in PUNC:
            k = len(line)
            while ch.isascii() and ch.isalnum() and k and line[k - 1].isascii() and line[k - 1].isalnum(): k -= 1
            if not k: k = len(line)
            lines.append(line[:k]); line = line[k:] + ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in PUNC: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def phases(title, S, n, fs=24):
    W = 1200; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im); y = 20
    for t, bg, c, items in S:
        h = 66 + sum(para_h(s, fs, 1030 - fs * 1.1, gap=8) + 10 for s in items)
        dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
        yy = y + 62
        for s in items: yy = bullet(dr, 70, yy, s, fs, 1060, gap=8) + 10
        y += h + 16
    save(titled(im.crop((0, 0, W, y)), title), n)


import io

# 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '研究报告 · J Orthop Sports Phys Ther 2013', font=font(32), fill=TEAL)
for i, t in enumerate(['哪些训练能靶向臀肌，同时尽量少激活', '阔筋膜张肌？细丝电极肌电评估']):
    dr.text((70, 130 + i * 72), t, font=font(50), fill=INK)
dr.text((70, 300), 'Which Exercises Target the Gluteal Muscles While Minimizing Activation', font=font(28), fill=GREY)
dr.text((70, 338), 'of the Tensor Fascia Lata? Electromyographic Assessment Using Fine-Wire Electrodes', font=font(26), fill=GREY)
dr.line([70, 420, W - 70, 420], fill=(200, 205, 210), width=2)
dr.text((70, 450), 'Selkowitz DM, Beneck GJ, Powers CM. J Orthop Sports Phys Ther.', font=font(30), fill=GREY)
dr.text((70, 494), '2013;43(2):54-64. doi:10.2519/jospt.2013.4116', font=font(30), fill=GREY)
dr.text((70, 550), '美国西部健康科学大学 · 加州州立大学长滩分校 · 南加州大学', font=font(26), fill=GREY)
dr.text((70, 612), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


def photo(pno):
    pg = doc[pno]; x = pg.get_images()[0][0]
    if pg.get_drawings():  # 图 9 的箭头和步序数字是矢量图层，整块渲染
        r = pg.get_image_rects(x)[0]; pix = pg.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=r)
        return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    return Image.open(io.BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def row(items, title, n):
    k = len(items); gap = 15; tw = (1200 - gap * (k - 1)) // k; tiles = []
    for pno, t in items:
        ph = photo(pno); ph = ph.resize((tw, round(ph.height * tw / ph.width)), Image.LANCZOS); tiles.append((ph, t))
    hh = max(ph.height for ph, _ in tiles); ch = max(para_h(t, 26, tw - 24, gap=8) for _, t in tiles)
    im = Image.new('RGB', (1200, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im)
    for i, (ph, t) in enumerate(tiles):
        x = i * (tw + gap); im.paste(ph, (x, hh - ph.height))
        dr.rectangle([x, hh, x + tw, hh + ch + 20], fill=(232, 232, 232)); para(dr, x + 12, hh + 12, t, 26, tw - 24, gap=8)
    save(titled(im, title), n)


F_ZH = {30: '原文图 1　侧卧髋外展（ABD）', 31: '原文图 2　侧卧蚌式开合（CLAM）',
        32: '原文图 3　双腿臀桥（BiBRG）', 33: '原文图 4　单腿臀桥（UniBRG）',
        34: '原文图 5　肘撑四点跪伸髋，膝随之伸直（再回到屈膝位）（QKE）', 35: '原文图 6　肘撑四点跪伸髋，膝全程保持屈曲（QKF）',
        36: '原文图 7　向前弓步（LUNGE）', 37: '原文图 8　深蹲（SQUAT）',
        38: '原文图 9　侧向走（SIDE-STEP），向右和向左。向左走时左腿先迈（1），向右走时右腿先迈（3）',
        39: '原文图 10　骨盆上提（HIKE）', 40: '原文图 11　向前上台阶（STEP-UP）'}
row([(30, F_ZH[30]), (31, F_ZH[31])], '原文图 1～2　侧卧位动作（图注译成中文）', 2)
row([(32, F_ZH[32]), (33, F_ZH[33])], '原文图 3～4　臀桥（图注译成中文）', 3)
row([(34, F_ZH[34]), (35, F_ZH[35])], '原文图 5～6　肘撑四点跪伸髋（图注译成中文）', 4)
row([(36, F_ZH[36]), (37, F_ZH[37]), (38, F_ZH[38])], '原文图 7～9　站立位动作（图注译成中文）', 5)
row([(39, F_ZH[39]), (40, F_ZH[40])], '原文图 10～11　单腿负重动作（图注译成中文）', 6)

# 编者图：表 1 + 表 2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
D = [('蚌式开合 *', 11.4, 26.7, 43.6, 115), ('弹力带侧向走 *', 13.1, 30.2, 27.4, 64), ('单腿臀桥 *', 18.1, 30.9, 34.6, 59),
     ('四点跪伸髋·伸膝 *', 15.6, 27.3, 28.5, 50), ('四点跪伸髋·屈膝 *', 18.7, 30.9, 30.1, 50), ('侧卧髋外展', 32.3, 43.5, 23.7, 38),
     ('向前上台阶', 21.4, 29.5, 22.8, 32), ('双腿臀桥 *', 8.2, 15.0, 17.4, 32), ('深蹲 *', 4.6, 9.7, 12.9, 28),
     ('骨盆上提', 31.4, 37.7, 17.7, 28), ('向前弓步', 21.6, 19.3, 20.1, 18)]
fig, ax = plt.subplots(figsize=(12, 10), dpi=100); h = 0.26
for k, (lab, col) in enumerate([('阔筋膜张肌', '#c0392b'), ('臀中肌', '#2e86c1'), ('臀大肌上部', '#1e8449')]):
    ys = [i + (k - 1) * h for i in range(len(D))]; vs = [d[1 + k] for d in D]
    ax.barh(ys, vs, h, color=col, label=lab)
    for y, v in zip(ys, vs): ax.text(v + 0.6, y, f'{v:g}', va='center', fontsize=11)
for i, d in enumerate(D): ax.text(57, i, f'GTA {d[4]}', va='center', fontsize=15, color='#1f3a93' if d[4] >= 50 else '#888', fontweight='bold')
ax.set_yticks(range(len(D))); ax.set_yticklabels([d[0] for d in D], fontsize=15); ax.invert_yaxis()
ax.set_xlim(0, 65); ax.set_xlabel('平均 %MVIC（n = 20 名健康人）', fontsize=14)
ax.axhline(4.5, color='#999', ls='--', lw=1)
ax.legend(fontsize=14, loc='lower center', bbox_to_anchor=(0.45, 1.0), ncol=3, frameon=False); ax.spines[['top', 'right']].set_visible(False)
fig.text(0.02, 0.01, '* 两块臀肌都显著高于阔筋膜张肌；按“臀肌-阔筋膜张肌激活指数（GTA）”从高到低排序，虚线以上 GTA ≥ 50', fontsize=12, color='#555', va='bottom')
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f'{OUT}/_c.png'); plt.close(fig)
import os
c = Image.open(f'{OUT}/_c.png').convert('RGB'); os.remove(f'{OUT}/_c.png')
save(titled(c, '11 个动作的臀肌和阔筋膜张肌激活（编者根据原文表 1、表 2 整理）'), 7)

phases('想练臀、少用阔筋膜张肌，怎么选（编者根据原文整理）', [
    ('首选：GTA ≥ 50', GR, (40, 120, 60), ['蚌式开合（加弹力带）GTA 115：臀大肌上部 43.6%，阔筋膜张肌只有 11.4%',
        '弹力带深蹲位侧向走 64、单腿臀桥 59、肘撑四点跪伸髋（伸膝或屈膝）50', '这 5 个动作两块臀肌都 > 25% MVIC，阔筋膜张肌都 < 20% MVIC']),
    ('比例好但强度低：加负荷', LT, TEAL, ['双腿臀桥、深蹲：臀肌显著高于阔筋膜张肌，但绝对激活低（深蹲臀中肌 9.7%）',
        '作者认为加大阻力后比例不变、激活升高，GTA 会随之提高']),
    ('阔筋膜张肌也很活跃：慎选', PK, RED, ['侧卧髋外展：臀中肌最高（43.5%），但阔筋膜张肌 32.3%、臀大肌上部反而低于它',
        '骨盆上提：臀中肌与阔筋膜张肌无差异，臀大肌上部显著低于阔筋膜张肌', '弓步、上台阶：三块肌肉之间无显著差异']),
    ('GTA 指数怎么算', OR, (180, 90, 20), ['GTA =［(臀中肌 ÷ 阔筋膜张肌) × 臀中肌 + (臀大肌上部 ÷ 阔筋膜张肌) × 臀大肌上部］÷ 2',
        '既看臀肌相对阔筋膜张肌的比例，也看臀肌本身激活高不高；50 的分界是作者按数据聚集情况定的'])], 8)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), '臀肌训练 · 细丝肌电 · JOSPT', font=font(34), fill=TEAL)
dr.text((50, 128), '练臀别让阔筋膜张肌抢活', font=font(52), fill=INK)
dr.text((50, 214), '11 个动作谁最“纯”？', font=font(52), fill=INK)
dr.text((50, 318), '蚌式开合 · 侧向走 · 单腿臀桥 · 四点跪伸髋', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
