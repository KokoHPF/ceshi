#!/usr/bin/env python3
"""手部多发腕掌关节骨折脱位术后康复 1 例（Bell 等 2010）推文。

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
    "Bell T, Chinchalkar SJ, Faber K. Postoperative management of carpometacarpal joint fracture dislocation of the hand: A case report. Can J Plast Surg. 2010;18(3):e37-e40.",
    "作者单位：加拿大安大略省伦敦市 St Joseph’s 医疗中心手与上肢中心",
    f"文章类型：{b('病例报告')}（1 例）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"第 2～5 指{b('腕掌关节同时骨折脱位')}很少见，多由车祸等高能量外伤引起，闭合复位常失败，首选切开复位克氏针固定",
    f"作者设计了一种{b('环形腕掌稳定支具')}：从掌骨头包到桡腕关节，只保护腕掌关节，腕和手指可以照常活动",
    f"本例第 8 周开始手治疗，{b('第 10 周')}掌指、指间关节活动度恢复；第 12 周停支具开始强化，约半年时握力恢复到健侧的 {b('85%')}",
    f"但{red('只有 1 例')}，而且石膏固定了 6 周，并不算真正的“早期”活动",
]))

A.append(h2("一、为什么关注这种损伤"))
A.append(img(2))
A.append(cap("背景（编者根据原文整理）"))
A.append(p(f"腕掌关节由掌骨底和远排腕骨构成，周围韧带非常坚强，骨性咬合也很紧密，{b('通常很难脱位')}。一旦多个腕掌关节同时骨折脱位，往往意味着很大的暴力（轴向负荷加剪切力）。"))
A.append(p(f"治疗上的矛盾在于：受伤的腕掌关节需要{b('稳定')}才能愈合，而长期把整个手腕和手指固定起来，又会带来{b('关节僵硬、肌腱粘连、手内在肌无力')}，严重时还要再手术松解。"))

A.append(h2("二、病例：28 岁男性，车祸"))
A.append(img(3))
A.append(cap("原文图 1：受伤时 X 线"))
A.append(img(4))
A.append(cap("原文图 2：闭合复位后"))
A.append(img(5))
A.append(cap("原文图 3：切开复位内固定后"))
A.append(img(6))
A.append(cap("治疗时间线（据原文表 1 及正文整理）"))
A.append(p(f"作者坦言，他们{b('没有参与患者伤后早期的处理')}，所以患者在石膏里固定的时间比他们希望的要长；到第 6 周拆石膏时，腕关节只剩伸 30°、屈 40°，掌指关节只剩伸 15°、屈 25°。"))

A.append(h2("三、康复：腕掌支具＋保护下活动"))
A.append(img(7))
A.append(cap("原文图 4：术后第 6 周，克氏针尚未拔除"))
A.append(img(8))
A.append(cap("原文图 5：环形腕掌稳定支具"))
A.append(img(9))
A.append(cap("康复方案（据原文整理）"))
A.append(p(f"这个支具的思路是{mk('只保护受伤的关节，放开没受伤的关节')}：早期减少腕掌关节受力，让腕、掌指、指间关节尽早活动；后期做握力训练时，再给腕掌关节提供环形支撑，减少平移和旋转应力。"))
A.append(img(10))
A.append(cap("原文图 6：伤后 10 周的活动度"))
A.append(img(11))
A.append(cap("握力恢复（据原文表 1 重画）"))
A.append(tcap("原文表 1：活动度变化（伸／屈，单位：度）"))
A.append(table(["时间", "腕关节", "掌指关节", "指间关节"], [
    ["第 6 周（拆石膏）", "30 / 40", "15 / 25", "正常"],
    ["第 8 周（拔针，开始手治疗）", "45 / 45", "10 / 65", "—"],
    ["第 10 周", "—", "正常", "正常"],
    ["约第 26 周（11 月 14 日）", "正常", "正常", "正常"],
]))

A.append(h2("这篇文章能信几分"))
A.append(img(12))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例')}、没有对照，没有疼痛、功能评分和长期随访，说不清支具本身起了多大作用",
    "支具是作者团队自己设计的，原文没有给出制作材料和具体做法，只有一张照片",
    "患者是 28 岁的年轻男性，结果不一定能推广到年长或合并其他损伤的患者",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "正文说第 10 周活动度“全部恢复”，表 1 中腕关节活动度要到约第 26 周才记录为正常",
    "正文说大多角骨骨折，图 3 图注写的是小多角骨用螺钉固定；表 1 还有“6 月 31 日”这个不存在的日期",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"腕掌关节骨折脱位术后，{b('不必把腕和手指一起长期固定')}；可考虑只包住腕掌关节的支具，让腕、掌指、指间关节尽早活动",
    "练习先单关节、再复合动作；配合肌腱滑动练习预防粘连，屈指手套可辅助被动牵伸",
    "握力强化要等到腕掌关节稳定（本例第 12 周），强化期仍可戴支具提供支撑",
    "具体何时拔针、何时开始活动，要和手术医生根据固定情况商量",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Bell T, Chinchalkar SJ, Faber K. Postoperative management of carpometacarpal joint fracture dislocation of the hand: A case report. Can J Plast Surg. 2010;18(3):e37-e40.</em><br>"
    "原文版权归 Pulsus Group Inc. 所有（All rights reserved），非开放许可。本文为非商业的学术交流中文解读：原文图 1～6 引自原文，图像未作修改，中文说明见图注；握力图由编者根据原文表 1 重画，整理卡为编者根据原文撰写。仅供学习交流，如有侵权请联系删除。"
))
TITLE = "「手部」腕掌关节骨折脱位术后：只包腕掌关节的支具，让手腕和手指早点动起来"
PTITLE = "腕掌关节骨折脱位术后康复推文"
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
