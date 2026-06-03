# Scene Match Score Guide

Score each frame against candidate scene cameras using weighted criteria.

## Suggested dimensions

- `horizon_alignment`
- `camera_height_match`
- `vanishing_direction_match`
- `lens_feel_match`
- `subject_staging_support`
- `ground_plane_match`
- `light_direction_match`
- `action_support_match`

## Result thresholds

- `>= 80` -> `direct_fuse`
- `60-79` -> `empty_plate_first`
- `< 60` -> `new_camera_needed`

Do not average away structural failure. A scene with a strong art style but broken ground plane should still fail.
