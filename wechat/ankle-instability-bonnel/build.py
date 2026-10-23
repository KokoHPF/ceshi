#!/usr/bin/env python3
"""慢性踝关节不稳的生物力学与病理力学（Bonnel 2010）推文。

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


A = []
A.append(img(1))
A.append(cap("原文首页（OTSR 2010 年第 96 卷）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Chronic ankle instability: Biomechanics and pathomechanics of ligaments injury and associated lesions（慢性踝关节不稳：韧带损伤及合并损伤的生物力学与病理力学）",
    f"{b('作者')}：F. Bonnel, E. Toullec, C. Mabit, Y. Tourné, 以及法国骨科与创伤外科学会（Sofcot）",
    f"{b('机构')}：蒙彼利埃解剖实验室 · 波尔多 Tondu 私立医院 · 利摩日 Dupuytren 教学医院 · 格勒诺布尔 Republic 外科集团",
    f"{b('期刊')}：Orthopaedics & Traumatology: Surgery & Research（OTSR）",
    f"{b('年卷期')}：2010;96(4):424-432",
    f"{b('DOI')}：10.1016/j.otsr.2010.04.003",
    f"{b('文章类型')}：综述（Review article），基于文献和 2008 年 Sofcot 专题研讨会资料",
    f"{b('证据级别')}：原文未标注（属于综述）",
    f"{b('关键词')}：Ankle anatomy · Subtalar joint · Chronic ankle instability · Ligament reconstruction · Proprioception · Ankle osteoarthritis",
], square=True))

A.append(h2("🎯 背景：为什么有的崴脚会变成“老崴脚”？"))
A.append(p(
    f"慢性踝关节不稳的危险因素分为两类：{b('内因')}（骨、韧带、姿势等个体形态及其变异）和{b('外因')}（运动或职业中的损伤机制）。"
    f"两者相互作用，决定了一次扭伤会不会发展成慢性不稳。"
))
A.append(quote(
    "The biomechanics of the ankle cannot be reduced to a simple flexion—extension movement with one degree of freedom as characterized by the talocrural joint: its function cannot be dissociated from the subtalar joint.",
    "踝关节的生物力学不能简化为距小腿关节那样单一自由度的屈伸运动：它的功能与距下关节密不可分。",
))
A.append(p(f"理解这些因素，有助于选择检查手段、制定治疗策略。"))

A.append(h2("🔴 核心框架：从形态到不稳"))
A.append(table(
    ["层面", "关键内容"],
    [
        ["骨性形态", "距骨滑车像“截锥体”；内外侧曲率半径不同，分为 3 型，影响韧带受力"],
        ["韧带系统", "外侧副韧带三部分 ＋ 距下关节的颈韧带和距跟骨间韧带"],
        ["关节运动", "滚动＋滑动＋旋转的多轴运动；跖屈位潜在不稳"],
        ["损伤机制", "内翻最常见：先伤颈韧带和距腓前韧带"],
        ["不稳类型", "机械性不稳（韧带松弛、骨性异常）与功能性不稳（本体感觉缺陷、姿势问题）"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('慢性踝不稳是骨形态、韧带、本体感觉和足部姿势共同作用的结果')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、骨性因素：距骨是个“歪的截锥体”"))
A.append(ul([
    f"{b('截锥体')}：距骨滑车顶角平均 {b('24°（±11°）')}；旋转轴在冠状面向外下倾斜（与胫骨轴成 82°±3.6°，经过两踝尖下方），在水平面向后外与膝横轴成 20°～30°",
    f"{b('不对称')}：外侧缘比内侧缘更倾斜；滑车{b('前宽后窄')}，前后宽度平均相差 4±2 mm；外侧缘后部有一个斜面三角区",
    f"{b('三个圆')}：外侧缘由两个不同平面的圆组成（“外踝圆”平行于矢状面、“距骨外侧圆”倾斜 45°），两圆在中前部汇合、向后分开形成三角区；内侧为圆钝的“距骨内侧圆”",
]))
A.append(pic(2, "图1：距骨形态，不对称的截锥体"))
A.append(p(b("距骨滑车按内外侧曲率半径分 3 型：")))
A.append(table(
    ["分型", "曲率半径", "Bonnel 解剖", "Bedin-Mabit CT（32 例）"],
    [
        ["1 型", "内侧 ＜ 外侧", "86%", "66%（内侧 17 mm，外侧 20 mm）"],
        ["2 型", "内侧 ＝ 外侧", "11%", "19%（均为 18.6 mm）"],
        ["3 型", "内侧 ＞ 外侧", "3%", "15%（内侧 21 mm，外侧 19 mm）"],
    ],
))
A.append(pic(3, "图2：距骨曲率半径的 CT 生物测量研究（32 个距骨，Bedin-Mabit）"))
A.append(p(
    f"{b('运动方式')}：Barnett 和 Hicks 发现跖屈和背伸有两条不同的轴。距骨可以做纯旋转，也可以做{b('滚动（旋转＋滑动）')}，两者可同时出现。"
    f"滚动时瞬时旋转中心集中，说明关节面匹配良好；分散则提示关节功能紊乱。"
))
A.append(pic(4, "图3：滚动/滑动运动示意。1 型距骨使距腓前韧带紧张，3 型则保护距腓前韧带", w="86%"))
A.append(p(
    f"{b('矢状面稳定')}：推进期距骨嵌入踝穴，像拱顶石一样中和剪切力；关节面的凹凸形态和踝穴顶向前倾斜 5° 也参与稳定。"
))

A.append(h3("❇️二、韧带因素"))
A.append(h4("🔻1. 外侧副韧带（三部分）"))
A.append(ul([
    f"{b('距腓前韧带')}：起于外踝前缘，水平向前下，止于距骨颈、外踝关节面前方；很短，由上向下稍增宽",
    f"{b('跟腓韧带')}：被腓骨肌腱鞘覆盖，起于外踝尖，向后下止于跟骨外侧面；{red('特点是向后倾斜，与外踝轴成 45°')}",
    f"{b('距腓后韧带')}：位置很深、非常强韧，从外踝后窝水平止于距骨后面、滑车正下方",
    f"{b('变异')}：距腓前韧带可为双束，或在前、中韧带之间有副韧带",
]))
A.append(img(5))
A.append(cap("图4（左）：外侧韧带层面，跟腓韧带向后倾斜；图5（右）：距腓前韧带（1）和跟腓韧带（2）的解剖变异示例"))
A.append(h4("🔻2. 内侧副韧带（三角韧带）"))
A.append(ul([
    f"{b('浅层')}：呈三角形，起于内踝尖后散开——胫距后部（最强，止于距骨内侧结节）、胫跟部（垂直止于载距突内缘）、胫舟部和胫距前部（止于足舟骨和跖侧跟舟韧带即弹簧韧带）",
    f"{b('“足髋臼”（coxa pedis）')}：浅层与跟舟跖侧韧带一起，构成距骨周围关节的前内侧稳定结构",
    f"{b('深层')}：纤维致密而强韧，从内踝尖深面斜行止于滑车下方的整个距骨内侧面，以及距骨颈最前部",
]))
A.append(h4("🔻3. 距下关节的韧带"))
A.append(ul([
    f"{b('距跟骨间韧带')}：位于跗骨窦，由垂直和斜行纤维束组成，与脂肪组织交织；斜向排列（与冠状面约 35°），是旋转稳定的{red('“中央枢轴”')}，相当于膝关节的交叉韧带",
    f"{b('颈韧带（前外侧距跟韧带）')}：常为多束，连接距骨颈和跟骨外侧缘，是距下关节{b('第一道前外侧稳定结构')}，外侧与伸肌支持带相连，但常被忽视",
    f"{b('其他')}：距跟内侧、后、外侧韧带（外侧韧带不恒定）",
    f"{b('跟腓韧带')}：常被说成距下关节稳定结构，其实主要维持“距跟单元”的稳定",
]))
A.append(pic(7, "图6：颈韧带——距下关节的前外侧“锁”"))
A.append(pic(8, "图7：副韧带复合体示意。跟腓韧带扭伤不等于距下关节不稳；颈韧带扭伤才意味着距下关节松弛"))

A.append(h3("❇️三、关节运动学"))
A.append(ul([
    f"{b('最稳定的位置')}（紧密嵌合位）：距小腿关节{b('最大背伸')}＋距下关节外翻、跟骨外翻，如下蹲、爬坡；距骨嵌入踝穴，关节面最匹配",
    f"{b('跖屈即潜在不稳')}：行走中一旦到达跖屈，踝关节就处于潜在不稳状态",
    f"{b('双重稳定')}：旋后时，第一道稳定是距下关节的{b('颈韧带')}，动作加大时再加上距跟骨间韧带（外侧纤维）；如果再加上跖屈形成内翻，第二道稳定是{b('距腓前韧带')}。这解释了临床上距小腿关节和距下关节常同时受损",
    f"{b('旋转')}：跖屈时距骨内旋（内收），背伸时外旋（外展）；从跖屈到背伸的自动旋转幅度，文献报道 5°～18° 不等，大部分发生在中立位到背伸之间",
    f"{b('多轴运动')}：现在多数学者认为距骨做的是屈伸滚动＋水平旋转滑动＋冠状面内收外展的复合运动",
    f"{b('下胫腓联合')}：可能不只是适应距骨不对称，更像一个“减震器”，保护外踝免于应力骨折",
]))
A.append(p(b("不同距骨分型对韧带的影响：")))
A.append(table(
    ["分型", "运动特点", "对韧带的影响"],
    [
        ["1 型（最常见）", "不对称滚动，像倒车入库一样“滚＋滑”进入踝穴", "背伸时后部韧带紧张、跖屈时前部紧张，是真正的旋转稳定；跟腓韧带在背伸时与距腓前韧带接近直角，稳定距骨"],
        ["2 型", "旋转应力较小", "距腓前韧带受力"],
        ["3 型", "内旋和旋后成分最小", "对距腓前韧带和颈韧带起保护作用"],
    ],
))
A.append(p(
    f"内侧韧带是踝关节的“锚点”，旋转围绕它进行。此外，{b('腓骨肌和胫骨后肌')}等关节周围肌腱对稳定和负重适应至关重要，"
    f"{u('用它们做肌腱转位修复韧带时必须权衡')}。"
))

A.append(h3("❇️四、损伤机制"))
A.append(table(
    ["机制", "常见情境", "受伤结构"],
    [
        ["内翻（最常见）", "前足外侧缘绊到或落地", "先伤颈韧带和距腓韧带，极端扭转时伤及分歧韧带；可合并腓肠神经、腓浅神经分支或腓骨肌腱牵拉伤"],
        ["内翻＋背伸", "较少见", "跟腓韧带"],
        ["足固定于地面时旋转", "—", "内侧或外侧间室损伤，纤维性撞击、部分距骨穹窿骨软骨损伤，可累及下胫腓联合"],
        ["强力跖屈", "前足被绊住", "内外侧副韧带前部纤维、前关节囊，甚至跗跖关节"],
    ],
))
A.append(p(f"反复扭伤的机制可能各不相同，所以{red('临床和影像检查必须评估踝、中足和后足的全部韧带结构')}。"))

A.append(h3("❇️五、不稳的两大类型"))
A.append(h4("🔻1. 机械性不稳"))
A.append(table(
    ["类型", "要点"],
    [
        ["骨性", "距骨穹窿较宽、覆盖减少、负重侧位片距骨前移；外踝后移（距腓前韧带松弛或断裂、距骨内旋如高弓足、外踝畸形愈合）；外踝高度影响不大；下胫腓分离或外踝外旋畸形愈合是重要因素"],
        ["韧带性", "不只来自损伤，也有先天性松弛（如马凡综合征）；应力位片价值有争议，肌肉收缩可能掩盖松弛；距下关节不稳已被认识但临床难评估，MRI 更精确"],
        ["关节性", "距骨前宽，所以背伸受限本身就是不稳因素：前方骨赘（撞击性外生骨疣）、前方滑膜增生（纤维性撞击）、小腿三头肌或腓肠肌挛缩都会加重不稳；Barouk 发现腓肠肌短缩者 67% 有整体不稳感，25% 有踝不稳"],
    ],
))
A.append(pic(9, "图8：外踝畸形愈合，外旋并伴下胫腓分离", w="55%"))
A.append(h4("🔻2. 功能性不稳"))
A.append(p(f"本体感觉是姿势控制的一部分。踝部有{b('四类感受器')}："))
A.append(ul([
    "肌梭",
    "高尔基腱器（位于肌腱-肌肉交界，调节肌张力、防止肌腱过度牵拉）",
    "Ruffini 关节机械感受器（对速度、方向、幅度敏感，只在极端运动时被激活）",
    "足底皮肤机械感受器（Merkel、Ruffini 对皮肤牵拉敏感，Pacini 对振动敏感）",
]))
A.append(p(f"视觉和前庭系统同样是必不可少的姿势信息来源，检查时也要评估。"))
A.append(quote(
    "None of the neuromuscular responses to ankle varus was fast enough to prevent ligament injury, which occurs in 30 ms.",
    "对踝内翻的任何神经肌肉反应，都快不过韧带损伤发生的 30 毫秒。",
))
A.append(p(
    f"因此真正起保护作用的是{hl('肌肉预激活')}：动态运动中，肌肉在着地前约 {b('100 ms')} 就开始激活。"
    f"Wang 和 Lin 发现，足底感觉下降时慢性不稳会加重，闭眼时更明显；肥胖者本体感觉也会下降。"
))
A.append(p(b("临床怎么评估本体感觉？")))
A.append(ul([
    f"{b('闭眼单腿站立')}：具有体征价值",
    f"{b('单脚反复跳')}：似乎最可靠，可评估腓骨肌、胫骨后肌、小腿三头肌等稳定肌的预激活",
]))
A.append(p(b("功能性肌肉不稳：")))
A.append(ul([
    "肌肉反应延迟：一过性神经问题（如跷二郎腿后的轻瘫），或肌肉本身问题（肌腹过低、腱鞘炎、腓骨肌腱脱位）",
    f"Morrison 和 Kaminski 的步态分析：第一跖趾关节背伸增加、触地时间延长、中前足外侧缘压力增加、旋前旋后指数增加",
]))
A.append(p(b("功能性姿势不稳：")))
A.append(ul([
    f"{red('后足内翻')}是韧带重建失败的原因之一：足外侧缘压力过大、单腿负重时姿势失衡、腓骨肌张力过高（常伴牵张反射丧失），或相反出现反射亢进伴腓骨肌挛缩（如跗骨窦综合征）",
    "合并马蹄足时趾长伸肌收缩不足，或相反屈曲过度导致外侧足趾爪形",
    "第五趾爪形或第四跖骨头下胼胝，也是踝不稳的征象",
    "双下肢不等长（短侧趋于内翻马蹄）、膝内翻、内收足、前足旋前等，也会让足外侧缘受压过大",
]))
A.append(pic(10, "图9：后足内翻（左：右侧踝关节正位片显示内翻；右：后面观）。未矫正后足内翻，腓骨短肌重建失败"))

A.append(h3("❇️六、治疗的基本原则"))
A.append(quote(
    "Not overly 'tighten' ankle ligaments in reconstruction procedures so as to preserve proprioceptive reflexes.",
    "重建手术中不要把踝关节韧带“拉得过紧”，以保留本体感觉反射。",
))
A.append(ul([
    "韧带重建不要过紧，保留本体感觉反射",
    "肌腱转位要不改变距小腿关节和距下关节的生物力学",
    "平衡肌力缺陷",
    "矫正力线，恢复姿势平衡",
]))

A.append(h2("⚖️ 证据评价"))
A.append(ul([
    f"{b('性质')}：叙述性综述，结合文献和 2008 年 Sofcot 专题研讨会的解剖、CT 数据，多数观点为专家意见",
    f"{b('数据前后不一')}：摘要说距骨 1/2/3 型分别为 66%/19%/15%，这是 Bedin-Mabit 的 CT 数据（32 例）；而 Bonnel 的解剖数据为 86%/11%/3%，差别较大，原文未解释原因，样本量也未交代",
    f"{b('术语不统一')}：颈韧带在一处被称为“前外侧距跟韧带”，在讲损伤机制时又写成“距跟外侧韧带”，而图 6 写的是“颈韧带或距跟外侧韧带”，读者需注意区分",
    f"{b('局限')}：作者自己也承认，评估踝不稳的有效检查很少，这也是扭伤复发和部分重建失败的原因",
    f"{b('隐私与版权')}：原图 9 的 X 线片左下角带有患者姓名，本文已抹除；本文为 Elsevier 版权论文（非开放获取），图片仅供学术交流",
]))

A.append(h2("📌 总结：慢性踝不稳要“全面体检”"))
A.append(p(
    f"{red('① 骨')}：距骨是不对称截锥体，前宽后窄；1 型最常见，使距腓前韧带受力<br>"
    f"{red('② 韧带')}：外侧三韧带 ＋ 颈韧带和距跟骨间韧带；跟腓韧带向后倾斜 45°<br>"
    f"{red('③ 运动')}：背伸最稳定，跖屈潜在不稳；旋后时先颈韧带、再距腓前韧带<br>"
    f"{red('④ 机制')}：内翻最常见，内翻＋背伸才伤跟腓韧带<br>"
    f"{red('⑤ 不稳')}：机械性（骨、韧带、背伸受限）＋功能性（本体感觉、肌肉、后足内翻）<br>"
    f"{red('⑥ 治疗')}：重建不过紧、转位不改变力学、平衡肌力、矫正力线"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Bonnel F, Toullec E, Mabit C, Tourné Y, Sofcot. Chronic ankle instability: Biomechanics and pathomechanics of "
    "ligaments injury and associated lesions. Orthop Traumatol Surg Res. 2010;96(4):424-432. doi:10.1016/j.otsr.2010.04.003</em><br>"
    "文中图片均来自原文，图中英文和法文标注已改为中文，图 9 中的患者姓名已抹除，仅用于学术交流。"
))

TITLE = "「踝关节」崴脚为什么会反复？慢性踝不稳的生物力学"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>慢性踝不稳推文</title>
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
