---
title: "Split-Family Count Model"
artifact: SPEC-060
track: implementable
status: Complete
author: cristos
created: 2026-03-30
last-updated: 2026-03-31
type: feature
parent-epic: EPIC-031
linked-artifacts:
  - INITIATIVE-006
depends-on-artifacts:
  - SPEC-048
  - SPEC-055
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Split-Family Count Model

## Problem Statement

The family logistics burden of each configuration depends on how many families would have children in two different buildings simultaneously. Option A (Pre-K-1 / 2-4 split) structurally creates this for any family with children spanning the grade boundary. Option B (K-4 redistrict) doesn't. Variant C (Pre-K-2 / 3-4) creates it at a different boundary. This is the single most impactful metric for family experience and hasn't been quantified.

## Desired Outcomes

For each configuration, a credible estimate of how many families face split-building logistics in a given school year. This grounds the abstract "grade-band split" concept in a concrete number that parents and board members can react to.

## External Behavior

**Inputs:**
- Current enrollment by grade (from evidence pools / SPEC-048)
- Grade-band boundaries for each configuration
- Estimated sibling overlap rates (from census household composition data or published research on sibling grade gaps in elementary schools)

**Outputs:**
- `docs/analysis/split-family-model.md` — methodology and results
- `pipeline/transport/split_family.py` — calculation script
- Comparison table: configuration, grade_boundary, estimated_split_families, percentage_of_elementary_families

**Model mechanics:**
1. For each configuration, identify the grade boundary where children change buildings
2. Count students in the grade(s) on each side of the boundary
3. Apply sibling co-enrollment rate to estimate families (not students) affected
4. Typical sibling overlap: ~30-40% of elementary families have 2+ children in the system; of those, some fraction spans the grade boundary in any given year

**Constraints:**
- This is an estimate, not a precise count (we don't have family-level data)
- Document the sibling rate assumption and cite the source (Census Bureau SIPP data or published education research)
- The estimate should be presented as a range, not a point estimate

## Acceptance Criteria

- Given three configurations with different grade boundaries, when the model runs, then each produces a different split-family count
- Given the results, when Option A and Variant C are compared, then the impact of a Pre-K-1 boundary vs. Pre-K-2 boundary on split-family count is quantified
- Given Option B (no grade-band split), when modeled, then split-family count is zero or near-zero (confirming the structural advantage)
- Given the methodology, when reviewed, then the sibling rate assumption is cited and the sensitivity to that assumption is noted

## Scope & Constraints

**In scope:** Split-family estimation for 3 configurations.
**Out of scope:** Geographic analysis of which families are split (requires addresses). Before/after care impact (that's SPEC-064).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-031 |
| Complete | 2026-03-31 | — | Analysis implemented; see docs/analysis/ |
