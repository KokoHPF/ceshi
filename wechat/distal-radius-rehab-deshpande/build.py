#!/usr/bin/env python3
"""Deshpande 等 2026《提高桡骨远端骨折康复的功能结局》（JOCR）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
配图：python3 tools/make_figs.py src/paper.pdf images <中文字体>（原文图都是照片，图内没有英文，不需要 fig-translate）
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






# ---------- 正文 ----------
def cap(t):
    return f'<p style="margin:0 0 20px;font-size:12px;line-height:1.6;color:#888;">🔖{t}</p>'


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
    "Deshpande SS, Ghodke PP, Kale SY, Brahmbhatt HM, Shah HM, Deshpande S. Enhancing Functional Outcomes in Distal End Radius Fracture Rehabilitation. J Orthop Case Rep. 2026;16(1):278-287. doi:10.13107/jocr.2026.v16.i01.6680",
    "中文题目：提高桡骨远端骨折康复的功能结局",
    "作者单位：印度 D. Y. Patil 大学物理治疗学院、医学院骨科等",
    f"文章类型：期刊标为原创文章，实际是{b('作者团队的分期康复方案介绍')}，没有患者数据，相当于专家意见",
], square=True))

A.append(h2("先说为什么要读这篇"))
A.append(p(
    f"桡骨远端骨折是最常见的骨折之一，{b('儿童青少年和老年人')}两头多见，两类人群的骨折类型、处理和并发症都不一样。"
    "这篇只讲成人。"
))
A.append(p(
    f"桡骨远端骨折术后或拆石膏后怎么练，{b('至今没有公认的标准方案')}。Cochrane 综述（Handoll 2015）的结论是各家方案五花八门，"
    f"没法只靠一套；但综述和指南都指向同一点：{mk('做一些训练，总比不做好')}，而且早开始通常更好。"
))
A.append(p(
    f"这篇的价值在于把{b('保守治疗、克氏针、掌侧锁定钢板')}三条路线各自分期写清楚：每期的目标、固定、负重、训练和辅助手段，"
    "并配了 10 张动作示范照片，拿来做患者宣教很方便。"
))

A.append(h2("评估看什么"))
A.append(ul([
    f"{b('影像')}：桡骨高度、桡偏角（尺偏角）、掌倾角、尺骨变异、有无尺骨茎突骨折、下尺桡关节是否增宽",
    f"{b('客观指标')}：腕关节活动度、握力、捏力",
    f"{b('患者自评')}：DASH（上肢功能障碍问卷）和 MHQ（密歇根手功能问卷）最常用",
]))

A.append(h2("三条路线一览"))
A.append(tcap("三种处理方式的分期（编者根据原文整理）"))
A.append(table(["路线", "第 0～4 周", "第 5～8 周", "第 8 周以后"], [
    ["保守", "长臂石膏（肘上到掌骨头）；2 周起腕被动活动", "夹板，每天摘 2～3 次练；助力 → 主动；8 周末开始轻抗阻", "9～12 周回归活动期，不再固定；≥ 12 周强化期"],
    ["克氏针", "石膏 2 周；不负重；2 周后次大等长", "部分负重；主动活动、关节松动 I～II 级、握力捏力", "完全负重；渐进抗阻、俯卧撑进阶"],
    ["掌侧锁定钢板", "石膏 2 周；不负重；2 周后腕被动活动", "仍不负重；4 周后助力活动", "部分到完全负重（按耐受）；抗阻、搬运、功能训练"],
]))
A.append(img(9))
A.append(small("时间节点是作者的经验做法，原文也说要按固定方式、患者依从性和术者意见调整"))

A.append(h2("保守治疗"))
A.append(h3("阶段 I：早期活动期（0～4 周）"))
A.append(p(f"石膏从{b('肘上一直打到掌骨头')}。这一期的重点是：护住骨折、消肿止痛、别让邻近关节僵、预防复杂区域疼痛综合征（CRPS）。"))
A.append(ul([
    f"{b('抬高患肢高于心脏')}，冷疗消肿",
    "轻捏球和各种抓握动作，练腕、指的长屈肌",
    "颈部和肩胛周围软组织松动：固定久了近端肌肉容易紧、弱",
    f"{b('腕屈伸肌次大强度等长收缩')}",
    "肩胛活动和后缩训练；肩、肘徒手抗阻；深呼吸和步行维持心肺",
    "肩、颈、肘、手指主动活动",
    f"{mk('2 周起')}开始腕、前臂和手的无痛被动活动",
]))

A.append(h3("阶段 II：主动活动期（5～8 周）"))
A.append(p(f"换成{b('复位后夹板')}，每天摘下来练 2～3 次。"))
A.append(ul([
    f"{b('消肿')}：压力手套、水肿松动手法、按摩、肌内效贴；没有肿胀时可以热敷放松前臂和手部肌肉",
    f"{b('预防 CRPS')}：脱敏训练（不同温度、质地、刺激）加上肢活动",
    f"{b('活动度')}：无痛的助力和主动活动；腕骨间、掌骨间、掌指关节 Maitland I～II 级松动；肌肉能量技术",
    f"{b('手功能')}：揉毛巾、手指爬行、{b('肌腱固定术式训练')}、{b('差异性肌腱滑动')}",
    "轻柔牵伸前臂屈伸肌和手内在肌；肩胛稳定训练（T、I、Y）",
    "大球顶墙的本体感觉训练，给上肢适度加压",
    f"{mk('第 8 周末')}开始轻抗阻：弹力棒、治疗泥、弹力带或小哑铃",
]))
A.append(img(2))
A.append(img(3))
A.append(img(4))
A.append(img(5))
A.append(img(6))
A.append(p(f"辅助：感应电刺激止痛、诱发主动收缩；电刺激防肌萎缩；低能量激光止痛。"))
A.append(img(7))

A.append(h3("阶段 III：回归活动期（9～12 周）"))
A.append(p("不再固定。前两期的训练按需继续，再加："))
A.append(ul([
    "腕屈伸肌、前臂肌、肱二头肌、肱三头肌牵伸",
    f"桡腕、腕骨间、掌指关节 {b('Maitland III～IV 级松动')}，改善关节附属运动",
    f"{b('四点跪位负重')}和 {b('BOSU 球上撑起')}，练上肢负重和本体感觉",
    "弹力带、哑铃练肘、前臂、腕力量；橡皮筋练指力；插板练精细动作",
]))
A.append(img(8))
A.append(p("辅助：神经肌肉电刺激、冲击波、Matrix 节律治疗（原文的证据见后文）。"))

A.append(h3("强化期（≥ 12 周）"))
A.append(ul([
    "目标：腕活动度和力量回到伤前水平，上肢本体感觉和平衡，专项技能",
    "弹力带、哑铃、等速设备做专项力量；游泳",
    f"{b('上肢增强式训练')}：先双侧后单侧",
    "战绳、出拳、投掷",
]))

A.append(h2("克氏针固定"))
A.append(h4("阶段 I：术后即刻期（0～4 周）"))
A.append(ul([
    f"术后{b('石膏 2 周')}，防止再移位；患肢{b('不负重')}",
    "抬高、冷疗 7～10 分钟、膈肌和节段呼吸、颈肩肘主动活动",
    "无痛范围内轻揉毛巾、手指爬行",
    f"{b('2 周后')}腕屈伸肌次大等长；肩肘徒手或沙袋抗阻",
    "注意早期并发症：骨筋膜室综合征、神经损伤",
]))
A.append(h4("阶段 II：中期（5～8 周）"))
A.append(ul([
    f"{b('部分负重')}；无痛主动活动；仍肿就继续抬高",
    "轻柔牵伸腕和手指，防手内在肌紧张；I～II 级关节松动",
    "海绵球练握力、弹力棒练屈伸腕、捏力练习、插板",
    "辅助：冷压设备、Matrix 节律治疗、冲击波、镜像疗法",
]))
A.append(h4("阶段 III：回归活动期（> 8 周）"))
A.append(ul([
    f"{b('完全负重')}；捏球、弹力带、小哑铃渐进抗阻；哑铃腕弯举；壶铃持握（等长）",
    "肌腱滑动和肌腱阻挡训练",
    f"负重进阶：{mk('前臂支撑俯卧 → 手撑 → 墙俯卧撑 → 桌面俯卧撑 → 地面俯卧撑')}",
    "辅助：等速训练、血流限制训练、水中训练",
]))

A.append(h2("掌侧锁定钢板"))
A.append(h4("阶段 I：术后即刻期（0～4 周）"))
A.append(ul([
    "向患者交代术后注意事项；防早期并发症和皮肤问题；防关节源性肌肉抑制",
    f"术后{b('石膏 2 周')}；{b('不负重')}；抬高、冷疗、呼吸训练、颈肩肘主动活动",
    f"{b('2 周后')}开始腕和手的无痛被动活动、腕屈伸肌次大等长",
]))
A.append(h4("阶段 II：中期（5～8 周）"))
A.append(ul([
    f"{b('仍不负重')}；{b('4 周后')}开始无痛助力活动",
    "腕和手指牵伸；I～II 级关节松动；握力、捏力和插板训练",
    "辅助：冷压设备、Matrix 节律治疗、功能性电刺激、冲击波、镜像疗法",
]))
A.append(h4("阶段 III：回归活动期（> 8 周）"))
A.append(ul([
    f"按耐受{b('部分到完全负重')}",
    "弹力带腕和前臂弯举；治疗泥、握力器、网球练抓握；肌腱滑动",
    "渐进加量的搬运、模拟日常活动、写字和捡小物件",
    f"划船、战绳练耐力；{b('药球投掷')}练爆发力",
]))

A.append(h2("讨论里说了什么"))
A.append(ul([
    f"{b('早期康复')}：作者引用 Zhou 2024 的荟萃分析，说术后 2 周内开始康复功能更好。编者查了这篇：只纳入{b('掌侧钢板术后')}的 7 项研究，"
    f"早期康复改善了上肢功能、腕背伸活动度和疼痛，但{b('腕关节功能评分和并发症没有差异')}",
    f"{b('有训练比没训练好')}：作者引用 2024 年美国物理治疗协会的桡骨远端骨折临床实践指南（Mehta 2024），不论方案是否标准化",
    f"{b('CRPS')}：仍是重要并发症，可能到康复后期才显现，全程都要盯；早期活动、脱敏和镜像疗法应该成为常规的一部分",
    f"{b('谁恢复得好')}：年龄、合并症、基线疼痛和抑郁等心理社会因素，可能比治疗方式和影像参数更能预测结局（原文这句没有给出处）",
    "激光、冲击波、神经肌肉电刺激等辅助手段证据还在积累，方案之间差异大，高质量证据有限",
]))

A.append(h2("这篇能信几分"))
A.append(ul([
    f"{b('证据等级低')}：没有研究对象、没有检索策略、没有结局数据，是作者团队的经验方案。期刊标为原创文章，摘要和正文还用了“材料与方法”标题，但内容是方案介绍",
    f"{b('辅助手段的证据偏弱')}：Matrix 节律治疗引的是两篇个案（其中一篇是胫腓骨骨折后膝僵硬）；冷疗引的是膝关节置换术后肿胀的综述；冲击波的证据来自骨折延迟愈合和不愈合，不是常规新鲜骨折",
    f"{b('钢板组的节奏偏保守')}：锁定钢板固定较稳，常被用来支持早期活动，原文却在钢板组安排 2 周石膏、8 周不负重，比克氏针组还慢，没有解释原因",
    "优点：三条路线分开写，每期目标、固定、负重和训练都具体到动作，配图清楚，适合给患者做宣教的底稿",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('许可声明自相矛盾')}：文字写“Creative Commons Attribution 4.0 International License”（CC BY 4.0），链接却是 CC BY-NC 4.0。本文按更严格的 BY-NC 处理",
    f"{b('保守治疗阶段 I 和石膏冲突')}：石膏从肘上打到掌骨头，但目标写“维持腕和指间关节活动度”，干预里有肘关节主动活动、肘部徒手抗阻，2 周起还有腕和前臂被动活动，这些在长臂石膏里都做不了；这一期还叫“早期活动期”",
    f"{b('克氏针阶段 I 同样冲突')}：前 2 周石膏固定，同时写“前 2 周做腕和手的无痛助力活动”；目标里还有“增加上肢和握力”，放在术后即刻期也不合适",
    f"{b('负重安排倒过来了')}：克氏针 5～8 周部分负重、8 周后完全负重；更稳的锁定钢板 5～8 周仍不负重、8 周后才“部分到完全”。克氏针组也没提什么时候拔针",
    f"{b('图号引错')}：钢板阶段 III 写“肌腱滑动训练（图 8）”，图 8 是电刺激，肌腱滑动是图 5",
    f"{b('时间段重叠')}：保守治疗阶段 III 是 9～12 周，强化期是 ≥ 12 周，第 12 周两期都算",
    f"{b('参考文献重复')}：[5] 和 [15] 是同一篇（Zhou 2024）",
    f"{b('Zhou 2024 用得太宽')}：引言说它显示早期康复“改善腕关节活动”，讨论又说术后 2 周内开始功能更好。这篇只纳入掌侧钢板术后的研究，腕关节功能评分没有差异；摘要里也没有“2 周”这个分界（编者未核对全文）",
    f"{b('镜像疗法“预防 CRPS”')}：引用的 Kotiuk 2019 研究的是{b('已经确诊 CRPS I 型')}的患者，属于治疗，不能直接说明可以预防",
    f"{b('冲击波用于“畸形愈合”')}：原文说冲击波用于骨折延迟愈合和畸形愈合，冲击波的证据针对的是延迟愈合和不愈合，它纠正不了畸形愈合",
    f"{b('激光“促进骨折愈合”')}：引用的 Sæbø 2022 随机对照试验是拆石膏后用激光减轻疼痛和功能障碍，没有评估骨愈合",
    f"{b('测量工具写成训练工具')}：“用握力计做腕部强化”“用捏力计改善捏力”，握力计和捏力计是用来测的",
    f"{b('血流限制训练练“爆发力”')}：血流限制训练用的是低负荷，主要练肌肥大和力量，和爆发力训练的目标不一致",
    f"{b('结论多出正文没有的内容')}：结论提到虚拟康复和疼痛科医生，正文都没讲",
    f"{b('无出处的绝对说法')}：“康复 1 年后，无论固定方式和制动时长，都能恢复完整的腕和前臂活动度”，没有引用，说得也太满",
    f"{b('名称不统一')}：图 6 图注叫“前庭球”，照片是普通健身球；正文写 Quadrupod，图 9 图注写 Quadruped（四点跪位）",
]))

A.append(h2("落到临床"))
A.append(img(10))
A.append(cap("临床要点（编者整理）"))
A.append(ul([
    f"{mk('第一天就开始动能动的')}：抬高、冷疗，肩、肘（不在石膏里时）、颈、手指主动活动，腕在石膏里先做次大等长",
    f"{b('5～8 周抓活动度')}：助力到主动，肌腱滑动、肌腱固定术式训练、低级别关节松动，同时盯肿胀和 CRPS",
    f"{b('8 周后加力量和负重')}：握力、捏力、抗阻；四点跪位到俯卧撑逐级加负重",
    f"{b('时间点按固定方式调')}：原文的周数是经验值，钢板组比克氏针组还保守；固定稳、复查好的，一般可以更早活动，最终听术者意见",
    f"{b('物理因子只当辅助')}：原文多数辅助手段的证据是个案或来自别的部位，不能代替主动训练",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Deshpande SS, Ghodke PP, Kale SY, Brahmbhatt HM, Shah HM, Deshpande S. Enhancing Functional Outcomes in Distal End Radius Fracture Rehabilitation. J Orthop Case Rep. 2026;16(1):278-287. doi:10.13107/jocr.2026.v16.i01.6680</em><br>"
    "编者核对引用时参考：Zhou Z, et al. BMC Musculoskelet Disord. 2024;25:198. doi:10.1186/s12891-024-07317-0；"
    "Kotiuk V, et al. Br J Pain. 2019;13(1):35-42. doi:10.1177/2049463718782544；"
    "Sæbø H, et al. Photobiomodul Photomed Laser Surg. 2022;40(1):33-41. doi:10.1089/photob.2021.0125（摘要信息来自 PubMed）<br>"
    "原文以知识共享署名—非商业性使用 4.0 协议（CC BY-NC 4.0）开放获取。本文为非商业学术交流用的中文解读：原文图 1～10 为照片，图内无文字，编者裁切后加了中文图注；"
    "表格、首图、时间轴和临床要点卡为编者根据原文整理。仅供学习交流，如有侵权请联系删除。"
))

def inline_imgs(html):
    """预览页里的图片改成 base64 内嵌：单个 preview.html 拿到哪里打开都能看到图。"""
    import base64
    import re
    mime = {".png": "image/png", ".gif": "image/gif"}

    def rep(m):
        f = HERE / m.group(1)
        return f'src="data:{mime.get(f.suffix, "image/jpeg")};base64,{base64.b64encode(f.read_bytes()).decode()}"'
    return re.sub(r'src="((?:images|gifs)/[^"]+)"', rep, html)


TITLE = "「桡骨远端骨折」保守、克氏针、钢板分别怎么练？三条路线分期康复，附原文对不上的地方"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>桡骨远端骨折康复推文</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
  :root { --ground:#ececec; --paper:#ffffff; color-scheme:light; }
  body { background:var(--ground); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
         padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:16px 32px; }
  .paper { max-width:640px; margin:0 auto; background:var(--paper); padding:20px 16px 28px; box-sizing:border-box; }
  .paper h1 { font-size:22px; line-height:1.4; margin:0 0 8px; color:#111; text-wrap:balance; }
  .paper .by { font-size:14px; color:#576b95; margin-bottom:20px; }
  .paper img { max-width:100%; }
  .paper table { display:block; overflow-x:auto; }
</style>
<div class="paper">
<h1>""" + TITLE + """</h1>
<div class="by">原创 · 骨科康复小黄</div>
""" + inline_imgs(BODY) + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
