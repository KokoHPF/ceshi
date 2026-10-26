#!/usr/bin/env python3
"""Araújo 等 2024《儿童半月板：正常表现、解剖变异、损伤、撕裂及术后影像》（Insights into Imaging）推文配图。
原文 © The Author(s) 2024，CC BY 4.0，允许改编：
- 原文图 1 是带英文标注和缩写的解剖示意 + MRI，标注已用 tools/fig1_zh.py 原位换成中文（src/fig1_zh.png）；
- 原文图 2～12 是 MRI / 关节镜图像，图内只有面板字母、测量字母和箭头，没有英文词句，原样引用（只等比缩放），
  中文图注放在图外上方色条里；
- 首图、血供分区示意、撕裂类型分布图、报告清单卡和封面为编者根据原文绘制。
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
    for tok in re.findall(r"[A-Za-z0-9.%\-+/～±≥≤°×]+|.", t):
        if line and dr.textlength(line + tok, font=font(fs)) > w and tok not in '，。；：、）”°':
            dr.text((x, y), line.rstrip(), font=font(fs), fill=fill); y += fs + gap; line = tok.lstrip()
        else: line += tok
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1000):
    """原图等比缩放（不改内容）放在下方，中文图注放在图外上方的色条里"""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    def lay(dr):
        y = 14
        for seg in cap.split('\n'): y = para(dr, 16, y, seg, 27, W - 34, fill=TEAL, gap=10)
        return y + 4
    hh = lay(ImageDraw.Draw(Image.new('RGB', (W, 3000))))
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); lay(dr)
    t.paste(im, (0, hh + 8)); return t


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


def head():
    W = 1080; im = Image.new('RGB', (W, 1400), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 14], fill=TEAL)
    dr.text((50, 50), 'Insights into Imaging · 2024 · 教育性综述', font=font(30), fill=TEAL)
    y = para(dr, 50, 110, 'Pediatric menisci: normal aspects, anatomical variants, lesions, tears, and postsurgical findings',
             34, W - 100, fill=GREY, gap=10)
    y = para(dr, 50, y + 24, '儿童半月板：正常表现、解剖变异、损伤、撕裂及术后影像', 48, W - 100, fill=INK, gap=16)
    dr.line([50, y + 16, W - 50, y + 16], fill=(210, 210, 210), width=2)
    rows = [('作者', 'Araújo FF, Guimarães JB, da Cruz IAN, Morimoto LdR, Ormond Filho AG, Nico MAC'),
            ('单位', '巴西圣保罗 Fleury 医学与健康集团，肌骨放射科'),
            ('出处', 'Insights Imaging. 2024;15:295. doi:10.1186/s13244-024-01867-6'),
            ('许可', '开放获取，CC BY 4.0（允许改编、商用，须注明出处和改动）')]
    y += 44
    for k, v in rows:
        dr.text((50, y), k, font=font(28), fill=TEAL)
        y = para(dr, 140, y, v, 28, W - 190, gap=10) + 10
    dr.rounded_rectangle([40, y + 10, W - 40, y + 150], 14, fill=OR)
    para(dr, 70, y + 32, '一句话：儿童半月板不是“缩小版的成人半月板”，血供、信号、变异和撕裂类型都不同，'
         '读片和处理都要按儿童的规律来。', 30, W - 140, fill=(150, 70, 0), gap=12)
    return im.crop((0, 0, W, y + 180))


def vasc():
    """血供随年龄变化 + 红区 / 红白区 / 白区（编者根据原文文字绘制）"""
    W, H = 1080, 820; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '半月板血供：随年龄由全层退到外周（编者示意）', font=font(36), fill='white')
    stages = [('出生时', 1.0, '整个半月板\n都有血管'), ('约 9 个月', 0.67, '内 1/3\n血管已退化'),
              ('10～12 岁以后', 0.25, '只剩外周\n10%～30%（同成人）')]
    for i, (t, frac, note) in enumerate(stages):
        cx = 190 + i * 350; cy = 360; R, r = 140, 55
        dr.pieslice([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=(235, 235, 235), outline=(160, 160, 160), width=2)
        rv = R - (R - r) * frac
        dr.pieslice([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=(222, 80, 80))
        dr.pieslice([cx - rv, cy - rv, cx + rv, cy + rv], 180, 360, fill=(240, 240, 240))
        dr.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill='white')
        dr.rectangle([cx - R - 2, cy, cx + R + 2, cy + 4], fill='white')
        dr.text((cx - dr.textlength(t, font=font(32)) / 2, 150), t, font=font(32), fill=INK)
        yy = cy + 24
        for ln in note.split('\n'):
            dr.text((cx - dr.textlength(ln, font=font(26)) / 2, yy), ln, font=font(26), fill=GREY); yy += 36
        if i < 2:
            dr.polygon([(cx + 160, 300), (cx + 160, 340), (cx + 190, 320)], fill=GREY)
    y = 530
    for c, h, t in [((222, 80, 80), '红区（外 10%～30%）', '血供丰富，愈合潜力好；外 1/3 的撕裂可保守或缝合'),
                    ((240, 170, 170), '红白区（中间过渡带）', '血供中等'),
                    ((235, 235, 235), '白区（内 70%～90%）', '基本无血管，只靠关节液弥散营养，撕裂愈合差、易扩展')]:
        dr.rectangle([50, y + 4, 86, y + 36], fill=c, outline=(160, 160, 160))
        dr.text((104, y), h, font=font(28), fill=INK)
        para(dr, 104 + dr.textlength(h, font=font(28)) + 20, y + 2, t, 25, W - 160 - dr.textlength(h, font=font(28)), fill=GREY)
        y += 58
    para(dr, 50, y + 16, '读片提示：儿童半月板内的线状高信号可以只是正常血管，只要没有接触关节面，就不应报撕裂。',
         26, W - 100, fill=RED)
    return im


def tears():
    """Shieh 等（原文引 [3]）293 例儿童青少年关节镜下撕裂类型分布，编者按原文百分比绘制"""
    data = [('复杂撕裂', 28), ('纵向（垂直）撕裂', 16), ('盘状半月板撕裂', 14), ('桶柄样撕裂', 14), ('放射状撕裂', 10),
            ('水平撕裂', 8), ('斜形撕裂', 5), ('磨损', 3), ('根部撕脱', 2)]
    W = 1080; H = 140 + len(data) * 64 + 90; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '儿童青少年半月板撕裂类型（293 例关节镜）', font=font(36), fill='white')
    x0 = 330; sc = (W - x0 - 120) / 30; y = 112
    for k, v in data:
        dr.text((x0 - 20 - dr.textlength(k, font=font(28)), y + 6), k, font=font(28), fill=INK)
        dr.rectangle([x0, y + 4, x0 + v * sc, y + 44], fill=TEAL if v >= 14 else (120, 175, 185))
        dr.text((x0 + v * sc + 12, y + 6), f'{v}%', font=font(28), fill=INK)
        y += 64
    para(dr, 30, y + 14, '数据：Shieh 等 2013（原文文献 [3]），编者按原文给出的百分比重绘。复杂撕裂多见于男性和体重指数高者；'
         '最常累及后角。', 23, W - 60, fill=GREY)
    return im


CAPS = {
    1: '原文图 1　膝关节半月板解剖。A 磁共振轴位上的示意：半月板根部及其与周围关节囊韧带结构的关系；'
       'B 后外侧视角三维示意，重点显示韧带结构；C、D 内侧半月板冠状位（C）、矢状位（D）T2 压脂像，'
       '显示板股韧带、板胫韧带和半月板—关节囊连接；E、F 外侧半月板矢状位，显示腘肌—半月板束和腘肌腱。'
       '图中英文标注和缩写已译成中文。',
    2: '原文图 2　不完全型盘状外侧半月板患儿的 MRI 测量。A 冠状位：半月板最小宽度 a、胫骨最大宽度 b，'
       '半月板 / 胫骨宽度比 = a/b × 100%；B 矢状位：前角宽 c、后角宽 d、半月板最大直径 e，半月板覆盖率 = (c + d)/e × 100%',
    3: '原文图 3　Watanabe 分型。Ⅰ型（A、B）完全型，后方附着正常（箭头）；Ⅱ型（C、D）不完全型，后方附着正常（箭头）；'
       'Ⅲ型（E、F）Wrisberg 型，缺少常规后方附着而不稳（虚线箭头）；拟议的Ⅳ型（G、H）环形半月板，'
       '外侧间室中央有三角形半月板组织（三角箭头），后方胫骨附着正常（箭头）',
    4: '原文图 4　Ahn MRI 分型。A、B 无移位型（原图注为内侧盘状半月板，广泛水平撕裂延伸至下关节面，伴小的半月板周围囊肿）；'
       'C、D 前中心移位型，半月板向前脱位（箭头），后段像“消失”了一样；E、F 后中心移位型，外侧半月板向后移位（箭头）；'
       'G、H 中心移位型，半月板向髁间窝方向内移',
    5: '原文图 5　13 岁男孩，跑步和伸膝时痛。右膝冠状位（A）、矢状位（B）压脂 T2：无移位型完全型外侧盘状半月板伴退变，'
       '半月板旁软组织水肿（箭头），后上腘肌—半月板束缺失（虚线箭头）。这些都是周缘不稳的征象',
    6: '原文图 6　20 岁女性，盘状半月板复查。A 右膝矢状位压脂 T2：半月板前缘向前膨出，5 年前的检查（B）没有这一表现；'
       '后上腘肌—半月板束缺失（虚线箭头，Wrisberg 型）。几个征象合起来提示周缘不稳',
    7: '原文图 7　其他半月板变异。A 矢状位压脂 T2：典型的半月板褶皱（波纹状，箭头），可被误当成半月板截断或放射状撕裂；'
       'B、C 14 岁男孩，既往内侧半月板后根撕裂（未展示），出现创伤后半月板小骨：冠状位 T1（B）、矢状位质子密度像（C）'
       '显示内侧半月板后根内的小骨（箭头），也容易被误判为撕裂',
    8: '原文图 8　12 岁女孩，膝扭伤后疼痛、活动受限。A 轴位 T2 压脂：后角撕裂（虚线箭头）和半月板周围炎症征象（箭头）；'
       'B、C 矢状位 T2 压脂：前交叉韧带撕裂（三角箭头）和外侧半月板后角纵向撕裂（箭头）',
    9: '原文图 9　9 岁女孩，轮滑摔倒后膝痛。右膝冠状位（A）、轴位（B）压脂 T2：内侧半月板后根放射状撕裂（箭头）；'
       'C 数天后的关节镜证实为完全性放射状根部撕裂（虚线箭头）',
    10: '原文图 10　17 岁男性足球运动员，膝外伤，缝合术后 6 个月复查。A、B 术前矢状位、冠状位 T2 压脂：后角半月板—关节囊连接分离'
        '（三角箭头），部分半月板向前移位（虚线箭头），前角增厚（箭头）；C、D 术后 6 个月：后方半月板—关节囊修复（箭头），'
        '恢复良好，外观与 D 中所示对侧半月板相近',
    11: '原文图 11　11 岁男孩，膝外伤，缝合术后 2 个月复查。A、B 术前矢状位、轴位 T2 压脂：后角半月板—关节囊连接分离（三角箭头），'
        '向前移位（虚线箭头），前角增厚（箭头）；C、D 后角重新固定术后 2 个月：后方修复（箭头），'
        '体部和前、后角内的高信号线是缝合处（虚线箭头）',
    12: '原文图 12　7 岁女孩，外伤后膝痛，术后 3 个月复查。A、B 术前冠状位、矢状位 T2 压脂：盘状半月板因水平撕裂（虚线箭头）'
        '向后半脱位（三角箭头），前方半月板—关节囊连接分离（未展示），属后中心移位型；C、D 术后 3 个月：半月板体积缩小、'
        '轮廓不规则、游离缘变短 / 截断，实质内信号改变与手术操作有关（箭头）',
}


def report():
    return card(1080, '半月板撕裂：报告里要写什么（原文表 2）', [
        ('① 半月板形态', '正常，还是盘状', PU, PUR),
        ('② 撕裂类型', '水平、放射状、垂直、纵向、桶柄样、复杂', BL, BLU),
        ('③ 位置', '外周（外 1/3，血供好、易愈合），还是靠近游离缘', GR, GRN),
        ('④ 撕裂长度', '< 2.5 cm（预后好），还是 > 2.5 cm', OR, ORG),
        ('⑤ 过度活动 / 不稳的征象', '半月板移位；外侧半月板缺少常规后方附着；半月板—关节囊连接损伤', PK, RED),
        ('⑥ 合并损伤', '韧带（尤其前交叉韧带）；软骨和软骨下骨', LT, TEAL),
    ])


def cover():
    W, H = 900, 383; im = Image.new('RGB', (W, H), (0, 92, 110)); dr = ImageDraw.Draw(im)
    f1 = Image.open(f'{SRC}/fig1_zh.png').convert('RGB').crop((225, 640, 900, 1265))
    f1 = f1.resize((round(f1.width * H / f1.height), H), Image.LANCZOS)
    im.paste(f1, (W - f1.width, 0))
    dr.rectangle([0, 0, 420, H], fill=(0, 92, 110))
    dr.text((40, 60), '儿童半月板', font=font(72), fill='white')
    dr.text((40, 160), 'MRI 怎么看', font=font(56), fill=(255, 220, 140))
    dr.text((40, 250), '血供 · 盘状半月板 · 撕裂 · 术后', font=font(25), fill='white')
    return im


if __name__ == '__main__':
    save(head(), 1)
    save(capbox(Image.open(f'{SRC}/fig1_zh.png').convert('RGB'), CAPS[1]), 2)
    save(vasc(), 3)
    for n, k in [(4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 7), (10, 8), (11, 9)]:
        save(capbox(raw(k), CAPS[k]), n)
    save(tears(), 12)
    for n, k in [(13, 10), (14, 11), (15, 12)]:
        save(capbox(raw(k), CAPS[k]), n)
    save(report(), 16)
    cover().save(f'{OUT}/cover.jpg', quality=90)
    print('done')
