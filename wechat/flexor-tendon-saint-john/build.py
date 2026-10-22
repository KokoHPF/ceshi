#!/usr/bin/env python3
"""屈肌腱修复术后 Saint John 方案（Higgins & Lalonde 2016）推文，含补充视频动图。

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


def gif(name, t, w="72%"):
    return ('<p style="margin:0 0 8px;text-align:center;">'
            f'<img src="gifs/{name}" alt="{t}" style="width:{w};max-width:{w};height:auto;display:block;margin:0 auto;"></p>'
            + cap(t))


A = []
A.append(img(1))
A.append(cap("原文信息（编者中文重排）"))

A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Higgins A, Lalonde DH. Flexor Tendon Repair Postoperative Rehabilitation: The Saint John Protocol. Plast Reconstr Surg Glob Open. 2016;4(11):e1134. doi:10.1097/GOX.0000000000001134",
    "作者：Amanda Higgins（加拿大圣约翰地区医院作业治疗师）、Donald Lalonde（手外科医生，清醒局麻无止血带手术 WALANT 的主要倡导者）",
    f"文章类型：{b('视频手术技术')}，正文只有两页，核心内容在 4 段补充视频里；{mk('本文的动图都截自这 4 段原文视频')}",
], square=True))

A.append(h2("先说为什么要改掉“全拳放置—保持”"))
A.append(p(
    f"屈肌腱 2 区修复后，传统做法是让患者被动把手指放到全拳位置再主动保持（place and hold）。作者团队做的是{b('清醒局麻无止血带（WALANT）')}屈肌腱修复："
    f"患者术中是清醒的，可以当场主动屈伸手指，医生能直接看到修复口有没有缝隙、及时补缝，作者称这让他们的断裂率下降了 7%。"
))
A.append(p(
    f"术中反复观察后，他们有信心放弃全拳放置—保持，改为{mk('最多半拳的“真正主动屈曲”')}（Tang 的主张）。前提是：{b('4～6 股缝合、术中测试没有缝隙')}。"
    f"作者认为即使患者是全麻或镇静下手术、享受不到术中测试，也应如此。"
))
A.append(pic(2, "视频 1 要点：为什么只做到半拳（编者根据视频幻灯片翻译整理）"))
A.append(small("视频 1 是英文幻灯片讲座，包含大量术中照片，没有做成动图，要点已译成上面的卡片。"))

A.append(h2("怎么做的"))
A.append(p(
    f"这不是对照研究，而是作者医院的一套{b('术后康复流程')}，分 4 个阶段，用视频演示。下面这张卡片是全流程，后面按阶段配上视频动图。"
))
A.append(pic(3, "Saint John 方案各阶段要点（编者根据原文整理）"))

A.append(h2("重点一：术后头 2 周"))
A.append(h3("先等 3～5 天：完全不动、一直抬高"))
A.append(ul([
    f"术中就教会患者：{b('手指一点都不要动，手始终抬高')}，避免伤口内出血——{red('出血会形成血块，血块会变成瘢痕')}",
    f"为什么等 3～5 天：肿胀、屈曲做功和摩擦都会下降，断裂风险更低；而且{b('胶原第 3 天才开始形成')}，术后立刻活动没有必要，反而有害",
    f"术后立即戴{b('背侧阻挡支具')}：腕最多背伸 45°，手放在舒适位，掌指关节屈 30°，指间关节完全伸直",
]))
A.append(h3("4 天～2 周：清醒时每小时练 10 次"))
A.append(p(f"核心口诀：{mk('“可以动，但不能用！”')}——术中和每次复诊至少向患者强调 3 次。"))
A.append(gif("g1_warmup.gif", "动图 1：在支具内被动屈曲所有手指，作为主动活动前的“热身”（截自原文视频 2）"))
A.append(gif("g2_ip_ext.gif", "动图 2：被动屈曲掌指关节，在此位置下主动伸直指间关节，预防指间关节屈曲挛缩（截自原文视频 2）"))
A.append(gif("g3_halffist.gif", "动图 3：真正主动屈曲，最多到半拳（截自原文视频 2）"))
A.append(gif("g4_halffist2.gif", "动图 4：同一动作的侧面观，可以看到支具内的屈曲幅度（截自原文视频 2）"))
A.append(ul([
    f"{b('水肿控制')}：抬高 + 用自粘绷带（Coban 或 Co-Flex）轻轻包裹手指加压",
    f"{b('被动热身')}：在包含腕关节的背侧阻挡支具内，先被动屈曲所有手指",
    f"{b('防挛缩')}：掌指关节屈曲位下主动伸直指间关节",
    f"{b('真正主动屈曲')}：到{mk('三分之一至半拳')}，{b('从远侧指间关节开始启动')}（主动“勾拳”）",
    f"{red('不用力、不痛、不勉强')}；作者鼓励患者先停用所有止痛药，按疼痛引导训练，再开始真正主动活动",
    "视频结尾：前 2 周的目标就是半拳",
]))

A.append(h2("重点二：2～4 周，换短支具、加腕手协同"))
A.append(gif("g5_glide.gif", "动图 5：换成 Manchester 短支具，手腕可以活动；关键是保持肌腱主动屈曲、滑动足够，就不会粘住（截自原文视频 3）"))
A.append(gif("g6_dip.gif", "动图 6：真正主动活动从远侧指间关节开始启动肌腱滑动（截自原文视频 3）"))
A.append(gif("g7_synergy.gif", "动图 7：腕和手指的主动协同运动——伸腕时屈指、屈腕时伸指（截自原文视频 3）"))
A.append(ul([
    f"大约术后 2 周，背侧阻挡支具{b('改为 Manchester 短支具')}，允许腕关节活动",
    f"在短支具内做{mk('腕和手指的主动协同运动')}",
    "逐步从半拳做到全拳，腕背伸最多 45°",
    "继续在掌指关节完全屈曲位下完全伸直指间关节",
    f"目标：{b('6 周前做到全拳')}",
]))

A.append(h2("重点三：6 周，去支具、开始轻活动"))
A.append(gif("g8_fist.gif", "动图 8：逐步握到完整的拳（截自原文视频 4，视频中此阶段提示先争取 3/4 拳）"))
A.append(gif("g9_fist_open.gif", "动图 9：去掉支具后反复握拳、张开（截自原文视频 4）"))
A.append(gif("g10_passive_ext.gif", "动图 10：6 周后可以开始被动伸直手指，必要时夜间戴伸直支具纠正屈曲畸形（截自原文视频 4）"))
A.append(ul([
    f"{b('停用 Manchester 短支具')}，可以开始用手做轻活动",
    f"如有指间关节屈曲挛缩：{b('夜间戴手掌或手指伸直支具')}；白天活动时用{b('相对运动屈曲矫形器')}也有帮助",
    "视频 4 还演示了 6 周时开始被动伸直手指",
]))

A.append(h2("这些内容能信几分"))
A.append(ul([
    f"{b('这是技术介绍，没有疗效数据')}：没有报告病例数、断裂率、活动度或功能结局，属于经验分享",
    f"{b('有前提条件')}：作者明确说要 4～6 股缝合、术中测试无缝隙；缝合强度不够或没做术中测试时，能否照搬要谨慎",
    f"{b('理念有依据')}：半拳真正主动活动来自 Tang 等的研究，以及 WALANT 术中直接观察到的肌腱滑动和缝隙；“断裂率下降 7%”引自作者团队 2010 年的研究",
    f"{b('视频演示很直观')}：动作要点、幅度、支具都能看清，适合用来教患者",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“5 个理由”只列了 4 个')}：正文和视频 1 的说明都说讲了“5 个理由”，但视频里的幻灯片只列了 4 条",
    f"{b('开始活动的时间说法不一')}：正文说先制动 3～5 天，“4 天至 2 周”开始练；视频 2 的字幕则写“术后 3～4 天开始被动热身”",
    f"{b('阶段时间对不上')}：正文第三阶段标题是“6 周”，视频 4 的说明却是“术后 4～8 周”；而且视频 4 开头提示“争取 3/4 拳”，与正文“6 周前做到全拳”的说法也不完全一致",
    f"{b('腕关节角度自相矛盾')}：术后立刻戴的背侧阻挡支具就允许“腕背伸最多 45°”，2～4 周阶段又把“腕背伸到 45°”作为新目标",
    f"{b('“断裂率下降 7%”含糊')}：没说是从多少降到多少，是绝对值还是相对值",
    f"{b('版权声明矛盾')}：同时写了“All rights reserved（保留所有权利）”和 CC BY-NC-ND 开放许可",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先确认手术条件')}：几股缝合、术中有没有测过缝隙，决定能不能早期做真正主动屈曲",
    f"{b('头 3～5 天：不动 + 抬高')}，减少出血和水肿",
    f"{b('之后清醒时每小时 10 次')}：被动热身 → 掌指屈曲位伸直指间关节 → 从远侧指间关节开始的主动屈曲，最多半拳",
    f"{b('口诀“可以动，但不能用”')}，每次复诊都要重复",
    f"{b('约 2 周改短支具')}，加入腕手协同运动；6 周前逐步到全拳",
    f"{b('6 周去支具')}，开始轻活动；有屈曲挛缩就加夜间伸直支具或相对运动矫形器",
    f"{red('任何时候都不痛、不用力')}；按疼痛引导训练",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Higgins A, Lalonde DH. Flexor Tendon Repair Postoperative Rehabilitation: The Saint John Protocol. Plast Reconstr Surg Glob Open. 2016;4(11):e1134. doi:10.1097/GOX.0000000000001134</em><br>"
    "原文以 CC BY-NC-ND 4.0（署名—非商业性使用—禁止演绎）许可发表。本文为非商业的学术交流解读：动图 1～10 截自原文补充视频 2～4，英文字幕替换为中文；视频 1 要点和各阶段方案为编者翻译整理。如有侵权请联系删除。"
))

TITLE = "「手」屈肌腱修复术后怎么练？Saint John 方案 + 10 个视频动图"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>屈肌腱 Saint John 推文</title>
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
