#!/usr/bin/env python3
"""把卡片打包成 zip（文件夹按篇分），文件按发布顺序命名。
用法：python3 pack.py 输出.zip 文件夹名=卡片目录 [文件夹名2=卡片目录2 …]
例：  python3 pack.py 椎旁肌.zip 上篇=out/shang 中篇=out/zhong 下篇=out/xia
"""
import glob, os, sys, zipfile
out = sys.argv[1]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for arg in sys.argv[2:]:
        name, d = arg.split('=', 1)
        for i, f in enumerate(sorted(glob.glob(os.path.join(d, 'card*.jpg'))), 1):
            z.write(f, f'{name}/{name}_{i:02d}.jpg')
print(out, os.path.getsize(out), 'bytes')
