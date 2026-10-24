#!/usr/bin/env python3
"""Carvalho 等 2026 髌股疼痛：强化股四头肌、髋外展肌和外旋肌对下肢轴向力线的影响。
首图中文标题卡、原文图 1（训练动作照片，只有面板字母，原样引用）、四项影像指标说明卡、原文图 4（TT–TG 测量，原样引用）、
原文图 7～10（paper-figure-zh 译成中文后拼成 2×2）、临床要点卡、封面。
用法：python3 make_figs.py <work 目录> <输出目录> <字体>
work 目录需要：fig1.png、fig4.png（pymupdf 按图片区域 300 dpi 导出）、zh_p11_1.png、zh_p12_1.png、zh_p12_2.png、zh_p13_1.png（figtrans render 输出）"""
import sys
from PIL import Image, ImageDraw, ImageFont

WORK, OUT, F = sys.argv[1], sys.argv[2], sys.argv[3]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
op = lambda n: Image.open(f'{WORK}/{n}').convert('RGB')
def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        # 标点不放行首
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”': dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t


def card(W, title, blocks):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '前瞻性干预队列（单组前后对照）· 《J Funct Morphol Kinesiol》2026', font=font(32), fill=TEAL)
dr.text((70, 135), '强化股四头肌、髋外展肌和外旋肌', font=font(54), fill=INK)
dr.text((70, 205), '能否改变髌股疼痛大学生的下肢轴向力线', font=font(54), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Gir de Carvalho RA, Pizzolato BB, de Souza GPA, …, Buchaim RL, Munhoz MAS.', font=font(26), fill=GREY)
dr.text((70, 390), 'J Funct Morphol Kinesiol. 2026;11(2):225. doi:10.3390/jfmk11020225', font=font(28), fill=GREY)
dr.text((70, 435), '巴西容迪亚伊医学院（FMJ）、圣保罗大学等', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(op('fig1.png'), '原文图 1  12 个训练动作（A～L 为训练顺序，对应下文表 1）：A 靠墙等长髋外展；B 坐姿伸膝器械；C 髋外展器械；'
            'D 弹力带深蹲＋髋外展；E 侧卧弹力带髋外展＋外旋（蚌式）；F 交替单腿臀桥（等长）；G 四点跪位弹力带髋外展＋外旋；'
            'H 侧卧沙袋髋外展（伸膝）；I 弹力带侧向行走；J 坐姿拉力器髋外旋；K 弹力带臀桥＋髋外展（等长）；L 站姿拉力器髋外展＋外旋'), 2)

save(card(1200, '研究看的 4 个影像指标（编者整理）', [
    ('股骨颈前倾角（FNA）', '股骨颈轴线与股骨髁后缘连线的夹角，反映股骨“扭转”。成人一般 8°～20°，>20° 算增大。'
     '属于骨性结构，成年后基本定型', LT, TEAL),
    ('胫骨结节–滑车沟距离（TT–TG）', '把胫骨结节最高点和股骨滑车沟最深点两层 CT 叠在一起，量两者的内外侧距离（mm）。'
     '≥20 mm 视为异常，提示伸膝装置偏外、髌骨不稳风险高。股骨和胫骨之间的旋转也会改变它', GR, (0, 120, 60)),
    ('胫骨外旋角（TET）', '胫骨平台后缘切线与内外踝连线的夹角，反映胫骨“扭转”。同样是骨性结构', OR, (200, 120, 0)),
    ('Q 角（3D-CT）', '本研究在三维重建上从股骨大转子顶点画线到髌骨中心，再连到胫骨结节；'
     '与临床常用的从髂前上棘起画线不同，数值不能和临床 Q 角直接比较', PK, RED),
    ('共同条件', '仰卧、泡沫垫固定下肢、足尖朝上 90°，训练前和训练后用同一摆位扫描。都是静态、非负重的测量', (240, 240, 240), GREY),
]), 3)

save(capbox(op('fig4.png'), '原文图 4  TT–TG 的 CT 测量：A 选两层（1 滑车沟最深点，2 胫骨结节最高点）；B、C 两层的轴位像；'
            'D 两层叠加，R 为股骨髁后缘连线，从滑车沟最深点（TG）和胫骨结节（TT）各作 R 的垂线，两线间距即 TT–TG（图中示例 26 mm）'), 4)

# 原文图 7～10 中文版拼成 2×2
ims = [op(f'zh_{n}.png') for n in ['p11_1', 'p12_1', 'p12_2', 'p13_1']]
w = 700; ims = [i.resize((w, round(i.height * w / i.width)), Image.LANCZOS) for i in ims]
h = max(i.height for i in ims); g = Image.new('RGB', (w * 2 + 16, h * 2 + 16), 'white')
for k, i in enumerate(ims): g.paste(i, ((k % 2) * (w + 16), (k // 2) * (h + 16)))
save(capbox(g, '原文图 7～10（图中英文由编者译为中文）：左上 股骨颈前倾角，右上 TT–TG，左下 胫骨外旋角，右下 3D-CT Q 角。'
            '箱线图标注最小值、下四分位、均值、上四分位、最大值；* 表示训练前后差异有统计学意义'), 5)

save(card(1200, '这篇研究落到临床（编者整理）', [
    ('能说的', '12 周、每周 3 次、以髋外展和外旋为主、加上股四头肌的抗阻训练，10 名久坐的髌股疼痛大学生'
     '训练后 CT 上 TT–TG 平均小了 1.5 mm，3D-CT Q 角平均小了 1.1°', GR, (0, 120, 60)),
    ('不能说的', '没有对照组，不能排除测量误差、摆位差异和自然波动；没有报告疼痛和功能，不知道患者是否好转；'
     '股骨前倾和胫骨扭转没变，训练改变不了骨头', PK, RED),
    ('怎么用', '髋外展、外旋加股四头肌的组合本来就是指南推荐的一线方案，主要目的是减痛、改善功能和动态控制。'
     '不要向患者承诺“练肌肉能把力线矫正过来”', LT, TEAL),
]), 6)

# 封面：原文图 1 上排
c = op('fig1.png'); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
