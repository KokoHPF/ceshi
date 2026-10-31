#!/usr/bin/env python3
"""He、Zhou 等 2022 J Foot Ankle Res《三维 CT 骨折线图结合解剖测量的第五跖骨基底撕脱骨折分型》→ 小红书 3:4 图文卡片。
原文 CC BY 4.0：用编者中文标注版原图 work/lb*.jpg（先运行 tools/make_figs.py 生成）。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='足踝骨折', source='J Foot Ankle Res 2022;15:65', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
img = lambda n: Image.open(os.path.join(WORK, n + '.jpg')).convert('RGB')


def count_fig():
    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=100)
    lab = ['Ⅰ 型\n跖腱膜外侧束', 'Ⅱ 型\n腓骨短肌', 'Ⅲ 型\n两者共同']; v = [48, 54, 120]; c = ['#2E8B57', '#1F5F8B', '#C0392B']
    ax.bar(range(3), v, .6, color=c)
    for i, x in enumerate(v): ax.text(i, x + 3, f'{x} 例（{x / 222 * 100:.0f}%）', ha='center', fontsize=19, weight='bold', color=c[i])
    ax.set_xticks(range(3), lab, fontsize=18); ax.set_ylim(0, 140); ax.set_yticks([]); ax.spines[['top', 'right', 'left']].set_visible(False)
    fig.tight_layout(); return fig


deck.cover(['第五跖骨基底', '撕脱骨折', '是谁拉断的？'], kicker='J Foot Ankle Res 2022 · 222 例',
           subtitle='三维 CT 骨折线热图 + 解剖，提出新分型', photos=[(img('lb108').crop((0, 0, 709, 602)), 'Ⅰ、Ⅱ 型示意（原文图 8）')], banner='跖腱膜外侧束 · 腓骨短肌 · 两者共同')
deck.text('为什么要研究', '原文背景', [
    ('box', '很常见', '跖骨骨折 70% 在第五跖骨，其中三分之二是基底撕脱骨折\n机制：后足内翻 + 前足跖屈，力被导向基底', 'navy'),
    ('box', '现有分型不够用', 'Ekrol：Ⅰ 结节尖、Ⅱ 斜行入跖骰关节、Ⅲ 横行过 4/5 跖骨基底交界\nMehlhorn：按骨折线入关节位置 + 是否移位 >2 mm\n双骨折线、跨区、弯折的骨折线都描述不了', 'accent'),
    ('box', '这篇怎么做', '222 例 CT 三维重建 → 骨折线叠加成热图\n8 侧尸体标本测肌腱/筋膜附着区 → 两相对照，找“拉力源”', 'teal')])
deck.figure('① 222 例骨折线叠在一起', '原文图 1（编者中文标注）', [img('lb43').crop((0, 0, 1180, 721)), img('lb43').crop((1180, 0, 1946, 721))], None, [
    ('box', '看点', '222 例骨折线叠在同一个标准化左侧第五跖骨上：集中在基底，背侧面和外侧面最密', 'teal')], stack=True, max_h=480)
deck.figure('② 骨折线热图', '原文图 2（编者中文标注）', [img('lb41').crop((0, 0, 790, 400)), img('lb41').crop((790, 0, 1418, 400))], None, [
    ('bul', ['颜色越红，骨折线越集中', '背侧观上是一条**弧形带**，最密处距后缘 2/5～7/10'])], stack=True, max_h=560)
deck.figure('③ 腓骨短肌附着在哪', '原文图 5（编者中文标注）', img('lb71'), None, [
    ('box', '要点', '基底背外侧，卵圆形；腱径 5.70 mm', 'teal')], max_h=760)
deck.figure('④ 跖腱膜外侧束附着在哪', '原文图 6（编者中文标注）', img('lb70'), None, [
    ('box', '要点', '包绕结节，卵圆形；腱径 6.65 mm（三者最粗）\n第三腓骨肌：腱径 3.31 mm、附着更远、1 例缺如 → 作用不大', 'teal')], max_h=720)
deck.figure('⑤ 骨折块对上了附着区', '原文图 7（编者中文标注）', [img('lb94').crop((0, 0, 650, 294)), img('lb94').crop((650, 0, 1300, 294)), img('lb94').crop((1300, 0, 1946, 294))], None, [
    ('box', '结论', 'a 跖腱膜外侧束为主（48 例）· b 腓骨短肌为主（54 例）· c 两者共同（120 例）\n骨折块正好落在**跖腱膜外侧束和/或腓骨短肌**的附着区', 'navy')], stack=True, max_h=300)
deck.figure('⑥ 新分型', '原文图 8（编者中文标注）', [img('lb108').crop((0, 0, 709, 602)), img('lb108').crop((709, 0, 1418, 602))], None, [
    ('steps', [('Ⅰ 型', '近端骨折线：**跖腱膜外侧束**为主'), ('Ⅱ 型', '中间骨折线：**腓骨短肌**为主'), ('Ⅲ 型', '远端骨折线：两者共同；ⅢA 一条线，ⅢB 两条线')])], stack=True, max_h=440)
deck.chart('⑦ 222 例怎么分布', '据原文图 7 绘制', count_fig(), [
    ('bul', ['按原有 Ekrol 分型，有 **17.6%** 归不进去（特殊型）', '新分型中 Ⅲ 型最多，占一半以上'])])
deck.text('⑧ 对治疗的提示（作者观点）', '原文讨论', [
    ('box', 'Ⅲ 型移位 ≥2 mm 考虑手术', '随访 30 例保守治疗 3 个月，**5 例再移位，全是 Ⅲ 型**\n两条软组织同时牵拉；Ⅲ 型几乎都累及关节面，可能留下创伤性关节炎', 'accent'),
    ('box', 'Ⅰ 型要查腓骨短肌', '10 例 Ⅰ 型都在外踝尖处合并**腓骨短肌断裂**（肌腱自身断裂缓冲了对骨的拉力）\n→ 建议 MRI 或超声检查', 'yellow'),
    ('box', '局限', '标本仅 8 侧、来源单一；未做测量可靠性检验；分型尚待验证', 'grey')])
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('222 例', '急性第五跖骨基底撕脱骨折'), ('2/5～7/10', '骨折线最密集处（距后缘）'), ('6.65 mm', '跖腱膜外侧束腱径（最粗）'), ('5/30', '保守治疗再移位，全是 Ⅲ 型')]),
    ('h', '原文对不上的地方'),
    ('bul', ['方法写“女 97、男 125”，表 1 却是男 97、女 125；年龄上限 80 / 81 岁不一致', '先说远端骨折线很少穿过跖跗关节面，后又说 Ⅲ 型几乎都累及关节面', '“Ⅲ 型移位 ≥2 mm 手术”只基于 30 例 3 个月附带随访']),
    ('box', '文献', 'He W, Zhou H, Zhang Y, et al. Classification of avulsion fractures of the fifth metatarsal base using three-dimensional CT mapping and anatomical assessment: a retrospective case series study. J Foot Ankle Res. 2022;15:65.\nCC BY 4.0，原图引自原文，编者加中文标注', 'grey')])
deck.save(OUT)
