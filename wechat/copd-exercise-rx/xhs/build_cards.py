#!/usr/bin/env python3
"""《慢性阻塞性肺疾病运动处方指南》（中国全科医学 2026）→ 小红书 3:4 图文卡片。
原文 CC BY-NC-ND 4.0：图 1、图 2 为整页区域渲染的原图，未作任何修改（f1.jpg、f2.jpg：
E=../../skills/paper-to-xhs-cards/scripts/extract_figures.py；python3 $E src/paper.pdf work --clip 5 44 516 296 721 f1，
--clip 5 308 66 556 258 f2）；数据图为编者据原文数据重画；卡片注明“仅供学习交流，如有侵权请联系删除”。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from io import BytesIO
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='心肺康复', source='中国全科医学 2026;29(34):4993-5009,5032', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus'] = False
F = lambda n: Image.open(f'{WORK}/{n}.jpg').convert('RGB')


def fitt_fig():
    """三类运动处方速览（编者据原文表 4～6 绘制）"""
    cols = ['有氧运动', '抗阻运动', '吸气肌训练']
    rows = [('强度', ['低强度起始\nCPET 最大强度\n50%～70%', '1-RM 50% 起\n→ 60%～80%', '≥30% PImax 起\n→ 40%～50%']),
            ('频率', ['3～5 次/周', '>3 次/周', '5～7 天/周']),
            ('时长', ['≥30 min/天', '≥40 min/天', '15～30 min/天']),
            ('周期', ['6～12 周', '4～8 周', '≥8 周'])]
    fig, ax = plt.subplots(figsize=(9.6, 6.4), dpi=100); ax.set_xlim(0, 4); ax.set_ylim(-.3, 5.7); ax.axis('off')
    cc = ['#1F5F8B', '#C0392B', '#2E8B57']
    for j, c in enumerate(cols):
        ax.add_patch(plt.Rectangle((1 + j, 4.2), .96, .7, color=cc[j])); ax.text(1.48 + j, 4.55, c, ha='center', va='center', fontsize=21, color='white', weight='bold')
    for i, (k, vals) in enumerate(rows):
        y = [2.95, 1.9, .85, -.2][i]; hh = .95 if i else 1.15
        ax.add_patch(plt.Rectangle((0, y), .96, hh, color='#E8EEF4')); ax.text(.48, y + hh / 2, k, ha='center', va='center', fontsize=20, color='#16324F', weight='bold')
        for j, v in enumerate(vals):
            ax.add_patch(plt.Rectangle((1 + j, y), .96, hh, color='#F6F8FA')); ax.text(1.48 + j, y + hh / 2, v, ha='center', va='center', fontsize=16 if i == 0 else 19, color='#222')
    fig.tight_layout(pad=.2); return fig


def fig2img(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['慢阻肺', '运动处方指南'], kicker='中国全科医学 2026 · 指南', subtitle='有氧 · 抗阻 · 吸气肌训练，22 条推荐',
           photos=[(fig2img(fitt_fig()), '三类运动处方速览（据原文表 4～6）')], banner='练前先筛查 · 练中会识别 · 居家可远程')
deck.text('为什么要专门的运动处方', '原文引言与方法', [
    ('box', '病人多', '我国慢阻肺（COPD）患者约 **1 亿**，40 岁以上患病率 **13.7%**\n已有指南都推荐运动为核心疗法，但一直缺少**专门的运动处方指南**', 'teal'),
    ('box', '怎么制订的', '医学、体育、教育、康复、循证 5 个领域专家；GRADE 分级\n纳入 **65 项 RCT、6348 例**患者做 meta 分析；证据不足的问题用专家共识（GPS）', 'navy'),
    ('box', '回答 6 个问题、形成 22 条推荐', '① 运动前筛查评估　② 有氧　③ 抗阻　④ 吸气肌训练\n⑤ 急性加重风险与运动中不良反应　⑥ 远程康复', 'yellow'),
    ('box', '适用对象', '**排除急性加重期**，经评估有一定身体活动能力的 COPD 患者\n使用者：医生、康复治疗师、运动处方师、护士、营养师等', 'grey')])
deck.text('① 运动前评估：三大块', '原文表 3；推荐 1、推荐 4（GPS，强推荐）', [
    ('box', '体力活动水平', '首选**运动传感器**（计步器、加速度计），6MWT 也能反映日常活动\n问卷准确性低、变异大，更能反映高强度活动', 'teal'),
    ('box', '疾病筛查', '病史、并发症与合并症（**心血管病**是主要死因）、血液指标（CRP、纤维蛋白原、NLR、PLR 与预后相关）、用药、症状量表、运动风险评价、相关检查', 'accent'),
    ('box', '体适能测评', '心肺耐力：CPET、6MWT、往返步行试验、坐-起测试\n肌力和耐力：MIP / MEP、握力、30 秒屈臂、股四头肌\n柔韧：坐位体前屈、抓背　平衡：TUG、BBS、BESTest\n体成分：**小腿围、中臂围**（比 BMI 更准）', 'navy')])
deck.text('症状量表 + 用药提醒', '原文 3.2', [
    ('h', '三个短量表（临界值 · 最小临床意义差值）'),
    ('steps', [('mMRC', '0～4 分；**≥2 分**为较严重呼吸困难；MCID 1'), ('CAT', '0～40 分；**≥10 分**为症状较严重；MCID 2.54'), ('CCQ', '0～6 分，越高越差；MCID 0.4')]),
    ('h', '运动时留意的药物'),
    ('box', 'β2 受体激动剂 / 抗胆碱能药', '可能心动过速、心律异常、心血管事件增加 → 运动中**监测心率**，大强度时加强医务监督\n抗胆碱能药易口干 → 注意别过度补水', 'accent'),
    ('box', '糖皮质激素', '吸入激素易降骨密度 → **避免高冲击运动**\n口服激素可致肌无力 → 及时调整处方', 'yellow')])
deck.figure('什么时候需要先做医学检查？（一）', '原文图 1：ACSM 运动前健康筛查流程（有规律运动习惯）', F('f1'), None, [
    ('bul', ['“规律运动”＝近 3 个月每周 ≥3 天、每次 ≥30 min 中等强度', '无心血管、代谢、肾脏疾病及症状 → **不必筛查**，可继续并逐渐进阶', '有任何相关症状或体征 → 继续运动的同时**做医学筛查**'])])
deck.figure('什么时候需要先做医学检查？（二）', '原文图 2：ACSM 运动前健康筛查流程（无规律运动习惯）', F('f2'), None, [
    ('box', '推荐 2、3（GPS，强推荐）', '无规律运动习惯者，**即使没有症状**，运动前也应做医学检查\n有规律运动、无症状者继续低到中等强度可不查，但要监测症状、心率、血压、SpO2；**进阶到更大强度前**需检查', 'teal')])
deck.text('体适能测评：常用数字', '原文 3.5', [
    ('box', '心肺耐力', 'CPET 测 VO2max 是“金标准”；6MWT 可在多数场合替代\n耐力往返步行（ESWT）按 ISWT 峰速的 **85%** 走到力竭，对康复变化更灵敏\n1 分钟坐-起可替代 6MWT', 'teal'),
    ('box', '握力', '亚洲肌少症共识：男 **<28 kg**、女 **<18 kg** 为虚弱；双侧比 **>1.1** 为不对称', 'accent'),
    ('box', '平衡', 'TUG 快速筛跌倒风险；BBS 的 MCID **5**（有天花板效应）；BESTest 更全面（约 45 min），MCID **13**', 'yellow'),
    ('box', '体成分', '低体重、低去脂体重与死亡率升高相关；**小腿围、中臂围**比 BMI 更能预测预后', 'navy')])
deck.rows('② 有氧运动处方', '推荐 5～9', [
    ('长期规律有氧（B，强）', '改善呼吸困难、活动能力、肺功能和心肺耐力；初次在专业人员指导下练', '首选的基础处方', 'teal'),
    ('强度（B，弱）', '中低至中高强度；中高强度可设 CPET 最大强度的 50%～70%；太极、八段锦靶心率为预测最大心率的 43%～49% 或 6MWT 测得最大心率的 40%～60%', '低强度起始，结合 Borg 评分和呼吸调整', 'yellow'),
    ('频率（B，强）', '每周 3～5 次；耐受时太极、八段锦可每周 3～7 次', '3～5 次/周', 'navy'),
    ('时长与周期（A，强）', '要显著提升心肺耐力', '每天 ≥30 min，坚持 6～12 周', 'accent'),
    ('方式（B，强）', '快走、慢跑、踏车、游泳，以及八段锦、太极拳、瑜伽', '八段锦以略有累感、心率增加 <20 次/min、呼吸增加 <5 次/min 为宜', 'purple')])
fig, ax = plt.subplots(figsize=(9.6, 5.2))
lab = ['FEV1', '6MWD', 'FEV1/FVC', 'CAT 评分']; v = [.79, .77, 1.54, -2.36]; lo = [.44, .39, .88, -3.05]; hi = [1.14, 1.15, 2.20, -1.67]
y = list(range(4))[::-1]
for yy, a, l, h in zip(y, v, lo, hi):
    c = '#2E8B57' if a > 0 else '#C0392B'; ax.plot([l, h], [yy, yy], color=c, lw=4); ax.plot(a, yy, 's', ms=16, color=c)
    ax.text(a, yy + .3, f'{a:+.2f}', ha='center', fontsize=17)
ax.axvline(0, color='#555', lw=1.2); ax.set_yticks(y, lab, fontsize=19); ax.set_xlim(-3.4, 2.6); ax.set_ylim(-.6, 3.7)
ax.set_xlabel('标准化均数差 SMD（95% CI）　CAT 越低越好', fontsize=15); ax.tick_params(axis='x', labelsize=14)
ax.spines[['top', 'right', 'left']].set_visible(False); ax.grid(axis='x', alpha=.3); fig.tight_layout()
deck.chart('有氧运动的证据', '据原文推荐说明数据重画（20 项 RCT，n=1915）', fig, [
    ('bul', ['肺功能、6 分钟步行距离提高，CAT 评分下降', '亚组：单次 **>30 min**、每周 **>3 次**获益更明显', '常规有氧（快走、慢跑、踏车）提升肺功能比传统功法更多（SMD 2.58 vs 1.09）'])])
deck.text('③ 抗阻运动处方', '推荐 10～14', [
    ('box', '长期规律抗阻（B，强）', '改善呼吸困难、肌力和心肺耐力；募集小肌群、减轻通气负担', 'teal'),
    ('steps', [('强度', '从 **1-RM 50%** 起 → 耐受后进阶到 **60%～80%**（B，强）'), ('频率', '每周 **>3 次**（B，强）'),
               ('时长', '每天 **≥40 min**（需能耐受），周期 **4～8 周**（B，弱）'),
               ('方式', '杠铃、哑铃、弹力带、壶铃；坐姿推胸、腿举、坐姿划船；俯卧撑、深蹲、平板支撑等（B，强）')]),
    ('box', '和有氧一起练', '21 项 RCT（n=1397）：单纯抗阻提高 6MWD（SMD 0.91），**抗阻＋有氧**更多（SMD 1.82）', 'accent'),
    ('box', '指标', 'FEV1、最高摄氧量、握力、6MWD 提高；Borg、SGRQ、mMRC 下降', 'grey')])
deck.text('④ 吸气肌训练（IMT）', '推荐 15～19（均为 C 级证据，弱推荐）', [
    ('box', '谁适合', '吸气肌力减弱：**PImax <60 cmH2O** 的患者，作为辅助手段', 'teal'),
    ('steps', [('强度', '至少 **30% PImax** 起；每周复测，调到当前 PImax 的 **40%～50%**'), ('进阶', '每周递增 **5%～10%**；单次增幅 >15% 中断率升高'),
               ('频率', '每周 **5～7 天**（<3 次/周难有生理适应）'), ('时长', '每天 **15～30 min**，可分组，如练 2 min 歇 1 min'),
               ('方式', '优先**阈值负荷装置**；“缓慢深吸气＋充分呼气”')]),
    ('box', '别过量', '<30% PImax 难以诱发适应，**>60%** 可能增加急性加重风险；坚持 **≥8 周** PImax 可提升 30%～50%，停练后效益会消退', 'accent'),
    ('box', '共振呼吸（探索中）', '约 **6 次/min** 的慢呼吸使心率随呼吸波动最大，可调节自主神经；期待在 COPD 中进一步应用', 'grey')])
fig, ax = plt.subplots(figsize=(9.6, 4.8))
lab = ['单纯有氧', '单纯抗阻', '有氧＋抗阻', '其他（呼吸训练、间歇等）']; rr = [1.07, .61, .79, .49]; lo = [.94, .11, .71, .33]; hi = [1.21, 3.27, .87, .73]
y = list(range(4))[::-1]
for yy, a, l, h in zip(y, rr, lo, hi):
    c = '#2E8B57' if h < 1 else '#9AA5B1'; ax.plot([l, min(h, 1.8)], [yy, yy], color=c, lw=4); ax.plot(a, yy, 's', ms=15, color=c)
    ax.text(1.85, yy, f'RR {a:.2f}', va='center', fontsize=16)
ax.axvline(1, color='#555', lw=1.2); ax.set_yticks(y, lab, fontsize=17); ax.set_xlim(0, 2.3); ax.set_ylim(-.6, 3.6)
ax.set_xlabel('不良事件风险比 RR（<1 表示低于对照组；抗阻组上限 3.27 已截断）', fontsize=13); ax.tick_params(axis='x', labelsize=13)
ax.spines[['top', 'right', 'left']].set_visible(False); ax.grid(axis='x', alpha=.3); fig.tight_layout()
deck.chart('⑤ 运动安全吗？', '推荐 20（B，弱推荐）；据原文 meta 分析数据重画', fig, [
    ('bul', ['运动使**急性加重风险降低 18%**（RR 0.82，9 项研究，异质性极低）', '总不良事件降低 19%，但 P=0.05，**处于显著性边缘**', '有氧＋抗阻联合、分阶段练、组间休息、配合呼吸训练的组不良事件更少', '纳入研究的运动强度都是 Borg **3～6 分**的中等强度'])])
deck.text('⑥ 什么时候该停下来', '推荐 21（B，强推荐）：纳入研究用过的停止标准', [
    ('box', '盯住 4 个客观指标', '**SpO2**：低于 85%～90%（各研究阈值不同）\n**Borg**：≥5～7 分\n**心率**：>最大心率的 85%～90%，或 >130 / <40 次/min，或比静息升高 >50%，或出现严重心律失常\n**血压**：≥200/100 或 >180/100 mmHg；收缩压 <90 mmHg', 'accent'),
    ('box', '问清主观不适', '胸痛、胸闷、心悸、头晕、濒死感；咳嗽咳痰加重、辅助呼吸、三凹征；肌肉疼痛', 'yellow'),
    ('box', '处理', '调整或停止运动，医生评估；急性加重时吸氧、用药、送医\n负荷每周调整、循序渐进，主观疲劳评分保持 **≤14 分**', 'teal'),
    ('box', '远程康复（推荐 22，B，强）', '视频、电话、App 或混合模式；效果与门诊肺康复相当，**完成率 93% vs 70%**；维护性远程康复 6MWD 平均多 **78.1 m**', 'navy')])
deck.text('局限 + 原文细节', '原文总结与编者整理', [
    ('h', '指南自己说的局限'),
    ('bul', ['不适用于**急性加重期**患者', '传统功法 RCT 少，太极、八段锦只纳入了中低强度有氧']),
    ('h', '编者提醒'),
    ('bul', ['吸气肌训练 5 条推荐都是 **C 级证据、弱推荐**', '“显著降低不良事件”主要来自亚组分析，总效应 P=0.05']),
    ('h', '原文对不上的地方'),
    ('steps', [('1', '表 4 写“6MWT 测得 HRmax 43%～49%”，正文和推荐 6 是 **40%～60%**'), ('2', '吸气肌训练亚组中 MIP 和 6MWD 的 SMD 与 95%CI **完全相同**（1.1，0.22～1.98）'),
               ('3', '抗阻部分 Borg 与 SGRQ 总分的 SMD、95%CI 也**完全相同**（-0.57，-0.84～-0.30）')])])
deck.text('收藏：COPD 运动处方速查', '据原文整理', [
    ('steps', [('有氧', '3～5 次/周 · ≥30 min · 6～12 周 · 低强度起步'), ('抗阻', '>3 次/周 · ≥40 min · 4～8 周 · 1-RM 50%→60%～80%'),
               ('IMT', 'PImax<60 才练 · 30%→40%～50% · 每周+5%～10% · 5～7 天/周 · 15～30 min'),
               ('停', 'SpO2 <85%～90% · Borg ≥5～7 · 胸痛胸闷心悸头晕'), ('查', '无运动习惯者先做医学检查')]),
    ('box', '文献', '白云飞, 张永明, 李述刚, 等. 慢性阻塞性肺疾病运动处方指南[J]. 中国全科医学, 2026, 29(34): 4993-5009, 5032. DOI: 10.12114/j.issn.1007-9572.2026.0155', 'navy'),
    ('box', '版权', '原文 **CC BY-NC-ND 4.0**：图 1、图 2 为原图，未作修改；其余为编者整理和重画。**仅供学习交流，如有侵权请联系删除**', 'grey')])
deck.save(OUT)
