#!/usr/bin/env python3
"""Valencia Mora 等 2017 不稳肩的体格检查与评估：首图中文标题卡、松弛度分级卡、原文图 1～6 照片贴中文标签配中文图注、
各试验准确性中文柱状图、检查流程卡、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('综述 · 《The Open Orthopaedics Journal》2017', ['不稳肩的体格检查与评估'],
               'Valencia Mora M, Ruiz Ibán MÁ, Diaz Heredia J, Gutiérrez-Gómez JC, Ruiz Diaz R, Aramberri M, Cobiella C.',
               'Open Orthop J. 2017;11(Suppl-6, M12):946-956. doi:10.2174/1874325001711010946',
               '西班牙马德里 Jiménez Díaz 基金会大学医院、Ramón y Cajal 大学医院，英国伦敦大学学院'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1

k.save(k.card('先分清：松弛 ≠ 不稳（编者根据原文整理）', [
    ('松弛（laxity）', '关节允许的活动量，主要取决于韧带、关节囊等被动结构；随年龄增长而减小\n年轻运动员出现Ⅱ度移位也可能正常；两侧不对称不能单独作为诊断依据', LT, TEAL),
    ('不稳（instability）', '松弛加上症状：脱位、半脱位、疼痛、恐惧感\n诊断要结合病史：首次脱位年龄、机制、是否需要复位、脱位次数和诱发动作', PK, RED),
    ('移位分级（Hawkins，按手感）', '0 级：不移位\nⅠ级：移到盂缘\nⅡ级：越过盂缘，松手后复位\nⅢ级：越过盂缘，松手后仍在关节外', OR, (200, 120, 0)),
    ('尸体研究的平均移位', '向前 11.8 mm，向后 8.6 mm，向下 20.2 mm', PU, C_NAV),
]), n); n += 1
put(k.op('x284.jpg'), '原文图 1  抽屉试验：一手稳住肩胛（拇指在喙突、其余手指在肩胛冈），另一手把肱骨头向前推，看向前移位的程度。原文正文说患者应仰卧，这张照片为坐位')
s = k.op('x291.jpg'); s.thumbnail((2400, 2400)); s.save(f'{WORK}/f2.jpg')
put(tags_at(k, 'f2.jpg', [(.02, .02, '中立旋转', C_NAV), (.52, .02, '外旋', C_HI)]),
    '原文图 2  沟槽征：坐位、上臂垂在体侧，握住肘部向下拉。A 中立旋转，B 外旋各做一次。肩峰下方出现凹陷为阳性；外旋时移位反而更大，要考虑肩袖间隙损伤')
put(k.op('x233.jpg'), '原文图 3  Gagey 过度外展试验：检查者站在身后，一手按住肩胛，另一手把患臂被动外展，直到感到肩胛开始转动。被动外展超过 105° 为阳性，提示下盂肱韧带复合体松弛；要两侧对比')
put(tags_at(k, 'x235.jpg', [(.12, .005, '恐惧：外展 90°、屈肘 90°', C_HI), (.12, .335, '继续外旋', C_HI), (.12, .67, '复位：向后推肱骨头', C_OK)]),
    '原文图 4  恐惧试验和复位试验：仰卧，肩外展 90°、屈肘 90°，逐渐外旋，直到出现疼痛或恐惧（A、B）；然后在肩前方向后推（C）。恐惧感消失才算复位试验阳性，只是疼痛减轻不算')
put(tags_at(k, 'x237.jpg', [(.06, .01, '外展 90°＋内旋＋轴向加压', C_NAV), (.06, .51, '保持加压，水平内收', C_HI)]),
    '原文图 5  Jerk 试验：坐位，一手稳住肩胛，另一手握肘，把手臂外展 90°、内旋，并沿肱骨长轴向肩部加压（A、B）；保持加压把手臂水平内收，出现突然的“咔噔”为阳性（C、D）')
put(tags_at(k, 'x239.jpg', [(.04, .1, '一手握肘、一手握上臂', C_NAV), (.04, .6, '上举＋向后下推＋轴向加压', C_HI)]),
    '原文图 6  Kim 试验：坐位，检查者一手握肘、一手握上臂（A）；被动上举手臂，同时对上臂施加向后下的力、对肘部沿长轴加压（B）。疼痛或半脱位为阳性')

fig, ax = plt.subplots(figsize=(12, 5.6), dpi=100)
T = [('负荷—移位\n（前方不稳）', 50, 100), ('负荷—移位\n（后方不稳）', 14, 100), ('沟槽征 >2 cm', 28, 97), ('恐惧试验', 52.8, 98.9), ('复位试验\n（以疼痛为标准）', 45.83, 54.35), ('Jerk＋Kim 联合\n（后下盂唇撕裂）', 97, None)]
import numpy as np
x = np.arange(len(T))
for i, (nm, se, sp) in enumerate(T):
    ax.bar(i - .2, se, .38, color='#188080'); ax.text(i - .2, se + 1.5, f'{se:g}', ha='center', fontsize=14, color='#188080')
    if sp is not None: ax.bar(i + .2, sp, .38, color='#EE6348'); ax.text(i + .2, sp + 1.5, f'{sp:g}', ha='center', fontsize=14, color='#EE6348')
ax.set_xticks(x, [t[0] for t in T], fontsize=14); ax.set_ylim(0, 112); ax.set_ylabel('%', fontsize=15); ax.tick_params(axis='y', labelsize=13)
ax.bar([], [], color='#188080', label='敏感度'); ax.bar([], [], color='#EE6348', label='特异度'); ax.legend(frameon=False, fontsize=15, ncol=2, loc='upper right', bbox_to_anchor=(1, 1.12))
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); fig.tight_layout(); fig.savefig(f'{WORK}/acc.png', facecolor='white'); plt.close(fig)
put(k.op('acc.png'), '编者根据原文数字作图：各试验的敏感度和特异度（%）。多数试验特异度高、敏感度低——阳性很有价值，阴性不能排除；Jerk＋Kim 联合原文只报告了敏感度')
k.save(k.card('一套查不稳的顺序（编者根据原文整理）', [
    ('① 问病史', '首次脱位年龄和机制、是否医院复位、神经损伤、脱位次数、什么动作诱发；运动、癫痫、触电史', LT, TEAL),
    ('② 双侧对比的一般检查', '视诊、触诊（后方不稳常有后关节线压痛）、主被动活动度、肌力和感觉', PU, C_NAV),
    ('③ 先评估松弛', 'Beighton 评分（≥4～6 分提示全身松弛）→ 负荷—移位、抽屉试验 → 沟槽征（中立、外旋各一次）→ Gagey 过度外展', GR, (0, 120, 60)),
    ('④ 再做诱发试验', '前方：恐惧 → 复位 → 放松 / 惊吓（三者联合特异度高）\n后方：Jerk、Kim（联合敏感度 97%）', OR, (200, 120, 0)),
    ('⑤ 注意', '年轻运动员肩痛要想到隐匿性不稳；放松、惊吓试验可能很痛甚至导致脱位，动作要轻', PK, RED),
]), n); n += 1
c = k.op('x233.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
