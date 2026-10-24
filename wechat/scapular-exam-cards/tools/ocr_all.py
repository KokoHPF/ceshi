"""对原文 27 张图做 OCR，结果存为 src/ocr/<xref>.json：[x0,y0,x1,y1（原图像素）, 文字, 置信度]"""
import sys, json, glob, os
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
eng = RapidOCR()
for f in sorted(glob.glob('src/x*.jpg')):
    x = os.path.basename(f)[1:-4]; out = f'src/ocr/{x}.json'
    if os.path.exists(out): continue
    im = Image.open(f).convert('RGB'); s = min(1, 2400 / im.width)
    sm = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); tmp = f'/tmp/claude-0/-home-user-ceshi/4ba42343-d8b5-5006-989a-e66204e17130/scratchpad/ocr_{x}.png'; sm.save(tmp)
    res, _ = eng(tmp)
    rows = []
    for box, txt, conf in res or []:
        xs = [p[0] / s for p in box]; ys = [p[1] / s for p in box]
        rows.append([round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys)), txt, round(float(conf), 2)])
    json.dump(rows, open(out, 'w'), ensure_ascii=False); print(x, len(rows), flush=True)
