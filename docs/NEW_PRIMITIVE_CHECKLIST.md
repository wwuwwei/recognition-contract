# New Primitive Checklist

- [ ] Define primitive name, modality, temporal semantics, args, vocabulary, defaults, invalid behavior, selector behavior, missing-data behavior, and threshold boundaries.
- [ ] Add the smallest useful shared golden fixtures: success, failure, important boundary, and invalid args; add selector/history cases when applicable.
- [ ] Run `python tools/validate_fixtures.py`.
- [ ] Implement the Android production path and run Android shared fixtures.
- [ ] Implement the Windows production path and run Windows shared fixtures.
- [ ] Implement a future iOS path and run the same shared fixtures.
- [ ] Validate production JSON and complete release review.

Runners may perform representation adaptation only. They must not perform semantic compatibility conversion.
