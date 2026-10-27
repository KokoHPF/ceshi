#!/usr/bin/env python3
"""Bell、Chinchalkar、Faber 2010 多发腕掌关节骨折脱位术后康复 1 例：中文标题卡、背景卡、原文图 1～6 配中文图注（原图未改动；图片内嵌图像提取后是反色，改用整页区域渲染 g1～g6.jpg：
E=../../skills/paper-to-xhs-cards/scripts/extract_figures.py；python3 $E src/paper.pdf work --clip 1 39 53 545 238 g1，
1 39 267 280 399 g2，1 39 429 280 582 g3，1 304 268 545 432 g4，2 304 54 545 190 g5，2 40 531 545 723 g6），
时间线卡（原文表 1）、康复方案卡、握力恢复图（据原文表 1 用中文重画）、解读卡、封面。
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
k.save(k.title('病例报告 · 《Can J Plast Surg》2010', ['手部多发腕掌关节骨折脱位', '术后怎么康复：腕掌支具＋早期活动'],
               'Bell T, Chinchalkar SJ, Faber K.', 'Can J Plast Surg. 2010;18(3):e37-e40',
               '加拿大安大略省伦敦市 St Joseph’s 医疗中心手与上肢中心'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
card('为什么关注这种损伤（编者根据原文整理）', [
    ('少见', '腕掌关节（CMC，掌骨底与远排腕骨之间）韧带坚强、骨性咬合紧密，很难脱位；第 2～5 指同时骨折脱位更少见', LT, TEAL),
    ('多由高能量外伤引起', '大多是车祸；脱位方向多为背侧；闭合复位常复位不了或再脱位，首选手术', OR, (200, 120, 0)),
    ('预后（Prokuski 等 10 例，最大的病例系列）', '一半无痛，其余活动相关轻痛；6 个月握力为健侧的 50%～90%\n6 人活动度完全恢复；3 人后期需要关节融合；5 人回到原工作', GR, (0, 120, 60)),
    ('康复的难题', '长期制动 → 关节僵硬、肌腱粘连、手内在肌无力\n但腕掌关节又需要保护——作者用一种新的环形腕掌支具来平衡两者', PK, RED),
])
put('g1.jpg', '原文图 1  左手正位（A）和侧位（B）X 线：示指、中指、环指、小指腕掌关节向背侧脱位，伴第 3 掌骨和大多角骨骨折')
put('g2.jpg', '原文图 2  闭合复位后：A 正位，B 斜位，C 侧位——没能达到满意复位')
put('g3.jpg', '原文图 3  切开复位内固定后：经手背横切口，小多角骨用 2 枚小螺钉固定，腕掌关节用 7 根克氏针维持复位')
card('治疗时间线（原文表 1 及正文）', [
    ('第 0 周', '28 岁男性，左利手，车祸致左手多发腕掌关节骨折脱位；闭合复位失败，当天切开复位克氏针内固定', LT, TEAL),
    ('第 0～6 周', '中立位短臂夹板 2 周 → 短臂管型石膏 4 周', OR, (200, 120, 0)),
    ('第 6 周', '拆石膏，做掌侧热塑夹板\n腕伸/屈 30°/40°，掌指关节伸/屈 15°/25°，指间关节活动正常', GR, (0, 120, 60)),
    ('第 8 周', '拔克氏针，开始手治疗：屈指手套＋环形腕掌支具\n腕伸/屈 45°/45°，掌指关节 10°/65°', PU, C_NAV),
    ('第 10 周', '掌指、指间关节活动度完全恢复', LT, TEAL),
    ('第 12 周', '停支具，开始腕和握力训练；握力 左 24 kg／右 55 kg', OR, (200, 120, 0)),
    ('第 16 周 → 约第 26 周', '握力 35/50 kg → 46/54 kg；腕、掌指、指间关节活动度全部恢复', PK, RED),
])
put('g4.jpg', '原文图 4  术后第 6 周：切口愈合良好，针道清洁（克氏针第 8 周拔除）')
put('g5.jpg', '原文图 5  环形腕掌稳定支具：从掌骨头包到桡腕关节，牢牢托住腕掌关节，同时不妨碍腕和手指活动')
card('康复方案（原文）', [
    ('支具怎么戴', '拆石膏后全天佩戴环形腕掌支具；早期减少腕掌关节受力，后期握力训练时提供环形支撑，减少平移和旋转应力', LT, TEAL),
    ('每次治疗的流程', '10 分钟水疗 → 主动、被动活动度评估 → 活动度练习 → 戴支具做伸肌、屈肌腱滑动和抗阻练习', OR, (200, 120, 0)),
    ('练什么', '轻柔的被动腕、掌指、指间关节活动＋肌腱滑动练习；先单关节、再复合动作', GR, (0, 120, 60)),
    ('屈指手套', '清醒时每次 5～10 分钟，被动牵伸手指', PU, C_NAV),
    ('复查和进阶', '手治疗师每两周复查；第 12 周停支具，开始腕和握力强化', PK, RED),
])
put('g6.jpg', '原文图 6  伤后 10 周的活动度：A、B 握拳时腕屈曲和背伸，C 腕和手指完全伸直')
fig, ax = plt.subplots(figsize=(12, 6.4), dpi=100)
wk = [12, 16, 26]; L = [24, 35, 46]; R = [55, 50, 54]; x = range(3)
ax.bar([i - .18 for i in x], L, .36, color='#C0392B', label='患侧（左手，利手）'); ax.bar([i + .18 for i in x], R, .36, color='#9AA5B1', label='健侧（右手）')
for i in x:
    ax.text(i - .18, L[i] + 1, f'{L[i]}', ha='center', fontsize=17); ax.text(i + .18, R[i] + 1, f'{R[i]}', ha='center', fontsize=17)
    ax.text(i, 63, f'患侧为健侧的 {round(L[i] / R[i] * 100)}%', ha='center', fontsize=16, color='#C0392B')
ax.set_xticks(list(x), ['第 12 周\n（停支具、开始强化）', '第 16 周', '约第 26 周\n（11 月 14 日）'], fontsize=15)
ax.set_ylim(0, 70); ax.set_ylabel('握力（kg）', fontsize=16); ax.tick_params(axis='y', labelsize=14)
ax.set_title('握力恢复：强化训练开始后约 3 个半月到健侧的 85%', fontsize=20, pad=14); ax.legend(frameon=False, fontsize=15, loc='upper left', bbox_to_anchor=(0, .9))
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); fig.tight_layout(); fig.savefig(f'{WORK}/grip.png', facecolor='white'); plt.close(fig)
put('grip.png', '据原文表 1 重画：握力用握力计测量。注意患侧本来是利手，正常情况下应略强于对侧')
card('这个病例能说明什么（编者解读）', [
    ('作者的观点', '多发腕掌关节骨折脱位术后，用环形腕掌支具保护腕掌关节，同时尽早活动腕、掌指和指间关节，可以减少长期制动的并发症', GR, (0, 120, 60)),
    ('但这例并不“早”', '作者团队没有参与早期处理，患者石膏固定了 6 周、第 8 周才开始手治疗——作者自己也说固定时间比理想的长', PK, RED),
    ('证据很弱', '只有 1 例、没有对照，也没有疼痛、功能评分和长期随访；说不清支具本身起了多大作用', OR, (200, 120, 0)),
    ('可以借鉴的', '保护“受伤的关节”、放开“没受伤的关节”：支具只包腕掌关节，腕和手指照常练', LT, TEAL),
])
c = k.op('g5.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = max(0, (c.height - 383) // 2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
