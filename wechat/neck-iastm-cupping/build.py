#!/usr/bin/env python3
"""Jahan 2025 器械辅助软组织松动 vs 干拔罐治疗颈痛推文：生成 article_body.html 与 preview.html。

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
    "Jahan A. Effectiveness of Instrument-assisted Soft-tissue Mobilization Versus Dry Cupping on Pain and Cervical Range of Motion in Treatment of Neck Pain. Indian J Community Med. 2025;50(3):506-511.",
    "作者来自印度奥兰加巴德 Dhaneshwari 物理治疗学院",
    "短篇报告，两组比较研究（抽签分组）；DOI：10.4103/ijcm.ijcm_834_23",
], square=True))

A.append(h2("先说结论：这篇的结论不能用"))
A.append(p(
    f"题目很吸引人：颈痛用{b('器械辅助软组织松动')}（用不锈钢刮板沿肌肉刮，常被叫作“筋膜刀”）好，"
    f"还是用{b('干拔罐')}好？作者结论是拔罐更好。"
))
A.append(p(
    f"但这篇的数据问题非常严重：{red('报告的颈椎前屈活动度是 150°～177°')}，而正常人用量角器测颈椎前屈只有 45°～50° 左右；"
    f"8 张结果图里实际只有 4 组数字反复出现，标成“侧屈”的图用的是前屈的数字。"
    f"拔罐组到底怎么做的（拔哪、多大负压、留多久、一周几次）也没写。"
))
A.append(p(
    f"所以这篇推文的重点不是“拔罐更好”，而是：{mk('两种手法原文写了什么、可以怎么借鉴，以及读这类文章时要核对哪些地方')}。"
))

A.append(h2("怎么做的"))
A.append(pic(2, "原文图 3　研究流程"))
A.append(ul([
    f"对象：私人物理治疗诊所，{b('30 名')} 20～45 岁颈痛患者（2 男 28 女），颈痛超过 2 周，视觉模拟评分 ≥ 5",
    "排除：颈椎骨折等外伤史、颈椎手术史、强直性脊柱炎和骨髓炎等（原文把强直性脊柱炎写成了“慢性感染”）、对治疗有禁忌",
    "抽签分组，每组 15 人；治疗 4 周",
    "结局：视觉模拟评分（疼痛）、量角器测颈椎前屈和侧屈；第 0 天和第 4 周末各测一次",
]))

A.append(h2("重点：两种手法原文怎么写的"))
A.append(pic(3, "两组的治疗方案"))
A.append(h3("A 组：器械辅助软组织松动（筋膜刀）"))
A.append(ul([
    "体位：舒适的含胸坐姿，颈部涂凡士林",
    f"先用刮板沿{b('上斜方肌')}探查“受限”的地方",
    f"刮板倾斜约 {b('45°')}，从肌肉起点到止点顺着肌纤维轻柔地刮，{mk('每次约 3 分钟，全程不引起不适或疼痛')}",
    f"{b('每周 2 次 × 4 周')}；治疗后如果有灼热感，可以冰敷",
]))
A.append(pic(5, "原文图 2　不锈钢刮板"))
A.append(h3("B 组：干拔罐"))
A.append(ul([
    "同样含胸坐姿，涂润滑剂",
    "用硅胶罐，靠抽气泵抽出空气，形成负压吸附在皮肤上",
    f"{red('没有写：放在哪里、负压多大、留罐还是走罐、每次多久、每周几次')}——别人没办法照着做",
]))
A.append(pic(4, "原文图 1　干拔罐"))
A.append(h3("两组都加：上斜方肌牵伸"))
A.append(ul([
    f"治疗后做上斜方肌被动牵伸：头向一侧侧屈，{b('保持 30 秒 × 3 次')}；需要时加一点低头，加大牵拉",
    f"另外布置居家自我牵伸，{b('每周 5 次')}",
    "原文只写了“向左侧屈”，没有说明是不是按疼痛侧调整",
]))

A.append(h2("结果"))
A.append(pic(6, "疼痛评分（原文表 1、图表 1～2）"))
A.append(ul([
    f"疼痛：器械松动组 7.25 → 5.65，拔罐组 7.25 → {b('3.65')}，作者据此认为拔罐更好",
    "但两组治疗前的均值和标准差完全一样（7.25 ± 1.07），疼痛的组间比较没有给 P 值",
    "活动度：见下图，数值本身就不可信",
]))
A.append(pic(7, "报告的颈椎活动度 vs 正常参考值"))

A.append(h2("这些结果能信几分"))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    f"{red('颈椎前屈 149°～177°')}：量角器测颈椎前屈正常约 45°～50°，侧屈约 45°，原文数值不可能成立；标准差 93.45、88.38 也大得离谱",
    "8 张图只有 4 组数字：图表 5、8 标为“侧屈”的 152.67 → 176.93 和前屈一模一样；图表 6 标为“B 组前屈”的 151.2 → 152.67 其实是 A 组的；图表 7 拿 B 组治疗前的 149.47 当“A 组治疗后”去比较",
    "表 1 中 A 组前屈治疗后写 152.27，图表写 152.67；表中“n”栏大多空着",
    "两组治疗前疼痛完全一样（7.25 ± 1.07），像是复制粘贴",
    "器械松动组疼痛平均降 1.6 分（标准差约 1），15 人做配对比较通常 P 远小于 0.031；结果 P 值可信度存疑",
    "统计部分只列了“N、M（中位数）、SD”的定义，没写用了什么检验；人口学资料说收集了，但没有报告",
    "拔罐组方案几乎空白；结论写“一次拔罐就能即时减轻疼痛”，可研究测的是 4 周后",
    "图 2 的刮板图片来自商业网站，图 1 也像是网络图片",
    "引言里说拔罐能治贫血、血友病，促进消化液分泌、增强免疫等，没有可靠依据",
]))
A.append(ul([
    "只有 30 人、单中心、单一作者，没有盲法，没有随访",
    "两组都做了牵伸和居家牵伸，看不出手法本身的作用",
    "28 名女性、2 名男性，性别极不平衡",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{b('这篇不能作为“拔罐比筋膜刀好”的证据')}",
    f"可以借鉴的是 A 组的器械松动细节：{mk('上斜方肌、刮板约 45°、起点到止点、约 3 分钟、无痛、每周 2 次')}，再配合 30 秒 × 3 次的上斜方肌牵伸",
    "无论用哪种手法，颈痛的长期管理还是要靠主动训练（深层颈屈肌、肩胛稳定、姿势与工作习惯）",
    "读类似文章时，先看活动度、疼痛等数值是否在合理范围，再看方案有没有写到别人能照做的程度",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　视觉模拟评分与颈椎活动度（照录）"))
A.append(table(["治疗", "时间", "组", "n", "均值", "标准差", "P"], [
    ["器械松动", "治疗前", "A", "—", "7.25", "1.07", "—"],
    ["器械松动", "治疗后", "A", "—", "5.65", "0.91", "0.031"],
    ["干拔罐", "治疗前", "B", "—", "7.25", "1.07", "—"],
    ["干拔罐", "治疗后", "B", "—", mk("3.65"), "0.93", "0.001"],
    ["A 组", "前后", "—", "—", red("151.20"), red("93.45"), "0.01"],
    ["A 组", "前后", "—", "—", red("152.27"), red("88.38"), "—"],
    ["B 组", "前后", "—", "—", red("149.47"), "40.69", "0.01"],
    ["B 组", "前后", "—", "—", red("176.93"), "11.49", "0.01"],
    ["A 组 vs B 组", "治疗后", "—", "15", "152.67", "88.38", "0.01"],
    ["A 组 vs B 组", "治疗后", "—", "15", "176.93", "11.49", "0.001"],
]))
A.append(small("表题原文为“A 组……视觉模拟评分前后数据分析”，后 6 行为活动度，原表未注明是前屈还是侧屈。红字：数值超出生理范围。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Jahan A. Effectiveness of instrument-assisted soft-tissue mobilization versus dry cupping on pain and cervical range of motion in treatment of neck pain. Indian J Community Med. 2025;50:506-11. doi:10.4103/ijcm.ijcm_834_23</em><br>"
    "原文以 CC BY-NC-SA 4.0 协议开放获取（仅限非商业使用，改编作品须以相同协议发布），本文按同一协议发布。本文为学术交流用的中文解读；图 1、图 2 照片引自原文（原文注明图 2 来自商业网站），已模糊品牌字样；流程、方案卡与图表为编者中文重绘，表格为编者翻译。"
))

TITLE = "「颈痛」筋膜刀 vs 拔罐，谁更好？一篇结论不能用的研究，和它值得借鉴的细节"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>颈痛筋膜刀拔罐推文</title>
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
