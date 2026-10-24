"""桥式运动三部曲推文共用的画图工具：标题卡、带中文图注的配图、要点卡、多联图自动分块加中文标签、中文横向柱状图。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font = lambda s: ImageFont.truetype(F, max(8, int(s)))
INK = (30, 30, 30); GREY = (110, 110, 110); TEAL = (0, 110, 130); RED = (190, 40, 50)
LT = (225, 240, 243); OR = (252, 240, 230); GR = (232, 245, 233); PK = (250, 228, 228); PU = (240, 240, 248)
C_OK, C_HI, C_NAV = (24, 128, 128), (238, 99, 72), (22, 50, 79)


class Kit:
    def __init__(self, work, out, bold_font):
        self.work, self.out = work, out; self.FB = ImageFont.truetype(bold_font, 34)

    op = lambda self, n: Image.open(f'{self.work}/{n}').convert('RGB')

    def save(self, im, n):
        im = im.convert('RGB')
        if im.width > 1200: im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        im.save(f'{self.out}/img{n:02d}.jpg', quality=85)

    @staticmethod
    def para(dr, x, y, t, fs, w, fill=INK, gap=10):
        line = ''
        for ch in t:
            if dr.textlength(line + ch, font=font(fs)) > w: dr.text((x, y), line, font=font(fs), fill=fill); y += fs + gap; line = ch
            else: line += ch
        dr.text((x, y), line, font=font(fs), fill=fill); return y + fs + gap

    def capbox(self, im, cap, W=1200):
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        dd = ImageDraw.Draw(Image.new('RGB', (W, 2000))); hh = self.para(dd, 14, 14, cap, 28, W - 30, gap=12) + 4
        t = Image.new('RGB', (W, im.height + hh + 12), 'white'); dr = ImageDraw.Draw(t)
        dr.rounded_rectangle([0, 4, W, hh], 8, fill=LT); self.para(dr, 14, 14, cap, 28, W - 30, fill=TEAL, gap=12)
        t.paste(im, (0, hh + 8)); return t

    def card(self, title, blocks, W=1200):
        im = Image.new('RGB', (W, 5000), 'white'); dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, W, 76], fill=TEAL); dr.text((24, 16), title, font=font(36), fill='white'); y = 100
        for h, t, c, a in blocks:
            top = y; y2 = y + 62; dd = ImageDraw.Draw(Image.new('RGB', (W, 5000)))
            for seg in t.split('\n'): y2 = self.para(dd, 50, y2, seg, 28, W - 100, gap=14)
            dr.rounded_rectangle([20, top, W - 20, y2 + 10], 12, fill=c); dr.rectangle([20, top, 30, y2 + 10], fill=a)
            dr.text((50, top + 16), h, font=font(32), fill=a); yy = y + 62
            for seg in t.split('\n'): yy = self.para(dr, 50, yy, seg, 28, W - 100, gap=14)
            y = y2 + 30
        return im.crop((0, 0, W, y))

    def title(self, kicker, lines, authors, cite, unit):
        W, H = 1400, 640; im = Image.new('RGB', (W, H), (246, 248, 250)); dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, 18, H], fill=TEAL); dr.text((70, 50), kicker, font=font(32), fill=TEAL)
        for i, l in enumerate(lines): dr.text((70, 140 + i * 75), l, font=font(52), fill=INK)
        y = 140 + len(lines) * 75 + 40; dr.line([70, y, W - 70, y], fill=(200, 205, 210), width=2)
        for i, t in enumerate((authors, cite, unit)): dr.text((70, y + 30 + i * 45), t, font=font(26), fill=GREY)
        dr.text((70, y + 180), '编者中文解读，仅作学术交流', font=font(26), fill=(150, 150, 150)); return im

    def tagged(self, name, tags, W=1200):
        """多联图上下等分成 len(tags) 块，在每块左上角贴中文标签；tags 每项 (文字, 颜色)"""
        im = self.op(name); im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        d = ImageDraw.Draw(im); h = im.height / len(tags)
        for i, (t, c) in enumerate(tags):
            y0 = round(i * h); tw = d.textlength(t, font=self.FB)
            d.rounded_rectangle([12, y0 + 12, 40 + tw, y0 + 64], 10, fill=c); d.text((26, y0 + 16), t, font=self.FB, fill='white')
        return im

    def hbar(self, title, data, fontfile, path, xmax=None, note=None):
        """data: [(中文名, 值, 不稳定?)]，从高到低画中文横向柱状图"""
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
        font_manager.fontManager.addfont(fontfile); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fontfile).get_name()
        n = len(data); fig, ax = plt.subplots(figsize=(12, 1.2 + .62 * n), dpi=100); y = np.arange(n)[::-1]
        for yy, (lab, v, u) in zip(y, data):
            ax.barh(yy, v, .66, color='#E8A200' if u else '#7FB86A'); ax.text(v + 1, yy, f'{v:g}', va='center', fontsize=15)
        ax.set_yticks(y, [d[0] for d in data], fontsize=15); ax.set_xlim(0, xmax or max(d[1] for d in data) * 1.15)
        ax.set_xlabel('% MVIC', fontsize=14); ax.set_title(title, fontsize=20, pad=40); ax.tick_params(axis='x', labelsize=13)
        ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='x', alpha=.3)
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(color='#7FB86A', label='稳定支撑面'), Patch(color='#E8A200', label='一端在不稳定面（球、波速球、悬吊、振动台）')],
                  frameon=False, fontsize=13, loc='lower center', bbox_to_anchor=(.4, 1.0), ncol=2)
        fig.tight_layout(); fig.savefig(path, facecolor='white'); plt.close(fig)


def tags_at(kit, name, tags, W=1200):
    """tags: [(x 比例, y 比例, 文字, 颜色)]，在指定位置贴中文标签（适合网格多联图和示意图）"""
    im = kit.op(name); im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS); d = ImageDraw.Draw(im)
    for fx, fy, t, c in tags:
        x0, y0 = round(fx * im.width), round(fy * im.height); tw = d.textlength(t, font=kit.FB)
        d.rounded_rectangle([x0, y0, x0 + 28 + tw, y0 + 52], 10, fill=c); d.text((x0 + 14, y0 + 4), t, font=kit.FB, fill='white')
    return im
