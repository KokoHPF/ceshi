#!/usr/bin/env python3
"""Schroth 联合脊柱手法治疗青少年特发性脊柱侧凸（Chen & Zhang 2025）推文。

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
    "Chen H, Zhang C. The effect of Schroth Therapy combined with spinal manipulation for the treatment of adolescent idiopathic scoliosis. Pak J Med Sci. 2025;41(2):409-414.",
    "作者来自浙江中医药大学附属温州市中医院（骨科、针灸科）",
    "单中心回顾性研究（不是随机对照试验）",
], square=True))

A.append(h2("先说为什么要把这两样放在一起"))
A.append(p(
    f"青少年特发性脊柱侧凸（AIS）占所有脊柱侧凸的 80%～85%，10～18 岁青少年里大约每 25～50 人就有 1 个。"
    f"度数不大的孩子，保守治疗里最常见的是{b('Schroth 练习')}：用三维旋转呼吸、体位摆放和针对性的矫正动作，让孩子学会自己把弯“撑回来”。"
))
A.append(p(
    f"国内中医院还常给这些孩子做{b('推拿、整骨类的脊柱手法')}，松解侧凸处紧张的软组织、调整脊柱。"
    f"两样合起来做，是不是比单做 Schroth 更好？这篇就是{mk('翻病历，把“Schroth + 手法”和“单做 Schroth”的孩子各挑 50 个来比')}。"
))

A.append(h2("怎么做的"))
A.append(ul([
    "2023 年 1 月到 2024 年 2 月，温州市中医院 150 名接受 Schroth 治疗（加或不加手法）的 AIS 孩子",
    f"纳入：全脊柱 X 线确诊，{b('10～13 岁')}，{b('Cobb 角 10°～20°')}（轻度），资料完整",
    "排除：染色体异常、周围神经或肌肉病变、蝴蝶椎/半椎体/脊髓空洞、生长发育障碍、明显足和下肢畸形、非特发性侧凸",
    f"按性别配对后，{b('研究组')}（Schroth + 手法）和{b('对照组')}（单做 Schroth）各 50 人",
    "治疗前和治疗 6 个月后各评估一次",
]))

A.append(h2("重点：两组到底做了什么"))
A.append(pic(4, "两组方案一览（编者根据原文整理）"))
A.append(h3("Schroth 练习（两组都做）"))
A.append(p(
    f"第一次课先学 Schroth 的基本原则：{b('三维旋转呼吸')}、骨盆矫正、牵伸、基本张力和体位摆放；"
    f"同一节课里接着练肩部反向牵引、肌肉圆柱、侧方悬挂、帆式、突髋和 Schroth 步态。"
    f"{mk('每次 90 分钟，每周 3 次，连续 6 个月')}。原文图 1 给了十个练习的照片："
))
A.append(pic(2, "原文图 1（上排）：① 旋转呼吸与伸展；② 侧卧位肩部反向牵引；③ 侧卧位“肌肉圆柱”；④ 帆式练习（编者裁切重排，字母标注改为中文）"))
A.append(pic(3, "原文图 1（下排）：⑤ 半跪位“肌肉圆柱”；⑥ 坐球练习；⑦ 侧方悬挂；⑧ 俯卧位肩部反向牵引；⑨ 突髋练习；⑩ Schroth 步态练习"))
A.append(p(
    f"几个练习的意思简单说一下：{b('“肌肉圆柱”')}是侧卧或半跪时把躯干绷成一根“圆柱”，抵抗重力不塌；"
    f"{b('肩部反向牵引')}是把凸侧肩和凹侧骨盆往相反方向拉长；{b('突髋练习')}针对腰段侧弯时骨盆往一侧突出的问题；"
    f"{b('Schroth 步态')}是把矫正后的姿势带到走路里。所有动作都配合{red('往凹侧“吸气撑开”的旋转呼吸')}。"
))
A.append(h3("脊柱手法（只有研究组做，每周 2 次，6 个月）"))
A.append(ul([
    f"{b('① 点穴按摩（约 5 分钟）')}：沿足太阳膀胱经和督脉自上而下按压，督脉从大椎一直到尾骶；重点按委中、气海、命门、殷门、环跳，约每分钟 40 次",
    f"{b('② 解痉理筋（10 分钟）')}：先让孩子站着，找出侧凸处最紧张、痉挛的肌肉和韧带；再俯卧，用掌根滚法、肘揉、振法松解脊柱两侧",
    f"{b('③ 整骨手法（约 5 分钟）')}：在侧弯处依次推、拉肌肉和棘突，动作轻柔连贯，力度以孩子能忍受为准",
    f"{b('④ 旋转扳法（1 分钟 × 2 次）')}：孩子俯卧放松，治疗师站在侧凸一侧，{mk('一手按住腰部命门，一手拉肩，两手同时用力，把脊柱旋转、伸展到最大')}",
    f"{b('⑤ 抖动放松（2 分钟）')}：固定腰部，双手轻轻抖动肩部",
]))
A.append(p(
    f"算下来，研究组每周比对照组{red('多了 2 次、每次 20 多分钟的一对一手法')}。这一点后面讲可信度时还会提到。"
))

A.append(h2("看了哪些指标"))
A.append(ul([
    f"{b('疗效分级')}（看全脊柱 X 线上的 Cobb 角）：显效 = Cobb 角 ≤ 10° 或减少 ≥ 5°；有效 = 减少 ≤ 5°；无效 = 不变或加重。显效 + 有效 = 总有效率",
    f"{b('最大 Cobb 角')}和{b('锁骨角')}（两侧锁骨最高点连线与水平线的夹角，反映肩是否平）",
    f"{b('躯干旋转角（ATR）')}：用脊柱侧弯测量尺（Scoliometer）在前屈位测",
    f"{b('椎体旋转')}：Nash-Moe 法",
    f"{b('腰椎前屈、后伸活动度')}：用量角器测",
]))

A.append(h2("结果：两组都变好，加手法的更多一点"))
A.append(ul([
    f"基线：两组性别、年龄、体重、身高、侧弯部位、Risser 征都没有统计学差异",
    f"总有效率：{mk('研究组 96%，对照组 84%')}（P = 0.046）",
    "治疗 6 个月后，两组的最大 Cobb 角、锁骨角、ATR 和椎体旋转都比治疗前小，研究组更小",
    "两组腰椎前屈、后伸都比治疗前大，研究组更大",
]))
A.append(pic(5, "原文图 2 重绘：最大 Cobb 角和锁骨角。研究组从约 15° 降到约 9°，对照组从约 14° 降到约 10.5°（数值为编者按原图估读）"))
A.append(pic(6, "原文图 3 重绘：躯干旋转角（ATR）和椎体旋转"))
A.append(pic(7, "原文图 4 重绘：腰椎后伸和前屈活动度"))
A.append(p(
    f"注意：原文{b('只给了柱状图，没有给出任何具体的均值、标准差和 P 值')}，上面三张图里的数字是编者按原图估读的，"
    f"两组之间的差距大概是 Cobb 角 1.5°～2°、ATR 0.6° 左右。"
))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('回顾性、非随机')}：哪些孩子加手法是临床上定的，可能本身就有差别（比如家长依从性更好、更愿意来医院）。原文自己也承认样本小、没做样本量计算",
    f"{b('剂量不对等')}：研究组每周多 2 次一对一治疗，多出来的接触时间、关注度和期望效应都可能让结果更好看，没法单独归功于“手法”",
    f"{b('差距在测量误差以内')}：Cobb 角的测量误差一般就有 3°～5°，两组治疗后差不到 2°，ATR 差 0.6° 左右，{red('临床上很难说有实际意义')}",
    f"{b('疗效标准很宽松')}：入组 Cobb 角本来就是 10°～20°，“减少 ≤ 5°”就算“有效”，量出来少 1°～2° 也算，所以两组总有效率都很高",
    f"{b('没盲法')}：没说谁量的 X 线和 ATR，评估者知不知道分组",
    f"{b('只随访 6 个月')}：AIS 要一直管到骨骼成熟，6 个月的变化说明不了能否阻止进展",
    f"{b('人群窄')}：只有 10～13 岁、轻度（10°～20°）的孩子，中重度、需要支具的情况不能套用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“按性别配对”但性别并不平衡')}：方法里说按性别配对后各取 50 人，表 1 里却是研究组男/女 21/29、对照组 27/23",
    f"{b('年龄中位数落在四分位数范围外')}：对照组年龄写成“11（12～13）”岁，中位数 11 不可能比下四分位数 12 还小",
    f"{b('百分比算错')}：表 1 研究组“胸腰段 24 例（45.00%）”，24/50 应为 48%",
    f"{b('Risser 征的卡方值复核不上')}：按表 1 的人数算，χ² ≈ 0.70、P ≈ 0.87，原文写的是 1.347 和 0.718（结论不变，但数字对不上）；另外 Risser 征是分级，原文写成了“0°、I°…”",
    f"{b('总有效率的 P 值卡在边上')}：96% vs 84% 用普通卡方确实是 χ² = 4.000、P = 0.046，但对照组“无效”的期望频数刚好只有 5，"
    f"{red('用连续性校正后 P ≈ 0.096，Fisher 确切检验 P ≈ 0.092，都不显著')}",
    f"{b('疗效标准互相重叠')}：“显效”包括“减少 ≥ 5°”，“有效”是“减少 ≤ 5°”，正好减少 5° 两边都能归；“减少 ≤ 5°”字面上也包括 0°，又和“无效 = 不变”冲突",
    f"{b('椎体旋转的单位')}：Nash-Moe 法是按椎弓根位置分 0～4 级的分级方法，不是测角度，原文图 3 却用“°”标注，数值也只有 1～2",
    f"{b('结果只有图、没有数')}：Cobb 角、ATR、活动度等主要结果都没给均值、标准差、t 值和 P 值，没法复核",
    f"{b('体位描述前后矛盾')}：解痉时已经让孩子俯卧，整骨后又写“扶孩子转成俯卧位”；另外气海穴在下腹部，和俯卧位、沿背部经络按压的描述也不太对得上",
    f"{b('图 1⑦ 标的是“侧方悬挂”')}，照片里却是孩子跪坐、手搭在肩上，看不出“悬挂”",
    f"{b('讨论引用对不上')}：讨论说 Stępnik 等的研究是在“呼吸系统疾病患者”身上做手法，但该参考文献的标题写的是在{b('健康人')}身上做的",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('Schroth 本身是主角')}：两组都做了 6 个月、每周 3 次、每次 90 分钟的 Schroth，两组 Cobb 角都降了 4°～6°，这个量和以往 Schroth 研究差不多",
    f"手法可以作为{b('辅助')}，用来松解侧凸处紧张、疼痛的软组织，让孩子更舒服地练；但单靠这篇，{red('说不出手法能额外“矫正”多少度')}",
    "给孩子做旋转扳法要格外小心：这篇没报告任何不良事件，也没写排除标准里是否筛查过手法禁忌",
    "轻度 AIS 的核心仍然是：规律的特异性练习 + 按时复查 X 线 + 达到支具指征时及时上支具",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　两组基线资料比较"))
A.append(table(["项目", "研究组（n = 50）", "对照组（n = 50）", "t / χ²", "P"], [
    ["男/女", "21/29", "27/23", "1.442", "0.230"],
    ["年龄（岁）", "12（12～13）", "11（12～13）", "−1.255", "0.210"],
    ["体重（kg）", "37.92 ± 10.77", "35.86 ± 11.69", "0.916", "0.362"],
    ["身高（cm）", "147.74 ± 9.62", "146.92 ± 13.08", "0.357", "0.722"],
    [b("侧弯部位 [n（%）]"), "", "", "1.990", "0.370"],
    ["胸段", "17（34.00）", "14（28.00）", "", ""],
    ["胸腰段", "24（45.00）", "21（42.00）", "", ""],
    ["下腰段", "9（18.00）", "15（30.00）", "", ""],
    [b("Risser 征 [n（%）]"), "", "", "1.347", "0.718"],
    ["0 级", "4（8.00）", "6（12.00）", "", ""],
    ["Ⅰ 级", "13（26.00）", "13（26.00）", "", ""],
    ["Ⅱ 级", "18（36.00）", "15（30.00）", "", ""],
    ["Ⅲ 级", "15（30.00）", "16（32.00）", "", ""],
]))
A.append(small("年龄为中位数（四分位数范围），其余计量资料为均值 ± 标准差。表中数字照原文录入，原文的错误见上文。"))
A.append(tcap("表 2　两组疗效比较 [n（%）]"))
A.append(table(["组别", "n", "显效", "有效", "无效", "总有效"], [
    ["研究组", "50", "29（58.00）", "19（38.00）", "2（4.00）", "48（96.00）"],
    ["对照组", "50", "22（44.00）", "20（40.00）", "8（16.00）", "42（84.00）"],
]))
A.append(small("总有效率比较：χ² = 4.000，P = 0.046。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Chen H, Zhang C. The effect of Schroth Therapy combined with spinal manipulation for the treatment of adolescent idiopathic scoliosis. Pak J Med Sci. 2025;41(2):409-414. doi:10.12669/pjms.41.2.11355</em><br>"
    "原文以 CC BY 3.0 协议开放获取。本文为学术交流用的中文解读，图 1 引自原文（编者裁切重排、标注改为中文），图 2～4 为编者按原文柱状图估读重绘，方案卡为编者整理绘制，附录表格为编者翻译整理。"
))

TITLE = "「脊柱侧弯」Schroth 加上推拿整骨，效果更好吗？100 例青少年回顾"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>Schroth联合手法推文</title>
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
