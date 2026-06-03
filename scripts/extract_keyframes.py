#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


DEFAULT_POINTS = [0, 20, 40, 60, 80, 100]


def ffprobe_duration(video_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def clamp_time(time_sec: float, duration: float, fps: int) -> float:
    if duration <= 0:
        return 0.0
    frame_epsilon = 1.0 / max(fps, 1)
    max_time = max(duration - frame_epsilon, 0.0)
    return min(max(time_sec, 0.0), max_time)


def sec_to_tc(seconds: float, fps: int) -> str:
    total_frames = round(seconds * fps)
    hh = total_frames // (3600 * fps)
    mm = (total_frames // (60 * fps)) % 60
    ss = (total_frames // fps) % 60
    ff = total_frames % fps
    return f"{hh:02d}-{mm:02d}-{ss:02d}-{ff:02d}"


def extract_frame(video_path: Path, time_sec: float, out_path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(time_sec),
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            str(out_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def build_contact_sheet(images: list[Path], output_path: Path) -> None:
    opened = [Image.open(p).convert("RGB") for p in images]
    thumbs = []
    for img in opened:
        thumb = img.copy()
        thumb.thumbnail((320, 180))
        thumbs.append(thumb)
    cols = 3
    rows = math.ceil(len(thumbs) / cols)
    canvas = Image.new("RGB", (cols * 320, rows * 180), color=(20, 20, 20))
    draw = ImageDraw.Draw(canvas)
    for idx, thumb in enumerate(thumbs):
        x = (idx % cols) * 320
        y = (idx // cols) * 180
        canvas.paste(thumb, (x, y))
        draw.text((x + 8, y + 8), images[idx].stem, fill=(255, 255, 255))
    canvas.save(output_path)


def frame_type_for_index(index: int, total: int) -> str:
    if index == 0:
        return "anchor"
    if index == total - 1:
        return "transition"
    return "motion"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract AI+liveaction keyframes.")
    parser.add_argument("video_path")
    parser.add_argument("output_dir")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--percentages", default="0,20,40,60,80,100")
    parser.add_argument("--contact-sheet", default=None)
    args = parser.parse_args()

    video_path = Path(args.video_path).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    percentages = [int(p.strip()) for p in args.percentages.split(",") if p.strip()]
    if not percentages:
        percentages = DEFAULT_POINTS

    duration = ffprobe_duration(video_path)
    frames = []
    image_paths = []
    for idx, pct in enumerate(percentages, start=1):
        raw_time_sec = duration * (pct / 100.0)
        time_sec = clamp_time(raw_time_sec, duration, args.fps)
        tc = sec_to_tc(time_sec, args.fps)
        frame_id = f"frame_{idx:04d}_tc-{tc}"
        out_path = output_dir / f"{frame_id}.png"
        extract_frame(video_path, time_sec, out_path)
        frame_type = frame_type_for_index(idx - 1, len(percentages))
        frames.append(
            {
                "frame_id": frame_id,
                "timecode": tc.replace("-", ":"),
                "frame_type": frame_type,
                "image_path": str(out_path),
                "status": "extracted",
            }
        )
        image_paths.append(out_path)

    contact_sheet = Path(args.contact_sheet).expanduser().resolve() if args.contact_sheet else output_dir.parent / "contact_sheet.jpg"
    build_contact_sheet(image_paths, contact_sheet)

    print(json.dumps({"frames": frames, "contact_sheet": str(contact_sheet)}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
