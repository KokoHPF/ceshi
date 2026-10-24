#!/usr/bin/env python3
"""仰卧桥式运动综述 Part I（Colonna 等 2025）推文。

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
    "Colonna S, D'Alessandro A, Tarozzi R, Casacci F. Supine Bridge Exercise: A Narrative Review of the Literature (Part I). Cureus. 2025;17(3):e80349. doi:10.7759/cureus.80349",
    "作者单位：意大利博洛尼亚脊柱中心、骨科整骨脊柱教育中心（OSCE）",
    f"文章类型：{b('叙述性综述')}，三部曲的第一篇：本篇讲“桥怎么做、练到哪块肌肉”，第二篇讲腰痛，第三篇讲髋关节",
], square=True))

A.append(h2("先说为什么要关注这个"))
A.append(p(
    f"仰卧桥式（以下简称“桥”）是康复里研究最多、用得最多的动作之一，用于预防腘绳肌损伤、髂腰肌腱病，以及治疗慢性非特异性腰痛。"
    f"它是{b('多关节、两端闭链、自重')}的动作，可以在不稳定面上做，也可以加负荷。"
))
A.append(p(
    f"同样叫“桥”，{mk('脚放多远、踝怎么摆、腰挺多高、膝间夹球还是套带、背靠凳还是脚踩球')}，练到的肌肉差别很大。"
    "作者把文献里的做法和各肌肉的肌电数据整理成了一本“桥式使用手册”。"
))

A.append(h2("经典做法和生物力学"))
A.append(pic(2, "原文图 1：经典仰卧桥"))
A.append(pic(3, "原文图 2：桥式的生物力学示意"))
A.append(ul([
    f"桥的身体只有{b('一个自由度')}：脚的位置一旦确定，抬多高就决定了踝、膝、髋各是多少度",
    f"{b('脚到上背部支点的距离')}（约在 T3 水平）是最主要的变量",
    f"{b('膝')}：骨盆刚离地时总需要屈膝力矩（腘绳肌）；抬高后，如果脚离得近（距离 <1 m）会转为伸膝力矩（股四头肌），脚离得远（≥1 m）则一直需要屈膝力矩",
    f"{b('髋')}：几乎始终需要伸髋力矩；脚越远、躯干越平，伸髋力矩越大",
]))

A.append(h2("重点：改一个角度，换一批肌肉"))
A.append(h3("① 踝：前脚掌离地，多练臀、少练腘绳"))
A.append(pic(4, "原文图 3：踝背屈的桥"))
A.append(ul([
    f"足跟着地（踝背屈）时，腘绳肌活动下降、臀大肌上升；全脚踩地时腘绳肌更多（Yoo、Escamilla 等）",
    f"例：屈膝 90° 时，股二头肌从全脚踩地的 {b('69.2%')} 降到足跟着地的 {b('58.7%')} MVIC（Lehecka）",
    "Escamilla：想多练腘绳肌用全脚踩地；想多练股四头肌、内收肌和腹斜肌用足跟着地",
]))
A.append(h3("② 膝：脚越靠近臀部，臀越多、腘绳越少"))
A.append(pic(5, "原文图 4：不同屈膝角度"))
A.append(pic(6, "原文图 5：屈膝角度与臀大肌/股二头肌比值"))
A.append(ul([
    f"屈膝越大，臀大肌和大收肌越活跃，股二头肌越少",
    f"单腿桥屈膝到 {b('135°')}（“臀桥”）时，股二头肌从 75.3% 降到 {b('23.5%')} MVIC，臀大肌和臀中肌占优（Lehecka）",
    f"{mk('做桥腘绳肌抽筋？')}——把脚放得更靠近臀部，减少腘绳肌负担",
]))
A.append(h3("③ 腰：中立还是过伸，骨盆前倾还是后倾"))
A.append(pic(7, "原文图 6：脊柱中立与腰椎过伸"))
A.append(pic(8, "原文图 7：传统桥与腹部回缩"))
A.append(ul([
    "多数作者建议腰椎保持中立，避免竖脊肌过度代偿造成骨盆前倾、腰椎过伸，反复这样做可能增加腰骶部压力",
    f"控制方法：同时做{b('腹部回缩')}；保持肩—髋—大腿一条直线；膝上套弹力带做等长外展",
    f"做桥时有意{b('骨盆后倾')}：臀大肌活动显著更高、多裂肌更低，臀大肌/多裂肌、臀大肌/腘绳肌比值都更高",
]))

A.append(h2("重点：几种常见变式"))
A.append(h3("单腿桥"))
A.append(pic(9, "原文图 8：单腿桥的三种悬空腿姿势"))
A.append(pic(10, "原文图 9：波速球上的单腿桥"))
A.append(ul([
    f"比双腿桥更多动用臀大肌、臀中肌和腘绳肌，多裂肌没有差别；不负重就能有效练臀",
    "单腿支撑会产生躯干旋转力矩，需要更多腹斜肌（对侧腹内斜肌更活跃）",
    "加波速球等不稳定面：腹横肌（超声）和臀大肌并没有显著增加，主要是腘绳肌更多",
    f"{b('常见问题')}：腘绳肌抽筋——可能是臀肌弱、腘绳肌代偿；把脚放近一点",
]))
A.append(h3("夹球（内收）或套带（外展）"))
A.append(pic(11, "原文图 10：膝间夹球"))
A.append(pic(12, "原文图 11：膝上套弹力带"))
A.append(ul([
    f"{b('夹球内收')}：增加腹横肌激活（Lee）；同时动下肢还会增加腹内斜肌和多裂肌",
    f"{b('套带外展')}：外展 30° 能更有选择地练臀大肌、减少竖脊肌代偿和骨盆前倾；套带等长外展可让骨盆前倾减少约 20%",
]))
A.append(h3("上背垫高：臀推"))
A.append(pic(13, "原文图 12：背靠长凳"))
A.append(pic(14, "原文图 13：背靠瑞士球"))
A.append(pic(15, "原文图 14：杠铃臀推"))
A.append(ul([
    f"臀大肌在{b('接近完全伸髋')}时激活最高，臀推的活动范围恰好集中在这一段",
    "与杠铃深蹲比，杠铃臀推的臀大肌上、下部和股二头肌活动都更高；6 周训练对 10 m、20 m 冲刺可能更有利，前蹲对纵跳更有利",
    f"{red('注意')}：臀肌弱的人伸髋范围大时，股骨头会受到更多向前的力，需要循序渐进、确保是臀肌在控制",
]))
A.append(h3("脚垫高：凳、瑞士球、悬吊"))
A.append(pic(16, "原文图 15：脚踩长凳"))
A.append(pic(17, "原文图 16：脚踩瑞士球"))
A.append(pic(18, "原文图 17：悬吊伸膝"))
A.append(pic(19, "原文图 18：悬吊屈膝"))
A.append(ul([
    f"{b('悬吊桥')}比普通桥更多动用腹内斜肌、腹直肌、多裂肌和竖脊肌，多裂肌在悬吊时最高；悬吊越高，腹横肌和竖脊肌越多",
    "瑞士球上伸膝桥只需约 30% 的多裂肌和竖脊肌，70 秒内多裂肌疲劳不明显，适合练耐力",
    f"{red('但')}：慢性腰痛患者在瑞士球上做桥，表层肌肉活动更多、深层腹肌（腹横肌）反而更少，作者建议谨慎使用",
]))

A.append(h2("各肌肉的“排行榜”"))
A.append(p(f"原文把文献里的肌电数据按肌肉做成了 7 张排名图（共一百多项，英文小字）。编者按原图识别了数值，{b('每块肌肉取前 10 名')}，翻成中文重画。绿色为稳定支撑面，橙色为一端在球、波速球、悬吊或振动台上。"))
for i, m in enumerate(['臀大肌', '臀中肌', '腘绳肌', '竖脊肌', '腰多裂肌', '腹外斜肌', '腹横肌'], start=20):
    A.append(img(i)); A.append(cap(f"{m}（编者根据原文图 {i - 1} 重画）"))
A.append(ul([
    f"{b('臀大肌')}：杠铃臀推、美式臀推、杠铃臀桥（屈膝 135°）最高，约 66%～78%；普通双腿桥只有约 20%～27%",
    f"{b('臀中肌')}：杠铃臀桥 75%，单腿桥约 40%～47%",
    f"{b('腘绳肌')}：屈膝越小（脚越远）越高，屈膝 30° 的单腿桥超过 100%",
    f"{b('竖脊肌')}：同样是屈膝 30° 时最高（约 74%）",
    f"{b('多裂肌')}：双脚悬吊的桥最高（约 54%），普通桥约 39%～45%",
    f"{b('腹肌')}：都不高——腹外斜肌最高约 23%，腹横肌最高约 32%（单腿桥）",
]))

A.append(h2("这些内容能信几分"))
A.append(ul([
    f"{b('叙述性综述')}：没有系统检索和质量评价，作者自己在 PubMed 只检索到 74 篇，选哪些研究、怎么归纳带有主观性",
    f"{b('不同研究不能直接比')}：排名图把不同研究、不同 MVIC 测法、不同人群的 %MVIC 放在一起排，数值高低只能作参考",
    f"{b('多是健康人')}：大部分肌电数据来自无症状年轻人，用到患者身上要谨慎",
    f"{b('肌电≠力量≠疗效')}：激活高不代表训练效果更好，也没有临床结局数据",
    "作者致谢中说明使用了 ChatGPT 协助撰写",
    "优点：把散落的研究按“改哪个变量、练哪块肌肉”整理得很清楚，配了大量示范照片，实用性强",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('结论张冠李戴')}：“做桥时加髋内收比传统桥或加外展更能激活腹横肌”是 Lee 等的结论，原文却写成“作者 [15]（Escamilla）总结”",
    f"{b('外展前后矛盾')}：同一段先说加弹力带外展显著提高臀大肌上部活动，接着又说“与预期相反，不加外展的臀桥肌肉活动更高”",
    f"{b('排名图的引用和标签有误')}：同一个“非对称双腿臀桥（Kim）”在臀大肌图标为文献 [70]（实为 Hirose 和 Tsuruike），在腘绳肌图标为 [73]；“髋外展 0°”一项在同一图里分别引 [23] 和 [77]；竖脊肌图和腹外斜肌图里“髋内旋 25°”各出现两次、数值不同，多裂肌图里“低幅振动台”也出现两次，分不清对应哪种条件",
    f"{b('图的分图字母')}：图 16 实际标为 C、D，图 17 标为 E、F，与图注的 A、B 不符",
    f"{b('超过 100%')}：腘绳肌图中屈膝 30° 单腿桥达 107.8% MVIC，原文没有说明",
    f"{b('小错')}：臀中肌一节写“与无力的 GM（臀大肌）相关的损伤”，应为臀中肌；“upper thrunk”“Asimmetric”“harmstrings”等拼写错误",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('想多练臀、少练腘绳肌')}：脚放近（屈膝 ≥90°～135°）、足跟着地（前脚掌抬起）、骨盆后倾、膝上套带外展；需要加量时用臀推",
    f"{b('想多练腘绳肌')}：脚放远（屈膝小）、全脚踩地、单腿、脚踩瑞士球或悬吊",
    f"{b('想练腰背深层肌')}：悬吊桥、单腿桥；腹横肌可加膝间夹球",
    f"{b('腰容易过伸的人')}：同时做腹部回缩、保持肩—髋—大腿一直线，或改用背靠凳的臀推",
    f"{b('不稳定面不是越多越好')}：主要增加腘绳肌，对臀肌和深层腹肌帮助有限，腰痛患者慎用",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Colonna S, D'Alessandro A, Tarozzi R, Casacci F. Supine Bridge Exercise: A Narrative Review of the Literature (Part I). Cureus. 2025;17(3):e80349. doi:10.7759/cureus.80349</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流用的中文解读：原文图 1～18 引自原文，图中中文标签为编者所加；原文图 5、图 19～25 由编者根据原图数值用中文重画，表述为中文翻译。如有侵权请联系删除。"
))

TITLE = "「桥式」同样是臀桥，脚放远一点、踝翘起来、腰挺高一点，练到的肌肉完全不同（三部曲之一）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>仰卧桥式综述 Part I 推文</title>
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
