"""Validate recognition-contract v1 fixtures without implementing recognition semantics."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "v1"
SCHEMA = ROOT / "schema" / "fixture.schema.v1.json"
PROHIBITED = {"platform", "android", "windows", "ios", "kotlin", "python", "dto", "cached_features"}


def fail(path: Path, message: str) -> None:
    raise ValueError(f"{path.relative_to(ROOT)}: {message}")


def validate_fixture(path: Path, data: dict) -> tuple[str, str]:
    if not isinstance(data, dict): fail(path, "root must be an object")
    required = {"schema_version", "id", "primitive", "args", "input", "expected"}
    missing = required - data.keys()
    if missing: fail(path, f"missing required fields: {sorted(missing)}")
    if data["schema_version"] != 1: fail(path, "schema_version must be 1")
    for key in ("id", "primitive"):
        if not isinstance(data[key], str) or not data[key].strip(): fail(path, f"{key} must be non-empty")
    if not isinstance(data["args"], dict): fail(path, "args must be an object")
    if not isinstance(data["expected"], dict) or not isinstance(data["expected"].get("matched"), bool):
        fail(path, "expected.matched must be boolean")
    inp = data["input"]
    if not isinstance(inp, dict) or inp.get("mode") != "raw_landmarks": fail(path, "input.mode must be raw_landmarks")
    streams = [k for k in ("frames", "history") if k in inp]
    if len(streams) != 1 or not isinstance(inp[streams[0]], list) or not inp[streams[0]]: fail(path, "input must contain exactly one non-empty frames/history array")
    for frame in inp[streams[0]]:
        if not isinstance(frame, dict) or not isinstance(frame.get("hands"), dict): fail(path, "invalid frame")
        if not isinstance(frame.get("timestamp_ms"), (int, float)): fail(path, "frame.timestamp_ms must be numeric")
        for side in ("left", "right"):
            hand = frame["hands"].get(side)
            if hand is not None and (not isinstance(hand, dict) or not isinstance(hand.get("landmarks"), dict)): fail(path, f"invalid {side} hand")
    text = json.dumps(data).lower()
    for token in PROHIBITED:
        if re.search(rf"\b{re.escape(token)}\b", text): fail(path, f"platform-specific key/value prohibited: {token}")
    return data["id"], "history" if "history" in inp else "static"


def main() -> int:
    files = sorted(FIXTURES.rglob("*.json"))
    ids: dict[str, Path] = {}
    primitives: set[str] = set()
    counts = {"static": 0, "history": 0}
    try:
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        for path in files:
            data = json.loads(path.read_text(encoding="utf-8"))
            fixture_id, category = validate_fixture(path, data)
            if fixture_id in ids: fail(path, f"duplicate fixture id (also {ids[fixture_id]})")
            ids[fixture_id] = path
            primitives.add(data["primitive"])
            counts[category] += 1
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"fixtures: {len(files)}")
    print(f"primitives: {len(primitives)} ({', '.join(sorted(primitives))})")
    print(f"static: {counts['static']}")
    print(f"history: {counts['history']}")
    print(f"unique_ids: {len(ids)}")
    print("schema_validation: PASS")
    print("result: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
