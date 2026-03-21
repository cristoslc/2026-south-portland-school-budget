---
title: "Google Slides Export Support"
artifact: SPEC-023
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
depends-on-artifacts:
  - SPEC-013
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Google Slides Export Support

## Problem Statement

The budget page at spsdme.org/budget27 currently hosts 5 Google Slides presentations (budget overview decks). The `budget_page.py` connector detects these URLs but skips them as `slides_unsupported`, logging a warning. This means budget presentation content is not available to the interpretation pipeline. Adding export support would capture slide text and imagery as PDF, making it available for lever analysis.

## External Behavior

**Inputs:**
- Google Slides `edit` URLs of the form `https://docs.google.com/presentation/d/<id>/edit?...`
- Google Slides `pubembed` URLs of the form `https://docs.google.com/presentation/d/<id>/embed...` or `https://docs.google.com/presentation/d/e/<pubid>/pubembed...`

**Outputs:**
- PDF export downloaded to `data/school-board/budget-fy27/documents/<slug>.pdf`
- Discovery history entry with `ok` status

**Preconditions:**
- Network access to docs.google.com
- Slides must be publicly accessible (no authentication required)

**Postconditions:**
- All Google Slides URLs from the budget page are downloaded as PDFs
- History file records the download with status `ok` or `failed`
- No previously-unsupported Slides URL is retried within the backoff window after a failure

**Constraints:**
- Export must work without Google API credentials (anonymous HTTP export)
- Both `edit` and `pubembed` URL variants must be handled
- `pubembed` URLs use a different ID format (`/e/<pubid>`) — export URL construction differs from `edit` URLs
- Must not change behavior for existing PDF/XLSX/Docs/Sheets downloads

## Acceptance Criteria

1. **Given** a Google Slides `edit` URL, **when** the connector classifies it, **then** it returns `type: slides_pdf` and constructs the export URL as `https://docs.google.com/presentation/d/<id>/export?format=pdf`.

2. **Given** a Google Slides `pubembed` URL with a `/e/<pubid>/` path, **when** the connector classifies it, **then** it constructs the export URL as `https://docs.google.com/presentation/d/e/<pubid>/export?format=pdf`.

3. **Given** a connector run against the live budget page, **when** Slides URLs are present, **then** each is downloaded as a PDF and recorded as `ok` in discovery history.

4. **Given** a Slides export URL returns an HTTP error, **when** the download fails, **then** it is recorded as `failed` in history and subject to normal backoff — no crash or unhandled exception.

5. **Given** a file already exists locally with the derived filename, **when** the connector runs, **then** it skips the download (same skip-existing logic as other types).

6. **Given** a `--check-only` run, **when** Slides URLs are present, **then** the connector logs `WOULD DOWNLOAD` for each without downloading.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1 — edit URL → slides_pdf + correct export URL | `TestClassifyUrl::test_edit_url_classified_as_slides_pdf` | Pass |
| AC2 — pubembed URL → slides_pdf + correct export URL | `TestClassifyUrl::test_pubembed_url_classified_as_slides_pdf` | Pass |
| AC3 — run() downloads slides as PDF, records ok | `TestRunSlidesDownload::test_edit_slides_downloaded_as_pdf`, `test_pubembed_slides_downloaded_as_pdf`, `test_both_slide_variants_downloaded` | Pass |
| AC4 — HTTP error records failed, exits 0 | `TestRunSlidesDownload::test_failed_download_records_failed_exits_0` | Pass |
| AC5 — existing file skipped | `TestRunSlidesDownload::test_existing_file_skipped` | Pass |
| AC6 — check-only creates no files | `TestRunSlidesDownload::test_check_only_does_not_download` | Pass |

## Scope & Constraints

- Only targets spsdme.org/budget27 (no change to URL scope)
- Anonymous export only — no OAuth, no Google API key
- PDF is the only export format (covers text and images; no PPTX)
- `slides_unsupported` classification and its warning log are removed — previously-skipped URLs will now be attempted on next run (backoff window may delay some)
- The `classify_url` function in `budget_page.py` is the only change surface; download mechanics are unchanged

## Implementation Approach

1. Update `classify_url` in `scripts/connectors/budget_page.py`:
   - Match `pubembed` URLs with `/e/<pubid>/` path: export URL = `https://docs.google.com/presentation/d/e/<pubid>/export?format=pdf`
   - Match `edit` Slides URLs (already matched by `SLIDES_RE`): export URL = `https://docs.google.com/presentation/d/<id>/export?format=pdf`
   - Return `("slides_pdf", export_url, ".pdf")` instead of `("slides_unsupported", None, None)`
   - Remove `slides_unsupported` branch from the main loop in `run()`

2. Update regex or add new pattern for `/e/<pubid>/` pubembed variant.

3. Remove the `SLIDES_PUBEMBED_RE` guard that short-circuits before `SLIDES_RE` is checked (or fold it into the export logic).

4. Run `uv run python3 scripts/connectors/budget_page.py --check-only` to confirm slides appear as `WOULD DOWNLOAD`.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-20 | — | Initial creation |
