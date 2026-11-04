#!/usr/bin/env python3
"""从 extract_figures.py 导出的原图（work/x*.jpg）按白色间隙切分小图，只裁切、不改动像素。用法：python3 tools/crop.py work"""
import sys
from PIL import Image
import numpy as np
W = sys.argv[1]
def trim(im, pad=6):
    g = np.array(im.convert('L')) < 235; ys, xs = np.where(g)
    return im.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad, im.width), min(ys.max() + pad, im.height)))
def cut(src, boxes):
    im = Image.open(f'{W}/{src}.jpg').convert('RGB')
    for name, b in boxes.items(): trim(im.crop(b)).save(f'{W}/{name}.jpg', quality=95)
cut('x53', {'f1': (0, 0, 1280, 810)}); cut('x54', {'f2': (0, 0, 980, 543)}); cut('x55', {'f3': (0, 0, 1200, 732)})
cut('x63', {'f4a': (0, 0, 630, 1275), 'f4b': (695, 0, 1325, 1275), 'f4c': (1390, 0, 2020, 1275)})
cut('x67', {'f5': (0, 0, 980, 1283)}); cut('x68', {'f6': (0, 0, 570, 760)}); cut('x69', {'f7': (0, 0, 472, 1040)})
cut('x73', {'f8': (0, 0, 980, 1192)}); cut('x74', {'f9a': (0, 0, 690, 500), 'f9b': (700, 0, 1400, 500)})
cut('x78', {'f10a': (0, 0, 422, 464), 'f10b': (422, 0, 846, 464), 'f10c': (846, 0, 1262, 464)})
