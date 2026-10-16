#!/usr/bin/env python3
"""Dudek 2026 Haglund 术后康复：图 2 分期阶梯图中文重绘；图 1 背景海报、图 3 弹力带品牌字样模糊；封面取自图 1。
用法：python3 make_figs.py <素材目录（x01～x03.png、title.png）> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66); INK = (25, 25, 25)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def blur(im, boxes, r=12):
    for b in boxes:
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r)), b[:2])
    return im


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.width // 34))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    im.resize((W, round(im.height * W / im.width)), Image.LANCZOS).save(f'{OUT}/{name}', quality=88)


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

x1 = blur(X(1), [(360, 95, 570, 255), (960, 40, 1120, 230), (1660, 190, 1707, 300)])
save(badge(x1.copy(), '图1'), 'img02.jpg')
w, h = x1.size; ch = round(w * 383 / 900); y0 = h - ch
x1.crop((0, y0, w, h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)

# 图 2：重绘
W, H = 2000, 1150
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
ax0, ay1 = 230, 1010
d.line([(ax0, 70), (ax0, ay1), (W - 10, ay1)], fill=(40, 170, 140), width=8)
d.rectangle([0, 0, 215, 75], fill=(20, 160, 70)); d.text((22, 12), '健康', font=font(46), fill=INK)
lay = Image.new('RGBA', (700, 90), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((0, 0), '重返运动准备度', font=font(78), fill=INK)
lay = lay.rotate(90, expand=True); im.paste(lay, (100, 230), lay)
d.text((330, 40), '负荷管理', font=font(46), fill=INK)
LM = ['1. 外部负荷：日常活动需求、心肺负荷、力量训练耐受', '　 （可穿戴设备、GPS、计步器）', '2. 内部负荷：主观用力程度、心率、炎症、肿胀',
      '3. 主观状态：睡眠、压力、情绪、负荷后酸痛', '4. 客观测试标准']
for i, t in enumerate(LM):
    d.text((330, 110 + i * 52), t, font=font(36), fill=INK)
BOX = [((235, 850, 640, 1000), (0, 0, 0), '保护期 / 活动度', ['避免末端背屈', '逐步负重'], 'white'),
       ((555, 680, 1145, 845), (128, 92, 200), '耐力期', ['步态正常化', '双腿 → 单腿提踵耐力'], INK),
       ((865, 555, 1995, 672), (0, 176, 240), '力量与肥大期', ['下肢 LSI 恢复到 90%，发力超过体重，达到客观标准'], INK),
       ((1238, 368, 1995, 552), (31, 110, 190), '爆发力 A、B 期', ['A：跑跳前的爆发力训练', 'B：跑步进阶、交替敏捷、双腿 → 单腿增强式'], 'white'),
       ((1438, 212, 1995, 365), (255, 192, 0), '重返参与', ['早期非接触性参与'], INK),
       ((1588, 78, 1995, 209), (20, 176, 80), '重返比赛', ['全面恢复运动表现'], INK)]
for (x0, y0, x1_, y1), c, t, sub, tc in BOX:
    d.rectangle([x0, y0, x1_, y1], fill=c)
    fs = 50 if len(t) < 8 else 44
    d.text((x0 + 18, y0 + 12), t, font=font(fs), fill=tc, stroke_width=1, stroke_fill=tc)
    for k, s in enumerate(sub):
        d.text((x0 + 18, y0 + 18 + fs + k * 40), s, font=font(31), fill=tc)
for x, t in [(230, '时间'), (585, '6 周'), (840, '2 个月'), (1100, '3 个月'), (1430, '6 个月')]:
    d.text((x, 1030), t, font=font(52), fill=INK, stroke_width=1, stroke_fill=INK)
save(badge(im, '图2'), 'img03.jpg')

save(badge(blur(X(3), [(340, 360, 495, 400)], r=8), '图3'), 'img04.jpg')
