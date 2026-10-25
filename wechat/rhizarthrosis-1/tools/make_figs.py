#!/usr/bin/env python3
"""Colonna、Borghi 2024 拇指腕掌关节骨关节炎（Part I 文献综述）：首图中文标题卡、原文作者自绘/自摄的图贴中文标签
（图 3 方向词和神经名用 relabel 原位改成中文，见 work/labels.json、fixes.json）、Eaton-Littler 分期（原文图 12 的 X 线 + 中文说明重排）、
保守治疗要点卡、封面。原文图 2、4、5、6、9 为经许可转载的第三方图片，不使用。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
WORK, OUT, FM, FBOLD = sys.argv[1:5]
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('文献综述 · 《Cureus》2024', ['拇指腕掌关节骨关节炎（上）：', '文献综述'],
               'Colonna S, Borghi C.', 'Cureus. 2024;16(1):e52932. doi:10.7759/cureus.52932',
               '意大利博洛尼亚 Spine Center、Osteopathic Spine Center Education（OSCE）'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1

put(tags_at(k, 'x29.jpg', [(.45, .03, '拇指腕掌关节', C_HI)]), '原文图 1  拇指腕掌关节（大多角骨-第一掌骨关节，TMj）：拇指根部疼痛的常见来源')
put('x61.zh.jpg', '原文图 3  作用于拇指腕掌关节的肌肉：线的方向＝肌肉牵拉方向，长度＝力矩潜能（单位 Nm，横轴屈曲/伸展，纵轴内收/外展）。'
    'ADPo/ADPt＝拇收肌斜头/横头；OPP＝拇对掌肌；FBP＝拇短屈肌；FPL＝拇长屈肌；APB＝拇短展肌；APL＝拇长展肌；EPB＝拇短伸肌；EPL＝拇长伸肌')
put('x114.jpg', '原文图 7  作者借用 Neumann 的“骑马”比喻：第一掌骨像马鞍上的骑手。作者认为骑手应面向第二掌骨（尺侧），更符合这个关节的实际受力')
put(tags_at(k, 'x116.jpg', [(.0, .02, 'A 马镫完好', C_OK), (.5, .02, 'B 马镫断了', C_HI)]),
    '原文图 8  更贴切的比喻是“马术跳障碍”：起跳时骑手靠马镫保持稳定（A）；马镫断了，骑手会向前转、向后滑（B）。马镫就是关节周围的韧带——韧带松弛是关节炎的重要基础')
put(tags_at(k, 'x154.jpg', [(.0, .02, '研磨试验', C_NAV)]), '原文图 10  研磨试验（grind test）：握住拇指近节，沿第一掌骨长轴向关节方向挤压，同时轻轻旋转。阳性预测值高（91%），但阴性预测值低（68%）——不痛不能排除关节炎')
put(tags_at(k, 'x172.jpg', [(.0, .02, '杠杆试验', C_NAV)]), '原文图 11  杠杆试验（lever test）：拇指和示指捏住第一掌骨远端，在关节处交替向尺侧、桡侧撬动。诱发的疼痛最强、最像患者平时的痛，敏感度和特异度都最高')

# Eaton-Littler 分期
im = k.op('x193.jpg'); B = [(242, 90, 478, 321), (707, 90, 930, 321), (237, 407, 478, 647), (707, 407, 928, 647)]
T = [('Ⅰ期：滑膜炎期', ['关节轮廓正常', '关节间隙可增宽（积液或韧带松弛）', '没有骨赘']),
     ('Ⅱ期：关节囊明显松弛', ['关节间隙变窄', '大多角骨远端关节面尺侧有小骨赘', '无半脱位或半脱位 ≤1/3 关节面']),
     ('Ⅲ期：关节明显破坏', ['间隙进一步变窄，有囊变和骨硬化', '大多角骨远端尺侧明显骨赘', '第一掌骨基底向桡背侧中度半脱位', '舟大多角关节轻度骨关节炎']),
     ('Ⅳ期：大多角骨周围全关节炎', ['关节明显半脱位', '间隙狭窄同Ⅲ期', '软骨下骨囊变和硬化', '舟大多角关节明显侵蚀和破坏'])]
W, cw, ch = 1200, 600, 520; card = Image.new('RGB', (W, 76 + 2 * ch), 'white'); d = ImageDraw.Draw(card)
d.rectangle([0, 0, W, 76], fill=TEAL); d.text((24, 16), 'Eaton-Littler 分期（原文图 12，中文重排）', font=font(36), fill='white')
for i, (b, (t, pts)) in enumerate(zip(B, T)):
    x0, y0 = (i % 2) * cw, 76 + (i // 2) * ch
    d.rectangle([x0 + 8, y0 + 8, x0 + cw - 8, y0 + ch - 8], outline=(200, 205, 210), width=2)
    d.rectangle([x0 + 8, y0 + 8, x0 + cw - 8, y0 + 62], fill=LT); d.text((x0 + 22, y0 + 16), t, font=font(32), fill=TEAL)
    xr = im.crop(b); xr = xr.resize((260, round(xr.height * 260 / xr.width))); card.paste(xr, (x0 + cw - 278, y0 + 80))
    yy = y0 + 84
    for p in pts: yy = k.para(d, x0 + 22, yy, '· ' + p, 27, cw - 310, gap=10) + 8
k.save(card, n); n += 1

put(tags_at(k, 'x212.jpg', [(.02, .02, '长型（含腕）', C_NAV), (.52, .02, '短型', C_NAV)]),
    '原文图 13  两种拇指腕掌关节支具：左为长型（包括腕关节，多用于夜间静息），右为短型（白天活动时用）。保持拇指外展、对着中指（让患者做“O”形）、掌指关节微屈，指间关节放开')
put('x250.jpg', '原文图 14  神经动力学技术（桡神经滑动）：患者仰卧，治疗师下压肩、伸肘、上臂内旋，屈腕屈拇屈指、尺偏；然后交替做“肩下沉＋屈肘＋伸腕”和“肩上抬＋伸肘＋屈腕尺偏”，每个循环约 2 秒')
put('x267.jpg', '原文图 15  Kaltenborn 技术：患者坐位，肘屈 90°，前臂旋前、手背贴着治疗师身体；治疗师用拇指和示指捏住第一掌骨，做短幅前后向滑动＋Ⅲ级牵引。做 3 分钟、休 1 分钟，共 3 轮')
put('x281.jpg', '原文图 16  Mulligan 动态松动（MWM）：治疗师双拇指在第一掌骨基底施加反向推力，按患者反馈调整方向和力度，找到不痛的位置后，让患者做原来会痛的外展、内收动作，3 组 × 10 次')
put('x294.jpg', '原文图 17  Maitland 被动附属松动：体位同 Kaltenborn 技术，对腕掌关节做轻柔小幅度的前后向滑动（约每分钟 60 次），3 分钟、休 1 分钟，共 3 轮；以不痛为准')
c = k.op('x281.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .3)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
