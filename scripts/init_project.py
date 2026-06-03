#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIRS = [
    "00_brief",
    "01_source_video",
    "02_keyframes/frames",
    "02_keyframes/diagnosis",
    "03_assets/subject",
    "03_assets/scene",
    "03_assets/prop",
    "03_assets/style",
    "04_scene_library",
    "05_preprocess/mask",
    "05_preprocess/face",
    "05_preprocess/outfit",
    "05_preprocess/hand",
    "05_preprocess/prop",
    "05_preprocess/depth",
    "05_preprocess/pose",
    "05_preprocess/edge",
    "05_preprocess/contact",
    "06_empty_plate",
    "07_fusion",
    "08_qc",
    "09_delivery",
    "manifests/frames",
    "manifests/assets",
    "manifests/scene_match",
    "manifests/qc"
]


def slugify(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "project"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an AI+liveaction project scaffold.")
    parser.add_argument("project_root", help="Directory to create or update")
    parser.add_argument("--project-name", required=True, help="Human-readable project name")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--platform", default="unknown")
    parser.add_argument("--use-case", default="ai-liveaction-conversion")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    for rel in PROJECT_DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)

    manifest = {
        "project_name": args.project_name,
        "project_code": slugify(args.project_name),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "intake",
        "delivery_target": {
            "aspect_ratio": args.aspect_ratio,
            "platform": args.platform,
            "use_case": args.use_case,
            "notes": ""
        },
        "source_video": {
            "path": "",
            "duration_seconds": None,
            "frame_rate": None,
            "resolution": None,
            "codec": None
        },
        "assets": {
            "subject": [],
            "scene": [],
            "prop": [],
            "style": []
        },
        "paths": {
            "brief_dir": str(root / "00_brief"),
            "source_video_dir": str(root / "01_source_video"),
            "keyframes_dir": str(root / "02_keyframes"),
            "assets_dir": str(root / "03_assets"),
            "scene_library_dir": str(root / "04_scene_library"),
            "preprocess_dir": str(root / "05_preprocess"),
            "empty_plate_dir": str(root / "06_empty_plate"),
            "fusion_dir": str(root / "07_fusion"),
            "qc_dir": str(root / "08_qc"),
            "delivery_dir": str(root / "09_delivery"),
            "manifests_dir": str(root / "manifests")
        },
        "notes": ""
    }

    (root / "manifests" / "project.json").write_text(json.dumps(manifest, ensure_ascii=True, indent=2) + "\n")
    brief = root / "00_brief" / "project-brief.md"
    if not brief.exists():
        brief.write_text("# Project Brief\n\n- project_name: {}\n".format(args.project_name))
    print(str(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
