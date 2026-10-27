#!/usr/bin/env python3
"""rTMS 联合常规康复治疗桡骨远端骨折后 CRPS-I 1 例（古丽加克拉·艾山等 2020）推文。

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
    "古丽加克拉·艾山, 陈婵, 高天昊, 凌骏麒, 孙莉敏, 白玉龙. 重复经颅磁刺激联合常规康复对桡骨远端骨折后复杂区域性疼痛综合征Ⅰ型患者上肢功能影响 1 例报道[J]. 中国康复理论与实践, 2020, 26(2): 232-236. doi:10.3969/j.issn.1006-9771.2020.02.017",
    "作者单位：复旦大学附属华山医院康复医学科",
    f"文章类型：{b('病例报告')}（1 例，治疗 3 周）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"67 岁女性桡骨远端骨折，石膏固定后手腕{b('肿痛反而加重')}、皮温升高、皮肤发红，诊断为 {b('Ⅰ型复杂区域疼痛综合征（CRPS）')}",
    f"治疗 3 周：药物＋{b('重复经颅磁刺激（rTMS）')}（大脑运动皮层高频＋颈 7 棘突旁低频）＋淋巴引流＋理疗＋运动和作业治疗",
    f"疼痛 VAS {b('8 → 2 分')}，改良 Barthel 指数 {b('85 → 100 分')}，前臂旋转 55° → 90°，腕屈伸 20° → 42°",
    f"但{red('同时用了很多种治疗、没有对照')}，无法判断 rTMS 本身贡献了多少",
]))

A.append(h2("一、CRPS 是什么"))
A.append(img(2))
A.append(cap("背景（编者根据原文整理）"))
A.append(p(f"桡骨远端骨折是老年人最常见的骨折。骨折后出现 CRPS，会让肿胀、疼痛雪上加霜，普通止痛药效果差，进而导致肢体僵硬、影响睡眠和工作。原文提到，{b('伤后 1 周内的剧痛')}是发生 CRPS 的危险因素，{b('女性')}发生率明显高于男性。"))

A.append(h2("二、病例"))
A.append(img(3))
A.append(cap("病例经过（据原文整理）"))
A.append(img(4))
A.append(cap("原文图 1：左手外观、X 线和骨扫描"))
A.append(p(f"这个病例的典型线索是：{mk('骨折已经愈合，肿痛却越来越重')}，还伴有皮温升高、皮肤发红、关节普遍僵硬。上肢血管 B 超排除了血栓，三相骨扫描显示患侧多个关节骨代谢增强，符合国际疼痛研究学会（IASP）的 CRPS 诊断标准。"))

A.append(h2("三、怎么治"))
A.append(img(5))
A.append(cap("治疗方案（据原文整理）"))
A.append(p(f"治疗顺序值得注意：就诊时疼痛、水肿太明显，{b('没法做主动活动和关节活动度训练')}，所以先用药物、rTMS 和淋巴引流控制疼痛和水肿，等缓解后再开始{b('不引起疼痛的被动关节活动')}，并让左手作为辅助手参与日常生活。"))
A.append(img(6))
A.append(cap("原文图 2：左手肿胀的变化"))
A.append(img(7))
A.append(cap("原文图 3：握拳的变化"))

A.append(h2("四、结果"))
A.append(img(8))
A.append(cap("疗效指标（据原文正文重画）"))
A.append(img(9))
A.append(cap("关节活动度（据原文表 1、表 2 重画）"))
A.append(tcap("原文表 1：肘、前臂、腕关节被动活动度（°）"))
A.append(table(["", "肘屈曲/伸展", "前臂旋前/旋后", "腕屈曲/伸展", "腕桡偏/尺偏"], [
    ["治疗前", "87", "55", "20", "5"],
    ["治疗后", "100", "90", "42", "30"],
]))
A.append(tcap("原文表 2：手指关节被动活动度（°，治疗前 → 治疗后）"))
A.append(table(["", "MCP", "PIP", "DIP"], [
    ["拇指", "25 → 35", "20 → 45", "—"],
    ["示指", "20 → 43", "20 → 55", "15 → 40"],
    ["中指", "25 → 44", "35 → 60", "0 → 35"],
    ["环指", "10 → 30", "20 → 45", "10 → 20"],
    ["小指", "5 → 26", "15 → 30", "10 → 20"],
]))
A.append(p("MCP＝掌指关节，PIP＝近端指间关节，DIP＝远端指间关节。", "font-size:13px;color:#888;"))

A.append(h2("五、作者为什么选 rTMS"))
A.append(img(10))
A.append(cap("作者的思路（据原文讨论整理）"))

A.append(h2("这篇文章能信几分"))
A.append(img(11))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例')}、治疗只有 3 周，没有长期随访；改善可能部分来自 CRPS 的自然病程",
    "药物（塞来昔布、唑来膦酸）、淋巴引流、理疗、运动和作业治疗同时进行，无法拆分 rTMS 的作用",
    "颈 7 棘突旁低频 rTMS“抑制颈交感干”是作者的推测，原文没有给出客观的交感功能指标",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "rTMS 参数写成范围（10～20 Hz、80%～100% 阈值、“10～15 次治疗或 iTBS”），而“每天 1 次、治疗 3 周”又不止 15 次，看不出本例实际方案",
    "表 1 表头写“屈曲/伸展”“旋前/旋后”等，每格却只有一个数",
    "讨论部分的参考文献编号与内容错位（如“伤后 1 周内剧痛”一句标 [19]，实为 [18]）",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"骨折石膏固定期间或拆除后，肿痛{b('不减反增')}、皮温高、皮肤发红、关节普遍僵硬 → 要想到 CRPS，先排除血栓",
    f"急性期以{b('控制疼痛和水肿')}为先：淋巴引流、抬高患肢等；缓解后再做{b('不引起疼痛')}的被动活动，避免“越痛越练”",
    "让患手作为辅助手参与日常生活，减少废用",
    "rTMS 可作为综合方案的一部分，但需要有设备和资质的机构；参数应参照指南",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>古丽加克拉·艾山, 陈婵, 高天昊, 凌骏麒, 孙莉敏, 白玉龙. 重复经颅磁刺激联合常规康复对桡骨远端骨折后复杂区域性疼痛综合征Ⅰ型患者上肢功能影响 1 例报道[J]. 中国康复理论与实践, 2020, 26(2): 232-236.</em><br>"
    "原文未标注开放获取许可，版权归原作者和期刊所有。本文为非商业的学术交流解读：原文图 1～3 引自原文，图像未作修改，说明见图注；疗效图和活动度图由编者根据原文数据重画，整理卡为编者根据原文撰写。仅供学习交流，如有侵权请联系删除。"
))
TITLE = "「CRPS」桡骨远端骨折后手越来越肿痛？经颅磁刺激＋常规康复 3 周的 1 例报告"
PTITLE = "骨折后CRPS经颅磁刺激推文"
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
