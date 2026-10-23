#!/usr/bin/env python3
"""过顶运动员肘关节康复（Wilk 等 2012）推文。

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
    "Wilk KE, Macrina LC, Cain EL, Dugas JR, Andrews JR. Rehabilitation of the overhead athlete's elbow. Sports Health. 2012;4(5):404-414. doi:10.1177/1941738112455006",
    "作者来自美国 Champion 运动医学中心和 Andrews 运动医学与骨科中心，Wilk、Andrews 是投掷运动员康复领域的代表人物",
    "临床综述（专家经验方案）",
], square=True))

A.append(h2("先说为什么投手的肘容易伤"))
A.append(p(
    f"美国职业棒球大联盟投手的伤病里，{b('22%～26% 在肘部')}。投球时肘伸直速度超过每秒 2300 度，内侧剪切力约 300 N、压缩力约 900 N；"
    f"加速期的外翻力矩约 64 N·m，超过了尺侧副韧带本身能承受的极限。"
))
A.append(ul([
    f"{b('内侧')}被反复牵拉 → 尺侧副韧带损伤、内上髁炎、少棒肘",
    f"{b('外侧')}被反复挤压 → 肱骨小头剥脱性骨软骨炎",
    f"{b('后方')}受牵拉、挤压和扭转 → 外翻伸直过载、骨赘、鹰嘴应力骨折",
]))
A.append(p(f"所以无论受伤后还是术后，康复都要{mk('循序渐进、多阶段推进')}，同时练整条动力链：肩胛、肩、手、核心、髋和腿。"))

A.append(h2("重点一：通用的四阶段康复"))
A.append(pic(2, "四阶段总览（编者根据原文整理）"))
A.append(h3("第 1 阶段：即刻活动，先把伸肘找回来"))
A.append(pic(3, "原文图 1、2：低负荷长时间伸肘牵伸，以及两种居家伸肘牵伸支具"))
A.append(ul([
    f"{b('伸肘是重中之重')}：肘关节特别容易屈曲挛缩。术后的伸肘要以{b('受伤前的角度')}为标准，不要简单和对侧比；职业投手本来就常常差 3°～5° 伸不直",
    f"{b('松动')}：先用Ⅰ、Ⅱ级止痛，症状减轻后进阶到Ⅲ、Ⅳ级；做{b('肱尺关节后向滑动')}帮助伸直，也别忘了肱桡关节和桡尺关节",
    f"{b('低负荷长时间牵伸')}：仰卧，上臂远端垫毛巾卷，手腕挂轻弹力带拉向地面，肩内旋、前臂旋前；{mk('每次 15 分钟、每天 4 次，末端时间累计 ≥ 60 分钟')}，以不痛、不痉挛为度；效果不好就夜间戴牵伸支具",
    f"{b('看终末感决定力度')}：活动受限、终末感硬且不痛 → 可以更积极；没到阻力就痛或终末感空 → 慢慢来",
    "肘腕各肌群做无痛的次最大等长收缩；肩胛肌力训练立即开始；肩、肘、前臂的节律稳定练习",
    "冰敷、激光、高压电刺激用于消炎止痛",
]))
A.append(h3("第 2 阶段：中期，力量和控制"))
A.append(pic(4, "原文图 3：屈肘、屈腕旋前肌群的徒手向心和离心抗阻"))
A.append(ul([
    f"{b('进入条件')}：投掷所需活动度恢复、几乎不痛、屈伸肘肌力 ≥ 4 级",
    f"{b('肩的活动度')}：重点保持肩 90° 外展位{b('外旋')}（外旋不足会增加肘内侧应力）和{b('内旋')}（内旋活动度可提供保护性的内翻力）",
    f"{b('力量')}：先向心后离心，屈伸肘、屈伸腕、前臂旋前旋后；肩袖后部和肩胛肌；做{mk('投掷十项')}。有研究显示 6 周投掷十项能让高中投手球速提高约 2 英里/小时",
    "神经肌肉控制：本体感觉神经肌肉促进加节律稳定、肘腕徒手抗阻",
]))
A.append(h3("第 3 阶段：进阶强化"))
A.append(pic(5, "原文图 4～6：进阶投掷十项，在稳定球上做持续保持和节律稳定"))
A.append(pic(6, "原文图 7、8：90°/90° 对墙抛球加末端节律稳定、腕屈肌翻球"))
A.append(ul([
    f"{b('进入条件')}：肩内外旋总活动度无痛恢复、无压痛、力量达到健侧 70%",
    f"{b('屈肘强调离心')}：肱二头肌在随挥期负责“刹车”，防止鹰嘴撞向鹰嘴窝；肱三头肌主要练向心（对应加速期）",
    f"{b('器械训练')}：卧推、坐姿划船、高位下拉",
    f"{b('进阶投掷十项')}：坐在稳定球上做满罐、俯卧水平外展、外旋，加持续保持和节律稳定",
    f"{b('增强式')}：{mk('双手（胸前传、左右抛、过顶掷）→ 单手（90°/90° 抛、对蹦床做 0° 内外旋抛、对墙拍球）→ 腕屈翻球、伸腕抓握')}，用约 0.9 kg 的药球",
]))
A.append(h3("第 4 阶段：重返运动"))
A.append(ul([
    f"{b('进入条件')}：投掷活动度无痛、无压痛、等速测试满意、医生放行，增强式抛球无痛且动作质量好",
    f"{b('等速参考')}：180°/s 时投掷侧屈肘肌力应比对侧强 10%～20%，伸肘强 5%～15%",
    f"{b('长传间歇投掷')}：从 45 英尺（约 13.7 米）开始，按位置进阶到 120～180 英尺（约 36.6～54.9 米），全程无痛",
    f"{b('投前 1 组、投后 2 组')}力量练习；第二天练肩胛、外旋和核心",
    f"{b('投手再上投手丘')}：强度 50% → 75% → 90% → 100%，用 4～6 周；{mk('能以 ≥ 80% 强度无症状投 40～50 球后才加变化球')}",
]))

A.append(h2("重点二：常见损伤的非手术方案"))
A.append(pic(7, "常见损伤的非手术处理（编者根据原文整理）"))
A.append(ul([
    f"{b('尺侧副韧带部分损伤')}：先在 10°～100° 无痛范围内活动，必要时戴支具防外翻 → 每周增加 5°～10° → 6～7 周进入进阶强化 → 肌力 5 级、动态稳定良好后开始间歇投掷；症状反复就考虑手术",
    f"{b('内上髁炎、屈肌-旋前肌腱病')}：先分清“炎症”还是“退变”。炎症期控制疼痛后，做以离心为主的大负荷、低次数训练，屈伸腕时屈肘 30°～45° 以减少内侧应力；退变期以热疗、离心、横向按摩、干针、冲击波等促进修复",
    f"{b('外翻伸直过载')}：止痛后重点练屈肘肌离心力量，用来控制快速伸肘；同时检查投球动作，排除尺侧副韧带损伤",
    f"{b('肱骨小头剥脱性骨软骨炎')}：只有 1 期适合保守治疗：屈肘 90° 制动 3～6 周 → 等长 → 约 1 周后等张 → 高速、离心、增强式 → 间歇投掷",
    f"{b('少棒肘')}：无撕脱的按尺侧副韧带非手术方案处理，12～14 周内不做重负荷训练，休息 8～12 周后开始投；轻度移位的撕脱制动 7～14 天，第 8～12 周开始投",
]))

A.append(h2("重点三：常见术后方案的时间线"))
A.append(pic(8, "四种术后康复的大致时间线（编者根据原文绘制）"))
A.append(pic(9, "原文图 9：尺侧副韧带重建术后用铰链式肘支具保护移植物"))
A.append(ul([
    f"{b('尺侧副韧带重建（8 字形移植法）')}：屈肘 90° 后托 7 天；被动活动立即开始，{b('伸直早早做到至少 15°')}（能完全伸直且不痛也可以，完全伸直不会给移植物带来过大应力），屈曲从 100° 开始每周加 10°，4～6 周全范围；3～4 周轻等张、6 周投掷十项、8～9 周渐进抗阻；12～16 周离心和增强式（12 周双手、14 周单手）；{mk('16 周开始间歇投掷，约 9 个月回到比赛投球')}。743 名运动员中 83% 在 1 年内回到原水平或更高",
    f"{b('尺侧副韧带重建（对接法）')}：支具前 3 周限制在 30°～60°，第 4 周 15°～90°，6 周全范围；6 周等张、约 10 周增强式和器械；野手 12 周开始击球；4 个月间歇投掷，约 9 个月正式投球",
    f"{b('尺神经前置')}：后托 1 周，3～4 周恢复全活动度；4～6 周投掷十项，8 周进阶训练和增强式，10～12 周间歇投掷，约 16 周回到比赛",
    f"{b('鹰嘴后方骨赘切除')}：伸肘恢复要更保守（术后疼痛限制）；第 10 天约 15°～105/110°，第 14 天约 5～10°～115°，20～25 天全范围；前 2 周注意肱三头肌用力引起的后方痛；6 周投掷十项，10～12 周间歇投掷",
]))

A.append(h2("这些建议能信几分"))
A.append(ul([
    f"{b('专家经验为主')}：时间节点和标准来自作者团队大量临床经验，几乎没有对照研究直接验证",
    f"{b('关键细节在附表里')}：完整的分期方案、间歇投掷程序和投掷十项动作都放在在线补充材料里，正文只有概要",
    f"{b('部分理疗证据薄弱')}：激光、超声、离子导入、一氧化氮贴片等，作者列为常用手段，但证据并不强",
    f"{b('人群是棒球投手')}：网球、高尔夫等其他过顶运动可借鉴原则，但间歇程序要换成对应项目",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('非手术尺侧副韧带的时间算不通')}：从 10°～100° 开始，每周增加 5°～10°，却说 3～4 周恢复全活动度；屈曲从 100° 到约 145° 就要 4.5～9 周",
    f"{b('剥脱性骨软骨炎：制动和活动矛盾')}：说屈肘 90° 制动 3～6 周，同时又要每天做 3～4 次肩、肘、腕活动度练习；前一句“相对休息和制动直到肘部症状”也没写完",
    f"{b('内上髁的证据用的是外上髁研究')}：讲内上髁炎时，支持富血小板血浆的几项研究全部针对的是外侧网球肘",
    f"{b('解剖表述错误')}：外翻伸直过载写成“鹰嘴楔入内侧鹰嘴”，应为鹰嘴撞击鹰嘴窝内侧壁",
    f"{b('支具时间前后矛盾')}：尺侧副韧带重建术后先说后托只用 7 天，接着又说“4 周后”从后托换成铰链支具",
    f"{b('伸肘缺失数字不一致')}：一处说职业投手通常差 3°～5°，紧接着引用的研究是平均差 7°",
    f"{b('表格不在正文')}：正文引用的表 1、表 2 以及补充表 3～8、附录 A、B 都只在在线补充材料里，PDF 中看不到",
    f"{b('小错')}：“投后再做 2 组”写成了 proceeding（之前）；“elicit”写成“illicit”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('伸肘第一')}：术前、伤前的伸肘角度要记录，术后早期就用低负荷长时间牵伸，每天累计末端时间 ≥ 60 分钟",
    f"{b('按标准进阶')}：4 级肌力 → 70% 力量 → 等速达标、增强式无痛，再进入下一阶段",
    f"{b('肩一起管')}：保持肩外旋和内旋活动度，强化肩袖后部和肩胛肌，减轻肘内侧负担",
    f"{b('屈肘离心是很多肘病的共同重点')}：外翻伸直过载、骨赘切除术后、进阶期都要练",
    f"{b('回归投球有章法')}：长传间歇程序 → 投手丘 50%～100% 强度 → 再加变化球，投前投后都做力量练习",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Wilk KE, Macrina LC, Cain EL, Dugas JR, Andrews JR. Rehabilitation of the overhead athlete's elbow. Sports Health. 2012;4(5):404-414. doi:10.1177/1941738112455006</em><br>"
    "原文版权归作者所有（© 2012 The Author(s)），PDF 未标注开放许可协议。本文为学术交流用的中文解读：图 1～9 引自原文（加中文说明），四阶段卡、非手术方案卡和术后时间线为编者根据原文整理绘制。版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「肘关节」投手的肘伤怎么康复？四阶段方案 + 常见伤病与术后时间线"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>过顶运动员肘关节推文</title>
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
