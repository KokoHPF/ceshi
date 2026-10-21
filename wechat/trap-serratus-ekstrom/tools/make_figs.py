#!/usr/bin/env python3
"""Ekstrom 等 2003 JOSPT 斜方肌和前锯肌训练动作的表面肌电分析：首图为原题直译标题卡；
原文图 1～10 直接用原图照片（照片内无英文），英文图注译成中文放在照片下方；
原文图 11、12 是肌电软件截图，图中英文（机构、测试、受试者、采样频率、通道名）擦掉后在原位置写中文，文件名 EX-Sc-120、EX-Shrug 保留；
肌电热图和选动作卡为编者根据原文表 1～4 整理。
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
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=90)


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


import io

# 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '研究报告 · J Orthop Sports Phys Ther 2003', font=font(32), fill=TEAL)
for i, t in enumerate(['斜方肌和前锯肌训练动作的', '表面肌电分析']):
    dr.text((70, 130 + i * 72), t, font=font(54), fill=INK)
dr.text((70, 300), 'Surface Electromyographic Analysis of Exercises for the', font=font(28), fill=GREY)
dr.text((70, 338), 'Trapezius and Serratus Anterior Muscles', font=font(28), fill=GREY)
dr.line([70, 420, W - 70, 420], fill=(200, 205, 210), width=2)
dr.text((70, 450), 'Ekstrom RA, Donatelli RA, Soderberg GL. J Orthop Sports Phys Ther.', font=font(30), fill=GREY)
dr.text((70, 494), '2003;33(5):247-258. doi:10.2519/jospt.2003.33.5.247', font=font(30), fill=GREY)
dr.text((70, 550), '美国南达科他大学物理治疗系 · Physiotherapy Associates · 西南密苏里州立大学', font=font(26), fill=GREY)
dr.text((70, 612), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1～10：照片取自原文，图注译成中文
F_ZH = {1: (76, '原文图 1　站立位单侧耸肩'), 2: (77, '原文图 2　俯卧位单侧划船'),
        3: (75, '原文图 3　俯卧位，手臂沿下斜方肌纤维方向举过头顶'), 4: (74, '原文图 4　俯卧位肩水平外展加外旋'),
        5: (86, '原文图 5　俯卧位，肩外展 90°、屈肘 90°、肘支撑在床上做肩外旋'), 6: (85, '原文图 6　站立位，肩胛平面外展到 120° 以上'),
        7: (84, '原文图 7　坐位对角线练习：屈肩、水平内收加外旋'), 8: (83, '原文图 8　站立位，肩胛平面外展在 80° 以下'),
        9: (91, '原文图 9　仰卧位双侧肩胛前伸，肩水平内收约 45°、屈肘约 45°'), 10: (92, '原文图 10　仰卧位单侧推举，肩屈 90°、伸肘，肩胛完全前伸')}


def row(nums, title, n):
    gap = 15; tw = (1200 - gap) // 2; tiles = []
    for k in nums:
        x, t = F_ZH[k]; ph = Image.open(io.BytesIO(doc.extract_image(x)['image'])).convert('RGB')
        ph = ph.resize((tw, round(ph.height * tw / ph.width)), Image.LANCZOS); tiles.append((ph, t))
    hh = max(ph.height for ph, _ in tiles); ch = max(para_h(t, 26, tw - 24, gap=8) for _, t in tiles)
    im = Image.new('RGB', (1200, hh + ch + 30), 'white'); dr = ImageDraw.Draw(im)
    for i, (ph, t) in enumerate(tiles):
        x = i * (tw + gap); im.paste(ph, (x, hh - ph.height))
        dr.rectangle([x, hh, x + tw, hh + ch + 20], fill=(232, 232, 232)); para(dr, x + 12, hh + 12, t, 26, tw - 24, gap=8)
    save(titled(im, title), n)


row((1, 3), '原文图 1、3　耸肩和俯卧上举（图注译成中文）', 2)
row((2, 4), '原文图 2、4　俯卧划船和水平外展（图注译成中文）', 3)
row((5, 8), '原文图 5、8　外展 90° 位外旋和低位外展（图注译成中文）', 4)
row((6, 7), '原文图 6、7　高位外展和对角线练习（图注译成中文）', 5)
row((9, 10), '原文图 9、10　两种肩胛前伸练习（图注译成中文）', 6)


# 原文图 11、12：软件截图里的英文擦掉后写中文（坐标为 3 倍渲染图的像素）
def emg_fig(pno, xref, labels):
    pg = doc[pno]; r = pg.get_image_rects(xref)[0]
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=r)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); d = ImageDraw.Draw(im)
    for (x0, y0, x1, y1), t in labels:
        d.rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4], fill='white')
        ls = t.split('\n'); f = font(30); lh = 40; top = (y0 + y1) / 2 - lh * len(ls) / 2
        for i, l in enumerate(ls): d.text((x0, top + i * lh + 4), l, font=f, fill=(20, 20, 20))
    return im


HDR = lambda y: [y, y + 55, y + 110]
y7, y8 = HDR(95), HDR(59)
f11 = emg_fig(7, 104, [((141, y7[0], 485, y7[0] + 22), '机构：南达科他大学物理治疗系'), ((141, y7[1], 485, y7[1] + 22), '测试：肌肉测试-53'),
                       ((141, y7[2], 485, y7[2] + 22), '受试者：'), ((806, y7[0], 1104, y7[0] + 22), '记录：EX-Sc-120'),
                       ((806, y7[1], 1104, y7[1] + 22), '练习：EX-Sc-120'), ((806, y7[2], 1104, y7[2] + 22), '采样频率：1000 Hz'),
                       ((88, 760, 305, 818), '8　2000 μV\n前锯肌')])
f12 = emg_fig(8, 108, [((143, y8[0], 488, y8[0] + 22), '机构：南达科他大学物理治疗系'), ((143, y8[1], 488, y8[1] + 22), '测试：肌肉测试-47'),
                       ((143, y8[2], 488, y8[2] + 22), '受试者：'), ((806, y8[0], 1089, y8[0] + 22), '记录：EX-Shrug'),
                       ((806, y8[1], 1089, y8[1] + 22), '练习：EX-Shrug'), ((806, y8[2], 1089, y8[2] + 22), '采样频率：1000 Hz'),
                       ((88, 722, 305, 788), '5　5000 μV\n上斜方肌')])
save(titled(capbox(f11, '肩胛平面外展 120° 以上时前锯肌的原始肌电记录，3 次收缩，量程 0～2000 μV（图中英文由编者译成中文，记录文件名保留）'),
            '原文图 11　前锯肌原始肌电（高位外展）'), 7)
save(titled(capbox(f12, '单侧耸肩时上斜方肌的原始肌电记录，3 次收缩，量程 0～5000 μV（图中英文由编者译成中文，记录文件名保留）'),
            '原文图 12　上斜方肌原始肌电（单侧耸肩）'), 8)

# 编者热图：表 1～4 合并
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
EX = ['1 单侧耸肩', '2 俯卧单侧划船', '3 俯卧过头上举', '4 俯卧水平外展+外旋', '5 外展 90° 位外旋', '6 肩胛平面外展 > 120°',
      '7 对角线练习', '8 肩胛平面外展 < 80°', '9 仰卧双侧肩胛前伸', '10 仰卧单侧推举']
MU = ['上斜方肌', '中斜方肌', '下斜方肌', '前锯肌']
V = [[119, 53, 21, 27], [63, 79, 45, 14], [79, 101, 97, 43], [66, 87, 74, 9], [20, 45, 79, 57],
     [79, 49, 61, 96], [66, 21, 39, 100], [72, 47, 50, 62], [7, 7, 5, 53], [7, 12, 11, 62]]
TOP = {(0, 0), (2, 1), (3, 1), (1, 1), (2, 2), (4, 2), (6, 3), (5, 3)}  # 与该肌肉最高值无显著差异的动作
fig, ax = plt.subplots(figsize=(10, 9), dpi=110)
ax.imshow(V, cmap='YlOrRd', vmin=0, vmax=110, aspect='auto')
for i, row_ in enumerate(V):
    for j, v in enumerate(row_):
        ax.text(j, i, v, ha='center', va='center', fontsize=17, color='white' if v >= 70 else '#222')
        if (i, j) in TOP: ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False, ec='#1f3a93', lw=3.5))
ax.set_xticks(range(4)); ax.set_xticklabels(MU, fontsize=16); ax.xaxis.tick_top()
ax.set_yticks(range(10)); ax.set_yticklabels(EX, fontsize=15); ax.tick_params(length=0)
ax.set_xlabel('数值为平均 %MVIC（n = 30，5RM 负荷）；蓝框：该肌肉激活最高、彼此无显著差异的动作', fontsize=12)
fig.tight_layout(); fig.savefig(f'{OUT}/_hm.png'); plt.close(fig)
import os
hm = Image.open(f'{OUT}/_hm.png').convert('RGB'); os.remove(f'{OUT}/_hm.png')
save(titled(hm, '10 个动作 × 4 块肩胛肌的肌电（编者根据原文表 1～4 整理）'), 9)

phases('按目标肌肉选动作（编者根据原文整理）', [
    ('上斜方肌', PK, RED, ['单侧耸肩 119% MVIC，显著高于其余所有动作', '想少用上斜方肌：外展 90° 位外旋只有 20%，两种肩胛前伸只有 7%']),
    ('中斜方肌', LT, TEAL, ['俯卧过头上举 101%、俯卧水平外展加外旋 87%、俯卧划船 79%，三者无显著差异', '作者结论只推荐前两个，但划船在统计上并不落后']),
    ('下斜方肌', GR, (40, 120, 60), ['俯卧过头上举 97% 最高', '肩不宜上举时：外展 90° 位外旋 79%，同时上斜方肌只有 20%，隔离效果最好']),
    ('前锯肌', PU, (90, 60, 150), ['对角线练习 100%、肩胛平面外展 > 120° 96%：都需要大量肩胛上回旋',
        '常用的前伸类动作（双侧前伸 53%、单侧推举 62%）明显更低', '外展 > 120° 时斜方肌三部分 49%～79%，是练“上回旋力偶”的好选择'])], 10)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), '肩胛稳定 · 表面肌电 · JOSPT', font=font(34), fill=TEAL)
dr.text((50, 128), '斜方肌和前锯肌', font=font(56), fill=INK)
dr.text((50, 214), '10 个动作怎么选？', font=font(56), fill=INK)
dr.text((50, 318), '耸肩 · 俯卧上举 · 外旋 · 高位外展 · 对角线', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
