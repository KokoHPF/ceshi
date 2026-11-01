#!/usr/bin/env python3
"""label_figure：在原图的数字 / 字母 / 英文标注旁直接写中文名称，并可在图下加黑底中文图例条。

用法：python3 label_figure.py spec.json 字体目录
spec.json 是一个列表，每项对应一张图：
[
  {"src": "work/x108.jpg", "out": "work/f01.jpg", "fs": 30,
   "items": [[421, 387, "后腹", "c", 140],      # 带第 5 项(最小宽度) = 不透明框，用来完全盖住原英文
             [600, 200, "距骨", "l"]],          # 4 项 = 半透明小框，放在数字旁边，不盖原标注
   "strip": ["a 冈上肌前腹与后腹", "b、c 轴位：实线箭头 = 前腹长腱"]}
]
- 坐标一律是【原图像素】（x, y 为标签中心或左/右边缘）；锚点 l=从 x 向右，r=到 x 结束，c=以 x 居中。
- 先用原分辨率裁图 + 网格核对坐标，不要在缩小显示的图上读坐标（这是最常见的错位原因）。
- 中文放在数字旁边、空白处，不压住结构和箭头；没有空间时只写进 strip。
- 只在许可允许演绎时修改原图（CC BY 等）；ND / 非开放获取的图保持原样，说明写进卡片文字。
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

BOX = (20, 30, 50, 200)
TXT = (255, 255, 255, 255)


def run(spec, fontdir):
    font = lambda s: ImageFont.truetype(os.path.join(fontdir, 'NotoSansSC-Bold.otf'), s)
    for e in spec:
        fs = e.get('fs', 28); strip = e.get('strip') or []
        im = Image.open(e['src']).convert('RGBA'); top = im.height
        if strip:
            h = round(len(strip) * fs * 1.6 + fs * 1.2)
            c = Image.new('RGBA', (im.width, im.height + h), (0, 0, 0, 255)); c.paste(im, (0, 0)); im = c
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); f = font(fs); pad = round(fs * .3)
        for it in e.get('items', []):
            x, y, t, a = it[:4]; opaque = len(it) > 4
            w = max(d.textlength(t, font=f), (it[4] - 2 * pad) if opaque else 0)
            x0 = {'l': x, 'r': x - w - 2 * pad, 'c': x - w / 2 - pad}[a]; y0 = y - fs / 2 - pad
            d.rounded_rectangle([x0, y0, x0 + w + 2 * pad, y0 + fs + 2 * pad], pad, fill=BOX[:3] + (255,) if opaque else BOX)
            d.text((x0 + pad + w / 2, y0 + pad + fs * .45), t, font=f, fill=TXT, anchor='mm')
        for i, t in enumerate(strip):
            d.text((round(fs * .8), top + round(fs * .6) + i * fs * 1.6), t, font=f, fill=TXT)
        out = Image.alpha_composite(im, ov).convert('RGB')
        os.makedirs(os.path.dirname(e['out']) or '.', exist_ok=True); out.save(e['out'], quality=92)
        print(e['out'], out.size)


if __name__ == '__main__':
    run(json.load(open(sys.argv[1], encoding='utf-8')), sys.argv[2] if len(sys.argv) > 2 else 'fonts')
