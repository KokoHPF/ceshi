#!/usr/bin/env python3
"""cardkit：把“每张卡片放什么”变成 3:4 小红书图文卡片的排版引擎。

只依赖 Pillow（画数据图时另需 matplotlib）。典型用法：

    import sys; sys.path.insert(0, 'path/to/skills/paper-to-xhs-cards/scripts')
    from cardkit import Deck
    deck = Deck(series='后肩不稳', source='Boileau 等 Arthrosc Tech 2022;11(9):e1613')
    deck.cover(['一根拇指', '查后肩不稳'], subtitle='……', photos=[(img, '标签'), ...], banner='……')
    deck.figure('标题', '副标题', [img1, img2], ['标签1', '标签2'], items=[...])
    deck.text('标题', '副标题', items=[...])
    deck.save('out_dir')        # 写出 card01.jpg … 并生成 overview.jpg 供检查

items（文字块）格式，按顺序纵向排列，字号自动取能放下的最大值：
    ('h', '小标题')
    ('steps', [('1', '第一步'), ('2', '第二步'), ('!', '注意')])   # 圆形序号徽章，徽章内容任意短文本
    ('bul', ['要点 1', '要点 2'])                                 # 圆点列表
    ('box', '框标题', '框内文字', 'teal')                          # 彩色信息框，样式见 BOX_STYLES
文字里 **加粗强调色**、==黄色高亮==，换行用 \\n。
"""
import json
import os
import re
from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOBREAK = set('0123456789.%~～-–/×:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ°²')
NO_LINE_START = set('，。、；：！？）」”’%')


def _hex(c):
    if isinstance(c, (list, tuple)): return tuple(c)
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _merge(a, b):
    out = dict(a)
    for k, v in (b or {}).items():
        out[k] = _merge(a[k], v) if isinstance(v, dict) and isinstance(a.get(k), dict) else v
    return out


def load_theme(theme=None):
    """theme：None / JSON 路径 / dict。只需写要覆盖的字段。"""
    base = json.load(open(os.path.join(ROOT, 'config', 'theme.default.json'), encoding='utf-8'))
    if isinstance(theme, str): theme = json.load(open(theme, encoding='utf-8'))
    return _merge(base, theme or {})


class Deck:
    def __init__(self, series, source, theme=None, fonts_dir=None):
        self.t = load_theme(theme)
        self.W, self.H = self.t['size']
        C = {k: _hex(v) for k, v in self.t['colors'].items() if not k.startswith('_')}
        self.C = C
        self.series, self.source = series, source
        self.BOX = {  # 信息框样式：(底色, 标题色)
            'teal': (C['light_teal'], C['teal']), 'accent': (C['light_accent'], C['accent']),
            'coral': (C['light_accent'], C['accent']), 'yellow': (C['light_highlight'], C['primary']),
            'navy': (C['light_primary'], C['primary']), 'primary': (C['light_primary'], C['primary']),
            'purple': (C['light_purple'], C['purple']), 'grey': (C['grey_box'], C['muted'])}
        fd = fonts_dir or self.t['fonts']['dir']
        if not os.path.isabs(fd): fd = os.path.join(ROOT, fd)
        self._fontfile = {}
        for w, key in (('R', 'regular'), ('M', 'medium'), ('B', 'bold'), ('K', 'black')):
            p = os.path.join(fd, self.t['fonts'][key])
            if not os.path.exists(p):
                p = next((f for f in self.t['fonts']['fallback'] if os.path.exists(f)), None)
                if p is None: raise SystemExit('找不到中文字体：先运行 scripts/setup_fonts.sh，或在主题里指定 fonts')
            self._fontfile[w] = p
        self._fc = {}
        self.pages = []  # 延迟渲染：保存时才知道总页数

    # ---------- 基础 ----------
    def F(self, w, s):
        k = (w, int(s))
        if k not in self._fc: self._fc[k] = ImageFont.truetype(self._fontfile[w], int(s))
        return self._fc[k]

    def tokens(self, t):
        out = []
        for part in re.split(r'(\*\*.+?\*\*|==.+?==)', t):
            if not part: continue
            if part.startswith('**'): out.append((part[2:-2], 'em'))
            elif part.startswith('=='): out.append((part[2:-2], 'hl'))
            else: out.append((part, 'n'))
        return out

    def layout(self, t, w, fs, wt='R'):
        """逐字排版：数字、字母、%、° 等连写不拆行；标点不落行首"""
        lines = [[]]; cur = 0
        for txt, st in self.tokens(t):
            f = self.F('B' if st != 'n' else wt, fs); i = 0
            while i < len(txt):
                ch = txt[i]
                if ch == '\n': lines.append([]); cur = 0; i += 1; continue
                j = i + 1
                if ch in NOBREAK:
                    while j < len(txt) and txt[j] in NOBREAK: j += 1
                seg = txt[i:j]; sw = sum(f.getlength(x) for x in seg)
                if cur + sw > w and lines[-1] and not (len(seg) == 1 and seg in NO_LINE_START):
                    lines.append([]); cur = 0
                for x in seg: cw = f.getlength(x); lines[-1].append((x, st, cw)); cur += cw
                i = j
        return lines

    def rich(self, d, x, y, t, w, fs, col=None, wt='R', lh=1.45, em=None):
        col = col or self.C['ink']; em = em or self.C['accent']
        for ln in self.layout(t, w, fs, wt):
            xx = x; i = 0
            while i < len(ln):
                st = ln[i][1]; j = i
                while j < len(ln) and ln[j][1] == st: j += 1
                s = ''.join(c for c, _, _ in ln[i:j]); ww = sum(cw for _, _, cw in ln[i:j])
                if st == 'hl': d.rectangle([xx - 2, y + fs * .55, xx + ww + 2, y + fs * 1.15], fill=self.C['highlight'])
                d.text((xx, y), s, font=self.F('B' if st != 'n' else wt, fs),
                       fill=em if st == 'em' else (self.C['primary'] if st == 'hl' else col))
                xx += ww; i = j
            y += round(fs * lh)
        return y

    def th(self, t, w, fs, wt='R', lh=1.45):
        return len(self.layout(t, w, fs, wt)) * round(fs * lh)

    @staticmethod
    def rmask(w, h, r):
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255); return m

    def shadow(self, c, box, r=24, off=8, blur=18, alpha=40):
        x0, y0, x1, y1 = box
        sh = Image.new('RGBA', (x1 - x0 + 80, y1 - y0 + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([40, 40, 40 + x1 - x0, 40 + y1 - y0], r, fill=(60, 40, 20, alpha))
        sh = sh.filter(ImageFilter.GaussianBlur(blur)); c.paste(sh, (x0 - 40, y0 - 40 + off), sh)

    @staticmethod
    def fit(im, w, h, fy=.5, fx=.5):
        s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        x0 = round((im.width - w) * fx); y0 = round((im.height - h) * fy)
        return im.crop((x0, y0, x0 + w, y0 + h))

    def photo(self, c, im, box, r=22, fy=.5, fx=.5, tag=None, tagc=None, sh=True):
        """把图裁切填满 box（会裁边）；tag 为左上角标签"""
        x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
        if sh: self.shadow(c, box, r)
        c.paste(self.fit(im.convert('RGB'), w, h, fy, fx), (x0, y0), self.rmask(w, h, r))
        if tag:
            d = ImageDraw.Draw(c); f = self.F('B', 30); tw = d.textlength(tag, font=f)
            d.rounded_rectangle([x0 + 14, y0 + 14, x0 + 42 + tw, y0 + 64], 14, fill=tagc or self.C['primary'])
            d.text((x0 + 28, y0 + 19), tag, font=f, fill=self.C['white'])

    def put(self, c, im, x0, y0, w, h, r=18):
        """按给定尺寸整图缩放（不裁边）"""
        self.shadow(c, (x0, y0, x0 + w, y0 + h), r)
        c.paste(im.convert('RGB').resize((w, h), Image.LANCZOS), (x0, y0), self.rmask(w, h, r))

    def badge(self, d, x, y, t, col, r=22, fs=26):
        w = max(2 * r, d.textlength(t, font=self.F('K', fs)) + 20)
        d.rounded_rectangle([x, y, x + w, y + 2 * r], r, fill=col)
        d.text((x + w / 2 - d.textlength(t, font=self.F('K', fs)) / 2, y + r - fs * .68), t, font=self.F('K', fs), fill=self.C['white'])
        return w

    # ---------- 文字块 ----------
    def render_items(self, c, y, items, fs, dry=False, X=60, Wd=None, gap=14, lg=10):
        Wd = Wd or (self.W - 120); d = ImageDraw.Draw(c); C = self.C
        for it in items:
            kind = it[0]
            if kind == 'h':
                if not dry: d.text((X, y), it[1], font=self.F('K', fs + 6), fill=C.get(it[2], C['primary']) if len(it) > 2 else C['primary'])
                y += round((fs + 6) * 1.5)
            elif kind == 'steps':
                for k, t in it[1]:
                    bw = self.F('K', 26).getlength(k) + 20; w = max(44, bw)
                    col = C['accent'] if k in ('!', '✗') else (C['teal'] if len(k) == 1 else C['primary'])
                    if not dry: self.badge(d, X, y + max(0, (fs - 44) // 2) + 2, k, col)
                    y = (self.rich(d, X + w + 16, y, t, Wd - w - 16, fs) if not dry else y + self.th(t, Wd - w - 16, fs)) + lg
            elif kind == 'bul':
                col = C.get(it[2], C['accent']) if len(it) > 2 else C['accent']
                for t in it[1]:
                    if not dry:
                        d.ellipse([X, y + fs * .42, X + 14, y + fs * .42 + 14], fill=col)
                        y = self.rich(d, X + 32, y, t, Wd - 32, fs) + lg
                    else: y += self.th(t, Wd - 32, fs) + lg
            elif kind == 'box':
                _, title, t, style = it
                fill, col = self.BOX.get(style, self.BOX['teal'])
                hh = 24 + round((fs + 4) * 1.4) + self.th(t, Wd - 80, fs) + 18
                if not dry:
                    d.rounded_rectangle([X, y, X + Wd, y + hh], 26, fill=fill)
                    d.text((X + 32, y + 18), title, font=self.F('K', fs + 4), fill=col)
                    self.rich(d, X + 32, y + 24 + round((fs + 4) * 1.4), t, Wd - 80, fs)
                y += hh
            else:
                raise ValueError(f'未知文字块类型：{kind}')
            y += gap
        return y

    def auto(self, c, y, items, top=44, bottom=None):
        """字号取 ≤top 能放下的最大值；有空余时加大间距铺满版面"""
        bottom = bottom or self.H - 110
        hgt = 0
        for fs in range(top, 21, -1):
            hgt = self.render_items(c, 0, items, fs, dry=True)
            if y + hgt < bottom: break
        else:
            raise ValueError(f'文字放不下（{len(items)} 个块），请删减或拆成两张卡')
        spare = bottom - y - hgt
        n = sum(len(it[1]) if it[0] in ('steps', 'bul') else 1 for it in items) + len(items)
        self.render_items(c, y, items, fs, gap=14 + min(80, spare // max(1, n)), lg=10 + min(60, spare // max(1, n)))
        return fs

    # ---------- 页面骨架 ----------
    def _base(self, n, total, title, sub):
        C = self.C; c = Image.new('RGB', (self.W, self.H), C['bg']); d = ImageDraw.Draw(c)
        d.rounded_rectangle([60, 56, 200, 104], 24, fill=C['accent']); d.text((80, 58), f'{n:02d}/{total:02d}', font=self.F('B', 32), fill=C['white'])
        d.text((222, 62), f"{self.series} · {self.t['series_suffix']}", font=self.F('M', 28), fill=C['muted'])
        fs = 64
        while d.textlength(title, font=self.F('K', fs)) > self.W - 120 and fs > 40: fs -= 2
        d.text((60, 128 + (64 - fs) // 2), title, font=self.F('K', fs), fill=C['primary'])
        y = 220
        if sub: d.text((62, y), sub, font=self.F('M', 32), fill=C['muted']); y += 56
        d.line([60, self.H - 78, self.W - 60, self.H - 78], fill=(222, 214, 202), width=2)
        d.text((60, self.H - 62), self.t['account'], font=self.F('M', 24), fill=C['muted'])
        s = self.source; f = self.F('R', 22)
        while d.textlength(s, font=f) > self.W - 400 and len(s) > 10: s = s[:-2] + '…'
        d.text((self.W - 60 - d.textlength(s, font=f), self.H - 60), s, font=f, fill=C['muted'])
        return c, d, y + 10

    def _row(self, c, y, ims, tags, h):
        """一排等高图片，总宽不超过版心；返回底边 y"""
        cols = [self.C['accent'], self.C['teal'], self.C['primary']]
        ws = [im.width * h / im.height for im in ims]; s = min(1, (self.W - 120 - 16 * (len(ims) - 1)) / sum(ws)); h = round(h * s)
        ws = [round(w * s) for w in ws]; x = 60 + (self.W - 120 - sum(ws) - 16 * (len(ims) - 1)) // 2
        for i, (im, w) in enumerate(zip(ims, ws)):
            self.photo(c, im, (x, y, x + w, y + h), r=18, tag=(tags[i] if tags else None), tagc=cols[i % 3]); x += w + 16
        return y + h

    def _col(self, c, y, ims, tags, h):
        cols = [self.C['accent'], self.C['teal'], self.C['primary']]
        for i, im in enumerate(ims):
            hh = h; w = round(im.width * hh / im.height)
            if w > self.W - 120: w = self.W - 120; hh = round(im.height * w / im.width)
            x = 60 + (self.W - 120 - w) // 2
            self.photo(c, im, (x, y, x + w, y + hh), r=18, tag=(tags[i] if tags else None), tagc=cols[i % 3]); y += hh + 16
        return y - 16

    # ---------- 卡片类型 ----------
    def cover(self, title_lines, subtitle='', photos=(), banner='', kicker=''):
        """封面。title_lines：标题按行切好（论文标题中文直译）；首行白色，其余高亮色。
        photos：1～3 个 (图, 标签)。第 1 张放左侧大图，其余在右侧上下排。"""
        def draw(n, total):
            C = self.C; W, H = self.W, self.H; c = Image.new('RGB', (W, H), C['bg']); d = ImageDraw.Draw(c)
            f = lambda s: self.F('K', s)
            fs = 136
            while fs > 72 and max(d.textlength(t, font=f(fs)) for t in title_lines) > W - 110: fs -= 4
            lh = round(fs * 1.18); top = 150
            panel = top + lh * len(title_lines) + (100 if subtitle else 40)
            d.rectangle([0, 0, W, panel], fill=C['primary']); d.ellipse([720, -180, 1260, 360], fill=tuple(min(255, v + 18) for v in C['primary']))
            t = self.t['cover_tag']; tw = d.textlength(t, font=self.F('B', 34))
            d.rounded_rectangle([60, 64, 108 + tw, 120], 28, fill=C['accent']); d.text((84, 68), t, font=self.F('B', 34), fill=C['white'])
            if kicker: d.text((136 + tw, 74), kicker, font=self.F('M', 30), fill=(190, 205, 222))
            for i, t in enumerate(title_lines):
                d.text((56, top + i * lh), t, font=f(fs), fill=C['white'] if i == 0 else C['highlight'])
            if subtitle:
                sf = 38
                while d.textlength(subtitle, font=self.F('B', sf)) > W - 120 and sf > 26: sf -= 2
                d.text((60, panel - 80), subtitle, font=self.F('B', sf), fill=C['white'])
            y0, y1 = panel + 40, H - (150 if banner else 70)
            ph = list(photos)
            if len(ph) == 1:
                self.photo(c, ph[0][0], (60, y0, W - 60, y1), r=30, tag=ph[0][1], tagc=C['accent'])
            elif len(ph) >= 2:
                self.photo(c, ph[0][0], (60, y0, 520, y1), r=30, tag=ph[0][1], tagc=C['accent'])
                rest = ph[1:3]; hh = (y1 - y0 - 20 * (len(rest) - 1)) // len(rest)
                for i, (im, tg) in enumerate(rest):
                    self.photo(c, im, (560, y0 + i * (hh + 20), W - 60, y0 + i * (hh + 20) + hh), r=30, tag=tg, tagc=[C['teal'], C['primary']][i])
            if banner:
                d = ImageDraw.Draw(c); bf = 42
                while d.textlength(banner, font=self.F('K', bf)) > 760 and bf > 28: bf -= 2
                d.rounded_rectangle([140, H - 140, W - 140, H - 56], 42, fill=C['highlight'])
                d.text((W / 2 - d.textlength(banner, font=self.F('K', bf)) / 2, H - 98 - bf * .62), banner, font=self.F('K', bf), fill=C['primary'])
            return c
        self.pages.append(draw)

    def text(self, title, sub, items, top=48):
        """纯文字卡"""
        def draw(n, total):
            c, d, y = self._base(n, total, title, sub); self.auto(c, y, items, top); return c
        self.pages.append(draw)

    def figure(self, title, sub, images, tags=None, items=(), h=None, stack=False, top=44, min_fs=32, max_h=900):
        """图片卡：images 一排（stack=True 时上下排），下方 items。
        图片高度自动取“文字仍能以 ≥min_fs 字号放下”的最大值（不超过 max_h，也不超过 h 若给定）；
        实在放不下时再降字号。"""
        images = [images] if isinstance(images, Image.Image) else list(images)
        cap = min(h or max_h, max_h)

        def draw(n, total):
            for need in (min_fs, 22):
                for hh in range(cap, 239, -20):
                    c, d, y = self._base(n, total, title, sub)
                    yb = (self._col if stack else self._row)(c, y, images, tags, hh)
                    if not items: return c
                    if y + 28 + self.render_items(c, 0, list(items), need, dry=True) + (yb - y) < self.H - 110:
                        self.auto(c, yb + 28, list(items), top); return c
            raise ValueError(f'卡片“{title}”图文放不下，请删减文字')
        self.pages.append(draw)

    def chart(self, title, sub, fig, items=(), top=40):
        """数据图卡：fig 为 matplotlib Figure（建议 figsize 宽 9.6，字号 ≥18）"""
        def draw(n, total):
            import matplotlib.pyplot as plt
            buf = BytesIO(); fig.savefig(buf, format='png', dpi=100); plt.close(fig)
            im = Image.open(buf).convert('RGB')
            c, d, y = self._base(n, total, title, sub)
            hh = round(im.height * (self.W - 120) / im.width); self.put(c, im, 60, y, self.W - 120, hh)
            if items: self.auto(c, y + hh + 26, list(items), top)
            return c
        self.pages.append(draw)

    def rows(self, title, sub, rows, note=''):
        """速查表卡：rows 为 (标题, 说明, 结论, 样式)，样式取 BOX_STYLES 的键"""
        def draw(n, total):
            c, d, y = self._base(n, total, title, sub); C = self.C
            for fs in range(34, 21, -1):
                tot = sum(58 + self.th(b, 880, fs - 4, lh=1.35) + self.th('→ ' + e, 880, fs - 2, 'B', 1.35) + 34 for _, b, e, _ in rows)
                if y + tot + (40 if note else 0) < self.H - 100: break
            for a, b, e, st in rows:
                fill, col = self.BOX.get(st, self.BOX['teal'])
                hb = self.th(b, 880, fs - 4, lh=1.35) if b else 0; he = self.th('→ ' + e, 880, fs - 2, 'B', 1.35); hh = 58 + hb + he + 20
                d.rounded_rectangle([60, y, self.W - 60, y + hh], 22, fill=fill); d.rectangle([60, y + 16, 70, y + hh - 16], fill=col)
                d.text((92, y + 12), a, font=self.F('K', fs), fill=col)
                yy = self.rich(d, 92, y + 58, b, 880, fs - 4, col=C['muted'], lh=1.35) if b else y + 58
                self.rich(d, 92, yy + 2, '→ **' + e + '**', 880, fs - 2, em=C['ink'], lh=1.35); y += hh + 14
            if note: self.rich(d, 60, y + 2, note, self.W - 120, 24, col=C['muted'], lh=1.3)
            return c
        self.pages.append(draw)

    def custom(self, fn):
        """自定义卡：fn(deck, canvas, draw, y) 自己画；canvas 已带页眉页脚。用法 deck.custom(lambda k, c, d, y: ...) 并在 fn 前设 fn.title / fn.sub"""
        def draw(n, total):
            c, d, y = self._base(n, total, getattr(fn, 'title', ''), getattr(fn, 'sub', None)); fn(self, c, d, y); return c
        self.pages.append(draw)

    # ---------- 输出 ----------
    def save(self, out, overview=True, prefix='card'):
        total = len(self.pages)
        if total > self.t['max_cards']:
            print(f"⚠ 共 {total} 张，超过单篇上限 {self.t['max_cards']} 张，建议拆成上、中、下篇")
        os.makedirs(out, exist_ok=True); paths = []
        for i, fn in enumerate(self.pages, 1):
            p = os.path.join(out, f'{prefix}{i:02d}.jpg'); fn(i, total).save(p, quality=92); paths.append(p)
        if overview: contact_sheet(paths, os.path.join(out, '_overview.jpg'))
        print('ok', total, '张 →', out)
        return paths


def contact_sheet(paths, out, cols=6, w=360):
    """把所有卡片缩略拼成一张总览图，便于一次检查"""
    ims = [Image.open(p).resize((w, round(w * 4 / 3))) for p in paths]
    rows = (len(ims) + cols - 1) // cols; h = ims[0].height
    sheet = Image.new('RGB', (cols * (w + 10), rows * (h + 10)), 'white')
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * (w + 10), (i // cols) * (h + 10)))
    sheet.save(out, quality=85); return out


def split_lr(im, cut=None, trim_top=0):
    """左右拼图切成两张；cut 不给时自动找中线附近亮度跳变最大的列"""
    if cut is None:
        import numpy as np
        a = np.asarray(im.convert('L')).astype(int); dcol = abs(np.diff(a, axis=1)).mean(0)
        W = a.shape[1]; cut = max(range(int(W * .35), int(W * .65)), key=lambda k: dcol[k])
    return im.crop((0, trim_top, cut - 2, im.height)), im.crop((cut + 3, trim_top, im.width, im.height))
