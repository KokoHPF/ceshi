"""原文图 1～3 的箭头和文字是 PDF 矢量叠加层，按页面渲染裁切（300 dpi）后把英文标签换成中文。
用法：python3 tools/render_figs.py <思源黑体 Bold 字体文件>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
FONT = sys.argv[1]
d = pymupdf.open('src/paper.pdf')
CLIP = {1: (2, (49, 53, 286, 195)), 2: (2, (309, 53, 547, 266)), 3: (3, (48, 54, 287, 319))}
for n, (pg, r) in CLIP.items():
    pix = d[pg].get_pixmap(dpi=300, clip=pymupdf.Rect(*r)); im = Image.open(BytesIO(pix.tobytes('png'))).convert('RGB')
    if n == 1:  # 白底标签框 "Middle trapezius"（页面坐标 51,57～104,67）
        s = 300 / 72; dr = ImageDraw.Draw(im)
        x0, y0, x1, y1 = [round(v * s) for v in ((51 - r[0]), (57 - r[1]), (104 - r[0]), (67 - r[1]))]
        dr.rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], fill='white')  # 原白底黑框保留，只换框内文字
        f = ImageFont.truetype(FONT, round((y1 - y0) * .7)); tw = dr.textlength('中斜方肌', font=f)
        dr.text(((x0 + x1 - tw) / 2, y0 + (y1 - y0) * .1), '中斜方肌', font=f, fill='black')
    im.save(f'src/zh/fig{n}.jpg', quality=92); print(n, im.size)
