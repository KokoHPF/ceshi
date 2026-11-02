#!/usr/bin/env python3
"""Winnett & Fenech 2025 AJUM《TFCC 与下尺桡关节的超声解剖和成像》→ 小红书 3:4 图文卡片。
原文 CC BY 4.0：用编者中文标注版原图 work/zh/*.zh.jpg（relabel.py 生成）按面板裁切放大，图例说明写在卡片文字里。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='腕关节超声', source='Australas J Ultrasound Med 2025;28:e70012', fonts_dir=FONTS)
def G(x, box=None):
    p = os.path.join(WORK, 'zh', f'{x}.full.jpg'); p = p if os.path.exists(p) else os.path.join(WORK, 'zh', f'{x}.zh.jpg'); p = p if os.path.exists(p) else os.path.join(WORK, f'{x}.jpg')
    im = Image.open(p).convert('RGB'); return im.crop(box) if box else im
def hcat(*ims, gap=12):
    h = max(i.height for i in ims); ims = [i.resize((round(i.width * h / i.height), h)) for i in ims]
    c = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), h), 'white'); x = 0
    for i in ims: c.paste(i, (x, 0)); x += i.width + gap
    return c

deck.cover(['TFCC 与下尺桡关节', '超声解剖与扫查'], kicker='AJUM 2025 · 综述',
           subtitle='尺侧腕痛的“黑匣子”，拆开一个个看', photos=[(G('x69', (240, 0, 1001, 1098)), 'TFCC 五个组成部分（原文图 4）')], banner='9 张原图 + 2 段视频截图 · 中文标注')
deck.text('先说结论', '原文要点', [
    ('box', '为什么难', '尺侧腕痛被称为腕部的“腰痛”“黑匣子”：结构小而交织，病变**常多处并存**', 'navy'),
    ('box', 'TFCC 五个部分', '关节盘 · 半月板同系物 · ECU 腱下鞘 · 掌侧尺腕韧带 · 桡尺远侧韧带——超声都能单独显示', 'teal'),
    ('box', '要一起看', 'TFCC 和下尺桡关节交织在一起，**必须同时评估**', 'yellow'),
    ('box', '超声的边界', '外周看得好、能动态看；**中央和深部**撕裂超声不能可靠排除，要靠 MRI / MR 关节造影', 'accent')])
deck.text('① 尺侧腕痛可能是什么', '原文第 1 节', [
    ('box', '常见原因', 'TFCC 撕裂；下尺桡关节退变或不稳；尺侧腕伸肌（ECU）腱病、撕裂、半脱位', 'navy'),
    ('bul', ['尺骨茎突骨折、钩骨钩骨折', '钩骨关节面退变、豌豆三角关节病', '月骨缺血坏死（Kienböck 病）、月三角损伤和不稳', '尺侧 / 桡侧腕屈肌腱病', '尺神经及其分支卡压', '尺骨撞击综合征']),
    ('box', '超声的用处', '找结构性改变，引导注射止痛', 'teal')])
deck.figure('② 检查体位', '原文图 1', [G('x12', (0, 0, 959, 706)), hcat(G('x12', (996, 0, 1562, 706)), G('x12', (1579, 0, 2078, 706)))], None, [
    ('steps', [('A', '坐位，手旋前，前臂垫枕抬到肩高，经背尺侧长轴扫查'), ('B', '长轴：手桡偏，打开尺腕间隙'), ('C', '短轴：手桡偏')])
    ], stack=True, max_h=980)
deck.figure('③ 腕部三个关节', '原文图 2A（编者中文标注）', G('x41', (0, 0, 745, 400)), None, [
    ('box', '互不相通', '下尺桡关节、桡腕关节、腕中关节，正常时互不相通；“尺腕关节”更宜称**尺腕间隙**，TFCC 就在其中', 'navy'),
    ('box', '下尺桡关节', '枢轴关节：负责旋前旋后，也承重；**天生不稳**，主要靠软组织稳定', 'teal'),
    ('box', '怎么扫', '旋前 + 最大旋后都要扫；向近端扫到旋前方肌水平，积液会向近端延伸', 'accent')], max_h=620)
deck.figure('④ 尺骨头的四个部分', '原文图 2D（编者中文标注）', G('x41', (800, 420, 1491, 1084)), None, [
    ('steps', [('头周缘', '与桡骨乙状切迹相关节'), ('尺骨座', '朝向月骨，软骨软化好发'), ('小凹 · 茎突', 'TFCC 多个关节囊韧带结构的附着点')])], max_h=760)
deck.figure('⑤ 外在稳定：旋前方肌、骨间膜', '原文图 3E（编者中文标注）', G('x67', (545, 345, 1465, 840)), None, [
    ('box', '骨间膜', '远端增厚为远侧斜束，止于乙状切迹背侧缘；Galeazzi 骨折常伴骨间膜损伤', 'navy'),
    ('box', '旋前方肌', '骨间前神经支配；绷紧关节囊、限制桡骨背移', 'teal'),
    ('box', '下图对照', '图为左右对照：左前臂骨折后骨间前神经被卡压 → 旋前方肌萎缩、**回声增高**', 'accent')], max_h=640)
deck.figure('⑥ TFCC 五个组成部分', '原文图 4（背侧观，编者中文标注）', G('x69', (455, 430, 975, 1000)), None, [
    ('steps', [('①', '关节盘（Disc proper）'), ('②', '半月板同系物（MH）'), ('③', '尺侧腕伸肌腱下鞘（ECU sub-sheath）'), ('④', '尺月韧带（ULL）、尺三角韧带（UTL）'), ('⑤', '背侧 / 掌侧桡尺远侧韧带（DDRUL / PDRUL）')])], max_h=900)
deck.figure('⑦ 关节盘', '原文图 5A–C（编者中文标注）', [G('x94', (0, 0, 725, 834)), G('x94', (725, 0, 1501, 834))], None, [
    ('box', '结构', '桡侧附着部发出 → 分**近侧板**（止于小凹）和**远侧板**（止于茎突）；两板之间是下隐韧带（L. Subcruentum）', 'navy'),
    ('box', '怎么扫', '背侧入路屈腕 + 桡偏；尺侧入路以 ECU 为声窗', 'teal')], max_h=640)
deck.figure('⑧ 关节盘：血供与局限', '原文图 5D（编者中文标注）', G('x94', (400, 844, 1100, 1315)), None, [
    ('box', '血供', '骨间前动脉背、掌侧支吻合（红线）供血；**外周血供好，中央薄而少** → 随年龄退变穿孔，最早 40 多岁', 'teal'),
    ('box', '超声看不清', '中央部、下隐韧带位置深 → 撕裂**不能排除**；正尺骨变异时更难，需 MRI', 'accent')], max_h=560)
deck.figure('⑨ 半月板同系物（MH）', '原文图 6A（编者中文标注）', G('x126', (0, 34, 733, 873)), None, [
    ('steps', [('①', '体部（茎突部）：附着茎突，远端多附三角骨'), ('②', '桡尺部：最近端，与关节盘融合'), ('③', '侧副部：与 ECU 腱下鞘、尺侧副韧带融合'), ('④', '远侧部：到钩骨和第 5 掌骨底')]),
    ('box', '特点', '主要是滑膜组织，桡偏时延长、折叠；从三角骨整体脱离 = Nishikawa-tilt 损伤', 'yellow')], max_h=680)
deck.figure('⑩ MH 超声与茎突前隐窝', '原文图 6B、C，视频 2（编者中文标注）', [G('x126', (777, 34, 1501, 590)), G('x165')], None, [
    ('box', '怎么扫', '背尺侧长轴；正常 MH **桡偏、尺偏时可见滑动**；深部撕裂超声不能排除', 'teal'),
    ('box', '茎突前隐窝', '关节盘与 MH 体部之间的窄滑膜间隙；无症状腕也可见**气泡移动**，积液意义待研究', 'accent')], stack=True, max_h=860)
deck.figure('⑪ ECU 腱下鞘', '原文图 7（编者中文标注）', G('x189', (0, 42, 1470, 551)), None, [
    ('box', '最稳定的位置', '尺骨远端水平：包绕 ECU 肌腱的**高回声带**，把肌腱固定在尺骨沟', 'navy'),
    ('box', '伸肌支持带', '在浅面构成“顶”，不直接附着尺骨，防止肌腱弓弦样弹起', 'teal'),
    ('box', '再往远', '尺腕间隙以远边界不清、逐渐变薄，超声定义还需研究', 'grey')], max_h=520)
deck.figure('⑫ 掌侧尺腕韧带', '原文图 8A、B（编者中文标注）', G('x190', (0, 0, 1475, 777)), None, [
    ('box', '组成', '尺月韧带 ULL、尺三角韧带 UTL（尺头韧带是否属 TFCC 无共识）；起于掌侧桡尺韧带 PDRUL，扇形止于月骨、三角骨、头状骨', 'navy'),
    ('box', 'B 图缩写', 'Disc proper 关节盘 · DDRUL 背侧桡尺远侧韧带 · MH 半月板同系物', 'grey')], max_h=640)
deck.figure('⑬ 掌侧尺腕韧带超声', '原文图 8C、D（编者中文标注）', [G('x190', (290, 843, 1320, 1327)), G('x190', (290, 1348, 1320, 1899))], None, [
    ('box', '怎么扫', '探头放掌尺侧，以尺骨远端和月骨、三角骨为标志，在**屈肌腱深面**找；三条韧带常连成一片', 'teal'),
    ('box', '部分撕裂', '增厚、回声减低', 'accent')], stack=True, max_h=900)
deck.figure('⑭ 桡尺远侧韧带：旋前与旋后', '原文图 9A–C（编者中文标注）', G('x210', (0, 0, 1501, 870)), None, [
    ('steps', [('旋前', '背侧**浅层** + 掌侧**深层**紧张'), ('旋后', '背侧**深层** + 掌侧**浅层**紧张')]),
    ('box', '分层', '浅层止于尺骨茎突，深层止于小凹，尺侧呈“四臂”结构', 'navy')], max_h=760)
deck.figure('⑮ 桡尺远侧韧带超声', '原文图 9D、E（编者中文标注）', [G('x210', (0, 898, 655, 1286)), G('x210', (660, 898, 1501, 1286))], None, [
    ('box', '怎么扫', '背侧、掌侧入路长轴，探头**垂直于桡尺骨长轴**；呈纤维状带，旋前旋后动态看尺侧附着', 'teal'),
    ('box', 'D / E', 'D 掌侧韧带（白箭头，厚 1.8 mm）· E 背侧韧带：实线浅层、虚线深层', 'grey')], stack=True, max_h=760)
deck.text('收藏：超声 vs MRI', '据原文整理', [
    ('steps', [('能看', '下尺桡关节 · 关节盘外周 · MH · ECU 腱下鞘 · 尺腕韧带 · 桡尺远侧韧带'), ('看不清', '关节盘中央 · 下隐韧带 · MH 深部'), ('MRI 优势', 'MR 关节造影对深部、中央部损伤更敏感、更特异')]),
    ('h', '原文对不上的地方'),
    ('bul', ['图 9E 图注写黄、绿箭头，图中实为白色实线 / 虚线箭头', '“ULT 部分纤维附着 MH”：ULT 未定义，应为 UTL', 'MH 附着 90% / 10% 两组都附着三角骨，表述不清']),
    ('box', '文献', 'Winnett C, Fenech M. Sonographic Anatomy and Imaging of the TFCC and the DRUJ. Australas J Ultrasound Med. 2025;28:e70012.\nCC BY 4.0，原图引自原文，编者加中文标注', 'grey')])
deck.save(OUT)
