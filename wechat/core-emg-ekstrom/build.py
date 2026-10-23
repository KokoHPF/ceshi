#!/usr/bin/env python3
"""Ekstrom 等 2007 JOSPT 9 个康复动作核心、髋和大腿肌电分析中文解读推文

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
    "Ekstrom RA, Donatelli RA, Carp KC. Electromyographic analysis of core trunk, hip, and thigh muscles during 9 rehabilitation exercises. J Orthop Sports Phys Ther. 2007;37(12):754-762. doi:10.2519/jospt.2007.2471",
    "中文题目：9 个康复训练动作中核心躯干、髋部和大腿肌肉的肌电分析",
    "作者来自美国南达科他大学物理治疗系、Physiotherapy Associates",
    "研究类型：前瞻性、单组、重复测量设计",
], square=True))

A.append(h2("研究背景：自重训练，到底练到了多少"))
A.append(p(
    f"康复训练遵循“特定需求产生特定适应”的原则：想增加力量或耐力，就要针对薄弱或对活动重要的肌群。但臀桥、侧桥这类{b('自重动作')}，治疗师没法知道肌肉实际承受多少阻力。{b('表面肌电')}能反映肌肉激活程度，帮助判断一个动作更适合练力量，还是练耐力和稳定。"
))
A.append(ul([
    "腰伸肌、臀大肌和髋外旋肌无力、耐力差，与下肢损伤和腰痛有关",
    "未受伤运动员的髋外展和外旋肌力更强；髌股疼痛女性的髋外展、伸、外旋肌力更弱，强化后疼痛、下肢运动学和功能都有改善",
    "躯干和髋部肌肉对高尔夫、棒球挥杆的力量和准确性也很重要",
    f"{b('研究目的')}：量化 9 个常用动作中躯干、髋和大腿肌肉的激活，找出适合力量训练和适合耐力 / 稳定训练的动作",
]))

A.append(h2("方法"))
A.append(ul([
    f"{b('受试者')}：30 名健康人（男 19、女 11），19～58 岁，平均 27 岁；无下肢或腰背问题",
    f"{b('8 块肌肉')}：腹直肌、腹外斜肌、胸最长肌、腰多裂肌、臀大肌、臀中肌、股内斜肌、腘绳肌；单侧贴表面电极，电极中心距 20 mm",
    f"{b('标准化')}：每块肌肉做 3 次最大自主等长收缩（MVIC），每次 5 秒；动作中的肌电以 %MVIC 表示",
    f"{b('9 个动作，随机顺序')}：主动髋外展、臀桥、单腿臀桥、侧桥、俯桥（肘和脚尖）、四点跪对侧抬手抬腿、侧向上台阶（20.32 cm）、站立弓步、Dynamic Edge 滑雪模拟器",
    "躯干稳定动作做 3 次、每次保持 5 秒；上台阶和弓步慢速全程，在最大屈膝处保持 5 秒；Dynamic Edge 连续左右滑动",
    "信号处理：全波整流、均方根平滑（20 毫秒窗），取峰值附近 1 秒的平均幅值；每块肌肉做单因素重复测量方差分析，P < 0.05",
    "13 人重复做臀桥和四点跪抬手抬腿，检验同日重测信度",
]))
A.append(pic(2, "原文图 1～3（照片为原图，图注编者译成中文）"))
A.append(pic(3, "原文图 4～6（照片为原图，图注编者译成中文）"))
A.append(pic(4, "原文图 7～9（照片为原图，图注编者译成中文）"))

A.append(h2("结果"))
A.append(ul([
    f"{b('信度')}：臀桥和四点跪抬手抬腿的组内相关系数分别为 0.86 和 0.93，但测量标准误约 {b('20% MVIC')}",
    f"{b('臀中肌')}：侧桥最高（{b('74% ± 30%')}），显著高于其余 8 个动作",
    f"{b('臀大肌')}：四点跪对侧抬手抬腿最高（{b('56% ± 22%')}），显著高于其余动作；其次是单腿臀桥 40%、弓步 36%",
    f"{b('股内斜肌')}：侧向上台阶 {b('85% ± 17%')}、弓步 {b('76% ± 19%')}，两者差异不显著，都显著高于其他动作",
    f"{b('腘绳肌')}：单腿臀桥 40%、四点跪抬手抬腿 39% 最高，两者相当",
    f"{b('胸最长肌和腰多裂肌')}：臀桥、单腿臀桥、侧桥、四点跪抬手抬腿相近（36%～46%），显著高于其余动作；俯桥只有 5%～6%",
    f"{b('腹外斜肌')}：侧桥最高（{b('69% ± 26%')}）；{b('腹直肌')}：俯桥 43%、侧桥 34% 最高，两者差异不显著",
]))
A.append(pic(5, "编者根据原文表 1～4 整理"))

A.append(h2("作者怎么解读"))
A.append(ul([
    f"{b('45% MVIC 当作力量训练门槛')}：既往研究显示 45%～50% 1RM 的负荷能让未训练者增加力量，所以平均超过 45% MVIC 的动作“可能”提供力量刺激",
    f"按这个标准，{b('侧桥、侧向上台阶、弓步')}，可能还有{b('四点跪对侧抬手抬腿')}，对相应肌肉有力量训练价值；其余多数动作更适合耐力或运动控制训练",
    f"{b('侧桥练臀中肌')}：以前很少把侧桥当臀中肌力量训练，可以加入方案",
    f"{b('臀桥 / 单腿臀桥')}：Arokoski 等发现女性的背伸肌激活明显高于男性，所以部分人尤其女性可能从中获得力量效果",
    f"{b('主动髋外展')}：核心稳定肌参与很少，但能孤立臀中肌（39%），加外部阻力后可用于非负重下的臀中肌力量训练",
    "臀桥、单腿臀桥、侧桥、俯桥和四点跪抬手抬腿都有多肌群共同激活，适合稳定和耐力训练；Dynamic Edge 适合耐力训练",
]))
A.append(pic(6, "编者根据原文整理"))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{b('人群')}：30 名健康青年为主，不能直接外推到腰痛、髌股疼痛或术后患者，作者也提醒了这一点",
    f"{b('45% MVIC 门槛是推理，不是验证')}：%MVIC 和 %1RM 不是一回事，肌电幅值与力的关系还可能非线性；用它划分“力量”和“耐力”动作只是粗略参考",
    f"{b('变异大')}：标准差常接近均值的一半甚至更大（侧桥臀中肌 74% ± 30%），测量标准误约 20% MVIC，个体能否达到门槛差别很大",
    f"{b('静态保持')}：上台阶和弓步取的是最大屈膝位 5 秒等长保持，和临床常用的动态做法不同，数值不能直接对标动态训练",
    f"{b('串扰')}：臀中肌电极靠近臀大肌，可能有串扰；表面电极能否准确记录多裂肌仍有争议",
    f"{b('MVIC 姿势')}：臀中肌在外展末端测 MVIC，测试姿势会影响分母，进而影响所有 %MVIC 数值",
    f"{b('价值在于相对比较')}：受试者内设计，同一块肌肉在不同动作间的高低排序比绝对数值更可靠",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('俯桥的两块腹肌数值对调')}：讨论写俯桥时腹直肌 47% ± 21%、腹外斜肌 43% ± 21%，而表 4 是腹外斜肌 47%、腹直肌 43%",
    f"{b('弓步股内斜肌')}：结果正文写 77% ± 19%，表 2 和讨论都是 76% ± 19%",
    f"{b('四点跪臀大肌标准差')}：表 1 和结果是 56% ± 22%，讨论是 56% ± 23%",
    f"{b('结论和门槛不一致')}：结论说主动髋外展“对臀中肌非负重力量训练有效”，但它只有 39% MVIC，低于作者自己定的 45% 门槛，需要额外加阻力才成立",
    f"{b('笔误')}：表 4 脚注“external oblique obdominis”（应为 abdominis）；讨论中“rectus abdominus”（应为 abdominis）、“Aroskoski”（应为 Arokoski）",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先想清楚练什么')}：要力量就选高激活动作，要耐力和控制就选中低激活动作做长时间保持或多次重复",
    f"{b('练股内斜肌')}：侧向上台阶和弓步激活最高，可在最大屈膝位加 5 秒等长保持",
    f"{b('练臀中肌')}：侧桥激活最高，同时练到腹外斜肌；不能负重或侧桥做不了时，用侧卧髋外展加阻力",
    f"{b('练臀大肌')}：四点跪对侧抬手抬腿最高，单腿臀桥次之",
    f"{b('练腰背伸肌耐力')}：臀桥、单腿臀桥、侧桥、四点跪抬手抬腿差不多，按患者能力选择；俯桥几乎不练背伸肌",
    f"{b('练腹肌')}：侧桥和俯桥激活最高；要练腹肌力量，作者建议参考其他更针对的动作",
    f"{b('因人调整')}：数据来自健康人且个体差异大，体能好的人需要更大刺激，患者则可能在较低激活下就有效",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　9 个动作中臀中肌和臀大肌的肌电活动"))
A.append(table(["动作", "臀中肌", "臀大肌"], [
    ["1. 侧桥", "74 ± 30†", "21 ± 16"], ["2. 单腿臀桥", "47 ± 24‡", "40 ± 20‡"], ["3. 侧向上台阶", "43 ± 18‡", "29 ± 13"],
    ["4. 四点跪对侧抬手抬腿", "42 ± 17‡", "56 ± 22†"], ["5. 主动髋外展", "39 ± 17‡", "21 ± 16"], ["6. Dynamic Edge", "33 ± 16", "19 ± 14"],
    ["7. 弓步", "29 ± 12", "36 ± 17‡"], ["8. 臀桥", "28 ± 17", "25 ± 14"], ["9. 俯桥", "27 ± 11", "9 ± 7"],
]))
A.append(small("注：数值为均值 ± 标准差，%MVIC；n = 30；P < 0.05。† 臀中肌：动作 1 显著高于动作 2～9；臀大肌：动作 4 显著高于其他所有动作。‡ 臀中肌：动作 2～5 之间无显著差异，但都显著高于动作 7～9；臀大肌：动作 2 和 7 之间无显著差异，但都显著高于动作 1、3、5、6、8、9。"))
A.append(tcap("表 2　9 个动作中股内斜肌和腘绳肌的肌电活动"))
A.append(table(["动作", "股内斜肌", "腘绳肌"], [
    ["1. 侧向上台阶", "85 ± 17†", "10 ± 6"], ["2. 弓步", "76 ± 19†", "11 ± 6"], ["3. Dynamic Edge", "36 ± 12", "6 ± 3"],
    ["4. 俯桥", "23 ± 13", "4 ± 6"], ["5. 侧桥", "19 ± 11", "12 ± 11"], ["6. 单腿臀桥", "18 ± 13", "40 ± 17†"],
    ["7. 四点跪对侧抬手抬腿", "16 ± 11", "39 ± 14†"], ["8. 主动髋外展", "8 ± 8", "4 ± 3"], ["9. 臀桥", "3 ± 3", "24 ± 14"],
]))
A.append(small("注：数值为均值 ± 标准差，%MVIC；n = 30；P < 0.05。† 股内斜肌：动作 1 和 2 之间无显著差异，但都显著高于其他所有动作；腘绳肌：动作 6 和 7 之间无显著差异，但都显著高于其他所有动作。"))
A.append(tcap("表 3　9 个动作中胸最长肌和腰多裂肌的肌电活动"))
A.append(table(["动作", "胸最长肌", "腰多裂肌"], [
    ["1. 单腿臀桥", "40 ± 16†", "44 ± 18†"], ["2. 侧桥", "40 ± 17†", "42 ± 24†"], ["3. 臀桥", "39 ± 15†", "39 ± 15†"],
    ["4. 四点跪对侧抬手抬腿", "36 ± 18†", "46 ± 21†"], ["5. 侧向上台阶", "25 ± 10", "28 ± 10"], ["6. Dynamic Edge", "21 ± 10", "21 ± 11"],
    ["7. 主动髋外展", "18 ± 14", "20 ± 12"], ["8. 弓步", "17 ± 8", "25 ± 11"], ["9. 俯桥", "6 ± 4", "5 ± 4"],
]))
A.append(small("注：数值为均值 ± 标准差，%MVIC；n = 30；P < 0.05。† 两块肌肉在动作 1～4 之间均无显著差异，但都显著高于动作 5～9。"))
A.append(tcap("表 4　9 个动作中腹外斜肌和腹直肌的肌电活动"))
A.append(table(["动作", "腹外斜肌", "腹直肌"], [
    ["1. 侧桥", "69 ± 26†", "34 ± 13†"], ["2. 俯桥", "47 ± 21", "43 ± 21†"], ["3. 四点跪对侧抬手抬腿", "30 ± 18", "8 ± 7"],
    ["4. 单腿臀桥", "23 ± 16", "14 ± 13"], ["5. 臀桥", "22 ± 13", "13 ± 11"], ["6. 主动髋外展", "18 ± 10", "6 ± 4"],
    ["7. Dynamic Edge", "18 ± 12", "7 ± 5"], ["8. 弓步", "17 ± 11", "7 ± 5"], ["9. 侧向上台阶", "15 ± 10", "5 ± 3"],
]))
A.append(small("注：数值为均值 ± 标准差，%MVIC；n = 30；P < 0.05。† 腹外斜肌：动作 1 显著高于动作 2～9；腹直肌：动作 1 和 2 之间无显著差异，但都显著高于动作 3～9。原表各自按左列肌肉的激活从高到低排序。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Ekstrom RA, Donatelli RA, Carp KC. Electromyographic analysis of core trunk, hip, and thigh muscles during 9 rehabilitation exercises. J Orthop Sports Phys Ther. 2007;37(12):754-762. doi:10.2519/jospt.2007.2471</em><br>"
    "本文为中文解读，仅作学术交流：照片引自原文图 1～图 9（图注由编者译成中文），肌电热图和选动作卡为编者根据原文表 1～4 整理，表格为编者翻译。原文 © 2007 Journal of Orthopaedic & Sports Physical Therapy，版权归原出版方所有。"
))

TITLE = "「核心训练」侧桥、臀桥还是弓步？JOSPT 肌电研究：9 个康复动作练到哪块肌肉"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>核心训练肌电推文</title>
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
