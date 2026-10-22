#!/usr/bin/env python3
"""Ilizaliturri 等 2022 臀中肌、臀小肌治疗后的康复：首图中文标题卡；原文图 1～3 照片直接使用，图中英文标签原位改为中文；
病理力学数据与证据数据用中文绘图；保守康复与术后方案整理为中文卡片；表 1 用中文重排（保留原文排版的数值顺序）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys, os
import numpy as np
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
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


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def relabel(im, items, bg='white'):
    """items: (box@1000宽, 文字, 字号@1000宽, 对齐)"""
    s = im.width / 1000; d = ImageDraw.Draw(im)
    for box, t, fs, *al in items:
        b = [int(v * s) for v in box]
        d.rectangle(b, fill=bg)
        f = font(fs * s); lines = t.split('\n'); lh = fs * s * 1.25
        y0 = (b[1] + b[3]) / 2 - lh * len(lines) / 2
        for i, l in enumerate(lines):
            w = d.textlength(l, font=f)
            x = b[0] + 2 if al and al[0] == 'l' else (b[0] + b[2]) / 2 - w / 2
            d.text((x, y0 + i * lh), l, font=f, fill='black')
    return im


def blur(im, boxes, r=10):
    s = im.width / 1000
    for b0 in boxes:
        b = tuple(int(v * s) for v in b0); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * s)), b[:2])
    return im
def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def card(W, title, blocks, bg=(246, 248, 250)):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


up = lambda im, w=1000: im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def lab(im, page_bbox, items, fs=30, pad=6):
    """items: (页面 x, 页面 y, 中文, 颜色)；按 PDF 坐标映射到图像，白底写字"""
    x0, y0, x1, y1 = page_bbox; s = im.width / (x1 - x0); dr = ImageDraw.Draw(im)
    for x, y, t, *c in items:
        X, Y = (x - x0) * s, (y - y0) * s; f = font(fs)
        lines = t.split('\n'); w = max(dr.textlength(l, font=f) for l in lines); h = fs * 1.2 * len(lines)
        dr.rounded_rectangle([X - pad, Y - pad, X + w + pad, Y + h + pad], 6, fill=(255, 255, 255))
        for i, l in enumerate(lines): dr.text((X, Y + i * fs * 1.2), l, font=f, fill=c[0] if c else INK)
    return im


def row(ims, W=1200, gap=12):
    h = min(i.height for i in ims); ims = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in ims]
    tw = sum(i.width for i in ims) + gap * (len(ims) - 1); s = W / tw
    ims = [i.resize((round(i.width * s), round(h * s)), Image.LANCZOS) for i in ims]
    out = Image.new('RGB', (W, ims[0].height), 'white'); x = 0
    for i in ims: out.paste(i, (x, 0)); x += i.width + round(gap * s)
    return out


def stack(ims, gap=14):
    W = max(i.width for i in ims); out = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: out.paste(i, (0, y)); y += i.height + gap
    return out


import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0, HERE)
SRC = _os.path.join(HERE, '..', 'src')
import zh

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '专家意见 · 运动员康复与重返运动系列 · 2022', font=font(32), fill=TEAL)
dr.text((70, 150), '臀中肌和臀小肌治疗后的康复', font=font(60), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 335), 'Ilizaliturri VM Jr, Zepeda Mora R, Rodríguez Vega LP.', font=font(28), fill=GREY)
dr.text((70, 380), 'Arthrosc Sports Med Rehabil. 2022;4(1):e41-e50', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)


def boxes(im, items):
    """items: (box@1000宽, 文字, 字号@1000宽, 对齐, 颜色)；白底覆盖后写中文"""
    s = im.width / 1000; d = ImageDraw.Draw(im)
    for box, t, fs, al, col in items:
        b = [int(v * s) for v in box]; d.rectangle(b, fill='white'); f = font(fs * s); lh = fs * s * 1.35
        lines = t.split('\n'); y0 = (b[1] + b[3]) / 2 - lh * len(lines) / 2 if al == 'c' else b[1] + 4 * s
        for i, l in enumerate(lines):
            x = (b[0] + b[2]) / 2 - d.textlength(l, font=f) / 2 if al == 'c' else b[0] + 6 * s
            d.text((x, y0 + i * lh), l, font=f, fill=col)
    return im


# 原文图 1
f1 = boxes(raw(65), [((90, 0, 225, 37), '站立', 24, 'c', INK), ((437, 0, 570, 37), '站立（交叉腿）', 22, 'c', INK),
                     ((787, 0, 895, 39), '坐位', 24, 'c', INK), ((787, 624, 895, 666), '坐位（跷腿）', 22, 'c', INK),
                     ((255, 628, 405, 663), '拉伸', 24, 'c', INK)])
save(capbox(f1, '原文图 1  临床示意照片。上左：站立，髂胫束处于放松位；上中：交叉腿站立，增加髂胫束张力；上右：坐位，髂胫束放松；'
                '下右：跷二郎腿坐，增加髂胫束对臀肌腱的压力；下左：仰卧位髂胫束拉伸'), 2)

# 原文图 2：三个文字框内改写中文
f2 = raw(84)
f2 = boxes(f2, [((5, 202, 307, 358), '侧卧\n下方髋：体重直接压在大转子上\n上方髋：屈曲并内收\n\n高压迫', 15, 'l', INK),
                ((348, 202, 652, 358), '仰卧\n双髋轻度外展\n\n\n\n无压迫', 15, 'l', INK),
                ((691, 202, 994, 358), '改良侧卧\n两腿之间夹枕头\n\n\n\n压迫减轻', 15, 'l', INK)])
d = ImageDraw.Draw(f2); s = f2.width / 1000
for x0, c in ((5, RED), (348, (0, 140, 70)), (691, (200, 120, 0))):
    d.text((int((x0 + 6) * s), int(206 * s)), {5: '侧卧', 348: '仰卧', 691: '改良侧卧'}[x0], font=font(15 * s), fill=c)
save(capbox(f2, '原文图 2  卧姿与臀肌腱受压：左为普通侧卧（高压迫），中为仰卧轻度外展（无压迫），右为两腿间夹枕的改良侧卧（压迫减轻）'), 3)

# 病理力学数据图
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8), dpi=100)
a = ax[0]; v = [4, 36, 106]; bb = a.bar(['内收 0°', '内收 10°', '内收 40°'], v, color=['#9bc9d1', '#4f9fae', '#00788c'], width=.55)
for r, t in zip(bb, v): a.text(r.get_x() + r.get_width() / 2, t + 2, f'{t} N', ha='center', fontsize=13)
a.set_title('A  髂胫束对臀肌腱的压迫力随髋内收增加', fontsize=13); a.set_ylabel('压迫力（N）', fontsize=12); a.set_ylim(0, 125)
a = ax[1]; v = [656, 997]; bb = a.bar(['颈干角 128°', '颈干角 115°'], v, color=['#9bc9d1', '#be2832'], width=.5)
for r, t in zip(bb, v): a.text(r.get_x() + r.get_width() / 2, t + 15, f'约 {t} N', ha='center', fontsize=13)
a.set_title('B  股骨颈干角越小，髂胫束压在大转子上的力越大', fontsize=13); a.set_ylabel('压迫力（N）', fontsize=12); a.set_ylim(0, 1150)
for a in ax: a.spines[['top', 'right']].set_visible(False); a.tick_params(labelsize=12)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '编者根据原文正文数字绘图：A 髋内收角度越大，压迫越大（4→36→106 N）；B 颈干角从 128° 减到 115°，压迫力由约 656 N 升到约 997 N。'
                                          '两组数字来自不同模型，量级不能直接互比'), 4)

# 保守康复卡片
save(card(1200, '保守治疗的运动康复：按“先减压、再加载”推进', [
    ('① 姿势卫生：先把压迫拿掉', '避免交叉腿站立、跷二郎腿或双膝并拢坐、单侧髋“挂”着站。\n睡觉：仰卧膝下垫枕；侧卧时两腿间夹枕；也可取“四分之一俯卧”，让体重落在大腿前外侧而不是大转子上。\n不做内收肌、屈髋肌、伸髋肌的强力拉伸（拉伸本身就是“张力+压迫”的组合），可改用按摩和针刺类技术。', LT, TEAL),
    ('② 负荷管理：控制量，不是完全休息', '老年或体能差的患者：少爬坡和楼梯，按症状调节步行距离。\n运动员：暂停长跑、节奏跑、坡道跑和增强式训练，可改为水中运动、骑车。\n疼痛下降后，再在更大负荷、更快速度、更复杂动作（跑、落地、变向）中重新训练髋内收控制。', OR, (200, 120, 0)),
    ('③ 等长收缩：先止痛、试探肌腱反应', '低强度持续收缩（约 25% 最大自主收缩）在健康人中升高痛阈的效果，好于 80% 的高强度收缩。\n患侧在上侧卧，用枕头把髋垫到中立或轻度外展位做等长外展；双侧患病可仰卧轻度外展，用带子或弹力带绕大腿远端给轻阻力；也可站立轻度外展，背靠墙或手扶凳。\n先慢慢加力、尽量无痛，摸清肌腱的“反应性”。', GR, (0, 120, 60)),
    ('④ 低速、高张力负荷：增肌并提升肌腱承载力', '在不加压迫的外展位进行低速、大负荷的外展训练，类似肌肥大方案；每周只练 3 次，给软组织留出恢复适应时间。\n从中等用力、少次数起步；每一级负荷耐受后再缓慢加量。\n夜间痛的变化是判断反应的好指标。', PK, RED),
    ('⑤ 功能训练与合并问题', '桥式、下蹲、台阶训练可同时练功能性髋内收控制、下肢伸肌和腰盆支撑。\n腰椎、髋、膝的合并退变需要处理，但处理时仍要守住“臀肌腱不受压”的原则；运动和活动量增加也有助于减重。', (240, 240, 248), (90, 70, 170)),
]), 5)

# 原文图 3
f3 = boxes(raw(98), [((30, 5, 460, 50), '低负荷等长外展', 30, 'c', INK), ((590, 0, 960, 78), '中等负荷等长外展', 30, 'c', INK),
                     ((115, 86, 310, 115), '蚌式 屈髋 45°', 20, 'c', INK), ((675, 86, 865, 115), '单腿桥', 20, 'c', INK),
                     ((160, 378, 275, 413), '站立', 20, 'c', INK), ((745, 380, 830, 413), '下蹲', 20, 'c', INK)])
save(capbox(f3, '原文图 3  用于臀肌腱病的髋外展训练。左列为低负荷等长外展：屈髋 45° 蚌式、站立位双膝向外推（蓝色箭头示外展方向）；'
                '右列为中等负荷：单腿桥、下蹲'), 6)

# 证据数据图
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8), dpi=100, gridspec_kw={'width_ratios': [1.3, 1]})
a = ax[0]; x = np.arange(3); w = .36
e, sw = [7, 40, 80], [13, 68, 74]
b1 = a.bar(x - w / 2, e, w, color='#00788c', label='居家运动'); b2 = a.bar(x + w / 2, sw, w, color='#c9a227', label='冲击波')
for bs in (b1, b2):
    for r in bs: a.text(r.get_x() + r.get_width() / 2, r.get_height() + 2, f'{int(r.get_height())}%', ha='center', fontsize=12)
a.set_xticks(x); a.set_xticklabels(['4 周', '4 个月', '15 个月'], fontsize=12); a.set_ylim(0, 100); a.set_ylabel('报告改善的比例（%）', fontsize=12)
a.set_title('A  Rompe 2009 非随机试验（运动方案未专门练外展肌）', fontsize=12); a.legend(frameon=False, fontsize=12)
a = ax[1]; v = [78.6, 58.3, 51.9]; bb = a.bar(['教育+运动', '激素注射', '观望'], v, color=['#00788c', '#9aa5ad', '#c8ced3'], width=.55)
for r, t in zip(bb, v): a.text(r.get_x() + r.get_width() / 2, t + 2, f'{t}%', ha='center', fontsize=13)
a.set_ylim(0, 100); a.set_title('B  Mellor 2018 随机试验：52 周总体改善成功率', fontsize=12)
for a in ax: a.spines[['top', 'right']].set_visible(False); a.tick_params(labelsize=12)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(capbox(Image.open(buf).convert('RGB'), '编者根据原文引用的数字绘图。B 中教育+运动比激素注射高 20.4 个百分点（95% CI 4.9～35.9），比观望高 26.8 个百分点（95% CI 11.3～42.3）'), 7)

# 术后方案卡片
save(card(1200, '术后康复：先看修补方式，再定负重、支具和练习', [
    ('Milwaukee 分级（按钟面）', '右髋取 11～3 点，左髋取 9～1 点；撕裂从臀中肌腱中央纤维（右髋 1 点 / 左髋 11 点）开始，向下、向后扩展。\nⅠ 级 1 个钟点范围；Ⅱ 级 2 个；Ⅲ 级 3 个；Ⅳ 级几乎完全撕脱。', LT, TEAL),
    ('Davies 开放修补（23 例）', 'Ⅰ、Ⅱ 级：6.5 mm 锚钉 + 2 号缝线；Ⅲ、Ⅳ 级：骨隧道 + 5 号缝线。\n25% 负重时间：Ⅰ 级 6 周、Ⅱ 级 8 周、Ⅲ 级 10 周、Ⅳ 级 12 周。不同撕裂类型的结果没有显著差异。', OR, (200, 120, 0)),
    ('Stanton 急性外伤性撕裂开放修补（个案）', '限制负重 12 周后逐步进展；前 6 周屈髋不超过 90°；8 周后才允许髋外展或被动髋内旋。', PK, RED),
    ('Thaunat 内镜修补', '前 6 周避免主动康复：不做主动外旋和内收，前 3 周屈髋可到 90°，期间佩戴外展支具；6 周起逐步恢复负重以及主动外旋、外展。', GR, (0, 120, 60)),
    ('Kocaoglu / Saltzman 三期方案', '第 1 期（0～6 周）：不负重，轻柔被动关节活动，全天佩戴限制外展的支具。\n第 2 期（6～12 周）：逐步负重，停用支具，开始髋力量训练。\n第 3 期（12 周以后）：脱拐独立行走，回归日常活动。', (240, 240, 248), (90, 70, 170)),
]), 8)

# 表 1 中文重排
SEG3 = '前部\n中部\n后部'
T1 = [
    ('侧卧', '髋外展\n髋外展＋外旋\n髋外展＋内旋\n髋外展＋后伸\n蚌式 屈髋 0°\n蚌式 屈髋 30°\n蚌式 屈髋 45°\n蚌式 屈髋 60°*', SEG3,
     '13%～17%\n13%～21%\n3%\n13%～18%', '29%～37%\n23%～37%\n33%～36%\n31%\n27%～40%\n27%～36%\n23%\n18%～38%', '42%～45%\n41%～53%\n45%～49%\n47%', '79～100R\n62%'),
    ('下蹲', '单腿蹲\n单腿蹲＋外展\n单腿蹲＋内收\n单腿靠墙蹲\n单腿靠墙蹲＋外展\n单腿靠墙蹲＋内收\n下蹲\n靠墙蹲\n下蹲＋外展\n下蹲＋内收', '\n'.join([SEG3] * 6),
     '18%\n19%\n13%\n16%\n9%～12%\n9%～10%', '24%～37%\n27%\n33%\n31%\n22%\n22%～32%\n35%\n29%\n33%\n21%\n28%\n21%～33%\n24%', '41%～60%\n42%～46%\n42%\n52%\n44%\n47%～52%\n59%', '90%\n60%～92%\n87%'),
    ('台阶', '侧向上台阶\n侧向上台阶＋内旋\n侧向上台阶＋外旋\n侧向下台阶\n侧向迈步\n侧向迈步\n侧向迈步＋内旋\n侧向迈步＋外旋\n向前上台阶\n向前下台阶\n后退上台阶', '中部\n后部',
     '17%\n14%～17%', '38%～39%\n30%\n19%～25%\n24～40R\n19～36R\n27～48R\n29%～30%\n19%～28%\n37%', '60%\n41%\n40～50R\n44～58R\n44～55R', '63%\n74%\n62%'),
    ('弓步', '向前弓步\n横向弓步\n侧向弓步', SEG3, '8%～25%\n13%', '29%\n28R\n39%', '45R\n42%\n48%', '71R\n68%'),
    ('站立', '提髋/骨盆下降\n髋外展\n髋外展（运动侧下肢）', SEG3 + '\n' + SEG3, '', '21%～25%\n23%～38%\n22%～38%\n30%\n28%～33%', '42%～58%\n56%\n42～50R\n41%\n53R', '69%～80%\n66%～88%\n74%～88%'),
    ('仰卧', '单腿桥\n双腿桥', '11%～17%†', '20%～28%', '31%～35%', '40%～58%', ''),
]
HD = ['类别', '动作', '肌肉节段\n（未注明为中部）', '低\n（0～20%）', '中\n（21%～40%）', '高\n（41%～60%）', '很高\n（>60%）']
CW = [90, 250, 150, 170, 180, 180, 160]


def table(rows, title, note):
    W = sum(CW) + 40; f = font(24); fh = font(24); lh = 34
    hh = 2 * lh + 20; H = 100 + hh + sum(max(len(c.split('\n')) for c in r) * lh + 20 for r in rows) + 140
    im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(34), fill='white')
    y = 100; dr.rectangle([20, y, W - 20, y + hh], fill=LT); x = 20
    for c, w in zip(HD, CW):
        for i, l in enumerate(c.split('\n')): ctext(dr, x + w / 2, y + 10 + i * lh, l, fh, TEAL)
        x += w
    y += hh
    for k, r in enumerate(rows):
        n = max(len(c.split('\n')) for c in r); rh = n * lh + 20
        if k % 2: dr.rectangle([20, y, W - 20, y + rh], fill=(248, 249, 250))
        x = 20
        for j, (c, w) in enumerate(zip(r, CW)):
            for i, l in enumerate(c.split('\n')):
                ctext(dr, x + w / 2, y + 10 + i * lh, l, font(24) if j else font(26), INK if j else TEAL)
            x += w
        y += rh; dr.line([20, y, W - 20, y], fill=(200, 205, 210), width=1)
    para(dr, 24, y + 16, note, 22, W - 48, fill=GREY, gap=8)
    return im


NOTE = '外旋、内旋、后伸、外展、内收指动作中附加的髋部动作；% MVIC 为最大自主等长收缩的百分比。各列数值按原文排版的顺序照录，原文未与动作逐行对齐；“R”原文未作解释。'
save(table(T1[:2], '原文表 1（上）  各练习的臀中肌分段平均激活水平（% MVIC）', NOTE + '*原文误拼为 Claim。'), 9)
save(table(T1[2:], '原文表 1（下）  各练习的臀中肌分段平均激活水平（% MVIC）', NOTE + '†原文该数值排在“肌肉节段”一栏。'), 10)

# 封面：原文图 3 单腿桥照片裁成 900:383
c = raw(98).crop((818, 210, 1492, 210 + round(674 * 383 / 900))).resize((900, 383), Image.LANCZOS)
c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
