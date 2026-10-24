#!/usr/bin/env python3
"""Tsaklis 等 2015 精英女子田径运动员腘绳肌训练的肌肉与强度分类：首图中文标题卡、10 个练习照片（加中文名称和强度标签）
配中文图注、肌电结果图（原文图 11 为矢量图，柱高按 4 倍渲染的页面像素读出后用中文重画）、封面。
用法：python3 make_figs.py <work 目录> <输出目录> <字体>"""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

WORK, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
op = lambda n: Image.open(f'{WORK}/{n}').convert('RGB')
def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t


def card(W, title, blocks):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


FB = ImageFont.truetype(sys.argv[3].replace('Medium', 'Bold'), 30)

NAV = (22, 50, 79)
LOW, MID, HIGH = (24, 128, 128), (200, 120, 0), (210, 60, 45)


def tag(im, items):
    d = ImageDraw.Draw(im)
    for x, y, t, c in items:
        tw = d.textlength(t, font=FB); d.rounded_rectangle([x, y, x + 28 + tw, y + 50], 10, fill=c); d.text((x + 14, y + 6), t, font=FB, fill='white')
    return im


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '原创研究 · 《Open Access Journal of Sports Medicine》2015', font=font(32), fill=TEAL)
dr.text((70, 140), '精英女子田径运动员腘绳肌训练的', font=font(54), fill=INK)
dr.text((70, 215), '肌肉与强度分类：对康复选动作的启示', font=font(54), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Tsaklis P, Malliaropoulos N, Mendiguchia J, Korakakis V, Tsapralis K, Pyne D, Malliaras P.', font=font(24), fill=GREY)
dr.text((70, 405), 'Open Access J Sports Med. 2015;6:209-217. doi:10.2147/OAJSM.S79189', font=font(28), fill=GREY)
dr.text((70, 450), '希腊塞萨洛尼基理工学院、希腊国家田径中心、伦敦玛丽女王大学 等', font=font(26), fill=GREY)
dr.text((70, 540), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

EX = [  # (图, 名称, 强度, 颜色, 图注)
    ('x45', '① 弓步', '低强度', LOW, '原文图 1  弓步：站立快速向前弓步，髋、膝屈到 90°，躯干直立，膝不内扣。闭链、以髋为主'),
    ('x44', '② 单腿罗马尼亚硬拉', '低强度', LOW, '原文图 2  单腿罗马尼亚硬拉（T 字下落）：单腿站、膝微屈，腰椎保持中立，慢慢屈髋到末端，后腿随躯干前倾向后伸。闭链、以髋为主、屈膝很少'),
    ('x59', '③ 壶铃摆动', '低强度', LOW, '原文图 3  壶铃摆动（12 kg）：躯干与地面平行、膝屈约 10°～15°，把壶铃有力地向后摆到两腿之间，再爆发性伸髋把壶铃摆到胸高。闭链、以髋为主'),
    ('x58', '④ 单腿臀桥', '低～中强度', LOW, '原文图 4  单腿臀桥：仰卧屈膝 90°，一腿搭在对侧膝上，慢慢抬起骨盆到膝、髋、肩一条直线。闭链'),
    ('x57', '⑤ 悬吊带屈膝（TRX）', '中强度*', MID, '原文图 5  TRX 屈膝：仰卧，双足套在悬吊带里，抬起骨盆、伸直膝并保持，两腿交替慢速屈膝。原文归为开链、以膝为主（*按原文图 11，股二头肌已超过 80%）'),
    ('x60', '⑥ 足跟搭椅臀桥', '中强度', MID, '原文图 6  足跟搭椅的“腘绳肌臀桥”：仰卧屈膝、足跟放在椅子上，慢慢抬起骨盆到一条直线，保持 5 秒。闭链'),
    ('x75', '⑦ 弹力带站姿屈膝', '中强度', MID, '原文图 7  站姿弹力带屈膝：站立，对抗弹力带（<2 kg）慢速做屈膝伸髋的向心和离心，需要支撑腿髋部稳定和核心控制。开链、以膝为主'),
    ('x74', '⑧ 北欧挺', '中～高强度', MID, '原文图 8  北欧挺：跪在垫上，同伴固定双踝，保持髋中立，身体慢慢前倾到能控制的最低点，再回到起始位。下降幅度越大强度越高'),
    ('x73', '⑨ 瑞士球快速屈膝', '高强度', HIGH, '原文图 9  瑞士球屈膝：俯卧，瑞士球放在臀部位置，左右腿交替尽快屈膝用足跟踢球。开链、以屈膝为主；唯一股二头肌明显高于半腱肌的练习'),
    ('x76', '⑩ 单腿滑行屈伸', '最高强度', HIGH, '原文图 10  单腿滑行：仰卧屈膝，足跟踩在能在地上滑动的小毯上，一侧足跟支撑、抬起骨盆，慢慢把腿伸直再勾回，另一腿离地'),
]
for n, (x, name, lv, c, cap) in enumerate(EX, start=2):
    im = op(f'{x}.jpg'); im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    tag(im, [(16, 16, name, NAV), (16, 76, lv, c)])
    save(capbox(im, cap), n)

# 肌电结果图（据原文图 11 读数，单位按原文图注为 %MVIC）
font_manager.fontManager.addfont(sys.argv[3]); plt.rcParams['font.family'] = font_manager.FontProperties(fname=sys.argv[3]).get_name()
names = ['弓步', '单腿硬拉', '壶铃摆动', '单腿臀桥', 'TRX 屈膝', '搭椅臀桥', '弹力带屈膝', '北欧挺', '瑞士球屈膝', '单腿滑行']
bf = [13.2, 24.8, 27.1, 40.9, 83.6, 63.9, 55.6, 57.1, 111.8, 145.6]
st = [20.6, 29.8, 38.5, 48.8, 74.6, 66.1, 63.0, 64.6, 97.9, 142.1]
fig, ax = plt.subplots(figsize=(12, 7), dpi=100); x = np.arange(10); w = .38
ax.axhspan(0, 50, color='#DEF0EE', zorder=0); ax.axhspan(50, 80, color='#FFF4D2', zorder=0); ax.axhspan(80, 160, color='#FDE8E1', zorder=0)
for y, t in ((46, '低强度 <50%'), (76, '中强度 50%～80%'), (154, '高强度 ≥80%')): ax.text(-0.45, y, t, ha='left', va='center', fontsize=14, color='#555')
ax.bar(x - w / 2, bf, w, color='#D9432F', label='股二头肌（外侧）', zorder=2); ax.bar(x + w / 2, st, w, color='#188080', label='半腱肌（内侧）', zorder=2)
ax.set_xticks(x, names, fontsize=14, rotation=20); ax.set_ylim(0, 160); ax.set_ylabel('肌电（原文图注：%MVIC；纵轴标 μV）', fontsize=14)
ax.legend(frameon=False, fontsize=15, loc='upper center', bbox_to_anchor=(.45, 1.0), ncol=2); ax.tick_params(axis='y', labelsize=14); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{WORK}/emg.png', facecolor='white')
save(capbox(op('emg.png'), '原文图 11 重画：10 个练习中股二头肌和半腱肌的平均肌电。柱高为编者从原图读出的近似值；背景色为原文的强度分级（低 <50%、中 50%～80%、高 ≥80% MVIC）'), 12)

# 封面：北欧挺 + 单腿滑行
a = op('x74.jpg'); a = a.resize((round(a.width * 383 / a.height), 383), Image.LANCZOS)
b = op('x76.jpg'); b = b.resize((900 - a.width, round(b.height * (900 - a.width) / b.width)), Image.LANCZOS); y0 = max(0, (b.height - 383) // 2)
cv = Image.new('RGB', (900, 383), 'white'); cv.paste(a, (0, 0)); cv.paste(b.crop((0, y0, b.width, y0 + 383)), (a.width, 0)); cv.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
