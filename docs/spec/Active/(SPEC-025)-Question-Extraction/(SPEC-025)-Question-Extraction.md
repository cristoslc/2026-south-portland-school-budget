---
title: "Question Extraction"
artifact: SPEC-025
type: feature
status: Active
author: cristos
created: 2026-03-25
last-updated: 2026-03-25
parent-epic: EPIC-017
parent-initiative: INITIATIVE-004
priority-weight: high
acceptance-criteria:
  - Extraction script parses Open Questions from all briefings across all dates
  - Output JSON contains deduplicated questions with category, source persona(s), and evidence references
  - Only questions with at least one linkable evidence source are included in output
  - Each question has a stable slug for URL generation
depends-on-artifacts:
  - SPEC-022
addresses: []
---

# Question Extraction

## Problem Statement

EPIC-017 requires a question-first navigation layer, but the raw question data is scattered across 48+ briefing files as persona-voiced markdown strings. Questions overlap across personas (multiple personas ask about school closures, tax impact, etc.) and need deduplication, categorization, and evidence linking before they can be surfaced on the site.

## External Behavior

- **Input:** All briefing files in `data/interpretation/briefs/*/PERSONA-*.md`
- **Output:** `dist/questions.json` — array of deduplicated, categorized questions with evidence links
- **Invocation:** `python scripts/extract_questions.py`

### Output Schema

```json
[
  {
    "slug": "which-school-is-closing",
    "question": "Which school is formally closing?",
    "category": "School Closures & Reconfiguration",
    "personas": ["PERSONA-001", "PERSONA-000"],
    "evidence": [
      {
        "source": "school-board-budget-meetings",
        "title": "Budget Workshop 2026-03-23",
        "detail": "March 23 deck shows Kaler at zero allocation"
      }
    ],
    "context": "The budget detail shows Kaler Elementary at zero operating allocation for FY27, but no formal board vote on closure has been recorded."
  }
]
```

## Acceptance Criteria

1. Given briefings across all dates, when the extractor runs, then it parses every `## Open Questions` section from every PERSONA file
2. Given overlapping questions across personas (e.g., "Will my school close?" and "Which school is formally closing?"), when deduplicated, then semantically similar questions are merged with all source personas listed
3. Given an extracted question, when evidence linking runs, then only questions with at least one traceable evidence source (trove entry, meeting reference, budget document) are included in the output
4. Given the output JSON, when consumed by the site, then each question has a unique stable slug suitable for URL routing
5. Given the extraction, when categorized, then questions are grouped by topic (not persona) matching categories like: School Closures, Staffing, Tax Impact, Programs, Governance

## Scope & Constraints

- Uses `claude -p` for semantic deduplication and categorization (per LLM Usage Policy — no API keys)
- Questions without traceable evidence are excluded (operator decision: option B)
- The evergreen briefing (PERSONA-000) is included as a source
- Output is a build artifact in `dist/`, not committed source data

## Implementation Approach

1. **Parse briefings** — read all `data/interpretation/briefs/*/PERSONA-*.md`, extract `## Open Questions` sections
2. **Extract individual questions** — split bulleted lists, extract bolded question text and context
3. **Deduplicate** — use LLM to cluster semantically similar questions, pick canonical phrasing
4. **Categorize** — assign topic categories (LLM-assisted)
5. **Evidence link** — match question context against trove manifests and meeting sources to find linkable evidence
6. **Filter** — drop questions with zero evidence links
7. **Generate slugs** — deterministic slug from canonical question text
8. **Write JSON** — output to `dist/questions.json`

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-25 | — | Created from EPIC-017 decomposition; operator chose option B (sourced answers only) |
