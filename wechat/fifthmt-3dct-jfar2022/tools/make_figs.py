#!/usr/bin/env python3
"""He、Zhou 等 2022 J Foot Ankle Res《三维 CT 骨折线图结合解剖测量的第五跖骨基底撕脱骨折分型》推文配图。
原文 CC BY 4.0 开放获取：原文图 1～8（work/x*.jpg，extract_figures.py 导出）中的英文方位词用白底中文覆盖替换、
分型旁加中文名称，放不下的在图下加黑底图例条（均注明“编者中文标注”），输出 work/lb*.jpg 供小红书卡片复用；
其余为编者据原文撰写的整理卡和数据图。
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
BOX, TXT = (15, 30, 45, 200), (255, 236, 140, 255)


def labels(name, items=(), fs=28, strip=None, cover=(), out=None):
    """items: (x, y, 文字, 锚点 l/r/c) 深色小框标注；cover: (x0, y0, x1, y1, 文字, 字号) 白底覆盖原英文并写中文；
    strip: 图下黑底图例条（每项一行）。坐标为原图像素。"""
    im = k.op(name).convert('RGBA')
    if strip:
        h = round(len(strip) * fs * 1.6 + fs * 1.2); c = Image.new('RGBA', (im.width, im.height + h), (0, 0, 0, 255)); c.paste(im, (0, 0)); top = im.height; im = c
    d0 = ImageDraw.Draw(im)
    for x0, y0, x1, y1, t, s in cover:
        d0.rectangle([x0, y0, x1, y1], fill='white'); d0.text(((x0 + x1) / 2, (y0 + y1) / 2), t, font=FB(s), fill=(20, 20, 20), anchor='mm')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); f = FB(fs); pad = round(fs * .3)
    for x, y, t, a in items:
        w = d.textlength(t, font=f); x0 = {'l': x, 'r': x - w - 2 * pad, 'c': x - w / 2 - pad}[a]; y0 = y - fs / 2 - pad
        d.rounded_rectangle([x0, y0, x0 + w + 2 * pad, y0 + fs + 2 * pad], pad, fill=BOX)
        d.text((x0 + pad, y0 + pad + fs * .45), t, font=f, fill=TXT, anchor='lm')
    if strip:
        for i, t in enumerate(strip): d.text((round(fs * .8), top + round(fs * .6) + i * fs * 1.6), t, font=f, fill=TXT)
    im = Image.alpha_composite(im, ov).convert('RGB'); im.save(f'{WORK}/{out}.jpg', quality=92); return im


V5 = [('内侧面', 155), ('外侧面', 568), ('足底面', 972), ('背侧面', 1368), ('后面（近端）', 1772)]
labels('x43.jpg', cover=[(c - 150, 668, c + 150, 721, t, 40) for t, c in V5], fs=40,
       strip=['222 例骨折线叠加在同一个标准化左侧第五跖骨模型上'], out='lb43')
V4 = [('内侧面', 98), ('外侧面', 370), ('足底面', 643), ('背侧面', 920), ('后面', 1177)]
labels('x41.jpg', cover=[(c - 100, 362, c + 100, 400, t, 30) for t, c in V4] + [(1285, 0, 1418, 30, '频数', 24)], fs=24,
       strip=['颜色从蓝到红：该处骨折线出现次数从少到多'], out='lb41')
labels('x55.jpg', fs=26, strip=['a 后缘切线　b 外侧缘切线　c 干骺端内、外附着点连线　d 内侧缘切线', 'e 基底前后径　f 基底横径　g 骨折线到外侧缘切线的距离',
                                 'h 骨折线到后缘切线的距离　i 骨折线（橙色为骨折块）'], out='lb55')
labels('x54.jpg', cover=[(1290, 0, 1181, 0, '', 1)][:0], fs=26, strip=['背侧观热图：骨折线集中在一条弧形带上', '最密集处：距后缘切线 2/5～7/10'], out='lb54')
labels('x71.jpg', fs=26, strip=['腓骨短肌附着区（背外侧，卵圆形）', '长径 12.24 mm、短径 6.88 mm；内缘距第 4/5 跖间关节面 2.90 mm'], out='lb71')
labels('x70.jpg', fs=26, strip=['跖腱膜外侧束附着区（包绕结节，卵圆形）', '宽 10.13 mm、高 7.25 mm'], out='lb70')
labels('x94.jpg', fs=40, strip=['a 跖腱膜外侧束为主（48 例）', 'b 腓骨短肌为主（54 例）　c 两者共同作用（120 例）'], out='lb94')
labels('x108.jpg', [(12, 68, '跖腱膜外侧束为主', 'l'), (378, 68, '腓骨短肌为主', 'l'), (742, 68, '两者共同·1 条骨折线', 'l'), (1102, 68, '两者共同·2 条骨折线', 'l')], 22,
       strip=['上排：分型示意图　下排：对应患者的三维 CT 重建'], out='lb108')

n = 1
def nxt(im):
    global n; k.save(im, n); n += 1
def put(im, cap):
    im = k.op(im) if isinstance(im, str) else im; nxt(k.capbox(im, cap))
def card(t, items): nxt(k.card(t, items))


nxt(k.title('回顾性病例系列 · 《J Foot Ankle Res》2022', ['第五跖骨基底撕脱骨折', '222 例三维骨折线图 + 解剖，提出新分型'],
            'He W, Zhou H, Zhang Y, Yu T, Xia J, Zhao Y, Yang Y, Li B.', 'J Foot Ankle Res. 2022;15:65', '同济大学附属同济医院骨科'))
card('为什么要研究这个（原文背景）', [
    ('很常见', '跖骨骨折每年约 67/10 万人，其中 70% 是第五跖骨骨折；撕脱骨折占第五跖骨骨折的三分之二\n不处理可能遗留顽固疼痛、跖痛症', LT, TEAL),
    ('怎么伤的', '后足内翻 + 前足跖屈时，第五跖骨特殊的结构把力导向基底 → 撕脱\n基底附着有腓骨短肌、第三腓骨肌、跖腱膜外侧束', OR, (200, 120, 0)),
    ('现有分型不够用', 'Ekrol 分型：Ⅰ 结节尖撕脱、Ⅱ 斜行入跖骰关节、Ⅲ 横行过第 4/5 跖骨基底交界\nMehlhorn 分型：按骨折线进入关节的位置（外/中/内 1/3）+ 是否移位 >2 mm\n但临床上有双骨折线、跨区、弯折的骨折线，现有分型描述不了', PK, RED),
])
card('怎么做的（原文方法）', [
    ('病例', '2015.8—2020.8 同济医院 222 例急性第五跖骨基底撕脱骨折，≥18 岁\n排除合并足部其他骨折、开放/病理/陈旧骨折、足畸形或足部手术史', LT, TEAL),
    ('三维骨折线图', '64 排 CT（层厚 0.625 mm）→ Mimics 三维重建 → 每例骨折线画到标准化第五跖骨模型上 → 222 例叠加 → 转成热图', OR, (200, 120, 0)),
    ('尸体解剖', '8 侧成人冰冻标本（亚洲人），游标卡尺（精度 0.02 mm）测关节面、腓骨短肌、跖腱膜外侧束、第三腓骨肌的附着位置和大小', GR, (0, 120, 60)),
    ('两相对照', '把骨折线集中的区域和肌腱/筋膜的附着区比对，推断是谁“拉”出了骨折', PU, C_NAV),
])
put('lb43.jpg', '原文图 1（编者中文标注）  222 例骨折线的三维叠加图（左侧第五跖骨模型），五个方向观')
put('lb41.jpg', '原文图 2（编者中文标注）  骨折线热图，红色＝骨折线最集中')
put('lb55.jpg', '原文图 3（编者中文标注）  在背侧观上定位骨折线的测量方法')
put('lb54.jpg', '原文图 4（编者中文标注）  背侧观热图：骨折线集中在一条弧形带，从距后缘 1/4～4/5 处起、紧贴外侧缘开始、几乎到内侧缘结束；最密集处在 2/5～7/10')
put('lb71.jpg', '原文图 5（编者中文标注）  腓骨短肌在第五跖骨基底背侧的附着区')
put('lb70.jpg', '原文图 6（编者中文标注）  跖腱膜外侧束在第五跖骨结节的附着区')


def anat():
    rows = [('腓骨短肌', 5.70, '背外侧，卵圆形\n12.24 × 6.88 mm'), ('跖腱膜外侧束', 6.65, '包绕结节，卵圆形\n10.13 × 7.25 mm'), ('第三腓骨肌', 3.31, '基底远端背侧，较小\n8 例中 1 例缺如')]
    f, ax = plt.subplots(figsize=(12, 4.8), dpi=100)
    for i, (a, v, t) in enumerate(rows):
        y = 2 - i; ax.barh(y, v, .6, color=['#1F5F8B', '#2E8B57', '#9AA5B1'][i]); ax.text(v + .1, y, f'{v:g} mm', va='center', fontsize=17, weight='bold')
        ax.text(8.6, y, t, va='center', fontsize=14, color='#444')
    ax.set_yticks(range(3), [r[0] for r in rows][::-1], fontsize=17); ax.set_xlim(0, 11.5); ax.set_xlabel('止点近端 1 cm 处的腱径（代表强度）', fontsize=14)
    ax.spines[['top', 'right']].set_visible(False); ax.set_title('三条附着结构（8 侧标本，据原文表 3～5 绘制）', fontsize=19, loc='left', pad=10)
    f.tight_layout(); f.savefig(f'{WORK}/anat.png', facecolor='white'); plt.close(f)


anat()
put('anat.png', '据原文表 3～5 绘制：跖腱膜外侧束和腓骨短肌粗壮、附着在基底背外侧；第三腓骨肌细、附着更远，作者认为它在撕脱骨折中作用不大')
card('解剖测量结果（原文表 2～5）', [
    ('基底形态', '后面观呈三角形（8 例均是）\n内侧第 4/5 跖间关节面：宽 9.59、高 10.90 mm\n跖跗关节面：宽 15.14、高 13.83 mm；非关节面：宽 8.33、高 11.62 mm', LT, TEAL),
    ('腓骨短肌', '附着于基底背外侧，背侧观卵圆形；近缘挨着跖跗关节面，外缘挨着跖腱膜外侧束\n腱径 5.70 mm', OR, (200, 120, 0)),
    ('跖腱膜外侧束', '紧贴腓骨短肌外缘、包绕结节，侧面观卵圆形；腱径 6.65 mm（三者最粗）', GR, (0, 120, 60)),
    ('第三腓骨肌', '附着在基底远端背侧，附着区小；腱径 3.31 mm；1 例缺如', PU, C_NAV),
])
put('lb94.jpg', '原文图 7（编者中文标注）  按损伤机制分别作热图：骨折块正好落在跖腱膜外侧束和/或腓骨短肌的附着区')
put('lb108.jpg', '原文图 8（编者中文标注）  基于损伤机制的新分型')
card('新分型（原文）', [
    ('Ⅰ 型：近端骨折线（48 例）', '主要由跖腱膜外侧束牵拉', LT, TEAL),
    ('Ⅱ 型：中间骨折线（54 例）', '主要由腓骨短肌牵拉', OR, (200, 120, 0)),
    ('Ⅲ 型：远端骨折线（120 例）', '腓骨短肌 + 跖腱膜外侧束共同作用\nⅢA：一条骨折线　ⅢB：两条骨折线', PK, RED),
    ('优点（作者观点）', '按损伤机制分型，能描述双骨折线、跨区等特殊类型，帮助推断是哪条软组织拉的', GR, (0, 120, 60)),
])
card('对治疗的提示（原文讨论）', [
    ('Ⅲ 型移位 ≥2 mm 建议手术', '附带随访 30 例保守治疗 3 个月，5 例再移位，全部是 Ⅲ 型\n理由：两条软组织同时牵拉，再移位、不愈合风险高；Ⅲ 型几乎都累及关节面，保守可能留下创伤性关节炎', PK, RED),
    ('Ⅰ 型要查腓骨短肌', '10 例 Ⅰ 型患者主动要求手术，检查发现都在外踝尖处合并腓骨短肌断裂——可能是肌腱自身断裂缓冲了它对骨的拉力\n→ Ⅰ 型患者建议用 MRI 或超声检查腓骨短肌是否完整', OR, (200, 120, 0)),
    ('局限', '解剖标本仅 8 侧；患者和标本都来自国内；没有做测量可靠性检验；分型仍需临床和生物力学研究验证', LT, TEAL),
])


def counts():
    f, axs = plt.subplots(1, 2, figsize=(13, 4.8), dpi=100)
    for ax, t, labs, v, col in [(axs[0], '本研究新分型', ['Ⅰ 型', 'Ⅱ 型', 'Ⅲ 型'], [48, 54, 120], ['#2E8B57', '#1F5F8B', '#C0392B']),
                                (axs[1], '原有 Ekrol 分型（表 1）', ['Ⅰ', 'Ⅱ', 'Ⅲ', '特殊型'], [90, 39, 54, 39], ['#9AA5B1'] * 3 + ['#E3A21A'])]:
        ax.bar(range(len(v)), v, .6, color=col)
        for i, x in enumerate(v): ax.text(i, x + 2, f'{x}（{x / 222 * 100:.1f}%）', ha='center', fontsize=14)
        ax.set_xticks(range(len(v)), labs, fontsize=16); ax.set_title(t, fontsize=18); ax.set_ylim(0, 140); ax.spines[['top', 'right']].set_visible(False)
    f.suptitle('同一批 222 例，两种分型的分布（据原文表 1 和图 7）', fontsize=18, x=.02, ha='left'); f.tight_layout(rect=(0, 0, 1, .9))
    f.savefig(f'{WORK}/counts.png', facecolor='white'); plt.close(f)


counts()
put('counts.png', '据原文绘制：按原有 Ekrol 分型有 17.6% 归不进去（特殊型）；新分型中 Ⅲ 型（两条软组织共同作用）最多，占 54%')
im = Image.open(f'{WORK}/lb108.jpg').convert('RGB'); c = im.crop((0, 0, 1418, 603)).resize((900, 383), Image.LANCZOS); c.save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
