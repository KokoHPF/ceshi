#!/usr/bin/env python3
"""Fraser 2016 Part 2：图 1、2 英文标注改为中文；表 2～4 中的手法照片以 600 dpi 从原文裁出，
按表格顺序拼图并加中文名称；封面取自图 1。
用法：python3 make_figs.py <原文 PDF> <素材目录（x01、x02、title.png）> <输出目录>"""
import sys
import cv2
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

PDF, SRC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66); INK = (25, 25, 25)
font = lambda s: ImageFont.truetype(F, s)


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.width // 36))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=90)
    return im


def relabel(im, items, fs, extra=(), keep=None):
    """items: ((x0, y0, x1, y1), 中文)；黑底上把框内除骨骼（keep 判定）以外的像素涂黑，再居中写中文"""
    a = np.array(im); ai = a.astype(int)
    k = keep(ai) if keep else np.zeros(a.shape[:2], bool)
    lab, n = ndimage.label(k)  # 只保留大块骨骼区域，字母笔画是小连通域
    sz = ndimage.sum(k, lab, range(1, n + 1)); k = np.isin(lab, 1 + np.where(sz > 4000)[0])
    m = np.zeros(a.shape[:2], np.uint8)
    for (x0, y0, x1, y1) in [b for b, _ in items] + list(extra):
        m[y0:y1, x0:x1] = (~k[y0:y1, x0:x1]) * 255
    a = a.copy(); a[m > 0] = 3
    im = Image.fromarray(a); d = ImageDraw.Draw(im); f = font(fs)
    for (x0, y0, x1, y1), t in items:
        ls = t.split('\n'); lh = fs + 6; y = (y0 + y1) / 2 - lh * len(ls) / 2 + 3
        for l in ls:
            d.text(((x0 + x1) / 2 - d.textlength(l, font=f) / 2, y), l, font=f, fill='white'); y += lh
    return im


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

# 图 1：内翻损伤时的外部力矩与中足应力
im = relabel(Image.open(f'{SRC}/x01.png').convert('RGB'), [
    ((276, 86, 480, 152), '跨踝线'), ((522, 18, 655, 160), '跨跟骨线\n（距下）'),
    ((306, 226, 450, 367), '跨跟骨线\n（跗中）'), ((490, 278, 570, 377), '跨骰\n骨线'),
    ((150, 398, 388, 462), '前足外部\n内翻力矩'), ((459, 710, 598, 848), '前足外部\n内收力矩'),
    ((664, 688, 801, 788), '跗中关节\n内收应力'), ((855, 622, 975, 725), '后足\n内翻应力')], 30,
    keep=lambda a: (a[..., 0] > 90) & (a[..., 0] - a[..., 2] > 40))
save(badge(im, '图1'), 'img02.jpg')
c = im.crop((0, 150, im.width, 150 + round(im.width * 383 / 900)))
c.resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)

# 图 2：腓骨长肌收缩使骰骨外翻
im = relabel(Image.open(f'{SRC}/x02.png').convert('RGB'), [
    ((326, 180, 512, 282), '骰骨相对跟骨的\n外翻力矩'), ((494, 524, 594, 618), '腓骨\n长肌腱')], 30, extra=[(512, 180, 546, 236)],
    keep=lambda a: (a.mean(2) > 150) & (a[..., 0] - a[..., 2] > 12))
save(badge(im, '图2'), 'img03.jpg')

# 表 2～4 照片：在“图片”列内按连通域找出每张照片，600 dpi 重新渲染
doc = pymupdf.open(PDF)


def photos(pno, x0=440, x1=537, y0=60, y1=620):
    pg = doc[pno - 1]; pix = pg.get_pixmap(dpi=150, clip=pymupdf.Rect(x0, y0, x1, y1))
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3).astype(int)
    m = ((a.max(2) - a.min(2)) > 25) | (a.mean(2) < 200)
    lab, _ = ndimage.label(ndimage.binary_opening(m, np.ones((5, 5))))
    out = []
    for s in ndimage.find_objects(lab):
        h, w = s[0].stop - s[0].start, s[1].stop - s[1].start
        if h * w < 5000 or h < 60:  # 去掉表头红条和细线
            continue
        k = 72 / 150
        r = pymupdf.Rect(x0 + s[1].start * k, y0 + s[0].start * k, x0 + s[1].stop * k, y0 + s[0].stop * k)
        p = pg.get_pixmap(dpi=600, clip=r); out.append((s[0].start, Image.frombytes('RGB', (p.width, p.height), p.samples)))
    return [im for _, im in sorted(out, key=lambda t: t[0])]


def tile(im, t, H):
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    c = Image.new('RGB', (im.width, H + 64), 'white'); c.paste(im, (0, 0)); d = ImageDraw.Draw(c)
    f = font(34)
    while d.textlength(t, font=f) > im.width - 8 and f.size > 20:
        f = font(f.size - 1)
    d.text((im.width / 2 - d.textlength(t, font=f) / 2, H + 14), t, font=f, fill=INK)
    return c


def grid(ims, caps, rows, W=1620, gap=12):
    out = []; i = 0
    for n in rows:
        grp = ims[i:i + n]; cg = caps[i:i + n]; i += n
        H = min(560, round((W - gap * (n - 1)) / sum(g.width / g.height for g in grp)))
        ts = [tile(g, c, H) for g, c in zip(grp, cg)]
        r = Image.new('RGB', (sum(t.width for t in ts) + gap * (n - 1), ts[0].height), 'white'); x = 0
        for t in ts:
            r.paste(t, (x, 0)); x += t.width + gap
        if r.width > W:
            r = r.resize((W, round(r.height * W / r.width)), Image.LANCZOS)
        rr = Image.new('RGB', (W, r.height), 'white'); rr.paste(r, ((W - r.width) // 2, 0)); out.append(rr)
    c = Image.new('RGB', (W, sum(o.height for o in out) + gap * (len(out) - 1) + 80), 'white'); y = 0  # 底部留白放表号
    for o in out:
        c.paste(o, (0, y)); y += o.height + gap
    return c


P2 = photos(7); P3 = photos(8); P4 = photos(9)
assert (len(P2), len(P3), len(P4)) == (9, 6, 5), (len(P2), len(P3), len(P4))
C2 = ['① 第一跖趾关节被动活动度', '② 拇趾伸展活动范围', '③ 第一跗跖关节跖侧滑动', '④ 第一跗跖关节活动范围', '⑤ 前足/中足内翻、外翻活动度',
      '⑥ 中足内收被动活动度', '⑦ 距舟关节被动活动度', '⑧ 跟骰关节被动活动度', '⑨ 距下关节外翻被动活动度']
C3 = ['① 拇趾（跖趾关节）背侧滑动', '② 第一跗跖关节跖侧滑动', '③ 骰骨背外侧滑动 + 前足旋后', '④ 跟骰挤压', '⑤ 骰骨甩鞭手法', '⑥ 距舟关节跖侧/背侧滑动']
C4 = ['① 距下关节外侧滑动', '② 距骨牵引手法', '③ 距骨后向滑动手法', '④ 近端胫腓关节手法', '⑤ 远端胫腓关节后向滑动']
save(badge(grid(P2, C2, [3, 3, 3]), '表2配图'), 'img04.jpg')
save(badge(grid(P3, C3, [2, 2, 2]), '表3配图'), 'img05.jpg')
save(badge(grid(P4, C4, [2, 2, 1]), '表4配图'), 'img06.jpg')
