#!/usr/bin/env python3
"""急性 ACL 损伤体格检查的诊断准确性（Tanaka 2022）推文。

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


def pic(n, t, w=None):
    h = img(n)
    if w:
        h = h.replace("width:100%;max-width:100%;", f"width:{w};max-width:{w};")
    return h + cap(t)


def tcap(t):
    return f'<p style="margin:0 0 8px;font-size:14px;line-height:1.6;color:#000;font-weight:bold;">{t}</p>'


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2022 年第 17 卷第 5 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Diagnostic Accuracy of Physical Examination Tests for Suspected Acute Anterior Cruciate Ligament Injury: A Systematic Review and Meta-Analysis（疑似急性前交叉韧带损伤体格检查的诊断准确性：系统综述与荟萃分析）",
    f"{b('作者')}：Shigeharu Tanaka · Yu Inoue · Yuki Masuda · Hui Tian · Hungu Jung · Ryo Tanaka",
    f"{b('机构')}：神奈川县立保健福祉大学康复学院物理治疗学科（日本）等",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2022;17(5):742-752",
    f"{b('PMCID')}：PMC9340834",
    f"{b('文章类型')}：系统综述与荟萃分析",
    f"{b('证据级别')}：2 级",
    f"{b('注册号')}：UMIN000044766",
    f"{b('关键词')}：anterior cruciate ligament injury · diagnostic test accuracy · physical examination test · systematic review",
], square=True))

A.append(h2("🎯 背景：急性期的 ACL 损伤，最容易漏诊"))
A.append(p(
    f"ACL 损伤多见于急停、变向、跳跃落地的青少年和年轻人。急性期疼痛、肿胀、关节积血，让诊断变得困难：英国两项研究中，急性期正确诊断率只有 {b('28.2%')} 和 {b('14.4%')}，"
    f"确诊中位时间是伤后 {b('6 周')}。延误诊断会推迟治疗，增加膝关节继发损伤的风险。"
))
A.append(p(
    f"MRI 是金标准（LR+ 14.4，LR− 0.1），但体格检查便宜、不需要设备。常用的有 4 个：{b('拉赫曼试验、前抽屉试验、轴移试验、杠杆征试验')}。"
    f"以往的荟萃分析没有把{b('急性期')}单独拿出来分析，也没有把杠杆征和另外三个放在一起比较。"
))
A.append(p(f"本研究专门汇总{hl('伤后 6 周内（急性期）')}青少年和年轻人中这 4 个检查的诊断准确性。"))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["检查", "敏感度", "特异度", "阳性似然比", "阴性似然比", "AUC"],
    [
        ["拉赫曼试验", "0.79", "0.91", "7.63", "0.23", "0.927"],
        ["前抽屉试验", "0.78", "0.91", "6.70", "0.23", "0.919"],
        ["轴移试验", "0.55", b("0.96"), b("11.60"), "0.49", "0.891"],
        ["杠杆征试验", b("0.82"), "0.88", "6.49", b("0.21"), "0.904"],
    ],
))
A.append(small("数值来自原文图 4～6 的合并估计；加粗为四项中最好者。似然比：LR+ >10、LR− <0.1 通常被视为强证据。"))
A.append(p(f"{b('一句话概括')}：{red('急性期想“确诊”看轴移试验（阳性最可靠），想“排除”看杠杆征试验（阴性最可靠）；四个检查的 AUC 都 >0.89，最好组合使用')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、四个检查怎么做"))
A.append(table(
    ["检查", "做法", "阳性"],
    [
        ["拉赫曼试验（a）", "仰卧，屈膝约 15°；一手固定股骨远端，一手握胫骨近端向前拉", "患侧胫骨前移比健侧多"],
        ["前抽屉试验（b）", "仰卧，屈膝 90°；检查者坐在患者足上，双手握胫骨近端，拇指触胫骨平台、示指触内外侧腘绳肌腱，向前拉", "患侧胫骨前移比健侧多"],
        ["轴移试验（c）", "检查者站在患侧，一臂抱住小腿屈膝 90°，另一手掌使胫骨内旋（外侧胫骨平台半脱位），保持内旋慢慢伸膝", "接近完全伸直时胫骨平台复位，出现可听到或可触到的弹响"],
        ["杠杆征试验（d）", "仰卧双腿伸直，检查者一拳放在小腿近端 1/3 下方，另一手在股四头肌远端 1/3 向下压", "足跟不能抬起"],
    ],
))
A.append(pic(2, "图1：四项体格检查——a 拉赫曼试验、b 前抽屉试验、c 轴移试验、d 杠杆征试验（检查名称已改为中文）"))

A.append(h3("❇️二、研究方法"))
A.append(ul([
    "遵循 PRISMA-DTA（诊断准确性系统综述报告规范）",
    "检索 PubMed、MEDLINE、CINAHL、Web of Science 和日本医学数据库医中志（Ichushi），英文和日文，最后检索日期 2021 年 4 月 23 日",
    f"纳入：前瞻性队列或横断面的单门研究，含急性期（{b('伤后 6 周内')}）；能算出真阳性、真阴性、假阳性、假阴性；青少年和年轻人；部分或完全 ACL 损伤；以 MRI 和/或关节镜为参考标准",
    "排除：膝关节手术史；合并骨关节炎、半月板损伤等；仅用问卷或仪器诊断；以“松弛”为诊断",
    "两名评价者独立筛选，用 QUADAS-2 评估偏倚风险；用 Meta-Disc 1.4 合并；异质性显著（I² >50%）时用随机效应模型，否则用固定效应模型；AUC >0.70 视为有效",
]))
A.append(tcap("表1　检索策略"))
A.append(table(
    ["#", "检索式"],
    [
        ["1", "\"Anterior cruciate ligament\"（前交叉韧带）"],
        ["2", "Injury（损伤）"],
        ["3", "Rupture（断裂）"],
        ["4", "Tear（撕裂）"],
        ["5", "#2 OR #3 OR #4"],
        ["6", "\"Lachman test\"（拉赫曼试验）"],
        ["7", "\"Pivot shift test\"（轴移试验）"],
        ["8", "\"Anterior drawer test\"（前抽屉试验）"],
        ["9", "\"Lever sign test\"（杠杆征试验）"],
        ["10", "#6 OR #7 OR #8 OR #9"],
        ["11", "#1 AND #5 AND #10"],
    ],
))

A.append(h3("❇️三、纳入研究"))
A.append(ul([
    "检索到 3,836 篇，去重后 1,536 篇，筛选题目摘要后 86 篇读全文，最终纳入 8 篇（图 2）",
    f"共 {b('620')} 名受试者；6 篇由医生检查，2 篇由物理治疗师检查",
    "拉赫曼试验 8 篇、前抽屉 6 篇、轴移 5 篇、杠杆征 4 篇",
]))
A.append(pic(3, "图2：文献筛选流程（原图为英文，已按原内容中文重绘）", "92%"))
A.append(tcap("表2　纳入研究的特征"))
A.append(table(
    ["研究（年份）", "人数（男/女）", "年龄 均数（范围）", "检查者", "麻醉", "参考标准", "检查：真阳性/真阴性"],
    [
        ["Jarbo 2017", "102（58/44）", "23（15～66）", "医生", "29 人麻醉下<br>15 人清醒", "MRI", "拉赫曼 40/56<br>前抽屉 39/55<br>轴移 26/57<br>杠杆征 28/52"],
        ["Lee 1988", "79（NA）", "NA（14～59）", "医生", "NA", "MRI", "拉赫曼 21/56<br>前抽屉 18/56"],
        ["Massey 2017", "91（61/30）", "28（NA）", "医生", "清醒", "MRI", "拉赫曼 63/17<br>前抽屉 58/16<br>轴移 44/15<br>杠杆征 59/16"],
        ["Gürpınar 2019", "78（69/9）", "26（17～44）", "医生", "清醒", "MRI", "拉赫曼 50/10<br>前抽屉 48/11<br>轴移 32/15<br>杠杆征 57/15"],
        ["Kıyak 2018", "62（NA）", "NA", "医生", "清醒", "MRI", "拉赫曼 14/20<br>前抽屉 10/18<br>轴移 8/22"],
        ["Mulligan 2015", "45（21/24）", "40（20～64）", "物理治疗师", "NA", "MRI、关节镜", "拉赫曼 13/29"],
        ["Mulligan 2017", "60（38/22）", "42（18～65）", "物理治疗师", "NA", "MRI、关节镜", "拉赫曼 9/26<br>杠杆征 20/32"],
        ["Kostov 2014", "103（81/22）", "29（16～58）", "医生", "NA", "关节镜", "拉赫曼 67/30<br>前抽屉 69/30<br>轴移 45/29"],
    ],
))
A.append(small("NA：未报告；MRI：磁共振成像。"))
A.append(h4("🔻偏倚风险"))
A.append(ul([
    "病例选择：1 篇不清楚（未说明是否连续入组）",
    "待评价试验：1 篇高风险（未说明判读时是否不知道参考标准结果，阳性标准也不清楚）",
    f"流程与时间：{b('3 篇高风险')}（没有评估待评价试验与参考标准之间的时间间隔）",
    "三个领域的适用性均为低风险",
]))
A.append(pic(4, "图3：纳入研究的偏倚风险汇总（QUADAS-2，原图为英文，已中文重绘）", "92%"))

A.append(h3("❇️四、结果"))
A.append(pic(5, "图4：四项检查的敏感度和特异度森林图（按原图数据中文重绘；红色菱形为合并估计）"))
A.append(ul([
    f"合并{b('敏感度')}：拉赫曼 0.79（0.74～0.83）、前抽屉 0.78（0.73～0.82）、轴移 {b('0.55')}（0.49～0.60）、杠杆征 {b('0.82')}（0.76～0.87）",
    f"合并{b('特异度')}：拉赫曼 0.91（0.87～0.94）、前抽屉 0.91（0.86～0.95）、轴移 {b('0.96')}（0.91～0.98）、杠杆征 0.88（0.82～0.93）",
    f"敏感度的异质性都很大（I² 77.6%～92.3%）；轴移和杠杆征的特异度异质性为 0",
]))
A.append(pic(6, "图5：四项检查的阳性和阴性似然比森林图（对数刻度，按原图数据中文重绘）"))
A.append(ul([
    f"{b('阳性似然比')}：拉赫曼 7.63、前抽屉 6.70、{red('轴移 11.60（最高）')}、杠杆征 6.49",
    f"{b('阴性似然比')}：拉赫曼 0.23、前抽屉 0.23、轴移 0.49、{red('杠杆征 0.21（最低）')}",
]))
A.append(pic(7, "图6：四项检查的汇总受试者工作特征（SROC）曲线（按原文研究数据和 AUC 中文重绘）"))
A.append(p(f"四项检查的 AUC：拉赫曼 {b('0.9270')}、前抽屉 {b('0.9193')}、轴移 {b('0.8910')}、杠杆征 {b('0.9038')}，均 >0.70，诊断价值良好。"))

A.append(h3("❇️五、讨论"))
A.append(ul([
    f"一般认为 LR+ >10 可以有力地{b('确诊')}，LR− <0.1 可以有力地{b('排除')}。据此作者认为：{b('杠杆征试验适合排除')}，{b('轴移试验适合确诊')}急性 ACL 损伤",
    "与以往结果一致：2016 年系统综述中轴移试验特异度 97.5%、LR+ 16.00；Reiman 等的杠杆征 LR+ 9.2、LR− 0.58",
    "单一体格检查难以完全确诊，组合使用这几个准确性较高的检查，有助于减少误诊",
    f"{b('杠杆征')}是 2010 年代才提出的新检查：操作简单，需要的检查者力量较少，借助重力而非检查者的手感判断，可能更准确；Lichtenberg 等发现其检查者间一致性（kappa）在四项中最高",
]))
A.append(h4("🔻作者自述的局限"))
A.append(ul([
    "未检索常用的 EMBASE 数据库；只看急性期，仅纳入 8 篇",
    "排除了合并半月板损伤和松弛的受试者，推广性受限",
    "没有考虑麻醉的影响（麻醉下肌肉完全放松，可能提高准确性），且部分损伤和完全损伤混在一起",
    "参考标准有 MRI 和关节镜两种，可能引入混合偏倚",
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('亮点')}：首个专门针对急性期、并把杠杆征与另外三项放在一起比较的荟萃分析；方法按 PRISMA-DTA，预先注册，用 QUADAS-2 评估偏倚",
    f"{b('“排除”结论需要谨慎')}：杠杆征 LR− 0.21，并未达到作者自己引用的“<0.1 才算强证据”的标准，而且与拉赫曼（0.23）、前抽屉（0.23）相差很小、置信区间重叠；轴移 LR+ 11.60 达到了确诊标准",
    f"{b('异质性大、研究少')}：敏感度 I² 多在 80%～90% 以上；每项检查只有 4～8 篇；各研究的阳性判定标准、检查者（医生/治疗师）和麻醉状态不一",
    f"{b('“急性期”界定不清')}：纳入标准是“包含急性期”的研究，但部分研究可能混有非急性期患者；表 2 中有的受试者年龄达 60 多岁，与“青少年和年轻人”的定位不完全相符",
    f"{b('前后数字不一致')}：正文说 7 篇用 MRI、1 篇用关节镜、2 篇两者都用（合计 10 篇），实际 8 篇中按表 2 是 5 篇 MRI、1 篇关节镜、2 篇两者都用；麻醉状态“清醒 4、麻醉 1、不清楚 4”合计也是 9 篇；前抽屉敏感度置信区间正文写 0.73～0.83，图中为 0.73～0.82；图 3 把 Gürpınar 拼成 Grüpinar",
    f"{b('结果呈现不全')}：表 2 只给了真阳性和真阴性，没有假阳性和假阴性，读者无法自行复算",
]))

A.append(h2("📌 总结：急性 ACL 损伤怎么查"))
A.append(p(
    f"{red('① 四个检查都有用')}：AUC 0.89～0.93，特异度都在 0.88 以上<br>"
    f"{red('② 想确诊')}：轴移试验阳性最可靠（特异度 0.96、LR+ 11.6），但敏感度只有 0.55，阴性不能排除<br>"
    f"{red('③ 想排除')}：杠杆征阴性相对最可靠（敏感度 0.82、LR− 0.21），但和拉赫曼差别不大，仍未达强排除标准<br>"
    f"{red('④ 拉赫曼和前抽屉')}：表现相近且均衡（敏感度约 0.78、特异度 0.91）<br>"
    f"{red('⑤ 实践')}：组合检查，结合病史；结果不确定时 MRI 确认<br>"
    f"{red('⑥ 证据')}：只有 8 篇研究、异质性大，结论有待更多高质量研究验证"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Tanaka S, Inoue Y, Masuda Y, Tian H, Jung H, Tanaka R. Diagnostic Accuracy of Physical Examination Tests for Suspected Acute Anterior Cruciate "
    "Ligament Injury: A Systematic Review and Meta-Analysis. Int J Sports Phys Ther. 2022;17(5):742-752. PMCID: PMC9340834.</em><br>"
    "图 1 照片来自原文（检查名称已改为中文）；图 2～6 按原文图表数据中文重绘；表 1～2 已译为中文，仅用于学术交流。"
))

TITLE = "「膝关节」急性 ACL 损伤，哪个查体最靠谱？4 项检查的荟萃分析"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>急性ACL查体荟萃分析推文</title>
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
