#!/usr/bin/env python3
"""动力链募集与前锯肌激活：前出拳加强（Kaur 等 2020）推文。

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
    "Kaur N, Bhanot K, Ferreira G. Effects of lower extremity and trunk kinetic chain recruitment on serratus anterior muscle activation during forward punch plus exercise on stable and unstable surfaces. Int J Sports Phys Ther. 2020;15(1):126-138. doi:10.26603/ijspt20200126",
    "作者单位：美国圣奥古斯丁健康科学大学（奥斯汀校区）物理治疗系",
    f"研究类型：{b('描述性、受试者内重复测量的表面肌电研究')}，21 名健康男性",
], square=True))

A.append(h2("先说为什么要把腿和躯干加进前锯肌训练"))
A.append(p(
    f"前锯肌把肩胛骨稳定在胸廓上，是维持{b('正常肩肱节律')}的关键肌肉之一；肩上回旋、后倾、外旋不足与肩峰下撞击等问题有关，而肩部问题患者的前锯肌常常偏弱。"
    f"所以前锯肌的运动控制和力量训练是肩部康复的重点。"
))
A.append(p(
    f"肩复合体靠全身多节段协同。肌筋膜上，前锯肌是{mk('“塞拉佩效应”（serape effect）')}的一环：前锯肌—同侧菱形肌—腹外斜肌—对侧腹内斜肌—大腿内收肌像一条斜挎的披肩连在一起；"
    f"前锯肌还在肩胛下角附近与背阔肌相连，再经胸腰筋膜间接连到双侧臀大肌。作者之前已发现：在稳定地面上做前出拳加强时加入躯干和下肢，前锯肌激活更高。"
))
A.append(p(
    f"临床上还常用平衡垫、BOSU 球等{b('不稳定平面')}“增加难度”，但研究结论不一。这篇要回答两个问题：{b('① 在不稳定平面上，加入躯干和下肢动力链还能不能提高前锯肌激活？② 平面变不稳定后，前锯肌激活会不会变？')}"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：21 名健康男性，平均 26.7 岁，体脂率 12%（为减少脂肪对表面肌电的干扰，只招体脂“一般到很瘦”的人）；样本量按中等效应量（f = 0.25）、检验效能 0.80 计算需要 19 人",
    "排除：身体任何部位疼痛、神经肌肉或骨关节疾病、上肢活动受限、半年内上下肢损伤、颈背或四肢手术史、每周上肢力量训练超过 5 小时、支撑腿慢性踝关节不稳",
    f"{b('肌电')}：优势侧前锯肌（下部纤维）、背阔肌、腹外斜肌，非优势侧大腿内收肌，双侧臀大肌；按最大自主等长收缩（MVIC）标准化为 %MVIC",
    "前锯肌 MVIC：坐在床边，测试侧上肢上举 125°，检查者一手放上臂、一手放肩胛外缘，向下施力让受试者对抗",
    f"{b('统计')}：双因素重复测量方差分析（平面 × 动作），再按平面分别做单因素重复测量方差分析和 Sidak 事后比较",
]))

A.append(h2("重点：三个动作怎么做"))
A.append(pic(2, "六个动作（编者根据原文整理）"))
A.append(pic(3, "原文图 1～3：稳定平面上的三个动作"))
A.append(pic(4, "原文图 4～6：BOSU 球上的三个动作"))
A.append(ul([
    f"{b('前出拳加强（FPP）')}：起始双脚平行站立，优势侧屈肘 90°、前臂中立放在体侧；肩前屈到 90°、伸肘、肱骨内旋 45°，同时{mk('把肩胛向前“送出去”')}，再原路收回",
    f"{b('闭链塞拉佩（CS）')}：出拳同时{b('躯干转向对侧')}，{b('对侧腿屈髋内收、向前迈步越过身体中线落地')}；步长统一为腿长（髂前上棘到内踝）的 75%，地面用胶带标出",
    f"{b('开链塞拉佩（OS）')}：出拳同时躯干转向对侧，对侧腿屈髋内收、向前摆过中线但{b('不落地')}，单腿保持平衡",
    "每次都要尽全力出拳，拳头碰到最大够距处的标记，保证肩胛充分前伸；节拍器 50 次 / 分钟，出拳 1 拍、收回 1 拍",
    "每个动作做 3 次，次间至少休息 5 秒；不同动作之间至少休息 2 分钟；6 个动作顺序随机",
]))

A.append(h2("结果（压缩版）"))
A.append(pic(5, "六块肌肉的平均肌电（编者根据原文表 2～7 绘制）"))
A.append(ul([
    f"{b('加入动力链有效')}：两种平面上，{mk('前锯肌在 CS 和 OS 中的激活都显著高于单纯 FPP')}（稳定平面：85.5% → 132.5% / 160.7% MVIC）；腹外斜肌、内收肌、同侧臀大肌也一样",
    "对侧臀大肌只有 CS 显著高于 FPP，OS 不显著；背阔肌三个动作之间没有差异",
    "CS 和 OS 之间，只有内收肌有差异（OS 更高）",
    f"{b('不稳定平面没用')}：所有肌肉在稳定和不稳定平面之间都没有差异（平面主效应 P = 0.835，交互作用 P = 0.714）",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('只是健康年轻男性的肌电')}：不能直接推到肩痛患者、女性或其他年龄段；肌电高也不等于训练效果更好",
    f"{b('前锯肌超过 100% MVIC')}：CS、OS 中前锯肌达到 130%～160% MVIC，说明所用的 MVIC 测试姿势很可能没有诱发出真正的最大收缩；作者也承认这一点，所以数值只能在本研究内部比较",
    f"{b('变异很大')}：内收肌在 OS 中的标准差（101～141）甚至大于均值，个体差异非常大",
    f"{b('表面肌电的局限')}：电极位置、串扰（前锯肌和背阔肌离得很近）、动态动作中的伪迹都会影响结果",
    f"{b('“不稳定平面没用”只针对 BOSU 和这三个动作')}：作者认为 BOSU 带来的不稳定可能不够，换其他平面或更动态的动作结论可能不同",
    "作者给研究定的证据等级是 2b，但这是实验室肌电描述性研究，不是疗效研究",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('摘要说得太满')}：摘要说“除背阔肌外，所有肌肉在 CS 和 OS 中都显著高于 FPP”，但表 5 中对侧臀大肌 OS 与 FPP 的比较 P = 0.549（稳定）和 0.223（不稳定），并不显著；正文结果部分自己也写了这一点",
    f"{b('背阔肌的 F 值和 P 值对不上')}：不稳定平面 F = 4.8、P = 0.074。按 21 人、3 个动作（自由度 2, 40），F = 4.8 对应 P ≈ 0.013；即使做了球形校正，也很难到 0.074",
    f"{b('“除背阔肌外”的统计量含糊')}：结果写“除背阔肌外，所有肌肉在动作之间都有差异（F = 12.7，P &lt; 0.001）”，只给了一个 F 值，不知道是哪块肌肉的",
    f"{b('引用了不存在的表')}：结果部分说对侧臀大肌的差异见“表 1～6”，但表 1 是纳入 / 排除标准，肌电数据在表 2～7",
    f"{b('表 2 星号标注不一致')}：不稳定平面的 CS、OS 均值后面也加了 *（138.40*、157.39*），稳定平面没有加，而 P 值列已经标了显著性",
    f"{b('图 5 用了两个 BOSU')}：照片中迈步脚落在第二个 BOSU 上，方法部分只说在 BOSU 上做，没有说明迈步落点也是不稳定平面",
    f"{b('站姿描述不一致')}：动作描述是“双脚平行站立”，后文又说“双脚与髋同宽站在两种平面上”；单个 BOSU 上如何完成向前迈 75% 腿长的一步，没有交代",
    f"{b('样本量计算参数不清')}：“自由度 = 6”与 2 × 3 的重复测量设计对不上",
    f"{b('小错')}：“two of its’ variations”“thoraco-lumbar fasci”“reccomended”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('想多练前锯肌，就把腿和躯干带上')}：在前出拳加强的基础上加躯干对侧旋转和对侧腿迈步（CS）或摆腿（OS），前锯肌激活明显更高",
    f"{b('动作要点')}：出拳到底后继续把肩胛向前送；肱骨内旋约 45°；用节拍器控制速度（出拳 1 拍、收回 1 拍）",
    f"{b('CS 更稳、OS 更难')}：OS 要单腿平衡，内收肌参与更多；可以从 FPP → CS → OS 进阶",
    f"{b('别迷信 BOSU')}：加个不稳定平面不一定提高肌肉激活，想提高难度，先考虑加动力链、负荷或速度",
    f"{b('结合患者情况')}：这是健康人的肌电数据，用于肩痛患者时仍要看疼痛、代偿和功能反应",
]))

A.append(h2("附录：原文表格（中文翻译）"))
A.append(table(["纳入标准", "排除标准"], [
    ["• 男性<br>• 18～40 岁<br>• 按 ACSM《运动测试与处方指南》，年龄相关体脂率处于“一般”到“很瘦”",
     "• 目前身体任何部位疼痛<br>• 任何神经肌肉疾病、关节或骨疾病<br>• 上肢活动受限（目测）<br>• 近 6 个月内上肢或下肢损伤<br>• 颈、背、上肢或下肢手术史<br>"
     "• 每周上肢力量训练超过 5 小时<br>• 支撑腿慢性踝关节不稳史（用踝关节不稳量表判定）"],
], first_bold=False))
A.append(tcap("原文表 1：纳入 / 排除标准（中文翻译）"))
A.append(small("ACSM：美国运动医学会。"))


def emg(n, name, rows):
    A.append(table(["动作", "均值（%MVIC）", "标准差", "95% CI（下限～上限）", "P 值"],
                   [["<b>稳定平面</b>", "", "", "", ""]] + rows[:3] + [["<b>不稳定平面</b>", "", "", "", ""]] + rows[3:], first_bold=False))
    A.append(tcap(f"原文表 {n}：三个动作中{name}的平均肌电激活（中文翻译）"))


emg(2, "前锯肌", [["FPP", "85.50", "43.17", "65.85～105.15", ""], ["CS", "132.54", "86.97", "92.95～172.13", "0.034*"], ["OS", "160.65", "100.95", "114.70～206.60", "0.001*"],
                  ["FPP", "84.98", "37.70", "67.819～102.14", ""], ["CS", "138.40*", "94.33", "95.46～181.33", "0.03*"], ["OS", "157.39*", "110.23", "107.21～207.57", "0.007*"]])
emg(3, "腹外斜肌", [["FPP", "52.08", "21.81", "42.15～62.01", ""], ["CS", "78.75", "32.61", "63.90～93.59", "0.001*"], ["OS", "92.68", "34.04", "77.18～108.17", "0.001*"],
                    ["FPP", "53.83", "25.87", "42.05～65.60", ""], ["CS", "85.87", "33.99", "70.40～101.34", "0.001*"], ["OS", "87.79", "37.94", "70.52～105.06", "0.001*"]])
emg(4, "大腿内收肌", [["FPP", "14.87", "13.11", "8.90～20.834", ""], ["CS", "67.34", "67.06", "36.82～97.87", "0.002*"], ["OS", "111.52", "101.71", "65.21～157.81", "0.001*"],
                      ["FPP", "33.92", "52.57", "9.99～57.85", ""], ["CS", "73.00", "88.76", "32.60～113.41", "0.003*"], ["OS", "110.82", "140.68", "46.78～174.86", "0.003*"]])
emg(5, "对侧臀大肌", [["FPP", "12.27", "12.93", "6.39～18.16", ""], ["CS", "16.27", "13.38", "10.18～22.36", "0.001*"], ["OS", "13.41", "10.07", "8.82～17.99", "0.549"],
                      ["FPP", "10.12", "5.78", "7.49～12.75", ""], ["CS", "14.07", "9.02", "9.97～18.18", "0.04*"], ["OS", "12.53", "7.34", "9.19～15.87", "0.223"]])
emg(6, "同侧臀大肌", [["FPP", "15.91", "7.00", "12.72～19.09", ""], ["CS", "25.16", "12.63", "19.41～30.91", "0.002*"], ["OS", "33.20", "19.69", "24.23～42.16", "0.001*"],
                      ["FPP", "16.70", "7.47", "13.30～20.10", ""], ["CS", "22.46", "9.69", "18.05～26.87", "0.002*"], ["OS", "31.18", "20.50", "21.85～40.51", "0.001*"]])
emg(7, "背阔肌", [["FPP", "41.63", "28.03", "27.69～55.57", ""], ["CS", "43.8", "29.3", "29.24～58.39", "0.957"], ["OS", "57.27", "42.27", "36.24～78.29", "0.146"],
                  ["FPP", "37.03", "18.07", "28.05～46.02", ""], ["CS", "39.79", "20.62", "29.53～50.05", "0.785"], ["OS", "54.32", "42.56", "33.15～75.79", "0.074"]])
A.append(small("FPP：前出拳加强；CS：闭链塞拉佩效应 FPP；OS：开链塞拉佩效应 FPP。* P ≤ 0.05。P 值为与 FPP 比较的结果。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Kaur N, Bhanot K, Ferreira G. Effects of lower extremity and trunk kinetic chain recruitment on serratus anterior muscle activation during forward punch plus exercise on stable and unstable surfaces. Int J Sports Phys Ther. 2020;15(1):126-138. doi:10.26603/ijspt20200126</em><br>"
    "原文 PDF 中未标注开放许可协议，版权归原作者和出版方所有。本文为学术交流用的中文解读：原文图 1～6 引自原文并加中文图注，表 1～7 为中文翻译，动作卡和肌电结果图为编者根据原文整理绘制。如有侵权请联系删除。"
))

TITLE = "「肩」前锯肌怎么练才更“上劲”？出拳加转体迈步，BOSU 反而没用"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>前锯肌动力链推文</title>
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
