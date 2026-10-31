#!/usr/bin/env python3
"""《Lisfranc 关节复合体解剖：图解综述与手术入路》（Liu、Dalmau-Pastor 等 2026 KSSTA）推文。

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
    "Liu X, Hong CC, Torrent J, Del Vecchio J, Alcolea-Madera E, Dalmau-Pastor M. Anatomy of the Lisfranc joint complex: An illustrated review with surgical approach. Knee Surg Sports Traumatol Arthrosc. 2026;34:3178–3185. doi:10.1002/ksa.70260",
    "作者单位：西班牙巴塞罗那大学人体解剖与胚胎学教研室；遵义医科大学附属医院骨科；新加坡国立大学医院骨科；巴塞罗那 Rabat 足踝诊所 等",
    f"文章类型：{b('图解解剖综述')}（尸体标本照片 + 文献整理，附手术入路）；CC BY 开放获取",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"Lisfranc 关节复合体{b('不是一个关节')}，而是跖跗关节、跗骨间关节、近端跖骨间关节和一圈韧带组成的功能单元",
    f"{b('第 2 跖骨基底')}像“拱顶石”一样嵌在内侧楔骨（C1）和外侧楔骨（C3）之间，是整个复合体稳定的核心",
    f"{red('第 1、2 跖骨基底之间没有韧带')}，所以连接 C1 和 M2 的三条 Lisfranc 韧带（背侧、骨间、跖侧）至关重要；其中{b('骨间韧带最强')}，{b('背侧韧带最弱、最容易伤')}",
    f"榫卯越深、越宽越稳定；{b('第 2 跖骨相对越短越容易受伤')}；负重像上 {b('C1–M2 间距 ≥2 mm')} 提示不稳定",
    f"低能量单纯韧带伤漏诊可达 {b('20%')}，延误会导致慢性不稳、关节炎和畸形；手术多走{b('背内侧入路')}，复位从舟楔关系、M2 开始",
]))

A.append(h2("一、Lisfranc 关节复合体是什么"))
A.append(img(2))
A.append(cap("概念与损伤分型（据原文引言整理）"))
A.append(p(f"作者特别提到一个常被忽略的点：低能量运动伤导致的{b('单纯韧带损伤')}，症状轻微、影像不典型，{b('漏诊或误诊可达 20%')}。一旦延误，最常见的后果是关节炎，此外还有慢性中足不稳、疼痛和畸形。"))

A.append(h2("二、骨性结构"))
A.append(pic(3, "原文图 1（编者中文标注）  跖跗关节骨性成分呈弓形排列，背侧凸、足底侧凹。（a）楔骨和骰骨的前关节面（b）五块跖骨基底的后关节面"))
A.append(pic(4, "原文图 2（编者中文标注）  跖跗关节背面观：第 2 跖骨基底同时与 C1、C2、C3、M1、M3 相接触"))
A.append(pic(5, "原文图 3（编者中文标注）  跖跗关节足底面观：三块楔骨的“楔形”在中间楔骨（C2）处最明显，它的足底面很小"))
A.append(img(6))
A.append(cap("骨性结构要点（据原文整理）"))
A.append(p(f"可以把这一段概括成三个关键词：{b('阶梯错开、横弓、榫卯')}。第 2 跖骨基底比两边的 C1、C3 都“缩”进去，就像榫头插进卯眼里——C1 向前突出约 8 mm，C3 约 4 mm。这让跖跗关节几乎不动、非常稳定，也解释了为什么它一旦受伤就是大问题。"))
A.append(p(f"对手术有提示的一点：{b('M2 内侧对 C1 的关节面偏背侧')}，横穿 C1–M2 的螺钉有损伤关节软骨的风险。"))

A.append(h3("哪些骨性形态更容易受伤"))
A.append(pic(7, "据原文数字整理：骨性形态与 Lisfranc 损伤风险"))
A.append(ul([
    f"{b('榫卯内侧深度')}：越深越稳定，{b('每加深 1 mm，损伤可能性约降低 50%')}；浅的榫卯缺少宽厚的 Lisfranc 韧带保护。外侧深度则与损伤无明显关系",
    f"{b('第 2 跖骨长度 / 足长')}：比值{b('每降低 1%，损伤可能性增加到 1.82 倍')}；低于 29% 时尤其易伤。作者认为可作为运动、职业人群的筛查指标",
    f"{b('榫卯宽度')}：越宽，韧带越宽，越稳定",
    f"{b('影像')}：负重 CT 或负重 X 线上，{mk('C1–M2 间距 ≥2 mm')} 提示不稳定损伤，比 M1–M2 间距更准确、更敏感",
]))

A.append(h2("三、Lisfranc 韧带"))
A.append(pic(8, "原文图 4（编者中文标注）  稳定第 2 跖骨的背侧韧带：（1）C1–M1（2）背侧 Lisfranc 韧带（C1–M2）（3）C2–M2（4）C3–M2（5）C3–M3（6）M2–M3。注意 M1 和 M2 之间没有韧带"))
A.append(p(f"这张图最值得看的是{red('“缺了什么”')}：外侧几块跖骨基底之间都有背侧、跖侧韧带相连，唯独 {b('M1 和 M2 之间没有')}，只有薄弱的纤维组织。这里是天生的薄弱点，也正因为如此，C1 到 M2 的三条韧带才成为整个复合体的关键。"))
A.append(pic(9, "原文图 5（编者中文标注）  拆下第 1 跖骨后，从前方看 C1–M2 之间的三条 Lisfranc 韧带：（1）背侧（2）骨间（3）跖侧，跖侧分一束到 M2、一束到 M3"))
A.append(img(10))
A.append(cap("三条 Lisfranc 韧带（据原文整理）"))
A.append(img(15))
A.append(cap("三条韧带对比（编者据原文整理）"))
A.append(h3("力学强度：骨间韧带最强"))
A.append(pic(11, "据原文数字绘制：两项体外研究中三条韧带的刚度和失效载荷"))
A.append(table(["", "背侧（DLL）", "骨间（ILL）", "跖侧（PLL）"], [
    ["研究 A 刚度（N/mm）", "66.3 ± 18.3", "189.7 ± 57.2", "—"],
    ["研究 A 失效载荷（N）", "150.7 ± 33.1", "368.8 ± 126.8", "—"],
    ["研究 B 刚度（N/mm）", "40 ± 9", "90 ± 3", "62 ± 3"],
    ["研究 B 强度（N）", "170 ± 33", "449 ± 58", "305 ± 38"],
]))
A.append(p(f"两项研究结论一致：{b('骨间韧带最硬、最强')}（沿纤维方向加载时），背侧最弱。这也和临床相符——背侧韧带最先断，移位多向背侧。"))

A.append(h2("四、楔间韧带与两种不稳"))
A.append(pic(12, "原文图 6（编者中文标注）  C1、C2、M2 的内侧观，C1 背侧一半已沿矢状面切开，显示（1）C1–C2 骨间韧带（2）骨间 Lisfranc 韧带"))
A.append(img(13))
A.append(cap("楔间韧带与横向、纵向不稳（据原文整理）"))
A.append(table(["类型", "断裂的结构", "应力像表现"], [
    ["横向不稳", "骨间 + 跖侧 Lisfranc 韧带", "外展应力：C1–M2、C2–M2 都不稳"],
    ["纵向不稳", "骨间 Lisfranc 韧带 + C1–C2 骨间韧带", "内收应力：5 个标本中 4 个 C1–C2 不稳、1 个 C1–M2 不稳"],
]))
A.append(p(f"纵向不稳对应引言里的两种亚型：{b('内侧柱脱位（MCD）')}是 Lisfranc 韧带 + C1–C2 楔间韧带受伤；{b('近端延伸脱位（PE）')}再加上 C1–M1、C2–M2 韧带，更严重。"))

A.append(h2("五、手术解剖"))
A.append(img(14))
A.append(cap("手术入路与复位顺序（据原文整理）"))
A.append(ul([
    f"{b('背内侧入路')}：第 1、2 跖骨之间纵切口，多数 Lisfranc 损伤都累及第 2 跖跗关节，靠它就够了。要在{b('拇长伸肌腱和胫前血管神经束（足背动脉 + 腓深神经）之间')}进入，把血管神经束拉向外侧",
    f"{b('背外侧入路')}：累及第 3 跖跗关节或第 4、5 跖骨不稳时加做，沿第 4 跖骨轴线；注意{b('保护腓肠神经')}。两切口之间皮桥{b('至少 5 cm')}",
    f"{b('复位顺序')}：先恢复舟骨与楔骨的关系 → 再把 M2 对上 C2、C1（复位的基石）→ 依次处理第 1、3、4、5 跖跗关节",
    f"作者认为这类损伤几乎都有不稳成分、可能进展为畸形，{b('非手术治疗的作用很有限')}，解剖复位是重建稳定的关键",
]))

A.append(h2("原文对不上的地方"))
A.append(ul([
    f"说骨间 Lisfranc 韧带“{b('最窄但最厚')}”，但引用的三组数据里有一组宽 5.9 mm、厚 4.2 mm（宽大于厚），另一组厚 13.74 mm 却长只有 9.70 mm",
    f"“内侧足背皮神经（腓浅神经分支）常在{b('背内侧入路')}中遇到”这句话，被放在了描述{b('背外侧入路')}的段落里",
    f"两项生物力学研究的绝对数值相差约一倍（骨间韧带刚度 189.7 vs 90 N/mm），原文并列给出、没有解释",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Liu X, Hong CC, Torrent J, Del Vecchio J, Alcolea-Madera E, Dalmau-Pastor M. Anatomy of the Lisfranc joint complex: An illustrated review with surgical approach. Knee Surg Sports Traumatol Arthrosc. 2026;34:3178–3185. doi:10.1002/ksa.70260</em><br>"
    "原文为 CC BY 开放获取（© 2026 The Author(s)）。本文为中文解读：原文图 1～6 引自原文，编者在编号和骨名缩写旁加了中文名称，部分图下方加了中文图例条；其余整理卡和数据图由编者根据原文撰写、绘制。"
))
TITLE = "「足踝」Lisfranc 关节复合体：骨、韧带和手术入路，一篇图解解剖综述看懂"
PTITLE = "Lisfranc 关节复合体解剖推文"
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
