#!/usr/bin/env python3
"""编者示意图：前方入路髋关节注射的体表标志（右髋前面观）。用法：python3 schematic.py 字体 输出.jpg"""
import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Ellipse, FancyBboxPatch, Arc
font_manager.fontManager.addfont(sys.argv[1]); plt.rcParams['font.family'] = font_manager.FontProperties(fname=sys.argv[1]).get_name()
TEAL, RED, NAVY, GREY = '#188080', '#D9432F', '#16324F', '#777'
fig, ax = plt.subplots(figsize=(9.6, 8.4), dpi=125); ax.set_xlim(0, 100); ax.set_ylim(0, 88); ax.axis('off')
ax.add_patch(Ellipse((54, 36), 18, 18, fc='#F3E9D8', ec='#8A7A63', lw=2, alpha=.8)); ax.text(54, 36, '股骨头\n（深部）', ha='center', va='center', fontsize=15, color=GREY)
ax.plot([14, 82], [74, 52], color=NAVY, lw=3)                                     # 腹股沟韧带
ax.plot(14, 74, 'o', ms=14, color=TEAL); ax.text(4, 68, '髂前上棘', fontsize=19, color=TEAL)
ax.plot(82, 52, 'o', ms=12, color=GREY); ax.text(80, 56, '耻骨结节', fontsize=17, color=GREY)
ax.text(30, 76, '腹股沟韧带', fontsize=17, color=NAVY, rotation=-17)
ax.plot([64, 64], [80, 8], color=RED, lw=4, alpha=.75); ax.text(66, 14, '股动脉\n（摸搏动）', fontsize=17, color=RED)
y = 74 - (64 - 14) * 22 / 68; ax.plot(64, y, 'X', ms=16, color=RED, mec='white')
ax.plot([45, 64], [y - 2.5, y - 2.5], color=NAVY, lw=1.5); ax.annotate('', (45, y - 2.5), (64, y - 2.5), arrowprops=dict(arrowstyle='<->', color=NAVY, lw=1.5))
ax.text(48, y - 7.5, '2.5～3.5 cm', fontsize=16, color=NAVY)
ax.plot(45, y, marker='*', ms=30, color='#E8A200', mec=NAVY, mew=1.2); ax.text(29, y - 1.5, '进针点', fontsize=20, color='#C87800', fontweight='bold')
ax.text(4, 84, '外侧', fontsize=16, color=GREY); ax.text(90, 84, '内侧', fontsize=16, color=GREY); ax.text(4, 3, '编者示意图 · 右髋前面观 · 仰卧', fontsize=16, color=GREY)
ax.add_patch(FancyBboxPatch((4, 12), 42, 18, boxstyle='round,pad=0.8', fc='#FFF4D2', ec='#E0B84A'))
for i, t in enumerate(['22G 腰穿针', '向后内侧倾斜约 20°', '进针直到触及骨面', '再经影像确认后注药']):
    ax.text(5.5, 28 - i * 4.4, t, fontsize=15, color=NAVY, va='top')
fig.tight_layout(pad=0.2); fig.savefig(sys.argv[2], dpi=125, facecolor='white'); print('ok')
