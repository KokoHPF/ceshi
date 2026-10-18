#!/usr/bin/env python3
"""Serner 2020 急性内收肌损伤基于标准的康复与重返运动（OJSM 队列研究）：首图中文标题卡；图 1 方案总览、补充材料附录 2
的腹股沟训练与跑动两条进阶线、疼痛控制下最大重复次数示意、T 测试 / 伊利诺伊 / 星形跑示意均中文重绘；附录 2 动作照片
按阶段拼图加中文名；图 2 九个动作原图（仅数字编号）；图 3 流程中文重绘；图 4 按表 3 中位数与四分位距重绘。
用法：python3 make_figs.py <原文 PDF> <附录 2 PDF> <输出目录>"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, AP2, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 13
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
BLUE = (210, 222, 245); DBLUE = (150, 175, 225)
d = pymupdf.open(PDF); a2 = pymupdf.open(AP2)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def bx(dr, x0, y0, x1, y1, lines, fill, fs=28, col=INK, r=12):
    dr.rounded_rectangle([x0, y0, x1, y1], r, fill=fill, outline=(120, 140, 170), width=2)
    yy = (y0 + y1 - len(lines) * (fs + 8)) / 2 + 2
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs), col); yy += fs + 8


def clip(page, rect, dpi=300):
    pix = a2[page - 1].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*rect))
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '前瞻性队列研究 · 《骨科运动医学杂志》（OJSM）2020', font=font(32), fill=TEAL)
for i, t in enumerate(['急性内收肌拉伤：', '按标准康复，多久能回场？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '81 名男性运动员 · 9 个腹股沟动作 · 跑动四阶段 · 1 年再伤率 8%', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Serner A 等，Orthop J Sports Med 2020;8(1):2325967119897247', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1 方案总览 ----------
W, H = 1440, 560; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
bx(dr, 10, 10, 930, 70, ['腹股沟训练'], DBLUE, 30)
for i, t in enumerate(['主动柔韧', '早期抗阻', '负荷进阶', '大负荷/高速']):
    bx(dr, 10 + i * 232, 82, 228 + i * 232, 170, [t], 'white', 28)
bx(dr, 10, 190, 930, 250, ['非腹股沟训练'], DBLUE, 30)
bx(dr, 10, 262, 930, 330, ['个体化进阶'], 'white', 28)
bx(dr, 10, 350, 930, 410, ['跑动与专项功能'], DBLUE, 30)
for i, t in enumerate([['跑动动作'], ['慢跑', '+ 侧滑步'], ['跑动', '+ 变向'], ['冲刺', '+ 变向']]):
    bx(dr, 10 + i * 232, 422, 228 + i * 232, 545, t, 'white', 28)
for x in (240, 472, 704):
    for y in (126, 484):
        dr.polygon([(x - 12, y - 12), (x + 2, y), (x - 12, y + 12)], fill=INK)
bx(dr, 950, 10, 1110, 545, ['临床', '无痛'], 'white', 32)
bx(dr, 1120, 10, 1280, 545, ['受控', '专项', '训练'], DBLUE, 32)
bx(dr, 1290, 10, 1430, 545, ['回归', '全队', '训练'], 'white', 32)
out = Image.new('RGB', (W, H + 90), 'white'); od = ImageDraw.Draw(out)
od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), '原文图 1　基于标准的康复方案总览（三块训练可各自独立进阶）', font=font(38), fill='white')
out.paste(im, (0, 90)); save(out, 2)

# ---------- 附录 2：腹股沟训练四阶段 ----------
W = 1200; im = Image.new('RGB', (W, 2200), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, W, 90], fill=TEAL); dr.text((30, 20), '腹股沟训练进阶（补充材料附录 2）', font=font(44), fill='white')
G = [
    ('1', '主动柔韧', ['动作：4 组 × 20 次', '① 侧向摆腿（外展/内收）', '② 前后摆腿（屈/伸）', '③ 站立画髋圈'],
     ['进阶标准：静息、走路、站立无阻力最大外展发力时', '疼痛 ≤ 2/10']),
    ('2', '早期抗阻', ['动作：2 组 × 20+ 次（疼痛控制最大重复）', '节奏：向心 3 秒 / 离心 3 秒', '继续 ①～③，加：', '④ 弹力带站立内收  ⑤ 弹力带屈髋  ⑥ 弹力带转体'],
     ['进阶标准：无静息痛（允许延迟性酸痛）', '弹力带内收 ≥ 1 组 20 次（疼痛 ≤ 2/10）']),
    ('3', '负荷进阶', ['动作：3 组 × 15+ 次（疼痛控制最大重复）', '节奏：向心 3 秒 / 离心 3 秒', '继续 ①～⑥，加：⑦ 单腿协调（单腿越野滑雪）'],
     ['进阶标准：弹力带内收 ≥ 1 组 15 次（疼痛 ≤ 2/10）', '全范围高速主动动态/弹震式牵伸疼痛 ≤ 2/10']),
    ('4', '大负荷 / 高速', ['动作：3 组 × 15+ 次（疼痛控制最大重复）', '节奏：向心 ≤ 1 秒 / 离心 3 秒', '继续 ①～⑦，加：⑧ 踢球式张力弧  ⑨ 哥本哈根内收'],
     ['临床无痛标准：触诊无痛；外展外侧位最大等长内收无痛；', '最大被动内收肌牵伸无痛；弹力带内收 10RM 无痛；', '哥本哈根内收 10 次无痛；T 测试 100% 无痛']),
]
y = 110
for num, name, ex, cr in G:
    h = 40 + 44 * len(ex) + 36 * len(cr) + 40
    dr.ellipse([20, y + 10, 90, y + 80], fill=TEAL); ctext(dr, 55, y + 22, num, font(40), 'white')
    dr.rounded_rectangle([110, y, W - 20, y + h], 14, fill=(232, 240, 250))
    dr.text((140, y + 14), name, font=font(40), fill=TEAL); yy = y + 70
    for l in ex: dr.text((140, yy), l, font=font(30), fill=INK); yy += 44
    dr.rounded_rectangle([130, yy + 6, W - 40, yy + 16 + 36 * len(cr)], 10, fill=(255, 243, 200))
    for l in cr: dr.text((146, yy + 10), l, font=font(26), fill=RED if num == '4' else INK); yy += 36
    y += h + 24
save(im.crop((0, 0, W, y)), 3)

# ---------- 附录 2：跑动与专项四阶段 ----------
im = Image.new('RGB', (W, 2200), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, W, 90], fill=TEAL); dr.text((30, 20), '跑动与专项功能进阶（补充材料附录 2）', font=font(44), fill='white')
R = [
    ('1', '跑动动作', ['原地小碎步 → 慢跑（5 m 敏捷梯，两脚落在格内）'], ['进阶标准：30% 强度跑动动作无痛']),
    ('2', '慢跑 + 侧滑步', ['直线慢跑，逐步加速加时', '窄距侧滑步，逐步加大步幅和速度', '前后跑；之字形滑步'], ['进阶标准：60% 强度跑 15 分钟无痛；', '60% 强度侧滑步和之字跑无痛']),
    ('3', '跑动 + 变向', ['30 m 直线间歇跑逐步加速', '侧滑步与敏捷梯练习加大步幅和速度', '急加速、急减速；带球/不带球之字滑步与转身'], ['进阶标准：80% 强度 30 m 直线冲刺 10 次无痛；', '80% 强度 T 测试无痛']),
    ('4', '冲刺 + 变向', ['30 m 间歇跑到全速冲刺；侧滑步到最大步幅最大速度', '加减速到全速；之字滑步与转身到全速', '45°、90°、135°、180° 变向/切步'],
     ['临床无痛标准：10 × 30 m 全速冲刺无痛；T 测试 100% 无痛', '受控专项训练标准：伊利诺伊敏捷测试 100% 无痛；', '星形（蜘蛛）测试 100% 无痛（球类带球/不带球各做）；专项动作']),
]
y = 110
for num, name, ex, cr in R:
    h = 40 + 44 * len(ex) + 36 * len(cr) + 40
    dr.ellipse([20, y + 10, 90, y + 80], fill=(181, 83, 44)); ctext(dr, 55, y + 22, num, font(40), 'white')
    dr.rounded_rectangle([110, y, W - 20, y + h], 14, fill=(250, 236, 228))
    dr.text((140, y + 14), name, font=font(40), fill=(181, 83, 44)); yy = y + 70
    for l in ex: dr.text((140, yy), '· ' + l, font=font(30), fill=INK); yy += 44
    dr.rounded_rectangle([130, yy + 6, W - 40, yy + 16 + 36 * len(cr)], 10, fill=(255, 243, 200))
    for l in cr: dr.text((146, yy + 10), l, font=font(26), fill=INK); yy += 36
    y += h + 24
save(im.crop((0, 0, W, y)), 4)

# ---------- 疼痛控制最大重复次数 ----------
W, H = 1200, 360; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '“疼痛控制下最大重复次数”怎么调负荷', font=font(40), fill='white')
cols = [(120, 190, 120), (150, 205, 120), (250, 210, 90), (245, 160, 80), (235, 120, 80), (220, 80, 70)] + [(200, 60, 60)] * 5
for i in range(11):
    x0 = 60 + i * 98; dr.rectangle([x0, 150, x0 + 90, 220], fill=cols[i]); ctext(dr, x0 + 45, 162, str(i), font(40), 'white')
ctext(dr, 60 + 98 - 4, 240, '≤ 1：加负荷', font(30), (40, 120, 40))
dr.rounded_rectangle([60 + 2 * 98 - 8, 140, 60 + 2 * 98 + 98, 230], 10, outline=RED, width=6)
ctext(dr, 60 + 2 * 98 + 45, 240, '2：就是它', font(30), RED)
ctext(dr, 60 + 6 * 98 + 45, 240, '≥ 3：减负荷', font(30), (180, 70, 50))
ctext(dr, W / 2, 100, '数字疼痛评分（0～10）：每组做到力竭，过程中疼痛保持在 2/10', font(28), GREY)
ctext(dr, W / 2, 300, '每组都做到“再也做不动”，但疼痛不超过 2 分', font(30), INK)
save(im, 5)

# ---------- 原文图 2：九个动作 ----------
p = d[3]; info = [x for x in p.get_image_info(xrefs=True) if x['bbox'][3] - x['bbox'][1] > 300][0]
ph = Image.open(BytesIO(d.extract_image(info['xref'])['image'])).convert('RGB')
w = 1000; ph = ph.resize((w, round(ph.height * w / ph.width)), Image.LANCZOS)
out = Image.new('RGB', (w, ph.height + 90), 'white'); od = ImageDraw.Draw(out)
od.rectangle([0, 0, w, 76], fill=TEAL); od.text((24, 16), '原文图 2　方案中的 9 个腹股沟动作', font=font(40), fill='white')
out.paste(ph, (0, 90)); save(out, 6)

# ---------- 附录 2 动作照片：三块拼图 ----------
def board(title, rows):
    rh = 420; gap = 14; W = 1300
    out = Image.new('RGB', (W, 90 + len(rows) * (rh + 70)), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), title, font=font(40), fill='white')
    y = 90
    for name, cells in rows:
        od.text((24, y + 6), name, font=font(34), fill=TEAL); y += 56
        ims = [clip(pg, r).resize((round(clip(pg, r).width * rh / clip(pg, r).height), rh), Image.LANCZOS) for pg, r, _ in cells]
        tw = sum(i.width for i in ims) + gap * (len(ims) - 1); s = min(1, (W - 40) / tw)
        ims = [i.resize((int(i.width * s), int(i.height * s))) for i in ims]
        x = (W - (sum(i.width for i in ims) + gap * (len(ims) - 1))) // 2
        for im_, (_, _, t) in zip(ims, cells):
            out.paste(im_, (x, y))
            if t:
                f = font(30); tw_ = od.textlength(t, font=f)
                od.rounded_rectangle([x + 8, y + im_.height - 52, x + tw_ + 32, y + im_.height - 8], 8, fill='white')
                od.text((x + 20, y + im_.height - 48), t, font=f, fill=INK)
            x += im_.width + gap
        y += ims[0].height + 14
    return out.crop((0, 0, W, y))


save(board('第 1 阶段：主动柔韧', [
    ('① 前后摆腿（屈/伸）', [(8, (74, 198, 161, 303), '后摆'), (8, (168, 199, 255, 304), '前摆')]),
    ('② 侧向摆腿（外展/内收）', [(9, (85, 209, 180, 322), '外展'), (9, (183, 209, 269, 322), '内收')]),
    ('③ 站立画髋圈', [(10, (39, 182, 102, 283), ''), (10, (107, 181, 172, 283), ''), (10, (176, 182, 239, 283), ''), (10, (243, 183, 308, 284), '')]),
]), 7)
save(board('第 2 阶段：早期抗阻（弹力带）', [
    ('④ 站立内收', [(12, (46, 253, 165, 361), '起始'), (12, (170, 253, 283, 361), '结束')]),
    ('⑤ 屈髋', [(14, (59, 262, 167, 363), '起始'), (14, (175, 262, 283, 363), '结束')]),
    ('⑥ 转体', [(15, (62, 287, 153, 387), '起始'), (15, (163, 287, 256, 387), '结束')]),
]), 8)
save(board('第 3～4 阶段：协调、高速与大负荷', [
    ('⑦ 单腿协调（单腿越野滑雪）', [(17, (48, 218, 132, 316), ''), (17, (134, 218, 214, 315), ''), (17, (217, 217, 296, 315), '')]),
    ('⑧ 踢球式张力弧', [(16, (76, 263, 157, 368), '起始'), (16, (166, 263, 246, 367), '踢出')]),
    ('⑨ 哥本哈根内收', [(18, (50, 266, 163, 367), '起始'), (18, (172, 266, 290, 367), '结束')]),
]), 9)

# ---------- 三个测试示意 ----------
fig, axs = plt.subplots(1, 3, figsize=(13, 5.2), dpi=150)
ax = axs[0]
for x, y in [(0, 0), (0, 10), (-5, 10), (5, 10)]: ax.plot(x, y, '^', ms=14, color='#e07b39')
for (x0, y0, x1, y1), c in [((0, 0.6, 0, 9.4), '#1f5f8b'), ((-0.3, 10.3, -4.6, 10.3), '#b5532c'), ((-4.6, 9.7, 4.6, 9.7), '#b5532c'),
                            ((4.6, 10.6, 0.4, 10.6), '#b5532c'), ((0.4, 9.4, 0.4, 0.6), '#555')]:
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=14, color=c, lw=2))
ax.text(1, 5, '10 m 向前跑', fontsize=11); ax.text(0.9, 2, '倒退跑回', fontsize=11, color='#555'); ax.text(-5, 11.5, '侧滑步 5 m + 5 m，手触锥', fontsize=11, color='#b5532c')
ax.text(-1.5, -1.6, '起点/终点', fontsize=11); ax.set_title('T 测试', fontsize=14)
ax = axs[1]
for x, y in [(0, 0), (0, 10), (5, 0), (5, 10), (2.5, 1.7), (2.5, 4), (2.5, 6.3), (2.5, 8.6)]: ax.plot(x, y, '^', ms=12, color='#e07b39')
path = [(0, 0), (0, 10), (2.5, 9.5), (2.0, 7.5), (3.0, 5.1), (2.0, 2.9), (3.0, 1.0), (2.0, 2.9), (3.0, 5.1), (2.0, 7.5), (2.5, 9.5), (5, 10), (5, 0)]
ax.plot(*zip(*path), '-', color='#1f5f8b', lw=2)
ax.text(-0.8, -1.4, '起点', fontsize=11); ax.text(4.4, -1.4, '终点', fontsize=11); ax.text(5.4, 5, '10 m', fontsize=11)
ax.text(-1.8, 5, '5 m 宽', fontsize=11, rotation=90); ax.set_title('伊利诺伊敏捷测试', fontsize=14)
ax = axs[2]
import math
ax.plot(0, 0, 'o', ms=14, color='#1f5f8b'); ax.plot(0, -10, '^', ms=12, color='#e07b39')
ax.add_patch(FancyArrowPatch((0, -9.4), (0, -0.6), arrowstyle='-|>', mutation_scale=14, color='#555', lw=2)); ax.text(0.5, -6, '10 m', fontsize=11)
for ang in [45, 90, 135, 180]:
    for s in (1, -1):
        t = math.radians(90 - s * ang); x, y = 6 * math.cos(t), 6 * math.sin(t)
        if ang == 180 and s == -1: continue
        ax.plot(x, y, '^', ms=12, color='#e07b39')
        ax.add_patch(FancyArrowPatch((0, 0), (x * .9, y * .9), arrowstyle='-|>', mutation_scale=12, color='#b5532c', lw=1.6))
        ax.text(x * 1.25, y * 1.18, f'{ang}°', fontsize=10, ha='center')
ax.set_title('星形（蜘蛛）变向测试', fontsize=14); ax.text(-3.5, -12.5, '中心切步加速，跑回起点再做下一个方向', fontsize=10)
for a in axs:
    a.set_aspect('equal'); a.axis('off')
axs[0].set_xlim(-7, 7); axs[0].set_ylim(-2.5, 12.5); axs[1].set_xlim(-2.5, 7); axs[1].set_ylim(-2.5, 11.5); axs[2].set_xlim(-8.5, 8.5); axs[2].set_ylim(-13.5, 8.5)
fig.suptitle('三个“100% 强度无痛”测试示意（编者根据附录 2 重绘）', fontsize=15)
fig.tight_layout(); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 10)

# ---------- 图 3 流程 ----------
W, H = 1300, 1400; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def ar(x, a, b, c=(120, 170, 200)):
    dr.line([x, a, x, b], fill=c, width=6); dr.polygon([(x, b + 6), (x - 13, b - 12), (x + 13, b - 12)], fill=c)


def hl(y, a, b, c=(120, 170, 200)):
    dr.line([a, y, b, y], fill=c, width=6); dr.polygon([(b + 6, y), (b - 12, y - 13), (b - 12, y + 13)], fill=c)


bx(dr, 330, 20, 730, 90, ['急性腹股沟痛运动员 150 人'], (225, 232, 245), 25)
ar(530, 90, 150); hl(120, 530, 770)
bx(dr, 780, 50, 1290, 210, ['排除 41 人：拒绝参加 39 人', '（愿在俱乐部康复 32、个人原因 7）', '起病史不一致 2 人'], (245, 230, 230), 24)
bx(dr, 330, 155, 730, 225, ['纳入急性腹股沟痛 109 人'], (225, 232, 245), 25)
ar(530, 225, 285); hl(255, 530, 770)
bx(dr, 780, 225, 1290, 345, ['排除：疼痛不累及内收肌 28 人', '（屈髋肌 23、腹肌 4、髋关节 1）'], (245, 230, 230), 24)
bx(dr, 330, 290, 730, 360, ['急性内收肌损伤 81 人（100%）'], (200, 230, 210), 25)
ar(530, 360, 480); hl(420, 530, 770)
bx(dr, 780, 365, 1290, 640, ['中途停止康复 20 人：', '疼着回俱乐部 11；度假 1；', '回国继续治疗 2；工作/学业 2；', '合同到期 1；腹股沟手术 2；', '耻骨联合注射 1'], (245, 230, 230), 24)
bx(dr, 330, 485, 730, 555, ['达到临床无痛 61 人（75%）'], (200, 230, 210), 25)
ar(530, 555, 700); hl(625, 530, 770)
bx(dr, 780, 655, 1290, 735, ['未做完受控专项训练就回俱乐部 11 人'], (245, 230, 230), 24)
bx(dr, 330, 705, 730, 775, ['完成受控专项训练 50 人（62%）'], (200, 230, 210), 25)
ar(530, 775, 1170)
bx(dr, 20, 830, 640, 1110, ['回归全队训练的组成：', '完成受控专项训练 50；', '临床无痛但未完成专项训练 11；', '康复中疼着回俱乐部 11；', '度假后、本国治疗后、工作后回归各 1'], (240, 240, 240), 24)
bx(dr, 680, 880, 1290, 1060, ['失访 6 人：联系不上 3；', '合同到期、停止康复且当季', '未回俱乐部 3'], (245, 230, 230), 24)
bx(dr, 330, 1175, 730, 1245, ['回归全队训练 75 人（93%）'], (200, 230, 210), 25)
ctext(dr, 650, 1290, '百分比以 81 名急性内收肌损伤运动员为分母', font(24), GREY)
save(im.crop((0, 0, W, 1330)), 11)

# ---------- 图 4：按表 3 重绘 ----------
M = ['临床无痛', '完成受控专项训练', '回归全队训练']
T3 = {'0 级': [(13, 11, 14), (16, 15, 17), (17, 13, 18)], '1 级': [(13, 11, 17), (17, 16, 21), (21, 16, 26)],
      '2 级': [(17, 11, 24), (25, 15, 30), (21, 14, 28)], '3 级': [(55, 31, 75), (68, 51, 84), (78, 68, 98)]}
fig, axs = plt.subplots(1, 3, figsize=(13, 4.8), dpi=150, sharey=True)
cols = ['#9bbbd4', '#5d8fb8', '#1f5f8b', '#b5532c']
for ax, k in zip(axs, range(3)):
    for i, (g, v) in enumerate(T3.items()):
        med, lo, hi = v[k]
        ax.plot([lo, hi], [i, i], color=cols[i], lw=6, solid_capstyle='round'); ax.plot(med, i, 'o', color='black', ms=9)
        ax.text(hi + 3, i, f'{med} 天', va='center', fontsize=12)
    ax.set_yticks(range(4)); ax.set_yticklabels(['磁共振 ' + g for g in T3]); ax.invert_yaxis()
    ax.set_title(M[k], fontsize=14); ax.set_xlim(0, 125); ax.set_xlabel('受伤后天数')
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
fig.suptitle('三个重返运动节点所需天数（黑点＝中位数，色条＝四分位距；按原文表 3 重绘）', fontsize=14)
fig.tight_layout(); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 12)
import os; os.remove(f'{OUT}/_p.png')

# ---------- 封面 900×383 ----------
c = clip(18, (172, 266, 290, 367), 300); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = max(0, (c.height - 383) // 2); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
