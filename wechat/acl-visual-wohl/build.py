#!/usr/bin/env python3
"""ACL 损伤后视觉干扰训练（Wohl 2021）推文。

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


def tcap(t):
    return f'<p style="margin:0 0 8px;font-size:14px;line-height:1.6;color:#000;font-weight:bold;">{t}</p>'


def br(items):
    return "<br>".join(f"• {x}" for x in items)


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2021 年第 16 卷第 2 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Visual Perturbation to Enhance Return to Sport Rehabilitation after Anterior Cruciate Ligament Injury: A Clinical Commentary（用视觉干扰增强 ACL 损伤后的重返运动康复：临床评论）",
    f"{b('作者')}：Timothy R. Wohl · Cody R. Criss · Dustin R. Grooms",
    f"{b('机构')}：俄亥俄大学荣誉导师学院、俄亥俄肌骨与神经研究所、运动防护与物理治疗系；俄亥俄州立大学物理治疗系（美国）",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2021;16(2):552-564",
    f"{b('PMCID')}：PMC8016421",
    f"{b('文章类型')}：临床评论 / 当前概念综述",
    f"{b('证据级别')}：5 级",
    f"{b('关键词')}：anterior cruciate ligament · ACL · rehabilitation · stroboscopic glasses",
], square=True))

A.append(h2("🎯 背景：ACL 伤的是膝，改变的却是大脑"))
A.append(p(
    f"ACL 断裂后，即使接受了全面康复、恢复了股四头肌力量和关节稳定，{b('再伤率仍然很高')}，年轻女运动员尤甚。"
    "作者认为，这可能与康复没处理好的“神经层面”后果有关。"
))
A.append(p(
    f"ACL 虽是外周关节损伤，但积液、疼痛、机械不稳和关节机械感受器丢失（{b('传入阻滞')}）会引起{b('中枢神经系统重组')}："
    f"本体感觉下降、协调受损，控制下肢时{hl('更依赖视觉、注意力和认知')}。"
    "比赛场上视觉信息铺天盖地，这种“靠眼睛盯着动”的代偿就可能成为再伤隐患。"
))
A.append(p(
    f"本文提出用{b('频闪眼镜（stroboscopic glasses）')}做{b('视觉干扰训练')}，配合{b('视觉外部注意焦点')}和{b('内隐学习')}两条运动学习原则，"
    "促使神经系统把权重从视觉“调回”本体感觉，和/或提高视觉-运动处理效率。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["环节", "要点"],
    [
        ["问题", "ACL 损伤后控制下肢更依赖视觉和认知；视觉受干扰或双任务时表现明显变差"],
        ["证据", "行为学（遮挡视觉后姿势摇摆增加）+ 神经影像（视觉相关脑区和额叶激活增加、神经效率下降）"],
        ["工具", "频闪眼镜：透明期固定 100 毫秒，不透明期 25～900 毫秒可调，分级减少视觉信息"],
        ["运动学习", "视觉外部注意焦点（盯环境/目标而非关节）+ 内隐学习（比喻式指令、简单对/错反馈）"],
        ["训练举例", "T 型测试、敏捷梯、单腿硬拉、泡沫垫单腿站、纵跳摸高、转向深蹲跳"],
        ["进阶", "先能完成动作再戴眼镜；从最容易的级别开始；用错误计分、NASA-TLX 或 Borg 量表调难度"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('让患者在“看不太清”的情况下练动作，同时用目标和比喻代替“膝盖别内扣”式的提示，减少对视觉和意识控制的依赖')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、行为学证据：更依赖视觉、更耗认知"))
A.append(h4("🔻视觉依赖增加"))
A.append(ul([
    f"视觉不受限时，ACL 损伤者与健康人的姿势控制相近；{b('视觉一受干扰')}，损伤者表现明显更差（摇摆增加、任务失败）",
    "有荟萃分析认为 ACL 重建者不像未重建者那样依赖视觉，但可能是测试不够难：单腿站允许伸直膝、静态任务挑战不足、完全闭眼不足以干扰视觉空间处理",
    f"在{b('频闪眼镜下的跳落')}、闭眼时双腿到单腿站的过渡和视觉-认知任务中，ACL 重建者受影响更大",
    "原因：Ruffini、Pacini 小体等韧带机械感受器提供关节位置、运动和加速度信息，丢失后中枢把权重转向更可靠的视觉和前庭（贝叶斯最优整合模型），或调动更多认知和注意",
    f"康复本身也可能加重视觉依赖：多用视觉主导的训练，并给予{b('内部注意焦点')}反馈（强调关节角度、肌肉激活）",
]))
A.append(h4("🔻神经认知负荷增加"))
A.append(ul([
    f"过度膝外翻是初次和再次 ACL 损伤的主要危险因素（敏感度 {b('78%')}，特异度 {b('73%')}）",
    "Herman 和 Barth：视觉记忆和神经认知较差者，在落地后需要临时反应的跳落中膝外翻更多",
    "ACL 损伤者在姿势稳定、步态和平衡任务中的双任务代价更高（双任务如单腿站同时从 1000 每次减 7 倒数）",
    "可能机制：初级运动皮层失去正常 ACL 传入信息，额叶（辅助运动区、前辅助运动区）增加活动来代偿；比赛的认知需求可能超出患者同时关注外界刺激并保持安全力学的能力",
]))

A.append(h3("❇️二、神经影像证据"))
A.append(table(
    ["研究对象", "发现", "意义"],
    [
        ["ACL 缺失者（伤后约 2 年）", "单侧屈伸膝时颞下回后部激活增加；前辅助运动区激活增加", "颞下回后部参与识别生物运动；提示简单动作也需要更多皮层计划"],
        ["ACL 重建者（术后约 3 年）", "膝及髋-膝协调动作时舌回激活增加", "舌回参与视觉与触觉的空间整合，提示视觉处理权重转移"],
        ["ACL 重建者（术后约 5 年）", "额回、额极下部、扣带旁回、前扣带回激活增加", "用更多认知资源控制运动，神经效率下降"],
        ["ACL 重建者（术后约 1 年，脑电）", "力控制和关节位置觉任务中额叶 θ 波功率增加", "θ 波反映集中注意和任务复杂度：简单任务也更“费脑”"],
        ["ACL 缺失者（脑电）", "走、跑、落地时 δ、θ、α、β 波功率增加，跑和落地时额顶叶 β 波不对称", "日常和运动动作需要更多认知/注意资源"],
    ],
))
A.append(p(
    f"{b('神经效率')}：专家完成熟练任务所需的神经活动少于新手，并能应对更复杂的协调和环境干扰。ACL 损伤后神经效率下降，可能导致双任务或非预期动作中表现变差，"
    f"并在{b('重返运动早期快速增加动作复杂度和环境刺激时')}增加再伤风险。"
))

A.append(h3("❇️三、视觉干扰训练：频闪眼镜"))
A.append(ul([
    "传统视觉干扰只有睁眼/闭眼两档，没有中间进阶",
    f"频闪眼镜让镜片在透明和不透明之间切换：透明期固定 {b('100 毫秒')}，不透明期 {b('25～900 毫秒')}可调，可以{b('分级')}减少视觉信息",
    "原为便携运动训练工具；研究显示能改善运动一致性判断、分配注意、多目标追踪、短时视觉记忆、预判，以及单腿蹲、冰球、网球、羽毛球等专项表现",
    "能在可控的诊室环境中模拟运动时的动态视觉-运动和认知/注意需求",
    "目的：减少可用视觉信息，迫使运动员上调剩余的本体感觉和前庭输入；也可能代偿性地提高视觉-运动处理效率",
]))

A.append(h3("❇️四、两条运动学习原则"))
A.append(h4("🔻① 视觉外部注意焦点"))
A.append(ul([
    "外部焦点（EF）关注动作目标或动作对环境的影响；内部焦点（IF）关注身体部位或动作本身",
    "作者把 EF 改造成“把注意力推向外部视觉空间”，更接近真实比赛",
    f"例：单腿站时{b('伸直手臂让一根轻杆保持水平')}是视觉外部焦点；让患者“注意踝、膝、髋对齐”则是内部焦点——后者是 ACL 康复中的主流做法",
    f"{b('受限动作假说')}：有意识地关注动作会限制原本自动的皮层下控制过程；外部焦点能把控制交给皮层下，减轻皮层注意负担",
    "外部焦点能改善敏捷表现、提高跳跃高度，并让 ACL 重建者单腿跳远落地更安全；还能延长力竭时间、降低主观用力、提高动作效率",
]))
A.append(h4("🔻② 内隐学习"))
A.append(ul([
    "人类天生通过观察和试错学会动作（骑车、走路、扔东西）；内隐反馈不依赖明确的口头规则，减少动作所需的注意",
    "显性提示调动额顶叶认知过程，内隐提示更直接作用于感觉运动系统，并与运动皮层重组有关",
    "Popovic 等：内隐反馈比显性反馈或无反馈更能改善落地力学",
    f"例：训练跳落时，显性方式是逐条告诉运动员躯干前屈、屈膝、膝外翻、足旋转等；内隐方式则用{b('比喻')}（如“像羽毛一样落地”）加{b('简单的“对/错”“好/不好”反馈')}",
    "省下的认知资源可以用来关注球、对手等外界视觉刺激，同时保持神经肌肉控制",
]))

A.append(h3("❇️五、临床应用：六个训练举例"))
A.append(img(2))
A.append(cap("图1：训练举例——T 型测试（A）、敏捷梯（B）、单腿硬拉（C）、泡沫垫单腿站（D）、纵跳摸高（E）、深蹲跳（F）；受试者佩戴频闪眼镜"))
A.append(ul([
    f"{b('T 型测试（A）')}：前跑 10 米摸锥桶，向一侧切 5 米摸锥桶，再向对侧切 10 米，回中 5 米，最后后退跑 10 米回起点；进阶时由治疗师在到达第一个锥桶前喊“左/右”，变成{b('非预期切步')}（非预期切步的损伤风险力学更明显）",
    f"{b('敏捷梯（B）')}：在梯格内按指定脚步模式移动",
    f"{b('单腿硬拉（C）')}：轻轻把一个小物件放在锥桶旁；进阶时在视野内不同角度放多个锥桶（距离为单腿站时最大伸够距离），治疗师随机喊“左/中/右”",
    f"{b('泡沫垫单腿站（D）')}：伸直手臂握一根轻杆，专注于让杆保持水平",
    f"{b('纵跳摸高（E）')}：用 VERTEC 摸到最大纵跳高度 80% 的标记；起跳腾空初期治疗师喊“左/右”，要求单腿落地，形成{b('非预期落地')}",
    f"{b('深蹲跳（F）')}：在 0°、90°、180°、270° 方向放 4 个编号锥桶，治疗师快速喊号，每次跳完转身面对对应锥桶；可增加锥桶或加快喊号",
]))
A.append(tcap("表1　采用视觉外部焦点和内隐学习原则的器材与指令"))
A.append(table(
    ["训练", "视觉提示", "内隐提示"],
    [
        ["T 型测试", "摸锥桶", "“像猎豹一样快跑”"],
        ["敏捷梯", "梯子的边界", "“地板像岩浆一样烫”"],
        ["单腿硬拉", "把物件放到锥桶旁", "“像水一样流畅”"],
        ["泡沫垫单腿站", "保持横杆水平", "“像岩石一样稳”"],
        ["纵跳摸高", "摸到头顶目标", "“像火山一样爆发”"],
        ["深蹲跳", "落地时面向锥桶", "“像袋鼠一样跳”"],
    ],
))
A.append(tcap("表2　评估表现的错误计分"))
A.append(table(
    ["训练", "记为错误"],
    [
        ["T 型测试", br(["漏摸锥桶", "切错方向"])],
        ["敏捷梯", br(["碰到梯子", "落脚位置错误"])],
        ["单腿硬拉", br(["对侧脚触地", "任一手触地", "物件放错位置"])],
        ["泡沫垫单腿站", br(["对侧脚触地", "任一手触地"])],
        ["纵跳摸高", br(["没摸到目标", "落错脚"])],
        ["深蹲跳", br(["落地朝向错误"])],
    ],
))

A.append(h3("❇️六、频闪眼镜怎么调级别"))
A.append(ul([
    f"先确认患者{b('不戴眼镜')}能完成所有训练",
    f"从{b('最容易的级别')}（透明/不透明切换频率最高）开始；表现进步后逐步提高难度",
    "除错误计分外，可用 NASA 任务负荷指数或 Borg 主观用力量表调整难度：想模拟“困难”的比赛情境，但患者只评为“中等”，就提高干扰级别",
    f"另一种做法：先把眼镜加到{b('低于当前能力')}的训练上。例如刚能完成单腿跳的患者，先在单腿平衡中戴眼镜，成功后再在单腿跳中戴",
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：5 级临床评论；视觉依赖和神经效率下降的证据来自横断面行为学和神经影像研究，{red('尚无研究验证频闪眼镜训练能改善 ACL 患者结局或降低再伤')}，作者也明确说需要研究",
    f"{b('亮点')}：把神经科学发现转化为可操作的训练，给出具体动作、视觉提示、比喻指令和错误计分，便于临床和研究复制",
    f"{b('局限')}：频闪眼镜需要专门设备、成本不低；未给出每次训练的剂量、频次和级别进阶的具体标准；神经影像研究样本小、对象（缺失/重建、伤后时间）不一致",
    f"{b('注意')}：视觉依赖的证据并不完全一致（荟萃分析显示重建者依赖程度低于未重建者），作者认为可能是测试不够难",
    f"{b('小瑕疵')}：T 型测试描述中的回程方向与标准 T 型测试（侧滑步、后退跑）略有出入；原文多处“perturbating”为非标准拼写",
]))

A.append(h2("📌 总结：ACL 康复中加入视觉干扰训练"))
A.append(p(
    f"{red('① 为什么')}：ACL 损伤后中枢重组，控制下肢更依赖视觉和认知，比赛中容易“顾此失彼”<br>"
    f"{red('② 用什么')}：频闪眼镜，透明 100 毫秒、不透明 25～900 毫秒分级可调<br>"
    f"{red('③ 怎么教')}：视觉外部焦点（摸锥桶、保持杆水平）+ 内隐学习（“像羽毛一样落地”，只说对/错）<br>"
    f"{red('④ 练什么')}：T 型测试、敏捷梯、单腿硬拉、泡沫垫单腿站、纵跳摸高、转向深蹲跳，可加非预期口令<br>"
    f"{red('⑤ 怎么进阶')}：先不戴能完成，再从最易级别戴；用错误计分和主观难度调级别<br>"
    f"{red('⑥ 证据')}：理论合理，但疗效尚待研究验证"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Wohl TR, Criss CR, Grooms DR. Visual Perturbation to Enhance Return to Sport Rehabilitation after Anterior Cruciate Ligament Injury: "
    "A Clinical Commentary. Int J Sports Phys Ther. 2021;16(2):552-564. PMCID: PMC8016421.</em><br>"
    "文中图片来自原文（图中仅有 A～F 字母）；表 1～2 已译为中文，仅用于学术交流。"
))

TITLE = "「膝关节」ACL 伤后为什么总“靠眼睛”？频闪眼镜视觉干扰训练"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>ACL视觉干扰训练推文</title>
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
