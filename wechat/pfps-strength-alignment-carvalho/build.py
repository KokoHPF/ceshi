#!/usr/bin/env python3
"""Gir de Carvalho 等 2026《强化股四头肌、髋外展肌和外旋肌以改变髌股疼痛综合征大学生的下肢轴向力线：前瞻性队列研究》（J Funct Morphol Kinesiol）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
配图：python3 tools/make_figs.py <work 目录> images <中文字体>（原文图 7～10 先用 tools/fig-translate 译成中文）
"""
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
    mark = "▪" if square else "•"
    return '<section style="margin:0 0 14px;">' + "".join(
        f'<p style="margin:0 0 8px;padding-left:1.2em;text-indent:-1.2em;font-size:15px;line-height:1.75;color:{TEXT};">'
        f'<span style="color:{RED};">{mark}</span>&nbsp;{i}</p>' for i in items) + "</section>"


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
    html = (
        '<p style="margin:0 0 8px;text-align:center;">'
        f'<img src="images/img{n:02d}.jpg" alt="图{n}" style="width:100%;max-width:100%;height:auto;display:block;margin:0 auto;"></p>'
    )
    if caption:
        html += f'<p style="margin:0 0 20px;font-size:12px;line-height:1.6;color:#888;">🔖图{n}：{caption}</p>'
    return html


def small(t):
    return f'<p style="margin:0 0 16px;font-size:12px;line-height:1.6;color:#888;">{t}</p>'






# ---------- 正文 ----------
def cap(t):
    return f'<p style="margin:0 0 20px;font-size:12px;line-height:1.6;color:#888;">🔖{t}</p>'


def pic(n, t):
    return img(n) + cap(t)


def tcap(t):
    return p(b(t), "margin:18px 0 6px;font-size:14px;")


def mk(t):
    """黄底高亮"""
    return f'<span style="background:#fff3a3;padding:0 2px;font-weight:bold;">{t}</span>'



A = []
A.append(img(1))
A.append(cap("原文信息（编者中文重排）"))

A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Gir de Carvalho RA, Pizzolato BB, Afonso de Souza GP, Minussi Filho E, Calixto GFL, Galdeano EA, Madureira MMS, Rodrigues WM, da Cunha MR, Machado EG, Cunha FB, Buchaim RL, Munhoz MAS. The Strengthening of Quadriceps, Abductors, and External Rotator Muscles of the Hip to Alter Axial Alignment of the Lower Limbs in University Students with Patellofemoral Pain Syndrome: A Prospective Cohort Study. J Funct Morphol Kinesiol. 2026;11(2):225. doi:10.3390/jfmk11020225",
    "中文题目：强化股四头肌、髋外展肌和外旋肌以改变髌股疼痛综合征大学生的下肢轴向力线：前瞻性队列研究",
    "作者单位：巴西容迪亚伊医学院（FMJ）研究生部、圣保罗大学包鲁牙科学院、圣保罗州立大学等",
    f"文章类型：{b('单组前后对照的干预研究')}（作者称“前瞻性队列”和“预试验”），{b('没有对照组')}，最终分析 10 人",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"{b('髌股疼痛综合征（PFPS）')}是膝前痛最常见的原因之一，年轻女性和运动人群尤其多见。"
    f"强化{b('股四头肌、髋外展肌和髋外旋肌')}是指南推荐的一线保守治疗，减痛、改善功能的证据已经比较充分。"
))
A.append(p(
    "大家常用的解释是：髋外展、外旋肌力量不足，股骨就容易内旋、膝外翻，髌骨被拉向外侧，髌股关节压力增大。"
    f"那么，练这些肌肉之后，下肢的{b('“力线”')}在影像上真的会变吗？以往研究大多看临床量角器测的 Q 角或者动态外翻，"
    f"作者想用 {b('CT')} 同时看四个指标：{mk('股骨颈前倾角、TT–TG 距离、胫骨外旋角和 3D-CT 上的 Q 角')}。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：向 481 名医学生招募，29 人符合条件入组；{b('19 人中途退出或被剔除')}（主动退出 7 人、缺课超过 10% 的 10 人、复查 CT 超过 7 天的 2 人），{b('最终分析 10 人')}（女 6、男 4）",
    f"{b('入选条件')}：18～24 岁；下蹲、上楼等日常活动中髌股疼痛 VAS ≥ 5 分；Clarke 征阳性；临床量角器测 Q 角男 > 15°、女 > 20°；{b('过去 12 个月没有规律运动')}",
    f"{b('测哪条腿')}：两侧疼痛相近时选外翻更明显的一侧；外翻相近时选更痛的一侧",
    f"{b('训练')}：{mk('每周 3 次、共 12 周、36 次')}，物理治疗师全程在场监督；每次先拉伸 5 分钟、跑步机快走 15 分钟（4～5 km/h）热身，再做 12 个动作，每个 3 组左右，按 1RM 设定负荷、逐步加量",
    f"{b('评估')}：训练前和训练结束 7 天内各做一次下肢 CT（层厚 1 mm），同一摆位；二维轴位像测股骨颈前倾角（FNA）、TT–TG、胫骨外旋角（TET），三维重建测 Q 角",
    f"{b('统计')}：Shapiro–Wilk 检验正态性，训练前后比较用“两相关样本的方差分析”（两个时间点，相当于配对 t 检验），P < 0.05",
]))

A.append(h2("重点：12 个动作怎么练"))
A.append(pic(2, "原文图 1（只有面板字母，原样引用；动作中文说明由编者添加）"))
A.append(tcap("原文表 1　股四头肌、髋外旋肌和髋外展肌训练方案（A～L 为训练顺序）"))
A.append(table(["动作", "收缩方式", "器材", "组数", "次数 / 时间", "负荷"], [
    ["A 靠墙髋外展", "等长", "墙", "4", "40 s", "自重"],
    ["B 伸膝", "等张", "伸膝器械", "3", "20 / 15 / 10", "60% / 70% / 70% 1RM"],
    ["C 髋外展", "等张", "髋外展器械", "3", "20 / 15 / 10", "60% / 70% / 70% 1RM"],
    ["D 深蹲＋髋外展、本体感觉控制", "等张", "弹力带", "3", "15", "1.3～1.7 kgf"],
    ["E 髋外展＋外旋（侧卧）", "等张", "弹力带", "3", "20 / 15 / 10", "0.7～1.0 / 1.3～1.7 / 2.0～2.6 kgf"],
    ["F 交替单腿臀桥", "等长", "无", "6", "30 s", "自重"],
    ["G 四点跪位髋外展＋外旋", "等张", "弹力带", "3", "20 / 15 / 10", "0.7～1.0 / 1.3～1.7 / 2.0～2.6 kgf"],
    ["H 髋外展（伸膝）", "等张", "踝部沙袋", "3", "15 / 15 / 15", "2～3 / 3～4 / 4～5 kg"],
    ["I 弹力带侧向行走", "等张", "弹力带", "3", "20 步", "0.7～1.0 / 1.3～1.7 / 2.0～2.6 kgf"],
    ["J 坐姿髋外旋", "等张", "拉力器低位滑轮", "3", "20 / 15 / 10", "60% / 70% / 70% 1RM"],
    ["K 臀桥＋髋外展本体感觉控制", "等长", "弹力带", "3", "40 s", "1.3～1.7 kgf"],
    ["L 髋外展＋外旋", "等张", "拉力器低位滑轮", "3", "20 / 15 / 10", "60% / 70% / 70% 1RM"],
], first_bold=False))
A.append(small("kgf：千克力；1RM：一次最大重复重量。原表中次数和负荷是分三行列出的（如 20 次 60% 1RM、15 次 70%、10 次 70%），"
               "原文没说清楚是同一次训练里逐组递增，还是 12 周里分阶段递增。多关节动作之间休息 2～3 分钟。编者翻译"))
A.append(p(
    f"整套方案以{b('髋外展和髋外旋')}为主（12 个动作里 10 个），股四头肌只有伸膝器械一个动作；"
    f"既有器械和弹力带的等张练习，也有靠墙外展、臀桥这样的{b('等长')}练习，基本覆盖了临床常用的髋部强化动作。"
))

A.append(h2("CT 上怎么测"))
A.append(img(3))
A.append(cap("四项影像指标说明（编者根据原文整理）"))
A.append(pic(4, "原文图 4（图中只有字母和数字，原样引用；说明由编者添加）"))

A.append(h2("结果"))
A.append(tcap("训练前后四项指标（均数 ± 标准差，n = 10）"))
A.append(table(["指标", "训练前", "训练后", "平均减少", "P 值"], [
    ["股骨颈前倾角（°）", "15.46 ± 6.46", "14.78 ± 8.29", "0.68 ± 1.26", "0.0626"],
    ["TT–TG（mm）", "13.44*", "11.93*", "1.51 ± 0.97", "0.0001"],
    ["胫骨外旋角（°）", "26.18 ± 6.46", "24.80 ± 4.12", "1.38 ± 3.36", "0.2231"],
    ["3D-CT Q 角（°）", "11.20*", "10.07*", "1.14 ± 1.52", "0.0091"],
]))
A.append(small("*正文没给标准差，数值读自原文图 8、图 10 的均值标注。编者根据原文正文和图 7～10 整理"))
A.append(pic(5, "原文图 7～10（图中英文由编者译为中文）"))
A.append(ul([
    f"{mk('TT–TG 平均减少 1.51 mm、Q 角平均减少 1.14°')}，差异有统计学意义",
    f"{b('股骨颈前倾角和胫骨外旋角')}也略有减小，但没有统计学意义",
    f"值得注意：这 10 个人训练前的 {b('TT–TG 最大只有 15.1 mm')}，全都在正常范围（< 20 mm）；3D-CT Q 角也只有 7.4°～17.4°。也就是说，这些人在 CT 上本来就没有明显的“力线异常”",
    "女性训练后 BMI 从 22.12 降到 21.98，男性从 27.2 降到 26.47",
]))

A.append(h2("作者怎么解读"))
A.append(ul([
    f"{b('TT–TG 不全是“骨头”')}：尸体研究显示股骨与胫骨之间每旋转 1°，TT–TG 约变化 0.5 mm。作者认为髋部控制变好、股骨过度内旋减少，可能是 TT–TG 变小的原因",
    f"Q 角和 TT–TG {b('同时下降')}，作者认为两者有共同机制：髋部动态稳定性提高、功能性外翻减少",
    f"{b('骨头没变是意料之中')}：股骨前倾和胫骨扭转在成年后基本稳定，36 次训练不可能改变骨性结构；但功能上的力线可以在骨头不变的情况下改善",
    "可能的机制是神经适应（运动单位募集、协调性改善）和静息肌张力增加，但本研究没有做肌电、肌肉形态等检查来验证",
    f"作者自己也说：{b('样本小、没有对照组')}，结论要谨慎，需要大样本随机对照试验确认；也分不清是练髋还是练股四头肌起的作用",
]))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{b('没有对照组')}：只有训练前后两次 CT，测量误差、摆位差异和“回归均值”都可能造成 1～2 mm、1～2° 的变化，无法和训练效果区分开",
    f"{b('变化量很小，测量可靠性没报告')}：TT–TG 1.5 mm、Q 角 1.1° 已经接近 CT 手工画线的误差范围；原文没报告测量者内、测量者间信度，也没说测量者是否知道片子是训练前还是训练后的",
    f"{b('静态仰卧 CT 测“功能性力线”')}：作者用“股骨内旋减少、动态外翻改善”来解释，但 CT 是仰卧、非负重、用泡沫垫固定的，测不到动态控制；更可能反映的是扫描时下肢的摆位（旋转）差异",
    f"{b('脱落率 66%')}：29 人入组只分析了 10 人，只分析了坚持下来的人，结果可能偏乐观",
    f"{b('没有疼痛和功能结局')}：入组时测了 VAS，结果里却没有报告训练后疼痛和功能变化，看不出 CT 上的变化有没有临床意义",
    f"{b('人群特殊')}：久坐的医学生（排除了过去一年有规律运动的人），CT 上力线基本正常，结论不能推广到运动员或真正有结构性力线异常（如 TT–TG ≥ 20 mm）的患者",
    f"{b('为了研究让年轻人多做一次 CT')}：每人做两次下肢 CT，这对单组预试验来说辐射代价不小",
    "优点：训练方案写得很具体（12 个动作配照片、组数、负荷），物理治疗师全程监督；同一台 CT、同一摆位方案；CT 测量方法配图交代清楚",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('股骨颈前倾角的标准差不可能成立')}：训练前 SD 6.46°、训练后 8.29°，而差值的 SD 只有 1.26°。按配对数据换算，前后相关系数要大于 1 才可能，数学上不成立，至少有一个数字写错了",
    f"{b('股骨颈前倾角的 P 值对不上')}：用文中给的差值 0.68 ± 1.26°、n = 10 算配对 t 检验，t ≈ 1.71，双侧 P ≈ 0.12；文中的 0.0626 恰好接近单侧 P 值。而胫骨外旋角用同样方法算出双侧 P ≈ 0.226，和文中 0.2231 吻合，说明两个指标的 P 值算法不一致",
    f"{b('Q 角和 TT–TG 的 P 值偏小')}：Q 角 1.14 ± 1.52°、n = 10，算出来 P ≈ 0.042，文中写 0.0091；TT–TG 1.51 ± 0.97 mm 算出 P ≈ 0.0008，文中写 0.0001。结论（有显著性）不变，但显著程度被写大了",
    f"{b('两个指标的 SD 完全相同')}：胫骨外旋角训练前 SD 6.46° 与股骨颈前倾角训练前 SD 6.46° 一模一样，可能是抄录错误",
    f"{b('统计方法前后说法不同')}：摘要写“重复测量方差分析”，方法写“两相关样本的方差分析”；只有两个时间点时这其实就是配对 t 检验，但摘要的写法容易让人以为有多次测量",
    f"{b('入选的 Q 角和 CT 上的 Q 角对不上')}：入选要求临床 Q 角男 > 15°、女 > 20°，但 3D-CT 上 Q 角最大只有 17.4°、平均 11.2°。原因是 CT 上从股骨大转子起画线，而引言定义的 Q 角从髂前上棘起画线，两者不是一回事，原文没有说明",
    f"{b("“三维 CT”说法夸大")}：讨论称 TT–TG 和 Q 角的变化“只有用高精度三维 CT 才能测出”，但按方法部分，TT–TG 是在二维轴位像上测的，只有 Q 角用了三维重建",
    f"{b('引用错位')}：讨论 4.2 节说 TT–TG 增大与伸膝装置外偏、髌骨不稳相关，引用的文献 [36] 却是 ACSM 抗阻训练进阶的立场声明，应该是 [37]（Dejour 1994）",
    f"{b('研究设计名称混用')}：标题叫“前瞻性队列研究”，正文又叫“前瞻性干预性队列”和“预试验”；实际是没有对照组的单组前后对照。“缺少对照组”在讨论第二段提到了，却没写进局限性一节",
    f"{b('该报告的没报告')}：方法说收集了年龄、VAS，但结果里没有年龄和训练后疼痛；伦理批准是 2020 年 2 月，没写研究实际进行的时间，也没有试验注册号",
    f"{b('表 1 次数和负荷含义不清')}：同一动作列了 20 / 15 / 10 次和 60% / 70% / 70% 1RM 三行，没说是组内递增还是分阶段递增；按常规，70% 1RM 一般只能做 10～12 次左右，做 15 次偏重",
    f"{b('小笔误')}：图 4 图注写“胫骨结节内侧顶点”（apex of the medial tibial tubercle），胫骨结节并没有“内侧顶点”；图 1 图注 “resistence” 拼错",
]))

A.append(h2("落到临床"))
A.append(img(6))
A.append(cap("临床要点（编者整理）"))
A.append(ul([
    f"{mk('训练方案可以直接参考')}：12 周、每周 3 次、以髋外展和外旋为主、配合股四头肌，监督下进行；表 1 的 12 个动作从等长、器械到弹力带和功能性动作，适合作为髌股疼痛的强化模板",
    f"{b('别把“力线矫正”当卖点')}：TT–TG 1.5 mm、Q 角 1°的变化没有对照组、也没有和疼痛改善挂钩，不能据此告诉患者“练肌肉能把骨头的排列练正”；股骨前倾和胫骨扭转确实没变",
    f"{b('评估疗效看疼痛和功能')}：临床上仍应以疼痛（VAS/NRS）、功能问卷（如 AKPS/Kujala）和动态控制（单腿下蹲时的膝外翻）作为主要结局",
    "如果患者确实有结构性力线异常（TT–TG ≥ 20 mm、股骨前倾或胫骨扭转明显增大），保守训练仍可先做，但要知道它改变不了骨性结构，症状顽固时需要转诊评估",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Gir de Carvalho RA, Pizzolato BB, Afonso de Souza GP, et al. The Strengthening of Quadriceps, Abductors, and External Rotator Muscles of the Hip to Alter Axial Alignment of the Lower Limbs in University Students with Patellofemoral Pain Syndrome: A Prospective Cohort Study. J Funct Morphol Kinesiol. 2026;11(2):225. doi:10.3390/jfmk11020225</em><br>"
    "原文以 CC BY 4.0 协议开放获取（© 2026 by the authors，MDPI 出版）。本文为学术交流中文解读：原文图 1、图 4 原样引用；原文图 7～10 中的英文由编者译为中文并拼成一张图；表格为编者中文翻译；"
    "首图、指标说明卡和临床要点卡为编者根据原文整理；文中重新计算的 P 值为编者根据原文给出的均数和标准差推算。仅供学习交流，如有侵权请联系删除。"
))

def inline_imgs(html):
    """预览页里的图片改成 base64 内嵌：单个 preview.html 拿到哪里打开都能看到图。"""
    import base64
    import re
    mime = {".png": "image/png", ".gif": "image/gif"}

    def rep(m):
        f = HERE / m.group(1)
        return f'src="data:{mime.get(f.suffix, "image/jpeg")};base64,{base64.b64encode(f.read_bytes()).decode()}"'
    return re.sub(r'src="((?:images|gifs)/[^"]+)"', rep, html)


TITLE = "「髌股疼痛」练 12 周髋外展、外旋和股四头肌，CT 上 TT–TG 少了 1.5 mm：这算“矫正力线”吗？"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>髌股疼痛肌力强化推文</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
  :root { --ground:#ececec; --paper:#ffffff; color-scheme:light; }
  body { background:var(--ground); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
         padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:16px 32px; }
  .paper { max-width:640px; margin:0 auto; background:var(--paper); padding:20px 16px 28px; box-sizing:border-box; }
  .paper h1 { font-size:22px; line-height:1.4; margin:0 0 8px; color:#111; text-wrap:balance; }
  .paper .by { font-size:14px; color:#576b95; margin-bottom:20px; }
  .paper img { max-width:100%; }
  .paper table { display:block; overflow-x:auto; }
</style>
<div class="paper">
<h1>""" + TITLE + """</h1>
<div class="by">原创 · 骨科康复小黄</div>
""" + inline_imgs(BODY) + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
