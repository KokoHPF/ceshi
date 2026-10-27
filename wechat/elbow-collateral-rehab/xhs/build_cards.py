#!/usr/bin/env python3
"""Kim 等 2020 肘关节内外侧副韧带术后早期康复 3 例 → 小红书 3:4 图文卡片。
原文图 1、2 按空白列切成单幅；结果图用中文重画（数据来自原文图 3、表 3）。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='肘关节康复', source='Kim 等 IJERPH 2020;17(17):6133', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
f1 = Image.open(f'{WORK}/x190.jpg').convert('RGB'); f2 = Image.open(f'{WORK}/x240.jpg').convert('RGB')
xray, prom, band = (f1.crop((a, 0, b, f1.height)) for a, b in ((0, 393), (400, 798), (837, f1.width)))
flexi, wall, bosu = (f2.crop((a, 0, b, f2.height)) for a, b in ((0, 287), (297, 573), (588, f2.width)))
cols = {'A': '#2E86AB', 'B': '#E8A200', 'C': '#C0392B'}

# 1 封面
deck.cover(['肘关节内外侧副韧带', '手术修复后的早期康复：', '3 例报告'], kicker='IJERPH 2020 · 病例报告',
           subtitle='术后第 7 天开始动，随访 2 年',
           photos=[(prom, '第 7 天被动活动'), (band, '6 周弹力带'), (bosu, '3 个月神经肌肉训练')], banner='五期方案 + 恢复时间线')
# 2 背景
deck.text('为什么关注“内外侧一起伤”', '原文引言', [
    ('bul', ['肘韧带研究大多针对**投掷运动员的内侧副韧带**，康复方案也多为他们设计',
             '**外侧副韧带损伤、内外侧复合损伤**多由跌倒、脱位等外伤引起，较少见，康复报告更少']),
    ('box', '手术 vs 保守（原文引用）', '保守治疗后只有 **42%** 成功回归；手术后 **83%** 在 1 年内回到运动', 'teal'),
    ('box', '作者的假设', '术后**早期**开始康复是安全的，并能有效恢复活动度和肌力、回到日常生活', 'yellow'),
    ('box', '早动的理由', '术后僵硬至少发生在 **5%** 的患者中，会导致疼痛、影响功能恢复', 'accent')])
# 3 患者
deck.text('三位患者', '原文表 1', [
    ('box', 'A：39 岁女性 · 业余游泳', '摔倒手撑地，右肘完全脱位，复位后 4 天再脱位；内侧部分撕裂、外侧和伸肌总腱完全撕裂\n→ **开放修复外侧副韧带 · 6 个月回游泳**', 'teal'),
    ('box', 'B：60 岁女性 · 业余羽毛球', '无外伤，肘痛 2 年，内外侧副韧带明显退变；保守 6 个月仍加重\n→ **关节镜下缝合内外侧韧带 · 8 个月回羽毛球**', 'coral'),
    ('box', 'C：17 岁男性 · 业余柔道', '比赛中过度扭转、过伸，未完全脱位；石膏 3 周 + 理疗 2 个月仍痛、无力\n→ **关节镜下用掌长肌腱重建内侧副韧带 · 4 个月回柔道**', 'purple'),
    ('bul', ['三人都在术后 **6 周**回到日常生活'])])
# 4 方案
deck.text('五期康复方案', '原文表 2', [
    ('box', '第 1 期 · 术后 7 天', '长臂支具戴 6 周；等长肌力、握力、肩胛骨松动\n→ **可耐受范围内被动屈伸**', 'teal'),
    ('box', '第 2 期 · 术后 3 周', '继续第 1 期\n→ **加被动旋前、旋后**', 'navy'),
    ('box', '第 3 期 · 术后 6 周', '由最弱的带逐步换到最强，每天 2 次\n→ **弹力带做肘、腕屈伸**', 'yellow'),
    ('box', '第 4 期 · 术后 3 个月', '哑铃、器械（推胸、下拉）；弹力管旋前旋后\n→ **加站姿神经肌肉训练**', 'purple'),
    ('box', '第 5 期 · 术后 6 个月', 'BOSU、健身球跪姿俯卧撑；振动杆；药球接抛\n→ **强化肌力，强调离心**', 'coral'),
    ('bul', ['前 6 个月每周到中心 1～2 次，后 6 个月每月 1～2 次，其余在家练'])])
# 5 为什么这样排
deck.text('时间点是怎么定的', '原文讨论', [
    ('steps', [('7天', '遵循指南先**绝对制动 6 天**保护伤口，第 7 天开始被动屈伸'),
               ('3周', '旋前旋后会带来**内外翻应力**，复合损伤更怕，所以推迟'),
               ('6周', '肌腱、肌肉缝合处约 **6 周**才能稳定承受张力 → 开始屈伸抗阻'),
               ('3月', '旋转抗阻、神经肌肉训练；因为不是职业运动员，**以站姿为主**')]),
    ('box', '一开始就能做的', '肩胛骨练习、握力练习、肘**等长**收缩——不影响术区', 'teal')])
# 6 原文图 1
deck.figure('原文图 1：X 线和早期练习', '病例 A', [xray, prom, band], ['脱位 X 线', '被动活动', '弹力带'], [
    ('steps', [('a', '右肘**完全脱位**，没有骨折'), ('b', '戴长臂支具，在可耐受范围内**被动**活动，箭头示施力方向'),
               ('c', '术后 6 周起：站立位用**弹力带**做屈肘')]),
    ('box', '拉伸剂量', '每次 **10 秒 × 6 次**，每天至少 **6 轮**；配合自我按摩、热敷', 'yellow')])
# 7 原文图 2
deck.figure('原文图 2：神经肌肉训练', '术后 3 个月起', [flexi, wall, bosu], ['振动杆', '单手扶球推墙', 'BOSU 俯卧撑'], [
    ('steps', [('1', '先**站姿**扶健身球推墙，再**跪姿**健身球俯卧撑'),
               ('2', '难度：稳定的 **BOSU** → 大球 → 最小、最不稳的球'),
               ('3', '6 个月后加 **Flexi-bar 振动杆**、药球接抛')]),
    ('box', '目的', '提高关节稳定性和动态表现，降低再受伤风险', 'teal'),
    ('box', '为什么 3 个月才开始', '指南给运动员是 6～10 周开始增强式训练；本组**不是职业运动员**，作者有意放慢', 'yellow')])
# 8 ROM
t5 = ['6周', '3月', '6月', '12月', '24月']
rom = {'A': [75, 105, 130, 140, 145], 'B': [50, 90, 110, 135, 140], 'C': [70, 125, 135, 135, 135]}; hrom = {'A': 145, 'B': 145, 'C': 135}
fig, ax = plt.subplots(figsize=(9.6, 6.2))
for c, ys in rom.items():
    ax.plot(range(5), ys, marker='o', lw=3, ms=10, color=cols[c], label=f'病例 {c}（健侧 {hrom[c]}°）'); ax.axhline(hrom[c], color=cols[c], ls=':', lw=1.5)
ax.set_xticks(range(5), t5, fontsize=20); ax.tick_params(axis='y', labelsize=18); ax.set_ylim(40, 155); ax.set_ylabel('主动屈肘（°）', fontsize=20)
ax.legend(frameon=False, fontsize=18, loc='lower right'); ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); fig.tight_layout()
deck.chart('活动度：约 3 个月基本回来', '据原文图 3a 重画；点线为健侧', fig, [
    ('bul', ['6 周时只有 **50°～75°**', '病例 C（17 岁）**3 个月**就到 125°；病例 B（60 岁）最慢', '24 个月：A、C 与健侧相同，B 差 **5°**'])])
# 9 肌力
t4 = ['3月', '6月', '12月', '24月']
st = {'握力': ({'A': [12, 13, 25, 27], 'B': [10, 16, 23, 25], 'C': [22, 38, 48, 51]}, {'A': 28, 'B': 25, 'C': 52}),
      '屈肘': ({'A': [20, 30, 48, 53], 'B': [18, 21, 33, 48], 'C': [50, 72, 78, 80]}, {'A': 58, 'B': 50, 'C': 80}),
      '伸肘': ({'A': [18, 22, 35, 42], 'B': [15, 20, 30, 36], 'C': [32, 49, 52, 56]}, {'A': 46, 'B': 39, 'C': 57})}
fig, axs = plt.subplots(1, 3, figsize=(9.6, 6.2), sharey=True)
for ax, (nm, (d, h)) in zip(axs, st.items()):
    for c, ys in d.items(): ax.plot(range(4), [y / h[c] * 100 for y in ys], marker='o', lw=2.6, ms=8, color=cols[c], label=c)
    ax.axhline(100, color='#333', ls='--', lw=1); ax.axhline(90, color='#999', ls=':', lw=1)
    ax.set_xticks(range(4), t4, fontsize=15); ax.set_title(nm, fontsize=22); ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
axs[0].set_ylabel('占健侧（%）', fontsize=20); axs[0].set_ylim(20, 108); axs[0].tick_params(axis='y', labelsize=16); axs[0].legend(frameon=False, fontsize=16, loc='lower right')
fig.tight_layout()
deck.chart('肌力：6 个月还差得多', '据原文图 3 计算重画；等速肌力 3 个月起测', fig, [
    ('bul', ['6 个月时 A、B 握力只有 **13、16 kg**（健侧的 46%、64%）', '24 个月：三人握力、屈伸肌力都在健侧 **90% 以上**', '年轻男性恢复明显更快'])])
# 10 OES
oes = {'A': [7, 12, 22, 30, 44], 'B': [4, 9, 22, 34, 43], 'C': [10, 22, 30, 42, 46]}
fig, ax = plt.subplots(figsize=(9.6, 6.2))
for c, ys in oes.items(): ax.plot(range(5), ys, marker='o', lw=3, ms=10, color=cols[c], label=f'病例 {c}')
ax.axhline(48, color='#333', ls='--', lw=1); ax.text(0, 49.5, '满分 48', fontsize=18)
ax.set_xticks(range(5), t5, fontsize=20); ax.tick_params(axis='y', labelsize=18); ax.set_ylim(0, 53); ax.set_ylabel('Oxford 肘评分', fontsize=20)
ax.legend(frameon=False, fontsize=18, loc='lower right'); ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); fig.tight_layout()
deck.chart('能自理 ≠ 不受影响', '据原文表 3 重画；Oxford 肘评分越高越好', fig, [
    ('box', '6 周“回到日常生活”时', '评分只有 **4～10 分**；原文引用 40～50 岁无症状人群最低也有 12～16 分', 'accent'),
    ('bul', ['24 个月：**43～46 分**'])])
# 11 证据与对不上
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '证据很弱'),
    ('bul', ['只有 **3 例**、没有对照，只能说明“这样练没出事”', '年龄、性别、伤因、术式各不相同；大部分在家练，**练习频率没记录**']),
    ('h', '原文对不上'),
    ('steps', [('1', '讨论说 2 年活动度差约 10%，结论说完全恢复；按图 3 只有病例 B 差 5°'),
               ('2', '讨论说约 6 个月握力达日常所需（女性 18 kg），但 A、B 6 个月只有 13、16 kg'),
               ('3', '标题写“修复”，但病例 C 是**重建**，病例 A 只修了外侧')])])
# 12 收藏
deck.text('收藏：内外侧副韧带术后时间线', '前提：手术医生认可修复牢靠', [
    ('steps', [('7天', '被动屈伸 + 等长 + 握力 + 肩胛骨'), ('3周', '被动旋前旋后'), ('6周', '弹力带屈伸抗阻，回日常生活'),
               ('3月', '哑铃、旋转抗阻、站姿神经肌肉训练；活动度基本回来'), ('6月', '离心、BOSU、振动杆、药球'), ('4～8月', '回业余运动')]),
    ('box', '文献', 'Kim SE, Choi YC, Lee JY. Early Rehabilitation after Surgical Repair of Medial and Lateral Collateral Elbow Ligaments: A Report of Three Cases. Int J Environ Res Public Health. 2020;17(17):6133', 'navy'),
    ('box', '版权', '原文 **CC BY 4.0** 开放获取；原文图已切分，结果图为中文重画', 'teal')])
deck.save(OUT)
