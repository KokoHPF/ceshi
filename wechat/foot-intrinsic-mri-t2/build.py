#!/usr/bin/env python3
"""T2 磁共振观察足内在肌运动后激活（Gooding 等 2016）推文。

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
    "Gooding TM, Feger MA, Hart JM, Hertel J. Intrinsic Foot Muscle Activation During Specific Exercises: A T2 Time Magnetic Resonance Imaging Study. J Athl Train. 2016;51(8):644-650. doi:10.4085/1062-6050-51.10.07",
    "作者单位：美国弗吉尼亚大学（Jay Hertel 也是“足核心系统”概念的作者之一）",
    f"研究类型：{b('描述性实验室研究')}，8 名大学田径 / 越野运动员",
], square=True))

A.append(h2("先说为什么要用磁共振看足内在肌"))
A.append(p(
    f"足内在肌维持内侧纵弓、控制足弓形变的幅度和速度，并参与站立和步行中的姿势控制；足底筋膜病、拇外翻、扁平足都与内在肌无力或萎缩有关。"
    f"临床上开了很多内在肌练习，但{b('每个练习到底练到了哪几块肌肉')}，证据很少。"
))
A.append(p(
    f"难点在于测量：足内在肌小而深、挨得很近，{red('表面肌电串扰严重')}；细针肌电又很难确认针扎进了哪块肌肉，还得超声引导，一次也测不了几块。"
    f"{mk('T2 磁共振')}能通过运动后肌肉 T2 信号的变化（与血流、代谢和组织水分改变相关）无创地反映{b('每一块肌肉')}的激活，这是第一次用它来看足内在肌。"
))

A.append(h2("怎么做的"))
A.append(ul([
    f"{b('对象')}：8 名美国大学一级联赛越野和田径运动员（5 男 3 女，20 岁），{b('都练过这些动作、能双脚正确完成')}；排除影响肌肉大小或功能的疾病和当时有伤的人",
    f"{b('流程')}：先坐着、脚不负重 10 分钟 → 仰卧在 3T 磁共振里扫基线（踝背伸 0° 固定在脚踏板上）→ 回到坐位，{b('左右脚各做一个动作，交替进行')}，节拍器 20 次 / 分钟、每次收缩 3 秒，各做 40 次 → 立即回扫",
    "两天各做 2 个动作，间隔 48 小时；动作和左右脚的分配用拉丁方随机",
    f"{b('分析')}：每块肌肉取横截面积最大的连续 3 层；以静息 T2 均值 + 1 个标准差为阈值，超过阈值的像素算“激活”；运动后激活比例减去运动前激活比例 = {b('激活增加百分比')}",
    "分析的肌肉：拇展肌、趾短屈肌、小趾展肌、足底方肌、小趾短屈肌、拇收肌斜头、拇短屈肌、骨间肌和蚓状肌（两者没有清楚的筋膜分界，合并分析）；拇收肌横头分不清，未分析",
    "评判标准：95% 置信区间下限不跨过 0，就算这块肌肉被激活",
]))
A.append(pic(3, "原文图 2：磁共振分析示例"))

A.append(h2("重点：四个动作怎么做"))
A.append(pic(2, "原文图 1：四个足内在肌运动"))
A.append(ul([
    f"{mk('短足')}：把跖骨头拉向跟骨，让内侧纵弓变短、抬高，{b('不屈脚趾、不用外在肌代偿')}",
    f"{mk('脚趾张开')}：先伸直 5 个脚趾，再同时外展所有脚趾，并把{b('大脚趾和小趾屈回地面')}，第 2～4 趾保持伸直；然后放松中间三趾",
    f"{mk('大脚趾伸展')}：抬起大脚趾，第 2～5 趾平放在地上不动",
    f"{mk('第 2～5 趾伸展')}：抬起第 2～5 趾，大脚趾平放在地上不动",
    "全部坐位、不加阻力，跟节拍器做，每次收缩 3 秒，做 40 次（预实验确定这个量能让所有人产生中等程度的激活）",
]))

A.append(h2("结果（压缩版）"))
A.append(pic(6, "原文图 5：各运动后各肌肉激活增加（编者中文重绘）"))
A.append(ul([
    f"{b('四个动作都激活了全部被测的足底内在肌')}，增加幅度 8.9%～35.2%，95% 置信区间都不跨过 0",
    f"{b('短足')}：小趾展肌（34.9%）、拇展肌（29.7%）、趾短屈肌（24.8%）最高——这些肌肉与纵弓平行",
    f"{b('脚趾张开')}：小趾展肌（35.2%）、拇收肌斜头（31.5%）、小趾短屈肌（30.2%）最高——止于第 1、5 趾的肌肉",
    f"{b('大脚趾伸展')}：范围较窄（13.1%～18.1%），趾短屈肌、拇展肌、小趾短屈肌稍高——可能在把其余脚趾压在地上、稳定第 1 跖骨头",
    f"{b('第 2～5 趾伸展')}：小趾展肌（22.5%）、拇短屈肌（20.2%）、拇收肌斜头（17.6%）较高——可能在把大脚趾稳在地上",
    "受试者之间差异很大，看不出谁哪块肌肉总是最高或最低；运动前激活水平与增加幅度只有弱相关（r = −0.19）",
]))
A.append(table(["肌肉", "短足", "脚趾张开", "大脚趾伸展", "第 2～5 趾伸展"], [
    ["拇展肌", "29.7（16.8, 42.6）", "18.9（7.4, 30.5）", "16.9（8.3, 25.5）", "16.5（5.8, 27.2）"],
    ["趾短屈肌", "24.8（11.8, 37.9）", "27.0（18.3, 35.7）", "18.1（9.5, 26.7）", "15.1（5.4, 24.7）"],
    ["小趾展肌", "34.9（26.7, 43.0）", "35.2（23.6, 46.9）", "14.1（3.9, 24.2）", "22.5（10.0, 35.1）"],
    ["足底方肌", "19.0（12.0, 26.0）", "25.4（12.6, 38.2）", "13.9（5.8, 21.9）", "17.0（4.7, 29.3）"],
    ["小趾短屈肌", "23.4（4.0, 42.9）", "30.2（9.7, 50.6）", "16.3（6.5, 26.1）", "10.3（4.9, 15.7）"],
    ["拇收肌斜头", "22.4（4.5, 40.3）", "31.5（17.2, 45.8）", "15.9（5.9, 26.0）", "17.6（7.4, 27.8）"],
    ["拇短屈肌", "20.8（7.6, 33.9）", "29.5（20.8, 38.3）", "13.1（4.3, 22.0）", "20.2（9.6, 30.7）"],
    ["骨间肌和蚓状肌", "16.7（4.5, 28.8）", "17.3（6.5, 28.0）", "15.0（9.3, 20.7）", "8.9（3.9, 13.9）"],
]))
A.append(tcap("原文表格：4 个足内在肌运动后各肌肉激活的增加，均值 %（95% 置信区间）（中文翻译）"))
A.append(pic(4, "原文图 3：每位受试者的激活热图（英文缩写已改为中文）"))
A.append(pic(5, "原文图 4：组均值激活的解剖热图"))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('只有 8 人，而且是会做这些动作的健康运动员')}：结果不能直接推到扁平足、足底筋膜炎患者或不会做动作的人",
    f"{b('没有比较动作之间的差异')}：只看每个动作是否“显著高于 0”，所以不能说哪个动作更好；置信区间普遍很宽、大量重叠",
    f"{b('T2 磁共振是运动“之后”的间接指标')}：反映的是 40 次低强度收缩后的代谢和水分变化，不能区分向心、离心或等长作用，也不等于肌肉力量",
    f"{b('坐位、无阻力')}：临床上常从坐位进阶到双脚站、单脚站，站立位的激活可能完全不同",
    f"{b('“激活”阈值取静息均值 + 1 个标准差')}：这个阈值本身就决定了基线上有相当一部分像素被算作“激活”，结果对阈值设定很敏感",
    "优点：第一次能一次看到 8 组足底内在肌，弥补了表面肌电串扰和细针肌电只能测少数几块的不足",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('短足的最低值认错了肌肉')}：结果说短足的增加“从足底方肌的 16.7%”开始，但表中 16.7% 是骨间肌和蚓状肌，足底方肌是 19.0%",
    f"{b('热图少了 1 个人')}：样本是 8 人，但图 3 的短足（A）和脚趾张开（B）热图只有 #1～#7 共 7 列，另外两个动作有 8 列；原文没有解释",
    f"{b('图号对不上')}：结果说“热图见图 4”“解剖图见图 5”，实际上每人热图是图 3、解剖热图是图 4、图 5 是均值和置信区间",
    f"{b('“±”含义不清')}：结果写“34.9% ± 8.1%”，这个 ± 其实是 95% 置信区间的半宽，不是标准差，原文没说明",
    f"{b('阈值描述混乱')}：先说“上限设为 900～10 000”，后面又说激活范围是“到上限 900”；这些数值是什么单位也没说",
    f"{b('因变量前后说法不一')}：方法说因变量是“T2 时间”，实际报告的是超过阈值的像素比例变化",
    f"{b('结论自相矛盾')}：讨论先说能“确定地识别哪些肌肉在用”，紧接着又说看不出规律、无法针对具体肌肉推荐动作",
    f"{b('小错')}：“flexor digitorum（24.8%）”漏了 brevis；“abductor digitorum minimi”应为 abductor digiti minimi；表格中“(3.9. 13.9)”标点有误",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('四个动作都能练到全部足底内在肌')}：短足、脚趾张开、大脚趾伸展、第 2～5 趾伸展都可以用，40 次就能产生明显激活",
    f"{b('短足偏纵弓方向的肌肉')}（小趾展肌、拇展肌、趾短屈肌），适合扁平足、足弓支撑不足",
    f"{b('脚趾张开偏第 1、5 趾的肌肉')}（小趾展肌、拇收肌斜头、小趾短屈肌、拇短屈肌）",
    f"{b('趾伸展练习强度较低')}，可作为入门或补充；要点是“抬起的脚趾抬，压着的脚趾压住”",
    f"{b('内在肌倾向于“一起工作”')}：别指望某个动作只练一块肌肉，更重要的是动作做对、量够",
    f"{b('进阶')}：从坐位 → 双脚站 → 单脚站，再到功能动作",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Gooding TM, Feger MA, Hart JM, Hertel J. Intrinsic Foot Muscle Activation During Specific Exercises: A T2 Time Magnetic Resonance Imaging Study. J Athl Train. 2016;51(8):644-650. doi:10.4085/1062-6050-51.10.07</em><br>"
    "原文版权归美国运动防护师协会（NATA）所有，未标注开放许可协议；原文图 4 的解剖底图经许可引自 BMJ 出版集团。本文为学术交流用的中文解读：图 1、2、4 引自原文并加中文标签和图注，图 3 英文缩写改为中文，图 5 按原文数据中文重绘，表格为中文翻译。如有侵权请联系删除。"
))

TITLE = "「足踝」4 个足内在肌练习各练到哪块肌肉？磁共振给出答案"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>足内在肌 T2 推文</title>
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
