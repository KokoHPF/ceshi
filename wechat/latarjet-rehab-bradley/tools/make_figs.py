#!/usr/bin/env python3
"""Bradley 等 2021《Latarjet 术治疗运动员肩前向不稳：康复要点》（IJSPT）推文配图。
首图中文标题卡、原文图 1～8（含图中英文的图 1、3、4 先用 tools/fig-translate 译成中文）、附录 1 进阶标准流程卡、临床要点卡、封面。
用法：python3 make_figs.py <论文.pdf> <work 目录> <输出目录> <中文字体>
work 目录需要：zh_p3_1.png、zh_p4_2.png、zh_p5_1.png（figtrans render 输出，300 dpi）"""
import io
import sys

import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, WORK, OUT, F = sys.argv[1:5]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)
op = lambda n: Image.open(f'{WORK}/{n}').convert('RGB')
doc = pymupdf.open(PDF)
# 原文照片都是内嵌 JPEG，按 xref 直接取原始像素
XREF = {1: 53, 2: 62, 3: 63, 4: 69, 5: 70, 6: 80, 7: 81, 8: 86}


def raw(n):
    pix = pymupdf.Pixmap(doc, XREF[n])
    if pix.n > 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')


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


def card(W, title, blocks, arrows=False):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列；arrows=True 时块之间画向下箭头"""
    im = Image.new('RGB', (W, 6000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for k, (h, t, c, a) in enumerate(blocks):
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 6000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
        if arrows and k < len(blocks) - 1:
            cx = W // 2; dr.polygon([(cx - 22, y - 12), (cx + 22, y - 12), (cx, y + 14)], fill=(150, 150, 150)); y += 30
    return im.crop((0, 0, W, y))


def trim(im, pad=12):
    """裁掉四周白边"""
    g = im.convert('L').point(lambda v: 255 if v < 245 else 0); x0, y0, x1, y1 = g.getbbox()
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def stack(ims, W=1200, gap=16):
    ims = [i.resize((W, round(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    t = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: t.paste(i, (0, y)); y += i.height + gap
    return t


# 1 首图
W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '临床述评 · 《International Journal of Sports Physical Therapy》2021', font=font(30), fill=TEAL)
dr.text((70, 135), 'Latarjet 术治疗运动员肩前向不稳', font=font(58), fill=INK)
dr.text((70, 210), '康复要点：五阶段、按标准进阶', font=font(44), fill=INK)
dr.line([70, 315, W - 70, 315], fill=(200, 205, 210), width=2)
dr.text((70, 345), 'Bradley H, Lacheta L, Goldenberg BT, Rosenberg SI, Provencher MT, Millett PJ.', font=font(26), fill=GREY)
dr.text((70, 390), 'Int J Sports Phys Ther. 2021;16(1):259-269. doi:10.26603/001c.18707', font=font(28), fill=GREY)
dr.text((70, 435), '美国 Howard Head 运动医学中心、Steadman Philippon 研究所', font=font(26), fill=GREY)
dr.text((70, 535), '编者中文解读，仅作非商业学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(capbox(trim(op('zh_p3_1.png')), '原文图 1（图中英文由编者译为中文）  右肩三角肌胸大肌入路：在肩胛下肌下 1/3 劈开进入，'
            '把喙突尖连同联合腱一起截下，移到关节盂前下缘，联合腱从肩胛下肌劈开处穿出'), 2)
save(capbox(raw(2), '原文图 2  关节位置觉训练：仰卧闭眼，先主动把健侧手臂摆到一个位置，再让患侧尽量摆到同样的位置'), 3)
save(capbox(trim(op('zh_p4_2.png')), '原文图 3（图中英文由编者译为中文）  靠墙滑动（泡沫轴），用来激活前锯肌'), 4)
save(capbox(trim(op('zh_p5_1.png')), '原文图 4（图中英文由编者译为中文）  抗阻 PNF D2 模式：对角线、螺旋形、越过身体中线的动作'), 5)
save(capbox(raw(5), '原文图 5  四点跪位节律稳定：右上肢放在瑞士球上，处于过顶闭链位，治疗师施加扰动'), 6)
save(capbox(raw(6), '原文图 6A、6B  推拉臂缆绳训练：一侧推、一侧拉，带动整条动力链'), 7)
f7 = capbox(raw(7), '原文图 7  90/90 拍墙（开链）')
f8 = capbox(raw(8), '原文图 8  普拉提床上的上肢增强式跳跃：(A) 起始 (B) 结束')
save(stack([f7, f8], gap=30), 8)

save(card(1200, '各阶段进阶标准（编者译自原文附录 1）', [
    ('阶段 I 保护期 → 进入 II', '静息疼痛 < 3/10；QuickDASH < 60%\n被动活动度：前屈 120°、盂肱外展 90°、外旋 30°\n'
     '能主动完成肩胛后缩、前伸、下沉、上提', LT, TEAL),
    ('阶段 II 耐力期 → 进入 III（且术后 ≥ 6 周）', '主动活动时疼痛 < 3/10；QuickDASH < 40%\n主动活动度：前屈 120°、外展 120°、外旋 45°\n'
     '疲劳测试：肩胛面上举 90°、外展 90°、侧卧外旋到中立位，各等长保持或重复 20 次，看质量和数量\n'
     '肩胛运动障碍测试（不负重）正常；90° 以下关节角度复现误差 ≤ 3°\n同时评估下肢 Y 平衡', OR, (200, 120, 0)),
    ('阶段 III 力量期 → 出院或进入 IV', '临床检查无恐惧感；QuickDASH < 20%\n主动活动度 > 健侧 90%；总旋转弧达健侧 90%\n'
     '徒手肌力 4/5 或测力计 > 健侧 80%\n90° 以上关节角度复现误差 ≤ 3°；肩胛运动障碍测试（负重）正常\n完成运动员恐惧回避问卷（AFAQ）；做 FMS\n'
     '不需要爆发力动作 → 带维持方案出院\n需要 → 徒手肌力 5/5 或测力计 > 健侧 90%，ER90/IR90 > 70%，进入阶段 IV', GR, (0, 120, 60)),
    ('阶段 IV 爆发力期 → 进入 V', '按项目挑测试：CKCUEST > 21 次；上肢 Y 平衡两侧差 < 4 cm；改良俯卧撑 男 > 18、女 > 12；单臂坐位推球达常模或 > 健侧 90%\n'
     '过顶运动员另加：KJOC > 90；90/90 拍墙测试；俯卧落球测试；改良引体向上 男 > 12、女 > 4', PU, (110, 70, 190)),
    ('阶段 V 重返赛场 → 无限制参赛', '完成专项技术训练、训练课和比赛强度训练；过顶运动员完成间歇投掷方案', PK, RED),
], arrows=True), 9)

save(card(1200, '落到临床（编者整理）', [
    ('前 3 周护住两处', '外旋 < 30°，护肩胛下肌劈开和关节囊修复；前 2 周不做等长，'
     '也别做抗阻屈肘、前臂旋后，联合腱会把喙突骨块往下拉', PK, RED),
    ('按标准进阶，不只看时间', '每个阶段都有疼痛、QuickDASH、活动度、肌力和神经肌肉控制的门槛；力量期至少等到术后 6 周', LT, TEAL),
    ('外旋和肩胛下肌是重点', '外旋恢复慢但必须练满；腹压试验单独看肩胛下肌力量', OR, (200, 120, 0)),
    ('心理准备也要测', 'AFAQ 找出恐惧回避，必要时转运动心理', PU, (110, 70, 190)),
    ('重返前分项目测', '非过顶项目看闭链稳定和耐力；过顶项目加开链爆发力、KJOC 和至少 6 周增强式训练后的间歇投掷', GR, (0, 120, 60)),
]), 10)

# 封面：原文图 6A（推拉臂缆绳）
c = raw(6); x0 = round(c.width * 0.03); w = c.width // 2 - x0; h = round(w * 383 / 900); y0 = round(c.height * 0.18)
c.crop((x0, y0, x0 + w, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
