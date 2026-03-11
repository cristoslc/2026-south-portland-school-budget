---
title: "Live Discovery Connector Model"
artifact: SPEC-013
status: Implemented
author: cristos
created: 2026-03-11
last-updated: 2026-03-11
parent-epic: EPIC-006
linked-research: []
linked-adrs:
  - ADR-001
depends-on: []
addresses: []
evidence-pool: ""
swain-do: required
---

# Live Discovery Connector Model

## Problem Statement

The current connectors use a two-phase model: discovery writes URLs to a YAML config, download reads from that config. This creates stale config failures (BUG-001) and unnecessary complexity. Per ADR-001, connectors should enumerate sources live on every run. This spec defines the shared pattern that SPEC-014 and SPEC-015 implement per-connector.

## External Behavior

**Inputs:**
- Source endpoint (Vimeo channel URL, budget page URL)
- Filter criteria (title prefixes, date ranges, document types)
- Local data directory to diff against

**Outputs:**
- Downloaded files for newly discovered resources
- Updated `discovery.jsonl` history file

**Preconditions:**
- Network access to source endpoints
- Local data directory exists

**Postconditions:**
- All available FY27-relevant resources that aren't already local have been downloaded (subject to backoff)
- History file updated with discovery timestamps and attempt results
- Connector exits 0 unless a fatal error occurs (individual download failures are non-fatal)

**Constraints:**
- Must be safe for hourly execution (minimal API load, backoff for failures)
- History file must be append-friendly (JSONL, one record per URL update)
- Download failures must not cause non-zero exit when other downloads succeed

## Acceptance Criteria

1. **Given** a connector runs, **when** it enumerates source resources, **then** it filters to FY27-relevant content and downloads only resources not already in the local data directory.

2. **Given** a URL that returned 404 on the last attempt, **when** the connector runs again within the backoff window, **then** the URL is skipped with a debug-level log message.

3. **Given** a URL that failed 3 times, **when** the backoff window expires (8 hours), **then** the URL is retried.

4. **Given** 13 of 14 downloads succeed and 1 fails, **when** the connector completes, **then** it exits 0 (not 1) and logs the failure as a warning.

5. **Given** the history file exists, **when** an external process reads it, **then** it can determine all discovered URLs, their status, and when they were last attempted.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- History file format: JSONL at `data/<connector>/discovery.jsonl`
- Each line: `{"url": "...", "label": "...", "first_seen": "...", "last_attempt": "...", "status": "ok|failed|skipped", "fail_count": N, "last_error": "..."}`
- Backoff formula: skip if `last_attempt + min(2^fail_count, 48) hours > now`
- On successful download, reset fail_count to 0 and status to "ok"
- Connectors share a `pipeline/discovery.py` module with the history read/write/backoff logic
- The `--discover` flag is removed — discovery is the default behavior
- The `--check-only` flag remains for dry runs (enumerate and log, don't download)

## Implementation Approach

1. Create `pipeline/discovery.py` with:
   - `DiscoveryHistory` class: read/write/query JSONL history
   - `should_attempt(url)` method implementing backoff logic
   - `record_attempt(url, status, error=None)` method
   - `discovered_urls()` method for external consumers
2. Update `scripts/pipeline.py` exit code logic: exit 0 on partial success, exit 1 only on total failure
3. Remove `--discover` flag from pipeline runner (discovery is always-on)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-11 | d923074 | Initial creation |
| Implemented | 2026-03-11 | 6c1020c | Merged via PRs #5, #6, #7 |
