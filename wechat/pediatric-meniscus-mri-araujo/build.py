#!/usr/bin/env python3
"""Araújo 等 2024《儿童半月板：正常表现、解剖变异、损伤、撕裂及术后影像》（Insights into Imaging）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
配图：python3 tools/fig1_zh.py src/fig1.png src/fig1_zh.png <中文字体>
      python3 tools/make_figs.py src images <中文字体>
（原文 © The Author(s) 2024，CC BY 4.0：图 1 英文标注原位汉化，其余 MRI 原样引用加中文图注）
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
                'vertical-align:middle;">', 'vertical-align:middle;white-space:nowrap;">' if i == 0 and len(c) <= 7 else 'vertical-align:middle;">', 1)
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






# ---------- 正文 ----------
def cap(t):
    return f'<p style="margin:0 0 20px;font-size:12px;line-height:1.6;color:#888;">🔖{t}</p>'


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
    "Araújo FF, Guimarães JB, da Cruz IAN, Morimoto LdR, Ormond Filho AG, Nico MAC. Pediatric menisci: normal aspects, "
    "anatomical variants, lesions, tears, and postsurgical findings. Insights Imaging. 2024;15:295. doi:10.1186/s13244-024-01867-6",
    "中文题目：儿童半月板：正常表现、解剖变异、损伤、撕裂及术后影像",
    "作者单位：巴西圣保罗 Fleury 医学与健康集团（Higienópolis），肌骨放射科",
    f"文章类型：{b('教育性综述')}（以 MRI 读片为主线，配 12 幅病例图）",
], square=True))

A.append(h2("先说为什么要读这篇"))
A.append(p(
    "孩子运动越来越多，MRI 也越来越普及，儿童半月板撕裂的报告数量一直在涨，"
    f"原文引用的数据是{b('每 10 万名运动员 5.1 例')}。在骨骼未成熟的膝关节里，半月板损伤和前交叉韧带损伤一样，是最常见的关节内紊乱之一。"
))
A.append(p(
    f"问题在于：{mk('儿童半月板不是缩小版的成人半月板')}。血供更好，MRI 上本来就有“看起来像撕裂”的高信号；"
    "盘状半月板这类变异主要在儿童阶段出现症状；撕裂的部位和类型也跟成人不一样。"
    "照搬成人的读片标准，容易漏诊，也容易过度诊断。"
))
A.append(p(
    "这篇综述由放射科医生写给放射科医生，但对康复治疗师同样有用：孩子出现“伸不直”“深蹲卡住”“膝外侧弹响”时，"
    "知道背后可能是什么、MRI 报告里每个词是什么意思，转诊和沟通都会更有底。"
))

A.append(h2("一、解剖：内外侧半月板差在哪"))
A.append(ul([
    f"{b('内侧半月板')}：C 形，和关节囊贴得紧；半月板胫骨韧带（冠状韧带）在内侧更厚更强",
    f"{b('外侧半月板')}：几乎是正圆，更小，关节囊附着少，腘肌腱裂孔处没有半月板胫骨韧带，所以{b('天生更活动')}",
    f"{b('外侧半月板的额外附着')}：板股韧带（板股前韧带即 Humphrey 韧带，走在后交叉韧带前方；板股后韧带即 Wrisberg 韧带，走在后方）、"
    "腘肌—半月板束（前下、后上、后下三束）和半月板腓骨韧带",
    "板股韧带在屈膝时把外侧半月板后角往前内牵，屈膝 15°～90° 时还帮忙对抗胫骨后移，后交叉韧带断了的膝关节里更明显",
    "腘肌—半月板束损伤会导致外侧半月板过度活动和半脱位，常和前交叉韧带、后外侧角损伤同时出现",
    "儿童和成人半月板在整体形态和附着上没有明显差别，差别在组织成分随年龄的变化",
]))
A.append(img(2))

A.append(h2("二、发育与血供：儿童的“高信号”不一定是撕裂"))
A.append(p(
    "半月板在胚胎第 4 周出现，第 9 周可辨认，第 14 周已经接近成人形态。"
    f"{b('胎儿期和出生时，整个半月板都有血管')}；到 9 个月左右，内 1/3 的血管已经退化；"
    f"{b('10～12 岁以后只剩外周 10%～30% 有血管')}，和成人一样。"
))
A.append(p(
    "组织结构也在变：3 个月前以细胞为主，之后胶原逐渐增多；3 岁起胶原纤维开始沿长轴环形排列，"
    "孩子学会站立行走后环形纤维越来越多；大约 9 岁完成转变，10 岁以后的超微结构就和成人差不多了，以环形排列的 Ⅰ 型胶原为主。"
))
A.append(img(3))
A.append(p(
    f"{red('读片关键：')}儿童半月板内的高信号可能只是正常血管，越小越明显。呈线状时容易被当成撕裂，"
    f"但{b('血管信号不会接触关节面')}。这一条，是区分“正常血管”和“真撕裂”的第一道关。"
))

A.append(h2("三、盘状半月板：儿童最重要的变异"))
A.append(h4("是什么、有多常见"))
A.append(p(
    "盘状半月板是半月板形态的先天异常，看起来像一块扁平的圆盘，而不是正常的半月形。多见于外侧："
    f"{b('外侧盘状半月板发生率约 0.4%～17%，内侧约 0.06%，20% 为双侧')}。很多人没有症状，是偶然发现的，所以真实发生率并不清楚。"
))
A.append(h4("儿童的表现跟成人不一样"))
A.append(table(["", "成人", "儿童"], [
    ["常见症状", "活动痛、交锁、打软腿、典型的“弹响膝”", "伸膝受限、膝痛、关节线压痛、交锁、弹响、打软腿"],
    ["主要表现", "多与撕裂、脱离或板股后韧带缺陷有关", f"{b('伸膝受限')}是没有撕裂的盘状半月板最主要的表现，成人很少见"],
]))
A.append(p(
    "伸膝受限可能和盘状半月板在小关节腔里“占地方”有关，尤其是前部更厚：有伸膝受限的孩子，半月板前部厚度明显大于后部。"
))
A.append(h4("MRI 怎么诊断"))
A.append(ul([
    f"{b('成人传统标准')}：层厚 5 mm 的矢状位上，连续 3 层以上看到前后角相连",
    f"{b('Araki 标准')}：体部中段横径超过 14 mm，不管胫骨多宽",
    f"{b('包含儿童的新标准')}：半月板 / 胫骨宽度比 ≥ 20%，或半月板覆盖率 ≥ 75%；即使半月板已撕裂，"
    "两个指标的敏感度和特异度仍分别为 95% 和 97%（原文没有分开写两个指标各自的数值）",
]))
A.append(img(4))
A.append(p(
    "为什么盘状半月板容易撕？更厚、内部血供差，胶原纤维排列紊乱、数量少，胶原浓度低到接近退变半月板，"
    f"分散环向应力的能力下降。{b('最常见的撕裂类型是退变性水平裂（43%）')}。"
))
A.append(h4("两套分型"))
A.append(p(f"{b('Watanabe 分型')}（最常用，看形态）："))
A.append(ul([
    "Ⅰ 型完全型：盘状，中央薄，覆盖整个胫骨平台",
    "Ⅱ 型不完全型：半月形，部分覆盖胫骨平台",
    f"Ⅲ 型 Wrisberg 型：缺少正常的关节囊束和半月板胫骨韧带附着，只靠 Wrisberg 韧带连到后关节囊，{b('屈膝时容易半脱位')}，"
    "预后意义特殊。MRI 上正常束带缺失，会在半月板和关节囊之间留下 T2 高信号，看起来像周缘撕裂或束带损伤",
    "近年还提出 Ⅳ 型：环形半月板，后方胫骨附着正常",
], square=True))
A.append(img(5))
A.append(p(f"{b('Ahn MRI 分型')}（不描述撕裂类型，只看半月板往哪移）："))
A.append(table(["分型", "周缘附着", "整体移位方向"], [
    ["无移位型", "周缘没有和关节囊分开", "不移位"],
    ["前中心移位型", "后角周缘与关节囊分离", "向前 / 前中心"],
    ["后中心移位型", "前角周缘与关节囊分离", "向后 / 后中心"],
    ["中心移位型", "后外侧周缘撕裂或缺失", "向髁间窝方向"],
]))
A.append(img(6))
A.append(p("有症状、合并撕裂或不稳的盘状半月板需要治疗，所以准确诊断很重要。"))

A.append(h4("周缘不稳：术前 MRI 能提前看出来"))
A.append(p(
    f"关节镜研究里，{b('有症状的外侧盘状半月板 77% 不稳')}：前方不稳 53%，后方不稳 16%"
    "（不稳指成形术后用探钩检查，残留半月板过度活动、周缘脱离）。"
))
A.append(p(
    "移位型在 MRI 上一眼能看出，难的是“无移位型”：MRI 看着稳定，关节镜下却可能不稳。对这种情况，原文总结了几个预测征象："
))
A.append(ul([
    f"{b('预测前方不稳')}：半月板前方旁软组织水肿、前缘线状液体信号，阳性预测值、敏感度、特异度都高",
    f"{b('预测后方不稳')}：半月板边缘膨出、腘肌—半月板束缺失，敏感度高，但阳性预测值和特异度低",
    "术前判断有没有周缘不稳、在哪一侧，能帮外科医生做好手术计划",
]))
A.append(img(7))
A.append(img(8))

A.append(h2("四、其他变异"))
A.append(ul([
    f"{b('外侧半月板过度活动')}：没有撕裂、也不是盘状，但深屈膝时外侧关节线痛并交锁。多数是屈膝时外侧半月板后角异常前移，"
    f"伸膝时复位。{b('儿童多为后方关节囊附着先天不足，成人多为外伤')}。关节镜下用探钩能把它推过外侧髁或胫骨中点即可确认",
    "这类孩子首次 MRI 常常“没问题”；能复现交锁的，可以在交锁位扫描。Suganuma 的研究里，多数患者的腘肌—半月板束在 MRI 上不清楚或看不到",
    f"{b('“4 字”试验')}（LaPrade）：屈膝、内翻、外旋，可能诱发交锁。临床怀疑时，放射科要仔细看外侧半月板的关节囊附着，必要时加扫诱发体位",
    f"{b('半月板褶皱')}：屈膝时内侧半月板游离缘冗余形成的波浪状外观，见于 0.2%～0.3% 的无症状膝；"
    "以往当成变异，近期研究提示可能和内侧半月板撕裂有关，还可能被误读成半月板截断或放射状撕裂",
    f"{b('半月板小骨')}：半月板内的小骨化灶，多在内侧半月板后角，可能是胚胎变异或旧伤后遗。少见，多数没症状，"
    "也可引起机械症状或疼痛，X 线和 MRI 上容易误当成游离体或撕裂",
    "先天发育不良或缺如极其罕见",
]))
A.append(img(9))

A.append(h2("五、诊断：儿童的 MRI 准确率不如成人"))
A.append(p(
    "儿童的临床表现（关节痛、弹响、交锁）缺乏特异性，现在一般都要结合 MRI。MRI 没有辐射、能多平面成像、"
    "软组织分辨率高，大多数孩子也不用镇静。但要注意几个坑："
))
A.append(ul([
    f"{b('容易漏')}：盘状半月板撕裂漏诊率 26.7%，外侧半月板撕裂漏诊率 18.8%",
    f"{b('和关节镜比，MRI 会高估内侧、低估外侧')}：儿童半月板血供丰富，在 T2 上表现为水平线状高信号，既可能掩盖撕裂，也可能被当成撕裂；"
    "盘状半月板里的线状高信号也不一定就是损伤",
    f"{b('年龄越小越难')}：Kocher 2001 年的研究里，12 岁以下儿童 MRI 的敏感度只有 62%、特异度 90%，都比 12～16 岁的青少年低",
    "作为参照，成人 MRI 诊断内侧半月板撕裂的敏感度和特异度约为 92% 和 90%，外侧为 80% 和 95%",
]))
A.append(h4("作者医院的扫描方案"))
A.append(p(
    "术前、术后都先做常规 MRI：成对的快速自旋回波质子密度像加压脂 T2 筛查；术后金属伪影明显时，改用减金属伪影方案"
    "（优化的快速自旋回波质子密度像和反转恢复序列）。所有儿童膝关节都加一个各向同性 3D 序列，"
    "可以垂直于半月板做放射状重建，补足常规平面看不清的地方。关节造影只留给少数需要进一步解决问题的病例，"
    "因为它耗时、费钱、孩子难受，还有荨麻疹、迷走反应、过敏和化脓性关节炎等风险，不少国家关节内注射钆剂还属于超说明书用药。"
))
A.append(tcap("原文表 1　MRI 序列参数（编者译）"))
A.append(table(["序列", "TR / TE（ms）", "矩阵", "层厚 / 间隔（mm）", "时间"], [
    ["3D 快速自旋回波压脂 矢状位", "1100 / 35", "384 × 384", "1 / 无", "5:55"],
    ["快速自旋回波质子密度 矢状位", "2500 / 20～30", "512 × 480", "2.2 / 0.4", "1:48"],
    ["快速自旋回波 T2 压脂 轴位", "2500 / 40～50", "512 × 480", "3.5 / 0.3", "1:50"],
    ["快速自旋回波 T2 压脂 冠状位", "2500 / 40～50", "512 × 480", "3.5 / 0.3", "1:08"],
    ["T1 冠状位", "750 / 最短", "512 × 416", "3.5 / 0.3", "0:55"],
]))
A.append(small("TR：重复时间；TE：回波时间。视野均为 16 cm；带宽、回波链长度、激励次数等其余参数见原文表 1。"))

A.append(h2("六、儿童半月板损伤有什么特点"))
A.append(ul([
    "发生率明显低于成人；先要分清损伤发生在正常半月板还是盘状半月板上",
    f"{b('盘状半月板撕裂')}不一定有急性外伤，平均发病年龄更小（12.7 岁，非盘状 15.7 岁）",
    f"{b('正常半月板撕裂')}多来自运动伤，10 岁以下少见；撕裂类型和成人一样，但比例不同",
    f"{b('20 岁以下外侧比内侧多')}；单纯内侧撕裂随年龄增加",
    f"{b('年龄小的多为单纯半月板撕裂，年龄大的青少年更常合并韧带伤')}，可能和竞技运动参与增多有关；"
    "高中运动员最常见的合并伤是前交叉韧带损伤（36.9%）",
    f"Samora 等 124 例骨骼未成熟、做前交叉韧带重建的患者中，{b('69.3% 合并半月板损伤')}：只伤外侧 41%，只伤内侧 13%，两侧都伤 15%；"
    "主要是垂直和周缘撕裂",
]))
A.append(img(10))
A.append(img(12))
A.append(h4("根部撕裂：少见但后果重"))
A.append(p(
    "儿童半月板根部撕裂不常见，但一旦漏诊，会严重破坏半月板生物力学，加速骨关节炎。"
    f"和成人不同：{b('成人多是内侧后根撕裂，儿童多是外侧后根撕脱，而且常合并前交叉韧带损伤')}。"
    "原文图 9 这个 9 岁女孩是例外：内侧后根撕裂，没有前交叉韧带损伤。"
    "儿童急性后根撕裂血供好，及时诊断就更有机会修复愈合。"
))
A.append(img(11))

A.append(h2("七、报告里要写什么"))
A.append(p(
    "传统定义：半月板内线状高信号延伸到股骨面或胫骨面。按方向可分为水平、放射状、纵向、桶柄样和复杂撕裂："
))
A.append(ul([
    f"{b('水平撕裂')}：平行于胫骨平台，把半月板分成上下两片",
    f"{b('放射状撕裂')}：垂直于半月板长轴，从游离缘开始",
    f"{b('纵向撕裂')}：平行于长轴、垂直走行，远离游离缘",
    f"{b('桶柄样撕裂')}：纵向撕裂够长，内侧碎片移位进髁间窝",
    f"{b('复杂撕裂')}：信号异常以不止一个方向接触半月板表面，形成不止一个碎片",
]))
A.append(p(
    "除了信号，形态异常也提示撕裂：边缘不规则、关节面局灶缺损、某一段半月板异常变小。"
    f"{b('看到半月板某段比正常小，一定要去找移位的碎片')}。"
))
A.append(p(
    f"位置决定治疗：{b('外 1/3 的周缘撕裂血供丰富，保守或缝合都更容易愈合')}。"
    "斜坡样损伤（ramp 损伤）是半月板和相邻关节囊分离，可导致不稳，多见于内侧（和关节囊贴得紧），也可见于外侧后外角腘肌—半月板束附着处。"
    "儿童 MRI 上提示 ramp 损伤的表现有：内侧半月板撕裂、周缘不规则、半月板—关节囊连接处液体样信号、关节囊韧带撕裂。"
))
A.append(img(16))

A.append(h2("八、治疗原则：能缝就缝"))
A.append(ul([
    f"{b('保守治疗')}：无症状的撕裂和无症状的盘状半月板。外周血供区小的、无移位撕裂可能自愈或不再有症状。"
    f"做法是{mk('康复训练，同时 12 周内避免扭转动作和运动')}",
    f"{b('多数儿童撕裂较大，需要手术')}。缝合能降低以后关节退变的风险，强烈推荐用于中 1/3 和外 1/3（有血供区）的撕裂、"
    "纵向垂直撕裂，以及和前交叉韧带重建同期做",
    "系统综述显示：无论单纯缝合还是和前交叉韧带重建同期，儿童半月板缝合的结果都是良到优，并发症少，临床愈合率高",
    f"{b('全切或次全切的结果差')}，儿童以后的骨关节炎可能比成人更重",
    "半月板移植在儿童很少需要，是切除术后综合征的一个可行选择",
]))

A.append(h2("九、术后 MRI：别把正常愈合看成再撕裂"))
A.append(ul([
    f"缝合后，T2 上{b('修复处贯穿的液体样信号可以是正常表现')}：那是未成熟的纤维血管肉芽组织和成熟的纤维软骨瘢痕，"
    "可在 MRI 上持续 6 个月，最长到 12 年",
    f"{b('提示再撕裂')}：碎片移位；T2 上修复处贯穿的高信号（需结合术前、术式对比）；远离修复处的新异常信号",
    "常规 MRI 找不到原因、或高度怀疑再撕裂又没有术前片对比时，可做直接 MR 关节造影：造影剂在 T1 上渗进裂隙，是再撕裂的可靠征象",
    "不管用哪种方案，申请单上都要写清楚基线病史、症状、手术类型和日期，并附上术前影像",
]))
A.append(img(13))
A.append(img(14))
A.append(img(15))

A.append(h2("这篇能信几分"))
A.append(ul([
    f"{b('文章类型是教育性综述')}：单中心作者结合文献和自家病例写成，没有系统检索，也没有原始数据分析，适合当读片入门和知识框架，不能当证据级别高的结论用",
    f"{b('数字多来自被引文献')}：盘状半月板发生率、诊断准确率、撕裂类型比例等，都是转引，原始研究的样本和人群差别很大",
    f"{b('病例图都是典型例')}：挑出来的教学图，真实读片中边界情况更多",
    "优点：把“儿童和成人哪里不一样”这条主线串得很清楚，配图覆盖解剖、变异、撕裂和术后，报告清单实用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('引用错位')}：正文说 Samora 研究里的“主要撕裂类型是垂直和周缘撕裂 [36]”，但文献 36 是 Suganuma 关于腘肌—半月板束的研究，Samora 的文章是文献 52",
    f"{b('Watanabe 分型的年份')}：正文写“1978 年提出”，对应的文献 25 是 1979 年出版的关节镜图谱第 3 版",
    f"{b('图 4 的分型和部位')}：Ahn 分型是针对外侧盘状半月板的，但图 4 A、B 的图注写的是“内侧盘状半月板”",
    f"{b('儿童综述里出现了成人病例')}：图 6 是一位 20 岁女性（对比的是她 15 岁时的片子）",
    f"{b('“敏感度和特异度 95% 和 97%”指代不清')}：正文说半月板 / 胫骨宽度比和半月板覆盖率“两个比值的敏感度和特异度分别为 95% 和 97%”，没有分开写每个指标",
    f"{b('撕裂类型里混进了“盘状”')}：转引 Shieh 的撕裂类型分布时，把“盘状半月板撕裂”当成一种撕裂类型，和水平、放射状等并列",
    f"{b('表 2 小错')}：“SIGNS”拼成了“SINGS”；“撕裂长度 2.5 cm”这个预后切点正文没有给出处",
    f"{b('图 10 图注')}：说术后半月板“与 D 中的对侧半月板外观相近”，但 D 是同一膝关节的冠状位，指的应是同一膝的另一侧半月板（编者理解）",
]))

A.append(h2("落到康复门诊"))
A.append(ul([
    f"{b('孩子膝“伸不直”、又没有明显外伤')}：想到外侧盘状半月板，这是儿童盘状半月板最主要的表现",
    f"{b('深蹲 / 深屈膝时外侧卡住、伸直又好了')}：想到外侧半月板过度活动，可以做“4 字”试验；首次 MRI 阴性不能完全排除",
    f"{mk('看 MRI 报告时，儿童的“半月板内高信号”先别慌')}：没接触关节面，多是正常血管",
    f"{b('撕裂在外 1/3')}：愈合条件好；保守的话，康复期间 12 周内避免扭转和运动",
    f"{b('儿童以“保半月板”为原则')}：术后康复按缝合方案走，术后 MRI 上修复处的高信号可以持续很久，不等于失败",
    f"{b('合并前交叉韧带损伤的青少年')}：近七成合并半月板损伤，外侧更常见，评估时别只盯着韧带",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Araújo FF, Guimarães JB, da Cruz IAN, Morimoto LdR, Ormond Filho AG, Nico MAC. Pediatric menisci: normal aspects, "
    "anatomical variants, lesions, tears, and postsurgical findings. Insights Imaging. 2024;15:295. "
    "doi:10.1186/s13244-024-01867-6</em><br>"
    "原文 © The Author(s) 2024，以知识共享署名 4.0 国际许可（CC BY 4.0，http://creativecommons.org/licenses/by/4.0/）开放获取，"
    "允许在注明原作者和出处的前提下转载、改编。本文为中文解读，相对原文的改动：原文图 1 中的英文标注和缩写已原位译成中文；"
    "原文图 2～12 为 MRI 和关节镜图像，图内只有面板字母、测量字母和箭头，原样引用（仅等比缩放），中文图注为编者翻译；"
    "表格为编者根据原文表 1、表 2 翻译整理；首图、血供示意图、撕裂类型分布图、报告清单卡和封面为编者根据原文绘制。"
))


def inline_imgs(html):
    """预览页里的图片改成 base64 内嵌：单个 preview.html 拿到哪里打开都能看到图。"""
    import base64
    import re
    mime = {".png": "image/png", ".gif": "image/gif"}

    def rep(m):
        f = HERE / m.group(1)
        return f'src="data:{mime.get(f.suffix, "image/jpeg")};base64,{base64.b64encode(f.read_bytes()).decode()}"'
    return re.sub(r'src="((?:images|gifs)/[^"]+)"', rep, html)


TITLE = "「儿童半月板」MRI 怎么看？血供、盘状半月板、撕裂与术后表现一文读懂"

BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>儿童半月板影像推文</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
  :root { --ground:#ececec; --paper:#ffffff; color-scheme:light; }
  body { background:var(--ground); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
         padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:16px 32px; }
  .paper { max-width:640px; margin:0 auto; background:var(--paper); padding:20px 16px 28px; box-sizing:border-box; }
  .paper h1 { font-size:22px; line-height:1.4; margin:0 0 8px; color:#111; text-wrap:balance; }
  .paper .by { font-size:14px; color:#576b95; margin-bottom:20px; }
  .paper img { max-width:100%; }
  .paper table { display:block; overflow-x:auto; }
</style>
<div class="paper">
<h1>""" + TITLE + """</h1>
<div class="by">原创 · 骨科康复小黄</div>
""" + inline_imgs(BODY) + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
