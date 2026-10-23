#!/usr/bin/env python3
"""椎旁肌超声与磁共振图解（Hung 等 2024，Life）小红书 3:4 读图卡片，1080×1440，分上、中、下三篇。
原文 27 张图先由 tools/relabel.py 把英文标注原位改成中文（存于 src/zh/），本脚本按肌群排版并配中文解读。
用法：python3 xhs/make_cards.py <思源黑体目录> <输出目录>"""
import sys, re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FD, OUT = sys.argv[1:3]; SERIES = '背部肌肉超声'
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
    return Image.open(f'src/zh/z{x}.jpg').convert('RGB')


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
    lines = [[]]; cur = 0
    for txt, st in tokens(t):
        f = F('B' if st != 'n' else wt, fs)
        for ch in txt:
            if ch == '\n': lines.append([]); cur = 0; continue
            cw = f.getlength(ch)
            if cur + cw > w and lines[-1]:
                # 避免标点落在行首
                if ch in '，。、；：！？）」”' and lines[-1]: pass
                else: lines.append([]); cur = 0
            lines[-1].append((ch, st, cw)); cur += cw
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
    d.text((222, 62), SERIES + ' · 读图精讲', font=F('M', 28), fill=GREY)
    d.text((60, 128), title, font=F('K', 64), fill=tc)
    y = 128 + 92
    if sub: d.text((62, y), sub, font=F('M', 32), fill=GREY); y += 56
    # 页脚
    d.line([60, H - 78, W - 60, H - 78], fill=(222, 214, 202), width=2)
    d.text((60, H - 62), '骨科康复小黄', font=F('M', 24), fill=GREY)
    s = 'Hung 等 Life 2024;14(4):499'; d.text((W - 60 - d.textlength(s, font=F('R', 22)), H - 60), s, font=F('R', 22), fill=GREY)
    return c, d, y + 10


def bullet_list(d, x, y, items, w, fs=32, dot=CORAL, gap=18, lh=1.5):
    for it in items:
        d.ellipse([x, y + fs * .42, x + 14, y + fs * .42 + 14], fill=dot)
        y = rich(d, x + 32, y, it, w - 32, fs, lh=lh) + gap
    return y


def num(d, x, y, k, col=CORAL, r=30, fs=34):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=col)
    s = str(k); d.text((x + r - d.textlength(s, font=F('K', fs)) / 2, y + r - fs * .68), s, font=F('K', fs), fill=WHITE)


# 超声多行拼图的行范围（原图像素），用于把 3～4 行的大图分到两张卡片
ROWS = {67: [(0, 1538), (1538, 3048), (3048, 4549)], 81: [(0, 1366), (1366, 2714), (2714, 4035), (4035, 5368)],
        95: [(0, 1278), (1278, 2563), (2563, 3814), (3814, 5076)], 113: [(0, 1412), (1412, 2838)],
        120: [(0, 1330), (1330, 2655), (2655, 3996)], 135: [(0, 1554), (1554, 3123)], 142: [(0, 1580), (1580, 3127), (3127, 4692)],
        156: [(0, 1573), (1573, 3135)], 170: [(0, 1542), (1542, 3124)], 214: [(0, 1353), (1353, 2686), (2686, 3982), (3982, 5280)],
        228: [(0, 1430), (1430, 2882), (2882, 4324)], 242: [(0, 1570), (1570, 3102), (3102, 4622)]}


def rows(x, a, b):
    im = zh(x); r = ROWS[x]; return im.crop((0, r[a][0], im.width, r[b - 1][1]))


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
    for fs in (31, 30, 29, 28, 27, 26, 25, 24):
        c, d, y0 = base(n, total, title, sub)
        w = 960; h = round(img.height * w / img.width)
        mh = maxh or 820
        if h > mh: h = mh; w = round(img.width * h / img.height)
        th = render_items(c, 0, items, fs, dry=True)
        if y0 + h + 28 + th < H - 96: break
    else:
        raise SystemExit(f'卡片 {title} 放不下')
    x0 = 60 + (960 - w) // 2
    shadow(c, (x0, y0, x0 + w, y0 + h), 18)
    c.paste(img.resize((w, h), Image.LANCZOS), (x0, y0), rmask(w, h, 18))
    if tag:
        d = ImageDraw.Draw(c); f = F('B', 26); tw = d.textlength(tag, font=f)
        d.rounded_rectangle([x0 + w - tw - 40, y0 + h + 8, x0 + w, y0 + h + 52], 22, fill=LNAVY); d.text((x0 + w - tw - 20, y0 + h + 12), tag, font=f, fill=NAVY)
    render_items(c, y0 + h + 28 + (30 if tag else 0), items, fs)
    return c


SPLITX = {60: 1039, 74: 1696, 88: 1243, 102: 1185, 106: 1057, 128: 962, 149: 784, 163: 750, 177: 879, 188: 994, 203: 1880, 221: 1236, 235: 866}


def put(c, img, x0, y0, w, h):
    shadow(c, (x0, y0, x0 + w, y0 + h), 18); c.paste(img.resize((w, h), Image.LANCZOS), (x0, y0), rmask(w, h, 18))


def mri_card(n, total, title, sub, x, items):
    """磁共振卡：右侧轴位片（B 区）放大到整宽，左侧解剖示意图（A 区）作小图放在文字旁"""
    im = zh(x); sx = SPLITX[x]
    A = im.crop((0, 0, sx, im.height)); B = im.crop((sx + 8, 0, im.width, im.height))
    for fs in (30, 29, 28, 27, 26, 25, 24):
        c, d, y0 = base(n, total, title, sub)
        bw = 960; bh = round(B.height * bw / B.width)
        if bh > 760:  # 右侧是上下两张轴位片：缩到 760 高，示意图放右边
            bh = 760; bw = round(B.width * bh / B.height); aw = 960 - bw - 20; ah = round(A.height * aw / A.width)
            if ah > bh: ah = bh; aw = round(A.width * ah / A.height)
            ty = y0 + bh + 28; th = render_items(c, 0, items, fs, dry=True)
            if ty + th < H - 96: break
        else:
            aw = 250; ah = round(A.height * aw / A.width); ty = y0 + bh + 28
            if ty + ah > H - 100: ah = H - 100 - ty; aw = round(A.width * ah / A.height)  # 细长示意图按高度缩
            th = render_items(c, 0, items, fs, dry=True, X=60 + aw + 24, Wd=960 - aw - 24)
            if ty + max(th, ah) < H - 96: break
    else:
        raise SystemExit(f'卡片 {title} 放不下')
    if bh == 760:
        put(c, B, 60, y0, bw, bh); put(c, A, 60 + bw + 20, y0, aw, ah)
        render_items(c, ty, items, fs)
    else:
        put(c, B, 60, y0, bw, bh); put(c, A, 60, ty, aw, ah)
        render_items(c, ty, items, fs, X=60 + aw + 24, Wd=960 - aw - 24)
    return c


def cover(total, part, l1, l2, sub, ims, muscles):
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 620], fill=NAVY); d.ellipse([720, -180, 1260, 360], fill=(34, 70, 106))
    t = f'读图精讲 · {part}'; tw = d.textlength(t, font=F('B', 34))
    d.rounded_rectangle([60, 64, 108 + tw, 120], 28, fill=CORAL); d.text((84, 68), t, font=F('B', 34), fill=WHITE)
    d.text((136 + tw, 74), 'Life 2024 图解综述', font=F('M', 30), fill=(190, 205, 222))
    d.text((56, 150), l1, font=F('K', 112), fill=WHITE)
    d.text((56, 300), l2, font=F('K', 112), fill=YEL)
    d.text((60, 486), sub, font=F('B', 38), fill=WHITE)
    (a, ta), (b, tb) = ims
    photo(c, a, (60, 664, 1020, 920), r=26, tag=ta, tagc=CORAL)
    photo(c, b, (60, 944, 1020, 1200), r=26, tag=tb, tagc=TEAL)
    d = ImageDraw.Draw(c); y = 1228
    chips_y = y; xx = 60
    for s in muscles:
        tw = d.textlength(s, font=F('B', 30))
        if xx + tw + 40 > 1020: xx = 60; y += 64
        d.rounded_rectangle([xx, y, xx + tw + 40, y + 52], 26, fill=YEL); d.text((xx + 20, y + 6), s, font=F('B', 30), fill=NAVY); xx += tw + 54
    return c


def how_to_read(n, total):
    c, d, y = base(n, total, '先学会看这些图', '每组肌肉 = 解剖示意 + 轴位磁共振 + 超声')
    ex = rows(67, 0, 1)
    w = 960; h = round(ex.height * w / ex.width)
    shadow(c, (60, y, 60 + w, y + h), 18); c.paste(ex.resize((w, h), Image.LANCZOS), (60, y), rmask(w, h, 18)); d = ImageDraw.Draw(c)
    # 标注说明
    def call(px, py, k, col=CORAL):
        d.ellipse([px - 24, py - 24, px + 24, py + 24], fill=col, outline=WHITE, width=4)
        d.text((px - d.textlength(k, font=F('K', 30)) / 2, py - 21), k, font=F('K', 30), fill=WHITE)
    sx = w / ex.width
    call(60 + 300, y + 60, '1'); call(60 + 900, y + 175, '2'); call(60 + 360 + 10, y + h - 40, '3'); call(60 + 570, y + 70, '4')
    y += h + 30
    items = [('steps', [('1', '左边人形上的**红色长方形**：探头放在哪、朝什么方向'),
                        ('2', '**彩色阴影**：这一张要找的目标肌肉（原文用肤色、红、棕、黄区分）'),
                        ('3', '下方两角：**方向**（内侧 / 外侧、头侧 / 尾侧），左右对应探头两端'),
                        ('4', '画面**上方是皮肤（浅）**，往下越深；骨面、筋膜、神经常是**亮的高回声**，骨面后方是暗的声影')]),
             ('box', '磁共振图怎么看', '彩色块 = 目标肌肉；右下角小矢状位图上的**白色虚线**，标出这张轴位片所在的椎体水平（如 T9、C3）', LTEAL, TEAL)]
    render_items(c, y, items, 29)
    return c


def layers(n, total):
    c, d, y = base(n, total, '背部肌肉分三类', '从浅到深，先建立整体地图')
    G = [('浅层外在肌', '管上肢运动', '斜方肌、肩胛提肌、背阔肌、大菱形肌、小菱形肌', CORAL, LCOR),
         ('中层外在肌', '管呼吸', '上后锯肌、下后锯肌', (200, 120, 0), LYEL),
         ('固有肌 · 浅层', '夹肌', '头夹肌、颈夹肌（颈后外侧）', TEAL, LTEAL),
         ('固有肌 · 中层', '竖脊肌', '髂肋肌（最外）、最长肌、棘肌（最内）——颈、胸、腰都有', TEAL, LTEAL),
         ('固有肌 · 深层', '横突棘肌', '半棘肌、多裂肌、回旋肌（横突与棘突之间）', NAVY, LNAVY)]
    for a, b, t, col, fill in G:
        panelbox(c, (60, y, 1020, y + 150), r=24, fill=fill, sh=False); d = ImageDraw.Draw(c)
        d.rectangle([60, y + 24, 72, y + 126], fill=col)
        d.text((100, y + 18), a, font=F('K', 36), fill=col); tw = d.textlength(a, font=F('K', 36))
        d.rounded_rectangle([120 + tw, y + 22, 120 + tw + d.textlength(b, font=F('B', 26)) + 32, y + 64], 21, fill=col); d.text((136 + tw, y + 26), b, font=F('B', 26), fill=WHITE)
        rich(d, 100, y + 82, t, 900, 30, lh=1.4)
        y += 168
    y += 6
    render_items(c, y, [('bul', ['棘肌和回旋肌在超声上**很难和邻近肌肉分开**，原文没有单独讲',
                                 '全部超声用 **4–15 MHz 线阵**和 **1–6 MHz 凸阵**探头，受检者**俯卧或侧卧**'], TEAL)], 29)
    return c


# ======================= 上篇：肩胛背部浅层与后锯肌 =======================
def part1():
    T = 17; cs = []
    cs.append(cover(T, '上篇', '背部肌肉', '超声怎么扫', '中文标注的超声 + 磁共振图解',
                    [(rows(81, 2, 3), '大菱形肌 · 超声'), (zh(60).crop((0, 0, zh(60).width, 1500)), '斜方肌 · 背阔肌 · 磁共振')],
                    ['斜方肌', '背阔肌', '大小菱形肌', '肩胛提肌', '上后锯肌', '下后锯肌']))
    cs.append(layers(2, T)); cs.append(how_to_read(3, T))
    # 斜方肌 + 背阔肌
    cs.append(mri_card(4, T, '斜方肌和背阔肌', '解剖 + T9 轴位磁共振', 60, [
        ('bul', ['**斜方肌**：起于上项线内 1/3、枕外隆凸、项韧带和 **C7～T12 棘突**，止于锁骨外 1/3、肩峰、肩胛冈；稳定、移动肩胛，上部纤维还能伸颈',
                 '**背阔肌**：起于下 6 个胸椎棘突、胸腰筋膜、髂嵴后部，绕过大圆肌止于**结节间沟底**；使肱骨后伸、内收、内旋']),
        ('box', '读图', 'T9 层面两块肌肉都是**最表浅的一薄层**（棕 = 斜方肌，红 = 背阔肌），深面是竖脊肌和横突棘肌', LTEAL, TEAL)]))
    cs.append(figcard(5, T, '斜方肌：超声怎么扫', '图 2A、2B：上胸段', rows(67, 0, 2), [
        ('steps', [('A', '枕下靠棘突横放探头：斜方肌在头半棘肌浅面，**很薄**；往下滑到上胸段，**变厚变宽**、中线附着胸椎棘突'),
                   ('B', '往外：斜方肌一直延伸到肩峰，**盖在冈上肌表面**')])]))
    cs.append(figcard(6, T, '背阔肌：超声怎么扫', '图 2C：下胸段', rows(67, 2, 3), [
        ('steps', [('C', '继续往下到下胸段：背阔肌在下部斜方肌的**深面偏外**，是一层薄肌腹；到胸腰交界，它变成**最表浅**的背肌')]),
        ('box', '临床意义', '斜方肌扳机点很常见，痛可放射到**头、颈、肩、肩胛上区和肩胛间区**；超声引导注射可避开颈横动脉浅、深支和**副神经**。背阔肌损伤可单独发生，也可合并胸大肌、大圆肌或肩袖损伤，常见肱骨止点或肌腱结合处撕脱', LCOR, CORAL)]))
    # 菱形肌
    cs.append(mri_card(7, T, '大、小菱形肌', '解剖 + 磁共振（B 小菱形肌层面，C 大菱形肌层面）', 74, [
        ('bul', ['**小菱形肌**：起于项韧带下部和 **C7、T1 棘突**，止于肩胛骨内缘（肩胛冈水平）',
                 '**大菱形肌**：起于 **T2～T5 棘突**，止于小菱形肌下方的肩胛骨内缘',
                 '两者纤维平行、可融合成一块；把肩胛内缘向上内拉，完成**肩胛后缩**'])]))
    cs.append(figcard(8, T, '小菱形肌：超声怎么扫', '图 4A、4B：横斜切面', rows(81, 0, 2), [
        ('steps', [('A', '颈胸交界靠中线放探头，**朝肩胛冈方向斜向外下**：小菱形肌在斜方肌深面，呈四边形，以薄筋膜附着棘突'),
                   ('B', '靠近肩胛内缘时，小菱形肌比肩胛提肌**更靠内**；越往下，肩胛提肌越小，最后变成**高回声的腱性小条**')])]))
    cs.append(figcard(9, T, '大菱形肌：超声怎么扫', '图 4C、4D', rows(81, 2, 4), [
        ('steps', [('C', '从小菱形肌位置**往下滑**，保持同一方向，就看到大菱形肌'),
                   ('D', '探头**转 90°**：菱形肌群的短轴，大小菱形肌之间有一层**薄的筋膜**')]),
        ('box', '临床意义', '菱形肌是肩胛的重要稳定肌；**肩胛背神经**损伤可致菱形肌麻痹和**翼状肩胛**。做菱形肌扳机点注射要当心误伤这根神经', LCOR, CORAL)]))
    # 肩胛提肌
    cs.append(mri_card(10, T, '肩胛提肌', '解剖 + 磁共振', 88, [
        ('bul', ['起于 **C1～C4 横突后结节**，止于**肩胛骨内上缘**',
                 '主要作用是**上提肩胛**；配合其他肌肉可使肩胛下回旋（关节盂朝下），还参与伸颈和侧屈'])]))
    cs.append(figcard(11, T, '肩胛提肌：近端', '图 6A、6B：横切面', rows(95, 0, 2), [
        ('steps', [('A', '乳突下方 **C1 横突**水平横放，往下滑：从 C1～C4 横突各发出一束肌腹（1、2、3），表面是胸锁乳突肌'),
                   ('B', '到颈肩交界，几束合成一块走在斜方肌下：**副神经** = 斜方肌与肩胛提肌之间的高回声椭圆；**肩胛背神经**在肩胛提肌深面的筋膜层')])]))
    cs.append(figcard(12, T, '肩胛提肌：长轴和止点', '图 6C、6D', rows(95, 2, 4), [
        ('steps', [('C', '探头一端对**肩胛骨内上角**、另一端对 **C4 横突**或更高：看长轴'),
                   ('D', '想看**止点肌腱病变**（附着点病）：探头指向肩胛骨内面')]),
        ('box', '临床意义', '肩胛提肌附着点病常引起**肩胛内侧痛**；超声引导干预可避开**副神经和肩胛背神经**', LCOR, CORAL)]))
    # 后锯肌
    cs.append(mri_card(13, T, '上后锯肌', '图 7：解剖 + C7 轴位磁共振', 102, [
        ('bul', ['菱形肌深面的**薄四边形肌**', '起于项韧带下部和 **C7～T3 棘突**及棘上韧带', '向外下 4 个肌齿止于**第 2～5 肋**上缘', '上提肋骨，辅助**深吸气**'])]))
    cs.append(mri_card(14, T, '下后锯肌', '图 8：解剖 + T11 轴位磁共振', 106, [
        ('bul', ['胸腰交界处的**不规则四边形薄肌**', '起于 **T11～T12、L1～L2/3 棘突**和棘上韧带（与胸腰筋膜融合）', '向外上止于**下 4 肋**下缘、肋角外侧', '下拉肋骨，辅助**呼气**'])]))
    cs.append(figcard(15, T, '上后锯肌：超声怎么扫', '图 9：附着第 2、3 肋', zh(113), [
        ('steps', [('A', '探头放 **C7 棘突外侧**，向尾侧倾斜：最上一个肌齿是肩胛提肌深面的薄肌腹，从 C7 棘突斜向**第 2 肋角**，外侧可见**肩胛背动脉**'),
                   ('B', '往下滑，在肩胛提肌或菱形肌深面依次看到其余 3 个肌齿；让受检者**肩前伸**，可露出肋角')])]))
    cs.append(figcard(16, T, '下后锯肌：找“起始位”', '图 10A、10B', rows(120, 0, 2), [
        ('steps', [('A', '把**第 12 肋**放屏幕中央，探头旋转 **45°**（左侧顺时针、右侧逆时针）对准长轴：下后锯肌在第 12 肋浅面、背阔肌深面——这就是**起始位**'),
                   ('B', '往头侧滑：追到第 11～9 肋的附着')])]))
    cs.append(figcard(17, T, '下后锯肌：外侧缝', '图 10C', rows(120, 2, 3), [
        ('steps', [('C', '回到起始位再往尾侧：下后锯肌和背阔肌一起构成**胸腰筋膜后层**；在**外侧缝**处（腹肌筋膜与椎旁肌鞘汇合的致密结缔组织）与腰方肌、竖脊肌、腹肌相接')]),
        ('box', '临床意义', '上、下后锯肌的扳机点是**肩胛间区痛**和**胸腰段痛**的重要鉴别；超声引导上后锯肌注射被认为安全有效，可帮助诊断和治疗', LCOR, CORAL)]))
    return cs


# ======================= 中篇：颈部与枕下 =======================
def part2():
    T = 14; cs = []
    cs.append(cover(T, '中篇', '颈后肌肉', '超声怎么扫', '夹肌 · 最长肌 · 半棘肌 · 枕下肌',
                    [(rows(170, 0, 1), '头半棘肌 · 超声'), (zh(128).crop((0, 0, zh(128).width, 1700)), '头夹肌 · 头最长肌 · 磁共振')],
                    ['头夹肌', '头最长肌', '颈夹肌', '颈最长肌', '颈髂肋肌', '头/颈半棘肌', '颈多裂肌', '枕下肌']))
    cs.append(how_to_read(2, T))
    cs.append(mri_card(3, T, '头夹肌和头最长肌', '解剖 + C3 轴位磁共振', 128, [
        ('bul', ['**头夹肌**：起于 **C7～T3(4) 棘突**，止于乳突和上项线外 1/3 下方；在斜方肌深面、头半棘肌和头最长肌浅面。单侧收缩**同侧转头**，双侧伸头',
                 '**头最长肌**：起于下 3～4 个颈椎和上 4 个胸椎横突，斜向上前外止于**乳突后缘**，止点附近有**肌内腱**。单侧**同侧侧屈**，双侧伸头'])]))
    cs.append(figcard(4, T, '头夹肌：超声怎么扫', '图 12：短轴和长轴', zh(135), [
        ('steps', [('A', '**乳突尖后方**横放：由浅到深三层——胸锁乳突肌、头夹肌、头最长肌'),
                   ('B', '探头沿**乳突—C7 棘突连线**：头夹肌长轴')])]))
    cs.append(figcard(5, T, '头最长肌：乳突到 C1', '图 13A、13B', rows(142, 0, 2), [
        ('steps', [('A', '乳突水平：**枕动脉**可走在头最长肌内侧（深）或外侧（浅）'),
                   ('B', '往下到 C2 与乳突之间：能看到头最长肌的**肌内腱**')])]))
    cs.append(figcard(6, T, '头最长肌：颈中段', '图 13C', rows(142, 2, 3), [
        ('steps', [('C', '颈中段：头最长肌在**头半棘肌外缘前方**、**肩胛提肌后方**')]),
        ('box', '临床意义', '头夹肌、头最长肌是**颈部肌张力障碍**肉毒毒素注射的重要靶点；枕动脉可能绕行头最长肌，**超声引导**可避免误伤', LCOR, CORAL)]))
    cs.append(mri_card(7, T, '颈夹肌、颈最长肌、颈髂肋肌', '解剖 + 磁共振', 149, [
        ('bul', ['**颈髂肋肌**：第 3～6 肋角 → C4～C6 横突',
                 '**颈最长肌**：上 4～5 胸椎横突 → C2～C6 横突',
                 '**颈夹肌**：T3～T6 棘突 → C1～C3 横突',
                 '三者与头最长肌组成颈外侧**共同肌群**；单侧侧屈 / 转颈，双侧伸颈'])]))
    cs.append(figcard(8, T, '颈外侧三块肌：超声怎么扫', '图 15', zh(156), [
        ('steps', [('A', '三者在横突后结节处重叠，**超声很难分开**。颈中段：在肩胛提肌 4 束深面、关节柱浅面、头半棘肌和头最长肌外侧；**由外到内**依次是颈髂肋肌、颈最长肌、颈夹肌'),
                   ('B', '往下到颈胸交界：**上后锯肌**出现在这组肌肉的外缘')]),
        ('box', '临床意义', '这三块肌肉相对较小，**很少是背痛的主要来源**', LTEAL, TEAL)]))
    cs.append(mri_card(9, T, '头半棘肌和颈半棘肌', '解剖 + 磁共振', 163, [
        ('bul', ['**头半棘肌**：起于下 4 个颈椎上关节突和上 6～7 个胸椎横突，止于枕骨上、下项线之间；分**内、外侧头**，近端有厚腱隔；**枕大神经和第三枕神经穿过内侧头**',
                 '**颈半棘肌**：上 5～6 个胸椎横突 → **C2～C5 棘突**，伸颈',
                 '**颈多裂肌**：C4～C7 上关节突 → 上方 2～4 节的棘突，覆盖椎板'])]))
    cs.append(figcard(10, T, '头半棘肌：C1～C2 水平', '图 17A', rows(170, 0, 1), [
        ('steps', [('A', '**C1 水平**旁正中横放：头半棘肌在斜方肌深面、头夹肌内侧，**肌内腱隔**把它分成内侧束和外侧束'),
                   ('C2', '再往下到 C2：**枕大神经**是头半棘肌与头下斜肌之间的高回声椭圆')]),
        ('box', '临床意义', 'C1 水平头半棘肌内侧头：**一针同时阻滞枕大神经和第三枕神经**的合适靶点；慢性非特异性颈痛患者可见头半棘肌萎缩', LCOR, CORAL)]))
    cs.append(figcard(11, T, '颈半棘肌和颈多裂肌', '图 17B：颈中段', rows(170, 1, 2), [
        ('steps', [('B', '靠 C2 棘突横放、往下滑，看颈半棘肌从棘突发出；**颈深动脉**走在头、颈半棘肌之间的筋膜层，可作标志'),
                   ('B', '**多裂肌**在颈半棘肌深面：棘突与椎板交界外侧、椎板背侧、关节柱内侧')]),
        ('box', '临床意义', '颈半棘肌、颈多裂肌受刺激，疼痛可牵涉到**枕部、枕下、颈部和肩胛内上区**', LCOR, CORAL)]))
    cs.append(mri_card(12, T, '枕下肌群', '解剖 + 磁共振（B C1～2，C C2 水平）', 203, [
        ('bul', ['**头下斜肌**：C2 棘突 → C1 横突，同侧转头；**枕大神经从它上面经过**',
                 '**头上斜肌**：C1 横突 → 下项线外半，伸头、侧屈',
                 '**头后大直肌**：C2 棘突 → 下项线；**头后小直肌**：C1 后结节 → 下项线；伸头、同侧转头'])]))
    cs.append(figcard(13, T, '头下斜肌和头上斜肌', '图 23A、23B：长轴', rows(214, 0, 2), [
        ('steps', [('A', '探头内端放 **C2 棘突**、外端转向 **C1 横突**：C2 椎板上方的头下斜肌长轴；枕大神经在它和头半棘肌之间；深面是 C1/2 小关节，**外侧椎动脉、内侧 C2 背根神经节**'),
                   ('B', '外端留在 C1 横突、内端转向**枕骨**：头上斜肌长轴，C1 横突端是腱、枕骨端是肌')])]))
    cs.append(figcard(14, T, '头后大、小直肌', '图 23C、23D', rows(214, 2, 4), [
        ('steps', [('C', 'C1～C2 **旁正中矢状斜切**：两块直肌在棘突附着处（斜轴）'),
                   ('D', '在**枕骨与 C1 棘突之间横放**：头上斜肌、头后大直肌、头后小直肌的短轴')]),
        ('box', '临床意义', '枕下肌易受**挥鞭伤**（急减速）损伤；扳机点疼痛可从枕部放射到**颞部、眼周和前额**', LCOR, CORAL)]))
    return cs


# ======================= 下篇：胸腰段、前锯肌、腰方肌和腰大肌 =======================
def part3():
    T = 14; cs = []
    cs.append(cover(T, '下篇', '胸腰段肌肉', '超声怎么扫', '竖脊肌 · 多裂肌 · 前锯肌 · 腰方肌',
                    [(zh(195), '腰段竖脊肌和多裂肌 · 超声'), (rows(242, 2, 3), '腰方肌“三叶草征”')],
                    ['胸 / 腰髂肋肌', '胸最长肌', '胸半棘肌', '多裂肌', '前锯肌', '腰方肌', '腰大肌']))
    cs.append(how_to_read(2, T))
    cs.append(mri_card(3, T, '胸段竖脊肌和横突棘肌', '解剖 + T9 轴位磁共振', 177, [
        ('bul', ['**胸髂肋肌**：下 6 肋角 → C7 横突和上 6 肋角',
                 '**胸最长肌**：竖脊肌中**最大**；短的头端腱止于胸椎横突和邻近肋骨，长的尾端腱形成宽腱膜附着腰椎棘突、骶骨和髂嵴',
                 '**胸半棘肌**：T6～T10 横突 → C6～T4 棘突，伸胸椎；**胸多裂肌**：横突根部 → 上方 2～5 节棘突'])]))
    cs.append(figcard(4, T, '胸段：超声怎么扫', '图 19：肩胛间区横切', zh(184), [
        ('bul', ['肩胛间区横放：在菱形肌或上后锯肌深面，**由外到内**是胸髂肋肌、胸最长肌（**趴在横突上、最大**）',
                 '半棘肌和多裂肌在**棘突和横突之间**；多裂肌更深，紧贴**棘突与椎板交界**外侧',
                 '让受检者**肩前伸**（肩胛外展），更容易看清'], TEAL),
        ('box', '临床意义', '胸段固有背肌扳机点可致背痛并**向头、尾侧放射**；超声能看到损伤后的**肌肉水肿和正常纹理消失**，帮助制订康复方案', LCOR, CORAL)]))
    cs.append(mri_card(5, T, '腰段竖脊肌和多裂肌', '解剖 + 磁共振', 188, [
        ('bul', ['**胸最长肌腰部**：起于腰椎间腱膜，附着髂骨内侧和骶髂背侧韧带，止于腰椎**副突和横突**；外侧是**腰髂肋肌**',
                 '最长肌与多裂肌之间有一条充满**脂肪和静脉**的宽间隙',
                 '**腰多裂肌**：腰椎乳突和骶骨后面 → 上方 2～5 节的棘突'])]))
    cs.append(figcard(6, T, '腰段：超声怎么扫', '图 21：腰段横切', zh(195), [
        ('bul', ['上腰段棘突旁横放：**由外到内**依次是腰髂肋肌、胸最长肌、多裂肌',
                 '上腰段多裂肌局限在**椎板**上；从 **L3 往下**逐渐增大，最后覆盖骶骨',
                 '最长肌和髂肋肌向**横突**汇合；超声测多裂肌厚度（含动态体位）**可靠**'], TEAL),
        ('box', '临床意义', '腰段固有背肌扳机点可致**腰臀部痛**。多裂肌贡献约**三分之二的脊柱稳定性**，慢性腰痛患者主要萎缩的就是它', LCOR, CORAL)]))
    cs.append(mri_card(7, T, '前锯肌', '解剖 + 磁共振', 221, [
        ('bul', ['起于**第 1～8(9) 肋**，止于**肩胛骨内缘**',
                 '把肩胛向前拉、贴住胸壁（**前伸**）；与斜方肌上、下部一起**上回旋**肩胛，才能举手过头',
                 '肩带固定时可上提肋骨，辅助呼吸'])]))
    cs.append(figcard(8, T, '前锯肌：上部纤维', '图 25A、25B', rows(228, 0, 2), [
        ('steps', [('A', '俯卧，**肩胛冈水平**横放：肩胛骨下方的**三角形高回声**就是前锯肌上部；注意和同样附着肩胛内上角的**肩胛提肌**区分'),
                   ('B', '探头转成**矢状面**：看到它跨过肋间隙、止于肋骨')])]))
    cs.append(figcard(9, T, '前锯肌：下部肌齿', '图 25C', rows(228, 2, 3), [
        ('steps', [('C', '受检者**侧卧、患侧在上**，探头从**肩胛下角**朝下位肋骨横放，逐个看下部肌齿')]),
        ('box', '临床意义', '前锯肌扳机点的疼痛沿**腋中线第 5～7 肋**；超声引导注射比徒手触诊引导更能缓解疼痛，并**降低气胸风险**', LCOR, CORAL)]))
    cs.append(mri_card(10, T, '腰方肌和腰大肌', '解剖 + 磁共振', 235, [
        ('bul', ['**腰方肌**：髂嵴和髂腰韧带 → **第 12 肋和 L1～L4 横突**；侧屈腰椎、提骨盆，双侧收缩伸腰',
                 '**腰大肌**：T12～L4 椎体、椎间盘和 L1～L5 横突 → 与髂肌合成髂腰肌，止于**股骨小转子**；主要**屈髋**'])]))
    cs.append(figcard(11, T, '腰方肌：俯卧位扫查', '图 27A、27B', rows(242, 0, 2), [
        ('steps', [('A', '俯卧，腰椎中线旁放探头、上下移动找**横突**：腰方肌短轴在竖脊肌（髂肋肌、最长肌、多裂肌）**深面**，附着横突'),
                   ('B', '探头转成**头内—尾外**方向：腰方肌长轴从横突走到**髂嵴**；探头向内倾，可在椎体前外侧看到**腰大肌**')])]))
    cs.append(figcard(12, T, '腰方肌：三叶草征', '图 27C：侧卧位', rows(242, 2, 3), [
        ('steps', [('C', '**侧卧、患侧在上**，探头横放在腰椎侧面、上下找横突：腰方肌呈**三角形**（俯卧时是扁的），位于横突尖；它和腰大肌、竖脊肌围着横突，像一片**三叶草**')]),
        ('box', '临床意义', '腰方肌扳机点是**慢性腰痛**常见原因，痛在骶髂关节、臀部、大转子或腹股沟；腰大肌扳机点可致腰痛并放射到**腹股沟和膝**。超声引导注射对两者都有效', LCOR, CORAL)]))
    # 总结
    c, d, y = base(13, T, '总结：为什么要用超声', '看清每一块肌肉，注射才打得准')
    y = render_items(c, y, [('bul', ['超声能**区分各块椎旁肌**，提高肌筋膜痛干预的精度',
                                     '先**熟悉起止点**，才能认准扫到的是哪块肌肉',
                                     '配合颈、躯干的**屈伸和侧屈**动态扫查，可帮助确认痛源',
                                     '椎旁肌紧挨**脊髓、椎动脉、胸膜**等重要结构，注射**一定要超声引导**'], TEAL),
                            ('box', '还缺什么', '目前多是方法描述。超声上的**回声纹理、多普勒血流、弹性**在注射后会不会变化，还需要研究', LTEAL, TEAL),
                            ('box', '原文小问题', '图 17 的图注里 **“M”既指头半棘肌内侧束，又指多裂肌**，读图时要结合位置区分（本系列已分别译成“内侧束”和“多裂肌”）', LCOR, CORAL)], 30)
    cs.append(c)
    # 收尾
    c, d, y = base(14, T, '收藏这三篇，扫背不迷路', '上篇 · 中篇 · 下篇')
    y = render_items(c, y, [('steps', [('上', '斜方肌、背阔肌、菱形肌、肩胛提肌、上 / 下后锯肌'),
                                       ('中', '头 / 颈夹肌、头 / 颈最长肌、颈髂肋肌、半棘肌、颈多裂肌、枕下肌'),
                                       ('下', '胸 / 腰段竖脊肌、多裂肌、前锯肌、腰方肌、腰大肌')]),
                            ('box', '文献', 'Hung CY, Wang B, Chang HC, et al. Pictorial Essay on Ultrasound and Magnetic Resonance Imaging of Paraspinal Muscles for Myofascial Pain Syndrome. Life. 2024;14(4):499. doi:10.3390/life14040499', LNAVY, NAVY),
                            ('box', '版权', '原文以 **CC BY 4.0** 开放获取。图片引自原文，图中英文标注由编者改为中文；文字为编者解读，仅供学习交流，如有侵权请联系删除', LTEAL, TEAL)], 29)
    cs.append(c)
    return cs


import os
for name, fn in (('shang', part1), ('zhong', part2), ('xia', part3)):
    os.makedirs(f'{OUT}/{name}', exist_ok=True)
    for i, im in enumerate(fn(), 1):
        im.save(f'{OUT}/{name}/card{i:02d}.jpg', quality=92)
    print(name, 'ok')
