#!/usr/bin/env python3
"""Terrell 等 2021 FAIS 非手术与术后治疗性运动：首图为原题直译标题卡；四大支柱卡、术后五阶段卡、进阶标准卡为编者整理；
原文图 1～7 直接使用并加中文说明。
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


F1, F2, F3, F4, F5, F6, F7 = (raw(x) for x in (5, 9, 16, 26, 30, 34, 38))

# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '当前临床概念 · J Athl Train 2021', font=font(32), fill=TEAL)
for i, t in enumerate(['股骨髋臼撞击综合征非手术与术后', '管理的治疗性运动方法']):
    dr.text((70, 130 + i * 72), t, font=font(52), fill=INK)
line, y = '', 300
for w in 'Therapeutic Exercise Approaches to Nonoperative and Postoperative Management of Femoroacetabular Impingement Syndrome'.split():
    if dr.textlength(line + ' ' + w, font=font(26)) > W - 140: dr.text((70, y), line, font=font(26), fill=GREY); y += 36; line = w
    else: line = (line + ' ' + w).strip()
dr.text((70, y), line, font=font(26), fill=GREY)
dr.line([70, 430, W - 70, 430], fill=(200, 205, 210), width=2)
dr.text((70, 460), 'Terrell SL, Olson GE, Lynch J. J Athl Train 2021;56(1):31-45', font=font(30), fill=GREY)
dr.text((70, 515), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(titled(capbox(F1, 'A 凸轮型（cam）：股骨头颈交界处不圆、凸起，屈髋内旋时挤进髋臼；B 钳夹型（pincer）：髋臼边缘过度覆盖股骨头。两种可以同时存在'),
            '原文图 1　股骨髋臼撞击的两种类型'), 2)
save(titled(capbox(F2, 'A～C 屈曲-内收-内旋（FADIR）试验；D、E 仰卧滚木试验；F “C”字征（手呈 C 形握在大转子上方）；G～I 动态内旋撞击试验；J～L 动态外旋撞击试验'),
            '原文图 2　常用临床检查'), 3)
save(titled(capbox(F3, '沿股骨颈轴线过股骨头中心画一条线；在股骨头上画最佳拟合圆，找出头颈交界处离开圆的点，从圆心连到这一点。两线夹角即 α 角，≥ 55° 最常用作凸轮畸形的判断标准'),
            '原文图 3　α 角怎么量'), 4)

# 四大支柱卡
W = 1200; im = Image.new('RGB', (W, 500), 'white'); dr = ImageDraw.Draw(im)
ctext(dr, 600, 20, '非手术和术后康复，练的是同样四件事', font(34), INK)
P = [('姿势控制', '骨盆中立、减少骨盆前倾', LT, TEAL), ('核心稳定', '腹横肌、多裂肌、膈肌、盆底协同', OR, (180, 90, 20)),
     ('髋部力量\n与运动控制', '臀肌为主，少让阔筋膜张肌代偿', PU, (90, 60, 150)), ('柔韧性\n与活动度', '无痛范围内恢复功能活动度', GR, (40, 120, 60))]
for i, (t, s, bg, c) in enumerate(P):
    x = 40 + i * 285
    dr.rounded_rectangle([x, 90, x + 265, 360], 14, fill=bg)
    yy = 115
    for ln in t.split('\n'):
        ctext(dr, x + 132, yy, ln, font(32), c); yy += 44
    para(dr, x + 22, 225, s, 25, 225, gap=8)
dr.rounded_rectangle([40, 385, 1160, 480], 14, fill=(240, 240, 240))
para(dr, 70, 413, '原则：练习时不诱发疼痛；按个人目标个体化；目标是恢复无痛活动、纠正功能缺陷', 26, 1060, gap=8)
save(titled(im, '四大运动支柱（编者根据原文整理）'), 5)

save(titled(capbox(F4, '骨盆前后倾：A 起始（吸气）、B 结束（呼气）、C 重复；猫牛式：D 猫、E 牛、F 中立；坐位：G 后倾、H 前倾、I 中立；站立：J 后倾、K 前倾、L 中立'),
            '原文图 4　姿势训练'), 6)
save(titled(capbox(F5, '鸟狗式：A 起始、B 抬起对侧手脚并保持、C 回到起始；平板：D 俯卧平板、E 加伸髋、F 侧平板；死虫式：G 起始、H 放下对侧手脚并保持、I 换边（可抱球）；半跪旋转：J 高位、K 中间、L 终点'),
            '原文图 5　核心训练'), 7)
save(titled(capbox(F6, '蚌式：A 起始、B 上方腿打开并保持、C 加伸膝；臀桥：D 起始、E 单腿伸直保持、F 一腿抱向胸口；弹力带侧向走：G 带子在跖骨、H 踝、I 膝上；J 台阶下落点地；K 弓步伸手；L 负重弓步伸手'),
            '原文图 6　髋部力量与运动控制'), 8)
save(titled(capbox(F7, '静态牵伸：A 髋旋转肌、B 屈髋肌、C 腘绳肌；自我筋膜放松：D 长曲棍球、E 泡沫轴；弹力带牵引：F 外侧、G 向后；动态旋转：H 关门、I 开门；动态练习：J、K 靠墙摆腿，L 踢腿行进'),
            '原文图 7　柔韧性与活动度'), 9)

# 术后五阶段卡
W = 1200; im = Image.new('RGB', (W, 1700), 'white'); dr = ImageDraw.Draw(im)
S = [('第 1 周（急性期）', LT, TEAL, ['控制肿痛、保护修复组织；拄拐，清理类可足平放部分负重，1 周后脱拐；盂唇修复、微骨折可能限制负重至 8 周', '无痛范围被动内外旋；臀肌、腘绳肌、股四头肌、腹横肌等长收缩；无阻力直立单车（屈髋 < 90°）', '达标：疼痛控制好，用助行器步态正确']),
     ('第 2～4 周', OR, (180, 90, 20), ['四点跪位前后摇、治疗师松动和长轴牵引；三个平面髋部等张训练（屈髋要小心）；核心稳定；伤口愈合后可下水', '前 3～4 周被动活动度限制：屈 90°、伸 0°、外展 25°～30°、屈髋 90° 位内旋 0°、外旋 30°，俯卧外旋 20°', '达标：3 周后在无痛范围内放开活动度；第 4 周完全负重']),
     ('第 5～8 周', PU, (90, 60, 150), ['每天下肢牵伸；开链 + 闭链、轻重量多次数练臀中肌和臀大肌', '不稳定平面、单腿侧向步、滑板、台阶下落练运动控制', '平板、臀桥、跪姿劈砍练核心；单车时间延长或间歇训练', '达标：各方向主动活动度完全无痛、步态正常；屈髋肌力 4/5，外展、内收、伸、内外旋 4/5']),
     ('第 9～12 周', PK, RED, ['加大幅度和速度；迷你弹力带侧向步、小蹲、多方向台阶训练；椭圆机、单车、爬楼机交叉训练，持续 30 分钟、主观用力 5～7/10', '避免对抗、激进的屈髋肌强化和引起疼痛的强行牵伸', '进入专项训练：屈髋肌力 4+/5，其余下肢肌群 5/5']),
     ('第 13～16 周', GR, (40, 120, 60), ['深蹲、硬拉、弓步，进阶到单腿；多方向敏捷；进阶核心；按项目需要做增强式训练', '达标：活动度完全、心肺耐力符合运动或工作需求', 'Y 平衡两侧差：前向 ≤ 4 cm，后内、后外 ≤ 6 cm', '单跳、三级跳、交叉三级跳肢体对称指数 ≥ 90%，落地无髋内旋、膝外翻'])]
y = 20
for t, bg, c, items in S:
    h = 66 + sum(para_h(s, 24, 1040, gap=8) + 10 for s in items)
    dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
    yy = y + 62
    for s in items: yy = bullet(dr, 70, yy, s, 24, 1060, gap=8) + 10
    y += h + 16
im = im.crop((0, 0, W, y))
save(titled(im, '术后五阶段一览（编者根据原文表 6 整理）'), 10)

# 进阶标准时间线
fig, ax = plt.subplots(figsize=(12, 4.4), dpi=100)
ph = [(0, 1, '第 1 周', '#0b6e82'), (1, 4, '2～4 周', '#f39a2b'), (4, 8, '5～8 周', '#7b5ea7'), (8, 12, '9～12 周', '#d1495b'), (12, 16, '13～16 周', '#5aa469')]
for a, b_, t, c in ph:
    ax.barh(0, b_ - a, left=a, color=c, height=0.5); ax.text((a + b_) / 2, 0, t, ha='center', va='center', color='white', fontsize=13)
ms = [(4, '完全负重'), (8, '肌力 4/5\n活动度完全无痛'), (12, '屈髋 4+/5\n其余 5/5'), (16, 'Y 平衡 + 跳跃\n对称 ≥ 90%')]
for x, t in ms:
    ax.plot([x, x], [0.3, 0.75], color='#555', lw=1.5); ax.text(x, 0.8, t, ha='center', va='bottom', fontsize=13)
ax.text(8, -0.55, '盂唇修复、微骨折者可能限制负重至第 8 周，时间线需相应后移', ha='center', fontsize=13, color='#c0392b')
ax.set_xlim(-0.5, 17); ax.set_ylim(-0.8, 1.15); ax.set_yticks([]); ax.set_xticks(range(0, 17, 2)); ax.set_xlabel('术后周数', fontsize=13)
ax.spines[['top', 'right', 'left']].set_visible(False); ax.tick_params(labelsize=12)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '术后各阶段的关键进阶节点', 1200), 11)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), '股骨髋臼撞击综合征 · 运动康复', font=font(40), fill=TEAL)
dr.text((50, 130), '保守还是手术，', font=font(62), fill=INK)
dr.text((50, 220), '都练这四件事', font=font(62), fill=INK)
dr.text((50, 318), '诊断要点 · 非手术方案 · 术后 16 周五阶段', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
