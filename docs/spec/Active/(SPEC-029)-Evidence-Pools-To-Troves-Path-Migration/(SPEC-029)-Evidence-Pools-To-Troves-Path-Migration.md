---
id: SPEC-029
title: Evidence-Pools to Troves Path Migration
type: bug
parent-initiative: ""
parent-epic: ""
status: Active
priority-weight: high
created: 2026-03-24
last-updated: 2026-03-24
---

# SPEC-029: Evidence-Pools to Troves Path Migration

## Problem

Commit `5fe28f2` migrated evidence pools from `docs/evidence-pools/` to `docs/troves/` but left ~55 files referencing the old path. The pipeline normalizer is broken — new evidence downloads succeed but normalization fails because it writes to the deleted directory. Bundle manifests, tests, and documentation all reference the stale path.

## Scope

Mechanical path migration: `docs/evidence-pools/` → `docs/troves/` across:

1. **Pipeline scripts** (4 files) — `pipeline.py`, `bundle_meetings.py`, `build_evidence_pool.py`, `add_key_points.py`
2. **Pipeline utilities** (1 file) — `pipeline/source_completeness.py`
3. **Bundle manifests** (26 files) — `data/interpretation/bundles/*/manifest.yaml`
4. **Tests** (5 files) — `test_source_completeness.py`, `test_inter_meeting_schema.py`, `test_bundle_schema.py`, `test_bundle_layout.py`, `test_validate_interpretation.py`
5. **Schema docs** (2 files) — `data/interpretation/schema/`
6. **README + artifacts** (~16 files) — `README.md`, vision/epic/spec/journey/runbook docs

## Acceptance Criteria

- [ ] `python3 scripts/pipeline.py run --stage` normalizes new PDFs into `docs/troves/`
- [ ] `python3 scripts/bundle_meetings.py` loads manifests from `docs/troves/`
- [ ] All tests pass: `python3 -m pytest tests/`
- [ ] Zero occurrences of `evidence-pools` in code files (scripts/, pipeline/, tests/, .github/)
- [ ] Bundle manifest `normalized_path` fields point to `docs/troves/`
- [ ] README links resolve

## Lifecycle

| Phase | Date | Commit |
|-------|------|--------|
| Active | 2026-03-24 | |
