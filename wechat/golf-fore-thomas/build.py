#!/usr/bin/env python3
"""Thomas & Wilk 2023 高尔夫球员 Fore 三级训练方案推文：生成 article_body.html 与 preview.html。

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


def pic(n, t, w=None):
    h = img(n)
    if w:
        h = h.replace("width:100%;max-width:100%;", f"width:{w};max-width:{w};")
    return h + cap(t)


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
    "Thomas ZM, Wilk KE. The Golfer’s Fore, Fore +, and Advanced Fore + Exercise Program: An Exercise Series and Injury Prevention Program for the Golfer. Int J Sports Phys Ther. 2023;18(3):789-799.",
    "作者来自美国冠军运动医学中心（Champion Sports Medicine）、美国运动医学研究所（ASMI）",
    "临床评论（证据等级 5 级）；DOI：10.26603/001c.74973",
], square=True))

A.append(h2("先说为什么高尔夫也要做预防训练"))
A.append(p(
    f"很多人觉得高尔夫是“散步 + 挥杆”，不会受伤。但数据不是这样：业余球员{b('每年受伤率 15.8%～40.9%')}，职业球员一年内 31%、整个职业生涯 66%。"
    f"而且{mk('82.6% 是过度使用伤')}，只有 17.4% 是一次性外伤。"
))
A.append(ul([
    f"{b('职业球员')}：下腰（44%）和腕（44%）最多，其次是肘（23%）、颈（20%）、肩（19%）；男性下腰受伤是女性的 2.5 倍",
    f"{b('业余球员')}：肘（24.9%）、肩（18.6%）、腰椎（15.2%）",
    "受伤的原因也不同：职业球员主要是练得太多，业余球员更多是挥杆动作不好",
    f"有研究发现，{b('职业球员腰痛和前导侧髋内旋减少、腰椎伸展减少有关')}",
]))
A.append(p(
    f"现代挥杆讲究“{b('X 因子')}”——上半身和骨盆的分离角度越大，杆头速度越快。但结束时常出现过度后仰的“{b('反 C 字')}”收杆姿势，"
    f"会增加{red('腰椎小关节的负担')}。另外，水平面上的髋关节活动度，能解释{b('48% 的球速差异和 45% 的距离差异')}。"
))
A.append(p(
    f"所以这篇的思路是：做一套{mk('不需要监督、在家或球场就能练')}的方案，分{b('三个难度等级')}，用的器材只有{b('自重 + 一根弹力带')}，"
    "目的是预防受伤、提高力量和活动度、顺便提升表现。"
))

A.append(h2("重点：三级训练方案"))
A.append(ul([
    f"剂量：{mk('每个动作 2 组 × 10 次，组间几乎不休息')}",
    "每周练几次，按训练强度和赛季来定；可以当打球前的热身，也可以作为日常训练的基础",
    f"三级递进：{b('Fore（基础）→ Fore+（中级）→ 进阶 Fore+（高级）')}，每级都分{b('活动度、力量/肌肉激活、核心')}三块",
]))
A.append(pic(12, "三级方案一览（编者根据原文附录 1～3 整理）"))

A.append(h3("Fore 基础版：4 个活动度 + 10 个力量 + 3 个核心"))
A.append(p(f"{b('活动度部分')}："))
A.append(ul([
    f"{b('靠墙水平内收牵伸')}：背靠墙站着固定肩胛，手臂横过胸前往对侧拉。拉的是{b('肩后方')}，挥杆时前导手和后手都需要",
    f"{b('球杆“绕世界”')}：双手握球杆，顺时针、逆时针绕圈，把盂肱关节各个方向都活动开",
    f"{b('半跪位胸椎旋转')}和{b('深蹲 + 旋转')}：开始加入下肢和胸椎的活动度",
]))
A.append(pic(2, "原文图 1　半跪位胸椎旋转"))
A.append(p(f"{b('力量部分')}："))
A.append(ul([
    f"{b('分腿弓步低位划船 + 伸手')}：分腿站，{b('对侧手在前')}（比如左腿在前、右手握弹力带），右手划船、左手往前伸，直到右臂贴体侧。"
    f"伸手那侧顺带练胸椎旋转，强调{mk('骨盆稳住、上半身转')}；第二组换腿。持续保持弓步，是为了练单腿稳定——挥杆时重心要从后腿转到前腿",
    f"{b('深蹲位 PNF D1/D2 模式')}：侧对弹力带，从低往高斜向拉过身体。D1 屈曲：内侧手握带、从内侧髋开始；D2 屈曲：外侧手握带、从内侧髋开始。"
    f"{b('回程（伸展）也要慢')}，练离心控制",
]))
A.append(pic(6, "原文图 5　深蹲位 PNF D2 屈曲模式（Fore+ 中的同一动作）"))
A.append(ul([
    f"{b('深蹲位反向靠墙滑动')}：保持半蹲，{b('手、肘、下背')}都贴住墙往上滑，练上肢柔韧、胸椎活动和后肩袖激活",
]))
A.append(pic(3, "原文图 2　深蹲位反向靠墙滑动"))
A.append(ul([
    f"{b('肩胛系列')}：俯卧在床上、一只手垂在床边，做{b('俯卧 T')}（水平外展）和{b('俯卧 W')}（高位划船接外旋）",
    f"{b('改良“举手投降”')}：半蹲，双手各握弹力带一端，{b('屈肘 90° 贴在体侧、拇指朝外、掌心朝上')}，肘不离身体往外旋，"
    f"同时夹紧肩胛，{b('保持 2 秒')}再回。作者团队未发表的肌电研究发现，它的{mk('下斜方肌激活最高、上斜方肌最少')}",
]))
A.append(pic(4, "原文图 3　改良“举手投降”"))
A.append(ul([
    f"{b('臀桥（双腿、单腿）')}：仰卧屈膝约 90°、脚与肩同宽，脚跟发力，收紧核心和臀部抬起，{b('保持 2 秒')}。单腿版更多练髋外侧，稳定骨盆",
    f"{b('前弓步 + 旋转')}：双手平举球杆，往前弓步，{b('向前腿一侧转体')}（手臂伸直），再从前腿蹬回",
]))
A.append(p(f"{b('核心部分')}："))
A.append(ul([
    f"{b('深蹲位抗旋推（Pallof 推）')}：半蹲，侧对弹力带，双手握带贴在胸下，往正前方推直，{red('不让躯干被带转')}，练水平面稳定",
    f"{b('鸟狗式')}：四点跪，肩在腕正上方、髋在膝正上方，核心收紧、脊柱中立；一侧手往前伸、对侧腿往后蹬，{b('保持 2 秒')}，换边",
    f"{b('死虫式')}：仰卧，交替伸对侧手脚，保持核心稳定",
]))
A.append(pic(7, "原文图 6　深蹲位抗旋推"))

A.append(h3("Fore+ 中级版：7 个活动度 + 17 个力量 + 3 个核心"))
A.append(p(f"在基础版上{b('加量')}：活动度加了{b('墙角胸小肌牵伸、球杆辅助肩前屈、跪姿屈髋肌牵伸')}；力量加了"
           f"{b('深蹲位 0°/90° 外旋和内旋、俯卧 I 和 Y、弹力带侧向走')}。"))
A.append(pic(5, "原文图 4　球杆辅助肩前屈"))

A.append(h3("进阶 Fore+ 高级版：8 个活动度 + 19 个力量 + 3 个核心"))
A.append(p(
    f"在中级版上{b('加难度')}：很多动作从深蹲位改成{mk('分腿弓步位')}（外旋内旋、PNF、抗旋推），屈髋肌牵伸改成{b('后脚垫高')}，"
    f"胸椎旋转和靠墙滑动{b('加弹力带')}，肩胛系列放到{b('瑞士球')}上；新增了抗阻四点跪伸手旋转、单腿罗马尼亚硬拉接提膝、高位划船接外旋，"
    f"核心动作也升级成{b('抗旋推 + 上举、鸟狗式 + 划船、弹力带死虫式')}。"
))
A.append(pic(8, "原文图 7　单侧划船伸手 + 侧向下台阶"))
A.append(pic(9, "原文图 8　瑞士球上高位划船接外旋（“W”）"))
A.append(pic(10, "原文图 9　抗阻前弓步 + 旋转"))
A.append(pic(11, "原文图 10　鸟狗式 + 划船"))

A.append(h2("这篇的局限"))
A.append(ul([
    f"{red('证据等级 5 级')}：这是作者的经验方案，{b('没有任何试验验证')}它能不能减少受伤或提高表现",
    "“改良举手投降下斜方肌激活最高”来自作者团队未发表的预实验，无法核实",
    "进阶标准没写：什么时候从 Fore 升到 Fore+、再到进阶版，原文没给条件",
    "原文写基础版有“4 个核心动作”，附录和后文都只有 3 个；正文还让读者参考“表 2、表 3”，但文中并没有这两张表",
    "原文给每部分配了视频二维码，但编者扫码发现链接已被二维码服务商停用，视频看不到了",
    "版权声明写的是“CC BY 4.0”，括号里却是 CC BY-NC 4.0，两者不一致",
]))

A.append(h2("落到临床"))
A.append(p(
    f"这套方案的价值在于{mk('简单、全身、和挥杆动作贴得近')}：分腿弓步、旋转、单腿稳定、水平面抗旋，基本都在模拟挥杆时“下肢稳住、上身转”的需求。"
    f"器材只要一根弹力带，球员可以在家、在练习场边做。"
))
A.append(p(
    f"临床上可以这样用：{b('先评估')}髋内旋、胸椎旋转、肩后方紧张度、单腿稳定这些和挥杆相关的指标，"
    f"{b('哪里差就多练哪部分')}；{b('能轻松完成 2 组 × 10 次、动作质量好')}，再往上一级走。"
    f"有腰痛史的球员，额外注意{red('收杆时别“反 C”后仰')}，髋和胸椎的旋转要先练够。"
))

A.append(h2("附录：原文附录 1～3 动作清单"))
A.append(tcap("原文附录 1　Fore 基础版"))
A.append(table(["部分", "动作"], [
    ["活动度（上下肢与脊柱）", "靠墙水平内收牵伸；球杆“绕世界”（顺/逆时针）；半跪位胸椎旋转；深蹲 + 旋转"],
    ["力量/肌肉激活", "分腿弓步低位划船 + 伸手；深蹲位 PNF D1、D2 屈曲/伸展；深蹲位反向靠墙滑动；肩胛系列（俯卧 T、俯卧 W、改良“举手投降”）；臀桥（双腿、单腿）；前弓步 + 旋转"],
    ["核心激活", "深蹲位抗旋推；鸟狗式；死虫式"],
]))
A.append(tcap("原文附录 2　Fore+ 中级版"))
A.append(table(["部分", "动作"], [
    ["活动度（上下肢与脊柱）", "墙角胸小肌牵伸；靠墙水平内收牵伸；球杆辅助肩前屈；球杆“绕世界”；跪姿屈髋肌牵伸；半跪位胸椎旋转；深蹲 + 旋转"],
    ["力量/肌肉激活", "分腿弓步低位划船 + 伸手；深蹲位 0°、90° 外旋；深蹲位 0°、90° 内旋；深蹲位 PNF D1、D2；深蹲位反向靠墙滑动；肩胛系列（俯卧 I、T、Y、W，改良“举手投降”）；臀桥（双腿、单腿）；弹力带侧向走；前弓步 + 旋转"],
    ["核心激活", "深蹲位抗旋推；鸟狗式；死虫式"],
]))
A.append(tcap("原文附录 3　进阶 Fore+ 高级版"))
A.append(table(["部分", "动作"], [
    ["活动度（上下肢与脊柱）", "墙角胸小肌牵伸；靠墙水平内收牵伸；球杆辅助肩前屈；球杆“绕世界”；后脚垫高的跪姿屈髋肌牵伸；弹力带抗阻半跪胸椎旋转；深蹲 + 旋转；抗阻四点跪伸手 + 旋转"],
    ["力量/肌肉激活", "单侧划船伸手 + 侧向下台阶；分腿弓步位 0°、90° 外旋；分腿弓步位 0°、90° 内旋；分腿弓步位 PNF D1、D2；弹力带反向靠墙滑动；瑞士球上肩胛系列（俯卧 I、T、Y、W）；高位划船接外旋；改良“举手投降”；弹力带抗阻臀桥（双腿、单腿）；弹力带侧向走；单腿罗马尼亚硬拉接提膝；抗阻前弓步 + 旋转"],
    ["核心激活", "分腿弓步位抗旋推 + 上举；鸟狗式 + 划船；弹力带死虫式"],
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Thomas ZM, Wilk KE. The Golfer’s Fore, Fore +, and Advanced Fore + Exercise Program: An Exercise Series and Injury Prevention Program for the Golfer. Int J Sports Phys Ther. 2023;18(3):789-799. doi:10.26603/001c.74973</em><br>"
    "原文以 CC BY-NC 4.0 协议开放获取（仅限非商业使用）。动作照片来自原文（背景球衣姓名、器械品牌已模糊），方案一览图和附录清单为编者翻译整理，仅用于学术交流。"
))

TITLE = "「高尔夫」打高尔夫也会受伤！一根弹力带的三级预防训练方案"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>高尔夫三级训练推文</title>
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
