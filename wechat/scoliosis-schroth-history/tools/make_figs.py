#!/usr/bin/env python3
"""Moramarco & Borysov 2017 Schroth 脊柱侧弯康复与支具的历史（Open Orthop J）：首图中文标题卡；历史时间线、Schroth 要点卡为编者绘制；
原文图 1～13 加中文标题与分格标注（图 5 分型代码另附中文图例）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(38 if W >= 1100 else 32), fill='white')
    out.paste(im, (0, 90)); return out


def xim(x, w=None):
    im = Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')
    if w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    return im


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def tag(dr, x, y, t, fs=26):
    w = dr.textlength(t, font=font(fs))
    dr.rounded_rectangle([x, y, x + w + 20, y + fs + 14], 8, fill=(255, 255, 255), outline=TEAL, width=2)
    dr.text((x + 10, y + 5), t, font=font(fs), fill=TEAL)


def strip(x, w, labels, fs=26, bottom=False):
    """在图片下方加一排中文标签（等分）"""
    im = xim(x, w); n = len(labels); H = fs + 30
    out = Image.new('RGB', (im.width, im.height + H), 'white'); out.paste(im, (0, 0)); dr = ImageDraw.Draw(out)
    for i, t in enumerate(labels):
        ctext(dr, (i + 0.5) * im.width / n, im.height + 10, t, font(fs), TEAL)
    return out


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '专题通讯 · 《开放骨科杂志》2017', font=font(32), fill=TEAL)
for i, t in enumerate(['Schroth 脊柱侧弯康复：', '一百年怎么走过来的']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '旋转成角呼吸 · Lehnert-Schroth 分型 · Chêneau 支具的来龙去脉', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Moramarco K, Borysov M. Open Orthop J 2017;11(Suppl-9, M2):1452-1465', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 时间线 ----------
ev = [('古希腊', '希波克拉底牵引台', 0), ('1921', 'Katharina Schroth 创立方法', 1), ('1947', 'Stagnara 设计里昂支具', 0),
      ('1958', 'Blount 设计密尔沃基支具', 0), ('1970s', 'Lehnert-Schroth 提出分型；Chêneau 拜访 Schroth', 1),
      ('1973', '《脊柱侧弯三维治疗》出版', 1), ('1977', '波士顿支具首次报道', 0), ('1979', 'Chêneau 支具首次研究', 0),
      ('1984', 'Mehta 侧移法', 1), ('1990s', 'Weiss 组织 Schroth-Chêneau 工作坊；RSC 支具', 0),
      ('2008', 'Weiss 独立，推出 Schroth 最佳实践', 1), ('2011 后', 'Gensingen 支具（计算机设计制造）', 0),
      ('2013', 'BrAIST 随机对照试验证实硬支具有效', 0), ('2015', 'Christa Lehnert-Schroth 去世', 1)]
W = 1400; H = 120 + len(ev) * 86; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.line([260, 40, 260, H - 30], fill=(190, 200, 205), width=6)
for i, (y_, t, k) in enumerate(ev):
    y = 50 + i * 86; c = TEAL if k else (190, 100, 40)
    dr.text((240 - dr.textlength(y_, font=font(30)), y + 10), y_, font=font(30), fill=INK)
    dr.ellipse([248, y + 14, 272, y + 38], fill=c)
    dr.rounded_rectangle([300, y, W - 30, y + 66], 12, fill=LT if k else OR)
    dr.text((322, y + 14), t, font=font(30), fill=INK)
dr.text((300, H - 50), '■ 蓝：运动康复　■ 橙：支具', font=font(24), fill=GREY)
save(titled(im, '脊柱侧弯保守治疗大事记（编者根据原文整理）'), 2)

# ---------- 原文图 ----------
save(titled(xim(325, 700), '原文图 1　希波克拉底牵引台', 700), 3)
save(titled(strip(342, 1400, ['Abbott 1910', '密尔沃基支具', '波士顿支具', 'Chêneau 1990s', 'Gensingen 2016'], 28), '原文图 2　支具的演变：从左到右'), 4)
save(titled(xim(349, 1300), '原文图 3　20 世纪 30 年代 Schroth 研究所的集体训练', 1300), 5)
f4 = strip(419, 1200, ['侧弯时原有的呼吸方向', 'Schroth 旋转成角呼吸：把气吸向塌陷的一侧'], 26)
save(titled(f4, '原文图 4　胸廓横断面示意（改编自 Lehnert-Schroth）'), 6)

# 图 5 + 图例
f5 = xim(442, 1300); W = 1300
leg = [('3C', '三弯型：以胸弯为主、躯干平衡'), ('3CH', '三弯型：伴髋部突出'), ('3CTL', '三弯型：胸腰段弯'),
       ('3CL', '三弯型：伴长腰段代偿弯'), ('4C', '四弯型：胸、腰双主弯'), ('4CL', '四弯型：以腰弯为主'), ('4CTL', '四弯型：以胸腰段弯为主')]
L = Image.new('RGB', (W, 60 + 4 * 58), 'white'); dr = ImageDraw.Draw(L)
dr.text((20, 10), '图中代码（编者按通行解释）：3 = 三弯、4 = 四弯（多一个腰骶部代偿弯）', font=font(26), fill=GREY)
for i, (c, t) in enumerate(leg):
    x = 20 + (i % 2) * 640; y = 60 + (i // 2) * 58
    dr.text((x, y), c, font=font(30), fill=RED); dr.text((x + 110, y + 2), t, font=font(28), fill=INK)
both = Image.new('RGB', (W, f5.height + L.height + 10), 'white'); both.paste(f5, (0, 0)); both.paste(L, (0, f5.height + 10))
save(titled(both, '原文图 5　扩展的 Lehnert-Schroth 分型（上：体表；下：对应支具）'), 7)

save(titled(strip(526, 1200, ['站立位', '坐位：按弯型做的日常姿势矫正'], 28), '原文图 6　按弯型设计的日常生活姿势'), 8)

# ---------- Schroth 要点卡 ----------
W, H = 1400, 1180; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
pts = [('旋转成角呼吸', '把气有意识地吸向凹陷的一侧胸廓，配合躯干的去旋转，让塌陷的一侧“鼓起来”', LT),
       ('镜前监控', '对着镜子练，边做边看，及时得到视觉反馈，把矫正动作和身体感觉对上号', LT),
       ('按弯型分类训练', '先用 Lehnert-Schroth 分型判断是三弯还是四弯、哪里是主弯，再选对应的矫正动作', LT),
       ('重视腰骶部代偿弯', '20 世纪 70 年代 Christa Lehnert-Schroth 提出：第 4 个弯（腰骶部）也要一起矫正', LT),
       ('矢状面矫正', '最佳实践版本加入“生理性”训练，先把胸椎后凸、腰椎前凸调回来', GR),
       ('日常生活中的主动自我矫正', '站、坐、拿东西时都按自己的弯型保持矫正姿势，而不只是在训练课上', GR),
       ('短期集中学习', '最佳实践版本主张几天内集中教会，让患者能独立完成，不长期依赖治疗师', GR)]
for i, (t, s, bg) in enumerate(pts):
    y = 20 + i * 162
    dr.rounded_rectangle([20, y, W - 20, y + 146], 14, fill=bg)
    dr.text((50, y + 18), f'{i + 1}　{t}', font=font(36), fill=TEAL)
    line, yy = '', y + 76
    for ch in s:
        if dr.textlength(line + ch, font=font(28)) > 1290: dr.text((50, yy), line, font=font(28), fill=INK); yy += 38; line = ch
        else: line += ch
    dr.text((50, yy), line, font=font(28), fill=INK)
save(titled(im, 'Schroth 方法的核心要素（编者根据原文整理；绿色为“最佳实践”新增）'), 9)

# ---------- 支具相关图 ----------
save(titled(strip(255, 1200, ['不穿支具', '穿 Gensingen 支具', '脱下支具后'], 28), '原文图 7　支具的目标之一：改善躯干对称'), 10)
save(titled(xim(256, 900), '原文图 8　Chêneau 医生在 Schroth 诊所的工作坊（20 世纪 90 年代）', 900), 11)
save(titled(strip(258, 1200, ['不穿支具', '波士顿支具', 'Gensingen 支具'], 28), '原文图 9　同一名 11 岁患者，两种支具相隔 6 周'), 12)
save(titled(xim(260, 1200), '原文图 10　不同国家制作的 Chêneau 支具，外观差异很大'), 13)
save(titled(strip(261, 900, ['不穿支具', '穿支具：过度矫正'], 28), '原文图 11　支具内的过度矫正（2015）', 900), 14)
save(titled(strip(263, 1200, ['不穿支具：胸腰弯 41°', '穿支具：支具内完全矫正'], 28), '原文图 12　13 岁女孩胸腰弯在支具内的矫正（2017）'), 15)
save(titled(strip(265, 1200, ['侧面', '正面', '背面'], 28), '原文图 13　针对胸椎后凸的支具'), 16)

# ---------- 封面 ----------
c = xim(349, 900); top = 110; c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
