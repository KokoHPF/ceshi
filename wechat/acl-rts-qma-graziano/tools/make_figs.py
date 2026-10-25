#!/usr/bin/env python3
"""Graziano 等 2017《骨骼未成熟运动员 ACL 重建后重返运动》（OJSM）推文配图。
首图中文标题卡、原文图 1～7（图 2 流程图已用 tools/fig-translate 译成中文：src/fig2_zh.png；其余是照片，只加中文图注）、
动作质量评估卡、结果卡、临床要点卡、封面。
原文照片取自 PMC 开放获取包（src/fig*.jpg，比 PDF 内嵌的分辨率高）。
用法：python3 make_figs.py <src 目录> <输出目录> <中文字体>"""
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)


def raw(n):
    return Image.open(f'{SRC}/fig{n}.jpg' if n != 2 else f'{SRC}/fig2_zh.png').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        # 标点不放行首
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”': dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
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


def results():
    """42 人的去向：数字按原文正文和表 2、表 3"""
    W = 1200; im = Image.new('RGB', (W, 1000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '42 名运动员的结局（编者根据原文整理）', font=font(36), fill='white')
    L, R = 60, W - 60; X = lambda n: L + (R - L) * n / 42
    segs = [(35, '35 人 无再损伤，重返运动', GR, (0, 120, 60)), (6, '6 人 ACL 再断', PK, RED), (1, '1 人 半月板损伤', OR, (200, 120, 0))]
    x = 0; y = 120
    for n, lab, c, a in segs:
        dr.rectangle([X(x), y, X(x + n) - 3, y + 90], fill=a); x += n
    dr.text((L, y + 104), '35 人（83%）无再损伤', font=font(28), fill=(0, 120, 60))
    dr.text((X(38), y + 104), '6 人 ACL 再断', font=font(28), fill=RED, anchor='ma')
    dr.text((R, y + 150), '1 人 半月板损伤', font=font(28), fill=(200, 120, 0), anchor='ra')
    y = 370
    rows = [
        ('平均重返时间', '12 ± 2 个月；12 个月前放行的 19 人里 4 人（21%）二次受伤'),
        ('6 个月时', '没有一个人能完成无代偿的双腿深蹲'),
        ('9 个月时', '除 3 人外，单腿动作（如单腿跳）都还有风险表现'),
        ('6 例 ACL 再断', '同侧 4、对侧 2；全部是非接触伤；除术后 3 个月操场受伤那例，都发生在长曲棍球、篮球比赛中'),
        ('其中 3 例', '发生在没被放行的情况下：术后 3 个月操场受伤、被建议别打篮球却打了、只被允许参加长曲棍球以外的项目却打了长曲棍球'),
        ('竞技水平', '再损伤 83% 来自高水平（巡回联赛）组；娱乐和体育课组 0 例'),
        ('功能指标', 'KT-1000 双侧差 1.1 mm；单腿跳 93%；IKDC 93.1；Lysholm 97.6'),
    ]
    for h, t in rows:
        dr.text((L, y), h, font=font(28), fill=TEAL)
        y = para(dr, L + 230, y, t, 28, R - L - 230, gap=10) + 14
    return im.crop((0, 0, W, y + 10))


# 1 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '病例系列 · 《Orthopaedic Journal of Sports Medicine》2017', font=font(30), fill=TEAL)
dr.text((70, 135), '骨骼未成熟运动员 ACL 重建后重返运动', font=font(56), fill=INK)
dr.text((70, 210), '用动作质量评估加量化测试，预防二次损伤', font=font(44), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Graziano J, Chiaia T, de Mille P, Nawabi DH, Green DW, Cordasco FA.', font=font(26), fill=GREY)
dr.text((70, 390), 'Orthop J Sports Med. 2017;5(4):2325967117700599. doi:10.1177/2325967117700599', font=font(26), fill=GREY)
dr.text((70, 435), '美国纽约特种外科医院（HSS）', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作非商业学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(raw(1), '原文图 1  单腿跳远测试两侧距离 100% 对称，但落地质量差：膝外翻、骨盆下沉、躯干侧倾'), 2)
save(capbox(raw(2), '原文图 2  按标准进阶的康复流程（图中文字由编者译成中文；“第 4～6 个月”“第 5～6 个月”照原图）'), 3)
save(capbox(raw(3), '原文图 3  深蹲：A 膝主导（膝盖前移超过脚踝）；B 髋主导（重心向后坐到髋，膝对准脚踝）'), 4)
save(capbox(raw(4), '原文图 4  A 力线差：躯干侧倾、骨盆移位，右膝外翻；B 力线好：躯干中立、骨盆水平、膝无外翻'), 5)
save(capbox(raw(5), '原文图 5  A 术后 6 个月深蹲时重心偏向健侧（左腿）；B 同一人 12 个月时两侧负重对称，个子也明显长高了'), 6)
save(capbox(raw(6), '原文图 6  原地跳落地：A 屈膝不够、缓冲浅，双膝外翻；B 训练后用髋和膝吸收冲击，无外翻'), 7)
save(capbox(raw(7), '原文图 7  A 跳到对侧腿：落在左腿（健侧）力线好，落在右腿（术侧）膝外翻；B 90° 变向：左为力线正确，右为膝外翻；C 听口令急停：左为力线正确，右为髋内旋加膝外翻'), 8)

save(card(1200, '动作质量评估看什么（编者根据原文整理）', [
    ('每个动作都看 8 项', '疼痛 · 动作策略（髋主导还是膝主导）· 恐惧犹豫 · 动态力线 · 两侧对称 · 下蹲深度 · 疲劳后质量下降多快 · 控制', LT, TEAL),
    ('评估 1（约术后 6～7 个月）', '深蹲、单腿站、20 cm 台阶前向下台阶、单腿蹲、原地跳、侧向跳；能做再加立定跳远和单腿跳\n同时测 KT-1000 和膝屈伸等速肌力', GR, (0, 120, 60)),
    ('评估 2', '加跳跃、落地、减速；如安全再测等速肌力和单腿跳\n通过后开始有人看着的非对抗专项练习（传球、控球等）', OR, (200, 120, 0)),
    ('评估 3', '提速：前跑和后退跑、折返跑、冲刺听口令急停、90° 变向、90° 侧滑步\n从无对抗逐步过渡到有对抗', PK, RED),
    ('怎么用', 'Dartfish 录像，回放给孩子和家长看；每 6～8 周复评一次，针对问题给训练，直到全速专项动作质量都合格才放行', PU, (110, 70, 190)),
]), 9)
save(results(), 10)

save(card(1200, '落到临床（编者整理）', [
    ('别只看对称指数', '单腿跳 100% 对称也可能膝外翻、骨盆下沉；放行前录像看动作质量', PK, RED),
    ('术前就讲清楚时间', '和家长说好最少 9 个月、多半 12 个月；本组 12 个月前放行的二次受伤率更高', LT, TEAL),
    ('盯紧生长发育', '长个子后杠杆变长、重心改变，暑假前练好的动作回来可能又走样；骨骺闭合前定期复评', GR, (0, 120, 60)),
    ('高水平变向项目要更严', '足球、长曲棍球等高水平变向运动员占了再损伤的大头，放行标准应更高，并逐个项目放行', OR, (200, 120, 0)),
    ('健侧也要练', '对侧再断占三分之一；代偿把负荷转到健侧，两条腿都要按预防 ACL 损伤的原则训练', PU, (110, 70, 190)),
]), 11)

# 封面：原文图 3（膝主导和髋主导深蹲）
c = raw(3); w = c.width; h = round(w * 383 / 900)
if h > c.height: h = c.height; w = round(h * 900 / 383)
x0 = (c.width - w) // 2; y0 = (c.height - h) // 2
c.crop((x0, y0, x0 + w, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
