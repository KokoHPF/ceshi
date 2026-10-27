#!/usr/bin/env python3
"""Bao、Wang 2024 正骨手法联合神经肌肉电刺激治疗腰椎间盘突出 1 例：中文标题卡、背景卡、病例卡，原文图 1～8 配中文图注
（图 2、8 加中文动作标签，其余原样；影像设备参数保留原样），治疗思路卡、治疗方案卡、
活动度对比图（据原文表 1、2 用中文重画）、解读卡、封面。原文 CC BY。
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
k.save(k.title('病例报告 · 《Frontiers in Rehabilitation Sciences》2024', ['久坐上班族腰椎间盘突出', '正骨手法＋神经肌肉电刺激 1 例'],
               'Bao Y, Wang Z.', 'Front Rehabil Sci. 2024;5:1465623. doi:10.3389/fresc.2024.1465623',
               '大连市第四人民医院康复医学科、大连理工大学附属中心医院脊柱外科'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
POS = [(.02, .03, '前屈', C_NAV), (.52, .03, '后伸', C_NAV), (.02, .52, '左侧屈', C_NAV), (.52, .52, '右侧屈', C_NAV)]
card('为什么关注上班族腰痛（编者根据原文整理）', [
    ('越来越常见', '2006～2016 年腰痛发病增加 18%；成年人一生中约 80% 会腰痛\n不少上班族每天坐 8 小时以上，腰痛发生率 25%～51%', LT, TEAL),
    ('久坐的问题', '髂腰肌等维持坐姿的肌肉缩短，臀肌、竖脊肌、多裂肌相对无力 → 肌肉失衡', OR, (200, 120, 0)),
    ('作者的理论框架', '冯天有“新医正骨”：椎间盘、小关节、韧带构成脊柱“内平衡”，周围肌肉构成“外平衡”\n劳损或退变后，一次扭闪就可能造成椎体“位移”，内外平衡都被打破', GR, (0, 120, 60)),
    ('作者的设想', '先放松肌肉 → 再用正骨手法纠正“椎体位移” → 最后练肌力，维持内外平衡', PU, C_NAV),
])
card('病例：33 岁女性，白领（原文）', [
    ('病史', '长期伏案；3 个月前久坐后腰痛，就诊前一天搬重物后加重\n弯腰受限，伴下肢放射痛；之前吃药、按摩、理疗只能暂时缓解', LT, TEAL),
    ('查体', '左侧腰椎棘突旁压痛，左侧腰肌痉挛；直腿抬高试验阳性\n双下肢皮肤感觉、肌力正常', OR, (200, 120, 0)),
    ('评分', '腰痛 VAS 6 分；日本骨科协会（JOA）腰椎评分 19 分\n前屈 45°、后伸 10°、右侧屈 15°', GR, (0, 120, 60)),
    ('诊断', '① 腰肌劳损　② 腰椎间盘突出（L3/4、L4/5、L5/S1）', PK, RED),
])
put('x24.jpg', '原文图 1  MRI（上）示 L3/4、L4/5、L5/S1 椎间盘突出，压迫硬膜囊；CT（下）提示后纵韧带钙化')
put(tags_at(k, 'x41.jpg', POS), '原文图 2  治疗前的姿势和活动度评估：前屈、后伸、侧屈都明显受限')
put('x46.jpg', '原文图 3  腰椎正位片：棘突连线不居中，作者认为提示椎体有旋转（橙色竖线为原图所画的中线参考）')
put('x58.jpg', '原文图 4  腰椎侧位片：椎体边缘骨赘形成（放大圈），作者认为这是增加椎体稳定性的代偿')
card('治疗方案（原文）', [
    ('① 先放松：神经肌肉电刺激', '“解痉”模式缓解竖脊肌痉挛；电极贴在两侧竖脊肌肌腹\n每天 1～2 次，每次约 20 分钟；配合腰肌牵伸', LT, TEAL),
    ('② 再复位：脊柱（定点）旋转复位法', '把患者重心移到“错位”的小关节上，让脊柱暂时失稳\n术者拇指直接推顶偏歪的棘突，借牵拉和旋转力把椎体推回原位', OR, (200, 120, 0)),
    ('③ 后强化：电刺激同步肌力训练', '每周 3～5 次、共 4 周；腰腹肌训练时在收缩期同步电刺激\n瑜伽球背伸、动态瑜伽球平板支撑等核心训练，最后放松按摩', GR, (0, 120, 60)),
    ('④ 健康教育', '尽早复工；避免久坐久站、搬重物和扭腰；定时起身活动、用有靠背的椅子\n搬东西时屈髋屈膝、背挺直、收紧腹部；睡中等硬度床垫', PU, C_NAV),
])
put('x63.jpg', '原文图 5  神经肌肉电刺激：电极贴在两侧竖脊肌肌腹')
put('x78.jpg', '原文图 6  左侧腰肌痉挛')
put('x88.jpg', '原文图 7  正骨手法使用的复位椅')
put(tags_at(k, 'x83.jpg', POS), '原文图 8  治疗后的活动度评估：前屈、后伸、侧屈明显改善')
fig, ax = plt.subplots(figsize=(12, 6.4), dpi=100)
labs = ['前屈\n（正常 90°）', '后伸\n（正常 30°）', '左侧屈\n（正常 30°）', '右侧屈\n（正常 30°）']; pre = [45, 10, 25, 15]; post = [80, 30, 25, 25]; x = range(4)
ax.bar([i - .2 for i in x], pre, .4, color='#9AA5B1', label='治疗前'); ax.bar([i + .2 for i in x], post, .4, color='#2E86AB', label='随访')
for i in x:
    ax.text(i - .2, pre[i] + 1.5, f'{pre[i]}°', ha='center', fontsize=17); ax.text(i + .2, post[i] + 1.5, f'{post[i]}°', ha='center', fontsize=17)
ax.set_xticks(list(x), labs, fontsize=15); ax.set_ylim(0, 100); ax.set_ylabel('腰椎活动度（°）', fontsize=16); ax.tick_params(axis='y', labelsize=14)
ax.set_title('腰椎活动度：治疗前 vs 随访（疼痛 VAS 6 → 0）', fontsize=21, pad=14); ax.legend(frameon=False, fontsize=16)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
fig.text(.5, .015, '原文表 1 有“旋转”一栏，但没有给出数值', ha='center', fontsize=13, color='#555')
fig.tight_layout(rect=(0, .05, 1, 1)); fig.savefig(f'{WORK}/rom.png', facecolor='white'); plt.close(fig)
put('rom.png', '据原文表 1、2 重画：前屈 45°→80°、后伸 10°→30°、右侧屈 15°→25°，左侧屈不变；作者报告 3 次治疗后腰部压痛和痉挛消失，1 年随访未复发')
card('这个病例能说明什么（编者解读）', [
    ('作者的结论', '电刺激放松 → 正骨复位 → 电刺激同步肌力训练，能快速缓解上班族椎间盘突出的腰痛，1 年未复发', GR, (0, 120, 60)),
    ('证据很弱', '只有 1 例、没有对照；电刺激、正骨、核心训练、健康教育同时用，说不清谁起作用\n入院时测了 JOA 评分，治疗后却没有报告', PK, RED),
    ('理论需谨慎看待', '“椎体位移”和“内外平衡”是作者所采用的冯天有新医正骨理论；X 线棘突不居中能否代表“错位”、手法是否真把椎体推回原位，原文没有影像对比', OR, (200, 120, 0)),
    ('可以借鉴的', '先缓解肌肉痉挛再做手法；后期电刺激配合主动收缩练核心；把久坐、搬重物的习惯纳入健康教育', LT, TEAL),
])
c = k.op('x83.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = 80
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
