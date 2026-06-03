# FFmpeg Guide

Use `ffmpeg` and `ffprobe` as the default deterministic layer for:

- metadata probing
- frame extraction
- contact sheet assembly
- ratio-safe preview exports

## Baseline commands

Probe:

```bash
ffprobe -v error -print_format json -show_format -show_streams input.mp4
```

Frame extraction:

```bash
ffmpeg -i input.mp4 -vf "select='eq(n,0)+eq(n,48)+eq(n,96)'" -vsync vfr frame_%04d.png
```

Low-density scene review:

```bash
ffmpeg -i input.mp4 -vf fps=1 preview_%04d.jpg
```

This skill's Python scripts should wrap these commands rather than re-implement video parsing manually.
