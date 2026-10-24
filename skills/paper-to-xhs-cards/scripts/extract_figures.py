#!/usr/bin/env python3
"""从论文 PDF 提取图片和图注，生成核对用的缩略总览。

用法：python3 extract_figures.py paper.pdf out_dir [--min-width 150] [--render-dpi 300]
输出：
  out_dir/x<xref>.jpg      PDF 内嵌原图（最高分辨率）
  out_dir/page<页>.png     每页渲染图（110 dpi），用于看矢量箭头、表格和图注位置
  out_dir/figures.json     [{xref, page, bbox, width, height}] + 每页“Figure/Fig/图”开头的图注文字
  out_dir/_thumbs.jpg      所有提取图的缩略总览（标 xref）
  out_dir/text.txt         全文文字（按页）
另：python3 extract_figures.py paper.pdf out_dir --clip PAGE x0 y0 x1 y1 NAME
     把页面某区域按 --render-dpi 渲染成 out_dir/NAME.jpg（原图被反色、或箭头/标注是矢量叠加层时用）。
依赖：pymupdf（pip install pymupdf）、Pillow
"""
import json, os, re, sys
from io import BytesIO
import pymupdf
from PIL import Image, ImageDraw

args = sys.argv[1:]
pdf, out = args[0], args[1]; os.makedirs(out, exist_ok=True)
dpi = int(args[args.index('--render-dpi') + 1]) if '--render-dpi' in args else 300
doc = pymupdf.open(pdf)
if '--clip' in args:
    i = args.index('--clip'); pg, x0, y0, x1, y1, name = int(args[i + 1]), *map(float, args[i + 2:i + 6]), args[i + 6]
    pix = doc[pg].get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1))
    Image.open(BytesIO(pix.tobytes('png'))).convert('RGB').save(f'{out}/{name}.jpg', quality=93); print('saved', name); sys.exit()
minw = int(args[args.index('--min-width') + 1]) if '--min-width' in args else 150
figs, caps, seen = [], [], set()
with open(f'{out}/text.txt', 'w', encoding='utf-8') as ft:
    for pn, page in enumerate(doc):
        ft.write(f'=====PAGE {pn + 1}\n' + page.get_text())
        page.get_pixmap(dpi=110).save(f'{out}/page{pn + 1}.png')
        for b in page.get_text('blocks'):
            t = b[4].strip()
            if re.match(r'^(Fig(ure)?\.?\s*\d|FIGURE\s*\d|Table\s*\d|TABLE\s*\d|图\s*\d|表\s*\d)', t):
                caps.append({'page': pn, 'bbox': [round(v) for v in b[:4]], 'text': ' '.join(t.split())})
        for info in page.get_image_info(xrefs=True):
            x = info['xref']
            if not x or x in seen or info['width'] < minw: continue
            seen.add(x)
            e = doc.extract_image(x); im = Image.open(BytesIO(e['image']))
            im.convert('RGB').save(f'{out}/x{x}.jpg', quality=95)
            figs.append({'xref': x, 'page': pn, 'bbox': [round(v) for v in info['bbox']], 'width': im.width, 'height': im.height})
json.dump({'figures': figs, 'captions': caps}, open(f'{out}/figures.json', 'w'), ensure_ascii=False, indent=1)
th = []
for f in figs:
    t = Image.open(f"{out}/x{f['xref']}.jpg"); t.thumbnail((380, 300)); th.append((f, t))
if th:
    cols = 5; sheet = Image.new('RGB', (cols * 390, ((len(th) + cols - 1) // cols) * 320), 'white'); d = ImageDraw.Draw(sheet)
    for i, (f, t) in enumerate(th):
        sheet.paste(t, ((i % cols) * 390, (i // cols) * 320 + 16)); d.text(((i % cols) * 390, (i // cols) * 320), f"x{f['xref']} p{f['page'] + 1}", fill='red')
    sheet.save(f'{out}/_thumbs.jpg', quality=85)
print(f'{len(figs)} 张图，{len(caps)} 条图注/表题 → {out}')
for c in caps: print(f"  p{c['page'] + 1} {c['text'][:90]}")
