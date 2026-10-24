#!/usr/bin/env python3
"""Sakaguchi 等 2024《成人腰椎术后的评估与康复》（J Clin Med）推文配图。
首图中文标题卡、原文图 1～16（含图中英文的图 3、4、5、7、12 先用 tools/fig-translate 译成中文）、三类问题卡、临床要点卡、封面。
用法：python3 make_figs.py <论文.pdf> <work 目录> <输出目录> <中文字体>
work 目录需要：zh_p5_1.png、zh_p7_1.png、zh_p7_2.png、zh_p8_2.png、zh_p12_1.png（figtrans render 输出，300 dpi）"""
import io
import sys

import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, WORK, OUT, F = sys.argv[1:5]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
op = lambda n: Image.open(f'{WORK}/{n}').convert('RGB')
doc = pymupdf.open(PDF)
# 原文照片和示意图是内嵌位图，按 xref 直接取原始像素（页面上还压着一层审稿稿，不能整页截图）
XREF = {1: 91, 2: 126, 6: 288, 8: 373, 9: 404, 10: 405, 11: 479, 13: 523, 14: 604, 15: 646, 16: 681}


def raw(n):
    pix = pymupdf.Pixmap(doc, XREF[n])
    if pix.n > 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')


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
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


def trim(im, pad=12):
    """裁掉四周白边"""
    g = im.convert('L').point(lambda v: 255 if v < 245 else 0); x0, y0, x1, y1 = g.getbbox()
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def cut_bottom(im, frac, top=0.04):
    """figtrans 的裁剪框上下各带进了一截正文和图注，切掉"""
    return im.crop((0, round(im.height * top), im.width, round(im.height * (1 - frac))))


def stack(ims, W=1200, gap=16):
    ims = [i.resize((W, round(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    t = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: t.paste(i, (0, y)); y += i.height + gap
    return t


def side(a, b, W=1200, gap=16):
    h = 600
    a = a.resize((round(a.width * h / a.height), h), Image.LANCZOS); b = b.resize((round(b.width * h / b.height), h), Image.LANCZOS)
    t = Image.new('RGB', (a.width + b.width + gap, h), 'white'); t.paste(a, (0, 0)); t.paste(b, (a.width + gap, 0))
    return t.resize((W, round(h * W / t.width)), Image.LANCZOS)


# 1 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '叙述性综述 · 《Journal of Clinical Medicine》2024', font=font(32), fill=TEAL)
dr.text((70, 135), '成人腰椎术后的评估与康复', font=font(58), fill=INK)
dr.text((70, 210), '量表、体能测试与按手术入路的训练', font=font(44), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Sakaguchi T, Gunjotikar S, Tanaka M, et al.', font=font(26), fill=GREY)
dr.text((70, 390), 'J Clin Med. 2024;13(10):2915. doi:10.3390/jcm13102915', font=font(28), fill=GREY)
dr.text((70, 435), '日本冈山劳灾医院 康复科、骨科', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(raw(1), '原文图 1  Williams 腰椎屈曲训练：(A) 骨盆后倾 (B) 屈膝卷腹 (C) 双膝抱胸，牵伸竖脊肌 (D) 坐位够脚尖，牵伸腘绳肌和竖脊肌 '
            '(E) 前弓步，牵伸髂股韧带 (F) 坐位前屈 (G、H) 强化股四头肌，牵伸臀大肌和竖脊肌'), 2)
save(capbox(raw(2), '原文图 2  McKenzie 训练：(A) 站立前屈 (B) 站立后伸 (C) 卧位屈曲 (D) 治疗师辅助站立侧方滑移 (E) 站立侧方滑移 (F) 俯卧后伸'), 3)
save(capbox(trim(cut_bottom(op('zh_p5_1.png'), 0.06)), '原文图 3（图中英文由编者译为中文）  治疗后评估结果的解读：A 落在测量误差内，没有临床意义；'
            'B 超出测量误差（MDC），但还没到有临床意义的程度；C 超过 MCID，属于有临床意义的变化'), 4)

f4 = capbox(trim(cut_bottom(op('zh_p7_1.png'), 0.02)), '原文图 4  步速：前后各留 5 m 加减速，只计中间 10 m')
f5 = capbox(trim(cut_bottom(op('zh_p7_2.png'), 0.05)), '原文图 5  6 分钟步行试验：30 m 往返走 6 分钟，记录距离')
f6 = capbox(trim(raw(6)), '原文图 6  计时起立行走（TUG）：从椅子站起，走到 3 m 处转身，走回坐下')
f7 = capbox(trim(cut_bottom(op('zh_p8_2.png'), 0.05)), '原文图 7（图中英文由编者译为中文）  功能性前伸：手臂前平举，尽量前伸，量 A 到 B 的距离')
save(stack([f4, f5, f6, f7], gap=30), 5)

save(capbox(side(raw(9), raw(10)), '原文图 9、图 10  左：不同腰椎融合术的入路（ALIF 前路、OLIF 斜外侧、XLIF 极外侧、TLIF 经椎间孔、PLIF 后路）；'
            '右：OLIF 入路，从腹外斜肌、腹内斜肌、腹横肌之间进入，绕开腰大肌前缘'), 6)

save(card(1200, '术后要解决的 3 类问题（编者根据原文整理）', [
    ('第 1 类：单纯肌力下降', '手术切开或剥离造成的局部肌肉无力。后路（PLIF、TLIF）伤多裂肌、竖脊肌；侧路（XLIF、OLIF）伤腹斜肌、腹横肌和腰大肌\n'
     '→ 针对受累肌群做力量训练', LT, TEAL),
    ('第 2 类：持续能力下降', '能用力但撑不久，走不远、站不久\n→ 有氧和重复性训练，提高核心、上肢、下肢的耐力', OR, (200, 120, 0)),
    ('第 3 类：脊柱平衡失调', '本体感觉和姿势反射改变，动态平衡差，跌倒风险高\n→ 双任务、多任务平衡训练，回到日常活动', GR, (0, 120, 60)),
]), 7)

save(capbox(raw(11), '原文图 11  功能性中立位脊柱控制训练（NSCE）：(A) 腹部收紧（腹横肌预激活） (B) 鸟狗式 (C) 蚌式开合 '
            '(D) 双肩后伸（弹力带） (E) 双肩前屈（弹力带） (F) 髋外展。作者说从急性期就开始用这套动作'), 8)

f12 = capbox(trim(cut_bottom(op('zh_p12_1.png'), 0.04)), '原文图 12（图中英文由编者译为中文）  腰大肌在腰椎屈曲、中立、伸展三种姿势下的作用线')
f13 = capbox(raw(13), '原文图 13  腰大肌训练：(A) 坐位屈髋 (B) 靠墙站立屈髋（保持腰椎前凸）')
save(stack([f12, f13], gap=30), 9)

save(capbox(raw(14), '原文图 14  双任务、多任务平衡训练：(A) 端着托盘走，不让球掉下来 (B) 闭眼站平衡垫 (C) 站在平衡垫上接球 (D) 绕杆走，同时做认知任务'), 10)
save(capbox(raw(15), '原文图 15  辅具和日常动作指导：(A) 侧卧起身 (B) 从地上捡东西 (C) 用拾物器捡东西 (D) 用穿裤辅具穿裤子 '
            '(E) 原文图注与 D 重复，照片里是穿袜辅具 (F) 用鞋拔穿鞋'), 11)
save(capbox(raw(16), '原文图 16  骨融合前要避免的训练：(A) 仰卧双腿抬起 (B) 仰卧抬臀（桥式） (C) 四点跪位伸单臂，或同时伸对侧腿（鸟狗式） (D) 四点跪位拱背'), 12)

save(card(1200, '这篇综述落到临床（编者整理）', [
    ('先评估再练', '量表选 ODI 或 RMDQ，椎管狭窄加 ZCQ，长节段融合加 LSDI；体能测步速、6 分钟步行、TUG、功能性前伸，'
     '有条件再做 Mini-BESTest。拿 MCID 判断变化有没有临床意义', LT, TEAL),
    ('按入路练', '后路融合：多裂肌、竖脊肌，中立位控制为主；侧路融合：腹壁肌和腰大肌，屈髋训练时保持腰椎前凸', GR, (0, 120, 60)),
    ('肌力和平衡并重', '力量 → 耐力 → 双任务平衡逐级推进；长节段融合、老年患者要重视跌倒风险', OR, (200, 120, 0)),
    ('骨融合前慎做', '仰卧双腿抬起、桥式、鸟狗式、四点拱背，弯腰提重物、手持重物前举、系鞋带；'
     '原文自己的训练图里就有鸟狗式，开始时间要和术者商量', PK, RED),
]), 13)

# 封面：原文图 11 上排（中立位控制训练）
c = raw(11); h = round(c.height * 0.48); w = round(h * 900 / 383); x0 = (c.width - w) // 2
c.crop((x0, 0, x0 + w, h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
