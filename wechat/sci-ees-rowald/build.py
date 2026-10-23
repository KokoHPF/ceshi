#!/usr/bin/env python3
"""活动依赖性脊髓神经调控（Rowald 等 2022）推文。

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
    "Rowald A, Komi S, Demesmaeker R, et al. Activity-dependent spinal cord neuromodulation rapidly restores trunk and leg motor functions after complete paralysis. Nat Med. 2022;28(2):260-271. doi:10.1038/s41591-021-01663-5",
    "瑞士洛桑联邦理工学院和洛桑大学医院 Courtine、Bloch 团队，临床试验 STIMO（NCT02936453）的一部分",
    f"研究类型：{b('3 名患者的可行性研究')}，没有对照组；本文据作者接受稿 PDF 解读",
], square=True))

A.append(h2("先说为什么这篇值得看"))
A.append(p(
    f"硬膜外电刺激（刺激电极放在脊髓背面的硬膜外）能让一部分脊髓损伤患者重新走路，但以前用的电极板是{b('为治疗疼痛设计的')}，"
    f"对准的是脊髓后柱，而真正起作用的是{b('背根')}里的大直径传入纤维；电极板又太短，覆盖不到所有控制腿和躯干的背根。"
    f"结果是：只有少数运动完全损伤的人，在多名治疗师陪练好几个月后才能走。"
))
A.append(p(
    f"这项研究做了三件事：{mk('重新设计电极板、用个体化模型规划手术位置、开发能快速配置“按活动定制”刺激程序的软件')}。"
    f"3 名{red('感觉运动完全瘫痪')}的患者，{b('刺激第一天')}就能在跑台上迈步，随后几天内完成站、走、骑车、游泳和躯干控制。"
))

A.append(h2("怎么做的：从解剖到电极"))
A.append(pic(2, "原文图 1：脊髓解剖差异与个体化模型"))
A.append(ul([
    f"测量 27 人的脊髓：{b('节段长度个体差异很大')}（尤其上腰段），但{b('背根入髓区的宽度很一致')}",
    "用高分辨率磁共振和断层扫描建立 15 个个体化有限元模型，模拟刺激时哪些纤维被募集；模拟证实刺激优先募集大直径传入纤维",
]))
A.append(pic(3, "原文图 2：新型电极板的排布"))
A.append(ul([
    f"{b('16 个电极')}覆盖 T12～S2 共 16 条背根；长度按平均脊髓确定（73 mm），比常用的传统 5-6-5 电极长 18.8 mm",
    f"外侧电极距中线 {b('4.7 mm')}：理论最优是 2.3 mm，但偏 1 mm 选择性就掉一半，放宽一点更不怕手术偏差",
    f"加{b('中线电极')}做多极刺激，把电流“引”向目标根、少刺激对侧；骶段背根挤在一起，用{b('横向一排电极')}区分",
]))
A.append(pic(4, "原文图 3：术前规划与术中验证"))
A.append(ul([
    f"术前用{b('功能磁共振')}：被动活动关节或振动肌腱，找出每块腿部肌肉的本体感觉纤维投射到哪个节段，放进个体化模型",
    f"模型预测的最佳位置，术中用单脉冲刺激 + 肌电验证：{mk('上下移动 2 mm 选择性都会下降')}，说明预测准确；通用模型做不到",
    "同一患者术中对比：新电极能覆盖全部目标背根，传统 5-6-5 电极不能",
]))

A.append(h2("重点一：刺激程序怎么配"))
A.append(pic(5, "原文图 4：针对具体活动的刺激程序"))
A.append(ul([
    f"{b('第 1 步：建配置库')}（≤1 小时）。仰卧位给 500 毫秒短串刺激，看诱发的腿部动作，调整阴极阳极组合；"
    f"{mk('伸肌用 20 Hz，屈肌用 100 Hz')}（两类运动神经元偏好的频率不同）",
    f"{b('第 2 步：套模板')}。把健康人走路时“哪个节段、什么时候激活”的时空图，转成刺激序列模板：屈髋 → 全腿屈曲 → 承重 → 推进，左右交替",
    f"{b('第 3 步：现场微调')}（≤1 小时）。治疗师和患者一起试走，软件实时显示肌电、关节角度和刺激时序，边走边调",
    f"{b('其他活动照此办理')}：坐到站、站立、骑行、游泳、腿举、深蹲都有各自的程序",
]))
A.append(h3("第一天的表现"))
A.append(ul([
    f"三人刺激前都无法迈步，肌肉完全没反应；{b('第一天')}就能在跑台上独立迈步（需要较多体重支撑，伸展成分不足）",
    f"再过 1～3 天，能在多方向体重支撑系统下{b('地面行走')}；第一天最多走 300 多步，不像直接电刺激肌肉那样很快疲劳",
    "3 人中 2 人能按指令主动加大步长，说明刺激放大了残存的下行信号",
]))

A.append(h2("重点二：躯干也能刺激"))
A.append(pic(6, "原文图 5：躯干专用刺激程序"))
A.append(ul([
    f"刺激投射到 {b('T12')} 节段的背根，可以选择性激活上腹肌、腹斜肌、腰方肌，腿几乎不动；单侧刺激还能让躯干向一侧偏",
    f"刺激开时{b('腰椎过度前凸被纠正')}，从屈曲位回到直立位的时间明显缩短",
    "躯干程序还用于前拉、四点跪位、肩前举等训练，坐姿下拉器械的负重增加",
]))

A.append(h2("重点三：5 个月康复训练"))
A.append(pic(7, "原文图 6：在社区中恢复独立"))
A.append(ul([
    f"{b('流程')}：术后约 1 个月配置刺激程序 → {mk('5 个月康复，每周 4～5 次，每次 1～3 小时')}，内容随进步个体化调整",
    f"{b('训练内容')}：跑台和地面行走（缆绳机器人体重支撑、多种助行器）、坐到站、站立、腿部和躯干训练、游泳、骑行",
    f"{b('自己能操作')}：简化版软件给治疗师用平板、患者用智能手表；助行器上装按钮，随时切换站立 / 行走、支撑 / 摆动；也可以用穿戴传感器自动触发",
    f"{b('结果')}：三人都逐渐恢复{b('全负重')}，能在社区中独立站立；扶前轮助行器独立行走，完成 6 分钟和 10 米步行试验；其中一人能上楼梯、走复杂地形",
    "还能骑手脚并用的躺式三轮车、站着打拳击、在吧台站着喝东西、在湖上划桨",
    f"大腿和躯干肌肉面积增加 {b('18%～33%')}；{b('3 人中 2 人')}关掉刺激后也能主动收缩髂腰肌",
    "康复期结束后可进入延长期，在家继续使用，随访最长 6 年",
]))
A.append(p("下面这些扩展数据图展示了方法细节，可按需查看："))
for n, t in [(8, "扩展数据图 1：个体化模型建立流程"), (9, "扩展数据图 2：根丝建模与解剖变异"), (10, "扩展数据图 3：功能磁共振找投射区"),
             (11, "扩展数据图 4：术前规划"), (12, "扩展数据图 5：个体化模型才能准确预测"), (13, "扩展数据图 6：刺激方案配置步骤"),
             (14, "扩展数据图 7：不同频率诱发不同动作"), (15, "扩展数据图 8：第一天的即时效果"), (16, "扩展数据图 9：躯干肌选择性募集"),
             (17, "扩展数据图 10：躯干刺激的即时效果"), (18, "补充图 1：软件与无线刺激链路"), (19, "补充图 2：关掉刺激后的主动肌电活动")]:
    A.append(pic(n, t))

A.append(h3("受试者情况"))
A.append(table(["项目", "P1", "P2", "P3"], [
    ["性别 / 入组年龄", "男 / 32 岁", "男 / 41 岁", "男 / 29 岁"],
    ["伤后时间", "8 年 11 个月", "1 年 3 个月", "2 年 10 个月"],
    ["损伤分级（前 → 后）", "A → A", "A → A", "B → C"],
    ["神经损伤平面（前 → 后）", "T4 → T3", "T3 → T3", "T7 → T7"],
    ["下肢运动评分（右 | 左，满分各 25）", "0 | 0 → 0 | 0", "0 | 0 → 0 | 0", "0 | 0 → 2 | 4"],
    ["其中：屈髋 L2（前 → 后）", "0 | 0 → 0 | 0", "0 | 0 → 0 | 0", "0 | 0 → 1 | 2"],
    ["伸膝 L3 / 踝背屈 L4（后）", "0 / 0", "0 / 0", "1|1 / 0|1"],
    ["肛门深压觉 / 肛门自主收缩", "无 / 无", "无 / 无", "有 / 无"],
    ["轻触觉总分（满分 112，前 → 后）", "46 → 44", "46 → 43", "63 → 61"],
    ["针刺觉总分（满分 112，前 → 后）", "44 → 43", "48 → 42", "58 → 60"],
    ["L1～S2 皮节轻触 / 针刺", "全为 0", "全为 0", "全为 0"],
]))
A.append(tcap("原文补充表 1：受试者人口学与神经学状况（中文翻译，总分为左右相加）"))

A.append(h2("这些结果能信几分"))
A.append(ul([
    f"{b('只有 3 人，没有对照')}：属于可行性研究，不能区分多少来自刺激、多少来自高强度康复本身",
    f"{b('功能仍有限')}：作者自己也说{red('动作并不自然')}；康复后 6 分钟步行最好的约 55 米，另两人不到 25 米，10 米步速 0.1～0.26 米/秒，都是开着刺激、扶着助行器完成的",
    f"{b('统计把重复动作当成独立样本')}：例如躯干回位时间每人 5 次重复做组间检验，样本量其实是 1 人",
    f"{b('利益冲突明显')}：多名作者持有相关专利或是 ONWARD 公司员工、股东，电极和刺激器由 Medtronic 和 ONWARD 捐赠",
    f"{b('门槛很高')}：需要高分辨率磁共振、功能磁共振、个体化建模、术中电生理和改装刺激器，目前只在研究中心可行",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b("“第一天就能站、走、骑、游”说得太满")}：摘要说一天之内恢复这些活动，正文却写第一天只能在跑台上靠大量体重支撑迈步，地面行走要再过 1～3 天，骑行和游泳没给时间",
    f"{b("“无需任何帮助”与方法矛盾")}：正文说 6 分钟和 10 米步行试验“没有任何帮助”，方法里却写测试时开着刺激、用标准四轮助行器；正文又说是前轮助行器",
    f"{b('康复时长对不上')}：方法写 5 个月康复，图 6 图注写“练习 6 个月后”",
    f"{b('刺激频率前后不一')}：正文说伸肌 20 Hz、屈肌 100 Hz；扩展数据图 6 写 13～20 Hz 和 80～100 Hz；扩展数据图 7 和 9 又用 120 Hz",
    f"{b('并行波形数量不一致')}：正文说刺激平台可实时更新最多 10 个刺激波形，补充图 1 图注写最多 4 个",
    f"{b('损伤平面对不上')}：方法写 P2 是 T6/T7 损伤、P3 是 T5/T6，补充表 1 写 P2 为 T3、P3 为 T7",
    f"{b("“完全瘫痪”不完全准确")}：P3 入组时是 B 级（运动完全、感觉不完全），康复后变为 C 级，下肢运动评分从 0 升到 6，却仍和另两人一起称为“完全感觉运动瘫痪”",
    f"{b('图 5 统计写错')}：图注 P3 的 p 值写成“1429”（应为 0.1429，即无显著差异），而正文说三人回位都“变得轻松”",
    f"{b('图 3c 标注重复')}：三组柱状图都标成 P1，应分别为三名受试者",
    f"{b('人群描述')}：图 1 图注写 27 人为“男/女/多元性别”，但没有给出构成；3 名受试者全是男性、都是摩托车事故胸段损伤，代表性有限",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('刺激只是“开门”，训练才是主体')}：哪怕是这么先进的技术，患者也要经过 5 个月、每周 4～5 次、每次 1～3 小时的康复，才能把功能带到社区",
    f"{b('康复内容很“常规”')}：体重支撑步行、坐到站、站立、躯干训练、骑行、游泳，物理治疗师熟悉的项目都用得上，关键是在刺激打开时练",
    f"{b('躯干控制别忽视')}：躯干稳定直接决定站立和上肢活动，刺激 T12 背根就能改善姿势",
    f"{b('残存通路值得练')}：2 人关掉刺激后恢复了主动屈髋肌电，说明高强度主动训练可能唤醒“沉默”的纤维",
    f"{b('对患者说实话')}：目前仍是研究阶段，样本极少，效果是“能扶着助行器慢慢走、站着做些事”，不是恢复正常行走",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Rowald A, Komi S, Demesmaeker R, et al. Activity-dependent spinal cord neuromodulation rapidly restores trunk and leg motor functions after complete paralysis. Nat Med. 2022;28(2):260-271. doi:10.1038/s41591-021-01663-5</em><br>"
    "原文版权：© 2022 The Author(s)，由 Springer Nature 独家授权出版，未采用开放许可协议。本文为学术交流用的中文解读：图片均引自原文（英文标注改为中文并加中文图注，人物面部模糊为原文所做），补充表 1 为中文翻译。版权归原作者与期刊，如有侵权请联系删除。"
))

TITLE = "「神经康复」完全瘫痪，刺激第一天就迈步：脊髓电刺激 + 5 个月康复精读"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>脊髓神经调控推文</title>
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
