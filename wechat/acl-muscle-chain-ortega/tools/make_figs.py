#!/usr/bin/env python3
"""Ortega-Prados 2025 足球运动员 ACL 重建（肌肉链思路）病例：首图中文标题卡；照片图去掉英文字母、
按原位置换成①②③编号并加中文标题条；图 10.1、11.1 两张进阶示意图把英文标签就地换成中文。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); NAVY = (40, 70, 120)
d = pymupdf.open(PDF)
NUM = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫'


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


# ---------- 首图：中文标题卡 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '病例报告 · 《临床医学杂志》（JCM）2025', font=font(32), fill=TEAL)
for i, t in enumerate(['足球运动员 ACL 断裂的创新康复：', '肌肉链思路下的分阶段方案']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '29 岁半职业球员 · 腘绳肌腱自体移植 · 术前 + 术后 6 个阶段 · 12 个月回赛场', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Ortega-Prados P 等，J Clin Med 2025 年第 14 卷 4983', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，原文以 CC BY 4.0 开放获取', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 照片图：去字母、换编号 ----------
DPI = 220; S = DPI / 72


def photo_fig(n, page, rect, title, color=TEAL):
    p = d[page - 1]; r = pymupdf.Rect(*rect)
    labs = [w for w in p.get_text('words') if pymupdf.Rect(w[:4]).intersects(r)]
    lab_pos = [((w[0] + w[2]) / 2, w[1], w[4]) for w in labs if w[4].startswith('(') and len(w[4]) == 3]
    for w in labs: p.add_redact_annot(pymupdf.Rect(w[:4]))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    pix = p.get_pixmap(dpi=DPI, clip=r)
    ph = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    w = ph.width
    out = Image.new('RGB', (w + 60, ph.height + 110), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, w + 60, 80], fill=color); od.text((30, 18), title, font=font(40), fill='white')
    out.paste(ph, (30, 95))
    for cx, y, t in lab_pos:
        k = ord(t[1]) - 65
        ctext(od, 30 + (cx - r.x0) * S, 95 + (y - r.y0) * S + 6, NUM[k], font(38), INK)
    save(out, n)


FIGS = [
    (2, 4, (80, 120, 515, 213), '原文图 1　术前：减轻症状的动作进阶'),
    (3, 4, (80, 273, 515, 402), '原文图 2　术前：减轻症状、维持力量和肌肉量'),
    (4, 5, (80, 70, 515, 200), '原文图 3　术前：找回活动度、逐步加负荷'),
    (5, 7, (165, 412, 556, 687), '原文图 4　术后第 1 期：防肌肉流失、唤醒腘绳肌'),
    (6, 8, (80, 172, 515, 447), '原文图 5　术后第 1 期：防肌肉流失、唤醒股四头肌'),
    (7, 9, (80, 310, 515, 456), '原文图 6　术后第 1 期：练健康部位、练走路'),
    (8, 13, (165, 141, 535, 380), '原文图 7　第 2 期：唤醒腘绳肌（①～⑥）和股四头肌（⑦～⑫）'),
    (9, 13, (165, 465, 535, 697), '原文图 8　第 2 期：腘绳肌（①～⑥）和股四头肌（⑦～⑫）增肌增力'),
    (10, 14, (80, 70, 515, 212), '原文图 9　第 2 期：平衡与原地跑姿'),
    (12, 15, (80, 82, 515, 355), '原文图 10.2　第 2 期：初期跳跃练习举例'),
    (14, 16, (80, 292, 545, 420), '原文图 11.2　减速/制动动作练习'),
    (15, 16, (70, 431, 545, 564), '原文图 11.3　侧向移动练习'),
    (16, 16, (80, 575, 545, 712), '原文图 11.4　冲刺起步练习'),
    (17, 17, (80, 80, 545, 251), '原文图 11.5　跑步步伐练习'),
    (18, 17, (80, 258, 545, 405), '原文图 11.6　跑步技术练习'),
    (19, 21, (80, 96, 545, 394), '原文图 12　第 3 期：足球专项动作'),
]
for n, page, rect, title in FIGS:
    photo_fig(n, page, rect, title)


# ---------- 两张进阶示意图：英文标签就地换中文 ----------
def raw(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


def relabel(x, k, boxes, texts, vbars=()):
    im = raw(x); im = im.resize((im.width * k, im.height * k), Image.LANCZOS); dr = ImageDraw.Draw(im)
    for (x0, y0, x1, y1) in boxes:
        dr.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], fill=(228, 244, 244))
    for (x0, y0, t, fs, col) in texts:
        for i, line in enumerate(t.split('\n')):
            dr.text((x0 * k, y0 * k + i * (fs + 4) * k), line, font=font(fs * k), fill=col)
    for (x0, y0, x1, y1, cx_src, t) in vbars:
        bg = im.getpixel((cx_src * k, (y0 + y1) // 2 * k))
        dr.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], fill=bg)
        fs = 15; yy = (y0 + y1) / 2 - len(t) * (fs + 2) / 2
        for ch in t:
            ctext(dr, (x0 + x1) / 2 * k, yy * k, ch, font(fs * k), 'white'); yy += fs + 2
    return im


DK = (40, 40, 40)
# 图 10.1 跳跃进阶
im = relabel(375, 2,
    [(60, 26, 1170, 50), (20, 220, 145, 256), (20, 338, 145, 358), (25, 440, 135, 460), (25, 554, 135, 574),
     (1072, 128, 1233, 706), (58, 788, 134, 808), (911, 786, 1012, 810), (1069, 786, 1160, 810)],
    [(78, 28, '上肢（推/拉、内收/外展、叉腰/抱胸/上举）　 下肢（屈/伸、内收/外展）　 协调（上下肢）　 扰动/负重　 抛接', 17, DK),
     (40, 228, '多平面组合', 17, DK), (48, 340, '水平面', 17, DK), (48, 442, '冠状面', 17, DK), (48, 556, '矢状面', 17, DK),
     (1080, 133, '其他组合', 15, DK), (1080, 185, '高跳箱 + 多方向', 15, DK), (1080, 260, '高跳箱、不移动', 15, DK),
     (1080, 314, '栏架 + 多方向', 15, DK), (1080, 373, '低跳箱 + 多方向', 15, DK), (1080, 441, '低跳箱、不移动', 15, DK),
     (1080, 501, '台阶 + 多方向', 15, DK), (1080, 553, '台阶、不移动', 15, DK), (1080, 605, '地面/坐姿\n+ 多方向', 15, DK),
     (1080, 680, '地面/坐姿、不移动', 15, DK), (76, 789, '支撑：', 16, DK), (916, 789, '对侧>', 16, DK), (1071, 789, '同侧>', 16, DK)],
    [(171, 119, 187, 209, 172, '等长'), (192, 212, 211, 297, 175, '离心'), (204, 301, 237, 387, 180, '向心推进'),
     (244, 391, 266, 478, 185, '落地缓冲'), (269, 482, 292, 566, 190, '跳跃'), (294, 571, 318, 656, 200, '连续动作'),
     (323, 662, 344, 748, 210, '跨栏')])
w = im.width; out = Image.new('RGB', (w, im.height + 100), 'white'); od = ImageDraw.Draw(out)
od.rectangle([0, 0, w, 90], fill=TEAL); od.text((40, 18), '原文图 10.1　重建跳跃模式的进阶路线（中文标注）', font=font(52), fill='white')
out.paste(im, (0, 100)); save(out, 11)

# 图 11.1 跑步进阶
im = relabel(456, 2,
    [(0, 30, 1131, 58), (15, 140, 115, 174), (10, 230, 130, 250), (20, 324, 120, 344), (20, 430, 120, 450),
     (1008, 140, 1131, 476), (150, 476, 268, 513), (170, 374, 240, 394), (280, 455, 362, 476), (280, 300, 365, 336),
     (388, 424, 468, 445), (392, 288, 446, 326), (492, 380, 596, 418), (492, 259, 596, 279), (610, 343, 702, 382),
     (610, 198, 714, 252), (718, 299, 822, 352), (722, 168, 816, 205), (826, 224, 962, 278), (168, 563, 1131, 592)],
    [(8, 33, '上肢（推/拉、内收/外展）　　下肢（屈/伸、内收/外展）　　协调（上下肢）　　扰动（弹力带、负重、水中…）', 17, DK),
     (22, 148, '多平面组合', 16, DK), (30, 232, '水平面', 16, DK), (35, 326, '冠状面', 16, DK), (35, 432, '矢状面', 16, DK),
     (1015, 147, '变向', 16, DK), (1015, 198, '弧线', 16, DK), (1015, 249, '后退', 16, DK), (1015, 300, '侧向', 16, DK),
     (1015, 351, '向前', 16, DK), (1015, 402, '地面·动态', 16, DK), (1015, 454, '地面·静态', 16, DK),
     (168, 480, '①仰卧/俯卧位', 15, DK), (175, 377, '②坐姿', 15, DK), (282, 458, '①靠墙跑姿', 15, DK),
     (282, 302, '②单腿平衡', 15, DK), (390, 427, '①靠墙跑姿组合', 15, DK), (394, 292, '②跑姿练习\n+ 平衡', 15, DK),
     (494, 383, '①落地缓冲/\n减速', 15, DK), (494, 261, '②加速', 15, DK), (612, 346, '①弓步/单腿硬拉\n+ 靠墙跑姿', 14, DK),
     (612, 201, '②弓步/单腿硬拉\n+ 跑姿练习', 14, DK), (720, 316, '①软/中/硬地面\n慢跑（± 坡度）', 14, DK),
     (756, 170, '②跑步\n（± 坡度）', 15, DK), (828, 243, '跑步 + 动作技能\n（加减速、变向、跳）', 15, DK),
     (175, 567, '支撑：', 16, DK), (272, 567, '0', 16, DK), (318, 567, '单腿平衡', 16, DK), (466, 567, '1 个练习', 16, DK),
     (538, 567, '2 个练习', 16, DK), (615, 567, '3 个练习', 16, DK), (703, 567, '+', 16, DK), (745, 567, '慢跑/跑/冲刺', 16, DK)])
w = im.width; out = Image.new('RGB', (w, im.height + 100), 'white'); od = ImageDraw.Draw(out)
od.rectangle([0, 0, w, 90], fill=TEAL); od.text((40, 18), '原文图 11.1　重建跑步模式的进阶路线（中文标注）', font=font(52), fill='white')
out.paste(im, (0, 100)); save(out, 13)

# ---------- 封面 900×383 ----------
c = Image.open(f'{OUT}/img19.jpg'); c = c.crop((30, 95, c.width - 30, c.height // 2 + 40))
c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = max(0, (c.height - 383) // 2); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
