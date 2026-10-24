#!/usr/bin/env python3
"""Chernchujit 等 2019 膝关节腔注射：改良前外侧入路 vs 标准髌上外侧入路。首图中文标题卡、编者示意图、
原文图 1～4（annotate.py 加中文标注，见 annotate_spec.json）配中文图注、两种入路对比卡、结果图、封面。
用法：python3 make_figs.py <work 目录> <输出目录> <字体>"""
import sys
from PIL import Image, ImageDraw, ImageFont
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


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '临床对照研究 · 《AP-SMART》2019', font=font(32), fill=TEAL)
dr.text((70, 140), '无积液的症状性膝骨关节炎关节腔注射：', font=font(54), fill=INK)
dr.text((70, 215), '改良前外侧入路与髌上外侧入路准确率比较', font=font(54), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Chernchujit B, Tharakulphan S, Apivatgaroon A, Prasetia R.', font=font(26), fill=GREY)
dr.text((70, 405), 'Asia Pac J Sports Med Arthrosc Rehabil Technol. 2019;17:1-4', font=font(28), fill=GREY)
dr.text((70, 450), '泰国国立法政大学医学院骨科 等', font=font(26), fill=GREY)
dr.text((70, 540), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(op('schem.jpg'), '编者示意图  改良前外侧入路的进针点：髌骨下缘水平线与 Gerdy 结节垂线的交点（屈膝 90°）'), 2)
CAP = [
    ('fig1.zh.jpg', '原文图 1  改良前外侧入路（右膝）：仰卧或坐位，屈膝 90°；进针点为髌骨下缘水平线与 Gerdy 结节垂线的交点。先注入 10 mL 空气，看到回流（backflow）再注药'),
    ('fig2.zh.jpg', '原文图 2  标准髌上外侧入路（左膝）：仰卧伸膝，进针点为髌骨上缘水平线与髌骨外侧缘纵线的交点，针与股骨前方皮质平行'),
]
for n, (f, c) in enumerate(CAP, start=3): save(capbox(op(f), c), n)

save(card(1200, '两种入路怎么打（编者根据原文整理）', [
    ('通用', '严格无菌，聚维酮碘消毒；两组都用 25G 针、一根针两支注射器：先注 10 mL 空气，看到回流确认针尖在关节内，再换注射器注药；没有回流就再注 10 mL 空气。注药后能听到明显的“咕叽”声', LT, TEAL),
    ('改良前外侧入路（MAL）', '体位：仰卧或坐位，屈膝 90°\n进针点：髌骨下缘水平线 × Gerdy 结节垂线\n方向：与胫骨后倾平行（原文约 10°），针尖朝外侧胫骨平台，不朝髁间窝（避开脂肪垫、黏膜韧带、交叉韧带）\n终点：轻触股骨外侧髁软骨后退 1 mm——有“止点”可确认深度', GR, (0, 120, 60)),
    ('标准髌上外侧入路（SL）', '体位：仰卧，伸膝\n进针点：髌骨上缘水平线 × 髌骨外侧缘纵线\n方向：与股骨前方皮质平行，进入髌上囊', OR, (200, 120, 0)),
]), 5)

save(capbox(op('fig3.zh.jpg'), '原文图 3  注射不准（关节外）：注射后正、侧位片，空气分布在关节外的软组织中（箭头）'), 6)
save(capbox(op('fig4.zh.jpg'), '原文图 4  注射准确（关节内）：注射后正、侧位片，空气位于髌上囊内（白箭头）'), 7)

# 结果图
font_manager.fontManager.addfont(sys.argv[3]); plt.rcParams['font.family'] = font_manager.FontProperties(fname=sys.argv[3]).get_name()
fig, axs = plt.subplots(1, 2, figsize=(12, 5.6), dpi=100, gridspec_kw={'width_ratios': [1.15, 1]})
c = ['#188080', '#C87800']; g = ['改良前外侧', '标准髌上外侧']
b = axs[0].bar(g, [89, 58], color=c, width=.55); axs[0].set_ylim(0, 100); axs[0].set_title('注射准确率（%）', fontsize=20, pad=12)
for r, v in zip(b, ['89%（约 59/66）', '58%（约 38/66）']): axs[0].text(r.get_x() + r.get_width() / 2, r.get_height() + 2, v, ha='center', fontsize=17)
axs[0].text(.5, 96, 'P < 0.05', ha='center', fontsize=16, color='#D9432F')
axs[1].bar(g, [2.61, 2.65], yerr=[2.21, 2.76], capsize=8, color=c, width=.55, error_kw={'ecolor': '#555'}); axs[1].set_ylim(0, 10)
axs[1].set_title('注射疼痛 VAS（均数 ± 标准差）', fontsize=20, pad=12)
for x, v in enumerate([2.61, 2.65]): axs[1].text(x + .3, v + .2, f'{v}', fontsize=17)
axs[1].text(.5, 8.8, 'P = 0.917', ha='center', fontsize=16, color='#555')
for a in axs: a.tick_params(labelsize=16); a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{WORK}/result.png', facecolor='white')
save(capbox(op('result.png'), '原文表 1 重画：两种入路的准确率和注射疼痛（每组 66 膝；例数为编者按百分比推算）'), 8)

# 封面：原文图 1
c = op('x24.jpg').crop((20, 20, 996, 835)); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
y0 = 30; c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
