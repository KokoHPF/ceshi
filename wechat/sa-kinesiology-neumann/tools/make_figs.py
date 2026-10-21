#!/usr/bin/env python3
"""Neumann、Camargo 2019 前锯肌运动学（第 1 部分）：首图中文标题卡；原文图 1～3、6 的英文标注（PDF 中为叠加文字层）
按原位置改为中文，图 4、5、8～12 照片直接使用；图 7 照片保留，曲线按原文数据重绘为中文。
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
dr.text((70, 215), '第 1 部分：前锯肌', font=font(54), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 365), 'Neumann DA, Camargo PR. Braz J Phys Ther 2019;23(6):459-466', font=font(28), fill=GREY)
dr.text((70, 420), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1
f = raw(23); c = Image.new('RGB', (f.width + 230, f.height), 'white'); c.paste(f, (230, 0)); dr = ImageDraw.Draw(c)
dr.line([150, 362, 240, 362], fill='black', width=2); dr.text((20, 340), '前锯肌', font=font(40), fill=INK)
save(capbox(up(c, 1000), '原文图 1：前锯肌的附着点和整体力线（起自第 1～9 肋外侧，止于肩胛骨内侧缘前面）'), 2)

# 图 2
f = lab(raw(46), (63, 56, 267, 293), [(112, 151, '上斜方肌'), (106, 192, '中斜方肌'), (114, 246, '下斜方肌'), (182, 256, '前锯肌'),
                                      (176, 150, '三角肌'), (226, 186, '盂肱关节\n外展', (90, 80, 150)), (67, 266, '肩胸关节上回旋', (90, 80, 150))], fs=34)
save(capbox(up(f, 1000), '原文图 2：外展时肩胛上回旋肌与盂肱外展肌的配合（后面观）。主要力偶是前锯肌和斜方肌；'
                         '两个旋转轴：肩胛轴在肩峰附近，盂肱关节轴在肱骨头；粗黑线为各肌肉的内力臂'), 3)

# 图 3
f = lab(raw(61), (123, 57, 481, 308), [(146, 203, '中斜方肌'), (148, 240, '下斜方肌'), (279, 208, '后倾'), (367, 98, '后倾'),
                                      (420, 293, '外旋'), (279, 221, '外旋'), (270, 233, '前锯肌'), (387, 276, '中斜方', RED),
                                      (426, 246, '前锯', RED), (253, 239, '前锯', RED), (413, 152, '前锯', RED), (393, 180, '下斜方', RED),
                                      (196, 252, '下斜方', RED), (204, 214, '中斜方', RED)], fs=26, pad=4)
save(capbox(f, '原文图 3：A 肩胛面外展时，前锯肌与中、下斜方肌控制上回旋肩胛骨后倾和外旋的理论机制；'
               'B 前锯肌和下斜方肌形成力偶，使肩胛骨绕肩锁关节轴（绿点）后倾；C 前锯肌和中斜方肌形成力偶，使肩胛骨绕肩锁关节轴（蓝点）外旋'), 4)

# 图 4、5 徒手肌力测试
save(capbox(row([raw(62), raw(63)]), '原文图 4（左）：肩外展测试，检查者同时抵抗最大用力的肩胛面外展和肩胛上回旋；'
                                       '原文图 5（右）：肩胛前伸测试，检查者抵抗肩胛和整个上肢最大用力的前伸'), 5)

# 图 6
f = lab(raw(79), (143, 56, 444, 160), [(386, 70, '三角肌', RED), (322, 129, '前锯肌', RED)], fs=30)
save(capbox(up(f, 1200), '原文图 6：右侧胸长神经损伤导致前锯肌瘫痪后的翼状肩胛。A 肩胛骨下回旋、前倾、内旋；'
                         'B 缺乏前锯肌的上回旋力（渐隐箭头），肩胛骨无法稳定，三角肌（双向箭头）同时让肩胛下回旋、肱骨部分外展'), 6)

# 图 7：照片 + 重绘曲线
src = raw(94); pa = src.crop((340, 42, 822, 537)); pb = src.crop((1000, 42, 1473, 537))
abd_a = list(range(10, 180, 10)); st_a = [0, 7, 11, 10, 17, 21, 20, 23, 27, 29, 39, 40, 46, 50, 51, 52, 54]
abd_b = list(range(10, 160, 10)); st_b = [-6, -1, 8, -9, -12, -18, -20, -27, -15, 8, 21, 32, 40, 46, 48]
charts = []
for abd, st, t in ((abd_a, st_a, 'A 健康人'), (abd_b, st_b, 'B 前锯肌无力伴肩痛')):
    gh = [a - s for a, s in zip(abd, st)]
    fig, ax = plt.subplots(figsize=(6, 4.6), dpi=110)
    ax.plot(abd, gh, '-o', color='#2b3a9e', ms=4, label='盂肱关节外展')
    ax.plot(abd, st, '-o', color='#2e7d32', ms=4, label='肩胸关节旋转')
    ax.axvline(70, ls='--', color='k', lw=1); ax.axhline(0, color='#888', lw=0.8)
    ax.set_xlim(0, 180); ax.set_ylim(-40, 140); ax.set_xticks(range(10, 180, 20))
    ax.set_xlabel('肩外展（°）', fontsize=13); ax.set_ylabel('角度（°）', fontsize=13); ax.set_title(t, fontsize=14)
    ax.grid(ls=':', color='#bbb'); ax.legend(fontsize=11, loc='upper left', frameon=False)
    fig.tight_layout(); fig.savefig(f'{OUT}/_c.png'); plt.close(fig); charts.append(Image.open(f'{OUT}/_c.png').convert('RGB'))
os.remove(f'{OUT}/_c.png')
pa = lab(pa, (0, 0, pa.width, pa.height), [(300, 400, '肩外展 70°'), (150, 300, '上回旋 20°', (46, 125, 50)), (250, 200, '盂肱 50°', (43, 58, 158))], fs=30)
pb = lab(pb, (0, 0, pb.width, pb.height), [(270, 400, '肩外展 70°'), (120, 140, '下回旋 20°', (46, 125, 50)), (230, 200, '盂肱 90°', (43, 58, 158))], fs=30)
f = stack([row([pa, pb]), row(charts)])
save(capbox(f, '原文图 7：用量角器估计盂肱关节外展（蓝）= 肩外展（横轴）减去肩胸关节旋转（绿）。A 健康男性；B 肩胛运动障碍男性；'
               '两人照片均为肩外展 70°。正值为上回旋，负值为下回旋（曲线按原文数据重绘）'), 7)

# 图 8～12 训练动作
save(capbox(row([raw(92)]), '原文图 8：动态拥抱。用弹力带作阻力，双侧最大程度前伸肩胛'), 8)
save(capbox(row([raw(93)]), '原文图 9：毛巾贴墙滑动。站立位把毛巾沿墙推，从肩中立位滑到最大肩胛面外展并前伸肩胛'), 9)
save(capbox(row([raw(109)]), '原文图 10：前锯肌出拳。A 站立位用弹力带；B 仰卧位举哑铃；C 检查者徒手施加阻力'), 10)
save(capbox(row([raw(110)]), '原文图 11：手撑脚撑的俯卧撑加强（胸廓在固定的肩胛上前伸）。A 起始位；B 终末位；C 在不稳定面上做'), 11)
save(capbox(row([raw(111)]), '原文图 12：肘撑脚撑的俯卧撑加强。A 双侧胸廓在固定肩胛上前伸；B 左侧保持前伸，右侧由检查者抵抗（手臂和肩胛相对固定的胸廓前伸）'), 12)

c = raw(111); c = up(c, 900); y0 = max(0, (c.height - 383) // 2); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
