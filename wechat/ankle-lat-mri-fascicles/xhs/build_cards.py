#!/usr/bin/env python3
"""Hong、Calder 等 2022 KSSTA《3D 容积 MRI 可识别踝外侧韧带各束及 LFTCL 复合体》→ 小红书 3:4 图文卡片。
原文非开放获取（ESSKA 独家授权）：原文图按原样使用、不加字，中文对照写在卡片文字里；数据图为编者据原文绘制；
卡片注明“仅供学习交流，如有侵权请联系删除”。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='足踝影像解剖', source='KSSTA 2022 · doi:10.1007/s00167-022-07275-x', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
img = lambda n: Image.open(os.path.join(WORK, n + '.jpg')).convert('RGB')


def prev_fig(w=9.6, h=6.4, cover=False):
    rows = [('ATFL 可见两束', 86.7), ('弓状纤维（双束者）', 84.6), ('弓状纤维（单束者）', 75), ('CFL–PTFL 连接', 70), ('ATFL–PTFL 连接', 63.3), ('两束间穿支动脉', 16.7)]
    fig, ax = plt.subplots(figsize=(w, h), dpi=100); N = len(rows)
    for i, (a, v) in enumerate(rows):
        y = N - 1 - i; ax.barh(y, v, .64, color='#1F5F8B' if i < 3 else ('#2E8B57' if i < 5 else '#C0392B')); ax.text(v + 1.5, y, f'{v:g}%', va='center', fontsize=20, weight='bold')
    ax.set_yticks(range(N), [r[0] for r in rows][::-1], fontsize=18); ax.set_xlim(0, 118); ax.set_xticks([]); ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.set_ylim(-.6, N + (.6 if cover else 0)); fig.tight_layout(); return fig


def size_fig():
    fig, axs = plt.subplots(2, 1, figsize=(9.6, 7.2), dpi=100)
    labs = ['上束', '下束', '单束']; col = ['#1F5F8B', '#E3A21A', '#9AA5B1']
    for ax, t, m, lo, hi in [(axs[0], '长度（mm）', [18.4, 13.2, 17.3], [10.8, 8.0, 16.7], [23.4, 16.7, 18.0]), (axs[1], '宽度（mm）', [4.7, 2.6, 5.9], [1.8, 1.4, 4.3], [6.8, 3.8, 7.8])]:
        for i in range(3):
            ax.barh(2 - i, m[i], .6, color=col[i]); ax.plot([lo[i], hi[i]], [2 - i, 2 - i], color='#333', lw=2)
            ax.text(hi[i] + .3, 2 - i, f'{m[i]:g}', va='center', fontsize=18, weight='bold')
        ax.set_yticks(range(3), labs[::-1], fontsize=18); ax.set_title(t, fontsize=19, loc='left'); ax.spines[['top', 'right']].set_visible(False)
        ax.set_xlim(0, max(hi) * 1.18); ax.tick_params(axis='x', labelsize=13)
    fig.text(.99, .97, '柱＝均值　线＝范围', ha='right', fontsize=15, color='#555'); fig.tight_layout(rect=(0, 0, 1, .95)); return fig


def fig2img(fig):
    from io import BytesIO
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['距腓前韧带', '其实有两束', '3D MRI 能分清'], kicker='KSSTA 2022 · 影像解剖研究',
           subtitle='30 个健康踝：两束、弓状纤维、韧带间连接', photos=[(fig2img(prev_fig(9.6, 5.4, cover=True)), '各结构 MRI 检出率（据原文表 1）')], banner='“微不稳”可能藏在上束里')
deck.text('为什么要分束看', '原文引言', [
    ('box', 'ATFL 分上、下两束', '**上束**：关节内，泡在滑液里，伤了可能长不好\n**下束**：关节外，经**弓状纤维**连到跟腓韧带（CFL），合称外侧腓距跟韧带复合体（LFTCL）', 'navy'),
    ('box', '“微不稳”', '上束单独损伤 → 查体不明显的轻微不稳 + 慢性前外侧踝痛\n关节镜分 4 型：Ⅰ 松弛 Ⅱ 部分撕脱 Ⅲ 完全撕脱 Ⅳ 吸收', 'accent'),
    ('box', '这篇的问题', 'MRI 上能不能分清两束、看到弓状纤维？此前没有 MRI 研究描述过弓状纤维', 'teal')])
deck.figure('① 解剖标本里长什么样', '原文图 1（原图未改动）', img('x31'), None, [
    ('box', '图中编号', '① ATFL 上束　② ATFL 下束　③ 跟腓韧带（CFL）\n④ 连接下束与 CFL 的**弓状纤维**', 'teal')], max_h=700)
deck.text('② 怎么做的', '原文方法', [
    ('steps', [('对象', '30 名无踝伤史健康志愿者，平均 26.7 岁，男 14 人'), ('扫描', '3T MRI，3D 质子密度序列，层厚 **0.5 mm**，踝中立位'),
               ('判读', '两位 20 年以上经验骨肌放射科医生独立阅片、共识'), ('看什么', 'ATFL 束数和大小、弓状纤维、韧带间连接、血管')]),
    ('box', '定位', '前瞻性先导研究，证据等级 Ⅲ', 'grey')])
deck.figure('③ MRI 上的两束', '原文图 2（原图未改动）', img('x44'), None, [
    ('box', '图中编号', '1 = 上束　2 = 下束（矢状位）\n**86.7%**（26/30）的踝可见两束', 'teal')], max_h=640)
deck.chart('④ 上束明显更大', '据原文结果绘制（双束 n = 26，单束 n = 4）', size_fig(), [
    ('bul', ['上束比下束平均**长 39%、宽 80.7%**（P < 0.001）', '4 个单束踝与上束大小相近；年龄、性别无影响'])])
deck.figure('⑤ 弓状纤维：首次在 MRI 上看到', '原文图 4（原图未改动）', img('x64'), None, [
    ('box', '图中编号', '1 = ATFL 下束　2 = **弓状纤维**　3 = 跟腓韧带', 'teal'),
    ('box', '检出率', '双束者 **84.6%**，单束者 75%', 'yellow')], max_h=620)
deck.figure('⑥ 韧带之间也相连', '原文图 5（轴位）、图 6（冠状位），原图未改动', [img('x82'), img('x84')], None, [
    ('box', '图中编号', '图 5：1 = ATFL　2 = 距腓后韧带（PTFL），检出 **63.3%**\n图 6：1 = 跟腓韧带　2 = 距腓后韧带，检出 **70%**', 'teal')], max_h=640)
deck.figure('⑦ 两束之间的穿支动脉', '原文图 7（原图未改动）', img('x86'), None, [
    ('box', '图中编号', '1 = 上束　2 = 穿支动脉　3 = 下束；5 例（16.7%）可见', 'teal'),
    ('box', '意义', '可作区分两束的标志；可能解释部分扭伤后血肿大\n来自足背动脉的跗外侧支（以往解剖研究报道来自腓动脉）', 'navy')], max_h=560)
deck.text('⑧ 临床意义（作者观点）', '原文讨论', [
    ('box', '分束诊断', 'MRI 上专门看**上束**，可能帮助诊断“查体不松、却总觉不稳”的微不稳', 'teal'),
    ('box', '能不能只修 ATFL', '弓状纤维把张力从 ATFL 传到 CFL → ATFL、CFL 都伤时，只修 ATFL 也可能恢复稳定（CFL 需断在近端、弓状纤维完好）\nMRI 上弓状纤维已断 → 可能需要同时修 CFL', 'accent'),
    ('box', '单束可能是旧伤', '有学者认为单束 = 上束伤后吸收、下束代偿肥厚', 'grey'),
    ('box', '局限', '志愿者可能有已愈合的旧扭伤；细小纤维仍可能漏看；3T MRI 不普及；仅 30 例', 'yellow')])
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('86.7%', '健康踝 MRI 可见 ATFL 两束'), ('39% / 80.7%', '上束比下束更长 / 更宽'), ('84.6%', '双束者可见弓状纤维'), ('0.5 mm', '3D MRI 层厚')]),
    ('h', '原文对不上的地方'),
    ('bul', ['单束宽 5.9 mm、上束 4.7 mm，说“相近”只因 4 例测不出差异', '说上束“所有标本”都更大，但两束长度范围重叠，未给逐例数据', '对象全是健康人，却推论“支持单独修复 ATFL”']),
    ('box', '文献 · 版权', 'Hong CC, Lee JC, Tsuchida A, et al. Individual fascicles of the ankle lateral ligaments and the lateral fibulotalocalcaneal ligament complex can be identified on 3D volumetric MRI. Knee Surg Sports Traumatol Arthrosc. 2022. doi:10.1007/s00167-022-07275-x\n原图未改动。**仅供学习交流，如有侵权请联系删除**', 'grey')])
deck.save(OUT)
