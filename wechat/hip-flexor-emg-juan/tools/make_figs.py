#!/usr/bin/env python3
"""Juan 2024 屈髋肌（髂腰肌）肌电综述：图 1 + 附图 A1/A2 检索截图改为正文中文表格；
图 2 PRISMA、表 3 偏倚风险、图 3～9 柱状图按原文附录 E 数据中文重绘；附表 A3 动作照片按训练阶段拼图并加中文标注。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); RED = (171, 25, 66); TEAL = (20, 120, 110)
GREEN, PURPLE, BROWN = '#4f7f3a', '#7b4fa0', '#8c1a1a'
d = pymupdf.open(PDF)


def page(pg, dpi=200):
    pix = d[pg].get_pixmap(dpi=dpi)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


# ---------- 图 1：原文标题区 ----------
pix = d[0].get_pixmap(dpi=200, clip=pymupdf.Rect(30, 100, 560, 184))
save(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), 1)

# ---------- 图 2：PRISMA 流程 ----------
W, H = 1400, 1300
im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def box(x0, y0, x1, y1, lines, fill='white', fs=34):
    dr.rounded_rectangle([x0, y0, x1, y1], 14, fill=fill, outline=(60, 60, 60), width=3)
    f = font(fs); th = len(lines) * (fs + 12) - 12; y = (y0 + y1 - th) / 2
    for l in lines:
        dr.text(((x0 + x1 - dr.textlength(l, font=f)) / 2, y), l, font=f, fill=INK); y += fs + 12


def arrow(x0, y0, x1, y1):
    dr.line([x0, y0, x1, y1], fill=(60, 60, 60), width=4)
    if x0 == x1: dr.polygon([(x1, y1), (x1 - 12, y1 - 20), (x1 + 12, y1 - 20)], fill=(60, 60, 60))
    else: dr.polygon([(x1, y1), (x1 - 20, y1 - 12), (x1 - 20, y1 + 12)], fill=(60, 60, 60))


for y0, y1, t in [(40, 360, '识\n别'), (400, 1000, '筛\n选'), (1040, 1250, '纳\n入')]:
    dr.rounded_rectangle([30, y0, 110, y1], 12, fill=(30, 50, 100))
    f = font(40); ls = t.split('\n'); yy = (y0 + y1 - len(ls) * 52) / 2
    for l in ls: dr.text((50, yy), l, font=f, fill='white'); yy += 52
box(160, 60, 700, 190, ['数据库检索记录', '1883 篇'], (214, 228, 243))
box(820, 60, 1360, 190, ['其他来源', '0 篇'], (214, 228, 243))
box(820, 250, 1360, 360, ['剔除重复', '324 篇'], (235, 235, 235))
dr.line([430, 190, 430, 305], fill=(60, 60, 60), width=4); arrow(430, 305, 818, 305)
dr.line([1090, 190, 1090, 225], fill=(60, 60, 60), width=4); dr.line([430, 225, 1090, 225], fill=(60, 60, 60), width=4)
arrow(430, 305, 430, 418)
box(160, 420, 700, 540, ['题目、摘要筛选', '1559 篇'])
arrow(700, 480, 818, 480); box(820, 420, 1360, 540, ['排除', '1422 篇'], (235, 235, 235))
arrow(430, 540, 430, 618)
box(160, 620, 700, 740, ['获取全文', '137 篇'])
arrow(700, 680, 818, 680); box(820, 620, 1360, 740, ['未获取', '0 篇'], (235, 235, 235))
arrow(430, 740, 430, 818)
box(160, 820, 700, 940, ['全文评估', '137 篇'])
arrow(700, 880, 818, 880); box(820, 820, 1360, 940, ['排除', '128 篇'], (235, 235, 235))
arrow(430, 940, 430, 1078)
box(160, 1080, 700, 1200, ['最终纳入', '9 篇'], (190, 235, 180))
save(im, 2)

# ---------- 图 3：偏倚风险（表 3） ----------
STUD = ['Andersson\n1997', 'Andersson\n1995', 'Hu\n2011', 'Jiroumaru\n2014', 'Kim\n2016', 'Okubo\n2021', 'Philippon\n2011', 'Sugajima\n1996', 'Yamane\n2019']
pg9 = page(8, 110)
xs = [175 + 80 * i for i in range(9)]; ys = [382 + 22.4 * k for k in range(27)]
M = np.array([[1 if np.array(pg9.getpixel((int(x), int(y))))[1] > 120 else 0 for x in xs] for y in ys])
tot = M.sum(0)
ITEM = ['研究目的描述清楚', '结局指标描述清楚', '受试者特征描述清楚', '干预描述清楚', '混杂因素分布描述', '主要结果描述清楚',
        '报告随机变异', '报告不良事件', '描述失访', '报告确切 P 值', '受邀者有代表性', '参与者有代表性', '场所设施有代表性',
        '对受试者设盲', '对评估者设盲', '事后分析有说明', '随访时长调整', '统计方法恰当', '依从性可靠', '结局测量准确',
        '各组来源相同', '各组招募时间相同', '随机分组', '分配隐藏', '混杂因素调整', '考虑失访', '样本量计算']
fig, ax = plt.subplots(figsize=(10, 13.5), dpi=150)
ax.imshow(M, cmap=matplotlib.colors.ListedColormap(['#e05050', '#3aa35a']), aspect='auto')
ax.set_xticks(range(9)); ax.set_xticklabels(STUD, fontsize=10.5)
ax.xaxis.tick_top()
ax.set_yticks(range(27)); ax.set_yticklabels([f'{i + 1}. {t}' for i, t in enumerate(ITEM)], fontsize=11)
ax.set_xticks(np.arange(-.5, 9), minor=True); ax.set_yticks(np.arange(-.5, 27), minor=True)
ax.grid(which='minor', color='white', lw=1.5); ax.tick_params(which='both', length=0)
for i, t in enumerate(tot):
    ax.text(i, 27.2, str(t), ha='center', va='top', fontsize=13, fontweight='bold')
ax.text(-0.6, 27.2, '总分', ha='right', va='top', fontsize=13, fontweight='bold')
ax.set_ylim(28.3, -0.5)
fig.suptitle('偏倚风险评估（改良 Downs & Black 量表）', fontsize=17, fontweight='bold', y=.985)
fig.text(.5, .012, '绿色＝满足（1 分）；红色＝不满足或无法判断（0 分）。13～14 分为“差”，15 分为“一般”', ha='center', fontsize=11, color='#555')
fig.tight_layout(rect=(0, .025, 1, .965)); fig.savefig(f'{OUT}/_rob.png'); plt.close(fig)
save(Image.open(f'{OUT}/_rob.png'), 3)

# ---------- 图 4～10：柱状图（原文附录 E 表 A6～A12） ----------
F3 = [('双腿抬腿', 86), ('屈膝、双脚固定的屈髋起身', 80), ('单腿抬腿', 68), ('直腿抬高等长 60° + 外旋 20° + 外展 30°', 65.2),
      ('伸膝、双脚固定的屈髋起身', 60), ('直腿抬高等长 60° + 外展 30°', 59), ('直腿抬高等长 45° + 外展 30°', 48.9),
      ('直腿抬高等长 60° + 外旋 20°', 47.6), ('直腿抬高等长 45° + 外旋 20° + 外展 30°', 46.7), ('直腿抬高等长 60°', 44.1),
      ('直腿抬高等长 45° + 外旋 20°', 41.2), ('直腿抬高等长 45°', 40.6), ('直腿抬高等长 30°', 38.4),
      ('直腿抬高等长 30° + 外旋 20° + 外展 30°', 36.7), ('直腿抬高等长 30° + 外旋 20°', 35), ('直腿抬高等长 30° + 外展 30°', 32.5),
      ('屈膝、双脚不固定的不完全起身', 29), ('屈膝卷腹', 16.5)]
F4 = [('直腿抬高等长 60° + 外旋 20° + 外展 30°', 67.1), ('直腿抬高等长 60°', 60.8), ('直腿抬高等长 60° + 外旋 20°', 60.8),
      ('直腿抬高等长 60° + 外展 30°', 54.3), ('直腿抬高等长 45° + 外旋 20° + 外展 30°', 50.3), ('直腿抬高等长 45°', 48.8),
      ('直腿抬高等长 45° + 外展 30°', 45.6), ('直腿抬高等长 30° + 外旋 20°', 44.5), ('直腿抬高等长 30° + 外旋 20° + 外展 30°', 41.1),
      ('直腿抬高等长 45° + 外旋 20°', 37.7), ('直腿抬高等长 30° + 外展 30°', 35.9), ('直腿抬高顶端保持', 35),
      ('直腿抬高等长 30°', 34), ('直腿抬高 向心后段', 30), ('直腿抬高 向心中段', 15), ('直腿抬高 离心中段', 15),
      ('直腿抬高 向心早段', 10), ('直腿抬高 离心后段', 10)]
F5 = [('离心放腿', 23.6), ('直腿抬高', 17.6), ('离心仰卧起坐', 15.8), ('仰卧起坐', 13.2)]
F6 = [('单腿站立，同侧屈髋 90°', 99), ('单腿站立，同侧屈髋 60°', 75), ('仰卧同侧腿静态抬至 60°', 59), ('同侧最大直腿外展', 56),
      ('单腿站立，同侧屈髋屈膝 90°', 55), ('仰卧双腿静态抬至 60°', 55), ('同侧负重主动直腿抬高', 50), ('单腿站立，同侧屈髋 30°', 43),
      ('伸膝、双脚固定，躯干静态保持 60°', 42), ('同侧主动直腿抬高', 40), ('对侧最大伸髋', 26), ('坐位腰椎过度前凸', 22),
      ('对侧伸髋 30°', 16), ('对侧最大直腿外展', 16), ('静态向对侧侧屈', 16), ('抗重力静态向同侧侧屈', 16), ('挺直腰背坐', 4),
      ('单腿站立，对侧屈髋 30°', 1), ('对侧主动直腿抬高', 0), ('对侧负重主动直腿抬高', 0), ('站立', 0), ('站立，躯干前屈 30°', 0),
      ('单腿站立，同侧屈髋 0°', 0), ('单腿站立，对侧屈髋 0°', 0), ('单腿站立，对侧屈髋 60°', 0), ('单腿站立，对侧屈髋 90°', 0),
      ('单腿站立，对侧屈髋屈膝 90°', 0), ('同侧伸髋 30°', 0), ('同侧最大伸髋', 0), ('静态向同侧侧屈', 0)]
F7 = [('单腿站立，同侧屈髋 90°', 85), ('仰卧双腿静态抬至 60°', 59), ('仰卧同侧腿静态抬至 60°', 58), ('抗重力静态向同侧侧屈', 54),
      ('单腿站立，同侧屈髋 60°', 52), ('伸膝、双脚固定，躯干静态保持 60°', 52), ('同侧最大直腿外展', 36), ('单腿站立，同侧屈髋屈膝 90°', 34),
      ('单腿站立，同侧屈髋 30°', 21), ('坐位腰椎过度前凸', 17), ('静态向对侧侧屈', 16), ('对侧负重主动直腿抬高', 10),
      ('同侧负重主动直腿抬高', 10), ('挺直腰背坐', 9), ('对侧主动直腿抬高', 6), ('同侧主动直腿抬高', 6), ('对侧伸髋 30°', 4),
      ('对侧最大伸髋', 4), ('对侧最大直腿外展', 4), ('单腿站立，对侧屈髋 90°', 3), ('同侧最大伸髋', 2), ('单腿站立，对侧屈髋 30°', 1),
      ('单腿站立，对侧屈髋 60°', 1), ('站立', 0), ('站立，躯干前屈 30°', 0), ('单腿站立，同侧屈髋 0°', 0), ('单腿站立，对侧屈髋 0°', 0),
      ('单腿站立，对侧屈髋屈膝 90°', 0), ('同侧伸髋 30°', 0), ('静态向同侧侧屈', 0)]
F8 = [('60% 最大收缩屈髋（水中）', 514), ('40% 最大收缩屈髋（水中）', 334), ('60% 最大收缩屈髋（陆上）', 252), ('40% 最大收缩屈髋（陆上）', 215),
      ('20% 最大收缩屈髋（水中）', 209), ('20% 最大收缩屈髋（陆上）', 185), ('仰卧屈髋 向心', 17.5), ('侧卧髋外展 + 外旋 向心', 16),
      ('仰卧屈髋 离心', 14.6), ('传统蚌式开合 向心', 11.9), ('侧卧髋外展 + 外旋 离心', 11.1), ('传统蚌式开合 离心', 8),
      ('侧卧靠墙髋外展 向心', 7.8), ('中立位蚌式 向心', 7.8), ('侧卧靠墙髋外展 离心', 6.3), ('中立位蚌式 离心', 4.8),
      ('抗阻伸髋 向心', 4.4), ('抗阻屈膝 向心', 4.1), ('抗阻伸髋 离心', 3.9), ('抗阻伸膝 向心', 3.8), ('抗阻屈膝 离心', 3.7),
      ('侧卧髋外展 向心', 3.6), ('凳上髋旋转 离心', 3.5), ('抗阻伸膝 向心*', 3.5), ('凳上髋旋转 向心', 3.4), ('侧卧髋外展 离心', 3.3),
      ('双腿臀桥 向心', 3), ('双腿臀桥 离心', 2.7), ('单腿臀桥 向心', 2.5), ('俯卧夹脚跟 向心', 2.3), ('单腿臀桥 离心', 2.1)]
F9 = [('屈髋 30° 等长', 1.1), ('屈髋 60° 等长', 1.05), ('屈髋 0° 等长', 1), ('伸髋 10° 等长', .9)]


def bars(data, title, xlabel, n, color=GREEN, hl=(), hl2=(), note=None, w=10, fmt='{:g}'):
    names = [a for a, _ in data]; vals = [b for _, b in data]
    h = max(3.6, .42 * len(data) + 1.6)
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    cols = [PURPLE if i in hl else ('#c07a2a' if i in hl2 else color) for i in range(len(data))]
    y = np.arange(len(data))
    ax.barh(y, vals, color=cols, height=.68)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=12); ax.invert_yaxis()
    mx = max(vals)
    for i, v in enumerate(vals):
        ax.text(v + mx * .01, i, fmt.format(v), va='center', fontsize=11)
    ax.set_xlim(0, mx * 1.12); ax.set_xlabel(xlabel, fontsize=12)
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    ax.grid(axis='x', color='#ddd', lw=.8); ax.set_axisbelow(True)
    ax.set_title(title, fontsize=16, fontweight='bold', loc='left', pad=12)
    if note: fig.text(.01, .005, note, fontsize=10.5, color='#555', ha='left', va='bottom', wrap=True)
    fig.tight_layout(rect=(0, .035 if note else 0, 1, 1))
    fig.savefig(f'{OUT}/_b{n}.png'); plt.close(fig)
    save(Image.open(f'{OUT}/_b{n}.png'), n)


bars(F3, '原文图 3　髂肌平均激活（%MVIC，针电极）', '%MVIC', 4)
bars(F4, '原文图 4　腰大肌平均激活（%MVIC，针电极）', '%MVIC', 5, hl=(1, 11),
     note='紫色：同一个动作（直腿抬高约 60° 处等长保持）在两项研究中测得 60.8% 和 35%，差距很大')
bars(F5, '原文图 5　髂腰肌平均激活（%MVIC，表面电极）', '%MVIC', 6, color=BROWN, w=9)
bars(F6, '原文图 6　髂肌平均肌电振幅（µV，针电极）', '振幅（µV）', 7, note='同侧／对侧：相对于测量电极所在的一侧')
bars(F7, '原文图 7　腰大肌平均肌电振幅（µV，针电极）', '振幅（µV）', 8, note='同侧／对侧：相对于测量电极所在的一侧')
bars(F8, '原文图 8　髂腰肌平均肌电振幅（µV，针电极）', '振幅（µV）', 9, hl2=tuple(range(6)),
     note='橙色为 Sugajima 1996 水浸实验，其余为 Philippon 2011，两者测量方法不同，数值不宜直接比较。*原文此项重复标为“向心”')
bars(F9, '原文图 9　不同屈髋角度下髂腰肌均方根值（表面电极）', '均方根值', 10, color=BROWN, w=9, fmt='{:.2f}')

# ---------- 图 11～18：附表 A3 动作照片，按训练阶段拼图 ----------
ROWS = [(22, [(718, 360, 215, 270), (1203, 357, 215, 270)]), (22, [(719, 672, 214, 269), (1205, 663, 213, 287)]),
        (22, [(666, 986, 318, 227), (1146, 989, 329, 220)]), (22, [(633, 1252, 390, 214), (1113, 1248, 397, 215)]),
        (22, [(724, 1507, 203, 331), (1214, 1504, 193, 337)]), (23, [(722, 359, 209, 329), (1205, 359, 209, 328)]),
        (23, [(745, 725, 163, 270), (1223, 721, 175, 276)]), (23, [(744, 1034, 163, 270), (1220, 1038, 182, 263)]),
        (23, [(744, 1341, 163, 270), (1216, 1350, 189, 252)]), (23, [(670, 1651, 312, 218), (1179, 1647, 262, 221)]),
        (23, [(670, 1907, 312, 218), (1169, 1910, 280, 215)]), (24, [(670, 362, 313, 217), (1164, 364, 293, 213)]),
        (24, [(663, 615, 325, 221), (1147, 618, 325, 220)]), (24, [(656, 875, 339, 237), (1150, 874, 317, 232)]),
        (24, [(656, 1146, 340, 236), (1151, 1151, 321, 232)]), (24, [(639, 1423, 370, 235), (1146, 1428, 328, 227)]),
        (24, [(637, 1714, 379, 219), (1146, 1708, 326, 232)]), (25, [(632, 364, 392, 268), (1102, 367, 414, 264)]),
        (25, [(644, 684, 366, 289), (1124, 691, 370, 278)]), (25, [(631, 1023, 392, 307), (1105, 1029, 438, 297)]),
        (25, [(623, 1377, 400, 270), (1102, 1376, 414, 270)]), (25, [(622, 1703, 407, 243), (1134, 1696, 349, 244)])]
NAME = ['挺直腰背坐', '坐位腰椎过度前凸', '侧卧蚌式开合', '侧卧髋外展', '坐位抗重力躯干侧屈',
        'A. 坐位屈髋 90° 等长', 'B. 站立同侧屈髋 30° 等长', 'A. 站立同侧屈髋 60° 等长', 'B. 站立同侧屈髋 90° 等长',
        'A. 仰卧直腿屈髋 60° 等长', 'B. 仰卧直腿屈髋 30° 等长', 'C. 仰卧直腿屈髋 0° 等长',
        'A. 仰卧屈髋（屈膝）', 'B. 主动直腿抬高', 'C. 负重主动直腿抬高',
        'A. 屈膝卷腹', 'B. 伸膝、双脚固定的屈髋起身', 'C. 屈膝、双脚固定的屈髋起身',
        'A. 离心放腿', 'B. 负重离心放腿', 'C. 双腿抬腿', 'D. 负重双腿抬腿']
PHASE = [('第 1 阶段　低水平激活', [0, 1]), ('第 2 阶段　作为稳定肌间接激活', [2, 3, 4]), ('第 3 阶段　直接激活（等长）', [5, 6]),
         ('第 3+ 阶段　单腿支撑下等长', [7, 8]), ('第 4 阶段　长力臂等长（力量期开始）', [9, 10, 11]),
         ('第 5 阶段　过渡到动态训练', [12, 13, 14]), ('第 6 阶段　躯干在下肢上运动', [15, 16, 17]),
         ('第 7 阶段　离心与双侧（最高强度）', [18, 19, 20, 21])]
P = {pg: page(pg) for pg in (22, 23, 24, 25)}
W, RH, GAP = 1200, 330, 16
for k, (ttl, idx) in enumerate(PHASE):
    blocks = []
    for i in idx:
        pg, bs = ROWS[i]
        ims = [P[pg].crop((x, y, x + w, y + h)) for x, y, w, h in bs]
        ims = [m.resize((round(m.width * RH / m.height), RH), Image.LANCZOS) for m in ims]
        tw = ims[0].width + ims[1].width + GAP
        if tw > W:
            s = W / tw; ims = [m.resize((round(m.width * s), round(RH * s)), Image.LANCZOS) for m in ims]; tw = W
        rh = ims[0].height
        b = Image.new('RGB', (W, rh + 64), 'white'); bd = ImageDraw.Draw(b)
        bd.text((0, 6), NAME[i], font=font(36), fill=INK)
        x = (W - tw) // 2
        for j, m in enumerate(ims):
            b.paste(m, (x, 58)); bd.rounded_rectangle([x + 8, 66, x + 100, 108], 8, fill=(0, 0, 0, 160))
            bd.text((x + 18, 70), ['起始', '结束'][j], font=font(28), fill='white'); x += m.width + GAP
        blocks.append(b)
    Ht = 90 + sum(b.height + 30 for b in blocks)
    c = Image.new('RGB', (W + 60, Ht), 'white'); cd = ImageDraw.Draw(c)
    cd.rectangle([0, 0, W + 60, 70], fill=TEAL); cd.text((30, 14), ttl, font=font(40), fill='white')
    y = 90
    for b in blocks: c.paste(b, (30, y)); y += b.height + 30
    save(c, 11 + k)

# ---------- 封面 ----------
cv = Image.new('RGB', (900, 383), (234, 245, 243)); dr = ImageDraw.Draw(cv)
ph = P[25].crop((1102, 1376, 1516, 1646)); ph = ph.resize((round(ph.width * 383 / ph.height), 383), Image.LANCZOS)
ph = ph.crop(((ph.width - 420) // 2, 0, (ph.width - 420) // 2 + 420, 383))
cv.paste(ph, (480, 0))
dr.text((30, 40), '髂腰肌', font=font(76), fill=INK)
dr.text((30, 140), '怎么练才练得到？', font=font(44), fill=RED)
dr.text((30, 220), '9 项肌电研究 + 7 级进阶', font=font(30), fill=TEAL)
dr.text((30, 300), '临床医学杂志 2024 · 系统综述', font=font(24), fill=(110, 110, 110))
cv.save(f'{OUT}/cover.jpg', quality=92)
