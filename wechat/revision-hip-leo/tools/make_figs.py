#!/usr/bin/env python3
"""Leo 2023：图 4 进阶标准流程图中文重绘；其余照片加图号；封面取自图 5。
用法：python3 make_figs.py <素材目录（x01..x07.png、title.png）> <输出目录>"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 14))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')
for k, (src, n) in enumerate([(1, 1), (2, 2), (3, 3)]):
    save(badge(X(src), f'图{n}'), f'img{k + 2:02d}.jpg')

# ---------- 图 4：进阶标准流程图（中文重绘） ----------
phases = [
    ('第一阶段：保护期 → 进入第二阶段', ['臀中肌侧卧保持 30 秒', '臀大肌俯卧伸髋 10 次', '腹横肌激活 1 分钟（触诊下）',
                             '单腿站立 >10 秒，对侧髋不下沉', '各方向活动度达正常的 90%（外旋和屈曲达 75%）']),
    ('第二阶段：耐力期 → 进入第三阶段', ['等长伸髋、外展、内旋、外旋 LSI 80%', '等长屈髋 LSI 50%', '侧平板支撑 1 分钟，LSI 90%',
                             'FABER（膝到床面距离，cm）LSI 90%', 'Y 平衡前向伸够两侧差 <8 cm', '正常步态行走 10 分钟']),
    ('第三阶段：强化期 → 进入第四阶段', ['等长屈髋 LSI 80%', '等长伸髋、外展、外旋、内旋 90%', '膝屈/伸力量 LSI >90%',
                             '侧平板支撑 + 髋外展 10 次', 'Y 平衡前向伸够两侧差 <4 cm']),
    ('第四阶段：爆发力期 → 进入第五阶段', ['等长伸髋、外展、外旋、内旋、屈髋 LSI 保持 >90%', '单腿三级跳远 >90%', '单腿垂直跳 >90%',
                              'Vail 运动测试 >17/20 分', '  单腿蹲、侧向敏捷、斜向敏捷、向前箱式弓步']),
    ('第五阶段：重返运动', ['T 型敏捷测试 LSI 90%', '完成专项技能和训练', '手术医生、物理治疗师和医疗团队同意']),
]
FILL = (214, 228, 243); EDGE = (79, 129, 189); INK = (25, 25, 25)
W = 1080; fs, ts, lh, pad = 32, 38, 46, 26
H = sum(pad * 2 + ts + 18 + lh * len(b) for _, b in phases) + 70 * 4 + 40
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im); y = 20
for i, (t, items) in enumerate(phases):
    h = pad * 2 + ts + 18 + lh * len(items)
    d.rounded_rectangle([30, y, W - 30, y + h], 30, fill=FILL, outline=EDGE, width=4)
    d.text((60, y + pad), t, font=font(ts), fill=INK, stroke_width=1, stroke_fill=INK)
    for j, it in enumerate(items):
        yy = y + pad + ts + 18 + j * lh
        if it.startswith('  '):
            d.text((120, yy), '（' + it.strip() + '）', font=font(fs - 2), fill=(70, 70, 70))
        else:
            d.ellipse([78, yy + fs // 2 - 5, 90, yy + fs // 2 + 7], fill=EDGE)
            d.text((104, yy), it, font=font(fs), fill=INK)
    y += h
    if i < 4:
        cx = W // 2
        d.line([cx, y + 6, cx, y + 52], fill=EDGE, width=6)
        d.polygon([(cx - 18, y + 46), (cx + 18, y + 46), (cx, y + 66)], fill=EDGE)
        y += 70
im.crop((0, 0, W, y + 20)).save(f'{OUT}/img05.jpg', quality=92)

for k, (src, n) in enumerate([(5, 5), (6, 6), (7, 7)]):
    save(badge(X(src), f'图{n}'), f'img{k + 6:02d}.jpg')

# ---------- 封面：图 5 侧平板支撑，裁成 900×383 ----------
c = X(5); w, h = c.size; cw = round(h * 900 / 383); x = (w - cw) // 2
c.crop((x, 0, x + cw, h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('done')
