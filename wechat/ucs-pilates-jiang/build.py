#!/usr/bin/env python3
"""普拉提 + 筋膜放松治疗上交叉综合征 RCT 推文：生成 article_body.html 与 preview.html。

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
    return p(b(t), "margin:18px 0 6px;font-size:14px;")


def mk(t):
    """黄底高亮"""
    return f'<span style="background:#fff3a3;padding:0 2px;font-weight:bold;">{t}</span>'


A = []
A.append(img(1))
A.append(cap("原文标题（Healthcare 2025;13:410，开放获取）"))

A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Jiang L, Thadanatthaphak Y, Tudpor K. Effects of Pilates Training Combined with Fascial Massage on Upper Cross Syndrome in Office Workers. Healthcare. 2025;13(4):410.",
    "作者来自泰国玛哈沙拉坎大学，受试者在四川自贡招募",
    "单盲随机对照试验；DOI：10.3390/healthcare13040410",
], square=True))

A.append(h2("圆肩、探头，几乎是上班族的标配"))
A.append(p(
    f"上交叉综合征（UCS）说白了就是一种“前紧后弱”：{red('上斜方肌、胸大肌紧张')}，{b('下斜方肌、颈深屈肌无力')}，"
    "结果就是头往前探、肩往前扣、背往后弓。在办公室人群里，患病率能到 32% 左右。"
))
A.append(p(
    "普拉提和筋膜放松，单独拿出来都常被用来改善体态。这篇研究想看的是："
    f"{mk('普拉提之前先做 5 分钟筋膜放松，会不会比只练普拉提效果更好？')}"
))
A.append(p(f"先说结论：{b('两组都有改善，加了筋膜放松的那组在头前伸角、肩前伸角、颈椎后伸和旋转、疼痛和颈椎功能上更好')}。不过数据有几处明显对不上，后面细说。"))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：25～60 岁的上班族，有明显圆肩驼背，{b('头前伸角 ≥46°、肩前伸角 ≥52°')}，并伴颈肩痛、僵硬、活动受限",
    "排除：明显的颈椎间盘退变，颈肩外伤或手术史，严重心肝肾肺功能不全，孕妇，近 3 个月接受过其他治疗或运动",
    f"34 人随机分组：{b('试验组')}先做筋膜放松再练普拉提；{b('对照组')}只练普拉提。两组都是{mk('每周 3 次、每次 1 小时、共 12 周')}",
    "每组各脱落 2 人，最后每组 15 人进入分析",
    "评估：头前伸角和肩前伸角（体态）、颈椎 6 个方向的活动度、上斜方肌、下斜方肌和胸大肌的表面肌电（频率指标）、疼痛 VAS 和颈椎功能障碍指数 NDI",
]))
A.append(pic(2, "原文图 1　研究流程（中文重绘）"))
A.append(tcap("表 2　两组基线情况"))
A.append(table(
    ["指标", "试验组", "对照组", "P 值"],
    [["年龄（岁）", "35.87 ± 9.09", "35.40 ± 8.24", "0.884"], ["身高（m）", "1.68 ± 0.07", "1.67 ± 0.08", "0.671"],
     ["体重（kg）", "68.13 ± 7.89", "65.81 ± 7.58", "0.419"], ["BMI（kg/m²）", red("20.24 ± 1.64"), red("19.68 ± 1.46"), "0.332"], ["男 / 女", "6 / 9", "8 / 7", "—"]],
))
A.append(cap("按原文身高和体重算，BMI 应在 24 左右，原文的 20 显然对不上，见文末证据评价"))

A.append(h2("重点：训练方案"))
A.append(p(
    f"方案由 7 位康复和运动训练专家一起设计，每次 1 小时，分{b('热身唤醒 → 肌肉训练 → 放松')}三段。"
    f"试验组在这之前{red('多做约 5 分钟的筋膜放松')}。"
))
A.append(pic(3, "原文表 1　试验组额外的筋膜放松（动作名为编者按照片标注）"))
A.append(p(f"筋膜放松用的是{b('筋膜枪和泡沫轴')}，重点放松上交叉里“紧”的那一侧：胸大肌、胸小肌、上斜方肌、胸锁乳突肌和背阔肌等。"))
A.append(pic(4, "原文表 1　热身唤醒"))
A.append(pic(5, "原文表 1　肌肉训练"))
A.append(p(
    f"肌肉训练这部分是针对“弱”的那一侧：{mk('颈深屈肌稳定（头后夹一个小球靠墙）')}、颈部拉起、坐姿菱形肌训练，"
    "再加上单腿后拉、双腿后踢和游泳式这些练后链和背伸肌的动作。"
))
A.append(pic(6, "原文表 1　放松练习"))
A.append(tcap("训练剂量（除呼吸练习外，所有动作相同）"))
A.append(table(
    ["阶段", "每组次数", "组数", "动作间休息", "组间休息"],
    [["第 1～4 周", "10 次", "1 组", "10 秒", "20 秒"], ["第 5～8 周", "15 次", "1 组", "10 秒", "15 秒"], ["第 9～12 周", red("20 次"), "1 组", red("5 秒"), red("10 秒")]],
))
A.append(p(f"进阶思路很直接：{b('每 4 周加 5 次、缩短休息')}。呼吸练习固定 120 秒，筋膜放松固定约 5 分钟。"))

A.append(h2("结果"))
A.append(p("原文结果全部以柱状图给出，没有具体数值表。下面的图按原图柱高读数后中文重绘，数字是近似值。"))
A.append(pic(7, "原文图 2　头前伸角和肩前伸角（中文重绘）"))
A.append(p(
    f"体态改善最直观：试验组头前伸角大约从 49° 降到 {red('39°')}，对照组降到 43°；肩前伸角试验组从 57° 降到 {red('47°')}，对照组降到 52°。"
    f"两项都是{b('试验组明显更好')}。"
))
A.append(pic(8, "原文图 3　颈椎活动度（中文重绘）"))
A.append(p(f"6 个方向两组都有增加，但组间差异只出现在{mk('后伸、左旋和右旋')}，前屈和左右侧屈两组差不多。"))
A.append(pic(9, "原文图 4　表面肌电：平均功率频率（中文重绘）"))
A.append(pic(10, "原文图 5　表面肌电：中位频率（中文重绘）"))
A.append(p(
    f"肌电看的是频率指标，一般认为频率越高、肌肉越不容易疲劳。上斜方肌和胸大肌的频率两组都升高，试验组升得更多；"
    f"但{red('下斜方肌的频率两组都下降了')}，试验组的中位频率甚至比对照组更低。"
))
A.append(pic(11, "原文图 6　疼痛和颈椎功能障碍指数（中文重绘）"))
A.append(p(f"疼痛 VAS 两组都从 4 分多降到 1 分以下；颈椎功能障碍指数试验组降到约 {red('3%')}，对照组约 7%，组间差异显著。"))

A.append(h2("证据评价"))
A.append(p(red("这篇结论看着很漂亮，但有几处硬伤，用的时候要打折扣：")))
A.append(ul([
    f"{b('BMI 算不通')}：试验组平均身高 1.68 m、体重 68.1 kg，算出来 BMI 约 24.1，原文却写 20.24；对照组同样算出约 23.6，原文写 19.68",
    f"{b('下斜方肌的结果被说反了')}：讨论里说两种干预都“激活了薄弱的下斜方肌”，但实际数据是下斜方肌的频率{red('下降')}，按作者自己的逻辑这意味着更容易疲劳，而不是被激活",
    f"{b('对照组少了 5 分钟的“额外关注”')}：试验组多出来的不只是筋膜放松，还有额外的接触和时间，没有设置对照组的等时安慰处理",
    f"{b('“单盲”盲的是受试者')}：受试者不知道自己在哪组，但评估者是否设盲没有交代；而且做没做筋膜放松，受试者自己其实是知道的",
    "每组只有 15 人，没有样本量计算，没有长期随访；动作每个只做 1 组，却同时规定了“组间休息”",
    "筋膜放松只写了“约 5 分钟”，没有说每个部位多久、力度多大",
    "原文结果只有柱状图、没有具体均值和标准差，也没有报告效应量，读者无法核对",
    "小错误：肩前伸角的测量方法里写成了“头前伸角”；颈深屈肌稳定的目标肌写的是肩胛提肌和头半棘肌；正文说对照组疼痛 P＜0.05，图里却标的是 P＜0.001",
]))

A.append(h2("落到临床"))
A.append(p(
    f"这篇最实用的是那套{mk('“先松紧的、再练弱的”')}的结构：训练前用筋膜枪或泡沫轴放松胸大小肌、上斜方肌，"
    f"然后用颈深屈肌、菱形肌、背伸肌的普拉提动作去练弱的一侧，{b('每周 3 次、每 4 周加量')}。"
))
A.append(p(
    f"至于筋膜放松到底额外贡献了多少，这篇研究{red('还不足以下结论')}。临床上训练前花几分钟放松一下没什么坏处，"
    "但真正让体态和疼痛改善的，很可能还是那 12 周规律的训练本身。"
))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Jiang L, Thadanatthaphak Y, Tudpor K. Effects of Pilates Training Combined with Fascial Massage on Upper Cross Syndrome in Office Workers. Healthcare. 2025;13(4):410. doi:10.3390/healthcare13040410</em><br>"
    "原文以 CC BY 4.0 协议开放获取。动作照片来自原文表 1，流程图和结果图为编者按原文中文重绘（结果数值按原图读取，为近似值），仅用于学术交流。"
))

TITLE = "「颈肩」圆肩探头的上班族：普拉提前先做 5 分钟筋膜放松，效果更好吗？"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>上交叉普拉提推文</title>
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
