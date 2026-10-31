#!/usr/bin/env python3
"""《3D 容积 MRI 可识别踝外侧韧带各束及外侧腓距跟韧带复合体》（Hong、Calder 等 2022 KSSTA）推文。

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
    "Hong CC, Lee JC, Tsuchida A, Katakura M, Jones M, Mitchell AW, Dalmau-Pastor M, Calder J. Individual fascicles of the ankle lateral ligaments and the lateral fibulotalocalcaneal ligament complex can be identified on 3D volumetric MRI. Knee Surg Sports Traumatol Arthrosc. 2022 (published online 20 December 2022). doi:10.1007/s00167-022-07275-x",
    "作者单位：伦敦 Fortius 诊所（FIFA 医学卓越中心）；新加坡国立大学医院；巴塞罗那大学人体解剖教研室；伦敦帝国理工学院 等",
    f"文章类型：{b('前瞻性先导研究')}（30 名健康志愿者 3T MRI），证据等级 Ⅲ",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"在 3T、0.5 mm 层厚的 3D MRI 上，{b('86.7%')} 的健康踝能分清距腓前韧带（ATFL）的{b('上、下两束')}",
    f"上束明显更大：平均长 18.4 mm、宽 4.7 mm，比下束{b('长 39%、宽 80.7%')}；只有一束的踝，大小和上束相近",
    f"首次在 MRI 上看到连接 ATFL 下束和跟腓韧带（CFL）的{b('弓状纤维')}：双束者 84.6%、单束者 75% 可见",
    f"ATFL–距腓后韧带连接 63.3%，CFL–距腓后韧带连接 70%；{b('5 例')}两束之间可见穿支动脉",
    f"意义：MRI 上{b('有望单独诊断上束损伤')}（“微不稳”），弓状纤维是否完好可能影响{b('能否只修 ATFL')}",
]))

A.append(h2("一、为什么要分束看距腓前韧带"))
A.append(img(2))
A.append(cap("研究背景（据原文引言整理）"))
A.append(pic(4, "原文图 1  解剖标本中的外侧腓距跟韧带复合体（原图未改动，中文对照见图注）"))
A.append(p(f"简单说：ATFL 有两束。{b('上束在关节内')}，泡在滑液里，伤了可能长不好，引起查体不明显的轻微不稳和慢性前外侧痛（“微不稳”）；{b('下束在关节外')}，通过弓状纤维和 CFL 连成一体（LFTCL 复合体），是踝外侧的等长稳定结构。此前还没有 MRI 研究描述过弓状纤维。"))

A.append(h2("二、怎么做的"))
A.append(img(3))
A.append(cap("研究方法（据原文整理）"))

A.append(h2("三、结果"))
A.append(h3("1. 两束还是一束"))
A.append(pic(5, "原文图 2  矢状位 MRI 上的 ATFL 两束"))
A.append(pic(6, "原文图 3  只有一束的 ATFL"))
A.append(pic(7, "据原文结果绘制：各束大小"))
A.append(table(["", "长度 mm（范围）", "宽度 mm（范围）"], [
    ["双束·上束（n = 26）", "18.4（10.8～23.4）", "4.7（1.8～6.8）"],
    ["双束·下束（n = 26）", "13.2（8.0～16.7）", "2.6（1.4～3.8）"],
    ["单束（n = 4）", "17.3（16.7～18.0）", "5.9（4.3～7.8）"],
]))
A.append(small("上、下束长度和宽度差异均 P < 0.001；单束与上束差异无统计学意义。年龄、性别对束数和大小均无影响。"))
A.append(h3("2. 弓状纤维和各韧带之间的连接"))
A.append(pic(8, "原文图 4  ATFL 下束经弓状纤维连到 CFL"))
A.append(pic(9, "原文图 5  ATFL 与距腓后韧带相连"))
A.append(pic(10, "原文图 6  CFL 与距腓后韧带相连"))
A.append(h3("3. 两束之间的穿支动脉"))
A.append(pic(11, "原文图 7  ATFL 两束之间的穿支动脉"))
A.append(pic(12, "据原文表 1 绘制：各结构检出率"))

A.append(h2("四、作者怎么解读"))
A.append(pic(13, "据原文讨论整理：不同 MRI 研究中双束 ATFL 的检出率"))
A.append(img(14))
A.append(cap("讨论要点（据原文整理）"))
A.append(p(f"对临床最有用的两点：一是{b('分束诊断')}——以后读 MRI 时可以专门看上束，帮助解释“查体不松但总觉得不稳、前外侧痛”的患者；二是{b('弓状纤维')}——它能把张力从 ATFL 传到 CFL，这是“只修 ATFL 也能稳”的解剖基础，但前提是 CFL 断在近端、弓状纤维还在。"))
A.append(img(15))
A.append(cap("研究局限（据原文整理）"))

A.append(h2("原文对不上的地方"))
A.append(ul([
    f"说 4 个单束踝和上束“大小相近”，但单束平均宽 {b('5.9 mm')}，比上束 4.7 mm 宽约四分之一，只是 4 例样本太少测不出差异",
    f"摘要写上束“{b('在所有标本中')}都明显更大”，但上束长度最小 10.8 mm、下束最大 16.7 mm，范围重叠，文中没给逐例对比，无法核实",
    f"研究对象全是{b('健康志愿者')}，没有一例损伤，摘要却说结果“支持在 LFTCL 复合体完好时单独修复 ATFL”，属于推论",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Hong CC, Lee JC, Tsuchida A, Katakura M, Jones M, Mitchell AW, Dalmau-Pastor M, Calder J. Individual fascicles of the ankle lateral ligaments and the lateral fibulotalocalcaneal ligament complex can be identified on 3D volumetric MRI. Knee Surg Sports Traumatol Arthrosc. 2022. doi:10.1007/s00167-022-07275-x</em><br>"
    "原文版权归作者，独家授权欧洲运动创伤、膝关节外科与关节镜学会（ESSKA），非开放获取。本文为非商业的学术交流中文解读：原文图 1～7 按原样引用、未作修改，中文对照写在图注中；数据图由编者根据原文表 1 和讨论绘制，其余整理卡为编者根据原文撰写。仅供学习交流，如有侵权请联系删除。"
))
TITLE = "「足踝」距腓前韧带其实有两束！3D MRI 能分清，还能看到连接跟腓韧带的弓状纤维"
PTITLE = "踝外侧韧带分束 MRI 推文"
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
