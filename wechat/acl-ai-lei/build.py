#!/usr/bin/env python3
"""人工智能在 ACL 损伤诊治中的应用综述推文：生成 article_body.html 与 preview.html。

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
A.append(cap("原文首页（中华医学杂志 2026 年第 106 卷第 1 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('题目')}：人工智能在前交叉韧带损伤诊治中应用的研究进展",
    f"{b('作者')}：雷蕾 · 陈德生（通信作者）· 勾禹 · 王同富 · 朱佳旺 · 郭新静",
    f"{b('机构')}：天津大学医学院；天津大学天津医院运动医学与关节镜一科；天津中医药大学中西医结合学院",
    f"{b('期刊')}：中华医学杂志",
    f"{b('年卷期')}：2026;106(1):92-96",
    f"{b('DOI')}：10.3760/cma.j.cn112137-20250725-01849",
    f"{b('文章类型')}：综述（引用文献 37 篇）",
    f"{b('关键词')}：前交叉韧带；前交叉韧带损伤；人工智能；神经网络；计算机视觉；运动医学",
], square=True))

A.append(h2("🎯 背景：AI 进入运动医学"))
A.append(p(
    f"前交叉韧带（ACL）损伤是膝关节最常见的损伤类型，约 {b('80%')} 发生在急停、变向、跳跃落地等运动场景。"
    f"近年来，人工智能（AI）被引入骨科和运动医学，在{hl('术前诊断、风险预测、术中导航和术后康复')}中都有尝试。"
))
A.append(p("本文按“术前 → 术中 → 术后”的顺序，梳理了 AI 工具在 ACL 损伤围手术期的应用和评价。"))

A.append(h2("🔴 核心要点"))
A.append(pic(2, "全文框架示意：常用 AI 工具与围手术期应用（按原文内容自绘）"))
A.append(table(
    ["阶段", "AI 应用", "目前证据"],
    [
        ["术前", "损伤风险预测；MRI 自动识别和分级 ACL 撕裂", "诊断准确度与放射科医师相近；风险模型处于起步阶段，缺乏大规模验证"],
        ["术中", "计算机导航辅助骨隧道定位", "隧道定位更准，但术后功能评分和临床结局与传统手术无差异"],
        ["术后", "阿片类药物剂量与神经阻滞需求预测；AI 支具远程康复", "多为单项研究，远程 AI 康复短期评分更好"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('AI 读 MRI 已接近放射科医师水平，导航能让隧道打得更准，但“更准”还没有转化为更好的临床结局')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、常用 AI 工具：先分清几个名词"))
A.append(ul([
    f"{b('机器学习（ML）')}：AI 的核心分支，让计算机从数据中学习、改进，对新数据做出预测；包括监督、无监督、半监督和强化学习",
    f"{b('深度学习（DL）')}：ML 的子领域，用{b('多层神经网络')}模拟人脑神经元，自主提取特征",
    f"{b('卷积神经网络（CNN）')}：DL 的一种，由卷积层（提取特征）、池化层（减少数据量）、全连接层（做决策）组成，{b('特别适合图像识别')}",
    f"{b('计算机视觉（CV）')}：让计算机“看”——识别、跟踪、测量目标；术中导航就是结合 CV 根据影像定位手术目标",
]))

A.append(h3("❇️二、术前①：损伤风险预测"))
A.append(ul([
    "基于预训练 CNN 分析 3D 膝关节运动，监测运动员负荷和膝关节损伤风险，表现出高敏感性",
    f"用 ML 分析{b('膝关节形态学特征')}构建原发性 ACL 损伤预测模型，预测准确率超过 90%",
    "用惯性传感器和光电设备评估跳跃后的腿部稳定性和负荷吸收能力，落地错误评分与 ACL 损伤风险正相关",
    f"{red('作者结论')}：有一定可行性，但仍处于起步阶段，{b('缺乏公认的成熟模型和大规模临床验证')}",
]))

A.append(h3("❇️三、术前②：MRI 辅助诊断"))
A.append(p("MRI 是诊断 ACL 损伤的影像学金标准，结合前抽屉、拉赫曼、轴移等查体综合判断。AI 主要用于自动读片："))
A.append(table(
    ["研究", "模型", "AI 表现", "对照"],
    [
        ["Bien 2018（MRNet）", "CNN，识别完整与撕裂 ACL", "灵敏度 76%，特异度 97%", "放射科医师借助 AI 后诊断表现提升"],
        ["Liu 2019", "全自动 CNN，以关节镜为金标准", "全层撕裂灵敏度、特异度均 96%，AUC 0.98", "放射科医师 96%～98%，无显著差异"],
        ["Zhang 2020", "定制 CNN，多序列 MRI", "灵敏度、特异度、准确度均 96%", "高级放射科医师灵敏度 96%、特异度 86%，无显著差异"],
        ["Namiri 2020", "多类别 CNN：完整、部分撕裂、全层撕裂、移植物", "完整 ACL 灵敏度 89%～93%；全层撕裂 76%～82%；移植物 97%～100%", "未与放射科医师比较"],
    ],
))
A.append(ul([
    f"趋势：从早期的“完整 vs 撕裂”二分类，发展到{b('多类别分级')}，以及自动识别撕裂的解剖部位",
    "国内研究用无监督 ML 分析 ACL 断裂患者的临床特征，识别潜在亚群和合并损伤规律",
    f"作者认为 AI 模型“具有替代医师完成 ACL 损伤诊断工作的潜力”——这一表述{red('偏乐观')}，见证据评价",
]))

A.append(h3("❇️四、术中：导航辅助骨隧道定位"))
A.append(p(f"骨隧道位置是 ACL 重建的关键：胫骨隧道{b('太靠前')}增加移植物撞击风险，{b('太靠后')}增加旋转不稳。"))
A.append(ul([
    "回顾性队列：两组胫骨隧道无差异，导航组股骨隧道更垂直于 Blumensaat 线",
    "首例基于 CT 的导航 ACL 重建：用皮肤参考点配准，精度在 1 mm 以内",
    "前瞻性随机对照：导航组胫骨隧道更接近理想位置，移植物撞击更少",
    f"另一项 100 例随机对照：{b('两组定位准确性无差异')}，可能与术者经验丰富有关",
    f"荟萃分析：导航组隧道定位更精确，但{red('术后功能评分和临床结局无差异')}",
    "其他用途：保留 ACL 残端时辅助定位；比较前内侧入路与经胫骨隧道、单束与双束重建等",
]))
A.append(p(f"{b('启示')}：导航可能对{b('经验不足的术者')}更有帮助，术者经验仍是不可忽视的因素。"))

A.append(h3("❇️五、术后：疼痛管理与康复"))
A.append(ul([
    f"{b('阿片类药物')}：用 ML 建模预测理想剂量，防止过量使用",
    f"{b('股神经阻滞')}：ML 可预测 ACL 术后是否需要股神经阻滞",
    f"{b('冷疗')}：计算机模拟 + ML 实时预测冷疗时的膝关节内温度，误差约 0.1 ℃",
    f"{b('AI 支具远程康复')}：内置康复指导的便携式传感器支具，居家远程康复组的 IKDC 和 KOOS 评分高于院内康复组，1 年时 Tegner 活动评分也更高",
    f"{red('注意')}：远程 AI 康复不适合所有患者，有些情况仍需当面评估和手法治疗",
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('文章性质')}：叙述性综述，未交代检索策略和纳入标准，没有图表汇总，篇幅较短（正文约 3 页）",
    f"{b('“导航”是否等于 AI')}：文中引用的导航研究（2007、2011、2012 年等）大多是传统的计算机辅助导航，并不涉及机器学习，把它们归入 AI 应用概念上有些宽泛",
    f"{b('MRNet 数据疑似写反')}：原研究报告的是 AI 辅助{b('提高了放射科医师识别 ACL 撕裂的特异度')}，本文写成“灵敏度提高 5%、特异度不变”，并据此得出“提高诊断敏感度”的结论",
    f"{b('结论偏乐观')}：多数诊断模型是单中心、回顾性数据，缺少外部验证和前瞻性研究；“具有替代医师的潜力”的说法证据不足。文中也未讨论数据偏倚、可解释性、伦理和监管等问题",
    f"{b('多处引用与论点不对应')}：CNN 结构引用的是一篇导航荟萃分析；ML 定义引用的是一篇胫骨平台后倾的尸体研究；“查体联合影像高灵敏度”引用的是胫骨后倾病例系列；“保留残端促进恢复”引用的是导航翻修研究；阿片类剂量模型引用的是一篇阿片危机大数据综述；“远程 AI 康复有效”引用的是一篇手机平台满意度调查",
    f"{b('“扩大样本、延长随访”')}：引用的 Yavari 2023 是荟萃分析，并非一项扩大样本的原始研究",
    f"{b('缺少康复视角')}：术后康复部分只有一项 AI 支具研究，未涉及动作捕捉、可穿戴传感器评估重返运动等康复领域更常见的 AI 应用",
]))

A.append(h2("📌 总结：康复人怎么看 AI 与 ACL"))
A.append(p(
    f"{red('① 诊断')}：AI 读 MRI 已接近放射科医师，可作为辅助，但不能替代查体和临床判断<br>"
    f"{red('② 风险预测')}：模型仍在起步阶段，暂不能用于筛查运动员<br>"
    f"{red('③ 术中导航')}：隧道定位更准，但临床结局与传统手术无差异<br>"
    f"{red('④ 术后康复')}：AI 支具和远程康复有初步效果，适合作为补充，不能取代当面评估<br>"
    f"★ {red('注意')}：目前证据多为单中心、小样本研究，需要外部验证和长期随访"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>雷蕾, 陈德生, 勾禹, 等. 人工智能在前交叉韧带损伤诊治中应用的研究进展[J]. 中华医学杂志, 2026, 106(1): 92-96. DOI: 10.3760/cma.j.cn112137-20250725-01849.</em><br>"
    "原文无插图；首页为原文截图，框架示意图和表格为编者按原文内容整理绘制，仅用于学术交流。原文版权归中华医学会所有。"
))

TITLE = "「膝关节」AI 能看懂 ACL 损伤吗？从 MRI 诊断、术中导航到远程康复"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>AI与ACL损伤推文</title>
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
