---
title: "SPC-TV TelVue Connector"
artifact: SPEC-071
track: implementable
status: Active
author: operator
created: 2026-03-31
last-updated: 2026-03-31
type: feature
parent-epic: ""
parent-initiative: INITIATIVE-002
linked-artifacts:
  - SPEC-001
  - SPEC-014
  - SPEC-004
depends-on-artifacts: []
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# SPC-TV TelVue Connector

## Problem Statement

Meeting recordings are hosted on SPC-TV (South Portland Community Television) via the TelVue platform, not just Vimeo. The existing Vimeo connector (`scripts/connectors/vimeo.py`) only discovers and downloads from the Vimeo channel, missing recordings that appear on SPC-TV first or exclusively. The March 30, 2026 Board of Education recording was available on SPC-TV hours after the meeting but had no Vimeo counterpart yet.

SPC-TV hosts all South Portland public meetings — Board of Education, City Council, Planning Board, Comprehensive Plan Committee, and others — making it the most comprehensive single source for meeting video.

## Desired Outcomes

The evidence pipeline automatically discovers and ingests meeting recordings from SPC-TV's TelVue VOD player, producing VTT transcripts that feed into the existing normalization pipeline. Analysts and automated trove-extension workflows get meeting transcripts faster, without manual URL hunting.

## External Behavior

**Inputs:**
- SPC-TV TelVue VOD player API/page at `https://videoplayer.telvue.com/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/videos`
- Existing `discovery.jsonl` files for school-board and city-council meetings

**Outputs:**
- VTT transcript files at `data/{meeting-type}/meetings/{date}/transcript.en-x-autogen.vtt`
- Updated `discovery.jsonl` entries with TelVue media URLs

**Preconditions:**
- `yt-dlp` available on PATH (for transcript extraction from TelVue stream URLs)
- `pipeline.discovery.DiscoveryHistory` importable

**Constraints:**
- Must follow the same `DiscoveryHistory` pattern as `vimeo.py` (JSONL tracking, exponential backoff)
- Must coexist with the Vimeo connector — same discovery.jsonl, no conflicts on overlapping meetings
- Must support `--check-only` dry-run mode

## Acceptance Criteria

1. **Given** the SPC-TV VOD page has a new Board of Education recording, **when** the connector runs, **then** it discovers the video by title pattern and records it in `data/school-board/meetings/discovery.jsonl`.

2. **Given** a discovered SPC-TV video with no local transcript, **when** the connector downloads, **then** it extracts VTT captions to the standard path (`data/{type}/meetings/{date}/transcript.en-x-autogen.vtt`).

3. **Given** a meeting already has a transcript from Vimeo, **when** the TelVue connector finds the same meeting, **then** it skips download (disk-diff gate).

4. **Given** a previous download attempt failed, **when** the connector runs within the backoff window, **then** it skips the attempt (backoff gate via `DiscoveryHistory`).

5. **Given** `--check-only` flag, **when** the connector runs, **then** it lists what would be downloaded without downloading.

6. **Given** the TelVue page lists videos for City Council, Planning Board, and Board of Education, **when** the connector runs, **then** it correctly routes each to the appropriate data directory based on title matching.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- **In scope:** Discovery from TelVue VOD listing, VTT extraction via yt-dlp, DiscoveryHistory integration
- **Out of scope:** TelVue API authentication (VOD player is public), transcript normalization (handled by existing SPEC-004 pipeline), non-meeting content on SPC-TV
- **TelVue URL pattern:** `https://videoplayer.telvue.com/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/media/{media_id}`
- **Title patterns to match:** "South Portland Board of Education", "South Portland City Council", "South Portland City Council Workshop"

## Implementation Approach

Follow the structure of `scripts/connectors/vimeo.py` closely:

1. **Discovery:** Fetch the TelVue VOD listing page, parse video entries (title, media ID, duration, date added). The TelVue player is JS-rendered — investigate whether yt-dlp can enumerate the channel or if we need to scrape the page directly.

2. **Filtering:** Match titles against known meeting patterns. Infer meeting type and date from title text (e.g., "South Portland Board of Education - March 30 2026" → school-board, 2026-03-30).

3. **Diff against disk:** Check `data/{type}/meetings/{date}/transcript.en-x-autogen.vtt` — skip if exists.

4. **Download:** Use yt-dlp to extract VTT from the TelVue stream URL. Fall back to direct stream download + whisper if yt-dlp can't extract captions from TelVue.

5. **History tracking:** Record attempts in the same `discovery.jsonl` files as the Vimeo connector, using the TelVue URL as the key.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-31 | -- | Initial creation — user-requested |
