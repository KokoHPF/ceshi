#!/usr/bin/env python3
"""严重压砸伤致 Lisfranc 骨折的多学科处理与康复 1 例（Nangliya 等 2024）推文。

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
    "Nangliya R, Nandanwar SP, Deshpande M. Multidisciplinary Management and Rehabilitation of Severe Crush Injury Resulting in Lisfranc Fracture: A Case Report. Cureus. 2024;16(2):e54473. doi:10.7759/cureus.54473",
    "作者单位：印度 Datta Meghe 高等教育研究院 Ravi Nair 物理治疗学院肌骨物理治疗科",
    f"文章类型：{b('病例报告')}（1 例）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"58 岁男性被公交车撞伤左足：{b('Lisfranc 骨折＋全部楔骨和骰骨骨折＋足跟脂肪垫撕脱')}，伤口 20 cm、骨外露",
    f"清创＋克氏针固定后，按{b('六期')}推进物理治疗：先不负重、练髋膝核心，第 6～10 周行走靴下完全负重，第 11 周后脱靴、练踝和步态，第 13 周起加本体感觉",
    f"康复后：下肢功能量表 {b('26 → 58')}（满分 80），Olerud-Molander 踝评分 {b('10 → 75')}，疼痛 8 → 1 分",
    f"但{red('只有 1 例')}，方案偏通用模板，评估时间点也前后不一",
]))

A.append(h2("一、什么是 Lisfranc 损伤"))
A.append(img(2))
A.append(cap("背景（编者根据原文整理）"))
A.append(p(f"Lisfranc 关节就是{b('跖跗关节')}，连接中足的跗骨和前足的跖骨。原文把它的特征概括为{b('内侧楔骨与第 2 跖骨底之间')}的连接被外伤破坏。原文提到，这类损伤{b('漏诊、延误诊断')}与长期残疾相关。"))

A.append(h2("二、病例"))
A.append(img(3))
A.append(cap("伤情和术后评估（原文）"))
A.append(img(4))
A.append(cap("原文图 1、2：术前、术后 X 线"))
A.append(img(5))
A.append(cap("用药（原文表 3）"))

A.append(h2("三、六期康复方案"))
A.append(img(6))
A.append(cap("第 1～10 周（原文表 4）"))
A.append(img(7))
A.append(cap("第 11 周以后（原文表 4）"))
A.append(p(f"方案的主线是{mk('先保护、再负重、后功能')}：前 10 周在拐杖、行走靴保护下，把力气花在{b('髋、膝和核心')}上，防止制动带来的肌萎缩和僵硬；踝的主动活动要等医生评估（第 6～8 周）后才开始；脱靴后再练踝、步态和本体感觉。"))
A.append(img(8))
A.append(cap("原文图 3"))
A.append(img(9))
A.append(cap("原文图 4：动态股四头肌练习"))

A.append(h2("四、结果"))
A.append(img(10))
A.append(cap("结局量表变化（据原文表 5 重画）"))
A.append(tcap("原文表 6、7：左下肢肌力和活动度（康复前 → 康复后）"))
A.append(table(["项目", "康复前", "康复后"], [
    ["左膝屈曲", "0°～20°", "0°～100°"],
    ["左踝背伸", "0°～5°", "0°～15°"],
    ["左踝跖屈", "0°～10°", "0°～40°"],
    ["左髋屈曲", "0°～105°", "0°～115°"],
    ["左膝屈伸肌力", "2/5", "4/5"],
    ["左踝背伸、跖屈肌力", "2/5", "4/5"],
    ["左髋各组肌力", "3/5", "5/5"],
]))
A.append(p(f"值得注意的是，原文记录的{b('右侧（未受伤侧）')}髋、膝、踝肌力在康复前也都只有 3/5，康复后到 5/5。原文没有解释原因，但提示评估和训练不能只盯着患侧。"))

A.append(h2("这篇文章能信几分"))
A.append(img(11))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例')}、没有对照，随访时间短",
    "康复方案提到“移植物”“融合关节”，像是 Lisfranc 融合术后的通用方案，和本例克氏针固定并不完全对应",
    "引言和讨论提到的电疗、针灸、蜡疗、贴扎，在具体方案里没有写剂量和时间",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "评估时间点前后不一：表 5 写第 3 天和第 8～12 周，表 6 写第 7 天和第 3 周，表 7 写第 7 天和第 5 周",
    "表 1 说术后左踝活动度无法评估、表 2 左踝肌力为“－”，表 6、7 的康复前数据却是背伸 5°、跖屈 10°、肌力 2/5",
    "摘要写“乘用车事故”，正文写“被公交车撞伤”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"Lisfranc 骨折术后早期{b('不负重')}，但髋、膝、核心和健侧都要尽早练",
    "踝的主动活动和负重进度以手术医生的评估为准；行走靴下完全负重 → 脱靴 → 步态和本体感觉逐步过渡",
    "评估不只看踝：膝屈曲、健侧肌力、焦虑抑郁等都可能受影响",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Nangliya R, Nandanwar SP, Deshpande M. Multidisciplinary Management and Rehabilitation of Severe Crush Injury Resulting in Lisfranc Fracture: A Case Report. Cureus. 2024;16(2):e54473. doi:10.7759/cureus.54473</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～4 引自原文，中文说明见图注；结局量表图由编者根据原文表 5 重画；整理卡为编者根据原文撰写。"
))
TITLE = "「足部」压砸伤致 Lisfranc 骨折，术后怎么练？六期康复方案和 1 例结果"
PTITLE = "Lisfranc 骨折术后康复推文"
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
