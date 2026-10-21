#!/usr/bin/env python3
"""Gassert & Dietz 2018 康复机器人神经生理学视角综述：首图为原题直译标题卡；原文图 1～3 的英文标注是矢量字形——
逐个标注区域删除字形路径（保留插画、色块和线条），在原位置写中文；电机符号 M 和文献作者名、年份保留；
表 1 要点卡、强度剂量卡和设计原则卡为编者根据原文整理。
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


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=90)


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
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
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


def phases(title, S, n, fs=24):
    W = 1200; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im); y = 20
    for t, bg, c, items in S:
        h = 66 + sum(para_h(s, fs, 1030 - fs * 1.1, gap=8) + 10 for s in items)
        dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
        yy = y + 62
        for s in items: yy = bullet(dr, 70, yy, s, fs, 1060, gap=8) + 10
        y += h + 16
    save(titled(im.crop((0, 0, W, y)), title), n)


def zh_fig(pno, crop, labels):
    """删掉标注框内的英文字形路径，渲染后在原位置写中文。labels：(框, 中文, 字号 pt, 颜色, 对齐, 粗体)"""
    pg = doc[pno]
    for bb, *_ in labels:
        pg.add_redact_annot(pymupdf.Rect(bb) + (-0.4, -0.4, 0.4, 0.4), fill=None)
    pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED)
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=pymupdf.Rect(crop))
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); d = ImageDraw.Draw(im)
    for (x0, y0, x1, y1), t, pt, col, al, bold in labels:
        ls = t.split('\n'); s = pt * Z
        f = font(s); lh = s * 1.2
        X0, Y0, X1, Y1 = [(v - o) * Z for v, o in zip((x0, y0, x1, y1), (crop[0], crop[1], crop[0], crop[1]))]
        top = (Y0 + Y1) / 2 - lh * len(ls) / 2
        for i, l in enumerate(ls):
            tw = d.textlength(l, font=f)
            x = {'l': X0, 'r': X1 - tw, 'c': (X0 + X1 - tw) / 2}[al]
            d.text((x, top + i * lh + s * 0.08), l, font=f, fill=col, stroke_width=1 if bold else 0, stroke_fill=col)
    return im


# 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '综述 · J NeuroEng Rehabil 2018', font=font(32), fill=TEAL)
for i, t in enumerate(['康复机器人治疗感觉运动障碍：', '神经生理学视角']):
    dr.text((70, 130 + i * 72), t, font=font(54), fill=INK)
dr.text((70, 300), 'Rehabilitation robots for the treatment of sensorimotor deficits:', font=font(28), fill=GREY)
dr.text((70, 338), 'a neurophysiological perspective', font=font(28), fill=GREY)
dr.line([70, 420, W - 70, 420], fill=(200, 205, 210), width=2)
dr.text((70, 450), 'Gassert R, Dietz V. J Neuroeng Rehabil 2018;15(1):46.', font=font(30), fill=GREY)
dr.text((70, 494), 'doi:10.1186/s12984-018-0383-x', font=font(30), fill=GREY)
dr.text((70, 550), '瑞士苏黎世联邦理工学院健康科学与技术系 · Balgrist 大学医院脊髓损伤中心', font=font(26), fill=GREY)
dr.text((70, 612), '编者中文重排，仅作学术交流（原文 CC BY 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1（第 3 页）
ROWS = [(199.4, 199.6, 212.6, 230.1), (351.3, 351.4, 363.9, 376.8)]
L1 = [((176.3, 94.8, 247.9, 119.0), '固定式\n外骨骼', 10.5, K, 'c', True),
      ((299.8, 94.8, 373.4, 119.0), '固定式\n末端执行器', 10.5, K, 'c', True),
      ((428.4, 95.1, 500.0, 119.0), '可穿戴\n外骨骼', 10.5, K, 'c', True),
      ((78.8, 148.3, 134.4, 174.7), '上肢', 12, K, 'c', True),
      ((78.8, 288.9, 134.4, 315.2), '下肢', 12, K, 'c', True)]
for ds, dv, tr, ce in ROWS:
    L1 += [((71.6, ds, 141.6, ds + 7), '发展状态', 6.6, K, 'c', True),
           ((193.4, dv, 230.7, dv + 5.4), '已成熟', 6.6, K, 'c', False),
           ((317.5, dv, 354.8, dv + 5.4), '已成熟', 6.6, K, 'c', False),
           ((449.0, dv, 479.7, dv + 6.9), '新兴', 6.6, K, 'c', False),
           ((70.6, tr, 142.5, tr + 6.9), '技术综述', 6.6, K, 'c', True),
           ((76.5, ce, 136.7, ce + 5.6), '临床证据', 6.6, K, 'c', True)]
L1 += [((180.4, 212.4, 499.4, 219.8), '上肢：Loureiro 2011，Maciejasz 2014，Sheng 2016（双侧）｜手：Lum 2012，Bos 2016', 6.4, K, 'c', False),
       ((165.4, 226.0, 514.6, 233.4), '固定式：Klamroth 2014｜末端执行器：Lo 2010｜两者：Kwakkel 2008，Mehrholz 2015，Veerbeek 2017', 6.4, K, 'c', False),
       ((263.1, 235.3, 415.7, 242.1), '手：Balasubramanian 2010，Lambercy 2011', 6.4, K, 'c', False),
       ((278.7, 363.8, 399.7, 369.3), '固定式和可穿戴：Diaz 2011', 6.4, K, 'c', False),
       ((163.7, 376.7, 515.9, 384.1), '固定式：Tefertiller 2011，Benito-Penalva 2012，Nam 2017｜可穿戴：Louie 2016｜两者：Mehrholz 2017', 6.4, K, 'c', False)]
fig1 = zh_fig(2, (57, 89, 538, 388), L1)

WEDGE = lambda y: [((480.6, y, 526.8, y + 6.2), '负重', 6.6, G, 'r', True),
                   ((416.6, y + 7.6, 526.8, y + 13.9), '认知和身体参与', 6.6, G, 'r', True),
                   ((416.6, y + 15.2, 526.8, y + 21.5), '功能性 / 生理性运动', 6.6, G, 'r', True),
                   ((341.5, y + 22.9, 526.8, y + 29.2), '患者的功能能力 / 技术复杂度', 6.6, G, 'r', True)]
fig2 = zh_fig(4, (57, 369, 538, 655), [
    ((480.6, 386.6, 512.7, 406.5), '部分\n抗重力\n支持', 6.6, R, 'r', True),
    ((389.8, 412.6, 427.1, 432.5), '虚拟物体\n动力学\n渲染', 6.6, R, 'r', True),
    ((492.7, 426.9, 521.4, 438.6), '功能性\n手部使用', 6.6, R, 'l', True),
    ((458.4, 571.0, 476.8, 574.4), '耦合', 5, K, 'c', True),
    ((114.5, 637.5, 159.8, 646.1), '单手', 10, G, 'c', True),
    ((257.6, 637.5, 338.7, 646.1), '双手分开', 10, G, 'c', True),
    ((418.8, 637.5, 513.8, 646.1), '双手协同', 10, G, 'c', True)] + WEDGE(508.0))
fig3 = zh_fig(5, (57, 89, 538, 302), [
    ((426.5, 195.0, 465.0, 207.8), '髋伸展\n力矩', 6.6, R, 'r', True),
    ((411.9, 211.7, 454.0, 224.6), '传入输入\n负重', 6.6, R, 'r', True)] + WEDGE(267.2))

save(titled(capbox(fig1, '编者把原图英文译成中文。按训练部位分上肢和下肢；按结构分固定式外骨骼、固定式末端执行器和可穿戴外骨骼。前两类已经成熟，可穿戴外骨骼正在进入临床。下方三行分别列出发展状态、技术综述和临床证据的代表文献'),
            '原文图 1　康复机器人的分类'), 2)
save(titled(capbox(fig2, '上图：从高阻抗的工业机械臂，到在末端或每个关节提供控制的专用康复机器人，再到能渲染虚拟物体动力学、给出体感反馈的系统；未来会有可穿戴系统在家中日常活动时提供支持。楔形条表示从左到右负重、患者参与、功能性运动和技术复杂度递增。下图：手功能训练除了单手够取抓握，还应包括双手分开和双手协同任务（如拧瓶盖）；M 为电机'),
            '原文图 2　上肢康复机器人的演变（中文标注）'), 3)
save(titled(capbox(fig3, '从左到右：卧位工业机械臂被动带动下肢 → 减重跑台步态机器人 → 拐杖平衡的可穿戴外骨骼 → 未来可按需支持平衡的外骨骼。右边三种系统借鉴神经生理学：通过负重、足底着地和辅助髋伸展刺激传入感受器，触发屈腿。越往右患者需要的功能越多，机器人提供的支持越少，多数患者在不同恢复阶段会用到其中几种'),
            '原文图 3　下肢康复机器人的演变（中文标注）'), 4)

phases('上肢和下肢恢复有什么不同（编者根据原文整理）', [
    ('上肢 · 脑卒中、皮质脊髓束受损', PK, RED, ['恢复很少，尤其慢性期的手指伸展', '目标：激活近端肌、避免挛缩、患手能做支撑和固定',
        '技术：被动活动（位置控制）或减重下自主近端运动；带伸展偏置的手部模块；日常可用意图检测（力、肌电、眼动）触发的辅助']),
    ('上肢 · 脑卒中、皮质脊髓束完整', OR, (180, 90, 20), ['自发恢复约为初始损伤的 70%～80%（比例恢复规律）', '目标：够取和简单抓握，单手 / 双手日常活动',
        '技术：够取抓握时近端减重；针对单关节（含手指）和双手协同的专用设备；剂量效应有限，亚急性期 > 慢性期']),
    ('上肢 · 不完全脊髓损伤（常见 C6/7）', PU, (90, 60, 150), ['前臂屈肌痉挛会妨碍形成肌腱固定抓握', '目标：肌腱固定抓握、双手抓握',
        '技术：主动外骨骼 / 手套，由近端动作（如关节角度传感器）触发腕和手指屈伸']),
    ('下肢 · 脑卒中偏瘫、不完全脊髓损伤', GR, (40, 120, 60), ['脑卒中：自发恢复，可借痉挛支撑身体；脊髓损伤：需要一定近端肌功能和痉挛张力',
        '目标：不用辅助器具独立行走', '关键：负重（减重 / 再加载）和髋伸展产生合适的传入；步速和髋伸展启动摆动；有剂量效应',
        '技术：按瘫痪程度减重；重度用位置 / 导纳控制，轻中度用可变阻抗控制；机器人辅助髋伸展来激活屈腿肌'])], 5)

phases('机器人能多给什么（编者根据原文整理）', [
    ('重复次数', LT, TEAL, ['常规治疗：偏瘫患者 45 分钟只做约 30 次患侧上肢动作', '机器人辅助：每次可超过 1000 次']),
    ('剂量', OR, (180, 90, 20), ['慢性脑卒中剂量研究平均 13.6～26.3 小时，没有看到强度效应', '另一研究给到 300 小时，出现了有临床意义的改善',
        '作者推断：标准治疗的剂量可能不够高']),
    ('人力', PU, (90, 60, 150), ['减重跑台训练需要两名治疗师在两侧带腿，每天大约只能练半小时', '机器人减重步态训练效果与治疗师辅助相当，但可以练更久、用更少人']),
    ('参与度', GR, (40, 120, 60), ['按需辅助避免“偷懒”；自动调难度、认知挑战和即时反馈提升参与', '运动反馈和运动输出同步时，还可能促进运动皮层可塑性'])], 6)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), '康复机器人 · 脑卒中 · 脊髓损伤', font=font(34), fill=TEAL)
dr.text((50, 128), '康复机器人该怎么设计？', font=font(56), fill=INK)
dr.text((50, 214), '先懂神经生理', font=font(56), fill=INK)
dr.text((50, 318), '上肢 vs 下肢 · 按需辅助 · 剂量 · 可穿戴', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
