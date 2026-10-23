#!/usr/bin/env python3
"""器械辅助软组织松动对肩后侧活动度的即时影响（Laudner 2014）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
"""
import pathlib

HERE = pathlib.Path(__file__).parent


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
    "Laudner K, Compton BD, McLoda TA, Walters CM. Acute effects of instrument assisted soft tissue mobilization for improving posterior shoulder range of motion in collegiate baseball players. Int J Sports Phys Ther. 2014;9(1):1-7. PMID: 24567849",
    "中文题目：器械辅助软组织松动改善大学棒球运动员肩后侧活动度的即时效果",
    "作者来自美国伊利诺伊州立大学等机构，通讯作者 Kevin G. Laudner",
    "研究类型：随机对照试验（单次干预、即时前后测），作者自评证据等级 2b",
], square=True))

A.append(h2("研究背景"))
A.append(ul([
    "投球减速期，肩后侧结构反复承受很大的旋转和牵拉力；长期下来，棒球运动员投掷臂常出现外旋增大、内旋和水平内收减少，也就是常说的“肩后侧紧张”",
    "肩后侧紧张和多种投掷肩损伤有关；以往试过睡姿牵伸、水平内收牵伸、肌肉能量技术等，效果不一",
    f"器械辅助软组织松动（IASTM，如 Graston 技术）用不锈钢器械在皮肤上刮动，临床上常用于软组织受限，但{b('当时还没有研究看它对盂肱关节活动度的作用')}",
    "作者假设：一次器械松动后，被动水平内收和内旋会比对照组即时增加",
]))

A.append(h2("方法"))
A.append(pic(2, "编者根据原文整理"))
A.append(ul([
    f"{b('受试者')}：35 名 NCAA 一级联赛大学棒球运动员，无症状、不要求有活动度受限，随机分为器械松动组 17 人、对照组 18 人",
    f"{b('测量')}：仰卧、肩外展 90°、屈肘 90°，一人固定肩胛骨并被动活动到终末，另一人用数字倾角仪读数；事先检验的同测者信度：水平内收 ICC 0.93、SEM 1.6°，内旋 ICC 0.98、SEM 2.0°",
    f"{b('干预')}：俯卧同样体位，Graston GT-4 器械以约 45° 角在肩后腋缘（三角肌后束、背阔肌、大圆肌、小圆肌、冈下肌）先顺纤维、再横纤维各刮约 20 秒，{b('共约 40 秒')}；对照组俯卧同样时间、不做处理",
    f"{b('盲法')}：施术时测量者离开房间，受试者穿回上衣遮住皮肤发红；前后测相隔约 90 秒",
]))
A.append(pic(3, "原文图 1（照片内无文字，图注由编者翻译）"))
A.append(pic(4, "原文图 2（照片内无文字，图注由编者翻译）"))
A.append(pic(5, "原文图 3、图 4（照片内无文字，图注由编者翻译）"))
A.append(pic(6, "原文表 1（编者翻译重排）"))

A.append(h2("结果"))
A.append(ul([
    f"{b('水平内收')}：器械松动组从 -10.9° 增加到 0.2°，{mk('平均 +11.1°')}；对照组 -0.12°（组×时间交互 P < 0.001，F = 77.4，偏 η² = 0.7）",
    f"{b('内旋')}：器械松动组从 42.4° 增加到 47.2°，{mk('平均 +4.8°')}；对照组 -0.14°（P < 0.001，F = 12.7，偏 η² = 0.3）",
    "水平内收的方差不齐，作者把显著性门槛收紧到 P < 0.025，两项结果仍然显著",
]))
A.append(pic(7, "编者根据原文表 2、表 3 绘制"))
A.append(pic(8, "原文表 2、表 3（编者翻译合并）"))

A.append(h2("作者怎么解读"))
A.append(ul([
    "这是第一项显示短时器械松动能即时增加棒球运动员盂肱关节水平内收和内旋的研究",
    "改善幅度超过测量的标准误（SEM），作者认为具有临床意义；与睡姿牵伸（+2.3°、+3.1°）和肌肉能量技术（+6.8°、+4.2°）的既往结果“相似”",
    "可能机制：器械造成局部微损伤和炎症反应，重新启动修复过程（这是机制假说，本研究没有测）",
    "作者承认的局限：用了固定方案而非个体化治疗、只用一种器械和一个体位、只看即时效果；建议研究多次治疗、有活动度缺失的人群和长期效果",
]))
A.append(pic(10, "编者根据原文讨论整理"))

A.append(h2("这些结论能信几分"))
A.append(pic(9, "编者计算"))
A.append(ul([
    f"{b('水平内收的改善比较可信')}：11.1° 远高于按原文 SEM 算出的最小可检测变化（MDC95 约 4.4°），对照组几乎不变",
    f"{b('内旋的改善要打折扣')}：4.8° 低于 MDC95（约 5.5°），单个人测出这样的变化，可能就在测量误差之内；作者用“超过 SEM”判断临床意义，门槛偏低",
    f"{b('没有安慰对照')}：对照组只是躺着，受试者知道自己被处理过，期待效应和皮肤刺激带来的放松无法和器械本身的作用分开",
    f"{b('只看了 90 秒后')}：维持多久、多次治疗是否累积、对肩痛或投球表现有没有影响，全都不知道",
    f"{b('样本小且无症状')}：35 名健康运动员，结论不能直接外推到有肩后侧紧张或肩痛的病人",
    f"{b('报告不完整')}：没写随机方法、刮的次数和力度、基线比较；器械松动组身高、体重的离散度明显更大",
]))
A.append(pic(11, "编者评价"))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“小到中等”效应量')}：作者称偏 η² 0.7 和 0.3 是“small to moderate”，按常用标准（0.14 即为大效应）两者都属于大效应",
    f"{b('显著性门槛前后不一')}：方法和摘要写 α = 0.05，结果部分改成 P < 0.025",
    f"{b('对照组变化的小数位')}：摘要和表 2、表 3 写 -0.12°、-0.14°，结果正文写 -0.1°；按表中均值算是 -0.2° 和 -0.1°",
    f"{b("“盲法随机设计”说法偏宽")}：只有测量者在施术时回避，受试者和施术者都不盲，也没写随机方法",
    f"{b('信度检验和正式测量不是一回事')}：信度是“单一检查者”间隔 48 小时复测得到的，正式测量却由两人配合（一人摆位、一人读数）、间隔 90 秒",
    f"{b('与既往研究“相似”')}：本研究水平内收 +11.1°，是睡姿牵伸（+2.3°）的近 5 倍，用“相似”形容并不准确",
    f"{b('引用错位')}：“Aspegren 等 23 治疗排球运动员肋软骨炎”应为参考文献 16（文献 23 是一篇脊椎按摩治疗颈腰痛的回顾性研究）；“基于 Cyriax 深部摩擦按摩理论 21”引的是 Hammer 和 Pfefer 的个案，而不是 Cyriax 本人",
    f"{b('用词不统一')}：题目和正文是 instrument assisted soft tissue mobilization，表格缩写说明写成 Instrumented soft tissue mobilization；“standarized”为笔误",
]))

A.append(h2("落到临床"))
A.append(pic(12, "编者建议"))
A.append(ul([
    f"{mk('定位')}：器械松动可以作为投掷运动员肩后侧紧张的{b('即时“松解”选项')}，尤其是训练或投球前想快速改善水平内收时",
    f"{b('先量再做、做完再量')}：用同一方法测水平内收和内旋；内旋变化在 5° 以内时，别急着认定有效",
    f"{b('趁热巩固')}：刮完后马上接水平内收牵伸、睡姿牵伸和后侧肩袖、肩胛稳定训练，单靠器械不太可能带来持久改变（编者观点）",
    f"{b('注意皮肤')}：使用润滑剂，刮后发红常见；有皮肤破损、凝血问题等情况时慎用（编者观点）",
    f"{b('别过度承诺')}：目前这篇研究不能说明器械松动能预防肩伤或提高球速",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　受试者特征（均值 ± 标准差）"))
A.append(table(["组别", "年龄（岁）", "身高（cm）", "体重（kg）"], [
    ["器械松动组（n = 17）", "20.1 ± 1.2", "189.3 ± 11.2", "94.1 ± 22.2"],
    ["对照组（n = 18）", "20.3 ± 1.1", "185.7 ± 5.3", "85.4 ± 21.2"],
]))
A.append(tcap("原文表 2　盂肱关节水平内收活动度（度，均值 ± 标准差）"))
A.append(table(["组别", "前测", "后测", "变化", "P 值"], [
    ["器械松动组", "-10.9 ± 5.8", "0.2 ± 6.3", "+11.1†", "< 0.001"],
    ["对照组", "-10.4 ± 4.2", "-10.6 ± 4.4", "-0.12", ""],
]))
A.append(tcap("原文表 3　盂肱关节内旋活动度（度，均值 ± 标准差）"))
A.append(table(["组别", "前测", "后测", "变化", "P 值"], [
    ["器械松动组", "42.4 ± 10.8", "47.2 ± 9.2", "+4.8†", "< 0.001"],
    ["对照组", "41.6 ± 8.0", "41.5 ± 9.1", "-0.14", ""],
]))
A.append(small("† 与前测相比活动度增加（P < 0.025）。原文表格在 PDF 中为图片，编者按原值重排"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Laudner K, Compton BD, McLoda TA, Walters CM. Acute effects of instrument assisted soft tissue mobilization for improving posterior shoulder range of motion in collegiate baseball players. Int J Sports Phys Ther. 2014;9(1):1-7.（PubMed：24567849；PubMed Central：PMC3924602）</em><br>"
    "本文为中文解读，仅作学术交流：原文图 1～图 4 引自原文（照片内无文字，图注由编者翻译）；表 1～表 3 由编者翻译重排，研究流程、前后测图、测量误差图、对照表和评价卡为编者根据原文整理。原文版权归 Sports Physical Therapy Section 所有。"
))

TITLE = "「器械松动」刮 40 秒，投手肩后侧能松多少？"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>器械松动与肩后侧活动度推文</title>
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
