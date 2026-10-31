#!/usr/bin/env python3
"""Dalmau-Pastor 等 2024 KSSTA《三角韧带恒定由四束组成》推文配图。
原文为 CC BY 开放获取：原文图 1～8 用 extract_figures.py 导出（work/x*.jpg），编者在编号、骨名缩写旁加中文名称，
放不下的在图下加黑底图例条（均注明“编者中文标注”），输出 work/lb*.jpg 供小红书卡片复用；其余为编者据原文撰写的整理卡和数据图。
共用工具在 ../bridge-review-1/tools/bridgekit.py。用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
FB = lambda s: ImageFont.truetype(FBOLD, s)
BOX, TXT = (15, 30, 45, 190), (255, 236, 140, 255)


def labels(name, items, fs, strip=None, out=None):
    """在原图编号旁加中文名称。items: (x, y, 文字, 锚点)，l=文字在点右侧、r=在点左侧、c=以点为中心，坐标为原图像素。
    strip: 放不下的说明，写在图下新增的黑底条里（每项一行）。"""
    im = k.op(name).convert('RGBA')
    if strip:
        h = round(len(strip) * fs * 1.6 + fs * 1.2); c = Image.new('RGBA', (im.width, im.height + h), (0, 0, 0, 255)); c.paste(im, (0, 0)); top = im.height; im = c
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); f = FB(fs); pad = round(fs * .3)
    for x, y, t, a in items:
        w = d.textlength(t, font=f); x0 = {'l': x, 'r': x - w - 2 * pad, 'c': x - w / 2 - pad}[a]; y0 = y - fs / 2 - pad
        d.rounded_rectangle([x0, y0, x0 + w + 2 * pad, y0 + fs + 2 * pad], pad, fill=BOX)
        d.text((x0 + pad, y0 + pad + fs * .45), t, font=f, fill=TXT, anchor='lm')
    if strip:
        for i, t in enumerate(strip): d.text((round(fs * .8), top + round(fs * .6) + i * fs * 1.6), t, font=f, fill=TXT)
    im = Image.alpha_composite(im, ov).convert('RGB'); im.save(f'{WORK}/{out}.jpg', quality=92); return im



labels('x40.jpg', [(950, 470, '② 打开屈肌支持带', 'c'), (950, 520, '见胫后肌腱、趾长屈肌腱', 'c'), (520, 470, '① 内踝皮肤开窗', 'c'), (520, 520, '见屈肌支持带', 'c'),
                   (1370, 470, '③ 切除这两条肌腱', 'c'), (1790, 470, '④ 小心剥离腱鞘', 'c'), (1790, 520, '暴露三角韧带浅层', 'c')], 30, out='lb40')
labels('x48.jpg', [(640, 330, '踝前关节囊', 'l'), (318, 340, '拇长屈肌腱', 'c'), (1640, 240, '踝前关节囊（掀起）', 'l'), (1495, 398, '胫舟束', 'r')], 30,
       strip=['② 胫舟束　③ 胫弹簧束　④ 胫跟束　⑤ 胫距束后部（深层）', '⑥ 距骨后内侧结节　⑦ 拇长屈肌腱'], out='lb48')
labels('x49.jpg', [(1050, 60, '切断下胫腓联合，把胫骨向内翻开，从关节内看三角韧带深层', 'c')], 32, out='lb49')
labels('x59.jpg', [(2000, 610, '胫舟束', 'r'), (1712, 870, '胫弹簧束', 'c'), (1460, 822, '胫跟束', 'c'), (1312, 604, '胫距束（深层）后部', 'c')], 32,
       strip=['圈内轮廓线勾出内踝的前丘和后丘；括号标出各束范围'], out='lb59')
labels('x70.jpg', [(700, 120, '距骨已移除', 'l'), (1290, 1135, '胫舟束', 'r'), (1390, 1250, '胫弹簧束', 'r'), (1395, 1560, '胫跟束', 'r')], 30,
       strip=['① 胫舟束　② 胫弹簧束　③ 胫跟束', '④ 跟舟内上韧带（弹簧韧带复合体，表面有纤维软骨）'], out='lb70')
labels('x82.jpg', [(450, 60, '胫骨下端前下面观', 'c')], 30,
       strip=['① 胫舟束　② 胫弹簧束　③ 胫跟束（浅层，起于内踝内侧面）', '④ 胫距束（深层，起于内踝外侧面、紧贴关节软骨）', '虚线：关节软骨内侧边界'], out='lb82')
labels('x83.jpg', [(485, 198, '胫舟束', 'l'), (705, 438, '舟骨', 'l'), (445, 612, '弹簧韧带', 'l'), (305, 580, '载距突', 'r'), (222, 528, '距骨后内侧结节', 'c'), (285, 180, '拇长屈肌腱', 'c')], 26,
       strip=['① 胫舟束→舟骨　② 胫弹簧束→弹簧韧带　③ 胫跟束→载距突', '④ 胫距束后部（深层）→距骨后内侧结节　⑤ 拇长屈肌腱'], out='lb83')
labels('x107.jpg', [(1290, 110, '距骨内侧关节面（前宽后窄）', 'l'), (1380, 560, '胫距束止点（后宽前窄）', 'l')], 50, out='lb107')

n = 1
def nxt(im):
    global n; k.save(im, n); n += 1
def put(im, cap):
    im = k.op(im) if isinstance(im, str) else im; nxt(k.capbox(im, cap))
def card(t, items): nxt(k.card(t, items))


nxt(k.title('图解解剖论文 · 《KSSTA》2024', ['三角韧带恒定由四束组成', '舟骨、弹簧韧带、跟骨和距骨'],
            'Dalmau-Pastor M, Malagelada F, Guelfi M, Kerkhoffs G, Karlsson J, Calder J, Vega J.',
            'Knee Surg Sports Traumatol Arthrosc. 2024;32:3065–3075', '西班牙巴塞罗那大学人体解剖与胚胎学教研室；伦敦皇家医院；阿姆斯特丹大学医学中心 等'))
card('为什么要重新数三角韧带（原文引言）', [
    ('踝扭伤后的内侧问题', '踝扭伤大多是内翻扭伤，主要伤外侧韧带（距腓前、跟腓、距腓后）\n但 30%～40% 扭伤后留下慢性疼痛，最多 33% 发展为慢性踝关节不稳；其中最多 40% 合并或继发三角韧带（内侧副韧带）损伤', LT, TEAL),
    ('描述太乱：文献里多达 16 束', '最常用的说法是两层六束：浅层胫舟、胫弹簧（恒定），胫距浅、胫跟（不恒定）；深层胫距后（恒定）、胫距前深（不恒定）\n不同作者又陆续加了多个“新束”，累计 16 种，出现率各不相同', OR, (200, 120, 0)),
    ('带来的问题', '临床报告损伤、修复或重建时说不清到底是哪一部分；研究之间难以比较', PK, RED),
    ('这篇的思路', '多数研究只从关节外看；作者同时从关节外（内侧）和关节内（外侧）观察\n上一篇从关节内观察三角韧带的研究还是 1979 年', GR, (0, 120, 60)),
])
card('怎么做的（原文方法）', [
    ('标本', '32 例新鲜冷冻膝下标本，巴塞罗那大学解剖室，经伦理批准', LT, TEAL),
    ('先看浅层（内侧观）', '① 内踝皮肤开窗 → ② 打开屈肌支持带 → ③ 切除胫后肌腱、趾长屈肌腱 → ④ 小心剥离腱鞘\n⑤ 切除小腿前群肌腱 → ⑥ 解剖前关节囊 → ⑦ 测量浅层', OR, (200, 120, 0)),
    ('再看深层（关节内观）', '⑧ 切断下胫腓联合各韧带和骨间膜，把胫骨向内翻开 → ⑨ 去除滑膜 → ⑩ 测量深层\n不剥离浅层，保证深层完整', GR, (0, 120, 60)),
    ('关键提醒', '第 ③ 步容易误切胫跟束，第 ⑤ 步容易误切胫舟束——这可能是以往研究认为某些束“不恒定”的原因', PK, RED),
])
put('lb40.jpg', '原文图 1（编者中文标注）  浅层的解剖步骤：（a）内踝皮肤开窗见屈肌支持带（b）打开支持带见胫后肌腱、趾长屈肌腱（c）切除两条肌腱（d）小心剥离腱鞘，不破坏韧带')
put('lb48.jpg', '原文图 2（编者中文标注）  踝前关节囊与三角韧带前部的关系。（1）踝前关节囊（2）胫舟束（3）胫弹簧束（4）胫跟束（5）胫距束后部（深层）（6）距骨后内侧结节（7）拇长屈肌腱。右图掀起关节囊，可见胫舟束外缘与关节囊相延续')
put('lb49.jpg', '原文图 3（编者中文标注）  第 8 步：切开下胫腓联合，从关节内侧面观察三角韧带深层')
card('结果：两层、四束、恒定存在', [
    ('浅层：三束长纤维，都起于内踝前丘（关节外）', '胫舟束：前丘前部 → 舟骨上内侧；前部纤维在关节内\n胫弹簧束：前丘中部 → 跟舟内上韧带（弹簧韧带）上缘\n胫跟束：前丘后部 → 跟骨载距突上缘', LT, TEAL),
    ('深层：一束短纤维（关节内）', '胫距束：起于前丘外侧及后丘内外侧，紧贴关节软骨内侧，止于距骨内侧“逗号形”关节面下方的整片区域', OR, (200, 120, 0)),
    ('从表面看能见到四个止点', '舟骨、弹簧韧带、载距突（浅层）+ 距骨后内侧结节（深层胫距束最后部）', GR, (0, 120, 60)),
    ('关节内的部分', '胫距束全部 + 胫舟束前部在关节内（但在滑膜外）；胫舟束后部、胫弹簧束、胫跟束在关节外', PK, RED),
])
put('lb59.jpg', '原文图 4（编者中文标注）  三角韧带全貌，轮廓线为内踝前丘和后丘。（1）胫舟束（2）胫弹簧束（3）胫跟束（4）胫距束后部（深层）')
put('lb70.jpg', '原文图 5（编者中文标注）  浅层解剖（a），移除距骨后的微距照片（b）和描边（c）。（1）胫舟束（2）胫弹簧束（3）胫跟束（4）跟舟内上韧带')
put('lb82.jpg', '原文图 6（编者中文标注）  胫骨下端前下面观，虚线为关节软骨内侧边界：浅层三束起于内踝内侧面，深层胫距束起于外侧（关节内）、紧贴软骨')
put('lb83.jpg', '原文图 7（编者中文标注）  浅表观察能看到的四个止点：（a）舟骨（b）跟舟内上韧带（c）载距突（d）距骨后内侧结节')


def widths():
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.4), dpi=100, gridspec_kw={'width_ratios': [1, 1]})
    for ax, t, labs, pr, di in [(axs[0], '浅层（远端均更宽）', ['胫舟束', '胫弹簧束', '胫跟束'], [4.10, 5.30, 6.31], [14.90, 7.86, 9.83]),
                                (axs[1], '深层胫距束（按起点分三段）', ['前丘前部', '前丘', '后丘'], [5.98, 9.67, 9.66], [10.29, 8.84, 10.48])]:
        x = range(3)
        ax.bar([i - .19 for i in x], pr, .36, color='#9AA5B1', label='近端（胫骨）')
        ax.bar([i + .19 for i in x], di, .36, color='#1F5F8B', label='远端')
        for i in x:
            ax.text(i - .19, pr[i] + .3, f'{pr[i]:g}', ha='center', fontsize=14); ax.text(i + .19, di[i] + .3, f'{di[i]:g}', ha='center', fontsize=14)
        ax.set_xticks(list(x), labs, fontsize=16); ax.set_title(t, fontsize=17); ax.set_ylim(0, 17); ax.set_ylabel('附着宽度均值（mm）', fontsize=13)
        ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=12)
    axs[0].legend(fontsize=13, frameon=False, loc='upper right')
    fig.suptitle('四束的近端与远端附着宽度（据原文表 1、表 2 绘制，n = 32）', fontsize=19, x=.02, ha='left')
    fig.tight_layout(rect=(0, 0, 1, .92)); fig.savefig(f'{WORK}/widths.png', facecolor='white'); plt.close(fig)


widths()
put('widths.png', '据原文表 1、表 2 绘制：浅层三束远端都比近端宽，胫舟束最明显（4.1 → 14.9 mm），呈扇形；深层前丘前部同样向远端展开，前丘和后丘两段则近似直带')
put('lb107.jpg', '原文图 8（编者中文标注）  深层胫距束的距骨止点：距骨内侧关节面呈“逗号形”、前宽后窄；胫距束止点是倒过来的逗号、后宽前窄，两者像太极图一样互补')
card('临床意义（原文讨论）', [
    ('统一术语', '面对一个“最多 16 束、大多不恒定”的结构，医生之间很难交流诊断和治疗\n四束 + 两层的简化描述按“连接哪两块骨”命名，便于报告损伤和规划修复、重建', LT, TEAL),
    ('胫跟束其实恒定', '以往常说它不恒定；作者发现剥离胫后肌腱、趾长屈肌腱腱鞘时极易误切它的纤维', OR, (200, 120, 0)),
    ('深层为什么难愈合（作者假设）', '胫距束和胫舟束前部在关节内、滑膜外，类似膝前交叉韧带和距腓前韧带上束：断后残端可能重新被滑膜包裹，妨碍愈合\n→ 可能解释深层三角韧带损伤更易迁延', PK, RED),
    ('也有有利因素', '踝部韧带两端距离比膝短得多，不完全断裂也常见，保留部分纤维连续性可能有利于愈合；目前没有研究直接证实上述假设', GR, (0, 120, 60)),
    ('并非全新', '四束的描述最早见于 1956 年；本研究是用关节内外两种视角重新确认', PU, C_NAV),
])
card('局限（原文）', [
    ('样本量', '32 例，按可得标本数量纳入，没有做样本量计算', LT, TEAL),
    ('解剖本身有主观性', '逐层解剖受操作者理解影响——这也正是文献描述混乱的原因；本研究由一位资深解剖者按严格流程完成', OR, (200, 120, 0)),
])
im = Image.open(f'{WORK}/lb83.jpg'); c = im.crop((100, 120, 1000, 503)).resize((900, 383), Image.LANCZOS); c.save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
