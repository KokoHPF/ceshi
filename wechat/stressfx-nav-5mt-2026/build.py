#!/usr/bin/env python3
"""《舟骨与第五跖骨基底应力骨折：图解解剖综述》（Liu、Dalmau-Pastor 等 2026 KSSTA）推文。

用法：python3 tools/make_figs.py work images <中号字体> <粗体> && python3 build.py → article_body.html 和 preview.html
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
    "Liu X, Hong CC, Reina F, Carrera A, Alcolea-Madera E, Del Vecchio JJ, Dalmau-Pastor M. Navicular and fifth metatarsal base stress fractures: An illustrated anatomical review. Knee Surg Sports Traumatol Arthrosc. 2026;34:3135–3149. doi:10.1002/ksa.70413",
    "作者单位：西班牙巴塞罗那大学人体解剖与胚胎学教研室；遵义医科大学附属医院骨科；新加坡国立大学医院骨科；西班牙赫罗纳大学 等",
    f"文章类型：{b('图解解剖综述')}（以尸体标本照片为主，没有新的临床数据）；CC BY 开放获取",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"舟骨和第五跖骨近端分别是足{b('内侧柱和外侧柱')}的关键骨，两处都是{b('应力骨折高发、又容易延迟愈合、不愈合、再骨折')}的部位",
    f"共同原因是两条：{red('局部血供差')} + {red('受力复杂')}。舟骨的薄弱点在{b('中 1/3')}，第五跖骨的薄弱点在{b('干骺端-骨干交界（Jones 区）和近端骨干')}",
    f"舟骨要同时扛{b('纵向压力、横向拉力和侧向剪力')}，而松质骨抗拉能力只有抗压的约 70%；中 1/3 正对查体的{b('“N 点”')}",
    f"第五跖骨近端受{b('扭转、弯曲和肌腱牵拉')}；{b('加速动作')}时弯矩最大。基底横行骨折主要是{b('跖腱膜外侧束')}拉出来的，而不是腓骨短肌",
    f"周围软组织（弹簧韧带、胫后肌腱；腓骨短肌、跖腱膜外侧束、第三腓骨肌）既维持足弓，也是骨折的“拉力源”",
]))

A.append(h2("Part 1  舟骨"))
A.append(h3("一、骨性解剖"))
A.append(p(f"舟骨位于足内侧纵弓的顶部，和跟骰关节一起构成跗横关节（Chopart 关节），是{b('连接后足和前足的“桥”')}，负责传递负荷、支撑体重。名字来自拉丁语 navis（船），因为它形似小船。"))
A.append(pic(2, "原文图 1  舟骨（a）后方与距骨（b）相关节，前方与内侧（c）、中间（d）、外侧（e）三块楔骨相关节；（1）为足背动脉分支的血管进入点"))
A.append(pic(3, "原文图 2  右侧舟骨六个方向观（编者中文标注）：前关节面两条细嵴分出对应三块楔骨的小关节面；足底侧汇聚成“舟骨喙”（1）；内侧是舟骨结节（2）"))
A.append(img(4))
A.append(cap("舟骨骨性特点（据原文整理）"))
A.append(p(f"值得注意的是后关节面：它和距骨头构成{b('椭圆形球窝关节')}，但并不完全包住距骨头。如果关节面{b('凹得更深、杯更高、朝向更偏近端')}，关节匹配度下降，临床上可能和扁平足、内侧纵弓塌陷、前足外展有关。"))

A.append(h3("二、周围软组织"))
A.append(h4("1. 弹簧韧带复合体"))
A.append(pic(5, "原文图 3  距跟舟关节：距骨头没有骨性覆盖的部分由弹簧韧带复合体中的纤维软骨承托。（1）距骨头对弹簧韧带的关节面（2）弹簧韧带复合体（3）～（5）三角韧带浅层的胫舟束、胫弹簧束、胫跟束"))
A.append(pic(6, "原文图 4  去掉距骨后，弹簧韧带复合体和骨一起围成容纳距骨头的“窝”。（1）跟舟足底韧带（下束）（2）跟舟内上韧带（3）～（5）三角韧带浅层各束"))
A.append(img(7))
A.append(cap("弹簧韧带复合体（据原文整理）"))
A.append(p(f"弹簧韧带复合体从内下方“兜住”距骨头，和胫后肌腱一起提供站立、行走时的动态稳定。作者特别强调它和{b('三角韧带浅层')}的联动：胫弹簧束恒定止于跟舟内上韧带上缘，三角韧带浅层受伤可能让弹簧韧带变松；反过来，弹簧韧带损伤又会加重三角韧带负荷。{b('两者要一起评估')}，避免漏诊。"))
A.append(h4("2. 背侧韧带和胫后肌腱"))
A.append(pic(8, "原文图 5  舟骨背侧韧带：（1）距舟背侧韧带（2）～（4）舟骨与内、中、外侧楔骨之间的背侧韧带（5）舟骰背侧韧带"))
A.append(pic(9, "原文图 6  胫后肌腱（TPT）在舟骨的止点和延伸。（a）内侧观（b）（c）足底观，TPT 延伸到足底舟楔韧带和第 2、3 跖骨基底；（2）趾长屈肌腱（3）拇长屈肌腱（4）腓骨长肌腱"))
A.append(img(10))
A.append(cap("背侧韧带与胫后肌腱（据原文整理）"))

A.append(h3("三、舟骨为什么容易应力骨折"))
A.append(p(f"作者认为舟骨应力骨折是{b('内因 + 外因')}共同作用的结果。从解剖角度看，主要是两点："))
A.append(pic(11, "原文图 7  灌注红色树脂后塑化的矢状切面。左：足底内侧动脉分支经弹簧韧带复合体进入舟骨足底部；右：足背动脉分支进入舟骨背侧"))
A.append(img(12))
A.append(cap("舟骨应力骨折的解剖原因（据原文整理）"))
A.append(ul([
    f"{b('血供不均')}：滋养孔集中在背侧，内侧最少，前后关节面没有；中央区（尤其背侧中 1/3）乏血管，微损伤积累后修复不过来。不过也有研究发现 {b('58.8%')} 的舟骨骨内血供致密、没有乏血管区，说明力学因素可能更重要",
    f"{b('受力复杂')}：中足诸骨中舟骨的拉应力最大（主要来自弹簧韧带和胫后肌腱的牵拉），同时纵向受压、还要承受第 2 跖列传来的侧向剪力；三种力集中在较窄较弱的{mk('中 1/3')}",
    f"{b('查体对应')}：这个位置正好是舟骨应力骨折的特征性压痛点{b('“N 点”')}",
]))
A.append(p(f"作者还从血供角度提出一个{b('推测')}：背侧钢板需要掀起骨膜，可能破坏背侧血供；螺钉对骨膜破坏更小，{b('可能')}更利于愈合。这只是基于解剖的假设，没有临床数据。"))

A.append(h2("Part 2  第五跖骨基底"))
A.append(p(f"第五跖骨近端应力骨折是下肢最常见的过用损伤之一，多见于{b('跑步、篮球、足球')}等高冲击运动。起病隐匿，常只是足外侧说不清的不适，{b('容易误诊、延误')}；一旦延误，延迟愈合、不愈合、再骨折的发生率都很高。"))
A.append(h3("一、骨性解剖与分区"))
A.append(pic(13, "原文图 8  第五跖骨四个方向观（编者中文标注）。从近到远：基底（含结节）、干骺端-骨干交界、骨干、颈、头"))
A.append(pic(14, "原文图 9（截取基底部分，编者加中文图例）  第五跖骨近端分区"))
A.append(img(15))
A.append(cap("分区与关节面（据原文整理）"))
A.append(table(["分区", "位置", "对应骨折", "特点"], [
    ["1 区", "近侧线以近（结节）", "撕脱骨折", "血供丰富，愈合潜力强；再分 A/B/C"],
    ["2 区", "两线之间（干骺端-骨干交界）", "Jones 骨折", "乏血管区；多累及第 4/5 跖间关节软骨"],
    ["3 区", "远侧线以远 1.5 cm", "近端骨干应力骨折", "乏血管区，易延迟愈合、不愈合"],
]))
A.append(small("分区线：以第 4/5 跖骨间关节的近、远端为参照，垂直于第五跖骨长轴画两条线（Lawrence 和 Botte 分区）。"))
A.append(p(f"有两个细节对手术有提示：第 4/5 跖间关节面约 {b('48%')} 覆盖平坦软骨、软骨长约 9.5 mm，所以{b('Jones 骨折大多会累及关节软骨')}，置钉要避开这一区域；1 区骨折累及 A、B 还是 C 亚区，决定有没有肌肉动态牵拉、是否累及关节面，进而影响稳定性和是否手术。"))

A.append(h3("二、血供"))
A.append(pic(16, "原文图 10  塑化矢状切面。左：基底与骰骨的关节线；右：血管进入结节，中央区供血较少"))
A.append(img(17))
A.append(cap("第五跖骨血供（据原文整理）"))
A.append(p(f"一句话：{b('结节血供丰富，愈合好；干骺端-骨干交界和近端骨干是相对乏血管区')}。滋养动脉在近、中 1/3 交界内侧穿入，向近端只走到交界附近，所以这里骨折容易伤及骨内血供——这也是 Jones 骨折“难长”的解剖基础。"))

A.append(h3("三、止于基底的三条结构"))
A.append(pic(18, "原文图 11  止于第五跖骨结节的两条肌腱：（1）腓骨短肌（2）第三腓骨肌，它同时止于第 4 跖骨基底"))
A.append(pic(19, "原文图 12  足外侧解剖：（1）第三腓骨肌腱（2）腓骨短肌腱（3）跖腱膜外侧束"))
A.append(img(21))
A.append(cap("三条附着结构（据原文整理）"))
A.append(pic(20, "据原文数字绘制：第三腓骨肌在各研究中的出现率为 88.2%～100%，过去当作变异，其实是大多数人都有的恒定肌肉"))

A.append(h3("四、受力"))
A.append(img(22))
A.append(cap("第五跖骨近端的受力（据原文整理）"))
A.append(ul([
    f"{b('扭转')}：2 区外侧和 3 区受扭转，近段相对远段内旋，可促进应力骨折进展、骨折后造成旋转移位",
    f"{b('弯曲')}：{mk('加速动作时弯矩最大')}，其次是直线跑；增加加速训练或跑量可能打破骨吸收与形成的平衡",
    f"{b('牵拉')}：腓骨短肌对近端骨块有移位力，Jones 骨折中更明显，止点以远的骨折更不稳定，也是 Jones 术后不稳的来源之一；基底横行骨折则主要由{b('跖腱膜外侧束')}撕脱，切断外侧束后即使腓骨短肌完好也无法诱发骨折",
]))

A.append(h2("两块骨放在一起看"))
A.append(img(23))
A.append(cap("舟骨 vs 第五跖骨近端（编者据原文整理）"))

A.append(h2("原文对不上的地方"))
A.append(ul([
    f"舟骨部分通篇讲应力骨折，小结却突然改成讨论{b('舟骨缺血性坏死（AVN）')}，说它“不是单纯缺血而是多因素疾病”，前文并未展开",
    f"第五跖骨部分的数字有重复使用：跖腱膜外侧束和腓骨短肌附着区“距外侧缘”都是 {b('11.5 ± 0.9 mm')}，非关节区宽度也是这个数；腓骨短肌附着“长度 10.2 ± 2.2 mm”、外侧束“长度 9.5 ± 2.9 mm”与前文“距近端缘”的数值完全相同",
    f"说第三腓骨肌“只附着在 1 区远侧”，但同一段又说它可止于{b('骨干（45%）')}或基底与骨干两处",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Liu X, Hong CC, Reina F, Carrera A, Alcolea-Madera E, Del Vecchio JJ, Dalmau-Pastor M. Navicular and fifth metatarsal base stress fractures: An illustrated anatomical review. Knee Surg Sports Traumatol Arthrosc. 2026;34:3135–3149. doi:10.1002/ksa.70413</em><br>"
    "原文为 CC BY 开放获取（© 2026 The Author(s)）。本文为中文解读：原文图 1～12 引自原文，其中图 2、图 8 的方位标签由编者译为中文，图 9 截取基底部分并加中文图例；其余整理卡和数据图由编者根据原文撰写、绘制。"
))
TITLE = "「足踝」舟骨和第五跖骨基底：为什么容易应力骨折、又难长好？一篇图解解剖综述讲清楚"
PTITLE = "舟骨与第五跖骨应力骨折推文"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<!DOCTYPE html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>""" + PTITLE + """</title>
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
