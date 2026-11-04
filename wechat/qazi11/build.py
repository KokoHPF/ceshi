#!/usr/bin/env python3
"""DRUJ 不稳综述（J Hand Microsurg 2021）推文正文生成。

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
    "Qazi S, Graham D, Regal S, Tang P, Hammarstedt JE. Distal Radioulnar Joint Instability and Associated Injuries: A Literature Review. J Hand Microsurg. 2021;13(3):123-131.",
    "作者单位：Temple University Hospital；Allegheny General Hospital（美国宾夕法尼亚州）",
    f"文章类型：{b('文献综述')}；© Society of Indian Hand & Microsurgeons（Thieme 出版），{red('非开放获取')}",
], square=True))
A.append(p(f"下尺桡关节（DRUJ）负责前臂的旋前和旋后。它常常和桡骨远端骨折、Galeazzi 骨折等一起受伤，{b('初诊时很容易被漏掉')}，日后变成慢性疼痛、旋转受限和关节炎。这篇综述按“{b('解剖 → 查体 → 影像 → 各类合并损伤及处理')}”的顺序，把临床上需要的要点梳理了一遍。"))
A.append(h2("先说结论"))
I(2, "原文要点（编者整理）")

A.append(h2("一、DRUJ 解剖与生物力学"))
I(3, "解剖与生物力学（据原文整理）")
I(4, "原文图 1")
A.append(p(f"乙状切迹的形状和外伤后不稳有关。Tolat 等观察 50 例尸体，把乙状切迹分成 4 型。{mk('平坦型最常见（42%），也可能最容易不稳')}，单纯修软组织效果可能更差。"))
I(5, "原文图 2")
A.append(p(f"既然骨性结构只提供约 {b('20%')} 的稳定性，剩下的就靠软组织：TFCC、关节囊、骨间膜，以及 ECU 和旋前方肌。TFCC 由三角纤维软骨本体、尺腕半月板同系物、尺侧副韧带、深浅层背侧 / 掌侧桡尺韧带和 ECU 腱鞘组成，作用是把桡骨关节面延伸到尺骨头、传导尺腕关节的轴向力、在桡尺骨之间提供“结实又有弹性”的连接，并支撑腕骨尺侧。"))
I(6, "原文图 3")
I(7, "主要与次要稳定结构（据原文整理）")

A.append(h2("二、体格检查"))
A.append(p(f"诊断 DRUJ 损伤要{b('保持高度怀疑')}：近期腕部外伤、新出现的旋前或旋后受限都要警惕。所有检查都要{mk('和健侧对比')}。"))
I(8, "原文图 4")
I(9, "急性 / 慢性脱位与 Seo 分级（据原文整理）")
A.append(table(["分级", "前后应力试验表现"], [
    ["0", "稳定性正常"], ["1", "松弛度增加，无临床症状"], ["2", "平移增加，诱发症状，无坚实终末感"], ["3", "主动旋转前臂时出现半脱位"],
]))
A.append(tcap("原文表 1  前后应力试验中 DRUJ 不稳的分级（Seo 等；编者中译）"))
A.append(p("下面几个试验主要针对 TFCC 损伤，可以帮助进一步定位："))
I(10, "原文图 5")
I(11, "原文图 6、7")
I(12, "原文图 8")
I(13, "原文图 9")
I(14, "按压试验（据原文整理，原文无配图）")
A.append(table(["试验", "要点", "原文给出的数据"], [
    ["尺骨小凹征", "屈肘 90°，拇指深压尺骨小凹", "敏感度 95.2%"],
    ["TFCC 应力试验", "被动尺偏", "—"],
    ["尺腕应力试验", "尺偏 + 轴向压 + 旋前旋后", "—"],
    ["按压试验", "撑椅起立", "敏感度 100%（Lester 等）"],
    ["琴键征", "尺骨背→掌侧加压，与健侧比", "—"],
    ["双侧试验", "双手同时旋前→旋后，摸尺骨头", "敏感度 90%（20 例，以 CT 对照）"],
]))
A.append(tcap("查体试验速查（编者据原文整理）"))

A.append(h2("三、影像"))
I(15, "X 线（据原文整理）")
A.append(p(f"作者提醒：{mk('标准侧位片判断 DRUJ 半脱位并不可靠')}，加重应力侧位可以放大不稳的表现。要看清关节是否匹配，CT 更合适："))
I(16, "原文图 10")
I(17, "CT、MRI 与关节镜（据原文整理）")

A.append(h2("四、合并损伤与处理"))
A.append(h3("1. 单纯急性 DRUJ 脱位"))
I(18, "单纯急性脱位（据原文整理）")
A.append(h3("2. 桡骨远端骨折"))
I(19, "DRF 与 DRUJ 不稳（据原文整理）")
A.append(p(f"多项研究认为 DRUJ 不稳是 DRF {b('独立的预后不良因素')}；但 DRUJ 要不要专门处理仍有争议，也没有公认的治疗流程。作者的观点是：{b('骨折复位固定后，慢性 DRUJ 不稳并不常见')}——次要稳定结构加上锁定钢板，往往足以让 TFCC 在制动中愈合。"))
A.append(h3("3. 尺骨茎突骨折"))
I(20, "尺骨茎突骨折（据原文整理）")
A.append(h3("4. Galeazzi 骨折"))
I(21, "Galeazzi 骨折（据原文整理）")
A.append(h3("5. Essex-Lopresti 损伤"))
I(22, "Essex-Lopresti 损伤（据原文整理）")

A.append(h2("五、作者的总结"))
A.append(quote("Although there is still debate on treatment options, the majority of studies reported no chronic instability or loss in functional outcomes with adequate upper extremity fracture reduction/alignment and conservative treatment (cast immobilization in a position of maximal stability for 4–6 weeks) for the DRUJ.",
               "尽管治疗方案仍有争议，大多数研究显示：只要上肢骨折复位、对线良好，再对 DRUJ 做保守治疗（在最稳定的体位石膏制动 4–6 周），就不会出现慢性不稳或功能损失。"))
A.append(ul([
    "DRUJ 损伤在上肢外伤初诊时常被漏掉，查体手法很多，关键是想到它",
    "桡骨远端骨折、尺骨茎突基底骨折、乙状切迹和尺侧角骨折、Galeazzi 骨折、Essex-Lopresti 损伤都可能合并 DRUJ 损伤",
    "侧位 X 线判断不精确，加重应力侧位能提高敏感度；CT 有多种方法判断匹配度；关节镜是看 TFCC 撕裂的金标准",
    "持续不稳时：关节镜 / 开放修复 TFCC、固定尺骨茎突骨折、DRUJ 穿针",
]))
A.append(h2("原文对不上的地方"))
I(23, "编者核对原文时发现")
A.append(p("另外，影像一节“Park and Kim that the subluxation ratio method was the most reliable”漏了动词（应为 found），不影响理解。以上供阅读原文时参考。"))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Qazi S, Graham D, Regal S, Tang P, Hammarstedt JE. Distal Radioulnar Joint Instability and Associated Injuries: A Literature Review. J Hand Microsurg. 2021;13(3):123-131. doi:10.1055/s-0041-1730886</em><br>"
    "原文 © 2021 Society of Indian Hand & Microsurgeons, All rights reserved（Thieme 出版），非开放获取。本文为中文学习笔记：原文图只按面板裁切、未作改动，中文说明为编者所加；表 1 由编者中译。"
    "<b>仅供学习交流，如有侵权请联系删除。</b>"
))
TITLE = "「手腕」下尺桡关节（DRUJ）不稳怎么查、怎么想？解剖、查体、影像与合并损伤一文梳理"
PTITLE = "DRUJ 不稳综述推文"
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
