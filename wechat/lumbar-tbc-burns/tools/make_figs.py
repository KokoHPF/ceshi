#!/usr/bin/env python3
"""Burns 等 2011《腰椎疾病基于治疗分类的检查与干预方法》（Sports Health）推文配图。
原文 © 2011 The Author(s)，SAGE 出版，PMC 免费阅读，但没有采用知识共享（CC）许可，不允许改编。
原文图 1～12 都是照片或人体示意图，图内没有英文文字和缩写，原样引用（只等比缩放），
中文图注放在图外上方的色条里；三步流程卡、Ⅰ期分组速查卡、首图、临床要点卡和封面为编者绘制。
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


def steps():
    """三步流程：筛查 → 分期 → 分组干预"""
    W = 1200; im = Image.new('RGB', (W, 1000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '基于治疗分类（TBC）的三步走（编者整理）', font=font(36), fill='white')
    rows = [
        ('第一步  能不能保守治疗？', '筛查红旗征：骨折、马尾综合征、肿瘤、强直性脊柱炎、感染 → 有则转诊进一步检查\n'
                              '同时看黄旗：恐惧回避信念（FABQ）、抑郁、焦虑、疼痛灾难化', PK, RED),
        ('第二步  分期（看功能，不看病程）', 'Ⅰ期：坐、站、走都困难，改良 ODI 常 ≥ 20%\n'
                                 'Ⅱ期：日常基本活动可以，较重活动和慢跑等运动困难，ODI ≤ 20%\n'
                                 'Ⅲ期：日常无困难，但还不能完全回到赛场', OR, ORG),
        ('第三步  按分期配干预', 'Ⅰ期：手法 / 特定方向运动 / 稳定训练 / 牵引，四组按体征归类\n'
                           'Ⅱ期：止痛、柔韧、力量、姿势、身体力学、有氧\n'
                           'Ⅲ期：专项训练、脊柱稳定、防复发训练、功能训练', GR, GRN),
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
    para(dr, 30, y + 16, '分期是动态的：可以从任何一期进入，进展快慢因人而异；Ⅰ期改良 ODI 下降 33% 或降到 ≤ 20%，就进入Ⅱ期或Ⅲ期。',
         24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 100))


# 1 首图
W, H = 1400, 720; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '临床综述 · 《Sports Health》2011', font=font(30), fill=TEAL)
dr.text((70, 125), '腰椎疾病基于治疗分类的', font=font(50), fill=INK)
dr.text((70, 195), '检查与干预方法', font=font(50), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Burns SA, Foresman E, Kraycsir SJ, Egan W, Glynn P, Mintken PE, Cleland JA.', font=font(26), fill=GREY)
dr.text((70, 375), 'Sports Health. 2011;3(4):362-372. doi:10.1177/1941738111410378', font=font(26), fill=GREY)
dr.text((70, 420), '美国天普大学物理治疗系；科罗拉多大学；牛顿-韦尔斯利医院；', font=font(26), fill=GREY)
dr.text((70, 460), '富兰克林·皮尔斯大学', font=font(26), fill=GREY)
dr.text((70, 600), '编者中文解读 · 原文图 1～12 原样引用，图注为编者翻译', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(steps(), 2)

# 原文图：只缩放，不改图内内容
save(capbox(raw(1), '原文图 1  人体示意图：症状在膝以上（红线为症状范围）。手法组的条件之一是“膝以下没有症状”', img_w=420), 3)
save(capbox(raw(2), '原文图 2  腰椎节段后前向（PA）活动度评估。箭头为检查者施力方向。手法组的条件之一是“腰椎活动度降低”'), 4)
save(capbox(raw(3), '原文图 3  俯卧位用气泡倾角计测髋内旋活动度。箭头为评估左髋内旋时小腿摆动的方向。'
                    '手法组的条件之一是至少一侧髋内旋 ≥ 35°'), 5)
save(capbox(raw(4), '原文图 4  人体示意图：症状超过臀部、向远端延伸。伸展方向运动组的条件之一', img_w=420), 6)
save(capbox(raw(5), '原文图 5  俯卧位腰椎伸展。箭头示腿部症状向中心化（向腰部回缩）'), 7)
save(capbox(raw(6), '原文图 6  可见的冠状面偏移（侧移），红线示对侧下肢有症状', img_w=600), 8)
save(capbox(raw(7), '原文图 7  可见的冠状面偏移，箭头示症状向腰部中心化', img_w=600), 9)
save(capbox(raw(8), '原文图 8  同侧直腿抬高。稳定训练组的条件之一是直腿抬高 ≥ 91°'), 10)
save(capbox(raw(9), '原文图 9  俯卧不稳定试验。左：起始位，双脚着地；右：结束位，双脚离地。'
                    '白色箭头为检查者施加的后前向压力。双脚离地后疼痛减轻为阳性', W=1200), 11)
save(capbox(raw(10), '原文图 10  人体示意图：存在腿部症状。牵引组的条件之一', img_w=380), 12)
save(capbox(raw(11), '原文图 11  俯卧位腰椎伸展，箭头示症状外周化（向远端扩散）。牵引组的条件之一'), 13)
save(capbox(raw(12), '原文图 12  交叉直腿抬高：检查者抬起对侧（无症状侧）下肢，看症状是否向患侧下肢远端扩散'), 14)

save(card(1200, 'Ⅰ期四个分组速查（编者按原文表 4 和附录整理）', [
    ('手法（推扳）', '膝以下无症状；病程 ≤ 16 天；FABQ 工作分量表 ≤ 19；腰椎活动度降低；至少一侧髋内旋 ≥ 35°\n'
                  '满足 ≥ 4 项：2 次治疗内 ODI 降一半的概率约 95%', LT, TEAL),
    ('特定方向运动', '伸展：症状超过臀部、偏好伸展、屈曲时外周化、伸展时中心化\n'
                  '屈曲：年龄 ≥ 50 岁、偏好屈曲、影像有椎管狭窄\n'
                  '侧移：可见冠状面偏移、偏好侧向平移动作', OR, ORG),
    ('稳定训练', '年龄 ≤ 40 岁（正文写作 < 40 岁）；直腿抬高 ≥ 91°；有异常动作；俯卧不稳定试验阳性', GR, GRN),
    ('牵引', '有腿部症状；有神经根受压体征（肌节、皮节、腱反射异常）；伸展时外周化；交叉直腿抬高阳性', PU, PUR),
]), 15)

save(card(1200, '落到临床（编者整理）', [
    ('先筛查，再分类', '红旗征（外伤、鞍区麻木、大小便功能改变、50 岁以上、肿瘤史、夜间痛、发热等）先排除；'
                   '恐惧回避明显的，处理方式要跟着调整', PK, RED),
    ('分期看功能，不看几周', '用改良 ODI 和 NPRS 定期复评：ODI 变化 6 个百分点、NPRS 变化 2 分有临床意义，'
                       'ODI 降一半可视为治疗成功', OR, ORG),
    ('Ⅰ期按体征配干预', '急性、膝以下没症状 → 先考虑推扳手法 + 主动活动；有方向偏好 → 顺着能让症状中心化的方向练；'
                     '年轻、活动度大、有异常动作 → 稳定训练；有神经根体征、伸展外周化 → 可考虑牵引', LT, TEAL),
    ('Ⅱ、Ⅲ期练到能回场', '针对柔韧、力量、耐力、神经肌肉控制，兼顾髋和胸椎；Ⅲ期加专项训练和防复发计划，'
                      '同时教育运动员循序渐进、避免过度训练', GR, GRN),
    ('别把规则当金标准', '这是 2011 年的叙述性综述；各组预测规则大多来自中小样本，后续验证结果并不一致（编者观点）', PU, PUR),
]), 16)

# 封面：纯文字
W, H = 900, 383; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, H], fill=TEAL)
dr.text((50, 46), '临床综述 · Sports Health 2011', font=font(26), fill=TEAL)
dr.text((50, 118), '运动员腰痛', font=font(58), fill=INK)
dr.text((50, 198), '按治疗分类三步走', font=font(46), fill=INK)
dr.text((50, 290), '红旗筛查 · 功能分期 · 手法 · 方向运动 · 稳定 · 牵引', font=font(24), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
