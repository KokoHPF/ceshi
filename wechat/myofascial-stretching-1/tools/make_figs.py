#!/usr/bin/env python3
"""Colonna、Casacci 2024 肌筋膜系统与运动 Part I（拉伸）：首图中文标题卡、原文作者自绘的 Hill 三元素模型图和拉伸示意图贴中文标签、
触发点机制卡、三种拉伸方法对照卡、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
WORK, OUT, FM, FBOLD = sys.argv[1:5]
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('叙述性综述 · 《Cureus》2024', ['肌筋膜系统与运动（上）：', '拉伸'],
               'Colonna S, Casacci F.', 'Cureus. 2024;16(12):e75077. doi:10.7759/cureus.75077',
               '意大利博洛尼亚 Spine Center 康复医学部、Osteopathic Spine Center Education 研发部'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1
def strip(im, labels, W=1200, fs=30):
    im = k.op(im) if isinstance(im, str) else im; im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = max(t.count('\n') + 1 for _, t, _ in labels); h = lines * (fs + 10) + 24
    o = Image.new('RGB', (W, im.height + h), 'white'); o.paste(im, (0, 0)); d = ImageDraw.Draw(o); f = ImageFont.truetype(FBOLD, fs)
    for fx, t, c in labels:
        for j, ln in enumerate(t.split('\n')):
            tw = d.textlength(ln, font=f); d.text((fx * W - tw / 2, im.height + 12 + j * (fs + 10)), ln, font=f, fill=c)
    return o

put(strip('x94.jpg', [(.2, 'CE＝收缩成分（肌纤维）', RED), (.53, 'SE＝串联弹性成分', C_NAV), (.84, 'PE＝并联弹性成分', TEAL)], fs=28),
    '原文图 1  Hill 三元素模型：收缩成分（CE）与串联弹性成分（SE，如肌腱）串联，两者再与并联弹性成分（PE，如肌外膜、肌束膜、肌内膜等筋膜）并联')
k.save(k.card('触发点是怎么形成的？作者的新假说（编者整理）', [
    ('已知机制', '触发点是绷紧肌带中的高敏感点，内有大量“收缩结”（肌节过度收缩）\n持续低强度收缩（10%～25% 最大收缩）就足以让肌内压升高、血流受阻 → 缺氧 → ATP 不足，肌丝无法解离 → 局部挛缩；缺氧还促进缓激肽释放、致敏痛觉感受器', LT, TEAL),
    ('作者的假说', '本该由“并联”筋膜系统承担的稳定任务没做好时，“串联”系统就靠肌肉持续收缩来代偿\n这种收缩是为了“稳住”，不是为了“动”，在不能伸展的筋膜鞘里持续升高内压 → 缺血 → 触发点', OR, (200, 120, 0)),
    ('腰痛的例子', '健康人弯腰到底时竖脊肌会“放电静息”（屈曲-放松现象），靠韧带、筋膜等被动结构撑住\n很多腰痛患者这个现象消失，竖脊肌一直在收缩；超声也看到慢性腰痛者胸腰筋膜增厚、多裂肌变薄', PK, RED),
]), n); n += 1
put(tags_at(k, 'x195.jpg', [(.02, .1, 'A 放松', C_NAV), (.02, .33, 'B 被动拉伸', TEAL), (.02, .57, 'C 肌肉收缩', RED), (.02, .8, 'D 两者结合', (200, 120, 0))]),
    '原文图 2  不同负荷下张力落在哪：A 放松，各成分都不受力；B 经典被动拉伸，拉长的主要是并联筋膜（PE），串联部分（SE）被松弛的肌纤维“吸收”了；C 肌肉收缩，拉紧的是串联筋膜；D 先收缩再拉开，串联、并联都被加载')
put(tags_at(k, 'x213.jpg', [(.0, .0, 'A 中立', C_NAV), (.5, .0, 'B 经典静态拉伸', TEAL), (.0, .52, 'C 收缩-放松（CR）', RED), (.5, .52, 'D CR＋对侧肌收缩（CRAC）', (200, 120, 0))]),
    '原文图 3  腘绳肌拉伸的三种方法（脚放在瑜伽球上）：B 被动拉长；C 在拉长位让腘绳肌等长收缩后再拉；D 在 C 之后再收缩股四头肌（对侧肌），把腘绳肌进一步拉开。图中弹簧示意 CE、SE、PE')
k.save(k.card('三种拉伸方法分别作用于哪一部分（作者的力学解释）', [
    ('经典静态拉伸（Anderson）', '被动拉开起止点，最先被拉长的是并联筋膜；松弛的肌纤维弹性大，替串联部分“卸”掉了张力\n→ 主要作用于并联筋膜', LT, TEAL),
    ('收缩-放松（CR）', '在拉长位让被拉的肌肉等长收缩几秒，再拉到新的极限\n→ 收缩时张力主要加载在串联筋膜上，同时并联部分减负', OR, (200, 120, 0)),
    ('CR＋对侧肌收缩（CRAC）', 'CR 之后再主动收缩对侧肌（拉腘绳肌时收缩股四头肌），进一步拉开起止点\n→ 串联、并联都被加载；作者建议三种方法按顺序都用', PK, RED),
    ('原文建议的剂量（图 2D）', '目标肌收缩约 6～15 秒 → 放松，同时对侧肌收缩约 6～15 秒拉开；循环 3～5 次', GR, (0, 120, 60)),
]), n); n += 1
c = k.op('x213.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .58)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
