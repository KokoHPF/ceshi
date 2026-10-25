#!/usr/bin/env python3
"""尺侧腕痛 Part I 解剖与体格检查（Vezeridis 等 2010）推文。

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
    "Vezeridis PS, Yoshioka H, Han R, Blazar P. Ulnar-sided wrist pain. Part I: anatomy and physical examination. Skeletal Radiology. 2010;39(8):733-745. doi:10.1007/s00256-009-0775-x",
    "作者单位：美国哈佛医学院布莱根妇女医院骨科与放射科、加州大学尔湾分校放射科",
    f"文章类型：{b('叙述性综述')}（上篇讲解剖与查体，下篇讲影像）",
], square=True))

A.append(h2("先说为什么难"))
A.append(p(f"尺侧腕痛很常见，但结构{b('小而复杂')}，影像表现又常常不明显，手外科和放射科都觉得难。{mk('熟悉解剖＋系统查体')}，是找到病因的前提。"))

A.append(h2("重点一：尺侧腕部解剖"))
A.append(h3("骨与关节"))
A.append(pic(2, "原文图 1：Gilula 弧线"))
A.append(ul([
    "尺骨远端有尺骨头（与桡骨形成下尺桡关节）和尺骨茎突（尺侧副韧带起点）；两者之间的浅凹（小凹）是三角纤维软骨的附着处",
    f"{b('尺骨变异')}：尺骨与桡骨远端关节面的长度差。{red('正变异')}与 TFCC 撕裂、尺腕撞击综合征关系密切（TFCC、月骨、三角骨、尺骨头软骨退变）；负变异与月骨缺血坏死（Kienböck 病）的关系仍有争议",
    "月骨是腕部最常脱位、第二常骨折的骨；三角骨与钩骨形成“螺旋状”关节；豌豆骨在尺侧腕屈肌腱内，豌豆三角关节有 12%～25% 不与桡腕关节相通",
    f"{b('下尺桡关节')}：从旋前到旋后，尺骨头相对桡骨转约 150°，靠掌、背侧桡尺韧带和 TFCC 稳定；真侧位片上桡尺骨应重叠，不重叠提示下尺桡关节损伤",
]))
A.append(pic(3, "原文图 2：Ⅰ型和Ⅱ型月骨"))
A.append(h3("韧带：月三角韧带"))
A.append(pic(4, "原文图 3：月三角韧带近侧部的正常变异"))
A.append(ul([
    "U 形，分背侧、近侧、掌侧三部分：背侧部限制旋转，掌侧部最厚最强，近侧部是薄的纤维软骨",
    "月三角韧带撕裂时 X 线常正常；关节造影也可能把年龄相关的穿孔误当撕裂",
    f"近侧部在磁共振上 {b('>85%')} 呈三角形，约 2/3 的人有线状中高信号——{mk('不熟悉正常变异容易误判为撕裂')}",
]))
A.append(h3("三角纤维软骨复合体（TFCC）"))
A.append(pic(5, "原文图 4：TFCC 的磁共振表现"))
A.append(ul([
    "组成：关节盘、半月板同源物、尺月韧带、尺三角韧带、掌背侧桡尺韧带、尺侧副韧带等；作用是稳定下尺桡关节、在腕骨和尺骨之间传递轴向负荷",
    "大部分有两个尺骨附着点：茎突尖（远层）和小凹（近层）",
]))
A.append(pic(6, "原文图 5：TFCC 的血供"))
A.append(pic(7, "原文图 6：尺骨正变异、零变异、负变异"))
A.append(p(f"高分辨率磁共振显示：尺骨变异平均 +0.26 mm；尺骨变异越大，TFCC 角度越大（r＝0.84）、{b('TFCC 越薄')}（r＝−0.71）。薄的 TFCC 更不耐受应力。"))
A.append(h3("神经血管和肌腱"))
A.append(pic(8, "原文图 8：Guyon 管"))
A.append(ul([
    "Guyon 管在中段把尺神经、尺动脉分为深、浅支；出管后浅支尺动脉紧贴钩骨钩，没有保护，容易受伤",
    f"{b('尺侧腕伸肌腱')}在第 6 背侧间室、尺骨背外侧沟内，止于第 5 掌骨；{b('尺侧腕屈肌腱')}止于豌豆骨",
]))
A.append(pic(9, "原文图 9：尺侧腕伸肌腱随旋前旋后移动"))

A.append(h2("重点二：查体"))
A.append(img(10))
A.append(cap("查体顺序和正常活动度（编者根据原文整理）"))
A.append(ul([
    f"{b('Allen 试验')}：让患者反复用力握拳驱血，紧握时检查者同时压住桡、尺动脉；患者张手后松开其中一条，观察手掌是否迅速转红；再换另一条",
    "测腕屈伸肌力时让患者握拳，避免屈指肌代偿屈腕",
]))
A.append(h3("触诊：由近到远"))
A.append(ul([
    f"{b('尺骨和下尺桡关节')}：急性损伤时压痛、旋转受限；背侧脱位可见腕背隆起，前臂卡在旋前位",
    f"{b('月骨')}：压痛伴活动度下降，要想到 Kienböck 病",
    f"{b('三角骨')}：腕桡偏时在尺骨茎突远侧摸到；{b('月三角间隙')}：屈腕 30°，在第 4、5 背侧间室之间、下尺桡关节远侧一横指处",
    f"{b('豌豆骨')}：沿尺侧腕屈肌腱向远摸，在腕横纹处；球拍运动的屈腕和直接压迫会加重豌豆三角关节炎",
    f"{b('钩骨钩')}：从豌豆骨向第 2 掌骨头连线，距豌豆骨约 2 cm 处",
    f"{b('尺侧腕伸肌腱')}：查有无越过尺骨茎突的半脱位（外伤后旋前时可能听到“啪”一声）；{b('TFCC')}：摸豌豆骨、尺侧腕屈肌腱和尺骨茎突之间的凹陷",
]))
A.append(pic(11, "原文图 12：下尺桡关节背侧脱位"))
A.append(pic(12, "原文图 13：Kienböck 病"))
A.append(pic(13, "原文图 14：尺侧腕伸肌腱鞘炎伴部分断裂"))
A.append(h3("特殊检查"))
A.append(pic(14, "原文图 15：琴键试验"))
A.append(pic(15, "原文图 16：月三角冲击试验"))
A.append(img(16))
A.append(cap("特殊检查速查（编者根据原文整理）"))

A.append(h2("这篇综述能信几分"))
A.append(ul([
    f"{b('叙述性综述')}：没有给出各检查的敏感度、特异度，只说“敏感”“有用”",
    "作者之一是放射科医生，解剖部分偏重磁共振表现，部分结论来自作者团队自己的研究",
    "优点：解剖讲得系统，触诊定位和特殊检查描述清楚，适合作查体参考",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“Ⅱ型”指的不同')}：前文说月骨远端多一个与钩骨相关节的小面叫“Ⅱ型月骨”（发生率 50%～73%），后文又说三角钩关节与头月关节被钩月小面分开的情况占 20%、也叫“Ⅱ型月骨”，两个比例对不上",
    f"{b('神经分布写错')}：说桡神经支配拇、示、{red('环指')}背侧到远节指间关节，应为拇、示、中指和环指桡侧半；又说尺神经支配“腕、手、环小指的背侧和{red('桡侧')}面”，应为尺侧",
    f"{b('毛细血管再充盈')}：原文写正常 <5 秒，通常标准是 <2 秒",
    f"{b('尺侧腕伸肌腱')}：解剖部分写它在尺骨“背外侧”沟内，应为背内侧（尺侧）",
    f"{b('Guyon 管')}：一处写豌豆骨在“尺侧”、钩骨钩在“桡侧”，图 8 图注却写“Guyon 管位于豌豆骨桡侧”，表述角度不同容易混淆",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('按解剖分区想病因')}：尺骨头 / 下尺桡关节、TFCC、月三角、豌豆三角、钩骨钩、尺侧腕伸肌腱、Guyon 管",
    f"{b('先触诊定位最痛点')}，再选特殊检查：尺骨小凹征查 TFCC 小凹附着，琴键试验查下尺桡关节，冲击试验查月三角",
    f"{b('尺腕应力试验阳性不代表就是尺腕撞击')}，只能说明有关节内问题",
    "所有检查与对侧比较；影像（尤其高分辨率磁共振）看正常变异时要谨慎",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Vezeridis PS, Yoshioka H, Han R, Blazar P. Ulnar-sided wrist pain. Part I: anatomy and physical examination. Skeletal Radiol. 2010;39(8):733-745. doi:10.1007/s00256-009-0775-x</em><br>"
    "原文以知识共享署名-非商业性使用（CC BY-NC）协议开放获取，版权归原作者所有。本文为非商业的学术交流中文解读：原文图 1～6、8、9、12～16 引自原文，图中中文标签为编者所加；查体卡和速查卡为编者整理。原文图 10、11 为经许可转载自其他出版物的图片，本文未使用。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「尺侧腕痛」手腕小指侧痛怎么查？解剖要点＋触诊定位＋6 个特殊检查（上）"
PTITLE = "尺侧腕痛查体推文"
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
