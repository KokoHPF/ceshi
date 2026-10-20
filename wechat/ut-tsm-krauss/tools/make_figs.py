#!/usr/bin/env python3
"""Krauss 等 2008 上胸椎平移式手法对颈痛和颈椎活动度的即时影响：首图中文标题卡；原文图 1 英文标注改为中文，图 2、3 直接使用；
诊疗流程卡为编者绘制；旋转活动度变化图按原文表 2 和表 4 数值绘制。
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
dr.text((70, 50), '随机临床试验 · 《手法与整骨治疗杂志》2008', font=font(32), fill=TEAL)
dr.text((70, 130), '上胸椎平移式脊柱手法对颈痛', font=font(54), fill=INK)
dr.text((70, 210), '及颈椎活动度的即时影响：', font=font(54), fill=INK)
dr.text((70, 290), '一项随机临床试验', font=font(44), fill=INK)
dr.line([70, 380, W - 70, 380], fill=(200, 205, 210), width=2)
dr.text((70, 410), 'Krauss J, Creighton D, Ely JD, Podlewska-Ely J. J Man Manip Ther 2008;16(2):93-99', font=font(28), fill=GREY)
dr.text((70, 465), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

f1 = relabel(raw(7), [((672, 124, 898, 205), '① 把患者颈椎旋转到\n刚要出现症状的位置', 20, 'l'),
                      ((733, 308, 958, 414), '② 治疗师用左手和胸部\n托住患者头部', 20, 'l'),
                      ((200, 343, 455, 440), '③ 治疗师接触颈椎\n椎板和棘突', 20, 'l'),
                      ((125, 553, 457, 607), '④ 向右旋转该椎体，诱发颈部症状', 20, 'l')])
save(titled(f1, '原文图 1：颈椎症状定位（英文标注已改为中文）', 1200), 2)
save(titled(raw(8), '原文图 2：坐位上胸椎前后向关节游隙测试', 1200), 3)
save(titled(raw(9), '原文图 3：上胸椎平移式手法（双侧关节突关节牵引）', 1200), 4)

# 诊疗流程卡
W = 1200; im = Image.new('RGB', (W, 900), 'white'); dr = ImageDraw.Draw(im)
steps = [('1　确认是颈椎痛', '患者主动转头到疼痛加重，再稍回转到疼痛刚减轻处固定；治疗师从 C7 往上逐节被动旋转椎体，诱发出与主动旋转相同症状的节段即为症状节段', LT, TEAL),
         ('2　找出僵硬的上胸椎节段', '坐位，双臂交叉抱胸；治疗师食指放在待测节段的棘突间隙，手掌其余部分在下方固定，另一侧手臂绕过躯干从前方做前后向平移，T1～T4 中活动受限的节段就是治疗目标', OR, RED),
         ('3　平移式手法', '对僵硬节段做双侧关节突关节牵引：短、直线、被动的向背侧推动，方向大致垂直于关节突关节面、平行于椎间盘平面', GR, (40, 120, 60)),
         ('4　立即复测', '复测颈椎左右旋转角度（颈椎活动度测量仪）和旋转末端疼痛（9 点面部表情疼痛量表）', (240, 240, 240), INK)]
y = 10
for h, t, bg, col in steps:
    tmp = para(ImageDraw.Draw(Image.new('RGB', (W, 500))), 70, y + 74, t, 29, W - 130, gap=13)
    dr.rounded_rectangle([20, y, W - 20, tmp + 12], 14, fill=bg); dr.text((50, y + 18), h, font=font(34), fill=col)
    para(dr, 70, y + 74, t, 29, W - 130, gap=13); y = tmp + 30
im = im.crop((0, 0, W, y))
save(titled(im, '诊疗流程：先定位，再找僵硬节段，再做手法（编者根据原文整理）'), 5)

# 旋转活动度变化（表 2、表 4）
fig, ax = plt.subplots(figsize=(12, 5.8), dpi=110)
x = np.array([0, 1]); w = 0.34
ax.bar(x - w / 2, [-0.6, -0.1], w, yerr=[3.66, 2.33], color='#9aa0a6', edgecolor='#333', capsize=5, label='对照组（不处理，10 人）')
ax.bar(x + w / 2, [7.09, 8.23], w, yerr=[5.83, 7.41], color='#f39a2b', edgecolor='#333', capsize=5, label='手法组（22 人）')
for xi, v in zip(x + w / 2, [7.09, 8.23]): ax.text(xi, 1, f'{v}°', ha='center', fontsize=13, color='white', fontweight='bold')
for i, (m1, m2) in enumerate([(6.82, 17.3), (5.79, 12.0)]):
    ax.hlines(m1, i - .45, i + .45, colors='#2c7fb8', linestyles='--'); ax.text(i + .46, m1, f'原文 MDC {m1}°', va='center', fontsize=12.5, color='#2c7fb8')
    ax.hlines(m2, i - .45, i + .45, colors='#c0392b', linestyles=':'); ax.text(i + .46, m2, f'编者复算 ≈{m2}°', va='center', fontsize=12.5, color='#c0392b')
ax.set_xticks(x); ax.set_xticklabels(['向左旋转', '向右旋转'], fontsize=15); ax.set_xlim(-.6, 1.95)
ax.set_ylabel('治疗前后变化（°）', fontsize=14); ax.axhline(0, color='#333', lw=1); ax.set_ylim(-6, 20)
ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=12)
h_, l_ = ax.get_legend_handles_labels(); fig.legend(h_, l_, fontsize=13, frameon=False, ncol=2, loc='lower center', bbox_to_anchor=(0.5, 0.05))
fig.text(0.5, 0.01, '均值 ± 标准差，取自原文表 2。MDC：最小可测变化。蓝线为原文用变化值标准差算出的数值，红线为编者用基线标准差（表 1）重算的数值', ha='center', fontsize=11, color='#666')
fig.tight_layout(rect=(0, 0.12, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '颈椎旋转角度的即时变化', 1320), 6)

c = raw(9); h = round(c.width * 383 / 900); y0 = int(c.height * .15)
c.crop((0, y0, c.width, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
