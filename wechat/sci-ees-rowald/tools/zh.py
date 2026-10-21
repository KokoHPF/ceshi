"""图中英文标注替换为中文：按 OCR 定位框盖底色、写中文。框坐标为原图宽 1000 的比例坐标。"""
import json
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))


def bgcolor(im, b, pad=3):
    x0, y0, x1, y1 = b; px = []
    for x in range(max(0, x0 - pad), min(im.width, x1 + pad)):
        for y in (max(0, y0 - pad), min(im.height - 1, y1 + pad)): px.append(im.getpixel((x, y)))
    for y in range(max(0, y0 - pad), min(im.height, y1 + pad)):
        for x in (max(0, x0 - pad), min(im.width - 1, x1 + pad)): px.append(im.getpixel((x, y)))
    q = Counter(tuple(v // 8 * 8 for v in p) for p in px).most_common(1)[0][0]
    near = [p for p in px if all(abs(a - c) < 12 for a, c in zip(p, q))]
    return tuple(sum(c) // len(near) for c in zip(*near))


def fgcolor(im, b, bg):
    best, d = (0, 0, 0), -1
    for x in range(b[0], b[2], 2):
        for y in range(b[1], b[3], 2):
            p = im.getpixel((x, y)); dd = sum((a - c) ** 2 for a, c in zip(p, bg))
            if dd > d: best, d = p, dd
    lum = sum(best) / 3
    if max(best) - min(best) < 60: best = (255, 255, 255) if lum > 140 else (25, 25, 25)
    return best


def put(im, b, text, fs=None, al='c', fg=None, bg=None, rot=None, ml=1.0, cap=None):
    """b: 像素框；在框中心写 text，必要时向两侧（或单侧）延伸覆盖"""
    dr = ImageDraw.Draw(im)
    bg = bg or bgcolor(im, b); fg = fg or fgcolor(im, b, bg)
    w, h = b[2] - b[0], b[3] - b[1]
    vertical = rot if rot is not None else (h > 2.2 * w and len(text.replace('\n', '')) >= 2)
    if vertical: w, h = h, w
    lines = text.split('\n')
    if text == '':
        dr.rectangle(b, fill=bg); return
    f0 = fs or h / len(lines) * 0.82 * ml
    if cap and not fs: f0 = min(f0, cap * ml)
    tw = max(dr.textlength(l, font=font(f0)) for l in lines)
    if tw > w * 1.25 and not fs:
        f0 = max(f0 * w * 1.25 / tw, h / len(lines) * 0.55)
        if cap: f0 = min(f0, cap * ml)
    fnt = font(f0); tw = max(dr.textlength(l, font=fnt) for l in lines); th = f0 * 1.18 * len(lines)
    if not vertical:
        cx = {'c': (b[0] + b[2]) / 2, 'l': b[0] + tw / 2, 'r': b[2] - tw / 2}[al]; cy = (b[1] + b[3]) / 2
        r = [min(b[0], cx - tw / 2 - 2), min(b[1], cy - th / 2), max(b[2], cx + tw / 2 + 2), max(b[3], cy + th / 2)]
        dr.rectangle([b[0] - 1, b[1] - 1, b[2] + 1, b[3] + 1], fill=bg); dr.rectangle(r, fill=bg)
        for i, l in enumerate(lines):
            lw = dr.textlength(l, font=fnt)
            x = {'c': cx - lw / 2, 'l': cx - tw / 2, 'r': cx + tw / 2 - lw}[al]
            dr.text((x, cy - th / 2 + i * f0 * 1.18), l, font=fnt, fill=fg)
    else:
        t = Image.new('RGB', (int(tw) + 6, int(th) + 4), bg); td = ImageDraw.Draw(t)
        for i, l in enumerate(lines): td.text((3, 2 + i * f0 * 1.18), l, font=fnt, fill=fg)
        t = t.rotate(90, expand=True)
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        dr.rectangle([b[0] - 1, b[1] - 1, b[2] + 1, b[3] + 1], fill=bg)
        im.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)))


def apply(im, ocr, spec, W=2000, extra=()):
    """ocr: OCR 结果文件；spec: [(英文或英文列表, 中文, {选项})]；extra: [(框@1000, 中文, {选项})] 手工补充"""
    im = im.convert('RGB'); s = W / im.width
    im = im.resize((W, round(im.height * s)), Image.LANCZOS); k = W / 1000
    rows = json.load(open(ocr)); used = set()
    hs = sorted(min(r[3] - r[1], r[2] - r[0]) for r in rows); cap = hs[len(hs) // 2] * k * 0.95
    def box(r, p=2): return [int(r[0] * k) - p, int(r[1] * k) - p, int(r[2] * k) + p, int(r[3] * k) + p]
    jobs = []
    for item in spec:
        en, zh, *opt = item; opt = opt[0] if opt else {}
        keys = en if isinstance(en, list) else [en]
        hits = []
        for key in keys:
            t, _, at = key.partition('@')
            h = [i for i, r in enumerate(rows) if r[4].strip() == t.strip() and i not in used]
            if at and h:
                px, py = map(float, at.split(','))
                h = [min(h, key=lambda i: (rows[i][0] + rows[i][2] - 2 * px) ** 2 + (rows[i][1] + rows[i][3] - 2 * py) ** 2)]
            hits.append(h)
        if not all(hits): continue
        if isinstance(en, list):
            ids = [h[0] for h in hits]; used.update(ids)
            bs = [box(rows[i]) for i in ids]
            jobs.append(([min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)], zh, opt))
        else:
            for i in (hits[0] if opt.get('all', True) and '@' not in en else hits[0][:1]):
                used.add(i); jobs.append((box(rows[i]), zh, opt))
    for b, zh, opt in jobs:
        o = {kk: v for kk, v in opt.items() if kk != 'all'}
        put(im, b, zh, cap=cap, **o)
    for b0, zh, opt in extra:
        put(im, [int(v * k) for v in b0], zh, **{'cap': cap, **opt})
    left = [r[4] for i, r in enumerate(rows) if i not in used]
    return im, left
