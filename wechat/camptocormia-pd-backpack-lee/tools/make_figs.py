#!/usr/bin/env python3
"""Lee 等 2017《背伸肌强化训练与背包疗法治疗帕金森病躯干前屈：回顾性预试验》（Ann Rehabil Med）推文配图。
原文是 CC BY-NC 4.0（允许演绎，禁止商业使用）。原文图 1～5 图内只有 A～E 字母和箭头，没有英文需要翻译，
所以原图原样引用，中文说明放在图外的图注条里；首图、研究概况卡、训练方案图、各患者角度变化图（按原文表 2 重画）、
临床要点卡和封面为编者绘制。
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
    import re
    line = ''
    # 英文单词、数字整体换行；标点不放行首
    for tok in re.findall(r"[A-Za-z0-9.%\-]+|.", t):
        if line and dr.textlength(line + tok, font=font(fs)) > w and tok not in '，。；：、）”°':
            dr.text((x, y), line.rstrip(), font=font(fs), fill=fill); y += fs + gap; line = tok.lstrip()
        else: line += tok
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    """原图等比缩放后原样放在下方，中文图注放在图外上方的色条里"""
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


def program():
    """住院组一次 30 分钟课程的构成 + 背包和门诊安排"""
    W = 1200; im = Image.new('RGB', (W, 1400), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '训练方案怎么排（编者根据原文方法整理）', font=font(36), fill='white')
    dr.text((30, 104), '住院组（6 人）：每次 30 分钟，每天 2 次，约 5 周（平均 34 天，23～44 天）', font=font(28), fill=INK)
    L, R, y0, h = 30, W - 30, 160, 110
    xm = L + (R - L) * 20 / 30
    dr.rounded_rectangle([L, y0, xm - 4, y0 + h], 10, fill=TEAL)
    dr.rounded_rectangle([xm + 4, y0, R, y0 + h], 10, fill=ORG)
    dr.text(((L + xm) / 2, y0 + 30), '20 分钟 · 训练（以强化为主）', font=font(30), fill='white', anchor='mm')
    dr.text(((L + xm) / 2, y0 + 76), '核心肌群强化｜骨盆倾斜｜背伸肌强化｜弯曲侧牵伸', font=font(24), fill='white', anchor='mm')
    dr.text(((xm + R) / 2, y0 + 30), '10 分钟 · 背包行走', font=font(30), fill='white', anchor='mm')
    dr.text(((xm + R) / 2, y0 + 76), '背着低挂背包走路', font=font(24), fill='white', anchor='mm')
    y = y0 + h + 40
    blocks = [
        ('低挂背包', '起始 1.5 kg，按耐受逐步加重，直到站立时前屈被纠正为止；教患者每天背着走路至少 2 小时。'
                    '背包要挂得低（贴在下背部和骨盆后方）。最大加到多重，原文没写', OR, ORG),
        ('背不动怎么办', '1 名患者嫌背包太重受不了，改用前方脊柱过伸支具（原文图 2E，原文写成 hyperflexion，应为 hyperextension）', PU, (110, 70, 190)),
        ('门诊组（3 人）', '每周来 1 次，平均 3 个月；训练内容和住院组“差别不大”，重点教会居家训练和背包；'
                       '每 2～4 周复诊一次，查依从性、调整背包重量', GR, (0, 120, 60)),
        ('原文没写清的', '每个动作做几组几次、保持多久、怎么进阶；背包里装什么、怎么挂；门诊组在家每天练多少', PK, RED),
    ]
    for hd, t, c, a in blocks:
        top = y; dd = ImageDraw.Draw(Image.new('RGB', (W, 2000)))
        y2 = para(dd, 50, y + 62, t, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), hd, font=font(32), fill=a)
        para(dr, 50, y + 62, t, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


def angle_chart():
    """原文表 2 的站立前屈角，治疗前后连线"""
    data = [(1, 43, 43), (2, 77, 15), (3, 20, 2), (4, 24, 20), (5, 41, 32), (6, 6, -6), (7, 24, 5), (8, 49, 2), (9, 12, -3)]
    outp = {5, 8, 9}
    W = 1200; im = Image.new('RGB', (W, 1300), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '9 名患者治疗前后的站立前屈角（编者按原文表 2 重画）', font=font(34), fill='white')
    x0 = 30
    for c, t in ((GREY, '治疗前'), (TEAL, '治疗后')):
        dr.ellipse([x0, 108, x0 + 26, 134], fill=c); dr.text((x0 + 36, 102), t, font=font(26), fill=INK); x0 += 180
    dr.text((x0 + 10, 102), '★ 门诊组（居家训练）', font=font(26), fill=ORG)
    L, R, top, row = 150, 790, 200, 88
    vmin, vmax = -10, 80
    X = lambda v: L + (R - L) * (v - vmin) / (vmax - vmin)
    bot = top + row * len(data)
    for v in range(-10, 81, 10):
        dr.line([X(v), top - 20, X(v), bot], fill=(205, 205, 205) if v == 0 else (235, 235, 235), width=2 if v == 0 else 1)
        dr.text((X(v), bot + 10), f'{v}°', font=font(22), fill=GREY, anchor='ma')
    dr.line([X(45), top - 20, X(45), bot], fill=RED, width=2)
    dr.text((X(45), top - 46), '45°：多数文献的诊断阈值', anchor='ma', font=font(22), fill=RED)
    for i, (n, a, b) in enumerate(data):
        y = top + row * i + row / 2
        dr.text((L - 20, y), f'{"★" if n in outp else ""}{n} 号', font=font(26), fill=ORG if n in outp else INK, anchor='rm')
        dr.line([X(a), y, X(b), y], fill=(150, 200, 210), width=8)
        dr.ellipse([X(a) - 11, y - 11, X(a) + 11, y + 11], fill=GREY)
        dr.ellipse([X(b) - 11, y - 11, X(b) + 11, y + 11], fill=TEAL)
        d = a - b
        lx = R + 30
        dr.text((lx, y), f'{a}° → {b}°' + (f'（改善 {d}°）' if d else '（没变）'), font=font(22), fill=INK if d else RED, anchor='lm')
    y = bot + 60
    y = para(dr, 30, y, '9 人平均改善 20.7°（Wilcoxon 符号秩检验 p=0.012）。治疗前达到 45° 的只有 2 人（2 号、8 号），'
             '6 号和 9 号治疗前只有 6° 和 12°，治疗后变成负值（身体略向后仰）。', 24, W - 60, fill=GREY)
    y = para(dr, 30, y + 4, '角度是在侧面照片上手工量的（足中点—髋部点—耳廓中点），先自由行走 5 分钟再拍；测量者是否设盲没写。', 24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 10))


# 1 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '回顾性预试验 · 《Annals of Rehabilitation Medicine》2017', font=font(30), fill=TEAL)
dr.text((70, 125), '背伸肌强化训练与背包疗法', font=font(50), fill=INK)
dr.text((70, 195), '治疗帕金森病躯干前屈（camptocormia）', font=font(44), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Lee KH, Kim JM, Kim HS.', font=font(26), fill=GREY)
dr.text((70, 375), 'Ann Rehabil Med. 2017;41(4):677-685. doi:10.5535/arm.2017.41.4.677', font=font(26), fill=GREY)
dr.text((70, 420), '韩国国民健康保险公团一山医院 康复医学科', font=font(26), fill=GREY)
dr.text((70, 560), '编者中文解读，仅作非商业学术交流 · 原文 CC BY-NC 4.0', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, '研究概况（编者根据原文整理）', [
    ('谁', '9 名帕金森病患者（女 6、男 3），63～82 岁，均由神经内科确诊，2013 年 3 月～2015 年 8 月因姿势不稳转到康复科', LT, TEAL),
    ('怎么定义躯干前屈', '站立或行走时胸腰段异常前屈 ≥5°，躺下能纠正（以此和固定性驼背区分），并伴有日常生活或运动功能受限。'
                     '作者自己也说多数文献用的是 ≥45°', PK, RED),
    ('分组', '住院 6 人：每天 2 次、每次 30 分钟，约 5 周\n门诊 3 人：每周 1 次，平均 3 个月，以居家训练和背包为主', OR, ORG),
    ('看什么', '治疗前后：站立前屈角（侧面照片测量）、UPDRS 第 II 部分（日常生活）、第 III 部分（运动检查）、改良 Hoehn-Yahr 分期\n数据全部从病历里回顾性收集，没有对照组', GR, (0, 120, 60)),
]), 2)

save(capbox(raw('fig2.jpg'), '原文图 2  几种保守治疗方式。A：核心肌群强化训练；B：骨盆倾斜训练；C：背伸肌强化训练（俯卧抬起上身）；'
                              'D：低挂背包；E：前方脊柱过伸支具（原文写作 hyperflexion，应为 hyperextension）'), 3)
save(program(), 4)
save(capbox(raw('fig1.jpg'), '原文图 1  7 号患者治疗前后。A：她因驼背和腰痛做过 T12～L5 长节段融合手术，术后反而出现躯干前屈；'
                              'B：康复治疗前的侧面照；C：康复治疗后。白线示前屈角的测量方法：足中点—髋部点（髂前上棘水平线与股骨大转子垂线的交点）—耳廓中点'), 5)
save(angle_chart(), 6)
save(capbox(raw('fig3.jpg'), '原文图 3  4 号患者治疗前（A）后（B）。图注说她在门诊学居家训练，居家训练加背包 4 周后前屈改善'
                              '（但原文表 1 里她的治疗时长是 35 天，和住院组的写法一样）'), 7)
save(capbox(raw('fig5.jpg'), '原文图 5  9 号患者行走中前屈角加大。A：刚开始时前屈不明显；B：走了 10 分钟后前屈明显加重。'
                              '所以“什么时候量角度”会直接影响结果'), 8)
save(capbox(raw('fig4.jpg'), '原文图 4  1 号患者腰椎 MRI（T2 加权轴位），箭头示椎旁肌萎缩、脂肪变性。她是 9 人里唯一完全没改善的'), 9)

save(card(1200, '落到临床（编者整理）', [
    ('先区分是不是“真”躯干前屈', '躺下、靠墙站或扶高位助行器能伸直的，才是可纠正的躯干前屈；躺下也伸不直的是结构性驼背，'
                            '还要排除骨质疏松压缩骨折、腰椎管狭窄、既往脊柱手术后的交界区后凸', LT, TEAL),
    ('背伸肌强化可以作为首选之一', '俯卧抬上身、核心和骨盆训练成本低、风险小，本研究 8/9 有改善；但证据只是 9 例回顾性、无对照的预试验', GR, (0, 120, 60)),
    ('低挂背包：便宜的“外挂”', '从 1.5 kg 起，按耐受加重，行走时背着，每天累计 ≥2 小时；注意 8 号患者一摘背包前屈就回来了，'
                         '它更像辅助，不能替代训练', OR, ORG),
    ('早做，病程长的效果差', '1 号患者躯干前屈已有 10 年、MRI 上椎旁肌已明显脂肪变，完全没效果。椎旁肌萎缩前开始训练可能更有希望', PK, RED),
    ('评估要统一', '固定在行走若干分钟后、用同一套标志点拍侧面照或量角度；同时记录 UPDRS、步行距离和疼痛，不能只看角度', PU, (110, 70, 190)),
]), 10)

# 封面：纯文字
W, H = 900, 383; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, H], fill=TEAL)
dr.text((50, 46), '回顾性研究 · Ann Rehabil Med 2017', font=font(26), fill=TEAL)
dr.text((50, 118), '帕金森“弯腰驼背”', font=font(58), fill=INK)
dr.text((50, 198), '背伸肌训练＋低挂背包', font=font(46), fill=INK)
dr.text((50, 290), '躯干前屈 · 9 例 · 前屈角平均改善 21°', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
