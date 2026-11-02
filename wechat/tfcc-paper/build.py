#!/usr/bin/env python3
"""TFCC 与下尺桡关节超声解剖 推文正文生成。

用法：python3 tools/make_figs.py work images <中号字体> <粗体> && python3 build.py → article_body.html 和 preview.html
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
def I(n, c): A.append(img(n)); A.append(cap(c))
I(1, "原文信息（编者中文重排）")
A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Winnett C, Fenech M. Sonographic Anatomy and Imaging of the Triangular Fibrocartilage Complex and the Distal Radio-Ulnar Joint. Australas J Ultrasound Med. 2025;28:e70012. doi:10.1002/ajum.70012",
    "作者单位：澳大利亚中央昆士兰大学健康、医学与应用科学学院；I-MED Radiology；亚历山德拉公主医院、皇家布里斯班妇女医院医学影像科",
    f"文章类型：{b('综述')}（附示意图、MRI、超声图和视频）；CC BY 4.0 开放获取",
], square=True))
A.append(p(f"尺侧腕痛常被称为腕部的“{b('腰痛')}”或“{b('黑匣子')}”。这篇综述把三角纤维软骨复合体（TFCC）和下尺桡关节（DRUJ）拆成一个个能用超声看到的结构，逐个讲解剖、怎么扫、正常长什么样。"))
A.append(h2("先说结论"))
I(2, "原文要点（编者整理）")

A.append(h2("一、尺侧腕痛：鉴别诊断很多"))
I(3, "尺侧腕痛的原因（据原文整理）")
A.append(p(f"临床上这些病变{b('常常同时存在')}，所以单靠查体很难定位，超声常被用来找结构性改变、引导注射止痛。不过 TFCC 深部和中央部仍需 MRI。"))

A.append(h2("二、检查体位与探头"))
I(4, "原文图 1（编者中文图例）  尺侧腕部超声检查体位")
A.append(ul([
    f"患者{b('坐位面对检查者')}，前臂垫枕抬到肩高；手旋前（掌心向下），或把腕尺侧朝向天花板",
    "这样检查中可以做屈腕、伸腕、桡偏、尺偏",
    f"背侧、掌侧、尺侧{b('三个方向都要扫')}；耦合剂要多",
    f"{b('宽探头')}看骨性结构和下尺桡关节全貌；{b('小探头')}在动态动作中保持接触，并绕过尺骨茎突的骨性突起",
]))

A.append(h2("三、下尺桡关节（DRUJ）"))
I(5, "下尺桡关节解剖（据原文整理）")
I(6, "原文图 2（编者中文标注）  腕部关节与尺骨头")
A.append(p(f"TFCC 的主要功能是{b('稳定下尺桡关节')}、作为尺腕间隙的减震垫；背侧和掌侧桡尺远侧韧带随腕的位置协同稳定关节。{mk('TFCC 和下尺桡关节交织在一起，超声上不能单独评估，必须一起看')}。"))
A.append(h3("外在稳定结构：旋前方肌、骨间膜"))
A.append(ul([
    f"{b('旋前方肌')}：前臂远端掌侧的梯形肌，分浅、深两头，负责旋前；由正中神经的分支{b('骨间前神经')}支配（神经在肌肉深面，也支配下尺桡关节感觉）。它绷紧关节囊，防止冗余囊袋在旋转时卡入关节，并限制桡骨相对尺骨向背侧移位",
    f"{b('骨间膜')}：桡尺骨之间的宽片状结缔组织，防止桡骨向近端移位和向背侧移位；最远端增厚为{b('远侧斜束')}，止于桡骨乙状切迹背侧下缘，协助稳定下尺桡关节",
    f"前臂骨折（尤其 {b('Galeazzi 骨折')}）要评估骨间膜，它常伴骨间膜损伤和下尺桡关节脱位或半脱位",
]))
I(7, "原文图 3（编者中文标注）  旋前方肌、骨间膜")
A.append(h3("怎么扫下尺桡关节"))
A.append(ul([
    f"看关节完整性、骨性改变、滑膜炎和不稳；骨赘提示退变，严重 TFCC 撕裂可致关节不稳、进行性关节炎",
    f"在{b('旋前和最大旋后')}两个位置都要扫；做内外、远近方向的动态扫查",
    f"向近端扫到{b('旋前方肌水平')}：关节积液会向近端延伸，可在短轴和长轴上测量",
]))
I(8, "原文视频 1 截图（编者中文标注）  下尺桡关节积液：背侧入路长轴，由尺侧扫向桡侧")

A.append(h2("四、TFCC 的五个组成部分"))
A.append(p(f"TFCC 的命名在文献里很混乱，作者采用最一致的五部分：{b('① 关节盘 ② 半月板同系物 ③ ECU 腱下鞘 ④ 掌侧尺腕韧带（尺月、尺三角）⑤ 背侧和掌侧桡尺远侧韧带')}。它的三大功能：稳定下尺桡关节、稳定尺腕间隙、缓冲并传导腕部负荷。"))
I(9, "原文图 4（编者中文标注）  TFCC 的五个组成部分（背侧观）")

A.append(h3("1. 关节盘"))
I(10, "关节盘（据原文整理）")
I(11, "原文图 5（编者中文标注）  关节盘")
A.append(p(f"作者特意不用“关节软骨盘”这个叫法，因为它是{b('纤维软骨')}而非透明软骨——纤维软骨富含致密编织的胶原纤维，抗压能力强，和椎间盘、耻骨联合、膝半月板同类。超声上关节盘与近端的尺骨关节软骨、远端的 MH 体部可以区分，改变声束角度可见回声差异。"))
A.append(p(f"{red('局限：')}超声{b('不能可靠排除关节盘中央撕裂')}，尤其正尺骨变异时中央负荷大大增加；怀疑中央撕裂要做 MRI，MRI 还能显示月骨、三角骨、尺骨头的软骨软化。"))

A.append(h3("2. 半月板同系物（MH）"))
I(12, "半月板同系物与茎突前隐窝（据原文整理）")
I(13, "原文图 6（编者中文标注）  半月板同系物的四个部分")
A.append(p(f"{b('尺侧副韧带')}：位于 MH 浅面、ECU 腱下鞘深面的薄纤维韧带，是否真实存在有争议；超声上无法与 MH 或 ECU 腱下鞘区分，常被称为“尺侧关节囊”。"))
I(14, "原文视频 2 截图（编者中文标注）  茎突前隐窝内的气泡")

A.append(h3("3. ECU 腱下鞘"))
I(15, "ECU 腱下鞘（据原文整理）")
I(16, "原文图 7（编者中文标注）  尺骨远端水平的 ECU 腱下鞘")
A.append(p(f"伸肌支持带不直接附着尺骨，作用是防止 ECU 肌腱收缩时“弓弦样”弹起；腱下鞘的位置随旋前、旋后、中立位改变，中立位时位于尺骨茎突背内侧，与尺侧副韧带几乎分不开。"))

A.append(h3("4 和 5. 掌侧尺腕韧带、桡尺远侧韧带"))
I(17, "掌侧尺腕韧带与桡尺远侧韧带（据原文整理）")
I(18, "原文图 8（编者中文标注）  掌侧尺腕韧带")
A.append(p(f"腕背侧的尺月、尺三角关节没有专门的韧带，只称“背侧关节囊”。桡尺远侧韧带深层包绕关节盘并与其周缘融合，所以关节盘周缘更厚；浅、深层分别止于茎突和小凹，在尺侧形成{b('“四臂”结构')}。"))
I(19, "原文图 9（编者中文标注）  桡尺远侧韧带在不同体位的紧张状态")
A.append(table(["体位", "紧张的韧带"], [
    ["旋前", "背侧桡尺远侧韧带浅层 + 掌侧桡尺远侧韧带深层"],
    ["旋后", "背侧桡尺远侧韧带深层 + 掌侧桡尺远侧韧带浅层"],
]))
A.append(tcap("据原文第 4.6 节整理"))

A.append(h2("五、超声和 MRI 怎么分工"))
I(20, "超声 vs MRI（据原文整理）")
A.append(table(["结构", "超声能否评估", "扫查要点"], [
    ["下尺桡关节", "能（积液、骨赘、滑膜炎、不稳）", "旋前 + 最大旋后；向近端扫到旋前方肌"],
    ["关节盘外周", "能", "背侧入路屈腕桡偏；尺侧入路以 ECU 为声窗"],
    ["关节盘中央、下隐韧带", "不能可靠排除", "需 MRI / MR 关节造影"],
    ["半月板同系物", "能看，深部撕裂不能排除", "背尺侧长轴，桡偏尺偏看滑动"],
    ["ECU 腱下鞘", "尺骨远端水平最稳定", "远端定义尚不清楚"],
    ["掌侧尺腕韧带", "能（部分 / 完全撕裂）", "掌尺侧长轴，屈肌腱深面"],
    ["桡尺远侧韧带", "能", "背、掌侧长轴，旋前旋后动态看"],
]))
A.append(tcap("各结构超声评估要点（据原文整理）"))

A.append(h2("原文对不上的地方"))
I(21, "编者核对原文时发现")
A.append(p(f"原文还把 Kienböck 病拼成了“Keinbock”。以上不影响主要结论，供阅读原文时参考。"))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Winnett C, Fenech M. Sonographic Anatomy and Imaging of the Triangular Fibrocartilage Complex and the Distal Radio-Ulnar Joint. Australas J Ultrasound Med. 2025;28:e70012. doi:10.1002/ajum.70012</em><br>"
    "原文为 CC BY 4.0 开放获取（© 2025 The Author(s)，Wiley 代澳大拉西亚超声医学会出版）。本文为中文解读：原文图 1～9 及视频 1、2 截图引自原文，编者将图内英文改为中文并在图下加中文图例条；其余整理卡由编者根据原文撰写。"
))
TITLE = "「腕关节」尺侧腕痛查什么？TFCC 和下尺桡关节超声解剖一次看懂"
PTITLE = "TFCC 超声解剖推文"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<!DOCTYPE html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>""" + PTITLE + """</title>
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
