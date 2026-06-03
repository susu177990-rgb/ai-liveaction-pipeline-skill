#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema


def load_schema(schema_path: Path) -> dict:
    return json.loads(schema_path.read_text())


def validate_file(schema: dict, payload_path: Path) -> list[str]:
    errors = []
    try:
        payload = json.loads(payload_path.read_text())
        jsonschema.validate(payload, schema)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{payload_path}: {exc}")
    return errors


def check_layer_paths(frame_payload: dict, payload_path: Path) -> list[str]:
    errors = []
    for layer in frame_payload.get("required_layers", []):
        path = frame_payload.get("layer_paths", {}).get(layer)
        if not path:
            errors.append(f"{payload_path}: missing layer path for {layer}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI+liveaction project manifests.")
    parser.add_argument("project_root")
    parser.add_argument("--strict-paths", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    schemas_dir = Path(__file__).resolve().parent.parent / "schemas"
    project_schema = load_schema(schemas_dir / "project.schema.json")
    frame_schema = load_schema(schemas_dir / "frame.schema.json")
    scene_match_schema = load_schema(schemas_dir / "scene-match.schema.json")
    qc_schema = load_schema(schemas_dir / "qc.schema.json")
    asset_schema = load_schema(schemas_dir / "asset.schema.json")

    errors: list[str] = []
    project_manifest = root / "manifests" / "project.json"
    errors.extend(validate_file(project_schema, project_manifest))

    for path in sorted((root / "manifests" / "frames").glob("*.json")):
        errors.extend(validate_file(frame_schema, path))
        payload = json.loads(path.read_text())
        errors.extend(check_layer_paths(payload, path))
        if args.strict_paths and not Path(payload["image_path"]).exists():
            errors.append(f"{path}: image path does not exist")

    for path in sorted((root / "manifests" / "scene_match").glob("*.json")):
        errors.extend(validate_file(scene_match_schema, path))

    for path in sorted((root / "manifests" / "qc").glob("*.json")):
        errors.extend(validate_file(qc_schema, path))

    for path in sorted((root / "manifests" / "assets").glob("*.json")):
        errors.extend(validate_file(asset_schema, path))

    if errors:
        print("\n".join(errors))
        return 1
    print("Project manifests are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
