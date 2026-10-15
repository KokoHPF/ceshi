#!/usr/bin/env python3
"""运动性耻骨痛及康复（Ellsworth 2014）推文。

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


def br(items):
    return "<br>".join(f"• {x}" for x in items)


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2014 年第 9 卷第 6 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Athletic Pubalgia and Associated Rehabilitation（运动性耻骨痛及其康复）",
    f"{b('作者')}：Abigail A. Ellsworth, PT, DPT · Mark P. Zoland, MD · Timothy F. Tyler, MSPT, ATC",
    f"{b('机构')}：威彻斯特普拉提治疗与健康中心 · 纽约普通与腹腔镜外科 · Lenox Hill 医院 NISMAT 运动医学研究所",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2014;9(6):774-784",
    f"{b('PMCID')}：PMC4223287",
    f"{b('文章类型')}：特邀临床评论（Invited Clinical Commentary）",
    f"{b('证据级别')}：5 级",
    f"{b('关键词')}：Adductor strain · athletic pubalgia · groin pain · rehabilitation · sports hernia · transversus abdominis",
], square=True))

A.append(h2("🎯 背景：“运动疝”其实不是疝"))
A.append(p(
    f"运动员腹股沟痛的评估和治疗很难：解剖复杂、多种病变常同时存在、不同病变症状相似，而且很多系统都能把疼痛牵涉到腹股沟。"
    f"康复师拿到的转诊单常常只写着“腹股沟痛”或“{b('运动疝')}”。"
))
A.append(p(f"“运动疝”这个词正在被淘汰，原因有二：{red('① 腹壁上并没有真正的缺损，不是疝；② 也不只发生在运动员身上')}。借助 MRI，它被拆分为两类："))
A.append(table(
    ["名称", "定义"],
    [
        ["腹股沟区损伤（inguinal disruption）", "腹股沟管周围软组织损伤引起的疼痛综合征；涵盖运动疝、早期疝、Gilmore 腹股沟、运动员腹股沟等说法"],
        ["运动性耻骨痛（athletic pubalgia）", "更内侧的腹直肌-内收肌共同腱膜从耻骨上撕脱/分离，通常伴有一定程度的内收肌腱病变"],
    ],
))
A.append(p(
    f"英国疝学会 2014 年立场声明（曼彻斯特共识）指出，耻骨联合 MRI 常见两类表现：{b('骨髓水肿')}，以及{b('耻骨联合关节囊和内收肌改变')}（累及前关节囊、关节囊韧带，以及长收肌与腹直肌共同腱膜的附着点）。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["内容", "要点"],
    [
        ["受伤机制", "高速下踩地转体、急停变向、反复踢球、侧向移动；耻骨联合在大腿强力外展/内收时反复承受扭矩"],
        ["典型症状", "运动时“深部”腹股沟或下腹痛，比内收肌或髂腰肌拉伤更深、更剧烈，多为单侧"],
        ["保守治疗", "首选，4 个阶段约 6～8 周；约 6 个月无效视为慢性，可考虑手术"],
        ["术后康复", "术后通常先休息约 4 周，按软组织愈合规律分阶段推进，8～12 周回归运动"],
        ["关键", "腹横肌的正确募集和时序，形成包绕脊柱的“圆柱”"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('先分清是哪种损伤，再按阶段重建核心与髋部的控制')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、鉴别诊断"))
A.append(p("需要通过详细的病史和查体，与以下情况鉴别："))
A.append(ul([
    "腹股沟（内收肌）拉伤、耻骨炎、真性疝",
    "髋关节骨关节炎",
    "直肠或睾丸的牵涉痛、梨状肌综合征",
    "骨盆或下肢合并骨折",
]))
A.append(p(
    f"诊断主要靠病史和查体，再用 MRI 确认。专门的 MRI 方案可评估腱膜板撕裂程度和内收肌腱病变；"
    f"做 / 不做 Valsalva 动作的序列可以评估腹横筋膜是否变薄（Gilmore 描述的腹股沟区损伤表现之一）。"
))
A.append(p(
    f"{b('常见体征')}：耻骨结节压痛、盆底及周围肌群无力；{b('抗阻仰卧起坐')}时症状加重（腹部向外鼓）；内收肌和屈髋肌在动态动作中无力；步态观察可见骨盆运动和下肢力线异常。"
))
A.append(tcap("表 1　提示运动性耻骨痛的 5 个体征（Kachingwe 等）"))
A.append(table(
    ["序号", "体征"],
    [
        ["1", "主诉腹股沟深部 / 下腹部疼痛"],
        ["2", "冲刺、切步、仰卧起坐等用力时加重，休息后缓解"],
        ["3", "耻骨支上、腹直肌和/或联合腱附着处可触及压痛"],
        ["4", "屈髋 0°、45° 和/或 90° 位抗阻内收时疼痛"],
        ["5", "抗阻卷腹时疼痛"],
    ],
))

A.append(h3("❇️二、保守治疗"))
A.append(p(
    f"保守治疗是首选：休息、避免诱发运动、针对性康复，必要时配合耻骨联合或内收肌起点激素注射、抗炎药。"
    f"支持保守治疗的证据不多，但多数研究显示 {b('6～8 周物理治疗')}后明显改善。"
))
A.append(p(
    f"康复重点：评估核心稳定、髋部力量和柔韧性，找出代偿和失衡；训练功能动作中的{b('激活时序和募集模式')}；用手法处理软组织和筋膜受限；"
    f"全面加强髋内收肌、屈肌、内旋肌、伸肌、核心稳定肌和腰盆肌群。"
))
A.append(tcap("表 2　运动性耻骨痛的保守治疗方案"))
A.append(phase_card("第一阶段", "1～2 周", [
    ("重点", ["控制疼痛和水肿",
             "坐、站、仰卧姿势和脊柱中立位的宣教",
             "腹横肌募集",
             "髋和腰椎松动（Ⅰ、Ⅱ 级）增加活动度",
             "轻柔主动拉伸腘绳肌、内收肌、股四头肌、髂腰肌和腰椎",
             "几乎不加负荷地强化腹横肌，侧卧髋外展和后伸"]),
]))
A.append(phase_card("第二阶段", "2～4 周", [
    ("重点", ["功率车或椭圆机热身",
             "步态训练：足跟着地、站立中期、蹬离时的骨盆运动与时序",
             "继续腹横肌募集和强化",
             "腰椎达到全范围/功能活动度，增加髋活动度",
             "开始静态核心强化，能保持脊柱中立",
             "加强髋和骨盆稳定的募集，重点臀肌、腹横肌、多裂肌",
             "功能强化从双腿开始，疼痛和力量改善后进阶到单腿",
             "脊柱和髋松动加入旋转（Ⅱ、Ⅲ 级）"]),
    ("进阶标准", ["日常活动疼痛 <2/10",
                 "腰椎和髋达到全功能活动度",
                 "站立和单腿活动时能募集并保持腹横肌收缩",
                 "行走无痛",
                 "行走和单腿活动时躯干无侧倾（无 Trendelenburg）"]),
]))
A.append(phase_card("第三阶段", "4～6 周", [
    ("重点", ["功率车或椭圆机更高速度和阻力热身，跑步机快走",
             "行走时骨盆稳定良好，能轻松募集腹横肌",
             "继续步态训练和骨盆 PNF 模式，建立良好运动模式",
             "腰盆和髋达到全/功能活动度，消除残余受限",
             "动态核心训练：活动中保持脊柱中立，加入不稳定平面",
             "站立稳定训练加阻力或平衡干扰，从双腿到单腿功能活动",
             "继续主动拉伸；肌筋膜放松和软组织处理"]),
    ("进阶标准", ["日常活动、行走和快走均无痛",
                 "髋、骨盆和腰椎全功能活动度",
                 "站、坐、走及单腿活动（加不稳定平面或扰动）时能保持脊柱中立",
                 "能察觉并纠正姿势异常"]),
]))
A.append(phase_card("第四阶段", "6～8 周", [
    ("重点", ["热身改为运动/娱乐项目专项",
             "活动度从功能范围进阶到全范围",
             "主动拉伸与静态拉伸交替",
             "以功能性、等张、等长和等速方式做向心和离心强化",
             "手法肌筋膜放松和软组织松动处理残余受限",
             "下肢及上下肢组合的 PNF 模式训练"]),
]))
small("原文第三阶段末尾写的是“未达到以下标准不要进入第三阶段”，按上下文应为“第四阶段”。")
A.append(tcap("表 3　保守治疗早期的核心与本体感觉练习示例"))
A.append(table(
    ["类别", "练习（均从双腿进阶到单腿）"],
    [
        ["初级下腹 / 核心", br(["呼气到底时做骨盆后倾", "骨盆后倾 + 呼气 + 桥式", "前桥和侧桥，配合呼气、保持骨盆中立"])],
        ["本体感觉", br(["在不稳定平面上保持骨盆中立", "在不稳定平面上抛接球", "在不稳定平面上使用 BodyBlade® 震颤棒"])],
    ],
))

A.append(h3("❇️三、术后康复"))
A.append(p(
    f"术后康复与保守治疗的阶段相似，但必须{red('遵循软组织愈合规律，不能过早给修复处过大应力')}。"
    f"不同外科医生的方案各有不同，但有共同原则。术后通常先休息约 4 周，3～4 周后才正式开始物理治疗；避免过度的躯干后伸和旋转；此时{u('禁止卷腹和仰卧起坐')}。"
))
A.append(tcap("表 4　术后康复方案"))
A.append(phase_card("第 1 周", "", [
    ("内容", ["只做日常活动",
             "不提重物，不做任何增加腹压的活动",
             "术后第二天开始在平地行走",
             "前 24～48 小时每 2 小时冰敷 15 分钟",
             "伤口护理"]),
]))
A.append(phase_card("第 2～3 周", "", [
    ("内容", ["触诊和视觉模拟评分（VAS）评估",
             "切口愈合允许时开始水中轻阻力练习",
             "站立闭链下肢和髋练习：提踵；站立髋内收、外展、屈、伸",
             "开始局部激活腹横肌、多裂肌、髂腰肌和髋深层旋转肌",
             "内收肌肌腹深层按摩",
             "胸腰椎手法，维持/改善活动度",
             "轻柔拉伸：躯干侧屈、髋后伸、腰大肌、腘绳肌、股四头肌",
             "倒走"]),
]))
A.append(phase_card("第 4 周", "", [
    ("内容", ["复评 VAS 监测进展",
             "双侧本体感觉和平衡练习，开始单侧",
             "在监控疼痛和负荷下做核心激活抗阻",
             "髋旋转肌、臀大肌、臀中肌稳定练习",
             "开始腹部瘢痕松动，以及周围组织的深层按摩和放松",
             "轻柔拉伸，逐渐加入轻中度阻力的主动拉伸",
             "手法改善髋、腰盆交界和脊柱活动度"]),
]))
A.append(phase_card("第 5～6 周", "", [
    ("内容", ["复评 VAS 监测进展和疼痛耐受",
             "单侧和双侧平衡与本体感觉练习",
             "开始内收肌渐进抗阻（监测疼痛）：等长收缩、屈膝外倒、弹力带抗阻侧步",
             "矢状面和水平面腹部进阶：90/90 脚跟下放、坐位等长保持、跪姿平板、标准平板、骨盆在髋上/躯干在骨盆上的整合功能练习、卷腹"]),
]))
A.append(phase_card("第 6～8 周", "", [
    ("内容", ["心肺训练 20～30 分钟，含热身和放松",
             "髋和下肢加负重强化",
             "前后慢跑、跳绳、短距离冲刺",
             "灵敏和协调训练；交叉步、跨步",
             "弹力带内收方向的单腿离心下放",
             "全身挑战的核心稳定；增强式训练",
             "动态骨盆稳定，髋外侧和臀肌强化"]),
]))
A.append(p(
    f"最后阶段一般按 {b('8～12 周回归运动')}计划，视手术范围和耐受情况可能更久：平衡和本体感觉进阶到专项水平，加入扰动和不平地面；"
    f"加强动态功能性向心和离心训练；第 8～12 周末加入上下肢结合的初级增强式训练。"
))
A.append(p(
    f"{b('合并伤')}：腹股沟痛常有多种病因同时存在。Larson 等发现，运动疝修补与髋关节镜手术同时进行，成功率明显高于只处理其中一种。"
))

A.append(h3("❇️四、训练图解"))
A.append(pic(2, "图1：骨盆后倾。A 仰卧放松，双手放在两侧髂前上棘，指尖轻压其内侧软组织；B 把耻骨联合向肚脐方向拉，指尖应感到两侧腹横肌对称收缩，肋骨下沉，腰椎轻松压平"))
A.append(pic(3, "图2：髋部与核心稳定练习。A 坐在球上，髋膝 90°，手放在髋或大腿上；B 双膝双脚并拢于中线，抬起一侧膝，同时保持骨盆和躯干稳定；能稳定后，对侧手压在抬起的膝上、另一手上举，进一步增加挑战"))
A.append(pic(4, "图3：桥式加抬腿。A 双脚踩地做桥式；B 双腿放在瑞士球上，向下压球、伸膝，让骨盆抬起；C 能在球上做桥后，一腿伸直抬起，保持躯干稳定", w="58%"))
A.append(pic(5, "图4：不稳定平面上的骨盆稳定进阶。A 坐在充气平衡垫上，双膝双脚并拢，双脚着地找到骨盆稳定；B 双臂前伸保持中线，抬起一侧膝"))
small("原文图 4 图注还描述了 C（双脚离地长时间保持平衡）和 D（再加抛接球），但原文只提供了 A、B 两张照片。")
A.append(pic(6, "图5：双腿与单腿平衡及本体感觉训练。A 站在 360° 平衡板上，屈髋屈膝保持平衡；B 掌握双腿后进阶到单腿；C 单腿稳定后加入抛接球"))
A.append(img(7))
A.append(cap("图6（左）：靠墙深蹲加骨盆稳定，球放在下背后，蹲到屈髋 90°，保持躯干骨盆不动再抬起一侧膝；图7（右）：侧桥，肩、肘、髋、踝对齐撑起"))
A.append(img(8))
A.append(cap("图8（左）：前桥进阶。A 前臂支撑，保持骨盆对齐；B 双手撑地，手在肩正下方；C 双手撑在 BOSU 球上保持平板<br>图9（右）：四点跪训练。A 膝在髋下、手在肩下，一腿伸出时保持骨盆对齐；B 伸出一腿和对侧手臂，保持骨盆和肩带对齐"))

A.append(h2("⚖️ 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：5 级临床评论，保守和术后方案都基于作者经验和既往文献，作者也承认可参考的康复研究很少",
    f"{b('图文不符')}：图 2 图注描述了 A、B、C 三步，原文只给了 A、B 两张照片，且 A 照片显示的是图注中 C 的手臂上举动作；图 4 图注描述 A～D，原文只有 A、B 两张",
    f"{b('笔误')}：表 2 第三阶段末写的是“不要进入第三阶段”，应为第四阶段；“Trendelenberg”应为 Trendelenburg",
    f"{b('术语仍未统一')}：作者也承认“腹股沟区损伤”和“运动性耻骨痛”的划分尚无普遍共识",
    f"{b('优点')}：同时给出保守和术后两套分阶段方案，进阶标准明确，配图清楚",
]))

A.append(h2("📌 总结：腹股沟痛，核心和髋要一起练"))
A.append(p(
    f"{red('① 概念')}：“运动疝”不是疝，分为腹股沟区损伤和运动性耻骨痛<br>"
    f"{red('② 诊断')}：深部单侧腹股沟痛、耻骨压痛、抗阻内收/卷腹痛，MRI 确认<br>"
    f"{red('③ 保守')}：四阶段 6～8 周，先控痛和腹横肌，再到单腿、不稳定平面和专项<br>"
    f"{red('④ 时限')}：约 6 个月保守无效视为慢性，可考虑手术<br>"
    f"{red('⑤ 术后')}：第 1 周只日常活动，2～3 周局部激活，5～6 周内收肌抗阻，8～12 周回归<br>"
    f"{red('⑥ 关键')}：腹横肌延迟激活与长期腹股沟痛相关，正确募集和时序是康复核心"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Ellsworth AA, Zoland MP, Tyler TF. Athletic Pubalgia and Associated Rehabilitation. "
    "Int J Sports Phys Ther. 2014;9(6):774-784. PMCID: PMC4223287.</em><br>"
    "文中图片均来自原文（图中仅有 A/B/C 字母），表 1～4 已译为中文，仅用于学术交流。"
))

TITLE = "「腹股沟」“运动疝”不是疝：运动性耻骨痛的保守与术后康复"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>运动性耻骨痛推文</title>
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
