#!/usr/bin/env python3
"""Küçük 等 2024 手法治疗对健康年轻人呼吸功能的即时影响：首图中文标题卡；原文图 1 流程图按原图中文重绘；
原文图 2～4 三个手法照片（模糊床单上的英文/土耳其文印章）；方案卡为编者绘制；PEF 结果按原文表 2 数值重绘。
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
dr.text((70, 60), '随机对照试验 · 《科学报告》2024', font=font(32), fill=TEAL)
for i, t in enumerate(['做一次胸椎手法 + 膈肌松动，', '呼吸功能马上会变好吗？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '104 名健康大学生，真手法 vs 假手法，治疗前后测肺功能', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Küçük E, et al. Sci Rep 2024;14:17419', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1：流程图中文重绘
W = 1200; im = Image.new('RGB', (W, 1180), 'white'); dr = ImageDraw.Draw(im)


def box(x0, y0, x1, y1, lines, fill=LT, fs=28, col=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill, outline=(150, 170, 175), width=2)
    lh = fs + 12; y = (y0 + y1) / 2 - lh * len(lines) / 2 + 4
    for l in lines: ctext(dr, (x0 + x1) / 2, y, l, font(fs), col); y += lh


def arrow(x0, y0, x1, y1):
    dr.line([x0, y0, x1, y1], fill=GREY, width=3)
    if x0 == x1: dr.polygon([(x1 - 9, y1 - 14), (x1 + 9, y1 - 14), (x1, y1)], fill=GREY)
    else: dr.polygon([(x1 - 14, y1 - 9), (x1 - 14, y1 + 9), (x1, y1)], fill=GREY)


for y, t in [(40, '入组'), (400, '分组'), (650, '干预'), (830, '复测'), (960, '分析')]:
    dr.rounded_rectangle([20, y, 190, y + 56], 10, fill=TEAL); ctext(dr, 105, y + 12, t, font(28), 'white')
box(300, 30, 720, 120, ['报名并评估是否符合条件', '（n = 207）'])
box(800, 150, 1180, 300, ['排除（n = 103）', '不符合纳入标准 85 人', '报名后拒绝参加 18 人'], fill=PK, fs=26)
arrow(510, 120, 510, 340); dr.line([510, 225, 785, 225], fill=GREY, width=3); arrow(770, 225, 800, 225)
box(260, 340, 760, 470, ['纳入（n = 104）', '社会人口学问卷 + 肺功能测试'])
arrow(510, 470, 510, 520)
box(330, 520, 690, 590, ['随机分组（n = 104）'])
dr.line([435, 610, 965, 610], fill=GREY, width=3)
dr.line([510, 590, 510, 610], fill=GREY, width=3)
arrow(435, 610, 435, 650); arrow(965, 610, 965, 650)
box(230, 650, 640, 780, ['第 1 组：手法治疗组', '（n = 52）'], fill=OR)
box(760, 650, 1170, 780, ['第 2 组：假手法组', '（n = 52）'], fill=GR)
arrow(435, 780, 435, 830); arrow(965, 780, 965, 830)
box(230, 830, 640, 920, ['干预后 5 分钟内复测肺功能'], fs=26)
box(760, 830, 1170, 920, ['干预后 5 分钟内复测肺功能'], fs=26)
arrow(435, 920, 435, 960); arrow(965, 920, 965, 960)
box(230, 960, 640, 1040, ['纳入分析（n = 52）'], fill=OR)
box(760, 960, 1170, 1040, ['纳入分析（n = 52）'], fill=GR)
dr.text((30, 1090), '无失访、无退出，两组 52 人全部纳入分析', font=font(26), fill=GREY)
save(titled(im, '图 1　受试者流程（按原图中文重绘）'), 2)

# 图 2～4：三个手法照片，模糊床单上的印章文字
f2 = blur(raw(101), [(16, 430, 318, 524)], 9)
save(titled(f2, '图 2　胸椎推扳手法（仰卧位）', 1200), 3)
f3 = blur(raw(111), [(850, 0, 1000, 150)], 14)
f3 = f3.crop((0, int(f3.height * .12), f3.width, int(f3.height * .12) + round(f3.width * .75)))
save(titled(f3, '图 3　胸椎松动（俯卧位，肋横突关节）', 1200), 4)
f4 = raw(110); f4 = f4.crop((0, int(f4.height * .2), f4.width, int(f4.height * .2) + round(f4.width * .75)))
save(titled(f4, '图 4　膈肌松动（仰卧位，双手抓下肋）', 1200), 5)

# 两组方案卡
W = 1200; im = Image.new('RGB', (W, 960), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 10, W - 20, 620], 14, fill=OR)
dr.text((50, 30), '手法治疗组：只做 1 次，三个技术依次做', font=font(36), fill=RED)
steps = [('1 胸椎推扳（thrust）　1 次', '仰卧，双臂交叉抱胸；治疗师一手垫在胸椎横突处，另一手扶住肘部；用屈曲加后向滑动找到组织“卡住”的位置，在受试者呼气时用身体向下快速推 1 下'),
         ('2 胸椎松动　每个肋横突关节 30 秒', '俯卧；一手豌豆骨一侧和两指放在肋横突关节外侧，另一手放在关节对侧；做顺时针、逆时针方向的后前向（PA）椎间松动'),
         ('3 膈肌松动　有节律地做 2～4 分钟', '仰卧，双手抓住下肋；先用左手把右侧下肋往上、往中线推，再用右手把左侧下肋往上、往中线推，交替进行，受试者正常呼吸')]
y = 100
for h, t in steps:
    dr.text((60, y), h, font=font(32), fill=INK); y = para(dr, 90, y + 48, t, 28, W - 150, fill=GREY, gap=12) + 22
dr.rounded_rectangle([20, 640, W - 20, 950], 14, fill=GR)
dr.text((50, 660), '假手法组：手放同样位置，但不用力', font=font(36), fill=(40, 120, 60))
y = 720
for t in ['同样的体位、同样的手部接触，总时长与手法组相同',
          '不施加任何力量或动作，只观察呼吸、触摸肌肉',
          '两组都在干预前和干预后 5 分钟内各测一次肺功能']:
    y = para(dr, 70, y, '· ' + t, 30, W - 130, gap=16)
save(titled(im, '两组到底做了什么（编者根据原文整理）'), 6)

# PEF 结果，按原文表 2 数值重绘
C1, C2 = '#f39a2b', '#8f9296'
fig, axs = plt.subplots(1, 2, figsize=(12, 5.6), dpi=110, gridspec_kw={'width_ratios': [1.5, 1]})
ax = axs[0]; x = np.array([0, 1.4]); w = 0.5
for j, (c, lab, m, s) in enumerate([(C1, '手法治疗组', [296.3, 316.1], [110.8, 119.1]), (C2, '假手法组', [337.1, 324.5], [93.3, 89.2])]):
    xx = x + (j - .5) * w * 1.05
    ax.bar(xx, m, w, yerr=s, color=c, edgecolor='#333', capsize=5, label=lab, error_kw={'lw': 1.2})
    for xi, mi in zip(xx, m): ax.text(xi, 40, f'{mi}', ha='center', fontsize=13, color='white' if j == 0 else 'black')
ax.set_xticks(x); ax.set_xticklabels(['干预前', '干预后'], fontsize=15); ax.set_ylabel('呼气峰流量 PEF（原文未注单位）', fontsize=14)
ax.set_ylim(0, 480); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=13)
ax.set_title('两组 PEF：干预前后', fontsize=15)
ax = axs[1]
ax.bar([0, 1], [19.8, -12.6], 0.55, yerr=[58.3, 33.6], color=[C1, C2], edgecolor='#333', capsize=5, error_kw={'lw': 1.2})
ax.axhline(0, color='#333', lw=1)
for xi, v in [(0, 19.8), (1, -12.6)]: ax.text(xi + .32, v, f'{v:+.1f}', va='center', fontsize=14)
ax.set_xticks([0, 1]); ax.set_xticklabels(['手法治疗组', '假手法组'], fontsize=14); ax.set_ylim(-60, 90)
ax.set_title('PEF 变化量（后 - 前）', fontsize=15); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=13)
h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', bbox_to_anchor=(0.5, 0.05), ncol=2, frameon=False, fontsize=14)
fig.text(0.5, 0.005, '误差线为标准差。组内：手法组 P = 0.018，假手法组 P = 0.002；变化量组间比较 P = 0.001。数值取自原文表 2', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.13, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '主要结果：只有 PEF 有差别（按原文表 2 重绘）', 1320), 7)

# 封面 900×383：取图 3 胸椎松动双手
c = raw(111); c = c.crop((0, int(c.height * .30), c.width, int(c.height * .30) + round(c.width * 383 / 900)))
c.resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
