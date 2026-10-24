#!/usr/bin/env python3
"""Singh 等 2014 髋关节腔注射要不要影像引导：首图中文标题卡、编者示意图、原文图 1～3（annotate.py 加中文标注，
见 annotate_spec.json）配中文图注、操作要点卡、结果图、封面。
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
dr.text((70, 50), '前瞻性研究 · 《The Open Orthopaedics Journal》2014', font=font(32), fill=TEAL)
dr.text((70, 150), '髋关节腔注射需要影像引导吗？', font=font(60), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 335), 'Singh J, Khan WS, Marwah S, Wells G, Tannous DK, Sharma HK.', font=font(26), fill=GREY)
dr.text((70, 380), 'Open Orthop J. 2014;8:114-117. doi:10.2174/1874325001408010114', font=font(28), fill=GREY)
dr.text((70, 425), '英国赫尔皇家医院、皇家国立骨科医院 等', font=font(26), fill=GREY)
dr.text((70, 520), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(op('schem.jpg'), '编者示意图  前方入路的体表标志：在股动脉与腹股沟韧带交点外侧 2.5～3.5 cm 进针，针向后内侧倾斜约 20°'), 2)
CAP = [
    ('fig1.zh.jpg', '原文图 1  体表标志：画出髂前上棘和股动脉（X，股动脉与腹股沟韧带交点），在其外侧 3 cm 标出进针点'),
    ('fig2.zh.jpg', '原文图 2  进针：在股动脉与腹股沟韧带交点外侧 3 cm 进针，针向后内侧倾斜 20°，直到触及骨面（照片中的红色十字为影像增强器的激光定位线）'),
    ('fig3.zh.jpg', '原文图 3  透视确认：注入造影剂后，造影剂在关节内弥散，说明针尖在关节腔内'),
]
for n, (f, c) in enumerate(CAP, start=3): save(capbox(op(f), c), n)

save(card(1200, '前方入路髋关节注射：原文怎么做（编者整理）', [
    ('体位与麻醉', '仰卧在可透视的手术床上，无菌操作；静脉镇静（芬太尼、咪达唑仑，必要时丙泊酚、面罩吸氧或笑气）', LT, TEAL),
    ('进针点', '摸到股动脉搏动，找到它与腹股沟韧带的交点，向外侧 2.5～3.5 cm（原文图示为 3 cm）', GR, (0, 120, 60)),
    ('进针', '22G 腰穿针，向后内侧倾斜约 20°，一直进到触及骨面', OR, (200, 120, 0)),
    ('确认与注药', '透视下注入造影剂（Omnipaque 250）：造影剂进入关节＝成功；针位不对或造影剂不进关节＝失败。药物：左布比卡因 2.5 mg/mL 10 mL＋甲泼尼龙 80 mg', PK, RED),
]), 6)

# 结果图
font_manager.fontManager.addfont(sys.argv[3]); plt.rcParams['font.family'] = font_manager.FontProperties(fname=sys.argv[3]).get_name()
fig, axs = plt.subplots(1, 2, figsize=(12, 5.8), dpi=100, gridspec_kw={'width_ratios': [1.5, 1]})
import numpy as np
x = np.arange(3); w = .36; c1, c2 = '#188080', '#E8A200'
a = axs[0].bar(x - w / 2, [67, 77.1, 57.7], w, color=c1, label='全部（100 髋）')
b = axs[0].bar(x + w / 2, [82.1, 87.9, 73.9], w, color=c2, label='BMI < 30（56 髋*）')
for r in list(a) + list(b): axs[0].text(r.get_x() + r.get_width() / 2, r.get_height() + 1.5, f'{r.get_height():g}%', ha='center', fontsize=15)
axs[0].set_xticks(x, ['总体', '主治医生', '住院医生']); axs[0].set_ylim(0, 118); axs[0].set_title('不用影像的注射成功率', fontsize=20, pad=12)
axs[0].legend(frameon=False, fontsize=15, loc='upper left', ncol=2)
axs[1].bar([0, 1], [28.45, 32.03], yerr=[5.21, 4.84], capsize=8, color=['#188080', '#D9432F'], width=.55, error_kw={'ecolor': '#555'})
for i, v in enumerate([28.45, 32.03]): axs[1].text(i + .3, v + .5, f'{v}', fontsize=16)
axs[1].set_xticks([0, 1], ['成功组', '失败组']); axs[1].set_ylim(0, 45); axs[1].set_title('患者 BMI（均数 ± 标准差）', fontsize=20, pad=12)
axs[1].text(.5, 41, 'P = 0.001', ha='center', fontsize=16, color='#D9432F')
for ax in axs: ax.tick_params(labelsize=16); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{WORK}/result.png', facecolor='white')
save(capbox(op('result.png'), '原文表 1 和结果部分重画：成功率按医生级别和患者 BMI 分组。*原文写 BMI < 30 的有“49 例（56%）”，按百分比推算应为 56 髋'), 7)

# 封面：原文图 3 透视
c = op('x23.jpg'); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS); y0 = 230
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
