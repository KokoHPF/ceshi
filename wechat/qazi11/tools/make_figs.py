#!/usr/bin/env python3
"""Qazi 等 2021《Distal Radioulnar Joint Instability and Associated Injuries: A Literature Review》(J Hand Microsurg 13:123-131) 推文配图。
原文非开放获取（© Society of Indian Hand & Microsurgeons，All rights reserved）：原文图只按面板裁切（tools/crop.py），不改动图像，
中文说明写在图上方的图注里；表 1 由编者中译重绘。用法：python3 tools/make_figs.py work images <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
from PIL import Image, ImageDraw
WORK, OUT, FM, FBOLD = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
k = Kit(WORK, OUT, FBOLD)
B, O, G, P = TEAL, (200, 120, 0), (0, 120, 60), RED
n = 1
def nxt(im):
    global n; k.save(im, n); n += 1
def capbox(im, cap, W=1200):
    """图注在图上方（支持 \\n 分段），原图不做任何改动"""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS); segs = cap.split('\n')
    dd = ImageDraw.Draw(Image.new('RGB', (W, 3000))); y = 14
    for s_ in segs: y = k.para(dd, 14, y, s_, 28, W - 30, gap=12)
    hh = y + 4; t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); y = 14
    for i, s_ in enumerate(segs): y = k.para(dr, 14, y, s_, 28, W - 30, fill=TEAL if i == 0 else INK, gap=12)
    t.paste(im, (0, hh + 8)); return t
def row(names, gap=16, H=None):
    ims = [k.op(f'{x}.jpg') for x in names]; H = H or max(i.height for i in ims)
    ims = [i.resize((round(i.width * H / i.height), H), Image.LANCZOS) for i in ims]
    c = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), H), 'white'); x = 0
    for i in ims: c.paste(i, (x, 0)); x += i.width + gap
    return c
def put(f, cap): nxt(capbox(k.op(f + '.jpg') if isinstance(f, str) else f, cap))
def card(t, items): nxt(k.card(t, items))

nxt(k.title('文献综述 · J Hand Microsurg 2021', ['下尺桡关节（DRUJ）不稳', '解剖、查体、影像与合并损伤'],
            'Sohail Qazi, David Graham, Steven Regal, Peter Tang, Jon E. Hammarstedt', 'J Hand Microsurg. 2021;13(3):123-131. doi:10.1055/s-0041-1730886',
            'Temple University Hospital / Allegheny General Hospital（美国）'))                              # 1
card('先说结论（原文要点）', [
    ('容易漏', 'DRUJ 不稳常继发于其他上肢损伤，初诊时容易被忽视；慢性不稳会带来疼痛、功能障碍和关节炎', LT, B),
    ('稳定靠软组织', '骨性结构只提供约 20% 的稳定性，其余靠 TFCC（尤其是桡尺韧带）、关节囊、骨间膜、尺侧腕伸肌腱鞘和旋前方肌', OR, O),
    ('查体要双侧对比', '前后应力试验、尺骨小凹征、TFCC 应力试验、尺腕应力试验、按压试验、琴键征、双侧试验', GR, G),
    ('这些损伤要想到 DRUJ', '桡骨远端骨折、尺骨茎突基底骨折、乙状切迹 / 尺侧角骨折、Galeazzi 骨折、Essex-Lopresti 损伤', PK, P),
    ('治疗总原则', '先把骨折复位固定好，再测 DRUJ 稳定性；多数在最稳定体位制动 4–6 周即可，仍不稳再修 TFCC、固定茎突或穿针', LT, B),
])                                                                                                       # 2
card('DRUJ 解剖与生物力学：几个数字', [
    ('关节类型', '桡骨远端乙状切迹与尺骨头之间、不完全匹配的滑膜关节，是前臂旋前–旋后的支点', LT, B),
    ('活动度', 'DRUJ 总旋转弧 150–180°，桡腕关节再提供约 30°；以旋转为主，伴轴向和平移运动', OR, O),
    ('负荷分配', '正常腕部约 80% 的力经桡骨传导，20% 经尺骨；随尺偏 / 桡偏变化', GR, G),
    ('接触面', '旋前、旋后极限时，乙状切迹边缘可能只有约 2 mm 接触，不到关节面积的 10%', PK, P),
    ('骨性稳定', '骨性结构只贡献约 20% 的稳定性', LT, B),
])                                                                                                       # 3
put('f1', '原文图 1  DRUJ 解剖\n图中英文：Scaphoid 舟骨，Lunate 月骨，Triquetrum 三角骨，Ulnolunate Ligament 尺月韧带，Ulnotriquetral Ligament 尺三角韧带，Ulnar Collateral Ligament 尺侧副韧带，Volar / Dorsal Radioulnar Ligament 掌侧 / 背侧桡尺韧带，Articular Disc 关节盘，ECU Sheath / Tendon 尺侧腕伸肌腱鞘 / 肌腱，Radius 桡骨，Ulna 尺骨')  # 4
put('f2', '原文图 2  乙状切迹的 4 种形状（Tolat 等 50 例尸体研究）\na “C”型（30%）　b “S”型（14%）　c 平面型 flat face（42%）　d 滑雪坡型 ski slope（14%）\n平坦的乙状切迹可能更容易不稳，单纯软组织修复的效果也更差')  # 5
put('f3', '原文图 3  深层与浅层桡尺韧带（水平面观）\n图中英文：Superficial / Deep Volar Radioulnar Ligament 浅层 / 深层掌侧桡尺韧带，Superficial / Deep Dorsal Radioulnar Ligament 浅层 / 深层背侧桡尺韧带，Ulnar Styloid 尺骨茎突')  # 6
card('谁在稳定 DRUJ', [
    ('主要稳定结构：桡尺韧带', '起于乙状切迹掌侧、背侧缘，呈三角形汇聚止于尺骨；冠状面分两束：深层（近端）止于尺骨小凹，浅层（远端）止于茎突基底和中部', LT, B),
    ('旋前时', '背侧浅层纤维 + 掌侧深层纤维紧张', OR, O),
    ('旋后时', '掌侧浅层纤维 + 背侧深层纤维紧张', OR, O),
    ('次要稳定结构', '旋前方肌深头（主动旋前、被动旋后时使关节面加压贴合）、骨间膜（IOM）、ECU 腱鞘、尺腕韧带', GR, G),
    ('两个“不会”', '骨间膜完好时不会发生完全的桡尺分离；单纯 TFCC 损伤而关节囊完好或已修复时，DRUJ 运动学能明显恢复', PK, P),
])                                                                                                       # 7
put(row(['f4a', 'f4b', 'f4c']), '原文图 4  DRUJ 前后应力试验（左起 A、B、C）\n体位：肘放在桌面上，手指向天花板，与健侧对比\nA 前臂中立位：固定桡骨，把尺骨远端向掌侧、背侧推移，看平移量（双箭头）\nB 检查者把桡骨–腕骨拉向自己，同时把尺骨远端向掌侧推（推向患者）\nC 检查者把桡骨–腕骨背侧拉向自己，同时把尺骨远端向背侧推（推向患者）\n看终末感是否坚实、是否诱发疼痛')  # 8
card('急性脱位 vs 慢性不稳：怎么看', [
    ('尺骨背侧脱位', '腕背尺侧隆起，旋后受阻', LT, B),
    ('尺骨掌侧脱位', '腕掌尺侧隆起，旋前受阻', OR, O),
    ('弹响', '主动、被动旋前旋后时可有可闻 / 可触的弹响；尺骨头明显半脱位即提示 DRUJ 不稳', GR, G),
    ('前后应力试验分级（Seo 等，原文表 1）', '0 级：稳定性正常\n1 级：松弛度增加，无临床症状\n2 级：平移增加，诱发症状，无坚实终末感\n3 级：主动旋转前臂时出现半脱位', PK, P),
])                                                                                                       # 9
put('f5', '原文图 5  尺骨小凹征（ulnar fovea sign）\n屈肘 90°，腕和前臂中立位；检查者一手托住患者的手，另一手拇指尖深压尺骨小凹——尺骨茎突与尺侧腕屈肌腱之间的“软点”\n压痛为阳性，提示 TFCC 损伤，敏感度 95.2%')  # 10
put(row(['f6', 'f7']), '原文图 6（左）  TFCC 应力试验：被动尺偏腕关节，诱发疼痛为阳性\n原文图 7（右）  尺腕应力试验：腕最大尺偏，双手施加轴向应力，同时被动旋前–旋后（箭头）；把 TFCC 夹在月骨 / 三角骨与尺骨远端之间研磨，尺侧腕痛为阳性')  # 11
put('f8', '原文图 8  琴键征（piano key sign）\n掌心平放桌面、腕完全旋前，在尺骨远端由背侧向掌侧加压（红点）；DRUJ 水平疼痛、尺骨活动（与对侧比较松弛）为阳性\n也可让患者自己把尺骨压向桌面\n正文另写：前臂中立、腕伸 20–30°，一手固定桡骨，另一手抓尺骨加压')  # 12
put(row(['f9a', 'f9b']), '原文图 9  双侧试验（bilateral test，Hahn 等）\n坐位，屈肘 90°、肩内收；检查者双手示指放在 DRUJ、中指放在尺骨头上，让双腕从旋前（左 A）到旋后（右 B）反复转动，诱发潜在半脱位\n20 例中，与 CT 对照的敏感度 90%')  # 13
card('另一个简单试验：按压试验（press test）', [
    ('做法', '患者双手撑椅子从坐位站起，使尺侧腕部承受轴向负荷', LT, B),
    ('阳性', '尺侧腕部局灶性疼痛', OR, O),
    ('数据', 'Lester 等报告其检出 TFCC 撕裂的敏感度为 100%', GR, G),
])                                                                                                       # 14
card('影像（一）：X 线', [
    ('标准位', '患侧前臂、腕、肘的真正后前位 + 侧位；肩外展 90°、腕中立旋转位拍腕，测尺骨变异；怀疑时拍健侧对比', LT, B),
    ('正位怎么看', '背侧脱位：DRUJ 间隙增宽，桡尺骨分离\n掌侧脱位：旋前方肌牵拉，桡尺骨在 DRUJ 水平重叠', OR, O),
    ('侧位的坑', '侧位片只要旋前 / 旋后偏 10°，半脱位就可能看起来“已复位”、脱位看起来像“半脱位”\n判断真侧位：豌豆骨掌侧面位于舟骨远极和头状骨掌侧面中间', PK, P),
    ('加重应力侧位', '屈肘 90°、前臂完全旋前搭在桌缘，手持 3–5 磅（约 1.4–2.3 kg）重物，拍水平侧位', GR, G),
    ('提示 DRUJ 损伤的征象', '尺骨茎突基底骨折；茎突骨折移位 >2 mm；桡骨远端骨折背倾 >20°；乙状切迹撕脱骨折', LT, B),
])                                                                                                       # 15
put(row(['f10a', 'f10b', 'f10c']), '原文图 10  CT 判断 DRUJ 是否匹配的三种方法（U 尺骨，R 桡骨；Dorsal 背侧，Volar 掌侧）\na Mino 法：经桡骨掌侧尺 / 桡缘画一条线，经背侧尺 / 桡缘再画一条线；稳定时尺骨头位于两线之间\nb 桡尺比（RUR）：用同心圆找尺骨头中心，连乙状切迹背侧、掌侧缘，再向尺骨头中心作垂线；AB:AC 即 RUR\nc 半脱位比：从乙状切迹掌侧、背侧缘作垂线，量尺骨头超出两线的距离，与乙状切迹长度相比')  # 16
card('影像（二）：CT、MRI 与关节镜', [
    ('CT', '临床怀疑即可做；Lo 等认为 RUR 优于 Mino 法、中心法和匹配法；Park 和 Kim 发现半脱位比的观察者内 / 间信度最好', LT, B),
    ('MRI', '评估软组织稳定结构，但敏感度和特异度不一；推荐 3T 高分辨率 + 关节内造影', OR, O),
    ('腕牵引', '40 腕前瞻研究：牵引后撕裂检出准确率 TFCC 83%→98%，月三角韧带 88%→100%，舟月韧带 95%→100%', GR, G),
    ('金标准', '关节镜仍是评估 TFCC 病变的金标准，比影像更敏感、更准确', PK, P),
])                                                                                                       # 17
card('单纯急性 DRUJ 脱位', [
    ('表现', '少见；多为背侧脱位，过度旋前 + 伸展受伤，手固定在旋前位、不能旋后，尺骨头背侧隆起\n掌侧脱位多为过度旋后，不能旋前，掌侧可触及尺骨头、背侧凹陷', LT, B),
    ('复位', '局麻 ± 镇静闭合复位：压住尺骨远端，对突出的尺骨强力旋后 / 旋前\n复杂脱位可能卡入 ECU、示指伸肌腱、TFCC 或小指伸肌（EDM）', OR, O),
    ('复位后', '背侧脱位旋后位最稳，掌侧脱位旋前位最稳\n仍不稳：在最稳体位用两枚克氏针桡尺固定（关节近端、两端略外露便于取出），或开放 / 关节镜修 TFCC', GR, G),
    ('制动', '最稳体位石膏 4 周，定期拍片；4–6 周后改可拆支具，逐步主动活动', PK, P),
])                                                                                                       # 18
card('桡骨远端骨折（DRF）与 DRUJ 不稳', [
    ('有多常见', 'Geissler：60 例关节面台阶 >2 mm，43% 有 TFCC 损伤\nLindau：51 例移位 DRF，84% 有 TFCC 损伤，中位随访 12 个月时 37% DRUJ 不稳\nMay：130 例 DRF，11% 合并急 / 慢性 DRUJ 不稳', LT, B),
    ('危险因素', '初始 DRUJ 大幅移位、严重桡骨短缩；最重要的保护因素是良好复位和对线', OR, O),
    ('怎么判断', '骨折固定后术中测 DRUJ 稳定性', GR, G),
    ('仍不稳怎么办', '尺骨茎突修复、延长制动、关节镜 / 开放修 TFCC，或加桡尺穿针，或单纯穿针；复位不良者固定乙状切迹 / 尺侧角骨折块', PK, P),
    ('保守也行', 'Kim 等 84 例：术中松弛者加 4 周糖钳夹板，12 个月功能和疼痛与稳定组无差异', LT, B),
])                                                                                                       # 19
card('尺骨茎突骨折', [
    ('发生率', 'Frykman：约 61% 的 DRF 合并尺骨茎突骨折，多数与 DRUJ 不稳无关', LT, B),
    ('高危', '经茎突基底的骨折；侧位片茎突位于尺骨干轴线掌侧时，要怀疑 DRUJ 稳定性受损', OR, O),
    ('流程', '先固定 DRF → 测 DRUJ\n稳定：茎突保守治疗\n不稳：固定茎突（克氏针、张力带、加压螺钉、微型钢板、缝合锚）\n仍不稳：关节镜或开放修复 TFCC 小凹止点（可能是茎突旁的独立撕脱骨块）', GR, G),
])                                                                                                       # 20
card('Galeazzi 骨折', [
    ('定义', '桡骨干骨折 + DRUJ 脱位；多为高能量损伤，腕过伸、旋前位受力；几乎都有 1B 型 TFCC 损伤', LT, B),
    ('7.5 cm', '骨折距桡骨关节面中点 7.5 cm 以内时，DRUJ 损伤发生率更高', OR, O),
    ('复位阻挡', '最常见是 ECU 腱，也可为 EDM 腱、示指伸肌腱或骨块', GR, G),
    ('“必须手术的骨折”', '保守效果差：旋前方肌、肱桡肌、拇长伸 / 展肌牵拉远端骨块；至少要桡骨切开复位内固定，然后测 DRUJ：稳定 → 制动后早期活动；不稳 → 同 DRF 合并不稳的处理', PK, P),
])                                                                                                       # 21
card('Essex-Lopresti 损伤', [
    ('定义', '桡骨头粉碎骨折 + DRUJ 脱位 + 骨间膜撕裂；轴向压力导致桡骨向近端移位、尺骨撞击腕骨', LT, B),
    ('查体', '尺骨背侧突出、骨间膜压痛、腕伸受限、旋前旋后受限；肘和 DRUJ 都要查', OR, O),
    ('影像', '肘、前臂、腕正侧位，留意尺骨变异\n桡骨牵拉试验（9.1 kg）：桡骨头 + 骨间膜断裂时近移 ≥3 mm；再加 TFCC 断裂时 >6 mm', GR, G),
    ('治疗', '桡骨头 ORIF 或置换（置换相当于内夹板，让骨间膜和 TFCC 愈合）；一周内早治疗：10 例中 9 例满意，超过一周仅 14 例中 4 例\n之后测 DRUJ，不稳则修 TFCC；长臂支具 / 石膏防旋转 4–6 周', PK, P),
])                                                                                                       # 22
card('原文对不上的地方（编者核对）', [
    ('尺骨小凹征的做法', '正文：一手从桡侧托住腕，小凹是“尺骨头远端、腕尺侧的软点”\n图 5 注：一手从背侧托住手，小凹在“尺骨茎突与尺侧腕屈肌腱之间”', OR, O),
    ('琴键征的体位', '正文：前臂中立位、掌心放桌上并旋前，腕伸 20–30°\n图 8 注：掌心平放、腕完全旋前，没提伸腕角度', LT, B),
    ('“不完全不稳”', '原文写“单纯 TFCC 损伤不会导致 incomplete instability”，结合上下文（骨间膜完好时不会完全分离）应为“complete instability”，疑为笔误', PK, P),
])                                                                                                       # 23
im = k.op('f3.jpg'); w = im.width; h = round(w * 383 / 900); y0 = max(0, (im.height - h) // 2)
im.crop((0, y0, w, y0 + h)).resize((900, 383), Image.LANCZOS).save(f'{OUT}/cover.jpg', quality=90)
print('ok', n - 1)
