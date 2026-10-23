#!/usr/bin/env python3
"""半月板修复术后康复推文配图：首图、原文图（英文换成中文）、编者整理卡片、封面
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


import io


def raw(x):
    return Image.open(io.BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def cover_from(im, cx=0.5, cy=0.5):
    """封面 900×383：从原文插图按比例裁出一块（cx、cy 为裁剪中心的相对位置）"""
    r = 900 / 383; w, h = im.size
    if w / h > r: cw, ch = round(h * r), h
    else: cw, ch = w, round(w / r)
    x = min(max(0, round(cx * w - cw / 2)), w - cw); y = min(max(0, round(cy * h - ch / 2)), h - ch)
    im.crop((x, y, x + cw, y + ch)).resize((900, 383), Image.LANCZOS).convert('RGB').save(f'{OUT}/cover.jpg', quality=90)


def tiles(items, title, n, fs=24):
    """原图并排（等高），下方灰底中文图注"""
    gap = 15; W = 1200; hs = 600
    ims = [x.resize((round(x.width * hs / x.height), hs), Image.LANCZOS) for x, _ in items]
    k = (W - gap * (len(ims) - 1)) / sum(i.width for i in ims)
    ims = [i.resize((round(i.width * k), round(i.height * k)), Image.LANCZOS) for i in ims]
    hh = ims[0].height; ch = max(para_h(t, fs, i.width - 24, gap=8) for i, (_, t) in zip(ims, items))
    im = Image.new('RGB', (W, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im); x = 0
    for i, (_, t) in zip(ims, items):
        im.paste(i, (x, 0)); dr.rectangle([x, hh, x + i.width, hh + ch + 20], fill=(232, 232, 232))
        para(dr, x + 12, hh + 12, t, fs, i.width - 24, gap=8); x += i.width + gap
    save(titled(im, title), n)


def one(x, cap, title, n):
    save(titled(capbox(x, cap), title), n)


def title_card(tag, zh, en, au, cite, org):
    W, H = 1400, 700; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, 18, H], fill=TEAL)
    dr.text((70, 56), tag, font=font(32), fill=TEAL)
    y = 130
    for l in zh: dr.text((70, y), l, font=font(50), fill=INK); y += 70
    y += 20
    for l in en: dr.text((70, y), l, font=font(28), fill=GREY); y += 40
    y += 20; dr.line([70, y, W - 70, y], fill=(200, 205, 210), width=2); y += 30
    dr.text((70, y), au, font=font(30), fill=GREY); y += 44
    dr.text((70, y), cite, font=font(28), fill=GREY); y += 56
    dr.text((70, y), org, font=font(26), fill=GREY)
    dr.text((70, H - 60), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
    save(im, 1)


def zh_label(im, boxes):
    """图中白底英文标注：整块刷成底色后在原位置写中文。boxes 为 (x0, y0, x1, y1, 文字, 字号, 对齐)"""
    d = ImageDraw.Draw(im); a = np.asarray(im.convert('L')) < 240; H_, W_ = a.shape
    for x0, y0, x1, y1, t, fs, al in boxes:
        # 向外扩到字母上下沿的浅色像素，碰到照片（成片非白）就停
        e0, e1, ex0, ex1 = y0, y1, max(0, x0 - 8), min(W_, x1 + 8)
        while e0 > 0 and y0 - e0 < 14 and a[e0 - 1, ex0:ex1].mean() < 0.3: e0 -= 1
        while e1 < H_ - 1 and e1 - y1 < 14 and a[e1 + 1, ex0:ex1].mean() < 0.3: e1 += 1
        d.rectangle([ex0, e0, ex1, e1], fill='white')
        f = font(fs); w = d.textlength(t, font=f); cy = (y0 + y1) / 2
        x = x0 if al == 'l' else (x1 - w if al == 'r' else (x0 + x1 - w) / 2)
        d.text((x, cy), t, font=f, fill=(0, 0, 0), anchor='lm')
    return im


def zh_boxes(im, boxes, s):
    """流程图：方框内部刷成框内底色（保留边框），再写中文。坐标按缩略图给出，s 为放大倍数"""
    d = ImageDraw.Draw(im); a = np.asarray(im)
    for (x0, y0, x1, y1), t, fs, al in boxes:
        x0, y0, x1, y1 = (round(v * s) for v in (x0, y0, x1, y1)); m = round(2.5 * s)
        bg = tuple(int(c) for c in np.median(a[y0 + m:y1 - m, x0 + m:x1 - m].reshape(-1, 3), 0))
        d.rectangle([x0 + m, y0 + m, x1 - m, y1 - m], fill=bg)
        fg = 'white' if sum(bg) < 500 else (20, 20, 20); f = font(fs * s); ls = t.split('\n'); lh = fs * s * 1.3
        top = (y0 + y1) / 2 - lh * len(ls) / 2 + lh / 2
        for i, l in enumerate(ls):
            x = x0 + m + 4 if al == 'l' else (x0 + x1 - d.textlength(l, font=f)) / 2
            d.text((x, top + i * lh), l, font=f, fill=fg, anchor='lm')
    return im


def heal(im, mask, it=400):
    """把 mask 区域（文字笔画）用四邻域扩散补成周围底色（照片上的字母用）"""
    a = np.asarray(im).astype(float); m = mask.copy(); a[m] = a[~m].mean(0)
    ys, xs = np.nonzero(m); y0, y1, x0, x1 = max(ys.min() - 2, 0), ys.max() + 3, max(xs.min() - 2, 0), xs.max() + 3
    sub = a[y0:y1, x0:x1]; sm = m[y0:y1, x0:x1]
    for _ in range(it):
        p = np.pad(sub, ((1, 1), (1, 1), (0, 0)), mode='edge')
        avg = (p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) / 4
        sub[sm] = avg[sm]
    a[y0:y1, x0:x1] = sub
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def dark_mask(im, boxes, thr=90, grow=2):
    """boxes 内比 thr 暗的像素（黑色字母）作为 mask，向外扩 grow 像素"""
    g = np.asarray(im.convert('L')); m = np.zeros(g.shape, bool)
    for x0, y0, x1, y1 in boxes: m[y0:y1, x0:x1] = g[y0:y1, x0:x1] < thr
    for _ in range(grow):
        p = np.pad(m, 1); m = p[1:-1, 1:-1] | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    return m


def vtext(im, box, t, fs, fill=(0, 0, 0), bg='white'):
    """竖排文字区（旋转 90° 的英文）：刷底色后写逆时针旋转 90° 的中文"""
    d = ImageDraw.Draw(im); d.rectangle(box, fill=bg); f = font(fs)
    w = int(d.textlength(t, font=f)) + 8; lay = Image.new('RGBA', (w, fs + 10), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((4, 2), t, font=f, fill=fill); lay = lay.rotate(90, expand=True)
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2; im.paste(lay, (cx - lay.width // 2, cy - lay.height // 2), lay)
    return im


def chart_style():
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    fm.fontManager.addfont(F); plt.rcParams['font.family'] = fm.FontProperties(fname=F).get_name()
    plt.rcParams['axes.unicode_minus'] = False
    return plt


def figsave(plt, fig, title, n):
    b = io.BytesIO(); fig.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
    save(titled(Image.open(b).convert('RGB'), title), n)


def ctable(title, hdr, cw, rows, n, fs=22):
    """编者整理的对照表卡片"""
    W = 1200; H = 64 + sum(max(para_h(t, fs, w - 24, gap=6) for t, w in zip(r, cw)) + 24 for r in rows)
    im = Image.new('RGB', (W, H + 20), 'white'); dr = ImageDraw.Draw(im); x = 20
    for t, w in zip(hdr, cw): dr.rectangle([x, 10, x + w, 64], fill=TEAL); dr.text((x + 12, 22), t, font=font(26), fill='white'); x += w
    y = 64
    for k, r in enumerate(rows):
        h = max(para_h(t, fs, w - 24, gap=6) for t, w in zip(r, cw)) + 24; x = 20
        for j, (t, w) in enumerate(zip(r, cw)):
            dr.rectangle([x, y, x + w, y + h], fill=LT if k % 2 else 'white', outline=(210, 210, 210))
            para(dr, x + 12, y + 12, t, fs, w - 24, fill=RED if j == 0 else INK, gap=6); x += w
        y += h
    save(titled(im.crop((0, 0, W, y + 14)), title), n)


# 首图：原题直译
title_card('综述 · Current Reviews in Musculoskeletal Medicine 2012',
           ['半月板修复术后的康复'],
           ['Rehabilitation following meniscal repair'],
           'John T. Cavanaugh, Sarah E. Killian',
           'Curr Rev Musculoskelet Med. 2012;5(1):46-58. doi:10.1007/s12178-011-9110-y',
           '美国纽约特种外科医院（HSS）运动康复与表现中心')

# 原文图 1：线稿里的英文标注换成中文
im = raw(64); d = ImageDraw.Draw(im)
# 字母所在的紧凑方框：刷白（框内没有线条），再写中文
for (x0, y0, x1, y1), t, fs in (((254, 27, 345, 42), '腓总神经', 15), ((112, 77, 189, 112), '股二头肌腱', 14),
                                ((230, 93, 350, 109), '腓肠肌', 14), ((251, 111, 329, 130), '（外侧头）', 13),
                                ((9, 280, 97, 299), '腘肌腱', 15), ((27, 353, 160, 369), '外侧副韧带', 15), ((60, 373, 129, 391), '', 14),
                                ((392, 101, 401, 112), '神', 9), ((419, 108, 429, 119), '静', 9), ((393, 123, 402, 134), '静', 9), ((398, 141, 407, 152), '动', 9)):
    d.rectangle([x0, y0, x1, y1], fill='white')
    if t: d.text(((x0 + x1) / 2, (y0 + y1) / 2), t, font=font(fs), fill='black', anchor='mm')
one(im, '原文图 1　由内向外缝合：在关节内把缝线穿过半月板，再在关节囊外打结。图为外侧半月板，后外侧放置挡板保护腓总神经；右上角椭圆里的“神、静、动”分别为神经、静脉、动脉（HSS 运动医学科提供）',
    '由内向外缝合（原文图 1）', 2)

one(raw(70), '原文图 2　由外向内缝合：在关节内把缝线（打 Mulberry 结）固定在撕裂的一侧，再在关节囊上打结；常用于中 1/3 和前角撕裂，可降低外侧修复时腓总神经损伤风险（HSS 运动医学科提供）',
    '由外向内缝合（原文图 2）', 3)

phases('半月板修复术后康复的原则（原文表 1）', [
    ('个体化：考虑伤前状态', LT, TEAL, [
        '同一诊断的病人表现各不相同；精英运动员、业余爱好者和体能差的非运动员要区别对待',
        '看下肢力线：内侧修复合并膝内翻、外侧修复合并膝外翻，受累间室压力更大，进度要更保守，可能推迟负重或用减荷支具']),
    ('懂基础科学、跟进临床研究', GR, (40, 120, 60), [
        '知道日常活动和每个练习在什么时候、怎样给半月板加压，了解炎症和组织愈合过程',
        '指南已越来越有科学依据，要跟进手术和康复技术的新进展']),
    ('团队协作：分工和沟通', OR, RED, [
        '外科医生把术式、修复部位和合并病变（如软骨退变、髌骨软化、ACL 缺失）告诉康复师，最好附手术记录',
        '一周 168 小时，病人在治疗师监督下只有约 3 小时（2%），其余 98% 靠自己，所以依从性至关重要']),
    ('康复三条规则（Gray）', PK, RED, [
        '1. 创造安全的环境：练习不能影响修复处愈合，如严格执行负重和活动度限制',
        '2. 不弄伤病人：练习无痛，也教病人别自己弄伤自己',
        '3. 在不违反前两条的前提下积极推进']),
    ('按功能顺序、按评估进阶', PU, TEAL, [
        '先学会简单的再做难的：直腿抬高无伸膝滞后→正常步态→上楼→下楼→跑步→敏捷、增强式和专项训练',
        '时间框架要灵活，如“第 4～6 周出现无痛步态即可弃拐”，而不是“第 6 周弃拐”；积液和疼痛增加说明进得太快']),
], 4)

ctable('各家术后方案差别很大（编者根据原文整理）', ['作者', '负重', '活动度 / 支具', '回到运动'], [200, 330, 380, 230], [
    ('Barber', '加速方案：早期负重', '早期活动度训练', '早期回到运动；愈合率与保守方案无差别'),
    ('Kocabey', '前后向纵裂 ≤3 cm：不限负重、不用支具；>3 cm：不限负重、支具锁定', '≤3 cm：3～6 周逐步到屈曲 125°；>3 cm：6～8 周解除 0～125° 限制', '纵裂 3 个月'),
    ('Kocabey', '复杂、放射状撕裂：初期限制负重', '初期限制活动度并戴支具；6～8 周完全负重、主动活动 0～125°', '4～5 个月'),
    ('Bryant 等', '前 3 周拄拐完全负重，支具锁定伸直', '3 周后可耐受负重、活动度不限', '结果与其他方案相近'),
    ("O'Shea 和 Shelbourne", '术后第 3 天开始负重', '活动度不限', '愈合率高'),
    ('Noyes 和 Barber-Westin', '按修复类型限制负重 4～6 周', '6 周内逐步到屈曲 135°', '76% 结果很好，87% 在 33 个月时无症状'),
    ('本文（HSS）', '纵裂、桶柄样撕裂：逐步到可耐受负重；放射状、复杂撕裂：足尖点地 4～6 周', '支具锁定伸直 4～6 周；屈曲限 90°，后角修复前 4 周限 70°', '4 个月开始跑步，第 14～22 周按标准回场')], 5)

phases('为什么要这样限制（编者根据原文整理）', [
    ('伸直负重：多数撕裂可以', LT, TEAL, [
        '负重时压力在半月板上转成环向应力（hoop stress），伸直位会把半月板“压回”关节囊，稳定纵向、桶柄样修复',
        '放射状撕裂贯穿整个横截面或后根撕裂时，环向应力会把撕裂两缘拉开，所以要推迟负重']),
    ('屈膝：越深压力越大', OR, RED, [
        '屈膝时半月板向后移，负重下从伸直屈到 90°，后角压力约增大 4 倍；屈膝 <60° 时半月板移动最小，所以早期可考虑限制在 60° 内',
        '屈膝前 30° 内胫骨旋转会让半月板大幅移动，深屈时股骨髁后移、压迫半月板：早期避免深蹲和胫骨旋转',
        '半膜肌附着于内侧半月板、腘肌附着于外侧半月板：早期避免主动或抗阻屈膝']),
    ('什么时候够结实', GR, (40, 120, 60), [
        '犬模型中修复处 12 周达最大抗拉强度的 80%；不少医生仍要求术后 4 个月以上才回到需要扭转的运动']),
], 6)

phases('第 1 阶段：术后 0～6 周，保护修复（原文表 2）', [
    ('目标', LT, TEAL, ['重点恢复完全被动伸直；控制术后疼痛肿胀；屈曲到 90°；恢复股四头肌控制；能独立完成家庭训练']),
    ('注意', OR, RED, [
        '避免主动屈膝；4 周前走路必须戴锁定在 0° 的支具；避免久站久走',
        '支具在前 4～6 周走路和睡觉时戴；后角修复前 4 周屈曲限 70°']),
    ('怎么练', GR, (40, 120, 60), [
        '毛巾伸膝、俯卧悬垂练伸直；股四头肌等长收缩（配合电刺激或肌电反馈）；髌骨松动',
        '拄拐、支具锁定 0° 下逐步负重到可耐受；复杂或放射状撕裂只能足尖点地',
        '辅助主动屈伸 90°→0°；各方向直腿抬高；髋渐进抗阻；双腿负重平衡板（能负重 50% 后开始）',
        '第 4～6 周：泳池行走或水下跑台（齐胸水深减重 60%～75%，齐腰 40%～50%）',
        '屈曲 >85° 后：短曲柄（90 mm）功率车、双腿腿举（60°→0°）、60° 位次最大强度股四头肌等长',
        '上肢有氧、腘绳肌和小腿牵伸、冷疗']),
    ('进入第 2 阶段的条件', PK, RED, ['直腿抬高无伸膝滞后；活动度 0～90°；患腿单腿负重不痛']),
], 7)

one(raw(118), '原文图 3　用 Kneehab 电刺激设备辅助股四头肌等长收缩（膝下垫毛巾卷）', '股四头肌再训练（原文图 3）', 8)
one(raw(117), '原文图 4　用 Biodex 平衡系统做动态稳定训练，屏幕实时反馈', '平衡训练（原文图 4）', 9)

phases('第 2 阶段：术后 6～14 周，恢复活动度和日常功能（原文表 2）', [
    ('目标', LT, TEAL, ['恢复全范围活动度和正常步态；能控制好下肢、不痛地上下 8 英寸（约 20 cm）台阶；提高日常活动耐力和下肢柔韧性']),
    ('注意', OR, RED, ['股四头肌控制和下肢力线不够好时，避免交替下楼；练习和日常活动都不应引起疼痛；避免跑步和运动']),
    ('怎么练', GR, (40, 120, 60), [
        '股四头肌控制好后，支具开到 0～60°、拄拐或手杖逐步负重；步态无痛不跛即弃拐；支具按医生要求换成减荷支具或髌骨护套',
        '负重直腿抬高、近端渐进抗阻；神经肌肉训练从双腿到单腿支撑：平衡仪、泡沫垫、外力扰动',
        '屈曲 110°～115° 后换标准功率车（170 mm）；屈曲 >120° 加股四头肌牵伸',
        '腿举从双腿到离心再到单腿（<90°）；扶瑞士球深蹲（0°～60°）；无痛、无摩擦音范围内的开链伸膝',
        '前向上台阶、下台阶，台阶从 4、6 英寸到 8 英寸；踏步机、椭圆机、倒走跑台（逐步加坡度）',
        '第 14 周做前向下台阶测试（NeuroCom）：从 8 英寸台阶慢慢下到测力台，冲击力常模为体重的 10%，两侧对称性 85%']),
    ('进入第 3 阶段的条件', PK, RED, ['活动度正常；能控制好下肢、不痛地下 8 英寸台阶']),
], 10)

one(raw(126), '原文图 5　从 8 英寸（约 20 cm）台阶前向下台阶，检验术侧股四头肌的控制', '前向下台阶（原文图 5）', 11)

phases('第 3 阶段：术后 14～22 周，回到运动（原文表 2）', [
    ('目标', LT, TEAL, ['跑步不痛；力量和柔韧性满足日常和运动需要；离院时能独立在健身房维持训练']),
    ('注意', OR, RED, ['练习和功能活动都不应引起疼痛；力量足够并经医生同意前不做运动']),
    ('怎么练', GR, (40, 120, 60), [
        '深蹲进阶到 <90°；弓步；术后 4 个月、活动度对称、股四头肌控制好且 8 英寸下台阶合格后，开始跑台向前跑，先短距离求速度',
        '倒跑；继续下肢力量和柔韧性训练；结合项目的敏捷训练（变速、减速、变向、冲刺），留意有没有恐惧动作',
        '力量基础足够后开始增强式训练，从双腿跳到跳箱；无痛、无摩擦音范围内等张屈伸膝；等速训练从快速到中速再到慢速']),
    ('回场标准', PK, RED, [
        '跑步和专项敏捷无症状；做专项动作不恐惧；柔韧性达到运动要求',
        '单腿跳和交叉跳的两侧对称性 >85%',
        '等速测试（180°/s 和 300°/s）股四头肌和腘绳肌平均峰力矩、总功的缺失 <15%',
        '结果交给手术医生，由医生最终决定能否回到运动']),
], 12)

# 封面：原文图 3、4、5 三张康复照片并排（股四头肌电刺激、平衡训练、下台阶），拼成 900×383
H = 383; ws = [300, 296, 296]; gap = 4
q = raw(118).crop((185, 0, 475, 372)); b = raw(117).crop((0, 205, 384, 701)); s = raw(126)
cv = Image.new('RGB', (900, H), 'white'); x = 0
for p, w in zip((q, b, s), ws):
    r = max(w / p.width, H / p.height); p = p.resize((round(p.width * r), round(p.height * r)), Image.LANCZOS)
    l = (p.width - w) // 2; t = (p.height - H) // 2; cv.paste(p.crop((l, t, l + w, t + H)), (x, 0)); x += w + gap
cv.save(f'{OUT}/cover.jpg', quality=90)
