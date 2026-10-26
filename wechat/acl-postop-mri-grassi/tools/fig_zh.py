#!/usr/bin/env python3
"""原文图里烧进像素的英文原位换成中文（其余标注只有面板字母、测量线字母、数字和星号，原样保留）。
- 图 7B 左下角黄色方位标记 "A"（anterior，前方）→ "前"
- 图 15 测量软件残留的 "Perim.: 118.40 mm" "Area: 1114.51 mm" → "周长：118.40 mm" "面积：1114.51 mm"
用法：python3 tools/fig_zh.py src <中文字体>   # 生成 src/fig7_zh.png、src/fig15_zh.png
src/figN.png 是从原文 PDF 按 400 dpi 渲染后裁出的整幅图（含 PDF 里叠加的矢量标注）。"""
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, F = sys.argv[1:3]
font = lambda s: ImageFont.truetype(F, s)

# 图 7B：黑底上的黄色 "A"，涂黑后写 "前"
im = Image.open(f'{SRC}/fig7.png').convert('RGB'); dr = ImageDraw.Draw(im)
dr.rectangle([562, 636, 596, 672], fill=(0, 0, 0))
dr.text((564, 638), '前', font=font(28), fill=(235, 225, 120))
im.save(f'{SRC}/fig7_zh.png')

# 图 15：两行白色等宽小字压在 MRI 上，换成半透明深色底的中文标签
im = Image.open(f'{SRC}/fig15.png').convert('RGBA')
ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
dr.rectangle([492, 419, 684, 450], fill=(20, 20, 20, 235))
dr.text((496, 419), '周长：118.40 mm', font=font(14), fill=(255, 255, 255, 255))
dr.text((496, 434), '面积：1114.51 mm', font=font(14), fill=(255, 255, 255, 255))
Image.alpha_composite(im, ov).convert('RGB').save(f'{SRC}/fig15_zh.png')
print('done')
