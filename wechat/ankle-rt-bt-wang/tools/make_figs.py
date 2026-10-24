#!/usr/bin/env python3
"""Wang 等 2021 踝扭伤：抗阻训练与平衡训练对等速外翻肌力、动态平衡、单腿跳和 FAOS 的影响比较。
首图中文标题卡、原文图 1～3（paper-figure-zh 位图路线译成中文）、四项评估说明卡、临床要点卡、封面。
用法：python3 make_figs.py <work 目录> <输出目录> <字体>
work 目录需要：zh_p4_1.png、zh_p5_1.png、zh_p7_1.png（figtrans render 输出，300 dpi）"""
import sys
from PIL import Image, ImageDraw, ImageFont

WORK, OUT, F = sys.argv[1], sys.argv[2], sys.argv[3]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
op = lambda n: Image.open(f'{WORK}/{n}').convert('RGB')
def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        # 标点不放行首
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”': dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
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



def trim(im, pad=12):
    """裁掉四周白边"""
    g = im.convert('L').point(lambda v: 255 if v < 245 else 0); x0, y0, x1, y1 = g.getbbox()
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '非随机对照试验（按编号单双号分组）· 《Life》2021', font=font(32), fill=TEAL)
dr.text((70, 135), '复发性踝扭伤居家康复 6 周', font=font(54), fill=INK)
dr.text((70, 205), '抗阻训练与平衡训练效果比较', font=font(54), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Wang H, Yu H, Kim YH, Kan W.', font=font(26), fill=GREY)
dr.text((70, 390), 'Life (Basel). 2021;11(4):307. doi:10.3390/life11040307', font=font(28), fill=GREY)
dr.text((70, 435), '洛阳师范学院、北京体育大学、韩国江陵原州大学、兰州大学', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 原文图 1：去掉页眉横线
f1 = op('zh_p4_1.png'); f1 = trim(f1.crop((0, round(f1.height * 0.1), f1.width, f1.height)))
save(capbox(f1, '原文图 1（图中英文由编者译为中文）  A 抗阻训练：(a) 弹力带外翻 (b) 弹力带背屈 (c) 弹力带内翻 (d) 提踵；'
            'B 平衡训练：(a) BOSU 球单腿站 (b) TOGU 气垫单腿站 (c) BAPS 平衡板 (d) 动态平衡（原图把最后一格也标成了 c）'), 2)

save(capbox(trim(op('zh_p5_1.png')), '原文图 2（图中英文由编者译为中文）  A 等速肌力测试（HUMAC NORM），30°/s 和 120°/s 向心收缩测外翻峰力矩；'
            'B Y 平衡测试，单腿站在中间，另一脚向前、后内侧、后外侧三个方向尽量远推'), 3)

save(card(1200, '研究看的 4 类结局（编者整理）', [
    ('等速外翻肌力', '30°/s 和 120°/s 两种角速度，看患侧外翻峰力矩的绝对值（Nm）和相对体重的值（Nm/kg，图中以 % 表示）', LT, TEAL),
    ('Y 平衡测试（YBT）', '前向、后内侧、后外侧三个方向的最远距离（cm），综合得分 = 三方向之和 ÷（下肢长 × 3）× 100', GR, (0, 120, 60)),
    ('单腿跳测试', '单次跳远、三连跳远、交叉三连跳（左右跨过中线）的距离（cm），以及 6 米计时单腿跳（s）', OR, (200, 120, 0)),
    ('FAOS 足踝结局评分', '疼痛、其他症状、日常生活、运动娱乐、生活质量 5 个分量表，共 42 题，0～100 分，分越高越好', PK, RED),
    ('共同条件', '训练前和 6 周后各测一次，只分析患侧；先测健侧再测患侧', (240, 240, 240), GREY),
]), 4)

save(capbox(trim(op('zh_p7_1.png')), '原文图 3（图中英文由编者译为中文）  A 等速外翻肌力：(a) 30°/s 绝对值 (b) 30°/s 相对值 (c) 120°/s 绝对值 (d) 120°/s 相对值；'
            'B Y 平衡测试：(a) 前向 (b) 后内侧 (c) 后外侧 (d) 综合得分。小括号上的 * 表示组内前后差异显著，大括号上的 p 为时间 × 组别交互作用'), 5)

save(card(1200, '这篇研究落到临床（编者整理）', [
    ('能说的', '复发性踝扭伤的业余运动人群，居家做 6 周弹力带抗阻训练或平衡训练，外翻肌力、Y 平衡、单腿跳和 FAOS 都有改善；'
     '平衡组在后内侧、后外侧伸够距离、交叉跳和 FAOS 疼痛、运动、生活质量上改善更多', GR, (0, 120, 60)),
    ('不能说的', '不是随机分组，没有设盲，没有不训练的对照组，也没有随访再扭伤率；不能说平衡训练“更能预防复发”，'
     '也不能说它“更利于重返运动”', PK, RED),
    ('怎么用', '两种训练都值得做，不必二选一：弹力带外翻、背屈打底，单腿站、软垫、BAPS 板和动态平衡逐级进阶；'
     '要回到变向多的运动，平衡和变向跳要练够', LT, TEAL),
]), 6)

# 封面：原文图 1 下排（平衡训练）
c = f1.crop((0, round(f1.height * 0.53), f1.width, round(f1.height * 0.94)))
w = round(c.height * 900 / 383); x0 = (c.width - w) // 2
c.crop((x0, 0, x0 + w, c.height)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
