#!/usr/bin/env python3
"""Voight 等 2010 运动人群髋关节镜术后康复指南 推文正文生成

用法：python3 build.py   # 生成 article_body.html 和 preview.html
"""
import pathlib

HERE = pathlib.Path(__file__).parent


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
    "Voight ML, Robinson K, Gill L, Griffin K. Postoperative rehabilitation guidelines for hip arthroscopy in an active population. Sports Health. 2010;2(3):222-230. doi:10.1177/1941738110366383",
    "中文题目：运动人群髋关节镜术后康复指南",
    "作者来自美国贝尔蒙特大学、Titleist 高尔夫表现研究所（TPI）、STAR 物理治疗诊所",
    "文章类型：临床综述（检索 PubMed、EMBASE、PEDro，1992～2009 年），给出四阶段康复框架；样本方案见在线附录",
], square=True))

A.append(h2("研究背景：手术能修结构，功能要靠康复"))
A.append(p(
    f"过去十年髋关节镜越来越普及，髋关节内的问题（盂唇损伤、游离体、股骨髋臼撞击等）被更多地发现和处理。{b('手术可以解决机械性问题，功能缺陷却要靠康复来纠正')}。但髋关节镜术后康复的研究证据很少，很多做法借鉴自膝、肩、肘、踝的微创术后康复。"
))
A.append(ul([
    f"康复目标：{b('减轻症状')}（控制疼痛和炎症）、{b('恢复功能')}（活动度、力量、本体感觉、耐力），按病情和功能需求系统推进",
    f"{b('患者教育是基础')}：患者要明白注意事项和进阶节奏；和医生沟通，定出合理目标",
    f"{b('不同术式节奏差别很大')}：退变明显者恢复慢，居家方案可能就够；软骨磨削成形、微骨折需要较长时间保护性负重；关节其他方面健康的盂唇修复者可以推进得更积极，最好在设备齐全的机构康复",
]))
A.append(p(f"原文附录 A 给出了{b('不需要太多生物愈合')}的术式（游离体取出、盂唇清理、滑膜切除、圆韧带清理等）的样本方案，附录 B 给出了{b('需要较多生物愈合')}的术式（盂唇修复、微骨折、股骨成形）的方案（仅在线提供，本文未收录）。"))

A.append(h2("方法：四个阶段怎么练"))
A.append(pic(2, "四个阶段一览（编者根据原文整理）"))

A.append(h3("术前：康复从手术前开始"))
A.append(ul([
    "可以是结构化的术前预康复，处理疼痛、肿胀、姿势偏差、代偿动作、活动度丢失、本体感觉下降和整体力量耐力；也可以只做一次全面的术前宣教",
    "离开门诊前就要掌握负重限制、伤口护理和助行器使用",
    f"术后马上开始{b('髋部等长收缩和踝泵')}，促进下肢循环",
]))

A.append(h3("阶段 1：活动度与初期训练"))
A.append(p(f"目标：{b('保护修复组织、减轻疼痛炎症、恢复无痛活动度、防止肌肉抑制、不拄拐正常走路')}。这一阶段主要受软组织愈合限制，同时要避免制动的负面影响。"))
A.append(ul([
    f"{b('负重')}：不需要大量愈合的术式，通常允许{b('足平放负重')}、1 周内脱拐；盂唇修复、微骨折等需要愈合的，可能限制负重{red('长达 8～10 周')}",
    f"{b('为什么是“足平放”而不是完全不负重')}：完全不着地需要很大的肌肉力量把腿悬空，反而在关节上产生明显的压力；让腿的重量放在地上，可以抵消这部分肌肉收缩产生的压力",
    f"{b('臀中肌容易“掉线”')}：前外侧和后外侧入路都穿过臀中肌，术后常见反射性抑制，走路会出现特伦德伦堡步态（摆动侧骨盆下沉）；用拐杖帮助减少骨盆下沉、恢复正常步态",
]))
A.append(pic(3, "原文图 1（加中文说明）"))
A.append(ul([
    f"{b('早期活动度')}：为减少关节周围粘连，重点做{b('被动内旋和屈曲')}，防止关节囊和盂唇之间形成瘢痕；后关节囊紧会限制屈髋和内旋，可用四点跪位前后摇牵伸",
    f"{b('牵伸只到能忍受')}：各平面都练，末端由不适程度决定；硬推极限对功能帮助不大，还会加重不适。例外：切除了阻挡活动的大骨赘后，早期积极牵伸可以拿回原来被挡住的活动度",
    f"{b('固定自行车')}：无阻力或很小阻力，{b('每天骑')}；{red('不要用卧式自行车，也不要低头俯身')}，避免屈髋过大",
]))
A.append(pic(4, "原文图 2、图 3（加中文说明）"))
A.append(ul([
    f"{b('手法')}：小幅度附属振动刺激关节机械感受器、帮助止痛并保持关节囊活动度；关节中度疼痛时轻柔地做屈曲内收或内旋方向的分级松动",
    f"{b('牵引')}：活动时疼痛明显的阶段最有用，沿股骨长轴轻柔振动牵拉，可在不同屈髋角度做",
    f"{b('三维松动')}：把股骨旋转到受限位置，再做纵向或向下滑动；负重时痛的人，可在“压缩”方向做振动、停在疼痛位置之前",
    "髋臼内前后方向活动很少，但前后滑动可用于止痛；在生理活动末端做附属滑动可以增加活动度",
    f"{b('关节囊模式')}：术后积液常造成屈曲、外展、内旋明显受限，伸展和外旋丢失较少；疼痛受限时要仔细评估末端感觉，再决定能不能松动",
]))
A.append(pic(5, "原文图 4（加中文说明）"))
A.append(ul([
    f"{b('第一周内开始肌肉激活')}：等长收缩最简单、最不容易刺激关节，包括臀肌、股四头肌、腘绳肌、内收肌、外展肌和下腹部；拮抗肌等长收缩可能缓解痉挛和疼痛",
    f"{b('重点练臀肌')}：骨盆中立位下做臀肌等长收缩，可能减轻髂腰肌痉挛和前髋痛；侧卧、俯卧徒手肌力测试评估臀肌，{b('单腿蹲')}评估单腿支撑的动态质量",
    f"{b('蚌式进阶')}：侧卧屈髋约 30°，先外旋（臀中肌后部），再反向蚌式内旋（臀中肌前中部），再抬腿与地面平行做内旋",
    "同期可以开始双腿臀桥、小范围腿举和小蹲，练臀大肌",
]))
A.append(pic(6, "原文图 5（加中文说明）"))
A.append(ul([
    f"{b('水中训练')}：伤口愈合、拆线后即可开始，浮力提供安全阻力，在齐腰深水中练步态，各平面活动都更容易",
    f"{b('进入阶段 2 的条件')}：{mk('活动度接近完全、不拄拐步态正常、几乎不痛')}",
]))

A.append(h3("阶段 2：中期训练与稳定（通常第 4 周起）"))
A.append(ul([
    "继续活动度训练直到完全无痛，同时加强力量和稳定训练，加入负重和渐进抗阻",
    f"{b('纠正肌肉失衡和代偿')}：长期过用或损伤会造成神经肌肉功能受损，表现为关节源性抑制、协同肌代偿主动肌、紧张肌肉抑制其拮抗肌",
    f"{b('最常见的失衡')}：{b('屈髋肌和竖脊肌紧、臀肌和腹肌弱')}，造成骨盆前倾、腰椎前凸增大",
    f"既往研究认为肌电激活{b('超过 50%～60% 最大自主收缩')}的动作足以增强力量（原文表 1）",
]))
A.append(pic(7, "原文表 1（编者翻译）"))
A.append(pic(8, "原文图 6（加中文说明）"))
A.append(p(f"{b('核心稳定常被忽视')}：很多人四肢专项肌肉的力量、爆发力和耐力都够了，腰-骨盆-髋复合体却不够。核心训练与髋部抗阻训练同步推进，并用 4 个动作筛查核心稳定。"))
A.append(pic(9, "原文图 7（加中文说明）"))
A.append(pic(10, "原文图 8、图 9（加中文说明）"))
A.append(pic(11, "原文图 10、图 11（加中文说明）"))
A.append(ul([
    f"{b('骨盆前后倾')}：检查髋和腰椎活动度以及骨盆姿势控制",
    f"{b('骨盆旋转')}：下半身能否独立于上半身旋转，需要脊柱、髋、骨盆活动度和躯干稳定",
    f"{b('躯干旋转')}：上半身能否独立于下半身旋转，腰线以下不应动",
    f"{b('臀桥伸膝')}：保持 10 秒；悬空侧骨盆下沉或支撑腿抖，提示{b('支撑侧臀肌弱')}；支撑侧腘绳肌或下背抽筋，提示{b('臀肌被抑制')}、由协同肌代偿",
]))

A.append(h3("阶段 3：进阶训练与神经肌肉控制"))
A.append(ul([
    f"关节损伤常伴随本体感觉缺陷；{b('髋臼盂唇有游离神经末梢和感受器')}，还能维持关节内负压、增加稳定，损伤后稳定性可能下降",
    "早期做关节位置觉训练，之后在功能模式和调整后的活动范围内做本体感觉神经肌肉促进",
    f"{b('闭链训练')}逐步增加下肢负重转移，减少关节面剪切和平移力",
    f"{b('平衡进阶')}：双脚站 → 单脚站（睁眼 / 闭眼）→ 双侧提踵、小蹲 → 单侧提踵、小蹲；部分深蹲、弓步、动态重心转移{b('先在水中做')}",
    f"{b('进阶原则')}：慢 → 快、简单 → 复杂、稳定 → 不稳定、低负荷 → 高负荷、一般 → 专项；平衡器材、小蹦床、结合上肢动作的平衡训练进一步挑战神经肌肉系统",
]))
A.append(pic(12, "原文图 12、图 13（加中文说明）"))

A.append(h3("阶段 4：回归运动"))
A.append(ul([
    "回归时间取决于髋关节病变和预期活动的具体要求",
    "模拟日常和专项动作的功能训练要在病变允许的范围内个体化",
    "根据病变程度和术式，愈合期间可能需要限制或调整运动产生的压缩负荷",
]))

A.append(h2("结果：作者的结论"))
A.append(p(
    f"髋关节镜术后康复普遍被认为很重要，但{red('支持具体康复方案的循证研究很有限')}。作者认为康复的共同目标应是{b('无痛活动和长期恢复髋关节功能')}；摘要称现有结局数据表明这一目标正在实现，但还需要更多数据验证长期效果。"
))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{b('本质是专家经验')}：虽然写了检索数据库和年份，但没有报告检索结果、纳入了哪些研究、证据质量如何，属于叙述性综述",
    f"{b('没有给出疗效数据')}：正文没有任何结局数据，阶段划分、时间节点和动作选择都没有对照研究支持",
    f"{b('后期阶段太粗')}：阶段 3、阶段 4 既没有时间范围也没有进阶标准，回归运动没有任何功能测试或量化标准",
    f"{b('核心筛查缺少依据')}：4 个筛查动作（作者之一来自 TPI）没有信度、效度或判定标准",
    f"{b('时间较早')}：发表于 2010 年，之后髋关节镜术后康复已有更多基于标准的进阶方案和回归运动测试，使用时要结合新证据",
    f"{b('价值在于框架和动作库')}：四阶段思路、足平放负重的力学解释、臀中肌抑制的处理和 13 张动作图，作为临床参考很实用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('摘要说“结局数据表明目标正在实现”')}：正文没有给出任何结局数据",
    f"{b('检索年份与参考文献')}：摘要说检索 1992～2009 年文献，参考文献里却有 1971、1977、1978、1980 年的文献；检索结果和纳入标准都没有报告",
    f"{b('阶段 2 的时间与负重限制矛盾')}：阶段 2“通常从第 4 周开始”、进入条件包括不拄拐步态正常，但盂唇修复、微骨折可能限制负重 8～10 周，这类患者第 4 周不可能达标",
    f"{b('蚌式“强调内旋”')}：正文说蚌式进阶用来强调内旋，随后描述的第一步却是外旋；图 4 图注写“通过旋转骨盆分开双膝”，而蚌式通常要求骨盆不动",
    f"{b('表 1 来源不清')}：表 1 引用的文献 13（Ekstrom 等 2007）只分析了 9 个康复动作，表 1 列出 14 项（单腿深蹲、单腿硬拉、单腿臀桥在两列重复出现），部分动作来源没有交代",
    f"{b('“骨盆前后倾的质量和幅度反映日常使用频率”')}：这一说法没有给出依据",
    f"{b('参考文献拼写')}：Crowninshield 写成 Crowninsheild，Kelly、Philippon 写成 Kelley、Philapon，Thieme 写成 Theime，limbus 写成 lumbus；第四作者 Griffin 在文献 16、22 中写作 Griffen",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先问清术式')}：清理类和修复类（盂唇修复、微骨折、股骨成形）的负重和进阶节奏完全不同，按医生的负重医嘱来",
    f"{b('能足平放就别悬空')}：允许的话让腿的重量放在地上，比完全悬空对关节的压力更小",
    f"{b('第一周就开始')}：髋部等长收缩、踝泵、无阻力固定自行车（不用卧式、不低头俯身）",
    f"{b('盯住臀中肌')}：蚌式进阶、侧卧外展、侧平板外展；用单腿蹲和臀桥伸膝检查骨盆控制",
    f"{b('活动度不硬推')}：重点恢复屈髋和内旋，只牵伸到能忍受；关节囊紧可配合牵引和三维松动",
    f"{b('用标准而不是时间进阶')}：活动度接近完全、不拄拐步态正常、几乎不痛再进入阶段 2；后期补充力量测试、跳跃和专项测试作为回归标准（原文没有给出，编者补充）",
    f"{b('水中训练是好帮手')}：伤口愈合后就能下水，弓步、部分深蹲可以先在水中做",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　肌电激活超过 50% 最大自主收缩、可用于增强臀中肌和臀大肌的动作"))
A.append(table(["臀中肌", "臀大肌"], [
    ["侧平板 + 髋外展", "单腿硬拉"],
    ["侧卧髋外展", "单腿深蹲"],
    ["单腿臀桥 + 核心激活", "上台阶 + 伸髋"],
    ["单腿深蹲", "平板支撑 + 伸髋"],
    ["弹力带侧向走", "弹力带后退走"],
    ["单腿硬拉", "单腿臀桥 + 核心激活"],
    ["反向蚌式进阶", "四点跪位抗阻伸髋"],
], first_bold=False))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Voight ML, Robinson K, Gill L, Griffin K. Postoperative rehabilitation guidelines for hip arthroscopy in an active population. Sports Health. 2010;2(3):222-230. doi:10.1177/1941738110366383</em><br>"
    "原文版权 © 2010 The Author(s)，SAGE 出版。本文为中文解读，仅作学术交流：照片引自原文图 1～图 13（编者加中文说明），四阶段总览为编者根据原文整理，表格为编者翻译。"
))

TITLE = "「髋关节」髋关节镜术后怎么练？运动人群四阶段康复指南（附 13 张动作图）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>髋关节镜术后康复推文</title>
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
