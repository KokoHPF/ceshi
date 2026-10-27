#!/usr/bin/env python3
"""正骨手法联合神经肌肉电刺激治疗腰椎间盘突出 1 例（Bao、Wang 2024）推文。

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
    "Bao Y, Wang Z. Combination of traditional Chinese bone setting and NMES technique for treating lumbar disc herniation: a case report. Front Rehabil Sci. 2024;5:1465623. doi:10.3389/fresc.2024.1465623",
    "作者单位：大连市第四人民医院康复医学科、大连理工大学附属中心医院脊柱外科",
    f"文章类型：{b('病例报告')}（1 例，随访 1 年）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"33 岁久坐白领，L3/4、L4/5、L5/S1 三节段{b('椎间盘突出')}，腰痛 VAS 6 分，弯腰受限、下肢放射痛",
    f"治疗三步走：{b('神经肌肉电刺激放松')} → {b('脊柱（定点）旋转复位法')}正骨 → {b('电刺激同步肌力训练')}，再加健康教育",
    f"作者报告 3 次治疗后压痛、痉挛消失；随访疼痛降到 0，前屈 45° → 80°，{b('1 年未复发')}",
    f"但{red('只有 1 例、多种方法同时用')}，“椎体位移”的理论也缺乏影像对比，结论要谨慎看",
]))

A.append(h2("一、为什么关注上班族腰痛"))
A.append(img(2))
A.append(cap("背景与作者的理论框架（编者根据原文整理）"))
A.append(p(f"作者采用的是冯天有教授的{b('“新医正骨”')}理论：椎间盘、小关节和韧带构成脊柱的{b('“内平衡”')}，脊柱前后左右的肌肉构成{b('“外平衡”')}。久坐劳损或退变后，一次弯腰搬物就可能造成单个或多个椎体“位移”，打破内外平衡，引起腰痛和代偿性的肌肉僵硬、脊柱侧弯。"))

A.append(h2("二、病例"))
A.append(img(3))
A.append(cap("病例概况（据原文整理）"))
A.append(img(4))
A.append(cap("原文图 1：MRI 和 CT"))
A.append(img(5))
A.append(cap("原文图 2：治疗前活动度"))
A.append(img(6))
A.append(cap("原文图 3：腰椎正位片"))
A.append(img(7))
A.append(cap("原文图 4：腰椎侧位片"))

A.append(h2("三、怎么治"))
A.append(img(8))
A.append(cap("治疗方案（据原文整理）"))
A.append(img(9))
A.append(cap("原文图 5：电极位置"))
A.append(img(10))
A.append(cap("原文图 6：左侧腰肌痉挛"))
A.append(img(11))
A.append(cap("原文图 7：复位椅"))
A.append(p(f"作者认为电刺激在这里有几层作用：早期{b('缓解腰肌痉挛')}，为手法复位做准备；早期做稳定肌的{b('等长收缩')}，减轻脊柱关节的机械应力；腰部肌肉以耐力型 Ⅰ 型纤维为主，电刺激程序可针对性训练；电刺激与主动收缩同步，还有助于{b('运动再学习和姿势控制')}。上班族时间有限，也可以在家继续使用。"))

A.append(h2("四、结果"))
A.append(img(12))
A.append(cap("原文图 8：治疗后活动度"))
A.append(img(13))
A.append(cap("活动度对比（据原文表 1、2 重画）"))
A.append(tcap("原文表 2：治疗前后对比"))
A.append(table(["项目", "治疗前", "治疗后"], [
    ["疼痛 VAS", "6", "0"],
    ["前屈", "45°", "80°"],
    ["后伸", "10°", "30°"],
    ["侧屈（左／右）", "25° / 15°", "25° / 25°"],
    ["复发", "有", "1 年随访无复发"],
    ["回归工作", "延迟", "很快复工"],
]))

A.append(h2("这篇文章能信几分"))
A.append(img(14))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例')}、没有对照；电刺激、正骨、核心训练、健康教育一起用，无法区分各自的作用",
    "入院时测了 JOA 评分（19 分），治疗后没有报告；也没有治疗后的影像，无法证实“椎体位移”被纠正",
    "优点：治疗流程和电刺激参数写得比较清楚，有治疗前后的活动度照片对比",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "表 1 表头有“旋转（左／右）”，但没有给出数值，表 2 也没有旋转",
    "结果说 3 次治疗后“前屈恢复正常”，表中随访前屈为 80°（表头正常范围 0～90°）",
    "讨论中冯天有手法的出处标为文献 12，实为电刺激综述；电刺激的出处标为文献 13，实为冯天有学术研究，两者对调",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"腰肌痉挛明显时，可以{b('先用电刺激或其他方法放松')}，再做手法或运动治疗",
    "后期用电刺激配合主动收缩训练核心（腰腹肌、瑜伽球背伸、平板支撑），比单纯被动治疗更有利于维持疗效",
    f"对久坐人群，{b('健康教育')}不能少：定时起身、椅子有靠背、搬物屈髋屈膝背挺直",
    "正骨手法需由受过训练的医生操作；原文也提醒手法不当可能造成神经损伤或进一步错位",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Bao Y, Wang Z. Combination of traditional Chinese bone setting and NMES technique for treating lumbar disc herniation: a case report. Front Rehabil Sci. 2024;5:1465623. doi:10.3389/fresc.2024.1465623</em><br>"
    "原文以知识共享署名（CC BY）协议开放获取。原文图 1～8 引自原文，图 2、8 的中文动作标签为编者所加，影像设备参数保留原样；活动度图由编者根据原文表 1、2 重画；整理卡为编者根据原文撰写。"
))
TITLE = "「腰椎」久坐白领三节段椎间盘突出：电刺激放松＋正骨复位＋电刺激练核心，1 年未复发？"
PTITLE = "腰突正骨联合电刺激推文"
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
