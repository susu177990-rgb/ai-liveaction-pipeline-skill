# 03 Frame Diagnosis

## Purpose

Generate a shot-structure diagnosis card for every core frame so scene matching and fusion decisions are grounded.

## Required inputs

- frame manifests from stage 02
- source video context

## Execution steps

1. Open each core frame and classify:
   shot size, camera height, camera direction, focal feel, subject position, body orientation.
2. Record action state, expression state, hand state, and visible contact points.
3. Mark foreground obstruction, midground structures, replaceable background area, horizon line, vanishing direction, and main perspective lines.
4. Decide whether original lighting can be reused, partially reused, or discarded.
5. Fill [frame-diagnosis-card.md](../templates/frame-diagnosis-card.md) and update the frame manifest.

## Expected outputs

- one diagnosis card per core frame
- updated frame manifests with structure notes

## Writes

- `02_keyframes/diagnosis/*.md`
- `manifests/frames/*.json`

## Upstream / downstream

- requires `02-keyframe-selection`
- feeds `04-asset-bible` and `05-scene-camera-match`

## Escalation conditions

- perspective lines cannot be recovered
- contact points are ambiguous
- frame is too blocked or too distorted for reliable conversion
