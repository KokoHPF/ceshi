#!/usr/bin/env python3
"""运动员尺侧腕痛（Yamabe 等 2012）推文，尺侧腕痛系列第三篇。

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
    "Yamabe E, Nakamura T, Pham P, Yoshioka H. The athlete's wrist: ulnar-sided pain. Seminars in Musculoskeletal Radiology. 2012;16(4):331-337. doi:10.1055/s-0032-1327006",
    "作者单位：美国加州大学尔湾分校放射科、日本庆应义塾大学医学部骨科",
    f"文章类型：{b('叙述性综述')}（尺侧腕痛系列第三篇：上篇讲解剖与查体，中篇讲影像和治疗，本篇讲运动员）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"运动员的尺侧腕伤可以按{b('投掷、负重、扭转、撞击')}四种机制来想，{mk('问清楚受伤机制是诊断的第一步')}",
    f"不同运动有“招牌伤”：棒球和高尔夫的{b('钩骨钩骨折')}、网球和体操的{b('尺腕撞击综合征')}、赛艇和网球的{b('尺侧腕伸肌腱问题')}",
    f"钩骨钩骨折常规片容易漏，{red('临床怀疑就加特殊体位或直接 CT')}；TFCC 和肌腱问题要靠磁共振",
]))

A.append(h2("一、为什么运动员的尺侧腕伤更麻烦"))
A.append(p(f"尺侧结构负责{b('有力抓握')}和{b('前臂旋转')}，所以比起其他部位的腕伤，尺侧伤对运动员影响更大。腕部结构又小又复杂，非手外科专科的骨科医生有时会漏掉腕骨间韧带损伤或隐匿骨折；处理不当会推迟复出、影响成绩。"))

A.append(h2("二、四种受伤机制"))
A.append(img(2))
A.append(cap("四种受伤机制（编者根据原文整理）"))
A.append(ul([
    f"{b('投掷')}：反复屈伸腕和桡尺偏，过头运动多见，常导致尺侧腕伸肌腱炎和尺侧腕屈肌腱炎",
    f"{b('负重')}：上肢当腿用，腕部反复承受高压力，TFCC 首当其冲",
    f"{b('扭转')}：用力旋转腕关节，多损伤下尺桡关节或尺侧腕骨",
    f"{b('撞击')}：直接撞击或摔倒手撑地，可致钩骨骨折、韧带损伤、TFCC 撕裂等",
]))

A.append(h2("三、不同运动的“招牌伤”"))
A.append(img(3))
A.append(cap("不同运动的尺侧腕痛（编者根据原文整理）"))
A.append(h3("棒球"))
A.append(ul([
    "腕伤大多是被球直接打中，其次是与人或外场围栏相撞；扭伤占 33%，骨折占 46%",
    f"{b('击球手的钩骨钩骨折多在非利手')}：不是被球打到，而是擦棒（打成界外球）时球棒尾端的反作用力顶到钩骨钩",
    "腕过伸位滑垒可伤 TFCC；投掷引起腕伸、屈肌腱炎；击球可引起尺侧腕伸肌腱半脱位或脱位",
]))
A.append(h3("网球等球拍类运动"))
A.append(ul([
    "网球运动员上肢伤占 20%～45%，其中 7.7% 在腕部",
    f"所有击球瞬间腕都在背伸位，{b('发球时还加上尺偏')}，水平越高背伸越多——这可能是尺侧伤多的原因",
    f"常见：TFCC 损伤、尺侧腕伸肌腱炎和半脱位、钩骨钩骨折；{mk('尺腕撞击综合征是网球运动员的特征性损伤')}，症状和 TFCC 撕裂很像，因为持续撞击本身就会压伤 TFCC",
]))
A.append(h3("高尔夫"))
A.append(ul([
    "职业球员受伤最多的部位是左腕（占 24%）；业余球员手腕伤占 20%",
    "右手球员的左腕伤多是 de Quervain 腱鞘炎、桡侧撞击综合征等桡侧问题",
    f"尺侧主要是{b('击球时钩骨钩骨折')}；杆头打到地面也可伤 TFCC",
]))
A.append(h3("体操"))
A.append(ul([
    f"上肢变成负重肢体，腕在{b('背伸位受压')}，再加桡尺偏，伤病率比肘和肩还高",
    f"{b('46%～87%')} 的精英体操运动员职业生涯中有腕痛；尺腕撞击综合征是最常见的尺侧腕痛之一",
]))

A.append(h2("四、鉴别诊断和影像要点"))
A.append(h3("尺骨茎突骨折"))
A.append(pic(4, "原文图 1：尺骨茎突基底骨折合并桡骨远端骨折"))
A.append(ul([
    "常合并桡骨远端骨折（Frykman 报道桡骨远端骨折中 61% 合并尺骨茎突骨折）；单纯茎突骨折多为直接打击",
    "正位片就能诊断，按骨折位置分为尖部、中部、基底、基底斜形 4 型",
    f"{red('基底和基底斜形骨折累及三角韧带（桡尺韧带）')}，可致下尺桡关节不稳，要加做磁共振看韧带；尖部和中部骨折一般不影响稳定，预后好",
]))
A.append(pic(5, "原文图 2：尺骨茎突骨折分型"))
A.append(h3("钩骨骨折"))
A.append(ul([
    "分钩骨体骨折和钩骨钩骨折，可单独或同时发生，表现为腕尺侧半疼痛、局部肿胀压痛",
    f"棒球、网球、壁球、高尔夫运动员腕尺侧{b('深部疼痛')}，要高度怀疑钩骨钩骨折。棒球和高尔夫多在{b('非利手')}，球拍类多在{b('利手')}；也可见于小鱼际着地摔倒",
    "正位片线索：钩骨钩消失、皮质环征（钩骨钩的环形影）异常、钩区硬化；但常规正侧位常常看不出",
    f"加拍：{b('腕管位')}（急性疼痛腕背伸不够时难拍）、{b('腕背伸旋后斜位')}、拇指外展经虎口的侧位",
    f"{mk('CT 更可靠')}：敏感度 100%、特异度 94%、准确度 97.2%；X 线分别只有 72%、88%、80.5%",
    "钩骨体骨折分近极、内侧结节、矢状斜形、背侧冠状 4 型；多数正侧位能看到，骨折线斜行时要仔细看",
]))
A.append(pic(6, "原文图 3：钩骨钩骨折的特殊体位 X 线"))
A.append(pic(7, "原文图 4：钩骨钩骨折的 CT 和三维 CT"))
A.append(h3("小指掌骨基底骨折和豌豆骨骨折"))
A.append(ul([
    f"{b('第 5 掌骨基底骨折')}属于钩骨－掌骨关节内骨折，多由沿第 5 掌骨长轴的纵向暴力或直接打击引起。X 线容易发现，但{b('范围常被低估')}；推荐前臂从中立位旋后 60° 拍正位，避开骨重叠",
    f"{b('豌豆骨骨折')}约占腕骨骨折 2%，多为小鱼际直接撞击，也可因反复创伤（豌豆骨是尺侧腕屈肌腱里的籽骨）。骨很小，常规片难发现，要加旋后斜位、腕管位或 CT",
]))
A.append(pic(8, "原文图 5：小指掌骨基底关节内骨折"))
A.append(pic(9, "原文图 6：豌豆骨骨折的 CT"))
A.append(h3("TFCC 损伤"))
A.append(ul([
    "TFCC 既稳定下尺桡关节、又承担腕骨的压力负荷；由关节盘、半月板同源物、尺月韧带、尺三角韧带、三角韧带（掌、背侧桡尺韧带）和尺侧副韧带组成",
    f"外伤机制：腕{b('背伸＋旋前位')}受轴向负荷（摔倒手撑地）；球拍运动中作用于前臂掌侧的牵拉力也可致伤。{b('尺骨正变异')}是解剖上的危险因素",
    "X 线（中立位正位＋侧位）看不到 TFCC 本身，但能看腕骨排列、茎突形态、下尺桡关节和最重要的尺骨变异；正变异可能伴月骨尺侧半软骨软化或囊变",
    f"关节造影：造影剂从下尺桡关节漏到桡腕关节（或反过来），{b('高度怀疑三角韧带从尺骨小凹撕脱')}",
    f"{mk('磁共振已是 TFCC 损伤最有用的检查')}，必须高分辨率；常规磁共振看 TFCC 尺侧周边附着常不清楚，压脂 T1 磁共振关节造影更好",
]))
A.append(pic(10, "原文图 7：掰手腕选手的 TFCC 损伤 X 线"))
A.append(pic(11, "原文图 8：腕关节造影"))
A.append(pic(12, "原文图 10：柔道运动员的三角韧带撕脱"))
A.append(h3("尺腕撞击综合征"))
A.append(ul([
    "尺骨头和尺侧腕骨相撞，导致尺侧腕痛和尺侧退变",
    "X 线最常见尺骨正变异，但零变异和负变异也可能发生；间接征象是月骨尺侧近端、三角骨、尺骨头软骨下硬化或囊变",
    f"磁共振能看到软骨退变或缺损、骨髓水肿、囊变、硬化，{b('比 X 线早得多')}",
]))
A.append(h3("尺侧腕伸肌腱和尺侧腕屈肌腱"))
A.append(ul([
    f"尺侧腕伸肌腱靠尺骨头沟里的深层支持带（腱下鞘）固定。{b('赛艇、需要“甩腕”的球拍运动')}反复刺激，可致狭窄性腱鞘炎、腱鞘撕裂或肌腱半脱位／脱位",
    f"{red('它和 TFCC 损伤很难靠查体分开')}，因为腱下鞘本身就是 TFCC 的重要稳定结构。X 线看不出，磁共振可见肌腱增粗、信号增高，腱鞘内积液提示活动性腱鞘炎",
    f"{b('尺侧腕屈肌腱炎')}与反复尺偏（如锤击）有关，见于壁球、羽毛球、高尔夫；切线位 X 线有时见钙化，梯度回波磁共振对钙化更敏感",
]))
A.append(pic(13, "原文图 11：赛艇运动员尺侧腕伸肌腱脱位"))
A.append(pic(14, "原文图 12：网球运动员尺侧腕伸肌腱鞘炎"))
A.append(img(15))
A.append(cap("怀疑什么，先拍什么（编者根据原文整理）"))

A.append(h2("这篇综述能信几分"))
A.append(ul([
    f"{b('叙述性综述')}，篇幅短（7 页、19 篇参考文献），没有检索方法；流行病学数据多来自 1980～1990 年代的老研究",
    "放射科作者所写，侧重影像，几乎没有讲治疗和重返运动（治疗可参考本系列中篇）",
    "配图都是作者单位的运动员病例，真实但只是个例",
    "优点：按受伤机制和运动项目梳理尺侧腕痛，问病史时很好用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“稳定”写成了反义')}：尺骨茎突基底骨折累及三角韧带，原文写“can lead to DRUJ {red('stability')}”，按上下文应为 instability（不稳）",
    f"{b('桡侧伤混进尺侧清单')}：撞击伤列举“尺侧腕伤”时包括了{red('舟月分离')}，舟月韧带在腕桡侧",
    f"{b('图 2 拼写')}：标注写“Meniscus homogogue”，应为 homologue（同源物）",
    f"{b('重复表述')}：肌腱病“T1 和 T2 加权像信号都增高，以及 T2 加权像”，T2 重复出现",
    f"{b('参考文献')}：正文写 Frykman，文献表写成“Fyrkman”；茎突骨折分型引用的第 10 篇文献当时标为“In press”（尚未发表）",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先问运动项目和受伤动作')}：持拍／持棒手还是非利手、是撞击还是反复负荷、发生在哪个技术动作",
    f"握拍、握棒的运动员小鱼际深部痛，{b('先排除钩骨钩骨折')}，X 线阴性不等于没事",
    f"体操和网球运动员的慢性尺侧痛，想到{b('尺腕撞击')}，看尺骨变异",
    f"赛艇、网球运动员旋后时腕背尺侧痛或弹响，查{b('尺侧腕伸肌腱')}稳定性，并和 TFCC 损伤一起考虑",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Yamabe E, Nakamura T, Pham P, Yoshioka H. The athlete's wrist: ulnar-sided pain. Semin Musculoskelet Radiol. 2012;16(4):331-337. doi:10.1055/s-0032-1327006</em><br>"
    "原文版权归 Thieme Medical Publishers 所有，非开放获取。本文为学术交流中文解读：原文图 1～8、10～12 引自原文，图中中文标签为编者所加；机制卡、运动卡和影像速查卡为编者整理。原文图 9 为经许可转载自其他出版物的图片，本文未使用。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「尺侧腕痛」运动员手腕小指侧痛：棒球、网球、高尔夫、体操各伤哪儿？影像怎么查（下）"
PTITLE = "运动员尺侧腕痛推文"
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
