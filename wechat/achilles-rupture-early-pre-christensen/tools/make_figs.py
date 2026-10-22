#!/usr/bin/env python3
"""Christensen 等 2024 Pilot Feasibility Stud 急性跟腱断裂早期渐进抗阻训练方案的可行性：首图为原题直译标题卡；
原文图 1 为照片（图内只有分图字母），图注译成中文；原文图 2 流程图为矢量图，按 PDF 文字位置覆盖中文；
原文表 1 时间表按原配色重排成中文，训练卡、结果图和临床卡为编者根据原文整理。
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


# 首图：原题直译
title_card('单组可行性研究 · Pilot and Feasibility Studies 2024',
           ['急性跟腱断裂早期渐进', '抗阻训练方案的可行性'],
           ['Feasibility of an early progressive resistance exercise program', 'for acute Achilles tendon rupture'],
           'Christensen M, Silbernagel KG, Zellers JA, Kjær IL, Rathleff MS',
           'Pilot Feasibility Stud. 2024;10:66. doi:10.1186/s40814-024-01494-4',
           '丹麦奥尔堡大学医院物理与作业治疗科 等')

# 原文图 1：训练照片（图内只有分图字母）
one(raw(79), '原文图 1　三项加做训练：A 穿步行靴坐位提踵；B 坐位提踵，上身前压增加负荷；C 弹力带踝跖屈；D 不同阻力的弹力带（黄、红、绿、蓝）',
    '早期加做的抗阻训练（原文图 1）', 2)

# 原文表 1：训练和固定时间表（编者按原表配色重排成中文）
BL, OG, DG, LG = (146, 205, 220), (228, 108, 10), (119, 147, 60), (196, 215, 155)
W = 1200; im = Image.new('RGB', (W, 760), 'white'); dr = ImageDraw.Draw(im)
L0, cw, rh, top = 190, 110, 64, 20
COL = {1: [], 2: [('等长', OG)], 3: [('活动度', BL), ('等长', OG), ('坐位提踵', OG)], 4: [('活动度', BL), ('等长', OG), ('坐位提踵', OG)],
       5: [('活动度', BL), ('等长', OG), ('坐位提踵', OG), ('弹力带 1', OG)],
       6: [('活动度', BL), ('弹力带 1', BL), ('站立等长', OG), ('坐位提踵', OG)]}
for w in (7, 8, 9): COL[w] = [('活动度', BL), ('弹力带 1', BL), ('站立等长', OG), ('坐位提踵', OG), ('弹力带 2', OG)]
for w, cells in COL.items():
    x = L0 + (w - 1) * cw
    for i, (t, c) in enumerate(cells):
        y = top + (4 - i) * rh; dr.rectangle([x, y, x + cw, y + rh], fill=c, outline='white', width=2)
        dr.text((x + cw / 2, y + rh / 2), t, font=font(24), fill=(20, 20, 20), anchor='mm')
dr.text((20, top + 10), '训练', font=font(28), fill=INK)
y = top + 5 * rh + 6
def band(y, label, segs, h=64):
    dr.text((20, y + h / 2), label, font=font(28), fill=INK, anchor='lm')
    for w0, w1, t, c in segs:
        x0, x1 = L0 + (w0 - 1) * cw, L0 + w1 * cw
        dr.rectangle([x0, y, x1, y + h], fill=c, outline=(180, 180, 180), width=2)
        dr.text(((x0 + x1) / 2, y + h / 2), t, font=font(24), fill=(20, 20, 20), anchor='mm')
    return y + h
y = band(y, '周', [(w, w, str(w), 'white') for w in range(1, 10)], 56)
y = band(y, '固定', [(1, 3, '步行靴，3 块楔垫', DG), (4, 5, '步行靴，2 块楔垫', LG), (6, 7, '步行靴，1 块楔垫', LG), (8, 9, '步行靴，无楔垫', LG)])
y = band(y, '负重', [(1, 2, '不负重', 'white'), (3, 4, '部分负重，双拐', 'white'), (5, 6, '部分负重，1～2 拐', 'white'), (7, 9, '完全负重，长距离用拐', 'white')])
y += 24
for t in ['蓝色 = 常规训练；橙色 = 本研究加做的训练', '活动度 = 控制范围的踝关节活动；等长 = 等长收缩；坐位提踵 = 穿开放的步行靴坐着提踵',
          '弹力带 1 = 轻阻力（黄、红）；弹力带 2 = 换更强的弹力带（红、蓝、绿）']:
    y = para(dr, 20, y, t, 24, W - 40, fill=GREY, gap=8)
save(titled(im.crop((0, 0, W, y + 10)), '9 周时间表（原文表 1，编者中文重排）'), 3)

phases('三项加做训练怎么做、怎么进阶（编者根据原文整理）', [
    ('① 踝跖屈等长收缩', OR, RED, ['穿着、扣好步行靴做，醒着时每小时一次（约每天 12 次），第 2～5 周共 4 周；表 1 显示第 6 周起换成站立位等长']),
    ('② 坐位提踵', OR, RED, ['打开步行靴、垫着当周数量的楔垫坐着做，每天 5 次，第 3 周开始',
                         '进阶：上身前倾压在大腿上加负荷（图 1B）']),
    ('③ 弹力带踝跖屈', OR, RED, ['每天 5 次，第 5 周开始；先用轻阻力（黄、红），第 7 周起换更强的弹力带']),
    ('剂量和安全规则', LT, TEAL, [
        '一周后开始，每周 1 次物理治疗师面对面指导，其余在家做，并记训练日记',
        '用 Borg CR10 自评用力程度，保持在“轻松”到“吃力”（2～5 分）之间，按感觉加减负荷',
        '踝背伸不超过中立位（0°）；训练不能引起肌腱突然或剧烈疼痛，肌肉酸痛可以接受',
        '每次训练前检查：断端无可触及的凹陷、足呈跖屈位、肌腱轻压痛可以但不应疼痛、周围轻度肿胀可以']),
], 4)

# 原文图 2：入组流程图（矢量图，按原文文字位置覆盖中文）
MP = {'Screening': '筛查', 'Inclusion': '纳入', 'Follow-up': '随访', 'Eligibility screening (n =29)': '资格筛查（n = 29）',
      'Included (n = 16)': '纳入（n = 16）', 'Follow-up 13 weeks (n = 16)': '随访 13 周（n = 16）', 'Excluded (n = 13)': '排除（n = 13）',
      'High rupture/tennis leg/partial (4)': '高位断裂/网球腿/部分断裂（4）', 'Comorbidity (3)': '合并症（3）',
      '>3 days delayed treatment (2)': '延迟 > 3 天治疗（2）', 'Age >65 (1)': '年龄 > 65 岁（1）', 'Injection (1)': '注射（1）',
      'Compliance (1)': '依从性（1）', 'Logistic (1)': '后勤原因（1）'}
im = vec_fig(5, pymupdf.Rect(120, 478, 490, 709), 4, MP)
save(titled(capbox(im, '原文图 2　入组流程：29 人筛查，排除 13 人，纳入 16 人，全部完成第 9 周和第 13 周随访'), '谁进了研究（原文图 2，编者中文覆盖）'), 5)

# 结果：可接受度和依从性
plt = chart_style()
fig, axs = plt.subplots(1, 2, figsize=(10.9, 4.8), gridspec_kw={'width_ratios': [1.25, 1]})
ax = axs[0]; LV = [('7 非常可以接受', 10, 9, '#1b7a5a'), ('6 可以接受', 5, 6, '#55b08a'), ('5 中等可以接受', 1, 1, '#b5dfc9')]
left = [0, 0]
for t, a9, a13, c in LV:
    ax.barh([1, 0], [a9, a13], left=left, color=c, label=t, height=0.55)
    for yy, v, l in ((1, a9, left[0]), (0, a13, left[1])): ax.text(l + v / 2, yy, str(v), ha='center', va='center', fontsize=13, color='white' if c != '#b5dfc9' else '#222')
    left = [left[0] + a9, left[1] + a13]
ax.axvline(13, color='#c0392b', ls='--', lw=1.5); ax.text(12.8, 1.45, '可行标准：≥ 13/16 人 ≥ 4 分', ha='right', fontsize=10.5, color='#c0392b')
ax.set_yticks([1, 0]); ax.set_yticklabels(['第 9 周', '第 13 周'], fontsize=13); ax.set_xlim(0, 16); ax.set_ylim(-0.5, 1.7)
ax.set_xlabel('人数（共 16 人；7 分制 Likert）', fontsize=11.5); ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, -0.38), ncol=3, frameon=False)
ax.set_title('可接受度：16 人全部 ≥ 5 分', fontsize=13); ax.spines[['top', 'right']].set_visible(False)
ax = axs[1]
ax.bar([0], [74], color='#2C8C9E', width=0.5); ax.text(0, 76, '平均 74%\n（范围 4%～117%）', ha='center', fontsize=11.5)
ax.bar([1], [15 / 16 * 100], color='#D2553C', width=0.5); ax.text(1, 96, '15/16 人\n完成 ≥ 50%', ha='center', fontsize=11.5)
ax.axhline(80, xmin=0.55, color='#c0392b', ls='--', lw=1.5); ax.text(1.35, 81, '标准 80%', fontsize=10.5, color='#c0392b')
ax.set_xticks([0, 1]); ax.set_xticklabels(['家庭训练完成率', '完成 ≥ 50% 的人数比例'], fontsize=11.5); ax.set_ylim(0, 120); ax.set_ylabel('%', fontsize=12)
ax.set_title('依从性：达到可行标准', fontsize=13); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout()
figsave(plt, fig, '结果：可接受度和依从性都过了线（编者据原文表 3 和正文绘制）', 6)

phases('落到临床：保守治疗的跟腱断裂，早期可以练什么（编者观点）', [
    ('可以借鉴', GR, (40, 120, 60), [
        '保守治疗、穿步行靴的 9 周里，不必只做活动度：第 2 周起加踝跖屈等长，第 3 周起加坐位提踵，第 5 周起加弹力带',
        '用 Borg 2～5 分自我调节负荷，配合每周一次面对面指导；摸着小腿肌肉收缩做，比超声更实用，也让患者更有信心',
        '每小时一次的等长收缩在患者能走动后很难坚持，可以随负重增加而减量']),
    ('守住的底线', OR, RED, [
        '背伸不过中立位，不引起肌腱突然或剧烈疼痛；每次训练前查断端凹陷、足的跖屈位和肿胀',
        '早期仍要关注深静脉血栓：本研究 16 人中有 1 例，发生在伤后 7～10 天']),
    ('别过度解读', PK, RED, [
        '这是 16 人的单组可行性研究，只回答“患者愿不愿意做、能不能坚持”，不能说明能减少力量缺失',
        '16 人里没有再断裂，但样本太小，按“三分之一法则”，真实再断裂率最高仍可能接近 19%，安全性还要大样本 RCT 验证',
        '只针对保守治疗、年龄 18～65 岁、伤后 3 天内开始治疗的患者']),
], 7)

# 封面：原文图 1A、1B 两张穿步行靴坐位提踵的照片，裁小腿和足
im = raw(79); ch = round(im.width * 383 / 900); y = 425
im.crop((0, y, im.width, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
