#!/usr/bin/env python3
"""雷蕾等 2026 人工智能在 ACL 损伤诊治中的应用：原文无图无表；首页标题区截图；按正文内容绘制“AI 工具 → 围手术期应用”示意图；封面为文字设计图。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import math
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); RED = (171, 25, 66); BLUE = (40, 90, 160); TEAL = (20, 120, 110); GREY = (120, 120, 120)

d = pymupdf.open(PDF)
pix = d[0].get_pixmap(dpi=200, clip=pymupdf.Rect(55, 100, 470, 226))
Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(f'{OUT}/img01.jpg', quality=88)

W, H = 1600, 1300
im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def ctext(cx, y, t, f, fill):
    for k, l in enumerate(t.split('\n')):
        dr.text((cx - dr.textlength(l, font=f) / 2, y + k * (f.size + 10)), l, font=f, fill=fill)


def pill(cx, y, t, col, w=None):
    f = font(34); w = w or dr.textlength(t, font=f) + 60
    dr.rounded_rectangle([cx - w / 2, y, cx + w / 2, y + 64], 32, fill=col)
    ctext(cx, y + 13, t, f, 'white')


def box(x0, y0, x1, y1, title, body, col):
    dr.rounded_rectangle([x0, y0, x1, y1], 20, fill='white', outline=col, width=5)
    dr.rounded_rectangle([x0, y0, x1, y0 + 70], 20, fill=col)
    dr.rectangle([x0, y0 + 50, x1, y0 + 70], fill=col)
    ctext((x0 + x1) / 2, y0 + 14, title, font(38), 'white')
    ctext((x0 + x1) / 2, y0 + 92, body, font(30), INK)


def arrow(x0, y0, x1, y1, col=GREY):
    dr.line([x0, y0, x1, y1], fill=col, width=7)
    a = math.atan2(y1 - y0, x1 - x0); L = 26
    dr.polygon([(x1, y1), (x1 - L * math.cos(a - 0.45), y1 - L * math.sin(a - 0.45)), (x1 - L * math.cos(a + 0.45), y1 - L * math.sin(a + 0.45))], fill=col)


ctext(W / 2, 30, '人工智能在 ACL 损伤诊治中的应用', font(54), INK)
ctext(W / 2, 110, '常用 AI 工具', font(40), TEAL)
pill(W / 2, 175, '人工智能（AI）', TEAL, 420)
pill(480, 300, '机器学习（ML）', TEAL, 400)
pill(1120, 300, '计算机视觉（CV）', TEAL, 420)
pill(480, 420, '深度学习（DL）', TEAL, 400)
pill(480, 540, '卷积神经网络（CNN）', TEAL, 460)
arrow(W / 2 - 60, 240, 520, 296); arrow(W / 2 + 60, 240, 1080, 296)
arrow(480, 365, 480, 416); arrow(480, 485, 480, 536)
dr.text((720, 440), '多层神经网络，自主提取特征', font=font(28), fill=GREY)
dr.text((750, 560), '擅长图像识别（如 MRI）', font=font(28), fill=GREY)
ctext(1120, 380, '识别、跟踪、测量目标（术中导航）', font(28), GREY)
arrow(W / 2, 625, W / 2, 705, BLUE)
ctext(W / 2, 712, '围手术期应用', font(40), BLUE)
bw, bh = 470, 380; ys = 785; xs = [60, 565, 1070]
R = [('术前管理', '损伤风险预测\n（运动负荷、膝关节\n形态、落地动作）\n\nMRI 辅助诊断\n（撕裂识别、分级）'),
     ('术中应用', '计算机导航\n骨隧道精准定位\n\n★ 定位更准，\n但临床功能评分\n与传统手术无差异'),
     ('术后康复', '阿片类剂量预测\n股神经阻滞需求预测\n冷疗膝内温度预测\n\nAI 支具居家\n远程康复')]
for x, (t, b) in zip(xs, R):
    box(x, ys, x + bw, ys + bh, t, b, BLUE)
dr.text((60, H - 70), '按原文内容自绘示意图', font=font(28), fill=GREY)
im.save(f'{OUT}/img02.jpg', quality=90)

cv = Image.new('RGB', (900, 383), (234, 245, 243)); dr = ImageDraw.Draw(cv)
dr.rectangle([0, 0, 900, 70], fill=TEAL)
dr.text((40, 14), '中华医学杂志 2026 · 综述精读', font=font(34), fill='white')
dr.text((40, 105), 'AI 能看懂 ACL 损伤吗？', font=font(64), fill=INK)
dr.text((40, 200), '从诊断、导航到康复', font=font(56), fill=BLUE)
x = 40
for tg in ['深度学习', 'MRI 诊断', '术中导航', '远程康复']:
    w = dr.textlength(tg, font=font(28)) + 28
    dr.rounded_rectangle([x, 305, x + w, 353], 22, fill='white', outline=TEAL, width=2)
    dr.text((x + 14, 313), tg, font=font(28), fill=TEAL); x += w + 14
cv.save(f'{OUT}/cover.jpg', quality=92)
