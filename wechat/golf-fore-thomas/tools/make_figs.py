#!/usr/bin/env python3
"""Thomas & Wilk 2023 高尔夫球员 Fore / Fore+ / Advanced Fore+ 三级训练方案：首图中文标题卡；图 1～10 动作照片
模糊背景球衣姓名、器械品牌等英文后加中文标题与“起始/结束”标签；附录 1～3 三级方案对照卡。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def raw(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


def blur(im, boxes, base, r=14):
    """boxes 以宽度为 base 的显示坐标给出"""
    k = im.width / base
    for b in boxes:
        bb = tuple(int(v * k) for v in b)
        im.paste(im.crop(bb).filter(ImageFilter.GaussianBlur(r)), bb[:2])
    return im


def tag(dr, x, y, t, fs=56):
    f = font(fs); w = dr.textlength(t, font=f)
    dr.rounded_rectangle([x, y, x + w + 30, y + fs + 24], 12, fill=(255, 255, 255))
    dr.text((x + 15, y + 10), t, font=f, fill=INK)


def titled(ph, title, w=1300):
    ph = ph.resize((w, round(ph.height * w / ph.width)), Image.LANCZOS)
    out = Image.new('RGB', (w, ph.height + 96), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, w, 82], fill=TEAL); od.text((28, 16), title, font=font(46), fill='white')
    out.paste(ph, (0, 96)); return out


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '临床评论 · 《国际运动物理治疗杂志》（IJSPT）2023', font=font(32), fill=TEAL)
for i, t in enumerate(['高尔夫球员的三级训练方案：', 'Fore、Fore+、进阶 Fore+']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '活动度 · 力量与肌肉激活 · 核心 · 一根弹力带 + 自重就能练', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Thomas ZM, Wilk KE. IJSPT 2023;18(3):789-799', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，原文以 CC BY-NC 4.0 开放获取', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 照片 ----------
SPLIT = [  # (xref, 标题, 模糊框(显示坐标), 显示宽, 两个标签)
    (53, '原文图 1　半跪位胸椎旋转（Fore）', [(510, 0, 960, 235), (0, 0, 95, 340), (1570, 0, 2000, 250), (1025, 0, 1150, 355), (640, 610, 705, 670), (1695, 630, 1755, 690)], 2000, ('起始', '旋转')),
    (59, '原文图 2　深蹲位反向靠墙滑动（Fore）', [], 1000, ('起始', '上滑')),
    (60, '原文图 3　改良“举手投降”（Fore）', [(680, 30, 760, 60), (690, 0, 745, 12)], 800, ('侧面', '背面')),
    (69, '原文图 4　球杆辅助肩前屈（Fore+）', [(40, 30, 108, 98), (268, 60, 308, 112), (585, 78, 642, 138), (792, 105, 832, 152), (540, 40, 580, 60)], 1000, ('起始', '上举')),
    (75, '原文图 5　深蹲位 PNF D2 屈曲模式（Fore+）', [(100, 0, 168, 58), (108, 56, 168, 125), (390, 40, 435, 80), (620, 12, 690, 72), (628, 70, 690, 138), (895, 38, 940, 85)], 1000, ('起始', '结束')),
    (76, '原文图 6　深蹲位抗旋推（Fore+）', [], 1000, ('起始', '推出')),
    (82, '原文图 7　单侧划船伸手 + 侧向下台阶（进阶 Fore+）', [(150, 255, 215, 295), (555, 270, 630, 310), (355, 100, 390, 320), (750, 100, 785, 320)], 800, ('起始', '结束')),
    (90, '原文图 9　抗阻前弓步 + 旋转（进阶 Fore+）', [(250, 0, 330, 60), (685, 0, 790, 70)], 800, ('起始', '结束')),
    (91, '原文图 10　鸟狗式 + 划船（进阶 Fore+）', [], 800, ('起始', '结束')),
]
NUM = {53: 2, 59: 3, 60: 4, 69: 5, 75: 6, 76: 7, 82: 8, 90: 10, 91: 11}
for x, title, boxes, base, (t1, t2) in SPLIT:
    ph = blur(raw(x), boxes, base); dr = ImageDraw.Draw(ph); fs = int(ph.width / 30)
    tag(dr, 20, ph.height - fs - 50, t1, fs); tag(dr, ph.width // 2 + 40, ph.height - fs - 50, t2, fs)
    save(titled(ph, title), NUM[x])
ph = raw(83); dr = ImageDraw.Draw(ph); fs = int(ph.width / 30)
tag(dr, 20, 20, '起始', fs); tag(dr, ph.width - fs * 3 - 60, ph.height - fs - 50, '结束', fs)
save(titled(ph, '原文图 8　瑞士球上高位划船接外旋（“W”，进阶 Fore+）'), 9)

# ---------- 三级方案对照卡 ----------
LV = [
    ('Fore（基础）', (225, 240, 230), {
        '活动度': ['靠墙水平内收牵伸', '球杆“绕世界”（顺/逆时针）', '半跪位胸椎旋转', '深蹲 + 旋转'],
        '力量/肌肉激活': ['分腿弓步低位划船 + 伸手', '深蹲位 PNF D1/D2 屈曲—伸展', '深蹲位反向靠墙滑动', '肩胛系列：俯卧 T、俯卧 W、改良“举手投降”', '臀桥（双腿、单腿）', '前弓步 + 旋转'],
        '核心': ['深蹲位抗旋推', '鸟狗式', '死虫式']}),
    ('Fore+（中级）', (250, 238, 210), {
        '活动度': ['＋墙角胸小肌牵伸', '靠墙水平内收牵伸', '＋球杆辅助肩前屈', '球杆“绕世界”', '＋跪姿屈髋肌牵伸', '半跪位胸椎旋转', '深蹲 + 旋转'],
        '力量/肌肉激活': ['分腿弓步低位划船 + 伸手', '＋深蹲位 0°/90° 外旋、内旋', '深蹲位 PNF D1/D2', '深蹲位反向靠墙滑动', '肩胛系列：俯卧 I、T、Y、W，改良“举手投降”', '臀桥（双腿、单腿）', '＋弹力带侧向走', '前弓步 + 旋转'],
        '核心': ['深蹲位抗旋推', '鸟狗式', '死虫式']}),
    ('进阶 Fore+（高级）', (250, 228, 228), {
        '活动度': ['墙角胸小肌牵伸', '靠墙水平内收牵伸', '球杆辅助肩前屈', '球杆“绕世界”', '后脚垫高的跪姿屈髋肌牵伸', '弹力带抗阻半跪胸椎旋转', '深蹲 + 旋转', '＋抗阻四点跪伸手 + 旋转'],
        '力量/肌肉激活': ['单侧划船伸手 + 侧向下台阶', '分腿弓步位 0°/90° 外旋、内旋', '分腿弓步位 PNF D1/D2', '弹力带反向靠墙滑动', '瑞士球上肩胛系列：俯卧 I、T、Y、W', '＋高位划船接外旋', '改良“举手投降”', '弹力带抗阻臀桥（双腿、单腿）', '弹力带侧向走', '＋单腿罗马尼亚硬拉接提膝', '抗阻前弓步 + 旋转'],
        '核心': ['分腿弓步位抗旋推 + 上举', '鸟狗式 + 划船', '弹力带死虫式']}),
]
W = 1100; im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, W, 96], fill=TEAL); dr.text((30, 22), '三级方案一览（每个动作 2 组 × 10 次，组间几乎不休息）', font=font(40), fill='white')
y = 116
for name, col, secs in LV:
    n = sum(len(v) for v in secs.values()); h = 90 + 60 * 3 + 44 * n
    dr.rounded_rectangle([20, y, W - 20, y + h], 16, fill=col)
    dr.text((44, y + 20), name, font=font(44), fill=INK); yy = y + 88
    for sec, items in secs.items():
        dr.text((50, yy), f'【{sec}】', font=font(34), fill=RED); yy += 52
        for it in items:
            dr.text((76, yy), '· ' + it, font=font(31), fill=INK); yy += 44
        yy += 8
    y += h + 20
ctext = None
dr.text((30, y), '注：“＋”为相比上一级新增的动作；同名动作在高一级中', font=font(28), fill=GREY)
dr.text((30, y + 40), '多改为分腿弓步位、加弹力带或放到瑞士球上。', font=font(28), fill=GREY)
save(im.crop((0, 0, W, y + 90)), 12)

# ---------- 封面 900×383 ----------
c = blur(raw(53), SPLIT[0][2], 2000); c = c.crop((c.width // 2, 0, c.width, c.height))
c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = int(c.height * 0.18); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
