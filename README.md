# Cross-Platform Recognition Behavioral Contract

`recognition-contract` is the canonical, platform-neutral contract repository for Android, Windows, and future iOS recognition implementations. It owns the fixture schema, canonical golden fixtures, fixture IDs, cross-platform behavioral expectations, documentation, and validation tools.

It does not own Android/Python DTOs, Kotlin classes, MediaPipe or registry implementations, UI/camera pipelines, cached derived features, or platform compatibility adapters.

```text
recognition-contract (schema + fixtures)
          |             |             |
       Android       Windows         iOS
        runner        runner        runner
          |             |             |
   production path production path production path
```

## Current contract

- Canonical root: `fixtures/v1/`
- Fixture representation: `schema_version: 1`, `input.mode: raw_landmarks`
- Static input uses `input.frames`; motion input uses `input.history` in canonical order.
- Expected behavior currently freezes only `expected.matched: boolean`.
- `region` is a protocol field and must be a non-empty array of strings; `region: ["A", "B"]` means A OR B.

The three existing fixture IDs remain unchanged for evidence compatibility:

- `post_p2.1/hand_shape/static_pipeline`
- `post_p2.1/hand_face_position/static_current_frame`
- `post_p2.4/point_motion/left_wrist_down`

## Runner boundary

Runners may parse JSON, validate/decode fixtures, construct points and platform DTOs, and adapt representation at the platform boundary. They must not coerce arguments, translate aliases, normalize regions/selectors/targets, rewrite thresholds, sort/deduplicate history, append frames, or special-case expected results. Representation adaptation is allowed; semantic adaptation is forbidden. If a fixture cannot be interpreted directly, the runner fails.

## Validation

Run `python tools/validate_fixtures.py`. The validator recursively discovers `fixtures/v1/**/*.json`, checks the v1 structure, landmark basics, unique IDs, supported version, and prohibited platform-specific fields. JSON Schema is in `schema/fixture.schema.v1.json`; primitive vocabulary and semantics remain outside the generic schema.

## Ownership and change policy

The contract and golden fixtures define behavior; implementations conform to them. For a semantic change: decide and document the contract change, update/add canonical fixtures, validate, update Android and prove it, update Windows and prove it, then migrate/validate production JSON and release. Never silently change an expected result to make one platform pass.

See [docs/FIXTURE_SPEC.md](docs/FIXTURE_SPEC.md), [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md), and [docs/NEW_PRIMITIVE_CHECKLIST.md](docs/NEW_PRIMITIVE_CHECKLIST.md).
