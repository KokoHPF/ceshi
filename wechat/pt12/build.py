#!/usr/bin/env python3
"""桡骨远端关节内骨折术后康复（臨床整形外科 2024）推文正文生成。

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
    "松澤翔太, 森谷浩治. 橈骨遠位端関節内骨折術後のリハビリテーションの実際. 臨床整形外科. 2024;59(5):638-643（特集：絶対！整形外科外傷学 · 第 5 章 康复室）",
    "作者单位：一般财团法人新潟手外科研究所（Niigata Hand Surgery Foundation）",
    f"文章类型：{b('日文特集综述（治疗师视角）')}；医学書院出版，{red('非开放获取')}",
], square=True))
A.append(p(f"2000 年以后，掌侧锁定钢板（palmar locking plate, PLP）让桡骨远端骨折术后可以更安全地早期活动。有研究认为只在家训练与接受手治疗的效果差不多，{b('但仍有一部分患者在家练不出来，这时候康复介入是有效的')}。这篇文章从治疗师的角度，按术后时间线讲 PLP 术后怎么做康复。"))
A.append(h2("先说结论"))
I(2, "原文要点（编者整理）")

A.append(h2("一、后疗法时间表"))
I(3, "原文图 1")
I(4, "原文图 1（编者中文重绘）")
A.append(p(f"整个流程分 4 段：{b('外固定期（0–1 周）')} → {b('训练前期（去外固定后，1–5 周）')} → {b('训练中期（5–8 周）')} → {b('训练后期（8–12 周）')}。训练、支具、日常生活活动三条线同时推进。"))
I(5, "开始时机与水肿管理（据原文整理）")

A.append(h2("二、外固定期：最重要的时期"))
A.append(p(f"作者说：{mk('这一时期的训练说是最重要的也不为过')}。核心是未固定关节的活动和水肿管理。"))
I(6, "原文图 2")
I(7, "外固定期要点（据原文整理）")
I(8, "原文图 3")

A.append(h2("三、训练前期（去外固定后）"))
I(9, "训练前期：腕关节（据原文整理）")
I(10, "原文图 4")
I(11, "前臂旋转、握力与日常使用（据原文整理）")
A.append(table(["项目", "原文给出的数字"], [
    ["掌侧锁定钢板刚度", "约 150–250 N"],
    ["握力与桡骨远端负荷", "握力每 1 kg 增加约 26 N"],
    ["10 kg 握力", "约 260 N，超过钢板刚度"],
]))
A.append(tcap("握力训练为什么要慢（原文数据；编者整理）"))
A.append(p(f"所以作者建议：{b('早期握力训练只给日常生活确实受限的老年人等')}，先从握毛巾、软球这种轻负荷开始，见到骨痂再上握力器。"))

A.append(h2("四、训练中期到后期"))
I(12, "中后期要点（据原文整理）")
I(13, "原文图 5")
A.append(p(f"图 5e、f 的前臂自我被动旋转有个细节：{b('旋后时把尺骨头从背侧推向掌侧，旋前时从掌侧推向背侧')}，和前面“引导桡骨绕尺骨头旋转、平移”的思路一致。"))
I(14, "原文图 6")

A.append(h2("五、按周速查"))
A.append(table(["时间", "训练", "日常生活"], [
    ["术后第 1 天", "未固定关节（手指、拇指、肘、肩）ROM；水肿管理", "戴外固定、不痛范围轻用；≤500 g（非不稳定骨折）"],
    ["1–3 周", "腕背伸支具 / 前臂托；约 1 周起腕关节 ROM（不稳定骨折外固定约 3 周后）", "同上"],
    ["去外固定后", "腕、前臂辅助主动 / 主动；飞镖投掷运动；轻度被动 + 器具；轻度握力", "不痛范围逐步使用"],
    ["4–5 周", "—", "可提约 1 kg，逐步加量"],
    ["见骨痂后", "加大被动强度；握力器、沙袋、弹力带抗阻", "—"],
    ["6 周", "—", "解除日常生活限制"],
    ["8 周起", "腕部负荷训练（尺骨正变异、关节面高度粉碎者不勉强）", "逐步手部承重、提重物、运动、重体力"],
    ["12 周前", "—", "避免患肢过度负荷"],
]))
A.append(tcap("按周速查（编者据原文正文与图 1 整理）"))
A.append(p("原文另附 2 段无声动画（腕关节、前臂的康复手法），发布在医学書院网站，公开至 2027 年 5 月 31 日，可按原文二维码查看。", "font-size:14px;color:#666;"))

A.append(h2("原文对不上的地方"))
I(15, "编者核对原文时发现")
A.append(p("以上不影响主要结论，供阅读原文时参考。"))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>松澤翔太, 森谷浩治. 橈骨遠位端関節内骨折術後のリハビリテーションの実際. 臨床整形外科. 2024;59(5):638-643.</em><br>"
    "原文 © IGAKU-SHOIN Ltd, 2024（医学書院），非开放获取。本文为中文学习笔记：原文图按原样引用、未作改动，中文说明为编者所加；图 1 由编者据原文中译重绘。"
    "<b>仅供学习交流，如有侵权请联系删除。</b>"
))
TITLE = "「手腕」桡骨远端骨折钢板术后康复怎么做？按周推进的后疗法时间表"
PTITLE = "桡骨远端骨折术后康复推文"
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
