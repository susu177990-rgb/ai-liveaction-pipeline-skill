# 08 Subject Fusion Relight

## Purpose

Create controlled fusion prompts that respect structure first, then subject, then environment.

## Required inputs

- frame diagnosis card
- subject lock card
- scene or empty plate target
- preprocessing layer requirements
- style lock card

## Execution steps

1. Confirm structure source, subject source, and environment source are separately defined.
2. Fill [fusion-prompt-template.md](../templates/fusion-prompt-template.md).
3. Specify what must remain frozen:
   pose, body proportion, camera perspective, contact relations, action direction.
4. Specify what may change:
   environment, relight, atmosphere, controlled costume swap, controlled prop swap.
5. Fill [repair-prompt-template.md](../templates/repair-prompt-template.md) for likely failure regions:
   face, hands, edges, prop grip, contact shadow.

## Expected outputs

- fusion prompt package
- repair prompt package
- updated frame manifest statuses

## Writes

- `07_fusion/*.md`
- `manifests/frames/*.json`

## Upstream / downstream

- requires `06-preprocessing-layers` and `07-empty-plate-generation` when needed
- feeds `09-continuity-control`

## Escalation conditions

- subject identity remains under-locked
- plate geometry still conflicts with the subject
- relight intent contradicts scene logic
