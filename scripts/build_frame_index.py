#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create frame manifests and a markdown keyframe table from extracted frames JSON.")
    parser.add_argument("frames_json", help="JSON output from extract_keyframes.py")
    parser.add_argument("manifest_dir")
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    frames_json = Path(args.frames_json).expanduser().resolve()
    manifest_dir = Path(args.manifest_dir).expanduser().resolve()
    manifest_dir.mkdir(parents=True, exist_ok=True)
    markdown_output = Path(args.markdown_output).expanduser().resolve()

    payload = json.loads(frames_json.read_text())
    rows = ["| frame_id | timecode | frame_type | purpose | subject_state | motion_note | recommended_use |", "|---|---|---|---|---|---|---|"]
    for frame in payload["frames"]:
        manifest_path = manifest_dir / f"{frame['frame_id']}.json"
        manifest = {
            "frame_id": frame["frame_id"],
            "timecode": frame["timecode"],
            "frame_type": frame["frame_type"],
            "image_path": frame["image_path"],
            "status": "extracted",
            "diagnosis": {},
            "required_layers": [],
            "layer_paths": {},
            "scene_match": {},
            "prompts": {}
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=True, indent=2) + "\n")
        rows.append(f"| {frame['frame_id']} | {frame['timecode']} | {frame['frame_type']} | pending | pending | pending | pending |")

    markdown_output.write_text("\n".join(rows) + "\n")
    print(str(markdown_output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
