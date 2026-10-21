#!/usr/bin/env python3
"""Stone 等 2018 赛季中投掷肩损伤非手术治疗：首图为原题直译标题卡；四阶段卡、间歇投掷卡、客观标准卡为编者根据原文表 1～6 和附录 A 整理；
原文图 1～3 直接使用（原文已遮挡面部）并加中文说明。
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


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * (len(tiles) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def pair(a, b, ca, cb, W=1200):
    """两张照片左右并排，各自上方加说明"""
    w = (W - 14) // 2
    ta, tb = capbox(a, ca, w), capbox(b, cb, w)
    h = max(ta.height, tb.height); out = Image.new('RGB', (W, h), 'white')
    out.paste(ta, (0, 0)); out.paste(tb, (w + 14, 0)); return out


F1, F2, F3 = raw(21), raw(25), raw(26)


def phases(title, S, n, fs=24):
    W = 1200; im = Image.new('RGB', (W, 2400), 'white'); dr = ImageDraw.Draw(im); y = 20
    for t, bg, c, items in S:
        h = 66 + sum(para_h(s, fs, 1040, gap=8) + 10 for s in items)
        dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
        yy = y + 62
        for s in items: yy = bullet(dr, 70, yy, s, fs, 1060, gap=8) + 10
        y += h + 16
    save(titled(im.crop((0, 0, W, y)), title), n)


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '临床评论 · IJSPT 2018', font=font(32), fill=TEAL)
for i, t in enumerate(['赛季中投掷肩损伤的非手术治疗：', '当前概念综述与临床评论']):
    dr.text((70, 130 + i * 72), t, font=font(52), fill=INK)
line, y = '', 300
for w in 'Nonoperative Treatment for Injuries to the In-Season Throwing Shoulder: A Current Concepts Review with Clinical Commentary'.split():
    if dr.textlength(line + ' ' + w, font=font(26)) > W - 140: dr.text((70, y), line, font=font(26), fill=GREY); y += 36; line = w
    else: line = (line + ' ' + w).strip()
dr.text((70, y), line, font=font(26), fill=GREY)
dr.line([70, 430, W - 70, 430], fill=(200, 205, 210), width=2)
dr.text((70, 460), 'Stone MA, Jalali O, Alluri RK, et al. Int J Sports Phys Ther 2018;13(2):306-320', font=font(30), fill=GREY)
dr.text((70, 515), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

phases('四个阶段一览（编者根据原文表 1～5 整理）', [
    ('阶段 1　急性期（受伤后立即开始）', LT, TEAL, ['目标：控制炎症疼痛、评估并纠正活动度缺陷、延缓肌萎缩、恢复本体感觉、开始动力链训练',
        '做法：非甾体抗炎药 / 激素注射、冰敷、激光、离子导入；助力和被动活动度、手法牵伸（交叉内收、睡姿牵伸）；纠正姿势、胸小肌牵伸、软组织松动；肩等长收缩；节律性稳定 ± PNF；腰盆等长训练']),
    ('阶段 2　中期（疼痛炎症消退、神经肌肉控制和静态稳定够了）', OR, (180, 90, 20), ['目标：重建盂肱和肩胸肌群平衡；继续活动度、柔韧和神经肌肉控制；加强动力链并开始体能训练',
        '做法：投手 10 项（俯卧划船到外旋、侧卧外旋、满罐）；低位划船、割草机、“抢劫”式；仰卧前伸、靠墙俯卧撑练前锯肌；侧卧外旋、俯卧前屈、俯卧水平外展加外旋、俯卧后伸练中下斜方肌；末端稳定；腰盆等张训练']),
    ('阶段 3　进阶强化（活动度完全、肌力 ≥ 4/5、几乎不痛）', PU, (90, 60, 150), ['目标：积极强化、提升爆发力和耐力、开始专项功能训练、加强动力链和体能',
        '做法：进阶投手 10 项；增强式训练（胸前传球、头上足球式掷球、左右抛、侧抛）、靠墙拍球、靠墙画圈、轻球 / 重球投掷；最大外旋位徒手抗阻和节律性稳定加扰动；功能性腰盆强化']),
    ('阶段 4　回归投掷（查体满意、无痛活动度、等速测试满意、增强式训练完成）', GR, (40, 120, 60), ['目标：恢复专项和位置要求',
        '做法：间歇投掷方案，第 1 阶段平地投掷，第 2 阶段投手上投手丘、野手练长距离'])], 2)

save(titled(capbox(F1, 'A 站立交叉内收牵伸（借助 Rotater 工具）；B 改良睡姿牵伸：没有工具或交叉内收牵伸引起疼痛时用。可做主动、被动或肌肉能量技术，可配合关节松动'),
            '原文图 1　纠正内旋缺陷和后关节囊挛缩'), 3)
save(titled(capbox(F2, '患者仰卧、手臂垂在床边，治疗师向后下方推压肩前方，帮助牵伸胸小肌；也可以自己做单侧墙角牵伸'),
            '原文图 2　治疗师辅助牵伸胸小肌'), 4)
save(titled(capbox(F3, 'A、B 俯卧：治疗师左手把肩胛骨抬离胸壁，右手松动、牵伸肩胛骨下方的肌肉附着；C 侧卧：左手把喙突向后推、让肩胛骨离开胸壁，右手牵拉肩胛骨下角'),
            '原文图 3　肩胛胸壁软组织松动'), 5)

phases('间歇投掷方案（编者根据原文表 6 整理）', [
    ('第 1 阶段　平地投掷（长传）', LT, TEAL, ['第 1 天：最多 25 次，距离 20～45 英尺（约 6～14 米）', '长传距离逐步增加：45 → 60 → 90 → 120 英尺（约 14 → 18 → 27 → 37 米）；投手目标 150 英尺（约 46 米）', '平直出手，不要高抛；用四缝线直球握法；早期用次最大力量']),
    ('第 2 阶段（投手）　上投手丘', OR, (180, 90, 20), ['从 45 英尺开始，直球 50% 最大球速，逐步增加球数和距离', '球速调到 75%～100%；直球和变速球都能投之后，才加入变化球']),
    ('第 2 阶段（野手）　长距离投掷', PU, (90, 60, 150), ['先练动作，再练准确性', '距离 120 → 150 → 180 英尺（约 37 → 46 → 55 米）']),
    ('休息日', GR, (40, 120, 60), ['做强度和难度类似阶段 2 的练习；保持肩部放松、减少酸痛；10 分钟轻松传球']),
    ('通用规则', (240, 240, 240), INK, ['隔天投一次；连续 3 个投掷日顺利完成再进到下一级', '投掷时出现明显疼痛或肩部深处痛，当天全部停止，改天重新评估', '强调“收步”（gathering step），有意识地用下肢和躯干发力'])], 6)

phases('客观标准参考（编者根据原文附录 A 整理）', [
    ('盂肱关节活动度', LT, TEAL, ['投掷侧内旋缺陷 < 18°（最大保护）；文献中 18°～25° 都有，没有共识']),
    ('肩袖力量', OR, (180, 90, 20), ['等速外旋 / 内旋比 66%，或等长外旋 / 内旋比 75%～100%', '投掷侧肩袖整体力量比非投掷侧高 10%', '外旋离心力量等于内旋等长力量']),
    ('肩胛骨位置和力量', PU, (90, 60, 150), ['手臂完全上举时肩胛骨上回旋 60°', '单手运动项目中，优势侧肩胛周围肌力量高 10%']),
    ('胸小肌长度', GR, (40, 120, 60), ['胸小肌指数（静息长度 ÷ 身高 × 100）> 7.65']),
    ('回归比赛三步走（Matheson 模型）', PK, RED, ['① 评估健康状态（分析性和功能性测试）', '② 考虑运动风险修正因素（项目、位置、竞技水平）', '③ 考虑外部修正因素（社会、经济压力、赛季时间）'])], 7)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), '投掷肩 · 赛季中非手术康复', font=font(40), fill=TEAL)
dr.text((50, 130), '赛季中肩伤了，', font=font(62), fill=INK)
dr.text((50, 220), '不开刀怎么回场？', font=font(62), fill=INK)
dr.text((50, 318), '四阶段康复 · 间歇投掷 · 回归标准', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
