#!/usr/bin/env python3
"""Nangliya 等 2024 严重压砸伤致 Lisfranc 骨折的多学科处理与康复 1 例：中文标题卡、背景卡、病例卡、原文图 1～4 配中文图注，
用药卡、六期康复方案卡（原文表 4）、结局量表变化图（据原文表 5 重画）、解读卡、封面。
共用工具在 ../bridge-review-1/tools/bridgekit.py。用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('病例报告 · 《Cureus》2024', ['足部严重压砸伤致 Lisfranc 骨折', '多学科处理和分期康复'],
               'Nangliya R, Nandanwar SP, Deshpande M.', 'Cureus. 2024;16(2):e54473. doi:10.7759/cureus.54473',
               '印度 Datta Meghe 高等教育研究院 Ravi Nair 物理治疗学院肌骨物理治疗科'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
def pair(a, b, name, H=900):
    ims = [Image.open(f'{WORK}/{x}.jpg').convert('RGB') for x in (a, b)]
    ims = [i.resize((round(i.width * H / i.height), H), Image.LANCZOS) for i in ims]
    c = Image.new('RGB', (ims[0].width + ims[1].width + 12, H), 'white'); c.paste(ims[0], (0, 0)); c.paste(ims[1], (ims[0].width + 12, 0))
    c.save(f'{WORK}/{name}.jpg', quality=93); return name + '.jpg'
card('Lisfranc 损伤是什么（编者根据原文整理）', [
    ('定义', '跖跗关节（Lisfranc 关节）骨折脱位：一块或多块跖骨与跗骨分离，关键是内侧楔骨与第 2 跖骨底之间的连接被破坏', LT, TEAL),
    ('表现', '中足肿胀、疼痛、沉重感；不稳定损伤发生率约 6/10 万人年', OR, (200, 120, 0)),
    ('别漏诊', '漏诊、延误诊断与长期残疾相关', PK, RED),
    ('治疗', '轻度扭伤无分离：石膏或靴子制动\n严重骨折脱位：克氏针、螺钉等手术固定，术后系统物理治疗', GR, (0, 120, 60)),
])
card('病例：58 岁男性，被公交车撞伤左足（原文）', [
    ('伤情', '左足 20 cm 污染撕裂伤口、骨和组织外露；中足背侧、足底压痛，可触及骨擦感；足背动脉、胫后动脉可触及', LT, TEAL),
    ('诊断', '左足压砸伤；Lisfranc 骨折；全部楔骨和骰骨骨折；足跟脂肪垫撕脱', PK, RED),
    ('手术', '伤口清创＋克氏针固定', OR, (200, 120, 0)),
    ('术后评估', '疼痛 8/10；左膝屈曲只有 0°～20°，左膝屈伸肌力 2/5，左踝活动度和肌力无法评估\n站立、行走、如厕都有困难', PU, C_NAV),
])
put(pair('x49', 'x59', 'xr'), '原文图 1、2  左足 X 线：左为术前，Lisfranc 骨折伴全部楔骨和骰骨骨折；右为术后，楔骨、骰骨克氏针固定，另有一根横向克氏针稳定中足')
card('用药（原文表 3）', [
    ('布洛芬 400 mg', '每日 2 次', LT, TEAL),
    ('维生素 C 500 mg', '每日 2 次', OR, (200, 120, 0)),
    ('胰蛋白酶＋糜蛋白酶片', '每日 3 次', GR, (0, 120, 60)),
])
card('康复方案（一）：第 1～10 周（原文表 4）', [
    ('Ⅰ期 第 1～2 周：休息、消肿', '不负重；学会安全使用拐杖或滚轮拐杖；家属和患者宣教（手术、解剖、愈合时间）\n髋主动活动，戴夹板下膝主动活动', LT, TEAL),
    ('Ⅱ期 第 3～6 周：保护融合部位', '行走靴或玻璃纤维石膏保护；抬高消肿；腹肌激活（够球、桥式）；直腿抬高、髋膝主动活动\n第 6～8 周视医生评估开始踝屈伸、内外翻主动活动；拉伸臀大肌、梨状肌、股直肌、腘绳肌', OR, (200, 120, 0)),
    ('Ⅲ期 第 6～10 周：行走靴下完全负重', '固定自行车；徒手抗阻和 0.5 kg 沙袋练核心、髋、膝；行走靴下逐步完全负重', GR, (0, 120, 60)),
    ('剂量', '每个动作 10 次×2 组，逐步加到 10 次×4 组', PU, C_NAV),
])
card('康复方案（二）：第 11 周以后（原文表 4）', [
    ('Ⅳ期 第 11～12 周：脱靴完全负重', '按摩消肿；踝背伸、跖屈、内外翻主动活动；必要时刺激内外翻肌开始步态再训练\n进阶到站立腿举；视医生评估逐渐脱离行走靴', LT, TEAL),
    ('Ⅴ期 第 13～15 周：活动度和步态', '非融合关节和踝主被动活动；拉伸臀肌、梨状肌、腘绳肌、小腿、股直肌；踝足趾非融合关节手法松动\n弹力带练踝、负重内外翻、提踵；本体感觉：平衡板单腿站、平地单腿站，可配踝护具', OR, (200, 120, 0)),
    ('Ⅵ期 第 16 周：恢复工作能力', '继续第 15 周的力量和本体感觉训练；必要时配矫形鞋垫或改鞋继续步态训练', GR, (0, 120, 60)),
])
put('x85.jpg', '原文图 3  原文图注为“骨盆桥式”，用于增强下背部和髋部伸肌力量')
put('x94.jpg', '原文图 4  左侧动态股四头肌练习，用于增强股四头肌力量')
fig, axs = plt.subplots(1, 2, figsize=(12, 6.4), dpi=100, gridspec_kw={'width_ratios': [1, 1.6]})
ax = axs[0]; labs = ['下肢功能量表\nLEFS（满分 80）', 'Olerud-Molander\n踝评分（满分 100）']; pre = [26, 10]; post = [58, 75]
for i, (a, b2) in enumerate(zip(pre, post)):
    ax.bar(i - .18, a, .36, color='#9AA5B1'); ax.bar(i + .18, b2, .36, color='#2E86AB')
    ax.text(i - .18, a + 1.5, str(a), ha='center', fontsize=17); ax.text(i + .18, b2 + 1.5, str(b2), ha='center', fontsize=17)
ax.set_xticks(range(2), labs, fontsize=13); ax.set_ylim(0, 90); ax.set_title('功能（越高越好）', fontsize=18); ax.spines[['top', 'right']].set_visible(False)
ax = axs[1]; it = ['焦虑', '抑郁', '疲劳', '睡眠障碍', '疼痛干扰', '疼痛强度\n（0～10）']; pre2 = [12, 12, 16, 4, 12, 8]; post2 = [0, 0, 3, 0, 3, 1]
xs = range(len(it))
ax.bar([i - .18 for i in xs], pre2, .36, color='#9AA5B1', label='康复前（第 3 天）'); ax.bar([i + .18 for i in xs], post2, .36, color='#C0392B', label='康复后（第 8～12 周）')
for i in xs: ax.text(i - .18, pre2[i] + .3, str(pre2[i]), ha='center', fontsize=14); ax.text(i + .18, post2[i] + .3, str(post2[i]), ha='center', fontsize=14)
ax.set_xticks(list(xs), it, fontsize=13); ax.set_ylim(0, 19); ax.set_title('PROMIS-29 部分维度（越低越好）', fontsize=18); ax.legend(frameon=False, fontsize=13, loc='upper right'); ax.spines[['top', 'right']].set_visible(False)
fig.suptitle('结局量表：康复前后', fontsize=21)
fig.text(.5, .015, 'PROMIS-29 身体功能 8/20 → 16/20（越高越好），活动能力维度 16/20 → 5/20（原文未说明方向）', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, .94)); fig.savefig(f'{WORK}/outcome.png', facecolor='white'); plt.close(fig)
put('outcome.png', '据原文表 5 重画：下肢功能量表 26 → 58 分，Olerud-Molander 踝评分 10 → 75 分；焦虑、抑郁从 12 分降到 0 分')
card('这个病例能说明什么（编者解读）', [
    ('可以借鉴的', '按周分六期：先保护融合部位、练髋膝和核心，再逐步负重、恢复踝活动和步态，最后本体感觉和重返工作\n未受伤的关节和健侧肌力一开始就练', GR, (0, 120, 60)),
    ('结果要客观看', '左膝屈曲 20° → 100°、左踝背伸 5° → 15°、跖屈 10° → 40°；左下肢肌力到 4/5\n功能评分明显提高，但随访时间短，没有长期结果', OR, (200, 120, 0)),
    ('证据很弱', '单个病例；方案像是通用模板（提到“移植物”“融合关节”，而本例只做了克氏针固定）\n各项评估的时间点前后不一，原文提到的电疗、针灸、蜡疗、贴扎在方案里没有具体写', PK, RED),
])
c = k.op('x94.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = 300
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
