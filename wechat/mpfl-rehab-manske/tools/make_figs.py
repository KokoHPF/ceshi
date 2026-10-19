#!/usr/bin/env python3
"""Manske & Prohaska 2017 内侧髌股韧带重建术后康复（IJSPT 临床述评）：首图中文标题卡；四期康复时间轴、髌骨活动度象限示意、
单腿下台阶评分卡、重返运动标准卡为编者绘制；原文图 1～18 加中文标注（皮肤字母标记、衣服与墙面文字、关节镜放大倍数已模糊）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
# 原文图号 -> xref
X = {1: 7, 2: 17, 3: 18, 4: 22, 5: 23, 6: 24, 7: 25, 8: 29, 9: 30, 10: 37, 11: 38, 12: 53, 13: 57, 14: 58, 15: 59, 16: 60, 17: 64, 18: 65}
# 以宽 600 为基准的模糊区域
BL = {3: [(165, 215, 285, 325)], 4: [(45, 145, 175, 275)], 5: [(15, 0, 95, 32)], 9: [(125, 165, 265, 300)],
      12: [(265, 135, 365, 215), (150, 95, 192, 135)], 13: [(145, 200, 225, 305), (75, 395, 128, 428), (570, 388, 600, 412)], 14: [(210, 90, 378, 180)], 16: [(235, 80, 350, 160), (235, 570, 350, 665)],
      17: [(175, 65, 315, 180), (45, 500, 175, 690), (455, 495, 535, 705)], 15: [(125, 200, 190, 270), (545, 385, 585, 405)], 18: [(210, 90, 330, 180)]}


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def fig(n, W):
    im = Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB')
    s = im.width / 600
    for b in BL.get(n, []):
        bb = tuple(int(v * s) for v in b)
        im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(14 * s)), bb[:2])
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200, maxh=820):
    im = fig(n, W)
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


def board(items, title, W=1200):
    tiles = [tile(n, c, W) for n, c in items]
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
dr.text((70, 60), '临床述评 · 《国际运动物理治疗杂志》（IJSPT）2017', font=font(32), fill=TEAL)
for i, t in enumerate(['髌骨脱位做了 MPFL 重建，', '术后怎么练？四期方案']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '不用支具 · 早期全范围活动 · 20 周左右重返运动', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Manske RC, Prohaska D. Int J Sports Phys Ther 2017;12(3):494-511', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 四期总览 ----------
W, H = 1400, 1500; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
ph = [('第Ⅰ期 保护期', '术后 1 天～6 周', LT,
       '保护移植物、消肿止痛、恢复活动度和髌骨滑动、防止股四头肌抑制',
       '可耐受负重（多数 1 周内全负重）；不用支具；活动度随耐受立即开始；髌骨各方向松动；股四头肌/腘绳肌/臀肌等长、足跟滑动、四方向直腿抬高、踝抗阻；全负重后：提踵、小幅下蹲、上下台阶、平衡',
       '无痛全范围活动；全负重不跛行；疼痛肿胀不加重；髌骨活动 ≥2 象限；能单腿站'),
      ('第Ⅱ期 中度保护期', '第 7～12 周', GR,
       '维持全范围活动、保护移植物、逐步开始功能活动',
       '负重下蹲（加重、平衡板）；弓步（平地 → 不稳定面）；双腿、单腿腿举；弹力带侧向走、单腿桥、提髋；单腿平衡加扰动、抛接球；单腿蹲（镜前 + 口令纠正）',
       '保持前期标准；髋、股四头肌、腘绳肌力量完全恢复'),
      ('第Ⅲ期 最小保护期', '第 13～16 周', OR,
       '逐步回到功能和运动活动',
       '加大下蹲、弓步、腿举的阻力和强度；双腿原地跳、多方向双腿跳；内外侧跳跃；先双腿跳，单腿跳留到下一期',
       '保持前期标准 + 对膝关节有信心'),
      ('第Ⅳ期 重返运动期', '第 17～20 周以后', PK,
       '推进功能活动，全面回到原来的运动',
       '单腿跳（先患腿起跳、健腿落地）；侧滑步、敏捷梯、交叉步；间歇跑步计划',
       '全范围活动、力量完全恢复、功能测试达标（见下文）')]
y = 20
for t, w, bg, g, ex, ms in ph:
    dr.rounded_rectangle([20, y, W - 20, y + 350], 16, fill=bg)
    dr.text((50, y + 20), t, font=font(40), fill=TEAL); dr.text((520, y + 28), w, font=font(32), fill=RED)
    yy = para(dr, 50, y + 86, '目标：' + g, 26, 1290, INK, 8)
    yy = para(dr, 50, yy + 4, '训练：' + ex, 26, 1290, INK, 8)
    para(dr, 50, yy + 4, '进入下期：' + ms, 26, 1290, (40, 110, 60), 8)
    y += 370
save(titled(im, '四期康复方案总览（编者根据原文整理）'), 2)

# ---------- 髌骨活动度象限 ----------
W, H = 1400, 620; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
cx, cy, r = 360, 300, 150
for k in range(4):
    dr.rectangle([cx - 2 * 75 + k * 75, cy - r, cx - 2 * 75 + (k + 1) * 75, cy + r], outline=(150, 170, 180), width=3, fill=(240, 246, 248) if k % 2 else 'white')
dr.ellipse([cx - 150, cy - r, cx + 150, cy + r], outline=TEAL, width=6)
for k in range(1, 4): dr.line([cx - 150 + k * 75, cy - r - 30, cx - 150 + k * 75, cy + r + 30], fill=(160, 160, 160), width=2)
ctext(dr, cx, cy + r + 40, '髌骨宽度 = 4 个象限', font(30))
dr.line([cx + 160, cy, cx + 310, cy], fill=RED, width=6); dr.polygon([(cx + 310, cy - 16), (cx + 340, cy), (cx + 310, cy + 16)], fill=RED)
dr.text((cx + 170, cy - 88), '外推 2 象限', font=font(26), fill=RED); dr.text((cx + 170, cy - 52), '= 半个髌骨', font=font(26), fill=RED)
rows = [('< 1 象限', '活动度过小', '需做髌骨松动'), ('1～3 象限', '正常范围', ''), ('> 3 象限', '活动度过大', ''), ('≈ 2 象限（内、外）', '重建术后目标', '少于 2 象限就要松动')]
for i, (a, b, c) in enumerate(rows):
    yy = 80 + i * 120
    dr.rounded_rectangle([760, yy, 1380, yy + 100], 12, fill=PK if i == 3 else LT)
    dr.text((785, yy + 14), a, font=font(32), fill=RED if i == 3 else TEAL); dr.text((785, yy + 58), b + ('　' + c if c else ''), font=font(26), fill=INK)
dr.text((40, 30), '屈膝 20°～30° 让髌骨进入滑车后，向内、向外推', font=font(28), fill=GREY)
save(titled(im, '髌骨被动活动度：用“象限”来量（编者示意）'), 3)

# ---------- 原文图 ----------
save(board([(1, '膝内侧解剖：镊子挑起的就是内侧髌股韧带，连接髌骨内缘近端一半与股骨内髁（原文经期刊授权转载）')], '内侧髌股韧带在哪里'), 4)
save(board([(2, '检查髌骨被动活动：A 拇指先找髌骨中线，B 向外推看移动多少；重建后目标约 2 个象限'),
            (3, '术前屈膝位髌骨向外移位'), (4, '术前伸膝位髌骨向外移位')], '查体：髌骨被动活动度'), 5)
save(board([(5, '关节镜下所见：髌骨不稳'), (6, '重建的两个切口位置'), (7, '取腘绳肌腱作移植物'),
            (8, '固定后调张力：移植物是“缰绳”，不能把髌骨往内拉'), (9, '术后屈膝 30° 外推髌骨，稳定性良好')], '手术怎么做'), 6)
save(board([(10, '术后髌骨活动度不足 2 象限时，做内外侧滑动松动；活动度不足是手术失败最常见的原因之一'),
            (11, '尽早恢复完全伸膝，防止屈曲挛缩')], '第Ⅰ期：髌骨松动与伸膝'), 7)
save(board([(12, '平衡板上下蹲：力量 + 本体感觉 + 平衡'), (13, '腿举：可控地加大负荷，双腿和单腿都要做'),
            (14, '弹力带侧向走：强化髋外展肌，改善膝关节控制')], '第Ⅱ期①　下蹲、腿举、侧向走'), 8)
save(board([(15, '单腿桥（原文图注误写为“弹力带侧向走”）'), (16, '提髋：A 骨盆下降位，B 骨盆抬起位'),
            (17, '单腿蹲：A 额状面、水平面、矢状面控制差（膝内扣）；B 对镜 + 口令纠正后改善')], '第Ⅱ期②　单腿桥、提髋、单腿蹲'), 9)
save(board([(18, '双腿跳，全程无痛无症状')], '第Ⅲ期：从双腿跳开始'), 10)

# ---------- 单腿下台阶 ----------
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 200], 14, fill=LT)
dr.text((50, 40), '做法', font=font(36), fill=TEAL)
para(dr, 50, 96, '站在 20 cm 台阶边缘，双手叉腰，患腿屈膝下蹲，让对侧脚轻点地面；连续做 5 次，按下面的项目扣分', 30, 1290)
items = [('用手臂保持平衡', 1), ('躯干向内或向外倾', 1), ('骨盆旋转或抬高', 1), ('胫骨结节移到第 2 趾内侧', 1),
         ('单腿站立不稳', 1), ('胫骨结节移到足内缘以内', 2)]
for i, (t, s) in enumerate(items):
    yy = 230 + i * 82
    dr.rounded_rectangle([20, yy, 1000, yy + 70], 10, fill=(245, 245, 245))
    dr.text((50, yy + 16), t, font=font(32), fill=INK); dr.text((900, yy + 14), f'{s} 分', font=font(34), fill=RED)
for i, (a, b, c) in enumerate([('0～1 分', '质量好', GR), ('2～3 分', '质量中等', OR), ('≥4 分', '质量差', PK)]):
    yy = 230 + i * 165
    dr.rounded_rectangle([1030, yy, W - 20, yy + 145], 14, fill=c)
    ctext(dr, 1205, yy + 22, a, font(42), INK); ctext(dr, 1205, yy + 84, b, font(32), TEAL)
dr.text((40, 740), '重返运动要求“质量好”（0～1 分）', font=font(36), fill=RED)
dr.text((40, 800), '该测试评分者间信度良好，能区分髋外展力量较弱、股四头肌柔韧性较差的人', font=font(26), fill=GREY)
save(titled(im, '出院标准之一：单腿下台阶测试'), 11)

# ---------- 跳跃标准 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
for i, (t, m, f) in enumerate([('双腿立定跳远', '≥ 身高的 100%', '≥ 身高的 90%'), ('单腿跳远', '≥ 身高的 90%', '≥ 身高的 80%')]):
    x0 = 20 + i * 690
    dr.rounded_rectangle([x0, 20, x0 + 670, 420], 16, fill=LT)
    ctext(dr, x0 + 335, 50, t, font(42), TEAL)
    dr.text((x0 + 50, 150), '男', font=font(40), fill=INK); dr.text((x0 + 140, 145), m, font=font(48), fill=RED)
    dr.text((x0 + 50, 270), '女', font=font(40), fill=INK); dr.text((x0 + 140, 265), f, font=font(48), fill=RED)
para(dr, 30, 450, '另需：全范围活动、力量完全恢复、单腿下台阶质量好。数值为健康人群常模（原文参考文献 89）', 28, 1340, GREY)
save(titled(im, '重返运动的跳跃标准'), 12)

# 封面
c = fig(12, 900); top = 40; c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
