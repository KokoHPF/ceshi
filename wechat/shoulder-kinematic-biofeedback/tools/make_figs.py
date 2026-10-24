#!/usr/bin/env python3
"""Parel 等 2023 肩袖修补术后运动学生物反馈康复方案：首图中文标题卡、原文图 1～2（界面截图，relabel.py 原位改中文，
labels.json / fixes.json 在本目录，输出 work/zh/）、原文图 3～14 练习照片（裁白边、加“起始 / 终点”标签）配中文图注、
常规康复四期卡、封面。
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

OK, NG = (24, 128, 128), (238, 99, 72)


def trim(im):
    g = np.asarray(im.convert('L')) < 235; ys, xs = np.where(g)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def ab(x):
    """原图 a/b 两张并排：裁白边，在两半左上角加“起始 / 终点”"""
    im = trim(op(f'{x}.jpg')); im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS); d = ImageDraw.Draw(im)
    for x0, (t, c) in ((0, ('a 起始', OK)), (im.width // 2, ('b 终点', NG))):
        tw = d.textlength(t, font=FB); d.rounded_rectangle([x0 + 14, 14, x0 + 40 + tw, 62], 10, fill=c); d.text((x0 + 27, 18), t, font=FB, fill='white')
    return im


# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '方案论文 · 《JMIR Research Protocols》2023', font=font(32), fill=TEAL)
dr.text((70, 140), '关节镜肩袖修补术后的运动学生物反馈康复训练：', font=font(48), fill=INK)
dr.text((70, 210), '一套新的整合康复方案', font=font(48), fill=INK)
dr.line([70, 320, W - 70, 320], fill=(200, 205, 210), width=2)
dr.text((70, 350), 'Parel I, Candoli V, Filippi MV, Padolino A, Merolla G, Sanniti S, Galassi R, Paladini P, Cutti AG.', font=font(24), fill=GREY)
dr.text((70, 395), 'JMIR Res Protoc. 2023;12:e35757. doi:10.2196/35757', font=font(28), fill=GREY)
dr.text((70, 440), '意大利罗马涅地方卫生局生物力学实验室、肩肘外科、康复医学科；意大利国家工伤保险局假肢中心', font=font(24), fill=GREY)
dr.text((70, 530), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, '医院原有的常规康复：四期（编者根据原文整理）', [
    ('第 1 期（术后 1～21 天）', '防旋转吊带固定 21 天；只在个人护理和活动肘、手时取下；只允许肩胛上提 / 下沉、前伸 / 后缩的滑动，盂肱关节保持休息位；第 15 天起每周 2 次门诊康复', LT, TEAL),
    ('第 2 期（21～35 天）', '逐步去吊带；肩胛平面 90° 以下被动活动（不做旋转），再逐步超过 90°；肩胛骨松动；激活肩胛稳定肌和肱骨头下压肌群，改善姿势；避免过度牵拉修补的肌腱；每周 2 次', GR, (0, 120, 60)),
    ('第 3 期（35～60 天）', '恢复全范围被动活动；开始盂肱外旋和主动上举；加入水中训练；每周 4 次（2 次门诊＋2 次小组水疗）', OR, (200, 120, 0)),
    ('第 4 期（60 天～回归工作）', '用哑铃、弹力带逐步加负荷的动态力量训练和功能训练；每周 2 次门诊，必要时再加 2 次水疗', PK, RED),
    ('生物反馈方案从哪天加入', '术后第 45 天（或按手术医生要求）开始，直到康复结束；每次 10 分钟穿戴和校准传感器，30 分钟有效训练，每周 2 次', (240, 240, 248), (90, 70, 170)),
]), 2)

save(capbox(op('zh/x52.zh.jpg'), '原文图 1  肩肱协调图：横轴为肱骨屈伸角度，纵轴为肩胛骨上回旋 / 下回旋角度（原文称内外侧旋转），曲线显示抬臂和放下过程中肩胛骨跟着转了多少；右侧柱为实时活动度。图中英文已改为中文'), 3)
save(capbox(op('zh/x79.zh.jpg'), '原文图 2  时间图：以肘关节为例，三条曲线分别为屈伸、提携角、旋前旋后随时间的变化。单一关节角度的练习用这种图。图中英文已改为中文'), 4)

CAP = [
    ('x105', '原文图 3  第 1 组 A：瑞士球辅助屈伸。双手放在凳上的瑞士球上、肩高、屈肘，双臂把球往前推到肱骨屈曲 ≥90°、伸肘；活动度增加后可加屈髋屈腰到 ≥120°。可减轻冈上肌和三角肌负担，是第一个做的练习'),
    ('x106', '原文图 4  第 1 组 B：持棒辅助屈伸。站或坐，双手握棒（与肩同宽），由健侧帮助伸肘上举到 ≥90°；注意躯干对齐、避免腰椎过伸，否则改坐位或减小幅度'),
    ('x118', '原文图 5  第 1 组 C：拉弹力带屈伸。先轻微外旋（拇指朝上）拉开弹力带，保持拉紧和外旋，伸肘上举到 ≥90°；弹力带能增加冈下肌、小圆肌激活'),
    ('x119', '原文图 6  第 1 组 D：开链屈伸（可负重）。伸肘上举到 ≥90°，可单臂做（避免躯干侧屈、旋转）；先不负重，再加哑铃或弹力带'),
    ('x132', '原文图 7  第 2 组 A：瑞士球辅助外展。手放在球上、肩高、屈肘，在肩胛平面把球向侧方推到 90°；活动度增加后加腰部侧屈到 ≥120°'),
    ('x133', '原文图 8  第 2 组 B：拉弹力带外展。拇指朝上轻微外旋拉开弹力带，保持拉紧，在肩胛平面上举到 ≥90°'),
    ('x146', '原文图 9  第 2 组 C：开链外展（可负重）。在肩胛平面上举到 ≥90°；先不负重，再逐步加负荷'),
    ('x155', '原文图 10  第 3 组 A：体侧内外旋。上臂贴体侧、屈肘 90°、手放腹部、拇指朝上，肘与躯干之间夹软球（或毛巾、小枕），夹住不掉做外旋'),
    ('x157', '原文图 11  第 3 组 B：前屈 90° 位内外旋。肱骨前屈 90° 并内旋、屈肘 90°、前臂水平，外旋到前臂竖直；先把上臂放在支撑面上，再脱离支撑'),
    ('x169', '原文图 12  第 3 组 C：外展 90° 位内外旋。肱骨在肩胛平面外展 90°、屈肘 90°，从前臂水平外旋到竖直；同样先有支撑、后无支撑'),
    ('x178', '原文图 13  第 4 组 A：扶凳俯卧撑。双脚着地、手扶凳或治疗床（越高负荷越小）、肱骨前屈 90°，屈伸肘，肘不超过躯干线；肩胛骨三个方向的时间曲线要尽量平'),
    ('x179', '原文图 14  第 4 组 B：前屈 90°～120° 位肩胛前伸后缩。坐位、伸肘，双臂同时做肩带前伸和后缩；先支撑肘和前臂，再悬空（可持重物），专门练前锯肌'),
]
for n, (x, c) in enumerate(CAP, start=5): save(capbox(ab(x), c), n)

# 封面：原文图 3（瑞士球辅助屈伸）
c = trim(op('x105.jpg')); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS); y0 = (c.height - 383) // 2
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
