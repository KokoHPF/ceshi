#!/usr/bin/env python3
"""Voight 等 2010 运动人群髋关节镜术后康复指南：首图为原题直译标题卡；四阶段总览卡和表 1 为编者整理；
原文图 1～13 按原版面直接截取并加中文说明。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
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


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def arrow_down(dr, cx, y0, y1, c=TEAL):
    dr.line([cx, y0, cx, y1 - 14], fill=c, width=6)
    dr.polygon([(cx - 16, y1 - 18), (cx + 16, y1 - 18), (cx, y1)], fill=c)


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * (len(tiles) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def pair(a, b, ca, cb, W=1200):
    """两张照片左右并排，各自上方加说明"""
    w = (W - 14) // 2
    ta, tb = capbox(a, ca, w), capbox(b, cb, w)
    h = max(ta.height, tb.height); out = Image.new('RGB', (W, h), 'white')
    out.paste(ta, (0, 0)); out.paste(tb, (w + 14, 0)); return out


def clip(pn, xs):
    """按原版面截取一组图片（同一张图的拼接条）"""
    pg = doc[pn]; r = pymupdf.Rect()
    for x in xs:
        for rr in pg.get_image_rects(x): r |= rr
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(4, 4), clip=r)
    return Image.open(BytesIO(pix.tobytes('png'))).convert('RGB')


def col(tiles, W=1200):
    """几张带说明的图上下排"""
    H = sum(t.height for t in tiles) + 14 * (len(tiles) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return out


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '临床综述 · Sports Health 2010', font=font(32), fill=TEAL)
dr.text((70, 140), '运动人群髋关节镜术后康复指南', font=font(58), fill=INK)
dr.text((70, 250), 'Postoperative Rehabilitation Guidelines for Hip Arthroscopy', font=font(28), fill=GREY)
dr.text((70, 290), 'in an Active Population', font=font(28), fill=GREY)
dr.line([70, 430, W - 70, 430], fill=(200, 205, 210), width=2)
dr.text((70, 460), 'Voight ML, Robinson K, Gill L, Griffin K. Sports Health 2010;2(3):222-230', font=font(30), fill=GREY)
dr.text((70, 515), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 四阶段总览
W = 1200; im = Image.new('RGB', (W, 1240), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([40, 20, 1160, 150], 14, fill=(240, 240, 240))
para(dr, 70, 40, '术前：宣教或术前预康复（疼痛、肿胀、姿势、代偿、活动度、本体感觉、力量与耐力）；学会负重限制、伤口护理、拐杖，术后马上开始髋部等长收缩和踝泵', 25, 1060, gap=8)
P = [('阶段 1　活动度与初期训练', LT, TEAL, ['目标：保护修复组织、控制疼痛炎症、恢复无痛活动度、防止肌肉抑制、脱拐', '负重：单纯清理类通常足平放负重、1 周内脱拐；盂唇修复、微骨折等需限制负重至 8～10 周', '早期被动内旋、屈曲；四点跪位前后摇；牵引、三维松动；无阻力固定自行车（避免卧式和低头俯身）', '臀肌、股四头肌等等长收缩；蚌式进阶；双腿臀桥、小范围腿举、小蹲；伤口愈合后可下水']),
     ('阶段 2　中期训练与稳定（约第 4 周起）', OR, (180, 90, 20), ['进入条件：活动度接近完全、不拄拐步态正常、几乎不痛', '继续活动度训练直到完全无痛；加入负重和渐进抗阻训练', '纠正肌肉失衡和代偿（常见：屈髋肌、竖脊肌紧，臀肌、腹肌弱）', '核心稳定 + 4 个筛查：骨盆前后倾、骨盆旋转、躯干旋转、臀桥伸膝']),
     ('阶段 3　进阶训练与神经肌肉控制', PU, (90, 60, 150), ['本体感觉重建：关节位置觉 → 功能模式下的本体感觉神经肌肉促进', '双脚站 → 单脚站（睁眼 / 闭眼）→ 提踵、小蹲由双侧到单侧', '弓步、部分深蹲先在水中做；慢 → 快、简单 → 复杂、稳定 → 不稳定']),
     ('阶段 4　回归运动', GR, (40, 120, 60), ['时间取决于病变、术式和项目要求', '模拟日常和专项动作，个体化安排；必要时限制或调整冲击负荷'])]
y = 180
for t, bg, c, items in P:
    h = 70 + sum(para_h(s, 25, 1040, gap=8) + 10 for s in items)
    dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 18), t, font=font(30), fill=c)
    yy = y + 66
    for s in items: yy = bullet(dr, 70, yy, s, 25, 1060, gap=8) + 10
    y += h + 18
im = im.crop((0, 0, W, y))
save(titled(im, '四个阶段一览（编者根据原文整理）'), 2)

save(titled(capbox(clip(2, [6, 7]), 'A→B 四点跪位，臀部向后坐向脚跟，渐进加大幅度；用来牵伸髋关节后关节囊，帮助恢复屈髋和内旋'),
            '原文图 1　四点跪位前后摇'), 3)
save(titled(pair(clip(2, [8]), clip(2, [9]), '图 2　直线牵引：髋关节放在松弛位，沿下肢长轴轻轻牵拉；适合活动时疼痛明显的阶段',
                 '图 3　三维松动：把股骨旋转到受限位置，再做纵向或向下滑动，帮助恢复髋内旋'), '原文图 2、图 3　治疗师手法'), 4)
save(titled(capbox(clip(3, [12, 13]), '侧卧、屈膝、头枕在下方手上。① 双脚并拢、分开双膝（外旋）；② 双膝并拢、分开双脚（内旋，反向蚌式）；③ 上方腿抬起，重复②；④ 上方髋抬起并伸展，再重复②。练习时骨盆保持不动'),
            '原文图 4　蚌式进阶（臀中肌）'), 5)
save(titled(capbox(clip(4, [16, 17]), 'A 双臂上举的三点支撑臀桥；B 骨盆固定在凳子上的抗重力伸髋，这个姿势还能通过交互抑制放松屈髋肌'),
            '原文图 5　臀肌力量训练'), 6)

# 表 1 卡
W = 1200; im = Image.new('RGB', (W, 640), 'white'); dr = ImageDraw.Draw(im)
L = ['侧平板 + 髋外展', '侧卧髋外展', '单腿臀桥 + 核心激活', '单腿深蹲', '弹力带侧向走', '单腿硬拉', '反向蚌式进阶']
R = ['单腿硬拉', '单腿深蹲', '上台阶 + 伸髋', '平板支撑 + 伸髋', '弹力带后退走', '单腿臀桥 + 核心激活', '四点跪位抗阻伸髋']
for x, t, items, bg, c in ((40, '臀中肌', L, LT, TEAL), (620, '臀大肌', R, OR, (180, 90, 20))):
    dr.rounded_rectangle([x, 20, x + 540, 620], 14, fill=bg); ctext(dr, x + 270, 40, t, font(36), c)
    yy = 110
    for s in items: yy = bullet(dr, x + 30, yy, s, 30, 480, gap=8) + 20
save(titled(im, '原文表 1　肌电激活超过 50% 最大自主收缩的动作'), 7)

save(titled(capbox(clip(5, [23, 24, 25, 26, 27]), 'A→B 侧向上台阶：上台阶的脚放在台阶上、髋完全外旋，与支撑脚成 90°，踏上再回到起始位，练臀中肌后部纤维；C 弹力带抗阻髋内旋；D 弹力带抗阻髋外旋'),
            '原文图 6　臀中肌后部纤维和髋旋转力量'), 8)
save(titled(capbox(clip(6, [30]), '侧平板支撑的同时抬起上方腿做髋外展，同时练核心稳定和臀中肌'), '原文图 7　侧平板 + 髋外展'), 9)

t8 = capbox(clip(6, [31]), '图 8　骨盆前后倾：前屈位下骨盆前倾（腰椎更弓）再后倾（腰椎变平），看幅度和流畅度')
t9 = capbox(clip(6, [32]), '图 9　骨盆旋转：双臂交叉放肩上，只转下半身，腰线以上不动，骨盆不侧移')
t10 = capbox(clip(7, [36]), '图 10　躯干旋转：只转上半身，腰线以下不动，胸椎不伸、不侧屈')
t11 = capbox(clip(7, [37]), '图 11　臀桥伸膝：腰带线与地面平行，伸直一侧膝保持 10 秒；悬空侧骨盆下沉、支撑腿抖或抽筋，提示支撑侧臀肌弱')
save(titled(col([t8, t9]), '原文图 8、图 9　核心筛查（1）'), 10)
save(titled(col([t10, t11]), '原文图 10、图 11　核心筛查（2）'), 11)
save(titled(pair(clip(7, [38]), clip(8, [41]), '图 12　在功能性深蹲机上做运动控制追踪练习（看屏幕控制轨迹）',
                 '图 13　不稳定平面单腿站，手持重物沿对角线移动，挑战稳定极限'), '原文图 12、图 13　阶段 3 神经肌肉控制'), 12)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), '髋关节镜术后康复 · 运动人群', font=font(40), fill=TEAL)
dr.text((50, 130), '四个阶段怎么练', font=font(62), fill=INK)
dr.text((50, 220), '从脚尖着地到回场', font=font(62), fill=INK)
dr.text((50, 318), 'Sports Health 2010 · 附 13 张原文动作图', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
