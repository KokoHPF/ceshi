#!/usr/bin/env python3
"""Sinha 等 2024 JPOSNA 青少年及青年髋痛的临床评估推文

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
    "Sinha R, Ellis HB, Podeszwa DA, Sucato DJ, Morris WZ. Clinical evaluation of the painful adolescent and young adult hip. J Pediatr Soc North Am. 2024;7:100043. doi:10.1016/j.jposna.2024.100043",
    "中文题目：青少年及青年髋痛的临床评估",
    "作者来自美国得克萨斯州达拉斯 Scottish Rite for Children 和得克萨斯大学西南医学中心",
    "文章类型：最新概念综述（Current Concept Review），与同期一篇影像学评估综述配套",
], square=True))

A.append(h2("研究背景：年轻人髋痛，先分清撞击还是不稳"))
A.append(ul([
    f"青少年和青年髋痛中，可能导致髋关节{b('早期退变')}的两大原因是{b('髋臼发育不良（不稳）')}和{b('股骨髋臼撞击（FAI）')}",
    "其他常见原因还有肌肉拉伤、肌腱炎、弹响髋、股骨头骨骺滑脱（SCFE）、Perthes 病、骨突炎和骨突撕脱骨折",
    f"影像之前，{b('问诊和查体')}是第一步，决定后续检查和保髋方向",
    f"{b('综述目的')}：把问诊、查体和针对病因的特殊检查整合成一套完整的评估流程",
]))

A.append(h2("方法"))
A.append(ul([
    f"这是一篇{b('叙述性综述')}，没有检索策略、纳入标准或证据分级，作者根据文献和临床经验整理",
    "按问诊 → 视诊与步态 → 触诊 → 关节活动度 → 肌力 → 特殊检查的顺序展开，并用 10 幅照片演示",
    "特殊检查分三组：撞击和盂唇病变（表 1）、不稳或关节囊功能不全（表 2）、弹响髋；部分检查给出了文献报道的敏感度、特异度和信度",
]))

A.append(h2("结果"))
A.append(h3("一、问诊"))
A.append(pic(2, "编者根据原文整理"))
A.append(ul([
    f"问清{b('部位、性质、起病方式和病程')}；病程长短能先缩小鉴别范围",
    f"足外展角逐渐变大、轻度跛行后突然剧痛不能行走，{b('高度怀疑 SCFE')}",
    f"大转子近端的外侧痛多是{b('外展肌疲劳')}，髋臼发育不良的生物力学劣势会加重这种疲劳",
]))
A.append(h3("二、视诊、触诊、活动度和肌力"))
A.append(pic(3, "原文图 1（照片为原图，图注编者译成中文）"))
A.append(pic(4, "编者根据原文整理"))
A.append(ul([
    f"{b('Trendelenburg 步态')}：外展肌不足以维持骨盆水平，对侧骨盆下掉，或躯干倒向支撑侧来减小外展肌需要的力，常见于髋臼发育不良",
    f"{b('正常活动度')}（青少年和青年）：屈曲约 {b('120°')}，内旋 {b('30°～40°')}，外旋 {b('40°～50°')}，后伸 {b('5°～10°')}；后伸最好侧卧、屈膝 90° 测",
    f"{b('内旋受限')}提示 FAI 或 SCFE；FAI 患者内旋 {b('< 10°')} 与影像上骨关节炎进展有关",
    f"{b('强制性外旋')}：屈髋时髋自动倒向外旋，警惕 SCFE，需拍骨盆正位和蛙式侧位",
    f"内旋或外旋 {b('> 60°')}：提示关节囊松弛和/或不稳",
    f"{b('直腿抬高')}出现皮节分布的放射痛，提示脊柱病变，尤其是椎间盘突出",
    f"{b('Stinchfield 试验')}（仰卧抗阻直腿抬高）疼痛：提示骨突炎、髂腰肌拉伤或关节内病变",
]))
A.append(pic(5, "原文图 2、5（照片为原图，图注编者译成中文）"))
A.append(pic(6, "原文图 3（照片为原图，图注编者译成中文）"))
A.append(pic(7, "原文图 4（照片为原图，图注编者译成中文）"))

A.append(h3("三、撞击和盂唇病变的特殊检查"))
A.append(ul([
    f"{b('FADIR')}：仰卧或侧卧，被动屈曲、内收、内旋，再现髋痛为阳性，提示前方/前外侧撞击；屈髋 90° 时敏感度 51%～100%，特异度 89%，观察者间一致性 96%",
    f"{b('IROP')}：FADIR 加轴向压力，提示前方撞击，敏感度 75%～89%；对关节内病变的阳性预测值高于 Stinchfield、Scour 和 FABER",
    f"{b('Scour 试验')}：轴向加压，从屈曲内旋位移到外展后伸位，撞击多在髋臼缘 10 点到 3 点之间，敏感度 50%～100%",
    f"{b('FABER')}：屈曲、外展、外旋并下压膝；同侧前方腹股沟痛提示 FAI 和/或盂唇病变，对侧后方痛提示骶髂关节；敏感度 41%～97%，特异度 18%～100%，观察者间信度 98%",
    f"{b('后方撞击试验')}：仰卧在床尾、腿自然下垂，患髋后伸、外展、外旋，再现后方痛为阳性；敏感度只有 {b('21%')}",
]))

A.append(h3("四、不稳或关节囊功能不全的特殊检查"))
A.append(ul([
    f"{b('前方恐惧试验')}：腿垂在床边，对侧髋屈曲，患髋被动后伸加外旋，出现前方腹股沟痛或恐惧感为阳性；敏感度 71%，特异度 89%",
    f"{b('俯卧恐惧复位试验（PART）')}：俯卧，患髋后伸 10°～15°、外展 10°，在臀横纹远端向前推股骨诱发前方痛、松手后缓解为阳性；提示髋臼前方覆盖不足，与 LCEA、FEAR 指数、前壁指数和外侧眉弓上斜等影像不稳指标相关，评估者内和评估者间信度都很好，敏感度和特异度还需研究",
    f"{b('外展-后伸-外旋试验')}：侧卧，患髋外展 30°、后伸再外旋，前方腹股沟痛或恐惧感提示前方不稳；敏感度 81%，特异度 89%",
    f"{b('俯卧外旋试验')}：俯卧屈膝 90°，腿越过中线使髋外旋，在大转子后方向前加压；敏感度只有 33%，但特异度 {b('98%')}",
    f"{b('Dial 试验')}：仰卧伸髋伸膝，把足被动内旋到底后松手，回弹后的外旋大于健侧，或足与床面夹角 < 20° 为阳性，提示前方关节囊不稳",
    f"{b('后方恐惧试验')}：屈髋 90°、内收内旋，向后推膝，再现后方痛或恐惧感提示后方不稳",
]))
A.append(pic(8, "原文图 6、8（照片为原图，图注编者译成中文）"))
A.append(pic(9, "原文图 7（照片为原图，图注编者译成中文）"))

A.append(h3("五、弹响髋"))
A.append(ul([
    f"{b('内源性')}：从 FABER 位移到后伸、内收、内旋位（EADIR），再现常可听见的弹响，是髂腰肌腱滑过髂耻隆起",
    f"{b('外源性')}：侧卧主动屈髋，再被动后伸、外展，看得见的弹响是髂胫束滑过大转子；也可站立内收位做环转（“呼啦圈”试验）",
    f"{b('Ober 试验')}：侧卧，髋被动后伸外展、托住膝，再让腿靠重力缓慢内收，内收受限提示髂胫束紧张，常与外源性弹响髋并存",
]))
A.append(pic(10, "原文图 9（照片为原图，图注编者译成中文）"))
A.append(pic(11, "原文图 10（照片为原图，图注编者译成中文）"))
A.append(pic(12, "编者根据原文正文整理"))

A.append(h2("作者怎么解读"))
A.append(ul([
    "详细的问诊和查体仍是首诊评估的“金标准”，能准确找到疼痛来源、加快决策",
    f"特殊检查的描述、操作方法和信度在文献中{b('差异很大')}，必须结合症状和影像来诊断，不能单靠某一个试验",
    f"四个关键概念：机械性症状提示有结构问题但分不出病因；Trendelenburg 步态常见于髋臼发育不良；{b('屈髋强制性外旋要拍片排除 SCFE')}；PART 阳性与影像上的不稳指标相关",
]))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{b('定位是教学性综述')}：结构清楚、照片直观，适合当查体清单，但没有系统检索，也没有对证据质量分级",
    f"{b('准确度数字来源杂')}：敏感度和特异度来自不同研究、不同人群和不同参考标准，很多是成人 FAI 或关节镜人群，不一定适用于青少年",
    f"{b('范围太宽的数字信息量有限')}：FADIR 敏感度 51%～100%、FABER 特异度 18%～100%，说明结论高度依赖研究和操作方法",
    f"{b('不稳检查的证据更少')}：PART 只有信度和影像相关性的数据；Dial、后方恐惧和轴向牵拉试验没有给出准确度",
    f"{b('作者都是小儿骨科医生')}：视角偏向结构性病变和保髋手术，对肌肉、肌腱、腰骶和运动链因素着墨较少",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('表 2 多出一个试验')}：轴向牵拉试验（Axial Distraction Test，屈髋屈膝 30° 加轴向牵拉）只出现在表 2，正文没有介绍",
    f"{b('FABER 的定位前后不一')}：正文说同侧前方痛提示 FAI 和/或盂唇病变，但表 1 的“撞击部位”只写了大转子与髂胫束、大转子与坐骨之间的后外侧撞击",
    f"{b('外展-后伸-外旋试验没有出处')}：正文给出敏感度 81%、特异度 89%，但这一句没有标注参考文献",
    f"{b('后方撞击试验的出处')}：敏感度 21% 引自文献 6，而文献 6 是关于症状性前方撞击临床表现的研究（编者根据参考文献标题推断）",
    f"{b('FADIR 的敏感度与特异度不对称')}：敏感度给的是 51%～100% 的范围，特异度只给了一个 89%，没有说明来自哪项研究",
    f"{b('排版和拼写')}：原文有“grater trochanter”“coxa salta interna”“condition-sepcific”“positivetest”等拼写错误，不影响内容",
]))

A.append(h2("落到临床"))
A.append(pic(13, "编者整理"))
A.append(ul([
    f"{mk('先排除不能漏的')}：青少年跛行伴膝或大腿痛、足外展角变大、屈髋强制性外旋，先拍骨盆正位加蛙式位排除 SCFE；骨突压痛加急性起病，想到撕脱骨折",
    f"{b('用问诊定方向')}：前方腹股沟或 C 字形疼痛查关节内，外侧痛查外展肌和大转子，骨突痛查骨突，弹响分清看得见（髂胫束）还是听得见（髂腰肌）",
    f"{b('撞击和不稳要成组看')}：内旋受限加 FADIR/IROP 阳性偏向 FAI；外侧痛、Trendelenburg 步态、PART/前方恐惧阳性、旋转 > 60° 偏向不稳",
    f"{b('高敏感度的试验用来排除，高特异度的用来确认')}：例如俯卧外旋试验敏感度低但特异度 98%，阳性更有价值",
    f"{b('康复师的角色')}：查体发现结构性问题（SCFE、明显发育不良或撞击）要转骨科和影像；外展肌无力、髂胫束紧张、髂腰肌问题可同时纳入康复评估",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　股骨髋臼撞击（FAI）的查体手法"))
A.append(table(["体位", "手法", "操作", "撞击部位"], [
    ["仰卧或侧卧", "屈曲-内收-内旋（FADIR）", "患髋屈曲、内旋、内收", "髋臼前缘/前外侧缘与股骨头颈交界处"],
    ["仰卧", "内旋加压（IROP）", "FADIR 加轴向压力", "髋臼前缘与股骨头颈交界处"],
    ["仰卧", "Scour 试验", "轴向加压，髋从屈曲内旋位移到外展后伸位", "髋臼缘 10 点到 3 点之间与股骨头颈交界处"],
    ["仰卧", "屈曲-外展-外旋（FABER）", "髋屈曲、外展、外旋，并向下压膝", "大转子与髂胫束之间的后外侧撞击；大转子与坐骨之间的深部后外侧撞击"],
    ["仰卧", "后方撞击试验", "躺在床尾、双腿自然下垂，患髋后伸、外展、外旋", "髋臼后缘与股骨头颈交界处"],
]))
A.append(tcap("表 2　不稳的查体手法"))
A.append(table(["体位", "手法", "操作", "阳性表现", "诊断"], [
    ["仰卧", "前方恐惧试验", "下肢垂在床边，髋后伸并外旋", "前方腹股沟痛或恐惧感", "前方不稳"],
    ["俯卧", "俯卧恐惧复位试验（PART）", "髋后伸 10°～15°、外展 10°，向前推股骨", "向前推股骨时出现前方髋痛，松开压力后缓解", "前方不稳"],
    ["侧卧", "外展-后伸-外旋试验", "患髋外展 30°、后伸，再外旋", "前方腹股沟痛或恐惧感", "前方不稳"],
    ["俯卧", "俯卧外旋试验", "腿越过中线使髋外旋，在大转子后方向前加压", "前方腹股沟痛或恐惧感", "前方不稳"],
    ["仰卧", "Dial 试验", "足被动内旋到最大后松开，让其自行回到外旋位", "足静止时外旋大于对侧，或足与床面夹角 < 20°", "前方不稳"],
    ["仰卧", "轴向牵拉试验", "髋、膝屈曲 30°，施加轴向牵拉力", "疼痛或恐惧感", "不稳"],
    ["仰卧", "后方恐惧试验", "髋屈曲 90°、内收、内旋，向膝施加向后的力", "后方髋痛或恐惧感", "后方不稳"],
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Sinha R, Ellis HB, Podeszwa DA, Sucato DJ, Morris WZ. Clinical evaluation of the painful adolescent and young adult hip. J Pediatr Soc North Am. 2024;7:100043. doi:10.1016/j.jposna.2024.100043</em><br>"
    "本文为中文解读，仅作学术交流：照片引自原文图 1～图 10（照片内无英文，图注由编者译成中文），问诊卡、查体流程卡、特殊检查准确度图和临床卡为编者根据原文整理，表格为编者翻译。原文 © 2024 The Authors，由 Elsevier 代表北美小儿骨科学会出版，采用 CC BY-NC 4.0 许可。"
))

TITLE = "「髋关节」青少年和年轻人髋痛怎么查？从问诊到 FADIR、PART 的完整查体流程"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>青少年及青年髋痛临床评估</title>
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
