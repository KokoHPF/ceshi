#!/usr/bin/env python3
"""Mugalur 2026 “不牵引”髋关节后脱位复位法：中文标题卡、背景卡、六步口诀卡，原文图 1、2 按步骤两两并排配中文标签，
原文图 3、4（两例 X 线）、与传统方法对比卡、解读卡、封面。单幅图先用 prep.py 切好。
共用工具在 ../bridge-review-1/tools/bridgekit.py。用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
WORK, OUT, FM, FBOLD = sys.argv[1:5]
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('病例报告 · 《J Orthop Case Rep》2026', ['髋关节后脱位', '不用牵引也能复位？'],
               'Mugalur A.', 'J Orthop Case Rep. 2026;16(5):156-160. doi:10.13107/jocr.2026.v16.i05.7240',
               '印度卡纳塔克邦迈索尔 Bhanavi 医院骨科'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def card(t, items):
    global n; k.save(k.card(t, items), n); n += 1
def pair(a, b, name, H=560):
    ims = [Image.open(f'{WORK}/p{x}.jpg').convert('RGB') for x in (a, b)]
    ims = [i.resize((round(i.width * H / i.height), H), Image.LANCZOS) for i in ims]
    c = Image.new('RGB', (ims[0].width + ims[1].width + 12, H), 'white'); c.paste(ims[0], (0, 0)); c.paste(ims[1], (ims[0].width + 12, 0))
    c.save(f'{WORK}/{name}.jpg', quality=93); return name + '.jpg'
def two(a, b, la, lb, ca=C_NAV, cb=C_NAV):
    f = pair(a, b, 'pair' + a + b); w0 = Image.open(f'{WORK}/p{a}.jpg'); r = (w0.width * 560 / w0.height + 12) / Image.open(f'{WORK}/{f}').width
    return tags_at(k, f, [(.02, .03, la, ca), (r + .02, .03, lb, cb)])
card('为什么要找新办法（编者根据原文整理）', [
    ('髋关节后脱位', '高能量外伤所致，属于骨科急诊；后脱位比前脱位常见\n尽快复位既能止痛，也能降低股骨头缺血坏死等并发症的风险', LT, TEAL),
    ('传统方法都靠“牵引”', '1870 年 Bigelow 首次描述闭合复位，此后的 Allis、Captain Morgan、East Baltimore 抬举、Stimson 重力法等\n不管怎么改，核心都是把股骨头沿股骨轴线拉出来', OR, (200, 120, 0)),
    ('牵引的麻烦', '术者腰背负担大，患者体格壮时更难；大多需要助手\n牵引床、液压升降装置虽然省力，但费时、费设备', PK, RED),
    ('作者的新方法', '仰卧位、一个人、不牵引、不需要特殊器械，只靠一套连续的体位变化', GR, (0, 120, 60)),
])
card('六步口诀：屈—内收—内旋—外展—外旋—伸（原文）', [
    ('准备', '腰麻（蛛网膜下腔阻滞）让双下肢完全放松；也可用镇静或短时全麻\n患者仰卧在手术台或转运床上，术者站在脱位髋的对侧', LT, TEAL),
    ('握法（以左髋为例）', '右手握脚踝和足部，左手扶膝；复位右髋时两手对调', OR, (200, 120, 0)),
    ('① 屈 ② 内收 ③ 内旋', '缓慢把髋屈到最大（过屈），同时尽量内收、内旋；膝完全屈曲', GR, (0, 120, 60)),
    ('④ 外展', '保持髋过屈，慢慢把髋“拨”向外展', PU, C_NAV),
    ('⑤ 外旋 ⑥ 伸直', '保持外展，髋逐步外旋、伸直，膝同时逐渐伸直 → 复位完成', PK, RED),
])
put(two('1a', '1b', '床尾看', '侧面看'), '原文图 1a、1b  起始握法（左髋脱位）：术者站在患者右侧，右手握左踝、左手扶左膝')
put(two('1c', '1d', '① 屈 ② 内收 ③ 内旋', '侧面看', C_HI), '原文图 1c、1d  第一步：髋过屈，最大限度内收、内旋，膝完全屈曲')
put(two('2a', '2b', '④ 外展（侧面）', '床尾看', C_HI), '原文图 2a、2b  第二步：保持髋过屈，把髋拨向外展')
put(two('2c', '2d', '⑤ 外旋 ⑥ 伸直', '侧面看', C_HI), '原文图 2c、2d  第三步：保持外展，髋逐步外旋、伸直，膝同时伸直')
put(two('2e', '2f', '复位完成', '侧面看', C_OK), '原文图 2e、2f  髋、膝逐步伸直到底，复位完成')
card('两个病例（原文）', [
    ('病例 1：31 岁男性', '车祸、未系安全带；左髋痛、伸不直，下肢呈屈曲、内收、内旋畸形\n腰麻下用此法闭合复位，术中透视确认同心复位；无医源性骨折、无神经血管损伤，次日出院', LT, TEAL),
    ('病例 2：35 岁男性', '骑摩托车被汽车撞；在外院多次尝试复位失败后转来\n腰麻下用此法复位成功，无神经血管损伤，次日出院', OR, (200, 120, 0)),
    ('作者补充', '一位体格健壮、一位中等体型；都是急性、单纯后脱位', GR, (0, 120, 60)),
])
put(tags_at(k, pair('3a', '3b', 'x3', 420), [(.02, .04, '复位前', RED), (.52, .04, '复位后', C_OK)]), '原文图 3  病例 1 骨盆正位片：a 左髋后脱位，b 复位后关节同心')
put(tags_at(k, pair('4a', '4b', 'x4', 420), [(.02, .04, '复位前', RED), (.52, .04, '复位后', C_OK)]), '原文图 4  病例 2 骨盆正位片：a 左髋后脱位（外院多次复位失败），b 复位后关节同心')
card('这个方法能信几分（编者解读）', [
    ('作者说的优点', '不牵引、几乎不用力 → 术者腰背没风险；不需要助手和特殊体位，转运床上就能做\n患者、术者体格对操作影响不大', GR, (0, 120, 60)),
    ('证据很少', '只有 2 例、同一位术者；没有记录复位时间、尝试次数，也没有和其他方法对比', PK, RED),
    ('没试过的情况', '陈旧性脱位、合并骨折的脱位、人工髋关节脱位都没用过\n作者推测同样原理可用于前脱位，但未验证', OR, (200, 120, 0)),
    ('麻醉条件', '两例都在腰麻、肌肉完全松弛下完成；急诊镇静下效果如何，原文没有数据', LT, TEAL),
])
c = Image.open(f'{WORK}/pair1c1d.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = 40
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
