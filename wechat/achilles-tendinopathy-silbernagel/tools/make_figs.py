#!/usr/bin/env python3
"""Silbernagel 等 2020 跟腱病保守治疗：首图中文标题卡；原文图 2（肌腱健康四维度）、图 5（疼痛监测模型）按原图重绘为中文；
四期负荷方案卡、活动分级卡、回场排程示例为编者绘制；原文图 1、3、4、6 加中文标注（图 4 超声英文标注、图 6 箭头说明改为中文）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); YL = (253, 246, 210)
doc = pymupdf.open(PDF)
X = {1: 2, 3: 10, 4: 11, 6: 30}


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def fig(n, W):
    im = Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB'); s = im.width / 600
    d = ImageDraw.Draw(im)
    if n == 4:
        for box, (x, y), t in [((265, 15, 425, 48), (285, 17), '跟腱'), ((35, 105, 150, 138), (45, 108), '跟骨'),
                               ((270, 294, 430, 328), (300, 296), '跟腱'), ((0, 350, 110, 382), (10, 352), '跟骨')]:
            d.rectangle(tuple(int(v * s) for v in box), fill=(15, 15, 15))
            d.text((int(x * s), int(y * s)), t, font=font(int(24 * s)), fill='white')
        d.rectangle(tuple(int(v * s) for v in (412, 498, 598, 590)), fill='white', outline='black', width=max(1, int(s)))
        for i, t in enumerate(['肌腱厚度测量：', '组内相关系数 0.898', '测量标准误 0.01 cm', '最小可测变化 0.03 cm']):
            d.text((int(436 * s), int((502 + i * 21) * s)), t, font=font(int(16 * s)), fill=INK)
        d.text((int(418 * s), int(568 * s)), 'C', font=font(int(20 * s)), fill=INK)
    if n == 6:
        for b0 in [(348, 222, 382, 292), (442, 476, 466, 500), (560, 98, 578, 130)]:
            b1 = tuple(int(v * s) for v in b0); im.paste(im.crop(b1).filter(ImageFilter.GaussianBlur(8 * s)), b1[:2])
        bb = tuple(int(v * s) for v in (455, 720, 585, 795))
        im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(14 * s)), bb[:2])
        d.text((int(470 * s), int(735 * s)), '快速完成', font=font(int(26 * s)), fill='black')
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200, maxh=1400):
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


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床述评 · 《运动防护杂志》（Journal of Athletic Training）2020', font=font(30), fill=TEAL)
for i, t in enumerate(['跟腱病保守治疗：', '疼痛监测 + 四期负荷 + 回场排程']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '提踵是主角 · 疼痛不超过 5 分 · 重活之后歇 3 天', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Silbernagel KG, Hanlon S, Sprague A. J Athl Train 2020;55(5):438-447', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(board([tile(1, '触诊：A 跟腱中段（跟骨附着点上方 2～6 厘米）；B 止点；C 内外侧脂肪垫和滑囊。前方压痛比跟腱本身更明显时，要考虑后踝撞击或三角骨综合征')], '查体：按哪里痛'), 2)

# 图 2 重绘
W, H = 1200, 1000; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im, 'RGBA')
cx, cy, R, r = 600, 500, 250, 210
cs = {'up': (0, -R), 'left': (-R, 0), 'right': (R, 0), 'down': (0, R)}
cols = {'up': (150, 150, 150, 110), 'left': (90, 90, 90, 110), 'right': (200, 200, 200, 110), 'down': (120, 120, 120, 110)}
for k, (dx, dy) in cs.items(): dr.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=cols[k])
dr.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill='white', outline=INK, width=3)
ctext(dr, cx, cy - 60, '肌腱', font(58), INK); ctext(dr, cx, cy + 10, '健康', font(58), INK)
txt = {'up': ('症状', ['疼痛', '僵硬', '患者自评量表']), 'left': ('结构', ['形态', '力学特性']), 'right': ('功能', ['小腿肌表现', '跳跃', '跑步', '患者自评量表']), 'down': ('心理', ['运动恐惧', '疼痛灾难化'])}
pos = {'up': (cx, cy - R - 150), 'left': (cx - R - 70, cy - 90), 'right': (cx + R + 70, cy - 120), 'down': (cx, cy + R + 10)}
for k, (t, items) in txt.items():
    x, y = pos[k]; ctext(dr, x, y, t, font(40), TEAL)
    for i, it in enumerate(items): ctext(dr, x, y + 56 + i * 40, it, font(30), INK)
save(titled(im, '肌腱健康的四个维度（按原文图 2 重绘）'), 3)

save(board([tile(3, '提踵耐力测试：A 起始位（踝背伸 0° 或 10°，标准化），B 最高位。伸膝、手指扶墙保持平衡，节拍器每分钟 30 次，做到力竭；记录次数、最大高度和总做功'),
            tile(4, '超声：A 中段型、B 止点型跟腱病，在症状部位和未受累部位测肌腱厚度（实线）；C 厚度测量的信度数据（标注已改为中文）')], '评估：耐力测试与超声'), 4)

# 图 5 疼痛监测模型重绘
W, H = 1300, 820; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
ctext(dr, W / 2, 20, '数字疼痛评分（0～10）', font(36), INK)
x0, x1, y0, y1 = 80, 1220, 90, 250; sc = (x1 - x0) / 10
for a, b_, c, t in [(0, 2, (110, 180, 90), '安全区'), (2, 5, (245, 225, 70), '可接受区'), (5, 10, (215, 60, 50), '高风险区')]:
    dr.rectangle([x0 + a * sc, y0, x0 + b_ * sc, y1], fill=c); ctext(dr, x0 + (a + b_) / 2 * sc, y0 + 58, t, font(36), 'white' if a == 5 else INK)
for v in (0, 2, 5, 10): ctext(dr, x0 + v * sc, y1 + 10, str(v), font(32), INK)
dr.text((x0 - 40, y1 + 52), '不痛', font=font(28), fill=GREY); dr.text((x1 - 170, y1 + 52), '能想象的最痛', font=font(28), fill=GREY)
rules = ['训练中，疼痛最多到 5 分', '训练结束后，疼痛最多到 5 分', '第二天早上，疼痛不超过 5 分', '疼痛和僵硬不能一周比一周加重']
for i, t in enumerate(rules):
    y = 370 + i * 100
    dr.rounded_rectangle([60, y, W - 60, y + 80], 12, fill=LT if i < 3 else PK)
    dr.ellipse([80, y + 14, 132, y + 66], fill=TEAL); ctext(dr, 106, y + 20, str(i + 1), font(32), 'white')
    dr.text((160, y + 20), t, font=font(34), fill=INK)
save(titled(im, '疼痛监测模型（按原文图 5 重绘，原图经授权转载自 Silbernagel 与 Crossley 2015）'), 5)

# 四期
W = 1400; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im)
ph = [('① 症状管理与减负荷期', '第 1～2 周', LT, '所有活动都痛，单腿提踵做不到 10 次',
       '负荷逐步加到 100% 体重，慢速、可控；需要时先水中、减重或等长跖屈', '每天 1 次：勾脚踩脚促循环；双腿提踵 3 × 10～15；单腿提踵 3 × 10；离心提踵 3 × 10；坐姿提踵 3 × 10（都在平地）'),
      ('② 恢复期', '第 2～5 周', GR, '运动时痛、晨僵、提踵时痛',
       '加快动作速度；体重方案轻松完成后加外部阻力', '每天 1 次：台阶边双腿提踵 3 × 15；台阶边单腿提踵 3 × 15；台阶边离心提踵 3 × 15；坐姿提踵 3 × 15；快速回弹提踵 3 × 20'),
      ('③ 重建期', '第 3～12 周', OR, '恢复期练习耐受好，止点不痛，晨僵可减可增',
       '继续加外部阻力，按耐受开始增强式训练', '每天练，其中每周 2～3 次加重：台阶边负重单腿提踵 3 × 15；负重离心提踵 3 × 15；坐姿提踵 3 × 15；快速回弹提踵 3 × 20；专项增强式训练'),
      ('④ 重返运动期', '3～6 个月', PK, '症状很少，偶有晨僵，能参加运动',
       '高强度日加入专项的速度和动作模式', '每周 2～3 次维持：台阶边负重单腿提踵 3 × 15；负重离心提踵 3 × 15；快速回弹提踵 3 × 20')]
y = 20
for t, w, bg, st, ld, ex in ph:
    tmp = ImageDraw.Draw(Image.new('RGB', (W, 3000)))
    yy = y + 82
    for lab, txt_, col in [('状态', st, GREY), ('负荷', ld, INK), ('练习', ex, INK)]: yy = para(tmp, 60, yy, f'{lab}：{txt_}', 27, 1290, col, 6) + 8
    h = yy - y + 10
    dr.rounded_rectangle([20, y, W - 20, y + h], 16, fill=bg)
    dr.text((50, y + 18), t, font=font(38), fill=TEAL); dr.text((560, y + 24), w, font=font(32), fill=RED)
    yy = y + 82
    for lab, txt_, col in [('状态', st, GREY), ('负荷', ld, INK), ('练习', ex, INK)]: yy = para(dr, 60, yy, f'{lab}：{txt_}', 27, 1290, col, 6) + 8
    y += h + 20
para(dr, 40, y, '止点型：全程都在平地做，不下台阶，必要时脚跟下垫 1.3～2.5 厘米的木板，减少背伸压迫', 28, 1320, RED); y += 90
save(titled(im.crop((0, 0, W, y)), '四期跟腱负荷方案（根据原文表 2 整理）'), 6)

save(board([tile(6, '常用负荷练习：A 双腿提踵；B 单腿提踵；C 坐姿提踵（膝上负重，练比目鱼肌）；D 离心提踵（双腿踮起、单腿慢放）；E 快速回弹提踵（箭头处已改为中文）')], '提踵的 5 种变化'), 7)

# 活动分级
W, H = 1400, 900; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
heads = ['', '轻', '中', '重']; cols = [None, GR, YL, PK]
rows = [('活动中疼痛', '1～2', '2～3', '4～5'), ('活动后（当时或次日）疼痛', '1～2', '3～4', '5～6'), ('自觉跟腱用力（0～10）', '0～1', '2～4', '5～10'),
        ('之后需要恢复几天', '0（可每天做）', '2 天', '3 天'), ('跑者举例', '走 70 分钟', '平地慢跑 30 分钟', '以伤前 85% 速度跑 20 分钟')]
cw = [420, 320, 320, 320]; xs = [20]
for c in cw[:-1]: xs.append(xs[-1] + c)
for j, h_ in enumerate(heads):
    if j: dr.rectangle([xs[j], 20, xs[j] + cw[j] - 6, 100], fill=cols[j]); ctext(dr, xs[j] + cw[j] / 2, 38, h_, font(40), TEAL)
for i, r_ in enumerate(rows):
    y = 110 + i * 150
    dr.rectangle([20, y, W - 20, y + 140], fill=(247, 247, 247) if i % 2 else 'white')
    para(dr, 40, y + 46, r_[0], 30, 380, INK)
    for j in range(1, 4):
        t = r_[j]; f = font(30 if len(t) > 6 else 38)
        lines = [t] if len(t) <= 9 else [t[:len(t) // 2], t[len(t) // 2:]]
        for k, l in enumerate(lines): ctext(dr, xs[j] + cw[j] / 2, y + 50 - 20 * (len(lines) - 1) + k * 44, l, f, RED if i == 3 else INK)
save(titled(im, '回场期：把每项活动分成轻、中、重（根据原文表 3 整理）'), 8)

# 排程示例
W, H = 1400, 620; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
plan = [('重', PK), ('轻', GR), ('轻', GR), ('轻', GR), ('中', YL), ('轻', GR), ('轻', GR)]
for i, (dname, (lv, c)) in enumerate(zip(days, plan)):
    x = 30 + i * 192
    ctext(dr, x + 90, 30, dname, font(32), GREY)
    dr.rounded_rectangle([x, 80, x + 180, 260], 14, fill=c); ctext(dr, x + 90, 140, lv, font(54), INK)
para(dr, 30, 300, '编者示例：重活动后接 3 个恢复日，中等活动后接 2 个恢复日，恢复日可以做轻活动。原文建议一次排约 3 周，每 3～4 周重新分级、加入新的“重”活动', 28, 1340, INK)
para(dr, 30, 440, '每天记训练日记：疼痛、症状，以及每次活动后的跟腱用力评分，和治疗师、教练一起看', 28, 1340, TEAL)
save(titled(im, '回场排程怎么排（编者示例）'), 9)

c = fig(6, 900); c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
