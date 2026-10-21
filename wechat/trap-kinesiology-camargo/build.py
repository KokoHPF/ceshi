#!/usr/bin/env python3
"""斜方肌运动学与针对性训练（Camargo、Neumann 2019）推文。

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
    "Camargo PR, Neumann DA. Kinesiologic considerations for targeting activation of scapulothoracic muscles – part 2: trapezius. Braz J Phys Ther. 2019;23(6):467-475. doi:10.1016/j.bjpt.2019.01.011",
    "作者为巴西圣卡洛斯联邦大学肩关节实验室的 Camargo 和《肌肉骨骼系统运动学》作者 Neumann",
    f"文章类型：{b('大师课（叙述性综述）')}，是第 1 部分（前锯肌）的姊妹篇",
], square=True))

A.append(h2("先说为什么要分开练斜方肌"))
A.append(p(
    f"前锯肌和斜方肌是作用于肩胛骨的{b('主要力偶')}。斜方肌分上、中、下三部分，纤维方向完全不同，作用也不同。"
    f"肩痛患者常见的模式是{red('上斜方肌过度激活，中、下斜方肌和前锯肌激活不足或延迟')}，所以训练时要“分部位”针对。"
))

A.append(h2("解剖与功能"))
A.append(pic(2, "原文图 1：斜方肌的三个部分"))
A.append(ul([
    f"{b('上斜方肌')}：起自枕骨、项韧带和最低到 C6 的棘突，几乎垂直下行，止于{b('锁骨外 1/3 后缘')}",
    f"{b('中、下斜方肌')}：起自 C7～T12 棘突；中部水平走行止于肩峰和肩胛冈，下部斜向上止于肩胛冈内侧根部",
    f"{b('神经')}：运动由副神经（第Ⅺ对脑神经）支配，感觉来自 C2～C4；副神经走行表浅，损伤后可出现{red('肩下垂')}（肩胛和锁骨下沉、前伸）和过度下回旋，长期可致盂肱、胸锁关节半脱位",
    f"{b('作用取决于哪端固定')}：颈部固定时上斜方肌上提并后缩锁骨；锁骨固定时则伸展、侧屈颈部。中、下斜方肌同理",
    f"总体上，{mk('斜方肌是肩胛的主要稳定肌，前锯肌是主要运动肌')}，两者有大量重叠",
]))
A.append(pic(3, "原文图 2：肩前屈时各肌的作用线"))
A.append(h3("上抬手臂时肩胛怎么动"))
A.append(ul([
    f"{b('上回旋')}最明显，可以摸肩胛下角的移动轨迹来验证",
    f"{b('内 / 外旋')}：前屈时通常轻度内旋、末端轻度外旋；靠近额状面的外展通常伴轻度外旋，让关节盂对准外展的肱骨",
    f"{b('后倾')}：肩峰向后离开前移的肱骨头，可能增大肩峰下间隙",
]))
A.append(h3("三部分各管什么"))
A.append(ul([
    f"{b('上斜方肌')}：只止于锁骨，主要通过锁骨起作用，强力上提和后缩锁骨。锁骨上提约贡献肩胛上回旋的 25%，锁骨后缩贡献肩胛外旋的 100%，所以它{b('对上回旋贡献不大，对肩胛外旋贡献大')}；只有在下斜方肌和前锯肌同时激活时，才间接参与上回旋力偶",
    f"{b('中、下斜方肌')}：直接把肩胛往内拉（后缩），并绕肩锁关节使肩胛外旋，用来{mk('对抗前锯肌的前伸和内旋')}",
    f"{b('下斜方肌')}与前锯肌是{b('主要的上回旋肌')}，尤其在外展早、中段；外展时比前屈时更有利",
    f"{b('后倾')}主要靠前锯肌，中、下斜方肌只是部分协助",
]))

A.append(h2("重点一：怎么测"))
A.append(pic(4, "原文图 3：斜方肌徒手肌力测试"))
A.append(ul([
    f"{b('上斜方肌')}：头颈稍向同侧侧屈，同时对抗头颈后伸侧屈和肩胛上提；无力时不能把肩峰拉向头部",
    f"{b('中斜方肌')}：俯卧，肩外展约 90° 并外旋，对抗水平外展；{red('肩胛内侧缘翘起')}（过度内旋）提示无力",
    f"{b('下斜方肌')}：俯卧，肩外展到与下斜方肌纤维平行（约 120°），保持手臂离床，对抗向下的阻力；{red('肩胛下角离开胸廓')}提示无力",
    "这些测试位置被证明能产生该部分最大的肌电活动",
    f"{b('还要看控制')}：让患者双侧在矢状面和额状面做空手和负重上举，观察肩胛运动障碍：内侧缘或下角突出、上举开始时过度耸肩、上举时快速下回旋",
]))

A.append(h2("肩痛时斜方肌出了什么问题"))
A.append(ul([
    f"{b('上斜方肌过度激活')} → 锁骨过度上提，伴不希望出现的{b('肩胛前倾')}",
    f"{b('下斜方肌激活减少')} → 肩胛上回旋不足",
    f"{b('中斜方肌激活延迟')} → 肩胛过度内旋、内侧稳定不足",
    f"但{red('肩胛运动障碍是肩痛的原因还是结果，目前并不清楚')}；疼痛、软组织紧张（后关节囊、胸小肌）、肌力或激活失衡、疲劳、驼背都可能参与",
]))

A.append(h2("重点二：怎么练"))
A.append(p(
    f"很多肩痛患者其实不是“没力气”，而是{b('耐力、控制或激活时机')}有问题。所以首选{mk('低到中等阻力、多次重复')}，配合治疗师的口令和反馈，重在动作质量；"
    f"确实有明显无力时才需要大负荷。原则是：{b('少用上斜方肌，多用中、下斜方肌和前锯肌')}。"
))
A.append(table(["训练动作", "针对部位"], [
    ["耸肩加后缩（图 4）", "上斜方肌"], ["过头耸肩（图 5）", "上斜方肌"], ["俯卧水平外展（图 6）", "中斜方肌"], ["过头后缩（图 7）", "中斜方肌"],
    ["俯卧肩胛定位（图 8）", "下斜方肌"], ["外旋位上举（图 9）", "下、中斜方肌"], ["俯卧后伸（图 10）", "下、中斜方肌"],
    ["侧卧外旋（图 11）", "下、中斜方肌"], ["侧卧前屈（图 12）", "下、中斜方肌"], ["俯卧 I、T、Y（图 13）", "下、中斜方肌"],
]))
A.append(tcap("原文表 1：针对斜方肌的训练动作（中文翻译）"))
A.append(h3("上斜方肌：只给真正需要的人"))
A.append(pic(5, "原文图 4：耸肩加后缩"))
A.append(pic(6, "原文图 5：过头耸肩"))
A.append(p(f"增强上斜方肌会增加肩胛前倾、压缩肩峰下间隙，{red('对多数肩痛、尤其有撞击症状的患者可能适得其反')}。只有明显上斜方肌无力、肩带下垂或前伸的患者才适合耸肩类训练。"))
A.append(h3("中斜方肌：肩胛内侧缘翘起的人"))
A.append(pic(7, "原文图 6：俯卧水平外展"))
A.append(pic(8, "原文图 7：过头后缩"))
A.append(h3("下斜方肌：肩胛前倾、内旋或上回旋不足的人"))
A.append(pic(9, "原文图 8：俯卧肩胛定位"))
A.append(pic(10, "原文图 9：外旋位上举"))
A.append(pic(11, "原文图 10：俯卧后伸"))
A.append(pic(12, "原文图 11：侧卧外旋"))
A.append(pic(13, "原文图 12：侧卧前屈"))
A.append(pic(14, "原文图 13：俯卧 I、T、Y"))
A.append(ul([
    f"共同要点：{mk('先把肩胛摆在后缩、下沉的位置，再动手臂')}，全程避免耸肩",
    "俯卧 I、T、Y 可由治疗师用手给反馈，依次做后伸（I）、水平外展（T）、上举约 120°（Y）",
    "外旋位上举用弹力带保持 30° 外旋张力，肩胛面上举到 90°",
]))

A.append(h2("这些建议能信几分"))
A.append(ul([
    f"{b('叙述性综述')}：功能分析多来自教科书模型和尸体、生物力学研究，属于理论",
    f"{b('表 1 只列名称，没有肌电数值')}：说是“循证动作”，但没给出各动作的激活程度或上 / 下斜方肌比值，读者无法比较",
    f"{b('“针对性训练能减轻肩痛”缺直接证据')}：文中承认运动障碍与肩痛的因果关系不明",
    f"{b('徒手肌力测试')}主要用于判断明显无力，对“控制和时机”问题不敏感",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('与第 1 部分说法不一')}：第 1 部分讲翼状肩胛时说上回旋力偶由前锯肌和{b('上、下斜方肌')}组成；本篇却说上斜方肌对上回旋的作用“次要而间接”，主要上回旋肌是下斜方肌和前锯肌",
    f"{b('上斜方肌的作用前后矛盾')}：功能部分说上斜方肌对肩胛{b('外旋')}贡献大、单独瘫痪会导致过度内旋；训练部分又说它“自然会使肩胛前倾”，而没提外旋，读者不清楚它到底是保护还是风险",
    f"{b('“锁骨上提贡献 75% 前倾”的表述')}：引用 Teece 的数据说锁骨上提贡献肩胛前倾的 75%，但上举时肩胛整体是后倾的，正文没有解释这一点",
    f"{b('测试证据引用不当')}：说测试位置能产生最大肌电活动，引用的是一篇讲肌电归一化方法的研究",
    f"{b('参考文献错误')}：文献 32 页码“2184-2193”有误；文献 31 作者 Castelein 重复列了两次；文献 25 中“subacromial”拼成“subcromial”",
    f"{b('小错')}：“described the upper trapezius has part of”应为 as；“Patients presenting either with...”缺少 or 的后半句",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先分型再选动作')}：内侧缘翘 → 中斜方肌；前倾 / 内旋 / 上回旋不足 → 下斜方肌；肩带下垂 → 才考虑上斜方肌",
    f"{b('多数肩痛患者别练耸肩')}，上斜方肌往往已经过度用力",
    f"{b('先摆好肩胛再抬手')}：后缩、下沉，治疗师用手给触觉反馈",
    f"{b('低负荷、多重复、重质量')}：目标是改善耐力和激活时机，而不是肌肉肥大",
    f"{b('与前锯肌一起练')}：斜方肌稳定、前锯肌推动，两者缺一不可（见第 1 部分）",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Camargo PR, Neumann DA. Kinesiologic considerations for targeting activation of scapulothoracic muscles – part 2: trapezius. Braz J Phys Ther. 2019;23(6):467-475. doi:10.1016/j.bjpt.2019.01.011</em><br>"
    "原文版权：© 2019 巴西物理治疗研究与研究生协会，Elsevier 出版，保留所有权利；图 1 经许可转载自 Neumann《肌肉骨骼系统运动学》第 3 版（Elsevier 2017）。本文为学术交流用的中文解读：图 1、2 英文标注改为中文，图 3～13 照片直接引用，表 1 为中文翻译。版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「肩关节」斜方肌上中下怎么分开练？肩痛患者为什么别急着耸肩"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>斜方肌推文</title>
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
