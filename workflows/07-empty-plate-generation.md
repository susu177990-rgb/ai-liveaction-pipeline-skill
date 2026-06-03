# 07 Empty Plate Generation

## Purpose

Generate or specify a camera-matched empty plate whenever direct fusion is unsafe.

## Required inputs

- frame diagnosis card
- scene match result
- preprocessing layer requirements
- style and scene constraints

## Execution steps

1. Confirm the frame result is `empty_plate_first` or `new_camera_needed`.
2. If `new_camera_needed`, stop direct fusion and document the missing camera asset requirement.
3. If `empty_plate_first`, fill [empty-plate-prompt-template.md](../templates/empty-plate-prompt-template.md).
4. Record target horizon, camera height, vanishing direction, ground plane, foreground occlusion, and light direction.
5. Save empty plate prompt and asset target path.

## Expected outputs

- empty plate prompt package
- empty plate generation brief
- plate asset contract

## Writes

- `06_empty_plate/*.md`
- `manifests/frames/*.json`

## Upstream / downstream

- follows `05-scene-camera-match` and `06-preprocessing-layers`
- feeds `08-subject-fusion-relight`

## Escalation conditions

- no scene asset can support the frame
- empty plate still cannot satisfy contact or perspective logic
