#!/usr/bin/env python3
"""肘关节电话＋视频远程评估（Vomer 等 2023）推文。

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
F = lambda i: i + 1  # 原文图 i → 第 i+1 张图
A.append(img(1))
A.append(cap("原文信息（编者中文重排）"))
A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Vomer RP II, Carfagno D, Lewno A, Shah NP, Farford BA, Kieneker L, Pujalte GGA. Elbow evaluation via telephone and video visit. Cureus. 2023;15(6):e39843. doi:10.7759/cureus.39843",
    "作者单位：美国梅奥诊所（杰克逊维尔）家庭医学科与运动医学科、杜克大学、密歇根大学等",
    f"文章类型：期刊归为原创研究，实际是{b('专家经验整理的操作指南')}（没有受试者，也没有验证数据）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"肘关节小、结构表浅，{b('主动活动度在视频里一眼就能看清')}，很适合远程评估；常见的网球肘、高尔夫球肘多数也不需要影像",
    f"远程查体的关键是{mk('让患者自己（或陪同的家人）当医生的手')}：自己摸压痛点、用健侧手给阻力、用牛奶桶当哑铃",
    f"顺序：{b('先排除颈椎')} → 视诊 → 自我触诊 → 活动度 → 抗阻 → 按外侧、后侧、前侧、内侧做特殊检查；{b('永远和健侧比')}",
    "电话问诊没有画面，就把每个检查改写成患者听得懂的问题，根据回答在脑中“画”出患者",
]))

A.append(h2("为什么要远程查肘"))
A.append(ul([
    "肘痛在基层门诊很常见；有些儿童、青少年的肘部问题拖延会有严重后果",
    "受伤的人自己开车来门诊有风险，往往还要家人陪同；运动队外出比赛时，远程评估也能先做分诊",
    "通过电话和视频可以判断损伤机制、看活动度，决定要不要拍片、拍什么，减少不必要的检查、操作和转诊",
]))

A.append(h2("第 0 步：先排除颈椎"))
A.append(pic(F(1), "原文图 1：改良 Spurling 试验"))
A.append(p(f"肘部的痛和麻可能来自颈神经根。正式查肘之前，先让患者做{b('改良 Spurling 试验')}：看向健侧肩、颈部后伸，用健侧手在头顶往下压。复现麻木或疼痛提示颈神经根病。"))

A.append(h2("第 1 步：视诊"))
A.append(p("请患者露出双肘，从前面、侧面、后面给医生看，注意两侧是否对称，有无力线异常、肌肉萎缩、肿胀、淤青、静脉怒张。"))
A.append(pic(F(2), "原文图 2：肘前面观"))
A.append(pic(F(3), "原文图 3：肘侧面观"))

A.append(h2("第 2 步：患者自己触诊"))
A.append(p(f"医生摸不到，就要{b('一边示范一边指导患者自己按')}。需要按的点："))
A.append(ul([
    f"{b('外侧')}：肱骨外上髁、桡骨头、外上髁远端 2～5 cm（伸肌总腱／桡管）",
    f"{b('前侧')}：肱二头肌远端肌腱、旋后肌腱、旋前肌腱",
    f"{b('内侧')}：屈肌总腱、尺侧副韧带位置、肱骨内上髁、肱三头肌内侧、肘管",
    f"{b('后侧')}：尺骨鹰嘴、肱三头肌腱",
]))
A.append(pic(F(4), "原文图 4：摸肱二头肌找凹陷"))
A.append(pic(F(5), "原文图 5：按压桡骨头和伸肌总腱"))

A.append(h2("第 3 步：活动度"))
A.append(p(f"{b('主动活动度')}在视频里很容易看。被动活动度：只有一侧受累时，可以用健侧手帮患侧活动（{red('不要推过疼痛点')}），有人陪同时也可以教陪同者来做。"))
A.append(img(19))
A.append(cap("正常值和功能范围（据原文整理）"))
A.append(pic(F(6), "原文图 6：屈肘"))
A.append(pic(F(7), "原文图 7：旋后"))
A.append(pic(F(8), "原文图 8：旋前"))
A.append(pic(F(9), "原文图 9：原文称“尺侧内收”"))
A.append(pic(F(10), "原文图 10：原文称“尺侧外展”"))
A.append(p(f"活动时有弹响或卡住，要请患者说出来：可能是{b('关节内游离体')}、滑膜皱襞综合征（外侧）、{b('尺神经半脱位')}或弹响肱三头肌（内侧）。"))

A.append(h2("第 4 步：抗阻测试"))
A.append(p("可以请陪同者给阻力，或者用哑铃、罐头、一桶牛奶，看有没有无力，或抗阻时有没有疼痛。医生要在视频里先示范怎么做。"))
A.append(img(20))
A.append(cap("抗阻测试查什么（据原文整理）"))
A.append(pic(F(11), "原文图 11：抗阻旋前，查旋前圆肌综合征"))

A.append(h2("第 5 步：按部位做特殊检查"))
A.append(h3("外侧"))
A.append(ul([
    f"让患者按伸肌总腱起点。伸指或伸腕时无力或痛（{b('Maudsley 试验、Cozen 试验')}），提示伸肌总腱或骨间后神经问题",
    f"捏住椅子往上提时无力或痛（{b('椅子提举试验')}），也提示伸肌总腱问题",
    f"旋后肌处 Tinel 征阳性提示桡神经问题；{b('没有无力')}的话，病变多在 Frohse 弓近端或桡神经浅支",
    "抗阻旋后时放射性麻木 → 桡神经深支／骨间后神经；肘外侧或肘窝局部痛 → 肱二头肌远端或肱桡滑囊炎",
    f"推的动作（如俯卧撑）时肘有“不稳”的感觉，提示{b('侧副韧带损伤')}，可以请患者在视频里试做一个俯卧撑",
]))
A.append(pic(F(12), "原文图 12：改良 Cozen 试验"))
A.append(pic(F(13), "原文图 13：桡神经三个部位的 Tinel 征"))
A.append(h3("后侧"))
A.append(ul([
    "按压肘后、抗阻伸肘：痛 → 肱三头肌或肘肌损伤；畸形＋淤青 → 肱三头肌腱断裂或骨折",
    f"肘后摸到包块多是{b('鹰嘴滑囊炎')}；要问有无发热、发红、活动受限，{red('警惕感染')}",
]))
A.append(h3("前侧"))
A.append(ul([
    "活动度＋抗阻屈肘、旋前、旋后：痛或无力 → 前外侧（肱二头肌、肱肌、肱桡肌、旋后肌、伸肌总腱、桡神经）或前内侧（旋前肌／屈肌总腱、正中神经）",
    f"{b('勾指试验')}：屈肘 90°，患者自己用手指从侧面勾住肱二头肌远端肌腱。{mk('勾得住说明肌腱连续')}；断裂时常有淤青，肘上方可见包块（肌腹回缩）",
    f"{b('倾斜试验')}：强力过度旋前，肘前外侧痛 → 肱二头肌远端肌腱病或肱桡滑囊炎",
    "肘窝淤青伴前臂外侧或内侧麻木 → 前臂外侧或内侧皮神经损伤",
]))
A.append(pic(F(14), "原文图 14：勾指试验"))
A.append(h3("内侧"))
A.append(ul([
    f"让患者从关节线下方的肘管一路按到内上髁、内上髁沟，再到肱三头肌内侧头。{b('肘管或内上髁沟 Tinel 征')}阳性提示尺神经问题",
    f"{b('屈肘试验')}：屈肘至少 60 秒，出现尺神经分布区（小指侧）的麻木，进一步支持尺神经问题",
    "屈肘时有“滑一下、弹一下”的感觉 → 尺神经半脱位；屈肘时出现第二下弹响 → 常是弹响肱三头肌综合征",
    f"请陪同者做外翻应力，或患者自己做{b('改良挤奶试验')}，查尺侧副韧带；外翻应力至少要在{b('屈肘 30°')}以上做",
    "抗阻屈腕或旋前痛 → 旋前肌／屈肌总腱损伤，或旋前圆肌综合征（正中神经卡压）",
]))
A.append(pic(F(15), "原文图 15：肘管 Tinel 征"))
A.append(pic(F(16), "原文图 16：原文图注称“Phalen 试验”"))
A.append(pic(F(17), "原文图 17：改良挤奶试验"))

A.append(h2("没有视频？电话问诊这样问"))
A.append(p(f"原文表 1～4 把每个检查都改写成了患者能听懂的问题，并列出可能的回答和意义。编者按部位整理成下面两张卡（问题都要{b('左右对比')}）："))
A.append(img(21))
A.append(cap("电话问诊：外侧和内侧（据原文表 1、3 改写）"))
A.append(img(22))
A.append(cap("电话问诊：前侧、后侧和特殊情况（据原文表 2、4 改写）"))
A.append(p(f"视诊和活动度也能在电话里问：“对着镜子看，两边肘一样吗？”“能弯肘摸到肩膀、再伸直吗？”“能摸到头顶吗？”（{b('摸不到头顶提示屈肘不到 130°')}）“屈肘 90°、掌心转向天花板和地面，两边转得一样多吗？痛吗？”"))

A.append(h2("这篇文章能信几分"))
A.append(ul([
    f"期刊归为“原创研究”，但{b('没有受试者，也没有数据')}，本质是作者的经验和文献整理；所有问题和远程试验都{red('没有做过信度、效度验证')}",
    "示范只有一名模特，文中各图、各表的编号多处对不上（见下），读的时候要以检查名称为准",
    "优点：覆盖了肘部四个区域和常见的年龄相关问题，问题设计口语化，可以直接拿来用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('勾指试验写反了')}：原文图 14 图注说“能勾住为阳性，提示肱二头肌腱断裂”。正文说的才对：勾得住说明肌腱连续，勾不住才提示断裂",
    f"{b('表 1、表 2 的说明对调了')}：正文说表 1 是视诊和活动度、表 2 是内侧，实际表 1 是内侧、表 2 是视诊和活动度",
    f"{b('表里引用的图号几乎全错')}：比如表 1 的肘管 Tinel 征写“见图 9”（应为图 15），挤奶试验写“见图 10”（应为图 17）；表 3 的 Cozen 试验写“见图 13”（应为图 12）；表 4 的勾指试验写“见图 15”（应为图 14）",
    f"{b('图 16 和正文说的不是一个试验')}：正文讲的是屈肘试验（屈肘 60 秒，查尺神经），图 16 却是“手背相贴、手指朝下”的腕部反 Phalen 姿势，图注又说提示正中神经问题；表 1 也把屈肘压迫试验写成“可能是正中神经损伤”",
    f"{b('图 9、图 10 放错位置')}：两张图是腕的尺偏／桡偏（原文称“尺侧内收／外展”），正文却在讲肘部弹响时引用它们",
    f"{b('引用了不存在的内容')}：正文两次说“见电话检查部分”（外翻应力的做法、年龄相关疾病），但电话检查部分并没有写这些，它们只出现在表 4",
    f"{b('表 2 的“向外动痛”')}：向内、向外活动痛都写成“屈肌总腱炎”，向外（桡侧）更可能对应伸肌，且两处都把 tendinitis 写成“tender tendinitis”",
    f"{b('作者单位')}：Scottsdale Sports Medicine Institute 的国家写成了“AFG”（阿富汗），应为美国",
    f"{b('Spurling 试验')}：表 4 写“肘痛加重则高度怀疑 C8～T1”，但肘外侧主要是 C5～C6 支配，没有区分内外侧",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"远程看肘，{mk('先看颈椎，再看肘')}；能视频就视频，至少让患者把双肘并排展示、做完屈伸和旋前旋后",
    "提前告诉患者准备好：短袖、能放下手机的位置、一桶牛奶或一瓶水当阻力；有家人在旁边更好",
    f"出现{red('明显畸形、淤青伴肌力突然丧失、肘后红肿发热、孩子拒绝活动肘部')}，不要停留在远程，尽快线下就诊或拍片",
    "远程结果只是初筛，回到门诊再用正式查体和影像确认",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Vomer RP II, Carfagno D, Lewno A, Shah NP, Farford BA, Kieneker L, Pujalte GGA. Elbow evaluation via telephone and video visit. Cureus. 2023;15(6):e39843. doi:10.7759/cureus.39843</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～17 引自原文，编者裁去了视频通话截图中的医生画面，并加了中文标签；活动度卡、抗阻测试卡和电话问诊卡据原文正文和表 1～4 整理改写。"
))

TITLE = "「肘关节」远程怎么查肘？电话＋视频问诊：自我触诊、活动度、抗阻＋Cozen、勾指、挤奶等特殊检查"
PTITLE = "肘关节远程评估推文"
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
