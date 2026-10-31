#!/usr/bin/env python3
"""《三维 CT 骨折线图结合解剖测量的第五跖骨基底撕脱骨折分型》（He、Zhou 等 2022 J Foot Ankle Res）推文。

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
A.append(img(1))
A.append(cap("原文信息（编者中文重排）"))
A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "He W, Zhou H, Zhang Y, Yu T, Xia J, Zhao Y, Yang Y, Li B. Classification of avulsion fractures of the fifth metatarsal base using three-dimensional CT mapping and anatomical assessment: a retrospective case series study. J Foot Ankle Res. 2022;15:65. doi:10.1186/s13047-022-00571-2",
    "作者单位：同济大学附属同济医院骨科（上海）",
    f"文章类型：{b('回顾性病例系列 + 尸体解剖')}，证据等级 Ⅲ；CC BY 4.0 开放获取",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"222 例第五跖骨基底撕脱骨折的骨折线，在背侧观上{b('集中在一条弧形带')}，最密集处距后缘 2/5～7/10",
    f"8 侧标本解剖：{b('腓骨短肌')}和{b('跖腱膜外侧束')}都附着在基底背外侧、粗壮；{b('第三腓骨肌')}细、附着更远（1 例缺如），作用不大",
    f"据此提出按损伤机制的新分型：{b('Ⅰ 型')}跖腱膜外侧束为主，{b('Ⅱ 型')}腓骨短肌为主，{b('Ⅲ 型')}两者共同（ⅢA 一条骨折线、ⅢB 两条）",
    f"作者建议：{red('Ⅲ 型移位 ≥2 mm 考虑手术')}；{red('Ⅰ 型要查腓骨短肌是否断裂')}",
]))

A.append(h2("一、为什么要研究"))
A.append(img(2))
A.append(cap("研究背景（据原文整理）"))
A.append(p(f"第五跖骨撕脱骨折很常见，但骨折线形态五花八门：有{b('双骨折线、跨区、弯折')}的。常用的 Ekrol 分型（按骨折线位置分 Ⅰ～Ⅲ）和 Mehlhorn 分型（按骨折线进入关节的位置和是否移位）都描述不了这些情况，也说不清骨折是“谁拉的”。"))

A.append(h2("二、怎么做的"))
A.append(img(3))
A.append(cap("研究方法（据原文整理）"))
A.append(pic(4, "原文图 1（编者中文标注）  222 例骨折线的三维叠加图"))
A.append(pic(5, "原文图 2（编者中文标注）  骨折线热图"))
A.append(pic(6, "原文图 3（编者中文标注）  背侧观上定位骨折线的测量方法"))

A.append(h2("三、结果"))
A.append(h3("1. 骨折线集中在哪"))
A.append(pic(7, "原文图 4（编者中文标注）  背侧观热图"))
A.append(p(f"骨折线集中在一条{b('弧形带')}：从距后缘切线 1/4～4/5 的位置开始，起点紧贴外侧缘、终点几乎到内侧缘；颜色最红（出现最多）的区域在{mk('距后缘 2/5～7/10')}。"))
A.append(h3("2. 谁附着在基底"))
A.append(pic(8, "原文图 5（编者中文标注）  腓骨短肌附着区"))
A.append(pic(9, "原文图 6（编者中文标注）  跖腱膜外侧束附着区"))
A.append(pic(10, "据原文表 3～5 绘制：三条附着结构的腱径"))
A.append(img(11))
A.append(cap("解剖测量结果（据原文表 2～5 整理）"))
A.append(h3("3. 骨折块和附着区对得上"))
A.append(pic(12, "原文图 7（编者中文标注）  按损伤机制分别作热图"))
A.append(p(f"把 222 例按骨折线位置分成三组分别作热图，骨折块恰好落在{b('跖腱膜外侧束和/或腓骨短肌的附着区')}。第三腓骨肌附着更远、更细，作者认为它在撕脱骨折中不起主要作用。"))

A.append(h2("四、新分型"))
A.append(pic(13, "原文图 8（编者中文标注）  基于损伤机制的新分型"))
A.append(table(["分型", "骨折线位置", "主要“拉力源”", "例数"], [
    ["Ⅰ 型", "近端", "跖腱膜外侧束", "48"],
    ["Ⅱ 型", "中间", "腓骨短肌", "54"],
    ["ⅢA 型", "远端，1 条骨折线", "两者共同", "120（ⅢA + ⅢB）"],
    ["ⅢB 型", "远端，2 条骨折线", "两者共同", ""],
]))
A.append(img(14))
A.append(cap("新分型要点（据原文整理）"))
A.append(pic(16, "据原文绘制：同一批病例两种分型的分布"))

A.append(h2("五、对治疗的提示"))
A.append(img(15))
A.append(cap("讨论要点（据原文整理）"))
A.append(ul([
    f"附带随访的 30 例保守治疗患者中，3 个月内 {b('5 例再移位，全是 Ⅲ 型')}；作者因此建议 Ⅲ 型移位 ≥2 mm 考虑手术",
    f"10 例 Ⅰ 型患者都在外踝尖处{b('合并腓骨短肌断裂')}，作者建议 Ⅰ 型患者用 MRI 或超声查腓骨短肌",
    f"作者也承认：多数撕脱骨折保守治疗效果好，最佳治疗方案仍需大样本随访研究",
]))

A.append(h2("原文对不上的地方"))
A.append(ul([
    f"性别前后相反：方法写“{b('97 例女性、125 例男性')}”，表 1 却是男 97 例（43.8%）、女 125 例（56.2%）；年龄上限一处写 80 岁、一处写 81 岁",
    f"讨论说远端和近端骨折线“{b('很少穿过跖跗关节面')}”，后文又说远端为主的 Ⅲ 型“{b('几乎都累及关节面')}”",
    f"“Ⅲ 型移位 ≥2 mm 建议手术”只基于 30 例、3 个月的附带随访（5 例再移位），文中没有给出各型分别有多少例、移位多少",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>He W, Zhou H, Zhang Y, Yu T, Xia J, Zhao Y, Yang Y, Li B. Classification of avulsion fractures of the fifth metatarsal base using three-dimensional CT mapping and anatomical assessment: a retrospective case series study. J Foot Ankle Res. 2022;15:65. doi:10.1186/s13047-022-00571-2</em><br>"
    "原文为 CC BY 4.0 开放获取（© The Author(s) 2022）。本文为中文解读：原文图 1～8 引自原文，编者将图中英文方位词替换为中文、在分型旁加了中文名称，部分图下方加了中文图例条；其余整理卡和数据图由编者根据原文撰写、绘制。"
))
TITLE = "「足踝」第五跖骨基底撕脱骨折是谁拉断的？222 例三维 CT 骨折线图给出新分型"
PTITLE = "第五跖骨撕脱骨折三维分型推文"
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
