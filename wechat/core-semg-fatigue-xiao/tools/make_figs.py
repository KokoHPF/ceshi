#!/usr/bin/env python3
"""Xiao 等 2016《经典康复训练中选定肌肉的表面肌电活动》（Rehabil Res Pract）推文配图。
首图中文标题卡、原文图 1～5（照片，只有面板字母，图注译成中文）、原文图 6～11（矢量曲线和柱状图，
已用 tools/fig-translate 原位译成中文，见 src/fig_zh/）、四个动作对比卡、临床要点卡、封面。
用法：python3 make_figs.py <论文.pdf> <中文图目录> <输出目录> <中文字体>"""
import sys

import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, ZH, OUT, F = sys.argv[1:5]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)
doc = pymupdf.open(PDF)
# 原文照片区域（页码从 0 开始，单位 pt）
CLIP = {1: (2, (115, 72, 483, 375)), 2: (2, (85.1, 438.3, 255.4, 566.0)), 3: (2, (343.1, 438.3, 513.4, 566.0)),
        4: (3, (85.1, 73.7, 255.3, 201.5)), 5: (3, (85.1, 242.2, 255.8, 370.8))}


def raw(n):
    pg, r = CLIP[n]
    pix = doc[pg].get_pixmap(dpi=300, clip=pymupdf.Rect(*r))
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def zh(name):
    return Image.open(f'{ZH}/zh_{name}.png').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    t = t.replace('−', '-')  # 文泉驿没有 U+2212 减号
    line = ''
    for ch in t:
        # 标点不放行首
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”': dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200, pad=0):
    iw = W - 2 * pad
    im = im.resize((iw, round(im.height * iw / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12 + pad), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (pad, hh + 8)); return t


def stack(ims, W=1200, gap=16):
    ims = [i.resize((W, round(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    t = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: t.paste(i, (0, y)); y += i.height + gap
    return t


def grid2(ims, W=1200, gap=16):
    """两张一行"""
    cw = (W - gap) // 2; rows = []
    for k in range(0, len(ims), 2):
        pair = [i.resize((cw, round(i.height * cw / i.width)), Image.LANCZOS) for i in ims[k:k + 2]]
        h = max(i.height for i in pair); r = Image.new('RGB', (W, h), 'white')
        for j, i in enumerate(pair): r.paste(i, (j * (cw + gap), 0))
        rows.append(r)
    return stack(rows, W, gap)


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


def heat():
    """表 2 重画：4 个动作 × 7 块肌肉，格子里是出现疲劳的人数（共 30 人），色深 = 人数多"""
    mus = ['竖脊肌\nES', '腹外斜肌\nEO', '腹直肌\nRA', '股直肌\nRF', '股二头肌\nBF', '胫骨前肌\nAT', '腓肠肌\nG']
    rows = [('平板支撑', [16, 24, 27, 19, 19, 17, 20]), ('仰卧臀桥', [16, None, 15, 20, None, None, None]),
            ('单腿臀桥\n（抬右腿）', [20, 21, 22, 18, 23, 17, None]), ('鸟狗式\n（抬左臂右腿）', [16, 23, 20, 16, 20, None, None])]
    W = 1200; L = 230; cw = (W - L - 20) / 7; rh = 120
    im = Image.new('RGB', (W, 120 + 110 + rh * 4 + 120), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '原文表 2：各动作中出现疲劳的人数（共 30 人）', font=font(34), fill='white')
    y0 = 100
    for j, m in enumerate(mus):
        for k, s in enumerate(m.split('\n')):
            x = L + cw * j + cw / 2
            dr.text((x, y0 + 12 + k * 36), s, font=font(26 if k == 0 else 24), fill=INK if k == 0 else GREY, anchor='ma')
    y = y0 + 100
    for name, vals in rows:
        for k, s in enumerate(name.split('\n')):
            dr.text((20, y + (30 if '\n' not in name else 22) + k * 36), s, font=font(28 if k == 0 else 22), fill=INK if k == 0 else GREY)
        for j, v in enumerate(vals):
            x0 = L + cw * j + 4; x1 = L + cw * (j + 1) - 4
            if v is None:
                dr.rounded_rectangle([x0, y + 6, x1, y + rh - 6], 8, fill=(244, 244, 244))
                dr.text(((x0 + x1) / 2, y + rh / 2), '<15', font=font(24), fill=(170, 170, 170), anchor='mm')
            else:
                t = (v - 14) / 14
                c = tuple(int(255 - (255 - e) * t) for e in (0, 110, 130))
                dr.rounded_rectangle([x0, y + 6, x1, y + rh - 6], 8, fill=c)
                dr.text(((x0 + x1) / 2, y + rh / 2), str(v), font=font(34), fill='white' if t > 0.5 else INK, anchor='mm')
        y += rh
    para(dr, 20, y + 18, '原文只列出超过半数（＞15 人）出现疲劳的肌肉；灰格表示不到半数，原文没有给出具体人数。仰卧臀桥的腹直肌只有 15 人，按原文标准其实不该列入。', 24, W - 40, fill=GREY, gap=8)
    return im


# 1 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '研究论文 · 《Rehabilitation Research and Practice》2016', font=font(30), fill=TEAL)
dr.text((70, 135), '经典康复训练中选定肌肉的表面肌电活动', font=font(56), fill=INK)
dr.text((70, 210), '平板支撑、臀桥、单腿桥、鸟狗式的中位频率疲劳分析', font=font(40), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Xiao J, Sun J, Gao J, Wang H, Yang X.', font=font(28), fill=GREY)
dr.text((70, 390), 'Rehabil Res Pract. 2016;2016:4796875. doi:10.1155/2016/4796875', font=font(28), fill=GREY)
dr.text((70, 435), '河北大学电子信息工程学院、河北大学附属医院康复科', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，原文按 CC BY 协议开放获取', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(raw(1), '原文图 1  电极位置（左右两侧都贴）：(a) 腹直肌和腹外斜肌，(b) 竖脊肌，(c) 股直肌，(d) 股二头肌，(e) 胫骨前肌，(f) 腓肠肌'), 2)
save(grid2([capbox(raw(2), '原文图 2  仰卧臀桥'), capbox(raw(3), '原文图 3  单腿臀桥'),
            capbox(raw(4), '原文图 4  平板支撑（肘撑俯卧桥）'), capbox(raw(5), '原文图 5  鸟狗式')]), 3)
save(heat(), 4)
save(stack([capbox(zh('p4_1'), '原文图 6  平板支撑：竖脊肌、腹外斜肌、腹直肌（左侧）的中位频率及线性拟合'),
            capbox(zh('p4_2'), '原文图 7  平板支撑：股直肌、股二头肌、胫骨前肌、腓肠肌（左侧）的中位频率及线性拟合')], gap=30), 5)
save(capbox(zh('p4_3'), '原文图 8  仰卧臀桥：竖脊肌、腹直肌、股直肌（左侧）的中位频率及线性拟合'), 6)
save(capbox(zh('p5_1'), '原文图 9  单腿臀桥（抬右腿）：(a) 竖脊肌和腹外斜肌，(b) 腹直肌和股直肌，(c) 股二头肌和胫骨前肌，左右两侧'), 7)
save(capbox(zh('p6_1'), '原文图 10  鸟狗式（抬左臂右腿）：(a) 两侧竖脊肌、腹外斜肌和左侧腹直肌，(b) 两侧股直肌、股二头肌和右侧腹直肌'), 8)
save(capbox(zh('p6_2'), '原文图 11  各动作中位频率斜率（Hz/s，越负表示下降越快）：(a) 平板支撑，(b) 仰卧臀桥，(c) 单腿臀桥（抬右腿），(d) 鸟狗式（抬左臂右腿）；* 表示两块肌肉之间差异显著。注意 (b)(d) 纵轴只到 −0.2，(a)(c) 到 −0.8 和 −0.7'), 9)

save(card(1200, '四个动作一图看懂（编者根据原文整理）', [
    ('平板支撑：七块肌肉都有半数以上人疲劳', '腹直肌 27 人最多，竖脊肌 16 人最少；斜率最陡的是腓肠肌（−0.71 Hz/s）和股二头肌（−0.48），竖脊肌最平（−0.09）', PK, RED),
    ('仰卧臀桥：最轻松', '只有竖脊肌、腹直肌、股直肌达到半数左右，斜率都在 −0.15 以内，肌肉之间没有显著差异', GR, (0, 120, 60)),
    ('单腿臀桥：比双腿桥累得多', '六块肌肉过半数；胫骨前肌下降最快，抬起侧（右）−0.65 比支撑侧（左）−0.43 更陡；竖脊肌两侧都在 −0.22', OR, (200, 120, 0)),
    ('鸟狗式：中等强度', '五块肌肉过半数，斜率都在 −0.18 以内，肌肉之间、左右之间都没有显著差异，作者认为适合练耐力', LT, TEAL),
    ('先记住一点', '这里的“疲劳”是指中位频率随时间下降，不等于肌肉激活程度高；原文没有测 MVIC 百分比，也没有在动作之间做统计比较', PU, (110, 70, 190)),
]), 10)

save(card(1200, '落到临床（编者整理）', [
    ('四个动作可以排一个大致的进阶', '仰卧臀桥 → 鸟狗式 → 单腿臀桥 / 平板支撑。双腿臀桥最轻松这一点，和以往按 %MVIC 测的结果一致（如 Czaprowski 2014 测腹肌）', GR, (0, 120, 60)),
    ('平板支撑也在练腿', '1 分钟肘撑平板，腓肠肌和股二头肌的疲劳比腹肌还明显；下肢力量差、跟腱或小腿有问题的患者，可能先撑不住的是腿', PK, RED),
    ('单腿桥两侧负荷不对称', '抬起侧的肌肉疲劳更明显，左右都要练；用来做左右对比时，注意结论只来自抬右腿的数据', OR, (200, 120, 0)),
    ('别拿斜率直接当“激活高低”', '中位频率斜率受基线频率影响，不同肌肉、不同动作之间直接比大小容易误判；想知道谁练得多，还是看 %MVIC 研究', PU, (110, 70, 190)),
    ('适用人群有限', '受试者是 30 名无痛的研究生，结果不能直接套到下腰痛患者身上', LT, TEAL),
]), 11)

# 封面：原文图 4（平板支撑）
c = raw(4); w = c.width; h = round(w * 383 / 900)
if h > c.height: h = c.height; w = round(h * 900 / 383)
x0 = (c.width - w) // 2; y0 = (c.height - h) // 2
c.crop((x0, y0, x0 + w, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
