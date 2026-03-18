---
title: "Diligent Community Agenda Connector"
artifact: SPEC-002
status: Complete
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
parent-epic: EPIC-001
linked-research:
  - SPIKE-002
linked-adrs: []
depends-on: []
addresses: []
trove: ""
swain-do: required
linked-epics:
  - EPIC-002
---

# Diligent Community Agenda Connector

## Problem Statement

City council meeting agendas are published on the Diligent Community portal. SPIKE-002 discovered the portal exposes a public REST API that returns agenda HTML without authentication. This connector automates fetching new agendas and saving them as text files.

## External Behavior

**Input:** Date range for meeting discovery (defaults to current month + next month).

**Output:** Agenda text files saved to:
- `data/city-council/meetings/{date}/agenda.txt`

**Preconditions:**
- Internet access to `southportland-gov.community.diligentoneplatform.com`

**Postconditions:**
- New agenda files exist for any City Council meetings not previously downloaded
- Existing agenda files are not re-downloaded or overwritten
- Meeting metadata (time, location, members) is preserved in the agenda text

**API Endpoints (from SPIKE-002):**
- Meeting list: `GET /Services/MeetingsService.svc/meetings?from={date}&to={date}&loadall=false`
- Meeting documents: `GET /Services/MeetingsService.svc/meetings/{id}/meetingDocuments`
- Meeting metadata: `GET /Services/MeetingsService.svc/meetings/{id}/meetingData`

**Interface:**
```bash
python3 scripts/connectors/diligent.py [--check-only] [--meeting-id ID] [--from DATE] [--to DATE]
```

## Acceptance Criteria

1. **Given** a date range containing City Council meetings, **when** the connector runs, **then** it discovers all meetings via the list endpoint and filters for City Council types.
2. **Given** a discovered meeting with no local agenda file, **when** the connector runs, **then** it fetches the agenda HTML, converts to plain text, and saves to the correct `data/` path.
3. **Given** a discovered meeting with an existing local agenda file, **when** the connector runs, **then** it skips the download.
4. **Given** the agenda HTML contains section headings and item text, **when** converted to text, **then** the output preserves the hierarchical structure (sections, items, position papers).
5. **Given** a meeting with no published agenda documents, **when** the connector runs, **then** it logs a note and continues without error.
6. **Given** the `--check-only` flag, **when** the connector runs, **then** it lists meetings that would be fetched but does not download anything.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Discover and filter meetings | `--check-only` found 4 City Council meetings from 90-day window, correctly filtered from all meeting types | Pass |
| AC2: Fetch and save agenda | `--meeting-id 1285` downloaded agenda for 2026-03-05 (42,658 chars) to correct path | Pass |
| AC3: Skip existing agendas | All 4 discovered meetings with existing `agenda.txt` reported "SKIP ... already exists" | Pass |
| AC4: HTML structure preserved | Output contains `#`/`##`/`###` headings, `-` list items, position papers with paragraph structure | Pass |
| AC5: Missing agenda handling | Code path logs "NO AGENDA" and increments `no_agenda` counter, verified by code inspection | Pass |
| AC6: --check-only mode | Ran `--check-only` — listed meetings with "WOULD DOWNLOAD" / "SKIP", no files written | Pass |

## Scope & Constraints

- Filters to City Council meetings only (`MeetingTypeName` contains "City Council")
- Uses Python `requests` (or `urllib`) -- no browser automation needed
- HTML-to-text conversion should preserve structure but doesn't need to be perfect markdown (that's EPIC-002's job)
- The base URL is configurable but defaults to the South Portland portal

## Implementation Approach

1. Create `scripts/connectors/diligent.py`
2. Fetch meeting list for the date range, filter to City Council
3. For each meeting, check if `data/city-council/meetings/{date}/agenda.txt` exists
4. For missing agendas, fetch the meetingDocuments endpoint, extract the `Html` field
5. Convert HTML to structured text (strip tags, preserve headings/lists)
6. Save with a header line containing the source URL

TDD cycles:
- AC1 → test meeting list filtering
- AC2+AC4 → test HTML-to-text conversion and structural preservation
- AC3 → test skip logic
- AC5 → test missing agenda handling
- AC6 → test --check-only mode

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-10 | 19807c6 | Initial creation |
| Implemented | 2026-03-10 | 4e32287 | All ACs verified, connector deployed |
