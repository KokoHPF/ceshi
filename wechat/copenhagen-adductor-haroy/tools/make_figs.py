#!/usr/bin/env python3
"""Harøy 等 2019 BJSM 内收肌强化方案预防男子足球运动员腹股沟问题的整群随机对照试验：首图为原题直译标题卡；
原文图 1～3 直接用原图：图 1 照片保留，在 3A～1B 标签下补中文级别和位置；图 2 流程图、图 3 折线图里的英文擦掉后在原位置写中文；
训练方案卡、结果森林图和临床卡为编者根据原文表 1、表 4 和正文整理。
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


def page_img(pno, xref, z=3):
    pg = doc[pno]; r = pg.get_image_rects(xref)[0]
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=r)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def overlay(im, boxes, fs=20):
    """boxes: (x0, y0, x1, y1), 中文（\\n 换行）, 底色, 字色, 对齐 c/r/v（v = 竖排逆时针 90°）"""
    d = ImageDraw.Draw(im)
    for (x0, y0, x1, y1), t, bg, fg, al in boxes:
        d.rectangle([x0, y0, x1, y1], fill=bg); ls = t.split('\n')
        if al == 'v':
            fv = min(fs, x1 - x0); f = font(fv); w = int(d.textlength(t, font=f)) + 4
            tile = Image.new('RGB', (w, fv + 6), bg); ImageDraw.Draw(tile).text((2, 1), t, font=f, fill=fg)
            tile = tile.rotate(90, expand=True); im.paste(tile, (x0 + (x1 - x0 - tile.width) // 2, (y0 + y1 - tile.height) // 2)); continue
        s = fs
        while s > 10 and (max(d.textlength(l, font=font(s)) for l in ls) > x1 - x0 - 4 or len(ls) * s * 1.2 > y1 - y0 + 6): s -= 1
        lh = s * 1.2; top = (y0 + y1) / 2 - lh * len(ls) / 2
        for i, l in enumerate(ls):
            w = d.textlength(l, font=font(s)); x = x1 - w if al == 'r' else (x0 + x1 - w) / 2
            d.text((x, top + i * lh + s * 0.08), l, font=font(s), fill=fg)
    return im


# 首图
W, H = 1400, 700; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '原创论著 · 整群随机对照试验 · Br J Sports Med 2019', font=font(32), fill=TEAL)
for i, t in enumerate(['内收肌强化方案预防男子足球运动员', '腹股沟问题：一项整群随机对照试验']):
    dr.text((70, 130 + i * 72), t, font=font(52), fill=INK)
dr.text((70, 300), 'The Adductor Strengthening Programme prevents groin problems among', font=font(27), fill=GREY)
dr.text((70, 338), 'male football players: a cluster-randomised controlled trial', font=font(27), fill=GREY)
dr.line([70, 420, W - 70, 420], fill=(200, 205, 210), width=2)
dr.text((70, 450), 'Harøy J, Clarsen B, Wiger EG, et al. Br J Sports Med. 2019;53(3):150-157.', font=font(30), fill=GREY)
dr.text((70, 494), 'doi:10.1136/bjsports-2017-098937 · 试验注册 ISRCTN98514933', font=font(30), fill=GREY)
dr.text((70, 550), '挪威体育科学学院奥斯陆运动创伤研究中心 · 哥本哈根大学医院 Amager-Hvidovre · 卡塔尔 Aspetar', font=font(25), fill=GREY)
dr.text((70, 620), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1：照片保留，标签下补中文
f1 = page_img(1, 4)
d1 = ImageDraw.Draw(f1)
for y in (34, 404, 749):
    for x, t in ((67, '起止位'), (719, '中间位')):
        d1.text((x + 60, y + 4), t, font=font(24), fill=TEAL)
save(titled(capbox(f1, '从上到下：第 3 级（最难）标准哥本哈根内收，同伴托踝；第 2 级（中等）短力臂哥本哈根内收，同伴托膝；第 1 级（最易）侧卧位髋内收。A 为起始/结束位，B 为中间位（标签旁中文为编者按原图注补上，原标签 3A～1B 保留）'),
            '原文图 1　内收肌强化方案三个难度级别'), 2)

# 编者卡：训练方案（原文表 1 + 正文）
phases('训练方案怎么做（编者根据原文表 1 和正文整理）', [
    ('一个动作，三个级别', LT, TEAL, ['第 3 级（最难）：标准哥本哈根内收，同伴托住上方腿的踝部', '第 2 级（中等）：同一动作，同伴托住膝部，力臂更短',
        '第 1 级（最易）：侧卧位髋内收', '两侧都练']),
    ('疼痛规则', PK, RED, ['所有人先从第 3 级开始', '练习中腹股沟疼痛 > 3/10 就降到第 2 级；第 2 级仍 > 3/10 就降到第 1 级']),
    ('季前 6～8 周（每次每侧 1 组）', GR, (40, 120, 60), ['第 1 周：每周 2 次，每侧 3～5 次', '第 2 周：每周 3 次，每侧 3～5 次',
        '第 3～4 周：每周 3 次，每侧 7～10 次', '第 5～6 周：每周 3 次，每侧 12～15 次', '第 7～8 周：每周 2 次，每侧 12～15 次']),
    ('比赛季 28 周', PU, (90, 60, 150), ['每周 1 次，每侧 1 组 12～15 次，放在常规热身里，不到 5 分钟'])], 3)

# 原文图 2：流程图英文擦掉写中文
GY, Wt, Bk = (221, 221, 221), (255, 255, 255), (0, 0, 0)
f2 = overlay(page_img(3, 66), [
    ((506, 10, 634, 66), '受邀\n（47 支球队）', Wt, INK, 'c'),
    ((925, 72, 1135, 120), '拒绝参加\n（12 支球队）', GY, INK, 'c'),
    ((458, 142, 682, 200), '随机分组\n(35 支球队；652 名球员)', Wt, INK, 'c'),
    ((925, 196, 1135, 266), '随机分组后退出\n(1 支球队；20 名球员)', GY, INK, 'c'),
    ((297, 272, 520, 328), '干预组\n(18 支球队；339 名球员)', Wt, INK, 'c'),
    ((630, 272, 854, 328), '对照组\n(16 支球队；293 名球员)', Wt, INK, 'c'),
    ((14, 338, 232, 388), '每周报告不足的球员\n（92 人）', (217, 217, 217), INK, 'c'),
    ((925, 338, 1135, 388), '每周报告不足的球员\n（51 人）', GY, INK, 'c'),
    ((494, 366, 648, 408), '意向性分析', Bk, Wt, 'c'),
    ((300, 409, 515, 458), '干预组\n（247 名球员）', Wt, INK, 'c'),
    ((630, 409, 856, 458), '对照组\n（242 名球员）', Wt, INK, 'c'),
    ((14, 472, 232, 524), '依从性低的球员\n（125 人）', (217, 217, 217), INK, 'c'),
    ((494, 498, 648, 540), '符合方案分析', Bk, Wt, 'c'),
    ((300, 541, 515, 592), '干预组\n（122 名球员）', Wt, INK, 'c'),
    ((630, 541, 856, 592), '对照组\n（242 名球员）', Wt, INK, 'c')], fs=21)
save(titled(capbox(f2, '球队和球员在整个干预期间的流向（图中英文由编者译成中文覆盖原文）'), '原文图 2　研究流程图'), 4)

# 原文图 3：坐标轴和标题英文擦掉写中文，补图例
f3 = page_img(4, 73)
ex = []
for dy, ttl, box in ((0, '全部腹股沟问题', (905, 34, 1122, 68)), (599, '严重腹股沟问题', (840, 620, 1146, 654))):
    ex += [(box, ttl, Wt, INK, 'r'), ((0, 196 + dy, 20, 308 + dy), '患病率', Wt, INK, 'v'),
           ((80, 513 + dy, 158, 533 + dy), '基线', Wt, INK, 'c'), ((170, 513 + dy, 270, 533 + dy), '季前期', Wt, INK, 'c'),
           ((480, 543 + dy, 756, 567 + dy), '比赛季第几周', Wt, INK, 'c')]
f3 = overlay(f3, ex, fs=24)
d3 = ImageDraw.Draw(f3)
for i, (fill, t) in enumerate(((None, '干预组'), (INK, '对照组'))):
    x = 905 + i * 120; d3.rectangle([x, 84, x + 14, 98], outline=INK, width=2, fill=fill); d3.text((x + 22, 78), t, font=font(22), fill=INK)
save(titled(capbox(f3, '上图为全部腹股沟问题、下图为严重腹股沟问题的每周患病率（含 95% CI），基线和比赛季 28 周各测 1 次，仅含意向性分析人群；'
                       '灰色区为季前 6～8 周执行方案的时段。空心方块为干预组，实心方块为对照组（图中英文由编者译成中文覆盖，图例为编者按原图注补上）'),
            '原文图 3　比赛季每周腹股沟问题患病率'), 5)

# 编者森林图：原文表 4
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib import font_manager
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
rows = [('全部问题·意向性分析', 0.59, 0.40, 0.86, '13.5% vs 21.3%', 'p = 0.008'), ('全部问题·符合方案', 0.53, 0.36, 0.78, '11.7% vs 21.3%', 'p = 0.001'),
        ('严重问题·意向性分析', 0.82, 0.51, 1.33, '5.7% vs 8.0%', 'p = 0.42'), ('严重问题·符合方案', 0.70, 0.40, 1.23, '4.5% vs 8.0%', 'p = 0.22')]
fig, ax = plt.subplots(figsize=(10.9, 4.9), dpi=110)
for i, (n, o, lo, hi, pv, p) in enumerate(rows):
    y = len(rows) - 1 - i; c = '#BE2832' if hi < 1 else '#888888'
    ax.plot([lo, hi], [y, y], color=c, lw=3); ax.plot(o, y, 's', color=c, ms=13)
    ax.text(1.62, y + 0.14, f'OR {o:.2f}（{lo:.2f}～{hi:.2f}）  {p}', va='center', fontsize=13)
    ax.text(1.62, y - 0.2, f'平均每周患病率 干预组 vs 对照组：{pv}', va='center', fontsize=11, color='#555')
ax.axvline(1, color='#333', lw=1.2, ls='--'); ax.set_xscale('log'); ax.set_xlim(0.27, 1.6)
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xticks([0.3, 0.5, 0.7, 1, 1.5]); ax.set_xticklabels(['0.3', '0.5', '0.7', '1', '1.5'], fontsize=12)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]], fontsize=14); ax.set_ylim(-0.7, len(rows) - 0.4)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.set_xlabel('比值比（OR，对数刻度）', fontsize=12)
fig.text(0.02, 0.02, 'OR < 1 表示干预组更少报告腹股沟问题；红色为 95% CI 不跨 1（有统计学意义），灰色为跨 1', fontsize=12, color='#444')
fig.tight_layout(rect=(0, 0.06, 0.70, 1)); fig.savefig(f'{OUT}/_fp.png'); plt.close(fig)
import os
fp = Image.open(f'{OUT}/_fp.png').convert('RGB'); os.remove(f'{OUT}/_fp.png')
save(titled(fp, '干预效果一览（编者根据原文表 4 整理）'), 6)

phases('落到临床（编者整理）', [
    ('适合谁', LT, TEAL, ['证据来自挪威第二、三级别半职业男子足球（平均 22～24 岁），含基线已有腹股沟症状的球员',
        '女子、青少年和顶级职业球员尚无直接证据；冰球、橄榄球等变向多的项目只能类推']),
    ('怎么执行', GR, (40, 120, 60), ['季前密集期是关键：6～8 周、每周 2～3 次，次数从每侧 3～5 次加到 12～15 次',
        '赛季每周 1 次维持，放进热身，不到 5 分钟', '按疼痛规则选级别，疼痛 > 3/10 就降级，不必停练']),
    ('别说过头', PK, RED, ['减少的是“自报的腹股沟问题”，严重问题只少了 18% 且不显著', '41% 来自比值比，按患病率算约少 37%（13.5% vs 21.3%）',
        '依从性靠球员自报，单个动作不能替代完整的预防计划'])], 7)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), '腹股沟损伤预防 · 整群 RCT · BJSM', font=font(34), fill=TEAL)
dr.text((50, 128), '一个哥本哈根内收动作', font=font(56), fill=INK)
dr.text((50, 214), '腹股沟问题少近四成', font=font(56), fill=INK)
dr.text((50, 318), '35 支球队 · 652 名球员 · 每周不到 5 分钟', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
