#!/usr/bin/env python3
"""Durall 2012 运动员非特异性颈痛的治疗性训练（Sports Health 现代概念综述）：首图中文标题卡；图 1～13 动作照片
加中文标题，图内 a/b/c 字母修补后换中文标注；图 6 格氏解剖图英文标签修补后改中文引线标注；三阶段方案流程卡。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import numpy as np
import cv2
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def raw(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


def inpaint(im, polys, thr=110, dil=5):
    """多边形内的深色笔画（英文字母）用 OpenCV 修补"""
    a = np.array(im); m = np.zeros(a.shape[:2], np.uint8)
    for poly in polys:
        if len(poly) == 4 and not isinstance(poly[0], (tuple, list)):
            x0, y0, x1, y1 = poly; poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        reg = np.zeros_like(m); cv2.fillPoly(reg, [np.array(poly, np.int32)], 255)
        m[(reg > 0) & (a.min(axis=2) < thr)] = 255
    m = cv2.dilate(m, np.ones((dil, dil), np.uint8))
    return Image.fromarray(cv2.inpaint(a, m, 7, cv2.INPAINT_TELEA))


def tag(dr, x, y, t, fs=40):
    f = font(fs); w = dr.textlength(t, font=f)
    dr.rounded_rectangle([x, y, x + w + 24, y + fs + 18], 10, fill=(255, 255, 255))
    dr.text((x + 12, y + 7), t, font=f, fill=INK)


def titled(ph, title, w=1000):
    ph = ph.resize((w, round(ph.height * w / ph.width)), Image.LANCZOS)
    out = Image.new('RGB', (w, ph.height + 86), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, w, 72], fill=TEAL); od.text((24, 14), title, font=font(38), fill='white')
    out.paste(ph, (0, 86)); return out


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '现代概念综述 · 《运动健康》（Sports Health）2012', font=font(32), fill=TEAL)
for i, t in enumerate(['运动员非特异性颈痛：', '怎么用训练来治']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '活动度 · 深层肌募集 · 耐力与力量 · 位置觉、眼动与平衡 · 三阶段方案', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Durall CJ. Sports Health 2012;4(4):293-301', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 照片图 ----------
save(titled(raw(38), '原文图 1　泡沫轴胸椎伸展自我松动'), 2)
save(titled(raw(36), '原文图 2　墙角胸小肌牵伸（肩外展约 90°）', 800), 3)
save(titled(raw(37), '原文图 3　半充气沙滩球辅助颈椎旋转'), 4)

ph = raw(39); k = 2.25
ph = inpaint(ph, [(0, 15, 50, 70), (0, 750, 50, 810)], 100, 7); dr = ImageDraw.Draw(ph)
tag(dr, 8, 12, '① 用绑带做支点', 46); tag(dr, 8, 752, '② 用食指、中指做支点', 46)
save(titled(ph, '原文图 4　颈椎伸展自我松动', 800), 5)

save(titled(raw(44), '原文图 5　颈椎回缩（收下巴）', 800), 6)

# 图 6：英文标签嵌在解剖图的排线里无法干净去除，改为编者参照格氏解剖图绘制的中文示意图
W6, H6 = 1200, 1110; an = Image.new('RGB', (W6, H6), 'white'); dr = ImageDraw.Draw(an)
BONE = (238, 228, 205); BO = (150, 135, 110); MU = (226, 146, 140); MO = (170, 80, 80); CX = 600
dr.chord([330, 40, 870, 230], 180, 360, fill=BONE, outline=BO, width=3)          # 枕骨基底部
dr.rectangle([330, 132, 870, 136], fill='white')
ys = [175 + 82 * i for i in range(10)]                                              # C1～C7、T1～T3
for i, y in enumerate(ys):
    w = 70 if i == 0 else 62
    dr.rounded_rectangle([CX - w, y, CX + w, y + 60], 14, fill=BONE, outline=BO, width=3)
    if i < 7:
        for sgn in (-1, 1):
            dr.rounded_rectangle([CX + sgn * 70 - (60 if sgn < 0 else 0), y + 18, CX + sgn * 70 + (60 if sgn > 0 else 0), y + 42], 10, fill=BONE, outline=BO, width=3)
dr.arc([180, ys[7] + 10, 1020, ys[7] + 620], 200, 340, fill=BO, width=26)            # 第 1 肋
dr.arc([120, ys[8] + 40, 1080, ys[8] + 700], 205, 335, fill=(200, 188, 165), width=22)  # 第 2 肋


def mus(pts):
    dr.polygon(pts, fill=MU, outline=MO); dr.line(pts + [pts[0]], fill=MO, width=3)


mus([(CX - 25, ys[0] + 10), (CX - 60, ys[0] + 10), (CX - 65, ys[9] + 50), (CX - 35, ys[9] + 50)])         # 左颈长肌
mus([(CX - 115, 125), (CX - 65, 125), (CX - 95, ys[5] + 40), (CX - 130, ys[5] + 40)])                     # 左头长肌
mus([(CX - 135, ys[2] + 25), (CX - 110, ys[2] + 25), (355, 830), (318, 820)])                              # 前斜角肌
mus([(CX + 30, ys[1]), (CX + 68, ys[1]), (CX + 70, ys[9] + 50), (CX + 38, ys[9] + 50)])                    # 右颈长肌垂直部
mus([(CX + 10, ys[0] + 45), (CX + 30, ys[0] + 30), (CX + 130, ys[4] + 30), (CX + 115, ys[4] + 45)])        # 上斜部
mus([(CX + 55, ys[8] + 20), (CX + 62, ys[9] + 30), (CX + 132, ys[5] + 42), (CX + 118, ys[5] + 25)])        # 下斜部
mus([(CX + 40, 128), (CX + 82, 128), (CX + 92, ys[0] + 22), (CX + 60, ys[0] + 22)])                        # 头前直肌
mus([(CX + 150, 118), (CX + 190, 118), (CX + 162, ys[0] + 22), (CX + 136, ys[0] + 22)])                    # 头外侧直肌
mus([(CX + 140, ys[1] + 25), (CX + 168, ys[1] + 25), (850, 812), (805, 806)])                              # 中斜角肌
mus([(CX + 155, ys[4] + 30), (CX + 178, ys[4] + 30), (925, 950), (885, 942)])                              # 后斜角肌
LAB = [('枕骨基底部', (CX - 200, 90), 'L', 60), ('寰椎', (CX - 10, ys[0] + 30), 'L', 150), ('头长肌', (CX - 105, 300), 'L', 290),
       ('颈长肌', (CX - 48, 560), 'L', 520), ('前斜角肌', (CX - 200, 700), 'L', 700), ('第 1 胸椎', (CX - 15, ys[7] + 30), 'L', 830),
       ('第 1 肋', (300, 851), 'L', 960),
       ('头前直肌', (CX + 65, 160), 'R', 50), ('头外侧直肌', (CX + 165, 150), 'R', 130), ('颈长肌（上斜部）', (CX + 80, 300), 'R', 250),
       ('颈长肌（垂直部）', (CX + 52, 560), 'R', 480), ('颈长肌（下斜部）', (CX + 95, ys[7]), 'R', 640),
       ('中斜角肌', (CX + 200, 560), 'R', 400), ('后斜角肌', (905, 946), 'R', 900)]
for t, (X, Y), side, ly in LAB:
    f = font(32); w = dr.textlength(t, font=f)
    tx, ex = (14, 14 + w + 8) if side == 'L' else (W6 - 14 - w, W6 - 14 - w - 8)
    dr.line([ex, ly + 18, X, Y], fill=(60, 60, 60), width=2); dr.ellipse([X - 5, Y - 5, X + 5, Y + 5], fill=RED)
    dr.text((tx, ly), t, font=f, fill=INK)
ctext(dr, W6 / 2, H6 - 50, '示意图：深层颈屈肌＝头长肌、颈长肌、头前直肌、头外侧直肌（另有舌骨肌群，图中未画）', font(26), GREY)
save(titled(an, '原文图 6　颈椎前方深层肌群（编者参照格氏解剖图绘制）', 1200), 7)

ph = raw(46); ph = inpaint(ph, [(400, 45, 500, 100)], 140, 5)
save(titled(ph, '原文图 7　压力反馈仪下的颅颈屈曲（点头）'), 8)

ph = raw(48)
ph = inpaint(ph, [(295, 2, 345, 62), (0, 805, 45, 872), (655, 805, 705, 872)], 100, 7); dr = ImageDraw.Draw(ph)
tag(dr, 300, 6, '① 坐/站位', 40); tag(dr, 6, 808, '② 后仰加难度', 40); tag(dr, 662, 808, '③ 头前伸＝太难了', 40)
save(titled(ph, '原文图 8　颈椎控制性屈曲（逐步后仰加重力）'), 9)

save(titled(raw(50), '原文图 9　下颈段伸展（上颈段保持中立）'), 10)
save(titled(raw(51), '原文图 10　仰卧枕部下压（深层伸肌）'), 11)

ph = raw(52); ph = inpaint(ph, [(0, 8, 48, 68), (0, 945, 48, 1006)], 100, 7); dr = ImageDraw.Draw(ph)
tag(dr, 8, 10, '① 起始', 46); tag(dr, 8, 948, '② 伸肘加阻力', 46)
save(titled(ph, '原文图 11　弹力带颈伸肌等长抗阻', 800), 12)

save(titled(raw(56), '原文图 12　头灯对靶：颈部位置觉训练'), 13)
save(titled(raw(60), '原文图 13　瑞士球仰卧桥式下斜向“砍柴”'), 14)

# ---------- 三阶段方案卡 ----------
W, H = 1000, 2600; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, W, 90], fill=TEAL); dr.text((30, 20), '运动员非特异性颈痛：三阶段训练方案', font=font(44), fill='white')
PH = [
    ('第 1 阶段', '疼痛和激惹性高', '慢、可控、几乎不痛：练协调和本体感觉', (250, 228, 228),
     ['仰卧在半充气沙滩球上转头', '颅颈屈曲（坐位点头或压力反馈仪上点头）', '仰卧把头往小枕头/毛巾卷/沙滩球里压', '头灯对靶（位置觉）',
      '头顶泡沫垫走路', '凳子/瑞士球上移重心或转躯干，眼睛盯住目标', '侧卧肩外旋、俯卧肩后伸', '有手臂症状时：朝向心化方向的重复运动', '每天步行 10～20 分钟']),
    ('第 2 阶段', '激惹性低到中等，活动多了才痛', '重点练肌耐力', (250, 238, 210),
     ['低阻力弹力带颈部四方向等长', '低阻力弹力带回缩等长（图 11）', '“T”字 + 肩外旋', '0° 外展位双侧肩外旋（低到中等阻力）',
      '靠墙滑举（站立肩外展）', '侧卧肩前屈', '本体感觉训练进阶', '胸锁乳突肌、斜角肌、上斜方肌、肩胛提肌、胸小肌牵伸（按需）',
      '泡沫轴胸椎伸展（按需）', '低到中等强度有氧 ≥ 20 分钟', '姿势稳定训练（表 3）']),
    ('第 3 阶段', '激惹性很低或没有，活动时几乎不痛', '重点练力量', (225, 240, 230),
     ['中到大阻力弹力带四方向等长、回缩等长', '躯干训练：平板、侧桥、四点跪伸手抬腿；瑞士球仰卧桥式练习（图 13）',
      '哑铃 I、Y、T', '卧推、划船、肩上举、高位下拉', '本体感觉、牵伸、胸椎松动继续（按需）',
      '中到高强度有氧 ≥ 20 分钟', '姿势稳定训练进阶', '下肢敏捷、上下肢增强式训练']),
]
y = 112


def wrap(t, f, maxw):
    out, cur = [], ''
    for ch in t:
        if dr.textlength(cur + ch, font=f) > maxw: out.append(cur); cur = '  ' + ch
        else: cur += ch
    return out + [cur]


for name, status, emph, col, items in PH:
    f = font(32); lines = [l for it in items for l in wrap('· ' + it, f, W - 120)]
    h = 190 + 46 * len(lines)
    dr.rounded_rectangle([20, y, W - 20, y + h], 16, fill=col)
    dr.text((44, y + 18), name, font=font(42), fill=INK)
    dr.text((44, y + 76), f'状态：{status}', font=font(32), fill=INK)
    dr.text((44, y + 120), f'重点：{emph}', font=font(32), fill=RED)
    for j, l in enumerate(lines):
        dr.text((60, y + 172 + 46 * j), l, font=f, fill=INK)
    y += h + 20
save(im.crop((0, 0, W, y + 10)), 15)

# ---------- 封面 900×383 ----------
c = raw(38); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = max(0, (c.height - 383) // 2); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
