#!/usr/bin/env python3
"""Duru 等 2026 肩袖肉毒毒素体表定位注射：首图中文标题卡、原文图 1～9（图中英文已原位改成中文）配中文图注、
编者整理的注射流程卡、封面。
图中文字：先跑 skills/paper-to-xhs-cards/scripts/extract_figures.py 和 relabel.py（labels.json / fixes.json 在本目录），
x63 分两遍（三角肌结节大字一遍、方位小字一遍），得到 work/zh/*.zh.jpg。
用法：python3 make_figs.py <work 目录> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFont

WORK, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
zh = lambda x: Image.open(f'{WORK}/zh/x{x}.zh.jpg').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t


def card(W, title, blocks):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '尸体研究 · 《Clinical Anatomy》2026', font=font(32), fill=TEAL)
dr.text((70, 140), '一种按患者个体定制的体表标志定位法：', font=font(54), fill=INK)
dr.text((70, 215), '肩袖肌内注射肉毒毒素的尸体研究', font=font(54), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Duru DO, Lee DKR, Jarvis GE, Kang N, Chaudhury S, Brassett C.', font=font(26), fill=GREY)
dr.text((70, 405), 'Clin Anat. 2026;39:912-922. doi:10.1002/ca.70068', font=font(28), fill=GREY)
dr.text((70, 450), '剑桥大学人体解剖中心 · 剑桥大学医院创伤骨科', font=font(26), fill=GREY)
dr.text((70, 540), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

CAP = [
    (23, '原文图 1  六个骨性标志（右肩后面观）：上角、下角、肩胛冈根部、三角肌结节、肩峰外侧缘（肩峰外缘中点，与肩胛冈轴线对齐）、肩锁关节。都是形态稳定、体表能摸到的骨点'),
    (51, '原文图 2  三个肩胛骨尺寸（右肩胛骨后面观）：高度 h＝上角到下角；肩胛冈长度 s＝肩胛冈根部到肩峰外侧缘；宽度 w＝肩胛冈根部到关节盂后缘中点'),
    (52, '原文图 3  找运动点：A 翻开冈下肌，用大头针垂直于骨面穿过肩胛上神经运动支入肌处；B 把肌肉放回原位，针的位置就是运动点的原位'),
    (63, '原文图 4  从三角肌结节量到“平均运动点”（红点，几根针的等距中心）：A 冈上肌（上面观，翻开斜方肌），X＝内外方向，Z＝前后方向；B 冈下肌（后面观，翻开三角肌），X＝内外方向，Y＝上下方向'),
    (86, '原文图 5  拍摄装置：标本按板上的标记摆放（L 左肩、R 右肩），相机位置固定，保证每个标本拍摄条件一致'),
    (131, '原文图 6  冈上肌运动点的位置可由肩胛骨尺寸预测：A 高度、B 肩胛冈长度、C 宽度，与“上角向外”“肩胛冈根部向外”“三角肌结节向前”三个距离的散点图和回归线'),
    (148, '原文图 7  冈下肌运动点的位置可由肩胛骨尺寸预测：A 高度与“肩胛冈根部向外 / 向下”；B 肩胛冈长度、C 宽度与“肩峰外侧缘向内 / 向下”'),
    (158, '原文图 8  体表定位注射（右肩）：A 冈上肌，从肩胛冈根部向外量 x mm、从三角肌结节向前量 z mm，交点为注射靶点；B 冈下肌，从肩峰外侧缘向内量 x mm、向下量 y mm'),
    (167, '原文图 9  亚甲蓝验证（左肩）：按公式定位、注射 2.5 mL 0.25% 亚甲蓝后解剖，冈下肌和冈上肌的神经入肌处都被染料覆盖'),
]
for n, (x, c) in enumerate(CAP, start=2):
    save(capbox(zh(x), c), n)

# 注射流程卡（公式按原文表 4 / 表 5 核对后给出，见正文“原文里对不上的地方”）
save(card(1200, '体表定位注射：四步走（编者根据原文整理）', [
    ('① 量肩胛骨', '摸清上角、下角、肩胛冈根部、肩峰外侧缘，量出肩胛冈长度（作者首选，最好量）；高度和宽度也可以用，算出的位置几乎一样。', LT, TEAL),
    ('② 算冈上肌靶点（按原文表 4）', 'X＝0.6444×冈长－23.85：从肩胛冈根部向外量\nZ＝0.3595×冈长－29.76：从三角肌结节向前量\n例：冈长 140 mm → 向外约 66 mm、向前约 21 mm\n注意：原文方法部分把这两条公式写反了', OR, (200, 120, 0)),
    ('③ 算冈下肌靶点（从肩峰外侧缘出发）', 'X＝0.3666×S＋29.39：向内量\nY＝0.5230×S－7.837：向下量\n原文写 S＝冈长；编者核对发现这两条公式只有代入肩胛骨宽度才与实测均值和原文图 7 吻合（宽 108 mm → 向内约 69 mm、向下约 49 mm），代入冈长会偏大 12～17 mm', GR, (0, 120, 60)),
    ('④ 进针', '在皮肤上标出交点，25G 针垂直皮肤进针，抵到冈上窝或冈下窝骨面（有阻力）即到深度；验证时注入 2.5 mL。肌肉发达者要更深，体弱、老年患者要浅一些——深度原文没有研究', PK, RED),
]), 11)

# 封面：原文图 8
c = zh(158); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS); y0 = (c.height - 383) // 2
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
