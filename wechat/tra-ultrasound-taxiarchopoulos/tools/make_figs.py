#!/usr/bin/env python3
"""Taxiarchopoulos 2023 超声生物反馈训练腹横肌：首图为原文标题区；图 1a 患者衣服上的英文模糊，图 1b 裁掉超声仪英文界面并把标注改中文；
图 2 运动控制测试照片（取原始图像，不带 a/b 字母）配中文标注；附录 A 训练动作照片按阶段拼图加中文；腹横肌 6 级进阶图自绘；图 3 流程图中文重绘。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import io
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); RED = (190, 40, 50); GREEN = (40, 140, 70); BLUE = (30, 90, 160); TEAL = (0, 110, 130)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def clip(pg, r, dpi=200):
    pix = d[pg].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*r))
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def raw(xref):
    return Image.open(io.BytesIO(d.extract_image(xref)['image'])).convert('RGB')


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def tag(dr, x, y, t, col=(0, 0, 0), fs=26):
    f = font(fs); w = dr.textlength(t, font=f) + 20
    dr.rounded_rectangle([x, y, x + w, y + fs + 14], 8, fill=col); dr.text((x + 10, y + 5), t, font=f, fill='white')


def board(title, rows, color=TEAL, H=300, W=1240):
    """rows: [(名称, 说明, [图...], [标签...])]"""
    blocks = []
    for name, note, ims, tags in rows:
        ims = [m.resize((round(m.width * H / m.height), H), Image.LANCZOS) for m in ims]
        tw = sum(m.width for m in ims) + 12 * (len(ims) - 1)
        if tw > W:
            s = W / tw; ims = [m.resize((round(m.width * s), round(m.height * s)), Image.LANCZOS) for m in ims]; tw = W
        top = 54 + (40 if note else 0)
        b = Image.new('RGB', (W, top + ims[0].height + 10), 'white'); bd = ImageDraw.Draw(b)
        bd.text((0, 4), name, font=font(34), fill=INK)
        if note: bd.text((0, 50), note, font=font(26), fill=GREY)
        x = (W - tw) // 2
        for m, t in zip(ims, tags):
            b.paste(m, (x, top))
            if t: tag(bd, x + 6, top + 6, t, RED if t == '错误' else (GREEN if t == '正确' else (0, 0, 0)))
            x += m.width + 12
        blocks.append(b)
    c = Image.new('RGB', (W + 60, 96 + sum(b.height + 26 for b in blocks)), 'white'); cd = ImageDraw.Draw(c)
    cd.rectangle([0, 0, W + 60, 76], fill=color); cd.text((30, 16), title, font=font(42), fill='white')
    y = 96
    for b in blocks: c.paste(b, (30, y)); y += b.height + 26
    return c


# ---------- 图 1：原文标题区 ----------
save(clip(0, (30, 102, 565, 200)), 1)

# ---------- 图 2：原文图 1a，衣服英文模糊 ----------
a = clip(2, (169, 525, 452, 683), 300)
s = a.width / 590; box = tuple(int(v * s) for v in (430, 245, 520, 330))
a.paste(a.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
save(a, 2)

# ---------- 图 3：原文图 1b，去掉超声仪英文界面，标注中文 ----------
b = clip(3, (166, 94, 466, 304), 300); s = b.width / 628; T = 82
b = b.crop((0, int(T * s), b.width, int(405 * s))); dr = ImageDraw.Draw(b)
for x0, y0, x1, y1 in [(76, 226, 152, 274), (396, 274, 462, 308), (78, 372, 112, 408), (388, 372, 422, 408)]:
    dr.rectangle([int(x0 * s), int((y0 - T) * s), int(x1 * s), int((y1 - T) * s)], fill=(18, 18, 22))
f = font(int(20 * s))
dr.text((int(70 * s), int((230 - T) * s)), '腹横肌', font=f, fill='white'); dr.text((int(388 * s), int((278 - T) * s)), '腹横肌', font=f, fill='white')
tag(dr, int(76 * s), int((372 - T) * s), '静息', (30, 90, 160), int(20 * s)); tag(dr, int(386 * s), int((372 - T) * s), '收缩', (190, 40, 50), int(20 * s))
save(b, 3)

# ---------- 图 4、5：原文图 2 运动控制测试 ----------
T = [((128, 130), '① 服务员鞠躬', '正确：屈髋 50°～70° 时腰椎不屈曲；错误：腰椎过早屈曲'),
     ((131, 132), '② 骨盆后倾', '正确：胸椎中立，腰椎轻微屈曲；错误：骨盆不后倾，腰椎反而后伸'),
     ((133, 134), '③ 屈膝仰卧位（屈膝外倒）', '正确：右腿外倒时骨盆和脊柱不动；错误：骨盆和脊柱被带着旋转'),
     ((135, 136), '④ 四点跪位（控制屈曲）', '骨盆向后坐。正确：屈髋到 120° 腰椎不动；错误：未到 120° 腰椎就屈曲'),
     ((137, 129), '⑤ 四点跪位（控制伸展）', '骨盆向前移。正确：屈髋 60° 腰椎不动；错误：未到 60° 腰椎就伸展'),
     ((171, 172), '⑥ 俯卧主动屈膝', '正确：屈膝 90° 骨盆和腰椎不动；错误：腰椎伸展或屈曲'),
     ((173, 174), '⑦ 坐位伸膝', '正确：伸膝 30°～50° 腰椎不屈曲；错误：未到 30° 腰椎就屈曲')]
rows = [(n, t, [raw(x) for x in xs], ['正确', '错误']) for xs, n, t in T]
save(board('7 项腰椎运动控制测试（一）', rows[:4], H=330), 4)
save(board('7 项腰椎运动控制测试（二）', rows[4:], H=330), 5)

# ---------- 图 6：腹横肌激活 6 级（自绘） ----------
W, H = 1500, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
ctext(dr, W / 2, 24, '用压力生物反馈仪评估腹横肌：6 个等级', font(42))
ctext(dr, W / 2, 86, '屈膝仰卧，气囊放腰下充气到 40 mmHg；收缩腹横肌时压力变化保持在 2～4 mmHg、坚持 10 秒才算合格', font(26), GREY)
L = [('1 级', '收缩 1 次，坚持 10 秒'), ('2 级', '收缩 3 次，每次 10 秒'), ('3 级', '收缩 10 次，每次 10 秒'),
     ('4 级', '保持收缩，每侧屈膝外倒 5 次'), ('5 级', '保持收缩，每侧屈膝抬腿 5 次'), ('6 级', '保持收缩，每侧滑腿伸膝再屈回 5 次')]
for i, (lv, t) in enumerate(L):
    x0 = 80 + i * 40; y0 = 160 + i * 128; w = 900
    col = tuple(int(c) for c in (220 - i * 28, 236 - i * 18, 246 - i * 6))
    dr.rounded_rectangle([x0, y0, x0 + w + 300 - i * 80, y0 + 104], 16, fill=col)
    dr.text((x0 + 26, y0 + 28), lv, font=font(40), fill=INK if i < 4 else 'white')
    dr.text((x0 + 170, y0 + 32), t, font=font(34), fill=INK if i < 4 else 'white')
ctext(dr, W / 2, 940, '能轻松完成规定次数的最高一级，就是这个人的等级', font(28), GREY)
save(im, 6)

# ---------- 图 7～11：附录 A 训练动作 ----------
def pr(a_, b_): return [raw(a_), raw(b_)]


save(board('热身（每个 3 组 × 10 次）', [
    ('① 骨盆后倾', '屈膝仰卧，做骨盆后倾', pr(292, 293), ['起始', '结束']),
    ('② 抱膝到胸', '屈膝仰卧，双手轮流抱一侧膝拉向胸口', pr(460, 461), ['起始', '结束']),
    ('③ 双膝左右倒', '屈膝仰卧，双膝并拢一起向左、向右倒', pr(462, 463), ['起始', '结束']),
    ('④ 下肢延长', '仰卧伸腿，从骨盆开始轮流“拉长”一侧腿', pr(464, 465), ['起始', '结束']),
    ('⑤ 俯卧抬上身', '俯卧，双手在腰后相扣，上身和头稍离开床面', pr(466, 467), ['起始', '结束']),
    ('⑥ 猫骆驼', '四点跪，手在肩下、膝在髋下，交替拱背和塌腰', pr(515, 516) + pr(669, 670), ['', '', '', ''])], H=260), 7)
save(board('主训练 · 屈膝仰卧位（第 1～2 周）', [
    ('① 静态收缩', '屈膝仰卧，收紧下腹，把肚脐往脊柱方向收', pr(671, 672), ['起始', '结束']),
    ('② 屈膝外倒（控制旋转）', '保持收缩，一侧腿向外倒再回来，倒到骨盆还能控制住为止', pr(673, 674), ['起始', '结束']),
    ('③ 屈膝抬腿（控制屈曲）', '保持收缩，一侧腿慢慢抬离床面再放回', pr(675, 676), ['起始', '结束']),
    ('④ 滑腿伸膝（控制伸展）', '保持收缩，脚跟贴着床面把腿滑出去再滑回，不要完全伸直', pr(709, 710), ['起始', '结束'])], H=260), 8)
save(board('主训练 · 俯卧与四点跪位', [
    ('⑤ 俯卧屈膝（控制伸展/旋转）', '保持收缩，两侧轮流屈膝到 90°', pr(834, 835), ['起始', '结束']),
    ('⑥ 四点跪前移（控制屈曲）', '手略低于肩、膝略低于髋，躯干向前越过双手，腰保持平', pr(836, 837), ['起始', '结束']),
    ('⑦ 四点跪后坐（控制伸展）', '躯干向后往腿的方向移，腰保持平', pr(838, 839), ['起始', '结束'])], H=280), 9)
save(board('主训练 · 坐位与站立位（负重）', [
    ('⑧ 坐位伸膝', '坐直、双手放身体两侧，保持收缩慢慢伸膝（不要完全伸直）', pr(906, 907), ['起始', '结束']),
    ('⑨ 坐位屈髋', '坐直，保持收缩和姿势，抬起一侧大腿', pr(908, 909), ['起始', '结束']),
    ('⑩ 靠墙骨盆后倾', '背靠墙站，膝稍屈、脚离墙一点，保持收缩做骨盆后倾', pr(949, 950), ['起始', '结束']),
    ('⑪ 站立鞠躬', '保持收缩，从髋部向前屈、腰保持平，可用手扶', pr(1103, 1104), ['起始', '结束'])], H=280), 10)
save(board('放松拉伸（每个 60 秒）', [
    ('① 抱膝拉伸（下背）', '仰卧，抱一侧膝拉向胸口并保持', pr(1105, 1106), ['起始', '结束']),
    ('② 仰卧扭转（下背侧方）', '仰卧，一侧腿屈膝倒向对侧床面，头转向另一侧', pr(1107, 1108), ['起始', '结束']),
    ('③ 梨状肌拉伸', '屈膝仰卧，一腿搭在另一腿上，双手抱住下面那条腿拉向胸口', pr(1109, 1110), ['起始', '结束']),
    ('④ 腘绳肌拉伸', '仰卧，用弹力带把伸直的腿往上拉到大腿后侧有牵拉感，保持', pr(1167, 1168), ['起始', '结束'])], H=260, color=GREEN), 11)

# ---------- 图 12：原文图 3 流程 ----------
W, H = 1300, 1150; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
BL = (215, 225, 245)


def bx(x0, y0, x1, y1, lines, fs=30):
    dr.rounded_rectangle([x0, y0, x1, y1], 18, fill=BL, outline=(110, 130, 190), width=3)
    yy = (y0 + y1 - len(lines) * (fs + 12)) / 2 + 4
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs)); yy += fs + 12


def ar(x0, y0, x1, y1):
    dr.line([x0, y0, x1, y1], fill=(90, 110, 170), width=4)
    if x0 == x1: dr.polygon([(x1, y1 + 2), (x1 - 11, y1 - 18), (x1 + 11, y1 - 18)], fill=(90, 110, 170))
    else: dr.polygon([(x1 + 2, y1), (x1 - 18, y1 - 11), (x1 - 18, y1 + 11)], fill=(90, 110, 170))


bx(150, 30, 650, 130, ['初筛', '27 人'])
bx(820, 120, 1250, 300, ['排除 4 人', '年龄 ＞60 岁 2 人', '系统性疾病 2 人'])
ar(400, 130, 400, 238); ar(400, 210, 818, 210)
bx(150, 240, 650, 340, ['入组并随机分为 2 组', '23 人'])
dr.line([400, 340, 400, 380], fill=(90, 110, 170), width=4); dr.line([220, 380, 600, 380], fill=(90, 110, 170), width=4)
ar(220, 380, 220, 428); ar(600, 380, 600, 428)
bx(60, 430, 380, 560, ['超声引导组', '（试验组）12 人'])
bx(440, 430, 760, 560, ['触觉反馈组', '（对照组）11 人'])
ar(600, 560, 600, 718); ar(220, 560, 220, 718); ar(780, 620, 958, 620)
bx(960, 570, 1250, 670, ['干预前评估'])
bx(40, 720, 400, 900, ['每周 2 次，共 7 周', '运动控制训练', '+ 超声反馈（12 人）'], 28)
bx(420, 720, 780, 900, ['每周 2 次，共 7 周', '运动控制训练', '+ 触觉反馈（11 人）'], 28)
dr.line([220, 900, 220, 950], fill=(90, 110, 170), width=4); dr.line([600, 900, 600, 950], fill=(90, 110, 170), width=4)
dr.line([220, 950, 600, 950], fill=(90, 110, 170), width=4); ar(410, 950, 410, 1028); ar(410, 970, 958, 970)
bx(960, 920, 1250, 1020, ['干预后评估'])
bx(150, 1030, 670, 1120, ['数据分析（23 人）'])
save(im, 12)

# ---------- 封面 ----------
cv = Image.new('RGB', (900, 383), 'white'); dr = ImageDraw.Draw(cv)
m = a.copy(); m = m.resize((round(m.width * 383 / m.height), 383), Image.LANCZOS)
cv.paste(m.crop((m.width - 440, 0, m.width, 383)), (460, 0))
dr.text((32, 50), '练腹横肌', font=font(70), fill=INK)
dr.text((32, 150), '看超声屏幕', font=font(52), fill=BLUE)
dr.text((32, 220), '比用手摸更有效吗？', font=font(40), fill=RED)
dr.text((32, 320), 'Healthcare 2023 · 随机对照预试验', font=font(22), fill=GREY)
cv.save(f'{OUT}/cover.jpg', quality=92)
