#!/usr/bin/env python3
"""溝田・壇 2025《足関節果部骨折に対する機能解剖学に基づく理学療法》(理学療法ジャーナル 59(5):572-587) 推文配图。
原文非开放获取（©医学書院）：原文图按 PDF 版面原样截取（work/fig*.jpg，extract_figures.py --clip），不改动图像，说明写在图上方的中文图注里；
图 11 流程图、表 1、表 2 由编者据原文重绘为中文。用法：python3 make_figs.py <work> <输出目录> <中号字体> <粗体>"""
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
B, O, G, P = TEAL, (200, 120, 0), (0, 120, 60), RED
n = 1
def nxt(im):
    global n; k.save(im, n); n += 1
def capbox(im, cap, W=1200):
    """图注在图上方（支持 \\n 分段），原图不做任何改动"""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS); segs = cap.split('\n')
    dd = ImageDraw.Draw(Image.new('RGB', (W, 3000))); y = 14
    for s_ in segs: y = k.para(dd, 14, y, s_, 28, W - 30, gap=12)
    hh = y + 4; t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); y = 14
    for i, s_ in enumerate(segs): y = k.para(dr, 14, y, s_, 28, W - 30, fill=TEAL if i == 0 else INK, gap=12)
    t.paste(im, (0, hh + 8)); return t
def put(f, cap): nxt(capbox(k.op(f), cap))
def card(t, items): nxt(k.card(t, items))

nxt(k.title('特集 · 《理学療法ジャーナル》2025', ['踝关节骨折后背屈受限', '从功能解剖到评估与治疗'],
            '溝田丈士（副島整形外科病院）, 壇 順司（帝京大学福岡医療技術学部）', '理学療法ジャーナル. 2025;59(5):572-587',
            '日本医学書院期刊，非开放获取'))                                                                   # 1
card('先说结论（原文要点）', [
    ('背屈为什么重要', '步行、起立、下蹲和运动都需要足够背屈；骨折后背屈受限与疗效相关，踝关节骨折约 20% 疗效不佳', LT, B),
    ('正常背屈两件事', '非负重：距骨滑车嵌入踝穴，距骨内侧结节向后突出\n负重：距下关节和 Chopart 关节外翻、内侧纵弓下降', OR, O),
    ('别漏了拇长屈肌（FHL）', 'FHL 走在距骨后方，是背屈受限的重要因素；可用 FHL excursion test 评估', PK, P),
    ('按“病态功能解剖”推理', '把骨折、韧带损伤、手术、免负重/固定对功能的影响逐层理清，再决定评估和治疗', GR, G),
])                                                                                                  # 2
put('fig1ab.jpg', '原文图 1a、b  距骨在跖屈 / 背屈时的位置（尸体标本）\na 跖屈：距骨滑车从踝穴向前突出（橙圈），踝穴与距骨滑车间出现间隙（浅橙箭头）\nb 背屈：距骨滑车嵌入踝穴并被锁定\n约在跖屈 27.1±2.3° 以上（向背屈方向），距骨滑车嵌入踝穴')  # 3
put('fig1c12.jpg', '原文图 1c ①②  距骨滑车嵌入踝穴的过程（X 线）')                                  # 4
put('fig1c3.jpg', '原文图 1c ③  嵌入后继续背屈：距骨内侧突起向踝穴后方突出，胫骨后下缘与跟骨结节上端的距离拉长（橙线）→ 走在关节后方的 FHL 要足够柔软，跟腱要能向远端滑动')  # 5
put('fig2.jpg', '原文图 2  背屈时的动态触诊要点\na 前方：距骨滑车外侧部，位于第三腓骨肌腱与外踝之间（蓝箭头）；跗骨窦在外踝下端前方约 2 横指（黄箭头）。看背屈时它能否顺畅嵌入踝穴\nb 后方：距骨内侧结节，在跟腱前方、FHL（红线）与趾长屈肌腱（蓝线）之间（黑箭头）；沿胫骨后肌腱向远端可摸到舟骨结节（绿箭头）。正常背屈时手指会被向后推出\nb③⑤ 超声：与跖屈相比，背屈时胫骨后下缘（黄）与距骨内侧结节（粉）的距离变长')  # 6
card('负重位背屈：还要“外翻 + 降足弓”', [
    ('关节', '除距小腿关节外，还需距下关节、Chopart 关节、Lisfranc 关节参与', LT, B),
    ('怎么动', '负重时距下关节、Chopart 关节外翻更大，内侧纵弓下降：小腿内旋（距骨在跟骨上内旋、跖屈），距骨头压向跟舟足底韧带', OR, O),
    ('需要的柔韧性', '足长延长 → 足底腱膜、拇展肌、拇短屈肌等要足够柔软', GR, G),
])                                                                                                  # 7
put('fig3ab.jpg', '原文图 3a、b  负重背屈时的骨骼运动\n与站立位（a）相比，负重背屈（b）时距骨外侧突与跟骨沟外侧部相接、跗骨窦闭合：小腿内旋，距下关节、Chopart 关节外翻，足弓下降（图中日文：立位＝站立位，荷重位背屈＝负重背屈，距骨の外側突起＝距骨外侧突，踵骨溝の外側部＝跟骨沟外侧部）')  # 8
put('fig3cd.jpg', '原文图 3c、d  内翻位（c）与外翻位（d）的 CT（① 内侧、② 外侧、③ 足底观）\n① 外翻时可见距骨头内侧部，载距突与舟骨结节间变宽，距骨头在此与跟舟足底韧带相接\n② 外翻时跟骨沟外侧部与距骨外侧突无间隙，跗骨窦闭合 —— 距骨在跟骨上内旋\n③ 外翻时距骨头与足底侧的跟舟足底韧带相接')  # 9
put('fig4.jpg', '原文图 4  外翻时的动态触诊要点\na 跗骨窦：内翻位（①）示指尖可伸入跗骨窦；外翻位（②）距骨在跟骨上跖屈、内旋，间隙变窄，指尖被推出\nb 舟骨结节：内翻位（①）内踝与舟骨靠近；外翻位（②）舟骨离开内踝')  # 10
card('背屈受限因素', [
    ('外伤后', '关节肿胀、疼痛；骨赘、骨关节炎等结构异常会导致骨性撞击', LT, B),
    ('腓肠肌、比目鱼肌', '伸膝背屈时弹性（僵硬度）由高到低：腓肠肌内侧头 > 外侧头 > 比目鱼肌；屈膝时比目鱼肌最高；均在肌腹远端（肌腱移行部）最高 → 要在不同膝位评估', OR, O),
    ('拇长屈肌（FHL）', '起于腓骨远端 2/3，踝关节水平紧贴后关节囊，经载距突下方、与趾长屈肌在足底交叉（Henry 结）后止于拇趾\n张力会限制背屈时距骨内侧结节向后突出；周围脂肪多（参与 Kager 脂肪垫），外伤炎症和制动会影响其滑动\n还可能与趾长屈肌、足底方肌相连 → 间接影响足底柔韧性', PK, P),
])                                                                                                  # 11
put('fig5.jpg', '原文图 5  拇长屈肌（FHL）的走行（左踝后面观，尸体标本）\na 已切除跟腱和小腿三头肌：FHL 起于腓骨后缘（箭头）\nb 再切除小腿骨：FHL 走在距骨内侧结节与后外侧结节之间\nc b 的水平面观：FHL 腱走在距骨后方 → 限制背屈时距骨向后下方滑动')  # 12
put('fig6.jpg', '原文图 6  FHL 柔韧性检查（FHL excursion test）\n屈膝 90°、踝关节最大背屈，固定第 1 跖骨头不让其跖屈，再伸拇趾，测拇趾相对足底的伸展角度；<20° 判为 FHL 柔韧性下降')  # 13
card('踝关节骨折：先看骨折，再看周围组织', [
    ('流行病学', '约占全部骨折 10%，是踝周最常见的骨折；骨折修复良好但疗效不佳的约 20%', LT, B),
    ('分型', '按骨折踝数：单踝 / 双踝 / 三踝\nDanis-Weber：按腓骨骨折高度\nLauge-Hansen：结合骨折形态和韧带损伤的受伤机制\n→ 越重、损伤组织越多，症状和背屈受限越明显', OR, O),
    ('踝周肌腱', '外踝后外侧：腓骨长、短肌腱\n内踝后内侧：胫骨后肌、趾长屈肌腱\n后踝后方：FHL 腱\n→ 肿胀压迫、疼痛引起的防御性收缩、固定后粘连和肌萎缩 / 短缩，都会加重背屈受限', PK, P),
])                                                                                                  # 14
put('fig7.jpg', '原文图 7  踝周肌腱与组织（经内、外踝中部的冠状面后方切面示意）\n外踝外下方：腓骨长、短肌腱紧邻跟腓韧带；内踝内下方：胫骨后肌、趾长屈肌腱紧邻三角韧带（胫跟部）\n（图中日文：内果＝内踝，外果＝外踝，靱帯＝韧带，腓骨筋腱＝腓骨肌腱，後脛骨筋腱＝胫骨后肌腱，長趾屈筋腱＝趾长屈肌腱）')  # 15
put('fig8.jpg', '原文图 8  病例影像（20 多岁女性）\na X 线（① 术前、③ 术后）、CT（②）：单纯外踝骨折，Danis-Weber B 型，Lauge-Hansen 旋后外旋型（SER）2 期\nb 下胫腓前韧带超声：与健侧（①）相比，患侧（②）纤维结构不规则（箭头）、呈低回声')  # 16
card('病例与评估（术后第 60 天）', [
    ('病例', '20 多岁女性，外踝骨折合并下胫腓韧带损伤；术后免负重 21 天，固定 14 天', LT, B),
    ('主诉', '走路、下楼梯时踝前方痛：踝前外侧、下胫腓前韧带附近，NRS 4/10', OR, O),
    ('压痛', '下胫腓前关节、比目鱼肌远端、腓骨长短肌、FHL', PK, P),
    ('评估项目', '非负重伸膝 / 屈膝背屈、负重背屈（图 9）；外翻活动度、FHL excursion test、负重背屈时足弓下降、超声下距骨内侧结节后突（图 10）', GR, G),
])                                                                                                  # 17
put('fig9.jpg', '原文图 9  病例的背屈活动度\na 非负重伸膝　b 非负重屈膝　c 负重屈膝\n① 健侧　② 患侧（治疗前）　③ 患侧（治疗后）')  # 18
put('fig10abc.jpg', '原文图 10a–c  各功能评估（① 健侧、② 患侧治疗前、③ 患侧治疗后）\na 外翻活动度　b FHL excursion test　c 负重背屈时足弓下降')  # 19
a, b = Image.open(f'{WORK}/fig10d12.jpg'), Image.open(f'{WORK}/fig10d3.jpg')
d = Image.new('RGB', (a.width, a.height + b.height + 10), 'white'); d.paste(a, (0, 0)); d.paste(b, ((a.width - b.width) // 2, a.height + 10)); d.save(f'{WORK}/fig10d.jpg')
put('fig10d.jpg', '原文图 10d  背屈时距骨内侧结节的后突（超声；① 健侧、② 患侧治疗前、③ 患侧治疗后）\n（图中日文：距骨内側結節＝距骨内侧结节，脛骨後下縁＝胫骨后下缘）')  # 20

# ---------- 原文图 11 流程图：编者据原文重绘中文版 ----------
def flow():
    W = 1200; im = Image.new('RGB', (W, 1700), 'white'); dr = ImageDraw.Draw(im)
    F = lambda s, bold=False: ImageFont.truetype(FBOLD if bold else FM, s); ORG = (230, 110, 20)
    def box(x0, y0, x1, lines, fill='white', bold0=False, col=INK, fs=26):
        h = 24 + len(lines) * (fs + 12); dr.rectangle([x0, y0, x1, y0 + h], fill=fill, outline=INK, width=2)
        for i, t in enumerate(lines):
            f = F(fs, bold0 and i == 0); dr.text(((x0 + x1) / 2, y0 + 14 + i * (fs + 12) + fs / 2), t, font=f, fill=col, anchor='mm')
        return y0 + h
    def ln(*pts): dr.line(pts, fill=ORG, width=4)
    dr.text((W / 2, 30), '原文图 11 病态解释与背屈受限流程图（编者中文重绘）', font=F(30, True), fill=TEAL, anchor='mm')
    y = box(40, 70, W - 40, ['外踝骨折', 'Danis-Weber B 型，Lauge-Hansen SER-2 期'], bold0=True)
    ln(600, y, 600, y + 30); ln(180, y + 30, 1020, y + 30)
    for x in (180, 600, 1020): ln(x, y + 30, x, y + 50)
    y1 = y + 50
    box(40, y1, 330, ['骨损伤']); box(440, y1, 760, ['下胫腓韧带损伤']); yb = box(870, y1, W - 40, ['关节肿胀', '腓骨短肌损伤？'])
    ln(180, y1 + 62, 180, y1 + 92); y2 = box(40, y1 + 92, 330, ['手术'])
    ln(1020, yb, 1020, y2 + 30); ln(180, y2, 180, y2 + 30)
    y3 = box(40, y2 + 30, 560, ['免负重 · 固定']); box(870, y2 + 30, W - 40, ['疼痛'])
    yA = box(190, y3 + 40, 520, ['皮肤切开、腓骨短肌切离', '钢板固定', '→ 疼痛'], fs=24); ln(355, y3, 355, y3 + 40)
    yB = box(580, y3 + 40, W - 40, ['下胫腓关节不稳定', '· 向外下方不稳', '· 背屈时距骨滑车嵌入踝穴难以制动', '· 负重及外旋、外翻方向难以制动'], bold0=True, fs=24); ln(600, y1 + 62, 600, y3 + 40)
    y4 = max(yA, yB) + 40; ln(355, yA, 355, y4); ln(800, yB, 800, y4); ln(1100, y2 + 92, 1100, y4)
    y5 = box(330, y4, W - 40, ['腓骨长、短肌防御性收缩或紧张', '腓骨长、短肌滑动不全'], fs=24)
    ln(150, y3, 150, y5 + 40); ln(745, y5, 745, y5 + 40)
    y6a = box(40, y5 + 40, 400, ['肌萎缩、短缩', '小腿肌萎缩、短缩', '足底腱膜柔韧性下降', '足内在肌萎缩、短缩'], bold0=True, fs=23)
    y6b = box(430, y5 + 40, W - 40, ['FHL 的功能代偿', 'FHL 代偿性紧张，以免胫腓韧带受力：', '· 限制距骨滑车嵌入踝穴', '· 使足处于内旋、内翻位，减轻胫腓关节负荷'], bold0=True, fs=23)
    y7 = max(y6a, y6b) + 40; ln(220, y6a, 220, y7 + 30); ln(800, y6b, 800, y7)
    y8 = box(330, y7, W - 40, ['距骨滑车向后突出受限 · 外翻受限 → 足弓难以下降'], fs=25); ln(220, y7 + 30, 330, y7 + 30)
    ln(745, y8, 745, y8 + 30)
    dr.rectangle([40, y8 + 30, W - 40, y8 + 100], fill=ORG); dr.text((W / 2, y8 + 65), '非负重位 · 负重位背屈受限', font=F(30, True), fill='white', anchor='mm')
    return im.crop((0, 0, W, y8 + 130))
fl = flow(); fl.save(f'{WORK}/flow.jpg'); nxt(fl)                                                   # 21
card('病例为什么背屈受限（原文解释）', [
    ('外踝后方的腓骨肌', '外踝在下胫腓关节水平螺旋形骨折 → 后方腓骨长短肌过度防御性收缩；手术切口和皮下钢板再压迫腓骨短肌 → 柔韧性下降、滑动障碍', LT, B),
    ('下胫腓不稳 → FHL 代偿', '下胫腓韧带损伤使关节向外下方不稳，腓骨肌被迫更紧张；为避免胫腓韧带受力，作用相反的 FHL（把距骨向前推、使足内翻）过度紧张；腓骨肌与 FHL 紧密相连', OR, O),
    ('负重背屈', '免负重和固定使足底腱膜、拇展肌、拇短屈肌变僵，加上 FHL 僵硬 → 外翻受限、足弓降不下来（FHL 试验阳性；负重背屈时拇趾屈曲、舟骨不下降）', PK, P),
    ('结果', '距骨滑车嵌不进踝穴、距骨内侧结节不能向后突出 → 背屈受限，背屈时前方软组织受挤压 → 前方疼痛', GR, G),
])                                                                                                  # 22
put('fig12a.jpg', '原文图 12a  治疗（一）：FHL 与腓骨肌\n① 在比目鱼肌深层投影出 FHL\n② 隔着比目鱼肌，手指插入 FHL 与前方腓骨短肌之间，向前加压并内外移动（黄箭头），改善柔韧性和肌间滑动\n③ 在跟腱正前方压住 FHL，被动伸趾（蓝箭头），踝最大背屈、趾伸展位下从距骨前方向后加压，引导距骨向后滑动（白箭头），进一步牵伸 FHL')  # 23
put('fig12bcd.jpg', '原文图 12b–d  治疗（二）：足底与负重位\nb 固定跖骨头不让其跖屈，伸展足趾（蓝箭头）：牵伸 FHL、趾长屈肌、足底腱膜和足内在肌\nc 负重背屈，把距骨滑车外侧部向后推；强调小腿内旋、足外翻（①），引导内侧纵弓下降（②）\nd 负重下被动伸拇趾，再前倾小腿做负重背屈（①），同时强调足外翻、降足弓（②）')  # 24
card('治疗思路（原文）', [
    ('稳定下胫腓', '用贴扎被动稳定胫腓关节，纠正其向后外下方的偏移，减少肌肉过度牵拉', LT, B),
    ('松解压痛肌', '对腓骨长短肌、比目鱼肌、FHL 做手法治疗，改善柔韧性和肌腱滑动（图 12a）', OR, O),
    ('关节活动练习', '背屈时让距骨滑车碰到外踝后“钻进”踝穴，再从前向后下方加压引导距骨后滑；同时让 FHL 处于紧张位，牵伸关节后方组织', PK, P),
    ('外翻 + 足底', '改善距下关节、Chopart 关节外翻活动度；牵伸与 FHL 相连的趾长屈肌、足底方肌，以及足底腱膜、拇展肌、拇短屈肌（图 12b）', GR, G),
    ('负重位', '非负重改善后，在负重位下徒手降足弓、把距骨向后推、牵伸 FHL（图 12c、d）', LT, B),
])                                                                                                  # 25
# 表 2 柱状图
items = ['非负重伸膝背屈', '非负重屈膝背屈', '负重背屈', '外翻', '拇趾伸展角']
v = [(10, 2, 7), (21, 10, 17), (47, 23, 38), (10, -3, 6), (23, 5, 16)]
fig, ax = plt.subplots(figsize=(12, 6.4), dpi=100); import numpy as np; x = np.arange(len(items)); w = .26
for j, (lab, c) in enumerate([('健侧', '#9aa5b1'), ('患侧治疗前', '#e4572e'), ('患侧治疗后', '#17807e')]):
    bars = ax.bar(x + (j - 1) * w, [t[j] for t in v], w, label=lab, color=c)
    for r, val in zip(bars, [t[j] for t in v]): ax.text(r.get_x() + r.get_width() / 2, val + (1 if val >= 0 else -5), str(val), ha='center', fontsize=17)
ax.set_ylim(-10, 60); ax.set_xticks(x); ax.set_xticklabels(items, fontsize=18); ax.axhline(0, color='#333', lw=1); ax.set_ylabel('角度（°）', fontsize=18)
ax.legend(fontsize=17, frameon=False, ncol=3, loc='upper right'); ax.spines[['top', 'right']].set_visible(False); ax.tick_params(axis='y', labelsize=16)
ax.set_title('原文表 2  活动度变化（2 周、2 次徒手治疗 + 自我训练）', fontsize=20, color='#00606e', loc='left', pad=14)
fig.tight_layout(); fig.savefig(f'{WORK}/table2.png'); nxt(Image.open(f'{WORK}/table2.png'))           # 26
card('原文对不上的地方', [
    ('FHL excursion test 的出处', '正文说这一检查见文献 16，图 6 的 20° 判定标准也引 16；但文献 16 是 FHL 腱鞘炎的临床研究，评估 FHL 滑移的方法学论文是文献 15', OR, O),
    ('术语前后不一', '同一结构交替写作“果間関節窩”和“果関節窩”（踝穴），“距骨内側結節”和“距骨の内側突起”', LT, B),
    ('文献 14 卷号', 'Le Sant 等 2017 发表于 J Anat 第 230 卷，原文写成“2017;30:639-650”', PK, P),
])                                                                                                  # 27
im = Image.open(f'{WORK}/fig2.jpg'); im.crop((0, 0, im.width, round(im.width * 383 / 900))).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok', n - 1)
