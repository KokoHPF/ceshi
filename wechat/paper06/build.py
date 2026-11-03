#!/usr/bin/env python3
"""踝关节骨折后背屈受限（理学療法ジャーナル 2025）推文正文生成。

用法：python3 tools/make_figs.py work images <中号字体> <粗体> && python3 build.py → article_body.html 和 preview.html
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
def I(n, c): A.append(img(n)); A.append(cap(c))
I(1, "原文信息（编者中文重排）")
A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "溝田丈士, 壇 順司. 足関節果部骨折に対する機能解剖学に基づく理学療法. 理学療法ジャーナル. 2025;59(5):572-587（特集：機能解剖学に基づく疾患別理学療法）",
    "作者单位：副島整形外科病院康复科（佐贺）；帝京大学福冈医疗技术学部",
    f"文章类型：{b('日文特集综述 + 病例')}；医学書院出版，{red('非开放获取')}",
], square=True))
A.append(p(f"踝关节骨折后，骨头长好了、背屈却总差一截，是康复里最常见的问题之一。这篇日文特集先讲{b('正常背屈时距骨怎么动')}，再用一个{b('外踝骨折病例')}演示：怎样把骨折、韧带损伤、手术、免负重/固定对功能的影响一层层理清，找出背屈受限的真正原因——其中最容易被忽略的是{b('拇长屈肌（FHL）')}。"))
A.append(h2("先说结论"))
I(2, "原文要点（编者整理）")

A.append(h2("一、正常背屈（非负重）：距骨要“嵌进去、再往后走”"))
A.append(p(f"踝关节由距骨滑车与胫骨下关节面、内踝关节面、外踝关节面构成。{b('背屈时距骨滑车嵌入踝穴，跖屈时从踝穴向前突出')}。嵌入的转折点约在{b('跖屈 27.1±2.3°')}；从这里继续往背屈方向走，距骨会把下胫腓关节向外撑开，同时把关节“锁”住。"))
I(3, "原文图 1a、b")
I(4, "原文图 1c ①②")
I(5, "原文图 1c ③")
A.append(p(f"嵌入之后再继续背屈，{b('距骨内侧结节会从踝穴向后突出')}，胫骨后下缘与跟骨结节上端距离拉大。所以关节后方的 {b('FHL 要够软、跟腱要能向远端滑动')}。作者给出了在体表触摸这一过程的方法："))
I(6, "原文图 2")

A.append(h2("二、负重背屈：还要“外翻 + 降足弓”"))
I(7, "负重位背屈（据原文整理）")
I(8, "原文图 3a、b")
I(9, "原文图 3c、d")
A.append(p(f"{mk('负重背屈时足弓要能降下来，所以外翻活动度是关键')}。评估和治疗时要记住图 3d 里这些骨性位置关系：距骨头、载距突、舟骨结节、跗骨窦。"))
I(10, "原文图 4")

A.append(h2("三、哪些因素会限制背屈"))
I(11, "背屈受限因素（据原文整理）")
I(12, "原文图 5")
I(13, "原文图 6")

A.append(h2("四、踝关节骨折的“病态功能解剖”"))
I(14, "踝关节骨折（据原文整理）")
I(15, "原文图 7")
A.append(p(f"骨折会连带周围组织受伤。作者把可能受累的组织和它们的功能列成了表："))
A.append(table(["部位", "组织", "功能"], [
    ["外踝", "距腓前韧带、距腓后韧带、跟腓韧带", "限制踝内收、足内翻"],
    ["外踝", "下胫腓前韧带、下胫腓后韧带", "稳定胫腓关节（限制踝背屈、后足外旋）"],
    ["外踝", "腓骨长肌", "足外翻、第 1 跖列跖屈"],
    ["外踝", "腓骨短肌", "足外翻、第 5 跖列外翻"],
    ["内踝", "三角韧带", "限制踝外展、足外翻"],
    ["内踝", "胫骨后肌", "踝跖屈、足内翻"],
    ["内踝", "趾长屈肌", "踝跖屈、足内翻、屈趾"],
    ["后踝", "下胫腓后韧带", "稳定胫腓关节（限制踝背屈、后足外旋）"],
    ["后踝", "拇长屈肌", "踝跖屈、屈拇趾"],
]))
A.append(tcap("原文表 1  骨折可能连带损伤的组织及其功能（编者中译）"))
A.append(p("任何一个组织受损，都可能让它的主要功能受限，或影响肌、腱等软组织的柔韧性和滑动，从而加重踝足的活动受限。"))

A.append(h2("五、病例：外踝骨折后背屈受限"))
I(16, "原文图 8")
I(17, "病例与评估（据原文整理）")
I(18, "原文图 9")
I(19, "原文图 10a–c")
I(20, "原文图 10d")
A.append(h3("把病态一层层理清"))
I(21, "原文图 11（编者中文重绘）")
I(22, "病例解读（据原文整理）")
A.append(p(f"作者强调：同样的思路可以用到其他骨折——{b('按骨折分型和表 1 理清受损组织、周围组织及其功能，先假设病态功能解剖，再解释临床症状')}。"))

A.append(h2("六、怎么治"))
I(23, "原文图 12a")
I(24, "原文图 12b–d")
I(25, "治疗思路（据原文整理）")

A.append(h2("七、结果"))
I(26, "原文表 2（编者重绘柱状图）")
A.append(table(["项目（°）", "健侧", "患侧治疗前", "患侧治疗后"], [
    ["非负重伸膝背屈", "10", "2", "7"], ["非负重屈膝背屈", "21", "10", "17"], ["负重背屈", "47", "23", "38"],
    ["外翻", "10", "-3", "6"], ["拇趾伸展角（FHL 试验）", "23", "5", "16"],
]))
A.append(tcap("原文表 2  活动度变化"))
A.append(ul([
    f"治疗 {b('2 周')}，{b('2 次')}徒手治疗 + 自我训练",
    "非负重、负重背屈、外翻、拇趾伸展角和负重时足弓下降都有改善；背屈时可见距骨嵌入踝穴、内侧结节向后突出，超声下内侧结节与胫骨后下缘距离的健患差缩小",
    f"主诉的前方疼痛 {b('NRS 4 → 1')}；但出现了关节后方的牵拉感——作者认为这说明背屈已接近正常关节运动，之后要持续做 FHL 和比目鱼肌的牵伸",
]))

A.append(h2("八、作者的总结"))
A.append(quote("治療の際には，関節や軟部組織に適切な方向に適した力を加えることが重要となる．また的確に評価・治療を実践するうえでは，各組織の構造や位置関係を理解し，正確に触知できるスキルが鍵となる．", "改善活动受限，要先知道正常情况下关节里发生了什么运动、有病变时会怎么变、又会怎样代偿；治疗时对关节和软组织施加方向合适的力。准确触诊各组织的能力是关键。"))

A.append(h2("原文对不上的地方"))
I(27, "编者核对原文时发现")
A.append(p(f"另外，图 12a ③ 的说明里“足关节最大背屈位にて足趾伸展位にて”重复了两个“にて”，属排版小疏漏。以上不影响主要结论，供阅读原文时参考。"))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>溝田丈士, 壇 順司. 足関節果部骨折に対する機能解剖学に基づく理学療法. 理学療法ジャーナル. 2025;59(5):572-587.</em><br>"
    "原文 © 医学書院（IGAKU-SHOIN Ltd.），非开放获取。本文为中文学习笔记：原文图按原样引用、未作改动，中文说明为编者所加；图 11、表 1、表 2 由编者据原文中译重绘。"
    "<b>仅供学习交流，如有侵权请联系删除。</b>"
))
TITLE = "「踝关节」骨折后背屈总差一截？别漏了拇长屈肌——从功能解剖到评估与治疗"
PTITLE = "踝关节骨折背屈受限推文"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<!DOCTYPE html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>""" + PTITLE + """</title>
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
