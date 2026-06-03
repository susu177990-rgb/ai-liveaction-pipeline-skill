# 01 Video Ingest

## Purpose

Probe the source video and turn it into a reliable metadata card that every later stage can trust.

## Required inputs

- path to the source video
- project manifest created in stage 00

## Execution steps

1. Run `scripts/probe_video.py` on the source video.
2. Extract duration, frame rate, resolution, codec, pixel format, and aspect ratio.
3. Note broad camera behavior:
   `locked`, `pan`, `tilt`, `push`, `pull`, `track`, `handheld`, or `mixed`.
4. Fill [video-ingest-card.md](../templates/video-ingest-card.md).
5. Save normalized metadata back to the project manifest.

## Expected outputs

- video ingest card
- normalized video metadata JSON
- camera motion baseline

## Writes

- `00_brief/video-ingest.md`
- `manifests/project.json`

## Upstream / downstream

- requires `00-project-intake`
- feeds `02-keyframe-selection`

## Escalation conditions

- unreadable video
- missing ffprobe data
- corrupt frame count or unknown duration
