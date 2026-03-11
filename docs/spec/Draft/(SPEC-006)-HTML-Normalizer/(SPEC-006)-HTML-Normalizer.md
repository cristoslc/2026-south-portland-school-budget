---
title: "HTML-to-Markdown Normalizer"
artifact: SPEC-006
status: Draft
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
parent-epic: EPIC-002
linked-research:
  - SPIKE-002
  - SPIKE-003
linked-adrs: []
depends-on: []
addresses: []
evidence-pool: ""
swain-do: required
---

# HTML-to-Markdown Normalizer

## Problem Statement

Diligent Community returns meeting agendas as HTML via its REST API (confirmed by SPIKE-002). The existing agenda sources in the city-council evidence pool are stored as plain text files that were manually extracted. This spec automates conversion of Diligent HTML agenda responses into evidence pool source markdown, producing output consistent with the existing `local` type sources.

## External Behavior

**Input:**
- HTML content (string or file) from Diligent Community API response
- Metadata: title, meeting date, source URL

**Output:**
- A markdown file matching the evidence pool source format:
  - YAML frontmatter with `source-id`, `title`, `type: local`, `path`, `fetched`, `hash`
  - Clean markdown body with agenda items, headings, and numbered lists preserved
- Updated `manifest.yaml` entry for the target evidence pool

**Preconditions:**
- HTML content has been fetched (by SPEC-002 connector or equivalent)
- Target evidence pool directory exists

**Constraints:**
- Must produce output structurally consistent with existing agenda evidence pool files (e.g., `city-council-meetings-2026/sources/008-council-agenda-2026-01-06.md`)
- SHA-256 hash computed from the HTML content (pre-conversion)
- Strip Diligent UI chrome (navigation, headers, footers) — extract agenda body only

## Acceptance Criteria

1. **Given** Diligent HTML containing a meeting agenda, **when** the normalizer runs, **then** it produces markdown with agenda items as a structured list preserving item numbers and titles.
2. **Given** HTML with nested agenda sections (e.g., executive session items, consent agenda), **when** the normalizer runs, **then** sections are represented as markdown headings with their items nested below.
3. **Given** HTML and metadata, **when** the normalizer runs, **then** the output has valid YAML frontmatter with all required fields (`source-id`, `title`, `type: local`, `path`, `fetched`, `hash`).
4. **Given** an existing evidence pool, **when** a new agenda is normalized into it, **then** `source-id` is auto-assigned as the next sequential ID.
5. **Given** a successful normalization, **when** the output is written, **then** `manifest.yaml` is updated with the new source entry.
6. **Given** the same HTML content run twice, **when** the hash matches an existing source, **then** the normalizer skips or warns.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

**In scope:**
- HTML-to-markdown conversion using a standard library (e.g., `markdownify`, `html2text`, or `beautifulsoup4` + manual conversion)
- Diligent-specific HTML structure handling (agenda body extraction)
- CLI entry point accepting HTML file/string + metadata arguments
- Manifest update and duplicate detection

**Out of scope:**
- HTML fetching from the Diligent API (EPIC-001 / SPEC-002)
- Handling non-agenda HTML (minutes, attachments)
- JavaScript-rendered content (Diligent API returns static HTML per SPIKE-002)

## Implementation Approach

1. Create `pipeline/normalize_html.py` with a `convert_html()` function
2. Use `beautifulsoup4` to parse and extract the agenda body, stripping UI chrome
3. Convert extracted HTML to markdown (either `markdownify` or manual BeautifulSoup traversal)
4. Add CLI wrapper (argparse) for standalone use
5. Share manifest update and hash/duplicate logic via `pipeline/pool_utils.py` (from SPEC-005)
6. Test against saved Diligent HTML responses, diff output against existing agenda sources

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-10 | f1208a3 | Initial creation |
