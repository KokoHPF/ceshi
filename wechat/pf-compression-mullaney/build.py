#!/usr/bin/env python3
"""髌股关节压迫问题的最新概念与治疗临床述评（Mullaney、Fukunaga 2016）推文。

用法：python3 build.py   → 生成 article_body.html（上传用正文）和 preview.html（在线预览）
样式全部内联；列表用“•”段落而不是 <ul>，避免公众号编辑器把列表拆乱。
"""
import pathlib

HERE = pathlib.Path(__file__).parent


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
    "Mullaney MJ, Fukunaga T. Current concepts and treatment of patellofemoral compressive issues. Int J Sports Phys Ther. 2016;11(6):891-902.",
    "中文题目：髌股关节压迫性问题的当前概念与治疗",
    "作者来自美国纽约 Nicholas 运动医学与运动创伤研究所、Mullaney & Associates 物理治疗诊所、霍夫斯特拉大学",
    "临床述评（专家意见），不是原始研究",
], square=True))

A.append(h2("研究背景：膝前痛，很多是髌骨被“压”出来的"))
A.append(p(
    f"骨科门诊看的膝伤里，将近 {b('25%')} 是髌股关节问题。髌股痛综合征的年发病率，男性约 3.8%、女性约 6.5%，青少年多在长个子快的时候出现，成年人可能已经合并退变，而且{b('常常迁延不愈')}。"
))
A.append(p(
    f"作者的切入点是{mk('压力')}：髌股关节受压过大，滑膜皱襞、髌下脂肪垫、支持带、关节囊、髌股韧带都可能疼；软骨下骨痛觉感受器多，应力高了也会疼；长期高压还会让软骨退变。"
))
A.append(h3("典型表现"))
A.append(ul([
    f"{b('核心标准')}：髌骨周围或后方疼痛，并且至少一个{b('屈膝负重')}的动作会加重，比如下蹲、上下楼、慢跑/跑步、单腿跳/跳跃",
    f"{b('辅助线索')}：屈膝时有摩擦音、髌骨关节面压痛、髌周少量积液、久坐或起身时痛",
    f"睡觉、站着、休息时（髌股关节不受压）很少疼",
    f"{b('没有一个检查能单独确诊')}。下蹲痛在髌股痛患者里很常见；髌骨边缘压痛的人 71%～75% 有髌股痛，所以{b('触诊髌骨内外侧关节面')}应该常规做；研磨、恐惧试验敏感度低，要谨慎使用",
]))
A.append(pic(2, "原文图 1（加中文说明）"))

A.append(h2("方法：作者怎么拆解这个问题"))
A.append(p("这是一篇述评，作者先讲解剖和力学，再按“找出损害 → 对症处理”的思路，逐项介绍检查和干预手段。"))
A.append(h3("骨和软组织：哪里会让髌骨受压"))
A.append(ul([
    f"{b('髌骨')}：关节面分成内外两大块，外侧面长而斜、内侧面小而陡，所以检查时要把两侧都摸到",
    f"{b('滑车沟')}：深约 5.2 mm，外侧髁比内侧髁高约 3.4 mm；滑车发育不良时沟变浅变平，容易脱位",
    f"{b('内侧')}：内侧髌股韧带是阻止髌骨外移的主要被动结构，它松了会改变髌股压力",
    f"{b('外侧')}：外侧支持带浅、深两层，太紧会把髌骨往外拉、往外倾，{b('外侧关节面压力增大')}，时间长了会退变；髂胫束和外侧支持带连在一起，所以要一起查",
    f"{b('髌下脂肪垫')}：神经很丰富，本身就可能是膝前痛的来源",
]))
A.append(h3("屈膝多少度时压力最大"))
A.append(pic(3, "屈膝角度与髌股压力（编者根据原文整理）"))
A.append(p(
    f"作者综合几项研究：上楼梯时髌股负荷在约 60° 最高；靠墙蹲在 80°～90° 时，脚离墙近的“短距离靠墙蹲”比脚离墙远的压力更大。由此推断{mk('屈膝 60°～90° 是压力最大的区间')}，检查和训练时要留意。"
))

A.append(h3("先找出哪里出了问题"))
A.append(pic(7, "检查和处理一览（编者根据原文整理）"))
A.append(h4("① 髋屈肌、股四头肌"))
A.append(p(
    f"髌股痛患者的股四头肌往往更短；股四头肌紧会把髌骨往滑车里压，髋屈肌紧则带来骨盆前倾、股骨内旋、髌骨轨迹异常，接触面积变小、应力变大。"
))
A.append(ul([
    f"{b('改良 Thomas 试验')}：仰卧在床边，{b('先把对侧腿抱到最大屈髋，让骨盆后倾')}，再放下被测腿，用量角器或电子水平仪量髋角，信度高；同一姿势量膝角可看股直肌",
    f"{b('Ely 试验')}：俯卧被动屈膝，看髋前部是否离开床面（骨盆前倾），可用量角器量膝角或胫骨角，信度中到好",
    f"{b('牵伸')}：Thomas 体位牵伸（对侧腿抱紧）、半跪髋屈肌牵伸、俯卧股四头肌牵伸（大腿远端垫毛巾卷）；{mk('每个牵伸累计至少 4 分钟')}，可以拆成几次",
    "Peeler 等的前瞻性队列研究显示，3 周居家股四头肌牵伸能明显改善髌股痛患者的功能评分",
]))
A.append(pic(4, "原文图 2、3、5、6（加中文说明）"))
A.append(pic(5, "原文图 4（加中文说明）"))
A.append(h4("② 阔筋膜张肌、髂胫束"))
A.append(ul([
    f"病例对照研究里，髌股痛患者 Ober 试验的髋内收角更小；髂胫束紧被认为会把髌骨往外拉、减小接触面积",
    f"{b('Ober 试验')}：侧卧，下面的腿屈髋屈膝并用手抱住、抓住床沿，固定骨盆后倾；被测腿外展、后伸后让它自然下落，在大腿远端放测斜仪，信度很好。{red('Thomas 试验阳性时 Ober 试验不成立')}，因为髋伸不过中立位，髂胫束绕不过大转子，会出现假阴性",
    f"{b('仰卧交叉试验')}：查髂胫束后部（连着臀大肌），屈髋约 70° 后内收到有阻力，骨盆不能侧倾；没有信效度数据，作者只作定性比较两侧",
    f"{b('牵伸')}：Ober 体位治疗师辅助牵伸；仰卧交叉体位用带子或靠墙自我牵伸；站立交叉腿、躯干侧屈，加上手臂动作能拉到整条体侧筋膜线",
]))
A.append(h4("③ 腘绳肌、腓肠肌"))
A.append(ul([
    f"腘绳肌紧理论上会让胫骨近端后移，改变股四头肌拉力方向，增加髌股压力；有生物力学研究显示，腘绳肌短的人下蹲时髌股应力和反作用力更高",
    f"腓肠肌紧可能有类似作用，但{b('没有直接证据')}；它还可能在步行中被足中段代偿，带出更多距下关节、胫骨和股骨旋转",
    f"{b('检查')}：直腿抬高、90/90 伸膝试验（腘绳肌）；{b('Silfverskiöld 试验')}比较屈膝、伸膝时的踝背伸，{mk('相差 ≥ 10° 提示腓肠肌挛缩')}",
    f"{b('牵伸')}：带子直腿抬高，可加“收缩—放松”类本体感觉神经肌肉促进技术提高耐受；腓肠肌站立位牵伸，后脚别外展，必要时穿鞋或垫足弓，防止拉到足中段",
]))
A.append(h4("④ 髌骨活动度"))
A.append(ul([
    f"{b('伸膝位')}检查髌骨上下、内外滑动，内外倾斜和额状面旋转，记录“受限 / 正常 / 过度活动”；常见的是{b('内倾 + 内滑同时受限')}",
    f"{b('只松受限的方向')}，用摆动或静态手法；可以教患者回家自己做，增加剂量；和髂胫束、外侧支持带牵伸一起用效果更好",
    f"不过作者也承认：髌骨松动的有效性证据有限，没有仪器时位置和活动度难以可靠评估，还有横断面研究发现有无髌股痛的人髌骨活动度没差别",
]))
A.append(h4("⑤ 筋膜和触发点"))
A.append(ul([
    "大腿阔筋膜和髂胫束、外侧肌间隔相连，太紧可能把髌骨“绑”得更紧；大腿的活动性触发点也能把痛牵涉到膝周",
    f"{b('检查')}：触诊紧张带里的压痛结节，按压引出局部抽搐或牵涉痛，评估者间信度中等",
    f"{b('处理')}：按压 + 牵伸 + 针对这块肌肉的训练，效果可能与干针相当；泡沫轴、按摩棒在健康人身上能短期增加柔韧性和活动度，器械辅助软组织松动在一项随机试验中优于泡沫轴；但能否持续、能否用到患者身上都不清楚",
]))
A.append(h4("⑥ 力量：髋要练"))
A.append(ul([
    "早在 1976 年 Nicholas 等就发现，髌股问题患者是所有受伤人群里肌肉最弱的，屈髋肌、腘绳肌、股四头肌都弱",
    f"Fukuda 等：常规膝康复{b('加上髋力量训练')}，疼痛、下肢评分和功能测试更好；Dolak 等：先练髋，膝前痛缓解得更快",
    "Khayambashi 等：只练髋外展和髋外旋 8 周，疼痛、功能和髋力量都明显改善",
]))

A.append(h2("结果：唯一的量化数据"))
A.append(p(
    f"述评本身没有新数据。全文最有分量的数字来自作者团队的 Tyler 2006 前瞻性队列：6 周物理治疗后，看三项指标是否恢复：{b('Ober 试验两侧一致')}、{b('Thomas 试验两侧一致')}、{b('手持测力计测屈髋力量提高 20% 以上')}。"
))
A.append(pic(6, "按原文数字重绘"))
A.append(table(["恢复了几项", "治疗成功率"], [
    ["三项都恢复", "93%"],
    ["恢复两项", "75%"],
    ["只恢复一项", "27%"],
]))
A.append(p(f"作者的结论是：{mk('先减压、改善软组织活动性，再加强髋和下肢力量')}，并按患者偏好、治疗师的技能和工具、现有证据来选具体手段。"))

A.append(h2("这些建议能信几分"))
A.append(ul([
    f"{b('专家述评')}：大部分建议是作者的临床做法，没有系统检索，也没有给出证据等级",
    f"{b('核心数据来自作者自己')}：93% / 75% / 27% 出自 Tyler 2006，第一作者 Mullaney 是该研究作者之一；原文没交代样本量和“成功”的定义，属于观察性队列，不能证明是这三项的改善带来了疗效",
    f"{b('“压力”多是理论推导')}：髂胫束、腘绳肌、腓肠肌紧如何增加髌股压力，很多是“理论上”“被认为”，腓肠肌一条作者自己说没有实证",
    f"{b('柔韧性证据多在健康人')}：泡沫轴、器械松动、腘绳肌与髌股应力的研究对象都是健康人",
    f"{b('检查本身有问题')}：Ober 试验的效度被解剖研究质疑，仰卧交叉试验没有信效度数据；髌骨活动度没有仪器难以可靠评估",
    f"{b('角度结论外推')}：60°～90° 压力最大的说法，部分依据来自人工膝关节和教材章节，并非髌股痛患者的测量",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('Witvrouw 研究的随访时间和人群')}：正文说是“一年”、对象是“大学运动员”，引用的文献 26 标题写明是“两年前瞻性研究”，对象是运动人群（体育专业学生）",
    f"{b('把健康人研究算成“患者”')}：正文说腘绳肌紧与髌股压力的关系“得到髌股痛患者横断面研究支持”（文献 25、27、53），其中 53 号 Whyte 2010 的对象是{b('健康成年男性')}",
    f"{b('上楼 60° 压力最大的引用')}：引的 23 号是“非骨水泥全膝置换术后髌骨假体失败”，24 号是生物力学教材章节，都不是髌股痛人群的数据",
    f"{b('发病率引用')}：男 3.8%、女 6.5% 的年发病率引的是 Blond 1998，那是对 250 名运动员的 5.7 年回顾性随访，不是发病率研究",
    f"{b('髋屈肌证据实为股四头肌牵伸')}：说“处理髋屈肌柔韧性与症状改善相关”，引用的 Peeler 2007 是股四头肌静态牵伸研究",
    f"{b('骨盆前倾的引用')}：髋屈肌紧导致骨盆前倾、股骨内旋，引的 29 号 Bazett-Jones 2013 研究的是力竭跑后髌股痛患者的力量和力学",
    f"{b('Dolak 研究的对照组')}：正文说对照是“标准膝康复”，文献标题写的对照是股四头肌力量训练（先练髋 vs 先练股四头肌）",
    f"{b('Walsh 章节标题')}：17 号文献题为“成人膝关节复发性脱位”，引用内容是髌骨和滑车解剖，疑为“髌骨”误作“膝关节”",
    f"{b('拼写和格式问题')}：rentinaculae、trochlear grove、gastrocnenimus、Witvrow、can be assumes；文献 42 作者写成“Mc CJ”（应为 McConnell J），61 写成“S. Wendell Holmes J, William G. Clancy J”，69 把 Mullaley 拼错",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先定位：屈膝负重痛 + 关节面压痛')}，别指望单个特殊试验确诊；研磨、恐惧试验参考价值有限",
    f"{b('固定一套柔韧性检查')}：改良 Thomas（对侧腿抱紧）、Ely、Ober（先确认 Thomas 阴性）、仰卧交叉、直腿抬高、Silfverskiöld，左右比较、量角度、记数字",
    f"{b('牵伸要够量')}：每个部位累计至少 4 分钟；腓肠肌牵伸防足中段代偿",
    f"{b('髌骨松动只做受限方向')}，常见内倾 + 内滑；可以教患者自己做",
    f"{b('训练时留意 60°～90°')}：急性期少做深蹲、短距离靠墙蹲，先在压力小的角度练",
    f"{b('别漏了髋')}：外展、外旋、屈髋力量都要练，用手持测力计跟踪；Ober、Thomas 两侧一致加屈髋力量提高 20% 可以作为阶段目标",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Mullaney MJ, Fukunaga T. Current concepts and treatment of patellofemoral compressive issues. Int J Sports Phys Ther. 2016;11(6):891-902.</em><br>"
    "原文 PDF 未标注开放许可协议。本文为学术交流用的中文解读：照片引自原文图 1～6（编者加中文说明），屈膝角度示意图和检查处理一览为编者根据原文绘制，成功率图按原文数字重绘。版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「膝关节」膝前痛反复不好？髌股关节压迫性问题的评估与治疗全解析"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>髌股压迫推文</title>
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
