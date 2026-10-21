#!/usr/bin/env python3
"""Rowald 等 2022 活动依赖性脊髓神经调控：首图中文标题卡；原文图 1～6、扩展数据图 1～10、补充图 1～2 的英文标注
按 tools/ocr.py 定位结果（src/o<xref>.json）逐条改为中文，规则见 tools/specs/；每张图加中文图注。
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

import os, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, 'specs')]
import zh
SRC = os.path.join(HERE, '..', 'src')


def zhfig(spec, xref):
    m = importlib.import_module(spec)
    im, _ = zh.apply(raw(xref), f'{SRC}/o{xref}.json', m.SPEC, extra=m.EXTRA)
    return im


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '临床研究 · 《自然 · 医学》2022', font=font(32), fill=TEAL)
dr.text((70, 125), '活动依赖性脊髓神经调控', font=font(56), fill=INK)
dr.text((70, 205), '在完全瘫痪后迅速恢复', font=font(56), fill=INK)
dr.text((70, 285), '躯干和腿部运动功能', font=font(56), fill=INK)
dr.line([70, 390, W - 70, 390], fill=(200, 205, 210), width=2)
dr.text((70, 420), 'Rowald A, Komi S, Demesmaeker R, et al. Nat Med 2022;28(2):260-271', font=font(28), fill=GREY)
dr.text((70, 475), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

FIGS = [('f1', 43, '原文图 1：脊髓解剖的个体差异与个体化计算模型。b 27 人的脊髓节段长度差异很大，背根入髓区宽度却很一致；c～g 由磁共振和断层扫描建立模型，模拟单脉冲刺激下各类纤维的募集'),
        ('f2', 47, '原文图 2：新型电极板的电极排布。b 按平均脊髓确定长度；c 外侧电极离中线 4.7 mm，不怕侧向偏移；d 中线阳极引导电流；e 骶段横向排列电极；f 16 个电极的最终布局'),
        ('f3', 51, '原文图 3：术前规划与术中验证。a 个体化模型；b 模型预测的最佳位置与术中实测一致；c 新电极比传统 5-6-5 电极选择性更好；d 横向电极的多极组合可选择性募集骶段背根'),
        ('f4', 58, '原文图 4：针对具体活动的刺激程序。a 四个功能热点的电极配置库；b 健康人步行的肌肉活动 → 运动神经元激活时空图 → 刺激序列模板；c 实时调整软件；d 配置不到 1 小时即可跑台行走；e 1 周内双杠间行走；f 坐到站、游泳、腿举、骑行'),
        ('f5', 65, '原文图 5：躯干专用刺激程序。a、b 刺激 T12 背根激活躯干和腹部肌肉；c 单侧刺激引起躯干侧向运动；d 刺激纠正腰椎过度前凸；e 刺激下从屈曲位回到直立位明显更快（与 5 名健康人比较）'),
        ('f6', 69, '原文图 6：在社区中恢复独立。a 训练 6 个月后户外独立行走；b 体重支撑逐月减少；c 6 分钟步行距离和 10 米步速；d 站着打拳击、在吧台站着喝东西；e 划桨；f 躯干和大腿肌肉面积增加；g 1 小时 1240 次蹬踏，肌肉活动不衰减'),
        ('e1', 91, '扩展数据图 1：个体化计算模型的建立流程（磁共振和断层扫描 → 分割 → 重建 → 根丝走行 → 神经纤维 → 电导率 → 电缆模型）'),
        ('e2', 110, '扩展数据图 2：用多根丝而不是单根神经根建模很重要；背根入髓区宽度的个体差异远小于节段长度差异'),
        ('e3', 129, '扩展数据图 3：用功能磁共振找出本体感觉传入纤维在脊髓的投射区（被动活动关节或肌腱振动）'),
        ('e4', 151, '扩展数据图 4：结合投射区做术前规划，选出电极板最佳置入位置；与传统 5-6-5 电极对比'),
        ('e5', 173, '扩展数据图 5：只有个体化模型能准确预测最佳电极位置，通用模型或通用肌节分布做不到'),
        ('e6', 192, '扩展数据图 6：配置针对具体活动的刺激方案。仰卧位用 500 毫秒脉冲串测试，伸肌用 20 Hz、屈肌用 100 Hz，治疗师评分后纳入配置库'),
        ('e7', 211, '扩展数据图 7：不同频率的刺激串诱发不同功能动作（20 Hz 偏向承重，100 Hz 偏向全腿屈曲）'),
        ('e8', 233, '扩展数据图 8：刺激第一天的效果。三人都能迈步，肌肉活动和关节活动度明显增加；首次训练最多走 300 多步；两人能主动迈大步'),
        ('e9', 249, '扩展数据图 9：选择性募集躯干肌。T12 背根单脉冲选择性激活躯干肌；高频刺激引起特定一侧的躯干偏移，腿部几乎不动'),
        ('e10', 265, '扩展数据图 10：躯干刺激的即时效果。前拉、四点跪位、肩前举时躯干姿势和控制改善，坐姿下拉器械负重增加'),
        ('s1', 344, '补充图 1：刺激配置软件和无线刺激链路；平板、智能手表、手动按钮和惯性传感器让治疗师和患者都能操作'),
        ('s2', 357, '补充图 2：康复 6 个月后关掉刺激，3 人中有 2 人能主动收缩髂腰肌（术前完全没有肌电活动）')]
for n, (spec, x, cap) in enumerate(FIGS, start=2):
    save(capbox(zhfig(spec, x), cap), n)

c = raw(69); s = c.crop((0, round(c.height * 0.01), c.width, round(c.height * 0.185)))
w = round(s.height * 900 / 383); x0 = (s.width - w) // 2
s.crop((x0, 0, x0 + w, s.height)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
