#!/usr/bin/env python3
"""Brumitt 2013 核心稳定训练处方（下）：首图中文标题卡；检索流程（按原文表 1）、15 项随机对照试验证据地图、
Norris & Matthews 三阶段方案卡、临床推荐（SORT 分级）均为编者中文重绘；封面为中文标题卡裁切。
用法：python3 make_figs.py <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); GY = (240, 240, 240)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t):
    W = im.width
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(38), fill='white')
    out.paste(im, (0, 90)); return out


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def bx(dr, x0, y0, x1, y1, lines, fill, fs=30, col=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 14, fill=fill, outline=(170, 190, 200), width=2)
    yy = (y0 + y1 - len(lines) * (fs + 10)) / 2 + 2
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs), col); yy += fs + 10


def down(dr, x, y0, y1):
    dr.line([x, y0, x, y1 - 14], fill=TEAL, width=5); dr.polygon([(x - 14, y1 - 18), (x + 14, y1 - 18), (x, y1)], fill=TEAL)


# ---------- 首图 + 封面 ----------
def title_card(W, H, big):
    im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, 18, H], fill=TEAL)
    if big:
        dr.text((70, 60), '系统综述 · 《运动健康》（Sports Health）2013', font=font(32), fill=TEAL)
        for i, t in enumerate(['核心稳定训练处方（下）：', '专练深层肌，真的更好吗？']):
            dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
        dr.text((70, 330), '15 项随机对照试验 · 运动控制训练 vs 一般性训练', font=font(30), fill=GREY)
        dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
        dr.text((70, 440), 'Brumitt J 等，Sports Health 2013;5(6):510-513', font=font(30), fill=GREY)
        dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
    else:
        dr.text((50, 60), '核心稳定训练', font=font(64), fill=INK)
        dr.text((50, 160), '专练深层肌 vs 整体练', font=font(54), fill=TEAL)
        dr.text((50, 260), '15 项随机对照试验怎么说', font=font(34), fill=GREY)
    return im


save(title_card(1400, 600, True), 1)
title_card(900, 383, False).save(f'{OUT}/cover.jpg', quality=90)

# ---------- 检索流程 ----------
W, H = 1400, 1000; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
bx(dr, 200, 20, 1200, 140, ['先用 MEDLINE、CINAHL、SPORTDiscus 检索', '“腰痛 + 运动”一项就超过 4100 篇'], GY, 32)
down(dr, 700, 145, 215)
bx(dr, 200, 220, 1200, 340, ['改用 PubMed 临床查询（Clinical Queries）', '优先检出随机对照试验，1966—2013 年 3 月'], LT, 32)
down(dr, 700, 345, 415)
bx(dr, 200, 420, 1200, 560, ['12 组关键词，每组检出少于 200 篇时逐篇看摘要', '纳入：英文、随机对照试验、至少一组为', '运动控制训练或一般性训练'], LT, 30)
down(dr, 700, 565, 635)
bx(dr, 350, 640, 1050, 740, ['纳入 15 项随机对照试验'], TEAL, 40, 'white')
dr.line([525, 745, 525, 800], fill=TEAL, width=5); dr.line([875, 745, 875, 800], fill=TEAL, width=5)
bx(dr, 150, 805, 690, 975, ['8 项：运动控制训练', '对照：全科医生常规处理、', '手法、宣教、McKenzie、安慰剂'], OR, 28)
bx(dr, 710, 805, 1250, 975, ['7 项：一般性训练', '其中 6 项直接与', '运动控制训练对比'], GR, 28)
save(titled(im, '原文表 1　怎么找的文献（编者重绘）'), 2)

# ---------- 证据地图 ----------
rows = [('运动控制训练 vs 其他（8 项）', None),
        ('O’Sullivan 1997', '全科医生常规处理', '+', '疼痛、功能障碍均更好（腰椎峡部裂/滑脱）'),
        ('Moseley 2002', '全科医生常规处理', '+', '8 次课：运动控制 + 手法 + 疼痛神经科学宣教'),
        ('Shaughnessy 2004', '不干预', '+', '10 周局部肌训练，功能障碍和生活质量更好'),
        ('Rasmussen-Barr 2003', '手法治疗', '+', '部分指标更好'),
        ('Niemistö 2003', '仅医生咨询', '+', '部分指标更好（组合了手法和稳定训练）'),
        ('Costa 2009', '安慰剂', '+', '部分指标更好'),
        ('Miller 2005', 'McKenzie 疗法', '≈', '当前疼痛指数两组相近'),
        ('Goldby 2006', '手法治疗', '≈', '两组都改善，仅 6 个月时运动控制组更好'),
        ('一般性训练（7 项，6 项对比运动控制）', None),
        ('Cairns 2006', '运动控制训练', '≈', '1 年时功能障碍、疼痛、心理、健康无差别'),
        ('Critchley 2007', '运动控制 / 宣教', '≈', '3 组 18 个月都改善，组间无差别'),
        ('Koumantakis 2005', '运动控制 + 一般性', '一般', '2 个月时一般性训练组功能障碍更好'),
        ('Norris 2008', '宣教手册', '+', '三阶段方案优于手册（对照不是运动控制）'),
        ('Ferreira 2007', '运动控制 / 脊柱手法', '≈', '原文归入“多数无差别”，未单独描述'),
        ('Macedo 2012', '运动控制训练', '≈', '原文归入“多数无差别”，未单独描述'),
        ('Unsgaard-Tøndel 2010', '运动控制 / 悬吊', '≈', '原文归入“多数无差别”，未单独描述')]
W = 1400; im = Image.new('RGB', (W, 30 + len(rows) * 70), 'white'); dr = ImageDraw.Draw(im)
y = 10
for r in rows:
    if r[1] is None:
        dr.rectangle([10, y + 6, W - 10, y + 62], fill=TEAL); dr.text((26, y + 14), r[0], font=font(32), fill='white')
    else:
        dr.rectangle([10, y + 2, W - 10, y + 66], fill=GY if rows.index(r) % 2 else 'white')
        dr.text((26, y + 16), r[0], font=font(28), fill=INK)
        dr.text((360, y + 16), r[1], font=font(26), fill=GREY)
        col = {'+': (40, 140, 70), '≈': GREY, '一般': (190, 100, 40)}[r[2]]
        tag = {'+': '更好', '≈': '相近', '一般': '一般性更好'}[r[2]]
        dr.rounded_rectangle([640, y + 12, 800, y + 56], 10, fill=col)
        ctext(dr, 720, y + 17, tag, font(26), 'white')
        dr.text((820, y + 18), r[3], font=font(24), fill=INK)
    y += 70
im = titled(im, '15 项试验一览：试验组 vs 对照组（编者按正文整理）')
dr = ImageDraw.Draw(im)
save(im, 3)

# ---------- Norris & Matthews 三阶段 ----------
W, H = 1400, 700; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
st = [('第 1 阶段', '姿势练习', ['姿势控制', '学会脊柱中立位', '下的腹部内收']),
      ('第 2 阶段', '背部体能', ['针对整体肌的', '背部力量与', '耐力练习']),
      ('第 3 阶段', '功能性强化', ['贴近日常和', '运动的功能性', '力量训练'])]
for i, (a, b2, ls) in enumerate(st):
    x0 = 30 + i * 460
    dr.rounded_rectangle([x0, 30, x0 + 400, 140], 14, fill=TEAL)
    ctext(dr, x0 + 200, 42, a, font(30), 'white'); ctext(dr, x0 + 200, 88, b2, font(36), 'white')
    dr.rounded_rectangle([x0, 155, x0 + 400, 400], 14, fill=LT)
    for j, l in enumerate(ls): dr.text((x0 + 40, 185 + j * 66), l, font=font(32), fill=INK)
    if i < 2: dr.polygon([(x0 + 412, 250), (x0 + 448, 280), (x0 + 412, 310)], fill=TEAL)
dr.rounded_rectangle([30, 430, 890, 640], 14, fill=OR)
dr.text((50, 450), '1 → 2 进阶条件', font=font(30), fill=(190, 100, 40))
dr.text((50, 505), '· 不再需要理疗等手段来止痛', font=font(28), fill=INK)
dr.text((50, 555), '· 能在脊柱中立位做出腹部内收', font=font(28), fill=INK)
dr.rounded_rectangle([920, 430, 1350, 640], 14, fill=OR)
dr.text((940, 450), '2 → 3 进阶条件', font=font(30), fill=(190, 100, 40))
dr.text((940, 505), '仰卧单腿抬起', font=font(28), fill=INK)
dr.text((940, 555), '能完成 5 次', font=font(36), fill=RED)
dr.text((30, 660), '6 周方案；对照为背部保健宣教手册。编者根据原文描述绘制', font=font(22), fill=(150, 150, 150))
save(titled(im, 'Norris & Matthews 2008：6 周三阶段背部稳定方案'), 4)

# ---------- 临床推荐 ----------
W, H = 1400, 760; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.text((30, 20), '推荐强度分级（SORT）', font=font(34), fill=TEAL)
for i, (k, v) in enumerate([('A', '一致、高质量、以患者结局为导向的证据'), ('B', '不一致或质量有限、以患者结局为导向的证据'),
                            ('C', '共识、以疾病指标为导向的证据、常规做法、专家意见或病例系列')]):
    dr.text((50, 80 + i * 52), k, font=font(32), fill=RED); dr.text((100, 82 + i * 52), v, font=font(28), fill=INK)
recs = ['腰痛超过 6 周的患者，以运动控制训练为主的运动方案可能有助于减轻疼痛和功能障碍',
        '腰痛超过 6 周的患者，以一般性背部力量训练为主的运动方案也可能获益']
for i, t in enumerate(recs):
    y0 = 270 + i * 230
    dr.rounded_rectangle([30, y0, W - 30, y0 + 200], 14, fill=OR if i == 0 else LT)
    yy = y0 + 40
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(34)) > 1040: dr.text((60, yy), line, font=font(34), fill=INK); yy += 50; line = ch
        else: line += ch
    dr.text((60, yy), line, font=font(34), fill=INK)
    dr.rounded_rectangle([1170, y0 + 40, 1340, y0 + 160], 14, fill=TEAL)
    ctext(dr, 1255, y0 + 52, '证据', font(28), 'white'); ctext(dr, 1255, y0 + 90, 'B 级', font(46), 'white')
dr.text((30, 735 - 20), '原文“临床推荐”框，编者中文重排', font=font(22), fill=(150, 150, 150))
save(titled(im, '原文临床推荐'), 5)
print('ok')
