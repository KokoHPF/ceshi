#!/usr/bin/env python3
"""Nakai 等 2026 IJSPT 弹性趾管训练对足内在肌大小和反应力量的急性效应（随机交叉研究）：首图为原题直译标题卡；
原文图 1 流程图框内英文擦掉后在原位置写中文，图 2、图 3 为照片（图内无英文），图注译成中文；
三种条件做法卡、结果图（横截面积、RSI、主观评价）和临床卡为编者根据原文方法和表 1～4 整理。
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
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88, optimize=True)


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


import numpy as np


import io


def raw(x):
    return Image.open(io.BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def cover_from(im, cx=0.5, cy=0.5):
    """封面 900×383：从原文插图按比例裁出一块（cx、cy 为裁剪中心的相对位置）"""
    r = 900 / 383; w, h = im.size
    if w / h > r: cw, ch = round(h * r), h
    else: cw, ch = w, round(w / r)
    x = min(max(0, round(cx * w - cw / 2)), w - cw); y = min(max(0, round(cy * h - ch / 2)), h - ch)
    im.crop((x, y, x + cw, y + ch)).resize((900, 383), Image.LANCZOS).convert('RGB').save(f'{OUT}/cover.jpg', quality=90)


def tiles(items, title, n, fs=24):
    """原图并排（等高），下方灰底中文图注"""
    gap = 15; W = 1200; hs = 600
    ims = [x.resize((round(x.width * hs / x.height), hs), Image.LANCZOS) for x, _ in items]
    k = (W - gap * (len(ims) - 1)) / sum(i.width for i in ims)
    ims = [i.resize((round(i.width * k), round(i.height * k)), Image.LANCZOS) for i in ims]
    hh = ims[0].height; ch = max(para_h(t, fs, i.width - 24, gap=8) for i, (_, t) in zip(ims, items))
    im = Image.new('RGB', (W, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im); x = 0
    for i, (_, t) in zip(ims, items):
        im.paste(i, (x, 0)); dr.rectangle([x, hh, x + i.width, hh + ch + 20], fill=(232, 232, 232))
        para(dr, x + 12, hh + 12, t, fs, i.width - 24, gap=8); x += i.width + gap
    save(titled(im, title), n)


def one(x, cap, title, n):
    save(titled(capbox(x, cap), title), n)


def title_card(tag, zh, en, au, cite, org):
    W, H = 1400, 700; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, 18, H], fill=TEAL)
    dr.text((70, 56), tag, font=font(32), fill=TEAL)
    y = 130
    for l in zh: dr.text((70, y), l, font=font(50), fill=INK); y += 70
    y += 20
    for l in en: dr.text((70, y), l, font=font(28), fill=GREY); y += 40
    y += 20; dr.line([70, y, W - 70, y], fill=(200, 205, 210), width=2); y += 30
    dr.text((70, y), au, font=font(30), fill=GREY); y += 44
    dr.text((70, y), cite, font=font(28), fill=GREY); y += 56
    dr.text((70, y), org, font=font(26), fill=GREY)
    dr.text((70, H - 60), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
    save(im, 1)


def zh_label(im, boxes):
    """图中白底英文标注：整块刷成底色后在原位置写中文。boxes 为 (x0, y0, x1, y1, 文字, 字号, 对齐)"""
    d = ImageDraw.Draw(im); a = np.asarray(im.convert('L')) < 240; H_, W_ = a.shape
    for x0, y0, x1, y1, t, fs, al in boxes:
        # 向外扩到字母上下沿的浅色像素，碰到照片（成片非白）就停
        e0, e1, ex0, ex1 = y0, y1, max(0, x0 - 8), min(W_, x1 + 8)
        while e0 > 0 and y0 - e0 < 14 and a[e0 - 1, ex0:ex1].mean() < 0.3: e0 -= 1
        while e1 < H_ - 1 and e1 - y1 < 14 and a[e1 + 1, ex0:ex1].mean() < 0.3: e1 += 1
        d.rectangle([ex0, e0, ex1, e1], fill='white')
        f = font(fs); w = d.textlength(t, font=f); cy = (y0 + y1) / 2
        x = x0 if al == 'l' else (x1 - w if al == 'r' else (x0 + x1 - w) / 2)
        d.text((x, cy), t, font=f, fill=(0, 0, 0), anchor='lm')
    return im


def zh_boxes(im, boxes, s):
    """流程图：方框内部刷成框内底色（保留边框），再写中文。坐标按缩略图给出，s 为放大倍数"""
    d = ImageDraw.Draw(im); a = np.asarray(im)
    for (x0, y0, x1, y1), t, fs, al in boxes:
        x0, y0, x1, y1 = (round(v * s) for v in (x0, y0, x1, y1)); m = round(2.5 * s)
        bg = tuple(int(c) for c in np.median(a[y0 + m:y1 - m, x0 + m:x1 - m].reshape(-1, 3), 0))
        d.rectangle([x0 + m, y0 + m, x1 - m, y1 - m], fill=bg)
        fg = 'white' if sum(bg) < 500 else (20, 20, 20); f = font(fs * s); ls = t.split('\n'); lh = fs * s * 1.3
        top = (y0 + y1) / 2 - lh * len(ls) / 2 + lh / 2
        for i, l in enumerate(ls):
            x = x0 + m + 4 if al == 'l' else (x0 + x1 - d.textlength(l, font=f)) / 2
            d.text((x, top + i * lh), l, font=f, fill=fg, anchor='lm')
    return im


def heal(im, mask, it=400):
    """把 mask 区域（文字笔画）用四邻域扩散补成周围底色（照片上的字母用）"""
    a = np.asarray(im).astype(float); m = mask.copy(); a[m] = a[~m].mean(0)
    ys, xs = np.nonzero(m); y0, y1, x0, x1 = max(ys.min() - 2, 0), ys.max() + 3, max(xs.min() - 2, 0), xs.max() + 3
    sub = a[y0:y1, x0:x1]; sm = m[y0:y1, x0:x1]
    for _ in range(it):
        p = np.pad(sub, ((1, 1), (1, 1), (0, 0)), mode='edge')
        avg = (p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) / 4
        sub[sm] = avg[sm]
    a[y0:y1, x0:x1] = sub
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def dark_mask(im, boxes, thr=90, grow=2):
    """boxes 内比 thr 暗的像素（黑色字母）作为 mask，向外扩 grow 像素"""
    g = np.asarray(im.convert('L')); m = np.zeros(g.shape, bool)
    for x0, y0, x1, y1 in boxes: m[y0:y1, x0:x1] = g[y0:y1, x0:x1] < thr
    for _ in range(grow):
        p = np.pad(m, 1); m = p[1:-1, 1:-1] | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    return m


def vtext(im, box, t, fs, fill=(0, 0, 0), bg='white'):
    """竖排文字区（旋转 90° 的英文）：刷底色后写逆时针旋转 90° 的中文"""
    d = ImageDraw.Draw(im); d.rectangle(box, fill=bg); f = font(fs)
    w = int(d.textlength(t, font=f)) + 8; lay = Image.new('RGBA', (w, fs + 10), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((4, 2), t, font=f, fill=fill); lay = lay.rotate(90, expand=True)
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2; im.paste(lay, (cx - lay.width // 2, cy - lay.height // 2), lay)
    return im


def chart_style():
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    fm.fontManager.addfont(F); plt.rcParams['font.family'] = fm.FontProperties(fname=F).get_name()
    plt.rcParams['axes.unicode_minus'] = False
    return plt


def figsave(plt, fig, title, n):
    b = io.BytesIO(); fig.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
    save(titled(Image.open(b).convert('RGB'), title), n)


# 首图：原题直译
title_card('随机交叉试验 · Int J Sports Phys Ther 2026 · 证据等级 2',
           ['弹性趾管训练对健康年轻男性', '足内在肌大小和反应力量的急性效应：', '一项随机交叉研究'],
           ['Acute Effects of an Elastic Toe-Tube Exercise on Intrinsic Foot Muscle Size',
            'and Reactive Strength in Healthy Young Men: A Randomized Crossover Study'],
           'Yuki Nakai, Yasufumi Takeshita, Makoto Komiya',
           'Int J Sports Phys Ther. 2026;21(8):707-717. doi:10.26603/001c.165043',
           '日本令和健康科学大学康复学部物理治疗系 等')

# 原文图 1：交叉设计流程图，框内英文刷掉后写中文
s = 3; im = raw(74); im = im.resize((im.width * s, im.height * s), Image.LANCZOS)
B = [((82, 10, 440, 52), '受试者（n = 20）', 20, 'c'), ((82, 87, 440, 129), '随机交叉设计', 20, 'c')]
for k, (p0, i0, i1, q0) in enumerate(((179, 246, 317, 341), (509, 574, 646, 670), (839, 905, 975, 1000)), 1):
    B += [((82, p0, 440, p0 + 42), '干预前：超声 + 反弹跳测试', 19, 'c'),
          ((82, i0, 440, i1), f'干预 {k}\n（弹性趾管 / 短足训练 / 对照，随机顺序）', 19, 'c'),
          ((82, q0, 440, q0 + 42), '干预后：超声 + 反弹跳测试', 19, 'c')]
B += [((65, 419, 458, 460), '洗脱期（≥ 1 周）', 19, 'c'), ((65, 748, 458, 790), '洗脱期（≥ 1 周）', 19, 'c')]
im = zh_boxes(im, B, s)
for k, (y0, y1) in enumerate(((198, 355), (525, 684), (855, 1014)), 1):
    im = vtext(im, (28 * s, (y0 - 14) * s, 70 * s, (y1 + 14) * s), f'条件 {k}', 26 * s)
flow = im.resize((round(im.width * 0.62), round(im.height * 0.62)), Image.LANCZOS)
cv = Image.new('RGB', (1200, flow.height + 20), 'white'); cv.paste(flow, ((1200 - flow.width) // 2, 10))
save(titled(capbox(cv, '原文图 1　随机交叉设计流程：20 名受试者以随机顺序完成三种条件，每种条件前后各测一次超声和反弹跳，条件之间洗脱至少 1 周（RJ = 反弹跳）'),
            '研究流程（原文图 1，编者中文覆盖）'), 2)

# 原文图 3：趾管训练（照片内只有分图字母 A/B）
one(raw(90), '原文图 3　弹性趾管训练：A 起始位；B 踝跖屈到末端、足趾保持屈曲。弹力管两端打结卡在拇趾和第 2 趾之间，另一端手握',
    '弹性趾管训练怎么做（原文图 3）', 3)

# 编者整理：三种条件的具体做法
phases('三种条件与测量（编者根据原文方法整理）', [
    ('弹性趾管训练（Tube-ex）', OR, RED, [
        '坐位，训练侧膝关节完全伸直，足跟着地',
        '绿色 TheraBand 弹力管（重阻力，长 1 m），两端打结，结卡在拇趾和第 2 趾之间，另一端手握，阻力方向与小腿长轴平行',
        '对抗弹力做踝跖屈和背伸；跖屈到末端时，所有足趾（含拇趾）的跖趾关节和趾间关节保持屈曲，足内在肌最大收缩 5 秒',
        '每组 10 次，共 3 组，组间休息 45 秒；口头提示避免趾间关节伸直']),
    ('短足训练（SF-ex）', LT, TEAL, [
        '坐位，膝关节屈曲约 90°',
        '把第一跖骨头往足跟方向拉，足沿前后方向“缩短”，不卷趾、不抬脚，在能感到足底肌收缩的位置保持 5 秒',
        '有视觉反馈监控足弓抬高；每组 10 次最大收缩，共 3 组，组间休息 45 秒（与趾管训练同量）']),
    ('对照', (240, 240, 240), GREY, ['同一坐姿静坐 5 分钟，不动足趾和踝']),
    ('每次干预前后都测', GR, (40, 120, 60), [
        '超声测非优势足 3 块足内在肌横截面积：拇展肌（AbH）、拇短屈肌（FHB）、趾短屈肌（FDB），每块取 3 张图平均',
        '非优势腿单腿连续反弹跳 7 次 × 2 组（Optojump 光电测时），去掉最大和最小后取 5 跳平均；反应力量指数 RSI = 腾空时间 ÷ 触地时间']),
], 4)

# 原文图 2：趾握力计（照片内为日文，无英文）
one(raw(77), '原文图 2　测趾握力用的趾握力计（Takei T.K.K. 3364）。坐位，髋、膝、踝均屈 90°，足跟抵住挡板、足背用非弹性带轻固定，拇趾近节对准握杆',
    '基线测量：趾握力（原文图 2）', 5)

plt = chart_style()
# CSA 变化
M = ['拇展肌 AbH', '拇短屈肌 FHB', '趾短屈肌 FDB']
D = {'弹性趾管': [20.38, 10.74, 25.46], '短足训练': [11.40, 5.03, 16.90], '对照': [0.77, -0.71, 0.70]}
MDC = {'弹性趾管': [7.90, 9.10, 9.42], '短足训练': [10.21, 8.51, 10.52], '对照': [9.29, 7.46, 5.91]}
PRE = {'弹性趾管': [230.35, 190.11, 196.63], '短足训练': [232.57, 190.51, 197.83], '对照': [231.48, 185.91, 192.35]}
C = {'弹性趾管': '#D2553C', '短足训练': '#2C8C9E', '对照': '#A0A0A0'}
fig, ax = plt.subplots(figsize=(10.9, 5.6)); w = 0.26
for j, k in enumerate(D):
    xs = [i + (j - 1) * w for i in range(3)]
    ax.bar(xs, D[k], w * 0.92, color=C[k], label=k)
    for x, v, m, p in zip(xs, D[k], MDC[k], PRE[k]):
        ax.plot([x - w * 0.46, x + w * 0.46], [m, m], color='black', ls='--', lw=1.2)
        ax.text(x, max(v, m) + 0.8, f'{v:+.1f}\n({v / p * 100:+.0f}%)', ha='center', va='bottom', fontsize=10.5)
ax.plot([], [], color='black', ls='--', lw=1.2, label='该条件的 MDC95（超过才算超出测量误差）')
for i, (p, e) in enumerate((('0.002', '0.34'), ('0.019', '0.21'), ('0.001', '0.61'))):
    ax.text(i, 36, f'交互作用 P = {p}，偏 η² = {e}', ha='center', fontsize=11, color='#333')
ax.set_xticks(range(3)); ax.set_xticklabels(M, fontsize=13); ax.set_ylim(-3, 40); ax.axhline(0, color='black', lw=0.8)
ax.set_ylabel('横截面积变化（干预后 - 干预前，mm²）', fontsize=12); ax.legend(fontsize=10.5, loc='upper left', bbox_to_anchor=(0, 0.9), frameon=False)
ax.spines[['top', 'right']].set_visible(False)
figsave(plt, fig, '结果①：足内在肌横截面积的即时变化（编者据原文表 1、表 2 绘制）', 6)

# RSI
fig, ax = plt.subplots(figsize=(10.9, 5.0))
R = {'弹性趾管': (0.366, 0.404, '+0.038'), '短足训练': (0.367, 0.376, '+0.009'), '对照': (0.372, 0.370, '-0.001')}  # Δ 照抄原文表 3
for k, (a, b_, dl) in R.items():
    ax.plot([0, 1], [a, b_], marker='o', ms=9, lw=2.6, color=C[k], label=f'{k}（{dl}）')
    ax.text(1.04, b_, f'{b_:.3f}', va='center', fontsize=12, color=C[k])
ax.text(-0.04, 0.366, '0.37 左右', ha='right', va='center', fontsize=12, color='#555')
ax.set_xticks([0, 1]); ax.set_xticklabels(['干预前', '干预后'], fontsize=13); ax.set_xlim(-0.35, 1.3); ax.set_ylim(0.355, 0.415)
ax.set_ylabel('反应力量指数 RSI（均值）', fontsize=12); ax.legend(fontsize=11.5, loc='upper left', frameon=False)
ax.text(0.5, 0.358, '时间 × 条件交互 P = 0.035，偏 η² = 0.16；只有弹性趾管前后差异显著（P = 0.001）\n干预后 RSI：趾管 vs 短足 d = 0.80，趾管 vs 对照 d = 0.66（组间标准差约 0.14，远大于变化量）',
        ha='center', fontsize=10.5, color='#333')
ax.spines[['top', 'right']].set_visible(False)
figsave(plt, fig, '结果②：反应力量指数 RSI（编者据原文表 3 绘制）', 7)

# 主观评价
fig, ax = plt.subplots(figsize=(10.9, 4.6))
Q = ['容易做', '觉得有效', '有被练到的感觉']; T = [(4.40, 0.99), (4.30, 1.03), (4.45, 1.15)]; Sx = [(2.75, 1.65), (3.65, 1.14), (3.40, 1.43)]
P = ['P = 0.005，r = 0.61', 'P = 0.072（不显著）', 'P = 0.042，r = 0.45']
for i in range(3):
    ax.barh(i + 0.2, T[i][0], 0.38, xerr=T[i][1], color=C['弹性趾管'], capsize=4, label='弹性趾管' if i == 0 else None)
    ax.barh(i - 0.2, Sx[i][0], 0.38, xerr=Sx[i][1], color=C['短足训练'], capsize=4, label='短足训练' if i == 0 else None)
    ax.text(6.0, i, P[i], va='center', fontsize=11.5)
ax.set_yticks(range(3)); ax.set_yticklabels(Q, fontsize=13); ax.invert_yaxis(); ax.set_xlim(0, 8.6); ax.set_xticks(range(1, 6))
ax.set_xlabel('5 分 Likert 量表（均值 ± 标准差，5 = 非常同意）', fontsize=11.5); ax.legend(fontsize=11, loc='lower right', bbox_to_anchor=(1, 1), ncol=2, frameon=False)
ax.spines[['top', 'right']].set_visible(False)
figsave(plt, fig, '结果③：受试者主观评价（编者据原文表 4 绘制）', 8)

phases('落到临床：弹性趾管训练怎么用、别怎么想（编者观点）', [
    ('可以试的场景', GR, (40, 120, 60), [
        '跳跃、冲刺等爆发性训练前的足部激活热身：一根弹力管、3 组 × 10 次、约 5 分钟',
        '早期康复里想要低负荷但有明确足底发力感的阶段（原文受试者更愿意做，也觉得更好掌握）',
        '短足训练学不会、找不到发力感的人，可以作为替代或过渡']),
    ('做的时候注意', OR, RED, [
        '结卡在拇趾和第 2 趾之间，跖屈到末端时全部足趾“抓住”管子保持 5 秒，不要让趾间关节伸直',
        '阻力方向与小腿长轴平行；原文用绿色（重阻力）弹力管，阻力以能做出最大收缩为准']),
    ('别过度解读', PK, RED, [
        '横截面积即刻增加约 6%～13% 是运动后的暂时肿胀，不是肌肉长大',
        'RSI 平均只升了 0.038，且只在健康年轻男性身上测过一次；能维持多久、能否转化到冲刺和变向都不知道',
        '没有测肌电，分不清是足内在肌还是趾长屈肌等外在肌在出力',
        '两种训练的姿势不同（趾管膝伸直、短足膝屈 90°），差异不全是“弹力管”带来的']),
], 9)

# 封面：原文图 3 两张趾管训练照片，裁足和小腿部分，并抹掉分图字母 A/B
im = raw(90)
im = heal(im, dark_mask(im, [(40, 960, 110, 1030), (585, 960, 650, 1030)], thr=70, grow=3))
r = 900 / 383; ch = round(im.width / r); y = 560
im.crop((0, y, im.width, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
