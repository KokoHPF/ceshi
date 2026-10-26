#!/usr/bin/env python3
"""腰痛中筋膜与肌肉的相互作用（van Amstel 等 2025）推文。

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
    "van Amstel RN, Weide G, Wesselink EO, Noten K, Jacobs K, Pool-Goudzwaard AL, Jaspers RT. A review and empirical findings of fasciae and muscle interactions in low back pain. Frontiers in Physiology. 2025;16:1604459. doi:10.3389/fphys.2025.1604459",
    "作者单位：荷兰阿姆斯特丹自由大学人体运动科学系、阿姆斯特丹大学医学中心、Fysio Physics Group（物理治疗机构）等",
    f"文章类型：{b('假说与理论')}——叙述性综述＋作者团队的探索性观察（1 具遗体、1 名腰痛者、1 名健康者）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"腰背部从皮肤到骨头是{b('连成一体')}的：皮肤 → 浅筋膜 → 胸腰筋膜 → 背肌 → 脊柱韧带关节囊，作者还在棘突处找到一个把它们“钉”在一起的“中央筋膜间三角”",
    f"腰痛患者的胸腰筋膜往往{b('更厚、在肌肉上滑得更少')}，弯腰到底时竖脊肌也不容易放松",
    f"超声下{mk('推一推腰背的皮肤，位移能一层层传到筋膜和背肌')}，越深越小；健康人比腰痛者推得动",
    f"文献提示推皮肤类手法能降低筋膜刚度、减轻疼痛，但{red('躯干活动度并没有比假治疗更好')}；肌内效贴反而让筋膜更硬、也不止痛",
    f"作者自己的数据只有 {red('1 具遗体＋2 个人')}，整篇本质是“假说”，不是定论",
]))

A.append(h2("一、三个假说"))
A.append(img(2))
A.append(cap("三个假说（编者整理）"))
A.append(p(f"作者把徒手软组织松动、筋膜松解、肌内效贴等统称为“筋膜组织操作”，核心动作都是{b('让皮肤移位')}，在下面的组织里产生拉力和剪切力。这篇文章想回答：这些力能传多深？传下去以后组织会怎样？"))

A.append(h2("二、从皮肤到骨头，是一张连续的网"))
A.append(img(3))
A.append(cap("原文图 2：皮肤—关节—肌筋膜复合体"))
A.append(ul([
    f"{b('浅筋膜')}在皮下，厚约 10～20 mm，通过皮支持带纤维和皮肤韧带连接真皮和深筋膜",
    f"{b('胸腰筋膜')}分前、中、后三层，后层在骶部最厚、胸段最薄，由两层纤维方向垂直的胶原组成，并与多块躯干肌的肌外膜融合",
    f"{b('肌筋膜')}：肌内膜、肌束膜、肌外膜和肌腱连成蜂窝状网络；{b('关节筋膜')}：关节囊、韧带、骨膜和椎间盘纤维环",
    f"筋膜里不只有胶原，还有{b('成纤维细胞、肌成纤维细胞')}（能主动收缩，腰筋膜里的估计收缩力可达 445 mN/mm²）和大量感受器——筋膜既能“变硬”，也会“报信”",
]))
A.append(p(f"活动受限可能来自皮肤、浅筋膜、深筋膜、肌肉或关节筋膜中的任何一层变短变硬；它们在力学上相互牵连。被动刚度来自筋膜基质和肌纤维里的肌联蛋白，主动刚度来自肌纤维和肌成纤维细胞的收缩。"))

A.append(h2("三、腰痛者的筋膜：变厚、变黏、滑不动"))
A.append(img(4))
A.append(cap("腰痛患者的筋膜改变（文献证据）"))
A.append(p(f"作者的推测链条：{b('反复微损伤 → 炎症迁延 → 纤维脂肪祖细胞分化成脂肪和纤维组织 → 筋膜增厚、层间连接变密 → 组织变硬、滑动减少')}；组织越硬，局部受力越不均，又更容易再受伤。滑动减少还会削弱细胞受到的拉伸和剪切刺激（力学转导），影响肌肉的适应和再生。"))
A.append(img(5))
A.append(cap("原文图 7：遗体逐层解剖"))
A.append(img(6))
A.append(cap("原文图 8：L2-3 横断面的四种视角"))
A.append(img(7))
A.append(cap("原文图 9：中央筋膜间三角"))

A.append(h2("四、推皮肤的力能传多深：作者的探索性实验"))
A.append(img(8))
A.append(cap("原文图 10：腰背部各层筋膜的超声和 MRI"))
A.append(img(9))
A.append(cap("作者的探索性实验（编者整理）"))
A.append(p(f"简单说：{mk('推皮肤时，浅层几乎“一起走”，到了胸腰筋膜和竖脊肌之间开始“错开”')}——这个错开的地方正是腰痛者滑不动的位置。作者认为这说明手法的力确实传到了深层；但样本只有两个人加一具遗体，还需要大样本验证。"))

A.append(h2("五、传下去以后：组织可能怎么变"))
A.append(img(10))
A.append(cap("假说 3 的可能机制（编者整理）"))
A.append(ul([
    "这些机制大多来自数学模型、离体组织、细胞和动物实验，人体上的直接证据很少",
    f"原文给出的“剂量”线索：持续施力 {b('≥60 秒')}（黏弹性模型）、{b('至少约 5 分钟')}（动物抗炎研究）；但究竟什么方向、多大力、多久最好，还不知道",
    "作者还提出：筋膜变“松”、恢复层间滑动后，肌肉和筋膜里的细胞能重新感受到正常的拉伸和剪切，可能让后续的抗阻训练更有效",
    "触摸本身带来的舒适感（C 类触觉纤维、岛叶）也可能参与止痛，但作者认为即时的活动度变化主要还是神经肌肉反射",
]))

A.append(h2("六、临床研究证据"))
A.append(img(11))
A.append(cap("推皮肤类手法 vs 肌内效贴（编者整理）"))
A.append(ul([
    f"推皮肤类手法：多项研究显示胸腰筋膜刚度下降、竖脊肌刚度下降；荟萃分析显示{b('止痛效果优于对照和假治疗')}",
    f"但同一篇荟萃分析里，{red('躯干活动度并没有比假治疗改善更多')}",
    f"腰背推皮肤和推大腿后侧皮肤，都能降低胸腰筋膜刚度——{b('不一定要推在痛的地方')}",
    f"肌内效贴：贴上后筋膜和椎旁肌{b('更硬')}，不改变弯腰时竖脊肌的活动，荟萃分析也不支持止痛",
    "作者建议：临床上先试不同位置、不同方向推皮肤，看哪种组合能即时改善活动（他们称为 DAMT 试验），再据此决定手法或贴扎方向；但这个试验的信度效度还没验证",
]))

A.append(h2("这篇文章能信几分"))
A.append(ul([
    f"{b('定位就是“假说与理论”')}：综述是叙述性的，检索只看了每个检索式的前 100 条结果",
    f"{b('自己的数据极少')}：1 具遗体、1 名腰痛者、1 名健康者，没有统计；作者自己也说超声分不清筋膜和旁边的脂肪，厚度可能被高估",
    f"{b('机制证据间接')}：细胞、动物、离体组织和数学模型为主",
    f"{b('利益相关')}：第一作者和另一名作者受雇于 Fysio Physics Group（物理治疗机构）",
    "优点：把“筋膜从皮肤连到骨头”“腰痛者筋膜滑不动”讲得很直观，超声和解剖图很有教学价值",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('结论和正文矛盾')}：结论写“文献表明推皮肤类手法能有效降低胸腰筋膜刚度、{red('改善躯干活动度')}、减轻疼痛”，但正文引用的荟萃分析明确说躯干活动度与假治疗相比{b('没有显著改善')}",
    f"{b('肌内效贴被算进“降低刚度”的手法')}：摘要和图 1 的模型都说这些操作让组织变软，但正文引用的研究显示肌内效贴让胸腰筋膜和椎旁肌{b('更硬')}；结论却写“两者都对胸腰筋膜刚度有临床效果”",
    f"{b('表 1 疑似复制错误')}：健康者向左推皮肤时，弯腰位前 7 层的位移（-24.9, -24.4, -25.3, -7.2, -5.5, -8.8, -3.9 mm）与中立位一字不差；表注说弯腰位分不清胸腰筋膜浅、深两层，表里却给了两层各自的数值",
    f"{b('“两个人”的说法')}：小节标题写“两名个体的筋膜厚度增加”，实际只有 1 名腰痛者，另 1 名是健康对照",
    f"{b('同一张 MRI 参数不同')}：图 8 写 T1、TR 707、TE 11，图 10 写 TE 1",
    f"{b('资助声明前后不一')}：声明“未获得任何资助”，作者贡献里却有多名作者负责“获取资助”",
    f"{b('笔误')}：图 8 把浅层脂肪组织 SAT 解释成“superior adiposity tissue”；图 11 的髂前上棘写成“SIAS”；图 7 标题“Mecchanical”；正文“sham FMTs”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"给患者解释时可以说：{b('腰背从皮肤到骨头是一整张网')}，有些腰痛者这张网变厚变黏、滑不动，弯腰时肌肉也放松不下来",
    f"徒手推皮肤、软组织松动可以作为{b('止痛和改善刚度')}的辅助，单次持续时间可参考 1～5 分钟；方向和位置可以先试、看即时反应",
    "别指望肌内效贴“放松筋膜”；它更可能是增加支撑感",
    f"手法之后接上{b('主动运动和抗阻训练')}——作者也认为恢复筋膜滑动的意义，在于让后续训练更有效",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>van Amstel RN, Weide G, Wesselink EO, Noten K, Jacobs K, Pool-Goudzwaard AL, Jaspers RT. A review and empirical findings of fasciae and muscle interactions in low back pain. Front Physiol. 2025;16:1604459. doi:10.3389/fphys.2025.1604459</em><br>"
    "原文以知识共享署名（CC BY）协议开放获取。原文图 2、7～10 引自原文，图 2、7、9 中文标签为编者所加；假说卡、证据卡和实验卡为编者根据原文整理。"
))

TITLE = "「筋膜」推一推腰背的皮肤，力能传到多深？腰痛者的筋膜更厚、滑不动——超声和解剖怎么看"
PTITLE = "筋膜与腰痛推文"
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
