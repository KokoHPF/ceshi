#!/usr/bin/env python3
"""Manske 2025 踝关节三角韧带肌骨超声推文：生成 article_body.html 与 preview.html。

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


def pic(n, t, w=None):
    h = img(n)
    if w:
        h = h.replace("width:100%;max-width:100%;", f"width:{w};max-width:{w};")
    return h + cap(t)


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2025 年第 20 卷第 4 期，“肌骨超声小贴士”栏目）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Diagnostic Musculoskeletal Ultrasound in the Evaluation of the Deltoid Ligament of the Ankle（诊断性肌骨超声评估踝关节三角韧带）",
    f"{b('作者')}：Robert C. Manske, PT, DPT · Chris Wolfe, PT, DPT · Phil Page, PT, PhD · Michael Voight, PT, DHSc",
    f"{b('栏目')}：MSK Ultrasound Bites: Tips and Tricks（肌骨超声小贴士）",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2025;20(4):641-647",
    f"{b('PMCID')}：PMC11964700",
    f"{b('关键词')}：musculoskeletal ultrasound · deltoid ligament · ankle instability · ligament injury · rehabilitation · dynamic imaging",
], square=True))

A.append(h2("🎯 背景：三角韧带伤得少，但漏诊后果重"))
A.append(p(
    f"踝扭伤是临床最常见的肌骨问题之一，{b('三角韧带')}受累占所有踝扭伤的 {b('10%～15%')}。它常与踝骨折或高能量创伤同时发生，但运动和日常活动中也可能单独损伤；如果没有准确诊断和处理，可能导致{red('慢性疼痛和内侧不稳')}。"
))
A.append(p(
    f"MRI 是韧带评估的金标准，但费用、可及性和等待时间限制了它在康复场景中的使用。肌骨超声{hl('便携、实时、便宜')}，还能做{b('动态应力检查')}——外翻应力下内侧结构的移位即可诊断三角韧带损伤。"
    f"文中引用的综述称，超声区分正常与损伤三角韧带的{b('敏感度达 0.90')}。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["项目", "要点"],
    [
        ["探头", "高频线阵探头（7～15 MHz），沿内踝放置，调整角度兼顾浅层和深层、前部和后部"],
        ["体位", "仰卧（或侧卧），髋膝伸直，下肢外旋；看胫跟韧带和后部纤维时把踝背屈，给韧带静态牵伸"],
        ["三个切面", "内踝前丘 → 舟骨结节（胫舟韧带）；内踝前丘 → 载距突（胫跟韧带 + 胫距后深韧带前部）；内踝后丘 → 距骨后内侧结节（胫距后浅韧带 + 胫距后深韧带后部）"],
        ["正常表现", "浅层为高回声、纤维状、边界连续清楚；深层纤维因位置较深可呈低回声"],
        ["急性损伤", "水肿性低回声增厚、纤维结构中断、部分/完全撕裂、关节积液；能量多普勒看充血"],
        ["慢性损伤", "韧带变薄、低回声，周围纤维化或钙化，应力下动态不稳"],
        ["局限", "依赖操作者；深部和骨性/关节内病变仍需 MRI"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('记住 5 个骨性标志、3 个切面，对比健侧并加应力动态观察，超声就能快速判断三角韧带各部分是否受伤')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、三角韧带的解剖"))
A.append(p(
    f"三角韧带也叫{b('踝内侧副韧带')}，是位于踝内侧的{b('双层三角形')}结构，从内踝延伸到足部诸骨。它抵抗外翻，并限制距骨外旋。"
    f"经典损伤机制是{b('强力外翻')}，常合并外踝骨折；另一机制是内翻扭伤，尤其见于慢性外侧不稳的患者。"
))
A.append(table(
    ["层次", "组成", "主要作用"],
    [
        ["浅层", "胫跟韧带（胫骨 → 跟骨）；胫舟韧带（向舟骨延伸）；胫距后浅韧带（稳定距骨后部）", "广泛对抗外翻"],
        ["深层", "胫距前韧带；胫距后深韧带", "稳定距骨，对抗内移和外旋（过度旋转）"],
    ],
))
A.append(p("理解分层结构和功能，是准确超声评估和区分损伤严重程度的前提。"))

A.append(h3("❇️二、超声评估韧带的优势与局限"))
A.append(ul([
    f"{b('实时成像')}：可在关节活动中动态评估韧带完整性",
    f"{b('高分辨率')}：能显示三角韧带的各个组成部分",
    f"{b('可及、省钱')}：便携、普及，比 MRI 便宜",
    f"{b('动态应力测试')}：在功能动作中直接看到韧带被拉长或断裂",
    f"{b('局限')}：依赖操作者经验；深部结构显示不如 MRI；骨和钙化会产生伪像，需要调整探头位置和频率",
]))

A.append(h3("❇️三、扫查技术"))
A.append(ul([
    f"{b('探头')}：高频线阵 7～15 MHz",
    f"{b('体位')}：仰卧或侧卧，踝轻度跖屈，便于看内侧结构（文中配图则采用仰卧、髋膝伸直、下肢外旋，并在部分切面把踝背屈）",
    f"{b('动态评估')}：外翻应力或背屈等应力手法，显示韧带不稳或断裂",
    f"{b('① 浅层')}：从内踝开始向远端扫查胫跟韧带和胫舟韧带；用{b('能量多普勒')}寻找提示炎症或急性损伤的充血；注意提示水肿的低回声区和纤维结构中断",
    f"{b('② 深层')}：靠近距骨评估；在静态和动态模式之间逐步切换，可发现部分撕裂或扭伤",
    f"{b('③ 对比健侧')}：以健侧为基线，尤其适用于怀疑部分撕裂时",
]))
A.append(pic(2, "图1：体位与骨性标志。1A 仰卧，髋膝伸直，下肢外旋；1B 标记：(1) 舟骨结节，(2) 内踝前丘，(3) 跟骨载距突，(4) 内踝后丘，(5) 距骨后内侧结节"))

A.append(h3("❇️四、正常声像图：三个切面"))
A.append(p(f"正常三角韧带浅层呈{b('高回声、纤维状、边界连续清楚')}；深层纤维因位置较深可呈低回声。后部三角韧带回声更低，深层胫距纤维不如前部浅层韧带清楚。应力手法可帮助确认韧带完整。"))
A.append(h4("🔻切面一：胫舟韧带（前部纤维）"))
A.append(p(f"仰卧、髋膝伸直、下肢外旋。探头沿{b('内踝前丘（标志 2）与舟骨结节背侧（标志 1）')}的连线放置，长轴切面上即可看到胫舟韧带纤维。"))
A.append(pic(3, "图2：胫舟韧带。2A 探头位置（黑框连接标志 2 与 1）；2B 实际放置；2C 正常长轴声像图；2D 标注图：胫骨与距骨、舟骨浅层的胫舟韧带（标注已改为中文）"))
A.append(h4("🔻切面二：胫跟韧带（中部纤维）和胫距后深韧带前部"))
A.append(p(f"检查者把患者踝{b('背屈')}，给胫跟韧带施加静态牵伸。探头沿{b('内踝前丘（标志 2）与跟骨载距突（标志 3）')}的连线放置，可同时看到浅层的胫跟韧带和其深面从内踝到距骨的{b('胫距后深韧带前部纤维')}。"))
A.append(pic(4, "图3：胫跟韧带与胫距后深韧带前部。3A 探头位置（连接标志 2 与 3）；3B 背屈下放置探头；3C 正常长轴声像图；3D 标注图：胫骨、载距突/跟骨之间浅层为胫跟韧带，深层为胫距后深韧带前部（标注已改为中文）"))
A.append(h4("🔻切面三：胫距后浅韧带和胫距后深韧带后部"))
A.append(p(
    f"同样背屈踝关节，探头沿{b('内踝后丘（标志 4）与距骨后内侧结节（标志 5）')}的连线长轴放置。"
    f"关键参照是短轴切面上的{b('胫后肌腱')}——它正下方就是后部三角韧带的深层关节囊带。"
))
A.append(pic(5, "图4：胫距后浅韧带与胫距后深韧带后部。4A 探头位置（连接标志 4 与 5）；4B 实际放置；4C 正常长轴声像图；4D 标注图：胫后肌腱、趾长屈肌腱深面依次为胫距后浅韧带和胫距后深韧带后部（标注已改为中文）"))

A.append(h3("❇️五、病理表现"))
A.append(table(
    ["类型", "超声征象"],
    [
        ["急性扭伤", "水肿导致的低回声增厚；纤维结构中断；部分或完全撕裂，可见不连续或回缩；伴关节积液"],
        ["慢性损伤与功能不全", "韧带变薄、回声减低；韧带周围纤维化或钙化；应力手法下动态不稳"],
    ],
))
A.append(pic(6, "图5：胫舟韧带完全断裂。长轴切面上韧带呈低回声中断（蓝箭头）；把踝关节完全跖屈做应力成像，可进一步确认完全撕裂（对照图 2）"))
A.append(pic(7, "图6：胫跟韧带和胫距后深韧带前部部分撕裂。6A 胫骨近端附着处部分撕裂，胫跟韧带增厚，两条韧带均呈低回声（蓝箭头）；6B 增厚韧带内可见钙化（黄箭头）（对照图 3）"))
A.append(pic(8, "图7：胫距后浅韧带慢性增厚（蓝箭头）和胫距后深韧带后部部分撕裂（黄箭头），后者呈不均匀低回声（对照图 4；标注已改为中文）"))

A.append(h3("❇️六、对康复人员的意义"))
A.append(ul([
    f"{b('早期发现、准确分级')}：快速区分扭伤与更严重的撕裂，指导治疗计划",
    f"{b('动态功能测试')}：治疗中监测恢复、动态评估韧带功能；{b('系列超声')}帮助判断韧带重塑情况，以及是否可以进阶",
    f"{b('引导介入')}：超声引导精准注射，如糖皮质激素抗炎或富血小板血浆（PRP）促进韧带再生",
    f"{b('患者教育')}：实时图像直观解释损伤，建立合理的恢复预期",
    f"{b('局限')}：怀疑骨性结构损伤或深部关节内病变等复杂情况时，超声不能完全替代 MRI；对操作技术的要求也限制了它的普及",
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：简短的技术栏目文章，没有原始数据，以作者经验和少量文献为主",
    f"{b('亮点')}：5 个骨性标志 + 3 个标准切面，配有探头摆放照片、正常声像图、标注图和对应的病理图，非常适合入门",
    f"{b('“超声优于 MRI”的说法需谨慎')}：引言称系统评价显示超声的合并敏感度和特异度优于 MRI 等，但结论部分又说 MRI 是金标准、超声不能完全替代；敏感度 0.90 的来源和研究条件未交代",
    f"{b('名称不统一')}：解剖部分说深层由“胫距前韧带和胫距后深韧带”组成，图中却用“胫距后深韧带前部/后部”；图 4 图注把胫距后浅韧带也称为“深层后部三角韧带”",
    f"{b('体位前后不一')}：技术部分写踝“轻度跖屈”，而图 3、图 4 的方法是踝“背屈”牵伸韧带",
    f"{b('图注笔误')}：图 6 图注写“图 7B 可见钙化”，应为图 6B；图 2D 原标注“Tibonavicular”拼写错误；正文另有“offers and readily”“it’s”等笔误",
]))

A.append(h2("📌 总结：超声看三角韧带，记住这几点"))
A.append(p(
    f"{red('① 解剖')}：浅层（胫跟、胫舟、胫距后浅）抗外翻，深层（胫距前、胫距后深）稳定距骨、抗外旋<br>"
    f"{red('② 标志')}：舟骨结节、内踝前丘、载距突、内踝后丘、距骨后内侧结节<br>"
    f"{red('③ 切面')}：前丘 → 舟骨结节；前丘 → 载距突；后丘 → 距骨后内侧结节（以胫后肌腱为参照）<br>"
    f"{red('④ 正常')}：浅层高回声纤维状、边界连续；深层和后部回声偏低属正常<br>"
    f"{red('⑤ 异常')}：低回声增厚、纤维中断、钙化、变薄，应力下不稳；能量多普勒看充血<br>"
    f"★ {red('技巧')}：对比健侧、加应力动态观察；复杂病例仍需 MRI"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Manske RC, Wolfe C, Page P, Voight M. Diagnostic Musculoskeletal Ultrasound in the Evaluation of the Deltoid Ligament of the Ankle. "
    "Int J Sports Phys Ther. 2025;20(4):641-647. PMCID: PMC11964700.</em><br>"
    "文中 7 张图片均来自原文：图 2D、3D、4D、7A 解剖标注已改为中文；表格为编者整理，仅用于学术交流。"
))

TITLE = "「踝关节」三角韧带伤了没？肌骨超声 3 个切面看清楚"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>三角韧带超声推文</title>
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
<div class="by">原创 · 悦美力</div>
""" + BODY + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
