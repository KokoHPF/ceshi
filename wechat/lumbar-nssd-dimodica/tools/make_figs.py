#!/usr/bin/env python3
"""Di Modica 等 2025《以非手术脊柱减压为核心、辅以物理因子的强化非侵入方案治疗 L4-L5 和 L5-S1 双节段椎间盘突出：病例报告》
（Trauma Case Reports）推文配图。
原文是 CC BY-NC-ND 4.0（禁止演绎），所以原文图一律原样引用、不改图内任何内容，中文说明只放在图外的图注条里：
原文图 1（体位照片）、图 2a/2b（测量示意）、图 3～5（MRI）图内只有字母，没有英文；
原文图 6（带英文坐标轴的折线图）不翻译，改由编者按原文表 2 的数据自己重画。
首图、病例卡、治疗安排图（按原文表 1）、临床要点卡和封面为编者绘制。
用法：python3 make_figs.py <src 目录> <输出目录> <中文字体>"""
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50); ORG = (215, 120, 20)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)


def raw(name):
    return Image.open(f'{SRC}/{name}').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        # 标点不放行首；英文单词、数字和小数点不拆开
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”' and not (line[-1:].isascii() and (line[-1:].isalnum() or line[-1:] == '.') and ch.isascii() and (ch.isalnum() or ch in '.%')):
            dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    """原图等比缩放后原样放在下方，中文图注放在图外上方的色条里，不改动原图内容"""
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


def sessions_chart():
    """原文表 1：2023 年 5～10 月每月的治疗次数（NSSD+常规理疗 / 只做常规理疗）"""
    W = 1200; im = Image.new('RGB', (W, 900), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '6 个月、92 次治疗是怎么排的（原文表 1）', font=font(36), fill='white')
    data = [('5 月', 20, 0, ''), ('6 月', 12, 8, ''), ('7 月', 12, 8, '复查 MRI'), ('8 月', 12, 0, ''), ('9 月', 8, 4, ''), ('10 月', 8, 0, '+针对性训练')]
    A, B = TEAL, (150, 200, 210)
    x0 = 30
    for c, t in ((A, 'NSSD + 常规理疗'), (B, '只做常规理疗')):
        dr.rectangle([x0, 106, x0 + 26, 132], fill=c); dr.text((x0 + 36, 102), t, font=font(26), fill=INK); x0 += 340
    L, R, top, bot = 110, W - 40, 190, 620
    Y = lambda v: bot - (bot - top) * v / 22
    for v in (0, 5, 10, 15, 20):
        dr.line([L, Y(v), R, Y(v)], fill=(230, 230, 230), width=1)
        dr.text((L - 12, Y(v)), str(v), font=font(22), fill=GREY, anchor='rm')
    dr.text((L - 12, top - 40), '次/月', font=font(22), fill=GREY)
    step = (R - L) / len(data)
    for i, (m, a, b, note) in enumerate(data):
        cx = L + step * (i + 0.5); bw = 90
        dr.rectangle([cx - bw / 2, Y(a), cx + bw / 2, bot], fill=A)
        if b: dr.rectangle([cx - bw / 2, Y(a + b), cx + bw / 2, Y(a)], fill=B)
        dr.text((cx, Y(a + b) - 8), str(a + b), font=font(26), fill=INK, anchor='md')
        dr.text((cx, bot + 16), m, font=font(26), fill=INK, anchor='ma')
        if note: dr.text((cx, bot + 52), note, font=font(22), fill=RED, anchor='ma')
    y = bot + 110
    y = para(dr, 30, y, '合计 92 次，其中 72 次含 NSSD。NSSD 每次 30 分钟，牵引力不超过体重的 50%，之后静止稳定一段时间；'
             '常规理疗只写了“BTL 公司的多种能量刺激设备”，具体是什么、参数多少，原文没给。', 24, W - 60, fill=GREY)
    y = para(dr, 30, y + 4, '方法里说开头一个月是“每周 5 次”，表 1 第一个月正好 20 次；4 月开始方案，治疗次数从 5 月记起。', 24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 10))


def mri_chart():
    """原文表 2 的 MRI 测量值，按真实时间间隔重画（原文图 6 是等间距横轴）"""
    T = [0, 6, 9, 14]  # 2022-10、2023-04、2023-07、2023-12，距首次 MRI 的月数
    rows = [
        ('突出物前后径（mm）', [4.54, 7.40, 5.4, 2.00], [5.68, 5.80, 5.26, 1.56], 8, '越小越好'),
        ('突出物面积（mm²）', [47.03, 94.72, 55.66, 28.00], [50.33, 55.09, 49.23, 23.66], 100, '越小越好'),
        ('椎管前后径（mm）', [14.53, 10.20, 12.99, 17.32], [7.79, 8.25, 8.54, 12.58], 20, '越大越好'),
        ('椎管面积（mm²）', [160.09, 141.12, 148.36, 185.20], [154.97, 144.81, 155.3, 181.06], 200, '越大越好'),
        ('突出指数 HI', [143.06, 299.67, 159.96, 67.94], [97.54, 163.12, 103.47, 57.64], 300, '越小越好'),
    ]
    W = 1200; PH = 330; im = Image.new('RGB', (W, 140 + PH * 3 + 300), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), 'MRI 测量值怎么变（编者按原文表 2 重画）', font=font(36), fill='white')
    C1, C2 = RED, TEAL
    x0 = 30
    for c, t in ((C1, 'L4-L5'), (C2, 'L5-S1')):
        dr.line([x0, 119, x0 + 40, 119], fill=c, width=6); dr.text((x0 + 52, 104), t, font=font(26), fill=INK); x0 += 200
    dr.rectangle([x0, 106, x0 + 40, 132], fill=(255, 243, 205)); dr.text((x0 + 52, 104), '强化治疗期（2023-05～10）', font=font(26), fill=INK)
    for k, (name, a, b, vmax, good) in enumerate(rows):
        col, row = k % 2, k // 2
        if k == 4: col = 0
        L = 100 + col * 570 if k < 4 else 100; R = L + 420 if k < 4 else W - 140
        top = 170 + row * PH + 70; bot = top + 180
        X = lambda t: L + (R - L) * t / 14
        Y = lambda v: bot - (bot - top) * v / vmax
        dr.rectangle([X(6.5), top, X(13), bot], fill=(255, 243, 205))
        dr.text((L - 60, top - 46), name, font=font(26), fill=INK)
        dr.text((R, top - 42), good, font=font(22), fill=GREY, anchor='ra')
        for v in (0, vmax / 2, vmax):
            dr.line([L, Y(v), R, Y(v)], fill=(225, 225, 225), width=1)
            dr.text((L - 10, Y(v)), f'{v:g}', font=font(20), fill=GREY, anchor='rm')
        for t, lab in zip(T, ('22-10', '23-04', '23-07', '23-12')):
            dr.text((X(t), bot + 10), lab, font=font(20), fill=GREY, anchor='ma')
        for vals, c, off in ((a, C1, -1 if a[1] >= b[1] else 1), (b, C2, 1 if a[1] >= b[1] else -1)):
            pts = [(X(t), Y(v)) for t, v in zip(T, vals)]
            dr.line(pts, fill=c, width=5)
            for (px, py), v in zip(pts, vals):
                dr.ellipse([px - 7, py - 7, px + 7, py + 7], fill=c)
            eo = -1 if vals[-1] >= (b[-1] if vals is a else a[-1]) else 1
            dr.text((pts[-1][0] + 12, pts[-1][1] + eo * 14), f'{vals[-1]:g}', font=font(20), fill=c, anchor='lm')
            dr.text((pts[1][0], pts[1][1] - 12 if off < 0 else pts[1][1] + 32), f'{vals[1]:g}', font=font(20), fill=c, anchor='md')
    y = 170 + 3 * PH - 10
    y = para(dr, 30, y, '横轴按实际间隔排列：治疗前（2022-10 → 2023-04）L4-L5 突出明显加重，治疗中和治疗后各项指标持续好转。'
             '以 2023 年 4 月为基线，两个节段突出物前后径都缩小约 73%；突出指数 L4-L5 下降约 77%、L5-S1 约 65%（编者按表 2 计算，和原文正文写的“74% 对 65%”对不上）。', 24, W - 60, fill=GREY)
    y = para(dr, 30, y + 4, '这些数值由作者自己在 MRI 上手工测量，没有说明测量者是否设盲、重复测量是否一致，前后几次 MRI 是否同一台机器也没交代。', 24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 10))


# 1 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '病例报告 · 《Trauma Case Reports》2025', font=font(30), fill=TEAL)
dr.text((70, 125), '以非手术脊柱减压为核心的强化非侵入方案', font=font(48), fill=INK)
dr.text((70, 195), '治疗 L4-L5、L5-S1 双节段腰椎间盘突出', font=font(44), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Di Modica V, Sciarrone GJ.', font=font(26), fill=GREY)
dr.text((70, 375), 'Trauma Case Rep. 2025;58:101214. doi:10.1016/j.tcr.2025.101214', font=font(26), fill=GREY)
dr.text((70, 420), '意大利 BioSalus 康复中心 · 米兰 Humanitas Pio X 脊柱与机器人外科中心', font=font(26), fill=GREY)
dr.text((70, 560), '编者中文解读，仅作非商业学术交流 · 原文 CC BY-NC-ND 4.0', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, '病例概况（编者根据原文整理）', [
    ('谁', '45 岁女性（摘要写 46 岁），体重指数正常，平时不运动\n主诉：明显腰痛、功能受限', LT, TEAL),
    ('影像', 'L4-L5：左旁中央型突出，压迫硬膜囊腹侧，轻触 L5 神经根\nL5-S1：左外侧较大突出，压迫硬膜囊，部分堵住侧隐窝，压迫左 S1 神经根', PK, RED),
    ('之前的治疗', '2022-09 起病 → 10 次理疗＋透热＋按摩＋药物，轻微好转\n2023-02 加重 → 10 次干针＋磁疗＋Tecar，没效果\n2023-03 神经外科：建议手术；患者拒绝', OR, ORG),
    ('换诊所后', '2023-04 功能检查（股神经牵拉试验、直腿抬高、足尖/足跟行走、MRC 肌力）＋复查 MRI → 开始 6 个月强化方案', GR, (0, 120, 60)),
]), 2)

save(capbox(raw('fig1.jpg'), '原文图 1  NSSD 治疗体位：患者趴在分节治疗床上，骨盆用腰带固定，双腿伸直、床尾向下倾斜，由电脑控制牵引力作用在病变节段（注意：照片是俯卧，正文却写“仰卧”）'), 3)
save(sessions_chart(), 4)

a, b = raw('fig2a.jpg'), raw('fig2b.jpg')
h = 700; a = a.resize((round(a.width * h / a.height), h)); b = b.resize((round(b.width * h / b.height), h))
both = Image.new('RGB', (a.width + b.width + 20, h), 'white'); both.paste(a, (0, 0)); both.paste(b, (a.width + 20, 0))
save(capbox(both, '原文图 2a（左）、2b（右）  轴位 MRI 测量示意。左：AB 为突出物前后径，上方粗线围成的区域为突出物面积，CD 为椎管前后径，下方区域为椎管面积。'
                  '右：EF 为突出物宽度，GH 为椎管总宽，IJ 为椎管总长，用于计算突出指数 HI = 突出物长×宽 ÷（椎管总长×总宽）× 1000'), 5)
save(capbox(raw('fig3.jpg'), '原文图 3  矢状位 T2 加权 MRI。A：2022-10 首次出现症状后；B：2023-04 初诊（治疗前）；C：2023-07 治疗 2 个月；D：2023-12 治疗结束后 1 个月'), 6)
save(capbox(raw('fig4.jpg'), '原文图 4  L4-L5 轴位 T2 加权 MRI，时间点同图 3（A：2022-10，B：2023-04 治疗前，C：2023-07，D：2023-12）'), 7)
save(capbox(raw('fig5.jpg'), '原文图 5  L5-S1 轴位 T2 加权 MRI，时间点同图 3（A：2022-10，B：2023-04 治疗前，C：2023-07，D：2023-12）'), 8)
save(mri_chart(), 9)

save(card(1200, '落到临床（编者整理）', [
    ('这篇能说明什么', '一位拒绝手术的双节段突出患者，做了 6 个月、92 次以 NSSD 为主的治疗，MRI 上突出明显缩小、功能检查转阴，随访 6 个月没有复发。说明“这种做法可行”，不能说明“是 NSSD 起的作用”', LT, TEAL),
    ('突出会自己吸收', '大的突出、游离型突出自然吸收并不少见，多节段和单节段吸收率相近（Hornung 2024）。没有对照，影像改善不能直接算在减压床头上', OR, ORG),
    ('先看有没有红旗', '马尾综合征（大小便障碍、鞍区麻木）、进行性肌力下降，应尽快转诊手术评估，不适合先尝试长疗程保守治疗（编者补充）', PK, RED),
    ('评估要有患者自评', '本例没报告任何疼痛评分或功能问卷（VAS、ODI 等），只有体检和 MRI。临床上建议至少记录疼痛和 ODI，再配合直腿抬高、肌力和感觉检查', GR, (0, 120, 60)),
    ('注意利益冲突和成本', '第一作者接受过设备厂商 BTL 的演讲酬金，用到的减压床和理疗设备都是 BTL 的。92 次治疗的时间和费用，作者自己也承认需要和手术做比较', PU, (110, 70, 190)),
]), 10)

# 封面：纯文字
W, H = 900, 383; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, H], fill=TEAL)
dr.text((50, 46), '病例报告 · Trauma Case Reports 2025', font=font(26), fill=TEAL)
dr.text((50, 118), '双节段腰突拒绝手术', font=font(56), fill=INK)
dr.text((50, 198), '92 次非手术脊柱减压', font=font(46), fill=INK)
dr.text((50, 290), 'NSSD · 物理因子 · MRI 定量随访', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
