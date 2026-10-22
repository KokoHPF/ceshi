#!/usr/bin/env python3
"""渐进性肌腱负荷训练治疗髌腱病随机试验推文配图：首图、原文图（英文换成中文）、编者整理卡片和图表、封面
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
title_card('随机临床试验 · British Journal of Sports Medicine 2021',
           ['渐进性肌腱负荷训练治疗髌腱病的有效性：', '一项随机临床试验'],
           ['Effectiveness of progressive tendon-loading exercise therapy in patients',
            'with patellar tendinopathy: a randomised clinical trial'],
           'Breda SJ, Oei EHG, Zwerver J, Visser E, Waarsing E, Krestin GP, de Vos RJ',
           'Br J Sports Med. 2021;55(9):501-509. doi:10.1136/bjsports-2020-103403',
           '荷兰鹿特丹伊拉斯姆斯大学医学中心 · JUMPER 研究（NCT02938143）')

one(raw(125), '原文图 1　膝痛定位图。初筛时请受试者选一张最符合自己疼痛位置的图：A 膝内侧痛；B 膝外侧痛；C 膝后方痛；D 髌骨后方和周围痛；E 髌骨正下方或沿髌腱走行痛；F 髌骨正上方痛。只选 E 才算符合入组',
    '受试者怎么自报疼痛位置（原文图 1）', 2)

# 原文图 2：两组训练流程，框内英文换成中文
im = raw(167)
im = zh_boxes(im, [
    ((551, 6, 1241, 128), '髌腱病\n（跳跃膝）', 34, 'c'),
    ((720, 243, 1075, 300), '随机分组', 34, 'c'),
    ((6, 440, 619, 613), '诱发疼痛的\n离心训练', 34, 'c'),
    ((1172, 441, 1787, 615), '四阶段\n渐进性肌腱负荷训练', 34, 'c'),
    ((64, 690, 588, 863), '阶段 1：\n单腿下斜板深蹲', 34, 'c'),
    ((743, 690, 1779, 811), '阶段 1：\n等长（静力）训练', 34, 'c'),
    ((743, 1281, 1779, 1403), '阶段 2：\n等张（动态）训练', 34, 'c'),
    ((743, 1872, 1779, 1994), '阶段 3：\n储能（爆发性）训练', 34, 'c'),
    ((64, 2141, 588, 2314), '阶段 2：\n专项训练', 34, 'c'),
    ((90, 2468, 565, 2552), '重返运动', 40, 'c'),
    ((743, 2453, 1788, 2575), '阶段 4：\n专项训练', 34, 'c')], 1)
one(im, '原文图 2　两组的训练方案示意（图为示范动作，完整方案见原文在线附录）。左：对照组，诱发疼痛的离心训练（EET）；右：干预组，四阶段渐进性肌腱负荷训练（PTLE）。原文图注把 PTLE 误写成 PLTE',
    '两组分别练什么（原文图 2）', 3)

phases('两组训练方案对照（编者根据原文整理）', [
    ('共同部分', LT, TEAL, [
        '共 24 周，无人监督的居家 / 健身房训练：一次面诊讲解，加手册和教学视频网站',
        '两组都另做针对危险因素的训练：股四头肌、腘绳肌和小腿肌群牵伸，弹力带练髋外展、伸髋，小腿力量和核心稳定',
        '两组都有运动医学医生宣教，用疼痛监测模型讲清负荷和疼痛的关系：明显诱发髌腱痛的运动至少减量或停 4 周，其余活动控制在 VAS ≤3']),
    ('干预组 PTLE：在可接受疼痛内逐级加载', GR, (40, 120, 60), [
        '阶段 1 等长：单腿腿举或伸膝，屈膝 60° 维持 45 秒 × 5 次，约 70% 最大自主收缩，每天做',
        '阶段 2 等张：第 1 天等长、第 2 天等张交替；单腿腿举或伸膝，从 4 组 × 15 次（屈膝 10°～60°）进阶到 4 组 × 6 次（接近伸直到屈膝 90°），逐步加重',
        '阶段 3 储能：每 3 天一次跳跃深蹲、跳箱、变向跑，从双腿 3 组 × 10 次到单腿 6 组 × 10 次；等长、等张继续',
        '阶段 4 专项：每 2～3 天一次专项训练，逐步回到运动',
        '进阶条件：单腿深蹲 VAS ≤3 且本阶段已练满 1 周；最早 4 周可回到运动；研究为受试者付了健身房会费']),
    ('对照组 EET：诱发疼痛的离心训练', OR, RED, [
        '阶段 1：25° 下斜板单腿深蹲，患腿下蹲、健腿为主站起，每天 2 次，持续 12 周；要求练的时候疼（VAS ≥5），不疼或只微疼就背包加重',
        '阶段 1 完全做到、负重离心时 VAS ≤3 后进入阶段 2 专项训练；4 周后、单腿深蹲 VAS ≤3 即可回到运动']),
], 4)

im = raw(224)
L = lambda *ls: '\n'.join(ls)
im = zh_boxes(im, [
    ((539, 5, 1421, 88), '272 名运动员接受资格筛查', 36, 'c'),
    ((1104, 118, 1902, 617), L('171 名排除', '　53 退出', '　40 疼痛不只在髌下区前方', '　25 年龄 <18 或 >35 岁', '　18 不从事肌腱负荷类运动',
                               '　18 VISA-P ≥80 分', '　12 已在每天做髌腱病训练', '　 5 既往膝关节手术'), 34, 'l'),
    ((464, 652, 1516, 789), '101 名在研究地点接受临床和影像评估', 36, 'c'),
    ((1105, 852, 1902, 1148), L('25 名排除', '　19 怀疑髌股疼痛', '　 3 退出', '　 2 超声证实滑囊炎', '　 1 VISA-P ≥80 分'), 34, 'l'),
    ((780, 1222, 1206, 1296), '76 名随机分组', 38, 'c'),
    ((5, 1384, 733, 1635), L('38 名随机分到渐进性', '肌腱负荷训练组（PTLE），', '在可接受疼痛内训练'), 34, 'c'),
    ((1245, 1382, 1973, 1634), L('38 名随机分到诱发疼痛的', '离心训练组（EET），', '在 25° 下斜板上训练'), 34, 'c'),
    ((8, 1669, 736, 1910), L('5 名未纳入分析', '原因：未回复（2）、', '没时间（3）'), 32, 'c'),
    ((1246, 1670, 1973, 1910), L('7 名未纳入分析', '原因：未回复（3）、没时间（3）、', '因踝扭伤退出（1）'), 32, 'c'),
    ((778, 1747, 1200, 1829), '12 周随访', 36, 'c'),
    ((6, 1948, 734, 2189), L('1 名未纳入分析', '原因：未回复（1）'), 32, 'c'),
    ((1245, 1949, 1973, 2191), L('8 名未纳入分析', '原因：未回复（5）、没时间（2）、', '因踝扭伤退出（1）'), 32, 'c'),
    ((780, 2027, 1202, 2109), '24 周随访', 36, 'c'),
    ((5, 2229, 733, 2311), '37 名纳入主要分析', 36, 'c'),
    ((1246, 2229, 1974, 2312), '30 名纳入主要分析', 36, 'c')], 1)
one(im, '原文图 3　CONSORT 流程图。272 人报名，76 人随机分组；24 周时 PTLE 组缺 1 人、EET 组缺 8 人，主要分析分别纳入 37 人和 30 人，缺失数据没有插补',
    '受试者是怎么筛下来的（原文图 3）', 5)

im = raw(253)
im = zh_label(im, [(187, 45, 478, 72, '干预组（PTLE）', 22, 'l'), (187, 117, 413, 142, '对照组（EET）', 22, 'l'),
                   (488, 440, 676, 463, '误差线：±1 个标准误', 18, 'c'),
                   (186, 552, 291, 576, '基线', 22, 'c'), (386, 552, 494, 576, '12 周', 22, 'c'), (590, 552, 698, 576, '24 周', 22, 'c'),
                   (400, 604, 474, 632, '时间', 24, 'c')])
im = vtext(im, (0, 88, 30, 452), '平均 VISA-P 评分（0～100）', 22)
one(im, '原文图 4　两组 VISA-P 平均分随时间的变化（未校正）。红线为干预组 PTLE（原图误标为 PLTE），蓝线为对照组 EET；误差线为 ±1 个标准误。VISA-P 满分 100，越高越好',
    'VISA-P 评分随时间的变化（原文图 4）', 6)

plt = chart_style()
fig, ax = plt.subplots(figsize=(10.9, 4.6))
lab = ['达到最小临床重要差异\n（≥13 分）', '以伤前水平\n回到想做的运动', '满意\n（很好 + 好）', '满意度\n“很好”', '肌腱专项训练\n依从性']
a = [87, 43, 81, 38, 40]; b = [77, 27, 83, 10, 49]; pv = ['p=0.24', 'p=0.16', 'p=0.81', 'p=0.009', 'p=0.33']
x = np.arange(len(lab)); w = 0.36
r1 = ax.bar(x - w / 2, a, w, color='#D2553C', label='PTLE 组'); r2 = ax.bar(x + w / 2, b, w, color='#5B8DB8', label='EET 组')
for r in list(r1) + list(r2): ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 1.5, f'{r.get_height():.0f}%', ha='center', fontsize=11)
for i, p in enumerate(pv): ax.text(i, 104, p, ha='center', fontsize=11, color='#D2553C' if p == 'p=0.009' else '#666666')
ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=11.5); ax.set_ylim(0, 112); ax.set_ylabel('24 周时的比例（%）', fontsize=12)
ax.legend(loc='upper right', bbox_to_anchor=(1, 0.93), frameon=False, fontsize=11.5); ax.spines[['top', 'right']].set_visible(False)
figsave(plt, fig, '24 周时的次要结局（编者据原文表 2 和正文绘制）', 7)

im = raw(275)
im = zh_label(im, [(843, 28, 1000, 56, '对照组', 22, 'l'), (843, 60, 1028, 90, '干预组', 22, 'l'),
                   (130, 485, 250, 512, '12 周', 22, 'c'), (540, 485, 660, 512, '24 周', 22, 'c')])
im = vtext(im, (0, 0, 27, 515), 'VISA-P 评分相对基线的变化', 22)
one(im, '原文图 5　每名患者 VISA-P 评分相对基线的变化。空心圆为对照组 EET，实心圆为干预组 PTLE（原文图注误写成 PLTE）；每个时间点最右侧的点和误差线是组间差值及其 95% 置信区间。个体差异很大，两组都有人变差',
    '每个人的变化（原文图 5）', 8)

phases('落到临床：怎么用这篇文献（编者整理）', [
    ('可以带走的', LT, TEAL, [
        '慢性髌腱病（多数已病 2 年、治过没好）的年轻运动员，练 24 周两种方案都明显改善；PTLE 在 24 周时平均多 9 分左右',
        '“在可接受疼痛内（VAS ≤3）逐级加载”的方案，练的时候更不疼（VAS 2 比 4），满意度“很好”的人更多',
        '从等长→等张→储能→专项的顺序给了一个清楚的进阶框架，也给出了每阶段的组数、次数和进阶条件']),
    ('需要打折扣的', OR, RED, [
        '组间差值 9 分低于作者自己设定的最小临床重要差异 13 分；达到 13 分的人数、回到伤前运动水平的比例，两组差别都不显著',
        'EET 组失访 8 人、PTLE 组只 1 人，又没插补；最坏情形的敏感性分析下，PTLE 的优势就不成立了',
        '依从性只有 40%～50%，而且是无人监督；结论更像“比离心训练不差、可能更好”，而不是“明确更优”']),
    ('怎么落地', GR, (40, 120, 60), [
        '把疼痛监测（单腿深蹲激发试验 VAS ≤3）作为加量的依据，不必硬要“练到疼”',
        '等长期可当作起步和止痛手段，但别停在等长，储能（跳跃、变向）阶段要按时加进来再回专项',
        '对依从性差、恢复慢的患者考虑有人监督的训练，并个体化调整']),
], 9)

# 封面：原文图 2 阶段 1 的两张示范照片（腿举机等长、单腿靠墙静蹲），裁成 900×383
im = raw(167).crop((747, 817, 1776, 1212))
cover_from(im, 0.5, 0.5)
