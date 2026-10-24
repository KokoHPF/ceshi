#!/usr/bin/env python3
"""Sieng 等 2025 女篮运动员 Latarjet 术后康复病例：首图中文标题卡、四期康复方案卡（附录 A＋正文）、
原文图 1～4（annotate.py 加中文标注，见 annotate_spec.json）配中文图注、患者自评结局图、封面。
用法：python3 make_figs.py <work 目录> <输出目录> <字体>"""
import sys
from PIL import Image, ImageDraw, ImageFont
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


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '病例报告 · 《IJSPT》2025', font=font(32), fill=TEAL)
dr.text((70, 140), '盂唇修补失败后行 Latarjet 术：', font=font(54), fill=INK)
dr.text((70, 215), '一名女性过头运动员的康复（住院医师病例报告）', font=font(50), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Sieng T, Cicciaro J, Michelini J, Farmer K, Zeppieri G.', font=font(26), fill=GREY)
dr.text((70, 405), 'Int J Sports Phys Ther. 2025;20(9):1388-1400. doi:10.26603/001c.143147', font=font(28), fill=GREY)
dr.text((70, 450), '美国佛罗里达大学健康中心康复科、运动医学科 等', font=font(26), fill=GREY)
dr.text((70, 540), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, 'Latarjet 术后康复：第 1～2 期（附录 A＋正文，编者整理）', [
    ('第 1 期 保护期（0～6 周）', '注意事项：吊带 6 周（睡觉也戴）；不提物、不负重；肩、肘不做主动活动；不做主动屈肘和抗阻屈肘、旋后（保护随喙突一起移位的肱二头肌短头和喙肱肌）\n0～3 周：被动前屈到能耐受；肩胛平面被动外旋 ≤30°（肩胛下肌劈开）；不做外展、内旋和 90° 外展位外旋；腕手主动活动\n4～6 周：加钟摆、助力活动（外展 ≤90°）；亚极量等长收缩、肩胛时钟、弹力带外旋、节律稳定、上肢功率车；附录还列了血流限制训练（30/15/15/15 次）\n正文实际：第 1 周肩胛主动活动，第 2 周亚极量等长，第 3 周节律稳定、轻弹力带划船和外旋，第 4 周俯卧水平外展、侧卧外旋、仰卧 PNF D2、靠墙滑动等', LT, TEAL),
    ('第 2 期 中间期（7～11/12 周）', '目标：被动、主动活动度恢复正常，开始增加力量和耐力\n7～9 周：关节松动（以后方为主）；各方向活动度到耐受（90° 外展位内旋到 60°）；低负荷高次数（2～3 组×12～15 次）练肩胛稳定肌、侧卧外旋；第 8 周开始闭链：墙→治疗床→地面改良平板→标准平板，再加重心转移和拍肩\n10～12 周：负荷到 3～5 组×8～12 次；双手胸前传球等轻量增强式训练、双手对墙运球；9.5 周回到场上做非对抗体能训练，所有动作在胸部高度以下', GR, (0, 120, 60)),
]), 2)
save(card(1200, 'Latarjet 术后康复：第 3～4 期（附录 A＋正文，编者整理）', [
    ('第 3 期 强化期（12～15/16 周）', '目标：力量、耐力、神经肌肉控制和爆发力恢复正常\n伸展：外旋不超过 90/90 位\n整体力量：窄距俯卧撑、部分幅度卧推、水平和垂直划船、过头推举（肘保持在身体中线前方）\n增强式：单手对墙运球（外展 90°、120°、160°，以及外展 90°＋屈肘 90°），再到药球胸前抛接、过头砸球、旋转抛接、增强式俯卧撑\n投篮进阶：篮下 3 英尺、5 个点“定点投篮”（不起跳），每次投进 50 个，每周后退 3 英尺到罚球线；16 周开始跳投', OR, (200, 120, 0)),
    ('第 4 期 回归期（16～24 周）', '16 周：力量和运动表现测试，达标后医生放行\n先半场再全场非对抗训练；20 周 1 对 1 对抗 → 21 周 2 对 2 → 22 周 3 对 3 → 23 周 4 对 4 → 24 周 5 对 5\n术后 5 个月：全场对抗赛；放行后继续理疗，维持活动度和力量', PK, RED),
    ('和 Bankart 术后康复的不同', '被动外展、外旋和抗阻训练都推迟：前 3 周外旋限制在 30°，6 周后才做外展位外旋；抗阻训练等 6 周复查 X 线确认骨块愈合后再开始（Bankart 一般 4 周左右）；但回归比 Bankart（常见 6～9 个月）更早', (240, 240, 248), (90, 70, 170)),
]), 3)

CAP = [
    ('fig1.zh.jpg', '原文图 1  外旋耐力测试：背靠墙站，术侧肩前屈 90° 握住固定在肩高的弹力带（女性用红色，约 1.7 kg），跟着节拍器拉到 90/90 外旋位。节拍每 20 秒加快 30 次/分（60→150），跟不上或做不到终点即停，记录时间'),
    ('fig2.zh.jpg', '原文图 2  单手坐姿推铅球测试：背靠墙坐，用 6 磅（约 2.7 kg）球从肩高处推出，尽量不借腿和躯干的力；试推 2 次后正式推 3 次，取平均距离'),
    ('fig3.zh.jpg', '原文图 3  上肢旋转测试（ULRT）：靠墙前臂撑平板，以支撑侧上肢为轴转体，另一手拍墙（手臂垂直地面），兼顾开链、闭链、躯干旋转和 90/90 肩位；记录 15 秒内拍墙次数'),
    ('fig4.zh.jpg', '原文图 4  单手对墙运球：A 外展 90°；B 外展 120°；C 外展 160°；D 外展 90°＋屈肘 90°；E 同 D，同时由治疗师用弹力带拉向外旋；F 过头运球，同时用弹力带拉向后伸。选这些角度是因为她正是在单手过头传球（外展外旋位）时脱位的'),
]
for n, (f, c) in enumerate(CAP, start=4): save(capbox(op(f), c), n)

# 患者自评结局图
font_manager.fontManager.addfont(sys.argv[3]); plt.rcParams['font.family'] = font_manager.FontProperties(fname=sys.argv[3]).get_name()
fig, axs = plt.subplots(2, 2, figsize=(12, 8.4), dpi=100)
t = ['术后\n第 1 天', '8 周', '16 周', '9 个月']
for ax, (v, lab, c, top) in zip(axs.flat, (([28, 42, 90.5, 99], 'PSS（0～100，越高越好）', '#188080', 115), ([0, 40, 93, 99.99], 'SANE（%，越高越好）', '#E8A200', 115),
                                          ([100, 50, 50, 6.25], 'QuickDASH（0～100，越低越好）', '#D9432F', 115), ([10, 3, 2, 1], 'OSPRO-YF 心理“黄旗”数（越少越好）', '#5A46AA', 12))):
    r = ax.bar(range(4), v, color=c, width=.55)
    for q, y in zip(r, v): ax.text(q.get_x() + q.get_width() / 2, y + top * .02, f'{y:g}', ha='center', fontsize=15)
    ax.set_xticks(range(4), t); ax.set_ylim(0, top); ax.set_title(lab, fontsize=18, pad=8)
    ax.tick_params(labelsize=14); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(f'{WORK}/pro.png', facecolor='white')
save(capbox(op('pro.png'), '原文表 1 重画：患者自评结局随时间的变化（PSS 宾夕法尼亚肩评分；SANE 单项数字评分，与伤前比的百分比；QuickDASH 上肢功能障碍；OSPRO-YF 心理黄旗计数）'), 8)

# 封面：原文图 4
c = op('x93.jpg').crop((0, 0, 977, 535)); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS); y0 = 40
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
