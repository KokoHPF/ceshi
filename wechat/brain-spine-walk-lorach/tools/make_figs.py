#!/usr/bin/env python3
"""Lorach 等 2023 Nature 脑-脊髓接口恢复行走：首图为原题直译标题卡；试验时间线卡、BSI 链路卡和结果数字卡为编者根据原文正文和方法整理；
原文图 1～4 和扩展数据图 7 直接使用（页面区域截取，不做模糊处理）并加中文说明。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
doc = pymupdf.open(PDF)
raw = lambda x: Image.open(BytesIO(doc.extract_image(x)['image'])).convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def arrow_down(dr, cx, y0, y1, c=TEAL):
    dr.line([cx, y0, cx, y1 - 14], fill=c, width=6)
    dr.polygon([(cx - 16, y1 - 18), (cx + 16, y1 - 18), (cx, y1)], fill=c)


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * (len(tiles) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def pair(a, b, ca, cb, W=1200):
    """两张照片左右并排，各自上方加说明"""
    w = (W - 14) // 2
    ta, tb = capbox(a, ca, w), capbox(b, cb, w)
    h = max(ta.height, tb.height); out = Image.new('RGB', (W, h), 'white')
    out.paste(ta, (0, 0)); out.paste(tb, (w + 14, 0)); return out


def phases(title, S, n, fs=24):
    W = 1200; im = Image.new('RGB', (W, 2400), 'white'); dr = ImageDraw.Draw(im); y = 20
    for t, bg, c, items in S:
        h = 66 + sum(para_h(s, fs, 1040, gap=8) + 10 for s in items)
        dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
        yy = y + 62
        for s in items: yy = bullet(dr, 70, yy, s, fs, 1060, gap=8) + 10
        y += h + 16
    save(titled(im.crop((0, 0, W, y)), title), n)


def clip(pn, r):
    pm = doc[pn].get_pixmap(matrix=pymupdf.Matrix(4, 4), clip=pymupdf.Rect(*r))
    return Image.open(BytesIO(pm.tobytes('png'))).convert('RGB')


F1, F2, F3, F4 = clip(1, (40, 44, 558, 258)), clip(2, (40, 44, 558, 444)), clip(4, (40, 44, 560, 529)), clip(5, (40, 44, 560, 469))
E7 = raw(579)

# 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '原创研究 · Nature 2023', font=font(32), fill=TEAL)
for i, t in enumerate(['利用脑-脊髓接口实现脊髓损伤后的自然行走']):
    dr.text((70, 140 + i * 72), t, font=font(54), fill=INK)
dr.text((70, 250), 'Walking naturally after spinal cord injury using a brain–spine interface', font=font(30), fill=GREY)
dr.line([70, 340, W - 70, 340], fill=(200, 205, 210), width=2)
dr.text((70, 370), 'Lorach H, Galvez A, Spagnolo V, …, Charvet G, Bloch J, Courtine G.', font=font(28), fill=GREY)
dr.text((70, 414), 'Nature 2023;618(7963):126-133. doi:10.1038/s41586-023-06094-5', font=font(28), fill=GREY)
dr.text((70, 480), '瑞士洛桑联邦理工学院 / 洛桑大学医院 · 法国格勒诺布尔 CEA Clinatec 等', font=font(26), fill=GREY)
dr.text((70, 560), '编者中文重排，仅作学术交流（原文 CC BY 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(titled(capbox(F1, 'a 两块颅骨内植入物（各 64 个电极）贴在感觉运动皮层的硬膜外记录脑电（ECoG），随身处理单元解码运动意图，再通过植入式脉冲发生器和 16 电极桨状电极，刺激腰骶段脊髓后根入髓区，激活下肢肌肉；b 术前用脑磁图定位想动腿时激活的皮层区，术后确认植入位置；c 个体化模型计算桨状电极最佳位置并在术后确认'),
            '原文图 1　脑-脊髓接口的设计、技术和植入'), 2)

phases('从 STIMO 到 STIMO-BSI（编者根据原文正文和方法整理）', [
    ('受伤', (240, 240, 240), INK, ['骑自行车事故，颈髓 C5/C6 不完全损伤；入组 STIMO-BSI 时 38 岁、伤后 10 年']),
    ('伤后 7 年　STIMO 试验（只有脊髓刺激）', LT, TEAL, ['植入 16 电极脊髓硬膜外刺激系统，靠足部运动传感器或抬脚跟触发预设刺激序列',
        '5 个月强化康复后，开刺激能扶前轮助行器迈步；之后居家用刺激约 3 年（方法写 2 年），恢复进入平台期',
        '局限：起步、停步困难，只能走平地，上坡、跨障碍、上楼都不行；动作不够“自然”']),
    ('入组前 1 年', (240, 240, 240), INK, ['双侧足部手术：距舟关节融合、肌腱转移、趾长屈肌腱切断等（因此不报告趾长伸肌评分）']),
    ('STIMO-BSI 试验（脑控脊髓刺激）', PK, RED, ['双侧开颅，植入两块 WIMAGINE 记录器替换骨瓣，术后第 2 天出院',
        '休息 2 周后开始校准；6 周映射期（30 次）建立解码器和刺激程序库',
        '15 周神经康复共 40 次，每次 1～3 小时', '时间分配：实验室行走 49.1%、被动治疗 21%、技巧性行走 12.8%、户外 7.9%、单关节 5.1%、平衡 4.1%']),
    ('之后　居家使用', GR, (40, 120, 60), ['集成助行器自己操作，约 5 分钟完成设置；随访到 3 年延伸期结束',
        '第 167 天右侧植入物处金黄色葡萄球菌皮下感染，取出右侧装置；左侧继续工作；2023 年 3 月 9 日重新植入'])], 3)

phases('数字桥怎么工作（编者根据原文正文和方法整理）', [
    ('① 记录', LT, TEAL, ['WIMAGINE：直径 50 mm 的钛壳，厚度与颅骨相同，植入后看不出来', '每块 64 个电极，实际用 32 个，采样率 586 Hz',
        '头戴耳机里两根天线：13.56 MHz 无线供电，402～405 MHz 实时传出脑电']),
    ('② 解码', OR, (180, 90, 20), ['提取空间、频谱、时间特征；“门控”模型判断想动哪个关节（左右髋、膝、踝或休息），“专家”模型预测动作方向和幅度',
        '隐马尔可夫模型保证稳定；校准时每 15 秒在线更新一次参数']),
    ('③ 刺激', PK, RED, ['解码结果换算成各关节刺激程序的幅度，每 300 ms 更新一次，限制在预设功能范围内',
        '无线发给 ACTIVA RC 脉冲发生器（原用于帕金森病脑深部刺激），经 Specify 5-6-5 桨状电极（16 个触点）刺激后根入髓区；通信延迟约 100 ms']),
    ('和单纯脊髓刺激比', GR, (40, 120, 60), ['刺激什么时候开、开多大由大脑实时决定，不再靠传感器触发预设序列',
        '能自己决定起步、连续走、停下或站着不动'])], 4)

save(titled(capbox(F2, 'a 尝试屈左髋时与动作相关的皮层电极分布和频段；b 调整阴极阳极组合和刺激参数（300 µs、40 Hz、14～16 mA），极坐标图显示主要激活髂腰肌；c 坐位在线校准，约 90 秒后髋屈解码准确率达到 97%；d、e 同时控制双侧髋、膝、踝 7 种状态，解码准确率 74%，刺激准确率 83%'),
            '原文图 2　脑-脊髓接口的校准'), 5)
save(titled(capbox(F3, 'a 站立抬膝：开 BSI 后髂腰肌活动和膝抬高明显增加；b 行走中关掉 BSI 立刻迈不了步（有迈步意图但没有肌肉活动），重新打开马上恢复；c 髋屈刺激幅度范围；d 开、关 BSI 的髂腰肌活动、步高、最大髋屈和膝屈；e 户外行走和主动停下站立，停顿期间没有误触发；f 术后到 11 个月，每一步的髋屈解码概率曲线保持稳定'),
            '原文图 3　BSI 恢复对行走的自然控制'), 6)
save(titled(capbox(F4, '以下均在关闭刺激时评估。a 三个时间点的行走：STIMO 前需 35% 减重 + 踝足矫形器，STIMO 后需踝足矫形器，BSI 后不用矫形器、拄拐走；b 两次试验时间线和康复内容构成；c 最大屈髋和髋屈肌肌电；d 下肢运动评分 23 → 29 → 29 → 31；e WISCI II；f 6 分钟步行（STIMO 后进入平台）；g 独立站立、计时起立行走、Berg 平衡量表；h 6 名盲法物理治疗师的观察性步态评分'),
            '原文图 4　BSI 支持的神经康复后，关刺激也有改善'), 7)

phases('关键数字（编者根据原文整理）', [
    ('校准快', LT, TEAL, ['坐位控制髋屈：不到 2 分钟，准确率 97%', '7 种状态（双侧髋膝踝 + 休息）：准确率 74%（随机水平 14%），刺激准确率 83%', '解码延迟约 1.1 秒',
        '站立抬脚：校准 5 分钟，髂腰肌活动是不开 BSI 时的 5 倍']),
    ('能用很久', OR, (180, 90, 20), ['近 1 年里脑电功率平均每天只降 0.03 dB', '行走时髋屈解码准确率：术后 0.92 → 2 个月 0.93 → 6 个月 0.97 → 11 个月 0.97',
        '隔 2 个月用同一个解码器仍能控制 6 个关节；刺激阈值 1 年没变']),
    ('关刺激也进步了', GR, (40, 120, 60), ['WISCI II：STIMO 前 6 → BSI 后 16；能不靠任何帮助和刺激、拄拐走 10 米以上',
        '下肢运动评分：STIMO 后 29 → BSI 后 31；轻触觉评分 +4', '独立站立 +593%，Berg 平衡 +73%，计时起立行走 +72%；盲法步态评分显著提高']),
    ('在家能自己用', PU, (90, 60, 150), ['设置约 5 分钟，电池约 2 小时', '居家使用 7 个月，解码表现稳定', 'PIADS 问卷：安全感、熟练度、参与能力都达到最大增益'])], 8)

save(titled(capbox(E7, 'a 集成助行器装下笔记本电脑、基站和电池，约 2 小时续航；b 居家设置 6 步：戴耳机、载入程序、调整耳机位置、设刺激幅度上下限、开始刺激、日常康复或活动；c 回家后 181 天的累计步数、使用时长和每步解码概率（左、右髋）'),
            '原文扩展数据图 7　居家独立使用的设计'), 9)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), 'Nature · 脊髓损伤 · 脑-脊髓接口', font=font(34), fill=TEAL)
dr.text((50, 128), '用“意念”控制双腿：', font=font(60), fill=INK)
dr.text((50, 218), '瘫痪 10 年后再走路', font=font(60), fill=INK)
dr.text((50, 318), '数字桥 · 自然行走 · 关刺激也有恢复', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
