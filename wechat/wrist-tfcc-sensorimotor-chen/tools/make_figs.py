#!/usr/bin/env python3
"""Chen 2021 三角纤维软骨复合体损伤的腕关节感觉运动康复方案：首图中文标题卡；原文图 1～4 照片直接使用（图中只有 a、b 字母），加中文图注；
四期方案卡和结果图为编者根据原文表 1、表 2 整理绘制。
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
dr.text((70, 50), '原创研究 · 《手部治疗》2021', font=font(32), fill=TEAL)
dr.text((70, 135), '三角纤维软骨复合体损伤的', font=font(56), fill=INK)
dr.text((70, 215), '腕关节感觉运动康复方案临床评价', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Chen Z.', font=font(28), fill=GREY)
dr.text((70, 405), 'Hand Therapy. 2021;26(4):123-133', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

blocks = [('第 1 期 疼痛控制', '飞镖投掷动作（DTM）主动活动：每天 20 次 × 3～5 组；间断佩戴支具\n进阶：主动活动全范围无痛；等长收缩时疼痛 <2 分', LT, TEAL),
          ('第 2 期 肌肉再教育、关节觉察', '继续 DTM 主动活动\n旋前方肌、尺侧腕伸肌自我等长：前臂中立位，保持 30 秒 × 5 组，每天\nDTM 等张：手持 0.5 kg 加重球，10～20 次 × 3 组，每周 3～4 次；夜间佩戴支具\n进阶：等张时疼痛 <2 分；能完成 10 次 × 2 组；全程能控制', GR, (40, 130, 60)),
          ('第 3 期 神经肌肉康复', '旋前方肌、尺侧腕伸肌从等长进到等张：10～20 次 × 5 组\n反应性肌肉激活：加重球翻转、弹力棒（Flexbar）扰动，2～3 分钟 × 3 组\n分级负重：对墙压健身球 ± 扰动；协调训练：哑铃 PNF；去掉支具\n进阶：对墙负重时疼痛 <2 分；多关节协调良好', OR, (200, 110, 30)),
          ('第 4 期 动作正常化和功能', '停止等长、等张练习；继续反应性激活：加重晃水管、腕力球\n进阶负重：靠墙俯卧撑 → 俯卧撑把手上做地面俯卧撑\n抗阻协调：弹力带 PNF；诊室内 BTE 模拟患者自己的活动\n目标：恢复伤前上肢功能水平', PK, RED)]
save(card(1200, '腕关节感觉运动康复方案（WSRP）四期（编者根据原文表 1 整理）', blocks), 2)

save(capbox(raw(14), '原文图 1  自我等长收缩，箭头示用力方向。(a) 旋前方肌：前臂中立位做旋前，对侧手放在桡骨远端抵抗；'
                     '(b) 尺侧腕伸肌：做腕尺偏伸，对侧手指抵在第 4、5 掌骨背侧提供反作用力'), 3)
save(capbox(raw(15), '原文图 2  DTM 等张训练，手持 0.5 kg 加重球。(a) 起始位：腕桡偏伸；(b) 结束位：腕尺偏屈'), 4)
save(capbox(raw(20), '原文图 3  反应性肌肉激活：弹力棒（Flexbar）扰动'), 5)
save(capbox(raw(21), '原文图 4  抗阻协调训练：弹力带 PNF（上肢 D2 屈伸模式）。(a) 起始位；(b) 结束位'), 6)

fig, ax = plt.subplots(1, 5, figsize=(14, 4.4), dpi=100)
data = [('PRWHE（分，越低越好）', 35.70, 10.45, 70), ('握力（kg）', 17.80, 27.33, 70), ('疼痛（NPRS）', 2.50, 0.00, 100),
        ('负重（kg）', 15.23, 22.10, 70), ('位置觉误差（°）', 6.20, 5.20, 10)]
for a, (t, pre, post, pct) in zip(ax, data):
    bars = a.bar([0, 1], [pre, post], 0.55, color=['#9fb7bd', '#00788c'])
    for r, v in zip(bars, [pre, post]): a.text(r.get_x() + r.get_width() / 2, v, f'{v:.2f}', ha='center', va='bottom', fontsize=10.5)
    a.set_xticks([0, 1]); a.set_xticklabels(['治疗前', '结束时'], fontsize=11); a.set_ylim(0, max(pre, post) * 1.25)
    a.set_title(f'{t}\n达到 MCID：{pct}%', fontsize=11.5); a.spines[['top', 'right']].set_visible(False); a.grid(axis='y', alpha=0.3)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '10 名患者治疗前后均值（编者根据原文表 2 绘制）。负重用的是最小可检测变化（4.4 kg）；位置觉 P=0.45，无统计学差异'), 7)

c = raw(21); k = 900 / c.width; c = c.resize((900, round(c.height * k)), Image.LANCZOS)
y0 = round(c.height * 0.30); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
