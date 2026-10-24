#!/usr/bin/env python3
"""仰卧桥式治疗腰痛 Part II（Colonna 等 2025）推文。

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
    "Colonna S, D'Alessandro A, Tarozzi R, Casacci F. Supine Bridge Exercise for Low Back Pain: A Fascial Approach for Movement Impairment Syndromes (Part II). Cureus. 2025;17(5):e83785. doi:10.7759/cureus.83785",
    "作者单位：意大利博洛尼亚脊柱中心、骨科整骨脊柱教育中心（OSCE）",
    f"文章类型：{b('综述＋作者提出的理论模型')}，三部曲的第二篇（第一篇讲桥的做法和肌电，见上一篇推文）",
], square=True))

A.append(h2("一句话先说清"))
A.append(p(
    f"作者提出：桥式用于腰痛，{mk('不只是为了练肌力，而是为了提高腰部筋膜的“张力”、增加节段稳定')}；"
    f"并且要{b('按腰痛的类型')}用不同的做法——屈曲型和伸展型几乎是反着来的。"
))

A.append(h2("背景：为什么腰痛要分型"))
A.append(ul([
    f"腰痛与腰伸肌无力、耐力差有关；健康人能保持完全伸髋的桥约 {b('170 秒')}，慢性腰痛患者约 {b('76 秒')}，所以桥也常用来评估腰椎稳定耐力",
    f"腰椎前凸和腰痛的关系一直有争议：传统观点认为{b('前凸过大')}引起腰痛，但不少研究发现{b('前凸减小')}（平背）更常见于腰痛、椎间盘突出和退变；也有荟萃分析认为两者没有差别",
    f"作者认为矛盾来自把所有“腰痛”混为一谈，应按 Sahrmann / Van Dillen 的{b('运动损伤综合征')}分型：哪个方向的动作和姿势诱发症状，就叫什么型",
]))
A.append(pic(2, "原文图 1：伸展型与屈曲型"))
A.append(ul([
    f"{b('伸展型（伸展—旋转型）')}：站立时腰椎前凸更大，后伸、旋转时症状加重，久站不舒服",
    f"{b('屈曲型（屈曲—旋转型）')}：腰椎较平，前屈或久坐时、之后疼痛",
]))

A.append(h2("作者的理论：筋膜张力平衡"))
A.append(pic(3, "原文图 2：前后方肌筋膜张力平衡与腰椎曲度"))
A.append(ul([
    "维持腰椎生理曲度需要前后方筋膜张力平衡；平衡被打破，曲度就会改变",
    f"{b('蠕变')}：长时间弯腰或塌腰坐，脊柱后方的韧带、筋膜会被慢慢拉松（蠕变），抵抗前屈的能力下降，形成恶性循环；恢复需要的时间比造成它的时间更长",
    f"被动组织松了，{b('竖脊肌就得多出力')}来补偿——这可能是腰痛患者肌电偏高、超声弹性成像测到肌肉“更硬”的原因",
]))
A.append(pic(4, "原文图 3：两种坐姿"))
A.append(pic(5, "原文图 4：屈曲—放松现象"))
A.append(ul([
    f"{b('屈曲—放松现象')}：健康人弯腰到底时竖脊肌肌电几乎消失，负荷交给被动组织；很多腰痛患者这时竖脊肌仍在收缩",
    "一项 12 周稳定训练（含桥）能减轻疼痛、恢复这一现象，其变化可解释功能评分改善的 38%",
    f"作者据此认为，腰痛的问题更多在{b('与肌肉并联的被动筋膜')}，康复应着重增强筋膜，而不只是练收缩力量",
]))
A.append(h3("腘绳肌、离心训练和筋膜"))
A.append(ul([
    "腘绳肌紧张与腰痛严重程度相关：紧张会限制骨盆前倾，弯腰时腰椎被迫多弯，加速后方筋膜蠕变——作者认为屈曲型腰痛可能与腘绳肌短缩有关",
    "单独练腰伸肌并不容易：负荷一大，臀大肌和股二头肌会接管更多",
    f"{b('离心训练')}后肌肉“硬度”常增加，胶原合成可增加约 300%，重复训练还有“重复负荷效应”；作者推测运动的损伤与修复主要发生在肌肉的结缔组织（筋膜）上，可让筋膜更结实——但这些研究都不是脊柱肌肉",
]))

A.append(h2("重点：两种腰痛，桥怎么做"))
A.append(img(13))
A.append(cap("两种腰痛的桥式做法对照（编者根据原文整理）"))
A.append(h3("屈曲型腰痛：多练腰背，少用腘绳肌"))
A.append(pic(6, "原文图 5：腰椎中立与腰椎过伸"))
A.append(ul([
    f"目标：最大限度激活竖脊肌、多裂肌和臀大肌，同时减少腘绳肌；{b('脚放近臀部')}",
    f"{red('与多数文献不同')}：作者主张终点做到{b('腰椎过伸')}，理由是在肌肉相对拉长的范围里训练会降低“张力”，而屈曲型腰痛需要的是增加后方张力",
    f"{b('剂量')}：双腿向心把骨盆抬到最高（含腰椎过伸）→ 等长保持 {b('20～30 秒')} → 离心回到中立；每组 {b('4～5 次')}",
    "进阶：双腿抬起后换单腿、保持骨盆水平（单侧负荷和扭转负荷，适合单侧问题和屈曲—旋转型）；等长从 5～10 秒开始逐步到 20～30 秒",
    f"{b('膝间夹球')}：屈曲型患者的外展外旋肌链常过度活跃，夹球激活内收肌，通过交互抑制让它们放松",
]))
A.append(pic(7, "原文图 6：单腿桥"))
A.append(pic(8, "原文图 7：膝间夹球"))
A.append(h3("伸展型腰痛：靠伸髋抬，腰不过中立"))
A.append(pic(9, "原文图 8：不同屈膝角度"))
A.append(pic(10, "原文图 9：腹部回缩"))
A.append(pic(11, "原文图 10：膝上套弹力带"))
A.append(pic(12, "原文图 11：背靠长凳的臀推"))
A.append(ul([
    f"骨盆主要靠{b('伸髋')}抬起，{b('腰椎不超过中立')}",
    f"屈膝 {b('60°～90°')}，让腘绳肌参与，促进骨盆后倾（腘绳肌长度与腰椎前凸成反比）",
    f"同时做{b('腹部回缩')}，限制腰椎后伸；{b('膝上套弹力带外展')}，通过交互抑制放松过度活跃的内收肌和屈髋肌",
    f"可改用{b('背靠凳的臀推')}，作者认为更容易避免腰椎过伸",
    "剂量同上：向心抬到最高（不过伸）→ 保持 20～30 秒 → 离心放下，每组 4～5 次",
]))

A.append(h2("这些内容能信几分"))
A.append(ul([
    f"{b('主要是理论')}：作者自己承认，“桥能改变筋膜张力”目前{red('没有直接证据')}，需要影像和生物力学研究验证，分型做法也没有临床试验",
    f"{b('推理链条很长')}：从其他部位（肘屈肌、股四头肌等）离心训练后的“硬度”变化，推到腰部筋膜、再推到桥式，每一步都有不确定性",
    f"{b('与第一篇的数据不完全一致')}：第一篇的肌电排行显示，竖脊肌在屈膝较小（脚放远）时最高，脚放近时竖脊肌也会下降；“脚放近、多练腰背”需要权衡",
    f"{b('“过伸”建议有争议')}：多数研究和临床建议桥时避免腰椎过伸，屈曲型患者做过伸的安全性和效果都没有被检验",
    "作者致谢中说明使用了 ChatGPT 润色语言",
    "优点：提醒临床按诱发方向区分腰痛，同一个动作根据分型调整踝、膝、腰的角度和附加动作，思路清楚、可操作",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('图 5 的 A、B 说反了')}：图注是“A 中立、B 过伸”，正文却写“做到腰椎过伸（图 5A）而不是中立（图 5B）”",
    f"{b('图 7 图注贴错')}：正文说的是膝间夹球（图片也是夹球），图注却是“不同屈膝角度 A～F”，与图 8 重复",
    f"{b('图 2 的说法前后相反')}：正文说“后方张力降低导致前凸增大（图 2C）”，图注却写 C 是“后方张力相对增加”",
    f"{b('腹部回缩的目的')}：原文写“为了增加髋伸肌筋膜系统的张力以进一步限制腰椎后伸，建议同时收腹”，逻辑上应是腹肌，表述混乱",
    f"{b('引用错位')}：“姿势不良导致脊柱负荷增加的确切机制尚不清楚”引的文献 3 是关于投掷动作的肌肉激活研究",
    f"{b('检索数字')}：第一篇说 Google Scholar 约 1500 篇，本篇说约 1400 篇",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先分型，再选做法')}：前屈、久坐痛 → 屈曲型；后伸、久站痛 → 伸展型",
    f"{b('伸展型')}：腰不过中立、屈膝 60°～90°、收腹、膝上套带，或改做背靠凳臀推——这些做法和主流建议一致，可以放心用",
    f"{b('屈曲型')}：脚放近、膝间夹球、逐步加单腿和等长时间是合理的；“做到腰椎过伸”是作者的理论建议，用之前要先确认患者做后伸不诱发症状，从小幅度开始",
    f"{b('剂量参考')}：向心抬起 → 等长 20～30 秒 → 离心放下，4～5 次一组",
    "筋膜理论仍待验证，评估效果还是要看疼痛、功能和动作控制的变化",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Colonna S, D'Alessandro A, Tarozzi R, Casacci F. Supine Bridge Exercise for Low Back Pain: A Fascial Approach for Movement Impairment Syndromes (Part II). Cureus. 2025;17(5):e83785. doi:10.7759/cureus.83785</em><br>"
    "原文以 CC BY 4.0 协议开放获取，版权归原作者所有。本文为学术交流用的中文解读：原文图 1～11 引自原文，图中中文标签为编者所加；做法对照卡为编者根据原文整理。如有侵权请联系删除。"
))

TITLE = "「桥式」腰痛做臀桥，屈曲型和伸展型要反着来？一个筋膜视角的新模型（三部曲之二）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>仰卧桥式治疗腰痛 Part II 推文</title>
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
