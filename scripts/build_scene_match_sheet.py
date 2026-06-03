#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCORING_KEYS = [
    "horizon_alignment",
    "camera_height_match",
    "vanishing_direction_match",
    "lens_feel_match",
    "subject_staging_support",
    "ground_plane_match",
    "light_direction_match",
    "action_support_match"
]


def classify(score: float) -> str:
    if score >= 80:
        return "direct_fuse"
    if score >= 60:
        return "empty_plate_first"
    return "new_camera_needed"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build scene match manifests from a scoring sheet.")
    parser.add_argument("input_json", help="JSON array of frame/scene score entries")
    parser.add_argument("output_dir")
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    input_json = Path(args.input_json).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_output = Path(args.markdown_output).expanduser().resolve()
    entries = json.loads(input_json.read_text())

    lines = ["| frame_id | scene_id | total_score | result |", "|---|---|---|---|"]
    for entry in entries:
        total = sum(float(entry["scores"].get(key, 0)) for key in SCORING_KEYS)
        result = classify(total)
        payload = {
            "frame_id": entry["frame_id"],
            "scene_id": entry["scene_id"],
            "scores": entry["scores"],
            "total_score": total,
            "result": result,
            "notes": entry.get("notes", "")
        }
        (output_dir / f"{entry['frame_id']}__{entry['scene_id']}.json").write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n")
        lines.append(f"| {entry['frame_id']} | {entry['scene_id']} | {total} | {result} |")

    markdown_output.write_text("\n".join(lines) + "\n")
    print(str(markdown_output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
