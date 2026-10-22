#!/usr/bin/env python3
"""Watson 等 2016 Shoulder Elbow 肩关节多向不稳康复方案（上篇，第 1～2 期）：首图为原题直译标题卡；
原文图 1～4 直接用原图（照片内只有分图字母 a/b/c，无英文需要覆盖，原文已遮挡受试者面部），图注译成中文；
原文表 1 另做中文卡片，六期总览、背景卡和临床卡为编者根据原文整理。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
Z = 4
K, G, R = (0, 0, 0), (94, 94, 94), (255, 38, 0)
doc = pymupdf.open(PDF)
PUNC = '，。；、：）”'


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88, optimize=True)


def titled(im, t, W=1200):
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30 and ch not in PUNC:
            k = len(line)
            while ch.isascii() and ch.isalnum() and k and line[k - 1].isascii() and line[k - 1].isalnum(): k -= 1
            if not k: k = len(line)
            lines.append(line[:k]); line = line[k:] + ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in PUNC: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def phases(title, S, n, fs=24):
    W = 1200; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im); y = 20
    for t, bg, c, items in S:
        h = 66 + sum(para_h(s, fs, 1030 - fs * 1.1, gap=8) + 10 for s in items)
        dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
        yy = y + 62
        for s in items: yy = bullet(dr, 70, yy, s, fs, 1060, gap=8) + 10
        y += h + 16
    save(titled(im.crop((0, 0, W, y)), title), n)


import numpy as np

import io


def raw(x):
    return Image.open(io.BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def cover_from(im, cx=0.5, cy=0.5):
    """封面 900×383：从原文插图按比例裁出一块（cx、cy 为裁剪中心的相对位置）"""
    r = 900 / 383; w, h = im.size
    if w / h > r: cw, ch = round(h * r), h
    else: cw, ch = w, round(w / r)
    x = min(max(0, round(cx * w - cw / 2)), w - cw); y = min(max(0, round(cy * h - ch / 2)), h - ch)
    im.crop((x, y, x + cw, y + ch)).resize((900, 383), Image.LANCZOS).convert('RGB').save(f'{OUT}/cover.jpg', quality=90)


def tiles(items, title, n, fs=24):
    """原图并排（等高），下方灰底中文图注"""
    gap = 15; W = 1200; hs = 600
    ims = [x.resize((round(x.width * hs / x.height), hs), Image.LANCZOS) for x, _ in items]
    k = (W - gap * (len(ims) - 1)) / sum(i.width for i in ims)
    ims = [i.resize((round(i.width * k), round(i.height * k)), Image.LANCZOS) for i in ims]
    hh = ims[0].height; ch = max(para_h(t, fs, i.width - 24, gap=8) for i, (_, t) in zip(ims, items))
    im = Image.new('RGB', (W, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im); x = 0
    for i, (_, t) in zip(ims, items):
        im.paste(i, (x, 0)); dr.rectangle([x, hh, x + i.width, hh + ch + 20], fill=(232, 232, 232))
        para(dr, x + 12, hh + 12, t, fs, i.width - 24, gap=8); x += i.width + gap
    save(titled(im, title), n)


def one(x, cap, title, n):
    save(titled(capbox(x, cap), title), n)


def title_card(tag, zh, en, au, cite, org):
    W, H = 1400, 700; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, 18, H], fill=TEAL)
    dr.text((70, 56), tag, font=font(32), fill=TEAL)
    y = 130
    for l in zh: dr.text((70, y), l, font=font(50), fill=INK); y += 70
    y += 20
    for l in en: dr.text((70, y), l, font=font(28), fill=GREY); y += 40
    y += 20; dr.line([70, y, W - 70, y], fill=(200, 205, 210), width=2); y += 30
    dr.text((70, y), au, font=font(30), fill=GREY); y += 44
    dr.text((70, y), cite, font=font(28), fill=GREY); y += 56
    dr.text((70, y), org, font=font(26), fill=GREY)
    dr.text((70, H - 60), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
    save(im, 1)


def roadmap(cur, n):
    """六期总览卡，cur 为本篇覆盖的期"""
    S6 = [('第 1 期', '肩胛控制 + 冠状面 0°～30°（45°）', '上篇'), ('第 2 期', '后方肌群发展（后方“支撑墙”）', '上篇'),
          ('第 3 期', '矢状面屈曲控制 0°～45°', '下篇'), ('第 4 期', '矢状面和冠状面控制 45°～90°', '下篇'),
          ('第 5 期', '三角肌前、中、后束孤立强化', '下篇'), ('第 6 期', '> 90° 及专项/功能性训练、回归', '下篇')]
    W = 1200; im = Image.new('RGB', (W, 40 + 112 * 6), 'white'); dr = ImageDraw.Draw(im)
    for i, (a, b_, c) in enumerate(S6):
        y = 20 + i * 112; on = (i + 1) in cur
        dr.rounded_rectangle([40, y, 1160, y + 96], 14, fill=LT if on else (240, 240, 240))
        dr.text((70, y + 28), a, font=font(34), fill=TEAL if on else GREY)
        dr.text((240, y + 30), b_, font=font(30), fill=INK if on else GREY)
        dr.text((960, y + 30), c + ('（本篇）' if on else ''), font=font(24), fill=RED if on else GREY)
    save(titled(im, 'Watson 多向不稳六期方案总览（编者根据原文整理）'), n)


title_card('综述（临床方案）· Shoulder & Elbow 2016 · 上篇',
           ['用康复方案治疗肩关节多向不稳：第 1 部分'],
           ['The treatment of multidirectional instability of the shoulder', 'with a rehabilitation program: Part 1'],
           'Watson L, Warby S, Balster S, Lenssen R, Pizzari T.',
           'Shoulder Elbow. 2016;8(4):271-278. doi:10.1177/1758573216652086',
           '澳大利亚墨尔本 LifeCare Prahran 运动医学中心 · 拉筹伯大学')

phases('多向不稳（MDI）是怎么回事（编者根据原文整理）', [
    ('是什么', LT, TEAL, ['肩关节在前、后、下两个及以上方向出现症状性不稳，多为非外伤性',
        '和对照者相比，肌力下降、神经肌肉控制改变；肩胛静息时偏向下回旋，抬臂时上回旋不足，肱骨头与关节盂接触面积变小，平移过多',
        '症状从轻微疼痛到恐惧感、撞击、肩袖痛，甚至神经性症状']),
    ('为什么先康复', GR, (40, 120, 60), ['多向不稳最常推荐的初始治疗是康复训练：强化肩胛和肩袖肌群，弥补被动稳定的不足、主动控制肩关节',
        '系统综述支持运动治疗，但证据质量很低；此前唯一可照做的方案（Rockwood 方案）很少关注肩胛和肱骨头控制，也缺少高位上举的训练']),
    ('Watson 方案的思路', OR, (170, 90, 30), ['作者 25 年临床经验总结，分评估和干预两部分、共六期，核心是重建并维持肩胛和肱骨头的控制',
        '各期不严格按顺序，可个体化；全程 3～6 个月；上篇讲评估和第 1、2 期，下篇讲第 3～6 期'])], 2)

one(raw(23), '原文图 1　（a）评估外旋肌力时，治疗师把肩胛托向上回旋，看结果是否改善；（b）肩上举 90° 抗阻外旋时，对肱骨头做由前向后的矫正（也可用抗阻内旋）；（c）负重水平屈曲时，对肱骨头做由后向前的矫正。部分患者因主要不稳方向不同，半脱位方向也会不同。',
    '原文图 1　矫正效果评估（图注编者译成中文）', 3)

roadmap((1, 2), 4)

phases('原文表 1　Watson 方案第 1～2 期（编者译成中文）', [
    ('第 1 期·肩胛阶段：建立肩胛稳定，让肱骨头居中', LT, TEAL, ['动作：站立位肩胛向上回旋，按需要加上提、外展 20°～30°、后倾',
        '剂量：1～3 组 × 20 次（每天 60 次），每次保持 5 秒，每天 2 次；手持 0 → 0.5 → 1 kg，肩胛抗阻带红色 → 绿色',
        '目标：站立向上回旋 3 × 20 次、手持 1 kg，可加绿色抗阻带',
        '注意：站立做不到 5 次先改侧卧；冈上肌痛则手臂外展 0°']),
    ('第 1 期·活动弧阶段：冠状面外展 0°～45° 内的控制', GR, (40, 120, 60), ['外旋/内旋/伸展控制：等长收缩 → 弹力带伸展到中立位 → 弹力带外旋 → 弹力带内旋',
        '外旋力量：侧卧离开支撑面外旋，可加抗阻带',
        '剂量：等长 5～10 次 × 保持 5 秒（20%～30% 最大自主收缩），每天 2～3 次；弹力带 1～3 × 20 次，每天 2 次，黄 → 红；侧卧 0 → 0.5 → 1 kg',
        '目标：外旋、内旋红/绿带 1～2 × 20 次；伸展划船绿带 1～2 × 20 次；侧卧外旋 1 kg 1～2 × 20 次',
        '注意：外旋控制好再练内旋；动作做不稳或诱发疼痛就退回等长；侧卧时腋下垫卷毛巾、离开支撑面；外旋时触摸肱骨头前方，防止向前平移']),
    ('第 2 期：发展后方肌群，为屈曲做准备', OR, (170, 90, 30), ['动作：站立向上回旋（± 后倾/上提）、弹力带外旋、侧卧离开支撑面外旋、俯身划船、外展 45° 弹力带伸展划船，± 抗阻带',
        '剂量：1～3 × 20 次，每天 1～2 次；弹力带绿色；侧卧 1 → 1.5 → 2 kg；俯身划船 0.5 → 1 → 1.5 → 2 kg',
        '目标：3 × 20 次；向上回旋 2 kg、侧卧 1.5～2 kg、外旋绿带、俯身划船 2 kg、45° 伸展划船绿带',
        '注意：俯身划船和站立划船只拉到身体侧方（伸展到中立位）'])], 5, fs=22)

one(raw(40), '原文图 2　（a）站立、外展 20°～30°，肩胛向上回旋的耸肩；（b）用肩胛抗阻带做向上回旋加后倾的肩胛设定',
    '原文图 2　第 1 期·肩胛设定（图注编者译成中文）', 6)
one(raw(41), '原文图 3　（a）弹力带外旋；（b）弹力带伸展（原文图注只写“两图都显示抗阻带”，按正文应为伸展）；两图都配合向上回旋加后倾的肩胛抗阻带',
    '原文图 3　第 1 期·活动弧练习（图注编者译成中文）', 7)

one(raw(47), '原文图 4　（a）侧卧离开支撑面的外旋，配合肩胛抗阻带；（b）伸展划船到外展 45°',
    '原文图 4　第 1～2 期的力量练习（图注编者译成中文）', 8)

phases('落到临床（编者整理）', [
    ('先评估矫正效果', LT, TEAL, ['让患者做一个客观测试（抬臂、外旋肌力等），再分别托肩胛、推肱骨头、两者合用，找出最能改善症状的位置',
        '改善明显，说明运动治疗大概率有效，这个位置就是全程要练的位置；都不改善，要考虑结构性损伤或炎症，先进一步检查']),
    ('肩胛先于手臂', GR, (40, 120, 60), ['第一步只练肩胛设定：外展 20°～30° 位耸肩加向上回旋，3 × 20 次、10 分钟内完成，每天 1～2 次',
        '能对抗抗阻带和手持 1 kg 做 3 × 20 次，再进入活动弧练习']),
    ('从小弧到大弧', OR, (170, 90, 30), ['外旋、伸展先在中段小范围练，控制住再扩大；伸展只到身体侧方，避免肩胛过度前倾',
        '内旋晚于外旋开始，太早练容易胸大肌主导、肩胛前倾']),
    ('先练后方“支撑墙”', PU, (90, 60, 150), ['第 2 期用俯身划船、侧卧外旋和 45° 伸展划船增加后方肌量，防止肱骨头向后平移，再进入下篇的屈曲和高位训练'])], 9)

# 封面：原文图 1 治疗师手法矫正肩胛（真人操作），从左侧裁到 900×383 的比例
f1c = raw(23); cover_from(f1c.crop((0, 24, f1c.width, f1c.height)), 0.0, 0.5)
