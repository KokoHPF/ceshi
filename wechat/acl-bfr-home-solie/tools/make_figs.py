#!/usr/bin/env python3
"""Solie 等 2023 诊所 + 居家血流限制训练（ACL 重建术后）病例报告：首图为原题直译标题卡；时间线卡、BFR 参数卡和两张数据图为编者根据原文正文、表 1 和表 2 整理；
原文图 1～5 直接使用（原文已遮挡面部）并加中文说明。
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


F1, F2, F3, F4, F5 = raw(102), raw(151), raw(180), raw(220), raw(221)
BLUE = (40, 90, 170)

# 首图
W, H = 1400, 700; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '病例报告 · Healthcare 2023', font=font(32), fill=TEAL)
for i, t in enumerate(['诊所与居家血流限制训练改善骨-髌腱-骨', '自体移植 ACL 重建术后大腿肌肉萎缩：', '病例报告']):
    dr.text((70, 130 + i * 70), t, font=font(48), fill=INK)
line, y = '', 360
for w in 'Clinic and Home-Based Exercise with Blood Flow Restriction Resolves Thigh Muscle Atrophy after Anterior Cruciate Ligament Reconstruction with the Bone-Patellar Tendon-Bone Autograft: A Case Report'.split():
    if dr.textlength(line + ' ' + w, font=font(26)) > W - 140: dr.text((70, y), line, font=font(26), fill=GREY); y += 36; line = w
    else: line = (line + ' ' + w).strip()
dr.text((70, y), line, font=font(26), fill=GREY)
dr.line([70, 500, W - 70, 500], fill=(200, 205, 210), width=2)
dr.text((70, 530), 'Solie BS, Eggleston GG, Schwery NA, Doney CP, Kiely MT, Larson CM.', font=font(28), fill=GREY)
dr.text((70, 572), 'Healthcare 2023;11(13):1885. doi:10.3390/healthcare11131885', font=font(28), fill=GREY)
dr.text((70, 630), '编者中文重排，仅作学术交流（原文 CC BY 4.0）', font=font(26), fill=(150, 150, 150))
save(im, 1)

save(titled(capbox(F1, '横轴为术后周数，纵轴为外部负荷和训练强度。蓝色：关节活动度和股四头肌激活（第 0～7 周）；红色：诊所 + 居家血流限制训练；黄色：股四头肌 / 髌腱等长和等张训练。左上为改良疼痛监测量表：每周疼痛和肿胀不应增加，训练中和训练后疼痛可到 3～5/10'),
            '原文图 1　16 周诊所 + 居家康复总览'), 2)

phases('康复时间线（编者根据原文正文和表 1 整理）', [
    ('术前（受伤后第 0～22 天）', (240, 240, 240), INK, ['门诊康复 4 次：宣教、居家训练、消肿、恢复活动度、激活股四头肌',
        '术前达标：积液降到 trace/1+；伸膝（含过伸）与健侧相同；屈膝 ≥ 120°；直腿抬高无伸膝迟滞']),
    ('术后 0～2 周　保护 + 激活', LT, TEAL, ['屈膝限制 0～90°（2 周）；伸膝位负重随耐受（6 周）；双拐 + 铰链支具 4 周，之后 2 周撤拐',
        '诊所每周 2 次（45 分钟 + 15 分钟电刺激）；居家每天 5～6 次（表 1 写 5 次）',
        '股四头肌 45 秒持续等长收缩、节拍器股四头肌收缩（60～95 次/分）、居家电刺激每天 2 次',
        '开链股四头肌训练只用小腿自重、限 0～90°，持续 4 周']),
    ('术后 1～2 周起　诊所 BFR', PK, RED, ['弹力带或主动活动度练习起步，每次累计加压 20～30 分钟（4～6 组 × 每组 3～5 分钟）',
        '股四头肌每周 8 组（第 2～4 周）→ 12 组以上（第 5 周起）']),
    ('术后 3～4 周起　居家 pBFR', OR, (180, 90, 20), ['每天 2 次，每次 6 组做到力竭，组间完全松开',
        '拐杖股四头肌收缩、俯卧屈膝、坐位伸膝；第 11 周后换成分腿蹲、站立屈膝、坐位伸膝']),
    ('术后 5～7 周起　加负荷', PU, (90, 60, 150), ['自重和渐进抗阻练习，每组做到力竭',
        '诊所伸膝器械 30～40 RM → 20～30 RM → 15～30 RM；单腿腿举、站立屈膝器械']),
    ('术后 6～7 周起　髌腱让步等长', GR, (40, 120, 60), ['窄距双腿深蹲等长，每天 2 次、间隔 6～8 小时，3 组 × 45 秒',
        '第 7～8 周加前脚垫高分腿蹲等长；之后进阶到分腿蹲和靠墙静蹲；腱痛加重就减小深度']),
    ('16 周以后', LT, TEAL, ['继续诊所和居家康复，加入小组体能训练', '2022 年 8 月重返足球；2022 年 9 月 28 日恢复伤前水平、无限制比赛'])], 3)

save(titled(capbox(F2, 'a 拐杖股四头肌收缩：坐位，弹力带一端系在拐杖上、另一端套在膝后，收缩股四头肌把膝向后压直，是闭链训练的最低起点；b 主观紧绷感评分（RPT）：7/10 为中等压力但不痛，10/10 为强烈压力伴疼痛；c 居家用的 RockCuff 绑带（5 厘米宽）'),
            '原文图 2　居家“实用型”血流限制（pBFR）'), 4)

phases('诊所 BFR 与居家 pBFR 怎么设（编者根据原文 2.3.4～2.3.5 整理）', [
    ('诊所 BFR（术后 1～2 周起）', PK, RED, ['设备：Delphi 个体化止血带系统，10 cm 宽袖带，绑在大腿最近端',
        '压力：先用 180 mmHg，2 次治疗内按 RPT 调到 7～8/10，即 210 mmHg，之后一直用这个压力',
        '剂量：每次累计加压 20～30 分钟；第 5～7 周起每组做到力竭']),
    ('居家 pBFR（术后 3～4 周起）', OR, (180, 90, 20), ['设备：5 cm 宽无弹性 RockCuff，旋钮绳扣收紧，家长自费购买',
        '压力：训练前收紧到 RPT 7～8/10，组间完全松开',
        '剂量：每天 2 次，每次 6 组做到力竭，目标累计加压 20～30 分钟']),
    ('安全检查', LT, TEAL, ['开始前做风险分层：仅因近期关节镜手术判为低到中等风险；运动员和家长同意',
        '充气后用血管多普勒在胫后动脉确认静息血流仍在',
        '大脚趾毛细血管再充盈 < 3 秒，间接说明没有完全阻断；居家训练由运动员自己查',
        '依从性：只靠口头确认，每周在诊所检查一次绑带和动作'])], 5)

save(titled(capbox(F3, 'a 血管多普勒确认加压时胫后动脉仍有血流；b 大腿围度在髌骨上极上方 15 cm 处测量；c～e 按压大脚趾后观察颜色恢复，毛细血管再充盈 < 3 秒提示动脉没有被完全阻断'),
            '原文图 3　动脉血流评估和大腿围度测量'), 6)

# 编者重绘：围度差和积液
wk = [0, 4, 6, 9, 12, 16]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=100)
a1.plot(wk, [-0.5, -1.5, 0, 1.5, 1.25, 2.25], 'o-', color='#b42832', lw=3, label='大腿围度差')
a1.plot(wk, [-0.25, -0.25, -0.25, 0.75, 0.75, 1], 's-', color='#2c5aa0', lw=3, label='小腿围度差')
a1.axhline(0, color='grey', lw=1)
for x, v in zip(wk, [-0.5, -1.5, 0, 1.5, 1.25, 2.25]): a1.annotate(f'{v:+g}' if v else '0', (x, v), textcoords='offset points', xytext=(0, 10 if v >= 0 else -24), ha='center', fontsize=12, color='#b42832')
a1.set_xticks(wk); a1.set_xlabel('术后周数', fontsize=13); a1.set_ylabel('术侧 - 健侧（cm）', fontsize=13); a1.set_title('围度差（术侧减健侧）', fontsize=15)
a1.legend(frameon=False, fontsize=12); a1.set_ylim(-2.2, 3)
eff = [3, 3, 2, 1, 1, 0.5]
a2.bar(range(6), eff, color=['#b42832' if e >= 2 else '#e8a33d' if e >= 1 else '#6aa36f' for e in eff])
for i, t in enumerate(['3+', '3+', '2+', '1+', '1+', 'trace']): a2.text(i, eff[i] + 0.08, t, ha='center', fontsize=13)
a2.set_xticks(range(6)); a2.set_xticklabels([str(w) for w in wk]); a2.set_xlabel('术后周数', fontsize=13); a2.set_yticks([0, 1, 2, 3]); a2.set_yticklabels(['0', '1+', '2+', '3+'])
a2.set_ylim(0, 3.5); a2.set_title('术侧膝关节积液（擦拭试验）', fontsize=15)
for a in (a1, a2):
    a.spines[['top', 'right']].set_visible(False); a.tick_params(labelsize=12)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(capbox(Image.open(buf).convert('RGB'), '数据来自原文表 2。第 9 周起术侧大腿围度超过健侧，但同一时期积液仍有 1+，小腿围度也多了 1 cm；围度增加不能全部算成肌肉'),
            '编者重绘　大腿 / 小腿围度差和积液变化'), 7)

# 编者重绘：股四头肌力量
fig, ax = plt.subplots(figsize=(12, 5), dpi=100)
x = [0, 1]; w = 0.36
b1 = ax.bar([i - w / 2 for i in x], [70, 87], w, color='#b42832', label='术侧')
b2 = ax.bar([i + w / 2 for i in x], [96, 135], w, color='#2c5aa0', label='健侧')
for b in list(b1) + list(b2): ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 2, f'{b.get_height():g}%', ha='center', fontsize=14)
ax.set_xticks(x); ax.set_xticklabels(['第 12 周（LSI 73%）', '第 16 周（LSI 66%）'], fontsize=15)
ax.set_ylabel('股四头肌力量 / 体重（%）', fontsize=13); ax.set_ylim(0, 155); ax.legend(frameon=False, fontsize=13)
ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=12)
fig.tight_layout(); buf = BytesIO(); fig.savefig(buf, format='png'); plt.close(fig)
save(titled(capbox(Image.open(buf).convert('RGB'), '数据来自原文表 2（Biodex 等长测试）。术侧 4 周里涨了 17 个百分点，但健侧涨得更多，肢体对称指数（LSI）反而从 73% 降到 66%；正文把第 16 周术侧写成 86%，表 2 是 87%'),
            '编者重绘　股四头肌力量：围度追上了，力量没追上'), 8)

save(titled(capbox(F4, '术后 16 周正面（a）和背面（b）。星号为术侧（左腿）。原文称客观测量确认大腿肌肉萎缩已经消除'),
            '原文图 4　术后 16 周双下肢外观'), 9)
save(titled(capbox(F5, '以健侧第 0 周大腿围度为 0 点。红线为术侧，蓝线为健侧：术侧第 4 周最低（−1.5 cm），第 6 周追平，第 16 周比基线多 4.25 cm；健侧同期也多了 2 cm'),
            '原文图 5　大腿围度变化（Δ）'), 10)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), 'ACL 重建 · 血流限制训练 · 病例报告', font=font(34), fill=TEAL)
dr.text((50, 128), '一天两次 BFR，', font=font(62), fill=INK)
dr.text((50, 218), '16 周大腿追回来了', font=font(62), fill=INK)
dr.text((50, 318), '诊所 BFR + 居家 pBFR · 剂量 · 安全检查', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
