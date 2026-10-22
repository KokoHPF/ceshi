#!/usr/bin/env python3
"""拇外翻女性 9 种足部训练的足内外在肌肌电激活（Esen 2026 BMC Musculoskelet Disord）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
"""
import pathlib

HERE = pathlib.Path(__file__).parent


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
    "Esen DH, Taş S, Salkın Y, Alcan V. Electromyographic activation of extrinsic and intrinsic foot muscles during nine different foot exercises in women with hallux valgus: a cross-sectional comparative study. BMC Musculoskelet Disord. 2026;27:591. doi:10.1186/s12891-026-09949-w",
    "中文题目：拇外翻女性在 9 种不同足部训练中足外在肌和内在肌的肌电激活：一项横断面比较研究",
    "作者来自土耳其托罗斯大学、梅尔辛大学和塔尔苏斯大学",
    "文章类型：横断面比较研究（按 STROBE 报告），无基金资助",
], square=True))

A.append(h2("研究背景：拇外翻练足，到底在练哪块肌肉"))
A.append(ul([
    "拇外翻是拇趾向外偏、第一跖骨向内移的进行性前足畸形，约 23% 的 18～65 岁成人有，女性更多，常伴疼痛、穿鞋困难、步态和平衡受影响",
    f"肌肉层面：{b('拇展肌')}常变弱；{b('拇长伸肌')}肌腱外移，可能把拇趾往外拉；{b('拇长屈肌')}肌腱变细、走向改变；{b('腓骨长肌')}负责第一跖列跖屈和内侧柱支撑",
    "以往拇外翻的训练研究多集中在短足训练和分趾训练、只看拇展肌；负重、多平面和平衡类训练对内外在肌的作用缺乏比较",
    f"{b('研究目的')}：在拇外翻女性中，比较 9 种常用足部训练时拇展肌、腓骨长肌、拇长屈肌和拇长伸肌的表面肌电；假设负重训练比坐位训练激活更高",
]))

A.append(h2("方法"))
A.append(h3("一、对象"))
A.append(ul([
    "在校园内筛查约 450 只优势足，最终纳入 17 名中重度拇外翻女性（Manchester 分级 ≥ 2 且拇外翻角 ≥ 20°）：年龄 22.2 ± 3.1 岁，BMI 21.5 ± 2.5，拇外翻角 29.6° ± 5.4°，88% 为中度",
    "AOFAS 拇趾评分中位数 70，MOXFQ 总分中位数 39.1",
    "样本量：参考既往拇展肌肌电研究，按配对设计、d = 0.7、α = 0.05、把握度 0.80 估算需 15 人",
]))
A.append(h3("二、9 种训练"))
A.append(pic(2, "原文图 1（英文由编者译成中文覆盖）"))
A.append(ul([
    "训练顺序随机；每种训练先示范、练 1～2 次，正式测 3 次：3～5 秒内逐渐用力到最大、维持 5 秒、2 秒内放松；两次之间休息 2 分钟，两种训练之间休息 10 分钟",
    "没有用仪器测外力，强度靠口令、示范和练习来统一",
]))
A.append(h3("三、肌电采集和分析"))
A.append(pic(3, "原文图 2（肌肉缩写由编者译成中文覆盖）"))
A.append(ul([
    "四通道无线表面肌电（Noraxon Ultium），2000 Hz 采样，10～500 Hz 带通滤波，150 ms 滑动窗 RMS；取 5 秒持续收缩中间 3 秒的平均 RMS，3 次取平均",
    f"{b('幅值没有做最大自主收缩（MVIC）标准化')}，单位是微伏，只能用于同一个人、同一块肌肉在不同训练间的相对比较",
    "统计：每块肌肉用 Friedman 检验比较 9 种训练，显著后用 Wilcoxon 符号秩检验两两比较（效应量 r = Z/√N）；另把训练分为负重（站立短足、单腿短足、提踵、站立摆腿）和非负重两类比较",
]))
A.append(pic(4, "原文图 3（英文由编者译成中文覆盖）"))

A.append(h2("结果"))
A.append(ul([
    "四块肌肉在 9 种训练间的肌电都有显著差异（均 P < 0.001）",
]))
A.append(pic(5, "原文图 4（英文由编者译成中文覆盖）"))
A.append(h3("一、拇展肌：单腿短足、分趾、站立摆腿高，毛巾卷最低"))
A.append(ul([
    f"{b('毛巾卷')}显著低于其余 8 种训练；坐位短足也偏低",
    f"{b('单腿短足')}显著高于坐位短足、站立短足、3DFA-D1E、3DFA-D2E 和提踵；分趾、站立摆腿与它相近",
]))
A.append(h3("二、腓骨长肌：提踵和对角线 1 最高"))
A.append(ul([
    f"{b('提踵')}显著高于其余 8 种训练；{b('3DFA-D1E')}高于除提踵外的 7 种",
    "坐位短足、毛巾卷、分趾最低；单腿短足、3DFA-D2E、站立摆腿居中",
]))
A.append(h3("三、拇长屈肌：毛巾卷、两个对角线和提踵最高"))
A.append(ul([
    f"{b('毛巾卷、3DFA-D1E、3DFA-D2E、提踵')}四者相近且最高；坐位短足和分趾最低；单腿短足和站立摆腿居中",
]))
A.append(h3("四、拇长伸肌：单腿短足最高"))
A.append(ul([
    f"作者报告{b('单腿短足和分趾')}最高；3DFA-D2E 和提踵较低（分趾的说法与表 5 有出入，见下文）",
]))
A.append(h3("五、负重 vs 非负重"))
A.append(ul([
    f"负重训练的拇展肌（P = 0.002）、腓骨长肌（P < 0.001）和拇长伸肌（P = 0.044）激活高于非负重训练；{b('拇长屈肌两类没有差别')}（P = 0.492）",
]))
A.append(pic(6, "编者从原文图 4 估读中位数后整理，只能同一块肌肉内部比较"))

A.append(h2("作者怎么解读"))
A.append(ul([
    "单腿短足和站立摆腿增加了姿势负荷，需要更多内侧前足和拇趾的主动支撑；分趾本身就是拇趾外展动作，所以拇展肌高",
    "提踵和 3DFA-D1E 需要更多负荷传递和踝足稳定，符合腓骨长肌跖屈第一跖列、支撑内侧柱的作用",
    "毛巾卷和提踵对拇趾屈曲的需求大，对角线伸展需要协调稳定拇趾和前足，所以拇长屈肌高；拇长屈肌主要负责推进而不是静态姿势控制，因此负重与否差别不大",
    f"结论：{b('没有一种训练能同时把四块肌肉都练到最优')}，应该组合不同姿势和运动方式的训练；这些都是急性肌电反应，长期效果还需要纵向和干预研究证实",
]))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{b('肌电没有标准化')}：幅值以微伏直接比较，受皮下脂肪、电极位置、皮肤阻抗影响，不能跨人、跨肌肉比较，也说不出“激活到了最大收缩的百分之几”。同类研究多用 %MVIC，如 Kim 等报告轻度拇外翻者分趾训练的拇展肌激活比短足训练高约 45% MVIC（{b('doi:10.3233/BMR-2012-00363')}），Hwang 等报告加压力生物反馈的分趾训练拇展肌达约 90% MVIC（{b('doi:10.3233/BMR-220252')}）",
    f"{b('多重比较没有校正')}：每块肌肉做了 36 次两两 Wilcoxon 检验，四块肌肉共 144 次，却以 P < 0.05 为界；样本量也是按一次配对比较估算的，零星的“显著”要打折扣",
    f"{b('拇长屈肌信号可能不纯')}：它是深层肌，表面电极可能混入趾长屈肌、胫骨后肌的信号，作者也承认",
    f"{b('“收缩强度”难统一')}：要求每种训练都“达到最大收缩并维持 5 秒”，但提踵、站立摆腿本身是动态动作，各训练的发力水平靠口令控制，没有测力",
    f"{b('人群窄')}：17 名年轻女性，88% 为中度；没有健康对照组，看不出这些模式是否为拇外翻特有",
    f"{b('只是急性肌电')}：激活高不等于长期训练能增粗肌肉、矫正外翻角或减轻疼痛",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('拇展肌比较方向写反')}：正文说“3DFA-D1E 的拇展肌激活显著高于分趾训练（P = 0.004）”，但图 4A 中 3DFA-D1E 中位数约 50、分趾约 110，图例也标分趾“显著高于 3DFA-D1E”",
    f"{b('拇长伸肌“分趾最高”与表 5 不符')}：正文和摘要说单腿短足和分趾“显著高于其余 7 种训练（均 P ≤ 0.013）”，但表 5 中分趾与坐位短足（P = 0.055）、站立短足（0.463）、毛巾卷（0.868）、3DFA-D1E（0.227）、站立摆腿（0.981）都无显著差异",
    f"{b('段落复制粘贴')}：拇长伸肌的效应量段落照搬了拇长屈肌的数字（单腿短足 vs 站立摆腿 r = −0.396，3DFA-D2E vs 提踵 r = −0.224）；拇长屈肌段落的 Friedman 统计量写成 χ² = 67.922（这是拇展肌的），前文总述是 92.361",
    f"{b('表内 P 值和效应量矛盾')}：表 3 毛巾卷 vs 分趾 P = 0.795 却 r = −0.878；表 5 3DFA-D1E vs 3DFA-D2E P = 0.840 却 r = −0.419，3DFA-D2E vs 站立摆腿 P = 0.028 却 r = −0.121；还有多处星号与 P 值不符（如 0.002 标一颗星、0.019 标两颗星）",
    f"{b('正文说“其他比较均 P > 0.68”')}，表 2 中却有 0.068、0.093、0.102 等，应为 0.068 的笔误",
    f"{b('单位不一')}：正文说幅值单位是微伏（µV），图 4 纵轴却标毫伏（mV）；图 4C 里的 Δ 和 ¥ 没有图例；图 4B 图例写成“standing ST”",
    f"{b('表 1 中位数落在四分位距外')}：AOFAS 功能分中位数 35，四分位距却写 20～30；量表名也写成“MTF-IP”（应为 MTP-IP）",
    f"{b('图号引错')}：方法写 9 种训练“（Fig. 2）”，图 2 是电极位置，训练示意是图 1",
    f"{b('纳入说法自相矛盾')}：方法说“不论性别都纳入以减少选择偏倚”，实际全部是女性，题目也限定女性",
]))

A.append(h2("落到临床"))
A.append(pic(7, "编者观点"))
A.append(ul([
    f"{mk('想练拇展肌')}：优先单腿短足、站立摆腿、分趾；毛巾卷几乎练不到它，主要是拇长屈肌在出力",
    f"{b('想练第一跖列的“下压”')}：提踵（重心压向拇趾）和三维足踝对角线 1 对腓骨长肌最强，同时也调动拇长屈肌",
    f"{b('进阶顺序可以参考')}：坐位短足 → 站立短足 → 单腿短足 / 站立摆腿，负重越多，拇展肌、腓骨长肌、拇长伸肌越活跃",
    f"{b('别只做一种')}：没有哪个动作能同时练到四块肌肉，按目标组合 3～4 种更合理；这些是即时肌电结果，能否改善外翻角和疼痛还没有证据",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　受试者特征和患者报告结局（n = 17）"))
A.append(table(["项目", "数值"], [
    ["年龄（岁）", "22.24 ± 3.09"], ["身高（cm）", "164.1 ± 6.0"], ["体重（kg）", "57.82 ± 6.54"], ["BMI（kg/m²）", "21.50 ± 2.51"],
    ["优势侧：右 / 左", "15（88.2%）/ 2（11.8%）"], ["拇外翻角（°）", "29.64 ± 5.37"], ["中度（Manchester = 2）/ 重度（= 3）", "15（88.2%）/ 2（11.8%）"],
    ["AOFAS 疼痛", "30（20～30）"], ["AOFAS 功能", "35（20～30）"], ["AOFAS 力线", "8（0～8）"], ["AOFAS 总分", "70（55.50～80.50）"],
    ["MOXFQ 疼痛", "35（7.50～55）"], ["MOXFQ 行走/站立", "39.28（16.06～60.71）"], ["MOXFQ 社交", "12.50（0～31.25）"], ["MOXFQ 总分", "39.06（10.15～47.65）"]]))
A.append(small("注：前 7 项为均值 ± 标准差或人数（%），AOFAS（拇趾跖趾-趾间关节评分）和 MOXFQ（曼彻斯特-牛津足部问卷）为中位数（四分位距）；AOFAS 功能一栏原文如此。"))
EX = ["坐位短足", "站立短足", "单腿短足", "毛巾卷", "分趾", "3DFA-D1E", "3DFA-D2E", "提踵", "站立摆腿"]
PAIRS = [(i, j) for i in range(9) for j in range(i + 1, 9)]
T = {
    "拇展肌": "<0.001 −0.878|<0.001 −0.878|0.007 −0.649|<0.001 −0.821|0.653 −0.109|0.068 −0.442|0.002 −0.752|<0.001 −0.809|0.002 −0.763|<0.001 −0.878|0.868 −0.040|0.031 −0.522|0.407 −0.201|0.831 −0.052|0.068 −0.442|<0.001 −0.878|0.210 −0.304|0.002 −0.740|0.025 −0.546|0.049 −0.476|0.831 −0.052|<0.001 −0.878|0.017 −0.580|<0.001 −0.878|<0.001 −0.844|<0.001 −0.878|0.004 −0.695|0.227 −0.293|0.435 −0.189|0.407 −0.201|0.019 −0.568|0.093 −0.408|0.003 −0.718|0.381 −0.213|0.102 −0.396|0.136 −0.362",
    "腓骨长肌": "0.002 −0.752|<0.001 −0.867|0.463 −0.178|0.407 −0.201|<0.001 −0.740|<0.001 −0.878|<0.001 −0.867|0.002 −0.763|<0.001 −0.855|0.093 −0.408|0.210 −0.304|0.002 −0.763|0.007 −0.660|0.002 −0.752|0.031 −0.522|0.001 −0.798|0.001 −0.798|0.006 −0.672|0.124 −0.373|0.006 −0.672|0.795 −0.063|0.795 −0.878|0.001 −0.878|0.001 −0.878|0.001 −0.878|0.001 −0.878|0.001 −0.878|0.001 −0.878|0.001 −0.878|0.001 −0.878|0.004 −0.695|0.011 −0.614|<0.001 −0.878|0.002 −0.763|0.055 −0.465|<0.001 −0.878",
    "拇长屈肌": "<0.001 −0.878|<0.001 −0.878|<0.001 −0.867|0.193 −0.316|<0.001 −0.878|<0.001 −0.878|<0.001 −0.878|<0.001 −0.867|0.009 −0.637|<0.001 −0.798|0.006 −0.660|<0.001 −0.878|<0.001 −0.878|<0.001 −0.867|0.022 −0.557|0.017 −0.580|<0.001 −0.878|0.006 −0.660|0.006 −0.660|0.006 −0.660|0.103 −0.396|<0.001 −0.867|0.868 −0.040|0.523 −0.155|0.687 −0.098|0.006 −0.660|<0.001 −0.878|<0.001 −0.878|<0.001 −0.878|<0.001 −0.844|0.723 −0.086|0.619 −0.121|0.011 −0.614|0.356 −0.224|0.002 −0.763|0.004 −0.695",
    "拇长伸肌": "0.003 −0.728|<0.001 −0.820|<0.017 −0.442|0.055 −0.355|0.210 −0.231|0.619 −0.121|0.981 −0.014|0.044 −0.497|0.011 −0.614|0.463 −0.178|0.463 −0.178|0.102 −0.396|0.007 −0.649|0.011 −0.614|0.278 −0.257|0.035 −0.515|0.149 −0.352|0.017 −0.442|0.002 −0.566|0.002 −0.566|0.019 −0.568|0.868 −0.040|0.149 −0.352|0.003 −0.728|0.005 −0.684|0.723 −0.086|0.227 −0.293|0.010 −0.603|0.013 −0.602|0.981 −0.014|0.840 −0.419|0.136 −0.362|0.407 −0.201|0.619 −0.121|0.028 −0.121|0.003 −0.718",
}
T = {k: [x.split() for x in v.split("|")] for k, v in T.items()}
A.append(tcap("表 2～表 5　各训练两两比较的 P 值和效应量 r（Wilcoxon 符号秩检验）"))
A.append(table(["比较", "拇展肌 P / r", "腓骨长肌 P / r", "拇长屈肌 P / r", "拇长伸肌 P / r"],
               [[f"{EX[i]} vs {EX[j]}"] + [f"{T[m][n][0]} / {T[m][n][1]}" for m in T] for n, (i, j) in enumerate(PAIRS)]))
A.append(small("注：原文表 2～表 5 按肌肉分 4 张表，编者合并为一张，数值照录（包括正文“原文里对不上的地方”提到的矛盾处）；原文 P < 0.05 加粗并加星号，此处省略。效应量 |r| ≥ 0.10 为小、≥ 0.30 为中、≥ 0.50 为大。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>[1] Esen DH, Taş S, Salkın Y, Alcan V. Electromyographic activation of extrinsic and intrinsic foot muscles during nine different foot exercises in women with hallux valgus: a cross-sectional comparative study. BMC Musculoskelet Disord. 2026;27:591. doi:10.1186/s12891-026-09949-w<br>"
    "[2] Kim MH, Kwon OY, Kim SH, Jung DY. Comparison of muscle activities of abductor hallucis and adductor hallucis between the short foot and toe-spread-out exercises in subjects with mild hallux valgus. J Back Musculoskelet Rehabil. 2013;26(2):163-8. doi:10.3233/BMR-2012-00363<br>"
    "[3] Hwang BH, Jeon IC. Comparison of abductor hallucis muscle activity in subjects with mild hallux valgus during three different foot exercises. J Back Musculoskelet Rehabil. 2024;37(1):47-54. doi:10.3233/BMR-220252</em><br>"
    "本文为中文解读，仅作学术交流：图片引自原文图 1～图 4（图中英文由编者译成中文覆盖原位置），热图和临床卡为编者根据原文整理，表格为编者翻译。原文以 CC BY-NC-ND 4.0 许可发表，版权归原作者所有。"
))

TITLE = "「拇外翻」9 种足部训练肌电对比：毛巾卷几乎练不到拇展肌"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>拇外翻足部训练肌电推文</title>
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
