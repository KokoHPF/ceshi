#!/usr/bin/env python3
"""Saito 等 2025 髋关节镜术后臀部痛的闭孔神经靶向治疗 2 例 → 小红书 3:4 图文卡片。原文 CC BY 4.0。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='髋关节康复', source='Saito 等 Cureus 2025;17(10):e95021', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
X = lambda n: Image.open(f'{WORK}/x{n}.jpg').convert('RGB')
f2, f4, f5 = X(49), X(83), X(138)
# 分界列由相邻列灰度差最大处定出（原图各分图之间没有白边）
f2a, f2b = f2.crop((0, 0, 1316, f2.height)), f2.crop((1326, 0, f2.width, f2.height))
f4a, f4b, f4c = f4.crop((0, 0, 1005, f4.height)), f4.crop((1014, 0, 1947, f4.height)), f4.crop((1956, 0, f4.width, f4.height))
f5a, f5b = f5.crop((0, 0, 1507, f5.height)), f5.crop((1516, 0, f5.width, f5.height))

deck.cover(['超声引导下闭孔神经靶向', '物理治疗：髋关节镜术后', '顽固臀部痛 2 例'], kicker='Cureus 2025 · 病例报告',
           subtitle='FAI 术后屁股还痛，想想闭孔神经',
           photos=[(f2b, '超声长轴图'), (f5b, '关节支急转弯'), (f4b, '神经滑动')], banner='水分离 + 手法 + 闭孔外肌激活')
deck.text('为什么关注术后臀部痛', '原文引言', [
    ('box', '关节镜不是“一做就好”', '股骨髋臼撞击症（FAI）术后回归运动约 **93%**，回到术前水平约 **82%**；部分人多年仍痛', 'teal'),
    ('box', '臀部痛被忽略', '术后**腹股沟痛**研究多；**臀部痛**和闭孔神经的关系很少被关注', 'yellow'),
    ('box', '闭孔神经为什么可疑', '发出**关节支**支配髋关节囊；走行在**闭孔外肌和闭孔内肌之间**，可能被卡压或滑动受限', 'accent')])
deck.text('两位患者', '原文', [
    ('box', '病例 1：40 多岁女性', '右髋关节镜（盂唇撕裂）术后 **8 个月**，**走路**时臀部痛\n关节内注射、富血小板血浆、坐骨神经水分离都无效', 'teal'),
    ('box', '病例 2：30 多岁男性', '左髋关节镜术后 **11 个月**，髋**外展外旋**时臀部剧痛\n关节内注射无效', 'coral'),
    ('box', '共同发现', 'FABER 诱发臀部痛（NRS **5、7**）；膝－床距离增大；髋外旋肌力 **2 级**\n超声下**闭孔外肌收缩差**，闭孔神经周围**压痛**', 'navy')])
deck.figure('FABER 位测膝－床距离', '原文图 1（演示模型；Tt 胫骨结节，BS 床面）', X(34), None, [
    ('bul', ['仰卧，被测髋**屈曲、外展、外旋**', '用尺子测膝外侧到床面的**垂直距离**；越大越“打不开”']),
    ('box', '两例首诊', '病例 1：患侧 **35.5** cm vs 健侧 26.5 cm\n病例 2：患侧 **31.0** cm vs 健侧 24.5 cm', 'yellow')])
deck.figure('关节支的“急转弯”', '原文图 5：作者自制模型', [f5a, f5b], ['中立位', 'FABER 位'], [
    ('bul', ['关节支穿出闭孔管后**突然转向**（▼处），容易卡住', 'FABER 牵拉**前下关节囊**——正是闭孔神经关节支的支配区', '痛在臀部不在前方会阴；坐骨神经水分离无效 → 更像**闭孔神经**'])])
deck.text('治疗方案', '原文', [
    ('steps', [('频率', '每周 1 次手法 + 运动；每两周 1 次**水分离**'), ('1', '**短轴滑动手法**：超声下在闭孔外肌和闭孔内肌之间滑动神经'),
               ('2', '**闭孔外肌激活**：看实时超声反复收缩，到压痛减轻'), ('3', '**水分离**：闭孔外肌深层注入 10 ml 0.09% 利多卡因盐水'),
               ('4', '注射后立即做**牵拉—放松**神经滑动')]),
    ('box', '为什么必须超声引导', '闭孔神经和周围结构**单靠触诊定不准**', 'accent')])
deck.figure('短轴滑动手法', '原文图 2（图中缩写见下方）', [f2a, f2b], ['解剖示意', '超声长轴'], [
    ('bul', ['超声显示**闭孔外肌长轴**和**闭孔管**', '手指从**耻骨下支、坐骨支**方向深入，在两块闭孔肌之间滑动神经']),
    ('box', '图中缩写', 'EO 闭孔外肌；IO 闭孔内肌；OC 闭孔管；Ac 髋臼；FH 股骨头', 'grey'),
    ('box', '原文附视频', '原文附示意动画和超声下操作视频（视频 1、2）', 'teal')])
deck.figure('超声反馈下激活闭孔外肌', '原文图 3（演示模型）', X(68), None, [
    ('bul', ['看着**实时超声**画面反复收缩闭孔外肌', '重复到**收缩改善、局部压痛减轻**为止']),
    ('box', '为什么练它', '作者认为闭孔外肌重新激活可增强髋关节**动态稳定**', 'teal')])
deck.figure('长轴滑动：牵拉—放松', '原文图 4', [f4a, f4b, f4c], ['起始', '牵拉', '放松'], [
    ('steps', [('牵', '仰卧，髋**内旋 + 外展** → 牵拉闭孔神经'), ('松', '髋**外旋 + 内收** → 放松神经'), ('复', '反复进行，直到活动**阻力消失**')]),
    ('box', '什么时候做', '每次**水分离注射后立即**做，希望既发挥药液作用，又促进神经滑动', 'yellow')])
fig, axs = plt.subplots(1, 2, figsize=(9.6, 6))
for ax, (nm, a, b, yl) in zip(axs, [('FABER 痛（NRS）', [5, 3, None, 0], [7, 2, 2, None], (0, 8.5)), ('膝－床距离（cm）', [26.8, 23.5, 22, 22], [21, 20, 20, None], (18, 28.5))]):
    for ys, c, lab in ((a, '#2E86AB', '病例 1'), (b, '#C0392B', '病例 2')):
        xs = [i for i, y in enumerate(ys) if y is not None]; v = [y for y in ys if y is not None]
        ax.plot(xs, v, marker='o', lw=3, ms=10, color=c, label=lab)
        for x, y in zip(xs, v): ax.text(x, y + (yl[1] - yl[0]) * .04, f'{y:g}', ha='center', fontsize=16, color=c)
    ax.set_xticks(range(4), ['0周', '1周', '2周', '4周'], fontsize=16); ax.set_ylim(*yl); ax.set_title(nm, fontsize=21)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); ax.tick_params(axis='y', labelsize=14)
axs[0].legend(frameon=False, fontsize=16); fig.tight_layout()
deck.chart('结果：每次治疗后都改善', '据原文表 1 重画；空缺处原文未记录', fig, [
    ('bul', ['闭孔外肌分级：两例都 **2 → 4 级**', '步行痛：病例 1 **第 4 次**消失，病例 2 **第 3 次**消失', '最后一次治疗后随访 **>6 个月**，均未复发'])])
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '证据很弱'),
    ('bul', ['只有 **2 例**、没有对照；不能排除安慰剂、自然恢复', '水分离、手法、运动**同时用**，分不清谁起作用', '没用标准化量表；按压力度没量化；没评估阴部神经']),
    ('h', '原文对不上'),
    ('steps', [('1', '正文首诊膝－床距离 35.5、31.0 cm，表 1 第 1 次却是 **26.8、21** cm'), ('2', '正文测“髋外旋肌力”，表 1 记为“**闭孔外肌分级**”')])])
deck.text('收藏：术后臀部痛想到闭孔神经', '髋关节镜术后、关节内注射无效时', [
    ('steps', [('查', 'FABER 诱发**臀部痛**、膝－床距离增大、髋外旋无力'), ('超', '超声：闭孔外肌**收缩差**、闭孔神经周围**压痛**'),
               ('练', '超声反馈下**闭孔外肌激活**'), ('滑', '髋内旋外展 ↔ 外旋内收的**神经滑动**'), ('注', '**水分离**须由有资质的医生超声引导下操作')]),
    ('box', '文献', 'Saito M, et al. Ultrasound-Guided Obturator Nerve-Targeted Physical Therapy for Persistent Buttock Pain After Hip Arthroscopy for FAI: A Report of Two Cases. Cureus. 2025;17(10):e95021', 'navy'),
    ('box', '版权', '原文 **CC BY 4.0** 开放获取；原文图 2、4、5 切分为单幅', 'teal')])
deck.save(OUT)
