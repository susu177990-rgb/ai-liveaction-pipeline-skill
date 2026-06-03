#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run_ffprobe(video_path: Path) -> dict:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe video metadata with ffprobe.")
    parser.add_argument("video_path")
    parser.add_argument("--output")
    args = parser.parse_args()

    video_path = Path(args.video_path).expanduser().resolve()
    data = run_ffprobe(video_path)
    video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    rate_raw = video_stream.get("avg_frame_rate", "0/1")
    num, den = rate_raw.split("/")
    frame_rate = round(float(num) / float(den), 4) if float(den) else 0.0

    payload = {
        "path": str(video_path),
        "duration_seconds": float(data.get("format", {}).get("duration", 0.0)),
        "frame_rate": frame_rate,
        "resolution": f"{video_stream.get('width', 0)}x{video_stream.get('height', 0)}",
        "codec": video_stream.get("codec_name"),
        "pixel_format": video_stream.get("pix_fmt"),
        "display_aspect_ratio": video_stream.get("display_aspect_ratio"),
        "color_space": video_stream.get("color_space"),
    }

    text = json.dumps(payload, ensure_ascii=True, indent=2) + "\n"
    if args.output:
        Path(args.output).expanduser().resolve().write_text(text)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
