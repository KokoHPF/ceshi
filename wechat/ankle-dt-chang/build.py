#!/usr/bin/env python3
"""Chang 2026 动态贴扎改善慢性踝关节不稳动态平衡推文：生成 article_body.html 与 preview.html。

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


def pic(n, t, w=None):
    h = img(n)
    if w:
        h = h.replace("width:100%;max-width:100%;", f"width:{w};max-width:{w};")
    return h + cap(t)


def gif(name, t, w="56%"):
    return ('<p style="margin:0 0 8px;text-align:center;">'
            f'<img src="gifs/{name}" alt="{t}" style="width:{w};max-width:{w};height:auto;display:block;margin:0 auto;"></p>'
            + cap(t))


def tcap(t):
    return f'<p style="margin:0 0 8px;font-size:14px;line-height:1.6;color:#000;font-weight:bold;">{t}</p>'


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2026 年第 21 卷第 7 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：Effects of Dynamic Taping on Dynamic Balance and Proprioception in Recreational Athletes with Chronic Ankle Instability（动态贴扎对慢性踝关节不稳业余运动员动态平衡和本体感觉的影响）",
    f"{b('作者')}：Yun-Chi Chang（张允琪）, PhD · Po-Tsun Chen, PhD · Wei-Jie Hsu, MS · Hsiao-Yun Chang（张晓昀）, PhD",
    f"{b('机构')}：辅仁大学体育学系；长庚大学物理治疗学系；台湾体育运动大学运动保健学系",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2026;21(7):681-692",
    f"{b('PMCID')}：PMC13327846",
    f"{b('研究类型')}：单盲随机对照试验",
    f"{b('证据级别')}：2 级",
    f"{b('关键词')}：elastic tape · ankle sprain · postural control · joint position sense",
], square=True))

A.append(h2("🎯 背景：白贴稳但限制活动，弹性贴能不能两全？"))
A.append(p(
    f"踝扭伤是运动中最常见的损伤之一，发生率约 {b('0.72～13.6 次/1000 运动小时')}；80%～90% 为外侧踝扭伤。外侧扭伤者中 {b('80%')} 会复发，反复扭伤者中 {b('75%')} 会发展为{b('慢性踝关节不稳（CAI）')}，表现为本体感觉和平衡受损。"
))
A.append(p(
    f"CAI 运动员常用{b('运动白贴（ST，非弹性）')}保护踝关节：能增加稳定，但限制活动度和表现。弹性贴则能让运动员自由活动。{b('肌内效贴')}能刺激皮肤感受器、改善本体感觉，但{b('不能提供支撑')}。"
))
A.append(p(
    f"{b('动态贴扎（Dynamic Tape，DT）')}由澳大利亚物理治疗师 Ryan Kendrick 发明：可以{b('多方向拉伸')}，弹性像橡皮筋一样强，可以通过改变运动模式来管理负荷、吸收外力、辅助发力。"
    f"此前研究只看过急性扭伤、平足或 CAI 的{b('静态')}平衡，DT 能否改善 CAI 的{hl('动态平衡')}尚不清楚。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["项目", "内容"],
    [
        ["研究对象", "28 名 CAI 业余运动员（CAIT <25 分），随机分为 DT 组和 ST 组，每组 14 人（男女各 7）"],
        ["干预", "ST：传统白贴（马镫、马蹄、8 字、锁跟）；DT：动态贴扎（见图 2 和视频）"],
        ["结局", "关节位置觉误差（手机测角 App）；动态平衡（单腿多次跳跃稳定测试）；贴扎前和贴扎后 15 分钟"],
        ["本体感觉", f"两组位置觉误差都显著下降（ST 6.64° → 2.52°，DT 5.40° → 2.23°），{b('组间无差异')}"],
        ["动态平衡", f"{b('只有 DT 组显著改善')}（87.38 → 64.64 分，越低越好），ST 组无显著变化（81.20 → 76.21 分）；交互作用 F = 20.42，P < 0.001，η² = 0.44"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('两种贴扎都能马上改善踝的位置觉，但只有动态贴扎同时改善了跳跃落地的动态平衡')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、研究设计与对象"))
A.append(ul([
    f"单盲随机对照，前测-后测设计；按 G*Power 计算（效应量 f = 0.5，检验效能 0.8，α = 0.05，考虑 10% 脱落）需 {b('28 人')}",
    f"纳入：至少一次踝扭伤且 {b('CAIT <25 分')}；近 3 个月下肢无其他肌骨损伤或手术；每周至少运动 2 次、每次 2 小时以上",
    "排除：下肢骨折或手术史；神经或前庭功能障碍",
    "两组基线（年龄、身高、体重、CAIT、运动频率、性别）无显著差异（表 1）",
]))

A.append(h3("❇️二、两种贴扎方法"))
A.append(h4("🔻运动白贴（ST）"))
A.append(p(f"使用 Mueller MTape（1.5 英寸）。先用{b('衬垫')}包住足和踝，在小腿下端和前足打{b('锚条')}，再依次贴{b('马镫、马蹄、8 字和锁跟')}（图 1）。这些手法限制踝关节活动、增加稳定。"))
A.append(pic(2, "图1：运动白贴步骤。(a) 衬垫，(b) 锚条，(c) 马镫，(d) 马蹄，(e) 8 字，(f) 锁跟"))
A.append(h4("🔻动态贴扎（DT）"))
A.append(p(f"按 DT 官方教学视频操作，贴扎人员都有 DT 1、2 级国际认证；受试者坐位。"))
A.append(ul([
    f"① 足{b('背屈 + 外翻')}：从{b('第一趾背侧')}起贴，斜行 30°～45° 越过足背和踝关节到外踝，再绕过足跟",
    f"② 足{b('跖屈 + 外翻')}位：从外踝贴到足跟，绕过跟骨底部",
    f"③ 足底朝向足跟、{b('中立位')}：从足外侧绕向距骨，最后锚定在{b('内踝上方靠近小腿')}处",
]))
A.append(pic(3, "图2：动态贴扎完成后的外观。(a) 外侧观，(b) 内侧观，(c) 上面观——从第一趾背侧起，斜越足背到外踝，绕足跟和跟骨，止于内踝上方"))
A.append(gif("video1.gif", "动图：踝关节动态贴扎完整操作示范（原文补充视频，2 倍速播放）"))

A.append(h3("❇️三、结局指标"))
A.append(h4("🔻关节位置觉误差"))
A.append(ul([
    "坐位屈膝 90°、踝自然下垂（图 3）；在腓骨头、外踝、第五跖骨头和足外侧贴彩色标记，用手机测角 App（G-pro Goniometer）在 1.5 m 外测角",
    f"目标角度为{b('全踝活动度（跖屈 + 背屈）的 50%')}；闭眼记住该位置，练习 3 次后正式测 3 次取平均",
    f"测试时{b('戴眼罩、耳机播放白噪声')}，排除视觉和前庭线索；重测信度 ICC = 0.940",
]))
A.append(pic(4, "图3：手机 App 测量踝关节主动活动度。(a) 起始位，(b) 终止位（App 界面英文已模糊处理）"))
A.append(h4("🔻动态平衡：单腿多次跳跃稳定测试"))
A.append(ul([
    "热身做 3～5 次单腿跳（不在测试标记上练习），然后沿预设顺序单腿连续跳过各标记点，每次落地后保持稳定 5 秒（图 4）",
    f"记两类错误：{b('落地错误')}（落点错误、对线丢失）和{b('平衡错误')}（失去姿势控制、另一只脚着地等）",
    f"{b('动态平衡得分 = 落地错误数 × 10 + 平衡错误数 × 3')}，{red('分数越低越好')}；重测信度 ICC = 0.868",
]))
A.append(pic(5, "图4：单腿多次跳跃稳定测试。(a) 测试场景，(b) 跳跃顺序：从起点依次跳到 1～10 号标记（T 恤字样已模糊处理，“Start”已改为“起点”）"))

A.append(h3("❇️四、结果"))
A.append(tcap("表1　受试者基本特征（n = 28）"))
A.append(table(
    ["指标", "ST 组（n = 14）", "DT 组（n = 14）", "F", "P"],
    [
        ["年龄（岁）", "21.07 ± 1.20", "20.50 ± 0.65", "1.15", "0.135"],
        ["身高（cm）", "168.21 ± 10.10", "169.21 ± 9.84", "0.018", "0.779"],
        ["体重（kg）", "65.50 ± 16.96", "66.28 ± 20.11", "0.051", "0.912"],
        ["CAIT 评分", "16.92 ± 3.02", "20.50 ± 3.74", "0.832", "0.956"],
        ["运动频率（天/周）", "2.5 ± 1.65", "2.5 ± 1.55", "0.028", "1.00"],
        ["性别（男/女）", "7/7", "7/7", "—", "—"],
    ],
))
A.append(small("CAIT：坎伯兰踝关节不稳工具；ST：运动白贴；DT：动态贴扎。"))
A.append(tcap("表2　关节位置觉误差和动态平衡得分（均数 ± 标准差）"))
A.append(table(
    ["指标", "ST 组 前测", "ST 组 后测", "DT 组 前测", "DT 组 后测"],
    [
        ["位置觉误差（°）", "6.64 ± 4.11*", "2.52 ± 2.28*", "5.40 ± 3.07*", "2.23 ± 2.07*"],
        ["动态平衡得分", "81.20 ± 21.15", "76.21 ± 19.97", "87.38 ± 25.83*", "64.64 ± 20.69*"],
        ["落地错误", "6.36 ± 1.68", "5.93 ± 1.64", "6.45 ± 2.25*", "4.75 ± 1.85*"],
        ["平衡错误", "5.87 ± 1.87", "5.64 ± 2.05", "7.62 ± 2.85*", "5.71 ± 2.63*"],
    ],
))
A.append(small("* P < 0.05，前后测差异显著。"))
A.append(tcap("表3　混合设计重复测量双因素方差分析"))
A.append(table(
    ["指标", "时间效应 F / P / η²", "组别效应 F / P / η²", "交互作用 F / P / η²（检验效能）"],
    [
        ["位置觉误差", "49.54 / <0.001* / 0.656", "0.571 / 0.457 / 0.021", "0.847 / 0.366 / 0.032（0.144）"],
        ["动态平衡得分", "52.57 / <0.001* / 0.669", "0.091 / 0.765 / 0.003", "20.42 / <0.001* / 0.440（0.992）"],
        ["落地错误", "32.50 / <0.001* / 0.556", "0.630 / 0.434 / 0.024", "11.61 / 0.002* / 0.309（0.906）"],
        ["平衡错误", "14.44 / 0.001* / 0.357", "1.126 / 0.298 / 0.042", "8.845 / 0.006* / 0.254（0.817）"],
    ],
))
A.append(small("* P < 0.05。"))
A.append(ul([
    f"{b('本体感觉')}：两组位置觉误差都明显下降（时间效应 η² = 0.656），但无交互作用——两种贴扎改善程度相近",
    f"{b('动态平衡')}：显著的组别 × 时间交互作用（η² = 0.44，大效应）；{b('只有 DT 组')}总分、落地错误和平衡错误都显著下降，ST 组均无显著变化",
]))

A.append(h3("❇️五、为什么动态贴扎能改善动态平衡？"))
A.append(ul([
    f"{b('皮肤感受器刺激')}：两种贴扎都刺激皮肤机械感受器，增加本体感觉反馈、提高运动神经元激活——所以位置觉都改善了",
    f"{b('本体感觉改善 ≠ 动态平衡改善')}：动态平衡还受其他因素影响；白贴带来的感觉输入可能不足以改变跳跃落地时的姿势控制",
    f"{b('弹性随动')}：弹性贴更贴合皮肤，随动作牵拉皮肤和筋膜，持续提供感觉输入",
    f"{b('纠正位置错误 + 弹性助力')}：CAI 踝关节距骨常前移；DT 可能起稳定作用，其强回弹和弹性阻力帮助吸收负荷、协助发力，纠正错误的关节或运动模式",
    "与 Lim 和 Park 在平足者中的结果一致：DT 比无贴扎显著提高 Y 平衡测试成绩，且不限制活动度",
]))

A.append(h3("❇️六、作者提到的局限"))
A.append(ul([
    "样本量小，增加 II 类错误风险，结果只适用于 CAI 业余运动员",
    "只看了贴后 15 分钟的即时效应，不知道长时间运动中效果能否维持",
    "没有评估贴扎与再损伤的关系；未来应在切步、折返跑等专项动作中评估",
]))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('亮点')}：直接比较临床常用的白贴和动态贴扎；动态平衡用跳跃落地任务，比静态站立更贴近运动；附有完整贴扎视频，可直接学习",
    f"{b('没有对照组')}：缺少无贴扎或假贴扎组，位置觉的改善可能部分来自{b('练习效应')}（同样的测试做两次）",
    f"{b('盲法交代不清')}：称为“单盲”，但没说明谁被盲；贴扎外观完全不同，受试者和测试者都很难盲",
    f"{b('设计描述矛盾')}：摘要写随机对照试验，方法部分又称“前测-后测比较设计”；ST 组用了衬垫，可能削弱皮肤刺激",
    f"{b('基线 CAIT 差异被忽略')}：ST 组 16.92 分、DT 组 20.50 分，相差约 3.6 分（DT 组不稳较轻），表中 P = 0.956 与此差距不相符；表 1 年龄 P 值 0.135 也与 F = 1.15 不太匹配",
    f"{b('数字不一致')}：正文落地错误交互作用写 F = 111.61，表 3 为 11.61；摘要 η² 写 0.03/0.44，正文 0.032/0.440；表 3 自由度写 F(2,28)，摘要为 F(1,26)",
    f"{b('结果解读需谨慎')}：DT 组前测动态平衡得分更差（87.38 vs 81.20），存在一定回归均值的可能；“η Power”等表头和“may is more adaptable”等语句有笔误",
]))

A.append(h2("📌 总结：CAI 运动员，白贴还是动态贴扎？"))
A.append(p(
    f"{red('① 两种都能')}：即时改善踝关节位置觉（误差约减少 3～4°）<br>"
    f"{red('② 只有 DT')}：改善单腿跳跃落地的动态平衡（落地错误和平衡错误都减少）<br>"
    f"{red('③ DT 贴法')}：背屈外翻起贴于第一趾背侧 → 斜越足背到外踝 → 绕足跟和跟骨 → 止于内踝上方<br>"
    f"{red('④ 可能机制')}：皮肤感觉输入 + 弹性回弹助力和稳定，同时不限制活动<br>"
    f"★ {red('注意')}：小样本、只看 15 分钟即时效应、无空白对照，长期效果和预防再扭伤作用未知"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Chang YC, Chen PT, Hsu WJ, Chang HY. Effects of Dynamic Taping on Dynamic Balance and Proprioception in Recreational Athletes with Chronic Ankle Instability. "
    "Int J Sports Phys Ther. 2026;21(7):681-692. PMCID: PMC13327846.</em><br>"
    "文中 4 张图片和动图均来自原文及其补充视频：图 3 App 界面英文和图 4 T 恤字样已模糊，“Start”改为“起点”；表 1～3 已译为中文，仅用于学术交流。"
))

TITLE = "「踝关节」慢性踝不稳，白贴还是动态贴扎？随机对照试验告诉你（附贴扎视频）"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>动态贴扎推文</title>
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
