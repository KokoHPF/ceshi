#!/usr/bin/env python3
"""Wilk 等 2012 过顶运动员肘关节康复：首图中文标题卡；原文图 1～9 直接使用并加中文标注；四阶段卡、非手术方案卡为编者绘制；
术后时间线图按原文正文数值绘制。
诊疗流程卡为编者绘制；旋转活动度变化图按原文表 2 和表 4 数值绘制。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
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


# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床综述 · 《运动健康》2012', font=font(32), fill=TEAL)
dr.text((70, 170), '过顶运动员的肘关节康复', font=font(64), fill=INK)
dr.line([70, 380, W - 70, 380], fill=(200, 205, 210), width=2)
dr.text((70, 410), 'Wilk KE, Macrina LC, Cain EL, Dugas JR, Andrews JR. Sports Health 2012;4(5):404-414', font=font(28), fill=GREY)
dr.text((70, 465), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

PH = {1: raw(87), 2: raw(90), 3: raw(92), 4: raw(93), 5: raw(95), 6: raw(96), 7: raw(97), 8: raw(98), 9: raw(37)}
LAB = {1: '图 1　低负荷长时间伸肘牵伸', 2: '图 2　居家伸肘牵伸支具（a、b 两种）', 3: '图 3　徒手抗阻：屈肘、屈腕旋前',
       4: '图 4　坐球满罐 + 持续保持', 5: '图 5　球上俯卧水平外展 + 持续保持', 6: '图 6　坐球 0° 外旋 + 节律稳定',
       7: '图 7　90°/90° 对墙抛球 + 末端节律稳定', 8: '图 8　腕屈肌翻球', 9: '图 9　术后铰链式肘支具'}


def row(nums, W=1200, gap=10):
    ims = [PH[n] for n in nums]; hh = 600
    ims = [m.resize((round(m.width * hh / m.height), hh), Image.LANCZOS) for m in ims]
    s = (W - gap * (len(ims) - 1)) / sum(m.width for m in ims)
    ims = [m.resize((round(m.width * s), round(hh * s)), Image.LANCZOS) for m in ims]
    h = ims[0].height; out = Image.new('RGB', (W, h + 52), 'white'); d = ImageDraw.Draw(out); x = 0
    for n, m in zip(nums, ims):
        out.paste(m, (x, 0)); f = font(26)
        while d.textlength(LAB[n], font=f) > m.width - 6: f = font(f.size - 1)
        ctext(d, x + m.width / 2, h + 10, LAB[n], f); x += m.width + gap
    return out


save(board([row([1]), row([2])], '第 1 阶段：先把伸肘找回来'), 3)
save(board([row([3])], '第 2 阶段：徒手抗阻与神经肌肉控制'), 4)
save(board([row([4, 5]), row([6])], '第 3 阶段：进阶投掷十项'), 5)
save(board([row([7, 8])], '第 3 阶段：增强式练习'), 6)
save(board([row([9])], '尺侧副韧带重建术后：铰链式支具防外翻'), 9)

# 四阶段卡
W = 1200
def card(title, items, n):
    im = Image.new('RGB', (W, 2600), 'white'); dr = ImageDraw.Draw(im); y = 10
    for h, t, bg, col in items:
        tmp = para(ImageDraw.Draw(Image.new('RGB', (W, 700))), 70, y + 70, t, 28, W - 130, gap=12)
        dr.rounded_rectangle([20, y, W - 20, tmp + 12], 14, fill=bg); dr.text((50, y + 16), h, font=font(33), fill=col)
        para(dr, 70, y + 70, t, 28, W - 130, gap=12); y = tmp + 28
    save(titled(im.crop((0, 0, W, y)), title), n)

card('四阶段总览（编者根据原文整理）', [
    ('第 1 阶段　即刻活动', '目标：减少制动影响、恢复无痛活动度（尤其伸肘）、消炎止痛、延缓萎缩。做法：主动辅助和被动活动度；Ⅰ、Ⅱ级松动止痛，症状减轻后进阶到Ⅲ、Ⅳ级；肱尺关节后向滑动帮助伸直；伸不直就做低负荷长时间牵伸（每次 15 分钟、每天 4 次，总末端时间 ≥ 60 分钟），必要时夜间戴支具；肘、腕次最大等长收缩；肩胛肌力训练；节律稳定练习', LT, TEAL),
    ('第 2 阶段　中期', '进入条件：投掷所需活动度恢复、几乎不痛、屈伸肘肌力 ≥ 4 级。做法：Ⅲ、Ⅳ级松动；保持肩 90° 外展位外旋和内旋活动度；等张力量（先向心后离心）：屈伸肘、屈伸腕、前臂旋前旋后；肩袖后部和肩胛肌；投掷十项；本体感觉神经肌肉促进加节律稳定、徒手抗阻', OR, RED),
    ('第 3 阶段　进阶强化', '进入条件：肩内外旋总活动度无痛恢复、无压痛、力量达到健侧 70%。做法：屈肘强调离心控制；器械训练（卧推、坐姿划船、高位下拉）；进阶投掷十项（稳定球上持续保持）；侧卧外旋徒手抗阻 → 0° 外旋 → 90° 外旋；增强式：双手（胸前传、左右抛、过顶掷）→ 单手（90°/90° 抛、对蹦床内外旋抛、对墙拍球）→ 腕屈翻球、伸腕抓握', GR, (40, 120, 60)),
    ('第 4 阶段　重返运动', '进入条件：投掷活动度无痛、无压痛、等速测试满意（180°/s：投掷侧屈肘应比对侧强 10%～20%，伸肘强 5%～15%）、医生放行、增强式抛球无痛。做法：长传间歇投掷，从 45 英尺（约 13.7 米）进阶到 120～180 英尺（约 36.6～54.9 米）；投球前先做 1 组力量练习，投后再做 2 组；投手再进阶到投手丘投球：强度 50% → 75% → 90% → 100%，4～6 周；能以 ≥ 80% 强度无症状投 40～50 球后才加变化球', (240, 240, 240), INK)], 2)

card('常见损伤的非手术处理（编者根据原文整理）', [
    ('尺侧副韧带部分损伤', '早期只在 10°～100° 无痛范围内活动，可戴支具防外翻；肩、肘、腕等长练习；冰敷和消炎药 → 活动度每周增加 5°～10° → 6～7 周进入进阶强化（投掷十项、慢慢加增强式）→ 活动度全、肩肘肌力 5 级、动态稳定好后开始间歇投掷；症状反复就考虑手术', LT, TEAL),
    ('内上髁炎、屈肌-旋前肌腱病', '先分清是“炎症”还是“退变”。肌腱炎：先控制疼痛和炎症，再加牵伸和以离心为主的大负荷、低次数力量训练，屈伸腕时屈肘 30°～45° 减少内侧应力。肌腱退变：热疗、牵伸、离心、激光、横向按摩、干针、冲击波，必要时富血小板血浆', OR, RED),
    ('外翻伸直过载（后内侧撞击）', '冰敷、激光、离子导入止痛 → 活动度恢复后做动态稳定，重点是屈肘肌的离心力量，用来控制快速伸肘；检查投球动作，排除尺侧副韧带损伤', GR, (40, 120, 60)),
    ('肱骨小头剥脱性骨软骨炎', '只有 1 期（没有软骨下移位或骨折）才保守治疗：屈肘 90° 制动 3～6 周，同时肩、肘、腕每天 3～4 次活动度练习 → 症状消失后先等长、约 1 周后等张 → 高速、离心、增强式 → 间歇投掷', PK, RED),
    ('少棒肘（内上髁骨骺损伤）', '无撕脱：按尺侧副韧带非手术方案，加强核心、下肢和肩，牵伸肩内旋和水平内收；12～14 周内不做重负荷训练；休息 8～12 周后开始间歇投掷。轻度移位的撕脱：制动 7～14 天，第 8～12 周开始间歇投掷；明显移位需切开复位内固定', (240, 240, 240), INK)], 7)

# 术后时间线
fig, ax = plt.subplots(figsize=(13, 6.2), dpi=110)
rows = [('尺侧副韧带重建\n（8 字形移植法）', [(0, 1, '#9aa0a6', ''), (1, 6, '#4c8fbf', '活动度'), (6, 12, '#f39a2b', '投掷十项'), (12, 16, '#c0392b', '增强式'), (16, 39, '#6aa96a', '间歇投掷 → 投手丘 → 约 9 个月比赛')]),
        ('尺侧副韧带重建\n（对接法）', [(0, 6, '#4c8fbf', '支具 → 全范围'), (6, 10, '#f39a2b', '等张力量'), (10, 17, '#c0392b', '增强式、器械'), (17, 39, '#6aa96a', '约 4 个月间歇投掷 → 约 9 个月投球')]),
        ('尺神经前置', [(0, 1, '#9aa0a6', ''), (1, 4, '#4c8fbf', '活动度'), (4, 8, '#f39a2b', '投掷十项'), (8, 10, '#c0392b', '增强'), (10, 16, '#6aa96a', '间歇投掷 → 16 周比赛')]),
        ('鹰嘴后方\n骨赘切除', [(0, 2, '#9aa0a6', '等长'), (2, 6, '#4c8fbf', '等张'), (6, 10, '#f39a2b', '投掷十项'), (10, 12, '#6aa96a', '投掷')])]
for i, (name, segs) in enumerate(rows):
    for a, b, c, t in segs:
        ax.barh(i, b - a, left=a, color=c, edgecolor='white', height=0.6)
        if t: ax.text((a + b) / 2, i, t, ha='center', va='center', fontsize=11.5, color='white' if c != '#9aa0a6' else '#222')
ax.set_yticks(range(4)); ax.set_yticklabels([r[0] for r in rows], fontsize=12.5); ax.invert_yaxis()
ax.set_xlabel('术后周数', fontsize=14); ax.set_xticks([0, 4, 8, 12, 16, 20, 26, 32, 39]); ax.set_xlim(0, 40); ax.tick_params(axis='x', labelsize=12)
ax.spines[['top', 'right']].set_visible(False)
fig.text(0.5, 0.01, '按原文正文整理的大致时间点，各阶段实际有重叠，需按标准而非时间推进', ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.04, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), '四种肘关节术后康复的时间线（编者根据原文绘制）', 1320), 8)

c = PH[7]; h = round(c.width * 383 / 900); y0 = int(c.height * .08)
c.crop((0, y0, c.width, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
