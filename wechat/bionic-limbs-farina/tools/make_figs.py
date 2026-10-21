#!/usr/bin/env python3
"""Farina 等 2021 高性能仿生肢体：首图中文标题卡；原文图 1～6 的英文标注（PDF 叠加文字层）用涂黑删除后
按原位置改写为中文（保留插图和矢量线条），并加中文图注。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import numpy as np
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
doc = pymupdf.open(PDF)
raw = lambda x: Image.open(BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def relabel(im, items, bg='white'):
    """items: (box@1000宽, 文字, 字号@1000宽, 对齐)"""
    s = im.width / 1000; d = ImageDraw.Draw(im)
    for box, t, fs, *al in items:
        b = [int(v * s) for v in box]
        d.rectangle(b, fill=bg)
        f = font(fs * s); lines = t.split('\n'); lh = fs * s * 1.25
        y0 = (b[1] + b[3]) / 2 - lh * len(lines) / 2
        for i, l in enumerate(lines):
            w = d.textlength(l, font=f)
            x = b[0] + 2 if al and al[0] == 'l' else (b[0] + b[2]) / 2 - w / 2
            d.text((x, y0 + i * lh), l, font=f, fill='black')
    return im


def blur(im, boxes, r=10):
    s = im.width / 1000
    for b0 in boxes:
        b = tuple(int(v * s) for v in b0); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * s)), b[:2])
    return im
def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def card(W, title, blocks, bg=(246, 248, 250)):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


stack = lambda ims: (lambda W: (lambda o: ([o.paste(i, (0, sum(j.height for j in ims[:n]))) for n, i in enumerate(ims)], o)[1])(Image.new('RGB', (W, sum(i.height for i in ims)), 'white')))(max(i.width for i in ims))
up = lambda im, w=1000: im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
DPI = 300


def zhfig(pno, clip, labels, fs_scale=1.35, fs_min=None):
    """labels: (英文行文本, 中文, 选项)；在 clip 内找到英文行，删去文字后按其位置写中文"""
    d = pymupdf.open(PDF); p = d[pno]; clip = pymupdf.Rect(clip); boxes = []
    lines = []
    for bl in p.get_text('dict', clip=clip)['blocks']:
        for l in bl.get('lines', []):
            t = ' '.join(s['text'] for s in l['spans']).strip()
            if t: lines.append((pymupdf.Rect(l['bbox']), t, l['spans'][0]['size']))
    used = set()
    for en, zh, *opt in labels:
        opt = opt[0] if opt else {}
        hit = [i for i, (r, t, s) in enumerate(lines) if t == en and i not in used and r.intersects(clip)]
        if not hit: print('  未找到：', en); continue
        if 'near' in opt:
            nx, ny = opt['near']; hit.sort(key=lambda i: abs(lines[i][0].x0 - nx) + abs(lines[i][0].y0 - ny))
        i = hit[0]; used.add(i); r, t, s = lines[i]
        boxes.append((r, zh, s, opt))
    for _, t, _ in lines: pass
    for r, *_ in boxes: p.add_redact_annot(r)
    for i, (r, t, s) in enumerate(lines):
        if i not in used and t.strip() not in ('', ) and opt_drop(t): p.add_redact_annot(r)
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    pix = p.get_pixmap(dpi=DPI, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    k = DPI / 72; dr = ImageDraw.Draw(im)
    for r, zh, s, opt in boxes:
        fs = s * k * fs_scale * opt.get('scale', 1.0); f = font(fs)
        ls = zh.split('\n'); w = max(dr.textlength(l, font=f) for l in ls); h = fs * 1.2 * len(ls)
        cx = ((r.x0 + r.x1) / 2 - clip.x0) * k; cy = ((r.y0 + r.y1) / 2 - clip.y0) * k
        al = opt.get('al', 'c'); x0 = {'c': cx - w / 2, 'l': (r.x0 - clip.x0) * k, 'r': (r.x1 - clip.x0) * k - w}[al]
        y0 = cy - h / 2 + opt.get('dy', 0) * k
        px = im.getpixel((int(min(max(cx, 0), im.width - 1)), int(min(max(cy, 0), im.height - 1))))
        fg = opt.get('fg') or ((255, 255, 255) if sum(px) < 300 else INK)
        if opt.get('box'): dr.rounded_rectangle([x0 - 6, y0 - 4, x0 + w + 6, y0 + h + 4], 6, fill=opt['box'])
        for j, l in enumerate(ls):
            lw = dr.textlength(l, font=f); xx = x0 if al == 'l' else (x0 + w - lw if al == 'r' else cx - lw / 2)
            dr.text((xx, y0 + j * fs * 1.2), l, font=f, fill=fg)
    return im


opt_drop = lambda t: False

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '观点 · 《自然 · 生物医学工程》（2021 年在线发表）', font=font(32), fill=TEAL)
dr.text((70, 130), '迈向更高性能的仿生肢体，', font=font(56), fill=INK)
dr.text((70, 215), '实现更广泛的临床应用', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 365), 'Farina D, Vujaklija I, Brånemark R, et al. Nat Biomed Eng 2023;7(4):473-485', font=font(28), fill=GREY)
dr.text((70, 420), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# 图 1：编号保留，下方加中文图例
f1 = zhfig(1, (304, 56, 552, 224), [])
leg = ['① 靶向肌肉神经移植', '② 骨整合', '③ 植入式传感器', '④ 先进的神经解码算法', '⑤ 现代多关节假肢']
f1 = up(f1, 1100); L = Image.new('RGB', (1100, 130), 'white'); dr = ImageDraw.Draw(L)
for i, t in enumerate(leg): dr.text((20 + (i % 3) * 360, 15 + (i // 3) * 55), t, font=font(32), fill=INK)
save(capbox(stack([f1, L]), '原文图 1：先进的仿生肢体技术（编号对应原图）'), 2)

# 图 2
f2 = zhfig(2, (110, 52, 482, 192), [('(1) Osseointegration', '① 骨整合植入物', {'al': 'l'}), ('(2) Abutment', '② 连接桩', {'al': 'l'}),
                                    ('(3) Myoelectrode', '③ 肌电电极', {'al': 'l'}), ('(4) Active elbow', '④ 主动肘关节', {'al': 'l'}),
                                    ('(5) Prosthetic limb', '⑤ 假肢', {'al': 'l'})], fs_scale=1.12)
save(capbox(up(f2, 1200), '原文图 2：经肱骨截肢者的骨整合植入物。a 残余肱骨内金属植入物的 X 线片；b 连接假肢的经皮植入物示意图；c 骨整合假肢装配示意图'), 3)

# 图 3
f3 = zhfig(3, (112, 54, 482, 266), [('Signals', '信号'), ('Features', '特征'), ('Control', '控制'), ('approaches', '方法'),
                                    ('Action', '动作'), ('potentials', '电位'), ('Time', '时域'), ('domain', '特征'), ('Spectral', '频谱'),
                                    ('Amplitude', '幅值'), ('EEG', '脑电'), ('ENG', '神经电'), ('EMG', '肌电'), ('Mechanical', '机械'),
                                    ('sensors', '传感器'), ('ECoG', '皮层电'), ('Model-based', '基于模型'), ('Classification', '分类'),
                                    ('Regression', '回归'), ('Direct mapping', '直接映射'), ('Data driven', '数据驱动')], fs_scale=1.2)
save(capbox(up(f3, 1200), '原文图 3：神经肌肉接口的多种方式及如何映射为假肢控制指令。信号可来自皮层电（侵入式）、脑电（非侵入式）、'
                          '周围神经电、肌电和机械传感器，提取特征后由算法映射为控制指令'), 4)

# 图 4
f4 = zhfig(4, (114, 52, 482, 136), [])
save(capbox(up(f4, 1200), '原文图 4：已在临床中测试的长期植入式肌电系统。a MyoPlant：感应供电的无线传感器，记录肌外膜双极信号；'
                          'b MIRA：多导联（每导 32 个传感器）全植入系统，经红外传输数字化肌电；c iSens：多通道记录，蓝牙传输，可扩展到神经外记录和刺激；'
                          'd IMES：最多 16 个独立的有源植入物，记录肌内肌电，由外部线圈供电'), 5)

# 图 5
f5 = zhfig(6, (114, 52, 484, 345), [('Intrafascicular', '束内', {'scale': 1.1}), ('implant', '植入电极', {'near': (351, 329)}),
                                    ('Extraneural', '神经外', {'scale': 1.1}), ('implant', '植入电极', {'near': (427, 329)}),
                                    ('Stimulation', '刺激'), ('current', '电流'), ('As', '幅值', {'al': 'l'}),
                                    ('Spikes from', '人工手指'), ('artificial finger', '产生的脉冲'),
                                    ('Neuromorphic encoding of sensor data', '用仿生模型对传感器数据'),
                                    ('using biologically inspired models', '进行神经形态编码'),
                                    ('Rough', '粗糙', {'near': (348, 73)}), ('Smooth', '光滑', {'near': (422, 73)}),
                                    ('Rough', '粗糙', {'near': (158, 99)}), ('Smooth', '光滑', {'near': (248, 99)})], fs_scale=1.15)
save(capbox(up(f5, 1200), '原文图 5：刺激传入纤维、恢复感觉的神经植入物。仿生手指尖的传感器接触粗糙表面时，把纹理信息编码为刺激电流，'
                          '经束内多通道电极（左下）或扁平神经外电极（右下）传回使用者'), 6)

# 图 6
f6 = zhfig(7, (40, 52, 292, 320), [('(1) Ischiadic nerve', '① 坐骨神经', {'al': 'l'}), ('(2) Implanted sensors', '② 植入式传感器', {'al': 'l'}),
                                   ('(3) Tibial nerve', '③ 胫神经', {'al': 'l'}), ('(4) Common peroneal nerve', '④ 腓总神经', {'al': 'l'}),
                                   ('(5) Targeted muscle', '⑤ 靶向肌肉', {'al': 'l'}), ('reinnervation', '　 神经移植', {'al': 'l'})], fs_scale=1.12)
save(capbox(up(f6, 1000), '原文图 6：连接“生物屏幕”的侵入式技术。把胫神经（③）和腓总神经（④）的神经束经靶向肌肉神经移植转到大腿肌肉，'
                          '配合植入式传感器（②），即可直观地控制假肢踝关节'), 7)

c = Image.open(BytesIO(pymupdf.open(PDF).extract_image(38)['image'])).convert('RGB'); c = up(c, 900); y0 = max(0, (c.height - 383) // 2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
