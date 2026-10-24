#!/usr/bin/env python3
"""Xiao 等 2016《经典康复训练中选定肌肉的表面肌电活动》（Rehabil Res Pract）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
配图：python3 tools/make_figs.py src/paper.pdf src/fig_zh images <中文字体>
     原文图 6～11 是矢量图，已用 tools/fig-translate 原位译成中文（译文见 src/fig_zh/strings.json）
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






# ---------- 正文 ----------
def cap(t):
    return f'<p style="margin:0 0 20px;font-size:12px;line-height:1.6;color:#888;">🔖{t}</p>'


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
    "Xiao J, Sun J, Gao J, Wang H, Yang X. The Activity of Surface Electromyographic Signal of Selected Muscles during Classic Rehabilitation Exercise. Rehabil Res Pract. 2016;2016:4796875. doi:10.1155/2016/4796875",
    "中文题目：经典康复训练中选定肌肉的表面肌电活动",
    "作者单位：河北大学电子信息工程学院；河北大学附属医院康复科",
    f"研究类型：横断面实验研究，{b('30 名健康研究生')}，表面肌电{b('中位频率')}分析",
], square=True))

A.append(h2("先说为什么要读这篇"))
A.append(p(
    f"平板支撑、臀桥、单腿桥、鸟狗式，几乎是每个核心训练方案里都有的四个动作。以往的肌电研究大多看{b('激活幅度')}"
    f"（%MVIC，相当于“这块肌肉用了几成力”），比如往期推文介绍过的 Ekstrom 2007。"
))
A.append(p(
    f"这篇换了一个角度：每个动作坚持 {b('1 分钟')}，看肌电信号的{b('中位频率')}随时间降得多快，"
    f"用它来反映{mk('哪块肌肉先累')}。而且除了腹肌和竖脊肌，还把{b('大腿和小腿肌肉')}也测了进来，这在以往研究里比较少见。"
))
A.append(p(
    "先交代一句：这篇的方法和数据问题不少（文末单独列出），结论要打折看。但“平板支撑时腿也在使劲”这类观察，对临床选动作有参考价值。"
))

A.append(h2("中位频率是什么"))
A.append(p(
    f"肌肉持续收缩、逐渐疲劳时，肌电信号的频谱会往低频移，{b('中位频率（MF）')}就随时间下降。"
    f"把 1 分钟内每秒的 MF 画出来，拟合一条直线，{b('斜率越负，说明疲劳越快')}。"
))
A.append(p(
    f"要注意，MF 斜率反映的是{b('疲劳')}，不是激活程度。一块肌肉用力不大但持续时间长，也可能慢慢疲劳；"
    "原文在不少地方把“疲劳快”说成“更活跃”，读的时候要区分开。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('受试者')}：30 名健康研究生，男女各 15 人，平均 24 岁，近一年腰、腹、腿无疼痛",
    f"{b('测哪些肌肉')}：竖脊肌（ES）、腹外斜肌（EO）、腹直肌（RA）、股直肌（RF）、股二头肌（BF）、胫骨前肌（AT）、腓肠肌（G），{b('左右两侧共 14 个通道')}",
    f"{b('设备')}：Noraxon 16 通道无线表面肌电，采样 1500 Hz",
    f"{b('动作')}：每个动作保持 1 分钟，中间休息 2 分钟，顺序随机",
    f"{b('分析')}：计算每秒的中位频率并做线性拟合；只分析{b('超过半数受试者出现疲劳')}的肌肉；左右两侧、不同肌肉之间用单因素方差分析比较",
]))
A.append(img(2))
A.append(h3("四个动作"))
A.append(ul([
    f"{b('仰卧臀桥')}：屈膝 90°，脚尖朝前，双手放体侧，把腹部（骨盆）抬起",
    f"{b('单腿臀桥')}：在仰卧臀桥基础上抬起一条腿；结果只分析了{b('抬右腿')}的情况",
    f"{b('平板支撑')}：肘和脚尖着地，身体与地面平行（原文叫 prone bridge，俯卧桥）",
    f"{b('鸟狗式')}：四点跪位，脊柱保持中立，抬起对侧的手和腿；结果只分析了{b('抬左臂和右腿')}",
]))
A.append(img(3))

A.append(h2("结果"))
A.append(h3("哪些肌肉有半数以上的人累了"))
A.append(img(4))
A.append(p(
    f"{b('平板支撑')}七块肌肉全部过半数，其中腹直肌最多（27 人）；{b('单腿臀桥')}六块过半数（腓肠肌没有）；"
    f"{b('鸟狗式')}五块（胫骨前肌、腓肠肌没有）；{b('仰卧臀桥')}只有三块，而且都只是刚过半数。"
))

A.append(h3("平板支撑：最累的是小腿和大腿后侧"))
A.append(img(5))
A.append(p(
    f"三块躯干肌里，腹直肌 MF 下降最快（−0.22 Hz/s），腹外斜肌其次，竖脊肌最平（−0.09）。"
    f"下肢肌肉更明显：{mk('腓肠肌 −0.71、股二头肌 −0.48')}，都比腹直肌还陡；股直肌和胫骨前肌与躯干肌差不多。"
))
A.append(p(
    f"作者据此认为平板支撑{b('不只是练腹肌')}，对大腿后侧和小腿也有明显的负荷。"
    "这和临床上的观察一致：很多人平板支撑撑不住，不一定是核心先垮，可能是脚尖撑地的小腿先酸。"
))

A.append(h3("仰卧臀桥：最轻松"))
A.append(img(6))
A.append(p(
    f"只有竖脊肌、腹直肌、股直肌达到半数左右，斜率都在 −0.15 Hz/s 以内，三块肌肉之间{b('没有显著差异')}。"
    f"这和以往 %MVIC 研究的结论一致：双腿仰卧桥是这几个动作里强度最低的（Czaprowski 2014 测腹肌时，仰卧桥的激活不到 5% MVC）。"
))

A.append(h3("单腿臀桥：明显比双腿桥累"))
A.append(img(7))
A.append(p(
    f"抬起一条腿后，过半数疲劳的肌肉从 3 块增加到 6 块，斜率也整体变陡。下降最快的是{b('胫骨前肌')}："
    f"抬起侧（右）−0.65，支撑侧（左）−0.43；竖脊肌两侧都在 −0.22 左右；腹直肌最平。"
))
A.append(p(
    f"左右两侧同名肌的斜率{b('没有统计学差异')}，但抬起侧整体略陡。作者的解释是抬起侧要对抗那条腿的重量，才能维持骨盆不掉。"
))

A.append(h3("鸟狗式：中等强度"))
A.append(img(8))
A.append(p(
    f"五块肌肉过半数疲劳，但斜率都不大（−0.05～−0.17 Hz/s），肌肉之间、左右之间都{b('没有显著差异')}。"
    f"抬起侧（右腿）的股二头肌下降最快，右侧腹外斜肌最平。作者把鸟狗式归为{b('中等强度、适合练耐力')}的动作。"
))

A.append(h3("中位频率斜率汇总"))
A.append(img(9))
A.append(tcap("各动作左侧肌肉的中位频率斜率（Hz/s，编者从原文图 6～11 的拟合方程整理）"))
A.append(table(["肌肉", "平板支撑", "仰卧臀桥", "单腿桥（抬右）", "鸟狗式"], [
    ["竖脊肌", "−0.09", "−0.14", "−0.22", "−0.16"],
    ["腹外斜肌", "−0.11", "—", "−0.15", "−0.09"],
    ["腹直肌", "−0.22", "−0.06", "−0.10", "−0.08"],
    ["股直肌", "−0.12", "−0.12", "−0.15", "−0.15"],
    ["股二头肌", "−0.48", "—", "−0.27", "−0.11"],
    ["胫骨前肌", "−0.20", "—", "−0.43", "—"],
    ["腓肠肌", "−0.71", "—", "—", "—"],
]))
A.append(small("“—”表示该动作中出现疲劳的人不到半数，原文没有分析。原文没有在不同动作之间做统计比较，横向看只能作参考"))

A.append(h2("作者的结论"))
A.append(quote(
    "For healthy people, we should do prone bridge exercise to train abdominal and calf muscles, do unilateral bridge exercise for back muscles, and do bird-dog exercise to balance our whole body muscles.",
    "对健康人来说，可以用平板支撑练腹肌和小腿肌肉，用单腿桥练背部肌肉，用鸟狗式平衡地练全身肌肉。"
))
A.append(img(10))

A.append(h2("这篇能信几分"))
A.append(ul([
    f"{b('测的是疲劳，不是激活')}：没有做 MVIC 标准化，所以无法回答“这个动作练到某块肌肉几成力”。标题和结论里的“activity（活动）”其实都是疲劳速度",
    f"{b('斜率没有按基线标准化')}：不同肌肉、不同动作的起始 MF 差别很大（28～101 Hz），直接比斜率大小会偏向起始频率高的肌肉。"
    f"例如按起始值折算，平板支撑竖脊肌每秒下降约 0.31%，仰卧臀桥竖脊肌约 0.19%，{b('结论与直接比斜率正好相反')}",
    f"{b('信号处理描述有硬伤')}：带通滤波写的是 80～250 Hz，可图中的中位频率大量低于 80 Hz（详见文末）",
    f"{b('统计方法偏弱')}：左右比较用单因素方差分析而不是配对检验；多块肌肉两两比较没提多重比较校正；“疲劳”的判定标准没有交代，而且只平均了被判为疲劳的受试者",
    f"{b('人群局限')}：30 名年轻无痛研究生，每个动作只做一次 1 分钟，不能直接推到下腰痛患者",
    "优点：把下肢肌肉纳入核心训练动作的肌电分析，四个动作的照片和电极位置清楚，可以作为“平板支撑也练腿”的一个参考",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('滤波范围和中位频率对不上')}：方法写 80～250 Hz 带通滤波，滤波后的信号中位频率应该落在 80 Hz 以上，"
    f"但图 6～10 里竖脊肌、腹直肌等的 MF 只有 28～50 Hz；而且按原文描述的顺序，是先全波整流、RMS 平滑后再算中位频率，整流会改变频谱，通常应在原始信号上做频谱分析",
    f"{b('胫骨前肌左右说反了')}：结果 3.1 写单腿桥“胫骨前肌最活跃，尤其是左侧”，但图 9(c) 和图 11(c) 显示右侧（抬起侧）−0.65 比左侧 −0.43 更陡，3.2 节也写的是右侧更累",
    f"{b('鸟狗式前后矛盾')}：3.2 节说鸟狗式“引起最多的肌肉疲劳”，摘要和讨论却说鸟狗式“不会引起太多疲劳”、属于中等强度",
    f"{b('表 2 写错动作')}：鸟狗式一行写成“抬左臂和右臂”，正文是抬左臂和右腿",
    f"{b('入选标准没守住')}：只分析“超过 50%”受试者疲劳的肌肉，但仰卧臀桥的腹直肌是 15/30，正好 50%，仍被纳入",
    f"{b('百分比和人数对不上')}：按 30 人算，腹直肌 27 人应为 90%（原文 91%），鸟狗式腹外斜肌 23 人应为 76.7%（原文 78%），仰卧桥股直肌 20 人应为 66.7%（原文 65%），竖脊肌 16 人同一个数在不同地方写成 52% 和 54%",
    f"{b('把腹肌叫成“下背肌”')}：结果里把竖脊肌、腹外斜肌、腹直肌统称为“low back muscles”；摘要结论又说平板支撑“影响下背和下肢肌肉”，可平板支撑里竖脊肌恰恰是疲劳人数最少、斜率最平的",
    f"{b('结论超出了数据')}：摘要说单腿桥比仰卧桥“激活更多”，讨论也做了不少动作间比较，但局限性里承认“没有比较同一块肌肉在不同动作中的水平”",
    f"{b('同一块肌肉的基线差得离谱')}：竖脊肌起始 MF 在平板支撑是 28 Hz，仰卧桥是 76 Hz；单腿桥左股直肌 47 Hz、右股直肌 73 Hz。同一批人、同一电极，差这么多原文没有解释",
    f"{b('引用撑不住论点')}：Czaprowski 2014 只测了腹肌，却被用来支持“竖脊肌疲劳高于腹外斜肌和腹直肌”；Ekstrom 2008 只测了胸最长肌和腰多裂肌，"
    f"摘要也只是把桥式、侧桥、四点跪位抬肢统归为 &lt;50% MVIC，却被引来说明“仰卧桥比平板支撑、鸟狗式激活更低”；Feldwieser 2012 只测躯干肌，被用来解释下肢左右差异（编者据 PubMed 摘要核对）",
    f"{b('统计用语错误')}：“confidence interval is set to 0.05”，应为显著性水平 α = 0.05",
    f"{b('时间对不上')}：每个动作做 1 分钟，图中横轴只到第 55～57 秒，没有说明截掉了哪一段",
]))

A.append(h2("落到临床"))
A.append(img(11))
A.append(cap("临床要点（编者整理）"))
A.append(ul([
    f"{mk('仰卧臀桥最轻松')}，适合放在核心训练的起点；加一条腿变成单腿桥，负荷明显上去",
    f"{b('平板支撑也在练腿')}：腓肠肌、股二头肌累得比腹肌还快，小腿或跟腱有问题的人可以先改跪姿平板或缩短时间",
    f"{b('鸟狗式强度适中')}，适合做耐力和控制训练",
    f"{b('看肌电文章先分清指标')}：%MVIC 回答“用了几成力”，中位频率斜率回答“累得多快”，两者不能互相替代",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Xiao J, Sun J, Gao J, Wang H, Yang X. The Activity of Surface Electromyographic Signal of Selected Muscles during Classic Rehabilitation Exercise. Rehabil Res Pract. 2016;2016:4796875. doi:10.1155/2016/4796875</em><br>"
    "编者核对引用时参考：Czaprowski D, et al. Phys Ther Sport. 2014;15(3):162-168. doi:10.1016/j.ptsp.2013.09.003；"
    "Ekstrom RA, et al. J Orthop Sports Phys Ther. 2008;38(12):736-745. doi:10.2519/jospt.2008.2865；"
    "Feldwieser FM, et al. Eur Spine J. 2012;21(Suppl 2):S171-S186. doi:10.1007/s00586-012-2254-7；"
    "Ekstrom RA, et al. J Orthop Sports Phys Ther. 2007;37(12):754-762. doi:10.2519/jospt.2007.2471（摘要信息来自 PubMed）<br>"
    "原文以知识共享署名协议（Creative Commons Attribution License，CC BY）开放获取。本文为中文解读：原文图 6～11 的图内英文已译成中文（数据和图形未改动），"
    "图 1～5 为原文照片，加了中文图注；表 2 热力图、斜率汇总表、首图、对比卡和临床要点卡为编者根据原文整理。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「核心训练肌电」平板、臀桥、单腿桥、鸟狗式，坚持 1 分钟谁先累？附原文对不上的地方"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>核心训练表面肌电推文</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
  :root { --ground:#ececec; --paper:#ffffff; color-scheme:light; }
  body { background:var(--ground); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
         padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:16px 32px; }
  .paper { max-width:640px; margin:0 auto; background:var(--paper); padding:20px 16px 28px; box-sizing:border-box; }
  .paper h1 { font-size:22px; line-height:1.4; margin:0 0 8px; color:#111; text-wrap:balance; }
  .paper .by { font-size:14px; color:#576b95; margin-bottom:20px; }
  .paper img { max-width:100%; }
  .paper table { display:block; overflow-x:auto; }
</style>
<div class="paper">
<h1>""" + TITLE + """</h1>
<div class="by">原创 · 骨科康复小黄</div>
""" + BODY + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
