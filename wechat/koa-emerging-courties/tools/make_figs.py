#!/usr/bin/env python3
"""Courties 等 2026《膝骨关节炎的新兴疗法》（Nat Rev Rheumatol）推文配图：首图为原题直译标题卡；
原文图 1～3 为矢量图，按行删除图中英文（保留插画、色块和线条），在原位置写中文，药物代号、分子缩写保留；
原文表 1 编者翻译重排；其余卡片和图表为编者根据原文整理。
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
    im.convert('RGB').save(f'{OUT}/img{n:02d}.jpg', quality=88, optimize=True)


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
        if ch == '\n': dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ''; continue
        if dr.textlength(line + ch, font=font(fs)) > w and ch not in PUNC:
            k = len(line)  # 英文单词和数字不拆开
            while ch.isascii() and ch.isalnum() and k and line[k - 1].isascii() and (line[k - 1].isalnum() or line[k - 1] in '.-/'): k -= 1
            if not k: k = len(line)
            dr.text((x, y), line[:k], font=font(fs), fill=fill); y += fs + gap; line = line[k:] + ch
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


import io

def cover_from(im, cx=0.5, cy=0.5):
    """封面 900×383：从原文插图按比例裁出一块（cx、cy 为裁剪中心的相对位置）"""
    r = 900 / 383; w, h = im.size
    if w / h > r: cw, ch = round(h * r), h
    else: cw, ch = w, round(w / r)
    x = min(max(0, round(cx * w - cw / 2)), w - cw); y = min(max(0, round(cy * h - ch / 2)), h - ch)
    im.crop((x, y, x + cw, y + ch)).resize((900, 383), Image.LANCZOS).convert('RGB').save(f'{OUT}/cover.jpg', quality=90)


def title_card(tag, zh, en, au, cite, org):
    W, H = 1400, 700; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, 18, H], fill=TEAL)
    dr.text((70, 56), tag, font=font(32), fill=TEAL)
    y = 130
    for l in zh: dr.text((70, y), l, font=font(50), fill=INK); y += 70
    y += 20
    for l in en: dr.text((70, y), l, font=font(28), fill=GREY); y += 40
    y += 20; dr.line([70, y, W - 70, y], fill=(200, 205, 210), width=2); y += 30
    dr.text((70, y), au, font=font(30), fill=GREY); y += 44
    dr.text((70, y), cite, font=font(28), fill=GREY); y += 56
    dr.text((70, y), org, font=font(26), fill=GREY)
    dr.text((70, H - 60), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
    save(im, 1)


def chart_style():
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    fm.fontManager.addfont(F); plt.rcParams['font.family'] = fm.FontProperties(fname=F).get_name()
    plt.rcParams['axes.unicode_minus'] = False
    return plt


def figsave(plt, fig, title, n):
    b = io.BytesIO(); fig.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
    save(titled(Image.open(b).convert('RGB'), title), n)


def ctable(title, hdr, cw, rows, n, fs=22):
    """编者整理的对照表卡片"""
    W = 1200; H = 64 + sum(max(para_h(t, fs, w - 24, gap=6) for t, w in zip(r, cw)) + 24 for r in rows)
    im = Image.new('RGB', (W, H + 20), 'white'); dr = ImageDraw.Draw(im); x = 20
    for t, w in zip(hdr, cw): dr.rectangle([x, 10, x + w, 64], fill=TEAL); dr.text((x + 12, 22), t, font=font(26), fill='white'); x += w
    y = 64
    for k, r in enumerate(rows):
        h = max(para_h(t, fs, w - 24, gap=6) for t, w in zip(r, cw)) + 24; x = 20
        for j, (t, w) in enumerate(zip(r, cw)):
            dr.rectangle([x, y, x + w, y + h], fill=LT if k % 2 else 'white', outline=(210, 210, 210))
            para(dr, x + 12, y + 12, t, fs, w - 24, fill=RED if j == 0 else INK, gap=6); x += w
        y += h
    save(titled(im.crop((0, 0, W, y + 14)), title), n)



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



# 首图：原题直译
title_card('综述 · Nature Reviews Rheumatology 2026',
           ['膝骨关节炎的新兴疗法'],
           ['Emerging therapies for knee osteoarthritis'],
           'Alice Courties, Tobias Winkler, Philip G. Conaghan, Francis Berenbaum',
           'Nat Rev Rheumatol. 2026. doi:10.1038/s41584-026-01441-y',
           '法国索邦大学圣安托万医院风湿科、奥地利维也纳医科大学、英国利兹大学')

phases('原文要点（编者翻译）', [
    ('两条路线', LT, TEAL, [
        '药物研发仍分成两类：改善疼痛和功能的对症治疗，和延缓结构进展的病情修饰药物（DMOAD），两者的机制、目标和监管要求都不同']),
    ('对症治疗', GR, (40, 120, 60), [
        '肠促胰素类药物（如司美格鲁肽）是肥胖相关膝骨关节炎最有前景的新方法，但长期安全性和停药后怎么维持还不清楚',
        '其他新兴对症疗法：缓释糖皮质激素、神经营养因子调节、甲氨蝶呤、润滑类注射剂、影像引导下的神经血管介入']),
    ('病情修饰', OR, RED, [
        '候选 DMOAD 针对软骨合成、Wnt 信号、免疫代谢、基质降解酶、软骨下骨重塑和关节内基因转移',
        '间充质基质细胞治疗疗效不一致，尚无令人信服的结构获益']),
    ('未来', PU, (90, 60, 150), [
        '未来的膝骨关节炎管理可能要靠按机制给患者分层，并把代谢、炎症、骨软骨和疼痛通路的治疗组合起来']),
], 2)

# 原文表 1（编者翻译重排）
T1A = [
    ('神经营养因子调节（NT3、p75NTR）\nLEVI-04', 'II 期（同行评议论文）', '剂量依赖性减轻疼痛；无快速进展性 OA 信号', '没有结构终点'),
    ('关节腔 TRPV1 激动剂\nCNTX-4975', 'III 期（会议摘要）', '镇痛获益不显著', '注射痛可能破坏盲法'),
    ('关节腔 TRPV1 激动剂\n树脂毒素', 'II 期（会议摘要）；III 期（ClinicalTrials.gov）', 'II 期阳性；III 期阴性', '—'),
    ('Nav1.7 抑制\nOLP-1002 基因治疗', 'IIa 期（公司新闻稿）', '结果待公布', '结果待公布'),
    ('化学神经松解\nSL-1002', 'II 期（结果待公布）', '试验进行中', '结果待公布'),
    ('关节润滑\nMM-II', 'II 期（同行评议论文）', '主要终点阴性，次要终点阳性', '未达主要终点'),
    ('缓释糖皮质激素\nTLC599', 'IIa 期（论文）；III 期（会议摘要）', '疼痛较安慰剂减轻', '未显示优于普通激素'),
    ('缓释糖皮质激素\nEP-104IAR', 'II 期（同行评议论文）', '疼痛较安慰剂减轻', '—'),
    ('全身抗炎\n甲氨蝶呤 25 mg/周（口服）', 'III 期（同行评议论文）', '疼痛较安慰剂减轻', '未显示结构获益'),
    ('全身抗炎\n甲氨蝶呤 15 mg/周（皮下）\n人群：MRI 示滑膜炎的炎症型 OA', 'III 期（同行评议论文）', '无统计学显著获益', '—'),
    ('减重（GLP1 受体激动剂）\n司美格鲁肽\n人群：肥胖（BMI ≥ 30）', 'III 期（同行评议论文）', '体重明显下降，疼痛和功能大幅改善', '长期维持和结构疗效不确定'),
    ('大麻素通路\n大麻二酚', 'II 期（论文）；I～II 期（结果待公布）', '无效；不良事件增加', '安全性问题'),
]
T1B = [
    ('CCL17 抑制\n抗 CCL17 单抗', 'II 期（ClinicalTrials.gov）', '中期分析阴性', '初步结果'),
    ('IL-6 治疗性疫苗', 'I 期（同行评议论文）', '安全性和免疫原性可接受', '需要更多安全性数据'),
    ('免疫代谢（AMPK 激活）\n二甲双胍\n人群：无糖尿病的 OA', 'II 期（同行评议论文）', '疼痛减轻，与体重下降无关', '结构疗效未证实'),
    ('软骨合成（ANGPTL3 衍生蛋白）\nLNA-043', 'IIb 期（ClinicalTrials.gov）', '未达主要终点', '初步结果'),
    ('软骨修复与骨形态调节\nTPX-100\n人群：双膝 OA（同一患者两膝对照）', 'II 期（同行评议论文）', '骨形态、软骨厚度和功能改善', '需要 III 期确认'),
    ('TGFβ 通路调节\nEngedi 1000\n人群：K-L 3 级 OA', 'II 期（会议摘要）', '未达主要终点；疗效信号仅见于预设亚组', '初步结果'),
    ('Wnt 通路抑制\nlorecivivint\n人群：病情较轻（关节间隙 > 3 mm）', 'III 期（同行评议论文）', 'III 期失败；可能存在亚组差异', '效应很小，无结构疗效'),
    ('骨重塑（组织蛋白酶 K 抑制）\nMIV-711\n人群：影像学膝 OA', 'II 期（同行评议论文）', '有结构获益，疼痛无改善', '无对症获益'),
]
ctable('原文表 1（上）　对症治疗（编者翻译重排）', ['机制 / 药物', '试验阶段（证据来源）', '主要结果', '主要局限'], [380, 260, 300, 220], T1A, 3, fs=21)
ctable('原文表 1（下）　潜在病情修饰药物（编者翻译重排）', ['机制 / 药物', '试验阶段（证据来源）', '主要结果', '主要局限'], [380, 260, 300, 220], T1B, 4, fs=21)

# 原文图 1（第 4 页）
fig1 = zh_txt(3, (36, 382, 562, 636), [
    (('Subchondral', 'Bone'), '软骨下骨', 'l'), ('Synovium', '滑膜', 'l'), ('Cartilage', '软骨', 'l'), ('Macrophage', '巨噬细胞', 'l'),
    (('Ablation', 'needle'), '消融针', 'l'), (('Radiofrequency', 'ablation'), '射频消融', 'l'), (('Genicular nerve', 'block'), '膝神经阻滞', 'l'),
    (('Chemoneurolytic', 'agent (SL-1002)'), '化学神经松解剂\n（SL-1002）', 'l'), (('Sensory', 'neuron'), '感觉\n神经元', 'l'),
    (('TrkA inhibitor', '(GZ389988A, ASP7962)'), 'TrkA 抑制剂\n（GZ389988A、ASP7962）', 'l'), ('Pan Trk inhibitor', '泛 Trk 抑制剂', 'l'),
    (('Bispecific antibodies', '(anti-TNF, anti-NGF', '(MEDI7352))'), '双特异性抗体\n（抗 TNF + 抗 NGF，\nMEDI7352）', 'l'),
    (('NGF inhibitor', '(tanezumab, fasinumab,', 'fulranumab)'), 'NGF 抑制剂\n（tanezumab、fasinumab、\nfulranumab）', 'l'),
    (('NT3 inhibitor', '(LEVI-04)'), 'NT3 抑制剂\n（LEVI-04）', 'l'), (('Nav1.7 inhibitor', '(OLP-1002)'), 'Nav1.7 抑制剂\n（OLP-1002）', 'l'),
    (('TRPV1 agonist', '(CNTX-4975,', 'RTX-GRT7039)'), 'TRPV1 激动剂\n（CNTX-4975、\nRTX-GRT7039）', 'l'),
    (('TRPA1 antagonist', '(LY3526318)'), 'TRPA1 拮抗剂\n（LY3526318）', 'l')])
save(titled(capbox(fig1, '关节软骨本身没有神经，痛觉感受器分布在滑膜、软骨下骨和关节周围组织。图中蓝框是各类镇痛靶点：NGF 抗体和 TrkA 抑制剂、NT3 抑制剂（LEVI-04）、TRPV1 激动剂、TRPA1 拮抗剂、Nav1.7 抑制剂、化学神经松解剂，以及射频消融、膝神经阻滞等介入手段。BDNF：脑源性神经营养因子；CBD：大麻二酚；CB1、CB2：大麻素受体'),
            '原文图 1　针对疼痛信号的新兴疗法'), 5)

# 原文图 2（第 6 页）
fig2 = zh_txt(5, (38, 428, 562, 671), [
    (('Biologic drugs (IL-1R inhibitor, IL-1Ra', 'gene therapy, AMG108, ABT-981,', 'canakinumab, intra-articular anakinra)'),
     '生物制剂（IL-1R 抑制剂、IL-1Ra 基因治疗、\nAMG108、ABT-981、canakinumab、\n关节腔注射 anakinra）', 'l'),
    ('DMARDs (methotrexate, colchicine)', 'DMARDs（甲氨蝶呤、秋水仙碱）', 'l'), ('PPS', 'PPS（戊聚糖多硫酸钠）', 'l'),
    ('Inflammasome inhibitor (DFV980)', '炎症小体抑制剂（DFV980）', 'l'), ('Pan caspase inhibitor (LG00034053)', '泛 caspase 抑制剂（LG00034053）', 'l'),
    ('Intra-articular GLP1RA', '关节腔内 GLP1 受体激动剂', 'l'), ('IL-10 gene therapy (XT-50)', 'IL-10 基因治疗（XT-50）', 'l'),
    ('Anti-IL-6 vaccine (PPV-06)', '抗 IL-6 疫苗（PPV-06）', 'l'), ('Pro-inflammatory mediators:', '促炎介质：', 'l'),
    ('Inflammasome', '炎症小体', 'l'), ('Cytokines', '细胞因子', 'l'), ('Chemokines', '趋化因子', 'l'), ('Complement', '补体', 'l'),
    ('Bioactive lipids (PGE2)', '生物活性脂质（PGE2）', 'l'), ('ROS', '活性氧（ROS）', 'l'), ('Matrix proteinases', '基质蛋白酶', 'l'),
    ('Synovium', '滑膜', 'l'), ('Cartilage', '软骨', 'l'), ('T cell', 'T 细胞', 'l'), ('Chondrocyte', '软骨细胞', 'l'), ('Macrophage', '巨噬细胞', 'l'),
    ('Fibroblast', '成纤维细胞', 'l'), ('Osteoblast', '成骨细胞', 'l'), (('Anti-CCL17', 'antibody', '(GSK3858279)'), '抗 CCL17\n抗体\n（GSK3858279）', 'l'),
    (('Glucocorticoids', '(TLC599,', 'EP-104IAR)'), '糖皮质激素\n（TLC599、\nEP-104IAR）', 'l'), (('Subchondral', 'bone'), '软骨下骨', 'l')])
save(titled(capbox(fig2, '骨关节炎是一种慢性低度炎症：滑膜细胞、免疫细胞、软骨细胞和软骨下骨细胞释放细胞因子、趋化因子、补体、PGE2、活性氧和炎症小体相关介质，导致软骨降解、滑膜炎和疼痛。右上框列出了针对这些通路的新兴药物（框内药名照原图保留，原图“DFV980”“XT-50”与正文不一致，见文末）'),
            '原文图 2　针对炎症通路的新兴疗法'), 6)

# 原文图 3（第 9 页）
fig3 = zh_txt(8, (102, 446, 478, 664), [
    ('Chondrocyte proliferation:', '促软骨细胞增殖：', 'l'), ('MSCs', '间充质基质细胞', 'l'), (('Neovessels', 'and neonerves'), '新生血管\n与新生神经', 'l'),
    (('TGFβ', 'receptor'), 'TGFβ\n受体', 'l'), (('ALK1', 'receptor'), 'ALK1\n受体', 'l'), ('Cathepsin K', '组织蛋白酶 K', 'l'),
    (('Cathepsin inhibitor', '(MIV-711)'), '组织蛋白酶抑制剂\n（MIV-711）', 'l'), (('Wnt signalling', 'inhibitor (lorecivivint)'), 'Wnt 信号抑制剂\n（lorecivivint）', 'l'),
    ('Subchondral bone', '软骨下骨', 'l'), ('Osteoclast', '破骨细胞', 'l'), ('Cartilage', '软骨', 'l'), ('Chondrocytes', '软骨细胞', 'l'),
    ('Osteoblasts', '成骨细胞', 'l'), ('Bisphosphonates', '双膦酸盐', 'l'),
    (('ADAMTS-5 inhibitor', '(GLPG1972/S201086,', 'M6495)'), 'ADAMTS-5 抑制剂\n（GLPG1972/S201086、\nM6495）', 'l'),
    (('Multispecific nanobody', 'inhibitor (SAR446959)'), '多特异性纳米抗体\n抑制剂（SAR446959）', 'l')])
save(titled(capbox(fig3, '骨关节炎进展伴随软骨降解、软骨下骨异常重塑，以及骨软骨交界处的病理性血管和感觉神经长入。新兴病情修饰策略包括 Wnt 信号抑制、ADAMTS-5 聚蛋白多糖酶抑制、多特异性纳米抗体、ANGPTL3 衍生蛋白（LNA043）和 TPX-100 促软骨合成、调节 TGFβ 信号（Engedi 1000）、组织蛋白酶 K 抑制（MIV-711）、双膦酸盐抑制骨吸收，以及 kartogenin、TissueGene-C、间充质基质细胞和 sprifermin（重组 FGF18）促软骨再生'),
            '原文图 3　针对软骨和软骨下骨重塑的新兴疗法'), 7)

# 编者图表：关键随机对照试验的疼痛组间差
plt = chart_style()
rows = [  # 名称, 组间差（换算为 0–100）, 是否统计学显著, 备注
    ('司美格鲁肽 2.4 mg/周\nSTEP 9，III 期，68 周', 14.1, 1, 'WOMAC 疼痛 0～100'),
    ('间充质基质细胞注射\n25 项 RCT 荟萃分析，6 个月', 12, 2, 'NRS 0～10 换算；证据确定性低'),
    ('二甲双胍 2000 mg/天\nRCT，6 个月', 11.4, 1, 'VAS 0～100 mm'),
    ('lorecivivint 0.07/0.23 mg\nOA-4，IIb 期', 9.6, 1, 'NRS 0～10 换算（7～9.6），III 期未能重复'),
    ('甲氨蝶呤 25 mg/周\nPROMOTE，6 个月', 7.9, 1, 'NRS 0～10 换算；12 个月未维持'),
    ('富血小板血浆 3 次\nRESTORE，12 个月', 4, 0, 'NRS 0～10 换算；P = 0.17'),
]
fig, ax = plt.subplots(figsize=(11, 6.2))
y = list(range(len(rows)))[::-1]
cols = {1: '#00788c', 2: '#9fc9cf', 0: '#bdbdbd'}
for yy, (nm, v, sg, note) in zip(y, rows):
    ax.barh(yy, v, height=.55, color=cols[sg], hatch='//' if sg == 2 else None, edgecolor='white')
    ax.text(v + .3, yy, f'{v:g}', va='center', fontsize=13, color='#222')
    ax.text(v + 2.2, yy, note, va='center', fontsize=10.5, color='#777')
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=12)
ax.set_xlim(0, 30); ax.set_xlabel('疼痛改善的组间差（较安慰剂，换算到 0～100 分）', fontsize=12)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='x', alpha=.3)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color='#00788c', label='统计学显著'), Patch(facecolor='#9fc9cf', hatch='//', edgecolor='white', label='显著但证据确定性低'),
                   Patch(color='#bdbdbd', label='不显著')], frameon=False, fontsize=11, loc='lower right')
b = io.BytesIO(); fig.savefig(b, dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
save(titled(capbox(Image.open(b).convert('RGB'), '编者把原文给出的组间差统一换算到 0～100 分。各试验的量表、人群和随访时间都不同，只能粗略比较，不能当作疗效排名。lorecivivint 取 IIb 期最佳剂量组（7～9.6 分），两项 III 期均未重复'), '几项关键试验的镇痛幅度（编者换算）'), 8)

phases('进展到哪一步了（编者根据原文整理）', [
    ('信号较好，等待确认', GR, (40, 120, 60), [
        '司美格鲁肽：III 期阳性，限肥胖人群；替尔泊肽 III 期、瑞他鲁肽在研',
        'LEVI-04：II 期剂量依赖性镇痛，20 周内未见快速进展性 OA，待 III 期',
        'TPX-100：II 期骨形态、软骨厚度和功能改善，III 期进行中',
        '二甲双胍、口服甲氨蝶呤：各有一项阳性 RCT；缓释激素 TLC599、EP-104IAR：中等镇痛',
        'MIV-711：结构有改善，疼痛没改善']),
    ('已失败或结果阴性', PK, RED, [
        '神经通路：CNTX-4975 和树脂毒素 III 期、TRPA1 拮抗剂 LY3526318、口服大麻二酚',
        '抗炎：抗 CCL17 单抗（中期分析无效终止）、IL-1 靶向药物、夹竹桃麻素加丹皮酚（APPA）',
        '软骨和骨：ADAMTS-5 抑制剂、LNA043、lorecivivint III 期、唑来膦酸',
        '衰老和氧化应激：白藜芦醇、UBX0101、非瑟酮',
        '细胞和自体制品：RESTORE 试验中的富血小板血浆、间充质基质细胞 III 期和 ADIPOA-2、脂肪微碎片']),
    ('早期或结果未公布', LT, TEAL, [
        'OLP-1002（Nav1.7 反义寡核苷酸）、SL-1002（已进入 III 期）、PPV-06（II 期）、DFV890、戊聚糖多硫酸钠',
        '关节腔 GLP1 受体激动剂（仅 I 期安全性）、CYT-108、SAR446959、Engedi 1000',
        '基因治疗：TissueGene-C（美国 III 期）、XT-150、PCRX-201、GNSC-001',
        '介入：射频消融、膝神经阻滞、冷冻神经松解、膝动脉栓塞，随机证据只支持短期、小幅镇痛']),
], 9)

ctable('按表型选治疗：原文设想的分层思路（编者整理）', ['可能的表型', '原文设想的对应方向', '原文中的例子'], [270, 420, 470], [
    ('肥胖、代谢异常', '减重和肠促胰素类药物', '司美格鲁肽、替尔泊肽；二甲双胍；戊聚糖多硫酸钠的 MaRVeL 试验（合并血脂异常）'),
    ('炎症型', '抗炎或免疫代谢干预', '甲氨蝶呤在 hsCRP 高者中可能更有效（事后分析）；PPV-06、DFV890 都选了炎症型患者'),
    ('软骨下骨病变为主', '骨靶向治疗', 'MIV-711；骨髓水肿样病变与疼痛和进展相关'),
    ('疼痛主导、伤害感受型', '神经调节', 'LEVI-04 等神经营养因子调节'),
    ('绝经后女性', '激素因素（原文称研究很少）', '激素替代治疗的作用几乎没人研究'),
    ('结构较轻', '可能存在“治疗窗口”', 'lorecivivint 只在内侧关节间隙 > 3 mm 者中见效')], 10)

phases('这些结论能信几分（编者评价）', [
    ('站得住的', GR, (40, 120, 60), [
        '作者明确区分了证据来源：同行评议论文、会议摘要、试验注册记录和公司新闻稿，并在表 1 逐项标注',
        '对阴性结果不回避：多数靶点在 III 期失败，作者都写了出来',
        '“结构改善不等于症状改善”“OA 异质性大、需要分层”这两条判断，有 MIV-711、lorecivivint 等多项试验支撑']),
    ('要打折扣的', OR, RED, [
        '这是叙述性综述，没有写检索策略、纳入标准和偏倚评估，选哪些药、怎么评价都带作者主观判断',
        '相当一部分内容来自会议摘要、注册网站和公司新闻稿，原文自己也说要谨慎解读',
        '利益冲突密集：Conaghan 是 LEVI-04、MIV-711 试验的第一作者，并为 Levicept、Biosplice、Kolon TissueGene、Genascence、Pacira 等相关公司做顾问；Berenbaum 是开发关节腔 GLP1 激动剂的 4Moving Biotech 联合创始人',
        '摘要把“局部给药的 GLP1 受体激动剂”列为已显示令人鼓舞信号的疗法，正文却只有一项 I 期安全性研究',
        '几乎只谈药物和介入，运动、教育等一线非药物治疗只在引言一笔带过']),
], 11)

phases('落到临床（编者建议）', [
    ('基础不变', LT, TEAL, [
        '运动训练、患者教育和减重仍是膝骨关节炎管理的基础，这篇综述里没有任何新药可以替代它们',
        '原文提到的现有药物和注射只能带来小幅、短暂的缓解，且不改变结构进展']),
    ('用减重药的患者', GR, (40, 120, 60), [
        '原文提醒：快速减重可能带来肌少性肥胖，尤其是老年人，需要同时做抗阻训练、保证蛋白质摄入',
        '约 30%～50% 的人一年内停用 GLP1 受体激动剂，停药后体重常反弹，运动习惯要提前建立（编者观点）']),
    ('和患者沟通时', OR, RED, [
        '富血小板血浆、干细胞注射在高质量随机对照试验中没有显示优于安慰剂，结构修复更没有证据',
        '射频消融、膝动脉栓塞等介入，随机证据只支持短期小幅镇痛，原文认为暂不宜在研究之外广泛使用',
        '多数“新药”还在 II 期或更早，患者问到时可以如实说明“还在试验阶段”']),
], 12)

# 封面：原文图 1 左侧膝关节示意（滑膜、软骨、软骨下骨），按 900×383 裁切
cover_from(fig1, 0.27, 0.42)
