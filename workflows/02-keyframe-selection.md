# 02 Keyframe Selection

## Purpose

Turn the source video into a controlled set of keyframe assets instead of relying on random screenshots.

## Required inputs

- source video
- video metadata from stage 01

## Keyframe classes

- `Anchor Frame`
  primary composition and identity baseline
- `Motion Keyframe`
  action shift, gesture change, body reorientation
- `Transition Frame`
  continuity support frames between main beats

## Execution steps

1. Decide whether to reuse existing supplied frames or extract new ones.
2. For simple shots, target at least:
   `0%`, `20%`, `40%`, `60%`, `80%`, `100%`.
3. For complex movement, expand to `8-12` frames.
4. Use `scripts/extract_keyframes.py` to extract frames and a contact sheet.
5. Use `scripts/build_frame_index.py` to create frame manifests and the keyframe table.
6. Label each extracted frame with `anchor`, `motion`, or `transition`.

## Expected outputs

- extracted frame files
- contact sheet
- keyframe table
- frame manifest stubs

## Writes

- `02_keyframes/frames/`
- `02_keyframes/contact_sheet.jpg`
- `02_keyframes/keyframe-table.md`
- `manifests/frames/*.json`

## Upstream / downstream

- requires `01-video-ingest`
- feeds `03-frame-diagnosis`

## Escalation conditions

- no frames clearly represent action transitions
- motion blur makes the frame unusable
- frame spacing is too sparse to support later video conversion
