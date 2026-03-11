---
title: "Budget Page PDF Connector"
artifact: SPEC-003
status: Implemented
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
parent-epic: EPIC-001
linked-research: []
linked-adrs: []
depends-on: []
addresses: []
evidence-pool: ""
swain-do: required
---

# Budget Page PDF Connector

## Problem Statement

The school district's budget page (spsdme.org/budget27) hosts meeting packets, presentation slides, and spreadsheets as downloadable files. New documents appear as the budget process progresses. This connector polls the page for new links and downloads files not yet in the local `data/` tree.

## External Behavior

**Input:** The budget page URL (defaults to `https://www.spsdme.org/budget27`).

**Output:** PDF/XLSX/PPTX files saved to the existing directory structure:
- `data/budget-fy27/meetings/{date}/packet.pdf`
- `data/budget-fy27/presentations/{date}-{slug}.pdf`
- `data/budget-fy27/documents/{date}-{slug}.xlsx`

**Preconditions:**
- Internet access to spsdme.org

**Postconditions:**
- New files are downloaded to the correct `data/` subdirectory
- Existing files are not re-downloaded
- A log of discovered vs. downloaded files is produced

**Interface:**
```bash
python3 scripts/connectors/budget_page.py [--check-only] [--url URL]
```

## Acceptance Criteria

1. **Given** the budget page contains PDF links, **when** the connector runs, **then** it discovers all downloadable document URLs on the page.
2. **Given** a discovered document URL with no local file, **when** the connector runs, **then** it downloads the file to the correct `data/` path.
3. **Given** a discovered document URL with an existing local file, **when** the connector runs, **then** it skips the download.
4. **Given** the budget page structure changes (different HTML layout), **when** the connector runs, **then** it logs a warning if zero documents are found rather than silently succeeding.
5. **Given** the `--check-only` flag, **when** the connector runs, **then** it lists documents that would be downloaded but does not download anything.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Discover document URLs | `--discover` found 14 Google Drive/Docs/Sheets links on budget page, identified 1 new link not in config | Pass |
| AC2: Download to correct path | Downloaded March 9 meeting packet (1,337,654 bytes) to `data/school-board/budget-fy27/meetings/2026-03-09-regular/packet.pdf` | Pass |
| AC3: Skip existing files | 12 of 13 configured sources reported "SKIP ... already exists" | Pass |
| AC4: Zero-doc warning | Tested against example.com — logged "Zero document links found ... page structure may have changed" | Pass |
| AC5: --check-only mode | Ran `--check-only` — listed 1 would-download + 12 skipped, no files written | Pass |

## Scope & Constraints

- The budget page is static HTML -- `requests` + `BeautifulSoup` (or similar) is sufficient
- File-to-path mapping may require manual config for the first run (mapping URL patterns to directory conventions), but should be automated for subsequent runs
- Binary files (PDF, XLSX) are gitignored -- the connector downloads them for local processing by EPIC-002
- Does not handle authentication (the budget page is public)

## Implementation Approach

1. Create `scripts/connectors/budget_page.py`
2. Fetch the budget page HTML
3. Extract all document links (filter to `.pdf`, `.xlsx`, `.pptx`)
4. Compare against existing files in `data/budget-fy27/`
5. Download missing files to the correct subdirectory
6. Log results (discovered N, downloaded M, skipped K)

TDD cycles:
- AC1 → test link extraction from sample HTML
- AC2 → test download to correct path
- AC3 → test skip logic
- AC4 → test zero-documents warning
- AC5 → test --check-only mode

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-10 | 19807c6 | Initial creation |
| Implemented | 2026-03-10 | _pending_ | All ACs verified, connector deployed |
