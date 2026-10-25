#!/usr/bin/env python3
"""肌筋膜系统与运动 Part II 增加刚度（Colonna、Casacci 2024）推文。

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
    "Colonna S, Casacci F. Myofascial System and Physical Exercise: A Narrative Review on Stiffening (Part II). Cureus. 2024;16(12):e76295. doi:10.7759/cureus.76295",
    "作者单位：意大利博洛尼亚 Spine Center 康复医学部、Osteopathic Spine Center Education 研发部",
    f"文章类型：{b('叙述性综述＋作者假说')}（两篇系列的下篇；上篇讲拉伸）",
], square=True))

A.append(h2("先说为什么要谈“增加刚度”"))
A.append(p(
    f"筋膜的核心功能是传递张力。无论手法治疗还是拉伸，大家关注的几乎都是{b('“太紧”')}——整骨里叫“运动屏障”。作者提醒：张力传递还有另一种异常，{mk('“太松”')}。"
))
A.append(pic(2, "原文图 1：链条太紧太松都不行"))
A.append(ul([
    "就像足弓：肌筋膜张力过高 → 高弓足；张力不足 → 扁平足",
    f"{b('全身性的松弛')}：Ehlers-Danlos 综合征、马凡综合征、关节过度活动综合征",
    f"{b('局部松弛')}：腹股沟疝、腹壁疝、腰疝；外伤（如踝扭伤后关节囊韧带撕裂）；长期姿势异常（如腰椎前凸变小）",
    "作者的疑问：如果很多腰痛治疗都在“松解”，而腰椎不稳又是重要病因，两者如何协调？",
]))
A.append(pic(3, "原文图 2：腰椎前后筋膜张力的三种模式"))
A.append(p(
    f"例如{b('腰椎变直')}：整骨里叫“屈曲功能障碍”（伸展受限、屈曲容易，弹压试验阳性）。通常归咎于前侧太紧，但作者认为{b('后侧张力不足')}也可能是主因，所以治疗要{b('拉长前侧、同时“收紧”后侧')}。"
))

A.append(h2("筋膜能自己“变硬”吗"))
A.append(ul([
    f"{b('黏弹性')}：筋膜的变形是非线性的，取决于负荷大小、持续时间和速度；张力变化会立即引起成纤维细胞骨架重组，改变组织刚度",
    f"{b('人体静息肌筋膜张力（HRMT）')}：肌电“静默”时仍存在的固有张力，来自肌成纤维细胞和肌节中的肌动-肌球蛋白相互作用，用最少的能量维持姿势稳定",
    f"{b('筋膜能主动收缩')}：成纤维细胞和{b('肌成纤维细胞')}（介于肌细胞和成纤维细胞之间，含 α-平滑肌肌动蛋白）可以像平滑肌一样持续等长收缩；肌成纤维细胞的收缩力约为成纤维细胞的 4 倍，受氧水平、血管活性肽、自主神经、炎症因子和机械张力影响",
    "大鼠研究提示，肌成纤维细胞最多的是肌束膜，尤其是张力性肌肉",
    "张力异常可能与两类问题相关：刚度过高（斜颈、帕金森僵直、强直性脊柱炎、慢性颈腰痛）；刚度不足（围产期骨盆不稳疼痛、腰椎节段不稳、纤维肌痛）",
]))

A.append(h2("重点：屈曲-放松现象"))
A.append(pic(4, "原文图 3：健康人和腰痛患者弯腰时谁在“撑”"))
A.append(ul([
    f"健康人站立弯腰到底时，竖脊肌出现{b('肌电静息')}：躯干重量由韧带、椎间盘和肌肉筋膜的被动成分撑住",
    f"很多慢性腰痛患者（包括神经根病）{b('这个现象消失')}，竖脊肌一直在收缩。作者解释：并联的被动筋膜张力不足，由肌肉收缩和串联筋膜代偿",
    "这个现象在弯腰坐姿、颈部屈曲中也存在；腘绳肌在弯腰时比竖脊肌更晚“静息”",
    "Lee 等：健康人竖脊肌 10% 最大收缩就能让脊柱刚度平均增加 11.8%——肌肉收缩确实可以代偿稳定性",
]))

A.append(h2("刚度怎么测"))
A.append(img(6))
A.append(cap("两种无创测量方法（编者根据原文整理）"))

A.append(h2("重点：运动和筋膜刚度"))
A.append(pic(5, "原文图 4 重画：运动后胶原合成与降解"))
A.append(ul([
    "运动后胶原合成可增加到 2～3 倍，约 24 小时达峰，升高可持续 70～80 小时；但降解同时增加，运动后 18～36 小时内为净分解，训练水平越高这段时间越短，之后转为净合成",
    f"作者据此建议：{b('针对性的筋膜训练每周 1～2 次、每次几分钟')}即可刺激胶原重塑；完整重塑需要 6 个月到 2 年",
]))
A.append(img(7))
A.append(cap("运动与刚度的证据（编者整理）"))
A.append(ul([
    "Thomas 等综述：抗阻训练增加肌腱刚度，对肌肉的作用不一致；增强式训练增加肌肉刚度",
    "卧床 60 天后腰部椎旁肌静息张力增加，恢复活动（包括跳跃）后同样增加，但组织化学变化不同",
    "一项被引用的研究只有 2 名受试者、没有基线数据、没写训练时长，作者自己也指出它价值有限",
    f"{b('能否“定向”练串联或并联筋膜')}：只有肌节的间接证据，筋膜是否遵循同样规律仍是推测",
]))

A.append(h2("这篇综述能信几分"))
A.append(ul([
    f"{b('“刚度不足”是值得重视的视角')}：提醒临床不要只想着“松”，腰椎不稳、关节过度活动、产后骨盆不稳等需要的是稳定和负荷",
    f"{b('但核心仍是推理')}：腰椎变直归因于“后侧筋膜张力不足”、屈曲-放松消失归因于“并联筋膜松弛”，都没有直接测量；腰痛患者也可能是因为疼痛、恐惧而保护性收缩",
    f"{b('关于“运动增加筋膜刚度”的证据很少且矛盾')}：多数研究测的是肌腱或整块肌肉，单独测筋膜的很少；离心运动后有的变硬、有的变软",
    "没有给出具体训练方案，“每周 1～2 次、几分钟”来自肌腱研究的外推",
    "作者在致谢中说明使用了 ChatGPT-4 做语言编辑",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('离心训练前后矛盾')}：一段说离心收缩“促进并联肌节增加”（纤维变粗），后一段又说“离心训练通常增加串联肌节、向心训练增加并联肌节”",
    f"{b('胶原净分解的时间')}：图 4 图注说“前 24 小时”净分解，正文说 18～36 小时",
    f"{b('引用编号错乱')}：图 4 称改编自 Magnusson 等“[50]”，但 Magnusson 是文献 [65]；Madeleine 等是 [74]，后文说“同一作者的研究”却引用 [54]",
    f"{b('单位混用')}：Sihvonen 研究中竖脊肌在“腰椎屈曲约 79°”时静息，腘绳肌在“96.6%”腰椎屈曲时静息，一个用角度、一个用百分比",
    f"{b('概念错误')}：说肌成纤维细胞“被称为 α-平滑肌肌动蛋白”——应为“表达 α-平滑肌肌动蛋白”",
    f"{b('推理跳跃')}：从“组织在快速受力时变形较小”直接推出“持续低强度牵拉比短时高负荷更伤害筋膜刚度”，缺少依据",
    f"{b('“10% 最大收缩”写成“最大收缩的 10%”')}的病句；“tensor fascia latae end gluteus maximus”（end 应为 and）；关键词 “miofascial” 拼错",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('评估时同时考虑“太紧”和“太松”')}：过度活动、反复扭伤、产后骨盆不稳、腰椎变直伴弯腰时竖脊肌持续紧张的患者，可能更需要稳定和负荷训练，而不是更多松解",
    f"{b('弯腰时看屈曲-放松现象')}：有表面肌电的可以作为腰痛评估和疗效监测的指标",
    f"{b('训练频率')}：以胶原转换为依据，针对结缔组织的负荷训练不必每天做，每周 1～2 次、给足恢复时间",
    "测量刚度时，肌张力测定仪和剪切波弹性成像不能互换，前后比较要用同一种方法",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Colonna S, Casacci F. Myofascial System and Physical Exercise: A Narrative Review on Stiffening (Part II). Cureus. 2024;16(12):e76295. doi:10.7759/cureus.76295</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流中文解读：原文图 1～3 引自原文，图中中文标签为编者所加；图 4 由编者根据原文用中文重画（示意图），要点卡为编者整理。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「筋膜」不只会太紧，也会太松：腰痛弯腰时肌肉停不下来，可能是筋膜“撑不住”（下）"
PTITLE = "肌筋膜与刚度推文"
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
