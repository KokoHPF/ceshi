#!/usr/bin/env python3
"""Abdo 2025 髌股痛在髋膝训练上加手法治疗（Scientific Reports 随机对照试验）：首图中文标题卡；方案总览卡、剂量卡；
原文图 1～10 动作照片按类别拼板并加中文标注；图 11 流程中文重绘；疼痛与 Kujala 结果图（按表 2、3）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
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
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); GY = (242, 242, 242)
CA, CB = '#9fb4bb', '#00788c'
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(38), fill='white')
    out.paste(im, (0, 90)); return out


def xim(x, w=None):
    im = Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')
    if w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    return im


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def tag(dr, x, y, t, fs=30):
    w = dr.textlength(t, font=font(fs))
    dr.rounded_rectangle([x, y, x + w + 24, y + fs + 18], 9, fill=(255, 255, 255), outline=TEAL, width=2)
    dr.text((x + 12, y + 7), t, font=font(fs), fill=TEAL)


def tagged(x, w, tags, fs=30):
    """tags: [(相对 x, 相对 y, 文字)]"""
    im = xim(x, w); dr = ImageDraw.Draw(im)
    for rx, ry, t in tags: tag(dr, int(rx * im.width) + 12, int(ry * im.height) + 12, t, fs)
    return im


def stack(ims, gap=16):
    W = max(i.width for i in ims); H = sum(i.height for i in ims) + gap * (len(ims) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for i in ims: out.paste(i, ((W - i.width) // 2, y)); y += i.height + gap
    return out


def bx(dr, x0, y0, x1, y1, lines, fill, fs=30, col=INK):
    dr.rounded_rectangle([x0, y0, x1, y1], 12, fill=fill, outline=(120, 150, 170), width=2)
    yy = (y0 + y1 - len(lines) * (fs + 10)) / 2 + 2
    for l in lines: ctext(dr, (x0 + x1) / 2, yy, l, font(fs), col); yy += fs + 10


def down(dr, x, y0, y1):
    dr.line([x, y0, x, y1 - 14], fill=TEAL, width=4); dr.polygon([(x - 12, y1 - 16), (x + 12, y1 - 16), (x, y1)], fill=TEAL)


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '双盲随机对照试验 · 《科学报告》（Scientific Reports）2025', font=font(32), fill=TEAL)
for i, t in enumerate(['髌股痛：髋膝训练之外，', '再加 3 个手法值不值？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '髌骨内推 · 髂胫束松解 · 外侧支持带深横摩擦 + 11 个训练动作', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Abdo N, Youssef EF, Ibrahim MM. Sci Rep 2025;15:32655', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 方案总览 ----------
W, H = 1400, 900; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([20, 20, W - 20, 120], 14, fill=TEAL)
ctext(dr, W / 2, 42, '每周 3 次 × 4 周 = 12 次 · 每次 45～60 分钟 · 门诊监督', font(36), 'white')
cols = [('牵伸（4 个）', ['小腿三头肌', '腘绳肌', '股四头肌', '髂胫束', '各 30 秒 × 3 次'], LT),
        ('闭链力量（4 个）', ['靠墙小幅下蹲 0～40°', '向前上台阶', '侧向上台阶', '站立弹力带伸膝末端'], GR),
        ('开链力量（3 个）', ['侧卧髋外展', '坐位髋外旋', '坐位伸膝', '沙袋 0.5～10 kg'], GR)]
for i, (t, ls, bg) in enumerate(cols):
    x0 = 20 + i * 460
    dr.rounded_rectangle([x0, 145, x0 + 440, 560], 14, fill=bg)
    ctext(dr, x0 + 220, 165, t, font(34), TEAL)
    for j, l in enumerate(ls): ctext(dr, x0 + 220, 235 + j * 62, l, font(28), RED if j == 4 or l.startswith('沙袋') else INK)
dr.text((30, 585), '↑ 两组都做（对照组只做这些）', font=font(30), fill=GREY)
dr.rounded_rectangle([20, 640, W - 20, H - 20], 14, fill=OR)
dr.text((50, 660), '手法组额外加 3 个手法（各约 1 分钟）', font=font(36), fill=(190, 100, 40))
for i, t in enumerate(['① 髌骨向内滑动松动', '② 髂胫束松解 + 髂胫束松动', '③ 外侧支持带深横摩擦按摩']):
    dr.text((60 + (i % 2) * 650, 730 + (i // 2) * 70), t, font=font(32), fill=INK)
save(titled(im, '治疗方案总览'), 2)

# ---------- 手法 ----------
f1 = tagged(89, 1200, [(0.0, 0.0, '① 髌骨向内滑动：掌根推髌骨向内，持续 1 分钟')], 32)
f2 = tagged(126, 1200, [(0.0, 0.0, '② 髂胫束松解'), (0.37, 0.0, '髂胫束松动')], 30)
f3 = tagged(125, 560, [(0.0, 0.0, '③ 外侧支持带深横摩擦')], 28)
save(titled(stack([f1, f2, f3]), '原文图 1～3　手法组额外的 3 个手法', 1200), 3)

# ---------- 牵伸 ----------
f4 = tagged(147, 1300, [(0.0, 0.0, '腘绳肌牵伸（仰卧）'), (0.505, 0.0, '股四头肌牵伸（侧卧）')])
f5 = tagged(146, 1300, [(0.0, 0.0, '髂胫束牵伸（侧卧）'), (0.505, 0.0, '小腿三头肌牵伸（仰卧）')])
save(titled(stack([f4, f5]), '原文图 4、5　治疗师辅助牵伸：每块肌肉 30 秒 × 3 次', 1300), 4)

# ---------- 闭链 ----------
f6 = tagged(145, 560, [(0.0, 0.0, '靠墙小幅下蹲 0～40°')], 28)
f7 = tagged(164, 900, [(0.0, 0.0, '向前上台阶'), (0.53, 0.0, '抬起对侧腿')], 28)
f8 = tagged(163, 900, [(0.0, 0.0, '侧向上台阶'), (0.53, 0.0, '抬起对侧腿')], 28)
f9 = tagged(162, 900, [(0.0, 0.0, '弹力带：屈膝起始'), (0.5, 0.0, '伸膝到底')], 26)
left = stack([f7, f8]); right = stack([f6, f9])
s = left.height / right.height; right = right.resize((round(right.width * s), left.height), Image.LANCZOS)
board = Image.new('RGB', (left.width + right.width + 16, left.height), 'white'); board.paste(left, (0, 0)); board.paste(right, (left.width + 16, 0))
save(titled(board, '原文图 6～9　闭链力量：每次保持 6 秒、放松 3 秒 × 10 次', 1400), 5)

# ---------- 开链 ----------
f10 = tagged(198, 1400, [(0.0, 0.0, '侧卧髋外展'), (0.39, 0.0, '坐位髋外旋'), (0.71, 0.0, '坐位伸膝')], 28)
save(titled(f10, '原文图 10　开链力量：沙袋负重，2 组 × 10 次', 1400), 6)

# ---------- 剂量卡 ----------
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
rows = [('牵伸', '小腿、腘绳肌（仰卧）；股四头肌、髂胫束（侧卧）', '治疗师保持 30 秒 × 3 次 / 每块肌肉', LT),
        ('闭链力量', '靠墙小幅下蹲（0～40°）、向前上台阶、侧向上台阶、站立弹力带伸膝末端', '保持 6 秒 + 放松 3 秒，10 次；动作间休息 1 分钟；每周每个动作 +2 次', GR),
        ('开链力量', '侧卧髋外展、坐位髋外旋、坐位伸膝', '2 组 × 10 次，保持 6 秒 + 放松 3 秒；组间和动作间休息 1 分钟；沙袋 0.5～10 kg，每周按 10 次最大重复量调整', GR),
        ('手法（手法组）', '髌骨向内滑动；髂胫束前后缘松解 + 拇食指捏住前后推动；外侧支持带垂直方向深横摩擦', '各约 1 分钟、做 1 次；感觉组织“松开”、出现新的阻力点就往前推进', OR)]
y = 20
for t, a, b2, bg in rows:
    dr.rounded_rectangle([20, y, W - 20, y + 220], 14, fill=bg)
    dr.text((46, y + 22), t, font=font(36), fill=TEAL if bg != OR else (190, 100, 40))
    yy = y + 80
    for txt, f, c in [(a, 27, INK), (b2, 27, RED)]:
        line = ''
        for ch in txt:
            if dr.textlength(line + ch, font=font(f)) > 1300: dr.text((46, yy), line, font=font(f), fill=c); yy += 40; line = ch
            else: line += ch
        dr.text((46, yy), line, font=font(f), fill=c); yy += 46
    y += 240
save(titled(im, '每个环节怎么做、做多少'), 7)

# ---------- 流程 ----------
W, H = 1300, 900; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
bx(dr, 350, 20, 950, 100, ['评估是否符合条件 159 人'], LT, 32)
dr.line([650, 100, 650, 300], fill=TEAL, width=4); dr.line([650, 160, 840, 160], fill=TEAL, width=4)
bx(dr, 840, 115, 1280, 260, ['排除 100 人', '不符合纳入标准 59 人', '拒绝参加 41 人'], GY, 26)
down(dr, 650, 280, 330)
bx(dr, 350, 330, 950, 410, ['随机分组（电脑表格生成）59 人'], LT, 30)
dr.line([650, 410, 650, 450], fill=TEAL, width=4); dr.line([330, 450, 970, 450], fill=TEAL, width=4)
down(dr, 330, 450, 510); down(dr, 970, 450, 510)
for cx, t, a in [(330, ['对照组 30 人', '全部接受分配的治疗'], ['分析 28 人', '其他疾病排除 2 人']),
                 (970, ['手法组 29 人', '接受治疗 27 人', '未接受 2 人（个人原因/失联）'], ['分析 25 人', '其他疾病或个人原因排除 2 人'])]:
    bx(dr, cx - 310, 510, cx + 310, 680, t, LT if cx < 600 else OR, 28)
    down(dr, cx, 680, 740)
    bx(dr, cx - 310, 740, cx + 310, 870, a, 'white', 28)
save(titled(im, '原文图 11　研究流程（中文重绘）'), 8)

# ---------- 结果 ----------
fig, axs = plt.subplots(1, 5, figsize=(16, 4.4))
res = [('上楼痛', (50.39, 23.25), (50.68, 20.96)), ('下楼痛', (40.93, 17.64), (38.28, 15.52)), ('下蹲痛', (53.43, 26.89), (64.28, 23.96)),
       ('久坐痛', (58.54, 32.86), (57.16, 27.68)), ('Kujala 功能', (70.86, 83.75), (67.08, 83.84))]
for ax, (t, a, b) in zip(axs, res):
    x = np.arange(2)
    ax.bar(x - 0.2, a, 0.38, color=CA, label='对照组'); ax.bar(x + 0.2, b, 0.38, color=CB, label='手法组')
    for i in range(2): ax.text(i - 0.2, a[i] + 1.5, f'{a[i]:.0f}', ha='center', fontsize=11); ax.text(i + 0.2, b[i] + 1.5, f'{b[i]:.0f}', ha='center', fontsize=11)
    ax.set_xticks(x); ax.set_xticklabels(['治疗前', '4 周后']); ax.set_title(t, fontsize=15); ax.set_ylim(0, 100)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
axs[0].set_ylabel('疼痛（0～100 mm）'); axs[4].set_ylabel('分（100 = 无受限）')
axs[0].legend(frameon=False, fontsize=11)
fig.text(0.01, -0.05, '均值，按原文表 2、3 重绘。两组都明显改善，组间无显著差别', fontsize=11, color='#777')
plt.tight_layout()
b = BytesIO(); plt.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close()
save(titled(Image.open(b).convert('RGB'), '结果：4 周后疼痛和功能（中文重绘）', 1300), 9)

# ---------- 封面 ----------
c = xim(89, 900); top = max(0, (c.height - 383) // 2); c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
