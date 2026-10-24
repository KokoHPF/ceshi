# paper-to-xhs-cards：论文 → 小红书图文卡片

把一篇医学 / 康复论文 PDF 做成 3:4 竖版学习卡片（1080×1440），默认署名“骨科康复小黄”，可改。

## 怎么给不同的模型 / 平台用

| 平台 | 做法 |
|---|---|
| Claude Code / Claude Agent SDK | 把整个文件夹放到项目的 `.claude/skills/paper-to-xhs-cards/`，会自动识别 `SKILL.md` |
| Claude.ai（Skills） | 把文件夹打成 zip 上传为自定义 Skill |
| 其他能运行代码的智能体（Codex、Cursor、Gemini CLI、OpenAI Agents 等） | 把文件夹放进工作区，在提示里写：“按 `paper-to-xhs-cards/SKILL.md` 的流程，把这篇 PDF 做成小红书卡片” |
| 只能聊天、不能运行代码的模型 | 只能参考 `SKILL.md` 里的内容规划部分写文案，图片需要人工排版 |

## 目录

```
SKILL.md                    给模型看的完整流程（核心）
config/theme.default.json   默认主题：账号名、配色、字体、尺寸、张数上限
scripts/cardkit.py          排版引擎（封面 / 图文卡 / 文字卡 / 数据图卡 / 速查表卡，自动字号）
scripts/extract_figures.py  提取 PDF 图片、图注、页面渲染
scripts/fetch_supplement.py 按 DOI 下载补充材料（视频、高清图）
scripts/video_frames.py     视频截帧
scripts/relabel.py          图中英文标注 → 中文（OCR + 修补 + 写字）
scripts/annotate.py         给示意图加中文结构标注和方向
scripts/pack.py             打包 zip
scripts/setup_fonts.sh      下载思源黑体
examples/thumb_test/        完整示例（拇指试验，9 张）
```

## 快速试跑示例

```bash
pip install pillow pymupdf numpy matplotlib opencv-python-headless rapidocr_onnxruntime
bash scripts/setup_fonts.sh
cd examples/thumb_test
python3 ../../scripts/fetch_supplement.py 10.1016/j.eats.2022.05.007 work
python3 ../../scripts/annotate.py annotate_spec.json --font ../../fonts/NotoSansSC-Bold.otf
python3 ../../scripts/video_frames.py work/mmc2.mp4 work --at 22 25 53 59 --crop-black
python3 build.py out          # 生成 out/card01.jpg … 和 out/_overview.jpg
```

## 改成自己的风格

新建 `my_theme.json`，只写要改的项，例如 `{"account": "某某康复", "colors": {"accent": "#E4572E"}}`，
构建时传 `Deck(..., theme='my_theme.json')`。
