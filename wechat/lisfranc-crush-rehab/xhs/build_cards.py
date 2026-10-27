#!/usr/bin/env python3
"""Nangliya 等 2024 压砸伤致 Lisfranc 骨折多学科处理与康复 1 例 → 小红书 3:4 图文卡片。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='足踝康复', source='Nangliya 等 Cureus 2024;16(2):e54473', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
X = lambda n: Image.open(f'{WORK}/x{n}.jpg').convert('RGB')

deck.cover(['严重压砸伤致', 'Lisfranc 骨折的', '多学科处理与康复：1 例报告'], kicker='Cureus 2024 · 病例报告',
           subtitle='克氏针固定后，六期康复方案',
           photos=[(X(59), '术后 X 线'), (X(94), '股四头肌练习'), (X(85), '床上训练')], banner='六期方案 + 量表前后对比')
deck.text('Lisfranc 损伤是什么', '原文引言', [
    ('box', '定义', '**跖跗关节**骨折脱位：一块或多块跖骨与跗骨分离；关键是**内侧楔骨与第 2 跖骨底**之间的连接被破坏', 'teal'),
    ('box', '表现', '中足**肿胀、疼痛、沉重感**；不稳定损伤约 **6/10 万**人年', 'yellow'),
    ('box', '别漏诊', '漏诊、延误诊断与**长期残疾**相关', 'accent'),
    ('box', '治疗', '轻度扭伤无分离 → 石膏或靴子制动\n严重骨折脱位 → **手术固定** + 系统物理治疗', 'navy')])
deck.text('病例：58 岁男性，被公交车撞伤左足', '原文', [
    ('box', '伤情', '左足 **20 cm** 污染撕裂伤口，骨和组织外露；中足压痛、骨擦感', 'teal'),
    ('box', '诊断', '**Lisfranc 骨折** + 全部楔骨和骰骨骨折 + **足跟脂肪垫撕脱**', 'accent'),
    ('box', '手术', '伤口清创 + **克氏针**固定', 'yellow'),
    ('box', '术后', '疼痛 **8/10**；左膝屈曲仅 **0°～20°**、肌力 2/5；站立、行走、如厕都困难', 'navy')])
deck.figure('X 线：术前和术后', '原文图 1（左）、图 2（右）', [X(49), X(59)], ['术前', '术后'], [
    ('bul', ['术前：Lisfranc 骨折，**全部楔骨和骰骨**骨折', '术后：楔骨、骰骨**克氏针**固定，另一根**横向克氏针**稳定中足']),
    ('box', '用药（原文表 3）', '布洛芬 400 mg 每日 2 次；维生素 C 500 mg 每日 2 次；胰蛋白酶 + 糜蛋白酶片每日 3 次', 'grey')])
deck.text('Ⅰ～Ⅱ期：第 1～6 周', '原文表 4', [
    ('box', 'Ⅰ期 第 1～2 周：休息、消肿', '**不负重**；学会用拐杖或滚轮拐杖；宣教手术、解剖和愈合时间\n髋主动活动；戴夹板下膝主动活动', 'teal'),
    ('box', 'Ⅱ期 第 3～6 周：保护融合部位', '行走靴或玻璃纤维石膏；**抬高**消肿\n腹肌激活（够球、**桥式**）；**直腿抬高**；髋膝主动活动', 'yellow'),
    ('box', '第 6～8 周', '视医生评估，开始**踝屈伸、内外翻**主动活动；拉伸臀大肌、梨状肌、股直肌、腘绳肌', 'accent')])
deck.text('Ⅲ～Ⅳ期：第 6～12 周', '原文表 4', [
    ('box', 'Ⅲ期 第 6～10 周：行走靴下完全负重', '固定自行车；徒手抗阻和 **0.5 kg** 沙袋练核心、髋、膝\n行走靴下逐步**完全负重**', 'teal'),
    ('box', 'Ⅳ期 第 11～12 周：脱靴完全负重', '按摩消肿；踝背伸、跖屈、内外翻**主动活动**\n必要时刺激内外翻肌开始**步态再训练**；进阶到站立腿举', 'yellow'),
    ('box', '剂量', '每个动作 **10 次 × 2 组**，逐步加到 **10 次 × 4 组**', 'grey')])
deck.text('Ⅴ～Ⅵ期：第 13 周以后', '原文表 4', [
    ('box', 'Ⅴ期 第 13～15 周：活动度和步态', '非融合关节和踝主被动活动；拉伸臀肌、梨状肌、腘绳肌、小腿、股直肌\n踝足趾非融合关节**手法松动**', 'teal'),
    ('box', '力量和本体感觉', '弹力带练踝、负重内外翻、**提踵**\n**平衡板单腿站** → 平地单腿站；可配踝护具', 'yellow'),
    ('box', 'Ⅵ期 第 16 周：恢复工作能力', '继续力量和本体感觉训练；必要时配**矫形鞋垫**或改鞋', 'accent')])
deck.figure('床上训练', '原文图 3（原文图注为“骨盆桥式”）', X(85), None, [
    ('bul', ['原文说明：增强**下背部和髋部伸肌**力量', '属于Ⅱ期的腹肌激活和桥式练习']),
    ('box', '同期还练', '**直腿抬高**、髋膝主动活动；患足不负重', 'teal')])
deck.figure('动态股四头肌练习', '原文图 4', X(94), None, [
    ('bul', ['坐位伸膝，增强**股四头肌**力量', '患足在支具保护下进行']),
    ('box', '为什么重要', '术后左膝屈曲只有 **0°～20°**、屈伸肌力 **2/5**，膝是这例患者的主要受限之一', 'yellow')])
fig, ax = plt.subplots(figsize=(9.6, 6))
labs = ['LEFS\n(满分 80)', '踝评分\n(满分 100)', '焦虑', '抑郁', '疲劳', '疼痛\n(0～10)']; pre = [26, 10, 12, 12, 16, 8]; post = [58, 75, 0, 0, 3, 1]
xs = range(6); ax.bar([i - .2 for i in xs], pre, .4, color='#9AA5B1', label='康复前'); ax.bar([i + .2 for i in xs], post, .4, color='#2E86AB', label='康复后')
for i in xs: ax.text(i - .2, pre[i] + 1, str(pre[i]), ha='center', fontsize=17); ax.text(i + .2, post[i] + 1, str(post[i]), ha='center', fontsize=17)
ax.axvline(1.5, color='#ccc', lw=1); ax.text(.5, 86, '越高越好', ha='center', fontsize=17, color='#2E86AB'); ax.text(3.5, 86, '越低越好', ha='center', fontsize=17, color='#C0392B')
ax.set_xticks(list(xs), labs, fontsize=15); ax.set_ylim(0, 92); ax.tick_params(axis='y', labelsize=14); ax.legend(frameon=False, fontsize=16, loc='center right')
ax.spines[['top', 'right']].set_visible(False); fig.tight_layout()
deck.chart('结果：量表前后对比', '据原文表 5 重画；焦虑、抑郁、疲劳为 PROMIS-29 维度', fig, [
    ('bul', ['下肢功能量表 **26 → 58**；Olerud-Molander 踝评分 **10 → 75**', '疼痛 **8 → 1**；焦虑、抑郁 **12 → 0**']),
    ('box', 'PROMIS-29 其他维度', '身体功能 **8 → 16**/20；疲劳 16 → 3；睡眠障碍 4 → 0；疼痛干扰 12 → 3', 'teal'),
    ('box', '注意时间', '康复前为**第 3 天**，康复后为**第 8～12 周**', 'grey')])
deck.text('活动度和肌力（左侧）', '原文表 6、7', [
    ('box', '活动度', '膝屈曲 **20° → 100°**；踝背伸 **5° → 15°**；踝跖屈 **10° → 40°**；髋屈曲 105° → 115°', 'teal'),
    ('box', '肌力', '膝屈伸、踝背伸跖屈 **2/5 → 4/5**；髋各组 **3/5 → 5/5**', 'yellow'),
    ('box', '健侧也弱', '右侧（未受伤）髋膝踝肌力康复前也只有 **3/5**，康复后 5/5；原文未解释原因', 'accent')])
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '证据很弱'),
    ('bul', ['**单个病例**，没有对照，随访短', '方案提到“移植物”“融合关节”，像**通用模板**，和克氏针固定不完全对应']),
    ('h', '原文对不上'),
    ('steps', [('1', '评估时间点前后不一：表 5、6、7 分别写**第 8～12 周、第 3 周、第 5 周**'), ('2', '表 1、2 说左踝**无法评估**，表 6、7 康复前却有具体数值'), ('3', '摘要写“乘用车事故”，正文写**被公交车撞伤**')])])
deck.text('收藏：Lisfranc 骨折术后六期康复', '先保护、再负重、后功能', [
    ('steps', [('1～2周', '不负重，拐杖；髋膝主动活动'), ('3～6周', '行走靴；桥式、直腿抬高；6～8 周视评估开始踝主动活动'),
               ('6～10周', '行走靴下完全负重；核心髋膝抗阻'), ('11～12周', '脱靴；踝主动活动；步态再训练'),
               ('13～15周', '手法松动；提踵；平衡板单腿站'), ('16周', '恢复工作能力；必要时矫形鞋垫')]),
    ('box', '文献', 'Nangliya R, et al. Multidisciplinary Management and Rehabilitation of Severe Crush Injury Resulting in Lisfranc Fracture: A Case Report. Cureus. 2024;16(2):e54473', 'navy'),
    ('box', '版权', '原文 **CC BY 4.0** 开放获取', 'teal')])
deck.save(OUT)
