#!/usr/bin/env python3
"""后肩不稳的“拇指试验”（Boileau 等 2022，Arthroscopy Techniques）小红书 3:4 图文卡片，1080×1440。
示意图（原文图 2、图 3A～C）由 tools/annotate.py 加中文结构标注；临床照片为原文图 1、图 4 和原文视频 1 的截帧。
用法：python3 xhs/make_cards.py <思源黑体目录> <输出目录>"""
import sys, re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

FD, OUT = sys.argv[1:3]; SERIES = '后肩不稳'
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
    return Image.open(f'src/zh/{x}.jpg').convert('RGB')


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
    s = 'Boileau 等 Arthrosc Tech 2022;11(9):e1613'; d.text((W - 60 - d.textlength(s, font=F('R', 22)), H - 60), s, font=F('R', 22), fill=GREY)
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


def cover():
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 640], fill=NAVY); d.ellipse([720, -180, 1260, 360], fill=(34, 70, 106))
    t = '康复人必收藏'; tw = d.textlength(t, font=F('B', 34))
    d.rounded_rectangle([60, 64, 108 + tw, 120], 28, fill=CORAL); d.text((84, 68), t, font=F('B', 34), fill=WHITE)
    d.text((136 + tw, 74), 'Boileau 团队 · 2022', font=F('M', 30), fill=(190, 205, 222))
    d.text((56, 150), '一根拇指', font=F('K', 136), fill=WHITE)
    d.text((56, 310), '查后肩不稳', font=F('K', 128), fill=YEL)
    d.text((60, 500), '拇指试验：顶住后方关节线，抬手不痛了 → 阳性', font=F('B', 36), fill=WHITE)
    photo(c, zh('v59'), (60, 680, 400, 1260), r=30, tag='拇指顶住', tagc=CORAL)
    photo(c, zh('fig3A'), (420, 680, 1020, 1260), r=30, fy=.55, tag='拇指＝“后方骨块”', tagc=TEAL)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([140, 1300, 940, 1384], 42, fill=YEL)
    s = '示意图逐张精讲 + 视频截帧'; d.text((540 - d.textlength(s, font=F('K', 42)) / 2, 1314), s, font=F('K', 42), fill=NAVY)
    return c


def why():
    c, d, y = base(2, T, '后肩不稳，为什么容易漏？', '年轻运动人群越来越常见')
    def fn():
        fig, ax = plt.subplots(figsize=(9.6, 3.6))
        ax.barh([1], [10], left=[2], color='#9bc9d1', height=.5); ax.barh([0], [20], color='#be2832', height=.5)
        ax.text(12.5, 1, '过去：2%～10%', va='center', fontsize=26); ax.text(20.5, 0, '现在：最高约 20%', va='center', fontsize=26)
        ax.set_xlim(0, 52); ax.set_yticks([]); ax.set_xlabel('占肩关节不稳的比例（%）', fontsize=20); ax.tick_params(labelsize=18)
        ax.spines[['top', 'right', 'left']].set_visible(False); fig.tight_layout(); return fig
    im = chart(fn); h = round(im.height * 960 / im.width); put(c, im, 60, y, 960, h); y += h + 26
    return fill(c, y, [('h', '难在哪', NAVY),
        ('steps', [('1', '患者多以**疼痛**就诊，**没有脱位或半脱位史**'), ('2', '后盂唇撕裂在磁共振 / 磁共振造影上**常看不清**，准确性低于前下盂唇'),
                   ('3', '常诉**肩前痛**、二头肌沟压痛，容易被带偏'), ('4', '常用查体（Jerk、Kim、推拉、Porcellini、后方负荷—移位）效果不一，患者疼痛**保护**时难做')]),
        ('box', '影像线索', '关节盂**后倾增大**、关节盂发育不良、后方关节囊面积增大、后肩峰较高且后倾角减小', LTEAL, TEAL)], top=40)


T = 11
cards = [cover(), why()]
# 3 图 2 精讲
c, d, y = base(3, T, '示意图①：为什么抬手会痛', '原文图 2：横断面（上为前，下为后）')
h = round(zh('fig2').height * 960 / zh('fig2').width); put(c, zh('fig2'), 60, y, 960, h); y += h + 26
cards.append(fill(c, y, [('steps', [('1', '手臂在**中立内收位前屈上举**时，肱骨头被推向**后方**（红色箭头）'),
                                   ('2', '半脱位的肱骨头压在**撕裂的后盂唇**上 → 疼痛、不稳甚至半脱位')]),
                        ('box', '一句话', '这个动作本身就是**诱发试验**；拇指试验要做的，就是把肱骨头“挡回去”', LYEL, NAVY)]))
# 4 第一步：诱发
c, d, y = base(4, T, '第一步：先诱发症状', '原文图 1 + 视频截帧')
y = strip(c, y, [gr(1), zh('v22'), zh('v25')], ['图 1', '视频：前屈', '视频：上举'], 640) + 28
cards.append(fill(c, y, [('steps', [('1', '坐位或站立，检查者站在**患侧后方**'), ('2', '让患者在**中立内收位**主动前屈，把患侧手臂举过头'),
                                   ('3', '记录有没有**后肩痛**和**不稳感**，或明显半脱位')])]))
# 5 图 3A 精讲
c, d, y = base(5, T, '示意图②：拇指放哪里', '原文图 3A：右肩横断面')
h = 640; w = round(zh('fig3A').width * h / zh('fig3A').height); put(c, zh('fig3A'), 60 + (960 - w) // 2, y, w, h); y += h + 26
cards.append(fill(c, y, [('steps', [('1', '拇指直接压在**后方盂肱关节线**上'), ('!', '**一半压在后方关节盂缘，一半压在肱骨头后内侧**')]),
                        ('box', '原理', '拇指起到功能性的“**后方骨块**”作用——就像后方骨块手术一样，把肱骨头挡住、恢复稳定', LTEAL, TEAL)]))
# 6 图 3B、3C 精讲
c, d, y = base(6, T, '示意图③：另一只手指干什么', '原文图 3B 横断面、3C 矢状面')
y = strip(c, y, [zh('fig3B'), zh('fig3C')], ['', ''], 760) + 28
cards.append(fill(c, y, [('bul', ['同侧手的**其余手指勾住前方锁骨**，作为反作用力', '这样拇指才能**用力顶住**后方关节线',
                                 '患者很壮、肌肉发达时，可以用**双手、两个拇指**一起顶'], TEAL)]))
# 7 第三步：拇指在位再做一次
c, d, y = base(7, T, '第三步：拇指顶住，再抬一次', '原文图 4 + 视频截帧')
y = strip(c, y, [zh('v53'), zh('v59'), gr(4)], ['放好拇指', '再前屈', '图 4'], 640) + 28
cards.append(fill(c, y, [('steps', [('1', '拇指保持顶住，用手指在锁骨上对抗'), ('2', '让患者**重复第一步的动作**：中立内收位前屈上举')]),
                        ('box', '阳性', '拇指在位时**后肩痛缓解、稳定性改善**（活动度可改善也可不改善）', LCOR, CORAL)]))
cards.append(text_card(8, '怎么解读', '阳性意味着什么', [
    ('bul', ['作者门诊中，诊断后盂唇撕裂 / 不稳且**拇指试验阳性**的患者，关节镜下**都发现了需要修补的后盂唇病变**',
             '还能帮助**确认不稳方向**——没有明显盂唇、关节囊撕裂时，方向在临床和影像上不一定清楚'], CORAL),
    ('box', '为什么好做', '这是**主动试验**，由患者自己抬手，**受疼痛保护和恐惧的影响小**，比检查者被动操作的试验更容易做', LTEAL, TEAL)]))
# 9 和其他试验比
c, d, y = base(9, T, '和其他后方不稳试验比', '原文讨论中的数据')
def fn():
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    L = ['Kim 试验', 'Jerk 试验']; se = [80, 73]; sp = [94, 98]; x = np.arange(2); w = .36
    b1 = ax.bar(x - w / 2, se, w, color='#00788c', label='敏感度'); b2 = ax.bar(x + w / 2, sp, w, color='#be2832', label='特异度')
    for bs in (b1, b2):
        for r in bs: ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 1.5, f'{int(r.get_height())}%', ha='center', fontsize=24)
    ax.set_xticks(x); ax.set_xticklabels(L, fontsize=24); ax.set_ylim(0, 128); ax.legend(frameon=False, fontsize=20, ncol=2, loc='upper center')
    ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=14); fig.tight_layout(); return fig
im = chart(fn); h = round(im.height * 960 / im.width); put(c, im, 60, y, 960, h); y += h + 26
cards.append(fill(c, y, [('bul', ['Kim 试验作者建议与 **Jerk 试验联合**使用，以更好地发现后下方不稳', '其他常用：推拉试验、Porcellini 试验、后方负荷—移位试验',
                                 '**没有哪一个试验单独使用**就有很好的敏感度和特异度，常需多个试验联合'], TEAL),
                        ('box', '拇指试验的位置', '**目前没有**敏感度、特异度和信度数据，是对现有试验的**补充**', LYEL, NAVY)], top=40))
cards.append(text_card(10, '要点与局限', '原文表 1', [
    ('steps', [('✓', '主动试验，操作简单，不太受疼痛保护和恐惧影响'),
               ('✓', '拇指**正对关节线**：一半在后方关节盂缘，一半在肱骨头后内侧'),
               ('!', '这只是**技术描述**，尚无敏感度、特异度和检查者间 / 内信度研究'),
               ('!', '“阳性者关节镜都有病变”来自作者自己门诊，**未给出例数**，也没有阴性者的对照')])]))
cards.append(text_card(11, '收藏：拇指试验三步走', '后肩痛 + 无脱位史时想到它', [
    ('steps', [('1', '站在患侧后方，让患者中立内收位**前屈上举** → 记录疼痛 / 不稳'), ('2', '拇指压**后方关节线**，手指勾**前方锁骨**'),
               ('3', '再上举：**疼痛减轻、更稳**＝阳性，提示后方不稳 / 后盂唇撕裂')]),
    ('box', '文献', 'Boileau P, Van Steyn PM, Czarnecki M, Teissier S, Gasbarro G, Galvin JW. The Thumb Test: A Simple Physical Examination Maneuver for the Diagnosis of Symptomatic Posterior Shoulder Instability. Arthrosc Tech. 2022;11(9):e1613-e1616', LNAVY, NAVY),
    ('box', '版权', '原文以 **CC BY-NC-ND 4.0** 开放获取（非商业、禁止演绎）。示意图加了中文标注，照片含原文视频截帧；仅供学习交流，如有侵权请联系删除', LCOR, CORAL)]))
import os
os.makedirs(OUT, exist_ok=True)
for i, im in enumerate(cards, 1):
    im.save(f'{OUT}/card{i:02d}.jpg', quality=92)
print('ok', len(cards))
