---
title: "Meaningful Document Filenames"
artifact: SPEC-024
track: implementable
status: Active
author: cristos
created: 2026-03-20
last-updated: 2026-03-20
type: enhancement
parent-epic: ""
parent-initiative: INITIATIVE-001
linked-artifacts:
  - SPEC-015
  - SPEC-023
depends-on-artifacts:
  - SPEC-013
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Meaningful Document Filenames

## Problem Statement

The budget page connector derives local filenames from the URL's last path segment (`edit`, `view`, `pubembed`) when no anchor text label is captured. The Apptegy CMS triple-escapes anchor text into a JSON blob, so `LINK_CONTEXT_RE` captures nothing — every file becomes `edit.pdf`, `view.pdf`, etc. These are neither distinct nor meaningful. Google's export endpoints return `Content-Disposition: attachment; filename*=UTF-8''<real title>.pdf` which provides the actual document title.

## External Behavior

**Inputs:** Same as SPEC-015/023 — Google Drive/Docs/Sheets/Slides export URLs.

**Outputs:**
- Downloaded files named after the document title from `Content-Disposition` (e.g., `FY27-Budget-3.9.26-Board-Meeting.pdf`)
- Fallback: Google document ID when no `Content-Disposition` (e.g., `1lNX2v1rq33OxDSmGwbsmSTjoI9z-My6mDO9qgSo3QIA.pdf`) — at minimum distinct
- Discovery history records `local_path` of the final file for skip-existing checks on subsequent runs

**Constraints:**
- No extra HTTP requests — filename derived from the download response headers only
- Existing files already on disk retain their names (not renamed retroactively)
- `local_path` added as optional field to discovery.jsonl records; old records without it fall back to file-existence scan

## Acceptance Criteria

1. **Given** a Google export URL whose response includes `Content-Disposition: attachment; filename*=UTF-8''My%20Doc.pdf`, **when** the connector downloads it, **then** the file is saved as `My-Doc.pdf` (URL-decoded, spaces → hyphens).

2. **Given** a Google export URL with no `Content-Disposition` header and no label, **when** the connector downloads it, **then** the file is named `<doc-id>.pdf` — not `edit.pdf` or `view.pdf`.

3. **Given** a file was previously downloaded and renamed to its CD name, **when** the connector runs again, **then** it skips the URL without re-downloading (uses `local_path` from history).

4. **Given** a `--check-only` run, **when** URLs are present, **then** it resolves and logs the candidate filename (from label or doc-id fallback) without downloading.

5. **Given** multiple documents from the same Google Drive with different IDs, **when** none have labels, **then** each is saved with a distinct filename.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

- Retroactive rename of already-downloaded files is out of scope
- The `DiscoveryHistory` class gains `get_record(url)` and a `local_path` kwarg on `record_attempt`
- `LINK_CONTEXT_RE` label capture is unchanged (CMS decoding improvement is a separate concern)

## Implementation Approach

1. Add `_extract_doc_id(url)` to `budget_page.py` — extracts the long alphanumeric ID from any Google URL using the existing compiled regexes.
2. Add `_parse_content_disposition(header)` — prefers `filename*=UTF-8''...` (RFC 5987), falls back to `filename=...`, URL-decodes, sanitizes (spaces → hyphens, strip unsafe chars).
3. Update `local_filename` fallback to use `_extract_doc_id` instead of last path segment.
4. Update `download_file` to return `(success, cd_filename | None)`.
5. Add `get_record(url)` to `DiscoveryHistory`; add `local_path` optional kwarg to `record_attempt`.
6. In `run()`: before download, check `record.get("local_path")` for skip-existing; after download, rename to CD name and record `local_path`.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-20 | — | Initial creation |
