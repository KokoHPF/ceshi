#!/usr/bin/env python3
"""Mao、Li、Chen、Zhao 2026 青少年特发性脊柱侧弯三维牵引＋常规康复 1 例：中文标题卡、背景卡、病例卡、原文图 1、2 配中文图注，
原文图 3（英文改中文，见 prep.py）、治疗思路卡、两阶段方案卡（原文表 2）、原文图 4 加中文标签、Cobb 角与旋转角变化图（据原文表 1 重画）、
解读卡、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('病例报告 · 《Front Sports Act Living》2026', ['青少年特发性脊柱侧弯', '三维牵引＋常规康复，不戴支具能矫正吗？'],
               'Mao Z, Li C, Chen S, Zhao Z.', 'Front Sports Act Living. 2026;8:1794187. doi:10.3389/fspor.2026.1794187',
               '复旦大学附属华山医院康复医学科、上海裕华康复医院、ASPINE 公司（中美）'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
card('青少年特发性脊柱侧弯（编者根据原文整理）', [
    ('是什么', '脊柱的三维畸形：冠状面侧弯（Cobb 角 ≥10°）＋矢状面生理曲度异常＋椎体旋转\n特发性里最常见的就是青少年型（AIS）', LT, TEAL),
    ('谁容易得', '10～18 岁生长高峰期；全球患病率 1.5%～3.0%，女孩约为男孩的 3 倍', OR, (200, 120, 0)),
    ('危害', '体态畸形、背痛；Cobb 角 >40° 时肺活量可下降约 30%；还可能伴焦虑、抑郁', PK, RED),
    ('指南怎么管', '有进展风险的骨骼未成熟患者：支具＋脊柱侧弯特定运动（SOSORT 指南）\n作者强调：本例方案是对支具的补充，而不是替代', GR, (0, 120, 60)),
])
card('病例：12 岁女孩（原文）', [
    ('主诉', '数月腰痛；双肩不等高、体态差，2024 年 3 月就诊', LT, TEAL),
    ('为什么不戴支具', '戴支具夜间不适加重、依从性差；也不想手术', OR, (200, 120, 0)),
    ('查体', '身体右倾，右侧髂前上棘偏高，左腿短；Adams 前屈试验阳性\n右胸段椎旁肌紧张压痛、左腰段椎旁肌压痛；脊柱侧弯尺：T8 右旋 7°、L2 左旋 14°', GR, (0, 120, 60)),
    ('X 线', '胸段右凸（T3～T8）Cobb 22°，椎体Ⅰ度右旋\n腰段左凸（T10～L3）Cobb 40°，椎体Ⅱ度左旋 → S 形侧弯，以腰段为主弯，骶骨右偏', PU, C_NAV),
    ('其他评估', '疼痛 VAS 4 分；椎旁肌张力（改良 Ashworth）2 级；竖脊肌、髂腰肌肌力 3+ 级；平衡误差评分 17 分', PK, RED),
])
put('x209.jpg', '原文图 1  初诊时的体态：正面和背面，身体向右倾斜')
put('x278.jpg', '原文图 2  初诊和 32 周时的 X 线：胸段 Cobb 角 22° → 15°，腰段 40° → 23°（图内 A、B 为胸段前后对比，C、D 为腰段前后对比，与原文图注字母不一致）')
put('x290.zh2.jpg', '原文图 3  Cobb 角的软件计算流程：原始 X 线片 → 分段标记椎体中心 → 生成生理曲度数据 → 计算 Cobb 角（软件为作者所在公司 ASPINE 开发，英文标注已改为中文）')
card('治疗思路：先骨盆、再胸腰（原文）', [
    ('方案名称', '基于姿势的脊柱康复（PSR）：姿势矫正训练、肌肉平衡训练、三维脊柱牵引、脊柱手法', LT, TEAL),
    ('先骨盆', '主弯在腰段、骶骨右偏 → 先通过骨盆调整恢复骨盆稳定，减少侧弯的代偿', OR, (200, 120, 0)),
    ('再胸腰', '骨盆稳定后，再对胸、腰、骶段做三维矫正', GR, (0, 120, 60)),
    ('反向姿势定位（RPP）', '让脊柱向畸形的反方向摆位、训练，恢复中立对线', PU, C_NAV),
    ('手法和牵引', '下落式治疗床（Drop Table）全脊柱调整；用常规器材搭成重力辅助三维牵引平台', PK, RED),
    ('目标', '50 次治疗内把 Cobb 角维持在手术阈值（40°）以下，减少旋转和侧弯', LT, TEAL),
])
card('第一阶段：骨盆调整期（第 1～12 周，原文表 2）', [
    ('第 1～4 周', '重力牵引：右侧卧、左髋屈曲，沙袋固定 L1～L3，每次 15 分钟\n右侧卧位左腿上抬 10 秒×10 组；颈椎活动度训练 20 次；平板支撑入门', LT, TEAL),
    ('第 5～8 周', '＋TRX 菱形肌划船＋深蹲 3×15\n＋瑞士球左侧卧拉伸（凸侧竖脊肌／凹侧髂腰肌）1 分钟×3\n＋坐位镜像训练：右旋＋右移＋左侧屈 50 次；胸大肌全脊柱拉伸 5×7 秒', OR, (200, 120, 0)),
    ('第 9～12 周', '重力牵引加到 20 分钟；右侧卧抗阻抬腿 15 秒×10 组\n瑜伽砖辅助镜像训练 80 次；TRX 复合动作 3×20', GR, (0, 120, 60)),
])
card('第二阶段：胸腰调整期（第 13～32 周，原文表 2）', [
    ('第 13～20 周', '站立抗阻镜像训练：弹力带固定骨盆、左侧第 12 肋下垫泡沫垫，右旋＋右移＋左侧屈 50 次\n重力牵引 25 分钟；瑞士球左侧核心训练 2 分钟×5；I/Y/W 字母训练 10 组', LT, TEAL),
    ('第 21～28 周', '＋弹力带抗阻三维矫正 100 次；进阶平板 1 分钟×3\n＋加重 TRX 划船＋深蹲 3×25；多方向全脊柱拉伸', OR, (200, 120, 0)),
    ('第 29～32 周', '复合抗阻镜像训练（80°～100° 动态矫正）100 次；瑞士球不稳定面训练 3 分钟×3\n日常生活模拟训练；三维矫正耐力训练 5×20 秒', GR, (0, 120, 60)),
    ('生活建议', '活动前后拉伸热身；手机举到视线高度防止头前伸；连续坐不超过 1 小时，每 30～40 分钟起来活动', PU, C_NAV),
])
put(tags_at(k, 'x389.jpg', [(.03, .03, '重力牵引', C_HI), (.03, .55, '瑞士球训练', C_NAV), (.47, .03, '镜像训练', C_NAV)]),
    '原文图 4  三类训练：A 重力牵引（右侧卧、左髋屈曲、沙袋固定腰段）；B 瑞士球左侧卧拉伸；C 站立抗阻镜像训练（弹力带固定骨盆，对着镜子做右旋＋右移＋左侧屈）')
fig, axs = plt.subplots(1, 2, figsize=(12, 6.4), dpi=100)
t3 = ['初诊', '16 周', '32 周']
for ax, (nm, d) in zip(axs, [('Cobb 角（°）', {'胸段·软件': [22, 23, 15], '胸段·手测': [22, 22, 18], '腰段·软件': [40, 36, 23], '腰段·手测': [40, 38, 23]}),
                             ('最大旋转角（°）', {'胸段': [12, 15, 9], '腰段': [27, 20, 15]})]):
    for lab, ys in d.items():
        c = '#2E86AB' if '胸' in lab else '#C0392B'; ls = '--' if '手测' in lab else '-'
        ax.plot(range(3), ys, marker='o', lw=2.6, ms=8, color=c, ls=ls, label=lab)
        ax.text(2.08, ys[-1], str(ys[-1]), fontsize=13, color=c, va='center')
    ax.set_xticks(range(3), t3, fontsize=15); ax.set_title(nm, fontsize=18); ax.set_xlim(-.2, 2.4); ax.tick_params(axis='y', labelsize=13)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); ax.legend(frameon=False, fontsize=13)
axs[0].axhline(40, color='#999', ls=':', lw=1.2); axs[0].text(0, 41, '手术阈值 40°', fontsize=12, color='#777')
fig.suptitle('50 次、32 周后：腰段改善明显，胸段手测只少了 4°', fontsize=20)
fig.tight_layout(rect=(0, 0, 1, .93)); fig.savefig(f'{WORK}/cobb.png', facecolor='white'); plt.close(fig)
put('cobb.png', '据原文表 1 重画：实线为作者公司软件测量，虚线为人工测量。腰段 40° → 23°，两种方法一致；胸段软件测得 22° → 15°，人工测量只到 18°')
card('这个病例能说明什么（编者解读）', [
    ('结果', '32 周、50 次治疗后：腰段 Cobb 40° → 23°，腰段旋转 27° → 15°；腰痛 VAS 4 → 2\n肌张力下降、肌力提高、平衡误差评分 17 → 11', GR, (0, 120, 60)),
    ('要打折扣的地方', '单个病例、没有对照，难以排除其他因素的影响\n胸段人工测量只改善 4°——原文也承认 3～4° 的改善可能接近测量误差', PK, RED),
    ('利益关系', '两位作者受雇于 ASPINE 公司，Cobb 角测量软件和治疗体系都来自该公司；软件用于临床前仍需医生核对', OR, (200, 120, 0)),
    ('别误读', '作者自己也说：支具仍是有进展风险的骨骼未成熟患者的基石，本方案只适合不能耐受支具的个别患者，有待对照研究验证', LT, TEAL),
])
c = k.op('x389.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = 80
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
