#!/usr/bin/env python3
"""大负荷力量训练治疗足底筋膜炎（Caratun 等 2018）推文。

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
    "Caratun R, Rutkowski NA, Finestone HM. Stubborn heel pain: treatment of plantar fasciitis using high-load strength training. Can Fam Physician. 2018;64(1):44-46. PMID: 29358253",
    "作者来自加拿大渥太华大学和布吕耶尔医院，发表在《加拿大家庭医生》的“临床实践技巧”栏目",
    f"文章类型：{b('临床经验分享')}。核心方案来自 Rathleff 等 2015 年的随机对照试验，作者做了简化",
], square=True))

A.append(h2("先说为什么要给足底筋膜“加负荷”"))
A.append(p(
    f"足底筋膜炎是足跟下方疼痛最常见的原因，普通人群患病率约 3.6%～7%，在跑步损伤里占到 8%。"
    f"它的名字有点误导：病理上看到的主要是{b('退变')}，而不是炎症，所以也有人叫它“足底筋膜病”。"
))
A.append(pic(2, "原文图 1：损伤最常见的位置在足底筋膜的跟骨附着点"))
A.append(p(
    f"大多数人一年内会好转，但{red('约 40% 的患者 2 年后还有症状')}。常用的激素注射、矫形鞋垫、夜间支具、牵伸，效果都不太稳定。"
    f"既然是退变，思路就借鉴跟腱病和髌腱病：{mk('用大的张力负荷刺激胶原合成，促进修复')}。"
))
A.append(pic(3, "原文图 2：提踵 + 足趾背伸，两路张力叠加在足底筋膜上"))
A.append(p(
    f"关键在{b('绞盘机制')}：足趾背伸时，足底筋膜像绞盘上的绳子一样被卷紧；这时再做提踵给跟腱加负荷，"
    f"两股力一起把足底筋膜“拉满”。所以动作要点就是{b('脚趾垫高再提踵')}。"
))

A.append(h2("重点：怎么做"))
A.append(pic(4, "原文图 3：患者指导（中文翻译）"))
A.append(pic(5, "原文图 4：踩在 T 恤卷上的单腿提踵"))
A.append(h3("准备"))
A.append(ul([
    f"{b('垫子用 T 恤，不用毛巾')}：作者发现毛巾太厚不好抓，纯棉 T 恤卷成约 {b('2 cm')} 粗的圆柱，柔软、好调整",
    f"{b('位置')}：T 恤卷放在台阶边缘往里约 5 cm，足趾包住它；台阶边缘在{b('脚长一半')}的位置，足跟悬空",
    "旁边最好有扶手，防止摔倒",
]))
A.append(h3("动作"))
A.append(ul([
    f"{mk('上 5 秒 → 顶端停 3 秒 → 下 5 秒')}，慢起慢落，离心阶段和向心阶段一样慢",
    f"尽量{b('单腿')}做，另一条腿离地；做不了或双脚都痛，就双脚一起",
    "下放时足跟可以低于台阶（图 4 A），让足底筋膜和跟腱都拉到位",
]))
A.append(h3("剂量和进阶"))
A.append(ul([
    f"{b('每天 1 组 10 次')}，至少坚持 {b('3 个月')}或做到不痛为止",
    f"{b('第 1～4 周')}：自身体重；一开始做不满 10 次很正常，能做几次做几次",
    f"{b('第 5～12 周')}：背包装书负重，加到{mk('刚好在力竭前能做完 10 次')}的重量",
    f"{b('疼痛规则')}：练的时候痛可以接受，{red('第二天比之前更痛')}就是“坏的痛”，要减次数或减重量",
    "配一张进度表，每天打钩记录，提高依从性",
    "可以单独使用，也可以和减重、牵伸、消炎药等一起用；做满 6 个月还没好就回去找医生",
]))

A.append(h2("和原始试验方案比，改了什么"))
A.append(pic(6, "原始试验方案与本文简化方案对比（编者整理）"))
A.append(p(
    f"作者说原方案组数一直在变，患者记不住、坚持不了，所以简化成{b('每天 1 组 10 次')}。好记是好记，但要注意，"
    f"{b('总量和强度都变了')}：前 4 周只用自身体重，算不上“大负荷”；每次只有 1 组，比原方案的 3～5 组少得多；"
    f"频率又从隔天改成了每天。"
))

A.append(h2("这些结果能信几分"))
A.append(p(f"这篇文章本身{b('没有数据')}，证据全部来自那一项原始试验。PubMed 上该试验的摘要显示："))
A.append(ul([
    f"48 名经超声确认的足底筋膜炎患者，{b('两组都配了鞋垫')}，一组每天做足底筋膜专项牵伸，一组隔天做大负荷力量训练",
    f"{b('3 个月')}时（主要终点）：力量组足功能指数比牵伸组低 29 分（95% 置信区间 6～52），{mk('好得更快')}",
    f"{b('1、6、12 个月')}：两组{red('没有差别')}；次要指标也都没有差别",
]))
A.append(p(
    f"所以更准确的说法是：大负荷力量训练{b('可能让疼痛和功能更快改善')}，而不是长期效果更好。"
    f"作者的简化版本则{b('没有经过任何对照研究验证')}，“依从性和疗效都提高了”只是临床印象。"
))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“已验证的方案”说法过头')}：原始证据只有一项 48 人的试验，而且优势只在 3 个月出现；作者又改了节奏、组数、频率和负荷，改完的版本并没有验证过",
    f"{b('练的是跖屈肌，却说增加背屈力量')}：讨论部分说这个方案能提高踝{b('背屈')}力量，抵消足底筋膜炎患者背屈力量下降。提踵练的是小腿三头肌（跖屈）；而引用的文献 11 讲的是腓肠肌挛缩（背屈活动度受限），并不是背屈力量",
    f"{b('引用不支持论点')}：说“与其他治疗相比疗效更好”时引用了文献 10，那是一篇跟腱病离心训练和胶原合成的研究，不是足底筋膜炎的疗效比较",
    f"{b('图注缩写不准')}：图 1、图 2 图注把 Ca 写成“跟骨附着点”，但图中 Ca 标的是整块跟骨",
    f"{b('“大负荷”名不副实')}：前 4 周只用自身体重、每天 1 组，与原方案从第 1 周起就用 12 次力竭重量做 3 组差别很大",
    f"{b('频率改成每天，没解释理由')}：原试验特意隔天训练，给组织留恢复时间；每天做到力竭附近，组织能否恢复文中没有讨论",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('脚趾垫高 + 慢速提踵')}是这个方案的核心，绞盘机制让足底筋膜真正吃到负荷",
    f"{b('按原试验的强度更有依据')}：隔天练，从 12 次力竭重量×3 组起步，逐步加到 8 次×5 组；患者实在记不住，再用本文的简化版提高依从性",
    f"{b('提前讲清楚“好的痛”和“坏的痛”')}，用第二天的反应调整剂量",
    f"{b('期望要说实话')}：它可能让好转来得更快，但一年后和牵伸 + 鞋垫的效果差不多",
    "家里就能做，只需要台阶、T 恤和装书的背包，成本很低",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Caratun R, Rutkowski NA, Finestone HM. Stubborn heel pain: treatment of plantar fasciitis using high-load strength training. Can Fam Physician. 2018;64(1):44-46. PMID: 29358253</em><br>"
    "<em>Rathleff MS, Mølgaard CM, Fredberg U, et al. High-load strength training improves outcome in patients with plantar fasciitis: a randomized controlled trial with 12-month follow-up. Scand J Med Sci Sports. 2015;25(3):e292-300. doi:10.1111/sms.12313</em><br>"
    "原文版权归加拿大家庭医生学会及作者所有，未标注开放许可协议。本文为学术交流用的中文解读：图 1～4 引自原文（英文标注改为中文，图 3 为中文翻译重排），方案对比卡为编者整理，原始试验数据来自其 PubMed 摘要。版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「足底筋膜炎」脚趾垫高再提踵：大负荷力量训练治顽固性足跟痛"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>足底筋膜炎力量训练推文</title>
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
