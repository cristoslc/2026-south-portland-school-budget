---
id: SPEC-031
title: Evidence Remediation Post Pool Migration
type: bug
parent-initiative: ""
parent-epic: ""
status: Proposed
priority-weight: high
created: 2026-03-24
last-updated: 2026-03-24
---

# SPEC-031: Evidence Remediation Post Pool Migration

## Problem

Between the `docs/evidence-pools/` deletion (commit `5fe28f2`, ~2026-03-14) and the path fix (SPEC-029, 2026-03-24), the pipeline downloaded evidence but could not normalize or bundle it. Evidence scraped during this window needs to be:

1. Identified — which downloads happened after the deletion?
2. Normalized — the `pipeline.py normalize` subcommand was run in SPEC-029 and re-normalized all 46 sources
3. Bundled — `bundle_meetings.py` needs to pick up any new normalized sources and affiliate them with meetings
4. Interpreted — any new bundles or updated bundles need to run through the interpretation pipeline
5. Folded + briefed — downstream cumulative folds and briefs need regeneration if source material changed

## Remediation Steps

### Step 1: Re-bundle
```bash
python3 scripts/bundle_meetings.py
```
Check if any bundles gained new sources (especially `2026-03-23-school-board` if it should exist).

### Step 2: Identify new/changed bundles
Compare bundle manifests before and after re-bundling. Any meeting with new sources needs reinterpretation.

### Step 3: Re-interpret changed meetings
```bash
python3 scripts/poll_interpret.py --dry-run
```
This will detect interpretation gaps. Run without `--dry-run` for affected meetings.

### Step 4: Downstream fold + brief
The regular Track 2 cron (`track2-cron.sh`) will handle fold and brief regeneration once interpretations are current.

## Acceptance Criteria

- [ ] `bundle_meetings.py` runs clean with `docs/troves/` paths
- [ ] Any meeting with new evidence sources has been reinterpreted
- [ ] No evidence files from the broken window remain unprocessed
- [ ] `poll_interpret.py --dry-run` shows 0 gaps

## Lifecycle

| Phase | Date | Commit |
|-------|------|--------|
| Proposed | 2026-03-24 | |
