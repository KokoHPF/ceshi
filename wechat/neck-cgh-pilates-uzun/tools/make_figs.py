#!/usr/bin/env python3
"""Uzun 等 2024 颈椎松动联合临床普拉提治疗颈源性头痛：首图中文标题卡；原文图 1 CONSORT 流程图按原图版式用中文重绘；
原文图 2 动作照片直接使用（图中只有 A～L 字母），加中文图注；干预方案卡和主要结果图为编者根据原文整理绘制。
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
dr.text((70, 45), '随机对照试验 · 《Medicina》2024', font=font(32), fill=TEAL)
dr.text((70, 115), '颈椎松动联合临床普拉提运动对颈源性头痛', font=font(50), fill=INK)
dr.text((70, 185), '患者疼痛、肌肉僵硬度及头颈部血流的影响：', font=font(50), fill=INK)
dr.text((70, 255), '随机对照试验', font=font(50), fill=INK)
dr.line([70, 350, W - 70, 350], fill=(200, 205, 210), width=2)
dr.text((70, 378), 'Uzun M, İkidağ MA, Ekmekyapar Fırat Y, Ergun N, Akbayrak T.', font=font(28), fill=GREY)
dr.text((70, 423), 'Medicina. 2024;60(6):852', font=font(28), fill=GREY)
dr.text((70, 485), '编者中文重排，仅作学术交流（原文 CC BY 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1 CONSORT：按原图坐标（1848×1709）缩放到 1200 宽重绘
S = 1200 / 1848; im = Image.new('RGB', (1200, round(1680 * S)), 'white'); dr = ImageDraw.Draw(im)
z = lambda *v: [round(a * S) for a in v]; BL = (168, 198, 250); BLT = (70, 110, 170)


def box(x0, y0, x1, y1, lines, fs=30):
    dr.rectangle(z(x0, y0, x1, y1), outline=INK, width=2); y = y0 + 22
    for l in lines: dr.text(z(x0 + 24, y), l, font=font(fs * S * 1.0), fill=INK); y += fs * 1.55


def stage(x0, y0, x1, y1, t):
    dr.rounded_rectangle(z(x0, y0, x1, y1), round(14 * S), fill=BL, outline=(60, 80, 120), width=2)
    f = font(34 * S); w = dr.textlength(t, font=f); dr.text(((x0 + x1) / 2 * S - w / 2, (y0 + y1) / 2 * S - f.size / 2 - 2), t, font=f, fill=BLT)


def arrow(x0, y0, x1, y1):
    dr.line(z(x0, y0, x1, y1), fill=INK, width=2); a = 14
    if x0 == x1: dr.polygon(z(x1, y1, x1 - a / 2, y1 - a, x1 + a / 2, y1 - a), fill=INK)
    else: dr.polygon(z(x1, y1, x1 - a, y1 - a / 2, x1 - a, y1 + a / 2), fill=INK)


stage(48, 40, 455, 125, '纳入')
box(695, 60, 1222, 165, ['评估是否符合条件（n=37）'])
box(1130, 197, 1778, 390, ['排除（n=6）', '◆ 不符合纳入标准（n=1）', '◆ 拒绝参加（n=5）'])
dr.line(z(960, 165, 960, 467), fill=INK, width=2); arrow(960, 318, 1128, 318)
box(757, 467, 1181, 557, ['随机分组（n=31）'])
arrow(960, 557, 960, 620); dr.line(z(400, 622, 1446, 622), fill=INK, width=2); arrow(400, 622, 400, 724); arrow(1446, 622, 1446, 728)
box(24, 726, 772, 982, ['分配到 CM 组（n=15）*', '◆ 接受了分配的干预（n=14）', '◆ 未接受分配的干预', '   （担心新冠）（n=1）'])
box(1072, 730, 1818, 987, ['分配到 CM+CPE 组（n=16）', '◆ 接受了分配的干预（n=14）', '◆ 未接受分配的干预', '   （担心新冠）（n=2）'])
stage(712, 682, 1089, 758, '分配')
arrow(400, 982, 400, 1110); arrow(1444, 987, 1444, 1110)
box(24, 1112, 772, 1325, ['失访（n=0）', '因没有时间中止干预（n=1）'])
box(1072, 1112, 1818, 1320, ['失访（n=0）', '因没有时间中止干预（n=2）'])
stage(730, 1046, 1108, 1126, '随访')
arrow(408, 1330, 408, 1425); arrow(1450, 1322, 1450, 1425)
box(14, 1427, 763, 1622, ['纳入分析（n=13）', '◆ 排除出分析（n=0）'])
box(1072, 1427, 1818, 1622, ['纳入分析（n=12）', '◆ 排除出分析（n=0）'])
stage(736, 1365, 1111, 1440, '分析')
save(capbox(im, '原文图 1  CONSORT 流程图（编者中文重绘）。CM：颈椎松动；CPE：临床普拉提运动。* 原图此处写作“CP intervention”，按正文应为 CM 组'), 2)

blocks = [('两组共同：颈椎松动（Cyriax 技术，约 10 分钟）', '松动前先做椎基底动脉（VBA）试验，全部阴性\n仰卧位依次做：桥式手法、手法牵引、牵引下旋转、牵引下前后滑动、侧向滑动、斜方肌手法牵伸，每种技术 8～10 次', LT, TEAL),
          ('CM+CPE 组另加：临床普拉提（APPI 体系）', '先教会 5 个基本要素：侧向呼吸、脊柱中立位与核心启动、肩带定位、胸廓定位、头颈定位；训练中用口头和触觉提示维持\n12 个动作（见原文图 2），每个 8～10 次；由 APPI 认证的物理治疗师现场指导\n目标：增强颈深屈肌、放松颈周肌肉、提高脊柱稳定性和灵活性', GR, (40, 130, 60)),
          ('频次', '每周 3 次，共 6 周；全部由同一名物理治疗师操作', OR, (200, 110, 30)),
          ('评估（治疗前后）', '头痛频率（次 / 月）、强度（VAS，cm）、止痛药用量（次 / 月）\n肌肉僵硬度：枕下肌、上斜方肌、胸锁乳突肌，左右各测 3 次（Myoton 肌肉测量仪，N/m）\n血流：颈内动脉、椎动脉收缩期峰值和舒张末期流速（多普勒超声，由放射科医生测）', PK, RED)]
save(card(1200, '干预方案（编者根据原文整理）', blocks), 3)

save(capbox(Image.open(os.path.join(SRC, 'f2.png')),
            '原文图 2  临床普拉提动作。A 上背部热身；B 侍者式（Dumb Waiter）；C 胸部牵伸；D 开瓶器式（Corkscrew）；E 上半身卷动；'
            'F 侧卧开臂 1 级；G 双腿伸展 1 级；H 天鹅潜水 1～3 级；I 蛙泳预备 1（2 级）；J 脊柱扭转；K 猫式伸展；L 主动斜方肌牵伸'), 4)

fig, ax = plt.subplots(1, 3, figsize=(12, 4.6), dpi=100)
data = [('头痛强度（VAS，cm）', (5.81, 1.74), (7.43, 1.88)), ('头痛频率（次 / 月）', (13.38, 3.62), (17.08, 3.58)),
        ('止痛药（次 / 月）', (12.23, 2.62), (13.75, 2.42))]
for a, (t, cm, cp) in zip(ax, data):
    x = np.arange(2); w = 0.36
    b1 = a.bar(x - w / 2, cm, w, color='#7fb3bf', label='CM 组（13 人）'); b2 = a.bar(x + w / 2, cp, w, color='#00788c', label='CM+CPE 组（12 人）')
    for bars in (b1, b2):
        for r in bars: a.text(r.get_x() + r.get_width() / 2, r.get_height(), f'{r.get_height():.2f}', ha='center', va='bottom', fontsize=10.5)
    a.set_xticks(x); a.set_xticklabels(['治疗前', '6 周后'], fontsize=12); a.set_title(t, fontsize=13)
    a.spines[['top', 'right']].set_visible(False); a.grid(axis='y', alpha=0.3); a.set_ylim(0, max(cm + cp) * 1.18)
h, l = ax[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', ncol=2, fontsize=12, frameon=False)
fig.tight_layout(rect=(0, 0.08, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '疼痛相关结果（编者根据原文表 2 均值绘制）。两组治疗后都明显下降；只有头痛强度的下降幅度组间有差异（P=0.025），'
                                              '但 CM+CPE 组治疗前强度高出 1.6 cm，治疗后两组几乎一样（1.74 对 1.88）'), 5)

c = Image.open(os.path.join(SRC, 'f2.png')).crop((476, 45, 1358, 420)).resize((900, 383), Image.LANCZOS)
c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
