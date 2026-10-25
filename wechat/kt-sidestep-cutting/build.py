#!/usr/bin/env python3
"""不同长度肌内效贴对慢性踝不稳侧切的影响（Wang 等 2024）推文。

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
    "Wang X, Quan W, Ma Y, Jozsef S, Fang Y, Gu Y. The Biomechanical Effects of Kinesiology Taping Methods on Side-Step Cutting Movements in Chronic Ankle Instability. Healthcare. 2024;12(24):2561. doi:10.3390/healthcare12242561",
    "作者单位：宁波大学体育学院、匈牙利塞格德大学工学院、宁波市第二医院放射科",
    f"文章类型：{b('实验室生物力学研究')}（12 人，同一批人分别在不贴、短贴、长贴三种条件下测试）",
], square=True))

A.append(h2("先说为什么研究这个"))
A.append(ul([
    f"踝外侧扭伤复发率高，约 {b('40%')} 会发展成{b('慢性踝不稳')}（反复扭伤、总觉得脚踝“发软”）",
    "侧切（急停变向）对膝、踝的多平面负荷很大；慢性踝不稳者侧切时踝跖屈、内翻更大，髋膝屈曲也和健康人不同",
    "肌内效贴可拉伸到原长的约 140%，对皮肤产生持续牵拉；有研究认为它能改善踝本体感觉和平衡",
    f"一个没人系统研究过的问题：{mk('贴多长才好？')}只贴足踝，还是延伸到膝下（跨关节）？理论上贴得越长，覆盖皮肤越多、感觉输入越多",
]))

A.append(h2("怎么做的"))
A.append(pic(2, "原文图 1：标记点和侧切实验"))
A.append(ul([
    f"{b('受试者')}：12 名慢性踝不稳者，平均 23.9 岁、身高 181 cm、体重 80 kg；坎伯兰踝不稳量表（CAIT）平均 16.7 分（≤24 分为不稳）",
    f"{b('三种条件（随机顺序）')}：不贴（NT）、短贴（ST）、长贴（LT），每种做 4 次成功的 45° 侧切",
    f"{b('设备')}：10 台 Vicon 红外摄像头（200 Hz）＋ Kistler 测力台（1000 Hz），赤脚，舒适速度跑来",
    f"{b('分析')}：Visual 3D 算关节角度、角速度、力矩；OpenSim 算关节反作用力（地面反作用力和肌肉力的合力）；用统计参数映射（SnPM）比较整个支撑期的曲线",
]))

A.append(h2("重点：怎么贴"))
A.append(pic(3, "原文图 2：短贴的 4 条"))
A.append(pic(4, "原文图 3：长贴的 4 条"))
A.append(img(5))
A.append(cap("贴扎步骤（编者根据原文整理）"))
A.append(p(small("注意：本研究贴完立即测试、测完就撕，只看{0}，不能说明贴几天的效果。".format("贴上当下的即刻作用"))))

A.append(h2("结果（原文作者的说法）"))
A.append(ul([
    f"{b('长贴')}：屈髋、屈膝角度和屈髋角速度更大；{b('踝关节反作用力降低')}（支撑期 10%～85%）",
    f"{b('短贴')}：踝内翻角减小，膝内旋角增大",
    f"{b('两种贴法')}：髋外展力矩、膝内收/外展力矩增大",
    "作者结论：长贴的改善更明显，可能有助于慢性踝不稳者预防下肢损伤",
]))
A.append(h3("对照原文曲线看"))
A.append(pic(6, "原文图 5（上排）"))
A.append(pic(7, "原文图 5（下排）"))
A.append(pic(8, "原文图 7（上排）"))
A.append(pic(9, "原文图 7（下排）"))
A.append(pic(10, "原文图 8（上排）"))
A.append(p(small("曲线为均数，阴影为标准差；正负号含义见每张小图的标题（如“膝屈(-)/伸(+)”表示数值越负、屈膝越多）。")))
A.append(ul([
    f"{b('踝内翻角')}：两种贴法都比不贴小几度，这一点和文字一致",
    f"{b('膝屈曲')}：图 5d 中屈膝最多（曲线最低）的是{red('短贴')}，长贴和不贴几乎重合——与“长贴屈膝更大”的说法{red('相反')}",
    f"{b('踝内翻力矩')}：图 7a 中两种贴法都{red('明显高于不贴')}，长贴最高——而结论写的是“长贴显著降低踝内翻力矩”",
    f"{b('髋外展力矩')}：图 7f 中负值代表外展力矩，不贴组更负（外展力矩更大），贴扎后反而变小——与“贴扎增大髋外展力矩”不符",
    f"{b('踝关节反作用力')}：贴扎后峰值从约 3.6 降到约 2.2 倍体重（降幅约 40%），而且短贴和长贴曲线几乎一样；文字却只说长贴降低",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('文字结论和图对不上')}：上面几处关键结论与原文自己的曲线方向相反，正负号定义可能出了问题，读者无法判断哪个是对的",
    f"{b('踝关节反作用力降 40% 不太可能')}：一条贴布不太可能让踝关节受力减少近一半；跑速只要求“舒适”，没有监测，三种条件之间速度不同就能造成这样的差异",
    f"{b('统计方法')}：同一批人做三种条件，却按“三个独立组”做单因素方差分析",
    f"{b('样本小、没有对照')}：只有 12 人、性别未报告；没有假贴（安慰剂）组，受试者和测试者都知道贴了什么",
    f"{b('任务简化')}：预先知道方向的侧切，真实比赛多为临时变向；只测即刻效果",
    "优点：同时看了髋、膝、踝三个关节和关节反作用力，贴法和剪裁长度写得具体，可以复制",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('结论与图相反')}：长贴“降低踝内翻力矩”“屈膝更大”“增大髋外展力矩”三处与图 5d、图 7a、图 7f 的曲线方向不符（见上）",
    f"{b('纳入标准矛盾')}：引言按国际标准定义慢性踝不稳为“至少两次明显扭伤和/或反复扭伤”；纳入标准却是“至少一次扭伤”，又写“近 6 个月有不稳感但没有反复扭伤”",
    f"{b('讨论提到没测的指标')}：讨论说贴扎降低了“踝矢状面角速度”，结果中只报告了踝水平面角速度；还说“初始触地时屈膝角显著增大”，结果并没有单独分析触地瞬间",
    f"{b('图 8 图注顺序反了')}：图注写 a 髋、b 膝、c 踝，图中 a 是踝、c 是髋",
    f"{b('补充材料描述不一')}：三张补充图分别写“支撑期”“落地前期”“下降期”，与正文只分析支撑期不符",
    f"{b('剪裁公式括号有歧义')}：[(actual length − 8 cm/1.5) + 8 cm] × 1.10，按字面是先算 8÷1.5",
    f"{b('排版残留')}：PDF 中残留“Healthcare 2025, 13, x FOR PEER REVIEW”字样和重复段落",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('目前不能据此说“贴到膝下更好”')}：文字结论与数据矛盾，样本小、无假贴对照",
    f"{b('比较一致的发现')}：贴扎后侧切时踝内翻角减小几度，与以往研究方向一致，可作为慢性踝不稳者运动时的辅助手段",
    "肌内效贴应作为平衡训练、力量训练、本体感觉训练的补充，而不是替代",
    "想试长贴的，可以参考原文贴法（4 条、20%～35% 张力），观察患者主观稳定感和变向表现",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Wang X, Quan W, Ma Y, Jozsef S, Fang Y, Gu Y. The Biomechanical Effects of Kinesiology Taping Methods on Side-Step Cutting Movements in Chronic Ankle Instability. Healthcare. 2024;12(24):2561. doi:10.3390/healthcare12242561</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流中文解读：原文图 1、2、3、5、7、8 引自原文，图中标题、横轴和图例改为中文或加了中文标签（纵轴标题保留英文），贴扎步骤卡为编者整理。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「踝不稳」侧切时贴肌内效贴，贴到膝下更好？12 人实验和原文自相矛盾的结论"
PTITLE = "肌内效贴与侧切推文"
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
