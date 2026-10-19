#!/usr/bin/env python3
"""Ibraheem 等 2026 足底筋膜炎多模式康复 RCT：首图中文标题卡；两组方案对比卡、提踵进阶卡、短足练习卡、结果图、流程图为编者绘制；
原文图 1～6 加中文标注（超声图英文改为中文，裤子品牌标签已模糊）。
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
X = {1: 79, 2: 111, 3: 124, 4: 123, 5: 139, 6: 138}
BL = {3: [(43, 252, 92, 302)]}


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def fig(n, W):
    im = Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB'); s = im.width / 600
    for b in BL.get(n, []):
        bb = tuple(int(v * s) for v in b)
        im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(12 * s)), bb[:2])
    if n == 1:
        d = ImageDraw.Draw(im)
        for box, (x, y), t in [((378, 143, 505, 172), (385, 145), '足底筋膜'), ((138, 214, 252, 245), (150, 217), '跟骨'), ((82, 318, 135, 340), (88, 318), '右侧')]:
            d.rectangle(tuple(int(v * s) for v in box), fill=(12, 12, 16))
            d.text((int(x * s), int(y * s)), t, font=font(int(22 * s)), fill='white')
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200, maxh=900):
    im = fig(n, W)
    if im.height > maxh: im = im.resize((round(im.width * maxh / im.height), maxh), Image.LANCZOS)
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


def board(items, title, W=1200, maxh=900):
    tiles = [tile(n, c, W, maxh) for n, c in items]
    H = sum(t.height for t in tiles) + 14 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


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
dr.text((70, 60), '随机对照试验 · 《BMC 肌肉骨骼疾病》2026', font=font(32), fill=TEAL)
for i, t in enumerate(['足底筋膜炎 + 扁平足：', '贴扎、短足练习、单腿提踵一起上']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '多模式康复 vs 常规康复，8 周、48 人', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Ibraheem MR, Abd El-Moneim MA, Ibrahim MM. BMC Musculoskelet Disord 2026;27:168', font=font(28), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 方案对比 ----------
W = 1400; im = Image.new('RGB', (W, 900), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 300], 16, fill=LT)
dr.text((50, 36), '两组都做（每周 3 次 × 8 周）', font=font(36), fill=TEAL)
for i, t in enumerate(['足底筋膜专项牵伸 + 腓肠肌、比目鱼肌牵伸（每天 2 次，每块肌肉 3 组 × 3 次 × 30 秒）',
                       '距小腿关节松动（Ⅰ级向下牵引 + 距骨后滑）', '动态关节松动（距骨后滑 + 向前弓步）', '距下关节内、外侧滑动（每种技术 1.5 分钟）']):
    dr.text((60, 100 + i * 48), '· ' + t, font=font(28), fill=INK)
dr.rounded_rectangle([20, 330, 690, 880], 16, fill=(240, 240, 240))
dr.text((50, 346), '常规组 另加', font=font(36), fill=GREY)
for i, t in enumerate(['足底筋膜松解', '（拇指松解筋膜和姆长屈肌，', '每次 5 分钟）', '', '治疗性超声', '（脉冲 50%、1.5 W/cm²、', '1 MHz、5 分钟）']):
    dr.text((60, 420 + i * 50), t, font=font(30), fill=INK)
dr.rounded_rectangle([710, 330, W - 20, 880], 16, fill=OR)
dr.text((740, 346), '多模式组 另加', font=font(36), fill=RED)
for i, t in enumerate(['低染贴扎', '（刚性贴布托住足弓，保留 24 小时）', '', '短足练习', '（主动抬高内侧纵弓）', '', '单腿提踵', '（脚趾垫毛巾，大负荷渐进）']):
    dr.text((750, 420 + i * 50), t, font=font(30), fill=INK)
save(titled(im, '两组到底差在哪（编者根据原文整理）'), 2)

# ---------- 短足练习 ----------
W, H = 1400, 640; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
steps = [('1', '站立，双脚与肩同宽'), ('2', '主动旋后：第 1 跖骨头往脚跟方向收，抬高足弓；脚趾不要抓地'),
         ('3', '单腿站，膝微屈，保持足弓高度 10 秒'), ('4', '用 5 秒慢慢放下足弓（离心控制）'), ('5', '最多 5 组，一天可做多次'),
         ('↑', '进阶：无支撑单腿站 → 闭眼')]
for i, (a, t) in enumerate(steps):
    y = 30 + i * 98
    dr.ellipse([40, y, 110, y + 70], fill=TEAL if a != '↑' else RED); ctext(dr, 75, y + 12, a, font(38), 'white')
    para(dr, 140, y + 14, t, 32, 1220, INK)
save(titled(im, '短足练习怎么做'), 3)

# ---------- 提踵 ----------
W, H = 1400, 720; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
for i, (wk, s, c) in enumerate([('第 1～2 周', '3 组 × 12 次', LT), ('第 3～4 周', '4 组 × 10 次', GR), ('第 5～8 周', '5 组 × 8 次', OR)]):
    x = 30 + i * 455
    dr.rounded_rectangle([x, 30, x + 430, 230], 16, fill=c)
    ctext(dr, x + 215, 55, wk, font(36), TEAL); ctext(dr, x + 215, 130, s, font(46), RED)
items = ['站在台阶边，脚趾下垫卷起的毛巾，让脚趾充分背伸（启动绞盘机制）', '节奏：向心 3 秒 → 顶端停 2 秒 → 离心 3 秒', '负荷：每组用刚好只能完成规定次数的重量；两周后背包里装书加重',
         '做不了单腿的，先双腿提踵，力量上来再换单腿', '每周 3 次，共 8 周（方案来自 Rathleff 等）']
for i, t in enumerate(items):
    dr.text((50, 270 + i * 82), '· ', font=font(32), fill=INK); para(dr, 80, 270 + i * 82, t, 30, 1280, INK)
save(titled(im, '单腿提踵的大负荷进阶'), 4)

# ---------- 原文图 ----------
save(board([(1, '超声测足底筋膜厚度：俯卧、踝中立、脚趾背伸，在跟骨附着处量，取 3 次平均（本例 4.9 毫米）')], '怎么量筋膜厚度'), 5)
save(board([(2, '距骨后滑：仰卧、小腿用带子托住，一手固定胫腓骨远端，另一手做Ⅰ级向下牵引并向后推距骨'),
            (3, '动态关节松动：患者一脚踩在椅子上，治疗师用带子套住小腿远端，推距骨向后，患者同时向前弓步'),
            (4, '距下关节滑动：侧卧，一手固定距骨、一手握跟骨，A 向外侧滑、B 向内侧滑')], '两组都做的关节松动', maxh=1000), 6)
save(board([(5, '低染贴扎：A 跖骨头处一圈锚定条（不加张力）；B 第一条“U”形条从第 5 跖骨头近端绕过跟骨到第 1 跖骨头，内侧拉紧，使后足内翻、前足内收；C 再贴 3～4 条，每条压前一条一半，最后一条在踝关节远端；D 完成效果'),
            (6, '单腿提踵：A 起始位，站在台阶上，脚趾垫毛巾充分背伸；B 向心上提；C 离心下放')], '多模式组另加的两项', maxh=1000), 7)

# ---------- 流程图 ----------
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
def box(x0, y0, x1, y1, t, fill=LT, fs=28, col=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill, outline=(170, 190, 200), width=2)
    lines = t.split('\n'); hh = len(lines) * (fs + 10)
    for i, l in enumerate(lines): ctext(dr, (x0 + x1) / 2, (y0 + y1) / 2 - hh / 2 + i * (fs + 10), l, font(fs), col)
def down(x, y0, y1):
    dr.line([x, y0, x, y1 - 14], fill=TEAL, width=5); dr.polygon([(x - 12, y1 - 18), (x + 12, y1 - 18), (x, y1)], fill=TEAL)
box(450, 20, 950, 100, '筛查 76 人')
box(980, 20, 1380, 200, '排除 20 人\n不符合纳入标准 10\n拒绝参加 7\n既往足部手术 3', PK, 26)
dr.line([950, 60, 980, 60], fill=TEAL, width=4)
down(700, 100, 180); box(450, 180, 950, 260, '随机分组 56 人')
dr.line([700, 260, 700, 300], fill=TEAL, width=5); dr.line([330, 300, 1070, 300], fill=TEAL, width=5); down(330, 300, 350); down(1070, 300, 350)
box(60, 350, 600, 470, '多模式组 28 人\n全部接受多模式康复', OR); box(800, 350, 1340, 470, '常规组 28 人\n全部接受常规康复', (240, 240, 240))
down(330, 470, 530); down(1070, 470, 530)
box(60, 530, 600, 690, '失访 4 人\n（症状好转后不再来）', (250, 250, 250), 26); box(800, 530, 1340, 690, '失访 4 人\n症状好转后不再来 2\n家庭原因 2', (250, 250, 250), 26)
down(330, 690, 750); down(1070, 690, 750)
box(60, 750, 600, 840, '纳入分析 24 人', GR); box(800, 750, 1340, 840, '纳入分析 24 人', GR)
para(dr, 60, 880, '注：按完成者分析，失访者未纳入统计', 26, 1280, GREY)
save(titled(im, '受试者流程（按原文图 7 重绘）'), 8)

# ---------- 结果图 ----------
fig_, axs = plt.subplots(1, 3, figsize=(13, 4.6), dpi=110)
data = [('晨起第一步疼痛\n（视觉模拟 0～100）', (78.42, 11.62), (79.50, 12.29), '组间 P=0.746'),
        ('足姿指数\n（越高越旋前）', (4.00, 3.71), (4.83, 2.75), '组间 P=0.027'),
        ('后足角（°）', (6.21, 5.22), (6.72, 4.32), '组间 P=0.046')]
for ax, (t, c, e, pv) in zip(axs, data):
    ax.plot([0, 1], c, '-o', color='#888888', lw=3, ms=9, label='常规组')
    ax.plot([0, 1], e, '-o', color='#c0504d', lw=3, ms=9, label='多模式组')
    ax.set_xticks([0, 1]); ax.set_xticklabels(['治疗前', '8 周后'], fontsize=13); ax.set_title(t, fontsize=14)
    ax.text(0.5, 0.92, pv, transform=ax.transAxes, ha='center', fontsize=13, color='#c0504d' if '0.7' not in pv else '#555555')
    ax.set_xlim(-0.3, 1.3)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
axs[0].legend(fontsize=12, frameon=False, loc='center right')
plt.tight_layout(); buf = BytesIO(); fig_.savefig(buf, format='png'); plt.close(fig_)
save(titled(Image.open(buf), '主要结果：疼痛一样降，足姿多模式组更好', 1320), 9)

# 封面
c = fig(5, 900); top = 300; c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
