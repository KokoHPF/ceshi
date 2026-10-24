#!/usr/bin/env python3
"""示例：Boileau 等《拇指试验》→ 11 张卡片。演示 cover / text / figure / chart 四种卡片和示意图标注。

准备素材（在本目录执行）：
  python3 ../../scripts/fetch_supplement.py 10.1016/j.eats.2022.05.007 work        # 得到 gr1～4.jpg、mmc2.mp4
  python3 ../../scripts/annotate.py annotate_spec.json --font ../../fonts/NotoSansSC-Bold.otf
  python3 ../../scripts/video_frames.py work/mmc2.mp4 work --at 22 25 53 59 --crop-black
  python3 build.py out
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

W = lambda f: Image.open(os.path.join(HERE, 'work', f))
deck = Deck(series='后肩不稳', source='Boileau 等 Arthrosc Tech 2022;11(9):e1613')
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()

# 1 封面：标题用论文标题的中文直译
deck.cover(['拇指试验：', '诊断症状性后肩不稳的', '简单查体方法'], kicker='Arthroscopy Techniques 2022',
           subtitle='拇指顶住后方关节线，抬手不痛了 → 阳性',
           photos=[(W('v59.png'), '拇指顶住'), (W('fig3A.zh.jpg'), '拇指＝“后方骨块”')], banner='示意图逐张精讲 + 视频截帧')
# 2 背景
fig, ax = plt.subplots(figsize=(9.6, 3.6))
ax.barh([1], [10], left=[2], color='#9bc9d1', height=.5); ax.barh([0], [20], color='#be2832', height=.5)
ax.text(12.5, 1, '过去：2%～10%', va='center', fontsize=26); ax.text(20.5, 0, '现在：最高约 20%', va='center', fontsize=26)
ax.set_xlim(0, 52); ax.set_yticks([]); ax.set_xlabel('占肩关节不稳的比例（%）', fontsize=20); ax.tick_params(labelsize=18)
ax.spines[['top', 'right', 'left']].set_visible(False); fig.tight_layout()
deck.chart('后肩不稳，为什么容易漏？', '年轻运动人群越来越常见', fig, [
    ('h', '难在哪'),
    ('steps', [('1', '患者多以**疼痛**就诊，**没有脱位或半脱位史**'), ('2', '后盂唇撕裂在磁共振上**常看不清**'),
               ('3', '常诉**肩前痛**、二头肌沟压痛，容易被带偏')]),
    ('box', '影像线索', '关节盂**后倾增大**、关节盂发育不良、后方关节囊面积增大', 'teal')])
# 3 示意图精讲
deck.figure('示意图①：为什么抬手会痛', '原文图 2：横断面（上为前，下为后）', W('fig2.zh.jpg'), None, [
    ('steps', [('1', '中立内收位**前屈上举**时，肱骨头被推向**后方**'), ('2', '半脱位的肱骨头压在**撕裂的后盂唇**上 → 疼痛、不稳')]),
    ('box', '一句话', '这个动作就是**诱发试验**；拇指试验要做的，是把肱骨头“挡回去”', 'yellow')])
# 4 步骤（原图 + 视频截帧一排）
deck.figure('第一步：先诱发症状', '原文图 1 + 视频截帧', [W('gr1.jpg'), W('v22.png'), W('v25.png')], ['图 1', '视频：前屈', '视频：上举'], [
    ('steps', [('1', '坐位或站立，检查者站在**患侧后方**'), ('2', '中立内收位主动**前屈上举**'), ('3', '记录有无**后肩痛**和**不稳感**')])])
deck.figure('示意图②：拇指放哪里', '原文图 3A：右肩横断面', W('fig3A.zh.jpg'), None, [
    ('steps', [('1', '拇指压在**后方盂肱关节线**上'), ('!', '**一半压关节盂缘，一半压肱骨头后内侧**')]),
    ('box', '原理', '拇指起到功能性“**后方骨块**”的作用', 'teal')])
deck.figure('示意图③：另一只手指干什么', '原文图 3B 横断面、3C 矢状面', [W('fig3B.zh.jpg'), W('fig3C.zh.jpg')], None, [
    ('bul', ['同侧手**其余手指勾住前方锁骨**作反作用力', '患者很壮时可用**双手、两个拇指**'], 'teal')])
deck.figure('第三步：拇指顶住，再抬一次', '原文图 4 + 视频截帧', [W('v53.png'), W('v59.png'), W('gr4.jpg')], ['放好拇指', '再前屈', '图 4'], [
    ('box', '阳性', '拇指在位时**后肩痛缓解、稳定性改善**', 'accent')])
# 纯文字
deck.text('要点与局限', '原文表 1', [
    ('steps', [('✓', '主动试验，不太受疼痛保护和恐惧影响'), ('!', '只是**技术描述**，尚无敏感度、特异度和信度研究')])])
deck.text('收藏：拇指试验三步走', '后肩痛 + 无脱位史时想到它', [
    ('steps', [('1', '中立内收位**前屈上举** → 记录疼痛 / 不稳'), ('2', '拇指压**后方关节线**，手指勾**前方锁骨**'), ('3', '再上举：**更不痛、更稳**＝阳性')]),
    ('box', '文献', 'Boileau P, et al. The Thumb Test. Arthrosc Tech. 2022;11(9):e1613-e1616', 'navy'),
    ('box', '版权', '原文 **CC BY-NC-ND 4.0**；示意图加了中文标注，仅供学习交流，如有侵权请联系删除', 'accent')])
deck.save(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out'))
