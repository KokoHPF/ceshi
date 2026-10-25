#!/usr/bin/env python3
"""开链、闭链和混合链训练治疗膝骨关节炎（Olagbegi 等 2017）推文。

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
    "Olagbegi OM, Adegoke BOA, Odole AC. Effectiveness of three modes of kinetic-chain exercises on quadriceps muscle strength and thigh girth among individuals with knee osteoarthritis. Archives of Physiotherapy. 2017;7:9. doi:10.1186/s40945-017-0036-6",
    "作者单位：南非罗德斯大学人体运动学与人类工效学系、尼日利亚伊巴丹大学物理治疗系；病例来自尼日利亚奥沃联邦医学中心",
    f"文章类型：{b('随机临床试验')}（96 人，三组比较；是同一试验疼痛结果之外的二次分析）",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"膝骨关节炎患者的{b('股四头肌')}普遍无力，而股四头肌是伸膝和稳定膝关节的主力。指南都推荐运动治疗，其中股四头肌力量训练是核心。"
))
A.append(p(
    f"力量训练可以分两类：{b('开链')}（脚不着地，只动小腿，如坐位伸膝、直腿抬高）和{b('闭链')}（脚踩地，全身一起负重，如靠墙滑蹲、上台阶）。两类单独都有效，但{mk('谁更好、两者结合会不会更好')}一直没有定论。"
))
A.append(p(
    f"作者之前发表过这项试验的疼痛结果：{b('开链＋闭链的混合组止痛效果最好')}。这篇文章接着看肌力和大腿围度。"
))

A.append(h2("怎么做的"))
A.append(pic(2, "研究流程（原文图 7 用中文重画）"))
A.append(ul([
    f"{b('对象')}：2013～2014 年在尼日利亚奥沃联邦医学中心就诊的膝骨关节炎患者，X 线 {b('Kellgren-Lawrence 2 级')}，并符合美国风湿病学会临床标准；平均约 61 岁，平均 BMI 约 30（偏胖）",
    f"{b('排除')}：合并神经系统疾病、严重全身疾病，或身体条件无法完成训练",
    f"{b('分组')}：电脑随机，每组 32 人：开链组、闭链组、混合链组；转诊医生和患者不知道分组，{b('评估者知道')}",
    f"{b('疗程')}：12 周；所有人每天服用{b('对乙酰氨基酚 3000 mg')}",
    f"{b('结局')}：静态股四头肌肌力（拉力计）、动态股四头肌肌力（推算 1RM）、大腿围度（大转子到髌骨尖的中点），在第 0、4、8、12 周测",
]))

A.append(h2("重点：三组的训练方案"))
A.append(img(3))
A.append(cap("三组方案总览（编者根据原文表 1 整理）"))
A.append(table(["", "开链组", "闭链组", "混合链组"], [
    ["第 1 周", "股四头肌等长收缩、空中蹬车", "股四头肌等长收缩、靠墙滑蹲", "直腿抬高、闭链式股四头肌等长收缩"],
    ["第 2 周", "＋直腿抬高", "同上", "＋靠墙滑蹲"],
    ["第 3 周", "直腿抬高改负重", "靠墙滑蹲改负重（哑铃）", "直腿抬高、靠墙滑蹲改负重"],
    ["第 4～5 周", "＋坐位全范围伸膝负重", "同上", "＋坐位全范围伸膝负重"],
    ["第 6 周", "同上", "＋上下台阶", "同上"],
    ["第 7～12 周", "同上", "上下台阶改负重", "同上"],
]))
A.append(tcap("原文表 1：12 周训练进阶（中文翻译，“＋”表示在上一阶段基础上增加）"))
A.append(ul([
    "每个动作 10 次；空中蹬车连续 2 分钟；坐位全范围伸膝 10 次 × 3 组",
    f"负重从{b('10RM')}（能做 10 次的最大重量）开始，{b('每周开始时重测新的 10RM')}加量",
    "靠墙滑蹲用哑铃加负荷",
]))
A.append(pic(4, "原文图 1：负重直腿抬高"))
A.append(pic(5, "原文图 2：坐位全范围伸膝"))
A.append(pic(6, "原文图 3：手持哑铃靠墙滑蹲"))
A.append(pic(7, "原文图 4：负重上下台阶"))

A.append(h2("肌力怎么测"))
A.append(pic(8, "原文图 5、6：静态和动态肌力测试"))
A.append(ul([
    f"{b('静态肌力')}：靠背坐，屈膝 60°，拉力计连在踝上，最大力伸膝不准猛拉；测 2 次（间隔 90 秒）取平均",
    f"{b('动态肌力')}：踝绑一个重量，伸膝到底保持 5 秒再放下，做到力竭；用 {b('Brzycki 公式')} 1RM ＝ 重量 ÷（1.0278 − 0.0278 × 次数）推算",
    "两种肌力都换算成牛顿后再除以体重的 0.67 次方做标准化",
]))

A.append(h2("结果"))
A.append(pic(9, "三组肌力和大腿围度的变化（编者根据原文表 3 重画）"))
A.append(table(["", "开链组", "闭链组", "混合链组", "组间 P"], [
    ["静态肌力 治疗前", "7.02 ± 2.67", "7.26 ± 2.60", "7.46 ± 2.39", ""],
    ["静态肌力 第 12 周", "9.97 ± 2.78", "10.25 ± 3.05", "11.41 ± 2.67", "0.106"],
    ["动态肌力 治疗前", "4.08 ± 0.68", "4.28 ± 0.79", "4.28 ± 0.65", ""],
    ["动态肌力 第 12 周", "4.75 ± 0.88", "5.00 ± 1.10", "5.11 ± 1.16", "0.291"],
    ["大腿围度 治疗前（cm）", "54.90 ± 7.19", "53.19 ± 7.43", "53.63 ± 5.69", ""],
    ["大腿围度 第 12 周（cm）", "55.91 ± 7.01", "54.47 ± 7.30", "55.31 ± 5.70", "0.660"],
]))
A.append(tcap("原文表 3、表 5 节选：三组治疗前和第 12 周的结果（均数 ± 标准差，中文翻译；肌力为标准化值）"))
A.append(ul([
    f"{b('时间效应')}：三组的静态肌力、动态肌力、大腿围度都随时间{b('显著增加')}（P<0.001），第 4、8、12 周每个时间点都比前一个高",
    f"{b('12 周平均增加')}：静态肌力 3.30（约 +45%）、动态肌力 0.74（约 +18%）、大腿围度 1.32 cm",
    f"{b('组间')}：三组之间{mk('没有显著差异')}，组别和时间也没有交互作用——三种方式练肌力效果相当",
    "从数字看混合链组的静态肌力涨得最多（+3.95，其他两组约 +3.0），但没有达到统计学差异",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('没有不训练的对照组')}：作者自己也承认，无法排除安慰剂效应、自然波动和每天 3000 mg 对乙酰氨基酚的影响",
    f"{b('评估者不盲')}：知道分组的人在测肌力，作者只是让一名中立助理录入数据",
    f"{b('退出 17.7%')}：缺失数据用“最后一次测量值”代替，可能低估或扭曲变化",
    f"{b('三组训练量不一样')}：开链组和混合链组后期有 4 个动作，闭链组只有 3 个；作者说三组“强度和进阶相当”，但没有给出训练量的数据",
    f"{b('肌力测量方法比较粗')}：拉力计和由次数推算的 1RM 都不是等速测试；大腿围度会受脂肪影响，增加约 1 cm 不等于肌肉肥大",
    f"{b('只有 K-L 2 级')}：结果不一定适用于更严重的膝骨关节炎",
    "优点：随机分组、样本量事先计算（每组至少 26 人）、按意向性分析、方案逐周写清楚、只用沙袋哑铃等简单器械",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('退出人数加不拢')}：正文说前 4 周退出 13 人，其中“7 人”没说原因（括号里是 3＋3＋2＝{red('8')} 人），另有 5 人因交通/时间退出——8＋5 才是 13；第 8 周又退出 4 人，合计 17 人，与流程图 6／6／5 一致",
    f"{b('表 4 统计量矛盾')}：大腿围度的时间效应 F＝1.864，却写 P<0.001、偏 η²＝0.426——F 值这么小不可能得到这样的 P 值和效应量，F 值可能有漏印",
    f"{b('表 2 统计量矛盾')}：身高 F＝1.466 却对应 P＝0.465（按自由度 2、93 应约为 0.24）",
    f"{b('置信区间不对称')}：表 3 开链组治疗前大腿围度 54.90，95% 置信区间却写 53.31～57.50（中点 55.4），其他格都是对称的",
    f"{b('肌力单位')}：肌力按体重的 0.67 次方标准化后不再是“牛顿”，但表格和摘要仍标“N”，读者容易误以为静态伸膝力只有 7 N",
    f"{b('纳入年龄')}：正文写美国风湿病学会标准“年龄 38 岁以上”，该标准原本是 50 岁以上",
    f"{b('训练频率缺失')}：本文没写每周练几次，只说详见之前的文章",
    f"{b('小错')}：“Tinaka”（应为 Tanaka）、“Statiic”、“Truamatology”；表 1 闭链组“Wall slides with weight (new 10 RM”括号没闭合",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('开链、闭链、混合都能练出股四头肌力量')}：12 周效果相当，可以按患者的疼痛、平衡能力、器械条件和喜好来选",
    f"{b('膝痛明显、站不稳')}的先从开链（等长收缩、直腿抬高、坐位伸膝）开始；{b('能负重、要回归日常活动')}的多加闭链（滑蹲、上台阶）",
    f"{b('混合方案')}在作者之前的文章里止痛效果最好，本研究肌力数字上也略占优，作为默认方案比较稳妥",
    f"{b('要逐周加量')}：每周重测 10RM 再加负荷，这是三组都能涨力量的关键；只做不加量的等长收缩效果有限",
    "器械只需沙袋、哑铃、矮台阶，适合基层和居家",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Olagbegi OM, Adegoke BOA, Odole AC. Effectiveness of three modes of kinetic-chain exercises on quadriceps muscle strength and thigh girth among individuals with knee osteoarthritis. Arch Physiother. 2017;7:9. doi:10.1186/s40945-017-0036-6</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流中文解读：原文图 1～6 引自原文，图中中文标签为编者所加；流程图和结果图由编者根据原文用中文重画，方案卡为编者整理，表格为中文翻译。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「膝骨关节炎」股四头肌怎么练？开链、闭链、两者结合，12 周肌力涨得一样多（附 4 个动作）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>膝骨关节炎动力链训练推文</title>
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
