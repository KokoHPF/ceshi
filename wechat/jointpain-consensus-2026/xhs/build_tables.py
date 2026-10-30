#!/usr/bin/env python3
"""《关节痛诊治与管理专家共识(2026)》原文表 1～13 合集卡片（第二组，与 build_cards.py 主卡分开发，避免单篇超过 18 张）。
原文非开放许可：表格按原样 400 dpi 矢量渲染截取，不做改动；卡片注明“仅供学习交流，如有侵权请联系删除”。
表格图片先运行（PAGE 为 0 起）：
  E=../../skills/paper-to-xhs-cards/scripts/extract_figures.py
  t01 2 46 72 549 488 | t02 2 46 483 292 698 | t03 3 46 601 549 683 | t04 4 46 271 549 640 | t05 5 46 192 549 608
  t06 5 46 604 549 794 | t07 6 46 305 549 411 | t08 6 46 457 549 551 | t09 7 46 63 292 275 | t10 7 46 312 549 585
  t11 8 46 475 549 594 | t12 9 46 98 549 181 | t13 9 304 322 549 488
  逐行：python3 $E src/paper.pdf work --render-dpi 400 --clip PAGE x0 y0 x1 y1 NAME
用法：python3 build_tables.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from io import BytesIO
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='关节痛管理 · 原表', source='中华全科医学 2026 · 网络首发', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
T = lambda i: Image.open(os.path.join(WORK, f't{i:02d}.jpg')).convert('RGB')

NAMES = ['常见病因', '致关节痛药物', 'RICE 问诊', '系统查体', '实验室与影像', '红色预警征', '物理因子治疗',
         '外用药', '糖皮质激素', '病因与机制用药', '社区评估', '运动处方', '多学科分工']


def list_fig(w=9.6, h=5.2):
    """13 张原表目录（编者整理）"""
    fig, ax = plt.subplots(figsize=(w, h), dpi=100); ax.set_xlim(0, 3); ax.set_ylim(0, 5); ax.axis('off')
    for i, n in enumerate(NAMES):
        col, row = divmod(i, 5); x = .05 + col * 1.0; y = 4.45 - row * .98
        c = ['#1F5F8B', '#2E8B57', '#E3A21A'][col]
        ax.text(x, y, f'表{i + 1}', fontsize=19, color=c, weight='bold', va='center')
        ax.text(x + .33, y, n, fontsize=17, color='#222', va='center')
    fig.tight_layout(pad=.2); return fig


def fig2img(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['关节痛共识', '13 张原表', '高清合集'], kicker='中华全科医学 2026 · 共识原表',
           subtitle='原表按原样高清截取，建议收藏后放大看', photos=[(fig2img(list_fig()), '本组收录的原表')], banner='配合上一篇图文卡片一起看')
deck.figure('表 1  关节痛的常见病因', '全身性因素 · 关节局部因素 · 特殊人群', T(1), max_h=1000)
deck.figure('表 2  可致关节痛的常用药物', '问诊时别忘了查用药史', T(2), max_h=1000)
deck.figure('表 3 + 表 6  问诊与红色预警征', 'RICE 问诊法；出现红旗征需警惕严重疾病', [T(3), T(6)], stack=True, max_h=1000)
deck.figure('表 4  系统查体内容及临床意义', '关节外体征常指向风湿免疫病、肿瘤、感染', T(4), max_h=1000)
deck.figure('表 5  实验室与影像学检查', '按临床假设个体化选择', T(5), max_h=1000)
deck.figure('表 7 + 表 8 + 表 12  治疗参数', '物理因子治疗 · 外用药 · 推荐运动', [T(7), T(8), T(12)], stack=True, max_h=1000)
deck.figure('表 9  糖皮质激素的应用', '关节腔注射 vs 全身应用', T(9), max_h=1000)
deck.figure('表 10 + 表 11  对因用药与社区评估', '病因治疗要点；生物-心理-社会多维度评估', [T(10), T(11)], stack=True, max_h=1000)
deck.figure('表 13  关节痛多学科管理', '各科室职责', T(13), None, [
    ('box', '文献 · 版权', '《关节痛诊治与管理专家共识(2026)》专家委员会. 关节痛诊治与管理专家共识(2026). 中华全科医学, 2026, 24. 网络首发 2026-08-19.\n原表按原样截取。**仅供学习交流，如有侵权请联系删除**', 'grey')], max_h=700)
deck.save(OUT)
