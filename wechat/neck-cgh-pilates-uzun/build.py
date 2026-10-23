#!/usr/bin/env python3
"""颈椎松动联合临床普拉提治疗颈源性头痛（Uzun 等 2024）推文。

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
    "Uzun M, İkidağ MA, Ekmekyapar Fırat Y, Ergun N, Akbayrak T. The Effects of Cervical Mobilization with Clinical Pilates Exercises on Pain, Muscle Stiffness and Head and Neck Blood Flow in Cervicogenic Headache: Randomized Controlled Trial. Medicina. 2024;60(6):852. doi:10.3390/medicina60060852",
    "作者单位：土耳其 SANKO 大学物理治疗与康复系、放射科、神经科，以及 Hacettepe 大学",
    f"研究类型：{b('随机对照试验')}，25 名颈源性头痛患者，治疗 6 周；ClinicalTrials.gov 注册号 NCT05883319",
], square=True))

A.append(h2("先说为什么要研究颈源性头痛的运动和手法"))
A.append(p(
    f"颈源性头痛（CHA）是一种{b('起源于上颈段结构')}的继发性头痛：多为单侧，从枕颈部放射到耳部和颧部，呈压迫样、有时搏动样，颈部动作可诱发，可持续数天到数周。"
    f"这类患者常有颈椎活动度下降、{b('颈深屈肌无力')}、头前伸姿势和颈部肌肉僵硬。"
))
A.append(p(
    f"手法治疗是 CHA 指南推荐的方法，以往研究多用 Mulligan SNAG、Maitland 等上颈段松动；运动方面有颅颈屈曲、颈部稳定训练等。作者想回答两个问题："
    f"{mk('在颈椎松动的基础上加临床普拉提，效果会不会更好')}？以及这些治疗会不会改变{b('头颈部动脉血流')}？"
    f"作者称这是第一项在 CHA 中使用 Cyriax 颈椎松动、也是第一项用临床普拉提治疗 CHA 的研究。"
))

A.append(h2("怎么做的"))
A.append(pic(2, "原文图 1：CONSORT 流程图（编者中文重绘）"))
A.append(ul([
    f"{b('对象')}：神经科门诊由专科医生诊断的 CHA 患者，18～65 岁，近几个月未接受过（除止痛药外的）药物或物理治疗；排除头痛手术史、严重心脏病史或手术史、恶性肿瘤史、癫痫",
    f"{b('分组')}：按年龄、性别和头痛病程用{b('最小化法')}随机分为 CM 组和 CM+CPE 组。37 人筛查，31 人随机，6 人中途退出（3 人担心新冠、3 人没时间），最终 CM 组 13 人、CM+CPE 组 12 人纳入分析",
    f"{b('评估')}：治疗前和 6 周后；血流由一名有 20 年经验的放射科医生测，其余指标由同一名物理治疗师测",
    f"{b('统计')}：组内前后比较用 Wilcoxon 符号秩检验，组间比较变化量用 Mann-Whitney U 检验",
]))

A.append(h2("重点：手法怎么做、普拉提怎么练"))
A.append(pic(3, "干预方案（编者根据原文整理）"))
A.append(h3("颈椎松动：Cyriax 技术，两组都做"))
A.append(ul([
    f"患者仰卧在治疗床上，{red('松动前先做椎基底动脉（VBA）试验')}，本研究全部阴性",
    f"依次做：{b('桥式手法、手法牵引、牵引下旋转、牵引下前后滑动、侧向滑动、斜方肌手法牵伸')}",
    "每种技术 8～10 次，共约 10 分钟；每周 3 次，共 6 周",
]))
A.append(h3("临床普拉提：APPI 体系，CM+CPE 组另加"))
A.append(p(
    f"澳大利亚物理治疗与普拉提学院（APPI）把传统普拉提改良成适合临床使用的版本。先把 {mk('5 个基本要素')}教会患者，训练全程用口头和触觉提示维持："
))
A.append(ul([
    f"{b('侧向呼吸')}：吸气时胸廓向两侧扩张",
    f"{b('脊柱中立位与核心启动')}",
    f"{b('肩带定位')}、{b('胸廓定位')}、{b('头颈定位')}",
]))
A.append(pic(4, "原文图 2：临床普拉提动作（A～L）"))
A.append(table(["编号", "动作", "体位"], [
    ["A", "上背部热身", "站立"], ["B", "侍者式（Dumb Waiter）", "站立"], ["C", "胸部牵伸", "站立"], ["D", "开瓶器式（Corkscrew）", "站立"],
    ["E", "上半身卷动", "站立"], ["F", "侧卧开臂 1 级", "侧卧"], ["G", "双腿伸展 1 级", "仰卧屈膝"], ["H", "天鹅潜水 1～3 级", "俯卧"],
    ["I", "蛙泳预备 1（2 级）", "俯卧"], ["J", "脊柱扭转", "盘腿坐"], ["K", "猫式伸展", "四点跪"], ["L", "主动斜方肌牵伸", "盘腿坐"],
], first_bold=False))
A.append(tcap("临床普拉提动作一览（编者根据原文图 2 整理；体位为编者根据照片补充）"))
A.append(ul([
    "每个动作 8～10 次，由 APPI 认证的物理治疗师现场指导",
    f"设计目标：{mk('增强颈深屈肌，放松颈周肌肉，提高脊柱稳定性和灵活性')}",
    "作者在讨论中说明：动作中靠颈深屈肌维持颈部稳定，靠菱形肌、中下斜方肌和前锯肌稳定肩胛，同时让上斜方肌和胸肌保持在拉长位，全程维持良好姿势",
]))

A.append(h2("结果（压缩版）"))
A.append(table(["", "CM 组（13 人）", "CM+CPE 组（12 人）", "P 值"], [
    ["年龄（岁）", "34.9 ± 9.214", "30.25 ± 9.016", "0.276ᵇ"],
    ["头痛病程（年）", "3.38 ± 2.142", "3.25 ± 2.454", "0.782ᵇ"],
    ["BMI（kg/m²）", "21.432 ± 4.896", "20.612 ± 3.946", "0.744ᵇ"],
    ["女性，n（%）", "9（69）", "9（75）", "0.748ᵃ"],
    ["男性，n（%）", "4（31）", "3（25）", ""],
]))
A.append(tcap("原文表 1：人口学资料和头痛病程（中文翻译）"))
A.append(small("数值为均值 ± 标准差；CM：颈椎松动组；CPE：临床普拉提运动组；ᵃ 卡方检验；ᵇ Mann-Whitney U 检验。"))
A.append(pic(5, "疼痛相关结果（编者根据原文表 2 均值绘制）"))
A.append(ul([
    f"{b('两组都明显改善')}：头痛频率从每月 13～17 次降到约 3.6 次，止痛药从每月 12～14 次降到约 2.5 次；三块肌肉的僵硬度都下降；颈内动脉和椎动脉血流速度都上升（组内均 P &lt; 0.05）",
    f"{b('组间差异只有 2 项')}：头痛强度下降幅度 CM+CPE 组更大（5.55 对 4.07 cm，P = 0.025），左侧胸锁乳突肌僵硬度下降更多（43.33 对 23.31 N/m，P = 0.044）",
    "头痛频率、止痛药用量、其余 5 处肌肉僵硬度、4 项血流指标，组间都没有差异",
]))
A.append(p(f"作者结论：{mk('在颈源性头痛的非药物治疗中，颈椎松动加临床普拉提可能更有益')}。"))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('没有“不治疗”或假治疗对照')}：两组都做了松动，头痛又有自然波动和回归均值，组内改善不能全算在治疗头上；作者说“证明手法有效”说过头了",
    f"{b('组间唯一的疼痛差异可能来自基线不同')}：CM+CPE 组治疗前头痛强度高 1.6 cm（7.43 对 5.81），治疗后两组几乎一样（1.88 对 1.74），“下降更多”很可能只是起点更高",
    f"{b('多重比较')}：组间比较了 13 个指标，只有 2 个 P 略小于 0.05，没有校正，偶然出现的可能性不小",
    f"{b('剂量不对等')}：CM+CPE 组每次多了一套 12 个动作的普拉提，治疗时间和治疗师接触都更多",
    f"{b('设盲不清楚')}：除血流外的指标都由同一名物理治疗师测，治疗也由同一名物理治疗师做，原文没说测量者是否知道分组",
    f"{b('血流“增加”临床意义很小')}：颈内动脉收缩期峰值只增加约 1.3～1.7 cm/s（约 1%），在多普勒测量误差范围内",
    f"{b('样本小、没随访、按实际完成者分析')}：25 人，6 周后就结束；退出的 6 人没有纳入分析",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('样本量算不通')}：原文说按效应量 d = 0.8、α = 5%、检验效能 95%，每组只需 9 人。按两独立样本比较，这些参数需要每组约 {b('42 人')}（效能 80% 也要约 26 人）；即使按配对比较也要约 23 人",
    f"{b('右侧胸锁乳突肌数据疑似抄错')}：CM 组右侧胸锁乳突肌治疗后 210.08 ± 22.29，和左侧完全相同；按前后均值算变化应为 32.61，表中写 34.30",
    f"{b('左上斜方肌变化量对不上')}：CM+CPE 组 332.42 − 275.50 = 56.92，表中写 56.58",
    f"{b('组内 P 值都是“最小可能值”')}：疼痛、僵硬度和颈内动脉收缩期峰值的组内 P 值，CM 组全是 0.001、CM+CPE 组全是 0.002。用 Wilcoxon 检验（正态近似），13 人和 12 人能得到的最小 P 值正好约为 0.0015 和 0.0022，意味着{b('每一位患者的每一项指标都改善了')}，包括血流速度，这在小样本中相当少见",
    f"{b('流程图组名写错')}：原文图 1 左侧写成“CP intervention”，按正文应为 CM 组",
    f"{b('缩写不统一')}：颈源性头痛在摘要里混用 CHA 和 CGH；摘要说“SKM 僵硬度”有组间差异，表中是左侧 SCM（胸锁乳突肌）",
    f"{b('注册时间存疑')}：注册号 NCT05883319 标注日期为 2022 年 3 月 22 日，但伦理审批在 2020 年、退出原因涉及新冠，研究可能在注册前就已开始；而按 ClinicalTrials.gov 的编号顺序，NCT0588 开头的注册号大约对应 2023 年年中",
    f"{b('结论超出数据')}：结论说颈椎松动能“增加颈部血流”，但这只是组内前后比较、增幅很小，且没有对照",
    f"{b('小错')}：表 1 “Famele”应为 Female；表 2 “X ± SS”应为 X ± SD；“three days 3 times a week”重复",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('颈源性头痛可以“手法 + 运动”一起上')}：这篇两组都明显改善，普拉提的额外好处不确定，但运动本身对颈深屈肌、姿势和长期管理有价值",
    f"{b('普拉提的抓手是 5 个基本要素')}：侧向呼吸、脊柱中立、肩带、胸廓、头颈定位，先教会再加动作；12 个动作大多徒手、垫上即可完成，适合做成家庭训练",
    f"{b('颈椎松动前做安全筛查')}：本研究先做 VBA 试验；临床上更重要的是问清楚头晕、视物异常、构音障碍等危险信号",
    f"{b('别被“血流增加”带偏')}：1% 左右的血流变化没有临床意义；也不能据此说手法改善脑供血",
    f"{b('评估别只看疼痛强度')}：头痛频率、止痛药用量更贴近患者生活，这篇里这两项组间并无差异",
]))

A.append(h2("附录：原文表 2 全文翻译"))
rows2 = []
for name, cm, pa, cp, pa2, z, pb in [
    ("头痛频率（次 / 月）", ("13.38 ± 7.54", "3.62 ± 2.78", "9.769 ± 5.433"), "0.001*", ("17.08 ± 10.71", "3.58 ± 2.99", "13.5 ± 8.969"), "0.002*", "−0.982", "0.325"),
    ("头痛强度（cm）", ("5.81 ± 1.18", "1.74 ± 1.41", "4.072 ± 1.076"), "0.001*", ("7.43 ± 1.04", "1.88 ± 1.14", "5.55 ± 1.720"), "0.002*", "−2.232", "0.025*"),
    ("止痛药（次 / 月）", ("12.23 ± 10.94", "2.62 ± 3.30", "9.615 ± 8.713"), "0.001*", ("13.75 ± 12.70", "2.42 ± 2.39", "11.33 ± 11.364"), "0.002*", "−0.491", "0.623"),
    ("右枕下肌（N/m）", ("331.85 ± 98.75", "254.23 ± 67.46", "77.61 ± 85.81"), "0.001*", ("304.92 ± 70.98", "232.08 ± 54.45", "72.83 ± 44.29"), "0.002*", "−0.598", "0.549"),
    ("左枕下肌（N/m）", ("326.69 ± 98.78", "237.69 ± 45.17", "89 ± 94.36"), "0.001*", ("302.83 ± 76.13", "236 ± 47.94", "66.83 ± 46.99"), "0.002*", "−0.163", "0.870"),
    ("右上斜方肌（N/m）", ("291.08 ± 47.40", "243.62 ± 40.39", "47.461 ± 26.38"), "0.001*", ("319.42 ± 55.64", "268.58 ± 51.25", "50.83 ± 17.23"), "0.002*", "−1.008", "0.313"),
    ("左上斜方肌（N/m）", ("299.08 ± 53.87", "255.46 ± 46.01", "43.61 ± 30.30"), "0.001*", ("332.42 ± 68.32", "275.50 ± 54.20", "56.58 ± 27.87"), "0.002*", "−1.142", "0.253"),
    ("右胸锁乳突肌（N/m）", ("242.69 ± 45.31", "210.08 ± 22.29", "34.30 ± 36.88"), "0.001*", ("246.50 ± 45.83", "204.83 ± 28.02", "41.66 ± 21.70"), "0.002*", "−1.715", "0.086"),
    ("左胸锁乳突肌（N/m）", ("233.38 ± 21.9", "210.08 ± 22.29", "23.307 ± 12.31"), "0.001*", ("253.25 ± 58.77", "209.92 ± 52.15", "43.33 ± 29.61"), "0.002*", "−2.013", "0.044*"),
    ("颈内动脉 PS（cm/s）", ("111.36 ± 14.86", "112.62 ± 14.95", "1.261 ± 1.025"), "0.001*", ("118.89 ± 13.11", "120.64 ± 13.22", "1.745 ± 1.104"), "0.002*", "−1.198", "0.231"),
    ("颈内动脉 ED（cm/s）", ("37.62 ± 7.63", "38.46 ± 7.27", "0.842 ± 0.902"), "0.011*", ("40.31 ± 4.38", "42.40 ± 5.462", "2.087 ± 3.207"), "0.005*", "−1.306", "0.191"),
    ("椎动脉 PS（cm/s）", ("82.75 ± 16.35", "83.39 ± 16.72", "0.638 ± 0.975"), "0.034*", ("70.720 ± 15.41", "71.49 ± 15.33", "0.775 ± 0.907"), "0.010*", "−0.326", "0.744"),
    ("椎动脉 ED（cm/s）", ("27.43 ± 6.80", "28.05 ± 6.86", "0.623 ± 0.709"), "0.012*", ("25.85 ± 6.50", "27.01 ± 6.40", "1.160 ± 1.382"), "0.015*", "−0.708", "0.479"),
]:
    rows2.append([name, f"前 {cm[0]}<br>后 {cm[1]}<br>变化 {cm[2]}", pa, f"前 {cp[0]}<br>后 {cp[1]}<br>变化 {cp[2]}", pa2, z, pb])
A.append(table(["指标", "CM 组", "pᵃ", "CM+CPE 组", "pᵃ", "Z", "pᵇ"], rows2))
A.append(tcap("原文表 2：组内和组间结局指标比较（中文翻译）"))
A.append(small("均值 ± 标准差。* p &lt; 0.05；pᵃ 为组内比较（Wilcoxon 检验），pᵇ 为组间比较（Mann-Whitney U 检验）。CM：颈椎松动组；CPE：临床普拉提运动组；PS：收缩期峰值流速；ED：舒张末期流速。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Uzun M, İkidağ MA, Ekmekyapar Fırat Y, Ergun N, Akbayrak T. The Effects of Cervical Mobilization with Clinical Pilates Exercises on Pain, Muscle Stiffness and Head and Neck Blood Flow in Cervicogenic Headache: Randomized Controlled Trial. Medicina. 2024;60(6):852. doi:10.3390/medicina60060852</em><br>"
    "原文以 CC BY 4.0 许可发表。本文为学术交流用的中文解读：原文图 1 按原意用中文重绘，图 2 原样引用并加中文图注，表 1、表 2 为中文翻译，方案卡和结果图为编者根据原文整理绘制。"
))

TITLE = "「颈椎」颈源性头痛：颈椎松动 + 临床普拉提，12 个动作和 6 周疗效精读"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>颈源性头痛推文</title>
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
