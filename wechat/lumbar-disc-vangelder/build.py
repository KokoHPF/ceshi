#!/usr/bin/env python3
"""统一推文插图比例。

原稿里并排的两张（或 2×2 四张）图片是用表格加百分比宽度排的，原图长宽比不同，
排出来高矮不一。这里把每组图片预先拼成一张图：同一行的图片缩放到相同高度，
整行铺满 1080px 宽（过高时限高居中），再用这张拼图替换原来的表格。
两张横图并排会太扁，改为上下排；单张图片统一居中、按类型给宽度。

用法：python3 build.py   → 生成 preview.html（在线预览）和 article_body.html（上传用正文）
"""
import pathlib
import re

from PIL import Image

HERE = pathlib.Path(__file__).parent
IMG = HERE / "images"
W, GAP, MAX_H, MIN_ROW_H = 1080, 16, 760, 330

# 单张图宽度：示意图窄一些，照片按横竖构图给宽度
SINGLE_WIDTH = {"fig01": "90%", "fig02": "72%", "fig20": "100%", "fig28": "56%"}


def stem(src):
    return re.match(r"(fig\d+[a-d]?)", src.split("/")[-1]).group(1)


def row_image(stems):
    ims = [Image.open(IMG / f"{s}.jpg").convert("RGB") for s in stems]
    ratios = [i.width / i.height for i in ims]
    h = min(MAX_H, int((W - GAP * (len(ims) - 1)) / sum(ratios)))
    ims = [i.resize((round(h * r), h), Image.LANCZOS) for i, r in zip(ims, ratios)]
    row = Image.new("RGB", (W, h), "white")
    x = (W - sum(i.width for i in ims) - GAP * (len(ims) - 1)) // 2
    for i in ims:
        row.paste(i, (x, 0))
        x += i.width + GAP
    return row


def row_height(stems):
    ratios = [Image.open(IMG / f"{s}.jpg").width / Image.open(IMG / f"{s}.jpg").height for s in stems]
    return (W - GAP * (len(stems) - 1)) / sum(ratios)


def compose(rows, name):
    # 横图并排会太扁（手机上不到 100px 高），这类行改成上下排，每张占满宽度
    flat = []
    for r in rows:
        flat.extend([[s] for s in r] if len(r) > 1 and row_height(r) < MIN_ROW_H else [r])
    parts = [row_image(r) for r in flat]
    out = Image.new("RGB", (W, sum(p.height for p in parts) + GAP * (len(parts) - 1)), "white")
    y = 0
    for p in parts:
        out.paste(p, (0, y))
        y += p.height + GAP
    out.save(IMG / name, quality=88, optimize=True)
    return name


src = (HERE / "original.html").read_text(encoding="utf-8")
body = re.search(r"<body[^>]*>(.*)</body>", src, re.S).group(1)

# 1) 并排图片表格 → 拼图
TABLE = re.compile(r'<table style="width:100%; border-collapse:collapse; margin:18px 0 0; table-layout:fixed;">(.*?)</table>', re.S)


def repl_table(m):
    rows = [[stem(s) for s in re.findall(r'<img src="([^"]+)"', tr)] for tr in re.findall(r"<tr>(.*?)</tr>", m.group(1), re.S)]
    name = compose(rows, "pair_" + "_".join(s for r in rows for s in r) + ".jpg")
    return (f'<p style="text-align:center; margin:18px 0 4px;">'
            f'<img src="images/{name}" style="width:100%; display:block; margin:0 auto;" /></p>')


body, n_tables = TABLE.subn(repl_table, body)
# 拼图下方图注原来上边距只有 4px，与单图图注统一
body = body.replace('margin:4px 0 20px;">🔖', 'margin:0 0 22px;">🔖')

# 2) 单张图片 → 统一居中与宽度
SINGLE = re.compile(r'<p style="text-align:center; margin:18px 0 4px;"><img src="(images/fig[^"]+)" style="[^"]*" /></p>')


def repl_single(m):
    s = stem(m.group(1))
    return (f'<p style="text-align:center; margin:18px 0 4px;">'
            f'<img src="images/{s}.jpg" style="width:{SINGLE_WIDTH.get(s, "90%")}; display:block; margin:0 auto;" /></p>')


body, n_single = SINGLE.subn(repl_single, body)
assert "<table style=\"width:100%; border-collapse:collapse; margin:18px 0 0;" not in body
print(f"拼图 {n_tables} 组，单图 {n_single} 张")

(HERE / "article_body.html").write_text(body, encoding="utf-8")
(HERE / "preview.html").write_text(
    """<title>腰椎间盘突出康复推文</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
  :root { --ground:#ececec; --paper:#ffffff; color-scheme:light; }
  body { background:var(--ground); padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:16px 32px; }
  .paper { max-width:640px; margin:0 auto; background:var(--paper); padding:20px 16px 28px; box-sizing:border-box; }
  .paper img { max-width:100%; }
</style>
<div class="paper">
""" + body + "\n</div>\n",
    encoding="utf-8",
)
