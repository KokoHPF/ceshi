#!/usr/bin/env python3
"""蔡晓熙等 2026 ACL 重建术后姿势控制障碍：原文无图无表；首页标题区截图；按正文内容绘制“机制 → 康复”示意图；封面为文字设计图。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); RED = (171, 25, 66); BLUE = (40, 90, 160)

d = pymupdf.open(PDF)
pix = d[0].get_pixmap(dpi=200, clip=pymupdf.Rect(55, 55, 470, 258))
Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(f'{OUT}/img01.jpg', quality=88)

W, H = 1600, 1230
im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)


def ctext(cx, y, t, f, fill):
    for k, l in enumerate(t.split('\n')):
        dr.text((cx - dr.textlength(l, font=f) / 2, y + k * (f.size + 10)), l, font=f, fill=fill)


def box(x0, y0, x1, y1, title, body, col):
    dr.rounded_rectangle([x0, y0, x1, y1], 20, fill=col + (0,) if False else (255, 255, 255), outline=col, width=5)
    dr.rounded_rectangle([x0, y0, x1, y0 + 70], 20, fill=col)
    dr.rectangle([x0, y0 + 50, x1, y0 + 70], fill=col)
    ctext((x0 + x1) / 2, y0 + 14, title, font(38), 'white')
    ctext((x0 + x1) / 2, y0 + 92, body, font(30), INK)


def arrow(x0, y0, x1, y1, col=(120, 120, 120)):
    dr.line([x0, y0, x1, y1], fill=col, width=8)
    import math
    a = math.atan2(y1 - y0, x1 - x0); L = 28
    dr.polygon([(x1, y1), (x1 - L * math.cos(a - 0.45), y1 - L * math.sin(a - 0.45)), (x1 - L * math.cos(a + 0.45), y1 - L * math.sin(a + 0.45))], fill=col)


ctext(W / 2, 30, 'ACL 重建术后姿势控制障碍：机制与康复', font(54), INK)
ctext(W / 2, 110, '机　制', font(42), RED)
bw, bh = 340, 270; ys = 180; xs = [60, 440, 820, 1200]
M = [('外周感觉', '机械感受器缺失\n本体感觉下降\n（位置觉、运动觉）'),
     ('中枢调控', '脊髓 α 运动神经元\n兴奋性下降\n皮层重塑\n依赖视觉代偿'),
     ('神经肌肉', '股四头肌抑制\n双侧肌力不对称\n腘绳肌激活延迟\n过度共激活'),
     ('心理认知', '运动恐惧\n“恐惧-僵硬”\n恶性循环')]
for x, (t, b) in zip(xs, M):
    box(x, ys, x + bw, ys + bh, t, b, RED)
for i in range(3):
    arrow(xs[i] + bw + 4, ys + bh / 2, xs[i + 1] - 6, ys + bh / 2)
dr.rounded_rectangle([300, 530, 1300, 630], 50, fill=(250, 235, 238), outline=RED, width=4)
ctext(W / 2, 552, '静态 + 动态姿势控制障碍 → 再损伤风险约增加 1 倍', font(38), RED)
arrow(W / 2, ys + bh + 10, W / 2, 525)
arrow(W / 2, 640, W / 2, 715, BLUE)
ctext(W / 2, 722, '康　复', font(42), BLUE)
bw2, bh2 = 470, 290; ys2 = 790; xs2 = [60, 565, 1070]
R = [('本体感觉训练', '平衡训练\n（平衡系统、倒走）\n体感刺激\n（振动、水疗）'),
     ('运动学习干预', '外部注意力焦点\n认知双任务\n虚拟现实训练\n（经颅磁刺激）'),
     ('神经肌肉训练', '力量 + 灵敏\n增强式 + 近端控制\n★ 联合外部注意焦点\n或 VR 效果更好')]
for x, (t, b) in zip(xs2, R):
    box(x, ys2, x + bw2, ys2 + bh2, t, b, BLUE)
dr.text((60, H - 70), '按原文内容自绘示意图；尚缺针对运动恐惧和抗扰动的训练方法', font=font(28), fill=(120, 120, 120))
im.save(f'{OUT}/img02.jpg', quality=90)

cv = Image.new('RGB', (900, 383), (236, 242, 250)); dr = ImageDraw.Draw(cv)
dr.rectangle([0, 0, 900, 70], fill=BLUE)
dr.text((40, 14), '中华创伤杂志 2026 · 综述精读', font=font(34), fill='white')
dr.text((40, 105), 'ACL 重建术后', font=font(70), fill=INK)
dr.text((40, 200), '姿势控制障碍：机制与康复', font=font(56), fill=RED)
x = 40
for tg in ['本体感觉', '中枢重塑', '运动恐惧', '外部注意焦点', 'VR']:
    w = dr.textlength(tg, font=font(28)) + 28
    dr.rounded_rectangle([x, 305, x + w, 353], 22, fill='white', outline=BLUE, width=2)
    dr.text((x + 14, 313), tg, font=font(28), fill=BLUE); x += w + 14
cv.save(f'{OUT}/cover.jpg', quality=92)
