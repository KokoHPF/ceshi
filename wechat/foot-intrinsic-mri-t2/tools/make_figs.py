#!/usr/bin/env python3
"""Gooding 等 2016 T2 磁共振观察足内在肌运动后激活：首图中文标题卡；原文图 1 按页面渲染裁切（直接提取的图像为反色）；图 2 磁共振加中文分图标签；
图 3 热图的英文缩写按 OCR 定位改为中文并配中文色标；图 4 解剖热图直接使用并在图注说明数字编号；图 5 森林图按原文表格数据用中文重绘。
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
dr.text((70, 50), '原创研究 · 《运动防护杂志》2016', font=font(32), fill=TEAL)
dr.text((70, 135), '特定运动中的足内在肌激活：', font=font(56), fill=INK)
dr.text((70, 215), '一项 T2 时间磁共振研究', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Gooding TM, Feger MA, Hart JM, Hertel J.', font=font(28), fill=GREY)
dr.text((70, 405), 'J Athl Train. 2016;51(8):644-650', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


def render(pn, clip, dpi=300):
    pix = doc[pn].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*clip)); return Image.open(BytesIO(pix.tobytes('png'))).convert('RGB')


def tag(im, t, fs=None):
    im = im.copy(); dr = ImageDraw.Draw(im); f = font(fs or max(22, im.width // 16)); w = dr.textlength(t, font=f)
    dr.rounded_rectangle([8, 8, 26 + w, 20 + f.size], 8, fill=(255, 255, 255), outline=(200, 200, 200)); dr.text((17, 12), t, font=f, fill=INK); return im


f1 = render(1, (121, 42, 496, 280)); w, h = f1.size
q = [f1.crop((0, 0, w // 2, h // 2)), f1.crop((w // 2, 0, w, h // 2)), f1.crop((0, h // 2, w // 2, h)), f1.crop((w // 2, h // 2, w, h))]
names = ['A 短足', 'B 脚趾张开', 'C 大脚趾伸展', 'D 第 2～5 趾伸展']
save(capbox(stack([row([tag(q[0], names[0]), tag(q[1], names[1])]), row([tag(q[2], names[2]), tag(q[3], names[3])])]),
            '原文图 1  四个足内在肌运动：A 短足；B 脚趾张开；C 大脚趾伸展；D 第 2～5 趾伸展'), 2)

pan = [stack([raw(13), raw(14)], gap=0), stack([raw(15), raw(16)], gap=0), stack([raw(17), raw(18)], gap=0)]
save(capbox(row([tag(pan[0], 'A 肌肉轮廓'), tag(pan[1], 'B 运动前'), tag(pan[2], 'C 运动后')]),
            '原文图 2  分析示例：A 勾画各肌肉的轮廓（绿线）；B 运动前的激活水平；C 运动后的激活水平。红色为超过阈值（静息 T2 均值 + 1 个标准差）的“激活”像素'), 3)

ZH = {'ABH': '拇展肌', 'FDB': '趾短屈肌', 'ADM': '小趾展肌', 'QP': '足底方肌', 'FDM': '小趾短屈肌', 'AHO': '拇收肌斜头', 'FHB': '拇短屈肌', 'I&L': '骨间肌\n蚓状肌'}


def heat(x, label):
    import json
    rows = json.load(open(f'{SRC}/o{x}.json')); ex = []
    for r in rows:
        t = r[4]
        if t in ZH:
            y0, y1 = r[1] - 18, r[3] + 18
            ex.append(((2, y0, 128, y1), ZH[t], {'fs': 19 if '\n' not in ZH[t] else 16, 'fg': INK, 'bg': (214, 220, 224)}))
        elif t == 'Avg': ex.append(((r[0] - 10, r[1] - 6, r[2] + 10, r[3] + 6), '均值', {'fs': 20, 'fg': INK, 'bg': (214, 220, 224)}))
        elif t == '8#': ex.append(((r[0] - 6, r[1] - 4, r[2] + 6, r[3] + 4), '#8', {'fs': 20, 'fg': INK, 'bg': (214, 220, 224)}))
    im, _ = zh.apply(raw(x), f'{SRC}/o{x}.json', [], W=900, extra=ex)
    return tag(im.crop((0, 80, im.width, im.height)), label, fs=30)


cb = raw(55); cb = cb.resize((round(cb.width * 1300 / cb.height), 1300), Image.LANCZOS)
lab = Image.new('RGB', (60, 1300), 'white'); d = ImageDraw.Draw(lab); f = font(26); t = '激活增加百分比（%）'
tw = d.textlength(t, font=f); tmp = Image.new('RGB', (int(tw) + 10, 40), 'white'); ImageDraw.Draw(tmp).text((5, 4), t, font=f, fill=INK)
lab.paste(tmp.rotate(90, expand=True), (10, 650 - int(tw) // 2))
g = stack([row([heat(30, 'A 短足'), heat(32, 'B 脚趾张开')], W=1600), row([heat(31, 'C 大脚趾伸展'), heat(29, 'D 第 2～5 趾伸展')], W=1600)])
cb2 = cb.resize((cb.width * g.height // cb.height, g.height)); lab2 = lab.resize((60, g.height))
full = Image.new('RGB', (g.width + cb2.width + 80, g.height), 'white'); full.paste(g, (0, 0)); full.paste(cb2, (g.width + 10, 0)); full.paste(lab2, (g.width + cb2.width + 15, 0))
save(capbox(full, '原文图 3  每位受试者（#1～#8）各肌肉的激活增加百分比热图及均值，右侧色标 0～50%，红色低、蓝色高。'
                  '注意 A、B 两幅只有 7 名受试者'), 4)

g = stack([row([tag(raw(38), 'A 短足'), tag(raw(39), 'B 脚趾张开')]), row([tag(raw(40), 'C 大脚趾伸展'), tag(raw(41), 'D 第 2～5 趾伸展')])])
cb2 = cb.resize((cb.width * g.height // cb.height, g.height)); lab2 = lab.resize((60, g.height))
full = Image.new('RGB', (g.width + cb2.width + 80, g.height), 'white'); full.paste(g, (0, 0)); full.paste(cb2, (g.width + 10, 0)); full.paste(lab2, (g.width + cb2.width + 15, 0))
save(capbox(full, '原文图 4  各运动的组均值激活增加，按色标涂在足底解剖图上（每组 4 幅从左到右为足底第 1～4 层）。'
                  '图中编号：1 拇展肌；2 趾短屈肌；3 小趾展肌；4 足底方肌；5 蚓状肌；6 小趾短屈肌；7a 拇收肌斜头；7b 拇收肌横头（未分析）；8 拇短屈肌；9 骨间肌。'
                  '解剖底图经许可引自 BMJ 出版集团'), 5)

MU = ['拇展肌', '趾短屈肌', '小趾展肌', '足底方肌', '小趾短屈肌', '拇收肌斜头', '拇短屈肌', '骨间肌和蚓状肌']
T = {'短足': [(29.7, 16.8, 42.6), (24.8, 11.8, 37.9), (34.9, 26.7, 43.0), (19.0, 12.0, 26.0), (23.4, 4.0, 42.9), (22.4, 4.5, 40.3), (20.8, 7.6, 33.9), (16.7, 4.5, 28.8)],
     '脚趾张开': [(18.9, 7.4, 30.5), (27.0, 18.3, 35.7), (35.2, 23.6, 46.9), (25.4, 12.6, 38.2), (30.2, 9.7, 50.6), (31.5, 17.2, 45.8), (29.5, 20.8, 38.3), (17.3, 6.5, 28.0)],
     '大脚趾伸展': [(16.9, 8.3, 25.5), (18.1, 9.5, 26.7), (14.1, 3.9, 24.2), (13.9, 5.8, 21.9), (16.3, 6.5, 26.1), (15.9, 5.9, 26.0), (13.1, 4.3, 22.0), (15.0, 9.3, 20.7)],
     '第 2～5 趾伸展': [(16.5, 5.8, 27.2), (15.1, 5.4, 24.7), (22.5, 10.0, 35.1), (17.0, 4.7, 29.3), (10.3, 4.9, 15.7), (17.6, 7.4, 27.8), (20.2, 9.6, 30.7), (8.9, 3.9, 13.9)]}
fig, axs = plt.subplots(2, 2, figsize=(12, 9), dpi=100, sharex=True)
for a, (nm, v) in zip(axs.flat, T.items()):
    y = np.arange(8)[::-1]
    for yy, (m, lo, hi) in zip(y, v):
        a.plot([lo, hi], [yy, yy], color='#555', lw=1.2); a.plot([lo, lo], [yy - .15, yy + .15], color='#555'); a.plot([hi, hi], [yy - .15, yy + .15], color='#555')
        a.plot(m, yy, 's', color='#00788c', ms=9); a.text(hi + 1, yy, f'{m}', va='center', fontsize=10, color='#333')
    a.set_yticks(y); a.set_yticklabels(MU, fontsize=12); a.set_xlim(0, 58); a.set_title(nm, fontsize=14); a.axvline(0, color='#999', lw=.8)
    a.grid(axis='x', alpha=.3); a.spines[['top', 'right']].set_visible(False)
for a in axs[1]: a.set_xlabel('激活增加（%）', fontsize=12)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '原文图 5（编者中文重绘）  各运动后各肌肉激活增加的组均值（方块）和 95% 置信区间（横线），数据取自原文表格'), 6)

c = q[1]; k = 900 / c.width; c = c.resize((900, round(c.height * k)), Image.LANCZOS)
y0 = max(0, (c.height - 383) // 2 + 40); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
