# 00 Project Intake

## Purpose

Lock the project brief, delivery target, risk notes, and folder ownership before any video parsing begins.

## Required inputs

- source video path or source video delivery note
- project name
- target aspect ratio
- desired output platform or downstream tool

Useful optional inputs:

- subject references
- scene references
- prop references
- style references
- client notes
- storyboard or shot intent

## Execution steps

1. Read the source package and identify what is present versus missing.
2. Fill [project-brief-template.md](../templates/project-brief-template.md).
3. Create or update the root `project manifest` using [project.schema.json](../schemas/project.schema.json).
4. Record any missing dependencies as `blocking`, `risky`, or `optional`.
5. Normalize the target directory structure using the standard project scaffold.

## Expected outputs

- completed project brief
- root project manifest
- intake risk summary
- standardized project folder map

## Writes

- `manifests/project.json`
- `00_brief/project-brief.md`

## Upstream / downstream

- no upstream stage
- feeds `01-video-ingest`

## Escalation conditions

- no source video
- no clear project goal
- contradictory output ratio or platform requirements
