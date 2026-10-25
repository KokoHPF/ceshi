#!/usr/bin/env python3
"""髋关节远程评估（Vomer 等 2023）推文。

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
F = lambda i: i + 2  # 原文图 i → 第 i+2 张图
A.append(img(1))
A.append(cap("原文信息（编者中文重排）"))
A.append(p(red("📚 文献信息"), "margin-bottom:10px;"))
A.append(ul([
    "Vomer RP II, York E, DeMatas K, Shah NP, Larick RS, Punj M, Rosario-Concepcion RA, Pujalte GGA. Telemedicine evaluation of hip ailments. Cureus. 2023;15(5):e38900. doi:10.7759/cureus.38900",
    "作者单位：美国梅奥诊所（杰克逊维尔）家庭医学科、运动医学科与康复科，杜克大学，东弗吉尼亚医学院",
    f"文章类型：期刊归为原创研究，实际是{b('作者经验整理的操作指南')}（示范模特是第一作者本人，没有验证数据）。和上一篇肘关节远程评估出自同一团队",
], square=True))

A.append(h2("先说结论"))
A.append(ul([
    f"远程查髋包括视诊、自我触诊、活动度、特殊检查、功能和步态，{b('大部分信息都能通过视频拿到')}",
    f"{mk('按体位排顺序')}：站 → 坐 → 站 → 仰卧 → 俯卧 → 坐，既减少折腾，变换体位本身也能看出髋痛对功能的影响",
    f"髋痛常常来自{b('腰椎、骶髂关节、腹股沟和腹盆腔')}，远程查髋要一起排查",
    f"出现{red('不能负重、红肿发热、夜间痛、大小便失禁')}等情况，不要停留在远程",
]))
A.append(img(2))
A.append(cap("远程查髋的体位顺序（编者根据原文整理）"))

A.append(h2("一、视诊"))
A.append(ul([
    f"让患者双脚与肩同宽站立，{b('最好穿贴身的运动服')}；从前、侧、后三面看",
    "前后面：髂前上棘、髂嵴是否等高，骨盆有无旋转；估计膝 Q 角，过大或过小会改变下肢动力链的受力，也可能引起髋痛",
    "侧面：腰椎前凸多少，有无“摇摆背”",
    f"让患者{b('指出最痛点，再用手指画出放射范围')}；留意经典的{b('“C 字征”')}：手呈 C 形握在大转子上方",
    "看有无发红、肿胀、明显畸形；有家人朋友在旁边，就请他们拿手机拍步态",
]))
A.append(pic(F(1), "原文图 1：视诊和自我触诊"))

A.append(h2("二、自我触诊"))
A.append(ul([
    "让患者按髂前上棘、髂后上棘、阔筋膜张肌、耻骨联合、坐骨结节、大转子，看哪里痛",
    "从髂嵴顶部开始，手沿顺时针方向逐个按各标志点",
    "再让患者说说大腿前侧、髋内侧、臀部的肌肉松紧、皮温和感觉",
]))

A.append(h2("三、活动度"))
A.append(p(f"髋的活动度要{b('左右对比')}，并且{b('同时查腰椎')}。"))
A.append(ul([
    "坐椅子、屈髋 90°，小腿向内、向外摆，看髋外旋、内旋时痛不痛（注意方向：足向外摆是髋内旋）",
    "同一姿势屈髋超过 90°，痛吗？能跷二郎腿吗？跷上去让上面的膝往外倒，痛吗？",
    "站立：向侧面抬腿估外展，向后伸腿估后伸",
    "腰椎：坐位前屈摸脚尖、后仰，从侧面估角度；侧屈和旋转从后面看",
]))
A.append(pic(F(2), "原文图 2：坐位查髋旋转"))

A.append(h2("四、特殊检查"))
A.append(h3("站立：先排除腰椎"))
A.append(pic(F(3), "原文图 3：Stork 试验"))
A.append(pic(F(4), "原文图 4：改良 Kemp 试验"))
A.append(h3("仰卧：髋、骶髂、神经根一起查"))
A.append(pic(F(5), "原文图 5：FABER（4 字）试验"))
A.append(ul([
    f"{b('FABER')}：一开始摆 4 字就痛 → 髋前方；往下压才痛 → 髋后方或骶髂关节；骶髂关节处痛 → 骶髂功能障碍或骶髂炎；腹股沟痛 → 髂腰肌拉伤、撞击、盂唇撕裂、软骨损伤或骨关节炎",
]))
A.append(pic(F(6), "原文图 6：改良直腿抬高和 Bragard 试验"))
A.append(pic(F(7), "原文图 7：改良 Thomas 试验"))
A.append(pic(F(8), "原文图 8：改良 FADDIR 试验"))
A.append(pic(F(9), "原文图 9：耻骨联合触诊和腹直肌离心测试"))
A.append(ul([
    "仰卧伸直双腿，看两侧足尖外旋是否一样：差别大提示髋稳定肌无力、过度活动或髋骨功能障碍",
    f"双腿慢放时，{b('腰过早离开垫在下面的手')}，提示腹直肌下部或脊柱稳定肌无力",
]))
A.append(h3("坐位和俯卧"))
A.append(ul([
    f"{b('改良 Beatty 试验')}：坐位跷二郎腿（患腿在上），再向前弯腰，复现疼痛提示梨状肌综合征",
    f"{b('Fortin 手指试验')}：最痛点正好在骶髂关节（髂后上棘下方的小窝附近），提示骶髂关节问题",
    "俯卧：查臀中肌腱病（“死臀综合征”）和臀肌发力顺序（原文没有给具体做法）",
]))

A.append(h2("五、力量、功能和步态"))
A.append(ul([
    f"{b('徒手深蹲')}：从侧面和后面看。能抗重力完成，下肢肌力至少 3 级",
    f"{b('髋移位')}：从后面看深蹲，骨盆偏向一侧，提示一侧髋活动度或力量不足（原文正文和图注对偏向哪侧说法相反，见文末）",
    f"{b('单腿站')}：看 Trendelenburg 征——对侧骨盆下沉，说明{b('支撑腿')}臀中肌无力",
    f"{b('单腿蹲')}：看髋无力、动态膝外翻，以及是否疼痛",
    "步态：看站宽、支撑时间和步长；视频里能看到 Trendelenburg 步态、划圈步态、跨阈步态和减痛步态",
]))
A.append(pic(F(10), "原文图 10：深蹲看髋移位"))
A.append(pic(F(11), "原文图 11：Trendelenburg 步态"))
A.append(pic(F(12), "原文图 12：划圈步态"))
A.append(pic(F(13), "原文图 13：跨阈步态"))

A.append(h2("六、电话问诊这样问"))
A.append(p(f"原文表 1～3 把每一项检查都改写成了患者能听懂的问题。编者按原表整理成三张卡（第三张合并了讨论部分的红旗）："))
A.append(img(16))
A.append(cap("问诊卡①：视诊和触诊（据原文表 1 改写）"))
A.append(img(17))
A.append(cap("问诊卡②：活动度和特殊检查（据原文表 2 改写）"))
A.append(img(18))
A.append(cap("问诊卡③：步态、功能和红旗（据原文表 3 和讨论整理）"))

A.append(h2("七、什么时候不能只靠远程"))
A.append(ul([
    f"{b('尽早拍片')}：不能负重、严重减痛步态、髋部红肿、外伤、夜间痛、发热或寒战伴髋痛",
    f"{red('立即线下就诊并做磁共振或 CT')}：大小便失禁、大腿内侧感觉消失、腿无力",
    "髋前方痛要想到腹腔疾病的牵涉痛；女性还要考虑卵巢囊肿、卵巢扭转、子宫内膜异位症、盆腔肌筋膜痛",
    "设备和沟通：双方都要有稳定网络和带摄像头的设备，平台要符合隐私保护要求；有语言障碍时一定要用医疗翻译",
]))

A.append(h2("这篇文章能信几分"))
A.append(ul([
    f"期刊归为原创研究，但{b('没有受试者也没有数据')}；所有远程检查都{red('没做过信度、效度验证')}",
    "作者自己承认：患者自己做的动作可能不如专业人员准确；活动严重受限的患者有些动作做不了；严重损伤时远程评估可能延误就医",
    "优点：按体位排好了检查顺序，覆盖腰椎、骶髂、腹股沟等髋痛常见来源，问题可以直接拿来用",
]))

A.append(h2("原文里对不上的地方"))
A.append(ul([
    f"{b('髋移位往哪边偏，说法相反')}：正文说“{red('偏离')}患侧”为阳性，表 3 也问“是否偏向没受伤那一侧”；图 10 图注却说“患者会{red('移向')}患侧”",
    f"{b('划圈步态的原因两处不一样')}：图 12 说提示髋内收肌张力高；表 3 说是髋膝屈肌或踝背屈肌无力和痉挛。通常划圈步态是摆动相屈髋、屈膝或踝背屈不足的代偿，内收肌张力高更常见的是剪刀步态",
    f"{b('跨阈步态的病因')}：跨阈步态通常是足下垂（踝背屈无力）的代偿，原文列出的可能病因里有“股骨头骨骺滑脱”，并不典型",
    f"{b('局限性和正文矛盾')}：局限性部分说远程“无法做触诊和力量测试”，但正文用了大量篇幅讲患者自我触诊、用深蹲和单腿站测力量",
    f"{b('图号引错')}：表 2 的 Kemp 试验写“见图 6”，应为图 4",
    f"{b('Thomas 试验四个观察点对不上')}：表 2 让患者看“髋屈起、膝伸直、小腿旋转、髋外旋”，结果解释却是“髋外展 → 阔筋膜张肌”，问的和答的不是同一项",
    f"{b('触诊清单')}：让患者摸的“骨性突起”里有小转子和梨状肌——小转子在体表摸不到，梨状肌是肌肉不是骨性突起",
    f"{b('FADDIR 少了内旋')}：图 8 只写了屈曲、内收再被动屈伸，没有内旋，表 2 也只说“屈髋上下活动”",
    f"{b('伦理声明自相矛盾')}：写着“梅奥诊所杰克逊维尔院区批准：无需批准”，又说本方案不需要伦理审批",
]))

A.append(h2("落到临床"))
A.append(ul([
    f"视频前提醒患者{b('穿贴身短裤、准备一把椅子和一块能躺的地方')}，最好有人帮忙拿手机",
    f"先让患者{b('指出最痛点')}：腹股沟（关节内）、大转子（外侧）、臀部或骶髂（后方），决定接下来的重点",
    f"查髋一定连带{b('腰椎和骶髂关节')}一起排查",
    "远程结果只是初筛；有红旗、或者远程看不清时，尽快安排线下查体和影像",
]))

A.append('<hr style="border:none;border-top:1px dashed #ccc;margin:32px 0 20px;">')
A.append(p(b("欢迎关注骨科康复小黄公众号，获取更多物理治疗的专业知识！"), "text-align:center;"))
A.append(p("📄<em>参考文献：</em>", "font-size:13px;margin-bottom:6px;"))
A.append(small(
    "<em>Vomer RP II, York E, DeMatas K, Shah NP, Larick RS, Punj M, Rosario-Concepcion RA, Pujalte GGA. Telemedicine evaluation of hip ailments. Cureus. 2023;15(5):e38900. doi:10.7759/cureus.38900</em><br>"
    "原文以知识共享署名 4.0（CC BY 4.0）协议开放获取。原文图 1～13 引自原文，中文标签为编者所加；流程卡和问诊卡据原文正文、表 1～3 和讨论整理改写。"
))

TITLE = "「髋关节」远程怎么查髋？视频问诊：视诊、自我触诊、活动度、FABER/Thomas/FADDIR 和步态"
PTITLE = "髋关节远程评估推文"
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
