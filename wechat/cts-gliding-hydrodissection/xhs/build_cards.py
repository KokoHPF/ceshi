#!/usr/bin/env python3
"""Savage & Albano 2020 腕管综合征注射水分离＋肌腱、神经滑动练习 → 小红书 3:4 图文卡片。
原文 CC BY-NC 3.0：原文图 1、2 已裁去英文说明栏（../tools/prep.py），说明译成中文写在卡片上。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='手腕康复', source='Savage & Albano J Orthop Case Rep 2020;10(9):38', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
I = lambda n: Image.open(f'{WORK}/{n}.jpg').convert('RGB')
X = lambda n: Image.open(f'{WORK}/x{n}.jpg').convert('RGB')
tendon = I('tendon'); top, bot = tendon.crop((0, 0, tendon.width, 219)), tendon.crop((0, 219, tendon.width, tendon.height))

deck.cover(['肌腱、神经滑动练习', '“联姻”注射水分离', '治疗腕管综合征：新疗法？'], kicker='J Orthop Case Rep 2020 · 病例报告',
           subtitle='两侧手腕自身对照，随访 1 年',
           photos=[(top, '肌腱滑动'), (I('nerve'), '神经滑动'), (X(2073), '超声')], banner='注射后马上动起来')
deck.text('腕管综合征怎么治', '原文引言', [
    ('box', '最常见的神经卡压', '患病率女性 **5.3%**、男性 **2.1%**；正中神经分布区痛、麻，**夜间加重**', 'teal'),
    ('box', '非手术治疗', '肌腱、神经**滑动练习**、夜间支具、消炎药、激素\n激素注射短中期有效，**长期效果不佳**', 'yellow'),
    ('box', 'PRP', '富血小板血浆含**生长因子**，可能促进神经修复', 'purple'),
    ('box', '水分离', '用注射液把正中神经从**粘连**的结缔组织中“剥”开，改善神经滑动', 'navy')])
deck.text('作者的新思路', '原文引言与讨论', [
    ('bul', ['腕管综合征患者正中神经周围的**滑膜下结缔组织增厚、纤维化**，神经滑动变差', '水分离负责“松开粘连”，滑动练习负责“让神经动起来”']),
    ('box', '本文的新意', '**首次**在水分离注射后**立即**配合主动肌腱、神经滑动练习', 'accent'),
    ('box', '作者的假设', '练习 + 水分离不论注射什么都有效；再加 PRP 的生长因子，效果更好', 'yellow'),
    ('box', '滑动练习的作用（原文引言）', '减轻水肿、减少周围结缔组织粘连、改善神经活动度；降低炎症物质浓度，减轻外周和中枢敏化', 'teal')])
deck.text('研究怎么做', '原文', [
    ('box', '患者', '37 岁男性，电缆工（重体力），吸烟饮酒\n双侧腕管综合征 **6 年**，右侧更重', 'teal'),
    ('box', '自身对照 + 三盲', '两侧手腕随机：一侧 **PRP**，一侧等量**盐水**\n患者、超声医生、电生理检查者都不知道分组', 'yellow'),
    ('box', '随访', '2、4、6 个月评估；6 个月揭盲\n盐水侧补打 PRP，再随访到 **1 年**', 'purple'),
    ('box', '看什么', '疼痛、波士顿腕管问卷（症状 SSS、功能 FSS，1～5 分）、神经传导、横截面积', 'navy')])
deck.text('注射和水分离怎么做', '原文', [
    ('steps', [('1', '抽血 30 ml，制成 **8 ml** 富生长因子血浆'), ('2', '坐位，前臂旋后，腕下垫**毛巾卷**略背伸'),
               ('3', '超声平面内：豌豆骨水平找正中神经，多普勒确认**尺动脉**'), ('4', '25G 针从**腕尺侧**刺向正中神经'),
               ('5', '把神经从**屈肌支持带**和**滑膜下结缔组织**中分离；每侧共 8 ml'), ('6', '夹板固定，**不用消炎药**，痛时冰敷；症状允许即开始练习')]),
    ('box', '粘连轻重', '右侧粘连更重，用了 **6 ml** 才分开；左侧 **3 ml**', 'yellow')])
deck.figure('基线超声：右侧更粗', '原文图 3：正中神经最粗处横截面积（黄线）', [X(2073), X(2074)], ['右腕 22 mm²', '左腕 15 mm²'], [
    ('bul', ['右腕 **0.22 cm²**：中重度', '左腕 **0.15 cm²**：中度'])], stack=True)
deck.figure('练习①：示指、中指肌腱滑动', '原文图 1（英文说明栏已裁去）', [top, bot], ['示指', '中指'], stack=True, items=[
    ('steps', [('1', '肘、腕**伸直**，拇指伸开'), ('2', '固定其余三指，主动把**示指**（或**中指**）向掌心屈'), ('3', '屈到**腕部有牵拉感**')]),
    ('box', '剂量', '**15 次 × 2 组**；做对了会有轻微牵拉不适', 'yellow')])
deck.figure('练习②：正中神经滑动', '原文图 1 下（英文说明栏已裁去）', I('nerve'), None, [
    ('steps', [('1', '肘伸直，**腕和手指伸开**'), ('2', '旋转肩膀，使手指**指向后方**'), ('3', '主动**上提、下压**肩胛带')]),
    ('box', '剂量', '**30 次 × 1 组**', 'yellow')])
deck.figure('练习③：收下巴 + 肩胛后缩', '原文图 2（英文说明栏已裁去）', [I('chin'), I('shoulder')], ['收下巴', '肩胛后缩'], [
    ('box', '收下巴', '背、肩、头靠墙，收下巴把颈部压平贴墙；保持 **5 秒 × 15 次**', 'teal'),
    ('box', '肩胛后缩', '双手放背后，夹紧肩胛骨，头和视线水平；保持 **1 秒 × 5 次，每天 6 组**', 'purple'),
    ('box', '为什么练', '作者用这两个姿势练习**辅助神经滑动**的效果', 'yellow')])
fig, axs = plt.subplots(1, 3, figsize=(9.6, 6.2))
xr = [0, 2, 4, 6, 7, 12]; xl = [0, 2, 4, 6, 12]
for ax, (nm, r, l, top_) in zip(axs, [('最严重疼痛', [4, 3, 4, 4, 3, 2], [4, 3, 1, 1, 0], 5), ('症状 SSS', [2.9, 2.5, 2.9, 2.5, 2.3, 1.6], [2.8, 1.5, 1.6, 1.1, 1.0], 3.2), ('功能 FSS', [2, 1.3, 1.3, 1.4, 1.1, 1.0], [1.9, 1, 1, 1, 1], 2.3)]):
    ax.axvspan(6, 7, color='#F4D03F', alpha=.35)
    ax.plot(xr, r, marker='o', lw=3, ms=8, color='#7F8C8D', label='右：盐水→PRP'); ax.plot(xl, l, marker='o', lw=3, ms=8, color='#C0392B', label='左：PRP')
    ax.set_xticks([0, 6, 12], ['0', '6', '12月'], fontsize=17); ax.set_ylim(0, top_); ax.set_title(nm, fontsize=21); ax.tick_params(axis='y', labelsize=15)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
axs[0].legend(frameon=False, fontsize=15, loc='lower left'); fig.tight_layout()
deck.chart('结果：两侧都好转，PRP 侧更快', '据原文表 1、2 重画；越低越好；黄带＝右腕补打 PRP', fig, [
    ('bul', ['左腕（PRP）6 个月：SSS **1.1**、FSS **1.0**，接近无症状', '右腕（盐水）6 个月：功能明显改善，症状改善有限', '1 年：两侧都比基线好'])])
deck.text('神经功能变化', '原文表 1、2', [
    ('box', '右腕（盐水）', '原本**测不出**的感觉神经反应 **2 个月**时出现\n运动潜伏期 6.6 → 5.3 ms；补打 PRP 后感觉波幅增加 **112%**', 'teal'),
    ('box', '左腕（PRP）', '感觉潜伏期 4.9 → 4.5 ms\n感觉波幅 6.2 → 18.4 μV（1 年时比 6 个月增加 **94%**）', 'coral'),
    ('box', '横截面积', '两侧全程**没有明显变化**', 'grey'),
    ('box', '安全性', '全程**无不良反应**、无神经损伤', 'yellow')])
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '证据很弱'),
    ('bul', ['只有 **1 人**，两侧病情轻重不同', '没有“只注射、不练习”的对照，**练习的作用无法单独评价**', '“可比手术”是与荟萃分析平均值的**间接**比较']),
    ('h', '原文对不上'),
    ('steps', [('1', '补打 PRP 日期：正文 11 月 2 日，表 1 写 **11 月 1 日**'), ('2', '讨论说问卷基线 **46 分**，但正文、表格用的是 **1～5 分**')])])
deck.text('收藏：注射后的滑动练习', '症状允许时开始，练到 2 个月', [
    ('steps', [('1', '**肌腱滑动**：固定其余手指，单独屈示指、中指；15 次 × 2 组'), ('2', '**神经滑动**：伸肘伸腕、转肩，上提下压肩胛带；30 次 × 1 组'),
               ('3', '**收下巴**：靠墙压平颈部，5 秒 × 15 次'), ('4', '**肩胛后缩**：1 秒 × 5 次，每天 6 组'), ('5', '用**练习日志**记录完成情况')]),
    ('box', '文献', 'Savage NJ, Albano J. Marrying Tendon and Nerve Gliding Exercises with Hydrodissection Following Injection for Carpal Tunnel Syndrome – A New Treatment Approach? J Orthop Case Rep. 2020;10(9):38-46', 'navy'),
    ('box', '版权', '原文 **CC BY-NC 3.0**；原文图裁去英文说明栏并加中文标签，仅供学习交流，如有侵权请联系删除', 'accent')])
deck.save(OUT)
