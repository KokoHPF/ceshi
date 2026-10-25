#!/usr/bin/env python3
"""Abioke 等 2025《老年面瘫的物理治疗管理：病例报告》（Cureus）推文配图。
首图中文标题卡、病例时间线与初评卡、原文图 1～7（治疗照片和治疗前后对比照，图内没有英文，只加中文图注；
患者眼部遮挡沿用原文作者的处理，编者未改动人物画面）、按原文表 2 重绘的结局指标对比图、临床要点卡、封面。
封面只用文字，不放患者照片。
用法：python3 make_figs.py <src 目录> <输出目录> <中文字体>"""
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)


def raw(name):
    return Image.open(f'{SRC}/{name}').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        # 标点不放行首
        # 数字和小数点不拆开
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”' and not (line[-1:] in '0123456789.' and ch in '0123456789.%'):
            dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t


def card(W, title, blocks):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 6000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 6000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


def outcome_chart():
    """原文表 2：三个量表治疗前后（House-Brackmann 越低越好，另外两个越高越好）"""
    W = 1200; im = Image.new('RGB', (W, 1000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '8 周物理治疗前后的结局指标（原文表 2）', font=font(36), fill='white')
    PRE, POST = (170, 170, 170), TEAL
    x0 = 30
    for c, t in ((PRE, '治疗前（2024-11-24）'), (POST, '治疗后（2025-02-09 随访）')):
        dr.rectangle([x0, 106, x0 + 26, 132], fill=c); dr.text((x0 + 36, 102), t, font=font(26), fill=INK); x0 += 420
    # 左：两个 0～100 的量表
    L, R, top, bot = 120, 700, 190, 640
    Y = lambda v: bot - (bot - top) * v / 100
    for v in (0, 20, 40, 60, 80, 100):
        dr.line([L, Y(v), R, Y(v)], fill=(230, 230, 230), width=1)
        dr.text((L - 12, Y(v)), str(v), font=font(22), fill=GREY, anchor='rm')
    for i, (name, a, b, note) in enumerate((('Sunnybrook 面神经分级', 25, 60, '+35（MCID 约 13 分）'), ('面部残疾指数 FDI', 40, 70, '+30'))):
        cx = L + 150 + i * 290
        for j, (v, c) in enumerate(((a, PRE), (b, POST))):
            x = cx - 70 + j * 76
            dr.rectangle([x, Y(v), x + 64, bot], fill=c)
            dr.text((x + 32, Y(v) - 8), str(v), font=font(26), fill=c, anchor='md')
        dr.text((cx, bot + 16), name, font=font(24), fill=INK, anchor='ma')
        dr.text((cx, bot + 50), note, font=font(22), fill=RED, anchor='ma')
    dr.text((L - 12, top - 40), '分（越高越好）', font=font(22), fill=GREY)
    # 右：House-Brackmann 分级
    hx = 780
    dr.text((hx, top - 40), 'House-Brackmann（I 正常～VI 完全瘫痪）', font=font(22), fill=GREY)
    grades = ['I', 'II', 'III', 'IV', 'V', 'VI']
    for k, g in enumerate(grades):
        y = top + 10 + k * 70
        c = POST if g == 'III' else PRE if g == 'IV' else (240, 240, 240)
        dr.rounded_rectangle([hx, y, hx + 120, y + 56], 8, fill=c)
        dr.text((hx + 60, y + 28), g, font=font(28), fill='white' if g in ('III', 'IV') else GREY, anchor='mm')
        if g == 'IV': dr.text((hx + 140, y + 28), '治疗前：中重度', font=font(24), fill=INK, anchor='lm')
        if g == 'III': dr.text((hx + 140, y + 28), '治疗后：中度', font=font(24), fill=TEAL, anchor='lm')
    dr.line([hx + 130, top + 10 + 3 * 70 + 10, hx + 130, top + 10 + 2 * 70 + 46], fill=RED, width=4)
    y = bot + 110
    y = para(dr, 30, y, '耳屏到口角的软尺测量：健侧（右）治疗前后都是 12.0 cm，患侧（左）12.5 → 12.0 cm。'
             '注意：原文病例部分写的是左 12 cm、右 11 cm，和表 2 对不上。', 24, W - 60, fill=GREY)
    y = para(dr, 30, y + 6, '单个病例、没有对照组，治疗开始时已发病 5 个月，改善不能全部归因于物理治疗。', 24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 10))


# 1 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '病例报告 · 《Cureus》2025', font=font(30), fill=TEAL)
dr.text((70, 135), '老年面瘫（贝尔麻痹）', font=font(56), fill=INK)
dr.text((70, 210), '的物理治疗管理', font=font(44), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Abioke UB, Anosike W, Olaniyi AO, Okwuowulu IL, Mandal M, Eze CY.', font=font(26), fill=GREY)
dr.text((70, 390), 'Cureus. 2025;17(7):e88045. doi:10.7759/cureus.88045', font=font(26), fill=GREY)
dr.text((70, 435), '尼日利亚贝宁大学物理治疗系 · 英国斯托克波特 NHS 基金会信托等', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作学术交流 · 原文 CC BY 4.0', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, '病例概况（编者根据原文整理）', [
    ('谁', '75 岁男性，左侧周围性面瘫；合并高血压、糖尿病、消化性溃疡\n症状：流口水、说话含糊、用杯子喝水会漏，嘴角被拉向右侧', LT, TEAL),
    ('时间线', '2024-06-18 发病 → 先用糖皮质激素 → 2024-11-24 才转到物理治疗门诊（已发病约 5 个月）→ 2025-02-09 随访', OR, (200, 120, 0)),
    ('初评', '左侧鼻唇沟消失、口角下垂、额纹消失、闭眼不全，Bell 征阳性\nHouse-Brackmann IV 级，Sunnybrook 25 分，面部残疾指数（FDI）40%\n左侧张力低、右侧轻度张力高', PK, RED),
    ('排除', '无疱疹、耳部水疱 → 排除 Ramsay Hunt 综合征；无其他神经症状 → 排除卒中\n（鉴别里还列了莱姆病、吉兰-巴雷综合征，但原文没写怎么排除）', GR, (0, 120, 60)),
]), 2)

save(capbox(raw('fig1.jpg'), '原文图 1  Kabat 技术，从上部支点（额肌）开始：治疗师在健侧施加阻力，借对角、旋转的 PNF 模式诱发患侧的动作和肌肉激活'), 3)
save(capbox(raw('fig2.jpg'), '原文图 2  电刺激眼轮匝肌和口轮匝肌（NMES）：频率 1～10 Hz、强度 2～5 mA、脉宽 150 µs、通 5 秒断 15 秒、每次 15 分钟'), 4)
save(capbox(raw('fig3.jpg'), '原文图 3  触觉刺激和面部按摩（提捏手法），涂爽身粉减少摩擦，用来增加感觉输入、改善局部循环'), 5)
save(capbox(raw('fig4.jpg'), '原文图 4  面部 PNF：结合对角和旋转方向的动作，诱发协调的肌肉活动、恢复功能性动作模式'), 6)
save(capbox(raw('fig5.jpg'), '原文图 5  肌内效贴：额肌从眉毛向发际线纵向贴，眼轮匝肌绕眼一圈，口轮匝肌沿唇周贴；额部留一小段不粘，用来做改良抬眉练习'), 7)
save(capbox(raw('fig6.jpg'), '原文图 6  家庭训练之一：鼓腮吹气（像吹气球一样），练口轮匝肌、颊肌等口周肌肉'), 8)
save(capbox(raw('fig7.jpg'), '原文图 7  左：治疗前；右：治疗后。原文称鼻唇沟更明显、眉下垂减轻、面部更对称、能闭眼、联带运动减少（眼部遮挡为原文作者所加）'), 9)
save(outcome_chart(), 10)

save(card(1200, '落到临床（编者整理）', [
    ('这套组合拳包括什么', '每周 3 次、每次 45 分钟、共 8 周：Kabat/PNF、电刺激、按摩和触觉刺激、面部训练、镜像反馈、肌内效贴，外加家庭训练和护眼宣教', LT, TEAL),
    ('护眼和生活建议先做', '闭眼不全的患者白天戴护目镜、夜间贴眼防干燥；用吸管喝水避免漏；鼓励用患侧咀嚼', GR, (0, 120, 60)),
    ('评估要用量表', 'House-Brackmann 分级粗，Sunnybrook 能分开看静态对称、自主运动和联带运动，FDI 反映患者自己的功能和社交感受，建议治疗前后都测', OR, (200, 120, 0)),
    ('电刺激有争议', '面瘫用电刺激的证据并不统一，也有学者担心它可能加重联带运动；本病例没有单独评估联带运动，不能据此推荐常规使用（编者补充）', PK, RED),
    ('别把单个病例当疗效证据', '发病 5 个月才开始治疗、没有对照，自然恢复可能占了很大一部分；能借鉴的是做法和评估思路', PU, (110, 70, 190)),
]), 11)

# 封面：纯文字，不用患者照片
W, H = 900, 383; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, H], fill=TEAL)
dr.text((50, 46), '病例报告 · Cureus 2025', font=font(26), fill=TEAL)
dr.text((50, 118), '75 岁面瘫老人', font=font(58), fill=INK)
dr.text((50, 198), '8 周物理治疗', font=font(46), fill=INK)
dr.text((50, 290), 'Kabat · 电刺激 · 肌内效贴 · 面部训练', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
