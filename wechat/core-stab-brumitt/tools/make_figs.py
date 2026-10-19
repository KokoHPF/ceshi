#!/usr/bin/env python3
"""Brumitt 2013 核心稳定训练处方（上）：首图中文标题卡；局部肌 vs 整体肌两种思路对比卡、Richardson 三阶段进阶卡、
压力生物反馈三项测试卡、McGill 耐力比值标准卡、桥式测试时间图为编者中文绘制；原文图 1–7 照片加中文名拼图。
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
LT = (225, 240, 243); OR = (252, 240, 230)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(38), fill='white')
    out.paste(im, (0, 90)); return out


def photo(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


def wrap(dr, t, f, w):
    out, cur = [], ''
    for ch in t:
        if dr.textlength(cur + ch, font=f) > w: out.append(cur); cur = ch
        else: cur += ch
    return out + [cur] if cur else out


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    for l in wrap(dr, t, font(fs), w):
        dr.text((x, y), l, font=font(fs), fill=fill); y += fs + gap
    return y


def board(items, cols, TW, TH, title):
    rows = (len(items) + cols - 1) // cols
    im = Image.new('RGB', (cols * (TW + 10) + 10, rows * (TH + 70) + 10), 'white'); dr = ImageDraw.Draw(im)
    for k, (x, t) in enumerate(items):
        p = photo(x); s = min(TW / p.width, TH / p.height); p = p.resize((round(p.width * s), round(p.height * s)), Image.LANCZOS)
        x0 = 10 + (k % cols) * (TW + 10); y0 = 10 + (k // cols) * (TH + 70)
        dr.rounded_rectangle([x0, y0, x0 + TW, y0 + 56], 8, fill=LT)
        dr.text((x0 + 16, y0 + 10), t, font=font(32), fill=TEAL)
        im.paste(p, (x0 + (TW - p.width) // 2, y0 + 62))
    return titled(im, title)


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床综述 · 《运动健康》（Sports Health）2013', font=font(32), fill=TEAL)
for i, t in enumerate(['核心稳定训练处方（上）：', '先评估，再选路线']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '局部肌“腹部回缩” vs 整体肌“McGill 三大动作” · 7 项核心测试', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Brumitt J 等，Sports Health 2013;5(6):504-509', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 两种思路对比 ----------
W, H = 1400, 800; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
cols = [('局部肌思路（Richardson / Hodges）', LT, TEAL, [
    ('针对', '腹横肌、多裂肌（局部稳定肌）'),
    ('依据', '腰痛者腹横肌“提前收缩”延迟，由持续收缩变成爆发式；多裂肌萎缩、易疲劳'),
    ('关键动作', '腹部回缩（drawing-in）：只收深层，不动脊柱和骨盆'),
    ('评估', '压力生物反馈：四点跪 → 俯卧 → 仰卧屈膝滑腿'),
    ('训练', '低负荷等长 → 闭链负重控制 → 开链远端活动'),
    ('观点', '过早加入整体肌可能有害：增加脊柱压力，反而加重局部肌负担')]),
    ('整体肌思路（McGill）', OR, (190, 100, 40), [
    ('针对', '所有核心肌：竖脊肌、腰方肌、腹斜肌和腹直肌，也包括局部肌'),
    ('依据', '腰伤后所有肌肉都有激活延迟；每块肌肉的贡献随动作而变'),
    ('关键动作', '腹部支撑（bracing）：整圈绷紧，被认为比回缩更稳'),
    ('评估', '3 项耐力计时测试（伸肌、侧桥左右、屈肌）+ 比值'),
    ('训练', '“三大动作”：侧桥、鸟狗、卷腹 → 再进阶功能训练'),
    ('观点', '不可能只练腹横肌而不带动其他腹肌')])]
for c, (t, bg, col, rows) in enumerate(cols):
    x0 = 20 + c * 690; dr.rounded_rectangle([x0, 20, x0 + 670, H - 20], 16, fill=bg)
    dr.text((x0 + 24, 40), t, font=font(36), fill=col)
    y = 110
    for k, v in rows:
        dr.text((x0 + 24, y), k, font=font(28), fill=col)
        y = para(dr, x0 + 150, y, v, 28, 495) + 26
save(titled(im, '两条核心稳定康复路线（编者根据原文整理）'), 2)

# ---------- Richardson 三阶段 ----------
W, H = 1400, 700; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
st = [('第 1 阶段', '局部肌控制', ['腹部回缩 + 多裂肌', '共同收缩', '低负荷等长，用生物', '反馈监测代偿', '（俯卧、仰卧）']),
      ('第 2 阶段', '闭链节段控制', ['屈曲位和直立位的', '负重练习', '稳定面 → 不稳定面', '局部肌 + 负重肌', '一起工作']),
      ('第 3 阶段', '开链远端活动', ['非负重练习', '四肢远端在动', '躯干保持节段稳定', '暴露残留的', '局部肌缺陷'])]
for i, (a, b2, ls) in enumerate(st):
    x0 = 30 + i * 460
    dr.rounded_rectangle([x0, 30, x0 + 400, 140], 14, fill=TEAL)
    dr.text((x0 + 200 - dr.textlength(a, font=font(30)) / 2, 42), a, font=font(30), fill='white')
    dr.text((x0 + 200 - dr.textlength(b2, font=font(36)) / 2, 88), b2, font=font(36), fill='white')
    dr.rounded_rectangle([x0, 155, x0 + 400, 520], 14, fill=LT)
    for j, l in enumerate(ls): dr.text((x0 + 30, 180 + j * 64), l, font=font(32), fill=INK)
    if i < 2: dr.polygon([(x0 + 412, 270), (x0 + 448, 300), (x0 + 412, 330)], fill=TEAL)
dr.text((30, 548), '进阶条件：第 1 → 2 阶段需在“局部肌共同收缩测试”中表现正常', font=font(30), fill=INK)
dr.text((30, 600), '其余进阶没有量化标准，靠治疗师持续复测运动控制测试来判断', font=font(30), fill=RED)
save(titled(im, '局部肌思路的三阶段康复（编者根据原文绘制）'), 3)

# ---------- 压力生物反馈测试 ----------
W, H = 1400, 760; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
tests = [('① 四点跪', '无需设备', ['脊柱中立', '“腹壁往里收，脊柱骨盆不动，', '正常呼吸，保持 10 秒”', '反复练到熟练 → 进入俯卧']),
         ('② 俯卧', '气囊垫在腹下，肚脐居中', ['充气到 70 mmHg', '回缩后压力下降 6～10 mmHg', '每次保持 10 秒，做 10 次', '做不好可直接当练习']),
         ('③ 仰卧屈膝', '气囊垫在腰下（下缘平 S2）', ['充气到 40 mmHg', '回缩后压力约升 2～4 mmHg', '脚跟贴床面滑出伸腿', '压力保持不变 = 腰盆控制好'])]
for i, (a, b2, ls) in enumerate(tests):
    x0 = 20 + i * 460
    dr.rounded_rectangle([x0, 20, x0 + 440, 540], 16, fill=LT)
    dr.text((x0 + 26, 40), a, font=font(40), fill=TEAL)
    dr.text((x0 + 26, 100), b2, font=font(26), fill=GREY)
    for j, l in enumerate(ls):
        dr.text((x0 + 26, 170 + j * 70), l, font=font(29 if j else 34), fill=RED if (j == 0 or (j == 1 and i)) else INK)
    dr.text((x0 + 26, 475), '进阶：' + ['四点跪 → 俯卧', '俯卧 → 仰卧', '支撑滑腿 → 腿悬空伸直'][i], font=font(27), fill=GREY)
dr.text((40, 575), '压力生物反馈仪：可充气的小气囊连压力表，', font=font(30), fill=INK)
dr.text((40, 623), '用来看腹横肌收缩时腰腹有没有动、代偿', font=font(30), fill=INK)
dr.text((40, 695), '原文表 1，编者中文重排', font=font(24), fill=(150, 150, 150))
save(titled(im, '原文表 1　局部肌（腹横肌、多裂肌）运动控制测试'), 4)

# ---------- 照片：图 1 ----------
save(board([(35, '仰卧屈膝 + 压力生物反馈（腰下）')], 1, 900, 680, '原文图 1　腹部回缩测试：腰盆控制'), 5)

# ---------- 照片：McGill 耐力测试 ----------
save(board([(37, '背伸肌测试：起始位'), (38, '背伸肌测试：测试位'), (44, '侧桥（侧方肌群）测试'), (41, '屈肌耐力测试')],
           2, 680, 510, '原文图 2～5　McGill 核心耐力测试'), 6)

# ---------- 比值标准 ----------
W, H = 1400, 820; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
rs = [('屈肌 ÷ 背伸肌', '< 1.0', '屈肌不应比背伸肌撑得久'),
      ('侧桥 ÷ 背伸肌', '< 0.75', '侧桥不应超过背伸肌的 3/4'),
      ('左侧桥 vs 右侧桥', '差 < 0.05', '左右比值应在约 0.95～1.05')]
for i, (a, v, n) in enumerate(rs):
    y0 = 20 + i * 150
    dr.rounded_rectangle([20, y0, W - 20, y0 + 130], 14, fill=LT)
    dr.text((50, y0 + 38), a, font=font(40), fill=INK)
    dr.text((560, y0 + 30), v, font=font(52), fill=RED)
    dr.text((850, y0 + 46), n, font=font(28), fill=GREY)
dr.text((30, 490), '编者补充：McGill 1999 年健康年轻人参考值（秒，均值）', font=font(32), fill=TEAL)
hd = ['', '背伸肌', '屈肌', '右侧桥', '左侧桥']
rows = [hd, ['男', '161', '136', '95', '99'], ['女', '185', '134', '75', '78']]
for r, row in enumerate(rows):
    for c, t in enumerate(row):
        x = 60 + c * 260; y = 550 + r * 70
        dr.text((x, y), t, font=font(34 if r else 30), fill=GREY if r == 0 else INK)
dr.text((30, 770), '原文只给了比值标准，未给参考时间；表中数值引自 McGill SM 等，Arch Phys Med Rehabil 1999', font=font(22), fill=(150, 150, 150))
save(titled(im, 'McGill 耐力测试：看的是“比值”，不只是秒数'), 7)

# ---------- 桥式测试 ----------
bt = board([(43, '俯卧桥（平板支撑）测试'), (42, '仰卧桥测试')], 2, 680, 510, '原文图 6～7　桥式测试')
fig, ax = plt.subplots(figsize=(9, 4.6))
cats = ['俯卧桥', '仰卧桥']; no = [72.5, 170.4]; nsd = [32.6, 42.5]; yes = [28.3, 76.7]; ysd = [26.8, 48.9]
import numpy as np
x = np.arange(2)
ax.bar(x - 0.2, no, 0.38, yerr=nsd, capsize=5, color='#4f9fb0', label='无腰痛')
ax.bar(x + 0.2, yes, 0.38, yerr=ysd, capsize=5, color='#e9a07a', label='有腰痛')
for i in range(2):
    ax.text(i - 0.2, no[i] + nsd[i] + 4, f'{no[i]}', ha='center'); ax.text(i + 0.2, yes[i] + ysd[i] + 4, f'{yes[i]}', ha='center')
ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_ylabel('坚持时间（秒）'); ax.set_ylim(0, 245)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc='upper left')
b = BytesIO(); plt.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close()
ch = Image.open(b).convert('RGB'); ch = ch.resize((bt.width - 40, round(ch.height * (bt.width - 40) / ch.width)), Image.LANCZOS)
out = Image.new('RGB', (bt.width, bt.height + ch.height + 50), 'white'); out.paste(bt, (0, 0)); out.paste(ch, (20, bt.height + 10))
ImageDraw.Draw(out).text((30, out.height - 40), '均值 ± 标准差，数据为原文引用的 Schellenberg 2007 研究', font=font(24), fill=(150, 150, 150))
save(out, 8)

# ---------- 封面 ----------
c = photo(44); s = 900 / c.width; c = c.resize((900, round(c.height * s)), Image.LANCZOS)
top = max(0, (c.height - 383) // 2 + 40); c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
