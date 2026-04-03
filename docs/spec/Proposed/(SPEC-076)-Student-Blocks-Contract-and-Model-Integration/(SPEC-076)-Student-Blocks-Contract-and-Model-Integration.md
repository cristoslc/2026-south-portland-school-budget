---
title: "Student Blocks Contract and Model Integration"
artifact: SPEC-076
track: implementable
status: Proposed
author: cristos
created: 2026-04-03
last-updated: 2026-04-03
priority-weight: high
type: feature
parent-epic: EPIC-034
parent-initiative: ""
linked-artifacts:
  - INITIATIVE-006
  - EPIC-031
depends-on-artifacts:
  - SPEC-065
addresses:
evidence-pool: sopo-redistricting-tool
source-issue: ""
swain-do: required
---

# Student Blocks Contract and Model Integration

## Problem Statement

`student_blocks.json` is easy to misuse. It is a weighted block file by grade and school. It is not a roster. It is not all whole numbers. Later work needs one contract for how the file loads, what totals it should match, and how it connects to the travel model.

## Desired Outcomes

A later reader can trust the inputs. The project has one place that says what the file is, what it is not, and what rules later work must follow.

## External Behavior

**Inputs:**
- `docs/troves/sopo-redistricting-tool/sources/sopo-data4good-repo/data/student_blocks.json`
- `docs/troves/sopo-redistricting-tool/sources/sopo-data4good-repo/src/data_loader.py`
- `docs/troves/sopo-redistricting-tool/sources/sopo-data4good-repo/src/config.py`

**Outputs:**
- A contract note listing schema, valid grade keys, valid school keys, and caveats
- A reconciliation report covering block count, grade totals, K-4 totals, and notable mismatches against config totals
- A loading step that later specs can call without guessing at the contract

**Constraints:**
- Must preserve the repo's weighted block model rather than rounding values away
- Must state clearly that the data is grouped and modeled, not raw address data
- Must disclose any mismatch between `student_blocks.json` totals and `config.py` totals

## Acceptance Criteria

- Given `student_blocks.json`, when the loader runs, then it validates top-level block IDs, grade keys, and school keys against the documented contract
- Given the loaded data, when totals are computed, then grade-level and K-4 totals are reported with any mismatch flagged explicitly
- Given the model note, when a later spec reads it, then it can reuse the data without guessing at fractional weights or caveats
- Given the repo's walkability mechanism, when integration is described, then the contract explains how block weights feed the travel model and later burden outputs

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

In scope: schema contract, reconciliation, model handoff.
Out of scope: public-facing brief copy, new travel metrics, or equity conclusions.

## Implementation Approach

Write the contract first. Then build a small load and check layer that matches the repo's assumptions. Put mismatches and caveats in the output.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-04-03 | — | Initial creation |
