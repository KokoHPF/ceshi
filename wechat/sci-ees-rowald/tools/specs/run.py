import sys, importlib
sys.path.insert(0, 'tools'); sys.path.insert(0, 'src/t')
import zh
from PIL import Image
for a in sys.argv[1:]:
    f, x = a.split(':'); m = importlib.import_module(f); importlib.reload(m)
    im, left = zh.apply(Image.open(f'src/x{x}.png'), f'src/o{x}.json', m.SPEC, extra=m.EXTRA)
    im.save(f'src/z{x}.png'); print(f, '未处理：', left)
