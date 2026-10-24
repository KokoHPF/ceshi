"""给原文示意图（图 2、图 3A/B/C）加中文结构标注和方向标注，输出到 src/zh/。
标注坐标为放大后图像像素；每条标注：(文字, 标签左上角, 指向点或 None, 颜色)。
用法：python3 tools/annotate.py <思源黑体 Bold 字体文件>"""
import sys
from PIL import Image, ImageDraw, ImageFont
FONT = sys.argv[1]
NAVY = (22, 50, 79); CORAL = (238, 99, 72); TEAL = (24, 128, 128); YEL = (255, 212, 92)


def label(im, items, fs):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, fs)
    for t, (x, y), pt, col in items:
        tw = d.textlength(t, font=f); box = [x, y, x + tw + 28, y + fs + 20]
        if pt:  # 引线：从标签最近的边到指向点
            cx = min(max(pt[0], box[0]), box[2]); cy = min(max(pt[1], box[1]), box[3])
            d.line([cx, cy, pt[0], pt[1]], fill='white', width=6); d.line([cx, cy, pt[0], pt[1]], fill=col, width=3)
            d.ellipse([pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8], fill=col, outline='white', width=3)
        d.rounded_rectangle(box, 14, fill=col); d.text((x + 14, y + 7), t, font=f, fill='white' if col != YEL else NAVY)
    return im


def dirs(im, top, bottom, left=None, right=None, fs=30):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, fs); W, H = im.size
    for t, (x, y) in ((top, (W / 2, 16)), (bottom, (W / 2, H - fs - 24)), (left, (16, H / 2)), (right, (W - 16, 16))):
        if not t: continue
        tw = d.textlength(t, font=f); x0 = x - tw / 2 - 12 if x not in (16, W - 16) else (16 if x == 16 else W - 16 - tw - 24)
        d.rounded_rectangle([x0, y - 4, x0 + tw + 24, y + fs + 12], 10, fill=(255, 255, 255)); d.text((x0 + 12, y), t, font=f, fill=NAVY)


g2 = Image.open('src/x_gr2.jpg').convert('RGB'); g2 = g2.resize((g2.width * 2, g2.height * 2), Image.LANCZOS)
label(g2, [('肩胛骨', (60, 300), (300, 470), TEAL), ('关节盂', (380, 150), (520, 380), TEAL),
           ('肱骨头', (900, 280), (780, 520), NAVY), ('肱骨头向后半脱位', (690, 700), (720, 640), CORAL),
           ('后盂唇撕裂处受压', (60, 640), (540, 600), CORAL)], 40)
dirs(g2, '前', '后', fs=36)
g2.save('src/zh/fig2.jpg', quality=93)

g3 = Image.open('src/x_gr3.jpg').convert('RGB')
P = {'A': g3.crop((0, 0, 233, 285)), 'B': g3.crop((239, 0, 446, 285)), 'C': g3.crop((453, 0, 758, 285))}
for k in P: P[k] = P[k].resize((P[k].width * 3, P[k].height * 3), Image.LANCZOS)
label(P['A'], [('关节盂', (20, 340), (300, 520), TEAL), ('肱骨头', (430, 300), (450, 520), NAVY),
               ('检查者拇指', (20, 600), (250, 720), CORAL), ('向前顶＝“后方骨块”', (20, 770), (560, 750), CORAL)], 34)
label(P['B'], [('手指勾住前方锁骨', (60, 110), (237, 412), TEAL), ('拇指顶在后方关节线', (40, 770), (540, 730), CORAL)], 32)
label(P['C'], [('手指搭在锁骨上', (110, 30), (420, 120), TEAL), ('拇指从后方顶住', (20, 430), (318, 600), CORAL),
               ('肱骨头与关节盂', (520, 770), (470, 560), NAVY)], 32)
for k in 'AB': dirs(P[k], None, None, None, '上前·下后', fs=26)
dirs(P['C'], None, None, None, '左后·右前', fs=26)
for k, im in P.items(): im.save(f'src/zh/fig3{k}.jpg', quality=93)
print('ok', g2.size, {k: v.size for k, v in P.items()})
