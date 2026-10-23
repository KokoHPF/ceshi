#!/usr/bin/env python3
"""Selhorst 等 2020 IJSPT 青少年运动员腰椎峡部裂的康复考量推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
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
    "Selhorst M, Allen M, McHugh R, MacDonald J. Rehabilitation considerations for spondylolysis in the youth athlete. Int J Sports Phys Ther. 2020;15(2):287-300. doi:10.26603/ijspt20200287",
    "中文题目：青少年运动员腰椎峡部裂的康复考量",
    "作者来自美国俄亥俄州 Nationwide 儿童医院运动与骨科物理治疗科、运动医学科，以及辛辛那提儿童医院医学中心",
    "文章类型：临床述评（Clinical Commentary），证据等级 5",
], square=True))

A.append(h2("研究背景：青少年运动员腰痛，最常见的明确病因"))
A.append(ul([
    f"一半青少年有过腰痛，参加运动的更多；青少年运动员腰痛最常见的{b('可明确病因')}是峡部型峡部裂，即椎弓峡部的骨应力损伤",
    "以往研究集中在诊断、影像愈合、支具和休息，物理治疗虽然常被推荐，却{0}，也没有详细的治疗描述".format(b('没有一项随机对照试验')),
    f"{b('述评目的')}：简述峡部裂的病理，并详细提出一套青少年运动员峡部裂的物理治疗方案",
]))
A.append(pic(2, "编者根据原文整理"))
A.append(pic(3, "原文图 1、2（图 1 中的英文由编者译成中文覆盖）"))

A.append(h2("方法"))
A.append(ul([
    f"这是一篇{b('专家述评')}：作者结合峡部裂相关文献、成人峡部裂和腰痛的证据、腰痛临床实践指南以及自身经验，提出三期康复框架",
    "按“背景 → 影像和结局指标 → 休息、支具和预后 → 心理社会因素 → 物理治疗依据 → 三期方案”的顺序展开",
    "方案按标准进阶而不是按时间，每期给出目标、肌肉表现、活动度、测试和进入下一期的标准（原文表 1）",
]))

A.append(h2("结果：作者的主要观点"))
A.append(h3("一、结局指标"))
A.append(ul([
    f"Oswestry 和 Roland-Morris 对功能好的青少年运动员有{b('地板效应')}；这些孩子日常生活很快就没问题，难的是跑、跳和专项动作",
    f"推荐 {b('Micheli 功能量表（MFS）')}：专为青少年运动员腰痛设计，内部一致性 α = 0.90，与 Oswestry 有同时效度，但最小临床重要差值尚未确定",
]))
A.append(h3("二、休息、支具和预后"))
A.append(ul([
    f"{b('先保守')}：绝大多数可以保守治愈；至少 6 个月系统治疗无效才考虑手术（直接修复或间接复位加压）",
    f"{b('休息')}：一般建议停专项运动至少 3 个月；但一项回顾性研究显示，更早开始物理治疗的患者回场更快。作者主张诊断后{b('几周内')}就开始有监督的训练",
    f"{b('支具')}：荟萃分析显示支具不影响临床结局，也不能预测长期运动参与、复发或主观结局；作者不建议常规使用，留给症状不改善的患者",
    f"{b('预后')}：保守治疗后 {b('92%')} 能在 6 个月内回场且基本不痛；但 1.5～8 年随访中 45%～51% 腰痛再次影响活动，18%～40% 因疼痛减少或停止运动",
    f"{b('骨愈合')}：荟萃分析中只有 28% 的病灶影像愈合，单侧 71%、双侧 18%，急性期 68%，终末期不愈合；而{b('影像愈合与生活质量和回场都无关')}，反应良好的患者不建议复查影像",
]))
A.append(pic(4, "编者根据原文整理"))
A.append(h3("三、心理社会因素"))
A.append(ul([
    "孩子常要停赛数月，可能出现失落、自尊下降、焦虑、挫败、孤立和抑郁；良好的医患沟通本身就是社会支持",
    f"孩子容易把自己的腰理解成“断了”，增加对活动和再受伤的恐惧；要告诉他们这是骨应力损伤，{b('腰没有断')}，并强调完全回场的可能性很高",
]))
A.append(h3("四、为什么这样练"))
A.append(ul([
    "峡部裂会造成节段性不稳（平移和旋转增加）；一项成人峡部裂/滑脱的随机对照试验中，针对深层腹肌和多裂肌的训练优于一般训练",
    f"三个原则：第一，这是{b('正在愈合的骨应力损伤')}，第一期在静态中立位练；第二，症状改善后{b('要主动练后伸和旋转')}，而不是一直回避，因为专项离不开这些动作；第三，运动员用的是全身，其他部位的问题会增加腰椎负荷",
    "躯干肌分为负责节段稳定的局部肌系统和负责产生动作的整体肌系统（原文表 2）",
]))
A.append(h3("五、三期康复方案"))
A.append(pic(5, "原文表 1（编者译成中文）"))
A.append(ul([
    f"{b('第一期·孤立训练')}：先建立“活动有益”的信念；中立位、无痛范围内练局部肌，逐步加上四肢活动；年龄小的孩子可用半泡沫轴或毛巾卷放在背上或腹部做外部反馈，嫌简单就加不稳定面；被动治疗少用，{b('不做腰椎高速推拿')}",
    "第一期也要查髋屈肌和腘绳肌柔韧性，拉伸时保持脊柱中立；还要找专项中的其他问题，比如投手胸椎旋转和肩外旋不足会让腰代偿",
    f"{b('第一期出期')}：腹横肌压力生物反馈“良好”、多裂肌抬臂试验收缩正常、反复屈伸腰无痛；用倾角计测腰椎活动度应达正常",
    f"{b('第二期·整合训练')}：从有支撑的静态体位进阶到无支撑、直立、多平面的动态练习，包括末端范围的脊柱运动；加入离心力量和发力训练，不忘髋、肩胛胸壁和肩部力量",
    f"{b('第二期出期')}：俯卧双腿抬起 > 30 秒、仰卧双腿下放 < 70°、侧桥计时，各方向腰椎活动无痛，MFS 的 B、C 部分接近 0 分",
    f"{b('第三期·回归运动')}：在家长、教练和队医配合下分级回归训练和比赛；提高有氧能力、耐力和专项力量；每周 1～2 小时的治疗远不够，要建立出院后的训练和自我管理",
    f"{b('出院标准')}：全量全强度专项动作流畅、无痛恢复伤前水平、MFS 0 分",
]))
A.append(pic(6, "原文图 3、4（照片为原图，图注编者译成中文）"))
A.append(pic(7, "原文图 5、6（照片为原图，图注编者译成中文）"))

A.append(h2("作者怎么解读"))
A.append(ul([
    "峡部裂保守治疗的证据在增加，物理治疗也常被推荐，这篇述评为分期实施物理治疗提供了急需的指导",
    f"作者坦言，建议{b('主要基于专家意见')}和从相似人群推广的研究，但能帮助建立安全有效的治疗方法，也可作为今后研究的框架",
]))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{b('证据等级 5')}：专家述评，没有系统检索，方案本身没有经过试验验证",
    f"{b('核心依据来自成人')}：“练深层肌优于一般训练”来自一项成人慢性腰痛合并峡部裂/滑脱的随机对照试验，青少年急性峡部裂是否同样适用并不确定",
    f"{b('“早开始训练”证据薄弱')}：依据是作者团队自己的一项回顾性病历研究，有选择偏倚",
    f"{b('出期标准多为经验值')}：俯卧双腿抬起 > 30 秒、仰卧双腿下放 < 70° 等阈值正文没有给出处；MFS 的最小临床重要差值也未确定",
    f"{b('实用价值高')}：不按时间、按功能标准进阶，把宣教、心理和全身动力链都纳入，和当前青少年运动损伤康复的思路一致",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('表 2 的出处标错了')}：表 2 标注“改编自 Hoogenboom 和 Kiesel³¹”，但文献 31 是 Kobayashi 等的 MRI 诊断研究，Hoogenboom 和 Kiesel 是文献 85",
    f"{b('腹横肌“良好”标准的出处')}：正文把“4 mmHg 下降保持至少 10 秒”引自文献 72，而文献 72 是关于儿童正常和峡部裂脊柱运动瞬时旋转轴的研究",
    f"{b('“> 10 秒”还是“≥ 10 秒”')}：表 1 写“> 10 秒”，图 3 说明写“10 秒或以上”",
    f"{b('图 2 不是 X 线片')}：图注写“radiographic image”，但图像是 CT 横断面",
    f"{b('仰卧双腿下放 < 70° 的量法没说清')}：图 6 说明记录腰离床时的位置，但没说明角度是腿与床面还是与垂直线的夹角",
    f"{b('表 2 有肌肉两边都列')}：腰大肌（后部/前部）、髋旋转肌和髋外展肌同时出现在局部和整体两栏，作者用星号注明存在争议",
    f"{b('休息建议前后有张力')}：一边说“建议停专项至少 3 个月”，一边主张诊断后几周内就开始训练；两者并不矛盾（停专项不等于不训练），但原文没有说明训练期间专项要停多久",
]))

A.append(h2("落到临床"))
A.append(pic(8, "编者整理"))
A.append(ul([
    f"{mk('怀疑就拍片')}：青少年运动员后伸加重的局限性腰痛，体检分不出来，先正侧位 X 线，早期加 MRI",
    f"{b('第一次见面先做宣教')}：腰没有断、预后好、要保持活动，减少恐惧回避",
    f"{b('不必等骨愈合')}：按功能标准进阶，单侧、急性期更可能愈合，但愈合与否不决定能否回场",
    f"{b('第一期就测、按测进阶')}：压力生物反馈测腹横肌，多裂肌抬臂试验，再到俯卧双腿抬起、仰卧双腿下放和侧桥",
    f"{b('后伸和旋转要练回来')}：第二期起逐步加入，配合髋、胸椎和肩的活动度和力量，减少专项中腰椎的代偿",
    f"{b('长期随访')}：近一半在数年内会复发，出院时要给好自我训练计划，并和教练、家长沟通训练量",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　青少年峡部裂运动员的物理治疗"))
A.append(table(["项目", "第一期　孤立训练", "第二期　整合训练", "第三期　回归运动训练"], [
    ["目标", "1. 宣教，减少灾难化和恐惧回避信念<br>2. 鼓励参与日常生活活动<br>3. 启动局部肌系统<br>4. 改善活动受限<br>5. 减轻疼痛",
     "1. 整合局部肌与整体肌系统<br>2. 开始站立平衡/动态活动<br>3. 提高孤立肌群的耐力<br>4. 获得满足运动需求的柔韧性/活动度和力量<br>5. 促进功能活动中可控的脊柱运动",
     "1. 渐进回归运动<br>2. 最大化专项力量和耐力<br>3. 保证专项动态活动中的核心控制<br>4. 建立合理的训练计划和出院后的自我管理"],
    ["肌肉表现", "· 以核心局部肌为主<br>· 四肢活动时保持脊柱静态稳定<br>· 低负荷、脊柱有支撑的体位",
     "· 整合局部和整体肌群<br>· 脊柱运动中保持稳定<br>· 单平面进阶到多平面<br>· 直立功能位的核心控制", "· 动态专项/位置练习<br>· 专项训练逐步增加强度和量<br>· 在监控下分级回归训练和比赛"],
    ["活动度", "· 在疼痛最小的范围内逐步增加脊柱活动<br>· 避免失控的脊柱运动<br>· 必要时改善柔韧性<br>· 促进正常的腰盆节律",
     "· 保证专项所需的上肢、下肢和躯干活动度及柔韧性<br>· 继续促进正常的腰盆节律", "（与上栏合并）"],
    ["测试/评估", "· 腹横肌激活（俯卧压力生物反馈）<br>· 俯卧多裂肌抬臂试验<br>· 上下肢力量/柔韧性<br>· 躯干活动（质和量）<br>· Micheli 功能量表",
     "· 俯卧双腿抬起<br>· 仰卧双腿下放<br>· 观察异常运动（必要时）<br>· 上下肢力量/柔韧性<br>· Micheli 功能量表",
     "· 模拟专项时的生物力学<br>· 回归过程中的症状和表现<br>· Micheli 功能量表"],
    ["进入下一期的标准", "1. 腹横肌激活“良好”、无代偿：俯卧压力生物反馈下降 4 mmHg 保持 > 10 秒<br>2. 俯卧多裂肌抬臂试验收缩正常<br>3. 反复屈伸腰椎无痛（10 次）",
     "1. 整体肌表现良好（俯卧双腿抬起 > 30 秒，仰卧双腿下放 < 70°）<br>2. 各平面躯干主动活动完整、无代偿<br>3. 专项动力链的柔韧性/活动度和力量足够<br>4. Micheli 功能量表 B、C 部分 0 分",
     "出院标准：<br>1. 全量、全强度专项动作中力学流畅<br>2. 无痛恢复伤前竞技水平<br>3. Micheli 功能量表 0 分"],
], first_bold=True))
A.append(small("注：缩写 ROM 活动度；UE 上肢；LE 下肢；TA 腹横肌；MT 多裂肌。原表第二、三期的“肌肉表现”和“活动度”两行在第三期合并为一格。"))
A.append(tcap("表 2　核心的局部肌系统和整体肌系统（原文标注改编自 Hoogenboom 和 Kiesel）"))
A.append(table(["局部肌系统", "整体肌系统"], [
    ["多裂肌", "腹直肌"], ["腹横肌", "腹外斜肌"], ["腰方肌（内侧部）", "腹内斜肌（前部纤维）"], ["膈肌", "最长肌和髂肋肌（胸段）"],
    ["腹内斜肌（后部纤维）", "腰方肌（外侧部）"], ["横突间肌和棘间肌", "背阔肌"], ["髂肋肌和最长肌（腰段）", "髂肌"],
    ["腰大肌（后部）", "腰大肌（前部）"], ["髋旋转肌*", "髋伸肌和内收肌"], ["髋外展肌*", "腘绳肌和股四头肌"], ["", "髋旋转肌*"], ["", "髋外展肌*"],
], first_bold=False))
A.append(small("注：* 这些肌肉属于局部还是整体肌系统存在争议。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Selhorst M, Allen M, McHugh R, MacDonald J. Rehabilitation considerations for spondylolysis in the youth athlete. Int J Sports Phys Ther. 2020;15(2):287-300. doi:10.26603/ijspt20200287</em><br>"
    "本文为中文解读，仅作学术交流：照片引自原文图 1～图 6（图 1 中的英文由编者译成中文覆盖原位置，图注由编者译成中文），表 1 中文卡、关键数字卡、预后图和临床卡为编者根据原文整理，表格为编者翻译。原文版权归原作者和 International Journal of Sports Physical Therapy 所有。"
))

TITLE = "「青少年腰痛」腰椎峡部裂的孩子怎么练回赛场？IJSPT 三期康复方案和进阶标准"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>青少年腰椎峡部裂康复</title>
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
