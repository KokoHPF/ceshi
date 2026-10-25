#!/usr/bin/env python3
"""下肢体位和髋周肌共同收缩对盆底肌收缩的影响（Sato 等 2025）推文。

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
    "Sato Y, Miyake Y, Nakajima M. Effects of Lower Limb Position and Peri-Hip Muscle Co-Contraction on the Efficiency of Voluntary Pelvic Floor Muscle (PFM) Contraction During PFM Exercises. Cureus. 2025;17(4):e83088. doi:10.7759/cureus.83088",
    "作者单位：日本福山 Studio TAIKA（物理治疗）、吉备国际大学保健医疗福祉学部作业治疗学科和物理治疗学科",
    f"文章类型：{b('原创研究')}（19 名健康女性，每人做 4 种练习的自身对照）",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"成年女性中约 30%～50% 有尿失禁，其中{b('压力性尿失禁')}（咳嗽、打喷嚏、跳跃时漏尿）最常见，主要和盆底肌功能不良有关。{b('盆底肌训练')}在日本指南中是 A 级推荐，但约 {red('30% 的人不会正确地主动收缩盆底肌')}。"
))
A.append(p(
    f"临床上常见两种“辅助”做法：一是换体位（躺着练还是屈膝练）；二是让患者{mk('同时夹腿或外撑腿')}，希望借髋内收肌、外展肌一起发力带动盆底肌。哪种体位更好、夹腿撑腿到底有没有用，并没有共识。"
))

A.append(h2("怎么做的"))
A.append(img(2))
A.append(cap("实验流程（编者根据原文整理）"))
A.append(h3("四种练习"))
A.append(pic(3, "原文图 1：A 仰卧伸腿"))
A.append(pic(4, "原文图 2：B 仰卧屈膝"))
A.append(pic(5, "原文图 3：C 屈膝＋外撑弹力带"))
A.append(pic(6, "原文图 4：D 屈膝＋夹球"))
A.append(ul([
    f"C、D 两种都把髋部用力控制在{b('最大自主用力的 30%')}，用拉力传感器或球上的压力表监控",
    "四种练习的顺序随机；每种收缩 10 秒、休息 20 秒，做 3 次，正常呼吸",
    "统一口令：“像把阴道往上提一样，收紧臀部”",
]))
A.append(h3("怎么测"))
A.append(pic(7, "原文图 5、6：经腹超声测膀胱底抬高"))
A.append(p(
    f"由一名有经验的女性治疗师用经腹超声测量，另有女性检查者确保骨盆处于中立位。盆底肌收缩时会把{b('膀胱底往上抬')}，抬得越高说明收缩越有效。"
))

A.append(h2("结果"))
A.append(pic(8, "四种练习的膀胱底抬高量（编者根据原文图 7 重画）"))
A.append(table(["练习", "膀胱底抬高（mm）", "与 B 比较"], [
    ["A 仰卧伸腿", "3.58 ± 2.1", "P＝0.001"],
    ["B 仰卧屈膝", f"{b('6.00 ± 3.1')}", "—"],
    ["C 屈膝＋外撑（髋外展）", "2.64 ± 4.3", "P＝0.001"],
    ["D 屈膝＋夹球（髋内收）", "2.73 ± 2.8", "P＝0.001"],
]))
A.append(tcap("四种练习的膀胱底抬高量（均数 ± 标准差，19 人，根据原文结果整理）"))
A.append(ul([
    f"{b('仰卧屈膝（B）最好')}：膀胱底抬高 6.00 mm，比仰卧伸腿（A）多约 2.4 mm",
    f"{mk('加上夹腿或撑腿反而更差')}：C、D 和 B 是同一个屈膝体位，只是多了髋部用力，抬高量却降到 2.6～2.7 mm，甚至比伸腿平躺还低",
    "A、C、D 三者之间没有报告显著差异",
]))
A.append(h3("作者怎么解释"))
A.append(ul([
    f"{b('屈髋为什么好')}：屈髋 45° 时闭孔内肌和耻骨直肠肌的腱弓被拉紧，可能更容易感知并收缩位置深在、负责上提膀胱底的耻骨直肠肌",
    f"{b('夹腿撑腿为什么差')}：作者认为是{b('双重任务干扰')}——同时做两件都不容易的事，注意力被分散，至少一件做不好；就像老人边走路边倒数数字时步速变慢、平衡变差",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('只是健康年轻女性的一次性测量')}：没有尿失禁患者、没有生育过的人，也没有训练效果；作者自己也承认，对真正的患者，夹腿撑腿是否帮助收缩还不能排除",
    f"{b('膀胱底抬高是间接指标')}：经腹超声测的是膀胱后壁位移，会受腹压、呼吸、膀胱充盈程度和探头位置影响；没有测盆底肌肌电或阴道压力",
    f"{b('统计方法不对')}：同一批人做了 4 种练习（自身对照），却用了比较独立组的单因素方差分析，并把四种练习称为“组”；应该用重复测量方差分析",
    f"{b('个体差异很大')}：C 组标准差 4.3 mm 大于均数 2.64 mm，说明有人抬得很高、有人几乎没抬甚至下降",
    f"{b('“双重任务”只是推测')}：研究没有测注意力，也没有测髋部用力时盆底肌是否被腹压往下推；C、D 的屈膝角度从照片看也比 B 更大",
    "口令里包含“收紧臀部”，本身就可能引起臀肌参与，和“单独收缩盆底肌”的理念不完全一致",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('体位名称前后不一')}：方法里四种练习都是“仰卧屈膝（supine kneeling）”，讨论和结论却写成“跪立位（upright kneeling）比仰卧更好”——两者完全不是一个姿势，照片显示是仰卧屈膝",
    f"{b('效应量算不出来')}：按文中均数和标准差计算，B 与 A、C、D 比较的 Cohen d 约为 0.9、0.9、1.1，文中却写 1.46、1.56、1.61；三个 P 值也都恰好是 0.001",
    f"{b('膀胱准备矛盾')}：先写“测前 1 小时排空膀胱后喝 500 ml 水”，后面又写“测量前让受试者排尿以统一膀胱容量”——排空后超声就看不清膀胱底",
    f"{b('超声频率')}：写成“3 Hz”，超声探头频率应为兆赫（MHz）级",
    f"{b('图 6 图注')}：提到“静息（a）”和“最大抬高（b）”两张图，但原文图 5、6 没有 a、b 标记",
    f"{b('结果描述混乱')}：结果部分有一句“B 组在盆底收缩后接着做屈膝体位”，与方法描述不符",
    f"{b('练习 D 的体位')}：写“屈髋 45°、髋外展 30°”再做内收夹球，和练习 B、C 的起始体位不同",
    f"{b('用词')}：讨论里说用低频电刺激让盆底肌“利他地（altruistic）”收缩，应为“被动地”",
]))

A.append(h2("落到临床"))
A.append(img(9))
A.append(cap("盆底肌练习体位要点（编者整理）"))
A.append(ul([
    f"{mk('教盆底肌收缩时，先用仰卧屈膝位')}，比平躺伸腿更容易收到位",
    f"{b('先别加夹腿、撑腿')}：对健康女性来说，这样不但不帮忙，还会让盆底肌收缩变差；先学会单独、准确地收缩",
    f"{b('看得见更好')}：有条件的话用经腹超声或其他生物反馈，让患者看到膀胱底被抬起，比单靠口令更可靠",
    "对已经尿失禁、产后或盆底功能很差的患者，体位和辅助动作的效果可能不同，需要个体化评估",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Sato Y, Miyake Y, Nakajima M. Effects of Lower Limb Position and Peri-Hip Muscle Co-Contraction on the Efficiency of Voluntary Pelvic Floor Muscle (PFM) Contraction During PFM Exercises. Cureus. 2025;17(4):e83088. doi:10.7759/cureus.83088</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流中文解读：原文图 1～6 引自原文，图中中文标签为编者所加；结果图由编者根据原文用中文重画，流程卡和要点卡为编者整理。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「盆底肌」练盆底肌要不要夹腿？仰卧屈膝收得最好，加上夹球或外撑反而更差"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>盆底肌练习体位推文</title>
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
