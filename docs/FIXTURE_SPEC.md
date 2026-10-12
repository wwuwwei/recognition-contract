# Fixture Specification v1

## Required and optional fields

Required top-level fields are `schema_version` (exactly `1`), non-empty `id`, non-empty `primitive`, object `args`, `input`, and `expected`. `scope` and `metadata` are optional. `expected` requires only `matched: boolean`; score, confidence, debug output, and platform internals are not part of v1.

`input.mode` is exactly `raw_landmarks`. Static fixtures provide `input.frames`; motion fixtures provide `input.history`. Exactly one stream is present, it is non-empty, and history order is canonical temporal order. Runners do not sort, deduplicate, interpolate, or append an implicit current frame.

Each frame has numeric `timestamp_ms` and `hands.left`/`hands.right`. A hand is null or contains `handedness` and `landmarks`. Landmarks contain a `space` and `points`, represented either as a dense array of `[x,y,z]` points or a sparse object keyed by numeric landmark index. A sparse index is the canonical landmark index; an absent key means that point is unspecified, not zero-filled or inferred. The generic schema checks structure only.

`args` is intentionally generic. Primitive-specific vocabulary, region vocabulary, selectors, defaults, and invalid behavior belong to the recognition protocol and primitive capability contract, not this generic schema.

## Naming and directories

`fixtures/v1/` is the stable discovery root. Existing paths and IDs are retained. New fixtures should use modality/primitive directories where compatible with consumers, for example `fixtures/v1/hand/hand_shape/basic_success.json`, `cross_modality/hand_face_position/`, or `motion/point_motion/`.

New IDs should follow `<primitive>/<behavior>/<case>`, such as `point_motion/direction/down`. File names should describe the case; avoid `test1.json`, `case2.json`, and temporary names. Fixture IDs are independent of filesystem paths and globally unique.

## Design rules

Fixtures prove one primary behavior using raw semantic input. Do not encode Kotlin/Python types, evaluator paths, cached producer results, or platform debug fields. Useful future categories include `canonical_success`, `canonical_failure`, `boundary`, `invalid_args`, `selector`, and `missing_data`; motion may additionally use `history`, `track_identity`, `minimum_samples`, and `temporal_boundary` when meaningful.

The canonical palm orientation fixtures demonstrate two distinct primitives: `palm_orientation` is a static current-orientation check represented by `frames`, while `palm_orientation_transition` is a temporal orientation transition represented by ordered `history`. The legacy `palm_orientation` plus `pattern: "transition"` form is not a canonical shared fixture.
