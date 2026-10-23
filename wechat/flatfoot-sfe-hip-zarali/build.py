#!/usr/bin/env python3
"""扁平足短足练习加髋外展推文：生成 article_body.html 与 preview.html。

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
    "Zarali A, Raeisi Z, Aminmahalati A. The effects of combined exercises, short foot exercises, and short foot exercises with isometric hip abduction on navicular drop, static parameters, and postural sway in women with flat foot: a randomized trial. BMC Sports Sci Med Rehabil. 2024;16:233.",
    "作者来自伊朗阿拉克大学运动康复系",
    "随机、单盲试验，伊朗临床试验注册号 IRCT20220409054456N",
], square=True))

A.append(h2("先说为什么要把髋也带上"))
A.append(p(
    f"柔韧性扁平足：站着时内侧纵弓塌下来、坐着又能恢复。它会让足过度旋前，和足底筋膜炎、姆外翻、髌股痛、腰痛等都有关系，平衡也更差。"
))
A.append(p(
    f"{b('短足练习')}是练足内在肌的经典动作：脚趾不弯，把第 1 跖骨头往脚跟方向收，让足弓拱起来。"
    f"扁平足的人姆展肌往往偏弱，做短足时{b('胫前肌容易代偿')}。Choi 等的肌电研究发现，做短足时{mk('膝上套弹力带、同时向外撑（等长髋外展）')}，"
    "胫前肌代偿更少、姆展肌激活更多。这篇就是把这个“即时效果”做成 6 周训练，看是不是更有用。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：{b('45 名')}女大学生，18～28 岁，体重指数 18～25，{b('舟骨下沉 &gt; 10 毫米')}（柔韧性扁平足），近半年无下肢或腰部损伤",
    "随机分三组，每组 15 人；评估者和数据分析者不知道分组",
    f"三组都是{b('每周 6 次 × 6 周')}（3 次有治疗师指导、3 次在家按指导单自己练），每 2 周升一级，每次约 30 分钟逐渐加到 45 分钟",
    "测量（只测优势脚）：舟骨下沉（Brody 法，坐位和站立位舟骨结节高度差）；足底压力板上单腿站 30 秒，记录足底接触面积、足轴旋转角、最大压力，以及压力中心的前后、内外侧晃动、轨迹长度、晃动面积和平均速度",
]))
A.append(pic(6, "受试者流程"))

A.append(h2("重点：三套练法"))
A.append(pic(2, "三组对比"))
A.append(h3("短足练习（两组短足组共用）"))
A.append(p(f"4 个动作：{b('脚趾分开、伸其余四趾、足弓拱起（短足）、伸姆趾')}。每 2 周换体位、加时间："))
A.append(pic(3, "进阶"))
A.append(h3("短足 + 等长髋外展"))
A.append(ul([
    f"在{b('膝关节上方')}套一圈弹力带",
    f"做每个短足动作时，{mk('双膝同时向外撑住弹力带，但不真正移动')}（等长髋外展）",
    "同样从坐位 → 双脚站 → 单脚站（单脚站时套带的那条腿抬起，支撑腿做短足）",
]))
A.append(pic(5, "原文图 3"))
A.append(h3("综合练习"))
A.append(p("按 2 周一档换动作（详见文末附录表 1），每个动作 10 次 × 3 组，收缩时间 5 → 8 → 10 秒："))
A.append(ul([
    f"{b('第 1～2 周')}：脚趾分开、伸姆趾、伸其余四趾；脚趾夹小物件；滚网球；毛巾套脚跟往回拉；用脚写字母；扶椅背单脚抬起",
    f"{b('第 3～4 周')}：侧卧髋外展；脚趾夹玻璃珠放到别处；脚趾卷毛巾；弹力带勾脚、踩脚；跟腱牵伸（直膝、屈膝）",
    f"{b('第 5～6 周')}（加弹力带）：下肢和足的 4 种对角线模式；弹力带内外翻；稳定面和不稳定面上保持平衡",
]))
A.append(pic(4, "原文图 2"))

A.append(h2("结果：三组都好转，加髋外展的最明显"))
A.append(pic(7, "主要结果"))
A.append(ul([
    f"{b('舟骨下沉')}：三组都减少；{mk('短足 + 髋外展组 11.26 → 6.28 毫米')}，治疗后显著少于综合练习组（P = 0.022）",
    f"{b('单腿站晃动')}：短足两组所有压力中心指标都下降；综合练习组前后晃动没有显著变化（P = 0.065）。治疗后{b('内外侧晃动')}短足 + 髋外展组显著低于综合练习组（P = 0.035）",
    f"{b('足底参数')}：三组足底接触面积和足轴旋转角都下降；最大压力只有两组短足组下降，综合练习组没变（P = 0.616）",
    "其余组间比较都没有统计学差异，但变化百分比基本是：短足 + 髋外展 &gt; 短足 &gt; 综合练习",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{red('样本小、只有年轻女性')}：每组 15 人，18～28 岁女大学生，不能直接推到男性、中老年或有症状的人",
    f"{red('只看了足和平衡指标')}：没有疼痛、功能或长期随访；舟骨下沉减少几毫米到底有没有临床意义，没有讨论",
    "没有不训练的对照组，6 周的改善有多少来自练习本身、多少来自学会了怎么站，无法区分",
    "综合练习组里也有脚趾分开、伸趾、侧卧髋外展等，和短足组有重叠，三组差别没那么“干净”",
    "大多数组间比较没有差异，作者多处用“变化百分比更高”来支持结论，说服力有限",
]))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    f"表 4 内外侧晃动：短足 + 髋外展组 108.38 → 69.13 毫米，实际下降约 {b('36%')}，表里却写 {red('56.77%')}；舟骨下沉同组 11.26 → 6.28，实际约 44%，表里写 40.14%",
    "效应量和正文对不上：正文说前后晃动交互作用效应量 0.378、内外侧 0.229，表 4 正好相反；按 F 值反算，内外侧晃动（F = 3.94）的效应量约 0.16，不是 0.378；轨迹长度组间 F = 0.35，效应量却写 0.205",
    "摘要写舟骨下沉组间比较 P = 0.22，结果部分写 0.022",
    f"讨论里说“{b('本研究中')}坐位和站立位短足加髋外展时胫前肌活动显著降低”，但本研究没测肌电，这是 Choi 等的结果",
    "最大压力单位写成牛顿（N），数值约 8～11，作为单腿站的压力明显偏低，单位可能有误",
    "表 4 内外侧晃动标准差写成“17/08”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"柔韧性扁平足练足弓，{mk('短足练习可以加一根弹力带')}：膝上套带、双膝向外撑住，同时做短足",
    "进阶按 2 周一级：坐 → 双脚站 → 单脚站，收缩 5 → 10 → 15 秒，12 次 × 3 组",
    "短足的要点：脚趾不弯、第 1 跖骨头往后收；先找感觉再加时间",
    "4 个动作组合练：脚趾分开、伸其余四趾、足弓拱起、伸姆趾",
    "如果只能选一样，短足练习比“卷毛巾、夹弹珠”更针对足内在肌",
    "这是短期、小样本的结果，用在有症状的人身上时要结合疼痛和功能来评估",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　综合练习"))
A.append(table(["第 1～2 周", "第 3～4 周", "第 5～6 周（加弹力带）"], [
    ["脚趾分开；伸姆趾；伸其余四趾", "侧卧髋外展", "下肢：屈髋—内收—外旋，屈膝；足：背伸—旋后—内翻，伸趾"],
    ["脚趾夹小物件", "脚趾夹玻璃珠放到别处", "下肢：伸髋—外展—内旋，伸膝；足：跖屈—旋前—外翻，屈趾"],
    ["滚网球", "脚趾卷毛巾", "下肢：屈髋—外展—内旋，屈膝；足：背伸—旋前—外翻，伸趾"],
    ["毛巾套住脚跟往回拉", "弹力带背伸和跖屈", "下肢：伸髋—内收—外旋，伸膝；足：跖屈—旋后—内翻，屈趾"],
    ["用脚写字母", "跟腱牵伸", "弹力带抗阻内翻和外翻"],
    ["扶椅背抬起一只脚", "屈膝跟腱牵伸", "在稳定和不稳定支撑面上保持平衡"],
    ["收缩 5 秒、放松 2 秒", "收缩 8 秒、放松 4 秒", "收缩 10 秒、放松 5 秒"]]))
A.append(small("每个动作 10 次 × 3 组；每周 6 次（3 次指导、3 次自练）。"))
A.append(tcap("原文表 2　短足练习"))
A.append(table(["周次", "体位", "收缩（秒）", "放松（秒）", "量", "频率"], [
    ["第 1～2 周", "坐位", "5", "2", "12 次 × 3 组", "每周 6 次（3 次指导、3 次自练）"],
    ["第 3～4 周", "双脚站", "10", "5", "12 次 × 3 组", "同上"],
    ["第 5～6 周", "单脚站", "15", "7", "12 次 × 3 组", "同上"]]))
A.append(small("短足练习包括：伸其余四趾、脚趾分开、足弓拱起、伸姆趾。"))
A.append(tcap("原文表 3　受试者基本情况（均值 ± 标准差）"))
A.append(table(["组别", "人数", "年龄（岁）", "体重（千克）", "身高（厘米）", "体重指数（kg/m²）"], [
    ["综合练习", "15", "21.93 ± 1.38", "59.8 ± 10.64", "162.86 ± 7.32", "22.56 ± 3.93"],
    ["短足", "15", "22.26 ± 1.66", "54.13 ± 8.06", "161.66 ± 4.76", "20.72 ± 3.03"],
    ["短足 + 髋外展", "15", "21.4 ± 1.12", "57.00 ± 7.75", "160.66 ± 5.44", "22.18 ± 3.59"],
    ["P 值", "", "0.248", "0.601", "0.232", "0.334"]]))
A.append(tcap("原文表 4　重复测量方差分析结果"))
R = [
    ("舟骨下沉（毫米）", ["10.84 ± 0.56", "11.11 ± 0.56", "11.26 ± 0.89"], ["8.37 ± 2.31", "7.92 ± 1.87", "6.28 ± 1.89"], ["&lt; 0.001", "&lt; 0.001", "&lt; 0.001"], ["22.78", "28.71", "40.14"], ["99.71 / &lt; 0.001 / 0.704", "3.51 / 0.039 / 0.143", "4.43 / 0.018 / 0.174"]),
    ("足底接触面积（cm²）", ["192.02 ± 18.52", "187.06 ± 11.34", "188.93 ± 11.24"], ["186.72 ± 15.20", "180.6 ± 14.59", "178.6 ± 7.72"], ["0.015", "&lt; 0.001", "0.001"], ["2.76", "3.45", "5.46"], ["47.54 / &lt; 0.001 / 0.773", "1.09 / 0.349 / 0.072", "1.71 / 0.198 / 0.109"]),
    ("足轴旋转角（°）", ["2.74 ± 0.98", "2.46 ± 1.12", "3.2 ± 1.14"], ["2.16 ± 0.84", "1.8 ± 0.68", "2.25 ± 0.85"], ["0.006", "0.022", "0.004"], ["21.16", "26.82", "29.68"], ["20.85 / &lt; 0.001 / 0.598", "1.71 / 0.201 / 0.108", "0.77 / 0.469 / 0.053"]),
    ("最大压力（原文单位 N）", ["10.32 ± 1.55", "11.13 ± 2.38", "11 ± 2.53"], ["10.05 ± 2.25", "8.4 ± 2.29", "8.3 ± 1.45"], ["0.616", "&lt; 0.001", "&lt; 0.001"], ["2.61", "24.52", "24.54"], ["36.58 / &lt; 0.001 / 0.723", "0.36 / 0.696 / 0.026", "6.55 / 0.005 / 0.319"]),
    ("前后晃动（毫米）", ["136.94 ± 27.21", "154.43 ± 35.67", "157.39 ± 39.79"], ["122.24 ± 30.92", "135.38 ± 41.96", "117.96 ± 34.65"], ["0.065", "0.007", "&lt; 0.001"], ["10.73", "12.33", "25.05"], ["40.02 / &lt; 0.001 / 0.741", "0.95 / 0.369 / 0.064", "4.14 / 0.026 / 0.229"]),
    ("内外侧晃动（毫米）", ["106.36 ± 36.13", "109.07 ± 26.78", "108.38 ± 31.57"], ["88.54 ± 29.68", "87 ± 28.76", "69.13 ± 17.08"], ["0.004", "0.015", "0.003"], ["16.75", "20.23", "56.77"], ["43.5 / &lt; 0.001 / 0.757", "0.63 / 0.548 / 0.088", "3.94 / 0.046 / 0.378"]),
    ("轨迹长度（毫米）", ["193.44 ± 50.68", "206.32 ± 46.15", "214.13 ± 47.73"], ["163.54 ± 42.86", "173.8 ± 43.24", "157.95 ± 34.76"], ["0.007", "0.001", "&lt; 0.001"], ["15.45", "15.76", "26.23"], ["50.21 / &lt; 0.001 / 0.782", "0.35 / 0.704 / 0.205", "2.53 / 0.098 / 0.153"]),
    ("晃动面积（mm²）", ["420.03 ± 101.31", "441.35 ± 104.06", "457.01 ± 120.14"], ["334.84 ± 114.75", "299.8 ± 60.91", "291.72 ± 85.14"], ["0.007", "&lt; 0.001", "&lt; 0.001"], ["20.28", "32.07", "36.16"], ["49.38 / &lt; 0.001 / 0.779", "0.02 / 0.978 / 0.002", "2.43 / 0.106 / 0.148"]),
    ("平均速度（毫米/秒）", ["19.34 ± 4.92", "20.67 ± 4.52", "21.51 ± 4.96"], ["16.33 ± 4.41", "17.54 ± 4.62", "15.7 ± 3.25"], ["0.006", "0.001", "&lt; 0.001"], ["15.56", "15.14", "27.01"], ["57.78 / &lt; 0.001 / 0.805", "0.41 / 0.665 / 0.029", "2.84 / 0.075 / 0.169"])]
rows = []
for name, pre, post, pw, pc, st in R:
    rows.append([name, "训练前", *pre, "时间 " + st[0]])
    rows.append(["", "6 周后", *post, "组别 " + st[1]])
    rows.append(["", "组内 P", *pw, "交互 " + st[2]])
    rows.append(["", "下降 %", *pc, ""])
A.append(table(["指标", "", "综合练习", "短足", "短足 + 髋外展", "F / P / 偏 η²"], rows))
A.append(small("内外侧晃动短足 + 髋外展组标准差原文印为“17/08”，此处按 17.08 录入；变化百分比均按原文照录。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Zarali A, Raeisi Z, Aminmahalati A. The effects of combined exercises, short foot exercises, and short foot exercises with isometric hip abduction on navicular drop, static parameters, and postural sway in women with flat foot: a randomized trial. BMC Sports Sci Med Rehabil. 2024;16:233. doi:10.1186/s13102-024-01019-9</em><br>"
    "原文以知识共享署名—非商业性使用—禁止演绎 4.0 协议（CC BY-NC-ND 4.0）发表。本文为非商业学术交流用的中文解读，照片引自原文图 2、3（编者加中文标注，器械与弹力带文字已模糊），流程图按原文图 1 重绘为中文，方案卡、进阶卡与结果图为编者中文绘制，表格为编者翻译，如有侵权请联系删除。"
))

TITLE = "「扁平足」短足练习加一根弹力带练髋外展，6 周舟骨下沉降得更多"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>扁平足短足练习推文</title>
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
