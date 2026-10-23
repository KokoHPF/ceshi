#!/usr/bin/env python3
"""腘绳肌拉伤诊断、康复和预防推文

用法：python3 build.py   # 生成 article_body.html 和 preview.html
"""
import pathlib

HERE = pathlib.Path(__file__).parent


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
    "Heiderscheit BC, Sherry MA, Silder A, Chumanov ES, Thelen DG. Hamstring Strain Injuries: Recommendations for Diagnosis, Rehabilitation, and Injury Prevention. J Orthop Sports Phys Ther. 2010;40(2):67-81. doi:10.2519/jospt.2010.3047",
    "中文题目：腘绳肌拉伤：诊断、康复和损伤预防的建议",
    "作者来自美国威斯康星大学麦迪逊分校骨科与康复系、运动医学中心、生物医学工程系和机械工程系，通讯作者 Bryan Heiderscheit",
    "文章类型：临床述评（无系统检索），美国国家橄榄球联盟（NFL）医学慈善基金、美国国立卫生研究院等资助",
], square=True))

A.append(h2("研究背景"))
A.append(ul([
    "腘绳肌拉伤在运动员中很常见，愈合慢、症状拖得久",
    f"{b('约三分之一会复发')}，多在回到运动后第一年内，且回场后头 2 周风险最高；复发往往比第一次更重，停训时间可翻倍",
    "复发率这么高，说明常用的康复方案可能没解决无力、组织延展性下降和动作模式改变，传统回场标准也可能太粗",
    "这篇述评想回答三件事：急性腘绳肌拉伤怎么查、怎么分阶段康复和判断回场、以后研究和预防往哪走",
]))
A.append(pic(2, "原文图 1（图内英文已换成中文）"))

A.append(h2("方法"))
A.append(ul([
    f"{b('这不是原始研究')}：作者根据已有文献和自己团队的研究、临床经验，提出检查流程和三阶段康复指南",
    "康复指南适用于 1、2 度拉伤，主要依据的是肌内肌腱和相邻肌纤维损伤（冲刺型）的文献；不适用于完全断裂、撕脱的术后康复",
    "原文附有在线视频演示部分动作（本文未收录）",
]))

A.append(h2("结果：作者的主要建议"))
A.append(h3("一、受伤机制决定预后"))
A.append(ul([
    f"{b('冲刺型')}：高速跑时在摆动相末期受伤，多伤股二头肌长头的肌内肌腱和相邻肌纤维；急性期看起来更重，但恢复较快",
    f"{b('拉伸型')}：舞蹈、踢腿等屈髋 + 伸膝到极限时受伤，多伤半膜肌近端游离肌腱；症状轻，却要花长得多的时间才能回到伤前水平",
    f"恢复更慢的信号：{b('累及近端游离肌腱、越靠近坐骨结节、MRI 上损伤越长越粗')}",
    "但初诊时伤得重不重（查体或 MRI），预测不了会不会复发",
]))
A.append(pic(3, "编者据原文表 1、表 2 整理"))
A.append(h3("二、检查要点"))
A.append(pic(5, "编者根据原文整理"))
A.append(pic(4, "原文表 3（编者翻译重排）"))
A.append(pic(6, "原文图 2（图中只有分图字母和箭头，图注由编者翻译）"))

A.append(h3("三、康复为什么强调离心和神经肌肉控制"))
A.append(ul([
    "复发可能与三点有关：受伤肌肉持续无力、瘢痕导致肌腱单元延展性下降、受伤后动作模式改变；伤前就有的危险因素（腰盆肌力和控制差、股四头肌紧）也要一并处理",
    f"瘢痕比肌肉硬，会让力量峰值出现在{b('更短的肌肉长度')}；离心训练可以把峰值推回更长的长度，理论上能降低再伤",
    f"Sherry 和 Best 的研究：{b('渐进敏捷和躯干稳定训练（PATS）')}比牵伸加力量训练（STST）复发少得多，回场 2 周时 0% vs 55%，1 年时 8% vs 70%",
    "牵伸对预防和恢复的作用不明确；Slump 试验阳性时可加神经松动；超声、按摩等缺乏证据",
]))
A.append(h3("四、三阶段康复"))
A.append(pic(7, "编者据原文附录整理"))
A.append(pic(8, "编者据原文附录整理"))
A.append(pic(9, "原文图 3（照片内只有分图字母，图注由编者翻译）"))
A.append(pic(10, "编者据原文附录整理"))
A.append(pic(11, "原文图 4（照片内只有分图字母，图注由编者翻译）"))
A.append(pic(12, "原文图 5（照片内只有分图字母，图注由编者翻译）"))
A.append(h3("五、回场标准"))
A.append(pic(13, "原文附录（编者翻译重排）"))
A.append(ul([
    "常用的“活动度、力量、跳跑变向都不痛”太笼统：疼痛和僵硬一般 1～2 周就消失，但组织修复和再伤风险可能再持续数周",
    f"作者团队的研究：13 名已无痛、恢复全量运动的股二头肌拉伤运动员，{b('伤后数月仍可见股二头肌长头萎缩、短头代偿性肥大和瘢痕')}，但跑步时的关节运动和肌电并没有一致的双侧差异",
]))
A.append(pic(14, "原文图 6（图中只有分图字母和箭头，图注由编者翻译）"))
A.append(h3("六、预防"))
A.append(pic(15, "编者根据原文整理"))

A.append(h2("作者怎么解读"))
A.append(ul([
    "腘绳肌拉伤要从多方面评估：局部和邻近肌肉的力量、髋膝活动度都要查；受伤机制和损伤位置决定预后",
    f"康复要以{b('神经肌肉控制和离心力量')}为重点，按标准而不是按天数进阶，才能既安全回场又降低复发",
    "未来要研究：按损伤类型（尤其近端游离肌腱）定制的康复、能预测再伤的回场指标（如离心力量、峰力矩角度、动态 MRI），以及更大规模的预防研究",
]))

A.append(h2("这些结论能信几分"))
A.append(ul([
    f"{b('这是 2010 年的临床述评')}：没有系统检索，三阶段方案和回场标准是作者的建议，本身没有经过试验验证；组数、次数也是示例，原文要求个体化",
    f"{b('关键证据样本很小')}：PATS 与 STST 的对比来自一项 24 人的小研究（编者注），复发率 0% vs 55% 这样的悬殊差距需要谨慎看待；冲刺型和拉伸型的数据也来自 Askling 等两组十几人的研究（编者注）",
    f"{b('“走完方案”不等于“完全恢复”')}：附录说三阶段一般 2～6 周，而表 2 冲刺型回到伤前水平的中位数是 16 周，读者容易把“走完方案”误当成“完全恢复”",
    f"{b('回场标准依赖设备')}：离心 / 向心等速比值和峰力矩角度需要等速测试仪，多数基层机构做不到；“<5% 双侧差距”的界值来自一项复发运动员研究，而该研究里也有 31% 的复发者力量正常",
    f"{b('后来的证据有更新')}：本文发表后，北欧腘绳肌离心训练（Nordic）的预防证据、Askling 的“L 方案”等陆续出现，可以作为补充（编者观点）",
    f"{b('方向依然可信')}：重视损伤类型、强调离心和躯干骨盆控制、按标准进阶，与之后的研究和共识大体一致（编者观点）",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('瘢痕持续时间前后不一')}：正文说 13 名运动员是在伤后 5～19 个月接受 MRI，图 6 图注却写瘢痕持续“伤后 5～23 个月”",
    f"{b('第 2 阶段进阶条件两处写法不同')}：正文是“以 50% 最大速度向前、向后慢跑不痛”，附录是“中等强度向前、向后慢跑不痛”",
    f"{b('“4 倍”和 4.66')}：正文写离心 / 向心失衡使受伤“风险比增加 4 倍”，括号里给的风险比是 4.66；同处还把 confidence interval 误写成 confidence internal",
    f"{b('峰力矩角度的测试速度')}：正文只说两侧屈膝峰力矩角度应相近，附录才写明是 60°/s 向心测试",
    f"{b('“没有证据”的说法偏绝对')}：正文说按摩对拉伤后愈合“没有证据”、治疗性超声“似乎无益”，引用的多是健康人或动物研究",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先问清怎么伤的')}：冲刺型和拉伸型预后差别很大，拉伸型（舞蹈、踢腿、近端肌腱）要提前讲清可能需要大半年",
    f"{b('查体量化')}：屈膝 15° 和 90° 两个角度测力、记录最痛点到坐骨结节的距离，作为基线和进阶依据",
    f"{b('早期就动，但别拉长')}：第 1 阶段在无痛范围内练躯干骨盆和平衡，不做单独腘绳肌抗阻；有无力时避免末端拉长",
    f"{b('按标准进阶、按标准回场')}：没有等速仪时，至少做到屈膝 15° 和 90° 最大用力连续 4 次不痛、接近最大速度的专项动作不痛",
    f"{b('回场后继续练')}：瘢痕和萎缩可能持续数月，离心训练和躯干控制训练应继续作为预防",
]))

A.append(h2("附录：原文表格"))
A.append(tcap("原文附录（节选）　腘绳肌急性拉伤康复指南的进阶条件"))
A.append(table(["阶段", "训练频率", "进入下一阶段 / 回场的条件"], [
    ["第 1 阶段", "每天", "正常步幅走路不痛；很慢的慢跑不痛；俯卧屈膝 90° 抗 50%～70% 阻力等长收缩不痛"],
    ["第 2 阶段", "每周 5～7 天", "俯卧屈膝 90° 徒手肌力 5/5 且不痛；中等强度向前、向后慢跑不痛"],
    ["第 3 阶段", "每周 4～5 天", "力量完全且不痛（屈膝 90° 和 15° 最大用力连续 4 次不痛；离心腘绳肌 30°/s 与向心股四头肌 240°/s 比值双侧差 <5%；60°/s 屈膝峰力矩角度两侧对称）；活动度完全不痛；接近最大速度的专项动作不痛"],
]))
A.append(small("原文附录注：组数、次数应个体化；三阶段一般约需 2～6 周，但应按标准逐个患者进阶。表 1～表 3 的内容见正文中的整理卡片"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Heiderscheit BC, Sherry MA, Silder A, Chumanov ES, Thelen DG. Hamstring Strain Injuries: Recommendations for Diagnosis, Rehabilitation, and Injury Prevention. J Orthop Sports Phys Ther. 2010;40(2):67-81. doi:10.2519/jospt.2010.3047（PubMed Central 作者稿 PMC2867336）</em><br>"
    "本文为中文解读，仅作学术交流：原文图 1～图 6 引自原文，其中图 1 的英文由编者替换为中文，其余照片和 MRI 内只有分图字母和箭头；损伤类型对照、检查要点、三阶段康复、回场标准和预防卡为编者根据原文整理。原文版权归 JOSPT 所有，原文图 1A、图 6 另经 Springer 授权转载。"
))

TITLE = "「腘绳肌拉伤」怎么查、怎么分三阶段练、什么时候能回场"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>腘绳肌拉伤康复推文</title>
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
