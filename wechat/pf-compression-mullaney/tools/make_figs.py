#!/usr/bin/env python3
"""Mullaney、Fukunaga 2016 髌股关节压迫问题：首图中文标题卡；原文图 1～6 照片加中文说明（人脸、墙上海报、
测斜仪屏幕、鞋标已模糊）；屈膝角度与髌股压力示意、检查→干预方法卡为编者根据原文绘制；
Tyler 2006 三项指标恢复数与成功率按原文数字重绘。
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


def blur(im, boxes, r=14):
    s = im.width / 1000
    for b0 in boxes:
        b = tuple(int(v * s) for v in b0); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * s)), b[:2])
    return im


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


# 照片：人脸、海报、测斜仪屏幕、鞋标模糊（坐标按 1000 宽）
P = {7: raw(7),
     14: blur(raw(14), [(30, 580, 190, 730), (850, 400, 1000, 700), (520, 650, 640, 712)]),
     15: blur(raw(15), [(0, 650, 175, 790), (745, 175, 915, 375)]),
     19: blur(raw(19), [(375, 95, 610, 315), (0, 1020, 80, 1100)]),
     20: blur(raw(20), [(445, 15, 605, 205), (0, 355, 35, 505), (370, 335, 480, 388)]),
     24: blur(raw(24), [(435, 45, 585, 215), (95, 385, 205, 475), (50, 30, 245, 315), (680, 170, 770, 270)])}

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床述评 · 《国际运动物理治疗杂志》2016', font=font(32), fill=TEAL)
for i, t in enumerate(['膝前痛、髌骨被“压”着痛，', '先查哪几处紧？']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '髌股关节压迫问题：屈膝角度、柔韧性检查、松动、筋膜和髋力量', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Mullaney MJ, Fukunaga T. IJSPT 2016;11(6):891-902', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1 髌骨内侧面触诊
save(titled(capbox(P[7], '先把髌骨往内推，再摸髌骨下面的内侧关节面；外侧面同理往外推。按压痛常见于髌股痛患者（71%～75%）', 800),
            '原文图 1　触诊髌骨内侧关节面', 800), 2)

# 屈膝角度与髌股压力
W = 1200; im = Image.new('RGB', (W, 820), 'white'); dr = ImageDraw.Draw(im)
X0, X1 = 90, 1110; px = lambda d: X0 + (X1 - X0) * d / 100
bands = [(0, 30, LT, '0°～30°', '髌骨还没进滑车沟，靠软组织稳住：内侧髌股韧带是阻止髌骨外移的主力'),
         (20, 30, None, '', ''),
         (30, 60, GR, '30°～60°', '髌骨嵌进滑车沟，骨性稳定增加；接触压力上升，接触区从髌骨下端移向上端'),
         (60, 90, PK, '60°～90°', '股四头肌腱和髌腱向后压的力越来越大，关节反作用力最高：上楼约 60°，靠墙蹲 80°～90°')]
dr.rounded_rectangle([X0, 60, X1, 140], 12, fill=(235, 235, 235))
for lo, hi, c, t, _ in bands:
    if c: dr.rectangle([px(lo), 60, px(hi), 140], fill=c); ctext(dr, (px(lo) + px(hi)) / 2, 84, t, font(30), TEAL)
for d in range(0, 101, 10):
    dr.line([px(d), 142, px(d), 156], fill=GREY, width=2); ctext(dr, px(d), 160, f'{d}°', font(22), GREY)
dr.text((X0, 14), '屈膝角度 →', font=font(26), fill=GREY)
y = 220
for lo, hi, c, t, s in bands:
    if not c: continue
    dr.rounded_rectangle([X0, y, X1, y + 160], 12, fill=c)
    dr.text((X0 + 24, y + 16), t, font=font(32), fill=TEAL); para(dr, X0 + 24, y + 66, s, 27, X1 - X0 - 48)
    y += 176
para(dr, X0, y + 6, '作者据此认为 60°～90° 的姿势和动作压力最大，检查和训练时要特别留意', 26, X1 - X0, fill=RED)
save(titled(im, '屈膝多少度时髌股关节压得最狠（编者根据原文整理）'), 3)

# 检查：Thomas、Ober、仰卧交叉
t1 = pair(P[14], P[15], '原文图 2　改良 Thomas 试验：对侧腿抱紧让骨盆后倾，用量角器或电子水平仪量髋角，同时量膝角看股直肌',
          '原文图 3　Thomas 体位直接变成髂腰肌牵伸，再屈膝可同时拉股直肌')
t2 = pair(P[20], P[24], '原文图 5　Ober 试验：侧卧、下面的腿屈髋屈膝并抱住床沿，被测腿外展后伸再自然下落，测斜仪放大腿远端',
          '原文图 6　仰卧交叉试验：屈髋约 70° 后内收到有阻力，查髂胫束后部；骨盆不能跟着侧倾')
save(board([t1, t2], '柔韧性怎么查：Thomas 试验和 Ober 试验'), 4)

# 半跪髋屈肌牵伸
save(titled(capbox(P[19], '原文图 4　半跪髋屈肌牵伸：躯干保持直立、腹肌适度收紧防止腰过度前凸，身体慢慢前移到感到前方牵拉', 860),
            '居家牵伸：半跪髋屈肌拉伸', 860), 5)

# Tyler 2006 成功率
fig, ax = plt.subplots(figsize=(12, 6.4), dpi=110)
labs = ['三项都恢复', '恢复两项', '只恢复一项']; vals = [93, 75, 27]
bars = ax.bar(labs, vals, color=['#2a7f62', '#4c8fbf', '#c0392b'], width=0.55)
for bb, v in zip(bars, vals):
    ax.text(bb.get_x() + bb.get_width() / 2, v + 2, f'{v}%', ha='center', fontsize=22, fontweight='bold')
ax.set_ylim(0, 108); ax.set_ylabel('治疗成功率（%）', fontsize=16); ax.tick_params(labelsize=16)
ax.spines[['top', 'right']].set_visible(False)
fig.text(0.5, 0.015, '三项：Ober 试验两侧一致、Thomas 试验两侧一致、手持测力计测屈髋力量提高 > 20%（数字引自原文对 Tyler 2006 的转述）',
         ha='center', fontsize=12, color='#666')
fig.tight_layout(rect=(0, 0.05, 1, 1)); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(Image.open(buf).convert('RGB'), 'Tyler 2006：髋的三项指标恢复得越全，效果越好', 1200), 6)

# 检查 → 干预 方法卡
W = 1200
rows = [('髋屈肌、股四头肌紧', '改良 Thomas 试验（信度高）、Ely 试验', 'Thomas 体位牵伸、半跪髋屈肌牵伸、俯卧股四头肌牵伸', LT),
        ('阔筋膜张肌、髂胫束紧', 'Ober 试验（髂胫束前部）、仰卧交叉试验（后部，无信效度数据）', 'Ober 体位治疗师辅助牵伸、仰卧交叉用带子自我牵伸、站立交叉腿侧屈', OR),
        ('腘绳肌、腓肠肌紧', '直腿抬高、90/90 伸膝；Silfverskiöld 试验（屈膝、伸膝背伸差 ≥ 10° 提示腓肠肌挛缩）', '带子直腿抬高牵伸，可加收缩—放松；站立腓肠肌牵伸，别让脚外展', GR),
        ('髌骨活动度差', '伸膝位查上下内外滑动、内外倾斜、旋转；常见内倾 + 内滑同时受限', '只松受限方向；静态或摆动手法，可教患者自我松动', PK),
        ('筋膜受限、触发点', '触诊紧张带里的压痛结节（评估者间信度中等）', '按压、牵伸 + 针对性训练；泡沫轴、器械辅助软组织松动', PU),
        ('髋和下肢无力', '屈髋、外展、外旋力量（手持测力计）', '先减压、改善软组织，再加髋外展、外旋、屈髋力量训练', (240, 240, 240))]
hs = [max(para_h(a, 26, 280), para_h(b, 24, 380), para_h(c, 24, 380)) + 40 for a, b, c, _ in rows]
im = Image.new('RGB', (W, sum(hs) + 10 * len(rows) + 60), 'white'); dr = ImageDraw.Draw(im)
for x, t in ((40, '问题'), (350, '怎么查'), (760, '怎么处理')): dr.text((x, 10), t, font=font(28), fill=GREY)
y = 56
for (a, b, c, bg), hh in zip(rows, hs):
    dr.rounded_rectangle([20, y, W - 20, y + hh], 12, fill=bg)
    para(dr, 40, y + 18, a, 26, 280, fill=TEAL); para(dr, 350, y + 20, b, 24, 380); para(dr, 760, y + 20, c, 24, 410, fill=GREY)
    y += hh + 10
save(titled(im, '先找出哪里出了问题，再对症处理（编者根据原文整理）'), 7)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 60), '髌股关节压迫问题', font=font(40), fill=TEAL)
dr.text((50, 130), '膝前痛，', font=font(64), fill=INK)
dr.text((50, 220), '先查哪几处紧？', font=font(64), fill=INK)
dr.text((50, 318), 'Thomas · Ober · 髌骨松动 · 髋力量', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
