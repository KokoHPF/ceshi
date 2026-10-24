#!/usr/bin/env python3
"""肩胛骨体格检查技术要点（Selman 等 2026，Arthroscopy Techniques）小红书 3:4 图文卡片，1080×1440。
原文图 1～3 由 tools/render_figs.py 按页面渲染（含矢量箭头）并把英文标签改为中文，存于 src/zh/fig1～3.jpg。
用法：python3 xhs/make_cards.py <思源黑体目录> <输出目录>"""
import sys, re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

FD, OUT = sys.argv[1:3]; SERIES = '肩胛骨查体'
font_manager.fontManager.addfont(f'{FD}/NotoSansSC-Medium.otf'); plt.rcParams['font.family'] = font_manager.FontProperties(fname=f'{FD}/NotoSansSC-Medium.otf').get_name()
W, H = 1080, 1440
BG = (247, 242, 235); NAVY = (22, 50, 79); CORAL = (238, 99, 72); TEAL = (24, 128, 128)
YEL = (255, 212, 92); INK = (40, 40, 40); GREY = (120, 120, 120); WHITE = (255, 255, 255)
LCOR = (253, 232, 225); LTEAL = (222, 240, 238); LYEL = (255, 244, 210); LNAVY = (228, 234, 242)
_fc = {}


def F(w, s):
    k = (w, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(f'{FD}/NotoSansSC-{ {"R": "Regular", "M": "Medium", "B": "Bold", "K": "Black"}[w]}.otf', s)
    return _fc[k]


def zh(x):
    return Image.open(f'src/zh/fig{x}.jpg').convert('RGB')


def fit(im, w, h, fy=.5, fx=.5):
    """按比例缩放后居中裁切填满 w×h"""
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = round((im.width - w) * fx); y0 = round((im.height - h) * fy)
    return im.crop((x0, y0, x0 + w, y0 + h))


def rmask(w, h, r):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255); return m


def shadow(c, box, r=28, off=8, blur=18, alpha=40):
    x0, y0, x1, y1 = box
    sh = Image.new('RGBA', (x1 - x0 + 80, y1 - y0 + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([40, 40, 40 + x1 - x0, 40 + y1 - y0], r, fill=(60, 40, 20, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); c.paste(sh, (x0 - 40, y0 - 40 + off), sh)


def photo(c, im, box, r=26, fy=.5, fx=.5, tag=None, tagc=NAVY, sh=True):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    if sh: shadow(c, box, r)
    c.paste(fit(im, w, h, fy, fx), (x0, y0), rmask(w, h, r))
    if tag:
        d = ImageDraw.Draw(c); f = F('B', 30); tw = d.textlength(tag, font=f)
        d.rounded_rectangle([x0 + 14, y0 + 14, x0 + 42 + tw, y0 + 64], 14, fill=tagc)
        d.text((x0 + 28, y0 + 19), tag, font=f, fill=WHITE)


def panelbox(c, box, fill=WHITE, r=28, sh=True, outline=None):
    if sh: shadow(c, box, r)
    ImageDraw.Draw(c).rounded_rectangle(box, r, fill=fill, outline=outline, width=3 if outline else 0)


# ---- 富文本：**加粗强调色**，==黄色高亮== ----
def tokens(t):
    out = []
    for part in re.split(r'(\*\*.+?\*\*|==.+?==)', t):
        if not part: continue
        if part.startswith('**'): out.append((part[2:-2], 'em'))
        elif part.startswith('=='): out.append((part[2:-2], 'hl'))
        else: out.append((part, 'n'))
    return out


def layout(t, w, fs, wt='R'):
    """逐字排版；连续的数字、字母和 % 等符号不拆行，避免“1 / 00%”这样断开；标点不落行首"""
    lines = [[]]; cur = 0
    WORD = set('0123456789.%%~～-–/×:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ°²')
    for txt, st in tokens(t):
        f = F('B' if st != 'n' else wt, fs)
        i = 0
        while i < len(txt):
            ch = txt[i]
            if ch == '\n': lines.append([]); cur = 0; i += 1; continue
            j = i + 1
            if ch in WORD:
                while j < len(txt) and txt[j] in WORD: j += 1
            seg = txt[i:j]; sw = sum(f.getlength(x) for x in seg)
            if cur + sw > w and lines[-1] and not (len(seg) == 1 and seg in '，。、；：！？）」”'):
                lines.append([]); cur = 0
            for x in seg: cw = f.getlength(x); lines[-1].append((x, st, cw)); cur += cw
            i = j
    return lines


def rich(d, x, y, t, w, fs, col=INK, wt='R', lh=1.55, em=CORAL):
    for ln in layout(t, w, fs, wt):
        xx = x; i = 0
        while i < len(ln):
            st = ln[i][1]; j = i
            while j < len(ln) and ln[j][1] == st: j += 1
            s = ''.join(c for c, _, _ in ln[i:j]); ww = sum(cw for _, _, cw in ln[i:j])
            if st == 'hl': d.rectangle([xx - 2, y + fs * .55, xx + ww + 2, y + fs * 1.15], fill=YEL)
            d.text((xx, y), s, font=F('B' if st != 'n' else wt, fs), fill=em if st == 'em' else (NAVY if st == 'hl' else col))
            xx += ww; i = j
        y += round(fs * lh)
    return y


def textheight(t, w, fs, wt='R', lh=1.55):
    return len(layout(t, w, fs, wt)) * round(fs * lh)


def base(n, total, title, sub=None, tc=NAVY):
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    # 页码与栏目
    d.rounded_rectangle([60, 56, 200, 104], 24, fill=CORAL); d.text((80, 58), f'{n:02d}/{total:02d}', font=F('B', 32), fill=WHITE)
    d.text((222, 62), SERIES + ' · 文献精读', font=F('M', 28), fill=GREY)
    d.text((60, 128), title, font=F('K', 64), fill=tc)
    y = 128 + 92
    if sub: d.text((62, y), sub, font=F('M', 32), fill=GREY); y += 56
    # 页脚
    d.line([60, H - 78, W - 60, H - 78], fill=(222, 214, 202), width=2)
    d.text((60, H - 62), '骨科康复小黄', font=F('M', 24), fill=GREY)
    s = 'Selman 等 Arthrosc Tech 2026;15:e70203'; d.text((W - 60 - d.textlength(s, font=F('R', 22)), H - 60), s, font=F('R', 22), fill=GREY)
    return c, d, y + 10


def bullet_list(d, x, y, items, w, fs=32, dot=CORAL, gap=18, lh=1.5):
    for it in items:
        d.ellipse([x, y + fs * .42, x + 14, y + fs * .42 + 14], fill=dot)
        y = rich(d, x + 32, y, it, w - 32, fs, lh=lh) + gap
    return y


def num(d, x, y, k, col=CORAL, r=30, fs=34):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=col)
    s = str(k); d.text((x + r - d.textlength(s, font=F('K', fs)) / 2, y + r - fs * .68), s, font=F('K', fs), fill=WHITE)


def badge(d, x, y, t, col=NAVY, r=22, fs=26):
    w = max(2 * r, d.textlength(t, font=F('K', fs)) + 20)
    d.rounded_rectangle([x, y, x + w, y + 2 * r], r, fill=col)
    d.text((x + w / 2 - d.textlength(t, font=F('K', fs)) / 2, y + r - fs * .68), t, font=F('K', fs), fill=WHITE)
    return w


def render_items(c, y, items, fs, dry=False, X=60, Wd=960, gap=14, lg=10):
    d = ImageDraw.Draw(c); R = X + Wd
    for it in items:
        kind = it[0]
        if kind == 'h':
            if not dry: d.text((X, y), it[1], font=F('K', fs + 6), fill=it[2] if len(it) > 2 else NAVY)
            y += round((fs + 6) * 1.5)
        elif kind == 'steps':
            for k, t in it[1]:
                w = 44 if len(k) == 1 else 44 + (len(k) - 1) * 16
                if not dry: badge(d, X, y + 2, k, col=TEAL if len(k) == 1 else NAVY)
                y = (rich(d, X + w + 16, y, t, Wd - w - 16, fs, lh=1.45) if not dry else y + textheight(t, Wd - w - 16, fs, 'R', 1.45)) + lg
        elif kind == 'bul':
            for t in it[1]:
                if not dry:
                    d.ellipse([X, y + fs * .42, X + 14, y + fs * .42 + 14], fill=it[2] if len(it) > 2 else CORAL)
                    y = rich(d, X + 32, y, t, Wd - 32, fs, lh=1.45) + lg
                else: y += textheight(t, Wd - 32, fs, 'R', 1.45) + lg
        elif kind == 'box':
            _, title, t, fill, col = it
            hh = 24 + round((fs + 4) * 1.4) + textheight(t, Wd - 80, fs, 'R', 1.45) + 18
            if not dry:
                panelbox(c, (X, y, R, y + hh), fill=fill, sh=False); d = ImageDraw.Draw(c)
                d.text((X + 32, y + 18), title, font=F('K', fs + 4), fill=col)
                rich(d, X + 32, y + 24 + round((fs + 4) * 1.4), t, Wd - 80, fs, lh=1.45)
            y += hh
        y += gap
    return y


def figcard(n, total, title, sub, img, items, maxh=None, tag=None):
    """图片尽量大：先按字号量出文字高度，剩余空间都给图片"""
    nat = min(round(img.height * 960 / img.width), 900)
    for fs in (36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26):
        c, d, y0 = base(n, total, title, sub)
        th = render_items(c, 0, items, fs, dry=True)
        avail = H - 100 - y0 - 28 - th
        h = min(nat, avail)
        if h >= min(nat, 440) or fs == 26: break
    w = round(img.width * h / img.height)
    if w > 960: w = 960; h = round(img.height * w / img.width)
    x0 = 60 + (960 - w) // 2
    shadow(c, (x0, y0, x0 + w, y0 + h), 18)
    c.paste(img.resize((w, h), Image.LANCZOS), (x0, y0), rmask(w, h, 18))
    for f2 in range(42, fs - 1, -1):
        if y0 + h + 28 + render_items(c, 0, items, f2, dry=True) < H - 110: break
    render_items(c, y0 + h + 28, items, f2)
    return c

def put(c, img, x0, y0, w, h):
    shadow(c, (x0, y0, x0 + w, y0 + h), 18); c.paste(img.resize((w, h), Image.LANCZOS), (x0, y0), rmask(w, h, 18))


def two(c, y, a, b, ta, tb, h):
    """两张图并排，等高"""
    wa = round(a.width * h / a.height); wb = round(b.width * h / b.height); s = min(1, 940 / (wa + wb)); h = round(h * s)
    wa = round(a.width * h / a.height); wb = round(b.width * h / b.height); x0 = 60 + (960 - wa - wb - 20) // 2
    photo(c, a, (x0, y, x0 + wa, y + h), r=18, tag=ta, tagc=CORAL); photo(c, b, (x0 + wa + 20, y, x0 + wa + 20 + wb, y + h), r=18, tag=tb, tagc=TEAL)
    return y + h


def stackAB(im):
    """左右两幅分图改为上下排列，竖版卡片里更大"""
    m = 1018; a = im.crop((0, 0, m - 3, im.height)); b = im.crop((m + 3, 0, im.width, im.height))  # 图 5 两幅分图的分界列
    out = Image.new('RGB', (a.width, a.height + b.height + 16), (247, 242, 235)); out.paste(a, (0, 0)); out.paste(b, (0, a.height + 16)); return out


def auto(c, y, items, top=44):
    """字号取能放下的最大值（≤top）；还有空余时按比例加大条目间距，让版面铺满"""
    for fs in range(top, 23, -1):
        hgt = render_items(c, 0, items, fs, dry=True)
        if y + hgt < H - 110: break
    spare = H - 110 - y - hgt
    nl = sum(len(it[1]) if it[0] in ('steps', 'bul') else 1 for it in items)
    lg = 10 + min(60, spare // max(1, nl + len(items)))
    gap = 14 + min(80, spare // max(1, nl + len(items)))
    render_items(c, y, items, fs, gap=gap, lg=lg)


def text_card(n, title, sub, items, fs=None):
    c, d, y = base(n, T, title, sub); auto(c, y, items); return c


def pair(n, title, sub, a, b, ta, tb, items, h=None):
    """两张照片 + 文字：比较“左右并排”和“上下排列”，取图片面积最大且字号 ≥30 能放下的方案"""
    best = None
    for fs in (36, 35, 34, 33, 32, 31, 30):
        c, d, y = base(n, T, title, sub)
        th = render_items(c, 0, items, fs, dry=True); avail = H - 110 - y - 28 - th
        # 左右并排：宽度受限
        hs = min(avail, round(940 / (a.width / a.height + b.width / b.height)))
        area_s = hs * hs * (a.width / a.height + b.width / b.height)
        # 上下排列：每张高 (avail-16)/2，宽 ≤960
        hv = (avail - 16) // 2; hv = min(hv, round(960 * a.height / a.width), round(960 * b.height / b.width))
        area_v = hv * hv * (a.width / a.height + b.width / b.height)
        for mode, hh, area in (('s', hs, area_s), ('v', hv, area_v)):
            if hh > 200 and (best is None or area > best[0] * 1.15 or (area >= best[0] * .87 and fs > best[2])):
                best = (area, mode, fs, hh)
    area, mode, fs, hh = best
    c, d, y = base(n, T, title, sub)
    if mode == 's':
        y = two(c, y, a, b, ta, tb, hh)
    else:
        for im, t, col in ((a, ta, CORAL), (b, tb, TEAL)):
            w = round(im.width * hh / im.height); x0 = 60 + (960 - w) // 2
            photo(c, im, (x0, y, x0 + w, y + hh), r=18, tag=t, tagc=col); y += hh + 16
        y -= 16
    for fs in range(42, fs - 1, -1):  # 图片放好后，字号取能放下的最大值
        if y + 28 + render_items(c, 0, items, fs, dry=True) < H - 110: break
    render_items(c, y + 28, items, fs); return c

def split(x, cut):
    im = zh(x); return im.crop((0, 22, cut - 3, im.height)), im.crop((cut + 3, 22, im.width, im.height))  # 去掉 a/b 字母行


def chart(fig_fn, w=960):
    fig = fig_fn(); buf = BytesIO(); fig.savefig(buf, format='png', dpi=100); plt.close(fig)
    return Image.open(buf).convert('RGB')


def cover():
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 640], fill=NAVY); d.ellipse([720, -180, 1260, 360], fill=(34, 70, 106))
    t = '康复人必收藏'; tw = d.textlength(t, font=F('B', 34))
    d.rounded_rectangle([60, 64, 108 + tw, 120], 28, fill=CORAL); d.text((84, 68), t, font=F('B', 34), fill=WHITE)
    d.text((136 + tw, 74), '梅奥诊所 2026 技术要点', font=F('M', 30), fill=(190, 205, 222))
    d.text((56, 150), '肩胛骨', font=F('K', 136), fill=WHITE)
    d.text((56, 310), '到底怎么查？', font=F('K', 120), fill=YEL)
    d.text((60, 500), '一套标准流程 · 9 个关键检查 · 分清麻痹和失衡', font=F('B', 36), fill=WHITE)
    photo(c, zh(3), (60, 680, 520, 1260), r=30, tag='肩屈曲抗阻试验', tagc=CORAL)
    photo(c, zh(2), (560, 680, 1020, 960), r=30, fy=.3, tag='肩胛辅助试验', tagc=TEAL)
    photo(c, zh(1), (560, 980, 1020, 1260), r=30, fx=.5, tag='中斜方肌力量', tagc=NAVY)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([140, 1300, 940, 1384], 42, fill=YEL)
    s = '附：肩胛运动肌肉表 + 判读速查'; d.text((540 - d.textlength(s, font=F('K', 40)) / 2, 1316), s, font=F('K', 40), fill=NAVY)
    return c


def muscles():
    c, d, y = base(3, T, '谁在动肩胛骨？', '原文表 1：各方向的主要肌肉')
    M = [('后缩（靠近中线）', '中斜方肌、菱形肌', CORAL, LCOR), ('前伸', '前锯肌、胸小肌', TEAL, LTEAL),
         ('上提', '肩胛提肌、大 / 小菱形肌、上斜方肌', (200, 120, 0), LYEL), ('下降', '下斜方肌、胸小肌、背阔肌', NAVY, LNAVY),
         ('手臂上举时', '前锯肌、上斜方肌和下斜方肌', CORAL, LCOR), ('手臂放下时', '菱形肌、肩胛提肌、胸小肌', TEAL, LTEAL)]
    for i, (a, b, col, fill) in enumerate(M):
        r_, k = divmod(i, 2); x0 = 60 + k * 490; y0 = y + r_ * 250
        panelbox(c, (x0, y0, x0 + 470, y0 + 230), r=26, fill=fill, sh=False); d = ImageDraw.Draw(c)
        d.rounded_rectangle([x0 + 24, y0 + 24, x0 + 24 + d.textlength(a, font=F('K', 34)) + 36, y0 + 84], 30, fill=col)
        d.text((x0 + 42, y0 + 30), a, font=F('K', 34), fill=WHITE)
        rich(d, x0 + 30, y0 + 110, b, 420, 34, wt='M', lh=1.4)
    y += 3 * 250 + 10
    auto(c, y, [('box', '怎么用这张表', '看到哪个方向的动作异常，就去查对应的肌肉；同一块肌肉（如**胸小肌**）可能出现在多个方向里', LYEL, NAVY)], top=36)
    return c


def lookup_card():
    c, d, y = base(12, T, '判读速查：看到什么，想到什么', '把检查结果串起来')
    R = [('肩胛离中线更远、内缘翘起，抗阻外旋时更明显（翻转征）', '斜方肌麻痹', CORAL, LCOR),
         ('出拳、靠墙俯卧撑时肩胛内缘离开胸壁', '前锯肌无力', TEAL, LTEAL),
         ('屈曲抗阻：30°、60° 下角翘起，100° 消失', '前锯肌活动不足，可伴胸小肌过度活动或挛缩', (200, 120, 0), LYEL),
         ('屈曲抗阻：各个角度都翘起', '前锯肌麻痹', NAVY, LNAVY),
         ('辅助肩胛后疼痛减轻、活动度改善', '肩胛运动异常是肩痛的“帮凶”', (90, 70, 170), (240, 240, 248)),
         ('静息位肩胛前伸，喙突到第 4 肋胸骨端距离缩短', '胸小肌短缩，或锁骨短缩', GREY, (236, 236, 236))]
    for a, b, col, fill in R:
        ha = textheight(a, 880, 32, 'R', 1.4); hh = 36 + ha + 56 + 26
        panelbox(c, (60, y, 1020, y + hh), r=22, fill=fill, sh=False); d = ImageDraw.Draw(c)
        d.rectangle([60, y + 16, 70, y + hh - 16], fill=col)
        rich(d, 92, y + 20, a, 880, 32, lh=1.4)
        rich(d, 92, y + 28 + ha, '→ **' + b + '**', 880, 34, em=col, lh=1.4)
        y += hh + 18
    return c


T = 13
cards = [cover(),
    text_card(2, '为什么要单独查肩胛骨', '肩胛是盂肱关节的“地基”', [
        ('bul', ['肩胛为盂肱关节运动提供**稳定的基座**，并在肩复合体中传递力量',
                 '肩胛运动障碍常与**肩袖撕裂、肩峰下撞击、肩关节不稳**相伴',
                 '它**本身不是诊断**，而是背后病理（多为神经肌肉问题）的表现，要放到整个动力链里看'], CORAL),
        ('h', '查之前', NAVY),
        ('steps', [('1', '**裸露上身**，从多个角度看，**最重要的是从背后看**'), ('2', '先做常规肩关节检查，了解整体功能'), ('3', '查**颈椎**，排除颈源性问题')])]),
    muscles(),
    text_card(4, '锁骨与胸小肌', '肩胛的“前方拉索”', [
        ('h', '锁骨、肩锁关节、胸锁关节', NAVY),
        ('bul', ['肩胛在胸壁上滑动，要靠肩锁关节、胸锁关节连接；两者**不稳**都会影响肩胛功能',
                 '触诊 + 应力试验：**交臂内收试验**、**O’Brien 试验**、**手臂牵拉试验**',
                 '**锁骨短缩**（与对侧比较）可使肩胛内旋、前倾，静息时表现为**过度前伸**'], TEAL),
        ('h', '胸小肌', NAVY),
        ('bul', ['胸小肌短缩可**模仿撞击时的肩胛运动**，可能参与肩峰下病变',
                 '测量：**喙突尖到第 4 肋与胸骨连接处**的距离，与对侧比较'], CORAL)]),
    text_card(5, '静息位置与肩胛节律', '从背后看', [
        ('steps', [('1', '先看**静息位置**：双侧是否等高、是否前伸'), ('2', '反复做**主动前屈和外展**，看肩胛节律'),
                   ('3', '留意**下角或内缘突出**，或明显的肩胛胸壁异常运动'), ('4', '测量**脊柱中线到肩胛内缘**的距离')]),
        ('box', '斜方肌麻痹', '患侧肩胛内缘**离中线更远**，两侧对比很有价值', LCOR, CORAL)]),
    figcard(6, T, '斜方肌力量', '图 1：双手叉腰，抗阻后缩，单独测中斜方肌', zh(1), [
        ('steps', [('上', '**上斜方肌**：抗阻**耸肩**'), ('中', '**中斜方肌 + 菱形肌**：抗阻**肩胛后缩**'),
                   ('!', '想把斜方肌和菱形肌**分开**：手臂轻度外展、**双手叉腰**，再抗阻后缩'),
                   ('中', '也可**俯卧、肩前屈约 90°** 做抗阻后缩'), ('下', '**下斜方肌**：肩前屈约 **120°** 做抗阻后缩')])]),
    text_card(7, '翻转征和“拳击出拳”', '一查斜方肌，一查前锯肌', [
        ('h', '肩胛翻转征（斜方肌）', NAVY),
        ('steps', [('1', '让患者做**抗阻外旋**'), ('!', '斜方肌麻痹时，肩胛**内缘明显翘起**＝翻转征阳性')]),
        ('h', '“拳击出拳”（前锯肌）', NAVY),
        ('steps', [('1', '肩前屈 **90°**、肘几乎伸直'), ('2', '让患者**向前推**，检查者给阻力'),
                   ('!', '前锯肌无力：推不动，并且肩胛**内缘离开胸壁**')])]),
    figcard(8, T, '肩胛辅助试验', '图 2：检查左肩', zh(2), [
        ('steps', [('1', '检查者站在后方，患者**主动上举**手臂（橙色箭头）'), ('2', '检查者用手给肩胛**上回旋 + 后倾**的力（灰色箭头）')]),
        ('box', '阳性', '辅助后**疼痛减轻或活动度改善** → 肩胛运动异常在“拖累”肩。适用于前锯肌麻痹、前锯肌活动不足、早期**面肩肱型肌营养不良**', LTEAL, TEAL)]),
    text_card(9, '靠墙俯卧撑', '查前锯肌耐力', [
        ('steps', [('1', '面对墙站立，双手撑墙'), ('2', '**慢慢地、反复**做俯卧撑'), ('!', '肩胛**内缘离开胸壁** → 提示前锯肌无力')]),
        ('box', '但它不是最好的', '对前锯肌功能障碍，**肩屈曲抗阻试验**的诊断准确性更好，优于传统的靠墙俯卧撑（下一张）', LYEL, NAVY)]),
    figcard(10, T, '肩屈曲抗阻试验', '图 3：A 抗阻屈曲约 100°，B 从背后观察肩胛', zh(3), [
        ('steps', [('1', '检查者在患侧后方，患者分别在 **30°、60°、100°** 做抗阻前屈'), ('2', '观察肩胛**下角**是否翘起')]),
        ('box', '怎么判读', '30°、60° 翘起、**100° 消失** → 前锯肌**活动不足**（可伴胸小肌过度活动或挛缩）\n**各角度都翘起** → 前锯肌**麻痹**', LCOR, CORAL),
        ('bul', ['原理：胸小肌和前锯肌上部起点相近，低角度时都参与；**100°** 时胸小肌影响最小，能更单独地评估前锯肌'], TEAL)]),
    text_card(11, '弹响肩胛与动力链', '最后两件事', [
        ('h', '弹响肩胛', NAVY),
        ('steps', [('1', '检查者把手放在患者描述的部位'), ('2', '让患者**重复诱发弹响的动作**'), ('3', '用手去**摸**、用耳朵去**听**')]),
        ('h', '别只盯着肩胛', NAVY),
        ('bul', ['肩胛把**躯干和下肢**的力量传到手臂，问题可能来自**远处**', '三维肩胛运动分析目前难以用于临床，**体格检查仍是最可行的工具**',
                 '康复重在恢复**神经肌肉控制**，而不只是单块肌肉的力量'], CORAL)]),
    lookup_card(),
    text_card(13, '收藏：肩胛查体顺序', '从静到动，从力量到功能', [
        ('steps', [('1', '常规肩关节 + 颈椎检查'), ('2', '锁骨、肩锁、胸锁关节；胸小肌长度'), ('3', '静息位置、肩胛节律、中线距离'),
                   ('4', '斜方肌上、中、下部力量；翻转征'), ('5', '前锯肌：出拳、靠墙俯卧撑、**屈曲抗阻试验**'), ('6', '肩胛辅助试验；弹响')]),
        ('box', '文献', 'Selman F, Perry NPJ, Restrepo DJ, Coleman D, Sanchez-Sotelo J. Refining Shoulder Diagnostics: A Technical Note on Scapular Physical Examination. Arthrosc Tech. 2026;15:e70203. doi:10.1002/atn2.70203', LNAVY, NAVY),
        ('box', '版权', '原文以 **CC BY 4.0** 开放获取。图片引自原文，英文标注由编者改为中文；仅供学习交流，如有侵权请联系删除', LTEAL, TEAL)])]
import os
os.makedirs(OUT, exist_ok=True)
for i, im in enumerate(cards, 1):
    im.save(f'{OUT}/card{i:02d}.jpg', quality=92)
print('ok', len(cards))
