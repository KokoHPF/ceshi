#!/usr/bin/env python3
"""Wilk 等 2021 青少年投掷十项训练方案：首图中文标题卡；原文图 1～6 动作照片两两拼板、中文标注
（模糊衣服和墙上球衣的英文字样）；方案总览卡与投球风险提示卡为编者根据原文绘制。
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


def fblur(im, boxes, r=10):
    for f in boxes:
        b = (int(f[0] * im.width), int(f[1] * im.height), int(f[2] * im.width), int(f[3] * im.height))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * im.width / 500)), b[:2])
    return im


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床观点 · 《国际运动物理治疗杂志》2021', font=font(32), fill=TEAL)
dr.text((70, 140), '青少年投掷十项训练方案：', font=font(54), fill=INK)
dr.text((70, 218), '一套增强青少年过顶投掷运动员', font=font(44), fill=INK)
dr.text((70, 280), '肩关节动态控制的训练变式', font=font(44), fill=INK)
dr.line([70, 380, W - 70, 380], fill=(200, 205, 210), width=2)
dr.text((70, 410), 'Wilk KE, Lupowitz LG, Arrigo CA. IJSPT 2021;16(6):1387-1395', font=font(30), fill=GREY)
dr.text((70, 465), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 照片：模糊衣服上的英文和墙上球衣名字
XR = {1: 53, 2: 59, 3: 60, 4: 66, 5: 67, 6: 71}
BL = {1: [(.40, .30, .66, .38), (.35, .0, .72, .15), (.88, .03, 1.0, .24)],
      2: [(.05, .08, .23, .26), (.36, .16, .54, .30), (.61, .10, .81, .25), (.86, .17, 1.0, .28), (.63, .41, .80, .57)],
      3: [(.08, .16, .36, .25), (.52, .15, .96, .255), (.36, .35, .54, .43)],
      4: [(.56, .17, .76, .30), (.78, .16, 1.0, .41), (.02, .13, .24, .23), (.58, .31, .76, .42)],
      5: [(.70, .07, .88, .29), (.10, .0, .92, .055), (.50, .28, .70, .38), (.50, .11, .55, .26)],
      6: [(.06, .10, .25, .25), (.31, .10, .43, .24), (.53, .14, .68, .26), (.73, .10, .90, .23), (.91, .15, 1.0, .28), (.38, .34, .60, .42)]}
LAB = {1: '图 1　弓步位满罐', 2: '图 2　侧桥位侧卧外旋', 3: '图 3　半蹲位低位划船', 4: '图 4　半蹲位改良“举手投降”',
       5: '图 5　单腿蹲', 6: '图 6　弹力带侧向滑步'}
PH = {n: fblur(raw(x), BL[n]) for n, x in XR.items()}


def row(nums, W=1200, gap=10):
    ims = [PH[n] for n in nums]; hh = 640
    ims = [m.resize((round(m.width * hh / m.height), hh), Image.LANCZOS) for m in ims]
    s = (W - gap * (len(ims) - 1)) / sum(m.width for m in ims)
    ims = [m.resize((round(m.width * s), round(hh * s)), Image.LANCZOS) for m in ims]
    h = ims[0].height; out = Image.new('RGB', (W, h + 56), 'white'); d = ImageDraw.Draw(out); x = 0
    for n, m in zip(nums, ims):
        out.paste(m, (x, 0)); ctext(d, x + m.width / 2, h + 12, LAB[n], font(28)); x += m.width + gap
    return out


save(board([row([1, 2])], '肩袖与肩胛：结合下肢和核心的姿势'), 3)
save(board([row([3, 4])], '半蹲位肩胛练习'), 4)
save(board([row([5, 6])], '下肢与髋：单腿控制和臀中肌'), 5)

# 方案总览卡
W = 1200; im = Image.new('RGB', (W, 1330), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 10, W - 20, 150], 14, fill=(240, 240, 240))
para(dr, 50, 30, '每个练习 2 组 × 10 次，组间几乎不休息；只用自重和一根弹力带。全程提示肩胛“后倾、外旋、后缩”', 30, W - 100, gap=14)
blocks = [('1　肩内旋、外旋', '肩外展 0°，腋下夹毛巾卷（没有就夹手套），弹力带内旋、外旋', LT, TEAL),
          ('2　弓步位（双腿交替）', '满罐：拇指朝上、两臂在肩胛平面上举到肩高，顶端停 2 秒\n侧平举：掌心向下，举到外展 90°', OR, RED),
          ('3　侧卧外旋', '弹力带外旋，可进阶到屈膝侧桥、标准侧桥', GR, (40, 120, 60)),
          ('4　半蹲位（髋膝屈 90°，躯干直立）', '低位划船 → 改良“举手投降” → 高位划船接 90°/90° 外旋', PK, RED),
          ('5　肘和前臂', '弹力带二头肌弯举、三头肌伸展；腕屈、腕伸、前臂旋前、旋后', (234, 230, 246), (100, 70, 160)),
          ('6　下肢与核心', '单腿蹲或向前下台阶；弹力带侧向滑步（从膝上逐步移到脚踝）', (250, 240, 215), (150, 100, 20))]
y = 170
for h, t, bg, col in blocks:
    n = len(t.split('\n')); hh = 92 + 44 * n + (40 if len(t) > 36 and n == 1 else 0)
    dr.rounded_rectangle([20, y, W - 20, y + hh], 14, fill=bg); dr.text((50, y + 18), h, font=font(34), fill=col)
    yy = y + 72
    for line in t.split('\n'): yy = para(dr, 70, yy, line, 29, W - 130, gap=12)
    y += hh + 14
im = im.crop((0, 0, W, y + 6))
save(titled(im, '方案总览：一根弹力带、6 类练习（编者根据原文整理）'), 2)

# 投球风险提示卡
im = Image.new('RGB', (W, 1000), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 10, W - 20, 470], 14, fill=PK)
dr.text((50, 28), '原文汇总的高风险因素', font=font(34), fill=RED); y = 90
for t in ['手臂疲劳时还在投：受伤风险约 36 倍', '每场投 80 球以上约 4 倍；一年投 8 个月以上约 5 倍',
          '球速 85 英里/小时以上约 2.6 倍；比同龄人高 4 cm、重 5 kg 也要多留意',
          '一年中有 69% 的投手带着手臂疲劳投球，38% 带着疼痛投球']:
    y = para(dr, 70, y, '· ' + t, 29, W - 130, gap=12) + 6
dr.rounded_rectangle([20, 490, W - 20, 990], 14, fill=LT)
dr.text((50, 508), '美国运动医学研究所的青少年投手建议', font=font(34), fill=TEAL); y = 570
for t in ['每年至少 4 个月不参加比赛投球', '遵守投球数和休息日限制', '不在赛季重叠的多支球队同时当投手',
          '不同时担任投手和捕手', '除棒球外参加其他运动', '肩或肘一痛就停止投球']:
    y = para(dr, 70, y, '· ' + t, 29, W - 130, gap=12) + 4
im = im.crop((0, 0, W, 1000))
save(titled(im, '先控制投球量，再谈练习（编者根据原文整理）'), 6)

# 封面 900×383：图 2 侧桥位外旋
c = PH[2]; h = round(c.width * 383 / 900); y0 = int(c.height * .28)
c.crop((0, y0, c.width, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
