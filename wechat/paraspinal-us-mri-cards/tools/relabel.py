"""把原文图里的英文标注抹掉（OpenCV 修补），在原位置写中文。
标注框来自 src/ocr/<xref>.json（两遍 OCR），再按 tools/fixes.py 里的逐图人工修正：EXTRA 补漏检的框，SKIP 跳过的框，TEXT 改正识别错的文字。
上下两行的长名称（如 Semispinalis / capitis m.）自动合并成一个框。"""
import json, sys, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from labels import lookup
import fixes

FONT = sys.argv[1] if len(sys.argv) > 1 else None


def boxes_for(x):
    rows = [list(r) for r in json.load(open(f'src/ocr/{x}.json'))]
    for i, t in fixes.TEXT.get(x, {}).items(): rows[i][4] = t
    rows = [r for i, r in enumerate(rows) if i not in fixes.SKIP.get(x, ())]
    rows += [list(r) + [1.0] for r in fixes.EXTRA.get(x, [])]
    # 合并上下行
    used = set(); out = []
    rows.sort(key=lambda r: (r[1], r[0]))
    for i, a in enumerate(rows):
        if i in used: continue
        cur = a[:]
        for _ in range(2):
            ha = cur[3] - cur[1]
            for j, b in enumerate(rows):
                if j in used or j == i or b is a: continue
                gap = b[1] - cur[3]; ov = min(cur[2], b[2]) - max(cur[0], b[0])
                if -0.3 * ha < gap < 0.9 * ha and ov > 0.2 * min(cur[2] - cur[0], b[2] - b[0]):
                    t = cur[4] + ' ' + b[4]
                    if lookup(t) and not lookup(cur[4]) or (lookup(t) and lookup(b[4]) is None):
                        cur = [min(cur[0], b[0]), cur[1], max(cur[2], b[2]), b[3], t, 1.0, ha]; used.add(j); break
        if len(cur) < 7: cur.append(cur[3] - cur[1])
        out.append(cur)
    return [r for r in out if lookup(r[4])]


def erase(img, box, lh):
    H, W = img.shape[:2]; x0, y0, x1, y1 = box; p = int(lh * .35)
    X0, Y0, X1, Y1 = max(0, x0 - p), max(0, y0 - p), min(W, x1 + p), min(H, y1 + p)
    reg = img[Y0:Y1, X0:X1]; g = cv2.cvtColor(reg, cv2.COLOR_RGB2GRAY).astype(int)
    ring = np.concatenate([g[:3].ravel(), g[-3:].ravel(), g[:, :3].ravel(), g[:, -3:].ravel()])
    bg = np.median(ring)
    m = ((g > bg + 38) | ((g > 205) & (bg < 200))).astype(np.uint8) * 255
    inner = np.zeros_like(m); inner[p // 2: m.shape[0] - p // 2, p // 2: m.shape[1] - p // 2] = 1
    m = m * inner
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=max(2, int(lh * .08)))
    full = np.zeros((H, W), np.uint8); full[Y0:Y1, X0:X1] = m
    return cv2.inpaint(img, full, max(3, int(lh * .25)), cv2.INPAINT_TELEA)


def relabel(x, scale=1.15):
    img = np.asarray(Image.open(f'src/x{x}.jpg').convert('RGB')).copy()
    bs = boxes_for(x)
    if not bs: return Image.fromarray(img)
    for b in bs: img = erase(img, b[:4], b[6])
    im = Image.fromarray(img); d = ImageDraw.Draw(im); W, H = im.size
    lhs = sorted(b[6] for b in bs); base = lhs[len(lhs) // 2]
    for b in bs:
        zh = lookup(b[4]); fs = int(base * scale * fixes.SIZE.get(x, 1.0))
        f = ImageFont.truetype(FONT, fs); tw = d.textlength(zh, font=f)
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        al = fixes.ALIGN.get(x, {}).get(b[4])
        X = b[0] if al == 'l' else (b[2] - tw if al == 'r' else cx - tw / 2)
        X = max(4, min(W - tw - 4, X)); Y = cy - fs * .62
        # 文字颜色按原底色：亮底用深字
        bgl = np.asarray(im.convert('L').crop((int(b[0]), int(b[1]), int(b[2]), int(b[3])))).mean()
        fill, st = ((255, 255, 255), (0, 0, 0)) if bgl < 170 else ((20, 20, 20), (255, 255, 255))
        d.text((X, Y), zh, font=f, fill=fill, stroke_width=max(2, fs // 12), stroke_fill=st)
    return im


if __name__ == '__main__':
    out = sys.argv[2]
    for x in sys.argv[3:]:
        im = relabel(x); im.save(f'{out}/z{x}.jpg', quality=90)
        t = im.copy(); t.thumbnail((1600, 1600)); t.save(f'{out}/zv{x}.jpg', quality=82)
        print(x, len(boxes_for(x)))
