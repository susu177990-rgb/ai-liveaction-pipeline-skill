# 06 Preprocessing Layers

## Purpose

Define which structural layers are required per frame before plate generation or fusion.

## Required formal layers

- `subject_mask`
- `face_mask`
- `outfit_mask`
- `hand_mask`
- `prop_mask`
- `depth_map`
- `pose_map`
- `edge_map`
- `contact_map`

## Required inputs

- frame diagnosis data
- scene match result

## Execution steps

1. Inspect the frame and note which edges, joints, contacts, and overlaps are fragile.
2. Mark every required preprocessing output in the frame manifest.
3. Use the guides in `tools/` to define asset shape and expected file paths.
4. Fill the preprocessing checklist per frame or batch.
5. Mark missing layers as blockers when they affect contact, identity, or spatial logic.

## Expected outputs

- per-frame preprocessing checklist
- updated frame manifests with required layer paths

## Writes

- `05_preprocess/preprocess-plan.md`
- `manifests/frames/*.json`

## Upstream / downstream

- follows `05-scene-camera-match`
- feeds `07-empty-plate-generation` and `08-subject-fusion-relight`

## Escalation conditions

- no reliable subject edge
- no usable depth or pose strategy for the frame
- contact points cannot be isolated
