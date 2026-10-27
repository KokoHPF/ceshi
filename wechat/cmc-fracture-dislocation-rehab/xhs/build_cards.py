#!/usr/bin/env python3
"""Bell 等 2010 多发腕掌关节骨折脱位术后康复 1 例 → 小红书 3:4 图文卡片。
原文非开放许可：原文图整幅原样放入卡片，不加标注（g1～g6.jpg 由 ../tools/make_figs.py 文件头的 --clip 命令渲染）。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='手部康复', source='Bell 等 Can J Plast Surg 2010;18(3):e37', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
G = lambda i: Image.open(f'{WORK}/g{i}.jpg').convert('RGB')

deck.cover(['手部腕掌关节', '骨折脱位的术后处理：', '1 例报告'], kicker='Can J Plast Surg 2010 · 病例报告',
           subtitle='只包腕掌关节的支具，让腕和手指早点动',
           photos=[(G(5), '环形腕掌支具'), (G(1), '受伤 X 线'), (G(6), '10 周活动度')], banner='时间线 + 康复方案 + 握力恢复')
deck.text('为什么关注这种损伤', '原文引言与讨论', [
    ('box', '很少见', '腕掌关节（掌骨底与远排腕骨之间）韧带坚强、骨性咬合紧密，**很难脱位**；第 2～5 指同时骨折脱位更少见', 'teal'),
    ('box', '多由高能量外伤引起', '大多是**车祸**，脱位方向多为**背侧**；闭合复位常失败或再脱位 → **首选手术**', 'yellow'),
    ('box', '康复的矛盾', '腕掌关节需要**稳定**才能愈合；但长期把腕和手指一起固定 → **关节僵硬、肌腱粘连、手内在肌无力**', 'accent')])
deck.text('已知的预后', 'Prokuski 等 10 例（最大的病例系列）', [
    ('steps', [('痛', '**5 人**无痛，其余为活动相关的轻痛'), ('力', '6 个月握力为健侧的 **50%～90%**'), ('动', '**6 人**活动度完全恢复，其余受限但不影响功能'),
               ('术', '**3 人**后期需要关节融合'), ('工', '**5 人**回到原工作')]),
    ('box', '空白', '作者检索到**没有**专门研究这种损伤术后康复方案的文献', 'navy')])
deck.figure('受伤时：4 个腕掌关节背侧脱位', '原文图 1（原图未改动）', G(1), None, [
    ('bul', ['28 岁男性，**左利手**，车祸', 'A 正位、B 侧位：**示指、中指、环指、小指**腕掌关节向背侧脱位', '伴**第 3 掌骨**和**大多角骨**骨折']),
    ('box', '损伤机制', '**轴向负荷 + 剪切力**共同作用（原文引用 Yoshida 等的研究）', 'teal'),
    ('box', '为什么要手术', '高能量损伤不易闭合复位；多发腕掌脱位保守治疗**常再脱位**', 'accent')])
deck.figure('闭合复位失败 → 切开复位内固定', '原文图 2（上）、图 3（下）', [G(2), G(3)], None, [
    ('bul', ['图 2：闭合复位后正位、斜位、侧位——**没能满意复位**', '图 3：经手背横切口，小多角骨 **2 枚小螺钉**，腕掌关节 **7 根克氏针**'])], stack=True)
deck.text('治疗时间线', '原文表 1 及正文', [
    ('steps', [('0周', '车祸，当天切开复位克氏针内固定'), ('0～6', '中立位短臂夹板 2 周 → **短臂石膏 4 周**'),
               ('6周', '拆石膏、做掌侧夹板；腕伸/屈 **30°/40°**，掌指 **15°/25°**'), ('8周', '**拔针**，开始手治疗：屈指手套 + 环形腕掌支具'),
               ('10周', '掌指、指间关节活动度**完全恢复**'), ('12周', '**停支具**，开始腕和握力强化'), ('约26周', '腕、掌指、指间关节活动度全部恢复')])])
deck.figure('术后第 6 周', '原文图 4（原图未改动）', G(4), None, [
    ('bul', ['切口愈合良好，**针道清洁**', '克氏针第 **8 周**在门诊拔除；X 线证实大多角骨和掌骨骨折愈合']),
    ('box', '作者坦言', '团队没参与早期处理，石膏固定**比理想的长**；拆石膏时腕、掌指关节活动明显受限', 'accent')])
deck.figure('核心：环形腕掌稳定支具', '原文图 5（原图未改动）', G(5), None, [
    ('bul', ['从**掌骨头**包到**桡腕关节**，牢牢托住腕掌关节', '腕和手指**可以照常活动**；拆石膏后**全天佩戴**']),
    ('box', '两个作用', '早期：减少腕掌关节受力，让周围关节尽早动\n后期：握力训练时提供**环形支撑**，减少平移和旋转应力', 'teal')])
deck.text('康复方案', '原文正文', [
    ('box', '每次治疗', '**10 分钟水疗** → 主动、被动活动度评估 → 活动度练习 → 戴支具做伸肌、屈肌腱滑动和抗阻练习', 'teal'),
    ('box', '练什么', '轻柔的被动腕、掌指、指间关节活动 + **肌腱滑动**练习；**先单关节、再复合动作**', 'yellow'),
    ('box', '屈指手套', '清醒时每次 **5～10 分钟**，被动牵伸手指', 'purple'),
    ('box', '复查和进阶', '手治疗师**每两周**复查；第 12 周停支具，开始腕和握力强化', 'coral')])
deck.figure('伤后 10 周的活动度', '原文图 6（原图未改动）', G(6), None, [
    ('steps', [('A', '握拳时腕**屈曲**'), ('B', '握拳时腕**背伸**'), ('C', '腕和手指**完全伸直**')]),
    ('box', '表 1 记录', '第 10 周：掌指、指间关节活动度**正常**；腕关节这一栏没有记录', 'grey')])
fig, ax = plt.subplots(figsize=(9.6, 6))
L = [24, 35, 46]; R = [55, 50, 54]; x = range(3)
ax.bar([i - .2 for i in x], L, .4, color='#C0392B', label='患侧（左，利手）'); ax.bar([i + .2 for i in x], R, .4, color='#9AA5B1', label='健侧（右）')
for i in x:
    ax.text(i - .2, L[i] + 1, str(L[i]), ha='center', fontsize=20); ax.text(i + .2, R[i] + 1, str(R[i]), ha='center', fontsize=20)
    ax.text(i, 64, f'{round(L[i] / R[i] * 100)}%', ha='center', fontsize=24, color='#C0392B', fontweight='bold')
ax.set_xticks(list(x), ['第 12 周', '第 16 周', '约第 26 周'], fontsize=20); ax.set_ylim(0, 82); ax.set_ylabel('握力（kg）', fontsize=20); ax.tick_params(axis='y', labelsize=16)
ax.legend(frameon=False, fontsize=17, loc='upper center', ncol=2); ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); fig.tight_layout()
deck.chart('握力恢复', '据原文表 1 重画；红字为患侧占健侧的比例', fig, [
    ('bul', ['第 12 周停支具、开始强化时只有健侧的 **44%**', '约半年时到 **85%**', '注意患侧本来是**利手**，正常时应略强于对侧'])])
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '证据很弱'),
    ('bul', ['只有 **1 例**、没有对照；没有疼痛、功能评分和长期随访', '支具由作者团队设计，原文只有照片，没给出制作方法', '石膏固定了 6 周，并不算真正的“早期”活动']),
    ('h', '原文对不上'),
    ('steps', [('1', '正文说第 10 周活动度全部恢复，表 1 腕关节要到**约第 26 周**才记为正常'), ('2', '正文说**大多角骨**骨折，图 3 写**小多角骨**用螺钉；表 1 有“6 月 31 日”')])])
deck.text('收藏：腕掌关节骨折脱位术后康复要点', '保护受伤的关节，放开没受伤的关节', [
    ('steps', [('1', '环形腕掌支具：从掌骨头包到桡腕关节，**全天佩戴**'), ('2', '腕、掌指、指间关节尽早活动：**先单关节、再复合**'),
               ('3', '**肌腱滑动**练习防粘连；屈指手套辅助牵伸'), ('4', '腕掌关节稳定后（本例 **12 周**）再做握力强化')]),
    ('box', '注意', '何时拔针、何时开始活动，以**手术医生**对固定情况的判断为准', 'yellow'),
    ('box', '文献', 'Bell T, Chinchalkar SJ, Faber K. Postoperative management of carpometacarpal joint fracture dislocation of the hand: A case report. Can J Plast Surg. 2010;18(3):e37-e40', 'navy'),
    ('box', '版权', '原文版权归 Pulsus Group 所有，非开放许可；原文图未作修改，仅供学习交流，如有侵权请联系删除', 'accent')])
deck.save(OUT)
