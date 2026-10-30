#!/usr/bin/env python3
"""AANEM《基于共识的腕管综合征严重程度分级指南》（Robinson 等, Muscle & Nerve 2026；中文译本）→ 小红书 3:4 图文卡片。
原文 © 2026 AANEM, All rights reserved：图 6（Bland 分级流程图，x16.jpg）原样使用未作修改；图 7 的手术结局数据由编者用中文重画；
卡片注明“仅供学习交流，如有侵权请联系删除”。用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from io import BytesIO
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='手腕康复', source='Robinson et al. Muscle Nerve 2026 · doi:10.1002/mus.70384', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
F = lambda n: Image.open(f'{WORK}/{n}.jpg').convert('RGB')

# 原文图 7：9406 例腕管松解术后患者报告结局（治愈、明显好转、好转、无变化、加重）
OUTC = {0: (240, 177, 59, 62, 46), 1: (331, 189, 62, 34, 46), 2: (671, 335, 86, 51, 73), 3: (1394, 720, 207, 65, 106),
        4: (753, 470, 125, 71, 90), 5: (1020, 787, 275, 111, 173), 6: (129, 167, 107, 111, 63)}
LAB = ['治愈', '明显好转', '好转', '无变化', '加重']; COL = ['#2E7D4F', '#8BC34A', '#F3E9C6', '#F0A030', '#C0392B']


def outcome_fig(w=9.6, h=5.6, cover=False):
    fig, ax = plt.subplots(figsize=(w, h), dpi=100)
    for g, v in OUTC.items():
        tot = sum(v); b = 0
        for k, (n, c) in enumerate(zip(v, COL)):
            p = n / tot * 100; ax.bar(g, p, .72, bottom=b, color=c, edgecolor='white', lw=.6)
            if k == 0 or (not cover and k == 1): ax.text(g, b + p / 2, f'{p:.0f}%', ha='center', va='center', fontsize=14, color='white' if k == 0 else '#1b3d1b', weight='bold')
            b += p
        if not cover: ax.text(g, 101.5, f'n={tot}', ha='center', fontsize=11, color='#555')
    ax.set_xticks(range(7), [f'{g} 级' for g in range(7)], fontsize=15); ax.set_ylim(0, 106); ax.set_ylabel('患者占比（%）', fontsize=14)
    ax.tick_params(axis='y', labelsize=12); ax.spines[['top', 'right']].set_visible(False)
    from matplotlib.patches import Patch
    if cover:
        ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(COL, LAB)], frameon=False, fontsize=13, loc='upper center', bbox_to_anchor=(.5, -.1), ncol=5)
        ax.set_ylim(0, 125); ax.set_yticks([0, 25, 50, 75, 100]); ax.set_ylabel('')
    else:
        ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(COL, LAB)][::-1], frameon=False, fontsize=12.5, loc='center left', bbox_to_anchor=(1.0, .5))
    fig.tight_layout(); return fig


def fig2img(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['腕管综合征', '肌电图严重程度', '统一用 Bland 分级'], kicker='AANEM 指南 · Muscle & Nerve 2026',
           subtitle='0～6 级怎么分、对手术效果意味着什么', photos=[(fig2img(outcome_fig(9.6, 5.7, cover=True)), '9406 例腕管松解术后结局（据原文图 7 重画）')],
           banner='2～3 级术后效果最好')
deck.text('为什么要统一分级', '原文背景与调查', [
    ('box', '现状很乱', '已发表的腕管综合征（CTS）电诊断严重程度量表有 **12 种**，连“中度”的定义都各不相同\n转诊医生看不出两份报告的“中度”是不是一回事，也不清楚分级里有没有混入临床症状', 'accent'),
    ('box', '调查 1253 名电诊断医生', '1066 名 AANEM 会员 + 187 名欧洲临床神经生理医生\n约 **90%** 始终或经常在报告里写严重程度\n只有 **43%** 完全按神经传导检查结果分级，其余混入症状、肌电图失神经等\n**27%** 不用任何固定量表（“普通英语”）\n美国最常用 Stevens 量表，欧洲最常用 Bland 量表', 'yellow'),
    ('box', '工作组目标', '2024 年 AANEM 成立 CTS 严重程度工作组，推荐**一个**统一的、有证据的分级量表', 'navy')])
deck.text('好量表要满足的 7 个要素', '德尔菲法：18 名专家（含物理治疗师、作业治疗师和患者）', [
    ('steps', [('1', '**一致性**：患者没变，重复检查（同一或不同实验室）应得到同一级'), ('2', '**可理解**：电诊断医生和转诊医生都看得懂；单维比多维好懂'),
               ('3', '**效度**：与症状、查体、自然病程、影像或治疗结局有关联'), ('4', '**客观性**：不同人看同一组数据，不用主观判断就给出同一级'),
               ('5', '**统一性**：按 AANEM 最低检查标准就能用，不额外要求针极肌电图等'), ('6', '**反应性**：病情好转或加重时分级跟着变'),
               ('7', '**有序性**：级别之间有明确先后顺序')]),
    ('box', '结果', '工作组按这 7 个要素给 12 种量表打分，**Bland 量表**（又称坎特伯雷量表）最符合，全体一致推荐', 'teal')])
deck.text('Bland 量表：0～6 级', '原文表 2（编者中文整理）', [
    ('steps', [('0', '**正常**：检查正常'), ('1', '**极轻度**：只有最敏感的对比测试（联合感觉指数、掌/腕对比等）异常'),
               ('2', '**轻度**：腕—指感觉传导减慢或远端感觉潜伏期延长；远端运动潜伏期（DML，记录拇短展肌）**正常**'),
               ('3', '**中度**：感觉异常、所有正中神经感觉反应**仍存在**；DML 延长但 **≤6.5 ms**'),
               ('4', '**重度**：一条或多条正中神经感觉反应**缺失**；DML 延长但 ≤6.5 ms'),
               ('5', '**极重度**：DML **>6.5 ms**；感觉反应通常缺失（也可存在但减慢）'),
               ('6', '**终末期**：感觉、运动反应基本记录不到；如有运动反应，波幅 **<0.2 mV**')]),
    ('box', '注', '原版把 6 级叫“极度重度”，指南建议改称“终末期”', 'grey')])
deck.figure('按流程图逐步定级', '原文图 6（原图未改动，英文）', F('x16'), None, [
    ('bul', ['确诊 CTS 后从顶部开始：先看拇短展肌 CMAP 是否记录不到（→6 级）', '再看 DML 是否 >6.5 ms（→5 级）、DML 是否延长、感觉反应是否缺失或延迟', '都正常时看敏感对比测试：异常 1 级，正常 0 级'])],
             max_h=1000)
deck.text('Bland 量表好在哪', '原文 1.7.1、1.7.2', [
    ('box', '技术要求低', '按 AANEM CTS 最低检查标准即可；感觉检查用潜伏期或传导速度都行\n唯一必需的运动检查：**正中神经→拇短展肌**\n**不需要针极肌电图**（也没有证据显示它对分级或预后有独特价值）', 'teal'),
    ('box', '与临床有关', '分级与**症状严重程度**、超声下**正中神经横截面积**强相关（p<0.0001）', 'navy'),
    ('box', '能预测手术结局', '基于 **9000 多例**腕管松解术的患者报告结局验证', 'yellow')])
deck.chart('分级与手术效果', '据原文图 7 重画：9406 例腕管松解术后患者自评结局', outcome_fig(), [
    ('bul', ['**2～3 级**“治愈”比例最高（约 55%～56%）', '0 级、6 级术后效果最差：6 级治愈仅约 22%，无变化或加重约 30%', '注意：这是单一数据库的自评结局，不是随机对照研究'])])
deck.text('分级怎么指导治疗', '原文 1.7.3', [
    ('box', '0～1 级（正常 / 极轻度）', '先**非手术**：夜间夹板和（或）类固醇注射——这类患者手术效果不佳', 'teal'),
    ('box', '2 级（轻度）', '也可先非手术；**无效再考虑转诊手术**', 'navy'),
    ('box', '3～4 级（中度 / 重度）', '告知患者这是**考虑腕管松解的最佳时机**，以防神经进一步退变', 'yellow'),
    ('box', '5～6 级（极重度 / 终末期）', '仍应考虑手术，但要告知**完全恢复的机会降低**', 'accent'),
    ('box', '编者注', '分级只反映神经电生理改变，不等于症状轻重；治疗决策仍需结合症状和查体', 'grey')])
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('2 级', '感觉异常、运动正常'), ('3 级', '运动 DML 也延长（≤6.5 ms）'), ('4 级', '感觉反应缺失'), ('5 级', 'DML >6.5 ms'), ('6 级', 'CMAP <0.2 mV 或记录不到')]),
    ('h', '中文译本的问题（卡片已按英文原意更正）'),
    ('bul', ['把 SNAP（感觉神经动作电位）译成“体感诱发电位”', '2 级把感觉传导速度（SCV）写成“运动传导速度”；3 级把 DML 写成“感觉运动潜伏期”', 'EDX（电诊断）在一处被译成“急诊科”']),
    ('box', '文献 · 版权', 'Robinson LR, Al-Lawati ZJ, Andary M, et al.《AANEM 基于共识的腕管综合征严重程度分级指南》. Muscle & Nerve, 2026. doi:10.1002/mus.70384（中文译本）\n© 2026 AANEM, All rights reserved；图 6 为原图未修改。**仅供学习交流，如有侵权请联系删除**', 'grey')])
deck.save(OUT)
