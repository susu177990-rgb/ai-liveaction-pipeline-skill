# AI Liveaction Pipeline Skill

Professional AI + live-action production pipeline for turning a source video and reference assets into a structured, reviewable delivery package: project manifest, video ingest metadata, extracted keyframes, scene-camera match results, preprocessing requirements, prompt packs, QC outputs, and final delivery summaries.

## Features

This repo is useful when you need a repeatable workflow for:

- AI + live-action shot conversion
- keyframe extraction from source footage
- scene/camera matching before background replacement
- empty plate and fusion prompt packaging
- continuity control before downstream video generation

## What You Get

- Skill entrypoint and routing docs in [SKILL.md](./SKILL.md)
- Stage-by-stage workflow docs in [workflows/](./workflows)
- Reusable templates in [templates/](./templates)
- JSON schemas for manifests in [schemas/](./schemas)
- Local automation scripts in [scripts/](./scripts)
- End-to-end reference cases in [examples/](./examples)

## Repository Structure

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

## Installation

- Python 3.10+
- `ffmpeg` and `ffprobe`
- Python packages:
  - `Pillow`
  - `jsonschema`

Install Python dependencies:

```bash
python3 -m pip install Pillow jsonschema
```

Check video tooling:

```bash
ffmpeg -version
ffprobe -version
```

## Usage

Minimal end-to-end command flow:

```bash
$ python3 scripts/init_project.py ./demo-project --project-name "Mars Base Spot"
$ python3 scripts/probe_video.py ./demo-project/01_source_video/source.mp4 --output ./demo-project/00_brief/video-ingest.json
$ python3 scripts/extract_keyframes.py ./demo-project/01_source_video/source.mp4 ./demo-project/02_keyframes/frames > ./demo-project/manifests/frames-extracted.json
$ python3 scripts/build_frame_index.py ./demo-project/manifests/frames-extracted.json ./demo-project/manifests/frames --markdown-output ./demo-project/02_keyframes/keyframe-table.md
$ python3 scripts/validate_project.py ./demo-project
$ python3 scripts/compile_qc_report.py ./demo-project --output ./demo-project/08_qc/final-qc-report.md
```

## Quickstart

### 1. Create a project scaffold

```bash
python3 scripts/init_project.py ./demo-project \
  --project-name "Mars Base Spot" \
  --aspect-ratio "16:9" \
  --platform "comfyui" \
  --use-case "ai-liveaction-conversion"
```

This creates the standard working layout:

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

### 2. Probe the source video

```bash
python3 scripts/probe_video.py ./demo-project/01_source_video/source.mp4 \
  --output ./demo-project/00_brief/video-ingest.json
```

### 3. Extract keyframes

```bash
python3 scripts/extract_keyframes.py \
  ./demo-project/01_source_video/source.mp4 \
  ./demo-project/02_keyframes/frames \
  --percentages "0,20,40,60,80,100" \
  --contact-sheet ./demo-project/02_keyframes/contact_sheet.jpg \
  > ./demo-project/manifests/frames-extracted.json
```

### 4. Build frame manifests and keyframe table

```bash
python3 scripts/build_frame_index.py \
  ./demo-project/manifests/frames-extracted.json \
  ./demo-project/manifests/frames \
  --markdown-output ./demo-project/02_keyframes/keyframe-table.md
```

### 5. Validate the project package

```bash
python3 scripts/validate_project.py ./demo-project
```

### 6. Compile a final QC summary

```bash
python3 scripts/compile_qc_report.py \
  ./demo-project \
  --output ./demo-project/08_qc/final-qc-report.md
```

## Core Workflow

The intended pipeline is:

```text
/intake -> /ingest -> /keyframes -> /diagnose -> /assets -> /match -> /preprocess -> /plate -> /fusion -> /qc -> /deliver
```

Routing logic and fallback rules are documented in [flowchart.md](./flowchart.md).

## Common Tasks

### Initialize a new client job

Use `scripts/init_project.py` first, then fill:

- `00_brief/project-brief.md`
- `manifests/project.json`

Reference:

- [workflows/00-project-intake.md](./workflows/00-project-intake.md)
- [templates/project-brief-template.md](./templates/project-brief-template.md)

### Turn a video into structured keyframe assets

Use:

- `scripts/probe_video.py`
- `scripts/extract_keyframes.py`
- `scripts/build_frame_index.py`

Outputs:

- video metadata JSON
- extracted frame PNGs
- contact sheet
- frame manifests
- keyframe markdown table

### Gate scene replacement before fusion

Use the scene-match workflow and scoring helper before generating fusion prompts.

References:

- [workflows/05-scene-camera-match.md](./workflows/05-scene-camera-match.md)
- [tools/scene-match-score-guide.md](./tools/scene-match-score-guide.md)
- [scripts/build_scene_match_sheet.py](./scripts/build_scene_match_sheet.py)

The default threshold contract is:

- `>= 80`: `direct_fuse`
- `60-79`: `empty_plate_first`
- `< 60`: `new_camera_needed`

## Script Reference

| Script | Purpose |
|---|---|
| `scripts/init_project.py` | Create the standard project scaffold and root manifest |
| `scripts/probe_video.py` | Extract normalized video metadata with `ffprobe` |
| `scripts/extract_keyframes.py` | Extract keyframes and build a contact sheet |
| `scripts/build_frame_index.py` | Generate frame manifests and a markdown keyframe table |
| `scripts/build_scene_match_sheet.py` | Convert scoring input into scene-match manifests and summary table |
| `scripts/validate_project.py` | Validate manifests against the bundled JSON schemas |
| `scripts/compile_qc_report.py` | Summarize frame/QC readiness into a delivery report |

## Examples

Reference workflows:

- [Apartment MV](./examples/apartment-mv-workflow.md)
- [Commercial Product](./examples/commercial-product-workflow.md)
- [Concert Stage](./examples/concert-stage-workflow.md)
- [Mars Base](./examples/mars-base-workflow.md)

## Development

Check CLI entrypoints:

```bash
python3 scripts/init_project.py --help
python3 scripts/probe_video.py --help
python3 scripts/extract_keyframes.py --help
python3 scripts/build_frame_index.py --help
python3 scripts/build_scene_match_sheet.py --help
python3 scripts/validate_project.py --help
python3 scripts/compile_qc_report.py --help
```

Audit this README:

```bash
ruby /Users/griffith/.codex/skills/github-readme/scripts/github_readme_audit.rb README.md --strict
```

## Contributing

When updating the pipeline:

- keep workflow docs, templates, schemas, scripts, and examples aligned
- do not change threshold semantics in only one layer
- treat source video as the structural truth for motion, perspective, and contact

Start from:

- [role.md](./role.md)
- [rule.md](./rule.md)
- [SKILL.md](./SKILL.md)

## License

No license file is included yet. Add a project license before publishing for external reuse.
