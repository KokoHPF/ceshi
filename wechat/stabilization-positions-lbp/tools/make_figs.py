#!/usr/bin/env python3
"""Ojoawo 等 2017 俯卧位与仰卧位稳定训练治疗慢性腰痛：首图中文标题卡、研究流程图（原文图 1 为矢量图，按原文数字用中文重画）、
6 个练习照片（原文图 2～7，贴中文名称标签）配中文图注、三组方案卡、结果折线图（据原文表 2～5）、封面。
共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
WORK, OUT, FM, FBOLD = sys.argv[1:5]
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('随机对照试验 · 《Journal of Exercise Rehabilitation》2017', ['两种稳定训练体位对腰痛患者', '疼痛和功能障碍的效果比较'],
               'Ojoawo AO, Hassan MA, Olaogun MOB, Johnson EO, Mbada CE.', 'J Exerc Rehabil. 2017;13(3):363-371. doi:10.12965/jer.1734932.466',
               '尼日利亚奥巴费米·阿沃洛沃大学医学康复系、奥孙州阿苏比亚罗专科医院物理治疗科'), 1)
n = 2
def put(im, cap):
    global n; k.save(k.capbox(im, cap), n); n += 1

# 流程图
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
fig, ax = plt.subplots(figsize=(12, 9.6), dpi=100); ax.set_xlim(0, 120); ax.set_ylim(0, 96); ax.axis('off')
def box(x, y, w, h, t, fc='#E4EAF2', ec='#16324F', fs=15, col='#16324F'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4', fc=fc, ec=ec, lw=1.5)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs, color=col)
def arr(x1, y1, x2, y2): ax.annotate('', (x2, y2), (x1, y1), arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
box(40, 86, 40, 7, '评估合格 n＝63'); box(40, 74, 40, 7, '随机分组 n＝63'); arr(60, 86, 60, 81.6)
G = [('A 组：俯卧位稳定训练\n分到 n＝21\n接受干预 n＝21', '失访 n＝1\n中断干预 n＝1', '纳入分析 n＝19\n排除 n＝0'),
     ('B 组：仰卧位稳定训练\n分到 n＝21\n接受干预 n＝11 ⚠', '失访 n＝4\n中断干预 n＝4', '纳入分析 n＝20 ⚠\n排除 n＝0'),
     ('C 组（“对照”）：俯卧＋仰卧\n分到 n＝21\n接受干预（未写人数）', '失访 n＝2', '纳入分析 n＝17\n排除 n＝17 ⚠')]
for i, (a, b, c) in enumerate(G):
    x = 2 + i * 40; arr(60, 74, x + 17, 66.6)
    box(x, 52, 34, 14, a, fs=13); box(x, 34, 34, 11, b, fc='#FFF4D2', ec='#C87800', fs=13); box(x, 16, 34, 11, c, fc='#DEF0EE', ec='#188080', fs=13)
    arr(x + 17, 52, x + 17, 45.6); arr(x + 17, 34, x + 17, 27.6)
ax.text(2, 6, '⚠ 为原文流程图中前后对不上的数字（见正文“原文里对不上的地方”）；原文摘要和表 1 为 19、20、17 人，共 56 人', fontsize=13, color='#D9432F')
fig.tight_layout(); fig.savefig(f'{WORK}/consort.png', facecolor='white'); plt.close(fig)
put(k.op('consort.png'), '原文图 1 重画：研究流程（数字照原文流程图翻译）')

T = lambda x, t, c: tags_at(k, x, [(.01, .02, t, c)])
put(T('x11.jpg', '练习 1：俯卧抬头抬胸', C_OK), '原文图 2  练习 1：俯卧，双臂放身体两侧，从中立位把头和胸抬离床面，保持 3～5 秒；15 次 × 2 组，量力而行')
put(T('x13.jpg', '练习 2：俯卧对侧手脚同时抬', C_OK), '原文图 3  练习 2：俯卧，对侧手臂和腿同时从中立位抬起到伸展，保持 3～5 秒后放下；15 次 × 2 组')
put(T('x17.jpg', '练习 3：俯卧单腿后伸', C_OK), '原文图 4  练习 3：俯卧，双臂向前伸放在床上，一条腿伸膝、髋过伸抬离床面，保持 3～5 秒；15 次 × 2 组')
put(T('x19.jpg', '练习 4：仰卧对侧手脚同时抬', C_HI), '原文图 5  练习 4：仰卧，对侧手臂（伸直）和腿（屈髋屈膝）同时抬离床面，保持 3～5 秒；15 次 × 2 组')
put(T('x23.jpg', '练习 5：仰卧屈膝向胸', C_HI), '原文图 6  练习 5：仰卧，双臂放在床上，把膝拉向胸口、离开床面保持 3～5 秒；15 次 × 2 组')
put(T('x21.jpg', '练习 6：迷你卷腹', C_HI), '原文图 7  练习 6：迷你卷腹，仰卧把头颈（正文写“头和躯干”）稍抬离床面，保持 3～5 秒；15 次 × 2 组')

k.save(k.card('三组怎么练（编者根据原文整理）', [
    ('三组都有的基础治疗', '腰部红外线照射 15 分钟＋揉捏按摩（配合止痛软膏）\n每周 2 次，共 8 周；第 0、4、8 周评估疼痛（语言评定量表 0～5）和功能障碍（Roland-Morris 问卷 0～24）', LT, TEAL),
    ('俯卧组（SIP，19 人）', '练习 1 俯卧抬头抬胸、练习 2 俯卧对侧手脚同时抬、练习 3 俯卧单腿后伸\n每个动作保持 3～5 秒，15 次 × 2 组', GR, (0, 120, 60)),
    ('仰卧组（SIS，20 人）', '练习 4 仰卧对侧手脚同时抬、练习 5 仰卧屈膝向胸、练习 6 迷你卷腹\n剂量同上', OR, (200, 120, 0)),
    ('俯卧＋仰卧组（SIPS，17 人，原文称“对照组”）', '俯卧和仰卧各选 2 个练习，剂量同上', PK, RED),
]), n); n += 1

fig, axs = plt.subplots(1, 2, figsize=(12, 5.6), dpi=100); wk = [0, 4, 8]
D = {'俯卧组': ([2.09, 1.27, 0.45], [10.09, 4.27, 1.72], '#188080'), '仰卧组': ([2.00, 0.90, 0.45], [7.82, 2.27, 1.00], '#E8A200'), '俯卧＋仰卧组': ([2.09, 1.90, 0.45], [11.18, 3.82, 1.64], '#D9432F')}
for g, (pi, di, c) in D.items():
    axs[0].plot(wk, pi, marker='o', lw=3, ms=9, color=c, label=g); axs[1].plot(wk, di, marker='o', lw=3, ms=9, color=c, label=g)
axs[0].set_title('疼痛（语言评定量表 0～5）', fontsize=18); axs[1].set_title('功能障碍（Roland-Morris 0～24）', fontsize=18)
for a in axs: a.set_xticks(wk, ['治疗前', '第 4 周', '第 8 周'], fontsize=14); a.tick_params(axis='y', labelsize=13); a.spines[['top', 'right']].set_visible(False); a.legend(frameon=False, fontsize=13)
axs[0].set_ylim(0, 3); axs[1].set_ylim(0, 13); fig.tight_layout(); fig.savefig(f'{WORK}/res.png', facecolor='white'); plt.close(fig)
put(k.op('res.png'), '原文表 2～5 重画：三组的疼痛和功能障碍随时间变化（均数）。三组都明显下降，组间没有显著差异；第 8 周三组疼痛完全相同（0.45±0.52）')
c = k.op('x13.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = (c.height - 383) // 2
c.crop((0, max(0, y0), 900, max(0, y0) + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
