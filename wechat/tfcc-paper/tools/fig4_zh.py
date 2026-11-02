#!/usr/bin/env python3
"""原文图 4（TFCC 五部分）完整中文化：色带上的英文缩写按文字颜色选出像素后用周围色带修补（OpenCV inpaint），再沿色带方向写中文；编号圆圈 ①–⑤ 保护不动。
输入 work/zh/x69.zh.jpg（骨名已由 relabel.py 改中文），输出覆盖同一文件的 *_full 版：work/zh/x69.full.jpg。坐标为原图像素。"""
import math, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
FB = sys.argv[1] if len(sys.argv) > 1 else '/tmp/xhs/fonts/NotoSansSC-Bold.otf'
im = Image.open('work/zh/x69.zh.jpg').convert('RGB'); a = np.asarray(im).copy(); H, W = a.shape[:2]
CIRCLES = [(643, 598), (706, 598), (770, 642), (535, 685), (510, 795), (838, 520), (910, 462)]
yy, xx = np.mgrid[0:H, 0:W]
protect = np.zeros((H, W), bool)
for cx, cy in CIRCLES: protect |= (xx - cx) ** 2 + (yy - cy) ** 2 <= 25 ** 2
def rect_mask(cx, cy, w, h, ang):
    t = math.radians(ang); ux, uy = math.cos(t), -math.sin(t); vx, vy = -uy, ux
    dx, dy = xx - cx, yy - cy
    return (np.abs(dx * ux + dy * uy) <= w / 2) & (np.abs(dx * vx + dy * vy) <= h / 2)
# (原文字区域 cx, cy, w, h, 角度) → (中文, 字号, 写字中心, 角度)
L = [((608, 560, 74, 36, 20), ('尺月\n韧带', 23, (606, 548), 20)),
     ((718, 550, 70, 34, -5), ('尺三角\n韧带', 23, (716, 540), -5)),
     ((688, 648, 124, 36, 0), ('掌侧桡尺韧带', 21, (680, 648), 0)),
     ((648, 698, 160, 34, 15), ('关节盘', 26, (648, 698), 15)),
     ((620, 772, 136, 42, 17), ('背侧桡尺韧带', 23, (640, 765), 17)),
     ((829, 570, 78, 36, 0), ('半月板\n同系物', 17, (821, 574), 0, 'w')),
     ((828, 682, 50, 36, 0), ('尺骨\n茎突', 17, (828, 682), 0)),
     ((884, 618, 292, 44, 70), ('尺侧腕伸肌腱下鞘', 25, (884, 620), 70)),
     ((768, 972, 74, 38, 0), ('尺侧\n腕伸肌', 20, (766, 970), 0, 'w'))]
for (cx, cy, w, h, ang), _ in L:
    m = rect_mask(cx, cy, w, h, ang) & ~protect
    r, g, b = [a[..., i].astype(int) for i in range(3)]
    txt = m & (r < 95) & (g < 105) & (b < 130)          # 原文深蓝色文字（紫、绿、品红色带本身不会被选中）
    txt = cv2.dilate(txt.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2).astype(bool) & ~protect
    a = cv2.inpaint(a, txt.astype(np.uint8) * 255, 5, cv2.INPAINT_TELEA)
out = Image.fromarray(a)
for _, (t, fs, (cx, cy), ang, *c) in L:
    f = ImageFont.truetype(FB, fs); lines = t.split('\n')
    tw = max(ImageDraw.Draw(out).textlength(s, font=f) for s in lines); th = fs * 1.2 * len(lines)
    tmp = Image.new('RGBA', (int(tw) + 8, int(th) + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    for i, s in enumerate(lines): d.text((tmp.width / 2, 4 + fs * .6 + i * fs * 1.2), s, font=f, fill=(255, 255, 255) if c else (25, 30, 60), anchor='mm')
    tmp = tmp.rotate(ang, expand=True, resample=Image.BICUBIC); out.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)), tmp)
out.save('work/zh/x69.full.jpg', quality=93); print('ok')
