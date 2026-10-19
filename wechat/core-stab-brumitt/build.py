#!/usr/bin/env python3
"""Brumitt 2013 核心稳定训练处方（上）推文：生成 article_body.html 与 preview.html。

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
    "Brumitt J, Matheson JW, Meira EP. Core Stabilization Exercise Prescription, Part I: Current Concepts in Assessment and Intervention. Sports Health. 2013;5(6):504-509.",
    "作者来自美国太平洋大学（俄勒冈）物理治疗学院等",
    "临床综述（检索 MEDLINE、CINAHL，1966—2013 年 3 月）；DOI：10.1177/1941738113502451",
], square=True))

A.append(h2("先说这篇在讲什么"))
A.append(p(
    f"运动员腰痛，“练核心”几乎是标配。但“核心”到底练什么、怎么评估，一直有两派："
    f"{b('一派盯着深层的腹横肌和多裂肌')}（Richardson、Hodges 的运动控制路线），"
    f"{b('一派主张所有核心肌一起练')}（McGill 的整体路线）。"
))
A.append(p(
    f"这篇上篇不做裁判，而是把两派各自的{mk('评估方法和训练流程')}讲清楚，外加两个门诊里很好用的桥式测试。"
    "对临床最有用的是：每一步测什么、怎么测、达到什么标准再往下走。"
))
A.append(pic(2, "两条核心稳定康复路线"))

A.append(h2("核心和“稳定”指什么"))
A.append(ul([
    "核心：腹部、脊柱、骨盆和髋的肌肉与关节。它们一方面保护脊柱免受有害外力，另一方面负责在身体各节段之间产生和传递力量，比如投手从下肢蹬地到上肢出手",
    "稳定：减少关节面之间异常或过度、会引起症状的位移",
    f"“功能性腰椎节段不稳”：X 线上不一定能看到节段过度移位，但因为{b('韧带约束不够 + 肌肉激活差')}，在正常负荷下也守不住节段的位置；这类症状可能对稳定训练有反应",
    "局部肌：腹横肌、多裂肌；整体肌：竖脊肌、腰方肌、腹斜肌、腹直肌",
]))

A.append(h2("重点一：局部肌路线怎么评估、怎么练"))
A.append(h3("为什么盯着腹横肌和多裂肌"))
A.append(ul([
    f"慢性腰痛的人，四肢一动之前腹横肌本该{b('提前收缩')}，这个提前量变迟了",
    "腹横肌的收缩还从持续性变成爆发式，变得只在快速动作时才收缩，并且像其他腹肌一样受动作方向影响",
    "多裂肌更容易疲劳、向心激活变低、出现萎缩和结构改变",
]))
A.append(h3("第一步：教会“腹部回缩”"))
A.append(p(
    f"先给患者讲清楚核心肌的解剖和作用，再教{mk('腹部回缩')}：把腹壁往里收，激活深层的局部肌，但不让表浅的整体肌参与，脊柱和骨盆不动。"
    "先在四点跪位练，再到俯卧和仰卧位用压力生物反馈仪检查。"
))
A.append(pic(4, "原文表 1　三项运动控制测试"))
A.append(pic(5, "原文图 1　仰卧屈膝滑腿测试（压力生物反馈仪垫在腰下）"))
A.append(ul([
    f"{b('四点跪')}：口令“腹壁往里收，脊柱骨盆不动，正常呼吸，保持 10 秒”，反复练到熟练",
    f"{b('俯卧')}：气囊放腹下、肚脐居中，充到 {b('70 mmHg')}；回缩后压力降 {red('6～10 mmHg')} 算成功；每次 10 秒、做 10 次，看耐力。做不好就把它直接当成练习",
    f"{b('仰卧屈膝')}：气囊放腰下（下缘平第 2 骶椎），充到 {b('40 mmHg')}，回缩后约升 2～4 mmHg；然后{mk('脚跟贴着床面把腿滑直，压力保持不变')}，说明能在四肢活动时稳住腰盆；再难一点就把腿悬空伸直",
]))
A.append(h3("第二步：三阶段康复"))
A.append(pic(3, "局部肌路线的三阶段"))
A.append(ul([
    f"{b('第 1 阶段 局部肌控制')}：俯卧、仰卧的低负荷等长练习，配合生物反馈，盯住代偿；做熟了可以进阶到桥式、鸟狗",
    f"{b('第 2 阶段 闭链节段控制')}：屈曲位和直立位的负重练习，先稳定面、再不稳定面，局部肌和负重肌一起工作。{b('进入条件：局部肌共同收缩测试正常')}",
    f"{b('第 3 阶段 开链远端活动')}：非负重练习，四肢远端动、躯干保持节段稳定，用来暴露残留的局部肌问题",
    "最后加入大负荷功能动作，局部肌与整体肌共同收缩",
    f"这一派的原则：{b('每个练习都先做腹部回缩')}；{red('过早加入整体肌可能有害')}——局部肌更擅长对抗剪切力，整体肌过度激活会给脊柱额外压力",
]))

A.append(h2("重点二：McGill 整体路线怎么评估、怎么练"))
A.append(p(
    f"McGill 的观点正相反：腰伤后{b('所有肌肉')}都有激活延迟，而且每块肌肉对稳定的贡献随动作变化；"
    f"想单独激活腹横肌而不带动其他腹肌，根本做不到；{mk('整圈绷紧的“腹部支撑”比“腹部回缩”更能增加稳定')}。"
))
A.append(h3("第一步：3 项耐力测试（计时到力竭）"))
A.append(pic(6, "原文图 2～5　背伸肌、侧桥、屈肌耐力测试"))
A.append(ul([
    f"{b('背伸肌测试')}：俯卧，髂前上棘以下固定在床上（绑带或测试者压住），上身悬空、先用手撑椅子；开始时上身与地面平行、双臂抱胸，计时到撑不住",
    f"{b('侧桥测试')}（左右各一次）：肘屈 90° 撑在肩正下方，双腿伸直与躯干成一线、上面的脚放在下面的脚前方，另一只手搭对侧肩；撑不住即停",
    f"{b('屈肌测试')}：靠在与床面成 60° 的靠垫上，双臂抱胸，屈髋屈膝 90°（脚固定）；把靠垫往后撤 10 cm 开始计时，背碰到靠垫即停",
]))
A.append(pic(7, "看比值：判断核心耐力是否失衡"))
A.append(p(
    f"关键不是秒数本身，而是{mk('比值')}：屈肌/背伸肌 < 1.0，侧桥/背伸肌 < 0.75，左右侧桥差 < 0.05。"
    "受伤的运动员通常至少有一项失衡。"
))
A.append(h3("第二步：“三大动作”练耐力，再进阶"))
A.append(ul([
    f"McGill 的{b('“三大动作”')}：{b('侧桥、鸟狗、卷腹')}",
    "耐力提高、比值恢复平衡后，再进阶到核心的功能性训练",
    "原文只列出了动作名称，没有给具体剂量和做法",
]))

A.append(h2("备选：桥式测试"))
A.append(p(
    "有些患者症状太重，摆不出 McGill 测试的体位；腹横肌、多裂肌的测试又测不出耐力。这时可以用俯卧桥（平板支撑）和仰卧桥做门诊评估："
))
A.append(pic(8, "原文图 6～7 与引用数据"))
A.append(ul([
    f"俯卧桥：无腰痛 {b('72.5 ± 32.6 秒')}，有腰痛 {red('28.3 ± 26.8 秒')}",
    f"仰卧桥：无腰痛 {b('170.4 ± 42.5 秒')}，有腰痛 {red('76.7 ± 48.9 秒')}",
]))

A.append(h2("这篇能信几分"))
A.append(ul([
    f"{red('这是叙述性综述，不是系统综述')}：虽然写了检索数据库，但没有纳入标准、没有质量评价，也没有比较两派的疗效",
    "大量依据来自两本教材（Richardson 1999、McGill 2007），而不是临床试验",
    "局部肌路线的阶段进阶“没有量化标准”，原文自己也承认要靠治疗师判断",
    "McGill 测试只给了比值标准，没有给参考时间；“三大动作”没有剂量",
]))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    "“不可能在其他腹肌参与的情况下激活腹横肌”——按 McGill 的原意应该是“不可能只激活腹横肌而不带动其他腹肌”，原文意思写反了",
    "仰卧桥的数据（170.4 秒 vs 76.7 秒）引用的是参考文献 22（Richardson 的教材），但俯卧桥和仰卧桥两组数据都出自 Schellenberg 2007（参考文献 26），应为引用错误",
    "左右侧桥“差 < 0.05”表述含糊：McGill 原文指左右比值偏离 1 不超过 0.05，原文没说清楚是比值还是秒数",
    "参考文献 23 作者写成“Richardson C, Hodges PW, Hides J, Richardson C”，Richardson 重复出现；参考文献 14（相邻节段病变的分类）与“功能性节段不稳”的论述不太相关",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{b('先评估、再选路线')}：腹部回缩做不好、仰卧滑腿压力守不住 → 先走局部肌控制；耐力比值明显失衡 → 先用三大动作补耐力",
    f"压力生物反馈的几个数字很实用：{mk('俯卧 70 mmHg 降 6～10，仰卧 40 mmHg 滑腿不掉压')}",
    f"McGill 三项测试{b('看比值不看绝对秒数')}，左右侧桥差别、屈肌是否超过背伸肌，往往比总时间更能说明问题",
    "症状重、摆不了体位的人，用俯卧桥/仰卧桥先粗筛",
    "两派并不完全对立：局部肌路线最后也要加入大负荷、局部和整体肌共同收缩；可以按患者当前能力选择起点",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　局部肌（腹横肌、多裂肌）运动控制测试"))
A.append(table(["测试", "做法"], [
    ["四点跪位腹部回缩测试", "口令：“腹壁往里收，脊柱和骨盆不动，正常呼吸，保持 10 秒。”反复练到掌握；患者在这个体位表现熟练后，进阶到俯卧测试"],
    ["俯卧位腹部回缩测试", "俯卧，用压力生物反馈仪评估腹横肌收缩：气囊中心对准肚脐，充气至 70 mmHg。做腹部回缩，成功时压力下降 6～10 mmHg，每次保持 10 秒。Richardson 建议做 10 次以评估耐力。表现差或耐力不足时，可直接把这个测试当作练习"],
    ["腹部回缩测试：腰盆控制（图 1）", "仰卧屈膝（屈髋屈膝、脚踩床面）。气囊放在腰下（下缘平第 2 骶椎），充气至 40 mmHg。做腹部回缩，压力通常升高 2～4 mmHg。然后脚跟沿床面滑动、把腿伸直，压力保持不变说明具备一定的腰盆控制（四肢活动时稳住躯干与骨盆）。可进一步做无支撑的伸腿来加大难度"],
], first_bold=True))
A.append(tcap("原文表 2　核心耐力测试"))
A.append(table(["测试", "做法"], [
    ["背伸肌测试（图 2、3）", "俯卧在治疗床上，下半身用绑带或测试者体重固定；上身从髂前上棘以上悬空，开始前双手撑在椅子上。患者摆出测试姿势（上身与地面平行、双臂抱胸）时开始计时"],
    ["侧方肌群测试（图 4）", "一侧肘屈 90° 撑在肩正下方，双腿伸直与躯干成一线，一只脚放在另一只脚前方；不负重的手放在对侧肩上。无法保持姿势时停止"],
    ["屈肌耐力测试（图 5）", "靠在与床面成 60° 的靠垫上，双臂抱胸，髋膝各屈 90°。把靠垫向后撤离背部 10 cm 时开始计时，背部碰到靠垫时停止"],
], first_bold=True))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Brumitt J, Matheson JW, Meira EP. Core Stabilization Exercise Prescription, Part I: Current Concepts in Assessment and Intervention. Sports Health. 2013;5(6):504-509. doi:10.1177/1941738113502451</em><br>"
    "<em>McGill SM, Childs A, Liebenson C. Endurance times for low back stabilization exercises: clinical targets for testing and training from a normal database. Arch Phys Med Rehabil. 1999;80:941-944.</em>（编者补充参考值来源）<br>"
    "原文版权归作者与 SAGE 出版社所有，非知识共享协议开放获取。本文仅为学术交流用的中文解读，照片引自原文图 1～7，示意图与图表为编者中文绘制，表格为编者翻译，如有侵权请联系删除。"
))

TITLE = "「核心」核心稳定怎么练？先评估再选路线：腹部回缩 vs McGill 三大动作"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>核心稳定训练处方推文</title>
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
