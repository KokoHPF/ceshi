#!/usr/bin/env python3
"""髋关节腔注射要不要影像引导（Singh 等 2014）推文。

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
    "Singh J, Khan WS, Marwah S, Wells G, Tannous DK, Sharma HK. Do We Need Radiological Guidance for Intra-Articular Hip Injections? The Open Orthopaedics Journal. 2014;8:114-117. doi:10.2174/1874325001408010114",
    "作者单位：英国皇家伦敦医院创伤骨科、皇家国立骨科医院、赫尔皇家医院创伤骨科",
    f"文章类型：{b('前瞻性病例系列')}（87 例患者，100 个髋），没有对照组",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"髋关节腔注射既用来{b('诊断')}（打完麻药疼痛明显减轻，说明痛源在关节内），也用来{b('治疗')}（激素等）。"
    f"髋关节位置深、周围有股动脉、股神经，很多骨科和放射科医生习惯在{b('透视或超声引导')}下做；风湿科和疼痛科医生则常常凭体表标志“盲打”。"
))
A.append(p(
    f"不用影像的好处很明显：{b('便宜、没有辐射、不用造影剂、不用住院')}。但到底能打得多准？以往研究结论不一，而且很少考虑{mk('操作者经验和患者胖瘦')}这两个因素。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：计划做诊断或治疗性髋关节注射的症状性髋骨关节炎患者，87 例共 {b('100 个髋')}；平均 69 岁（43～96 岁），平均 BMI {b('30.2')}（19.2～43.2）",
    f"{b('先“盲打”')}：仰卧在可透视的手术床上，静脉镇静下按体表标志用{b('前方入路')}进针（见下文）",
    f"{b('再透视验证')}：用影像增强器看针的位置，注入造影剂。造影剂进入关节＝成功；针位不对或造影剂不进关节＝失败",
    f"{b('药物')}：左布比卡因 10 mL＋甲泼尼龙 80 mg",
    f"{b('操作者')}：骨科主治医生和骨科住院医生；记录医生级别和患者 BMI，分析它们和成功率的关系",
]))

A.append(h2("重点：前方入路怎么找、怎么打"))
A.append(img(2))
A.append(cap("编者示意图：前方入路的体表标志（根据原文描述绘制）"))
A.append(ul([
    f"{b('摸股动脉')}：找到股动脉搏动和腹股沟韧带的{b('交点')}",
    f"{b('进针点')}：交点{mk('外侧 2.5～3.5 cm')}（原文图示为 3 cm）",
    f"{b('方向')}：22G 腰穿针，{b('向后内侧倾斜约 20°')}",
    f"{b('深度')}：一直进到{b('触及骨面')}",
]))
A.append(pic(3, "原文图 1：体表标志（图中中文标注为编者所加）"))
A.append(pic(4, "原文图 2：进针（图中中文标注为编者所加）"))
A.append(pic(5, "原文图 3：透视下造影剂进入关节（图中中文标注为编者所加）"))
A.append(img(6))
A.append(cap("操作要点（编者根据原文整理）"))

A.append(h2("结果"))
A.append(table(["", "全部（100 髋）", "BMI < 30（56 髋）"], [
    ["总体成功率", f"{b('67%')}", f"{b('82.1%')}"],
    ["主治医生", "77.1%（约 37/48）", f"{b('87.9%')}（约 29/33）"],
    ["住院医生", "57.7%（约 30/52）", "73.9%（约 17/23）"],
    ["主治 vs 住院", "P＝0.039", "P＝0.179"],
]))
A.append(tcap("原文表 1：不用影像的髋关节注射成功率（中文翻译；括号内例数为编者按百分比推算）"))
A.append(ul([
    f"不用影像，{b('三分之二')}的注射打进了关节",
    f"{b('经验很关键')}：主治医生 77.1%，住院医生 57.7%",
    f"{b('胖瘦很关键')}：成功组平均 BMI {b('28.5')}，失败组 {b('32.0')}（P＝0.001）；BMI < 30 的患者成功率升到 82.1%",
    f"{mk('主治医生＋BMI < 30')}：成功率 {b('87.9%')}（摘要写约 88%）",
    "没有出现压痛、血肿、过敏或感染，也没有血管神经损伤",
]))
A.append(pic(7, "两组结果对比（编者根据原文重画）"))
A.append(p(
    f"作者还算了一笔账：门诊注射约 {b('35 英镑')}，他们医院按日间手术做约 {b('1234 英镑')}。"
    "他们认为：选对患者（BMI 合适）、由有经验的医生操作，部分髋关节注射可以放到门诊做，省钱也省床位。"
))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('即使条件最好，也有约 1/8 打不进去')}：主治医生给不胖的患者打，仍有约 12% 失败；整体 1/3 失败。用于{red('诊断性注射')}时，打偏会造成假阴性或假阳性，作者自己也承认这一点",
    f"{b('主治和住院医生的差异并不稳')}：按编者推算的例数，未校正的卡方检验 P≈0.039，用连续性校正或 Fisher 精确检验则 P≈0.06，{b('不再显著')}；原文也没说明用的什么检验",
    f"{b('“盲打”并不完全是门诊条件')}：患者在可透视的手术床上、静脉镇静下操作，和门诊清醒状态下打不是一回事",
    f"{b('没有对照')}：没有和超声或透视引导直接比较，也没有疗效随访",
    f"{b('按“髋”统计')}：13 例患者两侧都打，同一个人的两侧髋不完全独立",
    "优点：每一针都用造影确认，判定客观；样本在同类研究中较大，并首次把医生级别和 BMI 一起分析",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b("“49 例（56%）”对不上")}：结果写 BMI < 30 的有 49 例患者（56%），但 49/87＝56% 是按患者算；而 82.1%、87.9%、73.9% 只能由 {b('56 个髋')}（46/56、29/33、17/23）得出，用 49 怎么也算不出 82.1%。表 1 表头写“全部患者 N＝87（100%）”，成功率却是按 100 髋算的",
    f"{b('“consultant / registrar / trainee”混用')}：摘要写 registrars（专科住院医生），正文写 trainees（受训医生）",
    f"{b('统计方法没交代')}：方法只写“描述性统计”，结果却给了 P 值；BMI 比较没说用什么检验",
    f"{b('进针距离')}：方法写 2.5～3.5 cm，图 2 图注写 3 cm",
    f"{b('引用人名写错')}：讨论里的“Karup & Ward”在参考文献中写成“Harish K, Peter W”（应为 Kurup H, Ward P）；“Demirhan 等 [4]”对应的参考文献 4 实际第一作者是 Dıraçoğlu；“Mauffrey & Pobbaley”与参考文献中的“Pobbathy”拼写不一致",
    f"{b('小错')}：“intra-articuar”“cntrast”“upto”等拼写错误；参考文献 5 混进了网页链接",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{b('不用影像也能打进去，但成功率取决于人和患者')}：经验丰富的医生、BMI < 30 的患者，成功率接近 90%；住院医生或肥胖患者，失败率可达 1/4～1/2",
    f"{b('诊断性注射要更谨慎')}：如果要靠注射后疼痛是否缓解来判断痛源在不在关节内，打偏会误导判断——这类注射更值得用影像引导",
    f"{b('前方入路的关键')}：先摸准股动脉，在它和腹股沟韧带交点外侧 2.5～3.5 cm 进针，向后内侧约 20°，触骨即止",
    "关节腔注射须由有资质的医生操作；对康复治疗师来说，了解注射是否“打准”很重要——注射后疼痛没缓解，不一定说明不是关节内问题，也可能是没打进去",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Singh J, Khan WS, Marwah S, Wells G, Tannous DK, Sharma HK. Do We Need Radiological Guidance for Intra-Articular Hip Injections? Open Orthop J. 2014;8:114-117. doi:10.2174/1874325001408010114</em><br>"
    "原文以 CC BY-NC 3.0 协议开放获取，版权归原作者所有。本文为非商业的学术交流中文解读：原文图 1～3 引自原文，图中中文标注为编者所加；示意图、要点卡和结果图为编者根据原文整理，表格为中文翻译。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「髋」髋关节腔注射一定要影像引导吗？不用影像成功率 67%，有经验的医生给不胖的患者打可达 88%"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>髋关节腔注射引导推文</title>
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
