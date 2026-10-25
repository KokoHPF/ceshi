#!/usr/bin/env python3
"""Pais-Vieira 等 2020 ExoAtlet 外骨骼穿戴与康复训练方法：首图中文标题卡、13 步流程卡、按页面区域从 PDF 高清裁出的原文图（英文字样用中文标签盖住），
脊髓损伤患者 13 次训练柱状图（原文图 16B 按原文数字用中文重画）、开门示意图（原文图 18 用中文重画）、封面。
共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <PDF> <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import pymupdf
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Arc, Rectangle, Circle, FancyArrowPatch
PDF, WORK, OUT, FM, FBOLD = sys.argv[1:6]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD); doc = pymupdf.open(PDF)


def crop(page, x0, y0, x1, y1, name):
    """按页面预览图（宽 650 像素）上的坐标裁图，4 倍分辨率渲染"""
    p = doc[page - 1]; s = p.rect.width / 650
    pix = p.get_pixmap(clip=pymupdf.Rect(x0 * s, y0 * s, x1 * s, y1 * s), dpi=288); pix.save(f'{WORK}/{name}'); return name


def cover(name, boxes, W=1200):
    """boxes: [(fx0, fy0, fx1, fy1, 中文, 颜色)]，用色块盖住原图英文并写中文"""
    im = k.op(name); im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS); d = ImageDraw.Draw(im)
    for fx0, fy0, fx1, fy1, t, c in boxes:
        x0, y0, x1, y1 = fx0 * im.width, fy0 * im.height, fx1 * im.width, fy1 * im.height
        fs = 34; f = ImageFont.truetype(FBOLD, fs); tw = d.textlength(t, font=f)
        w = max(x1 - x0, tw + 24); h = max(y1 - y0, fs + 16); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        bx0 = min(max(0, cx - w / 2), im.width - w); by0 = min(max(0, cy - h / 2), im.height - h)
        d.rounded_rectangle([bx0, by0, bx0 + w, by0 + h], 10, fill=c)
        d.text((bx0 + (w - tw) / 2, by0 + (h - fs) / 2 - 4), t, font=f, fill='white')
    return im


k.save(k.title('方法学论文 · 《MethodsX》2020', ['ExoAtlet 动力外骨骼的', '穿戴摆位与康复训练方法'],
               'Pais-Vieira C, Allahdad M, Neves-Amado J, Perrotta A, Morya E, Moioli R, Shapkova E, Pais-Vieira M.',
               'MethodsX. 2020;7:100849. doi:10.1016/j.mex.2020.100849',
               '葡萄牙天主教大学、米尼奥大学、阿威罗大学；巴西圣多斯杜蒙研究所；俄罗斯圣彼得堡肺结核研究所等'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1

k.save(k.card('13 步流程总览（编者根据原文表 1 整理）', [
    ('准备（步骤 1～4）', '① 充电：电池充满约需 6～8 小时，外骨骼用平板/笔记本上的 App 控制\n② 准备场地、患者和治疗师：宽松轻便衣服、平底鞋；新手治疗师先空载演练\n③ 量患者的脚长、小腿、大腿、骨盆宽度（仅第一次）\n④ 按“从远到近”（脚→小腿→大腿→腰）调外骨骼长度', LT, TEAL),
    ('穿上和站起（步骤 5～7）', '⑤ 轮椅与外骨骼成 45°～90°，两者都锁住再转移\n⑥ 从脚到胸逐个系绑带，关节对齐（误差 ≤2 cm）\n⑦ 借助助行器/拐杖站起：一人在后、一人在前；站起后量血压、看有无低血压或焦虑', GR, (0, 120, 60)),
    ('训练（步骤 8～11）', '⑧ 左右转移重心（用髋，不用肩）\n⑨ 原地踏步：先一步一按，再自动间隔 1～2 秒\n⑩ 连续行走：间隔逐步缩到 0 秒；跟在后面的治疗师晚一步迈腿\n⑪ 上下楼梯：每级台阶当一个独立障碍，双脚都上去再迈下一级', OR, (200, 120, 0)),
    ('结束（步骤 12～13）', '⑫ 坐下：椅子放在身后约 30 cm，切换坐姿模式（约 3 秒延迟），两人扶\n⑬ 检查皮肤压痕：关节和绑带处最常见，教会患者和家属自查', PK, RED),
]), n); n += 1

put(crop(3, 150, 84, 506, 372, 'f1.png'), '原文图 1  A：没有患者时，治疗师先自己练习操作外骨骼——注意治疗师的左脚跟着外骨骼的脚走，保证任何时候至少 3 个点着地；B：可调高度的琴凳，用来放外骨骼和转移患者')
put(cover(crop(4, 58, 86, 590, 357, 'f2.png'), [(.045, .855, .185, .935, '鞋码 +2', (24, 128, 64)), (.78, .915, .91, .985, '腰围 +2 cm', (200, 150, 0))]),
    '原文图 2  量体：外骨骼关节要和患者关节大致对齐。同色箭头表示同一个测量（外骨骼上和骨骼模型上对照）：脚长（外骨骼鞋码比患者大 2 码）、小腿（股骨外上髁到脚底）、大腿（大转子到股骨外上髁）、骨盆宽度（两侧大转子之间，再加 2 cm）')
put(crop(5, 60, 86, 598, 420, 'f3.png'), '原文图 3  调外骨骼：永远从远端到近端（脚→胸）。A：治疗师单膝跪地，把外骨骼的腿架在自己腿上调，省力；B：调膝；C：调腰宽。每次只由一名治疗师动手，防止外骨骼倒下或零件松脱伤人')
put(crop(6, 52, 86, 592, 230, 'f4.png'), '原文图 4  从轮椅转移到外骨骼（A→D）：轮椅和外骨骼都要锁住；外骨骼开机后关节锁定，可以当作额外的支撑')
put(crop(6, 60, 286, 592, 554, 'f5.png'), '原文图 5  系绑带：A～B 小腿绑带，可加护垫，松紧以能塞进一根手指为度；C～D 大腿支撑——大腿后侧要和支撑完全贴合，否则可能伤到腘绳肌；有导尿管的患者要确保管子不被压住')
put(crop(7, 60, 86, 598, 442, 'f6.png'), '原文图 6  借助助行器站起：A 患者先握住助行器下方横杆；B 一名治疗师在外骨骼后方、另一名在助行器前方；C 站起后常需要再紧一下绑带和锁扣')
put(cover(crop(8, 52, 84, 592, 432, 'f7.png'), [(.12, .0, .46, .065, '重心移向左腿', C_HI), (.62, .0, .97, .065, '重心移向右腿', C_HI)]),
    '原文图 7  左右转移重心：正式走之前先熟悉外骨骼带来的重心变化。要用髋部转移，不要耸肩或甩肩——用肩代偿会导致肌肉酸痛')
put(cover(crop(9, 222, 86, 434, 452, 'f8.png'), [(.30, .0, .70, .065, '安全吊带', RED), (.70, .06, 1.0, .15, '移位吊架', (60, 60, 60)), (.58, .855, .92, .925, '跑台', (60, 60, 60))]),
    '原文图 8  早期可以在跑台上配合安全吊带和移位吊架训练')
put(crop(10, 205, 86, 440, 494, 'f9.png'), '原文图 9  在平行杠里走：手臂只能“往下撑”，不能“往回拉”——以后用拐杖时也是靠向下撑地支撑身体')
put(crop(11, 60, 86, 598, 424, 'f10.png'), '原文图 10  上下楼梯：A～C 截瘫患者下楼梯；D 治疗师、患者、扶手和拐杖的整体站位。下楼比上楼危险：很多外骨骼没有足跟动作')
a, b = crop(12, 143, 86, 502, 464, 'f11.png'), crop(12, 163, 520, 482, 646, 'f12.png')
put(k.op(a), '原文图 11  坐下：外骨骼站立时，离身后的椅子大约 1 英尺（约 30 cm）的距离才能坐下（橙色箭头）')
put(cover(b, [(.27, .03, .50, .22, '压痕', RED)]), '原文图 12  一名健康受试者训练后大腿锁扣处留下的压痕（红色箭头）。每次训练后都要检查关节和绑带处的皮肤')
put(crop(13, 238, 86, 420, 400, 'f13.png'), '原文图 13  紧急停止：比如患者出现直立性低血压，治疗师用髋部顶住外骨骼，关机后慢慢放到坐姿，再解开绑带')

# 原文图 16B 中文重画
S = list(range(1, 14)); dur = [93, 48, 25, 46, 57, 60, 62, 80, 64, 49, 61, 39, 51]
walk = [0, 11, 9, 17, 20, 22, 23, 33, 27, 22, 27, 20, 33]; ns = [0, 2, 2, 4, 4, 6, 5, 5, 8, 10, 7, 18, 8]
fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
ax.bar(S, dur, .7, color='#D9E3EA', label='整次训练时长'); ax.bar(S, walk, .7, color='#5B9BD5', label='行走时长'); ax.bar(S, ns, .7, color='#16324F', label='不停歇连续行走')
for x, v in zip(S, dur): ax.text(x, v + 1.5, str(v), ha='center', fontsize=13)
for x in (8, 13): ax.annotate('评估', (x, dur[x - 1] + 9), (x, dur[x - 1] + 22), ha='center', fontsize=14, color='#D9432F', arrowprops=dict(arrowstyle='->', color='#D9432F', lw=2))
ax.set_xticks(S, [f'第{s}次' for s in S], fontsize=12); ax.set_ylabel('分钟', fontsize=15); ax.set_ylim(0, 112); ax.tick_params(axis='y', labelsize=13)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); ax.legend(frameon=False, fontsize=14, loc='upper right')
ax.set_title('脊髓损伤患者 13 次外骨骼训练：合计 735 分钟，行走 264 分钟，连续行走 79 分钟', fontsize=17)
fig.tight_layout(); fig.savefig(f'{WORK}/sci.png', facecolor='white'); plt.close(fig)
c16 = crop(17, 98, 86, 556, 402, 'f16a.png')
put(cover(c16, [(.0, .0, .48, .09, '第 1～5 次：多名助手', C_NAV), (.52, .0, 1.0, .09, '第 5～13 次：一名助手', C_OK)]),
    '原文图 16A  一名 21 岁男性脊髓损伤患者（胸 5～7 骨折，ASIA A 级完全性损伤，伤后 2 年开始训练）：前 5 次需要多名治疗师扶，之后只需一名')
put(k.op('sci.png'), '原文图 16B 重画（数字照原文图下表格）：每次训练时长、其中行走时长和不停歇连续行走时长。第 8、13 次做了足底压力评估')

# 原文图 18 中文重画
fig, axs = plt.subplots(1, 2, figsize=(12, 6.2), dpi=100)
for a, (ttl, exo) in zip(axs, [('不穿外骨骼', False), ('穿外骨骼', True)]):
    a.add_patch(Rectangle((-2.6, 4), 4.4, .35, fc='#C8641E')); a.add_patch(Circle((1.6, 3.75), .25, fc='#888'))
    a.add_patch(Arc((-2.6, 4.17), 8.4, 8.4, theta1=270, theta2=360, ls='--', lw=1.8, color='#333'))
    y = 1.1 if exo else 2.2
    a.add_patch(FancyBboxPatch((-1.1, y - .25), 2.2, .5, boxstyle='round,pad=0.1', fc='black')); a.add_patch(Circle((0, y), .45, fc='black'))
    if exo: a.add_patch(Rectangle((-1.0, y - 1.0), 2.0, .45, fc='#ddd', ec='#333'))
    a.add_patch(FancyArrowPatch((0, y + .6), (0, y + 1.4 if exo else 3.3), arrowstyle='-|>', mutation_scale=35, color='#5B9BD5', lw=6))
    a.text(0, -.9, '走到门边后可以随时\n后退、侧移来纠正' if not exo else '提前规划，停在门的\n开门轨迹（虚线）之外', ha='center', va='top', fontsize=16)
    a.set_title(ttl, fontsize=20); a.set_xlim(-3.2, 3.2); a.set_ylim(-2.4, 4.8); a.set_aspect('equal'); a.axis('off')
fig.tight_layout(); fig.savefig(f'{WORK}/door.png', facecolor='white'); plt.close(fig)
put(k.op('door.png'), '原文图 18 重画：穿外骨骼开门。外骨骼限制了后退、侧移和转身，走近门之前就要算好门扇的开门轨迹，否则临时调整容易摔倒')

c = k.op('f7.png'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
