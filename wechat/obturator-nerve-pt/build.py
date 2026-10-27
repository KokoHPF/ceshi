#!/usr/bin/env python3
"""髋关节镜术后顽固臀部痛的闭孔神经靶向物理治疗 2 例（Saito 等 2025）推文。

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
    "Saito M, Kawabata M, Shimizu S, Omodani T. Ultrasound-Guided Obturator Nerve-Targeted Physical Therapy for Persistent Buttock Pain After Hip Arthroscopy for Femoroacetabular Impingement: A Report of Two Cases. Cureus. 2025;17(10):e95021. doi:10.7759/cureus.95021",
    "作者单位：日本东京 Advanced Orthopaedics 康复科与骨科、北里大学医疗卫生学部",
    f"文章类型：{b('病例报告')}（2 例，原文附 8 段操作和超声视频）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"股骨髋臼撞击症（FAI）关节镜术后 8～11 个月仍有{b('臀部痛')}的 2 例患者，FABER 试验诱发臀部痛，超声下{b('闭孔外肌收缩差')}、{b('闭孔神经周围压痛')}",
    f"作者怀疑是{b('闭孔神经关节支')}卡压或滑动受限：每周超声引导手法＋闭孔外肌激活，每两周闭孔神经{b('水分离')}，注射后做“牵拉—放松”神经滑动",
    f"每次治疗后 FABER 痛、膝－床距离、闭孔外肌收缩都{b('当场改善')}；病例 1 第 4 次步行痛消失，两例随访 6 个月以上未复发",
    f"但{red('只有 2 例、没有对照')}，几种方法同时用，还需要更多研究验证",
]))

A.append(h2("一、为什么关注术后臀部痛"))
A.append(img(2))
A.append(cap("背景（编者根据原文整理）"))
A.append(img(3))
A.append(cap("两位患者（据原文整理）"))
A.append(img(4))
A.append(cap("原文图 1：FABER 位测膝－床距离"))
A.append(p(f"病例 1 患侧膝－床距离 {b('35.5 cm')}，健侧 26.5 cm；病例 2 患侧 {b('31.0 cm')}，健侧 24.5 cm。两人髋外旋徒手肌力都只有 {b('2 级')}（侧卧屈髋 90°、对抗内旋，无法抗重力保持体位）。"))

A.append(h2("二、闭孔神经关节支：一个“急转弯”"))
A.append(img(5))
A.append(cap("作者的解剖推理（据原文讨论整理）"))
A.append(img(6))
A.append(cap("原文图 5：闭孔神经关节支的走行"))
A.append(p(f"另有研究发现，髋伸展加外展会让闭孔神经向远端移动。作者认为 FABER 位诱发臀部痛，可能也是类似的{b('神经牵拉机制')}。"))

A.append(h2("三、怎么治疗"))
A.append(img(7))
A.append(cap("治疗方案（原文）"))
A.append(img(8))
A.append(cap("原文图 2：闭孔神经短轴滑动手法"))
A.append(img(9))
A.append(cap("原文图 3：超声反馈下激活闭孔外肌"))
A.append(img(10))
A.append(cap("原文图 4：闭孔神经长轴滑动（牵拉—放松）"))
A.append(p(f"水分离的位置选在{b('闭孔外肌深层')}、闭孔管远端。作者引用尸体研究：在闭孔管稍远处注射，药液可以扩散到关节支。注射后立刻配合“牵拉—放松”动作，{b('希望既发挥药液作用，又促进神经滑动')}。"))

A.append(h2("四、结果"))
A.append(img(11))
A.append(cap("疗程中的变化（据原文表 1 重画）"))
A.append(tcap("原文表 1：每次治疗时的评估（第 1～4 次治疗）"))
A.append(table(["", "0 周", "1 周", "2 周", "4 周"], [
    ["病例 1 FABER 痛（NRS）", "5", "3", "—", "0"],
    ["病例 1 膝－床距离（cm）", "26.8", "23.5", "22", "22"],
    ["病例 1 闭孔外肌分级", "2", "3", "4", "4"],
    ["病例 1 步行痛", "有", "有", "有", "无"],
    ["病例 2 FABER 痛（NRS）", "7", "2", "2", "—"],
    ["病例 2 膝－床距离（cm）", "21", "20", "20", "—"],
    ["病例 2 闭孔外肌分级", "2", "3", "4", "—"],
    ["病例 2 步行痛", "有", "有", "无", "—"],
]))
A.append(p(f"作者认为，注射后症状{b('立即')}改善，说明神经减压可能起了主要作用，之后再靠针对性的康复维持效果。最后一次治疗后随访{b('超过 6 个月')}，两例臀部痛都没有复发。"))

A.append(h2("这篇文章能信几分"))
A.append(img(12))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('2 例病例报告')}、没有对照，作者也承认不能排除安慰剂效应、霍桑效应、自然恢复或单纯康复的作用",
    "水分离、手法、运动治疗同时使用，分不清各自贡献；没有使用 HOS-ADL、iHOT-33 等标准化量表",
    "超声触诊的按压力度没有量化，阴部神经也没有评估",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "正文写首诊膝－床距离为 35.5 cm（病例 1）、31.0 cm（病例 2），表 1 第 1 次却是 26.8 cm、21 cm，甚至比正文给的健侧值还小",
    "正文测的是“髋外旋徒手肌力”，表 1 记为“闭孔外肌分级”，两者不完全是一回事",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"髋关节镜术后顽固臀部痛，关节内注射无效时，可以考虑{b('闭孔神经关节支和闭孔外肌')}这个方向",
    "查体线索：FABER 诱发臀部痛、膝－床距离增大、髋外旋无力；有条件时用超声看闭孔外肌收缩和闭孔神经周围压痛",
    f"治疗师可做的部分：超声反馈下{b('闭孔外肌激活')}、髋内旋外展↔外旋内收的{b('神经滑动')}练习；水分离须由有资质的医生操作",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Saito M, Kawabata M, Shimizu S, Omodani T. Ultrasound-Guided Obturator Nerve-Targeted Physical Therapy for Persistent Buttock Pain After Hip Arthroscopy for Femoroacetabular Impingement: A Report of Two Cases. Cureus. 2025;17(10):e95021. doi:10.7759/cureus.95021</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～5 引自原文，图上中文标签为编者所加（超声结构缩写保留原样）；疗程变化图由编者根据原文表 1 重画；整理卡为编者根据原文撰写。"
))
TITLE = "「髋关节」关节镜术后屁股还痛？别忘了闭孔神经：超声引导水分离＋神经滑动 2 例"
PTITLE = "闭孔神经靶向治疗推文"
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
