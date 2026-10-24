#!/usr/bin/env python3
"""给没有文字的示意图加中文结构标注（彩色标签 + 引线 + 圆点）和方向标注。

用法：python3 annotate.py spec.json --font 字体.otf
spec.json：
  [{"src": "gr2.jpg", "out": "fig2.zh.jpg", "scale": 2,            # scale：先放大几倍再标（小图建议 2～3）
    "crop": [0, 0, 233, 285],                                       # 可选，先裁切（原图像素）
    "fs": 40,                                                       # 标签字号（放大后像素）
    "labels": [["肱骨头", [900, 280], [780, 520], "primary"],       # [文字, 标签左上角, 指向点或 null, 颜色]
               ["向后半脱位", [690, 700], null, "accent"]],
    "dirs": {"top": "前", "bottom": "后", "left": null, "right": null, "corner": "上前·下后"}}]
颜色可用 primary / accent / teal / highlight，或 "#RRGGBB"。坐标都是放大后的像素。做完逐张看图，挡住结构就挪位置。
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont
COL = {'primary': (22, 50, 79), 'accent': (238, 99, 72), 'teal': (24, 128, 128), 'highlight': (255, 212, 92)}
spec = json.load(open(sys.argv[1], encoding='utf-8')); font = sys.argv[sys.argv.index('--font') + 1]
col = lambda c: COL.get(c) or tuple(int(c.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
for s in spec:
    im = Image.open(s['src']).convert('RGB')
    if s.get('crop'): im = im.crop(tuple(s['crop']))
    k = s.get('scale', 1); im = im.resize((im.width * k, im.height * k), Image.LANCZOS) if k != 1 else im
    d = ImageDraw.Draw(im); fs = s.get('fs', 36); f = ImageFont.truetype(font, fs)
    for t, (x, y), pt, c in s.get('labels', []):
        c = col(c); tw = d.textlength(t, font=f); box = [x, y, x + tw + 28, y + fs + 20]
        if pt:
            cx = min(max(pt[0], box[0]), box[2]); cy = min(max(pt[1], box[1]), box[3])
            d.line([cx, cy, *pt], fill='white', width=6); d.line([cx, cy, *pt], fill=c, width=3)
            d.ellipse([pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8], fill=c, outline='white', width=3)
        d.rounded_rectangle(box, 14, fill=c); d.text((x + 14, y + 7), t, font=f, fill=(22, 50, 79) if c == COL['highlight'] else 'white')
    dr = s.get('dirs', {}); df = ImageFont.truetype(font, max(24, fs * 3 // 4)); W, H = im.size
    pos = {'top': lambda tw: (W / 2 - tw / 2, 16), 'bottom': lambda tw: (W / 2 - tw / 2, H - df.size - 28),
           'left': lambda tw: (16, H / 2), 'right': lambda tw: (W - tw - 40, H / 2), 'corner': lambda tw: (W - tw - 40, 16)}
    for key, t in dr.items():
        if not t: continue
        tw = d.textlength(t, font=df); x, y = pos[key](tw)
        d.rounded_rectangle([x - 12, y - 4, x + tw + 12, y + df.size + 12], 10, fill='white'); d.text((x, y), t, font=df, fill=COL['primary'])
    im.save(s['out'], quality=93); print(s['out'], im.size)
