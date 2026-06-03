---
name: ai-liveaction-pipeline
description: 专业级 AI+实拍生产管线，用于把原始实拍视频和参考资产整理成可控的关键帧包、场景机位匹配、预处理要求、空背景提示词、人物融合提示词、连续性质检和可交付 manifest。适用于 AI+实拍、AI+liveaction、实拍换景、关键帧抽取、镜头拆解、空背景生成、人物融合重光照、连续镜头一致性、角色/服装/道具替换，以及基于原视频搭建商业级镜头转换流程的场景。用户提到原始实拍视频、参考图、机位匹配、关键帧、空背景、融合提示词、连贯性质检、交付包时使用这个 skill。
---

# AI+实拍 Pipeline

用这个 skill 把一段实拍视频和一组参考资产，拆成一套可执行、可追踪、可复检的 AI+实拍生产包。默认把原视频当作结构真相来源，再围绕关键帧、镜头诊断、场景机位匹配、预处理层、空背景、融合提示词、修复提示词、连续性质检和最终交付 manifest 展开。

## 这个 skill 负责什么

- 项目 intake 和 manifest 初始化
- 视频探测与关键帧抽取
- 单帧结构诊断
- 角色 / 场景 / 道具 / 风格资产归一化
- 场景机位匹配与阈值判断
- 预处理层需求定义
- 空背景提示词生成
- 人物融合与重光照提示词生成
- 连续性质检与最终交付摘要

## 核心模块

先读这几个根级模块：

- [SKILL.md](./SKILL.md)
  定位、标准输入输出、阶段总览
- [role.md](./role.md)
  执行身份与职责边界
- [rule.md](./rule.md)
  硬规则与停机条件
- [flowchart.md](./flowchart.md)
  阶段路由与回退逻辑

按需再加载详细资源：

- `workflows/`
  各阶段的具体执行说明
- `templates/`
  输出模板
- `schemas/`
  manifests 和校验结构
- `tools/`
  本地确定性工具与外部接入指南
- `examples/`
  端到端参考案例
- `glossary.md`
  中英术语对照

先只加载当前阶段必需文件，不要把全部 `workflows/`、`templates/`、`schemas/` 一次性读入上下文。需要落地文件、批量整理或结构化校验时，优先运行 `scripts/` 下的本地工具。

## 命令

| Command | Action | Load |
|---|---|---|
| `/start` | 说明 skill 的用途、输入要求和阶段结构 | `SKILL.md`, `flowchart.md` |
| `/intake` | 创建或检查项目 brief 和根 manifest | `workflows/00-project-intake.md`, `templates/project-brief-template.md`, `schemas/project.schema.json` |
| `/ingest` | 探测源视频并输出 ingest 元数据 | `workflows/01-video-ingest.md`, `templates/video-ingest-card.md` |
| `/keyframes` | 抽取或整理关键帧，并建立 frame stubs | `workflows/02-keyframe-selection.md`, `templates/keyframe-table.md`, `schemas/frame.schema.json` |
| `/diagnose` | 为核心帧生成结构诊断卡 | `workflows/03-frame-diagnosis.md`, `templates/frame-diagnosis-card.md` |
| `/assets` | 整理角色、场景、道具、风格资产库 | `workflows/04-asset-bible.md`, `templates/subject-lock-card.md`, `templates/scene-camera-card.md`, `templates/prop-lock-card.md`, `templates/style-lock-card.md`, `schemas/asset.schema.json` |
| `/match` | 对帧和场景机位做匹配评分 | `workflows/05-scene-camera-match.md`, `tools/scene-match-score-guide.md`, `schemas/scene-match.schema.json` |
| `/preprocess` | 定义遮罩、深度、姿态、边缘、接触点等预处理层 | `workflows/06-preprocessing-layers.md`, `tools/mask-guide.md`, `tools/depth-pose-guide.md`, `tools/contact-map-guide.md` |
| `/plate` | 生成空背景策略和提示词包 | `workflows/07-empty-plate-generation.md`, `templates/empty-plate-prompt-template.md` |
| `/fusion` | 生成人物融合与修复提示词包 | `workflows/08-subject-fusion-relight.md`, `templates/fusion-prompt-template.md`, `templates/repair-prompt-template.md` |
| `/qc` | 运行连续性和交付质检 | `workflows/09-continuity-control.md`, `templates/qc-checklist.md`, `schemas/qc.schema.json` |
| `/deliver` | 汇总最终交付状态和摘要 | `workflows/10-final-delivery-qc.md`, `schemas/project.schema.json`, `schemas/qc.schema.json` |
| `/help` | 显示命令表和使用说明 | `SKILL.md`, `flowchart.md` |

## 默认交互方式

- 用显式命令决定当前大阶段。
- 阶段内自然语言补充默认只影响当前阶段，除非用户明确要求切换阶段。
- 不因为用户着急要提示词就跳过结构分析、机位匹配或预处理判断。

如果用户没有显式输入命令，就按意图自动映射：

- 想先看这套流程怎么做，映射到 `/start`
- 想建项目包、整理 brief 或开始接单，映射到 `/intake`
- 想分析视频、抽帧、选关键帧，映射到 `/ingest` 或 `/keyframes`
- 想判断镜头能不能换景、背景合不合、机位像不像，映射到 `/match`
- 想要空背景提示词、融合提示词、修复提示词，先确认上游阶段是否已完成，再映射到 `/plate` 或 `/fusion`
- 想检查连续性、做交付总结或收尾，映射到 `/qc` 或 `/deliver`

## 默认项目目录

每个真实项目默认落地到：

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

需要本地自动化时，优先使用 skill 自带的 `scripts/` 工具。

## 硬执行规则

- 把原视频作为动作、透视、接触关系和时间节奏的真相来源。
- 当场景机位匹配低于阈值时，禁止硬融。
- 把 `subject_mask`、`face_mask`、`outfit_mask`、`hand_mask`、`prop_mask`、`depth_map`、`pose_map`、`edge_map`、`contact_map` 当作正式管线资产。
- 有不确定项就明确标出，不要假装项目已经可交付。

## 验证

宣布这套 skill 完成前，至少要做这些检查：

- 用本地 quick validator 校验 `SKILL.md`
- 保证 `agents/openai.yaml` 与这个入口一致
- 保证 `default_prompt` 显式使用 `$ai-liveaction-pipeline`
- 保证 schema 键名、模板、脚本和示例使用同一套字段名
