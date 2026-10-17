"""原文图 2、图 3（位图柱状图）中文化：灰色分类条重写中文、面板标题和纵轴标题覆盖后重写、图例改中文。"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)


def panels(im):
    a = np.array(im.convert('RGB')).astype(int)
    g = (abs(a[..., 0] - a[..., 1]) < 8) & (abs(a[..., 1] - a[..., 2]) < 8) & (a[..., 0] > 195) & (a[..., 0] < 232)
    n, lab, st, _ = cv2.connectedComponentsWithStats(g.astype(np.uint8))
    bars = [tuple(st[i, :4]) for i in range(1, n) if st[i, 2] > 250 and 18 < st[i, 3] < 60]
    dark = (a.max(2) < 120).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(dark)
    axes = [tuple(st[i, :4]) for i in range(1, n) if st[i, 3] > 60]
    out = []
    for bx, by, bw, bh in sorted(bars, key=lambda b: (b[1] // 200, b[0])):
        cand = [a_ for a_ in axes if bx - 60 < a_[0] < bx + 40 and a_[1] < by]
        c = max(cand, key=lambda c: c[1])
        row = dark[by - 14:by - 2, bx:bx + bw].any(0)
        xs, run = [], []
        for x, v in enumerate(row):
            if v: run.append(x)
            elif run: xs.append(bx + sum(run) / len(run)); run = []
        if run: xs.append(bx + sum(run) / len(run))
        out.append(((bx, by, bw, bh), c[0], c[1], c[2]))
    return out


def relabel(im, cats, titles, ylab, fs=24, up=72):
    im = im.convert('RGB'); dr = ImageDraw.Draw(im)
    for k, ((bx, by, bw, bh), ax, top, pw) in enumerate(panels(im)):
        dr.rectangle([bx, by, bx + bw, by + bh], fill=(214, 214, 214))
        n = len(cats)
        for i, c in enumerate(cats):
            cx = ax + pw * (i + .5) / n
            f = font(fs); dr.text((cx - dr.textlength(c, font=f) / 2, by + (bh - fs) / 2 - 2), c, font=f, fill=(20, 20, 20))
        if titles:
            dr.rectangle([bx, by + bh + 2, bx + bw, by + bh + 50], fill='white')
            f = font(34); t = titles[k]; dr.text((bx + bw / 2 - dr.textlength(t, font=f) / 2, by + bh + 6), t, font=f, fill=(20, 20, 20))
        dr.rectangle([max(0, ax - 125), max(0, top - up), ax + 24, top - 4], fill='white')
        f = font(26); dr.text((max(0, ax - 100), max(0, top - 50)), ylab, font=f, fill=(20, 20, 20))
    a = np.array(im).astype(int)
    for col, lab in [((0, 120, 140), '干预前'), ((255, 255, 70), '干预后')]:
        m = (np.abs(a - np.array(col)).sum(2) < 90).astype(np.uint8)
        n_, _, st, _ = cv2.connectedComponentsWithStats(m)
        for i in range(1, n_):
            x, y, w, h, _a = st[i]
            if 40 < w < 110 and 12 < h < 45 and w > 1.6 * h:
                dr.rectangle([x + w + 4, y - 8, x + w + 80, y + h + 8], fill='white')
                f = font(28); dr.text((x + w + 10, y + h / 2 - 15), lab, font=f, fill=(20, 20, 20))
    return im
