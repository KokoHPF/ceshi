#!/usr/bin/env python3
"""《2025年美国骨科医师学会(AAOS)急性骨筋膜室综合征临床实践指南解读》（中国修复重建外科杂志 2026）→ 小红书 3:4 图文卡片。
原文未标开放许可；原文无临床配图，推荐强度分布图为编者据原文绘制；卡片注明“仅供学习交流，如有侵权请联系删除”。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from io import BytesIO
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='创伤骨科', source='中国修复重建外科杂志 2026;40(9):1346-1350', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()


def strength_fig(w=9.6, h=5.0):
    """15 条推荐/共识按强度分布（编者据原文绘制）"""
    cols = [('中等证据推荐 · 3 条', ['股静脉乳酸（急性肢体缺血）', '筋膜室压力监测是重要客观方法', '重复/持续监测，ΔP>30 mmHg 辅助排除'], '#1F5F8B'),
            ('有限证据推荐 · 5 条', ['肌红蛋白尿、肌钙蛋白可能有帮助', '电击伤不用肌红蛋白尿判断', '清醒者连续体格检查', '合并骨折早期固定（新升级）', '筋膜切开后负压伤口治疗'], '#E3A21A'),
            ('专家共识 · 7 条', ['晚期/漏诊不靠血清标志物', '已不可逆损伤，测压意义有限', '昏迷镇静者重复/持续测压', '无其他可靠影像或化验', '椎管内麻醉可能掩盖疼痛', '充分减压比术式更重要', '不可逆损伤成人不做筋膜切开'], '#9AA5B1')]
    fig, ax = plt.subplots(figsize=(w, h), dpi=100); ax.set_xlim(0, 3); ax.set_ylim(0, 8.6); ax.axis('off')
    for j, (t, items, c) in enumerate(cols):
        x = .03 + j * 1.0
        ax.add_patch(FancyBboxPatch((x, 7.4), .94, .95, boxstyle='round,pad=0.01,rounding_size=0.05', fc=c, ec='none'))
        ax.text(x + .47, 7.87, t, ha='center', va='center', fontsize=15, color='white', weight='bold')
        for i, s in enumerate(items):
            y = 6.75 - i * .98
            ax.add_patch(FancyBboxPatch((x, y - .4), .94, .8, boxstyle='round,pad=0.01,rounding_size=0.04', fc='#F4F6F8', ec='none'))
            ax.text(x + .47, y, s, ha='center', va='center', fontsize=11.2, color='#222')
    fig.tight_layout(pad=.2); return fig


def count_fig(w=9.6, h=5.4):
    """推荐强度计数（编者据原文绘制）"""
    fig, ax = plt.subplots(figsize=(w, h), dpi=100); ax.set_xlim(-.12, 3.12); ax.set_ylim(0, 3.2); ax.axis('off')
    for j, (n, t, sub, c) in enumerate([('0', '强推荐', '本版没有', '#C9CED4'), ('3', '中等证据推荐', '压力监测 · 股静脉乳酸', '#1F5F8B'),
                                         ('5', '有限证据推荐', '含新升级：骨折早期固定', '#E3A21A'), ('7', '专家共识', '无证据支持时的建议', '#9AA5B1')][1:]):
        x = .05 + j * 1.0
        ax.add_patch(FancyBboxPatch((x, .25), .9, 2.45, boxstyle='round,pad=0.01,rounding_size=0.08', fc=c, ec='none'))
        ax.text(x + .45, 1.85, n, ha='center', va='center', fontsize=64, color='white', weight='bold')
        ax.text(x + .45, 1.05, t, ha='center', va='center', fontsize=19, color='white', weight='bold')
        ax.text(x + .45, .58, sub, ha='center', va='center', fontsize=12.5, color='white')
    fig.tight_layout(pad=.2); return fig


def fig2img(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['急性骨筋膜室', '综合征', 'AAOS 指南 2025'], kicker='中文解读 · 中国修复重建外科杂志',
           subtitle='8 条推荐 + 7 条专家共识，没有一条“强推荐”', photos=[(fig2img(count_fig()), '15 条意见的证据强度')], banner='一旦确诊，尽早筋膜切开减压')
deck.text('ACS 是什么', '原文引言', [
    ('box', '机制', '骨筋膜室内压力急剧升高，**超过毛细血管灌注压** → 组织灌注不足 → 肌肉、神经缺血坏死', 'teal'),
    ('box', '后果', '**数小时内**即可不可逆：严重功能障碍、**Volkmann 缺血性挛缩**甚至截肢；还可继发横纹肌溶解、急性肾损伤\n是典型的**时间敏感型**急症，预后取决于早识别、早减压', 'accent'),
    ('box', '常见于', '四肢创伤后，尤其**胫骨骨折**、高能量损伤、挤压伤、血管修复或再灌注后\n非创伤因素：**石膏或绷带过紧**、长时间肢体受压、严重烧伤、抗凝相关出血', 'yellow'),
    ('box', '难在哪', '早期表现不特异；意识障碍、镇静或机械通气的患者更难判断', 'grey')])
deck.text('这次更新了什么', '原文 1：更新背景与方法学', [
    ('box', '快速更新', '2018 版已满 5 年，但新证据不足以改动指南框架 → 只更新**推荐意见部分**；方法学、PICO、适用范围均沿用 2018 版\n新增纳入研究 **13 篇**', 'navy'),
    ('box', '唯一升级', '合并骨折者对长骨骨折**早期固定**：由“专家共识”升为“**有限推荐**”', 'accent'),
    ('h', '推荐强度怎么读（原文表 1）'),
    ('steps', [('强', '≥2 项高质量研究结论一致（本版没有）'), ('中等', '≥2 项中等质量一致，或 1 项高质量'), ('有限', '≥2 项低质量一致，或 1 项中等质量，或证据冲突'), ('共识', '无证据，由工作组按临床观点提出')])])
deck.text('诊断①：生物标志物要谨慎', '原文 2.1.1', [
    ('box', '肌红蛋白尿、血清肌钙蛋白（有限）', '可能有助于**创伤性下肢损伤**的 ACS 诊断\n肌红蛋白尿不足以作可靠指标；肌钙蛋白升高有提示意义，但**正常不能排除**', 'yellow'),
    ('box', '股静脉乳酸（中等）', '**急性肢体缺血**患者：血运重建前后股静脉乳酸变化与 ACS 密切相关\n仅适用于非创伤性股动脉栓塞所致急性下肢缺血', 'teal'),
    ('box', '电击伤（有限）', '高压电击伤中肌红蛋白尿与筋膜切开相关性弱 → **不建议**作为诊断依据', 'accent'),
    ('box', '晚期或漏诊（专家共识）', '血清生物标志物**不应**作为是否做筋膜切开的主要依据', 'grey')])
deck.text('诊断②：筋膜室压力监测', '原文 2.1.2', [
    ('box', '重要客观方法（中等）', '依据 2 项中等、3 项低质量研究；但各研究诊断标准、监测方式、切开阈值差异大', 'teal'),
    ('box', 'ΔP = 舒张压 − 筋膜室压', '采用**重复或持续**监测，**ΔP >30 mmHg** 作为参考阈值，用来**辅助排除** ACS（中等）\n但另有研究发现该阈值特异性低，单靠 ΔP 可能导致**不必要的筋膜切开**', 'navy'),
    ('box', '没有单一金标准', '目前缺乏证据支持用某个绝对压力值或 ΔP 作为确诊标准 → **临床评估 + 客观监测**结合', 'yellow'),
    ('box', '已不可逆（专家共识）', '晚期或漏诊、已有明确不可逆神经肌肉或血管损伤时，测压对决策价值有限', 'grey')])
deck.text('诊断③：体检、昏迷、麻醉', '原文 2.1.3～2.1.5', [
    ('box', '清醒患者：连续体格检查（有限）', '疼痛、苍白、脉搏、肿胀等与因疑似 ACS 行筋膜切开中度相关\n有参考价值，但**敏感性低于压力监测**', 'teal'),
    ('box', '昏迷或深度镇静（专家共识）', '无法可靠查体 → **重复或持续测压**，直至确诊或排除', 'navy'),
    ('box', '其他检查（专家共识）', '除查体和测压外，目前**没有**影像或化验能可靠决定是否切开', 'grey'),
    ('box', '椎管内麻醉（专家共识）', '可能**掩盖或延迟**典型疼痛，增加诊断难度；但能减少阿片用量\n→ 高危患者用此麻醉时，要加强查体和必要的测压', 'accent')])
deck.text('手术：怎么切、什么时候不切', '原文 2.2.1（均为专家共识）', [
    ('box', '充分减压 > 术式', '单切口还是双切口、切口位置都不如**每个筋膜室彻底减压**重要\n经验不足者建议**双切口**；但近期研究提示双切口要更注意手术部位感染', 'teal'),
    ('box', '已不可逆损伤的成人', '**不宜**再做筋膜切开；如需固定骨折，选**外固定或石膏**等不侵犯筋膜室的方式', 'accent'),
    ('box', '晚期 ACS', '切开可能带来再灌注损伤、广泛清创和感染等额外风险', 'yellow')])
deck.text('合并骨折 + 伤口管理', '原文 2.2.2、2.2.3（有限推荐）', [
    ('box', '合并骨折：早期固定（本版升级）', '需切开减压的 ACS 合并长骨骨折，**早期稳定固定**（外固定或内固定）可行\n3 项研究：在切开伤口关闭时或之前内固定可能感染更低；2 项未见差异\n证据质量低 → 按软组织、骨折类型、感染风险个体化', 'teal'),
    ('box', '伤口：负压伤口治疗（NPWT）', '可能**缩短伤口闭合时间、减少植皮**；对感染的影响证据不足', 'navy'),
    ('box', '皮肤牵张', '钢丝辅助牵张比缝线牵张可能增加感染\n地震伤小样本研究：皮肤牵张比 NPWT 植皮更少，闭合时间和感染率无差异 → 仍有争议', 'grey')])
deck.rows('AAOS 2025 vs 中国指南 2020', '原文 3：与中国 ACS 指南比较', [
    ('压力监测', '中国：可疑高危者测压，ΔP ≤30 mmHg 作为重要诊断参考；AAOS：重复/持续监测，ΔP >30 辅助排除', '都重视，中国偏“诊断”，AAOS 偏“排除”', 'teal'),
    ('生物标志物', '中国：乳酸、肌钙蛋白、肌红蛋白尿等有提示意义；AAOS：只认肌红蛋白尿、肌钙蛋白、特定情境股静脉乳酸', 'AAOS 更审慎，晚期 ACS 不据此决策', 'yellow'),
    ('治疗', '都强调确诊后尽早切开减压；AAOS 明确不可逆损伤的成人不再切开', 'AAOS 对晚期 ACS 限制更明确', 'accent'),
    ('覆盖面', '中国指南含儿童、高危筛查、减压时机、各部位切开方式；AAOS 方法学更透明、条目化', '中国更全面，AAOS 更规范', 'navy'),
], note='解读作者结论：多数推荐仍基于有限证据或专家共识，ACS 领域高质量 RCT 不足')
deck.text('收藏：ACS 关键点', '据原文整理', [
    ('steps', [('认', '胫骨骨折、挤压伤、再灌注后、石膏过紧 → 警惕'), ('查', '清醒者连续查体；昏迷镇静者重复/持续测压'), ('ΔP', '>30 mmHg 辅助排除，但别单凭它决定'),
               ('切', '确诊尽早切开，充分减压；不可逆损伤的成人不再切开'), ('后', '可早期固定骨折；伤口可用负压治疗')]),
    ('box', '编者提醒（康复科）', '骨折术后、石膏或支具固定的患者，出现与损伤不相称的剧痛、肿胀、皮肤苍白等，应及时报告医生，不要当成普通术后痛继续训练', 'accent'),
    ('box', '文献 · 版权', '叶艺, 卢冰, 肖成伟, 等. 2025 年美国骨科医师学会(AAOS)急性骨筋膜室综合征临床实践指南解读. 中国修复重建外科杂志, 2026, 40(9): 1346-1350. DOI: 10.7507/1002-1892.202603087\n本卡为编者整理。**仅供学习交流，如有侵权请联系删除**', 'grey')])
deck.save(OUT)
