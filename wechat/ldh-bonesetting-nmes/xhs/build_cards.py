#!/usr/bin/env python3
"""Bao、Wang 2024 正骨手法联合神经肌肉电刺激治疗腰椎间盘突出 1 例 → 小红书 3:4 图文卡片。原文 CC BY。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='腰痛康复', source='Bao & Wang Front Rehabil Sci 2024;5:1465623', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
X = lambda n: Image.open(f'{WORK}/x{n}.jpg').convert('RGB')
TAGS = ['前屈', '后伸', '左侧屈', '右侧屈']
def quad(im):
    w, h = im.size; return [im.crop((0, 0, w // 2, h // 2)), im.crop((w // 2, 0, w, h // 2)), im.crop((0, h // 2, w // 2, h)), im.crop((w // 2, h // 2, w, h))]
pre, post = quad(X(41)), quad(X(83))
def row(a, b):
    h = min(a.height, b.height); a = a.resize((round(a.width * h / a.height), h)); b = b.resize((round(b.width * h / b.height), h))
    c = Image.new('RGB', (a.width + b.width + 8, h), 'white'); c.paste(a, (0, 0)); c.paste(b, (a.width + 8, 0)); return c

deck.cover(['中医正骨联合', '神经肌肉电刺激', '治疗腰椎间盘突出：1 例报告'], kicker='Front Rehabil Sci 2024 · 病例报告',
           subtitle='久坐白领腰痛：放松 → 复位 → 强化',
           photos=[(X(63), '电刺激'), (pre[0], '治疗前前屈'), (post[0], '治疗后前屈')], banner='疼痛 6 → 0 · 1 年未复发')
deck.text('为什么关注上班族腰痛', '原文引言', [
    ('box', '越来越常见', '2006～2016 年腰痛发病增加 **18%**；成年人一生约 **80%** 会腰痛', 'teal'),
    ('box', '上班族', '不少人每天坐 **8 小时以上**；腰痛发生率 **25%～51%**', 'yellow'),
    ('box', '久坐的问题', '髂腰肌等缩短，**臀肌、竖脊肌、多裂肌**相对无力 → 肌肉失衡', 'accent'),
    ('box', '常规治疗', '药物、按摩、理疗常只能暂时缓解，症状反复', 'navy')])
deck.text('作者的理论框架', '冯天有“新医正骨”（原文讨论）', [
    ('box', '内平衡', '椎间盘、小关节、韧带 → 维持椎间关节稳定', 'teal'),
    ('box', '外平衡', '脊柱前后左右的**肌肉** → 维持各种姿势下的协调和稳定', 'yellow'),
    ('box', '失衡', '劳损或退变后，弯腰、扭闪可致单个或多个**椎体“位移”**\n小关节、韧带、椎间盘张力改变 → 肌肉僵硬、疼痛、代偿性侧弯', 'accent'),
    ('box', '治疗设想', '① 先**放松**肌肉　② 再**正骨**复位　③ 最后**练肌力**，维持内外平衡', 'navy')])
deck.text('病例：33 岁女性白领', '原文', [
    ('steps', [('史', '长期伏案；3 个月前久坐后腰痛，前一天**搬重物后加重**'), ('症', '弯腰受限，伴**下肢放射痛**'),
               ('查', '左侧棘突旁压痛、**左腰肌痉挛**；直腿抬高**阳性**；感觉、肌力正常'), ('评', 'VAS **6**；JOA **19** 分；前屈 45°、后伸 10°'),
               ('诊', '腰肌劳损 + L3/4、L4/5、L5/S1 **椎间盘突出**')])])
deck.figure('影像：MRI 和 CT', '原文图 1', X(24), None, [
    ('bul', ['MRI：**三个节段**椎间盘突出，压迫硬膜囊', 'CT：提示**后纵韧带钙化**'])])
deck.figure('X 线：作者眼中的“位移”', '原文图 3（左）、图 4（右）', [X(46), X(58)], None, [
    ('bul', ['正位片：棘突连线**不居中**，作者认为提示椎体**旋转**', '侧位片：椎体边缘**骨赘**（放大圈），作者认为是增加稳定的代偿']),
    ('box', '编者注', '“椎体位移”的判断来自作者采用的理论；原文没有治疗后的影像对比', 'grey')])
deck.text('治疗方案', '原文', [
    ('box', '① 放松：神经肌肉电刺激', '“解痉”模式；电极贴两侧**竖脊肌**肌腹；每天 1～2 次 × **20 分钟**；配合腰肌牵伸', 'teal'),
    ('box', '② 复位：脊柱（定点）旋转复位法', '重心移到“错位”小关节上使脊柱暂时失稳；术者**拇指**推顶偏歪的棘突复位', 'yellow'),
    ('box', '③ 强化：电刺激同步训练', '每周 **3～5 次 × 4 周**；腰腹肌收缩期同步电刺激；瑜伽球背伸、动态平板支撑', 'purple'),
    ('box', '④ 健康教育', '避免久坐久站、搬重物、扭腰；定时起身；**屈髋屈膝、背挺直**搬东西', 'coral')])
deck.figure('治疗用到的', '原文图 5（上）、6（左下）、7（右下）', [X(63), row(X(78), X(88))], ['电极位置', '左腰肌痉挛 · 复位椅'], stack=True, items=[
    ('bul', ['电刺激：两侧竖脊肌肌腹各贴电极', '左侧腰肌明显**痉挛**——先放松，再做手法', '正骨手法在专用**复位椅**上进行'])])
deck.figure('治疗前 vs 治疗后：前屈、后伸', '原文图 2（上）、图 8（下）', [row(pre[0], pre[1]), row(post[0], post[1])], ['治疗前', '治疗后'], stack=True, items=[
    ('bul', ['前屈 **45° → 80°**', '后伸 **10° → 30°**（达到正常 30°）'])])
deck.figure('治疗前 vs 治疗后：侧屈', '原文图 2（上）、图 8（下）', [row(pre[2], pre[3]), row(post[2], post[3])], ['治疗前', '治疗后'], stack=True, items=[
    ('bul', ['左侧屈 **25° → 25°**（不变）', '右侧屈 **15° → 25°**'])])
fig, ax = plt.subplots(figsize=(9.6, 6))
labs = ['前屈', '后伸', '左侧屈', '右侧屈']; a = [45, 10, 25, 15]; b = [80, 30, 25, 25]; x = range(4)
ax.bar([i - .2 for i in x], a, .4, color='#9AA5B1', label='治疗前'); ax.bar([i + .2 for i in x], b, .4, color='#2E86AB', label='随访')
for i in x:
    ax.text(i - .2, a[i] + 1.5, f'{a[i]}°', ha='center', fontsize=18); ax.text(i + .2, b[i] + 1.5, f'{b[i]}°', ha='center', fontsize=18)
ax.set_xticks(list(x), labs, fontsize=20); ax.set_ylim(0, 95); ax.tick_params(axis='y', labelsize=15); ax.set_ylabel('活动度（°）', fontsize=18)
ax.legend(frameon=False, fontsize=18); ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=.3); fig.tight_layout()
deck.chart('结果', '据原文表 1、2 重画', fig, [
    ('bul', ['疼痛 VAS **6 → 0**；作者报告 **3 次**治疗后压痛、痉挛消失', '很快复工；**1 年随访未复发**'])])
deck.text('能信几分 + 原文对不上的地方', '编者整理', [
    ('h', '证据很弱'),
    ('bul', ['只有 **1 例**、没有对照；多种方法同时用，分不清谁起作用', '入院测了 JOA，治疗后**没报告**；没有治疗后影像证实“复位”']),
    ('h', '原文对不上'),
    ('steps', [('1', '表 1 有“旋转”一栏，但**没有数值**'), ('2', '说 3 次后前屈“恢复正常”，表中随访是 **80°**（正常 90°）'), ('3', '讨论里文献 **12、13** 引用对调')])])
deck.text('收藏：久坐腰痛的三步思路', '本例方案（单个病例，仅供参考）', [
    ('steps', [('1', '**放松**：电刺激“解痉”模式，竖脊肌两侧贴电极，20 分钟'), ('2', '**复位**：脊柱（定点）旋转复位法（需受训医生操作）'),
               ('3', '**强化**：电刺激同步腰腹肌训练，每周 3～5 次 × 4 周'), ('4', '**教育**：定时起身、靠背椅、屈髋屈膝搬物')]),
    ('box', '文献', 'Bao Y, Wang Z. Combination of traditional Chinese bone setting and NMES technique for treating lumbar disc herniation: a case report. Front Rehabil Sci. 2024;5:1465623', 'navy'),
    ('box', '版权', '原文 **CC BY** 开放获取；图 2、8 切分为单幅并加中文标签', 'teal')])
deck.save(OUT)
