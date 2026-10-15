#!/usr/bin/env python3
"""图 1 四个英文说明框改为中文；9 个 YouTube 附件视频的封面截图拼成带中文编号的网格。
用法：python3 make_figs.py <素材目录（含 f1.png、vid/th1..9.jpg）> <输出目录>"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
K = (20, 20, 20)
RED = (171, 25, 66)

im = Image.open(f'{SRC}/f1.png').convert('RGB')
s = im.width / 1000
S = lambda *v: tuple(round(x * s) for x in v)
d = ImageDraw.Draw(im)
boxes = {
    (50, 28, 352, 167): ['D2 屈曲-外展-外旋', '肩：屈曲、外展、外旋', '肩胛：后上提', '肘：视目标而定', '腕：桡偏、旋后', '手指：伸展'],
    (640, 28, 966, 177): ['D1 屈曲-内收-外旋', '肩：屈曲、内收、外旋', '肩胛：前上提', '肘：视目标而定', '腕：桡偏、旋后', '手指：屈曲、内收'],
    (28, 272, 332, 412): ['D1 伸展-外展-内旋', '肩：伸展、外展、内旋', '肩胛：后下压', '肘：视目标而定', '腕：尺偏、旋前', '手指：伸展、外展'],
    (628, 272, 937, 412): ['D2 伸展-内收-内旋', '肩：伸展、内收、内旋', '肩胛：前下压', '肘：视目标而定', '腕：尺偏、旋前', '手指：屈曲、内收'],
}
for (x0, y0, x1, y1), lines in boxes.items():
    d.rectangle(S(x0 - 6, y0 - 6, x1 + 26, y1 + 8), fill='white')
    d.rectangle(S(x0, y0, x1, y1), fill='white', outline=K, width=round(1.5 * s))
    fb = ImageFont.truetype(F, round(17 * s)); fn = ImageFont.truetype(F, round(15 * s))
    y = y0 + 8
    for i, t in enumerate(lines):
        f = fb if i == 0 else fn
        d.text(S(x0 + 10, y), t, font=f, fill=RED if i == 0 else K, **({'stroke_width': 1, 'stroke_fill': RED} if i == 0 else {}))
        y += 24 if i == 0 else 21
im.save(f'{OUT}/g1.png')

# 视频封面：去黑边后统一裁成 4:5 竖图
TITLES = {
    1: '视频1 肩 D2 屈曲：主动肌反转', 2: '视频2 双侧肩胛后上提', 3: '视频3 肩 D2 屈伸慢速反转',
    4: '视频4 肩 D1 屈伸慢速反转', 5: '视频5 肩胛前上提慢速反转', 6: '视频6 肩胛后上提/前下压（侧卧）',
    7: '视频7 肩 D2 等张组合（站立）', 8: '视频8 肩 D2 等张组合（俯卧）', 9: '视频9 肩 D2 等张组合+重复牵张',
}


def tile(n):
    t = Image.open(f'{SRC}/vid/th{n}.jpg').convert('RGB')
    a = np.asarray(t).mean(2)
    rows = np.where(a.mean(1) > 25)[0]; cols = np.where(a.mean(0) > 25)[0]
    t = t.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    W, H = 360, 450
    r = max(W / t.width, H / t.height)
    t = t.resize((round(t.width * r), round(t.height * r)), Image.LANCZOS)
    x = (t.width - W) // 2; y = (t.height - H) // 2
    return t.crop((x, y, x + W, y + H))


def grid(ids, name):
    W, H, cap, g = 360, 450, 64, 14
    cols = 3
    rows = (len(ids) + cols - 1) // cols
    out = Image.new('RGB', (cols * W + (cols - 1) * g, rows * (H + cap) + (rows - 1) * g), 'white')
    d = ImageDraw.Draw(out)
    f = ImageFont.truetype(F, 24)
    for i, n in enumerate(ids):
        x = (i % cols) * (W + g); y = (i // cols) * (H + cap + g)
        out.paste(tile(n), (x, y))
        t = TITLES[n]
        lines = [t[:t.index(' ')], t[t.index(' ') + 1:]]
        for j, ln in enumerate(lines):
            ff = ImageFont.truetype(F, 22 if j else 24)
            d.text((x + (W - d.textlength(ln, font=ff)) / 2, y + H + 4 + j * 30), ln, font=ff,
                   fill=RED if j == 0 else K, **({'stroke_width': 1, 'stroke_fill': RED} if j == 0 else {}))
    out.save(f'{OUT}/{name}')


grid([1, 3, 4, 7, 8, 9], 'grid_shoulder.png')
grid([2, 5, 6], 'grid_scapula.png')
print('done')
