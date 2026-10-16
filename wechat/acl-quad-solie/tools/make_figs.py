#!/usr/bin/env python3
"""Solie 2024：图 2、3、4、5a、7 按原图数据中文重绘；图 8 流程图原图上逐框替换为中文、底部负荷进阶标准重画；
图 1、5b 解剖标注改为中文；图 10～12 背景墙/器械上的英文字样抹除或模糊；封面取自图 12。
用法：python3 make_figs.py <素材目录（x01～x13.png、title.png）> <输出目录>"""
import sys
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
RED = (171, 25, 66); INK = (25, 25, 25)
font = lambda s: ImageFont.truetype(F, s)
X = lambda i: Image.open(f'{SRC}/x{i:02d}.png').convert('RGB')


def badge(im, t):
    d = ImageDraw.Draw(im); f = font(max(26, min(46, im.height // 18)))
    w = d.textlength(t, font=f) + 24; h = f.size + 16
    x = im.width - w - 10; y = im.height - h - 10
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=RED)
    d.text((x + 12, y + 7), t, font=f, fill='white')
    return im


def save(im, name, W=1080):
    if im.width != W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}', quality=88)
    return im


def fig2pil(fig):
    fig.canvas.draw()
    im = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[..., :3].copy()); plt.close(fig)
    c = Image.new('RGB', (im.width, im.height + 64), 'white'); c.paste(im, (0, 0))
    return c


def inpaint(im, boxes, dark=True, thr=110):
    a = np.array(im); g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY); m = np.zeros(g.shape, np.uint8)
    for x0, y0, x1, y1 in boxes:
        sub = g[y0:y1, x0:x1]
        m[y0:y1, x0:x1] = 255 if dark is None else ((sub < thr) if dark else (sub > thr)).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((5, 5), np.uint8), 2)
    return Image.fromarray(cv2.inpaint(a, m, 5, cv2.INPAINT_TELEA))


def label(d, xy, t, fs, fill='white', stroke='black', sw=3):
    d.text(xy, t, font=font(fs), fill=fill, stroke_width=sw, stroke_fill=stroke)


def blur(im, boxes, r=14):
    for b in boxes:
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r)), b[:2])
    return im


Image.open(f'{SRC}/title.png').convert('RGB').save(f'{OUT}/img01.jpg', quality=88)

# ---------- 图 1：股四头肌解剖 ----------
im = X(1); d = ImageDraw.Draw(im)
for b in [(22, 56, 92, 100), (274, 56, 330, 100), (493, 56, 568, 100), (731, 56, 793, 100)]:
    d.rectangle(b, fill='black')
for x, t in [(18, '股外侧肌'), (262, '股中间肌'), (478, '股内侧肌'), (676, '股直肌')]:
    d.text((x, 10), t, font=font(38), fill='white')
im = inpaint(im, [(1148, 128, 1238, 178), (1678, 34, 1758, 82), (1912, 498, 1982, 544), (1798, 698, 1868, 748)], dark=None)
d = ImageDraw.Draw(im)
for xy, t in [((1116, 128), '股内侧肌'), ((1660, 32), '股四头肌腱'), ((1910, 498), '髌腱'), ((1790, 700), '胫骨粗隆')]:
    label(d, xy, t, 38, fill=INK, stroke='white')
save(badge(im, '图1'), 'img02.jpg')

# ---------- 图 2：各肌群平均失活率 ----------
fig, ax = plt.subplots(figsize=(10.8, 6.4), dpi=100)
names = ['伸膝肌群', '屈肘肌群', '跖屈肌群', '背屈肌群']; vals = [15.4, 5.1, 5.1, 1.2]
cols = ['#e8242a', '#18a84a', '#f7c500', '#3c6fc4']
bars = ax.bar(names, vals, color=cols, edgecolor='black', linewidth=1.5, width=.6)
for bb, v in zip(bars, vals):
    ax.text(bb.get_x() + bb.get_width() / 2, v + .3, f'约 {v:g}%', ha='center', fontsize=15)
ax.set_ylim(0, 18); ax.set_yticks(range(0, 19, 2)); ax.tick_params(labelsize=15)
ax.set_ylabel('平均失活率（%）', fontsize=17); ax.set_xlabel('肌群', fontsize=17)
ax.spines[['top', 'right']].set_visible(False)
ax.set_title('最大随意收缩时各肌群的平均失活率', fontsize=19, fontweight='bold', pad=14)
fig.tight_layout(); save(badge(fig2pil(fig), '图2'), 'img03.jpg')

# ---------- 图 3：长度-张力关系 ----------
fig, axs = plt.subplots(2, 2, figsize=(10.8, 8.6), dpi=100)
LT = np.array([[.5, 0], [1.3, 85], [2.0, 100], [2.25, 100], [4.0, 0]])
lt = lambda x: np.interp(x, LT[:, 0], LT[:, 1])
spec = [('股直肌', '#18a84a', 1.15, 2.5, 'a'), ('股中间肌', '#e8242a', 2.0, 2.5, 'b'),
        ('股内侧肌', '#f7c500', 2.0, 3.42, 'c'), ('股外侧肌', '#1f6fc4', 2.0, 3.52, 'd')]
for ax, (n, c, a0, a1, k) in zip(axs.flat, spec):
    xs = np.linspace(a0, a1, 80)
    ax.plot(xs, lt(xs), color=c, lw=13, alpha=.95, solid_capstyle='butt')
    ax.plot(LT[:, 0], LT[:, 1], 'k', lw=2)
    xo = np.linspace(1.7, 3.12, 80); ax.plot(xo, 115 * ((xo - 1.7) / 1.42) ** 2.2, ':', color='#c8692a', lw=2.5)
    ax.plot(3.12, 118, 'D', color='#c8692a', ms=11)
    xp = np.linspace(3.0, 4.55, 80); ax.plot(xp, 113 * ((xp - 3.0) / 1.55) ** 2.6, ':', color='#5b86d6', lw=2.5)
    ax.plot(2.5, lt(2.5), 'ko', ms=10); ax.plot(3.12, lt(3.12), 'D', mfc='white', mec='k', mew=2, ms=11)
    ax.plot([3.3, 3.36, 3.36, 3.3], [118, 118, 50, 50], 'k', lw=1)
    ax.text(3.42, 84, '残余力\n增强', fontsize=13, va='center')
    ax.text(4.0, 40, '被动\n张力', fontsize=13, va='center', color='#3d63a8')
    ax.text(.85, 107, n, fontsize=16, fontweight='bold'); ax.text(.12, 4, k, fontsize=17, fontweight='bold')
    ax.set_xlim(0, 4.6); ax.set_ylim(0, 125); ax.set_xticks(np.arange(0, 4.6, .5)); ax.set_yticks(range(0, 121, 25))
    ax.set_xlabel('肌节长度（μm）', fontsize=13); ax.set_ylabel('最大张力（%）', fontsize=13)
    ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=11)
fig.tight_layout(h_pad=2.2); save(badge(fig2pil(fig), '图3'), 'img04.jpg')

# ---------- 图 4：内力臂曲线 ----------
MA = {
    '股直肌': ('#18a84a', [(5, 20.5), (8, 25), (12, 30), (17, 37), (22, 40), (27, 43), (32, 40.5), (38, 37), (44, 35), (50, 32.5), (55, 32.7), (60, 33), (66, 28.5), (72, 26.5), (78, 24.5), (82, 23.5), (90, 23.7), (100, 23.5), (110, 23.3), (120, 23), (125, 23)]),
    '股内侧肌': ('#f2b600', [(5, 22), (7, 28), (12, 29.5), (18, 31.5), (22, 32), (28, 31.5), (34, 30.5), (40, 29), (50, 26.5), (60, 24), (70, 22.5), (80, 21.5), (90, 21), (100, 21.2), (110, 21.3), (120, 21.5), (126, 22), (133, 21.5)]),
    '股外侧肌': ('#2f72c4', [(5, 32.5), (8, 33), (10, 34), (13, 32.8), (17, 33.8), (22, 33.5), (28, 32.7), (34, 31.5), (40, 29.5), (50, 26.3), (60, 24), (70, 21.5), (80, 19.5), (85, 18.7), (95, 18.3), (105, 17.9), (115, 17.6), (120, 18), (125, 18.7), (133, 18)]),
    '股中间肌': ('#e8242a', [(5, 24.5), (8, 26), (12, 26.2), (17, 29.5), (22, 30.3), (28, 30.5), (34, 30.2), (40, 30), (50, 28.8), (60, 26.5), (70, 24.5), (80, 22.5), (90, 22), (100, 21.8), (110, 21.8), (120, 22), (126, 21.5), (130, 19.5), (133, 20)]),
}
fig, ax = plt.subplots(figsize=(10.8, 5.8), dpi=100)
ax.axvspan(17, 39, color='#f9d9db', alpha=.8, lw=0, label='伸膝内力矩峰值区（约 17°～39°）')
for n, (c, pts) in MA.items():
    p = np.array(pts); ax.plot(p[:, 0], p[:, 1], '--', color=c, lw=3, label=n)
ax.set_xlim(0, 145); ax.set_ylim(0, 64); ax.set_yticks([0, 20, 40, 60]); ax.tick_params(labelsize=14)
ax.set_xlabel('屈膝角度（°）', fontsize=17); ax.set_ylabel('力臂（mm）', fontsize=17)
ax.spines[['top', 'right']].set_visible(False); ax.legend(fontsize=14, frameon=False, loc='upper right')
fig.tight_layout(); save(badge(fig2pil(fig), '图4'), 'img05.jpg')

# ---------- 图 5：股四头肌腱/髌腱力比 + 标本 ----------
R = np.array([(0, 1.07), (5, 1.075), (10, 1.08), (15, 1.06), (20, 1.04), (25, 1.01), (28, 1.0), (35, .95), (40, .9), (50, .82), (60, .76), (70, .715), (80, .685), (90, .67), (100, .66), (110, .655), (123, .65)])
xs = np.linspace(0, 123, 300); ys = np.interp(xs, R[:, 0], R[:, 1])
fig, ax = plt.subplots(figsize=(8.4, 6.6), dpi=100)
ax.axhline(1, color='k', ls=':', lw=1.5)
ax.fill_between(xs, ys, 1, where=ys >= 1, color='#cfe1f5'); ax.fill_between(xs, ys, 1, where=ys <= 1, color='#d8f2e2')
ax.plot(xs[ys >= 1], ys[ys >= 1], color='#2f72c4', lw=3); ax.plot(xs[ys <= 1], ys[ys <= 1], color='#18a84a', lw=3)
ax.annotate('髌腱受力 > 股四头肌腱', (9, 1.08), (8, .38), fontsize=16, color='#2f72c4', arrowprops=dict(arrowstyle='->', lw=1.8))
ax.annotate('股四头肌腱受力 > 髌腱', (75, .86), (32, 1.4), fontsize=16, color='#118a3a', arrowprops=dict(arrowstyle='->', lw=1.8))
ax.set_xlim(0, 125); ax.set_ylim(0, 1.75); ax.set_yticks([0, .5, 1, 1.5]); ax.tick_params(labelsize=14)
ax.set_xlabel('屈膝角度（°）', fontsize=17); ax.set_ylabel('力比（髌腱 / 股四头肌腱）', fontsize=17)
ax.text(2, .05, 'a', fontsize=20, fontweight='bold'); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); A5 = fig2pil(fig)
b5 = X(5).crop((690, 6, 984, 394)); b5 = b5.resize((b5.width * 3, b5.height * 3), Image.LANCZOS)
b5 = inpaint(b5, [(s * 3 - 690 * 3 - 6, t * 3 - 18 - 6, u * 3 - 690 * 3 + 6, v * 3 - 18 + 6) for s, t, u, v in
                  [(800, 56, 840, 84), (872, 113, 912, 139), (735, 158, 785, 182), (892, 218, 930, 245), (892, 320, 944, 352)]], dark=None)
d = ImageDraw.Draw(b5)
for (x, y), t in [((793, 56), '股直肌'), ((850, 112), '股外侧肌'), ((738, 157), "股内侧肌"), ((882, 220), '股四头肌腱'), ((890, 324), '髌腱')]:
    label(d, ((x - 690) * 3, (y - 6) * 3), t, 48, sw=4)
H = A5.height; b5 = b5.resize((round(b5.width * H / b5.height), H), Image.LANCZOS)
c = Image.new('RGB', (A5.width + b5.width + 14, H), 'white'); c.paste(A5, (0, 0)); c.paste(b5, (A5.width + 14, 0))
save(badge(c, '图5'), 'img06.jpg')

# ---------- 图 6：标本（仅 a～d） ----------
save(badge(X(6), '图6'), 'img07.jpg')

# ---------- 图 7：力-速度关系 ----------
FV = np.array([(-300, 86), (-250, 94.3), (-200, 95.3), (-150, 89.3), (-100, 95), (-50, 89.3), (-25, 82.5), (0, 101), (30, 77), (50, 75.7), (100, 71), (150, 66), (200, 59.5), (250, 57.4), (300, 54)])
fig, ax = plt.subplots(figsize=(10.8, 6.8), dpi=100)
ax.axvspan(-300, 0, color='#f9cfd2'); ax.axvspan(0, 300, color='#fbf6c4'); ax.axvspan(-4, 4, color='#c9d3e3')
ax.plot(FV[:, 0], FV[:, 1], 'k', lw=2.6)
xr = np.linspace(0, -30, 30); ax.plot(xr, 101 + 13 * (xr / -30) ** .8, ':', color='#c8692a', lw=3); ax.plot(-38, 117, 'D', color='#c8692a', ms=13)
ax.annotate('离心收缩的\n残余力增强', (-30, 113), (-125, 108), fontsize=13, ha='center', arrowprops=dict(arrowstyle='->', lw=1.5))
ax.annotate('最大等长\n收缩力', (2, 101), (55, 110), fontsize=13, ha='center', arrowprops=dict(arrowstyle='->', lw=1.5))
ax.plot([-255, -255, -25, -25], [88, 86.5, 80.5, 82], 'k', lw=1); ax.text(-140, 74, '向心最大重量的\n105%～140%', fontsize=13, ha='center')
ax.plot([20, 30, 30, 20], [99, 99, 79, 79], 'k', lw=1); ax.text(40, 89, '向心最大重量的\n80%～100%', fontsize=13, va='center')
ax.text(-150, 40, '离心收缩', fontsize=22, ha='center', fontweight='bold'); ax.text(150, 40, '向心收缩', fontsize=22, ha='center', fontweight='bold')
ax.set_xlim(-300, 300); ax.set_ylim(30, 118); ax.tick_params(labelsize=14)
ax.set_xticks(range(-300, 301, 100)); ax.set_xticklabels(['-300', '-200', '-100', '0', '100', '200', '300'])
ax.set_xlabel('角速度（°/秒）', fontsize=17); ax.set_ylabel('最大伸膝力（%）', fontsize=17)
fig.tight_layout(); save(badge(fig2pil(fig), '图7'), 'img08.jpg')

# ---------- 图 8：训练动作选择进阶流程（原图逐框替换中文） ----------
im = X(8); d = ImageDraw.Draw(im)


def fit(box, text, fs=34, fill=None, col=INK, inset=6, bold=True):
    x0, y0, x1, y1 = box
    if fill is None:
        fill = im.getpixel((x0 + 14, y0 + 14)) if inset > 4 else im.getpixel((x0 + inset + 2, y0 + inset + 2))
    d.rectangle([x0 + inset, y0 + inset, x1 - inset, y1 - inset], fill=fill)
    w, h = x1 - x0 - 2 * inset - 8, y1 - y0 - 2 * inset - 4
    lines = text.split('\n')
    while True:
        f = font(fs); lh = fs + 6
        if max(d.textlength(l, font=f) for l in lines) <= w and lh * len(lines) - 6 <= h or fs <= 14:
            break
        fs -= 1
    ty = (y0 + y1) / 2 - (lh * len(lines) - 6) / 2
    for l in lines:
        tw = d.textlength(l, font=f)
        d.text(((x0 + x1) / 2 - tw / 2, ty), l, font=f, fill=col, stroke_width=1 if bold else 0, stroke_fill=col)
        ty += lh


fit((300, 14, 1560, 92), '术后训练动作选择的进阶', 46, fill='white')
for b, t in [((40, 104, 398, 184), '术后即刻期\n（第 0～3+ 周）'), ((480, 104, 728, 184), '过渡期\n（第 3～8+ 周）'),
             ((852, 104, 1100, 184), '早期力量期\n（第 8～12+ 周）'), ((1222, 104, 1520, 184), '传统力量期\n（第 12～24+ 周）'),
             ((1590, 104, 1822, 184), '离心/爆发力期\n（第 24+ 周）')]:
    fit(b, t, 32, inset=2)
OKC = [((50, 280, 357, 375), '节拍器\n股四头肌收缩'), ((393, 280, 762, 375), '次最大强度开链\n推/克服型等长'),
       ((832, 280, 1220, 375), '最大强度开链\n推/克服型等长'), ((1297, 280, 1840, 375), '弹震/爆发式开链\n推/克服型等长'),
       ((1583, 433, 1840, 527), '基于速度的\n向心训练'), ((112, 528, 304, 623), '直腿抬高'),
       ((342, 528, 538, 623), '直腿抬高\n+血流限制'), ((573, 528, 790, 623), '负重直腿抬高\n+血流限制'),
       ((219, 677, 308, 770), '长弧\n伸膝'), ((342, 677, 540, 770), '长弧伸膝\n+血流限制'),
       ((612, 677, 998, 770), '负重开链等张\n+血流限制'), ((1175, 677, 1775, 770), '伸膝机 大负荷慢速等张'),
       ((118, 823, 316, 917), '短弧伸膝'), ((344, 823, 542, 917), '短弧伸膝\n+血流限制'),
       ((305, 970, 735, 1066), '次最大强度开链\n退让/保持型等长'), ((779, 970, 1282, 1066), '伸膝机\n最大强度退让/保持型等长'),
       ((1550, 970, 1845, 1066), '上 2 下 1\n离心伸膝机'), ((5, 1120, 205, 1210), '股四头肌\n等长收缩'),
       ((1048, 1118, 1775, 1210), '伸膝机 离心准等长'),
       ((5, 1415, 203, 1502), '坐位弹力带\n末端伸膝'), ((272, 1410, 583, 1502), '坐位弹力带末端伸膝\n等张+血流限制'),
       ((620, 1412, 998, 1503), '闭链单腿等张\n+血流限制'), ((1175, 1412, 1775, 1502), '闭链单腿 大负荷慢速等张'),
       ((334, 1552, 573, 1648), '站立位\n末端伸膝'), ((1556, 1623, 1840, 1720), '上 2 下 1\n离心腿举机'),
       ((383, 1700, 683, 1798), '次最大强度双腿\n退让/保持型等长'), ((721, 1700, 1040, 1798), '次最大强度单腿\n退让/保持型等长'),
       ((1071, 1700, 1390, 1798), '最大强度单腿\n退让/保持型等长'), ((44, 1848, 242, 1942), '俯卧位\n股四头肌收缩'),
       ((284, 1850, 838, 1940), '俯卧股四头肌收缩→腿弯举\n等张+血流限制'), ((1145, 1848, 1772, 1942), '闭链单腿离心准等长')]
for b, t in OKC:
    fit(b, t, 32)
# 底部「基于标准的外部负荷进阶」整段重画
top = im.crop((0, 0, im.width, 2020))
lanes = [5, 373, 745, 1117, 1487, 1855]
lc = [top.getpixel(((lanes[i] + lanes[i + 1]) // 2, 1990)) for i in range(5)]
CR = [['疼痛与积液得到控制', '伸膝完全且双侧对称', '负重与屈膝逐步进阶', '股四头肌激活改善'],
      ['疼痛、积液、僵硬减轻', '屈膝 >120°', '无需辅具完全负重', '耐受次最大强度等长'],
      ['疼痛 <4/10，积液 <2+', '膝关节活动度完全对称', '耐受单腿闭链负荷', '耐受最大强度开链等长'],
      ['疼痛/积液轻微', '耐受牵张-缩短/弹震负荷', '负荷 >90% 最大重量', '耐受最大强度闭链等长'],
      ['疼痛/积液轻微', '发力率与力量持续提升', '负荷 >100% 最大重量', '耐受专项运动训练']]
nb = Image.new('RGB', (im.width, 330), 'white'); d = ImageDraw.Draw(nb)
f = font(40); t = '基于标准的外部负荷进阶'; d.text((im.width / 2 - d.textlength(t, font=f) / 2, 14), t, font=f, fill=INK, stroke_width=1, stroke_fill=INK)
for i in range(5):
    x0, x1 = lanes[i], lanes[i + 1]
    d.polygon([(x0, 76), (x1 - 8, 76), (x1 + 22, 198), (x1 - 8, 320), (x0, 320), (x0 + (22 if i else 0), 198)], fill=lc[i], outline=(60, 60, 60))
    f = font(27)
    for k, l in enumerate(CR[i]):
        d.text((x0 + 34, 94 + k * 55), l, font=f, fill=INK)
im = Image.new('RGB', (top.width, top.height + nb.height), 'white'); im.paste(top, (0, 0)); im.paste(nb, (0, top.height))
save(badge(im, '图8'), 'img09.jpg')


# ---------- 图 9：术后即刻期动作（无文字） ----------
save(badge(X(9), '图9'), 'img10.jpg', W=760)


# ---------- 图 10：背景墙英文大字抹除（按分栏处理，人物保留） ----------
def dewall(img, xr, ybot=618):
    src = np.array(img).astype(np.float32); out = src.copy()
    for x0, x1 in xr:
        im_ = src[:, x0:x1]; u8 = im_.astype(np.uint8)
        hsv = cv2.cvtColor(u8, cv2.COLOR_RGB2HSV); g = cv2.cvtColor(u8, cv2.COLOR_RGB2GRAY)
        lo = np.full(g.shape, 66, np.float32); lo[420:] = 42
        m = ((g > lo) & (g < 232) & (hsv[..., 1] < 52)).astype(np.uint8); m[ybot:] = 0
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)); m[ybot:] = 0
        wf = m.astype(np.float32); k = (151, 151)
        fc = cv2.blur(im_ * wf[..., None], k) / (cv2.blur(wf, k)[..., None] + 1e-3) * 0.85
        a = cv2.GaussianBlur(wf, (0, 0), 1.2)[..., None]
        out[:, x0:x1] = im_ * (1 - a) + fc * a
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


save(badge(dewall(X(10), [(17, 509), (515, 1005), (1012, 1499), (1506, 1997)]), '图10'), 'img11.jpg')

# ---------- 图 11、12：器械品牌/标签字样模糊 ----------
im = X(11)
B11 = []
for dx in (0, 612, 1226):
    B11 += [(140 + dx, 80, 205 + dx, 122), (470 + dx, 80, 530 + dx, 128), (292 + dx, 290, 334 + dx, 530),
            (150 + dx, 578, 300 + dx, 700)]
save(badge(blur(im, B11), '图11'), 'img12.jpg')
im = X(12); s = 1.0155
B12 = []
for dx in (0, 500, 1000, 1500):
    B12 += [(200 + dx, 2, 350 + dx, 50), (745 if dx == 500 else 1245, 45, 795 if dx == 500 else 1295, 230) if dx in (500, 1000) else None,
            (30 + dx, 455, 120 + dx, 540), (430 + dx, 750, 480 + dx, 840)]
B12 = [tuple(round(v * s) for v in b) for b in B12 if b]
save(badge(blur(im, B12), '图12'), 'img13.jpg')

# ---------- 图 13：速度训练（仅数字） ----------
save(badge(X(13), '图13'), 'img14.jpg')

# ---------- 封面：图 12 上排 ----------
c12 = Image.open(f'{OUT}/img13.jpg'); w = c12.width; ch = round(w * 383 / 900)
c12.crop((0, 40, w, 40 + ch)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
