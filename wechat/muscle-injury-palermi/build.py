#!/usr/bin/env python3
"""下肢间接结构性肌肉损伤康复综述推文：生成 article_body.html 与 preview.html。

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
    return p(b(t), "margin:18px 0 6px;font-size:14px;")


def mk(t):
    """黄底高亮"""
    return f'<span style="background:#fff3a3;padding:0 2px;font-weight:bold;">{t}</span>'


A = []
A.append(img(1))
A.append(cap("原文标题（J Funct Morphol Kinesiol 2021;6:75，开放获取）"))

A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Palermi S, Massa B, Vecchiato M, Mazza F, De Blasiis P, Romano AM, Di Salvatore MG, Della Valle E, Tarantino D, Ruosi C, Sirico F. Indirect Structural Muscle Injuries of Lower Limb: Rehabilitation and Therapeutic Exercise. J Funct Morphol Kinesiol. 2021;6(3):75.",
    "作者主要来自意大利那不勒斯费德里科二世大学公共卫生系",
    "叙述性综述；DOI：10.3390/jfmk6030075",
], square=True))

A.append(h2("拉伤之后，别再“等它自己好”"))
A.append(p(
    f"肌肉损伤是团队和个人项目里{b('最常见的运动损伤')}，在足球里占了所有伤病的一半。下肢最容易伤的四组肌肉依次是："
    f"{red('腘绳肌 ＞ 内收肌 ＞ 股直肌 ＞ 小腿三头肌')}。"
))
A.append(p(
    "可现实是，很多业余运动员的康复是“医院有什么就做什么”，而不是按证据来。作者也说得很直白："
    f"{mk('“观望等待”的做法已经被证明无效')}；各种理疗仪器越用越多，但到底哪个真有用，证据并不一致。"
))
A.append(p(
    f"这篇综述按意大利肌肉韧带肌腱学会（ISMuLT）和意大利共识会议的建议，把{b('间接结构性肌肉损伤')}（俗称“拉伤”“肌肉撕裂”）的保守康复整理成{b('0 期 + 三期')}，"
    "每期写清楚目标、谁来管、在哪练、做什么、什么时候进下一期，最后给了四组肌肉的具体动作和回归测试。"
))

A.append(h2("先分清是哪种拉伤"))
A.append(p("按 ISMuLT 分类，“间接”指不是被撞的，而是在用力收缩时被突然拉长超过极限造成的；“结构性”指肌肉组织真的有了损伤。"))
A.append(tcap("表 1　间接结构性肌肉损伤分类"))
A.append(table(
    ["严重程度", "部位", "组织", "复发"],
    [
        ["3A：轻度部分撕裂", "P：近端", "MF：肌筋膜", "R0：首次损伤"],
        ["3B：中度部分撕裂", "M：中段", "MT：肌腹和肌腱连接处", "R1：第一次复发"],
        ["4：次全或完全撕裂、肌腱撕脱", "D：远端", "T：中央肌腱或游离肌腱", "R2：第二次复发"],
        ["", "", "", "R3：第三次复发"],
    ],
))
A.append(ul([
    f"{red('近端')}的腘绳肌和股四头肌损伤、{red('远端')}的小腿损伤预后更差；{red('肌腱连接处')}的损伤恢复更慢",
    f"3A、3B 最常见，也是保守康复争议最大的；{b('4 型一般考虑手术')}",
    f"影像首选{b('超声')}：快、便宜、能反复看。核磁只在超声和临床不一致、或精英运动员时用；核磁信号恢复比功能恢复慢，{b('不能拿来决定回归')}",
]))

A.append(h2("核心：三期康复"))
A.append(pic(2, "三期康复总览（按原文内容自绘）"))
A.append(p(
    f"整个方案最重要的一条主线是：{mk('一期等长 → 二期向心 → 三期离心')}，收缩方式要跟组织愈合的阶段对得上。"
    f"另一条原则是：{red('进阶看标准，不看天数')}——每期多长，取决于临床检查、功能和超声，而不是“伤后第几周”。"
))

A.append(h3("0 期：伤后 0～72 小时"))
A.append(ul([
    f"{b('伤后 36～48 小时')}做超声最合适：血肿 24 小时达到最多，48 小时后开始减少",
    f"按 {b('PRICE')}（保护、休息、冰敷、加压、抬高）处理，现在更推荐 {b('POLICE')}，把“休息”换成“适当负荷”",
    f"{mk('冷敷加压：每次 15～20 分钟，间隔 30～60 分钟，共做 6 小时')}，加压 40～50 mmHg",
    f"短暂制动或相对制动，但{b('只限前 3～5 天')}；一般不需要拐杖，贴扎可以帮助固定和引流",
    f"{red('72 小时内不做任何产热的理疗')}，以免加重出血",
    "24 小时后可以做淋巴引流按摩，把加压绷带换成弹力绷带；脉冲超声、低能量激光的证据很少",
]))

A.append(h3("一期：破坏期（等长）"))
A.append(p(f"目标：处理诱发因素和拮抗肌；日常活动不痛；患肌能无痛地做到理论最大负荷的 {b('50%')}；延展性恢复到 {b('90%')}。地点在健身房，由医生和治疗师负责。"))
A.append(ul([
    f"伤后头 5～7 天瘢痕还很松，{red('最大风险是用力收缩把裂隙拉大')}",
    f"所以只做{b('等长收缩')}：肌丝不滑动、肌肉长度不变。{mk('30～50 次，每次 10～20 秒，全程在疼痛阈值以下')}",
    f"关节角度要{b('从肌肉产生力矩小的位置开始')}，再慢慢往力矩大的角度推进",
    "做无痛的延展性练习（被动、主动辅助、静态或动态），最好用功能性模式；双关节肌两端都要拉",
    f"{red('不要做深层按摩')}；积液没消就继续弹力绷带；血肿大的话在机化前超声引导下抽吸",
    "尽早用没受伤的部位做有氧，比如上肢有氧；每次练完冰按摩 15～20 分钟",
    f"电刺激（TENS、神经肌肉电刺激）从伤后头几天一直用到第 3 周左右；激光证据尚可；扑热息痛可以止痛，{red('不推荐非甾体抗炎药')}；PRP、干细胞、肌松药证据不足",
    f"{b('红灯')}：做力量练习或跑步机慢跑时痛",
]))

A.append(h3("二期：修复 / 再生期（向心）"))
A.append(p(
    f"{b('进入标准')}：肿胀消退；{mk('最大等长收缩不痛')}；主动和被动牵伸到末端不痛；关节活动度完整；超声上裂隙消失、瘢痕区有肉芽修复组织。"
))
A.append(ul([
    f"开始{b('向心收缩')}：肌肉缩短时瘢痕区不受牵拉。动作要{b('慢、可控')}，先徒手抗阻、再用器械，{red('不超过 60% 1RM')}",
    f"{red('离心部分尽量减到最小')}",
    "继续延展性练习；开始本体感觉训练（稳定或不稳定平面、加干扰、加认知任务）和核心稳定训练",
    f"有氧按顺序加：{b('功率车 → 椭圆机 → 减重跑台 → 跑步机')}",
    "这时可以开始按摩",
    f"目标：练习时不痛、没有“异样感”；延展性完全恢复；专项有氧指标恢复；体重回到伤前。{b('红灯')}：延展性测试仍阳性",
]))

A.append(h3("三期：重塑期（离心）"))
A.append(p(
    f"{b('进入标准')}：逐渐加量的抗阻向心收缩不痛；{mk('次最大离心收缩不痛')}；超声上裂隙基本消失。这一期可能要 {b('60 天以上')}。"
))
A.append(ul([
    f"以{b('离心收缩')}为主，强度逐步增加，可以用弹力带；要针对具体肌肉和部位，也要考虑受伤时的动作",
    "可加入等速、惯性（飞轮）训练",
    f"拉伸逐渐加入，{b('从 10～15 秒延长到 1 分钟')}，不能引起疼痛",
    f"{mk('患肌力量至少恢复到伤前或对侧的 70%，才加大跑量')}，最好有 GPS 监控",
    "专项动作放在这一期的最后，小心加入",
    f"{b('红灯')}：训练中或训练后肌肉有“不一样”的感觉",
]))

A.append(h2("四组肌肉的具体动作"))
A.append(p(f"原文给了四组肌肉的示范动作，同样遵循{b('等长 → 动态 → 本体感觉与拉伸 → 预防')}的顺序。"))
A.append(pic(3, "原文表 2　腘绳肌（一）"))
A.append(ul([
    f"{b('等长')}：坐位，用弹力带或治疗床做屈膝等长。近端损伤时小腿往后收的角度小，中远端损伤时膝更伸直；再在不同角度做等长",
    f"{b('动态')}：伸展者（仰卧抱住大腿，主动伸膝）、滑行者（手拉悬吊带，一腿向后滑）、{red('北欧挺')}",
]))
A.append(pic(4, "原文表 2　腘绳肌（二）"))
A.append(ul([
    "本体感觉：单腿站立，另一腿前后摆动（钟摆）",
    "拉伸：治疗师辅助直腿抬高",
    f"{b('二级预防')}：离心屈膝拉伸、离心伸髋拉伸",
]))
A.append(pic(5, "原文表 3　股直肌"))
A.append(ul([
    f"{b('等长和动态')}都分两种：近端损伤时仰卧、髋伸直位练伸膝；中远端损伤时坐位练",
    f"{b('二级预防')}：跪姿，躯干后仰，对股直肌做离心屈髋、伸膝拉伸",
]))
A.append(pic(6, "原文表 4　内收肌"))
A.append(ul([
    f"{b('等长')}：仰卧、站立或俯卧夹球",
    f"{b('动态')}：徒手抗阻内收、弹力带内收",
    "本体感觉：半球上单腿站加抛接球",
    f"{b('二级预防')}：离心侧弓步拉伸、{mk('哥本哈根内收肌训练')}",
]))
A.append(pic(7, "原文表 5　小腿三头肌"))
A.append(ul([
    f"{b('等长')}：俯卧屈膝和伸膝位，徒手抗阻跖屈（屈膝时更偏比目鱼肌）",
    f"{b('动态')}：徒手抗阻向心/离心，然后过渡到{b('提踵')}",
    "本体感觉：弓步位的平衡练习",
]))

A.append(h2("什么时候能回去训练、比赛"))
A.append(p("回归训练（RTT）的一般标准："))
A.append(ul([
    "没有症状，触诊不痛",
    f"{b('被动和主动牵伸都不痛')}；{b('等长、向心、离心收缩都不痛')}",
    "完成规定的康复方案；参考超声和核磁；也要听运动员自己的感受",
]))
A.append(p(
    f"回归比赛（RTP）前，建议{mk('至少一周、4 次以上正常训练，没有疼痛、不适或害怕')}，"
    f"同时用 GPS 和心率监控：{red('与伤前数据相差超过 10%，就推迟回归')}；最大摄氧量最好恢复到伤前的 {b('90%')} 以上。"
))
A.append(tcap("表 6　各肌群的回归测试"))
A.append(table(
    ["肌群", "专项检查", "实验室测试", "场地测试"],
    [
        ["腘绳肌", "被动直腿抬高；动态柔韧性 H 测试", "测力（等长、等张、等速）", "伊利诺伊敏捷测试；急停测试；倒退跑"],
        ["股四头肌", "被动股四头肌牵伸测试", "测力；同步测力板测试", "伊利诺伊敏捷测试；急停测试；踢球测试"],
        ["内收肌", "耻骨应力测试；抗阻内收测试；挤压测试；被动牵伸测试", "内收肌测力", "踢球测试；交叉步（卡里奥卡）测试"],
        ["小腿三头肌", "提踵测试；踝关节柔韧性测试", "测力；同步测力板测试；跳深测试", "伊利诺伊敏捷测试"],
    ],
))
A.append(p("具体怎么测，原文没有展开，需要查对应的参考文献。"))

A.append(h2("这篇的局限"))
A.append(ul([
    f"{b('叙述性综述')}，没有检索策略和质量评价，主要依据意大利的分类和共识，很多推荐本身是专家意见",
    f"作者自己也承认，{red('PRICE 没有高质量随机对照试验支持')}，大部分理疗（超声、激光、热疗、冲击波等）证据都很弱",
    "“一期等长、二期向心、三期离心”是原则，不是试验验证过的最优方案；作者也提到有人主张更早引入离心，比如腘绳肌的 L-protocol",
    "动作表只有名称和照片，没有组数、次数、负荷和进阶参数；回归测试也只列了名字",
    "部分数字缺少出处或依据：比如“一期延展性恢复 90%”“RTP 数据差距 10% 是人为设定”；电刺激能促进干细胞迁移的证据主要来自动物研究",
]))

A.append(h2("落到临床"))
A.append(p(
    f"这篇最大的价值是给了一个{mk('清楚、好执行的框架')}：先分型（程度、部位、组织、复发），再按“等长 → 向心 → 离心”分期推进，"
    f"每次进阶都用{b('“这一种收缩做到最大还痛不痛”')}来判断，配合超声复查。"
))
A.append(p(
    f"几个容易被忽略的细节值得记住：{red('72 小时内不要热疗')}；{red('一期不要深层按摩')}；二期向心收缩不超过 60% 1RM；"
    f"{b('力量没到对侧 70% 别急着加跑')}；回归前至少完整练一周。"
))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注悦美力公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Palermi S, Massa B, Vecchiato M, Mazza F, De Blasiis P, Romano AM, Di Salvatore MG, Della Valle E, Tarantino D, Ruosi C, Sirico F. Indirect Structural Muscle Injuries of Lower Limb: Rehabilitation and Therapeutic Exercise. J Funct Morphol Kinesiol. 2021;6(3):75. doi:10.3390/jfmk6030075</em><br>"
    "原文以 CC BY 4.0 协议开放获取。动作照片来自原文表 2～5（器材上的英文商标已模糊），三期总览图为编者按原文绘制，仅用于学术交流。"
))

TITLE = "「肌肉损伤」下肢拉伤怎么练？等长、向心、离心三期康复和回归标准"
BODY = "".join(A)
(HERE / "article_body.html").write_text(BODY, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>下肢肌肉拉伤康复推文</title>
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
