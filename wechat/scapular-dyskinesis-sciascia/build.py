#!/usr/bin/env python3
"""肩胛运动障碍的现代观点（Sciascia & Kibler 2022）推文。

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


def narrow(n, w):
    return img(n).replace("width:100%;max-width:100%;", f"width:{w};max-width:{w};")


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2022 年第 17 卷第 2 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Current Views of Scapular Dyskinesis and its Possible Clinical Relevance（肩胛运动障碍的现代观点及其可能的临床意义）",
    f"{b('作者')}：Aaron Sciascia, PhD, ATC · W. Ben Kibler, MD",
    f"{b('机构')}：Lexington Clinic 临床结局研究所 · 肯塔基肩关节中心",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2022;17(2):117-130",
    f"{b('PMCID')}：PMC8805107",
    f"{b('文章类型')}：临床观点（Clinical Viewpoint）",
    f"{b('证据级别')}：原文未标注（属于专家观点）",
    f"{b('关键词')}：scapular dyskinesis · shoulder · shoulder rehab",
], square=True))

A.append(h2("🎯 背景：常见，却常被误解"))
A.append(quote(
    "Too often it is viewed as a diagnosis which is not accurate because it is a physical impairment.",
    "肩胛运动障碍经常被当作一种诊断，这并不准确，因为它是一种身体功能损害。",
))
A.append(p(
    f"正因为这种错误归类，文献里对肩胛运动障碍的临床意义{u('既有支持也有反对')}，至今没有清晰的评估和治疗建议。"
    f"作者认为原因主要有三："
))
A.append(ul([
    f"{b('自由度多')}：附着在肩胛骨上的肌肉很多，同一个动作不同人的完成方式差异很大",
    f"{b('胸廓是椭圆形的')}：肩胛骨不可能只在单一平面运动，而是旋转和平移的复合运动",
    f"{b('角色多')}：肩胛骨是盂肱关节“凹-压”稳定的“G”、肩锁关节稳定的“A”、肩肱节律的“S”，还是动力链中把躯干和下肢能量传到手臂的关键一环",
]))
A.append(p(
    f"{b('术语小贴士')}：肩胛骨的旋转（前/后倾、上/下回旋、内/外旋）是附属运动；上提/下沉、内/外侧平移是生理运动。"
    f"描述运动过程用“{b('内侧/外侧平移')}”，描述运动结束后的位置才用“{b('后缩/前伸')}”。"
))

A.append(h2("🔴 核心观点：四句话"))
A.append(table(
    ["观点", "含义"],
    [
        ["① 是损害，不是诊断", "肩胛运动障碍有致病原因，需要找出原因"],
        ["② 病理解剖不是重点", "病理解剖要查，但不应是检查的主要焦点"],
        ["③ 定性检查最实用", "目前临床上最好用的，是判断肩胛是否参与肩部功能障碍的定性检查"],
        ["④ 康复重运动控制", "康复的首要目标是改善运动控制，而不是单纯增加力量"],
    ],
))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、什么是肩胛运动障碍"))
A.append(p(
    f"“Dys”（改变）＋“kinesis”（运动），泛指肩胛骨正常生理、力学和运动的控制丧失。临床表现包括："
))
A.append(ul([
    "内侧缘或内下缘突出",
    "上举手臂时肩胛过早上提（耸肩）",
    "放下手臂时肩胛快速下回旋",
]))
A.append(p(
    f"注意区分{b('“翼状肩胛”')}：这个词最好留给{red('神经损伤导致的')}肩胛异常——手臂一开始动，肩胛某部分就明显离开胸壁，且整个上举和下降过程都不贴合。"
    f"而运动障碍{u('更多在手臂下降阶段')}才看得出来。"
))
A.append(p("肩胛运动障碍与肩部损伤之间的因果关系，目前还没有确立。"))

A.append(h3("❇️二、为什么要重新思考临床检查"))
A.append(p(
    f"{b('83%')} 的肩痛患者就诊，是因为{b('无法完成重要的日常或运动功能')}。作者把功能看成：解剖 × 生理 → 力学 → 完成任务；"
    f"功能障碍就是病理解剖、病理生理、病理力学的不同组合。"
))
A.append(p(
    f"系统综述常批评肩胛检查的“诊断准确性”不足。但作者指出：{hl('运动障碍不是诊断，而是损害，本来就没有可以对照的金标准')}。"
    f"三维运动分析靠体表标记，只是骨骼位置的替代；骨钉研究最准确，却是有创的，无法用于临床。所以{b('定性评估仍是目前最好的临床工具')}。"
))

A.append(h3("❇️三、三步评估流程"))
A.append(img(2))
A.append(cap("图1：肩胛参与情况评估流程（已译为中文重绘）"))
A.append(h4("🔻第一步：有没有运动障碍？——肩胛运动障碍测试"))
A.append(ul([
    "患者双臂前屈上举到最大，再放下，重复 3～5 次",
    "看不清时，可以每只手拿 3～5 磅哑铃，或重复到 10 次，放大异常",
    f"重点看{b('下降阶段')}，记录症状侧内侧缘是否突出：“是”或“否”",
]))
A.append(p(b("三项肩胛肌力测试（看肩胛是否被“打破”位置）：")))
A.append(table(
    ["测试", "目标肌肉"],
    [
        ["手臂前屈 130° 徒手抗阻", "前锯肌"],
        ["手臂外展 130°～150° 徒手抗阻", "中、下斜方肌"],
        ["手臂在体侧后伸", "菱形肌"],
    ],
))
A.append(p("与普通肌力测试不同，这里检查者要试图“打破”患者手臂的位置，同时观察肩胛是否明显移位；两者同时出现提示肩胛肌无力。"))

A.append(h4("🔻第二步：运动障碍和症状有关吗？——矫正手法"))
A.append(table(
    ["矫正手法", "操作", "阳性", "提示"],
    [
        ["肩胛辅助试验", "患者上举手臂时，检查者在肩胛下角内侧施力，辅助肩胛上回旋和后倾", "疼痛弧缓解，活动范围增加", "肩胛运动异常与疼痛有关"],
        ["肩胛后缩试验", "先常规测前屈肌力；再把肩胛内侧缘固定在后缩位，重测", "后缩固定后力量增加", "肩胛参与肩袖力量不足"],
        ["Low Row 试验", "手臂轻度后伸，检查者向前施力，患者抵抗；再让患者收缩臀肌后重测", "收缩臀肌后力量增加", "康复应加入下肢/核心训练"],
    ],
))
A.append(img(4))
A.append(cap("图3（左）：肩胛运动障碍测试，患者双臂上举 3～5 次，检查者观察肩胛运动；图4（右）：肩胛辅助试验，一手稳定肩胛，另一手“辅助”肩胛沿正确平面运动"))
A.append(img(5))
A.append(cap("图5：肩胛后缩试验。a）先做常规前屈徒手肌力测试；b）检查者固定肩胛内侧缘后重复测试"))
A.append(narrow(6, "60%"))
A.append(cap("图6：Low Row 试验。检查者徒手抵抗手臂后伸，先不收缩、再收缩臀肌，比较两次力量"))
A.append(p(
    f"{red('矫正手法阳性')}，说明康复应{b('先关注肩胛活动度、肩胛力量或核心力量')}，而不是一上来就练肩袖。"
))

A.append(h4("🔻第三步：是什么导致了运动障碍？——逐步检查致病因素"))
A.append(img(3))
A.append(cap("图2：临床检查的推进顺序（已译为中文重绘）"))
A.append(p(
    f"作者所在机构对 {b('462 例')}连续就诊、满足前两步标准的肩痛患者做了全面检查（未发表数据）："
))
A.append(table(
    ["类型", "比例", "举例"],
    [
        ["病理解剖原因", "34.7%", "锁骨骨折、肩锁关节病变、盂肱关节内紊乱、神经损伤、肩胛周围肌肉损伤"],
        ["病理生理原因", "65.3%", "肌肉失衡、抑制、紧张/柔韧性差、前锯肌/下斜方肌功能不足"],
    ],
))
A.append(p(
    f"所以评估分两条路：{b('病理解剖型')}（约 1/3）可能需要手术恢复解剖；{b('病理生理型')}（约 2/3）需要全面评估肌肉功能，作为治疗依据。"
    f"部分病理解剖型患者也同时存在原发或继发的病理生理问题。"
))
A.append(p(
    f"这种思路与近年提出的{hl('基于运动损害（而非病理解剖）的分类系统')}一致：先识别可见的异常（如内侧缘突出、肩胛体位置），"
    f"再同时思考原因（活动度、力量、运动控制不足，或明确的解剖损伤）。"
))

A.append(h3("❇️四、为什么要重新思考治疗"))
A.append(p("过去治疗聚焦于提高活动度和力量，但很多研究发现，手法治疗和运动训练对肩胛运动本身影响很小。可能的原因："))
A.append(h4("🔻1. 活动度受限很少是急性的"))
A.append(p(
    f"投掷运动员投球后盂肱旋转会急性减少，但无论干预与否，{b('24～96 小时')}内平均都能恢复。慢性活动度受限往往伴有骨性适应、关节囊增厚和肌腱改变。"
    f"手法治疗后的即时活动度增加{u('不能持久')}，更可能是{b('内源性镇痛')}带来的疼痛调节，而不是组织真的被“矫正”了。"
))
A.append(h4("🔻2. EMG 研究的局限"))
A.append(ul([
    "常被误读为“某个动作只激活某块肌肉”，忽视了肌肉激活的叠加效应",
    "基础研究多在无症状人群中完成",
    "动作多是孤立的、在站立或俯卧/仰卧的静止体位下完成，可能强化低效或错误的运动模式",
]))
A.append(p(f"因此，{red('只关注增加力量，可能不是最理想的干预')}。"))
A.append(h4("🔻3. 问题更可能在运动控制"))
A.append(p(
    f"大多数上肢任务依靠{b('视觉反馈')}来定位和纠错，但肩胛骨在背后，看不见，这可能就是运动障碍的来源之一。研究显示："
))
A.append(ul([
    f"{b('有意识矫正')}：在上举或旋转手臂前先主动摆正肩胛，可以提高肩胛肌激活、改善肩胛运动学",
    f"{b('视觉、听觉、动觉反馈')}都能积极影响肩胛肌激活和位置",
    f"{b('整合动力链')}：坐位或站立位训练，用下肢和躯干带动肩胛和肩部的运动和肌肉激活",
]))
A.append(p(
    f"不过，目前{u('还没有随机对照试验')}比较“运动控制/动力链”方案与传统方案，相关建议都来自专家意见和共识。"
))

A.append(h3("❇️五、运动控制导向的康复方案"))
A.append(p(b("五个临床要点：")))
A.append(table(
    ["要点", "说明"],
    [
        ["① 短力臂进阶", "先从手臂贴近身体的动作开始"],
        ["② 坐位、站立优先", "优于俯卧或仰卧练习"],
        ["③ 按顺序处理损害", "活动度 → 运动控制 → 力量（必要时）→ 耐力"],
        ["④ 长力臂放到后期", "手臂上举或外展 90° 的动作留到康复后期"],
        ["⑤ 出院前做增强式训练", "临近结束时进阶到增强式动作"],
    ],
))
A.append(h4("🔻阶段 1：手臂贴体，建立正确的肩胛位置"))
A.append(p(
    f"从{b('有意识矫正')}和{b('Low Row 练习')}开始，用髋和躯干伸展带动肩胛后缩。"
    f"{red('前 4～6 周避免耸肩、肩胛上提类动作')}，以免过度偏向上斜方肌、延迟肩胛肌群的平衡。"
))
A.append(img(7))
A.append(cap("图7（左）：有意识矫正肩胛，站立位（a），主动“把肩胛骨夹在一起”（b），可借助镜子或手机看到肩胛位置；图8（右）：Low Row 练习，站立、膝微屈（a），伸髋和躯干带动肩胛后缩（b）"))
A.append(h4("🔻阶段 2：仍是短力臂，但更动态"))
A.append(p("前面的动作能完成且不加重症状后，加入更动态的短力臂动作。"))
A.append(img(8))
A.append(cap("图9（左）：手臂贴身的“割草机”，手臂像吊着吊带一样贴近身体（a），伸髋、伸躯干后转体，带动肩胛内侧平移和后缩（b）；图10（右）：“抢劫者”练习，口令“把手肘放进后裤兜”，从躯干和髋微屈（a）到伸展（b）"))
A.append(h4("🔻阶段 3：加入少量上举或外展（约 30°～45°）"))
A.append(img(9))
A.append(cap("图11（左）：手臂离开身体的“割草机”，起始时手臂轻度前屈（a），同样伸髋并转体（b）；图12（右）：“击剑”练习，手臂在额状面上举 90°（a），侧跨步的同时后缩肩胛、内收手臂（b）"))
A.append(h4("🔻阶段 4：传统长力臂动作（上举或外展 90°）"))
A.append(p("只有前面的动作都掌握、几乎不引起症状后，才在康复后期加入。"))
A.append(h4("🔻剂量与阻力"))
A.append(table(
    ["要素", "建议"],
    [
        ["起始剂量", "1～2 组 × 5～10 次，不加外部阻力"],
        ["加量", "根据症状和耐受加组数、次数"],
        ["加阻力的前提", "能完成 5～6 组 × 10 次且症状不加重"],
        ["阻力顺序", "先轻哑铃（最多 2～3 磅，约 1～1.4 kg）→ 再弹力带"],
        ["为什么哑铃在前", "哑铃更稳定；弹力带患者使用时变异大，尤其手臂位置变化时；用弹力带时可用主观用力程度量表监控"],
        ["反馈", "视觉、听觉、动觉反馈都可以；但反馈过多不利于学习，患者会依赖外部信息"],
    ],
))

A.append(h2("⚖️ 证据评价"))
A.append(ul([
    f"{b('专家观点')}：临床观点类文章，未标注证据级别，作者均来自同一个肩胛研究团队",
    f"{b('关键数据未发表')}：34.7%/65.3% 的病因构成来自作者机构未发表的调查，无法核查",
    f"{b('缺乏对照研究')}：作者也承认，运动控制/动力链方案目前没有与传统力量方案对比的随机对照试验",
    f"{b('定性检查的主观性')}：肩胛运动障碍测试和矫正手法依赖检查者经验，信度受影响",
    f"{b('小瑕疵')}：原文有几处拼写错误（如“Cooresponding”“promienance”“aa comprehensive”），不影响理解",
]))

A.append(h2("📌 总结：先找原因，再练控制"))
A.append(p(
    f"{red('① 定位')}：肩胛运动障碍是损害，不是诊断，要找出原因<br>"
    f"{red('② 检查')}：运动障碍测试 → 矫正手法（辅助、后缩、Low Row）→ 逐步排查致病因素<br>"
    f"{red('③ 病因')}：约 1/3 病理解剖，约 2/3 病理生理<br>"
    f"{red('④ 治疗')}：重运动控制，借助有意识矫正、反馈和动力链<br>"
    f"{red('⑤ 进阶')}：短力臂 → 动态短力臂 → 30°～45° → 90° 长力臂 → 增强式<br>"
    f"{red('⑥ 剂量')}：先徒手 5～6 组 × 10 次无症状，再加 2～3 磅哑铃，最后弹力带"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Sciascia A, Kibler WB. Current Views of Scapular Dyskinesis and its Possible Clinical Relevance. "
    "Int J Sports Phys Ther. 2022;17(2):117-130. PMCID: PMC8805107.</em><br>"
    "文中图片均来自原文，图 1、图 2 已译为中文重绘，仅用于学术交流。"
))

TITLE = "「肩胛」肩胛运动障碍：不是诊断，是需要找原因的损害"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>肩胛运动障碍推文</title>
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
