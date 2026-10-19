#!/usr/bin/env python3
"""Halabchi 等 2024 腓肠肌内侧头拉伤：首图中文标题卡；分级卡、四期总览、重返运动卡为编者绘制；原文图 6 诊疗流程按原图重绘为中文；
原文图 1 超声英文标注改为中文，图 2～5 加中文标注。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
raw = lambda x: Image.open(BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def vstack(ims, W=1200, gap=0):
    ims = [i.resize((W, round(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    out = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: out.paste(i, (0, y)); y += i.height + gap
    return out


def tile(im, n, cap, W=1200, maxh=1000):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    if im.height > maxh: im = im.resize((round(im.width * maxh / im.height), maxh), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in f'图 {n}　{cap}':
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, ((W - im.width) // 2, hh + 8)); return t


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '综述 · 《伊朗伊斯兰共和国医学杂志》2024', font=font(32), fill=TEAL)
for i, t in enumerate(['“网球腿”其实多是腓肠肌拉伤：', '诊断、分级与四期康复']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '腓肠肌内侧头拉伤 · 附诊疗流程图', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Halabchi F, Tavana MM, Seifi V, Mahmoudi Zarandi M. Med J Islam Repub Iran 2024;38:55', font=font(28), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1、2 ----------
us = raw(10); s = us.width / 600; d = ImageDraw.Draw(us)
for box, (x, y), t in [((65, 18, 140, 37), (75, 19), '近端'), ((275, 18, 355, 37), (295, 19), '长轴'), ((505, 15, 565, 35), (515, 16), '远端'),
                       ((52, 43, 112, 62), (58, 44), '缺损'), ((372, 56, 482, 75), (392, 57), '腓肠肌'), ((412, 108, 472, 127), (412, 109), '比目鱼肌')]:
    d.rectangle(tuple(int(v * s) for v in box), fill=(10, 10, 10))
    d.text((int(x * s), int(y * s)), t, font=font(int(15 * s)), fill='white')
mri = vstack([raw(11), raw(12)], 1800)
save(board([tile(us, 1, '全景超声：腓肠肌内侧头近端肌腱连续性中断并回缩，缺损处有积液，上方皮下水肿（原文引自放射学病例库，经授权）'),
            tile(mri, 2, '磁共振：A 冠状位脂肪抑制、B 横断位 T2 像，箭头示右侧腓肠肌内侧头（星号）上部部分撕裂；C 冠状位脂肪抑制 T2 像，三角箭头示筋膜层少量积液（原文引自病例报告，经授权）')],
           '影像：超声与磁共振'), 2)

# ---------- 分级 ----------
W, H = 1400, 760; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
gs = [('轻度', '肌肉损伤约 5%～10%', GR, ['轻度疼痛、压痛、痉挛、肿胀', '功能基本正常，力量和活动度损失很小（< 10°）', '通常还能继续运动']),
      ('中度', '肌肉损伤约 10%～50%', OR, ['中度疼痛、压痛、肿胀', '可摸到缺损', '冲刺受影响，活动度损失 10°～25°', '不能继续运动']),
      ('重度', '肌肉损伤 > 50%', PK, ['剧痛', '明显可摸到缺损', '不能冲刺，活动度损失 > 25°', '影像示完全撕裂'])]
for i, (t, a, c, items) in enumerate(gs):
    x = 20 + i * 460
    dr.rounded_rectangle([x, 20, x + 440, 740], 16, fill=c)
    ctext(dr, x + 220, 40, t, font(48), TEAL); ctext(dr, x + 220, 115, a, font(28), RED)
    y = 190
    for it in items: y = para(dr, x + 30, y, '· ' + it, 28, 380, INK, 8) + 14
save(titled(im, '腓肠肌内侧头拉伤分三级（根据原文表 2 整理）'), 3)

# ---------- 四期 ----------
W = 1400; im = Image.new('RGB', (W, 2600), 'white'); dr = ImageDraw.Draw(im)
ph = [('第 1 期', '急性期', LT,
       ['受伤后 24～48 小时按“保护、适当负荷、冰敷、加压、抬高”处理', '冰敷 + 20～30 mmHg 加压袖套至少 1 周，直到肿胀/血肿消退', '拐杖 1～2 周，按耐受负重；或穿助行靴加足跟垫',
        '禁止软组织手法和按摩、禁止牵伸', '无痛范围内主动、被动活动度', '不同角度等长跖屈 → 非负重等张跖屈；能耐受可做双腿提踵', '非负重平衡板；1 级核心训练；上肢功率车'],
       '肿胀/血肿消退；活动度无痛；等长跖屈无痛；正常步态行走无痛'),
      ('第 2 期', '亚急性期', GR,
       ['可以开始软组织手法', '非负重、低负荷、长时间毛巾静态牵伸', '双腿、单腿提踵（先快速无负荷，再加负荷）', '背伸、内外翻和足内在肌练习',
        '部分到全负重平衡板；2 级核心训练', '减重跑台、水中走；只在平坦硬地上走跑；可以上楼，不下楼'],
       '跖屈向心和离心肌力 5/5 无痛；快走无痛；本期练习基本无痛'),
      ('第 3 期', '强化期', OR,
       ['深部横向摩擦按摩', '负重、低负荷静态牵伸（伸膝、屈膝两种靠墙牵伸）', '各种向心、离心等张练习，按症状进阶', '全负重平衡板，可加后侧负荷',
        '2～3 级核心训练；不平或斜坡行走、固定自行车、下楼梯', '开始其他下肢牵伸'],
       '跖屈∶背伸肌力比 3～4∶1；患腿动态平衡好；慢跑无痛；本期练习基本无痛'),
      ('第 4 期', '重返运动期', PK,
       ['静态、动态、弹振式牵伸结合', '增强式训练和功能训练，逐步过渡到专项动作', '神经肌肉和平衡：单腿站平衡板、单腿风车触地、单腿罗马尼亚硬拉、单腿双臂推胸',
        '3 级核心训练（负重球单、双腿跳等）', '训练时长、频率、强度每次加约 5%', '平地慢跑 → 平坦与不平地面跑 → 冲刺、变向、加减速'],
       '无症状、小腿力量正常、单腿跳功能正常，才进入专项跑动')]
y = 20
for t, a, c, items, ms in ph:
    h = 110 + 46 * len(items) + 70
    dr.rounded_rectangle([20, y, W - 20, y + h], 16, fill=c)
    dr.text((50, y + 18), t, font=font(42), fill=TEAL); dr.text((230, y + 26), a, font=font(32), fill=RED)
    for i, it in enumerate(items): dr.text((60, y + 90 + 46 * i), '· ' + it, font=font(27), fill=INK)
    para(dr, 60, y + 96 + 46 * len(items), '进入下期：' + ms, 27, 1280, (40, 110, 60))
    y += h + 20
save(titled(im.crop((0, 0, W, y)), '非手术康复四期方案（编者根据原文整理）'), 4)

# ---------- 原文图 3～5 ----------
save(board([tile(raw(22), 3, '第 1 期练习：A 屈膝位主动踝活动（1 跖屈、2 背伸、3 内翻、4 外翻）；B 屈膝位被动踝活动（同上 4 个方向）；C 弹力带等张跖屈（1 起始、2 结束）；D 顶墙等长跖屈（1 伸膝、2 屈膝）')], '第 1 期练习'), 5)
save(board([tile(vstack([raw(26), raw(27)], 1198), 4, '第 2 期练习：A 双腿提踵（1 屈膝、2 伸膝）；B 单腿提踵（1 屈膝、2 伸膝）；C 毛巾牵伸小腿（1 屈膝、2 伸膝）', maxh=1400)], '第 2 期练习'), 6)
save(board([tile(raw(31), 5, '第 3 期练习：A 坐姿哑铃提踵（1 起始、2 结束）；B 下蹲接提踵（1 起始、2 结束）；C 靠墙牵伸；D 踮脚走；E 离心提踵')], '第 3 期练习'), 7)

# ---------- 重返运动 ----------
W, H = 1400, 620; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
rs = ['疼痛、紧绷、抽筋等自觉症状完全消失', '压痛等体征完全消失', '心理准备好，有足够信心', '力量、爆发力、耐力和背伸活动度，与健侧差距 < 10%', '能完成专项动作，并完整参加至少 1 次全量训练']
for i, t in enumerate(rs):
    y = 30 + i * 112
    dr.rounded_rectangle([30, y, W - 30, y + 92], 14, fill=GR)
    dr.ellipse([55, y + 18, 111, y + 74], fill=TEAL); ctext(dr, 83, y + 26, str(i + 1), font(34), 'white')
    dr.text((140, y + 26), t, font=font(32), fill=INK)
save(titled(im, '重返运动的 5 条标准'), 8)

# ---------- 流程图重绘 ----------
W, H = 1400, 2200; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
def box(x0, y0, x1, y1, t, fill=LT, fs=27, col=INK, r=12):
    dr.rounded_rectangle([x0, y0, x1, y1], r, fill=fill, outline=(150, 175, 190), width=2)
    lines = t.split('\n'); hh = len(lines) * (fs + 8)
    for i, l in enumerate(lines): ctext(dr, (x0 + x1) / 2, (y0 + y1) / 2 - hh / 2 + i * (fs + 8), l, font(fs), col)
def dia(cx, cy, w, h, t, fs=26):
    dr.polygon([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], fill=OR, outline=(200, 150, 110))
    lines = t.split('\n'); hh = len(lines) * (fs + 6)
    for i, l in enumerate(lines): ctext(dr, cx, cy - hh / 2 + i * (fs + 6), l, font(fs))
def arr(a, b, lab=None, col=TEAL):
    dr.line([a, b], fill=col, width=4)
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    dr.polygon([b, (b[0] - 18 * math.cos(ang - 0.4), b[1] - 18 * math.sin(ang - 0.4)), (b[0] - 18 * math.cos(ang + 0.4), b[1] - 18 * math.sin(ang + 0.4))], fill=col)
    if lab: dr.text(((a[0] + b[0]) / 2 + 8, (a[1] + b[1]) / 2 - 34), lab, font=font(26), fill=RED)
box(450, 20, 950, 110, '外伤后急性小腿后侧痛')
arr((700, 110), (700, 150)); box(450, 150, 950, 230, '病史与查体 ①')
arr((700, 230), (700, 270)); dia(700, 345, 300, 150, '确诊？')
arr((850, 345), (1010, 345), '否'); box(1010, 300, 1380, 390, '肌骨超声或磁共振\n（排除其他诊断）', fs=25)
arr((1195, 390), (1195, 440)); dia(1195, 515, 320, 150, '其他或\n合并诊断？')
arr((1195, 590), (1195, 650), '是'); box(1040, 650, 1350, 730, '相应处理')
arr((1035, 515), (860, 515), '否')
arr((700, 420), (700, 440), None); dia(700, 515, 320, 150, '有早期\n手术指征？②')
dr.text((710, 418), '是', font=font(26), fill=RED)
arr((540, 515), (380, 515), '是'); box(40, 475, 380, 555, '转骨科')
arr((700, 590), (700, 650), '否'); box(500, 650, 900, 730, '第 1 期康复', GR)
box(40, 650, 420, 730, '辅助治疗 ③（有指征时）', (245, 245, 245), 25)
dr.line([420, 690, 500, 690], fill=(150, 150, 150), width=3)
y0 = 730
for k, name in enumerate(['第 2 期康复', '第 3 期康复', '第 4 期康复']):
    cy = y0 + 110 + k * 330
    arr((700, cy - 110), (700, cy - 60)); dia(700, cy, 260, 120, '改善？')
    arr((570, cy), (330, cy), '否'); box(40, cy - 40, 330, cy + 40, '进一步评估', (245, 245, 245))
    arr((700, cy + 60), (700, cy + 140), '是'); box(500, cy + 140, 900, cy + 220, name, GR)
cy = y0 + 110 + 3 * 330
arr((700, cy - 110), (700, cy - 60)); dia(700, cy, 360, 140, '能完成\n专项技能？')
arr((880, cy), (1040, cy), '否'); box(1040, cy - 40, 1350, cy + 40, '骨科会诊', PK)
arr((700, cy + 70), (700, cy + 130), '是'); box(500, cy + 130, 900, cy + 210, '重返运动', GR, 30, TEAL)
im = im.crop((0, 0, W, cy + 230))
nt = Image.new('RGB', (W, 700), 'white'); nd = ImageDraw.Draw(nt)
notes = [('① 重要发现', '“啪”一声或断裂感；突发锐痛或延迟钝痛；小腿抽筋或无力；跛行；瘀斑肿胀；局部压痛或可摸到缺损；伸膝位被动背伸或抗阻跖屈痛；跑、跳、单腿跳受限'),
         ('② 早期手术指征', '完全或严重断裂；大血肿；骨筋膜室综合征'),
         ('③ 辅助治疗', '干针；非甾体抗炎药/对乙酰氨基酚；富血小板血浆、糖皮质激素、透明质酸注射；增生疗法；小牛血去蛋白提取物；复方草本顺势疗法制剂（原文对多数不推荐，见正文）')]
yy = 10
for t, c in notes:
    nd.text((30, yy), t, font=font(30), fill=TEAL); yy = para(nd, 30, yy + 44, c, 26, 1340, INK, 8) + 20
im = vstack([im, nt.crop((0, 0, W, yy))], W)
save(titled(im, '诊疗流程（按原文图 6 重绘）'), 9)

# 封面
c = raw(26).resize((900, round(441 * 900 / 1198))); c.crop((0, 0, 900, 330)).resize((900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
