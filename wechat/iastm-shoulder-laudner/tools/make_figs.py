#!/usr/bin/env python3
"""器械辅助软组织松动对肩后侧活动度的即时影响（Laudner 2014）推文配图
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


from PIL import ImageOps


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


def photo(x):
    """原文照片在 PDF 里以反相灰度存储（显示时再反转），这里还原成正常的黑白照片"""
    return ImageOps.invert(raw(x).convert('L')).convert('RGB')


# 首图：原题直译
title_card('原创研究 · International Journal of Sports Physical Therapy 2014',
           ['器械辅助软组织松动改善大学棒球运动员', '肩后侧活动度的即时效果'],
           ['Acute effects of instrument assisted soft tissue mobilization for improving',
            'posterior shoulder range of motion in collegiate baseball players'],
           'Kevin Laudner, Bryce D. Compton, Todd A. McLoda, Chris M. Walters',
           'Int J Sports Phys Ther. 2014;9(1):1-7. PMID: 24567849',
           '美国伊利诺伊州立大学等')

phases('研究怎么做的（编者根据原文整理）', [
    ('谁参加', LT, TEAL, [
        '35 名 NCAA 一级联赛大学棒球运动员，近 6 个月投掷臂无上肢伤病、从未做过手术',
        '不要求有活动度受限；随机分成器械松动组 17 人、对照组 18 人']),
    ('测什么', GR, (40, 120, 60), [
        '仰卧，优势臂（投掷臂）被动水平内收和被动内旋，用数字倾角仪测量',
        '一人摆位并固定肩胛骨，另一人读数；每个方向前后测各量一次']),
    ('怎么干预', OR, RED, [
        '前测后，测量者离开房间，第三位研究者（认证运动防护师，受过 Graston 培训）施术',
        '俯卧、肩外展 90°、屈肘 90°，涂润滑剂，用 Graston GT-4 器械以 45° 角处理肩后腋缘肌群（三角肌后束、背阔肌、大圆肌、小圆肌、冈下肌）',
        '先顺肌纤维方向约 20 秒，再垂直肌纤维方向约 20 秒，合计约 40 秒',
        '对照组同样俯卧相同时间，不做任何处理；受试者穿回上衣遮住皮肤发红，测量者回来做后测，前后测相隔约 90 秒']),
    ('怎么分析', PU, TEAL, ['2（组别）×2（时间）混合方差分析；水平内收的方差不齐，作者把显著性门槛收紧为 P < 0.025']),
], 2)

one(photo(8), '原文图 1　测量盂肱关节被动水平内收：一人固定肩胛骨外侧缘并把手臂水平内收到第一个阻力点，另一人把倾角仪贴在肱骨前侧读角度（相对于与床面垂直的线）',
    '水平内收怎么测（原文图 1）', 3)
one(photo(12), '原文图 2　测量盂肱关节被动内旋：肩外展 90°、屈肘 90°，肱骨下垫毛巾与肩峰齐平，一手压住肩峰固定肩胛骨，被动内旋到终末，倾角仪贴前臂尺骨读数',
    '内旋怎么测（原文图 2）', 4)
tiles([(photo(13), '原文图 3　顺着肩后侧肌纤维方向刮，器械约 45°，约 20 秒'),
       (photo(14), '原文图 4　垂直于肩后侧肌纤维方向刮，器械约 45°，约 20 秒')],
      '40 秒的器械松动（原文图 3、4）', 5)

ctable('两组基本情况（原文表 1）', ['组别', '年龄（岁）', '身高（cm）', '体重（kg）'], [320, 260, 280, 300], [
    ('器械松动组（17 人）', '20.1 ± 1.2', '189.3 ± 11.2', '94.1 ± 22.2'),
    ('对照组（18 人）', '20.3 ± 1.1', '185.7 ± 5.3', '85.4 ± 21.2')], 6, fs=24)

plt = chart_style()
fig, axs = plt.subplots(1, 2, figsize=(11, 4.8))
for ax, (nm, iv, ct) in zip(axs, (('被动水平内收（°）', (-10.9, 0.2), (-10.4, -10.6)), ('被动内旋（°）', (42.4, 47.2), (41.6, 41.5)))):
    ax.plot(['前测', '后测'], iv, 'o-', color='#00788c', lw=3, ms=9, label='器械松动组')
    ax.plot(['前测', '后测'], ct, 's--', color='#9a9a9a', lw=3, ms=9, label='对照组')
    for y, o, c in ((iv, ct, '#00788c'), (ct, iv, '#666666')):
        for k, v in enumerate(y): ax.annotate(f'{v}', (k, v), textcoords='offset points', xytext=(-40 if k == 0 else 12, 8 if v >= o[k] else -18), color=c, fontsize=12)
    lo, hi = min(iv + ct), max(iv + ct); ax.set_ylim(lo - 1.5, hi + 1)
    ax.set_title(nm, fontsize=15); ax.grid(axis='y', alpha=.3); ax.spines[['top', 'right']].set_visible(False); ax.set_xlim(-.4, 1.4)
axs[0].legend(frameon=False, fontsize=12, loc='center right')
axs[0].text(0.5, -0.17, '水平内收为负值：上臂还没到与床面垂直的位置', transform=axs[0].transAxes, ha='center', fontsize=11, color='#666')
figsave(plt, fig, '前后测均值：40 秒后两个方向都变大（原文表 2、3）', 7)

ctable('主要结果（原文表 2、3，单位：度）', ['指标与组别', '前测', '后测', '变化', '组×时间交互'], [300, 200, 200, 170, 290], [
    ('水平内收　器械松动组', '-10.9 ± 5.8', '0.2 ± 6.3', '+11.1', 'P < 0.001；F = 77.4；偏 η² = 0.7'),
    ('水平内收　对照组', '-10.4 ± 4.2', '-10.6 ± 4.4', '-0.12', ''),
    ('内旋　器械松动组', '42.4 ± 10.8', '47.2 ± 9.2', '+4.8', 'P < 0.001；F = 12.7；偏 η² = 0.3'),
    ('内旋　对照组', '41.6 ± 8.0', '41.5 ± 9.1', '-0.14', '')], 8)

# 编者计算：测量误差门槛
fig, ax = plt.subplots(figsize=(10, 4.6))
lab = ['水平内收', '内旋']; ch = [11.1, 4.8]; sem = [1.6, 2.0]; mdc = [round(s * 1.96 * 2 ** .5, 1) for s in sem]
y = [1, 0]
ax.barh(y, ch, height=.45, color='#00788c')
for k in range(2):
    ax.plot([sem[k]] * 2, [y[k] - .32, y[k] + .32], color='#9a9a9a', lw=3)
    ax.plot([mdc[k]] * 2, [y[k] - .32, y[k] + .32], color='#be2832', lw=3)
    ax.text(max(ch[k], mdc[k]) + .3, y[k], f'平均改善 {ch[k]}°', va='center', fontsize=13)
    ax.text(mdc[k], y[k] + .38, f'MDC95 ≈ {mdc[k]}°', color='#be2832', fontsize=12, ha='center')
    ax.text(sem[k], y[k] - .45, f'SEM {sem[k]}°', color='#666', fontsize=12, ha='center')
ax.set_yticks(y); ax.set_yticklabels(lab, fontsize=14); ax.set_xlim(0, 14); ax.set_ylim(-.7, 1.6)
ax.set_xlabel('度', fontsize=12); ax.spines[['top', 'right']].set_visible(False)
figsave(plt, fig, '超过测量误差了吗？（编者按 MDC95 = 1.96 × √2 × SEM 计算）', 9)

ctable('和其他一次性干预比（编者根据原文讨论整理）', ['干预（一次）', '水平内收增加', '内旋增加', '备注'], [400, 200, 170, 390], [
    ('器械松动 40 秒（本研究）', '11.1°', '4.8°', '无症状大学棒球运动员'),
    ('睡姿牵伸 3×30 秒（Laudner 等）', '2.3°', '3.1°', '同一团队早期研究'),
    ('肌肉能量技术 3 次（Moore 等）', '6.8°', '4.2°', '针对盂肱水平外展肌群，有对照组')], 10)

phases('这些结论能信几分（编者评价）', [
    ('站得住的', GR, (40, 120, 60), [
        '随机分组，有不干预对照；测量者在施术时离开房间、受试者穿回上衣遮红印，测量端做了盲法',
        '测量者信度事先检验过（ICC 0.93 和 0.98）；水平内收的改善远大于测量误差']),
    ('要打折扣的', OR, RED, [
        '只有 35 名无症状运动员，结果不能直接套到有肩痛或明显后侧紧张的病人身上',
        '只看了干预后约 90 秒，效果能维持多久完全未知',
        '对照组只是躺着，没有假刮或徒手按摩，受试者知道自己被处理过，安慰和期待效应无法排除',
        '内旋 4.8° 的改善低于编者算出的最小可检测变化（约 5.5°），作者“超过 SEM 即有临床意义”的说法偏乐观',
        '没有报告随机化方法、刮痧次数和力度，也没有活动度以外的功能或投球指标']),
], 11)

phases('落到临床（编者建议）', [
    ('什么时候可以试', LT, TEAL, [
        '投掷类运动员出现肩后侧紧张（水平内收、内旋受限），想在训练前快速“松一松”时，器械松动可作为选项之一',
        '本研究方案很短：俯卧、肩外展 90°、屈肘 90°，沿肩后腋缘顺纤维、横纤维各约 20 秒']),
    ('怎么用更稳妥', GR, (40, 120, 60), [
        '处理前后都用同一方法量水平内收和内旋，变化小于约 4～5° 时别急着下结论',
        '即时增加的活动度要用牵伸（如睡姿牵伸、水平内收牵伸）和后侧肩袖、肩胛力量训练去巩固',
        '注意皮肤反应，刮后发红在本研究中常见']),
    ('别过度期待', OR, RED, [
        '没有证据显示它能减少肩伤或提高投球表现，也不清楚效果持续多久',
        '需要多次治疗、有症状人群、带安慰对照的研究来回答']),
], 12)

# 封面：原文图 3（顺纤维方向器械松动），无文字
cover_from(photo(13), 0.5, 0.55)
