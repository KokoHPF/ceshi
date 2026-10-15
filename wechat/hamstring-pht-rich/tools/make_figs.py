#!/usr/bin/env python3
"""Rich 2025：图 1、2、4、5、7、9、10 英文流程图全部中文重绘；图 3、6、8 照片拆分图重排并重标 a～d；封面取自图 6。
用法：python3 make_figs.py <素材目录（x01..x10.png、title.png）> <输出目录>"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
RED = (171, 25, 66); INK = (25, 25, 25); EDGE = (90, 90, 90)
WHITE = (255, 255, 255); GRAY = (225, 225, 225); YEL = (255, 241, 150); GRN = (190, 235, 180); BLUE = (214, 228, 243); ORG = (253, 232, 214)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')
_d = ImageDraw.Draw(Image.new('RGB', (10, 10)))


def wrap(t, f, w):
    """中文逐字换行；连续的数字/字母/符号不拆开；标点不放在行首。"""
    import re
    out = []
    for para in t.split('\n'):
        toks = re.findall(r'[0-9A-Za-z/.%<>≤≥=~～+\-*]+ ?|.', para)
        line = ''
        for tk in toks:
            if line and _d.textlength(line + tk, font=f) > w:
                if tk[0] in '，。；：、）)？！':
                    line, tk = line[:-1], line[-1] + tk
                elif line[-1] in '（(“':
                    line, tk = line[:-1], line[-1] + tk
                out.append(line); line = tk
            else:
                line += tk
        out.append(line)
    for i in range(1, len(out)):
        while out[i] and out[i][0] in '，。；：、）)？！' and len(out[i - 1]) > 1:
            out[i - 1], out[i] = out[i - 1][:-1], out[i - 1][-1] + out[i]
    return out


# ---------- 流程图渲染 ----------
# 节点：dict(t=文本, fill=颜色, dash=虚线, label=上方箭头说明, bold_first=首行加粗)
# 分支：('split', 左列节点表, 右列节点表)
FS, LH, PAD, GAP = 30, 42, 22, 74


def box_h(t, w, bold_first=False):
    return PAD * 2 + LH * len(wrap(t, font(FS), w - PAD * 2))


def draw_box(d, x0, y0, w, n):
    h = box_h(n['t'], w)
    fill = n.get('fill', WHITE)
    if n.get('dash'):
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=fill)
        for x in range(x0, x0 + w, 22):
            d.line([x, y0, min(x + 12, x0 + w), y0], fill=EDGE, width=3); d.line([x, y0 + h, min(x + 12, x0 + w), y0 + h], fill=EDGE, width=3)
        for y in range(y0, y0 + h, 22):
            d.line([x0, y, x0, min(y + 12, y0 + h)], fill=EDGE, width=3); d.line([x0 + w, y, x0 + w, min(y + 12, y0 + h)], fill=EDGE, width=3)
    else:
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=fill, outline=EDGE, width=3)
    lines = wrap(n['t'], font(FS), w - PAD * 2)
    for i, ln in enumerate(lines):
        f = font(FS); tw = d.textlength(ln, font=f)
        kw = dict(stroke_width=1, stroke_fill=INK) if (i == 0 and n.get('bold_first')) else {}
        d.text((x0 + w / 2 - tw / 2, y0 + PAD + i * LH), ln, font=f, fill=INK, **kw)
    return h


def arrow(d, cx, y0, y1, label=None, dash=False, lw=None):
    if dash:
        for y in range(y0, y1 - 18, 14):
            d.line([cx, y, cx, min(y + 8, y1 - 18)], fill=EDGE, width=4)
    else:
        d.line([cx, y0, cx, y1 - 18], fill=EDGE, width=4)
    d.polygon([(cx - 13, y1 - 20), (cx + 13, y1 - 20), (cx, y1)], fill=EDGE)
    if label:
        f = font(26); lines = wrap(label, f, lw or 440)
        ty = (y0 + y1) / 2 - len(lines) * 34 / 2
        for i, ln in enumerate(lines):
            d.text((cx + 20, ty + i * 34), ln, font=f, fill=(60, 60, 60))


def gap_for(n, w):
    if not n.get('label'):
        return GAP
    return max(GAP, 34 * len(wrap(n['label'], font(26), w)) + 24)


def col_height(nodes, w):
    h = 0
    for k, n in enumerate(nodes):
        if k:
            h += gap_for(n, w // 2 if w < 900 else 440)
        h += box_h(n['t'], w)
    return h


def flow(title, items, name, W=1080, note=None):
    # 先估算高度
    est = 140 + sum(1200 if isinstance(it, tuple) else 400 for it in items)
    im = Image.new('RGB', (W, est), 'white'); d = ImageDraw.Draw(im)
    f = font(42); tw = d.textlength(title, font=f)
    d.text((W / 2 - tw / 2, 24), title, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
    y = 100; x0, bw = 40, W - 80; prev_bottom = None
    for k, it in enumerate(items):
        if isinstance(it, tuple):
            _, L, R = it
            cw = (bw - 40) // 2; xs = [x0, x0 + cw + 40]
            bottoms = []
            for ci, col in enumerate((L, R)):
                cy = y + 30
                cx = xs[ci] + 60
                n0 = col[0]
                g = gap_for(n0, cw - 100)
                # 从上一个框中心分叉
                d.line([W // 2, prev_bottom, W // 2, y], fill=EDGE, width=4)
                d.line([W // 2, y, cx, y], fill=EDGE, width=4)
                arrow(d, cx, y, cy + g - 30, n0.get('label'), n0.get('dash'), lw=cw - 100)
                cy = cy + g - 30
                for j, n in enumerate(col):
                    if j:
                        g = gap_for(n, cw - 100)
                        arrow(d, cx, cy, cy + g, n.get('label'), n.get('dash'), lw=cw - 100); cy += g
                    cy += draw_box(d, xs[ci], cy, cw, n)
                bottoms.append((cx, cy))
            y = max(b[1] for b in bottoms)
            # 汇合
            if k + 1 < len(items):
                for cx, by in bottoms:
                    d.line([cx, by, cx, y + 30], fill=EDGE, width=4)
                d.line([bottoms[0][0], y + 30, bottoms[1][0], y + 30], fill=EDGE, width=4)
                prev_bottom = y + 30; y += 30
            continue
        if k:
            g = gap_for(it, 460)
            arrow(d, W // 2, prev_bottom, y + g, it.get('label'), it.get('dash')); y += g
        h = draw_box(d, x0, y, bw, it)
        y += h; prev_bottom = y
    if note:
        d.text((x0, y + 18), note, font=font(24), fill=(110, 110, 110)); y += 50
    im.crop((0, 0, W, y + 24)).save(f'{OUT}/{name}', quality=92)


# ---------- 照片拆分图 ----------
def panels(im, min_area=40000, split_wide=2.4):
    g = np.array(im.convert('L'))
    m = (g < 238).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(m)
    rs = [tuple(st[i, :4]) for i in range(1, n) if st[i, 4] > min_area]
    out = []
    for x, y, w, h in rs:
        if w / h > split_wide:
            out += [(x, y, w // 2, h), (x + w // 2, y, w - w // 2, h)]
        else:
            out.append((x, y, w, h))
    out.sort(key=lambda r: (r[1] + r[3] // 2) // (im.height // 3) * 10000 + r[0])
    return [im.crop((x, y, x + w, y + h)) for x, y, w, h in out]


def label(im, t):
    d = ImageDraw.Draw(im); f = font(60)
    w = d.textlength(t, font=f) + 18; h = f.size + 12
    d.rectangle([0, im.height - h, w, im.height], fill='white')
    d.text((9, im.height - h + 5), t, font=f, fill=INK)
    return im


def row(ims, W=1080, gap=10):
    H = (W - gap * (len(ims) - 1)) / sum(i.width / i.height for i in ims)
    ims = [i.resize((max(1, round(i.width * H / i.height)), round(H)), Image.LANCZOS) for i in ims]
    out = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), round(H)), 'white'); x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width + gap
    return out


def stack(rows, gap=10):
    W = min(r.width for r in rows)
    rows = [r.resize((W, round(r.height * W / r.width))) for r in rows]
    out = Image.new('RGB', (W, sum(r.height for r in rows) + gap * (len(rows) - 1)), 'white'); y = 0
    for r in rows:
        out.paste(r, (0, y)); y += r.height + gap
    return out


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, im.height // 20))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)


save(Image.open(f'{SRC}/title.png').convert('RGB'), 'img01.jpg')

# 图 1：总体进阶
flow('图1　各阶段之间的进阶', [
    dict(t='第一阶段：等长收缩', bold_first=True, fill=BLUE),
    dict(t='第二阶段：等张力量\n（继续第一阶段）', bold_first=True, fill=BLUE, label='能按剂量完成第二阶段训练'),
    dict(t='第三阶段：动力链\n（继续第一、二阶段）', bold_first=True, fill=BLUE),
    dict(t='第四阶段：压缩负荷\n（继续第一～三阶段）', bold_first=True, fill=BLUE, label='第一～三阶段康复 2 周，症状加重未超过 2/10 持续 >24 小时'),
    dict(t='按指南逐步恢复以前诱发症状的“直线”活动，如快跑/上坡跑、深蹲；耐受剂量达到运动和职业需求后停止第四阶段', fill=GRAY,
         label='第一～四阶段康复 3 次，症状加重未超过 2/10 持续 >24 小时'),
    dict(t='运动或职业是否需要高能量储存与释放？（如踢球、弓步、从地上捡球）', fill=YEL),
    ('split',
     [dict(t='按指南逐步增加步行和/或跑步的量与强度', fill=GRAY, label='否')],
     [dict(t='第五阶段：能量储存与释放', bold_first=True, fill=BLUE, label='是'),
      dict(t='按指南逐步恢复相关运动和职业需求；耐受剂量达到需求后停止第五阶段', fill=GRAY)]),
    dict(t='继续康复（仅第一～三阶段）直到达成目标；出院时给维持方案（一般每周 2 次）', fill=GRN),
], 'img02.jpg')

# 图 2：第一阶段
flow('图2　第一阶段：等长收缩', [
    dict(t='仰卧腘绳肌臀桥*\n剂量：5 次 × 30～45 秒，每次之间休息 90 秒', bold_first=True, fill=BLUE),
    ('split',
     [dict(t='目标：骨盆稳定、腿不抖的高质量收缩\n按需调整难度，使患者在规定时长内保持良好控制', fill=GRN, label='正常进行')],
     [dict(t='所有重复都无法保持高质量收缩\n或 疼痛 >4/10 且 2 次内不缓解', fill=ORG, dash=True, label='出现以下情况', ),
      dict(t='降低负荷（如增加腿部支撑）\n给予优化腰盆控制的提示\n（调整后回到主训练）', fill=ORG, dash=True)]),
], 'img03.jpg', note='* 也可选其他训练')

# 图 4：第二阶段
flow('图4　第二阶段：等张力量', [
    dict(t='仰卧腘绳肌臀桥*\n剂量：2～3 组 × 10～15 次（低强度）进阶到 4～5 组 × 6～8 次（高强度，总计约 25～30 次）\n向心 2 秒、离心 3 秒，每次之间休息 1 秒；组间休息 1 分钟', bold_first=True, fill=BLUE),
    ('split',
     [dict(t='目标：力量 ≥ 健侧的 100%\n随力量提高和疼痛允许逐步增加强度', fill=GRN, label='正常进行')],
     [dict(t='疼痛 >4/10', fill=ORG, dash=True, label='出现以下情况'),
      dict(t='降低强度/负荷\n（调整后回到主训练）', fill=ORG, dash=True)]),
], 'img05.jpg', note='* 也可选其他训练')

# 图 5：第三阶段
flow('图5　第三阶段：动力链', [
    dict(t='前提：已开始第一、二阶段', fill=WHITE),
    dict(t='耐力期剂量：2 组 × 最多 20 次（尽量接近 20 次）；向心 2 秒、离心 2 秒，次间不休息；组间 1 分钟；目标：最后一组结束时疲劳 7/10', fill=GRAY),
    dict(t='力量期剂量：3 组 × 6～10 次；向心 2 秒、离心 2 秒，次间休息 1 秒；组间 2 分钟；目标：最后一组结束时疲劳 7/10', fill=GRAY),
    ('split',
     [dict(t='小腿', bold_first=True, fill=BLUE), dict(t='双腿提踵（耐力期）'), dict(t='单腿提踵 ± 辅助（耐力期）', label='2 组 × 20 次'),
      dict(t='负重单腿提踵（力量期）', label='单腿提踵 2 组 × 20 次'), dict(t='目标：自重单腿提踵 25 次', fill=GRN)],
     [dict(t='臀大肌与大收肌（伸髋）', bold_first=True, fill=BLUE), dict(t='双腿臀推 / 负重双腿臀推 / 串联臀推（耐力期）'),
      dict(t='负重双腿臀推 / 单腿臀推（力量期）', label='单腿臀推 3 组 × 6 次'), dict(t='目标：单腿臀推 3 组 × 10 次', fill=GRN)]),
    ('split',
     [dict(t='股四头肌\n*由治疗师决定是否加入', bold_first=True, fill=BLUE), dict(t='单腿伸膝 或 单腿上台阶（力量期）'), dict(t='目标：股四头肌力量 ≥ 健侧', fill=GRN)],
     [dict(t='腰盆控制\n*依治疗师评估决定', bold_first=True, fill=BLUE), dict(t='站立弹力带外展；骨盆和腰椎的运动控制提示\n剂量：最多 60 次，每组 3～10 次'),
      dict(t='目标：功能训练中能保持腰盆控制', fill=GRN)]),
], 'img07.jpg')

# 图 7：第四阶段
flow('图7　第四阶段：压缩负荷', [
    dict(t='前提：第二阶段康复 2 周，症状加重未超过 2/10 持续 >24 小时', fill=WHITE),
    dict(t='改良硬拉*\n剂量：首次 2 组 × 4～6 次；之后（首次耐受良好时）3 组 × 6～8 次\n向心 2 秒、离心 2 秒，次间休息 1 秒；组间休息 1 分钟\n重量应反映压缩位下的最大功能需求', bold_first=True, fill=BLUE),
    ('split',
     [dict(t='训练中疼痛 >4/10，或症状加重 >2/10 持续 >24 小时？', fill=YEL, label='每次训练后评估'),
      dict(t='否 → 加大最大屈髋角度\n是 → 减小最大屈髋角度', fill=ORG, dash=True),
      dict(t='仍疼痛 >4/10 或症状加重 >2/10 持续 >24 小时？\n否 → 回到主训练\n是 → 减轻重量，或暂停第四阶段 1～2 周后再试', fill=ORG, dash=True)],
     [dict(t='通过增加压缩（加大屈髋角度）进阶；持续进阶直到达到运动/职业所需的髋角度', fill=GRAY, label='耐受良好'),
      dict(t='目标：在个体所需髋角度下完成 3 次最大剂量（3 组 × 6～8 次），之后 24 小时症状加重不超过 2/10；完成后停止第四阶段', fill=GRN)]),
], 'img09.jpg', note='* 也可选其他训练')

# 图 9：第五阶段
flow('图9　第五阶段：能量储存与释放', [
    dict(t='前提：\n第二阶段 2 周且第四阶段 1 周，症状加重未超过 2/10 持续 >24 小时\n运动或职业需要高能量储存与释放（如跳、踢、弓步、从地上捡球）\n第二、四阶段中患侧负荷相近（差 <10%），或同重量下疲劳相近（NRS 差 ≤1/10）', bold_first=True, fill=WHITE),
    dict(t='分腿蹲或专项训练（如踢球、从地上捡球）\n剂量：1～2 个训练，3 组 × 8～20 次；从剂量下限开始', bold_first=True, fill=BLUE),
    ('split',
     [dict(t='逐步增加剂量直到模拟运动/职业需求，每次加 2～6 次\n目标：剂量模拟运动或职业暴露，如踢球 15 次 + 捡球 10 次 = 25 次', fill=GRN,
           label='训练中疼痛 ≤2/10，且之后 24 小时症状加重不超过 2/10')],
     [dict(t='训练中疼痛 >2/10，或症状加重 >2/10 持续 >24 小时', fill=ORG, dash=True, label='出现以下情况'),
      dict(t='减少剂量，或暂停第五阶段 1 周后再试\n（调整后回到主训练）', fill=ORG, dash=True)]),
], 'img11.jpg')

# 图 10：重返跑步
flow('图10　重返跑步的进阶', [
    dict(t='前提：\n完成 3 次第四阶段康复，症状加重未超过 2/10 持续 >24 小时\n步行 30～40 分钟，期间症状轻微（≤2/10），24 小时后不加重', bold_first=True, fill=WHITE),
    dict(t='首次跑步：在较长的步行中穿插 2 ×（跑 1 分钟、走 1 分钟）', fill=BLUE),
    dict(t='跑步时症状 ≤2/10，且 24 小时后不加重？', fill=YEL),
    ('split',
     [dict(t='按指南每 2～3 天增加跑量，直到累计 20 分钟', label='是'), dict(t='根据运动和目标制定个体化跑步计划', fill=GRN)],
     [dict(t='继续康复，1～2 周后再尝试跑步', fill=ORG, dash=True, label='否')]),
    dict(t='增加跑量时持续监测症状：跑步中轻度（≤2/10）症状可以接受，但负荷后 24 小时症状不应加重', fill=GRAY),
], 'img12.jpg')

# 照片图
p3 = [label(p, 'abcd'[k]) for k, p in enumerate(panels(X(3)))]
save(badge(stack([row(p3[:2]), row(p3[2:])]), '图3'), 'img04.jpg')
p6 = [label(p, 'abcd'[k]) for k, p in enumerate(panels(X(6)))]
save(badge(row([stack(p6[:2]), p6[2], p6[3]]), '图6'), 'img08.jpg')
p8 = [label(p, 'ab'[k]) for k, p in enumerate(panels(X(8), split_wide=1.2))]
save(badge(row(p8), '图8'), 'img10.jpg', W=760)
c = panels(X(6))[1]; w, h = c.size; ch = round(w * 383 / 900); y = max(0, (h - ch) // 2)
c.crop((0, y, w, y + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('panels', len(p3), len(p6), len(p8))
