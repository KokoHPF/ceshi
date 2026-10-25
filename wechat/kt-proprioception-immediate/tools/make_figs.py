#!/usr/bin/env python3
"""Chang 等 2026 肌内效贴张力对慢性踝不稳运动员本体感觉、功能和事件相关电位的即刻影响：首图中文标题卡、实验设计卡、
原文图 1、3、4 用 relabel 原位改中文（work/lab.json、fx.json），原文图 2A 裁切后贴中文标签，
JND 和 N1 结果用中文重画（据原文正文数字），原文图 5、6 脑电波形贴中文标签、功能测试结果卡、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('交叉设计研究 · 《BMC Sports Science, Medicine and Rehabilitation》2026', ['肌内效贴对慢性踝不稳运动员本体感觉', '和功能表现的即刻影响：来自脑电的证据'],
               'Chang CL, Lin HY, Tseng YT, Pan CY, Chen FC, Tsai CL.', 'BMC Sports Sci Med Rehabil. 2026;18:83. doi:10.1186/s13102-025-01468-w',
               '台湾成功大学体育健康与休闲研究所、台湾师范大学、高雄师范大学等'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1

k.save(k.card('实验怎么做（编者根据原文整理）', [
    ('对象', '30 名大学运动员（篮球、排球、羽毛球、足球等），男女各半，平均 21 岁，CAIT 平均 17.2 分；9 人双侧不稳，取 CAIT 分数较低一侧', LT, TEAL),
    ('两次实验', '第 1 次：35% 张力贴扎；间隔 2 个月；第 2 次：0% 张力贴扎（原文称“安慰剂贴”）\n顺序没有随机，所有人都先 35%、后 0%；每次都在贴前、贴后立即测', OR, (200, 120, 0)),
    ('本体感觉', '机器人踝关节装置被动跖屈两次（参考速度 15°/s，比较速度 8.5～14.8°/s），蒙眼塞耳，判断哪次更快，共 30 次\n算出最小可觉差（JND，越小越灵敏）和不确定区间（IU，越小越稳定）', GR, (0, 120, 60)),
    ('脑电', '测本体感觉时同步记录 32 导脑电，看刺激后 100～200 ms 的 N1 波（越负＝皮层反应越强）', PU, C_NAV),
    ('功能测试', '单腿站立（睁眼/闭眼，最长 30 秒）、单腿跳远、单腿左右侧跳（30 秒内跳过间距为身高 22% 的两个标记，记成功和失误次数）', PK, RED),
]), n); n += 1
put('x86.zh.jpg', '原文图 1  贴法：两条 I 形贴，胫骨前肌（蓝）从内侧踝上方贴到第一跖骨基底；腓骨肌（粉）从外侧踝上方贴到足底第五跖骨基底。按“起点到止点”的促进贴法，同一名治疗师操作，贴时受试者戴眼罩')
a = k.op('x97.jpg'); a = a.crop((0, 0, int(a.width * .47), a.height)); a.save(f'{WORK}/f2a.jpg')
put(tags_at(k, 'f2a.jpg', [(.0, .02, '脑电帽', C_NAV), (.0, .22, '眼罩＋耳塞', C_NAV), (.42, .86, '机器人踝本体感觉评估系统', C_OK)]),
    '原文图 2A  坐位，患足固定在踏板上，踝轴对准装置转轴；每次试验先后两次被动跖屈（顺序随机），停 2 秒，然后受试者口头回答“第一次”还是“第二次”更快，系统据此自适应调整下一次的速度差')
put('x104.zh.jpg', '原文图 3  单腿左右侧跳：用患侧单腿在两个标记之间来回横跳，30 秒内越多越好；双脚落地或没跳过标记算失误，连续 3 次失误终止')
put('x127.zh.jpg', '原文图 4  心理物理曲线示例：横轴是两次速度差，纵轴是答对率。答对率 75% 对应的速度差就是最小可觉差（JND，圆圈）；60%～90% 之间的范围是不确定区间（IU）。35% 张力贴后（红实线）曲线左移，0% 张力贴后（蓝实线）右移')

fig, axs = plt.subplots(1, 2, figsize=(12, 5.6), dpi=100)
for a, (t, d, yl, ylim) in zip(axs, [('最小可觉差 JND（°/s，越小越灵敏）', {'35% 张力': (1.86, 1.43), '0% 张力': (1.83, 2.19)}, '°/s', (0, 2.6)),
                                     ('N1 波幅（μV，越负越强）', {'35% 张力': (-13.64, -15.18), '0% 张力': (-15.23, -11.91)}, 'μV', (-18, 0))]):
    for (g, (pre, post)), c, dy in zip(d.items(), ['#D9432F', '#2E6BD9'], [abs(ylim[1]-ylim[0])*.035, -abs(ylim[1]-ylim[0])*.035]):
        a.plot([0, 1], [pre, post], marker='o', ms=10, lw=3, color=c, label=g)
        for x, v in ((0, pre), (1, post)): a.text(x + (-.08 if x == 0 else .08), v + (dy if x == 0 else 0), f'{v:g}', ha='right' if x == 0 else 'left', va='center', fontsize=15, color=c)
    a.set_xticks([0, 1], ['贴前', '贴后'], fontsize=16); a.set_xlim(-.4, 1.55); a.set_ylim(*ylim); a.set_title(t, fontsize=17)
    a.spines[['top', 'right']].set_visible(False); a.tick_params(axis='y', labelsize=13); a.legend(frameon=False, fontsize=15)
axs[0].text(1.12, 1.2, 'P＝0.004', color='#D9432F', fontsize=14); axs[0].text(1.12, 2.35, 'P＝0.015', color='#2E6BD9', fontsize=14)
axs[1].text(1.12, -10.6, 'P＝0.005', color='#2E6BD9', fontsize=14); axs[1].text(1.12, -16.6, 'P＝0.184', color='#D9432F', fontsize=14)
fig.tight_layout(); fig.savefig(f'{WORK}/res.png', facecolor='white'); plt.close(fig)
put(k.op('res.png'), '编者根据原文正文数字重画：35% 张力贴后 JND 变小（更灵敏），0% 张力贴后 JND 变大；N1 波幅在 35% 张力下没有显著变化，0% 张力下明显减弱')
put('x145.jpg', '原文图 5  【0% 张力】中线电极 Fz、FCz、Cz 的总平均脑电波形。红虚线＝贴前，蓝实线＝贴后，圆圈标出 N1 峰（约刺激后 130 ms）。贴后 N1 明显变浅')
put('x185.jpg', '原文图 6  【35% 张力】同上。贴前（红虚线）和贴后（蓝实线）的 N1 峰几乎重合，没有显著变化')
k.save(k.card('功能测试结果（编者根据原文整理）', [
    ('闭眼单腿站立', '35% 张力：16.9 → 21.7 秒（P＝0.001）；睁眼单腿站立没有变化', GR, (0, 120, 60)),
    ('单腿左右侧跳 成功次数', '两次实验贴后都比贴前多（整体 32.8 → 35.3 次）；贴后 35% 张力比 0% 张力多（37.1 vs 33.6 次）', LT, TEAL),
    ('单腿左右侧跳 失误次数', '0% 张力：3.4 → 4.4 次（P＝0.034）；贴后 0% 张力失误比 35% 多（4.4 vs 2.0 次）', OR, (200, 120, 0)),
    ('单腿跳远、不确定区间 IU', '都没有显著变化', PU, C_NAV),
    ('相关', 'JND 改善越多，N1 越强，侧跳成功越多、失误越少（r 约 0.3～0.46）', PK, RED),
]), n); n += 1
c = k.op('x86.zh.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .3)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
