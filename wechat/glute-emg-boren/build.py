#!/usr/bin/env python3
"""Boren 2011 臀中肌臀大肌康复动作肌电推文：生成 article_body.html 与 preview.html。

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
    "Boren K, Conrey C, Le Coguic J, Paprocki L, Voight M, Robinson TK. Electromyographic analysis of gluteus medius and gluteus maximus during rehabilitation exercises. Int J Sports Phys Ther. 2011;6(3):206-223.",
    "作者来自美国贝尔蒙特大学（田纳西州纳什维尔）",
    "横断面肌电研究",
], square=True))

A.append(h2("先说为什么关心“哪个动作更出力”"))
A.append(p(
    f"臀中肌和臀大肌负责在单腿支撑时{b('稳住骨盆、防止髋内收内旋')}。它们无力，跟胫骨应力骨折、腰痛、髂胫束摩擦综合征、前交叉韧带损伤、髌股痛都有关系。"
))
A.append(p(
    f"之前 Distefano、Bolgla、Ayotte 各自给一批动作排过肌电名次，但彼此没比过。这篇把三项研究的前几名，加上其他常用动作，{mk('放在同一批人身上一起测')}。"
    f"作者把 {b('≥70% 最大自主等长收缩（%MVIC）')}当作“够得上力量训练”的门槛。"
))
A.append(p(
    f"先说结论：{b('侧桥外展、单腿蹲、平板支撑 + 伸髋')}三类动作，两块肌肉都能到 70% 以上；"
    f"{b('蚌式 4')} 专练臀中肌（77%），{b('站立臀肌夹紧')}专练臀大肌（81%）。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：{b('24 名')}健康成人（≥21 岁），排除运动时疼痛、近 2 年下肢手术或前交叉韧带损伤",
    "表面肌电贴在优势腿（踢球那条腿）的臀中肌和臀大肌",
    "最大自主等长收缩：按徒手肌力测试标准体位，股骨远端用绑带固定，每块肌肉 3 次、每次 5 秒",
    f"每个动作{b('先练 3 次、再正式做 5 次')}，节拍器 60 次/分钟统一速度，赤脚，随机顺序，动作间休息 2 分钟",
    "取每次重复的峰值（前后 50 毫秒平均），换算成 %MVIC 后排名",
]))
A.append(pic(6, "原文图 1、2"))

A.append(h2("结果：两份排行榜"))
A.append(pic(2, "臀中肌排名"))
A.append(pic(3, "臀大肌排名"))
A.append(pic(4, "两块肌肉同时看"))
A.append(ul([
    f"{b('臀中肌 ≥70%')}：侧桥外展-优势腿在下 103%、侧桥外展-优势腿在上 89%、单腿蹲 82%、蚌式 4 77%、平板支撑伸髋 75%",
    f"{b('臀大肌 ≥70%')}：平板支撑伸髋 106%、臀肌夹紧 81%、两种侧桥外展 73% 和 71%、单腿蹲 71%",
    f"{mk('两块都 ≥70%')}：平板支撑伸髋、两种侧桥外展、单腿蹲",
    f"意外的是：{red('单腿桥只排臀大肌第 11（稳定面）和第 14（不稳定面）')}，受试者常说腘绳肌抽筋，作者怀疑腘绳肌代偿",
    "蚌式 2～4 臀中肌很高，但臀大肌只有 12%～27%，是“定点”练臀中肌的好选择",
]))

A.append(h2("重点：18 个动作怎么做"))
A.append(pic(5, "按难度分层"))
A.append(h3("一、侧卧与站立的臀中肌练习"))
A.append(pic(7, "蚌式、侧卧外展、骨盆下降"))
A.append(ul([
    f"{b('蚌式 1')}：侧卧，髋屈约 45°、屈膝、双脚并拢；外旋上方髋把两膝打开（1 拍），1 拍回来",
    f"{b('蚌式 2')}：同样姿势，{b('两膝并拢')}，内旋上方髋把上方脚抬离下方脚",
    f"{b('蚌式 3')}：上方腿抬到与地面平行，保持膝的高度，内旋髋把脚往天花板方向抬",
    f"{b('蚌式 4')}：同蚌式 3，但{mk('髋完全伸直')}；回到起始位时膝、踝在一条线上",
    f"{b('侧卧外展')}：下方腿屈髋屈膝支撑，上方腿外展约 30°，保持髋中立或微伸、膝伸直、{b('脚尖朝前')}；2 拍上、2 拍下（防止阔筋膜张肌代偿）",
    f"{b('骨盆下降')}：优势腿站在 5 cm 台阶边缘，另一侧脚跟下落轻触地面（不承重），再把骨盆抬回，髋膝始终伸直",
]))
A.append(h3("二、高阶：侧桥外展与平板支撑伸髋"))
A.append(pic(8, "侧桥外展、平板支撑伸髋"))
A.append(ul([
    f"{b('侧桥外展')}：肘和脚支撑，肩、髋、膝、踝成一条线，把髋抬起成侧桥；保持侧桥，上方腿外展 1 拍、放下 1 拍。{mk('支撑在下的那条腿，臀中肌 103%')}",
    f"{b('平板支撑 + 伸髋')}：前臂撑地的平板，躯干、髋、膝中立；优势腿离地、屈膝，把脚跟向天花板方向伸髋越过中立位，1 拍上、1 拍回",
    "这两个动作需要很强的核心稳定，不适合力量弱的早期患者",
]))
A.append(h3("三、桥与四点跪"))
A.append(pic(9, "单腿桥、四点跪伸髋"))
A.append(ul([
    f"{b('单腿桥（稳定面）')}：屈膝仰卧，先双腿桥抬到躯干、髋、膝中立；再伸直非优势腿的膝（两侧大腿保持平行）1 拍，收回 1 拍，落下 1 拍",
    f"{b('单腿桥（不稳定面）')}：同上，优势脚踩在不稳定平台中央，保持平台居中",
    f"{b('四点跪伸髋')}：四点跪，膝保持屈 90°，伸髋把脚往天花板抬到髋中立位，2 拍上、2 拍下；左右都测——{b('动的腿')}臀大肌 60%，{b('撑地的腿')}只有约 21%",
]))
A.append(h3("四、单腿负重"))
A.append(pic(10, "单腿蹲、单腿硬拉、滑冰者蹲"))
A.append(ul([
    f"{b('单腿蹲')}：优势腿站立，{mk('慢慢下蹲到臀部碰到 47 cm 高的椅子')}，2 拍下、2 拍上",
    f"{b('单腿硬拉')}：单腿站，背挺直屈髋，用对侧手碰地，2 拍下、2 拍上；腘绳肌紧可微屈膝",
    f"{b('滑冰者蹲')}：单腿站，另一腿伸髋屈膝在后，舒适深度下蹲同时躯干转动，2 拍下、2 拍上；后脚尖可在两次之间点地",
]))
A.append(h3("五、上台阶与摆腿"))
A.append(pic(11, "上台阶、摆腿"))
A.append(ul([
    f"{b('向前上台阶')}：优势腿先迈上 20 cm 台阶，另一腿跟上，再依次下来，每步 1 拍",
    f"{b('侧向上台阶')}：优势腿站在 15 cm 台阶边，慢慢下蹲让另一侧脚跟往地面落，再回到起始位",
    f"{b('动态摆腿')}：单腿站，另一腿屈膝前后摆（屈髋、伸髋各 1 拍），躯干保持直立",
]))
A.append(h3("六、单腿蹲 + 对侧脚画圈"))
A.append(pic(12, "画圈"))
A.append(ul([
    "站在平台旁，优势腿单腿下蹲，同时非优势脚脚尖沿平台外缘画弧（3 拍），再画回站起（3 拍）",
    "允许单手两指扶架子保持平衡；不稳定面版本把脚放在平台上推着画",
    f"{red('不稳定面反而更低')}：臀中肌从 57% 降到 38%",
]))
A.append(h3("七、臀肌夹紧"))
A.append(p(
    f"双脚与肩同宽站立，{b('全力夹紧臀部')} 2 拍、放松 2 拍。臀大肌 81%，排第 2。"
    f"注意这是唯一一个明确口令“全力收缩臀肌”的动作，作者也提醒高分可能和口令有关。"
))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{red('健康年轻人、表面肌电、只看峰值')}：峰值高不等于整个动作都在高强度工作，也不等于长期训练一定长得更多",
    "“70%MVIC 足够增肌”是作者根据别的研究推出来的，并不是本研究验证的",
    "两个动作超过 100%，说明最大等长收缩测试可能没测到真正最大值，或者核心协同收缩抬高了数值",
    "动作标准靠肉眼判断，没有用动作捕捉；单腿蹲按固定椅子高度（47 cm），个子高的人更难",
    "只在 24 人里测了一次，没有报告标准差和统计检验，排名之间很多只差几个百分点",
]))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    "题目和摘要说 18 个动作，表格里是 22 种条件（侧桥、单腿桥、画圈、四点跪各分两种，蚌式分 4 级）",
    "方法写“取中间 3 次重复”，讨论又写“第 5、6、7 次重复”，而正式记录只有 5 次",
    "作者名 Bolgla 在正文多处拼成“Bolga”；摘要“front plank”拼成“font plank”",
    "排除标准“年龄 <21 岁”与“健康受试者可运动 1 小时”并列，但没有报告受试者的年龄、性别等基本资料",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先定目标肌肉，再从低到高排动作')}：早期选蚌式 1、四点跪、单腿桥、侧卧外展；能负重后上台阶、单腿硬拉、滑冰者蹲；最后上侧桥外展、单腿蹲、平板伸髋",
    f"{b('只想练臀中肌')}：蚌式 3、4（伸髋位内旋）比蚌式 1 更“干净”，臀大肌参与很少",
    f"{b('只想练臀大肌')}：试试站立全力夹臀，或平板支撑伸髋",
    "侧卧外展注意脚尖朝前、髋略后伸，避免阔筋膜张肌代偿",
    "单腿桥如果腘绳肌抽筋，说明可能在代偿，要调整姿势或换动作",
    "不稳定面不一定更好：画圈和单腿桥放到不稳定面后，臀肌数值反而下降",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 4、5　22 种动作的 %MVIC 与排名"))
rows = [
    ("侧桥外展（优势腿在下）", 21, "103.11", 1, 21, "70.96", 4), ("侧桥外展（优势腿在上）", 22, "88.82", 2, 22, "72.87", 3),
    ("单腿蹲", 22, "82.26", 3, 22, "70.74", 5), ("蚌式 4", 23, "76.88", 4, 22, "26.22", 19),
    ("平板支撑 + 伸髋", 23, "75.13", 5, 22, "106.22", 1), ("蚌式 3", 22, "67.63", 6, 22, "26.63", 18),
    ("侧卧外展", 23, "62.91", 7, 22, "51.13", 13), ("蚌式 2", 22, "62.45", 8, 22, "12.36", 22),
    ("侧向上台阶", 21, "59.87", 9, 20, "63.83", 7), ("滑冰者蹲", 22, "59.84", 10, 21, "66.18", 6),
    ("骨盆下降", 23, "58.43", 11, 22, "25.10", 20), ("画圈（稳定面）", 23, "57.39", 12, 22, "37.85", 15),
    ("动态摆腿", 22, "57.30", 13, 22, "33.65", 16), ("单腿硬拉", 22, "56.08", 14, 21, "58.84", 9),
    ("单腿桥（稳定面）", 22, "54.99", 15, 21, "54.24", 11), ("向前上台阶", 22, "54.62", 16, 22, "54.67", 10),
    ("单腿桥（不稳定面）", 20, "47.29", 17, 18, "49.35", 14), ("蚌式 1", 22, "47.23", 18, 22, "53.10", 12),
    ("四点跪伸髋（优势腿动）", 23, "46.67", 19, 22, "59.70", 8), ("臀肌夹紧", 23, "43.72", 20, 22, "80.72", 2),
    ("画圈（不稳定面）", 23, "37.88", 21, 22, "28.87", 17), ("四点跪伸髋（非优势腿动）", 23, "22.03", 22, 22, "21.04", 21)]
A.append(table(["动作", "臀中肌 n", "臀中肌 %MVIC", "排名", "臀大肌 n", "臀大肌 %MVIC", "排名"],
               [[r[0], str(r[1]), mk(r[2]) if float(r[2]) >= 70 else r[2], str(r[3]), str(r[4]), mk(r[5]) if float(r[5]) >= 70 else r[5], str(r[6])] for r in rows]))
A.append(tcap("原文表 7　臀中肌：本研究与既往研究对比（%MVIC）"))
A.append(table(["本研究排名", "动作", "本研究", "Distefano", "Bolgla", "Ayotte"], [
    ["1", "侧桥外展（优势腿在下）", "103", "", "", ""], ["2", "侧桥外展（优势腿在上）", "89", "", "", ""],
    ["3", "单腿蹲", "82", "64", "", "52*"], ["4", "蚌式 4", "77", "", "", ""], ["5", "平板支撑 + 伸髋", "75", "", "", ""],
    ["7", "侧卧外展", "63", "81", "42", ""], ["9", "侧向上台阶", "60", "", "", "38"], ["11", "骨盆下降", "58", "", "57", ""],
    ["14", "单腿硬拉", "56", "58", "", ""], ["16", "向前上台阶", "55", "", "", "44"], ["18", "蚌式 1", "47", "40", "", ""]]))
A.append(tcap("原文表 8　臀大肌：本研究与既往研究对比（%MVIC）"))
A.append(table(["本研究排名", "动作", "本研究", "Distefano", "Ayotte"], [
    ["1", "平板支撑 + 伸髋", "106", "", ""], ["2", "臀肌夹紧", "81", "", ""], ["3", "侧桥外展（优势腿在上）", "73", "", ""],
    ["4", "侧桥外展（优势腿在下）", "71", "", ""], ["5", "单腿蹲", "71", "59", "86*"], ["7", "侧向上台阶", "64", "", "56"],
    ["9", "单腿硬拉", "59", "59", ""], ["10", "向前上台阶", "55", "", "74"], ["12", "蚌式 1", "53", "34", ""], ["13", "侧卧外展", "51", "39", ""]]))
A.append(small("* Ayotte 为单腿靠墙蹲。"))
A.append(tcap("原文表 1　Distefano 等的结果（%MVIC，括号内为排名）"))
A.append(table(["动作", "臀大肌", "臀中肌"], [
    ["侧卧髋外展", "39（6）", "81（1）"], ["蚌式（屈髋 30°）", "34（10）", "40（10）"], ["蚌式（屈髋 60°）", "39（6）", "38（12）"],
    ["单腿蹲", "59（1）", "64（2）"], ["单腿硬拉", "59（1）", "58（4）"], ["弹力带侧向走", "27（12）", "61（3）"],
    ["向前弓步", "44（4）", "42（9）"], ["侧向弓步", "41（5）", "39（11）"], ["转身弓步", "49（3）", "48（6）"],
    ["向前单腿跳", "35（8）", "45（8）"], ["侧向单腿跳", "30（11）", "57（5）"], ["转身单腿跳", "35（8）", "48（6）"]]))
A.append(tcap("原文表 2　Bolgla 与 Uhl 的结果（臀中肌 %MVIC）"))
A.append(table(["动作", "臀中肌"], [
    ["骨盆下降", "57"], ["负重位屈髋外展（左）", "46"], ["负重位外展（左）", "42"], ["非负重侧卧外展", "42"],
    ["非负重站立外展", "33"], ["非负重站立屈髋外展", "28"]]))
A.append(tcap("原文表 3　Ayotte 等的结果（%MVIC，括号内为排名）"))
A.append(table(["动作", "臀大肌", "臀中肌"], [
    ["单腿靠墙蹲", "86（1）", "52（1）"], ["小幅单腿蹲", "57（4）", "36（5）"], ["向前上台阶", "74（2）", "44（2）"],
    ["侧向上台阶", "56（5）", "38（3）"], ["后退上台阶", "59（3）", "37（4）"]]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Boren K, Conrey C, Le Coguic J, Paprocki L, Voight M, Robinson TK. Electromyographic analysis of gluteus medius and gluteus maximus during rehabilitation exercises. Int J Sports Phys Ther. 2011;6(3):206-223.</em><br>"
    "原文版权归作者与期刊所有，PDF 未标注知识共享协议。本文仅为学术交流用的中文解读，照片引自原文图 1～18（编者加中文标注，器材标识已模糊），排名图与分层卡为编者中文绘制，表格为编者翻译，如有侵权请联系删除。"
))

TITLE = "「臀肌」练臀中肌、臀大肌，18 个动作谁最出力？（附肌电排行榜与动作图解）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>臀肌肌电推文</title>
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
<div class="by">原创 · 骨科康复小黄</div>
""" + BODY + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
