#!/usr/bin/env python3
"""论文配图英译中：在原位置把图里的英文换成中文，插画、线条、色块和数据保持不动。

两步走，中间由人（或 Claude）只填一份译文表：
  1) extract  自动找出 PDF 里的每张图，提取图中所有英文文字及其位置、字号、颜色、方向，
             生成 figs.json（版式信息）和 strings.json（去重后的英文 -> 待填中文）。
  2) render   读回填好的 strings.json，矢量图直接删原文、写中文（不经过 OCR，零识别误差）；
             没有文字层的位图走 OCR + 背景修补 + 写中文的备用路线。
             输出 zh_<图号>.png（发布用）、zh_<图号>.pdf（矢量，可无限放大）、cmp_<图号>.png（原图/译图对照）。

用法：
  python3 figtrans.py extract <论文.pdf> <工作目录> [--pages 2,3,5] [--clip 页码:x0,y0,x1,y1 ...] [--glossary 术语表.json]
  python3 figtrans.py render  <工作目录> [--dpi 300] [--only p2_1,p5_1]
  python3 figtrans.py glossary <工作目录> <术语表.json>   # 把本次译文并入长期术语表，下次自动预填

strings.json 的填写规则：
  - 值留空或与英文相同 = 不翻，保留原文（缩写、基因名、单位、通道名等）。
  - 键里的 "\\n" 是原图的换行。译文也用相同数量的 "\\n" 时逐行对位替换（适合图例、竖排列表）；
    不带 "\\n" 时在原文本框内自动重新换行。
  - figs.json 里每个文字单元的 align（l/c/r）是自动猜的，排版不对时可以手动改后重新 render。
页码一律从 1 开始。
"""
import argparse, json, os, re, sys
from collections import Counter

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/System/Library/Fonts/PingFang.ttc',
    'C:/Windows/Fonts/msyh.ttc',
]
WORD = re.compile(r'[A-Za-z]{3,}')
HASLETTER = re.compile(r'[A-Za-z]{2,}')


def find_font(path=None):
    for p in ([path] if path else []) + FONT_CANDIDATES:
        if p and os.path.exists(p): return p
    sys.exit('找不到中文字体，请用 --font 指定一个 .ttf/.ttc/.otf 文件')


def translatable(t):
    """至少有一个 3 个字母以上的单词才交给翻译；纯数字、单位、单字母面板标号直接跳过"""
    return bool(WORD.search(t))


# ---------- 坐标系：把竖排文字也当横排处理 ----------
# u 为阅读方向，v 为换行方向（下一行所在的方向）。横排 u=x, v=y；自下而上竖排 u=-y, v=x；自上而下竖排 u=y, v=-x。
def to_uv(bb, d):
    x0, y0, x1, y1 = bb
    if d == 'h': return [x0, y0, x1, y1]
    if d == 'up': return [-y1, x0, -y0, x1]
    return [y0, -x1, y1, -x0]


def from_uv(u, v, d):
    """行内一点（u, v）换回页面坐标，以及 insert_text 需要的旋转角"""
    if d == 'h': return (u, v), 0
    if d == 'up': return (v, -u), 90
    return (-v, u), -90


def line_dir(l):
    dx, dy = l['dir']
    if abs(dx) > 0.9: return 'h'
    if abs(dy) > 0.9: return 'up' if dy < 0 else 'down'
    return None  # 斜排文字不处理


# ---------- extract ----------
def body_size(page):
    c = Counter()
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']: c[round(s['size'], 1)] += len(s['text'])
    return c.most_common(1)[0][0] if c else 9


def detect_figures(page):
    """把页面上的矢量图形、嵌入图片和小号文字聚成团，每团视为一张图"""
    W, H = page.rect.width, page.rect.height
    top, bot = H * 0.06, H * 0.95
    rects = []
    for d in page.get_drawings():
        r = d['rect']
        if r.y1 < top or r.y0 > bot or r.y0 < top * 0.6 or r.is_empty and r.width < 1: continue
        if r.width > W * 0.7 and r.height < 2 or r.height > H * 0.7 and r.width < 2: continue  # 页眉线、页边竖线
        rects.append([r.x0, r.y0, r.x1, r.y1, 1, 0])
    for im in page.get_image_info():
        r = pymupdf.Rect(im['bbox']) & pymupdf.Rect(W * 0.04, top, W * 0.96, bot)  # 被裁剪的图片，外接框可能伸出页面
        if r.width < 3 or r.height < 3: continue
        rects.append([r.x0, r.y0, r.x1, r.y1, 0, 1])
    clusters = merge(rects, 16)
    clusters = [c for c in clusters if (c[2] - c[0]) * (c[3] - c[1]) > W * H * 0.002]  # 先只去掉零星小图形，分图合并后再筛
    # 把紧贴图形的短文字（图中标注）也并进来，正文和图注段落除外
    bs = body_size(page); paras = para_blocks(page)
    labels = [l['bbox'] for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])
              if len(''.join(s['text'] for s in l['spans'])) < 60 and top < l['bbox'][1] and l['bbox'][3] < bot and not any(pymupdf.Rect(l['bbox']).intersects(p) for p in paras)]
    grown = True
    while grown:  # 标签可能一个挨一个地连出去，反复扩展到不再变化
        grown = False
        for x0, y0, x1, y1 in labels:
            for c in clusters:
                if x1 > c[0] - 12 and x0 < c[2] + 12 and y1 > c[1] - 12 and y0 < c[3] + 12:
                    if x0 < c[0] or y0 < c[1] or x1 > c[2] or y1 > c[3]:
                        c[0], c[1], c[2], c[3] = min(c[0], x0), min(c[1], y0), max(c[2], x1), max(c[3], y1); grown = True
                    break
    clusters = merge(clusters, 4)
    # 同一张图的各个分图之间常有较宽的空白：中间没有正文就继续合并
    body = para_blocks(page)
    clusters = merge(clusters, 40, lambda a, b: not any(r.intersects(gap_rect(a, b)) for r in body))
    for c in clusters:  # 图注紧贴在图下方（或上方）时，把范围收回到图注之外
        mid = (c[1] + c[3]) / 2
        for p in body:
            if p.x1 > c[0] and p.x0 < c[2] and p.y1 > c[1] and p.y0 < c[3]:
                if p.y0 > mid: c[3] = min(c[3], p.y0 - 1)
                elif p.y1 < mid: c[1] = max(c[1], p.y1 + 1)
    clusters = [c for c in clusters if (c[2] - c[0]) * (c[3] - c[1]) > W * H * 0.02 and (c[4] >= 15 or c[5])]
    out = []
    for c in sorted(clusters, key=lambda c: (round(c[1] / 40), c[0])):
        out.append([max(0, c[0] - 2), max(0, c[1] - 2), min(W, c[2] + 2), min(H, c[3] + 2)])
    return out


def gap_rect(a, b):
    return pymupdf.Rect(min(a[2], b[2]), min(a[3], b[3]), max(a[0], b[0]), max(a[1], b[1])).normalize() + (-1, -1, 1, 1)


def merge(rects, gap, ok=lambda a, b: True):
    rects = [list(r) for r in rects]
    changed = True
    while changed:
        changed = False; out = []
        for r in rects:
            for o in out:
                if r[0] < o[2] + gap and r[2] > o[0] - gap and r[1] < o[3] + gap and r[3] > o[1] - gap and ok(o, r):
                    o[0], o[1], o[2], o[3] = min(o[0], r[0]), min(o[1], r[1]), max(o[2], r[2]), max(o[3], r[3])
                    o[4] += r[4]; o[5] += r[5]; changed = True; break
            else: out.append(r)
        rects = out
    return rects


def para_blocks(page):
    """正文和图注段落（与正文同字号、字数多）的范围，图中文字提取时跳过"""
    bs = body_size(page)
    out = []
    for b in page.get_text('dict')['blocks']:
        if b['type'] or not b['lines']: continue
        n = sum(len(s['text']) for l in b['lines'] for s in l['spans'])
        big = max(s['size'] for l in b['lines'] for s in l['spans']) >= bs - 0.3
        cap = re.match(r'\s*(Extended Data |Supplementary )?(Fig|Figure|Table)\.?\s*\d', ''.join(s['text'] for s in b['lines'][0]['spans']))
        avg = n / len(b['lines'])  # 段落每行字多，图中标签每行字少
        if (big and n > 40 or n > 160) and avg > 30 and len(b['lines']) > 1 or cap: out.append(pymupdf.Rect(b['bbox']))
    return out


def segments(page, clip):
    """按字符取出图中文字，并在大空隙处把同一行拆成多段（例如一行里并排的两个标签）"""
    segs = []
    raw = page.get_text('rawdict', clip=clip, flags=pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP)
    seen = {}; paras = para_blocks(page)
    for bi, b in enumerate(raw['blocks']):
        for l in b.get('lines', []):
            lr = pymupdf.Rect(l['bbox'])
            if any((lr & p).get_area() > 0.5 * lr.get_area() for p in paras): continue  # 图注和正文
            d = line_dir(l)
            if not d: continue
            cur = None
            for s in l['spans']:
                for ch in s['chars']:
                    bb = to_uv(ch['bbox'], d)
                    if cur and (bb[0] - cur['uv'][2] > s['size'] * 0.9 or s['size'] != cur['size'] and ch['c'].strip()):
                        segs.append(cur); cur = None
                    if cur is None:
                        if not ch['c'].strip(): continue
                        cur = dict(dir=d, block=bi, size=s['size'], color=s['color'], font=s['font'],
                                   bold=bool(s['flags'] & 16) or 'Bold' in s['font'], text='', uv=list(bb), chars=[])
                    cur['text'] += ch['c']; cur['chars'].append(ch['bbox'])
                    if ch['c'].strip() and s['flags'] & 16 == 0 and 'Bold' not in s['font']: cur['bold'] = False
                    if ch['c'].strip():
                        cur['uv'] = [min(cur['uv'][0], bb[0]), min(cur['uv'][1], bb[1]), max(cur['uv'][2], bb[2]), max(cur['uv'][3], bb[3])]
            if cur: segs.append(cur)
    out = []
    for s in segs:
        s['text'] = s['text'].strip()
        k = (s['text'], s['dir'], tuple(round(v) for v in s['uv']))
        if not s['text']: continue
        if k in seen: seen[k]['chars'] += s['chars']; continue  # 同一段字画了两遍（如白色描边衬底），两遍都要删
        seen[k] = s; out.append(s)
    return out


def group(segs):
    """把上下紧挨、字号颜色相同的行合成一个文字单元（一个标签可能占好几行）"""
    segs.sort(key=lambda s: (s['dir'], s['uv'][1], s['uv'][0]))
    units = []
    for s in segs:
        for u in reversed(units[-30:]):
            last = u['lines'][-1]
            if (u['dir'] == s['dir'] and abs(u['size'] - s['size']) < 0.3 and u['color'] == s['color']
                    and HASLETTER.search(last['text']) and HASLETTER.search(s['text'])):  # 刻度数字不和标签合并
                a, b = last['uv'], s['uv']
                gap = b[1] - a[3]
                ov = min(a[2], b[2]) - max(a[0], b[0])
                if -0.3 * s['size'] < gap < 0.45 * s['size'] and ov > 0.3 * min(a[2] - a[0], b[2] - b[0]):
                    u['lines'].append(s); break
        else:
            units.append(dict(dir=s['dir'], block=s['block'], size=s['size'], color=s['color'], bold=s['bold'], lines=[s]))
    return units


def guess_align(u, obstacles):
    ls = [l['uv'] for l in u['lines']]
    if len(ls) > 1:
        spread = lambda f: max(map(f, ls)) - min(map(f, ls))
        sp = {'l': spread(lambda r: r[0]), 'c': spread(lambda r: (r[0] + r[2]) / 2), 'r': spread(lambda r: r[2])}
        return min(sp, key=sp.get)
    # 单行：左边紧挨着色块或图标（多半是图例）就左对齐，右边紧挨着就右对齐，否则居中
    r = ls[0]; sz = u['size']
    near = lambda o, side: o[1] < r[3] and o[3] > r[1] and (0 <= r[0] - o[2] < sz * 1.2 if side == 'l' else 0 <= o[0] - r[2] < sz * 1.2)
    obs = [to_uv(o, u['dir']) for o in obstacles]
    if any(near(o, 'l') for o in obs): return 'l'
    if any(near(o, 'r') for o in obs): return 'r'
    return 'c'


def key_of(u):
    return '\n'.join(l['text'] for l in u['lines'])


def cmd_extract(a):
    doc = pymupdf.open(a.pdf)
    os.makedirs(a.out, exist_ok=True)
    pages = [int(p) - 1 for p in a.pages.split(',')] if a.pages else range(doc.page_count)
    clips = {}
    for c in a.clip or []:
        p, r = c.split(':'); clips.setdefault(int(p) - 1, []).append([float(v) for v in r.split(',')])
    figs = []
    for pno in (sorted(clips) if clips else pages):
        page = doc[pno]
        for i, clip in enumerate(clips.get(pno) or detect_figures(page)):
            fid = f'p{pno + 1}_{i + 1}'
            fig = dict(id=fid, page=pno + 1, clip=[round(v, 2) for v in clip])
            units = [u for u in group(segments(page, pymupdf.Rect(clip))) if translatable(key_of(u))]
            img_area = sum(pymupdf.Rect(im['bbox']).intersect(pymupdf.Rect(clip)).get_area() for im in page.get_image_info())
            if len(units) < 2 and img_area > 0.5 * pymupdf.Rect(clip).get_area():
                fig.update(mode='raster', dpi=a.dpi, units=ocr_units(page, clip, a.dpi))
            else:
                obstacles = [list(d['rect']) for d in page.get_drawings() if d['rect'].intersects(pymupdf.Rect(clip))]
                obstacles += [im['bbox'] for im in page.get_image_info()]
                fig.update(mode='vector', units=[dict(
                    key=key_of(u), dir=u['dir'], size=round(u['size'], 2), color=u['color'], bold=u['bold'],
                    align=guess_align(u, obstacles),
                    lines=[dict(text=l['text'], bold=l['bold'], uv=[round(v, 2) for v in l['uv']],
                                chars=[[round(v, 2) for v in c] for c in l['chars']]) for l in u['lines']]) for u in units])
            if not fig['units']: continue
            page.get_pixmap(clip=pymupdf.Rect(clip), dpi=150).save(f'{a.out}/orig_{fid}.png')
            figs.append(fig)
    gl = json.load(open(a.glossary)) if a.glossary and os.path.exists(a.glossary) else {}
    sp = f'{a.out}/strings.json'
    old = json.load(open(sp)) if os.path.exists(sp) else {}
    strings = {}
    for f in figs:
        for u in f['units']: strings[u['key']] = old.get(u['key']) or gl.get(u['key'], '')
    json.dump(dict(pdf=os.path.abspath(a.pdf), figures=figs), open(f'{a.out}/figs.json', 'w'), ensure_ascii=False)
    json.dump(strings, open(sp, 'w'), ensure_ascii=False, indent=1)
    todo = sum(1 for v in strings.values() if not v)
    for f in figs: print(f"{f['id']}  第{f['page']}页  {f['mode']}  {len(f['units'])} 个文字单元  clip={f['clip']}")
    print(f'共 {len(figs)} 张图，{len(strings)} 条去重英文，其中 {len(strings) - todo} 条已有译文（术语表或上次填写），{todo} 条待翻译 -> {sp}')


# ---------- OCR（位图备用路线） ----------
_ocr = None


def ocr_units(page, clip, dpi):
    global _ocr
    import numpy as np
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr = RapidOCR()
    pix = page.get_pixmap(clip=pymupdf.Rect(clip), dpi=dpi)
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3]
    res, _ = _ocr(img)
    units = []
    for box, text, score in res or []:
        if float(score) < 0.6 or not translatable(text): continue
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        # 竖排文字（如纵坐标标题）：框明显高于宽
        vert = (max(ys) - min(ys)) > 1.8 * (max(xs) - min(xs)) and len(text.strip()) > 2
        units.append(dict(key=text.strip(), dir='v' if vert else 'h', px=[min(xs), min(ys), max(xs), max(ys)], align='c'))
    return units


# ---------- render ----------
def wrap(font, text, fs, width):
    """中文按字换行，英文单词和数字不拆开，标点不放行首"""
    lines, line = [], ''
    for ch in text:
        if font.text_length(line + ch, fs) > width and line and ch not in '，。；、：）》”,.;:)':
            k = len(line)
            while ch.isascii() and ch.isalnum() and k and line[k - 1].isascii() and line[k - 1].isalnum(): k -= 1
            if not k: k = len(line)
            lines.append(line[:k].rstrip()); line = line[k:].lstrip() + ch
        else: line += ch
    lines.append(line)
    return lines


def layout(u, zh, font):
    """返回 [(行文字, u 起点, 基线 v, 字号)] 以及是否溢出"""
    size = u['size']; ls = [l['uv'] for l in u['lines']]
    U0, V0, U1, V1 = min(r[0] for r in ls), min(r[1] for r in ls), max(r[2] for r in ls), max(r[3] for r in ls)
    asc = font.ascender
    zl = zh.split('\n')
    place = []
    if len(zl) == len(ls):  # 逐行对位
        fs = size * 0.95
        for t, r, l in zip(zl, ls, u['lines']):
            w = r[2] - r[0]
            room = max(w * 1.15, w + size * 1.5) if u['align'] == 'c' else max(w * 1.08, w + size)
            f = fs
            while font.text_length(t, f) > room and f > size * 0.6: f *= 0.95
            place.append((t, r, f, l.get('bold', u['bold'])))
        fs = min(p[2] for p in place)  # 同一单元统一字号
        out = []
        for t, r, _, b in place:
            tw = font.text_length(t, fs); h = r[3] - r[1]
            us = {'l': r[0], 'r': r[2] - tw, 'c': (r[0] + r[2] - tw) / 2}[u['align']]
            out.append((t, us, (r[1] + r[3]) / 2 + fs * (asc + font.descender) / 2, fs, b))
        over = any(font.text_length(t, fs) > (r[2] - r[0]) * 1.2 + size * 1.5 for t, r, _, _ in place)
        return out, over
    # 重新换行：先尽量保持原字号，放不下再缩小
    W = U1 - U0; Hh = V1 - V0
    if len(ls) == 1: W = max(W * 1.15, W + size * 1.5) if u['align'] == 'c' else max(W * 1.08, W + size)
    text = zh.replace('\n', '')
    fs = size * 0.95
    while True:
        lines = wrap(font, text, fs, W)
        if len(lines) > 1:  # 各行尽量等长，避免最后一行只剩一两个字
            w = font.text_length(text, fs) / len(lines)
            while w < W and len(wrap(font, text, fs, w)) > len(lines): w *= 1.03
            lines = wrap(font, text, fs, min(w, W))
        lh = fs * 1.18
        if (len(lines) == 1 or lines and len(ls) > 1 and len(lines) * lh <= Hh * 1.25 + size * 0.3) or fs < size * 0.62: break
        fs *= 0.95
    over = len(lines) * fs * 1.18 > Hh * 1.3 + size * 0.5 or max(font.text_length(t, fs) for t in lines) > W * 1.05
    tot = len(lines) * lh
    vtop = (V0 + V1) / 2 - tot / 2
    out = []
    for i, t in enumerate(lines):
        tw = font.text_length(t, fs)
        us = {'l': U0, 'r': U1 - tw, 'c': (U0 + U1 - tw) / 2}[u['align']]
        out.append((t, us, vtop + (i + 0.5) * lh + fs * (asc + font.descender) / 2, fs, u['bold']))
    return out, over


def rgb(c):
    return ((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255


def render_vector(fig, strings, fontfile, out, dpi):
    doc = pymupdf.open(fig['_pdf'])
    page = doc[fig['page'] - 1]
    font = pymupdf.Font(fontfile=fontfile)
    jobs, warn, halo_rects = [], [], []
    drawings = page.get_drawings()
    strokes = [d for d in drawings if d.get('fill') is None and d.get('color') is not None]
    for u in fig['units']:
        zh = (strings.get(u['key']) or '').strip()
        if not zh or zh == u['key']: continue
        # 有的图给文字加了描边衬底（一个个字形轮廓的矢量路径），也要找出来删掉，新字照样加衬底
        box = pymupdf.Rect(); [box.include_rect(pymupdf.Rect(c)) for l in u['lines'] for c in l['chars']]
        e = u['size'] * 0.25; big = box + (-e, -e, e, e)
        hs = [d for d in strokes if d['rect'] in big and d['rect'].width < u['size'] * 1.5 and d['rect'].height < u['size'] * 1.5]
        u['halo'] = hs[0]['color'] if len(hs) >= max(3, len(u['key']) // 3) else None
        if u['halo']:
            # 只能按“碰到就删”的方式删这些路径；字形框下面若还有别的图形（如底色块）会被一起删掉，这种情况宁可保留并提示
            ids = {id(d) for d in hs}
            if any(d['rect'].intersects(big) and id(d) not in ids for d in drawings if d['rect'].get_area() > 0):
                warn.append(f"{u['key']}（描边衬底下有底色，旧衬底未删，请检查）")
            else: halo_rects += [d['rect'] + (0.4, 0.4, -0.4, -0.4) for d in hs]
        for l in u['lines']:
            for c in l['chars']:  # 逐字删除，只缩小一点，避免误删相邻字符
                r = pymupdf.Rect(c)
                if r.is_empty: continue
                dx, dy = r.width * 0.2, r.height * 0.2
                page.add_redact_annot(pymupdf.Rect(r.x0 + dx, r.y0 + dy, r.x1 - dx, r.y1 - dy), fill=None)
        lines, over = layout(u, zh, font)
        if over: warn.append(u['key'].replace('\n', ' / '))
        jobs.append((u, lines))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    if halo_rects:  # 第二遍只删描边路径，不碰文字和图片
        for r in halo_rects: page.add_redact_annot(r, fill=None)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED,
                              text=pymupdf.PDF_REDACT_TEXT_NONE)
    page.insert_font(fontname='zhf', fontfile=fontfile)
    for u, lines in jobs:
        col = rgb(u['color'])
        for t, us, vb, fs, bold in lines:
            pt, rot = from_uv(us, vb, u['dir'])
            if u.get('halo'):
                page.insert_text(pt, t, fontsize=fs, fontname='zhf', color=u['halo'], render_mode=1, border_width=0.3, rotate=rot)
            kw = dict(render_mode=2, border_width=0.04) if bold else {}  # 中文字体没有粗体，用描边模拟
            page.insert_text(pt, t, fontsize=fs, fontname='zhf', color=col, fill=col, rotate=rot, **kw)
    clip = pymupdf.Rect(fig['clip'])
    page.get_pixmap(clip=clip, dpi=dpi).save(f"{out}/zh_{fig['id']}.png")
    vec = pymupdf.open(); np_ = vec.new_page(width=clip.width, height=clip.height)
    np_.show_pdf_page(np_.rect, doc, page.number, clip=clip)
    vec.save(f"{out}/zh_{fig['id']}.pdf", garbage=3, deflate=True)
    return warn


def render_raster(fig, strings, fontfile, out, dpi):
    import numpy as np, cv2
    from PIL import Image, ImageDraw, ImageFont
    doc = pymupdf.open(fig['_pdf'])
    pix = doc[fig['page'] - 1].get_pixmap(clip=pymupdf.Rect(fig['clip']), dpi=fig['dpi'])  # 与 OCR 时同一分辨率，坐标才对得上
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].copy()
    jobs, warn = [], []
    for u in fig['units']:
        zh = (strings.get(u['key']) or '').strip()
        if not zh or zh == u['key']: continue
        x0, y0, x1, y1 = [int(round(v)) for v in u['px']]
        x0, y0 = max(0, x0 - 2), max(0, y0 - 2); x1, y1 = min(pix.w, x1 + 2), min(pix.h, y1 + 2)
        # 背景色取文本框外一圈的众数，与背景差异大的像素当作文字
        ring = np.concatenate([img[max(0, y0 - 3):y0, x0:x1].reshape(-1, 3), img[y1:y1 + 3, x0:x1].reshape(-1, 3),
                               img[y0:y1, max(0, x0 - 3):x0].reshape(-1, 3), img[y0:y1, x1:x1 + 3].reshape(-1, 3)])
        bg = np.median(ring, 0) if len(ring) else np.array([255, 255, 255])
        box = img[y0:y1, x0:x1].astype(int)
        diff = np.abs(box - bg).sum(2) > 90
        # 抗锯齿边缘会把中位数拉向背景色（黑字变灰），只取与背景差异最大的那部分像素当字色
        if diff.any():
            d = np.abs(box - bg).sum(2); ink = np.median(box[d >= np.percentile(d[diff], 70)], 0)
        else: ink = np.array([0, 0, 0])
        mask = np.zeros(img.shape[:2], np.uint8); mask[y0:y1, x0:x1] = diff.astype(np.uint8) * 255
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)
        if len(ring) and ring.std(0).max() < 12: img[mask > 0] = bg  # 纯色背景直接填色
        else: img = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        jobs.append((zh, (x0, y0, x1, y1), tuple(int(v) for v in ink), u.get('align', 'c'), u.get('dir', 'h')))
    im = Image.fromarray(img); dr = ImageDraw.Draw(im)
    for zh, (x0, y0, x1, y1), ink, al, d in jobs:
        if d == 'v':  # 竖排：按横排写在转置的框里，再逆时针转 90° 贴回
            bw, bh = y1 - y0, x1 - x0; fs = int(bh * 0.85)
            while fs > 6 and dr.textlength(zh, font=ImageFont.truetype(fontfile, fs)) > bw * 1.15: fs -= 1
            f = ImageFont.truetype(fontfile, fs); tw = int(dr.textlength(zh, font=f)) + 4
            if tw > bw * 1.15: warn.append(zh)
            t = Image.new('RGBA', (tw, bh), (0, 0, 0, 0))
            ImageDraw.Draw(t).text((tw / 2, bh / 2), zh, font=f, fill=ink + (255,), anchor='mm')
            t = t.rotate(90, expand=True)
            im.paste(t, (x0, int((y0 + y1 - t.height) / 2)), t)
            continue
        h = y1 - y0; fs = int(h * 0.85)
        while fs > 6:
            f = ImageFont.truetype(fontfile, fs)
            if dr.textlength(zh, font=f) <= (x1 - x0) * 1.15 + h: break
            fs -= 1
        if dr.textlength(zh, font=f) > (x1 - x0) * 1.15 + h: warn.append(zh)
        tw = dr.textlength(zh, font=f)
        x = {'l': x0 + 2, 'r': x1 - 2 - tw, 'c': (x0 + x1 - tw) / 2}[al]
        dr.text((x, (y0 + y1) / 2), zh, font=f, fill=ink, anchor='lm')
    im.save(f"{out}/zh_{fig['id']}.png")
    return warn


def compare(out, fid):
    from PIL import Image
    a = Image.open(f'{out}/orig_{fid}.png').convert('RGB'); b = Image.open(f'{out}/zh_{fid}.png').convert('RGB')
    b = b.resize((a.width, round(b.height * a.width / b.width)))
    side = a.width < a.height * 1.2  # 宽图上下排，窄图左右排
    c = Image.new('RGB', (a.width * 2 + 10, a.height) if side else (a.width, a.height * 2 + 10), 'white')
    c.paste(a, (0, 0)); c.paste(b, (a.width + 10, 0) if side else (0, a.height + 10))
    c.save(f'{out}/cmp_{fid}.png')


def cmd_render(a):
    meta = json.load(open(f'{a.dir}/figs.json'))
    strings = json.load(open(f'{a.dir}/strings.json'))
    fontfile = find_font(a.font)
    only = set(a.only.split(',')) if a.only else None
    miss = [k for k, v in strings.items() if not v]
    for fig in meta['figures']:
        if only and fig['id'] not in only: continue
        fig['_pdf'] = meta['pdf']
        warn = (render_vector if fig['mode'] == 'vector' else render_raster)(fig, strings, fontfile, a.dir, a.dpi)
        compare(a.dir, fig['id'])
        print(f"{fig['id']}: zh_{fig['id']}.png" + (f'  ⚠ 请检查（可能放不下或有残留）：{warn}' if warn else ''))
    if miss: print(f'提示：{len(miss)} 条译文为空，按保留原文处理：{miss[:15]}{" …" if len(miss) > 15 else ""}')


def cmd_glossary(a):
    s = json.load(open(f'{a.dir}/strings.json'))
    g = json.load(open(a.glossary)) if os.path.exists(a.glossary) else {}
    n = 0
    for k, v in s.items():
        if v and k not in g: g[k] = v; n += 1
    json.dump(dict(sorted(g.items())), open(a.glossary, 'w'), ensure_ascii=False, indent=1)
    print(f'术语表新增 {n} 条，共 {len(g)} 条 -> {a.glossary}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('extract'); e.add_argument('pdf'); e.add_argument('out')
    e.add_argument('--pages'); e.add_argument('--clip', nargs='*'); e.add_argument('--glossary', default=f'{HERE}/glossary.json')
    e.add_argument('--dpi', type=int, default=300)
    r = sub.add_parser('render'); r.add_argument('dir'); r.add_argument('--dpi', type=int, default=300)
    r.add_argument('--only'); r.add_argument('--font')
    g = sub.add_parser('glossary'); g.add_argument('dir'); g.add_argument('glossary', nargs='?', default=f'{HERE}/glossary.json')
    a = ap.parse_args()
    {'extract': cmd_extract, 'render': cmd_render, 'glossary': cmd_glossary}[a.cmd](a)


if __name__ == '__main__':
    main()
