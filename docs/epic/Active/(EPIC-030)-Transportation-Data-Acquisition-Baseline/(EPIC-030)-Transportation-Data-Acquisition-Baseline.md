---
title: "Transportation Data Acquisition & Baseline"
artifact: EPIC-030
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision: VISION-001
parent-initiative: INITIATIVE-006
priority-weight: high
success-criteria:
  - Maine DOE per-pupil transportation expenditure data acquired for South Portland and peer districts
  - School locations, catchment zone boundaries, and bell schedule data documented
  - Every transportation-related claim, question, and non-answer from existing evidence pools extracted and cataloged with source citations and timestamps
  - SEA staffing and contract data extracted from budget documents
  - Walk zone policy documented (current district policy, state minimums)
depends-on-artifacts: []
addresses: []
evidence-pool: ""
---

# Transportation Data Acquisition & Baseline

## Goal / Objective

Acquire the external data sources and systematically extract every transportation-related claim from the project's existing evidence pools. This epic produces the dataset that EPIC-031 (configuration modeling), EPIC-032 (briefs), and EPIC-033 (V2 optimization) all consume. Special emphasis on cataloging the evidentiary record of what was and wasn't analyzed — the Feb 4 forum busing question, the March 2 "we'd need to look at the whole picture" response, and the Director of Operations' confirmation that no modeling exists.

## Desired Outcomes

The project has a structured transportation baseline: what the district currently spends, what peer districts spend, where the schools are, how the current bus tiers work, what the SEA staffing picture looks like post-cuts, and a timestamped catalog of every public question and official non-answer about transportation. This catalog is itself a deliverable — the evidentiary record of what was not analyzed before the vote.

## Scope Boundaries

**In scope:**
- Trove collection via swain-search: Maine DOE per-pupil transport expenditure by district, peer district benchmarking data
- Extraction from existing evidence pools: SEA contract/staffing data, bell schedule references, busing cost references, transportation consultant budget line
- School location geocoding and catchment zone boundary documentation
- Walk zone policy extraction (district policy documents, Maine state law minimums)
- Chronological catalog of transportation questions raised in public comment and official responses (or non-responses)
- [SPIKE-010](../../research/Active/(SPIKE-010)-Walk-Zone-Pedestrian-Infrastructure-Audit/(SPIKE-010)-Walk-Zone-Pedestrian-Infrastructure-Audit.md): walk zone and pedestrian infrastructure audit

**Out of scope:**
- Configuration modeling (EPIC-031)
- Brief generation (EPIC-032)
- Student address data (FERPA)

## Child Specs

_To be decomposed during implementation planning._

## Key Dependencies

- Existing evidence pools (already collected)
- Maine DOE financial data portal
- City of South Portland GIS / planning data

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of INITIATIVE-006; user-approved |
