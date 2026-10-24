#!/usr/bin/env python3
"""肱二头肌—盂唇复合体查体综述（Bryan 等 2024，Arthroscopy Techniques）小红书 3:4 图文卡片，1080×1440。
原文图 1～7 的英文标注先由 tools/relabel.py 原位改为中文（存于 src/zh/），本脚本排版并配中文解读。
用法：python3 xhs/make_cards.py <思源黑体目录> <输出目录>"""
import sys, re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

FD, OUT = sys.argv[1:3]; SERIES = '肩前痛查体'
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
    s = 'Bryan 等 Arthrosc Tech 2024;13(12):103136'; d.text((W - 60 - d.textlength(s, font=F('R', 22)), H - 60), s, font=F('R', 22), fill=GREY)
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
    render_items(c, y0 + h + 28, items, fs)
    return c

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


def cover():
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, 640], fill=NAVY); d.ellipse([720, -180, 1260, 360], fill=(34, 70, 106))
    t = '康复人必收藏'; tw = d.textlength(t, font=F('B', 34))
    d.rounded_rectangle([60, 64, 108 + tw, 120], 28, fill=CORAL); d.text((84, 68), t, font=F('B', 34), fill=WHITE)
    d.text((136 + tw, 74), 'HSS 团队 2024 查体综述', font=F('M', 30), fill=(190, 205, 222))
    d.text((56, 150), '肩前痛，', font=F('K', 120), fill=WHITE)
    d.text((56, 300), '先查二头肌', font=F('K', 128), fill=YEL)
    d.text((60, 500), '“三合一”查体 + 6 个经典试验，一次讲清', font=F('B', 38), fill=WHITE)
    photo(c, zh(24), (60, 680, 520, 1260), r=30, fx=.6, tag='抗阻投掷试验', tagc=CORAL)
    photo(c, zh(14).crop((0, 0, 1010, 1002)), (560, 680, 1020, 960), r=30, fy=.3, tag='O’Brien 征', tagc=TEAL)
    photo(c, zh(25), (560, 980, 1020, 1260), r=30, fy=.35, tag='触诊二头肌沟', tagc=NAVY)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([140, 1300, 940, 1384], 42, fill=YEL)
    s = '阴性就能基本排除 · 附准确性数据'; d.text((540 - d.textlength(s, font=F('K', 40)) / 2, 1316), s, font=F('K', 40), fill=NAVY)
    return c


def zones():
    c, d, y = base(2, T, '二头肌—盂唇复合体是什么', '盂唇上方 + 二头肌长头腱，分 3 个区')
    Z = [('关节内区', 'SLAP 损伤、前 / 后盂唇撕裂、二头肌长头腱在肱骨头与关节盂之间的动态嵌顿', CORAL, LCOR),
         ('交界区', '长头腱部分撕裂、二头肌软骨软化、肩胛下肌功能不全导致的近端长头腱不稳', (200, 120, 0), LYEL),
         ('二头肌沟区（关节外）', '长头腱部分撕裂、腱纽疼痛、长头腱不稳和狭窄、游离体', TEAL, LTEAL)]
    for k, (a, b, col, fill) in enumerate(Z, 1):
        hh = 80 + textheight(b, 840, 33, 'R', 1.45) + 32
        panelbox(c, (60, y, 1020, y + hh), r=24, fill=fill, sh=False); d = ImageDraw.Draw(c)
        num(d, 84, y + 20, k, col=col, r=26, fs=30); d.text((150, y + 18), a, font=F('K', 36), fill=col)
        rich(d, 150, y + 80, b, 840, 33, lh=1.45); y += hh + 26
    y += 6
    y = render_items(c, y, [('box', '为什么要靠查体', '**磁共振和关节镜单独使用都看不全**这 3 个区，尤其是关节外的二头肌沟区，关节镜下常被遮住；所以查体是诊断的关键', LNAVY, NAVY),
                            ('bul', ['常见于**过顶运动员**：肩前痛、不稳，投掷后期“咔哒”“弹响”', '常合并其他肩部损伤，和其他肩痛**症状重叠**'], CORAL)], 34)
    return c


def before():
    c, d, y = base(3, T, '专项查体之前，先做全面检查', '别一上来就做特殊试验')
    items = [('steps', [('1', '**颈椎**检查，排除颈源性肩痛'), ('2', '触诊**骨性标志**'), ('3', '主动、被动**活动度**和**肌力**'),
                        ('4', '过顶投掷者特别看**盂肱关节内旋不足（GIRD）**'), ('5', '仰卧位**负荷—移位试验**，评估前、后方稳定性'),
                        ('6', '怀疑肩胛问题时查 **SICK 肩胛**：肩胛位置异常、内下缘突出、喙突痛和位置异常、肩胛运动障碍')]),
             ('box', '查体分两组', '**“三合一”查体**：主动挤压试验（O’Brien 征）、抗阻投掷试验、二头肌沟触诊\n**传统试验**：Speed、Yergason、空罐、满罐、Crank、动态盂唇剪切试验', LTEAL, TEAL)]
    auto(c, y, items)
    return c


def auto(c, y, items, top=40):
    """字号自动取能放下的最大值"""
    for fs in range(top, 23, -1):
        if y + render_items(c, 0, items, fs, dry=True) < H - 110: break
    render_items(c, y, items, fs)


def text_card(n, title, sub, items, fs=None):
    c, d, y = base(n, T, title, sub); auto(c, y, items); return c


def evidence():
    c, d, y = base(11, T, '哪个试验更靠谱？', 'Taylor 等：116 例慢性症状 + 29 名无症状者')
    fig, ax = plt.subplots(figsize=(9.6, 5.6), dpi=100)
    G = [('传统 4 项', (15.2, 67.4), (75.6, 100.0)), ('“三合一”查体', (72.6, 97.8), (45.7, 78.8))]
    for i, (nm, se, sp) in enumerate(G):
        yv = 1 - i
        ax.plot(se, [yv + .12] * 2, color='#00788c', lw=22, solid_capstyle='round'); ax.plot(sp, [yv - .12] * 2, color='#be2832', lw=22, solid_capstyle='round')
        ax.text(se[1] + 2, yv + .12, f'{se[0]}～{se[1]}%', va='center', fontsize=17, color='#00788c')
        ax.text(sp[0] - 2, yv - .12, f'{sp[0]}～{sp[1]}%', va='center', ha='right', fontsize=17, color='#be2832')
    ax.set_yticks([1, 0]); ax.set_yticklabels([g[0] for g in G], fontsize=17); ax.set_xlim(0, 112); ax.set_ylim(-.6, 1.6)
    ax.plot([], [], color='#00788c', lw=8, label='敏感度范围'); ax.plot([], [], color='#be2832', lw=8, label='特异度范围')
    ax.legend(loc='upper center', ncol=2, frameon=False, fontsize=17, bbox_to_anchor=(.5, 1.12)); ax.set_xlabel('%', fontsize=15); ax.tick_params(labelsize=14)
    ax.spines[['top', 'right', 'left']].set_visible(False); ax.grid(axis='x', alpha=.3)
    fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
    im = Image.open(buf).convert('RGB'); put(c, im, 60, y, 960, round(im.height * 960 / im.width)); y += round(im.height * 960 / im.width) + 26
    render_items(c, y, [('bul', ['**传统 4 项**（Speed、Yergason、空罐、满罐）：特异度高、敏感度低，检查者间一致性弱到中等（κ 0.25～0.56）',
                                 '**“三合一”**：敏感度高、特异度较低；一致性好（κ 0.71 / 0.70 / 0.85）',
                                 '对**二头肌沟区**病变，阴性预测值：二头肌沟触诊 **96.4%**，O’Brien 征 **92.6%**——**阴性基本可排除**'], TEAL),
                        ('box', '其他研究', 'Speed：敏感度 32%、特异度 75%；Yergason：43%、79%（152 例）。另一研究中 Speed 敏感度 90%、特异度仅 13.8%——**结果差异很大**', LNAVY, NAVY)], 30)
    return c


def pearls():
    c, d, y = base(12, T, '要点与易错点', '原文表 2')
    P = [('O’Brien 征用 **Dines 或 Taylor 改良**，防止患者把被检侧外旋', '不控制对侧手臂，患者会把手臂转到肩胛平面，导致**假阴性或假阳性**'),
         ('**空罐 vs 满罐**：满罐痛偏向二头肌—盂唇，空罐痛偏向肩袖', 'O’Brien 征的痛要分清“**肩里面**”（复合体）还是“**肩顶上**”（肩锁关节）'),
         ('触诊二头肌沟时，**内、外旋上臂**更容易摸准长头腱', '按压**用力过大**会造成假阳性'),
         ('“三合一”阴性预测值高，**阴性可有效排除**关节外病变', '磁共振和关节镜都看不全 3 个区，**只靠影像会漏诊**')]
    d.rounded_rectangle([60, y, 530, y + 60], 20, fill=TEAL); d.rounded_rectangle([550, y, 1020, y + 60], 20, fill=CORAL)
    d.text((88, y + 8), '要点', font=F('K', 34), fill=WHITE); d.text((578, y + 8), '易错点', font=F('K', 34), fill=WHITE); y += 76
    for a, b in P:
        ha = textheight(a, 420, 33, 'R', 1.45); hb = textheight(b, 420, 33, 'R', 1.45); hh = max(ha, hb) + 56
        d.rounded_rectangle([60, y, 530, y + hh], 20, fill=LTEAL); d.rounded_rectangle([550, y, 1020, y + hh], 20, fill=LCOR)
        rich(d, 84, y + 28, a, 422, 33, lh=1.45); rich(d, 574, y + 28, b, 422, 33, lh=1.45); y += hh + 22
    return c


def ending():
    c, d, y = base(13, T, '一张图记住怎么查', '先“三合一”，再补传统试验')
    items = [('steps', [('1', '全面检查：颈椎、活动度、肌力、GIRD、稳定性、肩胛'), ('2', '**O’Brien 征**（Dines / Taylor 改良）：肩里面痛、掌心朝上减轻'),
                        ('3', '**抗阻投掷试验**：模拟投掷后期到加速早期'), ('4', '**二头肌沟触诊**：与健侧对比，力度适中'),
                        ('5', '补充：Speed、Yergason、满罐 / 空罐、Crank、动态盂唇剪切')]),
             ('box', '记住一句话', '“三合一”**阴性**→ 关节外二头肌病变基本可排除；**阳性**还要结合其他检查和影像', LYEL, NAVY),
             ('box', '文献', 'Bryan MR, White AE, Inclan PM, O’Brien SJ, Taylor SA. A Comprehensive Review of the Physical Examination for the Biceps-Labrum Complex of the Shoulder. Arthrosc Tech. 2024;13(12):103136', LNAVY, NAVY),
             ('box', '版权', '原文以 **CC BY-NC-ND 4.0** 开放获取（非商业、禁止演绎）。图片引自原文，英文标注由编者改为中文；仅供学习交流，如有侵权请联系删除', LCOR, CORAL)]
    auto(c, y, items)
    return c


T = 13
cards = [cover(), zones(), before(),
    figcard(4, T, 'O’Brien 征（主动挤压试验）', '三合一 ①：图 1，A Dines 改良，B Taylor 改良', zh(14), [
        ('steps', [('1', '站立面对检查者，双肩前屈 **90°**、伸肘；**完全内旋（拇指朝下）**，内收约 **10°～15°**，两手背相贴'),
                   ('2', '检查者向下施加**均匀的力**，患者抵抗保持 90°'),
                   ('3', '再在**外旋、掌心朝上**的位置重复')]),
        ('box', '阳性', '拇指朝下时“**肩里面**”痛，掌心朝上时**消失或减轻**。痛在“肩顶上”多为肩锁关节', LCOR, CORAL),
        ('bul', ['**Dines 改良**：双侧同时做、内收到中线，位置更稳定', '**Taylor 改良**：检查者握住对侧手腕，让对侧手臂前屈 45°、内旋，防止患者外旋被检侧'], TEAL)], maxh=420),
    figcard(5, T, '抗阻投掷试验', '三合一 ②：图 2', zh(24), [
        ('steps', [('1', '屈肘 **90°**、肩外展 **90°**、**最大外旋**，模拟投掷“后期准备”'),
                   ('2', '检查者站在被检侧后方，给手臂**等长阻力**'),
                   ('3', '患者对侧腿**向前迈步**，进入加速早期')]),
        ('box', '阳性', '诱发疼痛。对**交界区**病变最特异，也可提示二头肌沟区或关节内病变', LCOR, CORAL)], maxh=640),
    figcard(6, T, '二头肌沟触诊', '三合一 ③：图 3', zh(25), [
        ('steps', [('1', '上臂**中立位**，沿关节外的二头肌长头腱走行按压'),
                   ('2', '检查者被动**内、外旋**上臂，帮助摸准长头腱')]),
        ('box', '注意', '对**二头肌沟区**病变最敏感，也能帮助发现关节内和交界区病变。前肩**按得太重，正常人也会痛**——力度要控制，并**与健侧对比**', LCOR, CORAL)], maxh=660),
    figcard(7, T, 'Speed 试验', '传统试验：图 4', zh(26), [
        ('steps', [('1', '站立，肩前屈 **60°～90°**，前臂**完全旋后**、伸肘'),
                   ('2', '检查者向下压前臂，患者抵抗')]),
        ('box', '阳性与价值', '肩前方或关节内疼痛。多数研究认为**敏感度差、特异度尚可**', LNAVY, NAVY)], maxh=660),
    figcard(8, T, 'Yergason 试验', '传统试验：图 5，A 抗旋前，B 抗旋后', stackAB(zh(36)), [
        ('steps', [('1', '站立，上臂贴体侧、屈肘 **90°**'),
                   ('2', '前臂**完全旋前**起始，对抗检查者阻力做**旋后**；或从完全旋后起始，抵抗检查者使其**旋前**')]),
        ('box', '阳性与价值', '二头肌沟区或盂肱关节疼痛。**敏感度差、特异度高**', LNAVY, NAVY)], maxh=520),
]
c, d, y = base(9, T, '空罐 vs 满罐', '传统试验：图 6（空罐）、图 7（满罐）')
y = two(c, y, zh(37), zh(56), '空罐：拇指朝下', '满罐：拇指朝上', 700) + 28
render_items(c, y, [('bul', ['两者都是站立，肩在**肩胛平面**前屈 **90°**，检查者向下压，患者抵抗',
                             '**空罐**（Jobe 试验）：内旋、拇指朝下；疼痛传统上提示**冈上肌**病变',
                             '**满罐**：握拳、拇指朝上；疼痛或无力提示**冈上肌前缘、二头肌长头腱、肩胛下肌上缘**病变'], TEAL),
                    ('box', '怎么用', '**满罐痛偏向二头肌—盂唇复合体，空罐痛偏向肩袖**，两者对照帮助鉴别', LYEL, NAVY)], 33)
cards.append(c)
cards.append(text_card(10, 'Crank 和动态盂唇剪切试验', '原文无示意图，按文字整理', [
    ('h', 'Crank 试验', NAVY),
    ('steps', [('1', '坐位或仰卧，手臂上举到 **160°**'), ('2', '检查者沿肱骨**轴向加压**，同时内、外旋肱骨'),
               ('!', '疼痛多在**外旋**时出现，传统上提示盂唇病变；一项研究敏感度 46%、特异度 56%')]),
    ('h', '动态盂唇剪切试验', NAVY),
    ('steps', [('1', '站立，检查者在后方，一手握腕，一手在肱骨近端靠关节线处**向前推**'), ('2', '患者完全放松，手臂**外旋**，在身体平面内**外展到最大**'),
               ('!', '外展 **90°～120°** 之间肩痛或检查者在肩后方摸到**弹响**为阳性')]),
    ('box', '价值', '对 SLAP 损伤敏感度 78%、特异度 51%，阴性预测值 100%：**阴性可排除单纯 SLAP 损伤**，阳性却难以和合并损伤区分', LTEAL, TEAL)], fs=32))
cards += [evidence(), pearls(), ending()]
import os
os.makedirs(OUT, exist_ok=True)
for i, im in enumerate(cards, 1):
    im.save(f'{OUT}/card{i:02d}.jpg', quality=92)
print('ok', len(cards))
