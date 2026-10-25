#!/usr/bin/env python3
"""手和腕电话＋视频远程评估（Vomer 等 2023）推文。

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
F = lambda i: i + 2  # 原文图 i → 第 i+2 张图
A.append(img(1))
A.append(cap("原文信息（编者中文重排）"))
A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Vomer RP II, Lewno AJ, Udoh I, Albano-Aluquin S, Pujalte GGA. Evaluation of the hand and wrist via telephone and video visit. Cureus. 2023;15(2):e35322. doi:10.7759/cureus.35322",
    "作者单位：美国杜克大学骨科与家庭医学科、梅奥诊所（杰克逊维尔）、密歇根大学康复科、宾州州立大学风湿科",
    f"文章类型：期刊归为原创研究，实际是{b('作者经验整理的操作指南')}（示范模特是第一作者本人，没有验证数据）。和前两篇肘、髋远程评估出自同一团队",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"手和腕结构小、位置表浅，{b('视频里看得很清楚')}；难点是腕部结构挤在一起，患者指的痛点要医生对着解剖仔细核对",
    f"顺序：视诊 → 握拳和张手 → 自我触诊 → 活动度 → 抗阻 → {b('按桡侧、尺侧、神经分区做特殊检查')}；永远和健侧比",
    f"先问{red('有没有外伤')}，有外伤先排除骨折；怀疑舟骨骨折时{red('不要做 Watson 试验')}，以免骨折块移位",
    f"视频还有个额外好处：能直接看到患者{b('家里的电脑和工位')}，当场给人体工学建议",
]))
A.append(img(2))
A.append(cap("鉴别诊断流程（据原文图 11 改画成中文）"))

A.append(h2("一、视诊"))
A.append(ul([
    "让患者面对镜头坐好，先看手腕的掌侧、背侧、尺侧和桡侧",
    "和健侧比：力线异常、萎缩、肿胀、淤青、苍白、伤口、静脉怒张；腕背仔细找腱鞘囊肿",
    "请患者把在意的包块或隆起对着镜头，和对侧比较",
]))
A.append(pic(F(1), "原文图 1：手腕掌侧和背侧"))
A.append(pic(F(2), "原文图 2：腕背腱鞘囊肿好发处"))

A.append(h2("二、握拳和张手"))
A.append(ul([
    f"{b('握拳')}：掌骨头是否连成一条平滑的弧；指尖能否碰到手掌；各指是否都指向拇指根部（舟骨方向）——偏离提示骨折或损伤",
    f"仔细看握拳和张手的过程：{b('握拳时示、中指握不拢')}，原文认为提示骨间前神经损伤（“祝福手”）；{b('张手时环、小指伸不直')}，提示尺神经病变（尺侧爪形手）",
    f"不能做{b('“OK”手势')}（拇指和示指圈不成圆），要怀疑骨间前神经损伤",
]))
A.append(pic(F(3), "原文图 3：握拳看掌骨力线"))
A.append(pic(F(4), "原文图 4：原文称“尺侧爪形手”"))

A.append(h2("三、自我触诊"))
A.append(p(f"腕部结构挤在一起，指导患者按哪里不容易；{mk('患者指出的痛点要对照解剖结构仔细核对')}。重点部位："))
A.append(ul([
    "腕骨（尤其舟骨）、鼻烟窝、下尺桡关节、桡骨茎突、尺骨茎突、拇指腕掌关节",
    "伸肌腱：Lister 结节处的拇长伸肌腱、尺侧腕伸肌腱",
    "尺骨小凹处的 TFCC、各掌骨、钩骨钩、尺侧和桡侧腕屈肌",
]))

A.append(h2("四、活动度和抗阻"))
A.append(p(f"活动度{b('先主动、必要时再被动')}，和健侧比；抗阻测试找无力或疼痛。"))
A.append(img(13))
A.append(cap("活动度和抗阻测试（原文数据）"))

A.append(h2("五、桡侧"))
A.append(ul([
    "让患者按桡骨茎突、各伸肌间室、下尺桡关节、腕骨（尤其舟骨）、腕掌关节和掌骨",
    "查感觉：手背的桡神经浅支、手掌侧的正中神经",
    f"动拇指或抓握时痛，做{b('腕掌关节研磨试验')}：痛提示拇指腕掌关节或舟大小多角（STT）关节骨关节炎",
    f"{b('Finkelstein 试验')}：拇指握在拳内、腕向尺侧偏，痛或无力提示 de Quervain 腱鞘炎",
    f"{b('改良 Watson 试验')}：按住舟骨，同时腕从尺偏移到桡偏，痛或“咔噔”提示舟月不稳。{red('怀疑舟骨骨折时不要做')}",
    "握手或抓握时无力（伴或不伴痛），提示腕骨损伤或腕不稳",
    f"{b('拇指尺侧副韧带')}：稳住掌指关节、把拇指向桡侧扳，和健侧比间隙增大提示韧带损伤；摔倒后拇指尺侧痛就要查",
]))
A.append(pic(F(5), "原文图 5：第一腕掌关节"))
A.append(pic(F(6), "原文图 6：Finkelstein 试验和鼻烟窝"))
A.append(pic(F(10), "原文图 10：拇指尺侧副韧带外翻应力试验"))

A.append(h2("六、尺侧"))
A.append(ul([
    "让患者按尺骨茎突、尺侧腕伸肌腱、尺骨小凹和腕骨",
    f"{b('Guyon 管')}按压痛、持续按压复现症状 → 尺神经在腕部受压；尺侧有外伤史或反复撞击钩骨钩的，还要想到{b('小鱼际锤击综合征')}（尺动脉损伤）",
    "查环指、小指掌侧的感觉",
    f"尺偏时腕横纹处痛、{b('按尺骨小凹痛')}、推东西时腕尺侧痛 → TFCC 损伤",
    f"旋前旋后时腕横纹尺侧痛或无力 → 尺侧腕伸肌腱病；同时有{b('弹响或滑动感')}，常伴软组织肿胀 → 尺侧腕伸肌腱半脱位",
]))
A.append(pic(F(7), "原文图 7：Guyon 管"))

A.append(h2("七、神经和血管"))
A.append(ul([
    f"{b('腕管综合征')}：按压腕横纹（Durkin 试验）或叩击（Tinel 征）出现痛或麻；Phalen 试验（手背相贴、手指朝下）复现症状进一步支持",
    f"{b('桡神经浅支卡压')}：表带收紧时腕背痛或麻；没有手表就用另一只手紧握手腕模拟",
    f"{b('Allen 试验')}：握拳后请人压住腕两侧的桡、尺动脉，松开后手掌回红慢，提示掌动脉弓供血问题",
    "手指连带手臂烧灼感或麻木，按分布判断正中、尺、桡神经，并让患者做 Spurling 试验排除颈神经根",
]))
A.append(pic(F(8), "原文图 8：腕部 Tinel 征"))
A.append(pic(F(9), "原文图 9：Phalen 和反 Phalen 试验"))

A.append(h2("八、电话问诊这样问"))
A.append(p(f"原文表 1 把每项检查改写成了患者听得懂的问题。编者按部位整理成两张卡："))
A.append(img(14))
A.append(cap("电话问诊①：视诊、桡侧和拇指（据原文表 1 改写）"))
A.append(img(15))
A.append(cap("电话问诊②：尺侧、神经和血管（据原文表 1 改写）"))
A.append(p(f"其他要问的：“摔倒后开始痛的吗？”（按受伤方式和畸形想骨折）；“张手时某个手指卡住吗？”（扳机指）；“受伤时手指‘啪’一下，末节弯不了吗？”（球衣指）；“什么事因为手腕痛、没劲或活动受限做不了？”（{b('让患者在电话里复现动作并描述')}）。"))

A.append(h2("这篇文章能信几分"))
A.append(ul([
    f"期刊归为原创研究，但{b('没有受试者也没有数据')}；作者说以后会做验证研究，目前所有远程检查都{red('没有信度、效度数据')}",
    "电话问诊只能靠患者自述；视频能看，但摸不到，对医生的指导能力要求高",
    "优点：覆盖手腕各分区和常见神经卡压，问题口语化，流程图能直接拿来分诊",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b("“祝福手”归错了神经")}：原文说握拳时示、中指握不拢提示{red('骨间前神经')}损伤（祝福手），流程图又把“祝福手”归到“正中神经卡压”。祝福手通常是肘部或更近端的正中神经损伤；骨间前神经损伤的典型表现是做不成“OK”手势，原文另一处也这样写",
    f"{b('拇指尺侧副韧带的关节写错')}：正文写“稳住掌指关节、把拇指{red('远节')}向桡侧扳”，图 10 图注又说是让第{red('一腕掌关节')}张开。拇指尺侧副韧带在{b('掌指关节')}，应稳住掌骨、扳近节指骨",
    f"{b('从肘关节那篇抄过来的“肘”')}：表 1 两处写“回答可能提示{red('肘')}部的力量问题”，举的例子却是手腕拇指侧痛、握不住车把",
    f"{b('表 1 分栏放错')}：“力量测试”一栏下面列的全是尺侧按压痛的问题，并不是力量测试",
    f"{b('图号引错')}：表 1 推东西时腕尺侧痛写“见图 7”，图 7 是 Guyon 管；正文说“图 2～11 演示了表 1 的动作”，但图 11 是流程图",
    f"{b('不存在的骨间肌')}：表 1 说麻木“在第 4、5 掌侧骨间肌处提示尺神经”，掌侧骨间肌只有 3 块（也有算 4 块的），而且骨间肌也不是感觉分布区",
    f"{b('琴键试验')}：表 1 说用琴键试验查 TFCC 撕裂，琴键试验主要查的是下尺桡关节不稳",
    f"{b('流程图拼写')}：“compliant”（应为 complaint）、“Unlar claw”、“osetoarthritis”、“Tendititis”；正文还有“Sensor testing”、“extensor carpi radialis longus/radialis”等笔误",
    f"{b('伦理声明')}：写着“梅奥诊所杰克逊维尔院区批准：无”，又说不需要伦理审批",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"视频前请患者{b('露出双手双腕、把手机架稳')}，最好有人帮忙；准备一块手表方便做表带试验",
    f"先问外伤、再看握拳和张手，{b('最痛点在哪一侧')}基本决定后面查什么",
    f"{red('鼻烟窝痛＋外伤')}先按舟骨骨折处理，安排拍片，不要做 Watson 试验",
    "对伏案工作的人，顺便看看他的桌椅、键盘、鼠标摆放，远程给出人体工学建议",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Vomer RP II, Lewno AJ, Udoh I, Albano-Aluquin S, Pujalte GGA. Evaluation of the hand and wrist via telephone and video visit. Cureus. 2023;15(2):e35322. doi:10.7759/cureus.35322</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～10 引自原文，中文标签为编者所加；原文图 11 流程图由编者改画为中文；活动度卡和电话问诊卡据原文正文和表 1 整理改写。"
))

TITLE = "「手腕」远程怎么查手和腕？电话＋视频问诊：握拳看力线、分区触诊、Finkelstein、Phalen 等检查"
PTITLE = "手腕远程评估推文"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>""" + PTITLE + """</title>
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
