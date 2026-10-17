#!/usr/bin/env python3
"""曾文欣、万丽 2026 膝骨关节炎非手术治疗进展：原文无插图；首页标题区截图；表 1（各指南关节腔注射推荐）重绘为彩色对照图；封面为文字设计图。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); RED = (171, 25, 66)

d = pymupdf.open(PDF)
pix = d[0].get_pixmap(dpi=200, clip=pymupdf.Rect(40, 30, 555, 284))
Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(f'{OUT}/img01.jpg', quality=88)

# 表 1 重绘
G = ['OARSI 2019', 'AAOS 2021', 'ACR 2019', '中国指南 2024', 'AAC 2019']
D = ['皮质类固醇', '透明质酸', '富血小板血浆', '间充质干细胞']
V = [['推荐', '推荐', '未提及', '未提及'],
     ['推荐', '不推荐', '存在争议', '未提及'],
     ['推荐', '不推荐', '不推荐', '不推荐'],
     ['强推荐', '强推荐', '强推荐', '弱推荐'],
     ['推荐', '推荐', '中立', '不推荐']]
C = {'强推荐': (27, 120, 70), '推荐': (92, 170, 110), '弱推荐': (176, 214, 150), '中立': (240, 220, 150),
     '存在争议': (245, 190, 120), '不推荐': (205, 85, 80), '未提及': (225, 225, 225)}
W, H = 1600, 970; x0, y0, cw, ch = 330, 170, 312, 140
im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
t = '各指南对膝关节腔内常用注射剂的推荐意见'
dr.text((W / 2 - dr.textlength(t, font=font(46)) / 2, 40), t, font=font(46), fill=INK)
for j, n in enumerate(D):
    f = font(34); dr.text((x0 + j * cw + cw / 2 - dr.textlength(n, font=f) / 2, y0 - 55), n, font=f, fill=INK)
for i, g in enumerate(G):
    f = font(34); dr.text((x0 - 20 - dr.textlength(g, font=f), y0 + i * ch + ch / 2 - 18), g, font=f, fill=INK)
    for j in range(4):
        v = V[i][j]; X, Y = x0 + j * cw, y0 + i * ch
        dr.rounded_rectangle([X + 6, Y + 6, X + cw - 6, Y + ch - 6], 14, fill=C[v])
        tc = 'white' if v in ('强推荐', '推荐', '不推荐') else INK
        f = font(40); dr.text((X + cw / 2 - dr.textlength(v, font=f) / 2, Y + ch / 2 - 22), v, font=f, fill=tc)
note = 'OARSI：国际骨关节炎研究学会；AAOS：美国骨科医师学会；ACR：美国风湿病学会；AAC：加拿大关节镜协会'
dr.text((60, H - 70), note, font=font(26), fill=(110, 110, 110))
im.save(f'{OUT}/img02.jpg', quality=90)

# 封面
cv = Image.new('RGB', (900, 383), (245, 240, 232)); dr = ImageDraw.Draw(cv)
dr.rectangle([0, 0, 900, 70], fill=RED)
dr.text((40, 14), '中华疼痛学杂志 2026 · 综述精读', font=font(34), fill='white')
dr.text((40, 110), '膝骨关节炎', font=font(86), fill=INK)
dr.text((40, 215), '非手术治疗进展', font=font(64), fill=RED)
tags = ['减重', '运动', '药物', '注射', '中医', '射频']
x = 40
for tg in tags:
    w = dr.textlength(tg, font=font(30)) + 30
    dr.rounded_rectangle([x, 310, x + w, 358], 22, fill=(255, 255, 255), outline=RED, width=2)
    dr.text((x + 15, 317), tg, font=font(30), fill=RED); x += w + 16
cv.save(f'{OUT}/cover.jpg', quality=92)
