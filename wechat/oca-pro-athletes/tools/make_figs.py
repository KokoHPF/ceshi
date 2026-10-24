#!/usr/bin/env python3
"""Patel 等 2021 职业运动员同种异体骨软骨移植术后康复与回归：首图中文标题卡、五期康复方案卡（据原文表 1 和正文）、
原文图 1～9（加中文分图标签）和图 10（磁共振，relabel.py 把 “Figure 4a～4d” 改成中文，labels.json / fixes.json 在本目录）
配中文图注、封面。
用法：python3 make_figs.py <work 目录> <输出目录> <字体>"""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

WORK, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
op = lambda n: Image.open(f'{WORK}/{n}').convert('RGB')
def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
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


FB = ImageFont.truetype(sys.argv[3].replace('Medium', 'Bold'), 30)

C1, C2, C3 = (24, 128, 128), (238, 99, 72), (22, 50, 79)


def panels(im):
    """按竖直白缝把多联图分成几块，返回各块左边界"""
    a = np.asarray(im.convert('L')).mean(0) > 240; xs = [0]
    for x in range(1, im.width):
        if a[x - 1] and not a[x] and x - xs[-1] > 60: xs.append(x)
    return xs


def tag(im, items):
    """items: [(x, y, 文字, 颜色)]"""
    d = ImageDraw.Draw(im)
    for x, y, t, c in items:
        tw = d.textlength(t, font=FB); d.rounded_rectangle([x + 10, y + 10, x + 34 + tw, y + 56], 10, fill=c); d.text((x + 22, y + 13), t, font=FB, fill='white')
    return im


def fig(x, labels, W=1200):
    im = op(f'{x}.jpg'); s = W / im.width; im = im.resize((W, round(im.height * s)), Image.LANCZOS)
    if labels: xs = panels(im); tag(im, [(xx, 0, t, c) for xx, (t, c) in zip(xs, labels)])
    return im


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '临床述评 · 《IJSPT》2021', font=font(32), fill=TEAL)
dr.text((70, 140), '职业运动员同种异体骨软骨移植术后：', font=font(54), fill=INK)
dr.text((70, 215), '康复与重返赛场', font=font(54), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Patel S, Amirhekmat A, Le R, Williams RJ III, Wang D.', font=font(26), fill=GREY)
dr.text((70, 405), 'Int J Sports Phys Ther. 2021;16(3):941-958. doi:10.26603/001c.22085', font=font(28), fill=GREY)
dr.text((70, 450), '美国特种外科医院（HSS）运动康复中心、加州大学尔湾分校医学院', font=font(26), fill=GREY)
dr.text((70, 540), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, '五期康复：第 1～2 期（原文表 1＋正文，编者整理）', [
    ('第 1 期 术后即刻（0～2 周）', '负重：20% 足平放负重，双拐，支具锁在伸直位行走；睡觉锁伸直位 1 周\n活动度：立即开始被动活动，先拿伸直——1 周内至少到 0°，垫毛巾“垫脚跟”反复做；屈膝不强求，2 周内无僵硬地到 90° 即可（髌骨病灶术后 2～4 周限 90°）；膝下不垫枕头\n肌力：股四头肌等长、直腿抬高（配合神经肌肉电刺激），不能有伸膝滞后；腹肌和骨盆收紧、侧卧蚌式、屈膝外倒；可用血流限制训练（需医生同意）\n其他：髌骨各方向松动；加压冷疗至少 2 周', LT, TEAL),
    ('第 2 期（2～6 周）', '负重：2～4 周最多 50%，4～6 周可耐受负重；股四头肌控制好后解锁支具，4 周停用支具\n活动度：3 周 0～105°，4 周 0～115/120°，6 周 0～130°；屈膝约 90° 用短曲柄（90 mm）功率车，约 110° 换普通功率车\n肌力：双腿蹬腿 60°→0°（2～4 周）、90°→0°（4～6 周）；2～3 周双侧提踵；臀桥、平板、改良侧平板（图 3）\n步态和平衡：跨栏步态训练（图 2）；扶手重心转移 → 股四头肌控制好后单腿平衡；4～6 周切口愈合后水中训练；步态仍异常可用水下或减重跑台\n心理：做一些坐位的专项动作（如坐着运球、投篮）', GR, (0, 120, 60)),
]), 2)
save(card(1200, '五期康复：第 3～5 期（原文表 1＋正文，编者整理）', [
    ('第 3 期（6～12 周）', '活动度：达到全范围；加股四头肌、屈髋肌拉伸，开始泡沫轴\n肌力：多平面臀和髋（髋时钟、怪兽步，图 4）；徒手深蹲先学髋铰链（图 5）；离心蹬腿（双上单下）；坐箱深蹲、悬吊深蹲；6～8 周上台阶，8～12 周离心下台阶（4→6→8 英寸）；弓步、单腿罗马尼亚硬拉（图 6）；开链伸膝从多角度等长开始\n心肺：先练上肢（上肢功率车、TABATA 20 秒练 10 秒歇 ×8）；约 8 周低阻力功率车，8～12 周间歇骑车；深水跑\n核心：站立 Pallof 推（图 7）', OR, (200, 120, 0)),
    ('第 4 期（12～20 周）', '肌力：重点练离心；单腿蹲从垫块、悬吊辅助开始（图 8）；离心下台阶；等速伸膝（中高速）；每周 3～4 次\n跑步：能控制好地下 8 英寸台阶、医生确认愈合后，16～18 周（约 4～5 个月）开始减重跑台或水中跑\n专项：篮球运球、原地投篮 → 轻上篮；网球原地挥拍 → 轻侧移\n进阶标准：股四头肌、腘绳肌肢体对称 80%，活动后不痛不肿', PK, RED),
    ('第 5 期（20 周以后）', '6 个月复查磁共振（图 10）：软骨面完整、骨长入、无积液；加上动作好、股四头肌控制好、两侧力量差 <20%，才开始跑跳等高冲击\n增强式和敏捷训练（双腿 → 单腿），注意髌股关节负荷；先预设路线的训练，再到随机反应；非对抗 → 对抗 → 受控实战 → 全场比赛，初期限制上场时间\n回归标准：力量对称 ≥90%、动作对称、专项动作不恐惧；回归后通常还需 3～4 个月体能训练才能恢复伤前竞技水平', (240, 240, 248), (90, 70, 170)),
]), 3)

FIGS = [
    ('x66', None, '原文图 1  垫毛巾“垫脚跟”被动伸膝：毛巾卷垫在足跟下，靠重力做长时间、低负荷的伸膝牵拉，每天多次，尽早拿到完全伸直'),
    ('x78', [('a 起始', C1), ('b 最大屈膝＋对侧臂前摆', C3), ('c 足跟着地＋股四头肌收缩', C2)], '原文图 2  单个小栏架跨步：训练摆动期屈膝、足跟着地时伸膝和股四头肌发力，纠正长期戴支具形成的划圈步态'),
    ('x79', 'manual', '原文图 3  初步动力链训练：a 膝上套弹力带的双腿臀桥；b 前平板支撑；c 改良侧平板支撑——分别激活后侧、前侧和外侧'),
    ('x87', None, '原文图 4  弹力带站立“髋时钟”：支撑腿保持对线，另一腿朝不同方向点地，练多平面臀肌和髋部力量；要随时用口头和手法提示纠正膝外翻'),
    ('x88', None, '原文图 5  双腿深蹲的正确髋铰链：屈髋、臀部后坐，把负荷分给髋和近端肌群，减轻膝关节压力'),
    ('x94', [('a 单腿罗马尼亚硬拉', C1), ('b 侧弓步（哥萨克蹲）', C2)], '原文图 6  用髋铰链减轻膝关节压力：a 单腿罗马尼亚硬拉；b 侧弓步 / 哥萨克蹲。重点是慢速离心控制和动作质量'),
    ('x101', [('a 冠状面', C1), ('b 矢状面', C3), ('c 水平面', C2)], '原文图 7  Pallof 推的变式：a 冠状面（核心激活时机）；b 矢状面（核心力量）；c 水平面（抗旋转稳定）。站立完成，练习把力从稳定的下肢经躯干传到上肢'),
    ('x102', [('a 脚下垫块', C1), ('b 悬吊带辅助', C2)], '原文图 8  单腿蹲进阶：a 在一侧脚下垫瑜伽砖等，减少该侧负重；b 用悬吊带（TRX）辅助单腿蹲'),
    ('x109', [('a 错误', C2), ('b 正确', C1)], '原文图 9  动力链“断链”：a 向上拉绳时肋骨外翻、腰椎前凸增大，力没有通过核心传递；b 核心稳定，力沿整个动力链分散'),
]
n = 4
for x, lab, c in FIGS:
    if lab == 'manual':
        im = op('x79.jpg'); im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS); k = 1200 / 962
        tag(im, [(0, 0, 'a 弹力带臀桥', C1), (round(468 * k), 0, 'b 前平板', C3), (round(468 * k), round(322 * k), 'c 改良侧平板', C2)])
    else: im = fig(x, lab)
    save(capbox(im, c), n); n += 1
save(capbox(op('zh/x115.zh.jpg'), '原文图 10  一名职业篮球运动员的轴位磁共振：术后第 1 天的滑车（A，2 枚骨柱）和髌骨（B）；术后 6 个月滑车（C）和髌骨（D）的骨柱已逐步骨性愈合，关节软骨面保持完整。原图标注为 “Figure 4a～4d”，已改为中文'), n)

# 封面：原文图 7（Pallof 推）
c = op('x101.jpg'); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS); y0 = max(0, (c.height - 383) // 2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok', n)
