#!/usr/bin/env python3
"""Johnson & Grindstaff 2012 胸椎区域自我松动临床建议：首图为原题直译标题卡；原文图 1～3 照片直接使用并加中文说明；
两种练法对照卡为编者整理；胸椎正常活动度按原文文字数值重绘。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
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


# 原文照片直接使用
F1 = raw(10); F1a, F1b = F1.crop((0, 0, F1.width, 639)), F1.crop((0, 674, F1.width, F1.height))
F2, F3 = raw(14), raw(15)

# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '临床建议 · IJSPT 2012', font=font(32), fill=TEAL)
dr.text((70, 140), '胸椎区域自我松动：', font=font(58), fill=INK)
dr.text((70, 222), '一项临床建议', font=font(58), fill=INK)
dr.text((70, 330), 'Thoracic Region Self-Mobilization: A Clinical Suggestion', font=font(28), fill=GREY)
dr.line([70, 430, W - 70, 430], fill=(200, 205, 210), width=2)
dr.text((70, 460), 'Johnson KD, Grindstaff TL. Int J Sports Phys Ther 2012;7(2):252-256', font=font(30), fill=GREY)
dr.text((70, 515), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1：制作
save(titled(pair(F1a, F1b, 'a 两个网球并拢，用 1.27 cm（半英寸）运动胶布从一个球的一端绕到另一个球的另一端，再绕回起点，形成椭圆形；重复缠绕直到把两个球完全包住',
                 'b 做好的工具：最后在两球之间垂直方向用力缠一圈胶布，让中间的凹槽更明显，练习时用来对准棘突', W=1200),
     '原文图 1　自制“双网球”松动工具'), 2)

# 原文图 2：迷你卷腹
save(titled(capbox(F2, 'a 把工具放在要松动的节段，中间凹槽对准棘突，两个球落在棘突两侧（通常放在目标节段的下一节）；b 仰卧，双臂交叉抱胸，让肩胛骨前伸、避开球；c 慢慢把肩膀抬离地面约 13～15 cm，数 3 秒，再慢慢放下'),
            '原文图 2　胸椎迷你卷腹（关节松动）'), 3)

# 原文图 3：仰卧画圈
save(titled(capbox(F3, 'a 工具与脊柱平行，放在有压痛、不适的位置（可针对肋椎关节、肋横突关节或菱形肌、斜方肌、肩胛提肌）；b 仰卧，肩前屈 90°，手臂伸直垂直地面，顺时针、逆时针画小圈'),
            '原文图 3　仰卧手臂画圈（软组织松动）'), 4)

# 两种练法对照卡
W = 1200; im = Image.new('RGB', (W, 760), 'white'); dr = ImageDraw.Draw(im)
dr.rounded_rectangle([40, 20, 580, 570], 14, fill=LT); dr.rounded_rectangle([620, 20, 1160, 570], 14, fill=OR)
ctext(dr, 310, 44, '胸椎迷你卷腹', font(36), TEAL); ctext(dr, 890, 44, '仰卧手臂画圈', font(36), (180, 90, 20))
L = ['目标：胸椎节段活动不足，向伸展方向松动', '工具横放，凹槽对准棘突，放在目标节段下一节', '双臂抱胸，肩膀抬起约 13～15 cm、保持 3 秒再放下', '2～3 组 × 15 次', '强度自己控制：先做到活动末端，耐受后在末端处小幅度反复']
R = ['目标：触发点、肋椎 / 肋横突关节、菱形肌、斜方肌、肩胛提肌', '工具竖放与脊柱平行，放在压痛点', '肩前屈 90°，手臂伸直，画小圈', '顺、逆时针各做，2～3 组 × 30～60 秒', '可以换几个压痛点分别做']
y = 110
for t in L: y = bullet(dr, 64, y, t, 26, 500, gap=8) + 14
y = 110
for t in R: y = bullet(dr, 644, y, t, 26, 500, gap=8) + 14
dr.rounded_rectangle([40, 600, 1160, 740], 14, fill=PK)
y = para(dr, 70, 624, '太疼怎么办：改成站立靠墙做，减小压在横突和肋骨上的力；还是不舒服就换别的方法', 26, 1060, gap=8) + 10
para(dr, 70, y, '不要用：怀疑骨折、关节过度活动、有神经症状，或患者自己做不放心', 26, 1060, fill=RED, gap=8)
save(titled(im, '两种练法怎么选（编者根据原文整理）'), 5)

# 胸椎正常活动度
fig, ax = plt.subplots(figsize=(12, 4.6), dpi=100)
rng = [('屈曲', 20, 45), ('伸展', 25, 45), ('侧屈', 20, 40), ('旋转', 35, 60)]
for i, (n, a, b_) in enumerate(rng[::-1]):
    ax.barh(i, b_ - a, left=a, color='#0b6e82', height=0.5)
    ax.text(a - 1, i, f'{a}°', ha='right', va='center', fontsize=14); ax.text(b_ + 1, i, f'{b_}°', ha='left', va='center', fontsize=14)
ax.set_yticks(range(4)); ax.set_yticklabels([r[0] for r in rng[::-1]], fontsize=15); ax.set_xlim(0, 70)
ax.set_xlabel('角度（°）', fontsize=13); ax.tick_params(labelsize=12); ax.spines[['top', 'right']].set_visible(False)
fig.text(0.5, 0.01, '按原文引用的参考范围重绘；临床可用卷尺、量角器、倾角仪或目测评估，胸椎与肋骨运动很难完全分开测量', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.05, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '胸椎正常活动度大致范围', 1200), 6)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), '临床建议 · 胸椎自我松动', font=font(40), fill=TEAL)
dr.text((50, 130), '两个网球 + 一卷胶布', font=font(62), fill=INK)
dr.text((50, 220), '自己松胸椎', font=font(62), fill=INK)
dr.text((50, 318), '工具制作 · 迷你卷腹 · 仰卧画圈', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
