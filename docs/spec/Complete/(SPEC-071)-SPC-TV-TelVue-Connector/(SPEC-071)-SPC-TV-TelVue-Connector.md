---
title: "SPC-TV TelVue Connector"
artifact: SPEC-071
track: implementable
status: Complete
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
  - DESIGN-002
  - JOURNEY-005
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
- `curl` available on PATH
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
| AC1: Discover by title pattern | Live check-only: 8 relevant from 22 total | Pass |
| AC2: Extract VTT captions | Downloaded 3 VTTs via closed_captions endpoint (454KB, 375KB, 368KB) | Pass |
| AC3: Skip existing (disk-diff) | 5 meetings correctly skipped — transcripts already on disk from Vimeo | Pass |
| AC4: Backoff gate | 3 URLs entered backoff after initial yt-dlp failures; respected on retry | Pass |
| AC5: --check-only mode | Dry run listed 3 would-download, 5 skipped, 0 failed | Pass |
| AC6: Correct routing | BoE → school-board, CC → city-council, CC Workshop → city-council | Pass |

## Scope & Constraints

- **In scope:** Discovery from TelVue VOD listing, VTT extraction via closed_captions endpoint, DiscoveryHistory integration
- **Out of scope:** TelVue API authentication (VOD player is public), transcript normalization (handled by existing SPEC-004 pipeline), non-meeting content on SPC-TV
- **TelVue URL pattern:** `https://videoplayer.telvue.com/player/NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq/media/{media_id}`
- **Title patterns to match:** "South Portland Board of Education", "South Portland City Council", "South Portland City Council Workshop"

## Implementation Approach

Implemented at `scripts/connectors/telvue.py` following the structure of `vimeo.py`:

1. **Discovery:** Fetch the TelVue VOD listing page via curl. Parse video entries (title, media ID, duration) using regex against the HTML. The page is server-rendered — no JS execution needed.

2. **Filtering:** Match titles against known patterns (`Board of Education`, `City Council`, `Budget Workshop`). Infer meeting type and date from title text (e.g., "South Portland Board of Education - March 30 2026" → school-board, 2026-03-30). Handles both "March 30 2026" and "February 17, 2026" (comma variant).

3. **Diff against disk:** Check `data/{type}/meetings/{date}/transcript.en-x-autogen.vtt` — skip if exists.

4. **Download:** Extract caption URL from the TelVue media page HTML. The JW Player embeds a `tracks` array with a `/closed_captions/{base64_path}?sha={sig}` relative URL. Download the VTT directly via curl. No yt-dlp needed — TelVue serves captions as separate VTT files at a dedicated endpoint, not embedded in the HLS stream (the m3u8 declares `CLOSED-CAPTIONS=NONE`).

5. **History tracking:** Records attempts in the same `discovery.jsonl` files as the Vimeo connector, using the TelVue media URL as the key.

6. **Pipeline integration:** Registered as `telvue` connector in `scripts/pipeline.py` with the same watch dirs as Vimeo.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-31 | 349d798 | Initial creation — user-requested |
| Complete | 2026-03-31 | 3415f86 | Implemented, tested (31 unit tests), live-verified (3 transcripts downloaded) |
