#!/usr/bin/env python3
"""Qazi 等 2021《Distal Radioulnar Joint Instability and Associated Injuries: A Literature Review》→ 小红书 3:4 图文卡片。
原文非开放获取（© Society of Indian Hand & Microsurgeons，All rights reserved）：原图只按面板裁切（tools/crop.py）、不改动图像；
图中英文和箭头含义写在卡片文字里。用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
WORK, FONTS, OUT = sys.argv[1:4]
P = lambda x: Image.open(os.path.join(WORK, f'{x}.jpg')).convert('RGB')
def grid(*ims, gap=10, W=1400, ncol=2):
    rows = [ims[i:i + ncol] for i in range(0, len(ims), ncol)]; out = []
    for r in rows:
        h = round((W - gap * (len(r) - 1)) / sum(i.width / i.height for i in r)) if len(r) > 1 else round(min(W * .7 * r[0].height / r[0].width, r[0].height * 1.6))
        out.append([i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in r])
    c = Image.new('RGB', (W, sum(r[0].height for r in out) + gap * (len(out) - 1)), 'white'); y = 0
    for r in out:
        x = (W - sum(i.width for i in r) - gap * (len(r) - 1)) // 2
        for i in r: c.paste(i, (x, y)); x += i.width + gap
        y += r[0].height + gap
    return c
d = Deck(series='手腕康复', source='Qazi 等 · J Hand Microsurg 2021;13(3):123-131', fonts_dir=FONTS)
d.cover(['下尺桡关节（DRUJ）不稳', '怎么查、怎么想'], kicker='J Hand Microsurg 2021 · 文献综述',
        subtitle='解剖、7 个查体试验、影像与 5 类合并损伤', photos=[(P('f4a'), '前后应力试验（原文图 4A）'), (P('f8'), '琴键征（原文图 8）')], banner='学习笔记 · 仅供学习交流')
d.text('先说结论', '原文要点', [
    ('box', '容易漏', 'DRUJ 不稳常继发于其他上肢损伤，**初诊时易被忽视**；慢性不稳 → 疼痛、功能障碍、关节炎', 'navy'),
    ('box', '稳定靠软组织', '骨性结构只占约 **20%**；其余靠 TFCC（桡尺韧带）、关节囊、骨间膜、ECU 腱鞘、旋前方肌', 'teal'),
    ('box', '这些伤要想到 DRUJ', '桡骨远端骨折、尺骨茎突基底骨折、乙状切迹 / 尺侧角骨折、Galeazzi、Essex-Lopresti', 'accent'),
    ('box', '治疗总原则', '先复位固定骨折 → 再测 DRUJ；多数最稳体位制动 **4–6 周**即可', 'yellow')])
d.text('① 解剖与生物力学：几个数字', '据原文整理', [
    ('steps', [('150–180°', 'DRUJ 总旋转弧（桡腕关节另有约 30°）'), ('80% / 20%', '腕部负荷经桡骨 / 尺骨传导'),
               ('2 mm', '旋前旋后极限时乙状切迹边缘接触仅约 2 mm，<10% 关节面'), ('20%', '骨性结构对稳定的贡献')]),
    ('box', '关节类型', '乙状切迹与尺骨头之间**不完全匹配**的滑膜关节，是前臂旋转的支点；以旋转为主，伴轴向和平移运动', 'teal')])
d.figure('② DRUJ 解剖', '原文图 1', P('f1'), None, [
    ('bul', ['Scaphoid 舟骨 · Lunate 月骨 · Triquetrum 三角骨', 'Ulnolunate / Ulnotriquetral Ligament 尺月 / 尺三角韧带', 'Ulnar Collateral Ligament 尺侧副韧带',
             'Volar / Dorsal Radioulnar Ligament 掌侧 / 背侧桡尺韧带', 'Articular Disc 关节盘 · ECU Sheath / Tendon 尺侧腕伸肌腱鞘 / 肌腱'])], max_h=720)
d.figure('③ 乙状切迹的 4 种形状', '原文图 2 · Tolat 等 50 例尸体', P('f2'), None, [
    ('steps', [('a', '“C”型 30%'), ('b', '“S”型 14%'), ('c', '平面型 flat face 42%'), ('d', '滑雪坡型 ski slope 14%')]),
    ('box', '临床意义', '**平坦型**可能更易不稳，单纯修软组织效果更差', 'accent')], max_h=640)
d.figure('④ 主要稳定结构：桡尺韧带', '原文图 3（水平面观）', P('f3'), None, [
    ('box', '两层', '深层（近端）止于**尺骨小凹**；浅层（远端）止于茎突基底和中部', 'navy'),
    ('steps', [('旋前', '背侧浅层 + 掌侧深层紧张'), ('旋后', '掌侧浅层 + 背侧深层紧张')]),
    ('box', '次要稳定', '旋前方肌深头、骨间膜、ECU 腱鞘、尺腕韧带', 'teal')], max_h=620)
d.figure('⑤ 前后应力试验 + 分级', '原文图 4 A–C、表 1（Seo 等）', grid(P('f4a'), P('f4b'), P('f4c'), ncol=3), None, [
    ('steps', [('A', '前臂中立，固定桡骨，尺骨远端掌背侧推移（双箭头）'), ('B', '桡骨–腕骨拉向自己，尺骨向掌侧推'), ('C', '桡骨–腕骨背侧拉向自己，尺骨向背侧推')]),
    ('bul', ['0 级 正常　1 级 松弛增加、无症状', '2 级 平移增加、诱发症状、无坚实终末感', '3 级 主动旋转时半脱位'])], max_h=560)
d.figure('⑥ 尺骨小凹征', '原文图 5', P('f5'), None, [
    ('steps', [('体位', '屈肘 90°，腕和前臂中立位'), ('做法', '拇指尖深压尺骨小凹（**黑箭头**）：茎突与尺侧腕屈肌腱之间的“软点”')]),
    ('box', '阳性', '压痛，提示 TFCC 损伤；敏感度 **95.2%**', 'accent')], max_h=760)
d.figure('⑦ TFCC 应力试验 · 尺腕应力试验', '原文图 6（左）、图 7（右）', grid(P('f6'), P('f7'), ncol=2), None, [
    ('box', '图 6 TFCC 应力试验', '被动尺偏腕关节，痛即阳性', 'navy'),
    ('box', '图 7 尺腕应力试验', '腕最大尺偏 + 轴向压，同时被动旋前–旋后（**箭头**）；尺侧腕痛为阳性', 'teal')], max_h=700)
d.figure('⑧ 琴键征 · 按压试验', '原文图 8', P('f8'), None, [
    ('box', '琴键征', '掌心平放、腕完全旋前，在尺骨远端（**红点**）由背向掌加压；DRUJ 处痛、尺骨较健侧松动为阳性', 'navy'),
    ('box', '按压试验（无配图）', '双手撑椅起立，尺侧腕局灶痛为阳性；Lester 等报告敏感度 **100%**', 'accent')], max_h=660)
d.figure('⑨ 双侧试验（Hahn 等）', '原文图 9：左 A 旋前，右 B 旋后', grid(P('f9a'), P('f9b'), ncol=2), None, [
    ('steps', [('体位', '坐位，屈肘 90°、肩内收'), ('做法', '示指放 DRUJ、中指放尺骨头，双腕旋前→旋后反复转动'), ('数据', '20 例，与 CT 对照敏感度 **90%**')]),
    ('box', '看什么', '直接观察尺骨头在旋转中的动态表现，同时检查 DRUJ 的静态稳定性', 'teal')], max_h=700)
d.text('⑩ X 线怎么看', '据原文整理', [
    ('box', '标准位', '真正后前位 + 侧位（前臂、腕、肘）；肩外展 90°、腕中立测尺骨变异；**拍健侧对比**', 'navy'),
    ('box', '正位', '背侧脱位：间隙增宽、桡尺分离；掌侧脱位：桡尺重叠', 'teal'),
    ('box', '侧位的坑', '旋转偏 10° 半脱位就可能“看起来复位”；真侧位：豌豆骨掌侧面在舟骨远极与头状骨之间', 'accent'),
    ('box', '加重应力侧位', '前臂旋前搭桌缘，手持 3–5 磅重物拍侧位', 'yellow'),
    ('bul', ['茎突基底骨折 / 茎突移位 >2 mm', 'DRF 背倾 >20°', '乙状切迹撕脱骨折'])])
d.figure('⑪ CT：三种判断方法', '原文图 10（U 尺骨，R 桡骨；Dorsal 背侧，Volar 掌侧）', grid(P('f10a'), P('f10b'), P('f10c'), ncol=3), None, [
    ('steps', [('a Mino 法', '桡骨掌侧缘、背侧缘各画线，尺骨头应在两线之间'), ('b 桡尺比 RUR', 'AB:AC；Lo 等认为优于其他方法'), ('c 半脱位比', '尺骨头超出垂线的距离 / 乙状切迹长度；信度最好（Park 和 Kim）')]),
    ('box', 'MRI 与关节镜', '3T + 关节内造影；腕牵引后 TFCC 检出准确率 83%→98%；**关节镜是金标准**', 'teal')], max_h=420)
d.text('⑫ 单纯急性 DRUJ 脱位', '据原文整理', [
    ('steps', [('背侧脱位', '过度旋前 + 伸展；手固定于旋前、不能旋后，尺骨头背侧隆起'), ('掌侧脱位', '过度旋后；不能旋前，掌侧可触及尺骨头')]),
    ('box', '复位', '局麻 ± 镇静，压住尺骨远端，强力旋后 / 旋前；复杂脱位可卡入 ECU、示指伸肌腱、TFCC、EDM', 'navy'),
    ('box', '复位后', '背侧脱位**旋后位**最稳，掌侧脱位**旋前位**最稳；仍不稳 → 双克氏针桡尺固定或修 TFCC', 'teal'),
    ('box', '制动', '最稳体位石膏 4 周 → 4–6 周后可拆支具、逐步主动活动', 'accent')])
d.text('⑬ 桡骨远端骨折 · 尺骨茎突骨折', '据原文整理', [
    ('steps', [('43%', 'Geissler：关节面台阶 >2 mm 者 TFCC 损伤'), ('84% / 37%', 'Lindau：TFCC 损伤 / 12 个月时 DRUJ 不稳'), ('61%', 'Frykman：DRF 合并尺骨茎突骨折')]),
    ('box', 'DRF', '固定后术中测 DRUJ；良好复位最关键。仍不稳：修茎突 / TFCC、桡尺穿针或延长制动；Kim 等加 4 周糖钳夹板，疗效无差异', 'navy'),
    ('box', '茎突骨折', '**基底骨折**风险高；先固定 DRF → 稳定则保守，不稳则固定茎突 → 仍不稳修 TFCC 小凹止点', 'accent')])
d.text('⑭ Galeazzi 与 Essex-Lopresti', '据原文整理', [
    ('box', 'Galeazzi 骨折', '桡骨干骨折 + DRUJ 脱位；几乎都有 1B 型 TFCC 损伤；距关节面 **7.5 cm** 内更易伤 DRUJ；ECU 腱最常阻挡复位', 'navy'),
    ('box', '→ “必须手术”', '保守时旋前方肌、肱桡肌等牵拉骨块；桡骨 ORIF 后测 DRUJ：稳定 → 早期活动，不稳 → 同 DRF 流程', 'teal'),
    ('box', 'Essex-Lopresti', '桡骨头粉碎骨折 + DRUJ 脱位 + 骨间膜撕裂；桡骨牵拉试验 9.1 kg：近移 **≥3 mm** 提示桡骨头 + 骨间膜断裂，**>6 mm** 再加 TFCC', 'accent'),
    ('box', '→ 越早越好', '桡骨头 ORIF / 置换；一周内治疗 10 例中 9 例满意，超过一周 14 例中仅 4 例；长臂固定防旋转 4–6 周', 'yellow')])
d.rows('⑮ 查体速查', '编者据原文整理', [
    ('前后应力试验', '固定桡骨，推移尺骨；与健侧比', 'Seo 0–3 级', 'navy'),
    ('尺骨小凹征', '屈肘 90°，深压尺骨小凹', '敏感度 95.2%', 'teal'),
    ('TFCC / 尺腕应力试验', '被动尺偏；尺偏 + 轴向压 + 旋转', '尺侧腕痛', 'accent'),
    ('按压试验 · 琴键征', '撑椅起立；尺骨背→掌侧加压', '按压试验敏感度 100%', 'yellow'),
    ('双侧试验', '双手旋前→旋后摸尺骨头', '敏感度 90%（20 例）', 'grey')],
    note='所有检查都要和健侧对比；急性背侧脱位旋后受阻、掌侧脱位旋前受阻')
d.text('收藏 + 原文细节', '据原文整理', [
    ('h', '原文对不上的地方'),
    ('bul', ['尺骨小凹征：正文写“从**桡侧**托腕”，图 5 注写“从**背侧**托手”；小凹位置描述也不同', '琴键征：正文写**前臂中立**、腕伸 20–30°，图 8 注写**完全旋前**',
             '“单纯 TFCC 损伤不会导致 incomplete instability”，按上下文应为 complete，疑笔误']),
    ('box', '文献与版权', 'Qazi S, et al. J Hand Microsurg. 2021;13(3):123-131. © Society of Indian Hand & Microsurgeons，非开放获取；原图未改动\n仅供学习交流，如有侵权请联系删除', 'grey')])
d.save(OUT)
