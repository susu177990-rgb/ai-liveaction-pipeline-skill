#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a delivery QC summary from project manifests.")
    parser.add_argument("project_root")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    project = json.loads((root / "manifests" / "project.json").read_text())
    frame_paths = sorted((root / "manifests" / "frames").glob("*.json"))
    qc_paths = sorted((root / "manifests" / "qc").glob("*.json"))

    frames = [json.loads(path.read_text()) for path in frame_paths]
    qcs = [json.loads(path.read_text()) for path in qc_paths]

    status_counts: dict[str, int] = {}
    for frame in frames:
        status_counts[frame["status"]] = status_counts.get(frame["status"], 0) + 1

    blocked_qc = [qc for qc in qcs if qc["status"] != "pass"]
    lines = [
        "# Final QC Report",
        "",
        f"- project_name: {project['project_name']}",
        f"- project_code: {project['project_code']}",
        f"- project_status: {project['status']}",
        f"- total_frames: {len(frames)}",
        f"- total_qc_groups: {len(qcs)}",
        f"- blocked_qc_groups: {len(blocked_qc)}",
        "",
        "## Frame status counts",
    ]
    for key in sorted(status_counts):
        lines.append(f"- {key}: {status_counts[key]}")
    lines.extend(["", "## QC issues"])
    if blocked_qc:
        for qc in blocked_qc:
            lines.append(f"- {qc['frame_group_id']}: {qc.get('notes', '') or qc['status']}")
    else:
        lines.append("- none")

    output.write_text("\n".join(lines) + "\n")
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
