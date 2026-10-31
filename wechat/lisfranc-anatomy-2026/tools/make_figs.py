#!/usr/bin/env python3
"""Liu、Dalmau-Pastor 等 2026 KSSTA《Lisfranc 关节复合体解剖：图解综述与手术入路》推文配图。
原文为 CC BY 开放获取：原文图 1～6 用 extract_figures.py 导出（work/x*.jpg），编者在编号、骨名缩写旁加中文名称，
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


BONES = ['C1 内侧楔骨 · C2 中间楔骨 · C3 外侧楔骨 · Cu 骰骨', 'M1～M5 第 1～5 跖骨']
labels('x37.jpg', [(503, 722, '中间楔骨', 'c'), (752, 748, '内侧楔骨', 'c'), (277, 832, '外侧楔骨', 'c'), (168, 965, '骰骨', 'c'),
                   (187, 1315, '第 1 跖骨', 'c'), (350, 1273, '第 2 跖骨', 'c'), (497, 1325, '第 3 跖骨', 'c'), (642, 1410, '第 4 跖骨', 'c'),
                   (757, 1500, '第 5 跖骨', 'c'), (62, 1062, '楔骨和骰骨的前关节面', 'l'), (62, 1132, '跖骨基底的后关节面', 'l')], 28, out='lb37')
labels('x38.jpg', [(450, 205, '足背观', 'l'), (578, 366, '骰骨', 'c'), (663, 402, '外侧楔骨', 'c'), (790, 412, '中间楔骨', 'c'), (907, 470, '内侧楔骨', 'c'),
                   (500, 430, '第5跖骨', 'c'), (571, 486, '第4跖骨', 'c'), (658, 522, '第3跖骨', 'c'), (770, 535, '第2跖骨', 'c'), (906, 594, '第1跖骨', 'c')],
       19, strip=BONES, out='lb38')
labels('x39.jpg', [(450, 185, '足底观', 'l'), (790, 313, '骰骨', 'c'), (615, 328, '中间楔骨', 'c'), (692, 404, '外侧楔骨', 'c'), (523, 428, '内侧楔骨', 'c'),
                   (902, 407, '第5跖骨', 'c'), (803, 500, '第4跖骨', 'c'), (725, 540, '第3跖骨', 'c'), (637, 540, '第2跖骨', 'c'), (525, 570, '第1跖骨', 'c')],
       19, strip=BONES, out='lb39')
labels('x63.jpg', [(212, 395, 'C1–M1', 'r'), (337, 383, 'C1–M2', 'l'), (513, 350, 'C2–M2', 'l'), (695, 393, 'C3–M2', 'r'),
                   (820, 393, 'C3–M3', 'l'), (582, 600, 'M2–M3', 'r')], 30,
       strip=['①～⑥ 均为背侧韧带；② C1–M2 即背侧 Lisfranc 韧带', 'C1/C2/C3 内侧/中间/外侧楔骨 · M1～M3 第 1～3 跖骨'], out='lb63')
labels('x64.jpg', [(240, 100, '背侧', 'l'), (188, 248, '骨间', 'r'), (205, 338, '跖侧', 'r')], 28,
       strip=['C1 与 M2 之间的三条 Lisfranc 韧带（M1 已拆下）', '① 背侧　② 骨间　③ 跖侧（分两束，分别止于 M2 和 M3）'], out='lb64')
labels('x96.jpg', [(140, 290, 'C1–C2', 'r'), (275, 285, '骨间 Lisfranc 韧带', 'l'), (228, 378, '内侧楔骨', 'l'), (172, 95, '中间楔骨', 'l'),
                   (612, 190, '第 2 跖骨', 'l')], 26, strip=['① C1–C2 骨间韧带　② 骨间 Lisfranc 韧带（C1–M2）'], out='lb96')

n = 1
def nxt(im):
    global n; k.save(im, n); n += 1
def put(im, cap):
    im = k.op(im) if isinstance(im, str) else im; nxt(k.capbox(im, cap))
def card(t, items): nxt(k.card(t, items))


nxt(k.title('图解解剖综述 · 《KSSTA》2026', ['Lisfranc 关节复合体', '骨、韧带和手术入路，一篇看懂'],
            'Liu X, Hong CC, Torrent J, Del Vecchio J, Alcolea-Madera E, Dalmau-Pastor M.',
            'Knee Surg Sports Traumatol Arthrosc. 2026;34:3178–3185', '西班牙巴塞罗那大学人体解剖与胚胎学教研室；遵义医科大学附属医院；新加坡国立大学医院 等'))
card('Lisfranc 关节复合体是什么（原文引言）', [
    ('不是一个关节，而是一组', '跖跗关节（核心）+ 跗骨间关节 + 近端跖骨间关节，以及连接它们的韧带\n韧带按位置分背侧、骨间、跖侧；按纤维方向分纵行、斜行、横行', LT, TEAL),
    ('名字从哪来', 'Lisfranc 描述的是在跖跗关节水平截肢的术式，后来关节就被叫作“Lisfranc 关节”\n狭义的“Lisfranc 韧带”指连接内侧楔骨（C1）和第 2 跖骨（M2）的背侧、骨间、跖侧韧带\n（1955 年起解剖学名词已不建议用人名命名）', OR, (200, 120, 0)),
    ('Lisfranc 损伤', '泛指累及这些结构的骨折、脱位或单纯韧带扭伤：低能量运动伤或高能量损伤都可能\n常见第 1、2 跖跗关节不稳，伴撕脱骨折（“Fleck 征”）或 C1–M2 间隙增宽', GR, (0, 120, 60)),
    ('两种向近端延伸的亚型', '内侧柱脱位（MCD）：Lisfranc 韧带 + C1–C2 楔间韧带损伤，第 1 跖跗关节韧带完好\n近端延伸脱位（PE）：再加上 C1–M1、C2–M2 韧带损伤，更严重\n两者都属于纵向不稳', PU, C_NAV),
    ('为什么要重视', '没有明显骨折脱位的低能量单纯韧带伤，漏诊、误诊可达 20%\n延误治疗 → 慢性中足不稳、疼痛、关节炎（最常见）、中足畸形', PK, RED),
])
put('lb37.jpg', '原文图 1（编者中文标注）  跖跗关节骨性成分呈弓形排列，背侧凸、足底侧凹。（a）楔骨和骰骨的前关节面（b）五块跖骨基底的后关节面')
put('lb38.jpg', '原文图 2（编者中文标注）  跖跗关节背面观：第 2 跖骨基底同时与 C1、C2、C3、M1、M3 相接触')
put('lb39.jpg', '原文图 3（编者中文标注）  跖跗关节足底面观：三块楔骨的“楔形”在中间楔骨（C2）处最明显，它的足底面很小')
card('骨性结构：为什么第 2 跖骨是“拱顶石”', [
    ('阶梯状、交错排列', '跖跗关节面从第 1 跖骨基底向外、向后错开，前后相差约 20 mm，关节线弯曲，最高点在第 3 跖骨与外侧楔骨（C3）之间', LT, TEAL),
    ('横弓', '第 1～3 跖骨基底呈梯形或三角形：背侧宽、足底窄 → 形成背侧凸、内侧高于外侧的横弓；楔骨和骰骨也同样排成弓形', OR, (200, 120, 0)),
    ('榫卯结构', '第 2 跖骨基底深深嵌在 C1 和 C3 之间（C2 水平），位于横弓顶点，是维持足弓的“拱顶石”\nC1、C3 分别比 M2 基底向前突出约 8 mm 和 4 mm；C3 比骰骨向前突出 ≥2 mm，形成较浅的第二个榫卯', GR, (0, 120, 60)),
    ('关节面细节', 'C1 外侧面有两个小关节面：前上方卵圆形的对 M2，后方倒“L”形的对 C2\nM1 和 M2 基底通常不相关节；M2 内侧对 C1 的关节面靠背侧\n→ 横穿 C1–M2 的螺钉有损伤关节软骨的风险', PK, RED),
])


def risk():
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.6), dpi=100)
    data = [('榫卯内侧深度', '每加深 1 mm', '损伤风险约降低 50%', '#2E8B57'), ('M2 长度 / 足长', '每降低 1%', '损伤风险 ×1.82\n<29% 时尤其易伤', '#C0392B'),
            ('C1–M2 间距（负重像）', '≥2 mm', '提示不稳定损伤', '#1F5F8B')]
    for ax, (t, a, b_, c) in zip(axs, data):
        ax.axis('off'); ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=c, alpha=.1, transform=ax.transAxes))
        ax.text(.5, .82, t, ha='center', fontsize=19, weight='bold', color=c, transform=ax.transAxes)
        ax.text(.5, .55, a, ha='center', fontsize=26, weight='bold', color='#222', transform=ax.transAxes)
        ax.text(.5, .22, b_, ha='center', fontsize=18, color='#333', transform=ax.transAxes, linespacing=1.5)
    fig.suptitle('骨性形态与 Lisfranc 损伤风险（据原文数字整理）', fontsize=20, x=.02, ha='left')
    fig.tight_layout(rect=(0, 0, 1, .9)); fig.savefig(f'{WORK}/risk.png', facecolor='white'); plt.close(fig)


risk()
put('risk.png', '据原文整理：榫卯越深、越宽越稳定；第 2 跖骨相对越短越容易受伤；榫卯外侧深度与损伤风险无明显关系。影像上，C1–M2 间距比 M1–M2 间距更能反映 Lisfranc 韧带损伤')
put('lb63.jpg', '原文图 4（编者中文标注）  稳定第 2 跖骨的背侧韧带：（1）C1–M1（2）背侧 Lisfranc 韧带（C1–M2）（3）C2–M2（4）C3–M2（5）C3–M3（6）M2–M3。注意 M1 和 M2 之间没有韧带')
put('lb64.jpg', '原文图 5（编者中文标注）  拆下第 1 跖骨后，从前方看 C1–M2 之间的三条 Lisfranc 韧带：（1）背侧（2）骨间（3）跖侧，跖侧分一束到 M2、一束到 M3')
card('三条 Lisfranc 韧带（原文）', [
    ('关键背景：M1–M2 之间没有韧带', '外侧几块跖骨基底之间都有背侧、跖侧韧带相连，唯独 M1 和 M2 之间没有，只有薄弱的纤维组织\n→ 这里是天生的薄弱点，C1–M2 的三条韧带就成了关键稳定结构', PK, RED),
    ('背侧 Lisfranc 韧带（DLL）', 'C1 背面外缘 → M2 背面内缘近端；宽梯形，平均长 10.8、宽 8.3、厚 1.36 mm\n最薄、抗拉强度最弱、最容易伤 → 移位多向背侧\n超声看它的完整性，可早期筛查隐匿性 Lisfranc 损伤', OR, (200, 120, 0)),
    ('骨间 Lisfranc 韧带（ILL）', 'C1 外侧（楔间韧带前方）斜向外下 → M2 基底内侧；带状，1～4 束，最常见单束或双束；M2 附着面积约 135 mm²\n最窄但最厚、最强，是复合体的主要稳定结构；大小约为 DLL 的 4.5 倍、PLL 的 2 倍', LT, TEAL),
    ('跖侧 Lisfranc 韧带（PLL）', 'C1 足底前外侧 → M2 近端内下方和 M3 跖侧基底；跖侧主要稳定结构\n多为扇形，少数分浅、深两束：浅束到 M3、更粗更强，深束到 M2', GR, (0, 120, 60)),
])


def biomech():
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.6), dpi=100)
    lig = ['背侧（DLL）', '骨间（ILL）', '跖侧（PLL）']; col = ['#E3A21A', '#C0392B', '#1F5F8B']
    sets = [('刚度（N/mm）', [(66.3, 189.7, None), (40, 90, 62)]), ('失效载荷 / 强度（N）', [(150.7, 368.8, None), (170, 449, 305)])]
    for ax, (t, (a, b_)) in zip(axs, sets):
        for j, (ser, lab, hatch) in enumerate([(a, '研究 A（文献 17）', ''), (b_, '研究 B（文献 33）', '//')]):
            for i, v in enumerate(ser):
                if v is None: ax.text(i + (j - .5) * .38, 5, '无数据', ha='center', fontsize=12, color='#999', rotation=90); continue
                ax.bar(i + (j - .5) * .38, v, .36, color=col[i], alpha=1 if j == 0 else .55, hatch=hatch, edgecolor='white')
                ax.text(i + (j - .5) * .38, v * 1.02, f'{v:g}', ha='center', fontsize=13)
        ax.set_xticks(range(3), lig, fontsize=15); ax.set_title(t, fontsize=17); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=12)
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color='#888', label='实色：研究 A（只测了背侧和骨间）'), Patch(color='#888', alpha=.55, hatch='//', label='浅色斜线：研究 B')],
               loc='upper right', fontsize=13, frameon=False, ncol=2)
    fig.suptitle('三条 Lisfranc 韧带的力学强度（据原文数字绘制）', fontsize=19, x=.02, ha='left')
    fig.tight_layout(rect=(0, 0, 1, .88)); fig.savefig(f'{WORK}/biomech.png', facecolor='white'); plt.close(fig)


biomech()
put('biomech.png', '据原文数字绘制：两项体外生物力学研究都显示，骨间 Lisfranc 韧带最硬、最强，背侧最弱。两项研究的绝对数值差别较大（如骨间韧带刚度 189.7 vs 90 N/mm），原文未解释')
put('lb96.jpg', '原文图 6（编者中文标注）  C1、C2、M2 的内侧观，C1 背侧一半已沿矢状面切开，显示（1）C1–C2 骨间韧带（2）骨间 Lisfranc 韧带')
card('楔间韧带与两种不稳', [
    ('楔间韧带', 'C1–C2–C3 之间：背侧 2 条（C1–C2、C2–C3）、骨间 2 条（C1–C2、C2–C3）、跖侧只有 1 条（C1–C2），C2–C3 之间没有跖侧韧带\nC1–C2 背侧韧带小而方；骨间韧带粗厚、横行，起于 C1 外侧“L”形关节面的拐角', LT, TEAL),
    ('横向不稳', '骨间 + 跖侧 Lisfranc 韧带同时断裂\n外展应力像：C1–M2 和 C2–M2 都不稳', OR, (200, 120, 0)),
    ('纵向不稳', '骨间 Lisfranc 韧带 + C1–C2 骨间韧带断裂\n内收应力像：5 个标本中 1 个 C1–M2 不稳，4 个 C1–C2 不稳\n纵向不稳的 Lisfranc 损伤会累及 C1 和 C2 之间的韧带（即前面的 MCD、PE 亚型）', GR, (0, 120, 60)),
])
card('手术解剖（原文 Surgical anatomy）', [
    ('术前规划', '明确哪些关节不稳、需要固定还是融合；恢复内、外侧柱长度；处理柱间韧带不稳\n软组织包膜薄、易受医源性损伤', PU, C_NAV),
    ('背内侧入路（最常用）', '第 1、2 跖骨之间纵切口，可向近端延至距舟关节、向远端暴露第 1、2 跖骨全长\n遇到：拇长伸肌腱、胫前肌腱、胫前血管神经束（足背动脉 + 腓深神经）\n在拇长伸肌腱和血管神经束之间进入，血管神经束拉向外侧；暴露 M2 骨干时在血管神经束外侧解剖', LT, TEAL),
    ('背外侧入路（累及第 3 跖跗关节或第 4、5 跖骨时加做）', '以骰骨为中心、沿第 4 跖骨轴线，可向近端延至腓骨尖\n遇到：趾短伸肌、腓骨肌腱、腓肠神经和腓浅神经分支——尤其要保护腓肠神经\n两切口之间皮桥至少 5 cm', OR, (200, 120, 0)),
    ('复位顺序', '① 先恢复舟骨与楔骨的关系 → ② M2 对 C2、再对 C1（复位的基石）→ ③ 依次处理第 1、3、4、5 跖跗关节\n这类损伤几乎都有不稳成分，非手术治疗作用很有限', PK, RED),
])


def compare():
    rows = [('位置', 'C1 背面外缘 → M2 背面内缘', 'C1 外侧 → M2 基底内侧', 'C1 足底 → M2 和 M3 跖侧'), ('形态', '宽梯形，最薄', '带状，1～4 束；最窄最厚', '多为扇形，少数分浅深两束'),
            ('强度', '最弱，最易伤', '最强、最硬，主要稳定结构', '居中，跖侧主要稳定结构'), ('临床', '移位多向背侧；超声可筛查', '与 PLL 同断 → 横向不稳', '与 ILL 同断 → 横向不稳')]
    W = 1200; im = Image.new('RGB', (W, 1400), 'white'); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 76], fill=TEAL); d.text((24, 16), '三条 Lisfranc 韧带对比（编者据原文整理）', font=font(36), fill='white')
    y = 96; cx = [20, 130, 486, 842]; cw = 330
    for i, h in enumerate(['', '背侧（DLL）', '骨间（ILL）', '跖侧（PLL）']): d.text((cx[i] + 10, y), h, font=FB(30), fill=RED if i == 2 else INK)
    y += 56
    dd = ImageDraw.Draw(Image.new('RGB', (W, 400)))
    for j, row in enumerate(rows):
        hh = max(k.para(dd, 0, 0, t, 26, cw, gap=8) for t in row[1:]) + 16
        if j % 2 == 0: d.rectangle([20, y - 8, W - 20, y + hh], fill=(244, 247, 249))
        d.text((cx[0] + 10, y + hh / 2 - 22), row[0], font=FB(28), fill=TEAL)
        for c, t in zip(cx[1:], row[1:]): k.para(d, c + 10, y + 4, t, 26, cw, gap=8)
        y += hh + 14
    return im.crop((0, 0, W, y))


nxt(compare())
im = Image.open(f'{WORK}/lb63.jpg'); c = im.crop((60, 180, 900, 537)).resize((900, 383), Image.LANCZOS); c.save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
