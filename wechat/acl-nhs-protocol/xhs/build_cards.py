#!/usr/bin/env python3
"""East Kent Hospitals NHS《Anterior Cruciate Ligament (ACL) injury》患者手册 → 小红书 3:4 图文卡片。
原文版权归 East Kent Hospitals University NHS Foundation Trust；PDF 为网页打印版，动作照片未随文件保存，卡片为编者中文整理，
数据图由编者据原文数字绘制；卡片注明“仅供学习交流，如有侵权请联系删除”。
用法：python3 build_cards.py <work 目录> <字体目录> <输出目录>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'skills', 'paper-to-xhs-cards', 'scripts'))
from io import BytesIO
from PIL import Image
from cardkit import Deck
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
WORK, FONTS, OUT = sys.argv[1:4]
deck = Deck(series='膝关节康复', source='East Kent Hospitals NHS 患者手册 Web 640', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()


def road_fig(w=9.6, h=5.2):
    """受伤到回归运动的路线（编者据原文绘制）"""
    fig, ax = plt.subplots(figsize=(w, h), dpi=100); ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis('off')
    st = [('受伤后', '消肿、找回活动度\n4 个基础动作', '#1F5F8B'), ('术前强化', '11 个力量与平衡动作\n越强壮进手术越好', '#2E8B57'),
          ('术后 0～2 周', '踝泵、股四头肌－腘绳肌\n同收缩、髋周练习', '#E3A21A'), ('术后 2～6 周', '腘绳肌弯举、臀桥、\n靠墙蹲、上台阶', '#C0392B'),
          ('≥12 个月', '才能完全\n回归运动', '#16324F')]
    for i, (t, s, c) in enumerate(st):
        x = .1 + i * 1.98
        ax.add_patch(FancyBboxPatch((x, 2.9), 1.78, 1.2, boxstyle='round,pad=0.02,rounding_size=0.15', fc=c, ec='none'))
        ax.text(x + .89, 3.5, t, ha='center', va='center', fontsize=17, color='white', weight='bold')
        ax.text(x + .89, 2.2, s, ha='center', va='center', fontsize=12.5, color='#333', linespacing=1.5)
        if i < 4: ax.annotate('', xy=(x + 1.97, 3.5), xytext=(x + 1.8, 3.5), arrowprops=dict(arrowstyle='->', lw=2.5, color='#888'))
    ax.text(5, .7, '每个动作：每天 2～3 组 × 8～12 次，组间休息 60～120 秒，每周 3～5 天', ha='center', fontsize=14.5, color='#C0392B', weight='bold')
    fig.tight_layout(pad=.2); return fig


def fig2img(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['前交叉韧带损伤', '康复全程', '患者手册'], kicker='英国 NHS 医院 · 物理治疗科',
           subtitle='保守还是手术？术前术后各练什么？', photos=[(fig2img(road_fig()), '从受伤到回归运动')], banner='疼痛 ≤4/10 可接受 · 术后 12 个月再回归运动')
deck.text('ACL 是什么、怎么伤的', '原文：What is the ACL?', [
    ('box', '作用', '膝关节中间斜行的一条坚韧组织：防止胫骨相对股骨**向前移动和扭转**，和肌肉一起提供膝关节大部分稳定\n还给大脑传递膝关节运动和平衡的信息（**本体感觉**）', 'teal'),
    ('box', '怎么伤', '多发生在运动中，最常见是**膝关节扭转**；突然急停、变向或与人碰撞也会\n早期：肿胀、难活动、走路痛 → 之后可能**不稳、打软腿**', 'accent'),
    ('box', '常合并的损伤', '**半月板**（最常见；血供差，有的撕裂不愈合，可致早发关节炎）\n内外侧副韧带、后外侧角\n软骨损伤（游离体、软骨瓣 → 弹响、疼痛）\n后交叉韧带、Segond 骨折', 'yellow'),
    ('box', '另一侧也可能伤', '研究显示约 **16/100** 的人之后会伤到**另一条腿**的 ACL', 'navy')])
deck.text('要不要做重建手术？', '原文：Will I need ACL reconstructive surgery?', [
    ('box', '怎么确诊', '问病史 + 查体 + 影像；受伤时多会拍 X 线，**MRI 确诊**，通常由外科医生或膝关节专科安排', 'grey'),
    ('box', '完全断裂的 ACL 自己长不好', '但**不是人人都要手术**：膝关节不再反复打软腿、愿意调整活动、其他结构没有明显损伤的人可以保守', 'teal'),
    ('box', '共同决策', '由你和外科医生、膝关节专科、物理治疗师一起决定\n选了保守，**之后仍可改为手术**', 'navy'),
    ('box', '保守效果不好怎么办', '仍痛、不稳 → 可以选择手术稳定膝关节\n继续不手术：情况不太会自己变好，可能**早发骨关节炎**，要坚持规律锻炼保持力量和稳定', 'accent'),
    ('box', '什么时候建议手术', '尽力康复后仍打软腿、不稳、回不到日常活动；或合并疼痛反复肿胀、交锁卡顿', 'yellow')])
deck.text('受伤后头几天 + 等手术期间', '原文：How do I care for my knee?', [
    ('box', '头几天', '**减少活动量**，可开始基础动作\n可用止痛药、护膝或弹力绷带；肿胀就**冰敷**\n除非医生另有交代，可以**完全负重行走**；走不了可给拐杖，必要时给支具', 'teal'),
    ('box', '等手术也要做康复：一定要！', '术前做康复的人术后**更可能回归运动**——进手术时越强壮，术后就越强壮\n术后可能要部分负重或不负重的人，术前还要**练上肢力量**\n尽早康复也有助于预防再次受伤', 'accent'),
    ('box', '康复目标', '先恢复**完全主动活动度**、不拄拐不跛行\n再练到两腿**力量和平衡相同**，最后练爆发力和耐力，实现个人目标', 'navy')])
deck.text('练多少、痛到什么程度算正常', '原文：Will these exercises hurt?', [
    ('box', '剂量（全书通用）', '每个动作每天 **2～3 组**，每组 **8～12 次**，组间休息 **60～120 秒**（一次练完，不要早中晚各一组）\n每周至少 **3 天**、最多 **5 天**', 'teal'),
    ('box', '疼痛 ≤4/10：可以接受', '练的时候或第二天酸痛都正常（0 分不痛，10 分最痛）', 'navy'),
    ('box', '疼痛 >4/10 或练后肿胀', '① 减少次数或组数\n② 放慢速度\n③ 延长组间或次间休息\n缓解后再慢慢加回次数、组数或速度', 'accent'),
    ('box', '注意', '**不应该靠多吃止痛药**来完成训练；疼得很厉害（且近期没手术）→ 找药剂师或全科医生', 'yellow')])
deck.text('术前①：先找回活动度', '原文 Exercises 1～4（示范为左膝，练受伤侧）', [
    ('steps', [('1', '**足跟滑动**：躺下，脚跟在床面上轻轻前后滑动，膝关节尽量弯、尽量伸'),
               ('2', '**膝下垂伸直**：坐位腿伸直，脚跟垫在靠垫上，让重力把膝压直；舒服的话轻轻往下按'),
               ('3', '**股四头肌等长收缩**：坐位腿伸直，大腿肌肉轻轻收紧再放松，膝不动'),
               ('4', '**踝泵**：坐或躺，快速勾脚、绷脚')]),
    ('h', '满足这 3 条才进入力量训练'),
    ('bul', ['受伤膝能**弯、伸到和健侧一样**', '以上动作做起来已经很轻松', '膝关节专科或物理治疗师**同意**开始强化'])])
deck.text('术前②：力量与平衡 11 个动作', '原文 strengthening exercises', [
    ('steps', [('1', '**短弧股四头肌**：膝下垫毛巾卷，压毛巾抬起脚跟（不是抬整条腿）'), ('2', '**直腿抬高**：收紧大腿，伸直腿抬到脚跟高过髋'),
               ('3', '**1/4 蹲**：双脚与肩同宽、手叉腰、挺胸，微屈膝再站起'), ('4', '**上台阶**：受伤腿先上，控制住，尽量不用手拉'),
               ('5', '**俯卧屈膝**：趴着弯膝，再慢慢放下'), ('6', '**臀桥**：屈膝仰卧，夹臀抬起再慢放'),
               ('7', '**罗马尼亚硬拉**：背挺直、屈髋到大腿后侧发紧；可逐渐加小重量'), ('8', '**侧卧抬腿**：腿伸直向侧方抬约 **5 cm**'),
               ('9', '**提踵**：双脚与髋同宽，踮脚再放下'), ('10', '**单腿站**：用最少的扶持保持平衡 **30 秒**'),
               ('11', '**有氧**：活动度够了就骑固定自行车，从轻松 **5 分钟**开始；也可椭圆机、游泳')])])
fig, ax = plt.subplots(figsize=(9.6, 4.4))
lab = ['手术效果良好', '能回归运动', '回到伤前运动水平']; lo = [90, 73, 50]; hi = [90, 83, 65]
for i, (l, a, b) in enumerate(zip(lab, lo, hi)):
    y = 2 - i; ax.barh(y, b, .55, color='#D6E4F2'); ax.barh(y, a, .55, color='#1F5F8B')
    ax.text(b + 1.5, y, f'{a}%' if a == b else f'{a}%～{b}%', va='center', fontsize=20, weight='bold', color='#16324F')
ax.set_yticks([2, 1, 0], lab, fontsize=19); ax.set_xlim(0, 112); ax.set_xticks([]); ax.spines[['top', 'right', 'bottom']].set_visible(False); fig.tight_layout()
deck.chart('ACL 重建手术：做什么、效果如何', '原文 How successful…（编者据原文数字绘图）', fig, [
    ('box', '手术', '关节镜微创，多为**日间手术**、全麻；大多数需要**重建**（能直接修复的很少）\n移植物多用自体肌腱：**腘绳肌腱**（同侧或对侧）或**髌腱**；穿过胫骨和股骨隧道，用螺钉/纽扣固定', 'teal'),
    ('box', '回归运动', '外科医生建议**术后至少 12 个月**才能完全回归运动；延后到 12 个月以上结局更好', 'accent')])
fig, ax = plt.subplots(figsize=(9.6, 5.2))
lab = ['髌腱移植后髌骨痛', '5 年内移植物再断裂', '术后仍不稳', '膝关节僵硬', '深部感染']; lo = [20, 5, 5, 2, 1]; hi = [20, 8, 5, 5, 2]
for i, (l, a, b) in enumerate(zip(lab, lo, hi)):
    y = 4 - i; ax.barh(y, b, .55, color='#F4CFC9'); ax.barh(y, a, .55, color='#C0392B')
    ax.text(b + .4, y, f'{a}/100' if a == b else f'{a}～{b}/100', va='center', fontsize=18, weight='bold', color='#7a1f16')
ax.set_yticks(range(5)[::-1], lab, fontsize=17); ax.set_xlim(0, 26); ax.set_xticks([]); ax.spines[['top', 'right', 'bottom']].set_visible(False); fig.tight_layout()
deck.chart('手术有哪些风险', '原文 What are the risks?（编者据原文数字绘图）', fig, [
    ('bul', ['**深静脉血栓**：腿肿痛发热、皮肤变色；脱落到肺可致气促、胸痛、咯血 → 医院会评估并可能用药或弹力袜',
             '**感染**征兆：膝很热、红肿、伤口流黄脓 → 打 111 或去急诊', '术后**肿胀可持续约 3 个月**：冰敷 + 加压', '瘢痕周围、腿部**麻木**常见，一般不影响功能'])])
deck.text('术后：出院后要做的事', '原文：What should I do after ACL surgery?', [
    ('box', '听外科医生的', '给肘拐；医生会告诉你能**完全负重 / 部分负重 / 不负重**，以及要不要戴支具、戴多久（可能限制屈伸角度）', 'navy'),
    ('box', '每天冰敷', '减轻肿胀，帮助找回完全活动度', 'teal'),
    ('box', '复诊', '术后 **2 周内**应有门诊物理治疗预约；可选 ACL 专科康复班或一对一\n另有外科医生或膝关节专科随访', 'yellow'),
    ('box', '影响恢复速度的因素', '年龄（越大越慢）、受伤多久、术前有没有练、合并损伤、是否戴支具/不负重、是否坚持康复、并发症（如取腱处腘绳肌拉伤）、饮食和**吸烟**（戒烟是改善手术结局最好的一件事）', 'grey')])
deck.text('术后第 1 阶段：0～2 周', '原文 Phase 1：在物理治疗门诊前就要开始', [
    ('h', '戴支具：只做这 4 个'),
    ('steps', [('1', '**踝泵**：快速勾脚、绷脚'), ('2', '**股四头肌＋腘绳肌同时收缩**：膝下垫枕，脚跟往下踩、膝往枕头压，膝不动，保持 **5 秒 × 10 次**'),
               ('3', '**俯卧后伸髋**：趴着，腿向天花板抬'), ('4', '**侧卧外展**：手术腿伸直，向侧方抬约 **5 cm**')]),
    ('h', '不戴支具且允许完全负重：再加'),
    ('steps', [('5', '**足跟滑动**：仰卧，脚跟沿床面滑动屈伸膝'), ('+', '**1/4 蹲**　**提踵** → 轻松后改单腿　**单腿站 30 秒**')]),
    ('box', '注意', '严格按时间框架来，除非另有指示', 'accent')])
deck.text('术后第 2 阶段：约 2～6 周', '原文 Phase 2：物理治疗师同意后才开始', [
    ('steps', [('1', '**俯卧屈膝**：趴着弯膝，再慢慢放下'), ('2', '**臀桥**：屈膝仰卧，夹臀抬起慢放；轻松后改**单腿**'),
               ('3', '**靠墙蹲**：背靠墙下滑，脚跟不离地，再推回起始位'), ('4', '**上台阶**：在一级台阶上上、下')]),
    ('box', '之后', '由物理治疗师根据你的个人目标（如跑步、踢球）继续进阶，练力量、平衡、爆发力和耐力', 'teal'),
    ('box', '手册扉页的小设计', '让患者写下 **3 个想回归的目标以及原因**——康复全程围绕个人目标来安排', 'yellow')])
deck.text('收藏：ACL 康复要点', '据原文整理', [
    ('steps', [('剂量', '2～3 组 × 8～12 次，组间 60～120 s，每周 3～5 天'), ('疼痛', '≤4/10 可接受；超过就减量、放慢、多休息'),
               ('术前', '先找回活动度，再练力量和平衡'), ('术后', '0～2 周基础动作；2～6 周遵医嘱进阶'), ('回归', '≥12 个月')]),
    ('h', '原文细节'),
    ('bul', ['术后 2b“单腿提踵”的文字其实写的是单腿站立保持 30 秒，与第 3 个动作“单腿站”重复', 'PDF 为网页打印版，原手册中的动作照片未保存在文件里']),
    ('box', '来源 · 版权', 'East Kent Hospitals University NHS Foundation Trust. Anterior Cruciate Ligament (ACL) injury: Information for patients from the Physiotherapy Department. Ref Web 640, 首发 2023 年 11 月\nCopyright © East Kent Hospitals University NHS Foundation Trust；本卡为编者中文整理。**仅供学习交流，如有侵权请联系删除**', 'grey')])
deck.save(OUT)
