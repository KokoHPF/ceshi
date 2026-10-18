#!/usr/bin/env python3
"""Escamilla 2016 仰卧、俯卧、侧卧核心训练（有/无瑞士球）肌电研究：首图中文标题卡；图 1～9 动作照片按白缝切分、
修补右下角 a/b/c 字母后加中文标签；表 1 肌电做成热力图、表 2 主观用力做成条形图（均用原文数值）。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymupdf
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 13
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130)
d = pymupdf.open(PDF)


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88)


def raw(x):
    return Image.open(BytesIO(d.extract_image(x)['image'])).convert('RGB')


def panels(im):
    """按整行接近白色的缝把竖排的子图切开"""
    a = np.array(im.convert('L')); white = a.mean(axis=1) > 245
    out, s = [], None
    for i, wv in enumerate(list(white) + [True]):
        if not wv and s is None: s = i
        if wv and s is not None:
            if i - s > 40: out.append(im.crop((0, s, im.width, i)))
            s = None
    return out


def unletter(p):
    """修补右下角的小写字母"""
    a = np.array(p); h, w = a.shape[:2]; m = np.zeros((h, w), np.uint8)
    x0, y0 = w - 34, h - 34
    sub = a[y0:h - 2, x0:w - 2]
    lum = sub.mean(axis=2); bg = np.median(lum)
    m[y0:h - 2, x0:w - 2][np.abs(lum - bg) > 45] = 255
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    return Image.fromarray(cv2.inpaint(a, m, 5, cv2.INPAINT_TELEA))


def board(title, ims, tags, cw=900):
    ims = [i.resize((cw, round(i.height * cw / i.width)), Image.LANCZOS) for i in ims]
    W = cw + 40; H = 90 + sum(i.height + 16 for i in ims) + 10
    out = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(out)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(40), fill='white')
    y = 90
    for im, t in zip(ims, tags):
        out.paste(im, (20, y))
        if t:
            f = font(40); w = dr.textlength(t, font=f)
            dr.rounded_rectangle([20 + cw - w - 40, y + im.height - 66, 20 + cw - 10, y + im.height - 10], 10, fill=(255, 255, 255))
            dr.text((20 + cw - w - 25, y + im.height - 61), t, font=f, fill=INK)
        y += im.height + 16
    return out


# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '实验室研究 · 《运动健康》（Sports Health）2016', font=font(32), fill=TEAL)
for i, t in enumerate(['平板、侧桥、卷腹、瑞士球：', '10 个核心动作肌电大比拼']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), '18 名健康成人 · 7 块肌肉表面肌电 · 主观用力评分', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Escamilla RF 等，Sports Health 2016;8(4):372-379', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

# ---------- 动作照片 ----------
FIGS = [
    (36, '原文图 1　瑞士球俯卧位伸髋（右/左）', ['起始', '结束：伸右髋', '结束：伸左髋']),
    (39, '原文图 2　瑞士球俯卧平板', ['起始', '结束']),
    (40, '原文图 3　脚尖支撑俯卧平板', ['起始', '结束']),
    (41, '原文图 4　跪姿俯卧平板', ['起始', '结束']),
    (42, '原文图 5　瑞士球侧卷腹', ['起始', '结束']),
    (44, '原文图 6　脚支撑侧桥', ['起始', '结束']),
    (45, '原文图 7　跪姿侧桥', ['起始', '结束']),
]
for n, (x, title, tags) in enumerate(FIGS, start=2):
    ps = [unletter(p) for p in panels(raw(x))]
    assert len(ps) == len(tags), (x, len(ps))
    save(board(title, ps, tags), n)
save(board('原文图 8　卷腹（结束位）', [raw(46)], ['']), 9)
save(board('原文图 9　屈膝仰卧起坐（结束位）', [raw(47)], [''], 700), 10)

# ---------- 表 1 热力图 ----------
EX = ['瑞士球俯卧伸右髋', '瑞士球俯卧伸左髋', '瑞士球俯卧平板', '脚尖俯卧平板', '跪姿俯卧平板',
      '瑞士球侧卷腹', '脚支撑侧桥', '跪姿侧桥', '卷腹', '屈膝仰卧起坐']
MU = ['上腹直肌', '下腹直肌', '腹外斜肌', '腹内斜肌', '腰椎旁肌', '背阔肌', '股直肌']
V = np.array([[43, 44, 56, 40, 7, 17, 9], [41, 39, 39, 45, 6, 21, 35], [49, 48, 42, 39, 6, 17, 10], [34, 40, 40, 29, 5, 18, 20],
              [27, 26, 22, 20, 5, 10, 7], [21, 16, 50, 20, 22, 12, 8], [26, 21, 62, 28, 29, 12, 14], [17, 14, 37, 17, 18, 10, 10],
              [53, 39, 28, 33, 5, 8, 6], [40, 35, 36, 31, 6, 8, 23]])
fig, ax = plt.subplots(figsize=(9.5, 7.6), dpi=150)
cmap = matplotlib.colors.ListedColormap(['#eef4f8', '#a9cce3', '#2e86c1', '#1b3f66'])
norm = matplotlib.colors.BoundaryNorm([0, 20.5, 40.5, 60.5, 100], 4)
ax.imshow(V, cmap=cmap, norm=norm, aspect='auto')
for i in range(V.shape[0]):
    for j in range(V.shape[1]):
        ax.text(j, i, V[i, j], ha='center', va='center', fontsize=15, color='white' if V[i, j] > 40 else '#222')
ax.set_xticks(range(7)); ax.set_xticklabels(MU, fontsize=14); ax.xaxis.tick_top()
ax.set_yticks(range(10)); ax.set_yticklabels(EX, fontsize=14)
for y in (4.5, 7.5): ax.axhline(y, color='white', lw=4)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(['#eef4f8', '#a9cce3', '#2e86c1', '#1b3f66'],
          ['低（0～20%）', '中（21～40%）', '高（41～60%）', '很高（> 60%）'])],
          loc='upper center', bbox_to_anchor=(0.45, -0.02), ncol=4, frameon=False, fontsize=12)
ax.set_title('各动作肌肉激活（%最大自主等长收缩，原文表 1 均值）', fontsize=14, pad=36)
fig.tight_layout(); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 11)

# ---------- 表 2 主观用力 ----------
R = [13.1, 13.1, 11.8, 11.9, 8.9, 11.2, 11.2, 9.9, 10.2, 10.4]
order = np.argsort(R)
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=150)
ax.barh([EX[i] for i in order], [R[i] for i in order], color=['#1b3f66' if R[i] >= 13 else '#2e86c1' if R[i] >= 11 else '#a9cce3' for i in order])
for k, i in enumerate(order): ax.text(R[i] + 0.1, k, f'{R[i]}', va='center', fontsize=11)
ax.set_xlim(6, 14.5); ax.set_xlabel('主观用力评分（6～20 分，6＝毫不费力，13＝有点吃力）')
for s in ['top', 'right']: ax.spines[s].set_visible(False)
ax.set_title('各动作的主观用力（原文表 2 均值）', fontsize=14)
fig.tight_layout(); fig.savefig(f'{OUT}/_p.png'); plt.close(fig); save(Image.open(f'{OUT}/_p.png'), 12)
import os; os.remove(f'{OUT}/_p.png')

# ---------- 封面 900×383 ----------
c = unletter(panels(raw(36))[1]); c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
t = max(0, (c.height - 383) // 2); c.crop((0, t, 900, t + 383)).save(f'{OUT}/cover.jpg', quality=90)
