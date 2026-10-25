#!/usr/bin/env python3
"""Jorge 等 2024《三种腘绳肌强化训练与冲刺的肌肉活动和运动学比较：一项横断面研究》（IJSPT）推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
配图：python3 tools/make_figs.py src images <中文字体>
（原文图 3～5 是位图，已用 tools/fig-translate 走位图路线译成中文，结果在 src/fig3_zh.png 等，译文和版式在 fig_translate/；原文图 1 是照片，只加中文图注）
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
    "Jorge A, Lichtenstein E, Faude O, Roth R. Muscle Activity and Kinematics During Three Hamstring Strengthening Exercises "
    "Compared to Sprinting: A Cross-Sectional Study. Int J Sports Phys Ther. 2024;19(5):569-580. doi:10.26603/001c.116158",
    "中文题目：三种腘绳肌强化训练与冲刺跑的肌肉活动和运动学比较：一项横断面研究",
    "作者单位：瑞士巴塞尔大学运动、锻炼与健康系",
    f"研究类型：{b('实验室横断面研究')}（同一批人做冲刺和全部动作，原文标 3b 级证据）",
], square=True))

A.append(h2("先说为什么要读这篇"))
A.append(p(
    f"腘绳肌拉伤多发生在接近最高速度的冲刺中，约 {b('70%')} 伤在{b('股二头肌长头')}，"
    "最危险的时刻是摆动末期：腘绳肌被拉到最长、又要用力刹住往前甩的小腿。"
))
A.append(p(
    f"北欧挺能把腘绳肌拉伤减少约一半，是预防方案的标配。但它有两个常被提到的短板：一是{b('以膝为主')}，"
    f"多数研究里练得更多的是{b('半腱肌')}而不是最常伤的股二头肌长头；二是姿势和冲刺差得远，力量能不能转到冲刺上存疑。"
))
A.append(p(
    f"功能磁共振研究提示，{b('以伸髋为主')}的动作可能更多动用股二头肌长头。这篇就挑了两个以髋为主的闭链动作，"
    f"和北欧挺放在一起，{mk('以最大冲刺的肌电为 100%')}，看谁的激活和关节角度更像冲刺。"
))
A.append(p("作者的三个假设："))
A.append(ul([
    "以髋为主的动作，股二头肌长头激活比以膝为主的北欧挺高",
    "股二头肌长头 / 半腱肌的激活比值会随“髋主导还是膝主导”而不同",
    "所有动作对腘绳肌的拉长程度都比高速跑小",
]))

A.append(h2("研究怎么做"))
A.append(img(3))
A.append(ul([
    f"{b('8 名男性业余运动员')}，平均 24.0 岁，身高 1.79 m，最大冲刺速度 31.9 km/h；2022 年 12 月至 2023 年 9 月方便抽样招募",
    "测试日先在室外跑道做 2 次 40 m 全力冲刺，取肌电较大的一次作为 100% 参照",
    f"“高速跑”是在电动跑台上以最大冲刺速度的 {b('75%')}（约 23.9 km/h）跑，同时做三维动作捕捉；作者引用文献认为这是 15 步内不走形的最快速度",
    "4 个动作随机顺序，各做 3 次，每次间隔 5 分钟；做完用 Borg CR10 量表确认恢复后再做下一个",
    "统计用线性混合模型（每人一个随机截距），效应量按跑台跑的标准差标准化",
]))

A.append(h2("三个动作怎么做"))
A.append(img(2))
A.append(h4("① 杠杆髋伸器（Rocker）"))
A.append(p(
    "瑞士国家级田径运动员在用的自制器械。髋部固定在器械上，右脚踩在 42 cm 高、铺了平衡垫的台子上，"
    f"{b('单腿伸髋')}把身体和器械一起顶起来，要求“尽量高、尽量爆发”。它是一个二类杠杆，支点越往头侧阻力越大；"
    "熟悉课里给每人定到“连做 3 次速度不明显下降、不走形”的最大档位。"
))
A.append(h4("② 球上单腿髋伸（Perpetuum mobile，PM）"))
A.append(p(
    "来自物理治疗（Klein-Vogelbach 体系），原本用来练步态里的髋稳定和推进。仰卧，右小腿搭在 53 cm 的瑜伽球上，"
    "髋和左腿离地，双臂撑地。起始时球拉到靠近臀部，"
    f"伸髋把球往脚的方向滚出去，同时左腿屈髋屈膝，模仿跑步的摆动腿。分两种做法：{b('PM快')}（向心阶段爆发式）和 {b('PM慢')}（每个阶段 5 秒，节拍器控制）。"
))
A.append(h4("③ 北欧挺（NHE）"))
A.append(p(
    "跪在可调坡度的板上，脚踝固定，双手抱胸，保持伸髋向前倒，"
    f"{b('只做下放（离心）')}，5 秒落地。坡度按“刚好能做 3 次全程不失控”来调，所以每个人北欧挺的难度不同。"
))

A.append(h2("结果一：谁的激活最高"))
A.append(img(4))
A.append(p(
    f"峰值激活上，四个动作的腘绳肌大多{b('接近或超过最大冲刺')}；杠杆髋伸的股二头肌长头达到冲刺的 {b('132%')}。"
    f"差距主要在{b('平均激活')}上："
))
A.append(img(5))
A.append(ul([
    f"{b('杠杆髋伸')}最高：平均激活明显高于其他所有动作，峰值激活高于 PM慢、北欧挺和跑台跑",
    f"{b('PM快')}其次：高于 PM慢、北欧挺和跑台跑",
    f"{b('北欧挺和 PM慢')}与跑台跑相当，平均只有冲刺的三成多；北欧挺是“峰值高、平均低”",
    f"{b('臀大肌')}：杠杆髋伸、PM快和跑台跑的峰值都明显高于北欧挺；臀大肌个体差异很大（置信区间很宽）",
    f"{b('腓肠肌')}：所有动作都明显低于跑台跑",
]))
A.append(tcap("表 2　腘绳肌肌电（以最大冲刺为 1，均值及 95% 置信区间，编者翻译）"))
A.append(table(["动作", "峰值 股二头肌长头", "峰值 半腱肌", "平均 股二头肌长头", "平均 半腱肌"], [
    ["杠杆髋伸", "1.32（1.05～1.59）*", "1.04（0.90～1.17）", "0.70（0.56～0.84）", "0.58（0.51～0.65）"],
    ["PM快", "1.11（0.91～1.32）", "0.90（0.72～1.07）", "0.54（0.39～0.68）", "0.44（0.32～0.57）"],
    ["PM慢", "0.89（0.69～1.09）", "0.80（0.58～1.01）", "0.35（0.25～0.44）", "0.30（0.22～0.37）"],
    ["北欧挺", "0.99（0.72～1.26）", "0.79（0.65～0.94）*", "0.36（0.26～0.45）", "0.32（0.26～0.39）"],
    ["跑台跑", "0.80（0.65～0.95）*", "0.78（0.59～0.96）*", "0.30（0.23～0.37）", "0.28（0.22～0.35）"],
]))
A.append(small("* 峰值与最大冲刺有统计学差异"))
A.append(p(
    f"作者的解释：杠杆髋伸有额外负荷；爆发式动作向心阶段短，平均值接近峰值，慢动作收缩时间长、起伏大，平均值就被拉低；"
    "北欧挺开头那段负荷很小，也拉低了平均值。"
))

A.append(h2("结果二：股二头肌还是半腱肌"))
A.append(img(6))
A.append(ul([
    f"所有动作合起来看，{b('股二头肌长头都比半腱肌更活跃')}：峰值高 0.16（95% CI 0.07～0.26），平均高 0.06（0.01～0.11）",
    f"但比值在{b('各动作之间没有差异')}，北欧挺的均值也大于 1。也就是说，{mk('“髋主导练股二头肌、膝主导练半腱肌”在这里没有得到证实')}",
    "个体差异很大：同一个动作，有人比值 0.6，有人超过 2",
]))
A.append(p(
    "北欧挺这次也偏向股二头肌，和多数研究不同。作者认为和做法有关：坡度调到“3 次不失控”，起始膝屈平均只有 81.5°，"
    f"幅度短、没有“撑不住的断点”。有研究发现半腱肌在北欧挺前段更活跃、越接近伸直股二头肌占比越高，"
    f"所以作者建议{b('北欧挺要全程、不失控地做')}。"
))

A.append(h2("结果三：峰值出现在什么角度"))
A.append(img(7))
A.append(tcap("表 3　腘绳肌激活峰值时的髋、膝屈曲角度和拉长应力（°，均值及 95% 置信区间，编者翻译）"))
A.append(table(["动作", "髋屈角", "膝屈角", "拉长应力"], [
    ["杠杆髋伸", "44（35～52）*", "69（59～79）†", "−25（−35～−16）"],
    ["PM快", "24（8～40）", "49（34～65）", "−25（−29～−22）"],
    ["PM慢", "20（4～37）", "42（23～61）†", "−22（−26～−18）"],
    ["北欧挺", "24（20～29）", "50（39～61）", "−26（−34～−18）"],
    ["跑台跑", "58（52～65）***", "56（45～66）", "3（−3～9）***"],
]))
A.append(small("拉长应力 = 髋屈角减膝屈角，越大说明腘绳肌越被拉长。* 与其余不同；† 两者之间不同（p &lt; 0.05）"))
A.append(ul([
    f"跑台跑的髋屈最大（58°），其次是杠杆髋伸（44°），其余三个动作只有 20°～24°",
    "膝角只有杠杆髋伸和 PM慢之间有差异（差 27°）",
    f"{b('拉长应力：所有动作都是负值（约 −25），明显小于跑台跑')}，也就是说峰值都出现在腘绳肌比较短的位置",
    "作者认为 PM快和北欧挺的髋、膝角度组合和高速跑的摆动末期相近；杠杆髋伸峰值出现在动作初段、膝屈偏多，把起始膝角放得更直可能更好",
]))

A.append(h2("讨论里说了什么"))
A.append(ul([
    f"{b('闭链、以髋为主的爆发式动作值得重视')}：前人研究的仰卧踢腿（爆发式单腿臀桥）没加负荷，也是激活最高的动作之一，和本研究方向一致",
    f"{b('臀大肌差异大')}：动作对多数人是新的，可能各用各的发力策略；伸髋可以靠臀大肌，也可以少用臀大肌",
    f"{b('75% 速度的跑台跑激活偏低')}：另一项研究同样 75% 速度时腘绳肌激活就超过最大用力的动作，本研究没有重复出来。"
    "作者推测速度超过约 26 km/h 后腘绳肌负荷会成倍增加，75% 速度可能并不能代表最大冲刺",
    f"{b('从拉长角度看，这几个动作（包括北欧挺）都不利于降低拉伤风险')}：预防需要把腘绳肌拉过最适长度、促使肌束变长，"
    "而这几个动作峰值都在短位；纯向心训练甚至可能让肌纤维变短",
    "作者自认的局限：单通道表面肌电只代表肌肉一小块区域，还有串扰；肌电不等于肌力；为统一强度给每人调负荷，反而可能增加了角度和激活的变异",
]))

A.append(h2("这篇能信几分"))
A.append(ul([
    f"{b('样本只有 8 人')}：全是年轻男性业余运动员，置信区间很宽（臀大肌尤其明显）；作者报告“事后功效 > 0.92”，但事后功效本身说明不了什么，8 个人能检出的只是很大的差异",
    f"{b('“冲刺”参照有两套')}：100% 用的是室外 40 m 全力冲刺，运动学却只在跑台 75% 速度下测，最大冲刺时的角度和拉长应力其实没测到，作者自己也说 75% 速度可能不够代表",
    f"{b('负荷各不相同')}：杠杆档位、北欧挺坡度都按个人调，PM 没有外加负荷，比较的其实是“各自那套做法”，不是动作本身",
    f"{b('熟练度不一')}：杠杆髋伸和 PM 对多数人是新动作，只熟悉了一次",
    f"{b('肌电高 ≠ 训练效果好')}：作者在“实际应用”里也承认，目前没有证据表明这些动作能带来冲刺专项的适应或降低拉伤风险；"
    "可同一段又说这些动作“可以用到很早的治疗阶段”，本研究没有任何患者数据支持这一点",
    "优点：同一批人同时测肌电和三维运动学，把“激活多高”和“在什么角度激活”放在一起看；拉长应力这个简单指标对选动作很有提醒意义",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('体重')}：摘要写 76.8 ± 7.7 kg，表 1 写 76.3 ± 7.7 kg",
    f"{b('北欧挺峰值髋角')}：讨论写 26°（95% CI 18.8°～33.3°），表 3 和图 4 都是 24°（20～29）",
    f"{b('“三个髋主导动作”到底是哪三个')}：引言说研究“两个髋主导动作”再加北欧挺；摘要和研究目的写“比较三个髋主导动作：杠杆髋伸、PM快和 PM慢、北欧挺”，"
    "把以膝为主的北欧挺也算了进去，而假设 1 又明确把北欧挺称为膝主导动作；讨论里“三个髋主导动作中有两个的股二头肌激活高于北欧挺”，又是把 PM快、PM慢算成两个",
    f"{b('臀大肌“高于冲刺”')}：摘要说杠杆髋伸和 PM快的臀大肌激活高于冲刺，但结果部分没有报告和冲刺的比较；"
    "图 3 里这两个动作峰值的置信区间下限约 80% 和 58%，都跨过 100%，平均激活则全部低于冲刺。摘要说杠杆髋伸“臀大肌最高”，结果里它和 PM快、跑台跑之间也没有差异",
    f"{b('训练量和纳入标准')}：纳入要求每周冲刺相关训练超过 4.5 小时，表 1 却是 5.0 ± 1.8 小时。8 个人如果都不少于 4.5 小时、均值 5.0，标准差最多约 1.4，"
    "所以至少有人目前每周不到 4.5 小时（除非标准指的是过去某一年）",
    f"{b('慢动作的平均激活范围')}：讨论说北欧挺平均激活为冲刺的 26%～40%、PM慢 25%～39%，和表 2 对不上（北欧挺均值 32%～36%、置信区间 26%～45%；PM慢均值 30%～35%、置信区间 22%～44%）",
    f"{b('占位符没删')}：讨论第一段“峰值都出现在腘绳肌较短的位置（range）”，括号里的 range 应该是要填具体范围",
    f"{b('测了几块肌肉')}：研究设计一段说测的是股二头肌和半腱肌，实际测了 4 块（还有臀大肌和腓肠肌）",
    f"{b('笔误')}：图 3 图注写“peak (1A) und average (1B)”，und 是德语、面板号也写错了；同一图注把腓肠肌内侧头写成“gastrocnemius medius”（方法里是 medialis）；表 1“Verlocity”应为 Velocity",
    f"{b('许可声明自相矛盾')}：文末写“Creative Commons Attribution 4.0 International License（CCBY-NC-4.0）”，前者是 CC BY 4.0，括号和链接却是 CC BY-NC 4.0（非商业），两者不是同一个协议，本文按更严格的 CC BY-NC 4.0 处理",
]))

A.append(h2("落到临床"))
A.append(img(8))
A.append(cap("临床要点（编者整理）"))
A.append(ul([
    f"{mk('想要高激活')}：杠杆髋伸、爆发式球上单腿髋伸的平均激活明显高于北欧挺，可以作为北欧挺之外的补充；没有器械时，爆发式单腿臀桥类动作是现成的替代",
    f"{b('北欧挺尽量全程做')}：短幅度、坡度调低的北欧挺更像“峰值高、平均低”，全程不失控可能更能练到股二头肌长头",
    f"{b('髋主导和膝主导搭配')}：“髋主导专练股二头肌”在本研究没有得到证实，比值个体差异大，两类都练更稳妥",
    f"{b('别忘了长位')}：这些动作峰值都在腘绳肌短位，想练长位离心，还要配合全程北欧挺、髋屈位的离心动作和逐步加量的高速跑（编者补充）",
    "这是 8 个人的一次性肌电测量，不是训练研究；把杠杆髋伸、PM 当作“预防拉伤动作”之前，还需要训练和损伤数据",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Jorge A, Lichtenstein E, Faude O, Roth R. Muscle Activity and Kinematics During Three Hamstring Strengthening Exercises "
    "Compared to Sprinting: A Cross-Sectional Study. Int J Sports Phys Ther. 2024;19(5):569-580. doi:10.26603/001c.116158</em><br>"
    "原文 © The Author(s)，按知识共享署名—非商业性使用 4.0 国际协议（CC BY-NC 4.0，https://creativecommons.org/licenses/by-nc/4.0）开放获取"
    "（原文声明同时写了“CC BY 4.0”的名称，此处按更严格的非商业协议处理）。"
    "本文为非商业学术交流用的中文解读，对原文作了改编：照片引自原文图 1（编者加中文图注）；原文图 3～5 中的英文由编者译成中文覆盖原位置（肌肉缩写保留原文）；"
    "表格为编者翻译；首图、研究流程卡、平均激活重绘图和临床要点卡为编者根据原文整理。仅供学习交流，如有侵权请联系删除。"
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


TITLE = "「腘绳肌训练」北欧挺之外练什么？两个以髋为主的爆发式动作，平均激活比北欧挺高，但都练不到冲刺时的长度"

BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>腘绳肌训练与冲刺推文</title>
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
