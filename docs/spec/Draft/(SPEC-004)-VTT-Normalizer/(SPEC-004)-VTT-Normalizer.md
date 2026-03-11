---
title: "VTT-to-Markdown Normalizer"
artifact: SPEC-004
status: Draft
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
parent-epic: EPIC-002
linked-research:
  - SPIKE-003
linked-adrs: []
depends-on: []
addresses: []
evidence-pool: ""
swain-do: required
---

# VTT-to-Markdown Normalizer

## Problem Statement

The existing `build_evidence_pool.py` has correct VTT-to-markdown logic (`process_vtt()`) but hardcodes absolute paths, source lists, and pool identifiers. Per SPIKE-003, the processing functions are sound but need parameterization to work as a reusable pipeline component. This spec covers extracting and parameterizing the VTT processing path so any VTT file can be converted to evidence pool source markdown without editing the script.

## External Behavior

**Input:**
- Path to a VTT file (e.g., `data/school-board/meetings/2026-01-12/transcript.en-x-autogen.vtt`)
- Metadata: title, date, source URL or Vimeo ID

**Output:**
- A markdown file matching the evidence pool source format:
  - YAML frontmatter with `source-id`, `title`, `type: media`, `path`, `fetched`, `hash`, `duration`, `speakers`, `notes`
  - H1 title, duration line, source line
  - `## Transcript` section with `**[MM:SS]**` timestamped paragraphs
- Updated `manifest.yaml` entry for the target evidence pool

**Preconditions:**
- `parse_vtt.py` is available (used as-is per SPIKE-003)
- Target evidence pool directory exists

**Constraints:**
- Must produce output byte-identical in structure to existing VTT-sourced evidence pool files (e.g., `school-board-budget-meetings/sources/001-regular-meeting-2026-01-12.md`)
- SHA-256 hash of the source VTT file must be computed and stored in frontmatter
- `source-id` must be auto-assigned as the next sequential ID in the target pool

## Acceptance Criteria

1. **Given** a VTT file path and metadata, **when** the normalizer runs, **then** it produces a markdown file with valid YAML frontmatter containing all required fields (`source-id`, `title`, `type`, `path`, `fetched`, `hash`, `duration`).
2. **Given** a VTT file, **when** the normalizer runs, **then** the transcript body contains merged segments with `**[MM:SS]**` timestamps matching `parse_vtt.py` output.
3. **Given** an existing evidence pool with N sources, **when** a new VTT is normalized into it, **then** `source-id` is assigned as `N+1` (zero-padded to 3 digits).
4. **Given** a successful normalization, **when** the output is written, **then** `manifest.yaml` is updated with the new source entry.
5. **Given** the same VTT file run twice, **when** the hash matches an existing source, **then** the normalizer skips or warns (no duplicate sources).

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

**In scope:**
- Refactoring `process_vtt()` from `build_evidence_pool.py` into a parameterized function/module
- CLI entry point accepting VTT path + metadata arguments
- Manifest update logic
- Duplicate detection via SHA-256 hash

**Out of scope:**
- VTT discovery or download (EPIC-001 / SPEC-001)
- Key point extraction (remains manual)
- Batch processing of multiple VTTs in one invocation (future enhancement)

## Implementation Approach

1. Extract `process_vtt()` and supporting functions from `build_evidence_pool.py` into `pipeline/normalize_vtt.py`
2. Parameterize: replace hardcoded paths with function arguments
3. Add CLI wrapper (argparse) for standalone use
4. Add hash computation and duplicate check against existing pool sources
5. Add manifest update logic (read existing `manifest.yaml`, append entry, write back)
6. Test against existing VTT files, diff output against hand-built sources

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-10 | _pending_ | Initial creation |
