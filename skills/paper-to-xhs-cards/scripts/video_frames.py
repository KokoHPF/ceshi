#!/usr/bin/env python3
"""视频截帧：先出总览挑时间点，再按时间点截高清帧。

用法：
  python3 video_frames.py video.mp4 out_dir --sheet 3        每 3 秒一帧，生成 out_dir/_sheet.jpg（帧上标秒数）
  python3 video_frames.py video.mp4 out_dir --at 22 25 53    截取指定秒数，输出 out_dir/v22.png …；
                                                             竖屏视频带左右黑边时加 --crop-black 自动裁掉
依赖：ffmpeg、Pillow、numpy
"""
import os, subprocess, sys, glob
import numpy as np
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); a = sys.argv[3:]
if '--sheet' in a:
    step = float(a[a.index('--sheet') + 1]); tmp = os.path.join(out, '_s'); os.makedirs(tmp, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', v, '-vf', f'fps=1/{step},scale=320:-1', f'{tmp}/f%03d.jpg'], check=True)
    fs = sorted(glob.glob(f'{tmp}/f*.jpg')); w, h = Image.open(fs[0]).size
    sh = Image.new('RGB', (8 * (w + 2), ((len(fs) + 7) // 8) * (h + 2)), 'white'); d = ImageDraw.Draw(sh)
    for i, f in enumerate(fs):
        x, y = (i % 8) * (w + 2), (i // 8) * (h + 2); sh.paste(Image.open(f), (x, y)); d.text((x + 4, y + 2), f'{i * step:g}s', fill='yellow')
    sh.save(f'{out}/_sheet.jpg', quality=80); print('总览：', f'{out}/_sheet.jpg')
if '--at' in a:
    ts = [x for x in a[a.index('--at') + 1:] if not x.startswith('--')]
    for t in ts:
        p = f'{out}/v{t}.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', t, '-i', v, '-frames:v', '1', p], check=True)
        if '--crop-black' in a:
            im = Image.open(p).convert('RGB'); g = np.asarray(im.convert('L')).astype(int); c = (g > 12).mean(0)
            xs = [i for i in range(g.shape[1]) if c[i] > .3]
            if xs: im.crop((xs[0], 0, xs[-1] + 1, im.height)).save(p)
        print('saved', p)
