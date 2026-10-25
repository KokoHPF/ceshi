#!/usr/bin/env python3
"""不稳肩的体格检查与评估（Valencia Mora 等 2017）推文。

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
    "Valencia Mora M, Ruiz Ibán MÁ, Diaz Heredia J, Gutiérrez-Gómez JC, Ruiz Diaz R, Aramberri M, Cobiella C. Physical Exam and Evaluation of the Unstable Shoulder. The Open Orthopaedics Journal. 2017;11(Suppl-6, M12):946-956. doi:10.2174/1874325001711010946",
    "作者单位：西班牙马德里 Jiménez Díaz 基金会大学医院、Ramón y Cajal 大学医院，英国伦敦大学学院",
    f"文章类型：{b('叙述性综述')}（介绍查肩关节不稳的各项检查及其准确性）",
], square=True))

A.append(h2("先说为什么难"))
A.append(ul([
    f"肩关节是全身{b('最容易脱位')}的关节，过顶运动尤其多见；{b('95% 以上')}是外伤性前脱位，一般不难认",
    f"难的是{mk('非外伤性、后方、多方向不稳')}：主要症状往往是“痛”而不是“掉出来”",
    "能查出一种不稳的诱发试验，对另一种不稳可能会误导",
    f"{b('年轻运动员肩痛')}，要想到隐匿性不稳",
]))

A.append(h2("第一步：问清病史，双侧对比"))
A.append(ul([
    f"{b('首次脱位')}：几岁、什么机制、在医院复位还是自己复位、有无神经损伤",
    f"{b('反复不稳')}：脱位次数、在什么活动中发生、需要怎样复位",
    f"{b('查体一定两侧对比')}：视诊、触诊、主被动活动度、肌力和感觉，再根据怀疑选特殊检查",
]))

A.append(h2("重点一：先分清松弛和不稳"))
A.append(img(2))
A.append(cap("松弛与不稳、移位分级（编者根据原文整理）"))
A.append(ul([
    f"{b('Beighton 评分')}：9 分制，小指、拇指、肘、膝过伸和弯腰手掌贴地；年轻成人以 {b('4～6 分')}以上为全身松弛",
    f"评估肩松弛的“金标准”是{b('麻醉下检查')}（消除肌肉的主动稳定作用）；正常松弛度没有统一标准",
    "检查时每次用相同体位、相同力度，减少检查者之间的差异；有过脱位的人可能很难检查",
]))

A.append(h3("负荷—移位试验"))
A.append(p(f"坐位或仰卧，一手按肩顶稳住肩胛，一手握上臂近端；{b('先把肱骨头压回关节盂（负荷）')}，再向前或向后推（移位）。前方不稳敏感度 50%、后方 14%，特异度都是 {b('100%')}。"))
A.append(h3("抽屉试验"))
A.append(pic(3, "原文图 1：前抽屉试验"))
A.append(ul([
    f"{b('后抽屉')}：仰卧，一手握腕或前臂，另一手拇指在肱骨头前方向后推，同时把手臂前屈；在上举 45°～60° 的“零位”做更可靠",
    f"{b('前抽屉')}：外展 80°～120°、前屈 0°～20°、外旋 0°～30°；一手稳住肩胛（拇指在喙突），另一手向前推肱骨头",
    f"{mk('年轻运动员Ⅱ度移位可能是正常的')}，两侧不对称不能单独作为诊断依据",
]))
A.append(h3("沟槽征"))
A.append(pic(4, "原文图 2：沟槽征，中立和外旋各做一次"))
A.append(ul([
    "坐位最可靠，上臂垂在体侧，握肘向下拉，肩峰下方出现凹陷为阳性；主要反映上盂肱韧带（肩袖间隙）",
    f"分级：Ⅰ度 <1.5 cm、Ⅱ度 1.5～2 cm、Ⅲ度 >2 cm；{b('>2 cm 特异度 97%、敏感度只有 28%')}",
    f"外旋时移位{red('反而更大')}，要考虑肩袖间隙损伤",
    "无症状的人下方松弛范围也很大，没有一个绝对数值能定义下方不稳",
]))
A.append(h3("Gagey 过度外展试验"))
A.append(pic(5, "原文图 3：过度外展试验"))
A.append(ul([
    f"被动外展 {b('>105°')} 为阳性，提示下盂肱韧带复合体松弛；约 15% 的人会因恐惧而外展受限",
    f"现在多用{b('“对比过度外展试验”')}：同时满足三点才算阳性——诱发深部疼痛、两侧相差 {b('>20°')}、没有软的终末感",
]))

A.append(h2("重点二：前方不稳的诱发试验"))
A.append(pic(6, "原文图 4：恐惧试验和复位试验"))
A.append(ul([
    f"{b('恐惧试验')}：仰卧，靠床边让肩胛有支撑，外展 90°、屈肘 90°，检查者用膝顶住肘部，逐渐外旋，直到疼痛或恐惧。以{b('恐惧')}为标准比以疼痛为标准一致性更好；{b('特异度 98.9%')}，敏感度 52.8%",
    "站立位也可以做：同时握住双侧前臂做，比单侧加压更可靠",
    f"{b('复位试验')}：在恐惧位向后推肱骨头，看是{b('恐惧消失')}（真正的不稳）还是只是{b('疼痛减轻')}（可能是内撞击等隐匿性不稳）。以疼痛为标准时敏感度 45.83%、特异度 54.35%；以恐惧消失为标准，特异度可升到 100%",
    "复位试验也会让肩袖病变（82%）、后方不稳（63%）、肩锁关节病变（80%）患者疼痛，一定要记下{0}".format(b("痛在哪里")),
    f"{b('放松试验 / 惊吓试验')}：在复位位稍加外旋后突然松手（惊吓试验不加外旋），疼痛或恐惧加重为阳性；{red('可能很痛甚至导致脱位，动作要轻')}",
    f"{mk('恐惧、复位、放松三者联合，特异度很高')}",
]))

A.append(h2("重点三：后方不稳"))
A.append(ul([
    f"只占所有不稳的 {b('2%～10%')}，没有明确外伤时容易漏诊；运动、{b('癫痫发作、触电')}史要警惕",
    "常和撞击、盂唇撕裂并存；后关节线常有压痛；体位性后脱位者双侧三角肌后内侧可见小皮肤凹陷",
    "后方恐惧试验：屈曲、内收、内旋位向后推；但并非所有患者都在同一位置出现症状",
]))
A.append(pic(7, "原文图 5：Jerk 试验"))
A.append(pic(8, "原文图 6：Kim 试验"))
A.append(p(f"{b('Jerk 试验和 Kim 试验联合')}，对后下盂唇撕裂的敏感度达 {b('97%')}。"))

A.append(h2("准确性一览"))
A.append(pic(9, "各试验的敏感度和特异度（编者作图）"))
A.append(img(10))
A.append(cap("查不稳的顺序（编者根据原文整理）"))

A.append(h2("这篇综述能信几分"))
A.append(ul([
    f"{b('叙述性综述')}：没有说明检索方法和纳入标准，准确性数字来自不同研究，人群和金标准各不相同",
    "后方、多方向不稳的检查数据很少，作者也承认诊断仍然困难",
    "优点：动作要点、变式和注意事项写得具体，照片清楚，适合作查体参考",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('日期矛盾')}：收稿 2017 年 5 月 4 日，修回却是 2016 年 10 月 9 日、接收 2016 年 10 月 28 日",
    f"{b('分级前后不一')}：第一种方法把“1～2 cm（或到盂缘）”定为Ⅱ级，第三种方法又把“到盂缘”定为Ⅰ级；沟槽征分级用 1.5 cm 为界，与 Neer 原始分级（<1 cm、1～2 cm、>2 cm）不同",
    f"{b('图文不符')}：正文说抽屉试验要仰卧，图 1 是坐位；正文说 Jerk 试验是“屈曲、内收、内旋”，图 5 图注写的是“外展 90° 后水平内收”，并写成“患者握住肘部”",
    f"{b('Kim 试验')}：正文写“被动前屈 45°”，图注写“被动上举”，两处描述不一致",
    f"{b('沟槽征')}：说“两个体位的下方移位应相同”，但正常情况下外旋时移位应减小",
    f"{b('笔误')}：“hiperlaxity”“provoke and anterior translation”“Von Raebox”（应为 Von Raebrox）",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先分清松弛和不稳')}：查到松，不等于有病；要有症状、和病史对得上",
    f"{b('怀疑前方不稳')}：恐惧 → 复位 → 放松依次做，以“恐惧”而不是“疼痛”为判断标准",
    f"{b('怀疑后方不稳')}：Jerk＋Kim 联合，敏感度高；注意癫痫、触电史",
    f"{b('沟槽征')}中立、外旋各做一次，外旋时更松提示肩袖间隙问题",
    "所有检查两侧对比；对刚脱位或很恐惧的患者，诱发试验要轻，必要时延后",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Valencia Mora M, Ruiz Ibán MÁ, Diaz Heredia J, Gutiérrez-Gómez JC, Ruiz Diaz R, Aramberri M, Cobiella C. Physical Exam and Evaluation of the Unstable Shoulder. Open Orthop J. 2017;11(Suppl-6, M12):946-956. doi:10.2174/1874325001711010946</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流中文解读：原文图 1～6 引自原文，图中中文标签为编者所加；准确性图由编者根据原文数字绘制，要点卡为编者整理。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「肩关节不稳」松不等于不稳：从负荷—移位到恐惧、Jerk、Kim 试验，不稳肩怎么查（附动作图）"
PTITLE = "不稳肩查体推文"
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
