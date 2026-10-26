#!/usr/bin/env python3
"""自主神经再校准治疗肌筋膜痛病例系列（Seton 等 2024）推文。

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
    "Seton B, Pandey R, Piscura MK, Pearson WG Jr. Autonomic recalibration: a promising approach for alleviating myofascial pain explored in a retrospective case series. Cureus. 2024;16(1):e52450. doi:10.7759/cureus.52450",
    "作者单位：美国爱德华·维亚骨科医学院（奥本校区）生物医学研究部",
    f"文章类型：{b('回顾性病例系列')}（3 例）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"作者提出“{b('自主神经再校准')}”（AR）：认为慢性肌筋膜痛源于交感神经长期“过度警觉”，先从头到脚触诊找出一碰就躲的部位，再用两种手法“重置反射”，并结合创伤回忆和呼吸",
    f"3 个病例（9 岁腰椎滑脱、68 岁多次腹部手术后腹痛、56 岁腰椎融合术后痛）{b('都在 1～2 次治疗内疼痛降到 0')}，两人停用了阿片类药物",
    f"但这是{red('只有 3 例、没有对照、也没测任何自主神经指标')}的病例报告，效果好得不寻常，{mk('只能当作一种思路，不能当证据')}",
]))

A.append(h2("一、为什么从自主神经入手"))
A.append(img(2))
A.append(cap("背景（编者整理）"))

A.append(h2("二、AR 怎么做"))
A.append(img(3))
A.append(cap("AR 流程（据原文图 1 改画）"))
A.append(img(4))
A.append(cap("原文图 2：NSE 评估和 PRRT 按压示例"))
A.append(ul([
    f"{b('伤害性惊跳检查（NSE）')}：不是找压痛点，而是找“{b('正常力度一碰就回缩、抽动')}”的部位，作者认为这代表该处的原始保护反射过度兴奋",
    f"{b('原始反射释放技术（PRRT）')}：针对屈肌回缩反射和惊跳反射的“全身重置”，包括按压、关节挤压、摆位放松、轻叩；同时让患者回忆过去的创伤并配合呼吸",
    f"{b('疼痛中和技术（PNT）')}：患者专注于痛点时，治疗师轻压特定软组织点，直到所有“过度警觉区”消失",
    "两种技术都由个人（物理治疗师、医生）创立，原文引用的相关研究也都是病例系列或专著",
    f"复诊时如果触诊和活动都正常了还痛，作者认为可能有“{b('情绪驱动')}”，会做自主神经教育，并建议深呼吸、眼动脱敏与再处理（EMDR）等",
]))

A.append(h2("三、3 个病例"))
A.append(h3("病例 1：9 岁男孩，腰椎滑脱"))
A.append(img(5))
A.append(cap("病例 1（编者整理）"))
A.append(img(6))
A.append(cap("原文图 3：病例 1 首次治疗前后的触诊痛点"))
A.append(img(7))
A.append(cap("原文图 4：病例 1 一年后复发时第二次治疗前后"))
A.append(h3("病例 2：68 岁男性，多次腹部手术后慢性腹痛"))
A.append(img(8))
A.append(cap("病例 2（编者整理）"))
A.append(img(9))
A.append(cap("原文图 5：病例 2 首次治疗前后"))
A.append(img(10))
A.append(cap("原文图 6：病例 2 次日第二次治疗前后"))
A.append(h3("病例 3：56 岁男性，腰椎融合术后 14 年腰痛"))
A.append(img(11))
A.append(cap("病例 3（编者整理）"))
A.append(img(12))
A.append(cap("原文图 7：病例 3 首次治疗前后"))
A.append(img(13))
A.append(cap("原文图 8：病例 3 次日第二次治疗前后"))

A.append(h2("这篇文章能信几分"))
A.append(img(14))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('没有测量“自主神经”')}：题目叫自主神经再校准，但没有心率变异性、皮电、血压等任何客观指标，“交感过度”只是推测",
    f"{b('评估和疗效指标都是主观的')}：“过度警觉区”由治疗师自己触诊判断，没有盲法、没有信度检验；疼痛评分是患者当场口头报告",
    f"{b('很多因素混在一起')}：手法、触摸本身的放松、创伤回忆、呼吸、患者期望、自然病程……无法知道是哪一部分起作用",
    f"{b('随访短')}：除病例 1 外，最长只有约 4 周",
    "作者自己也承认需要有对照的大样本研究；致谢里注明文稿借助人工智能起草",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"病例 1 复发时，血液检查提示{b('类风湿关节炎')}，随后又诊断为{b('扩大性肌骨疼痛综合征')}，两者关系、是否接受风湿科治疗都没有交代",
    f"讨论里说病例系列“{b('证明了 AR 的疗效')}”，局限性部分又说疗效需要对照研究来验证，前后口径不一",
    f"病例 3 只随访约 4 周，却写成“{b('长期缓解')}”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"慢性疼痛患者确实常有应激、睡眠差、过度警觉，{b('关注创伤史、做疼痛教育、教放松呼吸')}都是有依据的做法",
    f"触诊时患者“一碰就躲”的反应可以作为{b('敏化程度的线索')}，但不要把它当成可靠的诊断工具",
    f"{red('不建议照搬“1～2 次治疗就停阿片类药物”')}：长期用药者停药要在开药医生指导下逐步减量",
    "儿童腰椎滑脱、术后腹痛这类有明确病理的情况，手法只能作为辅助，仍需专科随访",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Seton B, Pandey R, Piscura MK, Pearson WG Jr. Autonomic recalibration: a promising approach for alleviating myofascial pain explored in a retrospective case series. Cureus. 2024;16(1):e52450. doi:10.7759/cureus.52450</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 2～8 引自原文，中文标签为编者所加；原文图 1 由编者改画为中文；背景卡、病例卡和解读卡为编者整理。"
))

TITLE = "「肌筋膜痛」先“重置”交感神经再治痛？自主神经再校准的 3 个病例，以及为什么要谨慎看"
PTITLE = "自主神经再校准推文"
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
