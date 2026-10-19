#!/usr/bin/env python3
"""Berdishevsky 2016 七大脊柱侧弯特定运动学派综述（Scoliosis and Spinal Disorders）：原文图 1～97 全部使用。
带矢量箭头/标注的图从页面区域渲染（英文单词先涂白，单字母与数字保留）；位图内含英文的图（2、12、46、47、49、68、74、81）
逐处覆盖为中文，品牌字样（15、81、83）模糊；图 24、20、28、54 补中文标注或图例。按学派分组拼板，每格加中文标题。
用法：python3 make_figs.py <原文 PDF> <输出目录>"""
import sys, re
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

PDF, OUT = sys.argv[1], sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, s)
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233)
doc = pymupdf.open(PDF)
KEEP = re.compile(r'^([A-Fa-f]|[A-F][,)]?|\d+°?|>?\d+\s?%|\+)$')
DPI = 220
RAW = {2, 12, 15, 23, 46, 47, 49, 68, 74, 81, 83}


# ---------- 找每张图的位置 ----------
def locate():
    res = {}
    for i, p in enumerate(doc):
        blocks = p.get_text('blocks')
        caps = [b for b in blocks if re.match(r'Fig\. \d+', b[4])]
        ims = [x for x in p.get_image_info(xrefs=True) if x['width'] > 150 and x['bbox'][3] - x['bbox'][1] > 30]
        for c in caps:
            n = int(re.match(r'Fig\. (\d+)', c[4]).group(1))
            prev = [b[3] for b in caps if b[3] < c[1] and not (b[2] < c[0] or b[0] > c[2])]
            top = max(prev) if prev else 0
            mine = [x for x in ims if x['bbox'][3] <= c[1] + 5 and x['bbox'][1] >= top - 2 and not (x['bbox'][2] < c[0] or x['bbox'][0] > c[2])]
            if not mine: continue
            res[n] = dict(page=i, x0=min([c[0]] + [x['bbox'][0] - 2 for x in mine]), x1=max([c[2]] + [x['bbox'][2] + 2 for x in mine]), y0=min(x['bbox'][1] for x in mine) - 3, y1=c[1] - 2,
                          xref=sorted(mine, key=lambda x: -x['width'] * x['height'])[0]['xref'],
                          ibot=max(x['bbox'][3] for x in mine))
    return res


LOC = locate()
red_done = set()
WORDS = {}


def clip(n):
    L = LOC[n]; p = doc[L['page']]
    if L['page'] not in red_done:
        WORDS[L['page']] = p.get_text('words')
        for w in WORDS[L['page']]:
            if not KEEP.match(w[4]):
                p.add_redact_annot(pymupdf.Rect(w[:4]), fill=(1, 1, 1))
        p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
        red_done.add(L['page'])
    r = pymupdf.Rect(L['x0'], L['y0'], L['x1'], L['y1'])
    pm = p.get_pixmap(dpi=DPI, clip=r)
    return Image.frombytes('RGB', (pm.width, pm.height), pm.samples), r


def raw(n):
    return Image.open(BytesIO(doc.extract_image(LOC[n]['xref'])['image'])).convert('RGB')


def ctext(dr, cx, y, t, f, fill=INK):
    dr.text((cx - dr.textlength(t, font=f) / 2, y), t, font=f, fill=fill)


def blur(im, b, r=8):
    im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r)), b[:2])


def cover(im, box, lines, fs, fill='white', col=INK, center=True):
    dr = ImageDraw.Draw(im); dr.rectangle(box, fill=fill)
    h = len(lines) * (fs + 4); y = (box[1] + box[3] - h) / 2
    for l in lines:
        if center: ctext(dr, (box[0] + box[2]) / 2, y, l, font(fs), col)
        else: dr.text((box[0] + 4, y), l, font=font(fs), fill=col)
        y += fs + 4


def trim(im):
    """裁掉四周纯白边"""
    g = im.convert('L').point(lambda v: 255 if v < 245 else 0)
    b = g.getbbox()
    return im.crop((max(0, b[0] - 4), max(0, b[1] - 4), min(im.width, b[2] + 4), min(im.height, b[3] + 4))) if b else im


def legend(items, W):
    """items: [(颜色, 形状, 文字)]"""
    H = 20 + len(items) * 44; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
    for i, (c, s, t) in enumerate(items):
        y = 12 + i * 44
        if s == 'arrow':
            dr.rectangle([20, y + 12, 60, y + 22], fill=c); dr.polygon([(60, y + 6), (76, y + 17), (60, y + 28)], fill=c)
        else:
            dr.pieslice([28, y + 2, 60, y + 34], 90, 270, fill=c)
        dr.text((92, y + 4), t, font=font(24), fill=INK)
    return im


# ---------- 各图 ----------
def fig(n):
    if n in RAW:
        im = raw(n)
        if n == 2:
            im = im.resize((round(im.width * 1.5), round(im.height * 1.5)), Image.LANCZOS); s = 1.5
            for b, t in [((0, 0, 160, 28), ['诱发事件']), ((85, 120, 210, 200), ['椎体', '楔形变']), ((448, 120, 545, 190), ['脊柱', '弯曲']),
                         ((415, 390, 545, 458), ['不对称', '负荷']), ((98, 380, 222, 452), ['不对称', '生长'])]:
                cover(im, tuple(int(v * s) for v in b), t, 32)
        elif n == 12:
            im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
            top = [['侧弯出现前', '（<7 岁）'], ['青春期生长前', '（女孩 7～11 岁）'], ['青春期生长中', '（11～15 岁）'], ['骨量积累期', '（15～20 岁）']]
            bot = [['多走路、', '双足活动'], ['平衡训练'], ['调整两侧', '椎旁肌张力'], ['台阶、负重、', '轴向冲击']]
            for k, (x0, x1) in enumerate([(28, 118), (128, 218), (238, 328), (345, 437)]):
                c = im.getpixel((int((x0 + 45) * 3), int(48 * 3)))
                for (y0, y1), txt in [((42, 87), top[k]), ((229, 271), bot[k])]:
                    col = INK if k == 1 else 'white'
                    cover(im, (x0 * 3 + 6, y0 * 3 + 6, x1 * 3 - 6, y1 * 3 - 6), txt, 30, c, col)
            cover(im, (0, 0, 860, 90), ['Lyon 学派：不同年龄的运动建议'], 46, (0, 0, 0), (255, 190, 60))
        elif n == 15:
            blur(im, (100, 258, 195, 286), 6)
        elif n == 46:
            im = im.resize((round(im.width * 1.4), round(im.height * 1.4)), Image.LANCZOS); s = 1.4
            for b, t in [((98, 38, 160, 78), ['3C']), ((300, 38, 362, 78), ['4C']), ((498, 38, 588, 78), ['N3N4']), ((795, 26, 912, 72), ['腰/胸腰']),
                         ((310, 112, 385, 142), ['胸段']), ((310, 202, 372, 232), ['腰段']), ((498, 138, 572, 168), ['胸段']), ((502, 202, 568, 232), ['腰段'])]:
                cover(im, tuple(int(v * s) for v in b), t, 28)
        elif n == 47:
            im = im.crop((0, 0, im.width, 505))
            c = im.getpixel((10, 95))
            ImageDraw.Draw(im).rectangle([18, 83, 972, 114], fill=c)
            for (x0, x1), t in [((18, 305), '三弯 A1、A2、A3'), ((305, 530), '四弯 B1、B2'), ((530, 715), 'N3N4 C1、C2'), ((715, 972), '单腰/胸腰弯 E1、E2')]:
                ctext(ImageDraw.Draw(im), (x0 + x1) / 2, 86, t, font(24))
        elif n == 49:
            cover(im, (0, 0, 118, 55), ['自我延伸', '侧向矫正', '去旋转', '矢状面正常化'], 11, 'white', INK, False)
        elif n == 68:
            cover(im, (298, 676, 770, 729), ['不同手位塑造矢状面背部形态'], 28, (170, 200, 235))
        elif n == 74:
            cover(im, (805, 308, 905, 356), ['胸弯'], 26)
        elif n == 81:
            blur(im, (183, 58, 292, 118), 7)
            cover(im, (28, 266, 447, 304), ['腰盆稳定：在稳定的基础上活动'], 22, (40, 120, 130), 'white')
        elif n == 83:
            blur(im, (60, 60, 152, 100), 6); blur(im, (310, 60, 402, 100), 6)
        return im
    im, r = clip(n)
    s = DPI / 72; dr = ImageDraw.Draw(im)
    if n == 24:
        for w0, t in [((220, 476), '肩带块'), ((222, 509), '胸段块'), ((222, 541), '腰段块'), ((222, 575), '髋-骨盆块')]:
            x = (w0[0] - r.x0) * s; y = (w0[1] - r.y0) * s
            dr.text((x, y - 2), t, font=font(26), fill=INK)
    if n == 20:
        for w in WORDS[LOC[20]['page']]:
            if w[4] in ('year', 'years') and r.contains(pymupdf.Rect(w[:4])):
                x = (w[0] - r.x0) * s; y = (w[1] - r.y0) * s
                dr.rectangle([x - 50, y - 6, x + 120, y + 40], fill='white')
                dr.text((x - 44, y - 4), '停用 1 年' if w[4] == 'year' else '停用 2 年', font=font(30), fill=INK)
    if n == 69:
        w_, h_ = im.size; blur(im, (int(w_ * 0.68), 0, w_, int(h_ * 0.33)), 10)
    if n == 25:
        im = im.crop((0, 0, im.width, int((LOC[25]['ibot'] - r.y0) * s) + 4))
    if n in (28, 54):
        im = im.crop((0, 0, im.width, int((LOC[n]['ibot'] - r.y0) * s) + 6))
        im = trim(im)
        lg = legend([((210, 80, 30), 'arrow', '红/橙箭头：凸侧向前、向内收缩'), ((40, 190, 190), 'arrow', '青色箭头：躯干上下延伸'),
                     ((60, 200, 60), 'moon', '绿色半月：凹侧向外、向后扩张'), ((60, 110, 190), 'arrow', '蓝箭头：肩部牵引')], im.width)
        out = Image.new('RGB', (im.width, im.height + lg.height), 'white'); out.paste(im, (0, 0)); out.paste(lg, (0, im.height)); im = out
    return trim(im)


CAP = {
    1: 'Lyon 学派负责人 de Mauroy 医生', 2: '侧弯进展的“恶性循环”（左）与坐姿矫正（右）', 3: '借助录像实时反馈，认识自己的姿势缺陷',
    4: '胸段主动松动，促进胸椎后凸', 5: '腰段主动矫正，促进腰椎前凸', 6: '胸段侧移：持棍（左）、瑞士球上（右）',
    7: '胸段侧移 + 胸廓去旋转（X 线与示意图箭头示方向）', 8: '平衡与本体感觉：瑞士球（左）、平衡板（右）', 9: '脊柱稳定训练',
    10: '石膏背心内练习：核心力量、呼吸与胸段侧移、躯干延伸', 11: '石膏背心内练习：姿势矫正（左）、核心力量（右）',
    12: '按年龄推荐的运动', 13: '穿石膏背心用呼吸训练器，增加肺活量', 14: '胸段主动松动（右图箭头为胸廓松动方向）',
    15: '腰段主动松动（右上为腰弯示意）', 16: '肋椎关节松动', 17: '穿支具打篮球，帮助纵向伸展和脊柱灵活性',
    18: 'ARTbrace 支具前面（左）与后面（右），4 mm 聚碳酸酯', 19: '病例 S：13 岁胸弯 39°、胸椎后凸减小（a、c）；穿支具后侧弯减小、后凸增加（b、d）',
    20: '病例 S 停用支具 1 年、2 年后，Cobb 角减少一半以上', 21: '德国巴特索伯恩海姆的 Asklepios Katharina Schroth 诊所',
    22: 'Schroth 治疗师培训负责人 Axel Hennes', 23: 'Schroth 历史：Katharina 与女儿 Christa（右上），户外集体训练',
    24: 'Schroth 体块：解剖（a）、示意（b）、变形为梯形（c）、腰弯患者（d）', 25: '24 岁重度侧弯：治疗前（a）、强化旋转成角呼吸训练 9 个月（b）和 12 个月（c）',
    26: '腰段松动（左）与侧弯柔韧性练习（右）', 27: '“50 次瑞士球”：镜前坐球（左）、扶肋木三维自我矫正（右）',
    28: '俯卧练习：右髋屈曲激活髂腰肌，配合肩部牵引/反牵引', 29: '“帆”练习：站半圆泡沫轴、双手持杆，扩张左侧凹陷胸廓（红圈）',
    30: '“肌肉圆柱”（侧卧）练习：侧卧在腰凸侧，矫正腰弯', 31: '坐位、站位的三维姿势矫正，融入日常生活',
    32: 'SEAS 学派负责人：Antonio Negrini、Michele Romano、Alessandra Negrini', 33: '支具前的右胸弯松动，增加脊柱活动度',
    34: '支具内练习：俯卧抬离胸骨垫增加胸椎后凸（a、b）；站立腹部后移，加大腰垫压力（c、d）', 35: '脊柱松动与柔韧性练习',
    36: '学习初期用平衡板辅助', 37: '平衡板上保持自我矫正：单腿站（左）、屈膝（右）',
    38: '日常生活中保持自我矫正：坐（a）、前倾准备站起（b、c）、站立（d）、靠墙（e、f）', 39: '鼓励参加各种体育运动', 40: '鼓励正常生活',
    41: '不戴支具做 SEAS 2 年前后（照片与 X 线）', 42: '不戴支具做 SEAS 3.5 年前后（照片与 X 线）', 43: 'Sibilla 支具：用于 30° 以内的轻度进展性侧弯',
    44: 'Sforzesco 支具：用于 45°～50° 的重度侧弯', 45: 'BSPTS 创始人：Elena Salvá、Gloria Quera-Salvá、Manuel Rigo',
    46: 'BSPTS 分型：3C、4C、N3N4、单腰/胸腰弯（体块图与照片）', 47: 'Rigo 影像学分型（CSL 骶骨中垂线；TP 过渡点；TL 胸腰段；D 为近端胸弯修饰）',
    48: '三维主动自我矫正：扩张塌陷处、打开凹侧（a、b）', 49: '左腰/胸腰弯伴骨盆右移，双杆站立应用矫正原则 1～5（棕箭头肩牵引、蓝箭头肩反牵引与骨盆回中）',
    50: '扩张/收缩技术：蓝、黑箭头为躯干扩张，红色为绕凸起向前向内的力', 51: '旋转成角呼吸前（a）与呼吸中（b）：把气吸进塌陷的肺',
    52: '腰弯中髂腰肌的激活方向，帮助腰弯去侧弯、去旋转', 53: '治疗师协助松动左侧凹陷的肋骨，向外向后扩张胸廓', 54: '仰卧练习（腰弯为主）',
    55: '侧卧练习：腰弯为主（上）、胸弯为主（下）', 56: '俯卧凳上练习：腰凸侧下肢外展、脚凳垫高骨盆', 57: '“肌肉圆柱”练习：用于中重度腰弯，高阶动作',
    58: '日常生活姿势：睡、站、背包、弯腰、提物、够物，穿支具睡和坐', 59: '正确坐姿需要宣教和分步训练', 60: 'Rigo-Chêneau 支具各角度',
    61: 'Rigo-Chêneau 支具：胸弯 38°（a）→ 支具内矫正 >50%（b）→ 生长结束时 24%（c）', 62: 'Dobomed 创始人 Krystyna Dobosiewicz 教授（1931—2007）',
    63: 'Dobomed 典型练习：加胸椎后凸前（a）、后（b），四肢固定骨盆和肩带', 64: '“相锁”呼吸：9 张连续照片，凹侧塌陷的肺逐渐充满，手指轻压辅助',
    65: '旋转成角呼吸：患者演示（左）与胸廓矫正方向示意（右）', 66: '“休息”练习：最大胸椎后凸（a）与腰椎前凸（b），同时保持三维矫正',
    67: '“高位”进阶：从坐到跪再到站，全程保持三维矫正', 68: 'Dobomed 各种对称体位一览', 69: '侧移法负责人 Tony Betts（英国）',
    70: '“提踵”练习：左胸腰弯（a），中立位（b），提起凸侧脚跟、髋膝伸直（c）', 71: '“提踵-侧移”练习：双弯（a），中立（b），提踵（c），手固定腰弯、躯干向胸弯凹侧移（d）',
    72: '保持侧移位做稳定训练：鸟狗（左）、平板（右）', 73: '侧向（a）与矢状面（b）躯干松动', 74: '右胸弯站立位辅助侧移序列（右图为脊柱矫正方向）',
    75: '左胸腰弯：不穿支具（a、b）与穿支具（c、d）向右侧移', 76: '右胸弯：靠墙（a、b）与站立（c～e）侧移平衡稳定', 77: '坐到站（a）与站立（b）中的侧移',
    78: 'FITS 创始人 Marianna Białek 与 Andrzej M’hango', 79: '感觉运动平衡训练：从坐到站时看实时视频调整姿势', 80: '放松限制三维矫正的筋膜结构（腘绳肌）',
    81: '腰盆稳定：保持腰椎骨盆稳定，慢慢伸左髋', 82: '筋膜受限时额状面侧移更难：治疗前（a）、筋膜治疗后（b）',
    83: '仰卧矫正呼吸，脊柱侧弯尺显示呼气（a）与吸气（b）时肋骨扩张的位置', 84: '支具内三维矫正呼吸：向凹侧吸气（红色标记为凸侧）',
    85: '坐位三维矫正呼吸，红色弹力带辅助自我延伸', 86: '坐位（a）、站位（b）检查脊柱柔韧性', 87: '用 X 线片和脊柱模型帮助患者认识畸形',
    88: '平衡板上看实时视频做姿势矫正', 89: '仰卧在两个平衡垫上，双脚把球顶在肋木上保持平衡',
    90: '股直肌放松 + 去旋转手法（a）；趴在泡沫轴上做竖脊肌筋膜放松（b）', 91: '坐位练习双足正确负重',
    92: 'FITS 稳定练习：泡沫轴 + 平衡垫（a）、跪瑞士球（b）、顶球（c）、站双垫顶垫（d）、四点跪平衡板（e）',
    93: '弹力带矫正模式练习：先由治疗师协助，再独立完成', 94: '弹力带矫正模式练习', 95: '坐位姿势矫正前（a）后（b）',
    96: '12 岁左胸腰弯，支具 + FITS 后外观改善', 97: '15 岁双弯（上胸弯 32°、胸腰弯 36°），FITS 后外观改善'}


def save(im, name):
    im.convert('RGB').save(f'{OUT}/{name}.jpg', quality=85)


def board(nums, title, W=1200, maxh=900):
    tiles = []
    for n in nums:
        im = fig(n)
        s = min(W / im.width, maxh / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        t = Image.new('RGB', (W, im.height + 82), 'white'); dr = ImageDraw.Draw(t)
        dr.rounded_rectangle([0, 6, W, 64], 8, fill=LT)
        txt = f'图 {n}　{CAP[n]}'; fs = 28
        while dr.textlength(txt, font=font(fs)) > W - 30 and fs > 18: fs -= 1
        dr.text((14, 35 - fs // 2), txt, font=font(fs), fill=TEAL)
        t.paste(im, ((W - im.width) // 2, 74)); tiles.append(t)
    H = sum(t.height for t in tiles) + 90 + 16 * len(tiles)
    out = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(out)
    dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white')
    y = 90
    for t in tiles: out.paste(t, (0, y)); y += t.height + 16
    return out


GROUPS = [
    ('l1', [1, 3, 4, 5], 'Lyon 学派（法国）①　认识畸形与主动松动'), ('l2', [6, 7, 8, 9], 'Lyon 学派②　侧移、去旋转与稳定'),
    ('l3', [10, 11, 13], 'Lyon 学派③　石膏背心与支具内练习'), ('l4', [12], 'Lyon 学派④　运动建议'),
    ('l5', [14, 15, 16, 17], 'Lyon 学派⑤　松动与运动'), ('l6', [18, 19, 20], 'Lyon 学派⑥　ARTbrace 支具与病例'),
    ('s1', [21, 22, 23], 'Schroth 学派（德国）①　诊所与历史'), ('s2', [24, 25], 'Schroth 学派②　体块分型与呼吸疗效'),
    ('s3', [26, 27], 'Schroth 学派③　松动与“50 次瑞士球”'), ('s4', [28, 29, 30], 'Schroth 学派④　俯卧、“帆”与“肌肉圆柱”'),
    ('s5', [31], 'Schroth 学派⑤　日常生活矫正'),
    ('e1', [32, 33, 34], 'SEAS 学派（意大利）①　支具前后的练习'), ('e2', [35, 36, 37], 'SEAS 学派②　松动与平衡'),
    ('e3', [38, 39, 40], 'SEAS 学派③　日常生活与运动'), ('e4', [41, 42], 'SEAS 学派④　不戴支具的病例'), ('e5', [43, 44], 'SEAS 学派⑤　两种支具'),
    ('b1', [45, 46], 'BSPTS 学派（西班牙）①　创始人与分型'), ('b2', [47], 'BSPTS 学派②　Rigo 影像学分型'),
    ('b3', [48, 49, 50], 'BSPTS 学派③　三维自我矫正'), ('b4', [51, 52, 53], 'BSPTS 学派④　呼吸、肌肉激活与松动'),
    ('b5', [54, 55], 'BSPTS 学派⑤　仰卧与侧卧练习'), ('b6', [56, 57], 'BSPTS 学派⑥　俯卧与“肌肉圆柱”'),
    ('b7', [58, 59], 'BSPTS 学派⑦　日常生活'), ('b8', [60, 61], 'BSPTS 学派⑧　Rigo-Chêneau 支具'),
    ('d1', [62, 63, 64], 'Dobomed 学派（波兰）①　闭链后凸与“相锁”呼吸'), ('d2', [65, 66, 67], 'Dobomed 学派②　呼吸、“休息”与“高位”'),
    ('d3', [68], 'Dobomed 学派③　对称体位'),
    ('h1', [69, 70, 71], '侧移法（英国）①　提踵与提踵-侧移'), ('h2', [72, 73, 74], '侧移法②　稳定、松动与站立侧移'),
    ('h3', [75, 76, 77], '侧移法③　穿支具、平衡与日常侧移'),
    ('f1', [78, 79, 80, 81], 'FITS 学派（波兰）①　平衡、筋膜与腰盆稳定'), ('f2', [82, 83, 84, 85], 'FITS 学派②　侧移与三维矫正呼吸'),
    ('f3', [86, 87, 88, 89], 'FITS 学派③　检查、宣教与感觉运动训练'), ('f4', [90, 91, 92], 'FITS 学派④　放松、足部负重与稳定'),
    ('f5', [93, 94], 'FITS 学派⑤　弹力带矫正模式'), ('f6', [95, 96, 97], 'FITS 学派⑥　姿势矫正与病例')]

# ---------- 首图 ----------
W, H = 1400, 600; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 18, H], fill=TEAL)
dr.text((70, 60), '综述 · 《脊柱侧弯与脊柱疾病》2016', font=font(32), fill=TEAL)
for i, t in enumerate(['脊柱侧弯特定运动：', '七大学派一次看懂']):
    dr.text((70, 140 + i * 82), t, font=font(58), fill=INK)
dr.text((70, 330), 'Lyon · Schroth · SEAS · BSPTS · Dobomed · 侧移法 · FITS', font=font(30), fill=GREY)
dr.line([70, 410, W - 70, 410], fill=(200, 205, 210), width=2)
dr.text((70, 440), 'Berdishevsky H 等，Scoliosis Spinal Disord 2016;11:20', font=font(30), fill=GREY)
dr.text((70, 495), '编者中文重排，仅作学术交流', font=font(26), fill=(150, 150, 150))
save(im, 'img01')

# ---------- 共同要素卡 ----------
W, H = 1400, 980; im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
pts = [('三维自我矫正', '在冠状面、矢状面、水平面同时纠正：侧移回中、去旋转、恢复胸椎后凸和腰椎前凸', LT),
       ('稳定矫正后的姿势', '用等长肌肉收缩把矫正“锁住”，再在越来越难的条件下保持', LT),
       ('融入日常生活', '坐、站、起身、背包、睡觉时都按自己的弯型保持矫正', LT),
       ('认识自己的畸形', '镜子、录像、X 线片、脊柱模型，帮患者“看见”并“感觉到”侧弯', GR),
       ('呼吸矫正', '多数学派把气吸进凹陷一侧（旋转成角呼吸），帮助胸廓去旋转', GR),
       ('团队与个体化', '治疗师与骨科医生、支具师、心理医生合作；按年龄、弯型、风险调整强度', GR)]
for i, (t, s, bg) in enumerate(pts):
    y = 20 + i * 158
    dr.rounded_rectangle([20, y, W - 20, y + 142], 14, fill=bg)
    dr.text((50, y + 18), f'{i + 1}　{t}', font=font(36), fill=TEAL)
    line, yy = '', y + 76
    for ch in s:
        if dr.textlength(line + ch, font=font(28)) > 1290: dr.text((50, yy), line, font=font(28), fill=INK); yy += 38; line = ch
        else: line += ch
    dr.text((50, yy), line, font=font(28), fill=INK)
out = Image.new('RGB', (W, H + 90), 'white'); od = ImageDraw.Draw(out)
od.rectangle([0, 0, W, 76], fill=TEAL); od.text((24, 16), '各学派的共同点（国际侧弯矫形康复学会认可的三大要素 + 编者整理）', font=font(36), fill='white')
out.paste(im, (0, 90)); save(out, 'img02')

# 图 2 单独
save(board([2], '侧弯为什么会越弯越重：Stokes 与 Burwell 的“恶性循环”'), 'img03')
for i, (k, nums, t) in enumerate(GROUPS):
    save(board(nums, t), f'img{i + 4:02d}')
    print(k, end=' ', flush=True)

# 封面
c = fig(29); s = 900 / c.width; c = c.resize((900, round(c.height * s)), Image.LANCZOS)
top = int(c.height * 0.12); c.crop((0, top, 900, top + 383)).save(f'{OUT}/cover.jpg', quality=90)
print('\nok', len(GROUPS) + 3)
