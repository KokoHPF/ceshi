#!/usr/bin/env python3
"""治疗性与三维足踝运动中足内在肌肌电比较（Park & Hwang 2020）推文。

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
    "Park DJ, Hwang YI. Comparison of the Intrinsic Foot Muscle Activities between Therapeutic and Three-Dimensional Foot-Ankle Exercises in Healthy Adults: An Explanatory Study. Int J Environ Res Public Health. 2020;17(19):7189. doi:10.3390/ijerph17197189",
    "作者单位：韩国釜山天主教大学产业保健系、湖西大学物理治疗系",
    f"研究类型：{b('表面肌电研究')}，16 名健康成人，每人做 6 种足踝运动",
], square=True))

A.append(h2("先说为什么要比较这几个动作"))
A.append(p(
    f"足内在肌是足的“局部稳定肌”：力臂短，为足弓提供动态稳定，也提供感觉输入；它的无力与足底筋膜炎、拇外翻、扁平足、踝扭伤和慢性踝关节不稳有关，"
    f"老年人内在肌无力还会增加跌倒风险——拇展肌这类 Ⅱ 型纤维会随年龄萎缩。"
))
A.append(p(
    f"临床最常用的两个内在肌练习是{b('短足（SF）')}和{b('脚趾张开（TSO）')}：短足能抬高内侧纵弓、改善平衡；脚趾张开能让拇展肌变厚。"
    f"近年又有人提出用 {mk('PNF 下肢对角线模式里的三维踝足动作')}来练内在肌和外在肌，在扁平足、踝扭伤和足底筋膜炎病例中效果不错。"
    f"这篇就把三维动作和两个经典动作放在一起，看哪块肌肉在哪个动作里更活跃。"
))

A.append(h2("怎么做的"))
A.append(pic(2, "原文图 1：研究流程（编者中文重绘）"))
A.append(ul([
    f"{b('对象')}：20～30 岁、没练过足踝运动、近 3 个月没有踝损伤和疼痛的健康成人；19 人筛查，排除 2 人（足部畸形、活动度受限），1 人测试中因肌肉疲劳和痉挛退出，{b('最终 16 人')}（男女各半，平均 27.4 岁）",
    f"{b('训练')}：正式测试前先教 1 小时，通过动作考核才进入测试；6 个动作顺序随机",
    f"{b('肌电')}：优势侧拇展肌、拇收肌、拇长伸肌、拇短屈肌；拇收肌和拇短屈肌用自制足板测，减少足底接触带来的干扰",
    "每个动作做 3 次、每次 5 秒，取中间 3 秒；最后再测最大自主等长收缩（MVIC），把肌电标准化为 %MVIC",
    f"另外计算{b('拇展肌 / 拇收肌比值')}：评价拇外翻时常用，比值越接近或超过 1，说明拇展肌越能“独立”于拇收肌发力",
]))
A.append(pic(3, "原文图 2：自制肌电足板"))

A.append(h2("重点：六个动作怎么做"))
A.append(h3("两个经典动作"))
A.append(pic(4, "原文图 3：短足运动"))
A.append(ul([
    f"{mk('短足（SF）')}：在部分负重下进行，由治疗师先带着被动做，再过渡到主动；目标是{b('减少外在肌的过度参与、增加内在肌活动')}，让足变短、足弓抬起；足下垫毛巾提供感觉反馈",
]))
A.append(pic(5, "原文图 4：脚趾张开运动"))
A.append(ul([
    f"{mk('脚趾张开（TSO）')}：站立，先抬起脚跟和所有脚趾 → 把脚趾全部张开 → 脚跟着地 → 脚趾按{b('小趾、大脚趾、其余脚趾')}的顺序依次落地 → 保持",
]))
A.append(h3("四个三维足踝动作（PNF 对角线）"))
A.append(pic(6, "原文图 5：D1 模式"))
A.append(pic(7, "原文图 6：D2 模式"))
A.append(ul([
    f"{b('D1 屈曲（D1F）')}：从起始位开始，先做背伸—旋后—内翻加伸趾，再做跖屈—旋前—外翻加屈趾；动作从远端（脚趾）开始",
    f"{b('D1 伸展（D1E）')}：与 D1 屈曲方向相反",
    f"{b('D2 屈曲（D2F）')}：先做背伸—旋前—外翻加伸趾，再做跖屈—旋后—内翻加屈趾",
    f"{b('D2 伸展（D2E）')}：与 D2 屈曲方向相反",
    "四个动作都在同一坐姿下完成，做向心收缩",
]))

A.append(h2("结果（压缩版）"))
A.append(pic(8, "原文图 7：拇展肌和拇长伸肌的激活（编者中文重绘）"))
A.append(pic(9, "原文图 8：拇短屈肌激活和拇展肌 / 拇收肌比值（编者中文重绘）"))
A.append(ul([
    f"{b('拇展肌')}：TSO（80.8%）、D2E（79.0%）、D1E（76.5%）最高，三者都显著高于 D2F（51.0%）；SF 为 65.1%，TSO 比 SF 高约 15% 但差异不显著",
    f"{b('拇长伸肌')}：两个三维屈曲动作最高（D2F 73.2%、D1F 68.1%），显著高于其他动作",
    f"{b('拇短屈肌')}：D1E（105.1%）、D2E（97.2%）、SF（96.0%）较高，都显著高于 D2F（72.3%）",
    f"{b('拇展肌 / 拇收肌比值')}：TSO 最高（0.92），D2E（0.85）次之，两者都显著高于 D2F（0.58）",
    f"{b('拇收肌')}：各动作之间没有显著差异（原文如此，见后文），都在 86%～93% MVIC",
]))
A.append(table(["指标", "SF", "TSO", "D1F", "D1E", "D2F", "D2E"], [
    ["拇展肌（%MVIC）*", "65.06 ± 28.01", "80.84 ± 26.33", "61.41 ± 21.33", "76.48 ± 30.40", "51.00 ± 17.20", "78.97 ± 22.00"],
    ["拇收肌（%MVIC）", "92.36 ± 8.16", "88.10 ± 7.66", "86.18 ± 7.40", "93.37 ± 10.49", "88.95 ± 5.84", "92.96 ± 8.17"],
    ["拇长伸肌（%MVIC）*", "49.16 ± 16.44", "52.92 ± 19.37", "68.14 ± 19.37", "53.75 ± 14.22", "73.19 ± 22.83", "49.35 ± 11.56"],
    ["拇短屈肌（%MVIC）*", "95.96 ± 19.54", "90.09 ± 19.40", "84.58 ± 31.35", "105.14 ± 35.15", "72.28 ± 19.35", "97.23 ± 27.97"],
    ["拇展肌 / 拇收肌比值*", "0.70 ± 0.28", "0.92 ± 0.29", "0.71 ± 0.23", "0.81 ± 0.29", "0.58 ± 0.22", "0.85 ± 0.22"],
]))
A.append(tcap("原文表 2：各足部强化运动中四块肌肉的标准化肌电和拇展肌 / 拇收肌比值（n = 16）（中文翻译）"))
A.append(small("均值 ± 标准差。SF：短足；TSO：脚趾张开；D1F / D1E：D1 屈曲 / 伸展模式；D2F / D2E：D2 屈曲 / 伸展模式。* P &lt; 0.05。"))
A.append(table(["变量", "均值 ± 标准差"], [
    ["年龄（岁）", "27.44 ± 2.58"], ["身高（cm）", "166.19 ± 6.80"], ["体重（kg）", "59.75 ± 9.54"], ["体重指数（kg/m²）", "21.57 ± 2.62"],
    ["性别", "男 8 人（50%），女 8 人（50%）"], ["优势足", "右 13 人（81.2%），左 3 人（18.8%）"],
]))
A.append(tcap("原文表 1：研究对象描述性统计（n = 16）（中文翻译）"))
A.append(p(f"作者结论：{mk('三维伸展动作在拇展肌、拇短屈肌激活和拇展肌 / 拇收肌比值上，与经典治疗性动作效果相当；三维屈曲动作则更能激活拇长伸肌')}。"))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('只是健康年轻人的一次性肌电')}：肌电高不等于训练后肌肉变强，更不能直接推到扁平足、拇外翻患者",
    f"{b('样本没达到计算要求')}：样本量计算需要 19 人，最终只有 16 人",
    f"{b('足内在肌用表面肌电很难测准')}：这些肌肉小而深，相互挨得很近，串扰难以避免；拇收肌和拇短屈肌的 %MVIC 接近甚至超过 100%，作者也承认 MVIC 姿势可能诱发不出真正的最大收缩",
    f"{b('MVIC 放在最后测')}：做完 6 个动作再测，若肌肉已疲劳，MVIC 偏低，%MVIC 就会被高估",
    f"{b('拇长伸肌是外在肌')}：题目说比较“足内在肌”，结果里却有一块外在肌",
    "优点：三维动作和经典动作放在同一批人身上比较，方便临床挑选动作",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“短足的拇短屈肌最高”不对')}：讨论说短足的拇短屈肌活动最高，但表 2 中最高的是 D1E（105.14%），D2E（97.23%）也高于短足（95.96%）",
    f"{b('“短足和 D1E 平均都超过 105%”不对')}：短足只有 95.96%",
    f"{b('拇收肌的 P 值可疑')}：F = 3.491（6 个动作、16 人，自由度 5, 75），未校正时 P ≈ {b('0.007')}，原文却写“P &gt; 0.05、无显著差异”；即使做了球形校正，也很难超过 0.05",
    f"{b('讨论说三维伸展动作“拇收肌活动高于其他动作”')}：结果部分刚说拇收肌各动作之间无差异",
    f"{b('拇短屈肌电极位置写错')}：方法说拇长伸肌和拇短屈肌电极都贴在“内外踝连线上方三横指、胫骨嵴外侧”——那是小腿；拇短屈肌在足底。原文图 2 足板上画的拇短屈肌电极确实在足底",
    f"{b('足板测哪块肌肉前后不一')}：正文说足板用于测拇收肌和拇短屈肌，图 2 标注的却是拇展肌和拇短屈肌",
    f"{b('拇展肌电极位置自相矛盾')}：“内踝前缘”和“舟骨结节后方 1～2 cm”说的不是同一个位置",
    f"{b('动作命名混乱')}：正文说 D1F 是先做背伸—旋后—内翻、再做跖屈—旋前—外翻（图 5A），而图 5A 的图注只写了跖屈—旋前—外翻；屈曲模式和伸展模式的起止位描述容易让人看反",
    f"{b('人数描述不清')}：正文说“共选入 19 名受试者”，流程图显示其中 2 人被排除、1 人退出",
    f"{b('文献引用错位')}：局限性部分讲表面肌电串扰时引用的文献 33，是拇外翻手术的研究",
    f"{b('小错')}：“flexor braves”应为 brevis；局限性中“可用于腹部肌肉的方法”与本研究无关，像是从别处照搬",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('想练拇展肌（扁平足、拇外翻）')}：首选脚趾张开（TSO），D2E、D1E 这类三维伸展动作可以作为替代或进阶",
    f"{b('拇外翻要看“独立性”')}：TSO 的拇展肌 / 拇收肌比值最高，更能让拇展肌单独发力；三维动作的拇收肌也很活跃，用于拇外翻要谨慎",
    f"{b('短足仍是基础动作')}：拇短屈肌激活高，适合作为足核心训练的起点",
    f"{b('三维屈曲动作偏练拇长伸肌')}，不适合作为内在肌的主要练习",
    f"{b('教动作要花时间')}：本研究每人先练 1 小时、考核过关才测；临床上也要先教会、再加量",
    "扁平足患者还可以借助三维伸展动作同时激活胫骨后肌（D2E）和腓骨长肌（D1E），这是作者的推测，本研究没有测",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Park DJ, Hwang YI. Comparison of the Intrinsic Foot Muscle Activities between Therapeutic and Three-Dimensional Foot-Ankle Exercises in Healthy Adults: An Explanatory Study. Int J Environ Res Public Health. 2020;17(19):7189. doi:10.3390/ijerph17197189</em><br>"
    "原文以 CC BY 4.0 许可发表。本文为学术交流用的中文解读：原文图 1、7、8 按原意中文重绘，图 2 英文标注改为中文，图 3～6 原样引用并加中文图注，表 1、表 2 为中文翻译。"
))

TITLE = "「足踝」练足内在肌，短足、脚趾张开还是 PNF 三维动作？一项肌电研究"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>足内在肌肌电推文</title>
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
<div class="by">原创 · 悦美力</div>
""" + BODY + "\n</div>\n",
    encoding="utf-8",
)
print("written", len(BODY), "chars", BODY.count("<img"), "imgs")
