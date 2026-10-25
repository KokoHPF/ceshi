#!/usr/bin/env python3
"""Sato 等 2025 下肢体位和髋周肌共同收缩对盆底肌自主收缩的影响：首图中文标题卡、实验流程卡、原文图 1～4 四种练习照片贴中文标签、
原文图 5～6 超声图贴中文标签、结果柱状图（原文图 7 按原文数字用中文重画）、居家练习要点卡、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('原创研究 · 《Cureus》2025', ['下肢体位和髋周肌共同收缩', '对盆底肌自主收缩效率的影响'],
               'Sato Y, Miyake Y, Nakajima M.', 'Cureus. 2025;17(4):e83088. doi:10.7759/cureus.83088',
               '日本福山 Studio TAIKA 物理治疗、吉备国际大学保健医疗福祉学部'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1

k.save(k.card('实验怎么做（编者根据原文整理）', [
    ('受试者', '19 名健康女大学生，平均 20 岁，BMI 约 20；没有生育史、盆底疾病、腰髋骨科或神经疾病', LT, TEAL),
    ('测前准备', '测前 2 小时禁食；1 小时前排空膀胱，再喝 500 ml 水（让膀胱充盈，超声才看得清膀胱底）', PU, C_NAV),
    ('四种练习（随机顺序）', 'A 仰卧伸腿（髋 0°）\nB 仰卧屈膝（髋屈 45°）\nC 仰卧屈膝＋双腿往外撑弹力带（髋外展外旋，30% 最大力）\nD 仰卧屈膝＋双膝夹球（髋内收，30% 最大力）', GR, (0, 120, 60)),
    ('每种练习的做法', '收缩盆底肌 10 秒、休息 20 秒，做 3 次；正常呼吸\n口令：“像把阴道往上提一样，收紧臀部”', OR, (200, 120, 0)),
    ('怎么判断收得好不好', '经腹超声（肚脐下 10 cm，探头倾斜 30°）测膀胱底被抬高了多少毫米，3 次取平均；抬得越高，说明盆底肌收缩越有效', PK, RED),
]), n); n += 1

T = lambda x, t, c: tags_at(k, x, [(.02, .03, t, c)])
put(T('x38.jpg', 'A 仰卧伸腿', C_NAV), '原文图 1  练习 A：仰卧，双腿伸直（髋 0°）收缩盆底肌')
put(T('x54.jpg', 'B 仰卧屈膝（最好）', C_OK), '原文图 2  练习 B：仰卧屈膝，髋屈 45°、不内外旋，单纯收缩盆底肌——膀胱底抬得最高')
put(T('x65.jpg', 'C 屈膝＋外撑弹力带', C_HI), '原文图 3  练习 C：在 B 的姿势上，大腿套带拉力传感器的弹力带（股骨外上髁上方约 5 cm），一边往外撑（髋外展外旋，30% 最大力）一边收缩盆底肌')
put(T('x76.jpg', 'D 屈膝＋夹球', C_HI), '原文图 4  练习 D：在屈膝姿势上（髋外展 30°），两膝之间夹一个带压力表的球（股骨内上髁上方约 5 cm），一边夹（髋内收，30% 最大力）一边收缩盆底肌')

a, b = k.op('x90.jpg'), k.op('x92.jpg'); h = 700
a = a.resize((round(a.width * h / a.height), h)); b = b.resize((round(b.width * h / b.height), h))
m = Image.new('RGB', (a.width + b.width + 16, h), 'white'); m.paste(a, (0, 0)); m.paste(b, (a.width + 16, 0)); m.save(f'{WORK}/us.jpg')
put(tags_at(k, 'us.jpg', [(.08, .14, '静息', C_NAV), (.58, .14, '收缩', C_HI)]),
    '原文图 5、6  经腹超声看膀胱底（黑色区域为充盈的膀胱）。左：静息时在膀胱后壁位移最明显的点标“×”；右：收缩时膀胱底被抬高，上面的“×”为收缩时位置、下面的为静息时位置，两点的垂直距离就是抬高量')

fig, ax = plt.subplots(figsize=(10, 6.4), dpi=100)
names = ['A 仰卧伸腿', 'B 仰卧屈膝', 'C 屈膝＋外撑', 'D 屈膝＋夹球']; m = [3.58, 6.00, 2.64, 2.73]; sd = [2.1, 3.1, 4.3, 2.8]
cols = ['#8FA7BF', '#188080', '#E8A08A', '#E8A08A']
ax.bar(range(4), m, .6, yerr=sd, capsize=8, color=cols, error_kw=dict(lw=1.5, ecolor='#555'))
for i, (v, s) in enumerate(zip(m, sd)): ax.text(i + .33, v + .2, f'{v:.2f}', fontsize=16, fontweight='bold', va='bottom')
for x2, y in ((0, 9.8), (2, 10.9), (3, 12.0)):
    ax.plot([1, 1, x2, x2], [y - .3, y, y, y - .3], color='#333', lw=1.4); ax.text((1 + x2) / 2, y + .05, '**', ha='center', fontsize=18)
ax.set_xticks(range(4), names, fontsize=16); ax.set_ylabel('膀胱底抬高（mm）', fontsize=16); ax.set_ylim(0, 13.2); ax.tick_params(axis='y', labelsize=14)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
ax.set_title('四种练习中膀胱底抬高量（均数 ± 标准差，19 人）', fontsize=18, pad=12)
fig.tight_layout(); fig.savefig(f'{WORK}/res.png', facecolor='white'); plt.close(fig)
put(k.op('res.png'), '原文图 7 重画：仰卧屈膝（B）时膀胱底抬得最高，比其他三种都显著更高（** P<0.01）；加上髋外展或内收后反而下降。注意 C 组标准差（4.3）比均数（2.64）还大，个体差异很大')

k.save(k.card('落到训练：盆底肌练习怎么摆（编者整理）', [
    ('起始体位', '仰卧屈膝、双脚踩床，髋屈约 45°，膝不内扣也不外分', GR, (0, 120, 60)),
    ('只练盆底肌', '先学会单独收缩盆底肌：不要同时夹腿、撑腿、夹臀或憋气；能稳定做到后再考虑加其他动作', LT, TEAL),
    ('剂量（本研究）', '收缩 10 秒、放松 20 秒；正常呼吸', OR, (200, 120, 0)),
    ('要注意', '本研究对象是年轻、健康、没生过孩子的女性，只看了一次收缩时的即刻表现；压力性尿失禁患者是否同样适用、长期训练效果如何，还需要研究', PK, RED),
]), n); n += 1
c = k.op('x54.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .25)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
