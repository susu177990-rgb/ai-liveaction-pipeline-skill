# 10 Final Delivery QC

## Purpose

Compile the final production package and determine whether the project is ready for downstream video conversion or client delivery.

## Required inputs

- project manifest
- frame manifests
- scene match results
- QC manifests

## Execution steps

1. Run `scripts/validate_project.py` to check manifests and required file paths.
2. Run `scripts/compile_qc_report.py` to summarize readiness.
3. Fill the final section of [qc-checklist.md](../templates/qc-checklist.md).
4. Mark each frame and the root project as:
   `draft`, `ready_for_plate`, `ready_for_fusion`, `ready_for_video_conversion`, or `blocked`.
5. Save the final delivery summary.

## Expected outputs

- final QC report
- delivery readiness summary
- consolidated manifest status

## Writes

- `08_qc/final-qc-report.md`
- `09_delivery/delivery-summary.md`
- `manifests/project.json`

## Upstream / downstream

- requires `09-continuity-control`
- terminal stage before external video conversion

## Escalation conditions

- missing required outputs
- contradictory statuses across manifests
- unresolved high-risk QC failures
