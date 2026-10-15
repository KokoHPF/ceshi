#!/usr/bin/env python3
"""肩关节后方稳定术后康复（Goldenberg 2021）推文。

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
def fig(k, caption, w=None):
    """原文 Figure k → images/img{k+1}.jpg；图注直接用原文图号；w 用于缩窄"""
    h = img(k + 1)
    if w:
        h = h.replace("width:100%;max-width:100%;", f"width:{w};max-width:{w};")
    return (h +
            f'<p style="margin:0 0 20px;font-size:12px;line-height:1.6;color:#888;">🔖图{k}：{caption}</p>')


def tcap(t):
    return f'<p style="margin:0 0 8px;font-size:14px;line-height:1.6;color:#000;font-weight:bold;">{t}</p>'


A = []
A.append(img(1))
A.append('<p style="margin:0 0 20px;font-size:12px;line-height:1.6;color:#888;">🔖原文首页（IJSPT 2021 年第 16 卷第 3 期）</p>')

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Rehabilitation Following Posterior Shoulder Stabilization（肩关节后方稳定术后的康复）",
    f"{b('作者')}：Brandon T. Goldenberg, Pamela Goldsten, Lucca Lacheta, Justin W. Arner, Matthew T. Provencher, Peter J. Millett",
    f"{b('机构')}：Steadman Philippon 研究所 · Howard Head 运动医学 · 柏林夏里特医学院 · The Steadman Clinic",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2021;16(3):930-940",
    f"{b('PMCID')}：PMC8168996",
    f"{b('文章类型')}：临床评论 / 现代概念综述（Clinical Commentary / Current Concept Review）",
    f"{b('证据级别')}：5 级",
    f"{b('关键词')}：rehabilitation · posterior shoulder instability · physical therapy · movement system",
], square=True))

A.append(h2("🎯 背景：后方不稳，比想象中常见"))
A.append(quote(
    "Posterior shoulder instability has historically accounted for 2-5% of instability cases. However, recent reports estimate posterior instability accounts for approximately 24% of all operative glenohumeral instability cases.",
    "过去认为后方不稳只占肩关节不稳的 2%～5%，但近期报道显示，在接受手术的盂肱关节不稳中，后方不稳约占 24%。",
))
A.append(ul([
    f"{b('高发人群')}：过头投掷运动员（挥臂后期和随球动作对后方结构压力大）、举重者，以及经常做俯卧撑、格斗、负重训练的军人",
    f"{b('症状不典型')}：主诉多是{u('疼痛而不是“脱出来”')}，容易延误诊治、影响运动表现",
    f"{b('病因')}：急性创伤、反复微创伤、随意性脱位",
]))
A.append(p(
    f"保守治疗无效时，常做{b('关节镜后方盂唇修复')}（±关节囊修复）。但关于术后康复的文献很少，"
    f"这篇评论给出了一套{hl('以标准为导向的五阶段术后康复方案')}。"
))

A.append(h2("🔴 核心概念：五个阶段，达标才进阶"))
A.append(table(
    ["阶段", "大致时间", "核心目标"],
    [
        ["Ⅰ 保护期", "术后 0～6 周", "保护修复、止痛消肿、宣教；第 2 周起限制范围内被动活动"],
        ["Ⅱ 主动活动与肌耐力", "约 5～6 周起", "恢复主动活动度、肩袖和肩胛肌耐力、正常肩肱节律"],
        ["Ⅲ 初期抗阻", "≥8 周", "弹力带、轻哑铃加强肩袖和肩胛周围肌"],
        ["Ⅳ 进阶强化与爆发力", "约 3 个月起；爆发力约 5 个月", "闭链训练、后方负荷下的控制、增强式训练"],
        ["Ⅴ 重返运动", "通过功能测试后", "专项训练，如投掷程序"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('6 周内别让肩后方受力，之后按标准一步步加载')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、解剖：后方为什么容易松"))
A.append(ul([
    f"{b('盂唇')}：加深关节盂，像一圈“防剪切缓冲垫”",
    f"{b('动态稳定')}：肩袖和肩胛胸壁肌群；{red('肩胛下肌')}对后方稳定尤其重要；肩胛前伸、内侧缘稳定的良好节律也很关键",
    f"{b('后方结构薄弱')}：盂肱下韧带后束比前束薄；后方和多向不稳患者的后关节囊截面积更小，所以{u('较小的力量就可能造成损伤，这也解释了为什么反复微创伤是常见原因')}",
    f"{b('关节盂后倾')}：后方不稳患者后倾 -15.4°±5.1°，前方不稳为 -12.1°±6.9°（p<0.016）；但谁因谁果尚不清楚",
]))

A.append(h3("❇️二、手术"))
A.append(p(
    f"适用于保守治疗失败，或急性创伤伴明显软组织、骨性损伤者。没有骨缺损时，通常用缝合锚钉做{b('关节镜后方盂唇修复 ± 关节囊修复')}，"
    f"重返运动率和满意度都很高。常见合并伤有 SLAP 损伤、反 Hill-Sachs 损伤、肩袖撕裂；有关节盂骨缺损或发育不良时，可考虑植骨或关节盂截骨。"
))
A.append(quote(
    "It should be noted that the operating surgeon should be involved in the individualization of each patient’s rehabilitation protocol based on intra-operative findings.",
    "需要注意的是，主刀医生应根据术中所见参与制定每位患者的个体化康复方案。",
))

A.append(h3("❇️三、Ⅰ期：保护期（术后 0～6 周）"))
A.append(h4("🔻目标与要点"))
A.append(ul([
    f"{b('目标')}：保护修复、减轻疼痛和水肿、保持邻近关节活动度、{red('患者宣教')}",
    f"{b('开始时间')}：术后第 1 天即可开始物理治疗",
    f"{b('制动')}：带外展枕的吊带，让肩处于肩胛平面；制动时长取决于组织质量和修复范围",
    f"{b('冷疗')}：术后前 2 周，每天 5～6 次，每次 30 分钟",
    f"{b('预防血栓')}：弹力袜、踝泵",
    f"{b('邻近关节')}：颈椎、肘、腕、手主动活动；轻柔的肩胛后缩和下沉；脱吊带做，每天 3～4 次",
]))
A.append(h4("🔻被动活动（PROM）"))
A.append(p("通常术后 2 周、经医生同意后开始（也可以立即开始，视医生习惯而定）。到术后 6 周前的限制："))
A.append(table(
    ["方向", "限制"],
    [
        ["前屈", "≤120°"],
        ["外展", "≤90°"],
        ["内旋", "手臂贴体侧，内旋到腹部"],
        ["外旋", "≤30°（视病例和医生而定）"],
        ["禁忌", f"{red('至少 6 周内避免后方负荷，以及手臂离开身体时的内旋（如向身后够物）')}"],
    ],
))
A.append(h4("🔻等长收缩"))
A.append(p(
    f"开始 PROM 后 2～4 周，引入肩袖和肩胛肌群的{b('次最大等长收缩')}：站在门框处以墙为阻力，针对肩胛下肌、冈下肌、三角肌和菱形肌，"
    f"从约 {b('25% 最大力量')}开始逐渐增加，强调无痛和肩胛控制。"
))
A.append(p(
    f"{b('原理')}：肩胛下肌与冈下肌、小圆肌组成前后力偶，把肱骨头压向关节盂；三者还提供向内下的力，对抗三角肌上举时的上拉力。"
))
A.append(tcap("表 1　进入Ⅱ期（主动活动与肌耐力）的标准"))
A.append(table(
    ["标准", "达标值"],
    [
        ["疼痛", "<3/10"],
        ["Quick DASH 评分", "<60%"],
        ["被动活动度", "前屈 120°；外展 90°；外旋 30°"],
        ["能否完成“肩胛时钟”", "能（后缩、前伸、上提、下沉，代偿极少）"],
    ],
))

A.append(h3("❇️四、Ⅱ期：主动活动与肌耐力（约 5～6 周起）"))
A.append(p(
    f"目标是恢复正常主动活动度、提高肩袖和肩胛周围肌耐力、建立正常肩肱节律。此时修复处仍在愈合初期，"
    f"{u('继续避免后方负荷和手臂离开身体时的内旋')}。"
))
A.append(h4("🔻主动助力（AAROM）"))
A.append(p(
    "在开始主动活动前约 1 周开始。先仰卧或俯卧（减少重力），用健侧手或木棍做前屈、外旋、内旋；"
    "再进阶到站立位，用滑雪杖或木棍辅助前屈，最好对着镜子，避免耸肩和胸椎后伸代偿。"
))
A.append(fig(1, "用滑雪杖或木棍做主动助力前屈（A 起始位，B 终末位）"))
A.append(h4("🔻主动活动（AROM）"))
A.append(p(
    f"通常术后 {b('第 6 周')}开始，此时可以{b('去掉吊带')}、做轻度日常活动。先选短力臂、仰卧位的动作，逐步过渡到站立。"
))
A.append(table(
    ["目标肌肉", "动作与进阶"],
    [
        ["冈上肌", "仰卧“敬礼”式（肩胛平面前屈、微屈肘缩短力臂）→ “躺椅进阶”（从半躺到坐起）→ 坐/站位“满罐”"],
        ["冈下肌、小圆肌", "侧卧外旋（这两块肌肉 EMG 激活最高）"],
        ["肩胛下肌", "站立 0° 外展位内旋 → 90° 外展位内旋"],
        ["肩胛下肌、冈上肌、冈下肌", "俯卧 90° 外展位外旋"],
        ["中斜方肌、菱形肌", "俯卧划船"],
        ["冈上肌、下斜方肌、三角肌后束", "俯卧“满罐”"],
        ["前锯肌", "仰卧肩前屈 90° 做肩胛前伸（“仰卧出拳”）"],
    ],
))
A.append(fig(2, "半躺位“敬礼”练习（A 起始位，B 终末位）"))
A.append(fig(3, "侧卧外旋（A 起始位，B 终末位）"))
A.append(fig(4, "俯卧 90° 外展位外旋（A 起始位，B 终末位）"))
A.append(p(
    f"这一阶段还可以加入仰卧开链训练和{b('本体感觉神经肌肉促进（PNF）')}，例如治疗师在“仰卧出拳”时给予外部扰动，做节律性稳定训练。"
))
A.append(fig(5, "“仰卧出拳”加外部扰动"))
A.append(h4("🔻软组织处理"))
A.append(ul([
    "后方修复后常见后关节囊僵硬、前方肌肉缩短",
    "术后 6 周后可做轻柔的向后、向下关节松动，分别帮助改善内旋和外展",
    "术后约 7 周可开始低负荷长时间牵伸",
]))
A.append(tcap("表 2　进入Ⅲ期（初期抗阻）的标准"))
A.append(table(
    ["标准", "达标值"],
    [
        ["疼痛", "主动活动时 <3/10"],
        ["Quick DASH 评分", "<40%"],
        ["主动活动度", "前屈 120°；外展 120°；外旋 45°"],
        ["肩胛运动障碍测试", "肩胛运动正常"],
        ["重复主动活动疲劳测试", "以下动作各能完成 20 次：肩胛平面上举到 90°；外展到 90°；侧卧外旋到 0°"],
    ],
))

A.append(h3("❇️五、Ⅲ期：初期抗阻（≥8 周）"))
A.append(p(
    f"此时盂唇处于愈合后期，可以承受初步负荷。在Ⅱ期动作上{b('加弹力带或轻哑铃')}："
))
A.append(ul([
    "侧卧外旋加哑铃",
    "弹力带或拉索站立内旋、外旋",
    "弹力带站姿划船（中斜方肌、菱形肌）",
    "俯卧 90° 外展位外旋加重量",
    "俯卧“满罐”加哑铃（冈上肌、下斜方肌、三角肌后束）",
    "“仰卧出拳”加哑铃；站立泡沫轴靠墙滑动（肩上举 >90°，前锯肌激活好），手腕套弹力带增加后方肩袖激活",
]))
A.append(fig(6, "俯卧“满罐”练习（A 起始位，B 终末位）"))
A.append(fig(7, "站立泡沫轴靠墙滑动，手腕套弹力带（A 起始位，B 终末位）", "78%"))
A.append(tcap("表 3　进入Ⅳ期（进阶强化）的标准"))
A.append(table(
    ["标准", "达标值"],
    [
        ["Quick DASH 评分", "<20%"],
        ["主动活动度（前屈、外展、外旋）", ">健侧的 90%"],
        ["徒手肌力或手持测力计：满罐、外展、压腹试验、0° 外旋、0° 内旋", "所有方向 ≥4/5，或测力计 >健侧 80%"],
    ],
))
A.append(p("另外，日常活动应完全无痛，Ⅲ期所有力量训练都能顺利完成。"))

A.append(h3("❇️六、Ⅳ期：进阶强化与爆发力（约 3 个月起）"))
A.append(h4("🔻进阶强化"))
A.append(p(
    f"此时后方盂唇和关节囊被认为已经愈合，可以承受更大负荷。重点是{hl('在后方负荷下的控制')}："
))
A.append(ul([
    "站立抗阻外旋：肩外展 45° → 90°",
    "站立 90° 外展位抗阻内旋（肩袖、三角肌后束、中下斜方肌 EMG 都高）",
    f"{b('闭链训练')}：“仰卧出拳”变成闭链的{b('俯卧撑加（push-up plus）')}，从靠墙 → 地面 → BOSU 球",
    "静态俯卧撑加姿势下的节律性稳定和外部扰动 → 平板支撑交替拍肩",
    f"{red('注意')}：避免肱骨头过度向后移位，保持肩胛贴住胸廓",
]))
A.append(fig(8, "俯卧撑加，同时施加外部扰动", "78%"))
A.append(tcap("表 4　进入爆发力训练的标准"))
A.append(table(
    ["标准", "达标值"],
    [
        ["徒手肌力或手持测力计：满罐、外展、90° 外旋、90° 内旋", "所有方向 5/5，或测力计 >健侧 90%"],
        ["手持测力计 90° 位外旋/内旋比值", ">70%"],
    ],
))
A.append(h4("🔻爆发力训练（约 5 个月起）"))
A.append(p(
    f"增强式训练比单纯等张训练更能提高肩部爆发力、耐力、关节位置觉和投掷力量。进阶顺序："
))
A.append(ul([
    "双手药球胸前传球（对回弹网）→ 提高肩上举高度 → 单手传球",
    f"{b('反向接球')}：治疗师从身后抛轻球，患者接住并减速，训练肩带肌群的离心减速能力",
    "增强式俯卧撑：先靠墙，再到地面",
]))
A.append(fig(9, "反向接球的进阶（A→B→C）"))

A.append(h3("❇️七、Ⅴ期：重返运动"))
A.append(tcap("表 5　重返运动的功能测试标准"))
A.append(table(
    ["功能测试", "达标值"],
    [
        ["药球靠墙增强式弹击", "2 磅药球，以每分钟 165 拍的节奏完成 60 秒"],
        ["单臂推铅球", "6 磅球，推出距离 >健侧的 90%"],
        ["闭链上肢稳定性测试（CKCUEST）", "15 秒内 >21 次"],
        ["上肢 Y 平衡测试", ">健侧距离的 90%（标准化得分）"],
    ],
))
A.append(p(
    f"通过测试后，由{b('医生和物理治疗师共同决定')}能否开始专项训练（如投掷程序），以关节激惹程度作为进阶指导；"
    f"休息日继续做柔韧性、心肺耐力、上肢和核心的维持训练。"
))

A.append(h2("⚖️ 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：5 级专家意见，方案结合了作者经验与 EMG 等研究证据，没有在后方稳定术后人群中做过对照验证",
    f"{b('外旋/内旋比值前后不一')}：正文说正常肩的比值为 60%～70%，表 4 却要求 >70%，读者应注意",
    f"{b('时间与标准并用')}：各阶段既给了时间（6 周、8 周、3 个月、5 个月），又给了标准，两者冲突时原文没有说明以哪个为准；建议以“时间下限 ＋ 达标”同时满足为宜",
    f"{b('个体化')}：作者强调方案需根据术中所见（组织质量、修复大小、合并损伤）与主刀医生沟通调整",
    f"{b('利益冲突')}：部分作者与 Arthrex 等器械公司有经济往来（与本文无直接关系）",
]))

A.append(h2("📌 总结：先护后方，再练控制"))
A.append(p(
    f"{red('① Ⅰ期 0～6 周')}：吊带＋外展枕，PROM 前屈 ≤120°、外展 ≤90°、外旋 ≤30°，禁止后方负荷<br>"
    f"{red('② Ⅱ期 5～6 周起')}：AAROM → AROM，激活肩袖和肩胛肌，PNF 节律性稳定<br>"
    f"{red('③ Ⅲ期 ≥8 周')}：弹力带、轻哑铃抗阻，QuickDASH <40% 才能进入<br>"
    f"{red('④ Ⅳ期 ~3 个月')}：闭链俯卧撑加、扰动训练；~5 个月开始增强式训练<br>"
    f"{red('⑤ Ⅴ期')}：药球弹击、推铅球、CKCUEST、Y 平衡四项达标后重返运动<br>"
    f"{red('⑥ 关键')}：前锯肌和肩胛下肌是后方稳定的重点"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Goldenberg BT, Goldsten P, Lacheta L, Arner JW, Provencher MT, Millett PJ. Rehabilitation Following Posterior "
    "Shoulder Stabilization. Int J Sports Phys Ther. 2021;16(3):930-940. PMCID: PMC8168996.</em><br>"
    "文中图片均来自原文，表 1～5 已译为中文，仅用于学术交流。"
))

TITLE = "「肩关节」后方稳定术后怎么练？五阶段标准化康复方案"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>后方稳定术后康复推文</title>
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
