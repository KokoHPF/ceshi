#!/usr/bin/env python3
"""Barassi 等 2026《温泉疗法与关键肌筋膜触发点手法治疗合并 COPD 的肌筋膜痛：病例系列》（Healthcare）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
配图：python3 tools/make_figs.py src images <中文字体>
（原文是 CC BY 4.0，允许演绎和商业使用；原文图 1～7 是治疗照片，图内只有分图字母，原样引用，中文说明放图外）
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
                'vertical-align:middle;">', 'vertical-align:middle;white-space:nowrap;">' if i == 0 and len(c) <= 7 else 'vertical-align:middle;">', 1)
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
    "Barassi G, Panunzio M, Prosperi L, Marinucci C, Moccia A, Fratta DP, Cristinziano F, Della Rovere MP, Gallenga PE. "
    "Balneotherapy and manual therapy of key myofascial trigger points as therapeutic integration for COPD associated with "
    "myofascial pain syndrome: a case series. Healthcare. 2026;14(6):788. doi:10.3390/healthcare14060788",
    "中文题目：温泉疗法与关键肌筋膜触发点手法治疗合并 COPD 的肌筋膜疼痛综合征：病例系列",
    "作者单位：意大利基耶蒂-佩斯卡拉大学 Ce.Fi.R.R. 物理治疗与康复中心；卡斯泰尔诺沃德拉道尼亚温泉医学中心",
    f"研究类型：{b('回顾性病例系列（10 例），无对照组')}",
], square=True))

A.append(h2("先说为什么要读这篇"))
A.append(p(
    f"慢阻肺（COPD）患者除了喘，还常常{b('脖子、胸背、腰疼')}。呼吸费力时斜角肌、胸小肌、肩胛提肌、上斜方肌这些辅助呼吸肌长期加班，"
    f"再加上驼背、含胸，很容易长出{b('肌筋膜触发点')}，变成肌筋膜疼痛综合征（MPS）。原文引用的综述也说，COPD 患者的肌肉骨骼疼痛常集中在颈椎、腰椎、胸廓和膈肌周围。"
))
A.append(p(
    "意大利有用温泉治疗呼吸病和肌肉骨骼病的传统，但温泉研究的方案五花八门，很少写清楚到底做了什么。"
    f"这篇来自意大利一家温泉医学中心，把{b('喝温泉水、吸温泉蒸汽、泥疗、冷热池行走、温泉池水中训练')}串成一套固定流程，"
    f"每一站都插入{b('关键触发点手法')}，叫 BPM-ITC。10 名 COPD 合并 MPS 的患者做了 4 周 20 次，呼吸困难、疼痛和整体健康问卷都有下降。"
))
A.append(p(
    f"值得看的是它把方案写得很细：哪个温度、多少分钟、按哪些肌肉、怎么配合呼吸。但它只有 10 例、回顾性、没有对照，"
    f"{mk('结果只能说明“做完之后变好了”，说明不了“是因为做了才变好”')}，后面会说清楚。"
))

A.append(h2("研究对象：10 名 COPD 合并肌筋膜痛患者"))
A.append(img(2))
A.append(ul([
    f"{b('来源')}：2025 年 5～6 月到卡斯泰尔诺沃德拉道尼亚温泉医学中心就诊的患者，连续纳入",
    f"{b('诊断')}：COPD 是在外院确诊的，原文写的是“中重度”，但{b('没给肺功能数值或 GOLD 分级')}；合并 MPS 由中心的风湿科和康复科医生根据“有触发点的局部痛和放射痛”判断",
    f"{b('排除')}：心衰或肾衰、重度高血压、重度血栓性静脉炎、风湿病急性期、免疫缺陷、开放伤口和溃疡、精神疾病、步行严重受限、活动性感染（这是中心的常规禁忌）",
    f"{b('一般情况')}：男 4、女 6，平均 69±7 岁；都不吸烟；除 3、6、7 号偶尔活动（每周不到 2 次），都没有规律运动；各自的药物治疗全程不变",
]))
A.append(tcap("表 1　患者基本情况（编者根据原文表 1 翻译）"))
A.append(table(["编号", "年龄/性别", "BMI", "合并症", "NPRS", "MRC", "BPQ"], [
    ["1", "78/男", "29.4", "颈椎+腰椎管狭窄", "10", "3", "52"],
    ["2", "61/男", "29.0", "多关节炎；多发性神经病", "10", "3", "80"],
    ["3", "59/女", "25.3", "骨关节炎", "8", "2", "42"],
    ["4", "68/女", "23.6", "双髋关节炎；慢性静脉功能不全；乳腺象限切除术后", "9", "2", "44"],
    ["5", "75/女", "25.8", "重度多关节炎", "9.5", "3", "41"],
    ["6", "72/女", "27.3", "骨质疏松；纤维肌痛；颈痛；双膝痛；慢性静脉功能不全", "8.5", "2", "48"],
    ["7", "76/女", "24.7", "腰痛；上背痛；脊柱关节炎；代谢综合征；慢性静脉功能不全", "6.5", "2", "30"],
    ["8", "76/女", "27.5", "腰痛；轻度脊柱病；腰椎管狭窄；轻度高血压", "6", "3", "20"],
    ["9", "64/男", "30.1", "双侧坐骨神经痛；肥胖", "6.5", "2", "27"],
    ["10", "63/男", "33.8", "脑卒中后；轻度高血压；多关节炎；甲减；肥胖", "10", "2", "40"],
]))
A.append(small("身高、体重两列略去。BMI 单位 kg/m²；NPRS、MRC、BPQ 为治疗前分数。"))
A.append(p(f"注意合并症这一栏：{b('椎管狭窄、多关节炎、纤维肌痛、坐骨神经痛')}都会引起疼痛，所以这些人的“疼”不全是肌筋膜来源。"))

A.append(h2("具体怎么做"))
A.append(img(3))
A.append(h4("先找关键触发点"))
A.append(ul([
    f"每次治疗开始，由负责治疗的温泉治疗师花{b('约 5 分钟')}，在{b('站立、仰卧、俯卧')}三个体位依次看、摸、查主动活动度",
    f"关键触发点（KMTrP）的判断：{b('摸得到压痛结节 + 活动度受限 + 看得出的体位不对称')}",
    "双侧都查：胸大肌、腹直肌、股直肌、大收肌、胫骨前肌、拇收肌、足底方肌、小趾展肌；颈夹肌、上下斜方肌、胸最长肌、腰方肌、臀大肌、腓肠肌、比目鱼肌、腘绳肌",
    f"每次挑出{b('约 3 个')}关键点重点处理，后面每一站都回到这几个点上",
]))
A.append(h4("① 饮用温泉水"))
A.append(p("空腹 ≥6 小时后，喝约 500 mL 碳酸氢盐-硫酸盐-碱土金属矿泉水。患者拿着写了名字的小瓶，边做后面的治疗边喝。"))
A.append(h4("② 温泉蒸汽吸入 20 分钟（含手法）"))
A.append(img(4))
A.append(ul([
    "坐位，喷嘴距患者 50 cm，37～38 ℃ 的均匀水雾，1.5 个大气压",
    f"{b('前 10 分钟')}：治疗师站在身后，按压关键触发点和呼吸相关肌（{b('膈肌、胸小肌、肩胛提肌、星状神经节区')}），每点 {b('30 秒～1 分钟')}，可加辅助静态牵伸",
    f"{b('后 10 分钟')}：双手与肩同宽握木棒或塑料棒前屈上举，{b('深吸 4 秒、用力呼 4 秒')}，做 1 分钟、歇 1 分钟",
]))
A.append(h4("③ 泥疗 + 水疗浴 + 休息 50 分钟（含手法）"))
A.append(img(5))
A.append(ul([
    "仰卧，成熟的膨润土温泉泥敷在肩、肘、腕、脊柱、髋、膝、踝等大关节和关键触发点上，15 分钟",
    "接着在单人浴缸里泡温泉水加臭氧水疗喷射 15 分钟",
    f"再在温暖的房间休息 20 分钟，{b('前 10 分钟再按一遍触发点')}；为了卫生，可以用金属和木头做的 T 形按摩棒隔着泥按",
]))
A.append(h4("④ 臭氧“血管通道”行走 15 分钟"))
A.append(img(6))
A.append(p(f"在 {b('24 ℃ 和 38 ℃')} 两个池子之间来回走，{b('每分钟换一次')}，池壁有 4～6 个大气压的臭氧水柱冲击，用来促进下肢静脉和淋巴回流、给本体感觉刺激。边走边做不拿棒的上肢上举。"))
A.append(h4("⑤ 32.5 ℃ 温泉池水中再训练 60 分钟"))
A.append(p("分 4 段，每段 15 分钟，由治疗师带着做："))
A.append(img(7))
A.append(img(8))
A.append(img(9))
A.append(img(10))
A.append(ul([
    f"{b('适应和放松')}：浮条托住脊柱漂浮，配合膈式呼吸；钟摆运动；配合呼吸节律步行；持棒上举",
    f"{b('肌筋膜刺激')}：患者漂浮时，治疗师按压或捏压关键触发点，并被动活动脊柱和四肢",
    f"{b('关节活动和本体感觉')}：扶杆屈伸下肢；浮条辅助的动态自我牵伸；站在平衡板上做双侧踝背屈",
    f"{b('主动稳定')}：浮条辅助蹬车；手扶浮板侧向游泳",
]))
A.append(p(
    f"整套 {b('每周 5 次，连续 4 周，共 20 次')}，每个人都做完整套，只根据运动能力微调水中动作。"
    f"把各站时长加起来，{b('一次约 2.5 小时')}（编者计算）。原文{b('没写')}手法的力度、每个水中动作做几组几次、20 次里怎么进阶。"
))

A.append(h2("怎么评估"))
A.append(ul([
    f"{b('MRC 呼吸困难量表')}：0～4 级，0 级只在剧烈活动时喘，4 级休息时也喘；≥2 级提示需要重点关注。（0～4 级这个版本通常叫改良 MRC，即 mMRC——编者注）",
    f"{b('NPRS 疼痛数字评分')}：0～10 分，让患者报告肌肉骨骼{b('最痛那个部位')}的最高疼痛",
    f"{b('生物-姿势问卷（BPQ）')}：57 题自填问卷，覆盖肌肉骨骼、内脏、感知觉、心理情绪和生活方式，每题 0～2 分，总分 0～112，越高越差",
    "治疗前（T0）、20 次结束后（T1）各评一次，由中心的康复科或风湿科医生记录，不是做治疗的温泉治疗师",
    "统计：Wilcoxon 符号秩检验，并计算效应量 r 和四分位距",
]))

A.append(h2("结果：10 个人三项都下降"))
A.append(img(11))
A.append(tcap("表 2　治疗前后各项指标（编者根据原文表 2 翻译）"))
A.append(table(["编号", "MRC<br>前→后", "NPRS<br>前→后", "BPQ<br>前→后"], [
    ["1", "3 → 2", "10 → 6", "52 → 38"],
    ["2", "3 → 2", "10 → 5", "80 → 33"],
    ["3", "2 → 1", "8 → 5", "42 → 19"],
    ["4", "2 → 1", "9 → 6", "44 → 29"],
    ["5", "3 → 2", "9.5 → 8", "41 → 39"],
    ["6", "2 → 1", "8.5 → 5", "48 → 42"],
    ["7", "2 → 1", "6.5 → 4.5", "30 → 12"],
    ["8", "3 → 2", "6 → 3", "20 → 11"],
    ["9", "2 → 1", "6.5 → 6", "27 → 8"],
    ["10", "2 → 1", "10 → 6", "40 → 26"],
    ["均值", "2.4 → 1.4", "8.4 → 5.4", "42.4 → 25.7"],
    ["中位数", "2 → 1", "8.7 → 5.5", "41.5 → 27.5"],
    ["p 值", "<0.01", "<0.01", "<0.01"],
    ["效应量 r", "−0.98", "−0.87", "−0.87"],
]))
A.append(ul([
    f"{b('呼吸困难')}：{b('10 个人 MRC 都正好降 1 级')}，平均降约 42%。作者认为 1 级达到了最小临床重要差异",
    f"{b('疼痛')}：平均从 8.4 降到 5.4（约 35%），{b('8 人降了 ≥2 分')}。1、2、10 号（男性、BMI ≥29、治疗前疼痛 10 分）降得最多（4～5 分）；9 号只降 0.5 分，5 号降 1.5 分",
    f"{b('BPQ')}：平均从 42.4 降到 25.7（约 39%），但个人差别很大，2 号降了 47 分，5 号只降 2 分；5 号是合并“重度多关节炎”的那位",
    f"{b('依从性和安全')}：所有人都做完了 20 次，{b('没有报告不良事件')}",
]))
A.append(p(f"BPQ 治疗后的四分位距反而从 18 变成 26，说明大家改善的幅度分散了；NPRS 的四分位距从 3.5 变成 1，作者解读为疼痛都向“中度”（4～6 分）收拢。"))

A.append(h2("作者在讨论里怎么说"))
A.append(ul([
    f"{b('为什么可能有效')}：作者推测是温泉水的“机械 + 理化代谢”刺激和手法协同。触发点被看作身体和内脏症状在脊髓后角汇聚的“入口”；"
    f"温泉水、硫化氢、膨润土泥有抗炎、抗氧化作用；水的浮力、静水压、温度、阻力有利于运动和呼吸训练。"
    f"但作者也承认{b('这些都没测')}（没抽血、没做生化），只能“合理推测”",
    f"{b('呼吸困难')}：COPD 患者病情稳定时呼吸困难一般会随时间逐渐加重，所以 10 人都降 1 级，作者认为方案“可能延缓了短期的症状下滑”，但没有对照组，要谨慎",
    f"{b('谁效果好')}：作者觉得性别、BMI、合并症严重程度可能影响疗效，需要更大样本分层分析",
    f"{b('局限')}：例数少且杂、单中心、没有对照（假治疗或标准治疗）、没有长期随访、只用了主观量表；建议以后加肺功能、压痛阈、肌肉力学特性和生化指标，并和标准 COPD 治疗比较",
]))
A.append(quote(
    "the amount of data available is not sufficient to exclude the influence of placebo or Hawthorne effects or variations caused by the natural clinical history of the patients.",
    "现有数据不足以排除安慰剂效应、霍桑效应或患者病程自然变化的影响。"
))

A.append(h2("这篇能信几分"))
A.append(ul([
    f"{b('10 例、回顾性、没有对照、没有随访')}：只能说明“做完 4 周后量表分数低了”。安慰剂效应、霍桑效应、“到温泉中心度假”本身带来的放松、均值回归（3 个人治疗前疼痛就是满分 10 分）都可能解释一部分",
    f"{b('结局全是主观自评')}：MRC、NPRS、BPQ 都是患者自己填的，患者知道自己在做什么治疗，期望很高。作者说“自填量表减少了评估者偏倚”，但恰恰最容易受患者期望影响（编者观点）",
    f"{b('MRC 10 人全部正好降 1 级')}：这个量表只有 5 级，太粗；而且没有测肺功能、血氧、6 分钟步行、CAT 这些 COPD 常用指标，无法判断呼吸功能真的变了",
    f"{b('“中重度 COPD”没有依据')}：没给 FEV1、GOLD 分级、吸入药物，也不知道有没有人在同期做常规肺康复",
    f"{b('MPS 的诊断和疼痛来源不清')}：多人合并椎管狭窄、多关节炎、纤维肌痛、坐骨神经痛；NPRS 记的是“最痛部位”，每个人、前后两次可能不是同一个地方",
    f"{b('BPQ 没有出处')}：原文没给这个问卷的信效度研究，也没有最小临床重要差异，很难判断降 17 分算多少",
    f"{b('方案是“全家桶”')}：喝水、吸入、泥疗、冷热池、水中训练、手法一起上，一次约 2.5 小时，即使有效也分不清是哪一样起作用，更说明不了“温泉水成分”的作用",
    f"{b('利益相关')}：作者团队来自开展该方案的温泉中心，BPM-ITC 也是他们自己命名推广的方案；作者声明无利益冲突。研究没有经过伦理委员会审批，按当地规定以 ISO 9001 认证代替",
    "优点：方案写得非常具体，温度、时长、压力、体位都有，便于别人重复；每个患者的数据都给了；作者对局限说得也比较坦白",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('5 号的性别')}：表 1 写的是女性，结果部分却用“his comorbidities（他的合并症）”",
    f"{b('MRC 量表')}：写的是 MRC，但描述的是 0～4 级的版本，这通常叫{b('改良 MRC（mMRC）')}；原版 MRC 是 1～5 级",
    f"{b('NPRS')}：原文说它“源自十级视觉模拟评分”，NPRS 是 0～10 共 11 级；而且它通常只取整数，表里却有 9.5、8.5、6.5、4.5",
    f"{b('MRC 降幅')}：原文写平均下降 41.6%；按均值算是 (2.4−1.4)/2.4 ≈ 41.7%，按每人降幅平均是 43.3%，都对不上 41.6%（差别很小）",
    f"{b('NPRS 治疗后均值')}：10 人加起来 54.5，均值 5.45，表里写 5.4",
    f"{b('笔误')}：统计方法里“pre-post interference statistical analysis”应为 inference（推断）",
    f"{b('机制讨论')}：大段在讲含硫温泉水和硫化氢，但本中心用的是碳酸氢盐-硫酸盐-碱土金属水，作者只能说“推测和含硫水相似”",
]))

A.append(h2("落到临床"))
A.append(img(12))
A.append(cap("临床要点（编者整理）"))
A.append(ul([
    f"{mk('COPD 患者疼痛别忽略')}：查体时顺手摸摸斜角肌、胸小肌、肩胛提肌、上斜方肌、胸大肌，有触发点就一起处理（斜角肌为编者补充）",
    f"{b('没有温泉也能借用')}：坐位按压呼吸辅助肌触发点每点 30 秒～1 分钟；持棒上举配合“吸 4 秒、呼 4 秒”，做 1 分钟歇 1 分钟；有温水池的话，漂浮呼吸、扶杆下肢训练、浮条辅助牵伸都可以加",
    f"{b('不能替代肺康复')}：标准肺康复（耐力训练、力量训练、教育）证据充分，这个方案没和它比过，温泉和手法顶多算锦上添花",
    f"{b('安全先筛查')}：COPD 患者泡热水、走 38 ℃ 池、吸蒸汽前，要看血氧、心率、血压；有低氧、近期急性加重或心功能问题的先别下水（编者补充）",
    f"{b('评估别只看量表')}：同时记录肺功能、6 分钟步行、mMRC/CAT、压痛阈，并随访治疗结束后能维持多久",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Barassi G, Panunzio M, Prosperi L, Marinucci C, Moccia A, Fratta DP, Cristinziano F, Della Rovere MP, Gallenga PE. "
    "Balneotherapy and manual therapy of key myofascial trigger points as therapeutic integration for COPD associated with myofascial pain syndrome: "
    "a case series. Healthcare. 2026;14(6):788. doi:10.3390/healthcare14060788</em><br>"
    "原文 © 2026 by the authors，Licensee MDPI，以知识共享署名 4.0 协议（CC BY 4.0）开放获取。"
    "本文为中文解读：原文图 1～7 原样引用（图内只有分图字母，未作改动），中文说明为图外图注；表格为编者翻译（表 1 略去身高、体重两列）；"
    "首图、研究概况卡、治疗流程图、治疗前后对比图（按原文表 2 重画）、临床要点卡和封面为编者根据原文整理绘制。版权归原作者所有，如有侵权请联系删除。"
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


TITLE = "慢阻肺合并肌筋膜痛，泡温泉加按触发点，4 周能少喘少疼吗？（10 例病例系列）"

BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>COPD 肌筋膜痛温泉推文</title>
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
