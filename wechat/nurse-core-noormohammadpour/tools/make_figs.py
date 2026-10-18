#!/usr/bin/env python3
"""Noormohammadpour 2018 护士慢性腰痛多阶段核心稳定训练：首图为原文标题区；附录 1 动作照片按周拼图并加中文动作名；
图 1 流程图中文重绘。照片中人脸原文已模糊。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import io
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); RED = (190, 40, 50); TEAL = (0, 110, 130)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def raw(x):
    return Image.open(io.BytesIO(d.extract_image(x)['image'])).convert('RGB')


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


# 每周 4 个动作：(名称, [图像 xref])；None 表示原文无图
WEEKS = [
    ('第 1 周：学会收缩（静态）', [('① 屈膝仰卧收腹', [131]), ('② 四点跪收腹 + 腰背肌收缩', [129]),
                          ('③ 坐球保持平衡 + 收缩', [130]), ('④ 坐球单腿抬起', [124])]),
    ('第 2 周：带进日常', [('① 收缩状态下步行 20 分钟', [123]), ('② 日常活动中保持收缩', None),
                     ('③ 坐球单臂上举', [126]), ('④ 坐球双臂上举', [125])]),
    ('第 3 周：臀桥与对角', [('① 臀桥', [121]), ('② 臀桥 + 单腿伸膝', [120]),
                      ('③ 坐球对侧手脚抬起', [122]), ('④ 坐球同侧手脚抬起', [128])]),
    ('第 4 周：鸟狗、侧桥与骨盆控制', [('① 鸟狗式', [127]), ('② 侧桥（伸膝）', [150]),
                            ('③ 坐球骨盆侧倾与画圈', [148, 149]), ('④ 坐球骨盆前后倾', [140, 139])]),
    ('第 5 周：仰卧对角与球上桥', [('① 仰卧对侧手脚抬起', [142]), ('② 90-90 仰卧对侧肘碰膝', [141]),
                          ('③ 球上肩桥（身体平行地面）', [137]), ('④ 球上肩桥 + 举臂左右摆', [136])]),
    ('第 6 周：俯卧与球上俯身', [('① 俯卧头腿同时抬起', [138]), ('② 90-90 仰卧双腿左右转', [144, 143]),
                          ('③ 俯卧球上伸展（脚抵墙）', [146]), ('④ 俯卧球上对侧手脚抬起', [145])]),
    ('第 7 周：站立位', [('① 单腿站立', [178]), ('② 单腿站立 + 屈膝前够', [176]),
                    ('③ 背靠球靠墙微蹲', [177, 171]), ('④ 双脚放球上臀桥', [170, 173])]),
    ('第 8 周：弓步与球上支撑', [('① 后撤弓步', [172]), ('② 后撤弓步 + 抬腿前够', [168]),
                          ('③ 球上侧桥', [167, 169]), ('④ 双脚放球上俯卧撑', [175, 174])]),
]

save(Image.open(io.BytesIO(d[0].get_pixmap(dpi=200, clip=pymupdf.Rect(60, 84, 540, 198)).tobytes('png'))), 1)

CW, CH = 610, 330
for k, (ttl, items) in enumerate(WEEKS):
    c = Image.new('RGB', (2 * CW + 60, 100 + 2 * (CH + 76)), 'white'); dr = ImageDraw.Draw(c)
    dr.rectangle([0, 0, c.width, 76], fill=TEAL); dr.text((30, 16), ttl, font=font(42), fill='white')
    for i, (name, xs) in enumerate(items):
        gx, gy = 30 + (i % 2) * CW, 100 + (i // 2) * (CH + 76)
        dr.text((gx, gy), name, font=font(32), fill=INK)
        top = gy + 50
        if xs is None:
            dr.rounded_rectangle([gx + 20, top, gx + CW - 30, top + CH - 20], 20, fill=(236, 244, 246))
            ctext(dr, gx + CW / 2 - 5, top + CH / 2 - 60, '原文无图', font(30), GREY)
            ctext(dr, gx + CW / 2 - 5, top + CH / 2 - 10, '走路、站立、搬东西时', font(28), GREY)
            ctext(dr, gx + CW / 2 - 5, top + CH / 2 + 30, '都保持腹部微收', font(28), GREY)
            continue
        ims = [raw(x) for x in xs]
        if len(ims) == 2 and ims[0].width > ims[0].height * 1.3:
            h = (CH - 30) // 2; ims = [m.resize((round(m.width * h / m.height), h), Image.LANCZOS) for m in ims]
            w = max(m.width for m in ims); s = min(1, (CW - 40) / w)
            ims = [m.resize((round(m.width * s), round(m.height * s)), Image.LANCZOS) for m in ims]
            y = top
            for m in ims: c.paste(m, (gx + (CW - 20 - m.width) // 2, y)); y += m.height + 8
        else:
            H = CH - 20; ims = [m.resize((round(m.width * H / m.height), H), Image.LANCZOS) for m in ims]
            tw = sum(m.width for m in ims) + 10 * (len(ims) - 1); s = min(1, (CW - 40) / tw)
            ims = [m.resize((round(m.width * s), round(m.height * s)), Image.LANCZOS) for m in ims]
            x = gx + (CW - 20 - round(tw * s)) // 2
            for m in ims: c.paste(m, (x, top)); x += m.width + 10
    save(c, 2 + k)

# 流程图
W, H = 1300, 1060; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def box(x0, y0, x1, y1, lines, fill='white', fs=28):
    dr.rectangle([x0, y0, x1, y1], fill=fill, outline=(90, 90, 90), width=3)
    yy = (y0 + y1 - len(lines) * (fs + 12)) / 2 + 4
    for l in lines: dr.text((x0 + 20, yy), l, font=font(fs), fill=INK); yy += fs + 12


def ar(x, a, b):
    dr.line([x, a, x, b], fill=(90, 90, 90), width=4); dr.polygon([(x, b + 3), (x - 11, b - 17), (x + 11, b - 17)], fill=(90, 90, 90))


for t, y in [('入组', 40), ('分配', 330), ('随访', 560), ('分析', 900)]:
    dr.rounded_rectangle([20, y, 120, y + 60], 10, fill=(200, 220, 235)); ctext(dr, 70, y + 14, t, font(30))
box(400, 30, 800, 100, ['评估是否符合条件（50 人）'])
box(820, 110, 1280, 230, ['排除 14 人', '　不符合纳入标准 12 人', '　拒绝参加 2 人'])
ar(600, 100, 258); dr.line([600, 170, 818, 170], fill=(90, 90, 90), width=4)
box(450, 260, 750, 320, ['随机分组（36 人）'])
dr.line([600, 320, 600, 350], fill=(90, 90, 90), width=4); dr.line([340, 350, 900, 350], fill=(90, 90, 90), width=4)
ar(340, 350, 398); ar(900, 350, 398)
box(150, 400, 560, 500, ['干预组 18 人', '　均接受干预'])
box(690, 400, 1150, 500, ['等待名单（对照组）18 人', '　均按分组执行'])
ar(340, 500, 558); ar(900, 500, 558)
box(130, 560, 590, 860, ['失访 8 人', '　怀孕 2 人', '　搬离本市 2 人', '　工作排班冲突', '　　无法参加训练 4 人'])
box(670, 560, 1170, 860, ['失访 8 人', '　退休 2 人', '　自行退出、', '　　寻求其他治疗 6 人'])
ar(340, 860, 898); ar(900, 860, 898)
box(200, 900, 520, 980, ['纳入分析 10 人']); box(760, 900, 1080, 980, ['纳入分析 10 人'])
save(im, 10)

# 封面
cv = Image.new('RGB', (900, 383), 'white'); dr = ImageDraw.Draw(cv)
x = 520
for xr in [127, 136]:
    m = raw(xr); m = m.resize((round(m.width * 185 / m.height), 185), Image.LANCZOS)
    m = m.crop((0, 0, min(m.width, 370), 185)); cv.paste(m, (x, 6 + (xr == 136) * 192))
dr.text((32, 46), '护士腰痛', font=font(70), fill=INK)
dr.text((32, 146), '8 周核心稳定训练', font=font(46), fill=TEAL)
dr.text((32, 220), '每周 4 个动作，地面 + 瑞士球', font=font(28), fill=RED)
dr.text((32, 320), 'Asian Spine J 2018 · 随机对照试验', font=font(22), fill=GREY)
cv.save(f'{OUT}/cover.jpg', quality=92)
