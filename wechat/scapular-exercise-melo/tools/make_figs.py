#!/usr/bin/env python3
"""Melo 2025 肩胛治疗性训练：首图为原文标题区；8 周方案总览自绘；附表 A2～A4 动作照片按动作拼图并加中文标注；
原文图 1 流程图中文重绘；原文图 2、图 3（位图柱状图）保留绘图区，标签、标题、图例改中文（见 relabel.py）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import os
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from relabel import relabel

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); RED = (171, 25, 66); TEAL = (0, 110, 130); PINK = (220, 60, 130); GREEN = (60, 150, 70)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def clip(pg, r, dpi=200):
    pix = d[pg].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*r) & d[pg].rect)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def photos(pg):
    p = d[pg]; out = []
    for x in p.get_image_info():
        r = pymupdf.Rect(x['bbox']) & p.rect
        if x['width'] < 100 or r.is_empty: continue
        out.append((r.y0, r.x0, clip(pg, r)))
    out.sort(key=lambda t: (round(t[0] / 100), t[1]))
    return [t[2] for t in out]


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def sheet(title, sub, ims, tags, H=430, W=1240, color=TEAL):
    ims = [m.resize((round(m.width * H / m.height), H), Image.LANCZOS) for m in ims]
    gap = 14; tw = sum(m.width for m in ims) + gap * (len(ims) - 1)
    if tw > W:
        s = W / tw; ims = [m.resize((round(m.width * s), round(m.height * s)), Image.LANCZOS) for m in ims]; tw = W
    h = ims[0].height; top = 150 if sub else 100
    c = Image.new('RGB', (W + 60, top + h + 30), 'white'); dr = ImageDraw.Draw(c)
    dr.rectangle([0, 0, W + 60, 76], fill=color); dr.text((30, 16), title, font=font(42), fill='white')
    if sub: dr.text((30, 92), sub, font=font(30), fill=GREY)
    x = 30 + (W - tw) // 2
    for m, t in zip(ims, tags):
        c.paste(m, (x, top))
        if t:
            f = font(26); w = dr.textlength(t, font=f) + 20
            dr.rounded_rectangle([x + 6, top + 6, x + 6 + w, top + 46], 8, fill=(0, 0, 0))
            dr.text((x + 16, top + 11), t, font=f, fill='white')
        x += m.width + gap
    return c


# ---------- 图 1：原文标题区 ----------
save(clip(0, (30, 96, 565, 184)), 1)

# ---------- 图 2：8 周方案总览（自绘） ----------
W, H = 1500, 1080; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
ctext(dr, W / 2, 24, '8 周肩胛治疗性训练：每周 3 次，共 24 次，每次 25～40 分钟', font(40))
y0 = 100
for i, (t, b, col) in enumerate([('① 准备与热身', '腹式呼吸 + 核心激活\n（各 5～10 次）\n肩部环绕：前、后各 15 次', (226, 240, 244)),
                                  ('② 肩胛神经肌肉控制与力量', '每阶段 4 个主训练动作\n2 组 × 10～15 次\n组间休息 2 分钟，不痛为原则', (252, 232, 240)),
                                  ('③ 拉伸', '胸小肌、上斜方肌/肩胛提肌、\n肩后侧，各 2 次 × 15 秒\n有牵拉感或轻微不适即可', (232, 244, 232))]):
    x0 = 40 + i * 485
    dr.rounded_rectangle([x0, y0, x0 + 455, y0 + 220], 16, fill=col, outline=(150, 150, 150), width=2)
    ctext(dr, x0 + 227, y0 + 18, t, font(34))
    for k, l in enumerate(b.split('\n')): ctext(dr, x0 + 227, y0 + 80 + k * 42, l, font(26), GREY)
y = 380
dr.text((40, y), '每周阻力安排', font=font(34), fill=INK)
cols = {'无': (235, 235, 235), '红': (225, 60, 70), '绿': (60, 150, 70)}
plan = ['无', '红', '红', '绿', '无', '红', '红', '绿']
for w, r in enumerate(plan):
    x0 = 40 + w * 178; dr.rectangle([x0, y + 60, x0 + 168, y + 150], fill=cols[r])
    ctext(dr, x0 + 84, y + 72, f'第 {w + 1} 周', font(28), INK if r == '无' else 'white')
    ctext(dr, x0 + 84, y + 110, {'无': '徒手', '红': '红色弹力带', '绿': '绿色弹力带'}[r], font(24), INK if r == '无' else 'white')
dr.text((40 + 3 * 178 + 10, y + 160), '+ 推箱子任务', font=font(24), fill=RED); dr.text((40 + 7 * 178 + 6, y + 160), '+ 过头放置', font=font(24), fill=RED)
y = 600
for i, (t, rng, ex) in enumerate([('第一阶段（第 1～4 周）', '较小的肩关节活动范围，位置更安全', ['割草机式', '劫匪式', '站立外旋 + 夹肩胛', '坐位 0° 外旋 + 夹肩胛 + 躯干转向患侧']),
                                  ('第二阶段（第 5～8 周）', '较大的肩关节活动范围，要求更高', ['对角线 D2 屈曲（屈曲-外展-外旋）', '双臂抬起 + 外旋', '坐位 90° 外旋 + 夹肩胛 + 躯干转向患侧', '俯卧肩胛平面外展'])]):
    x0 = 40 + i * 725
    dr.rounded_rectangle([x0, y, x0 + 695, y + 420], 16, outline=TEAL, width=4)
    dr.rectangle([x0, y, x0 + 695, y + 70], fill=TEAL); ctext(dr, x0 + 347, y + 16, t, font(34), 'white')
    ctext(dr, x0 + 347, y + 88, rng, font(26), GREY)
    for k, e in enumerate(ex): dr.text((x0 + 30, y + 150 + k * 62), f'{k + 1}. {e}', font=font(30), fill=INK)
save(im, 2)

# ---------- 图 3：准备与热身（附表 A2） ----------
P = photos(18)
save(sheet('准备与热身', '腹式呼吸 → 核心激活 → 肩部环绕', P, ['腹式呼吸', '核心激活 前', '后', '肩部环绕 前', '后'], H=420), 3)

# ---------- 图 4～13：主训练动作（附表 A3） ----------
EX = [(19, '① 割草机式（第一阶段）', '主要募集：下斜方肌、前锯肌、上斜方肌'),
      (20, '② 劫匪式（第一阶段）', '主要募集：中、下斜方肌，前锯肌，上斜方肌'),
      (21, '③ 站立外旋 + 夹肩胛（第一阶段）', '主要募集：中、下斜方肌，前锯肌'),
      (22, '④ 坐位 0° 外旋 + 夹肩胛 + 躯干转向患侧（第一阶段）', '主要募集：下斜方肌、前锯肌'),
      (23, '第 4 周加：推箱子任务', '坐位，桌面不高于胸口，患侧手把 4 kg 的箱子沿桌面推出'),
      (24, '⑤ 对角线 D2 屈曲（第二阶段）', '主要募集：下斜方肌、前锯肌、上斜方肌'),
      (25, '⑥ 双臂抬起 + 外旋（第二阶段）', '主要募集：中斜方肌、肩胛提肌、下斜方肌'),
      (26, '⑦ 坐位 90° 外旋 + 夹肩胛 + 躯干转向患侧（第二阶段）', '主要募集：中、下斜方肌，前锯肌'),
      (27, '⑧ 俯卧肩胛平面外展（第二阶段）', '主要募集：下斜方肌、前锯肌'),
      (28, '第 8 周加：过头放置任务', '坐位，患侧手把 0.5 L 水瓶放到高于头顶的箱子上，再拿回原位')]
for k, (pg, t, sub) in enumerate(EX):
    P = photos(pg)
    tags = ['起始', '结束'] if len(P) == 2 else ['徒手 起始', '徒手 结束', '弹力带 起始', '弹力带 结束']
    save(sheet(t, sub, P, tags, color=PINK if '加' in t else TEAL), 4 + k)

# ---------- 图 14：拉伸（附表 A4） ----------
P = photos(29) + photos(30)
rows = [('胸小肌拉伸', P[0:2]), ('上斜方肌 / 肩胛提肌拉伸', P[2:4]), ('肩后侧拉伸', P[4:6])]
blocks = []
for t, ims in rows:
    ims = [m.resize((round(m.width * 380 / m.height), 380), Image.LANCZOS) for m in ims]
    b = Image.new('RGB', (1240, 440), 'white'); bd = ImageDraw.Draw(b); bd.text((0, 4), t, font=font(34), fill=INK)
    x = (1240 - ims[0].width - ims[1].width - 14) // 2
    for m, tg in zip(ims, ['正面', '背面']):
        b.paste(m, (x, 52)); bd.rounded_rectangle([x + 6, 58, x + 86, 96], 8, fill=(0, 0, 0)); bd.text((x + 16, 62), tg, font=font(26), fill='white'); x += m.width + 14
    blocks.append(b)
c = Image.new('RGB', (1300, 100 + 3 * 460), 'white'); cd = ImageDraw.Draw(c)
cd.rectangle([0, 0, 1300, 76], fill=GREEN); cd.text((30, 16), '课后自我拉伸（每个 2 次 × 15 秒）', font=font(42), fill='white')
for i, b in enumerate(blocks): c.paste(b, (30, 100 + i * 460))
save(c, 14)

# ---------- 图 15：原文图 1 受试者流程 ----------
W, H = 1200, 1000; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def box(x0, y0, x1, y1, lines, fill='white', fs=30, left=False):
    dr.rectangle([x0, y0, x1, y1], fill=fill, outline=(90, 90, 90), width=3)
    y = y0 + (y1 - y0 - len(lines) * (fs + 12)) / 2 + 4
    for l in lines:
        if left: dr.text((x0 + 20, y), l, font=font(fs), fill=INK)
        else: ctext(dr, (x0 + x1) / 2, y, l, font(fs))
        y += fs + 12


def arr(x, a, b):
    dr.line([x, a, x, b], fill=(90, 90, 90), width=4); dr.polygon([(x, b + 4), (x - 11, b - 16), (x + 11, b - 16)], fill=(90, 90, 90))


box(40, 40, 260, 110, ['招募'], (220, 220, 220)); box(300, 40, 760, 110, ['评估是否符合条件（137 人）'])
arr(530, 110, 330); dr.line([530, 210, 640, 210], fill=(90, 90, 90), width=4)
box(640, 140, 1160, 290, ['排除 119 人', '　不符合纳入标准 111 人', '　拒绝参加 8 人'], fs=28, left=True)
box(420, 330, 640, 400, ['分配'], (220, 220, 220))
box(200, 420, 860, 520, ['分配到干预组 18 人，均接受干预'], fs=30); arr(530, 520, 560)
box(420, 560, 640, 630, ['随访'], (220, 220, 220))
box(200, 650, 860, 750, ['中途退出 0 人，失访 0 人'], fs=30); arr(530, 750, 790)
box(420, 790, 640, 860, ['分析'], (220, 220, 220))
box(200, 880, 860, 970, ['纳入分析 18 人，排除 0 人'], fs=30)
save(im, 15)

# ---------- 图 16、17：原文图 2、图 3 ----------
save(relabel(clip(11, (78, 73, 519, 693)), ['外展/内收', '上提/下降', '上旋/下旋', '翼状'],
             ['静息', '伸手', '向前运送', '饮水', '向后运送', '放回'], '活动度（°）', 22), 16)
a = clip(12, (39, 513, 558, 660)); b = clip(13, (38, 58, 557, 440))
c = Image.new('RGB', (max(a.width, b.width), a.height + b.height), 'white'); c.paste(a, (0, 0)); c.paste(b, (0, a.height))
save(relabel(c, ['上斜方', '中斜方', '下斜方', '前锯上中', '前锯下', '肩胛提肌'], ['伸手', '向前运送', '饮水', '向后运送', '放回'], '相对肌电（%）', 21, 130), 17)

# ---------- 封面 ----------
cv = Image.new('RGB', (900, 383), 'white'); dr = ImageDraw.Draw(cv)
P = photos(25); x = 520
for m in P[2:4]:
    m = m.resize((round(m.width * 383 / m.height), 383), Image.LANCZOS); cv.paste(m, (x, 0)); x += m.width + 6
dr.text((36, 46), '肩痛 + 肩胛异常', font=font(48), fill=INK)
dr.text((36, 120), '8 周练什么？', font=font(64), fill=TEAL)
dr.text((36, 225), '8 个弹力带动作 + 2 个生活任务', font=font(28), fill=RED)
dr.text((36, 268), '每周 3 次，分两阶段进阶', font=font(28), fill=RED)
dr.text((36, 330), 'J Pers Med 2025 · 研究精读', font=font(22), fill=GREY)
cv.save(f'{OUT}/cover.jpg', quality=92)
