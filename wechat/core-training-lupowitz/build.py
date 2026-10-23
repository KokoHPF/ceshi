#!/usr/bin/env python3
"""运动物理治疗中的全面核心训练（Lupowitz 2023）推文。

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


def br(items):
    return "<br>".join(f"• {x}" for x in items)


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2023 年第 18 卷第 4 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Comprehensive Approach to Core Training in Sports Physical Therapy: Optimizing Performance and Minimizing Injuries（运动物理治疗中的全面核心训练：提升表现、减少损伤）",
    f"{b('作者')}：Lewis G. Lupowitz, PT, DPT, CSCS",
    f"{b('机构')}：Orlin & Cohen 骨科集团（Northwell Health 附属机构），美国纽约",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2023;18(4):800-806",
    f"{b('PMCID')}：PMC10399110",
    f"{b('文章类型')}：临床观点（Clinical Viewpoint）",
    f"{b('关键词')}：core training · sports rehab · stabilization training",
], square=True))

A.append(h2("🎯 背景：人人都说练核心，可到底怎么系统地练？"))
A.append(p(
    f"核心为运动员提供{b('稳定、力量传递和损伤预防')}。大家都知道核心要练，但文献里一直缺少一套{hl('系统的、有证据依据的')}核心训练方法。"
))
A.append(p(
    f"本文梳理了核心的解剖、功能、各运动项目的常见核心损伤和临床评估方法，并提出作者自己的四阶段训练框架——{red('“核心四层金字塔”')}：{b('激活 → 稳定 → 整合 → 扰动')}，每一阶段都有进入标准、目标和对应训练。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["环节", "要点"],
    [
        ["核心范围", "肩胛到臀部之间的所有结构：腰-盆-髋复合体，上至膈肌、下至盆底，后至多裂肌、前至腹直肌"],
        ["四大功能", "预判动作 · 稳定脊柱 · 为负重做准备 · 连接上下肢"],
        ["常见损伤", "棒球腹斜肌拉伤、篮球/冰球/足球内收肌拉伤、橄榄球“运动疝”"],
        ["评估", "主观 + 触诊/活动度/呼吸与肋骨位置/内收外展力量比 + 功能测试 + 躯干耐力 + 特殊检查 + 动态核心评估"],
        ["训练框架", "激活 → 稳定 → 整合 → 扰动，按标准逐级进阶"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('先会呼吸、会收紧，再抗住运动、练耐力，然后带进深蹲硬拉等动作，最后在干扰和反应中保持稳定')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、核心的解剖与功能"))
A.append(ul([
    f"核心指{b('肩胛与臀部之间')}的所有结构，包括腰-盆-髋复合体：上至膈肌、下至盆底，后至多裂肌、前至腹直肌",
    f"可分为{b('稳定肌')}（如腹内、外斜肌，离心控制活动范围）和{b('动力肌')}（如腹直肌、髂肋肌，向心加速）",
    f"各肌肉虽可单独训练，但实际通过{b('筋膜链')}（致密结缔组织）协同工作，形成动态系统，像链条一样把力传遍全身",
]))
A.append(table(
    ["核心的四大功能", "说明"],
    [
        ["① 预判动作", "让身体为动态动作提前做好准备"],
        ["② 稳定脊柱", "为力量传递提供坚实基础"],
        ["③ 为负重做准备", "负重活动时提供足够支撑"],
        ["④ 连接上下肢", "走、跑、投掷时协调上下肢动作"],
    ],
))
A.append(p(
    f"{b('核心稳定性')}：中枢神经系统察觉变化、提前募集肌肉，使躯干维持在稳定的骨盆基础上，防止“塌陷”，或在受到扰动后恢复平衡。它关系到动作效率、动态控制和损伤预防。"
))

A.append(h3("❇️二、各运动项目的核心损伤"))
A.append(table(
    ["项目", "主要发现"],
    [
        ["棒球", br(["Conte 等（2012）：腹部拉伤占伤病名单的 5%，2000 年代呈上升趋势；主要是腹内/外斜肌，打者多见，偏向对侧（前导侧）",
                    "Camp、Conte 等（2017）：每年 996 例腹斜肌损伤，共缺阵 22,064 天；小联盟更多，击球最受影响；再伤率 8.15%，赛季早期多见；注射治疗者重返时间更长"])],
        ["篮球", br(["Jackson 等：NBA 24 年（1988～2012）髋部损伤（含腘绳肌、内收肌拉伤）多发生在赛季第一个月",
                    "Patel 等（2010～2019）：72 名球员腹股沟损伤，6 例手术；平均 7～10 场或 17～20 天重返，再伤率 18%（甚至 1.5 年后），但重返后表现无变化"])],
        ["橄榄球", br(["Tramer 等（2010～2016）：NFL 112 名球员非手术治疗的髋和核心损伤，进攻球员缺阵 4.0 ± 5.2 场，防守球员 3.1 ± 2.6 场",
                     "Jack 等（1996～2015）：运动疝手术后 94.7% 重返，防守后卫和外接手最常见"])],
        ["冰球", br(["Tyler 等：腹股沟拉伤 3.2 次/1000 人次比赛暴露",
                    "Emery 等：NHL 训练营期间腹股沟拉伤风险是常规赛的 5 倍、季后赛的 20 倍；90% 为非接触；腹部损伤平均缺席 10.59 次训练/比赛，腹股沟 6.59 次"])],
        ["足球", br(["Giza 等（2005）：美国职业男足 2002 赛季 9.5% 的球员腹股沟拉伤",
                    "Sherman 等：髋和腹股沟损伤占足球损伤的 14%",
                    "Ekstrand 等：肌肉损伤多发生在比赛后段、年长球员；23% 与内收肌有关（平均缺席 14.0 ± 6.2 天）；腹部拉伤 <1%，但平均缺席 12.6 ± 9.2 天"])],
    ],
))

A.append(h3("❇️三、临床评估"))
A.append(p("先了解损伤机制和运动需求，再做主观、客观评估、功能测试和特殊检查，找出损伤的根本原因。"))
A.append(h4("🔻为什么腹直肌和长收肌常受伤"))
A.append(p(
    f"二者力的方向相反，在伸髋和躯干旋转时互为拮抗。它们的纤维在耻骨联合处汇合，形成{b('耻骨腱膜（“耻骨板”）')}，作为二者的支点。"
    "推测任一肌腱受伤都会改变生物力学，削弱骨盆稳定，使耻骨联合更易进一步受伤。"
))
A.append(h4("🔻主观评估"))
A.append(ul([
    f"最常见：运动时出现{b('深部、慢性的腹股沟或下腹痛')}，休息缓解，{b('变向时加重')}",
    "可能描述某处“卡一下”或“咬一下”的感觉；被诱发时会抓住该部位或面露痛苦",
    f"常见损伤机制（Anderson 等，2013）：{b('过度用力旋转、过伸加旋转、脊柱负荷过大、躯干-骨盆分离控制差')}",
]))
A.append(h4("🔻客观评估"))
A.append(ul([
    "触诊核心区压痛；测胸椎和骨盆在不同体位的活动度，观察肋骨位置",
    f"评估{b('膈肌和盆底控制')}：理想状态是 {b('360° 的压力腔')}——呼气时肋骨内旋、膈肌上抬呈穹顶状，骨盆后倾；很多人却是肋骨外旋、膈肌扁平，静息时可见{b('肋骨外翻')}，可能使疼痛迁延",
    f"左侧膈肌位置更低、中心腱更小，可能造成天然的不对称，旋转类运动员尤其容易因此受伤",
    f"{b('内收/外展力量比')}：Tyler 等（2001）发现比值 <80% 者受伤风险高 {red('17 倍')}",
]))
A.append(h4("🔻功能测试"))
A.append(ul([
    "单腿蹲/上台阶、单腿臀桥、躯干耐力测试",
    "Chaudhari 等（2014）：大联盟投手 3 英寸上台阶时骨盆前后偏移峰值越大，赛季中肩伤、UCL 撕裂和其他肘部拉伤风险越高",
    "Meister 等（2021）：职业投手单腿平衡时骨盆偏移大（核心稳定差），与上肢损伤有关",
    "McGill 等：女性屈、伸耐力更好，男性侧桥耐力更好；男性屈/伸耐力比略高",
    "Leetun 等：核心稳定指标低的运动员更易下肢受伤；受伤者髋外展、外旋力量（占体重百分比）更低，侧桥和背伸耐力更差——近端稳定才能保护远端",
]))
A.append(h4("🔻特殊检查"))
A.append(ul([
    "咳嗽试验：咳嗽可能诱发受累部位疼痛",
    f"{b('抗阻内收仰卧起坐试验（RASUT）')}：区分骨盆与髋关节病变、排除运动性耻骨痛；诊断比值比 6.08，敏感度 78%，阴性预测值 88%（图1）",
    f"Kurowicki 等：以下 4 项诱发疼痛或复现症状，识别核心肌肉损伤的{b('敏感度 100%')}（图2）：",
    "　① 4 字位抗阻交叉仰卧起坐：患侧下肢置于 4 字位，对侧肩抗阻向患侧方向抬起",
    "　② 直腿仰卧起坐：双肩和患侧腿抬离床面约 10 英寸（约 25 cm），抗阻保持",
    "　③ 外旋位抗阻屈髋",
    "　④ 4 字位时存在内收肌挛缩",
]))
A.append(pic(2, "图1（左）：抗阻内收仰卧起坐试验（RASUT）；图2（右）：Kurowicki 等的四项核心肌肉损伤检查（照片背景海报上的英文已模糊处理）"))
A.append(h4("🔻个体化动态核心评估"))
A.append(p(
    f"作者让患者取{b('死虫式起始位')}（图3），治疗师从多个方向施加阻力，挑战每条筋膜链的稳定，并与患者沟通哪个方向最难稳住。据此找出缺陷、制定个体化方案。"
))
A.append(pic(3, "图3：死虫式起始位下的个体化动态核心评估（背景海报英文已模糊处理）", "60%"))

A.append(h3("❇️四、核心四层金字塔"))
A.append(p("四个阶段由下到上：激活、稳定、整合、扰动。每一阶段都有进入标准、目标和对应训练。"))
A.append(pic(4, "图4：核心四层金字塔（原图为英文，已按原内容中文重绘，并补充各层要点）", "92%"))
A.append(phase_card("第一层：激活", "", [
    ("目标", br(["减轻疼痛", "恢复正确的呼吸模式", "改善姿势和活动度", "教会核心收紧（bracing）", "提高髋部力量", "患者教育"])),
    ("训练", br(["理疗、生物反馈", "膈式呼吸", "核心等长收缩", "髋部训练", "骨盆摆位", "躯干-髋分离活动练习"])),
]))
A.append(phase_card("第二层：稳定", "", [
    ("进入标准", br(["呼吸协调", "姿势排列良好", "无需提示即可主动收紧核心", "髋力量比（外展:内收）改善", "躯干耐力比改善"])),
    ("目标", br(["近端稳定下远端活动", "产生扭矩和力量", "引入节律性稳定", "恢复躯干耐力比和髋力量比"])),
    ("训练", br(["抗运动训练：死虫、鸟狗、Pallof 推、劈砍、上提", "耐力型核心训练：各种平板支撑（侧桥、哥本哈根）、反向/常规背伸", "臀桥", "平衡/本体感觉训练"])),
]))
A.append(p(
    f"{b('哥本哈根平板支撑的证据')}：Harøy 等在 35 支半职业足球队中做随机对照试验，干预组季前（6～8 周）每周 3 次、赛季中（28 周）每周 1 次做三级哥本哈根平板支撑，"
    f"{red('腹股沟相关损伤率下降 41%')}。"
))
A.append(phase_card("第三层：整合", "", [
    ("进入标准", br(["力量比和耐力比已恢复", "多关节训练中姿势不崩"])),
    ("目标", "给功能性动作模式加负荷"),
    ("训练", br(["深蹲、髋铰链、弓步", "负重行走", "垂直/水平推、划船", "侧滑", "爬行"])),
]))
A.append(phase_card("第四层：扰动", "", [
    ("进入标准", br(["负重下保持良好排列", "不稳定平面上，或稳定平面闭眼时，神经肌肉控制良好"])),
    ("目标", br(["提高中枢神经系统察觉变化、适应外力的能力，改善稳定和力量传递", "缩短反应时间"])),
    ("训练", br(["双任务训练", "徒手抗阻/扰动", "视觉反应任务", "口令反应训练"])),
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：临床观点类文章，“核心四层金字塔”来自作者临床经验，没有验证研究或患者结局数据",
    f"{b('亮点')}：把评估（尤其呼吸/肋骨位置、内收外展比、躯干耐力、特殊检查）和分层训练连在一起，每层有进入标准，便于临床落地",
    f"{b('标准不够量化')}：各阶段的进入标准多为描述性（如“力量比改善”“耐力比恢复”），没有给出具体数值或测试方法",
    f"{b('流行病学部分以美国职业联盟为主')}，与业余或青少年人群的推广性有限；部分研究讲的是髋/腹股沟损伤，与“核心损伤”的界定并不完全一致",
    f"{b('原文小瑕疵')}：图 4 正文未引用；“rectus abdomen”应为 rectus abdominis，“recuts”拼写错误；Chaudhari 写成 Chaudhair；“she light”应为 shed light；Emery 研究“more 5x and 20x more likely”句子重复",
]))

A.append(h2("📌 总结：核心训练四层金字塔"))
A.append(p(
    f"{red('① 先评估')}：问机制和运动需求；看呼吸与肋骨位置，测内收/外展比（<80% 风险高 17 倍）、躯干耐力；做 RASUT 等特殊检查和死虫位动态评估<br>"
    f"{red('② 激活')}：减痛、膈式呼吸、学会收紧核心、髋部力量、躯干-髋分离<br>"
    f"{red('③ 稳定')}：死虫、鸟狗、Pallof、劈砍；侧桥和哥本哈根平板（腹股沟损伤降 41%）<br>"
    f"{red('④ 整合')}：蹲、铰链、弓步、负重走、推拉、爬行，多关节动作中姿势不崩<br>"
    f"{red('⑤ 扰动')}：双任务、徒手扰动、视觉和口令反应，提高反应和适应能力<br>"
    f"{red('⑥ 贯穿始终')}：近端稳定才能保护远端，按标准逐层进阶"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Lupowitz LG. Comprehensive Approach to Core Training in Sports Physical Therapy: Optimizing Performance and Minimizing Injuries. "
    "Int J Sports Phys Ther. 2023;18(4):800-806. PMCID: PMC10399110.</em><br>"
    "文中图片均来自原文：照片背景海报上的英文已模糊处理，图 4 金字塔按原内容中文重绘；原文无表格，文中表格为整理，仅用于学术交流。"
))

TITLE = "「核心」核心训练怎么系统练？激活、稳定、整合、扰动四层金字塔"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>核心训练推文</title>
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
