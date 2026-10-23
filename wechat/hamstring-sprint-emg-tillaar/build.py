#!/usr/bin/env python3
"""高速跑与多种腘绳肌强化训练的肌电比较（van den Tillaar 等 2017）推文。

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
    "van den Tillaar R, Solheim JAB, Bencke J. Comparison of hamstring muscle activation during high-speed running and various hamstring strengthening exercises. Int J Sports Phys Ther. 2017;12(5):718-727. doi:10.16603/ijspt20170718",
    "作者来自挪威北方大学、丹麦哥本哈根大学医院",
    "实验室横断面肌电研究（同一批人做冲刺和全部动作）",
], square=True))

A.append(h2("先说为什么要拿冲刺跑当标尺"))
A.append(p(
    f"腘绳肌拉伤占运动损伤的 12%～24%，多数发生在{b('高速跑')}时。冲刺时腘绳肌在{b('摆动末期')}要离心收缩、刹住往前甩的小腿，这是最容易拉伤的时刻。"
))
A.append(p(
    f"大家练腘绳肌常用北欧挺等动作，但{mk('这些动作到底能把腘绳肌激活到冲刺时的几成？发力时的髋、膝角度像不像冲刺？')}以前没人直接比过。"
    f"这篇就把冲刺跑的肌电峰值当作 100%，看 7 个常用动作各能达到多少。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"对象：{b('12 名男性体育专业学生')}（平均 25 岁），都有下肢力量训练经验，过去一年没有腘绳肌拉伤",
    f"先在无动力弧形跑台上做一次全力冲刺（平均最高速度约 22.5 km/h），再按随机顺序做 7 个动作，每个做 3 次，间隔休息 5 分钟",
    f"在右腿{b('半腱肌、半膜肌、股二头肌')}贴表面肌电电极，同时用 8 台摄像机的三维动作捕捉记录髋、膝角度",
    "每个动作的肌电峰值都换算成“冲刺峰值的百分比”，并记录峰值出现时的髋、膝角度",
]))

A.append(h2("重点：7 个动作怎么做"))
A.append(h3("踢腿类：快速、单腿"))
A.append(pic(2, "原文图 1A、1B：仰卧踢腿、站立踢腿（原图为负片，编者已反相，字母改为中文）"))
A.append(ul([
    f"{b('① 仰卧踢腿')}：仰卧，双肩、臀部和{b('右脚跟')}着地；左腿猛地向上踢，借势让右脚离地、再落回。练的是{b('支撑腿（右腿）')}的腘绳肌，相当于一个爆发式单腿臀桥",
    f"{b('② 站立踢腿')}：左腿站立，右膝抬起后，右脚快速向前踢出，模拟跑步摆动末期的伸膝",
]))
A.append(h3("北欧挺及两个变式"))
A.append(pic(3, "原文图 1C～1E：北欧挺、北欧挺 + 回起、北欧挺 + 推拉"))
A.append(ul([
    f"{b('③ 北欧挺')}：跪姿，双脚被绑带固定；{mk('髋和背保持一条直线')}向前倒，撑不住时松开，用双手做离心俯卧撑缓冲",
    f"{b('④ 北欧挺 + 回起')}：同样向前倒，但在撑不住之前，用腘绳肌把身体{b('拉回直立')}",
    f"{b('⑤ 北欧挺 + 推拉')}：向前倒到能控制的极限，在这个位置把 {b('5 kg 重物')}尽快向前推出、再拉回",
]))
A.append(h3("鹤式及其变式"))
A.append(pic(4, "原文图 1F、1G：鹤式、鹤式 + 回起"))
A.append(ul([
    f"{b('⑥ 鹤式')}：同样固定双脚，但{b('先屈髋到 90°')}、躯干保持水平，再伸膝向前倒，撑不住时用双手离心缓冲",
    f"{b('⑦ 鹤式 + 回起')}：同鹤式，在撑不住之前拉回起始位置",
]))

A.append(h2("结果：谁也没超过冲刺"))
A.append(pic(5, "原文图 2 重绘：以冲刺跑为 100%，各动作的腘绳肌肌电峰值（数值为编者按原图估读）"))
A.append(ul([
    f"{b('总体')}：各动作的肌电峰值大约是冲刺时的：半腱肌 40%～65%、{red('股二头肌只有 18%～40%')}、半膜肌 40%～75%",
    f"{b('最高的')}：{mk('仰卧踢腿和三个北欧挺')}。半膜肌在仰卧踢腿时约 77%，是唯一和冲刺没有统计学差异的",
    f"{b('最低的')}：两个鹤式；站立踢腿对半膜肌也偏低",
    f"{b('北欧挺的变式')}：回起、推拉并没有比标准北欧挺更高，可以当作变化穿插使用",
]))
A.append(pic(6, "原文图 3：各动作肌电峰值出现时的髋、膝角度（三块肌肉平均；* 髋角与冲刺有差异，† 膝角与冲刺有差异）"))
A.append(ul([
    f"{b('北欧挺系列')}：峰值时的髋、膝角度{mk('和冲刺相近')}，说明练到了冲刺时“该用力”的那段位置",
    f"{b('鹤式')}：髋更伸直（约 155° vs 冲刺 123°），肌肉长度不同，激活也低",
    f"{b('站立踢腿')}：髋屈得多（约 81°），而且没有外加负荷，激活低",
    f"{b('仰卧踢腿')}：激活高，但{b('膝屈得多')}（约 103° vs 冲刺 126°），角度和冲刺不太像。作者认为把支撑脚放得更远（膝更伸直）可能更接近冲刺",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('样本小')}：只有 12 名男性，标准差很大，很多差异可能检测不出来；女性和受伤运动员不一定适用",
    f"{b('参照标准特殊')}：用冲刺峰值而不是最大自主收缩做 100%，再套用“达到 70% 最大自主收缩才有力量训练效果”这条线，两者是否等价有争议",
    f"{b('表面肌电的局限')}：半腱肌和半膜肌靠得很近，表面电极之间可能有串扰；冲刺时的峰值又容易受动作伪影影响",
    f"{b('肌电高 ≠ 训练效果好')}：这只是一次性的激活测量，不是训练研究。北欧挺之所以能预防拉伤，有训练和预防研究支持；仰卧踢腿还没有",
    f"{b('熟练度不一')}：有人练过这些动作，有人没练过（尤其是仰卧踢腿），作者自己也承认会影响结果",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('讨论和结果说反了')}：讨论说“半腱肌在三个北欧挺和仰卧踢腿时分别达到约 70% 和 80%，与冲刺无显著差异”，但结果部分写的是冲刺时半腱肌{red('显著高于所有动作')}；真正和冲刺没有差异的是{b('半膜肌')}的仰卧踢腿（约 77%），半腱肌的仰卧踢腿只有约 56%",
    f"{b('身高单位错误')}：受试者身高写成“1.80 ± 7.1 m”，标准差 7.1 米显然不可能，应为 cm",
    f"{b('速度单位')}：最高速度写成“22.5 km/t”，应为 km/h（t 是挪威语“小时”的缩写）",
    f"{b('效应量和 F 值对不上')}：肌电部分的效应量能按 12 人复算对上（如半膜肌 F = 14.1 → η² ≈ 0.56）；但角度分析里，髋角 F = 9.1 按 12 人算 η² 约 0.45，原文写 0.65；肌肉间比较 F = 0.79 应约 0.07，原文写 0.14（按他们自己的标准 0.14 已是“大效应”，却又说没有差异）",
    f"{b('图文不一致')}：正文说半腱肌和股二头肌的两个鹤式都显著低于三个北欧挺，但图 2 的半腱肌只标了“鹤式”，没标“鹤式 + 回起”",
    f"{b('证据等级')}：摘要标“1b”级证据，但这是实验室横断面肌电研究，不是随机对照试验",
    f"{b('小错')}：肌电均方根换算电路的频率响应写成“20～500 kHz”，应为 Hz；图 1 图注“lay on back with on shoulders”语句残缺",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('北欧挺仍是首选')}：在测试的动作里激活高、角度又和冲刺相近；回起、推拉变式效果差不多，可以轮换增加趣味",
    f"{b('仰卧踢腿值得一试')}：激活不输北欧挺，又是单腿、爆发式；做的时候支撑脚可以放远一点，让膝更接近伸直",
    f"{b('鹤式和空手站立踢腿激活偏低')}：作为热身或技术练习可以，单靠它们给腘绳肌力量刺激不够",
    f"{b('股二头肌是短板')}：所有动作对股二头肌的激活都不到冲刺的 40%，而它恰恰是最常拉伤的部位。北欧挺之外，最好再配合以髋为主的动作和规律的高速跑",
    "没有任何一个练习能替代冲刺本身：重返运动前，逐步增加的高速跑暴露必不可少",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("表 1　冲刺和 7 个动作中三块肌肉肌电峰值出现时的髋、膝角度（°，均值 ± 标准差）"))
A.append(table(["", "冲刺", "仰卧踢腿", "站立踢腿", "北欧挺", "北欧挺+回起", "北欧挺+推拉", "鹤式", "鹤式+回起"], [
    [b("髋角"), "", "", "", "", "", "", "", ""],
    ["半膜肌", "123±25", "134±31", "82±27*", "140±24", "141±26", "140±29", "150±18*", "160±21*"],
    ["半腱肌", "120±25", "132±30", "80±27*", "135±22", "141±26", "138±25", "154±18*", "153±22*"],
    ["股二头肌", "126±28", "134±33", "81±30*", "138±24", "141±27", "141±27", "160±13*", "156±19*"],
    [b("膝角"), "", "", "", "", "", "", "", ""],
    ["半膜肌", "123±27", "107±24*", "133±38", "128±15", "119±7", "111±9", "141±15", "119±15"],
    ["半腱肌", "128±27", "103±29*", "137±30", "128±11", "120±9", "112±9", "133±24", "125±12"],
    ["股二头肌", "127±23", "98±19*", "153±20*", "129±10", "111±12", "111±12", "139±23", "125±12"],
], first_bold=False))
A.append(small("* 原文用箭头标出与冲刺差异有统计学意义（p < 0.05），此处改用星号。角度越大表示关节越伸直。"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>van den Tillaar R, Solheim JAB, Bencke J. Comparison of hamstring muscle activation during high-speed running and various hamstring strengthening exercises. Int J Sports Phys Ther. 2017;12(5):718-727. doi:10.16603/ijspt20170718</em><br>"
    "原文 PDF 未标注开放许可协议。本文为学术交流用的中文解读：图 1 引自原文（原图为负片，编者反相、按动作分组并改为中文标注），图 2 为编者按原图估读重绘，图 3 引自原文（英文动作名改为中文），表 1 为编者翻译。版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「腘绳肌」7 个腘绳肌训练动作，能练到冲刺时的几成？肌电 + 动作捕捉实测"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>腘绳肌冲刺肌电推文</title>
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
