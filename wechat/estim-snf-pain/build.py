#!/usr/bin/env python3
"""高龄患者肩胛盂骨折＋肱骨头脱位后辅助电刺激 1 例（Rodriguez Reyes 等 2025）推文。

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
    "Rodriguez Reyes DA, Kominami E, Kang J, Darouian N. Adjunctive Use of Electrical Stimulation (E-Stim) for Pain Relief and Rehabilitation in a Skilled Nursing Facility Patient Following Right Glenoid Fracture and Humeral Head Dislocation. Cureus. 2025;17(6):e86690. doi:10.7759/cureus.86690",
    "作者单位：美国加州大学洛杉矶分校（UCLA）David Geffen 医学院、Fireside 医疗中心康复医学科",
    f"文章类型：{b('病例报告')}（1 例）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"87 岁女性跌倒后右肱骨头{b('后脱位')}，合并肩胛盂骨折、大结节骨折和多发肋骨骨折；闭合复位后因高龄选择{b('保守治疗')}",
    f"在专业护理机构（SNF）康复时{b('疼痛明显、限制了训练')}，治疗团队在常规物理和作业治疗之外加用了{b('电刺激')}",
    "电刺激过程中无痛、无并发症；患者能更好地参与训练，从“动不了”到能长时间坐直、用左手完成日常活动",
    f"但{red('没有任何量化数据')}，也没写电刺激参数，只能当作一个思路参考",
]))

A.append(h2("一、病例"))
A.append(img(2))
A.append(cap("病例经过（据原文整理）"))
A.append(img(3))
A.append(cap("原文图 1：复位前右肩 X 线"))
A.append(p(f"出院复查时，肱骨头已{b('同心复位')}，但大结节骨块向内侧移位。骨科综合考虑患者的年龄、合并症以及肩关节对位尚好，{b('没有手术')}，建议物理治疗、限制活动和定期复查影像。"))

A.append(h2("二、在护理机构怎么康复"))
A.append(img(4))
A.append(cap("康复安排（据原文整理）"))
A.append(img(5))
A.append(cap("原文图 3：坐在轮椅上进行肩胛周围电刺激"))
A.append(img(6))
A.append(cap("原文图 4：三角肌上的电极片"))
A.append(p(f"电刺激在治疗师监督下进行，针对{b('斜方肌、菱形肌、肩袖和三角肌')}，目的有三个：控制疼痛、改善局部循环、神经肌肉再教育。原文没有说明具体用的是哪种电刺激、频率和强度是多少、每次多长时间、一共做了多久。"))
A.append(img(7))
A.append(cap("电刺激简介（据原文引言和讨论整理）"))

A.append(h2("三、结果"))
A.append(img(8))
A.append(cap("结果（原文只有文字描述）"))

A.append(h2("这篇文章能信几分"))
A.append(img(9))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例、没有对照')}，也没有疼痛评分、活动度、功能量表等任何量化指标",
    "电刺激是在每周 5 天、每次 1 小时的物理和作业治疗基础上加用的，无法区分是谁起的作用",
    "结论说电刺激“加快了康复”“缩短住院时间”，但文中没有任何可供比较的时间数据",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "图 1（4 月 13 日，复位前）和图 2（4 月 29 日，复位后）是完全相同的同一张图片，图注却分别描述为脱位和已复位",
    "讨论把文献 [5] 说成“荟萃分析”，实际是一项偏瘫肩关节半脱位的随机对照试验；文献 [6] 被引为术后电刺激证据，实际是老年人运动建议指南",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"高龄、不能手术、患肢不负重的患者，{b('疼痛常常是康复的最大障碍')}；在常规训练外，可考虑加电刺激帮助控制疼痛、提高训练耐受度",
    "患侧受保护期间，同样要练健侧和肘、腕、手，尽早恢复坐位和日常自理",
    "使用时选择好类型（以止痛为主的 TENS 或以引起肌肉收缩为主的 NMES）并记录参数和疼痛、功能变化，才能判断是否真的有效",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Rodriguez Reyes DA, Kominami E, Kang J, Darouian N. Adjunctive Use of Electrical Stimulation (E-Stim) for Pain Relief and Rehabilitation in a Skilled Nursing Facility Patient Following Right Glenoid Fracture and Humeral Head Dislocation. Cureus. 2025;17(6):e86690. doi:10.7759/cureus.86690</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1、3、4 引自原文，图像未作修改（原文图 2 与图 1 为同一张图片，未重复使用）；整理卡为编者根据原文撰写。"
))
TITLE = "「肩关节」87 岁老人肩胛盂骨折＋肩脱位不能手术，疼得练不动？加用电刺激的 1 例报告"
PTITLE = "高龄肩脱位电刺激推文"
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
