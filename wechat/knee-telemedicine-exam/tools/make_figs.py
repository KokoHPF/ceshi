#!/usr/bin/env python3
"""Vomer 等 2023 膝关节远程医疗检查：首图中文标题卡；原文图 1～10 照片直接使用（图内只有 A/B/C 分图字母和箭头）并配中文图注；
检查流程与转诊红旗整理为中文卡片。表 1、表 2 在正文中以中文表格呈现。
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

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '操作指南 · 《Cureus》2023', font=font(32), fill=TEAL)
dr.text((70, 150), '膝关节的远程医疗检查', font=font(64), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 335), 'Vomer RP II, York E, Rayghan LS, Jethwa T, Montero DP, Nguyen CQ, Pujalte GGA.', font=font(26), fill=GREY)
dr.text((70, 380), 'Cureus. 2023;15(4):e37009', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 检查流程卡
save(card(1200, '远程膝关节检查：按体位一路做下来', [
    ('① 病史', '起病方式、疼痛部位、性质、程度、放射、随时间的变化、加重因素、已试过的处理；伴随的感觉、皮肤、温度改变，以及发热、寒战等全身症状。', LT, TEAL),
    ('② 视诊（站立，穿贴身运动服）', '双脚与肩同宽，前、侧、后三个方向看：腰椎前凸、髂前上棘和髂嵴高度、骨盆旋转；髌骨和腓骨头位置；估计 Q 角；让患者指出最痛点并用手指画出放射范围；看足跟和后足的旋前、旋后，胫骨与地面夹角。', OR, (200, 120, 0)),
    ('③ 触诊（患者自己摸）', '股四头肌腱、髂胫束、腓骨头、髌骨、内外侧关节面和关节线；描述大腿和小腿的肌肉量、皮温、感觉；摸腘窝有无囊肿或包块；做浮髌试验；摸远端脉搏、看有无迂曲静脉。', OR, (200, 120, 0)),
    ('④ 活动度（坐位，与健侧对比）', '坐在椅子上屈髋 90°：脚向内、向外转看胫骨内外旋；屈膝超过 90° 看是否疼痛，并记下髌骨开始痛的角度；伸膝可坐可站，坐位更方便。', GR, (0, 120, 60)),
    ('⑤ 力量、功能和步态', '徒手肌力改为抗重力动作：双腿深蹲（侧面和后面看，后面看有无髋偏移）→ 先健侧后患侧单腿蹲（看髋无力、动态膝外翻、疼痛）→ 双侧再单侧提踵（从后面看腓肠肌向心和离心收缩）。步态：看 Trendelenburg、足拍地、疼痛步态，以及步宽、支撑时间、步长。', PK, RED),
    ('⑥ 特殊检查（先站后坐）', '站立：患者自己给膝加内、外侧张开的力，查内、外侧副韧带；接着做 Thessaly 试验查半月板（站不稳可由家人扶或扶稳定物体）。然后坐下，侧对镜头做髌骨和髂胫束检查。', (240, 240, 248), (90, 70, 170)),
]), 2)

CAP = {
    97: '原文图 1  关节线触诊：患者坐位，用手指按压股骨与胫骨之间的关节线。原文图注认为诱发疼痛提示骨关节炎、髌腱炎或近端胫腓关节损伤',
    107: '原文图 2  主动屈伸膝：A 侧面拍摄，估计膝关节活动度；B 伸膝应有 0°～15°，伸不全提示腘绳肌受限；C 屈膝应约 120°～140°，屈曲受限可能来自股四头肌或髌骨病变',
    109: '原文图 3  J 征：A 伸膝时髌骨应走一条平滑的弧线；B 髌骨走出“J”形轨迹（J 征）提示髌骨不稳',
    111: '原文图 4  Trendelenburg 步态：A 正常步行时，髋外展肌稳定骨盆、保持水平；B 髋外展肌无力时，步行中骨盆不能保持水平，改变下肢动力链的受力，可能导致膝痛',
    124: '原文图 5  徒手深蹲：A 正面观，平稳下蹲；B 下蹲时膝内扣（箭头）并疼痛，提示内侧副韧带受累及患肢无力；C 后面观，平稳下蹲；D 髋偏移（箭头）提示偏离侧无力或活动受限',
    126: '原文图 6  改良内、外翻应力检查：A 中立站立；B 改良外翻应力，让患者把膝向内弯（箭头）；C 改良内翻应力，让患者把膝向外弯（箭头）。任一动作疼痛提示受力一侧的韧带受累',
    137: '原文图 7  改良 Noble 挤压试验：让患者用拇指按压髂胫束远端止点（A），然后伸膝（B）。疼痛提示髂胫束综合征或腓骨头功能障碍',
    139: '原文图 8  后沉征：患者仰卧，屈髋屈膝约 90°，足跟搁在纸箱上。两侧胫骨高度有明显差异即为后沉征，提示后交叉韧带受累',
    150: '原文图 9  改良 Thomas 试验：让患者坐在床边，把健侧膝抱向胸口后躺下。膝伸直提示股直肌受累；髋屈曲提示髂腰肌受累；小腿旋转提示髂胫束受限或髂胫束综合征；髋外展提示阔筋膜张肌受累',
    152: '原文图 10  改良 Thessaly 试验：A 患肢单腿站立，膝稍屈；让患者把肩膀转向左侧（B）和右侧（C）。转体时膝痛提示可能有半月板病变',
}
for n, x in enumerate([97, 107, 109, 111, 124, 126, 137, 139, 150, 152], start=3):
    save(capbox(raw(x), CAP[x]), n)

# 红旗卡
save(card(1200, '分诊：什么情况要尽快拍片或线下就诊', [
    ('尽早影像检查（低门槛）', '不能负重；严重的疼痛步态；膝关节肿胀、发红；髋部外伤；夜间痛；疼痛伴发热或寒战。', OR, (200, 120, 0)),
    ('立即急诊或线下评估', '直接钝器伤；高处坠落；其他体弱、病情复杂的患者。', PK, RED),
    ('问诊中的其他警示', '足部或小腿脉搏减弱（腘动脉损伤）、感觉减退（胫神经或腓总神经）；擦伤、新伤口、近期手术或局部红肿热加全身症状（化脓性关节炎、痛风、假痛风、蜂窝织炎）；明显畸形或重大外伤（骨折）；仪表盘损伤（后交叉韧带）；无明确外伤的青少年膝痛（警惕股骨头骨骺滑脱）。', LT, TEAL),
]), 13)

# 封面：原文图 10 改良 Thessaly 试验
c = raw(152); k = 900 / c.width; c = c.resize((900, round(c.height * k)), Image.LANCZOS)
c = c.crop((0, 0, 900, min(383, c.height)))
if c.height < 383:
    c = raw(150); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS); y0 = round(c.height * .15); c = c.crop((0, y0, 900, y0 + 383))
c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
