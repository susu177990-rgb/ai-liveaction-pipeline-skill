# 04 Asset Bible

## Purpose

Normalize all subject, scene, prop, and style references into reusable cards with explicit lock rules.

## Required inputs

- subject references
- scene references
- prop references
- style references

## Execution steps

1. Create subject lock cards for characters, actors, outfits, and makeup continuity.
2. Create scene camera cards for scene tiles, empty plates, and camera-specific references.
3. Create prop lock cards for hold angle, contact relation, scale, and permitted substitutions.
4. Create style lock cards for palette, contrast, texture, grain, atmosphere, and light philosophy.
5. Register all assets in the asset manifest using [asset.schema.json](../schemas/asset.schema.json).

## Expected outputs

- subject lock cards
- scene camera cards
- prop lock cards
- style lock cards
- asset manifest

## Writes

- `03_assets/**/*.md`
- `04_scene_library/**/*.md`
- `manifests/assets/*.json`

## Upstream / downstream

- follows `03-frame-diagnosis`
- feeds `05-scene-camera-match`

## Escalation conditions

- key subject identity is under-defined
- scene reference lacks usable camera cues
- prop reference is visually inconsistent across assets
