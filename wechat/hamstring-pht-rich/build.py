#!/usr/bin/env python3
"""近端腘绳肌腱病的个体化物理治疗（Rich 2025）推文。

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
A.append(cap("原文首页（IJSPT 2025 年第 20 卷第 6 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Treatment of Proximal Hamstring Tendinopathy with Individualized Physiotherapy: A Clinical Commentary（近端腘绳肌腱病的个体化物理治疗：临床评论）",
    f"{b('作者')}：Aidan Rich · Jillianne Cook · Andrew Hahne · Jon Ford",
    f"{b('机构')}：拉筹伯大学（La Trobe University）联合健康、人类服务与运动学院；Lifecare Malvern 运动医学；Advance Healthcare（澳大利亚）",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2025;20(6):892-910",
    f"{b('PMCID')}：PMC12129629",
    f"{b('文章类型')}：临床评论 / 当前概念综述",
    f"{b('证据级别')}：5 级",
    f"{b('关键词')}：physiotherapy · proximal hamstring tendinopathy · rehabilitation · tendinopathy · shockwave",
], square=True))

A.append(h2("🎯 背景：坐骨结节下方的“坐不住”的痛"))
A.append(p(
    f"{b('近端腘绳肌腱病（PHT）')}既见于运动人群，也见于久坐少动者，表现为{b('臀下部局限性疼痛')}，在久坐（尤其坐硬面）、深蹲、上坡走或跑步时加重。"
    "患病率数据很少，但在运动人群中被认为常见且致残。"
))
A.append(ul([
    f"{b('肌腱病连续体模型')}：急性过载 → {b('反应性')}肌腱病（大分子蛋白聚糖增加、肌腱肿胀，胶原结构完整）；持续慢性过载 → {b('失修/退变性')}肌腱病（胶原和基质紊乱）。负荷过多或过少都可能致病",
    f"肌腱主要承受拉力，但{b('压缩负荷')}也会引起基质改变：PHT 中屈髋角度大的动作（弓步、踢、深蹲、拉伸腘绳肌）和坐姿直接压迫，都会在{b('坐骨结节')}处产生压缩",
    "手术和影像研究显示病变集中在坐骨结节附着处附近，支持“压缩是关键因素”的假说",
    f"最新系统综述：{b('没有足够证据推荐某一种疗法优于另一种')}；冲击波相较 3 周运动有效，但该试验的运动方案与专家推荐不符",
    f"专家最常推荐的是{b('教育 + 运动')}",
]))
A.append(p(
    f"本文介绍作者为 PHT 设计的{hl('教育 + 五阶段个体化运动方案')}，借鉴其他肌腱病临床试验中有效的原则，并结合近端腘绳肌的解剖和生物力学特点。"
    f"该方案正在一项{b('与体外冲击波（ESWT）对比的随机对照试验')}中使用（ACTRN12620001243909）。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["阶段", "目的", "代表训练", "剂量要点", "疼痛上限"],
    [
        ["1 等长", "镇痛、热身、让患者放心", "仰卧腘绳肌臀桥", "5 × 30～45 秒，间歇 90 秒", "第 2 次结束时 ≤4/10"],
        ["2 等张力量", "腘绳肌力量/耐力，肌腱适应", "臀桥、俯卧/站立屈膝", "2～3 × 10～15 → 4～5 × 6～8", "≤4/10"],
        ["3 动力链", "补齐小腿、臀大肌、大收肌等短板", "提踵、臀推、伸膝、弹力带外展", "耐力 2 × 20 → 力量 3 × 6～10", "—"],
        ["4 压缩负荷", "逐步恢复对压缩的耐受", "改良硬拉、弓步、台阶单腿桥", "2 × 4～6 → 3 × 6～8，逐步加大屈髋", "≤4/10"],
        ["5 储能释能", "需要爆发的项目才做", "分腿蹲、专项动作", "1～2 个训练 3 × 8～20", "≤2/10"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('先减少坐压和拉伸，再从等长、等张、动力链练起，最后才逐步把屈髋压缩和爆发动作加回来')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、运动可能通过哪些机制起效"))
A.append(ul([
    "提高腘绳肌自主激活（增强皮质脊髓兴奋性、减少皮质抑制）",
    "改善肌-腱单元刚度、肌腱模量等力学特性；增加基质蛋白合成；与糖胺聚糖和液体动力学相关的神经化学作用",
    "恢复腘绳肌复合体和动力链的负荷能力；改善牵张-缩短循环的协调",
    "增加肌腱横截面积，引起肌腱结构改变",
    "治疗关系（“工作联盟”）、安慰剂效应、自然病程和教育也可能起作用——各机制的贡献大小尚不确定",
]))

A.append(h3("❇️二、标准化教育"))
A.append(p("第 1、2 次就诊时发放标准化信息单（诊断、疼痛监测、压缩管理、高/低肌腱负荷管理），第 6 次（最后一次）再发出院建议，鼓励患者反复阅读。"))
A.append(table(
    ["主题", "要点"],
    [
        ["诊断", "PHT 诊断不易，明确诊断并告诉患者疼痛和功能可能会改善，本身就能让人安心"],
        ["疼痛监测", f"训练中允许一定的肌腱痛，常用上限 {b('<4/10')}；超过时降低重量、负荷、次数和/或屈髋角度，或暂停该训练<br>第一阶段前 2 次允许较高疼痛（等长有镇痛作用）；第五阶段上限更低"],
        ["延迟疼痛", f"训练后 24 小时内可重复任务的疼痛增加 {b('≤2/10')} 可以接受；增加 {b('≥3/10')} 且持续超过 24 小时，则调整训练<br>强调“{b('疼痛≠损伤')}”；12～24 小时的延迟疼痛是判断耐受的最佳指标"],
        ["恐惧回避", "Örebro 肌骨疼痛筛查问卷简版（ÖMPSQ-SF）第 9 题恐惧回避得分 >50 者，更要反复强调“疼痛≠损伤”"],
        ["压缩管理", f"{b('减少坐骨结节处压缩')}：少久坐、少坐硬面，用软垫或分散压力的坐垫；暂时避免拉伸腘绳肌、深蹲、弓步等大角度屈髋动作<br>病变肌腱肿胀、含不耐压的胶原类型，对压缩耐受差；第四阶段再逐步恢复压缩"],
    ],
))

A.append(h3("❇️三、运动方案的关键组成"))
A.append(ul([
    f"{b('分级强化腘绳肌')}：第一阶段等长、第二阶段等张；等长以能全程保持高质量收缩为准，通过减少腿部支撑、改单腿或延长时间进阶；等张随力量提高或疼痛减轻加次数、重量、阻力",
    f"{b('听觉提示')}：用外部节拍（如手机节拍器）提高腘绳肌自主激活，用于直接加载腘绳肌的第一、二、四阶段",
    f"{b('对侧训练')}：除非疼痛或力量不允许，所有阶段都两侧分别练。单侧肌腱病常有双侧运动和感觉缺陷，提示中枢参与；单侧训练也能让对侧变强（“交叉教育”）",
    f"{b('恢复动力链')}：PHT 患者常有{b('臀大肌、小腿三头肌、内收肌')}力量不足，需要强化；各阶段都按需加入腰盆姿势和运动控制",
    f"{b('个体化')}：按患者自己设定的目标（日常活动、运动、职业）安排训练；进阶速度取决于去适应程度、病情严重度、依从性和个体反应；{b('第五阶段只给高储能释能需求者')}",
]))
A.append(pic(2, "图1：各阶段之间的进阶（原图为英文流程图，已按原内容中文重绘）"))

A.append(h3("❇️四、第一阶段：等长收缩"))
A.append(ul([
    "目的：疼痛高时减轻疼痛；作为后续训练的热身；让患者放心——有控制地加载腘绳肌是安全的",
    "所有人从这一阶段开始；功能完全无痛、已在做维持训练时可以停",
    "髌腱病研究中，等长收缩可即时减轻加载痛、提高力量，持续 45 分钟；其他肌腱病结果不一；PHT 中尚未测量（有 RCT 正在进行）",
    f"训练：{b('仰卧腘绳肌臀桥')}（易实施、易调节；有腰痛等限制时可换其他动作）；{b('5 次 × 30～45 秒')}",
    "进阶：双腿 → 单腿、加重量或减少腿部支撑，前提是每次都能高质量保持 45 秒",
    f"{red('腿不能抖')}；强调腰盆侧向和矢状面控制，避免骨盆过度前倾（对 PHT 不利）",
    "前 2 次允许较高疼痛（等长的镇痛效果需要时间）；此后仍 >4/10，就降低负荷或调整腰盆控制提示",
]))
A.append(pic(3, "图2：第一阶段：等长收缩的流程（原图为英文，已中文重绘）"))
A.append(pic(4, "图3：单腿腘绳肌臀桥——第一阶段做等长，第二阶段做等张。起始位（a）；等长保持位（b）；减少腿部支撑的进阶（c、d）（已重新排版）"))

A.append(h3("❇️五、第二阶段：等张力量"))
A.append(ul([
    "目的：提高腘绳肌复合体的能力和运动控制；PHT 常见腘绳肌力量下降和萎缩",
    "其他下肢肌腱病的分级强化训练能改善疼痛、功能障碍和功能",
    f"首选仍是{b('仰卧腘绳肌臀桥')}；开始每周 3 次（或隔天），{b('力量 ≥ 健侧')}后减为每周 2 次——病程长者可能需要 {b('3～6 个月或更久')}",
    "通常在第 1～2 次就诊时，能按本阶段参数完成动作后开始",
    f"重负荷、渐进的力量训练更能促进肌腱的适应性变化：先 {b('2～3 组 × 10～15 次')}（低强度）重视技术，后期减少次数、加大强度，典型为 {b('4～5 组 × 6～8 次')}",
    "强度以“做不了下一组规范动作”为准；训练经验少或疼痛持续较高者要谨慎",
    "可重复任务的疼痛增加 >2/10 并超过 24 小时 → 降低强度",
]))
A.append(pic(5, "图4：第二阶段：等张力量的流程（原图为英文，已中文重绘）"))

A.append(h3("❇️六、第三阶段：动力链"))
A.append(ul([
    "目的：提高动力链的能力、功能和运动控制；小腿三头肌和臀大肌力量下降在 PHT 中常见",
    "动力链关系到功率产生、负荷的吸收与分配、跑姿是否正常。例：踝扭伤后小腿三头肌功能下降的跑者、腰痛后伸髋功能下降的跑者，都可能让腘绳肌承受更多负荷",
    f"所有人都练{b('小腿和伸髋')}；客观测试（如单腿伸膝）发现股四头肌不足时加股四头肌",
    f"腰盆控制：观察下蹲、单腿站、走、跑中有无{b('侧向骨盆控制差')}（Trendelenburg 征、同侧躯干侧屈）或{b('骨盆过度前倾')}（结合腰椎前凸判断），有则用“运动控制”方式训练，只做高质量的重复",
    "一般在第 2～3 次就诊开始；小腿和伸髋从“耐力”剂量（2 组 × 最多 20 次）达到里程碑后进阶到“力量”剂量（3 组 × 6～10 次）；股四头肌直接用力量剂量",
]))
A.append(pic(7, "图5：第三阶段：动力链的流程（原图为英文，已中文重绘）"))
A.append(pic(8, "图6：动力链训练——单腿臀推强化臀大肌和内收肌（a、b）；站立弹力带外展训练腰盆控制（c、d）（已重新排版）"))

A.append(h3("❇️七、第四阶段：压缩负荷"))
A.append(ul([
    "目的：评估并逐步提高腘绳肌腱对压缩的耐受；个体的压缩需求达到后即停止，之后由运动/工作本身提供压缩",
    f"开始条件：第二阶段训练{b('耐受至少 2 周')}；力量明显不足者往往更晚开始",
    f"训练：{b('改良硬拉')}（图8），从接近患者{b('最大功能所需重量')}开始，逐步{b('加大屈髋角度')}和次数；不能硬拉（如腰痛）时可用弓步或抬高的臀桥",
    "按日常目标决定压缩训练的性质和强度：例如澳式足球运动员要从地上捡球，比长跑者需要更大的屈髋和压缩耐受；园艺、体力劳动也要考虑",
    "很多人的最大功能需求重量其实不大（如抱孩子、从低处拿东西）；想恢复硬拉训练的人则需要更大重量",
]))
A.append(pic(9, "图7：第四阶段：压缩负荷的流程（原图为英文，已中文重绘）"))
A.append(pic(10, "图8：压缩训练——改良硬拉（a）、改良深弓步（b）", "70%"))

A.append(h3("❇️八、第五阶段：储能与释能"))
A.append(ul([
    "目的：通过提高肌腱刚度等生物学适应，增强腘绳肌和下肢的储能与释能能力；也用于评估场地类、球拍类运动员能否恢复调整后的训练",
    f"{b('只给有高储能释能需求的人')}；以跑步为主（非场地运动）的运动员，负荷（速度、距离）容易量化、储能需求低，一般跳过此阶段，直接逐步恢复正常跑步训练",
    "开始条件：患侧力量缺陷可忽略，第二、四阶段耐受良好；去适应明显者可能超过 12 周才到这一步",
    "训练：分腿蹲，或按需求定制的专项动作——如模拟网球截击或低位反手的改良弓步，模拟足球中捡球的“腘绳肌铲球”动作",
    f"先试“储能”部分，再加入“释能”；疼痛上限更低：{red('≤2/10')}（负荷更高，更易诱发疼痛加重）",
]))
A.append(pic(11, "图9：第五阶段：储能与释能的流程（原图为英文，已中文重绘）"))

A.append(h3("❇️九、重返跑步和全面功能"))
A.append(ul([
    "跑步（尤其快跑、上坡跑）常诱发 PHT",
    "只有跑步引起高疼痛或症状加重超过 24 小时，才要求完全停跑；否则可只停快跑或上坡跑",
    "减少跑量时可用游泳、骑车、椭圆机等维持有氧能力，同样要监测延迟反应",
    f"完全停跑者首次跑步：在较长步行中跑 {b('2 分钟')}（每次 1 分钟）；耐受后每次增加 {b('1～3 分钟')}；累计跑到 {b('20 分钟')}后，再按目标增加距离或速度",
    f"距离恢复后再小心加入上坡；含强度（快跑或坡跑）的跑步一般{b('每周不超过 2 次')}（精英或高跑量者可 3 次）",
    "尽量量化跑步负荷；观察跑姿：腰盆控制差、胸/躯干过度前屈、落地声音大（步幅过大）、步频（随速度变化）",
    "园艺、深蹲、搬举、踢球等曾诱发疼痛的活动，同样从低量开始，按训练中和训练后的症状逐步增加",
]))
A.append(pic(12, "图10：重返跑步的进阶（原图为英文，已中文重绘）"))

A.append(h3("❇️十、各阶段如何组合"))
A.append(p(
    f"早期按{b('两天一循环')}：第 1 天做规定训练，第 2 天做不诱发症状的训练（其他有氧、上肢力量），必要时加第一阶段。"
    "第四阶段一般在干预 1～2 个月以上后加到第 1 天。需要第五阶段者改为三天一循环。"
    f"达成目标后，建议继续维持训练：从第一～三阶段选 2～3 个动作，{b('每周 2 次')}；避免高负荷活动快速增加和连续高肌腱负荷日，部分人应长期避免某些动作（如全幅度大重量硬拉）。"
))

A.append(tcap("表1　物理治疗各阶段概览"))
A.append(phase_card("第一阶段：等长", "", [
    ("目的", br(["疼痛高时减轻疼痛", "作为等张（或其他）训练前的“热身”", "让患者看到有控制地加载腘绳肌是安全的", "提高腘绳肌自主激活"])),
    ("可选训练", br(["双腿或单腿腘绳肌臀桥", "俯卧屈膝", "站立屈膝"])),
    ("剂量", "5 次 × 30～45 秒（每次之间休息 90 秒）<br>① 镇痛：每天最多 4 次<br>② 作为大训练计划的第一个动作，约每周 3 次"),
    ("目标", "完成训练"),
    ("注意", br(["优先保证高质量收缩（腿不抖、骨盆水平）", "按需继续第一阶段", "第 2 次结束时疼痛 ≤4/10"])),
]))
A.append(phase_card("第二阶段：等张力量", "", [
    ("目的", br(["提高腘绳肌复合体的力量/耐力", "促进受累肌腱的积极力学适应"])),
    ("可选训练", br(["双腿或单腿腘绳肌臀桥", "俯卧屈膝", "站立屈膝"])),
    ("剂量", "2～3 组 × 10～15 次，进阶到 4～5 组 × 6～8 次（向心 2 秒、离心 3 秒，次间休息 1 秒；组间 1 分钟）<br>每周 3 次（或隔天）"),
    ("目标", "力量 ≥ 健侧"),
    ("注意", br(["明显去适应和/或疼痛高时，开始可用高次数、低负荷", "所有重复疼痛 ≤4/10"])),
]))
A.append(phase_card("第三阶段：动力链", "", [
    ("目的", br(["补齐腘绳肌协同肌群的力量不足", "恢复下肢动力链功能"])),
    ("可选训练", br(["小腿：双腿提踵、单腿提踵、负重单腿提踵", "臀大肌和大收肌：双腿臀推、负重双腿臀推、串联臀推、单腿臀推", "髋外侧：站立弹力带外展", "股四头肌：坐位伸膝、上台阶"])),
    ("剂量", "耐力期：2 组 × 最多 20 次（向心 2 秒、离心 2 秒，次间不休息；组间 1 分钟）<br>力量期：3 组 × 6～10 次（向心 2 秒、离心 2 秒，次间 1 秒；组间 2 分钟）<br>每周 3 次（或隔天）<br>*髋外侧用运动控制剂量：最多 60 次，每组 3～10 次，每周 3 次（或隔天）"),
    ("目标", br(["小腿：自重单腿提踵 22～25 次", "臀大肌和大收肌：单腿臀推 3 组 × 10 次", "髋外侧：单腿站立时腰盆控制良好", "股四头肌：力量 ≥ 健侧"])),
    ("注意", br(["运动控制和腰盆控制由治疗师评估，按需给予提示", "髋外侧和股四头肌训练并非所有人都需要"])),
]))
A.append(phase_card("第四阶段：压缩负荷", "", [
    ("目的", "评估腘绳肌腱复合体对压缩负荷的耐受"),
    ("可选训练", br(["逐步加大屈髋的双腿硬拉", "逐步加大屈髋的单腿硬拉", "弓步", "台阶上单腿臀桥"])),
    ("剂量", "2 组 × 4～6 次，进阶到 3 组 × 6～8 次（向心 2 秒、离心 2 秒，次间 1 秒；组间 2 分钟）<br>每周 3 次（或隔天）"),
    ("目标", "在运动/职业所需髋角度下完成 2～3 次训练，症状无明显加重"),
    ("注意", br(["通过加大屈髋角度进阶", "负荷反映运动、职业和/或娱乐需求", "在所需髋角度完成 2～3 次后停止第四阶段"])),
]))
A.append(phase_card("第五阶段：储能与释能", "", [
    ("目的", "提高腘绳肌和下肢的储能与释能能力"),
    ("可选训练", br(["分腿蹲", "专项动作"])),
    ("剂量", "1～2 个训练，3 组 × 8～20 次<br>每周 2～3 天"),
    ("目标", "剂量模拟运动/职业需求，症状无明显加重"),
    ("注意", br(["先试储能部分，后加释能", "本阶段疼痛上限更低：≤2/10"])),
]))

A.append(tcap("表2　各阶段的组合（按日循环）"))
A.append(table(
    ["干预阶段", "第 1 天", "第 2 天", "第 3 天"],
    [
        ["早期（不跑）", "训练：第一/二/三阶段<br>有氧/其他：较少<br>跑步：否", "训练：第一阶段*<br>有氧/其他：较多<br>跑步：否", "不适用"],
        ["早期（跑）", "训练：第一/二/三阶段<br>有氧/其他：较少<br>跑步：否", "训练：第一阶段*<br>有氧/其他：较多†<br>跑步：是", "不适用"],
        ["中期（不跑）", "训练：第一/二/三/四阶段‡<br>有氧/其他：较少<br>跑步：否", "训练：第一阶段*<br>有氧/其他：较多<br>跑步：否", "不适用"],
        ["中期（跑）", "训练：第一/二/三/四阶段‡<br>有氧/其他：较少<br>跑步：否或少量", "训练：第一阶段*<br>有氧/其他：较多<br>跑步：是/较多量或强度", "不适用"],
        ["后期（需要第五阶段）", "训练：第一/二/三/四阶段‡<br>有氧/其他：较少<br>跑步：否", "训练：第一阶段*、第五阶段§<br>有氧/其他：调整后的训练<br>跑步：否或少量", "训练：第一阶段*<br>有氧/其他：少量"],
        ["恢复正常训练/出院**", "训练：第一/二/三阶段<br>有氧/其他：较少<br>跑步：否或少量", "训练：第一阶段*<br>有氧/其他：全量训练（高量）", "训练：第一阶段*<br>有氧/其他：全量训练（低/中量）"],
    ],
))
A.append(small("* 按个体反应和疼痛按需进行；† 含个体耐受范围内的跑步；‡ 功能需求达到后立即停止第四阶段；§ 高储能释能已纳入训练后停止第五阶段；** 第 2、3 天可按日常安排互换，出院时的训练处方因运动需求而异。"))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：5 级临床评论，方案尚未发表疗效数据；正在一项与冲击波对比的 RCT 中使用，结果出来后才能判断效果",
    f"{b('亮点')}：每个阶段都有明确的剂量、疼痛上限、进阶条件和调整办法（7 张流程图），并把“压缩负荷”单独作为一个阶段处理，切中 PHT 的病理特点",
    f"{b('机制多为推测')}：等长镇痛来自髌腱病研究，在 PHT 中尚未测量；动力链强化在 RCT 中尚未研究",
    f"{b('前后数字不一致')}：第四阶段组间休息，表 1 写 2 分钟，图 7 写 1 分钟；小腿目标，表 1 写 22～25 次，图 5 写 25 次；图 1 中第三阶段进入第四阶段写“2 周”，正文写“第二阶段耐受至少 2 周”",
    f"{b('小瑕疵')}：Prerequisites 拼写为 Prerequisties，正文有 demends、voume 等拼写错误",
]))

A.append(h2("📌 总结：近端腘绳肌腱病五阶段康复"))
A.append(p(
    f"{red('① 先教育')}：疼痛 <4/10 可接受，看 24 小时延迟反应；少坐硬面、暂不拉伸腘绳肌<br>"
    f"{red('② 第一阶段')}：仰卧臀桥等长 5 × 30～45 秒，腿不抖、骨盆稳<br>"
    f"{red('③ 第二阶段')}：臀桥等张 2～3 × 10～15 → 4～5 × 6～8，直到力量 ≥ 健侧<br>"
    f"{red('④ 第三阶段')}：提踵、臀推、按需股四头肌和髋外侧，补齐动力链<br>"
    f"{red('⑤ 第四阶段')}：改良硬拉逐步加大屈髋，恢复压缩耐受，达到需求即停<br>"
    f"{red('⑥ 第五阶段与跑步')}：有爆发需求才做，疼痛 ≤2/10；跑步从 2 分钟开始，累计 20 分钟后再加距离和速度"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Rich A, Cook J, Hahne A, Ford J. Treatment of Proximal Hamstring Tendinopathy with Individualized Physiotherapy: A Clinical Commentary. "
    "Int J Sports Phys Ther. 2025;20(6):892-910. PMCID: PMC12129629.</em><br>"
    "文中图片均来自原文：图 1、2、4、5、7、9、10 英文流程图已按原内容中文重绘，图 3、6、8 照片已重新排版；表 1～2 已译为中文，仅用于学术交流。"
))

TITLE = "「腘绳肌」坐久了屁股下面痛？近端腘绳肌腱病的五阶段康复"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>近端腘绳肌腱病康复推文</title>
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
