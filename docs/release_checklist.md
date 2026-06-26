# Stage 14 Release Checklist

This is the checklist before moving to Stage 15.

## Repo Package

- [ ] README opens cleanly.
- [ ] `EXTRACT_FIRST.md` warns about Windows path length.
- [ ] `INDEX.md` lists important files.
- [ ] `requirements.txt` is accurate.
- [ ] `.gitignore` blocks outputs, environments, and memory logs.
- [ ] docs are readable.
- [ ] scripts run on Windows.

## Privacy

- [ ] public/private memory folders are empty.
- [ ] outputs folder is empty.
- [ ] no secrets are included.
- [ ] no private identity material appears in public release docs.
- [ ] privacy test passes.

## Function

- [ ] mock backend run succeeds.
- [ ] tests pass.
- [ ] output generation creates Markdown and JSON.
- [ ] evaluation creates scorecard.
- [ ] memory retrieval works only when requested.

## Release Decision

- [ ] license selected.
- [ ] version number chosen.
- [ ] Stage 15 release notes drafted.
