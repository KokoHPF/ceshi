#!/usr/bin/env python3
"""肘关节内外侧副韧带术后早期康复 3 例（Kim 等 2020）推文。

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
    "Kim SE, Choi YC, Lee JY. Early Rehabilitation after Surgical Repair of Medial and Lateral Collateral Elbow Ligaments: A Report of Three Cases. Int J Environ Res Public Health. 2020;17(17):6133. doi:10.3390/ijerph17176133",
    "作者单位：韩国世宗大学体育系、江陵原州大学体育系",
    f"文章类型：{b('病例报告')}（3 例，随访 2 年）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"3 位肘关节{b('内侧＋外侧副韧带')}同时受伤的非职业运动员，术后{b('第 7 天')}开始被动活动，第 6 周加弹力带抗阻，第 3 个月加神经肌肉训练",
    f"大致时间线：{b('6 周')}回日常生活 → {b('约 3 个月')}活动度基本回来 → {b('约 6 个月')}肌力明显提高 → {b('4～8 个月')}回到业余运动",
    f"2 年随访：X 线正常、没有不稳，肌力都在健侧的 {b('90% 以上')}；全程{b('没有出现并发症')}",
    f"但{red('只有 3 例、没有对照')}，只能说明“这样练没出事”，不能证明早练比晚练好",
]))

A.append(h2("一、为什么关注内外侧一起伤"))
A.append(p(f"肘关节韧带损伤里，研究最多的是投掷运动员的{b('内侧副韧带（尺侧副韧带）')}损伤，康复方案也大多为他们设计。而{b('外侧副韧带单独损伤、或内外侧一起伤')}，多由跌倒脱位等外伤引起，发生得少，相关康复报告也少。"))
A.append(p(f"作者想看看：对这类复合损伤，术后{b('早一点开始动')}是否安全、能否顺利恢复活动度和肌力。"))
A.append(img(2))
A.append(cap("三位患者（据原文表 1 整理）"))

A.append(h2("二、康复方案：五期推进"))
A.append(img(3))
A.append(cap("五期康复方案（据原文表 2 整理）"))
A.append(p(f"几个时间点的考虑：皮肤缝合约 2～3 周愈合，肌腱和肌肉缝合处约 6 周才能稳定承受张力。所以{b('屈伸抗阻放在 6 周')}；而旋前旋后会给韧带带来{b('内外翻应力')}，复合损伤更怕这个，所以被动旋转推迟到 3 周、旋转抗阻推迟到 3 个月。"))
A.append(img(4))
A.append(cap("原文图 1：病例 A 的 X 线、被动活动和弹力带练习"))
A.append(p(f"神经肌肉训练从 3 个月开始，先站着推墙、再跪姿，难度从稳定的 BOSU 到大球、再到最小最不稳的球。作者说，考虑到患者不是职业运动员，{b('为安全起见以站姿为主')}。"))
A.append(img(5))
A.append(cap("原文图 2：神经肌肉训练"))

A.append(h2("三、恢复得怎么样"))
A.append(p(f"测量方法：量角器测活动度；等速肌力仪（30°/s，仰卧）测屈伸肌力，为安全起见{b('术后 3 个月才开始测')}；握力计测握力；Oxford 肘评分（OES）评估日常功能和疼痛。"))
A.append(img(6))
A.append(cap("活动度变化（据原文图 3a 重画）"))
A.append(img(7))
A.append(cap("肌力占健侧的百分比（据原文图 3b～d 计算重画）"))
A.append(img(8))
A.append(cap("Oxford 肘评分变化（据原文表 3 重画）"))
A.append(p(f"值得注意的是，3 人在{b('术后 6 周')}都“回到了日常生活”，但这时 OES 只有 {b('4～10 分')}（满分 48）——作者引用的数据是，40～50 岁无症状人群的最低分也有 12～16 分。也就是说，{mk('能自理不等于不受影响')}。年轻男性（病例 C）各项恢复都明显更快，两位女性慢一些，作者认为也可能和受伤前的肌力、练习参与度有关。"))

A.append(h2("这篇文章能信几分"))
A.append(img(9))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('病例报告')}：3 人的年龄、性别、伤因（脱位、退变、过伸扭伤）和术式（开放修复、镜下修复、镜下重建）都不一样，没法互相比较",
    "大部分练习在家完成，作者没有记录练习频率，也说不清哪部分起了作用",
    "优点：方案写得具体，有 2 年随访，内外侧复合损伤这类报告本来就少",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "讨论说 2 年时活动度“约有 10% 的差距”，结论又说“完全恢复”；按图 3 数据，只有病例 B 差 5°（140° vs 145°）",
    "讨论说约 6 个月握力达到日常所需（女性 18 kg），但图 3 中病例 A、B 6 个月时只有 13、16 kg，到 12 个月才达到",
    "标题写“修复”，但病例 C 实际是用掌长肌腱重建内侧副韧带，病例 A 只修了外侧",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"内外侧副韧带术后，若手术医生认可修复牢靠，可参考这条时间线：{b('7 天被动屈伸 → 3 周被动旋转 → 6 周屈伸抗阻 → 3 个月旋转抗阻和神经肌肉训练 → 6 个月离心和抛接')}",
    f"等长收缩、握力练习和{b('肩胛骨练习')}从一开始就能做，不影响术区",
    f"复合损伤要格外小心{b('内外翻应力')}，旋前旋后比屈伸晚加",
    "跟患者说清预期：6 周能自理但还很不方便，回业余运动大约要 4～8 个月，肌力接近健侧可能要 1～2 年",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Kim SE, Choi YC, Lee JY. Early Rehabilitation after Surgical Repair of Medial and Lateral Collateral Elbow Ligaments: A Report of Three Cases. Int J Environ Res Public Health. 2020;17(17):6133. doi:10.3390/ijerph17176133</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1、2 引自原文，图中中文标签为编者所加；结果图由编者根据原文图 3 和表 3 的数据重画；整理卡为编者根据原文撰写。"
))
TITLE = "「肘关节」内外侧副韧带术后，第 7 天就能动？3 例早期康复的时间线和 2 年随访"
PTITLE = "肘侧副韧带术后康复推文"
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
