#!/usr/bin/env python3
"""Saito 等 2025 髋关节镜术后顽固臀部痛的闭孔神经靶向物理治疗 2 例：中文标题卡、背景卡、患者卡、原文图 1～5 配中文标签和图注
（图内结构缩写保留原样，图注里解释），解剖卡、治疗方案卡、疗程变化图（据原文表 1 用中文重画）、解读卡、封面。
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
k.save(k.title('病例报告 · 《Cureus》2025', ['髋关节镜术后屁股还痛？', '超声引导下的闭孔神经靶向治疗'],
               'Saito M, Kawabata M, Shimizu S, Omodani T.', 'Cureus. 2025;17(10):e95021. doi:10.7759/cureus.95021',
               '日本东京 Advanced Orthopaedics 康复科、北里大学医疗卫生学部'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
T = lambda f, tags: tags_at(k, f, tags)
card('为什么关注术后臀部痛（编者根据原文整理）', [
    ('髋关节镜不是“一做就好”', '股骨髋臼撞击症（FAI）关节镜术后，多数人疼痛和功能改善\n但回归运动率汇总约 93%，回到术前水平约 82%；部分人术后多年仍痛', LT, TEAL),
    ('臀部痛容易被忽略', '术后腹股沟痛研究较多；臀部痛和闭孔神经的关系很少被关注', OR, (200, 120, 0)),
    ('闭孔神经为什么可疑', '它发出关节支支配髋关节囊，走行在闭孔外肌和闭孔内肌之间\n可能被卡压或滑动受限，引起臀部或大腿内侧痛', GR, (0, 120, 60)),
])
card('两位患者（原文）', [
    ('病例 1：40 多岁女性', '右髋关节镜（盂唇撕裂）术后 8 个月，走路时臀部痛\n关节内注射、富血小板血浆、坐骨神经水分离都没用', LT, TEAL),
    ('病例 2：30 多岁男性', '左髋关节镜（盂唇撕裂）术后 11 个月，髋外展外旋时臀部剧痛、大转子后方不适\n关节内注射无效，没做过系统物理治疗', OR, (200, 120, 0)),
    ('共同的查体发现', 'FABER 试验诱发臀部痛（NRS 5、7 分），膝－床距离比健侧大\n髋外旋徒手肌力 2 级；超声下闭孔外肌收缩差\n超声引导触诊：闭孔神经、闭孔外肌周围压痛（病例 1 还有闭孔内肌）', PK, RED),
])
put(T('x34.jpg', [(.02, .03, 'FABER 位测膝－床距离', C_NAV)]), '原文图 1  FABER 位（屈髋、外展、外旋）测膝－床距离（演示模型）：仰卧，测膝外侧到床面的垂直距离；距离越大说明越“打不开”。Tt 胫骨结节，BS 床面')
card('闭孔神经关节支：一个“急转弯”（原文讨论）', [
    ('FABER 为什么会诱发臀部痛', 'FABER 位会牵拉前下方髋关节囊，而这里由闭孔神经关节支支配\n有研究显示其分支分布在关节囊 3 点和 6 点半方向，所以痛可以放射到臀部和大腿后方', LT, TEAL),
    ('解剖上的弱点', '关节支穿出闭孔管后突然改变方向再到关节囊，容易被卡住或滑动受限', OR, (200, 120, 0)),
    ('排除其他神经', '痛在臀部而不在前方或会阴 → 股神经、阴部神经可能性小\n病例 1 之前做过坐骨神经水分离无效 → 更支持闭孔神经', GR, (0, 120, 60)),
])
put(T('x138.jpg', [(.13, .03, '中立位', C_NAV), (.63, .03, 'FABER 位', C_HI)]), '原文图 5  闭孔神经关节支的走行（作者自制模型）：a 中立位，b FABER 位。▼ 为关节支急转弯处。ON-Ab 闭孔神经关节支，ONA 前支，ONP 后支')
card('治疗方案（原文）', [
    ('频率', '每周 1 次手法和运动治疗；每两周 1 次超声引导下闭孔神经水分离', LT, TEAL),
    ('① 闭孔神经短轴滑动手法', '超声下显示闭孔外肌长轴和闭孔管；手指从耻骨下支、坐骨支方向深入\n在闭孔外肌和闭孔内肌之间对神经做滑动手法——超声引导是必须的，单靠触诊定不准', OR, (200, 120, 0)),
    ('② 闭孔外肌激活', '看着实时超声画面反复诱发闭孔外肌收缩，直到收缩改善、局部压痛减轻', GR, (0, 120, 60)),
    ('③ 水分离 + 长轴滑动', '在闭孔外肌深层注入 10 ml 0.09% 利多卡因生理盐水\n注射后立即做“牵拉—放松”：仰卧位髋内旋＋外展（牵拉）→ 外旋＋内收（放松），反复到活动阻力消失', PU, C_NAV),
])
put(T('x49.jpg', [(.07, .83, '解剖模型示意', C_NAV), (.57, .83, '超声长轴图', C_NAV)]), '原文图 2  闭孔神经短轴滑动手法：a 作者自制示意（绿线为闭孔神经），b 超声下闭孔外肌长轴和闭孔管。EO 闭孔外肌，IO 闭孔内肌，OC 闭孔管，Ac 髋臼，FH 股骨头')
put(T('x68.jpg', [(.02, .03, '超声实时反馈下激活闭孔外肌', C_HI)]), '原文图 3  闭孔外肌激活（演示模型）：看着实时超声画面反复收缩闭孔外肌，直到压痛减轻。图中超声缩写同图 2（图内“HF”应为 FH 股骨头）')
put(T('x83.jpg', [(.06, .03, '起始位', C_NAV), (.39, .03, '牵拉', C_HI), (.72, .03, '放松', C_OK)]), '原文图 4  闭孔神经长轴滑动：a 起始位；b 牵拉位——髋内旋（黑箭头）＋外展（绿箭头）；c 放松位——外旋（紫箭头）＋内收（蓝箭头）。反复进行，直到神经活动度改善、阻力减小')
fig, axs = plt.subplots(1, 3, figsize=(13, 6.2), dpi=100)
s = ['第 1 次\n（0 周）', '第 2 次\n（1 周）', '第 3 次\n（2 周）', '第 4 次\n（4 周）']
d = {'FABER 诱发疼痛（NRS，越低越好）': ([5, 3, None, 0], [7, 2, 2, None], (0, 8)),
     '膝－床距离（cm，越小越好）': ([26.8, 23.5, 22, 22], [21, 20, 20, None], (18, 28)),
     '闭孔外肌分级（0～5）': ([2, 3, 4, 4], [2, 3, 4, None], (0, 5))}
for ax, (nm, (a, b, yl)) in zip(axs, d.items()):
    for ys, c, lab in ((a, '#2E86AB', '病例 1'), (b, '#C0392B', '病例 2')):
        xs = [i for i, y in enumerate(ys) if y is not None]; v = [y for y in ys if y is not None]
        ax.plot(xs, v, marker='o', lw=2.6, ms=9, color=c, label=lab)
        for x, y in zip(xs, v): ax.text(x, y + (yl[1] - yl[0]) * .035, f'{y:g}', ha='center', fontsize=13, color=c)
    ax.set_xticks(range(4), s, fontsize=11); ax.set_ylim(yl[0], yl[1] + (yl[1] - yl[0]) * .12); ax.set_title(nm, fontsize=15)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); ax.tick_params(axis='y', labelsize=12)
axs[0].legend(frameon=False, fontsize=14)
fig.suptitle('每次治疗前的变化（原文表 1）', fontsize=21)
fig.text(.5, .015, '病例 1 第 3 次的 NRS、病例 2 第 4 次的数据原文空缺；两例闭孔外肌分级前 3 次相同，线重合', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, .94)); fig.savefig(f'{WORK}/course.png', facecolor='white'); plt.close(fig)
put('course.png', '据原文表 1 重画：两例 FABER 诱发疼痛、膝－床距离、闭孔外肌分级都逐次改善；最后一次治疗后随访超过 6 个月，臀部痛都没有复发')
card('这 2 例能说明什么（编者解读）', [
    ('提供了一个思路', '髋关节镜术后顽固臀部痛，除了关节内问题，还可以想到闭孔神经关节支和闭孔外肌\nFABER 诱发臀部痛＋超声下闭孔外肌收缩差＋闭孔神经周围压痛，是作者用的线索', GR, (0, 120, 60)),
    ('证据很弱', '只有 2 例、没有对照；不能排除安慰剂、自然恢复或单纯康复的作用\n水分离、手法、运动同时做，分不清谁起作用；没用 HOS-ADL、iHOT-33 等量表', PK, RED),
    ('门槛不低', '需要熟练的超声引导触诊、手法和注射技术；水分离属于注射操作，须由有资质的医生完成\n压痛按压力度没有量化；阴部神经也没评估', OR, (200, 120, 0)),
])
c = k.op('x49.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = max(0, (c.height - 383) // 2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
