#!/usr/bin/env python3
"""髋关节镜翻修术后基于标准的康复（Leo 2023）推文。

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


def crit(t):
    return (f'<section style="margin:0 0 16px;padding:10px 12px;border-left:3px solid {RED};background-color:#fbf3f5;">'
            f'<p style="margin:0;font-size:14px;line-height:1.75;color:{TEXT};"><strong style="color:{RED};">进阶标准</strong><br>{t}</p></section>')


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2023 年第 18 卷第 2 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Criteria-Based Rehabilitation Following Revision Hip Arthroscopy: A Clinical Commentary（髋关节镜翻修术后基于标准的康复：临床评论）",
    f"{b('作者')}：Haley Leo, PT, DPT · Trevor Shelton, MD, MS · Helen Bradley, PT, MSc, SCS, CSCS",
    f"{b('机构')}：Howard Head 运动医学中心（美国科罗拉多州）",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2023;18(2):477-492",
    f"{b('PMCID')}：PMC10069339",
    f"{b('文章类型')}：临床评论 / 当前概念综述",
    f"{b('证据级别')}：5 级",
    f"{b('关键词')}：criteria-based · rehabilitation · revision hip arthroscopy · physical therapy",
], square=True))

A.append(h2("🎯 背景：翻修越来越多，康复却没有专门方案"))
A.append(p(
    f"髋关节镜手术近年快速增加，{b('4%～10%')} 的初次手术最终需要翻修，初次与翻修之间平均约 {b('2 年')}。"
    f"翻修最常见的原因是{b('残留骨性撞击')}（术前影像中近 {b('80%')} 有此表现）、盂唇撕裂、软骨损伤、微不稳和过度瘢痕。"
))
A.append(p(
    f"微不稳可能来自 FAI 本身，也可能是软组织不足造成的——盂唇清理后功能不全、关节囊切除、骨性撞击{b('切除过多')}。过度的生理活动会成为疼痛源，并让关节囊和盂唇进一步受损。"
))
A.append(ul([
    "Thorborg 等：初次术后 1 年功能有临床意义的改善，但仍不及健康人",
    f"做髋关节镜的外科医生中，{b('不到 30%')} 会给患者康复方案；而且支具、负重、活动度限制、重返时间差异很大",
    f"ACL 领域：采用基于标准的进阶，再伤风险可降低 {b('4 倍')}；肩稳定术后，很多人到了“预期恢复时间”仍未通过标准测试",
]))
A.append(p(
    f"翻修患者往往{b('疼了几个月甚至几年')}，代偿模式根深蒂固，组织愈合也不一定按常规时间表走。"
    f"因此作者提出一套{hl('以标准为主、兼顾时间')}的五阶段康复进阶：{b('保护 → 耐力 → 力量 → 爆发力 → 重返运动')}。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["阶段", "重点", "训练参数", "进入下一阶段的关键标准"],
    [
        ["Ⅰ 保护", "保护愈合组织、控制肿痛、在限制内恢复活动度、激活臀肌", "—", "侧卧臀中肌保持 30 秒；单腿站立 >10 秒骨盆不下沉；活动度达正常 90%"],
        ["Ⅱ 耐力", "正常步态、日常活动、肌耐力", "3 组 × 15～20 次，每周 2～3 次", "等长伸/外展/旋转 LSI 80%、屈髋 50%；Y 平衡前向差 <8 cm；正常步态 10 分钟"],
        ["Ⅲ 力量", "加大负荷，臀肌和深层外旋肌", "3～6 组 × 3～5 次，60%～80% 1RM（RPE 6～8/10）", "屈髋 LSI 80%、其余 90%；膝屈伸 >90%；Y 平衡前向差 <4 cm"],
        ["Ⅳ 爆发力", "发力速率、增强式训练", "3 组 × 3～6 次，轻中负荷，每周 2～3 次", "等长力量 LSI >90%；三级跳、垂直跳 >90%；Vail 测试 >17/20"],
        ["Ⅴ 重返运动", "专项动作，逐步回到比赛", "—", "T 型敏捷测试 LSI 90%；医疗团队同意"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('翻修患者别按时间表走——每一阶段都用客观标准把关，边练边纠正多年的代偿模式')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、FAI 与翻修手术"))
A.append(table(
    ["FAI 类型", "特点", "常见损伤"],
    [
        ["凸轮型（cam）", "股骨头非球形，屈髋时撞击", "盂唇撕裂或从髋臼缘撕脱，髋臼软骨损伤"],
        ["钳夹型（pincer）", "髋臼过度覆盖，可伴髋臼过深或后倾", "盂唇退变、骨化，股骨头颈部软骨损伤"],
        ["混合型", "两者兼有", "盂唇及髋臼和/或股骨头颈软骨损伤"],
    ],
))
A.append(p("FAI 常伴髂前下棘撞击、髂腰肌撞击、运动性耻骨痛、圆韧带撕裂等。"))
A.append(h4("🔻翻修手术怎么做"))
A.append(ul([
    f"目标：恢复盂唇的{b('“负压密封”')}功能和髋关节生物力学，减少活动时的压应力、保护软骨",
    "多数翻修病例盂唇与关节囊之间有粘连，需要术中处理",
    f"盂唇怎么处理取决于质量：质量好、粘连少 → {b('修复')}；有环形纤维但不足 → {b('增强')}（保留神经和血供，利于移植物愈合）；没有环形纤维 → {b('重建')}（节段或全周，自体或异体移植物）",
    f"同期处理合并问题：切除不足者{b('补充骨成形')}；切除过多者用{b('填充术（remplissage）')}，取髂胫束或阔筋膜张肌填补；处理软骨缺损、松解粘连、修复或重建关节囊缺损",
    "关节囊盂唇隐窝血供丰富、易粘连，粘连严重者可能需要在盂唇与关节囊之间放“间隔移植物”",
]))

A.append(h3("❇️二、第一阶段：保护期"))
A.append(p(
    f"目标：{b('保护愈合组织')}（支具、活动度限制、负荷管理）、控制炎症和疼痛、在限制范围内最大化活动度以减少粘连、开始肌肉激活，并恢复睡眠、精力、情绪、营养等基础状态。"
))
A.append(ul([
    "限制伸髋和外旋：减少前关节囊、盂唇修复和切口的张力；限制主动屈髋：减少屈髋肌负担",
    f"负重减少，具体由术者决定；与初次手术相比，限制负重的时间可能更长，{b('尤其做了微骨折时')}",
    "各项限制高度个体化，应按每位患者的术后限制来安排活动度、负重和训练",
]))
A.append(tcap("表1　翻修髋关节镜常见手术组合与术后限制"))
A.append(table(
    ["项目", "翻修髋关节镜（含盂唇修复/增强、填充术、关节囊折叠等）", "翻修 + 微骨折", "翻修 + 臀中肌修复"],
    [
        ["活动度限制", br(["屈髋：2 周内不坐到 90°；不做主动屈髋", "伸髋：17 天内不超过中立位", "外旋：21 天内不超过中立位", "外展：0°～45°，14 天", "内收：不限", "内旋：不限"]),
         br(["屈髋：2 周内不坐到 90°；不做主动屈髋", "伸髋：17 天内不超过中立位", "外旋：21 天内不超过中立位", "外展：0°～45°，14 天", "内收：不限", "内旋：不限"]),
         br(["屈髋：2 周内不坐到 90°；不做主动屈髋", "伸髋：17 天内不超过中立位", "外旋：21 天内不超过中立位", "外展：10°～30°至 45°，21 天", "内收：21 天内不超过外展 10°～30° 位", "内旋：不限"])],
        ["支具", "17 天", "17 天", "17 天"],
        ["负重", "20 磅 × 10～14 天，然后逐步撤拐", "20 磅 × 约 6 周，然后逐步撤拐", "20 磅 × 10～14 天，然后逐步撤拐"],
        ["体位", "4 周内不俯卧，避免牵拉前关节囊", "4 周内不俯卧，避免牵拉前关节囊", "4 周内不俯卧，避免牵拉前关节囊"],
    ],
))
A.append(small("本表列出作者常见的翻修手术组合及其限制；20 磅约 9 kg。"))
A.append(h4("🔻控制肿痛与粘连"))
A.append(ul([
    "翻修手术时间长，术后关节积液明显，会通过关节源性和神经源性抑制影响肌肉激活",
    f"手法治疗如{b('淋巴引流按摩')}帮助消肿；{b('CPM')} 使关节内压力周期性变化，起到“泵”的作用，把血液和水肿液带离关节",
    "拆线后做瘢痕松动，预防粘连",
    f"{b('被动环转')}是术后早期标准做法：不做环转的髋，瘢痕形成增加 {b('4.1 倍')}",
    "氯沙坦（Losartan）越来越多用于髋部术后：改善软骨缺损，并通过阻断 TGF-β1 减少术后纤维化",
]))
A.append(pic(2, "图1：四点跪位后坐（Quadruped Rock Backs）——从四点跪位移动到婴儿式，再到改良平板支撑位，用于在多数手术限制范围内做髋的主动活动"))
A.append(h4("🔻臀肌激活与代偿模式"))
A.append(ul([
    f"维持额状面骨盆稳定所需的外展力，{b('70%')} 来自止于大转子的肌肉",
    "步态中伸髋越大，髋前方受力越大；臀肌伸髋力量和髂腰肌屈髋力量下降，都会增加髋前方关节受力",
    f"常见代偿：{b('臀大肌弱 + 腘绳肌、腰伸肌过度活跃')}；{b('臀中肌弱 + 阔筋膜张肌过度活跃')}；深层髋旋转肌和前侧核心无力",
    "让患者自评“哪里在发力/哪里累”，能帮助识别代偿，也提高对动作的内在觉察",
]))
A.append(pic(3, "图2：臀推——高跪于治疗床尾，踝放在床外以求舒适；臀部坐向足跟（可垫枕头），然后激活臀肌伸髋。可加药球增加动态负荷和核心激活（解除负重限制后使用）"))
A.append(ul([
    "训练从辅助主动过渡到主动活动，重点是肌肉激活正确",
    f"组织愈合允许后，{b('术后 2 周')}可以开始主动屈髋",
    f"腰大肌常被认为“用得太多”，但它对屈髋和日常活动很重要。{b('髋滚球')}（图3）用于促进腰大肌次最大激活：触诊发现越偏外越偏股直肌，越偏内越偏腰大肌",
]))
A.append(pic(4, "图3：髋滚球——仰卧，双腿放在大球上，激活髂腰肌把球向内拉（凭经验触诊位置更偏内侧），可用手触诊肌肉激活"))
A.append(crit("臀中肌侧卧保持 30 秒；臀大肌俯卧伸髋 10 次；腹横肌激活 1 分钟（触诊下）；单腿站立 >10 秒对侧髋不下沉；各方向活动度达正常的 90%（外旋和屈曲达 75%，因早期有手术限制）。<br>这一阶段不适合测力计，所以用俯卧伸髋、腹横肌激活和侧卧保持来评估肌肉功能，并发现腘绳肌、背阔肌、屈髋肌的代偿。"))
A.append(pic(5, "图4：基于标准的进阶流程图（原图为英文，已按原内容中文重绘）", "92%"))

A.append(h3("❇️三、第二阶段：耐力期"))
A.append(p(
    f"重点是建立肌耐力，使患者能无痛、无代偿地完成日常活动。目标：主动活动度与健侧一致，髋部肌耐力足以过渡到{b('完全负重、无痛性步态')}，并重建关节和组织对负荷的耐受。"
    f"训练按耐力参数：{b('3 组 × 15～20 次，每周 2～3 次')}。"
))
A.append(ul([
    f"用 {b('FABER（屈曲-外展-外旋）')}体位逐步恢复功能性外旋，并重新适应以前诱发疼痛的姿势；腰大肌张力或保护性紧张可用 PNF 的轻柔收缩-放松，利用交互抑制缓解",
    f"轻柔关节松动可调节疼痛；使用高级别松动前，要先确认受限是{b('关节囊性而非骨性')}——比较伸髋位（关节囊紧张）和屈髋位（肌肉紧张）的内外旋差异",
    "内收肌、腰大肌、阔筋膜张肌的疼痛和高张力容易被忽视，需要手法处理",
    f"{b('步态')}：负重增加要循序渐进，可用体重秤控制负重百分比；从双拐到单拐可能需要数周；泳池步行、水中跑台、减重跑台、TRX 都能逐步加载。{red('撤拐要按标准，不按时间')}",
    "单腿平衡中加入神经认知任务；开链训练加阻力，近端稳定后加入闭链训练；监测疲劳部位和过用信号",
    f"教育患者{b('“微剂量”安排日常活动')}：把任务分散到一天或几天完成，减少微炎症（它会引起关节源性抑制）",
    f"Bergmann 等体内测量：以 4 km/h 行走时髋关节负荷为体重的 {b('238%')}，上楼 {b('251%')}，下楼 {b('260%')}；步速加快和跑步还会更高",
]))
A.append(crit("等长伸髋、外展、内旋、外旋 LSI 80%；等长屈髋 LSI 50%；侧平板支撑 1 分钟、LSI 90%；FABER（膝到床面距离，cm）LSI 90%；Y 平衡前向伸够两侧差 <8 cm；正常步态行走 10 分钟。<br>等长测试首选手持测力计，没有时以标准体位徒手肌力 4 级代替。Y 平衡前向两侧差 >4 cm 能预测损伤，但作者认为此阶段先用 <8 cm 作为可达成的目标。"))
A.append(pic(6, "图5：侧向躯干耐力测试——侧卧，以肘和（理想情况下）足撑起身体离开床面；与“侧平板支撑 + 髋外展”训练的体位相同，变容易后可抬起上方腿，增加双侧髋外展肌激活和核心稳定挑战"))

A.append(h3("❇️四、第三阶段：强化期"))
A.append(ul([
    f"训练参数：{b('3～6 组 × 3～5 次，60%～80% 1RM')}（新手到有经验者）",
    f"激活 ≥40%～60% MVIC 才有强化效果，约 {b('70%')} 最理想（增肌）",
    f"康复中测 1RM 困难且可能不安全，可用{b('主观用力程度（RPE）')}监控：60%～80% 1RM 约等于 RPE {b('6～8/10')} 或 {b('14～17/20')}",
    "本阶段后期加快动作速度，引入发力速率（RFD）训练，帮助患者建立快速移动的信心、减少恐惧，为爆发力期做准备",
    f"内外旋肌都要强化，尤其{b('深层外旋肌')}：Tateuchi 等发现深层外旋肌弱时深蹲髋前方受力增加；Meinders 等发现最大激活深层外旋肌可减小髋接触力角度和髋臼负荷（图6、图7）",
    f"{b('侧平板支撑 + 髋外展')}的臀中肌激活最高（{b('103% MVIC')}），所以用它作为测试",
]))
A.append(tcap("表3　常用训练中臀中肌和臀大肌的激活（%MVIC）"))
A.append(table(
    ["训练（臀中肌）", "Boren", "Distefano", "Ekstrom"],
    [
        ["四点跪伸髋（运动侧）", "22.03", "", "42 ± 17"],
        ["蚌式开合（屈髋 45°）", "47.23", "40 ± 38（屈髋 30°）<br>38 ± 29（屈髋 60°）", ""],
        ["单腿硬拉", "56.08", "58 ± 25", ""],
        ["侧卧髋外展", "62.91", "81 ± 42", "39 ± 17"],
        ["反向蚌式（伸髋 0° + 髋外展至中立）", "76.88", "", ""],
        ["*单腿蹲", "82.26", "64 ± 24", ""],
        ["*侧平板支撑（同侧）", "103.11", "", "74 ± 30"],
    ],
))
A.append(table(
    ["训练（臀大肌）", "Boren", "Distefano", "Ekstrom"],
    [
        ["站立臀肌夹紧", "80.72", "", ""],
        ["蚌式开合（屈髋 45°）", "53.10", "34 ± 27（屈髋 30°）<br>39 ± 34（屈髋 60°）", ""],
        ["单腿臀桥（稳定侧）", "54.24", "", "40 ± 20"],
        ["单腿硬拉", "58.84", "59 ± 28", ""],
        ["侧卧髋外展", "51.13", "39 ± 18", "21 ± 16"],
        ["*前平板支撑 + 伸髋", "106.22", "", "9 ± 7（不伸髋）"],
        ["*单腿蹲", "70.74", "59 ± 27", ""],
    ],
))
A.append(small("MVIC：最大自主等长收缩；* 表示按 Boren 等的数据，臀中肌和臀大肌激活均 >70%。"))
A.append(pic(7, "图6：侧卧深层外旋肌训练——目标腿在下，与躯干成一直线；收紧臀部深层启动，以髋为轴旋转把足抬离床面；提示下方膝始终贴床，减少内收肌参与"))
A.append(pic(8, "图7：单腿抬髋 + 旋转——靠墙站立，髋与墙之间夹大球并保持压力；躯干前倾约 45°，非支撑腿与躯干成一直线；以支撑腿为轴转动骨盆，躯干、骨盆和对侧腿保持一体"))
A.append(crit("等长屈髋 LSI 80%；等长伸髋、外展、外旋、内旋 90%；膝屈/伸力量 LSI >90%；侧平板支撑 + 髋外展 10 次；Y 平衡前向伸够两侧差 <4 cm。"))

A.append(h3("❇️五、第四阶段：爆发力期"))
A.append(p(
    f"能否进入这一阶段取决于三点：{b('① 髋部手术和翻修的次数；② 患者期望；③ 术者期望')}。三者一致且达到第三阶段标准，才进入爆发力训练。"
))
A.append(ul([
    "多次翻修者，长期肌肉抑制、代偿模式、关节异常负荷和心理社会因素都会增加回到高水平活动的难度，应调整期望",
    f"{red('关节间隙 <2 mm')} 者翻修后远期效果差，日后更可能需要全髋置换；是否回到高强度活动，要与医疗团队讨论关节间隙和微骨折史",
    f"训练参数：{b('轻中负荷，3 组 × 3～6 次')}，强调发力速率；每周 2～3 次，在同一次训练中先做爆发力、后做力量",
    "增强式训练从双腿、低冲击开始（如蹬踏机、TRX，先延长缓冲期），再逐步加快、加外部阻力，进阶到跳下落地；矢状面 → 额状面 → 多平面",
    "双腿跳在体重及以上负荷都控制良好后，才进阶到单腿弹跳、单腿跳",
    f"{b('Vail 髋运动测试')}在撞击角度加载髋关节，评估组织耐受和动作模式：单膝屈曲、侧向敏捷、斜向敏捷、向前箱式弓步；成绩与伸髋和外旋力量相关",
    "三级跳和垂直跳在 ACL 重建后信度好，可推广到其他下肢问题，方便比较两侧爆发力",
]))
A.append(crit("等长伸髋、外展、外旋、内旋、屈髋 LSI 保持 >90%；单腿三级跳远 >90%；单腿垂直跳 >90%；Vail 运动测试 >17/20 分。"))

A.append(h3("❇️六、第五阶段：重返运动"))
A.append(ul([
    "进入时机高度个体化：取决于既往史、手术复杂程度、术者和团队意见、患者目标",
    f"建议：力量和爆发力测试 {b('LSI ≥90%')}，加上 {b('T 型敏捷测试')}（评估下肢速度、爆发力和敏捷，信效度好）",
    "结合测试中的动作质量和团队的临床判断；与患者、教练、医疗和体能人员充分沟通",
    f"专项训练进阶：{b('单独专项动作 → 非对抗训练 → 对抗训练 → 队内比赛/训练 → 无限制比赛')}",
]))
A.append(tcap("表2　各阶段训练进阶"))
A.append(table(
    ["类别", "第一阶段", "第二阶段", "第三阶段", "第四阶段", "第五阶段"],
    [
        ["复合动作", br(["猫牛式", "四点跪位后坐", "站立弹力带末端伸膝", "站立外展内旋"]),
         br(["蹬踏机/TRX 深蹲", "重心转移", "深蹲", "平衡", "双任务平衡", "神经认知任务"]),
         br(["弓步", "单腿蹲", "平衡深蹲", "硬拉", "侧向下台阶"]),
         br(["抗阻单腿蹲", "侧向/斜向敏捷", "上台阶 + 提膝", "跳箱", "单腿硬拉"]),
         br(["敏捷梯", "多平面动作", "专项非对抗训练"])],
        ["伸髋", br(["四点跪伸髋"]), br(["鸟狗式", "臀推", "臀桥"]), br(["单腿臀桥"]), "", ""],
        ["髋外展", br(["站立髋外展内旋"]), br(["侧卧深层外旋肌训练"]), br(["单腿抬髋"]), "", ""],
        ["外旋肌", br(["侧卧臀肌保持与踢腿", "反向蚌式", "蚌式至中立位"]), br(["侧向行走", "滑盘伸髋/外展", "侧平板支撑（+ 髋外展）"]), br(["单腿抬髋 + 旋转"]), "", ""],
        ["屈髋肌/核心", br(["侧卧辅助屈髋", "髋滚球", "腹横肌激活"]), br(["站立踏步", "抗阻髋滚球", "足跟拖拽", "跪姿平板支撑"]), br(["标准平板支撑"]), "", ""],
    ],
))
A.append(small("原表按行排列较松散，此处按类别和阶段整理；内容与原表一致。"))

A.append(h3("❇️七、心理因素"))
A.append(ul([
    "心理健康与髋部病变密切相关；有心理问题史者 FAI 术后结局更差，也可能是既往手术失败的因素之一，并提示早晚期都可能存在持续疼痛",
    f"Browning 等：髋关节镜术后{b('疼痛灾难化和运动恐惧')}者，1 年时重返运动结局差",
    f"评估工具：{b('Hip-RSI')}（由 ACL-RSI 改编，在髋关节镜术后人群中信效度良好）；SF-36、Tampa 运动恐惧量表（非髋术后专用）",
    "可结合疼痛神经科学教育，缓解恐惧和不良习惯",
    f"{b('自我效能')}：低自我效能与更高疼痛相关；高自我效能可提高依从性、改善功能、减轻疼痛。可通过替代经验、言语说服和正向强化提升；必要时转介心理医生",
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：5 级临床评论，基于作者机构经验和文献，没有患者结局数据验证",
    f"{b('亮点')}：专门针对翻修人群，给出不同手术组合的具体限制（表 1）、按阶段的训练清单（表 2）、训练的肌电依据（表 3）和每阶段的客观进阶标准（图 4）",
    f"{b('部分标准为作者经验')}：如 Y 平衡前向差 <8 cm、等长屈髋 LSI 50% 等，作者明确说明是“可达成”的阶段目标，尚未验证",
    f"{b('图表引用有误')}：正文写“图 4 展示早期活动度训练”，实际是图 1；写“图 1 展示爆发力期进阶标准”，实际是图 4；表 2 中侧卧深层外旋肌训练标注“图 5”，实际是图 6",
    f"{b('原文小瑕疵')}：Vail 测试第一项正文写“单膝屈曲”，流程图写“单腿蹲”；流程图中 “Diagnoal”“Agiltiy” 拼写错误；第三阶段等长伸髋等标准写“90%”未注明 LSI；正文作者 Cheng/Chang 混用",
    f"{b('Vail 测试分数')}：流程图要求 >17/20，但未说明分数来源和计分方法",
]))

A.append(h2("📌 总结：髋关节镜翻修术后五阶段"))
A.append(p(
    f"{red('① 保护期')}：按手术组合遵守限制（伸髋、外旋、负重、不俯卧）；消肿、被动环转防粘连；激活臀肌，2 周后开始主动屈髋<br>"
    f"{red('② 耐力期')}：3 × 15～20；按标准撤拐，正常步态 10 分钟；“微剂量”安排日常活动<br>"
    f"{red('③ 强化期')}：60%～80% 1RM（RPE 6～8）；重点臀肌和深层外旋肌；侧平板支撑 + 外展<br>"
    f"{red('④ 爆发力期')}：结合翻修次数、患者和术者期望决定；先双腿后单腿；三级跳、垂直跳 >90%，Vail >17/20<br>"
    f"{red('⑤ 重返运动')}：力量和爆发力 LSI ≥90%、T 型敏捷测试，医疗团队同意<br>"
    f"{red('⑥ 贯穿始终')}：识别和纠正代偿，关注运动恐惧和自我效能"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Leo H, Shelton T, Bradley H. Criteria-Based Rehabilitation Following Revision Hip Arthroscopy: A Clinical Commentary. "
    "Int J Sports Phys Ther. 2023;18(2):477-492. PMCID: PMC10069339.</em><br>"
    "文中图片均来自原文：图 4 流程图按原内容中文重绘，其余照片无文字；表 1～3 已译为中文，仅用于学术交流。"
))

TITLE = "「髋关节」髋关节镜翻修术后怎么练？五阶段、按标准进阶"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>髋关节镜翻修术后康复推文</title>
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
