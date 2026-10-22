#!/usr/bin/env python3
"""Chinn 和 Hertel 2010 Clin Sports Med 运动员踝与足部损伤的康复（临床综述）：首图为原题直译标题卡；
原文图 1～3 为照片（图内只有分图字母和箭头，无英文），图注译成中文；
损伤一览、步态示意和各损伤康复卡为编者根据原文整理。
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
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88, optimize=True)


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


import numpy as np


import io


def raw(x):
    return Image.open(io.BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def cover_from(im, cx=0.5, cy=0.5):
    """封面 900×383：从原文插图按比例裁出一块（cx、cy 为裁剪中心的相对位置）"""
    r = 900 / 383; w, h = im.size
    if w / h > r: cw, ch = round(h * r), h
    else: cw, ch = w, round(w / r)
    x = min(max(0, round(cx * w - cw / 2)), w - cw); y = min(max(0, round(cy * h - ch / 2)), h - ch)
    im.crop((x, y, x + cw, y + ch)).resize((900, 383), Image.LANCZOS).convert('RGB').save(f'{OUT}/cover.jpg', quality=90)


def tiles(items, title, n, fs=24):
    """原图并排（等高），下方灰底中文图注"""
    gap = 15; W = 1200; hs = 600
    ims = [x.resize((round(x.width * hs / x.height), hs), Image.LANCZOS) for x, _ in items]
    k = (W - gap * (len(ims) - 1)) / sum(i.width for i in ims)
    ims = [i.resize((round(i.width * k), round(i.height * k)), Image.LANCZOS) for i in ims]
    hh = ims[0].height; ch = max(para_h(t, fs, i.width - 24, gap=8) for i, (_, t) in zip(ims, items))
    im = Image.new('RGB', (W, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im); x = 0
    for i, (_, t) in zip(ims, items):
        im.paste(i, (x, 0)); dr.rectangle([x, hh, x + i.width, hh + ch + 20], fill=(232, 232, 232))
        para(dr, x + 12, hh + 12, t, fs, i.width - 24, gap=8); x += i.width + gap
    save(titled(im, title), n)


def one(x, cap, title, n):
    save(titled(capbox(x, cap), title), n)


def title_card(tag, zh, en, au, cite, org):
    W, H = 1400, 700; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, 18, H], fill=TEAL)
    dr.text((70, 56), tag, font=font(32), fill=TEAL)
    y = 130
    for l in zh: dr.text((70, y), l, font=font(50), fill=INK); y += 70
    y += 20
    for l in en: dr.text((70, y), l, font=font(28), fill=GREY); y += 40
    y += 20; dr.line([70, y, W - 70, y], fill=(200, 205, 210), width=2); y += 30
    dr.text((70, y), au, font=font(30), fill=GREY); y += 44
    dr.text((70, y), cite, font=font(28), fill=GREY); y += 56
    dr.text((70, y), org, font=font(26), fill=GREY)
    dr.text((70, H - 60), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
    save(im, 1)


def zh_label(im, boxes):
    """图中白底英文标注：整块刷成底色后在原位置写中文。boxes 为 (x0, y0, x1, y1, 文字, 字号, 对齐)"""
    d = ImageDraw.Draw(im); a = np.asarray(im.convert('L')) < 240; H_, W_ = a.shape
    for x0, y0, x1, y1, t, fs, al in boxes:
        # 向外扩到字母上下沿的浅色像素，碰到照片（成片非白）就停
        e0, e1, ex0, ex1 = y0, y1, max(0, x0 - 8), min(W_, x1 + 8)
        while e0 > 0 and y0 - e0 < 14 and a[e0 - 1, ex0:ex1].mean() < 0.3: e0 -= 1
        while e1 < H_ - 1 and e1 - y1 < 14 and a[e1 + 1, ex0:ex1].mean() < 0.3: e1 += 1
        d.rectangle([ex0, e0, ex1, e1], fill='white')
        f = font(fs); w = d.textlength(t, font=f); cy = (y0 + y1) / 2
        x = x0 if al == 'l' else (x1 - w if al == 'r' else (x0 + x1 - w) / 2)
        d.text((x, cy), t, font=f, fill=(0, 0, 0), anchor='lm')
    return im


def zh_boxes(im, boxes, s):
    """流程图：方框内部刷成框内底色（保留边框），再写中文。坐标按缩略图给出，s 为放大倍数"""
    d = ImageDraw.Draw(im); a = np.asarray(im)
    for (x0, y0, x1, y1), t, fs, al in boxes:
        x0, y0, x1, y1 = (round(v * s) for v in (x0, y0, x1, y1)); m = round(2.5 * s)
        bg = tuple(int(c) for c in np.median(a[y0 + m:y1 - m, x0 + m:x1 - m].reshape(-1, 3), 0))
        d.rectangle([x0 + m, y0 + m, x1 - m, y1 - m], fill=bg)
        fg = 'white' if sum(bg) < 500 else (20, 20, 20); f = font(fs * s); ls = t.split('\n'); lh = fs * s * 1.3
        top = (y0 + y1) / 2 - lh * len(ls) / 2 + lh / 2
        for i, l in enumerate(ls):
            x = x0 + m + 4 if al == 'l' else (x0 + x1 - d.textlength(l, font=f)) / 2
            d.text((x, top + i * lh), l, font=f, fill=fg, anchor='lm')
    return im


def heal(im, mask, it=400):
    """把 mask 区域（文字笔画）用四邻域扩散补成周围底色（照片上的字母用）"""
    a = np.asarray(im).astype(float); m = mask.copy(); a[m] = a[~m].mean(0)
    ys, xs = np.nonzero(m); y0, y1, x0, x1 = max(ys.min() - 2, 0), ys.max() + 3, max(xs.min() - 2, 0), xs.max() + 3
    sub = a[y0:y1, x0:x1]; sm = m[y0:y1, x0:x1]
    for _ in range(it):
        p = np.pad(sub, ((1, 1), (1, 1), (0, 0)), mode='edge')
        avg = (p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) / 4
        sub[sm] = avg[sm]
    a[y0:y1, x0:x1] = sub
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def dark_mask(im, boxes, thr=90, grow=2):
    """boxes 内比 thr 暗的像素（黑色字母）作为 mask，向外扩 grow 像素"""
    g = np.asarray(im.convert('L')); m = np.zeros(g.shape, bool)
    for x0, y0, x1, y1 in boxes: m[y0:y1, x0:x1] = g[y0:y1, x0:x1] < thr
    for _ in range(grow):
        p = np.pad(m, 1); m = p[1:-1, 1:-1] | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    return m


def vtext(im, box, t, fs, fill=(0, 0, 0), bg='white'):
    """竖排文字区（旋转 90° 的英文）：刷底色后写逆时针旋转 90° 的中文"""
    d = ImageDraw.Draw(im); d.rectangle(box, fill=bg); f = font(fs)
    w = int(d.textlength(t, font=f)) + 8; lay = Image.new('RGBA', (w, fs + 10), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((4, 2), t, font=f, fill=fill); lay = lay.rotate(90, expand=True)
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2; im.paste(lay, (cx - lay.width // 2, cy - lay.height // 2), lay)
    return im


def chart_style():
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    fm.fontManager.addfont(F); plt.rcParams['font.family'] = fm.FontProperties(fname=F).get_name()
    plt.rcParams['axes.unicode_minus'] = False
    return plt


def figsave(plt, fig, title, n):
    b = io.BytesIO(); fig.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
    save(titled(Image.open(b).convert('RGB'), title), n)


# 首图：原题直译
title_card('临床综述 · Clinics in Sports Medicine 2010',
           ['运动员踝与足部损伤的康复'],
           ['Rehabilitation of Ankle and Foot Injuries in Athletes'],
           'Lisa Chinn, Jay Hertel',
           'Clin Sports Med. 2010;29(1):157-167. doi:10.1016/j.csm.2009.09.006',
           '美国弗吉尼亚大学运动机能学项目，运动与运动损伤实验室')

# 编者整理：五类损伤一览
W = 1200; rows = [
    ('外侧踝扭伤', '内翻 + 跖屈', '活动度、力量、神经肌肉协调；平衡从双足到单足、从稳定到不稳定面', '活动度完全、力量达伤前 80%～90%、步态正常、能无代偿地变向和落地，整场训练不痛不肿'),
    ('内侧 / 下胫腓联合扭伤', '外翻 + 背伸 / 外旋', '先固定加拐杖，控制疼痛肿胀；内外翻尽量少；之后按外侧扭伤的流程进阶', '同上，并能顺利跑动和变向；愈合可能要数月'),
    ('足底筋膜炎', '慢性劳损', '先止痛、减少不必要的负重；恢复踝和拇趾背伸；练足内外在小肌群', '能不痛地走完一整天，再逐步加量'),
    ('跟腱炎', '慢性过用', '休息和调整活动、跟杯；牵伸和渐进力量，离心训练；评估足型和步态', '活动度、力量和耐力恢复，整场训练不痛'),
    ('草皮趾', '拇趾过伸', '休息、换鞋；疼痛肿胀减轻后练屈伸趾、短足和关节松动', '疼痛肿胀消失；硬鞋垫或贴扎保护')]
cw = [210, 190, 420, 340]; hdr = ['损伤', '机制', '康复重点', '回场标准']
H = 64 + sum(max(para_h(t, 22, w - 24, gap=6) for t, w in zip(r, cw)) + 24 for r in rows)
im = Image.new('RGB', (W, H + 20), 'white'); dr = ImageDraw.Draw(im); x = 20
for t, w in zip(hdr, cw): dr.rectangle([x, 10, x + w, 64], fill=TEAL); dr.text((x + 12, 22), t, font=font(26), fill='white'); x += w
y = 64
for k, r in enumerate(rows):
    h = max(para_h(t, 22, w - 24, gap=6) for t, w in zip(r, cw)) + 24; x = 20
    for j, (t, w) in enumerate(zip(r, cw)):
        dr.rectangle([x, y, x + w, y + h], fill=LT if k % 2 else 'white', outline=(210, 210, 210))
        para(dr, x + 12, y + 12, t, 22, w - 24, fill=RED if j == 0 else INK, gap=6); x += w
    y += h
save(titled(im.crop((0, 0, W, y + 14)), '五类常见踝足损伤的康复要点（编者根据原文整理）'), 2)

# 步态：支撑相里距下关节的旋前和旋后
plt = chart_style()
fig, ax = plt.subplots(figsize=(10.9, 3.9))
ax.barh(2, 20, left=0, color='#F2B880', height=0.5); ax.text(10, 2, '足跟着地→前足着地\n快速旋前', ha='center', va='center', fontsize=11)
ax.barh(1, 85, left=0, color='#2C8C9E', height=0.5); ax.barh(1, 30, left=55, color='#2C8C9E', alpha=0.45, height=0.5, hatch='//', edgecolor='white')
ax.text(27, 1, '旋前：中跗关节“解锁”，足吸收冲击、适应地面', ha='center', va='center', fontsize=11.5, color='white')
ax.text(70, 0.62, '最大旋前出现在 55%～85%', ha='center', fontsize=10.5, color='#2C8C9E')
ax.barh(0, 30, left=70, color='#D2553C', height=0.5); ax.text(85, 0, '再旋后：足变硬\n（杠杆）准备蹬离', ha='center', va='center', fontsize=11, color='white')
ax.set_yticks([2, 1, 0]); ax.set_yticklabels(['承重早期', '旋前', '再旋后'], fontsize=12.5); ax.set_xlim(0, 100); ax.set_ylim(-0.5, 2.5)
ax.set_xticks([0, 20, 55, 70, 85, 90, 100]); ax.set_xticklabels(['足跟着地', '20%', '55%', '70%', '85%', '90%', '足尖离地'], fontsize=11)
ax.set_xlabel('支撑相进程（原文描述的是跑步）', fontsize=11.5); ax.spines[['top', 'right']].set_visible(False)
figsave(plt, fig, '正常步态：支撑相的距下关节运动（编者据原文描述绘制）', 3)

one(raw(13), '原文图 1　单足平衡训练：A 单足站立；B 单足站在不稳定的气垫上；C 双臂外展、单足站在软垫上。可通过改变手臂位置、闭眼、加不稳定支撑面来进阶',
    '平衡训练怎么进阶（原文图 1）', 4)

phases('外侧踝扭伤：分期康复（编者根据原文整理）', [
    ('早期：还不能负重', LT, TEAL, [
        '等长收缩和开链活动度，重点是背伸和跖屈，被动、主动按耐受做',
        '毛巾牵伸、摇板活动度；固定自行车兼顾活动度和心肺；关节松动改善背伸；水疗']),
    ('中期：能负重以后', GR, (40, 120, 60), [
        '平衡：双足→单足、稳定→不稳定面，再加闭眼、外力扰动、抛接重球、单腿蹲、单腿伸够',
        '继续活动度：摇板、斜板牵伸跟腱',
        '疼痛肿胀控制后加力量：先背伸跖屈（负重提踵、深蹲），韧带愈合后再加内外翻；弹力带、踝部沙袋；对角线动作',
        '重新教正确的走路方式']),
    ('功能期：活动度和力量恢复后', OR, RED, [
        '先单平面：直线走、慢跑，做到不痛不跛',
        '再加单足跳、跳跃、垫步、变向：健侧连跳 10 次测距离和高度，患侧去追平',
        '变向从大弧线到更急、更快的切步；侧滑步、交叉步；换上专项鞋，从无对抗→对抗→全场']),
    ('回场标准', PK, RED, [
        '活动度完全、力量达伤前的 80%～90%、步态正常，变向和落地无代偿，能不痛不肿地完成一整场训练']),
], 5)

one(raw(17), '原文图 2　用弹力管做力量训练（图为弹力管抗阻踝背伸）', '弹力管抗阻训练（原文图 2）', 6)

phases('内侧踝扭伤和下胫腓联合扭伤（编者根据原文整理）', [
    ('和外侧扭伤有什么不同', LT, TEAL, [
        '内侧扭伤：过度外翻 + 背伸，伤三角韧带；内侧肿胀瘀青，不愿负重',
        '下胫腓联合扭伤：过度外旋或强制背伸，伤胫腓骨远端之间的韧带；常常肿得不明显，但下胫腓前方压痛很明显；血供差，常需数月愈合']),
    ('怎么练', GR, (40, 120, 60), [
        '先固定、拄拐，以控制疼痛和肿胀为主；固定期间可做受控的开链背伸跖屈，内外翻尽量少，任何训练都不能加重疼痛肿胀',
        '能负重后尽量少用拐，必要时做步态训练；之后按外侧扭伤的流程进阶']),
    ('回场和宣教', OR, RED, [
        '活动度完全、力量达伤前 80%～90%，跑动和变向没有困难，整场训练不痛不肿',
        '最重要的是耐心：要让运动员、教练和家长明白，这类扭伤比外侧扭伤恢复慢得多']),
], 7)

one(raw(35), '原文图 3　短足训练：收缩足底内在肌，把跖骨头往跟骨方向拉（箭头），尽量不让外在肌参与', '短足训练（原文图 3）', 8)

phases('足底筋膜炎（编者根据原文整理）', [
    ('识别', LT, TEAL, [
        '足跟内前方、筋膜起点处疼痛，早上起床头几步或久坐后起身最明显，走开了会减轻，站太久或常踮脚又加重；背伸前足和足趾时加重',
        '易患因素：高弓足、过度旋前、超重、长时间在硬地上走跑站、旧鞋（足弓支撑不足）、跟腱紧']),
    ('怎么治、怎么练', GR, (40, 120, 60), [
        '先止痛、休息，减少不必要的负重；穿舒适、有支撑的鞋，加跟杯或定制矫形鞋垫',
        '恢复踝和拇趾背伸：毛巾牵伸、斜板牵伸、关节松动；疼痛减轻后练足内外在小肌群：毛巾卷、拇趾/小趾抬起、短足训练；可配合横向摩擦按摩',
        '能不痛地走完一整天再加量；短时间、多次牵伸比一天一次长时间牵伸好']),
    ('小技巧', OR, RED, [
        '坐着用网球、高尔夫球在足弓下滚动；纸杯装水冻成冰杯来滚，冷敷和牵伸一起做',
        '起床下地前先穿上有足弓支撑的鞋；夜间夹板让足保持背伸或中立位；白天别穿高跟鞋和没支撑的凉鞋',
        '反复发作是因为只治了症状没治原因：要评估步态，必要时定制矫形鞋垫']),
], 9)

phases('跟腱炎（编者根据原文整理）', [
    ('识别', LT, TEAL, [
        '长跑运动员最常见的过用伤；跟骨止点上方 2～6 cm 逐渐疼痛、僵硬，跑坡、爬楼、冲刺后加重',
        '小腿肌力测试可能正常，但柔韧性下降；提踵到力竭时比健侧差；局部可发热、压痛、捻发感，肌腱增粗提示慢性']),
    ('怎么练', GR, (40, 120, 60), [
        '早期：休息、调整活动，用跟杯减负；横向摩擦按摩；毛巾和斜板牵伸，一天多次',
        '活动度恢复后去掉跟杯，避免适应性缩短；一开始就加渐进力量：提踵、弹力管，从少组少次到少组多次练耐力',
        '疼痛减轻后加器械、弓步和专项动作；小腿三头肌离心训练常有好效果；评估足型和步态，过度旋前可用矫形鞋垫',
        '活动度、力量、耐力恢复后，在平地上从走、慢跑和短促加速开始']),
    ('宣教', OR, RED, [
        '坡道训练每周最多一次；了解自己的足型和合适的鞋，跑鞋每 500 英里（约 800 km）或最多 2 年换一双；经常牵伸']),
], 10)

phases('草皮趾和总结（编者根据原文整理）', [
    ('草皮趾', LT, TEAL, [
        '拇趾过伸导致第一跖趾关节扭伤和关节囊损伤；急性多因急停时鞋卡在地上、身体前冲，慢性多因鞋子让拇趾活动过多',
        '休息、换鞋，先控制疼痛；疼痛肿胀减轻后做屈伸趾（卷趾、短足训练）和拇趾关节松动',
        '回场：疼痛肿胀消失；用钢板或其他硬质前掌鞋垫、拇趾贴扎限制背伸；不处理可能留下活动度永久下降、骨刺和关节炎']),
    ('所有踝足损伤的共同原则', GR, (40, 120, 60), [
        '恢复关节活动度、肌力和神经肌肉协调，并恢复正常步态',
        '逐级回归运动，包括专项训练，目标是安全回场、减少再伤']),
], 11)

# 封面：原文图 1A、1B 两张单足平衡照片，各自以人为中心裁出后并排，抹掉分图字母 A
im = raw(13); a = im.crop((25, 0, 405, 325)); m = np.zeros((a.height, a.width), bool); m[10:46, 0:22] = True; a = heal(a, m)
b_ = im.crop((510, 0, 890, 325)); cv = Image.new('RGB', (766, 325), 'white'); cv.paste(a, (0, 0)); cv.paste(b_, (386, 0))
cv.resize((900, 382), Image.LANCZOS).resize((900, 383)).save(f'{OUT}/cover.jpg', quality=90)
