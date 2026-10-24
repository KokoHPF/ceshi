#!/usr/bin/env python3
"""《膝关节临床检查：掌握膝关节损伤的诊断工具》（Rossi 等 2011，SMARTT）小红书 3:4 图文卡片，1080×1440。
原文图 1～15 为无英文标注的临床照片，直接使用；左右拼图按分界列切开后上下或并排排版。
用法：python3 xhs/make_cards.py <思源黑体目录> <输出目录>"""
import sys, re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

FD, OUT = sys.argv[1:3]; SERIES = '膝关节查体'
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
    return Image.open(f'src/x{x}.jpg').convert('RGB')


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
    s = 'Rossi 等 SMARTT 2011;3:25'; d.text((W - 60 - d.textlength(s, font=F('R', 22)), H - 60), s, font=F('R', 22), fill=GREY)
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


def gr(i):
    return Image.open(f'src/x_gr{i}.jpg').convert('RGB')


def strip(c, y, ims, tags, h, cols=(CORAL, TEAL, NAVY)):
    """一排等高照片，总宽 960"""
    ws = [im.width * h / im.height for im in ims]; s = min(1, (960 - 16 * (len(ims) - 1)) / sum(ws)); h = round(h * s)
    ws = [round(w * s) for w in ws]; x = 60 + (960 - sum(ws) - 16 * (len(ims) - 1)) // 2
    for im, t, w, col in zip(ims, tags, ws, cols):
        photo(c, im, (x, y, x + w, y + h), r=18, tag=t, tagc=col); x += w + 16
    return y + h


def fill(c, y, items, top=44):
    auto(c, y, items, top=top); return c


FIG = {1: 13, 2: 27, 3: 36, 4: 38, 5: 51, 6: 53, 7: 65, 8: 67, 9: 79, 10: 81, 11: 83, 12: 94, 13: 96, 14: 106, 15: 108}
CUT = {1: 516, 3: 731, 4: 772, 5: 878, 6: 842, 13: 850, 14: 933}


def fg(n, part=None):
    im = zh(FIG[n])
    if part is None: return im
    c = CUT[n]; return im.crop((0, 0, c - 2, im.height)) if part == 0 else im.crop((c + 3, 0, im.width, im.height))


def card(n, title, sub, ims, tags, items, h=620, stack=False):
    """ims 一排（或上下）放图，再自动排文字"""
    c, d, y = base(n, TOT, title, sub)
    if stack:
        for im, t, col in zip(ims, tags, (CORAL, TEAL)):
            hh = h; w = round(im.width * hh / im.height)
            if w > 960: w = 960; hh = round(im.height * w / im.width)
            photo(c, im, (60 + (960 - w) // 2, y, 60 + (960 - w) // 2 + w, y + hh), r=18, tag=t, tagc=col); y += hh + 16
        y -= 16
    else:
        y = strip(c, y, ims, tags, h)
    return fill(c, y + 28, items, top=40)


def cover():
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 680], fill=NAVY); d.ellipse([720, -180, 1260, 360], fill=(34, 70, 106))
    t = '康复人必收藏'; tw = d.textlength(t, font=F('B', 34))
    d.rounded_rectangle([60, 64, 108 + tw, 120], 28, fill=CORAL); d.text((84, 68), t, font=F('B', 34), fill=WHITE)
    d.text((136 + tw, 74), 'SMARTT 2011 综述', font=F('M', 30), fill=(190, 205, 222))
    d.text((56, 150), '膝关节临床检查：', font=F('K', 104), fill=WHITE)
    d.text((56, 290), '掌握膝关节损伤的', font=F('K', 104), fill=YEL)
    d.text((56, 420), '诊断工具', font=F('K', 104), fill=YEL)
    d.text((60, 580), '髌股关节 · 半月板与软骨 · 韧带不稳，30+ 个检查', font=F('B', 34), fill=WHITE)
    photo(c, fg(9), (60, 720, 520, 1270), r=30, tag='Lachman 试验', tagc=CORAL)
    photo(c, fg(3, 0), (560, 720, 1020, 990), r=30, tag='McMurray 试验', tagc=TEAL)
    photo(c, fg(14, 1), (560, 1010, 1020, 1270), r=30, tag='Dial 试验', tagc=NAVY)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([140, 1300, 940, 1384], 42, fill=YEL)
    s = '15 张查体图 + 损伤模式速查表'; d.text((540 - d.textlength(s, font=F('K', 40)) / 2, 1316), s, font=F('K', 40), fill=NAVY)
    return c


def table_card():
    c, d, y = base(17, TOT, '损伤模式速查', '原文表 1：按敏感性排序的阳性试验')
    R = [('前内侧不稳', '前交叉 + 内侧副韧带 + 内侧半月板', '外翻应力、前抽屉、Lachman', CORAL, LCOR),
         ('前外侧不稳', '前交叉 + 外侧关节囊 + 外侧半月板', '外翻应力、前抽屉、Lachman、轴移', TEAL, LTEAL),
         ('后外侧不稳', '后外侧角', '外旋、Dial、反屈、后外侧抽屉', (200, 120, 0), LYEL),
         ('后内侧不稳', '内侧副韧带 + 前交叉 + 后内侧角', '外翻应力、后抽屉、Lachman', NAVY, LNAVY),
         ('前内 + 前外侧不稳', '前交叉 + 内侧副韧带 + 外侧关节囊（后交叉完好）', '前抽屉、Lachman、轴移、外翻应力', (90, 70, 170), (240, 240, 248)),
         ('后内 + 后外侧不稳', '前交叉 + 内侧副韧带 + 后外侧角（后交叉完好）*', '前抽屉、Lachman、轴移、外翻、内翻应力', GREY, (236, 236, 236))]
    for a, b, e, col, fill in R:
        hb = textheight(b, 880, 28, 'R', 1.35); he = textheight('→ ' + e, 880, 30, 'B', 1.35); hh = 58 + hb + he + 20
        panelbox(c, (60, y, 1020, y + hh), r=22, fill=fill, sh=False); d = ImageDraw.Draw(c)
        d.rectangle([60, y + 16, 70, y + hh - 16], fill=col)
        d.text((92, y + 12), a, font=F('K', 34), fill=col)
        yy = rich(d, 92, y + 60, b, 880, 28, col=GREY, lh=1.35)
        rich(d, 92, yy + 4, '→ **' + e + '**', 880, 30, em=INK, lh=1.35); y += hh + 10
    rich(d, 60, y + 2, '*原文如此，与名称不符，宜以后抽屉、Dial 等为准', 960, 24, col=GREY, lh=1.3)
    return c


TOT = T = 18
cards = [cover(),
    text_card(2, '先问诊，再查体', '影像不能代替查体', [
        ('h', '问诊三件事', NAVY),
        ('steps', [('1', '**定位**：伸膝装置？关节内（内侧 / 外侧 / 髌股）？韧带（内侧 / 外侧 / 中轴）？'), ('2', '**时间**：急性、陈旧伤、慢性病还是过用？'), ('3', '**症状**：疼痛、不适还是功能障碍？')]),
        ('bul', ['**绞锁**多见于半月板桶柄状撕裂；后关节囊和内侧副韧带出血导致的腘绳肌痉挛可**模仿绞锁**',
                 '韧带断裂常有“**啪**”一声，让患者尽量**复现受伤时的扭转动作**', '“打软腿”不特异：游离体、髌骨软化、不稳、股四头肌无力都可以'], CORAL),
        ('box', '查体分三组', '① 髌股关节 / 伸膝装置　② 关节内（半月板、软骨）　③ 膝关节不稳', LTEAL, TEAL)]),
    card(3, '髌骨滑移试验', '髌股关节 ①：原文图 1', [fg(1, 0), fg(1, 1)], ['', ''], [
        ('bul', ['**Q 角**：髂前上棘—髌骨中心与胫骨结节—髌骨中心两线夹角，建议**屈膝 30°** 测，正常 **10°～20°**；临床价值有争议，**不能单独**用于诊断',
                 '**髌骨倾斜**：伸膝位，髌骨外缘**掀不过水平** → 外侧支持带紧张',
                 '**滑移**：屈膝 30°，向外推 **>75%** 髌骨宽 → 内侧松弛；**<25%** → 外侧紧张'], CORAL)], h=520),
    card(4, 'MPFL 触诊与髌骨轨迹', '髌股关节 ②：原文图 2', [fg(2)], [''], [
        ('bul', ['伸膝位，拇指像滑移试验一样把髌骨**向内推**，拉紧内侧髌股韧带（MPFL）；**压痛点**通常就是撕裂位置；向外滑移 >75% 提示 MPFL 功能不全',
                 '**轨迹**：从伸到屈应平滑；屈膝 20°～30° 时髌骨进入滑车',
                 '**J 征**：伸膝末端髌骨从外侧半脱位**突然向内滑入滑车**，走出“J”形'], TEAL)], h=560),
    card(5, 'McMurray 试验', '半月板 ①：原文图 3', [fg(3, 0), fg(3, 1)], ['', ''], [
        ('steps', [('1', '屈膝，小腿**外旋**，一指按住关节线'), ('2', '慢慢**伸膝**；查外侧半月板时小腿**内旋**'), ('!', '股骨髁卡进撕裂处时出现**疼痛或弹响**')]),
        ('box', '为什么这样做', '所有半月板 / 软骨试验都是**屈膝 + 胫骨旋转 + 关节线应力**：此时后髁后滚、关节间隙变窄，半月板被夹紧', LTEAL, TEAL)], h=520),
    card(6, '“4 字”半月板应力手法', '半月板 ②：原文图 4', [fg(4, 0), fg(4, 1)], ['', ''], [
        ('steps', [('1', '下肢摆成“**4 字**”（Cabot）体位'), ('2', '膝关节从**内翻快速摆到外翻**，同时一指压进关节线'), ('!', '半月板被推向外周、手指把它推向中心 → 撕裂时**锐痛**')]),
        ('bul', ['**Bragard**：外旋 + 伸膝时关节线压痛 → 软骨或半月板病变', '**Steinmann 第二**：压痛点随屈膝**后移**、伸膝**前移**'], CORAL)], h=440),
    card(7, 'Apley 研磨试验', '半月板 ③：原文图 5', [fg(5, 0), fg(5, 1)], ['', ''], [
        ('steps', [('1', '**俯卧**，屈膝 90°'), ('2', '旋转小腿，先**牵拉**再**加压**'), ('!', '只在**加压**时痛 → 半月板；牵拉和加压**没区别** → 更像软骨病变')]),
        ('bul', ['**Bohler**：内、外翻应力挤压撕裂处痛', '**深蹲、鸭步、Thessaly**：负重下反复屈膝', '**Merke**：负重转身，内旋身体时内侧关节线痛 → 内侧半月板',
                 '**Payr**：盘腿坐诱发内侧痛　**Steinmann 第一**：屈膝 90° 外旋痛 → 内侧，内旋痛 → 外侧'], CORAL)], h=380),
    card(8, '外翻 / 内翻应力试验', '不稳 ①：原文图 6', [fg(6, 0), fg(6, 1)], ['', ''], [
        ('bul', ['在**屈膝 30°** 做（不是完全伸直）：放松肌腱和后关节囊，才能**单独**检查内、外侧副韧带', '一指放在关节线上感觉**张开程度**'], TEAL),
        ('box', '分级（美国医学会）', 'Ⅰ 度 0～5 mm，终点硬；Ⅱ 度 5～10 mm，终点硬；Ⅲ 度 >10 mm，**终点软**', LYEL, NAVY),
        ('box', '注意', '看**张开程度**，不看疼痛：部分断裂常更痛，完全断裂反而只轻痛', LCOR, CORAL)], h=380),
    card(9, 'Cabot 手法', '不稳 ②：原文图 7，查外侧副韧带', [fg(7)], [''], [
        ('steps', [('1', '下肢摆成“**4 字**”体位，给膝关节**内翻**应力'), ('2', '外侧副韧带完好时，可在**腓骨头与股骨外上髁之间**摸到一根绷紧的“**弦**”')]),
        ('box', '注意', '这个姿势下还能顺便做“4 字”半月板应力手法；两者都可能**剧痛**，急性期难做', LCOR, CORAL)], h=600),
    card(10, '前抽屉试验', '不稳 ③：原文图 8', [fg(8)], [''], [
        ('bul', ['在**中立、内旋 30°、外旋 30°** 三个位置做；内旋会拉紧后交叉和后外侧角，前抽屉可能转阴',
                 '先找“**零点**”：中立位胫骨平台比股骨内髁**前移约 0.5～1 cm**', '后交叉断裂时胫骨起点**偏后**，复位到中立会被误当成前抽屉阳性',
                 '急性肿胀膝可在**屈膝 60°～80°** 做；外侧半月板像“**门挡**”卡住，可造成**假阴性**'], TEAL)], h=560),
    card(11, 'Lachman 试验', '不稳 ④：原文图 9', [fg(9)], [''], [
        ('steps', [('1', '完全伸膝和**屈膝 30°**、轻度外旋'), ('2', '前拉胫骨，看**前移量**和**终点**')]),
        ('box', '最关键是终点', '**软终点**高度提示前交叉断裂；**硬终点**即使前移较多也可能完好。受伤头几天肿痛明显时，它是**最容易做**的前交叉检查', LCOR, CORAL),
        ('bul', ['KT-1000 定量适合**随访**，不适合诊断', '后 Lachman 查后交叉，效果不如前 Lachman'], TEAL)], h=560),
    card(12, '后交叉：后沉征与股四头肌试验', '不稳 ⑤：原文图 10、图 11', [fg(10), fg(11)], ['胫骨后退', '股四头肌主动'], [
        ('bul', ['仰卧屈髋 90°、屈膝 90°：后交叉断裂时胫骨**向后“沉”**（被动后沉征）',
                 '**股四头肌主动试验**：保持屈膝，让患者收缩股四头肌 → 胫骨被拉回、后沉**消失**',
                 '也可在 Lachman 体位抗阻抬腿，或叩髌腱反射诱发收缩'], TEAL)], h=480),
    card(13, '轴移试验', '不稳 ⑥：原文图 12', [fg(12)], [''], [
        ('steps', [('1', '早期屈膝时加**外翻 + 内旋**：胫骨外侧平台**向前半脱位**'), ('2', '屈到约 **30°**，髂胫束越过旋转中心，把胫骨**突然推回** → “跳”一下')]),
        ('bul', ['查前交叉缺失的**旋转不稳**，**最有效**，但痛、常只能做一次', '单纯前交叉断裂“跳”得轻；明显可见、可闻的大“跳”提示**合并后外侧角**损伤',
                 '要么在**伤后极早期**做，要么等**慢性期**；肿起来后越来越难做', '**Noyes 滑移轴移**：轴向加压 + 上抬胫骨，出现“滑”而非“咔”；**Hughston**：从屈到伸'], CORAL)], h=400),
    card(14, 'Slocum 前外侧旋转不稳试验', '不稳 ⑦：原文图 13', [fg(13, 0), fg(13, 1)], ['', ''], [
        ('steps', [('1', '健侧在下**半侧卧**，患膝伸直、只用足跟搭在床上 → 小腿自然内旋'), ('2', '给**外翻**应力，逐渐屈膝'), ('!', '前 20° 半脱位，约 **40°** 突然复位（“咔”一下）')]),
        ('box', '优点', '骨盆侧卧稍后倾，消除髋旋转的干扰；据报道**比其他轴移试验更有效、更不痛**', LTEAL, TEAL),
        ('bul', ['**反轴移征**：后交叉缺失时外旋 + 外翻下胫骨外侧平台**向后**半脱位，伸膝时复位'], CORAL)], h=380, stack=False),
    card(15, 'Dial 试验（胫骨外旋）', '后外侧角 ①：原文图 14', [fg(14, 0), fg(14, 1)], ['', ''], [
        ('steps', [('1', '仰卧更舒服，**俯卧**能用体重固定髋、消除髋旋转'), ('2', '在**屈膝 30° 和 90°** 比较两侧胫骨外旋'), ('!', '患侧比健侧多外旋 **≥10°** 为阳性')]),
        ('bul', ['完全伸直时腓肠肌外侧头绷紧，会**减少**外旋', '屈膝位胫骨还会**向后半脱位**；用手指把胫骨复位到股骨外髁上，外旋会更大',
                 '后外侧角损伤常**合并**前交叉或后交叉损伤，容易漏诊'], TEAL)], h=440),
    card(16, '外旋反屈试验与后外侧抽屉', '后外侧角 ②：原文图 15', [fg(15)], [''], [
        ('bul', ['**外旋反屈**：从屈膝 10° 伸到最大，同时外旋；外旋增大 + **膝反屈** → 后外侧角和后关节囊损伤；也可**提起脚趾**抬起伸直的下肢看',
                 '反屈很明显时提示**合并后交叉断裂**'], TEAL),
        ('box', '后外侧外旋抽屉', '屈膝 30° 和 90° 向后 + 外旋推胫骨：**只在 30°** 半脱位 → 单纯后外侧角；**90° 也**半脱位 → 后交叉 + 后外侧角', LYEL, NAVY)], h=640),
    table_card(),
    text_card(18, '收藏：膝关节查体三组工具', '对号入座，按需选用', [
        ('steps', [('1', '**髌股关节**：Q 角、倾斜、滑移、MPFL 触诊、轨迹、J 征'), ('2', '**半月板 / 软骨**：McMurray、4 字应力、Apley、Thessaly、Steinmann 等'),
                   ('3', '**不稳**：内外翻应力、Cabot、前后抽屉、Lachman、后沉征、轴移、Slocum、Dial、外旋反屈')]),
        ('box', '文献', 'Rossi R, Dettoni F, Bruzzone M, Cottino U, D’Elicio DG, Bonasia DE. Clinical examination of the knee: know your tools for diagnosis of knee injuries. Sports Med Arthrosc Rehabil Ther Technol. 2011;3:25. doi:10.1186/1758-2555-3-25', LNAVY, NAVY),
        ('box', '版权', '原文以 **CC BY 2.0** 开放获取；原文图片注明改编自 Springer 出版的《Orthopedic Sports Medicine》。仅供学习交流，如有侵权请联系删除', LTEAL, TEAL)])]
import os
os.makedirs(OUT, exist_ok=True)
for i, im in enumerate(cards, 1):
    im.save(f'{OUT}/card{i:02d}.jpg', quality=92)
print('ok', len(cards))
