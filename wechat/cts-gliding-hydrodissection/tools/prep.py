#!/usr/bin/env python3
"""原文图 1、2 右侧的英文说明栏裁掉（中文说明写进图注和卡片），照片部分上下拼接；图 3 两张超声上下拼接。
原文 CC BY-NC 3.0，允许演绎。用法：python3 prep.py <work 目录>"""
import sys
from PIL import Image
W = sys.argv[1]
o = lambda x: Image.open(f'{W}/x{x}.jpg').convert('RGB')
def stack(ims, name, gap=8):
    w = max(i.width for i in ims); c = Image.new('RGB', (w, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: c.paste(i, (0, y)); y += i.height + gap
    c.save(f'{W}/{name}.jpg', quality=93); return c
t = o(2069).crop((0, 0, 368, 438)); n = o(2070).crop((0, 0, 368, 223))
c = o(2071).crop((0, 0, 368, 222)); s = o(2072).crop((0, 0, 368, 388))
t.save(f'{W}/tendon.jpg', quality=93); n.save(f'{W}/nerve.jpg', quality=93); c.save(f'{W}/chin.jpg', quality=93); s.save(f'{W}/shoulder.jpg', quality=93)
stack([t, n], 'fig1'); stack([c, s], 'fig2'); stack([o(2073), o(2074)], 'fig3')
print('ok')
