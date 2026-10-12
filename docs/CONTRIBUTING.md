# Contributing

## Contract changes

When an existing primitive's semantics change, follow this order:

1. Record the contract decision and why it changed.
2. Update or add canonical shared fixtures.
3. Run `python tools/validate_fixtures.py`.
4. Update Android and run Android shared-fixture proof.
5. Update Windows and run Windows shared-fixture proof.
6. Validate/migrate production JSON as required, then release.

Do not modify a platform merely to make a test pass, and do not silently change an existing expected result.

## Versioning

Ordinary fixture additions, new primitives, and compatible argument additions remain in `fixtures/v1` with `schema_version: 1`. Create v2 only for an incompatible change to the shared fixture representation. No v2 is created in this phase.

## Ownership

`recognition-contract` owns the cross-platform behavioral contract and canonical fixtures. Android, Windows, and iOS own their implementations and transparent runners. Implementation details never define the contract.
