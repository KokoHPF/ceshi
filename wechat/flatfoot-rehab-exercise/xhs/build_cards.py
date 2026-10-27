#!/usr/bin/env python3
"""Kolhe 等 2024 20 岁女性疼痛性扁平足足部康复训练 1 例 → 小红书 3:4 图文卡片。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='足踝康复', source='Kolhe 等 Cureus 2024;16(4):e59377', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
X = lambda n: Image.open(f'{WORK}/x{n}.jpg').convert('RGB')
f1, f3 = X(38), X(70)
f1a, f1b = f1.crop((0, 0, f1.width, f1.height // 2)), f1.crop((0, f1.height // 2, f1.width, f1.height))
f3a, f3b = f3.crop((0, 0, f3.width // 2, f3.height)), f3.crop((f3.width // 2, 0, f3.width, f3.height))

deck.cover(['足部康复训练对', '20 岁女性疼痛性扁平足', '的效果：病例分析'], kicker='Cureus 2024 · 病例报告',
           subtitle='6 个居家动作，练 2 个月',
           photos=[(f3a, '跟腱拉伸'), (f3b, '弹力带抗阻'), (X(80), '足弓滚球')], banner='疼痛 7 → 2 分 · 肌力 1 → 4+ 级')
deck.text('扁平足是什么', '原文引言与讨论', [
    ('box', '定义', '足**内侧纵弓塌陷**，走路时缺少“弹簧”缓冲，每一步足部受力更大', 'teal'),
    ('box', '常见吗', '4～6 岁前超过 **70%** 的孩子是扁平足，6 岁后降到约 **9%**；成人约 **20%**', 'yellow'),
    ('box', '多数不痛', '多为功能性、无痛；但会影响**下肢和腰椎**生物力学，增加疼痛和受伤风险', 'accent'),
    ('box', '可能的原因', '病因不明；不少研究认为与**足内在肌无力**有关', 'navy')])
deck.text('病例：20 岁女性', '原文', [
    ('steps', [('诉', '走路困难，**剧烈活动时痛**（VAS 7/10）'), ('史', '自幼**双侧扁平足**，一侧足跟发育不良'), ('辅', '在用**足弓支撑带**和**鞋内垫板**'),
               ('力', '足内在肌、拇展肌、踝背屈肌都只有 **1 级**'), ('姿', '足姿指数 FPI-6 **+6**，属于旋前足')]),
    ('box', '其他', '神经系统检查正常；步态分析见**代偿动作**', 'grey')])
deck.figure('她在用的辅具', '原文图 1', f1, None, [
    ('steps', [('A', '鞋内植入的**垫板**'), ('B', '双足**足弓支撑带**')]),
    ('box', '用途', '帮助走路时**保持平衡**；训练期间一直在用', 'yellow')], max_h=820)
deck.figure('怎么确认扁平足', '原文图 2', X(40), None, [
    ('bul', ['原文用 **Feiss 线测试**确认扁平足', '并配合徒手肌力评定和足姿指数 FPI-6 评估']),
    ('box', '编者注', 'Feiss 线通常连接**内踝尖**和**第 1 跖骨头**，看**足舟骨结节**落在线下多少', 'teal')])
deck.text('训练方案：2 个月，每周 5 天', '原文表 2', [
    ('box', '① 抓毛巾', '毛巾铺地上，用**脚趾**往回抓；每次 **15 分钟**', 'teal'),
    ('box', '② 跟腱拉伸', '面墙弓步，后脚跟贴地、髋部压向墙；**30 秒**拉 + 30 秒放，10 次 × 3 组', 'yellow'),
    ('box', '③ 脚趾外展', '双脚平放，脚趾尽量**分开**；保持 5 秒、放松 2 秒，10 次 × 3 组', 'navy'),
    ('box', '④～⑥', '弹力带抗阻（见下页）；**滚球**约 2 分钟；**赤脚活动**每天 ≥45 分钟', 'coral')])
deck.figure('跟腱拉伸 + 弹力带抗阻', '原文图 3', [f3a, f3b], ['A 跟腱拉伸', 'B 弹力带'], [
    ('steps', [('A', '面墙弓步，**后腿**脚跟贴地，髋部轻压向墙'), ('B', '坐位，弹力带绕患足、另一端踩在另一只脚下；**慢慢**把脚向上抬再放回')]),
    ('box', '注意', '原文把 B 叫“胫骨后肌强化”，但动作是**背屈**；胫骨后肌主要负责**内翻**和跖屈', 'accent')])
deck.figure('足弓滚球', '原文图 4', X(80), None, [
    ('bul', ['坐位，球放在**足弓**下', '轻压着**前后滚动**约 2 分钟，换脚', '留意哪里紧、哪里不舒服']),
    ('box', '小提示', '原文叫“高尔夫球”，图中用的是一个**圆柱形小滚筒**', 'grey')], max_h=700)
deck.text('为什么练这些', '原文讨论', [
    ('steps', [('1', '抓毛巾、脚趾外展 → 练**足内在肌**'), ('2', '跟腱拉伸 → 改善**跟腱和小腿**柔韧性，利于步态时足部对线'),
               ('3', '胫骨后肌强化 → 支撑**内侧纵弓**、防止过度旋前'), ('4', '赤脚活动 → 获得**本体感觉**反馈、激活肌肉')]),
    ('box', '作者的结论', '针对内在肌、足弓支撑和本体感觉的个体化训练，是缓解疼痛性扁平足的关键', 'teal'),
    ('box', '但要注意', '这些机制是作者根据文献的推论，本例**无法验证**哪一项起了作用', 'accent')])
fig, axs = plt.subplots(1, 3, figsize=(9.6, 6), gridspec_kw={'width_ratios': [3, 1, 2]})
C0, C1 = '#9AA5B1', '#2E86AB'
ax = axs[0]; pre = [5, 4, 5]; post = [2, 1, 1]; x = range(3)
ax.bar([i - .2 for i in x], pre, .4, color=C0, label='前'); ax.bar([i + .2 for i in x], post, .4, color=C1, label='后')
ax.set_xticks(list(x), ['痛', '难', '限'], fontsize=18); ax.set_ylim(0, 6.5); ax.set_title('FFI（越低越好）', fontsize=18); ax.legend(frameon=False, fontsize=16)
ax = axs[1]; ax.bar([0, 1], [7, 2], .6, color=[C0, C1]); ax.set_xticks([0, 1], ['前', '后'], fontsize=18); ax.set_ylim(0, 10); ax.set_title('VAS', fontsize=18)
ax = axs[2]; x = range(2); ax.bar([i - .2 for i in x], [50, 50], .4, color=C0); ax.bar([i + .2 for i in x], [97, 100], .4, color=C1)
ax.set_xticks(list(x), ['日常', '运动'], fontsize=18); ax.set_ylim(0, 110); ax.set_title('FAAM（%）', fontsize=18)
for a in axs: a.spines[['top', 'right']].set_visible(False); a.tick_params(axis='y', labelsize=14)
fig.tight_layout()
deck.chart('训练 2 个月后', '据原文表 3 重画', fig, [
    ('bul', ['疼痛 VAS **7 → 2**', 'FAAM 日常 **50% → 97%**，运动 **50% → 100%**', '肌力 **1 → 4+ 级**；足姿指数 **+6 → -2**（旋前 → 轻度旋后）'])])
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '要打折扣'),
    ('bul', ['**单个病例**、无对照、无随访；同时还在用**辅具**', '2 个月内肌力 1 → 4+、足姿从旋前到旋后，**变化偏大**；评估者是否盲法未交代']),
    ('h', '原文对不上'),
    ('steps', [('1', '正文说支撑带是图 1A、垫板是 1B，图注和图片**相反**'), ('2', '正文说下肢肌力正常，表 1 却记三组肌群都是 **1 级**'),
               ('3', '“胫骨后肌强化”动作是**背屈**，与该肌作用不符')])])
deck.text('收藏：扁平足居家足部训练', '每周 5 天，持续 2 个月', [
    ('steps', [('1', '**抓毛巾** 15 分钟'), ('2', '**跟腱拉伸** 30 秒 × 10 次 × 3 组'), ('3', '**脚趾外展** 保持 5 秒 × 10 次 × 3 组'),
               ('4', '**弹力带**抗阻 10 次 × 3 组（练胫骨后肌宜做抗阻**内翻**）'), ('5', '**足弓滚球** 约 2 分钟'), ('6', '**赤脚活动**每天 ≥45 分钟')]),
    ('box', '文献', 'Kolhe PD, et al. Effect of Foot Rehabilitation Exercises for Painful Flat Foot in a 20-Year-Old Female: A Case Study Analysis. Cureus. 2024;16(4):e59377', 'navy'),
    ('box', '版权', '原文 **CC BY 4.0** 开放获取；原文图 1、3 切分为单幅', 'teal')])
deck.save(OUT)
