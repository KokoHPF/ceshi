#!/usr/bin/env python3
"""Oya-Casero 2022 网球肘：治疗师手法离心 vs 自己用弹力带离心（先导 RCT）：首图中文标题卡；图 1 时间线、图 4 流程
中文重绘；图 2、3 离心动作照片加中文标签；附录表 A1 的 10 个居家动作拼图加中文名；DASH/VAS 按原文表 1～3 数值作图。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def clean(page, rect):
    p = d[page - 1]
    for w in p.get_text('words'):
        if pymupdf.Rect(w[:4]).intersects(rect): p.add_redact_annot(pymupdf.Rect(w[:4]))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)


def grab(page, rect, dpi=260):
    pix = d[page - 1].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*rect))
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def board(title, cells, ncol, cw=400, color=TEAL):
    """cells: [(图, 标签)]，统一宽度拼图"""
    cells = [(im.resize((cw, round(im.height * cw / im.width)), Image.LANCZOS), t) for im, t in cells]
    rows = [cells[i:i + ncol] for i in range(0, len(cells), ncol)]
    gap = 16; W = ncol * cw + (ncol + 1) * gap
    H = 90 + sum(max(c[0].height for c in r) + 66 for r in rows) + gap
    out = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(out)
    dr.rectangle([0, 0, W, 76], fill=color); dr.text((24, 16), title, font=font(40), fill='white')
    y = 92
    for r in rows:
        h = max(c[0].height for c in r)
        for j, (im, t) in enumerate(r):
            x = gap + j * (cw + gap); out.paste(im, (x, y)); ctext(dr, x + cw / 2, y + h + 12, t, font(34))
        y += h + 66
    return out


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '先导随机对照试验 · 《临床医学杂志》（JCM）2022', font=font(32), fill=TEAL)
for i, t in enumerate(['网球肘离心训练：治疗师手法做', 'vs 病人自己用弹力带做']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '20 例肱骨外上髁肌腱病 · 10 次课 · DASH、疼痛、满意度 · 随访 3 个月', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Oya-Casero A 等，J Clin Med 2022;11(24):7434', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，原文以 CC BY 4.0 开放获取', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1 时间线 ----------
W, H = 1400, 260; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
xs = [(30, 280, ['基线评估']), (380, 630, ['干预', '（10 次课）']), (770, 1020, ['干预后评估']), (1130, 1380, ['随访评估'])]
for x0, x1, t in xs:
    dr.rounded_rectangle([x0, 70, x1, 190], 16, fill=(225, 232, 245))
    yy = 130 - len(t) * 22
    for l in t: ctext(dr, (x0 + x1) / 2, yy, l, font(34)); yy += 44
for (a, b), t in zip([(280, 380), (630, 770), (1020, 1130)], ['', '2 周', '3 个月']):
    dr.line([a + 6, 130, b - 16, 130], fill=(120, 170, 200), width=8)
    dr.polygon([(b - 4, 130), (b - 26, 114), (b - 26, 146)], fill=(120, 170, 200))
    if t: ctext(dr, (a + b) / 2, 78, t, font(30), GREY)
save(im, 2)

# ---------- 图 2 治疗师手法离心 ----------
r2 = pymupdf.Rect(160, 495, 560, 662); clean(4, r2)
ph = grab(4, (163, 499, 558, 657)); w3 = ph.width / 3
cells = [(ph.crop((round(i * w3), 0, round((i + 1) * w3), ph.height)), t) for i, t in enumerate(['① 起始', '② 中间', '③ 结束'])]
save(board('原文图 2　治疗师手法离心（训练组）', cells, 3), 3)

# ---------- 图 3 弹力带离心 ----------
r3 = pymupdf.Rect(160, 230, 560, 418); clean(5, r3)
ph = grab(5, (165, 234, 556, 411)); w3 = ph.width / 3
cells = [(ph.crop((round(i * w3), 0, round((i + 1) * w3), ph.height)), t) for i, t in enumerate(['① 起始', '② 中间', '③ 结束'])]
save(board('原文图 3　病人自己用弹力带离心（对照组）', cells, 3), 4)

# ---------- 图 4 流程（照原图数字重绘） ----------
W, H = 1300, 1040; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def bx(x0, y0, x1, y1, lines, fill, fs=28):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill)
    yy = (y0 + y1 - len(lines) * (fs + 10)) / 2 + 3
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs)); yy += fs + 10


def ar(x, a, b, c=(120, 170, 200)):
    dr.line([x, a, x, b], fill=c, width=6); dr.polygon([(x, b + 6), (x - 13, b - 12), (x + 13, b - 12)], fill=c)


bx(330, 20, 730, 100, ['评估是否符合条件（25 人）'], (225, 232, 245))
ar(530, 100, 260); dr.line([530, 180, 760, 180], fill=(120, 170, 200), width=6)
bx(760, 120, 1280, 250, ['排除 5 人：', '不符合纳入标准 2 人；拒绝参加 2 人', '因病无法参加 1 人'], (245, 230, 230), 26)
bx(380, 265, 680, 335, ['随机分组（20 人）'], (200, 230, 210), 30)
ar(530, 335, 380); dr.line([270, 380, 790, 380], fill=(120, 170, 200), width=6); ar(270, 380, 420); ar(790, 380, 420)
for cx, a, b in [(270, '分到训练组（12 人）', '纳入分析 12 人'), (790, '分到对照组（8 人）', '纳入分析 8 人')]:
    bx(cx - 230, 425, cx + 230, 505, [a], (250, 238, 210))
    ar(cx, 505, 570); bx(cx - 230, 575, cx + 230, 645, [b + '（干预后）'], (240, 240, 240), 26)
    ar(cx, 645, 710); bx(cx - 230, 715, cx + 230, 785, [b + '（随访）'], (240, 240, 240), 26)
ctext(dr, 650, 860, '注：此图组别人数照原文图 4 重绘；原文表 1～4 写的是训练组 8 人、对照组 12 人，', font(26), RED)
ctext(dr, 650, 900, '两处正好相反，原文未说明。', font(26), RED)
save(im.crop((0, 0, W, 950)), 5)

# ---------- 附录表 A1：10 个居家动作 ----------
clean(10, pymupdf.Rect(150, 330, 570, 900)); clean(11, pymupdf.Rect(150, 100, 570, 230))
L, R = (205, 322), (402, 520)
NAMES = ['屈肘', '伸肘', '张开手', '握拳（手指屈曲）', '屈腕', '伸腕', '握紧拳头', '张开拳头']
cells = []
for i, (y0, y1) in enumerate([(377, 451), (473, 549), (570, 645), (667, 741)]):
    for j, (x0, x1) in enumerate([L, R]):
        cells.append((grab(10, (x0, y0, x1, y1)), NAMES[2 * i + j]))
cells += [(grab(11, (L[0], 134, L[1], 207)), '伸肌牵伸（外上髁）'), (grab(11, (R[0], 134, R[1], 207)), '屈肌牵伸（内上髁）')]
save(board('原文附录表 A1　居家活动度与牵伸动作（两组相同）', cells, 2, 520), 6)

# ---------- 结果图 ----------
T = ['基线', '干预后', '随访 3 个月']
fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), dpi=150)
for a, (ttl, e, c, yl) in zip(axs, [('DASH 功能障碍（越低越好）', [54.25, 38.34, 34.08], [56.42, 47.72, 31.05], (0, 70)),
                                     ('疼痛 VAS（越低越好）', [6.5, 3.7, 3.1], [6.04, 4.62, 3.33], (0, 8))]):
    a.plot(T, e, 'o-', color='#1f5f8b', lw=2.5, label='训练组（治疗师手法离心）')
    a.plot(T, c, 's--', color='#b5532c', lw=2.5, label='对照组（自己用弹力带）')
    for ys, other, col in [(e, c, '#1f5f8b'), (c, e, '#b5532c')]:
        for x_, y_, o_ in zip(T, ys, other):
            a.annotate(f'{y_:g}', (x_, y_), textcoords='offset points', xytext=(0, 8 if y_ >= o_ else -16), ha='center', color=col, fontsize=11)
    a.set_title(ttl, fontsize=13); a.set_ylim(*yl)
    for s in ['top', 'right']: a.spines[s].set_visible(False)
axs[0].legend(frameon=False, fontsize=10, loc='lower left')
fig.tight_layout(); fig.savefig(f'{OUT}/_p.png'); plt.close(fig)
save(Image.open(f'{OUT}/_p.png'), 7)
import os; os.remove(f'{OUT}/_p.png')

# ---------- 封面 900×383 ----------
c = grab(11, (L[0], 134, L[1], 207), 400)
c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = max(0, (c.height - 383) // 2); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
