#!/usr/bin/env python3
"""Awaad 等 2026 JHSGO 食指、中指 III 区屈肌腱松解术后结合文化日常任务的康复（个案报告）：首图为原题直译标题卡；
原文图 1～3 直接用原图：图 1 支具照片和图 3 阿拉伯咖啡用具照片里的英文擦掉后在原位置写中文，图 2 念珠手势照片无文字，图注译成中文；
病程时间线卡、手指总主动活动度图和临床卡为编者根据原文整理。
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


def page_img(pno, xref, z):
    pg = doc[pno]; r = pg.get_image_rects(xref)[0]
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=r)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def relabel(im, boxes, k, dark):
    """boxes 坐标按 2.5 倍渲染给出，k 为实际渲染倍数 / 2.5；框内文字像素（dark=True 取深色，否则取彩色）用周围像素逐圈扩散填补，再在原位置写中文"""
    from scipy import ndimage
    a = np.asarray(im).astype(float); H_, W_ = a.shape[:2]; mask = np.zeros((H_, W_), bool)
    sat = a.max(2) - a.min(2); lum = a.mean(2)
    for (x0, y0, x1, y1), *_ in boxes:
        x0, y0, x1, y1 = (round(v * k) for v in (x0, y0, x1, y1))
        mask[y0:y1, x0:x1] = (lum[y0:y1, x0:x1] < 110) if dark else (sat[y0:y1, x0:x1] > 35)
    mask = ndimage.binary_dilation(mask, iterations=round(3 * k))
    known = ~mask; ker = np.ones((3, 3))
    while mask.any():
        cnt = ndimage.convolve(known.astype(float), ker, mode='constant')
        acc = np.stack([ndimage.convolve(a[..., c] * known, ker, mode='constant') for c in range(3)], -1)
        new = mask & (cnt > 0)
        a[new] = acc[new] / cnt[new][:, None]; known |= new; mask &= ~new
    im = Image.fromarray(a.clip(0, 255).astype('uint8')); d = ImageDraw.Draw(im)
    for (x0, y0, x1, y1), t, fs, al, fg in boxes:
        x0, y0, x1, y1 = (v * k for v in (x0, y0, x1, y1))
        f = font(fs * k); ls = t.split('\n'); lh = fs * k * 1.15; top = (y0 + y1) / 2 - lh * len(ls) / 2
        for i, l in enumerate(ls):
            w = d.textlength(l, font=f); x = x0 + 2 if al == 'l' else (x0 + x1 - w) / 2
            d.text((x, top + i * lh), l, font=f, fill=fg, stroke_width=round(2 * k) if dark else 0, stroke_fill='white')
    return im


def cover_from(im, cx=0.5, cy=0.5):
    """封面 900×383：从原文插图按比例裁出一块（cx、cy 为裁剪中心的相对位置）"""
    r = 900 / 383; w, h = im.size
    if w / h > r: cw, ch = round(h * r), h
    else: cw, ch = w, round(w / r)
    x = min(max(0, round(cx * w - cw / 2)), w - cw); y = min(max(0, round(cy * h - ch / 2)), h - ch)
    im.crop((x, y, x + cw, y + ch)).resize((900, 383), Image.LANCZOS).convert('RGB').save(f'{OUT}/cover.jpg', quality=90)


# 首图
W, H = 1400, 700; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '个案报告 · J Hand Surg Glob Online 2026', font=font(32), fill=TEAL)
for i, t in enumerate(['食指、中指 III 区屈肌腱松解术后', '结合文化习惯的康复方案：个案报告']):
    dr.text((70, 130 + i * 72), t, font=font(52), fill=INK)
dr.text((70, 300), 'Culturally Tailored Rehabilitation Approach "After zone III Flexor Tendon', font=font(27), fill=GREY)
dr.text((70, 338), 'Tenolysis in the Index and Middle Fingers: A Case Report', font=font(27), fill=GREY)
dr.line([70, 420, W - 70, 420], fill=(200, 205, 210), width=2)
dr.text((70, 450), 'Awaad S, Sherifi O, Al Katheri S, Fallatah S, Alfuraydi A, Hamzah H.', font=font(30), fill=GREY)
dr.text((70, 494), 'J Hand Surg Glob Online. 2026;8(3):100977. doi:10.1016/j.jhsg.2026.100977', font=font(30), fill=GREY)
dr.text((70, 550), '埃及扎加齐格大学 · 沙特国王大学 · 阿卜杜勒阿齐兹国王大学 · 泰巴大学', font=font(26), fill=GREY)
dr.text((70, 620), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 编者卡：病程时间线
phases('病程时间线（编者根据原文整理）', [
    ('2 岁', OR, (170, 90, 30), ['右手 III 区屈肌腱损伤，幼年手术修复，术后没有任何康复']),
    ('32 岁首诊', PK, RED, ['左利手男性，右手功能严重受限，只能用环指、小指抓握',
        '各指被动屈曲正常；食指、中指 PIP 和 DIP 完全不能主动屈曲，MCP 主动屈曲 80°（食指）、85°（中指）',
        'PIP 伸直欠缺 -15°（食指）、-20°（中指），总活动弧都只有 65°；握力因代偿无法可靠测量；中指持续麻木']),
    ('术前康复 12 次（数月）', LT, TEAL, ['镜像疗法 + 20 分钟综合训练：大鱼际、小鱼际肌力、抗阻和精细动作',
        '训练时配合感觉阈强度 TENS（100 Hz、50 μs、15～20 mA）；加入念珠手势（拇指依次对指）',
        '结果：PIP 伸直到 0°、MCP 屈曲到 90°，但 PIP、DIP 仍不能主动屈曲，证实存在粘连']),
    ('清醒局麻手术', GR, (40, 120, 60), ['术中发现粘连致密，且当年把指浅屈肌腱错误缝到了指深屈肌腱上',
        '切除无法保留的中指 FDS、保留 FDP；食指远端 FDP 粘连做端端固定', '关闭切口前，患者在手术台上就能主动握满拳、指尖触掌']),
    ('术后三期康复', PU, (90, 60, 150), ['0～3 周：背侧阻挡支具，单指伸直、被动活动，不主动抓握；念珠手势',
        '3～5 周：腕指联合屈伸；念珠手势分三步做差异性肌腱滑动', '6 周后：去支具主动活动，弹力带和治疗泥抗阻，阿拉伯咖啡方案']),
    ('随访 14～18 个月', LT, TEAL, ['14 个月握力 18 kg；18 个月中指指尖触掌 0 cm，食指 2 cm', '自述信心、手功能和社交参与明显改善'])], 2)

# 原文图 1：支具照片，英文擦掉写中文
f1 = page_img(1, 7, 4)
f1 = relabel(f1, [((2, 199, 318, 225), '掌指关节屈曲 60°', 22, 'l', (68, 114, 196)),
                  ((531, 156, 810, 185), '指间关节中立位', 22, 'l', (197, 90, 17)),
                  ((86, 333, 338, 359), '腕关节屈曲约 25°', 22, 'l', (56, 118, 29))], 4 / 2.5, False)
save(titled(capbox(f1, '修复术后使用的支具，由正常人示范：前臂背侧阻挡支具，腕关节屈曲约 25°，掌指关节屈曲 60°，指间关节中立位（原图注写作“II 区”，图中英文由编者译成中文覆盖）'),
            '原文图 1　背侧阻挡支具'), 3)

# 原文图 2：念珠手势照片
f2 = page_img(1, 13, 2.5)
save(titled(capbox(f2, '由正常人示范念珠手势练习：拇指依次与各指的指节相触（照片为原图，图注编者译成中文）'), '原文图 2　念珠（Tasbeeh）手势练习'), 4)

# 原文图 3：阿拉伯咖啡用具，英文擦掉写中文
f3 = page_img(2, 23, 5)
f3 = relabel(f3, [((36, 394, 167, 434), '咖啡杯\nFinjān', 16, 'c', (20, 20, 20)),
                  ((296, 452, 507, 496), '咖啡壶 Dallah', 22, 'c', (20, 20, 20))], 5 / 2.5, True)
save(titled(capbox(f3, '阿拉伯咖啡方案用到的器具：左手持咖啡壶（Dallah），右手持咖啡杯（Finjān）用于递出和接过（图中英文由编者译成中文覆盖，阿拉伯语名称保留）'),
            '原文图 3　阿拉伯咖啡方案的器具'), 5)

# 编者图：各时间点总主动活动度
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
fig, axes = plt.subplots(1, 2, figsize=(10.9, 5.2), dpi=110, sharey=True)
J = ['MCP', 'PIP', 'DIP']; C = ['#0F6E82', '#E08A2E', '#7A5AA6']
data = {'食指': [(80, 0, 0), (90, 90, 65)], '中指': [(85, 0, 0), (90, 90, 90)]}
for ax, (fg, rows) in zip(axes, data.items()):
    for i, vals in enumerate(rows):
        bot = 0
        for j, v in enumerate(vals):
            if v: ax.bar(i, v, bottom=bot, color=C[j], width=0.55, label=J[j] if i == 1 else None); ax.text(i, bot + v / 2, f'{J[j]} {v}°', ha='center', va='center', color='white', fontsize=12)
            bot += v
        ax.text(i, bot + 6, f'{bot}°', ha='center', fontsize=15, fontweight='bold')
    ax.set_xticks([0, 1]); ax.set_xticklabels(['术前', '出院时'], fontsize=14); ax.set_title(fg, fontsize=16)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
axes[0].set_ylabel('主动屈曲角度合计（°）', fontsize=13); axes[0].set_ylim(0, 300)
axes[1].legend(loc='upper left', fontsize=12, frameon=False)
fig.text(0.02, 0.015, '术前数值按原文“结局”一节（只有 MCP 能动）；原文病例描述里同期总活动弧为 65°（扣除了 PIP 伸直欠缺）', fontsize=11, color='#444')
fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(f'{OUT}/_tam.png'); plt.close(fig)
import os
tam = Image.open(f'{OUT}/_tam.png').convert('RGB'); os.remove(f'{OUT}/_tam.png')
save(titled(tam, '术前和出院时的总主动活动度（编者根据原文整理）'), 6)

phases('落到临床（编者整理）', [
    ('把训练装进患者熟悉的动作', LT, TEAL, ['念珠手势本质是拇指对指 + 依次屈指，可以替代或补充传统的肌腱滑动练习',
        '端咖啡壶、递咖啡杯练的是三指抓握、精细操作和耐力；换成筷子、茶杯、写字等本地日常任务同样适用',
        '对“记不住、做不进去”的患者，熟悉的动作更容易坚持']),
    ('陈旧性屈肌腱损伤的思路', OR, (170, 90, 30), ['被动活动正常、主动屈曲缺失，先做术前康复：把被动活动、伸直和内在肌练好再松解',
        '术前康复做到平台期仍不能主动屈指，提示需要手术松解', '清醒局麻下松解可以在手术台上直接验证主动屈曲']),
    ('别照搬', PK, RED, ['这是单个病例，没有对照、没有标准化的功能问卷，不能证明“文化化训练”优于常规训练',
        '术后 0～3 周用的是修复术后的保护支具，因为食指同时做了肌腱固定；单纯松解通常可以更早主动活动',
        '念珠和阿拉伯咖啡带有宗教和地域背景，借鉴的是“用患者熟悉的任务”这一思路'])], 7)

# 封面：原文图 2（念珠手势）上排
# 封面：图 2 上排 4 个手部动作（取原图数据，比页面渲染清晰），横向拼成一条
import io
raw2 = Image.open(io.BytesIO(doc.extract_image(13)['image'])).convert('RGB')
strip = Image.new('RGB', (4 * 320 + 3 * 10, 624), 'white')
for i, x0 in enumerate((10, 435, 913, 1735)):
    strip.paste(raw2.crop((x0, 6, x0 + 320, 630)), (i * 330, 0))
cover_from(strip, 0.5, 0.45)
