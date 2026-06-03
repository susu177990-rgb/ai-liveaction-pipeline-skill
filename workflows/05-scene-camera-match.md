# 05 Scene Camera Match

## Purpose

Score each frame against available scene camera assets before attempting fusion.

## Required inputs

- diagnosed frame manifests
- scene camera cards

## Match result classes

- `direct_fuse`
- `empty_plate_first`
- `new_camera_needed`

## Execution steps

1. Compare each frame against candidate scene camera assets.
2. Score horizon, vanishing direction, camera height, lens feel, subject staging support, ground plane, light direction fit, and action compatibility.
3. Record weighted scores using [scene-match.schema.json](../schemas/scene-match.schema.json).
4. Use the result thresholds:
   - `>= 80` -> `direct_fuse`
   - `60-79` -> `empty_plate_first`
   - `< 60` -> `new_camera_needed`
5. Summarize recommended scene per frame and note why weaker candidates failed.

## Expected outputs

- frame-to-scene match table
- scene match manifests
- fusion strategy per frame

## Writes

- `04_scene_library/scene-match-sheet.md`
- `manifests/scene_match/*.json`

## Upstream / downstream

- requires `03-frame-diagnosis` and `04-asset-bible`
- feeds `06-preprocessing-layers` and `07-empty-plate-generation`

## Escalation conditions

- no candidate scene reaches `60`
- action support conflicts with chosen scene
- ground or perspective mismatch remains unresolved
