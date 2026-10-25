#!/usr/bin/env python3
"""寰枕关节（C0-C1）注射综述（Mares & Majdalani 2024）推文。

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
    "Mares C, Majdalani C. C0-C1 joint injection: anatomical, clinical and technical review. Interventional Pain Medicine. 2024;3:100443. doi:10.1016/j.inpm.2024.100443",
    "作者单位：加拿大蒙特利尔大学附属医院（CHUM）、魁北克物理医学研究所、Cité-de-la-Santé 医院",
    f"文章类型：{b('叙述性综述＋作者自己的操作技术')}（国际疼痛与脊柱介入学会会刊）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"颈源性头痛最常见的痛源是 {b('C2-C3 小关节')}，但{b('寰枕关节（C0-C1）')}也可以是痛源；它到底占多少，目前不知道",
    f"寰枕关节痛的牵涉范围比寰枢关节大：{b('同侧枕下为主，向上到头顶、向外到耳旁')}；但查体没有特异性，{mk('只有关节内阻滞能确诊')}",
    f"寰枕关节注射风险高：{red('椎动脉 V3 段就在关节后方稍下')}，周围还有一大片静脉丛；作者提出“{b('瞄关节线上方进针')}”来避开它们",
    "对康复治疗师来说，这篇的价值在于：理解上颈段的解剖和牵涉痛，知道什么时候该转诊、介入医生在担心什么",
]))

A.append(h2("一、颈源性头痛和寰枕关节"))
A.append(img(2))
A.append(cap("颈源性头痛：痛从哪来"))
A.append(ul([
    "上颈段的痛之所以“跑到头上”，是因为上颈段神经和三叉神经的痛觉信号在三叉颈核汇聚；早期研究在健康志愿者的关节里注射生理盐水，撑开关节囊就能诱发头颈痛",
    "这也能解释部分患者的眼眶、前额、颞部痛",
    "处理要多学科：先物理治疗、物理因子、镇痛抗炎药，无效再考虑关节内注射",
]))

A.append(h2("二、解剖：寰枕关节周围有什么"))
A.append(img(3))
A.append(cap("寰枕关节的结构和活动"))
A.append(h3("骨和韧带"))
A.append(ul([
    "寰椎（C1）没有椎体，前、后弓由两侧侧块连成一个环；侧块向上托住枕骨髁（寰枕关节），向下与枢椎相关节",
    "点头（屈伸）主要在寰枕关节，转头主要靠枢椎齿突和寰椎前弓之间的关节",
    "十字韧带是正中寰枢关节最主要的稳定结构；翼状韧带从齿突连到枕骨髁内侧；后寰枕膜从寰椎后弓连到枕骨大孔后缘",
]))
A.append(h3("肌肉：枕下三角"))
A.append(p(f"枕下三角被头半棘肌覆盖，内上界是头后大直肌、外界是头上斜肌、下界是头下斜肌；三角里有{b('椎动脉第三段、枕下静脉丛和枕下神经（C1 后支）')}——这正是进针要穿过的区域。"))
A.append(h3("椎动脉、静脉丛和弓状孔"))
A.append(img(4))
A.append(cap("为什么寰枕关节注射风险高"))
A.append(ul([
    f"椎动脉 V3 段出寰椎横突孔后，沿寰椎后弓上方的沟向内、向后走，{b('占沟宽的 57%')}；它在关节后方的{b('稍下方')}，但可能和关节线重叠",
    "变异很多：小脑后下动脉可能从 V3 段发出、和 C1 神经并行；寰前动脉残留；椎动脉在 C1-C2 就进椎管等，所以术前必须看三维影像",
    f"{b('枕下海绵窦')}：包绕 V3 段的大片静脉丛，分外、中、内三段，内、外段静脉窦更多，中段正好在关节后方；在上颈段手术里，它是主要的出血来源",
    f"{b('弓状孔')}：部分人后寰枕膜骨化形成骨桥，椎动脉从中穿过；转头时椎动脉可能被拉长变窄，与短暂性椎基底动脉供血不足有关",
]))
A.append(img(8))
A.append(cap("原文 Image 2：颅颈交界真侧位片，黑箭头所示为弓状孔"))
A.append(img(9))
A.append(cap("原文 Image 4：静脉扩张（蓝色箭头和圆圈）位于椎动脉（红色箭头和圆圈）上方、C0-1 关节正后方——作者因此决定不做注射"))
A.append(h3("神经"))
A.append(ul([
    f"寰枕关节{b('由 C1 前支直接支配')}，不像下面的小关节靠后支内侧支——所以不能用“内侧支阻滞”来诊断它",
    "C1 脊神经在椎动脉沟里走在椎动脉的下方和前方（和其他节段相反），出来后分出后支支配枕下肌群",
]))

A.append(h2("三、寰枕关节痛：痛在哪、怎么查"))
A.append(img(5))
A.append(cap("寰枕关节痛的牵涉范围和查体"))
A.append(ul([
    f"健康志愿者的注射研究：寰枕关节痛{b('只在同侧')}，以枕下为主，向上可到头顶、向外到耳旁但不包括耳朵，原文形容为“{b('雄性脱发')}”式分布；寰枢关节的痛基本局限在枕下",
    "另一项研究：寰枕关节痛 100% 有耳后和颈后外侧痛，30% 有枕部痛（不到头顶）",
    "临床实践指南的结论：病史和查体没有特异性；寰枢关节痛多局限在枕下且可复现，寰枕关节痛的分布则很杂，下可到 C5、上可到头顶",
    f"原文引用的查体手法：一手拇指放在{b('乳突和寰椎横突之间')}、虎口固定颅颈交界，另一手在头顶做{b('同侧侧屈＋对侧旋转')}，受限或疼痛提示寰枕关节",
]))

A.append(h2("四、作者的注射思路"))
A.append(p(f"{red('以下只是对原文技术的概括，帮助理解风险所在，不能作为操作指导。')}作者强调：只有受过专门训练、有经验的介入医生才应该做这项操作。"))
A.append(img(6))
A.append(cap("作者的注射思路（编者概括）"))
A.append(h3("透视定位"))
A.append(img(10))
A.append(cap("原文 Image 6：正位片，黑箭头为左侧 C1-2 关节，白箭头为 C0-1 关节"))
A.append(img(11))
A.append(cap("原文 Image 7：向左侧同侧斜约 15°，看清左侧 C0-1 关节（黑箭头）"))
A.append(img(12))
A.append(cap("原文 Image 8：正位下靶点（笔尖）在枕骨髁外上方，高于关节线；白箭头所指的关节线只是关节“杯底”"))
A.append(h3("为什么要瞄“高”"))
A.append(img(13))
A.append(cap("原文 Image 9a：真侧位，笔尖指向 C0-C1 关节线（绿线）上方，蓝线是避开椎动脉的理想路径"))
A.append(img(14))
A.append(cap("原文 Image 9b：红线是“照着正位片上的关节线去打”的路径，可能直接穿过椎动脉 V3 段"))
A.append(h3("进针和造影"))
A.append(img(15))
A.append(cap("原文 Image 12：进针后切到侧位，确认路径始终高于寰椎后弓"))
A.append(img(16))
A.append(cap("原文 Image 14：对侧斜位，针尖到达关节"))
A.append(img(17))
A.append(cap("原文 Image 16：侧位关节造影，显示“杯状”关节"))
A.append(img(18))
A.append(cap("原文 Image 17：正位关节造影"))

A.append(h2("五、疗效证据"))
A.append(img(7))
A.append(cap("疗效证据有多少"))
A.append(p(f"证据很薄：只有 1 项小样本随机试验（还是两种注射互相比、没有假治疗对照）、1 项短期观察研究和几组病例。作者没检索到并发症报道，但仍认为风险{red('应视为很大')}。"))

A.append(h2("这篇文章能信几分"))
A.append(ul([
    f"{b('叙述性综述')}：没有检索策略和纳入标准，结论是作者的经验和文献整理",
    "注射技术只用一个真实病例的图像演示，没有成功率、并发症率等数据",
    "疗效部分引用的研究样本都很小、随访短",
    "优点：把颅颈交界的血管、静脉丛和神经关系讲得很细，对理解上颈段风险很有帮助",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('寰椎下面连的是谁')}：原文写“C1 向上与枕骨髁、向下与{red('寰椎')}相关节”，向下应为{b('枢椎（C2）')}",
    f"{b('正中寰枢关节写错了弓')}：原文说正中寰枢关节由齿突、{red('寰椎后弓')}和横韧带组成；同一段前面又说齿突与{b('寰椎前弓')}后面相关节，后者才对",
    f"{b('结论和引言矛盾')}：引言说 C0-C1 作为痛源的比例“未知”，结论却说“众所周知”痛源依次是 C2-3、C1-2、C3-4、然后才是 C0-1",
    f"{b('“诊断”用了激素')}：材料里写“5 mg 地塞米松＋0.5 ml 2% 利多卡因用于阻滞的诊断部分”，诊断性阻滞只需要局麻药，激素属于治疗",
    f"{b('斜位角度不一')}：步骤里写同侧斜 15°～20°，Image 7 图注写约 15°",
    f"{b('排版残留')}：步骤 h 里留着一句占位文字“Image for theoretical trajectory”；章节在版面上顺序错乱（4.5 排在 4.3 前，4.15 排在 4.12 前）",
    f"{b('神经部分有句子缺失')}：“寰枕关节由 C1 前支直接支配。值得注意的是，窦椎神经……”后面讲的是窦椎神经支配椎管内结构，和寰枕关节的关系没交代清楚",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"枕下痛向头顶、耳旁放射，并且{b('只在一侧')}，除了 C2-C3，也要想到寰枕关节",
    f"上颈段手法要{b('尊重椎动脉')}：有弓状孔、椎动脉变异或转头时出现头晕、视物模糊等症状的患者，要更谨慎，必要时先看影像",
    "保守治疗无效、需要明确痛源时，可以转诊有经验的介入医生做诊断性阻滞；但要知道这项操作风险高、证据有限",
    "寰枕关节主要负责点头，评估时别只查旋转",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Mares C, Majdalani C. C0-C1 joint injection: anatomical, clinical and technical review. Interv Pain Med. 2024;3:100443. doi:10.1016/j.inpm.2024.100443</em><br>"
    "原文以知识共享署名-非商业性使用-禁止演绎（CC BY-NC-ND 4.0）协议开放获取，版权归原作者所有。本文为非商业的学术交流中文解读：原文 Image 2、4、6～9、12、14、16、17 原样引用，未作任何修改，中文说明见图注；编者整理卡为编者根据原文撰写。原文 Image 1、3、5 为他人授权使用的图片，本文未使用。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「颈源性头痛」寰枕关节（C0-C1）：牵涉痛在哪、为什么注射风险高？椎动脉、静脉丛与进针思路"
PTITLE = "寰枕关节注射推文"
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
