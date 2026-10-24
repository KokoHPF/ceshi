#!/usr/bin/env python3
"""Chen 等 2026 经桡侧腕屈肌腱（trans-FCR）正中神经阻滞：首图中文标题卡、原文图 1（paper-figure-zh 译成中文）、
原文图 2（缩写保留，加中文对照）、三种进针法对比卡、操作要点卡、结果图、封面。
用法：python3 make_figs.py <work 目录> <输出目录> <字体>
work 目录需要：zh_p3_1.png（figtrans render 输出的原文图 1 中文版）、fig2.png（原文图 2，pdfimages 导出）"""
import sys
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

WORK, OUT, F = sys.argv[1], sys.argv[2], sys.argv[3]
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
dr.text((70, 50), '尸体解剖研究 · 《Journal of Hand Surgery Global Online》2026', font=font(32), fill=TEAL)
dr.text((70, 140), '经桡侧腕屈肌腱的体表触诊定位法', font=font(56), fill=INK)
dr.text((70, 215), '用于正中神经局部麻醉注射', font=font(56), fill=INK)
dr.line([70, 320, W - 70, 320], fill=(200, 205, 210), width=2)
dr.text((70, 350), 'Chen CJ, Sobol KR, Hickey CP, VanNest DS, Ibrahim JM, Raphael J.', font=font(26), fill=GREY)
dr.text((70, 395), 'J Hand Surg Glob Online. 2026;8:101034. doi:10.1016/j.jhsg.2026.101034', font=font(28), fill=GREY)
dr.text((70, 440), '美国托马斯·杰斐逊大学骨科、Hoag 骨科研究所', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(op('zh_p3_1.png'), '原文图 1  经 FCR 入路横断面示意：针从桡侧水平穿过桡侧腕屈肌腱（蓝色），到达正中神经旁；'
            '腕部横断面呈椭圆形，腕中立位时桡动脉偏向背侧，不在针道上（图中英文由编者译为中文）'), 2)
save(capbox(op('fig2.png'), '原文图 2  尸体解剖对照（掌侧观，上方为手掌，下方为近端）：A＝经 FCR 法；B＝第四指连线法（标准 1）；'
            'C＝腕横纹 1/3 宽度法（标准 2）。MN 正中神经；PCBMN 正中神经掌皮支；RA 桡动脉；L-FDS 中指指浅屈肌；'
            'FCR 桡侧腕屈肌腱；U 尺侧结构（尺动脉和尺神经）'), 3)

save(card(1200, '三种进针法：原文怎么比（编者整理）', [
    ('A  经 FCR 法（本文新方法）', '腕横纹近端约 4 cm，从桡侧横向进针，针与腕横纹平行、与床面平行，'
     '穿过桡侧腕屈肌腱和腱鞘，有“突破感”后即到正中神经旁', GR, (0, 120, 60)),
    ('B  标准 1：第四指连线法', '腕横纹近端 1 cm，与第四指（环指）同一纵线，针顺前臂纵轴、与水平面成 30°', OR, (200, 120, 0)),
    ('C  标准 2：1/3 腕宽法', '腕横纹近端 1 cm、腕横纹宽度的 1/3 处，针顺前臂纵轴、与水平面成 30°（原文没写从哪一侧量起）', PK, RED),
    ('共同条件', '14 个新鲜冷冻上肢标本，25G 针；前臂旋后、腕中立位；按针尖解剖到深层，'
     '2.5 倍放大镜下用卡尺量针尖到正中神经、桡动脉、正中神经掌皮支的距离，两人独立测量取平均', LT, TEAL),
]), 4)

save(card(1200, '经 FCR 法操作要点（编者根据原文整理）', [
    ('体位', '前臂旋后，掌侧朝上，腕关节中立位。不要尺偏：尺偏时正中神经会向桡侧移到 FCR 下方', LT, TEAL),
    ('找肌腱', '从腕横纹向近端摸桡侧腕屈肌腱，一直摸到前臂远端 1/3；腕部可借舟骨结节定位 FCR 远端', GR, (0, 120, 60)),
    ('进针', '腕横纹近端约 4 cm（正中神经在这里从中指指浅屈肌下方穿出、位置变浅），'
     '从桡侧横向进针，针与腕横纹平行、与床面平行', OR, (200, 120, 0)),
    ('深度', '针穿过 FCR 肌腱和腱鞘时有“突破感”即停；若推药时 FCR 腱鞘鼓起，说明太浅，再穿过腱鞘对侧壁', PK, RED),
    ('不适用', '不建议用于腕管内激素注射：针要穿过肌腱，激素有损伤胶原、导致肌腱断裂的理论风险。有超声时优先超声引导', (240, 240, 240), GREY),
]), 5)

# 结果图（原文表 2）
font_manager.fontManager.addfont(F); plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
fig, axs = plt.subplots(1, 2, figsize=(12, 5.8), dpi=100, gridspec_kw={'width_ratios': [1.6, 1]})
x = np.arange(3); w = .26; cols = ['#188080', '#E8A200', '#D9432F']
names = ['经 FCR 法', '标准 1', '标准 2']
data = {'经 FCR 法': ([3.5, 8.5, 3.8], [1.2, 3.5, 2.9]), '标准 1': ([5.2, 18.5, 10.7], [4.2, 5.5, 3.2]),
        '标准 2': ([3.0, 7.2, 2.1], [2.1, 4.2, 1.5])}
for i, n in enumerate(names):
    m, s = data[n]
    bars = axs[0].bar(x + (i - 1) * w, m, w, yerr=s, capsize=4, color=cols[i], label=n, error_kw={'ecolor': '#666', 'lw': 1})
    for r, v in zip(bars, m): axs[0].text(r.get_x() + r.get_width() / 2, .4, f'{v:g}', ha='center', fontsize=13, color='white', fontweight='bold')
axs[0].set_xticks(x, ['到正中神经', '到桡动脉', '到正中神经掌皮支']); axs[0].set_ylim(0, 27)
axs[0].set_title('针尖到关键结构的距离（mm，均数 ± 标准差）', fontsize=18, pad=12)
axs[0].legend(frameon=False, fontsize=14, loc='upper right')
pen_mn, pen_pc = [0, 4, 2], [0, 0, 2]
axs[1].bar(np.arange(3) - .18, pen_mn, .36, color='#16324F', label='刺入正中神经')
axs[1].bar(np.arange(3) + .18, pen_pc, .36, color='#9AA9B8', label='刺入掌皮支')
for i in range(3):
    axs[1].text(i - .18, pen_mn[i] + .1, pen_mn[i], ha='center', fontsize=15)
    axs[1].text(i + .18, pen_pc[i] + .1, pen_pc[i], ha='center', fontsize=15)
axs[1].set_xticks(range(3), names); axs[1].set_ylim(0, 7); axs[1].set_yticks(range(0, 6))
axs[1].set_title('刺入神经的标本数（/14）', fontsize=18, pad=12)
axs[1].legend(frameon=False, fontsize=13, loc='upper right')
axs[1].text(.3, 5.2, '三组比较\nP = 0.103', ha='center', fontsize=14, color='#D9432F')
for ax in axs: ax.tick_params(labelsize=14); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{WORK}/result.png', facecolor='white')
save(capbox(op('result.png'), '原文表 2 和结果部分重画。三种方法的距离差异 P 均 < 0.001；刺入神经的比例差异不显著（P = 0.103）。'
            '桡动脉三组都没有被刺入'), 6)

# 封面：原文图 1 中文版上半部分
c = op('zh_p3_1.png'); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS); y0 = 10
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
