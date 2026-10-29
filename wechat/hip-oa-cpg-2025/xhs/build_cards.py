#!/usr/bin/env python3
"""《髋痛与活动受限——髋骨关节炎物理治疗临床实践指南(2025版)》更新解读（中国中医骨伤科杂志 2026）→ 小红书 3:4 图文卡片。
原文非开放许可：图 1 为原文嵌入图（x69.jpg），原样使用未作修改；推荐等级变化图为编者据原文表 2 绘制；卡片注明“仅供学习交流，如有侵权请联系删除”。
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
deck = Deck(series='髋关节康复', source='中国中医骨伤科杂志 2026;34(10):1-7', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
F = lambda n: Image.open(f'{WORK}/{n}.jpg').convert('RGB')


def grade_fig(w=9.6, h=5.0):
    """2017 → 2025 推荐等级变化（编者据原文表 2 绘制）"""
    G = {'A': 4, 'B': 3, 'C': 2, 'D': 1}
    rows = [('手法治疗', 'A', 'A', '证据 I～IV → I/II'), ('体能训练', 'A', 'A', '证据 I～III → I/II'), ('体重管理', 'C', 'B', '证据 III → I'),
            ('超声治疗', 'B', 'D', '证据 I → I'), ('干针治疗', None, 'A', '新增，证据 I')]
    fig, ax = plt.subplots(figsize=(w, h), dpi=100)
    for i, (k, a, b, note) in enumerate(rows):
        c = '#2E8B57' if (a and G[b] > G[a]) or a is None else ('#C0392B' if G[b] < G[a] else '#1F5F8B')
        if a: ax.plot([0, 1], [G[a] + i * .0, G[b]], color=c, lw=0)
        y = len(rows) - 1 - i
        ax.text(-.05, y, k, ha='right', va='center', fontsize=20, color='#16324F', weight='bold')
        ax.text(.25, y, a or '—', ha='center', va='center', fontsize=26, color='#888')
        ax.annotate('', xy=(.62, y), xytext=(.36, y), arrowprops=dict(arrowstyle='->', lw=3, color=c))
        ax.text(.72, y, b, ha='center', va='center', fontsize=30, color=c, weight='bold')
        ax.text(.86, y, note, ha='left', va='center', fontsize=15, color='#555')
    ax.set_xlim(-.55, 1.6); ax.set_ylim(-.5, len(rows) + .3); ax.axis('off'); fig.tight_layout(pad=.3); return fig


def fig2img(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['髋骨关节炎', '物理治疗指南', '2025 版更新'], kicker='APTA 指南 · 中文解读',
           subtitle='哪些升级、哪些降级、哪些新增', photos=[(fig2img(grade_fig()), '推荐等级 2017 → 2025（据原文表 2）')], banner='手法 A · 运动 A · 干针 A · 减重 B · 超声 D')
deck.text('这份指南是什么', '原文引言与指南概况', [
    ('box', '来源', '美国物理治疗协会（APTA）2025 年在 **JOSPT** 发布《Hip Pain and Mobility Deficits—Hip Osteoarthritis: Revision 2025》，是 2017 版之后的**第二次更新**\n本文是长春中医药大学团队的中文解读', 'navy'),
    ('box', '这次更新回答一个问题', '“针对髋骨关节炎患者的**物理治疗干预**证据是什么？”\n纳入 2016 年以来近 10 年的研究，以 I/II 级 RCT 为主', 'teal'),
    ('box', '怎么读等级', '证据等级 I～V（牛津循证医学中心）；推荐等级 A～F：\n**A** 强证据　**B** 中等证据　**C** 弱证据　**D** 证据冲突　**F** 专家团队的最佳实践意见', 'yellow'),
    ('box', '前提', '绝大多数治疗方法只适用于**轻、中度**髋骨关节炎；非药物治疗是核心和一线', 'grey')])
deck.text('① 怎么判断是髋骨关节炎', '沿用 2017 版 A 级推荐', [
    ('box', '临床分类标准', '**50 岁以上**，负重活动时中等程度的**前方腹股沟区或外侧髋痛**\n**晨僵 <1 h**\n并有以下任一：\n• 髋内旋 **<24°**\n• 髋内旋和屈曲比健侧少 **≥15°**\n• 被动内旋诱发疼痛加重', 'teal'),
    ('box', '注意', '美国风湿病学会用的是髋内旋 <15°；2017 版已改成 **<24°**，2025 版沿用', 'yellow'),
    ('box', '框架', '按 WHO《国际功能、残疾和健康分类》（ICF）做损伤/功能导向的诊断，指导评估和治疗', 'grey')])
deck.text('② 影像：新增检查路径和分级', '2025 版新增', [
    ('steps', [('1', '先拍**骨盆和髋关节 X 线**'), ('2', '平片正常或不清楚 → **诊断性超声**看关节外病变'), ('3', '仍不够 → **MRI 或 CT**')]),
    ('box', 'Kellgren-Lawrence 分级（0～4 级）', '看关节间隙狭窄、骨赘、软骨下硬化、关节畸形；应用最广', 'teal'),
    ('box', 'Tönnis 分级（0～3 级）', '看间隙变窄、骨赘、软骨下囊肿、骨硬化、股骨头变形', 'navy'),
    ('box', '为什么要分级', '干针推荐就限定在 **K-L 2/3 级**患者', 'accent')])
deck.text('③ 评估：最小数据集', '2025 版新增“最佳实践要点”', [
    ('box', '底线要求', '至少 **1 项自评量表 + 1 项躯体功能测试**，再加疼痛、关节刺激性、髋活动度、肌力\n基线测一次，**至少再随访 1 次**（出院或治疗结束时）', 'accent'),
    ('box', '疼痛用 NPRS', '比 VAS 更省时、可口头问，适合门诊、电话、线上随访', 'teal'),
    ('box', '常用工具', '自评：WOMAC、HOOS、PROMIS、LEFS\n功能：6MWT、30 s 坐立、上下楼梯、TUG、自主步速、单腿站立、四方格跨步、台阶测试\n损伤：NPRS、FABER、被动髋活动度、髋部肌力', 'yellow'),
    ('box', '怎么组合', '门诊：**PROMIS 或 WOMAC 功能分量表 + TUG + NPRS**\n住院/康复：**WOMAC/HOOS + 6MWT**，能做再加 30 s 坐立\n只用 NPRS+TUG 适合快速筛查，但**不满足**最低要求', 'navy')])
deck.text('④ 手法治疗：A 级，证据升到 I/II', '重点推荐 MWM 和长轴牵引', [
    ('box', '动态松动术（MWM）', '在关节上持续施加附加滑动，同时让患者做原本受限或疼痛的动作（如屈髋、内旋），追求少痛或无痛\n高质量系统评价：**单次**即可减痛、增加屈曲和内旋，并改善 TUG、30 s 坐立、步速', 'teal'),
    ('box', '长轴牵引', '沿股骨长轴牵引，减少关节压缩、改善关节囊\n不同力度都能改善疼痛和功能：**高力度更增活动度，低力度更偏镇痛**', 'navy'),
    ('box', '剂量', '每周 **1～3 次**，持续 **6～12 周**', 'yellow'),
    ('box', '知识缺口', '个体化方法、对结构的影响、长期疗效仍需研究', 'grey')])
deck.text('⑤ 运动：A 级，强调个体化', '体能训练', [
    ('box', '剂量', '每周 **1～5 次**，每次 **30～120 min**，持续 **5～16 周**；渐进式', 'teal'),
    ('box', '哪种更好', '**渐进式力量训练 > 有氧运动 > 无监督家庭锻炼**\n渐进方案下，8 周内高速和低速抗阻效果无显著差异', 'accent'),
    ('box', '水中运动', '被推荐：改善运动能力、肌力、功能和疼痛', 'navy'),
    ('box', '患者教育（B 级，未变）', '和运动/手法结合：活动与运动指导、体重管理、关节减负\n线上疼痛自我管理可能短期有用，长期额外获益不稳定', 'yellow')])
deck.text('⑥ 体重管理：C → B，变成核心干预', '证据 III → I', [
    ('box', '推荐', '肥胖患者：**减重约 5.0%～7.5% + 运动**（B 级）\n能改善疼痛、减缓进展、增加关节活动能力', 'teal'),
    ('box', '跨学科分工', '骨科/康复医师：评估、筛查合并症\n**物理治疗师：疼痛、功能和运动处方**\n营养师：饮食与体重　必要时内科医师控制代谢风险', 'navy'),
    ('box', '难点', '疼痛 → 少动 → 体重增加的恶性循环\n优先：关节减负教育、**低冲击或水中运动**、分级渐进、必要时助行', 'accent')])
deck.text('⑦ 干针新增 A 级，超声降到 D 级', '原文 4.4、4.5', [
    ('box', '干针（新增，A 级）', '针对**髂腰肌、股直肌、阔筋膜张肌、臀中肌、臀小肌**的肌筋膜触发点\n3 项 RCT：短期（3 周）改善肌肉疼痛、功能和肌力，**K-L 2/3 级**更明显\n但样本小，警惕小样本效应和发表偏倚', 'teal'),
    ('box', '超声（B → D）', '新 RCT（71 例）：在常规理疗基础上加各种超声 vs 假超声，2 周、14 周均无差异\n→ 可在**共同决策**下作为可选加用，要告知疗效不确定、权衡时间和费用', 'accent'),
    ('box', '解读作者的不同看法', '新试验是在运动等强干预之上比“附加效应”，参数也不同（3 MHz、1.5 W/cm2 vs 2017 证据的 1 MHz、1 W/cm2＋热疗）\n更应理解为疗效**依赖参数和情境**，不宜过早否定', 'yellow'),
    ('box', '其余不变', '功能/步态/平衡训练 **C 级**；氨基葡萄糖、软骨素、透明质酸注射证据不足；NSAIDs 个体化权衡', 'grey')])
deck.figure('⑧ 临床路径：分层 + 共同决策', '原文图 1（原图未改动）', F('x69'), None, [
    ('bul', ['人人都做：**患者教育（B）+ 个体化运动（A）**', '再按分层加：活动受限、疼痛明显 → 手法（A）；K-L 2/3 级 + 触发点 → 干针（A）；超重肥胖 → 减重（B）；步态平衡问题 → 功能训练（C）',
             '超声、支具等仅在运动或手法无效时共同决策', '无效或与分类不符 → 回到诊断和转诊'])])
deck.text('⑨ 落到我国临床', '解读作者的建议', [
    ('box', '老年人多、共病多', '合并**骨质疏松**：抗阻不套常规强度，以低负荷、渐进为主，加脊柱保护、平衡和防跌倒\n合并**腰椎退变**：减少腰部负担动作，强化髋周稳定和步态训练', 'teal'),
    ('box', '简化成居家方案', '把运动方案简化为低门槛、易坚持的核心动作，配合家庭随访、阶段复评', 'navy'),
    ('box', '中医外治', '接受度高，但髋骨关节炎领域高质量证据不足，适合放在整合康复框架下发展', 'grey')])
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('A', '手法（MWM、长轴牵引）· 个体化运动 · 干针（K-L 2/3 级）'), ('B', '患者教育 · 减重 5%～7.5% + 运动'), ('C', '功能 / 步态 / 平衡训练'), ('D', '超声（共同决策下可选）'),
               ('评估', '1 项自评 + 1 项功能测试 + NPRS，基线 + 至少 1 次随访')]),
    ('h', '原文对不上的地方'),
    ('bul', ['运动频率：4.2 节开头写每周 **1～3 次**，同节后文和表 2 写 **1～5 次**']),
    ('box', '文献 · 版权', '石明鹏, 周国徽, 张宪帅, 等.《髋痛与活动受限——髋骨关节炎物理治疗临床实践指南(2025版)》更新解读. 中国中医骨伤科杂志, 2026, 34(10): 1-7. DOI: 10.20085/j.cnki.issn1005-0205.261001\n原文非开放许可，图 1 为原图未修改。**仅供学习交流，如有侵权请联系删除**', 'grey')])
deck.save(OUT)
