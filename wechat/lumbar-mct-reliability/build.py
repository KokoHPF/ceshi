#!/usr/bin/env python3
"""腰椎运动控制测试的信度（Luomajoki 等 2007）推文。

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
    "Luomajoki H, Kool J, de Bruin ED, Airaksinen O. Reliability of movement control tests in the lumbar spine. BMC Musculoskeletal Disorders. 2007;8:90. doi:10.1186/1471-2474-8-90",
    "作者单位：瑞士 Reinach 物理治疗诊所、芬兰库奥皮奥大学、苏黎世应用科学大学物理治疗研究所、苏黎世大学医院、苏黎世联邦理工学院",
    f"文章类型：{b('信度研究')}（40 人的录像，4 名物理治疗师评分）",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"最多 {b('90%')} 的腰痛属于“非特异性腰痛”，找不到明确的结构性原因。临床上常把其中一类人归为{b('运动控制障碍')}："
    f"他们控制不好腰部的主动运动，在不知不觉中反复用“会诱发疼痛”的方式活动——O'Sullivan 称之为“疼痛诱发者”。"
))
A.append(p(
    f"Sahrmann 的“相对柔韧性”理论也是类似思路：运动会走“阻力最小”的路径，比如髋屈曲比腰椎更僵，弯腰时就更多由腰来完成，久而久之出现屈曲相关的腰痛。"
))
A.append(p(
    f"判断有没有运动控制障碍，主要靠{b('看患者做主动动作')}。这些测试临床上很常用，但{mk('不同治疗师看同一个动作，结论一致吗？')}"
    "之前只有少数研究，而且大多是把病史、症状和动作放在一起判断，没有单独看每个测试。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：瑞士一家物理治疗诊所的 40 名患者：{b('27 名')}非特异性腰痛、{b('13 名')}因其他肌骨问题就诊、没有腰痛（让“做得好”的人也占一定比例）；平均 52 岁；排除急性腰痛和严重病理",
    f"{b('录像')}：同一人按标准指令拍摄 {b('10 项')}主动运动测试，每人约 10 分钟；穿内衣，能看清整个脊柱、髋和下肢，不露脸；指令听不懂可再讲解、示范一次，仍做错则按做错记",
    f"{b('评分者')}：4 名物理治疗师，两两一组——资深组 2 人（工作 25 年、手法治疗研究生学历、熟悉运动控制评估），年轻组 2 人（工作 5 年，上过 3 天运动控制课程）；评分前由研究者讲解典型表现和评分标准",
    f"{b('评分')}：只看录像、每段只看一遍，不知道诊断和病史，互不知情；每项判为{b('“正确 / 不正确”')}；只有{b('明显的')}运动控制障碍才判不正确，经指导能纠正的不算",
    f"{b('测试者内信度')}：每组中 1 人隔 2 周再评一次同样的录像",
    f"{b('统计')}：Kappa 值、一致百分比和 95% 置信区间；作者设定的“合格线”是测试者间、测试者内及两者平均的 Kappa 都 {b('>0.4')}，且置信区间下限 >0.2",
]))
A.append(small("Kappa 解读（原文标准）：>0.80 很好，0.60～0.80 较好，0.40～0.60 中等（原文写“good”），0.20～0.40 一般，<0.20 差。Kappa 扣除了“碰巧一致”的部分，比单纯的一致百分比更严格。"))

A.append(h2("重点：10 项运动控制测试怎么做"))
A.append(p(f"测试来自 Sahrmann 和 O'Sullivan 的描述，分三类：{b('屈曲控制 3 项、伸展控制 3 项、旋转控制 4 项')}（单腿站左右各算 1 项）。共同原则是：{mk('让四肢动，看腰能不能保持不动')}。"))
A.append(h3("屈曲控制"))
A.append(img(2))
A.append(cap("① “服务员鞠躬”：屈髋 50°～70°，腰不能跟着弯"))
A.append(img(3))
A.append(cap("② 坐位伸膝：保持腰椎前凸伸膝，腰不能往后塌"))
A.append(img(4))
A.append(cap("③ 四点跪位向后摇：屈髋到 120°，腰不能弓起来"))
A.append(h3("伸展控制"))
A.append(img(5))
A.append(cap("④ 站立骨盆后倾：能主动后倾骨盆，用臀肌而不是胸椎代偿"))
A.append(img(6))
A.append(cap("⑤ 四点跪位向前摇：骨盆前移，腰不能塌成伸展"))
A.append(img(7))
A.append(cap("⑥ 俯卧主动屈膝（看伸展）：屈膝 ≥90°，腰和骨盆不能往伸展方向动"))
A.append(h3("旋转控制"))
A.append(img(8))
A.append(cap("⑦⑧ 单腿站（左、右）：肚脐侧移两侧对称，相差 ≤2 cm"))
A.append(img(9))
A.append(cap("⑨ 俯卧主动屈膝（看旋转）：屈膝 ≥90°，骨盆不能旋转"))
A.append(img(10))
A.append(cap("⑩ 屈膝仰卧位髋外展：一侧髋外展时，骨盆不能旋转或倾斜"))

A.append(h2("结果"))
A.append(img(11))
A.append(cap("10 项测试的信度（编者根据原文表 2 重画）"))
A.append(table(["测试", "测试者间：资深组", "测试者间：年轻组", "测试者内：评分者 1", "测试者内：评分者 2"], [
    ["服务员鞠躬", "0.71", "0.52", "0.75", "1.0"],
    ["骨盆后倾", "0.60", "0.70", "0.80", "0.80"],
    ["单腿站 右", "0.56", f"{red('0.29')}", "0.64", "0.69"],
    ["单腿站 左", "0.70", "0.80", "0.67", "1.0"],
    ["坐位伸膝", f"{b('0.80')}", "0.64", "1.0", "0.90"],
    ["跪位向后摇", "0.68", "0.45", "0.73", "0.70"],
    ["跪位向前摇", "0.66", "0.69", f"{red('0.22')}", "0.80"],
    ["俯卧屈膝（伸展）", "0.75", f"{red('0.19')}", "0.59", "0.80"],
    ["俯卧屈膝（旋转）", "0.62", "0.54", "0.60", "0.95"],
    ["仰卧髋外展", "0.44", f"{red('0.32')}", "0.84", "0.88"],
]))
A.append(tcap("原文表 2：各测试的 Kappa 值（中文整理；红字为 <0.4）"))
A.append(ul([
    f"{b('测试者间')}：两组平均 Kappa 0.38～0.72；{b('5 项')} >0.6，4 项在 0.4～0.6，1 项 <0.4；一致百分比 65%～97.5%",
    f"{b('测试者内')}：平均 Kappa 0.51～0.95，除 1 项外都 >0.6——{mk('同一个人前后评，比两个人互评更一致')}",
    f"{b('最稳的')}：坐位伸膝、骨盆后倾、单腿站（左）、服务员鞠躬",
    f"{b('最不稳的')}：屈膝仰卧位髋外展（两组都低，0.44 和 0.32）；俯卧屈膝（伸展）和跪位向前摇也要打问号",
    f"{b('经验有用')}：资深组 10 项中有 8 项 Kappa ≥0.60，年轻组只有 4 项",
    "腰痛患者平均有 3～4 项做不好，没有腰痛的人平均 1 项（作者未做进一步分析）",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('看的是录像，不是真人')}：评分者只看一遍、没有病史和症状信息，比临床更“纯”，但也更难；临床中能让患者重复、换角度看，结果可能不同",
    f"{b('只回答“看得准不准”，没回答“有没有用”')}：信度不等于效度——这些测试能不能区分腰痛和非腰痛、能不能指导治疗，本研究没有回答",
    f"{b('评分者少')}：每组只有 2 人，测试者内信度各只有 1 人，结论很大程度取决于这几个人",
    f"{b('培训影响大')}：4 名评分者都说事先的标准培训还可以更充分；年轻组只上过 3 天课程",
    f"{b('Kappa 的“悖论”')}：做错的人很少时，一致百分比很高 Kappa 却可能很低。比如年轻组单腿站（右）一致率 97.5%，Kappa 只有 0.29",
    "优点：测试简单、不需要设备、10 分钟做完；判定标准写得清楚（有角度、有距离）；评分者盲法设计",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('摘要和正文数字不一')}：摘要写测试者间 Kappa 0.24～0.71、{b('6 项')} >0.6；正文和表 2 是两组平均 0.38～0.72、{b('5 项')} >0.6，单组数值则在 0.19～0.80",
    f"{b('“全部 P<0.001”不对')}：结果写测试者内信度“全部 P<0.001”，但表 2 中评分者 1 的跪位向前摇 P＝0.16，并不显著；测试者间“除两项外 P<0.01”，表中其实有 3 项不满足（0.053、0.11、0.012）",
    f"{b('一致率 100% 但 Kappa 不是 1')}：评分者 2 的单腿站（右）、跪位向前摇、俯卧屈膝（旋转）一致率都是 100%，Kappa 却是 0.69、0.8、0.95——两次评分完全一致时 Kappa 应为 1",
    f"{b('一致百分比的分母对不上')}：资深组的 85.7%、92.8%、97.6%、78.6% 只能由 42 例算出（如 36/42），但只有 40 人",
    f"{b('标准误和置信区间对不上')}：如评分者 2 俯卧屈膝（伸展）标准误 0.94、置信区间却只有 0.62～0.98；评分者 1 骨盆后倾标准误 0.01、置信区间却是 0.61～0.99；评分者 2 俯卧屈膝（旋转）置信区间 0.94～0.96 窄得不合理",
    f"{b('“最好的测试”前后不一')}：结果说两组都 >0.6 的是骨盆后倾、单腿站左、坐位伸膝和跪位向前摇；结论却把“服务员鞠躬”列为最好之一（年轻组只有 0.52），没提跪位向前摇",
    f"{b('谁更稳')}：讨论说“经验少的人测试者内信度更高（全部 >0.69）”，但方法没交代评分者 1、2 分别是资深还是年轻的",
    f"{b('样本量计算的写法有误')}：“α＝0.01、power [β＝0.80]”应为 1－β＝0.80；原假设和备择假设写反了",
    f"{b('引用和图表编号')}：Kappa 分级标准引了文献 30（实为 Murphy 的髋伸展测试研究）；正文提到“表 5”，实际只有表 3；图 10 的分图标成“4a～4j”；图 5 和图 8 用了同一个标题；图 9 图注评分规则重复两遍",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('优先用信度较好的几项')}：坐位伸膝、服务员鞠躬（屈曲），骨盆后倾（伸展），单腿站（旋转）",
    f"{b('同一位治疗师跟到底')}：测试者内信度明显好于测试者间，复评最好由同一人完成",
    f"{b('先统一标准再评')}：只把“明显”的代偿判为不正确，经提示能纠正的不算；团队内最好先一起看录像对标准",
    f"{b('看“腰能不能不动”')}：所有测试的核心都是四肢动、腰保持中立——这也可以直接转化为训练动作",
    "这些测试只说明“看得比较一致”，要结合病史、疼痛行为和其他检查来判断是否属于运动控制障碍亚组",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Luomajoki H, Kool J, de Bruin ED, Airaksinen O. Reliability of movement control tests in the lumbar spine. BMC Musculoskelet Disord. 2007;8:90. doi:10.1186/1471-2474-8-90</em><br>"
    "原文以 CC BY 2.0 协议开放获取，版权归原作者所有。本文为学术交流用的中文解读：原文图 1～9 引自原文，图中中文标签为编者所加；信度结果图根据原文表 2 重画，表格为中文翻译。如有侵权请联系删除。"
))

TITLE = "「腰」10 个腰椎运动控制测试，治疗师看得准吗？坐位伸膝、骨盆后倾最稳（附动作图解）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>腰椎运动控制测试推文</title>
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
