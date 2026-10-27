#!/usr/bin/env python3
"""髋关节后脱位“不牵引”复位法（Mugalur 2026）推文。

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
    "Mugalur A. “No Traction” Technique: A Novel, Simple, Easy, and Ergonomic Maneuver to Reduce Posterior Dislocation of the Hip Joint – A Case Report. J Orthop Case Rep. 2026;16(5):156-160. doi:10.13107/jocr.2026.v16.i05.7240",
    "作者单位：印度卡纳塔克邦迈索尔 Bhanavi 医院骨科",
    f"文章类型：{b('病例报告')}（2 例，介绍一种新的复位手法）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"髋关节后脱位的各种闭合复位法，核心都是{b('牵引')}；作者提出一种{b('完全不牵引')}的手法",
    f"口诀：{mk('屈—内收—内旋—外展—外旋—伸')}——先过屈、内收、内旋，再保持过屈外展，最后外旋并伸直髋膝",
    f"仰卧位、{b('一个人')}就能做，不需要助手和特殊器械，术者腰背几乎不用力",
    f"但{red('只有 2 例、同一位术者')}，两例都在腰麻下完成，还谈不上“验证”",
]))

A.append(h2("一、为什么要找新办法"))
A.append(img(2))
A.append(cap("背景（编者根据原文整理）"))
A.append(p(f"髋关节脱位多由车祸等高能量外伤引起，{b('后脱位')}比前脱位常见。尽快复位不仅能缓解疼痛，也能降低股骨头缺血坏死等并发症的风险。"))
A.append(p(f"自 1870 年 Bigelow 描述闭合复位以来，各种改良方法层出不穷，但作者指出，它们的共同点是{b('都要牵引')}，区别只在于怎么省力："))
A.append(tcap("原文讨论中提到的复位方法（编者整理）"))
A.append(table(["思路", "代表方法"], [
    ["经典仰卧牵引", "Allis、Bigelow（术者腰背负担大，患者壮时尤其难）"],
    ["改良以减轻腰背负担", "Lefkowitz、Captain Morgan、Tulsa、Rochester、Whistler、East Baltimore 抬举、Piggy Back"],
    ["改变患者体位", "Skoff、对抗牵引（侧卧）；Stimson 重力法（俯卧）"],
    ["加辅助牵引或支点", "Howard 法、侧方牵引、屈曲内收法（需助手推股骨头）、足支点法、Waddell 法"],
    ["借助设备", "牵引床（Shigemura 法）、液压升降装置（Zwank 法）——省力但费时费设备"],
]))

A.append(h2("二、怎么做：六步口诀"))
A.append(img(3))
A.append(cap("操作要点（据原文整理）"))
A.append(img(4))
A.append(cap("原文图 1a、1b：起始握法"))
A.append(img(5))
A.append(cap("原文图 1c、1d：过屈、内收、内旋"))
A.append(img(6))
A.append(cap("原文图 2a、2b：保持过屈，外展"))
A.append(img(7))
A.append(cap("原文图 2c、2d：外旋、伸直"))
A.append(img(8))
A.append(cap("原文图 2e、2f：复位完成"))
A.append(p(f"整个过程每一步都是{b('“逐渐”')}完成的，原文没有描述需要用力牵拉或推压股骨头的环节。作者认为，正因为不需要用力，{b('术者和患者的体格都不影响操作')}，转运床上也能做。"))

A.append(h2("三、两个病例"))
A.append(img(9))
A.append(cap("两个病例（据原文整理）"))
A.append(img(10))
A.append(cap("原文图 3：病例 1 复位前后"))
A.append(img(11))
A.append(cap("原文图 4：病例 2 复位前后"))
A.append(p(f"病例 2 在外院{b('多次复位失败')}后转来，用这一方法复位成功，这是全文最有说服力的一点。不过原文没写外院用的是什么方法、是否在麻醉下进行，所以两者没法直接比较。"))

A.append(h2("这篇文章能信几分"))
A.append(img(12))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('病例报告')}：2 例、同一位术者，没有复位时间、尝试次数、并发症随访等数据",
    "两例都在腰麻、肌肉完全松弛下完成；急诊科常用的镇静条件下是否同样容易，原文没有数据",
    "陈旧性脱位、合并髋臼或股骨头骨折的脱位、人工关节脱位都没有试过",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "版权声明写的是“CC BY 4.0”，但链接指向 CC BY-NC 4.0，正文也写“非商业性复制”",
    "摘要说该方法“不受术者和患者体格影响”，但依据只是 2 例（一位健壮、一位中等体型）",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"记住口诀：{b('屈—内收—内旋 → 外展 → 外旋—伸')}，术者站在对侧，一手握踝、一手扶膝",
    "适用于急性、单纯的后脱位；合并骨折者原文未试，应按常规评估和处理",
    "复位后按常规确认关节同心、无医源性骨折，并检查神经血管情况（原文两例均已确认）",
    "作为传统牵引法之外的一个备选，尤其适合人手不够、患者体格壮时；但它还需要更多病例来验证",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Mugalur A. “No Traction” Technique: A Novel, Simple, Easy, and Ergonomic Maneuver to Reduce Posterior Dislocation of the Hip Joint – A Case Report. J Orthop Case Rep. 2026;16(5):156-160. doi:10.13107/jocr.2026.v16.i05.7240</em><br>"
    "原文为开放获取，许可链接为知识共享署名-非商业性使用 4.0（CC BY-NC 4.0），版权归原作者所有。本文为非商业的学术交流中文解读：原文图 1～4 引自原文，切分为单幅并加了中文标签，X 线上的“RIGHT”改为“右”；整理卡为编者根据原文撰写。仅供学习交流，如有侵权请联系删除。"
))
TITLE = "「髋关节」后脱位不用牵引也能复位？一个人就能做的六步手法（附步骤图）"
PTITLE = "髋后脱位不牵引复位推文"
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
