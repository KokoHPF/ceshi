#!/usr/bin/env python3
"""上胸椎平移式手法对颈痛和颈椎活动度的即时影响（Krauss 等 2008）推文。

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
    "Krauss J, Creighton D, Ely JD, Podlewska-Ely J. The immediate effects of upper thoracic translatoric spinal manipulation on cervical pain and range of motion: a randomized clinical trial. J Man Manip Ther. 2008;16(2):93-99.",
    "作者来自美国奥克兰大学物理治疗项目，属于 Kaltenborn-Evjenth 骨科手法体系",
    "随机临床试验，32 名颈痛患者，只看一次治疗后的即时效果",
], square=True))

A.append(h2("先说为什么颈痛要治胸椎"))
A.append(p(
    f"临床上有个常见思路：{b('一个节段僵硬，会让相邻节段代偿性活动过多而疼痛')}。颈胸交界和上胸椎活动受限被认为是颈痛的危险因素，挥鞭伤患者中上胸椎功能障碍的比例高达 69%。"
))
A.append(p(
    f"已有研究发现胸椎推拿能减轻颈痛和功能障碍，但{b('没有随机对照研究用倾角仪测过颈椎活动度的变化')}。"
    f"这篇用的是 Kaltenborn 和 Evjenth 发展的{mk('平移式脊柱手法')}：短距离、直线、平行或垂直于关节面的推动，作者认为它能恢复关节活动，同时不容易诱发症状。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：19～50 岁、无外伤史、隐匿起病的{b('中颈段（C4～C7）后方疼痛')}，转头时加重；排除胸椎来源症状、系统性疾病、神经根症状、脊髓病和颈椎手术史",
    f"{b('分组')}：32 人（女 26、男 6），信封随机分到手法组 22 人、对照组 10 人；{b('对照组什么都不做')}，在治疗床上坐等相同时间",
    f"{b('评估')}：由不知分组的物理治疗师助理在治疗前后测颈椎左右旋转角度（颈椎活动度测量仪）和转头末端的疼痛（9 点面部表情疼痛量表）",
    "首次检查当天不治疗，1～2 天后复诊时随机分组并完成治疗和复测",
]))

A.append(h2("重点：从定位到手法的完整流程"))
A.append(pic(5, "诊疗流程（编者根据原文整理）"))
A.append(h3("第一步：确认疼痛来自颈椎（症状定位）"))
A.append(pic(2, "原文图 1：颈椎症状定位"))
A.append(ul([
    "让患者主动向疼痛侧转头，转到疼痛加重；再慢慢回转，到疼痛刚好减轻一点的位置",
    "治疗师用胸部和非检查手把头固定在这个位置",
    f"从 {b('C7 开始往上')}，逐节被动旋转椎体（手接触椎板后部和棘突）",
    f"{mk('诱发出与主动转头相同症状的节段')}，其上位椎体就是症状节段",
]))
A.append(h3("第二步：找出僵硬的上胸椎节段（前后向关节游隙测试）"))
A.append(pic(3, "原文图 2：坐位上胸椎前后向关节游隙测试"))
A.append(ul([
    f"患者{b('坐在治疗床上，双臂交叉抱胸')}",
    f"治疗师{b('食指放在待测节段的棘突间隙')}，手掌其余部分在下方节段固定",
    "另一侧手臂绕过患者躯干、从交叉的手臂下方接触前胸和对侧上肢，用手臂和胸部带动患者做前后向平移",
    f"在 {b('T1～T4')} 中找出平移受限的节段；所有入组者都至少有 1 个",
]))
A.append(h3("第三步：平移式手法"))
A.append(pic(4, "原文图 3：上胸椎平移式手法"))
A.append(ul([
    f"对僵硬的上胸椎节段做{b('双侧关节突关节牵引手法')}",
    f"{mk('短距离、被动、直线的推动，方向朝背侧')}：大致垂直于关节突关节面、平行于该节段的椎间盘平面",
    "从图上看，患者仰卧、双臂交叉抱胸，治疗师从上方用身体施力",
    f"原文{red('没有写推几次、用多快的速度、要不要听到弹响')}",
]))

A.append(h2("结果：转头角度多了 7～8°"))
A.append(pic(6, "颈椎旋转角度的即时变化（按原文表 2、表 4 绘制）"))
A.append(ul([
    f"{b('活动度')}：手法组向左转平均增加 {b('7.09°')}、向右转增加 {b('8.23°')}，对照组基本不变；组间差异显著（P = 0.001、0.002）",
    f"{b('疼痛')}：按疼痛方向分成 3 个亚组后，只有{b('双侧转头都痛')}的手法组患者（8 人）疼痛显著下降，组间比较只在向右转时达到 P = 0.05",
    "没有人报告手法后症状加重",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('对照组什么都不做')}：没有假手法，患者知道自己有没有被治疗，期望效应和“被碰了一下”的效果都混在里面，作者自己也承认",
    f"{b('“超过最小可测变化”的结论站不住')}：最小可测变化应该用测量值本身的离散程度来算，原文却用了“变化量”的标准差。按表 1 的基线标准差重算，左转需要约 {red('17°')}、右转约 {red('12°')}，即使改用同一测量者的信度也要 11～13°，平均 7～8° 的改善达不到",
    f"{b('疼痛结论很弱')}：亚组每组只有 2～8 人；面部表情疼痛量表没有公认的最小临床重要差异；而且治疗后是在“新的、更大的转头末端”测疼痛，作者也承认这会低估疼痛改善",
    f"{b('分组不均')}：22 比 10，对照组样本太小",
    f"{b('只看即时效果')}：没有任何随访",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b("“所有人都超过最小可测变化”不可能")}：讨论说手法组全部 22 人的改善都超过最小可测变化（左转 6.82°），又说其中 12 人改善了 10°～30°。若真如此，左转平均值至少约 8.5°，但实际平均只有 7.09°（标准差 5.83°），两种说法无法同时成立；结论里“所有受试者活动度都改善了”也是同样问题",
    f"{b('年龄超出纳入范围')}：纳入标准是 19～50 岁，表 1 手法组年龄却是 16～52 岁",
    f"{b('对照组的符号错了')}：表 2 对照组左转变化写成 −0.6°，但 t 值为正、95% 置信区间（−2.02～3.22）的中心是 +0.6；右转（−0.1°，区间 −1.57～1.77）同样如此",
    f"{b('表号引错')}：正文说最小可测变化的计算见表 3，实际在表 4；说疼痛亚组分析见表 4，实际在表 3",
    f"{b('摘要和结果不一致')}：摘要只说双侧痛患者向右转疼痛改善（P = .05）；结果里组内比较左右都显著（P = .01、.03），组间比较只有右侧（P = .05，且并未小于 0.05）",
    f"{b('统计表述错误')}：“显著性水平设为 0.05%”应为 0.05；用 Levene 检验“正态性”不对，它检验的是方差齐性，而且不能用于性别这种分类变量",
    f"{b('拼写')}：MDC 多处写成“MCD”；摘要“re- and post-intervention”应为 pre-",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('转头受限的颈痛患者，可以查一查上胸椎')}：坐位前后向关节游隙测试简单易学，T1～T4 中常能找到僵硬节段",
    f"{b('先做症状定位，确认是颈椎痛')}：从 C7 往上逐节旋转诱发，排除胸椎来源",
    f"{b('上胸椎平移式手法可以作为增加转头角度的手段')}，即时增加约 7～8°，且没有人加重。但这个幅度可能在测量误差范围内，要结合患者主观感受判断",
    "疼痛改善的证据很弱，不能只靠这一招；手法之后要跟上颈部主动活动和功能训练",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　两组年龄、基线活动度（°）和疼痛评分比较"))
A.append(table(["项目", "组别", "均值", "标准差", "标准误", "95% CI", "最小值", "最大值"], [
    ["年龄", "对照组", "34.20", "9.555", "3.021", "27.37～41.03", "19", "50"], ["", "手法组", "34.95", "10.513", "2.241", "30.29～39.62", "16", "52"],
    ["基线左转", "对照组", "54.80", "12.656", "4.002", "45.75～63.85", "30", "70"], ["", "手法组", "58.95", "14.669", "3.128", "52.45～65.46", "17", "78"],
    ["基线右转", "对照组", "55.80", "11.084", "3.505", "47.87～63.73", "35", "70"], ["", "手法组", "60.41", "15.271", "3.256", "53.64～67.18", "22", "85"],
    ["左转时疼痛", "对照组", "2.50", "2.838", ".898", ".47～4.53", "0", "7"], ["", "手法组", "3.73", "2.707", ".577", "2.53～4.93", "0", "9"],
    ["右转时疼痛", "对照组", "2.80", "1.889", ".597", "1.45～4.15", "0", "5"], ["", "手法组", "2.75", "2.671", ".570", "1.57～3.93", "0", "8"],
]))
A.append(tcap("表 2　颈椎旋转角度的组内变化（°）"))
A.append(table(["组别与方向", "均值", "标准差", "95% CI", "t", "自由度", "P（双侧）"], [
    ["对照组 左转", "−0.6", "3.66", "−2.02～3.22", ".529", "9", ".626"], ["手法组 左转", "7.09", "5.83", "4.52～9.68", "5.71", "21", "< 0.01*"],
    ["对照组 右转", "−0.1", "2.33", "−1.57～1.77", ".136", "9", ".895"], ["手法组 右转", "8.23", "7.41", "4.94～11.51", "5.21", "21", "< 0.01*"],
]))
A.append(tcap("表 3　转头时疼痛的组内变化（9 点面部表情疼痛量表）"))
A.append(table(["亚组", "组别与方向", "均值", "标准差", "95% CI", "t", "自由度", "P"], [
    ["仅右转痛", "对照组 右转", "−.100", ".224", "−.378～.178", "−1.00", "4", ".37"], ["", "手法组 右转", "1.50", "2.88", "−1.52～4.52", "1.28", "5", ".26"],
    ["仅左转痛", "对照组 左转", ".667", "1.16", "−2.20～3.54", "1.00", "2", ".42"], ["", "手法组 左转", ".688", "1.03", "−.176～1.55", "1.88", "7", ".10"],
    ["双侧转头痛", "对照组 右转", "−.500", ".707", "−6.85～5.85", "−1", "1", ".50"], ["", "手法组 右转", "1.38", "1.09", ".461～2.29", "3.56", "7", ".01*"],
    ["", "对照组 左转", "−.500", ".707", "−6.85～5.85", "−1", "1", ".50"], ["", "手法组 左转", "1.63", "1.62", ".270～2.98", "2.84", "7", ".03*"],
]))
A.append(tcap("表 4　倾角仪测量颈椎旋转的信度和反应度"))
A.append(table(["方向", "组内相关系数", "标准差", "测量标准误", "最小可测变化（95%）"], [
    ["右转", ".92", "7.41", "2.09", "5.79"], ["左转", ".82", "5.83", "2.47", "6.82"],
]))
A.append(small("* P < 0.05。表中数字照原文录入，原文的错误见上文。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Krauss J, Creighton D, Ely JD, Podlewska-Ely J. The immediate effects of upper thoracic translatoric spinal manipulation on cervical pain and range of motion: a randomized clinical trial. J Man Manip Ther. 2008;16(2):93-99.</em><br>"
    "原文 PDF 未标注开放许可协议。本文为学术交流用的中文解读：图 1 引自原文（英文标注改为中文），图 2、3 引自原文，诊疗流程卡和活动度变化图为编者根据原文整理绘制，表格为编者翻译。版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「颈痛」转头受限，推上胸椎有用吗？平移式手法随机试验与数据复核"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>上胸椎手法颈痛推文</title>
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
