#!/usr/bin/env python3
"""Luomajoki 等 2007 腰椎运动控制测试的信度：首图中文标题卡、10 项测试原图（A/B 并排，加“正确 / 不正确”中文标签）配中文图注、
信度结果图（据原文表 2 重画，代替原文图 10）、封面。
用法：python3 make_figs.py <work 目录> <输出目录> <字体>"""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

WORK, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
op = lambda n: Image.open(f'{WORK}/{n}').convert('RGB')
def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t


def card(W, title, blocks):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


FB = ImageFont.truetype(sys.argv[3].replace('Medium', 'Bold'), 30)


def pair(a, b, la, lb, H=560, gap=12):
    """两张原图等高并排，左上角加中文标签（la/lb: (文字, 颜色)）"""
    ims = [op(f'{x}.jpg') for x in (a, b)]; ims = [i.resize((round(i.width * H / i.height), H), Image.LANCZOS) for i in ims]
    out = Image.new('RGB', (ims[0].width + ims[1].width + gap, H), 'white'); x = 0
    for im, (t, c) in zip(ims, (la, lb)):
        out.paste(im, (x, 0)); d = ImageDraw.Draw(out); tw = d.textlength(t, font=FB)
        d.rounded_rectangle([x + 12, 12, x + 36 + tw, 62], 10, fill=c); d.text((x + 24, 17), t, font=FB, fill='white'); x += im.width + gap
    return out


OK, NG, NAV = (24, 128, 96), (210, 60, 45), (22, 50, 79)
# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '信度研究 · 《BMC Musculoskeletal Disorders》2007', font=font(32), fill=TEAL)
dr.text((70, 150), '腰椎运动控制测试的信度', font=font(62), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 335), 'Luomajoki H, Kool J, de Bruin ED, Airaksinen O.', font=font(26), fill=GREY)
dr.text((70, 380), 'BMC Musculoskelet Disord. 2007;8:90. doi:10.1186/1471-2474-8-90', font=font(28), fill=GREY)
dr.text((70, 425), '瑞士 Reinach 物理治疗诊所、芬兰库奥皮奥大学、苏黎世应用科学大学 等', font=font(26), fill=GREY)
dr.text((70, 520), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

T = [  # (A, B, 标签 A, 标签 B, 图注)
    ('x44', 'x45', ('A 正确', OK), ('B 不正确', NG), '原文图 1  “服务员鞠躬”（屈曲控制）：直立，屈髋前倾而腰不动。A 正确：腰椎不动，屈髋 50°～70°；B 不正确：腰不动时屈髋不到 50°，或腰椎出现屈曲'),
    ('x54', 'x55', ('A 正确', OK), ('B 不正确', NG), '原文图 2  坐位伸膝（屈曲控制）：坐直、保持腰椎前凸，伸膝时腰不动。A 正确：腰不动，伸膝到差 30°～50° 伸直属正常；B 不正确：腰椎随伸膝屈曲，患者自己察觉不到'),
    ('x52', 'x53', ('A 正确', OK), ('B 不正确', NG), '原文图 3  四点跪位向后摇（屈曲控制）：骨盆向后移、腰保持中立。A 正确：屈髋到 120° 腰不动；B 不正确：屈髋带动腰椎屈曲（患者通常察觉不到）'),
    ('x63', 'x64', ('A 正确', OK), ('B 不正确', NG), '原文图 4  站立骨盆后倾（伸展控制）：主动后倾骨盆（臀肌发力），胸椎保持中立。A 正确：腰椎向屈曲方向移动；B 不正确：骨盆倾不动，或腰向伸展方向动、臀肌不发力、用胸椎屈曲代偿'),
    ('x73', 'x74', ('A 正确', OK), ('B 不正确', NG), '原文图 6  四点跪位向前摇（伸展控制）：骨盆向前移。A 正确：腰椎不出现伸展；B 不正确：髋的运动带动腰椎伸展'),
    ('x61', 'x62', ('A 正确', OK), ('B 不正确', NG), '原文图 5  俯卧主动屈膝（伸展控制）：A 正确：屈膝至少 90°，腰和骨盆不伸展；B 不正确：屈膝时腰椎不能保持中立、向伸展方向动'),
    ('x71', 'x72', ('单腿站：一侧', NAV), ('单腿站：另一侧', NAV), '原文图 7  单腿站（旋转控制）：两脚间距为两侧大转子距离的 1/3，从双脚站到单腿站，用尺量肚脐向侧方移动的距离。正确：左右对称，相差不超过 2 cm；不正确：肚脐侧移超过 10 cm，或两侧相差超过 2 cm'),
    ('x90', 'x91', ('A 正确', OK), ('B 不正确', NG), '原文图 8  俯卧主动屈膝（旋转控制）：A 正确：屈膝至少 90°，腰和骨盆不旋转；B 不正确：屈膝时骨盆旋转'),
    ('x88', 'x89', ('A 正确', OK), ('B 不正确', NG), '原文图 9  屈膝仰卧位髋外展（旋转控制）：A 正确：主动外展一侧髋，骨盆和腰不旋转；B 不正确：肚脐侧移，骨盆旋转或倾斜'),
]
for n, (a, b, la, lb, c) in enumerate(T, start=2): save(capbox(pair(a, b, la, lb), c), n)

# 信度结果图（据原文表 2）
font_manager.fontManager.addfont(sys.argv[3]); plt.rcParams['font.family'] = font_manager.FontProperties(fname=sys.argv[3]).get_name()
names = ['服务员鞠躬', '坐位伸膝', '跪位向后摇', '骨盆后倾', '跪位向前摇', '俯卧屈膝（伸展）', '单腿站 右', '单腿站 左', '俯卧屈膝（旋转）', '仰卧髋外展']
inter = [0.62, 0.72, 0.57, 0.65, 0.68, 0.47, 0.43, 0.65, 0.58, 0.38]
intra = [0.88, 0.95, 0.72, 0.80, 0.51, 0.70, 0.67, 0.84, 0.78, 0.86]
grp = ['屈曲'] * 3 + ['伸展'] * 3 + ['旋转'] * 4
fig, ax = plt.subplots(figsize=(12, 9), dpi=100); y = np.arange(len(names))[::-1]
ax.barh(y + .2, inter, .38, color='#188080', label='测试者间（两组平均）'); ax.barh(y - .2, intra, .38, color='#E8A200', label='测试者内（两人平均）')
for yy, a, b in zip(y, inter, intra):
    ax.text(a + .01, yy + .2, f'{a:.2f}', va='center', fontsize=14); ax.text(b + .01, yy - .2, f'{b:.2f}', va='center', fontsize=14)
ax.set_yticks(y, [f'{g}｜{n}' for g, n in zip(grp, names)]); ax.set_xlim(0, 1.08)
for v, t in ((.4, '0.4'), (.6, '0.6'), (.8, '0.8')): ax.axvline(v, color='#999', ls='--', lw=1)
ax.text(.2, len(names) - .3, '一般', ha='center', fontsize=14, color='#777'); ax.text(.5, len(names) - .3, '中等', ha='center', fontsize=14, color='#777')
ax.text(.7, len(names) - .3, '较好', ha='center', fontsize=14, color='#777'); ax.text(.94, len(names) - .3, '很好', ha='center', fontsize=14, color='#777')
ax.set_ylim(-.8, len(names) + .1); ax.set_xlabel('Kappa 值', fontsize=16); ax.tick_params(labelsize=15)
ax.legend(frameon=False, fontsize=15, loc='upper center', bbox_to_anchor=(.45, 1.09), ncol=2); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{WORK}/kappa.png', facecolor='white')
save(capbox(op('kappa.png'), '原文表 2 重画（代替原文图 10）：10 项测试的测试者间和测试者内 Kappa 均值。虚线为 0.4、0.6、0.8 分界'), 11)

# 封面：服务员鞠躬、坐位伸膝的正确 / 不正确各一张，裁成等宽四联
cv = Image.new('RGB', (900, 383), 'white'); x = 0
for f, (t, c) in (('x44', ('正确', OK)), ('x45', ('不正确', NG)), ('x54', ('正确', OK)), ('x55', ('不正确', NG))):
    im = op(f + '.jpg'); im = im.resize((round(im.width * 383 / im.height), 383), Image.LANCZOS); l = (im.width - 219) // 2
    cv.paste(im.crop((l, 0, l + 219, 383)), (x, 0)); d = ImageDraw.Draw(cv); tw = d.textlength(t, font=FB)
    d.rounded_rectangle([x + 10, 10, x + 34 + tw, 58], 10, fill=c); d.text((x + 22, 14), t, font=FB, fill='white'); x += 227
cv.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
