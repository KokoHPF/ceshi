#!/usr/bin/env python3
"""ACL 重建术后十项任务进阶（Buckthorpe 2020）推文。

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


def tcap(t):
    return f'<p style="margin:0 0 8px;font-size:14px;line-height:1.6;color:#000;font-weight:bold;">{t}</p>'


A = []
A.append(img(1))
A.append(cap("原文首页（IJSPT 2020 年第 15 卷第 4 期）"))

A.append(p(red("📚 文献卡片"), "margin-bottom:10px;"))
A.append(ul([
    f"{b('英文原题')}：A Ten Task-Based Progression in Rehabilitation after ACL Reconstruction: From Post-Surgery to Return to Play – A Clinical Commentary（ACL 重建术后康复的十项任务进阶：从术后到重返赛场）",
    f"{b('作者')}：Matthew Buckthorpe, PhD · Antonio Tamisari · Francesco Della Villa, MD",
    f"{b('机构')}：Isokinetic 医疗集团，FIFA 卓越医学中心（意大利博洛尼亚；英国伦敦）",
    f"{b('期刊')}：International Journal of Sports Physical Therapy（IJSPT）",
    f"{b('年卷期')}：2020;15(4):611-623",
    f"{b('PMCID')}：PMC7735691",
    f"{b('文章类型')}：临床评论（Clinical Commentary）",
    f"{b('关键词')}：biomechanics · criterion-based progressions · movement system · performance rehabilitation · screening",
], square=True))

A.append(h2("🎯 背景：术后 12 周就能跑？看功能，不看日历"))
A.append(p(
    f"ACL 重建（ACLR）后重返运动率不理想、再伤风险高。{b('动作再训练')}越来越受重视：ACL 损伤会让{b('双侧')}下肢的动作质量都发生改变，动作功能障碍也是初次和再次 ACL 损伤的危险因素。"
))
A.append(p(
    f"问题在于，大家知道“为什么”要练动作，却不清楚“{b('怎么练、练什么、什么时候练')}”。比如开始跑步常按时间定在{b('术后约 12 周')}——但这个时间点和移植物愈合无关，患者跑不了就觉得“失败”，能跑就觉得“正常”，却很少评估功能。"
    f"另一个趋势是功能训练上得太早，患者准备不足，增加再伤、关节过载和代偿的风险。"
))
A.append(p(
    f"作者提出一个{hl('十项任务进阶体系')}：从正常走路一直到专项变向，每一项都有进入前需要满足的{b('力量和活动度标准')}，并配合四项监测，给患者结构感和自主性，也方便医疗团队沟通。"
))

A.append(h2("🔴 核心要点"))
A.append(table(
    ["环节", "要点"],
    [
        ["三种负荷", "峰值负荷（如地面反作用力峰值）· 总量负荷（负荷 × 次数）· 加载速率"],
        ["最佳负荷", "既保护移植物不过载，又给足刺激促进神经肌肉适应和移植物重塑"],
        ["髌股保护", "闭链训练中屈膝越深髌股压力越大，早期高负荷功能训练限制在屈膝 0°～80°"],
        ["四项监测", "运动后反应（疼痛、肿胀）· 动作质量 · 力量 · 肌肉酸痛"],
        ["十项任务", "走 → 双腿蹲 → 单腿蹲 → 双腿落地 → 跑台跑 → 双腿跳深 → 单腿减速 → 单腿跳深 → 90° 切步 → 专项反应性变向"],
    ],
))
A.append(p(f"{b('一句话概括')}：{red('每进一步都要过力量和活动度这一关，动作质量不达标就降级，疼痛肿胀加重就暂停')}。"))

A.append(h2("🟢 逐节深度解读"))

A.append(h3("❇️一、负荷管理"))
A.append(ul([
    f"负荷由神经肌肉系统吸收，也由肌腱、韧带、关节被动吸收；{b('力量不足')}时离心吸收能力差，就更多依赖被动结构",
    f"负荷在踝、膝、髋之间分配，取决于动作策略：{b('膝主导')}模式增加膝负荷，{b('回避膝')}的策略则减少膝负荷",
    f"Laughlin 等：女性 30 cm 单腿落地时 ACL 峰值负荷约 {b('0.7 倍体重（约 440 N）')}，远低于约 1300 N 的断裂阈值；但这只是矢状面，胫骨/股骨旋转等不良力学会让负荷更接近损伤阈值，因此{b('额状面和水平面控制')}是动作再训练的重点",
    f"ACLR 后髌股疼痛常见；弓步、腿举等闭链训练在接近完全屈膝时股四头肌力和髌股压力最大，早期高负荷功能训练建议限制在{b('屈膝 0°～80°')}",
]))

A.append(h3("❇️二、四项监测"))
A.append(table(
    ["监测", "问题", "做法"],
    [
        ["运动后反应", "关节受得了吗？", "训练应基本无痛；只有上次训练后疼痛（数字评分）和肿胀（推扫试验）都没有增加，才进入下一项。过载指标：髌骨处肿胀增加 >1 cm 或疼痛 +1 分"],
        ["动作质量", "任务是不是太难？", "用额状面三条线（躯干、骨盆、下肢）和矢状面（踝-膝、膝-髋）对线来教和监测（图1）；做不好就简化任务或减负荷（不加重量或加支撑）"],
        ["力量", "够不够强？", "伸膝力量是功能进阶的主要障碍；可用等速/等长测力、手持测力计、腿举 8RM 或 10RM、测力台等长深蹲评估"],
        ["肌肉酸痛", "负荷是否太大？", "迟发性肌肉酸痛反映肌肉负荷和恢复需求，酸痛明显时调整后续训练"],
    ],
))
A.append(pic(2, "图1：易教易用的动作分析模型。1a 额状面三条线——躯干稳定/对线（理想 <5°，不倾斜）、骨盆稳定/对线（理想 <5°，不下沉/上提）、下肢对线（无动态膝外翻）；1b 矢状面，视任务而定，看踝到膝、膝到髋的对线（理想约 90°）（图中英文标注已改为中文）"))
A.append(p(
    f"常见任务的地面反作用力：{b('双腿落地约 1～1.5 倍体重')}，{b('跑台跑 2～3 倍')}，{b('单腿增强式 2～6 倍')}。了解下肢产生和承受力量的能力，才能判断“什么时候”可以开始这些有风险的任务。"
))

A.append(h3("❇️三、十项任务逐一看"))
A.append(pic(3, "图2：ACL 重建术后的十项任务进阶——1 走路、2 双腿蹲、3 单腿蹲、4 双腿落地、5 跑台跑、6 双腿跳深、7 单腿减速、8 单腿跳深、9 90° 切步、10 专项变向（第 10 图背景横幅英文已去除）"))
A.append(h4("🔻任务 1：正常步态"))
A.append(ul([
    "术后通常 2～4 周不能完全负重或脱拐；异常步态与肌无力、功能差、满意度低和骨关节炎等并发症有关，回到跑步时还会加重",
    f"先恢复活动度：脱拐前要{b('完全伸膝并能控制')}；股四头肌抑制会妨碍力量恢复",
    f"直腿抬高时仍有{b('伸膝迟滞')}，若到{b('术后第 5 周')}还没消除，6 个月时更可能明显股四头肌无力",
    f"脱拐条件：完全主动伸膝、积液得到控制、无关节过载（肿胀增加 >1 cm 或疼痛 +1 分）、直腿抬高无伸膝迟滞",
]))
A.append(h4("🔻任务 2：双腿蹲"))
A.append(ul([
    "Neitzel 等：部分患者术后 12 个月深蹲时两腿负重仍不对称，并与功能差有关",
    "双腿蹲是三关节屈伸 + 躯干控制的基础动作，也是落地、跳跃、增强式训练的动作模式",
    f"进阶：徒手蹲、靠墙蹲、高脚杯蹲、后蹲、前蹲、过顶蹲，先不负重再逐步加重；早期控制在{b('屈膝 <90°')}；半月板修复等情况下可能要限制",
]))
A.append(h4("🔻任务 3：单腿蹲"))
A.append(ul([
    "最具功能性的基础动作，是所有单腿加速、减速、落地动作的基础",
    f"建议先能{b('单腿腿举约 100% 体重')}，才有足够力量承受单腿蹲",
    f"进阶：分腿蹲（前腿约承担 60% 体重）、后撤弓步、行进弓步、上台阶、单腿蹲；先在当前任务加负荷再进阶（如 80 kg 运动员分腿蹲加 20 kg，前腿约多承担 12 kg，相当于约 75% 体重）",
]))
A.append(h4("🔻任务 4：双腿落地"))
A.append(ul([
    f"第一个“离地”任务，地面反作用力约 {b('1.5～2 倍体重')}（每条腿约 1 倍，且加载速率高）",
    f"开始前建议腿举 8 次能达到{b('单腿 1 倍体重、双腿 2 倍体重')}",
    "训练所需速度下的离心控制，为单腿落地和跑步做准备；进阶：跳箱落地、原地跑后落地、跳起落地，可垂直、水平或旋转；泳池、沙地、蹦床或软垫可降低峰值力",
]))
A.append(h4("🔻任务 5：跑台跑"))
A.append(ul([
    f"跑步是重要里程碑，每一步承受约 {b('2～3 倍体重')}",
    "跑台上便于给视觉或视频反馈，改善跑姿；可分析步长、触地时间和力吸收",
    f"慢速（{b('8 km/h')}）跑姿正常是进阶到单腿减速和落地训练的前提；{red('跑台上的力学恢复后，才能到户外跑或做敏捷训练')}；接近最大冲刺速度下无痛、对称是后期目标",
    "注意：许多功能指标在术后第一年内都不会完全恢复正常",
]))
A.append(h4("🔻任务 6：双腿增强式（双腿跳深）"))
A.append(ul([
    "牵张-缩短循环训练，发展爆发速度、力量和功率，优于传统抗阻训练；也能提高关节觉察和本体感觉",
    f"冲击力约 {b('2～6 倍体重')}；高强度增强式会造成肌肉损伤和关节过载",
    f"双腿跳深中控制{b('动态膝外翻')}与 ACL 损伤/再伤风险有关；青少年跳深时膝外展力矩高，精英成年运动员没有，说明技术很关键",
]))
A.append(h4("🔻任务 7：单腿落地/减速"))
A.append(ul([
    f"ACL 损伤多发生在减速和落地中，这类动作危险，心理上也有挑战；单腿负荷约 {b('2～3 倍体重')}",
    f"开始前建议：伸膝力量与健侧差距在 {b('20% 以内（LSI ≥80%）')}；单腿腿举能推 {b('1.5 倍体重')}（离心 2 倍）",
    f"先在吸能表面（垫子、蹦床、沙地）练，台阶高度 {b('20 → 30 → 40 cm')} 或逐步加速度，再过渡到跑动中的自然减速；目标是直线跑后单腿减速控制和力学良好",
]))
A.append(h4("🔻任务 8：单腿增强式（单腿跳深）"))
A.append(ul([
    "变向类动作就是单腿增强式的性质；从单平面进阶到多平面",
    f"冲击力 {b('2～6 倍体重')}，离心成分会带来明显肌肉酸痛，需仔细监测；单腿跳深动作质量和力吸收良好后，才进阶到旋转增强式或变向",
]))
A.append(h4("🔻任务 9：90° 切步"))
A.append(ul([
    "恢复高负荷运动任务中的对称性可能降低再伤风险；多方向和高速度会增加膝负荷",
    f"精英手球运动员侧切时膝外展负荷是跳深时的 {b('5 倍')}",
    "从简单动作、小角度开始；先慢速分解（两个动作间稍停），用一两步进入，低速学会技术后再逐步提高助跑速度",
    "90° 切步控制良好后，才进入专项（反应性、对抗、技术）训练",
]))
A.append(h4("🔻任务 10：专项反应性变向"))
A.append(ul([
    "逐步过渡到更高速度、反应性多方向任务，再到视觉-运动要求更高（选择更多）的专项任务",
    f"{b('反应性动作比预先计划的动作更挑战动作质量、膝负荷更大')}：先在预设任务中动作安全，再练反应性动作，重返运动前确认反应性动作也安全",
    f"ACL 损伤常发生在复杂刺激、注意力在外部时；{b('外部注意焦点')}训练的保持效果更好；从有意识控制、少干扰过渡到混乱、反应性的比赛情境",
    "对抗项目还要加入扰动/接触训练（图3）",
]))
A.append(pic(4, "图3：场上扰动训练，为重返赛场的身体接触做准备——运动员在受到瑞士球或球员间接触时，仍要保持良好控制、力学和控球（背景横幅英文已去除）", "66%"))

A.append(tcap("表1　ACL 重建术后十项任务进阶：任务、训练类别，以及可无限制练习所需的力量和膝活动度"))
A.append(table(
    ["序号", "任务类别", "训练/目标动作", "所需力量", "所需膝活动度"],
    [
        ["1", "走路", "无跛行、无辅助行走（如脱拐）", "股四头肌募集良好", "完全伸膝"],
        ["2", "双腿基础动作", "双腿蹲到 90°，两腿负重不对称 <20%", "单腿腿举 50% 体重", "完全伸膝/屈曲 >90°"],
        ["3", "单腿基础动作", "单腿蹲到 90°", "单腿腿举 80% 体重", "屈曲 >120°"],
        ["4", "双腿落地", "次最大跳后的双腿落地控制", "单腿腿举 100% 体重和/或双腿腿举/深蹲 150% 体重", "屈曲 >130°"],
        ["5", "跑步", "跑台 8 km/h", "单腿腿举/深蹲 125% 体重和/或等长伸膝 LSI >70%", "屈曲 >130°"],
        ["6", "双腿增强式", "30 cm 双腿跳深", "伸膝 LSI >80%，且单腿腿举/深蹲 125% 体重或 200% 体重", "完全"],
        ["7", "单腿跳/落地", "向前和侧向跑动中的单腿减速", "等速伸膝 LSI >80% 和/或单腿腿举/深蹲 150% 体重", "完全"],
        ["8", "单腿增强式", "单腿跳深", "同上", "完全"],
        ["9", "预设的多方向动作", "90° 切步", "同上", "完全"],
        ["10", "专项动作", "45° 反应性变向", "等速伸膝 LSI >90% 和/或单腿腿举/深蹲 200% 体重", "完全"],
    ],
))
A.append(small("力量用等长或等速伸膝、腿举和/或深蹲测试；深蹲力量指测力台和等长测试架上测得的力占体重的百分比，而不是自由重量深蹲额外加的重量。LSI：肢体对称指数。"))

A.append(h2("🧭 证据评价"))
A.append(ul([
    f"{b('性质')}：临床评论，由理论、现有证据和作者大量实践经验整合而成；没有验证这套进阶能否降低再伤或提高重返率",
    f"{b('亮点')}：把“什么时候做什么”量化成力量和活动度门槛，配合疼痛、肿胀、动作质量、酸痛四项监测，便于团队沟通和患者自我管理，也可能推广到其他下肢重伤",
    f"{b('门槛多为经验值')}：腿举倍数、LSI 等阈值大多是作者建议，缺少直接验证；部分评估（如测力台等长深蹲）需要设备",
    f"{b('前后数值不一致')}：单腿减速前的力量，正文写“单腿腿举 1.5 倍体重（离心 2 倍）”，与表 1 一致，但正文双腿落地要求“单腿 1 倍、双腿 2 倍体重”，表 1 写“单腿 100% 和/或双腿 150%”；双腿落地的地面反作用力一处写 1～1.5 倍，一处写 1.5～2 倍；单腿蹲正文要求腿举约 100% 体重，表 1 写 80%",
    f"{b('小瑕疵')}：文章类型拼成 “CLINICAL COMMENTRY”；“cannot not fully weight bear”多一个 not；表 1 任务 6 的“125% 或 200%”含义不清",
]))

A.append(h2("📌 总结：ACL 重建术后十项任务"))
A.append(p(
    f"{red('① 走路')}：完全伸膝、无伸膝迟滞、肿痛不加重才脱拐<br>"
    f"{red('② 双腿蹲 → ③ 单腿蹲')}：腿举 50% → 80%～100% 体重，屈膝先控制在 90° 内<br>"
    f"{red('④ 双腿落地 → ⑤ 跑台跑')}：腿举 100%～125% 体重或伸膝 LSI >70%，屈曲 >130°，先慢速 8 km/h<br>"
    f"{red('⑥ 双腿跳深 → ⑦ 单腿减速 → ⑧ 单腿跳深')}：伸膝 LSI >80%、单腿腿举 125%～150% 体重，先软表面低高度<br>"
    f"{red('⑨ 90° 切步 → ⑩ 反应性变向')}：先预设后反应，最后 LSI >90%、单腿腿举 200% 体重<br>"
    f"{red("★ 贯穿始终")}：疼痛肿胀不加重、动作质量过关、肌肉酸痛可恢复，才往下走"
))
A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Buckthorpe M, Tamisari A, Della Villa F. A Ten Task-Based Progression in Rehabilitation after ACL Reconstruction: From Post-Surgery to Return to Play – "
    "A Clinical Commentary. Int J Sports Phys Ther. 2020;15(4):611-623. PMCID: PMC7735691.</em><br>"
    "文中图片均来自原文：图 1 英文标注已改为中文，图 2、图 3 背景横幅英文已去除；表 1 已译为中文，仅用于学术交流。"
))

TITLE = "「膝关节」ACL 重建术后什么时候能跑能跳？十项任务进阶"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>ACL十项任务推文</title>
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
