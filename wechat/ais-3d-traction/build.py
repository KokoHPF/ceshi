#!/usr/bin/env python3
"""青少年特发性脊柱侧弯三维牵引＋常规康复 1 例（Mao 等 2026）推文。

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
    "Mao Z, Li C, Chen S, Zhao Z. Integration of three-dimensional spinal traction and conventional rehabilitation for structural correction in adolescent idiopathic scoliosis: a case report. Front Sports Act Living. 2026;8:1794187. doi:10.3389/fspor.2026.1794187",
    "作者单位：ASPINE 旭阳医生集团（上海）、上海裕华康复医院、复旦大学附属华山医院康复医学科、ASPINE Health Group（美国）",
    f"文章类型：{b('病例报告')}（1 例，32 周）",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"12 岁女孩，S 形侧弯：胸段右凸 22°、{b('腰段左凸 40°')}，伴腰痛；戴支具夜间不适、依从性差，也不想手术",
    f"采用{b('基于姿势的脊柱康复（PSR）')}：先骨盆、再胸腰，结合重力三维牵引、镜像训练、核心训练和脊柱手法，32 周共 50 次",
    f"结果：腰段 Cobb 角 {b('40° → 23°')}，旋转角 27° → 15°，腰痛 VAS 4 → 2",
    f"但{red('只有 1 例、没有对照')}，测量软件和治疗体系都来自作者所在公司；作者也强调支具仍是基石，本方案只是补充",
]))

A.append(h2("一、背景"))
A.append(img(2))
A.append(cap("青少年特发性脊柱侧弯（编者根据原文整理）"))
A.append(p(f"按照 SOSORT 指南，有进展风险、骨骼尚未成熟的患者，标准做法是{b('支具＋脊柱侧弯特定运动')}。但现实中，不少孩子因为不适、睡眠受影响或活动需求，戴不够规定的时间。这篇病例想回答的是：{b('戴不了支具时，还能做些什么')}。"))

A.append(h2("二、病例"))
A.append(img(3))
A.append(cap("病例资料（据原文整理）"))
A.append(img(4))
A.append(cap("原文图 1：初诊体态"))
A.append(img(5))
A.append(cap("原文图 2：初诊和 32 周时的 X 线"))
A.append(img(6))
A.append(cap("原文图 3：软件计算 Cobb 角的流程"))
A.append(p(f"Cobb 角同时用了两种方法：{b('作者公司的 AI 辅助软件')}（用 3000～4000 张侧弯 X 线训练，标记椎体中点后自动计算）和{b('人工测量')}。原文说明软件结果在用于临床解读前，需要医生核对。"))

A.append(h2("三、怎么治：先骨盆、再胸腰"))
A.append(img(7))
A.append(cap("治疗思路（据原文整理）"))
A.append(img(8))
A.append(cap("第一阶段（据原文表 2 整理）"))
A.append(img(9))
A.append(cap("第二阶段（据原文表 2 整理）"))
A.append(img(10))
A.append(cap("原文图 4：三类训练"))
A.append(p(f"重力牵引的设计：右侧卧（凸侧在下）、左髋屈曲，用沙袋固定 L1～L3，目的是通过轴向牵引减少腰段旋转应力；左髋屈曲位让右侧髂腰肌做离心收缩，帮助恢复骨盆对称。镜像训练的核心动作是{mk('右旋＋右移＋左侧屈')}，后期加弹力带固定骨盆、泡沫垫限制非目标节段。"))

A.append(h2("四、结果"))
A.append(img(11))
A.append(cap("Cobb 角和旋转角变化（据原文表 1 重画）"))
A.append(tcap("原文表 1：三个时间点的评估结果"))
A.append(table(["指标", "初诊", "16 周", "32 周"], [
    ["疼痛 VAS", "4", "3", "2（运动时最高 3）"],
    ["椎旁肌张力（改良 Ashworth）", "2", "2", "1+"],
    ["竖脊肌、髂腰肌肌力（MMT）", "3+", "4", "4+"],
    ["平衡误差评分（BESS，越低越好）", "17", "15", "11"],
    ["Cobb 角·软件（胸／腰）", "22° / 40°", "23° / 36°", "15° / 23°"],
    ["Cobb 角·人工（胸／腰）", "22° / 40°", "22° / 38°", "18° / 23°"],
    ["最大旋转角（胸／腰）", "12° / 27°", "15° / 20°", "9° / 15°"],
]))

A.append(h2("这篇文章能信几分"))
A.append(img(12))
A.append(cap("编者解读"))
A.append(ul([
    f"{b('单个病例')}、没有对照；PSR、牵引、手法、多种训练同时使用，无法分辨哪一项起作用",
    f"胸段人工测量只改善 4°（22° → 18°），原文也承认 3～4° 的改善可能接近测量误差；{b('腰段的改善两种方法一致')}，更可信",
    "两位作者受雇于 ASPINE 公司，评估软件和治疗体系都出自该公司；50 次治疗的时间和经济成本也不低",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    "摘要写“右凸胸腰段侧弯，Cobb 40°”，正文影像是胸段右凸 22°＋腰段左凸 40° 的 S 形侧弯",
    "图 2 图注说 B 是初诊腰段 40°、C 是 32 周胸段 15°，图内实际是 B 为胸段 15°、C 为腰段 40°",
    "MI 训练在图 4 图注里是镜像训练（Mirror Image），讨论里却写成运动想象（Motor Imagery）",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"有进展风险的骨骼未成熟 AIS 患者，{b('首选仍是支具＋特定运动')}；本例方案只适合确实无法耐受支具的个别患者",
    "可借鉴的思路：先评估骨盆和腿长，以主弯为重点；牵引、镜像训练都按“凸侧—凹侧”设计方向",
    "疗效判断以 X 线 Cobb 角为准，注意测量误差（约 3～5°）；定期复查，进展时及时转诊",
    "生活上：活动前后拉伸，手机举到视线高度，连续坐不超过 1 小时",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Mao Z, Li C, Chen S, Zhao Z. Integration of three-dimensional spinal traction and conventional rehabilitation for structural correction in adolescent idiopathic scoliosis: a case report. Front Sports Act Living. 2026;8:1794187. doi:10.3389/fspor.2026.1794187</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～4 引自原文，图 3 的英文标注改为中文、图 4 加了中文标签；结果图由编者根据原文表 1 重画；整理卡为编者根据原文撰写。"
))
TITLE = "「脊柱侧弯」戴不了支具怎么办？三维牵引＋镜像训练，12 岁女孩腰段 Cobb 角 40°→23°"
PTITLE = "青少年脊柱侧弯三维牵引推文"
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
