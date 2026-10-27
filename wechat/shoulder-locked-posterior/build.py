#!/usr/bin/env python3
"""慢性锁定性肩关节后脱位闭合复位 3 例（Calamita、Boileau 等 2025）推文。

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
    "Calamita AG, Aguilar J, Chelli M, Descamps J, Boileau P. Treatment of Chronic Locked Posterior Dislocation of the Shoulder: Is There a Time Limit to Try a Closed Reduction? A Report of 3 Cases. JBJS Case Connect. 2025;15(4):e25.00384. doi:10.2106/JBJS.CC.25.00384",
    "作者单位：法国尼斯 ICR 修复外科研究所（KANTYS 集团），以及意大利、西班牙、法国巴黎的骨科",
    f"文章类型：{b('病例报告')}（3 例，随访 2～5 年）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"传统观点：肩关节后脱位超过 {b('3 周')}、或反 Hill-Sachs 缺损 {b('>25%')}，就不该再闭合复位，直接手术",
    f"本文 3 例在受伤 {b('4～10 周')}后、缺损 {b('25%～36%')}，在全麻肌松下用{b('“双拇指”手法')}闭合复位，全部成功",
    f"复位后{mk('外旋位固定 6 周')}，3 个月内避免强力内旋；随访 2～5 年无再脱位、无股骨头坏死、无骨关节炎",
    f"但{red('只有 3 例')}，且由手法发明者团队完成，只能说明“时间界限也许没那么死”",
]))

A.append(h2("一、什么是慢性锁定性后脱位"))
A.append(img(2))
A.append(cap("背景（编者根据原文整理）"))
A.append(img(3))
A.append(cap("原文图 11：a 锁定性后脱位和反 Hill-Sachs 损伤示意图；b 复位体位——患者侧卧、全麻肌松，助手跪在手术台上稳住上肢，术者站在后方"))
A.append(img(4))
A.append(cap("原文图 2：病例 1 的 CT 横断面（左）和三维重建（右），肱骨头卡在关节盂后方，前内侧有明显的压缩缺损（反 Hill-Sachs 损伤）"))

A.append(h2("二、“双拇指”复位法"))
A.append(img(5))
A.append(cap("复位三步（据原文整理）"))
A.append(img(6))
A.append(cap("原文图 12：双拇指复位三步。a 助手逐渐内旋（IR），让肱骨头从关节盂后缘脱开；b 助手牵引（TRACTION）上提，术者双拇指向前上推（PUSH UP）；c 解锁后助手外旋（ER），能恢复外旋即复位成功"))
A.append(p(f"作者特别强调：这一手法要在{b('手术室、全身麻醉、肌肉完全松弛')}下进行，推、拉、转逐步配合，{b('不能暴力')}，并在透视下确认对位。"))

A.append(h2("三、复位后：外旋位固定"))
A.append(img(7))
A.append(cap("固定与康复（据原文整理）"))
A.append(img(8))
A.append(cap("原文图 3：外旋 30°、外展 30° 的肩关节支具，固定 6 周后开始系统康复"))
A.append(p(f"这和常见的“肩关节脱位后内旋位吊带”正好相反。原因是后脱位锁住几周后，{b('后方关节囊被拉长成一个袋子')}，内旋位会让肱骨头又滑回去——病例 3 在外院复位后就是因为内旋位固定而复发。"))

A.append(h2("四、三个病例"))
A.append(img(9))
A.append(cap("三位患者（据原文表 I 整理）"))
A.append(h3("病例 1：53 岁女性，癫痫发作摔倒"))
A.append(img(10))
A.append(cap("原文图 1：a 复位前正位片（左）和肩胛 Y 位片（右），锁定性后脱位；b 末次随访，肱骨头居中，无骨关节炎"))
A.append(img(11))
A.append(cap("原文图 4：5 年随访，主动上举、外旋、内旋均恢复"))
A.append(h3("病例 2：67 岁男性，触电"))
A.append(img(12))
A.append(cap("原文图 5：受伤 10 周时，a 右肩外旋明显受限，b 主动前屈上举受限"))
A.append(img(13))
A.append(cap("原文图 6：a 正位片关节间隙消失，可见“双轮廓征”，提示锁定性后脱位；b 术中透视确认复位"))
A.append(img(14))
A.append(cap("原文图 7：a 复位前 CT，锁定性后脱位伴反 Hill-Sachs 损伤；b 5 年随访，肱骨头居中，无骨关节炎"))
A.append(img(15))
A.append(cap("原文图 8：MRI T2 横断面，a 确诊时肱骨头前部明显高信号，b 1 年后完全消退"))
A.append(h3("病例 3：23 岁男性，工伤，外院复位后再脱位"))
A.append(img(16))
A.append(cap("原文图 9：a 复位前正位片，锁定性后脱位；b 末次随访，肱骨头居中、关节间隙保留"))
A.append(img(17))
A.append(cap("原文图 10：a 复位前 CT，锁定性后脱位伴反 Hill-Sachs 损伤；b 复位后 CT，肱骨头居中，无骨关节炎"))
A.append(tcap("原文表 I：末次随访结果"))
A.append(table(["", "病例 1", "病例 2", "病例 3"], [
    ["复位时间", "4 周", "10 周", "8 周"],
    ["缺损占肱骨头", "36%", "25%", "34%"],
    ["固定体位（6 周）", "外旋 30°＋外展 30°", "外旋 60°＋外展 30°", "外旋 60°＋外展 30°"],
    ["随访", "5 年", "5 年", "2 年"],
    ["主动上举 / 外旋 / 内旋", "170° / 50° / T12", "180° / 50° / T12", "180° / 60° / T12"],
    ["疼痛 VAS", "2/10", "0/10", "0/10"],
    ["主观肩关节评分（SSV）", "80%", "100%", "90%"],
    ["Constant / Rowe / Walch-Duplay", "79 / 90 / 90", "93 / 100 / 100", "91 / 80 / 90"],
]))

A.append(h2("这篇文章能信几分"))
A.append(img(18))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('病例报告')}：3 例、同一团队、没有对照组，也没说期间有没有闭合复位失败、转为手术的患者",
    "3 例缺损都 <50%（Randelli 1 型），作者也只把结论限定在 25%～50% 之间",
    "优点：有 2～5 年的影像和功能随访，病例 2 还有 MRI 证明肱骨头前部的异常信号 1 年后消退",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "病例 3 正文写 10 周转诊，表 I 写 8 周复位",
    "摘要说 3 例缺损都 >25%，但病例 2 是 25%",
    "讨论说外旋 >30° 固定，病例 1 实际是 30°",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"癫痫、触电后的肩痛，外旋明显受限（甚至外旋不到中立位），要{b('想到后脱位')}；正位片“双轮廓征”，加拍肩胛 Y 位片，CT 可确认并测量缺损",
    f"超过 3 周不一定只能手术：缺损 {b('<50%')}、无合并骨折时，可在有经验的中心考虑全麻下闭合复位",
    f"复位后{b('外旋位')}固定 6 周，3 个月内避免强力内旋；康复先恢复活动度，再练肩胛控制和动态稳定",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Calamita AG, Aguilar J, Chelli M, Descamps J, Boileau P. Treatment of Chronic Locked Posterior Dislocation of the Shoulder: Is There a Time Limit to Try a Closed Reduction? A Report of 3 Cases. JBJS Case Connect. 2025;15(4):e25.00384. doi:10.2106/JBJS.CC.25.00384</em><br>"
    "原文以知识共享署名-非商业性使用-禁止演绎（CC BY-NC-ND 4.0）协议开放获取，版权归原作者所有。本文为非商业的学术交流中文解读：原文图 1～12 原样引用，未作任何修改，中文说明见图注；编者整理卡为编者根据原文撰写。仅供学习交流，如有侵权请联系删除。"
))
TITLE = "「肩关节」后脱位锁住 10 周，还能不开刀复位？“双拇指”手法 3 例 5 年随访"
PTITLE = "慢性肩后脱位闭合复位推文"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>""" + PTITLE + """</title>
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
