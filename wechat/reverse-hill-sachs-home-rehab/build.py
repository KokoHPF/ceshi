#!/usr/bin/env python3
"""肩关节后脱位并发反 Hill-Sachs 损伤术后居家康复 1 例（周罗治非等 2021）推文。

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
    "周罗治非, 夏晓胜, 王梓力. 肩关节后脱位并发反 Hill-Sacks 损伤术后居家康复训练个案分析[J]. 中国康复理论与实践, 2021, 27(2): 230-236. doi:10.3969/j.issn.1006-9771.2021.02.018",
    "作者单位：中南大学湘雅三医院",
    f"文章类型：{b('个案分析')}（1 例，随访 10 个月）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"44 岁粉刷工，{b('癫痫发作')}后右肩后脱位并发反 Hill-Sachs 损伤，当地正位片{b('漏诊')} 2 周",
    f"关节镜下复位＋肩胛下肌填塞（McLaughlin 术）后，{b('完全在家康复')}：出院前床旁教 4 次，带纸质方案回家，远程答疑，定期门诊复评",
    f"四阶段方案：{mk('外展外旋位支具 8 周')}，前 8 周禁止内收、内旋",
    f"6 个月时前屈、外展、外旋恢复正常，肌力 5 级、不痛，改良 Rowe 评分 16 → {b('91')} 分，回到粉刷工作；10 个月时 {b('93')} 分",
    f"但{red('只有 1 例')}，主动内旋 10 个月仍只到 L1",
]))

A.append(h2("一、先了解这个病"))
A.append(img(2))
A.append(cap("背景（编者根据原文整理）"))

A.append(h2("二、病例"))
A.append(img(3))
A.append(cap("病例经过（据原文整理）"))
A.append(img(4))
A.append(cap("原文图 1：术前查体，右肩关节腔空虚"))
A.append(img(5))
A.append(cap("原文图 2～6：术前 X 线、CT、MRI 和术后第 2 天复查 CT"))
A.append(p(f"缺损约占肱骨头关节面的 {b('20%')}、稳定性差，正好落在手术指征（≥20%）上，所以选择了关节镜下 McLaughlin 术：把肩胛下肌固定到肱骨头缺损处，填住这个“坑”，防止肱骨头再卡回去。"))

A.append(h2("三、居家康复怎么做"))
A.append(img(6))
A.append(cap("居家康复的组织方式（据原文整理）"))
A.append(img(7))
A.append(cap("第一、二阶段（据原文表 1 整理）"))
A.append(img(8))
A.append(cap("原文图 7、8：外展外旋位支具"))
A.append(p(f"为什么固定在{b('外展外旋位')}？作者解释：软组织愈合前，肱骨在肩胛骨平面、盂肱关节中间位（前屈 45°、外展 45°）时软组织张力最小；超出肩胛平面会增加再脱位风险；软组织愈合需要 6～8 周。再加上本例合并韧带和肩袖损伤，所以支具戴满 8 周，第二阶段的被动活动也限制在肩胛骨平面内。"))
A.append(img(9))
A.append(cap("第三、四阶段（据原文表 1 整理）"))
A.append(img(10))
A.append(cap("原文图 9：居家康复锻炼"))

A.append(h2("四、恢复得怎么样"))
A.append(img(11))
A.append(cap("恢复曲线（据原文表 2 重画）"))
A.append(tcap("原文表 2（上）：活动度"))
A.append(table(["时间", "前屈", "外展", "外旋", "内旋"], [
    ["术前（主动）", "0～60°", "0～30°", "−10～0°", "腰骶部"],
    ["2 个月（被动）", "0～90°", "0～80°", "0～15°", "股骨粗隆下"],
    ["4 个月（主动）", "0～110°", "0～100°", "0～40°", "骶尾部"],
    ["6 个月（主动）", "0～180°", "0～180°", "0～90°", "L3"],
    ["10 个月（主动）", "0～180°", "0～180°", "0～90°", "L1"],
]))
A.append(tcap("原文表 2（下）：肌力、疼痛和功能"))
A.append(table(["时间", "肌力", "VAS", "改良 Rowe"], [
    ["术前", "未测", "6", "16"],
    ["2 个月", "2 级", "4", "51"],
    ["4 个月", "4 级", "0", "71"],
    ["6 个月", "5 级", "0", "91"],
    ["10 个月", "5 级", "0", "93"],
]))
A.append(img(12))
A.append(cap("原文图 10：术后 10 个月肩关节功能（右侧为患侧）"))
A.append(p(f"2 个月时{b('被动外旋只有 15°')}，作者认为与患者担心外旋会影响肩胛下肌愈合、练得太保守有关，后期经过心理疏导和强化训练明显改善。10 个月时主动内旋只到 L1（正常可达 T7），作者认为与肩胛下肌填入缺损后{b('内旋力臂缩短')}有关。"))

A.append(h2("这篇文章能信几分"))
A.append(img(13))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例')}，无法和住院或门诊康复比较；作者也提到缺乏专业手法治疗、理疗和早期心理辅导",
    "患者是体力劳动者、癫痫控制良好，结果不一定适用于其他人群",
    "优点：方案按周期写得非常具体，禁忌动作和理由都写清楚了，可直接参考",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "中文标题和正文写作“Hill-Sacks”，英文标题写作“Hill-Sachs”（后者为正确拼写）",
    "表 2 中术后 2 个月记录的是被动活动度，其余时间点是主动活动度，不能直接连成一条曲线比较",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"癫痫发作或电击后的肩痛、{b('肩关节腔空虚')}、外旋受限，要想到后脱位；正位片阴性时加拍腋位片或做 CT",
    f"McLaughlin 术后：外展外旋位支具约 8 周，{b('前 8 周禁止内收、内旋')}和向内钟摆；被动活动先限制在肩胛骨平面内",
    "第 9 周后再加内旋和肩袖主动训练，14 周后抗阻、本体感觉和抛接球",
    "居家康复要有书面方案、远程答疑和定期复评；留意患者“不敢练”的心理",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>周罗治非, 夏晓胜, 王梓力. 肩关节后脱位并发反 Hill-Sacks 损伤术后居家康复训练个案分析[J]. 中国康复理论与实践, 2021, 27(2): 230-236.</em><br>"
    "原文未见开放获取许可声明，版权归原作者及期刊所有。本文为非商业的学术交流解读：原文图 1～10 引自原文，图像未作修改；恢复曲线图由编者根据原文表 2 重画，整理卡为编者根据原文撰写。仅供学习交流，如有侵权请联系删除。"
))
TITLE = "「肩关节」后脱位＋反 Hill-Sachs 损伤术后，全靠在家练能恢复吗？四阶段居家康复方案"
PTITLE = "反Hill-Sachs术后居家康复推文"
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
