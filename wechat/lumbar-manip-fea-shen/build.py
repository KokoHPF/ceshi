#!/usr/bin/env python3
"""腰椎旋转扳法两种体位生物力学对比推文：生成 article_body.html 与 preview.html。

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
    "Shen J, Gao X, Zheng H, Zhang X, Li Z, Fan Y, Zhang W, Wang P. Biomechanical comparison of lumbar rotational manipulations in two different positions using force measurement and finite element analysis. Chiropr Man Therap. 2026;34:56.",
    "作者来自中国中医科学院望京医院等单位",
    "实测手法力 + 有限元模拟的生物力学研究（不是临床试验）",
], square=True))

A.append(h2("先说为什么要比这两种扳法"))
A.append(p(
    f"腰椎旋转扳法是腰椎间盘突出、小关节紊乱和腰痛常用的手法，最常见的就是{b('侧卧位')}和{b('坐位')}两种。"
    f"可这两种扳法到底把力传到了哪一节、椎间盘和小关节各受多大的力，{b('一直说不太清')}，手法轻重主要靠医生的经验。"
))
A.append(p(
    f"以往的有限元研究多数只看一种手法，而且输入模型的力往往是“设定”的。这篇的做法是：{mk('先用测力手套把医生真实用的力测出来，再把这些力放进腰椎有限元模型')}，"
    "看两种扳法在椎间盘和小关节软骨上各留下什么样的应力和变形。"
))

A.append(h2("怎么做的"))
A.append(p(b("第一步：测医生的手法力")))
A.append(ul([
    "20 名健康志愿者（20～30 岁，体重指数 18～24），随机分两组，每组 10 人：一组做侧卧位扳法，一组做坐位扳法",
    f"所有扳法都由{b('同一位资深医生')}完成，戴着智能测力手套（薄膜压力传感器 + 无线传输 + 采集软件）",
    "每人左右两侧各扳 3 次，每种扳法一共 60 组数据",
    "再用 K 均值聚类把这 60 组力分成几种“发力模式”",
]))
A.append(pic(2, "智能测力手套系统"))
A.append(p(b("第二步：建腰椎模型")))
A.append(ul([
    "一名 25 岁健康女性（165 cm、60 kg）的 CT，重建 L1～L5",
    "椎体分皮质骨和松质骨，椎间盘分髓核和纤维环，加上终板、小关节软骨和 7 种韧带（弹簧单元）",
    "约 89 万个节点；按体外标本数据核对了屈伸、侧屈、旋转的活动度",
    "L5 下表面固定，把第一步测到的力换算成扭矩加在模型上",
]))
A.append(pic(4, "有限元模型"))

A.append(h2("重点：两种扳法具体怎么操作"))
A.append(p("以右侧为例（对侧反过来做）："))
A.append(p(red("侧卧位扳法")))
A.append(ul([
    "患者左侧卧，左腿伸直，右腿屈髋屈膝搭在左腿上；左臂屈 90° 抱在胸前，右臂沿背后伸",
    f"医生站在患者腹侧，{b('左手放右髋后方，右手放右肩前方')}",
    "以脊柱为轴做旋转，到关节“弹性固定”感后，两手同时做一个短促的斜向扳动",
]))
A.append(p(red("坐位扳法")))
A.append(ul([
    "患者骑坐在方木凳上，两腿自然分开，右手放头顶，左手从胸前伸到右腋下",
    f"医生坐在患者身后，{b('左手拇指指腹顶在 L4 棘突右侧')}，右臂从患者右腋下穿过搭到左肩",
    "带着腰椎慢慢右转，同时左拇指向左推棘突；到“锁住”感后，两手同步做一个短促的旋转扳动",
]))
A.append(pic(3, "两种扳法的操作"))

A.append(h2("重点：医生实际用了多大的力"))
A.append(ul([
    f"侧卧位：左右两侧没有差别。肩部力约 52 vs 57 N，髋部力中位数约 86 vs 81 N——{b('髋部用力明显比肩部大')}",
    f"坐位：{mk('右侧扳的肩部力比左侧大（78 vs 63 N）')}，腰部（拇指）力左侧反而大一点（33 vs 26 N）",
    "作者推测可能和医生的优势手有关，但只有一位医生，分不清是“优势手”还是“这位医生的习惯”",
]))
A.append(p("聚类以后，侧卧位分出两种发力模式，坐位分出三种："))
A.append(pic(5, "手法力聚类散点图"))
A.append(pic(9, "各发力模式的实测力和输入模型的扭矩"))
A.append(p(
    f"可以看到：侧卧位的“{b('髋主导型')}”髋部力达到 120 N 以上，换算到 L5 的扭矩约 24 N·m；"
    f"坐位以“{b('肩主导型')}”最多（55%），力主要来自肩部，拇指推棘突的力只有 26 N 左右。"
))

A.append(h2("重点：模型里看到了什么"))
A.append(p(f"一句话：{mk('侧卧位“高应力、低位移”，集中在下腰段；坐位“低应力、高位移”，集中在上腰段')}。"))
A.append(pic(6, "侧卧位扳法有限元结果"))
A.append(ul([
    "侧卧位两种模式：椎间盘最大应力 7.9～13.4 MPa，最大变形 7.2～12.3 mm",
    f"髋主导型最“重”：{b('L3/4 椎间盘应力最高（13.4 MPa），L4/5 变形最大（12.3 mm）')}，小关节软骨应力也最高（15.0 MPa）",
]))
A.append(pic(7, "坐位扳法有限元结果"))
A.append(ul([
    "坐位三种模式：椎间盘最大应力 5.9～8.1 MPa，比侧卧位低；但最大变形 11.7～16.4 mm，比侧卧位大",
    f"变形主要在{b('上腰段（L1/2～L2/3）')}；肩主导型的变形最大（16.4 mm），轻柔加载型各项都最低",
]))
A.append(pic(8, "五种发力模式的峰值对比"))
A.append(p(
    f"另一个共同点：{mk('两种扳法都在 L4/5 小关节软骨出现应力集中')}。"
    "作者的解释是：侧卧位通过骨盆加载，力臂短，力直接压到下腰段；坐位靠脊柱轴向旋转，力臂长，要转到终末位需要更大的位移，力被分摊到更多节段上。"
))

A.append(h2("这些结果能信几分"))
A.append(ul([
    "测力的是健康年轻人、只有一位医生，每种扳法 10 个人；对 60 组数据做聚类，样本偏小，同一个人的 6 次数据也不独立",
    "同一次连扳 3 次，后面几次可能受前面关节“打开”、组织放松的影响",
    f"模型只有{b('一名健康女性')}，没有椎间盘突出等病变；材料是线弹性、静态加载，{b('没有肌肉')}，也没有骨盆",
    "把手上测到的力乘以一个固定力臂（20 cm 或 6 cm）当成扭矩直接加在 L1/L5 上，这一步简化很大",
    f"作者自己也说：这些应力、位移只能看“{b('相对模式')}”，不能当成组织会不会损伤的直接证据",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "坐位腰部力 Z = 2.129，对应双侧 P ≈ 0.033，原文写 0.042",
    "图 5 标题写的是“俯卧位”扳法，实际研究的是侧卧位",
    "图 4 把纤维环拼成了“Nnulus fibrosus”",
    "方法里说 L5 下表面完全固定，但侧卧位又在 L5 上加了一个反向扭矩——固定面上加载的意义说得不清楚",
    f"椎间盘“总变形”12～16 mm 明显超出一个椎间盘本身能有的形变，应该是整段的位移叠加，原文却据此说“{b('超出正常生理范围')}”",
    "模型验证：L2/3 侧屈 10.7° vs 文献 14.0 ± 1.2°，差距不小，仍被描述为“基本一致”",
    "用椎间盘的等效应力去和松质骨屈服强度（约 10 MPa）比较，组织类型不同（作者随后也承认不能直接等同）",
    "讨论说侧卧位的力“经骶髂关节传到下腰段”，但模型只建到 L5，没有骨盆和骶髂关节",
    "输入扭矩 8～24 N·m，超出验证时用的 10 N·m，模型在这个范围是否仍可靠没有交代",
    "引言说扳法“疗效已经确立”，说法偏满",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('下腰段问题（比如 L4/5 小关节紊乱）更像侧卧位扳法的“目标区”')}；上腰段、胸腰交界的僵硬更像坐位扳法的“目标区”——但这是模型推断，不是疗效证据",
    f"侧卧位别让髋部力“一枝独秀”：髋主导型在下腰段的应力最高，{b('骨质差、终板脆弱、退变明显')}的人要格外收着",
    "坐位位移大，上腰段神经根受压的患者可能受益，但幅度要控制，注意神经症状",
    "两种扳法都会让 L4/5 小关节软骨受力集中，这个节段要多留心",
    "坐位左右两侧用力可能不对称，练手法时有意识地对齐两侧的发力",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　腰椎有限元模型的材料参数"))
A.append(table(["材料", "弹性模量（MPa）", "泊松比", "刚度（N/mm）"], [
    ["皮质骨", "12000", "0.3", "—"], ["松质骨", "100", "0.3", "—"], ["终板", "25", "0.25", "—"],
    ["纤维环", "4.2", "0.45", "—"], ["髓核", "1", "0.49", "—"], ["小关节软骨", "10.4", "0.4", "—"],
    ["前纵韧带", "—", "—", "8.74"], ["后纵韧带", "—", "—", "5.83"], ["黄韧带", "—", "—", "15.38"],
    ["棘间韧带", "—", "—", "10.85"], ["棘上韧带", "—", "—", "2.39"], ["横突间韧带", "—", "—", "0.19"]]))
A.append(tcap("表 2　侧卧位扳法左右两侧手法力比较"))
A.append(table(["力参数", "左侧（n = 30）", "右侧（n = 30）", "t / Z 值", "P 值"], [
    ["肩部力（N）", "51.99 ± 15.66", "57.00 ± 17.42", "−1.231", "0.228"],
    ["髋部力（N）", "85.60（72.45～103.66）", "81.48（60.17～124.53）", "−0.946", "0.344"]]))
A.append(tcap("表 3　侧卧位扳法手法力聚类"))
A.append(table(["聚类", "肩部平均力（N）", "髋部平均力（N）", "样本数", "占比"], [
    ["1 肩髋协调型", "64.61", "71.37", "34", "56.7%"], ["2 髋主导型", "41.26", "121.62", "26", "43.3%"]]))
A.append(tcap("表 4　坐位扳法左右两侧手法力比较"))
A.append(table(["力参数", "左侧（n = 30）", "右侧（n = 30）", "t / Z 值", "P 值"], [
    ["肩部力（N）", "62.56 ± 15.58", "77.70 ± 7.72", "−10.088", "&lt; 0.001"],
    ["腰部力（N）", "32.80（27.75～38.20）", "26.06（22.66～33.54）", "2.129", "0.042"]]))
A.append(tcap("表 5　坐位扳法手法力聚类"))
A.append(table(["聚类", "肩部平均力（N）", "腰部平均力（N）", "样本数", "占比"], [
    ["1 肩腰协调型", "70.13", "47.37", "13", "21.7%"], ["2 肩主导型", "78.59", "26.16", "33", "55.0%"],
    ["3 轻柔加载型", "50.20", "30.85", "14", "23.3%"]]))
A.append(tcap("表 6　模型各节段活动度验证（°）"))
A.append(table(["节段", "屈伸：本研究 / 文献", "左右侧屈：本研究 / 文献", "左右旋转：本研究 / 文献"], [
    ["L1/2", "10.1 / 10.1 ± 1.1", "9.9 / 9.9 ± 0.8", "5.5 / 4.6 ± 1.1"],
    ["L2/3", "11.0 / 10.8 ± 0.6", "10.7 / 14.0 ± 1.2", "6.2 / 5.2 ± 0.8"],
    ["L3/4", "12.2 / 11.2 ± 1.1", "10.2 / 11.5 ± 0.8", "5.6 / 5.2 ± 0.8"],
    ["L4/5", "13.0 / 14.7 ± 1.1", "9.7 / 11.4 ± 1.0", "4.2 / 4.4 ± 0.8"]]))
A.append(small("文献数据为 Yamamoto 体外标本研究。"))
A.append(tcap("表 7　五种发力模式的有限元应力与位移统计"))
T7 = [("椎间盘等效应力（MPa）", [("7.8686", "0.6743", "0.0123"), ("13.4001", "0.7720", "0.0167"), ("7.4277", "0.7623", "0.0157"), ("8.0874", "0.8470", "0.0189"), ("5.8738", "0.5985", "0.0159")]),
      ("椎间盘总变形（mm）", [("7.2165", "2.4436", "0.0002"), ("12.3090", "3.2221", "0.0004"), ("14.7910", "4.9275", "0.0016"), ("16.4390", "5.5405", "0.0016"), ("11.6770", "3.9523", "0.0015")]),
      ("小关节软骨等效应力（MPa）", [("8.8213", "2.7731", "0.2485"), ("15.0320", "3.4454", "0.1587"), ("8.3299", "2.6842", "0.1697"), ("9.9368", "3.0998", "0.2724"), ("6.6952", "1.9414", "0.0748")]),
      ("小关节软骨总变形（mm）", [("3.5502", "1.3787", "0.0089"), ("6.0592", "1.9990", "0.0078"), ("9.0523", "2.9286", "0.0099"), ("9.5503", "3.0370", "0.0136"), ("8.0447", "2.7382", "0.0066")])]
rows = []
for name, vals in T7:
    rows.append([b(name), "", "", "", "", ""])
    for i, lab in enumerate(["最大", "平均", "最小"]):
        rows.append([lab] + [v[i] for v in vals])
A.append(table(["指标", "侧卧位 肩髋协调", "侧卧位 髋主导", "坐位 肩腰协调", "坐位 肩主导", "坐位 轻柔加载"], rows))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Shen J, Gao X, Zheng H, Zhang X, Li Z, Fan Y, Zhang W, Wang P. Biomechanical comparison of lumbar rotational manipulations in two different positions using force measurement and finite element analysis. Chiropr Man Therap. 2026;34:56. doi:10.1186/s12998-026-00683-7</em><br>"
    "原文以 CC BY 4.0 协议开放获取。本文为学术交流用的中文解读，图 1～8 引自原文（编者改为中文标注、鞋子标志已模糊，图 1B 软件界面按原图重绘），图 9 与力和扭矩卡片为编者据原文数据绘制，附录表格为编者翻译整理。"
))

TITLE = "「腰椎扳法」侧卧位 vs 坐位：实测手法力 + 有限元，力都去哪了？"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>腰椎扳法生物力学推文</title>
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
