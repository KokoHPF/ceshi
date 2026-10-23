#!/usr/bin/env python3
"""膝关节远程查体（Vomer 等 2023）小红书 3:4 图文学习卡片，1080×1440。
照片取自原文图 1～10（CC BY 4.0），分图按原图切开后配中文标签；文字为编者根据原文整理。
用法：python3 make_cards.py <原文 PDF> <思源黑体目录（NotoSansSC-Regular/Medium/Bold/Black.otf）> <输出目录>"""
import sys, re
from io import BytesIO
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PDF, FD, OUT = sys.argv[1:4]
doc = pymupdf.open(PDF)
W, H = 1080, 1440
BG = (247, 242, 235); NAVY = (22, 50, 79); CORAL = (238, 99, 72); TEAL = (24, 128, 128)
YEL = (255, 212, 92); INK = (40, 40, 40); GREY = (120, 120, 120); WHITE = (255, 255, 255)
LCOR = (253, 232, 225); LTEAL = (222, 240, 238); LYEL = (255, 244, 210); LNAVY = (228, 234, 242)
_fc = {}


def F(w, s):
    k = (w, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(f'{FD}/NotoSansSC-{ {"R": "Regular", "M": "Medium", "B": "Bold", "K": "Black"}[w]}.otf', s)
    return _fc[k]


def raw(x):
    return Image.open(BytesIO(doc.extract_image(x)['image'])).convert('RGB')


# 原文多分图照片的切分位置（像素）
PANELS = {107: [(0, 271), (277, 705), (711, 986)], 109: [(0, 496), (501, 986)], 111: [(0, 496), (501, 986)],
          126: [(0, 333), (338, 657), (662, 986)], 137: [(0, 496), (501, 986)], 152: [(0, 329), (334, 661), (666, 986)]}


def panel(x, i, row=None):
    im = raw(x)
    if x == 124:  # 2×2
        r, c = divmod(i, 2); xs = [(0, 499), (504, 986)][c]; ys = [(0, 326), (331, 651)][r]
        return im.crop((xs[0] + 6, ys[0] + 48, xs[1] - 6, ys[1] - 6))
    a, b = PANELS[x][i]
    return im.crop((a + 6, 48, b - 6, im.height - 6))  # 去掉分图字母和白色分隔线


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
    d.text((222, 62), '远程查膝 · 文献精读', font=F('M', 28), fill=GREY)
    d.text((60, 128), title, font=F('K', 64), fill=tc)
    y = 128 + 92
    if sub: d.text((62, y), sub, font=F('M', 32), fill=GREY); y += 56
    # 页脚
    d.line([60, H - 78, W - 60, H - 78], fill=(222, 214, 202), width=2)
    d.text((60, H - 62), '悦美力 · 物理治疗', font=F('M', 24), fill=GREY)
    s = 'Vomer 等 Cureus 2023;15(4):e37009'; d.text((W - 60 - d.textlength(s, font=F('R', 22)), H - 60), s, font=F('R', 22), fill=GREY)
    return c, d, y + 10


def bullet_list(d, x, y, items, w, fs=32, dot=CORAL, gap=18, lh=1.5):
    for it in items:
        d.ellipse([x, y + fs * .42, x + 14, y + fs * .42 + 14], fill=dot)
        y = rich(d, x + 32, y, it, w - 32, fs, lh=lh) + gap
    return y


def num(d, x, y, k, col=CORAL, r=30, fs=34):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=col)
    s = str(k); d.text((x + r - d.textlength(s, font=F('K', fs)) / 2, y + r - fs * .68), s, font=F('K', fs), fill=WHITE)


TOTAL = 11
cards = []

# ========== 01 封面 ==========
c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
# 背景大色块
d.rectangle([0, 0, W, 640], fill=NAVY)
d.ellipse([720, -180, 1260, 360], fill=(34, 70, 106))
d.rounded_rectangle([60, 64, 330, 120], 28, fill=CORAL); d.text((84, 68), '康复人必收藏', font=F('B', 34), fill=WHITE)
d.text((360, 74), 'Cureus 2023 文献精读', font=F('M', 30), fill=(190, 205, 222))
d.text((56, 150), '隔着屏幕', font=F('K', 148), fill=WHITE)
d.text((56, 320), '也能查膝盖', font=F('K', 148), fill=YEL)
d.text((60, 520), '远程膝关节查体 · 6 步流程 · 7 个自测试验', font=F('B', 40), fill=WHITE)
# 照片拼贴
p1 = panel(124, 1); p2 = panel(152, 1); p3 = raw(139)
photo(c, p1, (60, 700, 520, 1110), r=30, tag='深蹲看膝内扣', tagc=CORAL)
photo(c, p2, (560, 700, 1020, 1110), r=30, fy=.6, tag='Thessaly 自测', tagc=TEAL)
photo(c, p3, (60, 1140, 1020, 1300), r=30, fy=.12, tag='纸箱做后沉征', tagc=NAVY)
d = ImageDraw.Draw(c)
d.rounded_rectangle([140, 1316, 940, 1396], 40, fill=YEL)
s = '附 47 条问诊清单 + 红旗分诊'; d.text((540 - d.textlength(s, font=F('K', 42)) / 2, 1328), s, font=F('K', 42), fill=NAVY)
cards.append(c)

# ========== 02 为什么 + 准备 ==========
c, d, y = base(2, TOTAL, '视频问诊查膝，先做好准备', '疫情后远程问诊普及，但查体全靠患者自己做')
panelbox(c, (60, y, 1020, y + 320)); d = ImageDraw.Draw(c)
d.text((100, y + 30), '远程能做', font=F('K', 38), fill=TEAL)
bullet_list(d, 100, y + 96, ['看**动作和步态**，更贴近日常', '看**家里环境**，评估跌倒风险', '快速**分诊**：急诊还是先保守'], 410, fs=29, dot=TEAL, gap=12, lh=1.45)
d.line([540, y + 36, 540, y + 290], fill=(230, 224, 214), width=3)
d.text((575, y + 30), '远程做不了', font=F('K', 38), fill=CORAL)
bullet_list(d, 575, y + 96, ['**徒手测肌力**', '传统**特殊检查**（医生亲手做）', '亲手触诊和细微的疼痛表情'], 410, fs=29, gap=12, lh=1.45)
y += 360
d.text((60, y), '问诊前发给患者的准备清单', font=F('K', 44), fill=NAVY); y += 80
PREP = [('穿短裤或贴身运动服', '膝、大腿、小腿要露出来'), ('镜头能拍到全身', '前、侧、后三个方向都要拍'),
        ('一把椅子或一张床', '坐位、卧位检查要用'), ('一个纸箱或矮凳', '做“后沉征”时垫脚跟'), ('请家人在旁边', '扶一把、帮忙调镜头')]
for k, (a, b) in enumerate(PREP, 1):
    panelbox(c, (60, y, 1020, y + 104), r=24, sh=False, fill=WHITE); d = ImageDraw.Draw(c)
    num(d, 86, y + 22, k, col=[CORAL, TEAL, NAVY, CORAL, TEAL][k - 1])
    d.text((176, y + 12), a, font=F('B', 36), fill=INK); d.text((176, y + 60), b, font=F('R', 26), fill=GREY)
    y += 116
cards.append(c)

# ========== 03 流程总览 ==========
c, d, y = base(3, TOTAL, '6 步流程，一张图看懂', '按体位来：站 → 走 → 坐 → 躺，少折腾患者')
STEPS = [('病史', '起病、部位、性质、程度、放射、加重因素、已试过的处理；有无发热寒战', NAVY),
         ('视诊', '前、侧、后三面看全身力线；指出最痛点并画出放射范围', TEAL),
         ('触诊', '患者自己按压各结构；自做浮髌试验；摸远端脉搏', TEAL),
         ('活动度', '坐位屈伸、胫骨内外旋，与健侧对比；看 J 征', CORAL),
         ('力量 · 功能 · 步态', '抗重力动作代替徒手肌力；深蹲、单腿蹲、提踵；看步态', CORAL),
         ('特殊检查', '7 个“患者自己做”的改良试验，最后分诊', NAVY)]
x0 = 100
d.line([x0 + 30, y + 40, x0 + 30, y + 40 + 5 * 178], fill=(214, 204, 190), width=6)
for k, (a, b, col) in enumerate(STEPS, 1):
    num(d, x0, y + 10, k, col=col, r=32, fs=36)
    panelbox(c, (190, y - 6, 1020, y + 150), r=24, sh=False); d = ImageDraw.Draw(c)
    d.text((222, y + 10), a, font=F('K', 40), fill=col)
    rich(d, 222, y + 70, b, 770, 28, col=INK, lh=1.45)
    y += 178
cards.append(c)

# ========== 04 视诊 + 触诊 ==========
c, d, y = base(4, TOTAL, '视诊 + 触诊：让患者当你的手', '站着看力线，坐下自己摸')
photo(c, raw(97), (60, y, 480, y + 400), fy=.35, tag='摸关节线', tagc=TEAL)
d = ImageDraw.Draw(c)
d.text((520, y + 4), '视诊看什么', font=F('K', 38), fill=NAVY)
bullet_list(d, 520, y + 66, ['腰椎前凸、**髂嵴高低**、骨盆旋转', '髌骨、腓骨头位置，估 Q 角', '让患者**指出最痛点**、画出放射范围', '后面看足：**“脚趾过多”**＝过度旋前'], 500, fs=28, gap=8, dot=TEAL)
y += 450
d.text((60, y), '触诊清单（患者自己按）', font=F('K', 38), fill=NAVY); y += 66
CHIPS = ['股四头肌腱', '髂胫束', '腓骨头', '髌骨上下', '内侧关节面', '外侧关节面', '关节线', '腘窝包块', '远端脉搏']
xx = 60
for s in CHIPS:
    tw = d.textlength(s, font=F('M', 30))
    if xx + tw + 40 > 1020: xx = 60; y += 70
    d.rounded_rectangle([xx, y, xx + tw + 40, y + 54], 27, fill=LTEAL); d.text((xx + 20, y + 6), s, font=F('M', 30), fill=TEAL); xx += tw + 56
y += 100
panelbox(c, (60, y, 1020, y + 400), fill=LYEL, sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 28), '重点：自己做浮髌试验', font=F('K', 40), fill=CORAL)
for k, s in enumerate(['伸直腿，放松大腿', '一只手放在**髌骨上方**往下推', '另一只手**轻拍髌骨**', '有**“漂浮感”**→ 提示关节积液或积血'], 1):
    num(d, 100, y + 104 + (k - 1) * 70, k, col=NAVY, r=24, fs=28)
    rich(d, 166, y + 104 + (k - 1) * 70, s, 820, 34)
cards.append(c)

# ========== 05 活动度 ==========
c, d, y = base(5, TOTAL, '活动度：坐着就能估', '一定要和健侧比，角度只能目测')
ims = [panel(107, i) for i in range(3)]
bw = (960 - 2 * 20) // 3
for i, (im, t) in enumerate(zip(ims, ['坐位侧面', '伸膝', '屈膝'])):
    photo(c, im, (60 + i * (bw + 20), y, 60 + i * (bw + 20) + bw, y + 330), tag=t, tagc=[NAVY, TEAL, CORAL][i])
y += 370; d = ImageDraw.Draw(c)
ROM = [('屈膝', '0°～140°', '软组织挤压'), ('伸膝', '0°～15°', '软组织牵拉'), ('胫骨外旋', '30°～40°', '软组织牵拉'), ('胫骨内旋', '20°～30°', '软组织牵拉')]
panelbox(c, (60, y, 1020, y + 70 + 4 * 66), sh=False); d = ImageDraw.Draw(c)
d.rounded_rectangle([60, y, 1020, y + 66], 28, fill=NAVY); d.rectangle([60, y + 36, 1020, y + 66], fill=NAVY)
for xx, s in ((100, '动作'), (420, '正常范围'), (740, '终末感')): d.text((xx, y + 12), s, font=F('B', 30), fill=WHITE)
for k, (a, b2, e) in enumerate(ROM):
    yy = y + 76 + k * 66
    if k % 2: d.rectangle([62, yy - 6, 1018, yy + 58], fill=(250, 247, 242))
    d.text((100, yy), a, font=F('B', 31), fill=INK); d.text((420, yy), b2, font=F('K', 31), fill=CORAL); d.text((740, yy), e, font=F('R', 29), fill=GREY)
y += 70 + 4 * 66 + 34
j = [panel(109, 0), panel(109, 1)]
photo(c, j[0], (60, y, 290, y + 250), tag='正常', tagc=TEAL)
photo(c, j[1], (310, y, 540, y + 250), tag='J 征', tagc=CORAL)
d = ImageDraw.Draw(c)
rich(d, 572, y + 10, '伸膝时盯住**髌骨**\n走平滑弧线 → 正常\n走出“J”形 → 提示\n==髌骨不稳==', 450, 32, lh=1.55)
cards.append(c)

# ========== 06 力量 ==========
c, d, y = base(6, TOTAL, '没法徒手测肌力？', '用 5 个抗重力动作代替')
STR = [('坐位把膝完全伸直', '股四头肌'), ('坐位把膝完全屈曲', '腘绳肌'), ('提踵', '小腿跖屈肌'), ('侧卧抬起上方腿', '髋外展肌'), ('仰卧双腿桥 → 单腿桥', '髋伸肌')]
for k, (a, m) in enumerate(STR, 1):
    panelbox(c, (60, y, 1020, y + 104), r=24, sh=False); d = ImageDraw.Draw(c)
    num(d, 88, y + 22, k, col=[CORAL, TEAL, NAVY, CORAL, TEAL][k - 1])
    d.text((180, y + 26), a, font=F('B', 36), fill=INK)
    tw = d.textlength(m, font=F('B', 30)); d.rounded_rectangle([1000 - tw - 40, y + 24, 1000, y + 80], 28, fill=LTEAL); d.text((1000 - tw - 20, y + 30), m, font=F('B', 30), fill=TEAL)
    y += 118
y += 6
panelbox(c, (60, y, 1020, y + 200), fill=NAVY, sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 30), '能完成 ＝ 至少 3/5 级', font=F('K', 50), fill=YEL)
rich(d, 100, y + 108, '没有阻力，**最多只能判断“至少 3 级”**；再结合患者自觉的无力', 860, 30, col=WHITE, em=YEL)
y += 236
d.text((60, y), '更有价值的是功能动作质量', font=F('K', 38), fill=NAVY); y += 66
bullet_list(d, 60, y, ['**单腿蹲**：先健侧做基线，再做患侧，看髋无力、动态膝外翻、疼痛', '**提踵**：先双侧再单侧，从后面看腓肠肌向心和离心收缩'], 960, fs=30, gap=12)
cards.append(c)

# ========== 07 深蹲 + 步态 ==========
c, d, y = base(7, TOTAL, '深蹲和走路，藏着很多线索', '正面看膝，背面看髋')
bw = 470; bh = 270
for i, (t, col) in enumerate([('正面 · 正常', TEAL), ('膝内扣 · 异常', CORAL), ('背面 · 正常', TEAL), ('髋偏移 · 异常', CORAL)]):
    r_, c_ = divmod(i, 2)
    photo(c, panel(124, i), (60 + c_ * (bw + 20), y + r_ * (bh + 20), 60 + c_ * (bw + 20) + bw, y + r_ * (bh + 20) + bh), tag=t, tagc=col)
y += 2 * bh + 20 + 28; d = ImageDraw.Draw(c)
SQ = [('疼痛', '髌股关节受累'), ('膝内扣 + 痛', '内侧副韧带受累、患肢无力'), ('髋偏移', '偏离的那一侧无力或受限'), ('膝过度前移', '可能松弛')]
for k, (a, b) in enumerate(SQ):
    xx = 60 + (k % 2) * 490; yy = y + (k // 2) * 92
    d.rounded_rectangle([xx, yy, xx + 470, yy + 80], 20, fill=WHITE)
    d.text((xx + 22, yy + 8), a, font=F('B', 30), fill=CORAL); d.text((xx + 22, yy + 46), b, font=F('R', 24), fill=INK)
y += 196
d.text((60, y), '走向镜头、再走远，看步态', font=F('K', 36), fill=NAVY); y += 62
GA = [('骨盆往下掉', 'Trendelenburg 征，臀中肌无力'), ('脚“啪”地拍地', '腓总神经卡压'), ('走路痛', '疼痛步态'), ('上下楼痛', '髌股关节受累')]
for k, (a, b) in enumerate(GA):
    yy = y + k * 54
    d.ellipse([60, yy + 14, 74, yy + 28], fill=TEAL)
    d.text((88, yy), a, font=F('B', 30), fill=INK); d.text((330, yy + 2), '→ ' + b, font=F('M', 28), fill=TEAL)
cards.append(c)

# ========== 08 特殊检查 ① ==========
c, d, y = base(8, TOTAL, '患者自己做的特殊检查 ①', '韧带 · 髂胫束 · 后交叉韧带')
TESTS = [
    ([panel(126, 1), panel(126, 2)], ['往内弯', '往外弯'], '改良内、外翻应力',
     '站立，自己把膝**往内弯**（外翻）或**往外弯**（内翻）', '受力那一侧痛 → 内 / 外侧副韧带受累'),
    ([panel(137, 0), panel(137, 1)], ['按住', '伸膝'], '改良 Noble 挤压试验',
     '拇指按住**膝外上方髂胫束止点**，再把膝伸直', '痛 → 髂胫束综合征、腓骨头功能障碍'),
    ([raw(139)], ['纸箱垫脚跟'], '后沉征',
     '仰卧，屈髋屈膝 90°，脚跟搁纸箱上，**比两侧胫骨高度**', '一侧下沉 → 后交叉韧带受累'),
]
for ims, tags, name, how, pos in TESTS:
    panelbox(c, (60, y, 1020, y + 336), sh=False); d = ImageDraw.Draw(c)
    if len(ims) == 2:
        photo(c, ims[0], (84, y + 22, 284, y + 314), tag=tags[0], tagc=TEAL, sh=False, r=20)
        photo(c, ims[1], (296, y + 22, 496, y + 314), tag=tags[1], tagc=CORAL, sh=False, r=20)
    else:
        photo(c, ims[0], (84, y + 22, 496, y + 314), tag=tags[0], tagc=NAVY, sh=False, r=20, fy=.3, fx=.25)
    d = ImageDraw.Draw(c)
    d.text((528, y + 26), name, font=F('K', 36), fill=NAVY)
    yy = rich(d, 528, y + 88, how, 466, 28, lh=1.5)
    d.rounded_rectangle([528, yy + 10, 996, yy + 10 + textheight(pos, 430, 26, 'B', 1.45) + 24], 16, fill=LCOR)
    rich(d, 546, yy + 22, pos, 430, 26, col=CORAL, wt='B', lh=1.45)
    y += 356
cards.append(c)

# ========== 09 特殊检查 ② ==========
c, d, y = base(9, TOTAL, '患者自己做的特殊检查 ②', '半月板 · 髋前方紧张 · 髌股关节')
for i, (t, col) in enumerate([('单腿站', NAVY), ('向左转', TEAL), ('向右转', CORAL)]):
    photo(c, panel(152, i), (60 + i * 330, y, 60 + i * 330 + 300, y + 290), tag=t, tagc=col)
y += 312; d = ImageDraw.Draw(c)
d.text((60, y), '改良 Thessaly 试验', font=F('K', 40), fill=NAVY)
rich(d, 60, y + 62, '患侧单腿站、膝稍屈，**肩膀向左、向右转** → 膝痛提示**半月板病变**；站不稳就扶家人或桌子', 960, 29, lh=1.5)
y += 168
photo(c, raw(150), (60, y, 440, y + 360), fy=.25, tag='抱健侧膝躺下', tagc=TEAL)
d = ImageDraw.Draw(c)
d.text((470, y), '改良 Thomas 试验', font=F('K', 38), fill=NAVY)
TH = [('膝伸直', '股直肌'), ('髋屈曲', '髂腰肌'), ('小腿旋转', '髂胫束'), ('髋外展', '阔筋膜张肌')]
for k, (a, b) in enumerate(TH):
    yy = y + 70 + k * 66
    d.rounded_rectangle([470, yy, 1020, yy + 54], 16, fill=WHITE)
    d.text((492, yy + 7), '看患侧' + a, font=F('B', 28), fill=INK); d.text((800, yy + 7), '→ ' + b, font=F('B', 28), fill=TEAL)
y += 384
panelbox(c, (60, y, 1020, y + 150), fill=LNAVY, sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 22), '髌骨挤压试验', font=F('K', 34), fill=NAVY)
rich(d, 100, y + 78, '伸膝，用手**向下压髌骨**，痛 → 提示**髌股关节退变**', 880, 29)
cards.append(c)

# ========== 10 红旗 ==========
c = Image.new('RGB', (W, H), (60, 18, 22)); d = ImageDraw.Draw(c)
d.rounded_rectangle([60, 56, 200, 104], 24, fill=YEL); d.text((80, 58), f'10/{TOTAL}', font=F('B', 32), fill=(60, 18, 22))
d.text((222, 62), '远程查膝 · 文献精读', font=F('M', 28), fill=(220, 180, 175))
d.text((60, 120), '出现这些，', font=F('K', 76), fill=WHITE)
d.text((60, 216), '别再隔着屏幕看了！', font=F('K', 76), fill=YEL)
y = 350
RED = [('立即急诊 / 线下', ['直接钝器伤', '高处坠落', '体弱、病情复杂的患者'], (226, 64, 52)),
       ('尽快拍片', ['不能负重、严重疼痛步态', '膝关节肿胀、发红', '髋部外伤、夜间痛', '疼痛伴发热或寒战'], (238, 130, 60)),
       ('问诊里的危险信号', ['足部脉搏减弱 → 腘动脉损伤', '感觉减退 → 胫神经 / 腓总神经', '伤口、近期手术、红肿热 + 全身症状 → 化脓性关节炎等', '明显畸形、重大外伤 → 骨折', '仪表盘损伤 → 后交叉韧带', '无外伤的青少年膝痛 → 警惕股骨头骨骺滑脱'], (90, 120, 160))]
for name, its, col in RED:
    hh = 82 + sum(textheight(s, 860, 28, 'M', 1.35) + 6 for s in its) + 12
    d.rounded_rectangle([60, y, 1020, y + hh], 28, fill=WHITE)
    d.rounded_rectangle([60, y, 1020, y + 70], 28, fill=col); d.rectangle([60, y + 40, 1020, y + 70], fill=col)
    d.text((96, y + 12), name, font=F('K', 38), fill=WHITE)
    yy = y + 88
    for s in its:
        d.ellipse([100, yy + 13, 112, yy + 25], fill=col)
        yy = rich(d, 128, yy, s, 860, 28, wt='M', lh=1.35) + 6
    y += hh + 22
d.line([60, H - 78, W - 60, H - 78], fill=(110, 60, 60), width=2)
d.text((60, H - 62), '悦美力 · 物理治疗', font=F('M', 24), fill=(220, 180, 175))
cards.append(c)

# ========== 11 理性看待 ==========
c, d, y = base(11, TOTAL, '理性看待：它是分诊工具', '不是诊断工具')
panelbox(c, (60, y, 1020, y + 220), fill=NAVY, sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 14), '62%', font=F('K', 130), fill=YEL)
rich(d, 400, y + 56, '远程与线下膝关节评估的\n**平均一致率**（引自另一篇综述）', 580, 32, col=WHITE, em=YEL, lh=1.5)
y += 260
d.text((60, y), '使用时记住', font=F('K', 40), fill=NAVY); y += 70
y = bullet_list(d, 60, y, ['这是一份**操作指南**，没有患者数据；所有“改良”检查都**没和线下查体对照过**',
                           '力量只能判断“**至少 3 级**”，看动作质量和两侧对比更有用',
                           '改良特殊检查**只是线索**，可疑结构损伤仍要线下查体和影像确认'], 960, fs=30, gap=14)
y += 10
panelbox(c, (60, y, 1020, y + 330), fill=LCOR, sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 24), '原文避坑：这几处写错了', font=F('K', 36), fill=CORAL)
bullet_list(d, 100, y + 86, ['**髌骨倾斜试验**：外侧支持带紧张时，髌骨外侧**掀不起来**才是阳性，原文写反',
                             '“把膝往外弯”应是**内翻**试验，原文写成外翻',
                             '**股四头肌回避步态**是屈膝减少，原文写成“更屈曲”'], 880, fs=27, gap=8, lh=1.45)
y += 360
d = ImageDraw.Draw(c)
s = '收藏这套流程，下次视频问诊直接用'
d.rounded_rectangle([60, y, 1020, y + 84], 42, fill=YEL); d.text((540 - d.textlength(s, font=F('K', 36)) / 2, y + 16), s, font=F('K', 36), fill=NAVY)
d.text((60, H - 112), '原文 CC BY 4.0 开放获取，图片引自原文，如有侵权请联系删除', font=F('R', 22), fill=GREY)
cards.append(c)

for i, im in enumerate(cards, 1):
    im.save(f'{OUT}/card{i:02d}.jpg', quality=92)
print('ok', len(cards))
