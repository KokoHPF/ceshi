#!/usr/bin/env python3
"""Dalmau-Pastor 等 2024 KSSTA《三角韧带恒定由四束组成》→ 小红书 3:4 图文卡片。
原文 CC BY 开放获取：用编者中文标注版原图 work/lb*.jpg（先运行 tools/make_figs.py 生成）。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='足踝解剖', source='KSSTA 2024;32:3065-3075', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
img = lambda n: Image.open(os.path.join(WORK, n + '.jpg')).convert('RGB')


def widths_fig():
    """附着宽度（据原文表 1、表 2，竖排版）"""
    fig, axs = plt.subplots(2, 1, figsize=(9.6, 7.6), dpi=100)
    for ax, t, labs, pr, di in [(axs[0], '浅层（远端均更宽）', ['胫舟束', '胫弹簧束', '胫跟束'], [4.10, 5.30, 6.31], [14.90, 7.86, 9.83]),
                                (axs[1], '深层胫距束（按起点分段）', ['前丘前部', '前丘', '后丘'], [5.98, 9.67, 9.66], [10.29, 8.84, 10.48])]:
        for i in range(3):
            ax.bar(i - .19, pr[i], .36, color='#9AA5B1'); ax.bar(i + .19, di[i], .36, color='#1F5F8B')
            ax.text(i - .19, pr[i] + .3, f'{pr[i]:g}', ha='center', fontsize=15); ax.text(i + .19, di[i] + .3, f'{di[i]:g}', ha='center', fontsize=15)
        ax.set_xticks(range(3), labs, fontsize=18); ax.set_title(t, fontsize=19, loc='left'); ax.set_ylim(0, 17)
        ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=13)
    fig.text(.99, .97, '灰＝近端（胫骨）　蓝＝远端　单位 mm', ha='right', fontsize=15, color='#555')
    fig.tight_layout(rect=(0, 0, 1, .95)); return fig


deck.cover(['三角韧带', '到底几束？', '恒定四束'], kicker='KSSTA 2024 · 32 例标本解剖',
           subtitle='舟骨、弹簧韧带、跟骨、距骨各一束', photos=[(img('lb83').crop((100, 120, 1000, 700)), '从表面看四个止点（原文图 7）')], banner='浅层三束 + 深层一束 · 深层在关节内')
deck.text('为什么要重新数', '原文引言', [
    ('box', '内侧也常受伤', '踝扭伤后 30%～40% 留下慢性疼痛，最多 33% 发展为慢性不稳\n其中**最多 40%** 合并三角韧带损伤', 'accent'),
    ('box', '描述太乱', '常用“两层六束”里就有不恒定的束，各家又陆续添加 → 累计 **16 种**\n临床报告、修复、重建时说不清伤的是哪部分', 'yellow'),
    ('box', '这篇怎么做', '32 例新鲜冷冻标本；浅层从内侧看，深层**切开下胫腓联合、从关节内看**\n上一篇从关节内看三角韧带的研究还是 1979 年', 'teal')])
deck.figure('① 浅层解剖步骤', '原文图 1（编者中文标注）', [img('lb40').crop((300, 0, 1200, 560)), img('lb40').crop((1170, 0, 2100, 560))], None, [
    ('box', '关键提醒', '剥离胫后肌腱、趾长屈肌腱腱鞘时最易**误切胫跟束**；切小腿前群肌腱时易误切胫舟束\n→ 可能是以往认为它们“不恒定”的原因', 'accent')], stack=True, max_h=440)
deck.text('② 结果：两层、四束', '原文 Results', [
    ('steps', [('胫舟束', '内踝前丘前部 → **舟骨**上内侧（前部在关节内）'), ('胫弹簧束', '前丘中部 → **弹簧韧带**（跟舟内上韧带）上缘'),
               ('胫跟束', '前丘后部 → 跟骨**载距突**上缘'), ('胫距束', '深层：前丘外侧 + 后丘 → **距骨**内侧关节面下方（关节内）')]),
    ('box', '一句话', '浅层三束长纤维、都起于前丘，在关节外；深层一束短纤维，在关节内', 'teal')])
deck.figure('③ 从表面看四个止点', '原文图 7（编者中文标注）', img('lb83').crop((0, 0, 1000, 920)), max_h=1050)
deck.figure('④ 四束全貌', '原文图 4（编者中文标注）', img('lb59').crop((980, 0, 2100, 1050)), None, [
    ('box', '看图', '①～③ 浅层三束从前到后排开；④ 是深层胫距束最后部，止于距骨后内侧结节', 'teal')], max_h=760)
deck.figure('⑤ 起点：一个在外，一个在内', '原文图 6（编者中文标注）', img('lb82').crop((500, 30, 1000, 500)), None, [
    ('box', '图中编号', '① 胫舟束　② 胫弹簧束　③ 胫跟束　④ 胫距束（深层）\n虚线：关节软骨内侧边界', 'grey'),
    ('box', '要点', '浅层三束起于内踝**内侧面**（关节外）；深层胫距束起于**外侧面**、紧贴关节软骨（关节内）', 'navy')], max_h=760)
deck.chart('⑥ 附着宽度', '据原文表 1、表 2 绘制（n = 32）', widths_fig(), [
    ('bul', ['浅层三束都是远端更宽，胫舟束最明显（4.1 → 14.9 mm），呈扇形', '深层前丘前部也向远端展开；前丘、后丘两段近似直带'])])
deck.figure('⑦ 太极图一样的距骨止点', '原文图 8（编者中文标注）', img('lb107').crop((0, 0, 2100, 900)), None, [
    ('box', '互补', '距骨内侧关节面“逗号形”前宽后窄；胫距束止点是倒逗号、**后宽前窄**', 'teal')], max_h=640)
deck.text('⑧ 临床意义', '原文讨论', [
    ('box', '统一术语', '按“连到哪块骨”命名四束，便于报告损伤和规划修复、重建', 'teal'),
    ('box', '深层可能更难愈合（作者假设）', '胫距束和胫舟束前部在**关节内、滑膜外**，类似膝前交叉韧带：断后残端可能被滑膜包裹，妨碍愈合', 'accent'),
    ('box', '但也有有利因素', '踝韧带两端距离短，不完全断裂常见；目前没有研究直接证实上述假设', 'grey'),
    ('box', '并非全新', '四束描述最早见于 1956 年；本研究用关节内外两种视角重新确认', 'navy')])
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('4 束', '胫舟、胫弹簧、胫跟（浅）+ 胫距（深）'), ('16 种', '文献中曾描述的束数'), ('40%', '踝扭伤合并三角韧带损伤（最多）'), ('32 例', '新鲜冷冻标本')]),
    ('h', '原文对不上的地方'),
    ('bul', ['说浅层“所有标本”远端更宽，表 1 胫跟束远端最小 2.36 mm，小于近端最小 4.25 mm', '说深层“近乎等宽”，表 2 前丘段远端却明显更窄（P = 0.0226）', '深层 PostC 先写“后丘”，后又写“前丘以后”']),
    ('box', '文献', 'Dalmau-Pastor M, Malagelada F, Guelfi M, et al. The deltoid ligament is constantly formed by four fascicles reaching the navicular, spring ligament complex, calcaneus and talus. Knee Surg Sports Traumatol Arthrosc. 2024;32:3065-3075.\nCC BY 开放获取，原图引自原文，编者加中文标注', 'grey')])
deck.save(OUT)
