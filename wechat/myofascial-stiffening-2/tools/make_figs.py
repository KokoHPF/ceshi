#!/usr/bin/env python3
"""Colonna、Casacci 2024 肌筋膜系统与运动 Part II（增加刚度）：首图中文标题卡、原文作者自摄/自绘的图贴中文标签、
运动后胶原合成与降解曲线（原文图 4 用中文重画）、刚度测量方法卡、运动与筋膜刚度证据卡、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('叙述性综述 · 《Cureus》2024', ['肌筋膜系统与运动（下）：', '增加刚度'],
               'Colonna S, Casacci F.', 'Cureus. 2024;16(12):e76295. doi:10.7759/cureus.76295',
               '意大利博洛尼亚 Spine Center 康复医学部、Osteopathic Spine Center Education 研发部'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1

put(tags_at(k, 'x45.jpg', [(.02, .01, 'A 老式链条张紧器', C_NAV), (.02, .515, 'B 新式后拨张紧', C_NAV)]),
    '原文图 1  自行车链条：太紧、太松都是“功能障碍”，所以车上都有调节张力的装置。作者认为肌筋膜系统同样是传递张力的“链条”，也会有张力过高和不足两种问题')
put(tags_at(k, 'x58.jpg', [(.01, .02, 'A 后侧主导', C_NAV), (.35, .02, 'B 平衡', C_OK), (.69, .02, 'C 前侧主导', C_HI)]),
    '原文图 2  腰椎矢状位 MRI 上的前后筋膜张力示意（红色弹簧，粗细代表张力大小）：A 后侧张力占优（前凸明显）；B 前后平衡；C 前侧张力占优（腰椎变直）。作者认为 C 型应拉长前侧、“收紧”后侧')
put(tags_at(k, 'x110.jpg', [(.0, .02, 'A 健康：被动结构撑住', C_OK), (.51, .02, 'B 腰痛：肌肉代偿', C_HI)]),
    '原文图 3  弯腰到底时：A 健康人主要靠并联筋膜（PE）撑住躯干，竖脊肌放电静息；B 腰痛患者并联系统张力不足，改由肌肉收缩（CE）和串联筋膜（SE）代偿，屈曲-放松现象消失')

t = np.linspace(0, 80, 400)
syn = 1.9 * np.exp(-((t - 24) / 17) ** 2) * (1 - np.exp(-t / 4)); syn += .15 * (t > 50) * (1 - np.exp(-(t - 50) / 10)) * np.exp(-(t - 50) / 60)
deg = -2.3 * np.exp(-((t - 22) / 11) ** 2) * (1 - np.exp(-t / 4)) - .12 * (t > 40) * np.exp(-(t - 40) / 40)
net = syn + deg
fig, ax = plt.subplots(figsize=(11, 6.2), dpi=100)
ax.plot(t, syn, color='#555', lw=2.5, label='胶原合成'); ax.plot(t, deg, color='#999', lw=2.5, ls='--', label='胶原降解')
ax.fill_between(t, 0, net, where=net < 0, color='#E05050', alpha=.85, label='净分解')
ax.fill_between(t, 0, net, where=net >= 0, color='#3CB371', alpha=.85, label='净合成')
ax.axhline(0, color='#333', lw=1); ax.set_xticks([0, 24, 48, 72], ['运动结束', '24 小时', '48 小时', '72 小时'], fontsize=15)
ax.set_yticks([]); ax.set_xlim(0, 80); ax.spines[['top', 'right']].set_visible(False)
ax.text(1, 2.0, '↑ 合成', fontsize=15, color='#555'); ax.text(1, -2.45, '↓ 降解', fontsize=15, color='#555')
ax.legend(frameon=False, fontsize=14, loc='upper right'); ax.set_title('运动后胶原转换示意：先净分解，约 1～2 天后转为净合成', fontsize=18)
fig.tight_layout(); fig.savefig(f'{WORK}/col.png', facecolor='white'); plt.close(fig)
put(k.op('col.png'), '原文图 4 重画（示意，非实测数据）：运动后胶原合成增加，约 24 小时达峰，可升高到平时的 2～3 倍；但降解也增加，头一段时间降解多于合成（红），之后转为净合成（绿），持续到约 72 小时。作者据此建议这类训练每周 1～2 次')

k.save(k.card('筋膜刚度怎么测（编者根据原文整理）', [
    ('肌张力测定仪（myotonometry，如 MyotonPRO）', '探头给组织几下短促冲击，分析回弹的振动波形，得出张力、动态刚度等指标\n便携、快速；但测不出是哪一层组织的刚度', LT, TEAL),
    ('剪切波弹性成像（SWE）', '超声发出声辐射力，产生横向传播的剪切波；组织越硬，波速越快，换算成剪切模量并用彩色叠加在 B 超图像上\n比压迫式弹性成像更客观、可量化、可重复，能看清测的是哪一深度', GR, (0, 120, 60)),
    ('两者不能互换', '离心运动后两种方法都显示变硬，但变化量互不相关，可能与肌筋膜水肿有关', PK, RED),
]), n); n += 1
k.save(k.card('运动能不能让筋膜“变硬”？目前的证据（编者整理）', [
    ('肌腱有较明确的证据', '抗阻训练增加肌腱刚度；运动后肌腱胶原合成增加 2～3 倍，作者建议每周 1～2 次、每次几分钟的针对性训练，胶原重塑需 6 个月～2 年', GR, (0, 120, 60)),
    ('肌肉和筋膜结果互相矛盾', '离心运动后：腘绳肌深筋膜 1 小时和 3 天后变硬，与迟发性肌肉酸痛程度相关；但斜方肌、股四头肌（极限越野跑后）反而变软\n增强式训练增加肌肉刚度；15 周等速训练让股内侧肌变硬；6 周训练没改变肱三头肌刚度', OR, (200, 120, 0)),
    ('能不能“定向”练串联或并联筋膜', '没有研究直接看过。只有肌节的间接证据：拉长位离心收缩增加串联肌节（纤维变长）；短位向心收缩（如上坡跑）减少串联肌节\n筋膜是否遵循同样的规律，目前只是推测', PK, RED),
]), n); n += 1
c = k.op('x110.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .02)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
