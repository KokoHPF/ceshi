#!/usr/bin/env python3
"""原文图 3（流程图）英文改中文：先用 relabel.py 处理 3 处标注并抹掉中间“Generate physiological curvature data”，
再在原位写三行中文。图中软件界面截图里的中文、Cobb 角测量标注保持原样。
  R=../../skills/paper-to-xhs-cards/scripts/relabel.py
  python3 $R ocr work/x290.jpg；python3 $R apply work/labels.json work/x290.jpg --font <粗体> --fixes work/fixes.json --out work
用法：python3 prep.py <work 目录> <粗体>"""
import sys
from PIL import Image, ImageDraw, ImageFont
W, FB = sys.argv[1:3]
im = Image.open(f'{W}/x290.zh.jpg').convert('RGB'); d = ImageDraw.Draw(im); f = ImageFont.truetype(FB, 26)
for i, t in enumerate(['生成', '生理曲度', '数据']):
    d.text((850, 340 + i * 36), t, font=f, fill=(90, 40, 140), anchor='mm')
im.save(f'{W}/x290.zh2.jpg', quality=93); print('ok')
