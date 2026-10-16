#!/usr/bin/env python3
"""Manske 2026 膝关节半月板肌骨超声推文：生成 article_body.html 与 preview.html。

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


def tcap(t):
    return f'<p style="margin:0 0 8px;font-size:14px;line-height:1.6;color:#000;font-weight:bold;">{t}</p>'


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2026 年第 21 卷第 1 期，“肌骨超声小贴士”栏目）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Diagnostic Musculoskeletal Ultrasound in the Evaluation of the Knee Menisci（诊断性肌骨超声评估膝关节半月板）",
    f"{b('作者')}：Robert C. Manske, PT, DPT · Chris Wolfe, PT, DPT · Phil Page, PT, PhD · Michael Voight, PT, DHSc",
    f"{b('栏目')}：MSK Ultrasound Bites: Tips and Tricks（肌骨超声小贴士）",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2026;21(1):108-114",
    f"{b('PMCID')}：PMC12758935",
    f"{b('证据级别')}：5 级",
    f"{b('关键词')}：musculoskeletal ultrasound · knee · meniscus · rehabilitation · dynamic imaging",
], square=True))

A.append(h2("🎯 背景：半月板损伤常见，单靠查体容易误诊"))
A.append(p(
    f"半月板是位于股骨和胫骨之间的两块{b('楔形纤维软骨盘')}（内侧、外侧），帮助传递压缩、剪切和旋转负荷，并参与关节润滑和营养分布。"
    f"胫骨平台表面较浅，半月板把它变成更深的凹面来容纳股骨髁——{b('外侧尤其重要')}，因为外侧胫骨平台更平，甚至略凸。"
))
A.append(p(
    f"半月板撕裂会削弱膝关节的减震能力、增加关节机械应力，长期可能促进关节退变。"
    f"{b('急性撕裂')}多见于需要转身、切步的运动，常合并前交叉韧带、内侧副韧带损伤；{b('年龄较大者')}更多是退变性撕裂，从地上站起来、蹲下种花这类简单动作就可能撕裂。"
    f"急性半月板损伤{red('单靠查体常常难以确诊，误诊多见')}。"
))
A.append(p(f"诊断性肌骨超声（MSKUS）{hl('便携、实时、便宜')}，在康复和运动医学中越来越常用。本文介绍用超声评估内、外侧半月板的解剖、常见损伤、扫查技术和对康复的意义。"))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["项目", "要点"],
    [
        ["探头", "高频线阵探头（半月板外缘位置表浅）"],
        ["体位", "仰卧，膝下垫小枕屈膝约 20°～30°：外侧半月板小腿内旋，内侧半月板小腿外旋"],
        ["切面", "沿关节线长轴（LAX）放置，从前向后扫查前角、体部、后角"],
        ["正常表现", "股骨与胫骨（高回声骨面）之间、边界清楚、回声均匀的三角形结构"],
        ["撕裂征象", "低回声/无回声裂隙、轮廓不规则或截断、半月板突出（超出胫骨缘）、关节线积液、半月板旁囊肿"],
        ["动态评估", "内翻/外翻应力、屈伸活动、负重与非负重下观察"],
        ["主要局限", "依赖操作者；只能看清外周缘，深部撕裂可能漏诊；MRI 仍是参考标准"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('超声看半月板外周缘快、便宜、可动态，适合作为一线工具；看不清深部时仍需 MRI')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、超声评估半月板的优势"))
A.append(ul([
    f"{b('无创')}：即时超声可用于半月板等多种膝关节软组织病变",
    f"{b('实时、动态')}：可在{b('负重和非负重')}下观察内、外侧半月板，可以边加载、边在可用活动范围内活动膝关节，动态看到半月板移位",
    f"{b('分辨率高')}：能清楚显示沿胫股关节线分布的内、外侧半月板外缘",
    f"{b('准确性')}：超声诊断半月板撕裂的敏感度和特异度最高可达 {b('88%')} 和 {b('85%')}；内侧半月板撕裂的敏感度为 {b('83%～97.2%')}，特异度为 {b('83%～100%')}",
    f"{b('可及、省钱')}：便携、普及，比 MRI 便宜",
]))

A.append(h3("❇️二、局限性"))
A.append(ul([
    f"{b('依赖操作者')}：判读需要技术和经验，也受设备条件影响",
    f"{b('深度受限')}：外周缘通常看得清，{red('深部结构看不清')}——深部撕裂可能漏诊，而它们有时更有临床意义、症状更明显",
    f"{b('伪像和声影')}：骨和钙化会产生伪像，需要调整探头位置和频率",
]))

A.append(h3("❇️三、扫查技术：体位与探头放置"))
A.append(p(f"患者仰卧，膝下垫小枕，屈膝约 {b('20°～30°')}。这个体位放松股四头肌、打开关节间隙，为内、外侧半月板提供良好的声窗。"))
A.append(ul([
    f"{b('外侧半月板')}（图 1A、1C）：小腿{b('内旋')}暴露外侧关节线；先摸到{b('腓骨头')}，探头长轴放在其正上方，再向前移，直到在{b('外侧副韧带深面、腘肌腱旁')}看到外侧半月板。外侧半月板位置更深、弧度更大，需要轻微地{b('前后翘动探头（足跟-足尖摆动）')}减少各向异性、看清软骨-骨界面",
    f"{b('内侧半月板')}（图 1B、1D）：足和小腿{b('外旋')}暴露内侧关节线；从膝内侧后方开始，长轴沿内侧关节线放置，向前轻扫，直到在{b('内侧副韧带（MCL）深面')}看到三角形的纤维软骨楔；MCL 位于半月板体部浅层，常需轻微倾斜探头",
    f"{b('动态评估')}：轻施{b('外翻应力')}更好地显示内侧半月板，{b('内翻应力')}打开外侧关节线；也可做屈伸活动",
]))
A.append(pic(2, "图1：体位与探头放置。1A 外侧半月板，小腿内旋；1B 内侧半月板，足和小腿外旋（黑框示探头位置）；1C 外侧半月板，探头置于腓骨头上方，长轴放置；1D 内侧半月板，探头沿内侧关节线长轴放置"))

A.append(h3("❇️四、正常长轴声像图"))
A.append(ul([
    f"完整扫查要从前向后系统移动探头，依次看{b('前角、体部、后角')}；全程轻轻摆动探头，避免各向异性造成貌似病变的{b('假性低回声区')}",
    f"注意半月板和周围韧带的关系：内侧看{b('MCL')}，外侧看{b('外侧副韧带-腘肌腱界面')}",
    f"借助邻近软组织定位：内侧有{b('鹅足和半膜肌腱')}，外侧有{b('股二头肌和髂胫束')}；外侧血管结构较少，不容易把血管搏动误当成半月板病变",
    f"{b('外侧半月板')}：呈三角形，但通常比内侧{b('更深、更弯')}，位于外侧副韧带和腘肌腱深面，需要仔细调整角度；轻施内翻应力可见其活动度比内侧大",
    f"{b('内侧半月板')}：位于股骨内髁和胫骨平台之间，{b('回声均匀、中等偏高回声的三角形')}，上下缘光滑清楚",
]))
A.append(pic(3, "图2：外侧半月板长轴切面。2A 原始超声图；2B 标注图：浅层依次为皮下组织、脂肪、股二头肌腱和外侧副韧带，深面可见股骨、半月板、胫骨和腓骨头（解剖标注已改为中文）"))
A.append(pic(4, "图3：内侧半月板长轴切面。3A 原始超声图；3B 标注图：内侧副韧带深面，股骨髁与胫骨之间的三角形结构即内侧半月板（解剖标注已改为中文）"))

A.append(h3("❇️五、病理表现"))
A.append(h4("🔻撕裂的一般征象"))
A.append(ul([
    f"正常均匀的楔形结构被破坏，最常见的是纤维软骨内{b('局灶性低回声或无回声裂隙')}",
    f"随探头方向和扫查平面不同，可识别{b('垂直、水平、瓣状或放射状')}撕裂",
    f"以下附加征象能提高诊断信心：{b('半月板表面不规则或截断')}、{b('半月板突出超出胫骨边缘')}、{b('低回声裂隙延伸到关节面')}、关节线积液或滑膜增厚",
    f"{b('半月板旁囊肿')}：与撕裂相连的充液囊性肿物，多见于内侧，源自退变性撕裂，可表现为关节线处的软组织肿胀；超声上常为紧贴半月板体部的{b('薄壁无回声囊肿')}，有时可见液性裂隙从囊肿延伸到撕裂处",
]))
A.append(h4("🔻内侧半月板撕裂"))
A.append(p(
    f"内侧半月板位置浅、与关节囊和 MCL 连接牢固，撕裂{b('通常更容易显示')}：三角形轮廓消失、体部出现低回声/无回声裂隙（图 4A），以及超出胫骨内侧缘的突出（图 4B）。"
    f"关节线积液、关节囊增厚或邻近 MCL 受累也常见，尤其是退变性或慢性病例。"
))
A.append(pic(5, "图4：内侧半月板撕裂。4A 黄色箭头示半月板体内的低回声裂隙；4B 黄色箭头示撕裂处，半月板向胫骨内侧缘外突出（超声机英文注记已去除）"))
A.append(h4("🔻外侧半月板撕裂"))
A.append(p(
    f"外侧半月板位置更深，上面还有外侧副韧带和腘肌腱，撕裂在超声上{b('可能更隐蔽')}：表现为低回声缺损、边缘不规则或三角形楔形结构变形。"
    f"其他征象包括半月板与腘肌腱的接触异常、关节线旁的小移位碎片或游离体，以及常与外侧撕裂相关的{b('半月板旁囊肿')}。"
    f"关节线积液可以勾勒出撕裂平面；轻施内翻或外翻应力能突出半月板突出或显示撕裂部分的不稳定。"
))
A.append(pic(6, "图5：外侧半月板撕裂。5A、5B 黄色箭头示外侧半月板撕裂处（超声机英文注记已去除）"))

A.append(h3("❇️六、对康复人员的意义"))
A.append(ul([
    f"{b('早期发现、准确分级')}：快速区分半月板撕裂、积液或半月板突出，指导治疗计划",
    f"{b('动态功能测试')}：在负重活动或非负重活动范围内观察功能动作对半月板的影响",
    f"{b('引导介入')}：超声引导下精准注射（如糖皮质激素抗炎）",
    f"{b('患者教育')}：实时图像直观解释损伤，帮助患者建立合理的恢复预期",
]))
A.append(p(f"由于深部结构显示有限，{b('MRI 仍可能是首选影像')}；但超声能很快、低成本地评估半月板，很多情况下能看到病变，可作为急性和慢性情况下的{hl('一线工具')}，也可用于监测愈合和康复进展。"))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('证据级别低')}：5 级、简短的技术栏目文章，没有原始数据；文中的诊断准确性数字只引用了文献，未说明研究人群、参考标准和撕裂类型",
    f"{b('亮点')}：体位、探头放置、正常解剖标志和撕裂征象一目了然，配有标注图，适合康复人员入门",
    f"{b('体位描述前后不一致')}：前文“检查方案”写外侧半月板为{b('侧卧、双膝间垫枕施加内翻应力、探头放在腘窝横纹处（后外侧）')}，内侧半月板探头放在后内侧；后文图 1 部分则写{b('仰卧屈膝 20°～30°、小腿内旋、探头放在腓骨头上方')}——两种方法都可用，但原文没有说明怎样取舍",
    f"{b('图文对应不足')}：小节标题写“撕裂与囊肿形成”，但图 4、图 5 没有展示囊肿；图 5A、5B 没有单独的图注说明各自显示什么；图 2 标注里没有标出正文强调的腘肌腱",
    f"{b('“提高诊断准确性”的说法需谨慎')}：作者也承认超声看不清深部撕裂、MRI 仍是参考标准，超声更适合作为补充和筛查",
    f"{b('小瑕疵')}：“sports that involves”应为 involve；外侧体位一句“opens with the posterolateral joint line”语法不通",
]))

A.append(h2("📌 总结：超声看半月板，记住这几点"))
A.append(p(
    f"{red('① 探头')}：高频线阵，沿关节线长轴放置<br>"
    f"{red('② 体位')}：仰卧屈膝 20°～30°；看外侧小腿内旋、看内侧小腿外旋<br>"
    f"{red('③ 定位')}：外侧从腓骨头上方找，在外侧副韧带、腘肌腱深面；内侧在 MCL 深面<br>"
    f"{red('④ 正常')}：股骨、胫骨之间回声均匀的三角形；前角、体部、后角都要扫到<br>"
    f"{red('⑤ 异常')}：低/无回声裂隙、轮廓截断、突出超出胫骨缘、积液、半月板旁囊肿<br>"
    f"{red('⑥ 技巧')}：摆动探头避开各向异性；加内翻/外翻应力动态观察<br>"
    f"★ {red('局限')}：只看得清外周缘，深部撕裂仍需 MRI"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Manske RC, Wolfe C, Page P, Voight M. Diagnostic Musculoskeletal Ultrasound in the Evaluation of the Knee Menisci. "
    "Int J Sports Phys Ther. 2026;21(1):108-114. PMCID: PMC12758935.</em><br>"
    "文中 5 张图片均来自原文：图 2B、3B 解剖标注已改为中文，图 4A、5A 超声机英文注记已去除；核心要点表为编者整理，仅用于学术交流。"
))

TITLE = "「膝关节」半月板损伤怎么用超声看？体位、探头与撕裂征象"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>半月板超声推文</title>
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
