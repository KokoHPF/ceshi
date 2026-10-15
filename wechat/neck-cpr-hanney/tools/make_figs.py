#!/usr/bin/env python3
"""Hanney 2013：研究流程图中文重绘；附录图 10 英文标签改中文；附录 36 张照片按章节拼成等高网格并标图号。
用法：python3 make_figs.py <素材目录（x01..x40.png）> <输出目录>"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
INK = (30, 30, 30); RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)


# ---------- 研究流程图 ----------
def box(d, x0, y0, x1, y1, lines, dash=False, fill='white', fs=34, bold_first=False, w=4):
    if dash:
        for x in range(x0, x1, 28):
            d.line([x, y0, min(x + 16, x1), y0], fill=INK, width=w); d.line([x, y1, min(x + 16, x1), y1], fill=INK, width=w)
        for y in range(y0, y1, 28):
            d.line([x0, y, x0, min(y + 16, y1)], fill=INK, width=w); d.line([x1, y, x1, min(y + 16, y1)], fill=INK, width=w)
        d.rectangle([x0 + w, y0 + w, x1 - w, y1 - w], fill=fill)
    else:
        d.rectangle([x0, y0, x1, y1], fill=fill, outline=INK, width=w)
    h = len(lines) * (fs + 12)
    y = (y0 + y1) / 2 - h / 2
    for i, t in enumerate(lines):
        f = font(fs)
        kw = dict(stroke_width=1, stroke_fill=INK) if (bold_first and i == 0) else {}
        d.text(((x0 + x1) / 2 - d.textlength(t, font=f) / 2, y), t, font=f, fill=INK, **kw)
        y += fs + 12


def arrow(d, x1, y1, x2, y2, w=6):
    import math
    d.line([x1, y1, x2, y2], fill=INK, width=w)
    a = math.atan2(y2 - y1, x2 - x1); L = 26
    d.polygon([(x2, y2), (x2 - L * math.cos(a - .45), y2 - L * math.sin(a - .45)), (x2 - L * math.cos(a + .45), y2 - L * math.sin(a + .45))], fill=INK)


im = Image.new('RGB', (1080, 1500), 'white'); d = ImageDraw.Draw(im)
box(d, 40, 40, 520, 230, ['机械性颈痛患者', '接受纳入标准筛查', 'N = 146'], bold_first=True)
box(d, 600, 40, 1040, 160, ['不符合标准', 'N = 47'], fill=(235, 235, 235), bold_first=True)
arrow(d, 520, 100, 598, 100)
box(d, 600, 190, 1040, 470, ['手术史 22', '偏头痛 9', '待决法律诉讼 8', '神经根受压体征 2', '诊断纤维肌痛 6'], fs=30)
arrow(d, 820, 160, 820, 188)
arrow(d, 280, 230, 280, 518)
box(d, 40, 520, 520, 650, ['符合标准', 'N = 99'], fill=(242, 242, 242), bold_first=True)
box(d, 600, 530, 1040, 640, ['拒绝参加', 'N = 8'])
arrow(d, 520, 585, 598, 585)
arrow(d, 280, 650, 280, 778)
box(d, 40, 780, 520, 940, ['同意参加并签署', '知情同意书', 'N = 91'], bold_first=True)
arrow(d, 200, 940, 200, 1098); arrow(d, 400, 940, 760, 1098)
box(d, 40, 1100, 480, 1330, ['末次就诊时', '结局成功', 'N = 50'], dash=True, bold_first=True)
box(d, 560, 1100, 1040, 1330, ['末次就诊时', '结局未成功', 'N = 41'], w=7, bold_first=True)
d.text((40, 1370), '虚线框：成功（GROC ≥ +4，“中等程度改善”及以上）', font=font(28), fill=(110, 110, 110))
im.crop((0, 0, 1080, 1420)).save(f'{OUT}/flow_cn.png')

# ---------- 附录图 10：英文标签改中文 ----------
im = cv2.imread(f'{SRC}/x14.png'); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
photo = cv2.morphologyEx((g < 245).astype(np.uint8), cv2.MORPH_OPEN, np.ones((25, 25), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(photo)
rects = sorted([tuple(st[i, :4]) for i in range(1, n) if st[i, 4] > 40000], key=lambda r: (r[1] // 200, r[0]))
mask = np.zeros_like(g)
for x, y, w, h in rects:
    mask[y:y + h, x:x + w] = 1
im[(mask == 0)] = 255
p = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(p)
names = ['① 肩带下压', '② 盂肱外展', '③ 屈肘、伸腕伸指、旋后', '④ 盂肱外旋', '⑤ 伸肘', '⑥ 颈椎侧屈']
f = font(44)
for (x, y, w, h), t in zip(rects, names):
    d.text((x + w / 2 - d.textlength(t, font=f) / 2, y + h + 12), t, font=f, fill=INK)
p.save(f'{OUT}/fig10_cn.png'); print('fig10 rects', len(rects))


# ---------- 网格 ----------
def grid(rows, name, W=1080, gap=12, fs=30):
    """rows: [[(x编号, 图号), ...], ...]，每行等高、总宽 W"""
    out_rows = []
    for row in rows:
        ims = [Image.open(f'{SRC}/x{k:02d}.png').convert('RGB') for k, _ in row]
        ims = [i.crop((3, 3, i.width - 3, i.height - 3)) for i in ims]
        ratio = sum(i.width / i.height for i in ims)
        h = round((W - gap * (len(ims) - 1)) / ratio)
        r = Image.new('RGB', (W, h), 'white'); x = 0
        dd = ImageDraw.Draw(r)
        for (k, label), i in zip(row, ims):
            i = i.resize((round(i.width * h / i.height), h), Image.LANCZOS); r.paste(i, (x, 0))
            t = f'图{label}'; ff = font(fs); tw = dd.textlength(t, font=ff)
            dd.rectangle([x, 0, x + tw + 20, fs + 14], fill=RED); dd.text((x + 10, 5), t, font=ff, fill='white')
            x += i.width + gap
        out_rows.append(r)
    H = sum(r.height for r in out_rows) + gap * (len(out_rows) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for r in out_rows:
        out.paste(r, (0, y)); y += r.height + gap
    out.save(f'{OUT}/{name}'); print(name, out.size)


grid([[(5, 1), (6, 2)], [(7, 3), (8, 4)], [(9, 5), (10, 6)]], 'g_rom.png')
grid([[(11, 7), (12, 8)], [(13, 9), (16, 12)]], 'g_tests.png')
grid([[(17, '13 a/b')], [(18, '14 a/b')]], 'g_c12.png')
grid([[(19, 15), (20, 16)], [(21, 17), (22, 18)], [(23, 19), (24, 20)]], 'g_length.png')
grid([[(25, '21 a/b')], [(26, '22 a/b')]], 'g_lev_dnf.png')
grid([[(27, 23), (28, 24)], [(29, 25), (30, 26)]], 'g_mmt.png')
grid([[(31, 27), (32, 28), (33, 29), (34, 30)]], 'g_stretch.png')
grid([[(35, 31), (36, 32), (37, 33)], [(38, 34), (39, 35), (40, 36)]], 'g_strength.png')
