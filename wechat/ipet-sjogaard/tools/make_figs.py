#!/usr/bin/env python3
"""Sjøgaard 2023 IPET（智能体能训练）：原文图 1～5 按原图结构中文重绘；附表 A1 运动目录插图去掉英文文字后，
按身体部位拼图并加中文动作名；首图为原文标题区。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import math
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
from catalog import GROUPS, WARMUP

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); RED = (171, 25, 66); BLUE = (40, 90, 160); GREEN = (70, 140, 60)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK, sp=10):
    for k, l in enumerate(t.split('\n')):
        dr.text((cx - dr.textlength(l, font=f) / 2, y + k * (f.size + sp)), l, font=f, fill=fill)


def arrow(dr, x0, y0, x1, y1, col=GREY, w=6, L=22):
    dr.line([x0, y0, x1, y1], fill=col, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    dr.polygon([(x1, y1), (x1 - L * math.cos(a - .45), y1 - L * math.sin(a - .45)), (x1 - L * math.cos(a + .45), y1 - L * math.sin(a + .45))], fill=col)


# ---------- 图 1：原文标题区 ----------
pix = d[0].get_pixmap(dpi=200, clip=pymupdf.Rect(30, 100, 565, 182))
save(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), 1)

# ---------- 图 2（原文图 1）：一天的身体活动构成 ----------
S = 1300; im = Image.new('RGB', (S, S + 120), 'white'); dr = ImageDraw.Draw(im); C = S / 2
dr.ellipse([60, 60, S - 60, S - 60], fill=(25, 25, 25))
dr.ellipse([200, 200, S - 200, S - 200], fill=(190, 190, 190))
dr.ellipse([370, 370, S - 370, S - 370], fill='white')
for t, ang in [('工作', 180), ('休闲', 0), ('睡眠', 90)]:
    r = (C - 60 + C - 200) / 2; x = C + r * math.cos(math.radians(ang)); y = C + r * math.sin(math.radians(ang))
    ctext(dr, x, y - 36, t, font(64), 'white')
r2 = (C - 200 + C - 370) / 2
for t, ang in [('工作任务', 200), ('体能训练', 235), ('体育运动', 270), ('康复训练', 305), ('交通出行', 340), ('家务活动', 25)]:
    x = C + r2 * math.cos(math.radians(ang)); y = C + r2 * math.sin(math.radians(ang))
    ctext(dr, x, y - 22, t, font(40), INK)
    ax, ay = C + (C - 380) * math.cos(math.radians(ang)), C + (C - 380) * math.sin(math.radians(ang))
    bx, by = C + (C - 470) * math.cos(math.radians(ang)), C + (C - 470) * math.sin(math.radians(ang))
    arrow(dr, ax, ay, bx, by, INK, 5, 18)
arrow(dr, C, C + 280, C, C + 200, INK, 5, 18)
ctext(dr, C, C - 80, '一天累积的\n身体活动与\n静坐总量', font(48), INK, 14)
ctext(dr, C, S + 20, '工作、休闲、睡眠三部分各自对健康和体能有正面或负面影响', font(34), GREY)
save(im, 2)

# ---------- 图 3（原文图 2）：恶性循环与良性循环 ----------
W, H = 1600, 1100; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def oval(cx, cy, rx, ry, t, fs=40, fill=(238, 244, 252)):
    dr.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=(140, 160, 200), width=4)
    lines = t.split('\n'); ctext(dr, cx, cy - len(lines) * (fs + 10) / 2 + 5, t, font(fs))


def person(cx, top, h):
    hr = h * .09; dr.ellipse([cx - hr, top, cx + hr, top + 2 * hr], fill=INK)
    dr.rounded_rectangle([cx - h * .16, top + 2.2 * hr, cx + h * .16, top + h * .55], 10, fill=INK)
    dr.rectangle([cx - h * .12, top + h * .55, cx - h * .02, top + h], fill=INK); dr.rectangle([cx + h * .02, top + h * .55, cx + h * .12, top + h], fill=INK)


oval(W / 2, 110, 260, 85, '工作要求', 50)
oval(W / 2, 400, 270, 110, '完成工作时的\n相对负荷', 44)
arrow(dr, W / 2, 200, W / 2, 285)
person(230, 200, 330); person(1370, 200, 330)
arrow(dr, 420, 250, 525, 360); arrow(dr, 1180, 250, 1075, 360)
dr.text((60, 560), '个人能力 ↓', font=font(46), fill=RED); dr.text((1250, 560), '个人能力 ↑', font=font(46), fill=GREEN)
oval(560, 800, 230, 160, '疲劳\n疼痛\n功能下降', 42, (252, 236, 236))
oval(1040, 800, 230, 160, '功能维持\n或提高', 42, (232, 246, 232))
arrow(dr, 720, 510, 620, 640); arrow(dr, 880, 510, 980, 640)
arrow(dr, 330, 830, 200, 620, RED, 10, 30); arrow(dr, 1270, 830, 1400, 620, GREEN, 10, 30)
dr.text((40, 880), '恶性循环', font=font(52), fill=RED); dr.text((1340, 880), '良性循环', font=font(52), fill=GREEN)
ctext(dr, W / 2, 1010, '同样的工作，能力低的人相对负荷更高，长期可能越来越差；能力够的人则能维持甚至提升', font(32), GREY)
save(im, 3)

# ---------- 图 4（原文图 3）：筛查 → 训练类别 → 体能领域 → 健康获益 ----------
W, H = 1900, 1350; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
for x, t in zip([200, 735, 1195, 1650], ['筛查指标', '训练类别', '体能领域', '健康获益']): ctext(dr, x, 30, t, font(46), BLUE)
cats = ['有氧耐力', '高强度有氧', '爆发力\n（HIIT、发力速率）', '力量\n（分部位）', '功能训练\n（平衡、协调、冲击）']
cy = []
for i, t in enumerate(cats):
    y0 = 140 + i * 230; dr.rounded_rectangle([590, y0, 880, y0 + 170], 18, fill=(240, 240, 240), outline=(90, 90, 90), width=3)
    ctext(dr, 735, y0 + (40 if '\n' in t else 62), t, font(34)); cy.append(y0 + 85)
left = [('健康风险指标', None), ('身体成分\n（BMI、体脂、腰臀比）', (0, 1)), ('血压', (0, 1)), ('血液指标\n（胆固醇、血脂、血糖）', (0, 1)),
        ('肌肉骨骼疼痛', (3,)), ('身体能力', None), ('最大摄氧量', (0, 1, 2)), ('肌力（颈肩、手臂、\n躯干、髋膝）', (2, 3)), ('姿势平衡', (4,))]
y = 120
for t, tg in left:
    if tg is None:
        dr.text((20, y), t, font=font(38), fill=RED); y += 75; continue
    n = t.count('\n') + 1; dr.multiline_text((20, y), t, font=font(30), fill=INK, spacing=6)
    for j in tg: arrow(dr, 450, y + n * 18, 586, cy[j], GREY, 3, 14)
    y += 52 + n * 40
fit = [('代谢体能', 330), ('心肺体能', 660), ('肌肉骨骼体能', 990)]
for t, y0 in fit:
    dr.ellipse([1045, y0 - 90, 1345, y0 + 90], fill='white', outline=(90, 90, 90), width=4); ctext(dr, 1195, y0 - 22, t, font(38))
for i, tg in [(0, [0, 1]), (1, [1, 0]), (2, [1, 2]), (3, [2, 0]), (4, [2])]:
    for j in tg: arrow(dr, 882, cy[i], 1043, fit[j][1], GREY, 4, 16)
for k, (t, j) in enumerate([('糖尿病', 0), ('脑卒中', 1), ('心脏病', 1), ('肌肉骨骼疾病', 2), ('跌倒风险', 2), ('骨质疏松', 2)]):
    y0 = 250 + k * 150; dr.text((1520, y0), t, font=font(40), fill=INK); arrow(dr, 1347, fit[j][1], 1510, y0 + 22, INK, 4, 16)
ctext(dr, W / 2, H - 70, '按原文图 3 结构中文重绘；HIIT：高强度间歇训练', font(30), GREY)
save(im, 4)

# ---------- 图 5（原文图 4）：IPET 每周 1 小时的结构 ----------
W, H = 1700, 1180; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def bx(x0, y0, x1, y1, title, body='', fill='white', tf=36, bf=30):
    dr.rectangle([x0, y0, x1, y1], fill=fill, outline=(120, 120, 120), width=3)
    if body:
        ctext(dr, (x0 + x1) / 2, y0 + 16, title, font(tf)); ctext(dr, (x0 + x1) / 2, y0 + 30 + tf, body, font(bf), GREY)
    else:
        n = title.count('\n') + 1; ctext(dr, (x0 + x1) / 2, (y0 + y1) / 2 - n * (tf + 10) / 2 + 5, title, font(tf))


bx(30, 20, 640, 160, '按工作类型训练\n时长：20 分钟', fill=(225, 225, 225), tf=34)
bx(720, 20, 1670, 160, '按个人情况训练\n时长：30 分钟', fill=(225, 225, 225), tf=34)
for i, (t, b) in enumerate([('久坐工作', '中高强度有氧\n（70%～80% 最大心率）'), ('站立 / 走动工作', '高强度间歇有氧\n（85%～95% 最大心率）\n+ 核心肌群练习'),
                            ('重体力工作', '全身肌耐力训练\n（3 组，60% 1RM）')]):
    y0 = 190 + i * 300; bx(30, y0, 640, y0 + 240, t, b)
rows = [('有氧训练', '中高强度（70%～80% 最大心率）\n分到 10 分钟以上时，其余时间\n可做高强度间歇（85%～95%）'), ('专项力量训练', ''), ('全身力量训练', ''), ('平衡训练', '')]
for i, (t, b) in enumerate(rows):
    y0 = 190 + i * 240; bx(720, y0, 1330, y0 + (200 if b else 110), t, b, tf=34, bf=26)
for i, t in enumerate(['膝 / 踝', '髋', '下背', '肩 / 上背', '颈', '肘 / 手']):
    y0 = 360 + i * 85; bx(1400, y0, 1670, y0 + 65, t, tf=30)
    dr.line([1330, 485, 1400, y0 + 32], fill=GREY, width=3)
dr.line([660, 190, 680, 190, 680, 1060, 660, 1060], fill=GREY, width=4)
for i in range(4): dr.line([680, 625, 718, 190 + i * 240 + 55], fill=GREY, width=3)
ctext(dr, W / 2, 1100, '另加约 10 分钟热身（最大心率 60% 以下，Borg 9～13 分）', font(32), GREY)
save(im, 5)

# ---------- 图 6（原文图 5）：有氧强度与主观疲劳 ----------
fig, ax = plt.subplots(figsize=(11, 6.6), dpi=150)
lv = [('久坐', 0, 20, '#f5e600'), ('很轻', 20, 30, '#f5b400'), ('轻', 30, 40, '#8fd14f'), ('中等', 40, 60, '#1f6fc4'), ('高', 60, 80, '#8b2c4a'), ('剧烈', 80, 90, '#f20000'), ('接近最大', 90, 100, '#c00000')]
for i, (n, a, b, c) in enumerate(lv): ax.bar(i, b - a, bottom=a, width=1, color=c, edgecolor='white')
ax.set_xticks(range(7)); ax.set_xticklabels([v[0] for v in lv], fontsize=12); ax.set_ylim(0, 100); ax.set_ylabel('心率储备（%HRR）', fontsize=12)
ax.set_xlim(-.5, 6.5)
tx = [(95, '18～20', '10', '持续不到 10 分钟'), (85, '16～17', '9～10', '可连续做 30 分钟以内，\n无法连贯说话'), (70, '14～15', '7～8', ''),
      (50, '12～13', '5～6', '能连贯说话，可持续\n30～60 分钟'), (35, '9～11', '2～4', '呼吸没有明显变化，\n可持续 1 小时以上'), (25, '8', '1', ''), (10, '6～7', '0～0.5', '坐或躺，几乎没有额外活动')]
ax2 = ax.twinx(); ax2.set_ylim(0, 100); ax2.set_yticks([])
for y, c, cr, t in tx:
    ax2.text(7.0, y, c, va='center', fontsize=11); ax2.text(7.9, y, cr, va='center', fontsize=11)
    if t: ax2.text(8.9, y - (7 if '\n' in t and y in (85,) else 0), t, va='center', fontsize=10.5)
ax2.text(7.0, 104, 'Borg\n6～20', fontsize=10.5, fontweight='bold', va='bottom'); ax2.text(7.9, 104, 'Borg\n0～10', fontsize=10.5, fontweight='bold', va='bottom')
ax2.text(8.9, 104, '活动描述', fontsize=10.5, fontweight='bold', va='bottom')
for s in ['top', 'right']: ax.spines[s].set_visible(False)
ax2.axis('off')
fig.suptitle('有氧训练强度：心率储备与主观疲劳（RPE）对照', fontsize=15, fontweight='bold', x=.42)
fig.subplots_adjust(left=.07, right=.56, top=.84, bottom=.08)
fig.savefig(f'{OUT}/_f5.png'); plt.close(fig)
save(Image.open(f'{OUT}/_f5.png'), 6)

# ---------- 图 7～16：附表 A1 运动目录插图 ----------
for pg in range(15, 23):
    p = d[pg]
    for w in p.get_text('words'): p.add_redact_annot(pymupdf.Rect(w[:4]))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)


def grab(pg, x0, y0, x1, y1, dpi=220):
    pix = d[pg].get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1)); a = np.array(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))
    nw = a.min(2) < 235
    for y in range(a.shape[0]):
        if nw[y].mean() > .55 and a[y][nw[y]].std() < 40: a[y] = 255
    im = Image.fromarray(a); bb = ImageOps.invert(im.convert('L')).point(lambda v: 255 if v > 20 else 0).getbbox()
    return im.crop(bb) if bb else im


wu = grab(*WARMUP); wu = wu.resize((1500, round(wu.height * 1500 / wu.width)), Image.LANCZOS)
c = Image.new('RGB', (1560, wu.height + 170), 'white'); cd = ImageDraw.Draw(c)
cd.rectangle([0, 0, 1560, 70], fill=BLUE); cd.text((30, 14), '热身（约 10 分钟）', font=font(40), fill='white')
c.paste(wu, (30, 100)); ctext(cd, 780, wu.height + 115, '功率车、椭圆机、划船机或动态拉伸，慢速、微喘即可', font(32), GREY)
save(c, 7)

CW, CH, COLS = 500, 330, 3
for k, (ttl, items) in enumerate(GROUPS):
    n = len(items); rows = math.ceil(n / COLS)
    c = Image.new('RGB', (CW * COLS + 60, 90 + rows * (CH + 70) + 20), 'white'); cd = ImageDraw.Draw(c)
    cd.rectangle([0, 0, c.width, 70], fill=BLUE); cd.text((30, 14), ttl, font=font(40), fill='white')
    for i, (pg, x0, y0, x1, y1, name) in enumerate(items):
        m = grab(pg, x0, y0, x1, y1)
        s = min((CW - 40) / m.width, (CH - 30) / m.height); m = m.resize((round(m.width * s), round(m.height * s)), Image.LANCZOS)
        gx, gy = 30 + (i % COLS) * CW, 100 + (i // COLS) * (CH + 70)
        c.paste(m, (gx + (CW - m.width) // 2, gy + (CH - m.height) // 2))
        ctext(cd, gx + CW / 2, gy + CH + 8, name, font(34))
    save(c, 8 + k)

# ---------- 封面 ----------
cv = Image.new("RGB", (900, 383), "white"); dr = ImageDraw.Draw(cv)
icons = [grab(*GROUPS[2][1][0][:5]), grab(*GROUPS[5][1][3][:5]), grab(*GROUPS[8][1][1][:5])]
x = 560
for m in icons:
    m = m.resize((round(m.width * 250 / m.height), 250), Image.LANCZOS); cv.paste(m, (x, 90)); x += m.width + 10
dr.text((36, 50), '上班族的', font=font(52), fill=INK)
dr.text((36, 125), '运动处方', font=font(84), fill=BLUE)
dr.text((36, 240), '每周 1 小时，按工作类型和', font=font(30), fill=RED)
dr.text((36, 282), '身体情况“对症开练”', font=font(30), fill=RED)
dr.text((36, 335), 'JFMK 2023 · 综述精读', font=font(22), fill=GREY)
cv.save(f'{OUT}/cover.jpg', quality=92)
