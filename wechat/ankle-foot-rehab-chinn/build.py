#!/usr/bin/env python3
"""运动员踝与足部损伤的康复（Chinn 和 Hertel 2010 Clin Sports Med）推文

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
    "Chinn L, Hertel J. Rehabilitation of Ankle and Foot Injuries in Athletes. Clin Sports Med. 2010;29(1):157-167. doi:10.1016/j.csm.2009.09.006",
    "中文题目：运动员踝与足部损伤的康复",
    "作者来自美国弗吉尼亚大学运动机能学项目运动与运动损伤实验室，通讯作者 Jay Hertel",
    "文章类型：临床综述（叙述性，无系统检索），美国国家补充与替代医学中心资助",
], square=True))

A.append(h2("为什么要专门谈踝足康复"))
A.append(ul([
    "踝和足是运动员急性和慢性损伤最常见的部位之一，虽然很少危及生命，但会直接限制跑、跳、踢和变向",
    f"处理踝足损伤，除了损伤类型、严重程度、愈合时间和运动水平，还要考虑{b('足型、生物力学、比赛用鞋，以及支具和贴扎')}",
    f"足是下肢动力链的“底座”，康复没做好，{b('踝足损伤可能引发链条上方其他部位的继发损伤')}",
]))
A.append(pic(2, "编者根据原文整理"))

A.append(h2("先看懂正常步态"))
A.append(ul([
    "步态分为支撑相（足跟着地到足尖离地）和摆动相；评估步态、识别代偿，是决定是否需要专人指导康复的关键",
    f"足跟着地时距下关节处于旋后、胫骨外旋；承重后距下关节旋前、胫骨内旋，{b('中跗关节“解锁”')}，足像减震器一样吸收冲击、适应地面，把负荷分散到更多结构上",
    f"重心越过支撑面时旋前达到最大，随后足再旋后、中跗关节“锁住”，{b('足变成坚硬的杠杆')}，把力量传到地面完成蹬离",
    "旋前本身是正常的，问题在于时机和幅度",
]))
A.append(pic(3, "编者据原文描述绘制"))

A.append(h2("外侧踝扭伤"))
A.append(h3("一、分级"))
A.append(ul([
    "最常见的机制是后足相对胫骨过度内翻加跖屈，伤及距腓前韧带、距腓后韧带和跟腓韧带",
    f"{b('1 度')}：韧带被拉长，几乎不松弛，疼痛肿胀轻，处理疼痛肿胀后常可马上开始康复，停训一般少于 1 周",
    f"{b('2 度')}：部分纤维撕裂，中度松弛，疼痛肿胀中到重，常需固定数天",
    f"{b('3 度')}：韧带完全断裂，关节明显松弛，可能数周不能负重",
]))
A.append(h3("二、分期康复"))
A.append(pic(4, "原文图 1（照片内只有分图字母，图注由编者翻译）"))
A.append(pic(5, "编者根据原文整理"))
A.append(pic(6, "原文图 2（照片内无文字，图注由编者翻译）"))
A.append(h3("三、临床小技巧"))
A.append(ul([
    f"家庭训练：刷牙时用患侧单足站，进阶到闭眼刷牙",
    "由康复治疗师做距小腿关节和胫腓关节松动，改善背伸",
    "穿鞋和光脚交替训练，改变足底皮肤感觉输入",
    "在 10～20 码（约 9～18 m）的场地来回踮脚走，再分别用脚尖内扣、外八和足跟走",
    f"让患者用患侧连续单足跳 10 次、尽量跳高，同时观察面部表情：{mk('能做完且不皱眉')}，就可以开始功能性康复",
]))
A.append(h3("四、宣教和预防"))
A.append(ul([
    f"{b('踝扭伤最大的危险因素是既往扭伤')}；初次扭伤者约 30% 会发展成慢性踝关节不稳",
    "患者、教练和家长常认为踝扭伤不严重、很快能上场，很多人根本不就医；要让各方明白残留症状和反复扭伤很常见，必须等韧带愈合、活动度、力量和平衡都恢复后再回场",
    "康复过程中如果又肿了，说明练多了",
    "贴扎和护踝都能降低再扭伤风险：护踝方便、性价比高，还能提供本体感觉刺激；贴扎可以按运动员、项目和不稳方向定制",
]))

A.append(h2("内侧踝扭伤和下胫腓联合扭伤"))
A.append(pic(7, "编者根据原文整理"))

A.append(h2("足底筋膜炎"))
A.append(ul([
    "足底筋膜是从跟骨内侧延伸到跖趾关节的致密结缔组织，维持足的稳定、支撑纵弓；伸趾和足弓下沉时被拉紧",
    "原文认为病因是筋膜起点附近的劳损，常与跑姿不良、鞋不合适有关",
    "依从性好的话可以很快缓解，治疗不当则可能拖上数月甚至数年",
]))
A.append(pic(8, "原文图 3（照片内只有箭头，图注由编者翻译）"))
A.append(pic(9, "编者根据原文整理"))

A.append(h2("跟腱炎"))
A.append(pic(10, "编者根据原文整理"))

A.append(h2("草皮趾"))
A.append(pic(11, "编者根据原文整理"))

A.append(h2("作者的总结"))
A.append(ul([
    f"几乎所有运动员下肢损伤都能从包含{b('治疗性训练')}的康复方案中获益",
    "重点是恢复关节活动度、肌力、神经肌肉协调和正常步态",
    "逐级回归运动、加入专项训练，目标是安全回场、尽量减少再伤",
]))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{b('这是 2010 年的叙述性综述')}：没有系统检索，多数建议（如分期进阶、回场标准、各种小技巧）来自临床经验，只有少数几处引用研究；适合当作框架，不宜当作证据",
    f"{b("“跟腱炎”的说法已经过时")}：原文把它定义为炎症性疾病，而关键词里用的却是“跟腱变性（tendinosis）”；现在一般称为跟腱病，认为以肌腱退行性改变为主，治疗也更强调渐进负荷而不是长时间休息（编者观点）",
    f"{b("足底筋膜炎“先休息、减少负重”")}：原文以休息为起点，近年更多主张在负荷管理下尽早加入牵伸和力量训练（编者观点）",
    f"{b('“力量达伤前 80%～90%”很难操作')}：多数运动员没有伤前力量数据，临床通常改用健侧对比，原文没有给出具体测法",
    f"{b('部分说法缺少依据')}：如腰椎前凸导致足底筋膜炎、跑鞋每 500 英里或 2 年更换、坡道训练每周最多一次，原文都没有引用研究",
    f"{b('方向仍然可信')}：既往扭伤是再扭伤的首要危险因素、约 30% 发展为慢性踝关节不稳、贴扎和护踝能降低再扭伤，这几条原文都有引用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('步态时间段重叠')}：一处说距下关节旋前一直维持到支撑相的 55%～85%，下一句又说 70%～90% 开始再旋后，两段区间互相重叠，原文没解释",
    f"{b('对角线动作“孤立距小腿关节”')}：原文说跖屈 + 内翻、背伸 + 外翻的对角线动作可以孤立距小腿关节的运动，但内外翻主要发生在距下关节，组合动作恰恰不是孤立运动",
    f"{b('名称前后不一')}：关键词写“Achilles Tendinosis（跟腱变性）”，正文通篇写“Achilles tendonitis（跟腱炎）”并定义为炎症",
    f"{b('笔误较多')}：rigid level（应为 lever，杠杆）、reafoot（rearfoot）、planter / planar（plantar）、Tuft toe（Turf toe）、Towel crutches（应为 towel crunches，毛巾卷）、osteoarthritis arthritis；“roll on a ball underneath the medial longitudinal”漏了 arch",
    f"{b('版权页年份')}：页脚为 2010 年第 29 卷，ISSN 行却写“0278-5919/09”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('踝扭伤别轻视')}：分期进阶、平衡训练从易到难，回场前用单足连跳、跳远对比和整场训练检验",
    f"{b('高位扭伤要给足时间')}：下胫腓联合扭伤肿得不明显却可能要数月恢复，提前和运动员、教练讲清预期",
    f"{b('足底筋膜和跟腱')}：抓住背伸活动度、足部小肌群和小腿力量，同时评估鞋、足型和步态；具体负荷方案可参考更新的指南",
    f"{b('草皮趾')}：用硬质前掌鞋垫或贴扎限制拇趾背伸，比硬扛着练更重要",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Chinn L, Hertel J. Rehabilitation of Ankle and Foot Injuries in Athletes. Clin Sports Med. 2010;29(1):157-167. doi:10.1016/j.csm.2009.09.006（PubMed Central 作者稿 PMC2786815）</em><br>"
    "本文为中文解读，仅作学术交流：照片引自原文图 1～图 3（图中无英文，图注由编者翻译），损伤一览、步态示意和各损伤康复卡为编者根据原文整理。原文版权归 Elsevier 所有。"
))

TITLE = "「踝足康复」踝扭伤、足底筋膜炎、跟腱炎、草皮趾：运动员踝足损伤怎么练、何时回场"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>运动员踝足损伤康复推文</title>
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
