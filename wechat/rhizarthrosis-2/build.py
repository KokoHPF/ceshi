#!/usr/bin/env python3
"""拇指腕掌关节骨关节炎 Part II 手法与训练新方案（Colonna、Borghi 2024）推文。

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
    "Colonna S, Borghi C. Rhizarthrosis Part II: A New Approach of Manual Therapy and Therapeutic Exercise. Cureus. 2024;16(1):e52999. doi:10.7759/cureus.52999",
    "作者单位：意大利博洛尼亚 Spine Center、Osteopathic Spine Center Education（OSCE）",
    f"文章类型：{b('技术报告')}（提出方案，没有患者数据；上篇是文献综述）",
], square=True))

A.append(h2("先说为什么提出这个方案"))
A.append(p(
    f"上篇介绍过，拇指腕掌关节骨关节炎在{b('Eaton-Littler Ⅰ、Ⅱ期')}首选保守治疗。但作者指出两个空白："
))
A.append(ul([
    f"{b('手法技术没有比较')}：神经动力学、Kaltenborn、Mulligan、Maitland 这几种技术的研究几乎都出自同一个团队，没有比较过哪种更好",
    f"{b('运动训练不够专门')}：唯一结合手法和运动的研究用的是一套并非针对腕掌关节、也非针对手骨关节炎的通用练习",
]))
A.append(p(f"所以作者从腕掌关节的生物力学出发，提出{b('3 步手法＋以第一背侧骨间肌为核心的居家训练')}。"))
A.append(pic(2, "原文图 1：患侧外展受限"))

A.append(h2("生物力学依据"))
A.append(ul([
    "稳定靠韧带（主要是前斜韧带和背桡侧韧带）和肌肉的平衡；前斜韧带松弛被认为是软骨退变的起点",
    "用指尖捏 1 kg 时，腕掌关节承受约 12 kg 压力",
    f"{mk('第一背侧骨间肌')}：起于第一、第二掌骨，止于示指近节。尸体实验中，侧捏时去掉它的张力，第一掌骨基底向桡侧半脱位，恢复张力后复位",
    f"掌骨屈曲约 30° 时关节最吻合。此时{b('拇收肌（斜头）和拇对掌肌')}把掌骨基底往桡侧推（促半脱位），{b('第一背侧骨间肌')}则对抗这个力",
    f"作者的推论：{b('多用第一背侧骨间肌、少用拇收肌')}，可以减少关节囊韧带的牵拉和软骨的挤压",
]))

A.append(h2("重点一：3 步手法"))
A.append(img(3))
A.append(cap("方案总览（编者根据原文整理）"))
A.append(p("患者仰卧或坐位，治疗师坐在患侧。"))
A.append(h3("第 1 步（被动）：牵引分离"))
A.append(pic(4, "原文图 4：腕掌关节牵引分离"))
A.append(ul([
    "靠近患者的手固定腕（桡骨）、拇指压住大多角骨；同侧手的拇指和示指捏住第一掌骨；另一只手抓住拇指近节，做Ⅲ级牵引，让关节面分开",
    f"做 {b('15 次')}，幅度和节奏以{b('最多轻微不适或轻痛')}为限",
]))
A.append(h3("第 2 步（主动）：收缩-放松-再外展"))
A.append(pic(5, "原文图 5：第 2 步的手法"))
A.append(ul([
    "握腕那只手的拇指找到腕掌关节线，把第一掌骨基底向内、向远端推",
    "另一只手的示指和拇指像撬杠一样把掌骨推向外展，到疼痛允许的最大角度",
    f"患者{b('等长内收拇指 3～5 秒')} → 放松 3～5 秒 → 治疗师两手合力再加大外展（仍在疼痛范围内）",
    f"重复 {b('3～5 次')}。这是整骨的“肌肉能量技术”，目的是拉长把掌骨基底维持在错误位置的僵硬肌筋膜",
]))
A.append(h3("第 3 步（主动）：Mulligan 动态松动下张开手指"))
A.append(pic(6, "原文图 6：在固定点下主动张开手指"))
A.append(ul([
    "治疗师保持对第一掌骨基底向内、向远端的推力，另一只手的拇指抵住示指桡侧",
    f"患者有节奏地{b('最大张开手指 15 次')}，或最大收缩 5 秒、休息 5 秒，重复 3～5 次",
    "张开手指时外展肌和第一背侧骨间肌（作为示指外展肌）收缩，拇收肌、屈肌、对掌肌相对放松",
    "Mulligan 动态松动的原则：在无痛的矫正滑动下做原本会痛的动作；以前认为是纠正了“位置错误”，现在更多认为是神经生理机制，还可能包括降低运动恐惧和安慰剂效应",
]))

A.append(h2("重点二：居家训练第一背侧骨间肌"))
A.append(pic(7, "原文图 7：治疗师辅助"))
A.append(pic(8, "原文图 8：用另一只手固定"))
A.append(pic(9, "原文图 9：用桌边固定"))
A.append(ul([
    f"橡皮筋套在手指上，{b('最大限度张开手指')}，每次 5～10 下或等长保持 5 秒",
    f"{mk('关键是先固定拇指')}：不让腕掌关节内收，让它成为第一背侧骨间肌的固定点——可以由治疗师抵住、用另一只手的示指顶住第一掌骨基底，或用电脑、桌子的边缘顶住",
    "这种练法几乎不让腕掌关节活动",
    f"理想频率：{b('每天 10～15 次')}，两次之间休息 5～10 分钟",
]))
A.append(img(10))
A.append(cap("剂量和进阶（编者根据原文整理）"))

A.append(h2("这个方案能信几分"))
A.append(ul([
    f"{b('完全是理论方案')}：没有任何患者数据，作者自己强调必须先做对照临床试验验证，并用肌电研究确认训练时到底是哪些肌肉在收缩",
    f"{b('“撑指练第一背侧骨间肌”未经验证')}：张开手指会同时动员所有背侧骨间肌、小指展肌等；第一背侧骨间肌能否被“选择性”强化，拇收肌是否真的被抑制，都没有测过",
    f"{b('生物力学依据较老')}：关键证据来自数十年前的尸体和模型研究；第一背侧骨间肌的稳定作用也有不同看法",
    f"{b('可取之处')}：手法步骤和居家练习描述得具体、器材简单，可以作为临床尝试和研究设计的起点；“先固定拇指再撑指”的提示很实用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('橡皮筋位置')}：摘要和正文都写橡皮筋“套在拇指和小指之间”，但图 7～9 中橡皮筋套在示指到小指上，拇指被单独固定",
    f"{b('训练频率前后不一')}：摘要写“全天重复”，正文写“每天 10～15 次、间隔 5～10 分钟”",
    f"{b('“掌骨头”还是“基底”')}：第 2、3 步正文写治疗师接触“掌骨头”（远端），图 5 图注和作用原理都是推第一掌骨的近端（基底）",
    f"{b('牵引定义矛盾')}：与上篇相同，前一句说牵引垂直于关节面，后一句又说Ⅲ级牵引是“沿平行轴施加的额外力”",
    f"{b('图 1 图注')}：写“拇指第一节外展增加”，实际表现是掌指关节代偿性过伸",
    f"{b('第 2 步内容不一')}：正文让患者等长内收，图 5 图注写“等长内收/对掌”",
    f"{b('引用夸大')}：讨论说已有文献证明运动“能纠正关节面的位置异常”，引用的却是 Mulligan“位置错误”假说的文献，作者在前文自己也说这一假说已被神经生理机制取代",
    f"{b('其他')}：摘要中有一句重复了两遍；“MVMs”应为 MWMs；没有招募受试者却勾选了“已获受试者同意”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('可以当作 Eaton Ⅰ、Ⅱ期患者的一个尝试方案')}：牵引分离 → 收缩-放松-再外展 → 固定下张开手指，再配合居家撑指训练",
    f"{b('居家撑指的要点')}：一定先把拇指固定住（另一只手或桌边），不要让拇指跟着往里收",
    "剂量以疼痛为指导：手法最多轻微不适，训练按疼痛决定是否加量",
    "仍应配合支具、关节保护和日常动作调整；效果要用疼痛、捏力和功能问卷跟踪",
    "这是未经验证的方案，向患者说明，并和已有证据的治疗（支具、运动、手法组合）一起使用",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Colonna S, Borghi C. Rhizarthrosis Part II: A New Approach of Manual Therapy and Therapeutic Exercise. Cureus. 2024;16(1):e52999. doi:10.7759/cureus.52999</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流中文解读：原文图 1、4～9 引自原文，图中中文标签为编者所加；方案卡由编者整理。原文图 2、3 为经许可转载自其他出版物的图片，本文未使用。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「拇指根部痛」拇指腕掌关节炎（下）：3 步手法＋橡皮筋撑指，练第一背侧骨间肌稳住拇指"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>拇指腕掌关节炎（下）推文</title>
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
