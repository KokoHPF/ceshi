#!/usr/bin/env python3
"""Olagbegi 等 2017 开链、闭链、混合链训练治疗膝骨关节炎：首图中文标题卡、研究流程图（原文图 7 按原文数字用中文重画）、三组方案卡、
原文图 1～6 照片贴中文名称标签配中文图注、结果折线图（据原文表 3）、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('随机临床试验 · 《Archives of Physiotherapy》2017', ['开链、闭链和混合链训练对膝骨关节炎', '患者股四头肌力量和大腿围度的效果'],
               'Olagbegi OM, Adegoke BOA, Odole AC.', 'Arch Physiother. 2017;7:9. doi:10.1186/s40945-017-0036-6',
               '南非罗德斯大学人体运动学与人类工效学系、尼日利亚伊巴丹大学物理治疗系'), 1)
n = 2
def put(im, cap):
    global n; k.save(k.capbox(im, cap), n); n += 1

fig, ax = plt.subplots(figsize=(12, 9.6), dpi=100); ax.set_xlim(0, 120); ax.set_ylim(0, 96); ax.axis('off')
def box(x, y, w, h, t, fc='#E4EAF2', ec='#16324F', fs=15, col='#16324F'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4', fc=fc, ec=ec, lw=1.5)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs, color=col)
def arr(x1, y1, x2, y2): ax.annotate('', (x2, y2), (x1, y1), arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
box(36, 87, 40, 7, '医生转诊的膝骨关节炎患者 n＝105'); box(84, 79, 32, 6, '不符合纳入标准 n＝9', fc='#F3F3F3', ec='#888', col='#555', fs=14)
box(36, 72, 40, 7, '电脑随机分组 n＝96'); arr(56, 87, 56, 79.6); arr(56, 83, 83.6, 82)
G = [('开链组（OKCE）\nn＝32', '退出 6 人\n个人原因、交通/时间、膝痛', '分析 32 人\n（末次观察值结转）'),
     ('闭链组（CKCE）\nn＝32', '退出 6 人\n个人原因、交通/时间、死亡 1 人', '分析 32 人\n（末次观察值结转）'),
     ('混合链组（CCE）\nn＝32', '退出 5 人\n个人原因、交通/时间、膝痛', '分析 32 人\n（末次观察值结转）')]
for i, (a, b, c) in enumerate(G):
    x = 2 + i * 40; arr(56, 72, x + 17, 64.6)
    box(x, 54, 34, 10, a, fs=15); box(x, 33, 34, 12, b, fc='#FFF4D2', ec='#C87800', fs=13); box(x, 14, 34, 10, c, fc='#DEF0EE', ec='#188080', fs=14)
    arr(x + 17, 54, x + 17, 45.6); arr(x + 17, 33, x + 17, 24.6)
ax.text(2, 6, '共 17 人（17.7%）未完成，完成 79 人（26／26／27）；按意向性分析，缺失数据用最后一次测量值代替', fontsize=14, color='#D9432F')
fig.tight_layout(); fig.savefig(f'{WORK}/flow.png', facecolor='white'); plt.close(fig)
put(k.op('flow.png'), '原文图 7 重画：研究流程（数字照原文翻译）')

k.save(k.card('三组怎么练（编者根据原文表 1 整理）', [
    ('三组共同', '共 12 周（每周几次本文没写，要看作者之前发表的文章）；每天服对乙酰氨基酚 3000 mg\n抗阻动作从 10RM 重量开始，每周初重测新的 10RM 加量', LT, TEAL),
    ('开链组（OKCE）：脚不着地、只动小腿', '股四头肌等长收缩（10 次）＋空中蹬车（2 分钟）\n第 2 周加直腿抬高 → 第 3 周直腿抬高负重 → 第 4 周起加坐位全范围伸膝负重（10 次 × 3 组）', GR, (0, 120, 60)),
    ('闭链组（CKCE）：脚踩地、全身一起用力', '股四头肌等长收缩（10 次）＋靠墙滑蹲（10 次）\n第 3 周靠墙滑蹲手持哑铃 → 第 6 周加上下台阶 → 第 7 周起上下台阶负重', OR, (200, 120, 0)),
    ('混合链组（CCE）：开链＋闭链', '直腿抬高（10 次）＋闭链式股四头肌等长收缩（10 次）\n第 2 周加靠墙滑蹲 → 第 3 周直腿抬高、滑蹲负重 → 第 4 周起加坐位全范围伸膝负重', PK, RED),
]), n); n += 1

T = lambda x, t, c: tags_at(k, x, [(.01, .02, t, c)])
put(T('x67.jpg', '开链：负重直腿抬高', C_OK), '原文图 1：负重直腿抬高（开链组、混合链组）。仰卧，健侧屈膝，患侧踝绑沙袋伸直膝关节抬腿')
put(T('x66.jpg', '开链：坐位全范围伸膝', C_OK), '原文图 2：坐位全范围伸膝（开链组、混合链组）。坐在床边，踝绑沙袋，从屈膝伸到完全伸直；10 次 × 3 组')
put(T('x79.jpg', '闭链：负重靠墙滑蹲', C_HI), '原文图 3：手持哑铃靠墙滑蹲（闭链组、混合链组）。背靠墙，双脚前移，沿墙下蹲再起身')
put(T('x78.jpg', '闭链：负重上下台阶', C_HI), '原文图 4：负重上下台阶（闭链组第 6 周起）。踝绑沙袋，踏上矮木台再下来')
a, b = k.op('x77.jpg'), k.op('x89.jpg'); h = 700
a = a.resize((round(a.width * h / a.height), h)); b = b.resize((round(b.width * h / b.height), h))
m = Image.new('RGB', (a.width + b.width + 16, h), 'white'); m.paste(a, (0, 0)); m.paste(b, (a.width + 16, 0)); m.save(f'{WORK}/tests.jpg')
put(tags_at(k, 'tests.jpg', [(.01, .02, '静态肌力：拉力计', C_NAV), (.52, .02, '动态肌力：推算 1RM', C_NAV)]),
    '原文图 5、6：肌力测试。左：屈膝 60° 用拉力计测最大等长伸膝力，测 2 次取平均；右：踝绑重物伸膝到力竭，用 Brzycki 公式由重量和次数推算 1RM。两者都按体重的 0.67 次方标准化')

fig, axs = plt.subplots(1, 3, figsize=(15, 5.6), dpi=100); wk = [0, 4, 8, 12]
D = {'开链组': ([7.02, 8.03, 9.03, 9.97], [4.08, 4.30, 4.56, 4.75], [54.90, 55.06, 55.50, 55.91], '#188080'),
     '闭链组': ([7.26, 8.24, 9.25, 10.25], [4.28, 4.50, 4.75, 5.00], [53.19, 53.50, 54.09, 54.47], '#E8A200'),
     '混合链组': ([7.46, 9.46, 10.42, 11.41], [4.28, 4.59, 4.74, 5.11], [53.63, 54.28, 55.25, 55.31], '#D9432F')}
for g, (s, d, t, c) in D.items():
    for a, v in zip(axs, (s, d, t)): a.plot(wk, v, marker='o', lw=3, ms=8, color=c, label=g)
for a, tt in zip(axs, ['静态股四头肌肌力（标准化值）', '动态股四头肌肌力（标准化 1RM）', '大腿围度（cm）']):
    a.set_title(tt, fontsize=17); a.set_xticks(wk, ['治疗前', '第 4 周', '第 8 周', '第 12 周'], fontsize=13); a.tick_params(axis='y', labelsize=13)
    a.spines[['top', 'right']].set_visible(False); a.grid(axis='y', alpha=.3)
axs[0].legend(frameon=False, fontsize=14); axs[0].set_ylim(5, 13); axs[1].set_ylim(3.5, 5.5); axs[2].set_ylim(52, 57)
fig.tight_layout(); fig.savefig(f'{WORK}/res.png', facecolor='white'); plt.close(fig)
put(k.op('res.png'), '原文表 3 重画：三组肌力和大腿围度随时间变化（均数）。三组都逐渐上升，组间没有显著差异（P 分别为 0.106、0.291、0.660）；大腿围度纵轴从 52 cm 起画，12 周只增加约 1～1.7 cm')
c = k.op('x79.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .45)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
