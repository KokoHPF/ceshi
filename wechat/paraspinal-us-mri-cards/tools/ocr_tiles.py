"""第二遍 OCR：原图分块（1400×1400，重叠 300），补漏检的小字；与第一遍结果按重叠去重后写回 src/ocr/<xref>.json"""
import json, glob, os, sys
from PIL import Image, ImageOps
from rapidocr_onnxruntime import RapidOCR
eng = RapidOCR()
TMP = sys.argv[1]
def iou(a, b):
    x0, y0 = max(a[0], b[0]), max(a[1], b[1]); x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    if x1 <= x0 or y1 <= y0: return 0
    i = (x1 - x0) * (y1 - y0); return i / min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
for f in sorted(glob.glob('src/x*.jpg')):
    x = os.path.basename(f)[1:-4]; out = f'src/ocr/{x}.json'; done = f'src/ocr/{x}.tiles'
    if os.path.exists(done): continue
    rows = json.load(open(out)); im = Image.open(f).convert('RGB'); W, H = im.size
    new = []
    for inv in (False, True):  # 反色一遍，抓深色底上的浅色字和彩色底上的字
        src = ImageOps.invert(im) if inv else im
        for ty in range(0, H, 1100):
            for tx in range(0, W, 1100):
                t = src.crop((tx, ty, min(W, tx + 1400), min(H, ty + 1400))); p = f'{TMP}/tile.png'; t.save(p)
                res, _ = eng(p)
                for box, txt, conf in res or []:
                    if float(conf) < 0.6: continue
                    xs = [q[0] + tx for q in box]; ys = [q[1] + ty for q in box]
                    b = [round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys)), txt, round(float(conf), 2)]
                    if any(iou(b, r) > 0.4 for r in rows + new): continue
                    new.append(b)
    json.dump(rows + new, open(out, 'w'), ensure_ascii=False); open(done, 'w').write(str(len(new)))
    print(x, '+', len(new), [n[4] for n in new], flush=True)
