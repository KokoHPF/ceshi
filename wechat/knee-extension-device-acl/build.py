#!/usr/bin/env python3
"""伸膝装置围手术期康复＋关节镜松解治疗关节纤维化（Biggs-Kinzer 等 2010）推文。

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
    "Biggs-Kinzer A, Murphy B, Shelbourne KD, Urch S. Perioperative Rehabilitation Using a Knee Extension Device and Arthroscopic Debridement in the Treatment of Arthrofibrosis. Sports Health. 2010;2(5):417-423. doi:10.1177/1941738110379088",
    "作者单位：美国印第安纳波利斯卫理公会医院 Shelbourne 膝关节中心",
    f"文章类型：{b('回顾性病例系列')}（33 人，没有对照组）",
    f"{red('利益冲突')}：作者之一 Shelbourne 是伸膝装置生产公司（Kneebourne Therapeutics）的顾问",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"{b('关节纤维化')}是关节内外纤维组织异常增生，导致疼痛、活动度丢失、僵硬、无力、肿胀和功能受限，常见于{b('前交叉韧带重建')}和全膝置换之后，发生率报告在 {b('4%～35%')}。"
))
A.append(p(
    f"治疗以手术为主（关节镜松解、手法松解、开放清理），康复方面的报道很少，多是系列石膏和伸直支具——这些方法{b('费时费钱')}（每天治疗、反复打石膏），而且很少报告最终能否恢复到“正常”活动度和功能。"
))
A.append(p(f"作者从 2003 年起在关节镜清理前后配合使用{mk('患者自己操作的伸膝装置')}，这篇回顾了效果。"))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：33 名在外院手术或保守治疗失败后来就诊的关节纤维化患者，女 19 人、男 14 人，平均 31 岁；{b('27 人')}发生在前交叉韧带重建后，6 人在其他手术或并发症后",
    f"{b('治疗')}：所有人都做术前康复 → 关节镜瘢痕切除 → 术后康复",
    f"{b('测量')}：量角器测活动度，记为“过伸-伸直欠缺-屈曲”，并{b('和健侧比较')}；IKDC 主观膝关节评分（另一项研究中前瞻收集）",
    f"{b('“正常”的标准（IKDC）')}：与健侧相比，伸直差 ≤2°、屈曲差 ≤5° 为正常；伸直差 3～5°、屈曲差 6～15° 为接近正常；6～10° / 16～25° 为异常；>10° / >25° 为严重异常",
]))

A.append(h2("重点：围手术期康复怎么做"))
A.append(img(2))
A.append(cap("围手术期康复流程（编者根据原文整理）"))
A.append(p(f"核心思路是{mk('先把伸直练到和健侧一样，再练屈曲')}——伸直和屈曲很难同时改善，而丢伸直比丢屈曲更难忍受。整个进阶{b('按标准而不是按时间')}。"))
A.append(h3("每天 3～4 次的伸直训练"))
A.append(pic(3, "原文图 1：伸膝装置（图中中文为编者所加）"))
A.append(pic(4, "原文图 2：毛巾牵拉"))
A.append(pic(5, "原文图 3：垫高足跟"))
A.append(pic(6, "原文图 4：俯卧悬腿"))
A.append(pic(7, "原文图 5：站立锁膝"))
A.append(h3("什么时候能开始练屈膝"))
A.append(pic(8, "原文图 6：主动抬足跟"))
A.append(ul([
    f"伸直与健侧对称，{b('并且')}能主动收缩股四头肌把足跟抬离床面",
    "屈膝练习：足跟滑动、靠墙滑动；目标是能坐在脚跟上，或屈曲不再进步",
    f"{red('伸直一旦丢失，立即停止屈膝练习')}，先把伸直找回来",
    "髌腱挛缩（低位髌骨）的患者，屈曲通常很难恢复到和健侧一样（本组 3 人）",
]))
A.append(h3("几个细节"))
A.append(ul([
    f"{b('什么时候手术')}：术前伸直练到不再进步，说明剩下的受限来自瘢痕而不是软组织紧张",
    f"{b('术后卧床 5 天')}：除如厕外卧床，配合持续被动活动仪（0°～30°）和冷敷加压，预防关节积血——积血会抑制股四头肌和腘绳肌",
    f"{b('“正常”要和健侧比')}：大多数人膝有过伸（男性平均约 5°、女性约 6°，95% 以上的人有一定过伸）。健侧过伸 5°、患侧伸直差 2°，应记为相差 {b('7°')}，而不是 2°",
]))

A.append(h2("结果"))
A.append(table(["", "患侧", "健侧"], [
    ["术前（过伸-伸直欠缺-屈曲）", "0°-8°-117°", "5°-0°-147°"],
    ["术后平均 8.6 个月", "3°-0°-134°", "5°-0°-147°"],
]))
A.append(tcap("原文结果：平均活动度（中文整理）"))
A.append(ul([
    f"{b('伸直')}：平均改善 {b('11°')}（2°～28°）；33 人中 {b('27 人')}伸直恢复到“正常”",
    f"{b('屈曲')}：平均改善 {b('17°')}（－5°～60°）；只有 {b('14 人')}屈曲“正常”，出院时两侧屈曲平均差 13°（接近正常）——{mk('多数人最后卡在屈曲')}",
    f"{b('总体活动度')}：治疗前没有一人“正常”、21 人“严重异常”；治疗后 14 人正常、12 人接近正常、3 人异常、4 人严重异常（其中 2 人有低位髌骨）",
    f"{b('主观评分')}：IKDC 从 {b('45.3')} 升到 {b('67.1')}（术后平均 14.7 个月，P<0.01），33 人中 29 人提高；活动度“正常”者平均 72.6 分，显著高于其他人（P＝0.04）",
]))
A.append(pic(9, "活动度分级和主观评分（编者根据原文表 2、表 3 重画）"))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('没有对照')}：回顾性病例系列，无法区分效果来自伸膝装置、康复方案还是手术本身；也没有和石膏、支具等方法比较",
    f"{b('利益冲突')}：作者之一 Shelbourne 是伸膝装置生产公司的顾问，而研究评价的正是这款装置",
    f"{b('“活动度越大评分越好”只做了一次比较')}：只比较了“正常”组和其他所有人（P＝0.04），没有对四个等级做趋势检验；而且活动度在 8.6 个月测、评分在 14.7 个月测，时间点不同",
    f"{b('67 分仍不算好')}：作者自己也说不理想，提示预防关节纤维化比事后治疗更重要",
    f"{b('卧床 5 天')}：现在看来比较保守，血栓风险和依从性需要权衡",
    f"{b('没算成本')}：作者说伸膝装置能省钱省时，但研究没有评估费用",
    "优点：强调和健侧对比、按标准进阶、先伸直后屈曲，这些原则在今天仍然适用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“假设”和研究设计')}：摘要以“假设”形式提出结论，但这是回顾性病例分析，不是预先设计的检验",
    f"{b('低位髌骨人数')}：方法写 33 人中 3 人有低位髌骨，讨论写术后 4 名“严重异常”中 2 人有低位髌骨，第 3 人的结果没有交代",
    f"{b('结果时间点')}：活动度报告在术后平均 8.6 个月，主观评分在 14.7 个月，摘要把两者放在一起，容易误读为同一时间",
    f"{b('参考文献 11')}：Hassan 等的研究标为《Am J Sports Med》2000;13(4)，卷号与该刊不符",
    f"{b('小错')}：“0° to 30° degrees”；静脉用药“ketoralac”应为 ketorolac（酮咯酸）",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先伸直、后屈曲')}：伸直和健侧对称、能主动抬足跟之后再练屈膝；伸直一丢就退回去",
    f"{b('高频、低负荷、长时间')}：垫高足跟、俯卧悬腿、毛巾牵拉每天 3～4 次、每次 10 分钟——没有伸膝装置也能做",
    f"{b('一定和健侧比')}：大多数人有 5° 左右过伸，“到 0°”并不等于正常",
    f"{b('练到平台期再考虑手术')}：术前把软组织的部分尽量练回来，剩下的才是瘢痕",
    f"{b('预防胜于治疗')}：前交叉韧带重建后早期就要把伸直拿到和健侧一样",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Biggs-Kinzer A, Murphy B, Shelbourne KD, Urch S. Perioperative Rehabilitation Using a Knee Extension Device and Arthroscopic Debridement in the Treatment of Arthrofibrosis. Sports Health. 2010;2(5):417-423. doi:10.1177/1941738110379088</em><br>"
    "© 2010 The Author(s)，由 SAGE 出版，原文未标注开放获取许可。本文为学术交流用的中文解读：原文图 1～6 引自原文，图中中文标注为编者所加；流程卡和结果图为编者根据原文整理，表格为中文翻译。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「膝」前交叉韧带术后膝伸不直？先伸直、后屈曲：伸膝装置＋关节镜松解治疗关节纤维化（附动作图解）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>膝关节纤维化康复推文</title>
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
