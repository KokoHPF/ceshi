#!/usr/bin/env python3
"""Wilk 等 2023 ACL 伤后回场测试理论模型：首图中文标题卡、为什么要改/测试总览两张要点卡、三类测试的场地示意图（按原文尺寸换算成公制用中文画）、
原文图 1～8 测试照片贴中文名称标签配中文图注、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('临床评论 · 《International Journal of Sports Physical Therapy》2023', ['ACL 伤后的回场测试需要改变：', '一个理论模型'],
               'Wilk KE, Thomas ZM, Arrigo CA, Davies GJ.', 'Int J Sports Phys Ther. 2023;18(1):272-281. doi:10.26603/001c.67988',
               '美国 Champion Sports Medicine、美国运动医学研究所、佐治亚南方大学等'), 1)
n = 2
def put(im, cap):
    global n; k.save(k.capbox(im, cap), n); n += 1

k.save(k.card('为什么现有的“回场测试”不够（原文观点）', [
    ('1. 很多人根本没测', '一篇纳入 716 篇文章的综述里，只有 13% 用客观标准决定回场；多数决定在医生诊室做，只凭查体和主观描述，最常用的标准还是“术后多少个月”', PK, RED),
    ('2. 康复没做完就回去了', '保险额度用完、付不起费用或自己停止康复，回场前没练完整个流程', OR, (200, 120, 0)),
    ('3. 康复里缺高水平、专项化的挑战', '没在接近比赛的环境里练过，回场时准备不足', OR, (200, 120, 0)),
    ('4. 现有测试都是“预知动作”的单一任务', '单腿跳、折返跑、平衡、等速肌力、肢体对称指数……都是事先知道要做什么；而女足运动员的 ACL 损伤多发生在防守和来不及预判的反应动作中', LT, TEAL),
    ('作者的结论', '这些测试很有用，但更适合决定“能不能进入跑、跳、敏捷训练”，不足以判断“能不能回比赛”；回场前还缺一环：神经认知和反应性测试', GR, (0, 120, 60)),
]), n); n += 1

k.save(k.card('作者提出的测试顺序：3 类共 8 项', [
    ('先过准入标准', '疼痛、心理准备、关节积液、活动度、稳定性查体、全下肢肌力/爆发力/耐力、跳跃和单腿跳测试等都达标（见文中表格），才进入下面的反应性测试', LT, TEAL),
    ('① Blazepod 灯光反应测试（3 项）', '侧滑步接球拍灯（30 秒）→ 四角接球拍灯（30 秒）→ 站立左右脚拍灯（15 秒）\n记录：拍灯次数、平均反应时间（第 3 项另记错误数）', GR, (0, 120, 60)),
    ('② 反应性折返跑（2 项）', '反应性 10 码 T 形折返跑 → 反应性 10 码 L 形跑\n跑到约 2/3 时测试者喊方向；记录：完成时间', OR, (200, 120, 0)),
    ('③ 反应性单腿跳（3 项）', '单腿跳远 → 单腿交叉跳 → 左右交替交叉跳\n腾空时测试者喊落地脚；落地要稳住 2～3 秒；每项 3 次取平均距离', PK, RED),
    ('测试间休息', '按测试时长休息 1～3 分钟', PU, C_NAV),
]), n); n += 1

def pod(ax, x, y, c, r=.32, lab=None):
    ax.add_patch(Circle((x, y), r, fc=c, ec='#333', lw=1.5))
    if lab: ax.text(x, y - r - .35, lab, ha='center', va='top', fontsize=16, color='#333')
def arrow(ax, a, b, c='#555', ls='-', rad=0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=20, color=c, lw=2, ls=ls, connectionstyle=f'arc3,rad={rad}'))
def fin(fig, name):
    fig.tight_layout(); fig.savefig(f'{WORK}/{name}', facecolor='white'); plt.close(fig)

# Blazepod 三个场地
fig, axs = plt.subplots(1, 3, figsize=(15, 5.6), dpi=100)
a = axs[0]; xs = [-2.28, -.76, .76, 2.28]; cs = ['#9b59b6', '#2e86de', '#27ae60', '#e67e22']
for x, c in zip(xs, cs): pod(a, x, 0, c)
a.annotate('', (xs[1], -.9), (xs[0], -.9), arrowprops=dict(arrowstyle='<->', lw=1.2)); a.text(-1.52, -1.25, '1.52 m（5 英尺）', ha='center', va='top', fontsize=20)
a.plot(0, 0, marker='^', ms=16, color='#D9432F'); a.text(.3, .5, '起始站中间\n半蹲侧滑步', ha='left', fontsize=16)
a.plot(-1.6, 2.6, 'o', ms=12, color='#888'); a.text(-1.35, 2.6, '抛球的人', va='center', fontsize=20); arrow(a, (-1.5, 2.4), (-.85, .45), '#888', '--')
a.set_title('① 侧滑步接球拍灯（30 秒）\n4 个灯排一条线，只拍蓝灯', fontsize=19)
a.set_xlim(-3.2, 3.2); a.set_ylim(-2, 3.2)
a = axs[1]; P = [(-3.2, -3.2), (3.2, -3.2), (3.2, 3.2), (-3.2, 3.2)]
for (x, y), c in zip(P, ['#2e86de', '#e67e22', '#27ae60', '#e74c3c']): pod(a, x, y, c, .5)
a.plot([-3.2, 3.2, 3.2, -3.2, -3.2], [-3.2, -3.2, 3.2, 3.2, -3.2], ':', color='#aaa'); a.text(0, -4.0, '边长 6.4 m（21 英尺）', ha='center', va='top', fontsize=20)
a.plot(0, 0, marker='^', ms=16, color='#D9432F'); a.text(0, .6, '起始站中心', ha='center', fontsize=20); arrow(a, (0, 0), (-2.8, -2.8), '#D9432F')
a.set_title('② 四角接球拍灯（30 秒）\n一个灯亮蓝色，其余亮干扰色', fontsize=19); a.set_xlim(-5, 5); a.set_ylim(-5, 6.4)
a = axs[2]; Q = [(-.46, -.15), (.46, -.15), (-.46, .15), (.46, .15)]
for (x, y), c in zip(Q, ['#2e86de', '#888', '#888', '#e74c3c']): pod(a, x, y, c, .07)
a.add_patch(Rectangle((-.46, -.15), .92, .3, fill=False, ls=':', ec='#aaa'))
a.text(0, -.32, '长方形 91 × 30 cm（36 × 12 英寸）', ha='center', va='top', fontsize=20); a.text(0, 0, '双脚原地\n快速小碎步', ha='center', va='center', fontsize=20)
a.text(0, .42, '亮蓝灯 → 左脚拍；亮红灯 → 右脚拍\n一次只亮一个', ha='center', fontsize=17, color='#16324F')
a.set_title('③ 站立左右脚拍灯（15 秒）\n记拍灯数、错误数、反应时间', fontsize=19); a.set_xlim(-.8, .8); a.set_ylim(-.6, .75)
for a in axs: a.set_aspect('equal'); a.axis('off')
fin(fig, 'blaze.png')
put(k.op('blaze.png'), '编者示意图：3 项 Blazepod 灯光反应测试的场地（尺寸按原文换算）。灯在被拍后立刻随机切换，没有间隔')
T = lambda x, t, c: tags_at(k, x, [(.01, .02, t, c)])
put(T('x63.jpg', '侧滑步接球拍灯', C_OK), '原文图 1：侧滑步接球拍灯测试。保持半蹲运动姿势侧滑步，不许跳或跑；接住队友抛来的球、拍蓝灯、把球抛回，同时找下一个蓝灯')
put(T('x64.jpg', '四角接球拍灯', C_OK), '原文图 2：四角接球拍灯测试。4 个灯摆成边长 6.4 m 的正方形，从中心出发去找蓝灯，同样要接球、拍灯、回抛')
put(T('x76.jpg', '站立左右脚拍灯', C_OK), '原文图 3：站立左右脚拍灯测试。原地快速小碎步，蓝灯用左脚拍、红灯用右脚拍，15 秒内拍得越多越好')

# 折返跑
fig, axs = plt.subplots(1, 2, figsize=(14, 6.6), dpi=100)
for a, ttl in zip(axs, ['④ 反应性 10 码 T 形折返跑', '⑤ 反应性 10 码 L 形跑']):
    for x, y in [(0, 0), (-4.6, 9.1), (0, 9.1), (4.6, 9.1)]: a.plot(x, y, marker='^', ms=18, color='#E8A200', mec='#333')
    a.text(0, -.9, '起点', ha='center', va='top', fontsize=21); a.annotate('', (0, 8.6), (0, .5), arrowprops=dict(arrowstyle='-|>', lw=2.5, color='#16324F'))
    a.text(-.4, 4.5, '冲刺 9.1 m\n（10 码）', ha='right', va='center', fontsize=21); a.plot(0, 6.1, 'o', ms=10, color='#D9432F')
    a.text(.4, 6.1, '跑到约 2/3 处\n测试者喊“左/右”', va='center', fontsize=17, color='#D9432F')
    a.annotate('', (4.6, 10.6), (0, 10.6), arrowprops=dict(arrowstyle='<->', lw=1.2)); a.text(2.3, 10.9, '4.6 m（5 码）', ha='center', fontsize=20)
    a.set_title(ttl, fontsize=21); a.set_xlim(-7.5, 7.5); a.set_ylim(-2.5, 12.6); a.set_aspect('equal'); a.axis('off')
a = axs[0]
a.text(0, -2.2, '到中间锥后：侧滑步 4.6 m 碰一侧锥\n→ 反向侧滑 9.1 m 碰另一侧锥 → 侧滑回中间锥\n→ 转身冲刺回起点；计时', ha='center', va='top', fontsize=21)
a.annotate('', (4.4, 8.5), (.3, 8.5), arrowprops=dict(arrowstyle='-|>', lw=2, color='#188080'))
a.annotate('', (-4.4, 8.0), (4.4, 8.0), arrowprops=dict(arrowstyle='-|>', lw=2, color='#188080'))
a = axs[1]
a.text(0, -2.2, '听到方向后：转向该侧冲刺，绕过侧锥\n→ 跑回中间锥 → 转身冲刺回起点\n（走出一个“L”）；计时', ha='center', va='top', fontsize=21)
a.add_patch(FancyArrowPatch((.3, 9.3), (4.6, 9.8), arrowstyle='-|>', mutation_scale=20, color='#188080', lw=2, connectionstyle='arc3,rad=-.2'))
a.add_patch(FancyArrowPatch((4.9, 8.8), (.4, 8.4), arrowstyle='-|>', mutation_scale=20, color='#188080', lw=2, connectionstyle='arc3,rad=-.3'))
fin(fig, 'shuttle.png')
put(k.op('shuttle.png'), '编者示意图：2 项反应性折返跑的场地（尺寸按原文换算）。两项都用 T 形摆放的 4 个锥，方向在跑动中途才喊出')
put(T('x77.jpg', '反应性 T 形折返跑', C_HI), '原文图 4：反应性 10 码 T 形折返跑。图中运动员正在侧滑步去碰锥，测试者站在一旁喊方向')
put(T('x78.jpg', '反应性 L 形跑', C_HI), '原文图 5：反应性 10 码 L 形跑。听到方向后转身冲刺绕过侧锥，再回中间锥、转身冲回起点')

# 单腿跳
fig, axs = plt.subplots(1, 3, figsize=(15, 6.2), dpi=100)
def foot(a, x, y, side, c):
    a.add_patch(Rectangle((x - .12, y - .25), .24, .5, fc=c, ec='#333', lw=1)); a.text(x + (.45 if side == 'R' else -.45), y, '右' if side == 'R' else '左', ha='center', va='center', fontsize=20)
L, R = '#2e86de', '#e74c3c'
seqs = [('⑥ 反应性单腿跳远', [(-.3, 0, 'L', L), (.3, 3.2, 'R', R)], '单腿起跳，腾空时听口令，\n用指定的腿落地，\n稳住 2～3 秒'),
        ('⑦ 反应性单腿交叉跳', [(-.3, 0, 'L', L), (.4, 2.4, 'R', R), (-.4, 4.4, 'R', R), (.4, 6.4, 'R', R)], '第 1 跳听口令定落地腿，\n越过中线；之后同一条腿\n再交叉跳 2 次，最后一跳稳住'),
        ('⑧ 反应性左右交替交叉跳', [(-.3, 0, 'L', L), (.4, 2.4, 'R', R), (-.4, 4.4, 'L', L), (.4, 6.4, 'R', R)], '第 1 跳听口令定落地腿，\n越过中线；之后左右脚交替\n再跳 2 次，最后一跳稳住')]
for a, (t, pts, note) in zip(axs, seqs):
    a.plot([0, 0], [-.8, 7.4], color='#bbb', lw=6); a.plot([-1.2, 1.2], [-.6, -.6], color='#333', lw=2); a.text(1.25, -.6, '起跳线', va='center', fontsize=20)
    for i, (x, y, s, c) in enumerate(pts):
        foot(a, x, y, s, c)
        if i: arrow(a, (pts[i - 1][0], pts[i - 1][1] + .3), (x, y - .3), '#555', '--', .2)
    a.text(0, -1.3, note, ha='center', va='top', fontsize=21); a.set_title(t, fontsize=20)
    a.set_xlim(-1.8, 1.8); a.set_ylim(-3.8, 7.6); a.set_aspect('equal'); a.axis('off')
axs[0].text(.9, 1.6, '测试者喊“右”', fontsize=16, color='#D9432F'); axs[1].text(.55, .9, '喊“右”', fontsize=16, color='#D9432F'); axs[2].text(.55, .9, '喊“右”', fontsize=16, color='#D9432F')
fin(fig, 'hops.png')
put(k.op('hops.png'), '编者示意图：3 项反应性单腿跳（中间灰线为地面中线）。每项连做 3 次取平均距离，从起跳线量到落地脚的脚跟')
put(tags_at(k, 'x85.jpg', [(.01, .02, 'A 起跳', C_NAV), (.51, .02, 'B 按口令落地', C_NAV)]), '原文图 6：反应性单腿跳远。单脚站立向前跳，跳起后测试者才告诉用哪只脚落地')
put(tags_at(k, 'x86.jpg', [(.01, .02, 'A 起跳', C_NAV), (.51, .02, 'B 交叉越过中线', C_NAV)]), '原文图 7：反应性单腿交叉跳。听口令落地并越过中间的胶带线，之后同一条腿再交叉跳 2 次')
put(tags_at(k, 'x90.jpg', [(.01, .02, 'A 起跳', C_NAV), (.51, .02, 'B 左右交替交叉', C_NAV)]), '原文图 8：反应性左右交替交叉跳。听口令落地并越过中线，之后左右脚交替再交叉跳 2 次')
c = k.op('x63.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .3)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
