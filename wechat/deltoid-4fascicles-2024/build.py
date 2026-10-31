#!/usr/bin/env python3
"""《三角韧带恒定由四束组成》（Dalmau-Pastor 等 2024 KSSTA）推文。

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
    "Dalmau-Pastor M, Malagelada F, Guelfi M, Kerkhoffs G, Karlsson J, Calder J, Vega J. The deltoid ligament is constantly formed by four fascicles reaching the navicular, spring ligament complex, calcaneus and talus. Knee Surg Sports Traumatol Arthrosc. 2024;32:3065–3075. doi:10.1002/ksa.12173",
    "作者单位：西班牙巴塞罗那大学人体解剖与胚胎学教研室；英国伦敦皇家医院；荷兰阿姆斯特丹大学医学中心；瑞典哥德堡大学 等",
    f"文章类型：{b('尸体解剖研究（图解论文）')}，32 例新鲜冷冻标本；CC BY 开放获取",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"三角韧带（踝内侧副韧带）{b('恒定由四束、两层组成')}，按“连到哪块骨”命名即可，不必记文献里的 16 种束",
    f"{b('浅层三束')}都起于内踝前丘：{b('胫舟束')}→舟骨、{b('胫弹簧束')}→弹簧韧带、{b('胫跟束')}→跟骨载距突",
    f"{b('深层一束')}：{b('胫距束')}，从内踝的关节内一侧到距骨内侧，止点和距骨内侧关节面像{b('太极图')}一样互补",
    f"以往说胫跟束“不恒定”，很可能是解剖时{b('剥离肌腱鞘误切')}了它",
    f"{red('胫距束全部和胫舟束前部在关节内')}（滑膜外），作者推测这可能是深层三角韧带损伤更难愈合的原因",
]))

A.append(h2("一、为什么要重新数三角韧带"))
A.append(img(2))
A.append(cap("研究背景（据原文引言整理）"))
A.append(p(f"踝扭伤大多是内翻扭伤，但扭伤后 30%～40% 留下慢性疼痛、最多 33% 发展为慢性踝关节不稳，而其中{b('最多 40% 同时有三角韧带损伤')}。问题是三角韧带的解剖描述太乱：常用的“两层六束”里就有不恒定的束，各家又陆续添加，{b('累计多达 16 种')}，临床报告、修复和重建时很难说清到底伤的是哪一部分。"))

A.append(h2("二、怎么做的"))
A.append(img(3))
A.append(cap("研究方法（据原文整理）"))
A.append(pic(4, "原文图 1（编者中文标注）  浅层解剖的前四步"))
A.append(pic(5, "原文图 2（编者中文标注）  踝前关节囊与三角韧带前部的关系；右图掀起关节囊，可见胫舟束外缘与关节囊相延续"))
A.append(pic(6, "原文图 3（编者中文标注）  切开下胫腓联合，从关节内观察深层"))
A.append(p(f"这项研究的关键在于{b('“里外都看”')}：浅层从内侧（关节外）看，深层不剥离浅层，而是{b('切开下胫腓联合、把胫骨翻开，从关节内看')}。作者提醒，切除胫后肌腱、趾长屈肌腱腱鞘（第 3 步）和小腿前群肌腱（第 5 步）时最容易误切胫跟束和胫舟束。"))

A.append(h2("三、结果：两层、四束"))
A.append(img(7))
A.append(cap("四束的起止（据原文结果整理）"))
A.append(table(["层次", "名称", "起点", "止点", "关节内/外"], [
    ["浅层", "胫舟束", "内踝前丘前部", "舟骨上内侧", "前部在关节内"],
    ["浅层", "胫弹簧束", "内踝前丘中部", "跟舟内上韧带上缘", "关节外"],
    ["浅层", "胫跟束", "内踝前丘后部", "载距突上缘", "关节外"],
    ["深层", "胫距束", "前丘外侧、后丘内外侧", "距骨内侧关节面下方", "关节内"],
]))
A.append(pic(8, "原文图 4（编者中文标注）  三角韧带全貌，标出四束"))
A.append(pic(9, "原文图 5（编者中文标注）  移除距骨后看浅层三束的止点"))
A.append(pic(10, "原文图 6（编者中文标注）  胫骨下端：浅层起于内踝内侧面，深层起于外侧（关节内）、紧贴软骨"))
A.append(pic(11, "原文图 7（编者中文标注）  从表面能看到的四个止点：舟骨、弹簧韧带、载距突、距骨后内侧结节"))
A.append(h3("附着宽度"))
A.append(pic(12, "据原文表 1、表 2 绘制"))
A.append(p(f"浅层三束都是{b('远端比近端宽')}（P < 0.05），胫舟束最明显，从 4.1 mm 展开到 14.9 mm，呈扇形。深层胫距束按起点分三段：前丘前部同样向远端展开；前丘、后丘两段宽度变化不大，近似直带。"))
A.append(pic(13, "原文图 8（编者中文标注）  胫距束距骨止点与距骨内侧关节面呈“太极”互补"))

A.append(h2("四、临床意义"))
A.append(img(14))
A.append(cap("讨论要点（据原文整理）"))
A.append(p(f"作者把深层三角韧带类比为膝{b('前交叉韧带')}和距腓前韧带上束：它们都在关节内、滑膜外，断裂后残端可能重新被滑膜包裹，妨碍愈合。这{b('只是假设')}，目前没有研究直接证实；而且踝部韧带两端距离短、不完全断裂常见，又可能有利于愈合。"))
A.append(img(15))
A.append(cap("研究局限（据原文整理）"))

A.append(h2("原文对不上的地方"))
A.append(ul([
    f"正文说浅层每一束“{b('所有标本')}都是远端比近端宽”，但表 1 胫跟束远端最小值 {b('2.36 mm')}，比近端最小值 4.25 mm 还窄，说明至少有一例并非如此",
    f"说深层两段是“{b('近乎等宽的直带')}”，表 2 却显示前丘段远端（8.84 mm）明显比近端（9.67 mm）窄，P = 0.0226",
    f"深层分段的定义前后不一：先把 PostC 写成“后丘”，紧接着又写成“{b('前丘以后')}”",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Dalmau-Pastor M, Malagelada F, Guelfi M, Kerkhoffs G, Karlsson J, Calder J, Vega J. The deltoid ligament is constantly formed by four fascicles reaching the navicular, spring ligament complex, calcaneus and talus. Knee Surg Sports Traumatol Arthrosc. 2024;32:3065–3075. doi:10.1002/ksa.12173</em><br>"
    "原文为 CC BY 开放获取（© 2024 The Authors）。本文为中文解读：原文图 1～8 引自原文，编者在编号旁加了中文名称，部分图下方加了中文图例条；附着宽度图据原文表 1、表 2 绘制，其余整理卡由编者根据原文撰写。"
))
TITLE = "「足踝」三角韧带到底几束？32 例标本给出答案：恒定四束、两层"
PTITLE = "三角韧带四束解剖推文"
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
