#!/usr/bin/env python3
"""髋关节活动受限的自我松动与肌肉再教育（Reiman & Matheson 2013）小红书 3:4 图文学习卡片，1080×1440。
照片取自原文图 1～15，a/b 拼图切开后配中文标签；表 1 和正文由编者整理为中文。
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


# 原文 a/b 上下拼图的切分行（像素）
SPLIT = {27: (469, 478), 32: (592, 604), 36: (413, 421), 41: (434, 443)}


def panel(x, i):
    im = raw(x); a, b = SPLIT[x]
    return im.crop((0, 34, im.width, a)) if i == 0 else im.crop((0, b + 34, im.width, im.height))  # 去掉 a/b 字母


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
    d.text((222, 62), '髋关节自我松动 · 文献精读', font=F('M', 28), fill=GREY)
    d.text((60, 128), title, font=F('K', 64), fill=tc)
    y = 128 + 92
    if sub: d.text((62, y), sub, font=F('M', 32), fill=GREY); y += 56
    # 页脚
    d.line([60, H - 78, W - 60, H - 78], fill=(222, 214, 202), width=2)
    d.text((60, H - 62), '骨科康复小黄', font=F('M', 24), fill=GREY)
    s = 'Reiman & Matheson. IJSPT 2013;8(5):729-740'; d.text((W - 60 - d.textlength(s, font=F('R', 22)), H - 60), s, font=F('R', 22), fill=GREY)
    return c, d, y + 10


def bullet_list(d, x, y, items, w, fs=32, dot=CORAL, gap=18, lh=1.5):
    for it in items:
        d.ellipse([x, y + fs * .42, x + 14, y + fs * .42 + 14], fill=dot)
        y = rich(d, x + 32, y, it, w - 32, fs, lh=lh) + gap
    return y


def num(d, x, y, k, col=CORAL, r=30, fs=34):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=col)
    s = str(k); d.text((x + r - d.textlength(s, font=F('K', fs)) / 2, y + r - fs * .68), s, font=F('K', fs), fill=WHITE)


TOTAL = 13
cards = []
COLS = [CORAL, TEAL, NAVY]


def chips(d, x, y, items, fill, col, fs=28, maxw=1020):
    xx = x
    for s in items:
        tw = d.textlength(s, font=F('M', fs))
        if xx + tw + 40 > maxw: xx = x; y += fs + 34
        d.rounded_rectangle([xx, y, xx + tw + 40, y + fs + 24], (fs + 24) // 2, fill=fill); d.text((xx + 20, y + 8), s, font=F('M', fs), fill=col); xx += tw + 54
    return y + fs + 24


def photos(c, y, items, h, gap=20):
    """items: (图, 标签, fy)；等宽一排"""
    n = len(items); w = (960 - gap * (n - 1)) // n
    for i, (im, t, fy) in enumerate(items):
        photo(c, im, (60 + i * (w + gap), y, 60 + i * (w + gap) + w, y + h), fy=fy, tag=t, tagc=COLS[i % 3])
    return y + h


def steps(d, y, items, fs=30, w=890, gap=12, col=NAVY):
    for k, s in enumerate(items, 1):
        num(d, 60, y + 2, k, col=col, r=22, fs=26)
        y = rich(d, 120, y, s, w, fs, lh=1.45) + gap
    return y


def tech(n, k, name, fit_for, ph, ph_h, how, notes=None, dose=None, ntitle='注意'):
    c, d, y = base(n, TOTAL, f'技术 {k}｜{name}')
    d.rounded_rectangle([60, y - 6, 1020, y + 52], 26, fill=LTEAL); rich(d, 84, y + 2, '适合：' + fit_for, 900, 28, col=TEAL, wt='B', lh=1.3)
    y += 76
    # 先量文字高度，照片高度按剩余空间自动放大
    th = 58 + sum(textheight(s, 890, 30, 'R', 1.45) + 12 for s in how)
    if dose: th += 86
    if notes: th += 76 + sum(textheight(s, 860, 27, 'R', 1.45) + 8 for s in notes) + 10
    ph_h = max(ph_h, min(620, H - 110 - y - 30 - th))
    y = photos(c, y, ph, ph_h) + 30; d = ImageDraw.Draw(c)
    d.text((60, y), '怎么做', font=F('K', 36), fill=NAVY); y += 58
    y = steps(d, y, how)
    if dose:
        y += 6; tw = d.textlength(dose, font=F('K', 32))
        d.rounded_rectangle([60, y, 120 + tw, y + 60], 30, fill=YEL); d.text((90, y + 8), dose, font=F('K', 32), fill=NAVY); y += 80
    if notes:
        hh = 76 + sum(textheight(s, 860, 27, 'R', 1.45) + 8 for s in notes) + 10
        panelbox(c, (60, y, 1020, y + hh), fill=LCOR, sh=False); d = ImageDraw.Draw(c)
        d.text((92, y + 18), ntitle, font=F('K', 32), fill=CORAL)
        bullet_list(d, 92, y + 72, notes, 890, fs=27, gap=8, lh=1.45)
        y += hh
    assert y < H - 90, (n, y)
    return c


# ========== 01 封面 ==========
c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
d.rectangle([0, 0, W, 640], fill=NAVY)
d.ellipse([720, -180, 1260, 360], fill=(34, 70, 106))
d.rounded_rectangle([60, 64, 330, 120], 28, fill=CORAL); d.text((84, 68), '康复人必收藏', font=F('B', 34), fill=WHITE)
d.text((360, 74), 'IJSPT 文献精读', font=F('M', 30), fill=(190, 205, 222))
d.text((56, 150), '髋关节卡住了？', font=F('K', 128), fill=WHITE)
d.text((56, 318), '7 招自我松动', font=F('K', 148), fill=YEL)
d.text((60, 520), '毛巾 + 绑带 + 凳子 · 在家也能做', font=F('B', 40), fill=WHITE)
photo(c, raw(17), (60, 690, 520, 1290), r=30, fy=.45, tag='深蹲 + 外侧牵引', tagc=CORAL)
photo(c, raw(25), (560, 690, 1020, 980), r=30, fy=.5, tag='跪凳后方滑动', tagc=TEAL)
photo(c, raw(42), (560, 1000, 1020, 1290), r=30, fy=.55, tag='仰卧长轴牵引', tagc=NAVY)
d = ImageDraw.Draw(c)
d.rounded_rectangle([140, 1316, 940, 1396], 40, fill=YEL)
s = '按受限方向选招 + 居家训练流程'; d.text((540 - d.textlength(s, font=F('K', 40)) / 2, 1330), s, font=F('K', 40), fill=NAVY)
cards.append(c)

# ========== 02 为什么 ==========
c, d, y = base(2, TOTAL, '髋活动度差，麻烦不只在髋', '活动受限会沿着动力链往上、往下传')
d.text((60, y), '和这些问题都有关', font=F('K', 36), fill=NAVY); y += 62
y = chips(d, 60, y, ['腰椎疾病', '膝踝等下肢问题', '髋骨关节炎', '运动相关腹股沟痛', '髋撞击 FAI', '髋臼盂唇撕裂'], LCOR, CORAL, fs=30) + 40
FACTS = [('FAI / 盂唇撕裂', '常见**屈曲、内旋、内收**受限', CORAL),
         ('髋骨关节炎', '**内旋受限**、**下蹲诱发疼痛**是很强的预测因素', TEAL),
         ('外展活动度下降', '被认为可能**预测下肢损伤**', NAVY),
         ('跑步', '伸髋不足可能让**骨盆前倾、腰椎前凸**增加', CORAL)]
for a, b, col in FACTS:
    panelbox(c, (60, y, 1020, y + 120), r=24, sh=False); d = ImageDraw.Draw(c)
    d.rectangle([60, y + 20, 70, y + 100], fill=col)
    d.text((96, y + 16), a, font=F('K', 34), fill=col); rich(d, 96, y + 66, b, 900, 28)
    y += 138
y += 10
panelbox(c, (60, y, 1020, y + 290), fill=NAVY, sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 28), '关节囊受限多在哪？', font=F('K', 38), fill=YEL)
rich(d, 100, y + 92, '最可能是**后方、下方、外侧**关节囊\n治疗师手法松动之后，配合**居家自我松动 + 肌肉再教育**，帮助把效果留住', 860, 30, col=WHITE, em=YEL, lh=1.6)
cards.append(c)

# ========== 03 开始前 ==========
c, d, y = base(3, TOTAL, '开始前，先过这三关', '自我松动是治疗的补充，不是替代')
d.text((60, y), '① 前提', font=F('K', 38), fill=NAVY); y += 66
y = bullet_list(d, 60, y, ['先由治疗师在诊所**做过、而且有效**', '在诊所**独立、正确地做 1～2 次**再带回家', '力量大小、方向、时长**由治疗师定**'], 960, fs=32, gap=12, dot=TEAL) + 36
d.text((60, y), '② 禁忌：有这些先别做', font=F('K', 38), fill=CORAL); y += 68
y = chips(d, 60, y, ['骨折史', '近期手术', '服用抗凝药', '症状在加重', '全身或局部韧带松弛', '全身性疾病'], LCOR, CORAL, fs=30) + 24
y = bullet_list(d, 60, y, ['也不适合：**骨性形态改变明显**、**终末感不明确**、**诊所试做反应差**'], 960, fs=31, gap=8) + 40
d.text((60, y), '③ 准备器材', font=F('K', 38), fill=NAVY); y += 68
y = chips(d, 60, y, ['毛巾 / 床单', '跳绳 / 绑带 / 腰带', '重物或拉力器', '稳固的台阶', '结实的凳子', '牢固的柱子或门'], LTEAL, TEAL, fs=30) + 60
panelbox(c, (60, y, 1020, y + 120), fill=(60, 18, 22), sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 20), '出现麻木、刺痛等异常', font=F('K', 34), fill=WHITE)
d.text((100, y + 66), '→ 立即停止，不要硬拉', font=F('B', 30), fill=YEL)
cards.append(c)

# ========== 04 速查 ==========
c, d, y = base(4, TOTAL, '按受限方向，选对招', '先评估，再挑技术')
PICK = [('屈髋 + 内收受限（如 FAI）', '① 下后方滑动'), ('负重屈髋差、蹲不深', '② 骨盆-股骨屈曲 + 外侧牵引'),
        ('后方、外侧关节囊紧', '③ 跪凳后方滑动'), ('屈髋 + 内旋不足', '④ 跪姿外侧牵引 + 主动内旋'),
        ('外侧紧、负重屈髋受不了', '⑤ 站立外侧牵引'), ('伸髋不足（跑者）', '⑥ 前方滑动 + 主动伸髋'), ('多方向都受限（如骨关节炎）', '⑦ 仰卧长轴牵引')]
for k, (a, b) in enumerate(PICK):
    col = COLS[k % 3]
    panelbox(c, (60, y, 1020, y + 132), r=24, sh=False); d = ImageDraw.Draw(c)
    d.text((92, y + 18), a, font=F('B', 32), fill=INK)
    d.text((92, y + 72), '→ ' + b, font=F('K', 32), fill=col)
    y += 148
cards.append(c)

# ========== 05～11 技术 ==========
cards.append(tech(5, 1, '下后方滑动', '屈髋、内收受限，如 FAI',
                  [(raw(7), '起始位', .3), (raw(11), '上台阶', .5), (raw(12), '后退步', .5)], 330,
                  ['患侧脚踩稳固台阶，旁边有扶手', '毛巾绕大腿、**尽量贴近髋**，接跳绳，跳绳挂**重物**', '双手握跳绳把手，**随时调节负荷**', '在负荷下做**上台阶**或**后退步**'],
                  ['只想松动：停在起始位不动；想做**振动式**：提把手卸重、再放下', '毛巾往下滑又绑不紧 → **不做**，或从更大屈髋位开始', '重量按耐受、安全和目标定，次数个体化']))
cards.append(tech(6, 2, '屈髋 + 外侧牵引', '负重下屈髋差、蹲不深（如 FAI）',
                  [(raw(16), '俯身屈髋', .4), (raw(17), '深蹲', .4), (raw(18), '拉力器', .4)], 320,
                  ['绑带绕大腿近端，另一端固定在**牢固物体或门后**，把股骨**往外拉**', '上身往地面俯，让**骨盆在股骨上屈曲**，加大屈髋', '进阶：在**弓步、深蹲**中保持外侧牵引', '换成拉力器：**内侧脚往拉力器方向推地**，激活髋外展、外旋肌'],
                  None, dose='单纯松动：3 组 × 30 次，每天 2 次'))
cards.append(tech(7, 3, '跪凳后方滑动', '后方、外侧关节囊受限；需要上肢力量',
                  [(raw(25), '后方滑动', .5), (raw(26), '后外侧滑动', .5)], 340,
                  ['患侧膝跪在凳上（可垫软垫），**屈髋约 90°**', '双手抓凳两侧，**把躯干拉向凳面** → 股骨头向后滑', '可向**后方或后外侧**摇动身体，加入运动', '也可再加绑带做外侧牵引'],
                  ['后外侧方向**更接近撞击位**：出现**髋前方症状**就停', 'FAI 也可能有**后方不稳**（有后脱位报道），要选对人', '骨性改变明显、终末感不明、试做反应差 → **不适合**'], ntitle='小心'))
cards.append(tech(8, 4, '跪姿外侧牵引', '后外侧关节囊受限，屈髋 + 内旋不足',
                  [(panel(27, 0), '起始', .5), (panel(27, 1), '重心转移', .5), (raw(31), '主动内旋', .45)], 330,
                  ['跪姿，绑带绕患侧大腿近端，**向外牵引**', '保持牵引，把**重心转移**到终末位，再回来', '进阶：体重压在股骨上（**后方滑动**）＋ 外侧牵引，同时**主动内旋**（小腿向外摆）'],
                  ['这一招同时给**后方 + 外侧**方向的力', '以诊所里的反应为准，不舒服就退回单纯牵引']))
cards.append(tech(9, 5, '站立外侧牵引', '外侧紧；负重屈髋、内收受不了的人',
                  [(panel(32, 1), '推开', .4), (panel(36, 1), '拉力器外展', .4), (raw(37), '加压内收', .5)], 320,
                  ['患侧靠近固定物站，绑带**向外牵引**', '把髋推离固定物，或用近侧手**推开肩和髋**（顺带拉体侧和髂胫束）', '**肌肉再教育**：用拉力器，从内收位**闭链外展**到终点 → 臀中肌向心 + 离心', '**加压版**：对侧手把同侧膝**拉向内收**（脚固定还带出内旋）'],
                  ['患腿跨过健腿内收：外侧张力更大，但**更易撞击**'], dose='肌肉再教育：2～3 组 × 15～20 次'))
cards.append(tech(10, 6, '前方滑动 + 主动伸髋', '伸髋不足，尤其是跑者',
                  [(panel(41, 0), '起始：轻度屈髋', .45), (panel(41, 1), '前移伸髋', .45)], 420,
                  ['绑带从后方套住大腿近端，**把股骨头往前拉**', '从**受限位前一点**的屈曲位开始，身体前移形成伸髋（伸髋肌参与）', '伸髋**过中立位**还不够：从终末位开始，**健腿向前迈步**'],
                  ['盯住腰：伸髋受限的人常**用腰椎后伸代偿**', '前方滑动受限较少被提到，但对伸髋很重要']))
cards.append(tech(11, 7, '仰卧长轴牵引', '多方向受限（如骨关节炎），需要整体牵伸',
                  [(raw(42), '踝部绑带牵引', .55)], 400,
                  ['仰卧，绑带 / 粗弹力管 / 拉力器套在**患侧踝部**', '身体**往头侧挪**产生牵引；加量：健侧屈髋屈膝踩地，**蹬地上移**', '**中范围**牵引 → 缓解疼痛；**外展或旋转终末位**牵引 → 改善活动度'],
                  ['受髋关节形状影响，这招**本质上是向下滑动**', '用拉力器要密切观察反应；**不要过度牵拉**']))

# ========== 12 居家流程 ==========
c, d, y = base(12, TOTAL, '一次居家训练怎么排', '原文表 1：把自我松动嵌进完整流程')
FLOW = [('热身 5～8 分钟', '功率车**高转速、几乎不加阻力**；屈髋 + 内收/内旋会痛的人，改用椭圆机、走路或慢跑', CORAL),
        ('静态拉伸', '屈髋肌、髋旋转肌、腘绳肌、股四头肌，**每组肌群 2 组 × 30～60 秒**', TEAL),
        ('自我松动', '次数、负荷、时长**按治疗师处方**', NAVY),
        ('新范围内练习', '在新获得的范围里做**终末位等长**和**全范围等张**练习', CORAL),
        ('动态和敏捷练习', '合适时再加，在新范围里建立**神经肌肉控制**', TEAL)]
d.line([92, y + 40, 92, y + 40 + 4 * 196], fill=(214, 204, 190), width=6)
for k, (a, b, col) in enumerate(FLOW, 1):
    num(d, 60, y + 10, k, col=col, r=32, fs=36)
    panelbox(c, (150, y - 6, 1020, y + 172), r=24, sh=False); d = ImageDraw.Draw(c)
    d.text((182, y + 12), a, font=F('K', 38), fill=col)
    rich(d, 182, y + 70, b, 810, 28, lh=1.45)
    y += 196
y += 6
rich(d, 60, y, '松动之后**一定要练**：用肌肉把新范围“锁住”', 960, 32, col=NAVY, wt='B')
cards.append(c)

# ========== 13 理性看待 ==========
c, d, y = base(13, TOTAL, '理性看待：它是辅助', '不是替代治疗师的手')
panelbox(c, (60, y, 1020, y + 220), fill=NAVY, sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 14), '5 级', font=F('K', 130), fill=YEL)
rich(d, 380, y + 56, '证据等级：**专家临床建议**\n推荐来自作者的经验观察', 600, 32, col=WHITE, em=YEL, lh=1.5)
y += 260
d.text((60, y), '使用时记住', font=F('K', 40), fill=NAVY); y += 70
y = bullet_list(d, 60, y, ['**没有直接证据**证明髋自我松动有效，也没比较过哪招更好',
                           '间接证据：**有监督、能坚持**的居家方案，效果好于无监督练习',
                           '要和治疗师的**手法和运动治疗**一起用，不能单独替代',
                           '每次复诊**重新评估**，没效果或加重就换方案'], 960, fs=30, gap=14)
y += 16
panelbox(c, (60, y, 1020, y + 200), fill=LTEAL, sh=False); d = ImageDraw.Draw(c)
d.text((100, y + 24), '好处在哪？', font=F('K', 36), fill=TEAL)
rich(d, 100, y + 84, '把诊所里的手法**延续到家里**，可能提高依从性、功能结果和患者的自我管理能力', 880, 30, lh=1.5)
y += 236
s = '收藏备用，练之前先问问你的治疗师'
d.rounded_rectangle([60, y, 1020, y + 84], 42, fill=YEL); d.text((540 - d.textlength(s, font=F('K', 36)) / 2, y + 16), s, font=F('K', 36), fill=NAVY)
d.text((60, H - 112), '原文未标注开放许可，图片版权归原作者及期刊，仅供学习交流，如有侵权请联系删除', font=F('R', 22), fill=GREY)
cards.append(c)

for i, im in enumerate(cards, 1):
    im.save(f'{OUT}/card{i:02d}.jpg', quality=92)
print('ok', len(cards))
