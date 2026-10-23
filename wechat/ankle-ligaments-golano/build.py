#!/usr/bin/env python3
"""踝关节韧带解剖图谱（Golanó 2010）推文。

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


def fig(k, title, key=None, w=None, n=None):
    """原文 Figure k → images/img{k+1}.jpg；key 为图中数字标注的中文对照"""
    h = img(n or k + 1)
    if w:
        h = h.replace("width:100%;max-width:100%;", f"width:{w};max-width:{w};")
    t = f"图{k}：{title}"
    if key:
        t += "<br>" + "；".join(f"{i} {x}" for i, x in enumerate(key, 1))
    return h + cap(t)


A = []
A.append(img(1))
A.append(cap("原文首页（KSSTA 2010 年第 18 卷）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Anatomy of the ankle ligaments: a pictorial essay（踝关节韧带解剖：图谱综述）",
    f"{b('作者')}：Pau Golanó, Jordi Vega, Peter A. J. de Leeuw, Francesc Malagelada, M. Cristina Manzanares, Víctor Götzens, C. Niek van Dijk",
    f"{b('机构')}：巴塞罗那大学关节镜与外科解剖实验室 · 阿姆斯特丹大学学术医学中心骨科 等",
    f"{b('期刊')}：Knee Surgery, Sports Traumatology, Arthroscopy（KSSTA）",
    f"{b('年卷期')}：2010;18(5):557-569",
    f"{b('DOI')}：10.1007/s00167-010-1100-x",
    f"{b('文章类型')}：图谱综述（Pictorial essay）",
    f"{b('证据级别')}：原文未标注（属于解剖描述性综述）",
    f"{b('关键词')}：Ankle anatomy · Lateral collateral ligament · Medial collateral ligament · Ankle impingement · Ankle sprain",
], square=True))

A.append(h2("🎯 背景：崴脚最常见，解剖却常被忽视"))
A.append(quote(
    "Ankle ligament injury is the most frequent cause of acute ankle pain. Chronic ankle pain often finds its cause in laxity of one of the ankle ligaments.",
    "踝关节韧带损伤是急性踝痛最常见的原因；慢性踝痛也常常源于某一条踝关节韧带的松弛。",
))
A.append(ul([
    f"{b('内翻')}是最常见的损伤机制：{red('距腓前韧带')}往往最先或唯一受伤；完全断裂时还会累及跟腓韧带和距腓后韧带",
    f"{b('外翻')}损伤：可能伤及三角韧带",
    f"{b('过度背伸')}：可能伤及下胫腓联合韧带",
    f"有踝关节韧带损伤史的人，{b('多达 40%')} 会遗留影响日常生活的症状",
]))
A.append(p(f"这篇来自巴塞罗那解剖实验室的图谱，用 {b('21 幅高清解剖图')}把踝关节韧带一条条讲清楚。"))

A.append(h2("🔴 核心框架：三组韧带"))
A.append(table(
    ["分组", "包含的韧带", "常见损伤机制"],
    [
        ["外侧副韧带", "距腓前韧带、跟腓韧带、距腓后韧带", "内翻扭伤"],
        ["内侧副韧带（三角韧带）", "浅层：胫舟、胫弹簧、胫距后浅、胫跟韧带<br>深层：胫距后深、胫距前深韧带", "外翻扭伤"],
        ["下胫腓联合韧带", "胫腓前韧带、胫腓后韧带（浅部、深部=横韧带）、胫腓骨间韧带", "过度背伸、外旋"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('看懂韧带的走行和松紧变化，才能理解扭伤机制、撞击症和查体')}。"))
A.append(small("说明：图中方位罗盘已改为中文（背侧/跖侧/前方/后方/内侧/外侧/近端/远端），图中数字的含义见每幅图下方。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、外侧副韧带"))
A.append(fig(1, "踝关节前外侧观（解剖）", [
    "距腓前韧带", "胫腓前韧带", "跟腓韧带腓骨附着处", "伸肌上支持带", "伸肌下支持带", "第三腓骨肌腱",
    "趾长伸肌腱", "腓骨肌上支持带", "腓骨肌下支持带", "腓骨短肌腱", "腓骨长肌腱", "趾短伸肌"]))

A.append(h4("🔻1. 距腓前韧带（ATFL）"))
A.append(ul([
    f"{b('最常受伤')}：急诊最常见的踝关节损伤；限制距骨前移和踝跖屈",
    f"{b('双束结构')}：与关节囊关系密切，通常由{b('上、下两束')}组成，两束之间有腓动脉穿支及其与外踝动脉的吻合支穿过；文献报道 1～3 束不等，作者解剖中多为双束",
    f"{b('起止')}：起于外踝前缘，中心平均在腓骨尖近端 {b('10 mm')}；向前内走行，止于距骨体外侧关节面前方",
    f"{b('宽度')}：6～10 mm，与束数无关，提示束数变异不影响功能",
]))
A.append(fig(2, "足踝外侧韧带的骨关节解剖，距腓前韧带通常为两束", [
    "外踝尖", "胫骨", "胫腓前韧带", "胫腓前韧带远侧束", "距腓前韧带上束", "距腓前韧带下束", "距骨外侧关节面",
    "距骨颈", "距骨头", "跟腓韧带", "距跟骨间韧带", "颈韧带", "距舟韧带", "足舟骨"]))
A.append(p(
    f"{b('松紧变化')}：中立位时韧带几乎水平；背伸时向上倾斜，跖屈时向下倾斜。{red('只有在跖屈位才紧张，尤其是合并内翻时最容易受伤')}。"
    f"跖屈时上束紧张、下束松弛；背伸时上束松弛、下束紧张。"
))
A.append(fig(3, "足踝外侧区解剖，显示距腓前韧带与跟腓韧带的形态和关系", [
    "腓骨及腓骨尖", "胫骨（箭头示前结节）", "胫腓前韧带", "胫腓前韧带远侧束", "骨间膜", "腓动脉穿支孔", "距骨",
    "距腓前韧带", "跟腓韧带", "距跟骨间韧带", "伸肌下支持带（已切断）", "距舟韧带", "分歧韧带",
    "腓骨肌滑车（箭头示腓骨肌腱沟）", "腓骨长肌腱", "腓骨短肌腱", "跟腱"], w="64%"))
A.append(fig(4, "外侧韧带解剖，显示跟腓韧带、距跟外侧韧带与距腓前韧带的关系。有学者描述距腓前韧带存在第三束，但作者从未在解剖中见到；本例上束比通常要细", [
    "腓骨尖", "距腓前韧带上束和下束", "跟腓韧带", "距跟外侧韧带", "胫腓前韧带", "胫腓前韧带远侧束", "距骨三角区",
    "距骨外侧关节面", "距骨背侧关节面", "距跟骨间韧带", "颈韧带", "距舟韧带", "足舟骨", "跟骰外侧韧带",
    "分歧韧带（跟舟束）"]))

A.append(h4("🔻2. 跟腓韧带（CFL）"))
A.append(ul([
    f"{b('起止')}：起于外踝前部、距腓前韧带下束正下方（两者之间常有纤维相连）；中立位时向下后斜行，止于跟骨外侧面后部",
    f"{b('形态')}：横截面圆形，直径 6～8 mm，长约 20 mm；不属于关节囊，但与腓骨肌腱鞘后内侧部紧密相连，几乎被其完全覆盖，{b('只有约 1 cm 外露')}",
    f"{b('唯一跨两个关节的韧带')}：同时跨越距小腿关节和距下关节，所以既参与踝屈伸，也允许距下关节运动",
    f"{b('损伤')}：Broström 发现距腓前韧带合并跟腓韧带断裂约占 {b('20%')}，单独的跟腓韧带断裂非常罕见",
]))
A.append(fig(5, "踝关节运动中的跟腓韧带。a 中立位；b 背伸；c 跖屈。跟腓韧带在跖屈时变水平、背伸时变垂直，在整个活动范围内都保持紧张", [
    "跟腓韧带", "腓骨尖", "跟骨", "腓骨肌滑车", "距下关节", "距腓前韧带", "距骨颈", "距跟骨间韧带", "胫骨前结节",
    "胫距前韧带", "胫骨后结节", "距骨外侧突", "跟骰关节", "跟骰外侧韧带", "距舟韧带", "颈韧带", "足舟骨",
    "分歧韧带（跟舟束）", "足底长韧带"]))
A.append(p(
    f"距骨{b('外翻时跟腓韧带松弛、内翻时紧张')}，这解释了为什么即使没有屈伸动作，单纯内翻也能伤到它。"
))
A.append(fig(6, "跟腓韧带与腓骨肌腱的关系", [
    "跟腓韧带", "腓骨长肌腱", "腓骨短肌腱", "腓骨", "距腓韧带", "跟骨", "距下关节", "腓骨肌滑车处的纤维隔",
    "伸肌上支持带", "伸肌下支持带", "趾长伸肌腱", "第三腓骨肌腱", "趾短伸肌", "趾短伸肌腱", "跟腱",
    "Kager 脂肪垫", "第五跖骨粗隆", "足底筋膜外侧束", "小趾展肌"]))
A.append(p(b("跟腓韧带与距跟外侧韧带的变异：")))
A.append(table(
    ["比例", "类型"],
    [
        ["35%", "跟腓韧带由距跟外侧韧带加强（两者相连，在近端或远端分开）"],
        ["23%", "距跟外侧韧带独立存在，位于跟腓韧带前方"],
        ["42%", "没有距跟外侧韧带，由距跟前韧带代替；此时跟腓韧带对距下关节稳定的作用更大"],
    ],
))
A.append(fig(7, "骨关节解剖：跟腓韧带与距跟外侧韧带的关系", ["跟腓韧带", "距跟外侧韧带", "距腓前韧带", "腓骨肌滑车"]))

A.append(h4("🔻3. 距腓后韧带（PTFL）"))
A.append(ul([
    f"{b('起止')}：起于外踝内侧面的踝窝，近乎水平走行，止于距骨后外侧；多束结构，可止于距骨后面、距骨外侧突或三角骨，部分纤维参与构成踇长屈肌腱管",
    f"{b('松紧')}：跖屈和中立位松弛，{b('背伸时紧张')}",
    f"{b('损伤')}：除非出现明显的踝关节脱位，一般不受伤",
]))
A.append(fig(8, "踝关节韧带后面观（解剖）", [
    "腓骨尖", "腓骨的腓骨肌沟", "胫骨", "胫腓后韧带浅部", "胫腓后韧带深部（横韧带）", "距腓后韧带（原文误写为“跟腓后韧带”）",
    "距骨外侧突", "距骨内侧突", "踇长屈肌腱管", "踇长屈肌支持带", "跟腓韧带", "距下关节", "后踝间韧带",
    "趾长屈肌腱（已切断）", "胫骨后肌腱", "腓骨肌腱"]))

A.append(h4("🔻4. 后踝间韧带：后踝撞击的“元凶”之一"))
A.append(p(
    f"距腓后韧带的一部分纤维与{b('后踝间韧带')}融合。它因与{b('后踝软组织撞击综合征')}有关而受到关注。"
))
A.append(ul([
    f"{b('出现率')}：影像和解剖研究报道 19%～100% 不等；作者解剖中{b('恒定存在')}；Oh 等在 77 个标本中见到 63 个（81.8%），MRI 中 26 例全部可见",
    f"{b('差异原因')}：体积小、解剖时难以辨认，也可能与标本数量和人种差异有关；可分为 2～3 束（20%～100%）",
    f"{b('位置')}：后面观位于横韧带和距腓后韧带之间，从外下斜向内上",
    f"{b('松紧')}：背伸时紧张、跖屈时松弛。强力背伸可致其损伤、断裂或撕脱骨折；{red('跖屈时松弛，可能被夹在胫骨和距骨之间，引起撞击')}",
]))
A.append(fig(9, "a 踝关节韧带后面观，显示后踝间韧带、距腓后韧带和横韧带的关系；b T1 加权 MRI，与 a 中各层面对应", [
    "后踝间韧带", "胫腓后韧带浅部", "胫腓后韧带深部（横韧带）", "距腓后韧带", "距骨外侧突", "踇长屈肌腱管"]))
A.append(fig(10, "踝关节韧带后面观，显示后踝间韧带及其周围结构", [
    "腓骨", "腓骨尖", "腓骨的腓骨肌沟", "胫骨", "胫骨后结节", "胫腓后韧带浅部", "胫腓后韧带深部（横韧带）",
    "骨间膜", "距腓后韧带", "距骨外侧突", "踇长屈肌腱管", "踇长屈肌支持带", "跟腓韧带", "距下关节",
    "趾长屈肌腱（已切断）", "胫骨后肌腱（已切断）", "后踝间韧带"], w="64%"))
small("图 10 中后踝间韧带的附着点：A 胫骨附着（关节镜下所见的“胫骨束”）；B 距骨附着（距骨外侧突）；C 经趾长屈肌腱与胫骨后肌腱之间的纤维隔附着于内踝；D 经关节囊附着于距骨内侧突。")
A.append(fig(11, "后踝间韧带（箭头）在后踝软组织撞击中的作用：从背伸（a）到跖屈（d），再回到背伸（f）", [
    "胫腓后韧带浅部", "胫腓后韧带深部（横韧带）", "距腓后韧带", "距骨外侧突", "距骨内侧突", "踇长屈肌腱管",
    "内侧副韧带深层（胫距后深韧带）"]))
A.append(p("自 2000 年 van Dijk 等开展后踝关节镜以来，后方韧带已经可以在镜下清楚观察和处理。"))

A.append(h3("❇️二、内侧副韧带（三角韧带）"))
A.append(ul([
    f"{b('结构')}：多束韧带，分{b('浅、深两层')}；起于内踝，止于距骨、跟骨和足舟骨",
    f"{b('覆盖')}：胫骨后肌腱鞘覆盖其后部和中部，就像外侧的腓骨肌腱鞘覆盖跟腓韧带一样",
    f"{b('分束')}：Milner 和 Soames 描述了 6 个组成部分，其中 3 个恒定存在，3 个可有可无",
]))
A.append(p(b("表 1　内侧副韧带各部分的命名对照")))
A.append(table(
    ["Milner 和 Soames", "Sarrafian"],
    [
        [red("浅层"), ""],
        ["胫弹簧韧带（主要部分）", "胫韧带束"],
        ["胫舟韧带（主要部分）", "胫舟束及胫距前浅束"],
        ["胫距后浅韧带（附加束）", "胫距后浅韧带"],
        ["胫跟韧带（附加束）", "胫跟韧带"],
        [red("深层"), ""],
        ["胫距后深韧带（主要部分）", "胫距后深韧带"],
        ["胫距前深韧带（附加束）", "胫距前深韧带"],
    ],
    first_bold=False,
))
A.append(p(
    f"不过作者在解剖中发现，{u('各束大多彼此连续，很难截然分开，单独指认每一束其实有些人为')}。"
))
A.append(fig(12, "作者解剖中常见的内侧副韧带主要组成示意图。内踝形态有助于理解其起点：内侧面可见前丘和后丘两部分，由丘间沟分开", [
    "胫舟韧带", "胫弹簧韧带", "胫跟韧带", "胫距后深韧带", "弹簧韧带复合体（跖侧及内上跟舟韧带）", "前丘", "后丘",
    "丘间沟", "载距突", "距骨内侧突", "距骨外侧突", "足舟骨", "足舟骨粗隆"]))
A.append(fig(13, "内侧副韧带主要组成部分的内侧观（解剖）", [
    "胫舟韧带", "胫弹簧韧带", "胫跟韧带", "胫距后深韧带", "弹簧韧带复合体（内上跟舟韧带）", "距骨内侧突", "载距突",
    "距跟内侧韧带", "胫骨后肌腱"]))
A.append(fig(14, "内侧副韧带内侧观。大部分被胫骨后肌腱和趾长屈肌腱覆盖，为显示韧带已去除趾长屈肌腱。a 中立位，显示与胫骨后肌腱的关系；b 去除胫骨后肌腱；c 跖屈，双踝轴线前方的部分紧张；d 背伸，双踝轴线前方的部分松弛", [
    "内踝", "距骨外侧突", "载距突", "足舟骨", "胫骨后肌腱", "足舟骨粗隆", "踇长屈肌（已切断）", "踇长屈肌支持带",
    "距跟后韧带", "跟腱（于止点处切断）", "足底长韧带", "弹簧韧带复合体（内上跟舟韧带）", "胫舟韧带",
    "胫弹簧韧带", "胫跟韧带", "胫距后深韧带"], w="86%"))

A.append(h3("❇️三、下胫腓联合韧带"))
A.append(p(
    f"踝穴由胫骨远端和腓骨组成，包住距骨滑车。滑车{b('前宽后窄')}，所以背伸时腓骨要轻微上移并外旋，以适应变宽的距骨；跖屈时相反。"
    f"维持胫腓骨稳定、对抗轴向、旋转和平移分离力的，是三条韧带加上骨间膜下段："
))
A.append(ul([
    "胫腓前韧带（下胫腓前韧带）",
    "胫腓后韧带（下胫腓后韧带）",
    "胫腓骨间韧带",
]))
A.append(p(
    f"骨间韧带止点以下，前方是胫腓滑膜隐窝，后方有一小团脂肪组织，称为{b('滑膜脂肪皱襞')}。它随踝关节运动上下移动：背伸时退缩到胫腓骨之间，跖屈时下降到踝关节内。"
    f"这个结构被认为是崴脚后慢性疼痛的原因之一，即{red('前外侧软组织撞击（下胫腓联合撞击）')}。"
))
A.append(fig(15, "胫腓关节内侧观（已去除距骨）", [
    "外踝关节面", "胫骨远端关节面", "胫腓前韧带（远侧束）", "胫腓后韧带浅部", "胫腓后韧带深部（横韧带）",
    "滑膜脂肪皱襞", "距腓前韧带", "跟腓韧带", "距腓后韧带", "腓距跟韧带（Rouvière-Canela 韧带）"]))

A.append(h4("🔻1. 胫腓前韧带"))
A.append(ul([
    f"{b('起止')}：起于胫骨前结节（平均在关节面上方 5 mm），向远外侧走行，止于外踝前缘；越往远端纤维越长",
    f"{b('分束')}：由多束组成，腓动脉穿支从束间穿过；最远端的纤维在起点处容易和距腓前韧带混淆",
]))
A.append(img(17))
A.append(cap("图16（左）：距小腿关节和足背的前上面观。1 胫腓前韧带；2 胫骨前结节<br>"
             "图17（右）：踝关节前外侧部，显示胫腓前韧带与腓动脉穿支的关系（动脉内灌注黑色乳胶）。"
             "1 胫腓前韧带；2 胫腓前韧带远侧束；3 胫骨前结节；4 腓动脉穿支；5 距骨三角区；6 踝前动脉；"
             "7 距骨外侧关节面；8 距骨背侧关节面；9 距腓前韧带"))
A.append(h4("🔻2. 胫腓前韧带远侧束与前外侧撞击"))
A.append(p(
    f"胫腓前韧带{b('最远端的一束')}看起来独立于其余部分，由纤维脂肪隔分开，位置也稍深。这一束的病变常被认为是{red('前外侧软组织撞击')}的原因；"
    f"切除它（开放或关节镜）常能缓解症状，而且{b('不影响踝关节稳定')}。"
))
A.append(ul([
    f"{b('机制')}：外侧副韧带（如距腓前韧带）损伤 → 前后向松弛增加 → 距骨前移 → 远侧束与距骨接触和压力增加",
    f"{b('解剖因素')}：韧带在腓骨上的止点越低，中立位接触越多，越容易出问题",
    f"{b('正常现象')}：中立位时远侧束与距骨接触在解剖和关节镜下都很常见，应视为正常；关节牵引时接触减少",
    f"{b('不稳是直接因素')}：Akseki 发现切断距腓前韧带不改变中立位的接触，但运动中接触明显变化",
]))
A.append(p(f"{b('临床提示')}：{hl('崴脚后踝前外侧慢性疼痛、关节稳定、X 线正常')}的患者，应考虑这种韧带撞击。"))
A.append(fig(18, "踝关节前方韧带", [
    "胫腓前韧带", "胫腓前韧带远侧束", "胫骨（箭头示前结节）", "距腓前韧带", "距骨斜面三角区", "内侧副韧带深层",
    "内侧副韧带浅层", "Harty 切迹"]))
A.append(fig(19, "足踝韧带的骨关节解剖", [
    "外踝尖", "胫骨（箭头示前结节）", "胫腓前韧带", "胫腓前韧带远侧束", "远侧束胫骨附着处的钙化（影像）",
    "胫腓前韧带与距骨接触区域的关节软骨磨损", "距骨斜面三角区", "距腓前韧带", "跟腓韧带", "距跟外侧韧带",
    "软骨缘", "距舟韧带", "跟骰外侧韧带", "足舟骨", "颈韧带", "外侧楔骨", "骰舟背侧韧带", "楔舟背侧韧带",
    "跟骨（腓骨肌滑车）", "胫骨前肌腱"]))

A.append(h4("🔻3. 胫腓后韧带"))
A.append(ul([
    f"{b('浅部')}：起于外踝后缘，向近内侧止于胫骨后结节；相当于后方的胫腓前韧带，通常所说的“胫腓后韧带”就是指它",
    f"{b('深部（横韧带）')}：呈锥形，起于踝窝近端，止于胫骨后缘、紧贴胫骨下关节面软骨后方，纤维可达内踝；像{b('真正的盂唇')}一样加深关节，防止距骨后移",
]))
A.append(fig(20, "踝关节后方韧带（解剖）", [
    "外踝", "外踝尖", "腓骨肌沟", "胫骨", "胫骨后结节", "胫腓后韧带浅部", "胫腓后韧带深部（横韧带）", "距下关节",
    "距腓后韧带", "后踝间韧带", "距骨外侧突", "踇长屈肌腱管（肌腱已去除）", "距骨内侧突", "跟腓韧带", "趾长屈肌"]))
A.append(fig(21, "踝关节矢状切面（外侧观）", [
    "胫骨", "距骨", "跟骨", "胫腓后韧带", "胫腓后韧带浅部", "胫腓后韧带深部（横韧带）", "距腓后韧带",
    "后踝间韧带", "距下关节", "距小腿关节", "距下关节后关节囊隐窝", "踇长屈肌"], w="64%"))

A.append(h4("🔻4. 胫腓骨间韧带"))
A.append(p(
    "由致密的短纤维、脂肪组织和腓动脉的小分支组成，连接胫骨和腓骨，可看作骨间膜在下胫腓联合处的延续。"
    "有人认为它力学上不重要，也有人认为它是胫腓骨之间的主要连接；Hoefnagels 等认为它对踝关节稳定很重要。"
))

A.append(h3("❇️四、从解剖到临床"))
A.append(table(
    ["机制", "可能受伤的结构"],
    [
        ["内翻", "距腓前韧带最常见，多为单独损伤；约 20% 合并跟腓韧带损伤；也可伤及关节囊、内侧副韧带或胫腓韧带"],
        ["内翻合并跖屈或背伸", "跖屈时病变以前方为主，背伸时以后方为主；还可伤及后踝间韧带、距骨颈骨软骨区或胫骨前下缘"],
        ["外翻", "内侧关节囊和韧带；受距下关节旋转成分影响较大"],
        ["崴脚后", "软组织撞击综合征通常发生在一次扭伤之后"],
    ],
))

A.append(h2("⚖️ 证据评价"))
A.append(ul([
    f"{b('性质')}：解剖图谱综述，以作者团队的尸体解剖观察为主，不涉及临床疗效",
    f"{b('优点')}：解剖图质量极高，系统覆盖外侧、内侧和下胫腓三组韧带，并联系撞击症和关节镜",
    f"{b('原文笔误')}：讲距腓前韧带宽度时写成了“anterior tibiotalar ligament”（胫距前韧带），应为距腓前韧带；图 8 第 6 项写作“posterior calcaneofibular ligament”（跟腓后韧带），按位置应为距腓后韧带",
    f"{b('术语提醒')}：正文说跟腓韧带“extension 时水平、flexion 时垂直”，按欧洲解剖习惯，踝的 extension 指跖屈，与图 5 图注“跖屈时水平、背伸时垂直”一致，阅读原文时容易混淆",
    f"{b('其他')}：后踝间韧带出现率文献差异很大（19%～100%），作者“恒定存在”的结论来自自身解剖经验",
]))

A.append(h2("📌 总结：一张图记住踝关节韧带"))
A.append(p(
    f"{red('① 距腓前韧带')}：最常伤；双束；跖屈＋内翻时最紧、最易伤<br>"
    f"{red('② 跟腓韧带')}：唯一跨踝和距下关节；全程紧张；内翻紧、外翻松；约 20% 合并损伤<br>"
    f"{red('③ 距腓后韧带')}：背伸紧；很少受伤，除非脱位<br>"
    f"{red('④ 后踝间韧带')}：跖屈时可被夹住，导致后踝撞击<br>"
    f"{red('⑤ 三角韧带')}：浅深两层，6 个组成部分，各束实际上难以分开<br>"
    f"{red('⑥ 下胫腓联合')}：胫腓前、后、骨间韧带；胫腓前韧带远侧束可致前外侧撞击"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Golanó P, Vega J, de Leeuw PAJ, Malagelada F, Manzanares MC, Götzens V, van Dijk CN. Anatomy of the ankle "
    "ligaments: a pictorial essay. Knee Surg Sports Traumatol Arthrosc. 2010;18(5):557-569. doi:10.1007/s00167-010-1100-x</em><br>"
    "本文以开放获取（CC BY-NC）发表。文中图片均来自原文，图中方位罗盘与“Level”标注已改为中文，表 1 已译为中文，仅用于学术交流。"
))

TITLE = "「踝关节」一篇看懂踝关节韧带：21 幅解剖图谱精读"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>踝关节韧带解剖推文</title>
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
