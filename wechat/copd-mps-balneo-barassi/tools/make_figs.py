#!/usr/bin/env python3
"""Barassi 等 2026《温泉疗法与关键肌筋膜触发点手法治疗合并 COPD 的肌筋膜痛：病例系列》（Healthcare）推文配图。
原文是 CC BY 4.0（允许演绎和商业使用，需署名并注明改动）。原文图 1～7 都是治疗照片，图内只有 a/b/c 分图字母，
没有英文需要翻译，所以原图原样引用，中文说明放在图外的图注条里；首图、研究概况卡、一次治疗流程图、
10 名患者治疗前后对比图（按原文表 2 重画）、临床要点卡和封面为编者绘制。
用法：python3 make_figs.py <src 目录> <输出目录> <中文字体>"""
import re
import sys

from PIL import Image, ImageDraw, ImageFont

SRC, OUT, F = sys.argv[1:4]
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50); ORG = (215, 120, 20)
GRN = (0, 120, 60); PUR = (110, 70, 190)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (238, 232, 250)


def raw(name):
    return Image.open(f'{SRC}/{name}').convert('RGB')


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    # 英文单词、数字整体换行；标点不放行首
    for tok in re.findall(r"[A-Za-z0-9.%\-+]+|.", t):
        if line and dr.textlength(line + tok, font=font(fs)) > w and tok not in '，。；：、）”°':
            dr.text((x, y), line.rstrip(), font=font(fs), fill=fill); y += fs + gap; line = tok.lstrip()
        else: line += tok
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def capbox(im, cap, W=1200):
    """原图等比缩放后原样放在下方，中文图注放在图外上方的色条里"""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
    t.paste(im, (0, hh + 8)); return t


def blocks_at(dr, W, y, blocks):
    for h, t, c, a in blocks:
        top = y; dd = ImageDraw.Draw(Image.new('RGB', (W, 6000)))
        y2 = y + 62
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return y


def card(W, title, blocks):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 6000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    return im.crop((0, 0, W, blocks_at(dr, W, 100, blocks)))


def flow():
    """一次 BPM-ITC 治疗的先后顺序和时长"""
    W = 1200; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '一次治疗怎么走（编者根据原文方法整理）', font=font(36), fill='white')
    para(dr, 30, 100, '每周 5 次、共 4 周、20 次。每次开始先花约 5 分钟查体，在站、仰卧、俯卧位找出约 3 个关键触发点（KMTrP），'
         '后面每一站都要再按这几个点。各站加起来约 2.5 小时（编者按原文时长相加）。', 26, W - 60, fill=GREY)
    steps = [
        ('0', '饮用温泉水', '约 500 mL 碳酸氢盐-硫酸盐-碱土金属矿泉水，空腹 ≥6 小时后，带着小瓶边做后面的治疗边喝', '全程', LT, TEAL),
        ('1', '温泉水蒸汽吸入 20 分钟', '喷嘴距患者 50 cm，37～38 ℃、1.5 个大气压。\n前 10 分钟：治疗师站在身后按压触发点和呼吸相关肌（膈肌、胸小肌、肩胛提肌、星状神经节区），每点 30 秒～1 分钟，可加辅助静态牵伸。\n后 10 分钟：双手握棒前屈上举，吸 4 秒、用力呼 4 秒，做 1 分钟歇 1 分钟', '20 min', OR, ORG),
        ('2', '泥疗 + 浴疗 + 休息', '膨润土温泉泥敷在各大关节和触发点上 15 分钟 → 温泉水臭氧水疗浴 15 分钟 → 温暖环境休息 20 分钟，休息的前 10 分钟再按一遍触发点（隔着泥可用 T 形按摩棒）', '50 min', GR, GRN),
        ('3', '臭氧“血管通道”行走', '在 24 ℃ 和 38 ℃ 两个池子之间来回走，每分钟换一次池，池壁有 4～6 个大气压水柱冲击；边走边做不拿棒的上肢上举', '15 min', PU, PUR),
        ('4', '32.5 ℃ 温泉池水中再训练', '① 适应放松：漂浮 + 膈式呼吸、浮条托背钟摆、配合呼吸步行、持棒上举\n② 肌筋膜刺激：漂浮时按压触发点，被动活动脊柱和四肢\n③ 关节活动与本体感觉：扶杆屈伸下肢、浮条辅助动态自我牵伸、平衡板踝背屈\n④ 主动稳定：浮条辅助蹬车、侧向游泳', '60 min（4×15）', PK, RED),
    ]
    y = 220
    for n, h, t, d, c, a in steps:
        top = y; dd = ImageDraw.Draw(Image.new('RGB', (W, 3000)))
        y2 = y + 62
        for seg in t.split('\n'): y2 = para(dd, 110, y2, seg, 26, W - 160, gap=12)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.ellipse([36, top + 14, 88, top + 66], fill=a); dr.text((62, top + 40), n, font=font(30), fill='white', anchor='mm')
        dr.text((110, top + 18), h, font=font(32), fill=a)
        dr.text((W - 40, top + 22), d, font=font(26), fill=a, anchor='ra')
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 110, yy, seg, 26, W - 160, gap=12)
        y = y2 + 24
        if n != '4':
            dr.polygon([(W / 2 - 16, y - 18), (W / 2 + 16, y - 18), (W / 2, y - 4)], fill=(190, 190, 190))
    y = para(dr, 30, y + 4, '原文没写：手法每次具体做哪些点、按压力度；水中训练每个动作做几组几次；20 次里是否进阶。', 24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 10))


def results():
    """原文表 2：三项指标每人治疗前后"""
    data = [  # 编号, 性别, MRC 前后, NPRS 前后, BPQ 前后
        (1, '男', 3, 2, 10, 6, 52, 38), (2, '男', 3, 2, 10, 5, 80, 33), (3, '女', 2, 1, 8, 5, 42, 19),
        (4, '女', 2, 1, 9, 6, 44, 29), (5, '女', 3, 2, 9.5, 8, 41, 39), (6, '女', 2, 1, 8.5, 5, 48, 42),
        (7, '女', 2, 1, 6.5, 4.5, 30, 12), (8, '女', 3, 2, 6, 3, 20, 11), (9, '男', 2, 1, 6.5, 6, 27, 8),
        (10, '男', 2, 1, 10, 6, 40, 26)]
    W = 1200; im = Image.new('RGB', (W, 2000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), '10 名患者治疗前后（编者按原文表 2 重画）', font=font(36), fill='white')
    x0 = 30
    for c, t in ((GREY, '治疗前'), (TEAL, '4 周 20 次后')):
        dr.ellipse([x0, 108, x0 + 26, 134], fill=c); dr.text((x0 + 36, 102), t, font=font(26), fill=INK); x0 += 260
    dr.text((x0, 102), '三项都是分数越低越好', font=font(26), fill=GREY)
    panels = [('呼吸困难 MRC（0～4 级）', 2, 0, 4, 1), ('疼痛 NPRS（0～10）', 4, 0, 10, 2), ('生物-姿势问卷 BPQ（0～112）', 6, 0, 90, 30)]
    top, row = 230, 70; lab = 120; pw = (W - lab - 40) / 3
    bot = top + row * len(data)
    for k, (name, idx, vmin, vmax, step) in enumerate(panels):
        L = lab + k * pw + 34; R = L + pw - 68
        X = lambda v, L=L, R=R: L + (R - L) * (v - vmin) / (vmax - vmin)
        dr.text(((L + R) / 2, top - 60), name, font=font(24), fill=TEAL, anchor='ma')
        for v in range(vmin, vmax + 1, step):
            dr.line([X(v), top - 20, X(v), bot], fill=(235, 235, 235), width=1)
            dr.text((X(v), bot + 10), str(v), font=font(20), fill=GREY, anchor='ma')
        for i, d in enumerate(data):
            a, b = d[idx], d[idx + 1]; y = top + row * i + row / 2
            dr.line([X(a), y, X(b), y], fill=(150, 200, 210), width=8)
            dr.ellipse([X(a) - 10, y - 10, X(a) + 10, y + 10], fill=GREY)
            dr.ellipse([X(b) - 10, y - 10, X(b) + 10, y + 10], fill=TEAL)
    for i, d in enumerate(data):
        y = top + row * i + row / 2
        dr.text((lab - 10, y), f'{d[0]} 号 {d[1]}', font=font(24), fill=RED if d[0] in (5, 9) else INK, anchor='rm')
    y = bot + 60
    y = para(dr, 30, y, '均值：MRC 2.4 → 1.4；NPRS 8.4 → 5.4；BPQ 42.4 → 25.7（Wilcoxon 符号秩检验均 p<0.01）。'
             '10 人的 MRC 都正好降 1 级；疼痛降幅最小的是 9 号（0.5 分）和 5 号（1.5 分），5 号的 BPQ 也只降 2 分（编号标红）。', 24, W - 60, fill=GREY)
    y = para(dr, 30, y + 4, '只有治疗前后两次评估，没有对照组，也没有治疗结束后的随访。', 24, W - 60, fill=GREY)
    return im.crop((0, 0, W, y + 10))


# 1 首图
W, H = 1400, 720; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '病例系列 · 《Healthcare》2026', font=font(30), fill=TEAL)
dr.text((70, 125), '温泉疗法＋关键肌筋膜触发点手法', font=font(50), fill=INK)
dr.text((70, 195), '治疗 COPD 合并肌筋膜疼痛综合征', font=font(46), fill=INK)
dr.line([70, 300, W - 70, 300], fill=(200, 205, 210), width=2)
dr.text((70, 330), 'Barassi G, Panunzio M, Prosperi L, et al.', font=font(26), fill=GREY)
dr.text((70, 375), 'Healthcare. 2026;14(6):788. doi:10.3390/healthcare14060788', font=font(26), fill=GREY)
dr.text((70, 420), '意大利基耶蒂-佩斯卡拉大学 Ce.Fi.R.R. 物理治疗与康复中心', font=font(26), fill=GREY)
dr.text((70, 465), '卡斯泰尔诺沃德拉道尼亚温泉医学中心', font=font(26), fill=GREY)
dr.text((70, 600), '编者中文解读 · 原文 CC BY 4.0，图片引用未改动、中文图注为编者添加', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(card(1200, '研究概况（编者根据原文整理）', [
    ('谁', '10 名同时有中重度 COPD 和肌筋膜疼痛综合征（MPS）的患者，男 4、女 6，平均 69±7 岁（59～78 岁）。'
          'COPD 是外院诊断的，温泉中心的风湿科和康复科医生根据病史加“有触发点的局部及放射痛”确认合并 MPS', LT, TEAL),
    ('排除', '心衰或肾衰、重度高血压、重度血栓性静脉炎、风湿病急性期、免疫缺陷、开放伤口和溃疡、精神疾病、步行严重受限、活动性感染', PK, RED),
    ('做什么', 'BPM-ITC 温泉综合方案：饮用温泉水、蒸汽吸入、泥疗、冷热交替“血管通道”行走、温泉池水中训练，'
             '每一站都穿插关键触发点手法。每周 5 次，4 周共 20 次', OR, ORG),
    ('看什么', '治疗前后各一次：MRC 呼吸困难量表（0～4 级）、NPRS 疼痛评分（0～10）、生物-姿势问卷 BPQ（0～112 分，57 题，自填）\n'
             '数据从 2025 年 5～6 月的病历里回顾性提取，没有对照组，没有随访', GR, GRN),
]), 2)

save(flow(), 3)
save(capbox(raw('fig1.jpg'), '原文图 1  a：温泉水蒸汽吸入，喷嘴距患者 50 cm，治疗师同时用拇指按压右侧肩胛提肌的关键触发点；'
                              'b：配合呼吸节律的双手持棒上肢前屈上举'), 4)
save(capbox(raw('fig2.jpg'), '原文图 2  a：在各大关节上敷温泉泥，再敷到查体找到的触发点上；b：用工具隔泥处理左侧胸大肌触发点'), 5)
save(capbox(raw('fig3.jpg'), '原文图 3  臭氧“血管通道”：在冷（24 ℃）热（38 ℃）两池间来回走，边走边做上肢上举', W=900), 6)
save(capbox(raw('fig4.jpg'), '原文图 4  水中再训练第一阶段。a：浮条托住脊柱漂浮，配合膈式呼吸，之后做钟摆运动；b：水中持棒上肢上举'), 7)
save(capbox(raw('fig5.jpg'), '原文图 5  第二阶段。a：患者漂浮时用捏法处理左侧上斜方肌触发点；b：漂浮下被动活动右踝和右膝'), 8)
save(capbox(raw('fig6.jpg'), '原文图 6  第三阶段。a：扶杆下肢屈伸；b：浮条辅助的左侧髂腰肌和双侧胸大肌动态自我牵伸；c：站在平衡板上做踝背屈'), 9)
save(capbox(raw('fig7.jpg'), '原文图 7  第四阶段。a：浮条支撑下蹬车；b：手扶浮板的侧向游泳起始姿势'), 10)
save(results(), 11)

save(card(1200, '落到临床（编者整理）', [
    ('COPD 患者别忘了查肌肉', 'COPD 患者颈、胸、腰和膈肌周围的肌肉疼痛很常见，呼吸辅助肌长期过度工作。'
                         '查体时顺手摸一摸斜角肌、胸小肌、肩胛提肌、上斜方肌、胸大肌，有触发点就一起处理', LT, TEAL),
    ('能借用的“干货”', '没有温泉也能做：坐位按压呼吸辅助肌触发点每点 30 秒～1 分钟；持棒上举配合“吸 4 秒、呼 4 秒”，做 1 分钟歇 1 分钟；'
                    '温水池里的漂浮呼吸、扶杆下肢训练、浮条辅助牵伸', GR, GRN),
    ('不能替代肺康复', '这个方案没有和标准肺康复（耐力训练＋力量训练＋教育）比较过，也没测肺功能和 6 分钟步行。'
                    '温泉和手法最多算锦上添花', PK, RED),
    ('安全先筛查', '原文排除了心衰、重度高血压、血栓性静脉炎等；COPD 患者热水浸泡、38 ℃ 热池和吸入蒸汽前，要看血氧、心率、血压，'
                 '有低氧或近期急性加重的先别下水（编者补充）', OR, ORG),
    ('评估别只看量表', '建议同时记录肺功能、6 分钟步行、mMRC/CAT、压痛阈，并且随访治疗结束后能维持多久', PU, PUR),
]), 12)

# 封面：纯文字
W, H = 900, 383; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, H], fill=TEAL)
dr.text((50, 46), '病例系列 · Healthcare 2026', font=font(26), fill=TEAL)
dr.text((50, 118), '慢阻肺＋肌筋膜痛', font=font(58), fill=INK)
dr.text((50, 198), '泡温泉＋按触发点，管用吗？', font=font(46), fill=INK)
dr.text((50, 290), 'COPD · 触发点手法 · 温泉疗法 · 10 例', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
