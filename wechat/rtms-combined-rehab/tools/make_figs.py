#!/usr/bin/env python3
"""古丽加克拉·艾山、白玉龙等 2020 rTMS 联合常规康复治疗桡骨远端骨折后 CRPS-I 1 例：中文标题卡、背景卡、病例卡、
原文图 1～3（原样使用，不加标注）、治疗方案卡、疗效指标图和关节活动度图（据原文正文和表 1、2 用中文重画）、机制卡、解读卡、封面。
原文期刊未标注开放许可。共用工具在 ../bridge-review-1/tools/bridgekit.py。用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('病例报告 · 《中国康复理论与实践》2020', ['桡骨远端骨折后 CRPS', '经颅磁刺激＋常规康复 3 周'],
               '古丽加克拉·艾山, 陈婵, 高天昊, 凌骏麒, 孙莉敏, 白玉龙.', '中国康复理论与实践. 2020;26(2):232-236. doi:10.3969/j.issn.1006-9771.2020.02.017',
               '复旦大学附属华山医院康复医学科'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
card('复杂区域疼痛综合征（CRPS）是什么（编者根据原文整理）', [
    ('定义', '组织损伤后继发、以肢体疼痛为主，有血管运动因素参与，累及关节、肌肉、骨骼和皮肤的综合征\nⅠ型无神经损伤，Ⅱ型有神经损伤', LT, TEAL),
    ('表现', '局部疼痛、感觉改变、皮温异常、出汗异常、水肿、皮肤颜色改变；疼痛常为撕裂或灼烧样，遇冷加重，普通止痛药效果差', OR, (200, 120, 0)),
    ('和骨折的关系', '46% 的 CRPS 由骨折诱发；桡骨远端骨折后发生率 1%～37%\n伤后 1 周内剧痛、女性是危险因素', GR, (0, 120, 60)),
    ('治疗', '物理治疗、心理治疗、药物（非甾体抗炎药、双膦酸盐、加巴喷丁等）、交感神经阻滞等，最佳方案尚无共识', PU, C_NAV),
])
card('病例：67 岁女性（原文）', [
    ('受伤和固定', '雪地摔倒双手撑地，左桡骨远端骨折；手法复位、石膏固定\n次日起左手和腕疼痛、肿胀；6 周拆石膏，骨折愈合良好，但肿胀反而加重', LT, TEAL),
    ('就诊时（拆石膏后 1 个多月）', '左手、腕明显肿胀，前臂轻度肿胀；皮肤发红，皮温 36.8 ℃，手容积 330 ml\n疼痛 VAS 8 分；肘、前臂、腕、掌指和指间关节活动均受限；改良 Barthel 指数 85 分', OR, (200, 120, 0)),
    ('检查', '上肢血管 B 超排除血栓；三相骨扫描：左肘、腕、手关节骨代谢增强\nX 线和骨密度：明显骨质疏松（腰椎 T 值 -3.2）', GR, (0, 120, 60)),
    ('诊断', '符合国际疼痛研究学会（IASP）CRPS 标准：Ⅰ型 CRPS；左桡骨远端骨折石膏外固定后', PK, RED),
])
put('x7.jpg', '原文图 1  a 左手肿胀，肤色比右手深，手指周径明显大于右侧；b X 线：左手指骨和腕骨明显骨质疏松伴退行性改变；c 三相骨扫描：左肘、左腕和左手关节骨代谢增强')
card('治疗方案（原文，共 3 周）', [
    ('药物', '塞来昔布 200 mg，每日 2 次；静脉滴注唑来膦酸 100 ml（消炎止痛、治疗骨质疏松）', LT, TEAL),
    ('rTMS：中枢', '刺激疼痛肢体对侧初级运动皮层（M1）：10～20 Hz、80%～100% 阈值\n每组 20～30 个脉冲，间歇 8～10 秒，总数 >1000 个；或用间歇性 θ 短阵快速脉冲（iTBS）', OR, (200, 120, 0)),
    ('rTMS：外周', '刺激患侧第 7 颈椎棘突旁：1 Hz、100% 阈值、连续 1200 个脉冲\n作者用意：抑制颈交感干兴奋性', GR, (0, 120, 60)),
    ('消肿', '手法淋巴引流 30 分钟，每周 3 次；抬高患肢、冷热水交替浸泡，激光、微波、超声波', PU, C_NAV),
    ('运动和作业治疗', '疼痛、水肿缓解后再开始：不引起疼痛的被动关节活动，特别注意前臂旋后和适当腕背伸\n日常生活活动训练，左手作为辅助手参与', PK, RED),
])
put('x8.jpg', '原文图 2  左手肿胀程度：入院第 1 周（左）、入院第 2 周（中）、出院后随访（右）')
put('x12.jpg', '原文图 3  握拳的关节活动度：入院第 1 周（左）、入院第 2 周（右）')
fig, axs = plt.subplots(1, 4, figsize=(13, 6), dpi=100)
for ax, (nm, a, b, unit, c) in zip(axs, [('疼痛 VAS', 8, 2, '分', '#C0392B'), ('左手容积', 330, 310, 'ml', '#2E86AB'), ('皮温', 36.8, 33.8, '℃', '#E8A200'), ('改良 Barthel 指数', 85, 100, '分', '#2E9E5B')]):
    ax.bar([0, 1], [a, b], .6, color=['#9AA5B1', c])
    for x, y in ((0, a), (1, b)): ax.text(x, y * 1.01, f'{y:g}', ha='center', va='bottom', fontsize=19)
    lo = {'左手容积': 280, '皮温': 30}.get(nm, 0); ax.set_ylim(lo, max(a, b) * (1.12 if lo == 0 else 1.03))
    ax.set_xticks([0, 1], ['治疗前', '3 周后'], fontsize=15); ax.set_title(f'{nm}（{unit}）', fontsize=17); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=12)
fig.suptitle('3 周治疗前后：疼痛、肿胀、皮温和日常生活能力', fontsize=21)
fig.text(.5, .015, '容积、皮温两图纵轴不从 0 开始；手指最肿处周径每指只减少约 0.2 cm（如示指 7.2 → 7.0 cm）', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, .93)); fig.savefig(f'{WORK}/out.png', facecolor='white'); plt.close(fig)
put('out.png', '据原文正文数据重画：疼痛从 8 分降到 2 分，日常生活能力从 85 分升到满分 100 分；肿胀减轻有限')
lab = ['肘屈伸', '前臂旋转', '腕屈伸', '腕桡尺偏', '拇指 MCP', '拇指 PIP', '示指 MCP', '示指 PIP', '中指 MCP', '中指 PIP', '环指 MCP', '环指 PIP', '小指 MCP', '小指 PIP']
pre = [87, 55, 20, 5, 25, 20, 20, 20, 25, 35, 10, 20, 5, 15]; post = [100, 90, 42, 30, 35, 45, 43, 55, 44, 60, 30, 45, 26, 30]
fig, ax = plt.subplots(figsize=(12, 7), dpi=100)
y = list(range(len(lab)))[::-1]
ax.barh([i + .2 for i in y], pre, .4, color='#9AA5B1', label='治疗前'); ax.barh([i - .2 for i in y], post, .4, color='#2E86AB', label='3 周后')
for i, a, b in zip(y, pre, post): ax.text(b + 1, i - .2, str(b), va='center', fontsize=12); ax.text(a + 1, i + .2, str(a), va='center', fontsize=11, color='#666')
ax.set_yticks(y, lab, fontsize=13); ax.set_xlabel('被动关节活动度（°）', fontsize=14); ax.set_xlim(0, 112); ax.legend(frameon=False, fontsize=14, loc='lower right')
ax.set_title('关节活动度：前臂旋转和腕关节进步最明显', fontsize=20, pad=12); ax.spines[['top', 'right']].set_visible(False)
fig.text(.5, .01, '远端指间关节（DIP）也有改善，见表 2；原文表 1 每格只有一个数，未说明是哪个方向', ha='center', fontsize=12, color='#555')
fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(f'{WORK}/rom.png', facecolor='white'); plt.close(fig)
put('rom.png', '据原文表 1、表 2 重画：治疗前后左上肢各关节被动活动度')
card('作者为什么用 rTMS（原文讨论）', [
    ('证据基础', '2014 年欧洲专家指南：对 M1 区高频（≥5 Hz）rTMS 治疗神经病理性疼痛有明确镇痛作用（A 级证据）', LT, TEAL),
    ('CRPS 的“大脑改变”', '患侧手在初级躯体感觉皮层的代表区比健侧小，与疼痛严重程度有关\n疼痛抑制运动皮层，会降低运动学习能力和康复效果', OR, (200, 120, 0)),
    ('中枢＋外周两路', 'M1 高频刺激：调节疼痛环路\nC7 棘突旁低频刺激：作者认为可抑制颈交感干，控制多汗、皮肤改变', GR, (0, 120, 60)),
    ('作者推测的机制', '调节皮层兴奋性；增加局部脑血流；促进内源性阿片、γ-氨基丁酸、脑源性神经营养因子；疼痛减轻后更能配合训练', PU, C_NAV),
])
card('这个病例能说明什么（编者解读）', [
    ('结果', '3 周后疼痛 8 → 2 分，日常生活能力 85 → 100 分，前臂旋转 55° → 90°、腕屈伸 20° → 42°', GR, (0, 120, 60)),
    ('说不清谁起作用', '同时用了塞来昔布、唑来膦酸、淋巴引流、理疗、运动和作业治疗；没有对照，无法单独评价 rTMS', PK, RED),
    ('方案不够具体', 'rTMS 参数写成范围（10～20 Hz、80%～100% 阈值，或 iTBS），看不出本例实际用了哪一种', OR, (200, 120, 0)),
    ('值得借鉴的', '骨折石膏固定后肿痛反常加重、皮温高、皮肤发红 → 要想到 CRPS；先控制疼痛和水肿，再做无痛的被动活动', LT, TEAL),
])
c = k.op('x8.jpg'); c = c.resize((round(c.width * 383 / c.height), 383)); x0 = (c.width - 900) // 2
c.crop((x0, 0, x0 + 900, 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
