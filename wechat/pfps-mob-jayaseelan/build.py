#!/usr/bin/env python3
"""髌股疼痛的功能位关节松动（Jayaseelan 2020）推文。

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


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2020 年第 15 卷第 4 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Functional Joint Mobilizations for Patellofemoral Pain Syndrome: A Clinical Suggestion（髌股疼痛综合征的功能位关节松动：临床建议）",
    f"{b('作者')}：Dhinu J. Jayaseelan, DPT, OCS, FAAOMPT · Cameron Holshouser, DPT · Michael W. McMurray, DPT, OCS, FAAOMPT",
    f"{b('机构')}：乔治·华盛顿大学健康、人体功能与康复科学系；Total Motion Physical Therapy；弗吉尼亚大学物理与作业治疗；弗吉尼亚骨科手法物理治疗研究所（美国）",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2020;15(4):643-649",
    f"{b('PMCID')}：PMC7735690",
    f"{b('文章类型')}：临床建议（Clinical Suggestion）",
    f"{b('证据级别')}：5 级",
    f"{b('关键词')}：anterior knee pain · manipulation · manual therapy · mobilization · movement system",
], square=True))

A.append(h2("🎯 背景：躺着推髌骨不痛，一蹲就痛怎么办？"))
A.append(p(
    f"髌股疼痛综合征（PFPS）很常见：成人年患病率 {b('23%')}，青少年 {b('29%')}；约 {b('50%')} 的患者症状持续，有的长达数十年，还可能与早发骨关节炎和慢性疼痛有关。"
))
A.append(ul([
    f"完全伸膝时髌骨不与股骨髁接触，可以自由滑动；屈膝 {b('20°～30°')} 时髌骨下关节面开始接触，{b('60°～90°')} 时接触面积最大",
    f"负重大幅增加髌股关节压力：步行约 {b('1.3 倍体重')}，上下楼 {b('3.3 倍')}，跑步 {b('5.6 倍')}，深蹲可达 {b('7.8 倍')}——难怪多数患者在负重屈膝活动中痛",
    "运动和负荷管理是一线治疗，但很多人长期不改善，可能还有运动解决不了的问题：髌骨内滑受限，阔筋膜张肌、髂胫束或外侧支持带紧张，都可能增加屈膝时外侧关节负荷",
    f"PFPS 患者还可能存在{b('中枢疼痛处理异常')}：心理功能改变、时间总和增强、条件性疼痛调制受损、广泛痛觉过敏、体感改变、心理困扰、双侧触觉敏感性下降",
    "关节松动能改善活动度、降低伤害感受兴奋性、增强疼痛调制、减轻广泛痛觉过敏、改善心理结局",
]))
A.append(p(
    f"但髌股关节松动通常在{b('非负重伸膝位')}做——最容易感到活动度，却很少诱发症状，这可能是单独松动效果有限的原因之一。"
    f"作者提出：{hl('在诱发症状的功能位（屈膝、负重）做髌骨松动')}。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["步骤", "体位", "目的"],
    [
        ["1", "仰卧屈膝中段，髌骨内滑（图1）", "复制诱发症状的屈膝角度（蹲、上下楼），但不负重、压力小"],
        ["2", "静态弓步部分负重，髌骨内滑（图2）", "症状出现在负重活动范围某一点时"],
        ["3", "弓步中的动态松动（MWM）（图3）", "闭链屈膝时维持内滑"],
        ["4", "腿举中的动态松动（图4）", "可逐步加负荷，从部分负重到全体重或更多"],
        ["5", "深蹲中的动态松动（图5）", "单腿或双腿蹲时持续滑动或分级摆动"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('在患者“哪里痛就在哪里推”——从仰卧屈膝到静态弓步，再到弓步、腿举、深蹲中的动态松动，逐步负重、逐步功能化')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、为什么要在功能位松动"))
A.append(ul([
    "部分 PFPS 患者同时存在外周和中枢疼痛机制问题；关节松动可抑制异常疼痛机制，再加上生物力学作用，可作为有力的辅助手段",
    "屈膝时髌股吻合度增加、活动度下降，在诱发症状或受限的角度松动，可能改善髌股负荷分散、减轻疼痛",
    f"研究显示，{b('尽早找到并改善患者的主要诱发动作（可比较征）')}，出院时结局更好",
    "疼痛的动作常导致代偿或回避；让动作不那么痛，就可能变得更“功能”",
]))

A.append(h3("❇️二、五步进阶：从不负重到负重"))
A.append(pic(2, "图1（左）：非负重屈膝位的髌骨内滑；图2（右）：静态负重屈膝位的髌骨内滑"))
A.append(ul([
    f"{b('图1 仰卧屈膝中段')}：复制蹲、上下楼时的膝角，但去掉负重，压力较小",
    f"{b('图2 静态弓步')}：部分负重；适合负重时活动范围中某一点出现症状的患者",
]))
A.append(pic(3, "图3：单腿弓步中的髌骨内滑动态松动——a 起始位，b 结束位"))
A.append(ul([
    f"{b('图3 弓步中的动态松动（MWM）')}：滑动方向取决于哪个方向能减轻症状，和/或治疗师感觉哪个方向受限；示例中在闭链屈膝过程中维持内滑",
]))
A.append(pic(4, "图4：腿举中的髌骨内滑动态松动——a 起始位，b 结束位"))
A.append(ul([
    f"{b('图4 腿举')}：可加负荷，从部分负重进阶到全体重甚至更多；整个动作中维持内滑，理论上减少外侧关节的过度压力",
]))
A.append(pic(5, "图5：双腿深蹲中的髌骨内滑动态松动——a 起始位，b 结束位"))
A.append(ul([
    f"{b('图5 自重深蹲')}：患者做单腿或双腿蹲时，治疗师施加持续滑动或分级摆动",
    "按患者的症状和功能受限任务，还可以选其他体位；诊室有效的话，可以设计类似的家庭训练",
]))

A.append(h3("❇️三、剂量怎么定：看目的"))
A.append(table(
    ["主要问题", "手法选择", "持续时间"],
    [
        ["以疼痛为主（疼痛影响其他训练）", "低级别松动，不进入组织阻力屏障，通过神经生理作用减轻疼痛、使神经系统脱敏", "时间短，避免激惹症状，松动间给休息"],
        ["以僵硬为主", "高级别松动，从力学上改善活动、降低组织阻力", "做到感觉组织阻力改变为止，通常比镇痛更久"],
    ],
))
A.append(ul([
    "作者认为不宜给统一处方，手法应以患者为中心",
    "屈膝位髌股吻合度高，可用的活动度减少，可能难以评估现有关节活动",
    f"{b('动态松动（MWM）')}：维持一个能减痛的滑动，让患者主动做原来痛的动作；若该方向不减痛，就换方向，直到找到减痛的滑动（如果有）",
    "可调整推髌骨的角度，以适应股骨髁的解剖位置",
    "关节运动学原则来自尸体和正常关节的研究，病理、疼痛或活动受限时未必适用；例如粘连性关节囊炎中，反方向滑动反而更能改善活动度——手法要结合实时的临床推理",
]))

A.append(h3("❇️四、讨论：不是人人都要松动"))
A.append(ul([
    "PFPS 难治，部分原因是整条下肢动力链的多种损害、训练错误、鞋子、跑步地面以及可能的中枢疼痛处理异常",
    f"与其他干预联合时，关节松动能减轻疼痛、改善功能，效应量{b('中到大')}；但现有研究多在仰卧位做，可能对功能任务迁移有限",
    f"{red('作者并不建议所有 PFPS 患者都做关节松动')}：很多人没有活动受限，而是控制已有活动的能力不足，此时特定训练和负荷管理更有益",
    f"关节松动主要用于{b('有疼痛或活动受限')}时，而且{b('不应单独使用')}",
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：5 级临床建议，基于作者经验（“在疑难病例中效果不错”），没有研究验证功能位松动的效果，作者也明确说需要研究",
    f"{b('亮点')}：思路清楚——把常规松动从“不痛的位置”搬到“痛的位置”，并给出从不负重到负重的五步进阶，临床容易上手",
    f"{b('局限')}：没有给出具体剂量、级别或进阶标准；屈膝位髌骨活动度小，手法评估难度增加；负重位操作对治疗师体位和力量要求较高",
    f"{b('适用人群')}：主要针对存在疼痛或活动受限、单纯运动效果不好的顽固性 PFPS，不能替代运动和负荷管理",
    f"{b('小瑕疵')}：“arthokinematic” 拼写错误；图注中均为内滑示例，其他方向未展示",
]))

A.append(h2("📌 总结：髌股痛的功能位松动"))
A.append(p(
    f"{red('① 思路')}：髌股痛多在负重屈膝时出现，松动也应在这些位置做<br>"
    f"{red('② 五步进阶')}：仰卧屈膝 → 静态弓步 → 弓步 MWM → 腿举 MWM → 深蹲 MWM<br>"
    f"{red('③ 方向')}：选能减痛或感觉受限的方向，示例为内滑；不减痛就换方向<br>"
    f"{red('④ 剂量')}：以痛为主用低级别、短时间；以僵硬为主用高级别，做到阻力改变<br>"
    f"{red('⑤ 适应证')}：有疼痛或活动受限时才用，并与运动和负荷管理结合<br>"
    f"{red('⑥ 证据')}：目前只是经验性建议，有效性有待研究"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Jayaseelan DJ, Holshouser C, McMurray MW. Functional Joint Mobilizations for Patellofemoral Pain Syndrome: A Clinical Suggestion. "
    "Int J Sports Phys Ther. 2020;15(4):643-649. PMCID: PMC7735690.</em><br>"
    "文中图片均来自原文（图中仅有 a、b 字母，器械上的英文商标已模糊）；原文无表格，文中表格为整理，仅用于学术交流。"
))

TITLE = "「膝关节」髌股痛：哪里痛就在哪里推？功能位髌骨松动五步进阶"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>髌股功能位松动推文</title>
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
