#!/usr/bin/env python3
"""Kamalashiran 2024 急性缺血性卒中泰式按摩 23 步（MethodsX）：首图中文标题卡；方案总览卡；原文图 1～23 按部位分 4 板，
每格加中文“第几步 · 部位”标题（原图仅含数字与箭头）；Barthel 指数与 NIHSS 随时间变化图（按表 2、3）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 14
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233)
d = pymupdf.open(PDF)
XS = [18, 33, 35, 31, 47, 45, 61, 63, 78, 76, 74, 94, 90, 92, 106, 108, 125, 127, 129, 146, 148, 144, 155]
CAP = ['第 1 步　足底', '第 2 步　小腿后内侧', '第 2 步（续）　大腿内收肌', '第 3 步　踝前中点 + 趾缝',
       '第 4 步　小腿前外侧 + 大腿前外侧', '第 5 步　腓肠肌 → 跟腱', '第 6 步　腹股沟“风门”点', '第 7 步　下肢牵伸',
       '第 8 步　手掌 3 点', '第 9 步　前臂屈侧 2 线', '第 10 步　胸前 2 点', '第 11 步　手背指缝',
       '第 12 步　上臂后侧 → 前臂', '第 13 步　肱三头肌与大圆肌交点', '第 14 步　手与手指牵伸',
       '第 15 步　足底 + 小腿 + 大腿后侧', '第 16 步　小腿后侧 → 臀外缘', '第 17 步　竖脊肌 腰 → 颈',
       '第 18、19 步　菱形肌 + 上斜方肌', '第 20 步　胸锁乳突肌', '第 21 步　耳上颞肌', '第 22 步　腹部逆时针', '第 23 步　头部收尾']


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(38), fill='white')
    out.paste(im, (0, 90)); return out


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def board(idx, title, cols=2, TW=680, TH=520):
    rows = (len(idx) + cols - 1) // cols
    im = Image.new('RGB', (cols * (TW + 12) + 12, rows * (TH + 72) + 12), 'white'); dr = ImageDraw.Draw(im)
    for k, i in enumerate(idx):
        p = Image.open(BytesIO(d.extract_image(XS[i])['image'])).convert('RGB')
        s = min(TW / p.width, TH / p.height); p = p.resize((round(p.width * s), round(p.height * s)), Image.LANCZOS)
        x0 = 12 + (k % cols) * (TW + 12); y0 = 12 + (k // cols) * (TH + 72)
        dr.rounded_rectangle([x0, y0, x0 + TW, y0 + 56], 8, fill=LT)
        dr.text((x0 + 16, y0 + 10), CAP[i], font=font(30), fill=TEAL)
        dr.rectangle([x0, y0 + 60, x0 + TW, y0 + 62 + TH], outline=(230, 230, 230), width=2)
        im.paste(p, (x0 + (TW - p.width) // 2, y0 + 62 + (TH - p.height) // 2))
    return titled(im, title)


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '方法学论文 + 预试验 · 《MethodsX》2024', font=font(32), fill=TEAL)
for i, t in enumerate(['急性脑梗死早期：', '一套 23 步的泰式按摩']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '从足底到头顶 · 每天 60 分钟 · 配合常规康复', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Kamalashiran C 等，MethodsX 2024;13:102830', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 总览 ----------
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 300], 16, fill=LT)
dr.text((50, 40), '一天的安排（连续 5 天）', font=font(36), fill=TEAL)
for i, (a, b, c) in enumerate([('上午', '常规物理治疗 60 分钟', '两组都做，同一位治疗师'), ('下午', '泰式按摩 60 分钟', '仅按摩组，经培训的泰医按摩师'), ('全程', '标准内科治疗', '抗血栓、并发症预防')]):
    dr.text((60, 105 + i * 62), a, font=font(32), fill=INK); dr.text((180, 105 + i * 62), b, font=font(32), fill=RED if i == 1 else INK)
    dr.text((700, 110 + i * 62), c, font=font(26), fill=GREY)
dr.rounded_rectangle([20, 320, W - 20, H - 20], 16, fill=OR)
dr.text((50, 340), '23 步按摩的顺序', font=font(36), fill=(190, 100, 40))
seq = [('仰卧', '第 1～7 步', '患侧下肢：足底 → 小腿 → 大腿 → 风门点 → 下肢牵伸'),
       ('仰卧', '第 8～14 步', '患侧上肢：手掌 → 前臂 → 胸前 → 手背 → 上臂后侧 → 手指牵伸'),
       ('侧卧', '第 15～19 步', '下肢后侧 → 竖脊肌 → 菱形肌 → 上斜方肌'),
       ('仰卧', '第 20～23 步', '颈部 → 颞部 → 腹部 → 头部收尾')]
for i, (p_, s, t) in enumerate(seq):
    y = 410 + i * 130
    dr.rounded_rectangle([50, y, 190, y + 100], 12, fill=TEAL); ctext(dr, 120, y + 30, p_, font(34), 'white')
    dr.text((220, y + 8), s, font=font(34), fill=INK); dr.text((220, y + 56), t, font=font(28), fill=GREY)
dr.text((40, 935), '手法以拇指按压为主，沿“线”推进或在“点”上停留；点按通常 10～45 秒。第 15～19 步体位为编者按插图推断', font=font(22), fill=(150, 150, 150))
save(titled(im, '方案总览'), 2)

# ---------- 4 块图解 ----------
save(board(list(range(0, 8)), '原文图 1～8　下肢（第 1～7 步，仰卧，先做患侧）'), 3)
save(board(list(range(8, 15)), '原文图 9～15　上肢与胸前（第 8～14 步）'), 4)
save(board(list(range(15, 19)), '原文图 16～19　下肢后侧与背部（第 15～19 步）'), 5)
save(board(list(range(19, 23)), '原文图 20～23　颈、头与腹部（第 20～23 步）'), 6)

# ---------- 结果 ----------
days = ['基线', '第1天', '第2天', '第3天', '第4天', '第5天', '第6天', '第20天']
bi_a = [61.88, 64.38, 70.94, 73.13, 76.88, 79.06, 79.38, 88.44]; bi_b = [62.65, 67.06, 71.47, 75.00, 80.29, 82.06, 82.06, 86.76]
fig, axs = plt.subplots(1, 2, figsize=(14, 4.8), gridspec_kw={'width_ratios': [2.2, 1]})
x = range(8)
axs[0].plot(x, bi_a, '-o', color='#00788c', lw=3, label='按摩 + 物理治疗'); axs[0].plot(x, bi_b, '-s', color='#e9a07a', lw=3, label='仅物理治疗')
axs[0].set_xticks(list(x)); axs[0].set_xticklabels(days, fontsize=11); axs[0].set_ylim(50, 100); axs[0].set_title('Barthel 日常生活活动指数（越高越好）', fontsize=15)
axs[0].legend(frameon=False)
xs = range(3)
axs[1].plot(xs, [5.25, 2.63, 1.69], '-o', color='#00788c', lw=3); axs[1].plot(xs, [5.29, 3.65, 2.88], '-s', color='#e9a07a', lw=3)
axs[1].set_xticks(list(xs)); axs[1].set_xticklabels(['基线', '第6天', '第20天']); axs[1].set_ylim(0, 7); axs[1].set_title('NIHSS 卒中严重度（越低越好）', fontsize=15)
for ax in axs:
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.01, -0.04, '均值，按原文表 2、3 重绘。两组都明显改善，组间差异无统计学意义；两组均未出现不良反应', fontsize=11, color='#777')
plt.tight_layout()
b = BytesIO(); plt.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close()
save(titled(Image.open(b).convert('RGB'), '结果：20 天内的日常生活能力与卒中严重度', 1300), 7)

# ---------- 封面 ----------
c = Image.open(BytesIO(d.extract_image(74)['image'])).convert('RGB')
s = 900 / c.width; c = c.resize((900, round(c.height * s)), Image.LANCZOS); top = 120
c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
