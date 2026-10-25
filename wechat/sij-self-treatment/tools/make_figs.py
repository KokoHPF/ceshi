#!/usr/bin/env python3
"""Bertrand 等 2021 骶髂前屈试验（SIFFT）指导的自我矫正练习小样本随机试验：中文标题卡、研究设计卡、原文图 1～7 配中文图注，
判断方向卡、结果图（原文表 2 的 ODI 变化、原文图 9 的即时疼痛变化，用中文重画）、解读卡、封面。
原文图 8（试验流程图）、图 9（英文折线图）、图 10（会议海报）和视频截图不直接使用。
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
k.save(k.title('小样本随机试验 · 《Cureus》2021', ['骨盆一高一低？', '两分钟“找平”练习自我缓解慢性腰痛'],
               'Bertrand H, Reeves KD, Mattu R, Garcia R, Mohammed M, Wiebe E, Cheng AL.', 'Cureus. 2021;13(11):e19483. doi:10.7759/cureus.19483',
               '加拿大不列颠哥伦比亚大学家庭医学科、美国密苏里大学堪萨斯城分校医学院等'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
T = lambda f, tags: tags_at(k, f, tags)
k.save(k.card('研究怎么做的（编者根据原文整理）', [
    ('谁参加', '加拿大温哥华一家家庭医学诊所；腰痛 ≥3 个月、疼痛 ≥5/10\n两侧髂后上棘高度差 ≥5 mm、髂后上棘下方韧带压痛；72 人中 62 人（86%）符合', LT, TEAL),
    ('第 1 个月：随机分 3 组（开放标签，不设盲）', '① 找平练习组 21 人：按测出的方向做 2 分钟练习，痛了就做\n② 骨盆带组 21 人：做容易诱发腰痛的活动时系骨盆稳定带\n③ 常规治疗组 20 人：继续原来的理疗、按摩、针灸、用药等', OR, (200, 120, 0)),
    ('第 2 个月：所有人都用练习＋骨盆带', '按需使用 1 个月，再复查', GR, (0, 120, 60)),
    ('看什么', '主要：Oswestry 功能障碍指数（ODI，越低越好，最小有意义变化取 11 分）\n次要：髂后上棘高度差、简明疼痛量表（BPI）、做完练习或系上骨盆带前后的即时疼痛', PU, C_NAV),
]), n); n += 1
put(T('f1.jpg', [(.02, .02, '前屈位找髂后上棘', C_NAV)]), '原文图 1  骶髂前屈试验（SIFFT）：患者双腿伸直、髋部前屈，双臂靠在桌上放松臀肌。检查者用拇指尺侧从臀沟两侧向上按，碰到骨性阻挡就是髂后上棘下缘，用记号笔标在拇指和髂后上棘之间，痛侧写字母 B（before）')
put(T('f2.jpg', [(.02, .02, '水平仪放在低的一侧', C_NAV)]), '原文图 2  患者站直，把粘了小水平仪的尺子放在较低的标记上，调平后在较高一侧对应位置做记号')
put(T('f3.jpg', [(.02, .02, '量两侧高度差', C_HI)]), '原文图 3  用尺子量出两侧标记的高度差（单位 mm）。≥5 mm 判为骶髂“扭转”，可以入组')
k.save(k.card('按测出的方向选练习（原文的判断逻辑）', [
    ('先查腿长', '从肚脐量到内踝，两侧差 >1 cm 先在短腿侧垫鞋垫，再做测试；差 >3 cm 不入组', LT, TEAL),
    ('痛侧髂后上棘偏高 → 判为髋骨“前旋”', '练习：用同侧大腿顶住髂前上棘，把它往后推', OR, (200, 120, 0)),
    ('痛侧髂后上棘偏低 → 判为髋骨“后旋”', '练习：同侧大腿后伸到底，靠缝匠肌和股直肌把髋骨往前拉', GR, (0, 120, 60)),
    ('每个姿势保持 2 分钟，做完再测', '还不平且仍痛就再做一次；不痛的一侧少用力或只扶住', PU, C_NAV),
    ('注意：这是作者自己的模型', '“前旋／后旋”是根据髂后上棘高低推出来的，没有用影像证实；原文也承认没做正式的信度检验', PK, RED),
]), n); n += 1
put(T('f4.jpg', [(.02, .02, '弓步拉伸式（最常用）', C_HI)]), '原文图 4  拉伸式（右侧前旋＋左侧后旋）：右脚和左膝着地，双手放在右脚两侧；身体前倾，让右大腿用力顶住右髂前上棘；左膝尽量往后滑，使左髋后伸，左腹股沟有强烈牵拉感。保持 2 分钟。62 人中 51 人做这个')
put(T('f5.jpg', [(.02, .02, '仰卧、需要助手', C_NAV)]), '原文图 5  仰卧版（右侧前旋＋左侧后旋）：臀部在床沿，右腿屈、左腿伸；右脚垫软垫抵在检查者胸前，检查者前倾把右大腿压向右髂前上棘，同时向下压左大腿使其后伸。保持 2 分钟。62 人中 3 人因活动受限或腹部较大用这个')
put(T('f6.jpg', [(.02, .02, '椅子版（只适合前旋）', C_NAV)]), '原文图 6  椅子版（右侧前旋）：右脚踩在椅面上，双手抓住右脚两侧的椅面，左膝贴椅子前沿；身体后仰，双手用力往上拉，保持 2 分钟。适合只有一侧痛、且这一侧偏高、手臂力量够的人。62 人中 6 人做这个')
put(T('f7.jpg', [(.02, .02, '做完再测：A＝after', C_OK)]), '原文图 7  做完 2 分钟练习后重测，在新位置写字母 A（after）。作者的经验是两侧找平后，疼痛和活动受限也随之缓解')

# 结果图 1：ODI 0～1 个月改善
fig, ax = plt.subplots(figsize=(12, 6.4), dpi=100)
labs = ['找平练习组', '骨盆带组', '常规治疗组']; v = [12.5, 4.3, -3.4]; cols = ['#2E86AB', '#E8A200', '#9AA5B1']
b = ax.bar(labs, v, color=cols, width=.55)
for r, x in zip(b, v): ax.text(r.get_x() + r.get_width() / 2, x + (0.8 if x >= 0 else -1.8), f'{x:+g}', ha='center', fontsize=20)
ax.axhline(0, color='#333', lw=1); ax.axhline(11, color='#C0392B', ls='--', lw=1.5); ax.text(2.32, 11.4, '最小有意义变化 11 分', color='#C0392B', fontsize=14, ha='right')
ax.set_ylim(-8, 18); ax.set_ylabel('ODI 改善（分，越高越好）', fontsize=15); ax.tick_params(labelsize=16)
ax.set_title('第 1 个月：ODI 功能评分改善（平均值）', fontsize=21, pad=16); ax.spines[['top', 'right']].set_visible(False)
fig.text(.5, .015, '练习组 vs 常规治疗：差 15.9 分，P＝0.002；练习组 vs 骨盆带组：经多重比较校正后不显著', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, 1)); fig.savefig(f'{WORK}/odi.png', facecolor='white'); plt.close(fig)
put('odi.png', '据原文表 2 重画：第 1 个月 ODI 改善，找平练习组 12.5±14.8 分，骨盆带组 4.3±15.1 分，常规治疗组 −3.4±14.9 分（变差）。达到 ≥11 分改善的人数：练习组 9/21，骨盆带组 3/21')

# 结果图 2：即时疼痛（原文图 9 数据）
x = ['第1次\n就诊', '做完\n练习', '系上\n骨盆带', '1个月\n复诊', '做完\n练习', '系上\n骨盆带', '2个月\n复诊', '做完\n练习', '系上\n骨盆带']
d = {'找平练习组': [5.24, 2, 2, 4.19, 1.95, .95, 4, .64, .64], '骨盆带组': [4.48, 4.48, 2.33, 3.29, 1.33, 1.1, 3, 1.36, 1.36], '常规治疗组': [6.1, 6.1, 6.1, 5.55, 1.6, 1.15, 3, .61, .61]}
fig, ax = plt.subplots(figsize=(12, 6.6), dpi=100)
for (lab, ys), c in zip(d.items(), cols): ax.plot(range(9), ys, marker='o', lw=2.5, ms=8, color=c, label=lab)
for xx in (2.5, 5.5): ax.axvline(xx, color='#ccc', lw=1)
ax.set_xticks(range(9), x, fontsize=13); ax.set_ylim(0, 7.5); ax.set_ylabel('0～10 疼痛评分', fontsize=15); ax.tick_params(axis='y', labelsize=13)
ax.set_title('每次就诊：做练习、系骨盆带前后的即时疼痛', fontsize=21, pad=16); ax.legend(frameon=False, fontsize=14, ncol=3, loc='upper right')
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
ax.annotate('当场明显下降……', xy=(1, 2), xytext=(1.4, 5.6), fontsize=14, color='#2E86AB', arrowprops=dict(arrowstyle='->', color='#2E86AB'))
ax.annotate('……1 个月后又回到 4 分左右', xy=(3, 4.19), xytext=(3.3, 6.6), fontsize=14, color='#2E86AB', arrowprops=dict(arrowstyle='->', color='#2E86AB'))
fig.text(.5, .015, '第 1 个月骨盆带组、常规治疗组没有学练习，对应点沿用前值；第 2 个月起所有人都做练习＋系骨盆带', ha='center', fontsize=12, color='#555')
fig.tight_layout(rect=(0, .05, 1, 1)); fig.savefig(f'{WORK}/nrs.png', facecolor='white'); plt.close(fig)
put('nrs.png', '据原文图 9 数据重画：做完练习后 90% 的人当场疼痛减轻，但到下次复诊疼痛又回升；1 个月时三组 BPI 疼痛改善没有显著差异')
k.save(k.card('这个结果该怎么看（编者解读）', [
    ('有希望的地方', '练习组 1 个月 ODI 改善比常规治疗多 15.9 分，需治疗人数约 3 人；做完练习当场止痛率 90%\n方法便宜：一把粘了水平仪的尺子、一支记号笔；练习 2 分钟、在家能做', GR, (0, 120, 60)),
    ('要打折扣的地方', '每组只有约 20 人、单中心、只随访 2 个月；开放标签、结局全是自评\n测试的发明人就是第一作者，也是检查者之一；骨盆带由厂家免费提供', OR, (200, 120, 0)),
    ('关键问题没回答', '没有无腰痛的对照人群，不知道“骨盆一高一低”在健康人里有多常见\nSIFFT 没做正式的信度检验；“找平后就不痛”也可能是牵拉、动作本身或期望效应', PK, RED),
    ('临床怎么用', '可以当作一种低成本、低风险的自我管理尝试；先排除神经根痛和红旗征\n不要把“骨盆不平”当成腰痛的唯一解释，也不必为了找平反复做手法', LT, TEAL),
]), n); n += 1
c = k.op('f4.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = max(0, (c.height - 383) // 2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
