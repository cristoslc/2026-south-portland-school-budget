---
title: "Diligent Community Agenda Scraping"
artifact: SPIKE-002
status: Complete
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
question: "Can we reliably extract meeting agenda text from the Diligent Community portal using a headless browser?"
gate: Pre-MVP
risks-addressed:
  - Diligent Community may use anti-scraping measures (CAPTCHA, bot detection)
  - Page structure may be too dynamic or session-dependent for reliable automated extraction
depends-on: []
evidence-pool: ""
---

# Diligent Community Agenda Scraping

## Question

Can we reliably extract meeting agenda text from the Diligent Community portal (southportland-gov.community.diligentoneplatform.com) using a headless browser? Specifically:

1. What is the page structure? Is agenda content rendered client-side or server-side?
2. Does the portal require authentication or use anti-bot measures?
3. Can we enumerate meetings programmatically (list page with date filtering)?
4. Is the agenda content in a parseable structure, or is it embedded in an iframe/PDF viewer?

## Go / No-Go Criteria

- **Go:** Playwright can load the meeting list page, navigate to a specific meeting, and extract agenda text as structured content (HTML with identifiable sections). No CAPTCHA or login required for public meetings.
- **No-Go:** Portal requires authentication, deploys bot detection that blocks headless browsers, or embeds agendas as non-parseable PDFs without text layers.

## Pivot Recommendation

If scraping fails: monitor the portal manually but reduce effort by setting a calendar reminder on known meeting dates and using a browser bookmarklet to extract/save the agenda text in one click. Alternatively, check if Diligent Community sends email notifications that could be parsed.

## Findings

### No scraping needed -- Diligent Community has a public REST API

The Diligent Community portal is a JavaScript SPA backed by a REST API that requires **no authentication** for public meeting data. No Playwright, no scraping, no bot detection concerns.

#### Discovered Endpoints

**Meeting list:**
```
GET /Services/MeetingsService.svc/meetings?from=2026-01-01&to=2026-12-31&loadall=false
```
Returns JSON array of meetings with `Id`, `MeetingDate`, `MeetingTypeName`, `Name`, `MeetingLocation`. Supports date range filtering.

**Meeting documents (agenda HTML):**
```
GET /Services/MeetingsService.svc/meetings/{id}/meetingDocuments
```
Returns `{ "Documents": [{ "AgendaCover": "...", "Html": "...", "Format": "docx" }] }`. The `Html` field contains the full agenda as rendered HTML -- section headings, item text, position papers, attachment references.

**Meeting metadata:**
```
GET /Services/MeetingsService.svc/meetings/{id}/meetingData
```
Returns location, date, time, and other metadata.

**Video link:**
```
GET /api/videolink/{id}
```
Returns video URL if available (empty string if not).

#### Confirmed on meeting ID 1285 (City Council, March 5, 2026)

- Meeting list endpoint returned 30 meetings in the 2026 date range
- Meeting documents endpoint returned full agenda HTML with sections (Executive Session, Opening, Petitions, Consent Calendar, etc.) and references to attached PDFs
- No CAPTCHA, no Cloudflare, no authentication required
- All endpoints respond to simple GET requests with JSON

#### Impact on EPIC-001

The Diligent Community connector is **trivial** -- it's a `curl`/`fetch` call to two API endpoints (list + documents), not a browser automation task. This significantly reduces the complexity and fragility of EPIC-001.

### Recommendation

Use direct HTTP requests (Python `requests` or `urllib`) for the Diligent Community connector. The connector should:
1. Call the meetings list endpoint with a date range
2. Filter for City Council meetings (`MeetingTypeName` contains "City Council")
3. For each new meeting, fetch the documents endpoint and extract the `Html` field
4. Convert HTML to markdown for the evidence pool

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Planned | 2026-03-10 | _pending_ | Initial creation |
| Active | 2026-03-10 | _pending_ | Beginning investigation |
| Complete | 2026-03-10 | _pending_ | Public REST API discovered; no scraping needed |
