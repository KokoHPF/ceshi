#!/usr/bin/env python3
"""Chivers & Howitt 2009 膝关节半月板解剖与体格检查综述：首图中文标题卡；原文图 1 的英文标签原位改为中文，图 2～11 照片直接使用并配中文图注；
各检查的敏感度、特异度按原文正文数字用中文绘图；检查方法整理为中文卡片。
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
dr.text((70, 50), '叙述性综述 · 《加拿大脊骨神经医学会杂志》2009', font=font(32), fill=TEAL)
dr.text((70, 135), '膝关节半月板的解剖与体格检查：', font=font(56), fill=INK)
dr.text((70, 215), '骨科文献的叙述性综述', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Chivers MD, Howitt SD.', font=font(28), fill=GREY)
dr.text((70, 405), 'J Can Chiropr Assoc. 2009;53(4):319-333', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


def tag(im, t, fs=None):
    im = im.copy(); dr = ImageDraw.Draw(im); f = font(fs or max(22, im.width // 16)); w = dr.textlength(t, font=f)
    dr.rounded_rectangle([8, 8, 26 + w, 20 + f.size], 8, fill=(255, 255, 255), outline=(200, 200, 200)); dr.text((17, 12), t, font=f, fill=INK); return im


def boxes(im, items):
    s = im.width / 1000; d = ImageDraw.Draw(im)
    for box, t, fs in items:
        b = [int(v * s) for v in box]; d.rectangle(b, fill='white'); f = font(fs * s); lh = fs * s * 1.3
        lines = t.split('\n'); y0 = (b[1] + b[3]) / 2 - lh * len(lines) / 2
        for i, l in enumerate(lines): d.text(((b[0] + b[2]) / 2 - d.textlength(l, font=f) / 2, y0 + i * lh), l, font=f, fill='black')
    return im


f1 = boxes(raw(4), [((5, 160, 133, 226), '外侧\n半月板', 24), ((866, 158, 996, 224), '内侧\n半月板', 24)])
save(capbox(f1, '原文图 1  从上方俯视胫骨平台上的半月板：内侧半月板呈“C”形，外侧半月板更接近“O”形（图片由 Primal Pictures 提供）'), 2)

save(capbox(row([tag(raw(9), '图 2'), tag(raw(8), '图 3')]),
            '原文图 2（左）  半月板增大了凸的股骨髁与平坦的胫骨平台之间的接触面积（右侧灰色楔形为半月板）。'
            '原文图 3（右）  半月板的血供分区：深灰框为红区（外周 10%～30%，有血供），浅灰框为红白区（血供很少），白框为白区（内 1/3，无血供，靠滑液营养）'), 3)

PAIRS = [((16, 17), ('图 4  Apley 试验', '图 5  Anderson 内外侧研磨试验'),
          '原文图 4（左）  Apley 试验：俯卧屈膝 90°，检查者用膝压住患者大腿后侧，先牵拉再加压下旋转小腿，加压时疼痛加重为阳性。'
          '原文图 5（右）  Anderson 内外侧研磨试验：仰卧，检查者把小腿夹在躯干和上臂之间，拇指和食指放在前侧关节线上，屈膝到 45° 时加外翻应力、伸膝时加内翻应力，画圈并逐渐加大应力'),
         ((21, 22), ('图 6  McMurray 试验', '图 7  弹回试验'),
          '原文图 6（左）  McMurray 试验：仰卧，膝完全屈曲，握住足跟旋转小腿，再从最大屈曲伸到 90°，外旋查内侧、内旋查外侧半月板后部。'
          '原文图 7（右）  弹回试验（强制过伸）：仰卧，屈膝后让膝被动伸直，应“弹回”到完全伸直、终末感清脆；伸不直或终末感发软为阳性'),
         ((26, 27), ('图 8  轴向负荷轴移试验', '图 9  KKU 加压旋转试验'),
          '原文图 8（左）  轴向负荷轴移试验：仰卧伸膝，小腿完全内旋并在胫骨近端加外翻力，沿胫骨轴向加压的同时屈膝到 30°～45°，再在加压下伸回，关节线特定疼痛或弹响为阳性。'
          '原文图 9（右）  KKU 膝关节加压旋转试验：仰卧，握住踝部屈膝，另一手放在关节线上，把胫骨压向股骨后内旋、外旋，在 120°、90°、60°、30°、0° 各做一次'),
         ((31, 32), ('图 10a  Ege 试验（内旋）', '图 10b  Ege 试验（外旋）'),
          '原文图 10  Ege 试验：站立伸膝，两脚相距 40 cm。查外侧半月板时双小腿最大内旋（左），查内侧半月板时最大外旋（右），然后下蹲再慢慢站起，患者感到疼痛和（或）弹响为阳性'),
         ((33, 34), ('图 11a  Thessaly 试验（内旋）', '图 11b  Thessaly 试验（外旋）'),
          '原文图 11  Thessaly 试验：检查者扶住患者伸出的双手，患者单腿站立、膝屈 5°，带动身体向内（左）、向外（右）旋转各 3 次，再在屈膝 20° 重复；关节线不适、绞锁或卡住感为阳性')]
n = 4
for (a, b2), (ta, tb), c in PAIRS:
    save(capbox(row([tag(raw(a), ta, 26), tag(raw(b2), tb, 26)]), c), n); n += 1

# 检查速查卡
save(card(1200, '9 种半月板检查：怎么做、什么算阳性', [
    ('关节线压痛（JLT）', '屈膝并内旋或外旋小腿，便于摸到内、外侧半月板外缘；按压“红区”所在的关节线，局部压痛为阳性。', LT, TEAL),
    ('McMurray 试验', '膝完全屈曲 → 旋转小腿 → 保持旋转从最大屈曲伸到 90°；外旋查内侧、内旋查外侧。原始描述的阳性是“弹响 + 患者说和以前打软腿的感觉一样”。', LT, TEAL),
    ('Apley 试验', '俯卧屈膝 90°：先单纯旋转 → 牵拉下旋转（痛加重提示韧带）→ 加压下旋转（痛加重提示半月板）。', OR, (200, 120, 0)),
    ('Anderson 内外侧研磨试验', '仰卧，屈膝到 45° 时加外翻、伸膝时加内翻，画圈并逐渐加大应力。', OR, (200, 120, 0)),
    ('弹回试验 / 强制过伸', '被动伸膝应“弹回”到完全伸直；伸不直、终末感发软或强制过伸被挡住为阳性。伸不直要警惕移位的桶柄状撕裂，需尽快转骨科。', PK, RED),
    ('轴向负荷轴移试验', '伸膝位小腿内旋 + 外翻 + 轴向加压，屈到 30°～45° 再伸回；关节线疼痛或弹响为阳性。', GR, (0, 120, 60)),
    ('KKU 加压旋转试验', '胫骨压向股骨后内、外旋，在 120°、90°、60°、30°、0° 依次重复；关节线痛、弹响或摩擦感为阳性。', GR, (0, 120, 60)),
    ('Ege 试验（负重）', '两脚相距 40 cm，外旋下蹲查内侧、内旋下蹲查外侧，慢慢站起；疼痛和（或）弹响为阳性。', (240, 240, 248), (90, 70, 170)),
    ('Thessaly 试验（负重）', '扶手单腿站，屈膝 5° 和 20° 各向内、外旋转身体 3 次；关节线不适、绞锁或卡住为阳性。', (240, 240, 248), (90, 70, 170)),
]), 9)

# 敏感度/特异度点图
D = [  # 检查, 研究, 敏感度, 特异度
    ('McMurray', 'Kurosaka 1999', 37, 77), ('McMurray', 'Corea 1994', 59, 93), ('McMurray', 'Akseki 2005 内侧', 67, 69), ('McMurray', 'Akseki 2005 外侧', 53, 88),
    ('McMurray', 'Karachalios 2005 内侧', 48, 94), ('McMurray', 'Karachalios 2005 外侧', 65, 86), ('McMurray', 'Surachai 2007', 70, 82), ('McMurray', 'Lowery 2006', 20, 96),
    ('McMurray', 'Scholten 2001 合并', 48, 86), ('McMurray', 'Solomon 2001 合并', 53, 59),
    ('关节线压痛', 'Wadley 2007', 84.6, 31.2), ('关节线压痛', 'Fowler 1989', 85, 29), ('关节线压痛', 'Kurosaka 1999', 55, 67), ('关节线压痛', 'Karachalios 2005 内侧', 71, 87),
    ('关节线压痛', 'Karachalios 2005 外侧', 78, 90), ('关节线压痛', 'Lowery 2006', 65, 65), ('关节线压痛', 'Scholten 2001 合并', 77, 41), ('关节线压痛', 'Solomon 2001 合并', 79, 15),
    ('Apley', 'Fowler 1989', 16, 80), ('Apley', 'Kurosaka 1999', 13, 90), ('Apley', 'Karachalios 2005 内侧', 41, 93), ('Apley', 'Karachalios 2005 外侧', 41, 86),
    ('强制过伸', 'Fowler 1989', 44, 86), ('强制过伸', 'Kurosaka 1999', 47, 67), ('强制过伸', 'Lowery 2006', 36, 86),
    ('Thessaly 20°', 'Karachalios 2005 内侧', 89, 97), ('Thessaly 20°', 'Karachalios 2005 外侧', 92, 96), ('Thessaly 5°', 'Karachalios 2005 内侧', 66, 96), ('Thessaly 5°', 'Karachalios 2005 外侧', 81, 91),
    ('Ege', 'Akseki 2005 内侧', 67, 81), ('Ege', 'Akseki 2005 外侧', 64, 90), ('KKU', 'Surachai 2007', 86, 88), ('轴向负荷轴移', 'Kurosaka 1999', 71, 83),
]
fig, ax = plt.subplots(figsize=(12, 13), dpi=100)
y = len(D) - 1; yt = []; prev = None
for t, s, se, sp in D:
    if prev and t != prev: y -= .6; ax.axhline(y + .3, color='#ddd', lw=1)
    ax.plot([se, sp], [y, y], color='#ccc', lw=2, zorder=1)
    ax.scatter(se, y, color='#00788c', s=70, zorder=2); ax.scatter(sp, y, color='#be2832', marker='s', s=60, zorder=2)
    yt.append((y, f'{t}｜{s}')); y -= 1; prev = t
ax.set_yticks([a for a, _ in yt]); ax.set_yticklabels([b for _, b in yt], fontsize=11)
ax.set_xlim(0, 100); ax.set_xlabel('%', fontsize=12); ax.grid(axis='x', alpha=.3); ax.spines[['top', 'right']].set_visible(False)
ax.scatter([], [], color='#00788c', s=70, label='敏感度'); ax.scatter([], [], color='#be2832', marker='s', s=60, label='特异度')
ax.legend(loc='lower right', fontsize=12, frameon=True)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '编者根据原文正文数字绘图：各检查在不同研究中的敏感度（圆点）和特异度（方块）。'
                                          '注意 Karachalios 2005 以磁共振为参照、并纳入 197 名健康志愿者，数值可能偏高'), 10)

# 综合检查
fig, ax = plt.subplots(figsize=(12, 5), dpi=100)
C = [('Oberlander 1993 内侧', 87, 93), ('Oberlander 1993 外侧', 81, 93), ('O’Shea 1996 内侧', 88, 77), ('O’Shea 1996 外侧', 51, 90),
     ('Muellner 1997 内侧', 100, 76), ('Muellner 1997 外侧', 92, 98), ('Solomon 2001 合并', 77, 91), ('Lowery 2006 四项全阳性', 11, 99)]
x = np.arange(len(C)); w = .38
b1 = ax.bar(x - w / 2, [c[1] for c in C], w, color='#00788c', label='敏感度'); b2 = ax.bar(x + w / 2, [c[2] for c in C], w, color='#be2832', label='特异度')
for bs in (b1, b2):
    for r in bs: ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 1.5, f'{int(r.get_height())}', ha='center', fontsize=11)
ax.set_xticks(x); ax.set_xticklabels([c[0].replace(' ', '\n', 1) for c in C], fontsize=11); ax.set_ylim(0, 112); ax.set_ylabel('%', fontsize=12)
ax.legend(frameon=False, fontsize=12, ncol=2, loc='upper right'); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '编者根据原文数字绘图：病史 + 多项检查的综合评估。多数研究的敏感度、特异度明显高于单项检查；'
                                          'Lowery 2006 要求四项检查全阳性加机械症状时，特异度 99%，但敏感度只有 11%'), 11)

# 封面：原文图 6 McMurray 试验照片裁成 900:383
c = raw(21).crop((0, 110, 525, 110 + round(525 * 383 / 900))).resize((900, 383), Image.LANCZOS)
c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
