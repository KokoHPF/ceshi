#!/usr/bin/env python3
"""胫骨 Pilon 骨折术后康复 1 例（张言等 2025）推文。

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
A.append(cap("原文信息（编者重排）"))
A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "张言, 陈和木, 李键. 胫骨 Pilon 骨折术后康复治疗 1 例[J]. 临床医学进展, 2025, 15(8): 1230-1239. doi:10.12677/acm.2025.1582357",
    "作者单位：安徽医科大学第一临床医学院、安徽医科大学第一附属医院康复医学科",
    f"文章类型：{b('病例报告')}（1 例，随访至术后约 2 个月）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"47 岁男性左侧 Pilon 骨折，同时合并{b('腓总神经（及胫神经）损伤、胫后肌腱部分断裂和踝周多条韧带损伤')}",
    f"术后 48 小时床旁康复介入，按{b('第 1 周、第 2 周、第 3～4 周')}分阶段推进，消肿、神经、肌力、活动度、日常生活能力几条线同时做",
    f"负重推迟到{b('术后 8 周')}，从体重的 10%～20% 开始，{b('12 周内不超过 50%')}",
    f"术后约 2 个月：疼痛 4 → 1 分，Barthel 60 → 90 分，基本自理；但{red('踝关节仍僵硬、肌力仅 1 级')}，AOFAS 只有 47 分",
]))

A.append(h2("一、病例：不只是骨折"))
A.append(img(2))
A.append(cap("Pilon 骨折简介（编者根据原文整理）"))
A.append(img(3))
A.append(cap("病程经过（据原文整理）"))
A.append(img(4))
A.append(cap("原文图 1：CT 三维重建"))
A.append(img(5))
A.append(cap("原文图 2：MRI"))
A.append(img(6))
A.append(cap("原文图 3：两次手术后的 X 线"))
A.append(img(7))
A.append(cap("肌电图要点（据原文表 1 整理）"))
A.append(tcap("原文表 1：神经传导关键数据（左／右）"))
A.append(table(["项目", "左侧", "右侧"], [
    ["腓总神经运动波幅（踝，mV）", "4.80", "9.69"],
    ["腓总神经运动波幅（腓骨小头上，mV）", "9.14", "13.20"],
    ["腓浅神经感觉波幅（μV）", "18.7", "32.3"],
    ["针极肌电图（胫前肌、胫后肌、拇展肌、腓骨长肌）", "纤颤、正锐波，重收缩无运动单位电位", "—"],
]))
A.append(p(f"转康复科时，左踝背伸、拇趾背伸、跖屈肌力分别只有 {b('0、1、0 级')}，踝关节停在跖屈 30°，被动背伸 0°，内外翻 0°。肌电图说明这不只是疼痛或制动造成的“不敢动”，而是{b('神经损伤导致的肌肉失神经')}。"))

A.append(h2("二、康复怎么做"))
A.append(img(8))
A.append(cap("康复目标和注意事项（原文）"))
A.append(img(9))
A.append(cap("术后第 1 周（原文）"))
A.append(img(10))
A.append(cap("术后第 2 周（原文）"))
A.append(img(11))
A.append(cap("术后第 3～4 周（原文）"))
A.append(p(f"作者特别提到：由于骨折合并神经、肌腱和韧带损伤，{b('住院期间没有做负重训练')}；关节松动时也要留意胫后肌腱和韧带，避免二次损伤导致日后踝关节不稳。"))
A.append(img(12))
A.append(cap("出院后的负重进阶（原文）"))

A.append(h2("三、结果"))
A.append(img(13))
A.append(cap("评分变化（据原文数据重画）"))
A.append(p(f"术后约 2 个月，患者基础日常生活基本自理，但平地行走和上下楼仍需部分协助。作者认为 AOFAS 不理想主要是{b('踝关节僵硬和步行障碍')}，与 Pilon 骨折本身难以恢复正常活动度、以及合并多重损伤有关，活动度和步行能力的改善{b('可能需要 1 年甚至更久')}，因此也对患者做了预期管理。"))

A.append(h2("这篇文章能信几分"))
A.append(img(14))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例')}、随访只有约 2 个月，没有长期结果",
    "同时使用了运动治疗、电刺激、针刺、蜡疗、中药熏蒸、神经生长因子等十几种方法，无法判断各自的作用",
    "优点：检查资料齐全（CT、MRI、超声、肌电图），每周的训练参数写得很具体，便于参考",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "摘要中肌力写成“0-10 级”，正文为 0-1-0 级",
    "病例中写“不伴有血管损伤”，讨论又说本例“合并神经、血管、肌腱等损伤”",
    "正文说“经过 3 周的康复治疗”，实际 12 月 4 日转入、12 月 17 日出院，约 2 周",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"Pilon 骨折术后肌力异常低下时，{b('别只当成疼痛或制动')}，要想到神经损伤，必要时查肌电图",
    "早期以消肿、踝泵、被动活动、电刺激为主，支具保持踝关节功能位，防止跖屈挛缩",
    f"合并肌腱、韧带损伤时，关节松动和活动度训练要{b('温和渐进')}，负重可推迟到 8 周、12 周内不超过 50% 体重",
    "提前和患者沟通预期：日常自理可能较快，踝关节活动度和步行能力的恢复可能需要 1 年以上",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>张言, 陈和木, 李键. 胫骨 Pilon 骨折术后康复治疗 1 例[J]. 临床医学进展, 2025, 15(8): 1230-1239. doi:10.12677/acm.2025.1582357</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～3 引自原文，图中中文标注为原文自带；评分图由编者根据原文数据重画；整理卡为编者根据原文撰写。"
))
TITLE = "「踝关节」Pilon 骨折合并神经、肌腱、韧带损伤：术后分周康复怎么做？（附负重进阶）"
PTITLE = "Pilon 骨折术后康复推文"
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
