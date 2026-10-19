#!/usr/bin/env python3
"""颈椎病肌肉能量技术与关节松动推文：生成 article_body.html 与 preview.html。

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
    "Sezerel B, Yüksel İ. Efficacy comparison of osteopathic muscle energy techniques and cervical mobilization on pain, disability, and proprioception in cervical spondylosis patients. Med Sci Monit. 2024;30:e945149.",
    "作者来自北塞浦路斯东地中海大学物理治疗与康复系",
    "三组平行随机对照试验，临床试验注册号 NCT04777318",
], square=True))

A.append(h2("先说为什么要看“位置觉”"))
A.append(p(
    f"颈椎病是颈椎的退行性改变，65 岁时几乎人人都有，最常见的表现是慢性颈痛。除了痛，{b('颈部本体感觉（位置觉）变差')}也常被忽视："
    "头摆到哪儿自己感觉不准，节段稳定性和反射都会受影响，肌肉长时间过度紧张，颈痛也更难好。"
))
A.append(p(
    f"手法里，{b('关节松动')}恢复关节的滑动，{b('肌肉能量技术')}让病人主动做小力量的等长收缩，再借“收缩后放松”把肌肉带长。"
    "两者都被认为能刺激感受器、改善位置觉，但谁更好没人直接比过。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：40～65 岁、颈痛 &gt; 3 个月、经影像确诊颈椎病，近半年没做过保守治疗；{b('排除上肢放射痛或麻木')}、颈椎手术、神经系统疾病、肩部问题、正在吃止痛药",
    f"随机分 3 组各 32 人，{b('最终完成 76 人')}（理疗 25、理疗 + 肌肉能量 25、理疗 + 关节松动 26）",
    f"三组都{b('每周 3 次、隔天做，共 4 周 12 次')}，同一位有 7 年手法经验的治疗师操作和评估",
    "结局：静息和活动时疼痛（视觉模拟评分）、哥本哈根颈部功能障碍量表（0～30）；颈部关节位置误差（戴眼罩，用颈椎活动度测量仪测“回到中立位”和“回到目标位”的误差，8 个方向）",
]))
A.append(pic(2, "三组分组"))

A.append(h2("重点：两种手法怎么做"))
A.append(h3("肌肉能量技术（Lewit 等长收缩后放松）"))
A.append(p(f"做 6 个部位：{b('上斜方肌、胸锁乳突肌、前中后斜角肌、肩胛提肌')}，两侧都做，每块肌肉 3 次。"))
A.append(pic(3, "步骤"))
A.append(ul([
    f"{mk('力度只要 20%')}：用压力生物反馈仪先测最大力量，再按 20% 控制，靠看压力表确认",
    f"{b('7 秒')}等长收缩，配合{b('吸气屏气 + 眼睛看用力方向')}；放松时{b('呼气 + 闭眼')}",
    "每次放松后，治疗师把头颈带到新的受限点，再做下一次",
]))
A.append(pic(4, "原文图 1"))
A.append(h3("颈椎关节松动（Cyriax 法）"))
A.append(ul([
    "先做椎动脉检查，再在紧张疼痛的颈后肌肉上做深部横向摩擦按摩 3～4 分钟",
    f"仰卧位 5 种被动松动：{b('徒手牵引、“架桥”、侧向滑动、牵引下旋转、牵引下前后滑动')}",
    "头几次只做“架桥”和牵引，之后再加其余 3 种",
    "牵引每次 2～3 秒、重复 3～5 次；时长、频率、进阶按个人调整",
]))
A.append(pic(5, "原文图 2"))
A.append(h3("理疗（三组共用）"))
A.append(p("热敷斜方肌和枕下肌群 20 分钟；调制经皮神经电刺激 20 分钟（80 赫兹）；连续超声 10 分钟（1 兆赫，1.5 瓦/平方厘米）。"))

A.append(h2("结果"))
A.append(pic(6, "主要结果"))
A.append(ul([
    f"{b('疼痛和功能')}：三组都明显下降（P &lt; 0.001），效应量都大；{mk('组间没有差别')}——加不加手法、加哪种，止痛效果差不多",
    f"{b('位置觉')}：肌肉能量组 {b('8 个方向的误差全部显著下降')}；关节松动组只有左侧屈有改善；理疗组都没变",
    f"组间比较只有{b('后伸')}有差别：肌肉能量组 2.64 → 1.42°，理疗组 2.99 → 3.14°（P &lt; 0.001）",
    "没有人报告不良反应",
]))
A.append(pic(7, "各方向效应量"))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{red('同一个人既治疗又评估')}，病人和治疗师都没盲，位置觉测量容易受影响",
    f"{red('没有随访')}：只看了 4 周疗程结束时",
    "随机后有 15 人在开始治疗前就退出、5 人治疗中退出（约 21%），只分析了完成者",
    "关节松动组女性占 88.5%，另两组约 60%～68%，基线不完全可比（P = 0.063）",
    "位置觉只有后伸一项组间有差别，8 个方向各比一次、又没做多重比较校正，“肌肉能量技术改善位置觉更好”的结论要打折扣",
    "疼痛基线只有约 5～7 分，“理疗就够了”可能和病人整体偏轻有关",
]))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    "随机方法前后矛盾：一处说“按就诊日期生成随机数的简单随机”，又说由统计师用随机分配软件生成序列、装信封；简单随机也不可能保证“三组各 32 人”",
    f"方法说视觉模拟评分是 {b('0～100 毫米')}，表 2 结果却以{b('厘米')}报告；讨论又拿毫米单位的最小临床重要差异来比",
    "统计说数据不符合正态分布、用了非参数检验，但结果全部用均值 ± 标准差报告",
    "效应量分级说明“右-中立”是小效应，但 d = 0.41 已接近中效应；结论说肌肉能量技术“在所有方向”都有改善，但组间只有后伸有差别",
    "肌肉能量组和关节松动组静息疼痛基线都是 5.69，关节松动组活动痛基线标准差印成“.2.53”",
    "胸锁乳突肌拼成“sternocloidomastoideus”；量表缩写一处写成 CFDS",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"颈椎病颈痛，{b('热敷 + 电刺激 + 超声')}在短期内就能明显减痛；加手法不一定多减痛",
    f"如果病人有{b('位置觉差、头摆不准')}，可以试{mk('肌肉能量技术')}：20% 力量、7 秒等长、配合呼吸和眼动，每块肌肉 3 次",
    "肌肉能量技术是病人主动参与的方法，可以教给病人在家做，用一个血压计袖带或压力反馈仪控制力度",
    "关节松动要先排除禁忌（做椎动脉检查），从牵引和“架桥”开始，再逐步加旋转和滑动",
    "评估位置觉不需要昂贵设备：戴眼罩、头顶激光笔对靶，也能做“回到中立位”测试",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　基线资料"))
A.append(table(["变量", "理疗（25 人）", "理疗 + 肌肉能量（25 人）", "理疗 + 关节松动（26 人）", "P 值"], [
    ["年龄（岁）", "55.48 ± 8.24", "51.60 ± 7.64", "50.54 ± 8.43", "0.068"],
    ["体重指数（kg/m²）", "28.47 ± 5.45", "27.11 ± 4.80", "28.63 ± 5.93", "0.741"],
    ["病程（月）", "27.80 ± 32.02", "21.16 ± 25.73", "32.69 ± 39.41", "0.358"],
    ["性别（男/女）", "10（40%）/15（60%）", "8（32%）/17（68%）", "3（11.5%）/23（88.5%）", "0.063"],
    ["利手（右/左）", "25（100%）/0", "23（92%）/2（8%）", "24（92.3%）/2（7.7%）", "0.192"],
    ["利腿（右/左）", "23（92%）/2（8%）", "21（84%）/4（16%）", "23（88.5%）/3（11.5%）", "0.679"],
    ["职业：白领", "10（40%）", "7（28%）", "9（34.6%）", "0.206"],
    ["职业：蓝领", "2（8%）", "9（36%）", "3（11.5%）", ""],
    ["职业：退休", "6（24%）", "3（12%）", "4（15.4%）", ""],
    ["职业：家庭主妇", "7（28%）", "6（24%）", "10（38.5%）", ""]]))
A.append(tcap("原文表 2　疼痛和功能障碍"))
A.append(table(["指标", "时间", "理疗", "理疗 + 肌肉能量", "理疗 + 关节松动", "组间 P（治疗时 / 校正后）"], [
    ["静息痛（厘米）", "治疗前", "5.12 ± 2.80", "5.69 ± 3.06", "5.69 ± 1.68", "0.710 / 0.912"],
    ["", "治疗后", "2.13 ± 2.02", "2.52 ± 2.53", "2.35 ± 1.68", "0.797"],
    ["", "组内 P；d", "&lt; 0.001；1.23", "&lt; 0.001；1.13", "&lt; 0.001；1.99", ""],
    ["活动痛（厘米）", "治疗前", "6.26 ± 2.93", "6.84 ± 3.14", "6.74 ± 2.53", "0.567 / 0.176"],
    ["", "治疗后", "3.10 ± 2.63", "3.74 ± 2.63", "4.31 ± 2.36", "0.219"],
    ["", "组内 P；d", "&lt; 0.001；1.14", "&lt; 0.001；1.07", "&lt; 0.001；0.99", ""],
    ["哥本哈根颈部功能障碍", "治疗前", "12.92 ± 7.58", "14.44 ± 6.81", "14.50 ± 6.24", "0.765 / 0.441"],
    ["", "治疗后", "6.80 ± 6.58", "7.08 ± 5.01", "8.62 ± 6.40", "0.356"],
    ["", "组内 P；d", "&lt; 0.001；0.86", "&lt; 0.001；1.23", "&lt; 0.001；0.93", ""]]))
A.append(small("组间 P：治疗前一行为 Kruskal-Wallis 检验 / 非参数协方差分析（Quade 检验）；治疗后一行为 Kruskal-Wallis 检验。组内为 Wilcoxon 符号秩检验；d 为效应量。"))
A.append(tcap("原文表 3　关节位置误差（°）"))
JR = [("右-中立", ["4.79 ± 3.19", "4.17 ± 3.49", "3.79 ± 3.20"], ["4.66 ± 4.27", "2.69 ± 3.71", "3.10 ± 2.79"], ["0.192；0.03", "0.005；0.41", "0.071；0.22"], "0.407 / 0.092", "0.133"),
      ("左-中立", ["7.15 ± 6.84", "5.12 ± 4.36", "4.74 ± 3.59"], ["6.21 ± 5.91", "2.88 ± 3.75", "3.97 ± 3.76"], ["0.161；0.14", "0.001；0.55", "0.148；0.21"], "0.467 / 0.055", "0.061"),
      ("前屈", ["3.12 ± 2.93", "3.57 ± 2.49", "3.41 ± 2.59"], ["2.36 ± 1.66", "1.86 ± 1.61", "2.73 ± 2.22"], ["0.139；0.31", "0.003；0.81", "0.172；0.28"], "0.568 / 0.116", "0.213"),
      ("后伸", ["2.99 ± 2.04", "2.64 ± 1.56", "2.88 ± 2.18"], ["3.14 ± 1.87 ᵃ", "1.42 ± 1.17 ᵇ", "2.15 ± 1.02"], ["0.572；0.08", "0.004；0.89", "0.143；0.43"], "0.843 / " + mk("&lt; 0.001"), mk("&lt; 0.001")),
      ("右旋", ["3.39 ± 2.36", "3.86 ± 2.78", "3.79 ± 2.81"], ["2.93 ± 2.12", "2.55 ± 2.11", "3.36 ± 1.97"], ["0.372；0.20", "0.011；0.53", "0.352；0.16"], "0.935 / 0.243", "0.295"),
      ("左旋", ["3.06 ± 1.74", "4.48 ± 2.85", "2.88 ± 1.84"], ["2.66 ± 2.29", "2.21 ± 1.33", "2.75 ± 2.15"], ["0.365；0.20", "0.002；1.02", "0.909；0.06"], "0.096 / 0.482", "0.783"),
      ("右侧屈", ["3.44 ± 3.37", "2.36 ± 1.90", "2.34 ± 1.67"], ["2.52 ± 2.55", "1.36 ± 1.27", "2.11 ± 1.67"], ["0.115；0.30", "0.010；0.62", "0.442；0.14"], "0.612 / 0.132", "0.135"),
      ("左侧屈", ["2.21 ± 1.66", "2.06 ± 1.37", "2.75 ± 1.72"], ["1.81 ± 1.50", "1.17 ± 0.95", "1.96 ± 2.17"], ["0.135；0.25", "0.011；0.75", "0.046；0.40"], "0.218 / 0.450", "0.367")]
rows = []
for nm, pre, post, w, p1, p2 in JR:
    rows += [[nm, "治疗前", *pre, p1], ["", "治疗后", *post, p2], ["", "组内 P；d", *w, ""]]
A.append(table(["方向", "时间", "理疗", "理疗 + 肌肉能量", "理疗 + 关节松动", "组间 P"], rows))
A.append(small("ᵃ、ᵇ：字母不同表示组间有显著差异。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Sezerel B, Yüksel İ. Efficacy comparison of osteopathic muscle energy techniques and cervical mobilization on pain, disability, and proprioception in cervical spondylosis patients. Med Sci Monit. 2024;30:e945149. doi:10.12659/MSM.945149</em><br>"
    "原文以知识共享署名—非商业性使用—禁止演绎 4.0 协议（CC BY-NC-ND 4.0）发表。本文为非商业学术交流用的中文解读，照片引自原文图 1、2（编者加中文图注），分组卡、步骤卡与结果图为编者中文绘制，表格为编者翻译，如有侵权请联系删除。"
))

TITLE = "「颈椎病」肌肉能量技术 vs 关节松动：止痛差不多，位置觉谁更好？"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>颈椎病手法推文</title>
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
