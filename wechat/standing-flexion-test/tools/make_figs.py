#!/usr/bin/env python3
"""Colonna、Casacci 2026 站立前屈试验批判性综述：首图中文标题卡、原文图 1/2/7/8 贴中文标签、9 种模式柱状图（原文图 3 按原文数字用中文重画）、
原文图 4/5 示意图下方加中文说明、影响因素图（原文图 6 用中文重画）、站立-坐位-俯卧鉴别流程卡、封面。共用工具在 ../bridge-review-1/tools/bridgekit.py。
用法：python3 make_figs.py <work 目录> <输出目录> <中号字体> <粗体>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bridge-review-1', 'tools'))
from bridgekit import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
WORK, OUT, FM, FBOLD = sys.argv[1:5]
font_manager.fontManager.addfont(FM); plt.rcParams['font.family'] = font_manager.FontProperties(fname=FM).get_name()
k = Kit(WORK, OUT, FBOLD)
k.save(k.title('综述 · 《Cureus》2026', ['手法治疗中的站立前屈试验：', '批判性回顾与功能性再解读'],
               'Colonna S, Casacci F.', 'Cureus. 2026;18(1):e101225. doi:10.7759/cureus.101225',
               '意大利博洛尼亚 Spine Center 康复医学部、Osteopathic Spine Center Education 研发部'), 1)
n = 2
def put(im, cap):
    global n; im = k.op(im) if isinstance(im, str) else im; k.save(k.capbox(im, cap), n); n += 1

def strip(name, labels, W=1200, fs=30):
    """在图下方加一条白底中文说明：labels [(x 中心比例, 文字, 颜色)]"""
    im = k.op(name); im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    lines = max(t.count('\n') + 1 for _, t, _ in labels); h = lines * (fs + 10) + 24
    o = Image.new('RGB', (W, im.height + h), 'white'); o.paste(im, (0, 0)); d = ImageDraw.Draw(o); f = ImageFont.truetype(FBOLD, fs)
    for fx, t, c in labels:
        for j, ln in enumerate(t.split('\n')):
            tw = d.textlength(ln, font=f); d.text((fx * W - tw / 2, im.height + 12 + j * (fs + 10)), ln, font=f, fill=c)
    return o

put('x52.jpg', '原文图 1  站立前屈试验时摸髂后上棘（PSIS）：检查者双手拇指放在两侧 PSIS 的下缘（指尖在 PSIS 下方）')
put(tags_at(k, 'x85.jpg', [(.06, .03, 'A 先在前屈位摸', C_HI), (.55, .03, 'B 再回到站立位摸', C_OK)]),
    '原文图 2  “反向”站立前屈试验：作者团队发现，先在弯腰位找 PSIS、再在站直时找，比传统的“先站后弯”更容易摸准，检查者之间一致性更高')

P = ['左→左', '左→平', '左→右', '平→左', '平→平', '平→右', '右→左', '右→平', '右→右']; N = [9, 0, 0, 3, 21, 8, 0, 1, 6]
cl = ['#E8A200', '#ddd', '#ddd', '#188080', '#16324F', '#188080', '#ddd', '#E8A200', '#E8A200']
fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
ax.bar(range(9), [v / 48 * 100 for v in N], .65, color=cl)
for i, v in enumerate(N): ax.text(i, v / 48 * 100 + 1, f'{v / 48 * 100:.1f}%\n（{v} 人）', ha='center', fontsize=13)
ax.set_xticks(range(9), P, fontsize=15); ax.set_ylabel('占比（%）', fontsize=15); ax.set_ylim(0, 56); ax.tick_params(axis='y', labelsize=13)
ax.set_xlabel('PSIS 高低模式：站立时 → 前屈后（“左”＝左侧 PSIS 更靠上，“平”＝两侧等高）', fontsize=14)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color='#16324F', label='阴性（站立、前屈都等高）'), Patch(color='#188080', label='传统意义上的阳性（站立等高、前屈不等高）'), Patch(color='#E8A200', label='站立时就不等高：难以解读')],
          frameon=False, fontsize=13, loc='upper right')
ax.set_title('48 名受试者站立前屈试验的 9 种 PSIS 模式（同一名检查者）', fontsize=18)
fig.tight_layout(); fig.savefig(f'{WORK}/pat.png', facecolor='white'); plt.close(fig)
put(k.op('pat.png'), '原文图 3 重画：传统解读只有“阴性、左阳性、右阳性”3 种结果，实际有 9 种组合。48 人中有 16 人（33%）站立时两侧 PSIS 就不等高，按传统标准很难判断')

put(strip('x112.jpg', [(.17, 'C 前屈：右侧更高\n→ 右侧阳性', RED), (.5, 'B 前屈：仍等高\n→ 阴性', (0, 120, 60)), (.83, 'D 前屈：左侧更高\n→ 左侧阳性', RED)]),
    '原文图 4  解读清楚的情况。A（上）：站立时两侧 PSIS 等高；B/C/D（下）：前屈后的三种结果。红色箭头＝更靠上（头侧、腹侧），绿色＝等高')
put(strip('x127.jpg', [(.17, 'C 前屈：右侧仍更高\n→ 谁动得多？说不清', (200, 120, 0)), (.5, 'B 前屈：变等高\n→ 左侧动得多？', (200, 120, 0)), (.83, 'D 前屈：变成左侧更高\n→ 明确左侧阳性', RED)]),
    '原文图 5  解读模糊的情况。A（上）：站立时右侧 PSIS 就更高；前屈后变成 B、C 两种情况都很难按传统标准判断，只有 D 能明确判断为左侧阳性')

fig, ax = plt.subplots(figsize=(12, 7.2), dpi=100); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.axis('off')
def box(x, y, w, h, t, fc, ec, fs=16, col='#16324F'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5', fc=fc, ec=ec, lw=1.6)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs, color=col)
box(30, 62, 60, 6, '影响 PSIS 位置的因素', '#F2F2F2', '#555', fs=24)
F = [('骶髂关节\n活动受限', ['#D9432F']), ('竖脊肌\n僵硬不对称', ['#D9432F']), ('屈髋肌\n僵硬不对称', ['#D9432F']), ('伸髋肌\n僵硬不对称', ['#2E6BD9']), ('骨盆形态\n不对称', ['#D9432F', '#2E6BD9'])]
for i, (t, cs) in enumerate(F):
    x = 3 + i * 23.5; ax.annotate('', (x + 9, 46), (x + 9, 61), arrowprops=dict(arrowstyle='-|>', lw=6, color='#8DB8E0'))
    box(x, 33, 18, 13, t, '#E4EEF8', '#2E6BD9', fs=19)
    for j, c in enumerate(cs):
        dx = 0 if len(cs) == 1 else (-3 if j == 0 else 3); ax.annotate('', (x + 9 + dx, 16), (x + 9 + dx, 32), arrowprops=dict(arrowstyle='-|>', lw=6, color=c))
box(33, 6, 54, 8, 'PSIS 的位置', 'white', '#333', fs=26, col='#111')
ax.add_patch(plt.Rectangle((2, 9), 3, 3, color='#D9432F')); ax.text(6, 10.5, '向头侧、腹侧（更高）', va='center', fontsize=17)
ax.add_patch(plt.Rectangle((2, 3), 3, 3, color='#2E6BD9')); ax.text(6, 4.5, '向背侧、足侧（更低）', va='center', fontsize=17)
fig.tight_layout(); fig.savefig(f'{WORK}/fac.png', facecolor='white'); plt.close(fig)
put(k.op('fac.png'), '原文图 6 重画：可能影响 PSIS 位置的关节、肌筋膜和骨性因素，以及各自使 PSIS 移动的方向；几种因素可能同时存在')

put(tags_at(k, 'x206.jpg', [(.02, .02, '红：头侧牵拉（竖脊肌）', RED), (.40, .93, '蓝：足侧牵拉（腘绳肌）', (40, 90, 200))]),
    '原文图 7  弯腰时影响 PSIS 的两条肌筋膜力线示意：红色箭头为头侧的椎旁肌系统，蓝色箭头为足侧的腘绳肌系统')
put(tags_at(k, 'x263.jpg', [(.03, .02, 'A 站立', C_NAV), (.03, .64, 'B 坐位', C_NAV), (.45, .30, 'C 俯卧', C_NAV)]),
    '原文图 8  在三种体位下摸 PSIS：A 站立；B 坐位；C 俯卧（右上小图为俯卧时从上方看的手法）')

k.save(k.card('PSIS 不对称从哪来？站立→坐位→俯卧三步鉴别（作者提出的推理）', [
    ('第 1 步：站立前屈试验', '先排除髋关节问题（骨关节炎、髋撞击会让该侧骨盆前倾变少，对侧代偿，形成“假阳性”）\n记录站立和前屈时两侧 PSIS 的高低，按程度分级，而不是只记阳性/阴性', LT, TEAL),
    ('第 2 步：坐位前屈试验', '坐位屈膝时腘绳肌处于力学劣势\n不对称减轻或消失 → 多半来自足侧（腘绳肌为主）\n不对称不变 → 骨盆形态，或头侧（椎旁肌）因素', OR, (200, 120, 0)),
    ('第 3 步：俯卧位摸 PSIS', '俯卧时椎旁肌的牵拉减少\n不对称减轻或消失 → 头侧肌筋膜（椎旁肌）因素\n站、坐、卧都一样 → 骨盆形态本身不对称', GR, (0, 120, 60)),
    ('注意', '这是作者基于生物力学的推理框架，还没有研究验证它的准确性', PK, RED),
]), n); n += 1
c = k.op('x85.jpg'); c = c.resize((900, round(c.height * 900 / c.width))); y0 = int(c.height * .2)
c.crop((0, y0, 900, y0 + 383)).save(f'{OUT}/cover.jpg', quality=90); print('ok', n - 1)
