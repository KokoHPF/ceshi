#!/usr/bin/env python3
"""Shen 等 2026 侧卧位与坐位腰椎旋转手法生物力学比较：首图中文标题卡；原文图 1A 保留、1B 采集软件界面按原图重绘为中文；
图 2、3 鞋子标志已模糊；图 4～8 英文标注就地改为中文；图 9 按原文数据重绘；两种手法要点卡、力量与力矩卡为编者绘制。
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
dr.text((70, 60), '生物力学研究 · 《脊骨与手法治疗》2026', font=font(32), fill=TEAL)
for i, t in enumerate(['腰椎旋转扳法：侧卧位和坐位，', '力往哪儿走？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '测力手套实测手法力 + 有限元模型模拟', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Shen J, Gao X, Zheng H, et al. Chiropr Man Therap 2026;34:56', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1：A 保留，B 重绘
g = raw(48); A = g.crop((0, 0, int(g.width * 0.465), g.height))
A = A.resize((560, round(A.height * 560 / A.width)))
Bw, Bh = 620, A.height; B = Image.new('RGB', (Bw, Bh), (245, 245, 245)); d = ImageDraw.Draw(B)
d.rectangle([0, 0, Bw, 34], fill='white'); d.text((12, 6), '智能测力手套采集软件（示意）', font=font(18), fill=INK)
cols = [('设备设置', ['左手设备 ☑', '右手设备 ☑', '同步器', '连接设备', '启动设备']),
        ('采集控制', ['软件自动采集', '40 毫秒', '同步器', '自动保存 ☑', '开始/结束测试']),
        ('左手数据（牛）', ['食指', '无名指', '拇指', '中指', '手掌', '小指']),
        ('右手数据（牛）', ['拇指', '小指', '中指', '无名指', '食指', '手掌'])]
cw = (Bw - 20) / 4
for k, (t, items) in enumerate(cols):
    x = 10 + k * cw
    d.rectangle([x + 3, 46, x + cw - 3, Bh - 50], outline=(180, 180, 180), fill='white')
    ctext(d, x + cw / 2, 54, t, font(16))
    for i, it in enumerate(items): d.text((x + 12, 92 + i * 36), it, font=font(15), fill=INK)
ctext(d, Bw / 2, Bh - 40, 'B', font(30))
fig1 = Image.new('RGB', (1200, Bh), 'white'); fig1.paste(A, (0, 0)); fig1.paste(B, (580, 0))
t1 = capbox(fig1, '图 1　智能测力手套系统：A 压力传感器、硬件电路模块和无线传输单元（接收器上为“左手/右手接收器”）；B 专用数据采集软件（界面按原图重绘为中文）')

# 图 2、3
f2 = blur(raw(47), [(290, 190, 352, 228), (860, 165, 905, 192), (925, 168, 945, 190)])
f3 = blur(raw(65), [(70, 462, 112, 500), (215, 440, 272, 470), (712, 448, 752, 487), (858, 438, 900, 472), (55, 520, 95, 545)])
t2 = capbox(f2, '图 2　侧卧位腰椎旋转扳法（以右侧为例）：受试者左侧卧，左腿伸直、右腿屈髋屈膝搭在左腿上；左臂屈 90° 抱胸、右臂沿背后伸；操作者站在腹侧，左手按右髋后方、右手按右肩前方，以脊柱为轴旋转，到“弹性固定”后双手同步、短促斜向发力')
t3 = capbox(f3, '图 3　坐位腰椎旋转扳法（以右侧为例）：受试者骑坐方凳，右手放头顶、左手穿过胸前放右腋下；操作者坐在后方，左手拇指抵在 L4 棘突右侧，右臂从受试者右腋下穿过搭在其左肩；腰椎向右旋转，拇指逐渐向左推棘突，有“锁定感”后双手同步短促旋转发力')
save(board([t1], '测力：智能测力手套'), 2)
save(board([t2, t3], '两种扳法怎么做'), 3)

# 图 4
f4 = relabel(raw(90), [((40, 500, 200, 526), '正面观', 20), ((330, 500, 490, 526), '侧面观', 20),
                       ((540, 58, 645, 104), '皮质骨', 16), ((545, 112, 648, 156), '松质骨', 16), ((528, 280, 626, 330), '终板', 16),
                       ((905, 278, 1000, 330), '髓核', 16), ((900, 428, 1000, 482), '纤维环', 16)])
save(board([capbox(f4, '图 4　完整的腰椎（L1～L5）有限元模型：韧带用弹簧单元表示；椎体分皮质骨和松质骨，椎间盘分髓核和纤维环，上下终板各 0.25 毫米（原图“纤维环”拼写有误）')], '有限元模型'), 4)

# 图 5、6
def scat(x, title, ylab, sub, lgx, cols):
    im = raw(x); s = im.width / 1000; d = ImageDraw.Draw(im)
    d.rectangle([int(922 * s), int(318 * s), im.width, int(455 * s)], fill='white')
    for i, c in enumerate(cols):
        y = (372 + i * 30) * s
        d.rectangle([int(935 * s), int(y), int(958 * s), int(y + 22 * s)], fill=c)
        d.text((968 * s, y + 1 * s), str(i + 1), font=font(17 * s), fill='black')
    return relabel(im, [((180, 0, 820, 32), title, 22), ((260, 33, 740, 58), sub, 16), ((300, 727, 700, 752), '标准化肩部力', 17),
                        ((0, 230, 24, 520), '\n'.join(ylab), 15), ((lgx[0], lgx[1], lgx[2], lgx[3]), '聚类', 16)])
f5 = scat(109, '侧卧位扳法的聚类分析', '标准化髋部力', '最优聚类数：2 ｜ 总样本：60', (926, 335, 1000, 362), ('#E69F00', '#56B4E9'))
f6 = scat(118, '坐位扳法的聚类分析', '标准化腰部力', '最优聚类数：3 ｜ 总样本：60', (926, 335, 1000, 362), ('#1B9E77', '#D95F02', '#7570B3'))
save(board([capbox(f5, '图 5　侧卧位扳法力参数的聚类：橙色 = 聚类 1“肩髋协调型”（34 次），蓝色 = 聚类 2“髋主导型”（26 次）；大点为聚类中心（原图标题误写为“俯卧位”）'),
            capbox(f6, '图 6　坐位扳法力参数的聚类：绿色 = 聚类 1“肩腰协调型”（13 次），橙色 = 聚类 2“肩主导型”（33 次），紫色 = 聚类 3“轻柔加载型”（14 次）')], '手法力的聚类'), 5)

# 图 7、8 有限元云图
HDR = [('椎间盘', '等效应力（MPa）'), ('椎间盘', '总变形（mm）'), ('小关节软骨', '等效应力（MPa）'), ('小关节软骨', '总变形（mm）')]
def femap(x, titles, rows_y, vals):
    im = raw(x); s = im.width / 1000; d = ImageDraw.Draw(im)
    a = np.array(im)
    d.rectangle([0, 0, im.width, int(33 * s)], fill='white')
    for k, (h1, h2) in enumerate(HDR):
        cx = (125 + 250 * k) * s
        ctext(d, cx, 1 * s, h1, font(14 * s)); ctext(d, cx, 17 * s, h2, font(12 * s))
    for (y0, y1), t in zip(rows_y, titles):
        d.rectangle([int(250 * s), int(y0 * s), int(750 * s), int(y1 * s)], fill='white')
        ctext(d, 500 * s, (y0 + 1) * s, t, font(15 * s))
    # 色标：找红色块
    red = (a[:, :, 0] > 200) & (a[:, :, 1] < 60) & (a[:, :, 2] < 60)
    blue = (a[:, :, 2] > 180) & (a[:, :, 0] < 60) & (a[:, :, 1] < 90)
    pi = 0
    for (y0, y1) in rows_y:
        for k in range(4):
            xa, xb = int((250 * k + 5) * s), int((250 * k + 32) * s)
            ya, yb = int((y1 + 25) * s), int((y1 + 200) * s)
            r = np.argwhere(red[ya:yb, xa:xb]); bl = np.argwhere(blue[ya:yb, xa:xb])
            if len(r) == 0 or len(bl) == 0: pi += 1; continue
            top = ya + r[:, 0].min(); bot = ya + bl[:, 0].max(); cr = xa + max(r[:, 1].max(), bl[:, 1].max())
            d.rectangle([cr + 2, top - int(22 * s), cr + int(105 * s), bot + int(18 * s)], fill='white')
            y18 = top + 4 * s; y0v = bot + 9 * s
            yv = lambda v: y18 + (18 - min(v, 18)) / 18 * (y0v - y18)
            for v in range(0, 19, 2):
                d.text((cr + 4 * s, yv(v) - 6 * s), str(v), font=font(10 * s), fill=GREY)
            mx, mn = vals[pi]
            for v, lab in [(mx, '最大'), (mn, '最小')]:
                yy = yv(v) - 6 * s
                d.line([cr + 20 * s, yv(v), cr + 27 * s, yv(v)], fill='black', width=max(1, int(s)))
                d.rectangle([cr + 28 * s, yy - 1 * s, cr + 104 * s, yy + 13 * s], fill='white')
                d.text((cr + 30 * s, yy), f'{lab} {v:g}', font=font(10.5 * s), fill='black')
            pi += 1
    return im
V7 = [(7.8686, 0.0123), (7.2165, 0.0002269), (8.8213, 0.24854), (3.5502, 0.0088818),
      (13.4001, 0.0167344), (12.309, 0.0004426), (15.032, 0.15873), (6.0592, 0.0077657)]
V8 = [(7.4277, 0.015698), (14.791, 0.0015723), (8.3299, 0.16972), (9.0523, 0.0099441),
      (8.0874, 0.018875), (16.439, 0.0016005), (9.9368, 0.27238), (9.5503, 0.013628),
      (5.8738, 0.015867), (11.677, 0.0015096), (6.6952, 0.074785), (8.0447, 0.0065953)]
f7 = femap(127, ['聚类 1：肩髋协调型', '聚类 2：髋主导型'], [(37, 60), (309, 332)], V7)
f8 = femap(138, ['聚类 1：肩腰协调型', '聚类 2：肩主导型', '聚类 3：轻柔加载型'], [(37, 60), (311, 334), (587, 610)], V8)
save(board([capbox(f7, '图 7　侧卧位扳法两个聚类的有限元结果：每列从上到下为 L1/2～L4/5；A～D 肩髋协调型，E～H 髋主导型（左侧色标已改为中文，“最大/最小”为该部位的峰值和最小值）')], '侧卧位扳法：应力和变形分布'), 6)
save(board([capbox(f8, '图 8　坐位扳法三个聚类的有限元结果：A～D 肩腰协调型，E～H 肩主导型，I～L 轻柔加载型（左侧色标已改为中文）')], '坐位扳法：应力和变形分布'), 7)

# 图 9 重绘
lab = ['聚类1', '聚类2', '聚类1', '聚类2', '聚类3']
xs = [0, 1, 2.6, 3.6, 4.6]; colr = ['#6f97be'] * 2 + ['#d99a78'] * 3
data = [('椎间盘', '最大等效应力（MPa）', [7.8686, 13.4001, 7.4277, 8.0874, 5.8738]), ('椎间盘', '最大总变形（mm）', [7.2165, 12.309, 14.791, 16.439, 11.677]),
        ('小关节软骨', '最大等效应力（MPa）', [8.8213, 15.032, 8.3299, 9.9368, 6.6952]), ('小关节软骨', '最大总变形（mm）', [3.5502, 6.0592, 9.0523, 9.5503, 8.0447])]
fig, axs = plt.subplots(2, 2, figsize=(12, 9.5), dpi=110)
for ax, (t, yl, v), L in zip(axs.flat, data, 'ABCD'):
    ax.bar(xs, v, 0.75, color=colr, edgecolor='#333333')
    for x_, y_ in zip(xs, v): ax.text(x_, y_ + max(v) * 0.02, f'{y_:.2f}', ha='center', fontsize=11)
    ax.set_xticks(xs); ax.set_xticklabels(lab, fontsize=11); ax.set_title(t, fontsize=14); ax.set_ylabel(yl, fontsize=12)
    ax.text(0.25, -0.15, '侧卧位', transform=ax.transAxes, fontsize=12, ha='center', va='top', color='#3d6b96')
    ax.text(0.72, -0.15, '坐位', transform=ax.transAxes, fontsize=12, ha='center', va='top', color='#a55e3b')
    ax.text(-0.12, 1.05, L, transform=ax.transAxes, fontsize=18, fontweight='bold')
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    ax.set_ylim(0, max(v) * 1.18)
plt.tight_layout(h_pad=3); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf), '五个聚类的峰值对比（按原文图 9 重绘）', 1320), 8)

# 力和力矩卡
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
for k, (t, c, tc, rows, arm) in enumerate([
        ('侧卧位', LT, TEAL, [('肩髋协调型', '56.7%', '肩 64.6 N', '髋 71.4 N', 'L1 12.9 N·m / L5 14.3 N·m'), ('髋主导型', '43.3%', '肩 41.3 N', '髋 121.6 N', 'L1 8.3 N·m / L5 24.3 N·m')], '力臂：肩、髋到脊柱轴各 20 cm'),
        ('坐位', OR, RED, [('肩腰协调型', '21.7%', '肩 70.1 N', '腰 47.4 N', 'L1 14.0 N·m / L4 2.8 N·m'), ('肩主导型', '55.0%', '肩 78.6 N', '腰 26.2 N', 'L1 15.7 N·m / L4 1.6 N·m'), ('轻柔加载型', '23.3%', '肩 50.2 N', '腰 30.9 N', 'L1 10.0 N·m / L4 1.9 N·m')], '力臂：肩 20 cm，拇指到棘突轴 6 cm；另加 400 N 轴向体重')]):
    x = 20 + k * 690
    dr.rounded_rectangle([x, 20, x + 670, 960], 16, fill=c)
    ctext(dr, x + 335, 40, t, font(44), tc)
    for i, (n, pc, a, b_, mo) in enumerate(rows):
        y = 120 + i * 255
        dr.rounded_rectangle([x + 25, y, x + 645, y + 230], 12, fill='white')
        dr.text((x + 45, y + 16), n, font=font(34), fill=tc); dr.text((x + 500, y + 20), pc, font=font(30), fill=GREY)
        dr.text((x + 45, y + 76), a + '　' + b_, font=font(30), fill=INK)
        dr.text((x + 45, y + 130), '输入模型的扭矩：', font=font(24), fill=GREY); dr.text((x + 45, y + 168), mo, font=font(28), fill=RED)
    para(dr, x + 30, 900 - (0 if k else 0), arm, 24, 620, GREY, 6)
save(titled(im, '实测手法力和输入模型的扭矩（根据原文表 3、表 5 和正文整理）'), 9)

c = raw(65).resize((900, round(raw(65).height * 900 / raw(65).width))); blur(c, [(70, 462, 112, 500), (215, 440, 272, 470)]); c.crop((0, 40, 900, 423)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
