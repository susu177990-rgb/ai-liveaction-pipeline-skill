# Mask Guide

Treat mask generation as an external but formal dependency layer.

## Required mask outputs

- `subject_mask`
- `face_mask`
- `outfit_mask`
- `hand_mask`
- `prop_mask`

## Output contract

- one mask file per frame per layer
- same pixel dimensions as the frame
- explicit manifest path entry in the frame JSON
- clear binary or soft-edge intent noted in the manifest

## Tooling notes

Possible providers:

- SAM family
- RMBG or portrait segmentation tools
- manual Photoshop / Krita cleanup

The skill should never assume one provider is installed. It should define file shape, layer meaning, and where outputs belong.
