#!/usr/bin/env python3
"""Bradley 等 2021《Latarjet 术治疗运动员肩前向不稳：康复要点》（IJSPT）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
配图：python3 tools/make_figs.py src/paper.pdf <work 目录> images <中文字体>（原文图 1、3、4 先用 tools/fig-translate 译成中文）
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
    "Bradley H, Lacheta L, Goldenberg BT, Rosenberg SI, Provencher MT, Millett PJ. Latarjet Procedure for the Treatment of Anterior Glenohumeral Instability in the Athlete – Key Considerations for Rehabilitation. Int J Sports Phys Ther. 2021;16(1):259-269. doi:10.26603/001c.18707",
    "中文题目：Latarjet 术治疗运动员肩前向不稳：康复要点",
    "作者单位：美国 Howard Head 运动医学中心、Steadman Philippon 研究所、Steadman 诊所；德国柏林夏里特医学院",
    f"文章类型：{b('临床述评')}，证据等级 5 级（专家意见）。进阶标准在原文附录 1 的流程图里",
], square=True))

A.append(h2("先说为什么要读这篇"))
A.append(p(
    f"盂肱关节是全身最容易脱位的关节，{b('九成以上是前脱位')}，年轻男性运动员最多见，"
    "橄榄球、冰球、摔跤这类对抗项目，以及滑雪、排球、体操这类容易摔倒的项目风险最高。"
))
A.append(p(
    f"关节盂前方骨缺损达到 {b('13.5%')} 以上时，单做软组织修复效果差，需要补骨。"
    f"{b('Latarjet 术')}就是把喙突连同附着的联合腱一起移到关节盂前下缘。术后稳定率和重返运动率都很高，"
    f"但解剖改变大，{b('术后活动度容易受限')}，而活动度受限又和远期骨关节炎有关。"
))
A.append(p(
    f"问题在于：Latarjet 术后怎么练、什么时候可以进阶，{b('一直没有统一、客观的标准')}。"
    f"这篇述评给了一套{mk('五阶段、按标准进阶')}的方案：每个阶段都列出达标条件，"
    "达标再往下走，而不是单纯按术后天数推进。"
))

A.append(h2("Latarjet 为什么能稳：三重效应"))
A.append(table(["效应", "怎么起作用"], [
    ["吊带效应", "联合腱在上臂外展外旋时，从下方兜住肩胛下肌下部和前下关节囊"],
    ["骨块效应", "关节盂前缘补了一块骨，前后径变大"],
    ["关节囊效应", "用喙肩韧带的一段加固下方关节囊"],
]))
A.append(p(
    f"尸体研究（Yamamoto 2013）：在外展外旋的末端位置，吊带效应贡献 {b('76%～77%')} 的稳定性，关节囊修复 23%～24%；"
    f"在中间位置，吊带效应 51%～62%，骨块 38%～49%。也就是说，{b('联合腱的吊带作用是主力')}，三者合在一起才稳。"
))

A.append(h2("手术怎么做，决定了康复要护什么"))
A.append(p(
    "标准三角肌胸大肌入路：把胸小肌和喙肩韧带从喙突上切下，用摆锯截下约 25 mm 长的喙突，保留联合腱；"
    f"顺着纤维方向{b('劈开肩胛下肌')}（在下 1/3 与中 1/3 交界处）和关节囊，"
    "关节盂前颈打磨出血后，用两枚 3.5 mm 螺钉把喙突骨块固定上去。"
))
A.append(img(2))
A.append(p(f"从这里能直接推出早期的两条禁忌："))
A.append(ul([
    f"{b('肩胛下肌被劈开、关节囊被修复')} → 早期{red('限制外旋')}",
    f"{b('联合腱（肱二头肌短头 + 喙肱肌）还连在喙突骨块上')} → 早期{red('不要抗阻屈肘、前臂旋后')}，否则会把骨块从关节盂上拉开",
]))

A.append(h2("五个阶段一览"))
A.append(tcap("Latarjet 术后康复五阶段（编者根据原文整理）"))
A.append(table(["阶段", "时间", "目标", "主要内容"], [
    ["I 保护期", "术后", "保护重建、控制肿胀、恢复被动活动", "外展吊带 4 周；前 3 周外旋 &lt; 30°；被动活动；肩胛主动训练；2 周后开始次大等长"],
    ["II 耐力期", "达标", "主动活动、肌耐力、神经肌肉控制", "助力 → 主动活动；15～25 次 × 2～3 组；关节位置觉、PNF、肩胛控制"],
    ["III 力量期", "≥ 6 周", "力量、神经肌肉控制", "8～12RM × 3～6 组；功能性和闭链训练；动力链；心理评估"],
    ["IV 爆发力期", "按需", "爆发力", "80%～100% 1RM × 3～6 次 × 3～6 组；上肢增强式训练"],
    ["V 重返赛场", "达标", "回到比赛", "专项训练；过顶项目做间歇投掷"],
]))
A.append(small("只有阶段 III 给了最早时间（术后 6 周），其余阶段都以达标为准。不需要爆发力、对抗或过顶动作的人，阶段 III 达标就可以带维持方案出院"))

A.append(h2("阶段 I：保护期"))
A.append(ul([
    f"{b('患者教育')}：讲清楚为什么要保护，依从性才有保证",
    f"{b('外展吊带固定 4 周')}",
    f"{b('早期被动活动')}防僵硬：{mk('前 3 周外旋限制在 30° 以内')}，其他方向不限，尽早练到全范围",
    "手法：胸肌等肩周肌群的肌筋膜技术、瘢痕松动；冷疗等理疗消肿止痛、助眠",
    "肩胛主动训练（前伸、后缩、上提、下沉，如“肩胛时钟”），手、腕、肘、颈的主动活动",
    f"{red('术后 0～2 周不做任何等长收缩')}，尤其不要在屈肘、旋后时负重",
    f"{b('2 周后')}：中立旋转位的次大强度、无痛等长；中立位节律稳定（治疗师在前臂近端给轻微振荡扰动，患者保持不动）",
]))

A.append(h2("阶段 II：耐力期"))
A.append(ul([
    f"{b('先助力后主动')}：主动活动从仰卧、侧卧、俯卧（减重力）开始，耐力好了再站着练",
    f"{b('练耐力的参数')}：{mk('15～25 次 × 2～3 组，负荷 &lt; 65% 1RM，组间休息 ≤ 30 秒')}，练到局部疲劳",
    f"{b('外旋恢复慢，但一定要练满')}：任何活动度欠缺都可能影响远期关节健康、诱发骨关节炎",
    "活动度恢复慢的，术后 5～6 周可以开始轻柔的盂肱关节松动；配合软组织松动和长时间牵伸",
]))
A.append(h4("神经肌肉控制从这一期开始抓"))
A.append(p(
    f"肩不稳患者的{b('关节位置觉')}本来就差，开放修复术后要到 {b('12 个月')}左右才恢复到和健侧一样。"
    "练法：闭眼，先把健侧摆到一个位置，再让患侧去对齐（图 2）。"
))
A.append(img(3))
A.append(ul([
    f"{b('关节角度复现测试（JART）')}：治疗师把患肢被动摆到某个角度，停留感受后放回中立位，患者主动复现，用量角器或倾角仪量误差。健康人平均误差约 2.7°。矢状面、冠状面、水平面都可以练",
    f"{b('PNF')}（如 D2 屈 / 伸）：在功能模式中练稳定和控制",
    f"{b('节律稳定往末端走')}，尤其针对内外旋肌，促进肩袖前后部共同收缩",
    f"{b('肩胛控制')}：斜方肌和前锯肌协同发力时肩胛最稳。俯卧 90° 水平外展加外旋、俯卧后伸、俯卧 125° 上举对肩胛周围肌群效果好；动态拥抱和靠墙滑动（图 3）前锯肌激活好",
]))
A.append(img(4))
A.append(p(f"进入阶段 III 前，用 {b('90° 以下的 JART、肩胛运动障碍测试（McClure 法）和主动活动疲劳测试')}评估，不能有代偿动作；同时做一次{b('下肢 Y 平衡')}，找出下肢的不对称。"))

A.append(h2("阶段 III：力量期"))
A.append(p(
    f"至少{b('术后 6 周')}、阶段 II 达标才能进入，进阶参数要和整个治疗团队沟通。"
    "这时要把运动员的专项需求过一遍：过顶项目要把力量练到需要的活动范围，并开始模拟专项动作。"
))
A.append(ul([
    f"{b('负荷')}：{mk('8～12RM × 3～6 组')}；徒手阻力、哑铃、药球、壶铃、弹力带都可以",
    "先分肌群练（外旋肌、内旋肌），有了基础力量再练日常和专项的功能动作",
    f"{b('对角线和动力链模式')}：抗阻 PNF（图 4）、Crossover Symmetry 等，肩胛肌激活最大",
]))
A.append(img(5))
A.append(ul([
    f"{b('动态稳定')}：反应性神经肌肉训练和闭链训练；节律稳定可以融入全范围的任何动作；手下垫瑞士球等不稳定面、加扰动",
    f"{b('闭链进阶')}：{mk('墙 → 桌面 → 四点跪位')}（图 5），负荷逐步加大，对肩胛控制很好",
    f"{b('“混沌”训练')}：杠铃两端用弹力带挂重物做过顶推举，增加不稳定和不可预测性",
    f"{b('动力链')}：近端稳定才能远端灵活、发力和精准。单腿蹲、分腿蹲、半跪、高跪位下加远端阻力，整合同侧和对侧的动力链",
]))
A.append(img(6))
A.append(h4("进阶检查的几个重点"))
A.append(ul([
    f"{b('临床检查无恐惧感')}",
    f"{b('总旋转弧（外旋 + 内旋）')}：过顶运动员优势侧外旋多、内旋少很正常，但两侧总弧应相同，约 180°",
    f"{b('力量')}：0° 外展位外旋、内旋，90° 外展、肩胛面上举和{b('腹压试验')}，肢体对称指数（LSI）≥ 80%。"
    f"{mk('腹压试验单独评估肩胛下肌')}，正好反映术中劈开的这块肌肉恢复得怎样",
    "肩胛运动障碍测试异常的，用手持测力计测肩胛周围肌力",
    f"{b('心理准备')}：用运动员恐惧回避问卷（AFAQ）筛查，有问题尽早转运动心理，否则可能成为后面最大的拖延因素",
]))
A.append(p(
    f"不需要爆发力、对抗或过顶动作的人，到这里可以带维持方案出院。需要的人，"
    f"力量要达到健侧 {b('90% 以上')}，并测 90° 外展位的外旋 / 内旋，算出 {b('ER/IR 比值')}，再进入阶段 IV。"
))

A.append(h2("阶段 IV：爆发力期"))
A.append(p(
    f"爆发力 = 力 × 速度。阶段 III 练的是力，这一期加入速度。原文给的剂量是 {b('80%～100% 1RM、3～6 次、3～6 组')}。"
    "功能训练器（缆绳）可以在多个平面自由运动，从 90/90 外旋爆发力练到全动力链的推拉（图 6）。"
))
A.append(img(7))
A.append(h4("上肢增强式训练怎么进阶"))
A.append(table(["类型", "进阶顺序"], [
    ["开链", "双手：胸前传球、左右侧抛、过顶足球掷 → 单手：站立单手抛、单手侧抛、90/90 拍墙（图 7）、俯卧落球"],
    ["闭链", "部分负重：靠墙增强式俯卧撑、普拉提床上肢跳跃（图 8）→ 全负重：增强式俯卧撑、跳深俯卧撑、击掌俯卧撑"],
]))
A.append(img(8))
A.append(h4("阶段 IV 结束时的测试"))
A.append(ul([
    f"{b('所有运动员')}：闭链测试（上肢 Y 平衡、CKCUEST、改良俯卧撑）评估稳定和耐力；需要的话加单臂坐位推球测爆发力。有常模的测试优先，因为健侧本身也可能退化，LSI 会虚高",
    f"{b('过顶运动员另加')}：90/90 拍墙测试（2 磅球，肩外展外旋 90°，按 165 次 / 分节拍器拍 60 秒，全程保持姿势和肩胛控制）、"
    "俯卧落球测试（2 磅球，30 秒内放球接球次数，和对侧比）",
    "改良引体向上和俯卧撑对投掷距离有预测价值（r 分别为 0.70 和 0.63）",
    f"复查{b('下肢 Y 平衡')}（两侧差 &lt; 4 cm）和 {b('FMS')}（原文目标 ≥ 14 分）",
]))
A.append(small("原文也承认：上肢的功能测试远不如下肢成熟，高质量证据少、没有金标准，这套测试组合是基于作者的临床经验"))

A.append(h2("阶段 V：重返赛场"))
A.append(ul([
    "先摸清项目和场上位置的要求",
    f"过顶运动员做{b('间歇投掷方案')}，逐步增加投掷数量、距离、强度和类型；{mk('之前至少完成 6 周增强式训练')}",
    "逐级回归：专项技术 → 无对抗训练 → 对抗训练 → 训练频率和强度逐步接近比赛，和教练一起定进度",
    f"能无痛完成全量训练或间歇投掷、投掷技术正常，才进比赛；过顶运动员 {b('KJOC 评分 ≥ 90')} 才回到比赛",
]))

A.append(h2("各阶段进阶标准"))
A.append(img(9))
A.append(small("原文附录 1 是英文流程图，编者译成中文并重新排版。QuickDASH 为上肢功能障碍问卷简版，分数越高功能越差"))

A.append(h2("这篇述评能信几分"))
A.append(ul([
    f"{b('5 级证据，专家意见')}：方案和进阶标准来自作者团队的临床经验，没有疗效数据，也没有和别的方案比过",
    f"{b('早期部分借自别的手术')}：作者自己说 Latarjet 专用的康复证据有限，早期思路参考的是美国肩肘治疗师协会针对{b('关节镜下前方关节囊盂唇修复')}的共识指南",
    f"{b('利益冲突')}：两位资深外科作者报告了来自 Arthrex、Smith & Nephew 等公司的资助和个人费用；一位作者的职位由 Arthrex 资助（均声明与本文无关）",
    f"{b('门槛数值多数没有出处')}：如 QuickDASH &lt; 60% / 40% / 20%、活动度 120°、上肢 Y 平衡 &lt; 4 cm，正文和附录都没有给依据",
    "优点：阶段划分清楚，每期的目标、剂量、禁忌和进阶标准都写到了可以照着做的程度；把心理准备和下肢动力链纳入评估，对运动员很实用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('许可声明自相矛盾')}：文末写“Creative Commons Attribution 4.0 International License”（CC BY 4.0），括号里和链接却是 CC BY-NC-SA 4.0。本文按更严格的 BY-NC-SA 处理",
    f"{b('“发病率”写成了“患病率”')}：原文说年轻男性运动员脱位“患病率每年 3%”，引用的 Owens 2007（美国西点军校）报告的是 {b('1 年发病比例 2.8%')}，而且其中 84.6% 是半脱位，不全是脱位",
    f"{b('外旋限制的引用不对题')}：“前 3 周外旋 &lt; 30°”引用 Itoi 1999，那是一项关于{b('肩脱位后')} Bankart 损伤在什么体位下能贴合的尸体研究，和 Latarjet 术后保护肩胛下肌没有直接关系",
    f"{b('参考文献张冠李戴')}：“斜方肌和前锯肌协同发力时对肩胛稳定贡献大”引用的 [39] 是 Speer 1993 年的《水疗在肩部康复中的作用》",
    f"{b('ER/IR 比值前后不一')}：正文写“最低 65%、最佳 66%～75%”（最低值和最佳下限只差 1 个百分点），附录流程图又写 ER90/IR90 &gt; 70%",
    f"{b('力量门槛正文和附录不等价')}：正文说阶段 III 要求力量 LSI ≥ 80%；附录写“徒手肌力 4/5 {b('或')}测力计 &gt; 健侧 80%”，徒手肌力 4/5 的门槛比 80% 的测力值低得多，两种标准不能互换",
    f"{b('上肢 Y 平衡的标准用了下肢的数')}：正文说单侧测试的目标是 LSI &gt; 90%，附录却给上肢 Y 平衡“两侧差 &lt; 4 cm”，这是正文里下肢 Y 平衡的切点。上肢 Y 平衡一般用按臂长标准化的综合得分",
    f"{b('FMS 目标值')}：原文写“14 分或以上”。据编者了解，常引用的切点（Kiesel 2007）是 ≤ 14 分损伤风险增高，所以达标一般应是 &gt; 14 分",
    f"{b('爆发力期的负荷')}：80%～100% 1RM、3～6 次通常归为最大力量训练，这么大的负荷下动作速度很难快起来，和本阶段“加入速度”的目标不太一致",
    f"{b('结论和正文对不上')}：结论说阶段 III 做“末端节律稳定和 PNF”，正文把这两项都放在阶段 II",
    f"{b('缩写一词两用')}：SSC 在图 1 里是肩胛下肌（subscapularis），在增强式训练一节又是拉长—缩短周期（stretch-shortening cycle）",
    f"{b('人名拼错')}：“Meyers and Lephart”应为 Myers；“Wellman et al.”应为 Wellmann",
]))

A.append(h2("落到临床"))
A.append(img(10))
A.append(cap("临床要点（编者整理）"))
A.append(ul([
    f"{mk('前 3 周守住两条')}：外旋 &lt; 30°；前 2 周不做等长，不抗阻屈肘、旋后",
    f"{b('按标准进阶')}：每个阶段对照附录的疼痛、QuickDASH、活动度、肌力和神经肌肉控制门槛；力量期不早于术后 6 周",
    f"{b('外旋要练满，肩胛下肌要单独测')}：腹压试验是看肩胛下肌恢复的好指标",
    f"{b('耐力 → 力量 → 爆发力')}：15～25 次 → 8～12RM → 大负荷加速度；增强式先双手后单手、先部分负重后全负重",
    f"{b('别忘了心理和下肢')}：AFAQ 筛恐惧回避；下肢 Y 平衡和 FMS 查动力链",
    "这是 5 级证据的经验方案，几个门槛数值正文和附录不一致（ER/IR 比值、力量门槛、上肢 Y 平衡），用的时候建议按更严格的那个",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Bradley H, Lacheta L, Goldenberg BT, Rosenberg SI, Provencher MT, Millett PJ. Latarjet Procedure for the Treatment of Anterior Glenohumeral Instability in the Athlete – Key Considerations for Rehabilitation. Int J Sports Phys Ther. 2021;16(1):259-269. doi:10.26603/001c.18707</em><br>"
    "原文以知识共享署名—非商业性使用—相同方式共享 4.0 协议（CC BY-NC-SA 4.0）开放获取。本文为非商业学术交流用的中文解读：原文图 1、3、4 中的英文由编者译为中文，其余原文图未改动，图注为编者翻译；"
    "附录 1 进阶流程图由编者翻译并重新排版；表格、首图和临床要点卡为编者根据原文整理。改编的图片同样按 CC BY-NC-SA 4.0 共享。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「Latarjet 术后」运动员怎么练回赛场？五阶段按标准进阶：前 3 周外旋别过 30°，力量期不早于 6 周"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>Latarjet 术后康复推文</title>
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
""" + BODY + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
