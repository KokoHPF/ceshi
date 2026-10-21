#!/usr/bin/env python3
"""Ekstrom 等 2007 JOSPT 9 个康复动作中核心躯干、髋和大腿肌群的肌电分析：首图为原题直译标题卡；
原文图 1～9 直接用原图照片，图注英文译成中文放在每张照片下方（器械品牌 Skier's Edge 保留）；
肌电热图和选动作卡为编者根据原文表 1～4 整理。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
Z = 4
K, G, R = (0, 0, 0), (94, 94, 94), (255, 38, 0)
doc = pymupdf.open(PDF)
PUNC = '，。；、：）”'


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=90)


def titled(im, t, W=1200):
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30 and ch not in PUNC:
            k = len(line)
            while ch.isascii() and ch.isalnum() and k and line[k - 1].isascii() and line[k - 1].isalnum(): k -= 1
            if not k: k = len(line)
            lines.append(line[:k]); line = line[k:] + ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in PUNC: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def phases(title, S, n, fs=24):
    W = 1200; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im); y = 20
    for t, bg, c, items in S:
        h = 66 + sum(para_h(s, fs, 1030 - fs * 1.1, gap=8) + 10 for s in items)
        dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
        yy = y + 62
        for s in items: yy = bullet(dr, 70, yy, s, fs, 1060, gap=8) + 10
        y += h + 16
    save(titled(im.crop((0, 0, W, y)), title), n)


# 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '研究报告 · J Orthop Sports Phys Ther 2007', font=font(32), fill=TEAL)
for i, t in enumerate(['9 个康复训练动作中核心躯干、', '髋部和大腿肌肉的肌电分析']):
    dr.text((70, 130 + i * 72), t, font=font(54), fill=INK)
dr.text((70, 300), 'Electromyographic Analysis of Core Trunk, Hip, and Thigh Muscles', font=font(28), fill=GREY)
dr.text((70, 338), 'During 9 Rehabilitation Exercises', font=font(28), fill=GREY)
dr.line([70, 420, W - 70, 420], fill=(200, 205, 210), width=2)
dr.text((70, 450), 'Ekstrom RA, Donatelli RA, Carp KC. J Orthop Sports Phys Ther.', font=font(30), fill=GREY)
dr.text((70, 494), '2007;37(12):754-762. doi:10.2519/jospt.2007.2471', font=font(30), fill=GREY)
dr.text((70, 550), '美国南达科他大学物理治疗系 · Physiotherapy Associates', font=font(26), fill=GREY)
dr.text((70, 612), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1～9：照片直接取自原文，图注译成中文
FIGS = [(120, '原文图 1　侧卧位、髋中立旋转下的主动髋外展'), (121, '原文图 2　臀桥，抬到脊柱中立位'),
        (117, '原文图 3　单腿臀桥：一侧膝伸直，另一侧伸髋，躯干保持脊柱中立位'),
        (116, '原文图 4　侧桥，躯干保持脊柱中立位'), (119, '原文图 5　俯桥（肘和脚尖支撑），躯干保持脊柱中立位'),
        (118, '原文图 6　四点跪位对侧抬手抬腿，躯干保持脊柱中立位'),
        (114, '原文图 7　侧向上台阶，台阶高 20.32 cm'), (113, '原文图 8　站立弓步'),
        (115, '原文图 9　Dynamic Edge 训练：在阻力下左右滑动，模拟高山滑雪')]
TW = 390
for r in range(3):
    tiles = []
    for xref, t in FIGS[r * 3:r * 3 + 3]:
        ph = Image.open(__import__('io').BytesIO(doc.extract_image(xref)['image'])).convert('RGB')
        ph = ph.crop((0, 0, ph.width, round(ph.width * 250 / 334)))
        ph = ph.resize((TW, round(ph.height * TW / ph.width)), Image.LANCZOS); tiles.append((ph, t))
    ch = max(para_h(t, 24, TW - 20, gap=8) for _, t in tiles)
    im = Image.new('RGB', (1200, tiles[0][0].height + ch + 30), 'white'); dr = ImageDraw.Draw(im)
    for i, (ph, t) in enumerate(tiles):
        x = i * (TW + 15); im.paste(ph, (x, 0))
        dr.rectangle([x, ph.height, x + TW, ph.height + ch + 20], fill=(232, 232, 232))
        para(dr, x + 10, ph.height + 12, t, 24, TW - 20, gap=8)
    save(titled(im, f'原文图 {r * 3 + 1}～{r * 3 + 3}　受试者动作示范（图注译成中文）'), r + 2)

# 编者热图：表 1～4 合并
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
EX = ['主动髋外展', '臀桥', '单腿臀桥', '侧桥', '俯桥', '四点跪对侧抬手抬腿', '侧向上台阶', '弓步', 'Dynamic Edge']
MU = ['臀中肌', '臀大肌', '股内斜肌', '腘绳肌', '胸最长肌', '腰多裂肌', '腹外斜肌', '腹直肌']
V = [[39, 21, 8, 4, 18, 20, 18, 6], [28, 25, 3, 24, 39, 39, 22, 13], [47, 40, 18, 40, 40, 44, 23, 14],
     [74, 21, 19, 12, 40, 42, 69, 34], [27, 9, 23, 4, 6, 5, 47, 43], [42, 56, 16, 39, 36, 46, 30, 8],
     [43, 29, 85, 10, 25, 28, 15, 5], [29, 36, 76, 11, 17, 25, 17, 7], [33, 19, 36, 6, 21, 21, 18, 7]]
fig, ax = plt.subplots(figsize=(12, 8.6), dpi=100)
ax.imshow(V, cmap='YlOrRd', vmin=0, vmax=90, aspect='auto')
for i, row in enumerate(V):
    for j, v in enumerate(row):
        ax.text(j, i, v, ha='center', va='center', fontsize=17, color='white' if v >= 55 else '#222', fontweight='bold' if v > 45 else 'normal')
        if v > 45: ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False, ec='#1f3a93', lw=3))
ax.set_xticks(range(8)); ax.set_xticklabels(MU, fontsize=16); ax.xaxis.tick_top()
ax.set_yticks(range(9)); ax.set_yticklabels(EX, fontsize=16); ax.tick_params(length=0)
ax.set_xlabel('数值为平均 %MVIC（n = 30 名健康人）；蓝框为 > 45% MVIC，作者视为可能达到力量训练刺激', fontsize=14)
fig.tight_layout(); fig.savefig(f'{OUT}/_hm.png'); plt.close(fig)
import os
hm = Image.open(f'{OUT}/_hm.png').convert('RGB'); os.remove(f'{OUT}/_hm.png')
save(titled(hm, '9 个动作 × 8 块肌肉的肌电强度（编者根据原文表 1～4 整理）'), 5)

phases('按训练目的选动作（编者根据原文整理）', [
    ('作者认为可能达到力量刺激的动作', PK, RED, ['股内斜肌：侧向上台阶 85%、弓步 76%（5 秒等长保持在最大屈膝位）',
        '臀中肌：侧桥 74%；腹外斜肌：侧桥 69%', '臀大肌：四点跪对侧抬手抬腿 56%（作者说“可能”）']),
    ('更适合耐力和稳定训练（< 45% MVIC）', LT, TEAL, ['刚过 45% 的单腿臀桥臀中肌 47%、俯桥腹外斜肌 47%、四点跪腰多裂肌 46%，作者仍归为耐力训练', '胸最长肌和腰多裂肌：臀桥、单腿臀桥、侧桥、四点跪抬手抬腿都在 36%～46%，彼此没有显著差异',
        '腘绳肌：单腿臀桥 40%、四点跪抬手抬腿 39% 最高', '腹直肌：俯桥 43%、侧桥 34% 最高，其余动作都 < 15%']),
    ('孤立某块肌肉', GR, (40, 120, 60), ['主动髋外展：臀中肌 39%，核心肌群几乎不参与，适合非负重下单独练臀中肌；想加力量需在腿上加阻力',
        'Dynamic Edge：各肌肉都在 36% 以下，作者建议用于耐力训练']),
    ('别忘了', OR, (180, 90, 20), ['受试者是 30 名健康人，标准差常很大，个体反应差别不小',
        '45% MVIC 的阈值是借用“45%～50% 1RM 能让未训练者增力”推出来的，不是直接验证的结果'])], 6)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), '核心训练 · 表面肌电 · JOSPT', font=font(34), fill=TEAL)
dr.text((50, 128), '9 个康复动作', font=font(56), fill=INK)
dr.text((50, 214), '哪个最练臀、核心和股内斜肌？', font=font(48), fill=INK)
dr.text((50, 318), '侧桥 · 臀桥 · 四点跪 · 上台阶 · 弓步', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
