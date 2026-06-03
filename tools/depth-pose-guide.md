# Depth Pose Guide

Depth and pose are structural aids, not decorative extras.

## Required outputs

- `depth_map`
- `pose_map`
- optional `edge_map`

## Recommended providers

- Depth Anything or MiDaS for depth
- OpenPose or DWPose for pose
- Canny or lineart tools for edge maps

## Contract

- save outputs under `05_preprocess/depth`, `05_preprocess/pose`, `05_preprocess/edge`
- record each path in the frame manifest
- mark confidence notes when outputs are partial or weak
