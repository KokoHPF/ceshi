# 论文配图英译中（figtrans）

把论文 PDF 配图里的英文换成中文，原位置、原字号、原颜色，插画、线条、色块和数据不动。

- **矢量图**（绝大多数期刊的正式图）：直接删除 PDF 里的英文文字对象，再在同一位置写入中文。不经过 OCR，没有识别误差，图形一个像素都不改。
- **位图**（扫描件、只有图片没有文字层的 Extended Data 等）：OCR 识别文字，纯色背景直接填色、复杂背景用修补算法擦除，再写中文。属于有损，备用。

## 安装

```bash
pip install pymupdf pillow rapidocr-onnxruntime   # rapidocr 只在处理位图时用到
```

需要一个中文字体，脚本会自动找 Noto Sans CJK、文泉驿正黑、苹方、微软雅黑，也可以用 `--font` 指定。

## 用法

```bash
# 1. 提取：自动找图，生成 figs.json（版式）、strings.json（去重后的英文 -> 待填中文）和 orig_*.png（原图预览）
python3 figtrans.py extract paper.pdf work/                 # 整篇
python3 figtrans.py extract paper.pdf work/ --pages 2,3,5   # 只要这几页（页码从 1 开始）
python3 figtrans.py extract paper.pdf work/ --clip 3:100,50,480,450   # 自动找图不准时手动给范围（PDF 坐标，单位 pt）

# 2. 填写 work/strings.json 里的中文

# 3. 出图：zh_*.png（发布用）、zh_*.pdf（矢量）、cmp_*.png（原图/译图对照，用来检查）
python3 figtrans.py render work/ --dpi 300
python3 figtrans.py render work/ --only p3_1,p5_1           # 只重出某几张

# 4. （可选）把这次的译文并入长期术语表 glossary.json，下次 extract 自动预填
python3 figtrans.py glossary work/
```

## strings.json 填写规则

- 值留空或与英文相同：保留原文（缩写、基因名、药物代号、单位、通道名等）。
- 键里的 `\n` 是原图换行。译文用**相同数量**的 `\n` 时逐行对位替换，适合图例、竖排的一列标签、"标题 + 数值" 这种其实是几个独立标签被合在一起的情况；译文不带 `\n` 时在原文本框内自动重新换行。
- 排版不对时可以改 `figs.json` 里对应单元的 `align`（`l`/`c`/`r`），再 `render`。

## 已知限制

- 自动找图靠"矢量图形 + 图片 + 短标签聚团"，偶尔会把表格、清单页（如 Reporting Summary）也当成图，看 `orig_*.png` 后用 `--pages` 或 `--only` 排除即可。
- 有的图给文字加了矢量描边衬底（白色字形轮廓）。下面没有底色时会一并删除；下面有底色块时为了不误删底色会保留旧衬底，`render` 会提示，此时可选择不翻这一条。
- 中文字体没有粗体，用描边模拟。
- 位图路线是有损的，复杂背景上的擦除痕迹需要人工看一眼。
