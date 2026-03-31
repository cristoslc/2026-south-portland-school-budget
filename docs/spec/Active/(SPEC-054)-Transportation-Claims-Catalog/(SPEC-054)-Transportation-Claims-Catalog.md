---
title: "Transportation Claims Catalog"
artifact: SPEC-054
track: implementable
status: Complete
author: cristos
created: 2026-03-30
last-updated: 2026-03-31
type: feature
parent-epic: EPIC-030
linked-artifacts:
  - INITIATIVE-006
  - EPIC-032
depends-on-artifacts: []
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Transportation Claims Catalog

## Problem Statement

The governance accountability framing of the transportation briefs requires a timestamped, source-cited record of every transportation question raised in public and every official response or non-response. This evidence is scattered across meeting transcripts and budget documents.

## Desired Outcomes

A chronological, structured catalog of the transportation evidentiary record — what was asked, what was answered, what was explicitly not answered, and what was promised but not delivered. This catalog is itself a deliverable and feeds directly into the persona briefs.

## External Behavior

**Inputs:** Existing evidence pools (same three as SPEC-051)

**Outputs:** Structured catalog at `docs/troves/transportation-claims/` containing:
- `claims.yaml` or `claims.json` — fields: claim_id, type (claim | question | non_answer | commitment), text (exact quote), source_file, source_line, speaker, date, category (cost | routing | logistics | staffing | policy | consultant), response_status (answered | unanswered | deferred | contradicted)
- `synthesis.md` — chronological narrative of the transportation evidence gap, from the Feb 4 forum busing question through the Director of Operations' confirmation that no modeling exists
- `trove.yaml` manifest

**Key entries to capture (non-exhaustive):**
- Feb 4 forum: busing question raised, no answer provided
- March 2: "we would need to kind of look at the whole picture" response
- March 2: "budgeted for transportation consultancy" commitment
- March 2: "actual cost of change in transportation routes or driver hours, we don't anticipate being a significant cost" claim
- March 2: Parent testimony on 45-minute bus rides, one-car families, aftercare
- March 2: 90% of parents worried about busing complications (survey)
- Director of Operations: confirmation no modeling exists and none before vote

## Acceptance Criteria

- Given the evidence pools, when the catalog is complete, then every transportation question and official response from Feb 4 through March 30 is captured with source citations
- Given the catalog, when filtered by response_status=unanswered, then the complete list of unresolved transportation questions is available
- Given the chronological synthesis, when read, then the pattern of deferral is visible — the same questions repeated across meetings without resolution

## Scope & Constraints

**In scope:** Extraction and structuring from existing evidence.
**Out of scope:** Assessing whether claims are accurate (that's the modeling epics). New evidence collection.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-030 |
| Complete | 2026-03-31 | — | Claims catalog and synthesis populated |
