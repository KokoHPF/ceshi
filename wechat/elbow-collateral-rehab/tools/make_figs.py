#!/usr/bin/env python3
"""Kim 等 2020 肘关节内外侧副韧带术后早期康复 3 例报告：中文标题卡、病例卡、分期方案卡、原文图 1、2 配中文图注，
结果图（原文图 3 的 ROM、握力、等速肌力和表 3 的 Oxford 肘评分，用中文重画）、解读卡、封面。
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
k.save(k.title('病例报告 · 《IJERPH》2020', ['肘关节内外侧副韧带术后', '第 7 天就开始动：3 例两年随访'],
               'Kim SE, Choi YC, Lee JY.', 'Int J Environ Res Public Health. 2020;17(17):6133. doi:10.3390/ijerph17176133',
               '韩国世宗大学体育系、江陵原州大学体育系'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
T = lambda f, tags: tags_at(k, f, tags)
card('三位患者（原文表 1）', [
    ('A：39 岁女性，家庭主妇，业余游泳', '过马路摔倒、手撑地扭伤，右肘完全脱位（无骨折）；复位打石膏 4 天后再次脱位\nMRI：内侧副韧带部分撕裂、外侧副韧带和伸肌总腱完全撕裂 → 只开放修复外侧副韧带', LT, TEAL),
    ('B：60 岁女性，农民，业余羽毛球', '没有外伤，肘痛 2 年，理疗、止痛药无效，出现麻木和夜间痛\nMRI：内外侧副韧带明显退变；保守治疗 6 个月仍加重 → 关节镜下缝合修复内外侧韧带并清理', OR, (200, 120, 0)),
    ('C：17 岁男性，高中生，业余柔道', '比赛中肘部过度扭转、过伸（未完全脱位），石膏 3 周＋理疗 2 个月仍痛、没力气\n内外侧副韧带明显撕裂 → 关节镜下用掌长肌腱自体移植重建内侧副韧带', GR, (0, 120, 60)),
    ('共同点', '都不是职业运动员；术后 6 周恢复日常生活；分别在 6、8、4 个月回到原来的业余运动', PU, C_NAV),
])
card('五期康复方案（原文表 2）', [
    ('第 1 期：术后第 7 天', '长臂支具戴 6 周；可耐受范围内被动屈伸\n等长肌力练习、握力练习、肩胛骨松动', LT, TEAL),
    ('第 2 期：术后 3 周', '继续第 1 期；加被动旋前、旋后', OR, (200, 120, 0)),
    ('第 3 期：术后 6 周', '弹力带做肘和腕的屈伸（轻量肌力），由最弱的带逐步换到最强，每天 2 次', GR, (0, 120, 60)),
    ('第 4 期：术后 3 个月', '哑铃做肘腕屈伸，弹力管做旋前旋后，器械推胸、下拉等\n神经肌肉训练：站姿扶健身球、小球推墙', PU, C_NAV),
    ('第 5 期：术后 6 个月', '强化肌力，强调离心收缩；BOSU 球、健身球跪姿俯卧撑\nFlexi-bar 振动杆、药球接抛', PK, RED),
    ('怎么执行', '前 6 个月每周到中心 1～2 次，后 6 个月每月 1～2 次，其余在家练；拉伸每次 10 秒 × 6 次、每天至少 6 轮', LT, TEAL),
])
put(T('x190.jpg', [(.01, .02, 'a 脱位 X 线', C_HI), (.31, .02, 'b 被动活动度', C_NAV), (.65, .02, 'c 弹力带', C_NAV)]),
    '原文图 1  病例 A：a 右肘完全脱位的 X 线；b 术后早期被动活动度练习，戴着长臂支具，箭头示施力方向；c 术后 6 周起用弹力带做肘屈伸')
put(T('x240.jpg', [(.01, .03, 'a 振动杆', C_NAV), (.32, .03, 'b 单手扶球推墙', C_NAV), (.63, .03, 'c 双手 BOSU 俯卧撑', C_NAV)]),
    '原文图 2  神经肌肉训练（术后 3 个月起）：a Flexi-bar 振动杆；b 站姿单手扶球推墙；c 双手撑 BOSU 球俯卧撑。由稳定的 BOSU 到大球、再到最小最不稳的球逐步加难')

cols = {'A': '#2E86AB', 'B': '#E8A200', 'C': '#C0392B'}
# 结果图 1：ROM
t5 = ['6 周', '3 个月', '6 个月', '12 个月', '24 个月']
rom = {'A': [75, 105, 130, 140, 145], 'B': [50, 90, 110, 135, 140], 'C': [70, 125, 135, 135, 135]}
hrom = {'A': 145, 'B': 145, 'C': 135}
fig, ax = plt.subplots(figsize=(12, 6.6), dpi=100)
for c, ys in rom.items():
    ax.plot(range(5), ys, marker='o', lw=2.8, ms=9, color=cols[c], label=f'病例 {c}（健侧 {hrom[c]}°）')
    ax.axhline(hrom[c], color=cols[c], ls=':', lw=1.4)
for i, y in enumerate(rom['B']): ax.text(i, y - 9, str(y), ha='center', fontsize=12, color=cols['B'])
ax.set_xticks(range(5), t5, fontsize=15); ax.set_ylim(40, 155); ax.set_ylabel('肘主动屈曲活动度（°）', fontsize=15); ax.tick_params(axis='y', labelsize=13)
ax.set_title('活动度：3 个月大部分回来，6～12 个月接近健侧', fontsize=21, pad=16); ax.legend(frameon=False, fontsize=14, loc='lower right')
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
fig.text(.5, .015, '点线为各自健侧；数字标的是恢复最慢的病例 B（60 岁、退变）', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, 1)); fig.savefig(f'{WORK}/rom.png', facecolor='white'); plt.close(fig)
put('rom.png', '据原文图 3a 重画：病例 A 75°→105°→130°→140°→145°，病例 B 50°→90°→110°→135°→140°，病例 C 70°→125°→135°（与健侧相同）')

# 结果图 2：肌力占健侧百分比
t4 = ['3 个月', '6 个月', '12 个月', '24 个月']
st = {'握力': ({'A': [12, 13, 25, 27], 'B': [10, 16, 23, 25], 'C': [22, 38, 48, 51]}, {'A': 28, 'B': 25, 'C': 52}),
      '等速屈肘': ({'A': [20, 30, 48, 53], 'B': [18, 21, 33, 48], 'C': [50, 72, 78, 80]}, {'A': 58, 'B': 50, 'C': 80}),
      '等速伸肘': ({'A': [18, 22, 35, 42], 'B': [15, 20, 30, 36], 'C': [32, 49, 52, 56]}, {'A': 46, 'B': 39, 'C': 57})}
fig, axs = plt.subplots(1, 3, figsize=(13, 6.4), dpi=100, sharey=True)
for ax, (nm, (d, h)) in zip(axs, st.items()):
    ends = []
    for c, ys in d.items():
        p = [round(y / h[c] * 100) for y in ys]
        ax.plot(range(4), p, marker='o', lw=2.6, ms=8, color=cols[c], label=f'病例 {c}'); ends.append([p[-1], c])
    ends.sort(reverse=True)
    for i in range(1, 3): ends[i][0] = min(ends[i][0], ends[i - 1][0] - 4.5)
    for i, (y, c) in enumerate(ends):
        ax.text(3.12, y, f'{round(d[c][-1] / h[c] * 100)}%', fontsize=12, color=cols[c], va='center')
    ax.axhline(100, color='#333', ls='--', lw=1); ax.axhline(90, color='#999', ls=':', lw=1)
    ax.set_xticks(range(4), t4, fontsize=12); ax.set_title(nm, fontsize=18); ax.set_xlim(-.3, 3.7)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
axs[0].set_ylabel('占健侧的百分比（%）', fontsize=15); axs[0].set_ylim(20, 110); axs[0].legend(frameon=False, fontsize=13, loc='lower right')
fig.suptitle('肌力：6 个月还差不少，12～24 个月才接近健侧', fontsize=21)
fig.text(.5, .015, '编者按原文图 3 的数值除以图注给出的健侧值计算；虚线 100%、点线 90%', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, .95)); fig.savefig(f'{WORK}/str.png', facecolor='white'); plt.close(fig)
put('str.png', '据原文图 3b～d 重画：等速肌力从术后 3 个月才开始测。6 个月时病例 A、B 的握力只有 13、16 kg，分别是健侧的 46%、64%；24 个月时三人都在健侧的 90% 以上')

# 结果图 3：OES
oes = {'A': [7, 12, 22, 30, 44], 'B': [4, 9, 22, 34, 43], 'C': [10, 22, 30, 42, 46]}
fig, ax = plt.subplots(figsize=(12, 6.4), dpi=100)
for c, ys in oes.items():
    ax.plot(range(5), ys, marker='o', lw=2.8, ms=9, color=cols[c], label=f'病例 {c}')
    ax.text(4.1, ys[-1], str(ys[-1]), fontsize=13, color=cols[c], va='center')
ax.axhline(48, color='#333', ls='--', lw=1); ax.text(0, 49.2, '满分 48（正常肘）', fontsize=13, color='#333')
ax.set_xticks(range(5), t5, fontsize=15); ax.set_ylim(0, 52); ax.set_xlim(-.3, 4.5); ax.set_ylabel('Oxford 肘评分（0～48，越高越好）', fontsize=15)
ax.tick_params(axis='y', labelsize=13); ax.set_title('日常功能和疼痛：6 周时还很差，12～24 个月才明显好转', fontsize=20, pad=16)
ax.legend(frameon=False, fontsize=14, loc='upper left', bbox_to_anchor=(0, .92)); ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
fig.tight_layout(); fig.savefig(f'{WORK}/oes.png', facecolor='white'); plt.close(fig)
put('oes.png', '据原文表 3 重画：Oxford 肘评分 12 题、每题 0～4 分。术后 6 周三人只有 4～10 分，虽然已“回到日常生活”，其实还很不方便；24 个月时 43～46 分')
card('这 3 例能说明什么（编者解读）', [
    ('时间线可以参考', '6 周回日常 → 约 3 个月活动度基本回来 → 约 6 个月肌力有起色 → 4～8 个月回业余运动 → 2 年肌力在健侧 90% 以上\n没有再脱位、不稳等并发症', GR, (0, 120, 60)),
    ('早期练什么', '第 7 天开始被动屈伸，旋前旋后推迟到 3 周（怕内外翻应力）；等长收缩、握力、肩胛骨练习一开始就做\n抗阻屈伸 6 周、旋转抗阻和神经肌肉训练 3 个月', LT, TEAL),
    ('证据很弱', '只有 3 例、没有对照；性别、年龄、伤因、术式（开放修复、镜下修复、镜下重建）各不相同\n大部分在家练，练习频率没记录；说不清“早期”比“晚期”好多少', PK, RED),
    ('别直接照搬', '方案参考的主要是投掷运动员内侧副韧带的指南；具体何时动、动多少，以手术医生对修复强度的判断为准', OR, (200, 120, 0)),
])
c = k.op('x240.jpg'); c = c.resize((900, round(c.height * 900 / c.width)))
c = c.crop((0, 0, 900, min(383, c.height))); bg = Image.new('RGB', (900, 383), 'white'); bg.paste(c, (0, (383 - c.height) // 2)); bg.save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
