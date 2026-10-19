#!/usr/bin/env python3
"""跟腱病保守治疗推文：生成 article_body.html 与 preview.html。

用法：python3 build.py   → 生成 article_body.html（上传用正文）和 preview.html（在线预览）
样式全部内联；列表用“•”段落而不是 <ul>，避免公众号编辑器把列表拆乱。
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




def phase_card(name, when, rows):
    cell = "border:1px solid #d9d9d9;padding:6px 7px;font-size:13px;line-height:1.6;"
    trs = (f'<tr><td colspan="2" style="{cell}background-color:#f2f2f2;color:#000;font-weight:bold;font-size:14px;">'
           f'{name}<span style="font-weight:normal;color:#666;">　{when}</span></td></tr>')
    for k, v in rows:
        v = "<br>".join(f"• {x}" for x in v) if isinstance(v, list) else v
        trs += (f'<tr><td style="{cell}width:22%;color:{BLUE};font-weight:bold;white-space:nowrap;vertical-align:top;">{k}</td>'
                f'<td style="{cell}color:{TEXT};">{v}</td></tr>')
    return f'<table style="width:100%;border-collapse:collapse;margin:0 0 14px;"><tbody>{trs}</tbody></table>'




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
    "Silbernagel KG, Hanlon S, Sprague A. Current clinical concepts: conservative management of Achilles tendinopathy. J Athl Train. 2020;55(5):438-447.",
    "作者来自美国特拉华大学物理治疗系；第一作者是“疼痛监测模型”的提出者",
    "临床述评，推荐强度按 SORT 分级（A 一致高质量证据、B 证据有限或不一致、C 共识或专家意见）",
], square=True))

A.append(h2("先说跟腱病为什么难缠"))
A.append(ul([
    f"很常见：精英田径运动员 {b('43%')} 有过跟腱症状，中长跑高达 {b('83%')}；但全科门诊里 65% 和运动无关",
    f"{b('60%～80%')} 的运动员发病前训练量或强度突然增加（训练负荷失误）",
    f"恢复常要{b('一年以上')}，再伤率 {b('27%～44%')}；症状好了不代表功能和结构恢复了",
    "分型：中段型 55%～65%、止点型 20%～25%、近端肌腱肌腹交界 9%～25%；约 30% 双侧",
    "“肌腱炎”这个叫法不建议再用——病理上主要是退变或愈合失败，不一定有炎症",
    "可干预的风险因素：跖屈力量弱、髋神经肌肉控制差、踝背伸和距下活动异常、足过度旋前、体重大；氟喹诺酮类抗生素（约用药 8 天后）也和跟腱病、断裂有关",
]))

A.append(h2("怎么诊断"))
A.append(ul([
    f"典型症状：{b('晨起或久坐后僵硬')}、按压痛、跑跳时痛、成绩下降；早期常是“刚开始运动痛，热身后消失”；不受力时往往不痛",
    f"中段型：跟骨附着点上方 {b('2～6 厘米')}按压痛（敏感度 84%、特异度 73%）+ 自述该处疼痛（78%、77%）",
    f"{b('弧形征')}：捏住增厚结节，主动勾脚、踩脚时结节跟着移动为阳性（敏感度 25%、特异度 100%）",
    f"{b('皇家伦敦医院试验')}：休息位捏到最痛点，主动背伸后再捏同一点，疼痛减轻为阳性（51%、93%）",
    "鉴别：急性跟腱断裂、后踝撞击、三角骨综合征、副比目鱼肌、腓肠神经激惹、脂肪垫激惹、全身性炎症疾病",
]))
A.append(pic(2, "原文图 1"))

A.append(h2("评估：不只看痛"))
A.append(p(f"作者主张从{mk('四个维度')}评估“肌腱健康”，回场前每个维度都要恢复，否则容易复发。"))
A.append(pic(3, "四维度"))
A.append(ul([
    f"{b('症状')}：按压痛和单腿跳痛（0～10）；维多利亚运动研究所跟腱问卷（0～100，变化 10 分以上算有意义）；足踝结局评分、足踝能力量表",
    f"{b('功能')}：负重弓步测背伸（最小可测变化 3.88）；{b('提踵耐力测试')}（伸膝、每分钟 30 次、做到力竭，记次数、高度、总做功，算两侧对称指数）；等长或等速跖屈力量；单腿连续跳（腾空/触地时间比）、单腿落地反跳",
    f"{b('结构')}：超声测肌腱厚度，和健侧或同侧正常段比较；剪切波弹性成像测力学特性",
    f"{b('心理')}：坦帕运动恐惧量表（17 题，0～68）",
]))
A.append(pic(4, "原文图 3、4"))

A.append(h2("重点：怎么练"))
A.append(p(
    f"{b('运动是证据最强的治疗（A 级）')}。离心、慢速向心 + 离心都有效；等长收缩被说成“更好的起步”，但对跟腱病没有证据支持它比其他方式好。"
    f"肌腱对{mk('更大负荷、更长时间')}反应更好；后期还要练速度（快速也会加大肌腱负荷）。"
))
A.append(h3("疼痛监测模型：用疼痛决定练多少"))
A.append(pic(5, "疼痛监测模型"))
A.append(ul([
    "不需要完全休息——完全卸载反而不利于恢复",
    f"训练中、训练后、{b('第二天早上')}疼痛都不超过 5 分；疼痛和僵硬不能一周比一周重",
    "维持心肺可以用深水跑、骑车这类跟腱负荷小的运动",
    "让运动员记训练日记：做了什么、其他活动、早上和运动时的疼痛评分",
    "和运动员、教练、队医等所有人讲清楚负荷管理",
]))
A.append(h3("四期负荷方案"))
A.append(pic(6, "四期方案"))
A.append(pic(7, "原文图 6"))
A.append(ul([
    f"{b('第 1 期（1～2 周）')}：先在平地上把提踵的向心、离心都控制好；做不了提踵就从等长或弹力带开始",
    f"{b('第 2 期（2～5 周）')}：中段型改到台阶边做（加大活动范围），加快速回弹提踵，为增强式训练做准备；减重跑台或深水跑开始恢复跑步；同时处理踝、足内在肌、髋膝力量等其他问题",
    f"{b('第 3 期（3～12 周）')}：加外部负荷——负重背心、背包、腿举机或史密斯机；在家通常从 {b('10 磅（4.5 千克）')}开始，3 × 15 轻松完成就加重；也可以每周 3 次在健身房做重的、在家每天做轻的；增强式先双腿后单腿",
    f"{b('提醒运动员')}：力量和耐力恢复了也要继续做提踵，肌腱还在恢复",
    f"{b('止点型')}：全程在平地做，必要时脚跟下垫 1.3～2.5 厘米木板，避免背伸时肌腱被跟骨挤压",
]))
A.append(p(
    f"{b('开始跑跳前')}：日常走路疼痛 {mk('≤1～2 分')}；单腿跳 20 次疼痛超过 2 分的人，很难在疼痛监测范围内开始跑步。"
))

A.append(h2("重点：回场怎么排"))
A.append(p(
    f"肌腱从重负荷中恢复需要 {b('36～72 小时')}，轻活动可以更频繁。作者把运动员要做的每项活动，按疼痛和“自觉跟腱用力”分成轻、中、重三级："
))
A.append(pic(8, "活动分级"))
A.append(ul([
    f"{b('轻')}：可以每天做；{b('中')}：之后要 2 个恢复日；{b('重')}：之后要 3 个恢复日",
    "分级由治疗师、运动员、教练一起定；一次排约 3 周的计划",
    "每 3～4 周重新分级，加入新的“重”活动，逐步回到全量训练和比赛",
    "运动员每天在日记里记疼痛、症状和每次活动后的跟腱用力评分",
]))
A.append(pic(9, "排程示例"))
A.append(p(f"回场前要确认：症状恢复 + {b('提踵耐力和跳跃测试')}恢复，最好有两侧对称或伤前数据对比。"))

A.append(h2("其他治疗怎么看"))
A.append(table(["治疗", "原文评价", "推荐强度"], [
    ["运动", "证据最强；离心或慢速向心 + 离心都有效；每周至少 2 次", "A"],
    ["矫形鞋垫", "无法给出推荐；定制和成品没差别；可能减少跟腱应变，但不减痛", "B"],
    ["低能量激光", "证据矛盾，可作为运动的辅助", "B"],
    ["贴扎", "可能改变足姿、减少应变，减痛证据有限", "C"],
    ["离子导入", "对急性中段型可减轻疼痛和症状", "B"],
    ["器械辅助软组织松动", "踝活动度受限时有效", "C"],
    ["体外冲击波", "短期减痛、促进愈合；和离心训练合用优于单纯离心；个体差异大", "B"],
    ["注射", red("没有证据支持") + "单独使用或配合运动", "A"]]))
A.append(p("作者强调：负荷训练才是核心，手术等侵入性治疗只在规范康复失败后才考虑。"))

A.append(h2("怎么预防"))
A.append(ul([
    f"{mk('最好的预防是别忽视早期“小”症状')}：疼痛出现前，往往已经有几周到几个月的晨僵和轻微痛，甚至跑步变慢、跳得不高",
    "监控训练负荷，避免突然加量；定期测试表现，发现下滑及时调整",
    "超声上的结构改变可以先于症状，但不代表一定会发病，要结合负荷和表现判断",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    "这是临床述评，四期方案和回场排程主要来自作者团队自己的研究和经验",
    "推荐强度是作者按 SORT 自评的，部分评级值得商榷（如运动恐惧量表评 C，注射“没有证据支持”评 A）",
    "回场排程（轻、中、重分级和恢复天数）还没有前瞻性研究验证",
]))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    f"{red('表格编号对错位')}：正文说“表 2”是治疗汇总、“表 3”是分期方案、“表 4”是活动分级，实际表 2 是分期方案、表 3 是活动分级、表 4 是治疗汇总",
    "参考文献引错：分期方案表标注引自文献 7（那是推荐强度分级标准），活动分级表标注引自文献 40（那是弹性成像的研究）；低能量激光引文献 47，而文献 47 在正文是“肌腱需 36～72 小时恢复”的出处",
    f"{red('和自家模型矛盾')}：疼痛监测模型规定活动后疼痛不超过 5 分，但“重”活动的活动后疼痛写的是 {b('5～6 分')}",
    "活动分级的疼痛区间重叠：轻 1～2、中 2～3，评 2 分算哪一级不清楚",
    "超声厚度的测量标准误，正文写 0.02 厘米，图 4 写 0.01 厘米",
    "分期时间重叠：恢复期第 2～5 周、重建期第 3～12 周",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"跟腱痛不用完全停练，{mk('用疼痛监测模型管负荷')}：训练中、训练后、次日早上都 ≤5 分，且不逐周加重",
    "提踵是主角：平地双腿 → 单腿 → 离心 → 坐姿 → 台阶边 → 快速回弹 → 负重；止点型不下台阶",
    "负重从 4.5 千克左右起步，3 × 15 轻松就加重；力量恢复了也别停",
    "走路痛 ≤1～2 分、单腿跳 20 次痛 ≤2 分，再开始跑跳",
    "回场按轻、中、重排活动，重活动后歇 3 天、中等歇 2 天",
    "评估四个维度：症状、功能（提踵耐力、跳跃）、结构、心理，别只问“还痛不痛”",
    "早期出现晨僵、成绩下滑就要调整负荷，不要等到痛得练不了",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　推荐强度分级（SORT）"))
A.append(table(["推荐强度", "定义"], [
    ["A", "基于一致、高质量、以患者为导向的证据"],
    ["B", "基于不一致或质量有限、以患者为导向的证据"],
    ["C", "基于共识、常规做法、专家意见、以疾病为导向的证据，或诊断、治疗、预防、筛查的病例系列"]]))
A.append(tcap("原文表 2　跟腱综合负荷方案"))
A.append(table(["阶段", "患者状态", "负荷强度", "目标", "练习"], [
    ["症状管理与减负荷期：第 1～2 周（需要时更长）", "所有活动都痛，单腿提踵做不到 10 次", "逐步加到 100% 体重，慢速、可控；需要时先水中、减重或等长跖屈", "开始练习，了解伤病性质，学会用疼痛监测模型", "每天 1 次：疼痛监测模型讲解和运动建议；勾脚踩脚促循环；平地双腿提踵 3 × 10～15；平地单腿提踵 3 × 10；平地离心提踵 3 × 10；坐姿提踵 3 × 10"],
    ["恢复期：第 2～5 周（需要时更长）", "运动时痛、晨僵、提踵时痛", "加快速度、加外部阻力增加跟腱负荷；体重方案轻松完成后再加阻力", "开始力量训练", "每天 1 次：台阶边双腿提踵 3 × 15；台阶边单腿提踵 3 × 15；台阶边离心提踵 3 × 15；坐姿提踵 3 × 15；快速回弹提踵 3 × 20。止点痛者继续在平地做"],
    ["重建期：第 3～12 周（需要时更长）", "恢复期练习耐受好，止点不痛，晨僵可能减轻或加重", "继续加外部阻力，按耐受开始增强式训练", "更重的力量训练，增加或开始跑跳", "每天练，每周 2～3 次加重：台阶边负重单腿提踵 3 × 15；台阶边负重离心提踵 3 × 15；坐姿提踵 3 × 15；快速回弹提踵 3 × 20；专项增强式训练。止点痛者继续在平地做"],
    ["重返运动期：3～6 个月（需要时更长）", "症状很少，偶有晨僵（非每天），能顺利参加运动", "在前一阶段基础上，高强度日加入专项速度和动作模式", "维持训练，无症状", "每周 2～3 次：台阶边负重单腿提踵 3 × 15；台阶边负重离心提踵 3 × 15；快速回弹提踵 3 × 20。止点痛者继续在平地做"]]))
A.append(tcap("原文表 3　跟腱负荷活动分级与建议恢复天数"))
A.append(table(["特征", "轻", "中", "重"], [
    ["活动中疼痛（0～10）", "1～2", "2～3", "4～5"], ["活动后（当时或次日）疼痛", "1～2", "3～4", "5～6"],
    ["自觉跟腱用力（0～10）", "0～1", "2～4", "5～10"], ["活动间需要的恢复天数", "0（可每天做）", "2", "3"],
    ["跑者举例", "走 70 分钟", "平地慢跑 30 分钟", "以伤前 85% 速度跑 20 分钟"]]))
A.append(tcap("原文表 4　跟腱病的治疗与推荐强度"))
A.append(table(["治疗", "证据", "推荐强度"], [
    ["运动", "减轻症状、改善功能的证据最强；任何机械负荷（离心或慢速向心 + 离心）都有效；每周至少 2 次", "A"],
    ["矫形鞋垫", "无法给出推荐；定制与成品无差别；可能减少跟腱应变；不能减痛", "B"],
    ["低能量激光", "证据矛盾；可作为运动的辅助", "B"],
    ["贴扎", "可能改变足姿、减少跟腱应变；减痛证据有限", "C"],
    ["离子导入", "能减轻急性中段型跟腱病的疼痛和症状", "B"],
    ["器械辅助软组织松动", "踝关节活动度下降时有效", "C"],
    ["体外冲击波", "短期减痛、促进肌腱愈合；配合离心负荷优于单纯离心；结果差异大", "B"],
    ["注射", "没有证据支持单独使用或配合运动", "A"]]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Silbernagel KG, Hanlon S, Sprague A. Current clinical concepts: conservative management of Achilles tendinopathy. J Athl Train. 2020;55(5):438-447. doi:10.4085/1062-6050-356-19</em><br>"
    "原文版权归美国国家运动防护师协会所有，PDF 未标注知识共享协议；原文图 5 为经授权转载。本文仅为学术交流用的中文解读，照片引自原文图 1、3、4、6（编者加中文标注，超声英文标注和箭头说明改为中文，器械文字已模糊），"
    "图 2、5 按原图重绘为中文，四期方案卡、活动分级卡与排程示例为编者中文绘制，表格为编者翻译，如有侵权请联系删除。"
))

TITLE = "「跟腱病」不用完全停练：疼痛监测 + 四期提踵 + 回场排程"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>跟腱病保守治疗推文</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
  :root { --ground:#ececec; --paper:#ffffff; color-scheme:light; }
  body { background:var(--ground); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
         padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:16px 32px; }
  .paper { max-width:640px; margin:0 auto; background:var(--paper); padding:20px 16px 28px; box-sizing:border-box; }
  .paper h1 { font-size:22px; line-height:1.4; margin:0 0 8px; color:#111; text-wrap:balance; }
  .paper .by { font-size:14px; color:#576b95; margin-bottom:20px; }
  .paper img { max-width:100%; }
</style>
<div class="paper">
<h1>""" + TITLE + """</h1>
<div class="by">原创 · 悦美力</div>
""" + BODY + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
