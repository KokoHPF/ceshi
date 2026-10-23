#!/usr/bin/env python3
"""攀岩者 ACL 重建术后康复推文：生成 article_body.html 与 preview.html。

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
    "Vagy J, Schöffl V, Ohde J, Petersen W, Lutter C. Anterior cruciate ligament rehabilitation and return to sport in rock climbing athletes: a practical concept paper. Front Sports Act Living. 2025;7:1580509.",
    "作者来自美国南加州大学、德国班贝格医院、罗斯托克大学医学中心等",
    "方法学 / 概念性论文（作者提出的方案，尚未验证）",
], square=True))

A.append(h2("先说攀岩为什么要单独一套"))
A.append(p(
    f"ACL 断裂在攀岩里越来越常见，尤其是{b('抱石')}：一项研究里，{b('超过 90%')} 的抱石 ACL 损伤来自{mk('从岩壁上掉到地面')}。"
))
A.append(ul([
    f"球类运动的 ACL 损伤多发生在{b('急停变向')}；抱石是从最高约 3 米处{b('不受控地坠落、落地时膝外翻')}",
    f"先锋攀爬还要面对{b('冲坠后摆荡撞墙')}",
    "常规的回场测试（单腿跳、折返跑）看不到“从高处落地”这种离心负荷",
    "攀岩有自己的高风险动作：勾脚、高抬脚、落膝，再加上坠落，是攀岩急性膝伤的主要机制",
]))
A.append(p(f"所以作者在常规 ACL 方案上，加了{mk('攀岩专项训练和两个专项回场测试')}：坠落悬挂测试和先锋坠落测试。"))

A.append(h2("重点：六期方案"))
A.append(p(f"作者强调{b('按标准进阶、不按时间')}；给的时间是“最早不早于”，防止水平高的攀岩者回得太快。"))
A.append(pic(2, "六期总览"))

A.append(h3("第 1 期（0～4 周）术后早期"))
A.append(ul([
    "消肿止痛、步态、本体感觉和神经肌肉再教育；胫股、髌股关节被动和主动松动",
    f"{mk('尽早练踝背伸和髋屈曲、外展')}：背伸受限和落地机制差、地面反作用力大有关；髋越灵活，攀岩时膝在末端位越少受力",
    f"{b('别丢了手指力量')}：指力是攀岩成绩最强的预测因素，攀岩伤 40% 以上在手和手指。先坐位或卧位练握力，再站着拿便携指力板；{b('伤口愈合')}、能舒服悬挂后才上指力板，挂板高度以脚不离地为准",
    f"过关：{b('主动伸膝到 0°、被动屈膝到 90°')}",
]))

A.append(h3("第 2 期（4～8 周）术后后期"))
A.append(ul([
    "练伸膝肌、屈膝肌、小腿、髋外展和伸髋肌；平衡和神经肌肉练习加难度",
    f"{b('上肢')}：肩带耐力也是攀岩成绩的强预测因素，做引体向上和屈肘 90° 悬挂，单杠高度以脚不离地为准",
    f"{b('勾脚的腘绳肌训练')}（无禁忌、非腘绳肌腱移植时）：屈髋位小范围屈膝 → 俯卧负重全范围屈膝 → 双腿臀桥 + 滑板屈膝 → 单腿臀桥 + 弹力带屈膝；同时变换髋内收外展、踝屈伸、胫骨内外旋，模拟岩壁上的勾脚姿势",
    f"{b('高抬脚')}：手拉悬吊带或便携指力板辅助，从 {b('10 厘米')}台阶开始，逐步加到 0.5 米",
]))
A.append(pic(3, "原文图 1、2"))
A.append(p(f"{b('过关标准')}（比较多）："))
A.append(ul([
    "积液 ≤1+（膨隆试验）；屈膝主动活动度达健侧 90%",
    "单腿平衡练习（伸膝、屈膝位，配合上下肢动作）已做 2 周",
    f"伸膝、屈膝、髋外展等长肌力 {mk('&gt; 健侧 70%')}",
    f"{b('高抬脚上拉')} 0.5 米 × 10 次",
    f"防止靠手臂“作弊”：还要能{b('一步跨两级，连上 6 层楼')}（大致相当于一条室内线路的垂直爬升）",
    f"{b('改良 Grant 抬脚测试')}：离墙 23 厘米，双手撑墙略宽于肩，脚沿墙滑起到最大屈髋，量高度，两侧应达最大高度的 80%",
]))
A.append(pic(4, "原文图 3"))

A.append(h3("第 3 期（8～16 周）早期强化"))
A.append(ul([
    "继续加强下肢力量",
    f"术后{b('至少 12 周')}且第 2 期过关后，可以上{b('顶绳')}：难度比自己的顶绳水平{b('低 3 级')}（例如国际登山联合会难度 8 级 → 6 级），刚开始建议戴铰链护膝",
    "作者建议先爬仰角线路再爬垂直线路，减少掉落时脚卡在岩壁上的风险",
    f"过关：等长肌力达健侧 80%；单腿蹲到屈膝 60° 的次数对称性 ≥80%，且{b('无躯干侧倾、无膝外翻、不失衡')}；{b('Y 平衡')}前向和后内向两侧差 ≤4 厘米（超过 4 厘米的人更难达到单腿跳 90% 对称）",
]))

A.append(h3("第 4 期（16～24 周）后期强化"))
A.append(ul([
    f"{b('闭链上肢 + 四点跪')}：悬吊带平板支撑 + 下肢动作（比地面版肌电更高）；熊爬姿势 + 对侧手脚交叉，模拟攀爬",
    f"{b('坠落悬挂训练')}：挂在单杠上（或从箱子上退下）松手，落成{mk('屈膝 90° 下蹲')}；从 {b('10 厘米')}开始，到本期末 {b('0.5 米')}，变换脚位模拟抱石落地",
    f"{b('抱石横移')}：离地 ≤0.5 米的横向攀爬；注意横移时胫骨外旋对 ACL 的应力，{b('戴铰链护膝')}，学会用健腿下来",
    "顶绳难度提高到比自己水平低 2 级",
]))
A.append(pic(5, "原文图 4、5"))
A.append(p(f"{b('学会怎么掉下来')}：万一落地，要会缓冲。"))
A.append(ul([
    f"{b('向后掉')}：放松 → 屈膝屈肘 → 收手臂 → 向后滚",
    f"{b('侧向掉')}：看落地区 → 屈膝屈肘 → 收手臂 → 让垫子吸收冲击",
    f"{red('不要锁膝落地，不要用手撑地')}",
    "先口头讲清楚，再从下蹲位练习向后、向侧滚",
]))
A.append(pic(6, "原文图 6、7"))
A.append(p(f"{b('过关标准')}：ACL 重返运动心理准备量表 {b('≥56 分')}；{mk('坠落悬挂测试 90%、先锋坠落测试 100%')}；单腿跳远、6 米计时单腿跳、三级跳、交叉跳对称性 85%；等长肌力和单腿腿举达健侧 85%；术后至少 24 周。"))

A.append(h2("重点：两个攀岩专项测试"))
A.append(p(f"心理准备量表 ≥56 分后才做。害怕的攀岩者会过度抓握、动作顺序乱，甚至在本来做得到的动作上失误，增加手术腿负担或发生严重坠落。"))
A.append(pic(8, "坠落悬挂测试"))
A.append(pic(9, "先锋坠落测试"))

A.append(h3("第 5 期（24～36 周）重返运动"))
A.append(ul([
    f"虽然 6 个月就能进入本期，{b('很多人要到 9 个月左右才达标')}；在 6～9 个月之间，每推迟 1 个月回场，再伤风险可能降低 51%",
    f"{b('先锋')}：比当前顶绳水平低 3 级；{b('抱石')}：比自己水平低 2 级（如 V8 → V6），{mk('只爬确定不会掉的线路')}；先室内、后户外",
    f"{b('落膝训练')}：落膝要把重心压在一只脚外侧、髋内旋贴墙、膝往下沉，需要足够的股直肌长度和髋内旋；从坐地屈髋屈膝 90° 开始 → 站立 → 脚放垫高物上",
    "勾脚、高抬脚、落膝在攀爬中从“最大辅助”逐步到“最小辅助”",
    f"{b('落地训练')}继续进阶：加高度；支撑面从宽到窄、对称到错开、脚尖朝前到外八；躯干从前倾（臀肌吸收）到直立（伸膝装置吸收）；口令“{b('轻轻落地')}”能降低 ACL 负荷",
    "攀岩对心肺也有要求，疲劳会影响技术和决策、增加 ACL 风险，所以要在安全环境下做接近最大强度的模拟攀爬",
]))
A.append(pic(7, "原文图 8"))
A.append(p(f"{b('过关')}：术后{b('至少 9 个月')}；心理准备量表 {b('≥75 分')}；单腿跳、等长肌力、单腿腿举都 ≥90%；每周至少 3 次力量或增强式训练；能在抱石或先锋中完成勾脚、高抬脚、落膝，能爬到自己的水平。"))

A.append(h3("第 6 期（36 周以后）重返竞技"))
A.append(ul([
    "高难度落地、增强式和带本体感觉挑战的力量训练",
    "可以参加先锋比赛、爬自己的“项目”线路",
    f"比赛和项目抱石{mk('至少 12 个月后')}，12 个月内不爬超过 3 米的抱石线路",
    f"建议{b('术后持续做康复训练到 3 年')}，降低再断裂风险",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{red('这是作者提出的方案，没有验证')}：作者自己说“早期在个别攀岩者身上使用有希望”，需要研究检验安全性和有效性",
    "坠落悬挂测试、先锋坠落测试是新设计的，没有信度、效度和常模数据；分数线（90%、100%）是作者定的",
    "大部分过关标准借用了球类运动的 ACL 研究",
]))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    "背景说 71 名急性膝伤患者中有 7 例 ACL 断裂，占 9.1%；7/71 实际约 9.9%",
    f"图 3 图注写“落膝进阶练习”，但图里是第 2 期的{b('改良 Grant 抬脚测试')}",
    f"{red('先锋坠落测试 100%')} 是第 4 期的过关标准，但先锋攀爬要到第 5 期才允许，第 4 期怎么做先锋坠落没有交代",
    "第 3 期表格写“开始低风险的垂直攀爬”，正文又说先爬仰角线路、再过渡到垂直，前后矛盾",
    "难度换算不一致：8 级 → 6 级被说成“低 3 级”，8 级 → 7+ 却说成“低 2 级”（按国际登山联合会的细分，两者分别差 6 档和 2 档）",
    "第 5 期过关要求“术后至少 9 个月”（约 39 周），第 6 期却写“36 周以后开始”；坠落悬挂测试写“18 英寸（0.5 米）”，18 英寸约 0.46 米",
]))

A.append(h2("落到临床"))
A.append(ul([
    "攀岩者术后第一天就可以练手指和上肢，但伤口愈合前别挂指力板",
    f"{mk('早练踝背伸和髋屈曲外展')}，这两项对落地和高抬脚都很关键",
    "勾脚练腘绳肌、高抬脚练伸膝伸髋、落膝练髋内旋，分阶段从地面练到岩壁",
    "第 2 期用“一步跨两级上 6 层楼”防止靠手臂代偿",
    "教会攀岩者怎么掉：屈膝屈肘、收手、滚，不锁膝、不撑手",
    "回抱石前做坠落悬挂测试，回先锋前做先锋坠落测试",
    "顶绳 → 先锋 → 抱石，难度从低 3 级开始；12 个月内不爬 3 米以上的抱石",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　攀岩者 ACL 重建术后康复方案"))
A.append(table(["分期", "干预重点", "攀岩专项活动", "进入下期的标准"], [
    ["第 1 期（0～4 周）术后早期", "减轻疼痛；消肿；开始本体感觉、平衡和神经肌肉再教育；步态训练；胫股和髌股关节被动、主动松动；改善髋屈曲和外展；改善踝背伸", "开始坐位或卧位手指训练；建议伤口完全愈合后再挂指力板", "主动伸膝完全；被动屈膝到 90°"],
    ["第 2 期（4～8 周）术后后期", "继续改善活动度；加强伸膝肌、屈膝肌、小腿、髋外展和伸髋肌；平衡和神经肌肉练习加难度；维持或提高手指和肩带力量；开始攀岩动作的分解练习；提高上肢辅助下的上台阶能力", "悬挂下的肩带力量和耐力练习；开始勾脚相关的腘绳肌训练（无禁忌时）；高抬脚从 10 厘米开始", "改良 Grant 抬脚 80%；高抬脚上拉 0.5 米 × 10 次；一步跨两级上 6 层楼；积液 ≤1+；屈膝主动活动度达健侧 90%；单腿平衡练习（伸膝、屈膝位，配合上下肢动作）2 周；伸膝、屈膝、髋外展等长肌力 &gt; 健侧 70%"],
    ["第 3 期（8～16 周）早期强化", "开始低风险的垂直攀爬动作；加强伸膝肌、屈膝肌、小腿、髋外展和伸髋肌", "顶绳难度比估计水平低 3 级（8 级 → 6 级，国际登山联合会难度），建议至少 12 周后开始", "等长肌力达健侧 80%；单腿蹲到屈膝 60° 次数对称性 ≥80%，控制和质量良好；Y 平衡前向和后内向两侧差 ≤4 厘米"],
    ["第 4 期（16～24 周）后期强化", "加入低风险的横向攀爬动作；恢复四点跪负重动作和协调；加大下肢训练强度和动作难度；坠落技术教育；开始初级落地和增强式训练", "离地不超过 0.5 米的次最大强度抱石横移，建议戴铰链护膝；顶绳难度提高到低 2 级（8 级 → 7+）；模拟攀爬的闭链上肢和四点跪练习；早期落地训练，从低处开始到 0.5 米", "心理准备量表 ≥56 分；坠落悬挂测试 90%；先锋坠落测试 100%；单腿跳远、6 米计时单腿跳、三级跳、交叉跳对称性 85%；等长肌力达健侧 85%；单腿腿举达健侧 85%"],
    ["第 5 期（24～36 周）重返运动", "重新训练落地（抱石和先锋）；加强并协调攀岩专项动作；进阶到中级落地和增强式训练", "先锋难度比当前顶绳水平低 3 级（8 级 → 6 级）；垂直、不会掉的抱石，比估计水平低 2 级（V8 → V6）；落膝训练；在顶绳保护下练勾脚、高抬脚、落膝，再用到抱石或先锋中；落地训练进阶", "术后至少 9 个月；每周至少 3 次力量或增强式训练；能在抱石或先锋中完成勾脚、高抬脚、落膝；能爬到自己的水平；心理准备量表 ≥75 分；单腿跳对称性 ≥90%；等长肌力 ≥90%；单腿腿举 ≥90%"],
    ["第 6 期（36 周以后）重返竞技", "建议不早于术后 36 周；高处下落跳；带本体感觉挑战的高级力量训练；进阶到高级落地和增强式训练", "先锋比赛；先锋项目线路；抱石比赛（建议至少 12 个月后）；抱石项目线路（12 个月内避免超过 3 米的线路）", "建议术后持续做康复训练至 3 年，降低 ACL 再损伤风险"]]))
A.append(tcap("原文表 2　坠落悬挂评分（每级落 5 次）"))
A.append(table(["级别", "描述"], [
    ["第 1 级", "松手，双腿中立位落在抱石垫上"], ["第 2 级", "松手，手术腿在前、健腿在后落地"], ["第 3 级", "松手，健腿在前、手术腿在后落地"]]))
A.append(table(["评分项", "是（1 分）", "否（0 分）"], [
    ["屈膝角度 ≥90°", "", ""], ["无动态膝外翻（髌骨落到大脚趾内侧）", "", ""], ["脚的落点朝向正确", "", ""], ["向后滚", "", ""], ["总分", "____ / 20", ""]]))
A.append(tcap("原文表 3　先锋坠落评分"))
A.append(table(["评分项", "是（4 分）", "否（0 分）"], [
    ["屈膝角度 ≥60°", "", ""], ["屈髋角度 ≥60°", "", ""], ["会判断坠落区，技术和安全意识到位", "", ""], ["绳子保持在身体和岩壁之间", "", ""], ["松手时呼气，身体放松", "", ""], ["总分", "____ / 20", ""]]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Vagy J, Schöffl V, Ohde J, Petersen W, Lutter C. Anterior cruciate ligament rehabilitation and return to sport in rock climbing athletes: a practical concept paper. Front Sports Act Living. 2025;7:1580509. doi:10.3389/fspor.2025.1580509</em><br>"
    "原文以知识共享署名协议（CC BY）发表。本文为中文解读，插图引自原文图 1～8（编者加中文标注），六期总览、坠落悬挂评分卡与先锋坠落评分卡为编者中文绘制，表格为编者翻译。"
))

TITLE = "「ACL」攀岩者 ACL 重建后怎么回岩壁？六期康复 + 两个坠落测试"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>攀岩ACL康复推文</title>
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
