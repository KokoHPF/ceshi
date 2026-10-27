#!/usr/bin/env python3
"""Mao 等 2026 青少年特发性脊柱侧弯三维牵引＋常规康复 1 例 → 小红书 3:4 图文卡片。
原文 CC BY：图 2、图 4 按分隔线切成单幅；图 3 用 ../tools/prep.py 生成的中文版 x290.zh2.jpg。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='脊柱侧弯', source='Mao 等 Front Sports Act Living 2026;8:1794187', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
O = lambda f: Image.open(f'{WORK}/{f}').convert('RGB')
f2, f4 = O('x278.jpg'), O('x389.jpg')
x2 = {k: f2.crop(b) for k, b in {'A': (0, 0, 729, 740), 'B': (771, 0, 1500, 740), 'C': (0, 776, 729, 1654), 'D': (771, 776, 1500, 1654)}.items()}
x4 = {k: f4.crop(b) for k, b in {'A': (0, 0, 629, 520), 'B': (0, 530, 629, 1028), 'C': (638, 0, 1399, 1028)}.items()}

deck.cover(['三维脊柱牵引＋常规康复', '矫正青少年特发性', '脊柱侧弯：1 例报告'], kicker='Front Sports Act Living 2026',
           subtitle='戴不了支具，32 周腰段 Cobb 角 40°→23°',
           photos=[(x4['C'], '镜像训练'), (x2['C'], '初诊腰段 40°'), (x2['D'], '32 周 23°')], banner='先骨盆、再胸腰 · 两阶段方案')
deck.text('青少年特发性脊柱侧弯', '原文引言', [
    ('box', '是什么', '脊柱**三维畸形**：冠状面侧弯（Cobb ≥10°）＋矢状面曲度异常＋**椎体旋转**', 'teal'),
    ('box', '谁容易得', '**10～18 岁**生长高峰；患病率 1.5%～3.0%；女孩约为男孩的 **3 倍**', 'yellow'),
    ('box', '危害', '体态畸形、背痛；Cobb >40° 时肺活量可下降约 **30%**；焦虑、抑郁', 'accent'),
    ('box', '指南', '有进展风险的骨骼未成熟患者：**支具＋特定运动**（SOSORT）\n作者强调本方案是**补充**，不是替代支具', 'navy')])
deck.text('病例：12 岁女孩', '原文', [
    ('bul', ['数月**腰痛**、双肩不等高；戴支具夜间不适、**依从性差**，也不想手术']),
    ('box', '查体', '身体右倾、右髂前上棘偏高、左腿短；**Adams 前屈试验阳性**\n脊柱侧弯尺：T8 右旋 7°、L2 左旋 14°', 'teal'),
    ('box', 'X 线：S 形侧弯', '胸段右凸 **22°**（T3～T8）＋腰段左凸 **40°**（T10～L3）\n以**腰段为主弯**，骶骨右偏', 'accent'),
    ('box', '其他评估', 'VAS **4**；椎旁肌张力 2 级；竖脊肌、髂腰肌肌力 3+ 级；平衡误差 **17** 分', 'yellow')])
deck.figure('初诊体态', '原文图 1', O('x209.jpg'), None, [
    ('bul', ['正面、背面都可见身体**向右倾斜**', '双肩不等高，骨盆不对称']),
    ('box', '体态评估', '图中绿线为垂直参考线，红线连接两侧肩、肋、骨盆等标志点', 'grey')])
deck.figure('X 线：胸段 22° → 15°', '原文图 2 上半（A 初诊、B 32 周）', [x2['A'], x2['B']], ['初诊 22°', '32 周 15°'], [
    ('bul', ['胸段右凸，软件测 **22° → 15°**', '人工测量 22° → **18°**，只少了 4°']),
    ('box', '怎么看', '胸段是次弯；两种测量方法差 3°，改善幅度**接近测量误差**', 'grey'),
    ('box', '图中标注', 'COBB＝Cobb 角；−TxT＝胸段顶椎偏离骶骨中垂线的距离（1.57 → 1.24 cm）', 'teal')])
deck.figure('X 线：腰段 40° → 23°', '原文图 2 下半（C 初诊、D 32 周）', [x2['C'], x2['D']], ['初诊 40°', '32 周 23°'], [
    ('bul', ['腰段左凸 **40° → 23°**，软件和人工测量一致', '顶椎偏离骶骨中垂线 2.4 cm → 1.7 cm']),
    ('box', '意义', '主弯从手术阈值 **40°** 降到 **23°**；旋转角 27° → 15°', 'yellow'),
    ('box', '注意', '原文图注把 B、C 的字母写反了，以图内标注为准', 'grey')])
deck.figure('Cobb 角怎么算的', '原文图 3（英文已改中文）', O('x290.zh2.jpg'), None, [
    ('steps', [('1', '原始 X 线片 → 分段**标记椎体中心**'), ('2', '生成生理曲度数据'), ('3', '自动计算 **Cobb 角**')]),
    ('box', '注意', '软件由作者所在的 **ASPINE 公司**开发，用 3000～4000 张侧弯片训练；临床使用前需**医生核对**', 'accent')])
deck.text('治疗思路：先骨盆、再胸腰', '原文 2.4～2.5', [
    ('steps', [('1', '**PSR**：姿势矫正、肌肉平衡训练、**三维脊柱牵引**、脊柱手法'), ('2', '主弯在腰段、骶骨右偏 → **先调骨盆**，减少代偿'),
               ('3', '骨盆稳定后 → **胸腰骶段三维矫正**'), ('4', '**反向姿势定位（RPP）**：向畸形反方向摆位和训练'), ('5', '下落式治疗床全脊柱调整')]),
    ('box', '目标', '50 次内把 Cobb 角维持在手术阈值 **40°** 以下', 'yellow')])
deck.figure('重力牵引', '原文图 4A', x4['A'], None, [
    ('steps', [('1', '**右侧卧**（凸侧在下），**左髋屈曲**'), ('2', '沙袋固定 **L1～L3**，每次 15 → 20 → 25 分钟'), ('3', '之后右侧卧位**左腿上抬** 10 秒×10 组')]),
    ('box', '设计意图', '轴向牵引减少腰段旋转应力；左髋屈曲让右侧髂腰肌离心收缩，帮助骨盆对称', 'teal')])
deck.figure('瑞士球 + 镜像训练', '原文图 4B、4C', [x4['B'], x4['C']], ['瑞士球', '镜像训练'], [
    ('bul', ['瑞士球**左侧卧**：拉伸凸侧竖脊肌、凹侧髂腰肌，练核心', '镜像训练：对着镜子做**右旋＋右移＋左侧屈**', '后期站立位：弹力带固定骨盆，左第 12 肋下垫泡沫垫']),
    ('box', '剂量', '瑞士球 1 分钟×3 → 2 分钟×5；镜像训练 50 → 80 → 100 次', 'teal')])
deck.text('两阶段方案', '原文表 2', [
    ('box', '第 1～4 周', '重力牵引 15 分钟；右侧卧左腿上抬；颈椎活动度；平板入门', 'teal'),
    ('box', '第 5～12 周', '＋TRX 划船＋深蹲；瑞士球左侧卧拉伸；坐位镜像训练 50～80 次；牵引加到 20 分钟', 'yellow'),
    ('box', '第 13～20 周', '站立抗阻镜像训练；牵引 25 分钟；瑞士球核心；**I/Y/W** 字母训练', 'purple'),
    ('box', '第 21～32 周', '弹力带抗阻三维矫正 100 次；不稳定面训练；**日常生活模拟**；三维矫正耐力', 'coral')])
fig, axs = plt.subplots(1, 2, figsize=(9.6, 6))
for ax, (nm, d) in zip(axs, [('Cobb 角（°）', {'胸·软件': [22, 23, 15], '胸·手测': [22, 22, 18], '腰·软件': [40, 36, 23], '腰·手测': [40, 38, 23]}),
                             ('旋转角（°）', {'胸段': [12, 15, 9], '腰段': [27, 20, 15]})]):
    for lab, ys in d.items():
        ax.plot(range(3), ys, marker='o', lw=3, ms=9, color='#2E86AB' if '胸' in lab else '#C0392B', ls='--' if '手测' in lab else '-', label=lab)
    ax.set_xticks(range(3), ['初诊', '16周', '32周'], fontsize=18); ax.set_title(nm, fontsize=22); ax.tick_params(axis='y', labelsize=16)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); ax.legend(frameon=False, fontsize=13, loc='upper right')
fig.tight_layout()
deck.chart('结果：腰段改善明显', '据原文表 1 重画；虚线为人工测量', fig, [
    ('bul', ['腰段 Cobb **40° → 23°**，旋转 **27° → 15°**', '胸段软件 22° → 15°，人工只到 **18°**', 'VAS 4 → **2**；平衡误差 17 → **11**；肌力 3+ → **4+**'])])
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '要打折扣'),
    ('bul', ['只有 **1 例**、没有对照；多种方法同时用，分不清谁起作用', '胸段人工只改善 4°，原文也承认 3～4° 可能接近**测量误差**', '两位作者受雇于 **ASPINE 公司**，软件和治疗体系都出自该公司']),
    ('h', '原文对不上'),
    ('steps', [('1', '摘要写“右凸胸腰段侧弯 40°”，正文是胸右凸 22°＋腰左凸 40° 的 **S 形**'), ('2', '图 2 图注的 B、C 与图内内容**对调**'),
               ('3', 'MI 在图注是**镜像**训练，讨论里写成**运动想象**')])])
deck.text('收藏：AIS 不能戴支具时的思路', '前提：首选仍是支具＋特定运动', [
    ('steps', [('1', '评估骨盆、腿长，找**主弯** → 先稳骨盆'), ('2', '重力牵引：**凸侧在下**侧卧，固定主弯节段'), ('3', '镜像训练：对着镜子做**反向矫正**（旋转＋平移＋侧屈）'),
               ('4', '核心、TRX、I/Y/W 等**肌肉平衡**训练'), ('5', '定期拍片，以 **Cobb 角**判断疗效')]),
    ('box', '文献', 'Mao Z, Li C, Chen S, Zhao Z. Integration of three-dimensional spinal traction and conventional rehabilitation for structural correction in adolescent idiopathic scoliosis: a case report. Front Sports Act Living. 2026;8:1794187', 'navy'),
    ('box', '版权', '原文 **CC BY 4.0**；图 3 英文改中文，图 2、4 切分为单幅', 'teal')])
deck.save(OUT)
