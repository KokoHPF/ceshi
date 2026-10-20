#!/usr/bin/env python3
"""Rodríguez-Sanz 等 2021 慢性颈痛伴上颈椎旋转受限 RCT：首图为原题直译标题卡；研究设计卡为编者整理；
原文图 1、2 照片加中文说明（人脸已模糊）；屈曲旋转试验、疼痛、NDI 分级按原文表 2、表 3 数字重绘。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
doc = pymupdf.open(PDF)
raw = lambda x: Image.open(BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def arrow_down(dr, cx, y0, y1, c=TEAL):
    dr.line([cx, y0, cx, y1 - 14], fill=c, width=6)
    dr.polygon([(cx - 16, y1 - 18), (cx + 16, y1 - 18), (cx, y1)], fill=c)


def blur(im, boxes, r=14):
    s = im.width / 1000
    for b0 in boxes:
        b = tuple(int(v * s) for v in b0); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * s)), b[:2])
    return im


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * (len(tiles) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def pair(a, b, ca, cb, W=1200):
    """两张照片左右并排，各自上方加说明"""
    w = (W - 14) // 2
    ta, tb = capbox(a, ca, w), capbox(b, cb, w)
    h = max(ta.height, tb.height); out = Image.new('RGB', (W, h), 'white')
    out.paste(ta, (0, 0)); out.paste(tb, (w + 14, 0)); return out


# 照片：人脸模糊（坐标按 1000 宽）
F1 = blur(raw(26), [(45, 0, 95, 46), (52, 55, 95, 120), (335, 5, 405, 78), (322, 0, 362, 12), (565, 60, 650, 122), (895, 15, 968, 82), (935, 0, 985, 28)])
F2 = blur(raw(32), [(78, 35, 152, 132), (65, 0, 102, 22), (326, 35, 402, 132), (565, 0, 640, 12), (576, 35, 652, 132), (795, 0, 955, 92), (805, 92, 885, 152)])

# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '随机对照试验 · PeerJ 2021', font=font(32), fill=TEAL)
for i, t in enumerate(['有或无手法治疗的运动方案用于慢性颈痛伴', '上颈椎旋转受限患者的比较：随机对照试验']):
    dr.text((70, 130 + i * 72), t, font=font(50), fill=INK)
line, y = '', 300
for w in 'Comparison of an exercise program with and without manual therapy for patients with chronic neck pain and upper cervical rotation restriction. Randomized controlled trial'.split():
    if dr.textlength(line + ' ' + w, font=font(26)) > W - 140: dr.text((70, y), line, font=font(26), fill=GREY); y += 36; line = w
    else: line = (line + ' ' + w).strip()
dr.text((70, y), line, font=font(26), fill=GREY)
dr.line([70, 430, W - 70, 430], fill=(200, 205, 210), width=2)
dr.text((70, 460), 'Rodríguez-Sanz J, Malo-Urriés M, Lucha-López MO, et al. PeerJ 2021;9:e12546', font=font(30), fill=GREY)
dr.text((70, 515), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 研究设计卡（含 CONSORT 流程数字）
W = 1200; im = Image.new('RGB', (W, 880), 'white'); dr = ImageDraw.Draw(im)
def box(x0, y0, x1, y1, t, bg, fs=28, c=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=bg)
    lines = t.split('\n'); lh = fs + 10; y = (y0 + y1) / 2 - lh * len(lines) / 2
    for l in lines: ctext(dr, (x0 + x1) / 2, y, l, font(fs), c); y += lh
box(300, 20, 900, 120, '筛查 81 人 → 纳入 58 人\n慢性颈痛 > 3 个月 + 屈曲旋转试验阳性', (240, 240, 240))
arrow_down(dr, 600, 124, 170)
box(40, 180, 580, 420, '手法 + 运动组（29 人）\n每周 1 次 × 4 周，每次 20 分钟\n上颈椎手法（C0-1、C1-2、C2-3\n牵引式快速推）和/或 C0-1 松动\n+ 同样的运动 + 居家练习', LT, 26)
box(620, 180, 1160, 420, '单纯运动组（29 人）\n每周 1 次 × 4 周，每次 20 分钟\n颈深屈肌、颈深伸肌、\n颅颈屈曲、抗阻伸肌\n+ 居家练习（每天 2～5 次）', OR, 26)
for x, t in ((310, '实际复查：28 → 27 → 22 人'), (890, '实际复查：25 → 23 → 19 人')):
    ctext(dr, x, 440, t, font(26), RED)
box(40, 500, 1160, 640, '测量时间：治疗前（T0）、4 周治疗结束（T1）、3 个月（T2）、6 个月（T3）\n评估者不知道分组；患者、治疗师不设盲', (234, 230, 246), 26)
box(40, 670, 1160, 850, '主要指标：颈部功能障碍指数（NDI，按无 / 轻 / 中 / 重 / 完全分级）、屈曲旋转试验\n次要指标：疼痛（0～10）、压痛阈（斜方肌、肩胛提肌、C5-6 关节突）、颈椎主动活动度\n统计：线性混合模型，意向性分析（缺失值用期望最大化法填补，两组都按 29 人分析）', GR, 24)
save(titled(im, '研究怎么做的（编者根据原文整理）'), 2)

# 原文图 1 运动
save(titled(capbox(F1, 'A 颈深屈肌：仰卧轻轻点头，用压力生物反馈仪控制，每次保持 10 秒；B 颈深伸肌：四点跪位，下巴微收，保持下巴位置轻轻伸颈；C 颅颈屈曲：先点头收下巴，再把头抬离床面；D 抗阻伸肌：同 B，加弹力带阻力。每组 10 次 × 2 组，每次保持 10 秒'),
            '原文图 1　两组都做的 4 个颈部运动（人脸已模糊）'), 3)

# 原文图 2 手法
save(titled(capbox(F2, 'A/a C0-1 牵引式手法：仰卧、颈中立，一手托下巴，另一手食指桡侧放乳突下，向头侧快速推；B/b C1-2、C/c C2-3：手法相同，着力点移到寰椎、C3；D/d C0-1 向背侧松动：每次 5 分钟，45 秒松动 + 15 秒休息'),
            '原文图 2　手法组加做的上颈椎手法（人脸已模糊）'), 4)

# 结果：屈曲旋转试验 + 疼痛
T = ['治疗前', '4 周', '3 个月', '6 个月']
fig, axs = plt.subplots(1, 2, figsize=(13, 6.2), dpi=110)
ax = axs[0]
ax.plot(T, [21.26, 40.89, 37.76, 37.94], 'o-', color='#0b6e82', lw=3, label='手法 + 运动 右')
ax.plot(T, [23.12, 39.49, 38.81, 37.32], 's--', color='#0b6e82', lw=2, label='手法 + 运动 左')
ax.plot(T, [16.70, 18.56, 14.56, 14.56], 'o-', color='#d1495b', lw=3, label='单纯运动 右')
ax.plot(T, [19.01, 20.57, 15.17, 15.53], 's--', color='#d1495b', lw=2, label='单纯运动 左')
ax.axhline(32, color='#999', ls=':', lw=1.5); ax.text(3, 33, '32° 阳性线', ha='right', fontsize=12, color='#666')
ax.set_ylim(0, 50); ax.set_ylabel('屈曲旋转试验（°）', fontsize=15); ax.set_title('上颈椎旋转', fontsize=17)
ax.legend(fontsize=11, frameon=False, loc='lower left'); ax.tick_params(labelsize=13)
ax = axs[1]
ax.plot(T, [4.10, 0.70, 1.28, 1.17], 'o-', color='#0b6e82', lw=3, label='手法 + 运动')
ax.plot(T, [4.28, 3.46, 3.46, 3.91], 'o-', color='#d1495b', lw=3, label='单纯运动')
for y, c in (([4.10, 0.70, 1.28, 1.17], '#0b6e82'), ([4.28, 3.46, 3.46, 3.91], '#d1495b')):
    for i, v in enumerate(y): ax.text(i, v + (0.25 if c == '#d1495b' else -0.45), f'{v:.1f}', ha='center', fontsize=12, color=c)
ax.set_ylim(0, 6); ax.set_ylabel('疼痛强度（0～10）', fontsize=15); ax.set_title('疼痛', fontsize=17)
ax.legend(fontsize=12, frameon=False); ax.tick_params(labelsize=13)
for a in axs: a.spines[['top', 'right']].set_visible(False)
fig.text(0.5, 0.01, '数值为原文表 3 均值；6 个月时两组实际复查分别只有 22 人和 19 人，其余为填补值', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.04, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '结果：手法组旋转明显变大、疼痛明显下降，运动组几乎没变', 1200), 5)

# 结果：NDI 分级堆叠条
cats = ['无', '轻度', '中度', '重度']
cols = ['#5aa469', '#a7c957', '#f39a2b', '#c0392b']
data = {'手法 + 运动': [[3, 17, 8, 1], [16, 13, 0, 0], [19, 10, 0, 0], [20, 9, 0, 0]],
        '单纯运动': [[0, 16, 10, 3], [3, 19, 5, 2], [4, 16, 5, 4], [4, 16, 4, 5]]}
fig, axs = plt.subplots(1, 2, figsize=(13, 6), dpi=110, sharey=True)
for ax, (g, rows) in zip(axs, data.items()):
    left = [0] * 4
    for k in range(4):
        vals = [r[k] for r in rows]
        ax.barh(T[::-1], vals[::-1], left=left[::-1], color=cols[k], label=cats[k])
        for i, v in enumerate(vals[::-1]):
            if v >= 2: ax.text(left[::-1][i] + v / 2, i, str(v), ha='center', va='center', fontsize=12, color='white')
        left = [l + v for l, v in zip(left, vals)]
    ax.set_title(g, fontsize=17); ax.set_xlim(0, 29); ax.set_xlabel('人数（共 29 人）', fontsize=13); ax.tick_params(labelsize=13)
    ax.spines[['top', 'right']].set_visible(False)
fig.legend(*axs[0].get_legend_handles_labels(), fontsize=13, frameon=False, loc='upper center', ncol=4, title='功能障碍分级', bbox_to_anchor=(0.5, 1.0))
fig.text(0.5, 0.01, '按原文表 2 重绘；“完全障碍”两组各时间点均为 0 人；6 个月中度以上：手法组 0%，运动组 31%', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.04, 1, 0.88)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '颈部功能障碍指数（NDI）分级变化', 1200), 6)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), '随机对照试验 · 慢性颈痛', font=font(40), fill=TEAL)
dr.text((50, 130), '上颈椎转不动，', font=font(64), fill=INK)
dr.text((50, 220), '光练够不够？', font=font(64), fill=INK)
dr.text((50, 318), '运动 vs 运动 + 上颈椎手法 · 随访 6 个月', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
