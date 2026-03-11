---
title: "Budget Page Live Discovery"
artifact: SPEC-015
status: Draft
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

# Budget Page Live Discovery

## Problem Statement

The budget page connector currently reads source URLs from `budget-page-sources.yaml` (a static config populated by `--discover`). Per ADR-001, it should fetch and parse spsdme.org/budget27 live on every run, extract document links, filter to supported types (PDF, XLSX, Google Docs/Sheets), and download any that aren't already local. This supersedes SPEC-010.

## External Behavior

**Inputs:**
- Budget page URL: `https://www.spsdme.org/budget27` (hardcoded or minimal config)
- Supported document types: PDF, XLSX, Google Docs, Google Sheets

**Outputs:**
- Downloaded documents in `data/school-board/budget-fy27/documents/`
- Updated `data/school-board/budget-fy27/discovery.jsonl`

**Preconditions:**
- Network access to spsdme.org and docs.google.com
- `beautifulsoup4` installed

**Postconditions:**
- All supported document links from the budget page are downloaded locally
- History file reflects all discovered URLs and download status
- `budget-page-sources.yaml` is no longer read or written
- Unsupported URL types (Google Slides presentations with `pubembed` format) are recorded in history with appropriate error, not retried within backoff window

**Constraints:**
- Page parse uses BeautifulSoup (same as current implementation)
- Google Docs/Sheets export URLs must be constructed correctly (PDF export for Docs, XLSX export for Sheets)
- Google Slides `pubembed` URLs should be detected and skipped with a descriptive log message (known unsupported format)
- Must use `pipeline/discovery.py` for history and backoff (SPEC-013)

## Acceptance Criteria

1. **Given** a fresh run with no local documents, **when** the connector parses the budget page, **then** it downloads all supported document links.

2. **Given** documents already exist locally, **when** the connector runs, **then** it skips existing files and downloads only new ones.

3. **Given** a Google Slides `pubembed` URL, **when** the connector encounters it, **then** it logs a warning, records it in history as unsupported, and does not attempt download.

4. **Given** a network error on one download, **when** the connector continues, **then** it downloads remaining files and exits 0.

5. **Given** the history file records a URL that failed 3 times, **when** the connector runs within the backoff window, **then** it skips the URL silently.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Only targets spsdme.org/budget27 (URL stays hardcoded or in minimal config)
- Does not attempt to render or export Google Slides (known limitation — record and skip)
- Does not change download mechanics for PDFs (direct HTTP) or Google Docs/Sheets (export URL construction)
- `budget-page-sources.yaml` can be deleted after implementation

## Implementation Approach

1. Refactor `scripts/connectors/budget_page.py`:
   - Remove YAML config read/write
   - Main loop: fetch page → parse links → classify type → diff against disk → download missing
   - Add explicit Google Slides detection (skip `pubembed` URLs)
   - Use `DiscoveryHistory` from SPEC-013 for history and backoff
2. Move page URL and type filters to top-level constants
3. Update `scripts/pipeline.py` CONNECTORS dict if needed
4. Delete or gitignore `budget-page-sources.yaml`

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-11 | _pending_ | Initial creation |
