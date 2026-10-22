#!/usr/bin/env python3
"""Wen 等 2025 BMC Sports Sci Med Rehabil 肩胛运动障碍导向训练 vs 多模式物理治疗（肩峰下撞击伴肩胛运动障碍的年轻过顶运动员）：
首图为原题直译标题卡；原文图 1～5 直接用原图，图中英文由编者擦掉后在原位置写中文；
原文表 1～4 另做中文卡片，结果图和临床卡为编者根据原文表 7、表 9 整理。
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


def fit(im, W=1200):
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS) if im.width > W else im


# 首图
W, H = 1400, 720; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '随机对照试验 · BMC Sports Sci Med Rehabil 2025', font=font(32), fill=TEAL)
dr.text((70, 130), '基于肩胛运动障碍的运动疗法与多模式物理治疗', font=font(46), fill=INK)
dr.text((70, 196), '治疗伴肩胛运动障碍的年轻过顶运动员肩峰下撞击综合征：', font=font(46), fill=INK)
dr.text((70, 262), '一项随机对照试验', font=font(46), fill=INK)
dr.text((70, 350), 'Scapular dyskinesis-based exercise therapy versus multimodal physical therapy for subacromial', font=font(25), fill=GREY)
dr.text((70, 386), 'impingement syndrome in young overhead athletes with scapular dyskinesis: a randomized controlled trial', font=font(25), fill=GREY)
dr.line([70, 446, W - 70, 446], fill=(200, 205, 210), width=2)
dr.text((70, 478), 'Wen M, Hu X, Bao G.', font=font(30), fill=GREY)
dr.text((70, 522), 'BMC Sports Sci Med Rehabil. 2025;17:204. doi:10.1186/s13102-025-01254-8', font=font(30), fill=GREY)
dr.text((70, 584), '华南师范大学 · 南京体育学院 · 通辽市蒙医医院', font=font(26), fill=GREY)
dr.text((70, 650), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 编者卡：研究设计一览
phases('研究设计一览（编者根据原文整理）', [
    ('谁参加', LT, TEAL, ['18～25 岁男性过顶运动员，每周训练 ≥ 3 次；共筛查 68 人，纳入 32 人，随机分两组各 16 人，无人脱落',
        '肩峰下撞击：Hawkins-Kennedy、Neer、Jobe 空罐试验至少两项阳性，且恐惧试验时肩前方痛',
        '肩胛运动障碍：肩胛运动障碍试验（SDT）阳性；排除肩袖撕裂、肱二头肌腱病、脱位骨折史、近期手术，主动活动时疼痛 VAS > 6 也排除']),
    ('两组怎么做（8 周，每周 3 次）', GR, (40, 120, 60), ['SDBET 组：按肩胛运动障碍类型定制的三期训练，肩胛控制 → 肩胛稳定（牵伸 + 强化）+ 肩袖 → 功能性训练，在体育学院进行',
        'MPT 组：超声治疗 + 手法治疗（软组织、关节松动、被动牵伸）+ 活动度练习，每次 60 分钟，在当地康复医院进行']),
    ('测什么、什么时候测', OR, (170, 90, 30), ['主要结局：肩痛与功能障碍指数（SPADI）',
        '次要结局：Hawkins-Kennedy 试验时的疼痛 VAS（0～100 mm）、屈曲和外展主动活动度、中/下斜方肌、前锯肌和肩外旋等长肌力（手持测力计）、SDT 分型',
        '基线、第 8 周（干预结束）、第 12 周（停训 4 周后随访）；结局评估者设盲'])], 2)

# 原文图 1 流程图
s = 2533 / 1000
f1 = zh_boxes(raw(102), [
    ((25, 25, 210, 80), '纳入', 18, 'c'),
    ((313, 87, 512, 138), '评估是否符合条件\n（n=68）', 14, 'c'),
    ((532, 145, 758, 240), '排除（n=36）\n1 不符合纳入标准（n=23）\n2 拒绝参加（n=6）\n3 其他原因（n=7）', 12.5, 'l'),
    ((332, 253, 493, 298), '随机分组\n（n=32）', 14, 'c'),
    ((318, 373, 503, 433), '分配', 16, 'c'),
    ((60, 443, 308, 528), '分到 SDBET 组（n=16）\n· 接受肩胛运动障碍导向\n   运动疗法（n=16）\n· 失访（n=0）', 12.5, 'l'),
    ((508, 443, 758, 528), '分到 MPT 组（n=16）\n· 接受多模式物理治疗\n   （n=16）\n· 失访（n=0）', 12.5, 'l'),
    ((318, 542, 503, 607), '干预（8 周）', 16, 'c'),
    ((53, 620, 316, 682), '结局测量（第 8 周）', 15, 'c'),
    ((500, 620, 770, 682), '结局测量（第 8 周）', 15, 'c'),
    ((318, 693, 503, 758), '随访（4 周）', 16, 'c'),
    ((62, 760, 308, 830), '随访失访（n=0）\n结局测量（第 12 周）', 13.5, 'l'),
    ((510, 762, 758, 832), '随访失访（n=0）\n结局测量（第 12 周）', 13.5, 'l'),
    ((318, 845, 503, 905), '分析', 16, 'c'),
    ((80, 925, 290, 975), '纳入分析（n=16）', 14, 'c'),
    ((528, 925, 738, 975), '纳入分析（n=16）', 14, 'c')], s)
save(titled(fit(f1, 1000), '原文图 1　CONSORT 流程图（英文由编者译成中文覆盖）', 1000), 3)

# 原文表 1 中文卡
phases('原文表 1　SDBET 组三期训练方案（编者译成中文）', [
    ('第一期　肩胛控制训练（第 1 周，原文写“总时长 30 分钟”）', LT, TEAL, ['目标：激活肩胛肌群，改善肩胛运动控制',
        '① 肩胛定位训练：治疗师手法引导和口令，把肩胛放到第 2～7 肋之间、较额状面前倾约 30° 的位置，再练前伸/后缩、上提/下降、上回旋/下回旋等主动运动',
        '② Y-T-W-L 训练：俯卧于健身球或治疗床，分别重点收缩下斜方肌（Y）、中斜方肌（T）、中下斜方肌（W）和肩袖（L）',
        '③ 四点跪位肩胛前伸与后缩：闭链练习，前伸练前锯肌，后缩练菱形肌和中斜方肌',
        '每个动作 3 组 × 12～15 次；Borg CR10 强度 2～3']),
    ('第二期　+ 肩胛稳定训练 + 肩袖强化（第 2～6 周，每次 60 分钟）', GR, (40, 120, 60), ['目标：放松紧张肌肉，强化肩胛和肩袖肌群，进一步提高肩胛控制',
        '在第一期基础上，按肩胛运动障碍类型做对应的牵伸和强化（见原文表 2、表 3）',
        '肩袖：弹力带肩外旋/内旋、肩胛平面外展，3 组 × 10～12 次；Borg 强度 3～4']),
    ('第三期　+ 功能性肩部训练（之后至第 8 周）', OR, (170, 90, 30), ['只有前面的练习无明显疼痛或不适才进阶',
        '在第二期基础上加：割草机训练、肩胛俯卧撑、平板支撑（20～30 秒）、肩外展 90° 位弹力带内外旋；Borg 强度 4～5',
        '负荷：多数动作 3 组 × 10～12 次，红色弹力带（中等阻力），哑铃 4 磅（约 1.8 kg）'])], 4)

# 原文图 2
f2 = zh_label(raw(122), [
    (65, 2, 599, 32, '肩胛控制训练：', 40, 'l'),
    (728, 918, 1270, 945, '（1）肩胛定位训练', 40, 'c'),
    (822, 1891, 1168, 1918, '（2）Y-T-W-L 训练', 40, 'c'),
    (576, 2502, 1405, 2529, '（3）四点跪位肩胛前伸与后缩', 40, 'c')])
save(titled(fit(f2), '原文图 2　第一期：肩胛控制训练（英文由编者译成中文覆盖）'), 5)

# 原文表 2、3 中文卡
phases('原文表 2、3　按肩胛运动障碍类型选牵伸和强化（编者译成中文）', [
    ('Ⅰ型：肩胛下角突出，伴矢状面前倾', LT, TEAL, ['牵伸胸小肌：门框牵伸，手或前臂靠门框、肘略高于肩，一脚前跨、身体前推',
        '强化前锯肌、中斜方肌和下斜方肌']),
    ('Ⅱ型：整个肩胛内侧缘突出，伴肩胛内旋', GR, (40, 120, 60), ['牵伸大圆肌：靠墙牵伸，手掌贴墙高于肩、手臂微屈，身体前倾',
        '强化前锯肌、中斜方肌和菱形肌']),
    ('Ⅲ型：肩胛上角突出，伴肩胛上提', OR, (170, 90, 30), ['牵伸上斜方肌和肩胛提肌：一手扶头向对侧拉并稍向同侧转，另一手扶凳固定',
        '强化中斜方肌和下斜方肌']),
    ('强化动作库（3 组 × 10～12 次；牵伸每个 3 次 × 20 秒）', PU, (90, 60, 150), ['前锯肌：泡沫轴靠墙滑动、弹力带肩胛前伸（保持 1 秒）、靠墙俯卧撑',
        '中斜方肌和菱形肌：宽握弹力带划船、俯卧水平外展加外旋（屈肩 90° 持哑铃，伸肘）',
        '下斜方肌：侧卧外旋（肘与躯干间夹毛巾）、侧卧前屈至 90°'])], 6)

# 原文图 3
f3 = zh_label(raw(144), [
    (11, 13, 361, 34, '前锯肌：', 38, 'l'),
    (565, 410, 999, 438, '（1）泡沫轴靠墙滑动', 38, 'c'),
    (443, 875, 1122, 903, '（2）弹力带肩胛前伸', 38, 'c'),
    (606, 1339, 884, 1367, '（3）靠墙俯卧撑', 38, 'c'),
    (9, 1455, 653, 1485, '中斜方肌和菱形肌：', 38, 'l'),
    (25, 1919, 623, 1948, '（1）宽握弹力带划船', 38, 'l'),
    (1037, 1919, 1553, 2006, '（2）俯卧水平外展加外旋', 38, 'c'),
    (9, 2035, 343, 2067, '下斜方肌：', 38, 'l'),
    (206, 2499, 740, 2536, '（1）侧卧外旋', 38, 'c'),
    (948, 2499, 1462, 2536, '（2）侧卧前屈', 38, 'c')])
save(titled(fit(f3), '原文图 3　第二期：肩胛稳定训练（强化）（英文由编者译成中文覆盖）'), 7)

# 原文图 4
f4 = zh_label(raw(159), [
    (3, 3, 622, 46, '肩袖训练：', 42, 'l'),
    (593, 756, 1636, 796, '（1）肩关节外旋与内旋', 40, 'c'),
    (842, 1508, 1387, 1547, '（2）肩关节外展', 40, 'c')])
save(titled(fit(f4), '原文图 4　第二期：肩袖训练（英文由编者译成中文覆盖）'), 8)

# 原文图 5
f5 = zh_label(raw(165), [
    (4, 4, 1023, 44, '附加功能性肩部训练：', 40, 'l'),
    (623, 606, 1063, 637, '（1）割草机训练', 40, 'c'),
    (646, 1236, 1042, 1266, '（2）肩胛俯卧撑', 40, 'c'),
    (765, 1867, 923, 1897, '（3）平板支撑', 40, 'c'),
    (138, 2496, 1548, 2527, '（4）肩外展 90° 位弹力带内旋与外旋', 40, 'c')])
save(titled(fit(f5), '原文图 5　第三期：附加功能性肩部训练（英文由编者译成中文覆盖）'), 9)

# 原文表 4 中文卡
phases('原文表 4　MPT 组多模式物理治疗方案（编者译成中文）', [
    ('第 1 部分　超声治疗', LT, TEAL, ['Chattanooga 便携超声，脉冲模式（占空比 20%），1 MHz，1.0～1.5 W/cm²（按耐受调整），肩峰下区域约 25～50 cm²，每次 8 分钟']),
    ('第 2 部分　手法治疗', GR, (40, 120, 60), ['软组织松动：冈上肌腱和肱二头肌长头腱横向摩擦按摩；上斜方肌、肩胛提肌、胸小肌、大圆肌肌筋膜放松',
        '关节松动（Maitland）：盂肱关节牵引，下、上、后、前向滑动；肩锁关节滑动；肩胛骨各方向松动',
        '被动牵伸：屈曲、后伸、外展、水平外展、外旋、内旋']),
    ('第 3 部分　活动度练习（3 组 × 10～12 次）', OR, (170, 90, 30), ['爬墙练习、扶桌钟摆练习、体操棒练习']),
    ('频次', PU, (90, 60, 150), ['每周 3 次，共 8 周，每次 60 分钟'])], 10)

# 结果图
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
C1, C2 = '#0F6E82', '#BE2832'


def lines(panels, title, n, foot, leg=dict(loc='lower left')):
    fig, axs = plt.subplots(2, 2, figsize=(10.9, 8.2), dpi=110)
    for ax, (name, a, b, sig) in zip(axs.flat, panels):
        x = [0, 1, 2]
        for (m, sd), c, lab, dx in ((a, C1, 'SDBET 组', -0.04), (b, C2, 'MPT 组', 0.04)):
            ax.errorbar([i + dx for i in x], [v[0] for v in zip(m)], yerr=sd, color=c, marker='o', ms=7, lw=2.2, capsize=4, label=lab)
        ax.set_xticks(x); ax.set_xticklabels(['基线', '第 8 周', '第 12 周'], fontsize=12); ax.set_title(name, fontsize=14)
        ax.set_xlim(-0.3, 2.3)
        for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
        lo, hi = ax.get_ylim(); ax.set_ylim(lo, hi + (hi - lo) * 0.12); lo, hi = ax.get_ylim()
        for i, t in sig:
            ax.text(i, hi - (hi - lo) * 0.04, t, ha='center', fontsize=12, color='#333')
        ax.tick_params(labelsize=11)
    axs.flat[0].legend(fontsize=12, frameon=False, **leg)
    fig.text(0.02, 0.012, foot, fontsize=11, color='#444')
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(f'{OUT}/_t.png'); plt.close(fig)
    pg = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
    save(titled(pg, title), n)


import os
T7 = {  # 原文表 7：(均值, 标准差)，基线/第 8 周/第 12 周
    'SPADI': ([45.67, 24.20, 23.37], [6.01, 2.55, 3.17], [46.46, 25.12, 29.35], [5.34, 2.58, 1.80]),
    'VAS': ([45.38, 30.94, 30.63], [5.40, 5.79, 6.85], [45.50, 26.38, 33.00], [5.69, 4.40, 4.90]),
    '屈曲': ([159.38, 169.88, 171.13], [6.50, 5.32, 5.15], [157.94, 170.38, 163.69], [6.02, 4.99, 5.07]),
    '外展': ([146.06, 161.44, 162.63], [7.78, 5.28, 5.43], [143.75, 163.19, 153.06], [8.39, 5.78, 7.35]),
    'MT': ([10.23, 12.20, 12.40], [0.71, 0.70, 0.82], [9.97, 10.00, 10.03], [0.64, 0.67, 0.79]),
    'LT': ([7.89, 9.87, 9.96], [0.62, 0.71, 0.82], [7.70, 7.80, 7.75], [0.63, 0.57, 0.62]),
    'SA': ([14.96, 17.06, 17.17], [0.71, 0.84, 0.87], [14.83, 15.01, 15.08], [0.79, 0.83, 0.87]),
    'SER': ([6.81, 9.14, 9.24], [0.93, 0.92, 0.83], [6.77, 6.91, 6.85], [1.08, 1.06, 1.08])}
g = lambda k: ((T7[k][0], T7[k][1]), (T7[k][2], T7[k][3]))
lines([('SPADI（%，越低越好）', *g('SPADI'), [(1, 'n.s.'), (2, 'P < 0.001')]),
       ('Hawkins 试验时疼痛 VAS（mm）', *g('VAS'), [(1, 'P = 0.018'), (2, 'n.s.')]),
       ('无痛主动屈曲（°）', *g('屈曲'), [(1, 'n.s.'), (2, 'P < 0.001')]),
       ('无痛主动外展（°）', *g('外展'), [(1, 'n.s.'), (2, 'P < 0.001')])],
      '原文表 7　功能、疼痛和活动度（编者作图）', 11, '均值 ± 标准差；P 为同一时间点组间比较；n.s. 无显著差异。第 8 周为干预结束，第 12 周为停训 4 周后')
lines([('中斜方肌（kg）', *g('MT'), [(1, 'P < 0.001'), (2, 'P < 0.001')]),
       ('下斜方肌（kg）', *g('LT'), [(1, 'P < 0.001'), (2, 'P < 0.001')]),
       ('前锯肌（kg）', *g('SA'), [(1, 'P < 0.001'), (2, 'P < 0.001')]),
       ('肩外旋肌（kg）', *g('SER'), [(1, 'P < 0.001'), (2, 'P < 0.001')])],
      '原文表 7　手持测力计等长肌力（编者作图）', 12, '均值 ± 标准差；P 为同一时间点组间比较。MPT 组肌力在各时间点组内均无显著变化', dict(loc='upper left', bbox_to_anchor=(0, 0.92)))

# 原文表 9：SDT 分型
fig, ax = plt.subplots(figsize=(10.9, 4.6), dpi=110)
rows = [('SDBET 基线', [7, 6, 3, 0]), ('SDBET 第 8/12 周', [4, 4, 1, 7]), ('MPT 基线', [5, 8, 3, 0]), ('MPT 第 8/12 周', [5, 8, 3, 0])]
cols = ['#E08A2E', '#BE2832', '#7A4FD6', '#2E9A5A']; labs = ['Ⅰ型 下角突出', 'Ⅱ型 内侧缘突出', 'Ⅲ型 上角突出', 'Ⅳ型 正常']
for i, (r, v) in enumerate(rows):
    y = 3 - i; left = 0
    for j, x in enumerate(v):
        ax.barh(y, x, left=left, color=cols[j], height=0.6, label=labs[j] if i == 0 else None)
        if x: ax.text(left + x / 2, y, str(x), ha='center', va='center', color='white', fontsize=13)
        left += x
ax.set_yticks(range(4)); ax.set_yticklabels([r for r, _ in rows][::-1], fontsize=13); ax.set_xlim(0, 16); ax.set_xticks([0, 4, 8, 12, 16])
ax.set_xlabel('人数（每组 16 人）', fontsize=12)
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.legend(ncol=4, fontsize=12, frameon=False, loc='upper center', bbox_to_anchor=(0.5, 1.16))
fig.text(0.02, 0.02, '第 8 周和第 12 周的分型完全相同；组间 Fisher 精确检验 P = 0.018（第 8、12 周）', fontsize=11, color='#444')
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig(f'{OUT}/_t.png'); plt.close(fig)
pg = Image.open(f'{OUT}/_t.png').convert('RGB'); os.remove(f'{OUT}/_t.png')
save(titled(pg, '原文表 9　肩胛运动障碍分型的变化（编者作图）'), 13)

phases('落到临床（编者整理）', [
    ('先分型，再开处方', LT, TEAL, ['过顶运动员肩峰下撞击，先做 SDT 看肩胛下角、内侧缘还是上角突出',
        'Ⅰ型松胸小肌，Ⅱ型松大圆肌，Ⅲ型松上斜方肌和肩胛提肌；强化以中、下斜方肌和前锯肌为主，再加肩袖']),
    ('按期进阶', GR, (40, 120, 60), ['先练控制（肩胛定位、Y-T-W-L、四点跪位前伸后缩），再加稳定和肩袖，最后做割草机、肩胛俯卧撑、平板支撑和 90° 外展位内外旋',
        '无明显疼痛才进阶；强度用 Borg CR10 从 2～3 逐步到 4～5']),
    ('被动治疗的位置', OR, (170, 90, 30), ['超声 + 手法 + 活动度练习第 8 周止痛更快，但停治疗 4 周后疼痛、功能和活动度都回退',
        '可以作为早期止痛的辅助，不能代替主动训练']),
    ('别高估这项研究', PK, RED, ['32 名年轻男性、单中心、随访只有停训后 4 周；两组在不同机构、由不同人员治疗',
        '第 12 周 SPADI 组间差约 6 分，低于作者自己引用的 14.1～20.6 分最小临床重要差值'])], 14)

# 封面：原文图 4 上排两张弹力带肩外旋/内旋（真人动作、正面、红色弹力带醒目），各裁一块横向拼接
p4 = raw(159); strip = Image.new('RGB', (2 * 660 + 12, 568), 'white')
strip.paste(p4.crop((232 + 170, 147, 232 + 830, 715)), (0, 0))
strip.paste(p4.crop((1154 + 110, 147, 1154 + 770, 715)), (672, 0))
cover_from(strip, 0.5, 0.5)
