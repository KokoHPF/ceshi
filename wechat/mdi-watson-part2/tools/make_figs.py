#!/usr/bin/env python3
"""Watson 等 2016 Shoulder Elbow 肩关节多向不稳康复方案（下篇，第 3～6 期）：首图为原题直译标题卡；
原文图 1～5 直接用原图（照片内只有分图字母 a/b/c 和墙上的机构标志，无英文说明需要覆盖，原文已遮挡受试者面部），图注译成中文；
原文表 1 另做中文卡片，六期总览、剂量进阶卡和临床卡为编者根据原文整理。
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


title_card('综述（临床方案）· Shoulder & Elbow 2017 · 下篇',
           ['用康复方案治疗肩关节多向不稳：第 2 部分'],
           ['The treatment of multidirectional instability of the shoulder', 'with a rehabilitation programme: Part 2'],
           'Watson L, Warby S, Balster S, Lenssen R, Pizzari T.',
           'Shoulder Elbow. 2017;9(1):46-53. doi:10.1177/1758573216652087',
           '澳大利亚墨尔本 LifeCare Prahran 运动医学中心 · 拉筹伯大学')

roadmap((3, 4, 5, 6), 2)

phases('原文表 1　Watson 方案第 3～4 期（编者译成中文）', [
    ('第 3 期·肩胛阶段：矢状面的肩胛控制', LT, TEAL, ['动作：站立位肩胛向上回旋（± 后倾），从冠状面逐步转到矢状面',
        '剂量：1～3 × 20 次，每天 2 次；0 → 0.5 → 1 → 1.5 → 2 kg；后倾可加红 → 绿色弹力带',
        '目标：矢状面向上回旋（± 后倾）2 × 20 次，1～2 kg，每天 2 次']),
    ('第 3 期·活动弧阶段：矢状面 0°～45° 的控制', GR, (40, 120, 60), ['动作：肩胛平面屈曲 0°～45° → 矢状面屈曲 0°～45°',
        '剂量：1～3 × 20 次，每天 2 次；弹力带黄 → 红 → 绿',
        '目标：矢状面屈曲到 45°，1～2 × 20 次，负荷按功能需要',
        '注意：屈曲时触摸肱骨头，警惕向后平移；肩胛或肱骨头失控就退回第 2 期继续强化']),
    ('第 4 期·肩胛阶段：外展到 90° 的肩胛控制', OR, (170, 90, 30), ['动作：站立伸展划船，外展从 45° 到 90°',
        '剂量：1～3 × 20 次，每天 2 次；弹力带红 → 绿', '目标：外展 90° 站立伸展划船，绿带 1～3 × 20 次']),
    ('第 4 期·活动弧阶段：外展到 90° 的控制', PU, (90, 60, 150), ['外旋/内旋：90° 位外旋、90° 位内旋；屈曲：屈曲到 90°；水平伸展到水平屈曲：90° 位站立伸展划船，逐步转向水平屈曲；± 抗阻带',
        '剂量：1～3 × 20 次，每天 2 次；弹力带红 → 绿；哑铃 0.5～4 kg',
        '目标：90° 位外旋/内旋、屈曲到 90°、水平屈曲，红/绿带各 1～3 × 20 次',
        '注意：如功能需要，外旋/内旋也可在 0°～90° 之间（如外展 45°）练；前向不稳者 90° 位外旋先在肩胛平面做'])], 3, fs=22)

tiles([(raw(33), '原文图 1　配合肩胛抗阻带的屈曲练习（向前出拳）'), (raw(34), '原文图 3　水平屈曲练习')],
      '原文图 1、3　屈曲和水平屈曲（图注编者译成中文）', 4)
one(raw(32), '原文图 2　（a）外展 90° 位伸展划船；（b）外展 90° 位外旋', '原文图 2　第 4 期·外展 90° 位练习（图注编者译成中文）', 5)

phases('原文表 1（续）　Watson 方案第 5～6 期（编者译成中文）', [
    ('第 5 期：三角肌前、中、后束力量', LT, TEAL, ['后束：俯身划船，外展 0° → 45° → 90°；前束：弹力带屈曲（第 3 期）、坐位/站立短力臂负重屈曲；中束：短力臂外展 30°～90°，负重',
        '剂量：1～3 × 8～20 次，每天 1 次到每周 3 次；弹力带红 → 绿 → 蓝 → 黑；哑铃 0 → 0.5 → 1 → 4 kg',
        '注意：俯身划船只拉到伸展中立位；先练后束（更容易控制肱骨头），再练前束、中束']),
    ('第 6 期·活动弧阶段：外展/上举 > 90° 的控制', GR, (40, 120, 60), ['动作：> 90° 到末端范围的外旋、内旋、屈曲和三角肌练习',
        '剂量：募集/耐力（1～2 × 20 次，每天 2 次）→ 力量（3 × 10～12 次）→ 弹震（1～2 × 10 次以上）；弹力带黄 → 红 → 绿 → 蓝；三角肌 0 → 0.5 → 1 kg',
        '目标：外旋、内旋、屈曲各 20 次，范围和负荷向分解练习靠拢',
        '注意：考虑躯干稳定和整个动力链与肩部练习的整合']),
    ('第 6 期·分解练习和完整练习', OR, (170, 90, 30), ['分解练习：把功能动作拆开练并融入专项/功能任务，例如在瑞士球上练游泳的“抓水”阶段',
        '完整练习：参加训练、比赛或工作',
        '剂量和负荷要模拟任务需求；完整练习从小量逐步加大；目标是回归运动、工作和日常功能'])], 6, fs=22)

tiles([(raw(40), '原文图 4　（a）外展 90° 位俯身划船，练三角肌后束；（b）屈曲，练三角肌前束；（c）短力臂外展，练三角肌中束'),
       (raw(41), '原文图 5　自由泳划水“拉”阶段的分解练习；“抓水”和“移臂”阶段也要做分解练习')],
      '原文图 4、5　三角肌练习和专项分解练习（图注编者译成中文）', 7)

phases('剂量、负荷和进阶怎么定（编者根据原文整理）', [
    ('剂量：按能无痛、控制良好完成的次数', LT, TEAL, ['募集：1～3 × 20 次，每天 2～3 次', '耐力：1～3 × 10～15 次，每天 1～2 次',
        '力量：3～4 × 8～12 次，隔天一次；多数练习每次保持 3 秒']),
    ('负荷', GR, (40, 120, 60), ['哑铃从 0 kg（手臂自重）开始，每次加 0.5 kg，多数练习至少到 2 kg',
        '弹力带从黄色开始，女性至少到红色、男性至少到绿色；多数患者还要更重']),
    ('什么时候进阶', OR, (170, 90, 30), ['方式：加大活动弧、加负荷、改剂量或提高上举角度',
        '信号：现有练习无症状；治疗师看到肩胛和肱骨头控制良好；在新练习的模拟位置给等长负荷时仍能保持控制',
        '前面各期的练习继续做，只是剂量和负荷升级；例如 90° 位外旋用红带耐力剂量，0° 位外旋已用蓝带力量剂量']),
    ('病理限制和维持', PK, RED, ['后向为主的不稳：屈曲负荷晚一些；前向为主：外展和末端外旋负荷晚一些；残留后向不稳时不做负重练习',
        '先处理合并问题：颈椎姿势差、颈深屈肌无力、胸廓出口综合征、肩袖炎症、随意性不稳、明显疼痛',
        '结束后每周 2～3 次、每次 4～8 个练习维持；重症者应避免对抗性运动等高风险活动'])], 8)

phases('落到临床（编者整理）', [
    ('屈曲是分水岭', LT, TEAL, ['外展 45° 伸展划船能用绿带做 20 次再开始屈曲；屈曲激活前锯肌强，是提升肩胛上回旋的关键',
        '有后向不稳成分时，屈曲先在肩胛平面练，边练边摸肱骨头有无后移']),
    ('90° 是第二道门', GR, (40, 120, 60), ['先练 90° 位伸展划船，再练 90° 位外旋；外旋红带 20 次后再加内旋',
        '水平屈曲容易让肱骨头后移：从水平伸展起步，几周内一点点转身，直到手臂能横过胸前']),
    ('三角肌按后 → 前 → 中', OR, (170, 90, 30), ['仰卧屈曲练前束时肱骨头后方垫卷毛巾，防止后移']),
    ('专项化收尾', PU, (90, 60, 150), ['把专项动作拆开练（如游泳的抓水、拉水、移臂），剂量模拟真实需求，再回到完整训练',
        '给出维持计划，并讲清楚哪些活动要限制'])], 9)

# 封面：原文图 2 两张外展 90° 弹力带练习（真人动作、红色弹力带醒目），去掉分图字母后按 900×383 比例裁
f2c = raw(32); cover_from(f2c.crop((0, 22, f2c.width, f2c.height)), 0.5, 0.5)
