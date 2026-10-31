#!/usr/bin/env python3
"""Hong、Calder 等 2022 KSSTA《3D 容积 MRI 可识别踝外侧韧带各束及外侧腓距跟韧带复合体》推文配图。
原文版权归 ESSKA（独家授权 Springer），非开放获取：原文图 1～7（work/x*.jpg，extract_figures.py 导出）按原样使用，
中文对照写在图上方的图注框里，不在原图上加字；其余为编者据原文撰写的整理卡和数据图。
共用工具在 ../bridge-review-1/tools/bridgekit.py。用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)

n = 1
def nxt(im):
    global n; k.save(im, n); n += 1
def put(im, cap):
    im = k.op(im) if isinstance(im, str) else im; nxt(k.capbox(im, cap))
def card(t, items): nxt(k.card(t, items))
def fig(f, name):
    f.savefig(f'{WORK}/{name}.png', facecolor='white'); plt.close(f); return f'{name}.png'


def prevalence():
    rows = [('距腓前韧带（ATFL）可见两束', 86.7, '26/30'), ('弓状纤维（双束者）', 84.6, '22/26'), ('弓状纤维（单束者）', 75, '3/4'),
            ('跟腓韧带–距腓后韧带连接', 70, '21/30'), ('距腓前–距腓后韧带连接', 63.3, '19/30'), ('两束之间可见穿支动脉', 16.7, '5/30')]
    f, ax = plt.subplots(figsize=(12, 5.6), dpi=100); N = len(rows)
    for i, (a, v, m) in enumerate(rows):
        y = N - 1 - i; ax.barh(y, v, .62, color='#1F5F8B' if i < 3 else ('#2E8B57' if i < 5 else '#C0392B'))
        ax.text(v + 1, y, f'{v:g}%（{m}）', va='center', fontsize=16)
    ax.set_yticks(range(N), [r[0] for r in rows][::-1], fontsize=16); ax.set_xlim(0, 112); ax.tick_params(axis='x', labelsize=13)
    ax.spines[['top', 'right']].set_visible(False); ax.set_title('30 个健康踝 3D MRI 上能看到什么（据原文表 1 绘制）', fontsize=19, loc='left', pad=12)
    f.tight_layout(); return fig(f, 'prev')


def sizes():
    f, axs = plt.subplots(1, 2, figsize=(12, 5), dpi=100)
    labs = ['上束', '下束', '单束']; col = ['#1F5F8B', '#E3A21A', '#9AA5B1']
    for ax, t, m, lo, hi in [(axs[0], '长度（mm）', [18.4, 13.2, 17.3], [10.8, 8.0, 16.7], [23.4, 16.7, 18.0]), (axs[1], '宽度（mm）', [4.7, 2.6, 5.9], [1.8, 1.4, 4.3], [6.8, 3.8, 7.8])]:
        for i in range(3):
            ax.bar(i, m[i], .6, color=col[i]); ax.plot([i, i], [lo[i], hi[i]], color='#333', lw=2)
            ax.text(i + .33, m[i], f'{m[i]:g}', va='center', fontsize=16, weight='bold')
        ax.set_xticks(range(3), labs, fontsize=17); ax.set_title(t, fontsize=18); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=13)
    f.suptitle('距腓前韧带各束大小（柱为均值，竖线为范围；双束 n = 26，单束 n = 4）', fontsize=17, x=.02, ha='left')
    f.tight_layout(rect=(0, 0, 1, .9)); return fig(f, 'sizes')


def studies():
    rows = [('本研究（3D，0.5 mm 层厚）', 86.7, '26/30'), ('Choo 等（3D）', 81.8, '27/33'), ('Szaro 等', 74.7, '148/198'), ('Delfaut 等 2003（3 mm 层厚）', 55, '12/22')]
    f, ax = plt.subplots(figsize=(12, 4.2), dpi=100); N = len(rows)
    for i, (a, v, m) in enumerate(rows):
        y = N - 1 - i; ax.barh(y, v, .6, color='#1F5F8B' if i == 0 else '#9AA5B1'); ax.text(v + 1, y, f'{v:g}%（{m}）', va='center', fontsize=16)
    ax.set_yticks(range(N), [r[0] for r in rows][::-1], fontsize=16); ax.set_xlim(0, 112); ax.spines[['top', 'right']].set_visible(False)
    ax.set_title('MRI 上看到双束 ATFL 的比例：各研究对比（据原文讨论）', fontsize=18, loc='left', pad=10); f.tight_layout(); return fig(f, 'studies')


nxt(k.title('影像解剖研究 · 《KSSTA》2022', ['3D MRI 能分清距腓前韧带的两束', '还能看到连接跟腓韧带的弓状纤维'],
            'Hong CC, Lee JC, Tsuchida A, Katakura M, Jones M, Mitchell AW, Dalmau-Pastor M, Calder J.',
            'Knee Surg Sports Traumatol Arthrosc. 2022（网络首发 12 月 20 日）. doi:10.1007/s00167-022-07275-x', '伦敦 Fortius 诊所（FIFA 医学卓越中心）；新加坡国立大学医院；巴塞罗那大学 等'))
card('背景：距腓前韧带不是“一条”（原文引言）', [
    ('踝扭伤最常见的受害者', '踝扭伤占足球伤的 31%、篮球伤的 45%，多为旋后内翻，外侧韧带复合体（ATFL、CFL、PTFL）首当其冲，ATFL 最常伤', LT, TEAL),
    ('ATFL 分上、下两束', '上束：关节内，浸泡在滑液里\n下束：关节外，通过“弓状纤维”与跟腓韧带（CFL）相连，共同构成外侧腓距跟韧带复合体（LFTCL），作为等长的外侧稳定结构', OR, (200, 120, 0)),
    ('上束单独损伤 → “微不稳”', '上束在关节内、可能难以愈合，单独损伤可导致查体不易发现的轻微不稳和慢性前外侧踝痛，称为“微不稳”\nVega 等关节镜下把上束损伤分 4 型：Ⅰ 松弛、Ⅱ 部分撕脱、Ⅲ 完全撕脱、Ⅳ 部分或完全吸收', PK, RED),
    ('这篇想回答', '健康人的 3D MRI 上，能不能分清 ATFL 两束、看到弓状纤维和各韧带之间的连接？', GR, (0, 120, 60)),
])
card('怎么做的（原文方法）', [
    ('对象', '30 名无踝部损伤史的健康志愿者，各扫一侧踝；平均 26.7 岁（20～37），男 14 人\n排除：足踝痛影响活动 >1 周、足踝手术/骨折/应力反应史、近 6 个月不稳症状', LT, TEAL),
    ('扫描', '3T MRI，各向同性 3D 质子密度序列（SPACE），层厚 0.5 mm；踝中立位，矢状面采集后重建轴位、冠状位', OR, (200, 120, 0)),
    ('判读', '两位 20 年以上经验的骨肌放射科医生独立阅片、共识定论\n评估 ATFL 束数和大小、弓状纤维、ATFL/CFL 与 PTFL 的连接、周围血管', GR, (0, 120, 60)),
    ('定位', '前瞻性先导研究，证据等级 Ⅲ', PU, C_NAV),
])
put('x31.jpg', '原文图 1（原图未改动）  解剖标本显示外侧腓距跟韧带复合体。① ATFL 上束　② ATFL 下束　③ 跟腓韧带（CFL）　④ 连接 ATFL 下束与 CFL 的弓状纤维')
put('x44.jpg', '原文图 2（原图未改动）  矢状位 MRI：ATFL 两束。1 = 上束　2 = 下束')
put('x46.jpg', '原文图 3（原图未改动）  矢状位和轴位 MRI：只有一束的 ATFL（1）')
put(sizes(), '据原文结果绘制：双束者上束平均长 18.4 mm、宽 4.7 mm，下束 13.2 mm、2.6 mm（两项 P < 0.001），上束平均长 39%、宽 80.7%；4 个单束踝与上束大小相近。年龄、性别对束数和大小无影响')
put('x64.jpg', '原文图 4（原图未改动）  矢状位 MRI：1 = ATFL 下束，经 2 = 弓状纤维，连到 3 = 跟腓韧带，构成 LFTCL 复合体')
put('x82.jpg', '原文图 5（原图未改动）  轴位 MRI：1 = 距腓前韧带（ATFL）与 2 = 距腓后韧带（PTFL）相连')
put('x84.jpg', '原文图 6（原图未改动）  冠状位 MRI：1 = 跟腓韧带（CFL）与 2 = 距腓后韧带（PTFL）相连')
put('x86.jpg', '原文图 7（原图未改动）  左：矢状位；右：冠状位。1 = ATFL 上束　2 = 两束之间的穿支动脉（来自足背动脉的跗外侧动脉）　3 = ATFL 下束')
put(prevalence(), '据原文表 1 绘制：各结构在 30 个健康踝 MRI 上的检出率')
put(studies(), '据原文讨论整理：层厚越薄，越能看到双束；作者认为至少 75% 的人 MRI 上可见两束')
card('作者怎么解读（原文讨论）', [
    ('单束可能是“旧伤”', '有学者认为单束 ATFL 是既往扭伤后上束损伤、吸收，下束代偿肥厚“伪装”成单束\n本研究单束者大小与上束相近', LT, TEAL),
    ('MRI 可做“分束诊断”', '能分清两束，就有可能在 MRI 上发现上束的单独损伤，用于解释查体没有明显松弛的“微不稳”症状', OR, (200, 120, 0)),
    ('弓状纤维与手术', '弓状纤维能把张力从 ATFL 下束传到 CFL，因此 ATFL 和 CFL 都伤时，只修 ATFL 也可能恢复稳定（前提是 CFL 断在近端、弓状纤维完好）\nMRI 上若弓状纤维已断，单修 ATFL 效果可能变差，或需同时修 CFL', PK, RED),
    ('穿支动脉', '可作为区分上、下束的标志；也可能解释部分扭伤后血肿范围大\n以往解剖研究报道两束之间的血管来自腓动脉，本研究只看到来自足背动脉跗外侧支的', GR, (0, 120, 60)),
])
card('局限（原文）', [
    ('“健康”不等于从没扭过', '只排除了近 6 个月有不稳症状者，可能有人以前扭伤后已愈合——这会影响单束、上束萎缩等发现', LT, TEAL),
    ('仍可能漏看', '即使 3T、0.5 mm 层厚、两位资深医生阅片，很细的下束、弓状纤维或连接纤维仍可能看不到', OR, (200, 120, 0)),
    ('设备门槛', '3T MRI 并非处处都有；样本只有 30 例的先导研究', PK, RED),
])
from PIL import Image
im = Image.open(f'{WORK}/prev.png').convert('RGB'); c = im.resize((900, round(im.height * 900 / im.width))); y0 = max(0, (c.height - 383) // 2); c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok', n - 1)
