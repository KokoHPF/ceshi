#!/usr/bin/env python3
"""Davies 等 2015 增强式训练的最新概念：首图中文标题卡；原文图 1～24 动作照片按类别拼板、中文标注
（模糊衣服上的校名与标识、墙上英文标牌和器械品牌）；开练门槛卡为编者根据原文表 1 和正文绘制。
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


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床述评 · 《国际运动物理治疗杂志》2015', font=font(32), fill=TEAL)
for i, t in enumerate(['增强式训练怎么练？', '上下肢 24 个动作 + 剂量指南']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '原理、开练门槛、进阶顺序、训练量和禁忌证', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Davies G, Riemann BL, Manske R. IJSPT 2015;10(6):760-786', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 动作照片：按图号取原图并模糊衣服校名、墙上英文标牌、器械品牌（坐标为 1000 宽比例）
XREF = {1: 22, 2: 23, 3: 27, 4: 28, 5: 29, 6: 30, 7: 34, 8: 85, 9: 86, 10: 84, 11: 90, 12: 94, 13: 91, 14: 92, 15: 93,
        16: 106, 17: 107, 18: 115, 19: 116, 20: 117, 21: 121, 22: 124, 23: 122, 24: 123}
BLUR = {1: [(.36, .40, .64, .58)], 2: [(.42, .28, .72, .42)], 3: [(.50, .23, .74, .36)], 4: [(.45, .33, .64, .47)],
        5: [(.38, .29, .62, .42)], 6: [(.40, .23, .64, .33)], 7: [(.31, .29, .60, .44)], 8: [(.50, .42, .73, .70)],
        9: [(.58, .40, .84, .66)], 10: [(.40, .20, .76, .50)], 12: [(.32, .46, .58, .56)], 13: [(.50, .27, .76, .41)],
        14: [(.45, .25, .62, .39)], 15: [(.53, .60, .65, .67)],
        16: [(.38, .17, .62, .27), (.18, .13, .42, .19), (.60, .09, .69, .13)], 17: [(.26, .28, .43, .41)],
        18: [(.43, .215, .61, .30), (.24, .265, .46, .30), (.65, .20, .71, .24)], 20: [(.25, .25, .40, .38)],
        21: [(.42, .19, .60, .30), (.22, .19, .35, .23), (.64, .145, .70, .18)], 23: [(.37, .20, .70, .41)],
        24: [(.40, .20, .70, .41)]}


def fblur(im, boxes, r=14):
    for f in boxes:
        b = (int(f[0] * im.width), int(f[1] * im.height), int(f[2] * im.width), int(f[3] * im.height))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * im.width / 1000)), b[:2])
    return im


LAB = {1: '图 1　深蹲跳', 2: '图 2　分腿蹲跳', 3: '图 3　侧向跨跳', 4: '图 4　团身跳', 5: '图 5　跳上箱', 6: '图 6　跳深',
       7: '图 7　单腿跳', 8: '图 8　短弧：垫枕限制范围', 9: '图 9　短弧：治疗床支撑', 10: '图 10　全弧：手臂伸出床外',
       11: '图 11　扶墙增强式俯卧撑', 12: '图 12　增强式俯卧撑', 13: '图 13　躯干屈曲抛球', 14: '图 14　躯干旋转',
       15: '图 15　俯卧外旋落球', 16: '图 16　双手胸前传球', 17: '图 17　双手体侧旋转抛', 18: '图 18　双手过顶旋转抛',
       19: '图 19　双手低手旋转抛', 20: '图 20　单手侧臂抛', 21: '图 21　90°/90° 投掷', 22: '图 22　反向投掷（离心减速）',
       23: '图 23　腕屈肌翻球', 24: '图 24　腕伸肌翻球'}
PH = {n: fblur(raw(x), BLUR.get(n, [])) for n, x in XREF.items()}


def row(nums, W=1200, gap=10):
    ims = [PH[n] for n in nums]; hh = 600
    ims = [m.resize((round(m.width * hh / m.height), hh), Image.LANCZOS) for m in ims]
    s = (W - gap * (len(ims) - 1)) / sum(m.width for m in ims)
    ims = [m.resize((round(m.width * s), round(hh * s)), Image.LANCZOS) for m in ims]
    h = ims[0].height; out = Image.new('RGB', (W, h + 52), 'white'); d = ImageDraw.Draw(out); x = 0
    for n, m in zip(nums, ims):
        out.paste(m, (x, 0)); f = font(26)
        while d.textlength(LAB[n], font=f) > m.width - 6: f = font(f.size - 1)
        ctext(d, x + m.width / 2, h + 10, LAB[n], f); x += m.width + gap
    return out


save(board([row([1, 2, 3])], '下肢入门：双腿起跳为主'), 2)
save(board([row([4, 5]), row([6, 7])], '下肢进阶：团身、跳箱、跳深、单腿'), 3)
save(board([row([8, 9, 10])], '上肢术后：从短弧到全弧'), 5)
save(board([row([11, 12])], '上肢闭链：从扶墙到地面'), 6)
save(board([row([13, 14, 15])], '核心与肩外旋：药球练习'), 7)
save(board([row([16, 17]), row([18, 19])], '双手药球抛接'), 8)
save(board([row([20, 21, 22]), row([23, 24])], '单手、过顶投掷专项与腕部'), 9)

# 开练门槛卡
W = 1200; im = Image.new('RGB', (W, 1250), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 10, W - 20, 600], 14, fill=OR)
dr.text((50, 30), '下肢：开练前要过的关（原文表 1）', font=font(36), fill=RED); y = 96
for t in ['下肢无痛、无肿胀，全身关节活动度完整', '单腿站立：睁眼、闭眼各 30 秒',
          '肌力、肌耐力：两侧差距在 20% 以内', '神经肌肉控制：动作质量好、没有代偿',
          '单腿半蹲：无痛、动作质量好', '自由深蹲 1.5～2.5 倍体重；或 5 秒内用 60% 体重深蹲 5 次',
          '低强度增强式动作：无痛、动作质量好']:
    y = para(dr, 70, y, '· ' + t, 29, W - 140, gap=14) + 4
dr.rounded_rectangle([20, 620, W - 20, 1240], 14, fill=LT)
dr.text((50, 640), '上肢：开练前要过的关（作者经验标准）', font=font(36), fill=TEAL); y = 706
for t in ['尊重软组织愈合时间；伤处或术区无痛、无肿或微肿', '活动度、本体感觉：与健侧和常模相比正常',
          '受累肌肉徒手肌力至少 4 级，协同肌 5 级；神经检查和特殊检查阴性',
          '等速肌力：达到健侧峰力矩的 80%', '闭链上肢稳定性测试与常模差距在 20% 以内',
          '坐姿推铅球：两侧和常模相比差距在 20% 以内']:
    y = para(dr, 70, y, '· ' + t, 29, W - 140, gap=14) + 4
save(titled(im, '开练门槛：先过关，再跳、再抛（编者根据原文整理）'), 4)

# 封面 900×383：图 17 体侧旋转抛
c = PH[17]; c = c.crop((0, 150, c.width, 150 + round(c.width * 383 / 900)))
c.resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
