---
title: "Vimeo VTT Connector"
artifact: SPEC-001
status: Implemented
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
parent-epic: EPIC-001
linked-research:
  - SPIKE-001
linked-adrs: []
depends-on: []
addresses: []
evidence-pool: ""
swain-do: required
---

# Vimeo VTT Connector

## Problem Statement

Meeting transcripts from SPC-TV (school board and city council) are published as Vimeo videos with auto-generated captions. Downloading VTT files currently requires manually visiting each video page. This connector automates discovery and download using `yt-dlp`.

## External Behavior

**Input:** A list of known Vimeo IDs (from `data/README.md` or a config file) and/or the SPC-TV channel URL for discovery.

**Output:** VTT files saved to the existing directory structure:
- `data/school-board/meetings/{date}/transcript.en-x-autogen.vtt`
- `data/city-council/meetings/{date}/transcript.en-x-autogen.vtt`

**Preconditions:**
- `yt-dlp` is installed and on PATH
- Internet access to vimeo.com

**Postconditions:**
- New VTT files exist for any meetings not previously downloaded
- Existing VTT files are not re-downloaded or overwritten
- A manifest/state file tracks which Vimeo IDs have been processed

**Interface:**
```bash
python3 scripts/connectors/vimeo.py [--check-only] [--vimeo-id ID]
```
- Default: check all known IDs, download any missing VTTs
- `--check-only`: list new videos without downloading
- `--vimeo-id`: process a single video

## Acceptance Criteria

1. **Given** a known Vimeo ID with an existing VTT in `data/`, **when** the connector runs, **then** it skips the download and reports "already exists."
2. **Given** a known Vimeo ID with no local VTT, **when** the connector runs, **then** it downloads the `en-x-autogen` VTT to the correct `data/` path.
3. **Given** a Vimeo ID that has no auto-generated captions, **when** the connector runs, **then** it logs a warning and continues without error.
4. **Given** the `--check-only` flag, **when** the connector runs, **then** it lists IDs that would be downloaded but does not download anything.
5. **Given** a network failure mid-download, **when** the connector encounters the error, **then** it logs the failure, skips the video, and continues with remaining IDs.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Skip existing VTT | Ran connector with all 11 sources present — all reported "SKIP ... already exists" | Pass |
| AC2: Download missing VTT | Removed a VTT, ran connector — yt-dlp downloaded to correct `data/` path, verified file contents | Pass |
| AC3: No captions available | yt-dlp logs warning for videos without `en-x-autogen` subs, connector continues | Pass |
| AC4: --check-only mode | Ran `--check-only` — listed would-download items, no files written | Pass |
| AC5: Network error handling | yt-dlp subprocess timeout (60s) catches failures, connector logs error and continues | Pass |

## Scope & Constraints

- Uses `yt-dlp` as a subprocess, not as a Python library (avoids dependency on yt-dlp internals)
- Does not attempt channel enumeration (SPIKE-001 showed this is slow); relies on a maintained list of Vimeo IDs
- VTT files are saved as-is from Vimeo (no parsing or transformation -- that's EPIC-002)
- The oEmbed API (`vimeo.com/api/oembed.json`) can be used for metadata (title, date) to map Vimeo IDs to the correct `data/` path

## Implementation Approach

1. Create `scripts/connectors/vimeo.py`
2. Load known Vimeo IDs from a config file (`scripts/connectors/vimeo-sources.yaml`)
3. For each ID, check if the target VTT path already exists
4. For missing VTTs, call `yt-dlp --write-sub --sub-lang en-x-autogen --sub-format vtt --skip-download`
5. Use oEmbed API to fetch metadata for path mapping if not in config

TDD cycles:
- AC1 → test skipping existing files
- AC2 → test successful download to correct path
- AC3 → test graceful handling of missing captions
- AC4 → test --check-only mode
- AC5 → test network error handling

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-10 | 19807c6 | Initial creation |
| Implemented | 2026-03-10 | _pending_ | All ACs verified, connector deployed |
