#!/usr/bin/env python3
"""Meister 等 2025 尺侧副韧带“混合”重建术与康复：首图中文标题卡；原文图 1～26 照片直接使用（相邻两三张按等高拼排），加中文图注；
康复时间线卡为编者根据原文表 2 整理。原文的手术视频封面（英文）未使用。
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
dr.text((70, 50), '临床观点 · 《国际运动物理治疗杂志》2025', font=font(32), fill=TEAL)
dr.text((70, 135), '过头运动员的尺侧副韧带', font=font(56), fill=INK)
dr.text((70, 215), '混合重建手术与康复', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Meister KM, Evans D, Wilk KE, Arrigo CA.', font=font(28), fill=GREY)
dr.text((70, 405), 'Int J Sports Phys Ther. 2025;20(2):293-305', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文重排，仅作学术交流（原文 CC BY-NC 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

R = lambda *xs: row([raw(x) for x in xs])
save(capbox(raw(59), '原文图 1  切取掌长肌腱并制备移植物：腕横纹处 1 cm 横切口，编织缝合后用肌腱剥离器取腱，去除肌腹、另一端再缝合成管状'), 2)
save(capbox(R(60, 61), '原文图 2（左）皮肤切口标记；原文图 3（右）初始皮肤切口：自内上髁上缘向远端，长约 6 cm'), 3)
save(capbox(R(70, 71), '原文图 4（左）在内上髁后缘游离并抬起尺神经，部分松解内侧肌间隔；原文图 5（右）沿指浅屈肌与尺侧腕屈肌间隙纵行劈开屈肌群后缝并掀起'), 4)
save(capbox(R(72, 73), '原文图 6（左）实心箭头所指为已减压的尺神经；原文图 7（右）纵行劈开韧带，可见近端撕裂'), 5)
save(capbox(R(74, 86), '原文图 8（左）用导向器和 3.5 mm 钻头在高耸结节两侧钻远端骨道；原文图 9（右）用弯针引过缝线'), 6)
save(capbox(R(87, 88), '原文图 10（左）放置旋入式锚钉（Swivel Lock）；原文图 11（右）内支架方向与肌腱骨道对齐（原文这两张图是同一张照片）'), 7)
save(capbox(R(89, 90), '原文图 12（左）内上髁起始钻孔（图注写 2.7 mm，正文为 2.5 mm）；原文图 13（右）用 4.5 mm 钻头扩钻，制作肱骨近端骨窝'), 8)
save(capbox(R(91, 101), '原文图 14（左）经内上髁的两条分叉近端骨道；原文图 15（右）远端修复：肌腱移植物穿过远端骨道'), 9)
save(capbox(R(102, 103), '原文图 16（左）肌腱移植物穿过远端骨道；原文图 17（右）对内支架和肌腱移植物加张力并打结（先拉紧内支架）'), 10)
save(capbox(R(104, 105), '原文图 18（左）内支架两臂和肌腱两臂都已引入肱骨骨道、加张力并打结；原文图 19（右）在近端移植物上方缝合残留的自体韧带，并把肌腱移植物与自体韧带、内支架缝合在一起'), 11)
save(capbox(R(106, 116), '原文图 20（左）缝合筋膜；原文图 21（右）皮内缝合皮肤'), 12)

blocks = [('保护期：0～3 周', '支具锁定 90°（第 1 周）→ 第 1 周后 30°～90° → 之后每周屈伸各放开 10°\n肩、腕、手主动活动和握力练习；亚极量等长收缩；手法节律性稳定和肩胛控制（都在支具锁定 90° 下做）\n第 2 周拆线，开始卧式单车、步行、下肢和核心训练\n第 3 周开始手法抗阻的肩内旋 / 外旋等长收缩', LT, TEAL),
          ('中期：3～12 周', '继续逐步放开支具；轻柔手法，避免激进被动活动；活动度停滞立即联系医生\n第 6 周去支具，开始渐进抗阻：俯卧 T、I、Y、W，侧卧外旋，肩胛面上举，弹力带内旋等\n第 10 周开始轻负荷复合动作：地板哑铃卧推、俯身哑铃划船、绳索高位划船', GR, (40, 130, 60)),
          ('强化期：12 周～6 个月', '12 周：不限制的力量房训练，但避免外翻负荷\n双手增强式（药球胸前传、劈砍、过顶侧抛等）：高中 / 大学 15 周，职业 17 周\n单手增强式（90/90 反弹抛、过顶拍墙、减速、俯卧翻腕）：高中 / 大学 17 周，职业 19～20 周\n起始量 2～3 组 × 12～15 次', OR, (200, 110, 30)),
          ('回归投掷期', '高中 / 大学：5 个月开始远距离抛（ITP）→ 约 8 个月投手丘 → 约 12 个月完全回归\n职业：6 个月开始远距离抛 → 约 9 个月投手丘 → 约 14 个月完全回归\n远投 45 → 60 → 75 → 90 → 105 → 120 英尺，按测速枪速度区间控制强度，穿插减量期', PK, RED)]
save(card(1200, '康复时间线（编者根据原文表 2 和正文整理）', blocks), 13)

save(capbox(R(136, 137), '原文图 22（左）术后肘关节可调角度支具；原文图 23（右）在术后支具内做被动活动'), 14)
save(capbox(R(145, 146, 147), '原文图 24（左）肘和肩的被动活动；原文图 25（中）双手药球胸前传墙；原文图 26（右）单手过顶拍墙'), 15)

c = raw(145); c = c.crop((0, 560, 801, 560 + 341)).resize((900, 383), Image.LANCZOS)
c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
