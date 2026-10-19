#!/usr/bin/env python3
"""Mattacola & Dwyer 2002 踝扭伤与慢性踝关节不稳的康复：首图中文标题卡；原文图 1 韧带标注改为中文；原文图 2 愈合分期按原图重绘；
三阶段总览、DAPRE 进阶说明、平衡训练进阶卡为编者绘制；原文图 3～10 加中文标注（衣服、护具、袜子与墙面文字已模糊）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
# 原文图号 -> xref
X = {1: 11, 3: 17, 4: 18, 5: 26, 6: 27, 7: 31, 8: 39, 9: 43, 10: 47}
# 以宽 600 为基准的模糊区域
BL = {3: [(185, 170, 250, 210), (255, 70, 315, 100)],
      5: [(280, 655, 412, 715)],
      7: [(110, 140, 182, 238), (428, 140, 482, 238)],
      8: [(55, 85, 130, 120), (240, 85, 315, 115), (450, 85, 505, 110), (115, 425, 200, 460), (290, 475, 377, 528), (503, 458, 547, 497), (266, 383, 290, 407), (203, 433, 234, 460)],
      9: [(0, 58, 24, 120), (390, 103, 448, 140)],
      10: [(183, 473, 242, 507), (348, 508, 387, 537), (428, 488, 487, 517), (68, 503, 97, 530), (128, 480, 184, 509), (480, 488, 532, 517)]}
# 图 1 英文标注 -> 中文（以宽 600 为基准：遮盖框，文字位置，文字）
LAB = [((38, 58, 162, 142), (40, 70), '下胫腓\n后韧带'), ((0, 193, 118, 278), (4, 205), '距腓\n后韧带'),
       ((393, 88, 522, 198), (400, 100), '距腓前\n韧带\n（拉长）'), ((212, 486, 432, 542), (225, 495), '跟腓韧带（拉长）'),
       ((38, 638, 162, 717), (40, 650), '下胫腓\n后韧带'), ((0, 768, 118, 852), (4, 780), '距腓\n后韧带'),
       ((386, 666, 532, 777), (395, 670), '距腓前\n韧带\n（部分撕裂）'), ((203, 1063, 437, 1122), (220, 1072), '跟腓韧带（拉长）'),
       ((18, 1190, 167, 1299), (22, 1195), '下胫腓\n后韧带\n（部分撕裂）'), ((0, 1348, 142, 1457), (4, 1355), '距腓\n后韧带\n（部分撕裂）'),
       ((408, 1248, 532, 1354), (412, 1255), '距腓前\n韧带\n（断裂）'), ((222, 1638, 447, 1697), (235, 1648), '跟腓韧带（断裂）')]


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def raw(n):
    return Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB')


def fig(n, W):
    im = raw(n); s = im.width / 600
    for b in BL.get(n, []):
        bb = tuple(int(v * s) for v in b)
        im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(12 * s)), bb[:2])
    if n == 1:
        d = ImageDraw.Draw(im)
        for box, (x, y), t in LAB:
            d.rectangle(tuple(int(v * s) for v in box), fill='white')
            d.multiline_text((int(x * s), int(y * s)), t, font=font(int(25 * s)), fill=INK, spacing=int(4 * s))
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200, maxh=900, fw=None):
    im = fig(n, fw or W)
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


def board(items, title, W=1200, maxh=900):
    tiles = [tile(n, c, W, maxh) for n, c in items]
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
dr.text((70, 60), '综述 · 《运动防护杂志》（Journal of Athletic Training）2002', font=font(32), fill=TEAL)
for i, t in enumerate(['崴脚之后怎么练？', '急性扭伤与慢性不稳的三阶段康复']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '活动度 → 力量 → 本体感觉与平衡 → 回到运动', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Mattacola CG, Dwyer MK. J Athl Train 2002;37(4):413-429', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 图 1 ----------
save(board([(1, '踝扭伤三度：A Ⅰ度，距腓前韧带、跟腓韧带拉长；B Ⅱ度，距腓前韧带部分撕裂、跟腓韧带拉长；C Ⅲ度，距腓前韧带、跟腓韧带断裂，距腓后韧带和下胫腓韧带部分撕裂（标注已改为中文）')],
           '踝扭伤怎么分度', maxh=1700), 2)

# ---------- 图 2 重绘 ----------
fig2, ax = plt.subplots(figsize=(12, 4.2), dpi=110)
bars = [('炎症反应', 1, 15, '#c0504d'), ('炎症期', 1, 5.5, '#e8a06b'), ('增生期', 5, 21, '#4f9a8f'), ('成熟期', 20, 45, '#2f6f9f')]
for i, (t, a, b_, c) in enumerate(bars):
    y = len(bars) - i
    ax.barh(y, b_ - a, left=a, height=0.55, color=c)
    ax.text(a + 0.3, y, t, va='center', ha='left', color='white', fontsize=15, fontweight='bold')
ax.axvspan(1, 5, color='#fde9d9', alpha=0.6, zorder=0); ax.axvspan(6, 42, color='#e5f1ee', alpha=0.5, zorder=0)
ax.text(3, 4.75, '第 1～5 天：保护', ha='center', fontsize=12, color='#8b3a2f')
ax.text(24, 4.75, '第 6～42 天：在保护下逐步施加应力', ha='center', fontsize=12, color='#2a6f62')
ax.set_xlim(0, 45); ax.set_ylim(0.4, 5.1); ax.set_yticks([])
ax.set_xticks([1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41]); ax.set_xlabel('受伤后天数', fontsize=13)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
plt.tight_layout(); buf = BytesIO(); fig2.savefig(buf, format='png'); plt.close(fig2)
save(titled(Image.open(buf), '组织愈合的三个阶段（按原文图 2 重绘）', 1320), 3)

# ---------- 三阶段总览 ----------
W = 1400; im = Image.new('RGB', (W, 1500), 'white'); dr = ImageDraw.Draw(im)
ph = [('早期功能性康复', '受伤当天开始', LT, '活动度 + 等长/等张力量',
       ['48～72 小时内开始跟腱牵伸（不论能否负重）', '被动活动度、字母操（用脚写大小写字母）', '等长：跖屈、背伸、内翻、外翻，各保持 5～10 秒',
        '等张：弹力带、沙袋或治疗师徒手阻力，强调离心（停 1 秒，4 秒慢慢放）', '卷毛巾、脚趾夹弹珠、提踵、足跟走、足尖走', '两侧都练；腓骨长短肌是重点']),
      ('中期功能性康复', '无痛完全负重后', GR, '本体感觉与平衡',
       ['摇板/平衡盘：顺、逆时针转，先坐后站、先双脚后单脚', '睁眼 → 闭眼；硬地 → 软垫 → 不平或会动的面', '在不同地面上走（硬地、不平地毯、泡沫垫），正常走或脚跟接脚尖',
        '治疗师徒手本体感觉神经肌肉促进（随机扰动）', '可间歇穿戴护踝或矫形鞋垫，提供反馈和支撑']),
      ('后期功能性康复', '行走距离不再受疼痛限制', OR, '回到运动',
       ['摇板上加弹力带阻力或治疗师扰动', '蹦床、泡沫、水中阻力下做功能动作', '走跑交替：50% 走 + 50% 慢跑，每次加约 0.2 km',
        '慢跑 → 跑 → 倒跑 → 图形跑（绕圈、8 字）', '能无痛完成专项动作、达到伤前水平，才算结束'])]
y = 20
for t, w, bg, g, items in ph:
    h = 120 + 46 * len(items) + 16
    dr.rounded_rectangle([20, y, W - 20, y + h], 16, fill=bg)
    dr.text((50, y + 18), t, font=font(40), fill=TEAL); dr.text((480, y + 26), w, font=font(30), fill=RED)
    dr.text((50, y + 78), '重点：' + g, font=font(28), fill=GREY)
    for i, it in enumerate(items): dr.text((60, y + 126 + 46 * i), '· ' + it, font=font(28), fill=INK)
    y += h + 20
save(titled(im.crop((0, 0, W, y)), '三阶段功能性康复（编者根据原文整理）'), 4)

# ---------- 原文图 3～7 ----------
save(board([(3, '训练时可间歇穿戴护踝，提供稳定和感觉反馈'), (4, '跟腱牵伸：A 负重位，B 非负重位（毛巾拉脚）')], '早期①　护踝与跟腱牵伸'), 5)
save(board([(5, '治疗师徒手阻力，在无痛范围内做：A 跖屈与背伸，B 外翻，C 内翻'),
            (6, '徒手扰动：治疗师突然把踝推向内翻和跖屈，运动员要迅速用力抵抗，并把踝带向背伸、外翻')], '早期②　徒手阻力与扰动', maxh=1500), 6)

# ---------- DAPRE ----------
W, H = 1400, 760; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.text((40, 20), '每级 4 组 × 10 次，每组重量递增（以第 2 级为例）', font=font(32), fill=TEAL)
for i, (s, w) in enumerate([('第 1 组', '1 磅'), ('第 2 组', '1.5 磅'), ('第 3 组', '2 磅'), ('第 4 组', '3 磅')]):
    x = 40 + i * 335; hh = 90 + i * 60
    dr.rounded_rectangle([x, 400 - hh, x + 300, 400], 12, fill=(int(225 - 40 * i), int(240 - 30 * i), int(243 - 20 * i)))
    ctext(dr, x + 150, 400 - hh + 20, w, font(40), INK); ctext(dr, x + 150, 415, s + ' · 10 次', font(28), GREY)
dr.rounded_rectangle([40, 480, W - 40, 600], 14, fill=PK)
para(dr, 70, 500, '升级规则：第 4 组能以正确动作完成 10 次，下一次就换到下一级（共 17 级，第 1 组从 0 磅一直到 32.5 磅）', 30, 1260, INK)
dr.text((40, 630), '每次：向心 → 停 1 秒 → 4 秒慢慢离心放回', font=font(30), fill=RED)
dr.text((40, 685), '没时间做徒手阻力时，作者更推荐用重量，而不是弹力带', font=font(28), fill=GREY)
save(titled(im, '每日调整渐进抗阻（DAPRE）怎么用'), 7)

save(board([(7, '足跟走（A）和足尖走（B）：既可作为负重和平衡能力的粗略检查，也是中期练习')], '早期③　足跟走与足尖走'), 8)

# ---------- 平衡进阶 ----------
W, H = 1400, 560; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
steps = [('非负重', '负重'), ('双脚', '单脚'), ('睁眼', '闭眼'), ('硬地', '软垫'), ('软垫', '不平/会动的面'), ('静止', '加扰动')]
for i, (a, b_) in enumerate(steps):
    y = 30 + i * 84
    dr.rounded_rectangle([60, y, 420, y + 66], 12, fill=LT); ctext(dr, 240, y + 14, a, font(32), TEAL)
    dr.line([440, y + 33, 600, y + 33], fill=RED, width=6); dr.polygon([(600, y + 18), (630, y + 33), (600, y + 48)], fill=RED)
    dr.rounded_rectangle([650, y, 1010, y + 66], 12, fill=OR); ctext(dr, 830, y + 14, b_, font(32), RED)
para(dr, 1040, 40, '一次只改一个条件', 32, 330, TEAL)
para(dr, 1040, 110, '常见错误：速度和强度没有变化。练平衡也要变快、变慢、加干扰', 26, 330, GREY, 8)
save(titled(im, '平衡训练怎么一步步加难度'), 9)

save(board([(8, '平衡练习：A、B 换不同支撑面，C 睁眼或闭眼，D 主动动作制造扰动（另一侧腿拉弹力带），E 外部扰动（治疗师推）')], '中期①　平衡训练', maxh=1400), 10)
save(board([(9, 'A、B 后期平衡与功能练习：在动态动作中自己制造扰动（摆腿、伸手够远处）'),
            (10, '水中训练减少关节压力、托住受伤组织：A、B 先无阻力（提踵等），C 再加水流阻力，D 最后做功能动作')], '中后期　动态平衡与水中训练', maxh=1400), 11)

# 封面
c = fig(9, 900); top = 40; c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
