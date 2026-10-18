#!/usr/bin/env python3
"""Jiang 2025 普拉提 + 筋膜放松治疗上交叉综合征：首图为原文标题区；图 1 流程中文重绘；表 1 动作照片按阶段拼图加中文名；
图 2～6 柱状图按原图读取的近似值中文重绘（原文未给数值表）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageOps

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); RED = (190, 40, 50); TEAL = (0, 110, 130)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


pix = d[0].get_pixmap(dpi=200, clip=pymupdf.Rect(30, 111, 565, 162))
save(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), 1)

# ---------- 图 1 流程 ----------
W, H = 1400, 1080; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def bx(x0, y0, x1, y1, lines, fill, fs=28, col=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 10, fill=fill)
    yy = (y0 + y1 - len(lines) * (fs + 10)) / 2 + 3
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs), col); yy += fs + 10


def ar(x, a, b, c=(110, 200, 220)):
    dr.line([x, a, x, b], fill=c, width=8); dr.polygon([(x, b + 6), (x - 16, b - 16), (x + 16, b - 16)], fill=c)


for y0, y1, t in [(30, 380, ['第 1 步', '随机分组与', '干预前测试']), (430, 700, ['第 2 步', '干预 12 周后', '复测 5 项指标']), (760, 1050, ['第 3 步', '统计分析'])]:
    bx(20, y0 + 60, 260, y1 - 60, t, (238, 238, 238), 28)
bx(620, 40, 820, 100, ['34 人'], (160, 170, 240))
ar(720, 100, 132)
bx(470, 135, 970, 205, ['随机分为试验组 17 人、对照组 17 人'], (190, 235, 180), 26)
bx(300, 230, 690, 300, ['试验组：筋膜放松 + 普拉提'], (250, 235, 180), 26)
bx(760, 230, 1150, 300, ['对照组：仅普拉提'], (250, 235, 180), 26)
MS = ['头前伸角\n肩前伸角', '颈椎功能\n障碍指数', '颈椎\n活动度', '疼痛\nVAS', '表面\n肌电']
for i, t in enumerate(MS):
    x0 = 300 + i * 220; bx(x0, 320, x0 + 200, 400, t.split('\n'), (253, 230, 210), 24)
    bx(x0, 560, x0 + 200, 640, t.split('\n'), (253, 220, 220), 24)
ar(720, 410, 470)
bx(330, 480, 1110, 540, ['12 周后复测：试验组（普拉提 + 筋膜放松）、对照组（仅普拉提）'], (245, 245, 245), 24)
ar(720, 650, 700)
bx(840, 680, 1300, 750, ['脱落：每组各 2 人'], (230, 240, 250), 26)
bx(420, 790, 1020, 870, ['统计分析：试验组 15 人、对照组 15 人'], (230, 230, 236), 26)
ar(720, 875, 925)
bx(600, 935, 840, 1000, ['结果与结论'], (230, 230, 236), 26)
save(im, 2)

# ---------- 表 1 动作照片 ----------
for _pg in (4, 5, 6):
    _p = d[_pg]
    for _w in _p.get_text('words'): _p.add_redact_annot(pymupdf.Rect(_w[:4]))
    _p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)


def grab(pg, y0, y1, x0=216, x1=327):
    pix = d[pg].get_pixmap(dpi=260, clip=pymupdf.Rect(x0, y0, x1, y1)); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    bb = ImageOps.invert(im.convert('L')).point(lambda v: 255 if v > 18 else 0).getbbox()
    return im.crop(bb)


def board(title, items, n, color=TEAL, CW=420, CH=330, cols=3):
    rows = (len(items) + cols - 1) // cols
    c = Image.new('RGB', (cols * CW + 60, 100 + rows * (CH + 110)), 'white'); dr = ImageDraw.Draw(c)
    dr.rectangle([0, 0, c.width, 76], fill=color); dr.text((30, 16), title, font=font(42), fill='white')
    for i, (name, sub, part) in enumerate(items):
        gx, gy = 30 + (i % cols) * CW, 100 + (i // cols) * (CH + 110)
        m = grab(*part); s = min((CW - 30) / m.width, CH / m.height); m = m.resize((round(m.width * s), round(m.height * s)), Image.LANCZOS)
        c.paste(m, (gx + (CW - 10 - m.width) // 2, gy + (CH - m.height) // 2))
        ctext(dr, gx + CW / 2 - 5, gy + CH + 10, name, font(32)); ctext(dr, gx + CW / 2 - 5, gy + CH + 54, sub, font(22), GREY)
    save(c, n)


# 筋膜放松：原图为 6 张小图竖排，整列使用
fa = grab(4, 149, 452); fa = fa.resize((round(fa.width * 900 / fa.height), 900), Image.LANCZOS)
c = Image.new('RGB', (1100, 1080), 'white'); dr = ImageDraw.Draw(c)
dr.rectangle([0, 0, 1100, 76], fill=(190, 60, 40)); dr.text((30, 16), '试验组额外：训练前筋膜放松（约 5 分钟）', font=font(40), fill='white')
c.paste(fa, (60, 120))
for k, t in enumerate(['筋膜枪：颈后', '筋膜枪：肩颈前侧', '泡沫轴：上背', '泡沫轴：侧卧背阔肌', '泡沫轴：俯卧胸前', '泡沫轴：仰卧胸椎']):
    dr.text((60 + fa.width + 50, 150 + k * 150), t, font=font(32), fill=INK)
dr.text((60 + fa.width + 50, 1010), '目标：胸大小肌、上斜方肌、胸锁乳突肌、背阔肌等', font=font(24), fill=GREY)
save(c, 3)

board('热身唤醒（每次 1 小时训练的开头）', [
    ('呼吸练习', '120 秒', (4, 468, 541)), ('肩关节屈伸', '胸大肌、三角肌、背阔肌', (4, 558, 632)), ('深蹲', '臀大肌、股四头肌', (4, 642, 761)),
    ('站立提踵', '腓肠肌、比目鱼肌', (5, 148, 267)), ('骨盆时钟', '腹直肌、腹斜肌、腹横肌', (5, 284, 349))], 4)
board('肌肉训练', [
    ('颈部拉起', '颈深屈肌', (5, 373, 443)), ('坐姿菱形肌训练', '菱形肌、中斜方肌', (5, 467, 535)), ('单腿后拉', '胸大肌、腹肌、屈髋肌', (5, 545, 624)),
    ('颈深屈肌稳定', '原文写作肩胛提肌、头半棘肌', (5, 650, 730)), ('双腿后踢', '背伸肌群、腘绳肌', (6, 146, 202)), ('游泳式', '背伸肌群', (6, 212, 263))], 5, (40, 90, 160))
board('放松练习', [
    ('婴儿式', '下背部', (6, 273, 332)), ('倒 V 式', '胸大肌、背伸肌群、腘绳肌', (6, 344, 409)), ('坐姿脊柱旋转', '多裂肌等', (6, 419, 479))], 6, (0, 130, 110))

# ---------- 图 2～6：结果（近似值） ----------
E_C = ['试验组', '对照组']; PRE = '#2b2b2b'; POST = '#a8a8a8'


def panel(ax, vals, ylabel, ylim, within, between, title=None):
    x = np.arange(2); w = .32
    ax.bar(x - w / 2, [vals[0][0], vals[1][0]], w, color=PRE, label='干预前')
    ax.bar(x + w / 2, [vals[0][1], vals[1][1]], w, color=POST, label='干预后')
    ax.set_xticks(x); ax.set_xticklabels(E_C, fontsize=12); ax.set_ylim(0, ylim * 1.22); ax.set_yticks(np.linspace(0, ylim, 6)); ax.set_ylabel(ylabel, fontsize=12)
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    for i in range(2):
        for j in range(2):
            v = vals[i][j]; ax.text(i + (j - .5) * w, v + ylim * .01, f'{v:g}', ha='center', fontsize=9.5)
        if within[i]:
            top = max(vals[i]) + ylim * .07
            ax.plot([i - w / 2, i - w / 2, i + w / 2, i + w / 2], [top - ylim * .02, top, top, top - ylim * .02], color='k', lw=1)
            ax.text(i, top + ylim * .005, within[i], ha='center', fontsize=12)
    if between:
        top = max(max(v) for v in vals) + ylim * .2
        ax.plot([w / 2, w / 2, 1 + w / 2, 1 + w / 2], [top - ylim * .02, top, top, top - ylim * .02], color='k', lw=1)
        ax.text(.5 + w / 2, top + ylim * .005, between, ha='center', fontsize=12)
    if title: ax.set_title(title, fontsize=13, pad=4)


def fig(panels, n, title, ncol, note):
    nrow = (len(panels) + ncol - 1) // ncol
    f, axs = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 3.9 * nrow + .6), dpi=150, squeeze=False)
    for ax, pp in zip(axs.flat, panels): panel(ax, *pp)
    for ax in list(axs.flat)[len(panels):]: ax.axis('off')
    h, l = axs[0][0].get_legend_handles_labels(); f.legend(h, l, loc='upper right', fontsize=11, frameon=False)
    f.suptitle(title, fontsize=15, fontweight='bold', x=.02, ha='left')
    f.text(.02, .005, note, fontsize=10, color='#555')
    f.tight_layout(rect=(0, .03, 1, .95)); f.savefig(f'{OUT}/_r.png'); plt.close(f)
    save(Image.open(f'{OUT}/_r.png'), n)


NOTE = '数值按原图柱高读取，为近似值；*、**、*** 为组内前后比较，#、##、### 为干预后组间比较'
fig([([(49, 39), (48.8, 43)], '头前伸角（°）', 80, ['***', '***'], '#', '头前伸角'),
     ([(57, 47), (57, 52)], '肩前伸角（°）', 80, ['***', '***'], '#', '肩前伸角')], 7, '原文图 2　体态', 2, NOTE)
fig([([(36, 38.5), (36, 38)], '屈曲（°）', 60, ['*', '*'], '', '前屈'),
     ([(30.5, 41), (31.5, 37)], '后伸（°）', 60, ['***', '***'], '#', '后伸'),
     ([(32.5, 35.8), (32, 35.5)], '左侧屈（°）', 60, ['**', '**'], '', '左侧屈'),
     ([(32, 35.5), (31.7, 34.3)], '右侧屈（°）', 60, ['*', '*'], '', '右侧屈'),
     ([(51.5, 68), (53, 61.5)], '左旋（°）', 100, ['***', '***'], '#', '左旋'),
     ([(52, 69.5), (52, 61.5)], '右旋（°）', 100, ['***', '***'], '##', '右旋')], 8, '原文图 3　颈椎活动度', 3, NOTE)
fig([([(65, 78), (66, 72.5)], 'Hz', 100, ['***', '***'], '##', '左上斜方肌'),
     ([(68, 81), (67.5, 77)], 'Hz', 100, ['***', '***'], '#', '右上斜方肌'),
     ([(67, 59.5), (67, 62)], 'Hz', 100, ['***', '***'], '', '左下斜方肌'),
     ([(64, 58.5), (64.5, 61)], 'Hz', 100, ['***', '**'], '', '右下斜方肌'),
     ([(66, 81.5), (66.5, 76)], 'Hz', 100, ['***', '***'], '#', '左胸大肌'),
     ([(66.5, 83), (66.5, 75.5)], 'Hz', 100, ['***', '***'], '##', '右胸大肌')], 9, '原文图 4　表面肌电：平均功率频率', 3, NOTE)
fig([([(60, 75), (59, 68.5)], 'Hz', 100, ['***', '***'], '##', '左上斜方肌'),
     ([(59, 73), (59, 68)], 'Hz', 100, ['***', '***'], '##', '右上斜方肌'),
     ([(61, 49), (60.5, 52.5)], 'Hz', 100, ['***', '***'], '#', '左下斜方肌'),
     ([(58, 52.5), (57, 56.5)], 'Hz', 100, ['***', ''], '#', '右下斜方肌'),
     ([(62.5, 68), (62.5, 65.5)], 'Hz', 100, ['***', '***'], '', '左胸大肌'),
     ([(58.5, 66.5), (59, 62.5)], 'Hz', 100, ['***', '**'], '#', '右胸大肌')], 10, '原文图 5　表面肌电：中位频率', 3, NOTE)
fig([([(4.3, .5), (4.3, 1.0)], 'VAS（分）', 10, ['***', '***'], '#', '疼痛'),
     ([(23.8, 3.2), (24.5, 7.0)], 'NDI（%）', 50, ['***', '***'], '###', '颈椎功能障碍指数')], 11, '原文图 6　疼痛与颈椎功能', 2, NOTE)

cv = Image.new('RGB', (900, 383), 'white'); dr = ImageDraw.Draw(cv)
m = grab(5, 467, 535); m = m.resize((round(m.width * 383 / m.height), 383), Image.LANCZOS); m = m.resize((420, round(m.height * 420 / m.width)), Image.LANCZOS); cv.paste(m, (480, (383 - m.height) // 2))
dr.text((30, 44), '圆肩探头', font=font(76), fill=INK)
dr.text((30, 150), '普拉提 + 筋膜放松', font=font(46), fill=TEAL)
dr.text((30, 225), '12 周，每周 3 次', font=font(32), fill=RED)
dr.text((30, 320), 'Healthcare 2025 · 随机对照试验', font=font(22), fill=GREY)
cv.save(f'{OUT}/cover.jpg', quality=92)
