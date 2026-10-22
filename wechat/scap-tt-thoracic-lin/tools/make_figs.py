#!/usr/bin/env python3
"""Lin 等 2025 乒乓球运动员肩胛动力障碍：单纯肩胛稳定训练与联合胸椎灵活性训练。首图中文标题卡；原文图 1～4 训练照片直接使用，加中文图注；
研究设计卡和主要结果图为编者根据原文整理绘制。
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
dr.text((70, 45), '对照研究 · 《人体运动学杂志》2025', font=font(32), fill=TEAL)
dr.text((70, 115), '比较单纯肩胛稳定训练与联合胸椎灵活性训练', font=font(50), fill=INK)
dr.text((70, 185), '对肩胛动力障碍精英乒乓球运动员的效果', font=font(50), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Lin Y, Zhang R, Zhang Y, Xu Y, Gao Q, Luo Q.', font=font(28), fill=GREY)
dr.text((70, 375), 'J Hum Kinet. 2025;98:93-106', font=font(28), fill=GREY)
dr.text((70, 440), '编者中文重排，仅作学术交流（原文 CC BY 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

blocks = [('分组', '对照组 10 人：无肩胛功能障碍，不干预，只测一次基线\n肩组 10 人：有肩胛动力障碍，只做肩胛稳定训练（SST）\n胸组 10 人：有肩胛动力障碍，SST + 双侧胸椎灵活性训练（TFT）+ 胸椎后前向松动\n（肩组和胸组用在线随机工具分组）', LT, TEAL),
          ('SST（只练持拍侧）', '① 弹力带 T、Y、W 抗阻\n② 弹力带肩外旋 / 内旋抗阻，末端保持 15 秒\n③ 弹力带前锯肌“出拳”，最大前伸位保持 15 秒\n④ 坐位激光笔描圆（距墙 1 m，2 组，组间休息 30 秒）', GR, (40, 130, 60)),
          ('TFT（双侧）', '侧卧，屈髋屈膝 90°、双肩前屈 90°、双臂伸直，上方手臂越过身体向后旋转，带动胸椎旋转（“开书”）', OR, (200, 110, 30)),
          ('剂量和进阶', '每周 3 次，每次 30～40 分钟，共 6 周；同一组物理治疗师监督\n弹力带每 2 周升一级：黄（3 磅）→ 绿（4.6 磅）→ 蓝（5.8 磅）\n胸椎训练每 2 周加量：每组 8 → 10 → 12 次', PK, RED)]
save(card(1200, '研究设计和训练方案（编者根据原文整理）', blocks), 2)

save(capbox(raw(27), '原文图 1  弹力带 TYW 抗阻训练。T：持拍臂外展 90° 抗阻；Y：上肢外展约 145° 抗阻；W：外展 90°、屈肘 60° 抗阻'), 3)
save(capbox(raw(28), '原文图 2  站立位弹力带肩外旋 / 内旋抗阻：屈肘 90°，对抗弹力带做外旋和内旋，末端保持 15 秒再回到起始位'), 4)
save(capbox(raw(29), '原文图 3  左：弹力带前锯肌“出拳”，伸肘、肩前屈 90°，肩胛前伸到最大并保持 15 秒；右：坐位描圆，距墙 1 m，手握激光笔沿靶板画圆，靶板高度与肩关节对齐'), 5)
save(capbox(raw(30), '原文图 4  侧卧位胸椎旋转（胸椎灵活性训练）：屈髋屈膝 90°、双肩前屈 90°，上方手臂越过身体向后打开，带动胸椎旋转'), 6)

fig, ax = plt.subplots(1, 3, figsize=(12, 4.6), dpi=100)
data = [('挥拍角速度变化（°/s）', 9.20, 44.35, '中位数', 'P=0.003'), ('持拍侧 Y 平衡变化（%）', 1.23, 10.87, '均值', 'P=0.002'),
        ('向右胸椎旋转变化（°）', -0.40, 4.72, '均值', 'P=0.001')]
for a, (t, sh, ch, kind, pv) in zip(ax, data):
    bars = a.bar([0, 1], [sh, ch], 0.55, color=['#7fb3bf', '#00788c'])
    for r, v in zip(bars, [sh, ch]): a.text(r.get_x() + r.get_width() / 2, v, f'{v:.2f}', ha='center', va='bottom' if v >= 0 else 'top', fontsize=11)
    a.axhline(0, color='#555', lw=1); a.set_xticks([0, 1]); a.set_xticklabels(['肩组（SST）', '胸组（SST+TFT）'], fontsize=12)
    lo = min(0, sh, ch); hi = max(sh, ch); a.set_ylim(lo - (hi - lo) * 0.12, hi * 1.2)
    a.set_title(f'{t}\n{kind}，组间 {pv}', fontsize=12.5); a.spines[['top', 'right']].set_visible(False); a.grid(axis='y', alpha=0.3)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '组间差异有统计学意义的 3 项指标（编者根据原文表 3 绘制，数值为干预后减干预前）。其余指标（本体感觉误差、LSST、非持拍侧 Y 平衡、'
                                              '向左胸椎旋转、肌力）组间无差异'), 7)

c = raw(27).crop((0, 0, 773, 329)).resize((900, 383), Image.LANCZOS)
c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
