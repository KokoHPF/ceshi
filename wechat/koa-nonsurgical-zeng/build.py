#!/usr/bin/env python3
"""曾文欣、万丽 2026 膝骨关节炎非手术治疗进展推文：生成 article_body.html 与 preview.html。

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
A.append(cap("原文首页（中华疼痛学杂志 2026 年第 22 卷第 1 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('题目')}：膝骨关节炎非手术治疗进展",
    f"{b('作者')}：曾文欣 · 万丽（通信作者）",
    f"{b('机构')}：广州医科大学附属第二医院疼痛科",
    f"{b('期刊')}：中华疼痛学杂志",
    f"{b('年卷期')}：2026;22(1):134-141",
    f"{b('DOI')}：10.3760/cma.j.cn101658-20250902-00151",
    f"{b('文章类型')}：综述",
    f"{b('关键词')}：骨关节炎，膝；注射，关节内；富含血小板的血浆；非手术治疗；疾病修饰性药物",
], square=True))

A.append(h2("🎯 背景：尚无药物能逆转病程，非手术治疗是主角"))
A.append(p(
    f"膝骨关节炎（KOA）是一种与年龄相关的退行性关节疾病，全球患病率高且持续上升；在我国，KOA 发病率高于髋关节炎，{b('以老年女性为主')}。"
    f"治疗遵循{b('阶梯化、个体化')}原则，非手术治疗安全经济，占据重要地位。但目前{red('尚无药物能预防或减缓疾病进展')}，疾病修饰性骨关节炎药物（DMOADs）成为研究热点。"
))
A.append(p(f"本文由疼痛科医生撰写，系统梳理了 KOA 的{hl('体重管理、运动康复、中医疗法、药物、关节腔注射和微创介入')}等非手术治疗手段。"))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["治疗", "要点"],
    [
        ["体重管理", "体重增加往往提示病情恶化；适当减重可减少疾病进展和功能恶化"],
        ["运动康复", "有氧、肌力和平衡训练；股四头肌肌力训练最重要；八段锦、太极拳改善疼痛效果突出"],
        ["中医疗法", "推拿；针灸可持续改善疼痛和功能 3～6 个月，电针镇痛效果最好；温针、艾灸"],
        ["药物", "口服 NSAIDs 为一线；有胃肠/心血管风险者优先外用 NSAIDs；阿片类获益有限；辣椒素可替代外用 NSAIDs"],
        ["关节腔注射", "激素起效快但仅 1～6 周；透明质酸疗效有争议；PRP 6～12 个月优于透明质酸但制备不统一；干细胞仍在研究阶段"],
        ["微创介入", "膝神经射频（膝上内、上外、下内侧）缓解顽固性疼痛；腰交感神经射频属探索性；关节镜清理、关节腔灌洗"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('减重和运动（尤其股四头肌训练）是基石，药物和注射以缓解症状为主，目前还没有能真正逆转病程的药物')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、发病机制：不只是“磨损”"))
A.append(ul([
    f"KOA 是{b('累及整个关节')}的疾病，除软骨外还影响滑膜、肌腱、肌肉、韧带、软骨下骨和脂肪组织",
    f"它是关节组织修复与破坏失衡引起的{b('主动动态改变')}，而非传统认为的被动退行性或磨损性疾病",
    "主要机制：软骨降解、软骨下骨重塑、异位骨和骨赘形成、关节囊肥大、滑膜炎症",
    f"新发现：{b('细胞衰老、低度慢性炎症、新血管形成')}三者相互作用（衰老细胞诱发炎症，促血管生成因子驱动低度炎症），共同导致疼痛和结构损伤",
]))

A.append(h3("❇️二、诊断标准（中国骨关节炎诊疗指南 2024 版）"))
A.append(p(f"满足 {b('(1)')} + 其他任意 {b('2 条')}即可诊断："))
A.append(ul([
    "(1) 近 1 个月内反复膝痛",
    "(2) 年龄 ≥50 岁",
    "(3) 晨僵 <30 分钟",
    "(4) 活动时有骨擦音（感）",
    "(5) 站立或负重位 X 线片示关节间隙变窄、软骨下骨硬化或囊性变、关节边缘骨赘形成",
]))

A.append(h3("❇️三、体重管理与运动康复"))
A.append(ul([
    f"高体重指数人群增加使 KOA 病例增加约 {b('20%')}；系统回顾显示体重增加往往提示病情恶化，{b('适当减重')}可减少疾病进展和功能恶化",
    f"《中国膝骨关节炎非手术治疗专家共识（2023 版）》推荐{b('有氧运动、肌力训练和平衡训练')}",
    f"{b('股四头肌肌力训练最为重要')}：增强膝关节稳定性，促进滑液循环，改善软骨营养",
    "《中国膝骨关节炎康复治疗指南（2023 版）》建议日常平地行走的活动强度应达到世界卫生组织推荐的健康有益水平",
    f"{b('中医练功')}：易筋经、太极拳、八段锦、五禽戏均能改善情绪和生活质量；网状荟萃分析中，八段锦改善僵硬和身体功能最好，{b('八段锦和太极拳')}改善疼痛最佳",
]))

A.append(h3("❇️四、中医疗法"))
A.append(ul([
    "KOA 属中医“骨痹”，病机为气滞血瘀、经脉不通，治疗重在温经散寒、行气活血、通络止痛",
    "中药：辨证论治，内服方剂或中成药，或熏洗、敷贴、离子导入外治",
    f"{b('推拿')}：点按、拿捏等手法改善肌张力和柔韧性、促进血液循环，缓解疼痛和僵硬",
    f"{b('针灸')}：降低环氧合酶 2、前列腺素 E2，抑制 IL-1β、IL-6、TNF-α，可在治疗结束后 {b('3～6 个月')}持续改善疼痛和功能，安全性好；不同针灸技术都有效，{b('电针镇痛效果最好')}，比普通针刺更能降低 TNF-α",
    f"{b('温针')}适用于寒湿痹阻证（疼痛重着，遇冷加剧，得温则减）；{b('艾灸')}可能通过调节 NF-κB 通路、抑制炎症发挥作用",
]))

A.append(h3("❇️五、药物治疗（以缓解症状为主）"))
A.append(ul([
    f"{b('NSAIDs')}：口服是常用方法，长期使用需关注胃肠道和心血管风险；有风险者，OARSI 强烈推荐优先{b('外用 NSAIDs')}（双氯芬酸凝胶、布洛芬乳膏、氟比洛芬贴剂等）；微针经皮给药正在探索",
    f"{b('阿片类')}：对疼痛和功能的改善临床意义有限，剂量越大不良反应越多；仅在常规治疗无效时使用，老年人和免疫力低下者慎用",
    f"{b('辣椒素')}：TRPV1 受体激动剂，使伤害感受器“去功能化”；可减轻疼痛长达 3 个月，疗效与外用 NSAIDs 相当，可能有局部烧灼感",
]))

A.append(h3("❇️六、关节腔内注射"))
A.append(p(f"关节腔注射可提高局部生物利用度、减少不良事件，但{red('注射本身的安慰剂效应可能强于外用或口服给药')}，评价真实疗效需要设计严谨的随机对照试验。"))
A.append(pic(2, "表1 重绘：各指南对膝关节腔内常用注射剂的推荐意见（按原文表 1 数据中文重绘）"))
A.append(ul([
    f"{b('皮质类固醇')}：抑制炎症级联反应，减少急性疼痛发作；疗效多在 {b('1～6 周')}内明显，长期获益不明确",
    f"{b('透明质酸')}：补充滑液中降解的透明质酸；部分指南仍推荐，但高质量荟萃分析显示与安慰剂相比效应量{b('接近零')}，疗效有争议",
    f"{b('富血小板血浆（PRP）')}：生长因子促进软骨修复、抗炎；欧洲 ESSKA 共识认为可作为一线注射选择；多项研究显示 {b('6～12 个月')}的疼痛和功能改善优于透明质酸。少白细胞 PRP 可能更有优势，高浓度 PRP（如 1000×10⁹/L）促进软骨细胞增殖。但部分大样本 RCT（如 RESTORE 试验）显示 PRP 与安慰剂差异无统计学意义——{b('制备工艺和注射方案亟需标准化')}",
    f"{b('联合注射')}：激素 + 透明质酸在 2～52 周的疼痛缓解优于单用透明质酸，但中重度患者与单用激素无差异，长期疗效都不佳；PRP + 透明质酸的结论不一致",
    f"{b('间充质干细胞')}：一项脂肪源性干细胞 RCT 中，12 个月时疼痛评分从约 6.7 降到 2.6，并延缓 MRI 上的进展；但仍处于临床研究阶段，{b('暂不推荐常规应用')}",
    f"{b('臭氧')}：改善疼痛和功能，4、12 周时与激素相当，20 和 40 μg/ml 浓度疗效无差异，但不如 PRP",
    f"{b('新方向')}：铁螯合剂去铁胺（抑制软骨细胞铁死亡）、缓释特立帕肽水凝胶（促进软骨再生）——目前均为基础或早期研究",
]))

A.append(h3("❇️七、微创介入"))
A.append(ul([
    f"{b('射频')}：连续射频（高温不可逆阻断痛觉信号）和脉冲射频（短脉冲，不造成神经结构损伤）",
    f"{b('膝神经射频')}：仅处理{b('膝上内侧、膝上外侧和膝下内侧神经')}即可减轻疼痛；隐神经连续或脉冲射频也有效",
    f"{b('腰交感神经射频')}：基于“腰膝同治”理念，可能改善膝关节血供并影响疼痛传导，但{red('缺乏高级别证据，属探索性治疗')}",
    "关节镜可诊断并清理病变组织，但对严重磨损的软骨无效；关节腔灌洗可清除炎症介质和碎屑，灌洗后再注射效果更好",
]))

A.append(h3("❇️八、总结与展望"))
A.append(ul([
    "基础治疗以体重管理和运动康复为基石，运动以股四头肌训练为主，辅以八段锦、太极拳",
    "药物：口服 NSAIDs 一线，有风险者用外用 NSAIDs，辣椒素可作替代",
    "注射：激素快而短，透明质酸有争议，PRP 中长期优于透明质酸但需标准化，臭氧可作补充，干细胞暂不常规使用",
    "未来方向：开发真正能延缓或逆转病程的 DMOADs；标准化 PRP 等生物制剂；开展大样本、长期随访的高质量 RCT",
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('文章性质')}：叙述性综述。摘要称“系统综述”，但没有交代检索策略、纳入标准和质量评价，不属于方法学意义上的系统综述",
    f"{b('亮点')}：覆盖面广，把中西医、药物、注射和介入放在一起比较，并用表格汇总了中外 5 部指南对关节腔注射的推荐，实用性强",
    f"{b('运动康复篇幅偏少')}：作为指南公认的核心治疗，文中只用了一段，没有给出运动类型、强度、频次等具体处方；“股四头肌训练最为重要”引用的是 2003 年的一项小样本研究",
    f"{b('引用与表述有出入')}：透明质酸“高质量荟萃分析显示效应量接近零”引用的是美国风湿病学会指南；“PRP 优于臭氧”引用的是一篇文献可视化（计量学）分析；皮质类固醇段把长效混悬剂归入“即释类固醇”，前后矛盾",
    f"{b('表与正文不一致')}：表 1 显示中国指南（2024）对间充质干细胞为“弱推荐”，而正文结论写“暂不推荐常规应用”",
    f"{b('证据等级混杂')}：去铁胺、特立帕肽水凝胶等仍是动物或早期研究，与临床疗法并列介绍，阅读时需区分",
]))

A.append(h2("📌 总结：膝骨关节炎非手术治疗怎么选"))
A.append(p(
    f"{red('① 基石')}：减重 + 运动，股四头肌训练为核心，可加八段锦、太极拳<br>"
    f"{red('② 药物')}：外用 NSAIDs 优先（尤其有胃肠/心血管风险者），口服 NSAIDs 短期用，阿片类尽量少用<br>"
    f"{red('③ 注射')}：激素快但只管 1～6 周；透明质酸有争议；PRP 中长期优于透明质酸但需标准化；干细胞暂不常规<br>"
    f"{red('④ 中医')}：针灸（尤其电针）、推拿可作为补充<br>"
    f"{red('⑤ 介入')}：顽固性疼痛可考虑膝神经射频<br>"
    f"★ {red('注意')}：注射的安慰剂效应很强；目前还没有能逆转病程的药物"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>曾文欣, 万丽. 膝骨关节炎非手术治疗进展[J]. 中华疼痛学杂志, 2026, 22(1): 134-141. DOI: 10.3760/cma.j.cn101658-20250902-00151.</em><br>"
    "原文无插图；首页为原文截图，表 1 按原文数据重绘，其余表格为编者整理，仅用于学术交流。原文版权归中华医学会所有。"
))

TITLE = "「膝关节」膝骨关节炎非手术治疗进展：减重、运动、药物、注射怎么选？"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>膝骨关节炎非手术治疗推文</title>
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
