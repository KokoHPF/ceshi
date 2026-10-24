#!/usr/bin/env python3
"""肩袖撕裂的体格检查与保守治疗（Itoi 2013，J Orthop Sci）小红书 3:4 图文卡片，1080×1440。
原文图 1～13 为无英文标注的黑白照片，直接使用并配中文标签；文字和数据图为编者根据原文整理。
用法：python3 xhs/make_cards.py <思源黑体目录> <输出目录>"""
import sys, re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

FD, OUT = sys.argv[1:3]; SERIES = '肩袖撕裂'
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
    s = 'Itoi. J Orthop Sci 2013;18(2):197-204'; d.text((W - 60 - d.textlength(s, font=F('R', 22)), H - 60), s, font=F('R', 22), fill=GREY)
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


def render_items(c, y, items, fs, dry=False, X=60, Wd=960):
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
                y = (rich(d, X + w + 16, y, t, Wd - w - 16, fs, lh=1.45) if not dry else y + textheight(t, Wd - w - 16, fs, 'R', 1.45)) + 10
        elif kind == 'bul':
            for t in it[1]:
                if not dry:
                    d.ellipse([X, y + fs * .42, X + 14, y + fs * .42 + 14], fill=it[2] if len(it) > 2 else CORAL)
                    y = rich(d, X + 32, y, t, Wd - 32, fs, lh=1.45) + 8
                else: y += textheight(t, Wd - 32, fs, 'R', 1.45) + 8
        elif kind == 'box':
            _, title, t, fill, col = it
            hh = 24 + round((fs + 4) * 1.4) + textheight(t, Wd - 80, fs, 'R', 1.45) + 18
            if not dry:
                panelbox(c, (X, y, R, y + hh), fill=fill, sh=False); d = ImageDraw.Draw(c)
                d.text((X + 32, y + 18), title, font=F('K', fs + 4), fill=col)
                rich(d, X + 32, y + 24 + round((fs + 4) * 1.4), t, Wd - 80, fs, lh=1.45)
            y += hh
        y += 14
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


def auto(c, y, items, top=40):
    """字号自动取能放下的最大值"""
    for fs in range(top, 23, -1):
        if y + render_items(c, 0, items, fs, dry=True) < H - 110: break
    render_items(c, y, items, fs)


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
    d.text((136 + tw, 74), '日本骨科学会教育讲座', font=F('M', 30), fill=(190, 205, 222))
    d.text((56, 150), '肩袖撕了', font=F('K', 128), fill=WHITE)
    d.text((56, 310), '先别急着开刀', font=F('K', 112), fill=YEL)
    d.text((60, 500), '13 个查体动作 + 保守治疗有效率 + 谁适合保守', font=F('B', 36), fill=WHITE)
    photo(c, zh(52), (60, 680, 520, 1260), r=30, fy=.4, tag='吹号征', tagc=CORAL)
    a, b = split(58, 407)
    photo(c, b, (560, 680, 780, 1260), r=30, tag='抬离', tagc=TEAL); photo(c, zh(46), (800, 680, 1020, 1260), r=30, fx=.45, tag='空罐', tagc=NAVY)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([140, 1300, 940, 1384], 42, fill=YEL)
    s = '保守治疗 73%～80% 有效'; d.text((540 - d.textlength(s, font=F('K', 42)) / 2, 1314), s, font=F('K', 42), fill=NAVY)
    return c


def iceberg():
    c, d, y = base(2, T, '肩袖撕裂很常见，但多数不痛', '你在门诊看到的只是冰山一角')
    # 15 个小人：1 个就诊、4 个有症状未就诊、10 个无症状
    for i in range(15):
        r_, k = divmod(i, 5); x0 = 110 + k * 180; y0 = y + 10 + r_ * 150
        col = CORAL if i == 0 else ((200, 120, 0) if i < 5 else (170, 185, 200))
        d.ellipse([x0 + 40, y0, x0 + 90, y0 + 50], fill=col); d.rounded_rectangle([x0 + 25, y0 + 56, x0 + 105, y0 + 130], 22, fill=col)
    y += 470
    for col, t in ((CORAL, '1 人：有症状、来门诊'), ((200, 120, 0), '4 人：有症状，但没来门诊'), ((170, 185, 200), '10 人：撕裂了却不痛')):
        d.ellipse([60, y + 8, 92, y + 40], fill=col); d.text((110, y), t, font=F('B', 34), fill=INK); y += 58
    y += 16
    auto(c, y, [('bul', ['人群调查：**50 岁以上约 25%**、20 岁以上约 20% 有肩袖撕裂', '其中只有 **1/3 疼痛**；疼痛的人只有 **20%** 去医院 → 只有约 **1/15** 会来门诊',
                         '来门诊的 157 人中，**87.9% 因为痛**，10.8% 因为痛 + 无力，只有 1.3% 单纯因为无力'], CORAL),
                 ('box', '所以', '**控制疼痛是治疗的关键**。疼痛多与**炎症**有关：肩峰下注射局麻药后疼痛减轻、力量增加', LTEAL, TEAL)], top=40)
    return c


def table_card():
    c, d, y = base(12, T, '一张表：哪个试验查哪条肌腱', '定位撕裂的“专项”查体')
    R = [('冈上肌', '空罐试验、满罐试验', '以“无力”判断时准确率：满罐 75%、空罐 70%', CORAL, LCOR),
         ('冈下肌', '外旋坠落征 / 外旋滞后征', '对冈下肌 3～4 期脂肪变：敏感度、特异度均 100%', (200, 120, 0), LYEL),
         ('小圆肌', '吹号征', '对小圆肌 3～4 期脂肪变：敏感度 100%、特异度 93%', TEAL, LTEAL),
         ('肩胛下肌', '抬离试验；内旋受限时用压腹试验', '贴腰内旋位只剩肩胛下肌在工作', NAVY, LNAVY),
         ('全层撕裂（不定位）', '触诊肌腱缺损（delle）', '敏感度 96%、特异度 97%，与磁共振、超声相当', (90, 70, 170), (240, 240, 248)),
         ('肩峰下撞击', '疼痛弧、Neer 征、Hawkins 征', '提示疼痛来源，不定位撕裂', GREY, (236, 236, 236))]
    for a, b, e, col, fill in R:
        hh = 78 + textheight(e, 880, 32, 'R', 1.4) + 36
        panelbox(c, (60, y, 1020, y + hh), r=22, fill=fill, sh=False); d = ImageDraw.Draw(c)
        d.rectangle([60, y + 16, 70, y + hh - 16], fill=col)
        d.text((92, y + 14), a, font=F('K', 36), fill=col); tw = d.textlength(a, font=F('K', 36))
        d.text((110 + tw, y + 18), '→ ' + b, font=F('B', 31), fill=INK)
        rich(d, 92, y + 74, e, 880, 32, col=GREY, lh=1.4); y += hh + 22
    return c


def success():
    c, d, y = base(13, T, '保守治疗能好几成？', '全层撕裂，不手术')
    def fn():
        fig, ax = plt.subplots(figsize=(9.6, 5.2))
        L = ['Itoi 回顾\n62 肩，3.4 年', 'Itoi 前瞻\n103 肩，32 个月', 'Kuhn 多中心\n6 周', 'Kuhn 多中心\n2 年']; v = [82, 73, 90, 80]
        bb = ax.bar(L, v, color=['#9bc9d1', '#00788c', '#e9a27a', '#be2832'], width=.6)
        for r, t in zip(bb, v): ax.text(r.get_x() + r.get_width() / 2, t + 2, f'{t}%', ha='center', fontsize=20)
        ax.set_ylim(0, 105); ax.set_ylabel('成功率（%）', fontsize=16); ax.tick_params(labelsize=15)
        ax.spines[['top', 'right']].set_visible(False); fig.tight_layout(); return fig
    im = chart(fn); h = round(im.height * 960 / im.width); put(c, im, 60, y, 960, h); y += h + 26
    auto(c, y, [('bul', ['文献报道成功率 **33%～82%**；综合来看全层撕裂保守治疗约 **73%～80%** 有效',
                         'Itoi 前瞻研究：50% 完全不痛、40% 轻痛无需止痛药，75% 日常活动不受限',
                         '系统综述：运动治疗能**减轻疼痛、改善功能**，但对**活动度和力量**没有明显改善'], TEAL),
                 ('box', '保守治疗包括', '口服 NSAIDs；按撕裂部位向盂肱关节或肩峰下注射激素或透明质酸；热疗、牵伸、被动 / 主动活动度训练、肌力训练；**纠正肩胛运动障碍（肩胛前伸）**', LNAVY, NAVY)], top=40)
    return c


def responders():
    c, d, y = base(14, T, '谁适合保守？看 4 个因素', '123 肩：62 人有效 vs 56 人最终手术')
    def fn():
        fig, ax = plt.subplots(figsize=(9.6, 5.4))
        L = ['撞击征阳性\n（%）', '主动外旋\n（°）', '冈上肌肌内腱\n完整（%）', '冈上肌\n占有率（%）']; a = [30.7, 52.2, 58.4, 78.0]; b = [79.3, 35.0, 24.1, 69.8]
        x = np.arange(4); w = .38
        b1 = ax.bar(x - w / 2, a, w, color='#00788c', label='保守有效'); b2 = ax.bar(x + w / 2, b, w, color='#be2832', label='保守无效（手术）')
        for bs in (b1, b2):
            for r in bs: ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 1.5, f'{r.get_height():g}', ha='center', fontsize=15)
        ax.set_xticks(x); ax.set_xticklabels(L, fontsize=15); ax.set_ylim(0, 95); ax.legend(frameon=False, fontsize=15, ncol=2, loc='upper left')
        ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=14); fig.tight_layout(); return fig
    im = chart(fn); h = round(im.height * 960 / im.width); put(c, im, 60, y, 960, h); y += h + 26
    auto(c, y, [('steps', [('1', '**撞击征阴性**'), ('2', '**主动外旋角度好**'), ('3', '磁共振上**冈上肌肌内腱完整**'), ('4', '**冈上肌没有明显萎缩**')]),
                 ('box', '4 个因素都有 vs 都没有', '保守成功率 **92%** vs **5.2%**。冈上肌、冈下肌功能保留得好，最适合保守', LYEL, NAVY)], top=40)
    return c


def recurrence():
    c, d, y = base(15, T, '好了还会复发吗？', '复发和撕裂扩大有关')
    auto(c, y, [('bul', ['Yamaguchi：58 例**无症状撕裂**，平均 2.8 年后 **51% 出现症状**，与撕裂变大明显相关',
                         'Mall：195 例无症状撕裂，出现疼痛时，**18%** 的全层撕裂扩大 >5 mm，**40%** 的部分撕裂进展为全层',
                         'Safran：61 个 ≥5 mm 的全层撕裂，平均 29 个月 **49% 变大**，与疼痛相关'], CORAL),
                 ('h', '撕裂扩大的危险因素', NAVY),
                 ('steps', [('1', '年龄 **>60 岁**'), ('2', '**全层**撕裂'), ('3', '肩袖肌**脂肪浸润**'),
                            ('4', '**重体力劳动**：撕裂面积 8.2 cm² vs 中等 4.9、久坐 4.2 cm²（未发表数据）'), ('5', '**吸烟**：吸烟指数越高，撕裂越大')]),
                 ('box', '临床提示', '高风险扩大、肩袖功能差的人，保守效果差，**可能需要手术**；保守期间也要定期复查', LCOR, CORAL)], top=40)
    return c


def ending():
    c, d, y = base(16, T, '收藏：肩袖查体流程', '视诊 → 触诊 → 撞击 → 定位 → 决策')
    auto(c, y, [('steps', [('1', '**视诊**：冈下窝凹陷（萎缩）、肩胛位置、上举放下时肩胛内缘翘起'), ('2', '**触诊**：肩峰前缘摸肌腱缺损'),
                           ('3', '**疼痛弧 + 撞击征**：Neer、Hawkins 及改良'), ('4', '**定位**：空罐 / 满罐、外旋坠落征、吹号征、抬离 / 压腹'),
                           ('5', '**决策**：撞击征、外旋角度、磁共振肌内腱和萎缩 → 预判保守是否有效')]),
                 ('box', '文献', 'Itoi E. Rotator cuff tear: physical examination and conservative treatment. J Orthop Sci. 2013;18(2):197-204. doi:10.1007/s00776-012-0345-2', LNAVY, NAVY),
                 ('box', '版权', '原文版权归日本骨科学会（© JOA 2012，Springer 出版），未标注开放许可。图片引自原文，仅供学习交流，如有侵权请联系删除', LCOR, CORAL)], top=40)
    return c


T = 16
a51, b51 = split(51, 390)
a58, b58 = split(58, 407)
a59, b59 = split(59, 386)
cards = [cover(), iceberg(),
    pair(3, '视诊：先看后背', '图 1 肌肉萎缩，图 2 肩胛内缘翘起', zh(14), zh(15), '冈下窝凹陷', '肩胛内缘翘起', [
        ('bul', ['**冈下肌**就在皮下，从背后看**冈下窝凹陷**很容易发现萎缩（冈上肌被斜方肌盖住，不好看）',
                 '肩胛周围肌肉不给力时，肩胛**前伸**、离棘突更远',
                 '看手臂上举 / 放下时肩胛的运动：肩峰下撞击时，放下手臂时**肩胛内缘翘起**，以避免肩袖从肩峰下通过'], CORAL)]),
    figcard(4, T, '触诊：摸肩袖“缺口”', 'Codman 法，图 3', zh(16), [
        ('steps', [('1', '指尖放在**肩峰前缘的正前方**'), ('2', '**伸肩**时可摸到肌腱缺损（delle）；**屈肩**时缺损转到肩峰下就摸不到了')]),
        ('box', '准确性', '诊断全层撕裂：**敏感度 96%、特异度 97%**，与磁共振、超声相当', LTEAL, TEAL)]),
    pair(5, '疼痛弧和撞击征', '图 4 Neer 征，图 5 Hawkins 征', zh(32), zh(33), 'Neer 征', 'Hawkins 征', [
        ('box', '疼痛弧（主动）', '主动上举时 **90°～120°** 疼痛，放下时 **90°～30°** 疼痛', LYEL, NAVY),
        ('bul', ['被动活动时痛 = **撞击征阳性**', '**Neer 征**：一手按住肩胛防止旋转，把**内旋位**的手臂被动上举', '**Hawkins 征**：手臂**前屈**位，施加**内旋**力'], CORAL)]),
    pair(6, '改良 Neer 征和 Hawkins 征', '图 6、图 7', zh(34), zh(31), '改良 Neer', '改良 Hawkins', [
        ('bul', ['**改良 Neer 征**：手臂**外旋**位被动上举', '**改良 Hawkins 征**：手臂保持**外展**，施加**内旋**力'], CORAL),
        ('box', '有什么用', '撞击征提示疼痛来自**肩峰下撞击**；撞击征阳性的人，保守治疗效果更差（见后文）', LTEAL, TEAL)]),
    pair(7, '冈上肌：空罐和满罐', '图 8、图 9', zh(46), zh(45), '空罐：拇指朝下', '满罐：拇指朝上', [
        ('bul', ['手臂在**肩胛平面上举 90°**，检查者向下压', '**空罐**：内旋、拇指朝下；**满罐**：外旋、拇指朝上',
                 '冈上肌撕裂时，患者因**无力**扛不住，手臂被压下'], CORAL),
        ('box', '判断看“无力”', '以无力为阳性时准确率最高：**满罐 75%、空罐 70%**', LTEAL, TEAL)]),
    pair(8, '冈下肌：外旋坠落征', '图 10：a 健侧，b 患侧', a51, b51, 'a 健侧', 'b 患侧', [
        ('bul', ['上臂贴体侧测**外旋等长肌力**，最常用于查冈下肌撕裂', '把前臂放到外旋位后松手：健侧能**保持**外旋；冈下肌大部分撕裂时**保持不住**，前臂回到中立位',
                 'Hertel 的**外旋滞后征**与此类似'], CORAL),
        ('box', '准确性', '对冈下肌 3～4 期脂肪变：**敏感度、特异度均 100%**', LTEAL, TEAL)]),
    figcard(9, T, '小圆肌：吹号征', '图 11', zh(52), [
        ('steps', [('1', '让患者双手**举到嘴边**（像吹号）'), ('2', '健侧（左）手肘不用抬高就能做到；患侧（右）只能**抬高手肘、腕背伸**才够得着')]),
        ('box', '意义与准确性', '撕裂扩大到**小圆肌**时，外展位外旋无力。对小圆肌 3～4 期脂肪变：**敏感度 100%、特异度 93%**', LTEAL, TEAL)]),
    pair(10, '肩胛下肌：抬离试验', '图 12：a 正常，b 撕裂', a58, b58, 'a 能抬离', 'b 抬不起来', [
        ('bul', ['手背放在**腰部后方**：肩几乎完全内旋，此时**只剩肩胛下肌**还能继续内旋', '让患者把手**从背上抬离**；抬不起来或保持不住 → 提示肩胛下肌撕裂',
                 '中立位徒手测内旋不可靠：大圆肌、背阔肌、胸大肌都能代偿'], CORAL)]),
    pair(11, '肩胛下肌：压腹试验', '图 13：a 正常，b 撕裂；内旋受限时用', a59, b59, 'a 正常', 'b 撕裂', [
        ('bul', ['手掌压腹，**手、腕、肘保持一条直线**', '肩胛下肌撕裂时做不到：患者会**屈腕、把肘往后拉**来借力', '手背够不到腰后（内旋受限）时，用它代替抬离试验'], CORAL)]),
    table_card(), success(), responders(), recurrence(), ending()]
import os
os.makedirs(OUT, exist_ok=True)
for i, im in enumerate(cards, 1):
    im.save(f'{OUT}/card{i:02d}.jpg', quality=92)
print('ok', len(cards))
