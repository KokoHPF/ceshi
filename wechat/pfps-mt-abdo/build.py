#!/usr/bin/env python3
"""Abdo 2025 髌股痛髋膝训练加手法治疗推文：生成 article_body.html 与 preview.html。

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
    "Abdo N, Youssef EF, Ibrahim MM. Efficacy of adding manual therapy to hip and knee exercises in patients with patellofemoral pain syndrome: a double-blinded randomized controlled clinical trial. Sci Rep. 2025;15:32655.",
    "作者来自埃及开罗大学物理治疗学院",
    "双盲随机对照试验（临床试验注册号 NCT05665452）；DOI：10.1038/s41598-025-17453-9",
], square=True))

A.append(h2("先说这篇在问什么"))
A.append(p(
    f"髌股痛的康复，指南推荐的核心是{b('髋和膝的力量训练 + 牵伸')}。很多治疗师还会顺手加几个手法："
    f"推髌骨、松髂胫束、揉外侧支持带。问题是——{mk('训练已经做足了，再加手法还有没有额外好处？')}"
))
A.append(p(
    f"这篇的答案是：{b('两组 4 周后疼痛、功能、力量、柔韧性都明显改善，但加不加手法没有显著差别')}。"
    f"不过对临床更有用的是，它把{mk('11 个训练动作 + 3 个手法')}都配了照片、写清了剂量，可以整套拿来用。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：开罗大学物理治疗门诊和本校学生中 {b('59 名')} 18～35 岁髌股痛患者（平均约 22 岁），症状超过 4 周，疼痛 >3/10",
    "诊断：隐匿起病；髌骨内侧或外侧缘压痛、髌后痛；上下楼、跪、久坐、下蹲中至少 2 项诱发前膝痛；髌骨挤压试验阳性",
    f"分组：对照组 30 人只做训练；手法组 29 人做{b('同样的训练 + 3 个手法')}",
    f"{b('每周 3 次 × 4 周，共 12 次')}，每次 45～60 分钟，门诊进行",
    "结局（不知道分组的评估者测）：上楼、下楼、下蹲、久坐时的疼痛，Kujala 髌股功能评分，髋外展、髋外旋、伸膝肌力，腘绳肌和小腿柔韧性，30 秒下台阶测试",
]))
A.append(pic(8, "原文图 11　研究流程"))

A.append(h2("重点：整套方案"))
A.append(pic(2, "治疗方案总览"))
A.append(pic(7, "每个环节的剂量"))

A.append(h3("一、牵伸（两组都做）"))
A.append(pic(4, "原文图 4、5　治疗师辅助牵伸"))
A.append(ul([
    f"{b('腘绳肌')}：仰卧，治疗师抬起伸直的腿",
    f"{b('股四头肌')}：侧卧，屈膝把足跟拉向臀部、髋后伸",
    f"{b('髂胫束')}：侧卧，上方腿后伸并内收垂向床下",
    f"{b('小腿三头肌')}：仰卧，膝伸直，治疗师把踝向背屈方向推",
    f"每块肌肉 {mk('保持 30 秒 × 3 次')}",
]))

A.append(h3("二、闭链力量（两组都做）"))
A.append(pic(5, "原文图 6～9　闭链力量"))
A.append(ul([
    f"{b('靠墙小幅下蹲')}：背靠墙，屈膝只到 {b('0～40°')}，避开髌股关节压力最大的角度",
    f"{b('向前上台阶')}：患腿踩台阶，蹬直把身体撑上去，对侧腿抬离地面",
    f"{b('侧向上台阶')}：侧对台阶，患腿踩上去撑起身体",
    f"{b('站立弹力带伸膝末端')}：弹力带套在膝后方，从微屈膝用力伸到完全伸直",
    f"剂量：{mk('每次保持 6 秒、放松 3 秒，做 10 次')}；动作间休息 1 分钟；{b('每周每个动作加 2 次')}",
]))

A.append(h3("三、开链力量（两组都做）"))
A.append(pic(6, "原文图 10　开链力量"))
A.append(ul([
    f"{b('侧卧髋外展')}：患腿在上，沙袋绑在踝上，膝伸直向上抬",
    f"{b('坐位髋外旋')}：坐床边、屈膝 90°，沙袋绑踝，小腿向内摆（髋外旋）",
    f"{b('坐位伸膝')}：坐位，沙袋绑踝，把膝伸直",
    f"剂量：{mk('2 组 × 10 次，每次保持 6 秒、放松 3 秒')}；组间和动作间休息 1 分钟；沙袋 0.5～10 kg，{b('每周按 10 次最大重复量重新调整重量')}",
]))

A.append(h3("四、手法（只有手法组做）"))
A.append(pic(3, "原文图 1～3　3 个手法"))
A.append(ul([
    f"{b('① 髌骨向内滑动')}：仰卧、膝伸直，治疗师用{b('掌根')}把髌骨向内推，{mk('持续 1 分钟，做 1 次')}",
    f"{b('② 髂胫束松解')}：仰卧，双手手指垂直插入{b('髂胫束与股外侧肌之间（前缘）')}、{b('髂胫束与股二头肌之间（后缘）')}，每处持续施压 1 分钟",
    f"{b('　 髂胫束松动')}：双手拇指和食指捏住髂胫束，按受限方向向前或向后推动，持续 1 分钟",
    f"{b('③ 外侧支持带深横摩擦')}：仰卧，手指垂直于支持带纤维方向做深横摩擦，1 分钟",
    f"进阶：{b('感觉组织“松开”、出现新的阻力点时，就往前推进')}",
]))

A.append(h2("结果（简要）"))
A.append(pic(9, "4 周后疼痛与功能"))
A.append(ul([
    f"两组{b('上下楼、下蹲、久坐时的疼痛都下降一半左右')}，Kujala 功能评分都从约 70 分升到约 84 分",
    "髋外展、髋外旋、伸膝力量，腘绳肌和小腿柔韧性，30 秒下台阶次数，两组也都提高",
    f"{red('组间所有指标都没有显著差别')}；手法组多数指标的改善百分比略高",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('髌股痛的主角是训练')}：这套 4 周、12 次的髋膝力量 + 牵伸方案，单独做就能明显减痛、改善功能",
    f"闭链动作用{b('“保持 6 秒 + 放松 3 秒”的等长停留')}和{b('0～40° 的小角度下蹲')}，对疼痛明显的患者很友好；每周加 2 次即可进阶",
    "开链用沙袋就能做，按 10 次最大重复量每周调整，在家也能复制",
    "髌骨内推、髂胫束松解、外侧支持带摩擦这 3 个手法每个只要 1 分钟，可以作为训练前的准备；但不要指望它们替代训练",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　基线资料（均值 ± 标准差）"))
A.append(table(["项目", "对照组（28 人）", "手法组（25 人）", "P"], [
    ["年龄（岁）", "22.64 ± 3.71", "21.92 ± 2.39", "0.41"], ["体重（kg）", "64.87 ± 11.51", "68.06 ± 8.96", "0.27"],
    ["身高（cm）", "167.19 ± 8.27", "166.20 ± 9.51", "0.69"], ["体重指数（kg/m²）", "23.18 ± 3.60", "24.77 ± 3.63", "0.12"],
]))
A.append(tcap("原文表 2　疼痛（视觉模拟评分，0～100 mm，均值 ± 标准差）"))
A.append(table(["情境", "", "对照组", "手法组", "组间差（95%CI）", "P"], [
    ["上楼", "治疗前", "50.39 ± 25.42", "50.68 ± 23.43", "−0.29（−13.82～13.25）", "0.97"],
    ["", "治疗后", "23.25 ± 18.12", "20.96 ± 17.16", "2.29（−7.47～12.05）", "0.74"],
    ["", "改善", "53.86%", "58.64%", "", ""],
    ["下楼", "治疗前", "40.93 ± 23.36", "38.28 ± 24.75", "2.65（−10.62～15.92）", "0.69"],
    ["", "治疗后", "17.64 ± 17.79", "15.52 ± 17.12", "2.12（−7.54～11.78）", "0.93"],
    ["", "改善", "56.90%", "59.46%", "", ""],
    ["下蹲", "治疗前", "53.43 ± 26.88", "64.28 ± 28.59", "−10.85（−26.16～4.45）", "0.16"],
    ["", "治疗后", "26.89 ± 22.31", "23.96 ± 18.56", "2.93（−8.46～14.34）", "0.09"],
    ["", "改善", "49.67%", "62.73%", "", ""],
    ["久坐", "治疗前", "58.54 ± 31.55", "57.16 ± 31.34", "1.38（−15.99～18.75）", "0.87"],
    ["", "治疗后", "32.86 ± 24.22", "27.68 ± 25.52", "5.18（−8.55～18.89）", "0.66"],
    ["", "改善", "43.87%", "51.57%", "", ""],
]))
A.append(small("组内前后比较 P 均 <0.001。"))
A.append(tcap("原文表 3　Kujala 功能评分"))
A.append(table(["", "对照组", "手法组", "组间差（95%CI）", "P"], [
    ["治疗前", "70.86 ± 13.76", "67.08 ± 13.56", "3.78（−3.77～11.33）", "0.32"],
    ["治疗后", "83.75 ± 9.50", "83.84 ± 10.63", "−0.09（−5.64～5.46）", "0.20"],
    ["改善", "12.89 分（18.19%）", "16.76 分（24.99%）", "", ""],
]))
A.append(tcap("原文表 4　肌力（按体重标准化，均值 ± 标准差）"))
A.append(table(["肌群", "", "对照组", "手法组", "组间 P"], [
    ["髋外展", "治疗前 / 后", "14.83 ± 5.66 / 17.51 ± 4.88", "13.15 ± 4.46 / 16.08 ± 5.39", "0.24 / 0.84"],
    ["髋外旋", "治疗前 / 后", "13.34 ± 5.02 / 15.28 ± 4.93", "12.01 ± 4.72 / 13.88 ± 6.38", "0.33 / 0.95"],
    ["伸膝", "治疗前 / 后", "23.81 ± 9.76 / 31.41 ± 12.07", "25.74 ± 11.22 / 30.28 ± 12.01", "0.51 / 0.17"],
]))
A.append(tcap("原文表 5　柔韧性（°，均值 ± 标准差）"))
A.append(table(["", "", "对照组", "手法组", "组间 P"], [
    ["腘绳肌（腘角）", "治疗前 / 后", "44.86 ± 13.67 / 55.61 ± 10.27", "51.05 ± 11.76 / 60.95 ± 12.59", "0.09 / 0.82"],
    ["小腿（踝背屈角）", "治疗前 / 后", "37.31 ± 9.91 / 40.48 ± 8.51", "33.82 ± 8.22 / 39.53 ± 6.73", "0.17 / 0.28"],
]))
A.append(tcap("原文表 6　30 秒下台阶测试（次，中位数 ± 四分位距）"))
A.append(table(["", "对照组", "手法组"], [["治疗前", "12 ± 5", "13 ± 4"], ["治疗后", "15 ± 5", "16 ± 4"], ["改善", "3 次（25%）", "3 次（23.08%）"]]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Abdo N, Youssef EF, Ibrahim MM. Efficacy of adding manual therapy to hip and knee exercises in patients with patellofemoral pain syndrome: a double-blinded randomized controlled clinical trial. Sci Rep. 2025;15:32655. doi:10.1038/s41598-025-17453-9</em><br>"
    "原文以 CC BY 4.0 协议开放获取。本文为学术交流用的中文解读，动作照片引自原文图 1～10 并加中文标注，方案卡、流程与结果图为编者中文重绘，表格为编者翻译。"
))

TITLE = "「髌股痛」髋膝训练之外再加手法，值不值？一套 4 周方案（附 14 个动作图解）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>髌股痛手法训练推文</title>
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
