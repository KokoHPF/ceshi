#!/usr/bin/env python3
"""20 岁女性疼痛性扁平足足部康复训练 1 例（Kolhe 等 2024）推文。

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
    "Kolhe PD, Sharath HV, Rathi SG, Patil DS. Effect of Foot Rehabilitation Exercises for Painful Flat Foot in a 20-Year-Old Female: A Case Study Analysis. Cureus. 2024;16(4):e59377. doi:10.7759/cureus.59377",
    "作者单位：印度 Datta Meghe 高等教育研究院 Ravi Nair 物理治疗学院",
    f"文章类型：{b('病例报告')}（1 例）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"20 岁女性，自幼双侧扁平足，剧烈活动时疼痛（VAS 7/10），走路困难",
    f"做了 {b('2 个月、每周 5 天')}的足部训练：抓毛巾、跟腱拉伸、脚趾外展、弹力带抗阻、足弓滚球、每天赤脚活动 45 分钟",
    f"训练后疼痛 7 → 2 分，足功能、足踝能力评分明显改善，肌力从 1 级升到 {b('4+ 级')}",
    f"但{red('只有 1 例、没有对照')}，部分结果变化幅度偏大，要谨慎看待",
]))

A.append(h2("一、扁平足和这个病例"))
A.append(img(2))
A.append(cap("扁平足简介（编者根据原文整理）"))
A.append(img(3))
A.append(cap("病例情况（据原文整理）"))
A.append(img(4))
A.append(cap("原文图 1：患者已在使用的辅具"))
A.append(img(5))
A.append(cap("原文图 2：Feiss 线测试"))
A.append(tcap("原文表 1：徒手肌力评定（0～5 级）"))
A.append(table(["肌群", "训练前", "训练后"], [
    ["足内在肌", "1", "4+"],
    ["拇展肌（脚趾外展）", "1", "4+"],
    ["踝背屈肌", "1", "4+"],
]))

A.append(h2("二、训练方案"))
A.append(img(6))
A.append(cap("6 个训练动作（据原文表 2 整理）"))
A.append(img(7))
A.append(cap("原文图 3：跟腱拉伸和弹力带抗阻"))
A.append(img(8))
A.append(cap("原文图 4：足弓滚球练习"))
A.append(p(f"作者的思路是：抓毛巾和脚趾外展练{b('足内在肌')}，跟腱拉伸改善小腿和跟腱柔韧性，胫骨后肌强化支撑{b('内侧纵弓')}、防止过度旋前，赤脚活动则让足部在没有支撑的情况下获得本体感觉反馈和肌肉激活。"))

A.append(h2("三、结果"))
A.append(img(9))
A.append(cap("评估结果（据原文表 3 重画）"))
A.append(tcap("原文表 3：训练前后评估"))
A.append(table(["量表", "训练前", "训练后"], [
    ["足功能指数 FFI：疼痛和僵硬 / 困难程度 / 活动受限（1～6）", "5 / 4 / 5", "2 / 1 / 1"],
    ["疼痛 VAS（0～10）", "7", "2"],
    ["FAAM：日常生活 / 运动", "50% / 50%", "97% / 100%"],
    ["足姿指数 FPI-6", "+6（旋前）", "-2（轻度旋后）"],
]))

A.append(h2("这篇文章能信几分"))
A.append(img(10))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例')}、没有对照，没有随访；训练期间仍在使用足弓支撑带和鞋垫，无法区分训练和辅具各自的作用",
    "原文没写评估由谁做、是否盲法；2 个月内肌力从 1 级到 4+ 级、足姿从旋前变成旋后，变化幅度偏大",
    "患者一侧足跟发育不良，原文没有交代如何处理",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "正文说足弓支撑带是图 1A、鞋内垫板是图 1B，图注和图片正好相反",
    "正文说下肢肌力正常、只是背屈和内翻弱于跖屈和外翻，表 1 却记录三组肌群都只有 1 级",
    "“胫骨后肌强化”的动作描述是把脚向上抬（背屈），与胫骨后肌内翻、跖屈的作用不符",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"有症状的扁平足可以先试{b('足部主动训练')}：抓毛巾、脚趾外展练内在肌，配合跟腱拉伸",
    "练胫骨后肌要做抗阻内翻（及跖屈），而不是单纯把脚往上抬",
    "赤脚活动可作为日常补充，但有明显疼痛或结构异常时，先评估再决定是否脱离辅具",
    "用 FPI-6、FFI、FAAM 等量表记录前后变化，便于判断训练是否有效",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Kolhe PD, Sharath HV, Rathi SG, Patil DS. Effect of Foot Rehabilitation Exercises for Painful Flat Foot in a 20-Year-Old Female: A Case Study Analysis. Cureus. 2024;16(4):e59377. doi:10.7759/cureus.59377</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～4 引自原文；评估结果图由编者根据原文表 3 重画；整理卡为编者根据原文撰写。"
))
TITLE = "「足踝」扁平足走路就痛？6 个居家足部训练练 2 个月，疼痛 7 分降到 2 分"
PTITLE = "疼痛性扁平足训练推文"
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
