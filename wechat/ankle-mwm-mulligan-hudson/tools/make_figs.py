#!/usr/bin/env python3
"""Hudson 等 2017 Mulligan 动态关节松动术治疗急性外侧踝扭伤病例系列：首图为原题直译标题卡；流程卡为编者整理；
原文图 1～3 照片直接使用并加中文说明；5 名患者 NRS、PSFS、DPA 按原文表 4 数字重绘。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
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


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def arrow_down(dr, cx, y0, y1, c=TEAL):
    dr.line([cx, y0, cx, y1 - 14], fill=c, width=6)
    dr.polygon([(cx - 16, y1 - 18), (cx + 16, y1 - 18), (cx, y1)], fill=c)


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * (len(tiles) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def pair(a, b, ca, cb, W=1200):
    """两张照片左右并排，各自上方加说明"""
    w = (W - 14) // 2
    ta, tb = capbox(a, ca, w), capbox(b, cb, w)
    h = max(ta.height, tb.height); out = Image.new('RGB', (W, h), 'white')
    out.paste(ta, (0, 0)); out.paste(tb, (w + 14, 0)); return out


# 原文照片直接使用（图 1 有箭头＝手的位置；图 2 有弹力带＝加压；图 3 贴扎）
F1, F2, F3 = raw(108), raw(106), raw(126)

# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '病例系列 · J Man Manip Ther 2017', font=font(32), fill=TEAL)
for i, t in enumerate(['应用 Mulligan 理念治疗外侧踝关节扭伤的', '新方法：一项探索性病例系列分析']):
    dr.text((70, 130 + i * 72), t, font=font(50), fill=INK)
line, y = '', 300
for w in 'Novel treatment of lateral ankle sprains using the Mulligan concept: an exploratory case series analysis'.split():
    if dr.textlength(line + ' ' + w, font=font(26)) > W - 140: dr.text((70, y), line, font=font(26), fill=GREY); y += 36; line = w
    else: line = (line + ' ' + w).strip()
dr.text((70, y), line, font=font(26), fill=GREY)
dr.line([70, 430, W - 70, 430], fill=(200, 205, 210), width=2)
dr.text((70, 460), 'Hudson R, Baker RT, May J, Reordan D, Nasypany A. J Man Manip Ther 2017;25(5):251-259', font=font(28), fill=GREY)
dr.text((70, 515), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 流程卡
W = 1200; im = Image.new('RGB', (W, 1010), 'white'); dr = ImageDraw.Draw(im)
def box(x0, y0, x1, y1, t, bg, fs=28, c=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=bg)
    lines = t.split('\n'); lh = fs + 10; y = (y0 + y1) / 2 - lh * len(lines) / 2
    for l in lines: ctext(dr, (x0 + x1) / 2, y, l, font(fs), c); y += lh
box(160, 20, 1040, 150, '5 名高中运动员（14～18 岁，4 男 1 女；篮球 3、足球 2）\n受伤 72 小时内的急性外侧踝扭伤，临床判定均为 II 度\n排除骨折（Ottawa 踝关节规则，2 人拍片）', (240, 240, 240), 26)
arrow_down(dr, 600, 154, 200)
box(40, 210, 580, 460, '传统手法（3 人）\n大鱼际放在外踝（腓骨远端）前外侧\n向后上方滑动腓骨\n患者同时主动跖屈 + 内翻\n到末端用治疗师腹部或弹力带加压', LT, 25)
box(620, 210, 1160, 460, '改良手法（2 人）\n手放外踝上方约 5～7.5 cm\n（软组织损伤、原位置按着疼）\n滑动方向、动作要求与传统相同\n全程必须不痛', OR, 25)
box(40, 490, 1160, 610, '每次 3 组 × 10 次，组间休息 ≥ 30 秒；全部由同一名运动防护师操作（上过 2 期 Mulligan 课程）', (234, 230, 246), 25)
box(40, 640, 1160, 800, '同时使用：每次治疗后贴腓骨复位胶布（留到下次）· 压力袜套日夜穿\n伤后 24 小时内冰敷（101 号除外）· 日常生活和训练不限制', PK, 25)
box(40, 830, 1160, 990, '结束治疗标准：PSFS ≥ 9、疼痛 NRS ≤ 1、DPA ≤ 23，且维持 24 小时以上\n结束后 2 周、4 周随访；比赛前可按本人要求继续贴扎', GR, 25)
save(titled(im, '研究怎么做的（编者根据原文整理）'), 2)

save(titled(capbox(F1, 'A 传统手法：大鱼际放在外踝前外侧，向后上方滑动腓骨，另一只手托住踝；B 改良手法：手上移到外踝上方 2～3 英寸（左踝）。箭头为滑动方向'),
            '原文图 1　Mulligan 外踝动态松动术的手放位置'), 3)
save(titled(capbox(F2, '患者在滑动维持下主动跖屈 + 内翻，到活动末端再加压。A 治疗师用腹部加压；B 用弹力带加压'),
            '原文图 2　活动末端加压的两种方式'), 4)
save(titled(capbox(F3, '治疗后沿松动方向贴一条硬质胶布（Leukotape P）帮助维持腓骨位置，留到下次治疗。A 传统贴法；B 改良贴法（左踝）'),
            '原文图 3　腓骨复位贴扎'), 5)

# 结果：5 人逐个画
T = ['初诊', '结束治疗', '结束后 2 周', '结束后 4 周']
D = {'NRS 疼痛（0～10，越低越好）': ([[5, 1, 1, 1], [2, 0, 0, 0], [7, 0, 0, 0], [9, 0, 0, 0], [5, 0, 0, 0]], 10, 1, '结束标准 ≤ 1'),
     'PSFS 功能（0～10，越高越好）': ([[0, 9, 9, 9], [7, 10, 10, 10], [3, 10, 10, 10], [3, 9, 9, 10], [3, 10, 10, 10]], 10, 9, '结束标准 ≥ 9'),
     'DPA 失能（0～64，越低越好）': ([[49, 12, 12, 12], [30, 0, 0, 0], [25, 12, 10, 12], [32, 18, 20, 16], [38, 0, 0, 0]], 55, 23, '结束标准 ≤ 23')}
cols = ['#0b6e82', '#d1495b', '#f39a2b', '#5aa469', '#7b5ea7']
fig, axs = plt.subplots(1, 3, figsize=(15, 6), dpi=100)
for ax, (t, (rows, top, th, lab)) in zip(axs, D.items()):
    for k, (r, c) in enumerate(zip(rows, cols)):
        off = (k - 2) * 0.04 * top / 10
        ax.plot(range(4), [v + off for v in r], 'o-', color=c, lw=2.5, ms=7, label=f'{101 + k} 号')
    ax.axhline(th, color='#999', ls=':', lw=1.5); ax.text(3.1, th + top * 0.02, lab, ha='right', fontsize=12, color='#666')
    ax.set_xticks(range(4)); ax.set_xticklabels(T, fontsize=12); ax.set_ylim(-top * 0.05, top * 1.05)
    ax.set_title(t, fontsize=15); ax.tick_params(labelsize=12); ax.spines[['top', 'right']].set_visible(False)
fig.legend(*axs[0].get_legend_handles_labels(), fontsize=13, frameon=False, loc='upper center', ncol=5)
fig.text(0.5, 0.01, '按原文表 4 逐例数字重绘（线条略错开以免重叠）；从初诊到结束治疗平均 9.2 天、4.4 次治疗', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.04, 1, 0.92)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '结果：5 人全部在 6～16 天内达到结束治疗标准，之后 4 周没有复发', 1200), 6)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), '病例系列 · 急性外侧踝扭伤', font=font(40), fill=TEAL)
dr.text((50, 130), 'Mulligan 动态松动术', font=font(62), fill=INK)
dr.text((50, 220), '急性崴脚能用吗？', font=font(62), fill=INK)
dr.text((50, 318), '5 名 II 度扭伤青少年运动员 · 平均 9 天结束治疗', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
