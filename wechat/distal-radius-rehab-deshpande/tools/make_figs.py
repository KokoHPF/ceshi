#!/usr/bin/env python3
"""Deshpande 等 2026《提高桡骨远端骨折康复的功能结局》（JOCR）推文配图。
首图中文标题卡、原文图 1～10（都是照片，图内没有英文，只把图注译成中文）、三条路线时间轴对比卡、临床要点卡、封面。
用法：python3 make_figs.py <论文.pdf> <输出目录> <中文字体>"""
import sys

import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)
doc = pymupdf.open(PDF)
# 原文照片在 PDF 里是带灰框的合成图，按照片区域（pt，已向内收 1pt 去掉边框）裁出来
CLIP = {1: (1, (53, 53, 293, 312)), 2: (1, (262, 527, 563, 697)), 3: (2, (53, 50, 366, 220)),
        4: (2, (263, 523, 562, 700)), 5: (3, (54, 54, 561, 204)), 6: (3, (326, 426, 558, 696)),
        7: (4, (57, 54, 557, 245)), 8: (4, (317, 534, 563, 705)), 9: (5, (53, 51, 373, 251)),
        10: (5, (305, 516, 563, 698))}


def raw(n):
    pg, r = CLIP[n]
    pix = doc[pg].get_pixmap(dpi=300, clip=pymupdf.Rect(*r))
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        # 标点不放行首
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”': dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t



def stack(ims, W=1200, gap=16):
    ims = [i.resize((W, round(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    t = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: t.paste(i, (0, y)); y += i.height + gap
    return t


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


def timeline():
    """三条路线 × 时间轴：固定、负重、腕关节活动从什么时候开始"""
    W = 1200; L = 230; R = W - 30; wk = 14  # 横轴 0～14 周
    X = lambda w: L + (R - L) * w / wk
    im = Image.new('RGB', (W, 1010), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '三条路线时间轴（编者根据原文整理）', font=font(36), fill='white')
    for w in (0, 2, 4, 8, 12):
        dr.line([X(w), 110, X(w), 900], fill=(215, 215, 215), width=2)
        dr.text((X(w) - 10, 905), f'{w}', font=font(26), fill=GREY)
    dr.text((R - 40, 940), '周', font=font(26), fill=GREY)
    rows = [
        ('保守治疗', [
            ('长臂石膏', 0, 4, (200, 200, 200)), ('夹板（练时摘）', 4, 8, (225, 225, 225)),
        ], [('2 周 腕被动活动', 2), ('5 周 助力/主动', 4.3), ('8 周末 轻抗阻', 8)]),
        ('克氏针', [
            ('石膏', 0, 2, (200, 200, 200)), ('不负重', 2, 4, PK), ('部分负重', 4, 8, OR), ('完全负重', 8, 14, GR),
        ], [('0～2 周 腕助力活动（与石膏冲突）', 0), ('2 周 等长', 2), ('5 周 主动', 4.3)]),
        ('掌侧锁定钢板', [
            ('石膏', 0, 2, (200, 200, 200)), ('不负重', 2, 8, PK), ('部分→完全', 8, 14, OR),
        ], [('2 周 腕被动活动', 2), ('4 周后 助力', 4)]),
    ]
    y = 130
    for name, bars, marks in rows:
        dr.text((24, y + 30), name, font=font(30), fill=INK)
        for lab, a, b, c in bars:
            dr.rectangle([X(a), y + 20, X(b) - 3, y + 80], fill=c)
            dr.text((X(a) + 8, y + 34), lab, font=font(24), fill=INK)
        yy = y + 100
        for lab, w in marks:
            dr.ellipse([X(w) - 8, yy + 6, X(w) + 8, yy + 22], fill=RED)
            dr.text((X(w) + 16, yy), lab, font=font(24), fill=RED); yy += 36
        y += 260
    dr.text((24, 960), '灰：石膏或夹板固定  粉：不负重  橙：部分负重  绿：完全负重；红点：腕关节活动开始的时间', font=font(22), fill=GREY)
    return im


# 1 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '原创文章 · 《Journal of Orthopaedic Case Reports》2026', font=font(30), fill=TEAL)
dr.text((70, 135), '提高桡骨远端骨折康复的功能结局', font=font(58), fill=INK)
dr.text((70, 210), '保守、克氏针、掌侧钢板三条路线的分期方案', font=font(44), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Deshpande SS, Ghodke PP, Kale SY, Brahmbhatt HM, Shah HM, Deshpande S.', font=font(26), fill=GREY)
dr.text((70, 390), 'J Orthop Case Rep. 2026;16(1):278-287. doi:10.13107/jocr.2026.v16.i01.6680', font=font(28), fill=GREY)
dr.text((70, 435), '印度 D. Y. Patil 大学物理治疗学院、骨科', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作非商业学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(stack([capbox(raw(1), '原文图 1  揉毛巾：手掌压在毛巾上，用手指把毛巾抓皱'),
            capbox(raw(2), '原文图 2  手指爬行：手指在桌面上一步步向前“走”')], gap=30), 2)
save(stack([capbox(raw(3), '原文图 3  腕和手的活动度训练'),
            capbox(raw(4), '原文图 4  肌腱固定术式训练：伸腕时手指自然屈曲，屈腕时手指自然伸展')], gap=30), 3)
save(capbox(raw(5), '原文图 5  差异性肌腱滑动：手指在几种握拳姿势间依次切换（直手、勾拳、全拳等），让指浅屈肌腱和指深屈肌腱分别滑动'), 4)
save(capbox(raw(6), '原文图 6  用大球做本体感觉训练（原文称“前庭球”）：手掌按球于墙上，给上肢加压'), 5)
save(capbox(raw(7), '原文图 7  抗阻训练：弹力棒、哑铃、治疗泥'), 6)
save(capbox(raw(8), '原文图 8  电刺激：电极贴在前臂伸肌群上'), 7)
save(stack([capbox(raw(9), '原文图 9  四点跪位：通过手掌负重，同时练本体感觉'),
            capbox(raw(10), '原文图 10  BOSU 球上做本体感觉训练（撑起位）')], gap=30), 8)
save(timeline(), 9)

save(card(1200, '落到临床（编者整理）', [
    ('先护骨折，同时别让别的关节僵', '抬高、冷疗、肩肘颈和手指主动活动从第一天就做；腕关节在石膏里可以先做次大等长', PK, RED),
    ('第 5～8 周是活动度关键期', '助力 → 主动活动，肌腱滑动、肌腱固定术式训练、关节松动 I～II 级；注意消肿和 CRPS 的早期迹象', LT, TEAL),
    ('8 周后加力量和负重', '握力、捏力、弹力带、哑铃；四点跪位 → 墙 / 桌 / 地面俯卧撑逐步加负重', GR, (0, 120, 60)),
    ('时间节点要按骨折和固定来调', '原文的周数是作者经验，钢板组比克氏针组还保守；固定越稳，一般可以越早动，最终听术者意见', OR, (200, 120, 0)),
    ('物理因子只当辅助', '激光、冲击波、Matrix 节律治疗、血流限制训练等，原文引用的证据大多是个案或其他部位，别替代主动训练', PU, (110, 70, 190)),
]), 10)

# 封面：原文图 5（差异性肌腱滑动）
c = raw(5); w = c.width; h = round(w * 383 / 900)
if h > c.height: h = c.height; w = round(h * 900 / 383)
x0 = (c.width - w) // 2; y0 = (c.height - h) // 2
c.crop((x0, y0, x0 + w, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
