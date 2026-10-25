#!/usr/bin/env python3
"""Jorge 等 2024《三种腘绳肌强化训练与冲刺的肌肉活动和运动学比较》（IJSPT）推文配图。
首图中文标题卡、原文图 1（照片，只加中文图注）、研究流程卡、原文图 3～5（图中英文已用 tools/fig-translate 走位图路线译成中文：
src/fig3_zh.png 等）、腘绳肌平均激活重绘图、临床要点卡、封面。原文图 2（反光标记点示意）与解读关系不大，未采用。
用法：python3 make_figs.py <src 目录> <输出目录> <中文字体>"""
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)


def raw(name):
    return Image.open(f'{SRC}/{name}').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        # 标点不放行首
        # 数字和小数点不拆开
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in '，。；：、）”' and not (line[-1:] in '0123456789.' and ch in '0123456789.%'):
            dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
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
    im = Image.new('RGB', (W, 6000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 6000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


def avg_chart():
    """腘绳肌平均激活（占最大冲刺的 %），数值取自原文表 2 的平均值（AV）列"""
    W = 1200; im = Image.new('RGB', (W, 900), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '收缩阶段的平均激活（占最大冲刺的 %）', font=font(36), fill='white')
    rows = [('杠杆髋伸', 70, 58), ('PM快', 54, 44), ('北欧挺', 36, 32), ('PM慢', 35, 30), ('跑台跑（75% 速度）', 30, 28)]
    L, R = 330, W - 80; X = lambda v: L + (R - L) * v / 100
    BF, ST = (200, 90, 40), (0, 110, 130)
    dr.rectangle([L, 104, L + 26, 130], fill=BF); dr.text((L + 36, 100), '股二头肌长头', font=font(26), fill=INK)
    dr.rectangle([L + 260, 104, L + 286, 130], fill=ST); dr.text((L + 296, 100), '半腱肌', font=font(26), fill=INK)
    y = 170
    for name, bf, st in rows:
        dr.text((L - 20, y + 30), name, font=font(28), fill=INK, anchor='rm')
        dr.rectangle([L, y, X(bf), y + 28], fill=BF); dr.text((X(bf) + 10, y + 14), f'{bf}%', font=font(24), fill=BF, anchor='lm')
        dr.rectangle([L, y + 34, X(st), y + 62], fill=ST); dr.text((X(st) + 10, y + 48), f'{st}%', font=font(24), fill=ST, anchor='lm')
        y += 110
    for v in (0, 25, 50, 75, 100):
        dr.line([X(v), 160, X(v), y - 20], fill=(225, 225, 225), width=1)
        dr.text((X(v), y - 10), str(v), font=font(24), fill=GREY, anchor='ma')
    y += 40
    y = para(dr, 40, y, '数值为原文表 2 的平均值，编者重绘；最大冲刺的峰值 = 100%。峰值激活四个动作都接近或超过冲刺（见前一张原文图 3），差距主要在平均值上。', 24, W - 80, fill=GREY)
    return im.crop((0, 0, W, y + 10))


# 1 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '横断面研究 · 《International Journal of Sports Physical Therapy》2024', font=font(30), fill=TEAL)
dr.text((70, 135), '三种腘绳肌强化训练与冲刺跑', font=font(56), fill=INK)
dr.text((70, 210), '肌肉活动和运动学比较', font=font(44), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Jorge A, Lichtenstein E, Faude O, Roth R.', font=font(26), fill=GREY)
dr.text((70, 390), 'Int J Sports Phys Ther. 2024;19(5):569-580. doi:10.26603/001c.116158', font=font(26), fill=GREY)
dr.text((70, 435), '瑞士巴塞尔大学 运动、锻炼与健康系', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作非商业学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(raw('fig1.jpg'), '原文图 1  三个动作的起止姿势。自上而下：A 杠杆髋伸器（Rocker）；B 球上单腿髋伸（Perpetuum mobile，分快、慢两种做法）；C 北欧挺'), 2)

save(card(1200, '研究怎么做（编者根据原文整理）', [
    ('谁', '8 名男性业余运动员（来自冲刺类项目），平均 24 岁；每周冲刺相关训练超过 4.5 小时、坚持至少一年；近 6 个月下肢无伤', LT, TEAL),
    ('第 1 次：熟悉', '约 45 分钟：学会标准热身和动作技术，定好每个动作的负荷（杠杆档位、北欧挺板的坡度）；至少 48 小时后正式测试', GR, (0, 120, 60)),
    ('第 2 次：测试', '热身 → 室外 40 m 全力冲刺 2 次（作为 100% 参照）→ 跑台以最大冲刺速度的 75% 跑（约 23.9 km/h）→ 4 个动作随机顺序，各 3 次，间隔 5 分钟', OR, (200, 120, 0)),
    ('测什么', '右腿 4 块肌肉的表面肌电：臀大肌、股二头肌长头、半腱肌、腓肠肌内侧头\n12 台摄像机三维动作捕捉：腘绳肌激活峰值出现时的髋、膝屈曲角度\n“拉长应力” = 髋屈角减膝屈角，数值越大腘绳肌被拉得越长', PK, RED),
]), 3)

save(capbox(raw('fig3_zh.png'), '原文图 3  4 个动作和跑台跑的峰值激活（上）与平均激活（下），以最大冲刺为 100%（虚线），横线为 95% 置信区间。GMax 臀大肌；BFlh 股二头肌长头；ST 半腱肌；GCM 腓肠肌内侧头（图中英文由编者译成中文，肌肉缩写保留原文）'), 4)
save(avg_chart(), 5)
save(capbox(raw('fig5_zh.png'), '原文图 5  股二头肌长头 / 半腱肌激活比值，大符号为均值，小点为每个人；虚线 = 1 表示两块肌肉一样活跃（图中英文由编者译成中文）'), 6)
save(capbox(raw('fig4_zh.png'), '原文图 4  左：髋角、膝角的定义；右：腘绳肌激活峰值出现时的髋、膝屈曲角度。* 与右侧其余各项不同；† 两者之间不同（图中英文由编者译成中文）'), 7)

save(card(1200, '落到临床（编者整理）', [
    ('想要高激活', '杠杆髋伸和爆发式的球上单腿髋伸，平均激活明显高于北欧挺；没有专用器械时，球上单腿髋伸和爆发式单腿臀桥类动作是现成的选择', LT, TEAL),
    ('北欧挺要做全程', '本研究把北欧挺做成“只做 3 次不失控”的短幅度版本；作者建议全程、不失控地做，可能更能练到股二头肌长头', OR, (200, 120, 0)),
    ('髋主导 + 膝主导搭配', '所有动作股二头肌长头都略高于半腱肌，但比值个体差异大；两类动作都练，才能照顾到内外侧腘绳肌', GR, (0, 120, 60)),
    ('这些动作都练不到“长位”', '峰值都出现在腘绳肌较短的位置，拉长应力全为负值；要练长位离心，还得配合北欧挺全程、髋屈位离心和逐步加量的高速跑', PK, RED),
    ('别把肌电当疗效', '这只是 8 个人的一次性测量；这些动作能不能提升冲刺、降低拉伤风险，还没有训练研究证明', PU, (110, 70, 190)),
]), 8)

# 封面：原文图 1 第一行（杠杆髋伸器）
c = raw('fig1.jpg'); c = c.crop((0, 0, c.width, c.height // 3))
w = c.width; h = round(w * 383 / 900)
if h > c.height: h = c.height; w = round(h * 900 / 383)
x0 = (c.width - w) // 2; y0 = (c.height - h) // 2
c.crop((x0, y0, x0 + w, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
