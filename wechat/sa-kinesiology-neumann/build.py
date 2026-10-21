#!/usr/bin/env python3
"""前锯肌运动学与针对性训练（Neumann、Camargo 2019）推文。

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
    "Neumann DA, Camargo PR. Kinesiologic considerations for targeting activation of scapulothoracic muscles – part 1: serratus anterior. Braz J Phys Ther. 2019;23(6):459-466. doi:10.1016/j.bjpt.2019.01.008",
    "第一作者 Donald Neumann 是《肌肉骨骼系统运动学》的作者，文中插图多来自这本教科书",
    f"文章类型：{b('大师课（叙述性综述）')}，与第 2 部分（斜方肌）配套",
], square=True))

A.append(h2("先说为什么前锯肌这么重要"))
A.append(p(
    f"前锯肌是肩复合体里最重要、临床上最相关的肌肉之一。它的{b('控制、力量或激活不足')}，被认为与肩峰下撞击、盂肱关节运动异常、肩胛运动障碍等多种疼痛问题有关。"
    f"想针对性地练好它，先要搞清楚它的解剖、功能和“坏了会怎样”。"
))

A.append(h2("解剖与功能"))
A.append(pic(2, "原文图 1：前锯肌"))
A.append(ul([
    f"{b('起止')}：起自第 1～9 肋外侧（呈锯齿状，因此得名），绕到肩胛骨前方，止于{b('肩胛骨内侧缘前面')}；与肩胛下肌、腹外斜肌的附着有交织",
    f"{b('神经')}：胸长神经（C5～C7），沿肌肉外表面长距离下行，{red('容易因外伤或过度牵拉受损')}，也可能因神经炎或原因不明而麻痹",
    f"{b('主要动作')}：{mk('肩胛前伸和上回旋')}。力线近乎水平，相对胸锁关节力臂长，所以前伸很有力",
    f"{b('“反向作用”')}：俯卧撑最后阶段，肩胛固定，前锯肌把胸廓和躯干“推离”地面；这需要斜方肌、菱形肌、肩胛提肌、胸小肌先稳住肩胛。{b('理解这一点是设计高强度前锯肌训练的关键')}",
    "与下斜方肌一起，能把上肢向斜前下方“伸长”，对转移（轮椅 ↔ 床）很重要，因此中段颈髓损伤者尤其要练这两块肌肉",
]))
A.append(pic(3, "原文图 2：上回旋力偶"))
A.append(ul([
    f"肩外展和前屈时，{b('前锯肌与斜方肌')}组成主要力偶让肩胛上回旋；前锯肌力臂好、多束纤维汇聚于下角，所以起主导作用",
    f"中斜方肌上回旋力臂小，但能{b('抵消前锯肌强大的前伸力')}；中斜方肌不足时，肩胛上回旋时会过度前伸",
]))
A.append(pic(4, "原文图 3：后倾和外旋的力偶"))
A.append(p(
    f"除了上回旋和前伸，前锯肌还参与肩胛的{b('后倾和外旋')}：与下斜方肌组成力偶完成后倾，与中斜方肌组成力偶完成外旋（以肩锁关节为轴）。"
    f"上回旋加后倾（以及少量外旋）可能{mk('增大或至少维持肩峰下间隙')}，这正是临床重视它的原因。"
))

A.append(h2("重点一：怎么测"))
A.append(pic(5, "原文图 4、5：前锯肌徒手肌力测试"))
A.append(ul([
    f"{b('肩外展测试')}：肩胛面外展约 120°～130°，检查者同时抵抗外展和肩胛上回旋；前锯肌弱时，肩胛撑不住，手臂会过早“塌”向内收",
    f"{b('肩胛前伸测试')}：仰卧或坐位，肩前屈 90°～100°、伸肘，抵抗整个上肢前伸；前锯肌弱时，肩胛被推向后缩和内旋，{red('内侧缘翘离胸廓——“翼状肩胛”')}",
    "翼状程度大致与无力程度成正比；两种方法都源自 Kendall 对脊髓灰质炎患者的经验",
]))

A.append(h2("翼状肩胛是怎么发生的"))
A.append(pic(6, "原文图 6：前锯肌瘫痪后的翼状肩胛"))
A.append(ul([
    f"外展时，前锯肌和上、下斜方肌产生的{b('上回旋力矩必须大于三角肌和冈上肌的下回旋力矩')}",
    f"前锯肌无力时，三角肌的拉力没人对抗，{red('肩胛反而下回旋')}，同时前倾、内旋",
    "长期翼状姿势会让胸小肌适应性短缩，进一步加重前倾和内旋；还可能伴随颈胸椎力线改变、塌腰坐姿、颈痛和上斜方肌过度激活",
    "肩胛位置异常会改变肩袖的拉力线，影响盂肱关节的运动控制，部分人可能挤压冈上肌等肩峰下组织（但肩峰下撞击是多因素的，不一定是疼痛唯一来源）",
]))

A.append(h2("重点二：用量角器看肩肱节律"))
A.append(pic(7, "原文图 7：量角器估计盂肱关节外展"))
A.append(p(
    f"方法很简单：每外展 10°，量一次{b('肩外展角')}（垂线与肱骨干）和{b('肩胛上回旋角')}（垂线与肩胛内侧缘），"
    f"两者相减就是{b('盂肱关节外展角')}。"
))
A.append(ul([
    f"{b('健康人')}：外展 70° 时肩胛上回旋 20°，盂肱约 50°；170° 时肩胛 54°、盂肱 116°，接近 {mk('2:1 的肩肱节律')}",
    f"{b('前锯肌无力伴前侧肩痛')}：前半程{red('肩胛反而下回旋')}，70° 时下回旋 20°，盂肱外展达 90°，{b('比整个肩的外展角还大')}；之后肩胛才开始上回旋，最多只能外展到 150°",
    "这种代偿会增加盂肱关节应力、改变肩袖拉力线和肩胛周围肌的长度-张力关系",
]))
A.append(table(["肩外展（°）", "健康人 肩胛旋转", "健康人 盂肱外展", "无力者 肩胛旋转", "无力者 盂肱外展"],
    [[str(a), str(s), str(a - s), (str(sb) if sb is not None else '—'), (str(a - sb) if sb is not None else '—')]
     for a, s, sb in zip(range(10, 180, 10), [0, 7, 11, 10, 17, 21, 20, 23, 27, 29, 39, 40, 46, 50, 51, 52, 54],
                         [-6, -1, 8, -9, -12, -18, -20, -27, -15, 8, 21, 32, 40, 46, 48, None, None])], first_bold=False))
A.append(tcap("原文图 7 中的数据表（中文整理；单位为度，正值上回旋、负值下回旋）"))

A.append(h2("重点三：练前锯肌的 5 个动作"))
A.append(p(
    f"理想的肩胛面外展应接近 2:1 节律，并伴随上回旋、适度外旋和后倾。训练目标是{b('让前锯肌和中、下斜方肌多出力，同时少用上斜方肌和胸小肌')}。"
))
A.append(pic(8, "原文图 8：动态拥抱"))
A.append(ul([f"{b('动态拥抱')}：弹力带绕背，双手像抱大树一样向前，{mk('最大程度前伸肩胛')}"]))
A.append(pic(9, "原文图 9：毛巾贴墙滑动"))
A.append(ul([f"{b('毛巾贴墙滑动')}：站立，手压毛巾沿墙向上滑，从中立位滑到{b('最大肩胛面外展 + 肩胛前伸')}"]))
A.append(pic(10, "原文图 10：前锯肌出拳"))
A.append(ul([f"{b('前锯肌出拳')}：伸肘，只用肩胛把拳头“送出去”；可站立拉弹力带、仰卧举哑铃，或由治疗师徒手抗阻"]))
A.append(pic(11, "原文图 11：手撑俯卧撑加强"))
A.append(ul([f"{b('俯卧撑加强（手撑）')}：做完俯卧撑后再把胸廓往上“顶”一下（肩胛固定、胸廓前伸），这就是前锯肌的“反向作用”；可在不稳定面上加难度"]))
A.append(pic(12, "原文图 12：肘撑俯卧撑加强"))
A.append(ul([f"{b('俯卧撑加强（肘撑）')}：平板支撑姿势下顶起胸廓；也可单侧保持前伸，治疗师对另一侧抗阻"]))

A.append(h2("这些建议能信几分"))
A.append(ul([
    f"{b('叙述性综述，以教科书理论为主')}：力偶、力臂分析多来自作者教科书的模型，属于理论推导",
    f"{b('动作的肌电证据没有给出')}：文中说这些动作“很多经肌电验证”，但没有列出任何具体肌电数值或比较",
    f"{b('量角器方法只用两个人举例')}：没有信度效度数据，且二维测量无法反映肩胛的倾斜和内外旋",
    f"{b('练前锯肌能否改善肩痛')}：文中只说“被认为与疼痛有关”，没有引用干预效果的随机对照试验",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('“前半程一直下回旋”不完全准确')}：图 7B 数据中，外展 30° 时肩胛其实是上回旋 8°，40° 起才转为下回旋；正文说“在大于 80° 后开始上回旋”，数据显示到 90° 仍下回旋 15°，100° 时才转为正值",
    f"{b('力偶成员说法不一')}：讲功能时说主要上回旋力偶是前锯肌和斜方肌（图 2 包括上、中、下三部分），讲病理时又只说前锯肌和上、下斜方肌",
    f"{b('“很多经肌电验证”缺依据')}：图 8～12 的动作没有逐一对应引用，读者无法知道哪个动作有证据、哪个只是经验",
    f"{b('参考文献错误')}：文献 14（Ekstrom）年份应为 2004 而非 2014；文献 20 作者 Cagnie 拼成“Gagnie”，页码“2184-2193”有误",
    f"{b('小错')}：rib cage 写成“rig cage”；“the scapular to paradoxically”应为 scapula；摘要中 palette 写成“pallet”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('先看再测')}：观察外展时肩胛是否翘起、是否过早下回旋，再用外展测试和前伸测试判断前锯肌力量",
    f"{b('一把量角器就能看节律')}：每 10° 量肩外展和肩胛上回旋角，算出盂肱角度，直观发现“盂肱外展比肩还多”的代偿",
    f"{b('训练顺序')}：从动态拥抱、出拳、贴墙滑动起步，再进阶到俯卧撑加强、不稳定面和单侧抗阻",
    f"{b('别忘了周围肌')}：中、下斜方肌要一起练，胸小肌短缩要松解，上斜方肌过度激活要控制",
    f"{b('翼状肩胛要查神经')}：明显翼状时考虑胸长神经损伤，必要时转诊做电生理检查",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Neumann DA, Camargo PR. Kinesiologic considerations for targeting activation of scapulothoracic muscles – part 1: serratus anterior. Braz J Phys Ther. 2019;23(6):459-466. doi:10.1016/j.bjpt.2019.01.008</em><br>"
    "原文版权：© 2019 巴西物理治疗研究与研究生协会，Elsevier 出版，保留所有权利；部分插图经许可转载自 Neumann《肌肉骨骼系统运动学》第 3 版（Elsevier 2017）。本文为学术交流用的中文解读：图 1～3、6 英文标注改为中文，图 4、5、8～12 照片直接引用，图 7 曲线按原文数据重绘。版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「肩关节」前锯肌怎么测、怎么练？翼状肩胛的力学机制与 5 个针对性动作"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>前锯肌推文</title>
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
