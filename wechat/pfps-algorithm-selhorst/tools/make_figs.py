#!/usr/bin/env python3
"""Selhorst 2015：图 1 PFPS 分组算法、图 9 招募流程图中文重绘；图 2～8 照片两两等高并排；封面取自图 2。
用法：python3 make_figs.py <素材目录（x03..x09.png、title.png）> <输出目录>"""
import re
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66); INK = (25, 25, 25); EDGE = (90, 90, 90)
BLUE = (214, 228, 243); YEL = (255, 241, 150); GRN = (190, 235, 180); GRAY = (230, 230, 230)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')
_d = ImageDraw.Draw(Image.new('RGB', (10, 10)))


def wrap(t, f, w):
    out = []
    for para in t.split('\n'):
        toks = re.findall(r'[0-9A-Za-z/.%<>≤≥=~～+\-*]+ ?|.', para); line = ''
        for tk in toks:
            if line and _d.textlength(line + tk, font=f) > w:
                out.append(line); line = tk
            else:
                line += tk
        out.append(line)
    for i in range(1, len(out)):
        while out[i] and out[i][0] in '，。；：、）)？！' and len(out[i - 1]) > 1:
            out[i - 1], out[i] = out[i - 1][:-1], out[i - 1][-1] + out[i]
    return out


def box(d, x0, y0, w, t, fill, fs=28, lh=38, pad=18, bold_first=True, h=None):
    lines = wrap(t, font(fs), w - pad * 2)
    hh = h or pad * 2 + lh * len(lines)
    d.rectangle([x0, y0, x0 + w, y0 + hh], fill=fill, outline=EDGE, width=3)
    ty = y0 + (hh - lh * len(lines)) / 2
    for i, ln in enumerate(lines):
        f = font(fs); tw = d.textlength(ln, font=f)
        kw = dict(stroke_width=1, stroke_fill=INK) if (i == 0 and bold_first) else {}
        d.text((x0 + w / 2 - tw / 2, ty + i * lh), ln, font=f, fill=INK, **kw)
    return hh


def bh(t, w, fs=28, lh=38, pad=18):
    return pad * 2 + lh * len(wrap(t, font(fs), w - pad * 2))


def varrow(d, cx, y0, y1, label=None, col=(46, 125, 50)):
    d.line([cx, y0, cx, y1 - 18], fill=col, width=6)
    d.polygon([(cx - 15, y1 - 20), (cx + 15, y1 - 20), (cx, y1)], fill=col)
    if label:
        d.text((cx + 18, (y0 + y1) / 2 - 16), label, font=font(26), fill=col)


def harrow(d, x0, x1, cy, label=None, col=(198, 40, 40)):
    d.line([x0, cy, x1 - 18, cy], fill=col, width=6)
    d.polygon([(x1 - 20, cy - 15), (x1 - 20, cy + 15), (x1, cy)], fill=col)
    if label:
        f = font(24); tw = d.textlength(label, font=f)
        d.text(((x0 + x1) / 2 - tw / 2, cy - 36), label, font=f, fill=col)


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 20))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def pair(a, b, ta, tb, H=900, gap=14):
    a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS)
    b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
    badge(a, ta); badge(b, tb)
    im = Image.new('RGB', (a.width + b.width + gap, H), 'white')
    im.paste(a, (0, 0)); im.paste(b, (a.width + gap, 0))
    return im


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')

# ---------- 图 1：PFPS 分组算法 ----------
W = 1080; LX, LW, RX, RW = 30, 470, 600, 450
rows = [
    ('恐惧回避\nFABQ-PA 评分 <15/24？', '恐惧回避组\n· 恐惧回避教育\n· 采用认知行为方法的分级运动', '否'),
    ('主要肌肉柔韧性\n股四头肌 ≥130°\n腓肠肌 ≥12°\n比目鱼肌 ≥20°\n负重背屈 >50°', '柔韧性组\n· 牵伸紧张的主要和次要肌肉\n· 加入低强度股四头肌和髋部强化\n· 单纯牵伸已被证明无效', '否'),
    ('次要肌肉柔韧性\nThomas 试验阴性？\nOber 试验阴性？\n直腿抬高 ≥80°？\n内收肌柔韧性正常？', None, '4 项中 3 项紧张'),
    ('功能性排列不良\n单腿蹲评分 ≤1？\n侧向下台阶评分 ≤1？', '功能性排列不良组\n· 处理动态动作中核心/下肢的神经肌肉控制\n· 通过增强式和专项活动逐步提高控制', '否'),
]
im = Image.new('RGB', (W, 2400), 'white'); d = ImageDraw.Draw(im)
f = font(40); t = '图1　PFPS 分组治疗算法'
d.text((W / 2 - d.textlength(t, font=f) / 2, 20), t, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
y = 100; flex_box = None
for i, (q, g, lab) in enumerate(rows):
    hq = bh(q, LW)
    hg = bh(g, RW) if g else 0
    h = max(hq, hg)
    box(d, LX, y, LW, q, YEL, h=h if g else hq)
    cy = y + (h if g else hq) / 2
    if g:
        box(d, RX, y, RW, g, BLUE, fs=26, lh=36, h=h)
        if i == 1:
            flex_box = (y, h)
    else:
        # 指向上一行的柔韧性组
        fy = flex_box[0] + flex_box[1]
        d.line([LX + LW, cy, RX + RW // 2, cy], fill=(198, 40, 40), width=6)
        d.line([RX + RW // 2, cy, RX + RW // 2, fy + 20], fill=(198, 40, 40), width=6)
        d.polygon([(RX + RW // 2 - 15, fy + 22), (RX + RW // 2 + 15, fy + 22), (RX + RW // 2, fy)], fill=(198, 40, 40))
        f2 = font(24); d.text((LX + LW + 14, cy - 36), lab, font=f2, fill=(198, 40, 40))
    if g:
        harrow(d, LX + LW, RX, cy, lab)
    y += (h if g else hq)
    varrow(d, LX + LW // 2, y, y + 70, '是'); y += 70
last = '强化/功能进阶组\n· 强化下肢，重点股四头肌、髋外展肌/外旋肌\n· 训练逐步帮助患者回到运动/功能活动'
hl_ = box(d, LX, y, W - 60, last, GRN, fs=27, lh=38)
y += hl_
d.text((LX, y + 14), '注：判断为“否”（或次要肌肉 4 项中 3 项紧张）即进入右侧对应治疗组；达标后才进入下一步评估', font=font(22), fill=(110, 110, 110))
im.crop((0, 0, W, y + 60)).save(f'{OUT}/img02.jpg', quality=92)

# ---------- 照片 ----------
save(pair(X(3), X(4), '图2', '图3'), 'img03.jpg')
save(pair(X(5), X(6), '图4', '图5'), 'img04.jpg')
save(pair(X(7), X(8), '图6', '图7'), 'img05.jpg')
save(badge(X(9), '图8'), 'img06.jpg', W=640)

# ---------- 图 9：招募流程 ----------
im = Image.new('RGB', (W, 1200), 'white'); d = ImageDraw.Draw(im)
f = font(40); t = '图9　患者招募流程'
d.text((W / 2 - d.textlength(t, font=f) / 2, 20), t, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
CX, CW = 60, 440; SX, SW = 580, 460; E = EDGE
y = 100
h = box(d, CX, y, CW, '评估是否符合条件\n（n=157）', BLUE); c1 = y + h / 2
h2 = box(d, SX, y + 110, SW, '排除（n=127）\n· 不符合纳入标准（n=127）\n· 拒绝参加（n=0）', GRAY, fs=26, lh=36, bold_first=True)
d.line([CX + CW // 2, y + h, CX + CW // 2, y + 360], fill=E, width=5)
harrow(d, CX + CW // 2, SX, y + 110 + h2 / 2, col=E)
y += 360
h = box(d, CX, y, CW, '同意接受治疗\n（n=30）', BLUE)
d.polygon([(CX + CW // 2 - 15, y - 20), (CX + CW // 2 + 15, y - 20), (CX + CW // 2, y)], fill=E)
y += h
d.line([CX + CW // 2, y, CX + CW // 2, y + 380], fill=E, width=5)
h2 = box(d, SX, y + 40, SW, '6 周随访\n· 失访（n=4）\n· 中止干预（n=5）：时间冲突 2 人，经济原因 1 人，与研究无关原因 2 人', GRAY, fs=26, lh=36)
harrow(d, CX + CW // 2, SX, y + 40 + h2 / 2, col=E)
y += 380
d.polygon([(CX + CW // 2 - 15, y - 20), (CX + CW // 2 + 15, y - 20), (CX + CW // 2, y)], fill=E)
h = box(d, CX, y, CW, '纳入分析\n（n=21）', GRN)
y += h
im.crop((0, 0, W, y + 30)).save(f'{OUT}/img07.jpg', quality=92)

# ---------- 封面：图 2 股四头肌柔韧性测试 ----------
c = X(3); w, h = c.size; ch = round(w * 383 / 900); y = 170
c.crop((0, y, w, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('done')
