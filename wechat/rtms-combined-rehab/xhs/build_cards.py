#!/usr/bin/env python3
"""古丽加克拉·艾山等 2020 rTMS 联合常规康复治疗桡骨远端骨折后 CRPS-I 1 例 → 小红书 3:4 图文卡片。
原文未标注开放许可：原文图整幅原样放入卡片，不加标注。用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='疼痛康复', source='古丽加克拉·艾山 等 中国康复理论与实践 2020;26(2):232', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
X = lambda n: Image.open(f'{WORK}/x{n}.jpg').convert('RGB')

deck.cover(['重复经颅磁刺激联合常规康复', '治疗桡骨远端骨折后', 'CRPS-Ⅰ型：1 例报道'], kicker='中国康复理论与实践 2020 · 病例报告',
           subtitle='骨折愈合了，手却越来越肿痛？',
           photos=[(X(8), '肿胀变化'), (X(7), '外观、X 线、骨扫描'), (X(12), '握拳变化')], banner='疼痛 8 → 2 分 · Barthel 85 → 100')
deck.text('复杂区域疼痛综合征（CRPS）', '原文引言', [
    ('box', '是什么', '组织损伤后继发、以**肢体疼痛**为主，有**血管运动因素**参与，累及关节、肌肉、骨骼和皮肤\nⅠ型无神经损伤，Ⅱ型有神经损伤', 'teal'),
    ('box', '表现', '疼痛、感觉改变、**皮温异常**、出汗异常、**水肿**、**皮肤颜色改变**；常为撕裂或灼烧样痛，遇冷加重', 'yellow'),
    ('box', '和骨折的关系', '**46%** 的 CRPS 由骨折诱发；桡骨远端骨折后发生率 **1%～37%**\n伤后 1 周内**剧痛**、**女性**是危险因素', 'accent')])
deck.text('病例：67 岁女性', '原文病例介绍', [
    ('steps', [('伤', '雪地摔倒、双手撑地，左桡骨远端骨折；手法复位 + **石膏**固定'), ('↑', '次日起手腕肿痛；6 周拆石膏，骨折愈合良好，**肿胀反而加重**'),
               ('评', '疼痛 VAS **8 分**；手容积 **330 ml**；皮温 **36.8 ℃**、皮肤发红\n肘、前臂、腕、手指关节活动都受限；改良 Barthel **85 分**')]),
    ('box', '检查', '血管 B 超排除血栓；三相骨扫描示左肘、腕、手骨代谢增强；明显**骨质疏松**（腰椎 T 值 -3.2）', 'navy'),
    ('box', '诊断', '符合国际疼痛研究学会（IASP）标准：**Ⅰ型 CRPS**', 'accent')])
deck.figure('原文图 1：患者左手', '原图未改动', X(7), None, [
    ('steps', [('a', '左手**肿胀**，肤色比右手深，手指明显变粗'), ('b', 'X 线：指骨、腕骨明显**骨质疏松**伴退行性改变'), ('c', '三相骨扫描：左肘、腕、手关节**骨代谢增强**')]),
    ('box', '典型线索', '**骨折已愈合，肿痛却越来越重**，伴皮温高、皮肤发红', 'yellow'),
    ('box', '先排除', '上肢血管 B 超排除**血栓**，再按 IASP 标准诊断 CRPS', 'teal')])
deck.text('治疗①：药物 + rTMS', '原文治疗部分', [
    ('box', '药物', '塞来昔布 200 mg，每日 2 次；静脉滴注**唑来膦酸**（消炎止痛、治疗骨质疏松）', 'teal'),
    ('box', 'rTMS 中枢：对侧 M1 区', '**10～20 Hz**、80%～100% 阈值；每组 20～30 个脉冲，间歇 8～10 秒，总数 >1000 个\n或用间歇性 θ 短阵快速脉冲（**iTBS**）', 'purple'),
    ('box', 'rTMS 外周：患侧 C7 棘突旁', '**1 Hz**、100% 阈值、连续 **1200** 个脉冲；作者用意是抑制颈交感干', 'yellow'),
    ('bul', ['每天 1 次，共 **3 周**'])])
deck.text('治疗②：消肿 + 运动 + 作业', '原文治疗部分', [
    ('box', '先消肿', '**手法淋巴引流** 30 分钟，每周 3 次\n抬高患肢、冷热水交替浸泡；激光、微波、超声波', 'teal'),
    ('box', '再活动', '疼痛和水肿缓解后：**不引起疼痛**的被动关节活动\n特别注意**前臂旋后**和适当**腕背伸**', 'yellow'),
    ('box', '作业治疗', '以日常生活活动训练为主，**左手作为辅助手**参与，提高生活参与度', 'purple'),
    ('box', '顺序很重要', '就诊时疼痛、水肿太重，**没法做主动活动**；先控痛消肿，再练活动度', 'accent')])
deck.figure('原文图 2：左手肿胀变化', '原图未改动；左→右：入院第 1 周、第 2 周、出院后随访', X(8), None, [
    ('bul', ['手容积 **330 → 310 ml**', '手指最肿处周径每指约减少 **0.2 cm**（如示指 7.2 → 7.0 cm）', '皮温 **36.8 → 33.8 ℃**']),
    ('box', '消肿用了什么', '**手法淋巴引流**每周 3 次 + 抬高患肢 + 冷热水交替浸泡 + 理疗', 'teal')])
deck.figure('原文图 3：握拳变化', '原图未改动；左：入院第 1 周，右：入院第 2 周', X(12), None, [
    ('bul', ['第 1 周：手指**握不拢**', '第 2 周：握拳明显改善']),
    ('box', '手指关节（举例）', '示指近端指间关节 **20° → 55°**；中指远端指间关节 **0° → 35°**', 'teal'),
    ('box', '训练原则', '只做**不引起疼痛**的被动活动，避免“越痛越练”', 'yellow')])
fig, axs = plt.subplots(1, 4, figsize=(9.6, 5.6))
for ax, (nm, a, b, c, lo) in zip(axs, [('疼痛VAS', 8, 2, '#C0392B', 0), ('手容积ml', 330, 310, '#2E86AB', 280), ('皮温℃', 36.8, 33.8, '#E8A200', 30), ('Barthel', 85, 100, '#2E9E5B', 0)]):
    ax.bar([0, 1], [a, b], .6, color=['#9AA5B1', c])
    for x, y in ((0, a), (1, b)): ax.text(x, y, f'{y:g}', ha='center', va='bottom', fontsize=18)
    ax.set_ylim(lo, max(a, b) * (1.15 if lo == 0 else 1.04)); ax.set_xticks([0, 1], ['前', '后'], fontsize=18); ax.set_title(nm, fontsize=19)
    ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=12)
fig.tight_layout()
deck.chart('3 周前后：疼痛、肿胀、皮温、ADL', '据原文正文数据重画；容积、皮温纵轴不从 0 开始', fig, [
    ('bul', ['疼痛 **8 → 2 分**', '改良 Barthel 指数 **85 → 100 分**（满分）', '肿胀减轻**有限**']),
    ('box', '肿胀到底减了多少', '手容积只减少 **20 ml**；手指最肿处周径每指只减少约 **0.2 cm**', 'grey')])
lab = ['肘屈伸', '前臂旋转', '腕屈伸', '腕桡尺偏', '示指MCP', '示指PIP', '中指PIP', '小指MCP']
pre = [87, 55, 20, 5, 20, 20, 35, 5]; post = [100, 90, 42, 30, 43, 55, 60, 26]
fig, ax = plt.subplots(figsize=(9.6, 6.4)); y = list(range(len(lab)))[::-1]
ax.barh([i + .2 for i in y], pre, .4, color='#9AA5B1', label='治疗前'); ax.barh([i - .2 for i in y], post, .4, color='#2E86AB', label='3 周后')
for i, a, b in zip(y, pre, post): ax.text(b + 1, i - .2, str(b), va='center', fontsize=15); ax.text(a + 1, i + .2, str(a), va='center', fontsize=13, color='#666')
ax.set_yticks(y, lab, fontsize=17); ax.set_xlim(0, 112); ax.tick_params(axis='x', labelsize=14); ax.legend(frameon=False, fontsize=16, loc='lower right'); ax.spines[['top', 'right']].set_visible(False); fig.tight_layout()
deck.chart('关节活动度（被动，°）', '据原文表 1、2 重画（手指只选部分关节）', fig, [
    ('bul', ['前臂旋转 **55° → 90°**，腕屈伸 **20° → 42°**，腕桡尺偏 **5° → 30°**', '所有手指关节都有改善，但离正常仍有距离']),
    ('box', '注意', '原文只测了**被动**活动度，没有握力和主动活动数据', 'grey')])
deck.text('作者为什么用 rTMS', '原文讨论', [
    ('box', '证据基础', '欧洲专家指南（2014）：M1 区**高频（≥5 Hz）**rTMS 治疗神经病理性疼痛有明确镇痛作用（**A 级**）', 'teal'),
    ('box', 'CRPS 的大脑改变', '患侧手在初级躯体感觉皮层的**代表区缩小**，与疼痛程度有关；疼痛抑制运动皮层、降低运动学习能力', 'yellow'),
    ('box', '作者推测的机制', '调节皮层兴奋性；增加脑血流；促进内源性阿片、γ-氨基丁酸、脑源性神经营养因子；**疼痛减轻后更能配合训练**', 'purple')])
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '证据很弱'),
    ('bul', ['**单个病例**、治疗只有 3 周、没有长期随访', '药物、淋巴引流、理疗、运动同时用，**无法拆分 rTMS 的作用**']),
    ('h', '原文对不上'),
    ('steps', [('1', 'rTMS 参数写成范围、“10～15 次或 iTBS”，但每天 1 次治疗 3 周；**看不出实际方案**'), ('2', '表 1 表头写“屈曲/伸展”等，每格却**只有一个数**'),
               ('3', '讨论部分参考文献编号**错位**（如“伤后 1 周剧痛”标 [19]，实为 [18]）')])])
deck.text('收藏：骨折后 CRPS 康复要点', '石膏固定期间或拆除后注意观察', [
    ('steps', [('疑', '肿痛**不减反增**、皮温高、皮肤发红、关节普遍僵硬 → 想到 CRPS'), ('排', '先排除**血栓**'), ('1', '急性期先**控痛消肿**：药物、淋巴引流、抬高'),
               ('2', '缓解后做**不引起疼痛**的被动活动'), ('3', '患手做**辅助手**参与日常生活'), ('+', 'rTMS 可作为综合方案的一部分')]),
    ('box', '文献', '古丽加克拉·艾山, 陈婵, 高天昊, 等. 重复经颅磁刺激联合常规康复对桡骨远端骨折后复杂区域性疼痛综合征Ⅰ型患者上肢功能影响 1 例报道. 中国康复理论与实践, 2020, 26(2): 232-236', 'navy'),
    ('box', '版权', '原文**未标注开放许可**；原文图未作修改，仅供学习交流，如有侵权请联系删除', 'accent')])
deck.save(OUT)
