#!/usr/bin/env python3
"""Wang 等 2024 不同长度肌内效贴对慢性踝不稳侧切动作生物力学的影响：首图中文标题卡、实验示意图（原文图 1，标注用 relabel 原位改中文）、
短贴/长贴照片贴中文标签、关键曲线（原文图 5、7、8 的上排曲线，标题和横轴用 relabel 改中文；纵轴标题保留英文以免遮挡刻度）、
贴扎步骤卡、结果与矛盾卡、封面。relabel 配置见 work/labels.json、fixes.json、lab1.json、fx1.json。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
WORK, OUT, FM, FBOLD = sys.argv[1:5]
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('原创研究 · 《Healthcare》2024', ['不同长度肌内效贴对慢性踝不稳者', '侧切动作生物力学的影响'],
               'Wang X, Quan W, Ma Y, Jozsef S, Fang Y, Gu Y.', 'Healthcare. 2024;12(24):2561. doi:10.3390/healthcare12242561',
               '宁波大学体育学院、匈牙利塞格德大学工学院、宁波市第二医院放射科'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def legend(im):
    """在曲线图上方加中文图例"""
    im = k.op(im) if isinstance(im, str) else im; W = 1200; im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    o = Image.new('RGB', (W, im.height + 60), 'white'); o.paste(im, (0, 60)); d = ImageDraw.Draw(o); f = ImageFont.truetype(FBOLD, 28)
    x = 20
    for t, c, dash in [('NT 不贴', (20, 20, 20), False), ('ST 短贴', (220, 40, 40), True), ('LT 长贴', (30, 50, 220), True)]:
        if dash:
            for s in range(0, 60, 16): d.line([x + s, 30, x + s + 9, 30], fill=c, width=5)
        else: d.line([x, 30, x + 60, 30], fill=c, width=5)
        d.text((x + 70, 13), t, font=f, fill=c); x += 260
    d.text((x, 13), '下方横条＝有显著差异的支撑期区间', font=font(26), fill=GREY)
    return o

f1 = k.op('x93.zh.jpg'); ImageDraw.Draw(f1).rectangle([1212, 780, 1290, 900], fill='white'); f1.save(f'{WORK}/f1.jpg')
put('f1.jpg', '原文图 1  a：OpenSim 模型上的 38 个反光标记点；b：45° 侧切实验——从起点以舒适速度跑来，右脚踩上测力台，左脚向左前方 45° 迈进 1 米宽的通道完成变向')
put(tags_at(k, 'x122.jpg', [(.01, .01, '短贴 ①', C_OK), (.51, .01, '短贴 ②', C_OK), (.01, .51, '短贴 ③', C_OK), (.51, .51, '短贴 ④', C_OK)]),
    '原文图 2  短贴（只贴足踝）：①足背第一楔骨/第一跖骨沿胫骨前肌向上，止于踝上 6 cm；②足底第一跖骨绕外踝沿腓骨长肌向上，止于踝上 6 cm；③内踝沿胫腓骨后内缘向后上，止于踝上 6 cm；④外踝前方绕到足底，止于横弓')
put(tags_at(k, 'x148.jpg', [(.01, .01, '长贴 ①', C_HI), (.51, .01, '长贴 ②', C_HI), (.01, .51, '长贴 ③', C_HI), (.51, .51, '长贴 ④', C_HI)]),
    '原文图 3  长贴（跨到膝下）：起点相同，①止于胫骨平台；②止于腓骨头；③止于腘窝下方；④同短贴，止于横弓。每条张力 20%～35%，测完立即撕掉')
k.save(k.card('怎么贴（编者根据原文整理）', [
    ('材料', '5 cm 宽的商用肌内效贴；中等张力 20%～35%；参照 Jackson 等的贴法', LT, TEAL),
    ('短贴：4 条，都在足踝', '① 足背内侧 → 沿胫骨前肌 → 踝上 6 cm\n② 足底第一跖骨 → 绕外踝 → 沿腓骨长肌 → 踝上 6 cm\n③ 内踝 → 沿胫腓骨后内缘 → 踝上 6 cm\n④ 外踝前方 → 足底 → 横弓', GR, (0, 120, 60)),
    ('长贴：前 3 条延长到膝下', '① → 胫骨平台；② → 腓骨头；③ → 腘窝下方；④ 不变', OR, (200, 120, 0)),
    ('剪多长', '原文公式：剪裁长度 ＝ [（实际长度 - 8 cm）÷ 1.5 ＋ 8 cm] × 1.10\n（原文括号写法有歧义，这是编者按常见做法理解的版本）', PK, RED),
]), n); n += 1
put(legend('k5a.zh.jpg'), '原文图 5（上排）运动学：a 踝内翻/外翻角，b 髋屈/伸角，c 髋内旋/外旋角。贴扎后踝内翻角变小（a）；长贴的屈髋角更大（b）')
put(legend('k5d.zh.jpg'), '原文图 5（下排）：d 膝屈/伸角（负值＝屈曲），e 膝内收/外展角，f 膝内旋/外旋角。长贴组膝内收角更大（e），两种贴法膝内旋角都更大（f）')
put(legend('k7a.zh.jpg'), '原文图 7（上排）动力学：a 踝内翻/外翻力矩，b 踝外旋/内旋力矩，c 膝内收/外展力矩。注意 a：两种贴法的踝内翻力矩都明显高于不贴，与原文结论“长贴降低踝内翻力矩”相反')
put(legend('k7d.zh.jpg'), '原文图 7（下排）：d 膝内旋/外旋力矩，e 髋屈/伸力矩，f 髋内收/外展力矩（负值＝外展力矩）。f 中不贴组的外展力矩绝对值反而更大')
put(legend('k8.zh.jpg'), '原文图 8（上排）关节反作用力：a 踝，b 膝，c 髋（倍体重）。贴扎后踝关节反作用力峰值从约 3.6 倍体重降到约 2.2 倍体重；膝、髋没有差异')
c = k.op('x148.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .08)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
