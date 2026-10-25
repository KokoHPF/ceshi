"""手工原位替换：图 1、3、4、5 图内英文与缩写（T、F）改中文。用法：python3 tools/translate_figs.py src/raw src 中文字体（原图是从原文 PDF 抽出的位图）"""
import sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
RAW, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, int(s))

def load(n): return cv2.imread(f'{RAW}/{n}.jpg')

def erase(img, box, cond, pad=3, inpaint=True):
    x0, y0, x1, y1 = box; x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    sub = img[y0:y1, x0:x1].astype(int)
    m = np.zeros(img.shape[:2], np.uint8); m[y0:y1, x0:x1] = cond(sub).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=2)
    if inpaint: return cv2.inpaint(img, m, 6, cv2.INPAINT_TELEA)
    img = img.copy(); img[m > 0] = 255; return img

def color(img, box, cond):
    x0, y0, x1, y1 = box; sub = img[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    s = sub[cond(sub)]; c = np.median(s, 0) if len(s) else (0, 0, 0)
    return (int(c[2]), int(c[1]), int(c[0]))

def write(pil, text, cx, cy, size, fill, stroke=0, anchor='mm'):
    ImageDraw.Draw(pil).text((cx, cy), text, font=font(size), fill=fill, anchor=anchor,
                             stroke_width=stroke, stroke_fill=(255, 255, 255))

dark = lambda s: s.sum(-1) < 3 * 110
nonwhite = lambda s: s.min(-1) < 215
blue = lambda s: (s[..., 0] - s[..., 2] > 40)
teal = lambda s: (s[..., 1] - s[..., 2] > 25)
teal_aa = lambda s: (s[..., 1] - s[..., 2] > 8)
blue_aa = lambda s: (s.min(-1) < 248) & (s[..., 2] - s[..., 0] < 50)  # 非白且非肤色

def to_pil(img): return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def bones(img, items):
    """items: (box, 文字, 加白描边)"""
    for box, _, _ in items: img = erase(img, box, dark)
    pil = to_pil(img)
    for (x0, y0, x1, y1), t, st in items:
        h = y1 - y0; cx = min((x0 + x1) / 2, pil.width - 30 - h * 0.95)
        write(pil, t, cx, (y0 + y1) / 2, h * 0.95, (0, 0, 0), stroke=2 if st else 0)
    return pil

def compass(img, words, size):
    cols = [color(img, b, nonwhite) for b, _ in words]
    for b, _ in words: img = erase(img, b, nonwhite, pad=2, inpaint=False)
    pil = to_pil(img)
    for ((x0, y0, x1, y1), t), c in zip(words, cols):
        write(pil, t, (x0 + x1) / 2, (y0 + y1) / 2, size, c)
    return pil

def cv(pil): return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)

# 图 1：入路标签（蓝字下有虚线，只擦虚线上方的字）
img = load('figA_p3L')
labs = [((6, 631, 284, 666), '前入路', 'l', 668), ((597, 701, 893, 735), '后内侧入路', 'r', 737)]  # 最后一项：虚线顶端所在行
cols = [color(img, b, blue) for b, *_ in labs]
for b, _, _, dtop in labs:
    # 字下方的虚线一起挖掉再修补，免得修补时把蓝色虚线“抹”进字的位置；修补完再把虚线原样放回
    x0, y0, x1, y1 = b
    m = np.zeros(img.shape[:2], np.uint8)
    m[y0 - 2:dtop, max(x0 - 2, 0):x1 + 2] = blue_aa(img[y0 - 2:dtop, max(x0 - 2, 0):x1 + 2].astype(int))
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=3); m[dtop:] = 0
    dash = np.zeros_like(m); dash[dtop - 1:dtop + 8, max(x0 - 10, 0):x1 + 10] = blue_aa(img[dtop - 1:dtop + 8, max(x0 - 10, 0):x1 + 10].astype(int))
    fixed = cv2.inpaint(img, ((m | dash) > 0).astype(np.uint8) * 255, 6, cv2.INPAINT_TELEA)
    fixed[dash > 0] = img[dash > 0]; img = fixed
pil = to_pil(img)
for ((x0, y0, x1, y1), t, al, _), c in zip(labs, cols):
    write(pil, t, x0 if al == 'l' else x1, y1 - 2, 34, c, anchor='ld' if al == 'l' else 'rd')
pil.save(f'{OUT}/fig1_zh.jpg', quality=92)

# 图 3、4：前入路 / 后内侧入路示意
def scheme(name, bonelist, needle, comp, out):
    img = load(name)
    pil = bones(img, bonelist)
    img = cv(pil)
    nc = color(img, needle, teal)
    img = erase(img, needle, teal_aa, pad=4)
    pil = to_pil(img)
    x0, y0, x1, y1 = needle; write(pil, '针', (x0 + x1) / 2, (y0 + y1) / 2, 36, nc)
    pil = compass(cv(pil), comp, 18)
    pil.save(f'{OUT}/{out}', quality=92)

scheme('fig3', [((493, 154, 515, 182), '胫骨', 0), ((285, 259, 304, 286), '腓骨', 0),
                ((1048, 388, 1069, 415), '胫骨', 1), ((709, 500, 727, 527), '腓骨', 1)],
       (815, 111, 933, 144),
       [((523, 525, 572, 541), '前侧'), ((471, 571, 515, 587), '外侧'), ((581, 571, 625, 586), '内侧'), ((519, 611, 575, 629), '后侧')],
       'fig3_zh.jpg')
scheme('fig4', [((488, 135, 510, 162), '胫骨', 0), ((280, 239, 298, 267), '腓骨', 0),
                ((886, 99, 907, 127), '胫骨', 1), ((1891, 20, 1913, 48), '胫骨', 1)],
       (1069, 515, 1191, 552),
       [((517, 504, 565, 519), '前侧'), ((463, 548, 508, 565), '外侧'), ((576, 549, 618, 563), '内侧'), ((514, 591, 568, 606), '后侧')],
       'fig4_zh.jpg')

# 图 5：解剖断面
img = load('fig5')
pil = bones(img, [((298, 420, 329, 459), '胫骨', 0), ((502, 235, 528, 274), '腓骨', 0),
                  ((1289, 507, 1320, 545), '胫骨', 0), ((1366, 217, 1393, 256), '腓骨', 0)])
pil = compass(cv(pil), [((963, 583, 1035, 607), '外侧'), ((863, 657, 941, 678), '前侧'),
                        ((1058, 659, 1148, 679), '后侧'), ((967, 729, 1036, 753), '内侧')], 22)
pil.save(f'{OUT}/fig5_zh.jpg', quality=92)
print('ok')
