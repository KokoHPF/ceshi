#!/usr/bin/env python3
"""Graham 等 2016 Nature Reviews Disease Primers《脑性瘫痪》：首图为原题直译标题卡；原文图 1～11 直接用原图，
图中英文是文本层——按行删除英文文字（保留插画、色块和线条），在原位置写中文；数字、缩写（DBS、SDR、NMDA 等）和分图字母保留；
要点卡和管理证据卡为编者根据原文整理。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (234, 230, 246)
Z = 4
K, G, R = (0, 0, 0), (94, 94, 94), (255, 38, 0)
doc = pymupdf.open(PDF)
PUNC = '，。；、：）”'


def save(im, n):
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=90)


def titled(im, t, W=1200):
    if im.width != W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    out = Image.new('RGB', (W, im.height + 90), 'white'); od = ImageDraw.Draw(out)
    od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), t, font=font(36), fill='white')
    out.paste(im, (0, 90)); return out


def capbox(im, cap, W=1200):
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = []; line = ''
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for ch in cap:
        if d0.textlength(line + ch, font=font(28)) > W - 30 and ch not in PUNC:
            k = len(line)
            while ch.isascii() and ch.isalnum() and k and line[k - 1].isascii() and line[k - 1].isalnum(): k -= 1
            if not k: k = len(line)
            lines.append(line[:k]); line = line[k:] + ch
        else: line += ch
    lines.append(line)
    hh = 24 + 40 * len(lines)
    t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
    dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT)
    for i, l in enumerate(lines): dr.text((14, 14 + 40 * i), l, font=font(28), fill=TEAL)
    t.paste(im, (0, hh + 8)); return t


def para(dr, x, y, t, fs, w, fill=INK, gap=10):
    line = ''
    for ch in t:
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in PUNC: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
        else: line += ch
    dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap


def bullet(dr, x, y, t, fs, w, fill=INK, gap=10):
    r = fs * 0.16; cy = y + fs * 0.55
    dr.ellipse([x + 4, cy - r, x + 4 + 2 * r, cy + r], fill=RED)
    return para(dr, x + fs * 1.1, y, t, fs, w - fs * 1.1, fill=fill, gap=gap)


def para_h(t, fs, w, gap=10):
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    return para(d0, 0, 0, t, fs, w, gap=gap)


def phases(title, S, n, fs=24):
    W = 1200; im = Image.new('RGB', (W, 3000), 'white'); dr = ImageDraw.Draw(im); y = 20
    for t, bg, c, items in S:
        h = 66 + sum(para_h(s, fs, 1030 - fs * 1.1, gap=8) + 10 for s in items)
        dr.rounded_rectangle([40, y, 1160, y + h], 14, fill=bg); dr.text((70, y + 16), t, font=font(30), fill=c)
        yy = y + 62
        for s in items: yy = bullet(dr, 70, yy, s, fs, 1060, gap=8) + 10
        y += h + 16
    save(titled(im.crop((0, 0, W, y)), title), n)


def norm(s):
    for a, c in (('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬃ', 'ffi'), ('ﬀ', 'ff')): s = s.replace(a, c)
    return ''.join(s.split()).lower()


def zh_txt(pno, crop, entries, fs=0.95):
    """entries：(英文行或连续多行的元组, 中文, 对齐)。元组末尾写 '...' 表示一直到该文字块结束；对齐加 w 表示按框宽自动换行"""
    pg = doc[pno]; crop = pymupdf.Rect(crop); L = []
    for bi, bl in enumerate(pg.get_text('dict', clip=crop)['blocks']):
        if bl['type']: continue
        for ln in bl['lines']:
            t = ''.join(s['text'] for s in ln['spans'])
            if not t.strip(): continue
            s0 = ln['spans'][0]; c = s0['color']
            L.append(dict(t=norm(t), bb=pymupdf.Rect(ln['bbox']), blk=bi, size=s0['size'], col=(c >> 16, c >> 8 & 255, c & 255),
                          bold=any(k in s0['font'] for k in ('Bold', 'Semibold')), vert=abs(ln['dir'][1]) > 0.9, dir=ln['dir'][1], used=False))
    jobs = []
    for en, zh, al in sorted(entries, key=lambda e: -len(e[0]) if isinstance(e[0], tuple) else 0):
        seq = [norm(x) for x in (en if isinstance(en, tuple) else (en,))]
        to_end = seq[-1] == '...'
        if to_end: seq = seq[:-1]
        hit = 0
        for i in range(len(L)):
            if i + len(seq) > len(L) or any(L[i + k]['used'] or L[i + k]['t'] != s for k, s in enumerate(seq)): continue
            j = i + len(seq)
            if to_end:
                while j < len(L) and L[j]['blk'] == L[i]['blk']: j += 1
            grp = L[i:j]
            for g in grp: g['used'] = True
            bb = pymupdf.Rect(grp[0]['bb'])
            for g in grp: bb |= g['bb']
            jobs.append((bb, zh, al, grp[0])); hit += 1
        assert hit, f'第 {pno + 1} 页找不到：{en}'
    for g in L:
        if g['used']:
            pg.add_redact_annot(g['bb'] + ((1.6, 0, -1.6, 0) if g['vert'] else (0, 1.6, 0, -1.6)), fill=None)
    pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=crop)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); d = ImageDraw.Draw(im)
    for bb, zh, al, g in jobs:
        s = g['size'] * Z * fs; f = font(s); lh = s * 1.12; col = g['col']; sw = 1 if g['bold'] else 0
        X0, Y0, X1, Y1 = (bb.x0 - crop.x0) * Z, (bb.y0 - crop.y0) * Z, (bb.x1 - crop.x0) * Z, (bb.y1 - crop.y0) * Z
        if g['vert']:
            tw = int(d.textlength(zh, font=f)) + 4; t = Image.new('RGBA', (tw, int(lh)), (0, 0, 0, 0))
            ImageDraw.Draw(t).text((2, s * 0.08), zh, font=f, fill=col, stroke_width=sw, stroke_fill=col)
            t = t.rotate(90 if g['dir'] < 0 else -90, expand=True); im.paste(t, (int((X0 + X1 - t.width) / 2), int((Y0 + Y1 - t.height) / 2)), t); continue
        ls = []
        for par in zh.split('\n'):
            if 'w' in al:
                line = ''
                for ch in par:
                    if d.textlength(line + ch, font=f) > X1 - X0 and ch not in PUNC: ls.append(line); line = ch
                    else: line += ch
                ls.append(line)
            else: ls.append(par)
        top = Y0 if 'w' in al else (Y0 + Y1) / 2 - lh * len(ls) / 2
        for i, l in enumerate(ls):
            tw = d.textlength(l, font=f); a = al[0]
            x = {'l': X0, 'r': X1 - tw, 'c': (X0 + X1 - tw) / 2}[a]
            d.text((x, top + i * lh + s * 0.1), l, font=f, fill=col, stroke_width=sw, stroke_fill=col)
    return im


def raw(pno, crop):
    pix = doc[pno].get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=pymupdf.Rect(crop))
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)

# 首图
W, H = 1400, 680; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 56), '疾病入门综述 · Nature Reviews Disease Primers 2016', font=font(32), fill=TEAL)
dr.text((70, 140), '脑性瘫痪', font=font(84), fill=INK)
dr.text((70, 270), 'Cerebral palsy', font=font(34), fill=GREY)
dr.line([70, 350, W - 70, 350], fill=(200, 205, 210), width=2)
dr.text((70, 380), 'Graham HK, Rosenbaum P, Paneth N, Dan B, Lin JP, Damiano DL, Becher JG,', font=font(28), fill=GREY)
dr.text((70, 420), 'Gaebler-Spira D, Colver A, Reddihough DS, Crompton KE, Lieber RL.', font=font(28), fill=GREY)
dr.text((70, 464), 'Nat Rev Dis Primers. 2016;2:15082. doi:10.1038/nrdp.2015.82', font=font(28), fill=GREY)
dr.text((70, 530), '通讯作者：H. Kerr Graham，澳大利亚墨尔本皇家儿童医院骨科', font=font(26), fill=GREY)
dr.text((70, 600), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 1)

phases('脑瘫的几个关键数字（编者根据原文整理）', [
    ('有多常见', LT, TEAL, ['儿童期起病、终身存在的肢体残疾里最常见的一种：约每 500 名新生儿 1 例，全球约 1700 万人',
        '澳洲和欧洲登记数据为每 1000 名活产 1.5～2.5 例；美国、中国台湾和埃及的新研究超过 3 例']),
    ('谁的风险高', OR, (180, 90, 20), ['早产是最重要的危险因素：胎龄 < 28 周出生，风险约为足月儿的 50 倍',
        '早产儿影像上有持续性白质损伤（囊腔或脑室扩大）时，约 50% 会发展为脑瘫', '但多数脑瘫患儿是足月出生的，这是原文图 3 所说的“悖论”']),
    ('病因不等于“出生时缺氧”', PU, (90, 60, 150), ['明确经历过严重出生窒息的不到 10%', '约 90% 是破坏性脑损伤；脑发育畸形约 10%～15%；足月儿围产期缺血性卒中 < 5%',
        '11%～17% 临床诊断的脑瘫 MRI 正常，要仔细排查遗传和代谢病']),
    ('一部分可以预防', GR, (40, 120, 60), ['早产风险孕妇使用硫酸镁，脑瘫减少约 30%；孕 34 周前使用产前激素也有效',
        '新生儿缺氧缺血性脑病出生 6 小时内开始全身低温治疗，可降低死亡和神经残疾的严重程度'])], 2)

# 原文图 1（第 3 页）
LV = [('Children walk at home, school, outdoors and in the', '儿童可在家、学校、户外和社区内行走；上下楼梯不用扶栏杆；能完成跑、跳等粗大运动技能，但速度、平衡和协调能力有限。'),
      ('Children walk in most settings and climb stairs holding', '儿童可在大多数环境中行走，上下楼梯需扶栏杆。长距离行走，在不平地面、斜坡、拥挤或狭窄空间中保持平衡可能有困难。可能需要他人扶持、手持助行器，长距离时使用轮式移动工具。跑、跳等粗大运动能力极少。'),
      ('Children walk using a hand-held mobility device in most', '在大多数室内环境中借助手持助行器行走；在监护或协助下可扶栏杆上下楼梯。长距离使用轮式移动工具，短距离可自己推轮椅。'),
      ('Children use methods of mobility that require physical', '在大多数环境中需他人协助或使用电动移动工具。在家可在他人扶持下短距离行走，或摆好体位后使用电动移动设备或躯干支撑助行器。在学校、户外和社区由他人推手动轮椅或使用电动移动工具。'),
      ('Children are transported in a manual wheelchair in all', '在所有环境中都由他人推手动轮椅转运；维持抗重力的头部和躯干姿势、控制上下肢运动的能力受限。')]
fig1 = zh_txt(2, (134, 175, 560, 671),
    [('GMFCS expanded and revised between 6th and 12th birthday: descriptors and illustrations', 'GMFCS 扩展修订版（6 岁至 12 岁生日之间）：描述与图示', 'l')]
    + [(f'GMFCS level {r}', f'GMFCS {r} 级', 'l') for r in ('I', 'II', 'III', 'IV', 'V')]
    + [((en, '...'), zh, 'lw') for en, zh in LV])
save(titled(capbox(fig1, '粗大运动功能分级系统（GMFCS）是脑瘫运动功能分级的金标准，不同年龄段描述不同，这里是 6～12 岁版本。它有效、可靠、稳定，能预测长期粗大运动功能'),
            '原文图 1　GMFCS 扩展修订版（6～12 岁）'), 3)

fig2 = zh_txt(3, (134, 57, 560, 236), [
    ('Unilateral cerebral palsy', '单侧脑瘫', 'c'), ('Bilateral cerebral palsy', '双侧脑瘫', 'c'),
    ('Monoplegia', '单瘫', 'c'), ('Hemiplegia', '偏瘫', 'c'), ('Diplegia', '双瘫', 'c'), ('Triplegia', '三肢瘫', 'c'), ('Quadriplegia', '四肢瘫', 'c')])
save(titled(capbox(fig2, '深绿色为受累更重的部位。单瘫多累及下肢；偏瘫为一侧身体受累，通常上肢重于下肢。双瘫四肢都受累但下肢重得多；三肢瘫一般为单侧上肢加双侧（不对称）下肢；四肢瘫四肢和躯干都受累。按欧洲脑瘫监测协作组（SCPE）术语，单瘫和偏瘫属单侧脑瘫，后三种属双侧脑瘫'),
            '原文图 2　脑瘫的部位分型'), 4)

fig3 = zh_txt(4, (346, 520, 560, 667), [
    ('Cerebral palsy cases', '脑瘫病例', 'c'), ('Gestational age (weeks)', '胎龄（周）', 'c'),
    (('Cerebral palsy cases per 1,000', 'neonatal survivors'), '每 1000 名存活新生儿中的\n脑瘫病例数', 'l'), ('Percentage of all cerebral palsy', '占全部脑瘫的百分比', 'l')])
save(titled(capbox(fig3, '蓝柱：胎龄越小，每 1000 名存活新生儿中的脑瘫例数越高（20～27 周约 87 例）。绿柱：但足月（37 周以上）出生的患儿占了全部脑瘫的约 60%。早产风险极高、患者却多为足月儿，这就是原文所说的“悖论”'),
            '原文图 3　胎龄与脑瘫患病率'), 5)

x = doc.extract_image(31); fig4 = Image.open(__import__('io').BytesIO(x['image'])).convert('RGB')
save(titled(capbox(fig4, 'a：孕 32 周冠状位和轴位 MRI，额叶发育不良和多小脑回（箭头），患儿后来为重度双侧痉挛型脑瘫（GMFCS V 级）。b：孕 30 周早产儿 5 周时的 MRI，囊性脑室周围白质软化（箭头），后来为 GMFCS IV 级。c：足月出生窒息患儿 3 岁时 MRI，皮质-皮质下萎缩（星号）和双侧基底节囊腔（箭头），后来为混合型（痉挛加运动障碍）脑瘫，GMFCS V 级'),
            '原文图 4　脑瘫的脑损伤（MRI）'), 6)

fig5 = zh_txt(6, (40, 57, 342, 343), [
    ('Excitotoxicity', '兴奋性毒性', 'c'), ('Extrinsic pathway', '外源性通路', 'c'), ('Inflammatory cytokines', '炎症因子', 'c'),
    ('Glutamate', '谷氨酸', 'c'), ('Caspase activation', '胱天蛋白酶激活', 'c'), ('Energy depletion', '能量耗竭', 'c'),
    (('Mitochondrial', 'dysfunction'), '线粒体\n功能障碍', 'c'), ('Mitochondrion', '线粒体', 'c'), (('Intrinsic', 'pathway'), '内源性\n通路', 'l'),
    ('DNA damage', 'DNA 损伤', 'c'), ('Apoptosis', '凋亡', 'c'), ('Nucleus', '细胞核', 'l')])
save(titled(capbox(fig5, '外源性通路：炎症因子与细胞表面结合，激活 FAS 死亡受体和 NMDA 受体介导的兴奋性毒性。内源性通路：应激的线粒体释放信号，激活依赖或不依赖胱天蛋白酶的细胞死亡。一氧化氮等自由基可导致 DNA 断裂。Vm：膜电位；VSCC：电压敏感钙通道'),
            '原文图 5　细胞死亡信号通路'), 7)

fig6 = zh_txt(7, (136, 338, 560, 577), [
    ('Typical development', '典型发育', 'l'), ('Cerebral palsy', '脑瘫', 'l'), ('Bone', '骨', 'l'), ('Muscle', '肌肉', 'l'), ('Growth', '生长', 'l'),
    (('Muscle', 'fibre'), '肌纤维', 'l'), (('Satellite', 'cell'), '卫星细胞', 'l'), ('Cross-sectional', '横切面', 'c'), ('Longitudinal', '纵切面', 'c')])
save(titled(capbox(fig6, 'a、b：脑瘫肌肉（b）的肌节比典型发育（a）长得多，尽管两者肌束总长度接近。c、d：骨骼生长时，典型发育的肌肉串联增加肌节，踝关节保持全范围活动；脑瘫肌肉推测不能串联增加肌节，骨长了肌肉跟不上，踝被拉成跖屈。横切面上脑瘫肌纤维更小，纵切面上卫星细胞更少。e～h：层粘连蛋白免疫染色，脑瘫肌肉（g、h）细胞外基质明显增多'),
            '原文图 6　脑瘫肌肉的结构改变'), 8)

fig7 = zh_txt(9, (36, 57, 560, 339), [
    ('Early CNS lesion and/or reorganization', '早期中枢神经系统损伤和 / 或重组', 'c'), ('Developmental delay', '发育迟缓', 'c'), ('Weakness', '无力', 'c'),
    ('Movement disorders', '运动障碍', 'c'), ('Stretch reflex disorder', '牵张反射障碍', 'c'), ('Muscle disorder', '肌肉病变', 'c'),
    (('Abnormal muscle activation', '(patterns and timing)'), '肌肉激活异常\n（模式和时序）', 'c'),
    (('Release of tonic labyrinthine', 'and neck reflexes'), '紧张性迷路反射和\n颈反射释放', 'c'),
    ('Loss of supraspinal inhibition', '脊髓上抑制丧失', 'c'), ('Trophic changes in muscles', '肌肉营养性改变', 'c'),
    (('EMG active', '(dependent on muscle', 'length or slow stretch)'), '肌电活跃\n（取决于肌肉长度\n或慢速牵伸）', 'c'), ('Inhibited by sleep', '睡眠时受抑制', 'c'),
    (('EMG active', '(dependent on velocity', 'of stretch)'), '肌电活跃\n（取决于\n牵伸速度）', 'r'),
    (('EMG silent', 'Resistance to', 'passive stretch'), '肌电静息\n对被动牵伸\n有阻力', 'r'), ('Independent of sleep', '不受睡眠影响', 'r'),
    ('Dystonic response', '肌张力障碍反应', 'c'), ('Spastic response', '痉挛反应', 'c'), ('Muscle fibre-type transformation', '肌纤维类型转化', 'c'),
    ('Movement disorder', '运动障碍', 'c'), ('Posture disorder', '姿势障碍', 'c'),
    (('Reduced muscle extensibility', 'and joint range'), '肌肉延展性和\n关节活动度下降', 'c'),
    ('Orthopaedic surgery', '骨科手术', 'c'), ('Levodopa', '左旋多巴', 'c'),
    (('BoNT-A', 'Oral baclofen or ITB', 'Benzodiazepines', 'Anticholinergics', 'Gabapentin'), 'A 型肉毒毒素\n口服或鞘内巴氯芬\n苯二氮卓类\n抗胆碱能药\n加巴喷丁', 'l'),
    (('EMG positive', 'Dynamic muscle resistance'), '肌电阳性\n动态肌肉阻力', 'c'),
    (('EMG negative', 'Passive muscle resistance', 'Contracture amd deformity'), '肌电阴性\n被动肌肉阻力\n挛缩和畸形', 'c'), ('Time', '时间', 'c')])
save(titled(capbox(fig7, '早期中枢损伤可引起肌电活跃的运动障碍，也可引起肌电静息的肌肉营养性改变和挛缩。睡眠时消失的是肌张力障碍（异常的肌肉激活或姿势）；不受睡眠影响的，考虑脊髓上抑制丧失导致的痉挛（速度依赖的牵张反射）。橙色框是过去 70 年形成的管理手段。DBS：脑深部电刺激；SDR：选择性脊神经后根切断术。右侧绿箭头表示随时间推移，肌肉逐渐走向固定畸形和挛缩'),
            '原文图 7　脑瘫的运动障碍'), 9)

fig8 = zh_txt(11, (40, 350, 348, 658), [
    ('Initial contact', '初始着地', 'c'), ('Loading response', '承重反应', 'c'), ('Mid-stance', '支撑中期', 'c'), ('Early', '早', 'c'), ('Late', '晚', 'c'),
    ('Terminal stance', '支撑末期', 'c'), ('Pre-swing', '摆动前期', 'c'), ('Ankle angle (degrees)', '踝关节角度（°）', 'c'),
    ('Stance phase', '支撑相', 'c'), ('Swing phase', '摆动相', 'c')])
save(titled(capbox(fig8, 'a：支撑相可分为初始着地、承重反应、支撑中期、支撑末期和摆动前期，红箭头为地面反作用力方向。b：踝关节角度，实线为典型发育儿童的平均背屈角度，虚线为均值 ± 2 个标准差'),
            '原文图 8　典型发育步态的支撑相和矢状面踝关节运动学'), 10)

fig9 = zh_txt(14, (40, 146, 342, 518), [
    ('CNS pathology', '中枢神经系统病变', 'c'), (('Loss of inhibition', 'of LMNs'), '对下运动神经元\n的抑制丧失', 'l'),
    (('Loss of connections to LMNs', '(and other pathways)'), '与下运动神经元的连接\n（及其他通路）丧失', 'l'),
    (('Positive features', 'of UMN syndrome'), '上运动神经元\n综合征阳性特征', 'l'), (('Negative features', 'of UMN syndrome'), '上运动神经元\n综合征阴性特征', 'l'),
    (('• Spasticity', '• Hyper-reflexia', '• Clonus', '• Co-contraction'), '· 痉挛\n· 反射亢进\n· 阵挛\n· 共同收缩', 'l'),
    (('• Weakness', '• Impaired selective', 'motor control', '• Poor coordination', '• Sensory deficits'), '· 无力\n· 选择性运动控制受损\n· 协调性差\n· 感觉缺陷', 'l'),
    ('Neural', '神经性', 'c'), ('Non-neural', '非神经性', 'c'), ('Upper limb', '上肢', 'c'), ('Spine/pelvis', '脊柱 / 骨盆', 'c'), ('Hips', '髋', 'c'),
    ('Lower limbs', '下肢', 'c'), (('Posture/', 'contractures'), '姿势异常 /\n挛缩', 'c'), ('Scoliosis', '脊柱侧凸', 'c'),
    ('Hip displacement', '髋关节移位', 'c'), ('Contractures', '挛缩', 'c'), ('Bony torsion', '骨扭转', 'c')])
save(titled(capbox(fig9, '上运动神经元损伤有两类后果：失去对下运动神经元的抑制，产生痉挛、反射亢进等“阳性”特征；失去皮质脊髓束对下运动神经元的连接，产生无力、选择性运动控制差等“阴性”特征，后者影响更大。传统上过分强调阳性特征。例如髋关节移位以前归因于内收肌痉挛，但移位发生率与 GMFCS 分级线性相关，提示阴性特征更重要'),
            '原文图 9　上运动神经元综合征'), 11)

fig10 = raw(16, (134, 57, 560, 177))
save(titled(capbox(fig10, 'a、b：8 岁右侧痉挛型偏瘫男孩，摆动末期右足下垂（蓝虚线），来自腓肠肌-比目鱼肌痉挛加选择性运动控制差，容易绊倒；佩戴踝足矫形器后足跟着地正常。c、d：12 岁痉挛型双瘫、蹲伏步态男孩，地面反作用力（红箭头）落在膝后方，股四头肌负担很重；佩戴双侧地面反作用式踝足矫形器后，力线移到膝前方，膝和髋伸展改善，步态更直立、更省力'),
            '原文图 10　踝足矫形器在可步行脑瘫儿童中的作用'), 12)

fig11 = zh_txt(17, (40, 57, 342, 389), [
    ('Children', '儿童', 'c'), ('Adolescents', '青少年', 'c'), (('Psychological', 'well-being'), '心理健康', 'r'), (('Moods and', 'emotions'), '情绪', 'r'),
    ('Self-perception', '自我认知', 'r'), ('Autonomy', '自主性', 'r'), (('Relationship', 'with parents'), '亲子关系', 'r'),
    (('Social support', 'and peers'), '社会支持\n与同伴', 'r'), ('School life', '学校生活', 'r'), (('Financial', 'resources'), '经济资源', 'r'),
    (('Social', 'acceptance'), '社会接纳', 'r'), ('QOL score', '生活质量评分', 'c'),
    ('Individuals with cerebral palsy', '脑瘫个体', 'l'), ('Matched controls from the general population', '一般人群中的匹配对照', 'l')])
save(titled(capbox(fig11, 'KIDSCREEN 问卷九个领域的生活质量评分（绿：脑瘫；蓝：一般人群匹配对照）。儿童期各领域与同龄人大致相当；青少年在“社会支持与同伴”领域明显偏低'),
            '原文图 11　KIDSCREEN 问卷各领域生活质量评分'), 13)

phases('脑瘫的管理：哪些有证据（编者根据原文整理）', [
    ('证据较充分', GR, (40, 120, 60), ['单侧脑瘫的高强度上肢训练（如强制性运动疗法）：改善手功能，是证据最一致的治疗',
        '任务特异性技能训练，加上针对无力、体能差等继发损害的体能训练', '踝足矫形器改善矢状面步态；单次多平面手术（6～12 岁）改善步态，有一项随机对照试验',
        '人群髋关节监测加适时的预防性和重建手术；重度脊柱侧凸用 T2 至骨盆的长节段融合']),
    ('效果有限或证据不一致', OR, (180, 90, 20), ['下肢任务训练不如上肢一致；减重跑台、机器人步态训练不优于同等强度的运动训练',
        '肌力训练结果不一；功能性或全腿肌力训练明显无效，应针对最限制任务的弱肌', '口服药、肉毒毒素和鞘内巴氯芬降张力，对固定挛缩进展影响很小',
        '虚拟现实不优于常规治疗；机器人踝训练只是概念验证']),
    ('不推荐或要谨慎', PK, RED, ['Bobath、Vojta 等传统方法缺乏证据支持，却仍很常见',
        '被动牵伸：最常引起疼痛的日常活动，对挛缩和功能没有临床意义的改善', '肉毒毒素和内收肌松解治疗不能行走儿童的髋关节移位，失败率高',
        '干细胞治疗：尚无疗效研究发表，需告知家庭“治愈并不临近”'])], 14)

phases('落到全生命周期（编者根据原文整理）', [
    ('婴儿期：早识别', LT, TEAL, ['高危婴儿（早产、缺氧缺血等）做全身运动评估加头颅超声，条件允许再做 MRI，诊断敏感度和特异度都很高',
        '没有危险因素的也要筛查：坐、站、走延迟，过早出现利手，爬行或行走不对称，肌张力异常']),
    ('儿童期：功能为先', GR, (40, 120, 60), ['目标是孩子和家庭最看重的功能活动；训练要主动参与、强度够、有变化、逐步加难',
        '6 岁前很少需要骨科手术；伴随问题要管：约 40% 有癫痫，还有喂养、反流、流涎、骨质疏松和疼痛']),
    ('青少年到成年：别断档', PU, (90, 60, 150), ['青少年和成年后活动量下降会加速继发损害；力量和体能训练应成为生活方式的一部分',
        '向成人医疗过渡时结局往往不好；成年人的社交、就业、疲劳、疼痛和抑郁需要关注'])], 15)

# 封面 900×383
im = Image.new('RGB', (900, 383), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 14, 383], fill=TEAL)
dr.text((50, 56), 'Nature Reviews Disease Primers', font=font(32), fill=TEAL)
dr.text((50, 128), '脑性瘫痪', font=font(64), fill=INK)
dr.text((50, 220), '从病因、肌肉到全生命周期管理', font=font(40), fill=INK)
dr.text((50, 318), 'GMFCS · 痉挛与肌张力障碍 · 无力 · 髋关节监测', font=font(26), fill=GREY)
im.save(f'{OUT}/cover.jpg', quality=90)
