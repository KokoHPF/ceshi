import sys
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
def font(s): return ImageFont.truetype(F, s)
RED = (171, 25, 66); INK = (30, 30, 30); GREY = (110, 110, 110)

def wrap(d, text, f, w):
    lines, cur = [], ''
    for ch in text:
        if d.textlength(cur + ch, font=f) > w and ch not in '、，。；：）)':
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur: lines.append(cur)
    return lines

def box_lines(d, items, w):
    """items: list of (kind,text); kind in title/sub/body/italic"""
    out = []
    for kind, t in items:
        f = font(40 if kind == 'title' else 35)
        for ln in wrap(d, t, f, w):
            out.append((kind, ln, f))
    return out

def box_h(d, items, w, pad=18):
    ls = box_lines(d, items, w - 2 * pad)
    return 2 * pad + sum(f.size + 10 for _, _, f in ls)

def draw_box(d, x, y, w, h, items, pad=18, fill='white', outline=INK, width=3, padl=None):
    padl = pad if padl is None else padl
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=width)
    ls = box_lines(d, items, w - pad - padl)
    total = sum(f.size + 10 for _, _, f in ls)
    cy = y + (h - total) / 2
    for kind, ln, f in ls:
        col = {'title': RED, 'sub': INK, 'body': INK, 'italic': GREY}[kind]
        sw = 1 if kind in ('title', 'sub') else 0
        d.text((x + padl, cy), ln, font=f, fill=col, stroke_width=sw, stroke_fill=col)
        cy += f.size + 10

def arrow(d, x1, y1, x2, y2, w=4):
    d.line([x1, y1, x2, y2], fill=INK, width=w)
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 18
    p1 = (x2 - L * math.cos(a - 0.45), y2 - L * math.sin(a - 0.45))
    p2 = (x2 - L * math.cos(a + 0.45), y2 - L * math.sin(a + 0.45))
    d.polygon([(x2, y2), p1, p2], fill=INK)

FACT = {
 'salti': [('title', '前锯肌/下斜方肌功能不足'), ('sub', '（SALTI）')],
 'hip': [('title', '髋/核心无力和/或不稳'), ('sub', '临床表现'), ('body', '＋单腿稳定系列测试有缺陷')],
 'frac': [('title', '骨折'), ('sub', '锁骨'), ('italic', '短缩、畸形、成角'), ('sub', '肩胛骨')],
 'musw': [('title', '肩部肌肉无力'), ('body', '临床表现：＋徒手肌力测试缺陷'), ('title', '肩胛肌肉无力'), ('body', '临床表现：＋Low Row 测试')],
 'acsc': [('title', '肩锁/胸锁关节'), ('italic', '畸形、不稳'), ('sub', '临床表现'), ('body', '＋松弛度测试'), ('body', '＋交叉内收试验')],
 'tight': [('title', '肌肉紧张'), ('italic', '胸小肌、上斜方肌、斜角肌、背阔肌、后方肌群')],
 'gh': [('title', '盂肱关节'), ('italic', '盂唇、不稳、肱二头肌、活动度')],
 'ctrl': [('title', '失去自主控制'), ('sub', '临床表现'), ('body', '＋不能主动后缩肩胛骨')],
 'neuro': [('title', '神经'), ('italic', '胸长神经、副神经'), ('sub', '临床表现'), ('body', '＋萎缩 ＋翼状肩胛 ＋肌电图')],
 'detach': [('title', '肩胛肌肉剥脱'), ('sub', '临床表现'), ('body', '＋内侧缘疼痛'), ('body', '＋可触及缺损')],
}

def fig1():
    W = 1080
    im = Image.new('RGB', (W, 2400), 'white'); d = ImageDraw.Draw(im)
    t = '哪些因素导致了肩胛运动障碍'
    d.text(((W - d.textlength(t, font=font(46))) / 2, 30), t, font=font(46), fill=INK, stroke_width=1, stroke_fill=INK)
    cx = 320; y = 120
    # diamond
    dw, dh = 340, 200
    d.polygon([(cx, y), (cx + dw / 2, y + dh / 2), (cx, y + dh), (cx - dw / 2, y + dh / 2)], outline=INK, width=3, fill='white')
    for i, ln in enumerate(['肩痛和/或', '功能障碍']):
        f = font(38); d.text((cx - d.textlength(ln, font=f) / 2, y + dh / 2 - 42 + i * 46), ln, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
    y += dh
    steps = [('1', '存在肩胛运动障碍？', '否', '不处理肩胛，处理其他病变'),
             ('2', '矫正手法阳性？', '否', '处理其他致病因素，重新审视诊断'),
             ('3', '评估致病因素', None, None)]
    bw, bh = 380, 120
    for n, s, no, alt in steps:
        arrow(d, cx, y, cx, y + 50); 
        if n != '1': d.text((cx + 12, y + 6), '是', font=font(34), fill=INK)
        y += 50
        draw_box(d, cx - bw / 2, y, bw, bh, [('sub', s)], fill=(242, 242, 242))
        f = font(56); d.text((cx - bw / 2 - 60, y + 18), n, font=f, fill=RED, stroke_width=1, stroke_fill=RED)
        if no:
            arrow(d, cx + bw / 2, y + bh / 2, cx + bw / 2 + 80, y + bh / 2)
            d.text((cx + bw / 2 + 24, y + bh / 2 - 46), no, font=font(34), fill=INK)
            draw_box(d, cx + bw / 2 + 80, y, W - 20 - (cx + bw / 2 + 80), bh, [('body', alt)], pad=14)
        y += bh
    # factor grid
    y += 30
    d.line([cx, y - 30, cx, y], fill=INK, width=4)
    d.line([60, y, W - 60, y], fill=INK, width=4)
    y += 30
    order = ['salti', 'hip', 'frac', 'musw', 'acsc', 'tight', 'gh', 'ctrl', 'neuro', 'detach']
    cw = (W - 24 * 2 - 24) / 2
    for r in range(5):
        a, b = order[2 * r], order[2 * r + 1]
        h = max(box_h(d, FACT[a], cw), box_h(d, FACT[b], cw))
        for c, k in enumerate((a, b)):
            x = 24 + c * (cw + 24)
            draw_box(d, x, y, cw, h, FACT[k])
        y += h + 26
    im.crop((0, 0, W, y + 14)).save(f'{OUT}/f1_cn.png'); print('f1', y)

def fig2():
    W = 1080
    im = Image.new('RGB', (W, 3000), 'white'); d = ImageDraw.Draw(im)
    t = '临床检查的推进顺序'
    d.text(((W - d.textlength(t, font=font(46))) / 2, 30), t, font=font(46), fill=INK, stroke_width=1, stroke_fill=INK)
    joint = [('title', '关节检查'), ('sub', '盂肱关节'), ('italic', '盂唇、不稳、肱二头肌、活动度'),
             ('sub', '肩锁/胸锁关节'), ('italic', '畸形、不稳'), ('sub', '临床表现'),
             ('body', '＋M-DLS（改良动态盂唇剪切试验）'), ('body', '＋松弛度测试'), ('body', '＋交叉内收试验')]
    seq = [FACT['hip'], FACT['detach'], FACT['musw'], FACT['tight'], FACT['ctrl'], FACT['salti'], joint, FACT['frac'], FACT['neuro']]
    cw = W - 2 * 70; y = 120; x = 70
    for i, it in enumerate(seq):
        h = box_h(d, it, cw - 40) + 6
        draw_box(d, x, y, cw, h, it, padl=58)
        n = str(i + 1)
        d.ellipse([x - 26, y - 26, x + 30, y + 30], fill=RED); d.text((x + 2 - d.textlength(n, font=font(34)) / 2, y - 18), n, font=font(34), fill='white')
        y += h
        if i < len(seq) - 1:
            arrow(d, W / 2, y + 4, W / 2, y + 50); y += 56
    im.crop((0, 0, W, y + 30)).save(f'{OUT}/f2_cn.png'); print('f2', y)

fig1(); fig2()
