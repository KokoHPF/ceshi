#!/usr/bin/env python3
"""手法治疗对健康年轻人呼吸功能的即时影响（Küçük 等 2024）推文。

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
    "Küçük E, Tozcu D, Topaktaş B, Coşkun G. Immediate effects of manual therapy on respiratory functions in healthy young individuals: a randomized controlled trial. Sci Rep. 2024;14:17419.",
    "作者来自土耳其阿马西亚大学、哈切特佩大学",
    "随机对照试验，已在 ClinicalTrials.gov 注册（NCT05934240）",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"胸廓要能“张得开”，肺才好充气。胸椎僵、肋骨活动差、呼吸肌绷得紧，胸壁就更硬，理论上会限制通气。"
    f"所以不少治疗师会给 COPD、哮喘的患者做{b('胸椎手法和膈肌松动')}，希望让胸廓更灵活、呼吸更顺。"
))
A.append(p(
    f"那在{b('健康人')}身上做呢？以往研究结论不一：有的说做完肺活量涨了，有的说什么都没变。"
    f"这篇就想看看：{mk('给健康大学生做一次胸椎手法 + 膈肌松动，肺功能会不会马上变化')}。"
    f"作者顺带还看了吸烟、得过新冠的学生做完有没有不同。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：阿马西亚大学健康学院 {b('18～22 岁')}的学生，207 人报名，排除 103 人后纳入 {b('104 人')}（女 87 人，平均 20.1 岁）",
    "纳入：在读、没有需要吃药的慢性病、自愿参加；测试前 24 小时不喝酒",
    "排除：骨科问题、心肺疾病、手法禁忌（如骨质疏松）、做过胸部/背部/腹部手术",
    f"随机分成{b('手法治疗组')}和{b('假手法组')}，各 52 人",
    f"{b('只做 1 次')}，做之前和做完 5 分钟内各测一次肺功能（便携式肺功能仪，按美国胸科学会标准测 3 次取最合适的值）",
    "指标：呼气峰流量（PEF）、第 1 秒用力呼气容积（FEV1）、用力肺活量（FVC）、一秒率（FEV1/FVC）",
    "测肺功能的人和做统计的人不知道分组；做手法的治疗师知道",
]))
A.append(pic(2, "原文图 1：受试者流程（编者中文重绘）"))

A.append(h2("重点：手法到底怎么做的"))
A.append(pic(6, "两组方案一览（编者根据原文整理）"))
A.append(p(f"手法组一次做三个技术，都由同一位治疗师完成。"))
A.append(h3("① 胸椎推扳手法（thrust，做 1 次）"))
A.append(pic(3, "原文图 2：胸椎推扳手法（床单印章文字已模糊处理）"))
A.append(ul([
    f"体位：受试者{b('仰卧')}，双臂交叉抱在胸前",
    "治疗师一只手垫在背后，放在胸椎横突处；另一只手扶住受试者交叉的肘部",
    f"通过{b('屈曲 + 向后滑动')}把要处理的节段“锁住”，找到组织屏障（感觉“卡住”的位置）",
    f"{mk('在受试者呼气时，治疗师用身体往下快速推 1 下')}，只做一次",
]))
A.append(p(f"这就是临床常说的仰卧位胸椎“扳一下”。原文{red('没写针对的是哪一节胸椎')}，也没写是否听到弹响。"))
A.append(h3("② 胸椎松动（每个肋横突关节 30 秒）"))
A.append(pic(4, "原文图 3：胸椎松动，俯卧位，作用在肋横突关节"))
A.append(ul([
    f"体位：受试者{b('俯卧')}",
    f"治疗师一只手用{b('豌豆骨一侧')}，加两根手指放在{b('肋横突关节外侧')}；另一只手放在关节对侧",
    f"做{b('顺时针和逆时针方向的后前向（PA）椎间松动')}",
    f"{mk('每个肋横突关节做 30 秒')}",
]))
A.append(p(f"肋横突关节是肋骨和胸椎横突相连的地方，直接关系到肋骨随呼吸的上抬。原文{red('也没说做了哪几个节段、一共做了几个关节')}，所以总时长没法算。"))
A.append(h3("③ 膈肌松动（有节律地做 2～4 分钟）"))
A.append(pic(5, "原文图 4：膈肌松动，仰卧位，双手抓住下肋"))
A.append(ul([
    f"体位：受试者{b('仰卧')}，正常呼吸",
    "治疗师双手抓住两侧下肋（拇指在肋弓下缘）",
    f"先用{b('左手把右侧下肋往上、往中线推')}，再用{b('右手把左侧下肋往上、往中线推')}",
    f"{mk('左右交替、有节律地做 2～4 分钟')}",
]))
A.append(p(f"原文说膈肌松动包含“8 种不同的牵拉技术”，但{red('只描述了上面这一种')}。"))
A.append(h3("假手法组"))
A.append(p(
    f"同样的体位、同样的手放在同样的位置，总时长和手法组一样，但{b('不施加任何力量或动作')}，"
    f"治疗师只是观察呼吸、触摸肌肉。所有人都没有出现不良反应，24 小时内也没人打电话报告不适。"
))

A.append(h2("结果：只有 PEF 有差别"))
A.append(pic(7, "PEF 结果（编者按原文表 2 数值重绘）"))
A.append(ul([
    f"{b('PEF')}：手法组 296.3 → 316.1（升 19.8，P = 0.018），假手法组 337.1 → 324.5（降 12.6，P = 0.002）；{mk('两组变化量相比 P = 0.001')}",
    "干预前假手法组的 PEF 本来就比手法组高（P = 0.045），干预后两组没差别",
    f"{b('FVC、FEV1、FEV1/FVC')}：两组干预前后都没有显著变化，组间也没差别",
    "亚组：手法组里吸烟的学生（15 人）PEF 从 330.3 升到 357.0（P = 0.039）；手法组没得过新冠的学生 FVC 从 3.5 升到 3.7（P = 0.041）",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('很可能是回归均值')}：手法组起点偏低、往上走；假手法组起点偏高、往下走，干预后两组几乎一样（316 vs 324）。"
    f"{red('这种“低的升、高的降、最后会合”的形态，本身就是回归均值的典型表现')}，不一定是手法的作用",
    f"{b('PEF 很吃力气')}：PEF 取决于受试者吹得多猛，受期望和配合度影响大。假手法只是把手放上去，受试者很可能猜得出自己是哪组，所谓“三盲”很难成立",
    f"{b('变化量小')}：手法组只升了约 20，假手法组的 SD 都有 90～120，个体变化的 SD 也有 30～60，这点差距在 PEF 本身的测试波动范围附近",
    f"{b('更稳定的 FVC、FEV1 都没变')}：反映肺容量和气道的“硬指标”没动，只是最容易受用力影响的 PEF 变了",
    f"{b('两组基线不均衡')}：随机分组后男生 14 vs 3 人、得过新冠 12 vs 29 人，差得很明显，作者也没在分析里校正",
    f"{b('亚组分析靠不住')}：吸烟、新冠亚组人数少，又只做了组内比较，多次检验也没校正",
    f"{b('只做 1 次、只测 5 分钟内')}：说明不了持续效果，对象也是健康年轻人，不能直接推到 COPD、哮喘患者",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“三盲”和描述矛盾')}：标题写的是三盲试验，但原文自己说做手法的治疗师不设盲；同一段里又说治疗师“在试验开始前不知道分组”，前后打架",
    f"{b('年龄标准差不可能这么大')}：纳入的是 18～22 岁，这个范围内标准差最大也就约 2.0，但对照组写 20.1 ± 2.6、全体写 20.1 ± 2.2",
    f"{b('一秒率组间差距说反了')}：正文和表 3 都说干预后两组 FEV1/FVC 差距“变小”，但按表 2 算，干预前差 4.9（89.2 vs 84.3），干预后差 5.8（88.9 vs 83.1），{red('其实是变大了')}",
    f"{b('BMI 分类少了 3 个人')}：对照组 BMI 分类 7 + 35 + 7 + 0 = 49 人，百分比也是按 49 算的，但对照组明明有 52 人；用 49 人算卡方正好得到原文的 P = 0.153",
    f"{b('百分比算错')}：对照组不吸烟 38 人写成 72.1%，38/52 应为 73.1%",
    f"{b('一秒率的标准差不合理')}：健康年轻人 FEV1/FVC 写成 89.2 ± 12.9，按这个分布会有相当一部分人超过 100%，而一秒率不可能大于 100%",
    f"{b('PEF 没写单位，数值也偏低')}：如果是 L/min，20 岁左右的健康人一般在 400 以上；而且手法组男生更多（27% vs 6%），PEF 反而更低，有点反常",
    f"{b('样本量计算没头没尾')}：只给了 FEV1/FVC 的均值 0.84 和标准差 0.0713，没说预期差多少，算出每组 12 人；而且最后下结论用的是 PEF，不是 FEV1/FVC",
    f"{b('吸烟亚组被拔高')}：讨论说吸烟者做完 PEF 的升幅“比不吸烟者更明显”，但结果里只做了吸烟者的组内比较，没有和不吸烟者比，也没给对照组吸烟者的数据",
    f"{b('解释对两组都适用')}：作者把假手法组 PEF 下降部分归因于“从躺着到站起来的体位变化”，可手法组也一样要从床上起来",
    f"{b('引用对不上')}：讲 MIP、MEP、脉冲振荡法的那句，引用的是《Maitland 脊柱手法》（参考文献 30）；讨论说 Nagy 等研究用的是膈肌松解，但该研究标题写明是膈肌松解{b('联合吸气肌训练')}；表 3 里 “Vemuldap” 应为 Vemulpad",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('别指望做一次胸椎手法就能让肺功能“马上变好”')}：这篇真正能说的，只是 PEF 有个小幅变化，而且很可能有回归均值和用力程度的干扰",
    f"手法本身值得借鉴：{b('仰卧胸椎推扳 + 俯卧肋横突关节 PA 松动 + 仰卧下肋交替上推')}这一套，对胸椎僵硬、肋骨活动差、觉得“吸不深”的人可以作为辅助手段，安全性也不错",
    "如果想评估手法对呼吸的作用，PEF 不是好指标；胸廓扩张度、膈肌超声、MIP/MEP 等更直接",
    "COPD、哮喘这类患者的证据要看针对患者的研究，不能拿健康人的结果去套",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　两组社会人口学特征和健康行为"))
A.append(table(["项目", "手法组（n = 52）", "假手法组（n = 52）", "P"], [
    ["年龄（岁）", "20.3 ± 1.9", "20.1 ± 2.6", "0.132ᵃ"],
    ["身高（m）", "1.7 ± 0.1", "1.7 ± 0.1", "0.181ᵃ"],
    ["体重（kg）", "63.4 ± 13.8", "58.9 ± 10.3", "0.103ᵃ"],
    ["BMI（kg/m²）", "22.7 ± 4.0", "21.5 ± 3.0", "0.280ᵃ"],
    [b("性别 [n（%）]"), "", "", "<b>0.004</b>ᵇ"],
    ["男", "14（26.9）", "3（5.8）", ""],
    ["女", "38（73.1）", "49（94.2）", ""],
    [b("BMI 分类 [n（%）]"), "", "", "0.153ᵇ"],
    ["偏瘦", "4（7.7）", "7（14.3）", ""],
    ["正常", "34（65.4）", "35（71.4）", ""],
    ["超重", "10（19.2）", "7（14.3）", ""],
    ["肥胖", "4（7.7）", "0（0.0）", ""],
    [b("吸烟 [n（%）]"), "", "", "0.827ᵇ"],
    ["是", "15（28.8）", "14（26.9）", ""],
    ["否", "37（71.2）", "38（72.1）", ""],
    [b("新冠 [n（%）]"), "", "", "<b>0.001</b>ᵇ"],
    ["确诊过", "12（23.1）", "29（55.8）", ""],
    ["未确诊", "40（76.9）", "23（44.2）", ""],
]))
A.append(small("计量资料为均值 ± 标准差。a：Mann-Whitney U 检验；b：卡方检验。新冠指经 PCR 确诊。表中数字照原文录入，原文的错误见上文。"))
A.append(tcap("表 2　两组肺功能测试结果"))
A.append(table(["指标 / 组别", "干预前", "干预后", "组内 P", "变化量"], [
    [b("PEF"), "", "", "", ""],
    ["手法组", "296.3 ± 110.8", "316.1 ± 119.1", "<b>0.018</b>ᵉ", "19.8 ± 58.3"],
    ["假手法组", "337.1 ± 93.3", "324.5 ± 89.2", "<b>0.002</b>ᶠ", "−12.6 ± 33.6"],
    ["组间 P", "<b>0.045</b>ᶜ", "0.683ᶜ", "", "<b>0.001</b>ᶜ"],
    [b("FVC"), "", "", "", ""],
    ["手法组", "3.6 ± 0.7", "3.7 ± 0.8", "0.074ᶠ", "0.1 ± 0.6"],
    ["假手法组", "3.3 ± 0.8", "3.5 ± 0.7", "0.137ᶠ", "0.2 ± 0.9"],
    ["组间 P", "0.106ᶜ", "0.539ᵈ", "", "0.290ᵈ"],
    [b("FEV1"), "", "", "", ""],
    ["手法组", "2.9 ± 0.6", "3.0 ± 0.6", "0.735ᶠ", "0.1 ± 0.4"],
    ["假手法组", "2.9 ± 0.6", "3.1 ± 0.6", "0.235ᶠ", "0.2 ± 0.8"],
    ["组间 P", "0.558ᶜ", "0.219ᵈ", "", "0.187ᶜ"],
    [b("FEV1/FVC"), "", "", "", ""],
    ["手法组", "84.3 ± 12.3", "83.1 ± 13.3", "0.506ᵉ", "−1.2 ± 12.2"],
    ["假手法组", "89.2 ± 12.9", "88.9 ± 12.3", "0.569ᶠ", "−0.3 ± 13.0"],
    ["组间 P", "<b>0.009</b>ᵈ", "<b>0.040</b>ᵈ", "", "0.121ᵈ"],
]))
A.append(small("c：Student t 检验；d：Mann-Whitney U 检验；e：配对 t 检验；f：Wilcoxon 检验。变化量 = 干预后 − 干预前。原文未注明 PEF 单位，FVC、FEV1 单位应为 L，FEV1/FVC 为 %。"))
A.append(tcap("表 3　以往研究中手法对肺功能的短期和长期影响"))
A.append(table(["研究", "设计与样本", "干预", "测量", "主要结果"], [
    ["Jonely 等", "RCT；21 名 50 岁以上健康人，分 2 组", "胸椎手法 vs 假肋间训练，各 3 次", "肺功能（第 3 次干预后 7 天内）、胸围、人体活动量表", "手法组第 3 次后一周内最大自主通气量显著改善；假手法组单次干预后呼气时胸廓活动度有显著差别"],
    ["Stępnik 等", "RCT；30 名 19～46 岁健康人，分 2 组", "整骨手法（胸椎推扳、胸骨泵、膈肌牵伸）vs 咬肌软组织治疗（安慰）", "干预前后肺功能", "手法组 PEF 显著改善（P = 0.001），FVC、FEV1 无显著变化"],
    ["Mustafaoğlu 等", "RCT；78 名 20 岁以上健康男性，分 2 组", "单次胸椎手法 vs 假胸椎手法", "干预前后肺功能、6 分钟步行、胸围、呼吸肌力量", "两组胸围、肺功能、呼吸肌力量、6 分钟步行距离均无显著差别"],
    ["Wall 等", "RCT；21 名 19～35 岁健康人，分 2 组", "单次两种手法：高速低幅推扳、低速关节松动", "基线及干预后 1、10、20、30 分钟肺功能", "干预后任何时间点肺功能均无显著变化"],
    ["Shin 和 Lee", "RCT；30 名健康年轻人，分 2 组", "胸椎手法 vs 假胸椎手法", "干预前后肺功能", "手法组 FVC、FEV1 显著增加，对照组无变化，组间差异显著"],
    ["Gonzalez 等", "RCT；80 名 20～50 岁健康成人，分 2 组", "膈肌技术 vs 安慰干预", "基线、干预后即刻、5 和 20 分钟肺功能，人体测量，最大呼吸压", "膈肌牵伸显著改善最大呼吸压（P < 0.001）、FVC（P = 0.006）和 FEV1（P = 0.042）；安慰组无变化"],
    ["Lima 等", "实验研究；100 名 17～30 岁健康成人", "颈胸部泵式松动，每个技术 6 次", "干预前后肺功能", "男性 FVC、PEF、FEV1 增加，一秒率下降；女性 FVC、FEV1 增加，PEF 不变，一秒率下降"],
    ["Engel 和 Vemulpad", "RCT；20 名健康人，分为对照组和 3 个干预组", "单纯运动、单纯整脊手法、手法后运动；4 周 6 次", "干预前后肺功能", "单纯运动组 FVC、FEV1 显著下降；单纯手法组 FVC、FEV1 显著增加；手法 + 运动组手法后增加、运动后进一步增加"],
    ["本研究", "RCT；104 名 18～22 岁健康年轻人，分 2 组", "胸椎手法、松动 + 膈肌松动 vs 假手法", "干预前后肺功能", "PEF 手法组升、假手法组降；FVC、FEV1、FEV1/FVC 组间无差别"],
], first_bold=True))
A.append(small("表 3 按原文内容翻译、精简；原文将“Vemulpad”误拼为“Vemuldap”。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Küçük E, Tozcu D, Topaktaş B, Coşkun G. Immediate effects of manual therapy on respiratory functions in healthy young individuals: a randomized controlled trial. Sci Rep. 2024;14:17419. doi:10.1038/s41598-024-68654-7</em><br>"
    "原文以 CC BY-NC-ND 4.0 协议开放获取（仅限非商业使用、原则上不允许改编）。本文为学术交流用的中文解读，手法照片引自原文图 2～4（床单印章文字已模糊），"
    "流程图、PEF 结果图为编者按原文中文重绘，方案卡为编者整理绘制，附录表格为编者翻译整理，版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「呼吸」做一次胸椎手法，肺功能马上变好？104 人随机对照试验"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>手法与呼吸功能推文</title>
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
