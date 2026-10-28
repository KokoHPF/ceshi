#!/usr/bin/env python3
"""Zhang、Raguzzi 等 2026 JOSPT 系统综述与 meta 分析（肩袖相关肩痛的肩部无力）：中文标题卡、背景卡、方法卡、
原文流程图（整页区域渲染 g1.jpg，原图未改动：E=../../skills/paper-to-xhs-cards/scripts/extract_figures.py；
python3 $E src/paper.pdf work --clip 3 36 88 369 302 g1）、纳入研究卡、
据原文表 4～6 用中文重画的效应量图 4 张、作者解释卡、解读卡、封面。
共用工具在 ../bridge-review-1/tools/bridgekit.py。用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
plt.rcParams['axes.unicode_minus'] = False
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('系统综述与 meta 分析 · 《JOSPT》2026', ['肩袖相关肩痛，肩膀没劲怎么办？', '28 项研究看康复能把肌力练回来多少'],
               'Zhang B, Raguzzi IA, Dupuis F, Gianola S, Morgan-Daniel J, Roy JS, Pozzi F.', 'J Orthop Sports Phys Ther. 2026;56(2):67-84',
               '美国佛罗里达大学物理治疗系；加拿大拉瓦尔大学；意大利米兰 Galeazzi 医院 等'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1

card('为什么关注肩部无力（原文引言）', [
    ('肩袖相关肩痛（RCRSP）是什么', '一个“打包”的诊断名：肩峰下疼痛、肩峰下撞击综合征、肩袖肌腱病、非特异性肩痛、肩袖撕裂都包括在内\n不再强求把疼痛归到某一个具体结构上', LT, TEAL),
    ('无力很常见，也很要紧', '患者常说提重物、搬东西、运动时“使不上劲”\n无力越明显，功能障碍越重、抑郁越多、生活质量越差；还可能伴随肩胛骨运动改变', OR, (200, 120, 0)),
    ('但以往证据缺了一块', '指南强烈推荐主动运动，以往综述证实能改善疼痛和功能\n但没有把“肌力”单独作为结局——练完到底有没有变强、哪种练法更好，并不清楚', PK, RED),
    ('这篇想回答', '① 康复后肩部各方向肌力提高多少\n② 不同类型的力量训练、不同疗程长度，效果有没有差别', GR, (0, 120, 60)),
])
card('怎么做的（原文方法）', [
    ('检索与纳入', '7 个数据库检索到 2024 年 4 月；纳入 18 岁以上 RCRSP 患者、非手术干预至少 6 周、用测力计客观测量肌力的随机对照试验或前瞻性队列研究\n排除：只纳入全层肩袖撕裂、做过肩部手术、合并不稳／冻结肩／骨折等其他肩病', LT, TEAL),
    ('把每个研究组按干预内容分成 5 类', '力量训练组：以肌肉强化为主\n多模式组：常规治疗或标准护理，可能有主动练习，但不是专门为增强肌力设计\n单纯宣教组、假治疗／安慰剂组、自然病程组（不干预）', OR, (200, 120, 0)),
    ('关键：比的是“组内前后变化”', '不是试验组和对照组相比，而是每个研究组自己“练前 vs 练后”的标准化均数差（SMD），再按测试方向分别合并\n好处是随机试验和队列研究都能用上；代价是不能直接说哪种干预更好', PK, RED),
    ('效应量怎么读', 'SMD 0～0.49 为小，0.5～0.79 为中等，≥0.8 为大；I² 越大表示研究之间结果越不一致', PU, C_NAV),
])
put('g1.jpg', '原文图  文献筛选流程：7 个数据库共检索到 6659 篇，去重后 3260 篇，全文评估 280 篇，最终纳入系统综述 33 项、meta 分析 28 项（另 5 项因数据不完整、只报告中位数或没注明患侧未纳入合并）')
card('纳入了哪些研究（原文结果）', [
    ('33 项研究、1702 人', '91% 是随机对照试验；来自 17 个国家；女性约占一半\n一半以上（52%）用的诊断名是“肩峰下撞击综合征”；症状时长 4 个月～3.6 年', LT, TEAL),
    ('怎么测肌力', '82% 用手持测力计测等长肌力，18% 用等速测力计\n测得最多的是外旋（31 项）、内旋（25 项）、外展（18 项）', OR, (200, 120, 0)),
    ('怎么练', '疗程 6～12 周；多为一对一，每周 2～3 次，每次 20～120 分钟；55% 配有家庭练习\n每个动作 1～12 组、每组 5～30 次；27 项研究写明了训练进阶', GR, (0, 120, 60)),
    ('研究组怎么分', '力量训练 42 组、多模式 20 组、自然病程 5 组、假治疗 1 组、宣教 1 组', PU, C_NAV),
    ('质量', '随机试验中低偏倚风险 27%、有一定担忧 30%、高风险 43%（主要是测量者没设盲、分配隐藏没报告）；2 项队列研究质量均为“差”', PK, RED),
])

ZONES = [(-1, 0, '#ffffff'), (0, .5, '#f3f6f9'), (.5, .8, '#e6eef6'), (.8, 3, '#d6e4f2')]
def zones(ax, lo, hi):
    for a, b, c in ZONES: ax.axvspan(max(a, lo), min(b, hi), color=c, zorder=0)
    ax.axvline(0, color='#555', lw=1.2, zorder=1)

def forest1():
    rows = [('外旋', .56, .39, .74, 49, '78%'), ('肩胛平面上举', .48, .27, .70, 9, '35%'), ('外展', .47, .32, .63, 25, '54%'),
            ('内旋', .41, .30, .52, 37, '25%'), ('前屈', .25, .01, .49, 6, '0%'), ('内收', .14, -.21, .50, 2, '0%'), ('后伸', .05, -.25, .36, 4, '0%')]
    fig, ax = plt.subplots(figsize=(12, 7.4), dpi=100); zones(ax, -.4, 1.0); N = len(rows)
    for i, (lab, e, lo, hi, m, I2) in enumerate(rows):
        y = N - 1 - i; sig = lo > 0; c = '#1F5F8B' if sig else '#9AA5B1'
        ax.plot([lo, hi], [y, y], color=c, lw=3, zorder=3); ax.plot(e, y, 's', ms=14, color=c, zorder=4)
        ax.text(1.03, y, f'{e:.2f}（{lo:.2f}, {hi:.2f}）', va='center', fontsize=15, transform=ax.get_yaxis_transform())
        ax.text(1.40, y, f'{m} 组　I² {I2}', va='center', fontsize=14, color='#666', transform=ax.get_yaxis_transform())
    ax.set_yticks(range(N), [r[0] for r in rows][::-1], fontsize=17); ax.set_xlim(-.4, 1.0); ax.set_ylim(-.7, N - .3)
    for x, t in [(.25, '小'), (.65, '中等'), (.9, '大')]: ax.text(x, N - .45, t, ha='center', fontsize=14, color='#5a7896')
    ax.set_xlabel('练后 vs 练前的标准化均数差（SMD）', fontsize=15); ax.tick_params(axis='x', labelsize=13)
    ax.set_title('所有康复干预合并：各方向肌力都有提高（后伸、内收除外）', fontsize=19, pad=14, loc='left')
    ax.spines[['top', 'right', 'left']].set_visible(False); fig.subplots_adjust(left=.15, right=.58, top=.9, bottom=.11)
    fig.savefig(f'{WORK}/forest1.png', facecolor='white'); plt.close(fig)

def forest3(title, rows, data, path, h=None, grey_small=False):
    """data: {方向: [(est, lo, hi, n) 或 None] 与 rows 对应}"""
    dirs = ['外展', '外旋', '内旋']; N = len(rows)
    fig, axs = plt.subplots(1, 3, figsize=(13, h or 1.6 + .72 * N), dpi=100, sharey=True)
    for ax, d in zip(axs, dirs):
        zones(ax, -.7, 2.3)
        for i, v in enumerate(data[d]):
            y = N - 1 - i
            if v is None: ax.text(.8, y, '无数据', ha='center', va='center', fontsize=12, color='#aaa'); continue
            e, lo, hi, m = v; sig = lo > 0; few = grey_small and m <= 2
            c = '#1F5F8B' if sig else '#9AA5B1'
            ax.plot([lo, hi], [y, y], color=c, lw=2.6, zorder=3, alpha=.55 if few else 1)
            ax.plot(e, y, 'o' if few else 's', ms=11, color=c, zorder=4, mfc='white' if few else c, mew=2.2)
            ax.text(2.25, y + .3, f'{e:.2f}　{m}组', ha='right', va='center', fontsize=12, color='#333')
        ax.set_title(d, fontsize=17); ax.set_xlim(-.7, 2.3); ax.set_ylim(-.7, N - .3); ax.tick_params(axis='x', labelsize=12)
        ax.spines[['top', 'right', 'left']].set_visible(False); ax.tick_params(axis='y', length=0)
    axs[0].set_yticks(range(N), rows[::-1], fontsize=15); axs[1].set_xlabel('练后 vs 练前的 SMD（浅色区 0.5 以上为中等，深色区 0.8 以上为大）', fontsize=13)
    fig.suptitle(title, fontsize=19, x=.02, ha='left'); fig.tight_layout(rect=(0, 0, 1, .95)); fig.savefig(f'{WORK}/{path}', facecolor='white'); plt.close(fig)

forest1()
put('forest1.png', '据原文表 4 重画：所有干预合并后，各测试方向的组内效应量（方块为 SMD，横线为 95% 置信区间；深蓝＝置信区间不跨 0，有统计学意义）。外旋为中等效应，外展、内旋、前屈、肩胛平面上举为小效应')
forest3('按干预类型分组：有主动运动的组才有肌力提高', ['力量训练', '多模式', '单纯宣教', '假治疗／安慰剂', '自然病程'], {
    '外展': [(.58, .40, .77, 18), (.29, .03, .55, 4), (.22, -.21, .66, 1), (.14, -.22, .49, 1), (-.07, -.58, .44, 1)],
    '外旋': [(.64, .43, .86, 29), (.57, .23, .92, 16), (.09, -.35, .52, 1), (.04, -.32, .39, 1), (-.01, -.43, .41, 2)],
    '内旋': [(.47, .34, .59, 21), (.46, .22, .69, 13), None, (-.02, -.38, .33, 1), (.01, -.41, .43, 2)]}, 'forest2.png', h=5.6)
put('forest2.png', '据原文表 4 重画：力量训练组外展、外旋为中等效应，内旋为小效应；多模式组外旋中等、外展和内旋小；宣教、假治疗、自然病程组都没有效果——但后三类各只有 1～2 组，而且都是试验里的对照组')
forest3('力量训练里，哪种练法组内提高最多？（空心＝只有 1～2 组数据）',
        ['运动控制训练', '非特定力量训练', '向心训练', '离心训练', '神经肌肉电刺激', '大负荷', '小负荷', '血流限制训练', '练健侧／远处部位'], {
    '外展': [(.45, .18, .72, 4), (.45, .24, .66, 7), (.65, .33, .96, 2), (.76, .05, 1.46, 4), (.85, .27, 1.43, 1), None, None, None, None],
    '外旋': [(.45, .22, .48, 6), (.38, .19, .56, 9), (.65, .14, 1.15, 3), (1.24, .25, 2.22, 5), (.92, .48, 1.35, 2), (.33, -.07, .73, 1), (.40, .01, .79, 1), (.67, -.09, 1.43, 1), (1.13, .46, 1.80, 1)],
    '内旋': [(.41, .10, .73, 4), (.35, .15, .55, 9), None, (.32, -.05, .70, 2), (.95, .51, 1.39, 2), (.50, .10, .90, 1), (.47, .07, .86, 1), (.54, -.21, 1.30, 1), (1.24, .56, 1.92, 1)]}, 'forest3.png', grey_small=True)
put('forest3.png', '据原文表 5 重画：离心训练对外旋的组内提高最大（SMD 1.24，但 I² 高达 93%，5 组之间差异很大）；神经肌肉电刺激三个方向都是大效应，但只有 1～2 组。数据点少的结果作者自己也提醒要谨慎看')
forest3('练多久？6～12 周的效果差不多', ['6 周', '8 周', '9 周', '12 周'], {
    '外展': [(.46, .18, .74, 6), (.50, .31, .69, 9), None, (.53, .19, .88, 8)],
    '外旋': [(.55, .21, .88, 11), (.47, .31, .62, 16), (.69, .30, 1.07, 2), (.74, .37, 1.11, 17)],
    '内旋': [(.48, .25, .71, 11), (.43, .26, .60, 14), (.51, .13, .89, 2), (.41, .17, .64, 8)]}, 'forest4.png', h=4.6)
put('forest4.png', '据原文表 6 重画（纳入所有主动干预组）：6、8、9、12 周的置信区间大幅重叠，作者认为疗程长短可能不是开处方时的关键因素')
card('作者怎么解释（原文讨论）', [
    ('肌力怎么提高', '一靠神经适应，二靠肌肉肥大\n疼痛会通过肌肉抑制和废用压低出力；肩痛患者肩袖激活更低。疼痛缓解后肌力可以很快回升，早期的提高多半是神经层面的改善', LT, TEAL),
    ('为什么有人练了也没变强', '刺激性高、耐受不了足够负荷；负荷太轻或频率不够；基线越弱，提高空间越大\n另外，抗阻练习的目的不一定是增肌——也可以是给肌腱加载、促进组织愈合', OR, (200, 120, 0)),
    ('肌力≠疼痛和功能', '肌力提高不一定带来疼痛和功能改善，反之亦然——符合生物－心理－社会模式', GR, (0, 120, 60)),
    ('研究之间为什么差异大', '测力工具（手持 vs 等速）、等长 vs 等速、每次测 2～10 遍、取平均值还是峰值、是否按体重标化都不统一\n训练的频率、强度、类型、时长也各不相同', PK, RED),
])
card('这篇能信几分（编者解读）', [
    ('最大的局限：只看组内前后变化', '“练后比练前强了”里混着自然恢复、疼痛缓解、测试熟练度和均值回归；不能当作“比不练强多少”\n作者也明确说：不能用来比较哪种干预、哪种练法更好', PK, RED),
    ('“最好的练法”证据很薄', '电刺激只有 1～2 组；离心训练外旋效应大，但 5 组之间差异极大（I² 93%）；大负荷、血流限制等都只有 1 组', OR, (200, 120, 0)),
    ('无效组的样本太少', '宣教、假治疗、自然病程各只有 1～2 组，而且都是试验里的对照组，置信区间都很宽', PU, C_NAV),
    ('研究质量一般', '43% 的随机试验偏倚风险高；13 项研究没说清有没有纳入肩袖撕裂患者', LT, TEAL),
    ('能放心带走的', '有主动运动／力量训练的康复，6～12 周后肩部肌力（尤其外旋、外展、内旋）普遍有小到中等的提高', GR, (0, 120, 60)),
])
c = k.op('forest2.png'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = max(0, (c.height - 383) // 2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
