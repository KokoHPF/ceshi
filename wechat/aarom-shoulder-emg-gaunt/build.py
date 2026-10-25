#!/usr/bin/env python3
"""Gaunt 等 2010《分解式助力肩上举训练的肌电评估》（Sports Health）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
配图：python3 tools/make_figs.py src images <中文字体>
（原文图 1～4 是练习照片，图内只有 A/B 面板字母、没有英文，只加中文图注；结果图按原文表 2～4 重绘）
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
    "Gaunt BW, McCluskey GM, Uhl TL. An Electromyographic Evaluation of Subdividing Active-Assistive Shoulder Elevation Exercises. "
    "Sports Health. 2010;2(5):424-432. doi:10.1177/1941738110366840",
    "中文题目：分解式助力肩上举训练的肌电评估",
    "作者单位：美国佐治亚州哥伦布市圣弗朗西斯康复中心、圣弗朗西斯骨科研究所；肯塔基大学康复科学系",
    f"研究类型：{b('对照实验室研究')}（健康人一次性肌电测量）",
], square=True))

A.append(h2("先说为什么要读这篇"))
A.append(p(
    f"肩袖修补、肩峰下撞击、肱二头肌长头腱固定等术后，恢复{b('主动上举')}往往占了康复的一大半。"
    f"常见的做法是从被动活动过渡到{b('助力活动（AAROM）')}，再到主动上举。"
))
A.append(p(
    f"助力阶段通常还要再细分：先做{b('减重力')}的（仰卧、侧卧、在桌面上滑），再做{b('直立助力')}的（滑轮、爬墙、体棒），最后才站着主动举。"
    "这个顺序的依据是生物力学推理：越接近直立、重力的阻力越大，肌肉就要越用力。"
))
A.append(p(
    f"可这一步到底让冈上肌、冈下肌多出了多少力，此前{b('没有人用肌电测过')}。"
    f"这篇就把 11 个临床常用的上举练习一个个测了，{mk('看“先躺后站”的分阶段到底有没有必要')}。"
))
A.append(p("作者的两个假设："))
A.append(ul([
    "直立助力练习的冈上肌、冈下肌、三角肌前束肌电，高于减重力练习",
    "站立主动上举的肌电，高于所有助力练习",
]))

A.append(h2("研究怎么做"))
A.append(img(2))
A.append(ul([
    f"{b('15 名健康年轻人')}（7 女 8 男），平均 23.9 岁；纳入标准是 18～40 岁、优势侧肩没有骨折、脱位、慢性疼痛或手术史，现在不痛、主动活动度正常",
    f"{b('冈上肌、冈下肌用针电极')}（冈上肌被斜方肌盖住，表面电极测不到），{b('三角肌前束用表面电极')}",
    "每块肌肉做 2 次 5 秒最大等长收缩（徒手肌力测试姿势），取最高的 500 ms 均方根作为 100% MVIC",
    f"11 个练习抽签定顺序，每个做 5 次，节拍器控制在{b('每秒约 30°')}；电子测角仪贴在肩胛冈和肱骨上，用来分出每一次动作",
    f"作者只看每次动作的{b('最大值')}而不是平均值，理由是要估计“最坏情况”下肌肉会用多大力，好保护正在愈合的组织",
]))

A.append(h2("11 个练习怎么分"))
A.append(p(
    f"作者把练习分成三类：{b('减重力')}（重力帮忙完成向心阶段，或者动作方向和重力垂直、手臂重量有支撑）、"
    f"{b('直立助力')}（站着对抗重力上举，但手有东西托着或沿着东西滑）、{b('直立主动')}（站着徒手举，作对照）。"
))
A.append(tcap("表 1　11 个上举练习（编者根据原文表 1 翻译整理）"))
A.append(table(["类型", "练习", "怎么做"], [
    ["减重力", "擦桌（正前方、内侧 45°、外侧 45°）", "坐在与肘同高的桌前，手压毛巾向前推到肘伸直再收回；内、外侧版本偏 45°（外侧即肩胛平面）。盂肱关节活动约 0°～45°"],
    ["减重力", "侧卧滑板上举", "健侧卧，患侧手放在熨衣板上，带着毛巾滑到约 140° 再滑回，手的重量一直落在板上"],
    ["减重力", "仰卧弹力带前屈（从 90° 起）", "仰卧屈膝，健侧手把红色 Thera-Band 按在腰部；患侧从屈曲 90° 主动举到约 160° 拉长弹力带，再慢慢放回，全程外旋"],
    ["直立助力", "滑轮", "主要靠健侧手拉绳，把患侧手沿肩胛平面从体侧拉到约 160°，再放下"],
    ["直立助力", "手指爬墙", "离墙 20～40 cm，食指、中指从肩高沿墙“走”上去再走下来，约 30°～160°"],
    ["直立助力", "墙面滚球", "离墙一臂远，伸肘把网球在墙上上下滚一个手掌的距离（约 20°）"],
    ["直立助力", "体棒助力前屈", "患侧手握 PVC 棒（拇指朝上），主要靠健侧手推着举到约 160° 再放下"],
    ["直立助力", "体棒助力＋主动下放", "同上，但放下时患侧手松开棒，伸肘自己慢慢放下（离心）"],
    ["直立主动", "站立主动上举", "站立、伸肘、拇指朝上，沿肩胛平面徒手举到约 160° 再放下"],
], first_bold=True))
A.append(img(3))
A.append(img(4))
A.append(img(5))
A.append(img(6))

A.append(h2("结果：三块肌肉各不相同"))
A.append(img(7))
A.append(tcap("表 2　三块肌肉的平均最大肌电（% MVIC，均值及 95% 置信区间，编者根据原文表 2～4 合并翻译）"))
A.append(table(["练习", "冈上肌", "冈下肌", "三角肌前束"], [
    ["侧卧滑板上举", "7（4～9）", "10（6～14）", "16（12～21）"],
    ["仰卧弹力带前屈", "8（5～11）", "13（9～18）", "15（12～18）"],
    ["擦桌·内侧", "12（8～15）", "7（4～10）", "16（12～20）"],
    ["擦桌·正前方", "12（8～16）", "8（5～10）", "16（11～20）"],
    ["擦桌·外侧", "13（9～17）", "9（6～13）", "14（9～19）"],
    ["墙面滚球", "16（11～21）", "18（11～24）", "27（23～32）"],
    ["体棒助力前屈", "16（11～21）", "13（8～19）", "30（25～36）"],
    ["滑轮", "17（11～23）", "14（9～18）", "31（23～38）"],
    ["手指爬墙", "21（16～27）", "19（11～27）", "32（27～36）"],
    ["体棒＋主动下放", "20（13～26）", "18（11～26）", "35（29～42）"],
    ["站立主动上举", "29（22～37）", "21（12～30）", "45（40～50）"],
]))
A.append(small("前 5 行为减重力，中间 5 行为直立助力，最后 1 行为直立主动。"))

A.append(h4("冈上肌"))
A.append(ul([
    f"{b('站立主动上举最高')}（29%），显著高于其余 10 个练习",
    "5 个减重力练习彼此没有差异；所有直立练习都高于侧卧滑板上举（7%）",
    f"直立助力里{b('只有手指爬墙')}（21%）显著高于全部 5 个减重力练习，其余只比 1～2 个减重力练习高",
]))
A.append(h4("冈下肌"))
A.append(ul([
    "站立主动上举数值最高（21%），但只显著高于擦桌·内侧（7%）",
    "只有擦桌·内侧和擦桌·正前方这 2 个减重力练习，显著低于滑轮、墙面滚球和两个体棒练习；擦桌·外侧、侧卧滑板上举、仰卧弹力带和任何练习都没有差异",
    f"{b('整体都偏低')}，最高也只有约 20%，个体差异大",
]))
A.append(h4("三角肌前束"))
A.append(ul([
    f"{b('站立主动上举最高')}（45%），显著高于其余所有练习",
    f"{b('直立助力（27%～35%）普遍高于减重力（14%～16%）')}，唯一的例外是滑轮：和侧卧滑板上举之间的差异 P = 0.00092，刚好没过 Bonferroni 校正后的门槛 0.00091",
]))
A.append(p(
    f"作者引用的分级：{b('< 20% 为低')}、20%～40% 中等、41%～60% 高、> 60% 很高。"
    "照此，减重力练习全部是“低”，直立助力在“低”到“中等”之间。"
))

A.append(h2("讨论里说了什么"))
A.append(ul([
    f"{b('减重力练习 ≈ 被动活动')}：冈上肌、冈下肌只有 7%～13% MVIC，和前人测的持续被动活动、治疗师被动上举（不超过 10%）差不多，适合作为从被动过渡到助力的第一步",
    f"{b('对冈上肌、冈下肌，分阶段没有必要')}：虽然数值从减重力到直立助力逐渐升高，但只有少数练习两两有差异、置信区间大量重叠，第一个假设在这两块肌肉上被否定。进阶应该看活动度、疼痛耐受和有没有代偿",
    f"{b('对三角肌前束，分阶段是有意义的')}：两类练习差得很清楚，在少数需要保护三角肌的情况下（如切开肩袖修补、三角肌成形）值得按“先减重力、后直立”来排",
    f"{b('手指爬墙不该当被动活动')}：它的冈上肌、三角肌前束都高于所有减重力练习，应放在助力阶段后期",
    f"{b('仰卧弹力带前屈其实很轻')}：虽然加了弹力带，肌电和其他减重力练习、被动活动相当，说明体位对低强度上举的肌肉负荷影响很大",
    "和 Kronberg 的研究比，本研究冈下肌和三角肌前束的数值偏低，作者认为和动作慢（每秒 30°）有关",
    "作者自认的局限：动态肌电和肌腱受到的拉力没有确定的对应关系；表面肌电有串扰，针电极只代表一小块肌肉；受试者是健康年轻人，不是有疼痛和活动受限的患者",
]))

A.append(h2("这篇能信几分"))
A.append(ul([
    f"{b('健康人、慢速、一次测量')}：15 个 22～28 岁的健康人，每个动作只做 5 次，节拍器压到每秒 30°。真正做这些练习的是术后、疼痛、活动受限的患者，他们可能耸肩、代偿，肌肉的用法会不一样",
    f"{b('“没差异”≠“一样”')}：11 个练习两两比较共 55 次，Bonferroni 把门槛压到 P < 0.00091，15 个人的样本能检出的只有很大的差异。冈上肌、冈下肌“分阶段没必要”的结论，很大程度上是统计效能不足的结果，不能当作“已证明一样”",
    f"{b('只看最大值')}：作者有意用峰值估计最坏情况，这对保护组织是合理的；但它不反映整个动作的持续负荷，和别人报告的平均值也不能直接比",
    f"{b('肌电不等于肌腱受力')}：保护修补后的肩袖，关心的是肌腱受到的拉力；% MVIC 只是间接指标，作者自己也承认",
    f"{b('利益冲突')}：研究部分由 McCluskey 教育与研究基金会资助，第二作者是该基金会研究主任，第一作者受雇于基金会董事拥有的公司（原文已声明）",
    "优点：用针电极测冈上肌、冈下肌，比表面电极可信；练习描述细，临床可以直接照做；把常凭经验排的进阶顺序第一次用数据检验了一遍",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('摘要说冈上肌、冈下肌“P > .05”')}：摘要写两块肌肉从减重力到直立助力只是“增高趋势（P > .05）”，"
    "可结果和表 2、表 3 明明有显著差异：冈上肌所有直立练习都高于侧卧滑板上举、手指爬墙高于全部减重力练习；冈下肌 4 个直立助力练习高于擦桌·内侧和正前方。准确说法应是“只有部分练习之间有差异”",
    f"{b('滑轮的三角肌前束数值')}：结果正文写 30% ± 12% MVIC，表 4 是 31 ± 13",
    f"{b('侧卧滑板上举的三角肌前束数值')}：结果正文写 16% ± 7% MVIC，表 4 是 16 ± 8",
    f"{b('站立主动上举算“中等”还是“高”')}：讨论说主动上举属于“中等强度”，但按作者自己引用的分级（41%～60% 为高），三角肌前束 45% MVIC 应属“高”，只有冈上肌（29%）、冈下肌（21%）是中等",
    f"{b('“减重力练习 7%～13%”')}：讨论把减重力练习的最大肌电概括为 7%～13% MVIC，这只是冈上肌和冈下肌的范围，三角肌前束是 14%～16%",
    f"{b('显著性门槛前后两套')}：方法写 Bonferroni 校正后 P < 0.00091，表 2～4 的表注却写“有显著差异（P < .05）”",
    f"{b('信度系数和次数对不上')}：方法写用 ICC(2,3) 评估信度，下标 3 表示取 3 次的平均，但每个练习做的是 5 次、分析用的也是 5 次平均",
    f"{b('SEM 比标准差还大')}：表 4 站立主动上举 SD 9、ICC 0.57，SEM 却是 10；按常用公式 SEM = SD × √(1 − ICC) 只有约 6，SEM 不可能大于 SD。滑轮（SD 13、ICC 0.59、SEM 11）、侧卧滑板上举（SD 8、SEM 7）、冈上肌仰卧弹力带（SD 6、SEM 6）也算不出来，原文没说明 SEM 用的是哪个 SD",
    f"{b('“前屈”还是“肩胛平面”')}：练习叫“active forward elevation（前屈上举）”，表 1 的做法却写“在肩胛平面内”上举；作为对照的动作和体棒“前屈”不在同一个平面",
    f"{b('速度统一不了')}：方法说 11 个练习都用节拍器控制在每秒 30°，但手指爬墙规定“40 次/分钟、4 拍走上去再走下来”，约 130° 的弧度换算下来并不是每秒 30°；墙面滚球只有约 20° 的弧度",
    f"{b('受试者和患者混用')}：方法同一段里前面说“participants 抽签”，后面又写“the patient was given a visual demonstration”，但受试者全是健康人",
    f"{b('笔误')}：Greenhouse-Geiser 应为 Greenhouse-Geisser；引言“for this level or exercise”应为 of；表 1“Dominate arm”应为 Dominant",
]))

A.append(h2("落到临床"))
A.append(img(8))
A.append(cap("临床要点（编者整理）"))
A.append(ul([
    f"{mk('刚从被动过渡到助力')}：擦桌、侧卧滑板上举、仰卧弹力带前屈，三块肌肉都在 20% MVIC 以下，是比较稳妥的起点",
    f"{b('保护冈上肌、冈下肌时')}：减重力和多数直立助力练习差别不大，不必卡死“先躺后站”，按活动度、疼痛和有没有耸肩代偿来进阶更实际",
    f"{b('保护三角肌时')}（切开修补、三角肌成形等）：直立助力的三角肌前束明显更高，先做减重力练习",
    f"{b('手指爬墙、体棒＋主动下放放在助力后期')}：这两个在直立助力里数值最高，主动下放本质上已经是主动离心",
    "这是健康年轻人、慢速动作下的肌电，不是术后患者的数据；具体到某个术式的限制，仍以手术医生的方案为准（编者补充）",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Gaunt BW, McCluskey GM, Uhl TL. An Electromyographic Evaluation of Subdividing Active-Assistive Shoulder Elevation Exercises. "
    "Sports Health. 2010;2(5):424-432. doi:10.1177/1941738110366840</em><br>"
    "原文 © 2010 The Author(s)，由 SAGE 出版，可在 PubMed Central（PMC3445058）免费阅读，但未采用知识共享（CC）开放许可。"
    "本文为学术交流用的中文解读：练习照片引自原文图 1～4（编者把上下两格改为左右并排，并加中文图注）；"
    "表格为编者翻译；首图、研究流程卡、肌电对比重绘图和临床要点卡为编者根据原文整理绘制。版权归原作者与出版方，仅供学习交流，如有侵权请联系删除。"
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


TITLE = "「肩助力上举」先躺后站有必要吗？11 个练习测肌电：对冈上肌、冈下肌差别不大，三角肌前束才分得清"

BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>分解式助力肩上举推文</title>
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
