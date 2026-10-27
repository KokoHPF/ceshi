#!/usr/bin/env python3
"""Kolhe 等 2024 20 岁女性疼痛性扁平足足部康复训练 1 例：中文标题卡、背景卡、病例卡、原文图 1～4 配中文图注，
训练方案卡（原文表 2）、评估结果图（据原文表 3 用中文重画）、解读卡、封面。
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
k.save(k.title('病例报告 · 《Cureus》2024', ['疼痛性扁平足', '6 个足部训练练 2 个月，效果如何'],
               'Kolhe PD, Sharath HV, Rathi SG, Patil DS.', 'Cureus. 2024;16(4):e59377. doi:10.7759/cureus.59377',
               '印度 Datta Meghe 高等教育研究院 Ravi Nair 物理治疗学院'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
card('扁平足是什么（编者根据原文整理）', [
    ('定义', '足内侧纵弓塌陷，走路时缺少“弹簧”缓冲，每一步足部受力都更大；与高弓足相反', LT, TEAL),
    ('常见吗', '4～6 岁前超过 70% 的孩子是扁平足，6 岁后降到约 9%；成人约 20%', OR, (200, 120, 0)),
    ('多数不痛', '骨科门诊常见，多数是功能性、无痛的；但会影响下肢和腰椎生物力学，增加疼痛和受伤风险', GR, (0, 120, 60)),
    ('可能的原因', '病因不明；不少研究认为与足内在肌无力有关', PU, C_NAV),
])
card('病例（原文）', [
    ('谁', '20 岁女性，因走路困难到物理治疗科就诊；自幼双侧扁平足，一侧足跟发育不良', LT, TEAL),
    ('症状', '剧烈活动时疼痛（VAS 7/10）；步态分析见代偿动作；神经系统检查正常', OR, (200, 120, 0)),
    ('已在用的辅具', '双足足弓支撑带、鞋内垫板，帮助走路时保持平衡', GR, (0, 120, 60)),
    ('肌力（徒手肌力评定）', '足内在肌、拇展肌（脚趾外展）、踝背屈肌都只有 1 级', PU, C_NAV),
    ('足姿指数 FPI-6', '+6 分，属于旋前足', PK, RED),
])
put('x38.jpg', '原文图 1  患者已在使用的辅具：A 鞋内植入的垫板，B 足弓支撑带')
put('x40.jpg', '原文图 2  Feiss 线测试，原文用它确认扁平足（编者注：通常连接内踝尖与第 1 跖骨头，看足舟骨结节落在线下多少）')
card('训练方案：2 个月，每周 5 天（原文表 2）', [
    ('① 抓毛巾', '毛巾平铺在地上，用脚趾把毛巾往回抓；每次 15 分钟', LT, TEAL),
    ('② 跟腱拉伸', '面对墙弓步站，后腿脚跟贴地、髋部轻压向墙；保持 30 秒、放松 30 秒，10 次 × 3 组', OR, (200, 120, 0)),
    ('③ 脚趾外展', '双脚平放，脚趾尽量分开；保持 5 秒、放松 2 秒，10 次 × 3 组', GR, (0, 120, 60)),
    ('④ 胫骨后肌强化', '坐位，弹力带一端绕在患足，另一端踩在另一只脚下；放松踝关节后把脚向上抬，再慢慢放回；10 次 × 3 组', PU, C_NAV),
    ('⑤ 滚球', '坐位，球放在足弓下，轻压着前后滚动约 2 分钟', LT, TEAL),
    ('⑥ 赤脚活动', '赤脚或穿无支撑的袜子、拖鞋站立活动（如看电视、玩耍），每天至少 45 分钟，每周 5 天', PK, RED),
])
put('x70.jpg', '原文图 3  A 跟腱拉伸：面对墙弓步站，后腿脚跟贴地；B 胫骨后肌强化：坐位用弹力带抗阻')
put('x80.jpg', '原文图 4  足弓滚球练习（原文称高尔夫球，图中是一个圆柱形小滚筒）')
fig, axs = plt.subplots(1, 4, figsize=(13, 6.2), dpi=100, gridspec_kw={'width_ratios': [3, 1, 2, 1]})
C0, C1 = '#9AA5B1', '#2E86AB'
ax = axs[0]; lab = ['疼痛和僵硬', '困难程度', '活动受限']; pre = [5, 4, 5]; post = [2, 1, 1]; x = range(3)
ax.bar([i - .2 for i in x], pre, .4, color=C0, label='训练前'); ax.bar([i + .2 for i in x], post, .4, color=C1, label='训练后')
for i in x: ax.text(i - .2, pre[i] + .1, pre[i], ha='center', fontsize=16); ax.text(i + .2, post[i] + .1, post[i], ha='center', fontsize=16)
ax.set_xticks(list(x), lab, fontsize=13); ax.set_ylim(0, 6.8); ax.set_title('足功能指数 FFI（各项 1～6，越低越好）', fontsize=14); ax.legend(frameon=False, fontsize=13, loc='upper right')
ax = axs[1]; ax.bar([0, 1], [7, 2], .6, color=[C0, C1]); [ax.text(i, v + .2, v, ha='center', fontsize=16) for i, v in enumerate([7, 2])]
ax.set_xticks([0, 1], ['前', '后'], fontsize=13); ax.set_ylim(0, 11); ax.set_title('疼痛 VAS', fontsize=14)
ax = axs[2]; pre = [50, 50]; post = [97, 100]; x = range(2)
ax.bar([i - .2 for i in x], pre, .4, color=C0); ax.bar([i + .2 for i in x], post, .4, color=C1)
for i in x: ax.text(i - .2, pre[i] + 2, f'{pre[i]}%', ha='center', fontsize=14); ax.text(i + .2, post[i] + 2, f'{post[i]}%', ha='center', fontsize=14)
ax.set_xticks(list(x), ['日常生活', '运动'], fontsize=13); ax.set_ylim(0, 115); ax.set_title('FAAM（越高越好）', fontsize=14)
ax = axs[3]; ax.bar([0, 1], [6, -2], .6, color=[C0, C1]); ax.axhline(0, color='#333', lw=1)
ax.text(0, 6.3, '+6', ha='center', fontsize=16); ax.text(1, -2.9, '−2', ha='center', fontsize=16)
ax.set_xticks([0, 1], ['前', '后'], fontsize=13); ax.set_ylim(-4, 8); ax.set_title('足姿指数 FPI-6', fontsize=14)
for a in axs: a.spines[['top', 'right']].set_visible(False); a.tick_params(axis='y', labelsize=12)
fig.suptitle('训练 2 个月前后的评估结果', fontsize=21)
fig.text(.5, .015, 'FPI-6：0～+5 正常，+6～+9 旋前，−1～−4 旋后', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, .94)); fig.savefig(f'{WORK}/score.png', facecolor='white'); plt.close(fig)
put('score.png', '据原文表 3 重画：疼痛、足功能、足踝能力全面改善；足姿指数从 +6（旋前）变成 -2（轻度旋后）')
card('这个病例能说明什么（编者解读）', [
    ('可以借鉴的', '方案简单、居家可做：抓毛巾、脚趾外展练内在肌，跟腱拉伸，弹力带练胫骨后肌，滚球放松足底，加上每天赤脚活动', GR, (0, 120, 60)),
    ('结果要打折扣', '肌力从 1 级到 4+ 级、足姿从旋前变成旋后，2 个月内变化这么大并不常见；原文没写评估由谁做、是否盲法', OR, (200, 120, 0)),
    ('证据很弱', '单个病例、没有对照，同时还在用足弓支撑带和鞋垫；没有随访，也没交代一侧足跟发育不良如何处理', PK, RED),
    ('别混淆', '方案里的“胫骨后肌强化”动作是把脚向上抬（背屈），更像练胫骨前肌；胫骨后肌主要负责内翻和跖屈', LT, TEAL),
])
c = k.op('x70.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = round(c.height * .55)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
