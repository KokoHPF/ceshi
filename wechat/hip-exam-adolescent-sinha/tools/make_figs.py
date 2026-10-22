#!/usr/bin/env python3
"""Sinha 等 2024 JPOSNA 青少年及青年髋痛的临床评估：首图为原题直译标题卡；
原文图 1～10 直接用原图照片（照片内无英文），英文图注译成中文放在照片下方；
问诊定位卡、查体流程卡、特殊检查敏感度/特异度图和临床卡为编者根据原文正文和表 1、表 2 整理。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
Z = 4
K, G, R = (0, 0, 0), (94, 94, 94), (255, 38, 0)
doc = pymupdf.open(PDF)
PUNC = '，。；、：）”'


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=90)


def titled(im, t, W=1200):
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30 and ch not in PUNC:
            k = len(line)
            while ch.isascii() and ch.isalnum() and k and line[k - 1].isascii() and line[k - 1].isalnum(): k -= 1
            if not k: k = len(line)
            lines.append(line[:k]); line = line[k:] + ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in PUNC: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def phases(title, S, n, fs=24):
    W = 1200; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im); y = 20
    for t, bg, c, items in S:
        h = 66 + sum(para_h(s, fs, 1030 - fs * 1.1, gap=8) + 10 for s in items)
        dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
        yy = y + 62
        for s in items: yy = bullet(dr, 70, yy, s, fs, 1060, gap=8) + 10
        y += h + 16
    save(titled(im.crop((0, 0, W, y)), title), n)


import io

# 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '最新概念综述 · J Pediatr Orthop Soc North Am 2024', font=font(32), fill=TEAL)
dr.text((70, 140), '青少年及青年髋痛的临床评估', font=font(58), fill=INK)
dr.text((70, 270), 'Clinical evaluation of the painful adolescent and young adult hip', font=font(30), fill=GREY)
dr.line([70, 360, W - 70, 360], fill=(200, 205, 210), width=2)
dr.text((70, 395), 'Sinha R, Ellis HB, Podeszwa DA, Sucato DJ, Morris WZ.', font=font(30), fill=GREY)
dr.text((70, 439), 'J Pediatr Soc North Am. 2024;7:100043. doi:10.1016/j.jposna.2024.100043', font=font(30), fill=GREY)
dr.text((70, 500), '美国得克萨斯州达拉斯 Scottish Rite for Children · 得克萨斯大学西南医学中心', font=font(26), fill=GREY)
dr.text((70, 600), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1～10：照片取自原文，图注译成中文
F_ZH = {1: (4, '原文图 1　左髋正常、右髋外展肌无力的患者。单腿站立时应能保持骨盆水平（左）；支撑腿髋外展肌无力时，对侧半骨盆向下掉，和/或躯干代偿性地向患侧倾斜，即 Trendelenburg 征阳性（右）'),
        2: (6, '原文图 2　直腿抬高试验（SLR）。沿下肢按皮节分布的放射痛提示脊柱病变'),
        3: (11, '原文图 3　髋内旋（左）和外旋（右）'),
        4: (13, '原文图 4　屈髋时，髋正常应能保持中立位（左）；出现强制性外旋时，屈髋会迫使髋倒向外旋，需警惕股骨头骨骺滑脱（SCFE）（右）'),
        5: (18, '原文图 5　屈髋、内收、内旋（FADIR），阳性提示股骨髋臼撞击（FAI）'),
        6: (20, '原文图 6　前方恐惧试验。对侧髋屈曲，患侧髋被动后伸并外旋，使前方关节囊和盂唇受力；出现疼痛或恐惧感为不稳阳性'),
        7: (25, '原文图 7　俯卧恐惧复位试验（PART）。患侧髋后伸 10°～15°、外展 10°，膝屈曲托住；向前推股骨诱发疼痛（左），松开压力后疼痛缓解（右）'),
        8: (27, '原文图 8　外展-后伸-外旋试验。患侧髋外展 30°、后伸、外旋；出现前方腹股沟痛或恐惧感提示前方不稳'),
        9: (32, '原文图 9　内源性弹响髋的检查。患侧髋从屈曲、外展、外旋位（FABER，左）移到后伸、内收、内旋位（EADIR，右）；再现弹响感提示弹响髋'),
        10: (34, '原文图 10　Ober 试验。髋外旋、外展后让其缓慢落向内收；内收不受限为髂胫束正常（左），内收受限为 Ober 试验阳性，提示髂胫束紧张（右）')}


def row(nums, title, n):
    gap = 15; tw = (1200 - gap) // 2 if len(nums) == 2 else 1200; tiles = []
    for k in nums:
        x, t = F_ZH[k]; ph = Image.open(io.BytesIO(doc.extract_image(x)['image'])).convert('RGB')
        ph = ph.resize((tw, round(ph.height * tw / ph.width)), Image.LANCZOS); tiles.append((ph, t))
    hh = max(ph.height for ph, _ in tiles); ch = max(para_h(t, 26, tw - 24, gap=8) for _, t in tiles)
    im = Image.new('RGB', (1200, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im)
    for i, (ph, t) in enumerate(tiles):
        x = i * (tw + gap); im.paste(ph, (x, hh - ph.height))
        dr.rectangle([x, hh, x + tw, hh + ch + 20], fill=(232, 232, 232)); para(dr, x + 12, hh + 12, t, 26, tw - 24, gap=8)
    save(titled(im, title), n)


phases('问诊：疼痛在哪、怎么起病（编者根据原文整理）', [
    ('起病方式', LT, TEAL, ['急性外伤：踢球、起跳等突然离心收缩后发作，接近骨骼成熟的青少年多见骨突撕脱骨折',
        '大腿、膝或髋轻痛，轻度跛行，足外展角逐渐变大，再突然剧痛不能走：高度怀疑股骨头骨骺滑脱（SCFE）', '隐匿起病：多见于撞击、髋臼发育不良和骨突炎']),
    ('疼痛部位', OR, (170, 90, 30), ['前方腹股沟：关节内（撞击、软骨盂唇损伤）或关节外（髂腰肌拉伤、肌腱炎）',
        '腹股沟周围“C 字形”分布：提示关节内病变', '大转子近端外侧痛：外展肌疲劳，常见于髋臼发育不良；正好压在大转子上：转子滑囊炎',
        'AIIS、ASIS、髂嵴等骨突压痛：骨突撕脱骨折或骨突炎']),
    ('弹响与卡顿', PU, (90, 60, 150), ['看得见的弹响，伴“要脱位”的感觉：外源性弹响髋（髂胫束滑过大转子）',
        '听得见的弹响，伴“卡住”感：内源性弹响髋（髂腰肌滑过髂耻隆起）', '间歇性“咔哒”或卡顿：多为关节内来源，但不特异']),
    ('机械性髋问题的共同信号', PK, RED, ['活动后加重、久坐不适、坐起痛、上下楼困难、性交痛', '这些提示“有结构问题”，但分不出病因'])], 2)

row((1,), '原文图 1　Trendelenburg 步态（图注译成中文）', 3)

phases('查体流程（编者根据原文整理）', [
    ('1 视诊与步态', LT, TEAL, ['站立看髋、腰椎、膝的姿势；髋和同侧膝轻度屈曲提示关节受刺激',
        '减痛步态：支撑期缩短、屈髋增加、骨盆保持水平；伴外旋要警惕 SCFE', 'Trendelenburg 步态：支撑期对侧骨盆下掉或躯干倒向支撑侧，提示外展肌无力或疲劳，见于髋臼发育不良',
        '站立摸髂嵴比腿长、前屈看脊柱侧弯；仰卧时髋停在屈曲外旋位提示滑膜炎或 SCFE']),
    ('2 触诊', GR, (40, 120, 60), ['骨突：大转子、髂嵴、ASIS、AIIS、坐骨结节、耻骨支/联合', '骶髂关节压痛提示骶髂关节炎',
        '前方软组织：髂腰肌腱炎或关节内；外侧：髂胫束综合征或大转子滑囊炎；后方：臀大肌挫伤']),
    ('3 关节活动度（先测健侧）', OR, (170, 90, 30), ['正常：屈曲约 120°，内旋 30°～40°，外旋 40°～50°，后伸 5°～10°',
        '内旋受限提示 FAI 或 SCFE 倾向；FAI 患者内旋 < 10° 与影像上骨关节炎进展有关', '屈髋时强制性外旋：警惕 SCFE，加拍骨盆正位和蛙式位',
        '内旋或外旋 > 60°：提示关节囊松弛和/或不稳', '被动活动（含滚木试验）疼痛：激惹髋、滑膜炎或 SCFE']),
    ('4 肌力', PU, (90, 60, 150), ['仰卧抗阻屈髋（Stinchfield 试验）：疼痛提示骨突炎、髂腰肌拉伤或关节内病变', '屈膝 90°、足平放，测抗阻外展和内收；外展也可侧卧测']),
    ('5 针对病因的特殊检查', PK, RED, ['撞击和盂唇：FADIR、IROP、Scour、FABER、后方撞击试验', '不稳：前方恐惧、PART、外展-后伸-外旋、俯卧外旋、Dial、后方恐惧',
        '弹响髋：FABER → EADIR、侧卧主动屈髋、Ober、呼啦圈试验'])], 4)

row((2, 5), '原文图 2、5　直腿抬高和 FADIR（图注译成中文）', 5)
row((3,), '原文图 3　髋内旋和外旋（图注译成中文）', 6)
row((4,), '原文图 4　强制性外旋（图注译成中文）', 7)
row((6, 8), '原文图 6、8　前方恐惧和外展-后伸-外旋试验（图注译成中文）', 8)
row((7,), '原文图 7　俯卧恐惧复位试验 PART（图注译成中文）', 9)
row((9,), '原文图 9　内源性弹响髋检查（图注译成中文）', 10)
row((10,), '原文图 10　Ober 试验（图注译成中文）', 11)

# 编者图：特殊检查的敏感度和特异度（原文正文引用的文献数值）
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
T = [('FADIR（撞击）', (51, 100), (89, 89)), ('IROP（撞击）', (75, 89), None), ('Scour（撞击）', (50, 100), None),
     ('FABER（撞击/盂唇）', (41, 97), (18, 100)), ('后方撞击试验', (21, 21), None), ('前方恐惧试验（不稳）', (71, 71), (89, 89)),
     ('外展-后伸-外旋（不稳）', (81, 81), (89, 89)), ('俯卧外旋试验（不稳）', (33, 33), (98, 98))]
fig, ax = plt.subplots(figsize=(10.9, 6.2), dpi=110)
for i, (n, se, sp) in enumerate(T):
    y = len(T) - 1 - i
    for v, dy, c in ((se, 0.15, '#0F6E82'), (sp, -0.15, '#BE2832')):
        if v is None: continue
        if v[0] == v[1]: ax.plot(v[0], y + dy, 'o', color=c, ms=10)
        else: ax.plot(v, [y + dy] * 2, color=c, lw=7, solid_capstyle='round')
        ax.text(v[1] + 2, y + dy, f'{v[0]}%' if v[0] == v[1] else f'{v[0]}%～{v[1]}%', va='center', fontsize=11, color=c)
ax.set_yticks(range(len(T))); ax.set_yticklabels([t[0] for t in T[::-1]], fontsize=14); ax.set_xlim(0, 115)
ax.set_xticks(range(0, 101, 20)); ax.set_xticklabels([f'{v}%' for v in range(0, 101, 20)], fontsize=12)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0); ax.grid(axis='x', color='#ddd'); ax.set_axisbelow(True)
ax.plot([], [], color='#0F6E82', lw=7, label='敏感度'); ax.plot([], [], color='#BE2832', lw=7, label='特异度')
ax.legend(loc='upper center', bbox_to_anchor=(0.45, 1.09), ncol=2, fontsize=13, frameon=False)
fig.text(0.02, 0.015, '条为文献报道的范围，点为单个数值；没画特异度的检查原文未给出。数值来自原文引用的不同研究，不能横向直接比较', fontsize=11, color='#444')
fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(f'{OUT}/_ss.png'); plt.close(fig)
import os
ss = Image.open(f'{OUT}/_ss.png').convert('RGB'); os.remove(f'{OUT}/_ss.png')
save(titled(ss, '特殊检查准不准（编者根据原文正文整理）'), 12)

phases('落到临床（编者整理）', [
    ('先问后查', LT, TEAL, ['问清部位、性质、起病和病程，用问诊把鉴别范围缩小，再有针对性地查体', '先测健侧当参照，再测患侧']),
    ('别漏的危险信号', PK, RED, ['青少年跛行、膝或大腿痛、足外展角变大、屈髋强制性外旋：先排除 SCFE，拍骨盆正位加蛙式位',
        '直腿抬高出现皮节放射痛：先查腰椎']),
    ('撞击还是不稳', OR, (170, 90, 30), ['内旋受限 + FADIR / IROP 阳性：偏向 FAI', '外侧髋痛、Trendelenburg 步态、PART / 前方恐惧阳性、旋转 > 60°：偏向髋臼发育不良或不稳',
        '单个试验都不够准，要和症状、影像一起判断']),
    ('弹响分清内外', PU, (90, 60, 150), ['看得见、侧方：髂胫束，做 Ober 和呼啦圈试验', '听得见、前方：髂腰肌，做 FABER → EADIR'])], 13)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), '髋关节 · 青少年及青年 · 临床查体', font=font(34), fill=TEAL)
dr.text((50, 128), '年轻人髋痛怎么查？', font=font(56), fill=INK)
dr.text((50, 214), '问诊、查体到特殊检查', font=font(48), fill=INK)
dr.text((50, 318), '撞击 · 不稳 · SCFE · 弹响髋', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
