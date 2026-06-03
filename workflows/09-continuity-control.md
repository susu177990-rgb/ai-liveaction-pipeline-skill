# 09 Continuity Control

## Purpose

Check that adjacent frames can survive video conversion without identity, prop, lighting, or spatial drift.

## Required inputs

- fusion results or prepared fusion prompts
- neighboring frame manifests
- asset lock cards

## Execution steps

1. Compare adjacent keyframes in timeline order.
2. Check:
   identity, hairstyle, outfit, prop state, body proportion, motion direction, light direction, palette, background geometry, and contact shadow logic.
3. Fill the QC checklist for each frame group.
4. Route failures backward:
   - structure mismatch -> `05-scene-camera-match`
   - missing layer -> `06-preprocessing-layers`
   - bad plate -> `07-empty-plate-generation`
   - bad prompt logic -> `08-subject-fusion-relight`

## Expected outputs

- continuity QA record
- issue log with re-entry stage per failure

## Writes

- `08_qc/continuity-qc.md`
- `manifests/qc/*.json`

## Upstream / downstream

- follows `08-subject-fusion-relight`
- feeds `10-final-delivery-qc`

## Escalation conditions

- serial identity drift
- prop state resets
- lighting direction flips between adjacent frames
