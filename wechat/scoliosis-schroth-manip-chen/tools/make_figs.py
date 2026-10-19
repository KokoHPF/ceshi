#!/usr/bin/env python3
"""Chen & Zhang 2025 Schroth 联合脊柱手法治疗青少年特发性脊柱侧凸：首图中文标题卡；原文图 1 十个练习按原图裁切、改为中文标注；
图 2～4 按原文柱状图估读数值重绘为中文；两组方案卡为编者绘制。
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
dr.text((70, 60), '回顾性研究 · 《巴基斯坦医学科学杂志》2025', font=font(32), fill=TEAL)
for i, t in enumerate(['青少年特发性脊柱侧凸：', 'Schroth 练习 + 脊柱手法']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '温州市中医院 100 例，6 个月，对比单做 Schroth', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Chen H, Zhang C. Pak J Med Sci 2025;41(2):409-414', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1：十个 Schroth 练习，按面板裁切后重新排版，字母标注改为中文
f1 = raw(4)
P = {'a': (0, 0, 333, 447), 'b': (362, 0, 968, 447), 'c': (998, 15, 1590, 447), 'd': (1618, 10, 1949, 447),
     'e': (0, 525, 287, 975), 'f': (310, 525, 660, 975), 'g': (686, 522, 1002, 975), 'h': (1022, 525, 1292, 975),
     'i': (1324, 520, 1660, 975), 'j': (1680, 518, 1949, 978)}
LAB = {'a': '① 旋转呼吸\n与伸展', 'b': '② 侧卧位\n肩部反向牵引', 'c': '③ 侧卧位\n“肌肉圆柱”', 'd': '④ 帆式练习',
       'e': '⑤ 半跪位\n“肌肉圆柱”', 'f': '⑥ 坐球练习', 'g': '⑦ 侧方悬挂', 'h': '⑧ 俯卧位\n肩部反向牵引',
       'i': '⑨ 突髋练习', 'j': '⑩ Schroth\n步态练习'}


def row(keys, W=1200, gap=10, ph=None):
    ims = [f1.crop(P[k]) for k in keys]
    hh = 400; ims = [m.resize((round(m.width * hh / m.height), hh), Image.LANCZOS) for m in ims]
    tw = sum(m.width for m in ims) + gap * (len(ims) - 1); s = W / tw
    ims = [m.resize((round(m.width * s), round(hh * s)), Image.LANCZOS) for m in ims]
    h = ims[0].height; out = Image.new('RGB', (W, h + 84), 'white'); d = ImageDraw.Draw(out); x = 0
    for k, m in zip(keys, ims):
        out.paste(m, (x, 0)); cx = x + m.width / 2
        for i, l in enumerate(LAB[k].split('\n')): ctext(d, cx, h + 8 + i * 34, l, font(26))
        x += m.width + gap
    return out


save(board([row('abcd')], 'Schroth 练习（一）'), 2)
save(board([row('efg'), row('hij')], 'Schroth 练习（二）'), 3)

# 两组方案卡
W = 1200; im = Image.new('RGB', (W, 1010), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 10, W - 20, 250], 14, fill=LT)
dr.text((50, 30), '两组都做：Schroth 练习', font=font(36), fill=TEAL)
y = 92
for t in ['每次 90 分钟，每周 3 次，连续 6 个月',
          '基础：三维旋转呼吸、骨盆矫正、牵伸、基本张力与体位摆放',
          '练习：肩部反向牵引、肌肉圆柱、侧方悬挂、帆式、突髋、Schroth 步态']:
    y = para(dr, 70, y, '· ' + t, 30, W - 130, gap=16)
dr.rounded_rectangle([20, 270, W - 20, 1000], 14, fill=OR)
dr.text((50, 290), '研究组另加：脊柱手法（每周 2 次，6 个月）', font=font(36), fill=RED)
steps = [('1 点穴按摩　约 5 分钟', '沿足太阳膀胱经和督脉自上而下按压，督脉从大椎到尾骶；重点按委中、气海、命门、殷门和环跳穴，频率约每分钟 40 次'),
         ('2 解痉理筋　10 分钟', '先站立找出侧凸处最紧张、痉挛的肌肉和韧带；再俯卧，用掌根滚法、肘揉、振法放松脊柱两侧'),
         ('3 整骨手法　约 5 分钟', '沿侧弯处依次推拉肌肉和棘突，动作轻柔连贯，力度以能耐受为度'),
         ('4 旋转扳法　1 分钟 × 2 次', '俯卧，治疗师站在侧凸一侧，一手按住腰部命门，一手拉肩，两手同时用力使脊柱旋转、伸展到最大'),
         ('5 抖动放松　2 分钟', '固定腰部，双手轻轻抖动肩部')]
y = 360
for h, t in steps:
    dr.text((60, y), h, font=font(32), fill=INK); y = para(dr, 90, y + 46, t, 28, W - 150, fill=GREY, gap=12) + 14
save(titled(im, '两组到底做了什么（编者根据原文整理）'), 4)

# 图 2～4 重绘（原文只给柱状图，数值为编者按图估读）
C1, C2 = '#f39a2b', '#8f9296'


def bars(panels, title, n):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5.6), dpi=110)
    for ax, (yl, ylim, v) in zip(axs, panels):
        x = np.array([0, 1.4]); w = 0.5
        for j, (c, lab) in enumerate([(C1, '研究组（Schroth + 手法）'), (C2, '对照组（单做 Schroth）')]):
            m = [v[0][j][0], v[1][j][0]]; s = [v[0][j][1], v[1][j][1]]
            ax.bar(x + (j - .5) * w * 1.05, m, w, yerr=s, color=c, edgecolor='#333', capsize=5, label=lab, error_kw={'lw': 1.2})
            ax.text(x[1] + (j - .5) * w * 1.05, m[1] + s[1] + ylim * .02, 'ab' if j == 0 else 'a', ha='center', fontsize=14)
        ax.set_xticks(x); ax.set_xticklabels(['治疗前', '治疗 6 个月后'], fontsize=15); ax.set_ylabel(yl, fontsize=15)
        ax.set_ylim(0, ylim); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=13)
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', bbox_to_anchor=(0.5, 0.05), ncol=2, frameon=False, fontsize=14)
    fig.text(0.5, 0.005, 'a：与本组治疗前比 P < 0.05；b：与对照组比 P < 0.05。柱高为编者按原图估读，非原文精确数值', ha='center', fontsize=12, color='#666')
    fig.tight_layout(rect=(0, 0.13, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
    save(titled(Image.open(buf).convert('RGB'), title, 1320), n)


bars([('最大 Cobb 角（°）', 20, [((15.1, 3.2), (14.4, 3.2)), ((8.8, 2.4), (10.5, 2.5))]),
      ('锁骨角（°）', 3, [((2.27, .52), (2.17, .47)), ((1.56, .50), (1.79, .41))])], '图 2　最大 Cobb 角和锁骨角（按原图重绘）', 5)
bars([('躯干旋转角 ATR（°）', 8, [((5.55, 1.35), (5.32, 1.13)), ((3.75, 1.28), (4.35, 1.22))]),
      ('椎体旋转（原文单位写作 °）', 3, [((1.90, .58), (1.97, .52)), ((1.38, .51), (1.70, .48))])], '图 3　躯干旋转角和椎体旋转（按原图重绘）', 6)
bars([('腰椎后伸（°）', 30, [((14.6, 2.5), (15.3, 3.4)), ((24.0, 4.1), (20.8, 3.3))]),
      ('腰椎前屈（°）', 100, [((73.7, 7.2), (72.8, 8.2)), ((85.8, 8.1), (81.5, 8.3))])], '图 4　腰椎屈伸活动度（按原图重绘）', 7)

# 封面 900×383：取图 1c 侧卧位练习
c = f1.crop((998, 110, 1590, 362)).resize((900, 383), Image.LANCZOS); c.save(f'{OUT}/cover.jpg', quality=90)
