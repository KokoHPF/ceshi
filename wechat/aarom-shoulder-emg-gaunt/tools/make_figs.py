#!/usr/bin/env python3
"""Gaunt 等 2010《分解式助力肩上举训练的肌电评估》（Sports Health）推文配图。
首图中文标题卡、研究流程卡、原文图 1～4（练习照片，图内只有 A/B 面板字母、没有英文，上下两格改成左右并排后加中文图注）、
按原文表 2～4 重绘的三块肌肉肌电对比图、临床要点卡、封面。原文图 5（电极和电子测角仪位置）与解读关系不大，未采用。
用法：python3 make_figs.py <src 目录> <输出目录> <中文字体>"""
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)


def raw(name):
    return Image.open(f'{SRC}/{name}').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        # 标点不放行首
        # 数字和小数点不拆开
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”' and not (line[-1:] in '0123456789.' and ch in '0123456789.%'):
            dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t


def side_by_side(im):
    """原文上下两格（A 起始、B 结束）之间有一条浅色分隔带：找到它，把两格改成左右并排"""
    g = im.convert('L'); w, h = g.size
    rows = [sum(g.getpixel((x, y)) for x in range(0, w, 4)) for y in range(h)]
    lo, hi = int(h * 0.3), int(h * 0.7)
    y = max(range(lo, hi), key=lambda r: rows[r])
    top, bot = y, y
    while top > 0 and rows[top - 1] > rows[y] * 0.92: top -= 1
    while bot < h - 1 and rows[bot + 1] > rows[y] * 0.92: bot += 1
    a, b = im.crop((0, 0, w, top)), im.crop((0, bot + 1, w, h))
    H = max(a.height, b.height)
    a = a.resize((round(a.width * H / a.height), H)); b = b.resize((round(b.width * H / b.height), H))
    out = Image.new('RGB', (a.width + b.width + 16, H), 'white')
    out.paste(a, (0, 0)); out.paste(b, (a.width + 16, 0)); return out


def card(W, title, blocks):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 6000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 6000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


# 原文表 2～4：均值及 95% 置信区间（% MVIC），按类型排列
GM_C, UA_C, A_C = (90, 150, 200), (220, 130, 40), (190, 40, 50)
EMG = [  # 动作, 类型色, (冈上肌), (冈下肌), (三角肌前束)
    ('侧卧滑板上举', GM_C, (7, 4, 9), (10, 6, 14), (16, 12, 21)),
    ('仰卧弹力带前屈', GM_C, (8, 5, 11), (13, 9, 18), (15, 12, 18)),
    ('擦桌·内侧 45°', GM_C, (12, 8, 15), (7, 4, 10), (16, 12, 20)),
    ('擦桌·正前方', GM_C, (12, 8, 16), (8, 5, 10), (16, 11, 20)),
    ('擦桌·外侧 45°', GM_C, (13, 9, 17), (9, 6, 13), (14, 9, 19)),
    ('墙面滚球', UA_C, (16, 11, 21), (18, 11, 24), (27, 23, 32)),
    ('体棒助力前屈', UA_C, (16, 11, 21), (13, 8, 19), (30, 25, 36)),
    ('滑轮', UA_C, (17, 11, 23), (14, 9, 18), (31, 23, 38)),
    ('手指爬墙', UA_C, (21, 16, 27), (19, 11, 27), (32, 27, 36)),
    ('体棒助力＋主动下放', UA_C, (20, 13, 26), (18, 11, 26), (35, 29, 42)),
    ('站立主动上举', A_C, (29, 22, 37), (21, 12, 30), (45, 40, 50)),
]


def emg_chart():
    W = 1200; im = Image.new('RGB', (W, 1400), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '11 个上举练习的最大肌电（% MVIC）', font=font(36), fill='white')
    x0 = 20
    for c, t in ((GM_C, '减重力'), (UA_C, '直立助力'), (A_C, '直立主动')):
        dr.rectangle([x0, 104, x0 + 26, 130], fill=c); dr.text((x0 + 36, 100), t, font=font(26), fill=INK); x0 += 200
    dr.text((x0 + 20, 102), '横线 = 95% 置信区间', font=font(24), fill=GREY)
    L = 290; PW = 270; GAP = 40; VMAX = 55
    cols = [L + i * (PW + GAP) for i in range(3)]
    top = 200
    for i, name in enumerate(('冈上肌', '冈下肌', '三角肌前束')):
        dr.text((cols[i] + PW // 2, 156), name, font=font(28), fill=INK, anchor='ma')
    RH = 70; bottom = top + RH * len(EMG)
    for cx in cols:
        X = lambda v, cx=cx: cx + PW * v / VMAX
        dr.rectangle([X(20), top - 10, X(40), bottom], fill=(246, 246, 246))  # 20%～40% 中等强度带
        for v in (0, 10, 20, 30, 40, 50):
            if v % 20: continue
            dr.line([X(v), top - 10, X(v), bottom], fill=(225, 225, 225), width=1)
            dr.text((X(v), bottom + 8), str(v), font=font(22), fill=GREY, anchor='ma')
    y = top
    for k, (name, c, *vals) in enumerate(EMG):
        if k in (5, 10):
            dr.line([20, y - 4, W - 20, y - 4], fill=(180, 180, 180), width=2)
        dr.text((L - 16, y + RH // 2 - 4), name, font=font(26), fill=INK, anchor='rm')
        for cx, (m, lo, hi) in zip(cols, vals):
            X = lambda v, cx=cx: cx + PW * v / VMAX
            dr.rectangle([X(0), y + 14, X(m), y + RH - 26], fill=c)
            dr.line([X(lo), y + RH // 2 - 6, X(hi), y + RH // 2 - 6], fill=INK, width=2)
            dr.text((X(hi) + 6, y + RH // 2 - 6), str(m), font=font(22), fill=c, anchor='lm')
        y += RH
    y = bottom + 50
    y = para(dr, 30, y, '数值为原文表 2～4 的均值和 95% 置信区间，编者按练习类型重新排序后重绘。灰色带 = 20%～40% MVIC（原文所用分级里的“中等”强度），左侧为“低”（< 20%）。', 24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 10))


# 1 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '对照实验室研究 · 《Sports Health》2010', font=font(30), fill=TEAL)
dr.text((70, 135), '分解式助力肩上举训练', font=font(56), fill=INK)
dr.text((70, 210), '的肌电评估', font=font(44), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Gaunt BW, McCluskey GM, Uhl TL.', font=font(26), fill=GREY)
dr.text((70, 390), 'Sports Health. 2010;2(5):424-432. doi:10.1177/1941738110366840', font=font(26), fill=GREY)
dr.text((70, 435), '美国佐治亚州圣弗朗西斯康复中心 · 肯塔基大学康复科学系', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, '研究怎么做（编者根据原文整理）', [
    ('谁', '15 名健康年轻人（7 女 8 男），平均 23.9 岁（22～28 岁）；优势侧肩从未受伤、现在不痛、主动活动度正常', LT, TEAL),
    ('测什么', '优势侧 3 块肌肉：冈上肌、冈下肌用针电极（插在肌腹里），三角肌前束用表面电极\n每块肌肉先做 2 次 5 秒最大等长收缩（MVIC），取最高值作为 100%', PK, RED),
    ('做什么', '11 个上举练习，从信封里抽签决定顺序；每个练习先看示范、最多试做 6 次，正式做 5 次\n节拍器控制速度，约每秒 30°；肩胛冈和肱骨上贴电子测角仪，用来切分每一次动作', OR, (200, 120, 0)),
    ('怎么算', '每次动作取肌电最大值，5 次取平均，换算成 % MVIC\n三块肌肉分开做重复测量方差分析，事后两两比较用 Bonferroni 校正（P < 0.00091）', GR, (0, 120, 60)),
]), 2)

save(capbox(side_by_side(raw('fig1.jpg')), '原文图 1  擦桌（正前方）：坐位，桌面与肘同高，手压毛巾向正前方推到肘伸直再收回。左 A 起始，右 B 结束。内侧、外侧版本分别偏 45°'), 3)
save(capbox(side_by_side(raw('fig2.jpg')), '原文图 2  侧卧滑板上举：健侧卧，患侧手放在调好高度的熨衣板上，带着毛巾滑到约 140° 再滑回。左 A 起始，右 B 结束'), 4)
save(capbox(raw('fig3.jpg'), '原文图 3  仰卧弹力带前屈（从 90° 起）：另一只手把红色 Thera-Band 按在腰部，患侧从屈曲 90° 主动举到约 160°，拉长弹力带后慢慢放回。上 A 起始，下 B 结束'), 5)
save(capbox(side_by_side(raw('fig4.jpg')), '原文图 4  站立体棒助力前屈：患侧手握 PVC 棒（拇指朝上），主要靠健侧手推着举到约 160° 再放下。左 A 起始，右 B 结束'), 6)
save(emg_chart(), 7)

save(card(1200, '落到临床（编者整理）', [
    ('最早期：减重力练习', '擦桌、侧卧滑板上举、仰卧弹力带前屈，三块肌肉都在 20% MVIC 以下，冈上肌、冈下肌只有 7%～13%，和文献里的被动活动差不多，可以作为从被动到助力的第一步', LT, TEAL),
    ('冈上肌、冈下肌：分不分阶段差别不大', '减重力和直立助力之间只有少数练习两两有差异、置信区间大量重叠；作者认为保护肩袖不必死守“先躺后站”，进阶看活动度、疼痛和代偿', GR, (0, 120, 60)),
    ('三角肌前束：分阶段有意义', '直立助力（27%～35%）明显高于减重力（14%～16%）；需要保护三角肌时（如切开肩袖修补、三角肌成形）先做减重力练习', OR, (200, 120, 0)),
    ('手指爬墙不算“被动”', '三角肌前束和冈上肌都明显高于所有减重力练习，作者建议放在助力阶段的后期', PK, RED),
    ('别把肌电直接当成负荷', '这是 15 个健康年轻人的数据，动作也很慢；术后患者疼痛、活动受限时肌肉的用法可能不同，肌电也不等于肌腱受到的拉力', PU, (110, 70, 190)),
]), 8)

# 封面：原文图 3 的起始姿势（仰卧弹力带前屈）
c = raw('fig3.jpg'); c = c.crop((0, 0, c.width, round(c.height * 0.69)))
w = c.width; h = round(w * 383 / 900)
if h > c.height: h = c.height; w = round(h * 900 / 383)
x0 = (c.width - w) // 2; y0 = (c.height - h) // 2
c.crop((x0, y0, x0 + w, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
