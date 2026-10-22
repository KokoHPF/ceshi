#!/usr/bin/env python3
"""Esen 等 2026 BMC Musculoskelet Disord 拇外翻女性 9 种足部训练的足内外在肌肌电激活（横断面研究）：首图为原题直译标题卡；
原文图 1～4 直接用原图，图中英文（说明框、肌肉缩写、信号标题、箱线图标题/纵轴/横轴/图例）由编者擦掉后在原位置写中文；
中位数热图（从原文图 4 估读）和临床卡为编者整理。
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


def box_text(im, box, title, body, fs=36):
    """原文图 1 右侧说明框：框内刷白（保留边框），竖直居中写中文标题和说明"""
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = box; d.rectangle(box, fill='white'); w = x1 - x0 - 36
    h = para_h(title, fs, w, gap=10) + para_h(body, fs, w, gap=10); y = (y0 + y1 - h) / 2
    y = para(d, x0 + 18, y, title, fs, w, fill=RED, gap=10); para(d, x0 + 18, y, body, fs, w, gap=10)


def wbox(im, box, t, fs, pad=12):
    """白底上的英文标题：四周外扩 pad 整块刷白后居中写中文"""
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = box; d.rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], fill='white')
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), t, font=font(fs), fill=(0, 0, 0), anchor='mm'); return im


def rot_label(im, t, x, y, fs, ang=45):
    """45° 斜排的横轴标签：文字末端落在 (x, y)"""
    f = font(fs); w = int(ImageDraw.Draw(im).textlength(t, font=f)) + 6; h = fs + 8
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((3, 2), t, font=f, fill=(0, 0, 0))
    lay = lay.rotate(ang, expand=True, resample=Image.BICUBIC); c = np.cos(np.radians(ang)) * w / 2
    im.paste(lay, (round(x - lay.width / 2 - c), round(y - lay.height / 2 + c)), lay)


def photo_label(im, items):
    """照片上的黑色英文缩写：扩散补底后写中文（items：框, 文字, 字号, 写字位置）"""
    im = heal(im, dark_mask(im, [b for b, *_ in items], thr=85, grow=3))
    d = ImageDraw.Draw(im)
    for b, t, fs, (x, y) in items:
        for i, l in enumerate(t.split('\n')): d.text((x, y + i * (fs + 4)), l, font=font(fs), fill=(0, 0, 0))
    return im


# 首图：原题直译
title_card('横断面比较研究 · BMC Musculoskelet Disord 2026',
           ['拇外翻女性在 9 种不同足部训练中', '足外在肌和内在肌的肌电激活：', '一项横断面比较研究'],
           ['Electromyographic activation of extrinsic and intrinsic foot muscles during',
            'nine different foot exercises in women with hallux valgus:', 'a cross-sectional comparative study'],
           'Esen DH, Taş S, Salkın Y, Alcan V · 土耳其托罗斯大学 等',
           'BMC Musculoskelet Disord. 2026;27:591. doi:10.1186/s12891-026-09949-w', '')

# 原文图 1：9 种训练，右侧英文说明框刷白后写中文
im = raw(77)
im = wbox(wbox(im, (324, 2, 500, 32), '训练动作', 36, pad=10), (1252, 2, 1481, 32), '动作要求', 36, pad=10)
for box, t, b_ in [
        ((896, 135, 1927, 542), '坐位 / 站立 / 单腿短足训练（SF，a～c）：',
         '脊柱挺直、骨盆中立，以维持足的位置；第 2 趾与跟骨对成一条直线。（a）把跖骨头往足跟方向拉、抬高内侧纵弓，不允许屈趾；全程前足和后足都要贴地。站立位（b）和单腿位（c）按同样要求完成。'),
        ((896, 655, 1927, 837), '毛巾卷训练（d）：', '坐在椅子上，双足平放并相互平行。听到指令后，抬高内侧纵弓并屈曲足趾，但不抬起跖骨头。'),
        ((896, 1003, 1927, 1106), '分趾训练（TSO，e）：', '保持同样坐姿，尽力主动张开足趾。'),
        ((907, 1299, 1936, 1624), '三维足踝对角线伸展（3DFA-D1E、3DFA-D2E，f、g）：',
         '属于 PNF 训练，足踝沿对角线 1、2 方向运动。对角线 1（f）做跖屈-旋前-外翻-屈趾，对角线 2（g）做跖屈-旋后-内翻-屈趾。'),
        ((907, 1774, 1936, 1998), '提踵训练（h）：', '不抬起另一条腿，站在台阶上让足跟落到台阶以下，再以经典提踵动作把重量压到拇趾上；可扶对面墙壁保持平衡。'),
        ((907, 2190, 1936, 2374), '站立摆腿训练（ı）：', '被测足单腿站立，另一条腿前后摆动，尽量保持平衡。')]:
    box_text(im, box, t, b_, fs=40)
save(titled(capbox(im, '原文图 1　9 种训练：坐位短足（a）、站立短足（b）、单腿短足（c）、毛巾卷（d）、分趾（e）、三维足踝对角线 1（f）和 2（g）伸展、提踵（h）、站立摆腿（ı）'),
            '9 种训练怎么做（原文图 1，编者中文覆盖）'), 2)

# 原文图 2：电极位置，照片上的肌肉缩写换成中文
im = photo_label(raw(104), [
    ((44, 220, 88, 248), '腓骨\n长肌', 22, (44, 210)), ((52, 377, 125, 407), '拇长\n伸肌', 22, (60, 368)),
    ((762, 282, 808, 308), '腓骨长肌', 24, (762, 282)), ((648, 442, 718, 473), '拇长\n伸肌', 22, (659, 432)),
    ((1298, 384, 1374, 413), '拇长屈肌', 24, (1298, 386)), ((1311, 482, 1386, 511), '拇展肌', 24, (1311, 484))])
save(titled(capbox(im, '原文图 2　表面肌电电极位置：腓骨长肌（PL）在腓骨头下 3～4 cm；拇长伸肌（EHL）在踝线上 3～4 cm、胫骨外缘旁；拇长屈肌（FHL）在跟腱止点上约 5 cm 内侧；拇展肌（ABH）在舟骨粗隆后 1～2 cm'),
            '测哪 4 块肌肉（原文图 2，编者中文覆盖）'), 3)

# 原文图 3：信号处理示意
im = zh_label(raw(139), [(867, 9, 1115, 38, '原始肌电信号', 34, 'c'), (711, 442, 1205, 473, '带通滤波（10～500 Hz）后的肌电信号', 32, 'c'),
                         (472, 1010, 1496, 1035, 'RMS 包络（150 ms 窗口）与选取的 3 秒分析窗', 32, 'c')])
save(titled(capbox(im, '原文图 3　一次试验的信号处理：上为原始肌电，中为带通滤波后，下为 150 ms 滑动窗 RMS 包络；红框是用于计算平均 RMS 的 5 秒持续收缩中间 3 秒（纵轴单位 µV，横轴单位秒）'),
            '肌电怎么算（原文图 3，编者中文覆盖）'), 4)

# 原文图 4：四块肌肉的箱线图，标题、纵轴名、斜排横轴标签和图例全部换成中文
EX = ['坐位短足', '站立短足', '单腿短足', '毛巾卷', '分趾', '3DFA-D1E', '3DFA-D2E', '提踵', '站立摆腿']
P4 = [  # 标题框, 标题, 纵轴名框, 横轴标签区, 刻度 x, 标签末端 y, 图例区, 图例
    ((363, 39, 695, 60), '拇展肌', (36, 100, 78, 448), (110, 489, 900, 640), (222, 298, 375, 452, 527, 604, 681, 757, 834), 500,
     (90, 650, 900, 895), ['* 显著低于单腿短足训练', '§ 显著高于 3DFA-D1E', '# 显著高于坐位短足训练', '¥ 显著低于其余 8 种训练']),
    ((1359, 31, 1688, 59), '腓骨长肌', (1044, 90, 1082, 435), (1100, 442, 1900, 610), (1205, 1282, 1360, 1442, 1520, 1602, 1680, 1760, 1838), 452,
     (1010, 645, 1940, 895), ['¥ 显著低于站立短足训练（原图误写为 ST）', '* 显著低于单腿短足、3DFA-D2E 和站立摆腿', '# 显著高于除提踵外的其余 7 种训练', '§ 显著高于其余 8 种训练']),
    ((330, 1033, 721, 1060), '拇长屈肌', (58, 1115, 99, 1462), (100, 1474, 900, 1620), (217, 293, 370, 446, 521, 600, 677, 755, 832), 1484,
     (70, 1630, 900, 1905), ['§ 显著低于其余训练', '* 显著低于单腿短足和站立摆腿', '# 显著高于坐位、站立、单腿短足，分趾和站立摆腿']),
    ((1294, 1013, 1721, 1039), '拇长伸肌', (1041, 1115, 1082, 1458), (1100, 1474, 1900, 1625), (1197, 1273, 1350, 1428, 1506, 1582, 1660, 1738, 1816), 1484,
     (1060, 1630, 1930, 1905), ['* 显著低于单腿短足训练', '§ 显著高于提踵', '# 显著高于 3DFA-D2E', '¥ 显著高于坐位短足训练'])]
im = raw(160); d = ImageDraw.Draw(im)
for tb, tt, yb, xr, ticks, ty, lb, leg in P4:
    im = wbox(im, tb, tt, 38); d = ImageDraw.Draw(im)
    im = vtext(im, yb, '肌肉活动（RMS，mV）', 31)
    d.rectangle(xr, fill='white')
    for x, t in zip(ticks, EX): rot_label(im, t, x + 8, ty + 6, 30)
    d.rectangle(lb, fill='white'); y = lb[1] + 18
    for t in leg: d.text((lb[0] + 8, y), t, font=font(32), fill=(0, 0, 0)); y += 62
save(titled(capbox(im, '原文图 4　四块肌肉在 9 种训练中 5 秒持续收缩中间 3 秒的肌电幅值（箱线图）：A 拇展肌，B 腓骨长肌，C 拇长屈肌，D 拇长伸肌。纵轴单位原图标为 mV，正文写的是 µV；C 图里的 Δ 和 ¥ 原图没有给出图例'),
            '结果：四块肌肉各自被哪些训练“点亮”（原文图 4，编者中文覆盖）'), 5)

# 编者估读的中位数热图（按每块肌肉自身最大值归一，因为幅值未标准化、不能跨肌肉比）
plt = chart_style()
MED = {'拇展肌 ABH': [55, 105, 140, 30, 112, 48, 85, 88, 142], '腓骨长肌 PL': [18, 35, 62, 28, 27, 125, 100, 147, 88],
       '拇长屈肌 FHL': [13, 34, 40, 78, 20, 88, 86, 77, 47], '拇长伸肌 EHL': [27, 63, 85, 50, 62, 38, 28, 31, 41]}
Mx = np.array([np.array(v) / max(v) for v in MED.values()]).T
fig, ax = plt.subplots(figsize=(10.9, 7.4))
ax.imshow(Mx, cmap='YlOrRd', vmin=0, vmax=1.05, aspect='auto')
for i in range(9):
    for j, k in enumerate(MED):
        v = Mx[i, j]; ax.text(j, i, f'{v * 100:.0f}%', ha='center', va='center', fontsize=13, color='white' if v > 0.65 else '#222')
ax.set_xticks(range(4)); ax.set_xticklabels(list(MED), fontsize=13); ax.xaxis.tick_top()
ax.set_yticks(range(9)); ax.set_yticklabels(['坐位短足', '站立短足 ★', '单腿短足 ★', '毛巾卷', '分趾', '3DFA-D1E', '3DFA-D2E', '提踵 ★', '站立摆腿 ★'], fontsize=13)
ax.set_xticks(np.arange(-.5, 4), minor=True); ax.set_yticks(np.arange(-.5, 9), minor=True); ax.grid(which='minor', color='white', lw=2); ax.tick_params(which='minor', length=0)
ax.set_xlabel('数值 = 该训练中位数 ÷ 该肌肉 9 种训练里最高的中位数（编者从原文图 4 估读）；★ = 负重训练', fontsize=11)
figsave(plt, fig, '编者整理：哪个训练最“点”哪块肌肉（只能同一块肌肉内部比）', 6)

phases('落到临床：拇外翻足部训练怎么挑（编者观点）', [
    ('想练拇展肌（把拇趾往内拉的那块）', GR, (40, 120, 60), [
        '首选单腿短足、站立摆腿、分趾；站立短足和提踵次之',
        '毛巾卷几乎不用拇展肌，主要是拇长屈肌在干活；坐位短足也偏低，适合作为入门']),
    ('想练腓骨长肌和拇长屈肌（第一跖列和拇趾的“下压”）', LT, TEAL, [
        '提踵和三维足踝对角线 1（3DFA-D1E）最高；对角线 2 和毛巾卷对拇长屈肌也高',
        '提踵时把重量压在拇趾上，是原文的做法']),
    ('拇长伸肌要不要避开', OR, RED, [
        '拇长伸肌外移被认为会加重外翻，但这项研究没法回答“该多用还是少用”它',
        '单腿短足里它也被明显激活，做短足时留意别让拇趾翘起']),
    ('别过度解读', PK, RED, [
        '17 名年轻女性、一次测试的肌电幅值，不等于长期训练能矫正外翻角或减轻疼痛',
        '幅值没有做最大收缩标准化，只能看同一块肌肉在不同训练间的高低',
        '每块肌肉做了 36 次两两比较却没有校正，零星的“显著”要打折扣；拇长屈肌是深层肌，表面电极可能混入邻近肌肉信号',
        '负重训练普遍更能调动拇展肌、腓骨长肌和拇长伸肌，组合几种不同类型的训练比只做一种更合理']),
], 7)

# 封面：原文图 2 三张小腿和足的照片（原图恰好接近 900×383 比例），抹掉肌肉缩写
im = heal(raw(104), dark_mask(raw(104), [(44, 220, 88, 248), (52, 377, 125, 407), (762, 282, 808, 308), (648, 442, 718, 473),
                                          (1298, 384, 1374, 413), (1311, 482, 1386, 511)], thr=85, grow=3))
cover_from(im)
