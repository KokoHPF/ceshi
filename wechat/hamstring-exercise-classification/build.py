#!/usr/bin/env python3
"""精英女子田径运动员腘绳肌训练的肌肉与强度分类（Tsaklis 等 2015）推文。

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
    "Tsaklis P, Malliaropoulos N, Mendiguchia J, Korakakis V, Tsapralis K, Pyne D, Malliaras P. Muscle and intensity based hamstring exercise classification in elite female track and field athletes: implications for exercise selection during rehabilitation. Open Access Journal of Sports Medicine. 2015;6:209-217. doi:10.2147/OAJSM.S79189",
    "作者单位：希腊塞萨洛尼基亚历山大理工学院、希腊国家田径中心运动损伤诊所、伦敦玛丽女王大学、卡塔尔 Aspetar 医院、西班牙 Zentrum 康复中心 等",
    f"文章类型：{b('肌电研究')}（20 名运动员，同一批人做全部 10 个练习）",
], square=True))

A.append(h2("先说为什么要研究这个"))
A.append(p(
    f"腘绳肌拉伤是田径运动中{b('最常见的肌肉损伤')}，症状持续时间长、复发率高。拉伤多发生在疾跑的{b('摆动末期')}：腘绳肌要减速屈髋和伸膝，紧接着伸髋，处于高负荷的离心收缩。"
))
A.append(p(
    f"拉伤可以发生在腘绳肌的不同部位，但常用的腘绳肌训练到底{mk('练的是内侧还是外侧、强度有多大')}，了解得并不多。作者测了 10 个常用练习中股二头肌和半腱肌的肌电，想给康复选动作提供依据。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：20 名希腊国家队女子田径运动员（10 名短跑、6 名跳远、4 名三级跳），平均 22.8 岁；排除近 6 个月有腘绳肌损伤者",
    f"{b('肌电')}：表面电极贴在优势腿的{b('股二头肌长头（外侧）')}和{b('半腱肌（内侧）')}",
    f"{b('标准化')}：俯卧屈膝 45° 在等速仪上做最大等长收缩，以最大值的 80% 作为参照，把各练习的肌电换算成 %MVIC",
    f"{b('动作时相')}：电子量角器同步记录膝角度，判断肌电峰值出现在肌肉—肌腱单元{b('拉长、缩短还是长度不变')}时",
    f"{b('练习')}：10 个练习按同一顺序各做 1 组 10 次，间隔 5 分钟；几乎都不负重",
    f"{b('强度分级')}：<50% MVIC 为低强度，50%～80% 为中强度，≥80% 为高强度",
]))

A.append(h2("重点：10 个练习，强度从低到高"))
A.append(h3("低强度：闭链、以髋为主，半腱肌更活跃"))
A.append(pic(2, "原文图 1：弓步"))
A.append(pic(3, "原文图 2：单腿罗马尼亚硬拉"))
A.append(pic(4, "原文图 3：壶铃摆动"))
A.append(pic(5, "原文图 4：单腿臀桥（接近中强度）"))
A.append(h3("中强度"))
A.append(pic(6, "原文图 5：TRX 屈膝"))
A.append(pic(7, "原文图 6：足跟搭椅臀桥"))
A.append(pic(8, "原文图 7：弹力带站姿屈膝"))
A.append(pic(9, "原文图 8：北欧挺（下降越低强度越高）"))
A.append(h3("高强度：开链为主，不负重也能练到很高"))
A.append(pic(10, "原文图 9：瑞士球快速屈膝"))
A.append(pic(11, "原文图 10：单腿滑行屈伸"))

A.append(h2("结果"))
A.append(pic(12, "两块肌肉的肌电（编者根据原文图 11 重画）"))
A.append(table(["练习", "强度", "偏向", "峰值时相", "开链 / 闭链"], [
    ["弓步", "低", "半腱肌", "拉长", "闭链"],
    ["单腿罗马尼亚硬拉", "低", "半腱肌", "拉长＋缩短", "闭链"],
    ["壶铃摆动", "低", "半腱肌", "拉长", "闭链"],
    ["单腿臀桥", "低（接近中）", "无", "缩短", "闭链"],
    ["TRX 屈膝", "中", "无", "长度不变", "开链"],
    ["足跟搭椅臀桥", "中", "无", "缩短", "闭链"],
    ["弹力带站姿屈膝", "中", "无", "缩短", "开链"],
    ["北欧挺", "中～高", "无", "拉长＋缩短", "开链"],
    ["瑞士球快速屈膝", "高", f"{b('股二头肌')}", "缩短", "开链"],
    ["单腿滑行屈伸", "高（最高）", "无", "拉长＋缩短", "原文前后不一"],
]))
A.append(tcap("原文表 1 和结果（中文整理）：强度、偏向哪块肌肉、肌电峰值出现的时相、开链还是闭链"))
A.append(ul([
    f"{b('低强度')}：弓步、单腿硬拉、壶铃摆动都是闭链、以髋为主，{b('半腱肌比股二头肌更活跃')}；单腿臀桥接近中强度，没有偏向",
    f"{b('高强度')}：瑞士球屈膝和单腿滑行；{mk('瑞士球快速屈膝是唯一偏向股二头肌的练习')}",
    f"{b('拉长相出峰值')}：只有弓步和壶铃摆动的肌电峰值只出现在拉长相，两者都要求{b('速度快')}",
    f"{b('不负重也能高强度')}：北欧挺和单腿滑行不加外部负荷就能让整个腘绳肌高度激活",
    f"{b('开链更高')}：肌电最高的两个是开链，最低的三个是闭链",
]))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('没有报告统计结果')}：方法说用 t 检验比较两块肌肉，但全文没有给出任何 P 值、标准差或置信区间，“半腱肌更高”“股二头肌更高”都无法判断是否有统计学意义",
    f"{b('标准化方法有问题')}：最大等长收缩时把两个通道的肌电{b('平均')}后作为参照，再用同一个参照去换算两块肌肉——这样比较内外侧会受电极位置、皮下脂肪等影响；参照取最大值的 80% 也会让数值整体偏高（所以会出现 >100%）",
    f"{b('只测了两块肌肉、一个位置')}：没测半膜肌和股二头肌短头，表面电极也只代表电极下方的局部",
    f"{b('几乎不负重')}：临床上常给练习加负荷，结果未必能推到加负荷的情况；作者对比 Ebben 的研究，加负荷后屈膝和硬拉的肌电明显更高",
    f"{b('顺序固定')}：10 个练习按同一顺序做，后面的练习可能受疲劳影响",
    f"{b('只看了“拉长 / 缩短”')}：没有区分离心和向心收缩",
    f"{b('只有女性')}：不能直接推到男性运动员",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('北欧挺算中强度还是高强度')}：摘要把北欧挺列为高强度；结果部分列为中强度（下降幅度大时才是高强度）；讨论又把它和单腿滑行并列为高强度。按图 11，北欧挺约 57%～65%，是中强度",
    f"{b('TRX 屈膝')}：按图 11，股二头肌约 84%，已经超过作者自己定的 80% 高强度线，原文却归为中强度；股二头肌也明显高于半腱肌，原文却说只有瑞士球屈膝偏向股二头肌",
    f"{b('单腿滑行是开链还是闭链')}：方法写“闭链、以屈膝为主”，结果和表 1 写开链，讨论“肌电最高的两个是开链”的结论正是基于后者",
    f"{b('图 11 单位')}：纵轴标“平均肌电（μV）”，图注写“%MVIC”",
    f"{b('与其他研究对比的数值')}：讨论说本研究硬拉约 22% MVIC，但图 11 中硬拉两块肌肉约 25%～30%",
    f"{b('足跟搭椅臀桥')}：方法写在顶端保持 5 秒（等长），表 1 却把峰值归为“缩短”",
    f"{b('小错')}：“closed kinematic chain”“closed change exercises”（应为 kinetic chain）；表 1 两行都只写“Bridge”，分不清单腿臀桥和搭椅臀桥",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('按强度排进阶')}：急性拉伤后早期先用低强度的闭链动作（弓步、单腿硬拉、单腿臀桥），再到中强度（搭椅臀桥、弹力带屈膝、北欧挺），最后是高强度（单腿滑行、瑞士球快速屈膝）",
    f"{b('想多练内侧')}：以髋为主的弓步、单腿硬拉、壶铃摆动半腱肌更活跃",
    f"{b('想多练外侧')}：瑞士球快速屈膝是唯一偏向股二头肌的动作——而股二头肌长头恰恰是短跑拉伤最常见的部位",
    f"{b('没器械也能练到位')}：北欧挺、单腿滑行不加负重就能高度激活",
    f"{b('速度要看阶段')}：峰值出现在拉长相的动作都需要快速，早期要结合症状和愈合阶段控制速度",
    "肌电高低只是参考，原文没有给出统计检验，具体选择还要结合损伤部位、疼痛和功能",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Tsaklis P, Malliaropoulos N, Mendiguchia J, Korakakis V, Tsapralis K, Pyne D, Malliaras P. Muscle and intensity based hamstring exercise classification in elite female track and field athletes: implications for exercise selection during rehabilitation. Open Access J Sports Med. 2015;6:209-217. doi:10.2147/OAJSM.S79189</em><br>"
    "原文以 CC BY-NC 3.0 协议开放获取，版权归原作者所有。本文为非商业的学术交流中文解读：原文图 1～10 引自原文，图中中文标签为编者所加；肌电图根据原文图 11 重画（数值为编者读图近似值），表格为中文整理。仅供学习交流，如有侵权请联系删除。"
))

TITLE = "「腘绳肌」10 个常用腘绳肌练习，哪个练内侧、哪个练外侧、强度多大？（附动作图解）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>腘绳肌练习分类推文</title>
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
