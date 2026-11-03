#!/usr/bin/env python3
"""溝田・壇 2025《足関節果部骨折に対する機能解剖学に基づく理学療法》→ 小红书 3:4 图文卡片。
原文非开放获取（©医学書院）：原文图按版面原样截取（work/fig*.jpg），只裁切面板、不改动图像；中文说明写在卡片文字里。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='踝关节康复', source='理学療法ジャーナル 2025;59(5):572-587', fonts_dir=FONTS)
G = lambda n, box=None: (lambda im: im.crop(box) if box else im)(Image.open(os.path.join(WORK, f'{n}.jpg')).convert('RGB'))

deck.cover(['踝关节骨折后', '背屈受限怎么查、怎么治'], kicker='理学療法ジャーナル 2025 · 特集',
           subtitle='从功能解剖出发，别漏了拇长屈肌', photos=[(G('fig2', (0, 0, 535, 540)), '背屈时触诊距骨滑车（原文图 2a）')], banner='学习笔记 · 仅供学习交流')
deck.text('先说结论', '原文要点', [
    ('box', '背屈很重要', '步行、起立、下蹲都要用；踝关节骨折约 **20%** 疗效不佳，背屈受限是相关因素', 'navy'),
    ('box', '正常背屈两件事', '非负重：距骨滑车**嵌入踝穴**，距骨内侧结节**向后突出**\n负重：距下 / Chopart 关节**外翻**、内侧纵弓下降', 'teal'),
    ('box', '别漏了 FHL', '拇长屈肌走在距骨后方，是背屈受限的重要因素', 'accent'),
    ('box', '方法', '把骨折、韧带、手术、免负重 / 固定对功能的影响逐层理清', 'yellow')])
deck.figure('① 背屈：距骨滑车嵌入踝穴', '原文图 1a、b（尸体标本）', G('fig1ab'), None, [
    ('steps', [('a 跖屈', '距骨滑车向前突出（橙圈），与踝穴间有间隙'), ('b 背屈', '距骨滑车嵌入踝穴并被锁定')]),
    ('box', '转折点', '约**跖屈 27.1±2.3°**；再往背屈走，距骨把下胫腓关节向外撑开', 'teal')], max_h=780)
deck.figure('② 嵌入后：距骨还要往后走', '原文图 1c（X 线）', [G('fig1c12'), G('fig1c3')], None, [
    ('box', '③ 继续背屈', '距骨内侧结节向后突出，胫骨后下缘与跟骨结节距离拉长（橙线）', 'navy'),
    ('box', '所以', '后方的 **FHL 要够软**，**跟腱要能向远端滑动**', 'accent')], stack=True, max_h=820)
deck.figure('③ 触诊：前方看距骨滑车', '原文图 2a', G('fig2', (0, 0, 1709, 540)), None, [
    ('steps', [('位置', '第三腓骨肌腱与外踝之间（蓝箭头）'), ('跗骨窦', '外踝下端前方约 2 横指（黄箭头）'), ('评估', '跖屈 27° 以下更好摸；背屈时它能否**顺畅嵌入踝穴**')])], max_h=520)
deck.figure('④ 触诊：后方看距骨内侧结节', '原文图 2b', G('fig2', (0, 540, 1190, 1601)), None, [
    ('box', '位置', '跟腱正前方，FHL（红线）与趾长屈肌腱（蓝线）之间（黑箭头）', 'navy'),
    ('box', '评估', '正常背屈时手指被**向后推出**；超声下胫骨后下缘（黄）与内侧结节（粉）距离变长', 'teal')], max_h=760)
deck.figure('⑤ 负重背屈：外翻 + 降足弓', '原文图 3a、b', G('fig3ab'), None, [
    ('box', '发生了什么', '距骨外侧突与跟骨沟外侧部相接、**跗骨窦闭合**：小腿内旋，距下 / Chopart 关节外翻，足弓下降', 'navy'),
    ('box', '需要什么', '足长变长 → 足底腱膜、拇展肌、拇短屈肌要够软', 'teal'),
    ('box', '图中日文', '立位＝站立位　荷重位背屈＝负重背屈', 'grey')], max_h=620)
deck.figure('⑥ 外翻时距骨在跟骨上内旋', '原文图 3c 内翻 / 3d 外翻（CT）', G('fig3cd'), None, [
    ('steps', [('① 内侧观', '外翻时载距突与舟骨结节间变宽，距骨头贴住跟舟足底韧带'), ('② 外侧观', '跗骨窦闭合'), ('③ 足底观', '距骨头与跟舟足底韧带相接')])], max_h=700)
deck.figure('⑦ 触诊：外翻', '原文图 4', G('fig4'), None, [
    ('box', 'a 跗骨窦', '内翻位指尖能伸进去；外翻位距骨跖屈、内旋，指尖被推出', 'navy'),
    ('box', 'b 舟骨结节', '内翻位舟骨靠近内踝；外翻位离开内踝', 'teal')], max_h=760)
deck.figure('⑧ 拇长屈肌（FHL）的走行', '原文图 5（左踝后面观，尸体标本）', G('fig5'), None, [
    ('steps', [('a', '起于腓骨后缘（箭头）'), ('b', '走在距骨内侧结节与后外侧结节之间'), ('c', 'FHL 腱在距骨后方 → 限制距骨向后下方滑动')]),
    ('box', '还会怎样', '周围脂肪多（属 Kager 脂肪垫），外伤和制动易致滑动障碍；可与趾长屈肌、足底方肌相连', 'accent')], max_h=560)
deck.figure('⑨ FHL 柔韧性检查', '原文图 6 · FHL excursion test', G('fig6'), None, [
    ('steps', [('1', '屈膝 90°，踝关节最大背屈'), ('2', '固定第 1 跖骨头，不让它跖屈'), ('3', '伸拇趾，测与足底的夹角')]),
    ('box', '判定', '**<20°** 为 FHL 柔韧性下降', 'accent'),
    ('box', '小腿三头肌', '伸膝背屈：腓肠肌内侧头 > 外侧头 > 比目鱼肌；屈膝时比目鱼肌为主 → 两种膝位都要测', 'teal')], max_h=640)
deck.rows('⑩ 骨折会连带伤到谁', '原文表 1（编者中译）', [
    ('外踝 · 韧带', '距腓前 / 后、跟腓韧带；下胫腓前韧带', '限制内翻；稳定胫腓关节', 'navy'),
    ('外踝 · 肌腱', '腓骨长肌、腓骨短肌', '足外翻', 'navy'),
    ('内踝', '三角韧带；胫骨后肌、趾长屈肌', '限制外翻；跖屈、内翻', 'teal'),
    ('后踝', '下胫腓后韧带；拇长屈肌', '稳定胫腓关节；跖屈、屈拇趾', 'accent')],
    note='外踝外下方是腓骨长短肌腱、内踝内下方是胫骨后肌和趾长屈肌腱（原文图 7）。损伤后：主要功能受限，软组织柔韧性和滑动变差 → 加重活动受限')
deck.figure('⑪ 病例：外踝骨折', '原文图 8', G('fig8'), None, [
    ('box', '病例', '20 多岁女性；Danis-Weber B、Lauge-Hansen SER-2；合并下胫腓前韧带损伤（b 低回声、纤维不规则）', 'navy'),
    ('box', '术后 60 天', '下楼痛在踝前外侧，NRS 4/10；免负重 21 天、固定 14 天', 'teal'),
    ('box', '核心推理（见下页）', '下胫腓不稳 → 腓骨肌紧张 + **FHL 代偿性紧张** → 距骨嵌不进、后不去，足弓降不下 → 背屈受限、前方挤压痛', 'accent')], max_h=560)
deck.figure('⑫ 病态一层层理清', '原文图 11（编者中文重绘）', (lambda im: im.crop((0, 60, im.width, im.height)))(G('flow')), None, [], max_h=1120)
deck.figure('⑬ 治疗：松解 FHL 与腓骨肌', '原文图 12a', G('fig12a'), None, [
    ('steps', [('①', '在比目鱼肌深层找到 FHL'), ('②', '手指插入 FHL 与腓骨短肌之间，内外移动（黄箭头）'), ('③', '压住 FHL、被动伸趾，从前向后推距骨（白箭头）')]),
    ('box', '同时', '贴扎稳定下胫腓关节', 'teal')], max_h=640)
deck.figure('⑭ 治疗：足底与负重位', '原文图 12b–d', G('fig12bcd'), None, [
    ('steps', [('b', '固定跖骨头伸趾：牵伸 FHL、趾长屈肌、足底腱膜'), ('c', '负重背屈，推距骨向后，强调内旋 + 外翻、降足弓'), ('d', '负重伸拇趾后前倾小腿')])], max_h=760)
font_manager.fontManager.addfont(os.path.join(FONTS, 'NotoSansSC-Medium.otf')); plt.rcParams['font.family'] = font_manager.FontProperties(fname=os.path.join(FONTS, 'NotoSansSC-Medium.otf')).get_name()
import numpy as np
items = ['非负重\n伸膝背屈', '非负重\n屈膝背屈', '负重背屈', '外翻', '拇趾伸展角']; v = [(10, 2, 7), (21, 10, 17), (47, 23, 38), (10, -3, 6), (23, 5, 16)]
fig, ax = plt.subplots(figsize=(9.6, 5.6), dpi=100); x = np.arange(5); w = .27
for j, (lab, c) in enumerate([('健侧', '#9aa5b1'), ('治疗前', '#e4572e'), ('治疗后', '#17807e')]):
    bars = ax.bar(x + (j - 1) * w, [t[j] for t in v], w, label=lab, color=c)
    for r, val in zip(bars, [t[j] for t in v]): ax.text(r.get_x() + r.get_width() / 2, val + (1 if val >= 0 else -6), str(val), ha='center', fontsize=16)
ax.set_ylim(-10, 60); ax.set_xticks(x); ax.set_xticklabels(items, fontsize=17); ax.axhline(0, color='#333', lw=1)
ax.legend(fontsize=17, frameon=False, ncol=3, loc='upper right'); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=15); fig.tight_layout()
deck.chart('⑮ 结果：2 周、2 次治疗', '原文表 2（单位：°）', fig, [
    ('box', '疼痛', '前方痛 **NRS 4 → 1**；出现后方牵拉感 → 背屈接近正常运动，需继续牵伸 FHL、比目鱼肌', 'teal')])
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('27°', '距骨滑车开始嵌入踝穴的跖屈角'), ('<20°', 'FHL excursion test 阳性'), ('20%', '踝关节骨折疗效不佳比例')]),
    ('h', '原文对不上的地方'),
    ('bul', ['FHL 试验引文献 16（腱鞘炎研究），方法学论文其实是文献 15', '“果間関節窩 / 果関節窩”“内側結節 / 内側突起”混用', '文献 14 应为 J Anat 第 230 卷，原文写 30']),
    ('box', '文献与版权', '溝田丈士, 壇 順司. 理学療法ジャーナル. 2025;59(5):572-587. © 医学書院，非开放获取；原图未改动\n仅供学习交流，如有侵权请联系删除', 'grey')])
deck.save(OUT)
