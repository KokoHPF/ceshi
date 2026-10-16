#!/usr/bin/env python3
"""Chang 2026 动态贴扎：图 3 手机测角 App 界面英文（Compare/Undo/Clear/1x）模糊；图 4 T 恤品牌字样模糊、“Start”改为“起点”；
补充视频转为 2 倍速 GIF 动图（正文用），并转码为 MP4 放入 videos/（上传永久素材，可在编辑器中插入）；封面取自图 2。
用法：python3 make_figs.py <素材目录（x01～x04.png、title.png、v.mpeg）> <输出目录>"""
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
ROOT = Path(OUT).parent
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def blur(im, boxes, r=14):
    for b in boxes:
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r)), b[:2])
    return im


def badge(im, t, left=False):
    d = ImageDraw.Draw(im); f = font(max(26, im.width // 30))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = 10 if left else im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    im.resize((W, round(im.height * W / im.width)), Image.LANCZOS).save(f'{OUT}/{name}', quality=88)


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)
save(badge(X(1), '图1'), 'img02.jpg')
x2 = X(2); save(badge(x2.copy(), '图2'), 'img03.jpg')
w, h = x2.size; ch = round(w * 383 / 900); y0 = (h - ch) // 2
x2.crop((0, y0, w, y0 + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)

x3 = blur(X(3), [(150, 25, 320, 80), (650, 660, 755, 705), (650, 745, 755, 790), (15, 1175, 105, 1235),
                 (955, 30, 1135, 85), (1480, 685, 1585, 730), (1480, 755, 1585, 805), (820, 1185, 910, 1245)])
save(badge(x3, '图3', left=True), 'img04.jpg')

x4 = blur(X(4), [(445, 275, 610, 370)], r=10)
d = ImageDraw.Draw(x4); d.rectangle([1165, 1205, 1265, 1260], fill='white')
f = font(30); d.text((1215 - d.textlength('起点', font=f) / 2, 1216), '起点', font=f, fill='black')
save(badge(x4, '图4'), 'img05.jpg')

# 补充视频：GIF（2 倍速、宽 320、6 帧/秒）+ MP4（H.264，去掉音轨）
v = f'{SRC}/v.mpeg'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-vf',
                'setpts=0.5*PTS,fps=6,scale=320:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none',
                str(ROOT / 'gifs' / 'video1.gif')], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-an', '-c:v', 'libx264', '-crf', '26', '-preset', 'slow',
                '-vf', 'scale=540:-2', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(ROOT / 'videos' / 'video1.mp4')], check=True)
