#!/usr/bin/env python3
"""图中英文标注 → 中文：OCR 定位 → 抹掉英文（OpenCV 修补，补出背景纹理）→ 原位写中文。不用色块盖，不模糊。

三步：
  1) python3 relabel.py ocr     img1.jpg [img2.jpg …]            # 每张图生成 <图>.ocr.json（两遍：整图 + 分块，补小字）
  2) python3 relabel.py preview labels.json img.jpg …            # 生成 <图>.check.jpg：绿框=能翻译，红框=词典里没有；框旁是序号
     → 补 labels.json（词典）和 fixes.json（漏检的框、要跳过的框、改字号等），直到红框都处理掉
  3) python3 relabel.py apply   labels.json img.jpg … --font 字体.otf [--fixes fixes.json] [--out 目录]
     → 输出 <out>/<原名>.zh.jpg，然后**逐张看图**核对

labels.json 格式：
  {"abbr": {"LD": "背阔肌", "Rm": "小菱形肌"},        # 缩写，区分大小写（Rm≠RM）
   "words": {"medial": "内侧", "latissimus dorsi": "背阔肌"}}  # 词组，不分大小写、忽略空格和句点，自动去掉结尾的 "m."
fixes.json 格式（键为图片文件名，都可省略）：
  {"x60.jpg": {"extra": [[x0,y0,x1,y1,"英文"]],   # OCR 漏检的框（原图像素）；高明显大于宽的框按竖排写
               "skip": [3, 7],                       # 不处理的 OCR 序号（见 check 图）
               "text": {"5": "Trap"},                # 改正 OCR 识别错的文字
               "zh": {"LT": "最长肌"},                # 这张图里单独改译法（比如改短）
               "pos": {"OCS": [2370, 537]},          # 中文写到指定中心点，避免重叠
               "erase": [[x0,y0,x1,y1]],             # 只抹不写（水印、机型名）
               "size": 0.85}}                        # 本图字号倍数
依赖：rapidocr_onnxruntime（OCR，仅第 1 步需要）、opencv-python、numpy、Pillow
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


def iou(a, b):
    x0, y0 = max(a[0], b[0]), max(a[1], b[1]); x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    if x1 <= x0 or y1 <= y0: return 0
    return (x1 - x0) * (y1 - y0) / min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))


def ocr(paths):
    from rapidocr_onnxruntime import RapidOCR
    eng = RapidOCR(); tmp = '/tmp/_relabel_ocr.png'
    for p in paths:
        im = Image.open(p).convert('RGB'); W, H = im.size; rows = []
        s = min(1, 2400 / W); im.resize((round(W * s), round(H * s))).save(tmp)
        for box, t, cf in (eng(tmp)[0] or []):
            xs = [q[0] / s for q in box]; ys = [q[1] / s for q in box]
            rows.append([round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys)), t, round(float(cf), 2)])
        for inv in (False, True):  # 第二遍：分块 + 反色，补小字和深底浅字
            src = ImageOps.invert(im) if inv else im
            for ty in range(0, H, 1100):
                for tx in range(0, W, 1100):
                    src.crop((tx, ty, min(W, tx + 1400), min(H, ty + 1400))).save(tmp)
                    for box, t, cf in (eng(tmp)[0] or []):
                        if float(cf) < .6: continue
                        b = [round(min(q[0] for q in box) + tx), round(min(q[1] for q in box) + ty), round(max(q[0] for q in box) + tx), round(max(q[1] for q in box) + ty), t, round(float(cf), 2)]
                        if not any(iou(b, r) > .4 for r in rows): rows.append(b)
        json.dump(rows, open(p + '.ocr.json', 'w'), ensure_ascii=False); print(p, len(rows), '个文字框')


class Labels:
    def __init__(self, path):
        d = json.load(open(path, encoding='utf-8'))
        self.abbr = d.get('abbr', {}); self.words = {self.norm(k).lower(): v for k, v in d.get('words', {}).items()}

    @staticmethod
    def norm(t):
        for ch in ' .,，()（）': t = t.replace(ch, '')
        return t.lstrip('-')

    def __call__(self, t):
        k = self.norm(t)
        if k in self.abbr: return self.abbr[k]
        lk = k.lower()
        for c in (lk, lk[:-1] if lk.endswith('m') else None):
            if c and c in self.words: return self.words[c]
        return None


def boxes(p, L, fx):
    rows = [list(r) for r in json.load(open(p + '.ocr.json'))] if os.path.exists(p + '.ocr.json') else []
    for i, t in fx.get('text', {}).items(): rows[int(i)][4] = t
    rows = [r for i, r in enumerate(rows) if i not in set(fx.get('skip', []))]
    rows += [list(r) + [1.0] for r in fx.get('extra', [])]
    zh = lambda t: fx.get('zh', {}).get(t) or L(t)
    rows.sort(key=lambda r: (r[1], r[0])); used = set(); out = []
    for i, a in enumerate(rows):  # 长名称常被拆成上下两行，能合成词典词条就合并
        if i in used: continue
        cur = a[:]
        for _ in range(2):
            ha = cur[3] - cur[1]
            for j, b in enumerate(rows):
                if j in used or j == i: continue
                gap = b[1] - cur[3]; ov = min(cur[2], b[2]) - max(cur[0], b[0])
                if -.3 * ha < gap < .9 * ha and ov > .2 * min(cur[2] - cur[0], b[2] - b[0]):
                    t = cur[4] + ' ' + b[4]
                    if b[4].replace('.', '').strip() == 'm' or (zh(t) and not zh(cur[4])):
                        cur = [min(cur[0], b[0]), cur[1], max(cur[2], b[2]), b[3], t, 1.0]; used.add(j); break
        out.append(cur[:6])
    return [r for r in out if zh(r[4])], zh


def erase(img, box, lh):
    import cv2
    H, W = img.shape[:2]; x0, y0, x1, y1 = [int(v) for v in box]; p = int(lh * .35)
    X0, Y0, X1, Y1 = max(0, x0 - p), max(0, y0 - p), min(W, x1 + p), min(H, y1 + p)
    g = cv2.cvtColor(img[Y0:Y1, X0:X1], cv2.COLOR_RGB2GRAY).astype(int)
    bg = np.median(np.concatenate([g[:3].ravel(), g[-3:].ravel(), g[:, :3].ravel(), g[:, -3:].ravel()]))
    m = ((np.abs(g - bg) > 38)).astype(np.uint8) * 255
    inner = np.zeros_like(m); inner[p // 2:m.shape[0] - p // 2, p // 2:m.shape[1] - p // 2] = 1; m *= inner
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=max(2, int(lh * .08)))
    full = np.zeros((H, W), np.uint8); full[Y0:Y1, X0:X1] = m
    return cv2.inpaint(img, full, max(3, int(lh * .25)), cv2.INPAINT_TELEA)


def apply(p, L, fx, font, out):
    bs, zh = boxes(p, L, fx); img = np.asarray(Image.open(p).convert('RGB')).copy()
    nl = lambda b: zh(b[4]).count('\n') + 1  # 译文可用 \n 分行（多行英文合并成一个框时）
    lh = lambda b: min(b[3] - b[1], b[2] - b[0]) if (b[3] - b[1]) > 1.6 * (b[2] - b[0]) and nl(b) == 1 else (b[3] - b[1]) / nl(b)
    for b in bs: img = erase(img, b[:4], lh(b))
    for b in fx.get('erase', []): img = erase(img, b, (b[3] - b[1]) * .8)
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    if bs:
        base = sorted(lh(b) for b in bs)[len(bs) // 2]; fs = int(base * 1.15 * fx.get('size', 1.0)); f = ImageFont.truetype(font, fs)
        for b in bs:
            t = zh(b[4]); tw = max(d.textlength(q, font=f) for q in t.split('\n'))
            cx, cy = fx.get('pos', {}).get(b[4], ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
            light = np.asarray(im.convert('L').crop(tuple(int(v) for v in b[:4]))).mean() >= 170
            fill, st = ((20, 20, 20), (255, 255, 255)) if light else ((255, 255, 255), (0, 0, 0))
            if (b[3] - b[1]) > 1.6 * (b[2] - b[0]) and len(t) > 1 and '\n' not in t:  # 竖排
                tmp = Image.new('RGBA', (int(tw) + 20, int(fs * 1.5)), (0, 0, 0, 0))
                ImageDraw.Draw(tmp).text((10, fs * .1), t, font=f, fill=fill, stroke_width=max(2, fs // 12), stroke_fill=st)
                tmp = tmp.rotate(90, expand=True); im.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)), tmp); continue
            ls = t.split('\n')
            for k, ln in enumerate(ls):
                tw = d.textlength(ln, font=f); x = max(4, min(im.width - tw - 4, cx - tw / 2))
                d.text((x, cy - fs * .62 + (k - (len(ls) - 1) / 2) * fs * 1.25), ln, font=f, fill=fill, stroke_width=max(2, fs // 12), stroke_fill=st)
    os.makedirs(out, exist_ok=True); o = os.path.join(out, os.path.splitext(os.path.basename(p))[0] + '.zh.jpg')
    im.save(o, quality=92); print(o, len(bs), '处标注')


def preview(p, L):
    im = Image.open(p).convert('RGB'); d = ImageDraw.Draw(im); fs = max(18, im.width // 80)
    rows = json.load(open(p + '.ocr.json')) if os.path.exists(p + '.ocr.json') else []
    for i, (x0, y0, x1, y1, t, c) in enumerate(rows):
        d.rectangle([x0, y0, x1, y1], outline=(0, 200, 0) if L(t) else (255, 0, 0), width=max(3, fs // 6))
        d.text((x0, y1 + 2), str(i), fill=(255, 200, 0))
    o = os.path.splitext(p)[0] + '.check.jpg'; im.thumbnail((1800, 1800)); im.save(o, quality=82)
    miss = [(i, r[4]) for i, r in enumerate(rows) if not L(r[4])]
    print(o, '未翻译：', miss)


if __name__ == '__main__':
    cmd, a = sys.argv[1], sys.argv[2:]
    opt = lambda k, dft=None: a[a.index(k) + 1] if k in a else dft
    files = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or not a[i - 1].startswith('--'))]
    if cmd == 'ocr': ocr(files)
    else:
        L = Labels(files[0]); fixes = json.load(open(opt('--fixes'), encoding='utf-8')) if opt('--fixes') else {}
        for p in files[1:]:
            if cmd == 'preview': preview(p, L)
            elif cmd == 'apply': apply(p, L, fixes.get(os.path.basename(p), {}), opt('--font'), opt('--out', os.path.dirname(p) or '.'))
