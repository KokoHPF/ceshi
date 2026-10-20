#!/usr/bin/env python3
"""Flore 等 2024 职业足球外侧踝扭伤康复流程：首图中文标题卡；原文图 1 康复流程、图 2 伤后金字塔中文重绘；
“三道关”方法卡、AFS 门槛台阶图、功能测试进阶图为编者根据原文绘制；原文图 1 原图附加中文说明放在附录。
原文图片里没有球员、人脸或联系方式，无需模糊。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
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


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


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


def arrow_down(dr, cx, y0, y1, c=TEAL):
    dr.line([cx, y0, cx, y1 - 14], fill=c, width=6)
    dr.polygon([(cx - 16, y1 - 18), (cx + 16, y1 - 18), (cx, y1)], fill=c)


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床述评 · 《国际运动物理治疗杂志》2024', font=font(32), fill=TEAL)
for i, t in enumerate(['职业球员崴脚后，', '什么时候能进下一级？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '外侧踝扭伤四级康复流程：问卷 + 体格检查 + 功能测试三道关', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Flore Z, Hambly K, De Coninck K, Welsch G. IJSPT 2024;19(7):910-922', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 2 伤后金字塔重绘
W = 1200; im = Image.new('RGB', (W, 900), 'white'); dr = ImageDraw.Draw(im)
lv = [('RTC 重返比赛', '全面参与训练和比赛', '标准：德国职业体育保险（VBG）测试组合；作者认为缺证据', PK),
      ('RTP 回归团队', '部分团队热身、部分团队训练，不做铲抢', '标准：缺乏，靠经验和主观判断', OR),
      ('RTS 专项训练', '球：盘带、传球、传中、射门；速度：加跑量、直线冲刺、变向冲刺；灵敏：跑动路线、T 测试、伊利诺伊测试', '进入标准：AFS > 95 + 体格检查 + 测试组合通过', GR),
      ('RTA 康复流程', '被动治疗 → 主动治疗 → 第 1 级本体感觉 → 第 2 级跑步 → 第 3 级跳跃 → 第 4 级跳跃和运动技能', '每升一级都要过三道关（见下图）', LT)]
y = 20; cx = 220
for i, (h, t, s, bg) in enumerate(lv):
    hh = 200
    half = 70 + i * 45
    dr.polygon([(cx - half, y + hh), (cx + half, y + hh), (cx + half - 45, y), (cx - half + 45, y)] if i else
               [(cx - half, y + hh), (cx + half, y + hh), (cx, y)], fill=bg, outline=(170, 170, 170))
    ctext(dr, cx, y + hh / 2 - 22, h.split(' ')[0], font(40), TEAL)
    dr.rounded_rectangle([420, y + 8, W - 20, y + hh - 8], 12, fill=bg)
    dr.text((444, y + 22), h, font=font(32), fill=TEAL)
    yy = para(dr, 444, y + 66, t, 25, W - 490, fill=INK, gap=8)
    para(dr, 444, yy + 4, s, 23, W - 490, fill=RED, gap=8)
    y += hh + 12
dr.text((20, y + 4), '越往上越接近比赛；本文的四级流程只覆盖最底层 RTA', font=font(26), fill=GREY)
save(titled(im, '原文图 2 重绘：伤后金字塔，从康复到重返比赛'), 2)

# 三道关方法卡
W = 1200; gates = [
    ('① 问卷：踝关节功能评分（AFS）', ['5 项：疼痛、不稳、负重、肿胀、步态，满分 100',
                                    '每一级设门槛：40 → 60 → 75 → 85 → 95', '门槛是作者按经验定的，文献只作参考'], LT),
    ('② 标准化体格检查', ['前抽屉、距骨倾斜试验查韧带松弛，伤后第 5 天起较准，用“+”号分级跟踪',
                        '徒手肌力测试，重点腓骨肌（第 1 级 4/5，第 2 级 5/5）',
                        '活动度：前两级背伸差 < 10°，之后要和健侧一样', '围度：比上一次测量增加不超过 1%'], OR),
    ('③ 功能测试', ['平衡 → 提踵、跑步分析 → 单腿跳，按愈合阶段从易到难',
                   '高动态跳跃先看动作质量和疼痛，再测成绩', '成绩用肢体对称指数（LSI）判定：患侧 > 健侧 90%'], GR)]
hs = [70 + sum(para_h(x, 27, W - 140) for x in it) + 16 for _, it, _ in gates]
im = Image.new('RGB', (W, sum(hs) + 14 * 3 + 80), 'white'); dr = ImageDraw.Draw(im); y = 10
for (h, it, bg), hh in zip(gates, hs):
    dr.rounded_rectangle([20, y, W - 20, y + hh], 14, fill=bg)
    dr.text((44, y + 16), h, font=font(32), fill=TEAL); yy = y + 66
    for x in it:
        yy = bullet(dr, 44, yy, x, 27, W - 110)
    y += hh + 14
para(dr, 30, y + 6, '三关全过才能进下一级；任一关没过，就留在当前级别继续练', 28, W - 60, fill=RED)
save(titled(im, '升级要过三道关（编者根据原文整理）'), 3)

# 原文图 1 中文重绘：四级流程
W = 1200
steps = [
    ('入口', '物理治疗之后', ['AFS > 40', '单腿站 30 秒', '走路不痛', '没有炎症迹象'], None, (240, 240, 240)),
    ('第 1 级', '本体感觉', ['徒手肌力 4/5（激活）+ 体格检查', '改良 Stork 平衡（静态）', 'Y 平衡测试（动态）'],
     '固定自行车、本体感觉进阶、扰动训练、闭链力量、水中训练/椭圆机、减重跑台', LT),
    ('第 2 级', '跑步', ['AFS ≥ 60（或比上次 +10%）', '徒手肌力 5/5 + 体格检查', '提踵测试、跑步分析（定性）'],
     '慢速有氧跑，为跳跃做准备', OR),
    ('第 3 级', '跳跃能力', ['AFS ≥ 75（或 +10%）', '体格检查', '侧向跳（额状面）、三级跳远（矢状面），先定性再定量'],
     '加跑量、间歇跑、跑步 ABC、急停急起；绳梯等短促反应性冲击，额状面、矢状面冲击', GR),
    ('第 4 级', '跳跃和运动技能', ['AFS ≥ 85（或 +5%）', '体格检查', '方形跳、交叉跳远、6 米交叉计时跳'],
     '直线冲刺、变向切入，T 测试、伊利诺伊测试当练习做', PK),
    ('RTS', '足球专项', ['AFS > 95', '体格检查', '测试组合通过'], None, PU)]
blocks = []
for name, aim, test, train, bg in steps:
    lh = 18 + sum(para_h(t, 25, 560 - 28) for t in test)
    rh = 18 + (para_h(train, 25, 440) + 40 if train else 0)
    blocks.append(max(lh, rh) + 64)
im = Image.new('RGB', (W, sum(blocks) + 46 * (len(steps) - 1) + 120), 'white'); dr = ImageDraw.Draw(im)
dr.text((40, 14), '先过这一关的测试 ↓', font=font(26), fill=GREY); dr.text((660, 14), '过了之后练什么', font=font(26), fill=GREY)
y = 56
for (name, aim, test, train, bg), hh in zip(steps, blocks):
    dr.rounded_rectangle([20, y, W - 20, y + hh], 14, fill=bg)
    dr.text((40, y + 14), name, font=font(34), fill=TEAL); dr.text((40 + dr.textlength(name, font=font(34)) + 18, y + 20), aim, font=font(28), fill=INK)
    yy = y + 66
    for t in test: yy = bullet(dr, 40, yy, t, 25, 560, gap=8)
    if train:
        dr.line([640, y + 66, 640, y + hh - 16], fill=(200, 200, 200), width=2)
        para(dr, 660, y + 66, train, 25, W - 700, fill=GREY, gap=8)
    y += hh
    if name != 'RTS': arrow_down(dr, W // 2, y + 4, y + 42)
    y += 46
dr.text((40, y - 30), '任一项没过：回到当前级别继续练，下次再测', font=font(26), fill=RED)
save(titled(im, '原文图 1 重绘：外侧踝扭伤四级康复流程'), 4)

# AFS 门槛台阶
fig, ax = plt.subplots(figsize=(12, 6.6), dpi=110)
labs = ['进入第 1 级', '进入第 2 级', '进入第 3 级', '进入第 4 级', '进入 RTS']
vals = [40, 60, 75, 85, 95]
cols = ['#4c8fbf', '#f39a2b', '#5aa469', '#d1495b', '#7a4fd6']
bars = ax.bar(labs, vals, color=cols, width=0.62)
for bb, v in zip(bars, vals):
    ax.text(bb.get_x() + bb.get_width() / 2, v + 2, f'{v}', ha='center', fontsize=20, fontweight='bold')
alt = ['', '或比上次 +10%', '或 +10%', '或 +5%', '']
for bb, a in zip(bars, alt):
    if a: ax.text(bb.get_x() + bb.get_width() / 2, 8, a, ha='center', fontsize=13, color='white')
ax.set_ylim(0, 108); ax.set_ylabel('踝关节功能评分（AFS，满分 100）', fontsize=15); ax.tick_params(labelsize=14)
ax.spines[['top', 'right']].set_visible(False)
fig.text(0.5, 0.01, '数值取自原文正文和表 1；“或比上次提高”只出现在原文图 1，正文和表 1 没有', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.04, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), 'AFS 门槛：每升一级，问卷分数要更高', 1200), 5)

# 功能测试进阶
W = 1200; seq = [('第 1 级', '静态 + 动态平衡', '改良 Stork 平衡测试、Y 平衡测试', '低冲击，不给外侧韧带施加冲击力', LT),
                 ('第 2 级', '小腿耐力 + 跑步', '提踵测试、跑步分析（定性）', '从闭链负重过渡到跑步', OR),
                 ('第 3 级', '单一平面跳', '侧向跳（额状面）→ 三级跳远（矢状面）', '先看动作和疼痛，再测成绩', GR),
                 ('第 4 级', '多方向跳', '方形跳（控制最多）→ 交叉跳远（控制减少）→ 6 米交叉计时跳（加时间压力）', '对称指数 > 90% 才算过', PK)]
hs = [70 + para_h(t, 27, W - 330) + para_h(n, 24, W - 330) for _, _, t, n, _ in seq]
im = Image.new('RGB', (W, sum(hs) + 14 * 4 + 10), 'white'); dr = ImageDraw.Draw(im); y = 10
for (lvn, h, t, n, bg), hh in zip(seq, hs):
    dr.rounded_rectangle([20, y, W - 20, y + hh], 14, fill=bg)
    dr.text((44, y + 18), lvn, font=font(32), fill=TEAL); dr.text((44, y + 64), h, font=font(24), fill=GREY)
    yy = para(dr, 290, y + 20, t, 27, W - 330); para(dr, 290, yy + 4, n, 24, W - 330, fill=RED)
    y += hh + 14
save(titled(im, '功能测试怎么一级级加难（编者根据原文整理）'), 6)

# 原文图 1 原图（附录）
save(capbox(raw(64), '原文图 1 原图：康复流程（© Zacharias Flore 2017，CC BY-NC 4.0）。左侧为每级测试，右侧为过关后的训练内容，“no”表示没过、回到原级'), 7)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), '职业足球 · 外侧踝扭伤', font=font(40), fill=TEAL)
dr.text((50, 130), '崴脚后康复', font=font(64), fill=INK)
dr.text((50, 220), '凭什么升级？', font=font(64), fill=INK)
dr.text((50, 318), '问卷 + 体检 + 功能测试 · 四级流程', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
