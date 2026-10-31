#!/usr/bin/env python3
"""《肩袖撕裂类型：MRI 表现及其手术意义》（Yubran 等 2024 Insights into Imaging）推文。

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
def I(n, c): A.append(img(n)); A.append(cap(c))
I(1, "原文信息（编者中文重排）")
A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Yubran AP, Cerezal Pesquera L, Llopis San Juan E, Idoate Saralegui F, Cerezal Canga A, Cruz Camara A, Matheus Valdivieso G, Pisanti Lopez C. Rotator cuff tear patterns: MRI appearance and its surgical relevance. Insights Imaging. 2024;15:61. doi:10.1186/s13244-024-01607-w",
    "作者单位：西班牙巴塞罗那 IBERORAD 放射科、坎塔布里亚、瓦伦西亚、潘普洛纳多家医院放射科；马德里拉帕斯大学医院骨科；委内瑞拉加拉加斯肩关节外科 等",
    f"文章类型：{b('欧洲放射学会教学综述')}（MRI 与关节镜对照）；CC BY 4.0 开放获取",
], square=True))
A.append(h2("先说结论"))
I(2, "原文要点（编者整理）")
A.append(ul([
    f"肩袖撕裂{b('没有公认的统一分型')}；作者推荐按 ISAKOS 共识描述：位置、范围、形态、回缩、脂肪萎缩",
    f"{b('分层撕裂、肌腱连接处撕裂、Fosbury flop')} 等新类型不在 ISAKOS 里，报告中要另外写明",
    f"全层撕裂在 MRI 上{b('最难判断的是形态')}（新月形、U 形、L 形），而形态决定怎么修",
    f"{red('脂肪浸润不可逆')}，是手术结构和功能结局的关键预后因素",
]))

A.append(h2("一、先搞懂解剖"))
I(3, "冈上肌、冈下肌（据原文整理）")
I(4, "原文图 1（编者中文标注）  冈上肌前、后两腹")
I(5, "原文图 2（编者中文标注）  冈上肌、冈下肌的止点")
A.append(p(f"两个容易被忽略的点：一是冈上肌{b('前腹')}收缩力大、腱却不比后腹粗，应力集中，所以肌腱连接处和肌腱损伤多发生在前腹；二是{b('冈下肌止点从上方覆盖冈上肌后缘')}，因此冈下肌受累可能比想象中常见。"))
I(6, "五层结构、肩袖索与肩胛下肌（据原文整理）")
I(7, "原文图 3（编者中文标注）  冈上肌、冈下肌的分层结构")
I(8, "原文图 4（编者中文标注）  正常肩袖索与新月区")
I(9, "原文图 5（编者中文标注）  正常肩胛下肌")
A.append(p(f"第 2 层（滑囊侧）弹性好、血供好；第 3 层（关节侧）无弹性、血供差、易撕裂——{mk('这两层的差异是部分撕裂和分层撕裂的解剖基础')}。肩袖索像“吊桥”分担新月区负荷，也能限制撕裂后的回缩。"))

A.append(h2("二、ISAKOS 分型"))
I(10, "ISAKOS 肩袖撕裂分型（据原文表 1 整理）")

A.append(h2("三、后上方部分撕裂"))
I(11, "关节侧、滑囊侧、腱内撕裂（据原文整理）")
I(12, "原文图 6（编者中文标注）  冈上肌关节侧部分撕裂")
I(13, "原文图 7（编者中文标注）  关节侧部分撕裂，ABER 体位关节造影")
I(14, "原文图 8（编者中文标注）  冈上肌滑囊侧部分撕裂")
I(15, "原文图 9（编者中文标注）  冈上肌腱内撕裂")
A.append(p(f"判断要点：撕裂深度以 {b('50% 腱厚')}为界分高、低级别——高级别 {b('55%')} 会进展为全层，低级别只有 14%。ABER（外展外旋）体位让冈上肌纤维放松，对比剂更容易进入撕裂处，能看清腱内水平延伸。"))
I(16, "部分撕裂的治疗（据原文整理）")

A.append(h2("四、后上方全层撕裂"))
I(17, "全层撕裂：形态、范围、回缩（据原文整理）")
I(18, "原文图 10（编者中文标注）  冈上肌全层撕裂")
I(19, "原文图 11（编者中文标注）  全层撕裂的三种形态")
A.append(p(f"形态在 MRI 上最难判断。一个实用技巧：{b('比较斜冠状位和斜矢状位上的裂口宽度')}——L 形在冠状位更宽、矢状位更短；新月形和 U 形则矢状位更宽。"))
I(20, "原文图 12（编者中文标注）  全层撕裂范围（Snyder 分级）")
I(21, "原文图 13（编者中文标注）  回缩分级（Patte）")

A.append(h2("五、特殊类型"))
A.append(h3("1. 分层撕裂"))
I(22, "分层撕裂（据原文整理）")
I(23, "原文图 14（编者中文标注）  分层撕裂的分型示意")
I(24, "原文图 15（编者中文标注）  冈上肌分层撕裂 MRI")
I(25, "原文图 16（编者中文标注）  关节层翻入关节腔")
A.append(h3("2. Fosbury flop、肌内囊肿、肌腱连接处撕裂"))
I(26, "其他特殊类型（据原文整理）")
I(27, "原文图 17（编者中文标注）  Fosbury flop 撕裂")
I(28, "原文图 18（编者中文标注）  冈上肌肌腱连接处撕裂")
I(29, "全层撕裂的治疗（据原文整理）")

A.append(h2("六、前方撕裂：肩胛下肌"))
I(30, "肩胛下肌撕裂（据原文整理）")
I(31, "原文图 19（编者中文标注）  Lafosse 1～3 型")
I(32, "原文图 20（编者中文标注）  Lafosse 4、5 型")
I(33, "原文图 21（编者中文标注）  外伤性肩胛下肌撕裂")
I(34, "原文图 22（编者中文标注）  桥接征")
A.append(p(f"肩胛下肌撕裂在 MRI 和关节镜下都容易漏，发生率 20%～37%。退变性撕裂{b('从上 1/3 开始往下发展')}；单纯撕裂多为外伤（外展位过伸或外旋）。“桥接征”提示肩胛下肌上部、冈上肌前部、喙肱韧带和盂肱上韧带联合撕裂，往往意味着更严重的肩袖撕裂和更多慢性疼痛。"))

A.append(h2("七、脂肪浸润"))
I(35, "脂肪浸润（据原文整理）")
I(36, "原文图 23（编者中文标注）  Goutallier 脂肪浸润分级")

A.append(h2("八、巨大撕裂与肩袖关节病"))
I(37, "巨大撕裂、肩袖关节病与挽救手术（据原文整理）")
I(38, "原文图 24（编者中文标注）  Hamada 肩袖关节病分期")

A.append(h2("原文对不上的地方"))
A.append(ul([
    f"Snyder 范围分级写 C2“<2 cm”、C3“回缩 3～4 cm”，{b('2～3 cm 的撕裂没有归属')}；而且 C3 前文说的是撕裂大小，这里写成了“回缩”",
    f"肩胛下肌 Lafosse 分型：4 型脂肪萎缩“{b('≤ Goutallier 3 级')}”，5 型“{b('≥ 3 级')}”，3 级两型都算",
    f"原文图 4 的图注里有{b('两个 “b”')}（轴位 MRI 和关节镜），后一个应为 c",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Yubran AP, Cerezal Pesquera L, Llopis San Juan E, et al. Rotator cuff tear patterns: MRI appearance and its surgical relevance. Insights Imaging. 2024;15:61. doi:10.1186/s13244-024-01607-w</em><br>"
    "原文为 CC BY 4.0 开放获取（© The Author(s) 2024），插画作者 Massimiliano Crespi。本文为中文解读：原文图 1～24 引自原文，编者将图内英文词替换为中文并在图下加中文图例条；其余整理卡由编者根据原文撰写。"
))
TITLE = "「肩关节」肩袖撕裂有哪些类型？24 张 MRI + 关节镜对照图一次看懂"
PTITLE = "肩袖撕裂类型 MRI 推文"
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
