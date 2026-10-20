#!/usr/bin/env python3
"""Short 等 2023 运动物理治疗中基于临床推理的手法治疗：首图中文标题卡；原文图 1 机制模型中文重绘；原文图 2 英文文字改为中文；
两个病例的处理流程卡为编者根据原文绘制。
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
dr.text((70, 60), '临床述评 · 《国际运动物理治疗杂志》2023', font=font(32), fill=TEAL)
dr.text((70, 150), '运动物理治疗中', font=font(58), fill=INK)
dr.text((70, 236), '基于临床推理的手法治疗', font=font(58), fill=INK)
dr.line([70, 380, W - 70, 380], fill=(200, 205, 210), width=2)
dr.text((70, 410), 'Short S, Tuttle M, Youngman D. IJSPT 2023;18(1):262-271', font=font(30), fill=GREY)
dr.text((70, 465), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1 机制模型中文重绘
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
def bx(x0, y0, x1, y1, t, fs=27, fill=(236, 236, 236), bold=True):
    dr.rounded_rectangle([x0, y0, x1, y1], 10, fill=fill, outline=(120, 120, 120), width=2)
    lines = t.split('\n'); lh = fs + 9; y = (y0 + y1) / 2 - lh * len(lines) / 2 + 3
    for l in lines: ctext(dr, (x0 + x1) / 2, y, l, font(fs), INK if bold else GREY); y += lh
def ln(a, b, both=False):
    dr.line([a, b], fill=(80, 80, 80), width=3)
    import math
    for p, q in ([(a, b)] + ([(b, a)] if both else [])):
        ang = math.atan2(q[1] - p[1], q[0] - p[0]); L = 14
        dr.polygon([q, (q[0] - L * math.cos(ang - .45), q[1] - L * math.sin(ang - .45)), (q[0] - L * math.cos(ang + .45), q[1] - L * math.sin(ang + .45))], fill=(80, 80, 80))
for (x0, x1, t, c) in [(0, 450, '区域 1：手法输入与情境', (210, 210, 210)), (460, 930, '区域 2：神经生理反应', (225, 225, 225)), (940, 1400, '区域 3：临床结局', (240, 240, 240))]:
    dr.rectangle([x0, 0, x1, 60], fill=c); ctext(dr, (x0 + x1) / 2, 14, t, font(30))
ln((80, 210), (80, 330), True); ln((80, 390), (80, 500), True); ln((250, 150), (250, 560), True)
ln((150, 360), (460, 360)); ln((400, 240), (520, 330)); ln((760, 360), (820, 360), True); ln((1080, 360), (1140, 360), True)
ln((1265, 390), (1265, 520), True); ln((330, 590), (460, 590), True); ln((610, 560), (610, 500), True); ln((760, 590), (860, 590), True)
ln((900, 620), (610, 830)); ln((960, 620), (935, 830)); ln((1040, 620), (1250, 830))
bx(170, 90, 330, 150, '治疗者'); bx(170, 165, 400, 215, '机械刺激'); bx(170, 215, 400, 265, '软组织、神经、关节', 23, (250, 250, 250), False)
bx(10, 90, 150, 210, '态度\n期望\n信念\n经验', 22, (250, 250, 250), False)
bx(10, 330, 150, 390, '情境')
bx(10, 500, 150, 690, '偏好\n期望\n信念\n情绪困扰\n既往经历', 22, (250, 250, 250), False)
bx(170, 560, 330, 620, '患者'); bx(200, 650, 340, 700, '组织'); bx(200, 700, 340, 800, '僵硬\n活动度\n张力', 22, (250, 250, 250), False)
bx(460, 330, 760, 390, '疼痛调节回路'); bx(500, 395, 760, 500, '体感诱发电位\nPET / 功能磁共振\n条件性疼痛调制', 22, (250, 250, 250), False)
bx(460, 560, 760, 620, '周围神经系统'); bx(500, 625, 760, 730, '细胞因子\n神经肽\n神经生长因子', 22, (250, 250, 250), False)
bx(820, 330, 1080, 390, '疼痛相关脑回路'); bx(860, 560, 1080, 620, '脊髓')
bx(1140, 330, 1390, 390, '疼痛抑制'); bx(1180, 395, 1390, 500, '痛敏感性 ↓\n疼痛抑制 ↑\n疼痛易化 ↓', 22, (250, 250, 250), False)
bx(1140, 520, 1390, 580, '临床结局'); bx(1160, 585, 1390, 760, '活动痛、静息痛\n情绪\n疲劳\n功能受干扰程度\n满意度', 22, (250, 250, 250), False)
bx(460, 830, 760, 890, '神经肌肉反应'); bx(460, 890, 760, 975, '运动神经元池、传入放电\n肌肉活动', 21, (250, 250, 250), False)
bx(790, 830, 1080, 890, '自主神经反应'); bx(790, 890, 1080, 975, '皮温、皮肤电导\n皮质醇、心率', 21, (250, 250, 250), False)
bx(1110, 830, 1390, 890, '时间总和')
save(titled(im, '原文图 1：手法治疗的多因素神经生理机制', 1200), 2)

# 图 2：英文改中文
f2 = relabel(raw(62), [((333, 200, 600, 300), '临床检查：找出症状复现、\n活动度、力量、爆发力、\n耐力和活动耐受方面的问题', 19, 'l'),
                       ((632, 346, 970, 450), '计划、排序并实施手法、\n运动和认知干预，改善症状、\n活动度、力量、爆发力、\n耐力和活动耐受', 19, 'l'),
                       ((333, 496, 580, 580), '观察评估干预效果，\n根据运动员的反应\n进阶、退阶或调整', 19, 'l'),
                       ((42, 347, 295, 412), '强化合适的手法和\n运动治疗，促进长期进展', 19, 'l')])
save(titled(f2, '原文图 2：手法治疗的临床推理反馈循环', 1200), 3)

# 病例卡
def case(title, rows, n, col):
    W = 1200; im = Image.new('RGB', (W, 1700), 'white'); dr = ImageDraw.Draw(im); y = 10
    for h, t, bg in rows:
        tmp = para(ImageDraw.Draw(Image.new('RGB', (W, 600))), 70, y + 70, t, 28, W - 130, gap=12)
        dr.rounded_rectangle([20, y, W - 20, tmp + 12], 14, fill=bg); dr.text((50, y + 16), h, font=font(33), fill=col)
        para(dr, 70, y + 70, t, 28, W - 130, gap=12); y = tmp + 28
    save(titled(im.crop((0, 0, W, y)), title), n)

case('病例 1：急性外侧踝扭伤（编者根据原文整理）', [
    ('情况', '扭伤后 72 小时，渥太华踝关节规则阴性，想 2 天内回场；中度肿胀和淤青，仰卧和负重背伸都受限，单腿蹲平衡差，跑步跛行，疼痛 7/10', (240, 240, 240)),
    ('第 1 次', '距骨前后向分级松动 → 仰卧背伸改善、负重背伸没改善 → 改做背伸动态关节松动，直到负重背伸接近对称 → 复测单腿蹲（痛和质量都改善）→ 试跑，疼痛降到 4/10 → 加离心内翻和跖屈力量、单腿平衡和下肢复合力量练习；宣教自然病程、早期负重和重返标准', LT),
    ('赛前复诊', '重复两种手法；单腿蹲背伸仍受限、活动痛 3/10 → 加距小腿关节和后足分离推扳 → 通过重返运动标准，戴半刚性护踝上场', OR),
    ('之后', '教弹力带自我动态松动（背伸）在训练前自己做；手法逐渐减少，只在疼痛需要时或训练后恢复时用；继续单腿平衡和力量训练，预防再扭伤和慢性不稳', GR)], 4, RED)
case('病例 2：急性腰痛（编者根据原文整理）', [
    ('情况', '篮球卡位时被对手压在背上，被迫负重屈曲加旋转；无神经根症状，椎旁肌张力高，前屈明显受限，后伸轻度受限，前屈回位时撑大腿起身，害怕弯腰', (240, 240, 240)),
    ('第 1 次', '椎旁软组织松解 → 后伸基本恢复、前屈仍害怕 → 疼痛节段腰椎中央后前向松动，从低级别开始按反应进阶 → 前屈疼痛减轻、更敢动 → 四点跪腰盆活动度练习 + 20 分钟不加重症状的有氧；宣教腰痛自然病程和良好预后；回家继续低强度有氧、活动度练习、热敷和后伸', LT),
    ('赛前 3 小时', '活动度基本恢复，但仍撑大腿起身、疼痛 3/10、怕身体对抗 → 解释推扳的神经生理机制并征得同意 → 侧卧腰椎推扳 → 立即复测前屈改善 → 加四点跪和闭链运动控制、力量练习 → 与队医等沟通后上场', OR),
    ('之后', '教模仿手法的自我活动度练习；和体能教练沟通，把近端躯干和下肢力量练习加入训练计划；手法只在症状加重时使用', GR)], 5, (40, 120, 60))

# 封面 900×383：图 2 中央
c = f2; h = round(c.width * 383 / 900); y0 = int(c.height * .27)
c.crop((0, y0, c.width, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
