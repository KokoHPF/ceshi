#!/usr/bin/env python3
"""Jiao、Xi、Lin《稳定型第五跖骨基底骨折早期主动康复：病例报告》（JRM-CC 2021;4:jrmcc00068）→ 小红书 3:4 图文卡片。
原文 CC BY-NC 开放获取（禁止商用）：原文图按原样使用；时间轴、负重进度图为编者据原文绘制；卡片注明“仅供学习交流，如有侵权请联系删除”。
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
deck = Deck(series='足踝骨折康复', source='JRM-CC 2021;4:jrmcc00068', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
img = lambda n: Image.open(os.path.join(WORK, n + '.jpg')).convert('RGB')


def timeline_fig(w=9.6, h=5.4):
    """康复时间轴（编者据原文绘制）"""
    ev = [('第 1～2 天', '抬高、冰敷；踝泵、等长收缩', '#1F5F8B'), ('第 4 天', '助行器下负重 10%', '#1F5F8B'), ('第 8 天', '负重 50%，站着讲课 1 h', '#1F5F8B'),
          ('第 14 天', '负重 100%，拄肘拐站 20 min', '#E3A21A'), ('第 25 天', '双肘拐返回工作', '#E3A21A'), ('第 30 天', '脱拐户外走 300 m', '#2E8B57'),
          ('第 55 天', '肌力 5 级，停止专业康复', '#2E8B57'), ('第 3 个月', '慢跑，日常活动全恢复', '#2E8B57')]
    fig, ax = plt.subplots(figsize=(w, h), dpi=100); ax.set_xlim(0, 2); ax.set_ylim(-.2, 5.2); ax.axis('off')
    for i, (t, s_, c) in enumerate(ev):
        col, row = divmod(i, 4); x = .04 + col * 1.0; y = 3.75 - row * 1.15
        ax.scatter(x + .05, y, s=300, color=c, edgecolors='white', linewidths=2.5, zorder=2)
        ax.text(x + .12, y + .2, t, ha='left', va='center', fontsize=19, color=c, weight='bold')
        ax.text(x + .12, y - .25, s_, ha='left', va='center', fontsize=16, color='#222')
    fig.tight_layout(pad=.2); return fig


def wb_fig():
    """负重进度（编者据原文绘制）"""
    fig, ax = plt.subplots(figsize=(9.6, 7.0), dpi=100)
    d = [1, 3, 4, 8, 14, 30]; v = [0, 0, 10, 50, 100, 100]
    ax.step(d, v, where='post', color='#1F5F8B', lw=3.5); ax.plot(d, v, 'o', color='#1F5F8B', ms=10)
    for x, y, t, tx, ty in [(4, 10, '第 4 天\n负重 10%', 4.3, 18), (8, 50, '第 8 天\n助行器 50%', 8.4, 58), (14, 100, '第 14 天 肘拐\n负重 100%', 14.6, 74),
                             (25, 100, '第 25 天\n双肘拐上班', 22.5, 104), (30, 100, '第 30 天\n脱拐', 28.6, 74)]:
        ax.text(tx, ty, t, fontsize=18, color='#333')
    ax.axvspan(0, 3, color='#E3A21A', alpha=.12); ax.text(.4, 88, '不负重', fontsize=18, color='#9a6a00')
    ax.plot([25], [100], 'o', color='#E3A21A', ms=10); ax.set_xlim(0, 34); ax.set_ylim(-5, 125); ax.set_xlabel('骨折后天数', fontsize=18); ax.set_ylabel('患肢负重（% 体重）', fontsize=18)
    ax.tick_params(labelsize=16); ax.spines[['top', 'right']].set_visible(False); fig.tight_layout(); return fig


def fig2img(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['第五跖骨基底骨折', '不打石膏', '第 2 天就开始练'], kicker='JRM-CC 2021 · 病例报告',
           subtitle='稳定型骨折，14 天全负重、30 天脱拐', photos=[(fig2img(timeline_fig()), '康复时间轴（编者据原文整理）')], banner='早期主动康复 · 1 例 37 岁女性')
deck.text('这个病例是什么情况', '原文引言与病例资料', [
    ('box', '国内常规做法', '稳定型第五跖骨基底骨折：骨科多用跨关节石膏/支具轻度外翻位**固定约 4 周**\n康复科出于安全考虑，常在固定 4 周后才开始康复', 'grey'),
    ('box', '这个病例', '37 岁女护士，2019 年 6 月下楼梯伤及左足，X 线示第五跖骨基底骨折（稳定型）\n骨科：跨关节支具、踝轻度外翻功能位固定 + 冰敷 + 活血化瘀药和止痛药，第 4 天复诊决定是否手术\n患者转到康复医院，知情同意后**不手术、不长期固定**，伤后第 1～2 天即开始康复', 'navy'),
    ('box', '作者说', '据作者所知，这是国内首个第五跖骨基底骨折早期康复训练的报告', 'teal')])
deck.figure('① 伤后影像', '原文图 1（伤后第 1 天）、图 2（第 3 天）', img('x4'), None, [
    ('bul', ['第 1 天 X 线：第五跖骨基底骨折', '第 3 天复查：骨折**无变化**'])], max_h=560)
deck.text('② 第 1～4 天：消肿 + 不负重活动', '原文 Treatment and results', [
    ('steps', [('第 1 天', '支具保护，卧床，患足抬高到**与心脏同高**，持续冰敷；监测疼痛、肿胀'),
               ('第 2 天', '冰敷 15 min、间隔 0.5～1 h；支具下踝背伸/跖屈；跖趾关节屈伸时等长收缩、膝屈伸抗阻，各 10 次×3 组/天\n床边坐 10 min（患者不自信、休息差，改回卧床）'),
               ('第 3 天', '足外侧瘀斑 2 cm×6 cm、轻肿不痛 → 停冰敷，小腿到足背贴肌内效贴（足背爪形）\n被动踝活动牵伸小腿三头肌 2 min×5 组/天；主动背伸（踝无阻力）5 s×10 次×3 组\n助行器下**无负重站立** 10 min'),
               ('第 4 天', '瘀斑减少 → 改热疗；助行器下**负重 10%**站立 2～3 min、休息 5 min，5 次/天\n踝中立位、**足跟承重**，防止骨折移位')])])
deck.figure('③ 第 5～15 天：从 50% 到 100% 负重', '原文图 3（第 14 天）、图 4（第 17 天 X 线）', img('x6'), None, [
    ('bul', ['第 5～8 天：踝、膝、髋全范围主动活动 10 次×3 组；助行器下平衡、耐力站立、室内行走\n第 8 天负重 50%，站着讲课 1 h 无不适',
             '第 9～15 天：三关节全范围**抗阻**训练；助行器走稳后换**双肘拐**部分负重行走\n第 14 天：负重 100%，拄肘拐正常姿势站 20 min', '第 17 天 X 线：无变化'])], max_h=520)
deck.chart('④ 负重怎么一步步加上去', '编者据原文绘制', wb_fig(), [
    ('bul', ['第 3 天先在助行器下无负重站立；关键做法：**踝中立位、足跟承重**，先助行器、再双肘拐、最后脱拐', '全程以“无痛、无不适”为前提，按患者反馈调整'])])
deck.figure('⑤ 第 16～35 天：上楼梯、上班、出远门', '原文图 5（第 25 天）、图 6（第 35 天）', img('x28'), None, [
    ('bul', ['第 16～20 天：肘拐下平衡 5 min×5 组；步态各期负重练习 20 min/天；双肘拐两点步户外行走，从 100 m 起加量',
             '第 21～25 天：肘拐上下楼梯；不同地面耐力行走；**第 25 天双肘拐返回工作**',
             '第 26～30 天：脱拐过渡；**第 30 天不用助行具户外走 300 m**', '出差前 5 天：踝本体感觉 20 min、独立行走平衡 10 min、行走耐力 30 min/天；第 35 天独立出行'])], max_h=480)
deck.text('⑥ 第 36 天以后：回归运动', '原文 Treatment and results', [
    ('steps', [('第 36 天起', '踝本体感觉、站立快速反应、不同地面和障碍物上的曲线行走、快速折返'), ('第 55 天', '评估无关节异常，**全身肌力 5 级**，日常和运动能力恢复 → 停止专业康复'),
               ('第 3 个月', '慢跑，恢复全部日常活动')]),
    ('box', '作者解释', '早期固定处于炎症期，随后主动+被动活动促进循环、消肿、减少粘连\n无痛下早期负重防止关节粘连、韧带过度挛缩；助行具辅助的日常和功能训练防止废用和肌力下降', 'teal')])
deck.figure('⑦ 骨折愈合', '原文图 7（第 80 天）、图 8（1.5 年）', img('x30'), None, [
    ('bul', ['第 80 天 X 线：骨折无异常', '1.5 年 X 线：骨折线已愈合'])], max_h=600)
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('第 4 天', '负重 10%'), ('第 8 天', '负重 50%'), ('第 14 天', '负重 100%'), ('第 25 天', '双肘拐上班'), ('第 30 天', '脱拐走 300 m'), ('第 55 天', '停止专业康复')]),
    ('h', '原文对不上的地方'),
    ('bul', ['摘要说“第 2 天”开始康复，正文写“第 1 天”就已启动', '摘要说“伤后 2 个月”慢跑，正文写的是“第 3 个月”', '全文没说骨折具体分区（结节撕脱还是 Jones 区），只说“稳定型”']),
    ('box', '编者提醒（康复科）', '这只是 **1 例**病例；Jones 骨折和近端骨干应力骨折血供差、愈合风险高，不能照搬。是否早期负重须由骨科医生根据分型判断', 'yellow'),
    ('box', '文献 · 版权', 'Jiao L, Xi J, Lin A. Early active rehabilitation treatment for a patient with a stable type of fifth metatarsal base fracture: a case report. J Rehabil Med Clin Commun. 2021;4:1000068.\nCC BY-NC，禁止商用。**仅供学习交流，如有侵权请联系删除**', 'grey')])
deck.save(OUT)
