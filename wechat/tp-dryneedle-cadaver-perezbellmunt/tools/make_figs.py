#!/usr/bin/env python3
"""Pérez-Bellmunt 等 2022《胫骨后肌后内侧干针入路准确且安全：尸体研究》（BMC Musculoskelet Disord）推文配图。
原文是 CC BY 4.0（允许改编，需署名并注明改动）。
原文图 1、3、4、5 图内英文和缩写（T 胫骨、F 腓骨、Needle、方位词、入路标签）已由编者原位译成中文
（tools/translate_figs.py，位图路线：擦除原字后在原位写中文），图内肌肉编号 1～10 和测量代号 A～E 保留，
对照写在推文图下说明里；原文图 2 图内只有分图字母，原样引用；原文表 2 按数据重画成柱状图；
首图、临床要点卡和封面为编者绘制。
用法：python3 tools/make_figs.py src images <中文字体>"""
import re
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50); ORG = (215, 120, 20)
GRN = (0, 120, 60); PUR = (110, 70, 190)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)



def raw(name):
    return Image.open(f'{SRC}/{name}').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    # 英文单词、数字整体换行；标点不放行首
    for tok in re.findall(r"[A-Za-z0-9.%\-+/～±]+|.", t):
        if line and dr.textlength(line + tok, font=font(fs)) > w and tok not in '，。；：、）”°':
            dr.text((x, y), line.rstrip(), font=font(fs), fill=fill); y += fs + gap; line = tok.lstrip()
        else: line += tok
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    """原图等比缩放后放在下方，中文图注放在图外上方的色条里（\n 分段）"""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    def lay(dr):
        y = 14
        for seg in cap.split('\n'): y = para(dr, 14, y, seg, 27, W - 30, fill=TEAL, gap=11)
        return y + 4
    hh = lay(ImageDraw.Draw(Image.new('RGB', (W, 3000))))
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); lay(dr)
    t.paste(im, (0, hh + 8)); return t


def card(W, title, blocks):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 6000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100; tx = 50
    for h, t, c, a in blocks:
        top = y; dd = ImageDraw.Draw(Image.new('RGB', (W, 6000)))
        y2 = y + 62
        for seg in t.split('\n'): y2 = para(dd, tx, y2, seg, 28, W - tx - 50, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((tx, top + 18), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, tx, yy, seg, 28, W - tx - 50, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


def distances():
    """原文表 2：两种入路针到神经、血管束的距离（均值 ± 标准差，单位 cm）"""
    W = 1200; H = 900; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '针离神经、血管有多远（编者按原文表 2 重画）', font=font(36), fill='white')
    cols = [(ORG, '前入路（小腿上 1/3）'), (TEAL, '后内侧入路（小腿中点）')]
    x0 = 40
    for c, t in cols:
        dr.rectangle([x0, 108, x0 + 28, 134], fill=c); dr.text((x0 + 38, 104), t, font=font(26), fill=INK); x0 += 380
    # (名称, 前入路均值, SD, 后内侧均值, SD, 显著性)
    groups = [('针尖→神经', 0.7, 0.3, 1.35, 0.7, 'P<0.001'), ('针尖→血管束', 0.9, 0.35, 1.45, 0.25, 'P<0.001'),
              ('针道→神经', 0.75, 0.3, 1.0, 0.3, '原文未报告'), ('针道→血管束', 0.65, 0.3, 0.95, 0.3, 'P=0.045')]
    top, bot, vmax = 210, 640, 2.2
    dr.line([90, bot, W - 30, bot], fill=GREY, width=2)
    for v in (0, 0.5, 1.0, 1.5, 2.0):
        y = bot - (bot - top) * v / vmax
        dr.line([90, y, W - 30, y], fill=(232, 232, 232), width=1)
        dr.text((80, y), f'{v:g}', font=font(22), fill=GREY, anchor='rm')
    dr.text((40, top - 40), 'cm', font=font(22), fill=GREY)
    gw = (W - 120) / 4
    for k, (name, a, sa, p, sp, sig) in enumerate(groups):
        L = 90 + k * gw; bw = 80; start = L + (gw - 2 * bw - 16) / 2
        for i, (v, sd) in enumerate(((a, sa), (p, sp))):
            x = start + i * (bw + 16); h = (bot - top) * v / vmax
            dr.rectangle([x, bot - h, x + bw, bot], fill=cols[i][0])
            yt = bot - (bot - top) * (v + sd) / vmax; yb = bot - (bot - top) * max(v - sd, 0) / vmax
            cx = x + bw / 2; dr.line([cx, yt, cx, yb], fill=INK, width=2); dr.line([cx - 10, yt, cx + 10, yt], fill=INK, width=2)
            dr.text((cx, yt - 6), f'{v:g}', font=font(22), fill=INK, anchor='md')
        dr.text((L + gw / 2, bot + 16), name, font=font(26), fill=INK, anchor='ma')
        dr.text((L + gw / 2, bot + 54), sig, font=font(22), fill=RED if sig.startswith('P') else GREY, anchor='ma')
    para(dr, 30, bot + 110, '柱高为均值，细线为 ±1 个标准差。前入路量的是腓深神经和胫前血管束，后内侧入路量的是胫神经和胫后血管束；'
         '每种入路 11 条腿。P 值为原文协方差分析（校正年龄、性别）结果。后内侧“针尖→神经”的标准差 0.7 与原文给的置信区间对不上，见正文。',
         22, W - 60, fill=GREY)
    return im


# 1 首图
W, H = 1400, 720; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '尸体研究 · 《BMC Musculoskeletal Disorders》2022', font=font(30), fill=TEAL)
dr.text((70, 125), '胫骨后肌干针：后内侧入路', font=font(50), fill=INK)
dr.text((70, 195), '准确且安全的操作（尸体研究）', font=font(46), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Pérez-Bellmunt A, López-de-Celis C, Rodríguez-Sanz J, et al.', font=font(26), fill=GREY)
dr.text((70, 375), 'BMC Musculoskelet Disord. 2022;23:570. doi:10.1186/s12891-022-05530-3', font=font(26), fill=GREY)
dr.text((70, 420), '西班牙加泰罗尼亚国际大学医学与健康科学学院；ACTIUM 功能解剖小组；', font=font(26), fill=GREY)
dr.text((70, 460), '美国贝勒大学物理治疗博士项目；西班牙胡安·卡洛斯国王大学', font=font(26), fill=GREY)
dr.text((70, 600), '编者中文解读 · 原文 CC BY 4.0，图 1、3、4、5 图内文字由编者译为中文', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(raw('fig1_zh.jpg'), '原文图 1（图内文字编者译）  胫骨后肌前入路与后内侧入路的进针点。'
                                '前入路在小腿上 1/3，后内侧入路在小腿中点（小腿长度从胫骨粗隆量到内外踝连线）。'
                                '原图把后内侧入路标作“Posterior approach”', W=760), 2)
save(capbox(raw('fig2.jpg'), '原文图 2  两种入路的操作。A：前入路，在小腿上 1/3、贴近胫骨前外侧进针，向后穿过骨间膜到达胫骨后肌；'
                             'B：后内侧入路，在小腿中 1/3、贴近胫骨后缘进针，由内向外穿过趾长屈肌到达胫骨后肌', W=760), 3)
save(capbox(raw('fig3_zh.jpg'), '原文图 3（图内文字编者译）  前入路示意：左为尸体断面，中、右为解剖示意。'
                                '针向后穿过骨间膜。编号与代号对照见图下说明'), 4)
save(capbox(raw('fig4_zh.jpg'), '原文图 4（图内文字编者译）  后内侧入路示意：左为尸体断面，中、右为解剖示意。'
                                '针由内向外穿过趾长屈肌。编号与代号对照见图下说明'), 5)
save(capbox(raw('fig5_zh.jpg'), '原文图 5（图内文字编者译）  解剖证实两种入路的针尖（蓝色乳胶点）都落在胫骨后肌（6）内。'
                                '左：前入路；右：后内侧入路。编号对照见图下说明'), 6)
save(distances(), 7)

save(card(1200, '落到临床（编者整理）', [
    ('后内侧入路怎么扎', '小腿中点（胫骨粗隆到内外踝连线的中点），贴着胫骨后缘进针，由内向外，先过趾长屈肌再到胫骨后肌；'
                       '本研究平均进针约 3.5 cm（35.1 ± 4.5 mm）', LT, TEAL),
    ('前入路怎么扎', '小腿上 1/3，贴着胫骨前外侧进针，向后穿过骨间膜；平均进针约 3.2 cm（31.9 ± 6.2 mm）。'
                   '针尖离腓深神经平均只有 7 mm 左右', OR, ORG),
    ('两条都能扎中，后内侧余量更大', '11 条腿两种入路都 100% 扎中胫骨后肌，没有刺破神经血管束；'
                               '后内侧入路针尖离神经、血管束平均多出约 0.5～0.6 cm', GR, GRN),
    ('贴骨走、控角度', '两种入路都紧贴胫骨进针，作者强调要严格控制针的角度和方向；本研究由 10 年以上经验的治疗师操作，'
                    '新手的准确性和安全性没有数据', PK, RED),
    ('别外推太多', '冷冻尸体、只测了两个固定点；扎触发点时位置可能偏离；脑卒中痉挛的肌肉结构也可能不同。'
                 '扎得准不等于有疗效，干针治疗痉挛还需要临床试验', PU, PUR),
]), 8)

# 封面：纯文字
W, H = 900, 383; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, H], fill=TEAL)
dr.text((50, 46), '尸体研究 · BMC MSK 2022', font=font(26), fill=TEAL)
dr.text((50, 118), '胫骨后肌干针', font=font(58), fill=INK)
dr.text((50, 198), '前入路还是后内侧入路？', font=font(46), fill=INK)
dr.text((50, 290), '干针 · 胫骨后肌 · 神经血管距离 · 安全', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
