#!/usr/bin/env python3
"""Vagy 等 2025 攀岩运动员 ACL 重建术后康复与重返运动：首图中文标题卡；六期总览、坠落悬挂评分卡、先锋坠落评分卡、
进阶标准一览为编者绘制；原文图 1～8 加中文标注。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); YL = (253, 246, 220); PU = (238, 232, 246)
doc = pymupdf.open(PDF)
X = {1: 311, 2: 344, 3: 389, 4: 417, 5: 420, 6: 455, 7: 452, 8: 539}
raw = lambda n: Image.open(BytesIO(doc.extract_image(X[n])['image'])).convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=86)


def titled(im, t, W=None):
    W = W or im.width
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def tile(n, cap, W=1200, maxh=1300):
    im = raw(n); im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    if im.height > maxh: im = im.resize((round(im.width * maxh / im.height), maxh), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in f'图 {n}　{cap}':
        if d0.textlength(line + ch, font=font(28)) > W - 30: lines.append(line); line = ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, ((W - im.width) // 2, hh + 8)); return t


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '方法学论文 · 《运动与积极生活前沿》2025', font=font(32), fill=TEAL)
for i, t in enumerate(['攀岩者 ACL 重建后：', '六期康复 + 攀岩专项回场测试']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '勾脚、高抬脚、落膝 · 坠落悬挂测试 · 先锋坠落测试', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Vagy J, Schöffl V, Ohde J, Petersen W, Lutter C. Front Sports Act Living 2025;7:1580509', font=font(28), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 六期总览 ----------
W = 1400; im = Image.new('RGB', (W, 3200), 'white'); dr = ImageDraw.Draw(im)
ph = [('第 1 期 术后早期', '0～4 周', LT, ['消肿止痛、步态、本体感觉；胫股和髌股关节松动', '尽早改善踝背伸、髋屈曲和外展活动度', '坐位或仰卧位练握力；伤口愈合后才挂指力板'],
       '主动伸膝到 0°；被动屈膝到 90°'),
      ('第 2 期 术后后期', '4～8 周', GR, ['练伸膝肌、屈膝肌、小腿、髋外展和伸髋肌', '引体向上、屈肘 90° 悬挂（脚不离地的高度）', '勾脚相关的腘绳肌训练（无禁忌时）；高抬脚从 10 cm 开始'],
       '积液 ≤1+；屈膝主动活动度达健侧 90%；单腿平衡练 2 周；伸膝、屈膝、髋外展等长肌力 > 健侧 70%；高抬脚上拉 0.5 m × 10 次；一步跨两级上 6 层楼；改良 Grant 抬脚 80%'),
      ('第 3 期 早期强化', '8～16 周', OR, ['继续加强下肢力量', '术后至少 12 周：顶绳攀爬，难度比自己顶绳水平低 3 级（如 8 级 → 6 级），建议戴铰链护膝'],
       '等长肌力达健侧 80%；单腿蹲到屈膝 60° 次数对称性 ≥80%、动作控制好；Y 平衡前向和后内向两侧差 ≤4 cm'),
      ('第 4 期 后期强化', '16～24 周', YL, ['悬吊带和四点跪闭链练习，模拟攀岩动作', '学习坠落技术；初级落地和增强式训练（坠落悬挂 10 cm → 0.5 m）', '离地 ≤0.5 m 的抱石横移（戴铰链护膝）；顶绳难度提高到低 2 级'],
       '心理准备量表 ≥56 分；坠落悬挂测试 90%；先锋坠落测试 100%；4 项单腿跳对称性 85%；等长肌力和单腿腿举达健侧 85%'),
      ('第 5 期 重返运动', '24～36 周', PK, ['先锋攀爬：比顶绳水平低 3 级；抱石：比自己水平低 2 级（如 V8 → V6），只爬不会掉的线路', '落膝训练；在顶绳保护下练勾脚、高抬脚、落膝', '落地训练继续进阶：高度、支撑面、躯干姿势、落地面'],
       '术后至少 9 个月；心理准备量表 ≥75 分；单腿跳对称性 ≥90%；等长肌力和单腿腿举 ≥90%；每周至少 3 次力量或增强式训练；能在攀爬中完成勾脚、高抬脚、落膝'),
      ('第 6 期 重返竞技', '36 周以后', PU, ['高难度落地和增强式训练', '比赛和“项目”先锋攀爬', '比赛和项目抱石至少 12 个月后；12 个月内不爬超过 3 米的抱石线路', '建议术后持续做康复训练至 3 年'], '')]
y = 20
for t, w, bg, items, ms in ph:
    for draw_pass in (0, 1):
        if draw_pass: dr.rounded_rectangle([20, y, W - 20, y + h], 16, fill=bg)
        tgt = dr if draw_pass else ImageDraw.Draw(Image.new('RGB', (W, 3200)))
        tgt.text((50, y + 18), t, font=font(38), fill=TEAL); tgt.text((480, y + 24), w, font=font(32), fill=RED)
        yy = y + 82
        for it in items: yy = para(tgt, 60, yy, '· ' + it, 27, 1290, INK, 6) + 6
        if ms: yy = para(tgt, 60, yy + 6, '进入下期：' + ms, 26, 1290, (40, 110, 60), 6)
        h = yy - y + 16
    y += h + 20
im = im.crop((0, 0, W, y))
save(titled(im, '六期总览（编者根据原文表 1 整理）'), 2)

# ---------- 原文图 ----------
save(board([tile(1, '勾脚的腘绳肌进阶：A 攀岩中的勾脚；B、C 屈髋位小范围屈膝；D、E 俯卧负重全范围屈膝；F、G 双腿臀桥 + 滑板屈膝；H、I 单腿臀桥 + 弹力带屈膝'),
            tile(2, '高抬脚进阶：A 攀岩中的高抬脚；B、C 起始屈髋屈膝 90° 的高抬脚上拉（手拉悬吊带或便携指力板）；D、E 起始屈髋屈膝更大')], '第 2 期：勾脚与高抬脚'), 3)
save(board([tile(3, '改良 Grant 抬脚测试：离墙 23 cm，双手撑墙略宽于肩，脚沿墙滑起到最大屈髋，量高度，两侧应达最大高度的 80%（原文图注误写为“落膝进阶练习”）')], '第 2 期过关测试：改良 Grant 抬脚'), 4)
save(board([tile(4, '模拟攀岩的闭链练习：A、B 悬吊带平板支撑 + 下肢动作；C、D 熊爬姿势 + 下肢动作（类似攀岩的对侧手脚交叉）'),
            tile(5, '坠落悬挂训练与测试：从单杠或吊环松手，落地成屈膝 90° 下蹲，再向后滚')], '第 4 期：闭链练习与落地训练'), 5)
save(board([tile(6, '向后坠落：放松 → 屈膝屈肘 → 收手臂 → 向后滚'),
            tile(7, '侧向坠落：看落地区 → 屈膝屈肘 → 收手臂 → 让垫子吸收冲击；不要锁膝，不要用手撑地')], '第 4 期：学会怎么掉下来'), 6)
save(board([tile(8, '落膝进阶：A 攀岩中的落膝；B～E 坐地髋内旋练习；F、G 站立落膝；H、I 一只脚放在垫高物上的站立落膝')], '第 5 期：落膝训练'), 7)

# ---------- 坠落悬挂评分 ----------
W, H = 1400, 1000; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.text((40, 20), '离垫子 0.5 米，从单杠或吊环松手，每级落 5 次，穿攀岩鞋', font=font(30), fill=TEAL)
for i, (lv, t) in enumerate([('第 1 级', '双脚平行站位落地'), ('第 2 级', '手术腿在前、健腿在后'), ('第 3 级', '健腿在前、手术腿在后')]):
    x = 30 + i * 455
    dr.rounded_rectangle([x, 80, x + 430, 230], 14, fill=[LT, OR, PK][i])
    ctext(dr, x + 215, 100, lv, font(36), TEAL); ctext(dr, x + 215, 160, t, font(28), INK)
dr.text((40, 260), '每次落地，以下每项做到得 1 分（4 项 × 5 次 = 20 分）', font=font(30), fill=TEAL)
for i, t in enumerate(['屈膝角度 ≥90°', '无动态膝外翻（髌骨不落到大脚趾内侧）', '脚的落点和朝向正确', '落地后向后滚，缓冲冲击']):
    y = 320 + i * 90
    dr.rounded_rectangle([40, y, W - 40, y + 72], 12, fill=(245, 245, 245))
    dr.text((70, y + 18), t, font=font(32), fill=INK); dr.text((W - 200, y + 18), '1 / 0', font=font(32), fill=RED)
dr.rounded_rectangle([40, 700, W - 40, 840], 14, fill=GR)
para(dr, 70, 720, f'每级至少 18 / 20 分（90%）才能进入下一级。测试前应先能从 0.5 米的箱子上以多种脚位、下蹲姿势轻松落地', 30, 1260, INK)
para(dr, 40, 870, '前提：心理准备量表 ≥56 分', 28, 1300, GREY)
save(titled(im, '坠落悬挂测试：能不能安全地从抱石上掉下来'), 8)

# ---------- 先锋坠落评分 ----------
W, H = 1400, 860; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
para(dr, 40, 20, '需要先锋线路和保护员。先在仰角线路上练：最后一把快挂在髋 → 膝 → 脚的高度时挂绳并坠落；安全后再练垂直或微仰角的摆荡坠落', 28, 1320, TEAL)
dr.text((40, 150), '每项做到得 4 分（5 项 × 4 = 20 分），必须 20 / 20 才通过', font=font(30), fill=RED)
for i, t in enumerate(['屈膝角度 ≥60°', '屈髋角度 ≥60°', '会判断坠落区，技术和安全意识到位', '绳子保持在身体和岩壁之间', '松手时呼气，身体放松']):
    y = 220 + i * 100
    dr.rounded_rectangle([40, y, W - 40, y + 80], 12, fill=(245, 245, 245))
    dr.text((70, y + 22), t, font=font(32), fill=INK); dr.text((W - 200, y + 22), '4 / 0', font=font(32), fill=RED)
para(dr, 40, 740, '有其他既往损伤时，可适当放宽', 28, 1300, GREY)
save(titled(im, '先锋坠落测试：能不能安全地冲坠和撞墙'), 9)

# 封面
c = raw(1); c = c.resize((900, round(c.height * 900 / c.width))); c.crop((0, 0, 900, 383)).save(f'{OUT}/cover.jpg', quality=90)
print('ok')
