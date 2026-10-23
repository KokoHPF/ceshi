#!/usr/bin/env python3
"""腘绳肌拉伤诊断、康复和预防推文配图：首图、原文图（英文换成中文）、编者整理卡片、封面
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


def vec_fig(pno, clip, z, mp):
    """矢量图（流程图）：按 PDF 文字块位置刷底色后写中文。mp：英文 -> 中文"""
    page = doc[pno]; im = Image.frombytes('RGB', *(lambda pm: ((pm.width, pm.height), pm.samples))(page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip)))
    a = np.asarray(im); d = ImageDraw.Draw(im)
    for b in page.get_text('dict', clip=clip)['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                t = s['text'].strip()
                if t not in mp: continue
                x0, y0, x1, y1 = [(v - o) * z for v, o in zip(s['bbox'], (clip.x0, clip.y0, clip.x0, clip.y0))]
                x0, y0, x1, y1 = round(x0) - 2, round(y0) - 1, round(x1) + 2, round(y1) + 1
                ring = np.concatenate([a[max(y0 - 3, 0), x0:x1], a[min(y1 + 3, a.shape[0] - 1), x0:x1]])
                bg = tuple(int(c) for c in np.median(ring, 0)); fs = round(s['size'] * z)
                if l['dir'][1] != 0:
                    im = vtext(im, (x0, y0, x1, y1), mp[t], fs, bg=bg); d = ImageDraw.Draw(im)
                else:
                    d.rectangle([x0, y0, x1, y1], fill=bg)
                    d.text(((x0 + x1) / 2, (y0 + y1) / 2), mp[t], font=font(fs), fill=(0, 0, 0), anchor='mm')
    return im


def ctable(title, hdr, cw, rows, n, fs=22):
    """编者整理的对照表卡片"""
    W = 1200; H = 64 + sum(max(para_h(t, fs, w - 24, gap=6) for t, w in zip(r, cw)) + 24 for r in rows)
    im = Image.new('RGB', (W, H + 20), 'white'); dr = ImageDraw.Draw(im); x = 20
    for t, w in zip(hdr, cw): dr.rectangle([x, 10, x + w, 64], fill=TEAL); dr.text((x + 12, 22), t, font=font(26), fill='white'); x += w
    y = 64
    for k, r in enumerate(rows):
        h = max(para_h(t, fs, w - 24, gap=6) for t, w in zip(r, cw)) + 24; x = 20
        for j, (t, w) in enumerate(zip(r, cw)):
            dr.rectangle([x, y, x + w, y + h], fill=LT if k % 2 else 'white', outline=(210, 210, 210))
            para(dr, x + 12, y + 12, t, fs, w - 24, fill=RED if j == 0 else INK, gap=6); x += w
        y += h
    save(titled(im.crop((0, 0, W, y + 14)), title), n)


# 首图：原题直译
title_card('临床述评 · JOSPT 2010',
           ['腘绳肌拉伤：诊断、康复和', '损伤预防的建议'],
           ['Hamstring Strain Injuries: Recommendations for Diagnosis,', 'Rehabilitation, and Injury Prevention'],
           'Heiderscheit BC, Sherry MA, Silder A, Chumanov ES, Thelen DG',
           'J Orthop Sports Phys Ther. 2010;40(2):67-81. doi:10.2519/jospt.2010.3047',
           '美国威斯康星大学麦迪逊分校骨科与康复系、生物医学工程系、机械工程系')

# 原文图 1：矢量图，英文换成中文
mp = {'Semitendinosus': '半腱肌', 'Semimembranosus': '半膜肌', 'Biceps femoris': '股二头肌', 'long head': '长头', 'short head': '短头',
      'Biceps Femoris Long Head': '股二头肌长头', 'Activation': '激活', '': '', 'L (mm)': 'ΔL（mm）', 'Power (W)': '功率（W）',
      'Time of': '拉长最大', 'peak stretch': '的时刻', 'Energy': '能量', 'absorption': '吸收', 'Gait Cycle (%)': '步态周期（%）'}
im = vec_fig(1, pymupdf.Rect(40, 95, 362, 312), 5, mp)
one(im, '原文图 1　A 腘绳肌包括半膜肌、半腱肌和股二头肌，高速跑时最常伤的是股二头肌长头；B 跑步摆动相里，股二头肌长头在激活的同时被拉长（ΔL 为相对直立位的长度变化），并吸收减速摆动腿的能量，这正是“拉长收缩”受伤的条件。横轴为步态周期，下方小人示意对应时相',
    '为什么跑快了容易伤（原文图 1）', 2)

ctable('两种腘绳肌拉伤：冲刺型和拉伸型（编者据原文表 1、表 2 整理）', ['', '冲刺型（最大或接近最大速度跑）', '拉伸型（屈髋 + 伸膝到极限）'], [190, 480, 470], [
    ('典型项目', '需要高速跑的运动', '舞蹈、踢腿'),
    ('受伤肌肉', '主要是股二头肌长头，其次半腱肌', '半膜肌近端肌腱'),
    ('部位', '腱膜和相邻肌纤维，近端多于远端', '近端肌腱和 / 或肌腱结合部'),
    ('距坐骨结节', '6.7 ± 7.1 cm（-2.1～21.8）', '-2.3 ± 0.8 cm（-3.4～1.1），负值表示在坐骨结节最低点以上'),
    ('MRI 损伤长度', '18.7 ± 7.4 cm', '9.8 ± 5.0 cm'),
    ('瘀斑', '少', '无'),
    ('直腿抬高缺失', '40%', '20%'),
    ('屈膝力量缺失', '60%', '20%'),
    ('疼痛', '中度', '轻'),
    ('最痛点距坐骨结节', '12 ± 6 cm（5～24）', '2 ± 1 cm（1～3）'),
    ('疼痛区长度', '11 ± 5 cm（5～24）', '5 ± 2 cm（2～9）'),
    ('回到伤前水平（中位数）', '16 周（6～50）', '50 周（30～76）')], 3)

ctable('腘绳肌拉伤还是牵涉痛（原文表 3，改编自 Brukner 和 Khan）', ['症状 / 体征', '腘绳肌拉伤', '其他来源牵涉到大腿后侧'], [250, 420, 470], [
    ('起病', '突然', '突然或逐渐'),
    ('疼痛', '轻到重', '轻到中；可能描述为发紧或抽筋感'),
    ('功能', '走、跑困难', '走或跑时症状变化不大；运动中甚至减轻，运动后加重'),
    ('局部血肿、瘀青', '较重的拉伤可能有', '无'),
    ('触诊', '局部可明显压痛；损伤处可摸到凹陷', '轻微或无'),
    ('力量下降', '明显', '轻微或无'),
    ('柔韧性下降', '明显', '轻微'),
    ('Slump 试验', '阴性', '常为阳性'),
    ('臀部扳机点', '按压不影响腘绳肌症状', '按压可能复现腘绳肌症状'),
    ('腰椎 / 骶髂检查', '偶有异常', '常有异常'),
    ('局部超声或 MRI', '异常（很轻的拉伤除外）', '正常')], 4)

phases('急性腘绳肌拉伤怎么查（编者根据原文整理）', [
    ('病史', LT, TEAL, [
        '多为某个动作中突然大腿后侧痛，最常见是高速跑；可能听到“啪”的一声（近端肌腱受累更常见），坐着时坐骨结节痛也提示近端肌腱',
        '问清受伤机制：冲刺型恢复较快，拉伸型（舞蹈、踢腿）恢复慢得多；没有明确受伤动作时要考虑其他来源']),
    ('力量和活动度', GR, (40, 120, 60), [
        '俯卧、髋 0° 伸展，在屈膝 15° 和 90° 两个位置抗阻屈膝；小腿内旋 / 外旋可偏向内侧 / 外侧腘绳肌；伸髋力量在屈膝 90° 和 0° 各测一次',
        '诱发疼痛和无力一样重要，都要和健侧对比',
        '被动直腿抬高（正常约 80°）和主动伸膝试验（正常可伸到 20°）；急性期常被疼痛限制，不一定反映真实长度']),
    ('触诊、鉴别和影像', OR, RED, [
        '伸膝位找最痛点，量它到坐骨结节的距离和疼痛区长度：最痛点越靠近坐骨结节，恢复越慢',
        'Slump 试验阳性提示神经张力或腰椎来源；还要和内收肌拉伤区分',
        '除非怀疑撕脱骨折，X 线意义不大；超声和 MRI 都能看急性水肿出血，MRI 看深部、既往伤和损伤大小更准；MRI 损伤长度和横截面积与停训时间成正比，但预测不了再伤']),
], 5)

one(raw(279), '原文图 2　右侧股二头肌长头高速跑受伤后的 T2 加权冠状位 MRI：A 伤后第 10 天，损伤处（箭头）明显水肿出血（高信号）；B 第 30 天仍有积液，并已出现大量瘢痕（低信号）。值得注意的是，这名运动员伤后第 23 天就获准回到运动',
    '伤后 30 天，瘢痕已经形成（原文图 2）', 6)

phases('第 1 阶段：保护（编者据原文附录整理）', [
    ('目标', LT, TEAL, ['保护瘢痕形成；尽量减少肌萎缩']),
    ('注意', OR, RED, [
        '避免过度主动或被动拉长腘绳肌；以疼痛出现为活动范围上限，步子迈小些，重者用拐；拄拐时别长时间主动屈膝',
        '每天冰敷 2～3 次（冰杯 3～5 分钟，冷敷包 15～20 分钟）；NSAIDs 有争议，可用对乙酰氨基酚代替，多数人靠冰敷和调整活动就够']),
    ('每天练（全程无痛，强度由轻到中）', GR, (40, 120, 60), [
        '固定自行车 10 分钟',
        '侧向跨步、交叉步（grapevine）：各 10 m，3 × 1 分钟，低到中强度，速度和步幅以不痛为准',
        '原地快速小碎步 2 × 1 分钟',
        '俯卧平板支撑、侧平板支撑各 5 × 10 秒；仰卧屈膝桥 10 × 5 秒',
        '单腿平衡，从睁眼到闭眼，4 × 20 秒；不单独做腘绳肌抗阻']),
    ('进入第 2 阶段的条件', PK, RED, [
        '正常步幅走路不痛；很慢的慢跑不痛；俯卧屈膝 90° 徒手肌力测试，抗 50%～70% 次最大阻力的等长收缩不痛']),
], 7)

phases('第 2 阶段：逐步加长、加速（编者据原文附录整理）', [
    ('目标', LT, TEAL, ['恢复无痛的腘绳肌力量，从中段长度逐步练到更长的长度；发展躯干和骨盆的神经肌肉控制，动作速度逐步加快']),
    ('注意', OR, RED, [
        '仍有无力时避免把腘绳肌拉到末端；训练后冰敷 10～15 分钟；一般不再用 NSAIDs，以免掩盖疼痛、进阶过猛',
        '跑速一般不超过最大速度的 50%；原文作者经验是不必专门牵伸，活动度会随疼痛肿胀消退恢复']),
    ('每周 5～7 天', GR, (40, 120, 60), [
        '固定自行车 10 分钟；侧滑步、交叉步慢跑各 10 m，3 × 1 分钟，中到高强度；拳击步 10 m，2 × 1 分钟',
        '转体平板支撑，每侧停 5 秒，2 × 10 次；仰卧屈膝桥走出（图 3），3 × 10 次',
        '单腿平衡风车触地（不负重），每侧手臂 4 × 8 次；弓步走加转体、对侧手摸脚尖和 T 字抬起，每腿 2 × 10 步',
        '单腿平衡、躯干前倾加对侧伸髋，每腿 5 × 10 秒',
        '先在额状面、水平面动，再逐步过渡到矢状面；离心力量在功能动作中、肌肉中段长度、次最大强度开始']),
    ('进入第 3 阶段的条件', PK, RED, [
        '俯卧屈膝 90° 徒手肌力测试达 5/5 且不痛；向前、向后慢跑不痛（正文写 50% 最大速度，附录写中等强度）']),
], 8)

one(raw(394), '原文图 3　仰卧屈膝桥走出：A 从仰卧臀桥开始；B、C 保持臀桥，双脚一步步往远离臀部的方向走出去',
    '仰卧屈膝桥走出（原文图 3）', 9)

phases('第 3 阶段：专项和末端离心（编者据原文附录整理）', [
    ('目标', LT, TEAL, ['所有活动无症状（不痛、不紧）；全范围、各速度下向心和离心力量正常；继续提高躯干骨盆控制，并融入专项动作']),
    ('注意', OR, RED, ['活动度不再限制；但达到回场标准前避免冲刺和爆发加速；有痛、紧或僵时不做全强度；训练后按需冰敷 10～15 分钟']),
    ('每周 4～5 天', GR, (40, 120, 60), [
        '固定自行车 10 分钟；侧滑步、交叉步慢跑各 30 m，3 × 1 分钟；拳击步 10 m，2 × 1 分钟，中到高强度',
        'A 跳步、B 跳步（B 跳步先伸膝再伸髋，模拟跑步摆动末期），抬膝高度逐步增加，不痛为准',
        '前后加速跑 3 × 1 分钟，距离 5 m→10 m→20 m',
        '持哑铃转体平板支撑，每侧停 5 秒，2 × 10 次；仰卧单腿椅上臀桥（图 4），3 × 15 次，由慢到快',
        '持哑铃单腿平衡风车触地（图 5），每侧手臂 4 × 8 次；持哑铃弓步走转体摸脚尖加 T 字抬起，每腿 2 × 10 步',
        '包含姿势控制、速度逐步提高的专项训练，加入各种头部和躯干姿势的快速变化']),
], 10)

one(raw(440), '原文图 4　仰卧单腿椅上臀桥：A 一条腿放在固定物上；B 抬起髋和骨盆离开地面', '仰卧单腿椅上臀桥（原文图 4）', 11)
one(raw(439), '原文图 5　持哑铃单腿平衡风车触地：A 单腿站、哑铃举过头；B 有控制地做风车动作；C 结束时哑铃触地', '持哑铃单腿风车触地（原文图 5）', 12)

phases('回场标准（原文附录）', [
    ('力量完全且不痛', LT, TEAL, [
        '俯卧屈膝 90° 和 15° 两个位置，最大用力徒手肌力测试连续 4 次不痛',
        '等速测试：离心腘绳肌（30°/s）与向心股四头肌（240°/s）的比值，双侧差距 <5%',
        '等速向心屈膝（60°/s）峰力矩出现的屈膝角度两侧对称']),
    ('活动度完全且不痛', GR, (40, 120, 60), ['髋、膝全范围活动无痛、无发紧']),
    ('专项动作', OR, RED, [
        '接近最大速度完成专项动作不痛，例如跑类项目做递增速度冲刺测试',
        '原文估计三阶段一般需 2～6 周，应按标准而不是天数进阶；组数次数要个体化']),
], 13)

one(raw(523), '原文图 6　受伤数月后，股二头肌长头近端肌腱结合部旁仍可见瘢痕（箭头，低信号）：A T1 加权快速自旋回波轴位；B 三维 IDEAL-SPGR 序列重组的冠状位同相位图像。这类瘢痕可长期存在（伤后 5～23 个月）',
    '回场以后，瘢痕还在（原文图 6）', 14)

phases('预防：哪些做法有证据（编者根据原文整理）', [
    ('有证据支持', GR, (40, 120, 60), [
        '把离心腘绳肌训练纳入日常训练：精英足球运动员赛季前和赛季中加练，腘绳肌拉伤风险比 0.43（95% CI 0.19～0.98）',
        '等速测试发现离心腘绳肌 / 向心股四头肌失衡（双侧差 20%）的人，受伤风险约为 4.66 倍；纠正到差距 <5% 后，复发者 12 个月内未再伤',
        '离心训练易引起延迟性肌肉酸痛，负荷和强度要逐步加']),
    ('有希望、证据还少', LT, TEAL, [
        '躯干和骨盆的神经肌肉控制训练：高抬腿、快速支撑跑、前倾起跑、爆发起跑等；跑步中变换躯干姿势的训练，2 年里伤病平均减少 70%',
        '康复期渐进敏捷和躯干稳定训练（PATS）比牵伸加力量（STST）再伤少：回场 2 周 0% vs 55%，1 年 8% vs 70%']),
    ('没有证据', OR, RED, [
        '单纯牵伸腘绳肌没被证明能减少拉伤；股四头肌、屈髋肌牵伸的效果未知',
        '治疗性超声、按摩、电疗缺乏促进愈合的证据']),
], 15)

# 封面：原文图 5 单腿风车触地三联照片，裁成 900×383，抹掉分图字母
im = raw(439); m = np.zeros((im.height, im.width), bool)
for x0 in (14, 320, 997): m[8:52, x0:x0 + 34] = True
im = heal(im, m); cover_from(im, 0.5, 0.6)
