#!/usr/bin/env python3
"""Kim 等 2024 徒手淋巴引流联合动态松动与肌筋膜释放：首图中文标题卡；原文图 1 流程图中文重绘；原文图 2～6 直接截取使用并加中文标注；
三组方案卡为编者绘制；伸展距离变化图按原文表 3 数值绘制。
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


def clip(n, r, dpi=250):
    pm = doc[n - 1].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*r))
    return Image.open(BytesIO(pm.tobytes('png'))).convert('RGB')


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '随机对照试验 · 《医疗保健》2024', font=font(32), fill=TEAL)
dr.text((70, 125), '徒手淋巴引流联合动态松动与肌筋膜释放', font=font(48), fill=INK)
dr.text((70, 195), '对小腿肌肉短缩成人动态平衡中', font=font(48), fill=INK)
dr.text((70, 265), '肌肉活动的影响', font=font(48), fill=INK)
dr.line([70, 370, W - 70, 370], fill=(200, 205, 210), width=2)
dr.text((70, 400), 'Kim SY, Kim KS, Hwang YI. Healthcare 2024;12(10):1038', font=font(30), fill=GREY)
dr.text((70, 455), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1 流程图中文重绘
W = 1200; im = Image.new('RGB', (W, 1120), 'white'); dr = ImageDraw.Draw(im)
def box(x0, y0, x1, y1, lines, fill=LT, fs=27):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill, outline=(150, 170, 175), width=2)
    lh = fs + 12; y = (y0 + y1) / 2 - lh * len(lines) / 2 + 4
    for l in lines: ctext(dr, (x0 + x1) / 2, y, l, font(fs)); y += lh
def arr(x, y0, y1):
    dr.line([x, y0, x, y1], fill=GREY, width=3); dr.polygon([(x - 9, y1 - 14), (x + 9, y1 - 14), (x, y1)], fill=GREY)
box(300, 20, 700, 110, ['评估是否符合条件', '（21 人，34 只脚）'])
box(760, 20, 1180, 150, ['排除', '筛查不符合：4 人，7 只脚', '中途退出：1 人，1 只脚'], fill=PK, fs=25)
dr.line([700, 65, 760, 65], fill=GREY, width=3)
arr(500, 110, 170); box(300, 170, 700, 260, ['随机分组', '（16 人，26 只脚）'])
arr(500, 260, 300)
box(80, 300, 1120, 420, ['治疗前测试：改良弓步测背伸活动度', '改良星形偏移平衡测试（惯性传感器、表面肌电、足底压力板）'], fill=(240, 240, 240), fs=26)
for cx in (200, 600, 1000): arr(cx, 420, 470)
box(30, 470, 380, 640, ['第 1 组（MR）', '动态松动 + 肌筋膜释放', '5 人，8 只脚'], fill=OR, fs=26)
box(425, 470, 775, 640, ['第 2 组（MD）', '动态松动 + 淋巴引流', '6 人，9 只脚'], fill=GR, fs=26)
box(820, 470, 1170, 640, ['第 3 组（MRD）', '动态松动 + 肌筋膜释放', '+ 淋巴引流；5 人，9 只脚'], fill=LT, fs=26)
for cx in (200, 600, 1000): arr(cx, 640, 690)
box(80, 690, 1120, 810, ['治疗后立即测试：同治疗前'], fill=(240, 240, 240), fs=26)
arr(600, 810, 860)
box(330, 860, 870, 1100, ['统计分析', '正态性检验、Kruskal-Wallis 检验', 'Bonferroni 校正、方差分析', '配对 t 检验'], fill=(250, 250, 250), fs=26)
save(titled(im, '原文图 1：研究流程（编者中文重绘）'), 2)

# 三组方案卡
im = Image.new('RGB', (W, 1150), 'white'); dr = ImageDraw.Draw(im)
items = [('动态松动（三组都做，5 分钟）', '先把脚放在 40 cm 高的椅子上，做闭链最大背伸；再用无弹性胶带把距骨/踝向后下方“固定”，带着胶带在跑步机上以 4.5 km/h、坡度 6° 走 5 分钟', OR, RED),
         ('肌筋膜释放（MR、MRD 组，5 分钟）', '用网球放在足底筋膜和小腿肌肉下，用体重加压放松：足底 2 分钟、小腿 3 分钟', GR, (40, 120, 60)),
         ('徒手淋巴引流（MD 组 15 分钟，MRD 组 10 分钟）', '按 Vodder 法：先轻抚整条腿，再依次处理大腿、腹股沟淋巴结、膝、小腿、跟腱、踝、足背和足弓，最后轻抚收尾；由 1 名受过 40 小时训练的研究者完成', LT, TEAL)]
y = 10
for h, t, bg, col in items:
    yy = y + 76; tmp = para(ImageDraw.Draw(Image.new('RGB', (W, 400))), 70, yy, t, 29, W - 130, gap=14)
    dr.rounded_rectangle([20, y, W - 20, tmp + 14], 14, fill=bg); dr.text((50, y + 20), h, font=font(34), fill=col)
    para(dr, 70, yy, t, 29, W - 130, gap=14); y = tmp + 34
dr.rounded_rectangle([20, y, W - 20, y + 190], 14, fill=(240, 240, 240))
dr.text((50, y + 20), '总时长', font=font(34), fill=INK)
for i, t in enumerate(['MR 组：动态松动 + 肌筋膜释放 = 10 分钟', 'MD 组：动态松动 + 淋巴引流 = 20 分钟；MRD 组：三者合计 = 20 分钟']):
    dr.text((70, y + 76 + i * 46), '· ' + t, font=font(29), fill=INK)
im = im.crop((0, 0, W, y + 200))
save(titled(im, '三组到底做了什么（编者根据原文整理，各做 1 次）'), 3)

f6 = clip(7, (155, 72, 562, 308))
save(titled(capbox(f6, '（a）无弹性胶带把踝向后下方滑动；（b）带着胶带在坡道跑步机上行走；（c）网球放松足底筋膜；（d）网球放松小腿肌肉；（e）徒手淋巴引流'), '原文图 6：三种干预的做法'), 4)
f2 = clip(4, (160, 186, 367, 314)); f3 = clip(5, (88, 84, 552, 396))
save(board([capbox(f2, '原文图 2：改良弓步测试（a 治疗前，b 治疗后），用手机倾角仪测背伸角度'),
            capbox(f3, '原文图 3：改良星形偏移平衡测试。a→b 第 1 段（前方去程）、b→c 第 2 段（前方回程）、c→d 第 3 段（后内去程）、d→e 第 4 段（后内回程）、e→f 第 5 段（后外去程）、f→a 第 6 段（后外回程）')], '评估方法'), 5)
f4 = clip(5, (160, 452, 550, 605)); f5 = clip(6, (160, 72, 575, 295))
save(board([capbox(f4, '原文图 4：（a）惯性传感器；（b）表面肌电；（c）足底压力平台'),
            capbox(f5, '原文图 5：（a）惯性传感器位置：①两侧髂后上棘之间 ②大腿 ③小腿 ④足；（b）肌电电极位置：①胫骨前肌 ②腓肠肌外侧头 ③腓肠肌内侧头 ④腓骨长肌')], '测量设备与电极位置'), 6)

# 伸展距离变化（表 3）
fig, ax = plt.subplots(figsize=(12, 5.8), dpi=110)
G = ['MR 组\n（松动+释放）', 'MD 组\n（松动+引流）', 'MRD 组\n（三者合用）']
D = {'前方': [86.70 - 89.69, 90.55 - 84.71, 93.68 - 91.63], '后内': [84.22 - 80.91, 87.23 - 82.77, 89.88 - 83.06], '后外': [97.62 - 96.21, 97.15 - 87.68, 104.37 - 100.28]}
SIG = {'前方': [0, 0, 1], '后内': [0, 0, 1], '后外': [0, 1, 1]}
x = np.arange(3); w = 0.26
for j, ((k, v), c) in enumerate(zip(D.items(), ['#4c8fbf', '#f39a2b', '#6aa96a'])):
    xx = x + (j - 1) * w; ax.bar(xx, v, w, color=c, edgecolor='#333', label=k)
    for xi, vi, s in zip(xx, v, SIG[k]):
        ax.text(xi, vi + (0.3 if vi >= 0 else -0.9), f'{vi:+.1f}' + ('*' if s else ''), ha='center', fontsize=12)
ax.axhline(0, color='#333', lw=1); ax.set_xticks(x); ax.set_xticklabels(G, fontsize=14)
ax.set_ylabel('最大伸展距离变化（腿长 %）', fontsize=14); ax.set_ylim(-5, 12); ax.spines[['top', 'right']].set_visible(False)
ax.tick_params(axis='y', labelsize=12); ax.legend(fontsize=13, frameon=False, ncol=3, loc='upper left')
fig.text(0.5, 0.01, '治疗后减治疗前，按原文表 3 计算；* 组内配对 t 检验 P < 0.05', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.04, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '星形偏移平衡测试：治疗后伸展距离的变化', 1320), 7)

# 封面 900×383：图 6 下排（网球放松小腿与淋巴引流）
y0, y1 = int(f6.height * .57), int(f6.height * .90); h = y1 - y0; w = round(h * 900 / 383); x0 = int(f6.width * .30)
f6.crop((x0, y0, min(f6.width, x0 + w), y1)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
