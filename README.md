# AI Liveaction Pipeline Skill / AI+实拍生产管线 Skill

Professional AI + live-action pipeline for turning a source video and reference assets into a structured, reviewable package with manifests, keyframes, scene-match results, preprocessing requirements, prompt packs, QC outputs, and final delivery summaries.  
这是一个面向 AI+实拍项目的专业生产管线，用原始视频和参考资产整理出可追踪、可复检的项目包，包括 manifest、关键帧、场景匹配、预处理要求、提示词包、质检结果和最终交付摘要。

## Features / 特性

- AI + live-action shot conversion / AI+实拍镜头转换
- keyframe extraction from source footage / 从原视频抽取关键帧
- scene-camera matching before background replacement / 换景前做场景机位匹配
- empty plate and fusion prompt packaging / 输出空背景与融合提示词包
- continuity control before downstream video generation / 下游视频生成前做连续性质检

## What You Get / 仓库内容

- skill entrypoint and routing docs: [SKILL.md](./SKILL.md)
- workflow stages: [workflows/](./workflows)
- reusable templates: [templates/](./templates)
- JSON schemas: [schemas/](./schemas)
- local automation scripts: [scripts/](./scripts)
- reference cases: [examples/](./examples)

## Repository Structure / 仓库结构

```text
.
├── SKILL.md
├── role.md
├── rule.md
├── flowchart.md
├── agents/
├── examples/
├── schemas/
├── scripts/
├── templates/
├── tools/
└── workflows/
```

## Installation / 安装

- Python 3.10+
- `ffmpeg` and `ffprobe`
- Python packages / Python 依赖:
  - `Pillow`
  - `jsonschema`

```bash
python3 -m pip install Pillow jsonschema
ffmpeg -version
ffprobe -version
```

## Usage / 用法

Minimal end-to-end command flow / 最小端到端命令流程:

```bash
$ python3 scripts/init_project.py ./demo-project --project-name "Mars Base Spot"
$ python3 scripts/probe_video.py ./demo-project/01_source_video/source.mp4 --output ./demo-project/00_brief/video-ingest.json
$ python3 scripts/extract_keyframes.py ./demo-project/01_source_video/source.mp4 ./demo-project/02_keyframes/frames > ./demo-project/manifests/frames-extracted.json
$ python3 scripts/build_frame_index.py ./demo-project/manifests/frames-extracted.json ./demo-project/manifests/frames --markdown-output ./demo-project/02_keyframes/keyframe-table.md
$ python3 scripts/validate_project.py ./demo-project
$ python3 scripts/compile_qc_report.py ./demo-project --output ./demo-project/08_qc/final-qc-report.md
```

## Quickstart / 快速开始

### 1. Create a project scaffold / 创建项目骨架

```bash
python3 scripts/init_project.py ./demo-project \
  --project-name "Mars Base Spot" \
  --aspect-ratio "16:9" \
  --platform "comfyui" \
  --use-case "ai-liveaction-conversion"
```

Standard working layout / 标准目录结构:

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

### 2. Probe the source video / 探测源视频

```bash
python3 scripts/probe_video.py ./demo-project/01_source_video/source.mp4 \
  --output ./demo-project/00_brief/video-ingest.json
```

### 3. Extract keyframes / 抽取关键帧

```bash
python3 scripts/extract_keyframes.py \
  ./demo-project/01_source_video/source.mp4 \
  ./demo-project/02_keyframes/frames \
  --percentages "0,20,40,60,80,100" \
  --contact-sheet ./demo-project/02_keyframes/contact_sheet.jpg \
  > ./demo-project/manifests/frames-extracted.json
```

### 4. Build frame manifests / 生成帧 manifest

```bash
python3 scripts/build_frame_index.py \
  ./demo-project/manifests/frames-extracted.json \
  ./demo-project/manifests/frames \
  --markdown-output ./demo-project/02_keyframes/keyframe-table.md
```

### 5. Validate the package / 校验项目包

```bash
python3 scripts/validate_project.py ./demo-project
```

### 6. Compile final QC summary / 汇总最终 QC

```bash
python3 scripts/compile_qc_report.py \
  ./demo-project \
  --output ./demo-project/08_qc/final-qc-report.md
```

## Core Workflow / 核心流程

```text
/intake -> /ingest -> /keyframes -> /diagnose -> /assets -> /match -> /preprocess -> /plate -> /fusion -> /qc -> /deliver
```

Routing logic and fallback rules are documented in [flowchart.md](./flowchart.md).  
路由逻辑和回退规则见 [flowchart.md](./flowchart.md)。

## Common Tasks / 常见任务

### Initialize a new client job / 初始化新项目

Use `scripts/init_project.py`, then fill `00_brief/project-brief.md` and `manifests/project.json`.  
先运行 `scripts/init_project.py`，再补全 `00_brief/project-brief.md` 和 `manifests/project.json`。

References / 参考:

- [workflows/00-project-intake.md](./workflows/00-project-intake.md)
- [templates/project-brief-template.md](./templates/project-brief-template.md)

### Turn a video into keyframe assets / 把视频转成关键帧资产

Use / 使用:

- `scripts/probe_video.py`
- `scripts/extract_keyframes.py`
- `scripts/build_frame_index.py`

Outputs / 产物:

- video metadata JSON
- extracted frame PNGs
- contact sheet
- frame manifests
- keyframe markdown table

### Gate scene replacement before fusion / 融合前先做换景准入判断

References / 参考:

- [workflows/05-scene-camera-match.md](./workflows/05-scene-camera-match.md)
- [tools/scene-match-score-guide.md](./tools/scene-match-score-guide.md)
- [scripts/build_scene_match_sheet.py](./scripts/build_scene_match_sheet.py)

Threshold contract / 阈值规则:

- `>= 80`: `direct_fuse`
- `60-79`: `empty_plate_first`
- `< 60`: `new_camera_needed`

## Script Reference / 脚本说明

| Script | Purpose |
|---|---|
| `scripts/init_project.py` | Create the project scaffold and root manifest |
| `scripts/probe_video.py` | Extract normalized video metadata with `ffprobe` |
| `scripts/extract_keyframes.py` | Extract keyframes and build a contact sheet |
| `scripts/build_frame_index.py` | Generate frame manifests and a keyframe table |
| `scripts/build_scene_match_sheet.py` | Build scene-match manifests and summary table |
| `scripts/validate_project.py` | Validate manifests against bundled JSON schemas |
| `scripts/compile_qc_report.py` | Summarize frame and QC readiness |

## Examples / 示例

- [Apartment MV](./examples/apartment-mv-workflow.md)
- [Commercial Product](./examples/commercial-product-workflow.md)
- [Concert Stage](./examples/concert-stage-workflow.md)
- [Mars Base](./examples/mars-base-workflow.md)

## Development / 开发

```bash
python3 scripts/init_project.py --help
python3 scripts/probe_video.py --help
python3 scripts/extract_keyframes.py --help
python3 scripts/build_frame_index.py --help
python3 scripts/build_scene_match_sheet.py --help
python3 scripts/validate_project.py --help
python3 scripts/compile_qc_report.py --help
ruby /Users/griffith/.codex/skills/github-readme/scripts/github_readme_audit.rb README.md --strict
```

## Contributing / 贡献

- keep workflows, templates, schemas, scripts, and examples aligned / 保持 workflow、模板、schema、脚本、示例同步
- do not change threshold semantics in only one layer / 不要只改某一层的阈值语义
- treat the source video as structural truth for motion, perspective, and contact / 把原视频当作动作、透视、接触关系的结构真相

Start from / 先看:

- [role.md](./role.md)
- [rule.md](./rule.md)
- [SKILL.md](./SKILL.md)

## License / 许可

No license file is included yet. Add one before external reuse.  
当前仓库还没有 license，若要对外复用，先补许可证文件。
