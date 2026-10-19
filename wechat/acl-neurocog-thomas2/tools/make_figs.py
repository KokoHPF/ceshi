#!/usr/bin/env python3
"""Thomas 等 2024 ACL 重建术后神经认知与神经肌肉康复（第 2 部分）：首图中文标题卡；分期总览、进阶变量卡、
T 跑/L 跑路线示意、重返运动标准卡为编者绘制；原文图 1～12 加中文标注（球衣号码、海报、器械与屏幕文字已模糊，
图 5 屏幕英文提示改为中文）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
# 原文图号 -> xref
X = {1: 55, 2: 66, 3: 78, 4: 87, 5: 88, 6: 89, 7: 90, 8: 100, 9: 99, 10: 106, 11: 107, 12: 114}
# 以宽 600 为基准的模糊区域
BL = {1: [(80, 98, 138, 132), (383, 122, 442, 158)],
      2: [(0, 25, 52, 92), (168, 25, 218, 97), (148, 175, 218, 222), (465, 258, 530, 285)],
      3: [(345, 92, 402, 152), (492, 28, 548, 62), (172, 68, 202, 98), (468, 85, 528, 148)],
      4: [(488, 113, 557, 182), (0, 38, 72, 72), (134, 88, 170, 130)],
      5: [(362, 162, 434, 274), (172, 82, 222, 138), (372, 296, 432, 322)],
      6: [(233, 138, 302, 195), (80, 262, 122, 288), (0, 278, 22, 302), (393, 168, 442, 202), (148, 228, 217, 264)],
      8: [(533, 38, 600, 142), (398, 113, 432, 152), (522, 76, 553, 110), (166, 178, 210, 206), (483, 163, 510, 207)],
      9: [(522, 40, 600, 165), (393, 113, 427, 152), (393, 198, 452, 237), (511, 0, 540, 30), (161, 96, 205, 126), (472, 81, 500, 126)],
      12: [(90, 70, 126, 116), (411, 70, 449, 116)],
      11: [(223, 198, 292, 232), (0, 25, 62, 82), (168, 120, 202, 140), (393, 103, 452, 142)]}


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def fig(n, W):
    im = Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB')
    s = im.width / 600
    for b in BL.get(n, []):
        bb = tuple(int(v * s) for v in b)
        im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(12 * s)), bb[:2])
    if n == 5:  # 屏幕叠加的英文提示改为中文
        d = ImageDraw.Draw(im); bb = tuple(int(v * s) for v in (0, 312, 262, 366))
        d.rectangle(bb, fill=(70, 70, 70)); d.text((int(10 * s), int(318 * s)), '按颜色反应：', font=font(int(34 * s)), fill='white')
        d.ellipse([int(215 * s), int(318 * s), int(255 * s), int(358 * s)], fill=(30, 90, 230))
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200, maxh=820):
    im = fig(n, W)
    if im.height > maxh: im = im.resize((round(im.width * maxh / im.height), maxh), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in f'图 {n}　{cap}':
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, ((W - im.width) // 2, hh + 8)); return t


def board(items, title, W=1200):
    tiles = [tile(n, c, W) for n, c in items]
    H = sum(t.height for t in tiles) + 14 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床述评 · 《国际运动物理治疗杂志》（IJSPT）2024', font=font(32), fill=TEAL)
for i, t in enumerate(['ACL 重建术后后半程：', '把“练大脑”加进康复和测试']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '神经认知与神经肌肉康复 · 第 2 部分（术后第 9 周以后）', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Thomas ZM, Lupowitz L, Ivey M, Wilk KE. Int J Sports Phys Ther 2024;19(12):1629-1640', font=font(28), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 为什么 ----------
W, H = 1400, 560; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.text((40, 20), '精英运动员 ACL 重建后能回到……', font=font(32), fill=TEAL)
for i, (v, t) in enumerate([(81, '任何运动'), (65, '伤前运动水平'), (55, '原来的比赛级别')]):
    y = 80 + i * 90
    dr.text((40, y + 10), t, font=font(30), fill=INK)
    dr.rounded_rectangle([320, y, 320 + 9 * 100, y + 60], 10, fill=(235, 235, 235))
    dr.rounded_rectangle([320, y, 320 + 9 * v, y + 60], 10, fill=TEAL)
    dr.text((320 + 9 * v + 16, y + 10), f'{v}%', font=font(36), fill=TEAL)
dr.line([40, 360, W - 40, 360], fill=(220, 220, 220), width=2)
for i, (v, t) in enumerate([('30%', '再次受伤率最高可达'), ('51%', '拖到术后 9 个月再回场，再伤率下降'), ('约 7 倍', '9 个月前回场，第二次 ACL 损伤风险')]):
    x = 40 + i * 450
    dr.rounded_rectangle([x, 385, x + 430, 540], 14, fill=PK if i != 1 else GR)
    ctext(dr, x + 215, 400, v, font(52), RED if i != 1 else (40, 110, 60)); para(dr, x + 20, 475, t, 26, 390, INK)
save(titled(im, '先看几个数（原文引用的既往研究）'), 2)

# ---------- 分期 ----------
W, H = 1400, 1260; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
ph = [('进阶期', '术后第 9～16 周', LT, '运动学习：联结期（减少错误，不再盯着动作本身）',
       ['继续恢复屈膝（足跟能碰到臀部）', '加大双腿、单腿力量训练；可配合血流限制训练', '神经肌肉控制：前向下台阶 + 激光外部反馈',
        '低强度增强式（各种双腿、单腿小跳），先练“刹车”（减速）再练“油门”',
        '力量达到健侧 65% 以上 → 减重跑台/水下跑台（约 10～12 周），约 14～16 周开始地面跑', '加视觉干扰、工作记忆、扰动：抛接球、彩色灯、数数、颜色词测试']),
      ('功能性专项训练期', '术后第 5～9 个月', GR, '运动学习：自动化期（多平面动作 + 高认知负荷同时完成）',
       ['已完成直线跑进阶；继续增强式、敏捷和专项训练', f'力量接近健侧 85%～90%', '重点：反应性敏捷、多平面稳定、爆发力、冲刺、跳跃落地',
        '反应性组合跑、镜像追随、反应性跳跃、反应性 T 跑/L 跑']),
      ('重返表现期', '术后 9 个月以后', OR, '先回训练，再回比赛（作者 2020 年提出的分阶段回归）',
       ['继续打磨跳跃、落地、单腿平衡、反应时间', '纵跳 + 多步记忆、数数、口令，同时保持双腿负重对称', '绳梯：两种步法切换 + 变向 + 指定手接球，不能断步',
        '诊所（封闭环境）过关后，再进训练场（开放环境）；与队医、体能教练、技术教练保持沟通'])]
y = 20
for t, w, bg, g, items in ph:
    h = 110 + 44 * len(items) + 20
    dr.rounded_rectangle([20, y, W - 20, y + h], 16, fill=bg)
    dr.text((50, y + 18), t, font=font(40), fill=TEAL); dr.text((480, y + 26), w, font=font(32), fill=RED)
    dr.text((50, y + 76), g, font=font(26), fill=GREY)
    for i, it in enumerate(items): dr.text((60, y + 120 + 44 * i), '· ' + it, font=font(27), fill=INK)
    y += h + 20
im = im.crop((0, 0, W, y))
save(titled(im, '术后第 9 周以后的三段（编者根据原文整理）'), 3)

# ---------- 进阶变量 ----------
W, H = 1400, 700; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, 680, 680], 16, fill=LT); dr.rounded_rectangle([720, 20, 1380, 680], 16, fill=OR)
ctext(dr, 350, 40, '怎么加难度（进阶变量）', font(36), TEAL); ctext(dr, 1050, 40, '在练哪种能力（神经认知需求）', font(36), RED)
for i, t in enumerate(['速度', '阻力', '双任务（抛接球、反应棒）', '扰动（推、拉、晃）', '认知任务（数数、记忆等）', '改变视觉（频闪、遮挡）', '干扰数量、颜色种类']):
    dr.text((60, 120 + i * 76), f'{i + 1}', font=font(36), fill=TEAL); dr.text((110, 122 + i * 76), t, font=font(32), fill=INK)
for i, t in enumerate(['视觉', '认知', '决策', '记忆', '双任务', '外部注意焦点', '反应时间']):
    dr.text((760, 120 + i * 76), '✓', font=font(36), fill=RED); dr.text((810, 122 + i * 76), t, font=font(32), fill=INK)
save(titled(im, '每个动作都能这样调（原文表 1、表 2 的共同框架）'), 4)

# ---------- 原文图 ----------
save(board([(1, '前向下台阶 + 激光外部提示（帮助对线）+ 血流限制训练；A、B 为两个时相'),
            (2, '摇板上单腿站 + 颜色词测试：屏幕上出现颜色词，按要求说出底色、字面颜色或字的颜色')], '进阶期①　血流限制与双任务平衡'), 5)
save(board([(3, '侧向滑步 + 扰动：地上贴编号胶带，目标间距约 1.5 米（60 英寸）'),
            (4, '四角目标灯：灯亮哪个就去拍哪个，灯与灯相距约 6.4 米（21 英尺）'),
            (5, '反应踏板：20 秒内保持快速碎步，屏幕显示哪种颜色就尽可能多地踩该颜色')], '进阶期②　侧滑、目标灯、反应踏板'), 6)
save(board([(6, '摇板单腿平衡 + 扰动 + 双任务：同时接多个负重球和网球，按口令用指定的手接'),
            (7, '镜像追随：一人带领变向，另一人跟随反应')], '功能性专项训练期　平衡与对抗反应'), 7)
save(board([(8, '反应性 10 码 T 形跑（口令决定先往哪边）'), (9, '反应性 10 码 L 形跑（口令决定转向方向）')], '反应性跑动测试'), 8)

# ---------- T/L 跑示意 ----------
W, H = 1400, 690; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
def arrow(a, b, c=TEAL, w=8):
    dr.line([a, b], fill=c, width=w)
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - 28 * math.cos(ang - 0.45), b[1] - 28 * math.sin(ang - 0.45)); p2 = (b[0] - 28 * math.cos(ang + 0.45), b[1] - 28 * math.sin(ang + 0.45))
    dr.polygon([b, p1, p2], fill=c)
# T
ctext(dr, 340, 20, 'T 形跑', font(38), TEAL)
s = (340, 520); top = (340, 160); L = (130, 160); R = (550, 160)
for pnt in (s, top, L, R): dr.ellipse([pnt[0] - 14, pnt[1] - 14, pnt[0] + 14, pnt[1] + 14], fill=(240, 130, 40))
arrow((340, 500), (340, 185)); arrow((320, 140), (155, 140), RED); arrow((155, 110), (525, 110), RED); arrow((525, 140), (360, 140), RED)
dr.text((360, 320), '① 直线跑 10 码', font=font(26), fill=INK); dr.text((110, 70), '② 侧滑 5 码 → 反向 10 码 → 回中', font=font(24), fill=RED)
dr.text((250, 570), '③ 转身跑回起点', font=font(26), fill=INK); dr.text((400, 500), '起点', font=font(24), fill=GREY)
# L
ctext(dr, 1040, 20, 'L 形跑', font(38), TEAL)
s2 = (900, 520); c2 = (900, 160); e2 = (1180, 160)
for pnt in (s2, c2, e2): dr.ellipse([pnt[0] - 14, pnt[1] - 14, pnt[0] + 14, pnt[1] + 14], fill=(240, 130, 40))
arrow((900, 500), (900, 185)); arrow((925, 160), (1155, 160), RED); arrow((1160, 190), (930, 190), GREY, 5)
dr.text((920, 320), '① 直线跑 10 码', font=font(26), fill=INK); dr.text((960, 100), '② 按口令转向跑 5 码', font=font(26), fill=RED)
dr.text((960, 210), '③ 转回起点', font=font(24), fill=GREY); dr.text((960, 500), '起点', font=font(24), fill=GREY)
dr.text((40, 640), '1 码 ≈ 0.91 米。口令在跑动中才给出，运动员无法预先计划路线', font=font(26), fill=GREY)
save(titled(im, 'T 形跑与 L 形跑路线（编者根据原文图注示意）'), 9)

save(board([(10, '测力台纵跳：A 下蹲、B 起跳；比较两侧对称性及向心、离心力量；可同时加多步记忆、数数、口令'),
            (11, '反应性绳梯 + 双任务：按口令切换两种步法、变向，并用指定的手接网球'),
            (12, '反应性单腿交叉跳远：起跳后才被告知落哪只脚，须跨过中线，再同侧连续交叉跳两次')], '重返表现期与反应性测试'), 10)

# ---------- 标准卡 ----------
W, H = 1400, 860; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 380], 16, fill=LT)
dr.text((50, 36), 'Kyritsis 等的 6 条（任一条没达到，再断裂风险约增至 4 倍）', font=font(32), fill=TEAL)
ks = ['股四头肌等速（60°/秒）两侧差 < 10%', '单腿跳远 LSI > 90%', '三级跳远 LSI > 90%', '交叉三级跳 LSI > 90%', '完成场上专项训练', 'T 形跑 < 11 秒']
for i, t in enumerate(ks):
    x = 60 + (i % 2) * 660; y = 100 + (i // 2) * 88
    dr.ellipse([x, y + 4, x + 40, y + 44], fill=TEAL); ctext(dr, x + 20, y + 8, str(i + 1), font(28), 'white'); dr.text((x + 60, y + 6), t, font=font(30), fill=INK)
dr.rounded_rectangle([20, 410, W - 20, 840], 16, fill=OR)
dr.text((50, 426), '作者认为传统测试的三个缺口', font=font(32), fill=RED)
gs = [('只看两侧对称', '健侧也会退步（“瘪胎现象”），对称不等于回到伤前水平'),
      ('测试可以预知', '动作固定，运动员可以提前练，成绩里有学习效应'),
      ('没有认知负荷', '加上认知任务后表现会下降，更接近真实比赛')]
for i, (a, b) in enumerate(gs):
    y = 490 + i * 112
    dr.text((60, y), a, font=font(32), fill=INK); para(dr, 330, y + 2, b, 28, 1020, GREY, 8)
save(titled(im, '重返运动测试：现有标准与不足'), 11)

# 封面
c = fig(11, 900); top = 120; c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
