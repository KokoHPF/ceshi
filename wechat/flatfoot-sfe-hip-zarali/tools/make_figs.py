#!/usr/bin/env python3
"""Zarali 等 2024 扁平足女性：综合练习 vs 短足练习 vs 短足 + 等长髋外展：首图中文标题卡；三组方案卡、短足练习进阶卡、
结果图为编者绘制；流程图按原文图 1 重绘为中文；原文图 2、3 加中文标注（器械与弹力带文字已模糊）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
X = {2: 109, 3: 115}
# 以宽 900 为基准
BL = {2: [(328, 512, 392, 552)], 3: [(780, 305, 858, 340)]}


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def fig(n, W):
    im = Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB'); s = im.width / 900
    for b in BL.get(n, []):
        bb = tuple(int(v * s) for v in b)
        im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(10 * s)), bb[:2])
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200):
    im = fig(n, W)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in f'图 {n}　{cap}':
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, ((W - im.width) // 2, hh + 8)); return t


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '随机试验 · 《BMC 运动科学、医学与康复》2024', font=font(32), fill=TEAL)
for i, t in enumerate(['扁平足练足弓，', '加一根弹力带练髋外展效果更好？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '综合练习 vs 短足练习 vs 短足 + 等长髋外展，6 周', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Zarali A, Raeisi Z, Aminmahalati A. BMC Sports Sci Med Rehabil 2024;16:233', font=font(28), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 三组 ----------
W = 1400; im = Image.new('RGB', (W, 820), 'white'); dr = ImageDraw.Draw(im)
gs = [('综合练习组', (240, 240, 240), GREY, ['脚趾分开、伸姆趾、伸其余四趾', '脚趾夹小物件、滚网球、毛巾卷', '毛巾拉脚、写字母、扶椅提踵', '侧卧髋外展、弹力带勾脚/踩脚', '跟腱牵伸（直膝、屈膝）', '稳定面和不稳定面平衡', '弹力带内外翻、对角线模式']),
      ('短足练习组', LT, TEAL, ['只做短足练习 4 个动作：', '脚趾分开', '伸其余四趾', '足弓“拱起”（短足）', '伸姆趾', '坐 → 双脚站 → 单脚站']),
      ('短足 + 髋外展组', OR, RED, ['同短足练习组的 4 个动作', '膝上方套一圈弹力带', '做短足的同时双腿向外撑带', '（等长髋外展）', '坐 → 双脚站 → 单脚站', ''])]
for i, (t, c, tc, items) in enumerate(gs):
    x = 20 + i * 460
    dr.rounded_rectangle([x, 20, x + 440, 620], 16, fill=c)
    ctext(dr, x + 220, 44, t, font(38), tc)
    for k, it in enumerate(items): dr.text((x + 30, 130 + k * 66), ('· ' if it and not it.startswith('（') and not it.endswith('：') else '') + it, font=font(28), fill=INK)
im = im.crop((0, 0, W, 640)); dr = ImageDraw.Draw(im)
save(titled(im, '三组各练什么（每周 6 次 × 6 周，3 次有人指导、3 次在家）'), 2)

# ---------- 短足进阶 ----------
W, H = 1400, 700; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
for i, (wk, pos, c, r, col) in enumerate([('第 1～2 周', '坐位', '收缩 5 秒', '放松 2 秒', LT), ('第 3～4 周', '双脚站', '收缩 10 秒', '放松 5 秒', GR), ('第 5～6 周', '单脚站', '收缩 15 秒', '放松 7 秒', OR)]):
    x = 30 + i * 455
    dr.rounded_rectangle([x, 30, x + 430, 330], 16, fill=col)
    ctext(dr, x + 215, 50, wk, font(34), TEAL); ctext(dr, x + 215, 110, pos, font(52), RED)
    ctext(dr, x + 215, 200, c, font(32), INK); ctext(dr, x + 215, 250, r, font(30), GREY)
dr.text((40, 360), '每个动作 12 次 × 3 组', font=font(34), fill=TEAL)
items = ['短足：脚趾不弯，把第 1 跖骨头往脚跟方向收，足长“变短”、足弓拱起', '髋外展版：膝上方套弹力带，做短足的同时双膝向外撑住（不动）',
         '综合练习组同样按 2 周一级加量：收缩 5 → 8 → 10 秒，10 次 × 3 组']
y = 420
for t in items: y = para(dr, 40, y, '· ' + t, 30, 1320, INK, 8) + 16
save(titled(im, '短足练习 2 周一级的进阶'), 3)

save(titled(tile(2, '综合练习：a 滚网球，b 脚趾卷毛巾，c、d 弹力带跖屈，e 弹力带外翻，f 弹力带背伸'), '综合练习组的部分动作'), 4)
save(titled(tile(3, '短足练习（含 / 不含等长髋外展）：a 脚趾分开，b 伸其余四趾，c 双脚站足弓拱起，d 单脚站足弓拱起，e、f 足弓拱起 + 等长髋外展，g 脚趾分开 + 等长髋外展，h 单脚站足弓拱起 + 等长髋外展'), '短足练习与加髋外展'), 5)

# ---------- 流程 ----------
W, H = 1400, 900; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
def box(x0, y0, x1, y1, t, fill=LT, fs=28):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill, outline=(170, 190, 200), width=2)
    lines = t.split('\n'); hh = len(lines) * (fs + 10)
    for i, l in enumerate(lines): ctext(dr, (x0 + x1) / 2, (y0 + y1) / 2 - hh / 2 + i * (fs + 10), l, font(fs))
def down(x, y0, y1):
    dr.line([x, y0, x, y1 - 14], fill=TEAL, width=5); dr.polygon([(x - 12, y1 - 18), (x + 12, y1 - 18), (x, y1)], fill=TEAL)
box(450, 20, 950, 100, '评估 88 人'); box(980, 20, 1380, 160, '排除 43 人\n不符合纳入标准 27\n拒绝参加 16', PK, 26)
dr.line([950, 60, 980, 60], fill=TEAL, width=4)
down(700, 100, 190); box(450, 190, 950, 270, '随机分组 45 人')
dr.line([700, 270, 700, 310], fill=TEAL, width=5); dr.line([233, 310, 1167, 310], fill=TEAL, width=5)
for k, (t, c) in enumerate([('综合练习组', (240, 240, 240)), ('短足练习组', LT), ('短足 + 髋外展组', OR)]):
    cx = 233 + k * 467
    down(cx, 310, 360); box(cx - 210, 360, cx + 210, 470, f'{t}\n15 人，全部接受干预', c, 26)
    down(cx, 470, 530); box(cx - 210, 530, cx + 210, 620, '6 周后随访 15 人', (250, 250, 250), 26)
    down(cx, 620, 680); box(cx - 210, 680, cx + 210, 790, '纳入分析 15 人\n剔除 0 人', GR, 26)
para(dr, 40, 820, '注：原文未报告任何失访或依从性问题', 26, 1300, GREY)
save(titled(im, '受试者流程（按原文图 1 重绘）'), 6)

# ---------- 结果 ----------
fig_, axs = plt.subplots(1, 3, figsize=(13, 4.6), dpi=110)
cols = ['#888888', '#2f8fa0', '#c0504d']; names = ['综合练习', '短足', '短足+髋外展']
data = [('舟骨下沉（毫米）', [(10.84, 8.37), (11.11, 7.92), (11.26, 6.28)], '组间：短足+髋外展 vs 综合练习 P=0.022'),
        ('内外侧晃动（毫米）', [(106.36, 88.54), (109.07, 87.00), (108.38, 69.13)], '组间：短足+髋外展 vs 综合练习 P=0.035'),
        ('晃动面积（平方毫米）', [(420.03, 334.84), (441.35, 299.80), (457.01, 291.72)], '组间差异不显著')]
for ax, (t, ds, note) in zip(axs, data):
    for (a, b), c, nm in zip(ds, cols, names): ax.plot([0, 1], [a, b], '-o', color=c, lw=3, ms=8, label=nm)
    ax.set_xticks([0, 1]); ax.set_xticklabels(['训练前', '6 周后'], fontsize=13); ax.set_title(t, fontsize=14); ax.set_xlim(-0.3, 1.3)
    ax.text(0.5, -0.2, note, transform=ax.transAxes, ha='center', fontsize=11, color='#c0504d' if 'P=' in note else '#555555')
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
axs[0].legend(fontsize=11, frameon=False)
plt.tight_layout(); buf = BytesIO(); fig_.savefig(buf, format='png'); plt.close(fig_)
save(titled(Image.open(buf), '主要结果：三组都改善，加髋外展的降得最多', 1320), 7)

# 封面
c = fig(3, 900); h = c.height; c.crop((0, h // 2, 900, h // 2 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
