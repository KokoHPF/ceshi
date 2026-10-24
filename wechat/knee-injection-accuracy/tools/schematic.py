#!/usr/bin/env python3
"""编者示意图：改良前外侧入路的进针点（右膝前面观，屈膝 90°）。用法：python3 schematic.py 字体 输出.jpg"""
import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Ellipse, Polygon, FancyBboxPatch
font_manager.fontManager.addfont(sys.argv[1]); plt.rcParams['font.family'] = font_manager.FontProperties(fname=sys.argv[1]).get_name()
BONE, EDGE, TEAL, RED, NAVY = '#F3E9D8', '#8A7A63', '#188080', '#D9432F', '#16324F'
fig, ax = plt.subplots(figsize=(9.6, 9.6), dpi=125); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
ax.add_patch(Polygon([[38, 100], [62, 100], [64, 74], [36, 74]], fc=BONE, ec=EDGE, lw=2))                 # 股骨干
ax.add_patch(Ellipse((40, 66), 20, 20, fc=BONE, ec=EDGE, lw=2)); ax.add_patch(Ellipse((60, 66), 20, 20, fc=BONE, ec=EDGE, lw=2))  # 股骨髁
ax.add_patch(Polygon([[28, 58], [72, 58], [70, 49], [58, 42], [57, 8], [43, 8], [42, 42], [30, 49]], fc=BONE, ec=EDGE, lw=2))   # 胫骨
ax.add_patch(Ellipse((50, 70), 15, 18, fc='#E9D9BC', ec=EDGE, lw=2.5))                                     # 髌骨
ax.add_patch(Polygon([[46, 61.5], [54, 61.5], [53, 43], [47, 43]], fc='#F7D9C4', ec='#C08060', lw=1.5))       # 髌腱
ax.add_patch(Ellipse((50, 41), 7, 4, fc='#E9D9BC', ec=EDGE, lw=1.5))                                        # 胫骨结节
ax.add_patch(Ellipse((32, 49), 5, 4, fc='#E9D9BC', ec=EDGE, lw=1.5))                                      # Gerdy 结节
ax.plot([18, 50], [61.5, 61.5], ls='--', color=TEAL, lw=2.5); ax.plot([32, 32], [49, 76], ls='--', color=TEAL, lw=2.5)
ax.plot(32, 61.5, marker='*', ms=30, color=RED, mec='white', mew=1.5)
lab = lambda x, y, t, c=NAVY, **k: ax.text(x, y, t, **{'fontsize': 19, 'color': c, **k})
lab(50, 70, '髌骨', ha='center', va='center'); lab(56, 50, '髌腱'); lab(55, 35, '胫骨结节')
lab(4, 42, 'Gerdy 结节', TEAL); ax.annotate('', (30, 48), (20, 44.5), arrowprops=dict(arrowstyle='->', color=TEAL, lw=2))
lab(2, 64, '髌骨下缘水平线', TEAL); lab(18, 79, 'Gerdy 结节垂线', TEAL)
lab(2, 52, '进针点', RED, fontweight='bold'); ax.annotate('', (31, 60.5), (12, 54.5), arrowprops=dict(arrowstyle='->', color=RED, lw=2))
lab(4, 94, '外侧', '#666'); lab(86, 94, '内侧', '#666'); lab(4, 2, '编者示意图 · 右膝前面观 · 屈膝 90°', '#666', fontsize=17)
ax.add_patch(FancyBboxPatch((64, 6), 34, 24, boxstyle='round,pad=0.8', fc='#FFF4D2', ec='#E0B84A'))
for i, t in enumerate(['方向：朝外侧胫骨平台，', '与胫骨后倾平行（约 10°），', '不朝髁间窝', '深度：轻触股骨外侧髁', '软骨后，退针 1 mm']):
    ax.text(65.5, 29 - i * 5, t, fontsize=15, color=NAVY, va='top')
fig.tight_layout(pad=0.2); fig.savefig(sys.argv[2], dpi=125, facecolor='white'); print('ok')
