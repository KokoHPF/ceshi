#!/usr/bin/env python3
"""Selhorst 等 2020 IJSPT 青少年运动员腰椎峡部裂的康复考量：首图为原题直译标题卡；
原文图 1～6 直接用原图：图 1 椎骨模型照片里的英文标注擦掉后在原位置写中文，图 2～6 照片内无文字，图注译成中文；
原文表 1（三期康复方案）另做中文卡片，预后图和临床卡为编者根据原文整理。
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


import io

def cover_from(im, cx=0.5, cy=0.5):
    """封面 900×383：从原文插图按比例裁出一块（cx、cy 为裁剪中心的相对位置）"""
    r = 900 / 383; w, h = im.size
    if w / h > r: cw, ch = round(h * r), h
    else: cw, ch = w, round(w / r)
    x = min(max(0, round(cx * w - cw / 2)), w - cw); y = min(max(0, round(cy * h - ch / 2)), h - ch)
    im.crop((x, y, x + cw, y + ch)).resize((900, 383), Image.LANCZOS).convert('RGB').save(f'{OUT}/cover.jpg', quality=90)


# 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '临床述评 · Int J Sports Phys Ther 2020 · 证据等级 5', font=font(32), fill=TEAL)
dr.text((70, 140), '青少年运动员腰椎峡部裂的康复考量', font=font(56), fill=INK)
dr.text((70, 270), 'Rehabilitation Considerations for Spondylolysis in the Youth Athlete', font=font(30), fill=GREY)
dr.line([70, 360, W - 70, 360], fill=(200, 205, 210), width=2)
dr.text((70, 395), 'Selhorst M, Allen M, McHugh R, MacDonald J.', font=font(30), fill=GREY)
dr.text((70, 439), 'Int J Sports Phys Ther. 2020;15(2):287-300. doi:10.26603/ijspt20200287', font=font(30), fill=GREY)
dr.text((70, 500), '美国俄亥俄州 Nationwide 儿童医院 · 辛辛那提儿童医院医学中心', font=font(26), fill=GREY)
dr.text((70, 600), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 编者卡：关键数字
phases('峡部裂的关键数字（编者根据原文整理）', [
    ('有多常见', LT, TEAL, ['青少年运动员中患病率 7%～21%；有腰痛的青少年运动员中 14%～30%，是非运动员的 2～5 倍',
        '有腰痛的男孩比女孩多 1.6～4.5 倍；儿童 2.5%～4.5%，一般青少年和成人约 6%', '最常见于 L5，其次 L4；无症状者偶然发现的峡部裂不需要治疗']),
    ('谁容易得', OR, (170, 90, 30), ['反复、用力的后伸，尤其后伸加旋转', '棒球、田径投掷、板球、跳水、体操、足球、摔跤、举重风险更高']),
    ('怎么表现', PU, (90, 60, 150), ['无外伤、隐匿起病的局限性腰痛，活动尤其是后伸时加重，一般不向腿放射',
        '常见腰椎前凸增加、腘绳肌紧张', '病史和体检的诊断价值都很低：单腿后伸试验既不敏感也不特异，确诊要靠影像']),
    ('影像怎么选', GR, (40, 120, 60), ['先拍正侧位两张片；斜位片增加辐射却几乎不提高敏感度', 'SPECT/CT 敏感但辐射大；MRI 准确度已接近 SPECT/CT，且无辐射',
        '推荐：先正侧位 X 线，早期加 MRI，腰痛持续较久时用 CT'])], 2)

# 原文图 1、2
f1 = page_img(1, 4, 5)
f1 = relabel(f1, [((296, 210, 382, 300), '峡部\n缺损', 20, 'c', (20, 30, 60))], 5 / 2, True)
f2 = page_img(1, 5, 3)  # 直接取原图数据会反色，按页面渲染
gap = 15; tw = (1200 - gap) // 2; tiles = []
for ph, t in ((f1, '原文图 1　峡部型峡部裂示意（模型照片中的英文标注由编者译成中文覆盖）'), (f2, '原文图 2　L4 椎体双侧峡部裂的影像（图注写作“X 线片”，实为 CT 横断面）')):
    ph = ph.resize((tw, round(ph.height * tw / ph.width)), Image.LANCZOS); tiles.append((ph, t))
hh = max(p.height for p, _ in tiles); ch = max(para_h(t, 26, tw - 24, gap=8) for _, t in tiles)
im = Image.new('RGB', (1200, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im)
for i, (ph, t) in enumerate(tiles):
    x = i * (tw + gap); im.paste(ph, (x, 0))
    dr.rectangle([x, hh, x + tw, hh + ch + 20], fill=(232, 232, 232)); para(dr, x + 12, hh + 12, t, 26, tw - 24, gap=8)
save(titled(im, '原文图 1、2　峡部裂是什么'), 3)

# 编者图：预后和骨愈合
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.9, 5.0), dpi=110, gridspec_kw={'width_ratios': [1.15, 1]})
lab = ['全部', '单侧', '双侧', '急性期']; v = [28, 71, 18, 68]
a1.bar(range(4), v, color=['#888888', '#0F6E82', '#BE2832', '#E08A2E'], width=0.6)
for i, x in enumerate(v): a1.text(i, x + 2, f'{x}%', ha='center', fontsize=14)
a1.set_xticks(range(4)); a1.set_xticklabels(lab, fontsize=14); a1.set_ylim(0, 100); a1.set_title('保守治疗后影像骨愈合率', fontsize=15)
a1.text(1.5, 88, '终末期/慢性病灶：不愈合', ha='center', fontsize=12, color='#555')
rows = [('6 个月内回归运动，基本不痛', '92%', 92), ('1.5～8 年后腰痛再次影响活动', '45%～51%', 51), ('因疼痛减少或停止运动', '18%～40%', 40)]
for i, (t, s, x) in enumerate(rows):
    y = 2 - i; a2.barh(y, x, color='#0F6E82' if i == 0 else '#BE2832', height=0.5); a2.text(x + 2, y, s, va='center', fontsize=13)
    a2.text(0, y + 0.42, t, fontsize=12)
a2.set_xlim(0, 115); a2.set_ylim(-0.5, 2.9); a2.set_yticks([]); a2.set_title('临床结局', fontsize=15)
for ax in (a1, a2):
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
a2.spines['left'].set_visible(False); a1.set_yticks([]); a1.spines['left'].set_visible(False)
fig.text(0.02, 0.015, '影像愈合与生活质量、能否回归运动都无关；左图来自 10 项影像研究的荟萃分析，右图来自系统综述和长期随访研究', fontsize=11, color='#444')
fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(f'{OUT}/_pg.png'); plt.close(fig)
import os
pg = Image.open(f'{OUT}/_pg.png').convert('RGB'); os.remove(f'{OUT}/_pg.png')
save(titled(pg, '骨长不长好，和能不能回场是两回事（编者根据原文整理）'), 4)

# 原文表 1 中文卡
phases('原文表 1　青少年峡部裂运动员的物理治疗（编者译成中文）', [
    ('第一期　孤立训练', LT, TEAL, ['目标：宣教减少灾难化和恐惧回避；鼓励日常活动；启动局部肌群；改善活动受限；减轻疼痛',
        '肌肉表现：以核心局部肌为主；四肢活动时保持脊柱静态稳定；低负荷、脊柱有支撑的体位',
        '活动度：在疼痛最小的范围内逐步增加脊柱活动；避免失控的脊柱运动；必要时改善柔韧性；促进正常的腰盆节律',
        '测试：俯卧压力生物反馈测腹横肌；俯卧多裂肌抬臂试验；上下肢力量/柔韧性；躯干活动质与量；Micheli 功能量表',
        '进入下一期：腹横肌激活“良好”（俯卧压力下降 4 mmHg 保持 > 10 秒、无代偿）；多裂肌收缩正常；反复屈伸腰 10 次不痛']),
    ('第二期　整合训练', GR, (40, 120, 60), ['目标：局部肌与整体肌协同；开始站立平衡/动态活动；提高孤立肌群耐力；获得运动所需的柔韧性、活动度和力量；功能活动中控制脊柱运动',
        '肌肉表现：整合局部和整体肌群；脊柱运动中保持稳定；单平面进阶到多平面；直立功能位的核心控制',
        '活动度：保证专项所需的上肢、下肢和躯干活动度；继续促进正常腰盆节律',
        '测试：俯卧双腿抬起；仰卧双腿下放；观察异常运动；上下肢力量/柔韧性；Micheli 功能量表',
        '进入下一期：整体肌表现良好（俯卧双腿抬起 > 30 秒，仰卧双腿下放 < 70°）；各平面躯干主动活动完整、无代偿；专项动力链柔韧性和力量足够；Micheli 量表 B、C 部分 0 分']),
    ('第三期　回归运动', OR, (170, 90, 30), ['目标：渐进回归运动；最大化专项力量和耐力；专项动态活动中控制核心；建立合理训练计划和出院后自我管理',
        '训练：动态专项/位置练习；逐步增加强度和量；在监控下分级回归训练和比赛',
        '测试：模拟专项时的生物力学；回归过程中的症状和表现；Micheli 功能量表',
        '出院标准：全量、全强度专项动作流畅；无痛恢复伤前水平；Micheli 量表 0 分'])], 5, fs=22)

# 原文图 3～6
F_ZH = {3: (37, '原文图 3　腹横肌压力生物反馈测试：俯卧，气囊充到 70 mmHg，口令“收紧腹壁 10 秒，背不动、正常呼吸”；记录压力下降 ≥ 4 mmHg 能维持多久，同时监控代偿；≥ 10 秒为“良好”'),
        4: (38, '原文图 4　多裂肌抬臂试验：俯卧，肩外展约 120°、屈肘 90°；治疗师触摸 L4/L5、L5/S1 棘突间隙外侧，让患者把对侧手臂抬离床面约 5 cm；收缩明显有力为正常，几乎摸不到为异常'),
        5: (42, '原文图 5　俯卧双腿抬起试验：俯卧，双手垫在额下，双腿抬起至膝离开床面并保持；计时到膝不能离床或出现疼痛'),
        6: (43, '原文图 6　仰卧双腿下放试验：仰卧，治疗师把伸直的双腿抬到骶骨刚要离床的位置；患者保持腰贴床、自行缓慢放下双腿，记录腰部因骨盆前倾离开床面时的角度')}


def row(nums, title, n):
    gap = 15; tw = (1200 - gap) // 2; tiles = []
    for k in nums:
        x, t = F_ZH[k]; ph = Image.open(io.BytesIO(doc.extract_image(x)['image'])).convert('RGB')
        ph = ph.resize((tw, round(ph.height * tw / ph.width)), Image.LANCZOS); tiles.append((ph, t))
    hh = max(ph.height for ph, _ in tiles); ch = max(para_h(t, 24, tw - 24, gap=8) for _, t in tiles)
    im = Image.new('RGB', (1200, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im)
    for i, (ph, t) in enumerate(tiles):
        x = i * (tw + gap); im.paste(ph, (x, 0))
        dr.rectangle([x, hh, x + tw, hh + ch + 20], fill=(232, 232, 232)); para(dr, x + 12, hh + 12, t, 24, tw - 24, gap=8)
    save(titled(im, title), n)


row((3, 4), '原文图 3、4　第一期的局部肌测试（图注译成中文）', 6)
row((5, 6), '原文图 5、6　第二期的整体肌测试（图注译成中文）', 7)

phases('落到临床（编者整理）', [
    ('先把话说对', PK, RED, ['告诉孩子和家长：这是骨应力损伤，腰没有“断”；保守治疗 92% 能在半年内回场',
        '无症状的偶然发现不用治；影像愈合不是回场标准，按功能进阶，不必反复拍片']),
    ('休息和支具', OR, (170, 90, 30), ['常规建议停专项运动至少 3 个月，但作者主张诊断后几周内就开始有监督的训练，减少肌肉萎缩和体能下降',
        '不建议常规戴支具，症状不改善时再考虑']),
    ('三期按标准进阶', LT, TEAL, ['第一期：中立位、低负荷练腹横肌和多裂肌，年龄小的孩子用半泡沫轴、毛巾卷做外部反馈，嫌无聊就加不稳定面',
        '第二期：站起来、动起来，逐步加入后伸和旋转，而不是一直回避', '第三期：在教练、家长和队医配合下分级回场']),
    ('别只盯着腰', GR, (40, 120, 60), ['查髋屈肌、腘绳肌柔韧性；查胸椎旋转和肩外旋，比如投手旋转不够就会用腰代偿',
        '不做腰椎推拿（高速手法）；被动治疗少用，目的是让孩子动起来'])], 8)

# 封面：原文图 1（峡部缺损，已换中文标注）
# 封面：图 4 治疗师手法辅助多裂肌训练（真人操作，横幅构图）
import io
cover_from(Image.open(io.BytesIO(doc.extract_image(38)['image'])).convert('RGB'), 0.5, 0.55)
