"""画出 OCR 框：绿=可翻译，红=未识别；标上序号，供人工核对"""
import json, sys, glob, os
sys.path.insert(0, 'tools')
from labels import lookup
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 40)
OUT = sys.argv[1]
for f in sorted(glob.glob('src/ocr/*.json'), key=lambda p: int(os.path.basename(p)[:-5])):
    x = os.path.basename(f)[:-5]; im = Image.open(f'src/x{x}.jpg').convert('RGB'); d = ImageDraw.Draw(im)
    for i, (x0, y0, x1, y1, t, c) in enumerate(json.load(open(f))):
        ok = lookup(t); col = (0, 255, 0) if ok else (255, 0, 0)
        d.rectangle([x0, y0, x1, y1], outline=col, width=6); d.text((x0, y1 + 2), str(i), font=F, fill=(255, 255, 0))
    im.thumbnail((1600, 1600)); im.save(f'{OUT}/v{x}.jpg', quality=80)
