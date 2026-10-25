#!/usr/bin/env python3
"""Kawabata 等 2025《新型 8 字贴扎治疗业余投手肩关节前向不稳：病例报告》（IJSPT）推文配图。
原文是 CC BY-NC 4.0（允许演绎，禁止商业使用，需署名并注明改动）。
原文图 2、图 3 图内英文已用 paper-figure-zh（tools/fig-translate/figtrans.py，位图路线）译成中文，
图 3A 的带描边标签为编者手工擦除后重写（src/fig2_zh.jpg、src/fig3_zh.jpg）；
原文图 1、4、5 图内只有分图字母和超声缩写，原样引用；原文图 6 柱状图按原文数据重画成中文；
首图、病例时间线、贴扎步骤卡、临床要点卡和封面为编者绘制。
用法：python3 make_figs.py <src 目录> <输出目录> <中文字体>"""
import re
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50); ORG = (215, 120, 20)
GRN = (0, 120, 60); PUR = (110, 70, 190)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)


def raw(name):
    return Image.open(f'{SRC}/{name}').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    # 英文单词、数字整体换行；标点不放行首
    for tok in re.findall(r"[A-Za-z0-9.%\-+/]+|.", t):
        if line and dr.textlength(line + tok, font=font(fs)) > w and tok not in '，。；：、）”°':
            dr.text((x, y), line.rstrip(), font=font(fs), fill=fill); y += fs + gap; line = tok.lstrip()
        else: line += tok
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    """原图等比缩放后放在下方，中文图注放在图外上方的色条里"""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t


def card(W, title, blocks, numbered=False):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 6000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100; tx = 110 if numbered else 50
    for k, (h, t, c, a) in enumerate(blocks):
        top = y; dd = ImageDraw.Draw(Image.new('RGB', (W, 6000)))
        y2 = y + 62
        for seg in t.split('\n'): y2 = para(dd, tx, y2, seg, 28, W - tx - 50, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        if numbered:
            dr.ellipse([36, top + 14, 88, top + 66], fill=a); dr.text((62, top + 40), str(k + 1), font=font(30), fill='white', anchor='mm')
        else:
            dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((tx, top + 18), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, tx, yy, seg, 28, W - tx - 50, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


def timeline():
    """病例经过：从初诊到 8 个月"""
    W = 1200; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '病例经过（编者根据原文整理）', font=font(36), fill='white')
    ev = [
        ('初诊前', '41 岁右利手男性，前全国级别半职业投手。肩痛逐渐加重，已 6 年不能投球，近 1 个月明显加重、影响日常生活；'
                   '肩袖间隙注射激素＋局麻后活动痛仍在', GREY, (242, 242, 242)),
        ('初诊查体', '投球痛 NRS 10/10，外旋痛 8～9/10；外旋肌力 2/5；超声见外旋末端肱骨头前移 4.43 mm，'
                    'Bennett 病损周围多普勒血流信号；复位试验让肱骨头后移 2.31 mm，外旋痛完全消失', RED, PK),
        ('当次贴扎后', '外旋肌力接近 5/5；外旋发力和“出手位推”时疼痛降到 NRS 1～3/10；空手投球（后期举臂、最大外旋、出手）不痛，'
                      '能顺畅扔网球。同时教了家庭训练和投球动作纠正', TEAL, LT),
        ('当天回家后', '患者自述贴着胶布从 18.44 米（正式投手距离）以约 85% 力量投球——研究者没有亲眼看到', ORG, OR),
        ('4 个月（邮件）', '回到比赛，最快球速 115 km/h，投球痛 NRS 3/10；QuickDASH 功能障碍/症状 0、工作 0、运动模块 25', GRN, GR),
        ('8 个月', '仍在业余投球，坚持家庭训练；QuickDASH 功能障碍/症状 0、工作 0、运动模块 18.8', PUR, PU),
    ]
    y = 110; lx = 230
    dr.line([lx, y + 20, lx, 2000], fill=(215, 215, 215), width=4)
    for h, t, a, c in ev:
        dd = ImageDraw.Draw(Image.new('RGB', (W, 2000)))
        y2 = para(dd, lx + 50, y + 18, t, 26, W - lx - 90, gap=12)
        dr.rounded_rectangle([lx + 30, y, W - 20, y2 + 6], 12, fill=c)
        para(dr, lx + 50, y + 18, t, 26, W - lx - 90, gap=12)
        dr.ellipse([lx - 12, y + 18, lx + 12, y + 42], fill=a)
        dr.text((lx - 28, y + 30), h, font=font(26), fill=a, anchor='rm')
        y = y2 + 30
    im = im.crop((0, 0, W, y)); dr = ImageDraw.Draw(im)
    dr.rectangle([lx - 2, y - 30, lx + 2, y], fill='white')
    # 竖线超出最后一个节点的部分盖掉
    return im


def steps():
    return card(1200, '8 字贴扎怎么贴（编者根据原文方法与图 3 整理）', [
        ('材料与体位', '5 cm 宽肌内效贴（原文用 KILO TAPE），拉伸到原长的 1.1～1.3 倍。'
                      '患者躯干前倾、患臂自然下垂（钟摆位）。共两条，叠着贴，彼此稍错开一点', LT, TEAL),
        ('起点：喙突 → 肱骨头前方', '从喙突处锚定，向外下经过肱骨头前方（肱骨头中心是“8”字的交叉点）', OR, ORG),
        ('横绕上臂后方', '水平绕过上臂近端后侧', GR, GRN),
        ('向上拉到肩峰前方', '再向头侧提拉，经过肱骨头中心拉向肩峰前方', PU, PUR),
        ('止于肩胛冈', '越过肩峰，固定在肩胛冈上', PK, RED),
        ('回到中立位', '手臂从钟摆位回到自然下垂位时，向上那一段胶布张力增加，'
                    '原文认为这能增强盂肱关节的前方稳定。原文附有操作视频', LT, TEAL),
    ], numbered=True)


def results():
    """原文图 6：干预前、4 个月、8 个月"""
    W = 1200; H = 760; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '疼痛和功能随时间的变化（编者按原文图 6 重画）', font=font(36), fill='white')
    cols = [((40, 40, 40), '干预前'), ((140, 140, 140), '4 个月'), ((120, 190, 200), '8 个月')]
    x0 = 40
    for c, t in cols:
        dr.rectangle([x0, 108, x0 + 28, 134], fill=c); dr.text((x0 + 38, 104), t, font=font(26), fill=INK); x0 += 190
    groups = [('QuickDASH\n功能障碍/症状', [11.4, 0, 0], 100), ('QuickDASH\n运动模块', [50, 25, 18.8], 100), ('投球时疼痛\nNRS 0～10', [10, 3, 3], 10)]
    top, bot = 200, 560; gw = (W - 80) / 3
    dr.line([40, bot, W - 40, bot], fill=GREY, width=2)
    for k, (name, vals, vmax) in enumerate(groups):
        L = 40 + k * gw; bw = 70; gap = 20; start = L + (gw - 3 * bw - 2 * gap) / 2
        for i, v in enumerate(vals):
            x = start + i * (bw + gap); h = (bot - top) * v / vmax
            dr.rectangle([x, bot - h, x + bw, bot], fill=cols[i][0])
            lab = f'{v:g}' + ('*' if k == 2 and i == 2 else '')
            dr.text((x + bw / 2, bot - h - 8), lab, font=font(24), fill=INK, anchor='md')
        dr.multiline_text((L + gw / 2, bot + 14), name, font=font(26), fill=INK, anchor='ma', align='center', spacing=6)
    para(dr, 30, bot + 100, 'QuickDASH 两个模块满分 100，越低越好；NRS 越低越好。*8 个月的投球疼痛正文没写，原文图 6 画的是 3（图中按 ×10 画成 30）；'
         '4 个月和 8 个月的数据都是患者通过邮件自报。', 24, W - 60, fill=GREY)
    return im


# 1 首图
W, H = 1400, 720; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '病例报告 · 《IJSPT》2025 · 证据等级 5', font=font(30), fill=TEAL)
dr.text((70, 125), '新型 8 字贴扎治疗', font=font(50), fill=INK)
dr.text((70, 195), '业余投手的肩关节前向不稳', font=font(46), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Kawabata M, Miyata T, Miyatake K.', font=font(26), fill=GREY)
dr.text((70, 375), 'Int J Sports Phys Ther. 2025;20(5):741-748. doi:10.26603/001c.136406', font=font(26), fill=GREY)
dr.text((70, 420), '日本北里大学保健医疗学部康复学系；相模原协同医院康复中心；横滨市立大学骨科', font=font(26), fill=GREY)
dr.text((70, 600), '编者中文解读 · 原文 CC BY-NC 4.0，图 2、图 3 图内文字由编者译为中文', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(timeline(), 2)
save(capbox(raw('fig1.jpg'), '原文图 1  抗阻外旋测试和疼痛部位超声。A：外展 45° 外旋（小圆肌）；B：中立位外旋（冈下肌），蓝箭头为检查者施力方向；'
                             'C：后方关节盂到冈下肌深层血流增多，白箭头为超声下按压的痛点。G 关节盂，HH 肱骨头，PD 三角肌后部，ISP 冈下肌'), 3)
save(capbox(raw('fig2_zh.jpg'), '原文图 2（图内文字编者译）  中立位外旋时后方肩的动态超声。A：自然外旋时肩前后都痛，末端肱骨头明显前移；'
                                'B：检查者用手把肱骨头往后推（复位），外旋痛明显减轻。D 为距离'), 4)
save(capbox(raw('fig3_zh.jpg'), '原文图 3（图内文字编者译）  新型 8 字贴扎。A：在患者身上的走向；a～e：在肩关节模型上的分步演示，'
                                'a 喙突起贴经肱骨头前方，b 横绕上臂后方，c 向上拉向肩峰前方，d 固定于肩胛冈，e 从钟摆位回到自然下垂位后向上的胶布绷紧'), 5)
save(steps(), 6)
save(capbox(raw('fig4.jpg'), '原文图 4  贴扎后外旋发力和空手投球不再疼痛。a：外展 45° 外旋；b：外展 90° 外旋；c：出手位；'
                             'e～g：空手投球的后期举臂、最大外旋和出手（原文分图编号从 c 直接跳到 e）'), 7)
save(capbox(raw('fig5.jpg'), '原文图 5  患者自述的投球变化。a：出手时手指“发力加速”的感觉回来了，恐惧感减少，挥臂顺畅；'
                             'b：贴扎前，因为肩前向不稳，投球时手向后引的动作总是慢半拍', W=1000), 8)
save(results(), 9)

save(card(1200, '落到临床（编者整理）', [
    ('先用复位试验“试药”', '恐惧试验/外旋诱发疼痛时，用手把肱骨头往后推，疼痛明显减轻，说明“把肱骨头摆正”这条路可能有效，'
                         '这时再考虑用贴扎替代手的作用', LT, TEAL),
    ('贴扎要点', '5 cm 肌内效贴，拉伸 1.1～1.3 倍，两条错开叠贴；躯干前倾钟摆位贴，喙突 → 肱骨头前 → 上臂后 → 肩峰前 → 肩胛冈；'
               '贴完回到中立位再检查外旋痛和肌力', GR, GRN),
    ('贴扎是“窗口”，训练才是正事', '本例同时教了无负荷三平面旋转训练（保持肱骨头居中）和投球动作纠正（举臂期别让肩往前冲），'
                              '患者 8 个月一直坚持。改善里贴扎和训练各占多少，分不开', OR, ORG),
    ('只有 1 个人', '证据等级 5，随访靠邮件自报，没有复查超声和肌力，不能证明贴扎“稳住了肱骨头”', PK, RED),
    ('别耽误手术评估', '有明确脱位史、骨性缺损或大的盂唇损伤，该看骨科就看骨科（编者补充）；原文也说贴扎适合介于手术和保守之间的“边缘”病例', PU, PUR),
]), 10)

# 封面：纯文字
W, H = 900, 383; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, H], fill=TEAL)
dr.text((50, 46), '病例报告 · IJSPT 2025', font=font(26), fill=TEAL)
dr.text((50, 118), '投手肩前向不稳', font=font(58), fill=INK)
dr.text((50, 198), '一次 8 字贴扎能管多久？', font=font(46), fill=INK)
dr.text((50, 290), '肌内效贴 · 肩关节不稳 · 投球 · 1 例', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
