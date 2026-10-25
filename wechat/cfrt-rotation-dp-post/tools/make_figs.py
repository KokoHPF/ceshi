#!/usr/bin/env python3
"""Post 等 2023《用颈椎屈曲旋转试验确认颈痛患者的旋转方向偏好：病例系列》（Cureus）推文配图。
原文 © 2023 Post et al.，CC BY 4.0，允许改编：
- 原文图 1～5、8、9 是检查和治疗照片，图内没有英文或缩写，原样引用（只等比缩放），中文图注放在图外上方色条里；
- 原文图 6、7、10 是同一张结局柱状图（三张图像素完全相同），按原图数值用中文重绘一次；
- 首图、决策流程卡、三例速览卡、临床要点卡和封面为编者绘制。
用法：python3 tools/make_figs.py src images <中文字体>"""
import re
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50); ORG = (215, 120, 20)
GRN = (0, 120, 60); PUR = (110, 70, 190); BLU = (40, 90, 170)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)
BL = (230, 238, 250)


def raw(n):
    return Image.open(f'{SRC}/fig{n}.jpg').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=90)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    # 英文单词、数字整体换行；标点不放行首
    for tok in re.findall(r"[A-Za-z0-9.%\-+/～±≥≤°]+|.", t):
        if line and dr.textlength(line + tok, font=font(fs)) > w and tok not in '，。；：、）”°':
            dr.text((x, y), line.rstrip(), font=font(fs), fill=fill); y += fs + gap; line = tok.lstrip()
        else: line += tok
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=900, img_w=None):
    """原图等比缩放（不改内容）放在下方居中，中文图注放在图外上方的色条里"""
    iw = img_w or W
    im = im.resize((iw, round(im.height * iw / im.width)), Image.LANCZOS)
    def lay(dr):
        y = 14
        for seg in cap.split('\n'): y = para(dr, 16, y, seg, 28, W - 34, fill=TEAL, gap=11)
        return y + 4
    hh = lay(ImageDraw.Draw(Image.new('RGB', (W, 3000))))
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); lay(dr)
    t.paste(im, ((W - iw) // 2, hh + 8)); return t


def card(W, title, blocks, fs=28):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 6000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100; tx = 50
    for h, t, c, a in blocks:
        top = y; dd = ImageDraw.Draw(Image.new('RGB', (W, 6000)))
        y2 = y + 62
        for seg in t.split('\n'): y2 = para(dd, tx, y2, seg, fs, W - tx - 50, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((tx, top + 18), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, tx, yy, seg, fs, W - tx - 50, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


def flow():
    """决策流程：矢状面 → 冠状面 → CFRT 阳性 → 上颈椎旋转手法 → CFRT 复测 → 旋转方向偏好"""
    W = 1200; im = Image.new('RGB', (W, 2000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '三例患者共同的评估思路（编者整理）', font=font(36), fill='white')
    rows = [
        ('① 排除禁忌、做基线', '神经系统查体（腱反射、霍夫曼征、C3～T1 肌节和皮节、分离 / 挤压 / 斯珀林试验）均正常；'
                          '记录疼痛、颈部活动度、颈椎屈曲旋转试验和上肢神经张力试验 1', PK, RED),
        ('② 矢状面重复运动', '后缩、后缩加伸展、屈曲，治疗师加压或松动\n→ 有改善但很快平台，或完全没变化', OR, ORG),
        ('③ 冠状面重复运动', '左 / 右侧屈，治疗师加压或松动\n→ 仍没有新的改善', OR, ORG),
        ('④ 转向水平面：上颈椎旋转', '颈椎屈曲旋转试验受限的一侧：仰卧上颈椎旋转松动（必要时推扳）+ 拮抗肌肌肉能量技术\n'
                               '→ 颈椎屈曲旋转试验和旋转活动度当场改善', LT, TEAL),
        ('⑤ 确认旋转方向偏好', '家庭训练改成“颈椎屈曲位下的上颈椎旋转 + 自我加压”，每次 10～20 下，每天 4～6 次；'
                           '症状稳定后再加深层颈屈肌耐力和肩胛胸壁力量训练', GR, GRN),
    ]
    y = 104
    for i, (h, t, c, a) in enumerate(rows):
        dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); y2 = y + 62
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 27, W - 100, gap=12)
        dr.rounded_rectangle([20, y, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, y, 30, y2 + 10], fill=a)
        dr.text((50, y + 18), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 27, W - 100, gap=12)
        y = y2 + 10
        if i < len(rows) - 1:
            cx = W // 2; dr.polygon([(cx - 22, y + 10), (cx + 22, y + 10), (cx, y + 36)], fill=GREY); y += 46
    y = para(dr, 30, y + 16, '每一步都以“基线是否当场改善”决定下一步：有改善就停在这个方向，没改善才换下一个平面。'
             '病例 2 的顺序略有不同：先做冠状面（延续他之前的侧屈家庭训练），再在矢状面屈曲方向得到改善，第 3 次就诊平台后才转到旋转。', 24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 20))


def chart():
    """按原文图 6 / 7 / 10 的数值用中文重绘（三张原图完全相同）"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    font_manager.fontManager.addfont(F)
    plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
    plt.rcParams['axes.unicode_minus'] = False
    blue, orange = '#4472C4', '#ED7D31'
    labels = ['初次评估', '第 2 次就诊', '第 3 次就诊', '第 4 次就诊', '出院']
    cols = [blue, orange, orange, orange, blue]
    # (病例, 指标, 五个时间点；None 表示该时间点没有数据)
    groups = [
        ('病例 1', '疼痛评分', [30, 30, 10, 10, 10]), ('病例 1', '颈部功能障碍指数', [34, None, None, None, 6]),
        ('病例 2', '疼痛评分', [40, 80, 50, 20, 20]), ('病例 2', '上肢功能障碍问卷\n（简版）', [52.3, None, None, None, 19]),
        ('病例 3', '疼痛评分', [70, 70, 30, 10, 10]), ('病例 3', '颈部功能障碍指数', [20, None, None, None, 4]),
    ]
    fig, ax = plt.subplots(figsize=(12, 7.2), dpi=110)
    bw = 0.15
    for g, (_, _, vals) in enumerate(groups):
        for k, v in enumerate(vals):
            if v is None: continue
            x = g + (k - 2) * bw
            ax.bar(x, v, bw * 0.85, color=cols[k], label=labels[k] if g == 0 else None)
            ax.text(x, v + 1.2, f'{v:g}', ha='center', va='bottom', fontsize=11, color='#333')
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([m for _, m, _ in groups], fontsize=12)
    for i, c in enumerate(['病例 1', '病例 2', '病例 3']):
        ax.text(2 * i + 0.5, -13.5, c, ha='center', va='top', fontsize=13, fontweight='bold', transform=ax.transData)
    ax.set_ylim(0, 90); ax.set_yticks(range(0, 91, 10))
    ax.set_ylabel('分值（换算成百分制）', fontsize=13)
    ax.yaxis.grid(True, color='#dddddd'); ax.set_axisbelow(True)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    h, l = ax.get_legend_handles_labels(); order = [l.index(x) for x in labels]
    ax.legend([h[i] for i in order], labels, ncol=5, loc='upper center', bbox_to_anchor=(0.5, -0.24), frameon=False, fontsize=12)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.96, bottom=0.27)
    path = f'{OUT}/_chart.png'; fig.savefig(path); plt.close(fig)
    im = Image.open(path).convert('RGB')
    import os; os.remove(path)
    return im


# 1 首图
W, H = 1400, 760; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '病例系列 · 《Cureus》2023 · 开放获取（CC BY 4.0）', font=font(30), fill=TEAL)
dr.text((70, 125), '用颈椎屈曲旋转试验确认', font=font(50), fill=INK)
dr.text((70, 195), '颈痛患者的旋转方向偏好', font=font(50), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Post MD, Schenk RJ, Fargnoli R.', font=font(26), fill=GREY)
dr.text((70, 375), 'Cureus. 2023;15(10):e47389. doi:10.7759/cureus.47389', font=font(26), fill=GREY)
dr.text((70, 420), '美国费城好牧人宾大合作康复中心（物理治疗）；', font=font(26), fill=GREY)
dr.text((70, 460), '美国塔夫茨大学医学院（波士顿，物理治疗）', font=font(26), fill=GREY)
dr.text((70, 640), '编者中文解读 · 结局图按原文数据中文重绘，照片原样引用', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(flow(), 2)

# 原文照片：只缩放，不改图内内容
save(capbox(raw(1), '原文图 1  颈椎屈曲旋转试验：患者仰卧，检查者把颈椎被动屈到末端，'
                    '再把头向一侧被动旋转到末端，比较左右两侧的活动度和症状'), 3)
save(capbox(raw(2), '原文图 2  用量角器测量颈椎屈曲旋转试验的旋转角度（病例 3 使用）'), 4)
save(capbox(raw(3), '原文图 3  仰卧位上颈椎右旋，治疗师松动。推扳手法和肌肉能量技术也用同样的体位'), 5)
save(capbox(raw(4), '原文图 4  颈椎屈曲位下的上颈椎右旋 + 自我加压（家庭训练）'), 6)
save(capbox(raw(5), '原文图 5  仰卧位，从屈曲预摆位做上颈椎右旋松动。推扳手法和肌肉能量技术也用同样的体位'), 7)
save(capbox(raw(8), '原文图 8  仰卧位上颈椎左旋，治疗师松动（病例 3）。推扳手法和肌肉能量技术也用同样的体位'), 8)
save(capbox(raw(9), '原文图 9  仰卧位上颈椎左旋松动（病例 3 第 2 次就诊改用的屈曲预摆位）。'
                    '推扳手法和肌肉能量技术也用同样的体位'), 9)

save(capbox(chart(), '原文图 6 / 7 / 10（三张原图相同，编者按原图数值中文重绘）  三例患者从初次评估到出院的疼痛和功能障碍变化。'
                     '疼痛评分原为 0～10 分，图中乘以 10 显示；功能障碍为百分比。两者都是分越低越好', W=1200), 10)

save(card(1200, '三例速览（编者按原文表 1～3 整理）', [
    ('病例 1  25 岁男性', '左侧颈、肩胛、肩、上臂间歇痛 1 年；疼痛最重 3/10；颈部功能障碍指数 34%\n'
                       '矢状面后缩 + 伸展有改善但平台 → 第 2 次就诊做上颈椎右旋松动，右旋到 80°，屈曲旋转试验更对称\n'
                       '5 次就诊、约 6 周：疼痛 1/10，功能障碍指数 6%，深层颈屈肌耐力 3 秒 → 38 秒', LT, TEAL),
    ('病例 2  38 岁男性', '反复搬重物后左侧颈、肩、上臂痛 5 周；疼痛最重 4/10；简版上肢功能障碍问卷 52.3%\n'
                       '侧屈、伸展无效，屈曲方向能消除上臂痛 → 第 3 次就诊屈曲平台，屈曲旋转试验左侧仍阳性，改做上颈椎左旋\n'
                       '5 次就诊、约 4 周：疼痛 2/10，问卷 19%', OR, ORG),
    ('病例 3  76 岁女性', '左侧颈痛 1 年，左旋加重；疼痛 7/10；颈部功能障碍指数 20%；合并症多\n'
                       '矢状面、冠状面都没变化 → 首诊就做上颈椎左旋松动，屈曲预摆位更好，后加推扳\n'
                       '6 次就诊、约 8 周：疼痛 1/10，功能障碍指数 4%，屈曲旋转试验左侧 27°（第 2 次就诊）→ 左右都是 37°', GR, GRN),
]), 11)

save(card(1200, '落到临床（编者整理）', [
    ('先把屈曲旋转试验当成基线', '颈痛患者做重复运动评估前后都测一次：它反映上颈椎（主要是寰枢关节）的旋转受限，'
                          '复测快、能量化（量角器或目测）', LT, TEAL),
    ('矢状面、冠状面没找到方向时', '别急着下“没有方向偏好”的结论：屈曲旋转试验阳性的，试一下受限侧的上颈椎旋转手法，'
                           '当场复测有改善，再把旋转写进家庭训练', OR, ORG),
    ('家庭训练怎么给', '坐位，颈椎先屈曲（或向对侧侧屈）锁住下颈椎，再向受限侧旋转到末端并用手加压，'
                    '每次 10～20 下，每天 4～6 次；症状外周化或加重就停', GR, GRN),
    ('别忘了后续的力量训练', '症状稳定后，三例都加了深层颈屈肌耐力和肩胛胸壁力量训练', PK, RED),
    ('证据级别要心里有数', '只有 3 例、没有对照组，同时用了手法和运动，不能区分谁起作用，也排除不了自然病程（编者观点）', PU, PUR),
]), 12)

# 封面：纯文字
W, H = 900, 383; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, H], fill=TEAL)
dr.text((50, 46), '病例系列 · Cureus 2023', font=font(26), fill=TEAL)
dr.text((50, 118), '颈痛找不到方向偏好？', font=font(52), fill=INK)
dr.text((50, 198), '试试屈曲旋转试验', font=font(46), fill=INK)
dr.text((50, 290), '重复运动 · 上颈椎旋转 · 松动与推扳 · 家庭训练', font=font(24), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
