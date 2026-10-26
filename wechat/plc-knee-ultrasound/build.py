#!/usr/bin/env python3
"""膝关节后外侧角超声图解（Wu 等 2024）推文。

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
    "Wu WT, Onishi K, Mezian K, Naňka O, Wang B, Su DCJ, Ricci V, Chang KV, Özçakar L. Ultrasound imaging of the posterior lateral corner of the knee: a pictorial review of anatomy and pathologies. Insights into Imaging. 2024;15:39. doi:10.1186/s13244-024-01606-x",
    "作者单位：台湾大学医院北护分院与台大医学院复健科，以及美国、捷克、意大利、土耳其等多国康复与影像科",
    f"文章类型：{b('图解综述')}（正常图像来自第一作者本人，病变图像来自影像库）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"膝关节后外侧角结构多、层次乱，现行的欧洲膝关节超声基础扫查方案{b('没有系统覆盖')}这一区域，腘肌肌腱结合部拉伤这类问题容易漏",
    f"按{b('三层')}记：髂胫束／股二头肌腱 → 髌外侧支持带／外侧副韧带 → 关节囊层（腓肠豆腓韧带、弓状韧带、腘肌腱、腘腓韧带）",
    f"超声能看清这些韧带的{b('扭伤、部分撕裂和钙化')}；{mk('一定要和健侧对比')}，动态内翻应力下测外侧关节间隙更有价值",
    f"这一区域有{red('腓总神经和膝下外侧动脉')}经过，注射和抽吸最好在超声引导下做",
]))

A.append(h2("一、解剖：分三层来记"))
A.append(img(2))
A.append(cap("后外侧角的分层（编者整理）"))
A.append(img(3))
A.append(cap("原文图 1：遗体、MRI 和示意图"))
A.append(img(4))
A.append(cap("原文图 2：遗体解剖"))
A.append(img(5))
A.append(cap("原文图 3：MRI 上的外侧副韧带、股二头肌腱和弓状韧带"))
A.append(img(6))
A.append(cap("原文图 4：MRI 上的腘腓韧带和腓肠豆腓韧带"))
A.append(img(7))
A.append(cap("各结构要点（编者整理）"))
A.append(p(f"股二头肌腱和外侧副韧带的连接方式有 5 种：LCL 从长头前臂和直臂之间穿过（Ⅰ型）、与前臂融合（Ⅱ型）、两者合成联合腱（Ⅲ型）、LCL 绕到股二头肌腱前缘外侧（Ⅳ型）、LCL 走在直臂后方（Ⅴ型）。{b('了解这些变异，超声上才不会把正常形态当成损伤')}。"))

A.append(h2("二、超声怎么扫"))
A.append(img(8))
A.append(cap("扫查步骤（编者整理）"))
A.append(img(9))
A.append(cap("原文图 5：外侧副韧带、腘肌腱、腘肌和两条深层韧带的长轴"))
A.append(img(10))
A.append(cap("原文图 6：横切面由近到远"))
A.append(p(f"关键技巧：{b('腘肌腱和腘肌不在一条直线上')}，看完肌腱后，探头要向远端移、并把远端转得更水平，才能看到肌腹。看弓状韧带和腘腓韧带时，{b('动态短轴扫查')}能帮助把两条重叠的韧带分开，同时看清弓状韧带和腓总神经的关系。"))
A.append(img(11))
A.append(cap("原文图 7：腓肠豆腓韧带"))

A.append(h2("三、常见损伤长什么样"))
A.append(img(12))
A.append(cap("查体和超声表现（编者整理）"))
A.append(img(13))
A.append(cap("原文图 8：外侧副韧带病变"))
A.append(img(14))
A.append(cap("原文图 9：股二头肌腱病变"))
A.append(img(15))
A.append(cap("原文图 10：分叉的外侧副韧带（正常变异）"))
A.append(img(16))
A.append(cap("原文图 11：弓状韧带病变"))
A.append(img(17))
A.append(cap("原文图 12：腘肌病变与超声引导注射"))
A.append(ul([
    f"{b('腘肌腱')}在最深层，症状不好定位；怀疑它时要把{b('肌腱、肌肉肌腱结合部和肌腹')}都扫到。肌腹撕裂可以考虑超声引导下再生注射",
    f"{b('腱鞘囊肿')}可以超声引导下抽吸，注意避开腓总神经",
    "腘腓韧带扭伤：和对侧比，增厚、回声减低",
]))

A.append(h2("这篇文章能信几分"))
A.append(ul([
    f"{b('图解综述')}：主要价值是解剖和扫查方法，正常图像只来自一名健康志愿者（第一作者），病变图像是挑选出来的典型病例",
    f"超声诊断准确性只引用了一项 {b('16 例')}的小研究（2010 年），腘肌静态超声的敏感度只有 33%——深层结构超声容易漏，阴性不能排除损伤，重要损伤仍需 MRI",
    "优点：遗体、MRI、超声三者对照，扫查步骤讲得具体，附有探头位置示意",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "图 1 图注把遗体图和 MRI 图都标成了“(a)”，MRI 应为 (b)",
    "结论说超声引导“肯定能”有效减少腓总神经和膝下外侧动脉的误伤，但文中并没有给出相关数据",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"膝后外侧痛先做查体：{b('内翻应力试验')}（外侧副韧带）、{b('拨号试验')}（后外侧旋转不稳）、Noble 挤压试验（髂胫束摩擦）",
    f"超声按层扫，{b('先找外侧副韧带这个“路标”')}，再往深找腘肌腱、腘腓韧带，往后找股二头肌腱和弓状韧带",
    "所有发现都和健侧对比；动态内翻应力下外侧关节间隙 ≥10.5 mm 提示后外侧角复合损伤",
    "后外侧角损伤常合并交叉韧带损伤，怀疑不稳时仍应转诊做 MRI 和骨科评估",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Wu WT, Onishi K, Mezian K, Naňka O, Wang B, Su DCJ, Ricci V, Chang KV, Özçakar L. Ultrasound imaging of the posterior lateral corner of the knee: a pictorial review of anatomy and pathologies. Insights Imaging. 2024;15:39. doi:10.1186/s13244-024-01606-x</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～12 引自原文，图中中文标签为编者所加（超声机参数和结构缩写保留原样）；整理卡为编者根据原文撰写。"
))

TITLE = "「膝关节」膝后外侧痛，超声怎么看？后外侧角三层解剖、扫查步骤和常见损伤（附 12 张图）"
PTITLE = "膝后外侧角超声推文"
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
