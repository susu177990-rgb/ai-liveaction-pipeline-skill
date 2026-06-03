<p align="right">
  <strong>语言 / Language:</strong>
  <a href="#中文">中文</a> ·
  <a href="#english">English</a>
</p>

<a id="中文"></a>

# AI Liveaction Pipeline Skill

这是一个给 `AI + 实拍` 项目用的生产管线 skill。它的作用不是单点生图，而是把一条原始视频、关键帧、场景匹配、预处理、融合、质检和交付整理成一条完整流程，让项目从“有素材”变成“可执行、可复检、可交付”。

## 它能帮你解决什么

- 把原始视频先做信息探测和整理
- 自动抽关键帧，形成项目级帧资产
- 在换背景或融合前先判断机位与场景是否匹配
- 整理空镜、融合提示词、修补需求和质检清单
- 把项目从零散文件变成标准目录和 manifest

## 功能亮点

- 视频探测、抽帧、建索引一条龙
- 适合多人协作的标准项目目录
- 融合前先做场景匹配，减少返工
- 自带 schema 校验和 QC 汇总
- 既能跑脚本，也能按阶段拆开使用

## 适合谁

- 做 AI+实拍广告的人
- 做 MV、舞台片、品牌片、短剧后期流程的人
- 需要把视频转成关键帧和制作包的人
- 需要交给不同协作者继续处理的人

## 你会拿到什么

- 项目目录骨架
- 视频探测结果
- 关键帧图片和 contact sheet
- 帧索引和 markdown 表
- 场景匹配结果表
- QC 报告
- 最终交付摘要

## Installation / 安装

```bash
$ python3 -m pip install Pillow jsonschema
$ ffmpeg -version
$ ffprobe -version
```

## Usage / 用法

最短上手流程：

```bash
$ python3 scripts/init_project.py ./demo-project --project-name "Mars Base Spot"
$ python3 scripts/probe_video.py ./demo-project/01_source_video/source.mp4 --output ./demo-project/00_brief/video-ingest.json
$ python3 scripts/extract_keyframes.py ./demo-project/01_source_video/source.mp4 ./demo-project/02_keyframes/frames > ./demo-project/manifests/frames-extracted.json
$ python3 scripts/build_frame_index.py ./demo-project/manifests/frames-extracted.json ./demo-project/manifests/frames --markdown-output ./demo-project/02_keyframes/keyframe-table.md
$ python3 scripts/validate_project.py ./demo-project
$ python3 scripts/compile_qc_report.py ./demo-project --output ./demo-project/08_qc/final-qc-report.md
```

## 核心流程

```text
/intake -> /ingest -> /keyframes -> /diagnose -> /assets -> /match -> /preprocess -> /plate -> /fusion -> /qc -> /deliver
```

你不用一开始就把所有步骤都跑完。多数项目最常见的切入点只有三个：

- 先建项目骨架
- 先抽关键帧
- 先判断这条视频适不适合做换景和融合

## 常见任务

### 1. 新建一个标准项目

```bash
python3 scripts/init_project.py ./demo-project \
  --project-name "Mars Base Spot" \
  --aspect-ratio "16:9" \
  --platform "comfyui" \
  --use-case "ai-liveaction-conversion"
```

生成后会得到标准目录：

```text
00_brief/
01_source_video/
02_keyframes/
03_assets/
04_scene_library/
05_preprocess/
06_empty_plate/
07_fusion/
08_qc/
09_delivery/
manifests/
```

### 2. 把视频先转成关键帧资产

常用脚本：

- `scripts/probe_video.py`
- `scripts/extract_keyframes.py`
- `scripts/build_frame_index.py`

你会拿到：

- 视频元数据 JSON
- 关键帧 PNG
- contact sheet
- 帧 manifest
- keyframe markdown 表

### 3. 融合前先做准入判断

如果你不确定某个镜头适不适合直接换景或融合，先看场景匹配结果。

阈值规则：

- `>= 80`：`direct_fuse`
- `60-79`：`empty_plate_first`
- `< 60`：`new_camera_needed`

相关文件：

- [workflows/05-scene-camera-match.md](./workflows/05-scene-camera-match.md)
- [tools/scene-match-score-guide.md](./tools/scene-match-score-guide.md)
- [scripts/build_scene_match_sheet.py](./scripts/build_scene_match_sheet.py)

## 依赖

- Python `3.10+`
- `ffmpeg`
- `ffprobe`
- Python 包：
  - `Pillow`
  - `jsonschema`

## 关键脚本一览

| 脚本 | 作用 |
|---|---|
| `scripts/init_project.py` | 建项目骨架和根 manifest |
| `scripts/probe_video.py` | 用 `ffprobe` 提取视频元信息 |
| `scripts/extract_keyframes.py` | 抽关键帧并输出 contact sheet |
| `scripts/build_frame_index.py` | 生成帧索引和 keyframe 表 |
| `scripts/build_scene_match_sheet.py` | 生成场景匹配清单 |
| `scripts/validate_project.py` | 用 JSON schema 校验项目结构 |
| `scripts/compile_qc_report.py` | 汇总项目和 QC 最终状态 |

## 仓库结构

```text
.
├── README.md
├── SKILL.md
├── agents/
├── examples/
├── schemas/
├── scripts/
├── templates/
├── tools/
└── workflows/
```

## 推荐先看哪里

- [SKILL.md](./SKILL.md)：入口说明
- [flowchart.md](./flowchart.md)：整体流程图
- [workflows/](./workflows)：每个阶段做什么
- [examples/](./examples)：直接看成品流程案例

## 示例案例

- [Apartment MV](./examples/apartment-mv-workflow.md)
- [Commercial Product](./examples/commercial-product-workflow.md)
- [Concert Stage](./examples/concert-stage-workflow.md)
- [Mars Base](./examples/mars-base-workflow.md)

---

<a id="english"></a>

## English

`AI Liveaction Pipeline Skill` is a practical pipeline for `AI + live-action` production. It helps you turn source footage into a structured project package with keyframes, manifests, scene-match decisions, preprocessing tasks, QC results, and delivery summaries.

## Best for

- ad production
- MV workflows
- branded videos
- short-form live-action to AI conversion
- multi-person production handoff

## Fast path

```text
init project -> probe video -> extract keyframes -> build frame index -> validate -> compile QC
```

## Main outputs

- project scaffold
- video ingest metadata
- keyframes and contact sheet
- frame manifests
- scene-match sheets
- QC report
- delivery summary

## License / 许可

仓库内如有单独许可文件，以仓库实际文件为准；当前 README 不额外重定义许可。
