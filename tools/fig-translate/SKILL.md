---
name: paper-figure-zh
description: 把论文 PDF 配图里的英文原位翻译成中文，保留原图的排版、插画、线条和数据不变，可整篇批量处理。用户要求翻译论文配图、图中文字汉化、给推文准备中文版原文图时使用。
---

# 论文配图英译中（原位替换）

目标：图里的英文换成中文，位置、字号、颜色、方向（含竖排坐标轴标题）跟原文一致，图形本身不动。整篇论文的图一次处理完。

工具是仓库 `KokoHPF/ceshi` 里的 `tools/fig-translate/figtrans.py`（说明见同目录 README.md）。

- **矢量图**：直接删除 PDF 里的英文文字对象，在原位写中文。不经过 OCR，零识别误差，图形不改动。这是主路线。
- **位图**（没有文字层）：自动改走 OCR + 背景修补 + 写中文的备用路线，有损。

## 准备

1. 找到脚本：优先用工作区里的 `tools/fig-translate/figtrans.py`。没有的话，从 GitHub 仓库 `KokoHPF/ceshi` 取 `tools/fig-translate/` 整个目录（含 `glossary.json`）放到草稿目录。
2. 安装依赖：`pip install pymupdf pillow rapidocr-onnxruntime`（rapidocr 只有位图需要）。
3. 确认有中文字体（脚本会自动找 Noto Sans CJK 或文泉驿正黑，没有就 `apt-get install fonts-wqy-zenhei` 或用 `--font` 指定）。

## 流程

### 1. 提取（一条命令处理整篇）

```bash
python3 figtrans.py extract <论文.pdf> <工作目录>            # 整篇
python3 figtrans.py extract <论文.pdf> <工作目录> --pages 2,3,5   # 只要正文图时指定页码（从 1 开始）
```

输出每张图的编号、模式（vector/raster）和文字单元数，生成：
- `figs.json`：版式信息；`strings.json`：去重后的英文 → 中文（术语表里有的已预填）；`orig_<图号>.png`：原图预览。

看一眼 `orig_*.png`，确认找到的是真正的图。表格、清单页（如 Reporting Summary）之类误识别的，后面 render 时用 `--only` 排除；图的范围不对时用 `--clip 页码:x0,y0,x1,y1` 手动指定后重新 extract。

### 2. 翻译：一次性填完 strings.json

这是唯一需要动脑的一步，直接读 `strings.json` 全部键，整体理解后一次写回（用一个 Python 片段 `json.load` → 填值 → `json.dump(ensure_ascii=False, indent=1)`），不要逐条处理。规则：

- **不翻的留空**：缩写和专有名词（BSI、ECoG、EMG、WISCI II、药物代号、基因/蛋白名、型号）、单位、纯符号、面板字母。留空 = 保留原文。
- **键里的 `\n` 是原图换行**：
  - 如果这几行其实是**几个独立标签**（图例列表、纵向排列的通道名、"标题 + 数值"），译文用**相同数量的 `\n`** 逐行对应，脚本会逐行对位替换。
  - 如果是**一句话被折行**（如 `Magnetic resonance\nimaging and computed\ntomography scan`），译文不带 `\n`，脚本在原文本框内自动重新换行、自动缩字号。
- 译文尽量短：图中空间有限，用简洁的学术术语（例如 "Half-prominence width" → "半峰宽"），括号用全角，数字与中文之间留空格，单位保留原文（mA、Hz、s）。
- 同一术语全篇统一；文章里已有的中文译名优先。
- 被裁断的残缺词（如 `Half-prominenc`）照常按完整词翻译。

### 3. 出图

```bash
python3 figtrans.py render <工作目录> --dpi 300            # 可加 --only p2_1,p3_1
```

输出 `zh_<图号>.png`（发布用）、`zh_<图号>.pdf`（矢量，可无限放大）、`cmp_<图号>.png`（原图与译图对照）。

### 4. 检查

用 Read 逐张看 `cmp_*.png`，重点看 render 打印的 ⚠ 条目：
- **放不下 / 重叠**：把译文改短，或者在 `figs.json` 里改这个单元的 `align`（l/c/r），再 `render --only <图号>`。
- **"描边衬底下有底色，旧衬底未删"**：这种标签保留英文（译文留空）最干净，或接受残留。
- 位图路线看擦除痕迹；不理想的条目留空保留原文。

修改后只重出受影响的图，不用重新 extract（重新 extract 也会保留已填的译文）。

### 5. 收尾

- 把本次译文并入长期术语表，下次自动预填：`python3 figtrans.py glossary <工作目录>`，并把更新后的 `glossary.json` 一起提交。
- 交付时说明：哪些图是矢量无损替换、哪些走了位图路线、哪些条目刻意保留了原文。

## 效率参考

一篇 Nature 正文 4 张矢量图：extract 约 20 秒，render 约 30 秒，中间只需一次性填约 150 条去重英文。含 Extended Data 位图的整篇（21 张图）extract 约 1.5 分钟。
