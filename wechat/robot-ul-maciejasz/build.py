#!/usr/bin/env python3
"""上肢康复机器人综述（Maciejasz 等 2014）推文。

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


import json, os


def table1():
    rows = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 't1_zh.json')))
    head = ['系统名称及文献', '自由度', '支持的运动', '主要控制输入', '驱动器', '类型；应用领域', '开发阶段；补充信息']
    th = ''.join(f'<th style="border:1px solid #d9d9d9;background-color:#f2f2f2;padding:4px 3px;font-size:11px;line-height:1.4;color:#000;text-align:center;font-weight:bold;">{h}</th>' for h in head)
    body, cur = '', None
    for r in rows:
        if r['sect'] != cur:
            cur = r['sect']
            body += f'<tr><td colspan="7" style="border:1px solid #d9d9d9;background-color:#e1f0f3;padding:4px 5px;font-size:11.5px;font-weight:bold;color:#006e82;">{cur}</td></tr>'
        tds = ''.join(f'<td style="border:1px solid #d9d9d9;padding:4px 3px;font-size:10.5px;line-height:1.45;color:{TEXT};vertical-align:top;">'
                      f'{"<em>" + c + "</em>" if i == 0 else c}</td>' for i, c in enumerate(r['c']))
        body += f'<tr>{tds}</tr>'
    return f'<table style="width:100%;border-collapse:collapse;margin:0 0 18px;"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


A = []
A.append(img(1))
A.append(cap("原文信息（编者中文重排）"))

A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Maciejasz P, Eschweiler J, Gerlach-Hahn K, Jansen-Troy A, Leonhardt S. A survey on robotic devices for upper limb rehabilitation. J Neuroeng Rehabil. 2014;11:3. doi:10.1186/1743-0003-11-3",
    "作者来自德国亚琛工业大学医学工程和医学信息技术研究所",
    f"文章类型：{b('技术综述')}，汇总了 120 多个上肢康复机器人系统（含研发中的），偏工程视角",
], square=True))

A.append(h2("先说为什么要关注康复机器人"))
A.append(p(
    f"神经系统疾病后的上肢康复，效果很大程度取决于{b('开始时间、训练时长、强度和任务导向')}，以及患者的注意力和努力程度。"
    f"大量重复的协调动作训练对治疗师来说负担很重，而住院康复时间越来越短、老龄化又让需求越来越大。"
))
A.append(p(
    f"机器人能不知疲倦地做重复训练，但现实是：文献里描述的设备很多，{red('真正进入临床的很少')}，进了临床的效果也没有预期那么好。"
    f"这篇综述的价值在于{mk('把各种技术方案摆在一起比较')}：应用领域、目标人群、辅助类型、机械结构、驱动、控制和临床证据。"
))

A.append(h2("重点一：机器人怎么分类"))
A.append(pic(5, "上肢康复机器人的分类（编者根据原文表 2～6 整理）"))
A.append(h3("按用途：日常辅助还是训练治疗"))
A.append(ul([
    f"{b('日常生活辅助')}（助力、震颤抑制）：需求大但设备很少，因为必须轻、便携、安全、便宜，而多关节助力就要多个驱动器，又重又耗电；例如 PowerGrip 抓握辅助、WOTAS 震颤抑制矫形器",
    f"{b('训练治疗')}：绝大多数设备属于这类，多数只能在康复机构由专业人员操作，价格让个人难以承受",
    f"有研究发现，{red('上机准备超过 5 分钟，很多治疗师就不愿再用')}，所以设备要直观、上机快、价格合理",
    "目标人群几乎都是卒中患者；脑外伤、脊髓损伤、多发性硬化、脑瘫、特发性震颤等研究很少",
]))
A.append(h3("按辅助类型"))
A.append(table(["术语", "说明"], [
    ["主动设备", "能带动肢体运动，需要主动驱动器，重量可能增加；也适用于完全不能动的患者"],
    ["被动设备", "不能带动肢体，但在动作方向错误时可施加阻力；只适用于能自己活动肢体的患者；除制动器外没有驱动器，通常比主动设备轻"],
    ["触觉设备", "通过触觉与使用者交互，多数提供一定阻力，常有振动等其他感觉，有时也能产生特定动作，但力通常较小；常与虚拟环境一起用于康复"],
    ["指导设备", "既不辅助也不阻碍动作，但能追踪动作并对表现给予反馈；与触觉设备一样常配虚拟环境"],
    ["主动训练", "患者主动活动肢体，设备可给予一定辅助；上面任何一类设备都能做"],
    ["被动训练", "患者保持被动，由设备带动肢体；需要主动设备，持续被动活动训练就是一例"],
]))
A.append(tcap("原文表 2：辅助类型相关术语（中文翻译）"))
A.append(p(f"注意：{b('主动设备也能做被动训练')}，比如持续被动活动设备本身是主动的，但患者不用力，所以训练是被动的。被动和无驱动设备更简单、安全、便宜，更适合康复后期，而不是早期严重运动障碍的训练。"))

A.append(h3("按机械结构"))
A.append(pic(2, "原文图 1：几种典型结构"))
A.append(table(["术语", "说明"], [
    ["末端执行器式设备", "只在肢体最远端接触患者，结构简单；但当可能的自由度多时，难以控制肢体位置"],
    ["外骨骼式设备", "机械结构与肢体骨骼对应，肢体每一节都连在设备相应的一节上；能独立、同时、精确地控制多个关节，但比末端执行器式复杂；限制或辅助一个或多个关节运动的矫形器也可算作外骨骼式"],
    ["平面机器人", "通常为末端执行器式，只在某个平面内运动；能降低成本，但可训练的动作范围也变小；末端在平面内运动时，肢体关节仍可在三维空间中运动"],
    ["反向驱动性", "设备处于被动状态时，患者也能推动设备；不束缚肢体、让肢体保持舒适姿势，提高安全性"],
    ["模块化", "可加装可选部件，以适应特定病情或做更多训练"],
    ["可重构性", "不加部件就能改变机械结构，以适应患者病情或做其他形式的训练"],
]))
A.append(tcap("原文表 3：机械结构相关术语（中文翻译）"))
A.append(ul([
    f"{b('末端执行器式')}（如 InMotion ARM / MIT Manus、NeReBot）：结构和控制简单，但末端最多 6 个运动方向，关节一多，手臂会出现多种可能姿势，{red('有受伤风险')}",
    f"{b('外骨骼式')}（如 ArmeoPower）：能同时独立控制多个关节，但{b('每段杆长都要按患者调')}，上机耗时；肩关节旋转中心会随动作移动，需要特殊机构保证安全",
    f"{b('混合式')}：ArmeoSpring 只有肘、前臂、腕是外骨骼，肩不受约束，适配快；也有用两台机器人模拟治疗师双手的",
    f"工业机器人便宜，但{b('阻抗远高于人的上肢')}，不宜与患者紧密接触；康复机器人多设计成低阻抗、可反向驱动",
    f"{b('平面机器人')}降低成本，选好工作平面就能满足多数训练；可重构设备（如 UHD 只有 2 个自由度却能换三种构型）能降低成本，但目前很少",
]))
A.append(pic(3, "原文图 2：上肢主要运动方向"))

A.append(h3("按驱动方式"))
A.append(table(["术语", "说明"], [
    ["电动驱动器", "用电流驱动；最常见，容易提供较大功率并储能；商用选择多，但有些较重或阻抗太高，不适合康复"],
    ["液压驱动器", "用液压（通常是油）驱动，能产生大的力；系统较复杂，需保持油压并防漏；商用液压驱动器也重，所以康复机器人只用专门设计的"],
    ["气动驱动器", "用压缩空气驱动，阻抗更低、比电动轻；需要专门的压缩机或压缩空气罐"],
    ["气动人工肌肉（McKibben 型）", "内胆外包编织网套，充气时像肌肉一样缩短；较轻，只能单向出力；动态响应慢且非线性，难控制"],
    ["串联弹性驱动器", "在驱动器后串联弹性元件；康复机器人中较常见，能降低惯量和固有阻抗，力控更准更稳，更安全"],
    ["功能性电刺激", "用电流兴奋神经，使其支配的肌肉收缩，用身体自己的“驱动器”产生动作；但难以做到精确、可重复的动作，还可能让患者疼痛"],
]))
A.append(tcap("原文表 4：驱动方式相关术语（中文翻译）"))
A.append(ul([
    "被动设备需要可调阻力：磁粉制动器（ARM Guide）、磁流变液 / 电流变液制动器（PLEMO 等），后者响应快、可重复",
    f"功能性电刺激能让肌肉真正收缩、维持肌容积，但会引起强烈不自主收缩、可能疼痛，且受疲劳和电极接触影响，{b('难以精确控制')}",
    "驱动器放在关节旁边，传动简单但远端重；放在近端减轻远端重量，但传动机构有摩擦、更难控制",
]))

A.append(h3("控制信号和反馈"))
A.append(table(["术语", "说明"], [
    ["动力学信号", "受试者作用于设备各关节（外骨骼式）或末端（末端执行器式）的力或力矩"],
    ["运动学信号", "设备或肢体各节段、关节的位置、方向、速度和加速度"],
    ["触发信号", "启动某个动作的信号；简单的用开关或按钮，复杂的设定某个信号的阈值（如对应一定肌肉收缩程度的表面肌电值）"],
]))
A.append(tcap("原文表 5：控制输入信号相关术语（中文翻译）"))
A.append(ul([
    f"{b('表面肌电控制')}能读出“想动”的意图，多用于肘关节（肱二头肌、肱三头肌信号好测）；最成功的是 MIT 的单自由度便携肘矫形器，后来商品化为 Myomo",
    f"{b('用健侧控制患侧')}：Bi-Manu-Track、ARMOR 等让健手带动患手，适合偏瘫",
    f"{b('反馈')}：视觉、触觉、听觉、电刺激；{mk('虚拟现实')}让训练更有趣、可快速切换任务、提高注意力和动机",
]))

A.append(h3("控制策略"))
A.append(table(["术语", "说明"], [
    ["“高层”控制策略", "专门为诱导运动可塑性而设计的控制算法"],
    ["辅助型控制", "设备提供物理辅助，帮助患者完成想做的动作"],
    ["挑战型控制", "设备给患者增加难度，挑战其完成动作"],
    ["触觉刺激", "把机器人当作触觉接口，在虚拟现实环境中完成活动"],
    ["指导型控制", "既不辅助也不阻碍，只量化表现并给予视觉、听觉等反馈"],
    ["“底层”控制策略", "通过控制力、位置、阻抗或导纳来实现“高层”策略"],
    ["导纳控制", "测量使用者施加的力，设备产生相应位移"],
    ["阻抗控制", "测量肢体运动，机器人给出相应的力反馈"],
]))
A.append(tcap("原文表 6：控制策略相关术语（中文翻译，多数参照 Marchal-Crespo 和 Reinkensmeyer）"))
A.append(ul([
    f"{b('辅助型')}：阻抗式（偏离轨迹才给回正力）、减重式、肌电式（触发或按比例辅助）、按表现自适应；{red('触发式容易让患者“偷懒”')}，只用刚好能触发的力",
    f"{b('挑战型')}：阻力训练、{mk('放大误差')}（误差越大学得越快）、约束诱导（限制健侧，逼患侧用）",
    f"{b('底层')}：阻抗控制交互稳定但自由空间精度差；导纳控制精度高但动态交互可能不稳，可用串联弹性驱动器解决",
]))

A.append(h2("重点二：临床证据怎么说"))
A.append(table(["类别", "说明"], [
    ["0 类", "初步可行性研究：少量健康志愿者，常用原型机，评估安全性和临床可行性"],
    ["Ⅰ类", "试点（概念考量）研究：小样本目标疾病患者，测试安全性、可行性和潜在获益；无对照组或以健康人为对照"],
    ["Ⅱ类", "概念发展研究：验证设备疗效；干预描述标准化，有对照组、随机分组和盲法评估"],
    ["Ⅲ/Ⅳ类", "概念展示 / 验证研究：进一步评估疗效；与Ⅱ类相似，但通常是多中心、大样本"],
]))
A.append(tcap("原文表 7：本文对康复机器人临床试验的分类（基于 Lo 的指南，补充了 0 类）"))
A.append(pic(4, "原文图 3：临床研究数量和入组人数"))
A.append(ul([
    f"检索 clinicaltrials.gov 得到 197 项试验，62 项相关，排除 4 项后剩 58 项：31 项验证设备，27 项探索更好的治疗方式；{b('54 项只纳入卒中')}",
    f"近三年“改进治疗方法”类研究的入组人数明显增加，说明重心正从“设备能不能用”转向“{mk('怎么用最好')}”",
    f"系统综述：机器人训练能改善卒中后{b('运动损伤和肌力')}，但{red('不能改善日常生活能力')}",
    f"首个大型多中心随机试验（MIT-Manus）：机器人训练与{b('同等强度的治疗师训练效果没有差别')}，总费用也相近",
    f"所以机器人最大的优势是{b('提供大剂量重复训练而不累垮治疗师')}，再加上游戏化的动机和量化反馈",
]))
A.append(h3("作者总结的训练原则"))
A.append(ul([
    "目标不只是最大化重复次数，还要最大化患者的注意力和努力",
    "单调重复不如变换任务，技能保持更好",
    "自适应、按需辅助优于固定模式；但自适应算法若让患者偷懒，反而可能拖慢恢复",
    "学习靠误差驱动，适当放大误差可能进步更快；内隐学习效果可能更大",
    f"很多功能改善{b('更依赖腕和手')}，而不是肩肘的活动度",
    f"关键不是最大肌力，而是{b('主动肌和拮抗肌的时机协调')}",
]))

A.append(h2("这些内容能信几分"))
A.append(ul([
    f"{b('这是技术综述，不是疗效综述')}：重点在设备怎么设计，临床结论主要转引其他系统综述",
    f"{b('表格中大量设备只有健康人或个案研究')}，130 个条目里商用系统只有十几个，Ⅱ类以上研究很少",
    f"{b('时效性')}：检索截至 2013 年，之后出现了很多新设备和更大的试验，读的时候要注意",
    f"{b('非系统检索')}：作者也承认肯定有遗漏，选择标准（排除纯机械装置、等速设备等）有一定主观性",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('同一设备两种描述')}：正文说 Umemura 的系统是轮椅安装的外骨骼，表 1 却写成固定式末端执行器式系统",
    f"{b('设备名称不一致')}：正文把手指触觉设备叫 HAFI，表 1 中对应条目叫 HIFE",
    f"{b('运动描述不对')}：正文说 UHD 可以训练“前臂屈伸和腕”，前臂只有旋前旋后，表 1 写的也是前臂旋前旋后",
    f"{b("“批准”与“许可”混用")}：正文说 Myomo 获得了 FDA“批准”，表 1 写的是 FDA“许可”（clearance），这是两种不同的上市路径",
    f"{b('缩写未定义')}：表 1 中 Bi-Manu-Track 的研究对象写成“sA”，图例里只有“aS”（急性卒中）",
    f"{b('引用编号不一致')}：正文介绍 iPAM 引用 [126]，表 1 写的是 [67]",
    f"{b('小错')}：表 6 把 coaching 写成 couching；图 3 纵轴“subjects”拼成“subjets”；“horizontal”拼成“horizonatal”；“clinical trial”写成“clinical train”",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"{mk('机器人是工具，不是疗法本身')}：与同等强度的人工训练效果相近，价值在于帮治疗师“放大”训练剂量",
    f"{b('选设备看病人')}：完全不能动用主动设备；能部分活动用被动 / 触觉设备；后期用指导型配虚拟现实",
    f"{b('设计训练时防偷懒')}：触发式辅助和自适应算法都可能让患者少用力，要监控主动参与",
    f"{b('别只练肩肘')}：功能改善更多依赖腕和手，训练重点放在协调而不是单纯肌力",
    f"{b('上机时间很关键')}：超过 5 分钟就可能用不下去，引进设备时要算上这部分成本",
]))

A.append(h2("附录：原文表 1（上肢康复机器人设备一览）"))
A.append(p("自由度一栏：[ ] 表示被动（只提供阻力），{ } 表示无驱动；“*”表示设备运动方向不对应单一解剖运动，而是多种运动的组合。研究类别见原文表 7；括号中的数字为使用该系统治疗的人数。设备名称保留原文。", "font-size:13px;color:#888;"))
A.append(table1())
A.append(tcap("原文表 1：上肢康复机器人设备（中文翻译，按辅助的关节分组）"))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Maciejasz P, Eschweiler J, Gerlach-Hahn K, Jansen-Troy A, Leonhardt S. A survey on robotic devices for upper limb rehabilitation. J Neuroeng Rehabil. 2014;11:3. doi:10.1186/1743-0003-11-3</em><br>"
    "原文采用 CC BY 2.0 开放许可（© 2014 Maciejasz et al.），允许在注明出处的前提下使用。原文图 1C（NeReBot）版权属 IEEE（©2007，经许可转载），图 1D 由 Hocoma AG 提供，不在 CC 许可范围内。本文为中文解读：图 1、2 引自原文（加中文图注 / 图例），图 3 按原图重绘，表 1～7 为中文翻译，分类卡为编者整理。"
))

TITLE = "「康复工程」上肢康复机器人怎么选？130 种设备的结构、驱动、控制与证据"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>上肢康复机器人推文</title>
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
