#!/usr/bin/env python3
"""膝关节腔注射改良前外侧入路 vs 髌上外侧入路（Chernchujit 等 2019）推文。

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
    "Chernchujit B, Tharakulphan S, Apivatgaroon A, Prasetia R. Accuracy comparisons of intra-articular knee injection between the new modified anterolateral approach and superolateral approach in patients with symptomatic knee osteoarthritis without effusion. Asia-Pacific Journal of Sports Medicine, Arthroscopy, Rehabilitation and Technology. 2019;17:1-4. doi:10.1016/j.asmart.2019.02.001",
    "作者单位：泰国国立法政大学医学院骨科、孔敬医院骨科、印尼巴查查兰大学骨科",
    f"文章类型：{b('前瞻性对照研究')}（132 膝，两种入路各 66 膝）",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"膝骨关节炎很常见，关节腔注射激素或其他药物是常用的保守治疗。药要{b('真的打进关节腔')}才能发挥作用；"
    f"打到关节外、前方脂肪垫或滑膜外组织，不仅效果打折，还可能带来{red('皮肤色素脱失、皮下脂肪和肌肉萎缩')}等局部损害。"
))
A.append(p(
    f"难点在于{b('没有积液的“干膝”')}：抽不出液体，就没法用回抽来确认针尖位置。原文引用的系统综述显示，伸膝位{b('髌上外侧入路')}准确率最高（约 91%），"
    f"外侧髌中、前外侧、前内侧入路分别约 85%、67%、72%。作者在标准前外侧入路的基础上提出一种{mk('改良前外侧入路')}，想看它能不能比髌上外侧入路更准。"
))
A.append(p("作者没有比较内侧入路：骨关节炎患者的内侧和髌股关节间隙往往很窄，从这里进针容易伤到软骨、引起疼痛。"))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：2014 年 5 月～2015 年 5 月，临床和影像确诊、口服药物效果不好、{b('没有积液')}的症状性膝骨关节炎（各 Kellgren-Lawrence 分级都纳入）；排除感染、凝血障碍、对注射药物过敏",
    f"{b('分组')}：共 132 膝，改良前外侧入路（MAL）和标准髌上外侧入路（SL）各 66 膝",
    f"{b('操作者')}：同一位从业 15 年以上的骨科医生",
    f"{b('确认是否打进关节')}：微量空气关节造影——注射后立即拍正、侧位片，看空气在关节内还是关节外（图 3、图 4）",
    f"{b('疼痛')}：注射完由独立评估者记录视觉模拟评分（VAS）",
]))

A.append(h2("重点：两种入路怎么打"))
A.append(img(2))
A.append(cap("编者示意图：改良前外侧入路的进针点和方向（根据原文描述绘制）"))
A.append(h3("改良前外侧入路（MAL）"))
A.append(ul([
    f"{b('体位')}：仰卧或坐位，{b('屈膝 90°')}",
    f"{b('进针点')}：{mk('髌骨下缘水平线与 Gerdy 结节垂线的交点')}",
    f"{b('方向')}：与胫骨后倾平行（原文约 10°），针尖朝{b('外侧胫骨平台')}，而不是传统前外侧入路的髁间窝——避开脂肪垫、黏膜韧带和交叉韧带，也不伤软骨和半月板",
    f"{b('深度')}：进针到轻触股骨外侧髁软骨，再{b('退 1 mm')}。作者认为这个“止点”比朝髁间窝进针更好把握深度",
]))
A.append(pic(3, "原文图 1：改良前外侧入路（图中中文标注为编者所加）"))
A.append(h3("标准髌上外侧入路（SL）"))
A.append(ul([
    f"{b('体位')}：仰卧，伸膝",
    f"{b('进针点')}：髌骨上缘水平线与髌骨外侧缘纵线的交点",
    f"{b('方向')}：与股骨前方皮质平行，进入髌上囊",
]))
A.append(pic(4, "原文图 2：标准髌上外侧入路（图中中文标注为编者所加）"))
A.append(h3("两组共用的“回流法”"))
A.append(p(
    f"两组都用 {b('25G 针')}，一根针配两支注射器：先注入 {b('10 mL 空气')}，像硬膜外注射那样感受“无阻力”，观察空气回流（backflow）确认针尖在关节内；"
    f"没有回流就再注 10 mL 空气。看到回流后换注射器注药，注完能听到明显的“咕叽”声。"
))
A.append(img(5))
A.append(cap("两种入路操作要点（编者根据原文整理）"))

A.append(h2("结果"))
A.append(pic(6, "原文图 3：注射不准——空气在关节外软组织（箭头）"))
A.append(pic(7, "原文图 4：注射准确——空气在髌上囊内（白箭头）"))
A.append(table(["结局", "改良前外侧（66 膝）", "标准髌上外侧（66 膝）"], [
    ["注射准确率", f"{b('89%')}*", "58%*"],
    ["注射疼痛 VAS（均数 ± 标准差）", "2.61 ± 2.21", "2.65 ± 2.76"],
    ["并发症", "无", "无"],
]))
A.append(tcap("原文表 1：准确率、疼痛和并发症（中文翻译）。*两组差异有统计学意义，P < 0.05"))
A.append(ul([
    f"改良前外侧入路准确率 {b('89%')}，明显高于髌上外侧入路的 {b('58%')}",
    f"注射疼痛两组几乎一样（VAS 2.61 vs 2.65，P＝0.917）",
    "两组都没有出现不良事件",
]))
A.append(pic(8, "两组结果对比（编者根据原文表 1 重画）"))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('分组方式说不清')}：摘要写“随机分成两组”，方法部分写的是连续纳入，没有交代怎么随机，局限性里又写“没有随机双盲”",
    f"{b('没有基线资料')}：两组的年龄、性别、体重、K-L 分级都没报告，无法判断两组是否可比；也没说多少人是双膝都打",
    f"{b('单一术者、未设盲')}：只有一位资深医生操作，他提出了改良入路，可能更熟练；读片的人是否知道分组也没交代",
    f"{b('髌上外侧组 58% 明显偏低')}：作者自己引用的综述中髌上外侧入路约 91%，这个差距没有解释，结果能否推广要打问号",
    f"{b('“准确”的判定和重复操作')}：空气位置不确定时“重复操作”，怎么计入准确率没有说明；两组都用了回流法，可能也影响结果",
    f"{b('统计方法不对')}：两组是独立的，准确率是分类变量，应该用卡方检验或 Fisher 精确检验，原文却用了配对 t 检验",
    f"{b('只看了“打没打进去”')}：没有随访止痛效果，也没有和超声引导比较",
    "优点：用影像确认是否打进关节，标准客观；改良入路屈膝 90° 就能做，作者认为对肥胖、伸膝或屈膝受限、关节间隙很窄的患者更友好",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('膝数前后不一')}：摘要和方法写 132 膝，结果写“One hundred and twenty-two knees（122 膝）”，但两组各 66 膝合计是 132",
    f"{b('样本量不够')}：样本量计算说每种技术至少需要 {b('130 膝')}，实际每组只有 66 膝；局限性里也承认例数偏少",
    f"{b('“配对设计”')}：样本量按配对设计计算、用配对 t 检验，但两组是不同的膝",
    f"{b('“随机”前后矛盾')}：摘要写随机分组，局限性写“没有随机双盲”",
    f"{b('表 1 与正文')}：表中并发症写“NA”（不适用），正文写两组都没有不良事件；髌上外侧组的例数没标；P 值写成 0.000",
    f"{b('角度符号丢失')}：“屈膝 90”“与胫骨后倾 10 平行”应为 90°、10°",
    f"{b('小错')}：“soft sport”应为 soft spot（软点）；“medial agents”应为 medical agents；25G 针引用“2007 WN Robert”不在参考文献里；参考文献 17 的 doi 写成“0.5435”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{b('干膝注射不容易打准')}：这篇里同一位资深医生用髌上外侧入路也只有 58% 进了关节，盲打的准确率不能想当然",
    f"{b('改良前外侧入路值得了解')}：屈膝 90° 坐位就能做，进针点用髌骨下缘和 Gerdy 结节两个好摸的标志，朝外侧胫骨平台、触到股骨外侧髁退 1 mm，有明确的深度“止点”",
    f"{b('先确认再注药')}：回流法、注药时无阻力、注后的“咕叽”声都是作者用来确认针尖在关节内的线索；条件允许时超声引导更可靠",
    "关节腔注射须由有资质的医生操作；对康复治疗师来说，了解进针点、体位和可能的并发症，有助于和医生沟通、做好注射前后的宣教和康复衔接",
    "这篇证据等级不高（单中心、单术者、分组方法不清、统计方法有误），结论需要更大规模、规范设计的研究来验证",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Chernchujit B, Tharakulphan S, Apivatgaroon A, Prasetia R. Accuracy comparisons of intra-articular knee injection between the new modified anterolateral approach and superolateral approach in patients with symptomatic knee osteoarthritis without effusion. Asia Pac J Sports Med Arthrosc Rehabil Technol. 2019;17:1-4. doi:10.1016/j.asmart.2019.02.001</em><br>"
    "原文以 CC BY-NC-ND 4.0 协议开放获取，版权归原作者所有。本文为非商业的学术交流中文解读：原文图 1～4 引自原文，图中中文标注为编者所加；示意图、流程卡和结果图为编者根据原文整理，表格为中文翻译。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「膝」没有积液的膝关节怎么打准关节腔？屈膝 90° 改良前外侧入路准确率 89%，髌上外侧仅 58%"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>膝关节腔注射入路推文</title>
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
