#!/usr/bin/env python3
"""腕管综合征注射水分离＋肌腱、神经滑动练习 1 例（Savage & Albano 2020）推文。

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
    "Savage NJ, Albano J. Marrying Tendon and Nerve Gliding Exercises with Hydrodissection Following Injection for Carpal Tunnel Syndrome – A New Treatment Approach? J Orthop Case Rep. 2020;10(9):38-46. doi:10.13107/jocr.2020.v10.i09.1896",
    "作者单位：美国犹他州 Total Rehab 物理治疗部、Albano 诊所",
    f"文章类型：{b('病例报告')}（1 例双侧腕管综合征，两侧手腕自身对照，随访 1 年）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"超声引导下腕管注射时同时做{b('正中神经水分离')}，把神经从粘连的结缔组织中“剥”开，注射后{b('立即开始主动肌腱、神经滑动练习')}",
    f"一位双侧腕管综合征患者，两侧随机打 {b('PRP')} 或{b('生理盐水')}：PRP 侧疼痛、症状、功能改善更快；{b('盐水侧也有明显改善')}",
    f"盐水侧 6 个月后补打 PRP，1 年时两侧症状和神经功能都比基线好，全程{b('无不良反应')}",
    f"但{red('只有 1 人')}，水分离和练习两侧都做了，练习本身的作用无法单独评价",
]))

A.append(h2("一、背景"))
A.append(img(2))
A.append(cap("腕管综合征和它的治疗（编者根据原文整理）"))
A.append(p(f"腕管综合征患者正中神经周围的{b('滑膜下结缔组织往往增厚、纤维化')}，神经滑动变差，被认为会让神经更容易受损。水分离就是针对这一点；而肌腱、神经滑动练习本来就是物理治疗的常用手段。作者的想法很直接：{mk('刚剥开粘连，就让神经和肌腱动起来')}。"))

A.append(h2("二、研究设计和注射"))
A.append(img(3))
A.append(cap("研究怎么做（原文）"))
A.append(img(4))
A.append(cap("注射和水分离（原文）"))
A.append(img(5))
A.append(cap("原文图 3：基线超声"))
A.append(p(f"按作者的分级标准，基线时{b('右腕为“中重度”、左腕为“中度”')}腕管综合征；水分离时右侧正中神经粘连更重，需要的注射液是左侧的两倍。"))

A.append(h2("三、注射后做哪些练习"))
A.append(img(6))
A.append(cap("练习处方（原文图 1、2 的说明栏，编者翻译）"))
A.append(img(7))
A.append(cap("原文图 1：肌腱滑动和正中神经滑动"))
A.append(img(8))
A.append(cap("原文图 2：收下巴和肩胛后缩"))
A.append(p(f"练习在注射后{b('症状允许时就开始')}，一直做到 2 个月复诊，患者用练习日志记录完成情况。收下巴和肩胛后缩是为了配合近端姿势，帮助神经滑动。"))

A.append(h2("四、结果"))
A.append(img(9))
A.append(cap("症状评分变化（据原文表 1、2 重画）"))
A.append(tcap("原文表 1：右腕（盐水 → 约 7 个月时补打 PRP）"))
A.append(table(["", "基线", "2 月", "4 月", "6 月", "1 年"], [
    ["最严重疼痛", "4", "3", "4", "4", "2"],
    ["症状 SSS", "2.9", "2.5", "2.9", "2.5", "1.6"],
    ["功能 FSS", "2.0", "1.3", "1.3", "1.4", "1.0"],
    ["感觉潜伏期 ms", "测不出", "5.5", "5.5", "5.5", "5.5"],
    ["感觉波幅 μV", "测不出", "5.2", "5.2", "5.2", "11"],
    ["运动潜伏期 ms", "6.6", "6.1", "5.8", "5.5", "5.3"],
    ["横截面积 mm²", "22", "22", "22", "21", "21"],
]))
A.append(tcap("原文表 2：左腕（PRP）"))
A.append(table(["", "基线", "2 月", "4 月", "6 月", "1 年"], [
    ["最严重疼痛", "4", "3", "1", "1", "0"],
    ["症状 SSS", "2.8", "1.5", "1.6", "1.1", "1.0"],
    ["功能 FSS", "1.9", "1.0", "1.0", "1.0", "1.0"],
    ["感觉潜伏期 ms", "4.9", "4.7", "4.6", "4.5", "4.5"],
    ["感觉波幅 μV", "6.2", "8.3", "8.9", "9.5", "18.4"],
    ["运动潜伏期 ms", "4.5", "4.4", "4.4", "4.4", "4.5"],
    ["横截面积 mm²", "15", "12", "17", "16", "14"],
]))
A.append(p(f"SSS、FSS 为 1～5 分，1 分表示无症状或无功能障碍。值得注意的是{b('盐水侧')}：原本测不出的感觉神经反应在 2 个月时出现，运动潜伏期逐渐缩短，功能评分也明显改善。作者认为这可能部分来自{b('水分离加滑动练习')}。两侧正中神经横截面积全程没有明显变化。"))

A.append(h2("这篇文章能信几分"))
A.append(img(10))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个患者')}，两侧病情轻重不同；没有“只注射、不练习”的对照，练习的贡献无法单独评价",
    "作者认为疗效“可与手术相当”，依据是与荟萃分析平均值的比较，属于间接对比",
    "优点：三盲、随机分配两侧手腕，电生理和超声检查者各自独立，随访到 1 年",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "右腕补打 PRP 的日期，正文写 2018 年 11 月 2 日，表 1 写 11 月 1 日",
    "讨论说本例波士顿问卷基线 46 分、6 个月 20 分，但正文和表格用的都是 1～5 分的平均分",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"腕管注射（尤其是做了水分离）后，可以在症状允许时{b('尽早开始肌腱、神经滑动练习')}，而不是一味制动",
    "肌腱滑动：固定其余手指，单独屈示指、中指；神经滑动：伸肘伸腕、转肩，配合上提下压肩胛带",
    "可配合收下巴、肩胛后缩等姿势练习；用日志记录完成情况，便于复诊调整",
    "PRP、水分离是否值得做，还需要更大样本的研究；本例只能作为思路参考",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Savage NJ, Albano J. Marrying Tendon and Nerve Gliding Exercises with Hydrodissection Following Injection for Carpal Tunnel Syndrome – A New Treatment Approach? J Orthop Case Rep. 2020;10(9):38-46. doi:10.13107/jocr.2020.v10.i09.1896</em><br>"
    "原文以知识共享署名-非商业性使用 3.0（CC BY-NC 3.0）协议开放获取，版权归原作者所有。本文为非商业的学术交流中文解读：原文图 1、2 裁去右侧英文说明栏（内容已译成中文），图 1～3 加了中文标签；评分图由编者根据原文表 1、2 重画；整理卡为编者根据原文撰写。仅供学习交流，如有侵权请联系删除。"
))
TITLE = "「手腕」腕管综合征注射水分离后，马上做肌腱和神经滑动练习？两侧手腕自身对照 1 年随访"
PTITLE = "腕管综合征水分离＋滑动练习推文"
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
