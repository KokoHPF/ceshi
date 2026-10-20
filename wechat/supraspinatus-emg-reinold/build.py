#!/usr/bin/env python3
"""冈上肌与三角肌肌电分析：满罐、空罐、俯卧满罐（Reinold 等 2007）推文。

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
    "Reinold MM, Macrina LC, Wilk KE, Fleisig GS, Dun S, Barrentine SW, Ellerbusch MT, Andrews JR. Electromyographic analysis of the supraspinatus and deltoid muscles during 3 common rehabilitation exercises. J Athl Train. 2007;42(4):464-469.",
    "作者来自波士顿红袜队、美国运动医学研究所（ASMI）等，Wilk、Andrews 都是肩关节康复领域的老牌名字",
    "实验室重复测量研究（同一批人做三个练习）",
], square=True))

A.append(h2("先说为什么要比这三个练习"))
A.append(p(
    f"肩袖的工作是把肱骨头“摁”在关节盂里，抵消三角肌往上拉的力。冈上肌受伤或无力，肱骨头就容易往上跑，撞到肩峰。"
    f"所以{b('练冈上肌')}几乎是所有肩关节康复方案的标配。"
))
A.append(p(f"但到底用哪个动作练，一直有争论："))
A.append(ul([
    f"{b('空罐')}：Jobe 最早推荐，肩胛平面上举 + 内旋（拇指朝下），像把罐子里的水倒空",
    f"{b('满罐')}：肩胛平面上举 + 外旋（拇指朝上），不少作者认为更好",
    f"{b('俯卧满罐')}：Blackburn 报告俯卧位外展 100° 外旋做水平外展时冈上肌激活更高",
]))
A.append(p(
    f"以往研究要么没把三个都比，要么没看三角肌，要么没做统计。作者认为{mk('理想的冈上肌练习，应该是冈上肌激活够高、同时三角肌激活尽量低')}，"
    f"于是用针电极把三个练习放在一起比。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：{b('22 名健康人')}（男 15、女 7，平均 26.7 岁），都没有肩痛、肩伤或不稳的病史；测优势侧",
    f"用{b('细钢丝针电极')}插进冈上肌、三角肌中束、三角肌后束（冈上肌在肩胛冈中点上方 1.5 cm 进针，直达冈上窝）",
    "先测每块肌肉的最大自主等长收缩（MVIC），练习时的肌电峰值用 MVIC 的百分比表示",
    "三个练习随机顺序，各做 5 次，取第 2～4 次的峰值平均",
]))

A.append(h2("重点：三个练习怎么做"))
A.append(pic(4, "三个练习的做法（编者根据原文整理）"))
A.append(h3("满罐 vs 空罐"))
A.append(pic(2, "原文图 1、2：左为满罐，右为空罐（背景球衣名字和衣服品牌已模糊处理）"))
A.append(ul([
    f"站立，手持哑铃，手臂在{b('肩胛平面')}（额状面往前约 30°）从体侧上举到 {b('90°')}，再慢慢放下",
    f"{b('满罐')}：{mk('肩外旋、拇指朝上')}",
    f"{b('空罐')}：肩内旋、拇指朝下",
    "两者唯一的区别就是手臂旋转方向",
]))
A.append(h3("俯卧满罐"))
A.append(pic(3, "原文图 3：俯卧满罐（背景球衣已模糊处理）"))
A.append(ul([
    f"俯卧在治疗床边，手臂自然垂下",
    f"在约 {b('100° 外展')}位做{b('水平外展')}，肩外旋、拇指朝上",
    f"{mk('举到末端就停，一出现代偿动作就停')}（由研究者在旁边盯着）",
]))
A.append(h3("负荷和节奏（三个练习统一）"))
A.append(ul([
    f"重量：每人每个练习用 {b('10RM')}（能保持标准姿势和节奏做 10 次的最大重量）；平均满罐、空罐 1.85 kg，俯卧满罐 1.53 kg",
    f"节奏：{b('节拍器每分钟 60 拍')}，上举 1 拍、放下 1 拍",
    "每个练习做 5 次，练习之间休息 3～5 分钟",
]))
A.append(p(f"注意重量很轻，{red('只有 1.5～2 kg 左右')}。这类练习本来就是低负荷、高质量控制的肩袖练习，不是大重量力量训练。"))

A.append(h2("结果：冈上肌差不多，三角肌差得多"))
A.append(pic(5, "主要结果（编者按原文表格数值重绘）"))
A.append(ul([
    f"{b('冈上肌')}：满罐 62%、空罐 63%、俯卧满罐 67% MVIC，{mk('三个练习没有差别')}（P = 0.807）",
    f"{b('三角肌中束')}：空罐 77%、俯卧满罐 63% 都比满罐 52% 高",
    f"{b('三角肌后束')}：俯卧满罐 87% 最高，空罐 54% 次之，满罐 38% 最低",
]))
A.append(p(
    f"所以作者的结论是：{mk('满罐能拿到和另外两个一样的冈上肌激活，同时三角肌最“安静”')}，"
    f"最适合用来练冈上肌，也适合做冈上肌的徒手肌力测试；空罐偏向练三角肌中束，俯卧满罐偏向练三角肌后束。"
))
A.append(h3("为什么三角肌少一点更好"))
A.append(pic(6, "原文图 4：上举到不同角度时盂肱关节合力方向。“中”为中立位，“外”为外旋（类似满罐），“内”为内旋（类似空罐）。原图引自 Poppen 和 Walker 1978"))
A.append(p(
    f"图 4 显示：在 30°、60° 上举时，{b('内旋（空罐）的合力明显指向上方')}，也就是更多往上的剪切力；外旋（满罐）的合力更朝向关节盂中心。"
))
A.append(pic(7, "原文图 5：A 为三角肌、B 为冈上肌、C 为两者合力在不同上举角度的方向。原图引自 Morrey 等《The Shoulder》1998"))
A.append(p(
    f"图 5 显示：单独三角肌在 30°～120° 时把肱骨头往上拉；冈上肌全程都在把肱骨头往关节盂里压。"
    f"作者据此推论：{red('三角肌相对冈上肌越活跃，肱骨头越容易上移、越容易撞击')}，这可能也是很多患者做空罐时会痛的原因。"
    f"此外满罐位肩峰下间隙更大、冈上肌力臂更长。"
))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b("冈上肌“没差别”不等于“一样”")}：冈上肌的标准差高达 40%～50% MVIC，而样本量是按“差值标准差 15%”算的，{red('真实变异比预想大得多，有差别也很可能测不出来')}",
    f"{b('都是健康人')}：没有一个肩痛或肩袖损伤的人，“对患者更安全”是推论，不是测出来的",
    f"{b('肌电 ≠ 力')}：三角肌肌电高，不代表一定产生了更多向上剪切力，更不等于更容易撞击；从肌电到“肱骨头上移”这一步是作者的推论",
    f"{b('只测了 3 块肌肉')}：没看冈下肌、肩胛下肌、三角肌前束和肩胛周围肌肉，而空罐时三角肌前束很可能更活跃",
    f"{b('只看峰值')}：每个练习只取峰值的 % MVIC，没看整个动作过程中激活的时间和分布",
    f"{b('采样率偏低')}：960 Hz 采样，作者自己也承认可能影响绝对数值",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('摘要和正文 P 值不一致')}：摘要说空罐和满罐的三角肌中束比较 P = .001，正文写的是 t₁₇ = 2.838、P = .011，按 t 值复算也是 0.011，{red('摘要多写了一个 0')}",
    f"{b('摘要和表格标准差不一致')}：摘要里空罐的三角肌后束是 54 ± 24% MVIC，表格里是 54 ± 28",
    f"{b('每块肌肉实际分析的人数不一样，原文没交代')}：入组 22 人，但从自由度反推，冈上肌是 21 人（F₂,₄₀）、三角肌中束 18 人（t₁₇、F₁.₂₉,₂₁.₈₉）、三角肌后束 20 人（t₁₉），少掉的数据去哪了没说",
    f"{b('表格里的“范围”其实是 95% 置信区间')}：比如冈上肌满罐 62 ± 40、“范围”44～80，均值±40 的数据不可能最小 44、最大 80；按 95% CI 复算正好对上",
    f"{b('仪器参数写错')}：“平均增益在 960 Hz 到 1040 Hz 之间”，增益没有 Hz 这个单位；另外放大器带宽到 1000 Hz，采样率却只有 960 Hz，不满足采样率至少是信号最高频率 2 倍的要求",
    f"{b('“肩胛平面”的两种说法')}：方法里说肩胛平面是“额状面前方 30°”，图 1、图 2 图注却写成“约 30° 水平外展”，按常用的量法这两种说法差了 30°，容易让人照错",
    f"{b('哑铃重量')}：说每个练习各自测 10RM，但满罐和空罐的平均重量和标准差完全一样（1.85 ± 0.64 kg），看起来更像两个练习用了同一个重量",
    f"{b('小错')}：960 Hz 采样率引用的是 Worrell 等的文献（参考文献 22）；参考文献 4 作者 “De Duca” 应为 De Luca；讨论里把健康受试者称作“无症状患者”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('练冈上肌，首选满罐')}：拇指朝上、肩胛平面上举到 90°，冈上肌激活不输另外两个，三角肌最少，对肩痛、肩袖无力的人更友好",
    f"{b('空罐尽量少用来练')}：内旋位上举时三角肌中束更活跃、合力更偏上，肩峰下间隙也更小，患者常会痛；可以留作诱发试验，看肩袖能不能稳住肱骨头",
    f"{b('俯卧满罐适合后侧')}：三角肌后束激活最高，适合需要练肩后侧的人；但对冈上肌并没有额外优势，肩痛急性期慎用",
    f"{b('徒手肌力测试')}：测冈上肌也可以优先用满罐位，三角肌的干扰更小",
    f"负荷参考：{b('10RM、1～2 kg 小哑铃、上下各 1 秒')}，动作标准、没代偿比重量更重要",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表　三个练习中各肌肉的肌电活动（% MVIC）"))
A.append(table(["肌肉", "满罐", "空罐", "俯卧满罐", "重复测量方差分析 P"], [
    ["冈上肌", "62 ± 40<br>（44～80）", "63 ± 45<br>（44～83）", "67 ± 50<br>（44～89）", "0.807"],
    ["三角肌中束", "52 ± 27<br>（39～65）", "77 ± 44<br>（55～99）", "63 ± 31<br>（48～79）", "<b>0.029*</b>"],
    ["三角肌后束", "38 ± 32<br>（23～53）", "54 ± 28<br>（41～67）", "87 ± 53<br>（62～111）", "<b>0.001*</b>"],
]))
A.append(small("数值为均值 ± 标准差，括号内原文标为“范围”，按复算应为 95% 置信区间。* 表示三个练习之间差异有统计学意义。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Reinold MM, Macrina LC, Wilk KE, Fleisig GS, Dun S, Barrentine SW, Ellerbusch MT, Andrews JR. Electromyographic analysis of the supraspinatus and deltoid muscles during 3 common rehabilitation exercises. J Athl Train. 2007;42(4):464-469.</em><br>"
    "原文版权归美国国家运动防护师协会（NATA）所有，可在 PubMed Central 免费阅读，但未采用知识共享（CC）开放许可。本文为学术交流用的中文解读：练习照片引自原文图 1～3（背景文字已模糊），"
    "图 4、图 5 原文本身转载自 Poppen 和 Walker 1978 及 Morrey 等 1998（编者反相并将标注改为中文），结果图为编者按原文表格重绘，方案卡为编者整理绘制，表格为编者翻译。版权归原作者与出版方，如有侵权请联系删除。"
))

TITLE = "「肩袖」练冈上肌：满罐、空罐还是俯卧满罐？针电极肌电告诉你"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>冈上肌肌电推文</title>
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
<div class="by">原创 · 悦美力</div>
""" + BODY + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
