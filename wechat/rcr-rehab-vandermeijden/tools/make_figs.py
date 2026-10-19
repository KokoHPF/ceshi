#!/usr/bin/env python3
"""Van der Meijden 等 2012 关节镜肩袖修补术后康复：首图中文标题卡；愈合时间轴、两套方案对比卡、四期总览卡为编者绘制；
原文图 1～15 加中文标注（运动内衣标志已模糊）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); YL = (253, 246, 215)
doc = pymupdf.open(PDF)
X = {1: 16, 2: 20, 3: 21, 4: 25, 5: 26, 6: 30, 7: 31, 8: 35, 9: 40, 10: 39, 11: 44, 12: 48, 13: 49, 14: 50, 15: 54}
BL = {3: [(262, 118, 312, 146)]}  # 以宽 400 为基准


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def fig(n, W):
    im = Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB'); s = im.width / 400
    for b in BL.get(n, []):
        bb = tuple(int(v * s) for v in b); im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(8 * s)), bb[:2])
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200, fw=None, maxh=900):
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
dr.text((70, 60), '临床述评 · 《国际运动物理治疗杂志》（IJSPT）2012', font=font(32), fill=TEAL)
for i, t in enumerate(['关节镜肩袖修补术后：', '保守与中等两套方案、四期怎么练']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '按愈合时间表加负荷 · 附逐周训练表', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'van der Meijden OA, Westgard P, Chandler Z, Gaskill TR, Kokmeyer D, Millett PJ.', font=font(26), fill=GREY)
dr.text((70, 480), 'Int J Sports Phys Ther 2012;7(2):197-218', font=font(26), fill=GREY)
dr.text((70, 525), '编者中文重排，仅作学术交流', font=font(24), fill=(150, 150, 150))
save(im, 1)

# 愈合时间轴
W, H = 1400, 610; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
x0, x1 = 60, 1340; sc = (x1 - x0) / 16
def wx(w): return x0 + w * sc
for a, b_, c, t, y in [(0, 1, (230, 120, 100), '炎症期', 60), (0.5, 4, (240, 190, 90), '增生（修复）期', 140), (3, 16, (110, 170, 150), '重塑期', 220)]:
    dr.rounded_rectangle([wx(a), y, wx(b_), y + 60], 10, fill=c)
    if b_ - a < 2: dr.text((wx(b_) + 14, y + 14), t + '（约第 1 周）', font=font(30), fill=c)
    else: dr.text((wx(a) + 12, y + 14), t, font=font(30), fill='white')
dr.line([x0, 310, x1, 310], fill=INK, width=3)
for w in range(0, 17, 2): dr.line([wx(w), 304, wx(w), 316], fill=INK, width=3); ctext(dr, wx(w), 322, str(w), font(26))
ctext(dr, (x0 + x1) / 2, 360, '术后周数', font(28), GREY)
for k, (w, t) in enumerate([(1.4, '约第 10 天：胶原和生长因子达峰'), (6, '第 4～8 周：进入平台期'), (12, '12～16 周起：才达到最大抗拉强度')]):
    yy = 400 + k * 46
    dr.line([wx(w), 318, wx(w), yy + 16], fill=RED, width=2); dr.ellipse([wx(w) - 6, yy + 10, wx(w) + 6, yy + 22], fill=RED)
    dr.text((wx(w) + 14, yy), t, font=font(26), fill=RED) if w < 10 else dr.text((wx(w) - 14 - dr.textlength(t, font=font(26)), yy), t, font=font(26), fill=RED)
para(dr, 60, 548, '腱骨交界处的正常纤维软骨不会再长出来，修复后长成的是瘢痕组织', 26, 1300, GREY)
save(titled(im, '肩袖修补后的愈合时间表（编者根据原文绘制）'), 2)

# 两套方案
W = 1400; im = Image.new('RGB', (W, 820), 'white'); dr = ImageDraw.Draw(im)
for k, (t, c, tc, who, items) in enumerate([
        ('中等方案', GR, TEAL, '较年轻、组织质量好、撕裂小', ['术后第 1 天开始被动活动（可耐受疼痛）', '被动前屈、外旋、外展：不限', '内旋：到肚子', '吊带 5～6 周', '5～6 周开始全范围主动活动', '弹力袜 2 周防血栓']),
        ('保守方案', OR, RED, '高龄、大撕裂、组织质量差', ['术后 10～14 天不做被动活动', '第 3 周：前屈 ≤120°、外旋 ≤30°、外展 ≤90°', '内旋：到肚子', '吊带 6～7 周', '6～7 周开始全范围主动活动', '弹力袜 2 周防血栓'])]):
    x = 20 + k * 690
    dr.rounded_rectangle([x, 20, x + 670, 800], 16, fill=c)
    ctext(dr, x + 335, 40, t, font(44), tc); ctext(dr, x + 335, 110, '适合：' + who, font(28), GREY)
    for i, it in enumerate(items): para(dr, x + 40, 190 + i * 98, '· ' + it, 30, 600, INK, 8)
save(titled(im, '先选方案：中等还是保守（根据原文附录整理）'), 3)

# 四期总览
W = 1400; im = Image.new('RGB', (W, 2600), 'white'); dr = ImageDraw.Draw(im)
ph = [('第Ⅰ期 最大保护', '约第 1～4 周', LT, ['外展吊带固定，护住修补处、改善血供', '治疗师做被动活动：短臂牵引下轻柔摆动，不拉到末端', '肩胛下沉、前伸（每次回到中立位）', '小幅钟摆（直径约 20 厘米）', '颈、肘、腕、手主动活动；冷敷 10～14 天'],
       '被动前屈 ≥125°，肩胛面被动外旋 ≥75°、内旋 ≥75°，外展 ≥90°'),
      ('第Ⅱ期 主动辅助 → 主动', '约第 4～8 周', GR, ['棍子辅助内外旋、健手辅助前屈；桌上推球画圈', '颈深水池中慢速主动活动', '俯卧肩胛后缩、下沉；仰卧肩胛前伸', '侧卧外旋、“敬礼”式肩胛面上举 → 满罐', '25% → 50%～75% 力量的等长内外旋；仰卧画圈写字母'],
       '主动活动范围和健侧一样，没有肩胛运动障碍'),
      ('第Ⅲ期 初步抗阻', '约第 8～12 周', OR, ['弹力带内外旋（腋下夹毛巾卷）', '弹力带“熊抱”练前锯肌', '站立弹力带划船、俯卧下斜方肌', '二头肌弯举、三头肌伸展', '四点跪重心转移和扰动'],
       '日常活动不痛，所有第Ⅲ期练习都能无痛完成'),
      ('第Ⅳ期 进阶抗阻', '约第 12～16 周起', PK, ['外展 45° 位弹力带外旋（后侧肩袖）；外展 90° 位外旋', '弹力带出拳加前伸；俯卧撑加前伸（墙 → 桌 → 地）', '“自由女神”位节律稳定；四点跪上下台阶', '治疗师徒手对角线抗阻', '后期：上肢增强式，双手 → 单手，肩高 → 过头'],
       '经术者同意，活动和力量双侧一样，肩胛运动正常，休息和活动都不痛 → 间歇性回场计划')]
y = 20
for t, w, bg, items, ms in ph:
    tmp = ImageDraw.Draw(Image.new('RGB', (W, 2600))); yy = y + 82
    for it in items: yy = para(tmp, 60, yy, '· ' + it, 27, 1290, INK, 6) + 6
    yy = para(tmp, 60, yy + 4, '进入下期：' + ms, 26, 1290, (40, 110, 60), 6)
    h = yy - y + 12
    dr.rounded_rectangle([20, y, W - 20, y + h], 16, fill=bg)
    dr.text((50, y + 18), t, font=font(38), fill=TEAL); dr.text((620, y + 24), w, font=font(32), fill=RED)
    yy = y + 82
    for it in items: yy = para(dr, 60, yy, '· ' + it, 27, 1290, INK, 6) + 6
    para(dr, 60, yy + 4, '进入下期：' + ms, 26, 1290, (40, 110, 60), 6)
    y += h + 20
save(titled(im.crop((0, 0, W, y)), '四期总览（编者根据原文整理）'), 4)

# 原文图
def half(n, cap): return tile(n, cap, 1200, 760)
save(board([tile(1, 'A～D 短臂牵引下、不同旋转角度的轻柔关节摆动，手臂轻度外展，用来减轻疼痛和肌肉保护性紧张'),
            half(2, '治疗师辅助的被动前屈'),
            tile(3, '单独的肩胛下沉（A）和前伸（B），每次回到中立位')], '第Ⅰ期：被动活动与肩胛激活'), 5)
save(board([tile(4, '主动辅助活动：A 用棍子辅助内旋；B 健手辅助前屈'),
            tile(5, '俯卧位激活肩胛周围肌：肩胛后缩、下沉，减少上斜方肌代偿'),
            tile(6, '“敬礼”练习：屈肘的肩胛面上举，A 起始、B 结束，之后可进阶到满罐'),
            tile(7, '开链本体感觉：仰卧，患侧前屈 90°，用小而可控的动作在空中画圈、写字母')], '第Ⅱ期：主动辅助到主动'), 6)
save(board([tile(8, '弹力带“熊抱”：背靠墙站、微屈膝；屈肘 45°、上臂外展 60°、内旋 45°，沿约 60° 高度的弧线水平内收，直到双拳相碰、肩胛最大前伸'),
            half(9, '站立弹力带划船：练斜方肌和菱形肌'),
            tile(10, '二头肌弯举（哑铃）'),
            half(11, '三头肌伸展（哑铃）')], '第Ⅲ期：初步抗阻'), 7)
save(board([tile(12, '外展 45° 位弹力带外旋（加毛巾卷），强化冈下肌、小圆肌'),
            half(13, '俯卧撑加前伸（四点跪、上下台阶的进阶版）：从推墙 → 桌边 → 地面'),
            half(14, '“自由女神”练习：外旋 90°、肩胛面前屈 90°，抵抗弹力带并快速晃动振动棒'),
            tile(15, '对着回弹网抛球：A 从肩高开始，B 进阶到过头')], '第Ⅳ期：进阶抗阻与增强式'), 8)

c = fig(8, 900); c.crop((0, 60, 900, 443)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
