#!/usr/bin/env python3
"""生成可直接粘贴进公众号后台的推文 HTML（全部样式内联，图片以 base64 内嵌）。

用法：python3 build.py   → 生成同目录下的 article.html
"""
import base64
import pathlib

HERE = pathlib.Path(__file__).parent

# ---------- 样式（公众号会过滤 <style> 和 class，只能用内联样式） ----------
RED = "#AB1942"   # 二级标题
BLUE = "#021EAA"  # 三级标题
PURPLE = "#7A4FD6"
TEXT = "#333333"
P_STYLE = f"margin:0 0 16px;font-size:15px;line-height:1.75;letter-spacing:0.5px;color:{TEXT};text-align:left;"


def p(html, extra=""):
    return f'<p style="{P_STYLE}{extra}">{html}</p>'


def b(t):
    return f'<strong style="color:#000;">{t}</strong>'


def u(t):
    return f'<span style="text-decoration:underline;text-underline-offset:3px;">{t}</span>'


def hl(t):
    return f'<strong style="color:{PURPLE};">{t}</strong>'


def red(t):
    return f'<strong style="color:{RED};">{t}</strong>'


def h2(t):
    return (
        '<hr style="border:none;border-top:3px solid #111;margin:36px 0 22px;">'
        f'<h2 style="margin:0 0 18px;font-size:16px;line-height:1.6;">'
        f'<span style="background-color:#000;color:#fff;padding:4px 10px;font-weight:bold;letter-spacing:1px;">{t}</span></h2>'
    )


def h3(t):
    return f'<h3 style="margin:30px 0 14px;font-size:16px;line-height:1.6;color:{RED};font-weight:bold;">{t}</h3>'


def h4(t):
    return f'<h4 style="margin:24px 0 12px;font-size:15px;line-height:1.6;color:{BLUE};font-weight:bold;">{t}</h4>'


def quote(en, zh):
    return (
        f'<blockquote style="margin:0 0 18px;padding:12px 14px;border-left:3px solid {RED};background-color:#f7f7f7;">'
        f'<p style="margin:0 0 10px;font-size:14px;line-height:1.7;color:#555;font-style:italic;">"{en}"</p>'
        f'<p style="margin:0;font-size:14px;line-height:1.75;color:{TEXT};">"{zh}"</p>'
        "</blockquote>"
    )


def ul(items, square=False):
    lis = "".join(
        f'<li><p style="margin:0 0 8px;font-size:15px;line-height:1.75;color:{TEXT};">{i}</p></li>' for i in items
    )
    return f'<ul style="margin:0 0 16px;padding-left:1.3em;list-style-type:{"square" if square else "disc"};">{lis}</ul>'


def table(head, rows, first_bold=True):
    th = "".join(
        f'<th style="border:1px solid #d9d9d9;background-color:#f2f2f2;padding:6px 5px;font-size:13px;line-height:1.5;color:#000;text-align:center;font-weight:bold;">{h}</th>'
        for h in head
    )
    body = ""
    for r in rows:
        tds = "".join(
            f'<td style="border:1px solid #d9d9d9;padding:6px 5px;font-size:13px;line-height:1.55;color:{TEXT};vertical-align:middle;">'
            f'{b(c) if (first_bold and i == 0) else c}</td>'.replace(
                'vertical-align:middle;">', 'vertical-align:middle;white-space:nowrap;">' if i == 0 and len(c) <= 6 else 'vertical-align:middle;">', 1)
            for i, c in enumerate(r)
        )
        body += f"<tr>{tds}</tr>"
    return (
        '<table style="width:100%;border-collapse:collapse;margin:0 0 18px;">'
        f"<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>"
    )


def img(n, caption=None):
    data = base64.b64encode((HERE / "images" / f"img{n:02d}.jpg").read_bytes()).decode()
    html = (
        '<p style="margin:0 0 8px;text-align:center;">'
        f'<img src="data:image/jpeg;base64,{data}" alt="图{n}" style="width:100%;max-width:100%;height:auto;display:block;margin:0 auto;"></p>'
    )
    if caption:
        html += f'<p style="margin:0 0 20px;font-size:12px;line-height:1.6;color:#888;">🔖图{n}：{caption}</p>'
    return html


def small(t):
    return f'<p style="margin:0 0 16px;font-size:12px;line-height:1.6;color:#888;">{t}</p>'


# ---------- 正文 ----------
A = []
A.append(img(1, "原文首页（IJSPT 2019 年第 14 卷第 5 期）"))

# 文献卡片
A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：A Comprehensive Rehabilitation Program for Treating Lateral Elbow Tendinopathy（肱骨外上髁肌腱病的综合康复方案）",
    f"{b('作者')}：Joseph M. Day, PT, PhD · Ann M. Lucado, PT, PhD, CHT · Timothy L. Uhl, PT, ATC, PhD",
    f"{b('机构')}：美国代顿大学物理治疗系 · 默瑟大学物理治疗系 · 肯塔基大学物理治疗系",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2019;14(5):818-834",
    f"{b('DOI')}：10.26603/ijspt20190818（PMCID：PMC6769266）",
    f"{b('文章类型')}：临床评论（Clinical Commentary）",
    f"{b('证据级别')}：原文标注 Level 5（专家意见 / 临床评论）",
    f"{b('关键词')}：scapula · lateral epicondylitis · shoulder · lateral epicondylalgia · movement system",
], square=True))

# 背景
A.append(h2("🎯 背景：网球肘，只盯着肘就够了吗？"))
A.append(p("网球肘（肱骨外上髁肌腱病，Lateral Elbow Tendinopathy，LET）几乎是每个物理治疗师门诊里的“常客”。"))
A.append(quote(
    "Lateral elbow tendinopathy (LET) is the most common musculoskeletal elbow tissue injury and can result in significant limitations in function and decreased participation in activities.",
    "肱骨外上髁肌腱病（LET）是最常见的肘部肌肉骨骼组织损伤，可导致明显的功能受限和活动参与度下降。",
))
p_bg = (
    f"传统的处理思路几乎都集中在{b('局部')}：伸腕肌离心训练、肘关节松动、深层横向按摩、冰敷、护具……"
    "这些方法短期内确实能缓解疼痛、改善功能。"
)
A.append(p(p_bg))
A.append(p(f"但问题来了——{b('到底什么才是“循证的多模式方案”？每个动作做多少、多重、多久、什么时候进阶？')}文献几乎没有给出答案。"))
A.append(p(
    f"更重要的是，近年来多项研究发现：{hl('网球肘患者常常伴有肩胛带肌力下降')}。"
    f"按照{b('动力链理论（Kinetic Chain Theory，KCT）')}，近端不稳，远端就要“替它干活”，"
    f"{u('肘和腕的伸肌腱负荷因此被放大')}。"
))
A.append(p("然而，此前没有任何一篇文献把“肩胛肌训练 + 局部肘腕治疗”写成一套足够详细、可以照着复制的临床方案。"))
A.append(p(f"这就是 Day 等人这篇临床评论要解决的问题——{b('给出一份细到动作、剂量和进阶标准的“双区域康复方案”')}。"))

# 核心概念
A.append(h2("🔴 核心概念：什么是“双重康复方案（DRP）”？"))
A.append(p("在逐节解读之前，先用两张表把这篇文章的核心框架讲清楚——"))
A.append(h3("传统局部方案 vs 本文的 DRP"))
A.append(table(
    ["对比项", "传统局部方案", "双重康复方案（DRP）"],
    [
        ["治疗区域", "肘 / 腕局部", "肩胛 + 前臂（肘 / 腕）两个区域"],
        ["理论基础", "局部组织修复", "局部修复 + 动力链理论"],
        ["运动处方", "多为笼统描述", "三阶段进阶，动作、组数、负荷都有明确规定"],
        ["进阶依据", "多按时间", "按功能标准（能否无痛完成特定测试）"],
        ["辅助手段", "按经验选用", "MWM 松动为核心，牵伸 / 支具 / 软组织 / 冷疗为补充"],
    ],
))
A.append(h3("DRP 的六大模块一览"))
A.append(table(
    ["模块", "核心内容", "剂量要点"],
    [
        ["① 主动热身", "上肢功率车（首选）或跑步机", "≤10 分钟，无阻力 / 平地 2.0 mph"],
        ["② 肩胛肌强化矩阵", "前锯肌 + 中下斜方肌，三阶段进阶", "逐步加至 3×10，阶段 2/3 最多 3×15"],
        ["③ 腕肘强化矩阵", "伸腕肌、桡偏肌、屈伸肘肌，三阶段进阶", "同上；阶段 3 引入增强式训练"],
        ["④ 患者教育", "负荷管理 + 人体工效学调整", "贯穿全程"],
        ["⑤ 关节松动", "肘关节动态松动术（MWM）", "每次 6-10 次，每周最多 3 次 × 4 周"],
        ["⑥ 其他干预", "伸腕肌牵伸、反作用力支具、软组织松动、冷疗", "按需选用"],
    ],
))
A.append(img(2, "原文 Table 1 双重康复方案总览（上）"))
A.append(img(3, "原文 Table 1 双重康复方案总览（续）"))
A.append(p(
    f"{b('一句话概括')}：DRP ＝ {red('近端肩胛稳定')} ＋ {red('远端腕肘强化')} ＋ {red('局部手法与对症处理')}，"
    "并且每一步都写清楚了“做什么、做多少、何时进阶”。"
))

# 逐节解读
A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、背景与目的：为什么需要一份“可复制”的方案？"))
A.append(quote(
    "Still, there is not a precise description of what constitutes an evidence-based multimodal treatment program for LET especially when it comes to preventing recurrence of the condition. Moreover, little guidance is available regarding the dosage (including the intensity, duration, frequency, and progression) of exercise prescription.",
    "然而，对于什么才构成循证的 LET 多模式治疗方案，目前仍没有精确的描述，尤其是在预防复发方面。此外，关于运动处方的剂量（包括强度、持续时间、频率和进阶），几乎没有可供参考的指导。",
))
A.append(quote(
    "The KCT proposes that during functional arm motions kinetic energy is transferred from proximal to more distal segments of the arm, providing an effective and efficient mode for distal function. As a result, proximal weakness increases the demand on the distal segment therefore overloading the distal segment.",
    "动力链理论认为，在功能性上肢活动中，动能从近端节段传递到更远端的节段，为远端功能提供一种有效且高效的方式。因此，近端无力会增加远端节段的需求，从而使远端节段负荷过度。",
))
A.append(p("🔻" + b("循证分析：")))
A.append(ul([
    "LET 多为慢性退行性改变（胶原紊乱、瘢痕组织、血管增生），而非单纯“炎症”",
    "风险因素包括负荷相关（生物力学）和全身性因素（高胆固醇血症、糖尿病、激素失衡、年龄、遗传）",
    "康复干预通常优先于药物、激素注射或手术",
    f"已有观察性研究发现 LET 患者存在肩胛带无力，{u('但此前没有方案把肩胛训练写到可复制的程度')}",
]))
A.append(quote(
    "The dual rehabilitation program (DRP) for LET is based on combining rehabilitation to two regions; the scapula and forearm (elbow/wrist).",
    "LET 的双重康复方案（DRP）建立在对两个区域联合康复的基础上：肩胛和前臂（肘 / 腕）。",
))
A.append(p(f"作者团队拥有合计 25 年以上的 LET 治疗经验，该方案{b('正在一项多中心随机对照试验（RCT）中与标准局部治疗进行比较')}，并计划随访至出院后 6 个月和 1 年。"))

A.append(h3("❇️二、主动热身：先让组织“热起来”"))
A.append(quote(
    "Although the UBE is preferred, the treadmill can be utilized for patients in the acute phase of LET as a means of indirectly increasing the temperature of the common wrist extensors.",
    "虽然上肢功率车（UBE）是首选，但对于 LET 急性期的患者，可以使用跑步机来间接提高伸腕肌总腱的温度。",
))
A.append(ul([
    f"{b('首选')}：上肢功率车（UBE），舒适速度、{b('无阻力')}",
    f"{b('备选')}：跑步机，平地、2.0 mph（约 3.2 km/h），适用于肘部激惹性高的患者",
    f"{b('时长')}：两种方式都{b('不超过 10 分钟')}",
    "目的：提高软组织温度、增强随后的肌肉表现；短时有氧运动还有助于降低疼痛敏感性",
]))
A.append(p(f"⚠️{b('临床提示')}：高激惹患者避免直接上 UBE，因为握把和蹬转本身就会给伸腕肌加载。"))

A.append(h3("❇️三、肩胛肌强化矩阵：近端稳定是怎么练出来的？"))
A.append(h4("🔻1. 三阶段设计：依据肌电（%MVIC）挑选动作"))
A.append(quote(
    "For neuromuscular re-education (phase 1), others have recommended exercises in the range of 20-40% of MVIC. In general, exercises producing higher than 40% MVIC will induce a strengthening stimulus.",
    "对于神经肌肉再教育（阶段 1），既往研究推荐选用 20%-40% MVIC 范围内的练习。一般而言，产生高于 40% MVIC 的练习才会诱发力量训练刺激。",
))
A.append(table(
    ["阶段", "目标", "负荷特点", "MVIC"],
    [
        ["阶段 1", "神经肌肉再教育", "无阻力或等长激活", "20%-40%"],
        ["阶段 2", "渐进抗阻强化", "轻-中等负荷 / 短力臂", "≥40%"],
        ["阶段 3", "进一步强化", "中-大负荷 / 长力臂", "≥40%"],
    ],
))
A.append(p(f"动作还兼顾了{b('上斜方肌 / 下斜方肌（UT/LT）比值')}——尽量多练下斜方肌，少让上斜方肌代偿。前侧（{b('前锯肌')}）和后侧（{b('中下斜方肌')}）的练习分成两行，{u('每个阶段从每一行各选 1 个动作')}。"))
A.append(img(4, "原文 Figure 1 肩胛肌强化进阶示例：阶段 1 等长肩胛后缩 → 阶段 2 弹力带划船 → 阶段 3 俯卧后伸"))
A.append(table(
    ["阶段", "前锯肌行（选 1）", "中下斜方肌行（选 1）"],
    [
        ["阶段 1", "肩胛下沉 / 推球下压 / 擦墙上滑 / 站立推球滚动", "等长肩胛后缩 / 低位划船 / 挺胸伸展 / 无负重割草机"],
        ["阶段 2", "仰卧负重前推 / 推墙 / 弹力带跨步前推 / 跪姿俯卧撑 plus", "俯卧后伸（无负重）/ 俯卧 135° 上举 / 割草机 + 外旋 / 弹力带划船"],
        ["阶段 3", "直臂内收下拉 / 抱树（水平内收）/ 上勾拳 / 标准俯卧撑 plus", "俯卧负重后伸 / 弹力带 90° 水平后拉 / 俯卧水平外展 / 弹力带水平外展"],
    ],
))
A.append(img(5, "原文附录 A 肩胛肌强化阶段 1：等长募集"))
A.append(img(6, "原文附录 A 肩胛肌强化阶段 2：轻负荷 / 短力臂"))
A.append(img(7, "原文附录 A 肩胛肌强化阶段 3：大负荷 / 长力臂"))

A.append(h4("🔻2. 进阶标准：按“能力”而不是按“时间”"))
A.append(quote(
    "In order to progress to Phase 2 the patient must demonstrate the ability to isolate scapular retraction/ sternal lift with correct head posture from a resting neutral posture 20 times in a row while standing in an upright posture without substitution or support and without aggravating symptoms.",
    "要进入阶段 2，患者必须能在直立站姿下，从放松的中立姿势开始，以正确的头部姿势连续 20 次独立完成肩胛后缩 / 挺胸动作，无代偿、无支撑、且不加重症状。",
))
A.append(table(
    ["进阶", "必须达到的标准"],
    [
        ["阶段 1 → 2", "站姿连续 20 次独立完成肩胛后缩 / 挺胸，每次保持 5 秒，无代偿、不加重症状"],
        ["阶段 2 → 3", "单臂划船 10 lb（约 4.5 kg）× 20 次，无痛、无代偿、症状不加重；且能单臂前推 10 lb，从腰部推到肩高"],
    ],
))
A.append(p(f"💡{b('实用小技巧')}：作者给出了一个“10 lb”的简易实现——{hl('黑色弹力带剪 50 cm')}，对身高 5-6 英尺（约 152-183 cm）的人拉到末端约为 10 lb；身高超过 6 英尺则用 60 cm 长的弹力带或拉力器。"))

A.append(h4("🔻3. 组数与加阻规则：24 小时 + 1 级疼痛原则"))
A.append(quote(
    "In all phases, the patient begins without weight and when the patient is no longer experiencing 24 hour post onset muscle soreness or the pain does not go up more than one level on the numeric pain rating scale (NPRS) (0-10), then resistance can be added.",
    "在所有阶段，患者都从无负重开始；当患者不再出现运动后 24 小时的肌肉酸痛，或疼痛在数字疼痛评分（NPRS，0-10）上上升不超过 1 级时，即可增加阻力。",
))
A.append(ul([
    f"{b('阶段 1')}：目标是动作募集，无症状、技术正确地完成 {b('3 组 × 10 次')}",
    f"{b('阶段 2、3')}：目标是力量和耐力，最多 {b('3 组 × 15 次，组间休息 60 秒')}",
    f"允许患者根据自身反馈{b('自我调节（autoregulate）')}次数、组数和负荷",
]))
A.append(p(f"⚠️{b('注意')}：正文写阶段 2/3 可做到 3×15，而 Table 1 写的是“逐步加至 3×10”。临床上可以把 3×10 作为起点、3×15 作为上限。"))

A.append(h3("❇️四、腕肘强化矩阵：局部肌腱怎么加载？"))
A.append(h4("🔻1. 同样的三阶段逻辑"))
A.append(table(
    ["阶段", "重点", "代表动作"],
    [
        ["阶段 1", "关节活动度 + 等长募集", "屈伸腕 / 桡尺偏 / 扭棍 / 捏橡皮泥 / 等长屈腕 / 等长伸腕"],
        ["阶段 2", "轻负荷、短力臂的向心 + 离心", "伸肘扭棍 / 弹力带屈肘（掌心向上、拇指向上、掌心向下）/ 屈肘位抗阻桡偏 / 屈肘位抗阻伸腕"],
        ["阶段 3", "长力臂、更大负荷、增强式训练", "增强式抛接球（掌心向上 / 向下）/ 伸肘位抗阻桡偏 / 伸肘位抗阻伸腕"],
    ],
))
A.append(p(f"阶段 2 → 3 的进阶遵循基本加载原则：{u('力臂更长、负重更多、重量或阻力更大、加入增强式训练')}。每个阶段{b('从清单中选 2-3 个动作')}。"))
A.append(img(8, "原文 Figure 2 伸腕肌强化进阶示例：短力臂等长 → 短力臂抗阻 → 长力臂抗阻"))
A.append(img(9, "原文附录 B 腕部强化三阶段动作清单"))
A.append(h4("🔻2. 进阶标准"))
A.append(table(
    ["进阶", "必须达到的标准"],
    [
        ["阶段 1 → 2", "腕关节全范围主动活动 + 等长伸腕均无痛"],
        ["阶段 2 → 3", "屈肘、前臂旋前支撑、腕悬于桌缘，向心 / 离心伸腕 20 次，无痛、无代偿、症状不加重；或者最大握力 ≥ 同年龄同性别常模的 80%"],
    ],
))
A.append(quote(
    "As an alternative, the patient could demonstrate a maximum effort grip strength that is no less than 80% of their age and sex matched normative data.",
    "作为替代标准，患者也可以通过证明其最大握力不低于同年龄、同性别常模数据的 80% 来进阶。",
))
A.append(p(f"握力测试体位：{b('坐位，肩中立，屈肘 90°，腕中立')}。定期用握力计复测，既能提供客观数据，也能{u('提升患者的康复动机')}。"))
A.append(p(f"⚠️{b('注意')}：阶段 2 → 3 的伸腕负荷，正文写 2 lb（约 0.9 kg），Table 1 写 5 lb（约 2.3 kg）。建议从 2 lb 起测，逐步过渡到 5 lb。"))

A.append(h3("❇️五、患者教育与家庭指导：不教育，就会复发"))
A.append(quote(
    "Education is unique in that it is ongoing and critical because without proper patient understanding of the insulting activities, it is likely that the patient will relapse with the symptoms or cause a delay in healing time.",
    "教育的独特之处在于它贯穿始终；它之所以关键，是因为如果患者不能正确理解哪些活动在损伤组织，症状很可能复发，或者愈合时间会被拖延。",
))
A.append(p("🔻" + b("原文给出的教育要点：")))
A.append(ul([
    f"{b('相对休息')}：暂停会增加肌腱负荷、诱发疼痛的活动，由治疗师指导合适的负荷和时机",
    f"{b('避免重复')}的腕、前臂、肘部动作，但{u('不要完全不用上肢')}，否则肌腱承受负荷的能力会进一步下降",
    f"{b('训练不加痛')}：运动时疼痛增加可能提示负荷过大",
    f"{b('加粗握柄')}：餐具、工具、球拍都换成更粗的握把",
    f"{b('工位调整')}：每 30 分钟起身一次；使用带麦克风的耳机和语音输入；用{hl('垂直鼠标')}让手腕保持中立位",
    f"{b('请教练纠正')}运动中的错误动作，或调整装备",
    f"{b('提物时掌心向上')}，避免掌心向下提重物",
    f"{b('避免把注射作为止痛手段')}：原文指出多次接受激素注射的患者，长期功能和疼痛往往更差",
]))
A.append(p(f"🎯{b('弹力带阻力参考（原文 Table 2）')}："))
A.append(table(
    ["弹力带颜色", "拉长 100% 时阻力（lb）", "拉长 200% 时阻力（lb）"],
    [
        ["黄色", "3.0", "4.3"],
        ["红色", "3.7", "5.5"],
        ["绿色", "4.6", "6.7"],
        ["蓝色", "5.8", "8.6"],
        ["黑色", "7.3", "10.2"],
    ],
))
A.append(small("🔖注：1 lb ≈ 0.45 kg；数据来源为 TheraBand 官方，原文引用。"))
A.append(img(10, "原文 Table 2 不同颜色 TheraBand 在不同拉伸长度下的阻力"))

A.append(h3("❇️六、关节松动：MWM 是局部手法的核心"))
A.append(quote(
    "A recent systematic review and meta-analysis found that mobilization with movement (MWM) techniques were effective at reducing pain and improving daily function up to three months after discharge in patients with LET.",
    "一项近期的系统综述和荟萃分析发现，动态关节松动术（MWM）能有效减轻 LET 患者的疼痛，并改善其日常功能，效果可持续至出院后 3 个月。",
))
A.append(table(
    ["技术", "操作要点", "适用情况"],
    [
        ["A. 肘关节持续外侧滑动 + 无痛抓握", "固定肱骨，向外侧滑动尺 / 桡骨；患者无痛范围内抓握并等长保持 5 秒", "抓握时肘外侧疼痛加重"],
        ["B. 松动带辅助外侧滑动", "用松动带提供同方向的外侧滑动力，患者改为主动伸肘", "同上"],
        ["C. 肱桡关节后前向滑动", "桡骨头相对尺骨做前向滑动，患者不做主动运动", "前两种技术效果不佳时"],
    ],
))
A.append(ul([
    f"{b('患者体位')}：仰卧，上肢有支撑、轻度外展，伸肘，前臂旋前",
    f"{b('治疗师位置')}：站在患侧，面向患者",
    f"{b('剂量')}：每次 6-10 次；每周最多 3 次，持续 4 周",
    f"{b('继续的前提')}：{u('只要疼痛明显缓解，且操作后没有延迟出现的疼痛')}",
]))
A.append(img(11, "原文 Figure 3 肘关节动态松动术（MWM）的三种技术"))
A.append(img(12, "原文附录 C 肘关节 MWM 操作细节"))

A.append(h3("❇️七、其他干预：按需选用的“工具箱”"))
A.append(p(f"作者建议在康复早期就用上这些手段，{b('先把疼痛控制住，让患者能更充分地参与运动训练')}——而运动训练才是长期功能改善更有效的部分。"))
A.append(h4("🔹1. 伸腕肌牵伸"))
A.append(quote(
    "Caution should be exercised against aggressive stretching if the pain on palpation is insertional (i.e. potentially related to enthesopathy) where compressive loads (stretching) can be catabolic in nature resulting in a negative response to other interventions.",
    "如果触诊疼痛位于止点处（即可能与附着点病变有关），应避免激进的牵伸，因为此处的压缩负荷（牵伸）可能具有分解代谢作用，导致对其他干预的负面反应。",
))
A.append(ul([
    f"所有患者都应学习伸腕肌牵伸：{b('即使柔韧性不差，牵伸也能短期抑制疼痛')}",
    f"Mill 征疼痛 {b('> 3/10')} 时：改为{hl('屈肘位')}、放松示指和中指，只用另一只手被动屈腕，减小伸腕肌张力",
    f"剂量：{b('每天 3 次，每次保持 30 秒，重复 3 遍')}",
]))
A.append(h4("🔹2. 反作用力支具（网球肘带）"))
A.append(quote(
    "The strap should be placed about two finger widths below the painful area and the patients are instructed to adjust the tension to comfort while muscles are relaxed, and not to over tighten.",
    "支具应放在疼痛区域下方约两横指处；指导患者在肌肉放松时把松紧调到舒适，不要绑得过紧。",
))
A.append(ul([
    "原理：把张力转移到肌腱更远端的部位，让受伤的近端止点有时间愈合",
    f"{b('工作或运动时佩戴，休息和睡觉时取下')}",
    "特别适合无法停止致病活动的人群，如高水平网球运动员、体力劳动者",
    "注意观察有无桡神经刺激症状",
]))
A.append(img(13, "原文 Figure 4 肱骨外上髁肌腱病反作用力支具"))
A.append(h4("🔹3. 软组织松动"))
A.append(ul([
    f"可选：{b('深层横向摩擦按摩（DFM）')}、伸腕肌肌腹按摩、肌筋膜放松，每次约 3-10 分钟",
    f"⚠️原文坦言：{u('软组织技术治疗肌腱病的证据有限')}，应根据查体结果（如软组织受限导致伸肘或屈腕活动度下降）决定是否使用",
]))
A.append(h4("🔹4. 冷疗"))
A.append(ul([
    f"{b('首选冰按摩')}：痛点处 3-5 分钟，尤其是在诱发活动之后",
    "不耐受时：冰袋隔一层薄布（如枕套），每次 10 分钟，每天最多 3-4 次",
    "机制：闸门控制理论 + 浅表血管收缩，减少化学性疼痛（原文写作“gait control theory”，应为 gate control theory 的笔误）",
]))

A.append(h3("❇️八、局限与鉴别诊断"))
A.append(quote(
    "Although the provided protocol is based on best available evidence, the authors acknowledge that the research regarding scapular muscle training for patients with LET is limited to observational studies only.",
    "虽然本方案基于现有最佳证据，但作者承认，关于 LET 患者肩胛肌训练的研究目前仅限于观察性研究。",
))
A.append(quote(
    "Lateral elbow tendinopathy is often misdiagnosed.",
    "肱骨外上髁肌腱病经常被误诊。",
))
A.append(p("🔻" + b("开始 DRP 之前，必须先排除：")))
A.append(table(
    ["需鉴别的情况", "可选的筛查"],
    [
        ["颈神经根病", "Wainner 测试组合 + C6、C7 神经学筛查"],
        ["桡管综合征（骨间后神经卡压）", "抗阻旋后试验"],
        ["外侧副韧带损伤、肱桡关节骨关节炎、骨折", "针对关节内结构的负荷试验"],
        ["肱三头肌腱炎、腕部损伤的牵涉痛", "病史 + 针对性查体"],
    ],
))

# 证据评价
A.append(h2("🔍 证据评价"))
A.append(h3("📄这篇文章能告诉我们什么、不能告诉我们什么"))
A.append(p("▪️" + b("值得肯定的部分：")))
A.append(ul([
    "方案细到动作图片、组数、负荷和进阶标准，可复制性很强——这正是既往文献最缺的",
    "肩胛动作按 %MVIC 和 UT/LT 比值挑选，有肌电学依据",
    "以“能力标准”而非“时间”进阶，配合 24 小时 / NPRS 1 级的负荷监测规则，安全且个体化",
    "MWM、牵伸、支具、冷疗等辅助手段都给出了适应证和剂量",
]))
A.append(p("▪️" + b("需要谨慎看待的部分：")))
A.append(ul([
    f"{b('证据级别为 Level 5（专家意见）')}：文章只描述方案，{u('没有报告任何疗效数据')}，配套 RCT 结果需另行查阅",
    "“肩胛无力 → 肘部负荷过大”的依据目前主要是观察性研究和动力链理论，因果关系尚未证实",
    "正文和 Table 1 有几处剂量不一致（组数 3×10 与 3×15；伸腕负荷 2 lb 与 5 lb；冰袋 10 分钟与 15 分钟），临床使用时需要自行统一",
    "“避免注射”等建议属于作者基于文献的观点，具体医疗决策仍需与医生共同讨论",
]))

# 临床启示
A.append(h2("🧠 物理治疗临床实践启示"))
A.append(h3("🔻启示1：网球肘患者，记得查一查肩胛"))
A.append(p("评估时不要只停留在肘部压痛、Mill 征和握力。建议加入："))
A.append(ul([
    "肩胛后缩 / 下沉的控制能力（能否连续 20 次、每次保持 5 秒且无代偿）",
    "前锯肌、中下斜方肌的徒手肌力或手持测力",
    "上斜方肌是否过度代偿",
]))
A.append(h3("🔻启示2：用“通关标准”管理进阶"))
A.append(p(f"把每个阶段的进阶标准写进治疗记录，{b('达标才升级')}。这样既能避免进阶过快导致复发，也能让患者清楚看到自己的进步。"))
A.append(h3("🔻启示3：把“24 小时 + NPRS 1 级”原则教给患者"))
A.append(ul([
    "训练后 24 小时内没有持续酸痛，或疼痛上升不超过 1 级 → 可以加阻力",
    "超过这个范围 → 维持或降低负荷",
    "这条规则简单好记，非常适合家庭训练计划（HEP）",
]))
A.append(h3("🔻启示4：手法为训练“开路”"))
A.append(p(f"MWM、牵伸、冷疗、支具的定位是{b('控制疼痛、让患者能练得动')}，而不是替代运动训练。每次治疗都应以主动训练结束。"))
A.append(h3("🔻启示5：教育和工效学调整决定是否复发"))
A.append(p(f"粗握柄、垂直鼠标、掌心向上提物、每 30 分钟起身——这些“小事”{u('直接决定患者回到工作和运动后会不会再次受伤')}。"))

# 总结
A.append(h2("📌 总结：网球肘的问题，可能不只在肘"))
A.append(p("这篇临床评论的价值，不在于提出了全新的治疗技术，而在于把分散的循证手段整合成一套可执行的方案："))
A.append(p(
    f"{red('① 热身')}：上肢功率车或跑步机，≤10 分钟<br>"
    f"{red('② 近端')}：肩胛肌三阶段强化（前锯肌 + 中下斜方肌）<br>"
    f"{red('③ 远端')}：腕肘三阶段强化，最后加入增强式训练<br>"
    f"{red('④ 手法')}：肘关节 MWM，每次 6-10 次<br>"
    f"{red('⑤ 辅助')}：牵伸、支具、软组织、冷疗按需选用<br>"
    f"{red('⑥ 教育')}：负荷管理 + 工效学调整，贯穿全程"
))
A.append(p("💡" + b("对物理治疗师的核心启示：")))
A.append(ul([
    "治疗网球肘时，把肩胛纳入评估和训练",
    "进阶看能力标准，不看时间",
    "负荷监测用“24 小时 + NPRS 1 级”原则",
    "手法和对症处理是为主动训练服务的",
    "这仍是专家意见级别的方案，期待配套 RCT 的结果",
]))
A.append(p(f"📡{b('人体是一条动力链。远端反复出问题时，不妨往近端看一看。')}"))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注本公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Day JM, Lucado AM, Uhl TL. A Comprehensive Rehabilitation Program for Treating Lateral Elbow Tendinopathy. "
    "Int J Sports Phys Ther. 2019;14(5):818-834. doi:10.26603/ijspt20190818. PMCID: PMC6769266.</em><br>"
    "文中图表均截取自原文，仅用于学术交流。"
))

ARTICLE = "\n".join(A)

PAGE = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>网球肘综合康复方案推文</title>
<style>
  body{{margin:0;background:#ededed;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;}}
  .bar{{position:sticky;top:0;z-index:9;background:#fff;border-bottom:1px solid #ddd;padding:10px 16px;}}
  .bar button{{background:#07c160;color:#fff;border:0;border-radius:6px;padding:8px 16px;font-size:15px;cursor:pointer;}}
  .bar span{{margin-left:10px;font-size:13px;color:#576b95;}}
  .meta{{max-width:640px;margin:16px auto 0;padding:14px 16px;background:#fffbe6;border:1px solid #f0e2a8;font-size:13px;line-height:1.7;color:#555;box-sizing:border-box;}}
  .phone{{max-width:640px;margin:16px auto 40px;background:#fff;padding:20px 16px 28px;box-sizing:border-box;}}
  .phone h1{{font-size:22px;line-height:1.4;margin:0 0 10px;color:#000;}}
  .phone .by{{font-size:14px;color:#576b95;margin-bottom:20px;}}
</style></head>
<body>
<div class="bar"><button id="copy">一键复制正文</button><span id="msg">复制后到公众号后台编辑器里直接粘贴</span></div>
<div class="meta">
<b>建议标题：</b>「网球肘」从肩胛到手腕：一套分期进阶的肱骨外上髁肌腱病综合康复方案<br>
<b>备选标题：</b>网球肘反复发作？这份“肩胛＋腕肘”双重康复方案值得收藏<br>
<b>摘要：</b>IJSPT 2019 临床评论精读：热身、肩胛与腕肘三阶段强化、MWM 松动、教育与辅助手段，附完整进阶标准和剂量。<br>
<b>说明：</b>本黄色框和标题不在复制范围内。标题请填到后台“标题”栏；若粘贴后个别图片没有显示，请从 images 文件夹按“图N”编号手动插入。
</div>
<div class="phone">
<h1>「网球肘」从肩胛到手腕：一套分期进阶的肱骨外上髁肌腱病综合康复方案</h1>
<div class="by">原创 · 你的公众号名称</div>
<section id="article">
{ARTICLE}
</section>
</div>
<script>
document.getElementById('copy').onclick = async function () {{
  var el = document.getElementById('article'), msg = document.getElementById('msg');
  try {{
    var html = el.innerHTML;
    await navigator.clipboard.write([new ClipboardItem({{
      'text/html': new Blob([html], {{type: 'text/html'}}),
      'text/plain': new Blob([el.innerText], {{type: 'text/plain'}})
    }})]);
  }} catch (e) {{
    var r = document.createRange(); r.selectNodeContents(el);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    document.execCommand('copy'); s.removeAllRanges();
  }}
  msg.textContent = '已复制！去公众号编辑器里 Ctrl/⌘ + V 粘贴';
}};
</script>
</body></html>
"""

(HERE / "article.html").write_text(PAGE, encoding="utf-8")
print("written", HERE / "article.html", len(PAGE) // 1024, "KB")
