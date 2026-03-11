---
title: "Vimeo Live Discovery"
artifact: SPEC-014
status: Implemented
author: cristos
created: 2026-03-11
last-updated: 2026-03-11
parent-epic: EPIC-006
linked-research: []
linked-adrs:
  - ADR-001
depends-on:
  - SPEC-013
addresses: []
evidence-pool: ""
swain-do: required
---

# Vimeo Live Discovery

## Problem Statement

The Vimeo connector currently reads video IDs from `vimeo-sources.yaml` (a static config populated by `--discover`). Per ADR-001, it should enumerate the SPC-TV channel live on every run, filter to FY27-relevant school board and city council meetings, and download VTTs for any videos not already in the local data directory. This supersedes SPEC-009.

## External Behavior

**Inputs:**
- SPC-TV Vimeo channel URL (hardcoded or in a minimal static config)
- Filter criteria: title prefixes (`spboe_`, `spcc_`, `spccws_`), date after `2025-12-01`

**Outputs:**
- VTT files downloaded for newly discovered videos
- Updated `data/school-board/meetings/discovery.jsonl` and `data/city-council/meetings/discovery.jsonl`

**Preconditions:**
- `yt-dlp` installed
- Network access to Vimeo

**Postconditions:**
- All FY27-relevant SPC-TV videos with auto-generated captions have VTTs in the local data directory
- History file reflects all discovered video URLs and download status
- `vimeo-sources.yaml` is no longer read or written

**Constraints:**
- Channel enumeration uses `yt-dlp --flat-playlist --dump-json` (one API call)
- Title-based date extraction via regex (SPC-TV convention: `spboe_YYYYMMDD`)
- Must use `pipeline/discovery.py` for history and backoff (SPEC-013)

## Acceptance Criteria

1. **Given** a fresh run with no local VTTs, **when** the connector enumerates the SPC-TV channel, **then** it downloads VTTs for all FY27-relevant videos.

2. **Given** VTTs already exist for some videos, **when** the connector runs, **then** it skips existing videos and downloads only new ones.

3. **Given** `vimeo-sources.yaml` exists in the repo, **when** the connector runs, **then** it ignores the file entirely (does not read from it).

4. **Given** a video without auto-generated captions, **when** the connector tries to download, **then** it logs a warning, records the failure in history, and continues.

5. **Given** the connector completes with some download failures, **when** it exits, **then** exit code is 0.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Only targets the SPC-TV Vimeo channel (channel ID stays hardcoded or in a tiny filter config)
- Filter prefixes and date cutoff may be parameterized for reuse in other fiscal years
- Does not change the download mechanics (still `yt-dlp --write-sub`)
- `vimeo-sources.yaml` can be deleted after this is implemented (or kept as historical reference)

## Implementation Approach

1. Refactor `scripts/connectors/vimeo.py`:
   - Remove YAML config read/write
   - Main loop: enumerate channel → filter → diff against disk → download missing
   - Use `DiscoveryHistory` from SPEC-013 for history and backoff
2. Move filter criteria (prefixes, date cutoff) to top-level constants or a small config section
3. Update `scripts/pipeline.py` CONNECTORS dict if needed (remove `supports_discover`)
4. Delete or gitignore `vimeo-sources.yaml`

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-11 | d923074 | Initial creation |
| Implemented | 2026-03-11 | 6c1020c | Merged via PRs #5, #6, #7 |
