#!/usr/bin/env python3
"""Biggs-Kinzer 等 2010 伸膝装置＋关节镜松解治疗关节纤维化：首图中文标题卡、围手术期康复流程卡、
原文图 1～6（annotate.py 加中文标注，见 annotate_spec.json）配中文图注、结果图（据原文表 2、表 3 重画）、封面。
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
dr.text((70, 50), '回顾性病例系列 · 《Sports Health》2010', font=font(32), fill=TEAL)
dr.text((70, 140), '用伸膝装置做围手术期康复，', font=font(54), fill=INK)
dr.text((70, 215), '配合关节镜清理治疗膝关节纤维化', font=font(54), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Biggs-Kinzer A, Murphy B, Shelbourne KD, Urch S.', font=font(26), fill=GREY)
dr.text((70, 405), 'Sports Health. 2010;2(5):417-423. doi:10.1177/1941738110379088', font=font(28), fill=GREY)
dr.text((70, 450), '美国印第安纳波利斯卫理公会医院 Shelbourne 膝关节中心', font=font(26), fill=GREY)
dr.text((70, 540), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, '围手术期康复：先伸直，再屈曲（编者根据原文整理）', [
    ('① 术前：把伸直练到“平台期”', '伸膝装置每次 10 分钟、每天 3～4 次，之后接着做：毛巾牵拉（10 秒 ×10 次）、垫高足跟（10 分钟）、俯卧悬腿（10 分钟，可加沙袋），都是每天 3～4 次；站立时把重心移到患腿、把膝锁直\n伸直不再进步了，说明剩下的受限来自瘢痕而不是软组织紧张，这时才手术', LT, TEAL),
    ('② 手术：关节镜瘢痕切除', '住院一晚，静脉酮咯酸镇痛抗炎；穿抗血栓袜，腿放在 0°～30° 的持续被动活动仪上抬高；冷敷加压装置预防关节积血', GR, (0, 120, 60)),
    ('③ 术后 5 天：卧床＋伸直', '除如厕外卧床 5 天，预防关节积血（积血会抑制股四头肌和腘绳肌）\n手术当天就开始：伸膝装置每次 10 分钟、每天 4 次，接毛巾牵拉、垫高足跟、直腿抬高', OR, (200, 120, 0)),
    ('④ 伸直对称后再练屈曲', '标准：伸直和健侧一样，并能主动抬起足跟（股四头肌收缩让足跟离床）\n然后才练屈膝：足跟滑动、靠墙滑动，目标是能坐在脚跟上或屈曲不再进步；一旦伸直丢失，立即停练屈曲，先把伸直找回来', PK, RED),
    ('⑤ 活动度最大化后再练力量', '低冲击训练：功率车、椭圆机、台阶机；单腿蹬腿；前提是活动度不丢', (240, 240, 248), (90, 70, 170)),
]), 2)

CAP = [
    ('fig1.zh.jpg', '原文图 1  伸膝装置：绑带分别绑在膝上和膝下，仰卧放松腘绳肌，转动摇柄给膝施加向下的压力、加大伸膝力矩；患者自己控制力度，属于低负荷、长时间牵拉。每次 10 分钟，每天 3～4 次'),
    ('fig2.zh.jpg', '原文图 2  毛巾牵拉：毛巾套住前脚掌，一手按住髌骨上方的大腿，另一手拉毛巾，使膝过伸、足跟离开床面。保持 10 秒，做 10 次，每天 3～4 次'),
    ('fig3.zh.jpg', '原文图 3  垫高足跟：足跟放在垫子上，膝后和大腿悬空，让膝在重力下伸直。每次 10 分钟，每天 3～4 次'),
    ('fig4.zh.jpg', '原文图 4  俯卧悬腿：俯卧，双膝以下悬在床沿外，让膝被动伸直；可在踝部加沙袋加大牵拉。每次 10 分钟，每天 3～4 次'),
    ('fig5.zh.jpg', '原文图 5  站立锁膝：全身重量放在患腿上，把膝锁到完全过伸'),
    ('fig6.zh.jpg', '原文图 6  主动抬足跟：仰卧伸膝，收缩股四头肌把足跟抬离床面。能做到并且伸直与健侧对称，才开始练屈膝'),
]
for n, (f, c) in enumerate(CAP, start=3): save(capbox(op(f), c), n)

# 结果图
font_manager.fontManager.addfont(sys.argv[3]); plt.rcParams['font.family'] = font_manager.FontProperties(fname=sys.argv[3]).get_name()
fig, axs = plt.subplots(1, 2, figsize=(12, 5.6), dpi=100, gridspec_kw={'width_ratios': [1.1, 1]})
cats = ['正常', '接近正常', '异常', '严重异常']; cols = ['#188080', '#7FB8A8', '#E8A200', '#D9432F']
before, after = [0, 7, 5, 21], [14, 12, 3, 4]
for i, (lab, v) in enumerate((('治疗前', before), ('治疗后', after))):
    left = 0
    for k, (c, x) in enumerate(zip(cols, v)):
        axs[0].barh(i, x, left=left, color=c, label=cats[k] if i == 0 else None)
        if x: axs[0].text(left + x / 2, i, str(x), ha='center', va='center', color='white', fontsize=16)
        left += x
axs[0].set_yticks([0, 1], ['治疗前', '治疗后']); axs[0].invert_yaxis(); axs[0].set_xlim(0, 33); axs[0].set_xlabel('人数（共 33 人）', fontsize=15)
axs[0].set_title('IKDC 活动度分级', fontsize=19, pad=34); axs[0].legend(frameon=False, ncol=4, fontsize=13, loc='lower center', bbox_to_anchor=(.5, 1.0))
m = [72.6, 68.8, 63.0, 45.8]; sd = [13.6, 20.6, 11.5, 8.3]
axs[1].bar(range(4), m, yerr=sd, capsize=7, color=cols, width=.6, error_kw={'ecolor': '#555'})
for i, v in enumerate(m): axs[1].text(i + .32, v + 1, f'{v}', fontsize=14)
axs[1].set_xticks(range(4), cats); axs[1].set_ylim(0, 100); axs[1].set_title('术后 IKDC 主观评分（按活动度分级）', fontsize=19, pad=12)
for a in axs: a.tick_params(labelsize=14); a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{WORK}/result.png', facecolor='white')
save(capbox(op('result.png'), '原文表 2、表 3 重画：左图为治疗前后 IKDC 活动度分级的人数；右图为不同活动度分级患者的术后 IKDC 主观评分（均数 ± 标准差），“正常”组显著高于其他组（P＝0.04）'), 9)

# 封面：原文图 1（伸膝装置）
c = op('x3.jpg'); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS); y0 = (c.height - 383) // 2
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
