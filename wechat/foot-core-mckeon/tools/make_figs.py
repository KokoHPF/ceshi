#!/usr/bin/env python3
"""McKeon 等 2015 足核心系统：首图中文标题卡；原文图 1 按原意重绘为中文，图 2～5、7 英文标注改为中文，图 6 加中文图例；
短足训练进阶卡与足内在肌测试卡为编者根据原文整理。
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
plt.rcParams['axes.unicode_minus'] = False
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


def card(W, title, blocks, bg=(246, 248, 250)):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


up = lambda im, w=1000: im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '综述 · 《英国运动医学杂志》2015', font=font(32), fill=TEAL)
dr.text((70, 130), '足核心系统：', font=font(56), fill=INK)
dr.text((70, 215), '理解足内在肌功能的新范式', font=font(56), fill=INK)
dr.line([70, 340, W - 70, 340], fill=(200, 205, 210), width=2)
dr.text((70, 375), 'McKeon PO, Hertel J, Bramble D, Davis I. Br J Sports Med 2015;49:290', font=font(28), fill=GREY)
dr.text((70, 430), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1：按原意重绘
W, H = 1200, 700; im = Image.new('RGBA', (W, H), 'white'); dr = ImageDraw.Draw(im)
PU, RD, BL = (112, 48, 160), (150, 40, 40), (70, 120, 190)
def box(x0, y0, x1, y1, c, t, lines):
    dr.rectangle([x0, y0, x1, y1], fill=c)
    ctext(dr, (x0 + x1) / 2, y0 + 14, t, font(36), 'white')
    for i, l in enumerate(lines): ctext(dr, (x0 + x1) / 2, y0 + 66 + 38 * i, l, font(26), 'white')
box(320, 10, 880, 190, PU, '神经子系统', ['肌肉肌腱感受器（局部和整体）', '韧带感受器（包括足底筋膜）', '足底皮肤感受器'])
box(10, 470, 520, 690, RD, '被动子系统', ['足弓骨骼（足“半穹顶”）', '足底筋膜', '韧带'])
box(680, 470, 1190, 690, BL, '主动子系统', ['足内在肌（局部稳定肌）', '足外在肌（整体运动肌）'])
ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
for (cx, cy), c in (((600, 255), PU), ((545, 340), RD), ((655, 340), BL)):
    od.ellipse([cx - 82, cy - 82, cx + 82, cy + 82], fill=c + (110,))
im = Image.alpha_composite(im, ov); dr = ImageDraw.Draw(im)
dr.ellipse([575, 288, 625, 338], outline=(240, 170, 0), width=4)
ctext(dr, 600, 205, '神经', font(28)); ctext(dr, 520, 345, '被动', font(28)); ctext(dr, 680, 345, '主动', font(28))
ctext(dr, 600, 425, '足核心系统', font(40), (230, 160, 0))
def arrow(p, q):
    import math
    dr.line([p, q], fill='black', width=16)
    for a, b in ((p, q), (q, p)):
        ang = math.atan2(b[1] - a[1], b[0] - a[0]); L = 38
        pts = [b, (b[0] - L * math.cos(ang - .5), b[1] - L * math.sin(ang - .5)), (b[0] - L * math.cos(ang + .5), b[1] - L * math.sin(ang + .5))]
        dr.polygon(pts, fill='black')
arrow((290, 450), (430, 215)); arrow((910, 450), (770, 215)); arrow((545, 580), (655, 580))
save(capbox(im.convert('RGB'), '原文图 1：足核心系统。神经、主动、被动三个子系统相互作用，提供稳定性和灵活性，以应对足部不断变化的需求（编者按原图重绘为中文）'), 2)

# 原文图 2
f = relabel(up(raw(45)), [((540, 196, 660, 234), '外侧观', 30), ((555, 556, 785, 604), '内侧观', 30), ((88, 646, 232, 690), '上面观', 30)])
save(capbox(f, '原文图 2：麦肯齐提出的功能性“半穹顶”。穹顶的中心被认为是距骨顶'), 3)

# 原文图 3
f = relabel(up(raw(59)), [((0, 280, 110, 405), '足底\n筋膜', 30), ((645, 460, 822, 492), '足底筋膜', 28), ((938, 150, 1000, 350), '跟\n腱', 32)])
save(capbox(f, '原文图 3：A 足底筋膜的走向；B 跟腱与足底筋膜在解剖和生物力学上的联系，两者在跟骨周围有筋膜相连'), 4)

# 原文图 4
f = relabel(up(raw(60)), [((553, 458, 892, 537), '跖骨深横韧带', 34), ((536, 653, 882, 735), '跖骨深横韧带', 34),
                          ((530, 878, 818, 998), '', 10), ((742, 803, 1000, 920), '足底楔舟\n韧带', 32),
                          ((530, 930, 742, 995), '足底骰舟\n韧带', 32), ((0, 960, 208, 1037), '足底长韧带', 34),
                          ((12, 1093, 222, 1167), '足底短韧带', 34), ((538, 1120, 702, 1197), '弹簧韧带', 34)])
save(capbox(f, '原文图 4：为足纵弓和横弓提供被动稳定的主要足底韧带'), 5)

# 原文图 5
f = relabel(up(raw(65)), [((362, 391, 525, 445), '拇长屈肌', 32), ((368, 501, 522, 552), '腓骨长肌', 32),
                          ((358, 638, 538, 692), '趾长屈肌', 32), ((568, 606, 692, 660), '胫骨后肌', 30),
                          ((583, 688, 717, 742), '腓骨长肌\n（切断）', 24), ((540, 803, 702, 887), '趾长屈肌\n（切断）', 26)])
save(capbox(f, '原文图 5：足外在肌肌腱在足底的止点。A 趾长屈肌、拇长屈肌纵向走行，支撑纵向稳定；腓骨长肌斜行经过中足，支撑横弓。'
               'B 去掉 A 中的肌腱后可见胫骨后肌：止点广泛分布于跗骨和跖骨，同时支撑纵弓和横弓'), 6)

# 原文图 6 + 中文图例
f = up(raw(66), 1200); leg = Image.new('RGB', (1200, 330), 'white'); dr = ImageDraw.Draw(leg)
L = [('第 1 层', '① 拇展肌　② 趾短屈肌　③ 小趾展肌'), ('第 2 层', '④ 足底方肌（止于趾长屈肌腱）　⑤ 蚓状肌（起于趾长屈肌腱）'),
     ('第 3 层', '⑥ 小趾短屈肌　⑦ 拇收肌斜头（a）和横头（b）　⑧ 拇短屈肌'), ('第 4 层', '⑨ 骨间足底肌'),
     ('足背', '⑩ 骨间背侧肌　⑪ 趾短伸肌')]
dr.rounded_rectangle([0, 0, 1200, 320], 10, fill=LT)
for i, (a, b_) in enumerate(L):
    dr.text((24, 18 + 60 * i), a, font=font(30), fill=TEAL); dr.text((170, 18 + 60 * i), b_, font=font(30), fill=INK)
out = Image.new('RGB', (1200, f.height + 340), 'white'); out.paste(f, (0, 0)); out.paste(leg, (0, f.height + 10))
save(capbox(out, '原文图 6：足底四层内在肌及足背内在肌（从左到右为第 1～4 层，下方为足背；图例编号对应原文）'), 7)

# 原文图 7
skin = up(raw(117)).getpixel((700, 258))
f = relabel(up(raw(117)), [((195, 0, 445, 34), '放松状态的足核心', 30), ((695, 0, 985, 34), '收缩状态的足核心', 30),
                           ((688, 365, 922, 393), '缩短后的足穹顶长度', 22), ((185, 398, 395, 423), '静息足穹顶长度', 22),
                           ((700, 398, 915, 423), '静息足穹顶长度', 22)])
f = relabel(f, [((720, 243, 922, 273), '短足动作', 28)], bg=skin)
save(capbox(f, '原文图 7：短足动作。左为放松时的足长（实线）；右为收缩时，足被“往里收”（箭头），足长缩短（虚线）'), 8)

# 编者卡：测试与训练进阶
blocks = [('足内在肌测试（评估）', '① 把患者的脚摆在距下关节中立位，跟骨和所有跖骨头着地。\n② 让患者把脚趾完全伸直抬起，再放回地面。\n'
           '③ 单腿站立，保持这个足姿 30 秒。\n④ 治疗师观察：舟骨高度有没有明显下降，足外在肌有没有过度用力。', LT, TEAL),
          ('短足训练：先控制，后能力', '要领：距下关节中立位，跟骨和跖骨头着地，脚趾既不屈也不伸；用足底内在肌把第 1 跖趾关节往跟骨方向拉，足弓抬起、足“变短”，脚趾不能卷曲。\n'
           '类比：就像腰椎核心训练里的腹部收缩（肚脐往里收），只动局部稳定肌，不让整体运动肌代偿。', OR, (200, 110, 30)),
          ('进阶顺序', '坐位 → 双腿站立 → 单腿站立 → 功能活动（深蹲、单腿跳）', GR, (40, 130, 60)),
          ('其他训练手段', '赤脚或极简鞋走路、跑步：增加足底感觉输入，有研究显示足长缩短、足部肌肉横截面积增大。\n足底感觉减退者（如糖尿病周围神经病变）不宜赤脚活动。', PK, RED)]
save(card(1200, '足核心的评估与训练（编者根据原文整理）', blocks), 9)

c = up(raw(66), 900); c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
