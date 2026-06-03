# ComfyUI Control Guide

ComfyUI is an optional downstream execution surface, not a hard dependency for this skill.

## What to specify

- expected input images
- required control layers
- prompt package
- output target paths
- batch naming convention

## Do not assume

- a fixed local install path
- a fixed custom-node set
- a fixed workflow JSON shape

Use this guide to describe how plates, masks, depth, pose, and fusion prompts should be handed off to a ComfyUI operator or workflow.
