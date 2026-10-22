import sys, json
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
eng = RapidOCR()
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); s = 2000 / max(im.size)
if s > 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
else: s = 1
im.save(out + '.png')
res, _ = eng(out + '.png')
W = Image.open(src).width
rows = []
for box, txt, conf in res or []:
    xs = [p[0] / s for p in box]; ys = [p[1] / s for p in box]
    b = [min(xs), min(ys), max(xs), max(ys)]
    rows.append([round(v * 1000 / W) for v in b] + [txt, round(float(conf), 2)])
json.dump(rows, open(out, 'w'), ensure_ascii=False)
for r in rows: print(r)
