#!/usr/bin/env python3
"""肌内效贴张力对慢性踝不稳运动员本体感觉的即刻影响（Chang 等 2026）推文。

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
    "Chang CL, Lin HY, Tseng YT, Pan CY, Chen FC, Tsai CL. Immediate effects of kinesiology taping on proprioception and functional performance in collegiate athletes with chronic ankle instability: evidence from event-related potentials. BMC Sports Science, Medicine and Rehabilitation. 2026;18:83. doi:10.1186/s13102-025-01468-w",
    "作者单位：台湾成功大学体育健康与休闲研究所等",
    f"文章类型：{b('自身交叉设计研究')}（30 名运动员，同一批人先后接受两种张力的贴扎）",
], square=True))

A.append(h2("先说为什么研究这个"))
A.append(ul([
    f"约 {b('40%')} 的踝扭伤运动员会发展为慢性踝不稳；问题不只是韧带松，还有{b('本体感觉下降')}——感知踝关节位置和运动的能力变差，肌肉反应延迟、落地不准，更容易再扭伤",
    "肌内效贴被认为能通过牵拉皮肤、刺激皮肤机械感受器来增强感觉输入",
    f"但研究结果不一致，一个可能原因是{mk('各研究的贴布张力差别很大（0%～35%）')}",
    f"本研究用{b('精确的本体感觉测试')}（机器人测“能分辨多小的速度差”）加{b('脑电')}，比较 35% 张力和 0% 张力的即刻效果",
]))

A.append(h2("怎么做的"))
A.append(img(2))
A.append(cap("实验设计（编者根据原文整理）"))
A.append(pic(3, "原文图 1：贴法"))
A.append(pic(4, "原文图 2A：机器人踝本体感觉测试"))
A.append(pic(5, "原文图 3：单腿左右侧跳"))
A.append(p(f"剪多长：剪裁长度 ＝ [（实际长度 − 8 cm）÷ 系数 ＋ 8 cm] × 1.10，35% 张力系数取 1.35，0% 张力取 1.00（两端各留 4 cm 不拉伸的锚点）。"))

A.append(h2("重点：本体感觉和脑电结果"))
A.append(pic(6, "原文图 4：心理物理曲线示例"))
A.append(pic(7, "JND 和 N1 结果（编者重画）"))
A.append(ul([
    f"{b('35% 张力')}：最小可觉差从 1.86 降到 {b('1.43 °/s')}（P＝0.004），能分辨的速度差更小，感觉更灵敏",
    f"{b('0% 张力')}：最小可觉差从 1.83 升到 {red('2.19 °/s')}（P＝0.015），反而变差",
    "不确定区间（IU）两种条件都没有变化",
    f"{b('脑电 N1')}：0% 张力贴后 N1 从 −15.2 减弱到 −11.9 μV（P＝0.005）；35% 张力贴后 −13.6 → −15.2 μV，{b('没有显著变化')}（P＝0.184）",
]))
A.append(pic(8, "原文图 5：0% 张力的脑电波形"))
A.append(pic(9, "原文图 6：35% 张力的脑电波形"))

A.append(h2("功能测试结果"))
A.append(img(10))
A.append(cap("功能测试结果（编者根据原文整理）"))
A.append(p(f"作者结论：{b('适当张力的肌内效贴能即刻提高本体感觉、皮层反应和功能稳定性')}，而不加张力的“安慰剂贴”可能干扰感觉处理、降低表现。"))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('顺序没有随机')}：所有人都先做 35%、两个月后再做 0%。两次实验的季节、训练状态、对测试的熟悉程度、期望都可能不同，差异不一定来自张力",
    f"{b('盲法不完整')}：贴的时候戴眼罩，但 35% 和 0% 张力贴上后皮肤牵拉感明显不同，受试者很可能分得出来；功能测试的评估者也不盲",
    f"{b('统计方法')}：同一批人做两种条件，统计自由度 F(1,58) 却相当于把 60 次测量当作独立样本，文中还出现了并不存在的“组别主效应”；相关分析也把每人两次的数据混在一起算",
    f"{b('“0% 张力变差”难以解释')}：作者原先假设 0% 张力不会有变化，结果却变差，事后解释为“安慰剂贴干扰感觉”，缺少直接证据",
    f"{b('结论说过头')}：摘要和结论说 35% 张力“增强了皮层反应”，但 35% 张力下 N1 并没有显著变化",
    f"{b('效应量小、只看即刻')}：JND 改善约 0.4 °/s，临床意义不明；贴完马上测，不知道能维持多久，也不知道能否减少再扭伤",
    "优点：本体感觉测试精细（随机顺序、贝叶斯自适应），同步记录脑电，样本量事先计算，男女各半",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('阈值数字矛盾')}：说两次运动的角度差“控制在 4° 以下，小于健康年轻人约 2.4° 的位置觉阈值”——4° 明明大于 2.4°",
    f"{b('N1 时间窗不一')}：引言写 N1 出现在刺激后 100～150 ms，方法写 100～200 ms",
    f"{b('设计名称不一')}：方法称“自身交叉设计”，统计部分写“两因素混合设计”，结果中多次报告“组别主效应”",
    f"{b('引言前后矛盾')}：先说肌内效贴对慢性踝不稳本体感觉和功能的影响“仍然未知”，下一句就列举了多项已有研究",
    f"{b('结论与数据不符')}：35% 张力下 N1 无显著变化（P＝0.184），摘要却说“适当张力增强皮层反应”",
    f"{b('笔误')}：表 2 写“p < 0.504”；伺服电机精度写“4.29–5°”，含义不明",
    f"{b('局限性说法')}：局限性称“样本量较小”，而事先功效分析只需要 26 人，研究纳入了 30 人",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('给慢性踝不稳运动员贴肌内效贴，拉一定张力（约 35%）比不拉更合理')}：至少在贴上当下，感觉更灵敏，闭眼单腿站得更久，侧跳失误更少",
    f"{b('不要把“不拉张力”当作无害')}：本研究中 0% 张力贴后感觉和侧跳表现反而变差（虽然可能有顺序效应）",
    "贴法简单：胫骨前肌、腓骨肌各一条 I 形贴，从踝上方贴到足部",
    "肌内效贴只是即刻的辅助手段，长期仍要靠平衡、本体感觉和力量训练",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Chang CL, Lin HY, Tseng YT, Pan CY, Chen FC, Tsai CL. Immediate effects of kinesiology taping on proprioception and functional performance in collegiate athletes with chronic ankle instability: evidence from event-related potentials. BMC Sports Sci Med Rehabil. 2026;18:83. doi:10.1186/s13102-025-01468-w</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流中文解读：原文图 1～6 引自原文，图中中文标签为编者所加；JND 和 N1 结果图由编者根据原文数字用中文重画，设计卡和结果卡为编者整理。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「踝不稳」肌内效贴要不要拉张力？35% 张力贴后踝更“灵敏”，不拉反而变差（附脑电证据）"
PTITLE = "肌内效贴张力推文"
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
