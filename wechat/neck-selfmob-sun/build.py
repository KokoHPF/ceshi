#!/usr/bin/env python3
"""慢性颈痛运动加颈胸自我松动推文：生成 article_body.html 与 preview.html。

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
    "Sun X, Chai L, Huang Q, Zhou H, Liu H. Effects of exercise combined with cervicothoracic spine self-mobilization on chronic non-specific neck pain. Sci Rep. 2024;14:5298.",
    "作者来自首都体育学院、滇西应用技术大学、北京大学第三医院骨科",
    "单盲随机对照试验，中国临床试验注册号 ChiCTR2300073801",
], square=True))

A.append(h2("先说为什么要连胸椎一起动"))
A.append(p(
    f"慢性非特异性颈痛越来越年轻化，和长时间低头看手机、久坐有关。颈痛的人{b('深层颈屈肌（颈长肌、头长肌）激活延迟')}，"
    "所以压力生物反馈下练深层颈屈肌，是常用的运动方案。"
))
A.append(p(
    f"另一方面，颈椎的活动里本来就包含上胸椎的活动，{b('上胸椎僵硬时颈椎要代偿')}。"
    f"这项研究想看：在练深层颈屈肌和肩胛稳定的基础上，{mk('病人自己用松动带和泡沫轴做颈椎、胸椎的自我松动')}，能不能多一些好处。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：颈后部疼痛 ≥3 个月、疼痛评分 ≥3、近 1 个月没接受过治疗；排除颈椎外伤手术、严重神经根型或脊髓型颈椎病、骨质疏松、肿瘤、心肺疾病",
    f"招募 47 人，最终 {b('30 人')}随机分 3 组，每组 10 人，无失访",
    f"三组都是{b('每周 3 次、每次 40 分钟，共 6 周 18 次')}；第 1 次教会、第 10 次进阶，其余自己练、旁边有人监督",
    "测量：疼痛（0～10）、颈椎 6 个方向活动度、颈部功能障碍指数、深层颈屈肌耐力（压力生物反馈）和力量（手持测力计）、生活质量（SF-36 生理和心理总分）",
]))
A.append(pic(7, "受试者流程"))
A.append(pic(2, "三组方案"))

A.append(h2("重点：三套练法"))
A.append(h3("一、三组共同的运动训练"))
A.append(pic(3, "深层颈屈肌与肩胛稳定"))
A.append(ul([
    f"{b('深层颈屈肌')}：仰卧屈髋屈膝，气囊垫在颈后充到 20 毫米汞柱，做“点头”式的颅颈屈曲；{b('保持 20 秒、休息 10 秒')}，每次目标压力加 2，直到 30 毫米汞柱",
    f"{b('肩胛稳定')}：俯卧、头伸出床外，手臂摆成 {b('W、Y、T')} 慢慢上下；前 3 周每个动作 2 组 × 15 次，后 3 周每组 30 次",
]))
A.append(pic(4, "原文图 1"))

A.append(h3("二、颈椎自我松动（用松动带）"))
A.append(ul([
    f"{b('后伸')}：把折叠的松动带横放在有问题节段的棘突上，双手抓住两端向上拉，带着该节段沿后伸方向滑动",
    f"{b('旋转')}（以右旋为例）：带子放在问题节段棘突上，双手抓两端；{b('左肘顶住椅背')}防止上背跟着转；向右转头时右手拉带子，方向顺着颈椎小关节面；转到末端时{mk('轻度加压，不引起疼痛')}",
]))
A.append(pic(5, "原文图 2"))

A.append(h3("三、胸椎自我松动（用泡沫轴）"))
A.append(ul([
    f"{b('胸椎伸展')}：仰卧，泡沫轴横放在{b('上胸椎')}下面，双臂上举、身体后仰、头朝地面方向；保持 5～10 秒，再把泡沫轴移到下一个节段",
    f"{b('胸椎旋转')}：侧卧屈髋屈膝 90°，上方腿搭在泡沫轴上、下方腿贴床，稳住骨盆和腰；双臂前伸，上方手画最大的圈，胸椎左右交替旋到最大",
    f"{b('祈祷式伸展')}：跪坐，臀部坐在脚跟上，双手伸直放在泡沫轴上，{b('一边慢慢呼气一边让胸口往地面沉')}",
]))
A.append(pic(6, "原文图 3"))

A.append(h2("结果：加松动的两组活动度更好，颈胸一起的最好"))
A.append(pic(8, "主要结果"))
A.append(ul([
    "三组 6 周后疼痛都下降、深层颈屈肌力量和耐力都提高、功能障碍都减轻",
    f"{b('活动度')}：两个自我松动组的后伸、侧屈、旋转改善比运动组好；运动组的左右侧屈、左右旋转其实{b('没有显著变化')}（右旋还从 50.6° 降到 50.1°）",
    f"{b('颈胸自我松动组')}：治疗后疼痛最低（2.3 vs 3.3、3.2），右侧屈最大（46.1° vs 38.6°、41.3°）",
    "深层颈屈肌力量和耐力三组提高幅度一样，加不加松动没影响",
    "生活质量生理总分，颈胸松动组比运动组高",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{red('每组只有 10 人')}，样本量是按 5 人一组的预试验算出来的（效应量 η² = 0.67，非常大），容易高估",
    f"{red('疼痛的组间差别没那么稳')}：时间 × 组别交互作用不显著（P = 0.388），所谓“颈胸组止痛最好”只是治疗后数值的比较",
    "颈胸组多做了一整套胸椎练习，训练量和时间更多，好处可能部分来自“练得更多”",
    "同一位评估者测所有结局，原文没说评估者是否知道分组",
    "只看了 6 周结束时，没有随访",
]))
A.append(p(b("原文里对不上的地方：")))
A.append(ul([
    f"深层颈屈肌耐力测试最高只测到 {b('30 毫米汞柱')}（训练也只练到 30），但治疗后三组平均值是 {red('35～36 毫米汞柱')}，超过了测试上限",
    "生活质量“交互作用不显著（F = 3.648，P = 0.040）”——P = 0.040 其实是显著的",
    "疼痛：正文写颈胸组 vs 颈椎组 d = 1.34，表 2 和摘要写 1.23",
    "颈部功能障碍指数：正文说颈胸组改善“好于”运动组，但 P = 0.122 并不显著",
    f"表 1 力量 t 值：颈椎组印成 2.343（和功能障碍指数同一个数，且符号相反）；颈胸组 t = −16.884 却只有 P = 0.007，运动组 t = −5.681 只有 P = 0.008，t 值和 P 值对不上",
    "表 2 多处置信区间有误：右侧屈、左旋的区间少了负号（“11.08 to −3.99”）；后伸 −0.48 的区间是“−4.38 to 5.34”；生理总分 −0.05（−0.13 至 −0.02）不含 0，P 却是 0.361",
    "功能障碍指数和生活质量的数值（如 0.53、−0.34）用的换算方式不常见，没法和常用的 0～50 分、0～100 分对照",
    "效应量分级用了非常规标准（d ≥ 0.7 就是“非常大”）；招募需 27 人，写“最终招募 47 人”实际纳入 30 人",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"慢性颈痛的底子：{b('压力生物反馈下练深层颈屈肌 + 俯卧 W、Y、T')}，能提高颈屈肌力量耐力、减痛",
    f"如果颈椎侧屈、旋转受限，{mk('加一套自我松动')}：松动带做颈椎后伸和旋转，泡沫轴做胸椎伸展、旋转和祈祷式伸展",
    "自我松动只要一根带子、一个泡沫轴，教会后病人可以在家做；注意末端加压不引起疼痛",
    "做颈椎旋转松动时，用对侧手肘顶住椅背，防止上背代偿",
    "这是 30 人、6 周的小样本研究，结果偏乐观，适合作为“可以试”的选项",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文表 1　三组训练前后结果（均值 ± 标准差）"))
T1 = [("疼痛（0～10）", [("运动", "5.70 ± 2.06", "3.30 ± 0.67", "4.811", "&lt; 0.001"), ("颈椎松动", "5.70 ± 1.70", "3.20 ± 0.63", "5.622", "&lt; 0.001"), ("颈胸松动", "5.80 ± 1.40", "2.30 ± 0.82", "8.720", "&lt; 0.001")]),
      ("前屈活动度（°）", [("运动", "26.52 ± 6.90", "37.20 ± 6.22", "−4.930", "0.001"), ("颈椎松动", "26.76 ± 6.72", "37.40 ± 5.68", "−4.598", "0.001"), ("颈胸松动", "28.70 ± 7.04", "40.34 ± 3.30", "−7.684", "0.000")]),
      ("后伸活动度（°）", [("运动", "39.56 ± 7.50", "44.02 ± 6.89", "−2.869", "0.018"), ("颈椎松动", "42.40 ± 5.80", "52.07 ± 3.64", "−4.583", "0.001"), ("颈胸松动", "42.40 ± 5.79", "51.59 ± 4.87", "−4.364", "0.002")]),
      ("左侧屈活动度（°）", [("运动", "36.27 ± 8.14", "41.33 ± 4.67", "−1.792", "0.107"), ("颈椎松动", "34.37 ± 6.42", "43.51 ± 3.53", "−4.166", "0.002"), ("颈胸松动", "37.92 ± 5.45", "45.76 ± 2.47", "−4.152", "0.002")]),
      ("右侧屈活动度（°）", [("运动", "34.84 ± 8.29", "38.57 ± 4.46", "−1.839", "0.099"), ("颈椎松动", "34.68 ± 7.75", "41.31 ± 3.39", "−3.517", "0.007"), ("颈胸松动", "38.07 ± 6.11", "46.11 ± 4.89", "−4.652", "0.001")]),
      ("左旋活动度（°）", [("运动", "46.32 ± 8.82", "47.25 ± 6.31", "−0.362", "0.726"), ("颈椎松动", "42.63 ± 7.67", "49.41 ± 4.34", "−4.019", "0.003"), ("颈胸松动", "42.75 ± 7.57", "54.72 ± 5.61", "−4.628", "0.001")]),
      ("右旋活动度（°）", [("运动", "50.58 ± 4.40", "50.08 ± 2.51", "0.371", "0.719"), ("颈椎松动", "49.03 ± 6.42", "53.80 ± 3.80", "−3.387", "0.008"), ("颈胸松动", "49.23 ± 6.75", "58.02 ± 6.27", "−3.479", "0.007")]),
      ("深层颈屈肌耐力（毫米汞柱）", [("运动", "24.20 ± 2.74", "35.40 ± 4.22", "−8.806", "&lt; 0.001"), ("颈椎松动", "24.60 ± 2.67", "35.20 ± 3.79", "−9.165", "&lt; 0.001"), ("颈胸松动", "23.20 ± 1.40", "36.20 ± 8.72", "−4.867", "&lt; 0.001")]),
      ("深层颈屈肌力量（牛）", [("运动", "54.70 ± 10.51", "73.50 ± 16.84", "−5.681", "0.008"), ("颈椎松动", "54.20 ± 12.88", "73.30 ± 19.62", "2.343", "0.019"), ("颈胸松动", "56.30 ± 17.23", "78.50 ± 15.63", "−16.884", "0.007")]),
      ("颈部功能障碍指数", [("运动", "0.53 ± 0.14", "0.42 ± 0.07", "2.127", "0.048"), ("颈椎松动", "0.44 ± 0.08", "0.39 ± 0.05", "2.343", "0.044"), ("颈胸松动", "0.45 ± 0.10", "0.36 ± 0.07", "2.234", "0.038")]),
      ("生活质量·生理总分", [("运动", "0.11 ± 0.10", "0.17 ± 0.10", "−1.287", "0.115"), ("颈椎松动", "0.12 ± 0.08", "0.23 ± 0.07", "−3.100", "0.006"), ("颈胸松动", "0.11 ± 0.08", "0.26 ± 0.06", "−4.782", "&lt; 0.001")]),
      ("生活质量·心理总分", [("运动", "−0.34 ± 0.03", "−0.31 ± 0.04", "−1.842", "0.099"), ("颈椎松动", "−0.31 ± 0.04", "−0.20 ± 0.16", "−3.187", "0.011"), ("颈胸松动", "−0.31 ± 0.06", "−0.19 ± 0.16", "−3.609", "0.006")])]
rows = []
for nm, gs in T1:
    for k, g in enumerate(gs): rows.append([nm if k == 0 else "", *g])
A.append(table(["指标", "组别", "训练前", "训练后", "t", "P"], rows))
A.append(tcap("原文表 2　训练后组间比较"))
T2 = [("疼痛", [("1.000", "0.00（−0.83～0.83）", "0.15"), ("0.014", "1.00（0.17～1.83）", "1.34"), ("0.014", "1.00（0.17～1.83）", "1.23")]),
      ("前屈", [("1.000", "−0.20（−6.32～5.92）", "0.03"), ("0.605", "−3.14（−9.26～2.98）", "0.63"), ("0.693", "−2.94（−9.06～3.18）", "0.63")]),
      ("后伸", [("0.006", "−8.05（−12.91～−3.18）", "1.46"), ("0.011", "−7.56（−12.43～−2.70）", "1.27"), ("1.000", "−0.48（−4.38～5.34）", "0.11")]),
      ("左侧屈", [("0.588", "−2.18（−6.36～2.01）", "0.53"), ("0.036", "−4.42（−8.79～−1.06）", "1.19"), ("0.546", "−2.25（−5.61～1.12）", "0.74")]),
      ("右侧屈", [("0.375", "−2.73（−6.29～0.81）", "0.69"), ("0.001", "−7.53（11.08～−3.99）", "1.61"), ("0.030", "−4.80（−8.34～−1.25）", "1.14")]),
      ("左旋", [("1.000", "−2.16（−7.18～2.87）", "0.40"), ("0.015", "−7.47（12.50～−2.44）", "1.25"), ("0.118", "−5.31（−10.34～−0.28）", "1.06")]),
      ("右旋", [("0.224", "−3.71（−7.81～0.40）", "1.16"), ("0.001", "−7.94（−12.04～−3.83）", "1.66"), ("0.131", "−4.23（−8.33～−0.13）", "0.81")]),
      ("颈屈肌耐力", [("1.000", "0.20（−5.31～5.71）", "0.05"), ("1.000", "−0.80（−6.31～4.71）", "0.12"), ("1.000", "−1.00（−6.51～4.51）", "0.15")]),
      ("颈屈肌力量", [("1.000", "0.20（−15.81～16.21）", "0.01"), ("1.000", "−5.0（−21.01～11.01）", "0.31"), ("1.000", "−5.20（−21.21～10.81）", "0.29")]),
      ("功能障碍指数", [("0.922", "0.03（−0.03～0.09）", "0.49"), ("0.122", "0.06（0.00～0.12）", "0.86"), ("0.831", "0.03（−0.02～0.09）", "0.49")]),
      ("生理总分", [("0.361", "−0.05（−0.13～−0.02）", "0.70"), ("0.037", "−0.09（−0.16～−0.02）", "1.09"), ("0.870", "−0.04（−0.11～−0.03）", "0.46")]),
      ("心理总分", [("0.236", "−0.11（−0.23～0.01）", "0.94"), ("0.207", "−0.11（−0.24～0.01）", "1.03"), ("1.000", "−0.00（−0.13～0.12）", "0.06")])]
cmp = ["运动 vs 颈椎松动", "运动 vs 颈胸松动", "颈椎松动 vs 颈胸松动"]
rows = []
for nm, gs in T2:
    for k, (pv, md, d) in enumerate(gs): rows.append([nm if k == 0 else "", cmp[k], md, mk(pv) if float(pv) < 0.05 else pv, d])
A.append(table(["指标", "比较", "均值差（95% 置信区间）", "P", "d"], rows))
A.append(small("置信区间按原文照录（部分区间缺负号或与均值差不一致，见正文）。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Sun X, Chai L, Huang Q, Zhou H, Liu H. Effects of exercise combined with cervicothoracic spine self-mobilization on chronic non-specific neck pain. Sci Rep. 2024;14:5298. doi:10.1038/s41598-024-55181-8</em><br>"
    "原文以知识共享署名 4.0 协议（CC BY 4.0）发表。本文为中文解读，照片引自原文图 1～3（编者加中文标注，压力表品牌与衣服标志已模糊），流程图按原文图 4 重绘为中文，方案卡、训练卡与结果图为编者中文绘制，表格为编者翻译。"
))

TITLE = "「颈痛」练深层颈屈肌之外，再加一套颈胸椎自我松动"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>颈胸自我松动推文</title>
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
