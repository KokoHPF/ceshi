#!/usr/bin/env python3
"""Liu、Dalmau-Pastor 等 2026 KSSTA《Lisfranc 关节复合体解剖：图解综述与手术入路》→ 小红书 3:4 图文卡片。
原文 CC BY 开放获取：用编者中文标注版原图 work/lb*.jpg 和 work/biomech.png（先运行 tools/make_figs.py 生成）。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='足踝解剖', source='KSSTA 2026;34:3178-3185', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
BONE = 'C1 内侧楔骨 · C2 中间楔骨 · C3 外侧楔骨 · Cu 骰骨 · M1～M5 第 1～5 跖骨'


def biomech_fig():
    """两项体外研究的刚度和失效载荷（据原文数字绘制，竖排版供卡片用）"""
    fig, axs = plt.subplots(2, 1, figsize=(9.6, 7.6), dpi=100)
    lig = ['背侧', '骨间', '跖侧']; col = ['#E3A21A', '#C0392B', '#1F5F8B']
    for ax, t, a, b in [(axs[0], '刚度（N/mm）', (66.3, 189.7, None), (40, 90, 62)), (axs[1], '失效载荷 / 强度（N）', (150.7, 368.8, None), (170, 449, 305))]:
        for j, ser in enumerate((a, b)):
            for i, v in enumerate(ser):
                if v is None: continue
                x = i + (j - .5) * .38; ax.bar(x, v, .36, color=col[i], alpha=1 if j == 0 else .5)
                ax.text(x, v * 1.02, f'{v:g}', ha='center', fontsize=16)
        ax.set_xticks(range(3), lig, fontsize=18); ax.set_title(t, fontsize=19, loc='left'); ax.spines[['top', 'right']].set_visible(False)
        ax.tick_params(axis='y', labelsize=13); ax.set_ylim(0, max(v for v in a + b if v) * 1.18)
    fig.text(.99, .97, '深色＝研究 A（未测跖侧）　浅色＝研究 B', ha='right', fontsize=15, color='#555')
    fig.tight_layout(rect=(0, 0, 1, .95)); return fig


img = lambda n, ext='jpg': Image.open(os.path.join(WORK, f'{n}.{ext}')).convert('RGB')

deck.cover(['Lisfranc', '关节复合体', '图解解剖'], kicker='KSSTA 2026 · 图解解剖综述',
           subtitle='骨、韧带和手术入路：6 张标本图看懂', photos=[(img('lb63').crop((40, 170, 1000, 690)), '稳定第 2 跖骨的背侧韧带（原文图 4）')],
           banner='第 2 跖骨是拱顶石 · M1–M2 之间没有韧带')
deck.text('Lisfranc 关节复合体是什么', '原文引言', [
    ('box', '不是一个关节', '跖跗关节（核心）+ 跗骨间关节 + 近端跖骨间关节 + 一圈韧带\n狭义“Lisfranc 韧带”：连接**内侧楔骨（C1）和第 2 跖骨（M2）**的背侧、骨间、跖侧三条', 'navy'),
    ('box', 'Lisfranc 损伤', '累及这些结构的骨折、脱位或单纯韧带扭伤；常伴撕脱骨折（**Fleck 征**）或 C1–M2 间隙增宽', 'teal'),
    ('box', '向近端延伸的两种亚型', '**MCD**：Lisfranc 韧带 + C1–C2 楔间韧带伤，第 1 跖跗关节韧带完好\n**PE**：再加 C1–M1、C2–M2 韧带伤，更严重', 'yellow'),
    ('box', '容易漏诊', '低能量单纯韧带伤漏诊可达 **20%** → 慢性不稳、疼痛、关节炎（最常见）、畸形', 'accent')])
deck.figure('① 骨性结构：弓形排列', '原文图 1（编者中文标注）', img('lb37'), None, [
    ('box', '横弓', '跖骨基底背侧宽、足底窄 → 背侧凸、**内侧高于外侧**的横弓；楔骨和骰骨同样排成弓形', 'teal')], max_h=820)
deck.figure('② 第 2 跖骨：嵌进去的“拱顶石”', '原文图 2 足背观（编者中文标注）', img('lb38').crop((436, 225, 1000, 635)), None, [
    ('box', '榫卯', 'M2 基底嵌在 C1 和 C3 之间，同时接触 C1、C2、C3、M1、M3\nC1、C3 分别比 M2 基底向前突出约 **8 mm** 和 **4 mm**', 'navy')], max_h=700)
deck.figure('③ 足底面看楔骨的“楔”', '原文图 3 足底观（编者中文标注）', img('lb39').crop((436, 208, 1000, 592)), None, [
    ('bul', ['关节线阶梯状错开，前后相差约 **20 mm**，最高点在 M3–C3', 'C2 的足底面很小，“楔形”最明显', 'M1、M2 基底通常不相关节；M2 对 C1 的关节面偏背侧 → **横穿 C1–M2 的螺钉可能伤软骨**'])], max_h=640)
deck.text('④ 哪些骨性形态更容易受伤', '原文 Skeletal elements', [
    ('steps', [('深度', '榫卯内侧每加深 **1 mm**，损伤可能性约降低 **50%**（外侧深度无关）'), ('长度', 'M2 长度 / 足长每降低 1%，损伤可能性 **×1.82**；<29% 时尤其易伤'),
               ('宽度', '榫卯越宽，韧带越宽，越稳定')]),
    ('box', '影像怎么看', '负重 CT 或负重 X 线：**C1–M2 间距 ≥2 mm** 提示不稳定损伤\n比 M1–M2 间距更准确、更敏感', 'accent')])
deck.figure('⑤ 关键：M1 和 M2 之间没有韧带', '原文图 4（编者中文标注）', img('lb63').crop((20, 70, 890, 950)), None, [
    ('box', '天生的薄弱点', '外侧跖骨基底之间都有背侧、跖侧韧带，唯独 **M1–M2 之间没有**，只有薄弱纤维组织\n→ C1–M2 的三条 Lisfranc 韧带成了关键', 'accent')], max_h=700)
deck.figure('⑥ 三条 Lisfranc 韧带', '原文图 5（编者中文标注，M1 已拆下）', img('lb64'), None, [
    ('steps', [('背侧', '宽梯形，**最薄最弱、最易伤**，移位多向背侧；超声可筛查'), ('骨间', '带状 1～4 束，**最强**，主要稳定结构，约为背侧的 4.5 倍大'),
               ('跖侧', '跖侧主要稳定结构；多为扇形，到 M2 和 M3')])], max_h=600)
deck.chart('⑦ 谁最强：骨间韧带', '据原文两项体外研究数字绘制', biomech_fig(), [
    ('bul', ['刚度：骨间 > 跖侧 > 背侧', '失效载荷：骨间约 369～449 N，背侧约 151～170 N', '两项研究绝对数值差约一倍，原文未解释'])])
deck.figure('⑧ 楔间韧带与两种不稳', '原文图 6（编者中文标注）', img('lb96'), None, [
    ('box', '横向不稳', '骨间 + 跖侧 Lisfranc 韧带断 → 外展应力下 C1–M2、C2–M2 都不稳', 'teal'),
    ('box', '纵向不稳', '骨间 Lisfranc 韧带 + **C1–C2 骨间韧带**断 → 内收应力下多为 C1–C2 不稳（5 个标本中 4 个）', 'yellow')], max_h=520)
deck.text('⑨ 手术解剖', '原文 Surgical anatomy', [
    ('box', '背内侧入路（最常用）', '第 1、2 跖骨间纵切口；在**拇长伸肌腱与胫前血管神经束**（足背动脉 + 腓深神经）之间进入，血管神经束拉向外侧', 'navy'),
    ('box', '背外侧入路', '累及第 3 跖跗关节或第 4、5 跖骨时加做，沿第 4 跖骨轴线；**保护腓肠神经**；两切口皮桥 **≥5 cm**', 'teal'),
    ('steps', [('1', '恢复舟骨与楔骨的关系'), ('2', 'M2 对 C2、再对 C1（复位的基石）'), ('3', '依次处理第 1、3、4、5 跖跗关节')]),
    ('box', '作者观点', '几乎都有不稳成分，非手术治疗作用很有限；解剖复位是关键', 'grey')])
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('20 mm', '跖跗关节面前后错开'), ('8 / 4 mm', 'C1 / C3 比 M2 基底前突'), ('2 mm', 'C1–M2 间距不稳阈值'), ('29%', 'M2 长度 / 足长的易伤阈值'), ('5 cm', '两切口间皮桥')]),
    ('h', '原文对不上的地方'),
    ('bul', ['说骨间韧带“最窄但最厚”，引用数据里却有宽 5.9 mm、厚 4.2 mm（宽 > 厚）', '“背内侧入路常遇内侧足背皮神经”被放在背外侧入路段落里', '两项力学研究数值相差约一倍，原文未解释']),
    ('box', '文献', 'Liu X, Hong CC, Torrent J, et al. Anatomy of the Lisfranc joint complex: An illustrated review with surgical approach. Knee Surg Sports Traumatol Arthrosc. 2026;34:3178-3185.\nCC BY 开放获取，原图引自原文，编者加中文标注', 'grey')])
deck.save(OUT)
