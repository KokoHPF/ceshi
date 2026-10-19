#!/usr/bin/env python3
"""Sun 等 2024 慢性非特异性颈痛：运动 vs 运动 + 颈椎自我松动 vs 运动 + 颈胸自我松动：首图中文标题卡；三组方案卡、
深层颈屈肌训练卡、结果图为编者绘制；流程图按原文图 4 重绘为中文；原文图 1～3 加中文标注（压力表品牌、衣服标志已模糊）。
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
font = lambda s: ImageFont.truetype(F, s)
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
X = {1: 63, 2: 87, 3: 118}
# 以宽 700 为基准
BL = {1: [(555, 55, 690, 100)], 3: [(220, 118, 251, 156), (582, 136, 612, 166)]}


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def fig(n, W):
    im = Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB'); s = im.width / 700
    for b in BL.get(n, []):
        bb = tuple(int(v * s) for v in b)
        im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(10 * s)), bb[:2])
    return im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)


def tile(n, cap, W=1200):
    im = fig(n, W)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in f'图 {n}　{cap}':
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, ((W - im.width) // 2, hh + 8)); return t


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '随机对照试验 · 《科学报告》2024', font=font(32), fill=TEAL)
for i, t in enumerate(['慢性颈痛：练深层颈屈肌之外，', '再加颈胸椎自我松动']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '松动带 + 泡沫轴，6 周三组对比', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Sun X, Chai L, Huang Q, Zhou H, Liu H. Sci Rep 2024;14:5298', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 三组
W = 1400; im = Image.new('RGB', (W, 700), 'white'); dr = ImageDraw.Draw(im)
gs = [('运动组', (240, 240, 240), GREY, ['压力生物反馈下', '深层颈屈肌训练', '+', '俯卧 W、Y、T', '肩胛稳定训练']),
      ('运动 + 颈椎自我松动', LT, TEAL, ['同运动组', '+', '松动带颈椎后伸', '松动带颈椎旋转（左右）']),
      ('运动 + 颈胸自我松动', OR, RED, ['同“运动 + 颈椎自我松动”', '+', '泡沫轴胸椎伸展', '侧卧胸椎旋转', '跪姿“祈祷式”伸展'])]
for k, (t, c, tc, items) in enumerate(gs):
    x = 20 + k * 460
    dr.rounded_rectangle([x, 20, x + 440, 560], 16, fill=c)
    ctext(dr, x + 220, 44, t, font(32), tc)
    for i, it in enumerate(items): ctext(dr, x + 220, 140 + i * 70, it, font(30 if it != '+' else 40), INK if it != '+' else tc)
para(dr, 30, 590, '每组 10 人；每周 3 次、每次 40 分钟，共 6 周 18 次。第 1 次和第 10 次有人指导教会/进阶，其余自己练、有人在旁监督和口头提醒', 28, 1340, GREY)
save(titled(im, '三组怎么练'), 2)

# 深层颈屈肌 + 肩胛
W, H = 1400, 1000; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 470], 16, fill=LT)
dr.text((50, 36), '深层颈屈肌（压力生物反馈）', font=font(36), fill=TEAL)
for i, t in enumerate(['仰卧屈髋屈膝，气囊垫在颈后，充气到 20 毫米汞柱', '做“点头”式的颅颈屈曲：下巴往回收，不抬头、不用浅层颈屈肌',
                       '保持 20 秒、休息 10 秒；每次目标压力加 2 毫米汞柱，直到 30', '前 3 周每周 3 组，后 3 周每周 5 组']):
    para(dr, 60, 110 + i * 88, f'{i + 1}. ' + t, 30, 1290, INK, 8)
dr.rounded_rectangle([20, 500, W - 20, 980], 16, fill=GR)
dr.text((50, 516), '肩胛稳定（俯卧，头伸出床外）', font=font(36), fill=TEAL)
for i, (a, t) in enumerate([('W', '肩外展 90°、屈肘 90°，手臂慢慢上下'), ('Y', '肩上举约 130°、伸肘，手臂慢慢上下'), ('T', '肩外展 90°、伸肘，手臂慢慢上下')]):
    y = 600 + i * 100
    dr.ellipse([60, y, 140, y + 80], fill=TEAL); ctext(dr, 100, y + 14, a, font(44), 'white')
    dr.text((170, y + 20), t, font=font(32), fill=INK)
dr.text((60, 910), '前 3 周每个动作 2 组 × 15 次；后 3 周每组 30 次；每周 3 次', font=font(30), fill=RED)
save(titled(im, '三组共同的运动训练'), 3)

save(titled(tile(1, '运动组：A、B 压力生物反馈下深层颈屈肌训练；C 压力表初始校准（20 毫米汞柱）；D 肩胛稳定训练 W 字；E Y 字；F T 字'), '深层颈屈肌与肩胛稳定'), 4)
save(titled(tile(2, '颈椎自我松动：A、B 颈椎后伸——折叠的松动带横放在问题节段棘突上，双手向上拉；C 向右旋转；D 向左旋转——带子绕颈，旋转到末端时顺着小关节面方向轻拉加压，不引起疼痛'), '用松动带做颈椎自我松动'), 5)
save(titled(tile(3, '胸椎自我松动：A、B 侧卧，上方腿搭在泡沫轴上固定骨盆，双臂前伸后上方手臂画大圈，胸椎左右交替旋到最大；C 跪坐“祈祷式”，双手放在泡沫轴上向前伸，呼气时胸口往下沉；D 泡沫轴横放在上胸椎下，双臂上举向后仰，保持 5～10 秒后换下一节段（原文图注：A、B 旋转，C 屈曲，D 伸展）'), '用泡沫轴做胸椎自我松动'), 6)

# 流程图
W, H = 1400, 760; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
def box(x0, y0, x1, y1, t, fill=LT, fs=28):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill, outline=(170, 190, 200), width=2)
    lines = t.split('\n'); hh = len(lines) * (fs + 10)
    for i, l in enumerate(lines): ctext(dr, (x0 + x1) / 2, (y0 + y1) / 2 - hh / 2 + i * (fs + 10), l, font(fs))
def down(x, y0, y1):
    dr.line([x, y0, x, y1 - 14], fill=TEAL, width=5); dr.polygon([(x - 12, y1 - 18), (x + 12, y1 - 18), (x, y1)], fill=TEAL)
box(450, 20, 950, 100, '招募并评估 47 人'); box(980, 20, 1380, 160, '排除 17 人\n不符合纳入标准 11\n拒绝参加 6', PK, 26)
dr.line([950, 60, 980, 60], fill=TEAL, width=4)
down(700, 100, 190); box(450, 190, 950, 270, '随机分组 30 人')
dr.line([700, 270, 700, 310], fill=TEAL, width=5); dr.line([233, 310, 1167, 310], fill=TEAL, width=5)
for k, (t, c) in enumerate([('运动组', (240, 240, 240)), ('运动 + 颈椎自我松动', LT), ('运动 + 颈胸自我松动', OR)]):
    cx = 233 + k * 467
    down(cx, 310, 360); box(cx - 215, 360, cx + 215, 470, f'{t}\n10 人', c, 27)
    down(cx, 470, 540); box(cx - 215, 540, cx + 215, 630, '纳入分析 10 人', GR, 27)
para(dr, 40, 670, '注：无失访', 26, 1300, GREY)
save(titled(im, '受试者流程（按原文图 4 重绘）'), 7)

# 结果
fig_, axs = plt.subplots(1, 3, figsize=(13, 4.6), dpi=110)
cols = ['#888888', '#2f8fa0', '#c0504d']; names = ['运动', '运动+颈椎松动', '运动+颈胸松动']
data = [('颈痛（0～10）', [(5.70, 3.30), (5.70, 3.20), (5.80, 2.30)]),
        ('右侧屈活动度（°）', [(34.84, 38.57), (34.68, 41.31), (38.07, 46.11)]),
        ('右旋活动度（°）', [(50.58, 50.08), (49.03, 53.80), (49.23, 58.02)])]
for ax, (t, ds) in zip(axs, data):
    for (a, b), c, nm in zip(ds, cols, names): ax.plot([0, 1], [a, b], '-o', color=c, lw=3, ms=8, label=nm)
    ax.set_xticks([0, 1]); ax.set_xticklabels(['训练前', '6 周后'], fontsize=13); ax.set_title(t, fontsize=14); ax.set_xlim(-0.3, 1.3)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
axs[0].legend(fontsize=11, frameon=False, loc='upper right')
plt.tight_layout(); buf = BytesIO(); fig_.savefig(buf, format='png'); plt.close(fig_)
save(titled(Image.open(buf), '主要结果：加颈胸自我松动的一组痛得最少、转得最多', 1320), 8)

c = fig(3, 900); c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
