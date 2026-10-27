#!/usr/bin/env python3
"""Savage & Albano 2020 腕管综合征：超声引导注射＋正中神经水分离后配合肌腱、神经滑动练习（双侧自身对照 1 例）。
中文标题卡、背景卡、设计卡、注射卡、原文图 3（超声）、练习处方卡、原文图 1、2（右侧英文说明栏已裁掉，中文写在图注和卡片里，
见 prep.py；原文 CC BY-NC 3.0 允许演绎）、症状评分变化图（据原文表 1、2 重画）、解读卡、封面。
共用工具在 ../bridge-review-1/tools/bridgekit.py。用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('病例报告 · 《J Orthop Case Rep》2020', ['腕管综合征：注射水分离后', '马上做肌腱、神经滑动练习'],
               'Savage NJ, Albano J.', 'J Orthop Case Rep. 2020;10(9):38-46. doi:10.13107/jocr.2020.v10.i09.1896',
               '美国犹他州 Total Rehab 物理治疗部、Albano 诊所'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
card('腕管综合征和它的治疗（编者根据原文整理）', [
    ('最常见的神经卡压', '人群患病率女性 5.3%、男性 2.1%；手部正中神经分布区疼痛、麻木，夜间加重', LT, TEAL),
    ('诊断', '靠病史和查体；神经电生理（神经传导＋针极肌电图）评估神经功能，超声测正中神经横截面积', OR, (200, 120, 0)),
    ('非手术治疗', '物理治疗（肌腱、神经滑动练习）、夜间支具、消炎药、口服或注射激素\n激素注射短中期有效，但长期效果不佳，还可能损害软组织和神经', GR, (0, 120, 60)),
    ('PRP 和水分离', '富血小板血浆（PRP）含生长因子，可能促进神经修复\n水分离：用注射液把正中神经从周围粘连的结缔组织中“剥”开，改善神经滑动', PU, C_NAV),
    ('本文的新意', '首次在水分离注射后立即配合主动肌腱、神经滑动练习', PK, RED),
])
card('研究怎么做（原文）', [
    ('患者', '37 岁男性，右利手，电缆工（重体力劳动），每天吸烟饮酒；BMI 27.7\n双侧腕管综合征 6 年，右侧更重；用过夜间支具和整脊，从未注射或手术', LT, TEAL),
    ('自身对照', '两侧手腕随机分配：一侧注射 PRP，另一侧注射等量生理盐水\n患者、超声医生、电生理检查者都不知道哪侧打了什么（三盲）', OR, (200, 120, 0)),
    ('随访', '注射后 2、4、6 个月评估；6 个月揭盲\n盐水侧若效果更差，可补打 PRP，再随访 6 个月（研究共 1 年）', GR, (0, 120, 60)),
    ('看什么', '疼痛 NPRS（最小有意义变化约 2 分）\n波士顿腕管问卷：症状严重度 SSS、功能状态 FSS（1～5 分，1 分＝无症状/无障碍）\n神经传导、正中神经横截面积', PU, C_NAV),
])
card('注射和水分离怎么做（原文）', [
    ('PRP 制备', '肘前静脉抽血 30 ml，制成 8 ml 富生长因子血浆（血小板为基线的 2～3 倍，红细胞、白细胞少）', LT, TEAL),
    ('体位', '坐位，前臂旋后、掌心向上，手腕垫毛巾卷略背伸', OR, (200, 120, 0)),
    ('超声引导', '平面内进针：在豌豆骨水平的腕管入口找到正中神经，多普勒确认尺动脉\n25G 针从腕尺侧刺向正中神经', GR, (0, 120, 60)),
    ('水分离', '每侧共注射 8 ml；把正中神经从浅层屈肌支持带和深层滑膜下结缔组织中分离\n右侧粘连更重，用了 6 ml 才分开；左侧 3 ml', PU, C_NAV),
    ('术后', '观察 20 分钟；夹板固定；不用消炎药；痛时每小时冰敷 10～15 分钟\n症状允许时开始练习', PK, RED),
])
put(tags_at(k, 'fig3.jpg', [(.02, .03, '右腕 22 mm²', RED), (.02, .53, '左腕 15 mm²', C_NAV)]),
    '原文图 3  基线超声：正中神经最粗处的横截面积（黄色描线），右腕 0.22 cm²（中重度），左腕 0.15 cm²（中度）')
card('练习处方（原文图 1、2 的说明栏）', [
    ('示指、中指肌腱滑动', '肘、腕伸直，拇指伸开；固定其余三指，主动把示指（或中指）向掌心屈，直到腕部有牵拉感\n15 次 × 2 组；做对了会有轻微牵拉不适', LT, TEAL),
    ('正中神经滑动', '肘伸直，腕和手指伸开；旋转肩膀使手指指向后方，主动上提、下压肩胛带\n30 次 × 1 组', OR, (200, 120, 0)),
    ('收下巴', '背、肩、头靠墙站，主动收下巴，尽量把颈部压平贴墙\n保持 5 秒 × 15 次 × 1 组', GR, (0, 120, 60)),
    ('肩胛后缩', '站或坐，双手放背后；夹紧肩胛骨，头和视线保持水平；能做到的话手离开腰部，不要前弯\n保持 1 秒 × 5 次，每天 6 组', PU, C_NAV),
    ('多久', '注射后症状允许即开始，练到 2 个月复诊；用练习日志记录依从性', PK, RED),
])
put(tags_at(k, 'fig1.jpg', [(.02, .02, '示指肌腱滑动', C_NAV), (.02, .36, '中指肌腱滑动', C_NAV), (.02, .70, '正中神经滑动', C_HI)], W=900),
    '原文图 1  肌腱滑动（上两行：固定其余手指，主动屈示指、中指）和正中神经滑动（下：伸肘伸腕，转肩使手指朝后，上提下压肩胛带）。右侧英文说明栏已裁去')
put(tags_at(k, 'fig2.jpg', [(.02, .02, '收下巴', C_NAV), (.02, .39, '肩胛后缩', C_NAV)], W=900),
    '原文图 2  收下巴（上）和肩胛后缩（下）：作者用这两个姿势练习辅助神经滑动的效果。右侧英文说明栏已裁去')
fig, axs = plt.subplots(1, 3, figsize=(13, 6.2), dpi=100)
xr = [0, 2, 4, 6, 7, 12]; xl = [0, 2, 4, 6, 12]
D = [('最严重疼痛（0～10）', [4, 3, 4, 4, 3, 2], [4, 3, 1, 1, 0], 5),
     ('症状严重度 SSS（1～5）', [2.9, 2.5, 2.9, 2.5, 2.3, 1.6], [2.8, 1.5, 1.6, 1.1, 1.0], 3.2),
     ('功能状态 FSS（1～5）', [2, 1.3, 1.3, 1.4, 1.1, 1.0], [1.9, 1, 1, 1, 1], 2.3)]
for ax, (nm, r, l, top) in zip(axs, D):
    ax.axvspan(6, 7, color='#F4D03F', alpha=.35)
    ax.plot(xr, r, marker='o', lw=2.6, ms=7, color='#7F8C8D', label='右腕：盐水 → 7 个月补打 PRP')
    ax.plot(xl, l, marker='o', lw=2.6, ms=7, color='#C0392B', label='左腕：PRP')
    ax.set_xticks([0, 2, 4, 6, 12], ['基线', '2', '4', '6', '12 月'], fontsize=13); ax.set_ylim(0, top); ax.set_title(nm, fontsize=17)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); ax.tick_params(axis='y', labelsize=12)
axs[0].legend(frameon=False, fontsize=12, loc='lower left')
fig.suptitle('左腕（PRP）改善更快；右腕补打 PRP 后也继续好转', fontsize=20)
fig.text(.5, .015, '黄色带：右腕 6 个月揭盲后约 1 个月补打 PRP；所有注射都做了水分离，术后都做了滑动练习', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, .94)); fig.savefig(f'{WORK}/score.png', facecolor='white'); plt.close(fig)
put('score.png', '据原文表 1、2 重画：分数越低越好。左腕 6 个月时 SSS 1.1、FSS 1.0，接近无症状；右腕（盐水）6 个月时功能改善明显，症状改善有限')
card('这个病例能说明什么（编者解读）', [
    ('结果', '左腕（PRP）：最严重疼痛 4 → 0，SSS 2.8 → 1.0，感觉波幅 1 年时翻倍\n右腕（盐水）：原本测不出的感觉反应 2 个月时出现，运动潜伏期逐渐缩短；补打 PRP 后症状继续好转', GR, (0, 120, 60)),
    ('作者的推测', '盐水侧也有改善，可能部分来自水分离＋滑动练习；PRP 侧更好，可能是练习＋生长因子的叠加', LT, TEAL),
    ('证据很弱', '只有 1 人，两侧病情轻重不同（右侧更重）；水分离和练习两侧都做了，无法单独评价练习的作用\n正中神经横截面积全程没有明显变化', PK, RED),
    ('“可比手术”要打折扣', '作者与荟萃分析的平均值比较；但左腕 6 个月感觉潜伏期只缩短 0.4 ms，手术平均 1.1 ms', OR, (200, 120, 0)),
])
c = k.op('fig1.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = 0
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
