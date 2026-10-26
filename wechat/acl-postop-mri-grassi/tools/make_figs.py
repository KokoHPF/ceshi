#!/usr/bin/env python3
"""Grassi 等 2016《前交叉韧带重建术后磁共振成像：实用指南》（World J Orthop）推文配图。
原文以 CC BY-NC 4.0 发表，允许非商业改编：
- 原文图 1～17 是 MRI 图像，图内标注只有面板字母（A/B/C）、测量线字母（a～g）、数字、角度和星号，原样保留；
  图 7B 的方位标记 "A" 和图 15 测量软件残留的英文已用 tools/fig_zh.py 原位换成中文（src/fig7_zh.png、src/fig15_zh.png）；
  图注译成中文，放在图外上方色条里，原图只等比缩放；
- 首图、移植物信号演变时间线、Figueroa 评分卡（原文表 1）、读片清单卡和封面为编者根据原文绘制。
用法：python3 tools/make_figs.py src images <中文字体>"""
import re
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 96, 140); RED = (190, 40, 50); ORG = (215, 120, 20)
GRN = (0, 120, 60); PUR = (110, 70, 190); BLU = (40, 90, 170)
LT = (226, 238, 246); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)
BL = (230, 238, 250)


def raw(n):
    for name in (f'fig{n}_zh.png', f'fig{n}.png'):
        try:
            return Image.open(f'{SRC}/{name}').convert('RGB')
        except FileNotFoundError:
            pass
    raise FileNotFoundError(n)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=90)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    # 英文单词、数字整体换行；标点不放行首
    for tok in re.findall(r"[A-Za-z0-9.%\-+/～±≥≤°×<>]+|.", t):
        if line and dr.textlength(line + tok, font=font(fs)) > w and tok not in '，。；：、）”°':
            dr.text((x, y), line.rstrip(), font=font(fs), fill=fill); y += fs + gap; line = tok.lstrip()
        else: line += tok
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1000):
    """原图等比缩放（不改内容）放在下方，中文图注放在图外上方的色条里；竖长的图缩窄居中，免得在手机上太长"""
    iw = W if im.height < im.width * 1.1 else 640
    im = im.resize((iw, round(im.height * iw / im.width)), Image.LANCZOS)
    def lay(dr):
        y = 14
        for seg in cap.split('\n'): y = para(dr, 16, y, seg, 27, W - 34, fill=TEAL, gap=10)
        return y + 4
    hh = lay(ImageDraw.Draw(Image.new('RGB', (W, 3000))))
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); lay(dr)
    t.paste(im, ((W - iw) // 2, hh + 8)); return t


def card(W, title, blocks, fs=28, foot=None):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 8000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100; tx = 50
    for h, t, c, a in blocks:
        top = y; dd = ImageDraw.Draw(Image.new('RGB', (W, 8000)))
        y2 = y + 62
        for seg in t.split('\n'): y2 = para(dd, tx, y2, seg, fs, W - tx - 50, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((tx, top + 18), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, tx, yy, seg, fs, W - tx - 50, gap=14)
        y = y2 + 30
    if foot:
        y = para(dr, 30, y, foot, 23, W - 60, fill=GREY) + 10
    return im.crop((0, 0, W, y))


def head():
    W = 1080; im = Image.new('RGB', (W, 1400), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 14], fill=TEAL)
    dr.text((50, 50), 'World Journal of Orthopedics · 2016 · 综述', font=font(30), fill=TEAL)
    y = para(dr, 50, 110, 'Magnetic resonance imaging after anterior cruciate ligament reconstruction: A practical guide',
             34, W - 100, fill=GREY, gap=10)
    y = para(dr, 50, y + 24, '前交叉韧带重建术后磁共振成像：实用指南', 48, W - 100, fill=INK, gap=16)
    dr.line([50, y + 16, W - 50, y + 16], fill=(210, 210, 210), width=2)
    rows = [('作者', 'Grassi A, Bailey JR, Signorelli C, Carbone G, Tchonang Wakam A, Lucidi GA, Zaffagnini S'),
            ('单位', '意大利博洛尼亚 Rizzoli 骨科研究所；美国杜克大学医学中心'),
            ('出处', 'World J Orthop. 2016;7(10):638-649. doi:10.5312/wjo.v7.i10.638'),
            ('许可', '开放获取，CC BY-NC 4.0（允许非商业转载、改编，须注明出处）')]
    y += 44
    for k, v in rows:
        dr.text((50, y), k, font=font(28), fill=TEAL)
        y = para(dr, 140, y, v, 28, W - 190, gap=10) + 10
    dr.rounded_rectangle([40, y + 10, W - 40, y + 150], 14, fill=OR)
    para(dr, 70, y + 32, '一句话：术后 MRI 要看的不只是“韧带断没断”，还有移植物成熟度、骨道位置与扩大、固定物、'
         '取腱处和膝关节本身的骨性形态；但 MRI 只能辅助，不能单独下结论。', 30, W - 140, fill=(150, 70, 0), gap=12)
    return im.crop((0, 0, W, y + 180))


def timeline():
    """不同移植物术后 MRI 信号随时间的变化（编者根据原文文字绘制）"""
    W = 1080; im = Image.new('RGB', (W, 1600), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '移植物信号怎么变：术后时间线（编者示意）', font=font(36), fill='white')
    x0, x1 = 250, W - 50; months = [0, 6, 12, 18, 24]
    sx = lambda m: x0 + (x1 - x0) * m / 24
    y = 110
    for m in months:
        dr.text((sx(m) - dr.textlength(f'{m}', font=font(28)) / 2, y), f'{m}', font=font(28), fill=GREY)
    dr.text((50, y), '术后月数', font=font(28), fill=GREY)
    LO, MID, HI = (70, 70, 70), (150, 150, 150), (222, 80, 80)
    rows = [
        ('骨—髌腱—骨', [(0, 1, LO, '低信号'), (1, 17, HI, '滑膜包裹、血管长入，信号升高（可到 16～18 个月）'), (17, 24, LO, '接近原生')]),
        ('腘绳肌腱', [(0, 12, MID, '束间、骨道界面可有液体，信号混杂（可持续到术后 1 年）'), (12, 24, LO, '之后与髌腱类似地成熟')]),
        ('同种异体', [(0, 24, HI, '成熟更慢，高信号可持续到 2 年')]),
    ]
    y = 170
    for name, segs in rows:
        dr.text((50, y + 22), name, font=font(28), fill=INK)
        for m in months:
            dr.line([sx(m), y, sx(m), y + 80], fill=(225, 225, 225), width=2)
        for a, b_, c, t in segs:
            dr.rounded_rectangle([sx(a) + 2, y + 10, sx(b_) - 2, y + 70], 10, fill=c)
        yy = y + 84
        for a, b_, c, t in segs:
            dr.rectangle([50, yy + 6, 72, yy + 28], fill=c)
            yy = para(dr, 80, yy, t, 28, W - 130, fill=GREY, gap=8)
        y = max(yy, y + 120) + 20
    y += 10
    for c, t in [(LO, '低信号（接近原生前交叉韧带 / 后交叉韧带）'), (MID, '中等或混杂信号'), (HI, '高信号（成熟中，力学较弱）')]:
        dr.rectangle([50, y + 4, 80, y + 30], fill=c); dr.text((96, y), t, font=font(28), fill=INK); y += 46
    y = para(dr, 50, y + 14, '动物实验（Weiler）：术后 6～12 周信号最高，此时移植物抗拉强度只剩初始的 7%～16%；'
             '6～24 个月信号与原生韧带无差异，强度回升到约 60%。', 28, W - 100, fill=RED)
    y = para(dr, 50, y + 4, '注：色条为编者按原文文字绘制的示意，起止时间是原文给出的大致范围，个体差异很大。', 25, W - 100, fill=GREY)
    return im.crop((0, 0, W, y + 20))


def figueroa():
    return card(1080, 'Figueroa 评分：用 MRI 给移植物“打分”（原文表 1）', [
        ('① 整合：骨道—移植物界面有没有滑液', '有 = 1 分；无 = 2 分', LT, TEAL),
        ('② 韧带化：移植物 > 50% 区域的信号', '低信号 = 3 分；等信号 = 2 分；高信号 = 1 分', PU, PUR),
        ('③ 合计（①＋②，2～5 分）', '2 分：移植物成熟不足\n3～5 分：韧带化和整合良好', GR, GRN),
    ], foot='原表把合计一栏写作“移植物特征：差 = 2 分，充分 = 3～5 分”，编者按表注改写为合计分的解读。')


def checklist():
    return card(1080, '术后 MRI 读片清单（编者根据原文整理）', [
        ('① 移植物信号', '对照术后时间和移植物类型判断是否“该亮”；远端 2/3 信号增高要想到髁间窝撞击', PK, RED),
        ('② 移植物完整性', 'T2 上移植物体部信号增高、走行不连续提示再断裂；MRI 敏感度约 60%、特异度约 87%，必须结合查体和外伤史', OR, ORG),
        ('③ 骨道位置', '矢状位：胫骨骨道中心约在平台前后径 42%，前缘在 Blumensaat 线切线之后；股骨骨道在股骨后皮质线与髁间窝外侧壁交点', BL, BLU),
        ('④ 移植物倾角', '矢状位 ≤ 60°（原生 50°～60°）；冠状位 < 75°。过陡（过于垂直）控制旋转差', PU, PUR),
        ('⑤ 骨道扩大 / 囊肿', '多发生在术后前 3 个月，之后稳定；MRI 测量可靠性差，要精确测请做 CT；> 15 mm 常需分期翻修', LT, TEAL),
        ('⑥ 固定物与取腱处', '金属伪影、螺钉移位或断裂；髌腱增厚和缺口、Hoffa 脂肪垫水肿、关节纤维化；腘绳肌腱再生情况', GR, GRN),
        ('⑦ 骨性形态（危险因素）', '外侧胫骨平台后倾大、髁间窝窄、外侧间室胫骨前移位多、外侧胫骨平台窄', PK, RED),
    ])


CAPS = {
    1: '原文图 1　移植物的不同信号强度。信号强度通常用信号噪声商（SNQ）计算：SNQ =（前交叉韧带移植物信号 − 后交叉韧带信号）/ 背景信号。'
       'A 高信号移植物；B 信号已下降、但还没到原生前交叉韧带水平；C 与后交叉韧带等信号',
    2: '原文图 2　腘绳肌腱（股薄肌 + 半腱肌）自体移植重建成功、愈合过程正常。A 术后第 6 个月，T2 快速恢复快速自旋回波（FRFSE）上'
       '移植物体部可见一条高信号线，周围包绕中等信号组织（红箭头），代表血管化和滑膜化；'
       'B 术后第 12 个月，韧带周围信号消失，移植物信号下降、接近后交叉韧带',
    3: '原文图 3　26 岁男性，腘绳肌腱自体移植重建术后 3 年。质子密度加权快速自旋回波像上，髁间窝被信号稍高的黏液样组织占据（白箭头），'
       '看不出移植物的正常走行',
    4: '原文图 4　矢状位胫骨骨道定位。A 股骨骨道应位于股骨后皮质线（a 线）与髁间窝外侧壁的交点；伸膝位时胫骨骨道前缘应在 Blumensaat 线'
       '切线（b 线）之后，但不超过胫骨近端中点。胫骨骨道入口位置的测法：在最能看清入口的矢状层面量胫骨平台前后径（c 线），'
       '平台前缘到骨道入口最前点（点 1）的距离 ÷ 前后径 × 100%；后缘（点 3）和骨道中心（点 2）同法。'
       'B 胫骨骨道位于平台中点之前，撞击风险增加；C 胫骨骨道过于靠后，移植物过于垂直。'
       '原图注：原生前交叉韧带位于平台前后径的 31%～63%，中心在 48%',
    5: '原文图 5　矢状位移植物倾角的测量：胫骨近端轴线（a—b 线）的垂线（c—d 线）与关节内移植物走行线（e—f 线）之间的夹角，'
       '角度越大，矢状位上移植物越垂直。A 55°，在正常范围；B 移植物偏垂直，夹角 78°，远高于正常的 50°～60°',
    6: '原文图 6　冠状位移植物倾角的测量：胫骨平台切线（a—b 线）与关节内移植物走行线（c—d 线）之间的夹角，'
       '角度越大，冠状位上移植物越垂直。A 70°；B 移植物偏垂直，夹角 88°，远高于正常的 < 75°',
    7: '原文图 7　29 岁女性，腘绳肌腱自体移植重建术后 3.5 年。A 冠状位质子密度频谱衰减反转恢复（SPAIR）像：胫骨骨道明显扩大（16.0 mm）；'
       'B 矢状位 T1 快速自旋回波像：骨道内可见高信号囊肿（图中标注 15.9 mm；“前”为方位标记，原图为英文 A）',
    8: '原文图 8　冠状位质子密度压脂像。股骨侧金属挤压螺钉（黑星号）产生明显伪影，影响骨道位置的判断；'
       '胫骨侧的可吸收挤压螺钉（白星号）则没有这个问题',
    9: '原文图 9　30 岁男性，骨—髌腱—骨自体移植重建术后 2 年。A 轴位质子密度压脂像：取腱处病变表现为劈开的髌腱周围高信号（星号）；'
       'B 矢状位质子密度像：术后髌腱病表现为腱内信号增高（星号），髌腱增粗、肿胀',
    10: '原文图 10　21 岁男性，骨—髌腱—骨取腱后的自然转归。A 髌骨前表面的骨缺损（星号）；B 劈开后的低信号髌腱（星号）；'
        'C 胫骨结节前方中央的方形骨缺损（星号）',
    11: '原文图 11　26 岁男性，腘绳肌腱自体移植重建术后 1.5 年，矢状位质子密度像。移植物远端前方有一片低—中等信号区（黑箭头），'
        '符合局限性关节纤维化',
    12: '原文图 12　腘绳肌腱取腱后的自然转归。A 21 岁男性，术后 2 年，轴位：“鹅足”结构清楚，缝匠肌筋膜已再生（黑星号），'
        '股薄肌腱（红星号）、半腱肌腱增粗（白星号）；B 35 岁男性，术后 7 年：可见缝匠肌筋膜（黑星号），股薄肌腱（红星号）'
        '和半腱肌腱（白星号）变细、萎缩',
    13: '原文图 13　胫骨平台后倾角的测量。A 内侧平台：在经过内侧平台中部的矢状层面，量胫骨近端轴线（a—b 线）的垂线（c—d 线）'
        '与平台切线（e—f 线）的夹角（本例 15.1°）；B 外侧平台同法（本例 18.0°）。胫骨近端轴线应经过距关节线 5 cm 和 15 cm '
        '处两条胫骨前后径的中点。图中其余小号数字是测量软件残留读数',
    14: '原文图 14　股骨髁间窝横截面积的测量。选经过 Blumensaat 线中点的冠状层面；在经过腘肌沟、平行于股骨关节面（a—b 线）'
        '的直线（c—d 线）上量髁间窝宽度（红虚线）；关节面到髁间窝顶的距离为高度；面积（红框）= 宽（mm）× 高（mm）',
    15: '原文图 15　胫骨相对股骨前移位（前方半脱位）的测量。MRI 在伸膝、外旋位采集：内侧选经过腓肠肌内侧头止点的矢状层面，'
        '外侧选胫腓关节处腓骨最内侧的层面。沿股骨后髁软骨下线画圆（a），画胫骨平台切线（b—c 线）；'
        '量经过平台后缘、垂直于平台的直线（d—e 线）与平行于它并与圆相切的直线（f—g 线）之间的距离（红星号）。'
        '图中“周长 / 面积”是测量软件残留读数，已译成中文',
    16: '原文图 16　胫骨平台形态在能同时看到两侧胫骨髁间棘的冠状层面上评估。股骨外侧髁（a 线）、内侧髁（b 线）直径从对应关节软骨边缘量起；'
        '胫骨外侧平台（c 线）、内侧平台（d 线）直径从髁间棘量到平台边缘',
    17: '原文图 17　单束重建加外侧关节外成形 / 加强术（腘绳肌腱自体移植）的 MRI。A 冠状位：关节内部分（黑箭头）向近端越过股骨外侧髁'
        '（红箭头），走“过顶位”；B 轴位、C 冠状位：髂胫束深面的外侧关节外成形（星号），从股骨外侧髁延伸到 Gerdy 结节',
}


def cover():
    W, H = 900, 383; BG = (0, 70, 105); im = Image.new('RGB', (W, H), BG); dr = ImageDraw.Draw(im)
    f = raw(5)
    f = f.crop((0, 0, f.width // 2, f.height))
    f = f.resize((round(f.width * H / f.height), H), Image.LANCZOS)
    im.paste(f, (W - f.width, 0))
    dr.rectangle([0, 0, W - f.width, H], fill=BG)
    dr.text((40, 56), '前交叉韧带', font=font(64), fill='white')
    dr.text((40, 140), '重建术后 MRI', font=font(56), fill=(255, 220, 140))
    dr.text((40, 236), '移植物信号 · 骨道 · 取腱处', font=font(27), fill='white')
    dr.text((40, 280), '实用读片指南', font=font(27), fill='white')
    return im


if __name__ == '__main__':
    save(head(), 1)
    save(capbox(raw(1), CAPS[1]), 2)
    save(timeline(), 3)
    save(capbox(raw(2), CAPS[2]), 4)
    save(figueroa(), 5)
    for n in range(3, 18):
        save(capbox(raw(n), CAPS[n]), n + 3)
    save(checklist(), 21)
    cover().save(f'{OUT}/cover.jpg', quality=90)
    print('done')
