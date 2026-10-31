#!/usr/bin/env python3
"""Yubran 等 2024 Insights into Imaging《肩袖撕裂类型：MRI 表现及其手术意义》→ 小红书 3:4 图文卡片。
原文 CC BY 4.0：用编者中文标注版原图 work/f*.jpg（先运行 tools/make_figs.py 生成），按面板裁切放大。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='肩关节影像', source='Insights Imaging 2024;15:61', fonts_dir=FONTS)
F = lambda i, box=None: (lambda im: im.crop(box) if box else im)(Image.open(os.path.join(WORK, f'f{i:02d}.jpg')).convert('RGB'))

deck.cover(['肩袖撕裂', '有哪些类型？', 'MRI 一次看懂'], kicker='Insights into Imaging 2024 · 教学综述',
           subtitle='部分、全层、分层、肩胛下肌撕裂与脂肪浸润', photos=[(F(11, (0, 492, 1418, 961)), '全层撕裂三种形态（原文图 11）')], banner='24 张 MRI + 关节镜对照图')
deck.text('先说结论', '原文要点', [
    ('box', '没有统一分型', '推荐按 **ISAKOS** 描述：位置、范围、形态、回缩、脂肪萎缩', 'navy'),
    ('box', '新类型要单独写', '分层撕裂、肌腱连接处撕裂、Fosbury flop 不在 ISAKOS 里', 'yellow'),
    ('box', '最难判断', '全层撕裂的**形态**（新月形、U 形、L 形）——决定怎么修', 'accent'),
    ('box', '预后关键', '**脂肪浸润**不可逆，决定手术结构和功能结局', 'teal')])
deck.figure('① 冈上肌分前、后两腹', '原文图 1（编者中文标注）', [F(1, (0, 0, 960, 518)), F(1, (0, 543, 960, 1499))], None, [
    ('box', '为什么前腹更容易伤', '前腹粗大、羽状、有肌内长腱，收缩力强；但两腹腱横截面积比仅 0.9∶1 → 前腹应力集中', 'accent')], stack=True, max_h=760)
deck.figure('② 五层结构', '原文图 3a（编者中文标注）', F(3, (0, 0, 752, 751)), None, [
    ('steps', [('1', '喙肱韧带浅层'), ('2', '致密平行胶原（滑囊侧）：弹性好、血供好、抗撕裂'), ('3', '细而杂乱的胶原（关节侧）：无弹性、血供差、**易撕裂**'),
               ('4', '肩袖索：“吊桥”分散新月区负荷'), ('5', '关节囊')])], max_h=560)
deck.figure('③ 肩袖索与新月区', '原文图 4（编者中文标注）', [F(4, (0, 839, 865, 1702)), F(4, (0, 1719, 865, 2481))], None, [
    ('box', '要点', '新月区在肩袖索外侧，特别容易撕裂；肩袖索还能限制撕裂后回缩', 'teal')], max_h=640)
deck.text('④ ISAKOS 分型', '原文表 1', [
    ('box', '部分撕裂（后上方）', '位置：关节侧 / 滑囊侧 / 腱内\n范围：<50% 或 >50% 腱厚', 'teal'),
    ('box', '全层撕裂（后上方）', '范围 C1–C4 · 形态 新月形 / U / L / 反 L · 回缩 1–3 级', 'navy'),
    ('box', '前方（肩胛下肌）', 'Lafosse 1～5 型', 'yellow'),
    ('box', '脂肪萎缩', '冈上 SS0–4、冈下 IS0–4、肩胛下 SSC0–4', 'grey')])
deck.figure('⑤ 部分撕裂：关节侧 vs 滑囊侧', '原文图 6b、图 8b（编者中文标注）', [F(6, (0, 728, 894, 1621)), F(8, (0, 736, 894, 1571))], None, [
    ('box', '关节侧（左）', '最常见，占全部撕裂 15%～60%；ABER 体位关节造影更易显示', 'teal'),
    ('box', '滑囊侧（右）', '约占部分撕裂 18%；几乎不能自愈，往往比全层还痛', 'accent'),
    ('box', '>50% 腱厚', '高级别：**55%** 进展为全层（低级别 14%）', 'yellow')], max_h=500)
deck.figure('⑥ 全层撕裂的形态', '原文图 11（编者中文标注）', [F(11, (0, 0, 1418, 483)), F(11, (0, 492, 1418, 961))], None, [
    ('box', 'MRI 技巧', 'L 形：斜冠状位裂口更宽\n新月形、U 形：斜矢状位更宽', 'teal'),
    ('box', '怎么修', '新月形直接固定；U、L 形先边缘汇聚成新月形再固定', 'navy')], stack=True, max_h=600)
deck.figure('⑦ 范围：Snyder C1–C4', '原文图 12（编者中文标注）', [F(12, (0, 0, 940, 506)), F(12, (940, 0, 1946, 506))], None, [
    ('steps', [('C1', '针孔样小撕裂'), ('C2', '<2 cm、单腱、无明显回缩'), ('C3', '大撕裂、回缩 3～4 cm、单腱'), ('C4', '两条及以上肌腱')])], stack=True, max_h=820)
deck.figure('⑧ 回缩：Patte Ⅰ–Ⅲ', '原文图 13（编者中文标注）', [F(13, (0, 0, 1293, 643)), F(13, (1302, 0, 1946, 643))], None, [
    ('steps', [('Ⅰ', '轻度回缩'), ('Ⅱ', '回缩到肱骨头顶点'), ('Ⅲ', '回缩到关节盂上缘或更内侧')]),
    ('box', '意义', '回缩越多，预后越差', 'accent')], stack=True, max_h=860)
deck.figure('⑨ 分层撕裂', '原文图 15（编者中文标注）', [F(15, (0, 0, 1418, 501)), F(15, (0, 508, 1418, 1027))], None, [
    ('box', '要点', '关节层和滑囊层被水平劈开；占全部撕裂 38%～82%\n降低肌腱质量、影响愈合 → 两层需**分别修复**', 'accent')], stack=True, max_h=820)
deck.figure('⑩ Fosbury flop 与肌腱连接处撕裂', '原文图 17c、图 18b（编者中文标注）', [F(17, (0, 1632, 718, 2481)), F(18, (0, 644, 894, 1392))], None, [
    ('box', 'Fosbury flop', '全层撕裂残端向上后翻折、贴在滑囊侧', 'teal'),
    ('box', '肌腱连接处撕裂', '30～50 岁、外伤后，多为冈上肌前腹；Ⅲ 级完全断裂后迅速萎缩和脂肪浸润', 'accent')], max_h=520)
deck.figure('⑪ 肩胛下肌撕裂（Lafosse）', '原文图 19（编者中文标注）', [F(19, (0, 0, 1418, 476)), F(19, (0, 484, 1418, 953))], None, [
    ('steps', [('1 型', '上 1/3 部分撕裂'), ('2 型', '上 1/3 全层'), ('3 型', '上、中 1/3'), ('4 型', '全腱撕裂，肱骨头居中'), ('5 型', '4 型 + 肱骨头前半脱位、脂肪浸润 ≥3 级')])], stack=True, max_h=760)
deck.figure('⑫ 脂肪浸润：Goutallier 0–4 级', '原文图 23（编者中文标注）', [F(23, (0, 0, 1946, 713)), F(23, (320, 719, 1650, 1454))], None, [
    ('box', '要点', '喙突水平斜矢状位 T1 评估；**不可逆**，修复后也不会减少\n0 正常 · 1 条纹 · 2 <50% · 3 约 50% · 4 >50%', 'accent')], stack=True, max_h=900)
deck.figure('⑬ 肩袖关节病：Hamada 分期', '原文图 24（编者中文标注）', [F(24, (0, 0, 1418, 488)), F(24, (0, 493, 1418, 974))], None, [
    ('box', '治疗选择', '高需求 + Hamada Ⅰ～Ⅲ：挽救手术（补片、上关节囊重建、肌腱转位、球囊）\n低需求 + Ⅳ/Ⅴ：关节置换', 'navy')], stack=True, max_h=820)
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('50%', '部分撕裂高/低级别分界'), ('55% / 14%', '高/低级别进展为全层'), ('38%～82%', '分层撕裂占比'), ('20%～37%', '肩胛下肌撕裂发生率'), ('5 mm', 'Hamada 肩肱间距分界')]),
    ('h', '原文对不上的地方'),
    ('bul', ['Snyder：C2 <2 cm、C3 3～4 cm，2～3 cm 无归属', 'Lafosse 4 型 ≤3 级、5 型 ≥3 级，3 级两边都算', '原文图 4 图注出现两个“b”']),
    ('box', '文献', 'Yubran AP, Cerezal Pesquera L, Llopis San Juan E, et al. Rotator cuff tear patterns: MRI appearance and its surgical relevance. Insights Imaging. 2024;15:61.\nCC BY 4.0，原图引自原文，编者加中文标注', 'grey')])
deck.save(OUT)
