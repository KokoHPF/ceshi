#!/usr/bin/env python3
"""Bianco 等 2019 Mulligan 腓骨动态松动治疗急性外侧踝扭伤：首图中文标题卡；原文图 1～4 直接使用并加中文标注；
结局变化折线图按原文表 4 数值绘制。
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
dr.text((70, 60), '病例系列 · 《加拿大整脊协会杂志》2019', font=font(32), fill=TEAL)
dr.text((70, 140), '运动人群外侧踝扭伤治疗中', font=font(56), fill=INK)
dr.text((70, 220), 'Mulligan 理念的应用：', font=font(56), fill=INK)
dr.text((70, 300), '一项探索性前瞻性病例系列', font=font(44), fill=INK)
dr.line([70, 390, W - 70, 390], fill=(200, 205, 210), width=2)
dr.text((70, 420), 'Bianco L, Fermin S, Oates R, et al. J Can Chiropr Assoc 2019;63(3):154-161', font=font(28), fill=GREY)
dr.text((70, 475), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

f1, f2, f3, f4 = raw(55), raw(56), raw(50), raw(49)


def row(ims, labs, W=1200, gap=10):
    hh = 600; ims = [m.resize((round(m.width * hh / m.height), hh), Image.LANCZOS) for m in ims]
    s = (W - gap * (len(ims) - 1)) / sum(m.width for m in ims)
    ims = [m.resize((round(m.width * s), round(hh * s)), Image.LANCZOS) for m in ims]
    h = ims[0].height; out = Image.new('RGB', (W, h + 52), 'white'); d = ImageDraw.Draw(out); x = 0
    for m, t in zip(ims, labs):
        out.paste(m, (x, 0)); ctext(d, x + m.width / 2, h + 10, t, font(26)); x += m.width + gap
    return out


save(board([row([f3], ['图 3　腓骨动态松动（FMWM）：远端接触，左为侧面、右为后面观'])], '原文图 3：标准腓骨动态松动'), 2)
save(board([row([f4], ['图 4　改良腓骨动态松动（MFMWM）：接触点更靠近端'])], '原文图 4：改良腓骨动态松动'), 3)
save(board([row([f1], ['图 1　负重弓步测试：起始位（左）与终止位（右）']), row([f2], ['图 2　Y 平衡测试：前、后内、后外三个方向'])], '评估：负重弓步测试和 Y 平衡测试'), 4)

# 结局变化（原文表 4）
T = ['首诊前', '首次治疗后', '出院', '1 周随访', '1 个月随访']
fig, axs = plt.subplots(2, 2, figsize=(12, 8.4), dpi=110)
def line(ax, xs, ys, lab, c, mk='o'):
    ax.plot(xs, ys, marker=mk, color=c, lw=2.4, ms=8, label=lab)
    for x, y in zip(xs, ys): ax.text(x, y, f' {y:g}', fontsize=11, va='bottom', color=c)
line(axs[0, 0], [0, 1, 2, 3, 4], [3.33, 0.83, 0, 0, 0], '疼痛评分', '#c0392b'); axs[0, 0].set_ylim(-0.3, 4.5); axs[0, 0].set_title('疼痛评分（0～10）', fontsize=15)
line(axs[0, 1], [0, 2, 3, 4], [82.5, 99.5, 98.2, 100], '足踝功能-日常', '#4c8fbf')
line(axs[0, 1], [0, 2, 3, 4], [65, 88.67, 95, 99.83], '足踝功能-运动', '#f39a2b', 's'); axs[0, 1].set_ylim(55, 108)
axs[0, 1].set_title('足踝能力量表（FAAM，0～100）', fontsize=15); axs[0, 1].legend(fontsize=12, frameon=False, loc='lower right')
line(axs[1, 0], [0, 1, 2, 3, 4], [7, 8.9, 10.42, 10, 10], '负重弓步', '#6aa96a'); axs[1, 0].set_ylim(5, 12); axs[1, 0].set_title('负重弓步测试（cm）', fontsize=15)
line(axs[1, 1], [0, 2, 3, 4], [22.67, 5.33, 3.8, 1.5], '失能', '#8e44ad'); axs[1, 1].set_ylim(-2, 28); axs[1, 1].set_title('运动人群失能量表（越低越好）', fontsize=15)
for ax in axs.flat:
    ax.set_xticks(range(5)); ax.set_xticklabels(T, fontsize=11.5); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=12)
fig.text(0.5, 0.005, '6 名患者的均值，数值取自原文表 4。功能量表和失能量表在首次治疗后未测', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.03, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '6 名患者的结局变化（按原文表 4 绘制）', 1320), 5)

# 封面 900×383：图 3 左半
c = f3; h = round(c.width * 383 / 900); y0 = c.height - h - 4
c.crop((0, y0, c.width, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
