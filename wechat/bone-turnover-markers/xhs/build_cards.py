#!/usr/bin/env python3
"""《骨代谢生化指标临床应用专家共识(2026修订版)》（中国骨质疏松杂志 2026）→ 小红书 3:4 图文卡片。
原文非开放许可：图 1 为原文嵌入图（x58.jpg），原样使用未作修改；分类示意图为编者据原文表 1 绘制；卡片注明“仅供学习交流，如有侵权请联系删除”。
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
deck = Deck(series='骨质疏松', source='中国骨质疏松杂志 2026;32(10):1405-1413', fonts_dir=FONTS)
fp = deck._fontfile['M']; font_manager.fontManager.addfont(fp); plt.rcParams['font.family'] = font_manager.FontProperties(fname=fp).get_name()
F = lambda n: Image.open(f'{WORK}/{n}.jpg').convert('RGB')


def class_fig(w=9.6, h=5.2):
    """四类骨代谢生化指标（编者据原文表 1 绘制）"""
    g = [('钙磷代谢调节', 'PTH 甲状旁腺素\n降钙素 CT\n维生素 D3', '#1F5F8B'), ('骨形成标志物', 'BALP · 骨钙素 OC\nPINP · PICP\n骨保护素 OPG', '#2E8B57'),
         ('骨吸收标志物', 'TRACP\nCTX · NTX\n尿吡啶啉', '#C0392B'), ('激素与细胞因子', 'GH · 雌激素 · 睾酮\nIL-1 · IL-6 · TGF\nTNF-α · IGF', '#E3A21A')]
    fig, ax = plt.subplots(figsize=(w, h), dpi=100); ax.set_xlim(0, 4); ax.set_ylim(0, 3.3); ax.axis('off')
    for i, (t, s, c) in enumerate(g):
        x = .05 + i * 1.0
        ax.add_patch(FancyBboxPatch((x, 2.15), .88, .62, boxstyle='round,pad=0.01,rounding_size=0.06', fc=c, ec='none'))
        ax.text(x + .44, 2.46, t, ha='center', va='center', fontsize=18, color='white', weight='bold')
        ax.add_patch(FancyBboxPatch((x, .3), .88, 1.72, boxstyle='round,pad=0.01,rounding_size=0.06', fc='#F4F6F8', ec='none'))
        ax.text(x + .44, 1.16, s, ha='center', va='center', fontsize=17.5, color='#222', linespacing=1.8)
    fig.tight_layout(pad=.2); return fig


def fig2img(fig):
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=100, facecolor='white'); plt.close(fig); return Image.open(buf).convert('RGB')


deck.cover(['骨代谢', '生化指标', '专家共识 2026'], kicker='中国骨质疏松杂志 2026 · 共识',
           subtitle='P1NP、CTX、骨钙素……化验单怎么看', photos=[(fig2img(class_fig()), '四类指标（据原文表 1）')], banner='晨起空腹采血 · 同一时间复查')
deck.text('骨代谢指标能干什么', '原文引言', [
    ('box', '从哪来', '成骨细胞、破骨细胞分泌的酶和激素，以及骨基质胶原的代谢产物；可在**血、尿**中检测', 'teal'),
    ('box', '用途', '评价骨代谢状态、骨质疏松**诊断分型**、**预测骨折风险**、代谢性骨病鉴别诊断、**评估抗骨质疏松治疗反应**', 'navy'),
    ('box', '这版是第几版', '在 2023 修订版基础上，结合近年中英文文献更新为 2026 修订版', 'grey'),
    ('box', '常用检测方法', 'ELISA、化学发光（CLIA）、电化学发光（ECLIA）、放射免疫（RIA/IRMA）、高效液相色谱（HPLC）', 'yellow')])
deck.text('① 钙磷调节：PTH、降钙素、维生素 D', '原文 2.1', [
    ('box', 'PTH（甲状旁腺素）', '双重作用：**持续大剂量 → 骨吸收 > 骨形成**；**间歇小剂量 → 促进骨形成**\n升高：原发/继发性甲旁亢（如肾病）等；降低：甲旁减等', 'teal'),
    ('box', '降钙素（CT）', '减少破骨细胞数量和活性、降低血钙；与 PTH、1,25(OH)2D3 共同维持血钙\n明显升高要警惕**甲状腺髓样癌**等', 'navy'),
    ('box', '维生素 D 看 25(OH)D3', '1,25(OH)2D3 代谢快、储存少；临床用 **25(OH)D3** 反映体内维生素 D\n化学发光法：<10 缺乏、10～30 不足、30～100 充足、>100 中毒\n电化学发光法：<20 缺乏、21～29 不足、≥30 充足', 'accent'),
    ('box', '有多普遍', '我国多中心研究：维生素 D **缺乏 61.3%**、**不足 91.2%**', 'yellow')])
deck.text('② 骨形成标志物', '原文 2.2', [
    ('box', 'BALP 骨特异性碱性磷酸酶', '与骨基质**矿化**密切相关\n升高：Paget 病、甲旁亢、甲亢、高转换型骨质疏松、佝偻病/骨软化、骨转移等\n降低：肾病相关无动力骨病、甲旁减等低转换状态', 'teal'),
    ('box', '骨钙素（OC / BGP）', '维生素 K 依赖的钙结合蛋白，反映骨形成速率\n**抗骨吸收药使其下降，促骨形成治疗使其上升**；长期用糖皮质激素会降低', 'navy'),
    ('box', 'PINP / PICP', 'I 型前胶原切下的两端肽段，反映 I 型胶原合成（成骨）', 'yellow'),
    ('box', '骨保护素（OPG）', '和 RANKL 竞争结合，**抑制破骨细胞分化**、促其凋亡；绝经后女性随年龄升高', 'grey')])
deck.text('③ 骨吸收标志物', '原文 2.3', [
    ('box', 'CTX（I 型胶原交联 C 末端肽）', '使用最广的胶原降解标志物，反映破骨细胞活性\n**对抗骨吸收治疗反应快而灵敏**', 'accent'),
    ('box', 'NTX（I 型胶原交联 N 末端肽）', '尿中稳定的终产物，晨起和夜间尿 NTX 能很好反映骨吸收，特异性更高', 'teal'),
    ('box', 'TRACP（抗酒石酸酸性磷酸酶）', '分 5a、5b 两个亚型；升高见于甲旁亢、肾功能不全、骨转移、高转换型骨质疏松等', 'navy'),
    ('box', '尿吡啶啉 / 脱氧吡啶啉', '用尿液检测，需用**肌酐校正**', 'grey')])
deck.text('④ 激素与细胞因子', '原文 2.4（多用于个体化治疗和科研）', [
    ('box', '护骨的', '**雌激素**：缺乏是绝经后骨质疏松的主要原因\n**睾酮**：青春期达峰值骨量，成年后促成骨抑吸收\n**生长激素、IGF-1**：随年龄下降，IGF-1 低与骨折相关\n**TGF-β**：促进骨形成', 'teal'),
    ('box', '促骨吸收的', '**IL-1、IL-6、TNF-α**：促进破骨细胞生成和活性、抑制成骨\n雌激素下降时 IL-1、IL-6 升高 → 绝经后骨丢失', 'accent')])
deck.figure('⑤ 骨质疏松的化验路径', '原文图 1（原图未改动）', F('x58'), None, [
    ('bul', ['**基本项目**：血尿常规、肝肾功能、血清蛋白电泳、血钙、血磷、25(OH)D3、尿钙、尿钠', '**疗效评价首选**：BALP、骨钙素、PICP、PINP；必要时 PTH、降钙素、TRACP、尿钙/肌酐',
             '**查继发性**：血沉、CRP、性激素六项、1,25(OH)2D3、甲状腺功能、尿游离皮质醇、血气、尿本周蛋白、血尿轻链'])])
deck.text('⑥ 哪些因素会干扰结果', '原文 4.1 生物学变异', [
    ('box', '改变不了的', '年龄（儿童是成人的 **2～10 倍**；约 30 岁后逐渐下降）、绝经、妊娠和哺乳、肝肾病、用药（激素、肝素、抗惊厥药、避孕药）\n**骨折后前 4 周骨吸收标志物升高**；卧床也会升高', 'grey'),
    ('box', '吃饭', '进食后除 BALP 外都会下降，**早餐后 CTX 降约 20%** → 要空腹', 'yellow'),
    ('box', '运动', '**剧烈运动后 TRACP、BALP、CTX 明显升高，约 2 小时恢复** → 采血前别做剧烈运动', 'accent'),
    ('box', '时间', '多数指标清晨 2:00～8:00 最高、午后到夜间最低，波动 15%～50%；**BALP 相反**\n月经周期前 3～7 天采样最佳；维生素 D 受季节、日照影响', 'navy')])
deck.text('⑦ 怎么采样才准', '原文 4.1.2、4.2', [
    ('steps', [('血', '**晨起空腹**采血，EDTA 管，尽快分离，立即测或 -20 ℃以下保存；**避免溶血**（OC、TRACP 会降解）'),
               ('尿', '取**晨起第 1 次尿**，用肌酐校正'), ('复查', '同一患者**同一时间、同样条件**采集和处理'),
               ('方法', '化学发光、电化学发光自动化程度高、最常用；不同方法、仪器、试剂、实验室之间结果有差异')]),
    ('box', '编者建议（康复科）', '复查前一天和当天早上**别安排剧烈训练**；提醒空腹、固定时间采样；骨折后早期、长期卧床时解读要考虑变异', 'teal')])
deck.text('收藏 + 原文细节', '据原文整理', [
    ('steps', [('形成', 'BALP · 骨钙素 · PINP · PICP'), ('吸收', 'CTX · NTX · TRACP'), ('维 D', '看 25(OH)D3，≥30 ng/mL 充足'), ('采样', '晨起空腹、避免剧烈运动、同一时间复查')]),
    ('h', '原文对不上的地方'),
    ('bul', ['维生素 D 两套判读标准不衔接：电化学发光法“<20 缺乏、21～29 不足”，20～21 没有归类', '1,25(OH)2D3 半衰期同时写了“6～8 h”和“5～7 d”两个值',
             '正文说 CTX 对抗骨吸收治疗反应最灵敏，但疗效评价“首选”清单里没有列 CTX']),
    ('box', '文献 · 版权', '《中国骨质疏松杂志》骨代谢专家组. 骨代谢生化指标临床应用专家共识(2026修订版). 中国骨质疏松杂志, 2026, 32(10): 1405-1413.\n原文非开放许可，图 1 为原图未修改。**仅供学习交流，如有侵权请联系删除**', 'grey')])
deck.save(OUT)
