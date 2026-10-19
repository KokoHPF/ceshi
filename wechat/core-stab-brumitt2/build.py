#!/usr/bin/env python3
"""Brumitt 2013 核心稳定训练处方（下）推文：生成 article_body.html 与 preview.html。

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
    "Brumitt J, Matheson JW, Meira EP. Core Stabilization Exercise Prescription, Part 2: A Systematic Review of Motor Control and General (Global) Exercise Rehabilitation Approaches for Patients With Low Back Pain. Sports Health. 2013;5(6):510-513.",
    "作者来自美国太平洋大学（俄勒冈）物理治疗学院等",
    "系统综述（PubMed 临床查询，1966—2013 年 3 月）；DOI：10.1177/1941738113502634",
    "上篇讲两条路线怎么评估、怎么练，本篇回答“哪条更有效”",
], square=True))

A.append(h2("先说结论"))
A.append(p(
    f"上篇介绍了两条核心稳定路线：{b('运动控制训练')}（专门练腹横肌、多裂肌，先学腹部回缩）"
    f"和{b('一般性训练')}（整体肌一起练，比如 McGill 三大动作、背部力量训练）。"
))
A.append(p(
    f"这篇把 15 项随机对照试验放在一起看，结论很直接：{mk('两条路线都能减轻慢性腰痛的疼痛和功能障碍')}；"
    f"但{red('直接对比时，大多数研究两组没差别')}，有 2 项反而是一般性训练更好。"
    f"作者的原话是：{b('“可能没有必要专门开那些号称能选择性激活局部肌的练习。”')}"
))

A.append(h2("怎么做的"))
A.append(pic(2, "检索流程（按原文表 1 重绘）"))
A.append(ul([
    "先在三个数据库里检索，结果太多（“腰痛 + 运动”超过 4100 篇），改用 PubMed 临床查询，专门筛随机对照试验",
    "12 组关键词，每组检出少于 200 篇时逐篇看摘要；只纳入英文随机对照试验，至少一组用运动控制训练或一般性训练",
    f"最终纳入 {b('15 项')}：8 项运动控制训练与其他处理比较，7 项一般性训练（其中 6 项直接与运动控制训练比较）",
]))

A.append(h2("结果：两条路线分别怎么样"))
A.append(pic(3, "15 项试验一览（编者按正文整理；原文附录 1、2 的逐项表格未能获取）"))
A.append(h3("运动控制训练：比“不怎么练”好"))
A.append(ul([
    f"和全科医生常规处理比，{b('2 项研究')}运动控制组更好：O’Sullivan 1997（腰椎峡部裂/滑脱）、Moseley 2002",
    f"Moseley 的方案只有 {b('8 次课')}：运动控制训练 + 手法 + {mk('疼痛神经科学宣教')}",
    f"Shaughnessy 2004：{b('10 周')}局部肌训练，功能障碍问卷和生活质量（除总体健康外）都明显优于不干预组",
    "对比手法、宣教、安慰剂时，运动控制训练在部分指标上更好",
    "对比 McKenzie 疗法（腰痛超过 7 周）：当前疼痛指数两组相近；6 周后运动控制组疼痛描述和当前疼痛指数都改善，McKenzie 组只改善了后者",
    "对比手法治疗（Goldby 2006）：两组 3、6、12 个月都改善，只有 6 个月时运动控制组更好",
]))
A.append(h3("一般性训练 vs 运动控制训练：大多打平"))
A.append(ul([
    f"Cairns 2006：专门练局部肌 vs 不含低负荷高重复练习的常规积极治疗，{b('1 年时')}功能障碍、疼痛、心理困扰、总体健康{b('都没差别')}",
    f"Critchley 2007：三组（含专门的躯干肌再训练、宣教）{b('18 个月')}都比基线改善，{b('组间没差别')}",
    f"{mk('Koumantakis 2005')}：运动控制 + 一般性训练 vs 单纯一般性训练，2 个月时{red('单纯一般性训练组的功能障碍反而更好')}，两组疼痛都明显下降；这项研究写清了每周的练习内容，并且按躯干肌的估算总输出力来平衡两组练习时间",
]))

A.append(h2("重点：一个可以照着用的三阶段方案"))
A.append(p(
    f"综述里写得最具体的方案来自 {b('Norris & Matthews 2008')}：慢性腰痛患者做 6 周三阶段背部稳定训练，"
    f"疼痛（简式 McGill 疼痛问卷）、功能障碍（Roland-Morris 问卷）和恐动（坦帕恐动量表）都优于只发背部保健手册。"
))
A.append(pic(4, "Norris & Matthews 三阶段方案与进阶条件"))
A.append(ul([
    f"{b('第 1 阶段 姿势练习')} → 进阶条件：{mk('不再需要理疗止痛，且能在脊柱中立位做出腹部内收')}",
    f"{b('第 2 阶段 背部体能练习')}（针对整体肌） → 进阶条件：{mk('仰卧单腿抬起能完成 5 次')}",
    f"{b('第 3 阶段 功能性强化')}",
    "有意思的是：它的入门用的是传统上用来“单独激活局部肌”的腹部内收，但后面的练习都是练整体肌的——两派的东西其实可以拼在一起用",
]))

A.append(h2("原文的临床推荐"))
A.append(pic(5, "原文临床推荐（SORT 分级）"))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{red('严格说算不上规范的系统综述')}：只检索了 PubMed 临床查询，只收英文，没有做偏倚风险或质量评价，没有合并数据，也没说明几个人筛选",
    "纳入研究的人群、方案、对照、随访时间差别很大（有的是腰椎滑脱，有的是复发性腰痛），放在一起只能定性看",
    "大多是慢性或亚急性腰痛的普通患者，专门针对运动员的随机对照试验几乎没有",
    "逐项研究的数据在附录里，正文只挑了几项描述；所以上面的一览图有 3 项只能写“原文归入多数无差别”",
]))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    "正文说“2 项研究结果支持一般性训练（参考文献 11、17）”，但 17 是 Niemistö（手法 + 稳定训练 vs 医生咨询，属运动控制类），紧接着描述的却是 Koumantakis（11）和 Norris & Matthews（18），引用应为 11、18",
    "而 Norris & Matthews 的对照是宣教手册，不是运动控制训练，不能算作“一般性训练优于运动控制训练”",
    "原文表 1“纳入评价”一列加起来是 14 篇（8 + 3 + 1 + 1 + 1），与正文“15 篇”对不上",
    "摘要写数据来源是 PubMed 临床查询，方法里却先写了 MEDLINE、CINAHL、SPORTDiscus（后放弃），摘要没交代",
    "参考文献 21 作者写成“Richardson C, Hodges PW, Hides J, Richardson C”，和上篇一样重复",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('别纠结“到底练深层还是练整体”')}：两条路线都有效，直接对比大多没差别，选患者能做、愿意坚持的",
    "腹部回缩可以作为入门技巧，但不必花几周只练“单独激活腹横肌”才敢往下走",
    f"推荐参考 Norris & Matthews 的思路：{b('先止痛 + 学会中立位收腹 → 整体肌力量耐力 → 功能性训练')}，用“仰卧单腿抬起 5 次”这类简单标准来决定进阶",
    "宣教不能少：Moseley 的方案里加了疼痛神经科学宣教",
    "证据等级只有 B，个体反应差别大，按评估结果（见上篇的测试）调整比死守一种流派更重要",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　关键词检索结果"))
A.append(table(["关键词", "检出", "可能相关", "纳入评价"], [
    ["运动控制训练", "1729", "—", "—"],
    ["治疗性运动 AND 腰痛", "837", "—", "—"],
    ["一般性运动 AND 腰痛", "188", "17", "8"],
    ["节段稳定", "139", "4", "0"],
    ["稳定 AND 运动", "122", "7", "3（2）"],
    ["整体运动 AND 腰痛", "70", "5", "1（2）"],
    ["运动控制训练 AND 腰痛", "33", "9", "0（4）"],
    ["腹横肌 AND 运动", "27", "7", "0"],
    ["核心稳定训练", "37", "2", "1"],
    ["节段稳定训练", "11", "3", "0"],
    ["局部肌训练 AND 腰痛", "10", "0", "1"],
    ["核心稳定训练 AND 腰痛", "6", "2", "0（2）"],
]))
A.append(small("括号内为与前面检索重复的篇数。“纳入评价”一列合计 14 篇，正文写 15 篇。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Brumitt J, Matheson JW, Meira EP. Core Stabilization Exercise Prescription, Part 2: A Systematic Review of Motor Control and General (Global) Exercise Rehabilitation Approaches for Patients With Low Back Pain. Sports Health. 2013;5(6):510-513. doi:10.1177/1941738113502634</em><br>"
    "原文版权归作者与 SAGE 出版社所有，非知识共享协议开放获取。本文仅为学术交流用的中文解读，所有图表均为编者根据原文中文重绘或翻译，如有侵权请联系删除。"
))

TITLE = "「核心」专练深层肌，真的比整体练更好吗？15 项随机对照试验的答案"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>核心稳定训练处方下篇推文</title>
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
