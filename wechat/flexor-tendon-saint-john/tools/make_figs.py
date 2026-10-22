#!/usr/bin/env python3
"""Higgins & Lalonde 2016 屈肌腱修复术后 Saint John 方案：首图中文标题卡；原文补充视频 2～4（src/video/v2～v4.mp4）截取动作片段做成 GIF，
英文字幕原位盖掉改为中文字幕；视频 1（英文幻灯片讲座）的要点和各阶段方案整理为中文卡片。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys, os
import numpy as np
import pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
font_manager.fontManager.addfont(F)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=F).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228)
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


def board(tiles, title, W=1200):
    H = sum(t.height for t in tiles) + 14 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles: out.paste(t, (0, y)); y += t.height + 14
    return titled(out, title)


def relabel(im, items, bg='white'):
    """items: (box@1000宽, 文字, 字号@1000宽, 对齐)"""
    s = im.width / 1000; d = ImageDraw.Draw(im)
    for box, t, fs, *al in items:
        b = [int(v * s) for v in box]
        d.rectangle(b, fill=bg)
        f = font(fs * s); lines = t.split('\n'); lh = fs * s * 1.25
        y0 = (b[1] + b[3]) / 2 - lh * len(lines) / 2
        for i, l in enumerate(lines):
            w = d.textlength(l, font=f)
            x = b[0] + 2 if al and al[0] == 'l' else (b[0] + b[2]) / 2 - w / 2
            d.text((x, y0 + i * lh), l, font=f, fill='black')
    return im


def blur(im, boxes, r=10):
    s = im.width / 1000
    for b0 in boxes:
        b = tuple(int(v * s) for v in b0); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * s)), b[:2])
    return im
def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def card(W, title, blocks, bg=(246, 248, 250)):
    """blocks: (小标题, 正文, 底色, 强调色)，纵向排列"""
    im = Image.new('RGB', (W, 4000), 'white'); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 100
    for h, t, c, a in blocks:
        top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 4000)))
        for seg in t.split('\n'): y2 = para(dd, 50, y2, seg, 28, W - 100, gap=14)
        dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c)
        dr.rectangle([20, top, 30, y2 + 10], fill=a)
        dr.text((50, top + 16), h, font=font(32), fill=a)
        yy = y + 62
        for seg in t.split('\n'): yy = para(dr, 50, yy, seg, 28, W - 100, gap=14)
        y = y2 + 30
    return im.crop((0, 0, W, y))


up = lambda im, w=1000: im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def lab(im, page_bbox, items, fs=30, pad=6):
    """items: (页面 x, 页面 y, 中文, 颜色)；按 PDF 坐标映射到图像，白底写字"""
    x0, y0, x1, y1 = page_bbox; s = im.width / (x1 - x0); dr = ImageDraw.Draw(im)
    for x, y, t, *c in items:
        X, Y = (x - x0) * s, (y - y0) * s; f = font(fs)
        lines = t.split('\n'); w = max(dr.textlength(l, font=f) for l in lines); h = fs * 1.2 * len(lines)
        dr.rounded_rectangle([X - pad, Y - pad, X + w + pad, Y + h + pad], 6, fill=(255, 255, 255))
        for i, l in enumerate(lines): dr.text((X, Y + i * fs * 1.2), l, font=f, fill=c[0] if c else INK)
    return im


def row(ims, W=1200, gap=12):
    h = min(i.height for i in ims); ims = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in ims]
    tw = sum(i.width for i in ims) + gap * (len(ims) - 1); s = W / tw
    ims = [i.resize((round(i.width * s), round(h * s)), Image.LANCZOS) for i in ims]
    out = Image.new('RGB', (W, ims[0].height), 'white'); x = 0
    for i in ims: out.paste(i, (x, 0)); x += i.width + round(gap * s)
    return out


def stack(ims, gap=14):
    W = max(i.width for i in ims); out = Image.new('RGB', (W, sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
    for i in ims: out.paste(i, (0, y)); y += i.height + gap
    return out


import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0, HERE)
SRC = _os.path.join(HERE, '..', 'src')

import subprocess, tempfile, shutil
ROOT = _os.path.join(HERE, '..'); VID = _os.path.join(SRC, 'video')

# 首图
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 50), '视频手术技术 · 《整形与重建外科全球开放》2016', font=font(32), fill=TEAL)
dr.text((70, 135), '屈肌腱修复术后康复：', font=font(56), fill=INK)
dr.text((70, 215), 'Saint John 方案', font=font(56), fill=INK)
dr.line([70, 330, W - 70, 330], fill=(200, 205, 210), width=2)
dr.text((70, 360), 'Higgins A, Lalonde DH.', font=font(28), fill=GREY)
dr.text((70, 405), 'Plast Reconstr Surg Glob Open. 2016;4(11):e1134', font=font(28), fill=GREY)
dr.text((70, 470), '编者中文解读，仅作学术交流；动图截自原文补充视频', font=font(26), fill=(150, 150, 150))
save(im, 1)

blocks = [('① 半拳就有足够的滑动', '做到半拳的真正主动屈曲，指深屈肌腱就能滑动 5～10 mm，足以防止粘连', LT, TEAL),
          ('② 全拳更容易在滑车硬缘上拉开修复口', '全拳时修复处会在 A4 滑车近端硬缘上折成约 90°，术中可见由此产生缝隙', OR, (200, 110, 30)),
          ('③ 全拳最后三分之一的屈曲做功更大', '做功越大，断裂风险越高', GR, (40, 130, 60)),
          ('④ 全拳最后三分之一的摩擦更大', '摩擦越大，断裂风险越高', PK, RED),
          ('术中观察到的', '清醒局麻无止血带（WALANT）手术中，半拳真正主动活动可带来 0.5～1 cm 的指深屈肌腱滑动；所谓全拳“被动放置并保持”，实际上常见的是“屈曲—弹跳”', LT, TEAL)]
save(card(1200, '为什么放弃全拳“放置—保持”，改做最多半拳的真正主动屈曲（视频 1 要点）', blocks), 2)

blocks = [('术后 0～3/5 天：制动和抬高', '术中就教会患者：手指完全不动，手始终抬高，避免伤口内出血（血块会变成瘢痕）\n背侧阻挡支具：腕最多伸 45°，掌指关节屈 30°，指间关节完全伸直\n理由：第 3 天前胶原还没开始形成；等 3～5 天，肿胀、屈曲做功和摩擦都下降', LT, TEAL),
          ('4 天～2 周：清醒时每小时 10 次', '口诀“可以动，但不能用！”（术中和每次复诊至少强调 3 次）\n抬高 + 自粘绷带轻压手指控制水肿\n支具内先做所有手指被动屈曲“热身”\n掌指关节被动屈曲位下主动伸直指间关节，预防屈曲挛缩\n真正主动屈曲到 1/3～半拳，从远侧指间关节开始启动（主动“勾拳”）\n不用力、不痛、不勉强；建议停用所有止痛药，按疼痛引导训练', GR, (40, 130, 60)),
          ('2～4 周：换 Manchester 短支具', '背侧阻挡支具改为 Manchester 短支具，允许腕活动\n在短支具内做腕和手指的主动协同运动\n逐步做到半拳到全拳，腕伸最多 45°\n继续在掌指关节完全屈曲位下完全伸直指间关节；6 周前争取做到全拳', OR, (200, 110, 30)),
          ('6 周', '停用 Manchester 短支具，可以开始用手做轻活动\n需要时夜间戴手掌或手指伸直支具，纠正指间关节屈曲挛缩；白天活动可用相对运动屈曲矫形器', PK, RED)]
save(card(1200, 'Saint John 方案各阶段要点（编者根据原文整理）', blocks), 3)



def clip(v, t0, dur, name, boxes, speed=1.0, fps=7, W=360):
    """截取视频片段：裁掉左右黑边（x 105～747），在英文字幕位置盖上深色框并写中文字幕，再合成 GIF"""
    tmp = tempfile.mkdtemp()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t0), '-t', str(dur), '-i', _os.path.join(VID, f'v{v}.mp4'),
                    '-vf', f'setpts={1 / speed}*PTS,fps={fps}', f'{tmp}/%04d.png'], check=True)
    for f in sorted(_os.listdir(tmp)):
        im = Image.open(f'{tmp}/{f}').convert('RGB'); dr = ImageDraw.Draw(im, 'RGBA')
        for (x0, y0, x1, y1), t, fs in boxes:
            dr.rectangle([x0, y0, x1, y1], fill=(0, 0, 0, 255))
            ft = font(fs); ls = t.split('\n'); lh = fs * 1.3; y = (y0 + y1) / 2 - lh * len(ls) / 2; cx = (max(x0, 105) + min(x1, 747)) / 2
            for l in ls:
                dr.text((cx - dr.textlength(l, font=ft) / 2, y), l, font=ft, fill='white'); y += lh
        im.crop((105, 0, 747, 480)).save(f'{tmp}/{f}')
    out = _os.path.join(ROOT, 'gifs', name)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', f'{tmp}/%04d.png', '-vf',
                    f'scale={W}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4',
                    '-loop', '0', out], check=True)
    shutil.copy(f'{tmp}/0001.png', _os.path.join(VID, name.replace('.gif', '_first.png')))
    shutil.rmtree(tmp); print(name, round(_os.path.getsize(out) / 1e6, 2), 'MB')


clip(2, 34, 12, 'g1_warmup.gif', [((105, 345, 760, 480), '术后 3～4 天开始被动热身\n清醒时每小时 10 次', 26)])
clip(2, 76, 14, 'g2_ip_ext.gif', [((105, 380, 760, 480), '被动屈曲掌指关节\n促进指间关节主动伸直', 26)])
clip(2, 112, 12, 'g3_halffist.gif', [((105, 10, 310, 170), '真正主动屈曲\n最多半拳', 26)])
clip(2, 132, 14, 'g4_halffist2.gif', [((105, 10, 310, 170), '真正主动屈曲\n最多半拳', 26)])
clip(3, 36, 12, 'g5_glide.gif', [((40, 55, 245, 475), '保持肌腱\n主动屈曲\n滑动足够\n就不会\n粘住', 26)])
clip(3, 77, 10, 'g6_dip.gif', [((40, 340, 760, 460), '真正主动活动\n从远侧指间关节开始启动肌腱滑动', 26)])
clip(3, 94, 18, 'g7_synergy.gif', [((630, 185, 850, 475), '腕和\n手指\n主动\n协同\n运动', 26)])
clip(4, 40, 18, 'g8_fist.gif', [])
clip(4, 86, 22, 'g9_fist_open.gif', [])
clip(4, 125, 15, 'g10_passive_ext.gif', [])

c = Image.open(_os.path.join(VID, 'g9_fist_open_first.png')).convert('RGB')
c = c.crop((0, 100, 642, 100 + 273)).resize((900, 383), Image.LANCZOS); c.save(f'{OUT}/cover.jpg', quality=90)
print('ok')
