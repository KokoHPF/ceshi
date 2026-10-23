#!/usr/bin/env python3
"""肱二头肌远端修复术后康复（Logan 2019）推文。

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
A = []
A.append(img(1, "原文首页（IJSPT 2019 年第 14 卷第 2 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Rehabilitation Following Distal Biceps Repair（肱二头肌远端修复术后康复）",
    f"{b('作者')}：Catherine A. Logan, MD, MBA, MSPT · Amir Shahien, MD · Daniel Haber, MD · Zach Foster, ATC · Anna Farrington, ATC · Matthew T. Provencher, MD",
    f"{b('机构')}：OrthoONE（丹佛）· 波士顿医疗中心 · 麻省总医院 · Steadman Philippon 研究所 / Steadman 诊所（韦尔）",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2019;14(2):308-317",
    f"{b('DOI')}：10.26603/ijspt20190308（PMCID：PMC6449020）",
    f"{b('文章类型')}：临床评论（Clinical Commentary）",
    f"{b('证据级别')}：原文标注 Level 5（专家意见 / 临床评论）",
    f"{b('关键词')}：Distal biceps tendon rupture · surgical repair · rehabilitation",
], square=True))

# 背景
A.append(h2("🎯 背景：少见，但伤了就是“力量级”损失"))
A.append(quote(
    "Distal biceps tendon ruptures are rare injuries that may have significant functional sequelae.",
    "肱二头肌远端肌腱断裂是一种少见的损伤，但可能留下明显的功能后遗症。",
))
A.append(p(
    f"肱二头肌远端是前臂{b('最主要的旋后肌')}，也是屈肘发力的主力。断了之后，拧螺丝、开门把手、端重物这类动作都会明显无力。"
    f"现在大多数病例都建议{b('手术修复')}，而术后康复的核心矛盾只有一个："
))
A.append(p(f"{hl('既要尽早恢复活动度，又绝不能让刚缝上的肌腱过早受力。')}"))
A.append(p("这篇临床评论用一张 16 周以上的分期表，把这个矛盾拆成了四个阶段——每个阶段做什么、不做什么、什么时候可以往下走，都写得很清楚。"))

# 核心概念
A.append(h2("🔴 核心概念：按“标准”推进的四阶段康复"))
A.append(p("先用一张表看清全貌："))
A.append(table(
    ["阶段", "时间", "核心任务", "关键限制"],
    [
        ["Ⅰ 早期恢复", "0-6 周", "保护修复、消肿止痛、恢复活动度", "支具保护；禁止主动屈肘和旋后；不提物"],
        ["Ⅱ 力量启动", "6-12 周", "伸肘等长 → 等张、腕部与肩胛训练", "仍禁止主动屈肘和旋后；不提物"],
        ["Ⅲ 肱二头肌加载", "12-16 周", "肱二头肌等长 → 第 16 周轻负荷等张", "无特殊限制"],
        ["Ⅳ 回归活动", "16 周以后", "弯举进阶、专项训练、回归运动", "力量差距 ≤10% 才回归"],
    ],
))
A.append(p(
    f"{b('关键点')}：时间只是参考，{u('能不能进入下一阶段，看的是标准')}。"
    f"任何阶段只要出现{red('持续或反复的疼痛 / 肿胀')}，就说明推进过快。"
))

# 逐节
A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、流行病学与解剖：谁容易断？断在哪？"))
A.append(quote(
    "They found that the injury occurs in the dominant extremity 86% of the time and smokers have a 7.5 fold greater risk of injury than nonsmokers.",
    "他们发现，86% 的损伤发生在优势侧上肢，而吸烟者的受伤风险是不吸烟者的 7.5 倍。",
))
A.append(ul([
    f"{b('典型人群')}：30-60 岁男性的优势手",
    f"{b('发生率')}：约每年每 10 万人 1.2 例",
    f"{b('危险因素')}：吸烟（风险 7.5 倍）、合成代谢类固醇、局部激素注射",
    f"{b('解剖要点')}：长头、短头两个头在三角肌粗隆水平合为一体，止于桡骨近端的{b('肱二头肌粗隆')}；"
    f"远端有{b('肱二头肌腱膜（lacertus fibrosus）')}向尺侧展开，起稳定作用",
]))

A.append(h3("❇️二、病因：缺血区 + 机械撞击"))
A.append(quote(
    "With the forearm fully pronated, the space for the distal biceps tendon insertion and its course is 48% less than the space available with the forearm in full supination.",
    "前臂完全旋前时，肱二头肌远端肌腱止点及其走行的空间，比完全旋后时少 48%。",
))
A.append(p(f"Seiler 等的尸体研究给出了两个机制："))
A.append(ul([
    f"{b('血供薄弱')}：肌腹-肌腱交界与粗隆止点之间有一段约 {b('2.14 cm')} 的乏血管区，镜下可见局灶性退变",
    f"{b('机械撞击')}：前臂旋前时肌腱通道变窄 48%，肌腱在桡骨与尺骨之间受挤压",
]))
A.append(p(f"💡这也解释了典型受伤动作：{u('屈肘、前臂旋前时，突然受到一个伸肘方向的外力')}，肱二头肌离心收缩被拉断。"))

A.append(h3("❇️三、诊断：Hook 试验比 MRI 还准"))
A.append(p("患者常描述受伤瞬间“啪”的一声，肘窝锐痛；疼痛缓解后，屈肘略弱，但旋后力量明显下降。两个床旁试验最实用："))
A.append(table(
    ["试验", "做法", "阳性表现"],
    [
        ["肱二头肌挤压试验（Ruland）", "屈肘 90°，挤压肱二头肌肌腹", "前臂没有出现旋后（类似跟腱的 Thompson 试验）"],
        ["Hook 试验（O'Driscoll）", "屈肘 90°，手指从肌腱外侧缘伸入肘窝去“勾”肌腱", "勾不到条索状的肌腱"],
    ],
))
A.append(quote(
    "It is important to emphasize probing the lateral edge of the biceps tendon, as an intact lacertus fibrosis encountered during a medial approach may be mistaken for an intact tendon.",
    "必须强调从肱二头肌腱的外侧缘去探查，因为从内侧探查时，完整的肱二头肌腱膜可能被误认为肌腱完好。",
))
A.append(ul([
    f"原始 45 例队列中，Hook 试验的敏感度和特异度都是 {b('100%')}，高于 MRI 的 92% / 85%",
    "X 光片作用有限，偶尔能看到桡骨粗隆的撕脱骨块",
    "怀疑部分断裂或陈旧损伤时，可做 FABS 体位 MRI（屈肘 90°、肩外展 180°、前臂旋后）",
]))

A.append(h3("❇️四、手术：单切口 vs 双切口"))
A.append(quote(
    "Surgical repair is ideally performed within a few weeks from injury.",
    "手术修复最好在受伤后几周内进行。",
))
A.append(p("拖得太久，肌腱回缩、瘢痕形成，可能只能做更大的重建手术（多用同种异体肌腱移植延长）。"))
A.append(table(
    ["对比项", "单切口", "双切口"],
    [
        ["前臂外侧皮神经麻痹", "11.6%", "5.8%"],
        ["异位骨化", "3.1%", "7%"],
        ["主要风险", "前臂外侧皮神经损伤", "骨间后神经损伤、异位骨化（可致桡尺骨融合）"],
        ["最终等长屈肘力量（Grewal）", "104%", "94%"],
    ],
))
A.append(small("🔖注：并发症数据来自 Watson 等的系统综述（22 项研究，494 例患者 / 498 个肘关节），总体并发症率 24.5%；力量数据来自 Grewal 等的随机对照研究，两组 2 年时疼痛与功能评分无差异。"))
A.append(quote(
    "Re-rupture occurred in 1.6% of cases overall, and there was no difference in re-rupture rates between the single and two-incision groups.",
    "总体再断裂率为 1.6%，单切口与双切口之间没有差异。",
))
A.append(p(
    f"固定方式上，{b('皮质骨纽扣（cortical button）')}的抗拉强度最高，但循环负荷下肌腱在止点处会有微动。"
    f"{hl('纽扣 + 挤压螺钉的双重固定')}既保留了强度，又减少了微动和间隙形成，{u('可能允许更积极的术后康复')}。"
    "所以康复开始前，一定要问清楚手术方式和固定方式。"
))

A.append(h3("❇️五、康复总原则"))
A.append(quote(
    "The overall principles guiding rehabilitation of the distal biceps tendon repair include protection of the tendon from excess load, followed by the safe and step-wise return to activities of daily living and sport.",
    "指导肱二头肌远端修复术后康复的总体原则是：先保护肌腱免受过度负荷，再安全、循序渐进地回归日常生活和运动。",
))
A.append(quote(
    "A complaint of persistent or recurrent pain and/or swelling indicate inappropriate phase progression.",
    "如果出现持续或反复的疼痛和 / 或肿胀，说明阶段推进不当。",
))
A.append(p(f"{b('支具')}：术后佩戴以保护修复。如果肌腱有回缩、缝合张力较大，医生会先限制伸肘角度，在 4-6 周内逐步放开，可用铰链式肘支具维持角度限制。"))

A.append(h3("❇️六、Ⅰ期：早期恢复（0-6 周）"))
A.append(quote(
    "No active elbow flexion or supination is permitted, including tasks such as drinking coffee or feeding.",
    "不允许任何主动屈肘或旋后，包括喝咖啡、吃饭这类动作。",
))
A.append(ul([
    f"{b('冷疗')}：冰按摩、冰袋、冷水浴或 Cryo-Cuff 冷敷袖套，每次 5-20 分钟，注意避免皮肤刺激",
    f"{b('立即开始')}：手和腕的活动、抓握练习（捏橡皮球、用手机都可以）",
    f"{b('肩胛与肩')}：肩胛后缩 / 前伸 / 上提 / 下沉，盂肱关节被动和主动活动，避免肩痛和僵硬",
    f"{b('肘关节')}：按术中确定的范围活动，通常前两周允许被动 0-90°；{b('第 2 周起')}可做重力辅助的屈伸",
    f"{b('可以做')}：电脑打字；{b('不能做')}：患肢提任何东西",
    f"{b('心肺训练')}：第 1 周就可开始跑步机步行、不用手臂的椭圆机、单车，{u('但一定要防跌倒，避免摔在患肢上')}",
]))
A.append(p(f"🎯{b('目标')}：第 6 周达到无痛的全范围活动。"))

A.append(h3("❇️七、Ⅱ期：力量启动（6-12 周）"))
A.append(p(f"这一阶段仍然{red('禁止主动屈肘和旋后、禁止提物')}，力量训练先从“肱二头肌以外”的肌群开始："))
A.append(ul([
    f"{b('第 6 周')}：伸肘肌（肱三头肌）等长收缩",
    f"{b('第 8 周')}：肱三头肌等张训练、腕屈伸肌力量、肩带力量",
    f"{b('姿势控制训练')}：纠正肩胛运动障碍，为Ⅲ期的力量进阶打基础",
]))
A.append(h4("🔻动作 1：坐位肱三头肌等长收缩"))
A.append(img(2, "坐位，前臂放在旁边桌面上、掌心向下，同侧肩带放松，用整个前臂和手掌向下压桌面"))
A.append(p(f"剂量：{b('每次保持 10 秒，10-15 次，3-5 组')}。"))
A.append(h4("🔻动作 2：瑞士球俯卧姿势控制"))
A.append(img(3, "俯卧在瑞士球上，保持脊柱中立、颈部放松，肩外展并外旋，两侧肩胛骨向中间夹紧"))
A.append(p(f"剂量：{b('夹紧保持 3 秒，10-15 次，3-5 组')}。"))
A.append(p(f"🚦{b('进入Ⅲ期的标准')}：肩、肘、腕、手无痛全范围活动；肩胛胸壁力学正常（无运动障碍）。"))

A.append(h3("❇️八、Ⅲ期：肱二头肌加载（12-16 周）"))
A.append(ul([
    f"{b('第 12 周')}：开始肱二头肌等长收缩",
    f"{b('第 16 周')}：开始轻负荷等张弯举——传统、锤式、反握三种握法",
    f"{b('肩袖与肩胛周围稳定训练')}：开链、闭链都要做",
    f"{b('心肺训练')}：椭圆机可以开始用手臂",
]))
A.append(quote(
    "Inclusion of both open and closed kinetic chain exercises is essential, as activity of shoulder girdle musculature demonstrates significant electromyographic (EMG) differences when activated in exercises performed in an open versus closed kinetic chain.",
    "开链和闭链训练都必须纳入，因为肩带肌群在开链与闭链练习中的肌电激活存在显著差异。",
))
A.append(img(4, "三种弯举：A 传统弯举（掌心朝前）；B 锤式弯举（掌心朝向身体）；C 反握弯举（掌心朝后）。站立、肩放松，10-15 次，3-5 组"))
A.append(p(f"🚦{b('进入Ⅳ期的标准')}：全范围无痛活动；肩胛力学正常；{b('肱二头肌抗重力肌力 5/5')}。"))

A.append(h3("❇️九、Ⅳ期：回归活动（16 周以后）"))
A.append(img(5, "肱二头肌侧举弯举：A 起始位，肩屈曲 90°、外展 90°，掌心向上；B 保持肩带和颈部放松，屈肘。10-12 次，3-5 组"))
A.append(ul([
    "弯举进阶：传统、锤式、反握，加上侧举弯举",
    "肱三头肌伸展、肩袖与肩胛周围强化",
    "专项训练：设计覆盖上肢、下肢和躯干的功能性动作训练",
]))
A.append(quote(
    "Criteria for return to activity include full and painless range of motion, strength within 10% of the contralateral upper extremity and pain-free participation in activity-specific movement patterns.",
    "回归活动的标准包括：全范围无痛活动、力量与对侧上肢相差不超过 10%、能无痛完成专项动作模式。",
))
A.append(p(f"⚠️原文坦言：{u('目前没有专门针对肱二头肌远端修复术后的回归运动测试')}，需要治疗师根据专项动作的质量和力量来判断。"))

A.append(h3("❇️十、完整方案（原文附录 1 中文全译）"))
A.append(phase_card("Ⅰ期", "术后 0-6 周", [
    ("注意事项", ["活动范围由术中确定，通常前两周允许被动 0-90°", "支具保护至第 6 周，逐步放开活动范围", "患肢不提物", "禁止主动屈肘和旋后"]),
    ("目标", "第 6 周达到无痛的全范围活动"),
    ("训练", ["按医嘱进行肘关节活动", "手 / 腕活动与水肿控制", "肩胛后缩 / 前伸 / 上提 / 下沉", "重力辅助屈伸（第 2 周起）", "心肺训练（跑步机步行、不用手臂的椭圆机、单车）"]),
    ("进阶标准", "出现持续或反复的疼痛和 / 或肿胀时，不得进入Ⅱ期"),
]))
A.append(phase_card("Ⅱ期", "术后 6-12 周", [
    ("注意事项", ["患肢不提物", "禁止主动屈肘和旋后"]),
    ("目标", ["维持正常的肩胛胸壁力学", "开始上肢力量训练"]),
    ("训练", ["肱三头肌等长训练（图2）", "肱三头肌等张训练（第 8 周起）", "腕屈肌、伸肌力量训练（第 8 周起）", "姿势控制训练（图3）", "肩胛后缩 / 前伸", "心肺训练（同Ⅰ期）"]),
    ("进阶标准", ["肩、肘、腕、手无痛全范围活动", "肩胛胸壁力学正常（无运动障碍）"]),
]))
A.append(phase_card("Ⅲ期", "术后 12-16 周", [
    ("注意事项", "无"),
    ("目标", "增加上肢功能性力量"),
    ("训练", ["肱二头肌等长训练", "轻负荷肱二头肌等张训练（第 16 周起，图4）：锤式、传统、反握", "肩袖与肩胛周围稳定训练：开链和闭链", "心肺训练（椭圆机可用手臂）"]),
    ("进阶标准", ["肩、肘、腕、手无痛全范围活动", "肩胛胸壁力学正常（无运动障碍）", "肱二头肌抗重力肌力满分（徒手肌力 5/5）"]),
]))
A.append(phase_card("Ⅳ期", "术后 16 周以后", [
    ("注意事项", "无"),
    ("目标", ["继续增强上肢力量", "回归运动和 / 或日常活动"]),
    ("训练", ["肱二头肌弯举：锤式、传统、反握、侧举弯举（图5）", "肱三头肌伸展", "肩袖与肩胛周围强化", "专项训练", "心肺训练"]),
    ("出院标准", "通过功能 / 专项测试后，转入维持训练计划"),
]))

# 证据评价
A.append(h2("🔍 证据评价"))
A.append(p("▪️" + b("值得肯定的部分：")))
A.append(ul([
    "每个阶段都写清了注意事项、目标、训练内容和进阶标准，可以直接用于临床",
    "诊断部分给出了量化数据（Hook 试验敏感度、特异度均为 100%），实用性强",
    "手术部分引用系统综述和随机对照研究，帮助康复治疗师理解不同术式的风险差异",
    "提醒康复前先了解固定方式，体现了医生与治疗师之间沟通的重要性",
]))
A.append(p("▪️" + b("需要谨慎看待的部分：")))
A.append(ul([
    f"{b('证据级别为 Level 5')}：方案来自通讯作者所在机构的经验，{u('没有报告使用这个方案的疗效数据')}",
    "各阶段的时间节点较保守，原文也提到双重固定可能允许更积极的康复，但没有给出对应的加速方案",
    "Ⅲ期“第 12 周开始等长、第 16 周开始等张”，而进入Ⅳ期又要求“抗重力 5/5”，两者之间的衔接写得比较粗",
    "没有专门的回归运动测试，“力量差距 ≤10%”具体用什么方法测量，原文没有说明",
]))

# 临床启示
A.append(h2("🧠 物理治疗临床实践启示"))
A.append(h3("🔻启示1：拿到病人先问手术细节"))
A.append(p("单切口还是双切口？用的什么固定方式？术中允许的活动范围是多少？是否有伸肘限制？这些信息直接决定Ⅰ期怎么做。"))
A.append(h3("🔻启示2：前 12 周的红线是“主动屈肘 + 旋后”"))
A.append(p(f"喝水、吃饭、拧瓶盖都属于主动屈肘或旋后。{b('一定要把这些日常动作具体讲给患者听')}，否则患者很容易在家里不知不觉就违反了禁令。"))
A.append(h3("🔻启示3：别让肩和手“陪葬”"))
A.append(p("肘被保护的这段时间，手、腕、肩胛和肩的活动要从第一天就开始，心肺训练也可以从第 1 周开始——前提是防跌倒。"))
A.append(h3("🔻启示4：用疼痛和肿胀当“刹车”"))
A.append(p("任何阶段出现持续或反复的疼痛、肿胀，都应退回上一阶段，而不是硬按时间表往前推。"))
A.append(h3("🔻启示5：回归运动看“对侧 10%”"))
A.append(p("建议用手持测力计分别测屈肘和旋后力量，与健侧对比；再结合专项动作质量，综合判断能否回归。"))

# 总结
A.append(h2("📌 总结：先护住肌腱，再一步步找回力量"))
A.append(p(
    f"{red('① 0-6 周')}：支具保护，禁止主动屈肘和旋后，手腕肩胛先动起来<br>"
    f"{red('② 6-12 周')}：肱三头肌、腕部、肩胛和姿势控制先练<br>"
    f"{red('③ 12-16 周')}：肱二头肌从等长开始，第 16 周轻负荷弯举<br>"
    f"{red('④ 16 周以后')}：弯举进阶 + 专项训练，力量差距 ≤10% 再回归"
))
A.append(p(f"📡{b('时间表是参考，标准才是门槛。疼痛和肿胀，是最诚实的进度条。')}"))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Logan CA, Shahien A, Haber D, Foster Z, Farrington A, Provencher MT. Rehabilitation Following Distal Biceps Repair. "
    "Int J Sports Phys Ther. 2019;14(2):308-317. doi:10.26603/ijspt20190308. PMCID: PMC6449020.</em><br>"
    "文中图片均来自原文，仅用于学术交流。"
))

BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>肱二头肌远端修复康复推文</title>
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
<h1>「肘关节」肱二头肌远端肌腱修复术后康复：16 周分期方案</h1>
<div class="by">原创 · 骨科康复小黄</div>
""" + BODY + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars")
