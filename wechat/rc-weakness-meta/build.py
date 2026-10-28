#!/usr/bin/env python3
"""肩袖相关肩痛的肩部无力：康复干预对肌力的作用（Zhang、Raguzzi 等 2026 JOSPT 系统综述与 meta 分析）推文。

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
    "Zhang B, Raguzzi IA, Dupuis F, Gianola S, Morgan-Daniel J, Roy JS, Pozzi F. Addressing Shoulder Weakness in Individuals With Rotator Cuff–Related Shoulder Pain: A Systematic Review With Meta-analysis. J Orthop Sports Phys Ther. 2026;56(2):67-84. doi:10.2519/jospt.2025.13445",
    "作者单位：美国佛罗里达大学物理治疗系；加拿大拉瓦尔大学、Cirris 研究中心；意大利米兰 Galeazzi 医院 等",
    f"文章类型：{b('系统综述与 meta 分析')}（33 项研究，28 项纳入合并；PROSPERO 预注册）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"肩袖相关肩痛（RCRSP）患者做 6～12 周康复后，肩部肌力普遍提高：{b('外旋为中等效应')}（SMD 0.56），外展、内旋、前屈、肩胛平面上举为小效应",
    f"提高主要来自{b('有主动运动的干预')}（力量训练、多模式康复）；单纯宣教、假治疗和自然病程组肌力没有变化",
    f"离心训练和神经肌肉电刺激的组内提高最大，但{red('数据组数很少、差异很大')}，作者也提醒谨慎解读",
    f"疗程 6、8、9、12 周的效果差不多，{b('疗程长短可能不是关键')}",
    f"注意：本文比的是{b('各组自己的练前练后')}，不是和对照组比，不能据此判断哪种练法更好",
]))

A.append(h2("一、为什么关注肩部无力"))
A.append(img(2))
A.append(cap("背景（据原文引言整理）"))
A.append(p(f"RCRSP 是一个把肩峰下疼痛、撞击综合征、肩袖肌腱病、非特异性肩痛和肩袖撕裂“打包”在一起的诊断名。这类患者常说{b('提东西、搬重物、运动时使不上劲')}，而且无力越明显，功能障碍越重、抑郁越多、生活质量越差。"))
A.append(p(f"指南强烈推荐主动运动，以往综述也证实运动能改善疼痛和功能，但{b('都没把肌力单独拿出来看')}。练完到底有没有变强？哪种练法、练多久更好？这篇综述想回答这些问题。"))

A.append(h2("二、怎么做的"))
A.append(img(3))
A.append(cap("研究方法（据原文整理）"))
A.append(img(4))
A.append(cap("原文图：PRISMA 文献筛选流程（原图未改动）"))
A.append(p(f"这篇综述的关键设计是{mk('只算“组内前后变化”')}：每个研究组自己“练前 vs 练后”算一个标准化均数差（SMD），再按测试方向（外旋、内旋、外展等）分别合并。这样随机试验和单组队列都能用上，但代价是{b('不能直接比较')}哪种干预更好。"))

A.append(h2("三、纳入了哪些研究"))
A.append(img(5))
A.append(cap("纳入研究概况（据原文结果整理）"))

A.append(h2("四、康复能把肌力练回来多少"))
A.append(img(6))
A.append(cap("所有干预合并的效应量（据原文表 4 重画）"))
A.append(img(7))
A.append(cap("按干预类型分组（据原文表 4 重画）"))
A.append(p(f"把所有干预合在一起，外旋、外展、内旋、前屈、肩胛平面上举的肌力都有提高，其中{b('外旋提高最明显')}；后伸和内收没有变化（数据也很少）。"))
A.append(p(f"分组看，{b('力量训练组')}外展、外旋都达到中等效应，内旋为小效应；{b('多模式组')}外旋中等，外展、内旋小。宣教、假治疗和自然病程组都没有效果。敏感性分析剔除高偏倚风险研究后，外展、外旋、内旋的结论依然成立，前屈和肩胛平面上举则不太稳定。"))

A.append(tcap("换算成千克：练完能多出多少力？（据原文表 7，单位 kg）"))
A.append(table(["方向", "研究数", "合并标准差", "力量训练组", "多模式组"], [
    ["外展", "4", "4.35", "1.74～3.35", "0.13～2.39"],
    ["外旋", "8", "3.24", "1.39～2.79", "0.75～2.98"],
    ["内旋", "8", "3.87", "1.32～2.29", "0.85～2.67"],
    ["肩胛平面上举", "3", "4.93", "1.28～4.49", "0.15～2.96"],
    ["前屈", "1", "2.04", "0.16～1.37", "无统计学意义"],
    ["后伸", "1", "1.34", "无统计学意义", "无统计学意义"],
]))
A.append(small("说明：原文用合并效应量 95% 置信区间的上下限乘以合并标准差，换算出平均提高的范围；原文另有按扭矩（N·m）和按体重标化的换算，这里只列千克。"))
A.append(p(f"也就是说，力量训练 6～12 周后，{b('外旋大约多出 1.4～2.8 kg')}，外展大约多出 1.7～3.4 kg。作者认为这可以作为临床上评估肌力恢复的参考。"))

A.append(h2("五、哪种练法提高最多"))
A.append(img(8))
A.append(cap("力量训练的类型（据原文表 5 重画）"))
A.append(ul([
    f"{b('离心训练')}：外旋提高最大（SMD 1.24），外展为中等；但 5 组之间差异极大（I² 93%），内旋则没有效果",
    f"{b('神经肌肉电刺激')}：外展、外旋、内旋都是大效应，但{red('只有 1～2 组数据')}",
    f"{b('运动控制训练、非特定力量训练')}：数据最多（4～9 组），一致性好（I² 0%），效果为小到中等",
    "大负荷、小负荷、血流限制训练、练健侧等都只有 1 组，几乎没法下结论",
]))

A.append(h2("六、练多久"))
A.append(img(9))
A.append(cap("疗程长度（据原文表 6 重画）"))
A.append(p(f"6、8、9、12 周的效应量相近，置信区间大幅重叠。作者认为{b('只要练够 6 周以上，疗程长短可能不是开处方时的关键')}，可以按患者偏好调整内容和时长。"))

A.append(h2("七、作者怎么解释"))
A.append(img(10))
A.append(cap("讨论要点（据原文整理）"))
A.append(p(f"作者特别提到：{b('肌力提高不一定带来疼痛和功能改善')}，反过来也一样。早期肌力回升多半是疼痛减轻后神经抑制解除，而不一定是肌肉长大了。"))

A.append(h2("这篇文章能信几分"))
A.append(img(11))
A.append(cap("编者解读"))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "表 5 中运动控制训练对外旋的 SMD 为 0.45，置信区间却写成 0.22～0.48，点估计不应落在区间之外",
    "偏倚风险部分的研究数和后面列的文献编号对不上：“9 项”后列了 10 篇、“13 项”后列了 11 篇，第 9 篇同时出现在两档",
    "正文说有 10 周疗程的 2 组，表 6 却没有 10 周这一行",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"RCRSP 患者如果有无力，康复里要{b('有主动运动和渐进抗阻')}，单靠宣教或被动治疗很难把肌力练回来",
    f"至少练 {b('6 周')}再评估肌力；外旋通常提高最明显，外展、内旋次之",
    "可以用手持测力计定期复测，把“外旋多出 1.4～2.8 kg”当作大致参照；测试方法前后要一致",
    "离心训练、电刺激可以作为备选，但证据还很少，不必神化",
    "刺激性高、疼痛明显的患者可能耐受不了足够负荷，需要先控制症状、逐步加量",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Zhang B, Raguzzi IA, Dupuis F, Gianola S, Morgan-Daniel J, Roy JS, Pozzi F. Addressing Shoulder Weakness in Individuals With Rotator Cuff–Related Shoulder Pain: A Systematic Review With Meta-analysis. J Orthop Sports Phys Ther. 2026;56(2):67-84.</em><br>"
    "原文版权归 JOSPT, Inc. 所有（All rights reserved），非开放许可。本文为非商业的学术交流中文解读：流程图引自原文，图像未作修改；效应量图由编者根据原文表 4～6 重画，千克换算表据原文表 7 整理，其余整理卡为编者根据原文撰写。仅供学习交流，如有侵权请联系删除。"
))
TITLE = "「肩关节」肩袖相关肩痛、肩膀没劲？28 项研究看康复能把肌力练回来多少"
PTITLE = "肩袖相关肩痛肌力康复推文"
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
